# LegomenaXL Training on MacBook Pro (64GB)

**Target:** Train Gemma 4 31B (or 26B fallback) on Apple Silicon

---

## Quick Start

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run setup (auto-selects best model for your RAM)
python train_legomena_xl.py --auto --dry-run

# 4. Run actual training
python train_unsloth_31b.py  # or train_unsloth_26b.py
```

---

## Memory Requirements

| Model | Quantization | Est. Memory | MacBook 64GB |
|-------|--------------|-------------|--------------|
| Gemma 4 31B | 4-bit QLoRA | ~35 GB | Tight ⚠️ |
| Gemma 4 26B | 4-bit QLoRA | ~25 GB | Good ✓ |
| Gemma 2 9B | 4-bit QLoRA | ~12 GB | Easy ✓ |

---

## Aggressive Memory Optimization Settings

These settings are already configured in the training scripts:

```python
# Reduce sequence length (saves ~40% memory)
max_seq_length = 2048  # Down from 4096

# Minimal batch size
batch_size = 1
gradient_accumulation = 16  # Effective batch = 16

# Reduced LoRA rank (saves ~20% memory)
lora_rank = 32  # Down from 64

# Enable gradient checkpointing (saves ~30% memory, slower)
gradient_checkpointing = True

# 4-bit quantization (saves ~75% memory)
load_in_4bit = True
```

---

## Before Training

### 1. Close Other Apps
Training will use most of your RAM. Close:
- Browsers (especially Chrome)
- Docker
- Slack/Discord
- IDEs

### 2. Monitor Memory
Open Activity Monitor or run:
```bash
# Watch memory pressure
watch -n 1 'memory_pressure'

# Or use htop
htop
```

### 3. Use Swap Wisely
macOS will use swap if needed. Ensure you have 50+ GB free disk space.

---

## Training Strategy

### Phase 1: Try 31B
```bash
python train_legomena_xl.py --model 31b --backend unsloth
python train_unsloth_31b.py
```

**If you see:**
- `CUDA out of memory` or `MPS out of memory` → Try 26B
- `Killed` or process dies → Try 26B
- Training starts but is extremely slow → Continue, it will finish

### Phase 2: Fallback to 26B
```bash
python train_legomena_xl.py --model 26b --backend unsloth
python train_unsloth_26b.py
```

### Phase 3: Safe Fallback to 9B
If 26B also fails:
```bash
python train_legomena_xl.py --model 9b --backend unsloth
python train_unsloth_9b.py
```

---

## Alternative: MLX Backend

MLX is Apple's ML framework, optimized for Apple Silicon:

```bash
# Install MLX
pip install mlx mlx-lm

# Train with MLX
python train_legomena_xl.py --model 31b --backend mlx
```

MLX advantages:
- Native Metal acceleration
- Better memory management on Apple Silicon
- May fit larger models than PyTorch

---

## Training Time Estimates

| Model | Examples | Epochs | Est. Time (M3 Max) |
|-------|----------|--------|-------------------|
| 31B | 44 | 3 | 4-8 hours |
| 26B | 44 | 3 | 2-4 hours |
| 9B | 44 | 3 | 30-60 min |

---

## After Training

### Merge LoRA Adapters
```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("google/gemma-4-31b")

# Load and merge LoRA
model = PeftModel.from_pretrained(base_model, "trained_models/legomena-xl-31b/final")
model = model.merge_and_unload()

# Save merged model
model.save_pretrained("trained_models/legomena-xl-31b-merged")
```

### Test the Model
```python
from transformers import pipeline

pipe = pipeline("text-generation", model="trained_models/legomena-xl-31b/final")
response = pipe("Derive the weak mixing angle sin²θ_W from the Z² Framework.")
print(response[0]['generated_text'])
```

---

## Troubleshooting

### "Killed" or Process Dies
- Reduce `max_seq_length` to 1024
- Reduce `lora_rank` to 16
- Try smaller model (26B → 9B)

### Very Slow Training
- Expected on MacBook
- 31B at batch_size=1 is slow but will finish
- Consider running overnight

### Metal/MPS Errors
```bash
# Force CPU fallback (slower but stable)
export PYTORCH_ENABLE_MPS_FALLBACK=1
python train_unsloth_31b.py
```

### Out of Disk Space
- Training checkpoints can be large
- Ensure 100+ GB free space
- Delete old checkpoints: `rm -rf trained_models/*/checkpoint-*`

---

## Recommended Workflow

1. **First attempt:** 31B with aggressive settings
2. **If fails:** 26B (very likely to work on 64GB)
3. **Train overnight:** Set it running and check in the morning
4. **Validate:** Test with Z² derivation prompts
5. **Iterate:** Expand training data if needed

---

## Training Data

Current corpus: `corpus/gold_examples.jsonl`
- 44 high-quality examples
- First-principles derivations
- Numerology rejection examples
- Quality tier classifications

To add more examples:
1. Edit `gold_examples.jsonl`
2. Follow the JSON format with all fields
3. Re-run training

---

*Last updated: May 8, 2026*
