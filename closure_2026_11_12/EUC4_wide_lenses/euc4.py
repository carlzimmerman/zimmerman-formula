#!/usr/bin/env python3
"""EUC4 (WIDE LENSES).  Frozen criteria: FROZEN_CRITERIA.md (commit 3ef9630a69).

Part A: EUC1's exploratory map put the excess over the law's ceiling in wide-separation lenses.  That split is tested
        here on the grade-B lenses (disjoint from EUC1's sample P), theta_E >= 1.7 arcsec, with EUC1's code.
Part B: (EXPLORATORY) the gas mass a beta-model group would need for law S to supply those lenses.

Run:
  python3 -I euc4.py --data-dir <dir with the two ECLIPSE csv files>
  EUC4_MUTATE=newton python3 -I euc4.py --data-dir <dir>      (must exit 1)
"""
import argparse, csv, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E
MUT = (os.environ.get("EUC4_MUTATE", "") or "").strip()
if MUT == "newton": E.FOOT = {k: 1.0e-30 for k in E.FOOT}
G, MSUN, KPC, PC = E.G, E.MSUN, E.KPC, E.PC
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def word(st):
    if st["N"] < 30: return "NOT EVALUABLE"
    if st["f25_lo"] >= 0.25: return "WIDE LENSES BREAK THE CEILING"
    if st["f25_hi"] <= 0.10: return "NOT CONFIRMED"
    return "NO VERDICT"

def grade(sample, rng, laws=("S", "B"), **kw):
    eng, z, RE, Re, n, lm = E.build(sample, **kw)
    Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
    out = {}
    for law in laws:
        for nm, a0 in E.FOOT.items():
            st = E.stats(eng.solve_b(Mmin, a0, law), rng); st["word"] = word(st); out[law + "_" + nm] = st
    return out

