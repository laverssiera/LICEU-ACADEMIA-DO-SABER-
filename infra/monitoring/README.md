# Monitoring

Stack de observabilidade para metricas, logs e traces do ecossistema LICEU.

## Visao Geral

Camada de observabilidade para operacao, diagnostico e analise de desempenho dos servicos.

## Componentes

- Prometheus
- Alertmanager
- Grafana
- Loki
- Tempo
- OpenTelemetry
- Jaeger

## Objetivo

Oferecer visibilidade operacional de servicos, desempenho de API e saude de integracoes em tempo real.

## Civilization Education Metrics

Métricas expostas pelo runtime em /metrics para acompanhar sincronização entre Academia e Civilization Brain:

- civilization_education_brain_sync_total{status="success|failure"}
- civilization_education_signals_published_total
- civilization_education_global_intelligence_score
- civilization_education_global_events
- civilization_education_last_sync_timestamp_seconds

## Prometheus Queries

- Taxa de sucesso de sync (5m):
	- rate(civilization_education_brain_sync_total{status="success"}[5m])
- Taxa de falha de sync (5m):
	- rate(civilization_education_brain_sync_total{status="failure"}[5m])
- Sinais publicados por minuto:
	- rate(civilization_education_signals_published_total[1m])
- Score global de inteligencia educacional:
	- civilization_education_global_intelligence_score
- Eventos globais acumulados:
	- civilization_education_global_events
- Idade do ultimo sync (segundos):
	- time() - civilization_education_last_sync_timestamp_seconds

## Grafana Panels

- Sync Success vs Failure (time series)
- Published Educational Signals (time series)
- Global Intelligence Score (gauge)
- Global Educational Events (stat)
- Last Sync Freshness (stat)

## Dashboard JSON

Dashboard pronto para importacao:

- infra/monitoring/grafana/dashboards/civilization-education-sync-dashboard.json

## Provisioning Automatico

Arquivos de provisioning para carregar datasource e dashboards automaticamente no startup do Grafana:

- infra/monitoring/grafana/provisioning/datasources/prometheus.yml
- infra/monitoring/grafana/provisioning/dashboards/dashboards.yml

Configuracao Prometheus utilizada no stack de observabilidade:

- infra/monitoring/prometheus/prometheus.yml
- infra/monitoring/prometheus/alerts/civilization-education-alerts.yml
- infra/monitoring/alertmanager/alertmanager.yml

Subir stack de observabilidade com provisioning:

- cd academia-do-saber
- docker compose -f docker-compose.observability.yml up -d

Webhook de notificacao (opcional, default local):

- ALERTMANAGER_WEBHOOK_URL=http://host.docker.internal:19093/alerts docker compose -f docker-compose.observability.yml up -d

Slack nativo por severidade (warning/critical):

- ALERTMANAGER_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
- ALERTMANAGER_SLACK_CHANNEL_WARNING=#civilization-warning
- ALERTMANAGER_SLACK_CHANNEL_CRITICAL=#civilization-critical

Exemplo:

- ALERTMANAGER_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ ALERTMANAGER_SLACK_CHANNEL_WARNING=#civilization-warning ALERTMANAGER_SLACK_CHANNEL_CRITICAL=#civilization-critical docker compose -f docker-compose.observability.yml up -d

## Alertas Provisionados

Regras ativas no Prometheus para a malha educacional civilizacional:

- CivilizationEducationSyncFailuresHigh
- CivilizationEducationSyncStale
- CivilizationEducationGlobalIntelligenceLow
- CivilizationEducationSignalsFlatline

Rotas no Alertmanager:

- Todos os alertas -> receiver civilization-webhook
- severity=warning -> receiver civilization-slack-warning
- severity=critical -> receiver civilization-slack-critical

Inibicao e escalonamento:

- Warning e inibido quando existir Critical com mesmo alertname e domain
- Critical notifica com menor latencia (group_wait=10s, repeat_interval=30m)
- Warning notifica com menor ruido (group_wait=1m, repeat_interval=2h)

Maintenance mode:

- Alertas com label maintenance="true" sao suprimidos no receiver civilization-maintenance-drop
- Use silences via API do Alertmanager para janelas planejadas sem alterar regras

Exemplo de silence por domain=education por 60 minutos:

- curl -X POST http://localhost:9093/api/v2/silences -H "Content-Type: application/json" -d '{"matchers":[{"name":"domain","value":"education","isRegex":false}],"startsAt":"2026-05-23T10:00:00Z","endsAt":"2026-05-23T11:00:00Z","createdBy":"ops-liceu","comment":"maintenance window"}'

Listar silences:

- curl http://localhost:9093/api/v2/silences

Script operacional para maintenance windows:

- scripts/alertmanager-silence.sh create --duration 60m --domain education --comment "maintenance window"
- scripts/alertmanager-silence.sh create --duration 30m --domain education --alertname CivilizationEducationSyncStale --comment "sync tuning"
- scripts/alertmanager-silence.sh list
- scripts/alertmanager-silence.sh expire --id <SILENCE_ID>

Script por servico para abrir/fechar janela de manutencao automaticamente:

- scripts/maintenance-window.sh open --service civilization-runtime --duration 90m --comment "upgrade deployment"
- scripts/maintenance-window.sh open --service civilization-runtime,academia-runtime --duration 45m --comment "coordinated deploy"
- scripts/maintenance-window.sh status --service civilization-runtime
- scripts/maintenance-window.sh status --service civilization-runtime,academia-runtime
- scripts/maintenance-window.sh status --all
- scripts/maintenance-window.sh close --service civilization-runtime
- scripts/maintenance-window.sh close --all

Verificacao rapida:

- Abrir Prometheus em http://localhost:9090/rules
- Confirmar carregamento do grupo civilization-education-alerts
- Abrir Alertmanager em http://localhost:9093
- Confirmar alertas ativos em http://localhost:9093/#/alerts
