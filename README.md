# LICEU-ACADEMIA-DO-SABER-
Missão: Tornar o aprendizado uma constância vitalícia (3 a 120 anos). Visão: Ser o modelo global de educação interdisciplinar e prática.
 LICEU ENGENHARIA — LICEU 6.0
Educação contínua do Fundamental ao Técnico com prática real no ecossistema
Missão: Tornar o aprendizado uma constância vitalícia (3 a 120 anos)
Visão: Ser o modelo global de educação interdisciplinar e prática

🧠 Estrutura Educacional Completa
👶 Ensino Fundamental (Base Cognitiva)


matemática aplicada ao cotidiano


lógica e pensamento computacional


ciências com laboratório virtual


educação financeira (ECONO)


sustentabilidade (ANCHOR microgrid)


introdução à engenharia


🧑‍🎓 Ensino Médio (Interdisciplinar Técnico)


física aplicada à construção


química dos materiais


programação básica


BIM introdutório


robótica construção civil


empreendedorismo técnico


🏗️ Ensino Técnico Profissionalizante
Trilhas:


técnico em edificações


técnico BIM


técnico em planejamento obra


técnico energia solar microgrid


técnico IoT construção


técnico manutenção predial


técnico industrialização construção



🎮 Aprendizado Prático Gamificado
Os alunos:


visitam obras virtuais


participam de missões técnicas


simulam canteiros


constroem digitalmente


operam laboratório virtual


evoluem por níveis



🔬 Laboratório Virtual do Ecossistema
Integrações:


gêmeo digital BIM


simulação estrutural


ensaio concreto virtual


simulação instalações


microgrid energia


IoT predial



🧠 John Brasileiro — Diretor Pedagógico Cognitivo
Funções:


tutor por faixa etária


adaptação didática automática


recomendação trilha carreira


avaliação contínua cognitiva


criação automática de cursos


acompanhamento individual aluno


ligação com mercado do ecossistema



🎯 Trilhas por Idade
3–10 anos  → base cognitiva11–14 anos → ciência aplicada15–17 anos → médio técnico18+ anos   → técnico profissionalProfissionais → reciclagem contínua

🎮 Obras Gamificadas Educacionais


visita obra em VR


missões segurança trabalho


simulação montagem estrutura


desafios planejamento


ranking alunos


multiplayer educacional



📡 Endpoints Educacionais
Estrutura Escolar
GET  /school/fundamentalGET  /school/high-schoolGET  /school/technicalPOST /school/enroll
Gamificação
POST /academy/gamification/startPOST /academy/gamification/visitGET  /academy/gamification/ranking
Laboratório
POST /academy/lab/simulatePOST /academy/lab/material-testGET  /academy/lab/results

🧠 John Educacional
POST /john/academy/recommendPOST /john/academy/evaluatePOST /john/academy/career-pathPOST /john/academy/learning-plan

🔗 Integração com Mãe LICEU
A escola recebe:


demandas de capacitação


novas tecnologias P&D


necessidade operacional


gaps profissionais


A escola envia:


profissionais formados


certificações


relatórios competências


evolução educacional



🔄 Fluxo Educacional Ecossistema
P&D cria tecnologia      ↓Mãe LICEU define prioridade      ↓LICEU Engenharia cria curso      ↓John recomenda alunos      ↓Treinamento prático gamificado      ↓Profissionais retornam ao ecossistema

🌐 Fachada Pública (EAD Moderna)


escola digital completa


campus virtual


laboratório virtual


visitas obras gamificadas


trilhas carreira


certificações


ensino fundamental ao técnico



🎯 Papel no Ecossistema
A LICEU ENGENHARIA passa a ser:
✔ escola fundamental
✔ ensino médio técnico
✔ escola técnica profissional
✔ universidade corporativa
✔ laboratório virtual
✔ treinamento contínuo
✔ formação do ecossistema

🧠 Resultado
Você cria:


escola própria completa


formação desde criança


profissionais alinhados ao ecossistema


aprendizado prático real


educação contínua vitalícia

## API inicial implementada

Este repositório agora possui uma API Node.js + Express baseada nos endpoints descritos neste documento.

### Como executar

1. Instale as dependências:

	npm install

2. Inicie a API:

	npm start

Para executar testes automatizados:

	npm test

3. Servidor disponível em:

	http://localhost:3000

### Endpoints disponíveis

Autenticação RBAC (obrigatória para endpoints de domínio):

- Header: `x-holding-user-id`
- Usuários da Holding (6): `HLD-001`, `HLD-002`, `HLD-003`, `HLD-004`, `HLD-005`, `HLD-006`

Estrutura Escolar:

- GET /school/fundamental
- GET /school/high-school
- GET /school/technical
- POST /school/enroll

Gamificação:

- POST /academy/gamification/start
- POST /academy/gamification/visit
- GET /academy/gamification/ranking

Laboratório:

- POST /academy/lab/simulate
- POST /academy/lab/material-test
- GET /academy/lab/results

John Educacional:

- POST /john/academy/recommend
- POST /john/academy/evaluate
- POST /john/academy/career-path
- POST /john/academy/learning-plan

SDK de Trilhas de Certificação:

- GET /sdk/certification/tracks
- POST /sdk/certification/tracks
- GET /sdk/certification/courses

Eventos P&D.IA (novas tecnologias):

