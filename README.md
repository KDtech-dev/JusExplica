# JusExplica

**JusExplica: a Justiça fala a sua língua!**

O JusExplica é um projeto que busca tornar as informações processuais mais acessíveis, transformando informações jurídicas em explicações claras, simples e compreensíveis.

A proposta também contempla recursos de acessibilidade, como a geração de áudio, para facilitar o acesso à informação jurídica.

> **Status:** Em desenvolvimento. As funcionalidades estão sendo implementadas progressivamente.

## Tecnologias

| Camada | Tecnologias |
|---|---|
| Frontend | Next.js, React e TypeScript |
| Backend | PHP e Laravel |
| Serviço de explicação | Python e FastAPI |
| Servidor ASGI | Uvicorn |
| Banco de dados | Configurado pelo Laravel |

## Arquitetura

O projeto é organizado em três componentes principais:

- **Frontend:** interface utilizada pelo usuário para acessar as funcionalidades do JusExplica.
- **Backend:** responsável pelas regras de negócio, pelo gerenciamento das solicitações e pela comunicação entre os componentes.
- **Serviço de explicação:** responsável pelo processamento das informações e pela produção de explicações em linguagem simples.

O fluxo de comunicação previsto é:

1. O usuário interage com a interface.
2. O frontend envia a solicitação ao backend Laravel.
3. O backend coordena o processamento com o serviço Python.
4. O serviço Python processa as informações recebidas.
5. O backend retorna o resultado ao frontend.
6. O usuário consulta a explicação apresentada.

A geração de áudio e outras funcionalidades serão incorporadas conforme a evolução do projeto.

## Estrutura do projeto

```text
JusExplica/
├── frontend/                 # Interface Next.js
├── backend/                  # API e regras de negócio Laravel
├── explanation-service/      # Serviço de explicação em Python
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── docs/                     # Documentação do projeto
├── .gitignore
└── README.md
```

A estrutura interna dos componentes pode ser ampliada conforme o desenvolvimento.

## Pré-requisitos

Antes de executar o projeto, instale:

