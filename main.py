import smtplib
import ssl
from email.message import EmailMessage

# Configurações
email_origem = "xxxx"
senha_app = "xxxxxxx xxx xxxxxxx" # Aquela de 16 dígitos que você gerou
email_destino = "sxxxxxxxxxx"

msg = EmailMessage()
msg['Subject'] = "TE AMO LINDA"
msg['From'] = email_origem
msg['To'] = email_destino
msg.set_content("VOCÊ É SUPER LINDA!")

contexto = ssl.create_default_context()

try:
    print("Conectando ao servidor...")
    # Usando porta 587 com timeout de 15 segundos para não travar
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
        servidor.starttls(context=contexto) # Camada de segurança
        print("Fazendo login...")
        servidor.login(email_origem, senha_app)
        print("Enviando e-mail...")
        servidor.send_message(msg)
    print("✅ E-mail enviado com sucesso!")

except Exception as e:
    print(f"❌ Erro encontrado: {e}")