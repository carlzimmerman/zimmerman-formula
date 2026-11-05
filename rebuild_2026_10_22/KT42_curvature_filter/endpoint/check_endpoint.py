"""Exact independent checks of the KT42 constant-quadratic endpoint implication.

No gravitational solver or old physics module is imported. Only source constants
and saved witnesses are read; the tensor/source, rank-one and virial checks are
independent symbolic constructions. The accompanying proof carries universality.
"""
import argparse
import ast
import json
import math
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
RB = ROOT / "rebuild_2026_10_22"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    checks = []

    def check(name, expression):
        ok = bool(expression)
        checks.append({"name": name, "pass": ok})
        if not ok:
            raise AssertionError(name)

    x = s.symbols("x y z", real=True)
    alpha, beta = s.symbols("alpha beta", real=True)
    c = alpha + beta
    psi = s.Function("psi")(*x)
    H = s.hessian(psi, x)
    lap = sum(H[i, i] for i in range(3))
    lap2 = sum(s.diff(lap, q, 2) for q in x)
    # Derive the full E_H from nine independent tensor entries, then impose the
    # Hessian constraint. This avoids dropping the two off-diagonal occurrences.
    raw = s.Matrix(3, 3, s.symbols("h0:9"))
    energy = alpha * s.trace(raw) ** 2 + beta * sum(v * v for v in raw)
    substitutions = dict(zip(raw, H))
    EH = raw.applyfunc(lambda h: s.diff(energy, h).subs(substitutions))
    source = -s.Rational(1, 2) * sum(
        s.diff(EH[i, j], x[i], x[j]) for i in range(3) for j in range(3)
    )
    check("full tensor Euler source equals -(alpha+beta) Laplacian squared psi",
          s.simplify(source + c * lap2) == 0)
    potential = -c * lap
    check("independent Laplacian of contact potential reproduces source",
          s.simplify(sum(s.diff(potential, q, 2) for q in x) - source) == 0)

    n = s.Matrix(s.symbols("n0:3", real=True))
    t = s.symbols("t", real=True)
    variation = raw + t * n * n.T
    varied_energy = alpha * s.trace(variation) ** 2 + beta * sum(v * v for v in variation)
    rank_one = s.diff(varied_energy, t, 2) / 2
    check("rank-one symbol is c times |n|^4 before unit normalization",
          s.simplify(rank_one - c * (n.dot(n)) ** 2) == 0)

    grad = s.Matrix([s.diff(psi, q) for q in x])
    current = grad * lap - H * grad
    divergence = sum(s.diff(current[i], x[i]) for i in range(3))
    null_density = lap ** 2 - sum(v * v for v in H)
    check("difference of isotropic quadratic invariants is an exact divergence",
          s.simplify(divergence - null_density) == 0)
    check("alpha=-beta is a null bulk source", s.simplify(source.subs(beta, -alpha)) == 0)

    # Independent generic density integration-by-parts identity in three dimensions.
    rho = s.Function("rho")(*x)
    density_current = s.Matrix(x) * rho ** 2 / 2
    divergence_rho = sum(s.diff(density_current[i], x[i]) for i in range(3))
    radial_rho = sum(x[i] * s.diff(rho, x[i]) for i in range(3))
    check("virial integration by parts retains the positive surface term",
          s.simplify(divergence_rho - rho * radial_rho - s.Rational(3, 2) * rho ** 2) == 0)

    # A complete decaying example independently checks all factors by integration.
    r = s.symbols("r", nonnegative=True)
    M, a, G, cc = s.symbols("M a G c", positive=True)
    plummer = 3 * M / (4 * s.pi * a ** 3) * (1 + r ** 2 / a ** 2) ** (-s.Rational(5, 2))
    rho_sq = s.integrate(4 * s.pi * r ** 2 * plummer ** 2, (r, 0, s.oo))
    direct_W = s.integrate(4 * s.pi * r ** 3 * plummer *
                           s.diff(-4 * s.pi * G * cc * plummer, r), (r, 0, s.oo))
    check("Plummer density-square integral exact coefficient",
          s.simplify(rho_sq - 45 * M ** 2 / (1024 * a ** 3)) == 0)
    check("direct Plummer force virial agrees with generic density identity",
          s.simplify(direct_W - 6 * s.pi * G * cc * rho_sq) == 0)
    check("Plummer trace variance coefficient is 45 pi G c M/(512 a^3)",
          s.simplify(direct_W / (3 * M) - 45 * s.pi * G * cc * M / (512 * a ** 3)) == 0)

    # Symbolic vertical profiles: the complete MW source is a positive sum.
    z, h, amp, R, Q, r0, cutoff, slope = s.symbols(
        "z h amp R Q r0 cutoff slope", positive=True)
    disk = amp * s.exp(-z / h)
    gas = amp / s.cosh(z / h) ** 2
    rp = s.sqrt(R ** 2 + (z / Q) ** 2)
    bulge = amp * (1 + rp / r0) ** (-slope) * s.exp(-(rp / cutoff) ** 2)
    check("exponential disk vertical derivative is -rho/h",
          s.simplify(s.diff(disk, z) + disk / h) == 0)
    check("sech-squared gas vertical logarithmic slope",
          s.simplify(s.diff(gas, z) + 2 * gas * s.tanh(z / h) / h) == 0)
    check("bulge vertical logarithmic slope",
          s.simplify(s.diff(bulge, z) / bulge +
                     (slope / (r0 + rp) + 2 * rp / cutoff ** 2) * z / (Q ** 2 * rp)) == 0)

    # Mutations are required to disagree; they do not change the physical model.
    check("reversed source sign mutation is detected", s.simplify(-source + c * lap2) != 0)
    check("omitted mixed entries mutation is detected",
          s.simplify(-sum(s.diff(EH[i, i], x[i], 2) for i in range(3)) / 2 - source) != 0)
    check("virial sign-flip mutation is detected", s.simplify(direct_W + 6 * s.pi * G * cc * rho_sq) != 0)

    force = json.loads((RB / "KT40_mechanism/mw/force_001/results.json").read_text())
    hydro = json.loads((RB / "KT40_mechanism/mw/hydro_002/results.json").read_text())
    localize = json.loads((RB / "KT40_mechanism/efe/localize_001/results.json").read_text())
    check("KT40 source records completed their own checks",
          force["complete"] and force["all_checks_pass"] and localize["all_checks_pass"])

    # Execute only literal constant assignments from the already reviewed source.
    # No old solver module and no fitted data-reading code executes here.
    p4 = RB / "P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py"
    desired = {"R0_MW", "PC2", "PC3", "R_FID", "S0_HI", "S0_H2"}
    namespace = {"math": math}
    extracted = []
    for node in ast.parse(p4.read_text()).body:
        if not isinstance(node, ast.Assign):
            continue
        names = {q.id for target in node.targets for q in ast.walk(target) if isinstance(q, ast.Name)}
        if names and names <= desired:
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(p4), "exec"), namespace)
            extracted.append({"names": sorted(names), "line": node.lineno})
    check("all declared source constants extracted", desired <= set(namespace))
    R0 = namespace["R0_MW"]
    sg = namespace["S0_HI"] * math.exp(-4 / R0 - R0 / 7) + namespace["S0_H2"] * math.exp(-12 / R0 - R0 / 1.5)
    mw = []
    for foot, index in [("canonical", 1368), ("alt", 1287)]:
        row = next(v for v in force["cases"] if v["footing"] == foot and v["refine"] == 6)
        point = next(v for v in row["points"] if v["R_kpc"] == 12 and v["z_kpc"] == .3)
        cell = next(v["cell"] for v in hydro["cases"] if v["footing"] == foot and v["index"] == index)
        stellar_column = cell["sb"] * 1e6 - sg
        check(foot + " prescribed stellar and bulge coefficients positive",
              stellar_column > 0 and cell["mbb"] > 0 and 0 < cell["fk"] < 1 and
              min(cell["ht"], cell["hk"], cell["rd"], cell["rdk"]) > 0)
        # This is a rigorous negative component subtotal; the omitted bulge is
        # also strictly decreasing by the symbolic identity above.
        Rv, zv = 12., .3
        thin = (1-cell["fk"]) * stellar_column * math.exp(R0/cell["rd"]-Rv/cell["rd"]-zv/cell["ht"]) / (2*cell["ht"])
        thick = cell["fk"] * stellar_column * math.exp(R0/cell["rdk"]-Rv/cell["rdk"]-zv/cell["hk"]) / (2*cell["hk"])
        hi = namespace["S0_HI"] * math.exp(-4/Rv-Rv/7) / (.34*math.cosh(zv/.17)**2)
        h2 = namespace["S0_H2"] * math.exp(-12/Rv-Rv/1.5) / (.18*math.cosh(zv/.09)**2)
        partial = -thin/cell["ht"]-thick/cell["hk"]-2*hi*math.tanh(zv/.17)/.17-2*h2*math.tanh(zv/.09)/.09
        check(foot + " actual fixed disk-plus-gas density derivative negative", partial < 0)
        old = point["force_parts"]["total"]
        check(foot + " old full-action vertical derivative negative", old < 0)
        mw.append({"footing": foot, "cell_index": index, "cell": cell,
                   "old_dPhi_dz_km2_s2_kpc": old,
                   "required_delta_dPhi_dz_for_nonnegative_km2_s2_kpc": -old,
                   "stellar_column_R0_Msun_pc2": stellar_column / 1e6,
                   "disk_plus_gas_d_rho_dz_Msun_kpc4": partial,
                   "bulge_derivative": "strictly negative; not included in component subtotal"})
    draco = next(v for v in localize["profiles"] if v["name"] == "Draco" and
                 v["footing"] == "canonical" and v["eta"] == .01 and v["upsilon"] == 2)
    old_W = draco["total_variance_terms"]["total"]
    check("canonical Draco witness has negative total trace virial", old_W < 0)
    result = {"assertion_tested": "Exact symbolic identities plus two fixed MW sign witnesses and one saved Draco threshold; universal family classification rests on DERIVATION.md",
              "all_checks_pass": all(q["pass"] for q in checks), "checks": checks,
              "number_of_checks": len(checks), "randomness": False,
              "symbolic_results": {"delta_N": "alpha+beta", "delta_Phi": "-4*pi*G*(alpha+beta)*rho up to the separately constrained harmonic boundary solution",
                                   "delta_W_surface_free": str(6*s.pi*G*cc*rho_sq),
                                   "plummer_delta_W_over_3M": str(s.simplify(direct_W/(3*M)))},
              "mw": mw, "draco": {"footing": "canonical", "eta": .01, "upsilon": 2,
                  "a_kpc": draco["a_kpc"], "old_W_over_3M_km2_s2": old_W,
                  "minimum_delta_W_over_3M_km2_s2": -old_W},
              "constant_extraction": extracted,
              "non_claims": ["No new gravitational field solve or MW/Cassini/dwarf fit", "No proof for density-dependent coefficients or nonlocal response", "No exact continuum certification of old finite-grid witnesses", "No independent actor review; symbolic and force-integral routes differ within one author"]}
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"checks": len(checks), "all_pass": result["all_checks_pass"], "mw_minimum_changes": [x["required_delta_dPhi_dz_for_nonnegative_km2_s2_kpc"] for x in mw], "Draco_minimum_change": -old_W}))


if __name__ == "__main__":
    main()
