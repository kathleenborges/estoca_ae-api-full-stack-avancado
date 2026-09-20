# 📦 Estoca aê! 
Primeiro MVP para Pós PUC RIO - Engenharia de Software 

O **Estoca aê!** é uma API de gerenciamento de estoque que tem por objetivo facilitar e centralizar o controle de materiais e solicitações de suprimentos de qualquer empresa.

## 🚀 Tecnologias Utilizadas

* **Python 3.10**
* **Flask**: Framework web para Python.
* **Flask-OpenAPI3**: Gerenciamento de rotas e documentação Swagger automática.
* **SQLAlchemy**: ORM para persistência de dados.
* **SQLite**: Banco de dados relacional leve.
* **Pydantic**: Validação de dados e definição de Schemas.

## 📋 Funcionalidades Principais

- **Cadastro de Materiais**: Registro completo de itens na base de dados.
*(Suporta: POST, GET e DELETE)*
- **Gestão de Solicitações**: Criação de pedidos de materiais com controle de status.
*(Suporta: POST, GET, PUT e DELETE)*
- **Atendimento de Estoque**: Processamento de solicitações para atualização de saldos.
*(Suporta: GET e DELETE)*

## 🔧 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   https://github.com/kathleenborges/estoca_ae_api.git
   
2. **Crie e ative o ambiente virtual:**

python3.10 -m venv venv-api

source venv-api/bin/activate

3. **Instale as dependências:**

pip install -r requirements.txt

4. **Inicie o servidor:**

python3.10 app.py
  
5. **Acesse a documentação:**

Abra o seu navegador em: http://127.0.0.1:5001/openapi

*"Dica: Certifique-se de selecionar o interpretador Python do ambiente virtual (venv-api) no seu editor."*


## 🛠️ Estrutura do Projeto
app.py: Ponto de entrada da aplicação e definição das rotas.

model/: Definições das tabelas do banco de dados (Banco SQLite).

schemas/: Schemas do Pydantic para validação e documentação Swagger.

Desenvolvido por Kathleen Borges 

