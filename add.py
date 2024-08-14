from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import Paciente

# Configurar o banco de dados SQLite
DATABASE_URL = "sqlite:///hospital.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Criar uma sessão do banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Adicionar vários pacientes fictícios
pacientes = [
    Paciente(
        nome="Victor Silva",
        telefone="+5581996005600",
        exame_marcado="2024-08-20",
        exame_realizado=True,
        resultado_disponivel=False
    ),
    Paciente(
        nome="João Santos",
        telefone="+5511987654322",
        exame_marcado="2024-09-15",
        exame_realizado=False,
        resultado_disponivel=False
    ),
    Paciente(
        nome="Ana Costa",
        telefone="+5511987654323",
        exame_marcado="2024-10-10",
        exame_realizado=False,
        resultado_disponivel=False
    )
]

# Adicionar todos os pacientes à sessão
session.add_all(pacientes)
session.commit()

print("Pacientes cadastrados com sucesso!")
