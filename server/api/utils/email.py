from pathlib import Path
from schemas.email import  EmailSchema
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

conf = ConnectionConfig(
    MAIL_USERNAME = "zewdu.anley@email.com",
    MAIL_PASSWORD = "0013B5526C23A34E9E3107BD101D1B6DBF0D",
    MAIL_FROM = "zewdu444@gmail.com",
    MAIL_PORT = 2525,
    MAIL_SERVER = "smtp.elasticemail.com",
    MAIL_FROM_NAME="Zewdu Anley",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    TEMPLATE_FOLDER =  Path(__file__).parent / '../templates/email')

async def password_request_mail(email:EmailSchema):
    message = MessageSchema(
        subject=email.subject,
         recipients=email.dict().get("email"),
         template_body=email.dict().get("body"),
         subtype= MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message, template_name="password_reset.html")
    return {"message" : "email has been sent"}
