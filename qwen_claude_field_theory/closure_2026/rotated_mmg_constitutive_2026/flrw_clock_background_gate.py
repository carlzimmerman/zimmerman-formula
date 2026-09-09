"""FLRW background gate for the covariant clock repair.

For a shift-symmetric clock action M^4 K(X), with
X=g^{mu nu} d_mu T d_nu T and T=t on flat FLRW, the acceleration is zero and
the clock Euler equation is

    d_t(a^3 K_X * Tdot) = 0.

At Tdot=1 and X=-1 this becomes 3 H a^3 K_X(-1)=0.  Therefore an expanding
background with H != 0 forces K_X(-1)=0.  The DBI repair used by the scalar
principal gate has K_X(-1) != 0, so T=t is not an exact shift-symmetric FLRW
solution.  The alternative K_X(-1)=0 removes the k-essence gradient term and
returns the zero-speed clock sector.  A potential can balance the equation
only by supplying V_T(t)=-3 H(t) K_X(-1), an additional model function that
must be included in the full Ward/PPN analysis.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


t, A, Ld, H = sp.symbols("t A Ld H", positive=True)
a = sp.Function("a")(t)
chi = sp.symbols("chi", positive=True)

# chi=-X=Tdot^2 is positive on the timelike branch; this is the DBI clock
# written in the positive-chi convention.
K = -A * sp.sqrt(1 - chi**2 / Ld**2)
K_chi = sp.simplify(sp.diff(K, chi))

Tdot = sp.Integer(1)
chi_bg = sp.Integer(1)
current = sp.simplify(a**3 * K_chi.subs(chi, chi_bg) * Tdot)
clock_residual = sp.simplify(sp.diff(current, t).subs(sp.diff(a, t), H * a))
dbi_witness = sp.simplify(K_chi.subs({chi: 1, Ld: 2, A: 1}))

# If a potential V(T) is added, its derivative must cancel the residual.
required_potential_slope = sp.simplify(3 * H * K_chi.subs(chi, chi_bg))

results = {
    "K_chi": str(K_chi),
    "FLRW_clock_current": str(current),
    "shift_symmetric_clock_residual_Teq": str(clock_residual),
    "residual_factor_after_H_nonzero": str(sp.simplify(clock_residual / (3 * H * a**3))),
    "DBI_K_chi_at_chi1_L2_A1": str(dbi_witness),
    "DBI_nonzero_current_coefficient": bool(dbi_witness != 0),
    "H_nonzero_requires_K_chi_zero": True,
    "required_potential_slope": str(required_potential_slope),
    "potential_repair_is_fixed_constant": False,
    "status": "OBSTRUCTION: shift-symmetric DBI clock repair with T=t is not an exact H!=0 FLRW solution; imposing K_chi=0 removes the gradient repair, while a potential must track H(t).",
}

print(json.dumps(results, indent=2, sort_keys=True))
out = Path(__file__).parent / "run_001" / "flrw_clock_background_results.json"
out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")

assert sp.simplify(clock_residual - 3 * H * a**3 * K_chi.subs(chi, chi_bg)) == 0
assert results["DBI_nonzero_current_coefficient"]
assert results["H_nonzero_requires_K_chi_zero"]
assert not results["potential_repair_is_fixed_constant"]
