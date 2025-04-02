from sqlalchemy.orm import Session
from models.usuario import Usuario
from models.transacao import Transacao
from sqlalchemy import func

def total_usuarios(db: Session):
    return db.query(Usuario).filter(Usuario.is_admin == False).count()

def soma_receitas_despesas(db: Session):
    receitas = db.query(func.sum(Transacao.valor)).filter(Transacao.tipo == 'receita').scalar() or 0
    despesas = db.query(func.sum(Transacao.valor)).filter(Transacao.tipo == 'despesa').scalar() or 0
    return {"receitas": receitas, "despesas": despesas}

def categorias_mais_usadas(db: Session, limite: int = 5):
    return (
        db.query(Transacao.categoria, func.count().label("quantidade"))
        .group_by(Transacao.categoria)
        .order_by(func.count().desc())
        .limit(limite)
        .all()
    )
