# JusExplica

**JusExplica: a Justiça fala a sua língua!**

O JusExplica é um projeto que busca facilitar a compreensão de informações processuais, transformando informações jurídicas em explicações com linguagem simples e acessível. O projeto também prevê suporte à geração de áudio, tornando o acesso à informação mais inclusivo.

## Tecnologias

- **Frontend:** Next.js, React e TypeScript.
- **Backend:** PHP e Laravel.
- **Serviço de explicação:** Python e FastAPI.
- **Servidor Python:** Uvicorn.

O projeto está em desenvolvimento, e suas funcionalidades serão implementadas progressivamente.

## Pré-requisitos

Antes de executar o projeto, instale as ferramentas necessárias:

- Git
- Node.js e npm
- PHP e Composer
- Python 3 e pip
- Banco de dados compatível com a configuração do Laravel.

## 1. Clonar o repositório

```bash
git clone git@github.com:KDtech-dev/JusExplica.git
cd JusExplica
```

## 2. Executar o serviço Python

Acesse a pasta do serviço:

```bash
cd explanation-service
```

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Inicie o servidor:

```bash
uvicorn app.main:app --reload --port 8001
```

Após a inicialização, acesse:

- **API:** http://127.0.0.1:8001
- **Documentação interativa:** http://127.0.0.1:8001/docs

Para encerrar o servidor, pressione `Ctrl + C`.

Para sair do ambiente virtual:

```bash
deactivate
```

## 3. Executar o backend Laravel

Em outro terminal, acesse a pasta do backend:

```bash
cd backend
```

Instale as dependências:

```bash
composer install
```

Configure as variáveis de ambiente:

```bash
cp .env.example .env
php artisan key:generate
```

Edite o arquivo `.env` e configure as credenciais do banco de dados e as demais variáveis necessárias.

Execute as migrações, caso estejam configuradas para o projeto:

```bash
php artisan migrate
```

Inicie o servidor:

```bash
php artisan serve
```

Por padrão, a aplicação ficará disponível em:

http://127.0.0.1:8000

## 4. Executar o frontend

Em outro terminal, acesse a pasta do frontend:

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

Acesse a aplicação pelo navegador:

http://localhost:3000

Configure a URL da API no ambiente do frontend conforme as variáveis utilizadas pelo projeto.

## Estrutura do projeto

A organização prevista para o projeto é:

```text
JusExplica/
├── frontend/             # Interface da aplicação
├── backend/              # API e regras de negócio
├── explanation-service/  # Serviço Python com FastAPI
├── docs/                 # Documentação complementar
└── README.md
```

Os diretórios e serviços podem ser ajustados conforme a evolução da implementação.

## Fluxo de funcionamento

O fluxo planejado para a aplicação é:

1. O usuário acessa a interface do JusExplica.
2. O frontend envia uma solicitação ao backend.
3. O backend coordena o processamento com o serviço Python.
4. O serviço Python processa as informações e gera uma explicação em linguagem simples.
5. O resultado é disponibilizado ao usuário.

A geração de áudio e outras funcionalidades serão integradas conforme forem implementadas.

## Desenvolvimento

Para manter o desenvolvimento organizado, utilize branches para novas funcionalidades e Pull Requests para integrar alterações à branch principal.

Antes de enviar alterações, verifique se os serviços afetados estão funcionando corretamente.

## Desenvolvimento e Contribuição

O desenvolvimento do JusExplica segue um fluxo de trabalho baseado em branches e Pull Requests, garantindo maior organização, rastreabilidade e segurança nas alterações do código.

### Proteção da branch principal

A branch `main` é protegida por um Ruleset do GitHub com as seguintes regras:

- **Restrict deletions:** impede a exclusão da branch protegida.
- **Block force pushes:** impede operações de force push.
- **Require a pull request before merging:** exige Pull Requests para integrar alterações.
- **Require conversation resolution:** exige a resolução das conversas de revisão antes do merge.

Alterações devem ser desenvolvidas em branches específicas e integradas à `main` por meio de Pull Requests.

### Padrão de branches

Utilize os seguintes prefixos para nomear as branches:

| Prefixo | Finalidade | Exemplo |
|---|---|---|
| `feature/` | Implementação de funcionalidades | `feature/explanation-service` |
| `fix/` | Correção de erros | `fix/api-connection` |
| `docs/` | Alterações na documentação | `docs/readme-project` |
| `refactor/` | Refatoração de código | `refactor/explanation-service` |
| `test/` | Implementação ou melhoria de testes | `test/python-service` |

### Fluxo de desenvolvimento

**1. Atualize a branch principal**

```bash
git switch main
git pull origin main
```

**2. Crie uma branch para a tarefa**

```bash
git switch -c feature/nome-da-funcionalidade
```

**3. Desenvolva e teste**

Implemente as alterações e execute os testes pertinentes antes de enviá-las ao repositório.

Confira as modificações:

```bash
git status
git diff
```

**4. Registre as alterações**

```bash
git add .
git commit -m "feat: descreve a funcionalidade"
```

**5. Envie a branch ao GitHub**

```bash
git push -u origin feature/nome-da-funcionalidade
```

**6. Abra um Pull Request**

No GitHub, crie um Pull Request utilizando:

- **Base:** `main`
- **Compare:** a branch criada para a tarefa.

Descreva as alterações realizadas, os testes executados e eventuais pontos que precisam de atenção.

Revise o código e resolva as conversas de revisão pendentes antes de integrar as alterações.

**7. Atualize a branch principal após o merge**

```bash
git switch main
git pull origin main
```

### Padrão de commits

O projeto utiliza a convenção [Conventional Commits](https://www.conventionalcommits.org/pt-br/) para manter o histórico de alterações organizado.

| Tipo | Finalidade | Exemplo |
|---|---|---|
| `feat` | Nova funcionalidade | `feat: adiciona serviço de explicação` |
| `fix` | Correção de erros | `fix: corrige resposta da API` |
| `docs` | Documentação | `docs: atualiza README` |
| `refactor` | Refatoração | `refactor: organiza lógica do serviço` |
| `test` | Testes | `test: adiciona testes da API` |
| `chore` | Manutenção e configuração | `chore: ajusta configuração do projeto` |

### Boas práticas

- Não desenvolva diretamente na branch `main`.
- Crie uma branch específica para cada tarefa.
- Utilize mensagens de commit claras e padronizadas.
- Teste as alterações antes de abrir um Pull Request.
- Mantenha os Pull Requests focados em uma tarefa ou funcionalidade.
- Não envie arquivos `.env`, credenciais, tokens ou outros dados sensíveis ao repositório.
- Atualize a documentação quando houver mudanças relevantes na instalação, configuração ou utilização dos serviços.
- Não utilize `git push --force` na branch principal.

### Fluxo resumido

```text
Criar tarefa
    ↓
Criar branch
    ↓
Desenvolver e testar
    ↓
Commit
    ↓
Push da branch
    ↓
Abrir Pull Request
    ↓
Revisar alterações
    ↓
Resolver conversas pendentes
    ↓
Merge na main
```
