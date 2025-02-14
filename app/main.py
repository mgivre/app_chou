from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.models import create_event, get_event, register_participant, get_event_registrations
from app.utils import generate_qr_code

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/create_event', methods=['GET', 'POST'])
def create_event_route():
    if request.method == 'GET':
        return render_template('event_form.html')
    
    # Traitement du formulaire POST
    data = request.form
    event_id = create_event(
        title=data['title'],
        description=data.get('description', ''),
        date=data['date'],
        location=data.get('location', ''),
        max_participants=int(data.get('max_participants', 0))
    )
    
    # Générer le QR code
    qr_code_url = generate_qr_code(event_id)
    
    return render_template('event_created.html', 
                          event_id=event_id, 
                          qr_code_url=qr_code_url)

@bp.route('/register/<event_id>', methods=['GET', 'POST'])
def register_for_event(event_id):
    event = get_event(event_id)
    if not event:
        flash('Événement non trouvé')
        return redirect(url_for('main.index'))
    
    if request.method == 'GET':
        return render_template('registration_form.html', event=event)
    
    # Traitement du formulaire POST
    data = request.form
    registration_id, message = register_participant(
        event_id=event_id,
        name=data['name'],
        email=data['email']
    )
    
    if not registration_id:
        flash(message)
        return redirect(url_for('main.register_for_event', event_id=event_id))
    
    flash('Inscription réussie !')
    return render_template('registration_success.html', 
                          event=event, 
                          registration_id=registration_id)

@bp.route('/event/<event_id>/registrations')
def view_registrations(event_id):
    event = get_event(event_id)
    if not event:
        flash('Événement non trouvé')
        return redirect(url_for('main.index'))
    
    registrations = get_event_registrations(event_id)
    return render_template('registrations.html', 
                          event=event, 
                          registrations=registrations)