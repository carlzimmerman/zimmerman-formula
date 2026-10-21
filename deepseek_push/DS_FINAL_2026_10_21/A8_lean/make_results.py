#!/usr/bin/env python3
"""Assemble a8_results.json from the Lean build logs and the check run.

Reads:  A8_*.out (compiler output, #print axioms lines)
        a8_lean_checks.py (to re-derive the check table)
Writes: a8_results.json
Deterministic, stdlib only, no network.
"""
import contextlib
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a8_lean_checks as C  # noqa: E402

CERTIFIES = {
    # C1 / C2
    "A8.a0_sq": "squares the vacuum-tied scale: a0^2 = kappa^2 c^2 G rho",
    "A8.kappa_Z_identity": "(a0/(cH))^2 = kappa^2*3/(8 pi) from a0=kappa c sqrt(G rho) and H^2=8 pi G rho/3",
    "A8.kappa_half_sq": "kappa=1/2 specialization: (a0/(cH))^2 = 3/(32 pi)",
    "A8.inv_two_sqrt_sq": "the target closed form 1/(2 sqrt(8 pi/3)) squares to 3/(32 pi)",
    "A8.a0_over_cH_eq_inv_two_sqrt": "positive branch: a0/(cH) = 1/(2 sqrt(8 pi/3)) = 1/Z",
    "A8.two_sqrt_32pi_3": "2 sqrt(32 pi/3) = 2(2 sqrt(8 pi/3)) = 2Z, exact identity in pi",
    "A8.inv_two_sqrt_eq_sqrt_ratio": "1/(2 sqrt(8 pi/3)) = sqrt(3/(32 pi)): the two closed forms are the same number",
    "A8.inv_twoZ_bracket": "1/12 < 1/(2Z) < 1/11: 'one twelfth' is not an identity",
    "A8.inv_twoZ_ne_twelfth": "1/(2Z) != 1/12",
    # C3
    "A8.gCanon_form": "g_c = gN/2 + sqrt(gN^2/4 + a0 gN): division-free form of the canonical root",
    "A8.gCanon_gt_gN": "canonical law exceeds Newton: gN < g_c",
    "A8.gQuad_gt_gN": "n=2 law exceeds Newton: gN < g_q",
    "A8.gCanon_root": "g_c^2 = gN(g_c + a0): the closed form satisfies the canonical law",
    "A8.gQuad_root": "g_q^2 = gN^2 + a0 gN: the closed form satisfies the n=2 law",
    "A8.gCanon_root_unique": "g_c is THE positive root of the canonical equation (uniqueness)",
    "A8.gCanon_sq_sub_gQuad_sq": "g_c^2 - g_q^2 = gN(g_c - gN): exact difference of squares",
    "A8.gQuad_lt_gCanon": "strict ordering g_q < g_c for ALL gN,a0>0; no extra hypothesis",
    "A8.gCanon_sub_gQuad_eq": "exact gap g_c - g_q = a0 gN^2/(g_c(g_c+g_q))",
    "A8.gCanon_sub_gQuad_le_gN": "gap bound g_c - g_q <= gN",
    "A8.gCanon_sub_gQuad_le_a0": "gap bound g_c - g_q <= a0",
    "A8.gQuad_normalised_tendsto": "deep limit: g_q/sqrt(a0 gN) -> 1 as gN/a0 -> 0+",
    "A8.gCanon_normalised_tendsto": "deep limit: g_c/sqrt(a0 gN) -> 1 as gN/a0 -> 0+",
    "A8.gap_tendsto_a0_zero": "Newtonian limit: gap -> 0 as a0 -> 0+ at fixed gN",
    # C4
    "A8.deriv_gQuad": "d/dgN sqrt(gN^2+a0 gN) = (2 gN+a0)/(2 sqrt(gN^2+a0 gN))",
    "A8.deriv_gCanon": "d/dgN g_c = 1/2 + (gN/2+a0)/(2 sqrt(gN^2/4+a0 gN))",
    "A8.deriv_gQuad_pos": "dg_q/dgN > 0 at every gN > 0",
    "A8.deriv_gCanon_pos": "dg_c/dgN > 0 at every gN > 0",
    "A8.gQuad_strictMonoOn": "n=2 closed form is strictly increasing on gN > 0",
    "A8.gCanon_strictMonoOn": "canonical closed form is strictly increasing on gN > 0",
    "A8.gQuad_slope_pos": "every difference quotient of the n=2 law is > 0",
    "A8.gCanon_slope_pos": "every difference quotient of the canonical law is > 0",
    "A8.gQuad_strictMonoOn_a0": "n=2 law is strictly increasing in a0",
    "A8.gCanon_strictMonoOn_a0": "canonical law is strictly increasing in a0",
    # C5
    "A8.mu_eq_of_canonical": "on the canonical law, gN/g = mu(g/a0) = x/(1+x)",
    "A8.boost_eq_one_add": "on the canonical law, g/gN = 1 + a0/g",
    "A8.mu_pos": "0 < mu x for x > 0",
    "A8.mu_lt_one": "mu x < 1 for x > 0",
    "A8.mu_tendsto_zero": "mu -> 0 as x -> 0",
    "A8.mu_tendsto_one": "mu -> 1 as x -> atTop",
}

