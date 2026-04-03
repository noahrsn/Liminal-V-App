from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Ungültige Anfrage."}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    event_type = data.get("event_type", "").strip()
    date = data.get("date", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "Bitte fülle alle Pflichtfelder aus."}), 400

    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")

    body = (
        "Neue Booking-Anfrage – Liminal V\n"
        "=" * 40 + "\n\n"
        f"Name:        {name}\n"
        f"E-Mail:      {email}\n"
        f"Event-Art:   {event_type or '–'}\n"
        f"Wunschdatum: {date or '–'}\n\n"
        f"Nachricht:\n{message}\n"
    )

    msg = MIMEMultipart()
    msg["From"] = smtp_user or "noreply@liminalv.band"
    msg["To"] = "liminalv.band@gmail.com"
    msg["Reply-To"] = email
    msg["Subject"] = f"Booking-Anfrage von {name}"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        if smtp_user and smtp_pass:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        return jsonify({"success": True})
    except Exception as e:
        print(f"[Email Error] {e}")
        return jsonify({
            "success": False,
            "error": "Nachricht konnte nicht gesendet werden. Bitte schreib uns direkt auf Instagram."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
