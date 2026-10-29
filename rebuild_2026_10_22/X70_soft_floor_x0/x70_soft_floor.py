#!/usr/bin/env python3
"""X70_soft_floor_x0: X43's core rule with the floor softened by the peak baryonic acceleration,
Sigma_core = max(Sigma_M F(X0), eta Sigma_coll), F = k X0 / sqrt(1 + (k X0)^2), k = 4 (spec; 3.93 by arithmetic, reported).
Frozen criteria cffa3cc8bd (committed alone). Machinery read-only: X68 (99028a0bb8) up to its main loop (X43's SPARC harness).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
F is a chosen interpolating form, not derived; nothing here says the data favour the framework.
Run:
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x70_soft_floor.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x70_soft_floor.py --mutate   -> k = 8, _MUTATE outputs
"""
import os, sys, io, json, math, time, resource, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.integrate import quad
from scipy.special import i0, i1, k0, k1

T0 = time.time()
MUTATE = "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

X68SRC = os.path.join(REB, "X68_split_scale_halo", "x68_split_scale.py"); T = open(X68SRC).read()
code68 = T[:T.index("\nfor f in FEET:\n    SLOG.clear()")]
for old, new in (('MUTATE = "--mutate" in sys.argv', "MUTATE = False"), ('"x68_x30_machinery"', '"x70_x30_machinery"')):
    assert code68.count(old) == 1; code68 = code68.replace(old, new)
N8 = {"__file__": os.path.join(HERE, "x68_ro.py"), "__name__": "x68_ro"}; argv0 = sys.argv; sys.argv = [X68SRC]
buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(compile(code68, X68SRC, "exec"), N8)
sys.argv = argv0
N8["MODE"]["split"] = False                                                   # halo_M is exactly X43's Burkert call
KF = 8.0 if MUTATE else 4.0
P(f"X70_soft_floor_x0  {'MUTATE run (k = 8)' if MUTATE else 'normal run'}  [c_f EXTERNAL; F chosen, not derived]")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian), core Sigma = max(Sigma_M F(X0), eta Sigma_coll), eta 14.83 not refit; not theory closed")
P(f"X68 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
FEET, SIG, SIG_PC, GE, MSUNE, MPCE, A0, GALS, UPS = (N8[k] for k in ("FEET", "SIG", "SIG_PC", "GE", "MSUNE", "MPCE", "A0", "GALS", "UPS"))
BGS, fit_one, pooled, line, sig_core, halo_M = (N8[k] for k in ("BGS", "fit_one", "pooled", "line", "sig_core", "halo_M"))
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
F = lambda X, k=KF: k * X / math.sqrt(1 + (k * X) ** 2)
iu5 = int(np.argmin(np.abs(UPS - 0.50))); assert abs(UPS[iu5] - 0.50) < 1e-9
GPK = {}
for q in GALS:
    gb = q["GB"][:, iu5]; GPK[q["name"]] = float(np.max(gb[np.isfinite(gb)]))
def sparc_soft(f, tag, k):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []; per = {}
    for q in GALS:
        lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
        sc, _ = sig_core(f, tag, M200)                                        # max(Sigma_M, eta Sigma_coll), X43
        scoll = sc if sc > SIG[f] else 0.0
        s = max(SIG[f] * (1.0 if k is None else F(GPK[q["name"]] / A0[f], k)), scoll)
        Mh = halo_M(M200 * MSUNE, R200, s, M200, q["Rm"], False, "sparc", f)
        r = fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300))); rows.append(r)
        per[q["name"]] = float(math.sqrt(r[0] / r[1]))
    st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows]); st["line"] = bool(line(st)); st["per"] = per; return st
checks = []
# K0: F == 1 reproduces X43
d0 = max(abs(sparc_soft(f, t, None)["rms"] - X43J["footings"][f]["sparc"][t]["rms"]) for f in FEET for t in BGS)
P(f"K0 F == 1 reproduces X43's SPARC rms (both footings, both backgrounds): max |d| {d0:.1e}: {'PASS' if d0 < 1e-6 else 'FAIL'}"); checks.append(("K0", d0 < 1e-6))
# K1: F algebra; exponential thin-disc peak vs quadrature
k1a = abs(F(1e4, 4.0) - 1) < 1e-6 and abs(F(0.33, 4.0) - 0.797) < 0.005
def gdisc(R, M, Rd):                                                          # Freeman 1970 thin exponential disc, radial g
    y = R / (2 * Rd); S0 = M / (2 * math.pi * Rd ** 2)
    return 4 * math.pi * GE * S0 * Rd * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)) / R
