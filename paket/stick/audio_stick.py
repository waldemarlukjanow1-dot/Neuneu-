"""Series soundtrack: light, upbeat background (marimba/pluck, soft drums) + SFX on scene events + voice with ducking.
usage: python3 audio_stick.py <ep_dir>"""
import json, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt

ep = sys.argv[1]
TL = json.load(open(f'{ep}/timeline.json'))
SR = 44100; T = TL['duration']; N = int(T * SR); t = np.arange(N) / SR
rng = np.random.default_rng(7)
def sos(k, f, o=2): return butter(o, f, k, fs=SR, output='sos')
def lp(x, f): return sosfilt(sos('lowpass', f), x)
def hp(x, f): return sosfilt(sos('highpass', f), x)
def bp(x, a, b): return sosfilt(sos('bandpass', [a, b]), x)
def env(n, a, d): x = np.arange(n) / SR; e = np.exp(-x / d); k = max(1, int(a * SR)); e[:k] *= np.linspace(0, 1, k); return e
def place(buf, s, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(s)); buf[i:j] += s[:j - i] * g
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)

# ---------- music: 100 bpm, C - G - Am - F ----------
bpm = 100; beat = 60 / bpm; bar = 4 * beat
chords = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]
music = np.zeros(N)
def marimba(f, d=0.5):
    n = int(d * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * x) + 0.25 * np.sin(2 * np.pi * f * 4 * x) * np.exp(-x * 30)) * np.exp(-x * 9)
pattern = [0, 2, 1, 2, 0, 2, 1, 0]   # chord tone index per 8th
for k in range(int(T / (beat / 2)) + 1):
    tt = k * beat / 2; b = int(tt / bar); ch = chords[b % 4]
    m = ch[pattern[k % 8]] + 12
    place(music, marimba(mtof(m)), tt, 0.22 if k % 2 == 0 else 0.15)
for b in range(int(T / bar) + 1):
    tb = b * bar; ch = chords[b % 4]
    n = int(bar * SR); x = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * mtof(m) * x) + 0.3 * np.sin(2 * np.pi * mtof(m) * 2.003 * x) for m in ch)
    place(music, lp(pad, 1200) * np.minimum(1, x / 0.3) * np.minimum(1, (bar - x) / 0.3) * 0.05, tb)
    bass = np.sin(2 * np.pi * mtof(ch[0] - 24) * x) * np.exp(-((x % beat) / beat) * 2.5)
    place(music, bass * 0.22, tb)
kick_n = int(0.3 * SR); kx = np.arange(kick_n) / SR
kick = np.sin(2 * np.pi * np.cumsum(50 + 90 * np.exp(-kx * 35)) / SR) * np.exp(-kx * 12)
shaker = hp(rng.standard_normal(int(0.07 * SR)), 6000) * env(int(0.07 * SR), 0.01, 0.02)
snap = bp(rng.standard_normal(int(0.12 * SR)), 1500, 5000) * env(int(0.12 * SR), 0.001, 0.03)
for k in range(int(T / beat) + 1):
    tt = k * beat
    if tt > 3.4:   # drums start after the hook
        place(music, kick, tt, 0.45 if k % 2 == 0 else 0.25)
        if k % 2 == 1: place(music, snap, tt, 0.25)
    for s8 in (0, 0.5): place(music, shaker, tt + s8 * beat, 0.12)

# ---------- SFX ----------
fx = np.zeros(N)
def whoosh(d=0.45):
    n = int(d * SR); x = np.arange(n) / SR; nz = rng.standard_normal(n)
    sweep = np.array([0.0]); return bp(nz, 400, 4000) * np.sin(np.pi * x / d) ** 2
def popsfx():
    n = int(0.12 * SR); x = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(500 + 900 * x / 0.12) / SR) * env(n, 0.002, 0.04)
def ding(f=1320):
    n = int(1.0 * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(2 * np.pi * f * 2.76 * x)) * np.exp(-x * 4)
def tick():
    n = int(0.03 * SR); return hp(rng.standard_normal(n), 3000) * env(n, 0.0005, 0.006)
def heartbeat():
    n = int(0.18 * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * 55 * x) * np.exp(-x * 25)
