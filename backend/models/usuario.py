from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    is_admin = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    transacoes = relationship("Transacao", back_populates="usuario")