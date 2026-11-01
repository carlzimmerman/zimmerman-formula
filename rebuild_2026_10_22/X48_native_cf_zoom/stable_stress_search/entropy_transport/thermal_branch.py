"""Bounded static discriminator for thermally relaxed gated X48 spheres.

This computes hydrostatic branches at fixed mass, not their thermal stability
or dynamical accessibility.  Zero heat flux on a connected active interior
requires psi=(K/Kstar)*(W/rho_q)**(3/2) to be constant.  The resulting dense
pressure is proportional to sqrt(rho), so the constant-K radial gap cannot
be applied to perturbations that exchange heat.

Shapes obey H'=-m/x**2 and m'=x**2*d, with x=r/L and
L=sqrt(Kstar*psi/(4*pi*G)). Entropy means integral (K/Kstar)**(1/3) dm;
temperature is the conjugate to this dimensionless specific entropy.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from material import (MaterialParameters, activation, density_weight)


_UNIT_MATERIAL = MaterialParameters(rho_q=1, a0=np.sqrt(8*np.pi), G=1, tau=1)
ENTHALPY_LIMIT = 2 / np.sqrt(1.5)
_DENSE_THRESHOLD_H = ENTHALPY_LIMIT - 1 / np.sqrt(2)
DEFAULT_CENTRAL_DENSITIES = [1.1, 1.5, 2, 3, 5, 10, 20, 50, 100, 300, 1000]


def _positive(value, name):
    value = np.asarray(value, dtype=float)
    if value.ndim != 0 or not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive scalar")
    return float(value)


def thermal_pressure_shape(d):
    """p_T(d)=d**2*h(d)/w(d)**(3/2), with w=W/rho_q."""
    d = np.asarray(d, dtype=float)
    w = density_weight(d, _UNIT_MATERIAL)
    return d**2 * activation(d) / w**1.5


def thermal_enthalpy(d):
    """Dimensionless thermal enthalpy, zero on the entire dormant interval.

    Its derivative is p_T'(d)/d, and its upper limit as d -> infinity is
    finite: 2/sqrt(1.5). In the dense phase H=C-1/sqrt(d).
    """
    d = np.asarray(d, dtype=float)
    w = density_weight(d, _UNIT_MATERIAL)
    result = d * activation(d) / w**1.5 - 2/np.sqrt(w) + ENTHALPY_LIMIT
    return np.where(d <= 1, 0.0, result)


def density_from_thermal_enthalpy(enthalpy):
    """Invert the occupied d>=1 branch; reject H outside [0,H_infinity)."""
    values = np.asarray(enthalpy, dtype=float)
    if np.any(~np.isfinite(values)) or np.any(values < 0) or np.any(values >= ENTHALPY_LIMIT):
        raise ValueError("thermal enthalpy must be finite in [0,H_infinity)")
    result = np.empty_like(values)
    for index in np.ndindex(values.shape):
        value = float(values[index])
        if value == 0:
            result[index] = 1.0
        elif value >= _DENSE_THRESHOLD_H:
            result[index] = 1/(ENTHALPY_LIMIT-value)**2
        else:
            result[index] = brentq(lambda d: float(thermal_enthalpy(d))-value,
                                   1.0, 2.0, xtol=5e-15, rtol=1e-14)
    return float(result) if result.ndim == 0 else result


def solve_shape(central_density, *, rtol=1e-9, atol=1e-11, include_profile=False):
    """Integrate one regular, baryon-free thermal shape through its free surface.

    Returns dimensionless integrals u=integral x**2*d/sqrt(w) dx,
    g=integral m*x*d dx, p=integral x**2*p_T dx. Gravity has sign -g.
    No guessed surface radius or density truncation is used.
    """
    dc = _positive(central_density, "central density ratio")
    if dc <= 1:
        raise ValueError("central density ratio must exceed one")
    rtol, atol = _positive(rtol, "rtol"), _positive(atol, "atol")
    hc = float(thermal_enthalpy(dc))
    if not 0 < hc < ENTHALPY_LIMIT:
        raise ValueError("central enthalpy is unresolved in floating point")
    wc = float(density_weight(dc, _UNIT_MATERIAL))
    # Central series H=Hc-dc*x**2/6+O(x**4), m=dc*x**3/3+O(x**5).
    x0 = min(1e-6, 1e-5*np.sqrt(hc/dc))
    initial = [hc-dc*x0*x0/6, dc*x0**3/3,
               dc*x0**3/(3*np.sqrt(wc)), dc*dc*x0**5/15,
               float(thermal_pressure_shape(dc))*x0**3/3]
    # Since d>=1, H(x)<=Hc-x**2/6. This is a rigorous finite search bound.
    maximum_radius = np.sqrt(6*hc)*(1+1e-8)

    def rhs(x, state):
        enthalpy, mass = state[:2]
        d = density_from_thermal_enthalpy(max(0.0, enthalpy))
        w = float(density_weight(d, _UNIT_MATERIAL))
        return [-mass/x**2, x*x*d, x*x*d/np.sqrt(w), mass*x*d,
                x*x*float(thermal_pressure_shape(d))]

    def surface(x, state):
        return state[0]

    surface.terminal = True
    surface.direction = -1
    solution = solve_ivp(rhs, (x0, maximum_radius), initial, events=surface,
                         rtol=rtol, atol=atol, max_step=maximum_radius/300)
    if not solution.success or solution.t_events[0].size != 1:
        raise RuntimeError(f"thermal shape did not reach the free surface: {solution.message}")
    enthalpy, mass, internal, gravity, pressure = solution.y[:, -1]
    result = {"central_density": dc, "central_enthalpy": hc,
              "central_enthalpy_margin": ENTHALPY_LIMIT-hc,
              "radius": float(solution.t[-1]), "mass": float(mass),
              "internal": float(internal), "gravity_magnitude": float(gravity),
              "pressure_integral": float(pressure), "rhs_evaluations": solution.nfev,
              "virial_relative_residual": float((3*pressure-gravity)/gravity)}
    if include_profile:
        profile_h = np.maximum(0.0, solution.y[0])
        result["profile"] = {"x": np.r_[0.0, solution.t].tolist(),
                             "density": np.r_[dc, density_from_thermal_enthalpy(profile_h)].tolist(),
                             "mass": np.r_[0.0, solution.y[1]].tolist(),
                             "enthalpy": np.r_[hc, profile_h].tolist()}
    return result


def fixed_mass_branch(central_density, mass, params, *, rtol=1e-9, atol=1e-11,
                      include_profile=False):
    """Choose psi to give the requested dimensional mass and report its energy."""
    target_mass = _positive(mass, "mass")
    shape = solve_shape(central_density, rtol=rtol, atol=atol, include_profile=include_profile)
    psi = (target_mass*np.sqrt(4*np.pi)*params.G**1.5 /
           (params.rho_q*params.k_star**1.5*shape["mass"]))**(2/3)
    length = np.sqrt(params.k_star*psi/(4*np.pi*params.G))
    mass_scale = 4*np.pi*params.rho_q*length**3
    energy_scale = params.k_star*psi*params.rho_q*mass_scale
    internal = energy_scale*shape["internal"]
    gravity = -energy_scale*shape["gravity_magnitude"]
    wc = float(density_weight(float(central_density), _UNIT_MATERIAL))
    result = {"central_density": float(central_density), "psi": float(psi),
              "central_K": float(params.k_star*psi/wc**1.5),
              "central_enthalpy_margin": shape["central_enthalpy_margin"],
              "physical_enthalpy_margin": float(params.k_star*psi*params.rho_q *
                                                 shape["central_enthalpy_margin"]),
              "mass": float(mass_scale*shape["mass"]),
              "radius": float(length*shape["radius"]),
              "internal_energy": float(internal), "gravitational_energy": float(gravity),
              "total_energy": float(internal+gravity),
              "pressure_volume_integral": float(energy_scale*shape["pressure_integral"]),
              "entropy": float(psi**(1/3)*mass_scale*shape["internal"]),
              "temperature": float(3*params.k_star*params.rho_q*psi**(2/3)),
              "virial_relative_residual": shape["virial_relative_residual"],
              "shape": shape}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--central-densities", type=float, nargs="+", default=DEFAULT_CENTRAL_DENSITIES)
    parser.add_argument("--mass", type=float, default=np.pi/3)
    parser.add_argument("--initial-energy", type=float, default=-0.6381918589)
    parser.add_argument("--rho-q", type=float, default=1)
    parser.add_argument("--G", type=float, default=1)
    parser.add_argument("--k-star", type=float, default=1)
    parser.add_argument("--rtol", type=float, default=1e-9)
    parser.add_argument("--atol", type=float, default=1e-11)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    params = MaterialParameters(rho_q=args.rho_q, G=args.G,
                                a0=np.sqrt(8*np.pi*args.G*args.k_star*args.rho_q**2), tau=1)
    if not np.isfinite(args.initial_energy):
        parser.error("initial energy must be finite")
    branches = [fixed_mass_branch(dc, args.mass, params, rtol=args.rtol, atol=args.atol)
                for dc in args.central_densities]
    for branch in branches:
        branch["energy_minus_initial"] = branch["total_energy"]-args.initial_energy
    brackets = [[left["central_density"], right["central_density"]]
                for left, right in zip(branches, branches[1:])
                if left["energy_minus_initial"]*right["energy_minus_initial"] < 0]
    report = {"scope": "regular static branches; no thermal stability or formation claim",
              "rho_q": params.rho_q, "G": params.G, "Kstar": params.k_star,
              "mass": args.mass, "initial_energy": args.initial_energy,
              "enthalpy_limit": ENTHALPY_LIMIT, "rtol": args.rtol, "atol": args.atol,
              "branches": branches, "crossing_brackets": brackets}
    rendered = json.dumps(report, indent=2, allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", dir=args.output.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(rendered)
        try:
            os.replace(temporary, args.output)
        finally:
            temporary.unlink(missing_ok=True)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
