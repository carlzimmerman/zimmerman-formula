#!/usr/bin/env python3
"""
Z² Physics-Informed Neural Network Encoder (PyTorch + MPS)

SPDX-License-Identifier: AGPL-3.0-or-later

A PyTorch neural network that predicts protein structure from sequence
using ONLY geometric physics constraints - NO evolutionary data.

THE REVOLUTION:
AlphaFold trains on millions of MSA sequences (evolution).
Z² PINN trains on a single mathematical law: Z² = 8 contacts.

Architecture:
- Graph Neural Network with attention
- Native M4 acceleration via torch.device('mps')
- Physics-informed loss function

Loss Function (NO DATA, PURE PHYSICS):
L = λ₁·L_Z² + λ₂·L_bonds + λ₃·L_clash + λ₄·L_Rg

Where:
- L_Z² = Σᵢ(contacts_i - 8)² → Force coordination number to 8
- L_bonds = Σᵢ(d_{i,i+1} - 3.8)² → Enforce Cα-Cα distances
- L_clash = Σᵢⱼ max(0, 3.0 - d_{ij})² → No steric clashes
- L_Rg = (Rg - Rg_target)² → Compact globular fold

Input: 1D FASTA sequence
Output: 3D Cα coordinates

This replaces evolutionary learning with GEOMETRIC learning.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103
OPTIMAL_CONTACTS = 8  # Z² topological optimum
CA_CA_DISTANCE = 3.8  # Å
CONTACT_CUTOFF = 8.0  # Å
CLASH_DISTANCE = 3.0  # Å

print("=" * 70)
print("Z² PHYSICS-INFORMED NEURAL NETWORK ENCODER")
print("=" * 70)
print(f"Z² = {Z2:.4f}")
print(f"Optimal coordination = {OPTIMAL_CONTACTS}")
print("Training on GEOMETRY, not evolution")
print("=" * 70)

# ==============================================================================
# DEVICE SELECTION (MPS for M4)
# ==============================================================================

def get_device():
    """Get best available device (MPS for M4 Mac)."""
    if torch.backends.mps.is_available():
        device = torch.device('mps')
        print(f"Using Apple M4 GPU acceleration (MPS)")
    elif torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"Using CUDA GPU")
    else:
        device = torch.device('cpu')
        print(f"Using CPU")
    return device


# ==============================================================================
# AMINO ACID ENCODING
# ==============================================================================

AA_LIST = 'ACDEFGHIKLMNPQRSTVWY'
AA_TO_IDX = {aa: i for i, aa in enumerate(AA_LIST)}
N_AMINO_ACIDS = len(AA_LIST)

# Physical properties
AA_PROPERTIES = {
    'A': [1.8, 0.0, 0.5, 1.42], 'C': [2.5, 0.0, 0.6, 0.70],
    'D': [-3.5, -1.0, 0.7, 1.01], 'E': [-3.5, -1.0, 0.8, 1.51],
    'F': [2.8, 0.0, 1.0, 1.13], 'G': [-0.4, 0.0, 0.3, 0.57],
    'H': [-3.2, 0.1, 0.8, 1.00], 'I': [4.5, 0.0, 0.9, 1.08],
    'K': [-3.9, 1.0, 0.9, 1.16], 'L': [3.8, 0.0, 0.9, 1.21],
    'M': [1.9, 0.0, 0.9, 1.45], 'N': [-3.5, 0.0, 0.7, 0.67],
    'P': [-1.6, 0.0, 0.6, 0.57], 'Q': [-3.5, 0.0, 0.8, 1.11],
    'R': [-4.5, 1.0, 1.0, 0.98], 'S': [-0.8, 0.0, 0.5, 0.77],
    'T': [-0.7, 0.0, 0.6, 0.83], 'V': [4.2, 0.0, 0.8, 1.06],
    'W': [-0.9, 0.0, 1.2, 1.08], 'Y': [-1.3, 0.0, 1.1, 0.69],
}


def encode_sequence(sequence: str, device: torch.device) -> torch.Tensor:
    """Encode sequence as feature tensor."""
    n = len(sequence)
    features = torch.zeros(n, N_AMINO_ACIDS + 4, device=device)

    for i, aa in enumerate(sequence):
        if aa in AA_TO_IDX:
            features[i, AA_TO_IDX[aa]] = 1.0
        props = AA_PROPERTIES.get(aa, [0, 0, 0.5, 1.0])
        features[i, N_AMINO_ACIDS:] = torch.tensor(props, device=device)

    return features


def positional_encoding(n: int, d_model: int, device: torch.device) -> torch.Tensor:
    """Sinusoidal positional encoding."""
    pe = torch.zeros(n, d_model, device=device)
    position = torch.arange(0, n, dtype=torch.float, device=device).unsqueeze(1)
    div_term = torch.exp(torch.arange(0, d_model, 2, dtype=torch.float, device=device) *
                        (-np.log(10000.0) / d_model))

    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)

    return pe


# ==============================================================================
# PHYSICS LOSS FUNCTIONS (DIFFERENTIABLE)
# ==============================================================================

def z2_contact_loss(coords: torch.Tensor, cutoff: float = CONTACT_CUTOFF) -> torch.Tensor:
    """
    Z² Contact Loss: Force coordination number to exactly 8.

    L_Z² = Σᵢ (contacts_i - 8)²

    This is the CORE physics constraint.
    """
    n = coords.shape[0]

    # Pairwise distances
    diff = coords.unsqueeze(0) - coords.unsqueeze(1)  # (n, n, 3)
    dist = torch.norm(diff, dim=2)  # (n, n)

    # Soft contact function (differentiable sigmoid)
    contacts = torch.sigmoid((cutoff - dist) / 1.0)

    # Zero out self and immediate neighbors
    mask = torch.abs(torch.arange(n, device=coords.device).unsqueeze(0) -
                    torch.arange(n, device=coords.device).unsqueeze(1)) > 2
    contacts = contacts * mask.float()

    # Sum contacts per residue
    contacts_per_residue = contacts.sum(dim=1)

    # Squared deviation from optimal Z² = 8
    deviation = contacts_per_residue - OPTIMAL_CONTACTS
    loss = (deviation ** 2).mean()

    return loss


def bond_length_loss(coords: torch.Tensor) -> torch.Tensor:
    """
    Bond Length Loss: Enforce Cα-Cα distance = 3.8 Å.

    L_bonds = Σᵢ (|rᵢ₊₁ - rᵢ| - 3.8)²
    """
    # Sequential distances
    diff = coords[1:] - coords[:-1]
    dist = torch.norm(diff, dim=1)

    deviation = dist - CA_CA_DISTANCE
    loss = (deviation ** 2).mean()

    return loss


def steric_clash_loss(coords: torch.Tensor, min_dist: float = CLASH_DISTANCE) -> torch.Tensor:
    """
    Steric Clash Loss: Penalize overlapping atoms.

    L_clash = Σᵢⱼ max(0, min_dist - d_{ij})²
    """
    n = coords.shape[0]

    # Pairwise distances
    diff = coords.unsqueeze(0) - coords.unsqueeze(1)
    dist = torch.norm(diff, dim=2)

    # Only consider non-bonded pairs (|i-j| > 2)
    mask = torch.abs(torch.arange(n, device=coords.device).unsqueeze(0) -
                    torch.arange(n, device=coords.device).unsqueeze(1)) > 2

    # Clash penalty (only if closer than min_dist)
    violation = F.relu(min_dist - dist) * mask.float()
    loss = (violation ** 2).sum() / (mask.sum() + 1e-6)

    return loss


def radius_of_gyration_loss(coords: torch.Tensor, n_residues: int) -> torch.Tensor:
    """
    Radius of Gyration Loss: Enforce compact fold.

    Target Rg ≈ 2.2 * N^0.38 (empirical for globular proteins)
    """
    center = coords.mean(dim=0, keepdim=True)
    rg = torch.sqrt(((coords - center) ** 2).sum(dim=1).mean())

    target_rg = 2.2 * (n_residues ** 0.38)
    deviation = rg - target_rg
    loss = deviation ** 2

    return loss


def total_physics_loss(coords: torch.Tensor,
                       weights: Dict[str, float] = None) -> Tuple[torch.Tensor, Dict]:
    """
    Total physics loss combining all constraints.

    L_total = λ₁·L_Z² + λ₂·L_bonds + λ₃·L_clash + λ₄·L_Rg
    """
    if weights is None:
        weights = {
            'z2_contact': 1.0,    # Z² = 8 contacts (MOST IMPORTANT)
            'bond_length': 5.0,   # Cα-Cα = 3.8 Å
            'steric_clash': 10.0, # No overlaps
            'radius_gyr': 0.5     # Compact fold
        }

    n = coords.shape[0]

    losses = {
        'z2_contact': z2_contact_loss(coords),
        'bond_length': bond_length_loss(coords),
        'steric_clash': steric_clash_loss(coords),
        'radius_gyr': radius_of_gyration_loss(coords, n)
    }

    total = sum(weights[k] * losses[k] for k in losses)

    return total, {k: v.item() for k, v in losses.items()}


# ==============================================================================
# NEURAL NETWORK ARCHITECTURE
# ==============================================================================

class Z2GraphAttention(nn.Module):
    """Graph attention layer for residue interactions."""

    def __init__(self, in_features: int, out_features: int, n_heads: int = 4):
        super().__init__()
        self.n_heads = n_heads
        self.head_dim = out_features // n_heads

        self.query = nn.Linear(in_features, out_features)
        self.key = nn.Linear(in_features, out_features)
        self.value = nn.Linear(in_features, out_features)
        self.out_proj = nn.Linear(out_features, out_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        n, d = x.shape

        # Multi-head attention
        Q = self.query(x).view(n, self.n_heads, self.head_dim)
        K = self.key(x).view(n, self.n_heads, self.head_dim)
        V = self.value(x).view(n, self.n_heads, self.head_dim)

        # Attention scores
        scores = torch.einsum('ihd,jhd->ijh', Q, K) / np.sqrt(self.head_dim)
        attn = F.softmax(scores, dim=1)

        # Apply attention
        out = torch.einsum('ijh,jhd->ihd', attn, V)
        out = out.reshape(n, -1)

        return self.out_proj(out)


class Z2PINNEncoder(nn.Module):
    """
    Z² Physics-Informed Neural Network Encoder.

    Predicts 3D coordinates from sequence using graph attention
    and physics-informed loss.
    """

    def __init__(self,
                 n_input: int = 24,      # 20 AA + 4 properties
                 d_model: int = 128,
                 n_layers: int = 6,
                 n_heads: int = 4):
        super().__init__()

        self.d_model = d_model

        # Input projection
        self.input_proj = nn.Sequential(
            nn.Linear(n_input, d_model),
            nn.LayerNorm(d_model),
            nn.ReLU()
        )

        # Positional encoding will be added
        self.pos_dim = 64

        # Graph attention layers
        self.layers = nn.ModuleList([
            nn.ModuleDict({
                'attention': Z2GraphAttention(d_model, d_model, n_heads),
                'norm1': nn.LayerNorm(d_model),
                'ffn': nn.Sequential(
                    nn.Linear(d_model, d_model * 4),
                    nn.GELU(),
                    nn.Linear(d_model * 4, d_model)
                ),
                'norm2': nn.LayerNorm(d_model)
            })
            for _ in range(n_layers)
        ])

        # Output: 3D coordinates
        self.coord_head = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.Linear(d_model // 2, 3)
        )

    def forward(self, seq_features: torch.Tensor,
                pos_encoding: torch.Tensor) -> torch.Tensor:
        """
        Forward pass: sequence → 3D coordinates.
        """
        # Project input
        x = self.input_proj(seq_features)

        # Add positional encoding
        x = x + pos_encoding[:, :self.d_model]

        # Graph attention layers with skip connections
        for layer in self.layers:
            # Self-attention
            attn_out = layer['attention'](layer['norm1'](x))
            x = x + attn_out

            # Feed-forward
            ffn_out = layer['ffn'](layer['norm2'](x))
            x = x + ffn_out

        # Predict coordinates
        coords = self.coord_head(x)

        return coords


# ==============================================================================
# TRAINING LOOP
# ==============================================================================

def train_z2_pinn(sequence: str,
                  n_epochs: int = 500,
                  lr: float = 0.001,
                  device: torch.device = None) -> Dict:
    """
    Train the Z² PINN to fold a sequence.

    Starts from random coil and optimizes toward Z² geometry.
    """
    if device is None:
        device = get_device()

    n_residues = len(sequence)
    print(f"\nTraining Z² PINN on sequence ({n_residues} residues)")
    print(f"Sequence: {sequence[:50]}..." if len(sequence) > 50 else f"Sequence: {sequence}")

    # Encode sequence
    seq_features = encode_sequence(sequence, device)
    pos_encoding = positional_encoding(n_residues, 128, device)

    # Initialize model
    model = Z2PINNEncoder(n_input=seq_features.shape[1], d_model=128).to(device)

    # Optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, n_epochs)

    # Training history
    history = {'total': [], 'z2': [], 'bonds': [], 'clash': [], 'rg': []}

    print(f"\n{'Epoch':<8} {'Total':<12} {'Z² Loss':<12} {'Bonds':<12} {'Clash':<12}")
    print("-" * 60)

    best_loss = float('inf')
    best_coords = None

    for epoch in range(n_epochs):
        model.train()
        optimizer.zero_grad()

        # Forward pass
        coords = model(seq_features, pos_encoding)

        # Physics loss (NO DATA LOSS - PURE PHYSICS)
        total_loss, losses = total_physics_loss(coords)

        # Backward pass
        total_loss.backward()

        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        optimizer.step()
        scheduler.step()

        # Record history
        history['total'].append(total_loss.item())
        history['z2'].append(losses['z2_contact'])
        history['bonds'].append(losses['bond_length'])
        history['clash'].append(losses['steric_clash'])
        history['rg'].append(losses['radius_gyr'])

        # Track best
        if total_loss.item() < best_loss:
            best_loss = total_loss.item()
            best_coords = coords.detach().cpu().numpy()

        # Print progress
        if epoch % 50 == 0 or epoch == n_epochs - 1:
            print(f"{epoch:<8} {total_loss.item():<12.4f} {losses['z2_contact']:<12.4f} "
                  f"{losses['bond_length']:<12.4f} {losses['steric_clash']:<12.4f}")

    # Final evaluation
    model.eval()
    with torch.no_grad():
        final_coords = model(seq_features, pos_encoding)
        final_loss, final_losses = total_physics_loss(final_coords)

    # Compute final contacts
    final_coords_np = final_coords.cpu().numpy()
    from scipy.spatial.distance import cdist
    dist_matrix = cdist(final_coords_np, final_coords_np)

    contacts = []
    for i in range(n_residues):
        n_contacts = 0
        for j in range(n_residues):
            if abs(i - j) > 2 and dist_matrix[i, j] < CONTACT_CUTOFF:
                n_contacts += 1
        contacts.append(n_contacts)

    mean_contacts = np.mean(contacts)

    print(f"\n{'='*60}")
    print("TRAINING COMPLETE")
    print(f"{'='*60}")
    print(f"Final Z² loss: {final_losses['z2_contact']:.4f}")
    print(f"Mean contacts: {mean_contacts:.2f} (Z² optimal = {OPTIMAL_CONTACTS})")
    print(f"Z² deviation: {mean_contacts - OPTIMAL_CONTACTS:+.2f}")

    return {
        'model': model,
        'history': history,
        'final_coords': final_coords_np,
        'best_coords': best_coords,
        'mean_contacts': float(mean_contacts),
        'z2_deviation': float(mean_contacts - OPTIMAL_CONTACTS),
        'final_losses': final_losses
    }


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def save_results(sequence: str, results: Dict, output_dir: str = "pinn_encoder"):
    """Save PINN training results."""
    os.makedirs(output_dir, exist_ok=True)

    # Save final structure as PDB
    coords = results['final_coords']
    pdb_path = os.path.join(output_dir, "z2_pinn_structure.pdb")

    with open(pdb_path, 'w') as f:
        f.write("REMARK  Z² PINN Predicted Structure\n")
        f.write(f"REMARK  Mean contacts: {results['mean_contacts']:.2f}\n")
        f.write(f"REMARK  Z² deviation: {results['z2_deviation']:+.2f}\n")

        for i, (coord, aa) in enumerate(zip(coords, sequence)):
            res_name = {'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
                       'Q': 'GLN', 'E': 'GLU', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
                       'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
                       'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'}.get(aa, 'ALA')

            f.write(f"ATOM  {i+1:5d}  CA  {res_name} A{i+1:4d}    "
                   f"{coord[0]:8.3f}{coord[1]:8.3f}{coord[2]:8.3f}"
                   f"  1.00  0.00           C\n")
        f.write("END\n")

    print(f"  ✓ Structure saved: {pdb_path}")

    # Save training history
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        ax1 = axes[0, 0]
        ax1.plot(results['history']['total'], 'b-', linewidth=1)
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Total Loss')
        ax1.set_title('Training Loss Curve')
        ax1.set_yscale('log')

        ax2 = axes[0, 1]
        ax2.plot(results['history']['z2'], 'r-', linewidth=1, label='Z² Contact')
        ax2.axhline(y=0, color='green', linestyle='--', label='Optimal')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Z² Loss')
        ax2.set_title(f'Z² Contact Loss → {results["final_losses"]["z2_contact"]:.4f}')
        ax2.legend()

        ax3 = axes[1, 0]
        ax3.plot(results['history']['bonds'], 'g-', linewidth=1)
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('Bond Loss')
        ax3.set_title('Bond Length Loss')

        ax4 = axes[1, 1]
        ax4.text(0.5, 0.5, f"""
