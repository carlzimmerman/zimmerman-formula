#!/usr/bin/env python3
"""
M4 ESM Predictor: Metal-Accelerated Protein Structure Prediction

SPDX-License-Identifier: AGPL-3.0-or-later

Uses ESM-2 on Apple M4's Metal Performance Shaders (MPS) backend
for GPU-accelerated protein structure prediction.

This is Stage 1 of the physics-first protein design pipeline:
1. ESM-2 structure prediction (this script)
2. OpenMM thermodynamic validation
3. Z² resonance filtering

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import torch
import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# METAL/MPS CONFIGURATION
# ==============================================================================

def setup_device() -> torch.device:
    """
    Setup compute device with M4 Metal acceleration.

    Priority: MPS (Metal) > CUDA > CPU
    """
    if torch.backends.mps.is_available():
        if torch.backends.mps.is_built():
            device = torch.device("mps")
            print(f"✓ Using Apple Metal (MPS) acceleration")
            print(f"  Backend: Metal Performance Shaders")
            return device

    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"✓ Using CUDA: {torch.cuda.get_device_name(0)}")
        return device

    print("⚠ Using CPU (no GPU acceleration)")
    return torch.device("cpu")


# ==============================================================================
# ESM-2 MODEL LOADING
# ==============================================================================

def load_esm_model(model_name: str = "esm2_t33_650M_UR50D"):
    """
    Load ESM-2 model with Metal acceleration.

    Available models (from smallest to largest):
    - esm2_t6_8M_UR50D     (8M params, fastest)
    - esm2_t12_35M_UR50D   (35M params)
    - esm2_t30_150M_UR50D  (150M params)
    - esm2_t33_650M_UR50D  (650M params, recommended)
    - esm2_t36_3B_UR50D    (3B params, requires >16GB)
    """
    print(f"\nLoading ESM-2 model: {model_name}")

    try:
        import esm
        model, alphabet = esm.pretrained.load_model_and_alphabet(model_name)
        batch_converter = alphabet.get_batch_converter()

        device = setup_device()
        model = model.to(device)
        model.eval()

        print(f"✓ Model loaded: {sum(p.numel() for p in model.parameters()):,} parameters")

        return model, alphabet, batch_converter, device

    except ImportError:
        print("⚠ ESM not installed. Install with: pip install fair-esm")
        return None, None, None, None
    except Exception as e:
        print(f"⚠ Error loading model: {e}")
        return None, None, None, None


# ==============================================================================
# STRUCTURE PREDICTION
# ==============================================================================

def predict_structure_esm(
    sequence: str,
    model,
    alphabet,
    batch_converter,
    device: torch.device,
    name: str = "protein"
) -> Dict:
    """
    Predict protein structure using ESMFold-style approach.

    Returns contact map and per-residue embeddings for downstream analysis.
    """
    print(f"\n{'='*60}")
    print(f"PREDICTING STRUCTURE: {name}")
    print(f"{'='*60}")
    print(f"Sequence length: {len(sequence)} residues")

    # Prepare batch
    data = [(name, sequence)]
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    batch_tokens = batch_tokens.to(device)

    # Extract representations
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[33], return_contacts=True)

    # Get embeddings (last layer)
    embeddings = results["representations"][33][0, 1:-1].cpu().numpy()  # Remove BOS/EOS

    # Get contact predictions
    contacts = results["contacts"][0].cpu().numpy()

    # Compute confidence metrics
    contact_probs = contacts
    mean_contact_prob = float(np.mean(contact_probs[contact_probs > 0.5]))
    n_confident_contacts = int(np.sum(contact_probs > 0.7))

    print(f"\n✓ Prediction complete")
    print(f"  Embedding shape: {embeddings.shape}")
    print(f"  Contact map shape: {contacts.shape}")
    print(f"  Mean confident contact prob: {mean_contact_prob:.3f}")
    print(f"  High-confidence contacts (>0.7): {n_confident_contacts}")

    return {
        "name": name,
        "sequence": sequence,
        "length": len(sequence),
        "embeddings": embeddings,
        "contacts": contacts,
        "mean_contact_prob": mean_contact_prob,
        "n_confident_contacts": n_confident_contacts,
        "device": str(device)
    }


def contacts_to_distance_matrix(contacts: np.ndarray, contact_threshold: float = 8.0) -> np.ndarray:
    """
    Convert contact probabilities to approximate distance matrix.

    Uses the relationship: P(contact) ≈ 1 / (1 + exp((d - threshold) / scale))
    Inverted: d ≈ threshold - scale * log(P / (1 - P))
    """
    n = len(contacts)
    distances = np.zeros((n, n))

    scale = 2.0  # Angstroms

    for i in range(n):
        for j in range(n):
            if i == j:
                distances[i, j] = 0.0
            else:
                p = np.clip(contacts[i, j], 0.01, 0.99)
                # Inverse sigmoid
                d = contact_threshold - scale * np.log(p / (1 - p))
                distances[i, j] = max(3.8, d)  # Minimum CA-CA distance

    return distances


def distance_matrix_to_coords(distances: np.ndarray, n_iter: int = 1000) -> np.ndarray:
    """
    Reconstruct 3D coordinates from distance matrix using MDS.

    Uses metric MDS (classical scaling) for fast initial guess,
    then optional refinement.
    """
    from sklearn.manifold import MDS

    n = len(distances)

    # Classical MDS
    mds = MDS(
        n_components=3,
        dissimilarity='precomputed',
        random_state=42,
        max_iter=n_iter,
        normalized_stress='auto'
    )

    coords = mds.fit_transform(distances)

    return coords


# ==============================================================================
# Z² CONSTRAINT CHECKING
# ==============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51

def check_z2_contacts(coords: np.ndarray, cutoff: float = 8.0) -> Dict:
    """
    Check if predicted structure has Z²-compatible contact geometry.

    The CUBE-SPHERE geometry predicts ~8 contacts per residue.
    """
    n = len(coords)
    contacts_per_residue = []

    for i in range(n):
        n_contacts = 0
        for j in range(n):
            if abs(i - j) > 1:  # Skip backbone neighbors
                d = np.linalg.norm(coords[i] - coords[j])
                if d < cutoff:
                    n_contacts += 1
        contacts_per_residue.append(n_contacts)

    mean_contacts = np.mean(contacts_per_residue)
    std_contacts = np.std(contacts_per_residue)

    # Z² predicts 8 contacts (CUBE vertices)
    z2_deviation = abs(mean_contacts - 8.0) / 8.0
    z2_compatible = z2_deviation < 0.5  # Within 50% of prediction

    return {
        "mean_contacts": float(mean_contacts),
        "std_contacts": float(std_contacts),
        "z2_expected": 8.0,
        "z2_deviation": float(z2_deviation),
        "z2_compatible": z2_compatible
    }


# ==============================================================================
# MAIN PREDICTION PIPELINE
# ==============================================================================

def predict_and_validate(
    sequence: str,
    name: str = "protein",
    output_dir: str = "predictions",
    model_name: str = "esm2_t33_650M_UR50D"
) -> Dict:
    """
    Full prediction pipeline with Z² validation.

    1. Load ESM-2 model (Metal-accelerated)
    2. Predict contacts and embeddings
    3. Reconstruct approximate 3D structure
    4. Check Z² compatibility
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load model
    model, alphabet, batch_converter, device = load_esm_model(model_name)

    if model is None:
        return {"error": "Could not load ESM model"}

    # Predict structure
    prediction = predict_structure_esm(
        sequence, model, alphabet, batch_converter, device, name
    )

    # Convert to distance matrix
    print("\nConverting contacts to distance matrix...")
    distances = contacts_to_distance_matrix(prediction["contacts"])

    # Reconstruct coordinates
    print("Reconstructing 3D coordinates (MDS)...")
    coords = distance_matrix_to_coords(distances)

    # Check Z² compatibility
    print("\nChecking Z² geometry compatibility...")
    z2_check = check_z2_contacts(coords)

    print(f"  Mean contacts/residue: {z2_check['mean_contacts']:.1f}")
    print(f"  Z² expected: {z2_check['z2_expected']:.1f}")
    print(f"  Z² deviation: {z2_check['z2_deviation']:.1%}")
    print(f"  Z² compatible: {'✓ YES' if z2_check['z2_compatible'] else '✗ NO'}")

    # Save results
    result = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "sequence": sequence,
        "length": len(sequence),
        "model": model_name,
        "device": str(device),
        "mean_contact_prob": prediction["mean_contact_prob"],
        "n_confident_contacts": prediction["n_confident_contacts"],
        "z2_geometry": z2_check,
        "coordinates": coords.tolist()
    }

    output_path = os.path.join(output_dir, f"{name}_esm_prediction.json")
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n✓ Results saved to: {output_path}")

    # Save PDB
    pdb_path = os.path.join(output_dir, f"{name}_esm.pdb")
    save_ca_pdb(sequence, coords, pdb_path)
    print(f"✓ PDB saved to: {pdb_path}")

    return result


