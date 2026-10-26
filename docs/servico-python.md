# Serviço Python — JusExplica

## 1. Visão geral

O `explanation-service` é um serviço desenvolvido em Python com FastAPI, responsável pelo processamento de movimentações judiciais e pela produção de explicações em linguagem simples.

Seu objetivo é ajudar o cidadão a compreender os registros processuais sem exigir conhecimento prévio de terminologia jurídica.

O serviço faz parte da arquitetura do JusExplica e se comunica com o backend Laravel, que atua como API principal da aplicação.

Nesta primeira versão, as explicações são produzidas por regras determinísticas. A utilização de fontes externas de dados processuais e de mecanismos mais avançados de interpretação ainda depende de implementação futura.

## 2. Responsabilidades

O serviço Python é responsável por:

- Receber e validar os dados de uma movimentação judicial.
- Identificar movimentações reconhecidas pelas regras implementadas.
- Produzir explicações em linguagem simples.
- Informar quando uma movimentação não é reconhecida.
- Expor endpoints HTTP para integração com o backend.
- Verificar a disponibilidade do próprio serviço.
- Garantir, por meio de testes automatizados, o comportamento esperado da aplicação.

O serviço não é responsável por gerenciar usuários, autenticação principal, persistência dos processos ou acesso direto ao banco de dados da aplicação.

Essas responsabilidades permanecem no backend Laravel.

## 3. Estrutura de diretórios

```text
explanation-service/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   └── explanations.py
│   │   └── router.py
│   ├── core/
│   │   └── config.py
│   ├── schemas/
│   │   └── explanation.py
│   ├── services/
│   │   └── explanation_service.py
│   └── main.py
├── tests/
│   └── test_explanations.py
├── .env.example
├── requirements.txt
└── pyproject.toml
```

Os arquivos `__init__.py` são utilizados nos diretórios da aplicação e dos testes para explicitar a organização dos pacotes Python.

### 3.1. `app/main.py`

Ponto de entrada da aplicação FastAPI.

Responsabilidades:

- Criar a instância do FastAPI.
- Definir os metadados da aplicação.
- Registrar o roteador principal.
- Disponibilizar o endpoint raiz.

Não deve concentrar as regras de explicação nem todas as definições de rotas.

### 3.2. `app/api/`

Camada responsável pelos endpoints HTTP.

**`router.py`**

Agrupa os roteadores da aplicação e aplica os prefixos necessários às rotas.

**`routes/health.py`**

Disponibiliza o endpoint de verificação de disponibilidade do serviço.

**`routes/explanations.py`**

Recebe solicitações de explicação, utiliza os schemas para validar os dados e encaminha a movimentação ao serviço responsável pelo processamento.

Essa camada é responsável pela comunicação HTTP, não pela implementação das regras de negócio.

### 3.3. `app/core/`

Camada destinada às configurações compartilhadas da aplicação.

**`config.py`**

Centraliza informações como nome, descrição, versão e prefixo da API.

As configurações podem ser definidas por valores padrão ou variáveis de ambiente.

### 3.4. `app/schemas/`

Define os modelos de entrada e saída utilizando Pydantic.

**`explanation.py`**

Contém os seguintes modelos:

- `MovementInput`: dados da movimentação recebida.
- `ExplanationRequest`: estrutura da solicitação.
- `ExplanationData`: conteúdo da explicação e suas limitações.
- `ExplanationResponse`: estrutura da resposta.

Os schemas verificam os tipos e as restrições dos dados. Eles não determinam, por si só, se uma interpretação jurídica está correta.

### 3.5. `app/services/`

Contém a lógica de processamento da aplicação.

**`explanation_service.py`**

Implementa a função `explain_movement`, responsável por procurar regras correspondentes à descrição recebida e produzir uma explicação ou informar que a movimentação não foi reconhecida.

As regras atuais constituem uma implementação inicial e podem ser ampliadas conforme a evolução do projeto.

### 3.6. `tests/`

Contém os testes automatizados.

**`test_explanations.py`**

Verifica o funcionamento dos endpoints, o processamento de movimentações conhecidas, o comportamento diante de movimentações desconhecidas e a validação dos dados recebidos.

Os testes devem ser executados sempre que houver alterações relevantes no serviço.

## 4. Fluxo de processamento

O processamento de uma solicitação segue estas etapas:

