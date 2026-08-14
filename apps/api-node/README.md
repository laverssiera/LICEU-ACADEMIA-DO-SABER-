# API Node

Servico Node.js para endpoints HTTP base da plataforma LICEU.

## Visao Geral

Este README descreve o contexto, a execucao e a operacao deste modulo no ecossistema LICEU.

## Stack

- Node.js
- Express

## Porta

- Local: 3000
- Docker Compose: nao publicado atualmente

## Execucao local

```bash
npm install
npm run dev
```

## Scripts

- `npm run dev`: modo desenvolvimento com watch
- `npm run start`: execucao padrao
- `npm run build`: validacao placeholder
- `npm run test`: testes Node
- `npm run lint`: lint em server.js

## Exemplos de endpoint

Health check (sem payload de entrada):

```bash
curl http://localhost:3000/
```

Resposta esperada:

```json
{
	"platform": "LICEU API Node",
	"version": "7.0",
	"status": "running"
}
```

## Variaveis de ambiente

Este servico nao possui variaveis obrigatorias documentadas no codigo atual.
