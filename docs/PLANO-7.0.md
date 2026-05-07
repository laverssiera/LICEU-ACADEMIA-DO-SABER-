# Plano de Execucao LICEU Academia 7.0

## Objetivo
Transformar a Academia em um sistema operacional cognitivo de aprendizado continuo, com entregas incrementais e validacao de impacto operacional.

## Fase 1 - Fundacao Cognitiva
- Escopo:
  - John Professor 7.0 (live teaching)
  - CORE DNA educacional (modelo e coleta)
  - CEFEIDA adaptativo (analise inicial)
- Entregaveis:
  - Endpoint `POST /john/academy/live-teaching`
  - Estrutura `cognitive_dna` definida
  - Eventos cognitivos publicados no barramento
- Criterios de aceite:
  - Aula imersiva criada com adaptacao de dificuldade
  - Perfil cognitivo persistivel por usuario
  - Telemetria minima no dashboard

## Fase 2 - Simulacao e Laboratorios
- Escopo:
  - Motor de laboratorios virtuais
  - Simulacao de obra, BIM e financeiro
  - Integração com feedback loop
- Entregaveis:
  - Endpoint `POST /academy/labs/start`
  - Catalogo de tipos de laboratorio por dominio
  - Indicadores de conclusao por sessao
- Criterios de aceite:
  - Sessao de laboratorio iniciada em menos de 2s
  - Resultado de aprendizado rastreado por usuario
  - Eventos em NATS para observabilidade

## Fase 3 - Corporate University SaaS
- Escopo:
  - White-label para empresas externas
  - Provisionamento de trilhas e IA pedagogica
  - Integracao comercial com EdTech externo
- Entregaveis:
  - Endpoint `POST /corporate-university/create`
  - Pacote de features por cliente
  - Configuracao de branding e trilhas
- Criterios de aceite:
  - Universidade provisionada com status `provisioned`
  - Ativacao de John/CEFEIDA por tenant
  - Governanca RBAC por tenant e holding

## Fase 4 - Streaming, Mobile e Campus Digital Twin
- Escopo:
  - Live classes com replay e legenda
  - App mobile offline-first
  - Navegacao no campus 3D
- Entregaveis:
  - Pipeline WebRTC + subtitles IA
  - Gateway mobile + notificacoes
  - Protótipo de campus digital twin
- Criterios de aceite:
  - Aula ao vivo com latencia controlada
  - Consumo mobile com sincronizacao posterior
  - Metricas de engajamento por turma

## Fase 5 - Marketplace e Editora GAME MKT
- Escopo:
  - Venda de cursos e mentorias
  - Esteira de conteudo da editora
  - Integracao com economia gamificada
- Entregaveis:
  - Backoffice de publicacao
  - Curadoria com ranking de qualidade
  - API de catalogo e monetizacao
- Criterios de aceite:
  - Especialista publica conteudo com revisão
  - Aluno compra e consome em multiplos formatos
  - Indicadores de receita e retenção ativos

## Fase 6 - Operacao, Talentos e Escala
- Escopo:
  - Integracao plena com HUBBACKOFFICE e RH
  - Sistema de talentos e recomendacao de carreira
  - Escala em Kubernetes e SRE basico
- Entregaveis:
  - Fluxo Academia -> RH com trilhas recomendadas
  - Streams dedicados 7.0 no NATS
  - Deploy segmentado por servico
- Criterios de aceite:
  - Talentos detectados com evidencias de desempenho
  - Provisionamento horizontal dos servicos criticos
  - Painel operacional com SLOs principais

## Matriz de Prioridade
- P0:
  - Live teaching
  - Labs start
  - Corporate University create
  - Modelo cognitive_dna
- P1:
  - Streaming nativo
  - Mobile
  - Marketplace
- P2:
  - Holografia avancada
  - Token educacional
  - Universidade LICEU blockchain

## Riscos Principais
- Complexidade de integracao entre modulos e monolitos.
- Volume de eventos em tempo real sem politicas de retenção e observabilidade.
- Escopo funcional maior que a capacidade de entrega por sprint.

## Mitigacoes
- Contratos de API versionados e testes de contrato.
- Event schema registry e politicas de DLQ.
- Roadmap por epicos com gates de aceite objetivos.
