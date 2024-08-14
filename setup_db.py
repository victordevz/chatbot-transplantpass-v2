from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import Paciente
from datetime import date

# Configurar o banco de dados SQLite
DATABASE_URL = "sqlite:///hospital.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Criar uma sessão do banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)


dados_ficticios = [
    Paciente 
]

