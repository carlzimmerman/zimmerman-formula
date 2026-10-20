#!/usr/bin/env python3
"""W4-11 -- the last gravity classes with no CFG894 register row: f(Q), f(R,T), bumblebee, Weyl conformal geometry.

Criteria: FROZEN_CRITERIA.md (committed alone, 6d88f570f). Structure-only classification (free couplings, pi, hbar).
Light: sympy, one process, about a second. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_11_last_gravity_classes/w4_11.py > why_4_puzzle/W4_11_last_gravity_classes/w4_11.out
    W4_11_MUTATE=1 ... > .../w4_11_MUTATE.out     (separate variants M1, M2; exit 1 when they bite)
kappa = 1/2 FITTED. Not theory closed.
"""
import json, os, re, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("W4_11_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
checks = []


def check(name, detail, ok, kind="K"):
    checks.append({"name": name, "detail": detail, "pass": bool(ok), "kind": kind})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# === COMPUTE BEGIN (I1 scans this block for forbidden inputs) ===
pi = sp.pi
G, H, alpha, n, lam, Lam, b, xi, q, hbar, c, a = sp.symbols("G H alpha n lambda Lambda b xi q hbar c a", positive=True)
R_, T_ = sp.symbols("R T_trace")


def Q1(einst_factor=2 * 8 * pi):
    """f(Q) = Q + alpha Q^n mapped to f(T): vacuum (6H^2)^(1-n) = alpha(2n-1); a^2 = alpha^(1/(1-n)); rho = 3H^2/(8piG)
    Friedmann normalisation 12H^2 f_T + f = einst_factor * G * rho (2*8pi in the standard form)."""
    H2 = (alpha * (2 * n - 1)) ** (1 / (1 - n)) / 6
    rho = 6 * H2 / (einst_factor * G)                     # from 6H^2 = einst_factor G rho at the matched point
    return sp.simplify(sp.powsimp(alpha ** (1 / (1 - n)) / (G * rho), force=True))


def Q2_vacuum(Ttrace):
    """f(R,T) = R + 2 lam T: trace equation -R + 2 lam T-terms ... = 8piG T -> with T = 0: R = 4 Lambda for any Lambda"""
    eq = sp.Eq(-R_ + 4 * Lam + 2 * lam * Ttrace, 8 * pi * G * Ttrace)
    return sp.solve(eq, R_)[0]


def Q3():
    rho = sp.Symbol("rho_vac", positive=True)              # bumblebee: vacuum constant independent of b
    return sp.simplify((c ** 2 / b) ** 2 / (c ** 2 * G * rho))


def Q4():
    MP2 = hbar * c / (8 * pi * G)                            # reduced Planck mass^2 (kg^2)
    Lam_w = xi ** 2 * MP2 * G / (hbar * c)                   # Lambda ~ xi^2 M_P^2 in curvature units (schematic, 1/m^2)
    m2 = q ** 2 * MP2 * c ** 2 / hbar ** 2                   # Weyl-vector mass^2 -> (1/m)^2 via (M c/hbar)^2
    rho = Lam_w * c ** 2 / (8 * pi * G)
    return sp.simplify((c ** 2) ** 2 * m2 / (c ** 2 * G * rho))
# === COMPUTE END ===


HAND = {"Q1": 16 * pi * (2 * n - 1) ** (1 / (n - 1))}


def same(a_, b_):
    """symbolic equality with a numeric fallback at n = 1.35, 2, 2.7, 3.5 (n > 1/2, so 2n - 1 > 0); first run lacked it"""
    if sp.simplify(a_ - b_) == 0:
        return True
    return all(abs(complex(sp.N((a_ - b_).subs(n, v)))) < 1e-12 * (1 + abs(complex(sp.N(b_.subs(n, v)))))
               for v in (1.35, 2, 2.7, 3.5))


def main():
    print("W4-11  last gravity classes vs the 4" + ("  [MUTATE]" if MUTATE else ""))
    print("kappa = 1/2 FITTED. Not theory closed.\n")
    block = open(os.path.abspath(__file__)).read().split("# === COMPUTE BEGIN")[1].split("# === COMPUTE END")[0]
    hits = [x for x in (r"9\.36", r"1\.13\d*e-10", r"0\.417", r"0\.45\b", r"0\.465", r"0\.55", r"5\.78", r"0\.685") if re.search(x, block)]
    check("I1 forbidden inputs", f"tokens in the compute block: {hits or 'none'}", not hits, "B")
    k1 = Q1()
    r2 = Q2_vacuum(0)
    k3 = Q3()
    k4 = Q4()
    rows = {"Q1": (k1, "f(Q) via the f(T) background map"), "Q3": (k3, "bumblebee"), "Q4": (k4, "Weyl conformal geometry")}
    for key, (e, d) in rows.items():
        fs = sorted(str(s) for s in e.free_symbols)
        print(f"  {key} {d:34s} kappa^2 = {e}   free {fs or '-'} -> {'TRADE' if fs else 'DETERMINATE'}")
    print(f"  Q2 f(R,T) vacuum (T = 0): R = {r2}  (Lambda free) -> TRADE")
    check("K1 f(Q) = f(T) value", f"Q1 kappa^2 = {k1} vs W4-01 F6 16pi(2n-1)^(1/(n-1))",
          same(k1, HAND["Q1"]) or MUTATE, "B" if MUTATE else "K")
    check("K2 f(R,T) vacuum free", f"R = {r2}: depends on Lambda only", sp.simplify(r2 - 4 * Lam) == 0, "B")
    hb4 = sp.simplify(sp.diff(sp.log(k4), hbar) * hbar) if hbar in k4.free_symbols else 0
    print(f"  Q4 hbar power of kappa^2: {hb4}  (q, xi free)")
    if not MUTATE:
        check("K3 hand values (normal-run)", f"Q1 {k1}", same(k1, HAND["Q1"]))
    else:
        m1 = Q1(einst_factor=2 * 4 * pi)
        check("K3 under M1 (2*8piG -> 2*4piG)", f"Q1 {m1}: normal value must FAIL", same(m1, HAND["Q1"]))
        m2 = Q2_vacuum(sp.Symbol("T_v", negative=True))
        check("K2 under M2 (nonzero vacuum trace)", f"R = {m2}: the 'any Lambda only' form must FAIL",
              sp.simplify(m2 - 4 * Lam) == 0)
    lane = "NO CLASS FIXES THE 4"
    print(f"\nLANE VERDICT: {lane}  (Q1 TRADE in n = f(T); Q2 GR in vacuum, Lambda free; Q3 TRADE; Q4 TRADE in q, xi)")
    n_pass = sum(x["pass"] for x in checks)
    print(f"\nchecks: {n_pass}/{len(checks)} pass")
    json.dump({"mutate": MUTATE, "Q1": str(k1), "Q2_R": str(r2), "Q3": str(k3), "Q4": str(k4), "lane_verdict": lane,
               "checks": checks}, open(os.path.join(HERE, f"w4_11_results{SUF}.json"), "w"), indent=1)
    if MUTATE:
        bite = all(not x["pass"] for x in checks if "under M" in x["name"])
        book = all(x["pass"] for x in checks if x["kind"] == "B")
        print(f"MUTATE: controls bite {bite}; bookkeeping passes {book}")
        sys.exit(1 if bite and book else 2)
    sys.exit(0 if n_pass == len(checks) else 1)


if __name__ == "__main__":
    main()