def sparkle():
    out = np.zeros(int(0.8 * SR))
    for k in range(6):
        n = int(0.25 * SR); x = np.arange(n) / SR; f = 2000 + 400 * k
        s = np.sin(2 * np.pi * f * x) * np.exp(-x * 18); out[int(k * 0.07 * SR):int(k * 0.07 * SR) + n] += s
    return out
def crack():
    n = int(0.15 * SR); return bp(rng.standard_normal(n), 800, 6000) * env(n, 0.0005, 0.02)
def cough():
    n = int(0.35 * SR); x = np.arange(n) / SR; return bp(rng.standard_normal(n), 250, 1800) * np.exp(-x * 10) * (1 + 0.5 * np.sin(2 * np.pi * 9 * x))
def drumhit():
    n = int(0.8 * SR); x = np.arange(n) / SR
    return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(45 + 120 * np.exp(-x * 20)) / SR) * np.exp(-x * 5)) + bp(rng.standard_normal(n), 2000, 8000) * np.exp(-x * 20) * 0.3
def confetti_pop():
    return np.concatenate([crack() * 1.2, np.zeros(int(0.05 * SR))]) + 0
sc = {s['id']: s for s in TL['scenes']}
ph = {}
for p in TL['phrases']: ph.setdefault(p['scene'], []).append(p)
for s in TL['scenes'][1:]: place(fx, whoosh(), s['start'] - 0.05, 0.35)
if 'min20' in sc:  # Folge 01
    h = sc['hook']; D = h['end'] - h['start']
    place(fx, popsfx(), h['start'] + 0.15, 0.4); place(fx, crack(), h['start'] + D - 1.0, 0.8); place(fx, drumhit(), h['start'] + D - 0.9, 0.5)
    s = sc['min20']
    for k in range(10): place(fx, tick(), s['start'] + 0.2 + k * 0.17, 0.5)
    for k in range(6): place(fx, heartbeat(), s['start'] + 1.0 + k * 0.8, 0.6); place(fx, heartbeat(), s['start'] + 1.18 + k * 0.8, 0.4)
    place(fx, popsfx(), s['start'] + 1.3, 0.3)
    s = sc['h12']; place(fx, popsfx(), s['start'] + 1.0, 0.3); place(fx, ding(1560), ph['h12'][1]['start'] + 0.1, 0.18)
    s = sc['d2']; place(fx, sparkle(), s['start'] + 0.5, 0.25); place(fx, popsfx(), s['start'] + 0.5, 0.3); place(fx, popsfx(), s['start'] + 1.1, 0.3)
    s = sc['crave']; place(fx, drumhit(), s['start'] + 0.7, 0.35); place(fx, sparkle(), ph['crave'][1]['start'] + 0.3, 0.3); place(fx, ding(), ph['crave'][1]['start'] + 0.5, 0.2)
    s = sc['w12']; place(fx, popsfx(), s['start'] + 0.1, 0.3)
    s = sc['m9']; place(fx, cough(), s['start'] + 0.15, 0.35); place(fx, cough(), s['start'] + 0.55, 0.3); place(fx, sparkle(), s['start'] + 1.6, 0.2)
    s = sc['y1']; place(fx, drumhit(), s['start'] + 0.05, 0.6); p2 = ph['y1'][1]['start']; place(fx, confetti_pop(), p2 + 2.0, 0.6); place(fx, ding(1760), p2 + 2.0, 0.25)
    s = sc['y10']; place(fx, drumhit(), s['start'] + 0.05, 0.5); place(fx, ding(1320), s['start'] + 2.6, 0.22)
    s = sc['outro']; place(fx, popsfx(), s['start'] + 1.2, 0.35); place(fx, ding(1980), ph['outro'][1]['start'] + 0.1, 0.25)
