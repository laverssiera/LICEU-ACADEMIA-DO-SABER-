#!/bin/bash
set -e
REPO="laverssiera/LICEU-ACADEMIA-DO-SABER-"

create_issue() {
  local title="$1"
  local label="$2"
  local body="$3"
  gh issue create --repo "$REPO" --title "$title" --label "$label" --body "$body"
  sleep 1
}

# ─── BLOCO 1 — FOUNDATION ────────────────────────────────────────────────────

create_issue \
"[ISSUE 1] Criar domínio educacional (core academy)" \
"bloco-1-foundation,priority-high" \
'## 🧱 Bloco 1 — Foundation | Core Educacional

### Objetivo
Criar o domínio central da Academia do Saber como base única de conhecimento do ecossistema LICEU.

### Entidades necessárias
- `users` — sincronizado com o core do ecossistema
- `courses` — cursos educacionais por domínio
- `modules` — módulos por curso
- `lessons` — lições por módulo (video, text, simulation, quiz)
- `tracks` — trilhas por monólito
- `enrollments` — matrículas de usuários
- `progress` — progresso por lição/curso
- `certifications` — certificações emitidas

### Critérios de aceite
- [ ] Domínio educacional definido e documentado
- [ ] Entidades com relacionamentos corretos (FK, índices)
- [ ] Base única consumida por todos os monólitos
- [ ] UUIDs e timestamps em todas as tabelas
- [ ] Endpoints CRUD básicos disponíveis

### Endpoints esperados
```
GET  /academy/courses
POST /academy/courses
POST /academy/enroll
POST /academy/lesson/complete
GET  /academy/courses/:id/progress
```

### Dependências
Nenhuma — issue base do projeto.

### Referência de implementação
`src/data.js`, `schema.sql`, `api/main.py`'

create_issue \
"[ISSUE 2] Criar schema SQL enterprise" \
"bloco-1-foundation,priority-high" \
'## 🧱 Bloco 1 — Foundation | Schema SQL

### Objetivo
Definir e criar o schema PostgreSQL enterprise da Academia do Saber.

### Tabelas necessárias

| Tabela | Descrição |
|--------|-----------|
| `academy_users` | Usuários espelhados do core |
| `courses` | Cursos e metadados |
| `modules` | Módulos por curso |
| `lessons` | Lições por módulo |
| `enrollments` | Matrículas com status e progresso |
| `lesson_progress` | Progresso por lição com score |
| `certifications` | Certificações emitidas |
| `cognitive_profiles` | Perfil cognitivo com skill_matrix (JSONB) |
| `academy_events` | Log de eventos para auditoria e NATS |

### Requisitos técnicos
- [ ] UUID padrão (`gen_random_uuid()`) em todos os IDs
- [ ] Timestamps `created_at` e `updated_at` com trigger auto
- [ ] Índices em `user_id`, `course_id`, `monolith`, `event_type`
- [ ] Tipos ENUM para `course_level`, `lesson_type`, `enrollment_status`, `cert_source`
- [ ] Foreignkeys com `ON DELETE CASCADE` onde apropriado
- [ ] JSONB para `skill_matrix`, `payload`, `custom_branding`

### Seed inicial
- Trilhas CORE LICEU inseridas na migração
- Cursos de compliance obrigatórios

### Dependências
- ISSUE 1

### Referência de implementação
`schema.sql`'

create_issue \
"[ISSUE 3] Criar estrutura de trilhas (tracks) por monólito" \
"bloco-1-foundation,priority-high" \
'## 🧱 Bloco 1 — Foundation | Trilhas por Monólito

### Objetivo
Criar as trilhas educacionais específicas para cada monólito do ecossistema.

### Trilhas a criar

| Trilha | Monólito | Obrigatória |
|--------|----------|-------------|
| Archimedes Track | archimedes (Imob Tech) | Não |
| Game MKT Track | gameMkt (Marketing) | Não |
| Jurídico Track | juridico (JuridicoTech) | Não |
| Finance Track | cea (CEA / Hub) | Não |
| OPERA Track | opera (OPERA) | Não |
| CEFEIDA Data Track | cefeida | Não |
| John Copilot Track | john | Não |

### Cada trilha deve ter
- [ ] Nome único
- [ ] Monólito de origem
- [ ] Lista de módulos ordenados
- [ ] Flag `is_mandatory` vinculada ao RBAC
- [ ] Lista de `skill_tags`
- [ ] Integração com `track_courses` (FK)

### Endpoints esperados
```
GET /academy/tracks
GET /academy/tracks/:monolith
```

### Dependências
- ISSUE 1, ISSUE 2

### Referência de implementação
`src/data.js` → `monolithTracks`, `api/main.py` → `/academy/tracks`'

create_issue \
"[ISSUE 4] Criar trilha CORE LICEU obrigatória (transversal)" \
"bloco-1-foundation,priority-high" \
'## 🧱 Bloco 1 — Foundation | Core LICEU Training

### Objetivo
Criar a trilha transversal obrigatória que todo usuário do ecossistema deve concluir antes de operar.

### Módulos obrigatórios

| # | Módulo | Duração |
|---|--------|---------|
| 1 | Cultura LICEU | 2h |
| 2 | Uso do Kanban Global | 1h30 |
| 3 | Uso do John | 2h |
| 4 | Compliance Jurídico Básico | 2h |
| 5 | Governança do Ecossistema | 1h |

**Carga total:** 8h30

### Regra de negócio
> ⚠️ Nenhum usuário pode operar no ecossistema sem concluir esta trilha.

- [ ] Middleware de bloqueio: `requireCoreTraining()`
- [ ] Flag `is_core_liceu = true` no banco
- [ ] Evento `academy.enrolled` emitido no onboarding
- [ ] Status verificado no RBAC antes de liberar endpoints críticos

### Endpoint
```
GET /academy/training/core-liceu
```

### Dependências
- ISSUE 2, ISSUE 3, ISSUE 11

### Referência de implementação
`src/data.js` → `coreLiceuTraining`, `api/main.py` → `/academy/training/core-liceu`'

echo "✅ Issues Bloco 1 criadas"

# ─── BLOCO 2 — JOHN TRAINING ENGINE ─────────────────────────────────────────

create_issue \
"[ISSUE 5] Integrar John ao aprendizado (John Training Engine)" \
"bloco-2-john,priority-high" \
'## 🤖 Bloco 2 — John Training Engine

### Objetivo
Integrar o John Brasileiro (IA pedagógico) ao motor de aprendizado da Academia.

### Funcionalidades
- Analisar performance atual do usuário
- Sugerir cursos e trilhas baseados em `skill_matrix`
- Ajustar dificuldade automaticamente
- Priorizar conteúdo por gap identificado
- Emitir `academy.john_recommended` via NATS

### Endpoint
```
POST /academy/john/train
Body: { user_id, current_scores: {}, completed_courses: [] }
```

