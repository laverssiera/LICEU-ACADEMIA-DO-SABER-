#!/usr/bin/env bash
set -euo pipefail

ALERTMANAGER_URL="${ALERTMANAGER_URL:-http://localhost:9093}"
CREATED_BY="${ALERTMANAGER_CREATED_BY:-ops-liceu}"
DEFAULT_DOMAIN="${ALERTMANAGER_DEFAULT_DOMAIN:-education}"
STATE_DIR="${MAINTENANCE_STATE_DIR:-/tmp/liceu-maintenance}"

usage() {
  cat <<'EOF'
Usage:
  scripts/maintenance-window.sh open --service SERVICE[,SERVICE2] [--duration 60m] [--domain education] [--comment TEXT]
  scripts/maintenance-window.sh close --service SERVICE[,SERVICE2] [--id SILENCE_ID]
  scripts/maintenance-window.sh close --all
  scripts/maintenance-window.sh status --service SERVICE[,SERVICE2]
  scripts/maintenance-window.sh status --all

Environment variables:
  ALERTMANAGER_URL            Default: http://localhost:9093
  ALERTMANAGER_CREATED_BY     Default: ops-liceu
  ALERTMANAGER_DEFAULT_DOMAIN Default: education
  MAINTENANCE_STATE_DIR       Default: /tmp/liceu-maintenance

Examples:
  scripts/maintenance-window.sh open --service civilization-runtime --duration 90m
  scripts/maintenance-window.sh open --service civilization-runtime,academia-runtime --duration 30m
  scripts/maintenance-window.sh close --service civilization-runtime
  scripts/maintenance-window.sh close --all
  scripts/maintenance-window.sh status --service civilization-runtime,academia-runtime
  scripts/maintenance-window.sh status --all
EOF
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

json_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/ }"
  printf '%s' "$value"
}

iso_now() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

iso_plus_duration() {
  local duration="$1"
  date -u -d "+${duration}" +"%Y-%m-%dT%H:%M:%SZ"
}

state_file_for_service() {
  local service="$1"
  mkdir -p "$STATE_DIR"
  printf "%s/%s.silence-id" "$STATE_DIR" "$service"
}