if 'etf' in sc:  # Folge 02
    def coin_sfx():
        n = int(0.5 * SR); x = np.arange(n) / SR
        return (np.sin(2 * np.pi * 2600 * x) + 0.6 * np.sin(2 * np.pi * 3900 * x)) * np.exp(-x * 9) * (1 + 0.3 * np.sin(2 * np.pi * 30 * x))
    h = sc['hook']; D = h['end'] - h['start']
    place(fx, popsfx(), h['start'] + 0.3, 0.35); place(fx, whoosh(0.6), h['start'] + D - 1.3, 0.4); place(fx, coin_sfx(), h['start'] + D - 0.4, 0.4)
    s = sc['month']
    for k in range(10): place(fx, popsfx(), s['start'] + 0.5 + k * 0.28, 0.12)
    place(fx, ding(1560), ph['month'][1]['start'] + 0.1, 0.2)
    s = sc['year']
    for k in range(8): place(fx, coin_sfx(), s['start'] + 0.3 + k * 0.22, 0.12)
    place(fx, popsfx(), ph['year'][1]['start'] + 0.1, 0.3); place(fx, popsfx(), ph['year'][1]['start'] + 0.6, 0.3)
    s = sc['y5']
    for k in range(6): place(fx, coin_sfx(), s['start'] + 0.4 + k * 0.6, 0.15)
    s = sc['etf']; place(fx, drumhit(), s['start'] + 0.05, 0.5); place(fx, sparkle(), ph['etf'][2]['start'] + 0.2, 0.25); place(fx, popsfx(), ph['etf'][3]['start'] + 0.1, 0.3)
    for sid in ('y10', 'y20'): place(fx, popsfx(), sc[sid]['start'] + 0.1, 0.3); place(fx, ding(1320), sc[sid]['start'] + 1.3, 0.18)
    s = sc['y40']; place(fx, drumhit(), ph['y40'][1]['start'] + 0.05, 0.6); place(fx, confetti_pop(), ph['y40'][1]['start'] + 0.6, 0.5)
    for k in range(10): place(fx, coin_sfx(), ph['y40'][1]['start'] + 0.6 + k * 0.15, 0.1)
    s = sc['outro']; place(fx, popsfx(), s['start'] + 0.4, 0.35); place(fx, ding(1980), ph['outro'][1]['start'] + 0.1, 0.25)

if 'mama' in sc:  # Folge 03
    def bloop():   # descending "shrink" sound
        n = int(0.32 * SR); x = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-x * 7) + 180) / SR) * env(n, 0.003, 0.12)
    def crowd(d=2.5):
        n = int(d * SR); x = np.arange(n) / SR
        return bp(rng.standard_normal(n), 300, 3000) * np.sin(np.pi * x / d) ** 0.7
    h = sc['hook']
    for k, hh in enumerate([1.0, 1.9, 2.8, 3.7]): place(fx, popsfx(), h['start'] + hh, 0.3); place(fx, bloop(), h['start'] + hh + 0.05, 0.45)
    for p in ph['intro']:
        for w in p['words']:
            if w['say'].startswith('Namen'): place(fx, bloop(), w['t0'] + 0.15, 0.55)
    tw = sc['you']['start']
    for p in ph['you']:
        for w in p['words']:
            if w['say'].startswith('weg'): place(fx, crack(), w['t0'], 0.6); place(fx, whoosh(0.4), w['t0'], 0.4)
    def wt(sid, prefix):
        for p in ph[sid]:
            for w in p['words']:
                if w['say'].startswith(prefix): return w['t0']
    tm = wt('school', 'Max')
    for d in (0, 1.3, 2.1): place(fx, popsfx(), tm + d, 0.35); place(fx, bloop(), tm + d + 0.05, 0.4)
    s = sc['mama']
    for k in range(14): place(fx, popsfx(), s['start'] + 0.6 + k * 0.28, 0.12)
    place(fx, ding(1320), ph['mama'][1]['start'] + 0.2, 0.2)
    tr = wt('star', 'rufen'); place(fx, crowd(2.2), tr - 1.4, 0.35); place(fx, drumhit(), tr, 0.6); place(fx, whoosh(0.5), tr + 0.05, 0.5)
    s = sc['rescue']; place(fx, sparkle(), s['start'] + 0.3, 0.25)
    s = sc['outro']; place(fx, popsfx(), s['start'] + 0.3, 0.35)

