# JusExplica — Contrato de API

**Versão:** 1.0  
**Status:** Proposta inicial  
**Data:** 26 de outubro de 2026

## 1. Objetivo

Este documento define o contrato de comunicação entre o backend Laravel e o serviço Python (Explanation Service).

O contrato estabelece:

- Os endpoints internos disponíveis.
- Os formatos das requisições.
- Os formatos das respostas.
- As regras de validação.
- O tratamento de erros.
- As responsabilidades de cada serviço.

O objetivo é permitir que o backend e o serviço Python sejam desenvolvidos e testados independentemente.

## 2. Comunicação

A comunicação entre o Laravel e o Explanation Service ocorrerá por HTTP, utilizando JSON.

Durante o desenvolvimento local, o serviço Python utilizará como endereço inicial:

`http://127.0.0.1:8001`

Esse endereço é válido quando ambos os serviços conseguem acessar a mesma interface de rede local. Se forem executados em contêineres separados, o endereço deverá ser adaptado à rede configurada.

A URL deverá ser configurável por variável de ambiente no Laravel, evitando que endereços locais sejam fixados no código da aplicação.

Exemplo de configuração no Laravel:

```dotenv
EXPLANATION_SERVICE_URL=http://127.0.0.1:8001
EXPLANATION_SERVICE_TIMEOUT=15
```

Os valores são iniciais e poderão ser ajustados conforme os testes de desempenho.

## 3. Convenções gerais

### 3.1. Formato

As requisições e respostas utilizarão JSON.

As requisições com corpo deverão utilizar:

`Content-Type: application/json`

As respostas JSON deverão utilizar:

`application/json`

### 3.2. Datas

As datas de movimentações serão representadas no formato:

`YYYY-MM-DD`

Exemplo:

`2026-10-26`

Quando for necessário representar data e hora, deverá ser utilizado um formato ISO 8601 com fuso horário explícito.

### 3.3. Identificadores

Os identificadores das movimentações deverão preservar o formato fornecido pela fonte processual.

Não se deverá presumir que todos os tribunais utilizam os mesmos códigos para representar eventos processuais.

### 3.4. Idioma

O idioma inicial das explicações será o português brasileiro:

`pt-BR`

Outros idiomas poderão ser adicionados futuramente.

## 4. Endpoints

A primeira versão do contrato prevê dois endpoints.

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/health` | Verificar a disponibilidade básica do serviço. |
| POST | `/v1/explanations` | Solicitar a interpretação de uma movimentação judicial. |

O endpoint de verificação não deverá retornar informações sensíveis sobre o ambiente.

O endpoint de interpretação deverá validar a entrada e produzir uma resposta estruturada.

## 5. Verificação de disponibilidade

### Requisição

```http
GET /health
```

### Resposta de sucesso

**Status HTTP:** `200 OK`

```json
{
  "success": true,
  "service": "explanation-service",
  "status": "online"
}
```

Esse endpoint verifica se a aplicação está respondendo.

Ele não garante, por si só, que todas as dependências externas ou todos os mecanismos de interpretação estejam disponíveis.

## 6. Solicitação de interpretação

### Endpoint

```http
POST /v1/explanations
```

### Objetivo

Receber uma movimentação judicial e retornar uma explicação em linguagem simples.

O Laravel será responsável por obter e validar a movimentação antes de encaminhá-la ao Python.

### 6.1. Exemplo de requisição

```json
{
  "movement": {
    "code": "CODIGO_DA_MOVIMENTACAO",
    "description": "Descrição original da movimentação processual",
    "date": "2026-10-26"
  },
  "language": "pt-BR"
}
```

O código e a descrição apresentados são exemplos ilustrativos. Não representam um código oficial nem uma movimentação judicial específica.

### 6.2. Campos da requisição

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `movement` | objeto | Sim | Dados da movimentação a ser interpretada. |
| `movement.code` | string ou `null` | Não | Código original da movimentação, quando disponível. |
| `movement.description` | string | Sim | Descrição original da movimentação. |
| `movement.date` | string ou `null` | Não | Data da movimentação no formato `YYYY-MM-DD`. |
| `language` | string | Sim | Idioma desejado para a explicação. |

A descrição deverá conter informações suficientes para tentar interpretar a movimentação.

O código poderá ser utilizado para identificar um mapeamento conhecido, mas não deverá ser considerado universal entre tribunais.

O número do processo, o nome das partes, documentos pessoais e outras informações identificáveis não deverão ser enviados ao Python quando não forem necessários para a interpretação.

### 6.3. Resposta de sucesso

**Status HTTP:** `200 OK`

```json
{
  "success": true,
  "data": {
    "explanation": "Explicação em linguagem simples da movimentação judicial.",
    "limitations": []
  }
}
```

### 6.4. Campos da resposta

| Campo | Tipo | Descrição |
|---|---|---|
| `success` | boolean | Indica se a solicitação foi processada com sucesso. |
| `data` | objeto | Contém o resultado da interpretação. |
| `data.explanation` | string | Explicação em linguagem simples. |
| `data.limitations` | array de strings | Limitações relevantes para a interpretação. |

O serviço deverá informar limitações quando os dados disponíveis não permitirem uma explicação suficientemente confiável.

Uma resposta bem-sucedida significa que o serviço processou a solicitação. Não significa que a movimentação contenha todas as informações necessárias para compreender o processo ou determinar as consequências jurídicas de um ato.

## 7. Movimentações desconhecidas ou insuficientes

Nem todas as movimentações poderão ser interpretadas com segurança.

Quando o serviço não reconhecer uma movimentação ou não tiver informações suficientes, deverá evitar conclusões não sustentadas pelos dados recebidos.

### Exemplo de resposta

**Status HTTP:** `200 OK`

```json
{
  "success": true,
  "data": {
    "explanation": "Não foi possível determinar com segurança o significado desta movimentação apenas com as informações disponíveis.",
    "limitations": [
      "A descrição recebida não contém informações suficientes para uma interpretação confiável."
    ]
  }
}
```

Nesse caso, a requisição foi processada corretamente, embora a interpretação seja limitada.

O serviço não deverá inventar prazos, obrigações, decisões ou consequências processuais para preencher lacunas.

## 8. Tratamento de erros

Os erros deverão utilizar códigos HTTP apropriados e uma estrutura JSON consistente.

### 8.1. Dados inválidos

**Status HTTP:** `422 Unprocessable Entity`

Exemplo:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Os dados enviados são inválidos.",
    "details": []
  }
}
```

