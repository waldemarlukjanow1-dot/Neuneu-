"""Sound for meow2.html: only the user's meow (one per ring break, sample unchanged except the leading silence)
and a small soft pop per bounce. Nothing else.
usage: python3 audio_meow2.py <info.json> <meow.wav> <out.wav>"""
import json, sys, wave
import numpy as np
info = json.load(open(sys.argv[1])); SR = 48000; T = info['duration']; N = int((T + 2.0) * SR)
with wave.open(sys.argv[2]) as w: m = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
env = np.convolve(np.abs(m), np.ones(480) / 480, 'same'); on = np.where(env > 0.01)[0]
meow = m[max(0, on[0] - 480): on[-1] + 2400]; meow = meow / np.max(np.abs(meow)); meow[:480] *= np.linspace(0, 1, 480)
buf = np.zeros(N)
def place(s, at, gain): i = max(0, int(at * SR)); j = min(N, i + len(s)); buf[i:j] += s[:j - i] * gain
def pop():   # short, soft "plop": falling sine blip
    n = int(0.06 * SR); x = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(380 + 900 * np.exp(-x * 90)) / SR) * np.exp(-x * 70) * np.minimum(1, x / 0.0015)
for e in info['events']:
    if e['type'] == 'break': place(meow, e['t'] - 0.03, 0.9)
    elif e['type'] == 'bounce': place(pop(), e['t'], 0.16)
buf = buf[:int(T * SR)]; buf /= np.max(np.abs(buf)) + 1e-9
with wave.open(sys.argv[3], 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 0.9 * 32767).astype(np.int16).tobytes())
print('ok', sum(e['type'] == 'break' for e in info['events']), 'meows', sum(e['type'] == 'bounce' for e in info['events']), 'pops')