if 'jetlag' in sc:  # Folge 04
    def wt(sid, prefix):
        for p in ph[sid]:
            for w in p['words']:
                if w['say'].startswith(prefix): return w['t0']
    def ring(d=1.8):
        n = int(d * SR); x = np.arange(n) / SR
        gate = (np.sin(2 * np.pi * 22 * x) > 0).astype(float)
        return (np.sin(2 * np.pi * 2400 * x) + 0.6 * np.sin(2 * np.pi * 3150 * x)) * gate * np.minimum(1, x / 0.01) * np.minimum(1, (d - x) / 0.15)
    def bloop():
        n = int(0.32 * SR); x = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-x * 7) + 180) / SR) * env(n, 0.003, 0.12)
    h = sc['hook']
    for k in range(10): place(fx, tick(), h['start'] + 0.2 + k * 0.32, 0.35)
    place(fx, popsfx(), h['start'] + 0.4, 0.3)
    s = sc['n22']
    for k in range(3): place(fx, popsfx(), s['start'] + 0.3 + k * 0.25, 0.25)
    tk = wt('n22', 'Keiner')
    for k in range(3): place(fx, whoosh(0.3), tk + 0.3 + k * 0.15, 0.25)
    place(fx, ding(1320), tk + 1.2, 0.18)
    tf = wt('n0', 'Folge')
    for k in range(3): place(fx, tick(), tf + k * 0.8, 0.6)
    place(fx, ding(1760), tf + 2.4, 0.15)
    tfr = wt('n0', 'Freiheit'); place(fx, sparkle(), tfr, 0.3); place(fx, confetti_pop(), tfr, 0.4)
    place(fx, popsfx(), wt('n2', 'Namen'), 0.3); place(fx, sparkle(), wt('n2', 'zurück') - 0.2, 0.22)
    s = sc['alarm']; place(fx, drumhit(), s['start'] + 0.05, 0.5); place(fx, ring(min(1.8, ph['alarm'][1]['start'] - s['start'] - 0.2)), s['start'] + 0.1, 0.22)
    place(fx, bloop(), wt('alarm', 'fünf'), 0.45)
    s = sc['w2']
    for k in range(13): place(fx, tick(), s['start'] + 0.5 + k * 0.25, 0.4)
    place(fx, bloop(), wt('w2', 'durchgemachten'), 0.45); place(fx, popsfx(), ph['w2'][1]['start'], 0.3)
    s = sc['jetlag']; place(fx, whoosh(0.9), s['start'] + 0.6, 0.3); place(fx, whoosh(0.9), s['start'] + 2.4, 0.3); place(fx, popsfx(), wt('jetlag', 'Jetlag') - 0.3, 0.3)
    s = sc['body']; place(fx, cough(), s['start'] + 0.15, 0.35); place(fx, cough(), s['start'] + 0.6, 0.3)
    for k in range(4): place(fx, popsfx(), ph['body'][0]['start'] + 2.65 + k * 0.25, 0.2)
    place(fx, drumhit(), wt('aha', 'leihst') - 0.1, 0.45)
    s = sc['outro']; place(fx, popsfx(), s['start'] + 0.3, 0.35); place(fx, ding(1980), s['start'] + 1.4, 0.2)