1. O cliente envia uma requisição HTTP ao endpoint de explicações.
2. O FastAPI recebe a requisição.
3. O Pydantic valida os dados de entrada.
4. A rota encaminha a movimentação ao serviço de explicação.
5. O serviço procura uma regra correspondente.
6. O serviço produz uma explicação ou informa que não reconheceu a movimentação.
7. A resposta é estruturada pelo schema de saída.
8. O FastAPI devolve a resposta HTTP ao cliente.

A separação permite modificar as regras de processamento sem concentrar a lógica nos endpoints.

## 5. Endpoints disponíveis

### `GET /`

Verifica se a aplicação está respondendo.

### `GET /health`

Retorna o estado de disponibilidade do serviço.

Exemplo de resposta:

```json
{
  "success": true,
  "service": "explanation-service",
  "status": "online"
}
```

### `POST /v1/explanations`

Solicita uma explicação para uma movimentação judicial.

Exemplo de requisição:

```json
{
  "movement": {
    "code": "123",
    "description": "Conclusos para decisão",
    "date": "2026-10-26"
  },
  "language": "pt-BR"
}
```

O campo `date` é opcional. O campo `language` possui valor padrão `pt-BR`.

Exemplo simplificado de resposta:

```json
{
  "success": true,
  "data": {
    "explanation": "O processo foi encaminhado ao responsável pela análise judicial para apreciação ou decisão. Esse registro, por si só, não informa qual será o resultado.",
    "limitations": [
      "Esta explicação é informativa e considera apenas a descrição da movimentação recebida. Consulte o processo ou um profissional do Direito para confirmar o significado no contexto do caso."
    ]
  }
}
```

A resposta deve informar quando a movimentação não for reconhecida pelas regras disponíveis.

## 6. Configuração e execução

O serviço utiliza um ambiente virtual Python para isolar suas dependências.

Ativação do ambiente:

```bash
cd explanation-service
source .venv/bin/activate
```

Instalação das dependências:

```bash
python -m pip install -r requirements.txt
```

Inicialização em desenvolvimento:

```bash
uvicorn app.main:app --reload --port 8001
```

A documentação interativa pode ser acessada em `/docs` enquanto o serviço estiver em execução.

As variáveis de ambiente disponíveis devem ser documentadas no arquivo `.env.example`. O arquivo `.env` local não deve ser versionado.

## 7. Testes

Os testes são executados com:

```bash
python -m pytest -v
```

A versão inicial possui cinco testes que cobrem:

1. Verificação de disponibilidade.
2. Explicação de uma movimentação reconhecida.
3. Tratamento de movimentação desconhecida.
4. Rejeição de descrição vazia.
5. Rejeição de data inválida.

A cobertura deve ser ampliada conforme forem adicionadas novas regras e funcionalidades.

## 8. Limitações conhecidas

A implementação atual utiliza regras determinísticas baseadas nas descrições das movimentações.

Isso significa que:

- Nem todas as movimentações judiciais são reconhecidas.
- A descrição isolada pode não fornecer contexto suficiente.
- O reconhecimento por palavras-chave pode produzir correspondências incorretas.
- O serviço ainda não consulta diretamente processos judiciais reais.
- A implementação atual não confirma prazos, resultados ou consequências jurídicas.
- A geração de áudio e a integração com canais de atendimento ainda não fazem parte desta versão.

As explicações devem permanecer limitadas às informações disponíveis. Movimentações não reconhecidas devem ser sinalizadas, e não interpretadas por suposição.

## 9. Evolução planejada

As próximas etapas previstas são:

1. Integrar o serviço Python ao backend Laravel.
2. Implementar tratamento de falhas e limites de tempo de resposta.
3. Aprimorar o reconhecimento das movimentações.
4. Definir fontes de dados processuais adequadas e autorizadas.
5. Ampliar os testes automatizados.
6. Avaliar recursos de áudio e outros canais de atendimento.

A evolução deve preservar a separação de responsabilidades entre frontend, backend e serviço Python.

## 10. Decisão arquitetural

O serviço Python foi organizado em camadas para separar inicialização, comunicação HTTP, configurações, validação de dados e processamento.

Essa separação facilita a manutenção, os testes e a evolução das regras de explicação, sem introduzir prematuramente dependências de banco de dados ou outras camadas ainda desnecessárias.
