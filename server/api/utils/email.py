from pathlib import Path
from schemas.email import  PasswordRequestSchema, LoanRequestSchema
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from config  import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_PORT, MAIL_SERVER, MAIL_FROM_NAME

conf = ConnectionConfig(
    MAIL_USERNAME = MAIL_USERNAME,
    MAIL_PASSWORD = MAIL_PASSWORD,
    MAIL_FROM = MAIL_FROM,
    MAIL_PORT = MAIL_PORT,
    MAIL_SERVER = MAIL_SERVER,
    MAIL_FROM_NAME= MAIL_FROM_NAME,
    MAIL_STARTTLS =True,
    MAIL_SSL_TLS = False,
    TEMPLATE_FOLDER =  Path(__file__).parent / '../templates/email')

async def password_request_mail(email:PasswordRequestSchema):
    message = MessageSchema(
         subject=email.dict().get("subject"),
         recipients=email.dict().get("email"),
         template_body=email.dict().get("body"),
         subtype= MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message, template_name="password_reset.html")
    return {"message" : "email has been sent"}

async def loan_registration_mail(email:LoanRequestSchema):
    message = MessageSchema(
         subject=email.dict().get("subject"),
         recipients=email.dict().get("email"),
         template_body=email.dict().get("body"),
         subtype= MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message, template_name="loan_registration.html")
    return {"message" : "email has been sent"}
