#!/usr/bin/env python3
"""
ERA5 Training Script - Train weather prediction model on real ERA5 data.

Usage:
    python scripts/train_era5.py --fast         # Quick test (1 week, minimal model)
    python scripts/train_era5.py --days 30      # 30 days of training data
    python scripts/train_era5.py --full         # Full training (slow!)
"""

import argparse
import sys
from pathlib import Path
import time
from functools import partial

# Force unbuffered output for real-time progress
print = partial(print, flush=True)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np

# Suppress gRPC debug messages
import os
os.environ['GRPC_VERBOSITY'] = 'ERROR'

print("=" * 70)
print("ERA5 WEATHER PREDICTION TRAINING")
print("=" * 70)

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--fast', action='store_true', help='Quick test mode (1 week)')
parser.add_argument('--days', type=int, default=7, help='Days of training data')
parser.add_argument('--epochs', type=int, default=10, help='Training epochs')
parser.add_argument('--batch_size', type=int, default=4, help='Batch size')
parser.add_argument('--full', action='store_true', help='Full training (1 year)')
args = parser.parse_args()

if args.fast:
    args.days = 7
    args.epochs = 5
elif args.full:
    args.days = 365
    args.epochs = 50

print(f"\nConfiguration:")
print(f"  Training days: {args.days}")
print(f"  Epochs: {args.epochs}")
print(f"  Batch size: {args.batch_size}")

# ============================================================================
# Step 1: Load ERA5 Data
# ============================================================================
print("\n" + "-" * 70)
print("Step 1: Loading ERA5 data from cloud...")
print("-" * 70)

from data.era5_loader import ERA5CloudLoader, FAST_CONFIG
from datetime import datetime, timedelta

loader = ERA5CloudLoader(verbose=True)

# Calculate date range
end_date = datetime(2017, 12, 31)
start_date = end_date - timedelta(days=args.days)

print(f"\nLoading data: {start_date.date()} to {end_date.date()}")

start_time = time.time()
ds = loader.load_time_range(
    start=start_date.isoformat(),
    end=end_date.isoformat(),
    config=FAST_CONFIG,
    time_step=6,  # 6-hourly
    lazy=True
)
load_time = time.time() - start_time
print(f"Dataset loaded (lazy) in {load_time:.2f}s")

# Get dimensions
n_times = len(ds.time)
n_lat = len(ds.latitude)
n_lon = len(ds.longitude)
variables = list(ds.data_vars)

print(f"\nDataset info:")
print(f"  Time steps: {n_times}")
print(f"  Spatial: {n_lat} x {n_lon}")
print(f"  Variables: {variables}")

# ============================================================================
# Step 2: Convert to NumPy Arrays
# ============================================================================
print("\n" + "-" * 70)
print("Step 2: Converting to NumPy arrays...")
print("-" * 70)

start_time = time.time()

# Load each variable and stack
data_list = []
n_channels = 0

for var in variables:
    print(f"  Loading {var}...")
    da = ds[var].compute()
    arr = da.values

    if 'level' in da.dims:
        # (time, level, lat, lon) -> (time, lat, lon, level)
        arr = np.moveaxis(arr, 1, -1)
        n_channels += arr.shape[-1]
    else:
        # (time, lat, lon) -> (time, lat, lon, 1)
        arr = arr[..., np.newaxis]
        n_channels += 1

    data_list.append(arr)

# Stack along channel dimension
data = np.concatenate(data_list, axis=-1).astype(np.float32)
convert_time = time.time() - start_time

print(f"\nConverted in {convert_time:.2f}s")
print(f"Data shape: {data.shape} (time, lat, lon, channels)")
print(f"Memory: {data.nbytes / 1e9:.2f} GB")

# ============================================================================
# Step 3: Normalize Data
# ============================================================================
print("\n" + "-" * 70)
print("Step 3: Normalizing data...")
print("-" * 70)