- GET /pd-ia/events/new-technologies
- POST /pd-ia/events/new-technologies

RBAC da Holding:

- GET /holding/rbac/users

### Exemplo rápido

Consulta de recomendação por idade:

curl -X POST http://localhost:3000/john/academy/recommend \
	-H "x-holding-user-id: HLD-004" \
  -H "Content-Type: application/json" \
  -d '{"age": 16}'

Consumir evento de nova tecnologia e gerar curso automaticamente:

curl -X POST http://localhost:3000/pd-ia/events/new-technologies \
	-H "x-holding-user-id: HLD-003" \
	-H "Content-Type: application/json" \
	-d '{"title":"BIM 6D com IA generativa","domain":"BIM","level":"avancado","workloadHours":40,"skillTags":["bim","ia","planejamento"]}'

## Roadmap de Implementação (GitHub Issues)

As 35 frentes do projeto foram registradas em issues rastreáveis:

### Resumo Executivo por Bloco

<!-- ROADMAP_STATUS_TABLE:BEGIN -->
| Bloco | Tema | Quantidade de Issues | Status |
|-------|------|----------------------|--------|
| Bloco 1 | Foundation | 4 | Aberto |
| Bloco 2 | John Training Engine | 3 | Aberto |
| Bloco 3 | Treinamento Operacional | 3 | Aberto |
| Bloco 4 | HubBackoffice (RH + DP) | 3 | Aberto |
| Bloco 5 | JuridicoTech | 2 | Aberto |
| Bloco 6 | Metrics | 2 | Aberto |
| Bloco 7 | EdTech Externo | 3 | Aberto |
| Bloco 8 | NATS | 3 | Aberto |
| Bloco 9 | CEFEIDA | 2 | Aberto |
| Bloco 10 | Trading Desk | 2 | Aberto |
| Bloco 11 | RBAC | 2 | Aberto |
| Bloco 12 | Core_DNA + John | 2 | Aberto |
| Bloco 13 | Kanban Global | 2 | Aberto |
| Bloco 14 | Infra / Deploy | 2 | Aberto |
| **Total** |  | **35** | **35 abertas / 0 fechadas** |
<!-- ROADMAP_STATUS_TABLE:END -->

- [ISSUE 1 - Criar domínio educacional (core academy)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/2)
- [ISSUE 2 - Criar schema SQL enterprise](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/3)
- [ISSUE 3 - Criar estrutura de trilhas (tracks) por monólito](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/4)
- [ISSUE 4 - Criar trilha CORE LICEU obrigatória (transversal)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/5)
- [ISSUE 5 - Integrar John ao aprendizado (John Training Engine)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/6)
- [ISSUE 6 - Criar cognitive_profile — score cognitivo do usuário](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/7)
- [ISSUE 7 - Aprendizado baseado em erro (loss intelligence)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/8)
- [ISSUE 8 - Criar Simulation Engine (treino real em sandbox)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/9)
- [ISSUE 9 - Replay de operações reais](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/10)
- [ISSUE 10 - Certificação automática por performance](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/11)
- [ISSUE 11 - Onboarding automático via HubBackoffice (RH + DP)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/12)
- [ISSUE 12 - Treinamento obrigatório por função (role-based training)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/13)
- [ISSUE 13 - Suporte a CLT + PJ — trilhas por tipo de contrato](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/14)
- [ISSUE 14 - Compliance educacional obrigatório (JuridicoTech)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/15)
- [ISSUE 15 - Integração de validação jurídica — evento juridico.validate_training](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/16)
- [ISSUE 16 - Dashboard educacional — KPIs e métricas](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/17)
- [ISSUE 17 - Correlação treinamento x performance real](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/18)
- [ISSUE 18 - Academia como produto SaaS (camada externa EdTech)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/19)
- [ISSUE 19 - Marketplace de cursos — especialistas e monólitos](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/20)
- [ISSUE 20 - White-label corporativo](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/21)
- [ISSUE 21 - Criar stream ACADEMY no NATS JetStream](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/22)
- [ISSUE 22 - Definir e documentar eventos padrão da Academia](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/23)
- [ISSUE 23 - Integrar eventos Academy com ecossistema](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/24)
- [ISSUE 24 - IA de aprendizado — análise comportamental (CEFEIDA)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/25)
- [ISSUE 25 - Geração de conteúdo dinâmico e adaptativo (CEFEIDA)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/26)
- [ISSUE 26 - Tela institucional — Trading Desk educacional](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/27)
- [ISSUE 27 - Ranking gamificado — XP, nível e performance](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/28)
- [ISSUE 28 - Criar papéis educacionais (RBAC da Academia)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/29)
- [ISSUE 29 - Permissão de trilha por monólito (RBAC por domínio)](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/30)
- [ISSUE 30 - Alimentar Core_DNA — aprendizado do John](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/31)
- [ISSUE 31 - John como professor — geração de aulas e dúvidas](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/32)
- [ISSUE 32 - Kanban Global → task gera treinamento automático](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/33)
- [ISSUE 33 - Feedback loop — erro → aprendizado → melhoria → execução](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/34)
- [ISSUE 34 - Docker stack — full stack da Academia](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/35)
- [ISSUE 35 - Deploy em produção — CI/CD, monitoramento e logs](https://github.com/laverssiera/LICEU-ACADEMIA-DO-SABER-/issues/36)


