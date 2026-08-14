# Infra

Camada de infraestrutura e operacao do ecossistema LICEU.

## Visao Geral

Reune componentes de deploy, observabilidade, rede e provisionamento.

## Estrutura

- docker: artefatos de execucao local e suporte a containers
- kubernetes: manifests de deploy
- monitoring: stack de observabilidade
- nginx: configuracoes de proxy/reverse proxy
- terraform: infraestrutura como codigo

## Uso rapido

- Ambiente local: priorizar docker compose da raiz
- Deploy orquestrado: usar manifests em kubernetes
- Provisionamento: usar terraform conforme ambiente alvo

## Variaveis de ambiente

As variaveis dependem da estrategia de deploy e do ambiente (local, staging, producao).
