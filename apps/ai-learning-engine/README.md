# AI Learning Engine

Engine FastAPI para recomendacao de conteudo adaptativo de aprendizagem.

## Visao Geral

Este README descreve o contexto, a execucao e a operacao deste modulo no ecossistema LICEU.

## Stack

- Python
- FastAPI
- Uvicorn

## Porta

- Local: 8110
- Docker Compose: 8110

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
curl -X POST http://localhost:8110/adaptive-learning
```

## Variaveis de ambiente

Este servico nao possui variaveis obrigatorias documentadas no codigo atual.
