from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Paciente

# Configurar o banco de dados SQLite
DATABASE_URL = "sqlite:///hospital.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Verificar se há pacientes cadastrados
pacientes = session.query(Paciente).all()

if not pacientes:
    print("Nenhum paciente cadastrado no banco de dados.")
else:
    print(f"Existem {len(pacientes)} pacientes cadastrados:")
    for paciente in pacientes:
        print(f"ID: {paciente.id}, Nome: {paciente.nome}, Telefone: {paciente.telefone}, Exame Marcado: {paciente.exame_marcado}")
