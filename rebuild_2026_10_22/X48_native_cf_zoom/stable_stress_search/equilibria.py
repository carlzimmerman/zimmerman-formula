#!/usr/bin/env python3
"""Fixed-entropy spherical cores; no formation or production X48 evolution.

Dimensionless variables are d=rho/rho_q, x=r/L, L=sqrt(K/(4*pi*G)),
m=M/(4*pi*rho_q*L**3), and H=enthalpy/(K*rho_q). K is constant.
Then H' = -(m+m_b)/x**2, m'=x**2*d(H). The external baryons are
Plummer: m_b(x)=B*x**3/(x**2+b**2)**(3/2), b>0.
"""
import argparse
from dataclasses import dataclass
import json
import math
import os
from pathlib import Path
import tempfile

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from material import dimensionless_enthalpy


def density_from_enthalpy(enthalpy):
    """Inverse on the occupied branch, d>=1; H<=0 returns surface d=1.

    The extension for negative H is used only for an ODE event bracket. It
    must not be interpreted as a physical exterior density.
    """
    value = float(enthalpy)
    if not math.isfinite(value):
        raise ValueError("enthalpy must be finite")
    if value <= 0:
        return 1.0
    if value >= 2.5:
        return (value + 1.5) / 2
    root = brentq(lambda t: 3*t*t + 2*t**3 - 2.5*t**4 - value,
                  0.0, 1.0, xtol=5e-15)
    return 1.0 + root


@dataclass
class Equilibrium:
    central_density: float
    radius: float
    mass: float
    half_mass_radius: float
    core_radius: float
    baryon_mass: float
    baryon_scale: float
    solution: object
    start: float
    central_enthalpy: float

    def radius_at_mass_fraction(self, fraction):
        if not np.isfinite(fraction) or not 0 < fraction < 1:
            raise ValueError("mass fraction must lie strictly between zero and one")
        return brentq(lambda x: self.mass_inside(x) - fraction*self.mass,
                      0.0, self.radius, xtol=1e-11)

    def mass_inside(self, x):
        values = np.asarray(x, dtype=float)
        if np.any(values < 0) or np.any(values > self.radius * (1 + 1e-12)):
            raise ValueError("profile radius must lie inside the cold sphere")
        clipped = np.clip(values, self.start, self.radius)
        result = np.asarray(self.solution.sol(clipped)[1])
        return np.where(values < self.start, self.central_density * values**3 / 3, result)

    def enthalpy(self, x):
        values = np.asarray(x, dtype=float)
        if np.any(values < 0) or np.any(values > self.radius * (1 + 1e-12)):
            raise ValueError("profile radius must lie inside the cold sphere")
        result = np.asarray(self.solution.sol(np.clip(values, self.start, self.radius))[0])
        central_baryons = 3 * self.baryon_mass / self.baryon_scale**3
        central = self.central_enthalpy - (self.central_density + central_baryons) * values**2 / 6
        return np.where(values < self.start, central, np.maximum(result, 0))

    def density(self, x):
        values = self.enthalpy(x)
        result = np.array([density_from_enthalpy(h) for h in np.ravel(values)])
        return result.reshape(np.shape(values))


