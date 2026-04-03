# Projekt: Liminal V - Band Website

## 1. Projektübersicht
Wir bauen die offizielle Website für die Coverband "Liminal V". Die Band spielt Partymusik (aber nicht ausschließlich) und tritt ca. 4-5 Mal im Jahr auf, hauptsächlich in Walbeck und Umgebung. Die Zielgruppe sind Veranstalter von Schützenfesten, Dorffesten, Open-Air-Festivals (z. B. Waldfreibad) und Afterwork-Partys (z. B. Schloss Walbeck).

## 2. Tech-Stack & Architektur
- **Frontend:** Reines HTML5, CSS3 und Vanilla JavaScript für eine schnelle und simple Oberfläche.
- **Backend:** Ein leichtgewichtiges Python-Backend (z. B. Flask oder FastAPI), um dynamische Anfragen zu verarbeiten.
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
- **Rolle:** Agiere als erfahrener UI/UX-Designer und Full-Stack-Entwickler. Das Design muss professionell wirken und die Live-Energie der Band transportieren.
- **Farbschema & Vibe:** - Die Basis-Farben stammen aus dem Bandlogo (Dunkelblau und Weiß).
    - Die Gesamtwirkung der Seite soll ausgewogen sein (weder reiner Dark Mode noch komplett grell/hell). Nutze neutrale Zwischentöne für Hintergründe, um Kontraste zu schaffen.
- **Layout-Regeln:** Mobile-First-Ansatz ist zwingend erforderlich. Nutze Whitespace für eine saubere Optik.
- **Pflicht-Inhalte (Sektionen):**
    - **Biografie & Vorstellung:** Eine kombinierte Sektion, in der die Bandgeschichte (Wer sind wir? Seit wann gibt es uns?) erzählt wird und die fünf Bandmitglieder sympathisch vorgestellt werden.
    - **Galerie:** Eine visuell ansprechende Sektion mit Bildern von vergangenen Auftritten.
    - **Setlist:** Eine beispielhafte Setlist von einem vergangenen Gig, um das Repertoire zu zeigen.
    - **Gigs:** Eine Übersicht der nächsten Termine sowie eine Liste von vergangenen Highlights (Gig-Historie).
    - **Kontakt:** Ein Formular für Booking-Anfragen (an das Python-Backend geknüpft).

## 5. Claude Code Workflow-Regeln
- **Planung zuerst:** Bevor du Code generierst, schlage mir die genauen Menüpunkte, den Seitenaufbau und die Struktur des Python-Backends vor. Erstelle erst Code, wenn ich zustimme.
- **Farben auslesen:** Ich werde dir das Logo als Bild zur Verfügung stellen. Bitte extrahiere daraus die passenden Hex-Codes für das CSS.
- **Micro-Interactions:** Baue in das CSS weiche Hover-Effekte für Buttons, Links, Bilder und Galerie-Elemente ein (z. B. `transition: all 0.3s ease;`).
- **Texte generieren:** Verwende kein "Lorem Ipsum". Schreibe direkt passende, lockere und authentische Entwürfe für alle Sektionen (inkl. einer ausgedachten Biografie/Gründungsgeschichte und einer Beispiel-Setlist, die ich dann später nur noch mit den echten Fakten anpassen muss).