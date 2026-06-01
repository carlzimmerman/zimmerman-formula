"""
Message Passing Neural Networks from First Principles

The fundamental insight: PDEs on graphs have the same structure as GNNs.

Consider a discretized diffusion equation:
    ∂u/∂t = α∇²u

Discretized on a graph:
    u_i^{n+1} = u_i^n + Δt·α·Σⱼ (u_j^n - u_i^n)/d_ij²

This IS message passing:
    - Message from j to i: m_ij = (u_j - u_i)/d_ij²
    - Aggregation: Σⱼ m_ij
    - Update: u_i + Δt·α·(aggregated messages)

The Navier-Stokes equations have the same structure when discretized.
By learning the message and update functions, we implicitly learn the PDE.

GraphCast Architecture:
    - Node features: atmospheric state variables at each mesh point
    - Edge features: spatial relationship (distance, direction)
    - Message: learned function of sender state, receiver state, edge features
    - Aggregation: sum (analogous to integral over neighbors)
    - Update: residual connection + learned transformation
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional, Dict
import numpy as np


class MLP(nn.Module):
    """
    Multi-Layer Perceptron - the building block for learned transformations.

    From first principles:
    Any smooth function can be approximated by a sufficiently wide/deep MLP
    (universal approximation theorem). We use MLPs to learn:
    - Message functions (how neighbors interact)
    - Update functions (how nodes evolve)
    """

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        n_layers: int = 2,
        activation: str = 'swish',
        layer_norm: bool = True,
    ):
        super().__init__()

        self.layers = nn.ModuleList()
        self.norms = nn.ModuleList() if layer_norm else None

        # Activation function
        if activation == 'swish':
            self.activation = nn.SiLU()  # Swish/SiLU: x * sigmoid(x)
        elif activation == 'relu':
            self.activation = nn.ReLU()
        elif activation == 'gelu':
            self.activation = nn.GELU()
        else:
            raise ValueError(f"Unknown activation: {activation}")

        # Build layers
        dims = [input_dim] + [hidden_dim] * (n_layers - 1) + [output_dim]
        for i in range(n_layers):
            self.layers.append(nn.Linear(dims[i], dims[i + 1]))
            if layer_norm and i < n_layers - 1:
                self.norms.append(nn.LayerNorm(dims[i + 1]))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for i, layer in enumerate(self.layers):
            x = layer(x)
            if i < len(self.layers) - 1:  # No activation on final layer
                if self.norms is not None:
                    x = self.norms[i](x)
                x = self.activation(x)
        return x


class MessagePassingLayer(nn.Module):
    """
    A single message passing layer implementing the GNN update equation.

    From first principles, the update equations are:

    1. Edge update (message computation):
       e'_ij = φ_e(e_ij, h_i, h_j)

    2. Node aggregation:
       m_i = Σⱼ e'_ij  (sum over neighbors j)

    3. Node update:
       h'_i = φ_v(h_i, m_i)

    The key insight is that φ_e and φ_v are learned functions,
    allowing the network to discover the correct physics implicitly.

    Residual connections help with gradient flow in deep networks.
    """

    def __init__(
        self,
        node_dim: int,
        edge_dim: int,
        hidden_dim: int = 256,
        n_mlp_layers: int = 2,
        residual: bool = True,
    ):
        super().__init__()

        self.node_dim = node_dim
        self.edge_dim = edge_dim
        self.residual = residual

        # Edge update MLP: takes (sender_features, receiver_features, edge_features)
        # Input: node_dim (sender) + node_dim (receiver) + edge_dim
        self.edge_mlp = MLP(
            input_dim=2 * node_dim + edge_dim,
            hidden_dim=hidden_dim,
            output_dim=edge_dim,
            n_layers=n_mlp_layers,
        )

        # Node update MLP: takes (node_features, aggregated_messages)
        # Input: node_dim + edge_dim (aggregated)
        self.node_mlp = MLP(
            input_dim=node_dim + edge_dim,
            hidden_dim=hidden_dim,
            output_dim=node_dim,
            n_layers=n_mlp_layers,
        )

    def forward(
        self,
        node_features: torch.Tensor,      # (N, node_dim)
        edge_features: torch.Tensor,      # (E, edge_dim)
        edge_index: torch.Tensor,         # (2, E) - [senders, receivers]
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Perform one round of message passing.

        Args:
            node_features: Node states, shape (N, node_dim)
            edge_features: Edge attributes, shape (E, edge_dim)
            edge_index: Edge connectivity, shape (2, E)
                        edge_index[0] = sender indices
                        edge_index[1] = receiver indices

        Returns:
            Updated (node_features, edge_features)
        """
        senders = edge_index[0]
        receivers = edge_index[1]

        # === STEP 1: Edge Update ===
        # Gather node features for senders and receivers
        sender_features = node_features[senders]    # (E, node_dim)
        receiver_features = node_features[receivers]  # (E, node_dim)

        # Concatenate inputs for edge MLP
        edge_input = torch.cat([
            sender_features,
            receiver_features,
            edge_features,
        ], dim=-1)  # (E, 2*node_dim + edge_dim)

        # Compute edge updates
        edge_updates = self.edge_mlp(edge_input)  # (E, edge_dim)

        # Residual connection for edges
        if self.residual:
            edge_features = edge_features + edge_updates
        else:
            edge_features = edge_updates

        # === STEP 2: Aggregate Messages to Nodes ===
        # Sum messages from all incoming edges to each receiver node
        n_nodes = node_features.shape[0]
        aggregated = torch.zeros(
            n_nodes, self.edge_dim,
            device=node_features.device,
            dtype=node_features.dtype,
        )

        # Scatter-add: accumulate edge features to receiver nodes
        aggregated.scatter_add_(
            dim=0,
            index=receivers.unsqueeze(-1).expand(-1, self.edge_dim),
            src=edge_features,
        )

        # === STEP 3: Node Update ===
        # Concatenate node features with aggregated messages
        node_input = torch.cat([node_features, aggregated], dim=-1)

        # Compute node updates
        node_updates = self.node_mlp(node_input)  # (N, node_dim)

        # Residual connection for nodes
        if self.residual:
            node_features = node_features + node_updates
        else:
            node_features = node_updates

        return node_features, edge_features


