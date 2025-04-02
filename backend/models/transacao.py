from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # receita ou despesa
    valor = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    descricao = Column(String)
    data = Column(Date, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))  # <- adicione esta linha

    # (opcional) se quiser navegar: transacao.usuario.nome
    usuario = relationship("Usuario", back_populates="transacoes")