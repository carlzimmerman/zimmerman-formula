"""
Conservation Laws as Physics-Informed Constraints

From First Principles:

The atmosphere obeys fundamental conservation laws that cannot be violated:

1. MASS CONSERVATION (Continuity Equation):
   ∂ρ/∂t + ∇·(ρv) = 0

   In pressure coordinates:
   ∂u/∂x + ∂v/∂y + ∂ω/∂p = 0

   Global integral: Total atmospheric mass is constant (~5.15×10¹⁸ kg)

2. ENERGY CONSERVATION:
   Total energy = Internal + Kinetic + Potential
   E = c_v·T + ½(u² + v²) + gz

   Global integral: Changes only through radiative forcing

3. MOMENTUM CONSERVATION (Navier-Stokes):
   ∂v/∂t + (v·∇)v = -∇p/ρ - 2Ω×v - g∇z + friction

4. ANGULAR MOMENTUM:
   L = (u + Ω·R·cos(φ))·R·cos(φ)
   Conserved for inviscid, axisymmetric flow

These constraints are implemented as soft penalties in the loss function:
   L_total = L_data + λ_mass·L_mass + λ_energy·L_energy + ...

This makes the model "physics-informed" - it learns from data while
respecting physical laws.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional, Dict
import numpy as np


# Physical constants
EARTH_RADIUS_M = 6.371e6      # Earth radius [m]
GRAVITY = 9.80665             # Standard gravity [m/s²]
C_P = 1004.0                  # Specific heat at constant pressure [J/(kg·K)]
C_V = 717.0                   # Specific heat at constant volume [J/(kg·K)]
R_DRY = 287.0                 # Gas constant for dry air [J/(kg·K)]
R_VAPOR = 461.0               # Gas constant for water vapor [J/(kg·K)]
L_V = 2.5e6                   # Latent heat of vaporization [J/kg]


def spherical_divergence_2d(
    u: torch.Tensor,          # Eastward wind (batch, lat, lon)
    v: torch.Tensor,          # Northward wind (batch, lat, lon)
    lat: torch.Tensor,        # Latitudes in radians (n_lat,)
    dlon: float,              # Longitude spacing in radians
    dlat: float,              # Latitude spacing in radians
    radius: float = EARTH_RADIUS_M,
) -> torch.Tensor:
    """
    Compute horizontal divergence on a sphere.

    From first principles:
    ∇·v = (1/(R·cos(φ))) · [∂u/∂λ + ∂(v·cos(φ))/∂φ]

    Using finite differences:
    - ∂u/∂λ ≈ (u[i,j+1] - u[i,j-1]) / (2·dλ)
    - ∂(v·cos(φ))/∂φ ≈ (v·cos(φ)[i+1,j] - v·cos(φ)[i-1,j]) / (2·dφ)

    Args:
        u: Eastward wind component
        v: Northward wind component
        lat: Latitude array
        dlon: Longitude grid spacing
        dlat: Latitude grid spacing
        radius: Earth radius

    Returns:
        Divergence field [s⁻¹]
    """
    # Latitude factors
    cos_lat = torch.cos(lat).view(1, -1, 1)  # (1, n_lat, 1)
    cos_lat_safe = torch.clamp(cos_lat, min=1e-6)  # Avoid pole singularity

    # ∂u/∂λ using central differences (periodic in longitude)
    du_dlambda = (torch.roll(u, -1, dims=-1) - torch.roll(u, 1, dims=-1)) / (2 * dlon)

    # ∂(v·cos(φ))/∂φ using central differences
    v_cos_lat = v * cos_lat
    # Pad for boundary conditions (constant extrapolation at poles)
    v_cos_padded = F.pad(v_cos_lat, (0, 0, 1, 1), mode='replicate')
    d_vcoslat_dphi = (v_cos_padded[:, 2:, :] - v_cos_padded[:, :-2, :]) / (2 * dlat)

    # Divergence formula
    div = (du_dlambda + d_vcoslat_dphi) / (radius * cos_lat_safe)

    return div


def mass_conservation_loss(
    rho_pred: torch.Tensor,    # Predicted density at t+Δt
    rho_curr: torch.Tensor,    # Current density at t
    u: torch.Tensor,           # Eastward wind
    v: torch.Tensor,           # Northward wind
    w: torch.Tensor,           # Vertical wind
    lat: torch.Tensor,
    dlon: float,
    dlat: float,
    dt: float,
    pressure_levels: torch.Tensor,
) -> torch.Tensor:
    """
    Compute penalty for violating mass conservation.

    From first principles:
    ∂ρ/∂t + ∇·(ρv) = 0

    Discretized:
    (ρ^{n+1} - ρ^n)/Δt + ∇·(ρv)^n ≈ 0

    So the residual should be small:
    residual = ρ^{n+1} - ρ^n + Δt·∇·(ρv)^n

    We penalize the L² norm of this residual.
    """
    # Compute horizontal divergence of mass flux
    rho_u = rho_curr * u
    rho_v = rho_curr * v

    div_rho_u = spherical_divergence_2d(rho_u, rho_v, lat, dlon, dlat)

    # For now, ignore vertical divergence (need 3D implementation)
    # In practice, would add ∂(ρw)/∂z term

    # Time derivative
    drho_dt = (rho_pred - rho_curr) / dt

    # Continuity residual
    residual = drho_dt + div_rho_u

    # Return mean squared residual
    return (residual ** 2).mean()


def divergence_penalty(
    u: torch.Tensor,
    v: torch.Tensor,
    lat: torch.Tensor,
    dlon: float,
    dlat: float,
    target_div: float = 0.0,
) -> torch.Tensor:
    """
    Penalize divergence deviating from target (usually 0 for incompressible).

    From first principles:
    For large-scale atmospheric flow, the horizontal divergence is small
    because vertical motions adjust to maintain hydrostatic balance.

    Typical values: |∇·v| ~ 10⁻⁵ s⁻¹

    This penalty encourages the model to produce physically realistic
    wind fields that don't have unrealistic convergence/divergence.

    Args:
        u: Eastward wind (batch, lat, lon) or (batch, lat, lon, levels)
        v: Northward wind, same shape
        lat: Latitudes in radians
        dlon, dlat: Grid spacing
        target_div: Target divergence (0 for incompressible)

    Returns:
        Scalar penalty
    """
    # Handle 4D (multi-level) case
    if u.dim() == 4:
        n_levels = u.shape[-1]
        total_penalty = 0.0
        for k in range(n_levels):
            div = spherical_divergence_2d(u[..., k], v[..., k], lat, dlon, dlat)
            total_penalty = total_penalty + ((div - target_div) ** 2).mean()
        return total_penalty / n_levels
    else:
        div = spherical_divergence_2d(u, v, lat, dlon, dlat)
        return ((div - target_div) ** 2).mean()


def energy_conservation_loss(
    state_pred: Dict[str, torch.Tensor],
    state_curr: Dict[str, torch.Tensor],
    lat: torch.Tensor,
    dlon: float,
    dlat: float,
    pressure_levels: torch.Tensor,
    dt: float,
    radiation_forcing: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    """
    Penalize violation of energy conservation.

    From first principles:
    Total energy E = c_p·T + ½(u² + v²) + gz

    d/dt ∫∫∫ E dV = Q_radiation (external forcing only)

    For closed system (no radiation), total energy should be constant.

    Args:
        state_pred: Predicted state with 'T', 'u', 'v', 'z' (or 'geopotential')
        state_curr: Current state
        lat: Latitudes
        pressure_levels: Pressure levels for vertical integration
        dt: Time step
        radiation_forcing: Optional external heating rate

    Returns:
        Energy conservation penalty
    """
    # Extract fields
    T_pred = state_pred['T']
    T_curr = state_curr['T']
    u_pred = state_pred['u']
    u_curr = state_curr['u']
    v_pred = state_pred['v']
    v_curr = state_curr['v']

    # Compute internal energy (c_p * T for dry air)
    E_internal_pred = C_P * T_pred
    E_internal_curr = C_P * T_curr

    # Compute kinetic energy (½(u² + v²))
    E_kinetic_pred = 0.5 * (u_pred**2 + v_pred**2)
    E_kinetic_curr = 0.5 * (u_curr**2 + v_curr**2)

    # Total energy per unit mass (ignoring potential for now)
    E_pred = E_internal_pred + E_kinetic_pred
    E_curr = E_internal_curr + E_kinetic_curr

    # Area weights (cos(lat))
    cos_lat = torch.cos(lat).view(1, -1, 1, 1)

    # Global mean energy
    global_E_pred = (E_pred * cos_lat).sum() / cos_lat.sum() / E_pred.shape[-1]
    global_E_curr = (E_curr * cos_lat).sum() / cos_lat.sum() / E_curr.shape[-1]

    # Energy change rate
    dE_dt = (global_E_pred - global_E_curr) / dt

    # Expected change (from radiation, if provided)
    if radiation_forcing is not None:
        expected_dE = (radiation_forcing * cos_lat).sum() / cos_lat.sum()
    else:
        expected_dE = 0.0

    # Penalty: deviation from expected change
    residual = dE_dt - expected_dE

    return residual ** 2


def physical_bounds_loss(
    state: Dict[str, torch.Tensor],
    bounds: Optional[Dict[str, Tuple[float, float]]] = None,
) -> torch.Tensor:
    """
    Penalize predictions that violate physical bounds.

    From first principles, atmospheric variables have physical constraints:
    - Temperature: T > 0 K (absolute zero), typically 180-330 K
    - Specific humidity: q ≥ 0 (non-negative water)
    - Pressure: p > 0 (positive definite)
    - Relative humidity: 0 ≤ RH ≤ 1 (can allow slight supersaturation)

    We use a soft penalty that grows as values exceed bounds:
    penalty = max(0, lower - x)² + max(0, x - upper)²

    Args:
        state: Dictionary of state variables
        bounds: Dictionary mapping variable names to (lower, upper) bounds
                Default bounds are used if not specified

    Returns:
        Total bounds violation penalty
    """
    if bounds is None:
        bounds = {
            'T': (150.0, 350.0),         # Temperature [K]
            'q': (0.0, 0.05),             # Specific humidity [kg/kg]
            'u': (-150.0, 150.0),         # Zonal wind [m/s]
            'v': (-100.0, 100.0),         # Meridional wind [m/s]
            'sp': (40000.0, 110000.0),    # Surface pressure [Pa]
        }

    total_penalty = torch.tensor(0.0, device=list(state.values())[0].device)

    for var_name, (lower, upper) in bounds.items():
        if var_name in state:
            var = state[var_name]

            # Lower bound violation
            lower_violation = F.relu(lower - var)

            # Upper bound violation
            upper_violation = F.relu(var - upper)

            # Squared penalty
            penalty = (lower_violation ** 2 + upper_violation ** 2).mean()
            total_penalty = total_penalty + penalty

    return total_penalty


def humidity_saturation_penalty(
    T: torch.Tensor,           # Temperature [K]
    q: torch.Tensor,           # Specific humidity [kg/kg]
    p: torch.Tensor,           # Pressure [Pa]
    max_supersaturation: float = 0.01,  # Allow 1% supersaturation
) -> torch.Tensor:
    """
    Penalize predictions with excessive supersaturation.

    From first principles:
    Specific humidity cannot exceed saturation:
    q ≤ q_sat(T, p) = ε · e_s(T) / (p - (1-ε)·e_s(T))

    where:
    - e_s(T) is saturation vapor pressure (Clausius-Clapeyron)
    - ε = R_dry/R_vapor ≈ 0.622

    In reality, slight supersaturation (1-2%) can occur before
    cloud formation, so we allow a small margin.

    Args:
        T: Temperature field
        q: Specific humidity field
        p: Pressure field
        max_supersaturation: Allowed excess over saturation

    Returns:
        Supersaturation penalty
    """
    # Saturation vapor pressure (Tetens formula)
    # e_s = 610.94 * exp(17.625 * (T-273.15) / (T-273.15+243.04))
    T_celsius = T - 273.15
    e_s = 610.94 * torch.exp(17.625 * T_celsius / (T_celsius + 243.04))

    # Ratio of gas constants
    epsilon = R_DRY / R_VAPOR  # ≈ 0.622

    # Saturation specific humidity
    q_sat = epsilon * e_s / (p - (1 - epsilon) * e_s)

    # Maximum allowed humidity
    q_max = q_sat * (1 + max_supersaturation)

    # Penalty for exceeding saturation
    excess = F.relu(q - q_max)

    return (excess ** 2).mean()


class PhysicsInformedLoss(nn.Module):
    """
    Combined physics-informed loss function.

    This module computes the total loss as:
    L = L_data + Σᵢ λᵢ · L_physics,i

    where L_physics,i are the various physical constraint penalties.
    """

    def __init__(
        self,
        grid_lat: torch.Tensor,
        dlon: float,
        dlat: float,
        lambda_divergence: float = 0.1,
        lambda_bounds: float = 1.0,
        lambda_energy: float = 0.01,
    ):
        super().__init__()

        self.register_buffer('lat', grid_lat)
        self.dlon = dlon
        self.dlat = dlat

        self.lambda_div = lambda_divergence
        self.lambda_bounds = lambda_bounds
        self.lambda_energy = lambda_energy

    def forward(
        self,
        pred: Dict[str, torch.Tensor],
        target: Dict[str, torch.Tensor],
        current: Optional[Dict[str, torch.Tensor]] = None,
        dt: float = 6 * 3600,  # 6 hours
        return_components: bool = False,
    ) -> torch.Tensor:
        """
        Compute total physics-informed loss.

        Args:
            pred: Predicted state dictionary
            target: Target state dictionary
            current: Current state (for conservation checks)
            dt: Time step in seconds
            return_components: If True, return dict of loss components

        Returns:
            Total loss (or dict of components)
        """
        losses = {}

        # Data loss (MSE, latitude-weighted)
        cos_lat = torch.cos(self.lat).view(1, -1, 1, 1)

        data_loss = 0.0
        for var in pred:
            if var in target:
                se = (pred[var] - target[var]) ** 2
                weighted_se = se * cos_lat
                data_loss = data_loss + weighted_se.mean()
        data_loss = data_loss / len(pred)
        losses['data'] = data_loss

        # Divergence penalty
        if 'u' in pred and 'v' in pred:
            div_loss = divergence_penalty(
                pred['u'], pred['v'], self.lat, self.dlon, self.dlat
            )
            losses['divergence'] = self.lambda_div * div_loss

        # Physical bounds
        bounds_loss = physical_bounds_loss(pred)
        losses['bounds'] = self.lambda_bounds * bounds_loss

        # Energy conservation (if current state provided)
        if current is not None and 'T' in pred and 'u' in pred and 'v' in pred:
            energy_loss = energy_conservation_loss(
                pred, current, self.lat, self.dlon, self.dlat,
                pressure_levels=torch.tensor([1000, 850, 500, 250]),
                dt=dt,
            )
            losses['energy'] = self.lambda_energy * energy_loss

        # Total loss
        total = sum(losses.values())

        if return_components:
            losses['total'] = total
            return losses
        else:
            return total
