import json, argparse, torch
import soundfile as sf
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

MODEL = "facebook/wav2vec2-lv-60-espeak-cv-ft"

processor = Wav2Vec2Processor.from_pretrained(MODEL)
model = Wav2Vec2ForCTC.from_pretrained(MODEL)

def infer_one(wav_path):
    x, sr = sf.read(wav_path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    inp = processor(x, sampling_rate=sr, return_tensors="pt")
    with torch.no_grad():
        logits = model(inp.input_values).logits
    ids = torch.argmax(logits, dim=-1)
    return processor.batch_decode(ids)[0]

def main(inp, out):
    rows = [json.loads(line) for line in open(inp, encoding="utf-8")]
    for r in rows:
        r["hyp_phon"] = infer_one(r["wav_path"])
    with open(out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--inp")
    p.add_argument("--out")
    a = p.parse_args()
    main(a.inp, a.out)