def save_ca_pdb(sequence: str, coords: np.ndarray, filepath: str):
    """Save Cα-only PDB file."""
    aa_map = {
        'A': 'ALA', 'C': 'CYS', 'D': 'ASP', 'E': 'GLU', 'F': 'PHE',
        'G': 'GLY', 'H': 'HIS', 'I': 'ILE', 'K': 'LYS', 'L': 'LEU',
        'M': 'MET', 'N': 'ASN', 'P': 'PRO', 'Q': 'GLN', 'R': 'ARG',
        'S': 'SER', 'T': 'THR', 'V': 'VAL', 'W': 'TRP', 'Y': 'TYR'
    }

    with open(filepath, 'w') as f:
        f.write(f"REMARK   ESM-2 predicted structure (Cα only)\n")
        f.write(f"REMARK   Generated: {datetime.now().isoformat()}\n")
        f.write(f"REMARK   Z² geometry validation included\n")

        for i, (aa, coord) in enumerate(zip(sequence, coords)):
            res_name = aa_map.get(aa, 'UNK')
            f.write(f"ATOM  {i+1:5d}  CA  {res_name} A{i+1:4d}    "
                    f"{coord[0]:8.3f}{coord[1]:8.3f}{coord[2]:8.3f}"
                    f"  1.00  0.00           C\n")

        f.write("END\n")