def gdisc_q(R, M, Rd):                                                        # same, by the Hankel quadrature of the potential (u = k R_d)
    from scipy.special import j1
    S0 = M / (2 * math.pi * Rd ** 2)
    return 2 * math.pi * GE * S0 * quad(lambda u: u * (1 + u * u) ** -1.5 * j1(u * R / Rd), 0, 400, limit=4000, epsabs=0, epsrel=1e-10)[0]
KPC = 3.0857e19; Mt = 1e9 * MSUNE; Rd_ = 1.0 * KPC
k1b = all(abs(gdisc(x * KPC, Mt, Rd_) / gdisc_q(x * KPC, Mt, Rd_) - 1) < 1e-4 for x in (0.3, 1.0, 2.2, 5.0))
P(f"K1 F(1e4) {F(1e4, 4.0):.6f}, F(0.33) {F(0.33, 4.0):.4f}; Freeman disc g vs Hankel quadrature (0.3-5 R_d): {'PASS' if k1a and k1b else 'FAIL'}")
checks.append(("K1", k1a and k1b))

RES = dict(frozen="cffa3cc8bd", mutate=MUTATE, k=KF, Sigma_Msun_pc2=SIG_PC, footings={})
for f in FEET:
    P(f"\n=== [{f}] a0 {A0[f]:.3e}, Sigma_M {SIG_PC[f]:.1f} Msun/pc^2")
    X0 = {n: g / A0[f] for n, g in GPK.items()}
    Fv = {n: F(x) for n, x in X0.items()}; shift = [n for n, v in Fv.items() if v < 0.794]
    frac = len(shift) / len(GALS); G1 = frac < 0.15
    P(f"  X0 (U = 0.50): median {np.median(list(X0.values())):.3f}, p10 {np.percentile(list(X0.values()), 10):.3f}, p90 {np.percentile(list(X0.values()), 90):.3f}; "
      f"F < 0.794 in {len(shift)}/{len(GALS)} = {100 * frac:.1f}% -> G1 {'PASS' if G1 else 'FAIL'} (< 15%)")
    hard = {t: sparc_soft(f, t, None) for t in BGS}; soft = {t: sparc_soft(f, t, KF) for t in BGS}; v393 = {t: sparc_soft(f, t, 3.93) for t in BGS}
    G2 = all(soft[t]["rms"] <= 0.08 for t in BGS)
    for t in BGS:
        P(f"  SPARC [{t}]: hard {hard[t]['rms']:.4f} -> soft {soft[t]['rms']:.4f} (line {'PASS' if soft[t]['line'] else 'FAIL'}, U median {soft[t]['U_median']:.2f}); k = 3.93 variant {v393[t]['rms']:.4f}")
    P(f"  G2 (rms <= 0.08 both backgrounds): {'PASS' if G2 else 'FAIL'}")
    dper = {n: soft["A_c2b_refit"]["per"][n] - hard["A_c2b_refit"]["per"][n] for n in shift}
    better = sum(v < 0 for v in dper.values())
    P(f"  shifted galaxies (bg A): per-galaxy rms better in {better}/{len(shift)}; median change {np.median(list(dper.values())) if dper else 0:+.4f} dex; "
      f"worst 5: " + ", ".join(f"{n} {v:+.3f}" for n, v in sorted(dper.items(), key=lambda kv: -kv[1])[:5]))
    v = "SOFT FLOOR PASSES" if (G1 and G2) else "SOFT FLOOR FAILS"
    det = ([] if G1 else [f"G1 {100 * frac:.1f}% shifted"]) + ([] if G2 else ["G2 rms " + "/".join(f"{soft[t]['rms']:.4f}" for t in BGS)])
    P(f"  VERDICT [{f}]: {v}" + (f"  (failing: {', '.join(det)})" if det else ""))
    # IC 1613 (IN1's HI estimator, route E halo)
    MS_, MG_, VROT48, RMAX, I0, RH = 2.88e7, 5.93e7, 16.9, 2.71, 48.0, 1.43978
    Mb = (MS_ + MG_) * MSUNE; rr = RMAX * KPC; gN = GE * Mb / rr ** 2
    Rd = RH / 1.678 * KPC; xs = np.linspace(0.05, 6, 6000) * Rd; gpk_hi = float(max(gdisc(x, Mb, Rd) for x in xs))
    bg = BGS["A_c2b_refit"]; rcrit = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
    M200 = 10 ** (bg["a"] + bg["b"] * (math.log10(MS_ + MG_) - 10)); R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rcrit)) ** (1 / 3)
    ic = {}
    for lab, X in (("hard", None), ("soft lo X0", gN / A0[f]), ("soft hi X0", gpk_hi / A0[f])):
        s = SIG[f] if X is None else SIG[f] * F(X)
        Mh = float(np.atleast_1d(halo_M(M200 * MSUNE, R200, s, M200, np.array([rr]), False, "ic1613", f))[0])
        gp = gN + GE * Mh / rr ** 2
        for i in (32.0, 36.0):
            V = VROT48 * math.sin(math.radians(I0)) / math.sin(math.radians(i)); E = math.log10((V * 1e3) ** 2 / rr) - math.log10(gp)
            ic[f"{lab}|{i:g}"] = dict(E=E, X0=X, F=None if X is None else F(X))
    resc = all(abs(ic[f"{b}|{i:g}"]["E"]) <= 0.15 for b in ("soft lo X0", "soft hi X0") for i in (32.0, 36.0))
    P(f"  IC 1613 (M200 10^{math.log10(M200):.2f}; X0 lo {gN / A0[f]:.3f} F {F(gN / A0[f]):.3f}, hi {gpk_hi / A0[f]:.3f} F {F(gpk_hi / A0[f]):.3f}): "
      + "; ".join(f"{k_} E {v_['E']:+.3f}" for k_, v_ in ic.items()) + f" -> {'RESCUED' if resc else 'NOT RESCUED'} (|E| <= 0.15)")
    RES["footings"][f] = dict(G1=G1, frac_shift=frac, shifted=shift, G2=G2, hard={t: dict(rms=hard[t]["rms"]) for t in BGS},
                              soft={t: dict(rms=soft[t]["rms"], line=soft[t]["line"], U_median=soft[t]["U_median"]) for t in BGS},
                              k393={t: v393[t]["rms"] for t in BGS}, dper_shifted=dper, verdict=v, failing=det, ic1613=ic, ic1613_rescued=resc,
                              X0=X0)
