#!/usr/bin/env bash

set -u

BASE_URL="${BASE_URL:-http://localhost:8000}"
TMP_DIR="$(mktemp -d)"
PASS_COUNT=0
FAIL_COUNT=0

cleanup() {
  rm -rf "$TMP_DIR"
}

trap cleanup EXIT

run_check() {
  local name="$1"
  local method="$2"
  local path="$3"
  local payload_file="$4"
  local expect_field="$5"

  local body_file="$TMP_DIR/${name}.json"
  local status

  if [[ -n "$payload_file" ]]; then
    status="$(curl -sS -o "$body_file" -w "%{http_code}" -X "$method" "${BASE_URL}${path}" -H "Content-Type: application/json" --data-binary "@$payload_file")"
  else
    status="$(curl -sS -o "$body_file" -w "%{http_code}" -X "$method" "${BASE_URL}${path}")"
  fi

  if [[ "$status" == "200" ]] && grep -q "$expect_field" "$body_file"; then
    echo "[PASS] $name -> HTTP $status"
    PASS_COUNT=$((PASS_COUNT + 1))
  else
    echo "[FAIL] $name -> HTTP $status"
    echo "Resposta:"
    cat "$body_file"
    echo
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
}

cat > "$TMP_DIR/autonomic_payload.json" <<'JSON'
{
  "student_id": "student-001",
  "discipline": "physics",
  "cognition_score": 0.82,
  "consistency": 0.74,
  "engagement": 0.91
}
JSON

cat > "$TMP_DIR/memory_mesh_payload.json" <<'JSON'
{
  "student_id": "student-002",
  "discipline": "chemistry",
  "cognition_score": 0.65,
  "consistency": 0.55,
  "engagement": 0.62
}
JSON

cat > "$TMP_DIR/reasoning_payload.json" <<'JSON'
{
  "student_id": "student-003",
  "discipline": "mathematics",
  "cognition_score": 0.48,
  "consistency": 0.52,
  "engagement": 0.50
}
JSON

cat > "$TMP_DIR/civilization_payload.json" <<'JSON'
{
  "federation_id": "federation-01",
  "region": "americas",
  "cognition_sync": 0.83,
  "curriculum_sync": 0.78,
  "intervention_sync": 0.81
}
JSON

cat > "$TMP_DIR/identity_payload.json" <<'JSON'
{
  "student_id": "student-004",
  "ecosystem": "academy",
  "discipline": "biology",
  "cognition_score": 0.79,
  "consistency": 0.73,
  "engagement": 0.76
}
JSON

echo "Executando smoke tests em: $BASE_URL"

run_check "autonomic_evaluate" "POST" "/education/autonomic/evaluate" "$TMP_DIR/autonomic_payload.json" "educational_autonomic_operational"
run_check "autonomic_history" "GET" "/education/autonomic/history?limit=20" "" "runtime_identity"

run_check "memory_mesh_upsert" "POST" "/education/memory-mesh/upsert" "$TMP_DIR/memory_mesh_payload.json" "educational_memory_mesh_operational"
run_check "memory_mesh_student" "GET" "/education/memory-mesh/student/student-002?limit=20" "" "student_id"
run_check "memory_mesh_snapshot" "GET" "/education/memory-mesh/snapshot?limit=20" "" "intervention_distribution"

run_check "pedagogical_reasoning_reason" "POST" "/education/pedagogical-reasoning/reason" "$TMP_DIR/reasoning_payload.json" "pedagogical_reasoning_operational"
run_check "pedagogical_reasoning_history" "GET" "/education/pedagogical-reasoning/history?limit=20" "" "runtime_identity"

run_check "civilization_sync_synchronize" "POST" "/education/civilization-sync/synchronize" "$TMP_DIR/civilization_payload.json" "civilization_education_sync_operational"
run_check "civilization_sync_history" "GET" "/education/civilization-sync/history?limit=20" "" "runtime_identity"

run_check "federated_identity_generate" "POST" "/education/federated-identity/generate" "$TMP_DIR/identity_payload.json" "federated_learning_identity_operational"
run_check "federated_identity_history" "GET" "/education/federated-identity/history?limit=20" "" "runtime_identity"

echo
echo "Resumo: PASS=$PASS_COUNT FAIL=$FAIL_COUNT TOTAL=$((PASS_COUNT + FAIL_COUNT))"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  exit 1
fi

exit 0