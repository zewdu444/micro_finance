from dotenv import load_dotenv
import os

load_dotenv()
# SMTP CONFIGURATION
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER  = os.getenv("MAIL_SERVER")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
    # Add other fields as needed

# JWT CONFIGURATION
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM  = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


# DATABASE CONFIGURATION
SQLALCHEMY_DATABASE_URL =  os.getenv("SQLALCHEMY_DATABASE_URL")
