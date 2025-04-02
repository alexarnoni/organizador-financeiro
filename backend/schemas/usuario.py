from pydantic import BaseModel, EmailStr, Field

class AdminCreate(BaseModel):
    email: EmailStr = Field(..., description="Email válido")
    senha: str = Field(..., min_length=6, description="Senha com no mínimo 6 caracteres")
