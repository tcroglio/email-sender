from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from uuid import uuid4

def load_images(caminho):
    with open(caminho, "rb") as f:
        return f.read()

def send_mail(smtp, remetente, assunto, template, dist, tos, ccs):
    cid_logo_colecta = "logo-colecta"
    cid_logo_reckitt = "logo-reckitt"
    cid_logo_esales = "logo-esales"

    html = template.render(
        **dist,
        logo_colecta_cid=cid_logo_colecta,
        logo_reckitt_cid=cid_logo_reckitt,
        logo_esales_cid=cid_logo_esales,
    )

    msg = MIMEMultipart("related")
    corpo = MIMEMultipart("alternative")

    msg["Subject"] = assunto
    msg["From"] = f"Colecta · eSales <{remetente}>"
    msg["To"] = ", ".join(tos)
    msg["Cc"] = ", ".join(ccs)
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    msg["X-Entity-Ref-ID"] = str(uuid4())

    corpo.attach(MIMEText(html, "html", "utf-8"))
    msg.attach(corpo)

    img_colecta = MIMEImage(load_images("assets/logo-colecta-branco.png"))
    img_colecta.add_header("Content-ID", f"<{cid_logo_colecta}>")
    img_colecta.add_header("Content-Disposition", "inline", filename="logo-colecta-branco.png")
    msg.attach(img_colecta)

    img_reckitt = MIMEImage(load_images("assets/logo-reckitt.png"))
    img_reckitt.add_header("Content-ID", f"<{cid_logo_reckitt}>")
    img_reckitt.add_header("Content-Disposition", "inline", filename="logo-reckitt.png")
    msg.attach(img_reckitt)

    img_esales = MIMEImage(load_images("assets/logo-esales.png"))
    img_esales.add_header("Content-ID", f"<{cid_logo_esales}>")
    img_esales.add_header("Content-Disposition", "inline", filename="logo-esales.png")
    msg.attach(img_esales)

    smtp.sendmail(remetente, tos + ccs, msg.as_string())