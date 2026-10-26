# Produktions-Code „Was passiert, wenn …?“

## Dateien
- `character.js` – die Hauptfigur (Kappe, Goldkette, Posen, Gesichter) + Nebenfiguren (`st.extra`). Intern heißt die Zeichenfunktion `drawKappi` – im Video wird nie ein Name genannt.
- `video.html` – Folge 1 (Rauchen) – Grundvorlage: Header, Zeitleiste, Untertitel, Sicherheitszone (`SAFE = 0.82`), Szenen-Wipes
- `video_ep02.html`, `video_ep03.html` – Folge 2 und 3 (gleiche Vorlage, andere Szenen)
- `epXX_scenes.js.txt` – nur der Szenen-Teil jeder Folge (zwischen `// ---------- scene data ----------` und `// ---------- captions ----------` in `video.html` einsetzen → `video_epXX.html`)
- `epXX_script.json` – Sprechtext (`say`) + Untertitel (`cap`, gleiche Wortanzahl, `*` = gelb hervorheben) pro Satz und Szene
- `build_voice.py` – erzeugt Stimme (Piper, Thorsten, +1,3 Halbtöne) und `epXX/timeline.json` mit Wort-Timings
- `audio_stick.py` – Mikro-Klangkette für die Stimme + Soundeffekte (keine Musik); pro Folge ein `if '<szene>' in sc:`-Block
- `render.js` – rendert die Frames per Playwright/Chromium; `sheet.html` + `shot.js` – Charakter-Referenzbild

## Einrichtung (einmalig pro neuer Umgebung)
```bash
pip install piper-tts scipy numpy
npm init -y && npm i playwright@1   # Chromium ist in Claude-Code-Cloud-Sessions meist vorinstalliert
# Stimme (ONNX, CC0):
curl -L -o thorsten.tgz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-thorsten-low.tar.gz
mkdir -p voice && tar xzf thorsten.tgz -C voice
```
Schriften: Inter und Noto Color Emoji müssen installiert sein.

## Neue Folge (Ablauf)
```bash
python3 build_voice.py epXX_script.json voice/de-thorsten-low.onnx epXX     # Stimme + Timeline
# video_epXX.html aus video.html + epXX_scenes.js.txt bauen, dann Testbilder mit TikTok-Overlay:
UI=1 PAGE=video_epXX.html node render.js epXX test 60,300,600
PAGE=video_epXX.html node render.js epXX frames all                          # alle Frames
python3 audio_stick.py epXX                                                  # Ton
ffmpeg -framerate 30 -i frames/f%05d.jpg -i epXX/mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=7" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest folge.mp4
```