list_state_services() {
  if [[ ! -d "$STATE_DIR" ]]; then
    return 0
  fi

  shopt -s nullglob
  local file
  for file in "$STATE_DIR"/*.silence-id; do
    basename "$file" .silence-id
  done
  shopt -u nullglob
}

extract_silence_id() {
  local response="$1"
  # Alertmanager API typically returns {"silenceID":"..."}
  sed -n 's/.*"silenceID"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' <<<"$response"
}

parse_service_list() {
  local raw_services="$1"
  local parsed=()
  local item=""

  IFS=',' read -r -a parsed <<<"$raw_services"
  for item in "${parsed[@]}"; do
    item="${item//[[:space:]]/}"
    if [[ -n "$item" ]]; then
      echo "$item"
    fi
  done
}

open_window() {
  local service=""
  local services_input=""
  local duration="60m"
  local domain="$DEFAULT_DOMAIN"
  local comment="maintenance window"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --service)
        services_input="$2"
        shift 2
        ;;
      --duration)
        duration="$2"
        shift 2
        ;;
      --domain)
        domain="$2"
        shift 2
        ;;
      --comment)
        comment="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown option for open: $1" >&2
        usage
        exit 1
        ;;
    esac
  done

  if [[ -z "$services_input" ]]; then
    echo "Missing required option: --service" >&2
    exit 1
  fi

  local starts_at ends_at
  starts_at="$(iso_now)"
  if ! ends_at="$(iso_plus_duration "$duration")"; then
    echo "Invalid duration: $duration. Use values like 30m, 1h, 2h." >&2
    exit 1
  fi

  while IFS= read -r service; do
    local full_comment
    full_comment="${comment} | service=${service} | maintenance=true"

    local payload
    payload=$(cat <<EOF
{"matchers":[
{"name":"domain","value":"$(json_escape "$domain")","isRegex":false},
{"name":"service","value":"$(json_escape "$service")","isRegex":false},
{"name":"maintenance","value":"true","isRegex":false}
],"startsAt":"${starts_at}","endsAt":"${ends_at}","createdBy":"$(json_escape "$CREATED_BY")","comment":"$(json_escape "$full_comment")"}
EOF
)

    local response
    response="$(curl -fsS -X POST "${ALERTMANAGER_URL}/api/v2/silences" -H "Content-Type: application/json" -d "$payload")"

    local silence_id
    silence_id="$(extract_silence_id "$response")"

    if [[ -z "$silence_id" ]]; then
      echo "Could not parse silence id from response: $response" >&2
      exit 1
    fi

    local state_file
    state_file="$(state_file_for_service "$service")"
    printf '%s\n' "$silence_id" > "$state_file"

    echo "Maintenance window opened"
    echo "service=${service}"
    echo "silence_id=${silence_id}"
    echo "starts_at=${starts_at}"
    echo "ends_at=${ends_at}"
    echo "state_file=${state_file}"
  done < <(parse_service_list "$services_input")
}

close_window() {
  local service=""
  local services_input=""
  local silence_id=""
  local close_all="false"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --service)
        services_input="$2"
        shift 2
        ;;
      --all)
        close_all="true"
        shift
        ;;
      --id)
        silence_id="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown option for close: $1" >&2
        usage
        exit 1
        ;;
    esac
  done

  if [[ "$close_all" == "true" && -n "$services_input" ]]; then
    echo "Use either --service or --all, not both." >&2
    exit 1
  fi

  if [[ "$close_all" == "true" && -n "$silence_id" ]]; then
    echo "--id is not supported with --all." >&2
    exit 1
  fi

  if [[ "$close_all" != "true" && -z "$services_input" ]]; then
    echo "Missing required option: --service or --all" >&2
    exit 1
  fi

  if [[ "$close_all" == "true" ]]; then
    services_input="$(list_state_services | paste -sd, -)"
    if [[ -z "$services_input" ]]; then
      echo "No local maintenance silences found in ${STATE_DIR}"
      exit 0
    fi
  fi

  while IFS= read -r service; do
    local effective_silence_id="$silence_id"

    if [[ -z "$effective_silence_id" ]]; then
      local state_file
      state_file="$(state_file_for_service "$service")"
      if [[ ! -f "$state_file" ]]; then
        echo "No stored silence id for service=${service}. Provide --id." >&2
        exit 1
      fi
      effective_silence_id="$(<"$state_file")"
    fi

    curl -fsS -X DELETE "${ALERTMANAGER_URL}/api/v2/silence/${effective_silence_id}" >/dev/null

    local state_file
    state_file="$(state_file_for_service "$service")"
    if [[ -f "$state_file" ]]; then
      rm -f "$state_file"
    fi

    echo "Maintenance window closed"
    echo "service=${service}"
    echo "silence_id=${effective_silence_id}"
  done < <(parse_service_list "$services_input")
}

status_window() {
  local service=""
  local services_input=""
  local status_all="false"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --service)
        services_input="$2"
        shift 2
        ;;
      --all)
        status_all="true"
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown option for status: $1" >&2
        usage
        exit 1
        ;;
    esac
  done

  if [[ "$status_all" == "true" && -n "$services_input" ]]; then
    echo "Use either --service or --all, not both." >&2
    exit 1
  fi

  if [[ "$status_all" != "true" && -z "$services_input" ]]; then
    echo "Missing required option: --service or --all" >&2
    exit 1
  fi

  if [[ "$status_all" == "true" ]]; then
    services_input="$(list_state_services | paste -sd, -)"
    if [[ -z "$services_input" ]]; then
      echo "No local maintenance silences found in ${STATE_DIR}"
      exit 0
    fi
  fi

  while IFS= read -r service; do
    local state_file
    state_file="$(state_file_for_service "$service")"

    if [[ ! -f "$state_file" ]]; then
      echo "No local maintenance silence stored for service=${service}"
      continue
    fi

    local silence_id
    silence_id="$(<"$state_file")"

    echo "Stored maintenance silence"
    echo "service=${service}"
    echo "silence_id=${silence_id}"
    echo "state_file=${state_file}"
    echo "hint: scripts/alertmanager-silence.sh list"
  done < <(parse_service_list "$services_input")
}

main() {
  require_cmd curl
  require_cmd date
  require_cmd sed

  if [[ $# -eq 0 ]]; then
    usage
    exit 1
  fi

  local command="$1"
  shift

  case "$command" in
    open)
      open_window "$@"
      ;;
    close)
      close_window "$@"
      ;;
    status)
      status_window "$@"
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown command: ${command}" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
