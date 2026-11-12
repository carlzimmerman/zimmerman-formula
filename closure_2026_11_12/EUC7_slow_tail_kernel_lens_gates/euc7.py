#!/usr/bin/env python3
"""EUC7 (SLOW-TAIL KERNEL ON THE LENS GATES).  Frozen criteria: FROZEN_CRITERIA.md (commit f4d4b5ae46).

The Codex phase-2 kernel mu(x) = 1 - 1/sqrt(1 + 2x), unscreened, through the lens gates of EUC1 / EUC4 / EUC5 with
nothing else changed.  A test lane; adopts nothing.

Run:
  python3 -I euc7.py --data-dir <dir with the two ECLIPSE csv files>
  EUC7_MUTATE=newton python3 -I euc7.py --data-dir <dir>          (must exit 1)
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC5_dynamical_boost"))
import euc5 as D
E = D.E
MUT = (os.environ.get("EUC7_MUTATE", "") or "").strip()
FOOT = {"canonical": 9.3603e-11, "alt": 1.132e-10}
if MUT == "newton": FOOT = {k: 1.0e-30 for k in FOOT}
G, MSUN, KPC, ARCSEC = E.G, E.MSUN, E.KPC, E.ARCSEC
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def g_slow(gN, a0):
    """invert g_N = mu(g/a0) g for mu = 1 - 1/sqrt(1+2x).  With u = sqrt(1+2x) = 1 + v:  v^3 + 2 v^2 - 2 y v - 2 y = 0."""
    y = np.maximum(np.asarray(gN, float) / a0, 1e-300)
    v = 1.0 + np.sqrt(2.0 * y)                                  # above the root; f is convex there, Newton descends monotonically
    for _ in range(80):
        f = v ** 3 + 2.0 * v * v - 2.0 * y * v - 2.0 * y
        v = v - f / (3.0 * v * v + 4.0 * v - 2.0 * y)
    return 0.5 * v * (v + 2.0) * a0

_orig = E.g_law
def g_law(gN, a0, law):
    return g_slow(gN, a0) if law == "K" else _orig(gN, a0, law)
E.g_law = g_law                                                 # euc1.Engine and euc5's Jeans code look the name up at call time

def med(x, rng):
    x = np.asarray(x, float); b = np.array([np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(2000)])
    return float(np.median(x)), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
def window_word(m, lo, hi):
    if hi < -0.25: return "OVERSHOOTS"
    if lo >= -0.25 and hi <= 0.10: return "INSIDE THE WINDOW"
    if lo > 0.10: return "SHORT"
    return "AT AN EDGE"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args(); t0 = time.time()
    tag = "euc7" + ("_MUTATE_" + MUT if MUT else "")
    P("EUC7 (SLOW-TAIL KERNEL ON THE LENS GATES)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    RES = dict(lane="EUC7", criteria_commit="f4d4b5ae46", mutate=MUT, footings=FOOT); CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    rng = np.random.default_rng(E.SEED)

    # ---------------------------------------------------------------- SLACS
    path = os.path.join(E.REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]; hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}; SL = []
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"): continue
        q = l.split("\t")
        if len(q) < len(hdr): continue
        d = dict(zl=E.fl(q[col["zlens"]]), zs=E.fl(q[col["zsrc"]]), RE=E.fl(q[col["RE"]]), lME=E.fl(q[col["Mass"]]), Fs=E.fl(q[col["Fs"]]),
                 Fc=E.fl(q[col["Fc"]]), ReV=E.fl(q[col["Re(V)"]]), sig=E.fl(q[col["sigma"]]))
        if all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"], d["Fc"]])) and d["RE"] > 0: SL.append(d)
    zl = np.array([d["zl"] for d in SL]); zs = np.array([d["zs"] for d in SL]); DAs = E.AUGER.DA(zl)
    REs = np.array([d["RE"] for d in SL]) * KPC; Res = np.array([d["ReV"] for d in SL]) * ARCSEC * DAs
    Ms = np.array([d["Fs"] * 10.0 ** d["lME"] for d in SL]) / E.M2D_frac(REs, Res, 4.0) * MSUN
    engS = E.Engine(REs, Res, np.full(len(SL), 4.0), Ms); Mlens = math.pi * REs ** 2 * E.AUGER.sigcr(zl, zs)
    hasσ = np.array([np.isfinite(d["sig"]) and d["sig"] > 0 for d in SL])
    def slacs_dyn(a0, law):
        return np.array([float(np.interp(math.log(SL[i]["sig"] * 1e3), np.log(D.sig_of_B(Ms[i], Res[i], 4.0, DAs[i], a0, law, 0.0, 1.5, 1.5)), D.LB)) for i in range(len(SL)) if hasσ[i]])

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    y = np.logspace(-6, 8, 400); gg = g_slow(y, 1.0); x = gg
    e1 = float(np.max(np.abs(x * (1.0 - 1.0 / np.sqrt(1.0 + 2.0 * x)) / y - 1.0)))
    ck("S1", "kernel inversion over g_N/a0 = 1e-6 .. 1e8 to 1e-10", "max error %.1e" % e1, e1 < 1e-10)
    lowr = float(g_slow(np.array([1e-6]), 1.0)[0] / math.sqrt(1e-6)); gh = float(g_slow(np.array([1e6]), 1.0)[0]); hir = (gh - 1e6) / math.sqrt(gh / 2.0)
    ck("S2", "deep limit g -> sqrt(g_N a0) and tail (g - g_N) -> sqrt(g a0 / 2), each to 1%", "%.4f ; %.4f" % (lowr, hir), abs(lowr - 1) < 0.01 and abs(hir - 1) < 0.01)
    gsun = G * MSUN / (1.495978707e11) ** 2; corr = float(g_slow(np.array([gsun]), 9.3603e-11)[0]) - gsun
    ck("S3", "unscreened Solar correction at 1 AU, canonical: 5.27e-7 m/s^2 to 1%", "%.3e" % corr, abs(corr / 5.27e-7 - 1.0) < 0.01)
    a0k = 1.132e-10; rat = []
    for i, d in enumerate(SL):
        sc = float(E.AUGER.sigcr(d["zl"], d["zs"])); REo = REs[i]
        gf = lambda r: _orig(G * Ms[i] * E.M3D_frac(r, Res[i], 4.0) / r ** 2, a0k, "S")
        fun = lambda R: E.M2D_from_gfun(R, gf) - math.pi * R * R * sc
        Rs = np.logspace(math.log10(0.15 * REo), math.log10(10.0 * REo), 60); v = np.array([fun(q) for q in Rs]); idx = np.where(np.diff(np.sign(v)) != 0)[0]
        if len(idx): rat.append(brentq(fun, Rs[idx[0]], Rs[idx[0] + 1], xtol=1e-5 * KPC) / REo)
    dS = float(np.median(slacs_dyn(a0k, "S") - engS.solve_b(Mlens, a0k, "S")[hasσ]))
    ck("S4", "law S through the same code: SLACS radius ratio 0.885 +- 0.005 and b_dyn - b_lens = +0.032 +- 0.005", "%.4f ; %+.3f" % (np.median(rat), dS),
       abs(np.median(rat) - 0.885) <= 0.005 and abs(dS - 0.032) <= 0.005)

    # ---------------------------------------------------------------- T1, T2
    P("\n[T1 SLACS lensing at the true source redshifts; T2 SLACS dynamics]   (law S on the record: b_lens +0.082 / +0.070, b_dyn +0.085)")
    T = {}
    for nm, a0 in FOOT.items():
        bl = engS.solve_b(Mlens, a0, "K"); bd = slacs_dyn(a0, "K")
        m1 = med(bl, rng); m2 = med(bd, rng); dd = float(np.median(bd - bl[hasσ]))
        T[nm] = dict(T1=m1, T1_word=window_word(*m1), T2=m2, T2_word=window_word(*m2), dyn_minus_lens=dd, one_potential=bool(abs(dd) <= 0.06),
                     frac_below_chabrier=float(np.mean(bl < -0.25)))
        P("  %-9s T1 b_lens = %+.3f [%+.3f, %+.3f]  -> %s      (lenses needing lighter than Chabrier: %.0f%%)" % (nm, *m1, T[nm]["T1_word"], 100 * T[nm]["frac_below_chabrier"]))
        P("  %-9s T2 b_dyn  = %+.3f [%+.3f, %+.3f]  -> %s (dynamics);  median (b_dyn - b_lens) = %+.3f -> %s"
          % (nm, *m2, T[nm]["T2_word"], dd, "ONE POTENTIAL HOLDS" if abs(dd) <= 0.06 else "lensing and dynamics disagree"))
    RES["slacs"] = T
    if MUT:
        ref = json.load(open(os.path.join(HERE, "euc7_results.json")))["slacs"]
        up = all(T[k]["T1"][0] > ref[k]["T1"][0] for k in FOOT)
        P("\n[MUTATE %s] T1 median b: canonical %+.3f (ref %+.3f), alt %+.3f (ref %+.3f) -> %s" % (MUT, T["canonical"]["T1"][0], ref["canonical"]["T1"][0],
          T["alt"]["T1"][0], ref["alt"]["T1"][0], "rose on both footings, as required; exit 1" if up else "DID NOT RISE"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if up else 2)

    # ---------------------------------------------------------------- T3, T4, T5 (Euclid)
    rows, _ = E.load(a.data_dir); E.OUT.clear()
    Pm, _ = E.select(rows, ("A",)); Bm, _ = E.select(rows, ("B",)); Sm, _ = E.select(rows, ("A", "B")); byid = {r["id"]: r for r in Sm}
    WB = [r for r in Bm if r["tE"] >= 1.7]
    P("\n[T3 Euclid ceiling, sample P; T4 wide grade-B lenses; source at infinity]   (law S on the record: f25 0.156 / 0.139 and 0.758 / 0.702)")
    EU = {}
    for name, smp, wfun in (("T3 sample P", Pm, E.word), ("T4 W_B theta_E >= 1.7", WB, None)):
        eng, z, RE, Re, n, lm = E.build(smp); Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
        for nm, a0 in FOOT.items():
            b = eng.solve_b(Mmin, a0, "K"); st = E.stats(b, rng)
            if wfun: w = wfun(st)
            else: w = "WIDE LENSES BREAK THE CEILING" if st["f25_lo"] >= 0.25 else ("NOT CONFIRMED" if st["f25_hi"] <= 0.10 else "NO VERDICT")
            st["word"] = w; st["frac_below_chabrier"] = float(np.mean(b < -0.25)); EU["%s_%s" % (name[:2], nm)] = st
            P("  %-22s %-9s %s   b_inf < -0.25: %.2f   -> %s" % (name, nm, E.fmt(st), st["frac_below_chabrier"], w))
    L = [r for r in csv.DictReader(open(os.path.join(HERE, "..", "EUC5_dynamical_boost", "euc5_a1_per_lens.csv"))) if r["unique_identifier"] in byid]
    sel = [byid[r["unique_identifier"]] for r in L]; zz = np.array([float(r["z_ref"]) for r in L]); vv = np.array([float(r["sigma_kms"]) for r in L]) / 1.064
    lm = E.arr(sel, "lm") + 2.0 * np.log10(E.EUCLID.DL(zz) / E.EUCLID.DL(E.arr(sel, "z")))
    eng, z, RE, Re, n, lm = E.build(sel, z=zz, lm=lm); DA = E.EUCLID.DA(zz); MsE = 10.0 ** lm * MSUN
    P("\n[T5 Euclid dynamics, DESI dispersions on the SLACS scale, sample S, N = %d]   (law S on the record: +0.135 / +0.128)" % len(sel))
    for nm, a0 in FOOT.items():
        b = np.array([D.b_dyn(vv[i] * 1e3, MsE[i], Re[i], n[i], DA[i], a0, "K", 0.0, 0.75, 1.1) for i in range(len(sel))]); m5 = med(b, rng)
        EU["T5_" + nm] = dict(med=m5, word=window_word(*m5), at_edge=int(np.sum(np.abs(b) >= 1.499)))
        P("  %-9s b_dyn = %+.3f [%+.3f, %+.3f]  -> %s (dynamics, reading)" % (nm, *m5, window_word(*m5)))
    RES["euclid"] = EU; RES["checks"] = CK
    allok = all(v["ok"] for v in CK.values()); verdict = "%s / %s" % (T["canonical"]["T1_word"], T["alt"]["T1_word"])
    RES["verdict"] = verdict if allok else "NOT EVALUABLE"
    P("\n[summary]")
    P("  instrument checks: %s" % ("all pass" if allok else "FAILED -> NOT EVALUABLE"))
    P("  LANE WORD (T1, SLACS lensing, canonical / alt): %s" % RES["verdict"])
    P("  kappa = 1/2 FITTED. A test lane; adopts nothing. No outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
