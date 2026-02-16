import smtplib
import ssl
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# --- FUNÇÃO DE ENVIO (SEU BACKEND) ---
def disparar_email(destinatario):
    email_origem = "XXX XX XX XXX"
    # LEMBRE-SE: Use a senha de 16 letras do Google aqui
    senha_app = "XXXX XXXXX XXXXX"

    
    msg = EmailMessage()
    msg['Subject'] = "TESTE "
    msg['From'] = email_origem
    msg['To'] = destinatario
    msg.set_content("TESTE!")


    contexto = ssl.create_default_context()
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
            servidor.starttls(context=contexto)
            servidor.login(email_origem, senha_app)
            servidor.send_message(msg)
        return True
    except Exception as e:
        print(f"Erro no servidor SMTP: {e}")
        return False

# --- SERVIDOR WEB NATIVO ---
class Handler(BaseHTTPRequestHandler):
    # GET: Carrega a página ao abrir http://localhost:8000
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        try:
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.wfile.write("Arquivo index.html não encontrado na pasta!".encode())

    # POST: Recebe o e-mail do formulário
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Traduz os dados do formulário (ex: email_destino=teste@gmail.com)
        dados_parseados = urllib.parse.parse_qs(post_data)
        email_cliente = dados_parseados.get('email_destino', [''])[0]

        print(f"Processando envio para: {email_cliente}")
        sucesso = disparar_email(email_cliente)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        if sucesso:
            resposta = "<h1>✅ Enviado com sucesso para " + email_cliente + "!</h1>"
        else:
            resposta = "<h1>❌ Falha no envio. Verifique o console do Python.</h1>"
        
        resposta += '<br><a href="/">Voltar</a>'
        self.wfile.write(resposta.encode())

# Iniciar o servidor
porta = 8000
print(f"Servidor rodando em http://localhost:{porta}")
HTTPServer(("localhost", porta), Handler).serve_forever()