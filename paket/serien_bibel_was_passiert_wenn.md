# Serien-Bibel: „Was passiert, wenn …?“

Diese Datei ist die feste Referenz für **jede** neue Folge. Vor jeder Produktion lesen.

## Hauptfigur (unveränderlich, ohne Namen)
- Die Figur hat im Video **keinen Namen**: Sie wird nie beim Namen genannt – nicht in Stimme, Untertiteln, Texten, Caption oder Hashtags. Sie steht für „du“ bzw. führt als Erzähler durchs Video.
- Strichmännchen: schwarze Linien (#16181D, 12 px), runder heller Kopf (#FFF6E6)
- **Blaue Kappe** (#1F6BFF, Schirm #1450C8) mit weißem „?“-Logo vorne – in jeder Szene sichtbar
- **Goldkette** (#F6C445, Schatten #B8860B) um den Hals, vorne auf der Brust, mit rundem Gold-Anhänger mit „?“ – immer getragen, in jeder Szene und jeder Folge
- Darf Emotionen und Posen wechseln, aber nie Form, Farben, Kappe oder Kette
- Nebenfiguren (Mama, Max, Kind …) sind einfache Strichmännchen mit Haaren – **nie** mit blauer Kappe oder Goldkette, damit die Hauptfigur unverwechselbar bleibt
- Code-Referenz: `stick/character.js` (DESIGN, drawChain, drawCap), Bild-Referenz: `hauptfigur_charakter_referenz.png`

## Stil
- Farbenfrohe Verlaufs-Hintergründe, pro Szene eine eigene Farbe, Kreis-Wipe als Übergang
- Oben: Serientitel „WAS PASSIERT, WENN“ (weiß) + Folgentitel (gelb #FFD23F, Schriftgröße passt sich automatisch an), darunter Zeitleiste/Stationen
- Untertitel: Wort für Wort, Inter 900, weiß mit schwarzer Kontur, Schlüsselwörter/Zahlen gelb
- 1080 × 1920, 9:16, 30 fps, 45–60 s
- **TikTok-Sicherheitszone:** Alle Inhalte (Text, Figur, Grafiken, Untertitel) liegen mittig in x ≈ 135–945 und y ≈ 150–1560 (Faktor 0,82 um die Bildmitte). Nichts unter den Like-/Kommentar-/Teilen-Buttons rechts, nichts unter der Beschreibung unten. Nur der Hintergrund füllt das ganze Bild. Vor jeder Folge mit UI-Overlay prüfen.

## Ton
- **Keine Hintergrundmusik**
- Stimme: deutsch, sauber, „gutes Mikro“, leicht jünger (+1,3 Halbtöne), kein Hall; dezente Soundeffekte (Whoosh, Pop, Ding)
- Lautheit: −14 LUFS

## Wiedererkennung (ab Folge 4 v2 – in jeder Folge einsetzen)
- **„?-Moment“:** Beim Aha-Moment zoomt die Kamera auf den „?“-Anhänger der Goldkette, er leuchtet auf (Strahlen + Glanz), dazu das feste Klang-Logo (drei steigende Glockentöne). Das ist das Markenzeichen der Serie.
- **Cold Open:** Die ersten 3 s zeigen einen Moment aus der Mitte/vom Ende (z. B. Wecker-Blitz), erst dann startet die Geschichte. Der Folgentitel wird nicht vorgelesen, er steht nur oben.
- **Loop-Ende:** Die letzte Szene endet auf exakt dem Bild, mit dem die Folge beginnt, und ohne Ausblende – das Video läuft nahtlos weiter.
- **Erst erleben, dann erklären:** Zahlen werden zu Situationen mit Gags (Kaffee ins Müsli, schlafende Abwehr-Wache), nicht zu Infotafeln.
- **Kamera:** kurze Punch-ins aufs Gesicht bei Pointen, Wackeln bei Schreckmomenten; die Bühne bleibt dabei in der Sicherheitszone.
- **Angekündigte Wendung** in der Mitte („… und am Wochenende wird's fies.“), die später aufgelöst wird.
- **Sichtbare Folgen an der Figur** (z. B. Augenringe), solange Form, Farben, Kappe und Kette gleich bleiben.
- **Stimme mit Ausdruck:** pro Satz Tempo/Tonhöhe/Lautstärke (`rate`, `pitch`, `gain`, `gap` in `epXX_script.json`); nachts leise und langsam, bei Schreckmomenten schneller.

## Hashtags
- Fest: #waspassiertwenn + 4–5 Themen-Tags (kein Figuren-Name)

## Inhalt
- Hook in den ersten 3 s, Zeitleisten-Dramaturgie, Aha-Moment gegen Ende, Kommentar-Frage zum Schluss
- Nur geprüfte Fakten (WHO, NHS, Fachgesellschaften), Unsicherheiten kennzeichnen, Quellen einblenden
- Gedankenexperimente als solche kennzeichnen, Rechnungen müssen stimmen

## Folgen
1. Was passiert, wenn du aufhörst zu rauchen? – fertig
2. Was passiert, wenn du jeden Tag 10 € (statt Döner) sparst? – fertig (Annahme 7 % p. a., Disclaimer: keine Anlageberatung)
3. Was passiert, wenn du bei jedem Namen 1 cm schrumpfst? – fertig (Gedankenexperiment; Hauptfigur = „du“, Ende: Freunde markieren)
4. Was passiert, wenn du jeden Tag bis spät in die Nacht wach bist? – fertig, v1 + v2 (v2 = erste Folge mit den Wiedererkennungs-Elementen; Dramaturgie: erst verlockend „Zeit für dich“, Kipp-Punkt Wecker; Quellen AASM/SRS 2015, Van Dongen 2003, Prather 2015, Wittmann 2006)
