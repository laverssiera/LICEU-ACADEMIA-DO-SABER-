# Backend Contracts

Contratos JSON Schema gerados automaticamente a partir dos schemas Zod do backend.

## Visao Geral

Este diretorio publica contratos para consumo por clientes e integracoes internas.

## Arquivos


## Como atualizar

1. Entre em apps/backend
2. Rode npm run contracts:generate
3. Commit dos artefatos gerados em apps/backend/contracts e docs/contracts

## Validacao local


Este comando regenera os contratos e falha se os arquivos versionados estiverem desatualizados.

## Objetivo

Garantir sincronizacao de contratos de API entre implementacao backend e consumidores internos.
