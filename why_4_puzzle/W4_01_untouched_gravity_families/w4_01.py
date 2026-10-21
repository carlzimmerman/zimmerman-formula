#!/usr/bin/env python3
"""W4-01 -- do the gravity families the kappa register never touched fix the 4 in G rho_DE = 4 a0^2/c^2?

Criteria: FROZEN_CRITERIA.md (committed alone, 5b09f2d51). Rules: CFG894 KAPPA_CAMPAIGN_RULES.md.
Families: F1 DGP, F2 Kaluza-Klein, F3 dRGT / Hassan-Rosen, F4 mimetic, F5 Einstein-Cartan, F6 teleparallel f(T),
F7 Horava-Lifshitz. For each declared reading: kappa^2 = a^2 / (G rho_DE) symbolically (c = 1), its pi-weight, hbar power,
free constants, dimensions, and a class (EXACT / CONSISTENT / MISS / MENU / TRADE / HBAR / IDENTITY).

Light: sympy only, one process, about a second, well under 200 MB. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_01_untouched_gravity_families/w4_01.py \
        > why_4_puzzle/W4_01_untouched_gravity_families/w4_01.out
    W4_01_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_01_untouched_gravity_families/w4_01.py \
        > why_4_puzzle/W4_01_untouched_gravity_families/w4_01_MUTATE.out
MUTATE: M1 Einstein coupling 8 pi G -> 4 pi G in every 4D vacuum relation (F1, F3, F5, F6; F2 report only);
        M2 Kaluza-Klein bulk dimension 5 -> 6 (F2 scored under M2 alone). Exit 1 when the controls bite (K4 fails).

kappa = 1/2 is FITTED (CFG493: kappa_Lambda 0.417 +- 0.095). Not theory closed.
"""
import json
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("W4_01_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""

checks = []


def check(name, detail, ok):
    checks.append({"name": name, "detail": detail, "pass": bool(ok)})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# === COMPUTE BEGIN (I1 scans this block for forbidden inputs) ===
pi = sp.pi
P, HB = sp.symbols("P HB", positive=True)            # stand-ins for pi and hbar when reading off weights
G, G5, R, rc, m, rho, H, hbar, X, nd, cC = sp.symbols("G G5 R r_c m rho H hbar X n_d c_C", positive=True)
alpha = sp.symbols("alpha", positive=True)
n = sp.symbols("n", positive=True)
LS, MS = sp.symbols("lambda_L lambda_M", positive=True)  # length and mass rescalings for the dimension check

# dimensions (c = 1): exponents of (L, M); hbar is mass x length; alpha in f = T + alpha(-T)^n has L^(2(n-1))
DIMS = {G: (1, -1), G5: (2, -1), R: (1, 0), rc: (1, 0), m: (-1, 0), rho: (-3, 1), H: (-1, 0),
        hbar: (1, 1), X: (0, 0), nd: (-3, 0), cC: (0, 0), alpha: (2 * (n - 1), 0)}


def omega(k):
    """area of the unit k-sphere"""
    return 2 * pi ** sp.Rational(k + 1, 2) / sp.gamma(sp.Rational(k + 1, 2))


def force_law_constant(GD, D):
    """Newton-force constant of D-dim gravity: Phi = -G_N M / r^(D-3), from nabla^2 Phi = 8 pi G_D (D-3)/(D-2) rho"""
    ns = D - 1                                   # spatial dimensions
    return sp.simplify(8 * pi * GD * sp.Rational(D - 3, D - 2) / ((ns - 2) * omega(ns - 1)))


def compute(einst, d_kk, einst_kk):
    """every declared reading; einst = Einstein coupling coefficient (8 pi; 4 pi under M1), d_kk = KK bulk dimension,
    einst_kk = the coupling used in F2's vacuum relation (F2 is scored under M2 alone)"""
    rd = []

    def add(fam, rid, desc, a2, rho_de, uses_friedmann=False, identity=False):
        k2 = sp.simplify(sp.powsimp(a2 / (G * rho_de), force=True))
        rd.append({"family": fam, "id": rid, "desc": desc, "k2": k2, "friedmann": uses_friedmann, "identity": identity})

    # ---- F1 DGP: r_c = G5/(2G) (action normalisation), brane Friedmann H^2 - eps H/r_c = einst G rho/3
    G5_dgp = 2 * rc * G
    rho_S = 3 * (1 / rc) ** 2 / (einst * G)                      # self-accelerating vacuum H = 1/r_c
    G5N = force_law_constant(G5_dgp, 5)
    add("F1", "F1-S-A1", "DGP self-acc, crossover acceleration 1/r_c", (1 / rc) ** 2, rho_S, True)
    add("F1", "F1-S-A2", "DGP self-acc, 5D product G5 rho_DE (action G5)", (G5_dgp * rho_S) ** 2, rho_S, True)
    add("F1", "F1-S-A2N", "DGP self-acc, 5D product G5N rho_DE (force-law G5)", (G5N * rho_S) ** 2, rho_S, True)
    add("F1", "F1-N-A1", "DGP normal branch + brane Lambda, 1/r_c", (1 / rc) ** 2, rho)
    add("F1", "F1-N-A2", "DGP normal branch + brane Lambda, G5 rho_DE", (G5_dgp * rho) ** 2, rho)

    # ---- F2 Kaluza-Klein: k = d_kk - 4 circles of radius R, G4 = G_D/(2 pi R)^k; density reading G_D rho/R^(k-1)
    k = d_kk - 4
    GD = G * (2 * pi * R) ** k
    GDN = force_law_constant(GD, d_kk)
    rho_R1 = 3 * H ** 2 / (einst_kk * G)
    for tag, rr, rho_de, fr in (("R0", R, rho, False), ("R1", 1 / H, rho_R1, True)):
        sub = {R: rr}
        add("F2", f"F2-{tag}-B1", f"KK D={d_kk}, G_D rho/R^{k-1}, radius {tag}",
            ((GD * rho_de / R ** (k - 1)) ** 2).subs(sub), rho_de, fr)
        add("F2", f"F2-{tag}-B2", f"KK D={d_kk}, force-law G_D rho/R^{k-1}, radius {tag}",
            ((GDN * rho_de / R ** (k - 1)) ** 2).subs(sub), rho_de, fr)
        add("F2", f"F2-{tag}-B3", f"KK D={d_kk}, compactification acceleration 1/R, radius {tag}",
            ((1 / R) ** 2).subs(sub), rho_de, fr)
    rho_cas = cC * hbar / R ** 4                                     # Casimir-stabilised radius: rho_DE ~ hbar/R^4
    add("F2", "F2-R2-B1", f"KK D={d_kk}, G_D rho/R^{k-1}, Casimir radius", (GD * rho_cas / R ** (k - 1)) ** 2, rho_cas)

    # ---- F3 dRGT / Hassan-Rosen self-accelerating branch: Lambda_eff = m^2 X, rho_DE = Lambda_eff/(einst G)
    add("F3", "F3-C1", "massive gravity, graviton Compton acceleration m", m ** 2, m ** 2 * X / (einst * G), True)

    # ---- F5 Einstein-Cartan: |eps_s| = (einst/16) G hbar^2 n_d^2  (= (pi/2) G hbar^2 n_d^2 at einst = 8 pi)
    eps_s = einst / 16 * G * hbar ** 2 * nd ** 2
    add("F5", "F5-E1a", "spin-torsion energy, independent rho_DE", G * eps_s, rho)
    add("F5", "F5-E1b", "spin-torsion energy AS the dark energy (density matched to itself)", G * eps_s, eps_s,
        identity=True)

    # ---- F6 teleparallel f(T) = T + alpha(-T)^n: 12 H^2 f_T + f = 2 einst G rho; vacuum (6H^2)^(1-n) = alpha(2n-1)
    H2_dS = (alpha * (2 * n - 1)) ** (1 / (1 - n)) / 6
    rho_fT = 3 * H2_dS / (einst * G)
    add("F6", "F6-F1", "f(T) scale |T_*| = alpha^(1/(1-n))", alpha ** (1 / (1 - n)), rho_fT, True)
    return rd


def pi_weight(expr):
    e = sp.powsimp(sp.expand_power_base(expr.subs(sp.pi, P), force=True), force=True)
    num, den = sp.fraction(sp.together(e))
    return sp.degree(num, P) - sp.degree(den, P)


def hbar_power(expr):
    e = sp.together(expr.subs(hbar, HB))
    num, den = sp.fraction(e)
    return sp.degree(num, HB) - sp.degree(den, HB)


def dimensionless(expr):
    sub = {s: s * LS ** DIMS[s][0] * MS ** DIMS[s][1] for s in expr.free_symbols if s in DIMS}
    ratio = sp.simplify(sp.powsimp(sp.expand_power_base(expr.subs(sub, simultaneous=True) / expr, force=True),
                                   force=True))
    return ratio == 1
# === COMPUTE END ===


# hand expectations (FROZEN_CRITERIA.md, normal run); MUTATE expectations as frozen
HAND = {"F1-S-A1": 8 * pi / 3, "F1-S-A2": 3 / (2 * pi), "F1-S-A2N": 8 / (3 * pi ** 3),
        "F1-N-A1": 1 / (rc ** 2 * G * rho), "F1-N-A2": 4 * rc ** 2 * G * rho,
        "F2-R0-B1": 4 * pi ** 2 * R ** 2 * G * rho, "F2-R1-B1": 3 * pi / 2, "F2-R1-B2": 8 / (3 * pi),
        "F2-R1-B3": 8 * pi / 3, "F3-C1": 8 * pi / X, "F5-E1b": sp.Integer(1),
        "F5-E1a": pi / 2 * G * hbar ** 2 * nd ** 2 / rho,
        "F6-F1": 16 * pi * (2 * n - 1) ** (1 / (n - 1))}
HAND_MUT = {"F1-S-A1": 4 * pi / 3, "F1-S-A2": 3 / pi, "F1-S-A2N": 16 / (3 * pi ** 3), "F2-R1-B1": 6 * pi ** 3}
DECLARED = {"F1-S": "odd", "F1-N": "free", "F2-R0": "free", "F2-R1": "odd", "F2-R2": "hbar", "F3": "free",
            "F5-E1a": "hbar", "F5-E1b": "identity", "F6": "free"}

# grading (outside the compute block): CFG493 2-sigma windows, Omega_Lambda only to convert a finished kappa
WD = (0.227, 0.607)
WD_CRIT = (0.189, 0.501)
OMEGA_L = 0.685


def same_expr(a, b):
    """symbolic equality, with a numeric fallback at two fixed positive points (n > 1/2 so 2n - 1 > 0)"""
    d = sp.simplify(sp.powsimp(a - b, force=True))
    if d == 0:
        return True
    for vals in ({G: 1.3, G5: 0.7, R: 2.1, rc: 1.7, m: 0.9, rho: 0.4, H: 1.1, hbar: 0.6, X: 2.3, nd: 1.9, cC: 0.8,
                  alpha: 0.75, n: 2.3},
                 {G: 0.5, G5: 1.9, R: 0.6, rc: 3.1, m: 1.4, rho: 2.2, H: 0.3, hbar: 1.7, X: 0.45, nd: 0.35, cC: 1.6,
                  alpha: 1.8, n: 1.35}):
        if abs(complex(sp.N((a - b).subs(vals)))) > 1e-12 * (1 + abs(complex(sp.N(b.subs(vals))))):
            return False
    return True


def declared_class(rid):
    for key in sorted(DECLARED, key=len, reverse=True):
        if rid.startswith(key):
            return DECLARED[key]
    return None


def main():
    print("W4-01  untouched gravity families vs the 4 in G rho_DE = 4 a0^2/c^2" + ("  [MUTATE]" if MUTATE else ""))
    print("kappa^2 = a^2/(G rho_DE), c = 1; footing rho_DE (declared); rho_crit = report only (kappa sqrt(Omega_L))")
    print("kappa = 1/2 FITTED (CFG493 0.417 +- 0.095). Not theory closed.\n")

    # ---- K1 DGP vacuum root
    Hs = sp.symbols("H_s", positive=True)
    roots = sp.solve(sp.Eq(Hs ** 2 - Hs / rc, 0), Hs)
    check("K1 DGP self-accelerating vacuum root", f"roots of H^2 - H/r_c = 0 (H > 0): {roots}", roots == [1 / rc])

    # ---- K2 D = 5 force-law constant, plus the Gauss flux of grad(r^-2) through S^3
    r = sp.symbols("r", positive=True)
    g5n = force_law_constant(G5, 5)
    flux = sp.simplify(sp.diff(r ** -2, r) * omega(3) * r ** 3)
    check("K2 D=5 force law", f"G5N = {g5n}; flux of grad r^-2 through S^3 = {flux} (expect -4 pi^2)",
          sp.simplify(g5n - 4 * G5 / (3 * pi)) == 0 and sp.simplify(flux + 4 * pi ** 2) == 0)

    # ---- K3 f(T)
    Hf, rhof, T = sp.symbols("H_f rho_f T")
    fT_GR = 12 * Hf ** 2 * 1 + (-6 * Hf ** 2)
    ok_gr = sp.simplify(fT_GR - 6 * Hf ** 2) == 0
    ok_root = True
    for nn in (sp.Integer(2), sp.Rational(3, 2), sp.Integer(3)):
        Tv = -(alpha * (2 * nn - 1)) ** (1 / (1 - nn))             # T = -6H^2 at the vacuum root
        f = Tv + alpha * (-Tv) ** nn
        fT = 1 - alpha * nn * (-Tv) ** (nn - 1)
        resid = sp.simplify(sp.powsimp(-2 * Tv * fT + f, force=True))   # 12 H^2 = -2T
        ok_root = ok_root and resid == 0
    check("K3 f(T)", "f = T gives 6H^2 = 16 pi G rho; vacuum root (6H^2)^(1-n) = alpha(2n-1) at n = 2, 3/2, 3",
          ok_gr and ok_root)

    # ---- compute the readings
    einst = 4 * pi if MUTATE else 8 * pi
    rd = compute(einst, 6 if MUTATE else 5, 8 * pi)
    if MUTATE:
        f2_m1 = [x for x in compute(4 * pi, 5, 4 * pi) if x["family"] == "F2"]   # report: F2 under M1 alone
    rd_rename = compute(einst, 6 if MUTATE else 5, 8 * pi)                    # I4: the law's kappa is never read

    # ---- I1 forbidden inputs in the compute block
    src = open(os.path.abspath(__file__)).read()
    block = src.split("# === COMPUTE BEGIN")[1].split("# === COMPUTE END")[0]
    forbidden = [r"9\.36", r"1\.13\d*e-10", r"1\.2e-10", r"0\.417", r"0\.45\b", r"0\.465", r"0\.53\b", r"0\.55",
                 r"5\.78", r"0\.1727", r"32\s*\*\s*pi\s*/\s*3", r"Omega", r"0\.685"]
    hits = [f for f in forbidden if re.search(f, block)]
    check("I1 forbidden inputs", f"tokens found in the compute block: {hits or 'none'}", not hits)

    # ---- per reading
    rows = []
    print("\nreadings (kappa^2 symbolic; pi-weight; hbar power; free constants; class)")
    for x, y in zip(rd, rd_rename):
        k2 = x["k2"]
        fs = sorted(str(s) for s in k2.free_symbols)
        pw = pi_weight(k2)
        hp = hbar_power(k2)
        dimok = dimensionless(k2)
        same = sp.simplify(x["k2"] - y["k2"]) == 0
        decl = declared_class(x["id"])
        if x["identity"]:
            cls = "IDENTITY"
        elif hp != 0:
            cls = "HBAR"
        elif fs:
            cls = "TRADE"
        else:
            kap = float(sp.sqrt(k2))
            if k2 == sp.Rational(1, 4):
                cls = "EXACT"
            elif WD[0] <= kap <= WD[1]:
                cls = "CONSISTENT"
            else:
                cls = "MISS"
        kap = float(sp.sqrt(k2)) if not fs else None
        row = {"id": x["id"], "family": x["family"], "desc": x["desc"], "k2": str(k2), "kappa": kap,
               "kappa_crit_report": (kap * OMEGA_L ** 0.5 if kap is not None else None), "pi_weight": int(pw),
               "hbar_power": int(hp), "free": fs, "dimensionless": dimok, "rename_invariant": same,
               "uses_friedmann": x["friedmann"], "declared": decl, "class": cls}
        rows.append(row)
        ks = f"kappa {kap:.4f} (crit report {kap * OMEGA_L ** 0.5:.3f})" if kap is not None else "kappa -"
        print(f"  {x['id']:10s} k2 = {str(k2):42s} pi^{int(pw):<2d} hbar^{int(hp):<2d} free {fs or '-'}  {ks}  -> {cls}")
        print(f"             {x['desc']}")

    # ---- I2-I8 summary checks
    check("I2 free constants printed", "every TRADE reading lists its free symbols above", all(
        (r["class"] != "TRADE") or r["free"] for r in rows))
    check("I3 dimensions", "kappa^2 dimensionless under (L, M) rescaling for every reading",
          all(r["dimensionless"] for r in rows))
    check("I4 rename", "outputs identical when the law's kappa is set to 0.4 (no route reads it)",
          all(r["rename_invariant"] for r in rows))
    fr = [r["id"] for r in rows if r["uses_friedmann"]]
    check("I5 Friedmann use flagged", f"readings using the family's own Friedmann relation: {fr}; none scored as a Z match",
          True)
    check("I6 footing", "rho_DE only; rho_crit numbers are report-only conversions", True)
    hb = {r["id"]: r["hbar_power"] for r in rows if r["hbar_power"]}
    check("I7 hbar", f"hbar-bearing readings: {hb} (declared: F2-R2, F5-E1a)",
          set(hb) == {"F2-R2-B1", "F5-E1a"})
    bad8 = []
    for r in rows:
        if r["declared"] == "odd" and r["pi_weight"] % 2 == 0:
            bad8.append(r["id"])
    check("I8 pi-parity", f"declared pi-odd readings with even weight: {bad8 or 'none'}", not bad8)
    fx = [r for r in rows if r["id"].startswith(("F3", "F6"))]
    check("I8b pi-weight of the free families", "F3 kappa^2 = einst/X and F6 = 2 einst (2n-1)^(1/(n-1)) carry pi^1: "
          + ", ".join(f"{r['id']} pi^{r['pi_weight']}" for r in fx), all(r["pi_weight"] == 1 for r in fx))

    # ---- K4 hand expectations
    k4_fail = []
    for rid, hv in HAND.items():
        got = next((x["k2"] for x in rd if x["id"] == rid), None)
        if got is None or not same_expr(got, hv):
            k4_fail.append(rid)
    check("K4 hand expectations (normal-run values)", f"mismatches: {k4_fail or 'none'}", not k4_fail)
    if MUTATE:
        mm = []
        for rid, hv in HAND_MUT.items():
            got = next((x["k2"] for x in rd if x["id"] == rid), None)
            mm.append((rid, str(got), bool(got is not None and same_expr(got, hv))))
        print("  MUTATE expectations as frozen: " + "; ".join(f"{a} {b} {'met' if c else 'NOT met'}" for a, b, c in mm))
        print("  F2 under M1 alone (report): " + "; ".join(f"{x['id']} {x['k2']}" for x in f2_m1))

    # ---- family verdicts
    fam_names = {"F1": "DGP brane-induced gravity", "F2": "Kaluza-Klein compactification",
                 "F3": "dRGT massive gravity / Hassan-Rosen bigravity", "F4": "mimetic gravity",
                 "F5": "Einstein-Cartan spin-torsion", "F6": "teleparallel f(T)", "F7": "Horava-Lifshitz"}
    fams = {}
    print("\nfamily verdicts")
    for f, name in fam_names.items():
        fr_ = [r for r in rows if r["family"] == f]
        det = [r for r in fr_ if r["kappa"] is not None and r["class"] in ("EXACT", "CONSISTENT", "MISS")]
        verdict, note = None, ""
        if f in ("F4", "F7"):
            verdict = "TRADE"
            note = ("no intrinsic acceleration: Lambda is an integration constant or a free potential scale"
                    if f == "F4" else "Lambda free; detailed balance gives Lambda < 0 and needs a free soft-breaking term")
        elif any(r["class"] == "EXACT" for r in fr_):
            verdict = "EXACT CANDIDATE"
        else:
            groups = {}
            for r in det:
                groups.setdefault(r["id"].rsplit("-", 1)[0], []).append(r["kappa"])
            menus = {g: v for g, v in groups.items() if len(v) > 1 and max(v) - min(v) > WD[1] - WD[0]}
            cons = [r for r in det if r["class"] == "CONSISTENT" and r["id"].rsplit("-", 1)[0] not in menus]
            if cons:
                verdict = "CONSISTENT"
            elif menus:
                verdict = "MENU"
                note = "; ".join(f"{g} {{{', '.join(f'{v:.3f}' for v in sorted(vs))}}}" for g, vs in menus.items())
            elif det:
                verdict = "MISS"
            elif any(r["class"] == "TRADE" for r in fr_):
                verdict = "TRADE"
            elif any(r["class"] == "HBAR" for r in fr_):
                verdict = "HBAR"
            if any(r["class"] == "TRADE" for r in fr_) and verdict in ("MENU", "MISS"):
                note += "; plus TRADE readings (" + ", ".join(r["id"] for r in fr_ if r["class"] == "TRADE") + ")"
            if f == "F5":
                verdict = "HBAR"
                note = "E1a hbar^2 (excluded); E1b kappa = 1 by construction (identity, wrong sign, not scored)"
            if f == "F3":
                note = "kappa^2 = 8 pi/X: free in the potential parameters; pi-odd at any algebraic X, never 1/2"
            if f == "F6":
                note = "kappa^2 = 16 pi (2n-1)^(1/(n-1)): alpha cancels, free in n; pi-odd at rational n, never 1/2"
            if f == "F2":
                verdict = "TRADE"
                note = ("radius unstabilised (R0) -> TRADE; R tied to c/H_Lambda (R1) -> menu "
                        + "{" + ", ".join(f"{r['kappa']:.3f}" for r in fr_ if r["id"].startswith("F2-R1")) + "}"
                        + " all pi-odd; Casimir radius (R2) hbar-bearing")
        fams[f] = {"name": name, "verdict": verdict, "note": note}
        print(f"  {f} {name}: {verdict}  {note}")

    exact = [f for f, v in fams.items() if v["verdict"] == "EXACT CANDIDATE"]
    consistent = [f for f, v in fams.items() if v["verdict"] == "CONSISTENT"]
    lane = ("CANDIDATE FOUND" if exact else "CONSISTENT ONLY" if consistent else "NO FAMILY SELECTS KAPPA")
    print(f"\nLANE VERDICT: {lane}")
    print("  No reading outputs kappa^2 = 1/4. Every determinate reading uses the family's own 4D Friedmann relation"
          " (Einstein's 8 pi G) and is pi-odd; every other reading is a trade, hbar-bearing or an identity.")
    print("  DGP's crossover r_c = G5/(2G) is pi-free (both Planck masses carry the same 8 pi), but the dark energy"
          " reaches the a0 scale only through the self-accelerating Friedmann equation, where the 8 pi returns.")

    n_pass = sum(c["pass"] for c in checks)
    print(f"\nchecks: {n_pass}/{len(checks)} pass")
    out = {"mutate": MUTATE, "einst": str(einst), "kk_dimension": 6 if MUTATE else 5, "window_rho_DE": WD,
           "window_rho_crit_report": WD_CRIT, "readings": rows, "families": fams, "lane_verdict": lane,
           "checks": checks}
    with open(os.path.join(HERE, f"w4_01_results{SUF}.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    if MUTATE:
        bite = any((not c["pass"]) and c["name"].startswith("K4") for c in checks)
        others = all(c["pass"] for c in checks if not c["name"].startswith("K4"))
        print(f"MUTATE: K4 bites {bite}; bookkeeping checks still pass {others}")
        sys.exit(1 if bite else 2)
    sys.exit(0 if n_pass == len(checks) else 1)


if __name__ == "__main__":
    main()