# Simple standardization
data_mean = data.mean(axis=(0, 1, 2), keepdims=True)
data_std = data.std(axis=(0, 1, 2), keepdims=True)
data_std = np.maximum(data_std, 1e-6)

data = (data - data_mean) / data_std

print(f"After normalization:")
print(f"  Mean: {data.mean():.6f} (should be ~0)")
print(f"  Std: {data.std():.6f} (should be ~1)")

# ============================================================================
# Step 4: Create PyTorch Model and Dataset
# ============================================================================
print("\n" + "-" * 70)
print("Step 4: Creating model and dataset...")
print("-" * 70)

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")


class WeatherDataset(Dataset):
    """Simple weather dataset - predicts next timestep from current."""

    def __init__(self, data, input_steps=2):
        # data shape: (time, lat, lon, channels)
        self.data = torch.from_numpy(data)
        self.input_steps = input_steps
        self.n_samples = len(data) - input_steps

    def __len__(self):
        return self.n_samples

    def __getitem__(self, idx):
        # Input: current and previous state
        x = self.data[idx:idx + self.input_steps]  # (2, lat, lon, channels)
        # Target: next state
        y = self.data[idx + self.input_steps]  # (lat, lon, channels)

        # Reshape to (channels, lat, lon) for conv2d
        x = x.permute(0, 3, 1, 2)  # (2, channels, lat, lon)
        x = x.reshape(-1, x.shape[2], x.shape[3])  # (2*channels, lat, lon)
        y = y.permute(2, 0, 1)  # (channels, lat, lon)

        return x, y


class WeatherNet(nn.Module):
    """UNet-style weather prediction network."""

    def __init__(self, in_channels, out_channels, hidden_dim=64):
        super().__init__()

        # Encoder
        self.enc1 = nn.Sequential(
            nn.Conv2d(in_channels, hidden_dim, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_dim, hidden_dim, 3, padding=1),
            nn.ReLU(),
        )
        self.pool1 = nn.MaxPool2d(2)

        self.enc2 = nn.Sequential(
            nn.Conv2d(hidden_dim, hidden_dim * 2, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_dim * 2, hidden_dim * 2, 3, padding=1),
            nn.ReLU(),
        )
        self.pool2 = nn.MaxPool2d(2)

        # Bottleneck
        self.bottleneck = nn.Sequential(
            nn.Conv2d(hidden_dim * 2, hidden_dim * 4, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_dim * 4, hidden_dim * 2, 3, padding=1),
            nn.ReLU(),
        )

        # Decoder
        self.up2 = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)
        self.dec2 = nn.Sequential(
            nn.Conv2d(hidden_dim * 4, hidden_dim * 2, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_dim * 2, hidden_dim, 3, padding=1),
            nn.ReLU(),
        )

        self.up1 = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)
        self.dec1 = nn.Sequential(
            nn.Conv2d(hidden_dim * 2, hidden_dim, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hidden_dim, out_channels, 3, padding=1),
        )

    def forward(self, x):
        # x shape: (batch, 2*channels, lat, lon)

        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool1(e1))

        # Bottleneck
        b = self.bottleneck(self.pool2(e2))

        # Decoder with skip connections
        d2 = self.up2(b)
        # Handle size mismatch from pooling
        if d2.shape != e2.shape:
            d2 = nn.functional.interpolate(d2, size=e2.shape[2:])
        d2 = self.dec2(torch.cat([d2, e2], dim=1))

        d1 = self.up1(d2)
        if d1.shape != e1.shape:
            d1 = nn.functional.interpolate(d1, size=e1.shape[2:])
        d1 = self.dec1(torch.cat([d1, e1], dim=1))

        # Residual connection: predict delta
        # Take the second half of input (current state) and add predicted delta
        current = x[:, x.shape[1]//2:, :, :]  # (batch, channels, lat, lon)
        return current + d1


# Create dataset and dataloader
dataset = WeatherDataset(data, input_steps=2)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0)

