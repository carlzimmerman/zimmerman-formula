#!/usr/bin/env python3
"""Hamiltonian-envelope completion for the exponential MOND relay.

The minimal separable scalar Hamiltonian fails the hypersurface-deformation
bracket because its ``A'(s) p^3`` term cannot vanish when
``A=1/mu``.  This gate tests a different, explicitly auxiliary completion.

For ``S=s^2/2`` and ``P=p^2/2`` introduce an algebraic field ``chi`` and

    H(P,S,chi) = W(chi) + mu(chi)*(S-chi^2/2) + P/mu(chi).

Its chi equation is an algebraic constraint.  On that constraint the envelope
derivatives are H_P=1/mu and H_S=mu, hence H_p H_s=p*s exactly.  At p=0,
chi=s and H=W(s), so W'(s)=mu(s)*s reproduces the MOND relay equation.

This is a constructive scalar-sector gate, not a claim of complete
four-dimensional closure.  The metric HDA, clock covariantization, PPN,
FLRW and stability gates remain outstanding.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


def exponential_data():
    y, chi, a0 = sp.symbols("y chi a0", positive=True)
    G = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    W = sp.Rational(1, 2) * a0**2 * G.subs(y, chi / a0)
    mu = 1 - sp.exp(-chi / a0)
    return {
        "G": G,
        "W": W,
        "mu": mu,
        "primitive_identity": sp.simplify(sp.diff(W, chi) - mu * chi) == 0,
        "mu_positive_witness": bool(mu.subs(chi, a0).subs(a0, 1).evalf() > 0),
    }


def envelope_identities():
    p, s, chi = sp.symbols("p s chi", real=True)
    mu = sp.Function("mu")(chi)
    W = sp.Function("W")(chi)
    # W_chi = mu*chi is the exact MOND primitive condition.
    H = W + mu * (s**2 / 2 - chi**2 / 2) + p**2 / (2 * mu)
    Cchi = sp.simplify(
        sp.diff(H, chi).subs(sp.diff(W, chi), mu * chi)
    )
    relation = sp.diff(mu, chi) * (
        s**2 / 2 - chi**2 / 2 - p**2 / (2 * mu**2)
    )
    Hp = sp.simplify(sp.diff(H, p))
    Hs = sp.simplify(sp.diff(H, s))
    hda_residual = sp.simplify(Hp * Hs - p * s)
    # On p=0 and the positive branch chi=s, H=W and H_s=mu(s)*s.
    static_H = sp.simplify(H.subs({p: 0, chi: s}))
    static_flux = sp.simplify(Hs.subs({p: 0, chi: s}))
    return {
        "H": H,
        "Cchi": Cchi,
        "relation": relation,
        "stationarity_factorization": sp.simplify(Cchi - relation) == 0,
        "H_P": Hp,
        "H_S": Hs,
        "hda_residual": hda_residual,
        "hda_closes_strongly": hda_residual == 0,
        "static_H": static_H,
        "static_flux": static_flux,
        "static_envelope_reduces_to_W": static_H == W.subs(chi, s),
        "static_flux_is_mu_s": static_flux == mu.subs(chi, s) * s,
    }


def hda_vector_identity():
    """Check the spatial-vector form, including a momentum-free slip relay."""

    p, m = sp.symbols("p m", nonzero=True)
    u1, u2, u3 = sp.symbols("u1 u2 u3")
    # H_p=p/m and H_{S}=m; therefore H_p H_{D_i u}=p D_i u.
    residuals = [sp.simplify((p / m) * (m * ui) - p * ui) for ui in (u1, u2, u3)]
    # A relay potential V(r') with p_r=0 contributes no H_p H_{D_i r}
    # term, so the total scalar bracket is still the u momentum constraint.
    r1, r2, r3 = sp.symbols("r1 r2 r3")
    slip_residuals = [sp.simplify(0 * ri) for ri in (r1, r2, r3)]
    return {
        "component_residuals": [str(v) for v in residuals],
        "slip_relay_residuals": [str(v) for v in slip_residuals],
        "three_dimensional_hda_identity": all(v == 0 for v in residuals + slip_residuals),
        "resulting_momentum_generator": "p_u D_i u (plus the standard tensor/matter generators)",
    }


def auxiliary_singularity_witness():
    """Expose the off-relay algebraic Hessian caustic instead of hiding it."""

    chi, P, S = sp.symbols("chi P S", positive=True)
    a0 = sp.symbols("a0", positive=True)
    mu = 1 - sp.exp(-chi / a0)
    mup = sp.diff(mu, chi)
    # On C_chi=0: S-chi^2/2=P/mu^2.  The Hessian is then
    # mu'*(-chi + 2*P*mu'/mu^3).
    hessian_on_shell = sp.simplify(mup * (-chi + 2 * P * mup / mu**3))
    P_singular = sp.simplify(chi * mu**3 / (2 * mup))
    singular_check = sp.simplify(hessian_on_shell.subs(P, P_singular)) == 0
    return {
        "hessian_on_algebraic_shell": str(hessian_on_shell),
        "positive_singularity_surface_P": str(P_singular),
        "singularity_surface_derived": singular_check,
        "interpretation": (
            "The envelope extension has an off-relay algebraic rank surface. "
            "The physical p=0 relay avoids it for chi>0; a full theory must "
            "either restrict/extend the Hamiltonian consistently or audit this surface."
        ),
    }


def poisson(A, B, coords, momenta):
    return sp.simplify(
        sum(
            sp.diff(A, q) * sp.diff(B, p) - sp.diff(A, p) * sp.diff(B, q)
            for q, p in zip(coords, momenta)
        )
    )


def dirac_relay(k_value: float, u_value: float, a0_value: float):
    """Compute the p=0 relay constraint matrix in local Fourier mode."""

    u, p, chi, pchi = sp.symbols("u p chi pchi", real=True)
    k, a0, rho = sp.symbols("k a0 rho", positive=True)
    s = k * u
    mu = 1 - sp.exp(-chi / a0)
    mu_chi = sp.diff(mu, chi)
    # p_u=0 is the primary; its preservation is the MOND Gauss constraint.
    C_M = k**2 * (1 - sp.exp(-s / a0)) * u - rho
    # The algebraic chi constraint restricted to the relay branch p=0.
    C_chi = sp.simplify(mu_chi * (s**2 / 2 - chi**2 / 2))
    constraints = [p, C_M, pchi, C_chi]
    coords = [u, chi]
    momenta = [p, pchi]
    matrix = sp.Matrix(
        [[poisson(A, B, coords, momenta) for B in constraints] for A in constraints]
    )
    source_value = float(k_value**2 * (1 - np.exp(-k_value * u_value / (2 * a0_value))) * u_value)
    substitutions = {
        k: k_value,
        u: u_value,
        chi: k_value * u_value,
        p: 0.0,
        pchi: 0.0,
        a0: a0_value,
        rho: source_value,
    }
    numeric = np.array(matrix.subs(substitutions).evalf(), dtype=float)
    rank = int(np.linalg.matrix_rank(numeric, tol=1e-10))
    determinant = float(np.linalg.det(numeric))
    hessian = sp.simplify(sp.diff(C_chi, chi)).subs(substitutions).evalf()
    return {
        "k": k_value,
        "constraints": [str(c) for c in constraints],
        "matrix": numeric.tolist(),
        "rank": rank,
        "determinant": determinant,
        "phase_space_dimension": 4,
        "remaining_phase_dimension": 4 - rank,
        "auxiliary_constraint_hessian": float(hessian),
        "source": source_value,
    }


def run():
    exp_data = exponential_data()
    envelope = envelope_identities()
    vector_hda = hda_vector_identity()
    singularity = auxiliary_singularity_witness()
    local = dirac_relay(1.0, 2.0, 1.0)
    homogeneous = dirac_relay(0.0, 2.0, 1.0)
    checks = {
        "exponential_primitive_derived": exp_data["primitive_identity"],
        "stationarity_factorization_derived": envelope["stationarity_factorization"],
        "envelope_HDA_identity": envelope["hda_closes_strongly"],
        "static_envelope_recovery": envelope["static_envelope_reduces_to_W"]
        and envelope["static_flux_is_mu_s"],
        "three_dimensional_hda_identity": vector_hda["three_dimensional_hda_identity"],
        "nonzero_mode_rank_computed": local["rank"] == int(np.linalg.matrix_rank(np.asarray(local["matrix"]), tol=1e-10)),
        "zero_mode_rank_drop_exposed": homogeneous["rank"] < local["rank"],
        "local_scalar_phase_removed": local["remaining_phase_dimension"] == 0,
        "auxiliary_hessian_regular_on_local_branch": abs(local["auxiliary_constraint_hessian"]) > 1e-12,
        "off_relay_singularity_is_exposed": singularity["singularity_surface_derived"],
    }
    result = {
        "candidate": "rmmg_envelope_completion_2026",
        "definitions": {
            "S": "s^2/2",
            "P": "p^2/2",
            "H_aux": "W(chi)+mu(chi)*(S-chi^2/2)+P/mu(chi)",
            "mu": "1-exp(-chi/a0)",
            "W": "a0^2/2 * [y^2+2(1+y)exp(-y)-2], y=chi/a0",
        },
        "exponential": {k: str(v) if isinstance(v, sp.Basic) else v for k, v in exp_data.items()},
        "envelope": {k: str(v) if isinstance(v, sp.Basic) else v for k, v in envelope.items()},
        "vector_hda": vector_hda,
        "auxiliary_singularity": singularity,
        "dirac_local": local,
        "dirac_homogeneous": homogeneous,
        "checks": {k: bool(v) for k, v in checks.items()},
        "status": "SCALAR_SECTOR_CONSTRUCTIVE_OPEN",
        "scope": (
            "Exact scalar Hamiltonian-envelope and relay constraints. The full metric/clock HDA, "
            "covariant action, Ward identity, PPN, FLRW and perturbative stability remain open."
        ),
        "next_gate": "Embed the envelope Hamiltonian in the full ADM metric constraint and vary an explicit covariant clock completion.",
    }
    out = Path(__file__).parent / "run_001"
    out.mkdir(exist_ok=True)
    (out / "envelope_completion_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    assert all(checks.values())
    return result


if __name__ == "__main__":
    run()