def solve_equilibrium(central_density, baryon_mass=0.0, baryon_scale=1.0,
                      rtol=1e-8, max_step=0.05):
    """Integrate a regular core to its first pressure-free surface."""
    values = (central_density, baryon_mass, baryon_scale, rtol, max_step)
    if not all(np.ndim(v) == 0 and np.isfinite(v) for v in values):
        raise ValueError("parameters must be finite scalars")
    if central_density <= 1 or baryon_mass < 0 or baryon_scale <= 0 or rtol <= 0 or max_step <= 0:
        raise ValueError("require central density>1, baryon mass>=0 and positive scale/tolerances")
    hc = float(dimensionless_enthalpy(central_density))
    db0 = 3 * baryon_mass / baryon_scale**3
    x0 = min(1e-6, baryon_scale * 1e-4,
             math.sqrt(hc / (central_density + db0)) * 1e-3)
    initial = [hc - (central_density + db0) * x0*x0 / 6,
               central_density * x0**3 / 3]

    def rhs(x, y):
        mb = baryon_mass * (x / math.hypot(x, baryon_scale))**3
        return [-(y[1] + mb) / (x*x), x*x*density_from_enthalpy(y[0])]

    def surface(x, y):
        return y[0]
    surface.terminal = True
    surface.direction = -1
    solution = solve_ivp(rhs, (x0, 100.0), initial, events=surface,
                         dense_output=True, rtol=rtol, atol=rtol*1e-3,
                         max_step=max_step)
    if not solution.success or len(solution.t_events[0]) != 1:
        raise RuntimeError("equilibrium failed to reach a first finite pressure-free surface")
    radius = float(solution.t_events[0][0])
    mass = float(solution.y_events[0][0][1])
    half = brentq(lambda x: solution.sol(x)[1] - mass/2, x0, radius, xtol=1e-11)
    if central_density > 2:
        core_h = float(dimensionless_enthalpy(central_density/2))
        core = brentq(lambda x: solution.sol(x)[0] - core_h, x0, radius, xtol=1e-11)
    else:
        # Half the central density lies below the finite-density free surface.
        core = radius
    return Equilibrium(float(central_density), radius, mass, float(half),
                       float(core), float(baryon_mass), float(baryon_scale),
                       solution, x0, hc)


def match_mass(target_mass, baryon_mass, baryon_scale, central_hint=5.0,
               rtol=1e-8, max_step=0.05):
    """Find an isentropic core with fixed cold mass and prescribed baryons."""
    if not np.isfinite(target_mass) or target_mass <= 0:
        raise ValueError("target_mass must be positive and finite")
    def residual(dc):
        return solve_equilibrium(dc, baryon_mass, baryon_scale, rtol, max_step).mass - target_mass
    low = 1.001
    if residual(low) >= 0:
        raise RuntimeError("target mass below this solver's declared central-density bracket")
    high = max(2.0, float(central_hint))
    for _ in range(30):
        if residual(high) >= 0:
            break
        high *= 2
    else:
        raise RuntimeError("fixed-mass central-density bracket exhausted")
    center = brentq(residual, low, high, xtol=1e-8, rtol=1e-10)
    return solve_equilibrium(center, baryon_mass, baryon_scale, rtol, max_step)


def dust_shell_radius(initial_radius, enclosed_cold_mass, baryon_mass, baryon_scale):
    """Circular-orbit adiabatic reference: r[m+Mb(r)]=r_initial*m.

    This is a declared comparison model, not a general collisionless theorem.
    """
    values = (initial_radius, enclosed_cold_mass, baryon_mass, baryon_scale)
    if not all(np.isfinite(v) for v in values) or min(initial_radius, enclosed_cold_mass, baryon_scale) <= 0 or baryon_mass < 0:
        raise ValueError("invalid circular-shell reference parameters")
    if baryon_mass == 0:
        return float(initial_radius)
    def residual(x):
        mb = baryon_mass * (x/math.hypot(x, baryon_scale))**3
        return x*(enclosed_cold_mass + mb) - initial_radius*enclosed_cold_mass
    return brentq(residual, 0, initial_radius, xtol=1e-12)


