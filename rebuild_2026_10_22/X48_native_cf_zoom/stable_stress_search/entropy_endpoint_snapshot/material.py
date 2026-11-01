"""Local density-gated memory stress, independent of X48 production dynamics.

Use one consistent system of physical units. ``K`` is dimensional, nonnegative,
and is advected when ``bulk_viscosity_source`` returns zero. The specific energy
is e=K*W(rho); its pressure is rho**2 * partial(e)/partial(rho) at fixed K.
The low-density phase retains latent energy while exerting exactly zero stress.

An entropy coordinate sigma>=0 may be chosen through K=Kstar*sigma**3. This
parameterization makes e convex in (sigma, specific volume). Positive acoustic
stiffness does not by itself establish convective or global halo stability.
No density threshold, gravitational background, or parameter evolves implicitly.
"""

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class MaterialParameters:
    """Positive scalar material scales; ``G`` and ``a0`` set P0 only.

    ``rho_q`` is the fixed physical density below which stress vanishes.
    ``tau`` sets the compression-rate threshold 1/tau. The dense polytropic
    coefficient is normalized by Kstar=P0/rho_q**2, not by latent W's offset.
    """

    rho_q: float
    a0: float
    G: float
    tau: float

    def __post_init__(self):
        for name in ("rho_q", "a0", "G", "tau"):
            value = np.asarray(getattr(self, name), dtype=float)
            if value.ndim != 0 or not np.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be a finite positive scalar")
            object.__setattr__(self, name, float(value))

    @property
    def p0(self) -> float:
        """Stress normalization a0**2/(8*pi*G)."""
        return self.a0**2 / (8 * np.pi * self.G)

    @property
    def k_star(self) -> float:
        """Dimensional coefficient normalization P0/rho_q**2."""
        return self.p0 / self.rho_q**2


def _finite_array(value, name, *, positive=False, nonnegative=False):
    result = np.asarray(value, dtype=float)
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be finite")
    if positive and np.any(result <= 0):
        raise ValueError(f"{name} must be positive")
    if nonnegative and np.any(result < 0):
        raise ValueError(f"{name} must be nonnegative")
    return result


def _state(rho, K):
    return np.broadcast_arrays(
        _finite_array(rho, "rho", positive=True),
        _finite_array(K, "K", nonnegative=True),
    )


def activation(d):
    """h(d): zero for 0<d<=1, cubic ramp to one at d=2; array-compatible."""
    d = _finite_array(d, "density ratio", positive=True)
    t = np.clip(d - 1, 0, 1)
    return t**2 * (3 - 2 * t)


def activation_derivative(d):
    """dh/dd, including the zero derivatives at both ramp endpoints."""
    d = _finite_array(d, "density ratio", positive=True)
    t = np.clip(d - 1, 0, 1)
    return 6 * t * (1 - t)


def density_weight(rho, params: MaterialParameters):
    """W(rho), in density units: 1.5*rho_q below the gate and rho above it."""
    rho = _finite_array(rho, "rho", positive=True)
    d = rho / params.rho_q
    t = np.clip(d - 1, 0, 1)
    return np.where(d >= 2, rho, params.rho_q * (1.5 + t**3 - 0.5 * t**4))


def specific_energy(rho, K, params: MaterialParameters):
    """Specific internal energy e=K*W; rho and K follow NumPy broadcasting."""
    rho, K = _state(rho, K)
    return K * density_weight(rho, params)


def pressure(rho, K, params: MaterialParameters):
    """Thermodynamic pressure P=K*rho**2*h, exactly zero below rho_q."""
    rho, K = _state(rho, K)
    return K * (rho * activation(rho / params.rho_q)) * rho


def sound_speed_squared(rho, K, params: MaterialParameters):
    """Adiabatic derivative dP/drho at fixed K, including gate stiffness."""
    rho, K = _state(rho, K)
    d = rho / params.rho_q
    h = activation(d)
    dh_drho = activation_derivative(d) / params.rho_q
    return K * (2 * (rho * h) + rho * (rho * dh_drho))


def dimensionless_enthalpy(d):
    """H(d)=d*h+W/rho_q-1.5, with H=0 throughout the dormant phase.

    For constant K, physical enthalpy relative to the zero-pressure boundary
    is K*rho_q*H. In the dense branch H=2*d-1.5. This is not a function of K
    and does not invert the degenerate dormant density interval.
    """
    d = _finite_array(d, "density ratio", positive=True)
    t = np.clip(d - 1, 0, 1)
    ramp = 3 * t**2 + 2 * t**3 - 2.5 * t**4
    return np.where(d >= 2, 2 * d - 1.5, ramp)


def bulk_viscosity_source(rho, theta, params: MaterialParameters) -> Tuple[np.ndarray, np.ndarray]:
    """Return (bulk pressure q, material derivative D_t K), broadcast together.

    theta is the physical velocity divergence, C=max(-theta,0). Compression
    heats only when rho>rho_q and C>1/tau. Both outputs are nonnegative and
    satisfy q*C=rho*W*D_tK. Using this same q in the momentum equation ensures
    rho*D_t e=-(P+q)*theta: heat is extracted from mechanical work, not added
    separately. The function evaluates a source; it performs no time step.
    """
    rho, theta = np.broadcast_arrays(
        _finite_array(rho, "rho", positive=True),
        _finite_array(theta, "theta"),
    )
    C = np.maximum(-theta, 0)
    excess = np.maximum(params.tau * C - 1, 0)
    activated = activation(rho / params.rho_q) * excess
    q = params.k_star * rho * density_weight(rho, params) * activated
    dk_dt = params.k_star * C * activated
    return q, dk_dt
