from sqlalchemy.orm import Session
from models.usuario import Usuario
from passlib.hash import bcrypt
from fastapi import HTTPException

def criar_usuario(db: Session, email: str, senha: str, is_admin: bool = False):
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    senha_criptografada = bcrypt.hash(senha)
    novo_usuario = Usuario(email=email, senha_hash=senha_criptografada, is_admin=is_admin)

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not bcrypt.verify(senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    return usuario
