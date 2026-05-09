#!/usr/bin/env python3
"""
LegomenaXL-31B Training with Unsloth
Auto-generated: 2026-05-08T22:36:26.295766

Optimized for MacBook Pro 64GB with aggressive memory settings.
"""

from unsloth import FastLanguageModel
import torch
from datasets import Dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import json

# ═══════════════════════════════════════════════════════════════════════════════
# AGGRESSIVE MEMORY SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════

# Force garbage collection
import gc
gc.collect()

# MPS (Metal) settings for Apple Silicon
if torch.backends.mps.is_available():
    torch.mps.empty_cache()

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD MODEL WITH UNSLOTH OPTIMIZATIONS
# ═══════════════════════════════════════════════════════════════════════════════

max_seq_length = 2048
dtype = None  # Auto-detect
load_in_4bit = True

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="google/gemma-4-31b",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

# ═══════════════════════════════════════════════════════════════════════════════
# ADD LORA ADAPTERS
# ═══════════════════════════════════════════════════════════════════════════════

model = FastLanguageModel.get_peft_model(
    model,
    r=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=64,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing=True,
    random_state=42,
    use_rslora=False,
    loftq_config=None,
)

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD TRAINING DATA
# ═══════════════════════════════════════════════════════════════════════════════

def load_z2_data():
    examples = []
    with open("corpus/gold_examples.jsonl") as f:
        for line in f:
            if line.strip():
                ex = json.loads(line)
                # Format as instruction-following
                text = f"""### Instruction:
{ex['instruction']}

### Response:
{ex['output']}"""
                examples.append({"text": text})
    return Dataset.from_list(examples)

dataset = load_z2_data()
print(f"Loaded {len(dataset)} training examples")

# ═══════════════════════════════════════════════════════════════════════════════
# TRAINING
# ═══════════════════════════════════════════════════════════════════════════════

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    dataset_num_proc=2,
    packing=False,
    args=TrainingArguments(
        output_dir="trained_models/legomena-xl-31b",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        warmup_steps=5,
        num_train_epochs=3,
        learning_rate=0.0001,
        fp16=not torch.backends.mps.is_available(),
        bf16=False,
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=42,
        save_strategy="epoch",
        # Memory optimization
        gradient_checkpointing=True,
        max_grad_norm=0.3,
    ),
)

# ═══════════════════════════════════════════════════════════════════════════════
# RUN TRAINING
# ═══════════════════════════════════════════════════════════════════════════════

print("Starting training...")
trainer_stats = trainer.train()

# Save the model
model.save_pretrained("trained_models/legomena-xl-31b/final")
tokenizer.save_pretrained("trained_models/legomena-xl-31b/final")

print("Training complete!")
print(f"Model saved to: trained_models/legomena-xl-31b/final")
