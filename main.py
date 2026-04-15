import json
import smtplib
import os
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from sender import send_mail

load_dotenv()
REMETENTE = os.getenv("SMTP_REMETENTE")
SENHA = os.getenv("SMTP_SENHA")

with open("data/distribuidores.json", encoding="utf-8") as f:
    distribuidores = json.load(f)

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("email_van.html")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(REMETENTE, SENHA)

    for dist in distribuidores:
        tos = dist["contatos"]
        ccs = dist["copia_industria"]
        assunto = f"[{dist['nome_distribuidora']}] Projeto Visibilidade Reckitt: eSales Colecta TESTE ENVIO"

        send_mail(smtp, REMETENTE, assunto, template, dist, tos, ccs)

        print(f"✅ {dist['nome_distribuidora']} — enviado para {len(tos)} contatos")