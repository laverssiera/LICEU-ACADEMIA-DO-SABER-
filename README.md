# LICEU ACADEMIA DO SABER

Monorepo da plataforma educacional LICEU, com servicos Node.js e Python, arquitetura orientada a eventos com NATS e stack de suporte para desenvolvimento local via Docker.

## Nova diretriz estrategica

A Academia do Saber deixa de operar apenas como plataforma educacional.

Ela passa a ser:

- infraestrutura cognitiva do ecossistema LICEU;
- motor de formacao continua humana;
- nucleo de transferencia cientifica;
- sistema operacional educacional civilizacional;
- academia tecnica e cientifica orientada a resolucao de problemas reais;
- plataforma de evolucao social, tecnologica e humana.

A missao central nao e emitir diplomas.

A missao e:

- formar solucionadores;
- desenvolver infraestrutura humana;
- reduzir sofrimento social;
- democratizar acesso a engenharia e ciencia;
- acelerar inovacao aplicada;
- gerar impacto positivo em larga escala;
- garantir moradia, infraestrutura e dignidade para todas as pessoas.

O modelo educacional cobre toda a jornada humana:

0 a 120 anos.

A Academia opera integrada com:

- P&D.IA
- OPERA
- BIM.ARQ.ENG
- ANCHOR
- HUB
- JOHN
- GAMEMKT
- laboratorios fisicos;
- runtime cientifico;
- simulacoes avancadas;
- sistemas interplanetarios.

A educacao deixa de ser estatica.

Ela passa a ser:

- adaptativa;
- continua;
- contextual;
- operacional;
- cientifica;
- simulada;
- gamificada;
- aplicada ao mundo real.

## Visao Geral

Este repositorio concentra:

- APIs e engines de aprendizado/simulacao
- Frontends web e apps auxiliares
- Infraestrutura local e manifests de deploy
- Scripts de smoke test e automacoes operacionais

## Stack

- Node.js (Express e servicos HTTP/WebSocket)
- Python (engines de IA e simulacao)
- PostgreSQL
- Redis
- NATS JetStream
- Docker Compose
- Turborepo

## Estrutura do Repositorio

```text
.
├── apps/
│   ├── admin/
│   ├── ai-engine/
│   ├── ai-learning-engine/
│   ├── api-node/
│   ├── api-python/
│   ├── backend/
│   ├── frontend/
│   ├── frontend-web/
│   ├── holographic-engine/
│   ├── mobile/
│   ├── realtime/
│   ├── simulation-engine/
│   └── streaming-engine/
├── database/
├── docs/
├── frontend/
├── infra/
├── nats/
├── packages/
├── reports/
├── scripts/
├── src/
├── docker-compose.yml
├── package.json
└── turbo.json
```

## Nova estrutura educacional

```text
apps/
├── academy-core/
├── academy-science/
├── academy-interplanetary/
├── academy-simulations/
├── academy-research/
├── academy-cognitive-runtime/
├── academy-lifelong-learning/
├── academy-holographic-learning/
├── academy-quantum-learning/
├── academy-extreme-engineering/
├── academy-social-impact/
├── academy-health-humanity/
├── academy-climate/
├── academy-robotics/
├── academy-consciousness/
├── academy-exotic-nuclei/
├── academy-oceanic-engineering/
├── academy-space-engineering/
├── academy-digital-twins/
├── academy-labs/
└── academy-knowledge-graph/
```

## Camada de educacao continuada 0-120 anos

```text
academy-lifelong-learning/
├── infancy/
├── childhood/
├── adolescence/
├── technical-formation/
├── scientific-formation/
├── higher-education/
├── masters/
├── doctorate/
├── post-doctorate/
├── elderly-learning/
├── adaptive-learning/
├── accessibility/
├── inclusion/
├── neurodiversity/
└── social-mobility/
```

## Nucleos cientificos

```text
academy-science/
├── cosmology/
├── dark-matter/
├── exotic-nuclei/
├── quantum-computing/
├── fusion-energy/
├── climate-engineering/
├── biosystems/
├── consciousness/
├── longevity/
├── extraterrestrial-life/
├── oceanic-engineering/
├── seismic-engineering/
├── planetary-engineering/
├── social-infrastructure/
├── resilient-cities/
└── autonomous-systems/
```

## Camada interplanetaria educacional

```text
academy-interplanetary/
├── planetary-survival/
├── low-gravity-training/
├── radiation-protection/
├── habitat-engineering/
├── rover-operations/
├── autonomous-research/
├── orbital-structures/
├── planetary-weather/
├── terraforming/
├── interplanetary-logistics/
├── extraterrestrial-biology/
├── cosmic-materials/
└── extreme-environments/
```

