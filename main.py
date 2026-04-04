import smtplib
import ssl
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# --- LÓGICA DE ENVIO ATUALIZADA ---
def disparar_email(destinatario, assunto, corpo):
    email_origem = "flaviordaypaa55@gmail.com"
    senha_app = "m**** **** *** ***" 
    
    msg = EmailMessage()
    msg['Subject'] = assunto  # Agora usa o que veio do HTML
    msg['From'] = email_origem
    msg['To'] = destinatario
    msg.set_content(corpo)    # Agora usa o que veio do HTML

    contexto = ssl.create_default_context()
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
            servidor.starttls(context=contexto)
            servidor.login(email_origem, senha_app)
            servidor.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Erro no servidor SMTP: {e}")
        return False

# --- SERVIDOR WEB ATUALIZADO ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # (Seu código do_GET continua igual aqui...)
        if self.path == "/style.css":
            self.servir_arquivo("style.css", "text/css")
        else:
            self.servir_arquivo("index.html", "text/html; charset=utf-8")

    def servir_arquivo(self, nome, tipo):
        try:
            with open(nome, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", tipo)
                self.end_headers()
                self.wfile.write(f.read())
        except:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        dados = urllib.parse.parse_qs(post_data)
        
        # PEGANDO AS NOVAS INFORMAÇÕES DO HTML
        email_cliente = dados.get('email_destino', [''])[0]
        assunto_cliente = dados.get('assunto', [''])[0]
        corpo_cliente = dados.get('corpo', [''])[0]

        print(f"Enviando: {assunto_cliente} para {email_cliente}")
        
        # PASSANDO PARA A FUNÇÃO DE ENVIO
        sucesso = disparar_email(email_cliente, assunto_cliente, corpo_cliente)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        status = "✅ Sucesso!" if sucesso else "❌ Falha no envio."
        cor = "green" if sucesso else "red"
        
        resposta = f"""
        <html>
            <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: {cor};">{status}</h1>
                <p><b>Para:</b> {email_cliente}</p>
                <p><b>Assunto:</b> {assunto_cliente}</p>
                <a href="/">Voltar</a>
            </body>
        </html>
        """
        self.wfile.write(resposta.encode())

if __name__ == "__main__":
    porta = 8000
    print(f"🚀 Servidor rodando em http://localhost:{porta}")
    HTTPServer(("localhost", porta), Handler).serve_forever()