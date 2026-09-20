import pytest
from app import app

PAYLOAD_CADASTRO = {
    "nome": "Parafuso",
    "valor": 2.50,
    "link": "https://www.exemplo.com/parafuso",
}
DATA_NECESSIDADE = "2026-12-01T00:00:00"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

def criar_cadastro(client, **extra):
    response = client.post("/cadastros", data={**PAYLOAD_CADASTRO, **extra})
    assert response.status_code == 200
    return response.get_json()


def criar_solicitacao(client, cadastro_id, quantidade=5):
    response = client.post("/solicitacoes", data={
        "cadastro_id": cadastro_id,
        "quantidade": quantidade,
        "data_necessidade": DATA_NECESSIDADE,
    })
    assert response.status_code == 201
    return response.get_json()


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------

def test_home_redireciona_para_openapi(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/openapi")


# ---------------------------------------------------------------------------
# CADASTRO
# ---------------------------------------------------------------------------

def test_criar_cadastro_sucesso(client):
    response = client.post("/cadastros", data=PAYLOAD_CADASTRO)
    assert response.status_code == 200
    assert response.get_json()["nome"] == PAYLOAD_CADASTRO["nome"]


def test_criar_cadastro_dados_invalidos(client):
    response = client.post("/cadastros", data={"nome": "X", "valor": "abc", "link": "y"})
    assert response.status_code in (400, 422)


def test_criar_cadastro_nome_duplicado(client):
    criar_cadastro(client)
    response = client.post("/cadastros", data=PAYLOAD_CADASTRO)
    assert response.status_code == 409


def test_criar_cadastro_link_duplicado(client):
    criar_cadastro(client)
    outro = {**PAYLOAD_CADASTRO, "nome": "Outro nome"}   # mesmo link, nome diferente
    response = client.post("/cadastros", data=outro)
    assert response.status_code == 409


def test_listar_cadastros_vazio(client):
    response = client.get("/cadastros")
    assert response.status_code == 200
    assert response.get_json() == {"cadastros": []}


def test_listar_cadastros_com_item(client):
    criar_cadastro(client)
    response = client.get("/cadastros")
    assert response.status_code == 200
    assert len(response.get_json()["cadastros"]) == 1


def test_deletar_cadastro_sucesso(client):
    cadastro = criar_cadastro(client)
    response = client.delete(f"/cadastros/{cadastro['id']}")
    assert response.status_code == 200


def test_deletar_cadastro_inexistente(client):
    response = client.delete("/cadastros/9999")
    assert response.status_code == 404


def test_deletar_cadastro_com_solicitacoes(client):
    cadastro = criar_cadastro(client)
    criar_solicitacao(client, cadastro["id"])
    response = client.delete(f"/cadastros/{cadastro['id']}")
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# SOLICITAÇÃO
# ---------------------------------------------------------------------------

def test_criar_solicitacao_sucesso(client):
    cadastro = criar_cadastro(client)
    solicitacao = criar_solicitacao(client, cadastro["id"], quantidade=5)
    assert solicitacao["status"] == "PENDENTE"
    assert solicitacao["quantidade"] == 5


def test_criar_solicitacao_cadastro_inexistente(client):
    response = client.post("/solicitacoes", data={
        "cadastro_id": 9999,
        "quantidade": 5,
        "data_necessidade": DATA_NECESSIDADE,
    })
    assert response.status_code == 404


def test_criar_solicitacao_dados_invalidos(client):
    response = client.post("/solicitacoes", data={"quantidade": "abc"})
    assert response.status_code in (400, 422)


def test_listar_solicitacoes_vazio(client):
    response = client.get("/solicitacoes")
    assert response.status_code == 200
    assert response.get_json() == {"solicitacoes": []}


def test_atender_solicitacao_sucesso(client):
    cadastro = criar_cadastro(client)
    solicitacao = criar_solicitacao(client, cadastro["id"])

    response = client.put(f"/solicitacoes/{solicitacao['id']}/atender")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ATENDIDA"


def test_atender_solicitacao_inexistente(client):
    response = client.put("/solicitacoes/9999/atender")
    assert response.status_code == 404


def test_atender_solicitacao_duas_vezes(client):
    cadastro = criar_cadastro(client)
    solicitacao = criar_solicitacao(client, cadastro["id"])

    client.put(f"/solicitacoes/{solicitacao['id']}/atender")
    response = client.put(f"/solicitacoes/{solicitacao['id']}/atender")
    assert response.status_code == 400


def test_deletar_solicitacao_pendente(client):
    cadastro = criar_cadastro(client)
    solicitacao = criar_solicitacao(client, cadastro["id"])
    response = client.delete(f"/solicitacoes/{solicitacao['id']}")
    assert response.status_code == 200


def test_deletar_solicitacao_atendida(client):
    cadastro = criar_cadastro(client)
    solicitacao = criar_solicitacao(client, cadastro["id"])
    client.put(f"/solicitacoes/{solicitacao['id']}/atender")

    response = client.delete(f"/solicitacoes/{solicitacao['id']}")
    assert response.status_code == 400


def test_deletar_solicitacao_inexistente(client):
    response = client.delete("/solicitacoes/9999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# ESTOQUE
# ---------------------------------------------------------------------------

def test_listar_estoque_vazio(client):
    response = client.get("/estoque")
    assert response.status_code == 200
    assert response.get_json() == {"estoque": []}


def test_atender_solicitacao_gera_estoque(client):
    cadastro = criar_cadastro(client)
    solicitacao = criar_solicitacao(client, cadastro["id"], quantidade=7)
    client.put(f"/solicitacoes/{solicitacao['id']}/atender")

    response = client.get("/estoque")
    itens = response.get_json()["estoque"]
    assert response.status_code == 200
    assert len(itens) == 1
    assert itens[0]["quantidade_disponivel"] == 7


def test_deletar_estoque_sucesso(client):
    cadastro = criar_cadastro(client)
    solicitacao = criar_solicitacao(client, cadastro["id"])
    client.put(f"/solicitacoes/{solicitacao['id']}/atender")
    estoque_id = client.get("/estoque").get_json()["estoque"][0]["id"]

    response = client.delete(f"/estoque/{estoque_id}")
    assert response.status_code == 200


def test_deletar_estoque_inexistente(client):
    response = client.delete("/estoque/9999")
    assert response.status_code == 404