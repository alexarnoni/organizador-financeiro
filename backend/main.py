from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from api.rotas_transacoes import router as transacoes_router
from database.db import engine
from models import transacao
from api.rotas_usuarios import router as usuarios_router
from models import usuario
import datetime
from services.sessao import obter_usuario_logado
from models.usuario import Usuario
from database.db import get_db
from services import admin as admin_service
from api.rotas_admin import router as admin_router

app = FastAPI(title="Organizador Financeiro")

# Criar tabelas
transacao.Base.metadata.create_all(bind=engine)
usuario.Base.metadata.create_all(bind=engine)

# Conectar rotas da API
app.include_router(transacoes_router, prefix="/api/transacoes")
app.include_router(usuarios_router, prefix="/api/usuarios")
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

# Configurar templates e arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Rota principal que renderiza home.html
@app.get("/", response_class=HTMLResponse)
def render_home(request: Request, db: Session = Depends(get_db)):
    try:
        usuario = obter_usuario_logado(request, db)
        return templates.TemplateResponse("home.html", {
            "request": request,
            "now": datetime.datetime.now(),
            "usuario_email": usuario.email
        })
    except:
        return RedirectResponse(url="/login")

templates = Jinja2Templates(directory="templates")

@app.get("/registrar", response_class=HTMLResponse)
def exibir_registro(request: Request, db: Session = Depends(get_db)):
    # Bloquear se já existe admin
    admin_existente = db.query(Usuario).filter(Usuario.is_admin == 1).first()
    if admin_existente:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("registrar.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def exibir_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        usuario = obter_usuario_logado(request, db)
        if not usuario.is_admin:
            return RedirectResponse(url="/", status_code=302)

        total_usuarios = admin_service.total_usuarios(db)
        resumo = admin_service.soma_receitas_despesas(db)
        categorias = admin_service.categorias_mais_usadas(db)

        return templates.TemplateResponse("admin/admin.html", {
            "request": request,
            "usuario_email": usuario.email,
            "total_usuarios": total_usuarios,
            "resumo": resumo,
            "categorias": categorias
        })
    except:
        return RedirectResponse(url="/login", status_code=302)

@app.get("/logout")
def logout_redirect():
    return RedirectResponse(url="/api/usuarios/logout")
