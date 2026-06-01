#!/usr/bin/env python3
"""
Test Z² Training Data Loading and Formatting
=============================================
Run this to verify the training data is valid before GPU training.
"""

import json
from pathlib import Path


def test_load_data():
    """Test loading the JSONL training data."""
    filepath = Path(__file__).parent / "z2_training.jsonl"

    print("Loading training data...")
    data = []
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            try:
                item = json.loads(line)
                data.append(item)
            except json.JSONDecodeError as e:
                print(f"ERROR on line {i+1}: {e}")
                return None

    print(f"Loaded {len(data)} training examples")
    return data


def validate_format(data):
    """Validate each item has required fields."""
    print("\nValidating format...")
    errors = []

    for i, item in enumerate(data):
        if "instruction" not in item:
            errors.append(f"Line {i+1}: Missing 'instruction'")
        if "chosen" not in item:
            errors.append(f"Line {i+1}: Missing 'chosen'")
        if "rejected" not in item:
            errors.append(f"Line {i+1}: Missing 'rejected'")

        # Check lengths
        if len(item.get("chosen", "")) < 50:
            errors.append(f"Line {i+1}: 'chosen' too short")
        if len(item.get("rejected", "")) < 50:
            errors.append(f"Line {i+1}: 'rejected' too short")

    if errors:
        print("ERRORS FOUND:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("All items valid!")
        return True


def show_stats(data):
    """Show training data statistics."""
    print("\n" + "=" * 50)
    print("TRAINING DATA STATISTICS")
    print("=" * 50)

    total_chosen_chars = sum(len(item["chosen"]) for item in data)
    total_rejected_chars = sum(len(item["rejected"]) for item in data)
    total_instruction_chars = sum(len(item["instruction"]) for item in data)

    print(f"Total examples: {len(data)}")
    print(f"Avg instruction length: {total_instruction_chars / len(data):.0f} chars")
    print(f"Avg chosen length: {total_chosen_chars / len(data):.0f} chars")
    print(f"Avg rejected length: {total_rejected_chars / len(data):.0f} chars")

    print("\nTopics covered:")
    topics = set()
    keywords = ["dark matter", "rotation", "cosmological", "fine structure",
                "hierarchy", "generations", "gauge", "MOND", "Born rule",
                "Constructor", "tensor", "Hubble"]

    for item in data:
        text = item["instruction"].lower()
        for kw in keywords:
            if kw.lower() in text:
                topics.add(kw)

    for topic in sorted(topics):
        print(f"  - {topic}")


def preview_examples(data, n=3):
    """Show preview of training examples."""
    print("\n" + "=" * 50)
    print(f"PREVIEW (first {n} examples)")
    print("=" * 50)

    for i, item in enumerate(data[:n]):
        print(f"\n--- Example {i+1} ---")
        print(f"Q: {item['instruction']}")
        print(f"\nCHOSEN (Z² answer):")
        print(f"  {item['chosen'][:200]}...")
        print(f"\nREJECTED (consensus answer):")
        print(f"  {item['rejected'][:200]}...")


def convert_to_sft_format(data):
    """Convert to SFT conversation format."""
    print("\n" + "=" * 50)
    print("SFT FORMAT PREVIEW")
    print("=" * 50)

    example = data[0]
    conv = [
        {"role": "user", "content": example["instruction"]},
        {"role": "assistant", "content": example["chosen"]}
    ]

    print("Conversation format:")
    print(json.dumps(conv, indent=2)[:500])


def convert_to_dpo_format(data):
    """Convert to DPO preference format."""
    print("\n" + "=" * 50)
    print("DPO FORMAT PREVIEW")
    print("=" * 50)

    example = data[0]
    dpo = {
        "prompt": example["instruction"],
        "chosen": example["chosen"],
        "rejected": example["rejected"]
    }

    print("DPO format:")
    print(json.dumps(dpo, indent=2)[:500])


if __name__ == "__main__":
    print("=" * 50)
    print("Z² TRAINING DATA TEST")
    print("=" * 50)

    data = test_load_data()
    if data is None:
        exit(1)

    if not validate_format(data):
        exit(1)

    show_stats(data)
    preview_examples(data)
    convert_to_sft_format(data)
    convert_to_dpo_format(data)

    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
    print("""
Ready for training:
    python train_gemma4.py --model gemma4-e2b --method sft

For DPO (preference learning):
    python train_gemma4.py --model gemma4-e2b --method dpo

For both SFT then DPO:
    python train_gemma4.py --model gemma4-e2b --method both --export-gguf
""")
