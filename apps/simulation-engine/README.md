# Simulation Engine

Engine FastAPI para execucao de simulacoes tecnicas e cenarios praticos.

## Visao Geral

Este README descreve o contexto, a execucao e a operacao deste modulo no ecossistema LICEU.

## Stack

- Python
- FastAPI
- Uvicorn

## Porta

- Local: 8100
- Docker Compose: 8100

## Execucao local

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
npm run dev
```

## Scripts

- `npm run dev`: inicia uvicorn em modo reload
- `npm run build`: validacao de sintaxe Python
- `npm run test`: pytest
- `npm run lint`: ruff check

## Exemplos de endpoint

```bash
curl -X POST http://localhost:8100/simulate/structural
```

## Variaveis de ambiente

Este servico nao possui variaveis obrigatorias documentadas no codigo atual.