NUMBERS = {
    "Z": {"value": 5.788810036466141, "formula": "2*sqrt(8*pi/3)", "source": "python float, exact formula"},
    "inv_Z": {"value": 0.17274707473566775, "formula": "1/Z = a0/(c H_Lambda)", "source": "python float"},
    "two_Z": {"value": 11.577620072932282, "formula": "2Z", "source": "python float"},
    "inv_two_Z": {"value": 0.08637353736783387, "formula": "1/(2Z)", "source": "python float"},
    "three_over_32pi": {"value": 0.029841551829730376, "formula": "3/(32*pi)", "source": "python float"},
    "inv_twelfth": {"value": 0.08333333333333333, "formula": "1/12", "source": "exact rational"},
    "rel_gap_inv_two_Z_vs_twelfth": {"value": 0.036482448414006496,
                                     "formula": "(1/(2Z))/(1/12) - 1", "source": "python float"},
    "ratio_inv_Z_to_twelfth": {"value": 2.072964896828013, "formula": "(1/Z)/(1/12)", "source": "python float"},
    "rho_Lambda_from_brief": {"value": 5.834769475277012e-27, "unit": "kg/m^3",
                              "formula": "Lambda c^2/(8 pi G)", "source": "BRIEF constants"},
    "a0_from_formula": {"value": 9.354173485820239e-11, "unit": "m/s^2",
                        "formula": "kappa c sqrt(G rho_Lambda), kappa=1/2", "source": "BRIEF constants"},
    "a0_quoted": {"value": 9.36e-11, "unit": "m/s^2", "source": "BRIEF section 4 (quoted footing)"},
    "H_Lambda": {"value": 1.806234009981721e-18, "unit": "1/s", "formula": "c sqrt(Lambda/3)",
                 "source": "BRIEF constants"},
    "a0_over_cH_Lambda": {"value": 0.17274707473566775, "formula": "a0/(c H_Lambda)",
                          "source": "python float; equals 1/Z to machine precision"},
    "a0_over_cH0": {"value": 0.14284743007481446, "formula": "a0/(c H0), H0=67.4 km/s/Mpc",
                    "source": "python float; NOT equal to 1/Z (H0 != H_Lambda)"},
    "ordering_witness_gN_1_a0_1": {"g_quad": 1.4142135623730951, "g_canon": 1.618033988749895,
                                   "gap": 0.20382042637679976, "source": "python float"},
    "deep_limit_rate_canon": {"value": 5.0001249999986896e-05,
                              "note": "g_c/sqrt(a0gN) - 1 at gN/a0 = 1e-8, consistent with sqrt(delta)/2",
                              "source": "python float (rate NOT certified in Lean)"},
    "deep_limit_rate_quad": {"value": 4.999999969612645e-09,
                             "note": "g_q/sqrt(a0gN) - 1 at gN/a0 = 1e-8, consistent with delta/2",
                             "source": "python float (rate NOT certified in Lean)"},
}


def parse_axioms(text):
    out = {}
    for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text):
        name, ax = m.group(1), m.group(2).strip()
        out[name] = [a.strip() for a in ax.split(",")] if ax else []
    return out


