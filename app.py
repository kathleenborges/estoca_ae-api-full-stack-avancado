from flask_openapi3 import OpenAPI, Info, Tag
from flask import jsonify
from flask import redirect
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import joinedload



from model import Session, Cadastro, Solicitacao, Estoque, Base, engine
from schemas import *
from flask_cors import CORS


# -----------------------------------------------------------------------------
# API INFO
# -----------------------------------------------------------------------------


info = Info(title="Estoca ae!", version="1.0.0", description="API de Cadastro, Solicitação e Estoque")
app = OpenAPI(__name__, info=info)
CORS(app)


# -----------------------------------------------------------------------------
# TAGS
# -----------------------------------------------------------------------------


home_tag = Tag(name="Home", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cadastro_tag = Tag(name="Cadastro", description="Adição, visualização e remoção de materiais à base")
solicitacao_tag = Tag(name="Solicitação", description="Realização de pedido de material")
estoque_tag = Tag(name="Estoque", description="Controle de estoque após atendimento da solicitação")


# -----------------------------------------------------------------------------
# HOME
# -----------------------------------------------------------------------------

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# -----------------------------------------------------------------------------
# CADASTRO
# -----------------------------------------------------------------------------

@app.post("/cadastros", tags=[cadastro_tag])

def criar_cadastro(form: CriacaoCadastroSchema):
    """Adiciona um novo material à base com campos individuais"""
    session = Session()
    try:
        
        dados = form.model_dump() 
        cadastro = Cadastro(**dados)
        session.add(cadastro)
        session.commit()
        
        return RespostaCadastroSchema.model_validate(cadastro).model_dump(), 200
    except IntegrityError:
        session.rollback()
        return {"message": "Erro de integridade (talvez o item já exista)"}, 409
    except Exception as e:
        session.rollback()
        return {"message": f"Erro interno: {str(e)}"}, 500
    finally:
        session.close()

@app.get("/cadastros", tags=[cadastro_tag], responses={"200": ListaCadastrosSchema})
def listar_cadastros():
    """Lista todos os produtos cadastrados."""
    session = Session()
    try:
        # Busca todos os cadastros
        cadastros = session.query(Cadastro).all()
        
        # Converte os objetos do banco para o formato do Schema
        return {
            "cadastros": [RespostaCadastroSchema.model_validate(c).model_dump() for c in cadastros]
        }, 200
        
    except Exception as e:
        print(f"Erro ao listar: {e}")
        return {"message": "Erro interno"}, 500
    finally:
        session.close()

@app.delete("/cadastros/<int:id>", tags=[cadastro_tag])
def deletar_cadastro(path: IdPathSchema):
    session = Session()

    cadastro = session.get(Cadastro, path.id)
    if not cadastro:
        session.close()
        return {"message": "Cadastro não encontrado"}, 404

    if cadastro.solicitacoes:
        session.close()
        return {
            "message": "Cadastro possui solicitações associadas"
        }, 400


    session.delete(cadastro)
    session.commit()
    session.close()

    return {"message": "Cadastro removido com sucesso"}


# -----------------------------------------------------------------------------
# SOLICITAÇÃO
# -----------------------------------------------------------------------------
    

@app.post("/solicitacoes", tags=[solicitacao_tag], responses={"201": RespostaSolicitacaoSchema})
def criar_solicitacao(form: CriacaoSolicitacaoSchema): 
    """Cria uma solicitação com campos individuais de preenchimento"""
    session = Session()
    try:
        
        cadastro = session.query(Cadastro).filter(Cadastro.id == form.cadastro_id).first()
        
        if not cadastro:
            return {"message": "Cadastro não encontrado"}, 404

        solicitacao = Solicitacao(
            quantidade=form.quantidade,
            data_necessidade=form.data_necessidade,
            cadastro_id=cadastro.id,
            status="PENDENTE"
        )

        session.add(solicitacao)
        session.commit()
        session.refresh(solicitacao)

        return RespostaSolicitacaoSchema.model_validate(solicitacao).model_dump(), 201
    except Exception as e:
        session.rollback()
        return {"message": f"Erro: {str(e)}"}, 500
    finally:
        session.close()


@app.put("/solicitacoes/<int:id>/atender", tags=[solicitacao_tag])
def atender_solicitacao(path: IdPathSchema):
    session = Session()
    try:
        solicitacao = session.get(Solicitacao, path.id)
        if not solicitacao:
            return {"message": "Solicitação não encontrada"}, 404

        gerar_estoque_da_solicitacao(solicitacao)
        session.commit()
        return RespostaSolicitacaoSchema.model_validate(solicitacao).model_dump(), 200
    except ValueError as e:
        session.rollback()
        return {"message": str(e)}, 400
    finally:
        session.close()


@app.get("/solicitacoes", tags=[solicitacao_tag], responses={"200": ListaSolicitacoesSchema})
def listar_solicitacoes():
    """Busca todas as solicitações feitas.
    Retorna uma listagem de solicitações.
    """
    session = Session()
    try:
        # Busca todas as solicitações no banco
        solicitacoes = session.query(Solicitacao).all()

        if not solicitacoes:
            return {"solicitacoes": []}, 200
        
        # Converte para o formato do Schema
        lista = [RespostaSolicitacaoSchema.model_validate(s).model_dump() for s in solicitacoes]
        
        return {"solicitacoes": lista}, 200
    finally:
        session.close()


@app.delete("/solicitacoes/<int:id>", tags=[solicitacao_tag])
def deletar_solicitacao(path: IdPathSchema):
    session = Session()

    solicitacao = session.get(Solicitacao, path.id)
    if not solicitacao:
        session.close()
        return {"message": "Solicitação não encontrada"}, 404

    if solicitacao.status == "ATENDIDA":
        session.close()
        return {
            "message": "Não é possível excluir solicitação atendida"
        }, 400

    session.delete(solicitacao)
    session.commit()
    session.close()

    return {"message": "Solicitação removida com sucesso"}


# -----------------------------------------------------------------------------
# ESTOQUE
# -----------------------------------------------------------------------------

@app.get("/estoque", tags=[estoque_tag], responses={"200": ListaEstoqueSchema})
def listar_estoque():
    """Lista todos os itens em estoque com os nomes dos produtos."""
    session = Session()
    try:
        
        itens = session.query(Estoque).options(
            joinedload(Estoque.solicitacao).joinedload(Solicitacao.cadastro)
        ).all()
        
        return {
            "estoque": [RespostaEstoqueSchema.model_validate(i).model_dump() for i in itens]
        }, 200
    finally:
        session.close()


@app.delete("/estoque/<int:id>", tags=[estoque_tag])
def deletar_estoque(path: IdPathSchema):
    session = Session()

    # Busca o item de estoque pelo ID
    estoque = session.get(Estoque, path.id)
    
    if not estoque:
        session.close()
        return {"message": "Estoque não encontrado"}, 404

    session.delete(estoque)
    session.commit()
    session.close()

    return {"message": "Estoque removido com sucesso"}

# -----------------------------------------------------------------------------
# SERVICE (REGRA DE NEGÓCIO)
# -----------------------------------------------------------------------------

def gerar_estoque_da_solicitacao(solicitacao: Solicitacao):
    """
    Regra de negócio para atender uma solicitação e gerar estoque.
    O estoque só precisa da quantidade e do vínculo com a solicitação.
    """
    if solicitacao.status == "ATENDIDA":
        raise ValueError("Solicitação já atendida")

    if solicitacao.estoque:
        raise ValueError("Estoque já gerado")

    data_atual_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # Criar o estoque exatamente com as colunas definidas na Model Estoque
    novo_estoque = Estoque(
        quantidade_disponivel=solicitacao.quantidade,
        data_entrada=data_atual_str,
        solicitacao_id=solicitacao.id  
    )
    
    # Vincula o objeto para o SQLAlchemy e para o Pydantic
    solicitacao.estoque = novo_estoque
    solicitacao.data_atendimento = data_atual_str
    solicitacao.status = "ATENDIDA"

# -----------------------------------------------------------------------------
# START
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Servidor rodando na porta 5001!")
   
    app.run(debug=True, port=5001)

