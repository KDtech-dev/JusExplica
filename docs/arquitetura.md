# JusExplica — Arquitetura do Sistema

**Versão:** 1.0  
**Status:** Proposta inicial  
**Data:** 26 de outubro de 2026

## 1. Visão geral

O JusExplica é um sistema que tem como objetivo tornar informações processuais judiciais mais compreensíveis para os cidadãos, traduzindo movimentações e termos jurídicos para uma linguagem simples e acessível.

A aplicação será desenvolvida com uma arquitetura composta por três componentes principais:

- **Frontend:** interface de interação com o cidadão.
- **Backend:** responsável pela lógica central da aplicação, gerenciamento das conversas e coordenação das integrações.
- **Explanation Service:** serviço Python responsável por interpretar movimentações judiciais e produzir explicações em linguagem simples.

Futuramente, o sistema poderá oferecer atendimento por meio do WhatsApp, reutilizando as funcionalidades disponibilizadas pelo backend.

## 2. Objetivos arquiteturais

A arquitetura deverá:

- Separar as responsabilidades de interface, gerenciamento da aplicação e interpretação textual.
- Permitir que cada componente seja desenvolvido e testado independentemente.
- Facilitar a manutenção e a evolução do sistema.
- Padronizar a comunicação entre os serviços.
- Evitar que o frontend tenha acesso direto a serviços internos.
- Proteger os dados processuais e as informações dos usuários.
- Reduzir o risco de apresentar explicações jurídicas incorretas ou não sustentadas pelos dados disponíveis.

## 3. Tecnologias

### 3.1. Frontend

**Tecnologias:** Next.js, React e TypeScript.

Responsabilidades:

- Apresentar a interface do JusExplica.
- Permitir o envio de mensagens.
- Exibir respostas e movimentações explicadas.
- Apresentar o histórico das conversas conforme as permissões de acesso.
- Disponibilizar as páginas institucionais e de privacidade.
- Comunicar-se com o backend por meio de uma API HTTP.

O frontend não deverá acessar diretamente o banco de dados nem o serviço Python.

### 3.2. Backend

**Tecnologia:** Laravel com PHP.

O backend será o núcleo da aplicação e o ponto central de comunicação entre os componentes.

Responsabilidades:

- Disponibilizar a API pública consumida pelo frontend.
- Gerenciar conversas e mensagens.
- Validar as requisições recebidas.
- Controlar o acesso às informações.
- Coordenar a consulta de dados processuais em fontes autorizadas.
- Encaminhar movimentações ao serviço Python.
- Validar as respostas recebidas do serviço Python.
- Devolver os resultados ao frontend.
- Receber futuramente as notificações e mensagens provenientes do WhatsApp.

O backend deverá evitar o armazenamento desnecessário de dados pessoais e processuais.

### 3.3. Explanation Service

**Tecnologia:** Python com FastAPI.

O Explanation Service será responsável pela interpretação das movimentações judiciais.

Responsabilidades:

- Receber movimentações processuais estruturadas.
- Validar os dados de entrada.
- Identificar significados com base em regras e referências confiáveis.
- Transformar descrições técnicas em explicações compreensíveis.
- Informar limitações quando não houver dados suficientes para uma interpretação confiável.
- Retornar respostas estruturadas ao backend.
- Disponibilizar mecanismos de verificação da saúde do serviço.

Inicialmente, a interpretação deverá priorizar regras determinísticas e mapeamentos de movimentações conhecidas. O uso de modelos de inteligência artificial poderá ser avaliado posteriormente.

O serviço não deverá inventar informações sobre decisões, obrigações, prazos ou consequências jurídicas.

### 3.4. Banco de dados

**Tecnologia inicial:** MySQL.

O banco de dados principal será gerenciado pelo backend Laravel.

Poderá armazenar:

- Conversas.
- Mensagens.
- Referências aos processos consultados.
- Metadados necessários ao funcionamento da aplicação.
- Informações de usuários, caso seja adotado um sistema de contas.

A estrutura definitiva será especificada no documento `banco-de-dados.md`.

O serviço Python não deverá acessar diretamente o banco de dados principal. As informações necessárias à interpretação serão recebidas por meio de requisições internas ao serviço.

## 4. Arquitetura de comunicação

A comunicação entre os componentes ocorrerá por meio de requisições HTTP.

O frontend consumirá a API pública do Laravel. O Laravel, por sua vez, poderá chamar a API interna do Explanation Service.

Fluxo principal:

1. O cidadão envia uma mensagem pelo frontend.
2. O frontend encaminha a requisição ao backend.
3. O backend valida a solicitação e identifica o contexto da conversa.
4. Quando necessário, o backend obtém informações processuais por meio de uma fonte autorizada.
5. O backend encaminha a movimentação ao Explanation Service.
6. O serviço Python valida os dados e produz uma explicação.
7. O Python retorna o resultado ao Laravel.
8. O Laravel valida e processa a resposta.
9. O frontend apresenta a explicação ao cidadão.

