#!/usr/bin/env python3
"""k1_numeric_audit.py -- lane K: run published claimed formulas for 1/alpha through lane D's bar (alpha_bar_checker.py, imported unmodified).

Run (real):    python3 k1_numeric_audit.py            -> exit 0 iff NO row passes all four bar criteria under P_MDL or P_decl (H1 in its strongest form)
MUTATE:        python3 k1_numeric_audit.py --mutate   -> feeds every row a miss of 1e-11 (precision it does not have); must exit 1 (a spurious clear appears)

Everything is declared in K_PREREGISTRATION.md (+ Amendments 1, 2). T = 137.035999177, delta_CODATA = 1.6e-10.
For each claim: value, miss, sigma, P_MDL (checker default shape count; intmax = max(12, largest integer)), P_forced (N=1), P_decl (declared slot family), fitted reals, scale stated.
Supplementary: s1 (Gilson family scan), s2 (Gilson rounding test at b=137), s3 (Gilson expansion), Atiyah checks (i)-(iii).
"""
import sys, os, math, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
DDIR = os.path.join(HERE, "..", "D_calibration_bar")
sys.path.insert(0, DDIR)
import numpy as np
import mpmath as mp
import bar_lib as B
import alpha_bar_checker as C

mp.mp.dps = 40
MUTATE = "--mutate" in sys.argv
T = mp.mpf("137.035999177")
SIG = 1.6e-10
DUP = C.DUP_E2
RHO = C.RHO_DEFAULT
out_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out_lines.append(s)


def miss_of(v):
    return float(abs(v / T - 1))


