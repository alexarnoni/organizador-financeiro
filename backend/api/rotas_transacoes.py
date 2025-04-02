from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.db import SessionLocal
from services import transacoes
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from services.sessao import obter_usuario_logado
from schemas.transacao import TransacaoUpdate
from models.usuario import Usuario
from database.db import get_db
from schemas.transacao import TransacaoCreate, TransacaoOut

router = APIRouter()

@router.post("/", response_model=TransacaoOut)
def criar_transacao(
    dados: TransacaoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_logado)
):
    return transacoes.criar_transacao(db, usuario_id=usuario.id, **dados.dict())

@router.get("/", response_model=List[TransacaoOut])
def listar_transacoes(
    mes: Optional[int] = Query(None),
    ano: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_logado)
):
    return transacoes.listar_transacoes(db, usuario.id, mes=mes, ano=ano)

@router.get("/resumo")
def resumo_financeiro(
    mes: Optional[int] = Query(None),
    ano: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_logado)
):
    return transacoes.obter_resumo(db, usuario_id=usuario.id, mes=mes, ano=ano)

@router.delete("/{transacao_id}")
def deletar_transacao(
    transacao_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_logado)
):
    return transacoes.excluir_transacao(db, transacao_id, usuario_id=usuario.id)

@router.get("/saldo-por-dia")
def saldo_por_dia(
    mes: Optional[int] = Query(None),
    ano: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_logado)
):
    return transacoes.saldo_por_dia(db, usuario_id=usuario.id, mes=mes, ano=ano)

@router.put("/{transacao_id}", response_model=TransacaoOut)
def atualizar_transacao(
    transacao_id: int,
    nova_transacao: TransacaoUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_logado)
):
    return transacoes.atualizar_transacao(db, transacao_id, nova_transacao, usuario.id)
