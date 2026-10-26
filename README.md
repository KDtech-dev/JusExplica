# JusExplica

**JusExplica: a Justiça fala a sua língua!**

O JusExplica é um projeto que busca tornar as informações processuais mais acessíveis, transformando informações jurídicas em explicações claras, simples e compreensíveis para qualquer pessoa.

A proposta também contempla a geração de áudio, contribuindo para ampliar a acessibilidade e facilitar o acesso à informação jurídica.

> **Status:** Em desenvolvimento. As funcionalidades estão sendo implementadas progressivamente.

## Tecnologias

O projeto utiliza tecnologias distintas para a interface, as regras de negócio e o processamento das explicações.

| Camada | Tecnologias |
|---|---|
| Frontend | Next.js, React e TypeScript |
| Backend | PHP e Laravel |
| Serviço de explicação | Python e FastAPI |
| Servidor ASGI | Uvicorn |

## Arquitetura do projeto

A arquitetura proposta divide a aplicação em três componentes principais:

- **Frontend:** interface utilizada pelo usuário para acessar as funcionalidades do JusExplica.
- **Backend:** responsável pelas regras de negócio, pelo gerenciamento das solicitações e pela comunicação entre os componentes.
- **Serviço de explicação:** responsável pelo processamento das informações e pela geração de explicações em linguagem simples.

A geração de áudio será integrada conforme a implementação e a evolução do projeto.

### Estrutura de diretórios

A organização prevista para o repositório é:

```text
JusExplica/
├── frontend/             # Interface da aplicação
├── backend/              # API e regras de negócio
├── explanation-service/  # Serviço de explicação em Python
├── docs/                 # Documentação complementar
└── README.md
```

A estrutura poderá ser ajustada conforme o desenvolvimento dos componentes.

## Pré-requisitos

Antes de executar o projeto, instale as seguintes ferramentas:

