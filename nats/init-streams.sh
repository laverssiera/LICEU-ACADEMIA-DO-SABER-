#!/bin/sh
# ────────────────────────────────────────────────────────
# NATS JetStream — Inicialização de Streams
# Academia do Saber — LICEU Ecossistema
# Uso: ./nats/init-streams.sh [nats_url]
# ────────────────────────────────────────────────────────

NATS_URL="${1:-nats://localhost:4222}"

echo "Conectando em $NATS_URL ..."

# ── Stream: ACADEMY ──────────────────────────────────────
# Eventos educacionais core
nats -s "$NATS_URL" stream add ACADEMY \
  --subjects "academy.*,academy.lesson.*,academy.course.*" \
  --storage file \
  --retention limits \
  --max-msgs=-1 \
  --max-age=72h \
  --replicas=1 2>/dev/null && echo "✓ Stream ACADEMY criado" || echo "→ Stream ACADEMY já existe"

# ── Stream: JOHN ─────────────────────────────────────────
# Eventos do motor de IA John
nats -s "$NATS_URL" stream add JOHN \
  --subjects "john.*" \
  --storage file \
  --retention limits \
  --max-msgs=50000 \
  --max-age=24h \
  --replicas=1 2>/dev/null && echo "✓ Stream JOHN criado" || echo "→ Stream JOHN já existe"

# ── Stream: CORE_DNA ─────────────────────────────────────
# Feed de conhecimento para o core_dna do John
nats -s "$NATS_URL" stream add CORE_DNA \
  --subjects "core_dna.*" \
  --storage file \
  --retention limits \
  --max-msgs=100000 \
  --max-age=168h \
  --replicas=1 2>/dev/null && echo "✓ Stream CORE_DNA criado" || echo "→ Stream CORE_DNA já existe"

# ── Stream: HUB ──────────────────────────────────────────
# Integração com HubBackoffice (RH + DP)
nats -s "$NATS_URL" stream add HUB \
  --subjects "hub.*" \
  --storage file \
  --retention limits \
  --max-msgs=-1 \
  --max-age=48h \
  --replicas=1 2>/dev/null && echo "✓ Stream HUB criado" || echo "→ Stream HUB já existe"

# ── Stream: JURIDICO ─────────────────────────────────────
# Integração com JuridicoTech
nats -s "$NATS_URL" stream add JURIDICO \
  --subjects "juridico.*" \
  --storage file \
  --retention limits \
  --max-msgs=-1 \
  --max-age=168h \
  --replicas=1 2>/dev/null && echo "✓ Stream JURIDICO criado" || echo "→ Stream JURIDICO já existe"

# ── Stream: KANBAN ────────────────────────────────────────
# Task learning via Kanban Global
nats -s "$NATS_URL" stream add KANBAN \
  --subjects "kanban.*" \
  --storage file \
  --retention limits \
  --max-msgs=-1 \
  --max-age=24h \
  --replicas=1 2>/dev/null && echo "✓ Stream KANBAN criado" || echo "→ Stream KANBAN já existe"

# ── Consumers: academy.enrolled ──────────────────────────
nats -s "$NATS_URL" consumer add ACADEMY academy-enrolled-consumer \
  --filter "academy.enrolled" \
  --deliver all \
  --ack explicit \
  --pull 2>/dev/null && echo "✓ Consumer academy-enrolled-consumer criado" || true

nats -s "$NATS_URL" consumer add ACADEMY academy-certified-consumer \
  --filter "academy.certified" \
  --deliver all \
  --ack explicit \
  --pull 2>/dev/null && echo "✓ Consumer academy-certified-consumer criado" || true

echo ""
echo "────────────────────────────────────────────────────"
echo "✅  NATS JetStream inicializado para Academia do Saber"
echo "────────────────────────────────────────────────────"
echo ""
echo "Streams disponíveis:"
nats -s "$NATS_URL" stream list
