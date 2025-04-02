from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from database.db import get_db
from models.usuario import Usuario
from sqlalchemy import func, extract
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.sessao import obter_usuario_logado
from services import auth
from schemas.usuario import AdminCreate  # ✅ Importação do schema

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/usuarios-por-mes")
def usuarios_por_mes(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            extract("year", Usuario.created_at).label("ano"),
            extract("month", Usuario.created_at).label("mes"),
            func.count(Usuario.id).label("total")
        )
        .group_by("ano", "mes")
        .order_by("ano", "mes")
        .all()
    )

    return [
        {
            "ano": int(r.ano),
            "mes": int(r.mes),
            "total": r.total
        }
        for r in resultados
    ]

@router.get("/criar-admin")
def exibir_formulario_admin(request: Request, usuario=Depends(obter_usuario_logado)):
    if not usuario.is_admin:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("admin/criar_admin.html", {
        "request": request,
        "mensagem": None,
        "erro": None
    })

@router.post("/criar-admin")
def criar_admin(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
    usuario=Depends(obter_usuario_logado)
):
    if not usuario.is_admin:
        return RedirectResponse(url="/", status_code=302)

    try:
        # ✅ Validação com Pydantic
        dados = AdminCreate(email=email, senha=senha)

        novo_admin = auth.criar_usuario(db, email=dados.email, senha=dados.senha, is_admin=True)

        return templates.TemplateResponse("admin/criar_admin.html", {
            "request": request,
            "mensagem": f"Administrador {novo_admin.email} criado com sucesso!",
            "erro": None
        })
    except Exception as e:
        return templates.TemplateResponse("admin/criar_admin.html", {
            "request": request,
            "mensagem": None,
            "erro": str(e)
        })
