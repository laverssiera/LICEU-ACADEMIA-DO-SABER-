# Apps - Catalogo de Servicos

Indice rapido dos aplicativos do monorepo com stack, porta e status no Docker Compose.

## Visao Geral

Este arquivo funciona como catalogo central dos apps da plataforma, facilitando onboarding tecnico e navegacao entre servicos.

## Estrutura

| App | Stack | Porta local | Publicado no compose | Observacoes |
|---|---|---:|---|---|
| admin | Node.js + Express | 8160 | Sim | Painel administrativo |
| ai-engine | Node.js + Express | 8140 | Sim | Recomendacao e IA adaptativa |
| ai-learning-engine | Python + FastAPI | 8110 | Sim | Conteudo adaptativo |
| api-node | Node.js + Express | 3000 | Nao | API Node auxiliar |
| api-python | Python + FastAPI | 8010 | Nao | API Python por rotas de dominio |
| backend | Node.js + TypeScript + Fastify | 3000 | Sim | API principal enterprise |
| frontend | Next.js 15 + React 19 | 3000 | Sim (8080->3000) | Frontend principal |
| frontend-web | React + Vite | 5173 | Nao | Frontend alternativo |
| game-engine | Node.js | n/a | Nao | Placeholder |
| holographic-engine | Node.js + Express | 8120 | Sim | Renderizacao XR |
| mobile | Node.js + Express | 8090 | Sim | Gateway mobile |
| realtime | Node.js + Express | 8150 | Sim | Distribuicao realtime |
| simulation-engine | Python + FastAPI | 8100 | Sim | Simulacoes tecnicas |
| streaming-engine | Node.js + Express | 8130 | Sim | Streaming de eventos |

## Execucao local

Comandos mais usados no workspace:

- npm run dev:workspace
- npm run test:workspace
- npm run up
- npm run logs
- npm run down

## Scripts

Na maioria dos apps, os scripts seguem:

- npm run dev
- npm run build
- npm run test
- npm run lint

Para apps Python, o script npm run dev depende de ambiente virtual .venv com requirements instalados.

## Variaveis de ambiente

Cada app define suas variaveis de ambiente no proprio contexto de execucao. Consulte o README especifico do servico em apps/<nome-do-app>/README.md.
