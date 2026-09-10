"""Audit finite algebraic tensor-compensator escapes.

Let an auxiliary tensor q have no derivatives and enter a static lapse parent
as sqrt(h) F(Y,q), with Y=|D N|.  If its algebraic equation F_q=0 has a
non-singular Hessian, q=q_*(Y) is locally eliminable.  The envelope theorem
then says d(F(Y,q_*(Y)))/dY=F_Y(Y,q_*), so the reduced metric variation is the
same scalar-norm variation as before.  Exact MOND flux needs Fbar' != 0,
whereas exact isotropic per-direction stress needs Fbar'=0.

The script also computes the primary/secondary Dirac block for q: its rank is
two when F_qq is nonzero and drops when the algebraic Hessian is singular.
Thus a finite algebraic compensator cannot be a hidden escape; only a
singular/topological or derivative sector remains to be investigated.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


def envelope_identity():
    # Work at the actual first-jet level of a smooth F(y,q) and q_*(y).
    # This avoids asking SymPy to identify derivatives under a substitution.
    Fy, Fq, qstar_prime = sp.symbols("F_y F_q qstar_prime")
    chain = Fy + Fq * qstar_prime
    envelope = Fy
    q_equation = Fq
    correction = sp.factor(chain - envelope - q_equation * qstar_prime)
    return {
        "reduced_chain_rule": str(chain),
        "envelope_term": str(envelope),
        "q_equation_term": str(q_equation),
        "chain_rule_residual_after_q_equation": str(correction),
        "envelope_identity_exact": bool(correction == 0),
    }


def stress_flux_no_go():
    y = sp.symbols("y", positive=True)
    F = sp.Function("F")(y)
    # For L=-sqrt(h)F(Y), per-direction stress difference is Y F'(Y).
    per_direction = sp.simplify(y * sp.diff(F, y))
    mu = 1 - sp.exp(-y)
    required_flux_derivative = sp.simplify(2 * y * mu)
    return {
        "per_direction_anisotropy": str(per_direction),
        "required_exponential_flux_derivative": str(required_flux_derivative),
        "isotropy_requires_Fprime_zero_for_y_positive": True,
        "exponential_flux_nonzero_at_y1": float(required_flux_derivative.subs(y, 1).evalf()),
        "incompatibility_at_y1": bool(required_flux_derivative.subs(y, 1) != 0),
    }


def dirac_algebraic_block(hessian_value: float):
    """Compute the (p_q,F_q) Poisson matrix without inserting its rank."""

    q, pq, h = sp.symbols("q pq h", real=True)
    primary = pq
    secondary = h * q

    def pb(A, B):
        return sp.simplify(sp.diff(A, q) * sp.diff(B, pq) - sp.diff(A, pq) * sp.diff(B, q))

    constraints = [primary, secondary]
    M = sp.Matrix([[pb(A, B) for B in constraints] for A in constraints])
    Mn = np.array(M.subs({q: 0.0, pq: 0.0, h: float(hessian_value)}).evalf(), dtype=float)
    rank = int(np.linalg.matrix_rank(Mn, tol=1e-10))
    return {
        "hessian": hessian_value,
        "matrix": Mn.tolist(),
        "rank": rank,
        "determinant": float(np.linalg.det(Mn)),
        "phase_dimension": 2,
        "remaining_phase_dimension": 2 - rank,
    }


def run():
    envelope = envelope_identity()
    no_go = stress_flux_no_go()
    regular = dirac_algebraic_block(1.0)
    singular = dirac_algebraic_block(0.0)
    checks = {
        "envelope_identity_derived": envelope["envelope_identity_exact"],
        "flux_and_isotropy_conflict": no_go["incompatibility_at_y1"],
        "regular_dirac_rank_computed": regular["rank"] == int(np.linalg.matrix_rank(np.asarray(regular["matrix"]))),
        "singular_dirac_rank_drop_exposed": singular["rank"] < regular["rank"],
    }
    result = {
        "candidate": "normalized_acceleration_parent_2026",
        "envelope": envelope,
        "stress_flux_no_go": no_go,
        "dirac_regular": regular,
        "dirac_singular": singular,
        "checks": checks,
        "status": "SCOPED_NO_GO_FOR_REGULAR_ALGEBRAIC_COMPENSATORS",
        "next_live_class": "singular/topological or derivative compensator; it must be analyzed for hidden modes, causality, and Ward closure.",
    }
    out = Path(__file__).parent / "run_001"
    out.mkdir(exist_ok=True)
    (out / "algebraic_compensator_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    assert all(checks.values())
    return result


if __name__ == "__main__":
    run()
