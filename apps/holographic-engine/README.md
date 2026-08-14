# Holographic Engine

Engine de renderizacao holografica/XR para experiencias imersivas.

## Visao Geral

Este README descreve o contexto, a execucao e a operacao deste modulo no ecossistema LICEU.

## Stack

- Node.js
- Express

## Porta

- Local: 8120
- Docker Compose: 8120

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

```bash
curl -X POST http://localhost:8120/holography/render
```

## Variaveis de ambiente

Este servico nao possui variaveis obrigatorias documentadas no codigo atual.
