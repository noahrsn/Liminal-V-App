# Deployment – Liminal V

Die Website läuft selbst gehostet: Docker-Container (Flask + Gunicorn) auf einer
Debian-12-LXC auf dem Proxmox-Host, erreichbar von außen über den bestehenden
Cloudflare Tunnel `homeserver`. Kein nginx, kein eigenes Zertifikat – TLS macht Cloudflare.

```
Browser → Cloudflare (TLS) → Tunnel "homeserver" (CT 101) → http://<CT-IP>:8080 → Gunicorn
```

| Komponente     | Wert                                   |
|----------------|----------------------------------------|
| LXC            | CT 102 `liminal-web` (Debian 12)       |
| Interner Port  | `8080` (Host → Container `8080:8080`)  |
| Public Hostname| `www.liminal-v.de`                     |
| Startbefehl    | `gunicorn --bind=0.0.0.0:8080 --timeout 600 --workers=2 app:app` |

> **Port prüfen:** Vor dem ersten Start auf der LXC mit `ss -tlnp | grep 8080` sicherstellen,
> dass 8080 dort frei ist. Da die App in einer eigenen LXC läuft, kollidiert sie nicht mit
> Diensten in anderen Containern – nur innerhalb von CT 102 muss der Port frei sein.

---

## 1. Einmalige Einrichtung auf der LXC

Voraussetzung: Docker + Docker Compose Plugin sind in CT 102 installiert.

```bash
# Docker installieren (falls noch nicht vorhanden)
apt update && apt install -y ca-certificates curl git
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
  > /etc/apt/sources.list.d/docker.list
apt update && apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Repository klonen:

```bash
mkdir -p /opt && cd /opt
git clone <REPO-URL> liminal-v
cd liminal-v
```

`.env` anlegen (wird **nicht** committet):

```bash
cp .env.example .env
nano .env      # SMTP_USER = liminalv.band@gmail.com, SMTP_PASS = Gmail-App-Passwort
```

Starten:

```bash
docker compose up -d --build
```

Prüfen:

```bash
docker compose ps
docker compose logs -f web
curl -I http://localhost:8080        # erwartet: HTTP/1.1 200 OK
```

## 2. Einmalig: Cloudflare Tunnel

Im Cloudflare **Zero Trust** Dashboard → *Networks → Tunnels* → Tunnel `homeserver`
→ *Public Hostname* → **Add a public hostname**:

| Feld       | Wert                     |
|------------|--------------------------|
| Subdomain  | `www`                    |
| Domain     | `liminal-v.de`           |
| Path       | *(leer)*                 |
| Type       | `HTTP`                   |
| URL        | `<CT-IP-von-102>:8080`   |

Speichern – der DNS-CNAME wird von Cloudflare automatisch angelegt. Danach ist die Seite
unter `https://www.liminal-v.de` erreichbar.

Optional zusätzlich die Apex-Domain `liminal-v.de` als zweiten Public Hostname auf dasselbe
Ziel legen, oder in Cloudflare unter *Rules → Redirect Rules* eine Weiterleitung
`liminal-v.de → www.liminal-v.de` einrichten.

## 3. Updates ausrollen

```bash
cd /opt/liminal-v
git pull
docker compose up -d --build
```

Alte Images gelegentlich aufräumen: `docker image prune -f`

## 4. Lokal entwickeln (Windows / Arbeitsrechner)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # FLASK_ENV=development setzen
python app.py               # http://localhost:8080
```

Alternativ identisch zur Produktion testen: `docker compose up --build`

## 5. Troubleshooting

| Symptom | Prüfen |
|---------|--------|
| Cloudflare zeigt Error 502 | Läuft der Container? `docker compose ps`, `curl -I http://localhost:8080` auf der LXC. Stimmt die CT-IP im Tunnel-Eintrag? |
| Kontaktformular meldet Fehler | `docker compose logs web` → `[Email Error]`. Meist falsches/abgelaufenes Gmail-App-Passwort in `.env`. Nach `.env`-Änderung: `docker compose up -d` (Neustart nötig). |
| Änderungen nicht sichtbar | `--build` vergessen: `docker compose up -d --build` |
| CT-IP hat sich geändert | Im Proxmox der LXC eine statische IP geben und den Tunnel-Eintrag anpassen. |
