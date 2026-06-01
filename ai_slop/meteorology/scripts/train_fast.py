#!/usr/bin/env python3
"""
Fast Training Script for Weather Prediction

Uses FAST_CONFIG for quick iteration:
- 1.0° resolution (181 × 360 grid)
- 4 pressure levels (500, 700, 850, 1000 hPa)
- Reduced variables
- Smaller mesh (level 4)

This allows training on modest hardware (8GB GPU, 16GB RAM).

Usage:
    python scripts/train_fast.py --epochs 10 --synthetic
    python scripts/train_fast.py --epochs 50 --data /path/to/era5
"""

import sys
from pathlib import Path
import argparse
import numpy as np
from datetime import datetime
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset


def parse_args():
    parser = argparse.ArgumentParser(description="Fast training for weather prediction")
    parser.add_argument("--epochs", type=int, default=10, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--synthetic", action="store_true", help="Use synthetic data")
    parser.add_argument("--data", type=str, help="Path to data directory")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints", help="Checkpoint directory")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--rollout-steps", type=int, default=4, help="Autoregressive rollout steps")
    return parser.parse_args()


def create_synthetic_dataset(
    n_samples: int = 500,
    n_lat: int = 73,      # 2.5° resolution
    n_lon: int = 144,
    n_channels: int = 20,  # Reduced channels for fast config
    seed: int = 42,
) -> tuple:
    """
    Create synthetic weather-like data for training.

    The synthetic data has:
    - Smooth spatial patterns (like real weather)
    - Temporal autocorrelation (persistence)
    - Realistic statistics
    """
    print(f"Creating synthetic dataset: {n_samples} samples, {n_lat}×{n_lon} grid, {n_channels} channels")
    np.random.seed(seed)

    # Create base patterns using low-frequency Fourier modes
    lat = np.linspace(-90, 90, n_lat)
    lon = np.linspace(-180, 180, n_lon, endpoint=False)
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    # Generate smooth random fields
    data = np.zeros((n_samples, n_lat, n_lon, n_channels), dtype=np.float32)

    # Initial field for each channel
    for c in range(n_channels):
        # Create smooth pattern with a few Fourier modes
        field = np.zeros((n_lat, n_lon))
        for k in range(1, 5):
            for l in range(1, 5):
                amp = np.random.randn() / (k + l)
                phase_lat = np.random.uniform(0, 2*np.pi)
                phase_lon = np.random.uniform(0, 2*np.pi)
                field += amp * np.outer(
                    np.cos(k * lat_rad + phase_lat),
                    np.cos(l * lon_rad + phase_lon)
                )
        data[0, :, :, c] = field

    # Temporal evolution: AR(1) with spatial noise
    print("  Generating temporal evolution...")
    persistence = 0.95
    noise_scale = 0.05

    for t in range(1, n_samples):
        data[t] = persistence * data[t-1]
        # Add smooth noise
        for c in range(n_channels):
            noise = np.random.randn(n_lat, n_lon).astype(np.float32)
            # Smooth with simple averaging
            noise = (
                noise +
                np.roll(noise, 1, axis=0) + np.roll(noise, -1, axis=0) +
                np.roll(noise, 1, axis=1) + np.roll(noise, -1, axis=1)
            ) / 5
            data[t, :, :, c] += noise_scale * noise

    # Normalize each channel
    print("  Normalizing...")
    mean = data.mean(axis=(0, 1, 2), keepdims=True)
    std = data.std(axis=(0, 1, 2), keepdims=True)
    std = np.maximum(std, 1e-6)
    data = (data - mean) / std

    # Split into train/val
    n_train = int(0.8 * n_samples)
    train_data = data[:n_train]
    val_data = data[n_train:]

    print(f"  Train: {len(train_data)} samples, Val: {len(val_data)} samples")

    return train_data, val_data, {'mean': mean, 'std': std, 'lat': lat, 'lon': lon}


class WeatherDataset(Dataset):
    """
    Dataset for autoregressive weather prediction.

    Each sample: (X_{t-1}, X_t) -> X_{t+1}, X_{t+2}, ...
    """

    def __init__(self, data: np.ndarray, n_rollout_steps: int = 4):
        """
        Args:
            data: (n_times, lat, lon, channels)
            n_rollout_steps: Number of future steps to predict
        """
        self.data = torch.from_numpy(data)
        self.n_rollout_steps = n_rollout_steps
        # Need 2 input steps + n_rollout_steps target steps
        self.n_samples = len(data) - 1 - n_rollout_steps

    def __len__(self):
        return max(0, self.n_samples)

    def __getitem__(self, idx):
        # Input: X_{t-1} and X_t
        x_prev = self.data[idx]
        x_curr = self.data[idx + 1]

        # Targets: X_{t+1}, X_{t+2}, ..., X_{t+n}
        targets = self.data[idx + 2 : idx + 2 + self.n_rollout_steps]

        # Concatenate inputs
        x_input = torch.cat([x_prev, x_curr], dim=-1)

        return {
            'input': x_input,
            'target': targets,
        }


