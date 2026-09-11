#!/usr/bin/env python3
"""Independent instantaneous WEAK-FIELD potentials from nonlinear slice jets.

Conventions: a(t0)=1, R(t0,r)=r, K_r=K_Omega=H_bg initially, and
g_ij=a**2[(1+2*zeta)delta_ij+2 E_,ij], g_0i=a**2 B_,i.
With beta=a**2(B-E_t), Phi_B=delta_N+beta_t and Psi_B=-zeta-H*beta.
Initial zero shear and exterior matching set beta=0, not beta_t=0.
The two reconstructions therefore use different data:

    Psi_B' = (A-1)/r,
    beta_t''-beta_t'/r = -(Kdot-3*hdot),
    Phi_B = delta_N+beta_t.

These equations are linear metric gauge transformations applied to time jets
of the nonlinear initial solution. Terms of second and higher order in source
amplitude are representation-dependent and ARE NOT nonlinear gravitational
slip. A finite small-source scaling check can verify the absence of an O(source)
slip in the tested family; it cannot establish nonlinear no-slip, lensing, or
PPN. No equality between Phi_B and Psi_B is supplied to either reconstruction.

Asymptotic assumption in reconstruct(): beyond the outer radius L the Gaussian
density and screened lapse tails are negligible and f=1-C/r. The exterior
time-jet equations then give shear=3*C/(2*r**3), hence beta_t=-C/(2*r),
beta_t'=C/(2*r**2). This follows by integrating the shear equation with no
constant or r**2 homogeneous mode, not by assigning Phi_B=Psi_B. The spatial A-1 tail
is integrated exactly: Psi_B(L)=2 log[(1+sqrt(f(L)))/2]. The ignored lapse tail
is reported, and changing the outer boundary is a required numerical control.
For non-negligible outer lapse tails use a larger domain or derive their
exterior integral; the present wrapper does not claim exact finite-L matching.

Sources: ../spherical_baryon_bridge/README.md (Bardeen conventions),
../spherical_baryon_bridge/action/REPORT.md (both metric Euler equations).
Float64 cubic-spline quadrature; regular center, positive f, finite inputs.
Mathbox computation-audit and test-driven-development guide the finite checks.
"""
import json

import numpy as np
from scipy.interpolate import CubicSpline


def _outside_integrals(r, values):
    integral = CubicSpline(r, values).antiderivative()
    return integral(r[-1])-integral(r)


def from_time_jets(r, f, delta, Kdot, hdot, *, psi_outer, beta_outer,
                   beta_prime_outer):
    """Integrate the two independent linear metric definitions.

Explicit outer values permit independent analytic-jet controls. They are
boundary data, not parameters fitted to a desired potential or slip.
"""
    r, f, delta, Kdot, hdot = [np.asarray(x, dtype=float)
                               for x in (r, f, delta, Kdot, hdot)]
    if (r.ndim != 1 or len(r) < 4 or r[0] != 0 or
            np.any(np.diff(r) <= 0) or any(x.shape != r.shape for x in
                                          (f, delta, Kdot, hdot))):
        raise ValueError("need increasing radial arrays including a regular center")
    if any(not np.all(np.isfinite(x)) for x in (r, f, delta, Kdot, hdot)):
        raise ValueError("all metric jets must be finite")
    if np.any(f <= 0):
        raise ValueError("the areal spatial coordinate patch requires f>0")
    if not np.all(np.isfinite([psi_outer, beta_outer, beta_prime_outer])):
        raise ValueError("outer matching values must be finite")

    sqrt_f = np.sqrt(f)
    # Stable A-1 avoids cancellation when the source is small.
    delta_A = (1-f)/(sqrt_f*(1+sqrt_f))
    psi_prime = np.zeros_like(r)
    psi_prime[1:] = delta_A[1:]/r[1:]
    Psi = psi_outer-_outside_integrals(r, psi_prime)

    shear = Kdot-3*hdot
    shear_over_r = np.zeros_like(r)
    shear_over_r[1:] = shear[1:]/r[1:]
    beta_dot_prime = r*(beta_prime_outer/r[-1]
                        + _outside_integrals(r, shear_over_r))
    beta_dot = beta_outer-_outside_integrals(r, beta_dot_prime)
    Phi = delta+beta_dot
    return {"r": r.copy(), "Phi": Phi, "Psi": Psi,
            "beta_dot": beta_dot, "beta_dot_prime": beta_dot_prime,
            "psi_prime": psi_prime, "slip": Phi-Psi,
            "shear": shear,
            "weak_field_size": float(max(np.max(abs(delta)),
                                           np.max(abs(delta_A))))}


def reconstruct(slice_data):
    """Apply explicit vacuum-curvature matching to a solve_slice result."""
    r = np.asarray(slice_data["r"])
    f = np.asarray(slice_data["f"])
    outer = r[-1]
    curvature_charge = outer*(1-f[-1])
    sqrt_f_outer = np.sqrt(f[-1])
    psi_outer = 2*np.log1p(-(1-f[-1])/(2*(1+sqrt_f_outer)))
    out = from_time_jets(
        r, f, slice_data["delta"], slice_data["Kdot"], slice_data["hdot"],
        psi_outer=psi_outer, beta_outer=-curvature_charge/(2*outer),
        beta_prime_outer=curvature_charge/(2*outer**2))
    out["outer_lapse_tail"] = float(max(abs(slice_data["delta"][-1]),
                                          abs(outer*slice_data["Nprime"][-1])))
    out["outer_curvature_charge"] = float(curvature_charge)
    potential_scale = float(np.max(abs(out["Psi"])))
    out["relative_slip"] = (float(np.max(abs(out["slip"]))/potential_scale)
                            if potential_scale else None)
    return out


def main():
    from initial import solve_slice
    rows = []
    for amplitude in (0., 2e-3, 1e-3, 5e-4):
        out = reconstruct(solve_slice(amplitude, .3, outer=20., points=2401))
        rows.append({"amplitude": amplitude,
                     "max_abs_phi": float(np.max(abs(out["Phi"]))),
                     "max_abs_psi": float(np.max(abs(out["Psi"]))),
                     "max_abs_slip": float(np.max(abs(out["slip"]))),
                     "relative_slip": out["relative_slip"],
                     "weak_field_size": out["weak_field_size"],
                     "outer_lapse_tail": out["outer_lapse_tail"]})
    print(json.dumps({"scope": "instantaneous weak-field reconstruction only",
                      "width": .3, "outer": 20., "points": 2401,
                      "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
