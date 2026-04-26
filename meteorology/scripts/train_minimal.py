#!/usr/bin/env python3
"""
Minimal Training Script - Quick validation that everything works.
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import torch
import torch.nn as nn
import torch.optim as optim

print("=" * 60)
print("MINIMAL WEATHER PREDICTION TRAINING")
print("=" * 60)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

# Tiny synthetic data (no scipy dependency)
print("\nCreating tiny synthetic dataset...")
np.random.seed(42)
n_samples, n_lat, n_lon, n_channels = 100, 32, 64, 8

# Simple smooth data via low-pass filter (pure numpy)
data = np.random.randn(n_samples, n_lat, n_lon, n_channels).astype(np.float32)
# Smooth spatially with simple averaging
for _ in range(3):
    data = 0.25 * (
        data +
        np.roll(data, 1, axis=1) +
        np.roll(data, -1, axis=1) +
        np.roll(data, 1, axis=2) +
        np.roll(data, -1, axis=2)
    ) / 1.25

# Add temporal correlation
for t in range(1, n_samples):
    data[t] = 0.9 * data[t-1] + 0.1 * data[t]

# Normalize
data = (data - data.mean()) / data.std()

print(f"  Data shape: {data.shape}")

# Simple CNN model
class TinyWeatherModel(nn.Module):
    def __init__(self, n_channels):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(2 * n_channels, 32, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, n_channels, 3, padding=1),
        )

    def forward(self, x_prev, x_curr):
        x = torch.cat([x_prev, x_curr], dim=1)
        delta = self.net(x)
        return x_curr + delta

model = TinyWeatherModel(n_channels).to(device)
n_params = sum(p.numel() for p in model.parameters())
print(f"Model parameters: {n_params:,}")

# Training
optimizer = optim.Adam(model.parameters(), lr=1e-3)
data_tensor = torch.from_numpy(data).to(device)

# Reshape for conv: (B, C, H, W)
data_tensor = data_tensor.permute(0, 3, 1, 2)

print("\nTraining...")
print("-" * 40)

n_epochs = 10
for epoch in range(n_epochs):
    model.train()
    total_loss = 0
    n_batches = 0

    # Simple iteration through time
    for t in range(1, len(data_tensor) - 1):
        x_prev = data_tensor[t-1:t]
        x_curr = data_tensor[t:t+1]
        target = data_tensor[t+1:t+2]

        optimizer.zero_grad()
        pred = model(x_prev, x_curr)
        loss = ((pred - target) ** 2).mean()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        n_batches += 1

    avg_loss = total_loss / n_batches
    print(f"Epoch {epoch+1:2d}/{n_epochs}: loss = {avg_loss:.6f}")

# Evaluation
print("\n" + "-" * 40)
print("EVALUATION: Model vs Persistence")
print("-" * 40)

model.eval()
with torch.no_grad():
    # Test on last 10 samples
    test_losses_model = []
    test_losses_persist = []

    for t in range(80, 98):
        x_prev = data_tensor[t-1:t]
        x_curr = data_tensor[t:t+1]
        target = data_tensor[t+1:t+2]

        # Model prediction
        pred = model(x_prev, x_curr)
        model_loss = ((pred - target) ** 2).mean().item()

        # Persistence (predict current = next)
        persist_loss = ((x_curr - target) ** 2).mean().item()

        test_losses_model.append(model_loss)
        test_losses_persist.append(persist_loss)

    model_rmse = np.sqrt(np.mean(test_losses_model))
    persist_rmse = np.sqrt(np.mean(test_losses_persist))
    skill = 1 - model_rmse / persist_rmse

    print(f"\nModel RMSE:       {model_rmse:.6f}")
    print(f"Persistence RMSE: {persist_rmse:.6f}")
    print(f"Skill Score:      {skill:+.1%}")

    if skill > 0:
        print("\n✓ SUCCESS: Model beats persistence!")
    else:
        print("\n✗ Model needs more training")

print("\n" + "=" * 60)
print("Training complete!")
print("=" * 60)