def rows_definition():
    pi, e = mp.pi, mp.e
    R = mp.log(2 + mp.sqrt(3))
    A = 4 * pi ** 3 + pi ** 2 + pi
    K = mp.mpf("9.9327912864")
    gil = pi / (29 * mp.cos(pi / 137) * mp.tan(pi / (29 * 137)))
    rows = [
        # id, label, value (mp), mdl_expr (or None), N_decl (or None), fitted, scale_stated, predicted_precision, source_status
        ("K1a", "Eddington 136 = 16+16*15/2", mp.mpf(16 + 16 * 15 // 2), "16+16*15/2", 64, 0, False, 0.0, "FULL TEXT (Kragh)"),
        ("K1b", "Eddington 137 = 136+1", mp.mpf(137), "16+16*15/2+1", 64, 0, False, 0.0, "FULL TEXT (Kragh)"),
        ("K2a", "Gilson pi/(29 cos(pi/137) tan(pi/(29*137)))", gil, "pi/(29*cos(pi/137)*tan(pi/(29*137)))", 40000, 0, False, 0.0, "value FULL TEXT (Dattoli); formula form from SNIPPET"),
        ("K2b1", "108 pi (8/1843)^(1/6)", 108 * pi * (mp.mpf(8) / 1843) ** (mp.mpf(1) / 6), "108*pi*(8/1843)**(1/6)", None, 0, False, 0.0, "FULL TEXT (Anastassov quoting Eagles)"),
        ("K2b2", "4 pi^5/9 + 37/36", 4 * pi ** 5 / 9 + mp.mpf(37) / 36, "4*pi**5/9+37/36", None, 0, False, 0.0, "FULL TEXT (Anastassov quoting Eagles)"),
        ("K2b3", "sqrt(137^2 + pi^2) (also Dattoli's Pythagorean formula)", mp.sqrt(137 ** 2 + pi ** 2), "sqrt(137**2+pi**2)", None, 0, False, 0.0, "FULL TEXT (Anastassov; Dattoli)"),
        ("K5", "Wyler (9/(8pi^4)) (pi^5/(2^4 5!))^(1/4), inverted", 1 / (9 / (8 * pi ** 4) * (pi ** 5 / (2 ** 4 * mp.factorial(5))) ** (mp.mpf(1) / 4)),
         "9/(8*pi**4)*(pi**5/(2**4*factorial(5)))**(1/4)", None, 0, False, 0.0, "FULL TEXT (Jentschura-Nandori Eq.8)"),
        ("K9", "combinatorial hierarchy 137/(1-1/(30*127))", mp.mpf(137) / (1 - mp.mpf(1) / (30 * 127)), "137/(1-1/(30*127))", 3060000, 0, True, 0.0, "FULL TEXT (Noyes; states alpha^-1(m_e))"),
        ("K13", "Rosen 42*41/(4 pi)", mp.mpf(42 * 41) / (4 * pi), "42*41/(4*pi)", 200, 0, False, 0.0, "FULL TEXT of description (Jentschura-Nandori Eq.9)"),
        ("K14", "Sherbon 4 pi^3 + pi^2 + pi", A, "4*pi**3+pi**2+pi", 1728, 0, False, 0.0, "SNIPPET (+ appears in Blandino summary)"),
        ("K11a", "Bleger 19596/143 + 5R/(6370-2R), R=ln(2+sqrt3)", mp.mpf(19596) / 143 + 5 * R / (6370 - 2 * R), "19596/143+5*R/(6370-2*R)", int(20000 * 200 * 10 * 7000 * 5), 0, False, 0.0, "SUMMARY of a Zenodo record"),
        ("K11b", "Blandino A - 1/(24A) - 1/(A^2 pi^2 K), K fitted to CODATA 2022", A - 1 / (24 * A) - 1 / (A ** 2 * pi ** 2 * K), "4*pi**3+pi**2+pi-1/(24*A)-1/(A**2*pi**2*K)", None, 1, False, 0.0, "SUMMARY of a Zenodo record"),
    ]
    return rows


def size_from_shape(expr):
    lg, st = B.mdl_size(expr, intmax=12)
    return lg, st, (2.0 ** lg) * DUP


def evaluate_row(row):
    rid, label, val, mexpr, Ndecl, fitted, scale, pred, status = row
    d = miss_of(val)
    if MUTATE:
        d = 1e-11
    rec = dict(id=rid, label=label, value=mp.nstr(val, 15), miss=d, sigma=d / SIG, fitted=fitted, scale=scale, status=status)
    if mexpr:
        lg, st, Nm = size_from_shape(mexpr)
        rm = B.evaluate(d, Nm, RHO, n_targets=1, predicted_precision=pred, fitted_reals=fitted, scale_stated=scale)
        rec.update(log2_mdl=lg, N_mdl=Nm, P_mdl=rm["p"], mdl_c=rm)
        # harness consistency: for expressions the checker can evaluate, assess(expr=...) must agree
        if rid in ("K5", "K9", "K13", "K14", "K1a", "K1b", "K2b2", "K2b3", "K2b1"):
            try:
                r2 = C.assess(expr=mexpr, delta=d if MUTATE else None, fitted_reals=fitted, scale_stated=scale, verbose=False)
                assert abs(math.log10(max(r2["p"], 1e-300)) - math.log10(max(rm["p"], 1e-300))) < 1e-6 or (r2["p"] > 0.999 and rm["p"] > 0.999), (rid, r2["p"], rm["p"])
                rec["harness_agrees"] = True
            except (KeyError, ValueError) as ex:
                rec["harness_agrees"] = "n/a (%s)" % type(ex).__name__
    rf = B.evaluate(d, 1.0, RHO, n_targets=1, predicted_precision=pred, fitted_reals=fitted, scale_stated=scale)
    rec.update(P_forced=rf["p"], forced_c=rf)
    if Ndecl:
        rd = B.evaluate(d, float(Ndecl), RHO, n_targets=1, predicted_precision=pred, fitted_reals=fitted, scale_stated=scale)
        rec.update(N_decl=Ndecl, P_decl=rd["p"], decl_c=rd)
    return rec


def crit(c):
    return "c1=%s c2=%s c3=%s c4=%s" % tuple("Y" if c[k] else "n" for k in ("c1_lookelsewhere", "c2_precision", "c3_no_fitted_real", "c4_scale_stated"))


def main():
    P("k1_numeric_audit  MUTATE=%s   T=%s  delta_CODATA=%g  rho=%.4f  dup=%.4f" % (MUTATE, mp.nstr(T, 12), SIG, RHO, DUP))
    rows = [evaluate_row(r) for r in rows_definition()]
    P("")
    P("%-5s %-58s %-17s %-10s %-10s %-9s %-9s %-9s" % ("id", "formula", "1/alpha value", "miss", "sigma", "P_MDL", "P_forced", "P_decl"))
    any_clear = []
    for r in rows:
        pm = "%.3g" % r["P_mdl"] if "P_mdl" in r else "n/a"
        pd = "%.3g" % r["P_decl"] if "P_decl" in r else "n/a"
        P("%-5s %-58s %-17s %-10.3g %-10.3g %-9s %-9.3g %-9s" % (r["id"], r["label"][:58], r["value"], r["miss"], r["sigma"], pm, r["P_forced"], pd))
        if "mdl_c" in r:
            P("        MDL: 2^%.1f syntactic x dup -> N=%.3g ; %s ; clears=%s   [harness %s]" % (r["log2_mdl"], r["N_mdl"], crit(r["mdl_c"]), r["mdl_c"]["clears"], r.get("harness_agrees", "")))
        if "decl_c" in r:
            P("        decl: N=%.3g ; %s ; clears=%s" % (r["N_decl"], crit(r["decl_c"]), r["decl_c"]["clears"]))
        fc = r["forced_c"]
        grant = fc["c1_lookelsewhere"] and fc["c2_precision"] and fc["c3_no_fitted_real"]
        P("        forced (N=1): %s ; would pass if all choices forced AND scale granted: %s ; source status: %s" % (crit(fc), grant, r["status"]))
        if ("mdl_c" in r and r["mdl_c"]["clears"]) or ("decl_c" in r and r["decl_c"]["clears"]):
            any_clear.append(r["id"])
    # stated-value-only rows (no formula that can be evaluated here)
    P("")
    P("Stated-value-only rows (no evaluable formula in my hands; miss computed from the printed number):")
    stated = [("K2c", "Anastassov alpha_rho (printed 137.035989392; formula garbled, NOT reconstructed)", mp.mpf("137.035989392"), 0.0),
              ("K3", "Atiyah Zh printed '137.035999...' (9 sig. figs; the true claimed value lies in [137.035999, 137.036000), so the miss is anywhere in 0..6e-9; the row uses the printed truncation, miss 1.3e-9, which does NOT decide c2)", mp.mpf("137.035999"), 0.0),
              ("K11c", "Reinisch model alpha = 7.364e-3 (abstract; author's own stated error ~1%)", 1 / mp.mpf("7.364e-3"), 1e-2)]
    for rid, lab, val, pred in stated:
        d = miss_of(val)
        if MUTATE:
            d = 1e-11
        r = B.evaluate(d, 1.0, RHO, n_targets=1, predicted_precision=pred, fitted_reals=0, scale_stated=False)
        P("%-11s %-100s value=%s miss=%.3g (%.3g sigma) ; N=1 check: %s ; no P_decl (no family declarable)" % (rid, lab[:100], mp.nstr(val, 12), d, d / SIG, crit(r)))
        if MUTATE and rid == "K11c":
            pass
    # Anastassov's printed statement: 'hits the central value' of the value of his day
    P("  info (not a bar row): hierarchy value 137.0359674 vs the era value the source compares with (137.0359895): rel miss %.2e" % float(abs(mp.mpf("137.0359674") / mp.mpf("137.0359895") - 1)))
    P("  note: Anastassov states agreement with 137.0359895(61) (1987 adjustment) and Noyes compares with the same value; against the 2022 target the misses are as printed above.")

    # ---------------- supplementary s1: Gilson family scan
    P("")
    P("== s1: Gilson family pi/(a cos(pi/b) tan(pi/(a b))), a,b in 1..200 (N=40000): empirical hit counts vs local density ==")
    a = np.arange(1, 201, dtype=float)[:, None]
    b = np.arange(1, 201, dtype=float)[None, :]
    with np.errstate(all="ignore"):
        beta = np.pi / b
        G = np.pi / (a * np.cos(beta) * np.tan(beta / a))
    Tf = float(T)
    rel = np.abs(G / Tf - 1)
    rel = np.where(np.isfinite(rel), rel, np.inf)
    s1 = {}
    for tol in (1e-9, 1e-8, 1e-7, 1e-6, 1e-5):
        s1[tol] = int((rel <= tol).sum())
    dens2 = int((rel <= 1e-2).sum())
    dens3 = int((rel <= 1e-3).sum())
    P("members within 1e-2 of T: %d ; within 1e-3: %d" % (dens2, dens3))
    for tol, n in s1.items():
        lam2 = dens2 * tol / 1e-2
        lam3 = dens3 * tol / 1e-3
        P("  tol %.0e : found %d ; predicted lambda from 1e-2 window = %.3g, from 1e-3 window = %.3g" % (tol, n, lam2, lam3))
    hits = np.argwhere(rel <= 1e-7)
    P("  members within 1e-7 (a,b,miss): " + "; ".join("(%d,%d,%.2e)" % (i + 1, j + 1, rel[i, j]) for i, j in hits))
    P("  Gilson's own (29,137): miss vs 2022 target = %.3e (%.1f sigma)" % (rel[28, 136], rel[28, 136] / SIG))
    # ---------------- s2: rounding test
    P("")
    P("== s2: with b = 137 fixed (as in the source) find the REAL a* that hits T exactly; distance of a = 29 from a* ==")
    f = lambda aa: mp.pi / (aa * mp.cos(mp.pi / 137) * mp.tan(mp.pi / (aa * 137))) - T
    astar = mp.findroot(f, 29)
    dG_da = (f(29.01) - f(28.99)) / mp.mpf("0.02")
    P("  a* = %s ; |29 - a*| = %s ; dG/da at 29 = %s per unit a (relative %s)" % (mp.nstr(astar, 10), mp.nstr(abs(29 - astar), 6), mp.nstr(dG_da, 6), mp.nstr(dG_da / T, 6)))
    dist = float(abs(29 - astar))
    P("  chance that the nearest integer to a real target lies within %.4g of it: 2*dist = %.3g (one try; b = 137 is the integer nearest to T, i.e. chosen from the data)" % (dist, 2 * dist))
    P("  reading: with b = 137 (the integer nearest to T, i.e. fixed by the data), the integer a is the only remaining choice; the values form a one-parameter grid whose relative spacing near a = 29 is %.2e, so the nearest grid point to ANY target in the covered range (%s .. %s) is within ~%.1e of it by rounding alone."
      % (float(dG_da / T), mp.nstr(mp.pi / (1 * mp.cos(mp.pi / 137) * mp.tan(mp.pi / 137)), 12), mp.nstr(137 / mp.cos(mp.pi / 137), 12), float(dG_da / T) / 2))
    P("  => the family is NOT flat near T: it has a dense line (b = 137), so the flat-density P_decl above UNDERSTATES the chance; the rounding chance %.2f (a single try at the achieved miss vs the 2022 target) is the appropriate look-elsewhere number for K2a (the 16 members within 1e-7 in s1 are all this line)." % (2 * dist))
    # ---------------- s3: expansion
    P("")
    P("== s3: small-beta expansion 1/alpha = b + pi^2/(2b) - pi^2/(3 a^2 b) + ... (b = 137, a = 29) ==")
    b0 = mp.mpf(137)
    t1 = mp.pi ** 2 / (2 * b0)
    t2 = -mp.pi ** 2 / (3 * 29 ** 2 * b0)
    full = mp.pi / (29 * mp.cos(mp.pi / 137) * mp.tan(mp.pi / (29 * 137)))
    P("  b = 137 ; + pi^2/(2b) = %s ; - pi^2/(3 a^2 b) = %s ; sum = %s ; exact = %s ; remainder = %s" % (mp.nstr(t1, 10), mp.nstr(t2, 8), mp.nstr(b0 + t1 + t2, 14), mp.nstr(full, 14), mp.nstr(full - (b0 + t1 + t2), 6)))
    P("  b + pi^2/(2b) alone = %s : miss vs T = %.3e ; the a-term (integer a) only moves the last digits by <= pi^2/(3 b) = %s" % (mp.nstr(b0 + t1, 12), float(abs((b0 + t1) / T - 1)), mp.nstr(mp.pi ** 2 / (3 * b0), 6)))
    P("  printed value in Dattoli: 137.035999786699 ; recomputed: %s ; agree to 1e-11: %s" % (mp.nstr(full, 14), abs(full - mp.mpf("137.035999786699")) < mp.mpf("1e-11")))
    P("  Gilson's printed value vs 2022 target: rel miss %.3e = %.1f sigma_CODATA" % (float(abs(mp.mpf("137.035999786699") / T - 1)), float(abs(mp.mpf("137.035999786699") / T - 1)) / SIG))

    # ---------------- Atiyah checks
    P("")
    P("== K3 Atiyah checks (i)-(iii) ==")
    k0 = 0
    kA = 2 * k0
    kB = int(2 ** k0)
    P("  (i) printed (8.3) with k(0)=0: 'k(j+1) = 2 k(j)' gives k(1) = %d ; 'log2 k(j+1) = k(j)' gives k(1) = 2^k(0) = %d ; consistent: %s" % (kA, kB, kA == kB))
    import random
    random.seed(1)
    ok = True
    prod = 1 + 0j
    for j in range(1, 60):
        nn = 2 ** j
        p = 2 * random.randrange(-nn // 2, nn // 2) + 1
        v = np.exp(1j * np.pi * p / nn)
        prod *= v
        ok = ok and abs(abs(v) - 1) < 1e-12
    P("  (ii) product of 59 primitive 2n-th roots of unity (n=2^j, random odd p): |product| = %.12f ; all |v|=1: %s ; so it cannot equal 137.036" % (abs(prod), ok))
    # (iii) literal iteration, two readings, base-2 logs: log2 v(j) = v(j-1) + k(j-2)  => v(j) = 2^(v(j-1)+k(j-2))
    def run(kseq):
        v = [1j]
        for j in range(1, 41):
            kk = kseq(j - 2)
            try:
                arg = v[-1] + kk
                if abs(arg.real) > 1000:
                    return v, "overflow at j=%d" % j
                v.append(2 ** arg)
            except OverflowError:
                return v, "overflow at j=%d" % j
        return v, "ok"
    def kA_seq(m):
        return 0 if m >= 0 else 0
    def kB_seq(m):
        if m < 1:
            return 0
        x = 1
        for _ in range(m - 1):
            if x > 40:
                return 10 ** 6
            x = 2 ** x
        return x
    vA, stA = run(kA_seq)
    vB, stB = run(kB_seq)
    prodA = 1 + 0j
    for x in vA:
        prodA *= x
    okA = any(abs(x - 137.036) < 0.137 for x in vA) or abs(prodA - 137.036) < 0.137
    okB = any(abs(x - 137.036) < 0.137 for x in vB)
    P("  (iii) reading A (k = 0, v(j) = 2^v(j-1)): status %s after %d terms ; last v = %s ; any v or the product within 1e-3 of 137.036: %s" % (stA, len(vA), np.round(vA[-1], 4), okA))
    P("        reading B (k = 1,2,4,16,65536,...): status %s after %d terms ; last v = %s ; any v within 1e-3 of 137.036: %s" % (stB, len(vB), vB[-1], okB))
    P("        both readings diverge (towers of exponentials); neither reaches 137.036. This is a guess at an ambiguous text, not a refutation of what the author intended.")
    P("  Atiyah text: value obtained 'Starting from the Eddington number 137' and 'start anew with Zh(1) = 137.035 as starting point': the leading digits are INPUT to the computation, so 137.035 is not an output.")

    P("")
    P("== Verdict ==")
    P("rows passing all four criteria under P_MDL or P_decl: %s" % (any_clear if any_clear else "none"))
    P("H1 (no published closed formula clears the bar, loosest reading): %s" % ("TRUE" if not any_clear else "FALSE"))
    h2 = [r for r in rows if r["miss"] > 1e-6 and "P_mdl" in r]
    P("H2 (every formula with miss > 1e-6 has P_MDL > 0.5): %s   rows: %s" % (all(r["P_mdl"] > 0.5 for r in h2), [(r["id"], "%.3g" % r["P_mdl"]) for r in h2]))
    tag = "_MUTATE" if MUTATE else ""
    json.dump({r["id"]: {k: (v if not isinstance(v, dict) else v) for k, v in r.items() if k not in ("mdl_c", "forced_c", "decl_c")} for r in rows},
              open(os.path.join(HERE, "k1_results%s.json" % tag), "w"), indent=1, default=str)
    open(os.path.join(HERE, "k1_numeric_audit%s.out" % tag), "w").write("\n".join(out_lines) + "\n")
    sys.exit(1 if any_clear else 0)


if __name__ == "__main__":
    main()
