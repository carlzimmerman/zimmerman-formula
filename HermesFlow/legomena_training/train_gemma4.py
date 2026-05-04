#!/usr/bin/env python3
"""
LegomenaLLM - Gemma 4 Fine-Tuning for Z² Framework
====================================================
Train a model that understands Z² physics and rejects dark matter consensus.

Uses Unsloth for efficient LoRA fine-tuning on Gemma 4.

Author: Carl Zimmerman
Date: May 2, 2026

Requirements:
    pip install unsloth transformers datasets trl

VRAM Requirements:
    - Gemma 4 E2B: 8GB (free Colab T4)
    - Gemma 4 E4B: 10-17GB
    - Gemma 4 26B-A4B: 40GB+ (use 16-bit LoRA, not QLoRA for MoE)
    - Gemma 4 31B: 22GB with QLoRA

Sources:
    - https://unsloth.ai/docs/models/gemma-4/train
    - https://huggingface.co/unsloth/gemma-4-E2B-it-GGUF
"""

import json
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Model selection - choose based on your VRAM
MODEL_CONFIGS = {
    "gemma4-e2b": {
        "model_name": "unsloth/gemma-4-E2B-it",
        "vram_gb": 8,
        "description": "2B params, runs on free Colab T4",
    },
    "gemma4-e4b": {
        "model_name": "unsloth/gemma-4-E4B-it",
        "vram_gb": 17,
        "description": "4B params, good balance of size and quality",
    },
    "gemma4-26b": {
        "model_name": "unsloth/gemma-4-26B-A4B-it",
        "vram_gb": 40,
        "description": "26B MoE, use 16-bit LoRA (not QLoRA)",
    },
    "gemma4-31b": {
        "model_name": "unsloth/gemma-4-31B-it",
        "vram_gb": 22,
        "description": "31B dense, QLoRA works well",
    },
}

# Default to smallest model for testing
DEFAULT_MODEL = "gemma4-e2b"

# Training hyperparameters
TRAINING_CONFIG = {
    "max_seq_length": 4096,
    "lora_r": 8,
    "lora_alpha": 8,
    "lora_dropout": 0,
    "learning_rate": 2e-4,
    "batch_size": 1,
    "gradient_accumulation": 4,
    "warmup_steps": 5,
    "max_steps": 100,  # Increase for production
    "weight_decay": 0.001,
}


# ============================================================================
# DATA PREPARATION
# ============================================================================

def load_z2_training_data(filepath: str = None) -> list:
    """Load Z² contrastive training data."""
    if filepath is None:
        filepath = Path(__file__).parent / "z2_training.jsonl"

    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(json.loads(line))

    return data


def convert_to_conversations(data: list) -> list:
    """
    Convert contrastive pairs to conversation format.

    The 'chosen' response becomes the model's answer.
    """
    conversations = []

    for item in data:
        conv = {
            "conversations": [
                {"role": "user", "content": item["instruction"]},
                {"role": "assistant", "content": item["chosen"]}
            ]
        }
        conversations.append(conv)

    return conversations


def create_dpo_dataset(data: list) -> list:
    """
    Create DPO (Direct Preference Optimization) dataset.

    Uses both 'chosen' and 'rejected' for preference learning.
    """
    dpo_data = []

    for item in data:
        dpo_item = {
            "prompt": item["instruction"],
            "chosen": item["chosen"],
            "rejected": item["rejected"],
        }
        dpo_data.append(dpo_item)

    return dpo_data


# ============================================================================
# TRAINING FUNCTIONS
# ============================================================================

