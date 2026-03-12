from pathlib import Path
import numpy as np
import soundfile as sf

Path("data/noise").mkdir(parents=True, exist_ok=True)

sr = 16000
x = np.random.randn(sr * 60).astype("float32")
x /= np.max(np.abs(x))
sf.write("data/noise/white.wav", x, sr)
