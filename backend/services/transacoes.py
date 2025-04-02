from sqlalchemy.orm import Session
from models.transacao import Transacao
from datetime import date
from sqlalchemy import func
from fastapi import HTTPException
from schemas.transacao import TransacaoUpdate

def criar_transacao(db: Session, usuario_id: int, tipo: str, valor: float, categoria: str, descricao: str, data: date):
    nova = Transacao(
        usuario_id=usuario_id,
        tipo=tipo,
        valor=valor,
        categoria=categoria,
        descricao=descricao,
        data=data
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def listar_transacoes(db: Session, usuario_id: int, mes: int = None, ano: int = None):
    query = db.query(Transacao).filter(Transacao.usuario_id == usuario_id)

    if mes and ano:
        query = query.filter(
            func.strftime("%m", Transacao.data) == f"{mes:02d}",
            func.strftime("%Y", Transacao.data) == str(ano)
        )
    elif ano:
        query = query.filter(func.strftime("%Y", Transacao.data) == str(ano))
    elif mes:
        query = query.filter(func.strftime("%m", Transacao.data) == f"{mes:02d}")

    return query.order_by(Transacao.data.desc()).all()

def obter_resumo(db: Session, usuario_id: int, mes: int = None, ano: int = None):
    query = db.query(Transacao).filter(Transacao.usuario_id == usuario_id)

    if mes and ano:
        query = query.filter(
            func.strftime("%m", Transacao.data) == f"{mes:02d}",
            func.strftime("%Y", Transacao.data) == str(ano)
        )
    elif ano:
        query = query.filter(func.strftime("%Y", Transacao.data) == str(ano))
    elif mes:
        query = query.filter(func.strftime("%m", Transacao.data) == f"{mes:02d}")

    transacoes = query.all()

    total_receitas = sum(t.valor for t in transacoes if t.tipo == "receita")
    total_despesas = sum(t.valor for t in transacoes if t.tipo == "despesa")
    saldo = total_receitas - total_despesas

    return {
        "receitas": total_receitas,
        "despesas": total_despesas,
        "saldo": saldo
    }

def atualizar_transacao(db: Session, transacao_id: int, nova_transacao: TransacaoUpdate, usuario_id: int):
    transacao = db.query(Transacao).filter(
        Transacao.id == transacao_id,
        Transacao.usuario_id == usuario_id
    ).first()

    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada.")

    transacao.tipo = nova_transacao.tipo
    transacao.valor = nova_transacao.valor
    transacao.categoria = nova_transacao.categoria
    transacao.descricao = nova_transacao.descricao
    transacao.data = nova_transacao.data

    db.commit()
    db.refresh(transacao)
    return transacao

def excluir_transacao(db: Session, transacao_id: int):
    transacao = db.query(Transacao).filter(Transacao.id == transacao_id).first()
    if transacao:
        db.delete(transacao)
        db.commit()
        return {"mensagem": "Transação excluída com sucesso"}
    else:
        return {"erro": "Transação não encontrada"}

def saldo_por_dia(db: Session, usuario_id: int, mes: int = None, ano: int = None):
    query = db.query(Transacao).filter(Transacao.usuario_id == usuario_id)

    if mes and ano:
        query = query.filter(
            func.strftime("%m", Transacao.data) == f"{mes:02d}",
            func.strftime("%Y", Transacao.data) == str(ano)
        )
    elif ano:
        query = query.filter(func.strftime("%Y", Transacao.data) == str(ano))
    elif mes:
        query = query.filter(func.strftime("%m", Transacao.data) == f"{mes:02d}")

    transacoes = query.order_by(Transacao.data.asc()).all()

    saldo = 0
    saldo_diario = {}

    for t in transacoes:
        if t.tipo == "receita":
            saldo += t.valor
        else:
            saldo -= t.valor

        data_str = t.data.strftime("%Y-%m-%d")
        saldo_diario[data_str] = saldo

    return [{"data": data, "saldo": valor} for data, valor in saldo_diario.items()]
