"""Energy-selected isentropic endpoint, conditional on actual isentropization.

The mass and conserved energy select K; no positive entropy floor is supplied.
The calculation assumes an isolated, baryon-free, regular hydrostatic sphere
with spatially constant K and a pressure-free surface at rho=rho_q.
It does not establish that any transport evolution converges to this branch.

For a differentiable fixed-mass equilibrium branch, the stationary envelope is
dE_eq/dK=integral W dm>0. The moving free boundary introduces no work because
P_surface=0; the latent specific energy W_surface=3*rho_q/2 remains in E.
The large-K limit is a sphere of density rho_q and E -> +infinity. The small-K
limit is the dense n=1 polytrope, R~sqrt(pi*K/(2G)) and
E~-G*M**2/(2R) -> -infinity. Uniqueness additionally uses the single regular
fixed-mass branch. Its absence of mass turning points follows from the positive
adiabatic radial gap, provided parameter derivatives are admissible radial
displacements. These are equilibrium facts, not a global convergence proof.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from equilibria import solve_equilibrium
from material import (MaterialParameters, activation, density_weight,
                      dimensionless_enthalpy)

_UNIT_MATERIAL = MaterialParameters(rho_q=1, G=1, a0=np.sqrt(8*np.pi), tau=1)


def _positive(value, name):
    if np.ndim(value) != 0 or not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive scalar")
    return float(value)


def initial_uniform_sphere_energy(mass, radius, velocity_gradient, G):
    """Continuum energy of a virgin uniform sphere with v=H*r and K=0."""
    mass, radius, G = (_positive(mass, "mass"), _positive(radius, "radius"),
                       _positive(G, "G"))
    if np.ndim(velocity_gradient) != 0 or not np.isfinite(velocity_gradient):
        raise ValueError("velocity gradient must be a finite scalar")
    return 3/10*velocity_gradient**2*mass*radius**2 - 3/5*G*mass**2/radius


def isentropic_equilibrium(central_density, mass, params, *, rtol=1e-10,
                           quadrature_rtol=2e-9, max_step=0.025):
    """Compute a constant-K equilibrium at fixed dimensional mass.

    Three profile quadratures independently give U, Omega and integral P dV.
    A fourth directly integrates the virial energy K*integral(W-3*rho*h) dm.
    """
    mass = _positive(mass, "mass")
    quadrature_rtol = _positive(quadrature_rtol, "quadrature_rtol")
    shape = solve_equilibrium(central_density, rtol=rtol, max_step=max_step)
    K = (mass*np.sqrt(4*np.pi)*params.G**1.5/(params.rho_q*shape.mass))**(2/3)
    length = np.sqrt(K/(4*np.pi*params.G))
    mass_scale = 4*np.pi*params.rho_q*length**3
    energy_scale = K*params.rho_q*mass_scale
    points = []
    if central_density > 2:
        transition = brentq(lambda x: float(shape.enthalpy(x))-2.5,
                             0.0, shape.radius, xtol=1e-12)
        points.append(transition)

    def integrand(x, kind):
        d = float(shape.density(x))
        w = float(density_weight(d, _UNIT_MATERIAL))
        h = float(activation(d))
        if kind == "internal":
            return x*x*d*w
        if kind == "gravity":
            return float(shape.mass_inside(x))*x*d
        if kind == "pressure":
            return x*x*d*d*h
        return x*x*d*(w-3*d*h)

    integrals = {}
    errors = {}
    for kind in ("internal", "gravity", "pressure", "virial_energy"):
        integrals[kind], errors[kind] = quad(
            integrand, 0, shape.radius, args=(kind,), points=points,
            epsabs=1e-11, epsrel=quadrature_rtol, limit=160)
    internal = energy_scale*integrals["internal"]
    gravity = -energy_scale*integrals["gravity"]
    pressure = energy_scale*integrals["pressure"]
    energy = energy_scale*integrals["virial_energy"]
    return {"central_density": float(central_density), "central_physical_density":
            float(params.rho_q*central_density), "K": float(K),
            "K_over_Kstar": float(K/params.k_star), "mass": float(mass_scale*shape.mass),
            "radius": float(length*shape.radius),
            "half_mass_radius": float(length*shape.half_mass_radius),
            "internal_energy": float(internal), "gravitational_energy": float(gravity),
            "total_energy": float(energy), "direct_total_energy": float(internal+gravity),
            "pressure_volume_integral": float(pressure),
            "direct_minus_virial_energy": float(internal+gravity-energy),
            "virial_relative_residual": float((gravity+3*pressure)/abs(gravity)),
            "entropy": float(mass*np.cbrt(K/params.k_star)),
            "energy_derivative_wrt_K": float(internal/K),
            "dimensionless_shape": {"radius": shape.radius, "mass": shape.mass,
                                     "half_mass_radius": shape.half_mass_radius},
            "quadrature_error_estimates": {key: float(energy_scale*value)
                                            for key, value in errors.items()}}


def solve_energy_limit(initial_energy, mass, params, *, central_bracket=(1.05, 10.0),
                       rtol=1e-10, quadrature_rtol=2e-9, max_step=0.025):
    """Select the regular isentropic equilibrium using mass and energy alone."""
    if np.ndim(initial_energy) != 0 or not np.isfinite(initial_energy):
        raise ValueError("initial energy must be a finite scalar")
    cache = {}

    def branch(dc):
        if dc not in cache:
            cache[dc] = isentropic_equilibrium(dc, mass, params, rtol=rtol,
                                               quadrature_rtol=quadrature_rtol,
                                               max_step=max_step)
        return cache[dc]

    def residual(dc):
        return branch(dc)["total_energy"]-initial_energy

    low, high = map(float, central_bracket)
    if not 1 < low < high:
        raise ValueError("central bracket must satisfy 1<low<high")
    for _ in range(32):
        if residual(low) >= 0:
            break
        low = 1+(low-1)/2
    else:
        raise RuntimeError("low-density energy bracket exhausted")
    for _ in range(32):
        if residual(high) <= 0:
            break
        high *= 2
    else:
        raise RuntimeError("high-density energy bracket exhausted")
    dc = brentq(residual, low, high, xtol=1e-10, rtol=1e-11)
    result = dict(branch(dc))
    result.update(initial_energy=float(initial_energy),
                  energy_residual=float(residual(dc)),
                  central_density_bracket=[low, high], equilibrium_evaluations=len(cache))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--initial-energy", type=float)
    parser.add_argument("--mass", type=float, default=np.pi/3)
    parser.add_argument("--initial-radius", type=float, default=1)
    parser.add_argument("--initial-velocity-gradient", type=float, default=-0.25)
    parser.add_argument("--rho-q", type=float, default=1)
    parser.add_argument("--G", type=float, default=1)
    parser.add_argument("--k-star", type=float, default=1)
    parser.add_argument("--rtol", type=float, default=1e-10)
    parser.add_argument("--quadrature-rtol", type=float, default=2e-9)
    parser.add_argument("--max-step", type=float, default=0.025)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    params = MaterialParameters(rho_q=args.rho_q, G=args.G,
                                a0=np.sqrt(8*np.pi*args.G*args.k_star*args.rho_q**2), tau=1)
    continuum_energy = initial_uniform_sphere_energy(
        args.mass, args.initial_radius, args.initial_velocity_gradient, args.G)
    target = continuum_energy if args.initial_energy is None else args.initial_energy
    endpoint = solve_energy_limit(target, args.mass, params, rtol=args.rtol,
                                  quadrature_rtol=args.quadrature_rtol, max_step=args.max_step)
    report = {"scope": "conditional static endpoint after isentropization; no convergence theorem",
              "mass": args.mass, "rho_q": params.rho_q, "G": params.G,
              "Kstar": params.k_star, "continuum_initial_energy": continuum_energy,
              "energy_source": "uniform_sphere_continuum" if args.initial_energy is None else "explicit",
              "initial_energy": target, "endpoint": endpoint,
              "rtol": args.rtol, "quadrature_rtol": args.quadrature_rtol,
              "max_step": args.max_step,
              "selection_inputs": ["mass", "energy", "material density gate", "G"],
              "branch_hypotheses": ["regular isolated hydrostatic sphere",
                                    "spatially constant K", "pressure-free material surface",
                                    "single differentiable fixed-mass equilibrium branch"]}
    rendered = json.dumps(report, indent=2, allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", dir=args.output.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(rendered)
        try:
            os.replace(temporary, args.output)
        finally:
            temporary.unlink(missing_ok=True)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
