#!/usr/bin/env python3
"""Read-only, exact algebra checks for the accompanying review; not theory certification.

Run from any directory: python3 -B /path/to/check_review_algebra.py
Requires SymPy. Results and source hashes go to stdout; no source/output is overwritten.
"""
import ast
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


def main():
    checks = {}

    def require(name, condition):
        checks[name] = bool(condition)
        if not checks[name]:
            raise AssertionError(name)

    rho, scale, eps = sp.symbols("rho rho_star epsilon", positive=True)
    pressure = eps * scale * (1 - sp.exp(-rho / scale))
    cs2 = sp.diff(pressure, rho)
    w = pressure / rho
    # Homogeneous energy conservation: d rho / d ln(a) = -3 (rho + P).
    local_p = sp.simplify(sp.diff(sp.log(cs2), rho) * (-3 * (rho + pressure)))
    require("sound_speed_is_pressure_derivative",
            sp.simplify(cs2 - eps * sp.exp(-rho / scale)) == 0)
    require("pressure_is_concave", sp.diff(pressure, rho, 2).is_negative)
    require("pressure_at_zero", pressure.subs(rho, 0) == 0)
    require("exact_local_growth_from_continuity",
            sp.simplify(local_p - 3 * (1 + w) * rho / scale) == 0)
    # This point is dustlike, causal, NEC-safe and violates BOTH advertised local ceilings.
    point = {rho: 2, scale: 1, eps: sp.Rational(1, 10**6)}
    p0, w0, c0 = (v.subs(point) for v in (local_p, w, cs2))
    require("counterexample_is_dustlike", 0 < w0 < sp.Rational(1, 10**6))
    require("counterexample_is_causal_and_respects_cs2_le_w", 0 < c0 < w0 < 1)
    require("universal_local_p_ceiling_is_false", p0 > 3 * (1 + w0) > 3)
    require("controlled_small_density_sound_speed", sp.limit(cs2, rho, 0) == eps)
    # Generic chain rule, with X = Q^2/2; an extra factor 2 in the reciprocal is incorrect.
    Q = sp.symbols("Q", positive=True)
    X = sp.symbols("X", positive=True)
    P = sp.Function("P")
    K = P(Q**2 / 2)
    kqq = sp.diff(K, Q, 2)
    expected = (sp.diff(P(X), X) + 2 * X * sp.diff(P(X), X, 2)).subs(X, Q**2 / 2)
    require("KQQ_chain_rule", sp.simplify(kqq - expected) == 0)
    # Faster than quadratic need not mean asymptotically dustlike: K=Q^3 gives w=1/2.
    cubic = Q**3
    cubic_rho = Q * sp.diff(cubic, Q) - cubic
    require("superquadratic_is_not_sufficient_for_dust", sp.simplify(cubic / cubic_rho) == sp.Rational(1, 2))

    root = Path(__file__).resolve().parents[3]
    names = [
        "L137_aest_dust_stiff_correction.py",
        "L139_cuscuton_transplant_route2_open.py",
        "L152_RUNNING_CS2_BOLTZMANN_VERDICT.md",
        "L152_running_cs2_cmb_boltzmann.py",
        "L152_running_cs2_pk_lyman_alpha.py",
        "L152_class_running_cs2/running_cs2.patch",
        "L152_class_running_cs2/apply_running_cs2_patch.py",
        "L152_class_running_cs2/build_patched_classy.sh",
        "L153a_identity_soundspeed_coupling.py",
        "L153e_verdict_window.py",
        "L155_disformal_gamma_cure.py",
        "L157_soundspeed_growth_realizability.py",
        "L158_gdm_loophole_verdict.py",
        "L165_smooth_dust_third_peak_calibrated_sigma.py",
        "lean_2026/Mondlean.lean",
    ]
    hashes = {name: hashlib.sha256((root / "fable_independent_2026" / name).read_bytes()).hexdigest()
              for name in names}
    target = root / "fable_independent_2026/L139_cuscuton_transplant_route2_open.py"
    tree = ast.parse(target.read_text())
    literal_checks = sorted(n.lineno for n in ast.walk(tree)
                            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                            and n.func.id == "check" and len(n.args) > 1
                            and isinstance(n.args[1], ast.Constant) and n.args[1].value is True)
    print(json.dumps({
        "scope": "Exact review algebra only; no full action, Lean build or Boltzmann rerun",
        "python": platform.python_version(), "sympy": sp.__version__,
        "checks": checks,
        "counterexample": {"P": str(pressure), "cs2": str(cs2), "local_p": str(local_p),
                           "at_rho_over_rho_star_2_epsilon_1e_minus_6":
                           {"cs2": str(sp.N(c0, 17)), "w": str(sp.N(w0, 17)), "p": str(sp.N(p0, 17))}},
        "KQQ": str(kqq), "L139_literal_true_check_lines": literal_checks,
        "source_sha256": hashes,
    }, indent=2))


if __name__ == "__main__":
    main()
