from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from database.db import get_db
from services import auth
from services.sessao import obter_usuario_logado
from pydantic import BaseModel, EmailStr
from models.usuario import Usuario

router = APIRouter()

class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str
    is_admin: bool = False

class UsuarioOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

@router.post("/registrar")
def registrar(usuario: UsuarioCreate, request: Request, db: Session = Depends(get_db)):
    # Impedir novos cadastros se já existe um admin
    admin_existente = db.query(Usuario).filter(Usuario.is_admin == 1).first()
    if admin_existente:
        raise HTTPException(status_code=403, detail="Registro fechado. Apenas um admin permitido.")

    # Criar novo admin se nenhum existe
    usuario_criado = auth.criar_usuario(db, usuario.email, usuario.senha)
    usuario_criado.is_admin = 1  # Torna o primeiro usuário um admin
    db.commit()

    return {
        "mensagem": "Usuário admin criado com sucesso!",
        "usuario": {
            "id": usuario_criado.id,
            "email": usuario_criado.email
        }
    }

@router.post("/login")
def login(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = auth.autenticar_usuario(db, usuario.email, usuario.senha)

    resposta = JSONResponse(content={"mensagem": "Login realizado com sucesso"})
    resposta.set_cookie(key="usuario_id", value=str(usuario_db.id), httponly=True)
    return resposta

@router.get("/login-status")
def login_status(request: Request, db: Session = Depends(get_db)):
    try:
        obter_usuario_logado(request, db)
        return {"logado": True}
    except:
        raise HTTPException(status_code=401, detail="Não autenticado")

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("usuario_id")
    return response