# ==============================================================================
# BATCH PREDICTION
# ==============================================================================

def batch_predict(
    sequences: List[Tuple[str, str]],
    output_dir: str = "predictions",
    model_name: str = "esm2_t33_650M_UR50D"
) -> List[Dict]:
    """
    Batch prediction for multiple sequences.

    Input: List of (name, sequence) tuples
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load model once
    model, alphabet, batch_converter, device = load_esm_model(model_name)

    if model is None:
        return [{"error": "Could not load ESM model"}]

    results = []

    for name, sequence in sequences:
        try:
            prediction = predict_structure_esm(
                sequence, model, alphabet, batch_converter, device, name
            )

            distances = contacts_to_distance_matrix(prediction["contacts"])
            coords = distance_matrix_to_coords(distances)
            z2_check = check_z2_contacts(coords)

            result = {
                "name": name,
                "length": len(sequence),
                "z2_compatible": z2_check["z2_compatible"],
                "mean_contacts": z2_check["mean_contacts"],
                "device": str(device)
            }
            results.append(result)

            # Save individual PDB
            pdb_path = os.path.join(output_dir, f"{name}_esm.pdb")
            save_ca_pdb(sequence, coords, pdb_path)

        except Exception as e:
            results.append({"name": name, "error": str(e)})

    return results


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("M4 ESM PREDICTOR - Metal-Accelerated Structure Prediction")
    print("=" * 70)

    # Test sequence: Short Z²-designed peptide
    test_sequence = "MKWVTFISLLLLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPFDEHVKLVNELTEFAKTCVADESHAGCEKSLHTLFGDELCKVASLRETYGDMADCCEKQEPERNECFLSHKDDSPDLPKLKPDPNTLCDEFKADEKKFWGKYLYEIARRHPYFYAPELLYYANKYNGVFQECCQAEDKGACLLPKIETMREKVLASSARQRLRCASIQKFGERALKAWSVARLSQKFPKAEFVEVTKLVTDLTKVHKECCHGDLLECADDRADLAKYICDNQDTISSKLKECCDKPLLEKSHCIAEVEKDAIPENLPPLTADFAEDKDVCKNYQEAKDAFLGSFLYEYSRRHPEYAVSVLLRLAKEYEATLEECCAKDDPHACYSTVFDKLKHLVDEPQNLIKQNCDQFEKLGEYGFQNALIVRYTRKVPQVSTPTLVEVSRSLGKVGTRCCTKPESERMPCTEDYLSLILNRLCVLHEKTPVSEKVTKCCTESLVNRRPCFSALTPDETYVPKAFDEKLFTFHADICTLPDTEKQIKKQTALVELLKHKPKATEEQLKTVMENFVAFVDKCCAADDKEACFAVEGPKLVVSTQTALA"

    # Check if ESM is available
    try:
        import esm
        print("\n✓ ESM library available")

        # Run prediction
        result = predict_and_validate(
            test_sequence[:100],  # Use first 100 residues for quick test
            name="test_z2_protein",
            output_dir="extended_research/biotech/hybrid_z2_test/m4_pipeline/predictions"
        )

        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Device: {result.get('device', 'unknown')}")
        print(f"Z² compatible: {result.get('z2_geometry', {}).get('z2_compatible', 'unknown')}")

    except ImportError:
        print("\n⚠ ESM not installed.")
        print("Install with: pip install fair-esm torch")
        print("\nTo use Metal acceleration on M4:")
        print("  pip install --upgrade torch torchvision torchaudio")
        print("\nThen run this script again.")