## Camada de engenharia extrema

Objetivo:

Treinar:

- engenharia sismica;
- engenharia oceanica;
- cidades resilientes;
- estruturas subterraneas;
- estruturas espaciais;
- sobrevivencia extrema;
- infraestrutura autonoma.

## Camada de simulacao educacional

```text
academy-simulations/
├── earthquake-runtime/
├── wind-tunnel/
├── hydrodynamic-runtime/
├── climate-runtime/
├── orbital-runtime/
├── pressure-runtime/
├── thermal-runtime/
├── structural-runtime/
├── emergency-runtime/
├── city-runtime/
├── social-scenarios/
├── robotics-runtime/
├── holographic-training/
└── digital-twins/
```

## Integracao com hardware real

```text
academy-labs/
├── seismic-tables/
├── wind-tunnels/
├── robotics/
├── drones/
├── vr-ar/
├── holographic-systems/
├── lidar/
├── edge-devices/
├── scientific-sensors/
├── oceanic-simulators/
├── pressure-chambers/
└── telemetry/
```

## Mestrado e doutorado orientado a problemas

```text
academy-research/
├── masters/
├── doctorate/
├── applied-research/
├── ecosystem-problems/
├── scientific-validation/
├── urban-infrastructure/
├── resilient-housing/
├── climate-solutions/
├── social-impact/
├── extreme-engineering/
└── interplanetary-research/
```

## Servicos do Docker Compose

Este repositorio possui dois compose principais:

- docker-compose.yml: stack full stack tradicional (apps web, APIs e engines)
- docker-compose.education.yml: stack educacional e runtime cognitivo da academia

### Stack full stack (docker-compose.yml)

Ao subir o ambiente padrao com docker compose, os servicos publicados sao:

- postgres: 5432
- redis: 6379
- nats: 4222 (cliente) e 8222 (monitoramento)
- backend: 3000
- frontend (apps/frontend): 8080
- mobile: 8090
- simulation-engine: 8100
- ai-learning-engine: 8110
- holographic-engine: 8120
- streaming-engine: 8130
- ai-engine: 8140
- realtime: 8150
- admin: 8160

### Stack educacional (docker-compose.education.yml)

Servicos principais:

- academia-runtime: 8910
- ecosystem-learning-runtime: 8010
- redis: 6379 (interna)
- neo4j: 7687 (interna)
- nats: 4222 (interna)

Health checks:

- academia-runtime: GET /healthz
- ecosystem-learning-runtime: GET /health

## Requisitos

- Docker e Docker Compose
- Node.js 20+
- npm 10+
- Python 3.10+ (para setup local de venv nos apps Python e runtime educacional)

## Execucao local

1. Instalar dependencias JS do workspace:

```bash
npm ci
```

2. Preparar ambientes Python locais (venv + requirements):

```bash
npm run python:setup
```

3. Subir stack full stack padrao:

```bash
npm run up
```

4. Acompanhar logs:

```bash
npm run logs
```

5. Derrubar ambiente:

```bash
npm run down
```

## Execucao da stack educacional

1. Build e subida da stack educacional:

```bash
docker compose -f docker-compose.education.yml up -d --build
```

2. Verificar saude dos runtimes:

```bash
curl -fsS http://localhost:8910/healthz
curl -fsS http://localhost:8010/health
```

3. Derrubar stack educacional:

```bash
docker compose -f docker-compose.education.yml down
```

## Scripts

- npm run dev: executa src/server.js em modo watch
- npm run start: inicia src/server.js
- npm run build: turbo run build
- npm run lint: turbo run lint
- npm run test: testes Node da raiz
- npm run dev:workspace: executa dev em paralelo nos pacotes com Turbo
- npm run test:workspace: executa testes do workspace com Turbo
- npm run up: sobe docker-compose.yml em background com build
- npm run logs: acompanha logs do docker-compose.yml
- npm run down: derruba docker-compose.yml

## Modelo educacional LICEU

O modelo educacional da Academia do Saber nao e baseado apenas em teoria.

Cada aluno deve:

- resolver problemas reais;
- atuar em desafios do ecossistema;
- construir solucoes;
- operar laboratorios;
- participar de simulacoes;
- colaborar com IA;
- desenvolver infraestrutura social;
- gerar impacto mensuravel.

O foco da formacao e:

- dignidade humana;
- moradia;
- infraestrutura;
- ciencia aplicada;
- sustentabilidade;
- engenharia resiliente;
- reducao de desigualdade;
- evolucao civilizacional.

## Smoke Test Full Stack

Existe um script de validacao ponta a ponta em scripts/smoke-fullstack.sh.

Execucao padrao:

```bash
bash scripts/smoke-fullstack.sh
```

