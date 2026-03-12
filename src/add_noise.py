import json, argparse
from pathlib import Path
import numpy as np
import soundfile as sf

def add_noise(x, n, snr):
    n = n[:len(x)]
    px = np.mean(x**2) + 1e-12
    pn = np.mean(n**2) + 1e-12
    s = np.sqrt(px / (pn * 10**(snr/10)))
    y = x + s * n
    m = np.max(np.abs(y))
    if m > 1: y = y / m
    return y

def main(inp, out, noise_path, snr):
    rows = [json.loads(x) for x in open(inp)]
    noise, nsr = sf.read(noise_path)
    out_dir = Path("data/raw/en/noisy")
    out_dir.mkdir(parents=True, exist_ok=True)
    new = []

    for r in rows:
        x, sr = sf.read(r["wav_path"])
        if noise.ndim > 1: noise1 = noise[:,0]
        else: noise1 = noise
        rep = int(np.ceil(len(x) / len(noise1)))
        n = np.tile(noise1, rep)[:len(x)]
        y = add_noise(x.astype("float32"), n.astype("float32"), snr)

        p = out_dir / f'{Path(r["wav_path"]).stem}_snr{snr}.wav'
        sf.write(p, y, sr)

        r2 = r.copy()
        r2["wav_path"] = str(p)
        r2["snr_db"] = snr
        new.append(r2)

    with open(out, "w") as f:
        for r in new:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--inp")
    p.add_argument("--out")
    p.add_argument("--noise")
    p.add_argument("--snr", type=float)
    a = p.parse_args()
    main(a.inp, a.out, a.noise, a.snr)