- [Git](https://git-scm.com/)
- [Node.js e npm](https://nodejs.org/)
- [PHP](https://www.php.net/)
- [Composer](https://getcomposer.org/)
- [Python 3](https://www.python.org/)
- `pip`, gerenciador de pacotes do Python
- Um banco de dados compatível com a configuração do Laravel.

Alguns pré-requisitos serão necessários apenas para executar os componentes correspondentes. A disponibilidade dos serviços depende da implementação atual do projeto.

## Instalação e execução

### 1. Clonar o repositório

Clone o repositório e acesse a pasta do projeto:

```bash
git clone git@github.com:KDtech-dev/JusExplica.git
cd JusExplica
```

### 2. Serviço de explicação — Python

Acesse o diretório do serviço:

```bash
cd explanation-service
```

Crie um ambiente virtual:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual no Linux:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Inicie o servidor de desenvolvimento:

```bash
uvicorn app.main:app --reload --port 8001
```

Com o serviço em execução, os endereços disponíveis são:

| Recurso | Endereço |
|---|---|
| API | http://127.0.0.1:8001 |
| Documentação interativa | http://127.0.0.1:8001/docs |

Para encerrar o servidor, pressione `Ctrl + C`.

Para sair do ambiente virtual:

```bash
deactivate
```

**Observação:** os comandos pressupõem que o arquivo `requirements.txt` e o módulo `app.main` estejam presentes no serviço.

### 3. Backend — Laravel

Em outro terminal, retorne à raiz do projeto e acesse o backend:

```bash
cd backend
```

Instale as dependências:

```bash
composer install
```

Crie o arquivo de configuração local:

```bash
cp .env.example .env
```

Gere a chave da aplicação:

```bash
php artisan key:generate
```

Configure no arquivo `.env` as variáveis necessárias, incluindo as credenciais do banco de dados.

Execute as migrações, caso estejam disponíveis e configuradas:

```bash
php artisan migrate
```

Inicie o servidor:

```bash
php artisan serve
```

Por padrão, o backend ficará disponível em:

http://127.0.0.1:8000

**Observação:** as instruções pressupõem que o diretório `backend` contenha uma aplicação Laravel configurada.

### 4. Frontend — Next.js

Em outro terminal, acesse o diretório do frontend a partir da raiz do projeto:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

Por padrão, a interface ficará disponível em:

http://localhost:3000

Configure a URL da API nas variáveis de ambiente utilizadas pelo frontend, de acordo com a configuração da aplicação.

**Observação:** as instruções pressupõem que o diretório `frontend` contenha uma aplicação Next.js configurada.

## Fluxo de funcionamento

O fluxo planejado para o JusExplica é:

1. O usuário acessa a interface da aplicação.
2. O frontend envia uma solicitação ao backend.
3. O backend coordena o processamento das informações com o serviço Python.
4. O serviço de explicação processa as informações e produz uma explicação em linguagem simples.
5. O backend disponibiliza o resultado ao frontend.
6. O usuário consulta a explicação gerada.

A geração de áudio e outras funcionalidades serão incorporadas conforme o avanço do desenvolvimento.

## Desenvolvimento e contribuição

O desenvolvimento utiliza branches específicas para organizar funcionalidades, correções e outras alterações. A integração de mudanças à branch principal é realizada por meio de Pull Requests.

### Proteção da branch principal

A branch `main` possui regras de proteção configuradas no GitHub:

- **Restrict deletions:** impede a exclusão da branch protegida.
- **Block force pushes:** impede operações de force push.
- **Require a pull request before merging:** exige um Pull Request para integrar alterações.
- **Require conversation resolution:** exige a resolução das conversas de revisão antes do merge.

Essas regras ajudam a preservar o histórico do projeto e a organizar as alterações.

### Convenção de branches

Utilize os seguintes prefixos para identificar o objetivo de cada branch:

| Prefixo | Finalidade | Exemplo |
|---|---|---|
| `feature/` | Nova funcionalidade | `feature/explanation-service` |
| `fix/` | Correção de erro | `fix/api-connection` |
| `docs/` | Documentação | `docs/readme-project` |
| `refactor/` | Refatoração | `refactor/explanation-service` |
| `test/` | Testes | `test/python-service` |

### Fluxo de trabalho

**1. Atualize a branch principal:**

```bash
git switch main
git pull origin main
```

**2. Crie uma branch para a tarefa:**

```bash
git switch -c feature/nome-da-funcionalidade
```

**3. Desenvolva e teste as alterações:**

```bash
git status
git diff
```

Execute também os testes pertinentes aos componentes modificados.

**4. Registre as alterações:**

```bash
git add .
git commit -m "feat: descreve a funcionalidade"
```

**5. Envie a branch ao GitHub:**

```bash
git push -u origin feature/nome-da-funcionalidade
```

**6. Abra um Pull Request:**

No GitHub, crie um Pull Request da sua branch para a `main`. Descreva as alterações realizadas, os testes executados e os pontos relevantes para a revisão.

Resolva as conversas de revisão pendentes antes de integrar as alterações.

**7. Atualize a branch principal após o merge:**

```bash
git switch main
git pull origin main
```

### Convenção de commits

O projeto adota a convenção [Conventional Commits](https://www.conventionalcommits.org/pt-br/) para manter as mensagens de commit claras e consistentes.

| Tipo | Finalidade | Exemplo |
|---|---|---|
| `feat` | Nova funcionalidade | `feat: adiciona serviço de explicação` |
| `fix` | Correção de erro | `fix: corrige resposta da API` |
| `docs` | Documentação | `docs: atualiza README` |
| `refactor` | Refatoração | `refactor: organiza lógica do serviço` |
| `test` | Testes | `test: adiciona testes da API` |
| `chore` | Manutenção e configuração | `chore: ajusta configuração do projeto` |

### Boas práticas

- Desenvolva em branches específicas, evitando alterações diretas na `main`.
- Mantenha cada Pull Request focado em uma tarefa.
- Utilize mensagens de commit descritivas.
- Teste as alterações antes de abrir um Pull Request.
- Não envie arquivos `.env`, credenciais, tokens ou outras informações sensíveis ao repositório.
- Atualize a documentação quando houver mudanças relevantes na instalação, configuração ou utilização dos serviços.
- Evite operações de force push na branch principal.

## Objetivos do projeto

O JusExplica busca:

- Facilitar a compreensão de informações processuais.
- Traduzir informações jurídicas para uma linguagem mais simples e acessível.
- Tornar o acesso à informação jurídica mais inclusivo.
- Ampliar as formas de consulta por meio de funcionalidades como a geração de áudio.

## Repositório

O código-fonte e o histórico de desenvolvimento estão disponíveis no GitHub:

**[KDTech-dev/JusExplica](https://github.com/KDtech-dev/JusExplica)**

---

Desenvolvido como um projeto de tecnologia voltado à acessibilidade e à compreensão da informação jurídica.
