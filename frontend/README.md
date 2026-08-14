# Frontend (raiz)

Aplicacao web alternativa do monorepo baseada em Vite + React.

## Visao Geral

Este README descreve o contexto, a execucao e a operacao deste modulo no ecossistema LICEU.

## Stack

- React 18
- Vite
- Tailwind CSS (dependencia presente)

## Estrutura

- src/main.jsx: bootstrap da aplicacao
- src/AcademyDesk.jsx: interface principal
- src/index.css: estilos globais
- index.html: entrada HTML
- nginx.conf: configuracao para deploy estatico

## Porta

- Desenvolvimento local: 5173 (padrao Vite)
- Dockerfile: disponivel para containerizacao

## Execucao local

```bash
npm install
npm run dev
```

## Scripts

- npm run dev
- npm run build
- npm run preview

## Variaveis de ambiente

Este frontend nao possui variaveis obrigatorias documentadas no codigo atual.
