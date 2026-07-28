# E-Mail-Setup – liminal-v.de

Ziel: Booking-Anfragen laufen über die eigene Domain statt über die Gmail-Adresse.

```
Veranstalter füllt Formular aus
   → App sendet über Resend    (Absender: noreply@liminal-v.de, DKIM-signiert)
   → an booking@liminal-v.de
   → Cloudflare Email Routing leitet weiter
   → landet in liminalv.band@gmail.com
   → Antwort geht über Gmail "Senden als" wieder als booking@liminal-v.de raus
```

Zwei getrennte Bausteine, weil **Cloudflare Email Routing nur empfangen kann, nicht senden**:

| Aufgabe   | Dienst                  | Kosten                        |
|-----------|-------------------------|-------------------------------|
| Empfangen | Cloudflare Email Routing| kostenlos, unbegrenzt         |
| Senden    | Resend                  | kostenlos, 3.000 Mails/Monat  |

Bei ~5 Gigs im Jahr liegt das Volumen weit im Freikontingent.

---

## Schritt 1 – Cloudflare Email Routing (Empfang)

Cloudflare Dashboard → Domain `liminal-v.de` → **Email** → *Email Routing* → **Get started**.

1. **Destination address** hinzufügen: `liminalv.band@gmail.com`.
   Cloudflare schickt dorthin eine Bestätigungsmail – Link anklicken, sonst geht nichts.
2. **DNS-Records** von Cloudflare automatisch anlegen lassen (Button *Add records automatically*).
   Angelegt werden drei MX-Records auf der Root-Domain und ein SPF-TXT-Record:

   | Typ | Name | Inhalt | Prio |
   |-----|------|--------|------|
   | MX  | `@`  | `route1.mx.cloudflare.net` | 2 |
   | MX  | `@`  | `route2.mx.cloudflare.net` | 41 |
   | MX  | `@`  | `route3.mx.cloudflare.net` | 87 |
   | TXT | `@`  | `v=spf1 include:_spf.mx.cloudflare.net ~all` | – |

3. **Custom addresses** anlegen, alle mit Ziel `liminalv.band@gmail.com`:
   - `booking@liminal-v.de`
   - `info@liminal-v.de`
4. **Catch-all** aktivieren (*Routing rules → Catch-all address* → Action: *Send to*
   → `liminalv.band@gmail.com`). Fängt Tippfehler und Antworten auf `noreply@` ab.

> `noreply@liminal-v.de` braucht **keine** Empfangsregel – die Adresse wird nur zum Senden
> benutzt. Der Catch-all fängt sie ohnehin ab, falls doch jemand darauf antwortet.

**Test:** Von einer beliebigen Adresse eine Mail an `booking@liminal-v.de` schicken – sie muss
innerhalb weniger Sekunden im Gmail-Postfach liegen. Erst weitermachen, wenn das klappt.

## Schritt 2 – Resend (Versand)

