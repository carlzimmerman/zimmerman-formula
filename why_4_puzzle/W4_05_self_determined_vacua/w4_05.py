#!/usr/bin/env python3
"""W4-05 -- theories that fix their own vacuum: can any of them fix the 4 in G rho_DE = 4 a0^2/c^2?

Criteria: FROZEN_CRITERIA.md (committed alone, af2a69b13). Rules: CFG894 KAPPA_CAMPAIGN_RULES.md.
Families: V1 EiBI, V2 f(R) = R - mu^4/R, V3 Brans-Dicke, V4 Maggiore RR, V5 Deser-Woodard, V6 running vacuum, V7 TeVeS.
Self-determined-vacuum dichotomy: Lambda_eff = A_L/l^2 and a = A_a c^2/l with algebraic A's give kappa^2 = 8 pi A_a^2/A_L.

Light: sympy only, one process, about a second. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_05_self_determined_vacua/w4_05.py \
        > why_4_puzzle/W4_05_self_determined_vacua/w4_05.out
    W4_05_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_05_self_determined_vacua/w4_05.py \
        > why_4_puzzle/W4_05_self_determined_vacua/w4_05_MUTATE.out
MUTATE: M1 8 pi G -> 4 pi G in rho_DE = Lambda/(8 pi G); M2 f(R) mu^4/R -> mu^6/R^2; M3 EiBI lambda 0 -> 1/2.

kappa = 1/2 is FITTED (CFG493: kappa_Lambda 0.417 +- 0.095). Not theory closed.
"""
import json
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("W4_05_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
checks = []


def check(name, detail, ok, kind="K"):
    checks.append({"name": name, "detail": detail, "pass": bool(ok), "kind": kind})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# === COMPUTE BEGIN (I1 scans this block for forbidden inputs) ===
pi = sp.pi
G, ell, mu, Lam, a_free, lamE, k_T, l_T, rho0, nu, H, m = sp.symbols(
    "G ell mu Lambda a lambda_E k_T ell_T rho_0 nu H m", positive=True)
R, kE, eps = sp.symbols("R kappa_E epsilon")


def rho_of(Lambda_eff, einst):
    return Lambda_eff / (einst * G)


def kappa2(a, rho):
    return sp.simplify(sp.nsimplify(a ** 2 / (G * rho)))


def eibi_leading_order():
    """sqrt|det(g + kE R)| = sqrt|g| sqrt(det(1 + kE M)), M = g^-1 R; leading order 1 + kE tr(M)/2"""
    ms = sp.symbols("m0:4")
    detf = sp.prod([1 + kE * mi for mi in ms])
    ser = sp.series(sp.sqrt(detf), kE, 0, 2).removeO()
    ok = sp.simplify(ser - (1 + kE * sum(ms) / 2)) == 0
    lam_s, Rs = sp.symbols("lambda_s R_s")
    # L/sqrt|g| = (1/kE)[1 + kE R/2 - lam] = R/2 + (1 - lam)/kE  ==  (1/2)(R - 2 Lambda)
    lagr = sp.expand((1 / kE) * (1 + kE * Rs / 2 - lam_s))
    Lam_eff = sp.solve(sp.Eq(lagr, sp.Rational(1, 2) * (Rs - 2 * sp.Symbol("L"))), sp.Symbol("L"))[0]
    return ok, sp.simplify(Lam_eff), sp.simplify(Lam_eff.subs(lam_s, 1))


def fR_vacuum(power):
    """vacuum trace equation R f' - 2 f = 0 for f = R - mu^(2(power+1))/R^power"""
    f = R - mu ** (2 * (power + 1)) / R ** power
    sols = [s for s in sp.solve(sp.Eq(R * sp.diff(f, R) - 2 * f, 0), R) if s.is_positive]
    return sols


def compute(einst, eibi_lambda, fR_power):
    rd = []

    def add(fam, rid, desc, k2, selfdet=False, cls_hint=None):
        rd.append({"family": fam, "id": rid, "desc": desc, "k2": k2, "selfdet": selfdet, "hint": cls_hint})

    # V1 EiBI: Lambda_eff = (lambda - 1)/kE; V1a lambda fixed (0, or 1/2 under M3), kE = -ell^2 (de Sitter); a = 1/sqrt|kE|
    LamA = (sp.Rational(eibi_lambda) - 1) / (-ell ** 2)
    add("V1", "V1a", f"EiBI, lambda = {eibi_lambda}, kappa_E < 0: Lambda_eff = {sp.simplify(LamA)}; a = 1/ell",
        kappa2(1 / ell, rho_of(LamA, einst)), True)
    add("V1", "V1b", "EiBI, lambda free: Lambda_eff free; a = 1/ell", kappa2(1 / ell, rho_of(Lam, einst)))
    # V2 f(R): de Sitter R = 4 Lambda
    Rv = fR_vacuum(fR_power)[0]
    add("V2", "V2", f"f(R) = R - mu^{2 * (fR_power + 1)}/R^{fR_power}: vacuum R = {Rv}; a = mu",
        kappa2(mu, rho_of(Rv / 4, einst)), True)
    # V3 Brans-Dicke: Lambda free, no intrinsic acceleration
    add("V3", "V3", "Brans-Dicke / scalar-tensor: Lambda free; a free", kappa2(a_free, rho_of(Lam, einst)))
    # V5 Deser-Woodard: a0 an explicit parameter, Lambda free
    add("V5", "V5", "Deser-Woodard nonlocal MOND: a0 a parameter; Lambda free", kappa2(a_free, rho_of(Lam, einst)))
    # V6 running vacuum: rho = rho0 + 3 nu H^2/(einst G); reading a = H (cH, H-type)
    add("V6", "V6", "running vacuum rho0 + 3 nu H^2/(8 pi G); a = cH", kappa2(H, rho0 + 3 * nu * H ** 2 / (einst * G)))
    # V7 TeVeS: a0 = sqrt(3 k)/(4 pi ell_T) (c = 1); Lambda free
    add("V7", "V7", "TeVeS a0 = sqrt(3k) c^2/(4 pi ell); Lambda free",
        kappa2(sp.sqrt(3 * k_T) / (4 * pi * l_T), rho_of(Lam, einst)))
    return rd


def pi_weight(expr):
    P = sp.Symbol("P", positive=True)
    num, den = sp.fraction(sp.together(sp.powsimp(sp.expand_power_base(expr.subs(pi, P), force=True), force=True)))
    return sp.degree(num, P) - sp.degree(den, P)
# === COMPUTE END ===


WD = (0.227, 0.607)          # CFG493 2-sigma window on rho_DE (grading only)
OMEGA_L = 0.685              # report-only conversion to rho_crit
HAND = {"V1a": 8 * pi, "V2": 32 * pi / sp.sqrt(3)}
# MUTATE variants, evaluated separately so they cannot cancel (M1 and M3 together leave EiBI at 8 pi):
MUT = {"M1": {"args": (4 * pi, 0, 1), "expect": {"V1a": 4 * pi, "V2": 16 * pi / sp.sqrt(3)}},
       "M2": {"args": (8 * pi, 0, 2), "expect": {"V2": 32 * pi / 4 ** sp.Rational(1, 3)}},
       "M3": {"args": (8 * pi, sp.Rational(1, 2), 1), "expect": {"V1a": 16 * pi}}}
# W4-01 self-accelerating curvature-scale readings, re-tabulated (not recomputed as attempts)
W401 = {"DGP crossover (W4-01 F1-S-A1)": 8 * pi / 3, "dRGT Compton (W4-01 F3-C1, algebraic X)": "8 pi/X",
        "f(T) scale (W4-01 F6-F1, rational n)": "16 pi (2n-1)^(1/(n-1))"}


def main():
    print("W4-05  self-determined vacua vs the 4 in G rho_DE = 4 a0^2/c^2" + ("  [MUTATE]" if MUTATE else ""))
    print("kappa^2 = a^2/(G rho_DE), rho_DE = Lambda_eff/(8 pi G), c = 1; footing rho_DE; rho_crit report only.")
    print("kappa = 1/2 FITTED (CFG493 0.417 +- 0.095). Not theory closed.\n")

    src = open(os.path.abspath(__file__)).read()
    block = src.split("# === COMPUTE BEGIN")[1].split("# === COMPUTE END")[0]
    forbidden = [r"9\.36", r"1\.13\d*e-10", r"1\.2e-10", r"0\.417", r"0\.45\b", r"0\.465", r"0\.53\b", r"0\.55",
                 r"5\.78", r"0\.1727", r"32\s*\*\s*pi\s*/\s*3", r"0\.685"]
    hits = [x for x in forbidden if re.search(x, block)]
    check("I1 forbidden inputs", f"tokens in the compute block: {hits or 'none'}", not hits, "B")

    ok1, LamE, Lam1 = eibi_leading_order()
    check("K1 EiBI vacuum", f"sqrt det(1 + kE M) = 1 + kE tr M/2 + O(kE^2): {ok1}; Lambda_eff = {LamE}; at lambda = 1: {Lam1}",
          ok1 and sp.simplify(LamE - (sp.Symbol('lambda_s') - 1) / kE) == 0 and Lam1 == 0, "B")
    L0 = sp.symbols("Lambda_0", positive=True)
    ctrl = sp.solve(sp.Eq(R * sp.diff(R - 2 * L0, R) - 2 * (R - 2 * L0), 0), R)
    r1 = fR_vacuum(1)
    check("K2 f(R) vacuum", f"R f' - 2f = 0 for f = R - mu^4/R gives R = {r1}; control f = R - 2 Lambda0 gives R = {ctrl}",
          r1 == [sp.sqrt(3) * mu ** 2] and ctrl == [4 * L0], "B")

    einst = 4 * pi if MUTATE else 8 * pi
    rd = compute(*MUT["M1"]["args"]) if MUTATE else compute(8 * pi, 0, 1)     # MUTATE table = M1 variant
    rows = []
    print("\nreadings")
    for x in rd:
        k2 = x["k2"]
        fs = sorted(str(s) for s in k2.free_symbols)
        pw = pi_weight(k2)
        if fs:
            cls = "TRADE"
            kap = None
        else:
            kap = float(sp.sqrt(k2))
            cls = "EXACT" if k2 == sp.Rational(1, 4) else ("CONSISTENT" if WD[0] <= kap <= WD[1] else "MISS")
        alg = bool(sp.simplify(k2 / pi).is_algebraic) if not fs else None
        rows.append({"id": x["id"], "family": x["family"], "desc": x["desc"], "k2": str(k2), "kappa": kap,
                     "kappa_crit_report": kap * OMEGA_L ** 0.5 if kap else None, "pi_weight": int(pw), "free": fs,
                     "self_determined": x["selfdet"], "k2_over_pi_algebraic": alg, "class": cls})
        ks = f"kappa {kap:.4f} (crit report {kap * OMEGA_L ** 0.5:.3f})" if kap else "kappa -"
        print(f"  {x['id']:4s} k2 = {str(k2):34s} pi^{int(pw):<2d} free {fs or '-'}  {ks}  -> {cls}")
        print(f"       {x['desc']}")
    print("  V4   Maggiore RR: the m <-> rho_DE relation is fixed only through the whole expansion history (zero-IC"
          " auxiliary fields) and needs the measured matter history upstream, which is forbidden; rho_DE,RR(z) drifts"
          " while m is constant (not tracking) -> CONDITION, no number")

    k_ = {r["id"]: r for r in rows}
    if not MUTATE:
        mism = [rid for rid, hv in HAND.items() if sp.simplify(sp.sympify(k_[rid]["k2"]) - hv) != 0]
        check("K3 hand values (normal-run)", f"V1a 8 pi, V2 32 pi/sqrt3; mismatches: {mism or 'none'}", not mism)
    else:
        for mname, spec in MUT.items():
            vk = {x["id"]: x["k2"] for x in compute(*spec["args"])}
            mism = [rid for rid, hv in HAND.items() if rid in spec["expect"] and sp.simplify(vk[rid] - hv) != 0]
            met = all(sp.simplify(vk[rid] - ev) == 0 for rid, ev in spec["expect"].items())
            print(f"  {mname}: " + ", ".join(f"{rid} {vk[rid]}" for rid in spec["expect"]) + f"; frozen MUTATE values met {met}")
            check(f"K3 hand values under {mname}", f"normal-run values must FAIL for {list(spec['expect'])}: "
                  f"mismatches {mism}", len(mism) == 0)
    selfdet = [r for r in rows if r["self_determined"]]
    check("I8 pi x algebraic", "self-determined kappa^2/pi algebraic and kappa^2 != 1/4: "
          + ", ".join(f"{r['id']} {r['k2_over_pi_algebraic']}" for r in selfdet),
          all(r["k2_over_pi_algebraic"] and r["class"] != "EXACT" for r in selfdet), "B")
    LS, MS = sp.symbols("lambda_L lambda_M", positive=True)
    dims = {G: (1, -1), ell: (1, 0), mu: (-1, 0), Lam: (-2, 0), a_free: (-1, 0), k_T: (0, 0), l_T: (1, 0),
            rho0: (-3, 1), nu: (0, 0), H: (-1, 0)}
    bad3 = []
    for x in rd:
        e = x["k2"]
        sub = {s_: s_ * LS ** dims[s_][0] * MS ** dims[s_][1] for s_ in e.free_symbols}
        if sp.simplify(sp.powsimp(e.subs(sub, simultaneous=True) / e, force=True)) != 1:
            bad3.append(x["id"])
    check("I3 dimensions", f"kappa^2 invariant under (L, M) rescaling (c = 1); failures: {bad3 or 'none'}", not bad3, "B")
    kap_syms = [x["id"] for x in rd if any(str(s_).startswith("kappa") and s_ != kE for s_ in x["k2"].free_symbols)]
    check("I4 rename", f"no kappa^2 contains a kappa symbol (the law's kappa is never read): offenders {kap_syms or 'none'}",
          not kap_syms, "B")

    print("\nself-determined-vacuum dichotomy count (K4)")
    count = []
    for r in selfdet:
        count.append((r["id"], r["k2"], r["kappa"]))
        print(f"  {r['id']}: kappa^2 = {r['k2']} = pi x algebraic, kappa {r['kappa']:.3f}")
    for name, v in W401.items():
        val = f"{float(sp.sqrt(v)):.3f}" if not isinstance(v, str) else "free parameter (TRADE)"
        print(f"  {name}: kappa^2 = {v}, kappa {val}")
    holds = all(r["k2_over_pi_algebraic"] and r["class"] != "EXACT" for r in selfdet)
    others = all(r["class"] == "TRADE" for r in rows if not r["self_determined"])
    check("K4 dichotomy", f"every self-determined reading is pi x algebraic (none 1/4): {holds}; every other family "
          f"TRADE/CONDITION: {others}", holds and others, "B")
    lane = "DICHOTOMY HOLDS" if holds and others else "DICHOTOMY BROKEN"
    print(f"\nLANE VERDICT: {lane}")
    print("  The theories that fix their own vacuum give kappa^2 = 8 pi x (algebraic), so never 1/2, and of size sqrt(8 pi):"
          " EiBI 5.01, f(R) 7.62, DGP 2.89. The measured 0.42 sits about ten times below that natural size. Every other"
          " family leaves the vacuum or a0 free.")
    n_pass = sum(c["pass"] for c in checks)
    print(f"\nchecks: {n_pass}/{len(checks)} pass")
    out = {"mutate": MUTATE, "einst": str(einst), "readings": rows, "lane_verdict": lane, "checks": checks,
           "W4_01_retabulated": {k: str(v) for k, v in W401.items()}}
    with open(os.path.join(HERE, f"w4_05_results{SUF}.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    if MUTATE:
        bit = all((not c["pass"]) for c in checks if c["name"].startswith("K3 hand values under"))
        book = all(c["pass"] for c in checks if c["kind"] == "B")
        print(f"MUTATE: K3 bites {bit}; bookkeeping (I1, K1, K2, I8, I3, I4, K4) passes {book}")
        sys.exit(1 if (bit and book) else 2)
    sys.exit(0 if n_pass == len(checks) else 1)


if __name__ == "__main__":
    main()