print(f"\nDataset created:")
print(f"  Train samples: {len(train_dataset)}")
print(f"  Val samples: {len(val_dataset)}")

# Create model
in_channels = n_channels * 2  # 2 timesteps
out_channels = n_channels
model = WeatherNet(in_channels, out_channels, hidden_dim=32).to(device)

n_params = sum(p.numel() for p in model.parameters())
print(f"\nModel created:")
print(f"  Parameters: {n_params:,}")
print(f"  Input channels: {in_channels}")
print(f"  Output channels: {out_channels}")

# ============================================================================
# Step 5: Training Loop
# ============================================================================
print("\n" + "-" * 70)
print("Step 5: Training...")
print("-" * 70)

optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-5)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

# Latitude weights for loss (cos weighting for spherical geometry)
lat_values = ds.latitude.values
lat_weights = np.cos(np.radians(lat_values))
lat_weights = lat_weights / lat_weights.mean()
lat_weights = torch.from_numpy(lat_weights).float().to(device)


def weighted_mse_loss(pred, target):
    """MSE loss weighted by latitude (cos weighting for sphere)."""
    # pred, target: (batch, channels, lat, lon)
    error = (pred - target) ** 2
    # Weight by latitude (broadcast across batch, channels, lon)
    weighted_error = error * lat_weights[None, None, :, None]
    return weighted_error.mean()


best_val_loss = float('inf')
train_losses = []
val_losses = []

for epoch in range(args.epochs):
    # Training
    model.train()
    train_loss = 0
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)

        optimizer.zero_grad()
        pred = model(x)
        loss = weighted_mse_loss(pred, y)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    train_loss /= len(train_loader)
    train_losses.append(train_loss)

    # Validation
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(device), y.to(device)
            pred = model(x)
            loss = weighted_mse_loss(pred, y)
            val_loss += loss.item()

    val_loss /= len(val_loader)
    val_losses.append(val_loss)

    scheduler.step()

    # Track best model
    if val_loss < best_val_loss:
        best_val_loss = val_loss

    print(f"Epoch {epoch+1:3d}/{args.epochs}: train_loss={train_loss:.6f}, val_loss={val_loss:.6f}")

# ============================================================================
# Step 6: Evaluation
# ============================================================================
print("\n" + "-" * 70)
print("Step 6: Evaluation vs Persistence Baseline...")
print("-" * 70)

model.eval()
model_rmses = []
persist_rmses = []

with torch.no_grad():
    for x, y in val_loader:
        x, y = x.to(device), y.to(device)

        # Model prediction
        pred = model(x)
        model_mse = weighted_mse_loss(pred, y).item()
        model_rmses.append(np.sqrt(model_mse))

        # Persistence baseline (predict current = next)
        current = x[:, x.shape[1]//2:, :, :]
        persist_mse = weighted_mse_loss(current, y).item()
        persist_rmses.append(np.sqrt(persist_mse))

model_rmse = np.mean(model_rmses)
persist_rmse = np.mean(persist_rmses)
skill = 1 - model_rmse / persist_rmse

print(f"\nResults:")
print(f"  Model RMSE:       {model_rmse:.6f}")
print(f"  Persistence RMSE: {persist_rmse:.6f}")
print(f"  Skill Score:      {skill:+.1%}")

if skill > 0:
    print("\n✓ SUCCESS: Model beats persistence baseline!")
else:
    print("\n✗ Model needs more training or data")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)

print(f"\nTraining summary:")
print(f"  Data: ERA5 cloud ({args.days} days)")
print(f"  Epochs: {args.epochs}")
print(f"  Best val loss: {best_val_loss:.6f}")
print(f"  Skill vs persistence: {skill:+.1%}")

print(f"\nNext steps:")
print(f"  1. Train longer: python scripts/train_era5.py --days 30 --epochs 50")
print(f"  2. Use full data: python scripts/train_era5.py --full")
print(f"  3. Switch to GraphCast architecture for production")
