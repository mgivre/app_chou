from flask import Flask
from config import Config
import sqlite3

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialiser la configuration
    config_class.init_app(app)
    
    # Initialiser la base de données
    init_db()
    
    # Enregistrer les routes
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

def init_db():
    conn = sqlite3.connect('instance/events.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            location TEXT,
            max_participants INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id TEXT PRIMARY KEY,
            event_id TEXT,
            participant_name TEXT NOT NULL,
            participant_email TEXT NOT NULL,
            registration_date TEXT,
            FOREIGN KEY (event_id) REFERENCES events (id)
        )
    ''')
    conn.commit()
    conn.close()