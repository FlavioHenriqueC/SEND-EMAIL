import smtplib
import ssl
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

# --- LÓGICA DE ENVIO ---
def disparar_email(destinatario):
    email_origem = "flaviordaypaa55@gmail.com"
    senha_app = "mtlc brrp jfoh pyfj" 
    
    msg = EmailMessage()
    msg['Subject'] = "TE AMO LINDA"
    msg['From'] = email_origem
    msg['To'] = destinatario
    msg.set_content("VOCÊ É SUPER LINDA!")

    contexto = ssl.create_default_context()
    try:
        print(f"Conectando ao Gmail para enviar para: {destinatario}...")
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
            servidor.starttls(context=contexto)
            servidor.login(email_origem, senha_app)
            servidor.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Erro no servidor SMTP: {e}")
        return False

# --- SERVIDOR WEB ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Rota para o CSS: se o navegador pedir /style.css
        if self.path == "/style.css":
            try:
                with open("style.css", "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-type", "text/css")
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "Arquivo style.css não encontrado")
        
        # Rota para a página principal (HTML)
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            try:
                with open("index.html", "rb") as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.wfile.write("Erro: O arquivo index.html não foi encontrado!".encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        dados = urllib.parse.parse_qs(post_data)
        
        # O formulário HTML deve ter action="/" para cair aqui
        email_cliente = dados.get('email_destino', [''])[0]

        print(f"Solicitação recebida para: {email_cliente}")
        sucesso = disparar_email(email_cliente)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        status = "✅ Sucesso!" if sucesso else "❌ Falha no envio."
        cor = "green" if sucesso else "red"
        
        resposta = f"""
        <html>
            <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: {cor};">{status}</h1>
                <p>Destinatário: {email_cliente}</p>
                <a href="/">Voltar</a>
            </body>
        </html>
        """
        self.wfile.write(resposta.encode())

if __name__ == "__main__":
    porta = 8000
    print(f"🚀 Servidor rodando em http://localhost:{porta}")
    HTTPServer(("localhost", porta), Handler).serve_forever()