def main():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = C.main()
    checks = C.RESULTS

    theorems = []
    for f, names in C.MANIFEST.items():
        ax = parse_axioms(open(os.path.join(HERE, f + ".out")).read())
        for n in names:
            theorems.append({
                "name": n,
                "file": f + ".lean",
                "axioms": ax.get(n, []),
                "axiom_footprint_ok": sorted(ax.get(n, [])) == sorted(C.ALLOWED),
                "certifies": CERTIFIES.get(n, ""),
            })

    doc = {
        "lane": "A8",
        "title": "Lean 4 + Mathlib certificates for the algebraic core of the DS_FINAL_2026_10_21 push",
        "status": "DERIVED",
        "status_note": ("Each theorem is an implication from explicitly listed premises "
                        "(the two defining equations, the two law definitions, positivity). "
                        "The algebra is derived; the physical premises themselves are inputs."),
        "premises": [
            "a0 = kappa * c * sqrt(G * rho) with kappa > 0 (definition; kappa = 1/2 is FITTED per BRIEF)",
            "H^2 = 8*pi*G*rho/3 (flat, Lambda-only Friedmann equation)",
            "canonical law: gN = g^2/(g + a0)  <=>  g = (gN/2)(1 + sqrt(1 + 4 a0/gN))",
            "n = 2 law: g^2 - gN^2 = a0 gN  <=>  g = sqrt(gN^2 + a0 gN)",
            "positivity: c > 0, G > 0, rho > 0, H > 0, gN > 0, a0 > 0 where stated",
        ],
        "toolchain": {
            "lean": "leanprover/lean4:v4.34.0-rc2",
            "mathlib": "leanprover-community/mathlib rev v4.34.0-rc2",
            "project": "/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026",
            "command": "cd <project> && lake env lean <this lane>/<file>.lean",
            "note": "no existing .lean file in the project was modified; the certificates live in the lane directory",
        },
        "theorems": theorems,
        "theorem_count": len(theorems),
        "allowed_axioms": C.ALLOWED,
        "checks": checks,
        "checks_passed": sum(1 for r in checks if r["pass"]),
        "checks_total": len(checks),
        "numbers": NUMBERS,
        "constants_used": [
            {"name": "c", "value": C.C_LIGHT, "unit": "m/s", "source": "BRIEF section 4"},
            {"name": "G", "value": C.G_NEWTON, "unit": "m^3 kg^-1 s^-2", "source": "BRIEF section 4"},
            {"name": "Lambda", "value": C.LAMBDA, "unit": "m^-2", "source": "BRIEF section 4"},
            {"name": "a0_can", "value": C.A0_CAN_QUOTED, "unit": "m/s^2", "source": "BRIEF section 4 (quoted, 3 s.f.)"},
            {"name": "kappa_can", "value": C.KAPPA_CAN, "unit": "-", "source": "BRIEF section 4; FITTED, not derived"},
            {"name": "H0", "value": 2.1843e-18, "unit": "1/s", "source": "BRIEF section 4 (67.4 km/s/Mpc)"},
        ],
        "mutation": {
            "file": "A8_C3_MUTATE.lean",
            "log": "A8_C3_MUTATE.out",
            "mutants": [
                "gCanon_le_gQuad_MUTANT: reversed ordering g_c <= g_q (FALSE)",
                "gCanon_eq_gQuad_MUTANT: the two laws identified g_c = g_q (FALSE)",
            ],
            "result": "compilation fails (exit 1) at both mutants; see MUTATE.md",
            "check_teeth": "a8_lean_checks.py --mutate asserts the false 1/12 identity and K5 FAILs",
        },
        "does_not_certify": [
            "any numerical value of G, H, rho or a0 (the certificates are symbolic identities in pi and in the constants)",
            "any physics premise beyond the stated equations: a0 = kappa c sqrt(G rho), H^2 = 8 pi G rho/3, and the two law definitions",
            "that kappa = 1/2 is derived (it is FITTED; the certificates only propagate it)",
            "that the 'one twelfth of the horizon' is an identity (the strict bracket 1/12 < 1/(2Z) < 1/11 is certified instead)",
            "that a0/(cH0) = 1/Z (that holds with H_Lambda = c sqrt(Lambda/3), not with the measured H0)",
            "that either galactic law is realised by data, or any fit / rotation-curve claim",
            "dynamical (perturbation) stability: C4 is monotonicity of the algebraic map gN -> g",
            "the 'capacity a0 vs a0/2' integral reading (only mu = gN/g and its limits are certified)",
        ],
        "files": sorted(f for f in os.listdir(HERE)
                        if f.startswith("A8_") or f.startswith("a8_") or f in
                        ("report.md", "MUTATE.md", "make_results.py")),
    }
    out = os.path.join(HERE, "a8_results.json")
    with open(out, "w") as fh:
        json.dump(doc, fh, indent=2)
    print(f"wrote {out}: {len(theorems)} theorems, "
          f"{doc['checks_passed']}/{doc['checks_total']} checks passed, "
          f"checks-script exit={code}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