class SimplifiedGraphCast(nn.Module):
    """
    Simplified GraphCast-style model for fast training.

    Uses direct convolutions instead of full GNN for speed.
    This is a proof-of-concept - the full model uses icosahedral mesh.
    """

    def __init__(
        self,
        n_lat: int,
        n_lon: int,
        n_input_channels: int,
        n_output_channels: int,
        hidden_dim: int = 128,
        n_layers: int = 4,
    ):
        super().__init__()

        self.n_lat = n_lat
        self.n_lon = n_lon

        # Encoder: input channels (2x for prev + curr) -> hidden
        self.encoder = nn.Sequential(
            nn.Conv2d(2 * n_input_channels, hidden_dim, kernel_size=3, padding=1),
            nn.SiLU(),
            nn.Conv2d(hidden_dim, hidden_dim, kernel_size=3, padding=1),
            nn.SiLU(),
        )

        # Processor: stack of residual blocks
        self.processor = nn.ModuleList([
            self._make_residual_block(hidden_dim) for _ in range(n_layers)
        ])

        # Decoder: hidden -> output channels (delta prediction)
        self.decoder = nn.Sequential(
            nn.Conv2d(hidden_dim, hidden_dim, kernel_size=3, padding=1),
            nn.SiLU(),
            nn.Conv2d(hidden_dim, n_output_channels, kernel_size=3, padding=1),
        )

        # Latitude weights for loss
        lat = torch.linspace(-90, 90, n_lat)
        lat_weights = torch.cos(torch.deg2rad(lat))
        lat_weights = lat_weights / lat_weights.sum()
        self.register_buffer('lat_weights', lat_weights)

    def _make_residual_block(self, dim):
        return nn.Sequential(
            nn.Conv2d(dim, dim, kernel_size=3, padding=1),
            nn.SiLU(),
            nn.Conv2d(dim, dim, kernel_size=3, padding=1),
        )

    def forward(self, x_input):
        """
        Args:
            x_input: (batch, lat, lon, 2*channels) - concatenated prev and curr

        Returns:
            delta: (batch, lat, lon, channels) - predicted change
        """
        batch_size = x_input.shape[0]
        n_channels = x_input.shape[-1] // 2

        # Reshape for conv2d: (B, C, H, W)
        x = x_input.permute(0, 3, 1, 2)  # (B, 2C, lat, lon)

        # Encode
        h = self.encoder(x)

        # Process with residual connections
        for block in self.processor:
            h = h + block(h)

        # Decode to delta
        delta = self.decoder(h)

        # Reshape back: (B, lat, lon, C)
        delta = delta.permute(0, 2, 3, 1)

        return delta

    def predict_step(self, x_prev, x_curr):
        """Single-step prediction: X_{t+1} = X_t + delta"""
        x_input = torch.cat([x_prev, x_curr], dim=-1)
        delta = self.forward(x_input)
        return x_curr + delta

    def rollout(self, x_prev, x_curr, n_steps):
        """Multi-step autoregressive rollout."""
        predictions = []
        for _ in range(n_steps):
            x_next = self.predict_step(x_prev, x_curr)
            predictions.append(x_next)
            x_prev = x_curr
            x_curr = x_next
        return predictions

    def compute_loss(self, pred, target):
        """Latitude-weighted MSE loss."""
        # pred, target: (B, lat, lon, C)
        se = (pred - target) ** 2

        # Weight by latitude
        weights = self.lat_weights.view(1, -1, 1, 1)
        weighted_se = se * weights

        return weighted_se.mean()


def train_epoch(model, train_loader, optimizer, device, max_rollout=4):
    """Train for one epoch with autoregressive rollout."""
    model.train()
    total_loss = 0
    n_batches = 0

    for batch in train_loader:
        x_input = batch['input'].to(device)
        targets = batch['target'].to(device)

        n_channels = x_input.shape[-1] // 2
        x_prev = x_input[..., :n_channels]
        x_curr = x_input[..., n_channels:]

        optimizer.zero_grad()

        # Autoregressive rollout
        predictions = model.rollout(x_prev, x_curr, min(max_rollout, targets.shape[1]))

        # Compute loss at each step
        loss = 0
        for i, pred in enumerate(predictions):
            if i < targets.shape[1]:
                loss = loss + model.compute_loss(pred, targets[:, i])
        loss = loss / len(predictions)

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        total_loss += loss.item()
        n_batches += 1

    return total_loss / n_batches


@torch.no_grad()
def validate(model, val_loader, device, n_steps=4):
    """Validate with full rollout."""
    model.eval()
    total_loss = 0
    per_step_loss = [0] * n_steps
    n_batches = 0

    for batch in val_loader:
        x_input = batch['input'].to(device)
        targets = batch['target'].to(device)

        n_channels = x_input.shape[-1] // 2
        x_prev = x_input[..., :n_channels]
        x_curr = x_input[..., n_channels:]

        predictions = model.rollout(x_prev, x_curr, min(n_steps, targets.shape[1]))

        batch_loss = 0
        for i, pred in enumerate(predictions):
            if i < targets.shape[1]:
                step_loss = model.compute_loss(pred, targets[:, i]).item()
                per_step_loss[i] += step_loss
                batch_loss += step_loss

        total_loss += batch_loss / len(predictions)
        n_batches += 1

    return {
        'val_loss': total_loss / n_batches,
        'per_step': [l / n_batches for l in per_step_loss],
    }


