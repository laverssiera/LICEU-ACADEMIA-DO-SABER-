#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-laverssiera/LICEU-ACADEMIA-DO-SABER-}"
README_PATH="README.md"

if ! command -v gh >/dev/null 2>&1; then
  echo "Erro: gh nao encontrado no PATH." >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Erro: jq nao encontrado no PATH." >&2
  exit 1
fi

if [[ ! -f "$README_PATH" ]]; then
  echo "Erro: README nao encontrado em $README_PATH" >&2
  exit 1
fi

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

issues_json="$tmp_dir/issues.json"
block_states="$tmp_dir/block_states.tsv"
agg_counts="$tmp_dir/agg.tsv"
table_md="$tmp_dir/table.md"
new_readme="$tmp_dir/README.new.md"

# Busca todas as issues com o padrao [ISSUE N] e extrai bloco + estado.
gh issue list \
  --repo "$REPO" \
  --state all \
  --limit 200 \
  --json title,state,labels > "$issues_json"

jq -r '
  .[]
  | select(.title | test("^\\[ISSUE [0-9]+\\]"))
  | [
      ([.labels[].name | select(test("^bloco-[0-9]+-"))] | first // ""),
      .state
    ]
  | @tsv
' "$issues_json" \
| awk -F '\t' '$1 != "" { print $1 "\t" $2 }' > "$block_states"

awk -F '\t' '
  {
    total[$1]++
    if ($2 == "OPEN") open[$1]++
    if ($2 == "CLOSED") closed[$1]++
  }
  END {
    for (k in total) {
      printf "%s\t%d\t%d\t%d\n", k, total[k], open[k] + 0, closed[k] + 0
    }
  }
' "$block_states" > "$agg_counts"

cat > "$table_md" <<'EOF'
| Bloco | Tema | Quantidade de Issues | Status |
|-------|------|----------------------|--------|
EOF

append_row() {
  local label="$1"
  local bloco="$2"
  local tema="$3"

  local metrics
  metrics="$(awk -F '\t' -v key="$label" '$1 == key { print $2 "\t" $3 "\t" $4 }' "$agg_counts")"

  local total=0
  local open=0
  local closed=0

  if [[ -n "$metrics" ]]; then
    IFS=$'\t' read -r total open closed <<< "$metrics"
  fi

  local status="Aberto"
  if [[ "$total" -eq 0 ]]; then
    status="Sem issues"
  elif [[ "$closed" -eq "$total" ]]; then
    status="Concluido"
  elif [[ "$open" -gt 0 && "$closed" -gt 0 ]]; then
    status="Em andamento"
  fi

  printf "| %s | %s | %d | %s |\n" "$bloco" "$tema" "$total" "$status" >> "$table_md"

  TOTAL_ISSUES=$((TOTAL_ISSUES + total))
  TOTAL_OPEN=$((TOTAL_OPEN + open))
  TOTAL_CLOSED=$((TOTAL_CLOSED + closed))
}

TOTAL_ISSUES=0
TOTAL_OPEN=0
TOTAL_CLOSED=0

append_row "bloco-1-foundation" "Bloco 1" "Foundation"
append_row "bloco-2-john" "Bloco 2" "John Training Engine"
append_row "bloco-3-simulacao" "Bloco 3" "Treinamento Operacional"
append_row "bloco-4-rh" "Bloco 4" "HubBackoffice (RH + DP)"
append_row "bloco-5-juridico" "Bloco 5" "JuridicoTech"
append_row "bloco-6-metrics" "Bloco 6" "Metrics"
append_row "bloco-7-edtech" "Bloco 7" "EdTech Externo"
append_row "bloco-8-nats" "Bloco 8" "NATS"
append_row "bloco-9-cefeida" "Bloco 9" "CEFEIDA"
append_row "bloco-10-ui" "Bloco 10" "Trading Desk"
append_row "bloco-11-rbac" "Bloco 11" "RBAC"
append_row "bloco-12-core-dna" "Bloco 12" "Core_DNA + John"
append_row "bloco-13-kanban" "Bloco 13" "Kanban Global"
append_row "bloco-14-infra" "Bloco 14" "Infra / Deploy"

printf "| **Total** |  | **%d** | **%d abertas / %d fechadas** |\n" \
  "$TOTAL_ISSUES" "$TOTAL_OPEN" "$TOTAL_CLOSED" >> "$table_md"

awk -v table_file="$table_md" '
  BEGIN {
    in_block = 0
    while ((getline line < table_file) > 0) {
      table = table line "\n"
    }
    close(table_file)
  }
  /<!-- ROADMAP_STATUS_TABLE:BEGIN -->/ {
    print
    printf "%s", table
    in_block = 1
    next
  }
  /<!-- ROADMAP_STATUS_TABLE:END -->/ {
    in_block = 0
    print
    next
  }
  in_block == 0 { print }
' "$README_PATH" > "$new_readme"

mv "$new_readme" "$README_PATH"

echo "Tabela de status atualizada em $README_PATH para o repo $REPO"
