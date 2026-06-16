#!/usr/bin/env python3
"""
Retrain the Legomena models LOCALLY on Apple Silicon (MLX), on the CLEAN
numerology-free corpus, then rebuild the ollama models with the honest system prompt.

Pipeline per model:
  1) mlx_lm.lora  --train   (LoRA adapter on the clean corpus)
  2) mlx_lm.fuse  --export-gguf   (fuse adapter into base, export f16 GGUF)
  3) ollama create <target>   (FROM the GGUF + honest SYSTEM prompt)

Usage:
  python retrain_mlx.py prepare                 # build train.jsonl / valid.jsonl from gold_examples.jsonl
  python retrain_mlx.py train legomena-moe      # one model
  python retrain_mlx.py all                     # all three, sequential

unsloth is NOT used (it requires CUDA; this is an M4 Max). MLX is the Apple-Silicon path.
"""
import json, subprocess, sys, os
from pathlib import Path
from datetime import datetime

HERE = Path(__file__).parent
CORPUS = HERE / "corpus"
ADAPTERS = HERE / "adapters"
GGUF = HERE / "gguf"
SYSPROMPT = (HERE / "SYSTEM_PROMPT.txt").read_text().rstrip()

# Base = confirmed-available MLX-format Gemma 4 weights (4-bit) from HuggingFace.
# legomena-moe uses the 26B-active-4B Mixture-of-Experts (the "smaller MoE").
CONFIGS = {
    "legomena-moe": {"base": "mlx-community/gemma-4-26b-a4b-it-4bit", "target": "legomena-moe-clean", "ident": "LegomenaLLM-MoE"},
    "legomena-xl":  {"base": "mlx-community/gemma-4-31b-it-4bit",     "target": "legomena-xl-clean",  "ident": "LegomenaXL"},
    "legomena":     {"base": "mlx-community/gemma-4-12B-it-4bit",     "target": "legomena-clean",     "ident": "LegomenaLLM"},
}
EPOCHS = 3
NUM_LAYERS = 8           # LoRA depth
BATCH = 1
LR = "1e-5"


def prepare():
    gold = CORPUS / "gold_examples.jsonl"
    if not gold.exists():
        sys.exit(f"ERROR: {gold} not found — assemble the clean corpus first.")
    ex = [json.loads(l) for l in gold.read_text().splitlines() if l.strip()]
    train, valid = [], []
    for i, e in enumerate(ex):
        # mlx_lm chat format
        rec = {"messages": [
            {"role": "user", "content": e["instruction"] + (("\n\n" + e["input"]) if e.get("input") else "")},
            {"role": "assistant", "content": e["output"]},
        ]}
        (valid if i % 10 == 0 else train).append(rec)
    CORPUS.mkdir(parents=True, exist_ok=True)
    (CORPUS / "train.jsonl").write_text("\n".join(json.dumps(r) for r in train) + "\n")
    (CORPUS / "valid.jsonl").write_text("\n".join(json.dumps(r) for r in valid) + "\n")
    print(f"prepared: {len(train)} train, {len(valid)} valid -> {CORPUS}")
    return len(train)


def run(cmd):
    print("\n$ " + " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True)


def train_one(key):
    cfg = CONFIGS[key]
    n = sum(1 for _ in (CORPUS / "train.jsonl").open())
    iters = max(200, (n * EPOCHS) // BATCH)
    adapter = ADAPTERS / f"{key}-{datetime.now().strftime('%Y%m%d')}"
    gguf = GGUF / f"{cfg['target']}.gguf"
    ADAPTERS.mkdir(parents=True, exist_ok=True); GGUF.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*72}\nRETRAIN {key}  base={cfg['base']}  iters={iters}\n{'='*72}")
    # 1) LoRA fine-tune on the CLEAN corpus
    run([sys.executable, "-m", "mlx_lm", "lora", "--model", cfg["base"], "--train",
         "--data", CORPUS, "--adapter-path", adapter,
         "--batch-size", BATCH, "--iters", iters, "--num-layers", NUM_LAYERS,
         "--learning-rate", LR, "--grad-checkpoint"])
    # 2) fuse + export GGUF
    run([sys.executable, "-m", "mlx_lm", "fuse", "--model", cfg["base"],
         "--adapter-path", adapter, "--export-gguf", "--gguf-path", str(gguf)])
    # 3) ollama create with the honest system prompt
    sp = SYSPROMPT.replace("You are LegomenaLLM,", f"You are {cfg['ident']},", 1)
    mf = HERE / f"Modelfile.{cfg['target']}"
    mf.write_text(
        f'FROM {gguf}\n\n'
        'TEMPLATE """<start_of_turn>user\n{{ .Prompt }}<end_of_turn>\n<start_of_turn>model\n{{ .Response }}<end_of_turn>"""\n\n'
        'PARAMETER stop "<end_of_turn>"\nPARAMETER temperature 0.6\nPARAMETER top_p 0.9\nPARAMETER num_ctx 8192\n\n'
        f'SYSTEM """{sp}"""\n')
    run(["ollama", "create", cfg["target"], "-f", str(mf)])
    print(f"\nDONE {key} -> ollama model '{cfg['target']}' (clean weights + honest prompt)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    if cmd == "prepare":
        prepare()
    elif cmd == "train":
        prepare(); train_one(sys.argv[2])
    elif cmd == "all":
        prepare()
        for k in ["legomena-moe", "legomena-xl", "legomena"]:
            try:
                train_one(k)
            except subprocess.CalledProcessError as e:
                print(f"!! {k} failed: {e} — continuing", flush=True)
    else:
        sys.exit("usage: retrain_mlx.py [prepare|train <key>|all]")