### Lógica de ajuste de dificuldade
| Cursos concluídos | Dificuldade recomendada |
|-------------------|------------------------|
| < 3 | basico |
| 3–7 | intermediario |
| 8+ | avancado |

### Critérios de aceite
- [ ] Endpoint funcional com validação de input
- [ ] Áreas fracas identificadas (score < 60)
- [ ] Sugestões geradas automaticamente
- [ ] Evento NATS publicado após análise
- [ ] Resposta inclui `next_step` acionável

### Integração NATS
```
Publica: academy.john_recommended
Consome: john.learn (após lesson.complete)
```

### Dependências
- ISSUE 1, ISSUE 6

### Referência de implementação
`src/app.js` → `/academy/john/train`, `api/main.py`'

create_issue \
"[ISSUE 6] Criar cognitive_profile — score cognitivo do usuário" \
"bloco-2-john,priority-medium" \
'## 🤖 Bloco 2 — John Training Engine | Cognitive Profile

### Objetivo
Criar e manter o perfil cognitivo de cada usuário para personalização do aprendizado.

### Tabela: `cognitive_profiles`

```sql
CREATE TABLE cognitive_profiles (
    user_id             UUID PRIMARY KEY,
    cognitive_score     FLOAT DEFAULT 0,
    skill_matrix        JSONB NOT NULL DEFAULT '"'"'{}'"'"',
    specialization_level TEXT DEFAULT '"'"'junior'"'"',
    weak_areas          TEXT[] DEFAULT '"'"'{}'"'"',
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Campos do `skill_matrix`
Exemplo:
```json
{
  "bim": 80,
  "juridico": 45,
  "financeiro": 70,
  "vendas": 90,
  "compliance": 60
}
```

### `cognitive_score`
Calculado como média ponderada do `skill_matrix`.

### `specialization_level`
- `junior` → média < 50
- `pleno` → média 50–75
- `senior` → média > 75

### Endpoints
```
GET  /academy/users/:userId/cognitive-score
POST /academy/users/:userId/cognitive-score
```

### Critérios de aceite
- [ ] Upsert funcional (cria ou atualiza)
- [ ] `cognitive_score` calculado automaticamente
- [ ] `weak_areas` inferidas (score < 60)
- [ ] Integração com John Train (ISSUE 5)

### Dependências
- ISSUE 2, ISSUE 5

### Referência de implementação
`src/app.js` → `/academy/users/:userId/cognitive-score`'

create_issue \
"[ISSUE 7] Aprendizado baseado em erro (loss intelligence)" \
"bloco-2-john,priority-medium" \
'## 🤖 Bloco 2 — John Training Engine | Error-Based Learning

### Objetivo
Gerar aulas automáticas a partir de erros reais registrados nos sistemas do ecossistema.

### Fontes de erro integradas
- `deals` — perdas em negociações (Archimedes)
- `audit` — inconsistências auditadas
- `loss_intelligence` — padrões de perda identificados pela IA

### Endpoint
```
POST /academy/john/learn-from-error
Body: { user_id, error_type, source_system, error_description }
```

### Mapeamento error_type → domínio educacional
| error_type | Domínio |
|------------|---------|
| deal | vendas |
| contract | juridico |
| financial | financeiro |
| audit | compliance |
| loss | operacoes |

### Lição gerada automaticamente inclui
- Título descritivo do erro
- Conteúdo contextualizado
- 3 exercícios práticos
- Duração estimada: 45min

### Evento NATS
```
Publica: academy.john_recommended (trigger: "error")
```

### Critérios de aceite
- [ ] Lição gerada automaticamente a partir do erro
- [ ] Mapeamento correto para domínio educacional
- [ ] Evento NATS publicado
- [ ] Registro persistido em `error_lessons`

### Dependências
- ISSUE 5, ISSUE 6

### Referência de implementação
`src/app.js` → `/academy/john/learn-from-error`'

echo "✅ Issues Bloco 2 criadas"

# ─── BLOCO 3 — TREINAMENTO OPERACIONAL ───────────────────────────────────────

create_issue \
"[ISSUE 8] Criar Simulation Engine (treino real em sandbox)" \
"bloco-3-simulacao,priority-high" \
'## 🎯 Bloco 3 — Treinamento Operacional | Simulation Engine

### Objetivo
Criar simulações de operações reais em ambiente sandbox para treinamento prático.

### Simulações disponíveis

| Tipo | Monólito | Descrição |
|------|----------|-----------|
| `venda` | archimedes | Fluxo completo de venda imobiliária |
| `negociacao` | sales_os | Negociação avançada com cliente |
| `contrato` | juridico | Assinatura e análise contratual |
| `financeiro` | cea | Análise de crédito e aprovação |

### Endpoints
```
POST /academy/sandbox/simulate
POST /academy/simulate/deal   ← cenário específico de deal
```

### Resposta de simulação inclui
- `score` (0–100)
- `outcome` (aprovado / em_reforco)
- `feedback` personalizado
- `monolith` de origem

### Critérios de aceite
- [ ] 4 tipos de simulação implementados
- [ ] Score gerado com lógica realista
- [ ] Feedback contextualizado por resultado
- [ ] Registro persistido em `sandbox_simulations`
- [ ] Integração com ranking (ISSUE 27)

### Dependências
- ISSUE 1, ISSUE 5

### Referência de implementação
`src/app.js` → `/academy/sandbox/simulate`, `api/main.py`'

create_issue \
"[ISSUE 9] Replay de operações reais" \
"bloco-3-simulacao,priority-medium" \
'## 🎯 Bloco 3 — Treinamento Operacional | Replay

### Objetivo
Permitir replay de operações reais como ferramenta pedagógica para aprendizado contextual.

### Tipos de replay

- **Replay de deals** — negociações do Archimedes
- **Replay de decisões do John** — raciocínio da IA em situações reais
- **Replay de erros** — operações com resultado abaixo do esperado

### Fonte de dados
- `events` (NATS audit log)
- `academy_events`
- Logs de audit

### Endpoints
```
POST /academy/replay
GET  /academy/replay?userId=:id
```

### Payload de replay
```json
{
  "user_id": "USR-001",
  "replay_type": "deal",
  "reference_id": "DEAL-999",
  "source_system": "Archimedes"
}
```

### Insights gerados automaticamente por replay
- Ponto crítico identificado
- Oportunidade de melhoria
- Recomendação de trilha

### Evento NATS
```
Publica: academy.replay.created
```

### Critérios de aceite
- [ ] Criação e listagem de replays por usuário
- [ ] Insights gerados automaticamente
- [ ] Evento NATS publicado
- [ ] Filtro por tipo de replay

### Dependências
- ISSUE 7, ISSUE 22

### Referência de implementação
`src/app.js` → `/academy/replay`'

create_issue \
"[ISSUE 10] Certificação automática por performance" \
"bloco-3-simulacao,priority-high" \
'## 🎯 Bloco 3 — Treinamento Operacional | Certificação Automática

### Objetivo
Emitir certificações automaticamente com base em critérios de performance real.

### Critérios de certificação (OR logic)
1. **KPI Score ≥ 75** — aprovado por indicador de performance
2. **Aprovado pelo John** — IA valida capacidade operacional
3. **Execução aprovada** — validação por operação real em produção

### Endpoint
```
POST /academy/certification/auto-certify
Body: { user_id, track_id, kpi_score, approved_by_john, execution_approved }
```

### Resposta inclui
- `status`: certificado | reprovado
- `issued_at`: timestamp (null se reprovado)
- `reason`: motivo da aprovação ou reprovação

### Eventos NATS
```
Aprovado  → academy.certified
Reprovado → academy.failed
```

### Critérios de aceite
- [ ] Lógica OR entre os 3 critérios
- [ ] Evento correto emitido em cada caso
- [ ] Histórico de tentativas persistido
- [ ] Integração com CORE_DNA (ISSUE 30) após certificação

### Dependências
- ISSUE 5, ISSUE 6, ISSUE 22

### Referência de implementação
`src/app.js` → `/academy/certification/auto-certify`'

echo "✅ Issues Bloco 3 criadas"

# ─── BLOCO 4 — HUBBACKOFFICE (RH + DP) ───────────────────────────────────────

create_issue \
"[ISSUE 11] Onboarding automático via HubBackoffice (RH + DP)" \
"bloco-4-rh,priority-high" \
'## 🧾 Bloco 4 — HubBackoffice | Onboarding Automático

### Objetivo
Automatizar a atribuição de trilhas obrigatórias quando um novo usuário é criado no ecossistema.

### Fluxo
```
Usuário criado no core
    ↓
