# JusExplica — Requisitos do Sistema

**Versão:** 1.0  
**Status:** Proposta inicial  
**Data:** 26 de outubro de 2026

## 1. Objetivo

Definir os requisitos funcionais e não funcionais do JusExplica, estabelecendo as funcionalidades necessárias para a primeira versão e orientando o desenvolvimento das próximas etapas.

## 2. Escopo da primeira versão

A primeira versão terá como objetivo permitir que o cidadão envie uma movimentação judicial e receba uma explicação em linguagem simples por meio de uma interface de conversa na web.

Inicialmente, a aplicação poderá utilizar movimentações previamente fornecidas, sem depender de uma integração real com sistemas processuais.

A consulta automatizada de processos, o atendimento pelo WhatsApp e a utilização de inteligência artificial generativa serão avaliados para etapas posteriores.

## 3. Requisitos funcionais

### RF01 — Página inicial

O sistema deverá apresentar o JusExplica, explicando sua finalidade e orientando o cidadão sobre como utilizar o serviço.

### RF02 — Iniciar conversa

O sistema deverá permitir que o cidadão inicie uma nova conversa pela interface web.

### RF03 — Enviar mensagem

O sistema deverá permitir que o cidadão envie mensagens relacionadas à compreensão de informações processuais.

### RF04 — Receber explicações

O sistema deverá apresentar explicações em linguagem simples a partir de movimentações judiciais fornecidas ao serviço.

### RF05 — Tratar informações insuficientes

O sistema deverá informar quando os dados disponíveis forem insuficientes para produzir uma explicação confiável.

### RF06 — Exibir mensagens de erro

O sistema deverá apresentar mensagens compreensíveis quando ocorrerem falhas no processamento de uma solicitação.

### RF07 — Consultar informações institucionais

O sistema deverá disponibilizar uma página com informações sobre o projeto e seu funcionamento.

### RF08 — Consultar informações de privacidade

O sistema deverá disponibilizar uma página com informações sobre o tratamento de dados e a privacidade dos usuários.

## 4. Requisitos funcionais futuros

Os requisitos abaixo não fazem parte obrigatoriamente da primeira versão.

### RF09 — Histórico de conversas

O sistema poderá permitir a consulta de conversas anteriores, respeitando os controles de acesso e a política de retenção de dados.

### RF10 — Consulta de processos

O sistema poderá consultar movimentações processuais por meio de fontes oficiais ou autorizadas, conforme a disponibilidade técnica e as condições de acesso aplicáveis.

### RF11 — Atendimento pelo WhatsApp

O sistema poderá receber mensagens pelo WhatsApp e encaminhá-las ao mesmo fluxo de atendimento utilizado pela interface web.

### RF12 — Respostas em áudio

O sistema poderá disponibilizar versões em áudio das explicações, mediante avaliação das tecnologias e dos requisitos de acessibilidade.

### RF13 — Inteligência artificial

O sistema poderá utilizar modelos de inteligência artificial para auxiliar na interpretação e simplificação das movimentações, desde que existam mecanismos adequados de validação e controle das respostas.

### RF14 — Autenticação

O sistema poderá oferecer contas de usuário caso sejam necessárias para gerenciar histórico, preferências ou funcionalidades que exijam identificação.

## 5. Requisitos não funcionais

### RNF01 — Segurança

O sistema deverá validar as entradas, proteger credenciais e impedir acesso não autorizado às informações.

### RNF02 — Privacidade

O sistema deverá minimizar a coleta e a retenção de dados pessoais e processuais.

### RNF03 — Confiabilidade

O sistema não deverá inventar informações processuais, prazos, obrigações ou consequências jurídicas.

### RNF04 — Tratamento de falhas

O sistema deverá tratar falhas de comunicação entre o frontend, o backend e o serviço Python sem expor detalhes técnicos desnecessários ao usuário.

### RNF05 — Manutenibilidade

O código deverá ser organizado em componentes e módulos com responsabilidades bem definidas.

### RNF06 — Testabilidade

As funcionalidades deverão ser desenvolvidas de forma que possam ser verificadas por testes automatizados.

### RNF07 — Usabilidade

A interface deverá utilizar linguagem clara, navegação compreensível e mensagens adequadas ao público geral.

### RNF08 — Acessibilidade

A interface deverá considerar recursos de acessibilidade, incluindo navegação por teclado, contraste adequado e identificação acessível dos elementos interativos.

### RNF09 — Desempenho

O sistema deverá estabelecer limites de tempo para requisições e tratar operações demoradas sem deixar o usuário sem retorno.

Os limites quantitativos de desempenho serão definidos após os primeiros testes.

### RNF10 — Interoperabilidade

A comunicação entre os serviços deverá utilizar contratos documentados e formatos de dados padronizados.

## 6. Critérios de aceitação da primeira versão

A primeira versão será considerada funcional quando:

1. O cidadão conseguir acessar a página inicial.
2. O cidadão conseguir iniciar uma conversa.
3. O sistema conseguir receber uma movimentação judicial previamente fornecida.
4. O backend conseguir encaminhar os dados ao serviço Python.
5. O serviço Python conseguir devolver uma explicação estruturada.
6. O backend conseguir devolver a resposta à interface web.
7. A interface conseguir apresentar a explicação ao cidadão.
8. O sistema informar quando não houver dados suficientes para uma interpretação confiável.
9. Erros de comunicação forem tratados sem expor detalhes internos.
10. Os principais fluxos estiverem cobertos por testes.

## 7. Restrições e premissas

- A primeira versão não dependerá obrigatoriamente de acesso automatizado ao eproc.
- A consulta de processos reais dependerá da identificação de uma fonte apropriada e das condições de acesso aplicáveis.
- O número do processo não será considerado, isoladamente, prova de autorização para acessar informações restritas.
- As explicações terão finalidade informativa e não substituirão orientação jurídica individualizada.
- A utilização de inteligência artificial generativa dependerá de uma avaliação posterior.
- As funcionalidades futuras somente serão implementadas após a definição dos respectivos requisitos.

## 8. Pendências

Antes de ampliar o escopo, deverão ser definidas:

- A estratégia de identificação e gerenciamento das conversas.
- A necessidade de autenticação na primeira versão.
- A política de armazenamento e exclusão de mensagens.
- As categorias de movimentações suportadas inicialmente.
- A fonte de dados processuais.
- Os critérios de avaliação da qualidade das explicações.
- Os requisitos de integração com o WhatsApp.
- A estratégia para geração de áudio.