Z² PINN TRAINING RESULTS

Sequence length: {len(sequence)}
Final Z² loss: {results['final_losses']['z2_contact']:.4f}
Mean contacts: {results['mean_contacts']:.2f}
Z² deviation: {results['z2_deviation']:+.2f}

THE REVOLUTION:
AlphaFold learns from EVOLUTION
Z² PINN learns from GEOMETRY

Loss = λ₁·L_Z² + λ₂·L_bonds + λ₃·L_clash

No MSA. No databases.
Just physics: Z² = 8 contacts.
        """, ha='center', va='center', fontsize=10,
                transform=ax4.transAxes,
                bbox=dict(boxstyle='round', facecolor='wheat'))
        ax4.axis('off')

        plt.tight_layout()
        fig_path = os.path.join(output_dir, "training_history.png")
        plt.savefig(fig_path, dpi=150)
        plt.close()
        print(f"  ✓ Training plot: {fig_path}")

    except ImportError:
        pass

    # Save JSON results
    json_results = {
        'timestamp': datetime.now().isoformat(),
        'sequence': sequence,
        'n_residues': len(sequence),
        'z2_constant': Z2,
        'optimal_contacts': OPTIMAL_CONTACTS,
        'final_losses': results['final_losses'],
        'mean_contacts': results['mean_contacts'],
        'z2_deviation': results['z2_deviation'],
        'training_epochs': len(results['history']['total']),
        'device': 'mps' if torch.backends.mps.is_available() else 'cpu'
    }

    json_path = os.path.join(output_dir, "pinn_results.json")
    with open(json_path, 'w') as f:
        json.dump(json_results, f, indent=2)

    print(f"  ✓ Results saved: {json_path}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Train Z² PINN on the synthetic Z² sequence."""

    # The Z² globular sequence
    sequence = "GNALEMALIYRQDPSMEFLIYKRNGNALEMALVIYEKNPSMEFLIYRQDGSALEMIYVKRNPNMEFLIYEQDGSALEM"

    print(f"\n{'='*60}")
    print("Z² PHYSICS-INFORMED NEURAL NETWORK")
    print(f"{'='*60}")
    print(f"Training on GEOMETRY, not evolution")
    print(f"Target: Z² = 8 contacts per residue")
    print(f"{'='*60}")

    # Get device
    device = get_device()

    # Train
    results = train_z2_pinn(
        sequence,
        n_epochs=200,
        lr=0.002,
        device=device
    )

    # Save results
    print(f"\n{'='*60}")
    print("SAVING RESULTS")
    print(f"{'='*60}")

    save_results(sequence, results, output_dir="pinn_encoder")

    print(f"\n{'='*60}")
    print("Z² PINN ENCODER COMPLETE")
    print(f"{'='*60}")

    print(f"""
  RESULTS:
  Mean contacts: {results['mean_contacts']:.2f} (target = {OPTIMAL_CONTACTS})
  Z² deviation: {results['z2_deviation']:+.2f}

  THE PARADIGM SHIFT:
  ┌─────────────────────────────────────────────┐
  │ AlphaFold:  Learns from EVOLUTION (MSA)     │
  │ Z² PINN:    Learns from GEOMETRY (Z² = 8)   │
  └─────────────────────────────────────────────┘

  We trained a neural network on a single physical law:
  "The coordination number must equal 8"

  No databases. No homology. No evolution.
  Just the geometry of the 8D Kaluza-Klein manifold.
""")

    return results


if __name__ == "__main__":
    results = main()