Evento: hub.rh.training_required
    ↓
Academia recebe e cria onboarding
    ↓
Trilhas obrigatórias atribuídas por role + contract_type
    ↓
Evento: academy.enrolled publicado
    ↓
Usuário recebe notificação de treinamento
```

### Endpoints
```
POST /academy/onboarding
GET  /academy/onboarding/:userId
```

### Body
```json
{
  "user_id": "USR-001",
  "name": "João Silva",
  "role": "corretor",
  "contract_type": "clt"
}
```

### Resposta inclui
- `mandatory_tracks` — lista completa (role + contract_type)
- `training_status` — pending | in_progress | completed
- `started_at`

### Critérios de aceite
- [ ] Onboarding criado automaticamente ao receber evento NATS
- [ ] Trilhas corretamente combinadas (role + contrato)
- [ ] Evento `academy.enrolled` publicado
- [ ] Endpoint de consulta de status por usuário

### Dependências
- ISSUE 3, ISSUE 4, ISSUE 22

### Referência de implementação
`src/app.js` → `/academy/hr/onboarding`, `api/main.py` → `/academy/onboarding`'

create_issue \
"[ISSUE 12] Treinamento obrigatório por função (role-based training)" \
"bloco-4-rh,priority-high" \
'## 🧾 Bloco 4 — HubBackoffice | Role-Based Training

### Objetivo
Definir e aplicar trilhas obrigatórias de acordo com a função do colaborador.

### Mapeamento de funções

| Função | Trilhas Obrigatórias |
|--------|---------------------|
| corretor | vendas, juridico_basico, crm, cultura_liceu |
| financeiro | cea, compliance, cultura_liceu, uso_john |
| gestor | governanca, lideranca, cultura_liceu, kanban_global, uso_john |
| tecnico | opera, bim_basico, cultura_liceu |
| analista_dados | cefeida_data, python_basico, cultura_liceu, uso_john |
| juridico | lgpd, contratos, nao_circunvencao, compliance, cultura_liceu |

### Endpoint
```
GET /academy/hr/mandatory-tracks/:role
```

### Resposta
```json
{
  "role": "corretor",
  "mandatory_tracks": ["vendas", "juridico_basico", "crm", "cultura_liceu"]
}
```

### Critérios de aceite
- [ ] Todos os papéis mapeados
- [ ] Endpoint retorna 404 para papel desconhecido com lista de disponíveis
- [ ] Integração com onboarding (ISSUE 11)
- [ ] Mapeamento extensível via configuração

### Dependências
- ISSUE 11

### Referência de implementação
`src/app.js` → `/academy/hr/mandatory-tracks/:role`'

create_issue \
"[ISSUE 13] Suporte a CLT + PJ — trilhas por tipo de contrato" \
"bloco-4-rh,priority-medium" \
'## 🧾 Bloco 4 — HubBackoffice | CLT + PJ

### Objetivo
Diferenciar trilhas obrigatórias conforme o tipo de vínculo do colaborador.

### Trilhas por tipo de contrato

**CLT:**
- cultura_liceu
- compliance_trabalhista
- uso_john
- kanban_global
- governanca_ecossistema

**PJ:**
- nao_circunvencao
- lgpd
- contratos_pj
- compliance_fiscal
- cultura_liceu

### Endpoint
```
GET /academy/hr/contract-tracks/:contractType
```
Aceita: `clt` ou `pj`

### Lógica de combinação (ISSUE 11)
```
trilhas_finais = unique(trilhas_por_role + trilhas_por_contrato)
```

### Critérios de aceite
- [ ] Endpoint funcional para `clt` e `pj`
- [ ] Retorno 404 para tipo inválido
- [ ] Integrado com onboarding automático
- [ ] Compliance fiscal/jurídico incluído para PJ

### Dependências
- ISSUE 11, ISSUE 12

### Referência de implementação
`src/app.js` → `/academy/hr/contract-tracks/:contractType`'

echo "✅ Issues Bloco 4 criadas"

# ─── BLOCO 5 — JURIDICOTECH ───────────────────────────────────────────────────

create_issue \
"[ISSUE 14] Compliance educacional obrigatório (JuridicoTech)" \
"bloco-5-juridico,priority-high" \
'## ⚖️ Bloco 5 — JuridicoTech | Compliance Obrigatório

### Objetivo
Garantir que todos os usuários completem os treinamentos jurídicos obrigatórios antes de operar.

### Cursos de compliance obrigatórios

| # | Curso | Duração | Domínio |
|---|-------|---------|---------|
| 1 | LGPD — Lei Geral de Proteção de Dados | 4h | juridico |
| 2 | Cláusula de Não-Circunvenção | 2h | juridico |
| 3 | Contratos: fundamentos e boas práticas | 3h | juridico |
| 4 | Compliance Corporativo | 3h | compliance |
| 5 | Ética e Conduta no Ecossistema | 1h30 | compliance |

### Regra de negócio
> ⚠️ Usuário que não concluiu os cursos obrigatórios **não pode operar** em endpoints críticos.

### Endpoint
```
GET  /academy/legal/compliance-courses   ← lista cursos obrigatórios
POST /academy/legal/sign-acceptance      ← registra aceite com assinatura
POST /academy/compliance/check           ← verifica status de compliance
```

### Aceite jurídico
```json
{
  "user_id": "USR-001",
  "course_id": 1,
  "signature": "ACEITE-USR-001-1-1714300000"
}
```

### Evento NATS
```
Publica: academy.compliance.accepted
Publica: juridico.validate_training
```

### Critérios de aceite
- [ ] Lista de cursos obrigatórios com flag `mandatory: true`
- [ ] Aceite com assinatura única gerada
- [ ] Verificação de compliance retorna `is_compliant` e cursos pendentes
- [ ] Impossível re-aceitar o mesmo curso

### Dependências
- ISSUE 2, ISSUE 15

### Referência de implementação
`src/app.js` → `/academy/legal/*`'

create_issue \
"[ISSUE 15] Integração de validação jurídica — evento juridico.validate_training" \
"bloco-5-juridico,priority-high" \
'## ⚖️ Bloco 5 — JuridicoTech | Validação via Evento

### Objetivo
Integrar a Academia com o JuridicoTech via NATS para validação de treinamento obrigatório.

### Fluxo de validação
```
Usuário tenta operar endpoint crítico
    ↓
Academia verifica compliance (ISSUE 14)
    ↓
Publica: juridico.validate_training
    ↓
JuridicoTech consome e valida
    ↓
Se pendente → bloqueia operação
```

### Evento publicado
```json
// Subject: juridico.validate_training
{
  "user": "USR-001",
  "timestamp": "2026-04-28T...",
  "context": "academy_compliance_check"
}
```

### Middleware de proteção
```python
@app.middleware("http")
async def require_compliance(request, call_next):
    # verifica se usuário concluiu compliance antes de operar
```

### Critérios de aceite
- [ ] Evento `juridico.validate_training` publicado em toda ação de aceite
- [ ] JetStream stream `JURIDICO` configurado (ISSUE 21)
- [ ] Middleware opcional disponível para endpoints críticos
- [ ] Log de validação em `academy_events`

### Dependências
- ISSUE 14, ISSUE 21

### Referência de implementação
`api/main.py` → `publish("juridico.validate_training", ...)`'

echo "✅ Issues Bloco 5 criadas"

# ─── BLOCO 6 — METRICS ────────────────────────────────────────────────────────

create_issue \
"[ISSUE 16] Dashboard educacional — KPIs e métricas" \
"bloco-6-metrics,priority-medium" \
'## 📊 Bloco 6 — Metrics | Dashboard Educacional

### Objetivo
Consolidar KPIs educacionais para visibilidade da performance do ecossistema.

### KPIs principais

| KPI | Descrição |
|-----|-----------|
| `completion_rate` | % de matrículas concluídas |
| `avg_score` | Média de pontuação nas lições/sandboxes |
| `total_enrollments` | Total de matrículas |
| `total_certifications` | Certificações emitidas |
| `total_courses` | Cursos disponíveis |
| `total_sandbox` | Simulações executadas |

### Endpoints
```
GET /academy/metrics
GET /academy/metrics/dashboard
GET /academy/metrics/correlation
```

### Dashboard institucional inclui também
- Progresso por trilha (track_completion)
- Top 10 do ranking
- Alertas de atraso (onboardings sem progresso)
- Últimos 10 eventos NATS

```
GET /academy/dashboard/institutional
```

### Critérios de aceite
- [ ] Todos KPIs retornando valores corretos
- [ ] Progresso por trilha calculado corretamente
- [ ] Alertas de atraso identificados
- [ ] `updatedAt` presente na resposta

### Dependências
- ISSUE 1, ISSUE 10, ISSUE 11

### Referência de implementação
`src/app.js` → `/academy/metrics/*`, `api/main.py`'

create_issue \
"[ISSUE 17] Correlação treinamento x performance real" \
"bloco-6-metrics,priority-medium" \
'## 📊 Bloco 6 — Metrics | Correlação Educação × Resultado

### Objetivo
Provar o impacto do treinamento nos resultados reais do ecossistema.

### Cruzamentos a realizar

| Variável de Treinamento | Variável de Resultado |
|------------------------|-----------------------|
| Conclusão de trilha de vendas | Taxa de conversão (Archimedes) |
| Score em compliance jurídico | Número de contratos com problema |
| Performance em sandbox | KPI real de operações |
| Score cognitivo médio | Ranking de performance |

### Endpoint
```
GET /academy/metrics/correlation
```

### Resposta inclui por usuário certificado
- `average_sandbox_score`
- `kpi_score` real
- `insight` — correlação identificada

### Insights gerados
- Score médio ≥ 80: "Alta correlação: treinamento intenso impacta resultado real"
- Score médio < 80: "Potencial de melhora com trilhas avançadas"

### Critérios de aceite
- [ ] Endpoint funcional linkando certificações com sandbox scores
- [ ] Insights textuais gerados por usuário
- [ ] `analyzed_at` timestamp na resposta
- [ ] Base para relatório executivo

### Dependências
- ISSUE 10, ISSUE 16

### Referência de implementação
`src/app.js` → `/academy/metrics/correlation`'

echo "✅ Issues Bloco 6 criadas"

# ─── BLOCO 7 — EDTECH EXTERNO ─────────────────────────────────────────────────

create_issue \
"[ISSUE 18] Academia como produto SaaS (camada externa EdTech)" \
"bloco-7-edtech,priority-medium" \
'## 🌐 Bloco 7 — EdTech | Academia como SaaS

### Objetivo
Expor a Academia do Saber como produto EdTech para o mercado externo.

### Funcionalidades
- Cursos pagos disponíveis ao público
- Trilhas abertas com certificação de mercado
- Catálogo público sem autenticação
- Integração com gateway de pagamento (futuro)

### Endpoints
```
GET  /academy/saas/courses   ← catálogo público
POST /academy/saas/courses   ← admin cria oferta
```

### Campos de oferta SaaS
```json
{
  "title": "BIM para Iniciantes",
  "domain": "BIM",
  "price": 299.90,
  "level": "basico",
  "target_audience": "mercado",
  "certification_included": true
}
```

### Critérios de aceite
- [ ] Catálogo público listável
- [ ] Criação de oferta com preço e certificação
- [ ] `type: "saas_externo"` diferencia de cursos internos
- [ ] Base para futura integração de pagamento

### Dependências
- ISSUE 1

### Referência de implementação
`src/app.js` → `/academy/saas/*`'

create_issue \
"[ISSUE 19] Marketplace de cursos — especialistas e monólitos" \
"bloco-7-edtech,priority-medium" \
'## 🌐 Bloco 7 — EdTech | Marketplace de Cursos

### Objetivo
Criar um marketplace onde especialistas externos e monólitos internos podem publicar cursos.

### Tipos de publicadores
- **Especialistas** — profissionais externos certificados
- **Monólitos** — equipes internas do ecossistema LICEU

### Endpoints
```
GET  /academy/marketplace/courses    ← lista público
POST /academy/marketplace/courses    ← publicar curso
```

### Campos
```json
{
  "title": "Energia Solar Residencial",
  "domain": "Energia",
  "author_id": "ESP-001",
  "author_type": "especialista",
  "price": 199,
  "skill_tags": ["energia", "solar", "instalacao"]
}
```

### Status de moderação
- `pending_review` → aguardando aprovação
- `active` → publicado
- `rejected` → reprovado

### Critérios de aceite
- [ ] Publicação com status `pending_review` por padrão
- [ ] Listagem pública de cursos ativos
- [ ] `author_type` diferencia especialista de monólito
- [ ] Integração com `courses` internos (ISSUE 1)

### Dependências
- ISSUE 1, ISSUE 18

### Referência de implementação
`src/app.js` → `/academy/marketplace/*`'

create_issue \
"[ISSUE 20] White-label corporativo" \
"bloco-7-edtech,priority-medium" \
'## 🌐 Bloco 7 — EdTech | White-label Corporativo

### Objetivo
Permitir que empresas parceiras usem a Academia do Saber com identidade própria.

### Casos de uso
- Construtoras usando a plataforma para treinar equipes
- Incorporadoras com trilhas customizadas
- Parceiros do ecossistema com certificação própria

### Endpoint
```
POST /academy/whitelabel/setup
```

### Body
```json
{
  "company_id": "CORP-001",
  "company_name": "Construtora Alpha",
  "tracks": ["bim_basico", "opera"],
  "custom_branding": {
    "primary_color": "#003366",
    "logo_url": "https://..."
  }
}
```

### Regras
- Um white-label por `company_id` (409 se já existe)
- Trilhas selecionadas são subconjunto dos disponíveis
- Branding customizado em JSONB

### Critérios de aceite
- [ ] Setup funcional com `status: "active"`
- [ ] Conflito 409 para empresa duplicada
- [ ] `custom_branding` persistido em JSONB
- [ ] Base para tenant isolation futura

### Dependências
- ISSUE 1, ISSUE 18

### Referência de implementação
`src/app.js` → `/academy/whitelabel/setup`'

echo "✅ Issues Bloco 7 criadas"

# ─── BLOCO 8 — NATS ───────────────────────────────────────────────────────────

create_issue \
"[ISSUE 21] Criar stream ACADEMY no NATS JetStream" \
"bloco-8-nats,priority-high" \
'## 📡 Bloco 8 — NATS | Stream ACADEMY

### Objetivo
Criar e configurar o JetStream stream ACADEMY para eventos educacionais.

### Comando de criação
```bash
nats stream add ACADEMY \
  --subjects "academy.*,academy.lesson.*,academy.course.*" \
  --storage file \
  --retention limits \
  --max-msgs=-1 \
  --max-age=72h \
  --replicas=1
```

### Streams necessários

| Stream | Subjects | Retenção |
|--------|----------|----------|
| ACADEMY | `academy.*` | 72h |
| JOHN | `john.*` | 24h |
| CORE_DNA | `core_dna.*` | 168h |
| HUB | `hub.*` | 48h |
| JURIDICO | `juridico.*` | 168h |
| KANBAN | `kanban.*` | 24h |

### Consumers a criar
- `academy-enrolled-consumer` — filtra `academy.enrolled`
- `academy-certified-consumer` — filtra `academy.certified`

### Configuração
Arquivo: `nats/nats.conf`
Script: `nats/init-streams.sh`

### Critérios de aceite
- [ ] Stream ACADEMY criado com subjects corretos
- [ ] Todos os 6 streams operacionais
- [ ] Consumers com `ack explicit` configurados
- [ ] Script de inicialização disponível e documentado
- [ ] NATS monitoring acessível em :8222

### Dependências
Nenhuma — infra base.

### Referência de implementação
`nats/nats.conf`, `nats/init-streams.sh`, `docker-compose.yml`'

create_issue \
"[ISSUE 22] Definir e documentar eventos padrão da Academia" \
"bloco-8-nats,priority-high" \
'## 📡 Bloco 8 — NATS | Eventos Padrão

### Objetivo
Padronizar todos os eventos publicados pela Academia do Saber no NATS JetStream.

### Catálogo de eventos

| Evento | Trigger | Payload |
|--------|---------|---------|
| `academy.enrolled` | Matrícula criada | `{ user_id, course_id, tracks }` |
| `academy.lesson.completed` | Lição concluída | `{ user_id, lesson_id, score }` |
| `academy.course.completed` | Curso concluído | `{ user_id, course_id, score }` |
| `academy.certified` | Certificação emitida | `{ user_id, track_id, cert_id }` |
| `academy.failed` | Reprovação | `{ user_id, track_id }` |
| `academy.john_recommended` | John fez recomendação | `{ user_id, plan, trigger }` |
| `academy.compliance.accepted` | Aceite jurídico | `{ user_id, course_id }` |
| `academy.onboarding.started` | Onboarding iniciado | `{ user_id, tracks }` |
| `academy.sandbox.executed` | Simulação executada | `{ user_id, type, score }` |
| `academy.replay.created` | Replay criado | `{ user_id, reference_id }` |
| `academy.task.learning_generated` | Task gerou treinamento | `{ user_id, task_id, domain }` |

### Padrão de payload
```json
{
  "type": "academy.enrolled",
  "payload": { "user_id": "USR-001", ... },
  "emitted_at": "2026-04-28T12:00:00Z"
}
```

### Critérios de aceite
- [ ] Todos os eventos documentados nesta issue
- [ ] Cada evento persistido em `academy_events` antes de publicar
- [ ] Retry automático em caso de falha no NATS
- [ ] Wrapper `publish()` centralizado em `api/main.py`

### Dependências
- ISSUE 21

### Referência de implementação
`api/main.py` → função `publish()`, `src/data.js` → `emitAcademyEvent()`'

create_issue \
"[ISSUE 23] Integrar eventos Academy com ecossistema" \
"bloco-8-nats,priority-medium" \
'## 📡 Bloco 8 — NATS | Integração com Ecossistema

### Objetivo
Garantir que os eventos da Academia impactem os demais monólitos do ecossistema.

### Impactos por monólito

| Evento Academy | Monólito Impactado | Ação |
|---------------|-------------------|------|
| `academy.certified` | Archimedes | Desbloqueia acesso a módulos de venda |
| `academy.certified` | OPERA | Habilita execução de tarefas avançadas |
| `academy.certified` | Hub | Atualiza perfil de competências do colaborador |
| `academy.certified` | John | Atualiza decisões baseadas no nível do usuário |
| `academy.enrolled` | Hub RH | Registra início de onboarding |
| `academy.compliance.accepted` | JuridicoTech | Libera operação de contratos |
| `academy.john_recommended` | John | Atualiza contexto de aprendizado |

### Consumidores NATS a implementar

```python
# Exemplo: consumer no Archimedes
# Consome academy.certified
# → desbloqueia operações de venda para usuário certificado
```

### Endpoint de consulta de eventos
```
GET /academy/events?type=academy.certified
```

### Critérios de aceite
- [ ] Endpoint de eventos filtráveis por tipo
- [ ] Documentação de cada integração
- [ ] Consumers configurados nos streams (ISSUE 21)
- [ ] Guia de adição de novos consumers

### Dependências
- ISSUE 21, ISSUE 22

### Referência de implementação
`src/app.js` → `/academy/events`, `docker-compose.yml` → `nats-init`'

echo "✅ Issues Bloco 8 criadas"

# ─── BLOCO 9 — CEFEIDA ────────────────────────────────────────────────────────

create_issue \
"[ISSUE 24] IA de aprendizado — análise comportamental (CEFEIDA)" \
"bloco-9-cefeida,priority-medium" \
'## 🧠 Bloco 9 — CEFEIDA | IA de Aprendizado

### Objetivo
Usar a CEFEIDA (motor de dados e IA do ecossistema) para analisar o comportamento de aprendizado e recomendar caminhos adaptativos.

### O que a CEFEIDA analisa
- **Comportamento de estudo** — horários, velocidade, sessões
- **Performance histórica** — scores por lição ao longo do tempo
- **Padrões de erro** — áreas com falha recorrente

### Endpoint
```
POST /academy/cefeida/analyze
Body: {
  user_id,
  study_behavior: {},
  performance_history: [70, 55, 80, 60],
  error_patterns: ["juridico", "financeiro"]
}
```

### Saída da análise
- `average_performance` — média calculada
- `top_error_patterns` — top 3 áreas de erro
- `recommendations` — ações sugeridas
- `adaptive_path` — basico | intermediario | avancado

### Critérios de aceite
- [ ] Média de performance calculada corretamente
- [ ] Recomendações baseadas nos padrões de erro
- [ ] `adaptive_path` inferido da média
- [ ] Registro persistido em `cefeida_analyses`

### Dependências
- ISSUE 6, ISSUE 5

### Referência de implementação
`src/app.js` → `/academy/cefeida/analyze`'

create_issue \
"[ISSUE 25] Geração de conteúdo dinâmico e adaptativo (CEFEIDA)" \
"bloco-9-cefeida,priority-medium" \
'## 🧠 Bloco 9 — CEFEIDA | Conteúdo Dinâmico

### Objetivo
Gerar automaticamente aulas, trilhas e microlearning adaptados ao perfil do usuário.

### Formatos de conteúdo

| Formato | Duração | Uso |
|---------|---------|-----|
| `microlearning` | 15min | Reforço pontual |
| `trilha_adaptativa` | 2h | Aprendizado profundo |
| `simulacao` | 45min | Prática contextualizada |

### Endpoint
```
POST /academy/cefeida/generate-content
Body: { user_id, domain, format, target_level }
```

### Conteúdo gerado inclui
- Título descritivo
- Resumo contextualizado ao ecossistema LICEU
- 5 passos de aprendizado
- Duração estimada
- Recomendação de próxima etapa

### Exemplo de resposta
```json
{
  "generated_content": {
    "title": "Micro-aula: BIM",
    "steps": ["Introdução rápida ao tema", "Exercício prático", "Quiz (5 questões)", "Caso real LICEU", "Próxima etapa"],
    "estimated_duration": "15min"
  }
}
```

### Critérios de aceite
- [ ] 3 formatos suportados
- [ ] Conteúdo contextualizado ao domínio solicitado
- [ ] Integração com `adaptive_path` da análise (ISSUE 24)
- [ ] Registro persistido em `dynamic_contents`

### Dependências
- ISSUE 24

### Referência de implementação
`src/app.js` → `/academy/cefeida/generate-content`'

echo "✅ Issues Bloco 9 criadas"

# ─── BLOCO 10 — TRADING DESK ─────────────────────────────────────────────────

create_issue \
"[ISSUE 26] Tela institucional — Trading Desk educacional" \
"bloco-10-ui,priority-medium" \
'## 🖥️ Bloco 10 — Trading Desk | Tela Institucional

### Objetivo
Criar a interface visual institucional da Academia do Saber no modelo Trading Desk.

### Stack
- React 18 + Vite
- Tailwind CSS (dark theme, bg-black)
- Proxy para API FastAPI em :8010

### Blocos da interface

| Bloco | Descrição |
|-------|-----------|
| Cursos | Lista com barra de progresso por curso |
| Trilhas | Trilhas por monólito com badges |
| Ranking | Top 10 por XP + nível |
| Compliance | Cursos jurídicos obrigatórios |
| Eventos | Log de eventos NATS em tempo real |
| Métricas | KPIs e conclusão por trilha |
| John Widget | Input para análise de performance + resultado |
| Alertas | Onboardings sem progresso (late_alerts) |

### Painel lateral direito
- John Recomenda (recomendações recentes)
- Widget de treinamento rápido com John
- Alertas de atraso
- Eventos recentes

### Atualização automática
- Polling a cada 30 segundos via `setInterval`

### Endpoints consumidos
- `GET /academy/dashboard`
- `GET /academy/tracks`
- `GET /academy/ranking/gamified`
- `GET /academy/events`
- `GET /academy/metrics/dashboard`
- `GET /academy/legal/compliance-courses`
- `GET /academy/dashboard/institutional`

### Critérios de aceite
- [ ] Interface dark theme responsiva
- [ ] 6 painéis navegáveis via sidebar com ícones
- [ ] Widget John funcional com chamada real à API
- [ ] Alertas exibindo onboardings atrasados
- [ ] Build Docker disponível

### Dependências
- ISSUE 16, ISSUE 25, ISSUE 27

### Referência de implementação
`frontend/src/AcademyDesk.jsx`'

create_issue \
"[ISSUE 27] Ranking gamificado — XP, nível e performance" \
"bloco-10-ui,priority-medium" \
'## 🖥️ Bloco 10 — Trading Desk | Ranking Gamificado

### Objetivo
Criar sistema de gamificação com XP, níveis e performance real para engajamento dos usuários.

### Sistema de XP

| Origem | XP |
|--------|----|
| Score de sandbox (1 ponto = 1 XP) | variável |
| Certificação emitida | +200 XP |
| Conclusão de lição | +10 XP (futuro) |

### Níveis

| Nível | XP necessário |
|-------|--------------|
| Aprendiz | 0–499 |
| Praticante | 500–1499 |
| Especialista | 1500–2999 |
| Mestre | 3000+ |

### Endpoint
```
GET /academy/ranking/gamified
```

### Resposta por usuário
```json
{
  "position": 1,
  "user_id": "USR-001",
  "xp": 1850,
  "level": "Especialista",
  "sessions": 12,
  "certifications": 3
}
```

### Critérios de aceite
- [ ] XP calculado corretamente (sandbox + certifications)
- [ ] Nível inferido do XP
- [ ] Posição no ranking calculada por XP descendente
- [ ] Exibido no Trading Desk (ISSUE 26)

### Dependências
- ISSUE 10, ISSUE 8

### Referência de implementação
`src/app.js` → `/academy/ranking/gamified`'

echo "✅ Issues Bloco 10 criadas"

# ─── BLOCO 11 — RBAC ─────────────────────────────────────────────────────────

create_issue \
"[ISSUE 28] Criar papéis educacionais (RBAC da Academia)" \
"bloco-11-rbac,priority-high" \
'## 🔐 Bloco 11 — RBAC | Papéis Educacionais

### Objetivo
Definir o controle de acesso baseado em papéis específico da Academia do Saber.

### Papéis e permissões

| Papel | Permissões |
|-------|-----------|
| ADMIN | `*` — acesso total |
| INSTRUCTOR | `courses:create,read`, `tracks:read`, `users:read`, `metrics:read` |
| USER | `courses:read`, `lessons:complete`, `progress:write` |
| CLIENT | `saas:read`, `marketplace:read` (cliente externo) |

### Holding RBAC (integração com ecossistema)

| Role Holding | Permissões Academy |
|-------------|-------------------|
| holding_admin | `*` |
| academy_director | courses, tracks, hr, metrics, john, cefeida, legal, saas |
| pd_ia_operator | courses:read, cefeida, metrics |
| instructor | courses, tracks, sandbox, replay, john |
| operations | courses:read, hr, sandbox, metrics |
| auditor | courses:read, tracks, metrics, legal, replay |

### Endpoints
```
GET /academy/rbac/roles
GET /academy/rbac/roles/:role
```

### Critérios de aceite
- [ ] 4 papéis educacionais definidos
- [ ] Integração com RBAC da Holding existente
- [ ] Endpoint retorna permissões por papel
- [ ] 404 para papel inexistente com lista de disponíveis

### Dependências
Nenhuma (paralelo à implementação).

### Referência de implementação
`src/app.js` → `/academy/rbac/*`, `api/main.py` → `RBAC dict`'

create_issue \
"[ISSUE 29] Permissão de trilha por monólito (RBAC por domínio)" \
"bloco-11-rbac,priority-medium" \
'## 🔐 Bloco 11 — RBAC | Permissão por Monólito

### Objetivo
Cada monólito define quais trilhas são obrigatórias e quais requerem permissão especial.

### Modelo de permissão

```json
{
  "archimedes": {
    "required_tracks": ["cultura_liceu", "vendas", "juridico_basico"],
    "optional_tracks": ["bim_avancado", "financeiro"],
    "admin_only_tracks": ["master_class_imobi"]
  }
}
```

### Regras
- `required_tracks` → usuário SEM essa trilha não acessa o monólito
- `optional_tracks` → visível mas não obrigatório
- `admin_only_tracks` → somente ADMIN ou academy_director

### Integração com onboarding
- Ao criar usuário num monólito → `required_tracks` atribuídas automaticamente

### Critérios de aceite
- [ ] Mapeamento por monólito configurável
- [ ] Validação automática no middleware de autenticação
- [ ] `required_tracks` incluídas no onboarding (ISSUE 11)
- [ ] Documentação do contrato entre monólitos

### Dependências
- ISSUE 28, ISSUE 11, ISSUE 3

### Referência de implementação
`src/data.js` → `mandatoryTracksByRole`, `educationalRoles`'

echo "✅ Issues Bloco 11 criadas"

# ─── BLOCO 12 — CORE_DNA + JOHN ──────────────────────────────────────────────

create_issue \
"[ISSUE 30] Alimentar Core_DNA — aprendizado do John" \
"bloco-12-core-dna,priority-high" \
'## 🧬 Bloco 12 — Core_DNA + John | Alimentar Core_DNA

### Objetivo
A Academia alimenta o `core_dna` do John com conhecimento derivado do aprendizado dos usuários.

### Evento publicado
```
Subject: core_dna.update
Payload: {
  "user": "john",
  "skill": "juridico",
  "knowledge": "Corretores que concluem trilha jurídica fecham 32% mais contratos",
  "confidence": 0.92
}
```

### Endpoint
```
POST /academy/john/feed-dna
Body: { source, knowledge, domain, confidence }
```

### Fontes de conhecimento para Core_DNA
- Padrões de erro recorrentes (ISSUE 7)
- Correlações treinamento × performance (ISSUE 17)
- Insights de certificação (ISSUE 10)
- Análises CEFEIDA (ISSUE 24)

### Resposta
```json
{
  "message": "Conhecimento absorvido pelo core_dna do John.",
  "entry": { "status": "absorbed", "confidence": 0.92 }
}
```

### Critérios de aceite
- [ ] Endpoint funcional com validação de campos
- [ ] Evento `core_dna.update` publicado no NATS
- [ ] Stream CORE_DNA configurado (ISSUE 21)
- [ ] Log persistido em `john_dna_feed`

### Dependências
- ISSUE 17, ISSUE 21, ISSUE 22

### Referência de implementação
`src/app.js` → `/academy/john/feed-dna`'

create_issue \
"[ISSUE 31] John como professor — geração de aulas e dúvidas" \
"bloco-12-core-dna,priority-medium" \
'## 🧬 Bloco 12 — Core_DNA + John | John como Professor

### Objetivo
Usar o John Brasileiro como motor pedagógico ativo: gerando aulas, respondendo dúvidas e simulando cenários.

### Funcionalidades
1. **Gerar aula** sobre qualquer tópico do ecossistema
2. **Responder dúvida** textual do usuário
3. **Simular cenário** prático aplicado

### Endpoint
```
POST /academy/john/teach
Body: {
  "user_id": "USR-001",
  "topic": "Contratos Imobiliários",
  "doubt": "Qual a diferença entre promessa e contrato definitivo?"
}
```

### Estrutura de resposta
```json
{
  "teacher": "John Brasileiro — IA Pedagógico",
  "lesson": {
    "introduction": "...",
    "key_points": ["...", "...", "...", "..."],
    "scenario": "...",
    "challenge": "...",
    "next_recommendation": "..."
  },
  "answered_doubt": "..."
}
```

### Critérios de aceite
- [ ] Estrutura completa de aula retornada
- [ ] Dúvida ecoada na resposta quando fornecida
- [ ] Scenario contextualizado ao ecossistema LICEU
- [ ] Recommendation para próxima trilha
- [ ] Funciona para qualquer tópico (genérico e domínio-específico)

### Dependências
- ISSUE 5, ISSUE 30

### Referência de implementação
`src/app.js` → `/academy/john/teach`'

echo "✅ Issues Bloco 12 criadas"

# ─── BLOCO 13 — KANBAN GLOBAL ─────────────────────────────────────────────────

create_issue \
"[ISSUE 32] Kanban Global → task gera treinamento automático" \
"bloco-13-kanban,priority-medium" \
'## 🧩 Bloco 13 — Kanban Global | Task como Aprendizado

### Objetivo
Integrar o Kanban Global com a Academia para que tasks bloqueadas ou falhas gerem treinamentos automáticos.

### Lógica de trigger
```
task.outcome == "blocked" || "failed"
    ↓
Gerar treinamento de reforço no domínio da task
    ↓
Publicar academy.john_recommended
Publicar academy.task.learning_generated
```

### Endpoint
```
POST /academy/kanban/task-learning
POST /academy/from-task   ← integração direta via evento NATS
```

### Body
```json
{
  "task_id": "TASK-101",
  "user_id": "USR-001",
  "task_title": "Elaborar contrato de permuta",
  "task_domain": "juridico",
  "task_outcome": "blocked"
}
```

### Resposta inclui
- `generated_training` — somente se `blocked` ou `failed`
  - `urgency: "alta"`
  - `suggested_track`
  - `reason`
- `recommendation` — texto personalizado

### Critérios de aceite
- [ ] Task `blocked`/`failed` → gera treinamento com urgência "alta"
- [ ] Task `completed` → sem treinamento gerado (null)
- [ ] Eventos NATS publicados quando necessário
- [ ] Registro persistido em `task_learnings`

### Dependências
- ISSUE 22, ISSUE 5

### Referência de implementação
`src/app.js` → `/academy/kanban/task-learning`'

create_issue \
"[ISSUE 33] Feedback loop — erro → aprendizado → melhoria → execução" \
"bloco-13-kanban,priority-medium" \
'## 🧩 Bloco 13 — Kanban Global | Feedback Loop Completo

### Objetivo
Fechar o ciclo de aprendizado: erro identificado → conteúdo gerado → treinamento concluído → melhoria na execução.

### Fluxo completo
```
1. Erro ocorre (deal perdido, task bloqueada, audit negativo)
        ↓
2. Sistema registra erro (source_system: Archimedes/Kanban/Audit)
        ↓
3. John gera lição automática (ISSUE 7)
        ↓
4. CEFEIDA gera microlearning adaptado (ISSUE 25)
        ↓
5. Usuário completa treinamento
        ↓
6. Score cognitivo atualizado (ISSUE 6)
        ↓
7. Core_DNA alimentado (ISSUE 30)
        ↓
8. John recomenda reexecução (ISSUE 5)
        ↓
9. Resultado melhora
        ↓
10. Correlação confirmada (ISSUE 17)
```

### Métricas do loop
- `time_to_learn` — tempo entre erro e conclusão do treinamento
- `improvement_rate` — variação de score antes/depois
- `recurrence_rate` — se o mesmo erro volta a ocorrer

### Critérios de aceite
- [ ] Todas as 10 etapas documentadas e rastreáveis via eventos NATS
- [ ] Métricas do loop disponíveis no dashboard (ISSUE 16)
- [ ] Recorrência detectável via `error_lessons` (ISSUE 7)
- [ ] John notificado ao completar o ciclo

### Dependências
- ISSUE 7, ISSUE 25, ISSUE 30, ISSUE 17

### Referência de implementação
Integração transversal: `src/app.js`, `api/main.py`, eventos NATS'

echo "✅ Issues Bloco 13 criadas"

# ─── BLOCO 14 — INFRA / DEPLOY ────────────────────────────────────────────────

create_issue \
"[ISSUE 34] Docker stack — full stack da Academia" \
"bloco-14-infra,priority-high" \
'## 🐳 Bloco 14 — Infra | Docker Stack

### Objetivo
Orquestrar todos os serviços da Academia do Saber em Docker Compose para desenvolvimento e produção.

### Serviços

| Serviço | Porta | Imagem |
|---------|-------|--------|
| `academy-api` | 8010 | Python 3.12 + FastAPI |
| `academy-node` | 3000 | Node.js 20 + Express |
| `academy-desk` | 8080 | React + Nginx |
| `postgres` | 5432 | postgres:15-alpine |
| `nats` | 4222 / 8222 | nats:2.10-alpine |
| `nats-init` | — | natsio/nats-box |
| `redis` | 6379 | redis:7-alpine |
| `adminer` | 8090 | adminer:latest |

### Health checks
- PostgreSQL: `pg_isready`
- Academy API: `GET /`

### Inicialização automática
- Schema SQL aplicado via `docker-entrypoint-initdb.d`
- NATS streams criados via `nats-init` service

### Comandos

```bash
# Subir tudo
docker compose up --build

# Apenas API + infra
docker compose up academy-api postgres nats

# Testar Node.js
npm test
```

### Critérios de aceite
- [ ] `docker compose up --build` funciona sem intervenção
- [ ] Schema aplicado automaticamente no postgres
- [ ] NATS streams criados pelo `nats-init`
- [ ] Health checks configurados
- [ ] Variáveis de ambiente documentadas

### Dependências
- Todas as Issues anteriores.

### Referência de implementação
`docker-compose.yml`, `api/Dockerfile`, `frontend/Dockerfile`, `Dockerfile.node`'

create_issue \
"[ISSUE 35] Deploy em produção — CI/CD, monitoramento e logs" \
"bloco-14-infra,priority-medium" \
'## 🚀 Bloco 14 — Infra | Deploy Produção

### Objetivo
Definir e implementar pipeline de CI/CD, monitoramento e observabilidade para a Academia em produção.

### Pipeline CI/CD (GitHub Actions)

```yaml
# Triggers
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Jobs
jobs:
  test-node:   # npm test (41 testes)
  test-python: # pytest api/
  build-api:   # docker build api/
  build-frontend: # docker build frontend/
  deploy:      # SSH + docker compose pull && up
```

### Monitoramento

| Ferramenta | Uso |
|-----------|-----|
| NATS monitoring | :8222 — streams, consumers, mensagens |
| Adminer | :8090 — inspeção do banco |
| FastAPI Docs | :8010/docs — OpenAPI interativo |
| Logs centralizados | `docker compose logs -f academy-api` |

### Variáveis de ambiente de produção

```env
DATABASE_URL=postgresql://academy:SECRET@postgres:5432/academy
NATS_URL=nats://nats:4222
ENV=production
PORT=3000
```

### Checklist de Deploy

- [ ] GitHub Actions configurado (test → build → deploy)
- [ ] Secrets configurados no repositório GitHub
- [ ] `npm test` passando (41 testes)
- [ ] Health checks em todos os serviços
- [ ] Backup automático do PostgreSQL
- [ ] Alertas de erro configurados
- [ ] Documentação OpenAPI disponível em /docs
- [ ] README atualizado com instruções de deploy

### Dependências
- ISSUE 34

### Referência de implementação
`.github/workflows/`, `docker-compose.yml`'

echo "✅ Issues Bloco 14 criadas"
echo ""
echo "════════════════════════════════════════════"
echo "✅  TODAS AS 35 ISSUES CRIADAS COM SUCESSO"
echo "════════════════════════════════════════════"
