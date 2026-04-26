"""
Training Loop for Weather Prediction

From First Principles:
======================

Weather prediction models require special training strategies:

1. AUTOREGRESSIVE ROLLOUT:
   The model predicts X_{t+Δt} from X_t.
   To forecast 10 days, we roll out 40 steps (with Δt=6h).
   Training must handle error accumulation.

2. MULTI-STEP LOSS:
   Compute loss at multiple lead times, not just one step ahead.
   This teaches the model to minimize error accumulation.
   GraphCast uses: 12h, 1d, 3d, 5d (progressive)

3. CURRICULUM LEARNING:
   Start with short rollouts (1-2 steps)
   Gradually increase to full 10-day rollouts
   This stabilizes training and prevents early divergence

4. LATITUDE WEIGHTING:
   Loss must be weighted by cos(latitude) for spherical geometry
   Otherwise polar errors dominate unfairly

5. GRADIENT CHECKPOINTING:
   Long rollouts require enormous memory for backprop
   Checkpoint intermediate states to trade compute for memory
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Dict, List, Optional, Tuple, Callable
from pathlib import Path
import numpy as np
from datetime import datetime
import json
import warnings


class WeatherLoss(nn.Module):
    """
    Latitude-weighted MSE loss for weather prediction.

    Accounts for spherical geometry: grid cells at different latitudes
    have different areas, so errors should be weighted accordingly.
    """

    def __init__(
        self,
        lat: torch.Tensor,
        variable_weights: Optional[Dict[str, float]] = None,
    ):
        """
        Args:
            lat: Latitude values in degrees, shape (n_lat,)
            variable_weights: Optional per-variable loss weights
        """
        super().__init__()

        # Compute latitude weights: w = cos(lat)
        lat_rad = torch.deg2rad(lat) if lat.abs().max() > np.pi else lat
        weights = torch.cos(lat_rad)
        weights = weights / weights.sum()  # Normalize

        self.register_buffer('lat_weights', weights)
        self.variable_weights = variable_weights or {}

    def forward(
        self,
        pred: torch.Tensor,      # (batch, lat, lon, channels)
        target: torch.Tensor,
        channel_names: Optional[List[str]] = None,
    ) -> torch.Tensor:
        """
        Compute latitude-weighted MSE loss.
        """
        # Squared error
        se = (pred - target) ** 2

        # Apply latitude weights: (n_lat,) -> (1, n_lat, 1, 1)
        weights = self.lat_weights.view(1, -1, 1, 1)
        weighted_se = se * weights

        # Apply variable weights if provided
        if channel_names and self.variable_weights:
            var_weights = torch.ones(se.shape[-1], device=se.device)
            for i, name in enumerate(channel_names):
                if name in self.variable_weights:
                    var_weights[i] = self.variable_weights[name]
            weighted_se = weighted_se * var_weights.view(1, 1, 1, -1)

        return weighted_se.mean()


class AutoregressiveLoss(nn.Module):
    """
    Multi-step loss for autoregressive training.

    Computes loss at multiple lead times with optional weighting
    to emphasize certain forecast horizons.
    """

    def __init__(
        self,
        base_loss: nn.Module,
        lead_time_weights: Optional[List[float]] = None,
    ):
        """
        Args:
            base_loss: Single-step loss function
            lead_time_weights: Weights for each lead time (default: uniform)
        """
        super().__init__()
        self.base_loss = base_loss
        self.lead_time_weights = lead_time_weights

    def forward(
        self,
        predictions: List[torch.Tensor],  # List of predictions at each lead time
        targets: List[torch.Tensor],      # List of targets
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Compute weighted sum of losses at multiple lead times.

        Returns:
            (total_loss, {lead_time: loss_value})
        """
        n_steps = len(predictions)

        if self.lead_time_weights is None:
            weights = [1.0 / n_steps] * n_steps
        else:
            weights = self.lead_time_weights
            # Normalize
            total = sum(weights)
            weights = [w / total for w in weights]

        total_loss = 0.0
        per_step_loss = {}

        for i, (pred, target, w) in enumerate(zip(predictions, targets, weights)):
            step_loss = self.base_loss(pred, target)
            total_loss = total_loss + w * step_loss
            per_step_loss[f'step_{i+1}'] = step_loss.item()

        return total_loss, per_step_loss


