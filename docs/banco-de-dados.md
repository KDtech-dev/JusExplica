# JusExplica — Modelagem do Banco de Dados

**Versão:** 1.0  
**Status:** Proposta inicial  
**SGBD:** MySQL

## 1. Objetivo

Este documento define a proposta inicial de modelagem do banco de dados do JusExplica.

O banco será gerenciado pelo backend Laravel e armazenará os dados necessários para o gerenciamento das conversas e mensagens.

O serviço Python não terá acesso direto ao banco de dados principal. As informações necessárias para interpretar movimentações serão recebidas por meio da API interna.

## 2. Princípios de modelagem

A modelagem deverá seguir os seguintes princípios:

- Armazenar apenas os dados necessários ao funcionamento da aplicação.
- Separar conversas de mensagens.
- Utilizar identificadores únicos para os registros.
- Preservar a integridade dos relacionamentos.
- Evitar o armazenamento desnecessário de dados pessoais e processuais.
- Permitir a evolução futura para autenticação e outros canais de atendimento.
- Definir políticas de retenção e exclusão antes da disponibilização do sistema em produção.

## 3. Entidades principais

A primeira versão deverá considerar as seguintes entidades:

- `conversations`: representa uma conversa iniciada no sistema.
- `messages`: representa as mensagens trocadas durante uma conversa.
- `process_references`: representa referências aos processos relacionados às conversas, quando necessário.

A necessidade de persistir referências processuais será avaliada conforme o fluxo definitivo da aplicação. Caso os dados possam ser utilizados sem armazenamento persistente, essa entidade poderá ser adiada.

## 4. Tabela `conversations`

Representa uma conversa mantida pelo JusExplica.

| Campo | Tipo conceitual | Obrigatório | Descrição |
|---|---|---|---|
| `id` | UUID | Sim | Identificador único da conversa. |
| `channel` | string | Sim | Canal de origem, como `web` ou `whatsapp`. |
| `status` | string | Sim | Estado da conversa. |
| `created_at` | timestamp | Sim | Data e hora de criação. |
| `updated_at` | timestamp | Sim | Data e hora da última atualização. |

### Valores iniciais

`channel` poderá assumir:

- `web`
- `whatsapp`

`status` poderá assumir:

- `active`
- `closed`

Esses valores são propostas iniciais e deverão ser validados durante a implementação.

A tabela não deverá armazenar diretamente informações de autenticação ou credenciais externas.

## 5. Tabela `messages`

Representa uma mensagem enviada pelo cidadão ou produzida pelo sistema.

| Campo | Tipo conceitual | Obrigatório | Descrição |
|---|---|---|---|
| `id` | UUID | Sim | Identificador único da mensagem. |
| `conversation_id` | UUID | Sim | Referência à conversa correspondente. |
| `sender_type` | string | Sim | Origem da mensagem. |
| `content` | text | Sim | Conteúdo textual da mensagem. |
| `created_at` | timestamp | Sim | Data e hora de criação. |

### Valores iniciais

`sender_type` poderá assumir:

- `user`
- `assistant`
- `system`

A relação entre `messages` e `conversations` será de um para muitos: uma conversa poderá conter várias mensagens, e cada mensagem pertencerá a uma única conversa.

O campo `content` deverá conter apenas informações necessárias ao histórico da conversa.

Dados pessoais ou processuais não deverão ser armazenados indiscriminadamente. A política de retenção e exclusão deverá ser definida antes da produção.

## 6. Tabela `process_references`

Representa uma referência a um processo associado a uma conversa.

Sua implementação dependerá da definição do mecanismo de consulta processual e das necessidades reais de persistência.

| Campo | Tipo conceitual | Obrigatório | Descrição |
|---|---|---|---|
| `id` | UUID | Sim | Identificador único da referência. |
| `conversation_id` | UUID | Sim | Referência à conversa associada. |
| `source` | string | Sim | Identificação da fonte dos dados processuais. |
| `external_reference` | string | Não | Referência externa ao processo, quando necessária. |
| `created_at` | timestamp | Sim | Data e hora de criação. |

O campo `external_reference` não deverá ser utilizado para armazenar informações além das necessárias para identificar a referência externa.

O número do processo não deverá ser considerado uma credencial de acesso.

Informações de processos protegidos por restrições de acesso deverão seguir os controles e as permissões aplicáveis.

A tabela não deverá armazenar cópias completas de processos ou documentos judiciais sem uma necessidade justificada e uma avaliação apropriada de segurança e privacidade.

## 7. Relacionamentos

Os relacionamentos previstos são:

- Uma conversa possui várias mensagens.
- Cada mensagem pertence a uma conversa.
- Uma conversa poderá possuir nenhuma, uma ou várias referências processuais.

Representação conceitual:

```text
CONVERSATIONS
    |
    | 1:N
    |
    +---------------- MESSAGES

CONVERSATIONS
    |
    | 1:N
    |
    +---------------- PROCESS_REFERENCES
```

## 8. Identificadores

A proposta inicial utiliza UUIDs como identificadores dos registros.

Essa escolha facilita a geração de identificadores únicos e evita a exposição direta de sequências numéricas simples nas URLs.

A utilização de UUIDs não substitui mecanismos de autenticação e autorização.

## 9. Persistência e privacidade

Antes de implementar a persistência, deverão ser definidos:

- Quais mensagens serão armazenadas.
- Por quanto tempo serão mantidas.
- Como o usuário poderá solicitar sua exclusão.
- Como serão tratadas conversas anônimas.
- Como será impedido o acesso indevido a conversas.
- Quais informações poderão aparecer nos logs.
- Como serão tratados os identificadores de usuários do WhatsApp.

O conteúdo de uma conversa poderá conter dados pessoais ou informações processuais. Por isso, a política de armazenamento deverá considerar a finalidade, a necessidade e os riscos envolvidos.

## 10. Evolução futura

Conforme os requisitos evoluírem, poderão ser consideradas novas entidades:

- `users`: usuários autenticados.
- `conversation_participants`: participantes de uma conversa, caso o modelo exija múltiplos participantes.
- `process_movements`: movimentações processuais armazenadas de forma controlada.
- `message_feedback`: avaliações das respostas fornecidas pelo sistema.

Essas entidades não deverão ser criadas antecipadamente sem uma necessidade funcional definida.

## 11. Decisões pendentes

Antes de criar as migrations do Laravel, será necessário definir:

1. Se a primeira versão permitirá conversas anônimas ou exigirá autenticação.
2. Se as conversas serão armazenadas no banco de dados.
3. Qual será a política de retenção e exclusão das mensagens.
4. Se as referências processuais precisarão ser persistidas.
5. Como será identificado o usuário em cada canal.
6. Se haverá necessidade de relacionar conversas a usuários autenticados futuramente.
7. Quais restrições de acesso serão aplicadas a cada tipo de informação.