V = {f: RES["footings"][f]["verdict"] for f in FEET}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
RV = {f: RES["footings"][f]["ic1613_rescued"] for f in FEET}
RES["ic1613"] = "RESCUED" if all(RV.values()) else ("NOT RESCUED" if not any(RV.values()) else f"UNDECIDED (footings disagree: {RV})")
P(f"\n=== VERDICT (both footings): {RES['verdict']} [c_f EXTERNAL; F chosen]\n=== IC 1613: {RES['ic1613']}")
checks.append(("K2", rss() < 2.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(bool(ok) for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
if MUTATE and os.path.exists(os.path.join(HERE, "x70_soft_floor_results.json")):
    NJ = json.load(open(os.path.join(HERE, "x70_soft_floor_results.json")))
    dm = max(abs(RES["footings"][f_]["soft"][t_]["rms"] - NJ["footings"][f_]["soft"][t_]["rms"]) for f_ in FEET for t_ in BGS)
    P(f"MUTATE sensitivity: max SPARC rms change vs normal run {dm:.5f} ({'sensitive' if dm > 1e-4 else 'HARNESS INSENSITIVE'})"); RES["mutate_max_drms"] = dm
open(os.path.join(HERE, f"x70_soft_floor{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
json.dump(RES, open(os.path.join(HERE, f"x70_soft_floor_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
