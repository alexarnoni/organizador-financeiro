import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Adiciona o diretório raiz ao sys.path para importar os módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ⬇️ Importe o Base e os modelos
from database.db import Base
from models.usuario import Usuario
from models.transacao import Transacao

# Configuração do Alembic
config = context.config

# Carrega o arquivo de logging do Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define qual metadata o Alembic usará para detectar mudanças
target_metadata = Base.metadata

# Funções padrão do Alembic
def run_migrations_offline():
    """Executa migrações em modo offline (gera SQL sem conexão com o banco)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Executa migrações conectando ao banco."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Define se roda em modo offline ou online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