class GasEngine:
    """stars (Sersic, catalogue mass x Bstar) + a beta = 2/3 gas body cut at 500 kpc; law S or B; solve for the gas mass."""
    def __init__(self, RE, Re, n, Mstar, rc, rcut=500.0 * KPC, rmax=1.0e6 * KPC):
        RE, Re, n, Mstar = (np.asarray(v, float) for v in (RE, Re, n, Mstar))
        U = np.arccosh(np.maximum(rmax / RE, 1.0 + 1e-9))
        r = RE[:, None] * np.cosh(E.GLX[None, :] * U[:, None])
        self.gs = G * Mstar[:, None] * E.M3D_frac(r, Re[:, None], n[:, None]) / r ** 2
        x = np.minimum(r, rcut) / rc; X = rcut / rc
        self.gg = G * ((x - np.arctan(x)) / (X - math.atan(X))) / r ** 2       # per kg of gas inside rcut
        self.pref = RE ** 2 / G * U; self.N = len(RE)
    def M2D(self, Mg, Bs, a0, law):
        gN = Bs * self.gs + np.asarray(Mg, float)[:, None] * self.gg
        return self.pref * np.sum(E.GLW[None, :] * E.g_law(gN, a0, law), axis=1)
    def solve(self, Mmin, Bs, a0, law="S"):
        lo = np.full(self.N, 8.0); hi = np.full(self.N, 16.0)
        none = self.M2D(np.full(self.N, 1.0e8 * MSUN), Bs, a0, law) >= Mmin
        for _ in range(44):
            mid = 0.5 * (lo + hi)
            up = self.M2D(10.0 ** mid * MSUN, Bs, a0, law) < Mmin
            lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        return np.where(none, -np.inf, 0.5 * (lo + hi)), none

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    t0 = time.time(); tag = "euc4" + ("_MUTATE_" + MUT if MUT else "")
    P("EUC4 (WIDE LENSES)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    rows, _ = E.load(a.data_dir); E.OUT.clear()
    Pm, _ = E.select(rows, ("A",)); Bm, _ = E.select(rows, ("B",))
    rng = np.random.default_rng(E.SEED)
    RES = dict(lane="EUC4", criteria_commit="3ef9630a69", mutate=MUT, footings=E.FOOT)
    CK = {}

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    if not MUT:
        g = grade(Pm, np.random.default_rng(E.SEED), laws=("S",))
        ok = abs(g["S_canonical"]["f25"] - 0.156) <= 0.001 and abs(g["S_alt"]["f25"] - 0.139) <= 0.001
        CK["E1"] = dict(value=[g["S_canonical"]["f25"], g["S_alt"]["f25"]], ok=bool(ok))
        P("  %s E1  EUC1's primary numbers on P reproduced: f25 = %.3f / %.3f (0.156 / 0.139)" % ("PASS" if ok else "FAIL", g["S_canonical"]["f25"], g["S_alt"]["f25"]))
    shared = len({r["id"] for r in Pm} & {r["id"] for r in Bm})
    CK["E2"] = dict(value=shared, ok=shared == 0)
    P("  %s E2  identifiers shared by grade A (P, N = %d) and grade B (N = %d): %d" % ("PASS" if shared == 0 else "FAIL", len(Pm), len(Bm), shared))

    # ---------------------------------------------------------------- Part A
    WB = [r for r in Bm if r["tE"] >= 1.7]
    SEC = [r for r in Bm if 1.3 <= r["tE"] < 1.7]
    CMP = [r for r in Bm if r["tE"] < 1.0]
    P("\n[Part A: grade-B lenses, source at infinity]")
    A = {}
    for name, smp in (("W_B: theta_E >= 1.7 arcsec (primary)", WB), ("secondary: 1.3 <= theta_E < 1.7", SEC), ("complement: theta_E < 1.0", CMP)):
        g = grade(smp, rng); A[name] = g
        for k in ("S_canonical", "S_alt", "B_canonical", "B_alt"):
            P("  %-38s law %s %-9s %s   -> %s" % (name, k[0], k[2:], E.fmt(g[k]), g[k]["word"]))
    prim = A["W_B: theta_E >= 1.7 arcsec (primary)"]
    verdict = "%s / %s" % (prim["S_canonical"]["word"], prim["S_alt"]["word"])
    P("  LANE WORD (W_B, law S, canonical / alt): %s" % verdict)
    RES["partA"] = A; RES["verdict"] = verdict
    P("  W_B medians: z_l = %.3f, theta_E = %.2f\", log M* = %.2f, theta_E/theta_e = %.2f, n = %.2f"
      % (np.median(E.arr(WB, "z")), np.median(E.arr(WB, "tE")), np.median(E.arr(WB, "lm")), np.median(E.arr(WB, "tE") / E.arr(WB, "te")), np.median(E.arr(WB, "n"))))

    if MUT:
        ref = json.load(open(os.path.join(HERE, "euc4_results.json")))["partA"]["W_B: theta_E >= 1.7 arcsec (primary)"]
        up = all(prim["S_" + k]["f25"] > ref["S_" + k]["f25"] for k in E.FOOT)
        P("\n[MUTATE %s] f25 on W_B, law S: canonical %.3f (ref %.3f), alt %.3f (ref %.3f) -> %s" % (MUT, prim["S_canonical"]["f25"],
          ref["S_canonical"]["f25"], prim["S_alt"]["f25"], ref["S_alt"]["f25"], "rose on both footings, as required; exit 1" if up else "DID NOT RISE"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if up else 2)

    # ---------------------------------------------------------------- robustness
    P("\n[robustness on W_B, law S; cannot change the word]")
    ROB = {}
    def rob(name, smp, **kw):
        g = grade(smp, rng, laws=("S",), **kw); ROB[name] = g
        P("  %-28s canonical %s  %s" % (name, E.fmt(g["S_canonical"]), g["S_canonical"]["word"]))
        P("  %-28s alt       %s  %s" % ("", E.fmt(g["S_alt"]), g["S_alt"]["word"]))
    rob("R_e x 0.80", WB, re_scale=0.80)
    rob("n = 4", WB, n_fix=4.0)
    Bsie, _ = E.select(rows, ("B",), "tSIE"); rob("SIE Einstein radius >= 1.7", [r for r in Bsie if r["tSIE"] >= 1.7], te_key="tSIE")
    rob("z_l < 1.0", [r for r in WB if r["z"] < 1.0])
    rob("r_max = 300 kpc", WB, rmax=300.0 * KPC)
    rob("threshold 1.5 arcsec", [r for r in Bm if r["tE"] >= 1.5])
    rob("threshold 2.0 arcsec", [r for r in Bm if r["tE"] >= 2.0])
    RES["robustness"] = ROB

    # ---------------------------------------------------------------- Part B (exploratory)
    P("\n[Part B, EXPLORATORY, no verdict: gas a beta-model group would need for law S to supply wide lenses]")
    wide = [r for r in Pm if r["tE"] >= 1.7] + WB
    eng, z, RE, Re, n, lm = E.build(wide)
    Ms = 10.0 ** lm * MSUN; u = MSUN / PC ** 2
    P("  lenses: %d (grade A %d, grade B %d), theta_E >= 1.7 arcsec; reference range for X-ray groups: 1e12 to 4e12 Msun inside R500 (from memory, PROVISIONAL)"
      % (len(wide), len(wide) - len(WB), len(WB)))
    P("  %-6s %-5s %-6s %-9s  %8s  %22s  %10s  %s" % ("r_c", "z_s", "stars", "footing", "no gas", "log M_g 16/50/84 %", "M_g/M*", "below 1e12 / in range / above 4e12"))
    PB = {}
    for rc in (30.0, 100.0):
        ge = GasEngine(RE, Re, n, Ms, rc * KPC)
        for zs, zl in ((E.ZS_INF, "inf"), (3.0, "3")):
            Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, zs)
            for Bs in (1.0, 1.174):
                for nm, a0 in E.FOOT.items():
                    lg, none = ge.solve(Mmin, Bs, a0)
                    q = np.percentile(np.where(np.isfinite(lg), lg, 0.0), [16, 50, 84])
                    need = np.isfinite(lg)
                    ratio = float(np.median(10.0 ** lg[need] * MSUN / Ms[need])) if need.any() else float("nan")
                    lo, mid, hi = float(np.mean(lg < 12.0)), float(np.mean((lg >= 12.0) & (lg <= math.log10(4e12)))), float(np.mean(lg > math.log10(4e12)))
                    key = "rc%d_zs%s_B%.3f_%s" % (rc, zl, Bs, nm)
                    PB[key] = dict(no_gas=float(none.mean()), q16=float(q[0]), q50=float(q[1]), q84=float(q[2]), ratio_med=ratio, below=lo, inrange=mid, above=hi,
                                   capped=float(np.mean(lg >= 15.99)))
                    P("  %-6.0f %-5s %-6.3f %-9s  %7.1f%%  %6.2f / %6.2f / %6.2f   %9.1f   %.2f / %.2f / %.2f"
                      % (rc, zl, Bs, nm, 100 * none.mean(), q[0], q[1], q[2], ratio, lo, mid, hi))
    RES["partB"] = PB
    # what the cold pull supplies at the median required gas (rc = 100, source at infinity, Salpeter)
    ge = GasEngine(RE, Re, n, Ms, 100.0 * KPC); Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
    for nm, a0 in E.FOOT.items():
        lg, none = ge.solve(Mmin, 1.0, a0); Mg = np.where(np.isfinite(lg), 10.0 ** lg, 0.0) * MSUN
        tot = ge.M2D(Mg, 1.0, a0, "S"); newt = ge.M2D(Mg, 1.0, 1.0e-30, "S"); st = ge.M2D(np.zeros(ge.N), 1.0, 1.0e-30, "S")
        area = math.pi * RE ** 2
        P("  r_c = 100 kpc, source at infinity, %-9s medians inside R_E [Msun/pc^2]: stars %.0f, gas (projected) %.0f, cold pull %.0f, needed %.0f"
          % (nm, np.median(st / area) / u, np.median((newt - st) / area) / u, np.median((tot - newt) / area) / u, np.median(Mmin / area) / u))

    with open(os.path.join(HERE, "euc4_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["unique_identifier", "grade", "z_l", "theta_E_arcsec", "log_Mstar", "b_inf_S_canonical", "b_inf_S_alt"])
        bb = {nm: eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), a0, "S") for nm, a0 in E.FOOT.items()}
        for i, r in enumerate(wide): w.writerow([r["id"], r["grade"], "%.3f" % z[i], "%.3f" % r["tE"], "%.3f" % lm[i], "%.4f" % bb["canonical"][i], "%.4f" % bb["alt"][i]])
    allok = all(v["ok"] for v in CK.values()); RES["checks"] = CK
    P("\n[summary]")
    P("  instrument checks: %s" % ("all pass" if allok else "FAILED -> NOT EVALUABLE"))
    P("  LANE WORD (W_B, law S, canonical / alt): %s" % (verdict if allok else "NOT EVALUABLE"))
    P("  kappa = 1/2 FITTED. One-sided test: no outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
