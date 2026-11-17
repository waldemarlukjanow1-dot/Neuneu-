"""Sound for meow.html: the user's meow on every ring break (unchanged sample, leading silence trimmed),
plus soft bounce ticks, a small glass sparkle per break and a riser for the rebuild. Circular mix → seamless loop.
usage: python3 audio_meow.py <info.json> <meow.wav> <out.wav>"""
import json, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt
info = json.load(open(sys.argv[1])); SR = 48000; T = info['duration']; N = int(T * SR)
with wave.open(sys.argv[2]) as w: m = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
env = np.convolve(np.abs(m), np.ones(480) / 480, 'same'); on = np.where(env > 0.01)[0]
meow = m[max(0, on[0] - 480): on[-1] + 2400]; meow = meow / np.max(np.abs(meow)); fade = min(480, len(meow)); meow[:fade] *= np.linspace(0, 1, fade)
rng = np.random.default_rng(4); buf = np.zeros(N)
def place(s, at, gain=1.0): i = int(at * SR) % N; idx = (np.arange(len(s)) + i) % N; np.add.at(buf, idx, s * gain)
def hp(x, f): return sosfilt(butter(2, f, 'highpass', fs=SR, output='sos'), x)
PENTA = [0, 2, 4, 7, 9]
def note(i, base=72): return 440 * 2 ** ((base + 12 * (i // 5) + PENTA[i % 5] - 69) / 12)
def marimba(f, d=0.3):
    n = int(d * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * 4 * f * x) * np.exp(-x * 40)) * np.exp(-x * 14) * np.minimum(1, x / 0.001)
def sparkle(d=0.5):
    n = int(d * SR); x = np.arange(n) / SR; s = hp(rng.standard_normal(n), 5000) * np.exp(-x * 18) * 0.4
    for k in range(6): f = 3000 + rng.random() * 4000; s += np.sin(2 * np.pi * f * x) * np.exp(-x * (15 + rng.random() * 15)) * 0.1
    return s
def thump(f=60, d=0.7):
    n = int(d * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * np.cumsum(f * (1 + 2 * np.exp(-x * 30))) / SR) * np.exp(-x * 6)
def riser(d):
    n = int(d * SR); x = np.arange(n) / SR; p = (x / d) ** 2; return hp(rng.standard_normal(n), 1500) * p * 0.25 + np.sin(2 * np.pi * np.cumsum(200 + 700 * p) / SR) * p * 0.12
lead = 0.03   # meow onset sits right on the break
for e in info['events']:
    if e['type'] == 'break':
        place(meow, e['t'] - lead, 0.85); place(sparkle(), e['t'], 0.25)
        if e['k'] == 44: place(thump(), e['t'], 0.8)
    elif e['type'] == 'bounce': place(marimba(note(e['n'] % 10)), e['t'], 0.12)
    elif e['type'] == 'rebuild': place(riser(T - e['t'] - 0.3), e['t'], 0.8)
buf /= np.max(np.abs(buf)) + 1e-9; buf = np.tanh(buf * 1.3) / np.tanh(1.3)
with wave.open(sys.argv[3], 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 0.9 * 32767).astype(np.int16).tobytes())
print('ok', sum(e['type'] == 'break' for e in info['events']), 'meows')
