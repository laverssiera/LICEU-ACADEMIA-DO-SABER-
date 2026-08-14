# Academy Learning Core - Plano de Execucao e Capacidade

Data: 2026-05-09
Escopo: Issues #37, #38, #39 e subtasks #40 a #48

## Restricao encontrada
A criacao de GitHub Project (board nativa) falhou por permissao da integracao:
- GraphQL: Resource not accessible by integration (createProjectV2)

## Board operacional (fallback)
Status padrao: To do -> In progress -> Done

### Sprint 1 (base funcional)
- #40 SUBTASK-ACA-001-01 Backend Learning Contract API
- #43 SUBTASK-ACA-002-01 Motor de regras adaptativas
- #44 SUBTASK-ACA-002-02 Endpoint de execucao adaptativa
- #46 SUBTASK-ACA-003-01 Contratos de evento de conhecimento

### Sprint 2 (confiabilidade e validacao)
- #41 SUBTASK-ACA-001-02 Aceite e trilha de auditoria
- #45 SUBTASK-ACA-002-03 Testes do Adaptive Runtime
- #47 SUBTASK-ACA-003-02 Pub Sub e idempotencia

### Sprint 3 (fechamento e observabilidade)
- #42 SUBTASK-ACA-001-03 Testes Learning Contracts
- #48 SUBTASK-ACA-003-03 Observabilidade e testes sync

## Plano de capacidade sugerido
Premissa de sprint: 2 semanas

### Perfis e disponibilidade
- 1 Backend Engineer (Node/API): 70% de foco
- 1 Platform Engineer (NATS/Eventing): 60% de foco
- 1 AI/ML Engineer (regras adaptativas): 50% de foco
- 1 QA Engineer: 60% de foco
- 1 SRE/Observability Engineer: 40% de foco (Sprint 3)

### Estimativa por subtask (esforco)
- #40: 3 dias uteis
- #41: 2 dias uteis
- #42: 2 dias uteis
- #43: 3 dias uteis
- #44: 2 dias uteis
- #45: 2 dias uteis
- #46: 2 dias uteis
- #47: 3 dias uteis
- #48: 2 dias uteis

Total estimado: 21 dias uteis de esforco tecnico distribuido por especialidade.

## Riscos principais
- Permissao insuficiente para GitHub Project reduz automacao visual da board.
- Integracao entre regras adaptativas e eventos pode gerar retrabalho se contratos mudarem tarde.
- Testes E2E de sync dependem de ambiente estavel de mensageria.

## Mitigacoes
- Usar labels sprint-1/sprint-2/sprint-3 + milestone existente para rastreio.
- Congelar contratos de evento no inicio da Sprint 1.
- Executar smoke de mensageria ao abrir e fechar cada sprint.

## Resultado esperado por sprint
- Sprint 1: feature base funcional em contratos, runtime e contratos de evento.
- Sprint 2: robustez com auditoria, idempotencia e cobertura de testes do runtime.
- Sprint 3: cobertura final e observabilidade pronta para operacao.
