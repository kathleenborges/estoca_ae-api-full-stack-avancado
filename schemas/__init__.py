from schemas.estoque import RespostaEstoqueSchema, ListaEstoqueSchema
from schemas.solicitacao import (
    CriacaoSolicitacaoSchema, 
    SolicitacaoUpdateStatusSchema, 
    RespostaSolicitacaoSchema,
    ListaSolicitacoesSchema
)
from schemas.cadastro import (
    CriacaoCadastroSchema, 
    RespostaCadastroSchema, 
    ListaCadastrosSchema,
    CadastroBuscaSchema,
    CadastroDelSchema
)
from schemas.error import ErrorSchema
from schemas.path import IdPathSchema