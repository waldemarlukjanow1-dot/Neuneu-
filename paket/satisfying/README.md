# Satisfying-Loops – das System

Abgeleitet aus dem Referenzvideo „arc squeeze“: Box mit 4 schwingenden Neon-Bögen, Bälle vermehren sich (4 → 279), Zähler darunter, nahtloser Loop.

## Warum solche Videos lange geschaut werden
1. **Sofort Bewegung, keine Einleitung:** Frame 1 läuft schon, kein Text, kein Logo.
2. **Ein Zähler = eine offene Frage:** „Wie hoch geht das?“ / „Schafft es das?“ – das Gehirn will die Auflösung sehen.
3. **Steigerung:** Es wird immer voller, schneller, bunter (Farbe wechselt pro Phase).
4. **Rhythmus + Ton pro Ereignis:** Jede Kollision macht einen Ton → ASMR-Effekt, Bild und Ton passen exakt.
5. **Klarer Payoff:** Am Ende ist etwas *komplett* (voll, perfekt, synchron, befreit).
6. **Nahtloser Loop:** Letztes Bild = erstes Bild. Viele merken den Neustart nicht → Watchtime > 100 %, das pusht der Algorithmus.
7. **Minimaler Look:** Dunkler Hintergrund, Neon-Glow, dünne weiße Linien, nur eine Zahl als Text.

## Die 3 neuen Prinzipien (je 8 s, 60 fps, 1080×1920)
| Datei | Prinzip | Spannung | Payoff |
|---|---|---|---|
| `sync.html` → `out/satisfying_01_sync.mp4` | 16 Punkte auf Ringen, Ring k macht 4+k Runden → Chaos, Sterne, Spiralen | Countdown „bis zur Synchronisation“ | Alle Punkte stehen exakt in einer Linie (Loop-Naht) |
| `galton.html` → `out/satisfying_02_kurve.mp4` | 200 Kugeln fallen durch ein Nagelbrett | Zähler „x / 200“ + gestrichelte Zielkurve: „Passt es genau?“ | Kurve wird grün, „✓ PERFECT“, Boden öffnet sich |
| `rings.html` → `out/satisfying_03_ringe.mp4` | Ball in 10 drehenden Ringen mit Lücke, jede Flucht zerschmettert einen Ring | „rings left“ 10 → 0 | „FREE!“, Ringe bauen sich wieder auf |

## Bauen
```
PAGE=sync.html node render.js x frames all
python3 audio_sat.py sync frames/info.json a.wav     # Töne aus den Ereignissen, kreisförmig gemischt (loopt nahtlos)
```
Danach mit ffmpeg auf −14 LUFS normalisieren und mit 60 fps kodieren.
