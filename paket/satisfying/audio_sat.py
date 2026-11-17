"""Sound for the satisfying loops: one synthesized hit per event (from info.json), mixed circularly so the 8 s file loops seamlessly.
usage: python3 audio_sat.py <sync|galton|rings> <info.json> <out.wav>"""
import json, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt
kind, info_path, out = sys.argv[1:4]
info = json.load(open(info_path)); SR = 48000; T = info['duration']; N = int(T * SR)
rng = np.random.default_rng(3)
buf = np.zeros(N)
def place(s, at, gain=1.0):   # circular: tails wrap to the start of the loop
    i = int(at * SR) % N; idx = (np.arange(len(s)) + i) % N; np.add.at(buf, idx, s * gain)
def hp(x, f): return sosfilt(butter(2, f, 'highpass', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'bandpass', fs=SR, output='sos'), x)
PENTA = [0, 2, 4, 7, 9]
def note(i, base=60): return 440 * 2 ** ((base + 12 * (i // 5) + PENTA[i % 5] - 69) / 12)
def bell(f, d=0.9, bright=0.35):
    n = int(d * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * x) + bright * np.sin(2 * np.pi * 2.76 * f * x) * np.exp(-x * 9) + 0.2 * np.sin(2 * np.pi * 2 * f * x)) * np.exp(-x * 5.5) * np.minimum(1, x / 0.002)
def marimba(f, d=0.45):
    n = int(d * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * 4 * f * x) * np.exp(-x * 40)) * np.exp(-x * 11) * np.minimum(1, x / 0.001)
def tick(f=4000, d=0.025):
    n = int(d * SR); x = np.arange(n) / SR
    return bp(rng.standard_normal(n), f * 0.7, min(f * 1.4, 20000)) * np.exp(-x * 260)
def shatter(d=0.9):
    n = int(d * SR); x = np.arange(n) / SR; s = hp(rng.standard_normal(n), 3500) * np.exp(-x * 7) * 0.6
    for k in range(10): f = 2500 + rng.random() * 5000; s += np.sin(2 * np.pi * f * x) * np.exp(-x * (12 + rng.random() * 20)) * 0.12 * (x > k * 0.012)
    return s
def thump(f=70, d=0.6):
    n = int(d * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * np.cumsum(f * (1 + 2 * np.exp(-x * 30))) / SR) * np.exp(-x * 7)
def riser(d=0.7):
    n = int(d * SR); x = np.arange(n) / SR; return bp(rng.standard_normal(n), 800, 6000) * (x / d) ** 2 * 0.5 + np.sin(2 * np.pi * np.cumsum(300 + 900 * (x / d) ** 2) / SR) * (x / d) ** 2 * 0.15
ev = info['events']
if kind == 'sync':
    for e in ev: place(bell(note(e['k'], 60), 1.0), e['t'], 0.22 if e['t'] > 0.01 else 0.3)
    x = np.arange(N) / SR; buf += 0.03 * (np.sin(2 * np.pi * 65.4 * x) + 0.5 * np.sin(2 * np.pi * 98 * x))   # soft drone, period fits the loop
elif kind == 'galton':
    for e in ev:
        if e['type'] == 'peg': place(tick(5200 - e['r'] * 260), e['t'], 0.06 * (0.6 + 0.8 * rng.random()))
        elif e['type'] == 'land': place(marimba(note(abs(e['b'] - 5) * -1 + 8, 64), 0.3), e['t'], 0.1)
        elif e['type'] == 'match':
            for i, k in enumerate([0, 2, 4, 5, 7]): place(bell(note(k, 60), 1.6), e['t'] + i * 0.05, 0.22)
        elif e['type'] == 'open':
            place(thump(55), e['t'], 0.5)
            for k in range(60): place(tick(2500 + rng.random() * 3000, 0.04), e['t'] + 0.05 + rng.random() * 0.5, 0.12)
elif kind == 'rings':
    for e in ev:
        if e['type'] == 'bounce': place(marimba(note(e['n'] % 12, 60)), e['t'], 0.28)
        elif e['type'] == 'break': place(shatter(), e['t'], 0.35 + 0.03 * e['k']); place(thump(80 - e['k'] * 3), e['t'], 0.45); place(bell(note(e['k'] + 5, 60), 1.2), e['t'], 0.18)
        elif e['type'] == 'rebuild': place(riser(T - e['t']), e['t'], 0.6)
buf /= np.max(np.abs(buf)) + 1e-9
buf = np.tanh(buf * 1.4) / np.tanh(1.4)
with wave.open(out, 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 0.9 * 32767).astype(np.int16).tobytes())
print('ok', kind, len(ev), 'events')
