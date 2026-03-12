import json, argparse
from jiwer import wer

def main(inp, out):
    rows = [json.loads(x) for x in open(inp, encoding="utf-8")]
    ref = [r["ref_phon"] for r in rows]
    hyp = [r["hyp_phon"] for r in rows]
    per = wer(ref, hyp)
    with open(out, "w", encoding="utf-8") as f:
        f.write(json.dumps({"per": per, "n": len(rows)}))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--inp")
    p.add_argument("--out")
    a = p.parse_args()
    main(a.inp, a.out)