if 'choice' in sc:  # Folge 05
    def wt(sid, prefix):
        for p in ph[sid]:
            for w in p['words']:
                if w['say'].startswith(prefix): return w['t0']
    def rewind(d=2.0):   # ticking that slows down while the clock turns back
        out = np.zeros(int(d * SR)); tt = 0.0; k = 0
        while tt < d - 0.05:
            n = int(0.03 * SR); s = hp(rng.standard_normal(n), 3000) * env(n, 0.0005, 0.006)
            i = int(tt * SR); out[i:i + n] += s[:len(out) - i]; tt += 0.06 + 0.12 * (tt / d); k += 1
        return out
    def bloop():
        n = int(0.32 * SR); x = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-x * 7) + 180) / SR) * env(n, 0.003, 0.12)
    h = sc['hook']; place(fx, popsfx(), h['start'] + 0.1, 0.3); place(fx, rewind(2.0), h['start'] + 0.6, 0.5); place(fx, ding(1320), h['start'] + 2.7, 0.18)
    tg = wt('gift', 'geschenkt'); place(fx, confetti_pop(), tg, 0.5); place(fx, sparkle(), tg + 0.1, 0.3)
    place(fx, popsfx(), wt('gift', 'schlafen') - 0.3, 0.3)
    s = sc['body']; place(fx, popsfx(), s['start'] + 0.2, 0.25); place(fx, popsfx(), s['start'] + 0.6, 0.25); place(fx, bloop(), wt('body', 'alten') - 0.2, 0.4)
    p2 = ph['body'][1]['start']
    for k in range(3): place(fx, popsfx(), p2 + 0.2 + k * 0.15, 0.2)
    place(fx, ding(990), p2 + 1.2, 0.2)
    s = sc['vote']
    for k in range(8): place(fx, tick(), s['start'] + 0.8 + k * 0.2, 0.4)
    place(fx, ding(1560), wt('vote', 'Prozent'), 0.22)
    place(fx, popsfx(), wt('choice', 'Sommerzeit') - 0.3, 0.3); place(fx, popsfx(), wt('choice', 'Winterzeit') - 0.3, 0.3); place(fx, drumhit(), wt('choice', 'Winterzeit') + 0.3, 0.35)
    place(fx, sparkle(), sc['summer']['start'] + 0.3, 0.25)
    s = sc['dark']; place(fx, drumhit(), s['start'] + 0.1, 0.45); place(fx, popsfx(), wt('dark', 'Schule') - 0.2, 0.3); place(fx, popsfx(), wt('dark', 'Arbeit') - 0.2, 0.3)
    s = sc['expert']; place(fx, popsfx(), s['start'] + 0.2, 0.3); place(fx, ding(1320), wt('expert', 'Licht') - 0.2, 0.18); place(fx, bloop(), ph['expert'][1]['start'] + 0.3, 0.4)
    s = sc['eu']; place(fx, whoosh(0.5), s['start'] + 0.2, 0.3); place(fx, ding(1760), wt('eu', 'Parlament') - 0.2, 0.2); place(fx, crack(), wt('eu', 'Länder') - 0.2, 0.5)
    s = sc['outro']; place(fx, popsfx(), s['start'] + 0.3, 0.35)

if 'freeze' in sc:  # Folge 06
    def wt(sid, prefix):
        for p in ph[sid]:
            for w in p['words']:
                if w['say'].startswith(prefix): return w['t0']
    def rewind(d=1.0):   # tape rewind: fast falling chirps
        n = int(d * SR); x = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(1800 - 1200 * (x / d) + 400 * np.sin(2 * np.pi * 14 * x)) / SR) * np.sin(np.pi * x / d) * 0.6
    def boing():
        n = int(0.35 * SR); x = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(220 + 180 * np.sin(2 * np.pi * 9 * x) * np.exp(-x * 6)) / SR) * env(n, 0.003, 0.15)
    def thud():
        n = int(0.25 * SR); x = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(140 * np.exp(-x * 12) + 50) / SR) * np.exp(-x * 18)
    def bark():
        n = int(0.18 * SR); x = np.arange(n) / SR
        return bp(rng.standard_normal(n), 500, 2200) * np.exp(-x * 20) + np.sin(2 * np.pi * np.cumsum(600 - 1500 * x) / SR) * np.exp(-x * 15) * 0.6
    def crowd(d=2.5):
        n = int(d * SR); x = np.arange(n) / SR
        return bp(rng.standard_normal(n), 300, 3000) * np.sin(np.pi * x / d) ** 0.7
    ty = wt('hook', 'zweitausend'); place(fx, rewind(1.0), ty - 0.4, 0.4); place(fx, confetti_pop(), ty + 0.6, 0.5); place(fx, ding(1560), ty + 0.6, 0.2)
    place(fx, popsfx(), wt('wake', 'jünger') - 0.3, 0.3); place(fx, popsfx(), wt('wake', 'Handy') - 0.4, 0.3)
    s = sc['apps']
    for k in range(3): place(fx, popsfx(), s['start'] + 0.2 + k * 0.35, 0.22); place(fx, whoosh(0.25), s['start'] + 0.6 + k * 0.35, 0.25)
    place(fx, popsfx(), ph['apps'][1]['start'] + 0.1, 0.25); place(fx, bark(), wt('apps', 'Snapchat') - 0.2, 0.35); place(fx, sparkle(), wt('apps', 'Streaks') - 0.3, 0.25)
    s = sc['games']; place(fx, popsfx(), s['start'] + 0.2, 0.25); place(fx, whoosh(0.25), s['start'] + 0.6, 0.25)
    td = wt('games', 'Dafür')
    for k in range(8): place(fx, boing(), td + 0.2 + k * 0.4, 0.12)
    place(fx, ding(1760), wt('games', 'Pokémon') - 0.2, 0.22)
    tb = wt('school', 'Bottle'); place(fx, whoosh(0.9), tb - 0.9, 0.3); place(fx, thud(), tb + 0.2, 0.6); place(fx, ding(1320), tb + 0.25, 0.18)
    place(fx, drumhit(), wt('school', 'Dab') - 0.05, 0.45)
    tf = wt('freeze', 'erstarren'); place(fx, crack(), tf - 0.25, 0.5); place(fx, sparkle(), tf - 0.2, 0.25)
    s = sc['summer']; place(fx, crowd(2.8), s['start'] + 0.3, 0.3)
    for k in range(5): place(fx, thud(), s['start'] + 0.4 + k * 0.78, 0.25)
    s = sc['aha']; place(fx, popsfx(), wt('aha', 'gestern') - 0.3, 0.3); td = wt('aha', 'Dabei')
    for k in range(10): place(fx, tick(), td + k * 0.12, 0.4)
    place(fx, drumhit(), td + 1.25, 0.5)
    s = sc['outro']; place(fx, popsfx(), s['start'] + 0.3, 0.35); place(fx, popsfx(), ph['outro'][1]['start'], 0.3)

