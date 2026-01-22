import os
from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

band = {
    'name': 'Liminal Horizon',
    'bio': 'Liminal Horizon erkundet Grenzbereiche von Ambient, Post-Rock und elektronischer Textur. Moderne, dichte Arrangements mit atmosphärischen Vocals.',
    'members': ['Aria Müller — Gesang / Synth', 'Jonas Beck — Gitarre', 'Marta Ruiz — Bass', 'Luca Weber — Schlagzeug']
}

tracks = [
    {'title': 'Threshold', 'length': '5:12', 'lyrics': 'Fading lights, I cross the line...'},
    {'title': 'Vessel', 'length': '6:03', 'lyrics': 'Empty rooms and echoing...'},
    {'title': 'Liminal V', 'length': '8:24', 'lyrics': 'At the fifth border we find...'}
]

gallery = [
    'https://images.unsplash.com/photo-1485579149621-3123dd979885?w=1200&auto=format&fit=crop&q=80',
    'https://images.unsplash.com/photo-1506152983158-1f2641c21f1d?w=1200&auto=format&fit=crop&q=80',
    'https://images.unsplash.com/photo-1511376777868-611b54f68947?w=1200&auto=format&fit=crop&q=80',
    'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=1200&auto=format&fit=crop&q=80',
    'https://images.unsplash.com/photo-1506152983158-1f2641c21f1d?w=1200&auto=format&fit=crop&q=80',
    'https://images.unsplash.com/photo-1511376777868-611b54f68947?w=1200&auto=format&fit=crop&q=80'
]

events = [
    {'date': '2025-06-12', 'city': 'Berlin', 'venue': 'Festsaal Kreuzberg', 'info': 'Support: Static Echo'},
    {'date': '2025-07-03', 'city': 'Hamburg', 'venue': 'Molotow', 'info': 'Clubshow, 20:00'},
    {'date': '2025-08-21', 'city': 'Köln', 'venue': 'Live Music Hall', 'info': 'Festival: Northern Lights'}
]

@app.route('/')
def home():
    return render_template('home.html', band=band, latest=tracks[2], tracks=tracks)

@app.route('/liminal-v')
def liminal_v():
    return render_template('liminal_v.html', tracks=tracks, band=band)

@app.route('/galerie')
def galerie():
    return render_template('galerie.html', gallery=gallery)

@app.route('/termine')
def termine():
    return render_template('termine.html', events=events)

@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # In Produktion: E-Mail versenden. Hier nur Loggen.
        print(f'Kontakt von {name} <{email}>: {message}')
        return render_template('message_sent.html', title='Danke', text='Ihre Nachricht wurde gesendet.')
    return render_template('kontakt.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        organizer = request.form.get('organizer')
        date = request.form.get('date')
        details = request.form.get('details')
        print(f'Booking-Anfrage: {organizer} für {date}: {details}')
        return render_template('message_sent.html', title='Booking Anfrage', text='Wir haben Ihre Anfrage erhalten.')
    return render_template('booking.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)