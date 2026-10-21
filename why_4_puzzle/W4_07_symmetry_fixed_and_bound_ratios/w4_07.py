#!/usr/bin/env python3
"""W4-07 -- ratios fixed by a symmetry or by a consistency bound: can any of them fix the 4?

Criteria: FROZEN_CRITERIA.md (committed alone, a8684c224). Rules: CFG894 KAPPA_CAMPAIGN_RULES.md.
B1 partially massless spin-2 (Higuchi point), B2 conformally coupled scalar in dS, B3 WGC saturation + seesaw,
B4 dS swampland conjecture, B5 TCC, B6 species scale, B7 seesaw as Berezhiani-Khoury superfluid, B8 flat-space positivity.

Light: sympy only, one process, about a second. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios/w4_07.py \
        > why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios/w4_07.out
    W4_07_MUTATE=1 ... > .../w4_07_MUTATE.out
MUTATE: M1 d 4 -> 5 (B1, B2); M2 reduced <-> non-reduced Planck mass (B7); M3 Higuchi coefficient (d-2) -> (d-1) (B1).
kappa = 1/2 is FITTED. Not theory closed.
"""
import json
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("W4_07_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
checks = []


def check(name, detail, ok, kind="K"):
    checks.append({"name": name, "detail": detail, "pass": bool(ok), "kind": kind})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# === COMPUTE BEGIN (I1 scans this block for forbidden inputs) ===
pi = sp.pi
H, G, c, hbar, rho, E, g, q, alpha, N, lam, phi = sp.symbols("H G c hbar rho E g q alpha N lambda phi", positive=True)
d = sp.symbols("d", positive=True, integer=True)
# (M, L, T) exponents for the SI-style items
DIM = {G: (-1, 3, -2), c: (0, 1, -1), hbar: (1, 2, -1), rho: (1, -3, 0), E: (1, 2, -2), H: (0, 0, -1)}


def rho_dS(dd):
    """d-dimensional Friedmann: H^2 = 16 pi G rho / ((d-1)(d-2)), c = 1"""
    return (dd - 1) * (dd - 2) * H ** 2 / (16 * pi * G)


def B1(dd, higuchi_shift=0):
    dd = sp.sympify(dd)
    m2 = (dd - 2 + higuchi_shift) * H ** 2            # partially massless point m^2 = (d-2) H^2
    return sp.simplify(m2 / (G * rho_dS(dd)))


def B2(dd):
    dd = sp.sympify(dd)                                 # exact arithmetic (a Python int here gave a float in run 1)
    xi_c = (dd - 2) / (4 * (dd - 1))                    # conformal coupling
    m2 = xi_c * dd * (dd - 1) * H ** 2                  # R = d(d-1) H^2
    return sp.simplify(m2 / (G * rho_dS(dd)))


def planck_energy(reduced):
    return sp.sqrt(hbar * c ** 5 / ((8 * pi if reduced else 1) * G))


def seesaw_a0(Escale, reduced):
    """a0 = E^2 / E_P  (energy), times c/hbar -> m/s^2"""
    return Escale ** 2 / planck_energy(reduced) * c / hbar


def kappa2_SI(a0, rho_mass):
    return sp.simplify(a0 ** 2 / (c ** 2 * G * rho_mass))


def B3(reduced=True):                                   # WGC saturated: m c^2 = sqrt2 g q E_P, seesaw
    return kappa2_SI(seesaw_a0(sp.sqrt(2) * g * q * planck_energy(reduced), reduced), rho)


def B6(reduced=True):                                   # species scale E_P/sqrt(N), seesaw
    return kappa2_SI(seesaw_a0(planck_energy(reduced) / sp.sqrt(N), reduced), rho)


def B7(reduced):                                        # BK: a0 = alpha^3 E^2/E_P with E^4 = eps (hbar c)^3
    a0 = alpha ** 3 * seesaw_a0(E, reduced)
    rho_mass = E ** 4 / (hbar * c) ** 3 / c ** 2
    return kappa2_SI(a0, rho_mass)


def B8():
    """flat-space vertices from L = (dphi)^2/2 - lam phi^4 - eps: no n >= 1 vertex depends on eps"""
    eps = sp.symbols("epsilon")
    V = lam * phi ** 4 + eps
    return all(sp.diff(sp.diff(V, phi, k).subs(phi, 0), eps) == 0 for k in range(1, 7))


def pi_weight(expr):
    P = sp.Symbol("P", positive=True)
    num, den = sp.fraction(sp.together(sp.powsimp(sp.expand_power_base(expr.subs(pi, P), force=True), force=True)))
    return sp.degree(num, P) - sp.degree(den, P)


def hbar_power(expr):
    HB = sp.Symbol("HB", positive=True)
    e = sp.powsimp(sp.expand_power_base(expr.subs(hbar, HB), force=True), force=True)
    return sp.Rational(sp.simplify(HB * sp.diff(sp.log(e), HB)))


def dimensionless(expr):
    LM, LL, LT = sp.symbols("lM lL lT", positive=True)
    sub = {s: s * LM ** DIM[s][0] * LL ** DIM[s][1] * LT ** DIM[s][2] for s in expr.free_symbols if s in DIM}
    return sp.simplify(sp.powsimp(sp.expand_power_base(expr.subs(sub, simultaneous=True) / expr, force=True),
                                  force=True)) == 1
# === COMPUTE END ===


WD = (0.227, 0.607)    # CFG493 2-sigma window (grading only)
HAND = {"B1": 16 * pi / 3, "B2": 16 * pi / 3, "B7_reduced": 8 * pi * alpha ** 6, "B7_nonreduced": alpha ** 6}


def main():
    print("W4-07  symmetry-fixed and bound-saturating ratios vs the 4" + ("  [MUTATE]" if MUTATE else ""))
    print("kappa^2 = a0^2/(c^2 G rho_DE); kappa = 1/2 FITTED (CFG493 0.417 +- 0.095). Not theory closed.\n")
    src = open(os.path.abspath(__file__)).read()
    block = src.split("# === COMPUTE BEGIN")[1].split("# === COMPUTE END")[0]
    forbidden = [r"9\.36", r"1\.13\d*e-10", r"1\.2e-10", r"0\.417", r"0\.45\b", r"0\.465", r"0\.53\b", r"0\.55",
                 r"5\.78", r"0\.1727", r"32\s*\*\s*pi\s*/\s*3", r"0\.685"]
    hits = [x for x in forbidden if re.search(x, block)]
    check("I1 forbidden inputs", f"tokens in the compute block: {hits or 'none'}", not hits, "B")

    def compute(D, hshift, swap):
        return {"B1": B1(D, hshift), "B2": B2(D), "B1_general_d": B1(d), "B2_general_d": B2(d),
                "B3": B3(True), "B6": B6(True), "B7_reduced": B7(not swap), "B7_nonreduced": B7(swap)}
    VARIANTS = {"M1 d=5": (5, 0, False), "M2 Planck swap": (4, 0, True), "M3 Higuchi (d-1)": (4, 1, False)}
    D, hshift, swap = VARIANTS["M1 d=5"] if MUTATE else (4, 0, False)
    k = compute(D, hshift, swap)
    rows = []
    print(f"readings (d = {D}{'; MUTATE table = variant M1' if MUTATE else ''})")
    for key in ("B1", "B2", "B1_general_d", "B2_general_d", "B3", "B6", "B7_reduced", "B7_nonreduced"):
        e = k[key]
        fs = sorted(str(s) for s in e.free_symbols)
        hp = hbar_power(e) if hbar in e.free_symbols else 0
        pw = pi_weight(e)
        if key.endswith("general_d"):
            cls = "d-dependent (S3)"
            kap = None
        elif hp != 0:
            cls = "HBAR / TRADE"
            kap = None
        elif fs:
            cls = "TRADE"
            kap = None
        else:
            kap = float(sp.sqrt(e))
            cls = "EXACT" if e == sp.Rational(1, 4) else ("CONSISTENT" if WD[0] <= kap <= WD[1] else "MISS")
        alg = bool(sp.simplify(e / pi).is_algebraic) if not fs else None
        rows.append({"id": key, "k2": str(e), "kappa": kap, "pi_weight": int(pw) if not key.endswith("general_d") else None,
                     "hbar_power": str(hp), "free": fs, "k2_over_pi_algebraic": alg, "class": cls})
        ks = f"kappa {kap:.4f}" if kap else "kappa -"
        print(f"  {key:15s} k2 = {str(e):38s} hbar^{str(hp):5s} free {fs or '-'}  {ks}  -> {cls}")
    print("  B4 dS swampland |V'|/V >= c_S/M_P : an inequality on the quintessence slope, no a0 -> BOUND (hbar via M_P)")
    print("  B5 trans-Planckian censorship      : inequalities on Lambda and on inflation, no a0 -> BOUND")
    b8 = B8()
    print(f"  B8 flat-space positivity           : n-point vertices of L = (dphi)^2/2 - lam phi^4 - eps independent of eps: "
          f"{b8} -> CLOSURE (eps enters only through curvature, i.e. H-type)")

    r = {x["id"]: x for x in rows}
    # K1 (dimension test): B1 = B2 at d = 4, differ at d = 5
    b14, b24, b15, b25 = B1(4), B2(4), B1(5), B2(5)
    check("K1 B1 vs B2", f"d = 4: {b14} vs {b24}; d = 5: {b15} vs {b25}",
          sp.simplify(b14 - b24) == 0 and sp.simplify(b15 - b25) != 0, "B")
    # K2: B7 hbar cancels (both conventions)
    hb7 = [hbar_power(B7(True)) if hbar in B7(True).free_symbols else 0,
           hbar_power(B7(False)) if hbar in B7(False).free_symbols else 0]
    check("K2 B7 hbar cancels", f"hbar power of kappa^2 (reduced, non-reduced): {hb7}", hb7 == [0, 0], "B")
    # K3 hand values: normal run checks the frozen values; MUTATE checks each variant separately (they must FAIL)
    if not MUTATE:
        mism = [key for key, hv in HAND.items() if sp.simplify(k[key] - hv) != 0]
        check("K3 hand values (normal-run)", f"B1 16pi/3, B2 16pi/3, B7 8pi alpha^6 / alpha^6; mismatches {mism or 'none'}",
              not mism)
    else:
        affected = {"M1 d=5": ["B1", "B2"], "M2 Planck swap": ["B7_reduced", "B7_nonreduced"], "M3 Higuchi (d-1)": ["B1"]}
        for vname, args in VARIANTS.items():
            kv = compute(*args)
            mism = [key for key in affected[vname] if sp.simplify(kv[key] - HAND[key]) != 0]
            print(f"  {vname}: " + ", ".join(f"{key} {kv[key]}" for key in affected[vname]))
            check(f"K3 hand values under {vname}", f"normal values must FAIL for {affected[vname]}: mismatches {mism}",
                  len(mism) == 0)
    # I3, I7, I8
    bad3 = [key for key in ("B3", "B6", "B7_reduced", "B7_nonreduced") if not dimensionless(k[key])]
    check("I3 dimensions (SI items)", f"failures {bad3 or 'none'}", not bad3, "B")
    hb = {x["id"]: x["hbar_power"] for x in rows if x["hbar_power"] != "0"}
    check("I7 hbar", f"hbar-bearing: {hb} (declared B3, B6; B7 cancels)", set(hb) == {"B3", "B6"}, "B")
    sym = [r["B1"], r["B2"]]
    check("I8 pi x algebraic", f"B1 {sym[0]['k2_over_pi_algebraic']}, B2 {sym[1]['k2_over_pi_algebraic']}; neither 1/4",
          all(s["k2_over_pi_algebraic"] and s["class"] != "EXACT" for s in sym), "B")
    print(f"\n  general d: B1 kappa^2 = {k['B1_general_d']}, B2 kappa^2 = {k['B2_general_d']}")
    print("  B7: kappa = 1/2 needs alpha = 2^(-1/3) = 0.794 (non-reduced M_Pl) or (32 pi)^(-1/6) = 0.457 (reduced)")

    exact = [x for x in rows if x["class"] == "EXACT"]
    lane = "CANDIDATE" if exact else "RIGID BUT PI-ODD"
    print(f"\nLANE VERDICT: {lane}")
    print("  The partially massless point and the conformal scalar fix a mass to Lambda by a symmetry, with no free coupling,"
          " and give kappa^2 = 16pi/3 (kappa 4.09): pi x algebraic, about ten times the measured value. The consistency"
          " bounds are inequalities or carry hbar; the microscopic seesaw cancels hbar but leaves its coupling alpha free"
          " and its pi set by the Planck-mass convention.")
    n_pass = sum(x["pass"] for x in checks)
    print(f"\nchecks: {n_pass}/{len(checks)} pass")
    json.dump({"mutate": MUTATE, "readings": rows, "B8_eps_free": b8, "lane_verdict": lane, "checks": checks},
              open(os.path.join(HERE, f"w4_07_results{SUF}.json"), "w"), indent=1, default=str)
    if MUTATE:
        bite = all(not x["pass"] for x in checks if x["name"].startswith("K3 hand values under"))
        book = all(x["pass"] for x in checks if x["kind"] == "B")
        print(f"MUTATE: every variant's K3 bites {bite}; bookkeeping passes {book}")
        sys.exit(1 if bite and book else 2)
    sys.exit(0 if n_pass == len(checks) else 1)


if __name__ == "__main__":
    main()
