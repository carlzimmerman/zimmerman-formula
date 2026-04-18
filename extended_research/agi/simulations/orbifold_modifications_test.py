#!/usr/bin/env python3
"""
Orbifold Neural Network - MODIFICATION TESTS

Testing if any variant of the orbifold idea works:
1. Different scaling factors (1, √Z, Z, Z²)
2. Periodic/time-series data (where orbifold might help)
3. Latent space only (VAE-style)
4. Different projection strategies

Author: Carl Zimmerman
Date: April 17, 2026
"""

import numpy as np
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import json

# ============================================================================
# CONSTANTS
# ============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.7888
Z_SQUARED = 32 * np.pi / 3       # ≈ 33.51
SQRT_Z = np.sqrt(Z)              # ≈ 2.406
ORBIFOLD_DIM = 3

np.random.seed(42)


# ============================================================================
# IMPROVED NEURAL NETWORK WITH GRADIENT CLIPPING
# ============================================================================

class ImprovedNN:
    """Neural network with gradient clipping for stability."""

    def __init__(
        self,
        layer_sizes: List[int],
        orbifold_mode: str = "none",  # "none", "all", "latent_only"
        gradient_scale: float = 1.0,   # 1.0, sqrt(Z), Z, Z²
        clip_value: float = 5.0
    ):
        self.layer_sizes = layer_sizes
        self.orbifold_mode = orbifold_mode
        self.gradient_scale = gradient_scale
        self.clip_value = clip_value

        self.weights = []
        self.biases = []

        # Xavier initialization with smaller scale for stability
        for i in range(len(layer_sizes) - 1):
            scale = np.sqrt(1.0 / (layer_sizes[i] + layer_sizes[i+1]))
            self.weights.append(np.random.randn(layer_sizes[i], layer_sizes[i+1]) * scale)
            self.biases.append(np.zeros(layer_sizes[i+1]))

    def _project_orbifold(self, x: np.ndarray) -> np.ndarray:
        """Project first 3 dimensions to T³/Z₂ orbifold."""
        x_proj = x.copy()
        if x.shape[-1] >= ORBIFOLD_DIM:
            orb = x_proj[..., :ORBIFOLD_DIM]
            # Soft projection using tanh (differentiable)
            orb = np.pi * np.tanh(orb / np.pi)
            x_proj[..., :ORBIFOLD_DIM] = orb
        return x_proj

    def _project_torus(self, x: np.ndarray) -> np.ndarray:
        """Project to torus using sin/cos embedding."""
        x_proj = x.copy()
        if x.shape[-1] >= ORBIFOLD_DIM:
            orb = x_proj[..., :ORBIFOLD_DIM]
            # Use sin for smooth periodicity
            orb = np.sin(orb)
            x_proj[..., :ORBIFOLD_DIM] = orb
        return x_proj

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass."""
        self.activations = [x]
        n_layers = len(self.weights)
        middle_layer = n_layers // 2

        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            z = self.activations[-1] @ W + b

            # Clip for stability
            z = np.clip(z, -100, 100)

            # Apply orbifold based on mode
            if self.orbifold_mode == "all" and i < n_layers - 1:
                z = self._project_orbifold(z)
            elif self.orbifold_mode == "latent_only" and i == middle_layer:
                z = self._project_orbifold(z)
            elif self.orbifold_mode == "torus" and i < n_layers - 1:
                z = self._project_torus(z)

            # Activation
            if i < n_layers - 1:
                a = np.maximum(0, z)  # ReLU
            else:
                a = z  # Linear output

            self.activations.append(a)

        return self.activations[-1]

    def backward(self, y_true: np.ndarray, learning_rate: float) -> float:
        """Backward pass with gradient scaling and clipping."""
        y_pred = self.activations[-1]
        m = max(1, y_true.shape[0])

        # MSE loss
        diff = y_pred - y_true
        loss = np.mean(diff ** 2)

        if np.isnan(loss) or np.isinf(loss):
            return 1e10  # Return large loss on numerical issues

        # Output gradient
        delta = 2 * diff / m

        for i in range(len(self.weights) - 1, -1, -1):
            dW = self.activations[i].T @ delta
            db = np.sum(delta, axis=0)

            # Clip gradients
            dW = np.clip(dW, -self.clip_value, self.clip_value)
            db = np.clip(db, -self.clip_value, self.clip_value)

            # Apply gradient scaling for orbifold dimensions
            if self.orbifold_mode != "none" and self.gradient_scale != 1.0:
                if dW.shape[1] >= ORBIFOLD_DIM:
                    dW[:, :ORBIFOLD_DIM] /= self.gradient_scale

            # Update
            self.weights[i] -= learning_rate * dW
            self.biases[i] -= learning_rate * db

            # Propagate
            if i > 0:
                delta = (delta @ self.weights[i].T) * (self.activations[i] > 0)
                delta = np.clip(delta, -100, 100)

        return loss


# ============================================================================
# TEST DATASETS
# ============================================================================

def generate_periodic_signal(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Periodic signal prediction - where orbifold SHOULD help.
    Predict next value of a sum of sinusoids.
    """
    t = np.linspace(0, 20*np.pi, n_samples + 10)
    signal = np.sin(t) + 0.5*np.sin(2*t) + 0.3*np.sin(3*t)
    signal += np.random.randn(len(signal)) * 0.1

    # Create sliding windows
    X = np.array([signal[i:i+10] for i in range(n_samples)])
    y = signal[10:n_samples+10].reshape(-1, 1)

    return X, y