if 'germany' in sc:  # Folge 07
    def wt(sid, prefix, k=0):
        for p in ph[sid]:
            for w in p['words']:
                if w['say'].startswith(prefix):
                    if k == 0: return w['t0']
                    k -= 1
    def star_ping():
        n = int(0.25 * SR); x = np.arange(n) / SR
        return np.sin(2 * np.pi * 1760 * x) * np.exp(-x * 14)
    def bloop():
        n = int(0.32 * SR); x = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-x * 7) + 180) / SR) * env(n, 0.003, 0.12)
    def horn():
        n = int(0.6 * SR); x = np.arange(n) / SR
        return (np.sign(np.sin(2 * np.pi * 330 * x)) + np.sign(np.sin(2 * np.pi * 415 * x))) * 0.25 * np.minimum(1, x / 0.02) * np.minimum(1, (0.6 - x) / 0.05)
    def stamp():
        n = int(0.3 * SR); x = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(120 * np.exp(-x * 10) + 45) / SR) * np.exp(-x * 14) + bp(rng.standard_normal(n), 300, 2000) * np.exp(-x * 40) * 0.5
    h = sc['hook']; place(fx, whoosh(0.6), h['start'], 0.35); place(fx, popsfx(), h['start'] + 0.1, 0.3)
    ta = wt('hook', 'alle')
    for k in range(10): place(fx, popsfx(), ta - 0.2 + k * 0.09, 0.12)
    place(fx, popsfx(), ph['hook'][1]['start'] - 0.1, 0.3)
    for sid in ('others', 'work', 'germany', 'still'): place(fx, star_ping(), sc[sid]['start'] + 0.5, 0.3)
    s = sc['others']; place(fx, popsfx(), s['start'] + 0.2, 0.25)
    tv = wt('others', 'verschoben')
    for k in range(3): place(fx, whoosh(0.3), tv - 0.2 + k * 0.25, 0.25)
    place(fx, popsfx(), ph['others'][1]['start'] + 0.2, 0.3); place(fx, popsfx(), wt('others', 'Twitch') - 0.3, 0.3); place(fx, bloop(), wt('others', 'Minus') - 0.2, 0.45)
    place(fx, ding(1320), wt('work', 'Prozent') - 0.3, 0.2); place(fx, cough(), wt('work', 'krankmelden') - 0.3, 0.3)
    place(fx, popsfx(), sc['germany']['start'] + 0.2, 0.3); place(fx, popsfx(), wt('germany', 'Zehnte') - 0.2, 0.3); place(fx, drumhit(), wt('germany', 'fehlen') - 0.2, 0.45)
    place(fx, horn(), wt('still', 'Busse') - 0.2, 0.25); place(fx, popsfx(), wt('still', 'Läden') - 0.2, 0.3); place(fx, popsfx(), wt('still', 'Pizza') - 0.2, 0.3); place(fx, sparkle(), wt('still', 'GTA') - 0.3, 0.3)
    s = sc['risk']; place(fx, drumhit(), s['start'] + 0.1, 0.4); place(fx, stamp(), wt('risk', 'fristlose') - 0.2, 0.6)
    tu = wt('aha', 'Urlaub'); place(fx, stamp(), tu - 0.3, 0.4); place(fx, ding(1760), tu - 0.2, 0.22)
    for k in range(5): place(fx, star_ping(), sc['aha']['start'] + 0.3 + k * 0.26, 0.12)
    s = sc['outro']; place(fx, popsfx(), s['start'] + 0.3, 0.35); place(fx, popsfx(), wt('outro', 'Markier') - 0.2, 0.3)

