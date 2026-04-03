from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
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

    # Format date to German style if provided
    date_display = "–"
    if date:
        try:
            date_display = datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y")
        except ValueError:
            date_display = date

    event_display = event_type or "–"

    # Plain text fallback
    body_plain = (
        "Neue Booking-Anfrage – Liminal V\n"
        "=" * 40 + "\n\n"
        f"Name:        {name}\n"
        f"E-Mail:      {email}\n"
        f"Event-Art:   {event_display}\n"
        f"Wunschdatum: {date_display}\n\n"
        f"Nachricht:\n{message}\n"
    )

    # HTML email
    body_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#0a0a0e;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0a0e;padding:48px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0"
               style="max-width:600px;width:100%;background:#16161c;border-radius:14px;overflow:hidden;border:1px solid #2a2a36;">

          <!-- HEADER -->
          <tr>
            <td style="background:#111118;padding:44px 48px 36px;text-align:center;border-bottom:1px solid #2a2a36;">
              <div style="font-size:30px;font-weight:800;letter-spacing:0.18em;color:#ffffff;text-transform:uppercase;font-family:'Helvetica Neue',Arial,sans-serif;margin-bottom:10px;">
                LIMINAL V
              </div>
              <table cellpadding="0" cellspacing="0" style="margin:0 auto 14px;">
                <tr>
                  <td style="width:36px;height:2px;background:#9838cc;font-size:0;">&nbsp;</td>
                  <td style="width:8px;">&nbsp;</td>
                  <td style="width:8px;height:8px;background:#9838cc;border-radius:50%;font-size:0;">&nbsp;</td>
                  <td style="width:8px;">&nbsp;</td>
                  <td style="width:36px;height:2px;background:#9838cc;font-size:0;">&nbsp;</td>
                </tr>
              </table>
              <div style="font-size:10px;letter-spacing:0.28em;text-transform:uppercase;color:#9838cc;font-weight:700;">
                Neue Booking-Anfrage
              </div>
            </td>
          </tr>

          <!-- BODY -->
          <tr>
            <td style="padding:40px 48px 32px;">

              <p style="margin:0 0 28px;color:#9a9690;font-size:14px;line-height:1.65;border-left:3px solid #2a2a36;padding-left:14px;">
                Neue Anfrage eingegangen&nbsp;·&nbsp;
                <strong style="color:#dedad3;">{datetime.now().strftime("%d.%m.%Y, %H:%M")} Uhr</strong>
              </p>

              <!-- DETAILS TABLE -->
              <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:32px;">

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #222230;">
                    <span style="display:block;font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#9838cc;font-weight:700;margin-bottom:5px;">Name</span>
                    <span style="font-size:16px;color:#ffffff;font-weight:600;">{name}</span>
                  </td>
                </tr>

                <tr>
                  <td style="padding:14px 0;border-bottom:1px solid #222230;">
                    <span style="display:block;font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#9838cc;font-weight:700;margin-bottom:5px;">E-Mail</span>
                    <span style="font-size:15px;color:#c8c4be;font-weight:400;">{email}</span>
                  </td>
                </tr>

                <tr>
                  <td style="padding:0;border-bottom:1px solid #222230;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                      <tr>
                        <td width="50%" style="padding:14px 16px 14px 0;">
                          <span style="display:block;font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#9838cc;font-weight:700;margin-bottom:5px;">Event-Art</span>
                          <span style="font-size:15px;color:#ffffff;font-weight:500;">{event_display}</span>
                        </td>
                        <td width="50%" style="padding:14px 0;border-left:1px solid #222230;padding-left:16px;">
                          <span style="display:block;font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#9838cc;font-weight:700;margin-bottom:5px;">Wunschdatum</span>
                          <span style="font-size:15px;color:#ffffff;font-weight:500;">{date_display}</span>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>

              </table>

              <!-- MESSAGE BOX -->
              <div style="background:#111118;border-radius:10px;padding:24px;border:1px solid #2a2a36;margin-bottom:36px;position:relative;">
                <div style="font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#9838cc;font-weight:700;margin-bottom:14px;">Nachricht</div>
                <p style="margin:0;color:#c8c4be;font-size:14px;line-height:1.75;white-space:pre-wrap;">{message}</p>
              </div>

              <!-- CTA BUTTON -->
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center">
                    <a href="mailto:{email}?subject=Re%3A%20Deine%20Booking-Anfrage%20bei%20Liminal%20V"
                       style="display:inline-block;background:#9838cc;color:#ffffff;text-decoration:none;font-size:12px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;padding:16px 40px;border-radius:8px;border:2px solid #9838cc;">
                      &#10148;&nbsp; Jetzt antworten
                    </a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background:#0e0e12;padding:28px 48px;border-top:1px solid #2a2a36;text-align:center;">
              <p style="margin:0 0 6px;font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:#9838cc;font-weight:700;">
                Liminal V &nbsp;&middot;&nbsp; Walbeck &nbsp;&middot;&nbsp; Niederrhein
              </p>
              <p style="margin:0;font-size:11px;color:#4a4845;line-height:1.6;">
                Diese E-Mail wurde automatisch &uuml;ber das Kontaktformular auf liminalv.band generiert.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["From"] = smtp_user or "noreply@liminalv.band"
    msg["To"] = "liminalv.band@gmail.com"
    msg["Reply-To"] = email
    msg["Subject"] = f"Booking-Anfrage von {name}"
    msg.attach(MIMEText(body_plain, "plain", "utf-8"))
    msg.attach(MIMEText(body_html, "html", "utf-8"))

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
