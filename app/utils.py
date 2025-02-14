import qrcode
import os
from flask import current_app
import uuid

def generate_unique_id():
    """Générer un identifiant unique pour les événements et inscriptions"""
    return str(uuid.uuid4())

def generate_qr_code(event_id):
    """Générer un QR code pour un événement spécifique"""
    # Créer l'URL d'inscription (à adapter selon votre domaine)
    registration_url = f"http://localhost:5000/register/{event_id}"
    
    # Générer le QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(registration_url)
    qr.make(fit=True)
    
    # Créer l'image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Chemin de sauvegarde
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{event_id}.png")
    qr_image.save(file_path)
    
    # Retourner le chemin relatif pour l'URL
    return f"/static/qr_codes/{event_id}.png"