# Backend

API principal enterprise da plataforma LICEU com Fastify, Prisma, JWT e integracoes de eventos.

## Visao Geral

Este README descreve o contexto, a execucao e a operacao deste modulo no ecossistema LICEU.

## Stack

- Node.js
- TypeScript
- Fastify
- Prisma
- PostgreSQL
- Redis
- NATS

## Porta

- Local: 3000
- Docker Compose: 3000

## Execucao local

```bash
npm install
npm run dev
```

## Scripts

- `npm run dev`: servidor TypeScript com watch
- `npm run build`: compilacao TypeScript
- `npm run start`: execucao de dist/server.js
- `npm run test`: testes TypeScript
- `npm run lint`: type-check sem emit
- `npm run contracts:generate`: gera contratos backend
- `npm run contracts:check`: valida contratos versionados

## Exemplos de endpoint

Cadastro de usuario:

```bash
curl -X POST http://localhost:3000/auth/register \
	-H "Content-Type: application/json" \
	-d '{"email":"aluno@liceu.com","password":"12345678"}'
```

Matricula em curso:

```bash
curl -X POST http://localhost:3000/academy/enroll \
	-H "Content-Type: application/json" \
	-d '{"course_id":"CRS-001"}'
```

## Variaveis de ambiente

- `JWT_SECRET` (opcional): segredo usado para assinatura de JWT
- Valor padrao no codigo quando ausente: `liceu`
- `NATS_EVENTS_ENABLED` (opcional): habilita emissao de eventos NATS quando igual a `1`
- `NATS_URL` (opcional): URL do broker NATS (padrao: `nats://localhost:4222`)

## Eventos NATS

Os endpoints de ciencia, interplanetario, learning, simulation e holographic publicam eventos de forma best-effort.

- Se `NATS_EVENTS_ENABLED=1`, a API tenta publicar no NATS.
- Se `NATS_EVENTS_ENABLED` nao estiver definido, a API nao publica eventos.
- Falhas de publicacao nao interrompem a resposta HTTP do endpoint.