O campo `details` poderá conter informações sobre os campos inválidos, sem incluir dados pessoais desnecessários.

### 8.2. Erro interno

**Status HTTP:** `500 Internal Server Error`

```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Não foi possível processar a solicitação."
  }
}
```

A resposta pública não deverá expor rastreamentos de execução, caminhos locais, credenciais ou detalhes internos da aplicação.

Os detalhes técnicos deverão ser registrados em logs protegidos, respeitando a política de privacidade.

### 8.3. Serviço indisponível

Quando o Laravel não conseguir acessar o Python, deverá tratar a falha de comunicação e devolver uma resposta controlada ao cliente.

A API pública do Laravel não deverá reproduzir diretamente detalhes técnicos da falha interna.

## 9. Responsabilidades de cada serviço

### 9.1. Laravel

O Laravel deverá:

- Receber as mensagens do cidadão.
- Gerenciar o contexto da conversa.
- Obter as informações processuais necessárias por fontes autorizadas.
- Validar os dados antes de encaminhá-los ao Python.
- Fazer a requisição HTTP ao serviço de interpretação.
- Controlar o tempo limite da requisição.
- Validar o formato da resposta.
- Tratar falhas de comunicação.
- Entregar a resposta ao frontend.

### 9.2. Python

O Explanation Service deverá:

- Receber a requisição interna.
- Validar os dados de entrada.
- Interpretar a movimentação com base nas informações disponíveis.
- Identificar quando não há informações suficientes.
- Produzir uma explicação estruturada.
- Retornar limitações relevantes.
- Respeitar o formato de resposta definido neste contrato.

O Python não deverá assumir a responsabilidade pelo gerenciamento de usuários, conversas ou permissões de acesso aos processos.

## 10. Segurança da comunicação

Como o endpoint de interpretação será interno, ele não deverá ser disponibilizado publicamente sem controles apropriados.

Antes de utilizar o sistema em produção, deverão ser definidos:

- O mecanismo de autenticação entre Laravel e Python.
- As restrições de rede para acesso ao serviço.
- A proteção das credenciais.
- Os limites de tamanho das requisições.
- A validação dos dados recebidos.
- Os limites de tempo e os mecanismos de tratamento de falhas.

A comunicação entre serviços deverá utilizar HTTPS quando atravessar redes não confiáveis.

O serviço Python não deverá aceitar requisições de origem desconhecida apenas porque conhece o formato do contrato.

## 11. Testes de contrato

A implementação deverá incluir testes para verificar:

- O funcionamento do endpoint `/health`.
- A aceitação de uma requisição válida.
- A rejeição de dados inválidos.
- A interpretação de movimentações conhecidas.
- O tratamento de movimentações desconhecidas.
- A presença dos campos obrigatórios na resposta.
- O comportamento em caso de erro interno.
- A compatibilidade entre a requisição do Laravel e o schema do Python.

Os testes deverão utilizar dados fictícios ou devidamente anonimizados.

## 12. Evolução do contrato

Este contrato representa a primeira versão proposta da comunicação interna.

Alterações futuras poderão incluir:

- Identificação da origem da movimentação.
- Referência à versão de um catálogo de códigos processuais.
- Metadados sobre o método de interpretação utilizado.
- Indicadores de revisão ou validação.
- Suporte a mais idiomas.
- Informações adicionais necessárias para produzir explicações mais contextualizadas.

Qualquer alteração deverá manter a compatibilidade entre o Laravel e o Python ou ser acompanhada de uma estratégia de versionamento.

O contrato deverá ser atualizado antes de implementar mudanças incompatíveis.

## 13. Pendências

Antes de considerar este contrato definitivo, será necessário:

1. Definir as primeiras categorias de movimentações que serão suportadas.
2. Determinar quais campos são realmente necessários para interpretar cada categoria.
3. Escolher a estratégia de autenticação entre Laravel e Python.
4. Definir os limites de tamanho das requisições e os tempos de resposta.
5. Validar o contrato por meio de testes automatizados.
6. Confirmar a fonte de dados processuais e suas características.
