import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-secrete-difficile-a-deviner'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'events.db')
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'qr_codes')
    
    @staticmethod
    def init_app(app):
        # Assurez-vous que le dossier de stockage des QR codes existe
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)