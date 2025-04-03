
# 💰 Organizador Financeiro Pessoal

Um sistema completo para gerenciamento de finanças pessoais com autenticação segura, controle multiusuário e visualização interativa de dados com gráficos.

---

## 🚀 Funcionalidades

- ✅ **Autenticação com email e senha**
- ✅ **Multiusuário**: cada usuário vê apenas suas próprias transações
- ✅ **Painel financeiro com CRUD completo** de transações
- ✅ **Filtros por mês e ano**
- ✅ **Gráficos interativos** com Chart.js
- ✅ **Painel de administração** (restrito)
- ✅ **Criação segura de novos administradores**
- ✅ **Proteção de rotas com cookies e verificação real**
- ✅ **Validações robustas com Pydantic (backend) e JS (frontend)**

---

## 📊 Tecnologias Utilizadas

### Backend
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic v2](https://docs.pydantic.dev/)
- [Passlib](https://passlib.readthedocs.io/en/stable/)
- SQLite (local) / PostgreSQL (pronto para produção)

### Frontend
- HTML + CSS + JavaScript
- Bootstrap (no painel de admin)
- Chart.js (gráficos)
- DataTables.js (opcional para tabelas futuras)

---

## 🧪 Como rodar localmente

```bash
git clone https://github.com/seuusuario/organizador-financeiro.git
cd organizador-financeiro/backend
python -m venv venv
venv\Scripts\activate    # No Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🛠️ Configuração do Banco de Dados

- SQLite usado por padrão (`financeiro.db`)
- Migrações com Alembic:
```bash
alembic revision --autogenerate -m "sua mensagem"
alembic upgrade head
```

---

## 🛡️ Segurança

- Login seguro com senha criptografada (`bcrypt`)
- Cookies HTTPOnly com `session_id`
- Todas as rotas protegidas com verificação real de sessão
- Painel de administrador totalmente restrito
- Criação de novos admins feita apenas via painel, por admins já existentes

---

## 👤 Admin (default)

> A criação do primeiro admin é liberada. Depois, **toda criação é protegida** e feita apenas via painel.

---

## 📈 Possíveis melhorias futuras

- Reset de senha via email
- Notificações quando saldo estiver negativo
- Exportação para CSV/PDF
- Modo escuro
- Página de perfil
- Metas de economia por categoria

---

## 📸 Prints (opcional)

> Inclua imagens da interface, gráficos e painel de admin para ilustrar.

---

## 👨‍💻 Autor

**Alexandre Arnoni Nieri de Freitas**  
📍 Praia Grande - SP  
📧 alexandre.anf@gmail.com  
🔗 [GitHub](https://github.com/alexarnoni) | [LinkedIn](https://www.linkedin.com/in/alexandrearnoni)

---

## ⭐ Licença

Este projeto está sob a licença MIT. Livre para usar, contribuir e evoluir.
