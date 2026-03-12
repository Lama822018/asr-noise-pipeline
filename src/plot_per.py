import json, argparse
import matplotlib.pyplot as plt

def main(inp, out, snr):
    with open(inp, encoding="utf-8") as f:
        x = json.load(f)

    plt.figure()
    plt.plot([snr], [x["per"]], marker="o")
    plt.xlabel("SNR (dB)")
    plt.ylabel("PER")
    plt.title("PER vs Noise")
    plt.savefig(out, bbox_inches="tight")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--inp")
    p.add_argument("--out")
    p.add_argument("--snr", type=float)
    a = p.parse_args()
    main(a.inp, a.out, a.snr)
