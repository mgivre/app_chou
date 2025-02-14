from flask import Flask, render_template, request, jsonify
import qrcode
from datetime import datetime
import sqlite3
import json
import uuid

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('events.db')
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

def generate_qr_code(event_id):
    # Créer l'URL d'inscription
    registration_url = f"http://votre-domaine.com/register/{event_id}"
    
    # Générer le QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(registration_url)
    qr.make(fit=True)
    
    # Créer l'image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save(f"static/qr_codes/{event_id}.png")
    return f"/static/qr_codes/{event_id}.png"

@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.json
    event_id = str(uuid.uuid4())
    
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (id, title, description, date, location, max_participants)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        event_id,
        data['title'],
        data.get('description', ''),
        data['date'],
        data.get('location', ''),
        data.get('max_participants', 0)
    ))
    conn.commit()
    conn.close()
    
    # Générer le QR code pour l'événement
    qr_code_url = generate_qr_code(event_id)
    
    return jsonify({
        'event_id': event_id,
        'qr_code_url': qr_code_url
    })

@app.route('/register/<event_id>', methods=['GET', 'POST'])
def register_for_event(event_id):
    if request.method == 'GET':
        # Afficher le formulaire d'inscription
        conn = sqlite3.connect('events.db')
        c = conn.cursor()
        c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
        event = c.fetchone()
        conn.close()
        
        if event:
            return render_template('registration_form.html', event=event)
        return "Événement non trouvé", 404
    
    elif request.method == 'POST':
        # Traiter l'inscription
        data = request.json
        registration_id = str(uuid.uuid4())
        
        conn = sqlite3.connect('events.db')
        c = conn.cursor()
        
        # Vérifier si l'événement n'est pas complet
        c.execute('''
            SELECT COUNT(*) from registrations WHERE event_id = ?
        ''', (event_id,))
        current_registrations = c.fetchone()[0]
        
        c.execute('SELECT max_participants FROM events WHERE id = ?', (event_id,))
        max_participants = c.fetchone()[0]
        
        if max_participants > 0 and current_registrations >= max_participants:
            conn.close()
            return jsonify({'error': 'Événement complet'}), 400
        
        # Enregistrer l'inscription
        c.execute('''
            INSERT INTO registrations (id, event_id, participant_name, participant_email, registration_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            registration_id,
            event_id,
            data['name'],
            data['email'],
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'registration_id': registration_id,
            'message': 'Inscription réussie'
        })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)