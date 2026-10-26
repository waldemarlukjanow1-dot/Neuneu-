"""Synthesise every phrase with Coqui VITS (Thorsten, German), then build timeline.json with word timings.
usage: python3 build_voice.py ep01_script.json <model_dir> <out_dir>"""
import json, sys, os, wave
import numpy as np

script = json.load(open(sys.argv[1])); model_dir = sys.argv[2]; out = sys.argv[3]
os.makedirs(out, exist_ok=True)
SR_OUT = 44100
PITCH = 2 ** (1.3 / 12)   # +1.3 Halbtöne: jünger klingende Stimme, Tempo bleibt gleich

def check_tokens():
    for p in script['phrases']:
        a, b = p['say'].split(), p['cap'].split()
        assert len(a) == len(b), (p['say'], len(a), len(b))
check_tokens()

import subprocess, tempfile
# Piper (ONNX) backend: model_dir is the .onnx file
def synth(txt, ls=1.0):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f: path = f.name
    subprocess.run([sys.executable, '-m', 'piper', '-m', model_dir, '-f', path, '--length-scale', str(round(0.95 * ls, 4)), '--noise-scale', '0.6', '--noise-w-scale', '0.75'],
                   input=txt.encode(), check=True, capture_output=True)
    with wave.open(path) as w: rate = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    os.unlink(path); return x, rate

def trim(x, thr=0.012):
    env = np.convolve(np.abs(x), np.ones(400) / 400, 'same')
    idx = np.where(env > thr)[0]
    if len(idx) == 0: return x
    return x[max(0, idx[0] - 600): idx[-1] + 1600]

clips = []
for i, p in enumerate(script['phrases']):
    # optional per-phrase delivery: rate (>1 = slower), pitch (extra semitones), gain
    pf = PITCH * 2 ** (p.get('pitch', 0) / 12)
    wav, sr = synth(p['say'], pf * p.get('rate', 1.0))
    wav = trim(wav) * p.get('gain', 1.0)
    # resample to 44.1k
    n = int(len(wav) * SR_OUT / (sr * pf))
    wav = np.interp(np.arange(n) * pf / SR_OUT, np.arange(len(wav)) / sr, wav).astype(np.float32)
    clips.append(wav)
    print(i, f'{len(wav)/SR_OUT:.2f}s', p['say'])

# timeline
t = 0.35; phrases = []; prev_scene = None
for p, wav in zip(script['phrases'], clips):
    if prev_scene is not None: t += (0.5 if p['scene'] != prev_scene else 0.22) + p.get('gap', 0)
    dur = len(wav) / SR_OUT
    say, cap = p['say'].split(), p['cap'].split()
    # word weights ~ syllable-ish length; punctuation adds a small pause after the word
    wts = []
    for w in say:
        core = ''.join(ch for ch in w if ch.isalnum())
        vowels = sum(1 for ch in core.lower() if ch in 'aeiouäöüy')
        wts.append(0.6 + max(1, vowels) * 1.0 + len(core) * 0.08 + (0.9 if w[-1] in ',.?!:' else 0))
    lead, tail = 0.04, 0.12
    span = dur - lead - tail; tot = sum(wts); c = t + lead; words = []
    for w, cw, wt in zip(say, cap, wts):
        d = span * wt / tot
        hl = cw.startswith('*'); cw = cw.lstrip('*')
        words.append({'say': w, 'cap': cw, 't0': round(c, 3), 't1': round(c + d * (0.82 if w[-1] in ',.?!:' else 1.0), 3), 'hl': hl})
        c += d
    phrases.append({'scene': p['scene'], 'start': round(t, 3), 'end': round(t + dur, 3), 'words': words})
    t += dur; prev_scene = p['scene']
total = t + script.get('tail', 2.2)   # short tail for videos that loop back to the start
scenes = []
for ph in phrases:
    if not scenes or scenes[-1]['id'] != ph['scene']: scenes.append({'id': ph['scene'], 'start': ph['start'] - (0.3 if scenes else ph['start']), 'end': ph['end']})
    else: scenes[-1]['end'] = ph['end']
for a, b in zip(scenes, scenes[1:]): a['end'] = b['start']
scenes[-1]['end'] = total

# voice track + envelope (for lip sync)
N = int(total * SR_OUT); voice = np.zeros(N, np.float32)
for ph, wav in zip(phrases, clips):
    i = int(ph['start'] * SR_OUT); voice[i:i + len(wav)] += wav[:N - i]
voice /= max(1e-6, np.max(np.abs(voice))) / 0.95
hop = SR_OUT // 100
env = [float(np.sqrt(np.mean(voice[k:k + hop] ** 2))) for k in range(0, N, hop)]
mx = max(env); env = [round(min(1, e / (mx * 0.55)), 3) for e in env]
with wave.open(os.path.join(out, 'voice.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR_OUT); w.writeframes((voice * 32767).astype(np.int16).tobytes())
json.dump({'title': script['title'], 'sources': script['sources'], 'duration': round(total, 3), 'phrases': phrases, 'scenes': scenes, 'env': env},
          open(os.path.join(out, 'timeline.json'), 'w'), ensure_ascii=False)
print('total', round(total, 2), 's;', [(s['id'], round(s['start'], 2)) for s in scenes])