def generate_phase_data(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Phase prediction - inherently periodic.
    Given sin(θ), cos(θ), predict sin(2θ), cos(2θ).
    """
    theta = np.random.uniform(0, 2*np.pi, n_samples)
    X = np.column_stack([np.sin(theta), np.cos(theta)])
    y = np.column_stack([np.sin(2*theta), np.cos(2*theta)])
    return X, y


def generate_fourier_data(n_samples: int = 1000, n_components: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Fourier coefficient prediction.
    Given time series, predict Fourier coefficients.
    """
    X = np.random.randn(n_samples, 20)

    # Add periodic structure
    for i in range(n_samples):
        t = np.linspace(0, 2*np.pi, 20)
        for k in range(n_components):
            amp = np.random.randn() * 0.5
            X[i] += amp * np.sin((k+1) * t)

    # Target: first few Fourier coefficients (simplified)
    y = np.zeros((n_samples, n_components))
    for i in range(n_samples):
        for k in range(n_components):
            t = np.linspace(0, 2*np.pi, 20)
            y[i, k] = np.mean(X[i] * np.sin((k+1) * t))

    return X, y


def generate_rotation_data(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    3D rotation prediction - SO(3) is periodic.
    Given rotation matrix elements, predict rotation angle.
    """
    angles = np.random.uniform(0, 2*np.pi, n_samples)

    # Create rotation matrices (around z-axis for simplicity)
    X = np.zeros((n_samples, 4))
    X[:, 0] = np.cos(angles)  # R[0,0]
    X[:, 1] = np.sin(angles)  # R[0,1]
    X[:, 2] = -np.sin(angles) # R[1,0]
    X[:, 3] = np.cos(angles)  # R[1,1]

    # Target: sin and cos of angle (periodic representation)
    y = np.column_stack([np.sin(angles), np.cos(angles)])

    return X, y


# ============================================================================
# BENCHMARK
# ============================================================================

@dataclass
class ModificationResult:
    task: str
    mode: str
    scale: str
    final_loss: float
    best_loss: float
    epochs_to_best: int
    time: float


def run_modification_test(
    task_name: str,
    X: np.ndarray,
    y: np.ndarray,
    hidden_sizes: List[int],
    n_epochs: int = 300,
    learning_rate: float = 0.005
) -> List[ModificationResult]:
    """Test all modifications on a single task."""

    results = []

    input_dim = X.shape[1]
    output_dim = y.shape[1]
    layer_sizes = [input_dim] + hidden_sizes + [output_dim]

    # Normalize data
    X_mean, X_std = X.mean(axis=0), X.std(axis=0) + 1e-8
    y_mean, y_std = y.mean(axis=0), y.std(axis=0) + 1e-8
    X_norm = (X - X_mean) / X_std
    y_norm = (y - y_mean) / y_std

    # Test configurations
    configs = [
        ("none", 1.0, "Standard"),
        ("all", 1.0, "Orbifold (scale=1)"),
        ("all", SQRT_Z, "Orbifold (scale=√Z)"),
        ("all", Z, "Orbifold (scale=Z)"),
        ("all", Z_SQUARED, "Orbifold (scale=Z²)"),
        ("latent_only", 1.0, "Latent-only (scale=1)"),
        ("latent_only", SQRT_Z, "Latent-only (scale=√Z)"),
        ("torus", 1.0, "Torus (sin projection)"),
    ]

    for mode, scale, name in configs:
        np.random.seed(42)  # Same initialization

        model = ImprovedNN(
            layer_sizes,
            orbifold_mode=mode,
            gradient_scale=scale
        )

        loss_history = []
        best_loss = float('inf')
        epochs_to_best = 0

        start = time.time()

        for epoch in range(n_epochs):
            # Shuffle
            idx = np.random.permutation(len(X_norm))
            X_shuffled = X_norm[idx]
            y_shuffled = y_norm[idx]

            epoch_loss = 0.0
            batch_size = 32
            n_batches = 0

            for i in range(0, len(X_norm), batch_size):
                X_batch = X_shuffled[i:i+batch_size]
                y_batch = y_shuffled[i:i+batch_size]

                model.forward(X_batch)
                loss = model.backward(y_batch, learning_rate)
                epoch_loss += loss
                n_batches += 1

            avg_loss = epoch_loss / max(1, n_batches)
            loss_history.append(avg_loss)

            if avg_loss < best_loss:
                best_loss = avg_loss
                epochs_to_best = epoch + 1

        elapsed = time.time() - start

        results.append(ModificationResult(
            task=task_name,
            mode=mode,
            scale=name,
            final_loss=loss_history[-1] if loss_history else float('inf'),
            best_loss=best_loss,
            epochs_to_best=epochs_to_best,
            time=elapsed
        ))

    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("ORBIFOLD MODIFICATIONS TEST")
    print("=" * 70)
    print(f"\nTesting if ANY variant of orbifold helps...")
    print(f"Z = {Z:.4f}, √Z = {SQRT_Z:.4f}, Z² = {Z_SQUARED:.4f}\n")

    all_results = {}

    # Task 1: Periodic Signal
    print("-" * 50)
    print("TASK 1: Periodic Signal Prediction")
    print("-" * 50)
    X, y = generate_periodic_signal(1000)
    results = run_modification_test("Periodic", X, y, [32, 16, 8])
    all_results["periodic"] = results

    print(f"{'Method':<30} {'Best Loss':<12} {'Final Loss':<12}")
    print("-" * 54)
    for r in sorted(results, key=lambda x: x.best_loss):
        print(f"{r.scale:<30} {r.best_loss:<12.6f} {r.final_loss:<12.6f}")

    # Task 2: Phase Prediction
    print("\n" + "-" * 50)
    print("TASK 2: Phase Prediction (sin/cos → sin/cos)")
    print("-" * 50)
    X, y = generate_phase_data(1000)
    results = run_modification_test("Phase", X, y, [16, 8])
    all_results["phase"] = results

    print(f"{'Method':<30} {'Best Loss':<12} {'Final Loss':<12}")
    print("-" * 54)
    for r in sorted(results, key=lambda x: x.best_loss):
        print(f"{r.scale:<30} {r.best_loss:<12.6f} {r.final_loss:<12.6f}")

    # Task 3: Fourier Coefficients
    print("\n" + "-" * 50)
    print("TASK 3: Fourier Coefficient Prediction")
    print("-" * 50)
    X, y = generate_fourier_data(1000)
    results = run_modification_test("Fourier", X, y, [32, 16])
    all_results["fourier"] = results

    print(f"{'Method':<30} {'Best Loss':<12} {'Final Loss':<12}")
    print("-" * 54)
    for r in sorted(results, key=lambda x: x.best_loss):
        print(f"{r.scale:<30} {r.best_loss:<12.6f} {r.final_loss:<12.6f}")

    # Task 4: Rotation
    print("\n" + "-" * 50)
    print("TASK 4: Rotation Matrix → Angle")
    print("-" * 50)
    X, y = generate_rotation_data(1000)
    results = run_modification_test("Rotation", X, y, [16, 8])
    all_results["rotation"] = results

    print(f"{'Method':<30} {'Best Loss':<12} {'Final Loss':<12}")
    print("-" * 54)
    for r in sorted(results, key=lambda x: x.best_loss):
        print(f"{r.scale:<30} {r.best_loss:<12.6f} {r.final_loss:<12.6f}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: Best Method Per Task")
    print("=" * 70)

    wins = {}
    for task, results in all_results.items():
        best = min(results, key=lambda x: x.best_loss)
        wins[best.scale] = wins.get(best.scale, 0) + 1

        standard = [r for r in results if r.mode == "none"][0]
        improvement = (standard.best_loss - best.best_loss) / standard.best_loss * 100

        print(f"\n{task.upper()}:")
        print(f"  Winner: {best.scale}")
        print(f"  Best loss: {best.best_loss:.6f}")
        print(f"  vs Standard: {improvement:+.1f}%")

    print("\n" + "-" * 50)
    print("WIN COUNTS:")
    print("-" * 50)
    for method, count in sorted(wins.items(), key=lambda x: -x[1]):
        print(f"  {method}: {count} wins")

    # Final verdict
    print("\n" + "=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)

    standard_wins = wins.get("Standard", 0)
    orbifold_any = sum(v for k, v in wins.items() if "Orbifold" in k or "Latent" in k or "Torus" in k)

    if orbifold_any > standard_wins:
        print("""
  Some orbifold variants DO help on periodic tasks!

  Best performing variants:""")
        for method, count in sorted(wins.items(), key=lambda x: -x[1])[:3]:
            print(f"    - {method}: {count} wins")
        print("""
  The key insight: orbifold/torus projections help when
  the underlying data has PERIODIC structure.

  This is NOT the claimed Z² = 33.5× speedup, but there
  may be a real (modest) benefit for specific tasks.
        """)
    elif standard_wins > orbifold_any:
        print("""
  Standard networks STILL win overall.

  Even on periodic data designed to favor orbifold methods,
  the constraint doesn't consistently help.

  CONCLUSION: The orbifold idea doesn't work as claimed.
        """)
    else:
        print("""
  Results are MIXED.

  Orbifold variants help on some tasks, hurt on others.
  No consistent advantage found.
        """)

    # Save results
    output = {
        "constants": {"Z": Z, "sqrt_Z": SQRT_Z, "Z_squared": Z_SQUARED},
        "tasks": {}
    }

    for task, results in all_results.items():
        output["tasks"][task] = [
            {
                "method": r.scale,
                "mode": r.mode,
                "best_loss": r.best_loss,
                "final_loss": r.final_loss,
                "epochs_to_best": r.epochs_to_best
            }
            for r in results
        ]

    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/agi/simulations/modification_test_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return all_results


if __name__ == "__main__":
    main()
