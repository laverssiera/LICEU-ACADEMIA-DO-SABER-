#!/usr/bin/env bash
set -euo pipefail

ALERTMANAGER_URL="${ALERTMANAGER_URL:-http://localhost:9093}"
CREATED_BY="${ALERTMANAGER_CREATED_BY:-ops-liceu}"
DEFAULT_DOMAIN="${ALERTMANAGER_DEFAULT_DOMAIN:-education}"

usage() {
  cat <<'EOF'
Usage:
  scripts/alertmanager-silence.sh create [--duration 60m] [--domain education] [--alertname NAME] [--comment TEXT]
  scripts/alertmanager-silence.sh list
  scripts/alertmanager-silence.sh expire --id SILENCE_ID

Environment variables:
  ALERTMANAGER_URL            Default: http://localhost:9093
  ALERTMANAGER_CREATED_BY     Default: ops-liceu
  ALERTMANAGER_DEFAULT_DOMAIN Default: education

Examples:
  scripts/alertmanager-silence.sh create --duration 2h --domain education --comment "maintenance window"
  scripts/alertmanager-silence.sh create --duration 30m --domain education --alertname CivilizationEducationSyncStale
  scripts/alertmanager-silence.sh list
  scripts/alertmanager-silence.sh expire --id 7fb6f353-8f3f-4d9c-8f90-9f5f9f2449f8
EOF
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

iso_now() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

iso_plus_duration() {
  local duration="$1"
  date -u -d "+${duration}" +"%Y-%m-%dT%H:%M:%SZ"
}

json_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/ }"
  printf '%s' "$value"
}

create_silence() {
  local duration="60m"
  local domain="$DEFAULT_DOMAIN"
  local alertname=""
  local comment="maintenance window"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --duration)
        duration="$2"
        shift 2
        ;;
      --domain)
        domain="$2"
        shift 2
        ;;
      --alertname)
        alertname="$2"
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
        echo "Unknown option for create: $1" >&2
        usage
        exit 1
        ;;
    esac
  done

  local starts_at
  local ends_at
  starts_at="$(iso_now)"
  if ! ends_at="$(iso_plus_duration "$duration")"; then
    echo "Invalid duration: $duration. Use values like 30m, 1h, 2h." >&2
    exit 1
  fi

  local matchers
  matchers='[{"name":"domain","value":"'"$(json_escape "$domain")"'","isRegex":false}]'
  if [[ -n "$alertname" ]]; then
    matchers='[{"name":"domain","value":"'"$(json_escape "$domain")"'","isRegex":false},{"name":"alertname","value":"'"$(json_escape "$alertname")"'","isRegex":false}]'
  fi

  local payload
  payload='{"matchers":'"$matchers"',"startsAt":"'"$starts_at"'","endsAt":"'"$ends_at"'","createdBy":"'"$(json_escape "$CREATED_BY")"'","comment":"'"$(json_escape "$comment")"'"}'

  curl -fsS -X POST \
    "${ALERTMANAGER_URL}/api/v2/silences" \
    -H "Content-Type: application/json" \
    -d "$payload"

  echo
  echo "Silence created for domain=${domain} duration=${duration}"
}

list_silences() {
  curl -fsS "${ALERTMANAGER_URL}/api/v2/silences"
  echo
}

expire_silence() {
  local silence_id=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id)
        silence_id="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown option for expire: $1" >&2
        usage
        exit 1
        ;;
    esac
  done

  if [[ -z "$silence_id" ]]; then
    echo "Missing required option: --id" >&2
    usage
    exit 1
  fi

  curl -fsS -X DELETE "${ALERTMANAGER_URL}/api/v2/silence/${silence_id}"
  echo
  echo "Silence expired: ${silence_id}"
}

main() {
  require_cmd curl
  require_cmd date

  if [[ $# -eq 0 ]]; then
    usage
    exit 1
  fi

  local command="$1"
  shift

  case "$command" in
    create)
      create_silence "$@"
      ;;
    list)
      list_silences
      ;;
    expire)
      expire_silence "$@"
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