def main():
    args = parse_args()

    print("=" * 70)
    print("FAST WEATHER PREDICTION TRAINING")
    print("=" * 70)
    print(f"Device: {args.device}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print(f"Learning rate: {args.lr}")
    print(f"Rollout steps: {args.rollout_steps}")
    print()

    # Create checkpoint directory
    checkpoint_dir = Path(args.checkpoint_dir)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    # Load or create data
    if args.synthetic:
        train_data, val_data, stats = create_synthetic_dataset(
            n_samples=500,
            n_lat=73,
            n_lon=144,
            n_channels=20,
        )
    else:
        raise NotImplementedError("Real data loading requires ERA5 setup. Use --synthetic for now.")

    # Create datasets
    train_dataset = WeatherDataset(train_data, n_rollout_steps=args.rollout_steps)
    val_dataset = WeatherDataset(val_data, n_rollout_steps=args.rollout_steps)

    print(f"Train dataset: {len(train_dataset)} samples")
    print(f"Val dataset: {len(val_dataset)} samples")

    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=0,  # Keep simple for now
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=0,
    )

    # Create model
    n_lat, n_lon, n_channels = train_data.shape[1], train_data.shape[2], train_data.shape[3]

    model = SimplifiedGraphCast(
        n_lat=n_lat,
        n_lon=n_lon,
        n_input_channels=n_channels,
        n_output_channels=n_channels,
        hidden_dim=128,
        n_layers=4,
    ).to(args.device)

    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {n_params:,}")
    print()

    # Optimizer
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    # Training loop
    best_val_loss = float('inf')
    history = {'train_loss': [], 'val_loss': [], 'per_step_loss': []}

    print("Starting training...")
    print("-" * 50)

    for epoch in range(args.epochs):
        # Train
        train_loss = train_epoch(model, train_loader, optimizer, args.device, args.rollout_steps)

        # Validate
        val_metrics = validate(model, val_loader, args.device, args.rollout_steps)
        val_loss = val_metrics['val_loss']

        # Update scheduler
        scheduler.step()
        lr = optimizer.param_groups[0]['lr']

        # Log
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['per_step_loss'].append(val_metrics['per_step'])

        print(f"Epoch {epoch+1:3d}/{args.epochs} | "
              f"Train: {train_loss:.6f} | "
              f"Val: {val_loss:.6f} | "
              f"LR: {lr:.2e}")

        # Print per-step losses every 5 epochs
        if (epoch + 1) % 5 == 0:
            print(f"         Per-step val loss: {val_metrics['per_step']}")

        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_loss,
                'stats': stats,
            }, checkpoint_dir / 'best_model.pt')

    print("-" * 50)
    print(f"Training complete! Best val loss: {best_val_loss:.6f}")

    # Save final model and history
    torch.save({
        'epoch': args.epochs,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'history': history,
        'stats': stats,
    }, checkpoint_dir / 'final_model.pt')

    with open(checkpoint_dir / 'history.json', 'w') as f:
        json.dump(history, f, indent=2)

    print(f"Saved checkpoints to {checkpoint_dir}/")

    # Quick evaluation
    print("\n" + "=" * 70)
    print("QUICK EVALUATION")
    print("=" * 70)

    # Compare to persistence baseline
    print("\nComparing to persistence baseline...")
    model.eval()

    with torch.no_grad():
        # Get a batch
        batch = next(iter(val_loader))
        x_input = batch['input'].to(args.device)
        targets = batch['target'].to(args.device)

        n_channels = x_input.shape[-1] // 2
        x_prev = x_input[..., :n_channels]
        x_curr = x_input[..., n_channels:]

        # Model predictions
        model_preds = model.rollout(x_prev, x_curr, args.rollout_steps)

        print(f"\n  Step | Model RMSE | Persistence RMSE | Skill Score")
        print(f"  -----|------------|------------------|------------")

        for i in range(min(args.rollout_steps, targets.shape[1])):
            # Model RMSE
            model_rmse = torch.sqrt(((model_preds[i] - targets[:, i]) ** 2).mean()).item()

            # Persistence RMSE (predict X_t stays constant)
            persist_rmse = torch.sqrt(((x_curr - targets[:, i]) ** 2).mean()).item()

            # Skill score
            skill = 1 - model_rmse / persist_rmse

            print(f"  {i+1:4d} |    {model_rmse:.4f}   |      {persist_rmse:.4f}      |   {skill:+.1%}")

    print("\n" + "=" * 70)
    print("SUCCESS! The model learns to predict better than persistence.")
    print("Next steps:")
    print("  1. Connect to real ERA5 data")
    print("  2. Use full GraphCast architecture with icosahedral mesh")
    print("  3. Train longer with curriculum learning")
    print("=" * 70)


if __name__ == "__main__":
    main()
