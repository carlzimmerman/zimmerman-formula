#!/usr/bin/env python3
"""
HONEST Orbifold Neural Network Benchmark

This is a FAIR comparison between:
1. Standard neural network with SGD
2. Orbifold-constrained neural network

NO biased data, NO inflated claims. Just honest measurement.

Author: Carl Zimmerman
Date: April 17, 2026
"""

import numpy as np
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict
import json

# ============================================================================
# CONSTANTS
# ============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.7888
Z_SQUARED = 32 * np.pi / 3       # ≈ 33.51
ORBIFOLD_DIM = 3

np.random.seed(42)  # Reproducibility


# ============================================================================
# SIMPLE NEURAL NETWORK (No frameworks, pure NumPy)
# ============================================================================

class SimpleNN:
    """Minimal feedforward network for fair comparison."""

    def __init__(self, layer_sizes: List[int], use_orbifold: bool = False):
        self.layer_sizes = layer_sizes
        self.use_orbifold = use_orbifold
        self.weights = []
        self.biases = []

        # Xavier initialization
        for i in range(len(layer_sizes) - 1):
            scale = np.sqrt(2.0 / (layer_sizes[i] + layer_sizes[i+1]))
            self.weights.append(np.random.randn(layer_sizes[i], layer_sizes[i+1]) * scale)
            self.biases.append(np.zeros(layer_sizes[i+1]))

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass with ReLU activations."""
        self.activations = [x]

        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            z = self.activations[-1] @ W + b

            # Apply orbifold projection to hidden layers if enabled
            if self.use_orbifold and i < len(self.weights) - 1:
                z = self._project_orbifold(z)

            # ReLU for hidden, linear for output
            if i < len(self.weights) - 1:
                a = np.maximum(0, z)
            else:
                a = z

            self.activations.append(a)

        return self.activations[-1]

    def _project_orbifold(self, x: np.ndarray) -> np.ndarray:
        """Project first 3 dimensions to T³/Z₂ orbifold."""
        x_proj = x.copy()
        if x.shape[-1] >= ORBIFOLD_DIM:
            # Map to [0, 2π], then fold to [0, π]
            orb = x_proj[..., :ORBIFOLD_DIM]
            orb = np.remainder(orb, 2 * np.pi)
            orb = np.where(orb > np.pi, 2 * np.pi - orb, orb)
            x_proj[..., :ORBIFOLD_DIM] = orb
        return x_proj

    def backward(self, y_true: np.ndarray, learning_rate: float) -> float:
        """Backward pass with gradient descent. Returns loss."""
        y_pred = self.activations[-1]
        m = y_true.shape[0]

        # MSE loss
        loss = np.mean((y_pred - y_true) ** 2)

        # Output layer gradient
        delta = 2 * (y_pred - y_true) / m

        # Backprop through layers
        for i in range(len(self.weights) - 1, -1, -1):
            # Gradient for weights and biases
            dW = self.activations[i].T @ delta
            db = np.sum(delta, axis=0)

            # Scale orbifold gradients (this is the Z² claim)
            if self.use_orbifold and i > 0:
                # Scale gradients for orbifold dimensions
                if dW.shape[1] >= ORBIFOLD_DIM:
                    dW[:, :ORBIFOLD_DIM] /= Z_SQUARED

            # Update weights
            self.weights[i] -= learning_rate * dW
            self.biases[i] -= learning_rate * db

            # Propagate gradient (ReLU derivative)
            if i > 0:
                delta = (delta @ self.weights[i].T) * (self.activations[i] > 0)

        return loss


# ============================================================================
# BENCHMARK TASKS
# ============================================================================

def generate_xor_data(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """XOR problem - classic nonlinear benchmark."""
    X = np.random.randn(n_samples, 2)
    y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(float).reshape(-1, 1)
    return X, y


def generate_spiral_data(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """Two spirals - harder classification problem."""
    n = n_samples // 2
    theta = np.linspace(0, 4*np.pi, n)

    r1 = theta + np.random.randn(n) * 0.2
    X1 = np.column_stack([r1 * np.cos(theta), r1 * np.sin(theta)])
    y1 = np.zeros((n, 1))

    r2 = theta + np.random.randn(n) * 0.2
    X2 = np.column_stack([r2 * np.cos(theta + np.pi), r2 * np.sin(theta + np.pi)])
    y2 = np.ones((n, 1))

    X = np.vstack([X1, X2])
    y = np.vstack([y1, y2])

    # Shuffle
    idx = np.random.permutation(n_samples)
    return X[idx], y[idx]


def generate_regression_data(n_samples: int = 1000, n_features: int = 10) -> Tuple[np.ndarray, np.ndarray]:
    """Nonlinear regression - sin/cos combination."""
    X = np.random.randn(n_samples, n_features)
    y = np.sin(X[:, 0]) * np.cos(X[:, 1]) + 0.1 * np.sum(X[:, 2:], axis=1)
    y = y.reshape(-1, 1)
    return X, y


def generate_autoencoder_data(n_samples: int = 1000, n_features: int = 20) -> Tuple[np.ndarray, np.ndarray]:
    """Autoencoder task - reconstruct input."""
    X = np.random.randn(n_samples, n_features)
    return X, X


# ============================================================================
# BENCHMARK RUNNER
# ============================================================================

@dataclass
class BenchmarkResult:
    task: str
    method: str
    final_loss: float
    epochs_to_threshold: int
    training_time: float
    loss_history: List[float]


def run_benchmark(
    task_name: str,
    X: np.ndarray,
    y: np.ndarray,
    hidden_sizes: List[int] = [32, 16],
    n_epochs: int = 200,
    learning_rate: float = 0.01,
    convergence_threshold: float = 0.05
) -> Dict[str, BenchmarkResult]:
    """Run fair comparison between standard and orbifold networks."""

    input_dim = X.shape[1]
    output_dim = y.shape[1]
    layer_sizes = [input_dim] + hidden_sizes + [output_dim]

    results = {}

    for use_orbifold in [False, True]:
        method = "Orbifold" if use_orbifold else "Standard"

        # Fresh initialization
        np.random.seed(42)
        model = SimpleNN(layer_sizes, use_orbifold=use_orbifold)

        loss_history = []
        epochs_to_threshold = n_epochs

        start_time = time.time()

        for epoch in range(n_epochs):
            # Mini-batch training
            batch_size = 32
            epoch_loss = 0.0
            n_batches = 0

            indices = np.random.permutation(len(X))

            for i in range(0, len(X), batch_size):
                batch_idx = indices[i:i+batch_size]
                X_batch = X[batch_idx]
                y_batch = y[batch_idx]

                model.forward(X_batch)
                loss = model.backward(y_batch, learning_rate)
                epoch_loss += loss
                n_batches += 1

            avg_loss = epoch_loss / n_batches
            loss_history.append(avg_loss)

            if avg_loss < convergence_threshold and epochs_to_threshold == n_epochs:
                epochs_to_threshold = epoch + 1

        training_time = time.time() - start_time

        results[method.lower()] = BenchmarkResult(
            task=task_name,
            method=method,
            final_loss=loss_history[-1],
            epochs_to_threshold=epochs_to_threshold,
            training_time=training_time,
            loss_history=loss_history
        )

    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("HONEST ORBIFOLD NEURAL NETWORK BENCHMARK")
    print("=" * 70)
    print(f"\nZ² = {Z_SQUARED:.4f}")
    print("Testing if orbifold constraint actually helps...\n")

    all_results = {}

    # Test 1: XOR
    print("-" * 50)
    print("TASK 1: XOR Classification")
    print("-" * 50)
    X, y = generate_xor_data(1000)
    results = run_benchmark("XOR", X, y, hidden_sizes=[16, 8], n_epochs=100)
    all_results["xor"] = results

    for method, res in results.items():
        converged = f"epoch {res.epochs_to_threshold}" if res.epochs_to_threshold < 100 else "did not converge"
        print(f"  {res.method:10s}: loss={res.final_loss:.6f}, {converged}, time={res.training_time:.3f}s")

    # Test 2: Spiral
    print("\n" + "-" * 50)
    print("TASK 2: Spiral Classification")
    print("-" * 50)
    X, y = generate_spiral_data(1000)
    results = run_benchmark("Spiral", X, y, hidden_sizes=[32, 16], n_epochs=200)
    all_results["spiral"] = results

    for method, res in results.items():
        converged = f"epoch {res.epochs_to_threshold}" if res.epochs_to_threshold < 200 else "did not converge"
        print(f"  {res.method:10s}: loss={res.final_loss:.6f}, {converged}, time={res.training_time:.3f}s")

    # Test 3: Regression
    print("\n" + "-" * 50)
    print("TASK 3: Nonlinear Regression")
    print("-" * 50)
    X, y = generate_regression_data(1000, 10)
    results = run_benchmark("Regression", X, y, hidden_sizes=[32, 16], n_epochs=200)
    all_results["regression"] = results

    for method, res in results.items():
        converged = f"epoch {res.epochs_to_threshold}" if res.epochs_to_threshold < 200 else "did not converge"
        print(f"  {res.method:10s}: loss={res.final_loss:.6f}, {converged}, time={res.training_time:.3f}s")

    # Test 4: Autoencoder
    print("\n" + "-" * 50)
    print("TASK 4: Autoencoder (Reconstruction)")
    print("-" * 50)
    X, y = generate_autoencoder_data(1000, 20)
    results = run_benchmark("Autoencoder", X, y, hidden_sizes=[16, 8, 16], n_epochs=200)
    all_results["autoencoder"] = results

    for method, res in results.items():
        converged = f"epoch {res.epochs_to_threshold}" if res.epochs_to_threshold < 200 else "did not converge"
        print(f"  {res.method:10s}: loss={res.final_loss:.6f}, {converged}, time={res.training_time:.3f}s")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    orbifold_wins = 0
    standard_wins = 0

    for task, results in all_results.items():
        std_loss = results["standard"].final_loss
        orb_loss = results["orbifold"].final_loss

        if orb_loss < std_loss * 0.95:  # Orbifold at least 5% better
            orbifold_wins += 1
            winner = "ORBIFOLD"
        elif std_loss < orb_loss * 0.95:  # Standard at least 5% better
            standard_wins += 1
            winner = "STANDARD"
        else:
            winner = "TIE"

        improvement = (std_loss - orb_loss) / std_loss * 100 if std_loss > 0 else 0
        print(f"  {task:15s}: {winner:10s} (orbifold {improvement:+.1f}%)")

    print(f"\nOrbifold wins: {orbifold_wins}/4")
    print(f"Standard wins: {standard_wins}/4")

    # Honest assessment
    print("\n" + "-" * 50)
    print("HONEST ASSESSMENT")
    print("-" * 50)

    if orbifold_wins > standard_wins:
        print("""
  The orbifold constraint DOES appear to help on some tasks.
  However, the improvement is NOT 33.5x as claimed.

  The Z² scaling of gradients may provide some regularization
  benefit, similar to learning rate scheduling.
        """)
    elif standard_wins > orbifold_wins:
        print("""
  The orbifold constraint does NOT improve performance.
  Standard networks work better on these benchmarks.

  The Z² = 33.5x speedup claim is NOT supported by evidence.
        """)
    else:
        print("""
  Results are mixed - no clear winner.

  The orbifold constraint is neither clearly better nor worse
  than standard methods on these benchmarks.
        """)

    # Save results
    output = {
        "z_squared": Z_SQUARED,
        "tasks": {}
    }

    for task, results in all_results.items():
        output["tasks"][task] = {
            "standard": {
                "final_loss": results["standard"].final_loss,
                "epochs_to_threshold": results["standard"].epochs_to_threshold,
                "time": results["standard"].training_time
            },
            "orbifold": {
                "final_loss": results["orbifold"].final_loss,
                "epochs_to_threshold": results["orbifold"].epochs_to_threshold,
                "time": results["orbifold"].training_time
            }
        }

    output["summary"] = {
        "orbifold_wins": orbifold_wins,
        "standard_wins": standard_wins,
        "claimed_speedup": Z_SQUARED,
        "actual_speedup": "See per-task results"
    }

    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/agi/simulations/honest_benchmark_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return output


if __name__ == "__main__":
    main()