- [Git](https://git-scm.com/)
- [Node.js e npm](https://nodejs.org/)
- [PHP](https://www.php.net/)
- [Composer](https://getcomposer.org/)
- [Python 3](https://www.python.org/)
- `pip`, gerenciador de pacotes do Python
- Um sistema de banco de dados compatível com a configuração do Laravel.

Verifique as instalações:

```bash
git --version
node --version
npm --version
php --version
composer --version
python3 --version
python3 -m pip --version
```

## Instalação e execução

Os componentes são executados separadamente durante o desenvolvimento. Utilize um terminal para cada serviço.

### 1. Clonar o repositório

Clone o repositório e entre na pasta do projeto:

```bash
git clone git@github.com:KDtech-dev/JusExplica.git
cd JusExplica
```

O comando de clonagem acima utiliza SSH. Para utilizá-lo, configure uma chave SSH associada à sua conta do GitHub.

### 2. Serviço de explicação — Python

Entre na pasta do serviço:

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
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Inicie o servidor de desenvolvimento:

```bash
uvicorn app.main:app --reload --port 8001
```

O serviço ficará disponível nos seguintes endereços:

| Recurso | Endereço |
|---|---|
| API | http://127.0.0.1:8001 |
| Documentação interativa | http://127.0.0.1:8001/docs |

Para encerrar o servidor, pressione `Ctrl + C`.

Para sair do ambiente virtual:

```bash
deactivate
```

**Observação:** mantenha o serviço Python em execução enquanto testa funcionalidades que dependam dele.

### 3. Backend — Laravel

Abra outro terminal e acesse a raiz do projeto:

```bash
cd ~/JusExplica/backend
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

Configure o arquivo `.env` com os dados necessários, incluindo as credenciais do banco de dados.

Depois de configurar e preparar o banco, execute as migrações disponíveis:

```bash
php artisan migrate
```

Inicie o servidor de desenvolvimento:

```bash
php artisan serve
```

Por padrão, o backend ficará disponível em:

http://127.0.0.1:8000

**Observação:** a execução completa depende da configuração do ambiente Laravel, do banco de dados e das integrações utilizadas pelo backend.

### 4. Frontend — Next.js

Abra outro terminal e acesse a pasta do frontend:

```bash
cd ~/JusExplica/frontend
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

Configure a URL do backend nas variáveis de ambiente utilizadas pelo frontend, conforme a implementação da aplicação.

**Observação:** a interface pode depender de endpoints do backend que ainda estejam em desenvolvimento.

## Documentação

A documentação complementar está disponível na pasta `docs/`.

| Documento | Descrição |
|---|---|
| [`arquitetura.md`](docs/arquitetura.md) | Organização dos componentes e decisões arquiteturais |
| [`contrato-api.md`](docs/contrato-api.md) | Contrato de comunicação entre Laravel e Python |
| [`requisitos.md`](docs/requisitos.md) | Requisitos funcionais e não funcionais |
| [`banco-de-dados.md`](docs/banco-de-dados.md) | Proposta inicial para a estrutura do banco de dados |

Os documentos representam as definições e propostas atuais do projeto e podem ser atualizados conforme as decisões de implementação.

## Desenvolvimento e contribuição

O desenvolvimento utiliza branches específicas para organizar funcionalidades, correções e alterações na documentação.

A integração de mudanças à branch principal deve ser realizada por meio de Pull Requests.

### Proteção da branch principal

A branch `main` possui regras de proteção configuradas no GitHub:

- **Restrict deletions:** impede a exclusão da branch protegida.
- **Block force pushes:** impede operações de force push.
- **Require a pull request before merging:** exige um Pull Request para integrar alterações.
- **Require conversation resolution:** exige a resolução das conversas de revisão antes do merge.

Essas regras ajudam a preservar o histórico do projeto e a organizar as revisões de código.

### Convenção de branches

Utilize os seguintes prefixos:

| Prefixo | Finalidade | Exemplo |
|---|---|---|
| `feature/` | Nova funcionalidade | `feature/explanation-service` |
| `fix/` | Correção de erro | `fix/api-connection` |
| `docs/` | Alteração na documentação | `docs/readme-project` |
| `refactor/` | Refatoração de código | `refactor/explanation-service` |
| `test/` | Criação ou atualização de testes | `test/python-service` |

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

**3. Desenvolva e revise as alterações:**

```bash
git status
git diff
```

Execute os testes pertinentes aos componentes modificados.

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

No GitHub, crie um Pull Request da sua branch para `main`.

Descreva as alterações realizadas, os testes executados e os pontos relevantes para a revisão. Resolva as conversas pendentes antes de integrar as alterações.

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
- Mantenha o `.gitignore` configurado para excluir dependências instaladas, ambientes virtuais, arquivos gerados e configurações locais.
- Atualize a documentação quando houver mudanças relevantes na instalação, configuração ou utilização dos serviços.
- Evite operações de force push na branch principal.

## Objetivos do projeto

O JusExplica busca:

- Facilitar a compreensão de informações processuais.
- Traduzir informações jurídicas para uma linguagem mais simples e acessível.
- Tornar o acesso à informação jurídica mais inclusivo.
- Ampliar as formas de consulta por meio de funcionalidades de acessibilidade, como a geração de áudio.

As explicações têm finalidade informativa e não substituem a análise individualizada de um profissional do Direito.

## Repositório

O código-fonte e o histórico de desenvolvimento estão disponíveis no GitHub:

**[KDTech-dev/JusExplica](https://github.com/KDtech-dev/JusExplica)**

---

Desenvolvido pela KDTech como um projeto de tecnologia voltado à acessibilidade e à compreensão da informação jurídica.