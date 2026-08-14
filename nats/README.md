# NATS

Configuracoes e scripts de inicializacao do NATS JetStream para o ecossistema LICEU.

## Visao Geral

Diretorio operacional de mensageria para inicializacao e administracao basica do NATS JetStream.

## Arquivos

- nats.conf: configuracao do servidor (portas e JetStream)
- init-streams.sh: cria streams e consumers padrao

## Portas

- 4222: conexoes cliente NATS
- 8222: endpoint HTTP de monitoramento

## Inicializacao de streams

```bash
sh nats/init-streams.sh
```

Com URL customizada:

```bash
sh nats/init-streams.sh nats://localhost:4222
```

## Requisito

O script init-streams.sh depende do CLI nats instalado no ambiente.
