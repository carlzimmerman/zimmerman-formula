"""CFG183 attacks (a) P0 physical possibility [a1-a4], (b) gas ceiling [+ b3 convention map], (c) survival [c1-c4, c4b]. Exit 0."""
import os, sys, json, math
import numpy as np
import CFG183_common as C
from CFG183_common import M, pr

S, AS, K = C.load("inc_star_deg")
T = C.make_law("T")
LAWS = (("flat", None, "flat"), ("rival", None, "H"), ("T", T, "H"))
res = {}

def dsig(smp, s, mu, law, which, **kw):
    return C.cell(smp, AS, s, mu, law, **kw)[which]

def jfix(o):
    if isinstance(o, dict): return {str(k): jfix(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jfix(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o

# ============================== (a) ==============================
pr("=== (a) Is P0 physically possible? conditions from the repo tables + the sigma methods note")
MUS = [0.67, 1.01, 1.5, 2.05, 3.47]
res["a1"] = {}
pr("a1 s-bands at fixed gas: s0 (D'=0) [s_lo (D'=-sigma), s_hi (D'=+sigma)]")
for mu in MUS:
    row = {}
    for L, law, wh in LAWS:
        f = lambda s: dsig(S, s, mu, law, wh)
        row[L] = (C.s_root(f), C.s_root(f, -1.0), C.s_root(f, +1.0))
    res["a1"][mu] = row
    pr("  mu=%.2f  " % mu + " | ".join("%s: %s [%s, %s]" % (L, *[("%.3f" % v if isinstance(v, float) else v) for v in row[L]]) for L in row))
pr("a2 K21 as a band: break-even mu and status at s = 0.6, 0.8, 1.0, 1.4 (ceiling 3.47)")
res["a2"] = {}
for s in (0.6, 0.8, 1.0, 1.4):
    row = {}
    for L, law, wh in LAWS:
        be = C.breakeven(lambda m: dsig(S, s, m, law, wh))
        row[L] = (C.fmt_be(be), C.status(be))
    res["a2"][s] = row
    pr("  s=%.1f  " % s + " | ".join("%s %s %s" % (L, *row[L]) for L in row))
pr("a3 what the s-axis means physically (KURVS ten discs; q = mean(1 - V^2/V_c^2) pressure fraction; corr = V_c/V - 1)")
res["a3"] = {}
for s in (0.0, 0.1, 0.3, 0.5, 0.6, 0.75, 1.0, 1.42, 3.0):
    r = C.cell(S, AS, s, 0.67, None)["r"]["po"]
    ratio = np.asarray(r["Vc2_over_V2"]); q = float(np.mean(1 - 1 / ratio)); cr = np.sqrt(ratio) - 1
    res["a3"][s] = (q, float(cr.min()), float(np.median(cr)), float(cr.max()))
    pr("  s=%.2f  q_mean=%.3f  V_c/V-1 min/median/max = %.2f / %.2f / %.2f   (isotropic-LOS anisotropy factor (sigma_R/sigma_los)^2 = s for K21's gradient)" % ((s,) + res["a3"][s]))
pr("a4 required non-supporting fraction f_ns = 1 - s_eff/s_phys of sigma_obs^2  (s_eff = s0, clipped at 0; also the 1sigma upper edge)")
res["a4"] = {}
for mu in MUS:
    row = {}
    for L in ("flat", "rival", "T"):
        s0, slo, shi = res["a1"][mu][L]
        def cl(v): return 0.0 if v == "<0" else (6.0 if v == ">6" else v)
        row[L] = {sp: (1 - cl(s0) / sp, 1 - cl(shi) / sp) for sp in (1.0, 3.0)}
    res["a4"][mu] = row
    pr("  mu=%.2f " % mu + " | ".join("%s: f_ns(s_phys=1) %.2f [at s_hi %.2f], (s_phys=3) %.2f" % (L, row[L][1.0][0], row[L][1.0][1], row[L][3.0][0]) for L in row))
pr("  in-hand outer-sigma measures: CFG141 sigma_out/sigma_0 ~ 1.05; paper's outer/full ratio 1.13 +- 0.26 (note, section 10)")
fT = [res["a4"][mu]["T"][1.0][0] for mu in (0.67, 1.01, 1.5)]
cls_a = "CONTAMINATION-ALLOWED" if all(0.7 <= v <= 1.0 for v in fT) else "NOT (f_ns outside [0.7,1.0] at some mu <= 1.69): %s" % ["%.2f" % v for v in fT]
pr("  classification (a4):", cls_a, " f_ns(T; mu=0.67,1.01,1.5) =", ["%.2f" % v for v in fT])
pr("  P0 not-excluded-by-the-repo test: T 1sigma band includes s <= 0.3 at mu <= 1.69?",
   [ (mu, res["a1"][mu]["T"][1] if not isinstance(res["a1"][mu]["T"][1], str) else res["a1"][mu]["T"][1]) for mu in (0.67, 1.01, 1.5)])
pr("  outside K21's own scatter test (T s_hi < 0.6)?", [(mu, res["a1"][mu]["T"][2], (res["a1"][mu]["T"][2] < 0.6) if isinstance(res["a1"][mu]["T"][2], float) else res["a1"][mu]["T"][2]) for mu in MUS])

# ============================== (b) ==============================
pr("=== (b) the gas ceiling 3.47 (declared choice)")
BE = {(L, s): C.breakeven(lambda m: dsig(S, s, m, law, wh)) for L, law, wh in LAWS for s in C.S_PUB}
CEILS = [1.69, 1.90, 2.0, 2.57, 3.47, 3.8, 4.0, 5.0]
res["b_matrix"] = {}
pr("status matrix by ceiling (s = 0 / 1 / 1.42 / 1.62 / 1.69 / 3.00); e=excluded a=allowed o=over")
for ce in CEILS:
    row = {L: "".join({"excluded": "e", "allowed": "a", "over": "o"}[C.status(BE[(L, s)], ce)] for s in C.S_PUB) for L in ("flat", "rival", "T")}
    res["b_matrix"][ce] = row
    pr("  ceiling %.2f  flat %s  rival %s  T %s" % (ce, row["flat"], row["rival"], row["T"]))
res["b_flip"] = {L: {s: BE[(L, s)]["lo"] for s in C.S_PUB} for L in ("flat", "rival", "T")}
pr("lowest ceiling at which each law becomes gas-allowed at s (= lower 1sigma edge):")
for L in ("flat", "rival", "T"):
    pr("  %-5s" % L, ["%.3f" % BE[(L, s)]["lo"] if BE[(L, s)]["lo"] else "n/a" for s in C.S_PUB])
PRI = {"primary": (1.01, .60, 1.69), "h=0.5": (1.57, .91, 2.57), "h=1": (2.05, 1.19, 3.47), "M": (1.30, .75, 2.26), "Z": (1.31, .75, 2.19)}
from math import erf, log, sqrt
def cdf_ln(x, med, sig): return 0.5 * (1 + erf((log(x) - log(med)) / (sig * sqrt(2))))
res["b_prior"] = {}
pr("P(prior mu >= mu_be) (lognormal matched to the READ median and 16-84% of CFG164; approximate):")
for nm, (med, p16, p84) in PRI.items():
    sg = log(p84 / p16) / 2
    row = {}
    for L in ("flat", "rival", "T"):
        row[L] = [ (1 - cdf_ln(BE[(L, s)]["mu"], med, sg)) if BE[(L, s)]["mu"] else None for s in C.S_PUB]
    res["b_prior"][nm] = row
    pr("  %-8s (med %.2f sig_ln %.3f) " % (nm, med, sg) + " | ".join("%s %s" % (L, ["%.3f" % v if v is not None else "  -  " for v in row[L]]) for L in row))
rob = all(C.status(BE[("T", s)], 3.5) == "excluded" for s in (1.0, 1.42, 1.62, 1.69, 3.0))
pr("classification: DECLARED CHOICE; T excluded at every published s for ceilings <= 3.5: %s (smallest lower edge %.4f); ceiling-FRAGILE above it: flips at %s" % (rob, BE[("T", 1.0)]["lo"], ["%.3f" % BE[("T", s)]["lo"] for s in (1.0, 1.42, 1.62, 1.69, 3.0)]))
res["b_robust_le_3.5"] = rob
pr("b3 (ADDED after the frozen list; not frozen) convention map of T's s=1 lower edge (ceiling 3.47; 'excluded' iff lower edge > 3.47):")
def lo1(smp=S, AS_=AS, law=T, **kw):
    return None
conv = {}
conv["main: sigma at trial mu, pooled anchor, inc_star"] = BE[("T", 1.0)]["lo"]
f = lambda m: dsig(S, 1.0, m, T, "H")
conv["sigma fixed at the break-even"] = C.be_generic(f, "fixed_be")["lo"]
conv["sigma fixed at mu=0.67"] = C.be_generic(f, "fixed", 0.67)["lo"]
conv["anchor = median (+0.073)"] = C.breakeven(lambda m: dsig(S, 1.0, m, T, "H", anchor_mode="median"))["lo"]
conv["anchor = none"] = C.breakeven(lambda m: dsig(S, 1.0, m, T, "H", anchor_mode="none"))["lo"]
S2, _, _ = C.load("inc_sfr_deg")
conv["inc_sfr_deg"] = C.breakeven(lambda m: dsig(S2, 1.0, m, T, "H"))["lo"]
conv["T at Om=0.3111"] = C.breakeven(lambda m: dsig(S, 1.0, m, C.make_law("T", Om=0.3111), "H"))["lo"]
conv["T at Om=0.30"] = C.breakeven(lambda m: dsig(S, 1.0, m, C.make_law("T", Om=0.30), "H"))["lo"]
conv["single z=1.5 for all ten"] = C.breakeven(lambda m: dsig(S, 1.0, m, C.make_law("Tconst", z=1.5), "H"))["lo"]
conv["gas-disc scale 1 R_d"] = C.breakeven(lambda m: C.cell(S, AS, 1.0, m, T, gas_scale=1.0)["H"])["lo"]
conv["gas-disc scale 3 R_d"] = C.breakeven(lambda m: C.cell(S, AS, 1.0, m, T, gas_scale=3.0)["H"])["lo"]
conv["R_e = 2 R_eff (KURVS and anchor)"] = C.breakeven(lambda m: C.cell(S, AS, 1.0, m, T, spec_kw=dict(Refac=2.0, Refac_anchor=2.0))["H"])["lo"]
conv["alt a0 footing (1.131e-10)"] = C.breakeven(lambda m: C.cell(S, AS, 1.0, m, T, foot="alt")["H"])["lo"]
res["b3"] = conv
for k, v in conv.items():
    pr("  %-46s lower edge %s  -> %s" % (k, "%.3f" % v if v else "n/a", "excluded" if v and v > C.CEIL else "ALLOWED"))
nflip = sum(1 for v in conv.values() if v and v <= C.CEIL)
pr("  %d of %d convention variants flip T's s=1 label to allowed" % (nflip, len(conv)))

# ============================== (c) ==============================
pr("=== (c) does the P0 fit survive?  survival := at P0, mu=0.67 |z_T|<2 AND T break-even 1sigma interval overlaps [0.60, 1.69]")
def survive(smp, law=T, **kw):
    d, sg = dsig(smp, 0.0, 0.67, law, "H", **kw)
    be = C.breakeven(lambda m: dsig(smp, 0.0, m, law, "H", **kw))
    ov = be["mu"] is not None and be["lo"] <= 1.69 and (be["hi"] >= 0.60)
    return {"d": d, "sig": sg, "z": d / sg, "be": C.fmt_be(be), "mu_be": be["mu"], "lo": be["lo"], "hi": be["hi"], "surv": bool(abs(d / sg) < 2 and ov)}
res["c1"] = {}
pr("c1 anchor / definition variants (T at P0):")
for nm, kw in (("pooled (main)", {}), ("anchor = median", {"anchor_mode": "median"}), ("anchor = none", {"anchor_mode": "none"}),
               ("gas-disc scale 1 R_d", {"gas_scale": 1.0}), ("gas-disc scale 3 R_d", {"gas_scale": 3.0}),
               ("R_e = 2 R_eff, anchor also", {"spec_kw": dict(Refac=2.0, Refac_anchor=2.0)}), ("alt a0 footing", {"foot": "alt"})):
    r = survive(S, **kw); res["c1"][nm] = r
    pr("  %-32s D'=%+.4f +-%.4f z=%+.2f  mu_be %s  survive=%s" % (nm, r["d"], r["sig"], r["z"], r["be"], r["surv"]))
pr("c3 inclination column (T at P0):")
res["c3"] = {}
for col in ("inc_star_deg", "inc_sfr_deg"):
    Sx, _, _ = C.load(col); r = survive(Sx); res["c3"][col] = r
    pr("  %-14s D'=%+.4f z=%+.2f mu_be %s survive=%s" % (col, r["d"], r["z"], r["be"], r["surv"]))
pr("c2 KROSS and the two-epoch consistency (T):")
dK0 = dsig(S, 0.0, 0.67, T, "H"); dR0 = dsig(K, 0.0, 0.67, T, "H"); dK1 = dsig(S, 1.0, 0.67, T, "H"); dR1 = dsig(K, 1.0, 0.67, T, "H")
res["c2"] = {"K0": dK0, "R0": dR0, "K1": dK1, "R1": dR1}
pr("  KURVS  P0 %+.4f+-%.4f (z %+.2f) | s=1 %+.4f+-%.4f (z %+.2f)" % (*dK0, dK0[0] / dK0[1], *dK1, dK1[0] / dK1[1]))
pr("  KROSS  P0 %+.4f+-%.4f (z %+.2f) | s=1 %+.4f+-%.4f (z %+.2f)" % (*dR0, dR0[0] / dR0[1], *dR1, dR1[0] / dR1[1]))
for nm, a, b in (("P0", dK0, dR0), ("s=1", dK1, dR1)):
    D = a[0] - b[0]; sD = math.hypot(a[1], b[1])
    pr("  D_T = D'_KURVS - D'_KROSS at %s (mu=0.67 both): %+.4f +- %.4f  (%.2f sigma from 0)" % (nm, D, sD, D / sD)); res["c2"]["D_" + nm] = (D, sD)
beK0, beR0 = BE[("T", 0.0)], C.breakeven(lambda m: dsig(K, 0.0, m, T, "H"))
def lnsig(be): return math.log(be["hi"] / be["lo"]) / 2
RT0 = beK0["mu"] / beR0["mu"]; sl = math.hypot(lnsig(beK0), lnsig(beR0))
res["c2"]["RT0"] = (RT0, sl)
pr("  R_T(P0) = %.3f, sigma_ln %.3f -> 1sigma [%.2f, %.2f]" % (RT0, sl, RT0 * math.exp(-sl), RT0 * math.exp(sl)))
for nm, (lo, hi) in (("in-repo PHIBSS [0.73,1.39]", (0.73, 1.39)), ("literature [1.61,2.42]", (1.61, 2.42))):
    edge = hi if RT0 > hi else (lo if RT0 < lo else RT0)
    zz = abs(math.log(RT0 / edge)) / sl
    pr("   vs %s: nearest edge %.2f at %.2f sigma_ln %s" % (nm, edge, zz, "(inside)" if lo <= RT0 <= hi else ""))
    res["c2"]["RT_vs_" + nm] = zz
pr("  KROSS at P0, mu=0.67: T over-predicts by %.1f sigma; KROSS mu_be(P0)=%s" % (-dR0[0] / dR0[1], C.fmt_be(beR0)))
pr("  common-gas joint chi2 of the two anchored levels at mu=0.67 (T): P0 %.1f, s=1 %.1f, s=0.26 %.1f" % (
    (dK0[0] / dK0[1]) ** 2 + (dR0[0] / dR0[1]) ** 2, (dK1[0] / dK1[1]) ** 2 + (dR1[0] / dR1[1]) ** 2,
    (lambda a, b: (a[0] / a[1]) ** 2 + (b[0] / b[1]) ** 2)(dsig(S, 0.26, 0.67, T, "H"), dsig(K, 0.26, 0.67, T, "H"))))
pr("  same, flat at s=1: %.2f ; rival s=1: %.2f" % ((lambda a, b: (a[0] / a[1]) ** 2 + (b[0] / b[1]) ** 2)(dsig(S, 1.0, 0.67, None, "flat"), dsig(K, 1.0, 0.67, None, "flat")),
                                                    (lambda a, b: (a[0] / a[1]) ** 2 + (b[0] / b[1]) ** 2)(dsig(S, 1.0, 0.67, None, "H"), dsig(K, 1.0, 0.67, None, "H"))))
meta = C.kross_meta()
kt = np.array([meta[n]["kin_type"] for n in K.ids]); ba = np.array([float(meta[n]["b_over_a"]) for n in K.ids])
vs = K.V / K.sig0
variants = {"all": np.ones(len(K.z), bool), "RT only": kt == "RT", "RT+ only": kt == "RT+", "v/sig0>=2": vs >= 2, "v/sig0>=3": vs >= 3,
            "log M* in KURVS range [9.55,10.68]": (K.logM >= 9.55) & (K.logM <= 10.68), "b/a>0.5": ba > 0.5, "z<0.85": K.z < 0.85, "z>=0.85": K.z >= 0.85}
res["c2_sub"] = {}
pr("  KROSS sub-samples (kin_type counts %s):" % dict(zip(*np.unique(kt, return_counts=True))))
for nm, m in variants.items():
    Ks = C.subset(K, np.where(m)[0]); n = int(m.sum())
    if n < 5: pr("   %-38s n=%d SKIPPED" % (nm, n)); continue
    a0 = dsig(Ks, 0.0, 0.67, T, "H"); a1 = dsig(Ks, 1.0, 0.67, T, "H"); af = dsig(Ks, 1.0, 0.67, None, "flat")
    b0 = C.fast_be(lambda mu: dsig(Ks, 0.0, mu, T, "H"), edges=False); b1 = C.fast_be(lambda mu: dsig(Ks, 1.0, mu, T, "H"), edges=False)
    res["c2_sub"][nm] = dict(n=n, P0=a0, s1=a1, flat_s1=af, be0=b0["mu"], be1=b1["mu"])
    pr("   %-38s n=%3d  T P0 %+.3f (z %+.1f) mu_be %s | T s=1 %+.3f (z %+.1f) mu_be %s | flat s=1 %+.3f" % (nm, n, a0[0], a0[0] / a0[1], "%.3f" % b0["mu"] if b0["mu"] else b0["note"], a1[0], a1[0] / a1[1], "%.3f" % b1["mu"] if b1["mu"] else b1["note"], af[0]))
pr("c4 KURVS sub-sample: leave-one-out (T; also flat and rival at P0)")
res["c4_loo"] = {}
n = len(S.z)
nex = 0; pfit = 0
for i in range(n):
    idx = [j for j in range(n) if j != i]; Sx = C.subset(S, idx)
    d0 = dsig(Sx, 0.0, 0.67, T, "H"); df = dsig(Sx, 0.0, 0.67, None, "flat"); dr = dsig(Sx, 0.0, 0.67, None, "H")
    b0 = C.fast_be(lambda m: dsig(Sx, 0.0, m, T, "H")); b1 = C.fast_be(lambda m: dsig(Sx, 1.0, m, T, "H"))
    ex = b1["lo"] is not None and b1["lo"] > C.CEIL
    sv = abs(d0[0] / d0[1]) < 2 and b0["mu"] is not None and b0["lo"] <= 1.69 and b0["hi"] >= 0.6
    nex += ex; pfit += sv
    res["c4_loo"][S.name[i]] = dict(zT0=d0[0] / d0[1], zf0=df[0] / df[1], zr0=dr[0] / dr[1], be0=b0["mu"], be1=b1["mu"], lo1=b1["lo"], excl_s1=bool(ex), survive=bool(sv))
    pr("  drop %-9s T P0 %+.3f (z %+.2f) mu_be(P0) %.3f | mu_be(s=1) %.3f lower edge %.3f -> %s | flat P0 z %+.1f rival P0 z %+.1f | P0 survive %s" % (S.name[i], d0[0], d0[0] / d0[1], b0["mu"], b1["mu"], b1["lo"], "excluded" if ex else "ALLOWED", df[0] / df[1], dr[0] / dr[1], sv))
pr("  LOO: s=1 exclusion kept in %d of %d ; P0 survival kept in %d of %d" % (nex, n, pfit, n))
res["c4_loo_summary"] = (nex, pfit, n)
pr("c4 bootstrap of the ten discs (N=2000, seed 183): T P0 D', mu_be(P0), lower edge at s=1")
rng = np.random.default_rng(183)
N = 2000; dd = np.zeros(N); b0m = np.full(N, np.nan); lo1 = np.full(N, np.nan); okp0 = np.zeros(N, bool); exc = np.zeros(N, bool)
for k in range(N):
    idx = rng.integers(0, n, n); Sx = C.subset(S, idx)
    d0 = dsig(Sx, 0.0, 0.67, T, "H"); dd[k] = d0[0]
    b0 = C.fast_be(lambda m: dsig(Sx, 0.0, m, T, "H"), edges=False); b0m[k] = b0["mu"] if b0["mu"] else np.nan
    z3 = dsig(Sx, 1.0, C.CEIL, T, "H"); exc[k] = z3[0] / z3[1] > 1.0      # lower edge > ceiling  <=>  D'(ceiling) > +sigma
    okp0[k] = abs(d0[0] / d0[1]) < 2
pctl = lambda x: np.nanpercentile(x, [16, 50, 84])
res["c4_boot"] = dict(dP0=pctl(dd).tolist(), mu_be_P0=pctl(b0m).tolist(), frac_excluded_s1=float(exc.mean()), frac_P0_within2=float(okp0.mean()))
pr("  D'_T(P0): 16/50/84 = %s ; mu_be(P0) 16/50/84 = %s" % (np.round(pctl(dd), 3), np.round(pctl(b0m), 3)))
pr("  fraction of resamples with T's s=1 label 'excluded' (D'(3.47) > +sigma): %.3f ; with |z_T(P0)|<2: %.3f ; with mu_be(P0) in [0.60,1.69]: %.3f" % (exc.mean(), okp0.mean(), np.nanmean((b0m >= 0.6) & (b0m <= 1.69))))
pr("c4b flagged-sub-sample split (partition fixed by the sigma methods note: flagged A = KURVS 15,16,17,21 ; U = 3,7,8,9,11,13)")
A = [i for i, x in enumerate(S.ids) if x in (4, 5, 6, 10, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22)]
U = [i for i in range(n) if i not in A]
res["c4b"] = {}
for nm, idx in (("A flagged", A), ("U unflagged", U), ("all", list(range(n)))):
    Sx = C.subset(S, idx)
    d0 = dsig(Sx, 0.0, 0.67, T, "H"); df = dsig(Sx, 0.0, 0.67, None, "flat"); dr = dsig(Sx, 0.0, 0.67, None, "H")
    b0 = C.fast_be(lambda m: dsig(Sx, 0.0, m, T, "H")); b1 = C.fast_be(lambda m: dsig(Sx, 1.0, m, T, "H"))
    ex = b1["lo"] is not None and b1["lo"] > C.CEIL
    res["c4b"][nm] = dict(ids=[S.ids[i] for i in idx], zT0=d0[0] / d0[1], dT0=d0[0], be0=b0["mu"], lo0=b0["lo"], hi0=b0["hi"], be1=b1["mu"], lo1=b1["lo"], excl=bool(ex), zf0=df[0] / df[1], zr0=dr[0] / dr[1])
    pr("  %-12s ids %s n=%d: T P0 D' %+.3f (z %+.2f) mu_be(P0) %.3f [%.3f, %.3f] | s=1 mu_be %.3f lower %.3f %s | flat P0 z %+.2f rival P0 z %+.2f" % (nm, [S.ids[i] for i in idx], len(idx), d0[0], d0[0] / d0[1], b0["mu"], b0["lo"], b0["hi"], b1["mu"], b1["lo"], "excluded" if ex else "ALLOWED", df[0] / df[1], dr[0] / dr[1]))
robust1 = all(v["survive"] for v in res["c4_loo"].values()) and all(v["surv"] for v in res["c1"].values())
pr("verdicts: P0 fit ROBUST (survival in all c1 rows and all ten LOO)? %s" % robust1)
pr("          s=1 exclusion ROBUST (>=90%% of bootstrap and all ten LOO keep it)? %s (bootstrap %.3f, LOO %d/%d)" % (bool(exc.mean() >= 0.9 and nex == n), exc.mean(), nex, n))
pr("          KROSS-CONSISTENT (R_T(P0) 1sigma overlaps in-repo bracket)? %s" % (RT0 * math.exp(-sl) <= 1.39))
json.dump(jfix(res), open(os.path.join(C.HERE, "CFG183_attacks_abc_results.json"), "w"), indent=1)
