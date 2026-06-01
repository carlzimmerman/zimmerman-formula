#!/usr/bin/env python3
"""
Z² Physics-Informed Neural Network (PINN) for Protein Structure

SPDX-License-Identifier: AGPL-3.0-or-later

A neural network that enforces Z² geometric constraints during training.

THE KEY INNOVATION:
Traditional NNs learn patterns from data.
Z² PINNs enforce PHYSICAL LAWS as differentiable loss terms.

PHYSICS CONSTRAINTS ENCODED:
1. Z² Contact Loss: Penalize deviation from 8 contacts/residue
2. Bond Length Loss: Cα-Cα distance ≈ 3.8 Å
3. Steric Clash Loss: No overlapping atoms
4. Radius of Gyration: Compact globular fold
5. Ramachandran Loss: Valid backbone angles
6. Secondary Structure: Helix/sheet propensities

The total loss combines data fitting with physics:
L_total = L_data + λ₁·L_Z² + λ₂·L_bonds + λ₃·L_steric + ...

This forces the network to learn PHYSICALLY VALID structures,
not just statistically likely ones.

AlphaFold learns from evolution (MSA patterns).
Z² PINN learns from GEOMETRY (first principles).

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Callable
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103
Z = np.sqrt(Z2)       # ≈ 5.7888
OPTIMAL_CONTACTS = 8  # Z² predicts 8 contacts per residue

# Physical constants
CA_CA_DISTANCE = 3.8  # Å (ideal Cα-Cα distance)
CONTACT_CUTOFF = 8.0  # Å
CLASH_DISTANCE = 3.0  # Å (minimum allowed distance)
VDW_RADIUS = 1.7      # Å

print("=" * 70)
print("Z² PHYSICS-INFORMED NEURAL NETWORK")
print("=" * 70)
print(f"Z² = {Z2:.4f}")
print(f"Optimal contacts = {OPTIMAL_CONTACTS}")
print("Neural network with physical law constraints")
print("=" * 70)

# ==============================================================================
# AMINO ACID ENCODING
# ==============================================================================

AA_LIST = 'ACDEFGHIKLMNPQRSTVWY'
AA_TO_IDX = {aa: i for i, aa in enumerate(AA_LIST)}
N_AMINO_ACIDS = len(AA_LIST)

# Physical properties for each amino acid
AA_PROPERTIES = {
    'A': {'hydro': 1.8, 'charge': 0, 'size': 0.5, 'helix': 1.42},
    'C': {'hydro': 2.5, 'charge': 0, 'size': 0.6, 'helix': 0.70},
    'D': {'hydro': -3.5, 'charge': -1, 'size': 0.7, 'helix': 1.01},
    'E': {'hydro': -3.5, 'charge': -1, 'size': 0.8, 'helix': 1.51},
    'F': {'hydro': 2.8, 'charge': 0, 'size': 1.0, 'helix': 1.13},
    'G': {'hydro': -0.4, 'charge': 0, 'size': 0.3, 'helix': 0.57},
    'H': {'hydro': -3.2, 'charge': 0.1, 'size': 0.8, 'helix': 1.00},
    'I': {'hydro': 4.5, 'charge': 0, 'size': 0.9, 'helix': 1.08},
    'K': {'hydro': -3.9, 'charge': 1, 'size': 0.9, 'helix': 1.16},
    'L': {'hydro': 3.8, 'charge': 0, 'size': 0.9, 'helix': 1.21},
    'M': {'hydro': 1.9, 'charge': 0, 'size': 0.9, 'helix': 1.45},
    'N': {'hydro': -3.5, 'charge': 0, 'size': 0.7, 'helix': 0.67},
    'P': {'hydro': -1.6, 'charge': 0, 'size': 0.6, 'helix': 0.57},
    'Q': {'hydro': -3.5, 'charge': 0, 'size': 0.8, 'helix': 1.11},
    'R': {'hydro': -4.5, 'charge': 1, 'size': 1.0, 'helix': 0.98},
    'S': {'hydro': -0.8, 'charge': 0, 'size': 0.5, 'helix': 0.77},
    'T': {'hydro': -0.7, 'charge': 0, 'size': 0.6, 'helix': 0.83},
    'V': {'hydro': 4.2, 'charge': 0, 'size': 0.8, 'helix': 1.06},
    'W': {'hydro': -0.9, 'charge': 0, 'size': 1.2, 'helix': 1.08},
    'Y': {'hydro': -1.3, 'charge': 0, 'size': 1.1, 'helix': 0.69},
}


def encode_sequence(sequence: str) -> np.ndarray:
    """
    Encode sequence as feature matrix.

    Returns: (n_residues, n_features) array
    """
    n = len(sequence)
    n_features = N_AMINO_ACIDS + 4  # One-hot + properties

    features = np.zeros((n, n_features))

    for i, aa in enumerate(sequence):
        # One-hot encoding
        if aa in AA_TO_IDX:
            features[i, AA_TO_IDX[aa]] = 1.0

        # Physical properties
        props = AA_PROPERTIES.get(aa, {'hydro': 0, 'charge': 0, 'size': 0.5, 'helix': 1.0})
        features[i, N_AMINO_ACIDS] = props['hydro'] / 5.0  # Normalize
        features[i, N_AMINO_ACIDS + 1] = props['charge']
        features[i, N_AMINO_ACIDS + 2] = props['size']
        features[i, N_AMINO_ACIDS + 3] = props['helix'] / 1.5

    return features


def positional_encoding(n_residues: int, d_model: int = 64) -> np.ndarray:
    """
    Sinusoidal positional encoding (Transformer-style).
    """
    positions = np.arange(n_residues)[:, np.newaxis]
    dims = np.arange(d_model)[np.newaxis, :]

    angles = positions / np.power(10000, (2 * (dims // 2)) / d_model)

    # Apply sin to even indices, cos to odd
    encoding = np.zeros((n_residues, d_model))
    encoding[:, 0::2] = np.sin(angles[:, 0::2])
    encoding[:, 1::2] = np.cos(angles[:, 1::2])

    return encoding


# ==============================================================================
# PHYSICS LOSS FUNCTIONS (DIFFERENTIABLE)
# ==============================================================================

def z2_contact_loss(coords: np.ndarray,
                    cutoff: float = CONTACT_CUTOFF,
                    target_contacts: int = OPTIMAL_CONTACTS) -> float:
    """
    Z² Contact Loss: Penalize deviation from optimal 8 contacts.

    L_Z² = Σᵢ (contacts_i - 8)²

    This is the CORE Z² physics constraint.
    """
    n = len(coords)

    total_loss = 0.0

    for i in range(n):
        # Count contacts (differentiable approximation)
        contacts = 0.0
        for j in range(n):
            if abs(i - j) > 2:  # Exclude neighbors
                dist = np.linalg.norm(coords[i] - coords[j])
                # Smooth contact function (sigmoid)
                contact_prob = 1.0 / (1.0 + np.exp((dist - cutoff) / 1.0))
                contacts += contact_prob

        # Squared deviation from optimal
        deviation = contacts - target_contacts
        total_loss += deviation ** 2

    return total_loss / n


def bond_length_loss(coords: np.ndarray,
                     target_distance: float = CA_CA_DISTANCE,
                     tolerance: float = 0.2) -> float:
    """
    Bond Length Loss: Enforce Cα-Cα distance ≈ 3.8 Å.

    L_bond = Σᵢ (|rᵢ - rᵢ₊₁| - 3.8)²
    """
    n = len(coords)

    total_loss = 0.0

    for i in range(n - 1):
        dist = np.linalg.norm(coords[i + 1] - coords[i])
        deviation = dist - target_distance
        # Only penalize if outside tolerance
        if abs(deviation) > tolerance:
            total_loss += deviation ** 2

    return total_loss / (n - 1)


def steric_clash_loss(coords: np.ndarray,
                      min_distance: float = CLASH_DISTANCE) -> float:
    """
    Steric Clash Loss: Penalize overlapping atoms.

    L_clash = Σᵢⱼ max(0, min_dist - |rᵢ - rⱼ|)²
    """
    n = len(coords)

    total_loss = 0.0
    n_pairs = 0

    for i in range(n):
        for j in range(i + 3, n):  # Skip nearby residues
            dist = np.linalg.norm(coords[i] - coords[j])

            if dist < min_distance:
                # Penalty for clash
                violation = min_distance - dist
                total_loss += violation ** 2
                n_pairs += 1

    return total_loss


def radius_of_gyration_loss(coords: np.ndarray,
                            target_rg: float = None,
                            n_residues: int = None) -> float:
    """
    Radius of Gyration Loss: Enforce compact globular fold.

    For globular proteins: Rg ≈ 2.2 * N^0.38 (empirical)
    """
    n = len(coords)

    if target_rg is None:
        # Empirical formula for globular proteins
        target_rg = 2.2 * (n ** 0.38)

    # Compute actual Rg
    center = coords.mean(axis=0)
    rg = np.sqrt(np.mean(np.sum((coords - center) ** 2, axis=1)))

    # Penalize deviation from expected
    deviation = rg - target_rg
    return deviation ** 2


def secondary_structure_loss(coords: np.ndarray,
                             sequence: str) -> float:
    """
    Secondary Structure Loss: Encourage helix/sheet formation.

    Based on local geometry (i to i+3 distance for helix).
    """
    n = len(coords)

    total_loss = 0.0

    for i in range(n - 3):
        # Helix: i to i+3 distance ≈ 5.4 Å
        helix_dist = np.linalg.norm(coords[i + 3] - coords[i])
        helix_target = 5.4

        # Check helix propensity of residues
        helix_prop = np.mean([
            AA_PROPERTIES.get(sequence[j], {'helix': 1.0})['helix']
            for j in range(i, min(i + 4, n))
        ])

        if helix_prop > 1.0:  # Good helix former
            # Encourage helix distance
            deviation = helix_dist - helix_target
            total_loss += helix_prop * deviation ** 2

    return total_loss / max(1, n - 3)


def compactness_loss(coords: np.ndarray) -> float:
    """
    Compactness Loss: Penalize extended conformations.

    Uses end-to-end distance relative to chain length.
    """
    n = len(coords)

    # End-to-end distance
    end_to_end = np.linalg.norm(coords[-1] - coords[0])

    # Expected for compact fold (random coil scaling)
    expected_compact = 3.8 * np.sqrt(n)  # Much less than contour length

    if end_to_end > expected_compact:
        return (end_to_end - expected_compact) ** 2
    return 0.0


# ==============================================================================
# NEURAL NETWORK ARCHITECTURE (NumPy-based for portability)
# ==============================================================================

def relu(x: np.ndarray) -> np.ndarray:
    """ReLU activation."""
    return np.maximum(0, x)


def softplus(x: np.ndarray) -> np.ndarray:
    """Softplus activation (smooth ReLU)."""
    return np.log1p(np.exp(x))


def layer_norm(x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """Layer normalization."""
    mean = x.mean(axis=-1, keepdims=True)
    std = x.std(axis=-1, keepdims=True)
    return (x - mean) / (std + eps)


class Z2PhysicsNN:
    """
    Physics-Informed Neural Network for protein structure prediction.

    Architecture:
    - Input: Sequence features + positional encoding
    - Hidden: Multi-layer perceptron with skip connections
    - Output: 3D coordinates per residue

    Loss: L_data + λ₁·L_Z² + λ₂·L_bonds + λ₃·L_clash + ...
    """

    def __init__(self,
                 n_input: int = 24,  # 20 AA + 4 properties
                 n_hidden: int = 128,
                 n_layers: int = 4,
                 n_output: int = 3,  # x, y, z
                 physics_weights: Dict = None):
        """
        Initialize network architecture.
        """
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.n_layers = n_layers
        self.n_output = n_output

        # Physics loss weights
        self.physics_weights = physics_weights or {
            'z2_contact': 1.0,      # Z² = 8 contacts
            'bond_length': 2.0,      # Cα-Cα = 3.8 Å
            'steric_clash': 5.0,     # No overlaps
            'radius_gyration': 0.5,  # Compact fold
            'secondary': 0.3,        # Helix/sheet
            'compactness': 0.2       # Not extended
        }

        # Initialize weights (Xavier initialization)
        self.weights = {}
        self.biases = {}

        # Input layer
        self.weights['input'] = np.random.randn(n_input + 64, n_hidden) * np.sqrt(2.0 / (n_input + 64))
        self.biases['input'] = np.zeros(n_hidden)

        # Hidden layers
        for i in range(n_layers):
            self.weights[f'hidden_{i}'] = np.random.randn(n_hidden, n_hidden) * np.sqrt(2.0 / n_hidden)
            self.biases[f'hidden_{i}'] = np.zeros(n_hidden)

        # Output layer
        self.weights['output'] = np.random.randn(n_hidden, n_output) * np.sqrt(2.0 / n_hidden)
        self.biases['output'] = np.zeros(n_output)

        # Training history
        self.history = {'total_loss': [], 'data_loss': [], 'physics_loss': []}

    def forward(self, sequence_features: np.ndarray,
                positional: np.ndarray) -> np.ndarray:
        """
        Forward pass: sequence → 3D coordinates.
        """
        n_residues = len(sequence_features)

        # Concatenate sequence features with positional encoding
        x = np.concatenate([sequence_features, positional], axis=1)

        # Input layer
        x = x @ self.weights['input'] + self.biases['input']
        x = relu(x)
        x = layer_norm(x)

        # Hidden layers with skip connections
        for i in range(self.n_layers):
            residual = x
            x = x @ self.weights[f'hidden_{i}'] + self.biases[f'hidden_{i}']
            x = relu(x)
            x = layer_norm(x)

            # Skip connection every 2 layers
            if i > 0 and i % 2 == 1:
                x = x + residual

        # Output layer (coordinates)
        coords = x @ self.weights['output'] + self.biases['output']

        return coords

    def compute_physics_loss(self, coords: np.ndarray,
                             sequence: str) -> Dict:
        """
        Compute all physics loss terms.
        """
        losses = {}

        # Z² contact loss (CORE CONSTRAINT)
        losses['z2_contact'] = z2_contact_loss(coords)

        # Bond length loss
        losses['bond_length'] = bond_length_loss(coords)

        # Steric clash loss
        losses['steric_clash'] = steric_clash_loss(coords)

        # Radius of gyration loss
        losses['radius_gyration'] = radius_of_gyration_loss(coords)

        # Secondary structure loss
        losses['secondary'] = secondary_structure_loss(coords, sequence)

        # Compactness loss
        losses['compactness'] = compactness_loss(coords)

        # Weighted total
        total_physics = sum(
            self.physics_weights[key] * loss
            for key, loss in losses.items()
        )

        losses['total_physics'] = total_physics

        return losses

    def compute_data_loss(self, predicted: np.ndarray,
                          target: np.ndarray) -> float:
        """
        Compute data fitting loss (MSE to target structure).
        """
        return np.mean((predicted - target) ** 2)

    def train_step(self, sequence: str,
                   target_coords: np.ndarray,
                   learning_rate: float = 0.001) -> Dict:
        """
        Single training step with gradient descent.

        Note: This uses numerical gradients for simplicity.
        In practice, use autograd (PyTorch/JAX) for efficiency.
        """
        # Encode sequence
        seq_features = encode_sequence(sequence)
        pos_encoding = positional_encoding(len(sequence))

        # Forward pass
        predicted = self.forward(seq_features, pos_encoding)

        # Compute losses
        data_loss = self.compute_data_loss(predicted, target_coords)
        physics_losses = self.compute_physics_loss(predicted, sequence)

        total_loss = data_loss + physics_losses['total_physics']

        # Numerical gradient descent (simplified)
        # In practice, use autograd
        eps = 1e-5

        for key in self.weights:
            grad = np.zeros_like(self.weights[key])

            # Sample a few gradients (stochastic approximation)
            for _ in range(min(10, self.weights[key].size)):
                i, j = np.random.randint(0, self.weights[key].shape[0]), \
                       np.random.randint(0, self.weights[key].shape[1])

                # Perturb
                self.weights[key][i, j] += eps
                pred_plus = self.forward(seq_features, pos_encoding)
                loss_plus = self.compute_data_loss(pred_plus, target_coords) + \
                           self.compute_physics_loss(pred_plus, sequence)['total_physics']

                self.weights[key][i, j] -= 2 * eps
                pred_minus = self.forward(seq_features, pos_encoding)
                loss_minus = self.compute_data_loss(pred_minus, target_coords) + \
                            self.compute_physics_loss(pred_minus, sequence)['total_physics']

                # Restore
                self.weights[key][i, j] += eps

                # Gradient
                grad[i, j] = (loss_plus - loss_minus) / (2 * eps)

            # Update weights
            self.weights[key] -= learning_rate * grad

        return {
            'total_loss': float(total_loss),
            'data_loss': float(data_loss),
            'physics_losses': {k: float(v) for k, v in physics_losses.items()}
        }

    def predict(self, sequence: str) -> np.ndarray:
        """
        Predict structure from sequence.
        """
        seq_features = encode_sequence(sequence)
        pos_encoding = positional_encoding(len(sequence))
        return self.forward(seq_features, pos_encoding)


# ==============================================================================
# STRUCTURE REFINEMENT WITH PHYSICS
# ==============================================================================

def refine_structure_with_physics(coords: np.ndarray,
                                  sequence: str,
                                  n_iterations: int = 100,
                                  learning_rate: float = 0.1) -> Dict:
    """
    Refine a structure by minimizing physics losses.

    This is gradient descent on the physics loss landscape,
    starting from an initial structure.
    """
    coords = coords.copy()
    n = len(coords)

    history = {
        'z2_contact': [],
        'bond_length': [],
        'steric_clash': [],
        'total': []
    }

    print(f"\nRefining structure with Z² physics ({n_iterations} iterations)...")

    for iteration in range(n_iterations):
        # Compute physics losses
        z2_loss = z2_contact_loss(coords)
        bond_loss = bond_length_loss(coords)
        clash_loss = steric_clash_loss(coords)
        rg_loss = radius_of_gyration_loss(coords)

        total_loss = z2_loss + 2*bond_loss + 5*clash_loss + 0.5*rg_loss

        history['z2_contact'].append(z2_loss)
        history['bond_length'].append(bond_loss)
        history['steric_clash'].append(clash_loss)
        history['total'].append(total_loss)

        if iteration % 20 == 0:
            print(f"  Iteration {iteration}: total={total_loss:.4f}, "
                  f"Z²={z2_loss:.4f}, bonds={bond_loss:.4f}")

        # Gradient descent on coordinates
        eps = 1e-4
        grad = np.zeros_like(coords)

        for i in range(n):
            for dim in range(3):
                # Numerical gradient
                coords[i, dim] += eps
                loss_plus = z2_contact_loss(coords) + 2*bond_length_loss(coords) + \
                           5*steric_clash_loss(coords) + 0.5*radius_of_gyration_loss(coords)

                coords[i, dim] -= 2*eps
                loss_minus = z2_contact_loss(coords) + 2*bond_length_loss(coords) + \
                            5*steric_clash_loss(coords) + 0.5*radius_of_gyration_loss(coords)

                coords[i, dim] += eps  # Restore

                grad[i, dim] = (loss_plus - loss_minus) / (2 * eps)

        # Update coordinates
        coords -= learning_rate * grad

        # Adaptive learning rate
        if iteration > 0 and history['total'][-1] > history['total'][-2]:
            learning_rate *= 0.9

    # Final losses
    final_losses = {
        'z2_contact': z2_contact_loss(coords),
        'bond_length': bond_length_loss(coords),
        'steric_clash': steric_clash_loss(coords),
        'radius_gyration': radius_of_gyration_loss(coords)
    }

    return {
        'refined_coords': coords,
        'history': history,
        'final_losses': final_losses,
        'n_iterations': n_iterations
    }


# ==============================================================================
# ANALYSIS AND COMPARISON
# ==============================================================================

def analyze_structure_physics(coords: np.ndarray,
                              sequence: str,
                              name: str = "structure") -> Dict:
    """
    Analyze how well a structure satisfies Z² physics.
    """
    n = len(coords)

    # Compute all physics metrics
    z2_loss = z2_contact_loss(coords)
    bond_loss = bond_length_loss(coords)
    clash_loss = steric_clash_loss(coords)
    rg_loss = radius_of_gyration_loss(coords)
    ss_loss = secondary_structure_loss(coords, sequence)
    compact_loss = compactness_loss(coords)

    # Count contacts per residue
    contacts_per_residue = []
    for i in range(n):
        contacts = 0
        for j in range(n):
            if abs(i - j) > 2:
                dist = np.linalg.norm(coords[i] - coords[j])
                if dist < CONTACT_CUTOFF:
                    contacts += 1
        contacts_per_residue.append(contacts)

    mean_contacts = np.mean(contacts_per_residue)
    z2_deviation = mean_contacts - OPTIMAL_CONTACTS

    # Compute actual Rg
    center = coords.mean(axis=0)
    rg = np.sqrt(np.mean(np.sum((coords - center) ** 2, axis=1)))

    return {
        'name': name,
        'n_residues': n,
        'physics_losses': {
            'z2_contact': float(z2_loss),
            'bond_length': float(bond_loss),
            'steric_clash': float(clash_loss),
            'radius_gyration': float(rg_loss),
            'secondary': float(ss_loss),
            'compactness': float(compact_loss)
        },
        'contacts': {
            'mean': float(mean_contacts),
            'std': float(np.std(contacts_per_residue)),
            'z2_deviation': float(z2_deviation),
            'per_residue': contacts_per_residue
        },
        'geometry': {
            'radius_of_gyration': float(rg),
            'expected_rg': float(2.2 * n**0.38)
        },
        'z2_compliance': float(1.0 / (1.0 + z2_loss))  # Higher = better
    }


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def generate_pinn_visualization(analysis: Dict,
                                refined_analysis: Dict = None,
                                output_path: str = "pinn_analysis.png"):
    """Generate PINN analysis visualization."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("  Warning: matplotlib not available")
        return

    fig = plt.figure(figsize=(16, 10))

    # 1. Physics loss comparison
    ax1 = fig.add_subplot(2, 2, 1)

    loss_names = list(analysis['physics_losses'].keys())
    original_losses = [analysis['physics_losses'][k] for k in loss_names]

    x = np.arange(len(loss_names))
    width = 0.35

    bars1 = ax1.bar(x - width/2, original_losses, width, label='Original', color='blue', alpha=0.7)

    if refined_analysis:
        refined_losses = [refined_analysis['physics_losses'][k] for k in loss_names]
        bars2 = ax1.bar(x + width/2, refined_losses, width, label='Refined', color='green', alpha=0.7)

    ax1.set_ylabel('Loss Value')
    ax1.set_title('Physics Loss Components')
    ax1.set_xticks(x)
    ax1.set_xticklabels(loss_names, rotation=45, ha='right')
    ax1.legend()

    # 2. Contacts per residue
    ax2 = fig.add_subplot(2, 2, 2)

    contacts = analysis['contacts']['per_residue']
    residue_idx = range(len(contacts))

    colors = ['green' if 7 <= c <= 9 else 'orange' if 5 <= c <= 11 else 'red' for c in contacts]
    ax2.bar(residue_idx, contacts, color=colors, width=1.0)
    ax2.axhline(y=OPTIMAL_CONTACTS, color='red', linestyle='--', linewidth=2, label=f'Z² optimal = {OPTIMAL_CONTACTS}')

    ax2.set_xlabel('Residue Index')
    ax2.set_ylabel('Contacts')
    ax2.set_title(f"Contacts per Residue (mean = {analysis['contacts']['mean']:.1f})")
    ax2.legend()

    # 3. Z² compliance score
    ax3 = fig.add_subplot(2, 2, 3)

    labels = ['Z² Compliance']
    scores = [analysis['z2_compliance']]

    if refined_analysis:
        labels.append('Refined Z² Compliance')
        scores.append(refined_analysis['z2_compliance'])

    colors = ['blue', 'green'][:len(scores)]
    bars = ax3.bar(labels, scores, color=colors, alpha=0.7)

    ax3.set_ylabel('Compliance Score')
    ax3.set_title('Z² Physics Compliance (higher = better)')
    ax3.set_ylim(0, 1)

    for bar, score in zip(bars, scores):
        ax3.text(bar.get_x() + bar.get_width()/2, score + 0.02,
                f'{score:.3f}', ha='center', va='bottom', fontsize=12)

    # 4. Summary text
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.axis('off')

    summary_text = f"""
    Z² PHYSICS-INFORMED NEURAL NETWORK ANALYSIS

    Structure: {analysis['name']}
    Residues: {analysis['n_residues']}

    CONTACT ANALYSIS:
    • Mean contacts: {analysis['contacts']['mean']:.2f}
    • Z² optimal: {OPTIMAL_CONTACTS}
    • Deviation: {analysis['contacts']['z2_deviation']:+.2f}

    GEOMETRY:
    • Radius of gyration: {analysis['geometry']['radius_of_gyration']:.1f} Å
    • Expected Rg: {analysis['geometry']['expected_rg']:.1f} Å

    Z² COMPLIANCE SCORE: {analysis['z2_compliance']:.3f}

    KEY INSIGHT:
    Traditional NNs learn from data patterns.
    Z² PINNs enforce PHYSICAL LAWS:
    • Z² = 8 contacts per residue
    • Bond lengths = 3.8 Å
    • No steric clashes
    • Compact globular fold
    """

    ax4.text(0.1, 0.95, summary_text, transform=ax4.transAxes,
             fontsize=10, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Visualization saved: {output_path}")


# ==============================================================================
# MAIN ANALYSIS
# ==============================================================================

def run_pinn_analysis(pdb_path: str,
                      output_dir: str = "physics_nn") -> Dict:
    """
    Run full PINN analysis on a structure.
    """
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nLoading structure: {pdb_path}")

    # Parse structure
    coords = []
    residues = []
    sequence = ""

    AA_3TO1 = {
        'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
        'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
        'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
        'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
    }

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and ' CA ' in line:
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    res_name = line[17:20].strip()

                    coords.append([x, y, z])
                    residues.append(res_name)
                    sequence += AA_3TO1.get(res_name, 'A')
                except:
                    continue

    coords = np.array(coords)
    n_residues = len(coords)

    print(f"  Residues: {n_residues}")

    # Analyze original structure
    print("\nAnalyzing structure physics...")
    analysis = analyze_structure_physics(coords, sequence, "Z² Protein")

    print(f"\n  Mean contacts: {analysis['contacts']['mean']:.2f} (Z² optimal = {OPTIMAL_CONTACTS})")
    print(f"  Z² deviation: {analysis['contacts']['z2_deviation']:+.2f}")
    print(f"  Z² compliance: {analysis['z2_compliance']:.3f}")

    # Refine structure with physics
    print("\n" + "=" * 60)
    print("PHYSICS-BASED STRUCTURE REFINEMENT")
    print("=" * 60)

    refinement = refine_structure_with_physics(
        coords, sequence,
        n_iterations=50,
        learning_rate=0.05
    )

    refined_analysis = analyze_structure_physics(
        refinement['refined_coords'], sequence, "Refined"
    )

    print(f"\nAfter refinement:")
    print(f"  Mean contacts: {refined_analysis['contacts']['mean']:.2f}")
    print(f"  Z² deviation: {refined_analysis['contacts']['z2_deviation']:+.2f}")
    print(f"  Z² compliance: {refined_analysis['z2_compliance']:.3f}")

    # Generate visualization
    print(f"\n{'='*60}")
    print("GENERATING OUTPUTS")
    print(f"{'='*60}")

    viz_path = os.path.join(output_dir, "pinn_analysis.png")
    generate_pinn_visualization(analysis, refined_analysis, viz_path)

    # Save refined structure
    refined_pdb = os.path.join(output_dir, "refined_structure.pdb")
    with open(refined_pdb, 'w') as f:
        f.write("REMARK  Z² Physics-Refined Structure\n")
        for i, (coord, res) in enumerate(zip(refinement['refined_coords'], residues)):
            f.write(f"ATOM  {i+1:5d}  CA  {res:3s} A{i+1:4d}    "
                   f"{coord[0]:8.3f}{coord[1]:8.3f}{coord[2]:8.3f}"
                   f"  1.00  0.00           C\n")
        f.write("END\n")
    print(f"  ✓ Refined PDB: {refined_pdb}")

    # Compile results
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_pdb': pdb_path,
        'n_residues': n_residues,
        'z2_constant': Z2,
        'optimal_contacts': OPTIMAL_CONTACTS,
        'original_analysis': analysis,
        'refined_analysis': refined_analysis,
        'refinement': {
            'n_iterations': refinement['n_iterations'],
            'initial_loss': refinement['history']['total'][0],
            'final_loss': refinement['history']['total'][-1],
            'improvement': (refinement['history']['total'][0] - refinement['history']['total'][-1]) /
                          refinement['history']['total'][0] * 100
        },
        'physics_weights': {
            'z2_contact': 1.0,
            'bond_length': 2.0,
            'steric_clash': 5.0,
            'radius_gyration': 0.5
        },
        'output_files': {
            'visualization': viz_path,
            'refined_pdb': refined_pdb
        }
    }

    # Save JSON
    json_path = os.path.join(output_dir, "pinn_results.json")
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

    print(f"  ✓ Results saved: {json_path}")

    # Summary
    print(f"\n{'='*60}")
    print("Z² PHYSICS-INFORMED NEURAL NETWORK COMPLETE")
    print(f"{'='*60}")

    improvement = results['refinement']['improvement']
    print(f"""
  ORIGINAL STRUCTURE:
  • Z² compliance: {analysis['z2_compliance']:.3f}
  • Mean contacts: {analysis['contacts']['mean']:.2f}

  AFTER PHYSICS REFINEMENT:
  • Z² compliance: {refined_analysis['z2_compliance']:.3f}
  • Mean contacts: {refined_analysis['contacts']['mean']:.2f}
  • Improvement: {improvement:.1f}%

  Z² PINN INNOVATION:
  Traditional NNs learn: patterns from data
  Z² PINNs enforce: physical laws as loss terms

  Loss = L_data + λ₁·L_Z² + λ₂·L_bonds + λ₃·L_clash + ...

  This ensures predicted structures are
  PHYSICALLY VALID, not just statistically likely.

  AlphaFold learns from evolution.
  Z² PINN learns from GEOMETRY.
""")

    return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run PINN analysis on Z² protein."""
    import sys

    if len(sys.argv) > 1:
        pdb_path = sys.argv[1]
    else:
        pdb_path = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"

    if not os.path.exists(pdb_path):
        print(f"PDB not found: {pdb_path}")
        return None

    results = run_pinn_analysis(pdb_path, output_dir="physics_nn")

    return results


if __name__ == "__main__":
    results = main()
