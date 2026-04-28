#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8010}"
OUT_FILE="${1:-reports/smoke-fullstack-report.json}"
HOLDING_USER_ID="${HOLDING_USER_ID:-HLD-002}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-15}"
RUN_ID="$(date +%s)"
SMOKE_USER_ID="USR-SMOKE-${RUN_ID}"
SMOKE_ONBOARD_USER_ID="USR-ONBOARD-${RUN_ID}"

mkdir -p "$(dirname "$OUT_FILE")"

TMP_RESULTS="$(mktemp)"
FIRST_RESULT=1
PASS=0
FAIL=0
TOTAL=0

json_escape() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'
}

append_result() {
  local item="$1"
  if [[ "$FIRST_RESULT" -eq 1 ]]; then
    printf '%s' "$item" > "$TMP_RESULTS"
    FIRST_RESULT=0
  else
    printf ',%s' "$item" >> "$TMP_RESULTS"
  fi
}

run_check() {
  local key="$1"
  local method="$2"
  local path="$3"
  local expected_code="$4"
  local body="${5:-}"
  local user_id="${6:-$HOLDING_USER_ID}"

  TOTAL=$((TOTAL + 1))

  local url="${BASE_URL}${path}"
  local response
  if [[ -n "$body" ]]; then
    response="$(curl -sS -m "$TIMEOUT_SECONDS" -w '\n%{http_code}' \
      -H "Content-Type: application/json" \
        -H "x-holding-user-id: ${user_id}" \
      -X "$method" "$url" \
      -d "$body" || true)"
  else
    response="$(curl -sS -m "$TIMEOUT_SECONDS" -w '\n%{http_code}' \
        -H "x-holding-user-id: ${user_id}" \
      -X "$method" "$url" || true)"
  fi

  local status_code
  status_code="$(printf '%s' "$response" | tail -n 1)"
  local payload
  payload="$(printf '%s' "$response" | sed '$d')"

  local ok="false"
  if [[ "$expected_code" == "2xx" ]]; then
    if [[ "$status_code" =~ ^2[0-9][0-9]$ ]]; then
      ok="true"
    fi
  elif [[ "$status_code" == "$expected_code" ]]; then
    ok="true"
  fi

  if [[ "$ok" == "true" ]]; then
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
  fi

  local payload_excerpt
  payload_excerpt="$(printf '%s' "$payload" | head -c 600 | json_escape)"
  local expected_json
  expected_json="$(printf '%s' "$expected_code" | json_escape)"

  local item
  item=$(cat <<JSON
{"key":"$key","method":"$method","path":"$path","expected":$expected_json,"status_code":"$status_code","ok":$ok,"payload_excerpt":$payload_excerpt}
JSON
)

  append_result "$item"
  printf '[%s] %s %s -> %s (expected %s)\n' "$key" "$method" "$path" "$status_code" "$expected_code"
}

echo "Iniciando smoke test full stack em ${BASE_URL}"

# Bloco 2/11: Core + Dashboard + Frontend data
run_check "B02_DASHBOARD" "GET" "/academy/dashboard" "200"
run_check "B02_ENROLL" "POST" "/academy/enroll" "201" "{\"user_id\":\"${SMOKE_USER_ID}\",\"course_id\":\"CRS-001\",\"source\":\"smoke\"}"
run_check "B02_LESSON_COMPLETE" "POST" "/academy/lesson/complete" "200" "{\"user_id\":\"${SMOKE_USER_ID}\",\"lesson_id\":\"LSN-001-${RUN_ID}\",\"score\":82}"

# Bloco 5/6: Compliance + HubBackoffice
run_check "B05_COMPLIANCE" "POST" "/academy/compliance?user_id=${SMOKE_USER_ID}" "200"
run_check "B06_ONBOARDING" "POST" "/academy/onboarding" "201" "{\"user_id\":\"${SMOKE_ONBOARD_USER_ID}\",\"role\":\"vendas\",\"contract_type\":\"clt\"}"

# Bloco 7/8: Simulação + Kanban
run_check "B07_SIMULATE" "POST" "/academy/simulate" "200" "" "HLD-005"
run_check "B08_FROM_TASK" "POST" "/academy/from-task" "201" '{"task_id":"TASK-001","domain":"negociacao"}'

# Bloco 9/10: Métricas + RBAC
run_check "B09_METRICS" "GET" "/academy/metrics" "200"
run_check "B10_RBAC" "GET" "/academy/rbac/roles" "200"

# Operação institucional
run_check "OPS_EVENTS" "GET" "/academy/events" "200"
run_check "OPS_INSTITUTIONAL_DASH" "GET" "/academy/dashboard/institutional" "200"
run_check "OPS_RANKING" "GET" "/academy/ranking/gamified" "200"

GENERATED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat > "$OUT_FILE" <<JSON
{
  "generated_at": "$GENERATED_AT",
  "base_url": "$BASE_URL",
  "holding_user_id": "$HOLDING_USER_ID",
  "summary": {
    "total": $TOTAL,
    "passed": $PASS,
    "failed": $FAIL,
    "success_rate": "$(python3 - <<PY
total = $TOTAL
passed = $PASS
print(f"{(passed/total*100):.1f}%" if total else "0.0%")
PY
)"
  },
  "results": [
$(cat "$TMP_RESULTS")
  ]
}
JSON

rm -f "$TMP_RESULTS"

echo "Relatório salvo em: $OUT_FILE"
if [[ "$FAIL" -gt 0 ]]; then
  echo "Smoke test finalizado com falhas: $FAIL/$TOTAL"
  exit 1
fi

echo "Smoke test finalizado com sucesso: $PASS/$TOTAL"
