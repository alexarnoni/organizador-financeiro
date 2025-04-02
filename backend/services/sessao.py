from fastapi import Request, HTTPException, Depends
from models.usuario import Usuario
from database.db import get_db
from sqlalchemy.orm import Session

def obter_usuario_logado(request: Request, db: Session = Depends(get_db)) -> Usuario:
    usuario_id = request.cookies.get("usuario_id")
    if not usuario_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado.")

    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")

    return usuario
