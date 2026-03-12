import json
import torch
import soundfile as sf
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

MODEL = "facebook/wav2vec2-base-960h"

processor = Wav2Vec2Processor.from_pretrained(MODEL)
model = Wav2Vec2ForCTC.from_pretrained(MODEL)

def main(inp, out):
    with open(inp) as f:
        rows = [json.loads(x) for x in f]

    for r in rows:
        wav, sr = sf.read(r["wav_path"])
        input_values = processor(wav, sampling_rate=sr, return_tensors="pt").input_values

        with torch.no_grad():
            logits = model(input_values).logits

        pred_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(pred_ids)[0]

        r["hyp_text"] = transcription

    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--inp")
    p.add_argument("--out")
    args = p.parse_args()
    main(args.inp, args.out)
