# LICEU ACADEMIA DO SABER 7.0

> **Missão:** Tornar o aprendizado uma constância vitalícia (3 a 120 anos).  
> **Visão:** Ser o modelo global de educação interdisciplinar e prática.

---

## Sumário

1. [Manifesto 7.0](#manifesto-70)
2. [Nova Visão da Academia](#nova-visão-da-academia)
3. [Conceito Operacional](#conceito-operacional)
4. [Arquitetura Alvo 7.0](#arquitetura-alvo-70)
5. [Módulos Estratégicos 7.0](#módulos-estratégicos-70)
6. [Novos Endpoints 7.0](#novos-endpoints-70)
7. [Evolução de Dados Cognitivos](#evolução-de-dados-cognitivos)
8. [NATS e Escalabilidade](#nats-e-escalabilidade)
9. [Épicos e Fases 7.0](#épicos-e-fases-70)
10. [Sobre o Projeto (Estado Atual)](#sobre-o-projeto-estado-atual)
11. [Arquitetura](#arquitetura)
12. [Serviços e Portas](#serviços-e-portas)
13. [Como Executar](#como-executar)
   - [Node.js (local)](#nodejs-local)
   - [FastAPI Python (local)](#fastapi-python-local)
   - [Docker Compose (stack completa)](#docker-compose-stack-completa)
14. [Autenticação RBAC](#autenticação-rbac)
15. [Endpoints da API](#endpoints-da-api)
   - [Estrutura Escolar](#estrutura-escolar)
   - [John Educacional (IA Pedagógica)](#john-educacional-ia-pedagógica)
   - [Gamificação](#gamificação)
   - [Laboratório Virtual](#laboratório-virtual)
   - [SDK de Certificação](#sdk-de-certificação)
   - [Eventos P&D.IA](#eventos-pdia)
   - [Onboarding / RH — HubBackoffice](#onboarding--rh--hubbackoffice)
   - [Compliance Jurídico](#compliance-jurídico)
   - [Métricas e Dashboard](#métricas-e-dashboard)
   - [EdTech Externo (SaaS / Marketplace)](#edtech-externo-saas--marketplace)
   - [CEFEIDA — IA de Aprendizado](#cefeida--ia-de-aprendizado)
   - [Trading Desk Educacional](#trading-desk-educacional)
   - [RBAC da Academia](#rbac-da-academia)
   - [Core DNA + John como Professor](#core-dna--john-como-professor)
   - [Kanban Global e Feedback Loop](#kanban-global-e-feedback-loop)
   - [RBAC por Domínio (Monólito)](#rbac-por-domínio-monólito)
16. [NATS JetStream — Streams e Eventos](#nats-jetstream--streams-e-eventos)
17. [Schema SQL Enterprise](#schema-sql-enterprise)
18. [Estrutura Educacional](#estrutura-educacional)
19. [Testes Automatizados](#testes-automatizados)
20. [CI/CD](#cicd)
21. [Roadmap de Issues](#roadmap-de-issues)

---

## Manifesto 7.0

"A infraestrutura educacional viva do ecossistema LICEU"

A Academia deixa de ser uma plataforma de cursos e evolui para um **Sistema Operacional Cognitivo de Aprendizado Contínuo Global** integrado ao ecossistema:

- HUBBACKOFFICE
- GAME MKT
- FORNECEDORES
- ECONO.TECH
- BIM.ARQ.ENG
- OPERA
- CORE DNA
- JOHN
- CEFEIDA
- P&D.IA

Resultado esperado: **engine de evolução humana do ecossistema**.

---

## Nova Visão da Academia

| Camada | Objetivo |
|--------|----------|
| Educação Base | Crianças e jovens |
| Formação Técnica | Profissionalização |
| Educação Corporativa | Empresas |
| Universidade LICEU | Engenharia, IA, BIM |
| Academia Operacional | Obras reais |
| Simuladores | Digital Twin |
| Laboratórios | Físicos + virtuais |
| Holografia | Ensino imersivo |
| Marketplace Educacional | Especialistas externos |
| Editora GAME MKT | Conteúdo didático |
| IA Pedagógica | John + CEFEIDA |
| Sistema Cognitivo | CORE DNA |
| Universidade SaaS | White-label |
| Centro de Pesquisa | P&D.IA |
| Arena Competitiva | Gamificação |
| Formação Industrial | Fornecedores |
| Incubadora de Talentos | RH + HUB |
| Academia Senior | 60+ |
| Academia Infantil | 3–12 |
| Academia Maker | Robótica/IoT |
| Escola de Negócios | Holding/financeiro |
| Escola ESG | Sustentabilidade |

---

## Conceito Operacional

**ACADEMIA = Simulador de Vida Real.**

O aluno passa a aprender por execução contextual:

- operação de obras simuladas e reais
- gestão de empresas e fluxo financeiro
- resolução de problemas de campo
- laboratório virtual e holografia
- interação contínua com IA (John e CEFEIDA)
- participação em squads e trading desks

---

## Arquitetura Alvo 7.0

```text
academy/
├── apps/
│   ├── api-node/
│   ├── api-python/
│   ├── frontend/
│   ├── holographic-engine/
│   ├── simulation-engine/
│   ├── game-engine/
│   ├── virtual-campus/
│   ├── mobile/
│   └── ai-learning-engine/
├── modules/
│   ├── john-teacher/
│   ├── cefeida/
│   ├── core-dna/
│   ├── gamification/
│   ├── holography/
│   ├── virtual-labs/
│   ├── publishing/
│   ├── certifications/
│   ├── edtech-marketplace/
│   ├── corporate-training/
│   ├── supplier-training/
│   ├── university/
│   ├── maker-space/
│   ├── simulation/
│   ├── live-classes/
│   ├── streaming/
│   ├── analytics/
│   ├── esports-learning/
│   ├── digital-twin-campus/
│   └── cognitive-analysis/
├── infra/
├── kubernetes/
├── terraform/
├── docker/
└── docs/
```

---

## Módulos Estratégicos 7.0

1. **John Professor 7.0:** aula ao vivo adaptativa, voz, simulação e prevenção de evasão.
2. **CORE DNA Educacional:** mapeamento cognitivo profundo e evolução de perfil.
3. **Laboratórios Virtuais:** estrutural, BIM, robótica, ESG, financeiro, industrial, energia e IA.
4. **Campus Digital Twin:** campus 3D com avatar, auditórios, fábricas e cidade virtual.
5. **Game Engine Educacional:** XP, níveis, guildas, torneios e economia gamificada.
6. **Editora GAME MKT:** produção de livros, vídeos, podcasts, holografias e avaliações.
7. **CEFEIDA Learning Engine:** detecção de sobrecarga e adaptação cognitiva contínua.
8. **Streaming Nativo:** WebRTC, replay, tradução, legenda e analytics ao vivo.
9. **Academia Infantil:** foco em criatividade, lógica, ciência e sustentabilidade.
10. **Academia Longevidade:** inclusão digital e trilhas assistidas para 60+.
11. **Academia Industrial:** trilhas para operadores, logística, qualidade e Six Sigma.
12. **Corporate University SaaS:** white-label para empresas externas.
13. **Marketplace Educacional:** venda de cursos, mentorias e simuladores.
14. **Trading Desk 2.0:** KPIs cognitivos, heatmaps e learning economy.
15. **Mobile App:** offline-first, voz, AR e laboratório mobile.
16. **Sistema de Talentos:** detecção de líderes e integração com RH/HUBBACKOFFICE.
17. **Holografia:** engine de professor holográfico e walkthrough BIM.
18. **Integração com OPERA:** treinamento em recebimento, logística e execução.
19. **Eventos NATS dedicados:** streams de holografia, simulação, cognitivo, marketplace e streaming.
20. **Kubernetes:** desacoplamento de APIs, IA, streaming e consumidores NATS.
21. **IA Operacional integrada:** John, CEFEIDA, Core DNA, P&D IA, Opera AI e Econo AI.
22. **Universidade LICEU:** trilhas superiores com certificação avançada.
23. **Token educacional:** incentivo de aprendizagem via ECONO.TECH.
24. **Loop de evolução:** erro -> feedback -> treino -> Core DNA -> John -> melhoria operacional.

---

## Novos Endpoints 7.0

| Método | Endpoint | Objetivo |
|--------|----------|----------|
| POST | `/john/academy/live-teaching` | Aula imersiva adaptativa em tempo real |
| POST | `/academy/labs/start` | Iniciar laboratório virtual por domínio |
| POST | `/corporate-university/create` | Provisionar universidade white-label |

Exemplo de payload para aula imersiva:

```json
{
  "student_id": "USR-001",
  "topic": "Estruturas metálicas",
  "mode": "immersive"
}
```

Exemplo de resposta esperada:

```json
{
  "lesson_id": "LESSON-9001",
  "holographic_scene": true,
  "difficulty_adapted": true,
  "simulation_enabled": true,
  "voice_tutor": "john_ptbr"
}
```

---

## Evolução de Dados Cognitivos

Tabela proposta para evolução do CORE DNA educacional:

```sql
CREATE TABLE cognitive_dna (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  logical_score NUMERIC(5,2),
  engineering_score NUMERIC(5,2),
  leadership_score NUMERIC(5,2),
  creativity_score NUMERIC(5,2),
  emotional_score NUMERIC(5,2),
  adaptive_learning_score NUMERIC(5,2),
  burnout_risk NUMERIC(5,2),
  generated_at TIMESTAMP DEFAULT now()
);
```

---

## NATS e Escalabilidade

Streams novos planejados para 7.0:

- `ACADEMY_HOLOGRAPHY`
- `ACADEMY_SIMULATION`
- `ACADEMY_COGNITIVE`
- `ACADEMY_GAMIFICATION`
- `ACADEMY_MARKETPLACE`
- `ACADEMY_STREAMING`

Workloads Kubernetes alvo:

- `academy-api`
- `academy-ai`
- `academy-streaming`
- `academy-websocket`
- `academy-holography`
- `academy-simulation`
- `academy-frontend`
- `academy-mobile-gateway`
- `academy-nats-consumer`

---

## Épicos e Fases 7.0

| Épico | Escopo | Resultado esperado |
|-------|--------|--------------------|
| E1 | Cognitive Core (John + CEFEIDA + CORE DNA) | Aprendizado adaptativo em tempo real |
| E2 | Simulação e Holografia | Ambiente imersivo de prática |
| E3 | Marketplace e Editora | Escala de conteúdo e especialistas |
| E4 | Corporate University SaaS | Expansão B2B white-label |
| E5 | Mobile + Streaming Nativo | Aprendizado ubiquo e síncrono |
| E6 | Operação e Talentos | Integração Academia -> RH/HUB |

Plano detalhado por fase, critérios de aceite e entregáveis: [docs/PLANO-7.0.md](docs/PLANO-7.0.md)

---

## Sobre o Projeto (Estado Atual)

O **LICEU ACADEMIA DO SABER** é a plataforma de educação contínua do ecossistema LICEU 6.0 / LICEU ENGENHARIA, cobrindo desde o Ensino Fundamental até o Técnico Profissionalizante com prática real. O sistema expõe:

- **API Node.js/Express** (porta 3000) — back-end principal
- **API FastAPI Python** (porta 8010) — back-end paralelo com WebSocket em tempo real
- **Frontend React** (porta 8080) — Trading Desk educacional dark theme
- **NATS JetStream** — barramento de eventos (6 streams)
- **PostgreSQL 15** — banco enterprise com schema completo
- **Redis** — cache e sessão

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                  LICEU ACADEMIA DO SABER                │
│                                                         │
│  [React:8080]  ──►  [FastAPI:8010]  ──►  [NATS:4222]   │
│                          │                    │         │
│  [Express:3000] ─────────┘            [PostgreSQL:5432] │
│                                       [Redis:6379]      │
│  [Adminer:8090]  (admin DB)                             │
└─────────────────────────────────────────────────────────┘
```

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Back-end principal | Node.js + Express | 20 LTS |
| Back-end paralelo | FastAPI + Uvicorn | Python 3.11 |
| Front-end | React + Vite + Tailwind | React 18 |
| Banco de dados | PostgreSQL | 15 |
| Mensageria | NATS JetStream | latest |
| Cache | Redis | 7 |
| Containerização | Docker Compose | v2 |
| CI/CD | GitHub Actions | — |

---

## Serviços e Portas

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| `academy-node` | **3000** | API Node.js/Express principal |
| `academy-api` | **8010** | API FastAPI + WebSocket `/events/ws` |
| `academy-desk` | **8080** | Frontend React (Nginx) |
| `postgres` | **5432** | PostgreSQL 15 |
| `nats` | **4222** / 8222 | NATS JetStream (cliente / monitoring) |
| `redis` | **6379** | Redis 7 |
| `adminer` | **8090** | Admin web do banco de dados |

---

## Como Executar

### Node.js (local)

```bash
npm install
npm start          # servidor em http://localhost:3000
npm test           # suite de 42 testes automatizados
```

### FastAPI Python (local)

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8010 --reload
# docs interativas em http://localhost:8010/docs
```

### Docker Compose (stack completa)

```bash
docker compose up --build
```

Sobe todos os 8 serviços. Aguarde o healthcheck do PostgreSQL antes de usar.

---

## Autenticação RBAC

Todos os endpoints de domínio exigem o header:

```
x-holding-user-id: <ID>
```

### Usuários da Holding

| ID | Role | Permissões principais |
|----|------|-----------------------|
| `HLD-001` | `holding_admin` | Acesso total |
| `HLD-002` | `academy_director` | Gestão educacional |
| `HLD-003` | `pd_ia_operator` | P&D, CEFEIDA, Core DNA |
| `HLD-004` | `instructor` | Cursos, avaliações |
| `HLD-005` | `operations` | Onboarding, Kanban |
| `HLD-006` | `auditor` | Leitura e compliance |

---

## Endpoints da API

> Disponíveis em `http://localhost:3000` (Node) e `http://localhost:8010` (FastAPI).

---

### Estrutura Escolar

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/school/fundamental` | Currículo do Ensino Fundamental |
| GET | `/school/high-school` | Currículo do Ensino Médio |
| GET | `/school/technical` | Trilhas técnicas profissionalizantes |
| POST | `/school/enroll` | Matrícula de aluno |

```bash
curl http://localhost:3000/school/technical

curl -X POST http://localhost:3000/school/enroll \
  -H "Content-Type: application/json" \
  -d '{"name":"Maria","age":16,"track":"tecnico_edificacoes"}'
```

---

### John Educacional (IA Pedagógica)

| Método | Path | Descrição |
|--------|------|-----------|
| POST | `/john/academy/recommend` | Recomendação de trilha por idade/perfil |
| POST | `/john/academy/evaluate` | Avaliação cognitiva do aluno |
| POST | `/john/academy/career-path` | Caminho de carreira sugerido |
| POST | `/john/academy/learning-plan` | Plano de aprendizado personalizado |

```bash
curl -X POST http://localhost:3000/john/academy/recommend \
  -H "x-holding-user-id: HLD-004" \
  -H "Content-Type: application/json" \
  -d '{"age": 16}'
```

---

### Gamificação

| Método | Path | Descrição |
|--------|------|-----------|
| POST | `/academy/gamification/start` | Iniciar missão gamificada |
| POST | `/academy/gamification/visit` | Registrar visita a obra virtual |
| GET | `/academy/gamification/ranking` | Ranking de XP e nível dos alunos |

---

### Laboratório Virtual

| Método | Path | Descrição |
|--------|------|-----------|
| POST | `/academy/lab/simulate` | Executar simulação (estrutura, energia, IoT) |
| POST | `/academy/lab/material-test` | Ensaio virtual de materiais |
| GET | `/academy/lab/results` | Resultados dos experimentos |

---

### SDK de Certificação

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/sdk/certification/tracks` | Listar trilhas de certificação |
| POST | `/sdk/certification/tracks` | Criar nova trilha |
| GET | `/sdk/certification/courses` | Listar cursos por trilha |

---

### Eventos P&D.IA

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/pd-ia/events/new-technologies` | Listar novas tecnologias P&D |
| POST | `/pd-ia/events/new-technologies` | Publicar nova tecnologia e gerar curso |

```bash
curl -X POST http://localhost:3000/pd-ia/events/new-technologies \
  -H "x-holding-user-id: HLD-003" \
  -H "Content-Type: application/json" \
  -d '{"title":"BIM 6D com IA generativa","domain":"BIM","level":"avancado","workloadHours":40,"skillTags":["bim","ia","planejamento"]}'
```

---

### Onboarding / RH — HubBackoffice

| Método | Path | Descrição |
|--------|------|-----------|
| POST | `/academy/onboarding/start` | Iniciar onboarding de novo colaborador |
| GET | `/academy/onboarding/status/:userId` | Status do onboarding |
| GET | `/academy/training/required/:role` | Treinamentos obrigatórios por função |
| GET | `/academy/training/contract-type/:type` | Trilhas CLT vs PJ |

---

### Compliance Jurídico

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/academy/compliance/required` | Treinamentos de compliance obrigatórios |
| POST | `/academy/compliance/validate` | Validar conformidade de treinamento |
| POST | `/juridico/validate-training` | Evento de validação jurídica |

---

### Métricas e Dashboard

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/academy/metrics/dashboard` | KPIs educacionais consolidados |
| GET | `/academy/metrics/performance-correlation` | Correlação treinamento × performance real |

---

### EdTech Externo (SaaS / Marketplace)

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/edtech/saas/plans` | Planos SaaS disponíveis |
| POST | `/edtech/saas/subscribe` | Assinar plano EdTech |
| GET | `/edtech/marketplace/courses` | Cursos no marketplace |
| POST | `/edtech/marketplace/publish` | Publicar curso de especialista |
| GET | `/edtech/white-label/config` | Configuração white-label corporativo |

---

### CEFEIDA — IA de Aprendizado

| Método | Path | Descrição |
|--------|------|-----------|
| POST | `/cefeida/behavioral-analysis` | Análise comportamental do aluno |
| POST | `/cefeida/adaptive-content` | Geração de conteúdo adaptativo |
| GET | `/cefeida/learning-profile/:userId` | Perfil de aprendizado CEFEIDA |

---

### Trading Desk Educacional

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/academy/desk/overview` | Painel geral da Academia (KPIs ao vivo) |
| GET | `/academy/desk/live-feed` | Feed em tempo real de eventos educacionais |

> **Frontend:** `http://localhost:8080` — Trading Desk React com tema dark, conecta ao WebSocket `/events/ws` do FastAPI.

---

### RBAC da Academia

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/holding/rbac/users` | Listar usuários e papéis da Holding |
| GET | `/academy/roles` | Papéis educacionais disponíveis |
| POST | `/academy/roles/assign` | Atribuir papel a usuário |

---

### Core DNA + John como Professor

| Método | Path | Descrição |
|--------|------|-----------|
| POST | `/core-dna/feed` | Alimentar Core DNA com aprendizado |
| GET | `/core-dna/profile/:userId` | Perfil Core DNA do usuário |
| POST | `/john/academy/generate-lesson` | John gera aula automaticamente |
| POST | `/john/academy/answer-question` | John responde dúvidas do aluno |

---

### Kanban Global e Feedback Loop

| Método | Path | Descrição |
|--------|------|-----------|
| POST | `/kanban/task-training` | Task do Kanban gera treinamento automático |
| GET | `/kanban/training-queue` | Fila de treinamentos gerados |
| POST | `/academy/feedback-loop` | Ciclo feedback: erro → lição → score → execução |
| GET | `/academy/feedback-loop/:userId` | Histórico de ciclos de feedback |

```bash
# Ciclo de feedback completo (6 passos)
curl -X POST http://localhost:3000/academy/feedback-loop \
  -H "x-holding-user-id: HLD-001" \
  -H "Content-Type: application/json" \
  -d '{"userId":"USR-001","errorType":"structural_calculation","context":"obra_residencial"}'
# Retorna: step1_error_captured → step2_lesson_generated →
#   step3_training_triggered → step4_score_updated →
#   step5_core_dna_fed → step6_reexecution_ready
```

---

### RBAC por Domínio (Monólito)

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/academy/monolith-rbac` | RBAC de todos os monólitos |
| GET | `/academy/monolith-rbac/:monolith` | Trilhas required/optional/admin por monólito |

**Monólitos:** `archimedes` · `opera` · `cea` · `juridico` · `cefeida` · `john` · `gameMkt`

```bash
curl http://localhost:3000/academy/monolith-rbac/archimedes
```

---

## NATS JetStream — Streams e Eventos

| Stream | Subjects | Retenção | Descrição |
|--------|---------|----------|-----------|
| `ACADEMY` | `academy.>` | 72h | Eventos educacionais principais |
| `JOHN` | `john.>` | 24h | Eventos do tutor IA John |
| `CORE_DNA` | `core_dna.>` | 168h | Perfil cognitivo e aprendizado |
| `HUB` | `hub.>` | 48h | HubBackoffice (RH, DP, onboarding) |
| `JURIDICO` | `juridico.>` | 168h | Compliance e validação jurídica |
| `KANBAN` | `kanban.>` | 24h | Tarefas e treinamentos automáticos |

**WebSocket em tempo real:** `ws://localhost:8010/events/ws`  
Todos os eventos publicados no NATS são transmitidos via broadcast WebSocket ao Trading Desk.

---

## Schema SQL Enterprise

Arquivo: [schema.sql](schema.sql)

**Extensions:** `pgcrypto`, `pg_trgm`

| Tabela | Descrição |
|--------|-----------|
| `users` | Usuários com UUID, role, tipo contrato |
| `tracks` | Trilhas de certificação por domínio |
| `courses` | Cursos com JSONB de conteúdo |
| `enrollments` | Matrículas com status e progresso |
| `certifications` | Certificações emitidas |
| `cognitive_profiles` | Score cognitivo por usuário |
| `feedback_loops` | Ciclos de erro → aprendizado |
| `kanban_tasks` | Tarefas com geração automática de treinamento |
| `compliance_records` | Registros de conformidade jurídica |
| `core_dna_entries` | Entradas no Core DNA do John |

---

## Estrutura Educacional

| Nível | Faixa Etária | Foco |
|-------|-------------|------|
| Ensino Fundamental | 3–14 anos | Base cognitiva, lógica, ciências, financeiro |
| Ensino Médio Técnico | 15–17 anos | Física, química, BIM, robótica, programação |
| Técnico Profissionalizante | 18+ anos | Edificações, BIM, microgrid, IoT, industrialização |
| Profissionais | Qualquer idade | Reciclagem contínua alinhada ao ecossistema |

---

## Testes Automatizados

```bash
npm test
# ✅ 42 passed / 0 failed
```

42 testes cobrindo todas as 35 issues — ISSUEs 1–33 com testes funcionais de endpoint + RBAC + edge cases.

---

## CI/CD

Pipeline em [.github/workflows/ci.yml](.github/workflows/ci.yml) — executa a cada push/PR em `main`:

| Job | O que faz |
|-----|-----------|
| `test-node` | `npm ci` + `npm test` (42 testes) |
| `test-python` | `pip install` + `py_compile` + import check |
| `build-docker` | Build das 3 imagens (node, api, frontend) |
| `smoke-test` | `docker compose up` + health checks nos 3 serviços |

---

## Roadmap de Issues

<!-- ROADMAP_STATUS_TABLE:BEGIN -->
| Bloco | Tema | Quantidade de Issues | Status |
|-------|------|----------------------|--------|
| Bloco 1 | Foundation | 4 | ✅ Fechado |
| Bloco 2 | John Training Engine | 3 | ✅ Fechado |
| Bloco 3 | Treinamento Operacional | 3 | ✅ Fechado |
| Bloco 4 | HubBackoffice (RH + DP) | 3 | ✅ Fechado |
| Bloco 5 | JuridicoTech | 2 | ✅ Fechado |
| Bloco 6 | Metrics | 2 | ✅ Fechado |
| Bloco 7 | EdTech Externo | 3 | ✅ Fechado |
| Bloco 8 | NATS | 3 | ✅ Fechado |
| Bloco 9 | CEFEIDA | 2 | ✅ Fechado |
| Bloco 10 | Trading Desk | 2 | ✅ Fechado |
| Bloco 11 | RBAC | 2 | ✅ Fechado |
| Bloco 12 | Core_DNA + John | 2 | ✅ Fechado |
| Bloco 13 | Kanban Global | 2 | ✅ Fechado |
| Bloco 14 | Infra / Deploy | 2 | ✅ Fechado |
| **Total** | | **35** | **0 abertas / 35 fechadas** |
<!-- ROADMAP_STATUS_TABLE:END -->

| # | Título | Status |
|---|--------|--------|
| 1 | Criar domínio educacional (core academy) | ✅ |
| 2 | Criar schema SQL enterprise | ✅ |
| 3 | Criar estrutura de trilhas por monólito | ✅ |
| 4 | Criar trilha CORE LICEU obrigatória | ✅ |
| 5 | Integrar John ao aprendizado | ✅ |
| 6 | Criar cognitive_profile — score cognitivo | ✅ |
| 7 | Aprendizado baseado em erro (loss intelligence) | ✅ |
| 8 | Criar Simulation Engine (sandbox) | ✅ |
| 9 | Replay de operações reais | ✅ |
| 10 | Certificação automática por performance | ✅ |
| 11 | Onboarding automático via HubBackoffice | ✅ |
| 12 | Treinamento obrigatório por função (role-based) | ✅ |
| 13 | Suporte a CLT + PJ — trilhas por contrato | ✅ |
| 14 | Compliance educacional obrigatório (JuridicoTech) | ✅ |
| 15 | Integração de validação jurídica | ✅ |
| 16 | Dashboard educacional — KPIs e métricas | ✅ |
| 17 | Correlação treinamento × performance real | ✅ |
| 18 | Academia como produto SaaS (EdTech externo) | ✅ |
| 19 | Marketplace de cursos | ✅ |
| 20 | White-label corporativo | ✅ |
| 21 | Criar stream ACADEMY no NATS JetStream | ✅ |
| 22 | Definir e documentar eventos padrão | ✅ |
| 23 | Integrar eventos Academy com ecossistema | ✅ |
| 24 | IA de aprendizado — análise comportamental (CEFEIDA) | ✅ |
| 25 | Geração de conteúdo dinâmico e adaptativo | ✅ |
| 26 | Tela institucional — Trading Desk educacional | ✅ |
| 27 | Ranking gamificado — XP, nível e performance | ✅ |
| 28 | Criar papéis educacionais (RBAC da Academia) | ✅ |
| 29 | Permissão de trilha por monólito (RBAC por domínio) | ✅ |
| 30 | Alimentar Core_DNA — aprendizado do John | ✅ |
| 31 | John como professor — geração de aulas | ✅ |
| 32 | Kanban Global → task gera treinamento automático | ✅ |
| 33 | Feedback loop — erro → aprendizado → execução | ✅ |
| 34 | Docker stack — full stack da Academia | ✅ |
| 35 | Deploy em produção — CI/CD, monitoramento e logs | ✅ |

---

*LICEU ACADEMIA DO SABER — 35/35 issues implementadas e fechadas.*
