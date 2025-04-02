from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

class TransacaoBase(BaseModel):
    tipo: str
    valor: float
    categoria: str
    descricao: Optional[str] = None
    data: date

    @validator("categoria", "descricao", pre=True, always=True)
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

class TransacaoCreate(TransacaoBase):
    tipo: str = Field(..., pattern="^(receita|despesa)$", description="Tipo deve ser 'receita' ou 'despesa'")
    valor: float = Field(..., gt=0, description="Valor deve ser maior que zero")
    categoria: str = Field(..., min_length=2, max_length=50, description="Categoria entre 2 e 50 caracteres")
    descricao: Optional[str] = Field(None, max_length=100, description="Descrição até 100 caracteres")
    data: date = Field(..., description="Data da transação")

class TransacaoUpdate(TransacaoBase):
    pass

class TransacaoOut(TransacaoBase):
    id: int

    class Config:
        from_attributes = True