Com URL customizada:

```bash
BASE_URL=http://localhost:8010 bash scripts/smoke-fullstack.sh
```

Saida padrao do relatorio:

- reports/smoke-fullstack-report.json

## Autenticacao e RBAC (API raiz em src)

Parte das rotas exige o header abaixo:

```http
x-holding-user-id: HLD-002
```

Sem esse header, endpoints protegidos retornam 401/403 conforme RBAC.

Sem esse header, endpoints protegidos retornam 401/403 conforme RBAC.

<!-- ROADMAP_STATUS_TABLE:BEGIN -->
| Bloco | Tema | Quantidade de Issues | Status |
|-------|------|----------------------|--------|
| Bloco 1 | Foundation | 4 | Concluido |
| Bloco 2 | John Training Engine | 3 | Concluido |
| Bloco 3 | Treinamento Operacional | 3 | Concluido |
| Bloco 4 | HubBackoffice (RH + DP) | 3 | Concluido |
| Bloco 5 | JuridicoTech | 2 | Concluido |
| Bloco 6 | Metrics | 2 | Concluido |
| Bloco 7 | EdTech Externo | 3 | Concluido |
| Bloco 8 | NATS | 3 | Concluido |
| Bloco 9 | CEFEIDA | 2 | Concluido |
| Bloco 10 | Trading Desk | 2 | Concluido |
| Bloco 11 | RBAC | 2 | Concluido |
| Bloco 12 | Core_DNA + John | 2 | Concluido |
| Bloco 13 | Kanban Global | 2 | Concluido |
| Bloco 14 | Infra / Deploy | 2 | Concluido |
| **Total** |  | **35** | **0 abertas / 35 fechadas** |
<!-- ROADMAP_STATUS_TABLE:END -->

## Documentacao Complementar

- docs/PLANO-7.0.md
- docs/contracts/
- infra/docker/README.md
- infra/monitoring/README.md
- reports/readiness-report.md

## Integracao GAMEMKT

O monolito GAMEMKT atua como:

- editora cientifica;
- plataforma de disseminacao;
- motor gamificado de aprendizado;
- runtime narrativo;
- engine de engajamento educacional.

Funcoes:

- publicacao de cursos;
- distribuicao de conteudos;
- gamificacao;
- storytelling cientifico;
- simuladores educacionais;
- desafios interativos;
- rankings;
- jornadas de aprendizado;
- marketplace educacional;
- certificacoes digitais.

## Integracao com P&D.IA

A Academia do Saber recebe continuamente:

- pesquisas;
- simulacoes;
- datasets;
- descobertas cientificas;
- padroes operacionais;
- modelos de IA;
- falhas reais;
- estudos extremos;
- runtime interplanetario.

O conhecimento recebido e convertido em:

- cursos;
- laboratorios;
- trilhas;
- certificacoes;
- simuladores;
- desafios;
- pesquisas aplicadas;
- programas de mestrado e doutorado.

## Pesquisa aplicada orientada ao ecossistema

Toda pesquisa desenvolvida na Academia deve possuir:

- problema real;
- impacto mensuravel;
- aplicabilidade;
- integracao operacional;
- potencial de melhoria social;
- possibilidade de escalabilidade.

A pesquisa nao e orientada apenas a publicacao academica.

Ela deve melhorar:

- moradia;
- infraestrutura;
- mobilidade;
- saude;
- educacao;
- sustentabilidade;
- engenharia resiliente;
- qualidade de vida.

## Endpoints da academia cientifica

Prefixo: /academy/science

- POST /research/create
- POST /research/validate
- POST /research/publish
- POST /scientific-runtime/run
- POST /knowledge/sync
- POST /simulation/generate
- POST /planetary/scenario
- GET /research/domains

## Endpoints interplanetarios

Prefixo: /academy/interplanetary

- POST /habitat/simulate
- POST /radiation/training
- POST /low-gravity/training
- POST /planetary-engineering/run
- POST /orbital-structure/train
- POST /survival/scenario
- POST /terraforming/simulation
- POST /rover/operation/train

## Endpoints educacionais

Prefixo: /academy/learning

- POST /adaptive-path/generate
- POST /student/runtime/update
- POST /skills/map
- POST /mission/create
- POST /ecosystem/problem/assign
- POST /scientific-mentor/connect
- GET /student/evolution
- GET /scientific-profile

## Subjects educacionais

- academy.science.research.created
- academy.science.simulation.generated
- academy.interplanetary.training.started
- academy.learning.path.generated
- academy.student.evolution.updated
- academy.problem.assigned
- academy.problem.solved
- academy.research.validated
- academy.research.promoted
- academy.knowledge.distributed
- academy.gamemkt.content.published
- academy.holographic.training.started
- academy.runtime.simulation.executed