class GraphCastTrainer:
    """
    Training loop for GraphCast-style weather models.

    Implements:
    - Autoregressive rollout training
    - Curriculum learning (gradually increasing rollout length)
    - Gradient checkpointing for memory efficiency
    - Mixed precision training
    - Logging and checkpointing
    """

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: Optional[DataLoader] = None,
        loss_fn: Optional[nn.Module] = None,
        optimizer: Optional[optim.Optimizer] = None,
        scheduler: Optional[optim.lr_scheduler._LRScheduler] = None,
        device: str = 'cuda',
        mixed_precision: bool = True,
        gradient_checkpointing: bool = True,
        max_rollout_steps: int = 20,  # 5 days at 6h steps
        checkpoint_dir: Optional[Path] = None,
    ):
        """
        Initialize trainer.

        Args:
            model: The weather prediction model
            train_loader: Training data loader
            val_loader: Validation data loader
            loss_fn: Loss function (default: WeatherLoss)
            optimizer: Optimizer (default: AdamW)
            scheduler: Learning rate scheduler
            device: Training device
            mixed_precision: Use automatic mixed precision
            gradient_checkpointing: Use gradient checkpointing for memory
            max_rollout_steps: Maximum autoregressive steps
            checkpoint_dir: Directory for saving checkpoints
        """
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        self.mixed_precision = mixed_precision
        self.gradient_checkpointing = gradient_checkpointing
        self.max_rollout_steps = max_rollout_steps
        self.checkpoint_dir = Path(checkpoint_dir) if checkpoint_dir else None

        if self.checkpoint_dir:
            self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # Loss function
        self.loss_fn = loss_fn or self._default_loss()

        # Optimizer
        self.optimizer = optimizer or optim.AdamW(
            model.parameters(),
            lr=1e-4,
            weight_decay=0.1,
            betas=(0.9, 0.95),
        )

        # Scheduler
        self.scheduler = scheduler

        # Mixed precision scaler
        self.scaler = torch.cuda.amp.GradScaler() if mixed_precision else None

        # Training state
        self.current_epoch = 0
        self.global_step = 0
        self.best_val_loss = float('inf')
        self.history: Dict[str, List[float]] = {
            'train_loss': [],
            'val_loss': [],
            'learning_rate': [],
        }

        # Curriculum: start with short rollouts
        self.current_rollout_steps = 1

    def _default_loss(self) -> nn.Module:
        """Create default latitude-weighted loss."""
        # Get latitude from model if available
        if hasattr(self.model, 'latitude_weights'):
            lat = torch.linspace(-90, 90, self.model.n_lat)
            return WeatherLoss(lat)
        else:
            # Uniform weights as fallback
            return nn.MSELoss()

    def train_epoch(self) -> float:
        """
        Train for one epoch.

        Returns:
            Average training loss
        """
        self.model.train()
        total_loss = 0.0
        n_batches = 0

        for batch in self.train_loader:
            loss = self._train_step(batch)
            total_loss += loss
            n_batches += 1
            self.global_step += 1

            # Log progress
            if self.global_step % 100 == 0:
                print(f"  Step {self.global_step}: loss = {loss:.6f}")

        return total_loss / n_batches

    def _train_step(self, batch: Dict[str, torch.Tensor]) -> float:
        """
        Single training step with autoregressive rollout.
        """
        # Move to device
        x_input = batch['input'].to(self.device)    # (B, lat, lon, 2*C)
        targets = batch['target'].to(self.device)   # (B, n_steps, lat, lon, C)

        n_channels = targets.shape[-1]
        n_target_steps = min(targets.shape[1], self.current_rollout_steps)

        # Split input into previous and current
        x_prev = x_input[..., :n_channels]
        x_curr = x_input[..., n_channels:]

        self.optimizer.zero_grad()

        # Autoregressive rollout
        predictions = []
        target_list = []

        with torch.cuda.amp.autocast(enabled=self.mixed_precision):
            for step in range(n_target_steps):
                # Forward pass
                if self.gradient_checkpointing and step > 0:
                    # Use checkpointing for intermediate steps
                    delta_x = torch.utils.checkpoint.checkpoint(
                        self.model, x_curr, x_prev
                    )
                else:
                    delta_x = self.model(x_curr, x_prev)

                # Predict next state
                x_next = x_curr + delta_x

                predictions.append(x_next)
                target_list.append(targets[:, step])

                # Prepare for next step
                x_prev = x_curr
                x_curr = x_next

            # Compute multi-step loss
            if isinstance(self.loss_fn, AutoregressiveLoss):
                loss, _ = self.loss_fn(predictions, target_list)
            else:
                # Simple average over steps
                loss = sum(
                    self.loss_fn(p, t) for p, t in zip(predictions, target_list)
                ) / len(predictions)

        # Backward pass
        if self.scaler:
            self.scaler.scale(loss).backward()
            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.scaler.step(self.optimizer)
            self.scaler.update()
        else:
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()

        return loss.item()

    @torch.no_grad()
    def validate(self) -> Dict[str, float]:
        """
        Run validation.

        Returns:
            Dictionary of validation metrics
        """
        if self.val_loader is None:
            return {}

        self.model.eval()
        total_loss = 0.0
        per_step_losses = {}
        n_batches = 0

        for batch in self.val_loader:
            x_input = batch['input'].to(self.device)
            targets = batch['target'].to(self.device)

            n_channels = targets.shape[-1]
            n_target_steps = targets.shape[1]

            x_prev = x_input[..., :n_channels]
            x_curr = x_input[..., n_channels:]

            # Full rollout for validation
            predictions = []
            for step in range(n_target_steps):
                delta_x = self.model(x_curr, x_prev)
                x_next = x_curr + delta_x
                predictions.append(x_next)
                x_prev = x_curr
                x_curr = x_next

            # Compute losses at each step
            for i, (pred, target) in enumerate(zip(predictions, targets.unbind(1))):
                step_loss = self.loss_fn(pred, target).item()

                key = f'val_loss_step_{i+1}'
                if key not in per_step_losses:
                    per_step_losses[key] = 0.0
                per_step_losses[key] += step_loss

            total_loss += sum(
                self.loss_fn(p, t).item()
                for p, t in zip(predictions, targets.unbind(1))
            ) / n_target_steps

            n_batches += 1

        # Average
        metrics = {'val_loss': total_loss / n_batches}
        for key in per_step_losses:
            metrics[key] = per_step_losses[key] / n_batches

        return metrics

    def fit(
        self,
        n_epochs: int,
        curriculum_schedule: Optional[Dict[int, int]] = None,
    ):
        """
        Full training loop.

        Args:
            n_epochs: Number of epochs
            curriculum_schedule: {epoch: rollout_steps} for curriculum learning
                Default: start with 1 step, increase by 1 every 5 epochs
        """
        if curriculum_schedule is None:
            curriculum_schedule = {i * 5: min(i + 1, self.max_rollout_steps)
                                   for i in range(self.max_rollout_steps)}

        print(f"Starting training for {n_epochs} epochs")
        print(f"Max rollout steps: {self.max_rollout_steps}")
        print(f"Device: {self.device}")
        print(f"Mixed precision: {self.mixed_precision}")
        print()

        for epoch in range(self.current_epoch, n_epochs):
            self.current_epoch = epoch

            # Update curriculum
            if epoch in curriculum_schedule:
                self.current_rollout_steps = curriculum_schedule[epoch]
                print(f"Curriculum update: rollout_steps = {self.current_rollout_steps}")

            # Train
            print(f"Epoch {epoch + 1}/{n_epochs}")
            train_loss = self.train_epoch()
            self.history['train_loss'].append(train_loss)

            # Validate
            val_metrics = self.validate()
            val_loss = val_metrics.get('val_loss', float('inf'))
            self.history['val_loss'].append(val_loss)

            # Learning rate
            if self.scheduler:
                self.scheduler.step()
            lr = self.optimizer.param_groups[0]['lr']
            self.history['learning_rate'].append(lr)

            # Print progress
            print(f"  Train loss: {train_loss:.6f}")
            print(f"  Val loss:   {val_loss:.6f}")
            print(f"  LR:         {lr:.2e}")

            # Save best model
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                if self.checkpoint_dir:
                    self.save_checkpoint('best.pt')
                    print(f"  Saved best model (val_loss = {val_loss:.6f})")

            # Regular checkpoint
            if self.checkpoint_dir and (epoch + 1) % 10 == 0:
                self.save_checkpoint(f'epoch_{epoch + 1}.pt')

            print()

        print("Training complete!")
        return self.history

    def save_checkpoint(self, filename: str):
        """Save training checkpoint."""
        path = self.checkpoint_dir / filename

        checkpoint = {
            'epoch': self.current_epoch,
            'global_step': self.global_step,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'best_val_loss': self.best_val_loss,
            'history': self.history,
            'current_rollout_steps': self.current_rollout_steps,
        }

        if self.scheduler:
            checkpoint['scheduler_state_dict'] = self.scheduler.state_dict()

        if self.scaler:
            checkpoint['scaler_state_dict'] = self.scaler.state_dict()

        torch.save(checkpoint, path)

    def load_checkpoint(self, path: Path):
        """Load training checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)

        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.current_epoch = checkpoint['epoch'] + 1
        self.global_step = checkpoint['global_step']
        self.best_val_loss = checkpoint['best_val_loss']
        self.history = checkpoint['history']
        self.current_rollout_steps = checkpoint.get('current_rollout_steps', 1)

        if self.scheduler and 'scheduler_state_dict' in checkpoint:
            self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

        if self.scaler and 'scaler_state_dict' in checkpoint:
            self.scaler.load_state_dict(checkpoint['scaler_state_dict'])

        print(f"Resumed from epoch {self.current_epoch}")
