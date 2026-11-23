"""Original background music, made from code (no samples, no license issues).
make_track(seconds, variant, path) writes a light, upbeat loop as a WAV file."""
import numpy as np, wave

SR = 44100
# chord progressions as semitones from A3 (220 Hz); each chord = list of notes
PROGS = [
    [[3, 7, 10], [-2, 2, 5], [0, 3, 7], [-4, 0, 3]],      # C  G  Am F  (pop)
    [[0, 3, 7], [-4, 0, 3], [3, 7, 10], [-2, 2, 5]],      # Am F  C  G
    [[5, 9, 12], [0, 4, 7], [2, 5, 9], [-2, 2, 5]],       # D  A  Bm G
    [[-2, 2, 5], [2, 5, 9], [-4, 0, 3], [3, 7, 10]],      # G  Bm F  C
]
BPMS = [104, 96, 110, 100]

def f(semi):
    return 220.0 * 2 ** (semi / 12)

def env(n, a=0.005, d=0.25):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def pluck(freq, n, d=0.25):
    t = np.arange(n) / SR
    w = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(4 * np.pi * freq * t) + 0.12 * np.sin(6 * np.pi * freq * t)
    return w * env(n, 0.004, d)

def kick(n):
    t = np.arange(n) / SR
    fr = 50 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 9)

def noise_hit(n, decay, rng, hp=True):
    x = rng.standard_normal(n)
    if hp:
        x = np.diff(np.concatenate([[0], x]))
    return x * np.exp(-np.arange(n) / SR * decay)

def make_track(seconds, variant, path):
    rng = np.random.default_rng(variant)
    prog, bpm = PROGS[variant % 4], BPMS[variant % 4]
    beat = 60 / bpm
    N = int(SR * (seconds + 0.5))
    out = np.zeros((N, 2))

    def add(sig, start, gain, pan=0.0):
        s = int(start * SR)
        if s >= N: return
        sig = sig[: N - s]
        out[s:s + len(sig), 0] += sig * gain * (1 - pan)
        out[s:s + len(sig), 1] += sig * gain * (1 + pan)

    b = 0
    while b * beat < seconds:
        bar, pos = divmod(b, 4)
        chord = prog[bar % 4]
        t0 = b * beat
        # drums
        if pos in (0, 2): add(kick(int(SR * 0.4)), t0, 0.9)
        if pos in (1, 3): add(noise_hit(int(SR * 0.2), 22, rng), t0, 0.18)
        for h in (0, 0.5):
            add(noise_hit(int(SR * 0.05), 90, rng), t0 + h * beat, 0.07, 0.3)
        # bass on 1 and the "and" of 2
        if pos in (0, 1):
            add(pluck(f(chord[0] - 24), int(SR * beat * 1.4), 0.35), t0 + (0 if pos == 0 else beat * 0.5), 0.45)
        # arpeggio (8th notes) up an octave
        for k in range(2):
            note = chord[(pos * 2 + k) % 3] + 12
            add(pluck(f(note), int(SR * 0.5), 0.18), t0 + k * beat / 2, 0.16, -0.35 if k else 0.35)
        # soft pad at start of each bar
        if pos == 0:
            n = int(SR * beat * 4)
            t = np.arange(n) / SR
            pad = sum(np.sin(2 * np.pi * f(c) * t) for c in chord) / 3
            pad *= np.minimum(1, t / 0.3) * np.minimum(1, (n / SR - t) / 0.3)
            add(pad, t0, 0.10)
        b += 1

    out = out[: int(SR * seconds)]
    fade = int(SR * 0.8)
    out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    out[: int(SR * 0.05)] *= np.linspace(0, 1, int(SR * 0.05))[:, None]
    out = np.tanh(out * 1.2)
    out *= 0.30 / max(1e-9, np.abs(out).max())  # keep it in the background (about -10 dBFS peak)
    pcm = (out * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return path

if __name__ == "__main__":
    import sys
    for v in range(4):
        make_track(12, v, f"/home/claude/out/music_test_{v}.wav")
    print("ok")
