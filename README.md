# 🚀 Estoca aê! — API

API REST de **Cadastro, Solicitação e Estoque de materiais**, desenvolvida em Python com Flask.

A API registra materiais, recebe solicitações e, quando uma solicitação é atendida, gera o item correspondente no estoque. Os dados são persistidos em SQLite e a documentação interativa da API é disponibilizada automaticamente por meio de **Swagger, Redoc e RapiDoc**.

Esta API é o **back-end da aplicação Estoca aê!**. O front-end fica em um repositório separado e também consome a **Fake Store API**, utilizada como catálogo externo de referência.

O fluxograma completo da arquitetura está disponível no README do repositório do front-end.

---

## 📑 Sumário

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Rotas](#-rotas)
- [Regras de negócio](#-regras-de-negócio)
- [Modelo de dados](#-modelo-de-dados)
- [Como executar](#-como-executar)
- [Testes](#-testes)
- [Documentação interativa](#-documentação-interativa)
- [Repositórios do projeto](#-repositórios-do-projeto)

---

## 🚀 Funcionalidades

### 📦 Cadastro

- Adicionar materiais.
- Listar materiais.
- Remover materiais.
- Validar dados de entrada.
- Impedir duplicidade de `nome` e `link`.

### 📋 Solicitação

- Criar solicitações de materiais.
- Listar solicitações.
- Atender solicitações.
- Remover solicitações pendentes.
- Controlar o status das solicitações.

### 🏭 Estoque

- Gerar itens de estoque a partir de solicitações atendidas.
- Listar itens disponíveis no estoque.
- Remover itens do estoque.

### 🛡️ Validação e documentação

- Validação dos dados de entrada com **Pydantic**.
- Tratamento de erros HTTP `400`, `404`, `409`, `422` e `500`.
- **CORS** habilitado para comunicação com o front-end.
- Documentação automática das rotas e schemas.
- Testes automatizados utilizando **pytest** e banco SQLite em memória.

---

## 🛠️ Tecnologias

| Item | Tecnologia |
|---|---|
| **Linguagem** | Python 3.12 |
| **Framework web** | Flask 3.1.2 |
| **Documentação OpenAPI** | flask-openapi3 4.3.0 |
| **Documentação disponível** | Swagger, Redoc e RapiDoc |
| **ORM** | SQLAlchemy 2.0.45 |
| **Validação** | Pydantic 2.12.5 |
| **CORS** | Flask-CORS 6.0.2 |
| **Banco de dados** | SQLite |
| **Testes** | pytest 7.4.2 |
| **Containerização** | Docker |

---

## 📁 Estrutura do projeto

```text
estoca_ae-api-full-stack-avancado/
│
├── app.py                    # Rotas e regras de negócio
├── conftest.py               # Configuração dos testes
├── Dockerfile                # Configuração da imagem Docker
├── .dockerignore             # Arquivos ignorados pelo Docker
├── requirements.txt          # Dependências do projeto
│
├── model/                    # Modelos e configuração do banco
│   ├── __init__.py           # Engine, Session e criação das tabelas
│   ├── base.py
│   ├── cadastro.py
│   ├── estoque.py
│   ├── solicitacao.py
│   └── database/
│       └── db.sqlite3       # Criado automaticamente
│
├── schemas/                  # Contratos da API com Pydantic
│   ├── __init__.py
│   ├── cadastro.py
│   ├── solicitacao.py
│   ├── estoque.py
│   ├── error.py
│   ├── mensagem.py
│   └── path.py
│
└── tests/
    └── test_api.py           # Testes automatizados
```

A pasta `model/` define **como os dados são armazenados no banco**.

A pasta `schemas/` define **o que a API recebe e devolve**.

---

## 🔗 Rotas

| Método | Rota | Descrição | Respostas |
|:---:|---|---|:---:|
| `GET` | `/` | Redireciona para a documentação (`/openapi`) | `302` |
| `POST` | `/cadastros` | Cadastra um material (`nome`, `valor`, `link`) | `200`, `409`, `422`, `500` |
| `GET` | `/cadastros` | Lista os materiais | `200`, `500` |
| `DELETE` | `/cadastros/{id}` | Remove um material sem solicitações associadas | `200`, `400`, `404` |
| `POST` | `/solicitacoes` | Cria uma solicitação | `201`, `404`, `422`, `500` |
| `GET` | `/solicitacoes` | Lista as solicitações | `200` |
| `PUT` | `/solicitacoes/{id}/atender` | Atende a solicitação e gera o estoque | `200`, `400`, `404` |
| `DELETE` | `/solicitacoes/{id}` | Remove uma solicitação ainda não atendida | `200`, `400`, `404` |
| `GET` | `/estoque` | Lista os itens em estoque | `200` |
| `DELETE` | `/estoque/{id}` | Remove um item do estoque | `200`, `404` |

### 📌 Dados enviados

Os dados de entrada das rotas `POST` são enviados como **formulário**, utilizando:

- `multipart/form-data`
- `application/x-www-form-urlencoded`

---

## 📋 Regras de negócio

- `nome` e `link` de um material são **únicos**.
- Tentar cadastrar um material com `nome` ou `link` já existente retorna `409`.
- Uma solicitação nasce com o status `PENDENTE`.
- Atender uma solicitação altera seu status para `ATENDIDA`.
- Ao atender uma solicitação, a API registra a data de atendimento.
- Ao atender uma solicitação, é criado o item correspondente no estoque.
- A `quantidade_disponivel` do estoque é igual à quantidade solicitada.
- Uma solicitação já atendida não pode ser atendida novamente.
- Uma solicitação já atendida não pode ser excluída.
- As operações inválidas relacionadas a uma solicitação já atendida retornam `400`.
- Um material que possui solicitações associadas não pode ser excluído.
- Operações de exclusão de materiais com solicitações associadas retornam `400`.

---

## 🗃️ Modelo de dados

### Cadastro

Representa os materiais cadastrados.

Campos:

- `id`
- `nome` — único
- `valor`
- `link` — único
- `data_cadastro`

### Solicitação

Representa uma solicitação de material.

Campos:

- `id`
- `quantidade`
- `status`
- `data_solicitacao`
- `data_necessidade`
- `data_atendimento`
- `cadastro_id`

### Estoque

Representa os itens gerados a partir de solicitações atendidas.

Campos:

- `id`
- `quantidade_disponivel`
- `data_entrada`
- `solicitacao_id` — único

### 🔗 Relacionamentos

```text
Cadastro
   │
   │ 1:N
   ▼
Solicitação
   │
   │ 1:1
   ▼
Estoque
```

- Um **Cadastro** pode possuir várias **Solicitações**.
- Cada **Solicitação atendida** gera um único item de **Estoque**.

---

# 🚀 Como executar

## Pré-requisitos

Você precisará de:

- [Git](https://git-scm.com/)
- **Python 3.12**
- ou [Docker](https://docs.docker.com/get-docker/)

> ⚠️ O projeto utiliza `flask-openapi3 4.3.0`, portanto recomenda-se utilizar Python 3.12.

---

## 💻 Opção 1 — Execução local

### 1. Clone o repositório

```bash
git clone https://github.com/kathleenborges/estoca_ae-api-full-stack-avancado.git
```

### 2. Entre na pasta

```bash
cd estoca_ae-api-full-stack-avancado
```

### 3. Crie o ambiente virtual

No macOS/Linux:

```bash
python3.12 -m venv venv
```

No Windows:

```bash
python3.12 -m venv venv
```

### 4. Ative o ambiente virtual

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute a API

```bash
python app.py
```

A API ficará disponível em:

```text
http://localhost:5001
```

O banco:

```text
model/database/db.sqlite3
```

é criado automaticamente na primeira execução.

---

## 🐳 Opção 2 — Execução com Docker

### 1. Construa a imagem

```bash
docker build -t estoca-ae-api .
```

### 2. Execute o container

```bash
docker run --rm \
  -p 5001:5001 \
  -v estoca_dados:/app/model/database \
  estoca-ae-api
```

### Parâmetros utilizados

| Parâmetro | Função |
|---|---|
| `-p 5001:5001` | Expõe a API na porta `5001` |
| `-v estoca_dados:/app/model/database` | Mantém o banco persistido em um volume Docker |
| `--rm` | Remove o container ao encerrá-lo |

A API ficará disponível em:

```text
http://localhost:5001
```

Para executar a API junto com o front-end, utilize o `docker-compose.yml` disponível no repositório do front-end.

---

# 🧪 Testes

Com o ambiente virtual ativado, execute:

```bash
python -m pytest -v
```

Os testes cobrem as principais rotas da API, incluindo cenários de sucesso e erro:

- `200`
- `201`
- `400`
- `404`
- `409`
- `422`

Os testes utilizam um banco **SQLite em memória**, configurado no `conftest.py`.

Dessa forma, os testes não alteram o banco de desenvolvimento.

Fora dos testes, quando `DATABASE_URL` não está definida, a API utiliza:

```text
model/database/db.sqlite3
```

---

# 📚 Documentação interativa

Com a API em execução, acesse:

```text
http://localhost:5001/openapi
```

A partir dessa página é possível acessar as diferentes interfaces de documentação:

### 🔵 Swagger

Interface interativa para visualizar e testar as rotas da API.

### 🔴 Redoc

Interface para consulta da documentação OpenAPI.

### 🟢 RapiDoc

Interface alternativa para explorar os endpoints e schemas.

A documentação apresenta:

- Endpoints disponíveis.
- Parâmetros.
- Schemas.
- Códigos de resposta.
- Exemplos de requisição e resposta.
- Possibilidade de testar as rotas diretamente.

---

## 🔄 Integração com o Front-end

A API é consumida pelo front-end do projeto **Estoca aê!**.

O front-end utiliza JavaScript e `Fetch API` para realizar requisições HTTP para:

```text
http://127.0.0.1:5001
```

Entre os recursos utilizados estão:

```text
GET    /cadastros
POST   /cadastros
DELETE /cadastros/{id}

POST   /solicitacoes
GET    /solicitacoes
PUT    /solicitacoes/{id}/atender
DELETE /solicitacoes/{id}

GET    /estoque
DELETE /estoque/{id}
```

O front-end também utiliza a **Fake Store API** como catálogo externo de produtos.

---

# 🔗 Repositórios do projeto

| Componente | Repositório |
|---|---|
| 🔧 **API / Back-end** | [estoca_ae-api-full-stack-avancado](https://github.com/kathleenborges/estoca_ae-api-full-stack-avancado) |
| 🌐 **Front-end** | [estoca_ae-front-full-stack-avancado](https://github.com/kathleenborges/estoca_ae-front-full-stack-avancado) |

---

## 👩‍💻 Desenvolvimento

**Estoca aê!**

Projeto desenvolvido por **Kathleen Borges** como MVP para a Pós-Graduação em Engenharia de Software.

### 🎯 Objetivo

Desenvolver uma solução para:

- Cadastro de materiais.
- Solicitação de materiais.
- Atendimento de solicitações.
- Controle de estoque.
- Integração entre front-end, back-end e serviço externo.
- Aplicação de conceitos de arquitetura de software.

📦 **Front-end:** HTML5, CSS3, JavaScript e Nginx  
🔧 **Back-end:** Python, Flask, SQLAlchemy e SQLite  
🐳 **Infraestrutura:** Docker e Docker Compose  
🧪 **Testes:** pytest  
📚 **Documentação:** OpenAPI, Swagger, Redoc e RapiDoc