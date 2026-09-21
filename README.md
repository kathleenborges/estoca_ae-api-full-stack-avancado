# Estoca aê! — API

API REST de **Cadastro, Solicitação e Estoque de materiais**, desenvolvida em Python com Flask. Ela registra os materiais, recebe solicitações e, quando uma solicitação é atendida, gera o item correspondente no estoque. Os dados são persistidos em SQLite e a documentação interativa (Swagger, Redoc e RapiDoc) é gerada automaticamente.

Esta API é o back-end da aplicação **Estoca aê!**. O front-end fica em outro repositório e consome também a Fake Store API (serviço externo). O fluxograma completo da arquitetura está no README do front.

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Rotas](#rotas)
- [Regras de negócio](#regras-de-negócio)
- [Modelo de dados](#modelo-de-dados)
- [Como executar](#como-executar)
- [Testes](#testes)
- [Documentação interativa](#documentação-interativa)
- [Repositórios do projeto](#repositórios-do-projeto)

## Funcionalidades

- **Cadastro:** adicionar, listar e remover materiais.
- **Solicitação:** criar, listar, atender e remover solicitações de material.
- **Estoque:** listar e remover os itens gerados quando uma solicitação é atendida.
- **Validação** dos dados de entrada com Pydantic e tratamento de erros (400, 404, 409, 422 e 500).
- **CORS** habilitado para o front-end.
- **Documentação** automática das rotas e dos schemas.
- **Testes automatizados** com pytest, usando um banco em memória.

## Tecnologias

| Item | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework web | Flask 3.1.2 |
| Documentação OpenAPI | flask-openapi3 4.3.0 (Swagger, Redoc e RapiDoc) |
| ORM | SQLAlchemy 2.0.45 |
| Validação | Pydantic 2.12.5 |
| CORS | Flask-CORS 6.0.2 |
| Banco de dados | SQLite |
| Testes | pytest 7.4.2 |
| Containerização | Docker |

## Estrutura do projeto

```
estoca_ae-api-full-stack-avancado/
├── app.py                 # Rotas e regra de negócio
├── conftest.py            # Configuração dos testes (banco em memória)
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── model/                 # Tabelas do banco (SQLAlchemy)
│   ├── __init__.py        # Engine, Session e criação das tabelas
│   ├── base.py
│   ├── cadastro.py
│   ├── estoque.py
│   ├── solicitacao.py
│   └── database/          # Criada automaticamente (db.sqlite3)
├── schemas/               # Contrato da API (Pydantic)
│   ├── __init__.py
│   ├── cadastro.py
│   ├── solicitacao.py
│   ├── estoque.py
│   ├── error.py
│   └── path.py
└── tests/
    └── test_api.py
```

A pasta `model/` define **como os dados são guardados no banco**, e a pasta `schemas/` define **o que a API recebe e devolve**.

## Rotas

| Método | Rota | Descrição | Respostas |
|---|---|---|---|
| GET | `/` | Redireciona para a documentação (`/openapi`) | 302 |
| POST | `/cadastros` | Cadastra um material (`nome`, `valor`, `link`) | 200, 409, 422, 500 |
| GET | `/cadastros` | Lista os materiais | 200 |
| DELETE | `/cadastros/{id}` | Remove um material sem solicitações | 200, 400, 404 |
| POST | `/solicitacoes` | Cria uma solicitação (`cadastro_id`, `quantidade`, `data_necessidade`) | 201, 404, 422, 500 |
| GET | `/solicitacoes` | Lista as solicitações | 200 |
| PUT | `/solicitacoes/{id}/atender` | Atende a solicitação e gera o estoque | 200, 400, 404 |
| DELETE | `/solicitacoes/{id}` | Remove uma solicitação ainda não atendida | 200, 400, 404 |
| GET | `/estoque` | Lista os itens em estoque | 200 |
| DELETE | `/estoque/{id}` | Remove um item do estoque | 200, 404 |

Os dados de entrada dos POST são enviados como **formulário** (`multipart/form-data` ou `application/x-www-form-urlencoded`).

## Regras de negócio

- `nome` e `link` de um material são **únicos**. Repetir um deles retorna 409.
- Uma solicitação nasce com o status `PENDENTE`.
- Atender uma solicitação muda o status para `ATENDIDA`, registra a data de atendimento e **cria o item de estoque** com `quantidade_disponivel` igual à quantidade solicitada.
- Uma solicitação já atendida não pode ser atendida de novo nem excluída (400).
- Um material que possui solicitações não pode ser excluído (400).

## Modelo de dados

- **Cadastro:** `id`, `nome` (único), `valor`, `link` (único), `data_cadastro`.
- **Solicitação:** `id`, `quantidade`, `status`, `data_solicitacao`, `data_necessidade`, `data_atendimento`, `cadastro_id`.
- **Estoque:** `id`, `quantidade_disponivel`, `data_entrada`, `solicitacao_id` (único).

Relacionamentos: um cadastro tem várias solicitações (1:N), e cada solicitação atendida gera um item de estoque (1:1).

## Como executar

### Pré-requisitos

- [Git](https://git-scm.com/)
- Python **3.12** (o `flask-openapi3` 4.3.0 não instala no Python 3.9) ou [Docker](https://docs.docker.com/get-docker/)

### Opção 1: localmente

```bash
git clone https://github.com/kathleenborges/estoca_ae-api-full-stack-avancado.git
cd estoca_ae-api-full-stack-avancado

python3.12 -m venv venv
source venv/bin/activate        # no Windows: venv\Scripts\activate
pip install -r requirements.txt

python app.py
```

A API fica disponível em http://localhost:5001. O banco `model/database/db.sqlite3` é criado automaticamente na primeira execução.

### Opção 2: com Docker

```bash
docker build -t estoca-ae-api .
docker run --rm -p 5001:5001 -v estoca_dados:/app/model/database estoca-ae-api
```

- `-p 5001:5001` expõe a API em http://localhost:5001.
- `-v estoca_dados:/app/model/database` guarda o banco em um volume, para os dados não se perderem quando o container é removido.

Para rodar a API junto com o front-end, use o `docker-compose.yml` do repositório do front.

## Testes

Com o ambiente virtual ativado:

```bash
python -m pytest -v
```

São 24 testes que cobrem todas as rotas, incluindo os casos de erro (400, 404, 409 e 422). Os testes usam um banco SQLite **em memória**, definido pela variável de ambiente `DATABASE_URL` no `conftest.py`, então o banco de desenvolvimento não é alterado.

Fora dos testes, se `DATABASE_URL` não estiver definida, a API usa o arquivo `model/database/db.sqlite3`.

## Documentação interativa

Com a API em execução, acesse http://localhost:5001/openapi e escolha o estilo de documentação:

- Swagger
- Redoc
- RapiDoc

Em cada um é possível ver os schemas, os códigos de resposta e testar as rotas diretamente.

## Repositórios do projeto

| Componente | Repositório |
|---|---|
| API (back-end, este repositório) | https://github.com/kathleenborges/estoca_ae-api-full-stack-avancado |
| Front-end | https://github.com/kathleenborges/estoca_ae_front |