1. Account auf [resend.com](https://resend.com) anlegen (Free-Plan reicht).
2. **Domains → Add Domain** → `liminal-v.de`, Region **EU (Ireland)** wählen
   (kürzere Wege, freundlicher für die DSGVO-Argumentation).
3. Resend zeigt drei DNS-Records an. Diese in Cloudflare unter **DNS → Records** eintragen –
   alle als **DNS only** (graue Wolke, nicht orange):

   | Typ | Name | Inhalt | Prio |
   |-----|------|--------|------|
   | MX  | `send` | `feedback-smtp.eu-west-1.amazonses.com` | 10 |
   | TXT | `send` | `v=spf1 include:amazonses.com ~all` | – |
   | TXT | `resend._domainkey` | `p=MIGfMA0GCSq…` (langer DKIM-Key aus dem Dashboard) | – |

   > **Wichtig:** Diese Records liegen auf der Subdomain `send.liminal-v.de`, nicht auf der
   > Root-Domain. Deshalb kollidieren sie **nicht** mit den MX-/SPF-Records aus Schritt 1.
   > Niemals einen zweiten SPF-TXT-Record auf `@` anlegen – pro Name ist nur einer erlaubt,
   > zwei davon machen SPF ungültig.

4. **Verify** klicken. Da die DNS-Zone bei Cloudflare liegt, ist der Status meist in
   1–2 Minuten grün.
5. **API Keys → Create API Key**, Permission *Sending access*, Domain `liminal-v.de`.
   Key beginnt mit `re_` und wird **nur einmal angezeigt** – direkt in die `.env` kopieren.

## Schritt 3 – DMARC (empfohlen)

Ohne DMARC funktioniert der Versand zwar, aber der Record verhindert, dass Fremde in eurem
Namen mailen, und verbessert die Zustellrate. In Cloudflare **DNS → Records**:

| Typ | Name | Inhalt |
|-----|------|--------|
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:info@liminal-v.de; adkim=r; aspf=r` |

`p=none` heißt: nur beobachten, nichts blockieren. Wenn nach ein paar Wochen alles sauber
zustellt, kann man auf `p=quarantine` hochziehen.

## Schritt 4 – `.env` auf der LXC anpassen

```bash
cd /opt/liminal-v
nano .env
```

```env
SMTP_HOST=smtp.resend.com
SMTP_PORT=587
SMTP_USER=resend
SMTP_PASS=re_dein_api_key_hier
MAIL_FROM=Liminal V <noreply@liminal-v.de>
MAIL_TO=booking@liminal-v.de
```

`SMTP_USER` ist wirklich wörtlich `resend` – das ist bei Resend für alle Accounts gleich,
authentifiziert wird über den API-Key im Passwortfeld.

Danach neu starten (eine `.env`-Änderung wird nicht automatisch übernommen):

```bash
docker compose up -d
```

## Schritt 5 – Antworten aus Gmail unter der Domain versenden

Damit eure Antworten an Veranstalter nicht wieder von der Gmail-Adresse kommen:

Gmail → ⚙ → *Alle Einstellungen ansehen* → **Konten und Import** →
*Senden als:* → **Weitere E-Mail-Adresse hinzufügen**

- Name: `Liminal V`
- E-Mail: `booking@liminal-v.de`
- Haken bei „Als Alias behandeln" **entfernen**
- SMTP-Server: `smtp.resend.com`, Port `587`, Benutzer `resend`,
  Passwort = derselbe API-Key, **TLS** (nicht SSL)

Gmail schickt einen Bestätigungscode an `booking@liminal-v.de` – der landet über die
Weiterleitung aus Schritt 1 im selben Postfach. Code eintragen, fertig.
Optional darunter *„Beim Antworten von der Adresse senden, an die die E-Mail ging"* aktivieren.

## Schritt 6 – Endtest

1. Auf `https://www.liminal-v.de` das Kontaktformular mit einer privaten Adresse ausfüllen.
2. Mail muss im Gmail-Postfach ankommen, Absender `noreply@liminal-v.de`.
3. In Gmail die Details der Mail öffnen (▾ neben dem Absender): dort muss
   **SPF: PASS**, **DKIM: PASS** und **DMARC: PASS** stehen. Wenn nicht: DNS-Records
   in Cloudflare gegen das Resend-Dashboard prüfen.
4. Auf die Mail antworten → Reply-To trägt die Adresse des Veranstalters, die Antwort
   geht als `booking@liminal-v.de` raus.
5. Resend-Dashboard → *Logs* zeigt jede gesendete Mail mit Status.

## Wenn etwas schiefgeht

| Symptom | Ursache / Lösung |
|---------|------------------|
| `[Email Error] 535 Authentication failed` | API-Key falsch, abgelaufen oder `SMTP_USER` ist nicht `resend`. |
| `[Email Error] ... domain is not verified` | Domain in Resend noch nicht grün, oder `MAIL_FROM` nutzt eine andere Domain. |
| Mail landet im Spam | DMARC-Record fehlt, oder DKIM steht noch nicht. Header-Analyse siehe Schritt 6.3. |
| Nichts kommt in Gmail an | Destination address in Cloudflare nie bestätigt, oder Routing-Regel fehlt. |
| Zwei SPF-Records auf `@` | Ungültig – es darf nur der Cloudflare-SPF auf der Root stehen. |

**Rollback:** In der `.env` wieder auf Gmail-SMTP zurückstellen
(`SMTP_HOST=smtp.gmail.com`, `SMTP_USER=liminalv.band@gmail.com`, `SMTP_PASS=` App-Passwort,
`MAIL_FROM=liminalv.band@gmail.com`, `MAIL_TO=liminalv.band@gmail.com`) und
`docker compose up -d`. Die DNS-Records können dabei stehen bleiben.
