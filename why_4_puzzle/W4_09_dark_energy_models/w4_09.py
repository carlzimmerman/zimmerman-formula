#!/usr/bin/env python3
"""W4-09 -- do the dark-energy models themselves fix the 4? (frozen as W4-08; renumbered, see FROZEN_CRITERIA.md)

Criteria: FROZEN_CRITERIA.md (89d2a43c5; rename erratum 8acbd3280). Rules: CFG894 KAPPA_CAMPAIGN_RULES.md.
E1 holographic (Li), E2 agegraphic, E3 Chaplygin, E4 Cardassian, E5 exponential scaling attractor, E6 LQC bounce density,
E7 causal-set everpresent Lambda, E8 Dirac large numbers, E9 interacting dark energy.
Light: sympy only, one process, about a second. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_09_dark_energy_models/w4_09.py > why_4_puzzle/W4_09_dark_energy_models/w4_09.out
    W4_09_MUTATE=1 ... > .../w4_09_MUTATE.out
MUTATE (separate variants): M1 reduced -> non-reduced Planck mass (E1, E2, E5); M2 causal-set exponent 1/2 -> 1/3 (E7).
kappa = 1/2 is FITTED. Not theory closed.
"""
import json
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("W4_09_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
checks = []


def check(name, detail, ok, kind="K"):
    checks.append({"name": name, "detail": detail, "pass": bool(ok), "kind": kind})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# === COMPUTE BEGIN (I1 scans this block for forbidden inputs) ===
pi = sp.pi
G, H, L, T, cH, n, A, alph, B, nC, lam, wb, gam, als, xi, a_free, hbar, c = sp.symbols(
    "G H L T c_H n A alpha B n_C lambda w_b gamma alpha_s xi a hbar c", positive=True)


def mp2(reduced):
    return 1 / ((8 * pi if reduced else 1) * G)


def compute(reduced=True, cs_exp=sp.Rational(1, 2)):
    k = {}
    k["E1"] = sp.simplify((1 / L) ** 2 / (G * 3 * cH ** 2 * mp2(reduced) / L ** 2))
    k["E2"] = sp.simplify((1 / T) ** 2 / (G * 3 * n ** 2 * mp2(reduced) / T ** 2))
    k["E3"] = sp.simplify(a_free ** 2 / (G * A ** (1 / (1 + alph))))
    k["E4"] = sp.simplify(a_free ** 2 / (G * B))                       # Cardassian: B sets the extra term; no scale
    lam_eff = lam if reduced else lam / sp.sqrt(8 * pi)                 # V0 exp(-lam phi/M): lambda tied to the M_P convention
    Om = 3 * (1 + wb) / lam_eff ** 2
    k["E5"] = sp.simplify(H ** 2 / (G * Om * 3 * H ** 2 / (8 * pi * G)))
    # E7 causal set, SI-style: Lambda = alpha_s l^-2 N^-p, N = V4/l^4, l^2 = hbar G/c^3, V4 = c^4/H^4; rho = Lambda c^2/(8 pi G)
    l2 = hbar * G / c ** 3
    V4 = c ** 4 / H ** 4
    Lam = als / l2 * (V4 / l2 ** 2) ** (-cs_exp)
    rho = Lam * c ** 2 / (8 * pi * G)
    k["E7"] = sp.simplify(sp.powsimp((c * H) ** 2 / (c ** 2 * G * rho), force=True))
    k["E9"] = sp.simplify(a_free ** 2 / (G * xi))                        # placeholder: xi free, no scale (TRADE)
    return k


def lqc_ratio():
    """E6: rho_c = sqrt3/(32 pi^2 gamma^3) rho_Pl, rho_Pl = c^5/(hbar G^2); SI magnitude with gamma = 0.2375"""
    rho_pl = 2.99792458e8 ** 5 / (1.054571817e-34 * 6.67430e-11 ** 2)
    rho_c = (3 ** 0.5) / (32 * 3.141592653589793 ** 2 * 0.2375 ** 3) * rho_pl
    return rho_c, rho_c / 6e-27                                          # 6e-27 kg/m^3: order-of-magnitude placeholder only


def pi_weight(e):
    P = sp.Symbol("P", positive=True)
    num, den = sp.fraction(sp.together(sp.powsimp(sp.expand_power_base(e.subs(pi, P), force=True), force=True)))
    return sp.degree(num, P) - sp.degree(den, P)


def hbar_power(e):
    if hbar not in e.free_symbols:
        return sp.Integer(0)
    HB = sp.Symbol("HB", positive=True)
    ee = sp.powsimp(sp.expand_power_base(e.subs(hbar, HB), force=True), force=True)
    return sp.nsimplify(sp.simplify(HB * sp.diff(sp.log(ee), HB)))
# === COMPUTE END ===


HAND = {"E1": 8 * pi / (3 * cH ** 2), "E2": 8 * pi / (3 * n ** 2), "E5": 8 * pi * lam ** 2 / (9 * (1 + wb)),
        "E7": 8 * pi / als}


def main():
    print("W4-09  dark-energy models vs the 4" + ("  [MUTATE]" if MUTATE else ""))
    print("kappa^2 = a^2/(G rho_DE), c = 1 except E6/E7 (SI). kappa = 1/2 FITTED. Not theory closed.\n")
    src = open(os.path.abspath(__file__)).read()
    block = src.split("# === COMPUTE BEGIN")[1].split("# === COMPUTE END")[0]
    forbidden = [r"9\.36", r"1\.13\d*e-10", r"1\.2e-10", r"0\.417", r"0\.45\b", r"0\.465", r"0\.53\b", r"0\.55",
                 r"5\.78", r"0\.1727", r"32\s*\*\s*pi\s*/\s*3", r"0\.685"]
    hits = [x for x in forbidden if re.search(x, block)]
    check("I1 forbidden inputs", f"tokens in the compute block: {hits or 'none'}", not hits, "B")

    k = compute()
    rows = []
    for key in ("E1", "E2", "E3", "E4", "E5", "E7", "E9"):
        e = k[key]
        fs = sorted(str(s) for s in e.free_symbols)
        hp = hbar_power(e)
        cls = "HBAR" if hp != 0 else ("TRADE" if fs else "DETERMINATE")
        rows.append({"id": key, "k2": str(e), "free": fs, "hbar_power": str(hp), "pi_weight": int(pi_weight(e)),
                     "class": cls})
        print(f"  {key}: kappa^2 = {str(e):34s} pi^{int(pi_weight(e)):<2d} hbar^{str(hp):4s} free {fs or '-'} -> {cls}")
    rc, ratio = lqc_ratio()
    print(f"  E6: LQC bounce density rho_c = {rc:.3e} kg/m^3, {ratio:.1e} x a dark-energy-scale density -> HBAR"
          " (a Planck-scale density, not dark energy)")
    print("  E8: Dirac large numbers: G ~ 1/t is excluded by lunar-ranging bounds on dG/dt (recalled); a0 ~ cH is H-type"
          " -> CLOSURE")

    sat1 = k["E1"].subs(cH, 1)
    sat2 = k["E2"].subs(n, 1)
    check("K1 saturated horizon routes agree", f"E1(c_H = 1) = {sat1}, E2(n = 1) = {sat2}, DGP crossover 8pi/3",
          sp.simplify(sat1 - 8 * pi / 3) == 0 and sp.simplify(sat2 - 8 * pi / 3) == 0, "B")
    hp7 = hbar_power(k["E7"])
    check("K2 causal-set hbar cancels", f"hbar power of E7 kappa^2 = {hp7}", hp7 == 0, "B")
    check("K4 LQC scale", f"rho_c / dark-energy-scale density = {ratio:.1e} > 1e100", ratio > 1e100, "B")
    LM, LL, LT = sp.symbols("lM lL lT", positive=True)
    dim = {G: (-1, 3, -2), c: (0, 1, -1), hbar: (1, 2, -1), H: (0, 0, -1)}
    e7 = k["E7"]
    sub = {s: s * LM ** dim[s][0] * LL ** dim[s][1] * LT ** dim[s][2] for s in e7.free_symbols if s in dim}
    d_ok = sp.simplify(sp.powsimp(sp.expand_power_base(e7.subs(sub, simultaneous=True) / e7, force=True), force=True)) == 1
    check("I3 dimensions (E7, SI)", f"dimensionless {d_ok}", d_ok, "B")

    if not MUTATE:
        mism = [key for key, hv in HAND.items() if sp.simplify(k[key] - hv) != 0]
        check("K3 hand values (normal-run)", f"E1 8pi/(3c_H^2), E2 8pi/(3n^2), E5 8pi lam^2/(9(1+w_b)), E7 8pi/alpha_s; "
              f"mismatches {mism or 'none'}", not mism)
    else:
        variants = {"M1 non-reduced M_P": (dict(reduced=False), ["E1", "E2", "E5"]),
                    "M2 causal-set exponent 1/3": (dict(cs_exp=sp.Rational(1, 3)), ["E7"])}
        for vname, (kw, keys) in variants.items():
            kv = compute(**kw)
            mism = [key for key in keys if sp.simplify(kv[key] - HAND[key]) != 0]
            print(f"  {vname}: " + ", ".join(f"{key} {kv[key]}" for key in keys)
                  + (f"; E7 hbar power {hbar_power(kv['E7'])}" if "E7" in keys else ""))
            check(f"K3 hand values under {vname}", f"normal values must FAIL for {keys}: mismatches {mism}", len(mism) == 0)
            if "E7" in keys:
                check("K2 under M2 (hbar must stop cancelling)", f"hbar power {hbar_power(kv['E7'])}",
                      hbar_power(kv["E7"]) == 0)

    exact = [r for r in rows if r["class"] == "DETERMINATE" and sp.sympify(r["k2"]) == sp.Rational(1, 4)]
    lane = "CANDIDATE" if exact else "NO MODEL FIXES THE 4"
    print(f"\nLANE VERDICT: {lane}")
    print("  Every dark-energy model carries its own free amplitude (c_H, n, A, B, lambda, alpha_s, xi). At the saturated"
          " horizon value the holographic and agegraphic models give 8pi/3 (kappa 2.89), the record's recurring H-type"
          " number. LQC's density is Planck-scale; Dirac's G(t) is excluded.")
    n_pass = sum(x["pass"] for x in checks)
    print(f"\nchecks: {n_pass}/{len(checks)} pass")
    json.dump({"mutate": MUTATE, "readings": rows, "lqc": {"rho_c": rc, "ratio": ratio}, "lane_verdict": lane,
               "checks": checks}, open(os.path.join(HERE, f"w4_09_results{SUF}.json"), "w"), indent=1, default=str)
    if MUTATE:
        bite = all(not x["pass"] for x in checks if x["name"].startswith("K3 hand values under")) and \
            not next(x for x in checks if x["name"].startswith("K2 under M2"))["pass"]
        book = all(x["pass"] for x in checks if x["kind"] == "B")
        print(f"MUTATE: controls bite {bite}; bookkeeping passes {book}")
        sys.exit(1 if bite and book else 2)
    sys.exit(0 if n_pass == len(checks) else 1)


if __name__ == "__main__":
    main()