O backend será responsável por controlar o fluxo da aplicação e decidir quando uma interpretação será necessária.

## 5. Fontes de informações processuais

A obtenção das movimentações processuais dependerá da disponibilidade de fontes autorizadas.

Antes da implementação dessa funcionalidade, deverão ser avaliados:

- A existência de APIs oficiais disponibilizadas pelos tribunais.
- As condições de acesso aos sistemas processuais pertinentes.
- As permissões necessárias para consultar cada tipo de informação.
- As restrições aplicáveis aos processos que tramitam em segredo de justiça.
- Os limites técnicos e jurídicos de cada fonte.

A existência de dados públicos em uma fonte não significa que todas as informações de um processo estejam disponíveis por meio dela.

A integração com o eproc ou com qualquer outra fonte processual será considerada pendente até que o mecanismo de acesso adequado seja identificado e validado.

## 6. Segurança e privacidade

O desenvolvimento deverá observar os princípios de proteção de dados, incluindo a minimização da coleta e do armazenamento.

Requisitos arquiteturais:

- O acesso às informações deverá respeitar as permissões aplicáveis.
- O número de um processo, isoladamente, não deverá ser tratado como prova de autorização para consultar informações restritas.
- Segredos, tokens e credenciais deverão ser armazenados em variáveis de ambiente ou em mecanismos apropriados de gerenciamento de segredos.
- A comunicação entre serviços deverá ser protegida conforme o ambiente de execução.
- As requisições deverão ser validadas antes do processamento.
- Os registros de aplicação não deverão expor desnecessariamente dados pessoais ou conteúdo processual.
- As respostas automatizadas deverão comunicar limitações relevantes.
- O sistema não deverá apresentar suas explicações como substitutas de orientação jurídica individualizada.

Os requisitos detalhados de privacidade, retenção e controle de acesso deverão ser definidos antes da disponibilização do sistema a usuários reais.

## 7. Tratamento de falhas

A aplicação deverá prever falhas nos serviços externos e internos.

Exemplos:

- Serviço Python indisponível.
- Fonte processual inacessível.
- Movimentação sem informações suficientes.
- Dados de entrada inválidos.
- Tempo de resposta excedido.
- Resposta do serviço Python incompatível com o contrato da API.

O backend deverá tratar essas situações e devolver respostas controladas, sem expor detalhes internos, credenciais ou mensagens técnicas desnecessárias ao cidadão.

Quando não for possível produzir uma explicação confiável, o sistema deverá informar a limitação em vez de apresentar uma interpretação especulativa.

## 8. Organização do repositório

O projeto será organizado em um repositório principal:

```text
JusExplica/
├── frontend/
├── backend/
├── explanation-service/
├── docs/
│   ├── arquitetura.md
│   ├── contrato-api.md
│   ├── requisitos.md
│   └── banco-de-dados.md
├── .gitignore
└── README.md
```

Cada componente terá suas próprias dependências e instruções de execução.

A documentação compartilhada deverá permanecer na pasta `docs/`.

## 9. Evolução prevista

A implementação será realizada incrementalmente.

### Fase 1 — Estrutura e contratos

- Documentar a arquitetura.
- Definir os contratos entre os serviços.
- Definir os requisitos funcionais e não funcionais.

### Fase 2 — API e protótipo funcional

- Criar a API inicial do Laravel.
- Criar os primeiros endpoints do Python.
- Implementar respostas simuladas para validar a comunicação.

### Fase 3 — Interpretação de movimentações

- Definir as primeiras movimentações suportadas.
- Implementar regras de interpretação.
- Criar testes para verificar a consistência das explicações.

### Fase 4 — Interface

- Implementar a interface de conversa.
- Integrar o frontend com o backend.
- Tratar estados de carregamento e falhas.

### Fase 5 — Integração processual e canais adicionais

- Validar uma fonte autorizada de informações processuais.
- Implementar a integração correspondente.
- Avaliar a integração com o WhatsApp.
- Revisar segurança, privacidade e confiabilidade.

## 10. Decisões pendentes

As seguintes decisões deverão ser tomadas durante o planejamento:

- Qual fonte oficial ou autorizada será utilizada para consultar movimentações processuais?
- O sistema permitirá utilização anônima ou exigirá autenticação?
- Como serão identificadas e protegidas as conversas dos usuários?
- Qual será a política de retenção e exclusão de mensagens?
- Quais movimentações serão suportadas na primeira versão?
- Será utilizado um modelo de inteligência artificial? Em caso afirmativo, qual será o mecanismo de avaliação e controle das respostas?
- O atendimento por áudio fará parte da primeira versão ou de uma evolução posterior?
- Como será implementada e autorizada a integração com o WhatsApp?

Essas decisões deverão ser documentadas antes da implementação das funcionalidades correspondentes.
