import sqlite3
from datetime import datetime
from app.utils import generate_unique_id

def get_db_connection():
    conn = sqlite3.connect('instance/events.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_event(title, description, date, location, max_participants):
    event_id = generate_unique_id()
    conn = get_db_connection()
    
    conn.execute('''
        INSERT INTO events (id, title, description, date, location, max_participants)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (event_id, title, description, date, location, max_participants))
    
    conn.commit()
    conn.close()
    return event_id

def get_event(event_id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    conn.close()
    return dict(event) if event else None

def register_participant(event_id, name, email):
    registration_id = generate_unique_id()
    conn = get_db_connection()
    
    # Vérifier si l'événement n'est pas complet
    current_registrations = conn.execute(
        'SELECT COUNT(*) FROM registrations WHERE event_id = ?', (event_id,)
    ).fetchone()[0]
    
    event = get_event(event_id)
    if event and event['max_participants'] > 0 and current_registrations >= event['max_participants']:
        conn.close()
        return None, 'Événement complet'
    
    # Enregistrer l'inscription
    conn.execute('''
        INSERT INTO registrations (id, event_id, participant_name, participant_email, registration_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (registration_id, event_id, name, email, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    return registration_id, 'Inscription réussie'

def get_event_registrations(event_id):
    conn = get_db_connection()
    registrations = conn.execute(
        'SELECT * FROM registrations WHERE event_id = ?', (event_id,)
    ).fetchall()
    conn.close()
    return [dict(reg) for reg in registrations]