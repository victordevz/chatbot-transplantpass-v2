from flask import Flask, request, jsonify, session
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Inicializar a aplicação Flask
app = Flask(__name__)
app.secret_key = "secret_key_for_session"  # Chave secreta para as sessões

# Configurar o banco de dados SQLite
DATABASE_URL = "sqlite:///hospital.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Modelo de Paciente
class Paciente(Base):
    __tablename__ = 'pacientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    telefone = Column(String, unique=True)
    exame_marcado = Column(String)
    exame_realizado = Column(Boolean, default=False)
    resultado_disponivel = Column(Boolean, default=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session_db = Session()

# Rota principal para receber mensagens do WhatsApp
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    numero_usuario = request.form.get("From")
    mensagem_usuario = request.form.get("Body").strip().lower()

    response = MessagingResponse()

    # Verificar se o usuário deseja sair e encerrar a sessão
    if mensagem_usuario == "/exit":
        session.pop("paciente_id", None)
        response.message("Você saiu. Por favor, digite seu ID numérico para validar novamente.")
        return str(response)

    # Verificar se o paciente já está autenticado
    paciente_id = session.get("paciente_id")
    
    if not paciente_id:
        # Tentar interpretar a mensagem do usuário como um ID de paciente
        try:
            paciente_id = int(mensagem_usuario)
            paciente = session_db.query(Paciente).filter_by(id=paciente_id).first()
        except ValueError:
            paciente = None

        if paciente:
            session["paciente_id"] = paciente_id  # Armazenar o ID do paciente na sessão
            response.message(f"Bem-vindo, {paciente.nome}! Como posso ajudar você hoje?")
        else:
            response.message("Por favor, digite o seu ID numérico para validação.")
        
        return str(response)
    
    # Se o paciente já está autenticado, prosseguir com o atendimento
    paciente = session_db.query(Paciente).filter_by(id=paciente_id).first()
    
    if "exame" in mensagem_usuario and "marcado" in mensagem_usuario:
        response.message(f"Seu exame está marcado para {paciente.exame_marcado}.")
    elif "realizei" in mensagem_usuario:
        paciente.exame_realizado = True
        session_db.commit()
        response.message("Obrigado por confirmar que realizou o exame. Seus resultados serão enviados assim que disponíveis.")
    elif "resultado" in mensagem_usuario:
        if paciente.resultado_disponivel:
            response.message("Seu resultado já está disponível. Por favor, acesse o portal do hospital para visualizar.")
        else:
            response.message("Seu resultado ainda não está disponível. Tente novamente mais tarde.")
    elif "atualizar cadastro" in mensagem_usuario:
        response.message("Por favor, envie as informações atualizadas que você gostaria de alterar.")
    else:
        # Saudação inicial com opções
        response.message(
            "Olá! Como posso ajudar você hoje? Aqui estão algumas opções:\n"
            "1. Perguntar sobre o exame marcado (Digite: 'exame marcado')\n"
            "2. Confirmar que realizou o exame (Digite: 'realizei')\n"
            "3. Consultar o resultado do exame (Digite: 'resultado')\n"
            "4. Atualizar cadastro (Digite: 'atualizar cadastro')\n"
            "Por favor, escolha uma das opções acima."
        )
    
    return str(response)

# Iniciar a aplicação Flask
if __name__ == "__main__":
    # Recuperar a porta a partir da variável de ambiente ou usar a porta padrão 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
