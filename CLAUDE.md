# Projekt: Liminal V - Band Website

## 1. Projektübersicht
Wir bauen die offizielle Website für die Coverband "Liminal V". Die Band spielt Partymusik (aber nicht ausschließlich) und tritt ca. 4-5 Mal im Jahr auf, hauptsächlich in Walbeck und Umgebung. Die Zielgruppe sind Veranstalter von Schützenfesten, Dorffesten, Open-Air-Festivals (z. B. Waldfreibad) und Afterwork-Partys (z. B. Schloss Walbeck).

## 2. Tech-Stack & Architektur
- **Frontend:** Reines HTML5, CSS3 und Vanilla JavaScript für eine schnelle und simple Oberfläche.
- **Backend:** Ein leichtgewichtiges Python-Backend (z. B. Flask oder FastAPI), um dynamische Anfragen zu verarbeiten.
- **Deployment:** Die Website muss sowohl lokal per `localhost` lauffähig und testbar sein als auch auf einer **Azure Web App** deployt werden können. Der Code und die Konfiguration (z. B. `requirements.txt`, Startbefehl) müssen Azure-kompatibel sein.
- **Struktur:** Sauberer, semantischer HTML-Aufbau.
- **Styling:** Verwende natives CSS. Lege die primären Farben als CSS-Variablen (`:root`) an, damit sie leicht anpassbar sind.
- **Formular-Verarbeitung:** Implementiere im Python-Backend eine sichere Logik (z. B. via `smtplib`), die die Eingaben aus dem Kontaktformular entgegennimmt und direkt als E-Mail an liminalv.band@gmail.com sendet.

## 3. Brand & Content Guidelines
- **Bandname:** Liminal V
- **Besetzung:** 
    - Sängerin
    - Rhythmus-Gitarrist (inkl. Background-Gesang)
    - Lead-Gitarrist
    - Bassist
    - Drummer
- **Tonalität der Texte:** Locker, sympathisch, energiegeladen und per "Du". Wir sind bodenständig und lokal verankert, liefern aber professionell ab.
- **Booking-Konditionen:** - Gage: 250 € pro Stunde
    - Technik-Pauschale: +100 € (wenn wir eigene PA/Technik mitbringen und aufbauen)
- **Social Media:** Es gibt ausschließlich Instagram. Bitte binde das Instagram-Logo gut sichtbar ein und verlinke es. Andere Plattformen (Facebook, TikTok etc.) existieren nicht und sollen auch nicht als Platzhalter auftauchen.
- **Kontakt:** Alle Anfragen laufen über das Kontaktformular an liminalv.band@gmail.com.

## 4. Design & UI/UX Vorgaben
- **Rolle:** Agiere als erfahrener UI/UX-Designer und Full-Stack-Entwickler. Das Design muss **maximal professionell** wirken, modern sein und die Live-Energie der Band transportieren.
- **Design-Orientierung:** Der strukturelle Aufbau orientiert sich an der Website von **Kontrollverlust** (kontrollverlust-band.de) – d. h. klare Sektionen, eine feste Navigation, starke Hero-Bilder, klare Typografie. **Farblich wird die Kontrollverlust-Website nicht übernommen.**
- **Farbschema & Vibe:**
    - Das Farbschema soll sich **nicht mit dem Bandlogo beißen** und im **gleichen Farbstil** wie das Logo sein (abgestimmt auf den Stil des Logos, z. B. dunkle, edle Töne mit passenden Akzentfarben).
    - Keine konkrete Farbvorgabe – wähle als Designer eigenständig eine professionell wirkende, zum Logo passende Palette.
    - Die Gesamtwirkung der Seite soll ausgewogen sein (weder reiner Dark Mode noch komplett grell/hell).
- **Layout-Regeln:** Mobile-First-Ansatz ist zwingend erforderlich. Nutze Whitespace für eine saubere Optik.
- **Navigation & Sektionen:** Die Website hat folgende Navigationspunkte (Reihenfolge kann von Claude nach UX-Gesichtspunkten optimiert werden):
    - **Über uns** – Bandgeschichte und Vorstellung der fünf Mitglieder
    - **Beispiel-Setlist** – Beispielhafte Setlist eines vergangenen Gigs
    - **Gigs** – Kommende Termine und vergangene Highlights (Gig-Historie)
    - **Galerie** – Visuell ansprechende Bildergalerie von Auftritten
    - **Kontakt / Buchung** – Kontaktformular für Booking-Anfragen (per E-Mail an liminalv.band@gmail.com)

## 5. Claude Code Workflow-Regeln
- **Planung zuerst:** Bevor du Code generierst, schlage mir den Seitenaufbau, die Navigationsreihenfolge und die Struktur des Python-Backends vor. Erstelle erst Code, wenn ich zustimme.
- **Farben:** Kein Farbauslesen aus dem Logo erforderlich. Wähle eigenständig eine professionelle, zum Logo passende Farbpalette und definiere sie als CSS-Variablen. Das Logo wird ggf. separat zur Verfügung gestellt.
- **Micro-Interactions:** Baue in das CSS weiche Hover-Effekte für Buttons, Links, Bilder und Galerie-Elemente ein (z. B. `transition: all 0.3s ease;`).
- **Texte generieren:** Verwende kein "Lorem Ipsum". Schreibe direkt passende, lockere und authentische Entwürfe für alle Sektionen (inkl. einer ausgedachten Biografie/Gründungsgeschichte und einer Beispiel-Setlist, die ich dann später nur noch mit den echten Fakten anpassen muss).
- **Azure-Kompatibilität:** Stelle sicher, dass der Code lokal per `python app.py` oder `flask run` startbar ist und gleichzeitig Azure-ready ist (korrekter `startup`-Befehl, `requirements.txt`, ggf. `web.config` oder `Procfile`).