## Camada JOHN EDUCADOR

```text
apps/ai-learning-engine/john_educator/
├── adaptive-learning/
├── cognitive-mapping/
├── scientific-guidance/
├── emotional-support/
├── talent-discovery/
├── research-guidance/
├── mission-allocation/
├── ecosystem-needs/
└── lifelong-learning/
```

## Loop cognitivo do ecossistema

P&D descobre ->
Academia transforma em ensino ->
GAMEMKT dissemina ->
Alunos simulam ->
OPERA executa ->
ANCHOR monitora ->
dados retornam ao P&D ->
o ecossistema evolui.

## Observacoes

- Este monorepo possui mais de um frontend em caminhos diferentes (apps/frontend e frontend na raiz). Verifique o alvo correto antes de desenvolver/deployar.
- O arquivo docker-compose.yml atual sobe apps/frontend (porta 8080), nao o frontend da raiz.

## Variaveis de ambiente

As variaveis de ambiente sao definidas por servico. Consulte os READMEs em apps/<nome-do-app>/README.md para detalhes.

## Ajuste final de posicionamento

A Academia do Saber deixa de ser apenas uma plataforma de ensino.

Ela passa a operar como:

- infraestrutura cognitiva civilizacional;
- universidade viva;
- runtime de evolucao humana;
- sistema operacional de formacao continua;
- academia cientifica integrada ao ecossistema;
- motor de transformacao social.

Seu objetivo final e:

formar pessoas capazes de resolver problemas reais,
reduzir sofrimento humano,
expandir acesso a infraestrutura,
e construir uma sociedade mais digna, resiliente e evolutiva para todas as pessoas.

## Educational Autonomic Runtime - Operacao

Os runtimes abaixo estao integrados no FastAPI da Academia:

- educational_autonomic_runtime
- educational_memory_mesh
- pedagogical_reasoning_runtime
- civilization_education_sync
- federated_learning_identity

Se estiver executando localmente via uvicorn padrao, use `http://localhost:8000`.
Se estiver executando via entrypoint federado, ajuste para a porta definida por `ACADEMIA_RUNTIME_PORT` (padrao 8910).

Para validar todos os endpoints em sequencia com resumo automatico:

```bash
BASE_URL=http://localhost:8000 ./scripts/smoke-educational-autonomic-runtime.sh
```

### 1) Educational Autonomic Runtime

```bash
curl -X POST http://localhost:8000/education/autonomic/evaluate \
	-H "Content-Type: application/json" \
	-d '{
		"student_id":"student-001",
		"discipline":"physics",
		"cognition_score":0.82,
		"consistency":0.74,
		"engagement":0.91
	}'
```

```bash
curl "http://localhost:8000/education/autonomic/history?limit=20"
```

### 2) Educational Memory Mesh

```bash
curl -X POST http://localhost:8000/education/memory-mesh/upsert \
	-H "Content-Type: application/json" \
	-d '{
		"student_id":"student-002",
		"discipline":"chemistry",
		"cognition_score":0.65,
		"consistency":0.55,
		"engagement":0.62
	}'
```

```bash
curl "http://localhost:8000/education/memory-mesh/student/student-002?limit=20"
```

```bash
curl "http://localhost:8000/education/memory-mesh/snapshot?limit=20"
```

### 3) Pedagogical Reasoning Runtime

```bash
curl -X POST http://localhost:8000/education/pedagogical-reasoning/reason \
	-H "Content-Type: application/json" \
	-d '{
		"student_id":"student-003",
		"discipline":"mathematics",
		"cognition_score":0.48,
		"consistency":0.52,
		"engagement":0.50
	}'
```

```bash
curl "http://localhost:8000/education/pedagogical-reasoning/history?limit=20"
```

### 4) Civilization Education Sync

```bash
curl -X POST http://localhost:8000/education/civilization-sync/synchronize \
	-H "Content-Type: application/json" \
	-d '{
		"federation_id":"federation-01",
		"region":"americas",
		"cognition_sync":0.83,
		"curriculum_sync":0.78,
		"intervention_sync":0.81
	}'
```

```bash
curl "http://localhost:8000/education/civilization-sync/history?limit=20"
```

### 5) Federated Learning Identity

```bash
curl -X POST http://localhost:8000/education/federated-identity/generate \
	-H "Content-Type: application/json" \
	-d '{
		"student_id":"student-004",
		"ecosystem":"academy",
		"discipline":"biology",
		"cognition_score":0.79,
		"consistency":0.73,
		"engagement":0.76
	}'
```

```bash
curl "http://localhost:8000/education/federated-identity/history?limit=20"
```
