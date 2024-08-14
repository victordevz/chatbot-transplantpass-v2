from sqlalchemy.orm import sessionmaker
from app import engine, Paciente

# Criar uma sessão do banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Deletar um paciente específico pelo ID
paciente_id = 1  # Substitua pelo ID do paciente que deseja deletar
paciente_para_deletar = session.query(Paciente).filter_by(id=paciente_id).first()

if paciente_para_deletar:
    session.delete(paciente_para_deletar)
    session.commit()
    print("Paciente deletado com sucesso!")
else:
    print("Paciente não encontrado.")
