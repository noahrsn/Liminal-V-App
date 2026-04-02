import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    event_date = (data.get("event_date") or "").strip()
    location = (data.get("location") or "").strip()
    message = (data.get("message") or "").strip()

    if not all([name, email, message]):
        return jsonify({"success": False, "error": "Bitte füll alle Pflichtfelder aus."}), 400

    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"success": False, "error": "Bitte gib eine gültige E-Mail-Adresse an."}), 400

    try:
        _send_mail(
            recipient=app.config["MAIL_RECIPIENT"],
            subject=f"Neue Booking-Anfrage von {name}",
            body=_build_mail_body(name, email, phone, event_date, location, message),
        )
        return jsonify({"success": True, "message": "Deine Anfrage ist angekommen – wir melden uns bald!"})
    except Exception as exc:
        logger.error("Mail send failed: %s", exc)
        return jsonify({"success": False, "error": "Beim Senden ist ein Fehler aufgetreten. Bitte versuch es später nochmal."}), 500


def _build_mail_body(name, email, phone, event_date, location, message):
    return f"""Neue Booking-Anfrage über die Liminal V Website
{"=" * 50}
Name:           {name}
E-Mail:         {email}
Telefon:        {phone or "–"}
Event-Datum:    {event_date or "–"}
Veranstaltungsort: {location or "–"}

Nachricht:
{message}
{"=" * 50}
"""


def _send_mail(recipient, subject, body):
    username = app.config["MAIL_USERNAME"]
    password = app.config["MAIL_PASSWORD"]

    if not username or not password:
        raise RuntimeError("Mail credentials not configured (MAIL_USERNAME / MAIL_PASSWORD missing).")

    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]) as server:
        server.ehlo()
        if app.config["MAIL_USE_TLS"]:
            server.starttls()
            server.ehlo()
        server.login(username, password)
        server.sendmail(username, recipient, msg.as_string())


if __name__ == "__main__":
    app.run(debug=False)
