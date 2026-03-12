import json
import subprocess
import argparse

def phonemize(text, lang):
    cmd = ["espeak-ng", "-q", "--ipa", "-v", lang, text]
    out = subprocess.check_output(cmd).decode().strip()
    return out

def main(inp, outp):
    with open(inp) as f:
        rows = [json.loads(x) for x in f]

    for r in rows:
        r["ref_phon"] = phonemize(r["ref_text"], r["lang"])

    with open(outp, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--inp")
    p.add_argument("--out")
    args = p.parse_args()
    main(args.inp, args.out)
