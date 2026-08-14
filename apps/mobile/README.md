# Mobile Gateway

Gateway HTTP de suporte para integracoes e funcionalidades mobile.

## Visao Geral

Este README descreve o contexto, a execucao e a operacao deste modulo no ecossistema LICEU.

## Stack

- Node.js
- Express

## Porta

- Local: 8090
- Docker Compose: 8090

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
- `npm run lint`: lint em gateway.js

## Exemplos de endpoint

```bash
curl http://localhost:8090/
```

## Variaveis de ambiente

Este servico nao possui variaveis obrigatorias documentadas no codigo atual.