def run_suite():
    """Declared loading grid and a tighter solve of the same implementation."""
    rows = []
    for dc in (5.0, 20.0):
        initial = solve_equilibrium(dc)
        initial_quantiles = {str(f): initial.radius_at_mass_fraction(f)
                             for f in (0.01, 0.05, 0.1, 0.5)}
        rows.append(dict(initial_central_density=dc, baryon_mass_fraction=0.0,
                         baryon_scale_over_initial_radius=None,
                         central_density=dc, cold_mass=initial.mass,
                         radius=initial.radius, core_radius=initial.core_radius,
                         half_mass_radius=initial.half_mass_radius,
                         half_mass_radius_ratio=1.0, dust_half_mass_radius_ratio=1.0,
                         relative_mass_error=0.0,
                         shell_radius_ratios={key: 1.0 for key in initial_quantiles},
                         dust_shell_radius_ratios={key: 1.0 for key in initial_quantiles}))
        for fraction in (0.1, 0.3):
            for scale in (0.1, 0.3):
                mb, b = fraction*initial.mass, scale*initial.radius
                final = match_mass(initial.mass, mb, b, central_hint=dc)
                dust = dust_shell_radius(initial.half_mass_radius, initial.mass/2, mb, b)
                shell_ratios = {key: final.radius_at_mass_fraction(float(key))/radius
                                for key, radius in initial_quantiles.items()}
                dust_ratios = {key: dust_shell_radius(radius, float(key)*initial.mass, mb, b)/radius
                               for key, radius in initial_quantiles.items()}
                rows.append(dict(initial_central_density=dc, baryon_mass_fraction=fraction,
                                 baryon_scale_over_initial_radius=scale,
                                 central_density=final.central_density,
                                 cold_mass=final.mass, radius=final.radius,
                                 core_radius=final.core_radius,
                                 half_mass_radius=final.half_mass_radius,
                                 half_mass_radius_ratio=final.half_mass_radius/initial.half_mass_radius,
                                 dust_half_mass_radius_ratio=dust/initial.half_mass_radius,
                                 relative_mass_error=abs(final.mass/initial.mass-1),
                                 shell_radius_ratios=shell_ratios,
                                 dust_shell_radius_ratios=dust_ratios))
    initial = solve_equilibrium(20.0)
    coarse = match_mass(initial.mass, .3*initial.mass, .1*initial.radius, central_hint=20)
    refined_initial = solve_equilibrium(20.0, rtol=1e-10, max_step=.0125)
    refined = match_mass(refined_initial.mass, .3*refined_initial.mass,
                         .1*refined_initial.radius, central_hint=20,
                         rtol=1e-10, max_step=.0125)
    refinement = {key: abs(getattr(refined,key)/getattr(coarse,key)-1)
                  for key in ("central_density", "radius", "core_radius", "half_mass_radius")}
    loaded = [row for row in rows if row["baryon_mass_fraction"] > 0]
    checks = dict(
        fixed_mass=all(row["relative_mass_error"] < 2e-7 for row in rows),
        finite_cores=all(np.isfinite(row["central_density"]) and row["core_radius"] > 0 for row in rows),
        contraction=all(0 < row["half_mass_radius_ratio"] < 1 for row in loaded),
        weaker_than_declared_dust_reference=all(row["half_mass_radius_ratio"] > row["dust_half_mass_radius_ratio"] for row in loaded),
        inner_shell_resistance=all(row["shell_radius_ratios"][key] > row["dust_shell_radius_ratios"][key]
                                   for row in loaded for key in row["shell_radius_ratios"]),
        refinement=all(value < 2e-5 for value in refinement.values()))
    return dict(schema="X48-memory-stress-equilibria-v1", rows=rows,
                normalization=dict(density="rho/rho_q", radius="r/sqrt(K/(4piG))",
                                   mass="M/[4pi rho_q (K/(4piG))^(3/2)]",
                                   entropy="K is spatially constant and fixed during baryon loading"),
                refinement_relative_changes=refinement, checks=checks,
                non_claims=["No time integration or selection of K from cold collapse",
                            "No forest-data likelihood or cosmological fit",
                            "Spherical smooth baryons only; no rotating disc or point-mass core claim",
                            "Circular-shell reference is a defined comparator, not all collisionless contraction"])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    report = run_suite()
    if args.output:
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=args.output.parent,
                                             suffix=".tmp", delete=False) as stream:
                temporary = stream.name
                json.dump(report, stream, indent=2, allow_nan=False)
                stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
            os.replace(temporary, args.output)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)
    else:
        print(json.dumps(report, indent=2, allow_nan=False))
    return 0 if all(report["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
