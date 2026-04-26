"""
GraphCast Model Implementation from First Principles

The complete encoder-processor-decoder architecture for weather prediction.

Architecture Overview:
======================

1. ENCODER (Grid → Mesh)
   - Interpolates lat-lon grid data to icosahedral mesh
   - Embeds interpolated values with mesh node features
   - Produces initial hidden state for each mesh node

2. PROCESSOR (Mesh → Mesh)
   - 16 layers of message passing on the multi-mesh
   - Long-range edges allow global information flow
   - Residual connections for gradient stability

3. DECODER (Mesh → Grid)
   - Projects mesh hidden states to output variables
   - Interpolates back to lat-lon grid
   - Produces predictions as residuals (ΔX = X_{t+Δt} - X_t)

Physical Interpretation:
========================

The model learns the mapping:
    X_{t+Δt} = X_t + NN(X_t, X_{t-Δt})

This residual formulation:
1. Makes it easier to learn identity (no change)
2. Concentrates capacity on predicting changes
3. Naturally handles different variable scales
4. Mirrors finite difference time-stepping

The loss function:
    L = Σᵢ wᵢ · ||y_pred - y_true||²

Where wᵢ = cos(φᵢ) accounts for spherical geometry (area weighting).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional, Dict, List
import numpy as np

from .message_passing import MLP, GraphNetwork, build_edge_index
from .encoder_decoder import GridToMeshEncoder, MeshToGridDecoder, BilinearInterpolator


class GraphCastProcessor(nn.Module):
    """
    The core processor: message passing on the multi-mesh.

    From first principles, this is analogous to:
    - Time-stepping a PDE with implicit methods
    - Iterative relaxation (like Gauss-Seidel)
    - Multi-grid methods (coarse → fine correction)

    The multi-mesh structure with long-range edges from coarse levels
    allows information to propagate globally in few steps, similar to
    how multigrid methods achieve fast convergence.
    """

    def __init__(
        self,
        node_dim: int = 256,
        edge_dim: int = 64,
        hidden_dim: int = 512,
        n_layers: int = 16,
    ):
        super().__init__()

        self.gnn = GraphNetwork(
            node_dim=node_dim,
            edge_dim=edge_dim,
            hidden_dim=hidden_dim,
            n_layers=n_layers,
        )

    def forward(
        self,
        node_features: torch.Tensor,
        edge_features: torch.Tensor,
        edge_index: torch.Tensor,
    ) -> torch.Tensor:
        """
        Process node features through the GNN.

        Args:
            node_features: (batch, n_mesh, node_dim) or (n_mesh, node_dim)
            edge_features: (n_edges, edge_dim)
            edge_index: (2, n_edges)

        Returns:
            Processed node features with same shape as input
        """
        # Handle batch dimension
        has_batch = node_features.dim() == 3

        if has_batch:
            batch_size, n_nodes, node_dim = node_features.shape
            # Process each batch item
            outputs = []
            for b in range(batch_size):
                out_nodes, _ = self.gnn(
                    node_features[b], edge_features, edge_index
                )
                outputs.append(out_nodes)
            return torch.stack(outputs, dim=0)
        else:
            out_nodes, _ = self.gnn(node_features, edge_features, edge_index)
            return out_nodes


class GraphCastModel(nn.Module):
    """
    Complete GraphCast model for weather prediction.

    Input: X_t, X_{t-Δt} (current and previous atmospheric state)
    Output: ΔX = X_{t+Δt} - X_t (predicted change)

    The model is trained autoregressively:
    1. Predict Δt = 6 hours ahead
    2. Add prediction to input: X_{t+6h} = X_t + ΔX
    3. Roll out to 10 days by iterating

    Loss is computed on the prediction error at each step,
    with latitude weighting for spherical geometry.
    """

    def __init__(
        self,
        grid_lat: np.ndarray,
        grid_lon: np.ndarray,
        mesh,  # IcosahedralMesh instance
        n_input_vars: int = 78,
        n_output_vars: int = 78,
        node_dim: int = 256,
        edge_dim: int = 64,
        hidden_dim: int = 512,
        n_processor_layers: int = 16,
    ):
        """
        Initialize the GraphCast model.

        Args:
            grid_lat: (n_lat,) array of grid latitudes in radians
            grid_lon: (n_lon,) array of grid longitudes in radians
            mesh: IcosahedralMesh instance
            n_input_vars: Number of input atmospheric variables × pressure levels
            n_output_vars: Number of output variables (usually = n_input_vars)
            node_dim: Hidden dimension for mesh nodes
            edge_dim: Hidden dimension for mesh edges
            hidden_dim: Hidden dimension for MLPs
            n_processor_layers: Number of message passing layers
        """
        super().__init__()

        self.n_input_vars = n_input_vars
        self.n_output_vars = n_output_vars

        finest_mesh = mesh.get_finest_mesh()
        mesh_lat = finest_mesh.lat
        mesh_lon = finest_mesh.lon

        # Get mesh node features
        mesh_features = mesh.get_node_features()
        n_mesh_features = 7  # sin_lat, cos_lat, sin_lon, cos_lon, x, y, z

        # Build mesh feature tensor
        self.register_buffer(
            'mesh_node_features',
            torch.tensor(np.stack([
                mesh_features['sin_lat'],
                mesh_features['cos_lat'],
                mesh_features['sin_lon'],
                mesh_features['cos_lon'],
                mesh_features['x'],
                mesh_features['y'],
                mesh_features['z'],
            ], axis=-1), dtype=torch.float32)
        )

        # Encoder: Grid → Mesh
        # Input includes X_t and X_{t-Δt}, so 2× the variables
        self.encoder = GridToMeshEncoder(
            grid_lat=grid_lat,
            grid_lon=grid_lon,
            mesh_lat=mesh_lat,
            mesh_lon=mesh_lon,
            n_input_channels=2 * n_input_vars,  # Current + previous state
            n_mesh_features=n_mesh_features,
            hidden_dim=hidden_dim,
            output_dim=node_dim,
        )

        # Processor: Mesh → Mesh (GNN)
        self.processor = GraphCastProcessor(
            node_dim=node_dim,
            edge_dim=edge_dim,
            hidden_dim=hidden_dim,
            n_layers=n_processor_layers,
        )

        # Decoder: Mesh → Grid
        self.decoder = MeshToGridDecoder(
            grid_lat=grid_lat,
            grid_lon=grid_lon,
            mesh_lat=mesh_lat,
            mesh_lon=mesh_lon,
            input_dim=node_dim,
            hidden_dim=hidden_dim,
            n_output_channels=n_output_vars,
        )

        # Build edge index and features
        self._build_mesh_graph(mesh, edge_dim)

        # Store grid info for loss computation
        self.register_buffer(
            'latitude_weights',
            torch.tensor(np.cos(grid_lat), dtype=torch.float32)
        )
        self.n_lat = len(grid_lat)
        self.n_lon = len(grid_lon)

    def _build_mesh_graph(self, mesh, edge_dim: int):
        """Build the multi-mesh graph structure."""
        # Get edges from all mesh levels (multi-mesh)
        multi_mesh_edges = mesh.get_multi_mesh_edges()

        # Build bidirectional edge index
        edge_index = build_edge_index(multi_mesh_edges, bidirectional=True)
        self.register_buffer('edge_index', edge_index)

        # Get edge features from finest mesh (approximate)
        edge_features = mesh.get_edge_features()
        n_edges = len(multi_mesh_edges)

        # Build edge feature tensor
        # For multi-mesh, we use distance-based features
        finest = mesh.get_finest_mesh()
        edge_feat_list = []

        for v1, v2 in multi_mesh_edges:
            # Compute features for this edge
            dx = finest.vertices[v2, 0] - finest.vertices[v1, 0]
            dy = finest.vertices[v2, 1] - finest.vertices[v1, 1]
            dz = finest.vertices[v2, 2] - finest.vertices[v1, 2]
            dist = np.sqrt(dx**2 + dy**2 + dz**2)

            edge_feat_list.append([dx, dy, dz, dist])

        edge_features_np = np.array(edge_feat_list, dtype=np.float32)

        # Embed edge features to edge_dim
        self.edge_embed = MLP(
            input_dim=4,  # dx, dy, dz, dist
            hidden_dim=edge_dim,
            output_dim=edge_dim,
            n_layers=2,
        )

        self.register_buffer(
            'raw_edge_features',
            torch.tensor(edge_features_np, dtype=torch.float32)
        )

        # For bidirectional, duplicate and flip direction features
        raw_forward = self.raw_edge_features
        raw_backward = raw_forward.clone()
        raw_backward[:, :3] *= -1  # Flip direction
        self.register_buffer(
            'raw_edge_features_bidir',
            torch.cat([raw_forward, raw_backward], dim=0)
        )

    def forward(
        self,
        x_current: torch.Tensor,   # (batch, n_lat, n_lon, n_vars)
        x_previous: torch.Tensor,  # (batch, n_lat, n_lon, n_vars)
    ) -> torch.Tensor:
        """
        Predict the change ΔX = X_{t+Δt} - X_t.

        Args:
            x_current: Atmospheric state at time t
            x_previous: Atmospheric state at time t - Δt

        Returns:
            delta_x: Predicted change, shape (batch, n_lat, n_lon, n_vars)
        """
        # Concatenate current and previous states
        x_input = torch.cat([x_current, x_previous], dim=-1)

        # Encode: Grid → Mesh
        node_features = self.encoder(x_input, self.mesh_node_features)

        # Embed edge features
        edge_features = self.edge_embed(self.raw_edge_features_bidir)

        # Process: Mesh → Mesh (GNN message passing)
        node_features = self.processor(
            node_features, edge_features, self.edge_index
        )

        # Decode: Mesh → Grid
        delta_x = self.decoder(node_features)

        return delta_x

    def predict_step(
        self,
        x_current: torch.Tensor,
        x_previous: torch.Tensor,
    ) -> torch.Tensor:
        """
        Predict the next state X_{t+Δt} = X_t + ΔX.
        """
        delta_x = self.forward(x_current, x_previous)
        return x_current + delta_x

    def rollout(
        self,
        x_init: torch.Tensor,      # X_0
        x_prev: torch.Tensor,      # X_{-Δt}
        n_steps: int,
    ) -> List[torch.Tensor]:
        """
        Autoregressive rollout for multi-step prediction.

        Args:
            x_init: Initial state (t=0)
            x_prev: Previous state (t=-Δt)
            n_steps: Number of Δt steps to predict

        Returns:
            List of predicted states [X_Δt, X_2Δt, ..., X_{n·Δt}]
        """
        predictions = []
        x_current = x_init
        x_previous = x_prev

        for _ in range(n_steps):
            x_next = self.predict_step(x_current, x_previous)
            predictions.append(x_next)
            x_previous = x_current
            x_current = x_next

        return predictions

    def compute_loss(
        self,
        pred: torch.Tensor,
        target: torch.Tensor,
        latitude_weighted: bool = True,
    ) -> torch.Tensor:
        """
        Compute latitude-weighted MSE loss.

        From first principles:
        On a sphere, the area element is dA = R²cos(φ)dφdλ.
        An unweighted loss would over-penalize polar errors.
        We weight by cos(latitude) to give equal importance per unit area.

        Args:
            pred: Predicted state (batch, n_lat, n_lon, n_vars)
            target: Target state (batch, n_lat, n_lon, n_vars)
            latitude_weighted: Whether to apply cos(lat) weighting

        Returns:
            Scalar loss value
        """
        # Squared error
        se = (pred - target) ** 2  # (B, lat, lon, vars)

        if latitude_weighted:
            # Weight by cos(latitude)
            # latitude_weights: (n_lat,) → (1, n_lat, 1, 1)
            weights = self.latitude_weights.view(1, -1, 1, 1)
            # Normalize weights to sum to n_lat
            weights = weights * self.n_lat / weights.sum()
            se = se * weights

        # Mean over all dimensions
        loss = se.mean()

        return loss


def create_graphcast_model(
    resolution_deg: float = 1.0,
    mesh_level: int = 5,
    n_vars: int = 78,
    **kwargs
) -> GraphCastModel:
    """
    Factory function to create a GraphCast model.

    Args:
        resolution_deg: Grid resolution in degrees (0.25 for ERA5)
        mesh_level: Icosahedral mesh refinement level (5 or 6)
        n_vars: Number of atmospheric variables
        **kwargs: Additional arguments for GraphCastModel

    Returns:
        Configured GraphCastModel instance
    """
    # Import mesh here to avoid circular imports
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from geometry.icosahedral_mesh import IcosahedralMesh

    # Create grid coordinates
    n_lat = int(180 / resolution_deg) + 1
    n_lon = int(360 / resolution_deg)

    grid_lat = np.linspace(-np.pi/2, np.pi/2, n_lat)
    grid_lon = np.linspace(-np.pi, np.pi, n_lon, endpoint=False)

    # Create icosahedral mesh
    mesh = IcosahedralMesh(max_level=mesh_level)

    # Create model
    model = GraphCastModel(
        grid_lat=grid_lat,
        grid_lon=grid_lon,
        mesh=mesh,
        n_input_vars=n_vars,
        n_output_vars=n_vars,
        **kwargs
    )

    return model
