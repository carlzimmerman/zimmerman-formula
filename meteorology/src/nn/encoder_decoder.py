"""
Encoder and Decoder for Grid ↔ Mesh Transformations

From First Principles:

The atmospheric state is observed on a latitude-longitude grid (e.g., ERA5 at 0.25°).
Our GNN processor operates on an icosahedral mesh.

We need:
1. Encoder: Grid → Mesh (interpolation + learned embedding)
2. Decoder: Mesh → Grid (interpolation + learned projection)

Physical Interpretation:
- Encoder transforms from "observation space" to "dynamics space"
- Like changing from physical to spectral coordinates in traditional NWP
- Decoder inverts this transformation

The key insight is that the mapping should preserve physical quantities:
- Total mass (integral over sphere should be conserved)
- Smooth fields should remain smooth
- No artificial gradients introduced at mesh boundaries
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional, Dict
import numpy as np

from .message_passing import MLP, MessagePassingLayer, build_edge_index


class BilinearInterpolator:
    """
    Bilinear interpolation from regular lat-lon grid to irregular mesh points.

    From first principles:
    Given a field f on a regular grid and a query point (lat, lon),
    bilinear interpolation finds the 4 surrounding grid points and
    computes a weighted average:

    f(lat, lon) = w_00·f_00 + w_01·f_01 + w_10·f_10 + w_11·f_11

    where weights are proportional to the area of opposite rectangles
    (normalized to sum to 1).

    For spherical geometry, we use local tangent plane approximation,
    which is valid when grid spacing << Earth radius.
    """

    def __init__(
        self,
        grid_lat: np.ndarray,  # (n_lat,) regular grid latitudes
        grid_lon: np.ndarray,  # (n_lon,) regular grid longitudes
        mesh_lat: np.ndarray,  # (n_mesh,) mesh node latitudes
        mesh_lon: np.ndarray,  # (n_mesh,) mesh node longitudes
    ):
        """
        Precompute interpolation indices and weights.
        """
        self.n_lat = len(grid_lat)
        self.n_lon = len(grid_lon)
        self.n_mesh = len(mesh_lat)

        # Grid spacing (assuming regular grid)
        self.dlat = grid_lat[1] - grid_lat[0]
        self.dlon = grid_lon[1] - grid_lon[0]

        # Grid bounds
        self.lat_min = grid_lat[0]
        self.lat_max = grid_lat[-1]
        self.lon_min = grid_lon[0]
        self.lon_max = grid_lon[-1]

        # Precompute indices and weights for each mesh point
        self.indices = np.zeros((self.n_mesh, 4), dtype=np.int64)
        self.weights = np.zeros((self.n_mesh, 4), dtype=np.float32)

        for i in range(self.n_mesh):
            lat, lon = mesh_lat[i], mesh_lon[i]

            # Handle longitude wraparound
            lon = np.mod(lon - self.lon_min, 2 * np.pi) + self.lon_min

            # Find surrounding grid cell
            lat_idx = (lat - self.lat_min) / self.dlat
            lon_idx = (lon - self.lon_min) / self.dlon

            # Integer indices (clamped to valid range)
            i0 = int(np.floor(lat_idx))
            j0 = int(np.floor(lon_idx))

            i0 = np.clip(i0, 0, self.n_lat - 2)
            j0 = np.clip(j0, 0, self.n_lon - 2)

            i1 = i0 + 1
            j1 = (j0 + 1) % self.n_lon  # Wrap longitude

            # Fractional position within cell [0, 1]
            lat_frac = lat_idx - i0
            lon_frac = lon_idx - j0

            lat_frac = np.clip(lat_frac, 0, 1)
            lon_frac = np.clip(lon_frac, 0, 1)

            # Bilinear weights (opposite area rule)
            w00 = (1 - lat_frac) * (1 - lon_frac)
            w01 = (1 - lat_frac) * lon_frac
            w10 = lat_frac * (1 - lon_frac)
            w11 = lat_frac * lon_frac

            # Store linear indices into flattened grid
            self.indices[i, 0] = i0 * self.n_lon + j0
            self.indices[i, 1] = i0 * self.n_lon + j1
            self.indices[i, 2] = i1 * self.n_lon + j0
            self.indices[i, 3] = i1 * self.n_lon + j1

            self.weights[i, :] = [w00, w01, w10, w11]

        # Convert to torch tensors (will be moved to device when used)
        self.indices = torch.tensor(self.indices, dtype=torch.long)
        self.weights = torch.tensor(self.weights, dtype=torch.float32)

    def interpolate(self, grid_data: torch.Tensor) -> torch.Tensor:
        """
        Interpolate from grid to mesh points.

        Args:
            grid_data: (batch, n_lat, n_lon, channels) or (n_lat, n_lon, channels)

        Returns:
            mesh_data: (batch, n_mesh, channels) or (n_mesh, channels)
        """
        # Handle batch dimension
        has_batch = grid_data.dim() == 4
        if not has_batch:
            grid_data = grid_data.unsqueeze(0)

        batch_size = grid_data.shape[0]
        n_channels = grid_data.shape[-1]

        # Flatten spatial dimensions
        grid_flat = grid_data.reshape(batch_size, -1, n_channels)  # (B, H*W, C)

        # Move indices/weights to same device
        indices = self.indices.to(grid_data.device)
        weights = self.weights.to(grid_data.device)

        # Gather values at the 4 corners for each mesh point
        # indices: (n_mesh, 4)
        # We need: (batch, n_mesh, 4, channels)

        # Gather: for each mesh point, get the 4 corner values
        corner_values = grid_flat[:, indices, :]  # (B, n_mesh, 4, C)

        # Apply weights: (n_mesh, 4) -> (1, n_mesh, 4, 1) for broadcasting
        weights = weights.unsqueeze(0).unsqueeze(-1)

        # Weighted sum
        mesh_data = (corner_values * weights).sum(dim=2)  # (B, n_mesh, C)

        if not has_batch:
            mesh_data = mesh_data.squeeze(0)

        return mesh_data


class GridToMeshEncoder(nn.Module):
    """
    Encode lat-lon grid data to mesh node features.

    Architecture:
    1. Interpolate grid data to mesh positions
    2. Concatenate with mesh node features (lat, lon, Coriolis, etc.)
    3. Apply learned embedding MLP

    From first principles:
    The encoder must:
    - Preserve physical information (no loss of data)
    - Add geometric context (where on Earth is this node?)
    - Transform to a representation suitable for message passing
    """

    def __init__(
        self,
        grid_lat: np.ndarray,
        grid_lon: np.ndarray,
        mesh_lat: np.ndarray,
        mesh_lon: np.ndarray,
        n_input_channels: int,
        n_mesh_features: int,  # lat, lon, sin_lat, cos_lat, sin_lon, cos_lon, coriolis
        hidden_dim: int = 256,
        output_dim: int = 256,
    ):
        super().__init__()

        # Precompute interpolation
        self.interpolator = BilinearInterpolator(
            grid_lat, grid_lon, mesh_lat, mesh_lon
        )

        # Input: interpolated channels + mesh node features
        total_input_dim = n_input_channels + n_mesh_features

        # Embedding MLP
        self.embed = MLP(
            input_dim=total_input_dim,
            hidden_dim=hidden_dim,
            output_dim=output_dim,
            n_layers=2,
        )

    def forward(
        self,
        grid_data: torch.Tensor,  # (batch, n_lat, n_lon, channels)
        mesh_features: torch.Tensor,  # (n_mesh, n_mesh_features)
    ) -> torch.Tensor:
        """
        Encode grid data to mesh representation.

        Returns:
            node_features: (batch, n_mesh, output_dim)
        """
        # Interpolate to mesh
        mesh_data = self.interpolator.interpolate(grid_data)  # (B, n_mesh, channels)

        # Add batch dimension to mesh features if needed
        batch_size = mesh_data.shape[0]
        mesh_features = mesh_features.unsqueeze(0).expand(batch_size, -1, -1)

        # Concatenate interpolated data with mesh features
        combined = torch.cat([mesh_data, mesh_features], dim=-1)

        # Apply embedding
        node_features = self.embed(combined)

        return node_features


class MeshToGridDecoder(nn.Module):
    """
    Decode mesh node features back to lat-lon grid predictions.

    Architecture:
    1. Apply learned projection MLP to get output channels
    2. Scatter mesh values to nearby grid points
    3. Weighted average based on distance

    From first principles:
    The decoder must:
    - Reconstruct full grid from mesh representation
    - Preserve smoothness (no artifacts at mesh boundaries)
    - Output physically meaningful quantities
    """

    def __init__(
        self,
        grid_lat: np.ndarray,
        grid_lon: np.ndarray,
        mesh_lat: np.ndarray,
        mesh_lon: np.ndarray,
        input_dim: int = 256,
        hidden_dim: int = 256,
        n_output_channels: int = 78,  # Typical ERA5 variable count
        n_neighbors: int = 4,
    ):
        super().__init__()

        self.n_lat = len(grid_lat)
        self.n_lon = len(grid_lon)
        self.n_mesh = len(mesh_lat)
        self.n_output_channels = n_output_channels

        # Projection MLP
        self.project = MLP(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            output_dim=n_output_channels,
            n_layers=2,
        )

        # Precompute inverse mapping: for each grid point, find nearest mesh nodes
        self._precompute_inverse_mapping(
            grid_lat, grid_lon, mesh_lat, mesh_lon, n_neighbors
        )

    def _precompute_inverse_mapping(
        self,
        grid_lat: np.ndarray,
        grid_lon: np.ndarray,
        mesh_lat: np.ndarray,
        mesh_lon: np.ndarray,
        n_neighbors: int,
    ):
        """
        For each grid point, find the nearest mesh nodes and their weights.
        """
        n_grid = self.n_lat * self.n_lon

        # Create grid of all lat-lon points
        lat_grid, lon_grid = np.meshgrid(grid_lat, grid_lon, indexing='ij')
        lat_grid = lat_grid.flatten()
        lon_grid = lon_grid.flatten()

        # For each grid point, find k nearest mesh nodes
        self.neighbor_indices = np.zeros((n_grid, n_neighbors), dtype=np.int64)
        self.neighbor_weights = np.zeros((n_grid, n_neighbors), dtype=np.float32)

        for i in range(n_grid):
            g_lat, g_lon = lat_grid[i], lon_grid[i]

            # Compute angular distances to all mesh nodes
            # Using simple Euclidean approximation in lat-lon space
            # (accurate enough for nearby points)
            dlat = mesh_lat - g_lat
            dlon = mesh_lon - g_lon
            # Handle longitude wraparound
            dlon = np.where(dlon > np.pi, dlon - 2*np.pi, dlon)
            dlon = np.where(dlon < -np.pi, dlon + 2*np.pi, dlon)
            dlon *= np.cos(g_lat)  # Scale by cos(lat) for spherical geometry

            distances = np.sqrt(dlat**2 + dlon**2)

            # Find k nearest
            nearest_idx = np.argsort(distances)[:n_neighbors]
            nearest_dist = distances[nearest_idx]

            # Inverse distance weighting
            # Avoid division by zero
            nearest_dist = np.maximum(nearest_dist, 1e-6)
            weights = 1.0 / nearest_dist
            weights /= weights.sum()

            self.neighbor_indices[i] = nearest_idx
            self.neighbor_weights[i] = weights

        # Convert to torch
        self.neighbor_indices = torch.tensor(self.neighbor_indices, dtype=torch.long)
        self.neighbor_weights = torch.tensor(self.neighbor_weights, dtype=torch.float32)

    def forward(self, node_features: torch.Tensor) -> torch.Tensor:
        """
        Decode mesh features to grid predictions.

        Args:
            node_features: (batch, n_mesh, input_dim)

        Returns:
            grid_output: (batch, n_lat, n_lon, n_output_channels)
        """
        # Project to output channels
        mesh_output = self.project(node_features)  # (B, n_mesh, n_channels)

        batch_size = mesh_output.shape[0]

        # Move to same device
        indices = self.neighbor_indices.to(mesh_output.device)
        weights = self.neighbor_weights.to(mesh_output.device)

        # Gather neighbor values: (B, n_grid, n_neighbors, n_channels)
        neighbor_values = mesh_output[:, indices, :]

        # Apply weights: (n_grid, n_neighbors) -> (1, n_grid, n_neighbors, 1)
        weights = weights.unsqueeze(0).unsqueeze(-1)

        # Weighted sum
        grid_output = (neighbor_values * weights).sum(dim=2)  # (B, n_grid, C)

        # Reshape to spatial grid
        grid_output = grid_output.reshape(
            batch_size, self.n_lat, self.n_lon, self.n_output_channels
        )

        return grid_output


class Grid2MeshGNN(nn.Module):
    """
    GNN that maps grid data to mesh using message passing.

    Alternative to pure interpolation - uses learned bipartite edges
    from grid nodes to mesh nodes.

    From first principles:
    This is like the "source term" in a PDE - the grid data injects
    information into the mesh representation through localized interactions.
    """

    def __init__(
        self,
        grid_dim: int,
        mesh_dim: int,
        edge_dim: int,
        hidden_dim: int = 256,
    ):
        super().__init__()

        self.message_layer = MessagePassingLayer(
            node_dim=mesh_dim,
            edge_dim=edge_dim,
            hidden_dim=hidden_dim,
        )

        # Embed grid features to mesh space
        self.grid_embed = MLP(
            input_dim=grid_dim,
            hidden_dim=hidden_dim,
            output_dim=mesh_dim,
            n_layers=2,
        )

    def forward(
        self,
        grid_features: torch.Tensor,
        mesh_features: torch.Tensor,
        g2m_edge_index: torch.Tensor,
        g2m_edge_features: torch.Tensor,
    ) -> torch.Tensor:
        """
        Transfer information from grid to mesh via GNN.
        """
        # Embed grid features
        grid_embedded = self.grid_embed(grid_features)

        # Concatenate grid and mesh nodes
        all_nodes = torch.cat([grid_embedded, mesh_features], dim=0)

        # Message pass (grid nodes send to mesh nodes)
        updated_nodes, _ = self.message_layer(
            all_nodes,
            g2m_edge_features,
            g2m_edge_index,
        )

        # Return only mesh nodes
        n_grid = grid_features.shape[0]
        mesh_output = updated_nodes[n_grid:]

        return mesh_output