class GraphNetwork(nn.Module):
    """
    Stack of message passing layers forming the full processor.

    From first principles:
    - Each layer allows information to propagate one hop along edges
    - With L layers and multi-scale edges, information can travel globally
    - Residual connections allow both shallow and deep paths

    GraphCast uses 16 processor layers, which with the multi-mesh structure
    allows planetary-scale information propagation.

    Physical interpretation:
    - Early layers: local interactions (pressure gradients, temperature advection)
    - Later layers: large-scale patterns (Rossby waves, teleconnections)
    """

    def __init__(
        self,
        node_dim: int,
        edge_dim: int,
        hidden_dim: int = 256,
        n_layers: int = 16,
        n_mlp_layers: int = 2,
    ):
        super().__init__()

        self.n_layers = n_layers

        self.layers = nn.ModuleList([
            MessagePassingLayer(
                node_dim=node_dim,
                edge_dim=edge_dim,
                hidden_dim=hidden_dim,
                n_mlp_layers=n_mlp_layers,
                residual=True,
            )
            for _ in range(n_layers)
        ])

        # Final layer norm for stability
        self.final_node_norm = nn.LayerNorm(node_dim)
        self.final_edge_norm = nn.LayerNorm(edge_dim)

    def forward(
        self,
        node_features: torch.Tensor,
        edge_features: torch.Tensor,
        edge_index: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Process features through all message passing layers.
        """
        for layer in self.layers:
            node_features, edge_features = layer(
                node_features, edge_features, edge_index
            )

        node_features = self.final_node_norm(node_features)
        edge_features = self.final_edge_norm(edge_features)

        return node_features, edge_features


def build_edge_index(edges: np.ndarray, bidirectional: bool = True) -> torch.Tensor:
    """
    Convert edge list to PyTorch edge_index format.

    Args:
        edges: (E, 2) array of [v1, v2] pairs
        bidirectional: If True, add reverse edges (v2 -> v1)

    Returns:
        edge_index: (2, E*) tensor where E* = E if not bidirectional else 2E
    """
    edges = torch.tensor(edges, dtype=torch.long)

    if bidirectional:
        # Add reverse edges
        reverse_edges = torch.stack([edges[:, 1], edges[:, 0]], dim=1)
        edges = torch.cat([edges, reverse_edges], dim=0)

    # Transpose to (2, E) format: [senders; receivers]
    edge_index = edges.T.contiguous()

    return edge_index