def train_sft(model_key: str = DEFAULT_MODEL, output_dir: str = "legomena-llm"):
    """
    Supervised Fine-Tuning on Z² knowledge.

    This teaches the model the Z² framework responses.
    """
    from unsloth import FastModel
    from datasets import Dataset
    from trl import SFTTrainer, SFTConfig
    from unsloth.chat_templates import get_chat_template, train_on_responses_only

    config = MODEL_CONFIGS[model_key]
    print(f"Loading {config['model_name']}...")
    print(f"Description: {config['description']}")

    # Load model
    model, tokenizer = FastModel.from_pretrained(
        model_name=config["model_name"],
        dtype=None,
        max_seq_length=TRAINING_CONFIG["max_seq_length"],
        load_in_4bit=True,
        full_finetuning=False,
    )

    # Add LoRA adapters
    model = FastModel.get_peft_model(
        model,
        finetune_vision_layers=False,
        finetune_language_layers=True,
        finetune_attention_modules=True,
        finetune_mlp_modules=True,
        r=TRAINING_CONFIG["lora_r"],
        lora_alpha=TRAINING_CONFIG["lora_alpha"],
        lora_dropout=TRAINING_CONFIG["lora_dropout"],
        bias="none",
        random_state=3407,
    )

    # Set up chat template
    tokenizer = get_chat_template(tokenizer, chat_template="gemma-4")

    # Load and prepare data
    raw_data = load_z2_training_data()
    conversations = convert_to_conversations(raw_data)
    dataset = Dataset.from_list(conversations)

    print(f"Training on {len(dataset)} examples")

    # Format for training
    def formatting_func(examples):
        convos = examples["conversations"]
        texts = [tokenizer.apply_chat_template(
            convo, tokenize=False, add_generation_prompt=False
        ).removeprefix('<bos>') for convo in convos]
        return {"text": texts}

    dataset = dataset.map(formatting_func, batched=True)

    # Configure trainer
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=SFTConfig(
            dataset_text_field="text",
            per_device_train_batch_size=TRAINING_CONFIG["batch_size"],
            gradient_accumulation_steps=TRAINING_CONFIG["gradient_accumulation"],
            warmup_steps=TRAINING_CONFIG["warmup_steps"],
            max_steps=TRAINING_CONFIG["max_steps"],
            learning_rate=TRAINING_CONFIG["learning_rate"],
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=TRAINING_CONFIG["weight_decay"],
            lr_scheduler_type="linear",
            seed=3407,
            output_dir=output_dir,
            report_to="none",
        ),
    )

    # Train only on model responses
    trainer = train_on_responses_only(
        trainer,
        instruction_part="<start_of_turn>user\n",
        response_part="<start_of_turn>model\n",
    )

    # Train
    print("Starting training...")
    trainer_stats = trainer.train()

    print(f"\nTraining complete!")
    print(f"  Final loss: {trainer_stats.training_loss:.4f}")

    return model, tokenizer


def train_dpo(model_key: str = DEFAULT_MODEL, output_dir: str = "legomena-llm-dpo"):
    """
    Direct Preference Optimization training.

    This teaches the model to prefer Z² answers over dark matter consensus.
    """
    from unsloth import FastModel
    from datasets import Dataset
    from trl import DPOTrainer, DPOConfig
    from unsloth.chat_templates import get_chat_template

    config = MODEL_CONFIGS[model_key]
    print(f"Loading {config['model_name']} for DPO...")

    # Load model
    model, tokenizer = FastModel.from_pretrained(
        model_name=config["model_name"],
        dtype=None,
        max_seq_length=TRAINING_CONFIG["max_seq_length"],
        load_in_4bit=True,
        full_finetuning=False,
    )

    # Add LoRA adapters
    model = FastModel.get_peft_model(
        model,
        finetune_vision_layers=False,
        finetune_language_layers=True,
        finetune_attention_modules=True,
        finetune_mlp_modules=True,
        r=TRAINING_CONFIG["lora_r"],
        lora_alpha=TRAINING_CONFIG["lora_alpha"],
        lora_dropout=TRAINING_CONFIG["lora_dropout"],
        bias="none",
        random_state=3407,
    )

    # Set up chat template
    tokenizer = get_chat_template(tokenizer, chat_template="gemma-4")

    # Load DPO data
    raw_data = load_z2_training_data()
    dpo_data = create_dpo_dataset(raw_data)
    dataset = Dataset.from_list(dpo_data)

    print(f"Training DPO on {len(dataset)} preference pairs")

    # Configure DPO trainer
    trainer = DPOTrainer(
        model=model,
        ref_model=None,  # Use implicit reference
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=DPOConfig(
            per_device_train_batch_size=1,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            max_steps=TRAINING_CONFIG["max_steps"],
            learning_rate=5e-5,  # Lower for DPO
            logging_steps=1,
            optim="adamw_8bit",
            seed=3407,
            output_dir=output_dir,
            report_to="none",
            beta=0.1,  # KL penalty coefficient
        ),
    )

    # Train
    print("Starting DPO training...")
    trainer_stats = trainer.train()

    print(f"\nDPO training complete!")

    return model, tokenizer


