# Checklist de Qualidade de Documentacao

Use esta lista antes de abrir PR quando houver alteracoes em README, docs de modulo ou guias operacionais.

## Estrutura e clareza

- O arquivo tem secao Visao Geral explicando contexto e escopo.
- As secoes seguem ordem consistente com o padrao do repositorio.
- Os titulos de secao estao objetivos e sem duplicidade.
- O texto evita termos ambiguos e descreve responsabilidades reais do modulo.

## Execucao e operacao

- Comandos de execucao local estao atualizados e testaveis.
- Portas e mapeamentos estao coerentes com docker-compose.yml e codigo.
- Variaveis de ambiente obrigatorias (quando existirem) estao descritas.
- Exemplos de endpoint/payload refletem rotas reais do servico.

## Consistencia entre documentos

- README do dominio aponta para documentos complementares relevantes.
- Nomes de pastas/servicos citados existem no repositorio.
- Informacoes duplicadas entre docs nao estao conflitantes.
- Contratos e referencias de API estao alinhados com artefatos publicados.

## Qualidade editorial

- Conteudo em ASCII para evitar problemas de encoding.
- Ortografia e padrao de termos estao consistentes.
- Frases curtas e diretas, sem excesso de texto promocional.
- Lista e tabelas foram revisadas para facilitar leitura rapida.

## Checklist rapido de merge

- Revisao tecnica concluida.
- Revisao de consistencia concluida.
- Links internos verificados.
- Arquivos novos foram referenciados no README do dominio.