# ---------- voice + ducking ----------
with wave.open(f'{ep}/voice.wav') as w: voice = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
# "good microphone" chain: clean low end, remove boxiness, gentle presence, de-ess, compression, a little air. No reverb.
def peq(x, f, gain_db, q=1.0):
    A = 10 ** (gain_db / 40); w = 2 * np.pi * f / SR; al = np.sin(w) / (2 * q)
    b0, b1, b2 = 1 + al * A, -2 * np.cos(w), 1 - al * A; a0, a1, a2 = 1 + al / A, -2 * np.cos(w), 1 - al / A
    from scipy.signal import lfilter
    return lfilter([b0 / a0, b1 / a0, b2 / a0], [1, a1 / a0, a2 / a0], x)
def follow(x, att, rel):
    from scipy.signal import lfilter
    a_r = np.exp(-1 / (rel * SR)); e = lfilter([1 - a_r], [1, -a_r], np.abs(x)); return e
voice = hp(hp(voice, 85), 85)
voice = peq(voice, 180, 1.5, 0.8)      # warmth
voice = peq(voice, 420, -3.0, 1.2)     # less boxy
voice = peq(voice, 1200, -1.0, 1.0)    # tame nasal synth tone
voice = peq(voice, 3800, 2.0, 0.9)     # clarity
# de-esser on 5-8 kHz
sib = bp(voice, 4800, 7800); se = follow(sib, 0.002, 0.04); thr = np.percentile(se, 92)
voice = voice - sib * np.clip(1 - thr / np.maximum(se, 1e-6), 0, 0.7)
# air: soft harmonics of the upper band (source ends at 8 kHz)
air = hp(np.tanh(hp(voice, 3500) * 4) / 4, 8000)
voice = voice + air * 0.35
# compressor 3:1 + makeup
e = follow(voice, 0.005, 0.12); lvl = 20 * np.log10(np.maximum(e, 1e-5)); th = np.percentile(lvl[e > 0.01], 70)
gr = np.where(lvl > th, (lvl - th) * (1 - 1 / 3), 0); voice = voice * 10 ** (-gr / 20)
voice /= np.max(np.abs(voice)) + 1e-9
act = (np.abs(voice) > 0.03).astype(float); k = int(0.3 * SR); c = np.concatenate([[0], np.cumsum(act)])
ma = (c[np.clip(np.arange(N) + k // 2, 0, N)] - c[np.clip(np.arange(N) - k // 2, 0, N)]) / k
duck = lp(np.clip(ma * 4, 0, 1), 5)
mix = fx * 0.35 + voice * 1.0   # keine Musik
mix = hp(mix, 30); mix = np.tanh(mix * 1.1); mix /= np.max(np.abs(mix)) * 1.05
fo = int(0.8 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
with wave.open(f'{ep}/mix.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('mix', round(T, 2))
