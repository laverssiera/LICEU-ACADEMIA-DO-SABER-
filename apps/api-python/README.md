# API Python

API FastAPI para dominio de IA aplicada, simulacoes, holografia e recursos cognitivos.

## Visao Geral

Este README descreve o contexto, a execucao e a operacao deste modulo no ecossistema LICEU.

## Stack

- Python
- FastAPI
- Uvicorn

## Porta

- Local: 8010
- Docker Compose: nao publicado atualmente

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

Health check:

```bash
curl http://localhost:8010/
```

Aula ao vivo com John AI:

```bash
curl -X POST http://localhost:8010/john/academy/live-teaching \
	-H "Content-Type: application/json" \
	-d '{
		"student_id": "STD-001",
		"topic": "estruturas metalicas",
		"mode": "immersive"
	}'
```

Inicializacao de simulacao (sem payload de entrada):

```bash
curl -X POST http://localhost:8010/simulations/start
```

Inicializacao de holografia (sem payload de entrada):

```bash
curl -X POST http://localhost:8010/holography/start
```

## Variaveis de ambiente

Este servico nao possui variaveis obrigatorias documentadas no codigo atual.