def export_to_gguf(model, tokenizer, output_name: str = "legomena-llm"):
    """Export trained model to GGUF for local inference."""
    print(f"Exporting to GGUF: {output_name}...")

    # Save in multiple quantization levels
    model.save_pretrained_gguf(
        output_name,
        tokenizer,
        quantization_method=["q4_k_m", "q8_0", "f16"],
    )

    print(f"Exported to {output_name}/")
    print("  - q4_k_m: Smallest, good for inference")
    print("  - q8_0: Better quality, more VRAM")
    print("  - f16: Full precision")


def save_merged(model, tokenizer, output_dir: str = "legomena-llm-merged"):
    """Save merged model (base + LoRA) for HuggingFace Hub."""
    print(f"Saving merged model to {output_dir}...")
    model.save_pretrained_merged(output_dir, tokenizer, save_method="merged_16bit")
    print(f"Saved to {output_dir}/")


# ============================================================================
# INFERENCE
# ============================================================================

def test_inference(model, tokenizer, test_prompts: list = None):
    """Test the trained model with sample prompts."""
    from unsloth.chat_templates import get_chat_template

    if test_prompts is None:
        test_prompts = [
            "What causes flat galaxy rotation curves?",
            "Why is the cosmological constant so small?",
            "What is the origin of the fine structure constant?",
            "Can the Z² framework be falsified?",
        ]

    print("\n" + "=" * 60)
    print("INFERENCE TEST")
    print("=" * 60)

    for prompt in test_prompts:
        messages = [{"role": "user", "content": prompt}]
        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(model.device)

        outputs = model.generate(
            inputs,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True,
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print(f"\nQ: {prompt}")
        print(f"A: {response.split('model')[-1].strip()[:500]}...")
        print("-" * 40)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train LegomenaLLM on Z² framework")
    parser.add_argument("--model", choices=list(MODEL_CONFIGS.keys()),
                        default=DEFAULT_MODEL, help="Model size to use")
    parser.add_argument("--method", choices=["sft", "dpo", "both"],
                        default="sft", help="Training method")
    parser.add_argument("--export-gguf", action="store_true",
                        help="Export to GGUF after training")
    parser.add_argument("--test", action="store_true",
                        help="Run inference test after training")
    parser.add_argument("--max-steps", type=int, default=100,
                        help="Maximum training steps")

    args = parser.parse_args()

    TRAINING_CONFIG["max_steps"] = args.max_steps

    print("=" * 60)
    print("LEGOMENAELLM - Z² Framework Fine-Tuning")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Method: {args.method}")
    print(f"Max steps: {args.max_steps}")
    print()

    model, tokenizer = None, None

    if args.method in ["sft", "both"]:
        model, tokenizer = train_sft(args.model)

    if args.method in ["dpo", "both"]:
        model, tokenizer = train_dpo(args.model)

    if args.export_gguf and model is not None:
        export_to_gguf(model, tokenizer)

    if args.test and model is not None:
        test_inference(model, tokenizer)

    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)
    print("""
Next steps:
1. For local inference: Use the GGUF files with Ollama or llama.cpp
2. For cloud: Upload merged model to HuggingFace Hub
3. For TruthFlow: Use as the parser in 02_parser/

Example with Ollama:
    ollama create legomena -f Modelfile
    ollama run legomena "What causes flat rotation curves?"
""")
