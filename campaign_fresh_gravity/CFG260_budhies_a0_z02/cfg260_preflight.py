#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG260 PRE-FLIGHT v2 (mocks only; reads NO HI line width): what the BUDHIES completeness-limited primary set PC could say about the implied a0 at z ~ 0.2, and whether FLAT can be told from a0 ~ H(z).
Frozen criteria: FROZEN_CRITERIA.md (00f20121d) + Addendum 1 (2b8a8e4c7) + Addendum 2 (committed before this run; it follows the FIRST run, kept as cfg260_preflight_v1.*).
The real inputs are the non-width columns (z, D_L, M_HI, S_int, B, R, membership, R_proj, beam position); the widths are MOCK.  The loader (cfg260_core.load_galaxies) cannot return a width unless widths=True,
which only the measurement script passes.  kappa = 1/2 FITTED; no sentence says the data favour a law.
Run: CFG260_SET=PC python3 cfg260_preflight.py  (also PC125 and P; ~3 min) | MUTATE=1 (s_true = 2) / 2 (truth rest-frame, analyst observed-frame) / 3 (analyst sin i_eff 0.70)  python3 cfg260_preflight.py
Exit: main 0 (1 if a control fails); MUTATE exits 1 when the control BITES.
"""
import os, sys, json, math, time, zlib
sys.dont_write_bytecode = True
import numpy as np
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg260_core as C

MUT = os.environ.get("MUTATE", "").strip()
SETKEY = os.environ.get("CFG260_SET", "PC").strip()
SFX = f"_{SETKEY}" + (f"_MUTATE{MUT}" if MUT else "")
T0 = time.time()
LOG = []


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


CK = []
RES = {}


def check(name, detail, ok, kind="control"):
    CK.append(dict(name=name, detail=detail, ok=bool(ok), kind=kind))
    P(f"  [{'PASS' if ok else 'FAIL'}] ({kind}) {name}\n         {detail}")


def jc(o):
    if isinstance(o, dict):
        return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, np.generic):
        return o.item()
    if isinstance(o, np.ndarray):
        return jc(o.tolist())
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


def finish():
    RES["checks"] = CK; RES["seconds"] = round(time.time() - T0, 1); RES["set"] = SETKEY
    json.dump(jc(RES), open(os.path.join(HERE, f"cfg260_preflight{SFX}_results.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg260_preflight{SFX}.out"), "w").write("\n".join(LOG) + "\n")


P(__doc__.split("Run: ")[0].strip())
P(f"\n  mode: {'MUTATE=' + MUT if MUT else 'main'}; primary set under test: {SETKEY} ({C.SUBSET_LABEL[SETKEY]})")

# ================================================================================================ the real non-width inputs
GALS = C.load_galaxies(widths=False)
PRIM = C.select(GALS, SETKEY)
A = C.Arr(PRIM)
NU, A0 = C.NU, C.A0["canonical"]
REC0 = dict(C.REC0)
BUDGET = {"A": dict(tau_ms=0.10, tau_gas=0.05, tau_w=5.0, tau_i=0.02, tau_r=0.05, tau_d=0.02),
          "B": dict(tau_ms=0.25, tau_gas=0.15, tau_w=12.0, tau_i=0.06, tau_r=0.15, tau_d=0.06)}
SINI60 = REC0["sini"]
FAC_RIVAL = np.array([C.E(float(z)) for z in A.z])
FDET = {"none": None, "f1": 1.0, "f1.25": 1.25, "f1.5": 1.5, "f2": 2.0}
F_PRIM, F_CTRL = "f1.25", "f1"


# ================================================================================================ the mock generator (FROZEN_CRITERIA section 4 + Addenda 1 and 2)
def gen_W(M, rng, s_true, F, level, f_det, k_true=1, noise=20.0, plant_tau_b=0.0, sini_fixed=None, scatter=True):
    """mock tabulated widths (M, n): truth from the RAR with scale a0 s_true F, per-galaxy scatter, random inclination CONDITIONED on detection at the galaxy's beam position, shared systematics at `level`"""
    n = A.n
    keys = tuple(BUDGET["A"])
    sh = {k: (rng.normal(0.0, BUDGET[level][k] / 2, size=M) if level else np.zeros(M)) for k in keys}
    sh["tau_ms"] = sh["tau_ms"] + plant_tau_b; sh["tau_gas"] = sh["tau_gas"] + plant_tau_b
    e1, e2, e3 = ((rng.normal(0, s, (M, n)) if scatter else np.zeros((M, n))) for s in (0.15, 0.06, 0.03))
    rt = dict(REC0)
    rt.update(tau_ms=sh["tau_ms"][:, None], tau_gas=sh["tau_gas"][:, None], rdex=sh["tau_r"][:, None], hubble=C.H0_TAB / (1.0 + sh["tau_d"][:, None]))
    Mgas, Mstar, Mb, R = C.baryons(A, rt, eps_ms=e1, eps_r=e2)
    gb = C.G * Mb * C.MSUN / R ** 2
    go = gb * C.nuv(NU, gb / (A0 * s_true * F))
    V = np.sqrt(go * R) * 10 ** e3 / 1e3                                                         # km/s
    fac = (1 + A.z) ** k_true
    dtrue = REC0["delta"] + sh["tau_w"][:, None]
    tw = (1 + sh["tau_i"][:, None])

    def Wt(sini):
        return 2 * V * sini * tw * fac + dtrue
    sini = np.full((M, n), sini_fixed) if sini_fixed is not None else np.sqrt(1 - rng.uniform(0, 1, (M, n)) ** 2)
    W = Wt(sini)
    if f_det is not None and sini_fixed is None:
        thr = f_det * A.spk_thr
        rej = (A.sint / W < thr); it = 0
        while rej.any() and it < 400:
            sn = np.sqrt(1 - rng.uniform(0, 1, (M, n)) ** 2)
            sini = np.where(rej, sn, sini); W = Wt(sini)
            rej = (A.sint / W < thr); it += 1
        if rej.any():
            sini = np.where(rej, 1e-3, sini); W = Wt(sini)
    return W + (rng.normal(0, noise, (M, n)) if noise else 0.0)


def batch_s(W, rec):
    """log10 s* per mock for the analyst's recipe `rec` (NaN widths ignored)"""
    d = C.derive(A, W, rec)
    D = np.where(d["ok"], d["D"], np.nan)
    l, u = C.implied(D, d["gb"], C.kernel_of(rec), A0)
    return l, u, d


def stats(l):
    return dict(median=float(np.median(l)), mean=float(np.mean(l)), sd=float(np.std(l, ddof=1)), p5=float(np.percentile(l, 5)), p95=float(np.percentile(l, 95)))


def rng_for(*tag):
    return np.random.default_rng(np.random.SeedSequence([260] + [int(t) for t in tag]))


def seed_of(*names):
    return zlib.crc32("|".join(names).encode())


REC_AN = dict(REC0)
if MUT == "3":
    REC_AN["sini"] = 0.70
K_TRUE = 0 if MUT == "2" else 1

# ================================================================================================ controls on the real non-width inputs
P("\n" + "=" * 110 + "\nCONTROLS (inputs)\n" + "=" * 110)
cnt = {}
for cl in C.CL:
    mem = [g for g in GALS if g["cl"] == cl and g["mem"]]
    cnt[cl] = (len(mem), sum(1 for g in mem if g["R"] < 1.0), sum(1 for g in mem if g["R"] < 2.0))
check("C1 CONTROL: membership (CFG212's rule and constants) reproduces CFG212's counts: A963 94 / 8 / 30, A2192 24 / 3 / 8 (members / < 1 Mpc / < 2 Mpc)", str(cnt),
      cnt["A963"] == (94, 8, 30) and cnt["A2192"] == (24, 3, 8))
dd = max(abs(g["dl"] / C.DL_mpc(g["z"]) - 1) for g in GALS)
check("C2 CONTROL: the table's D_L equals flat LCDM (H0 70, Om 0.3) to 0.5 %", f"max |D_L / D_L(z) - 1| = {dd:.4f}", dd < 0.005)
kk = np.array([g["mhi"] / (2.356e5 * g["dl"] ** 2 * g["sint"] / 1e3) * (1 + g["z"]) for g in GALS])
check("C3 CONTROL: M_HI x (1+z) / (2.356e5 D_L^2 S_int) in [0.99, 1.01] for every galaxy (S_int is in observed-frame velocity units: the frame evidence)", f"range {kk.min():.4f} to {kk.max():.4f}", kk.min() > 0.99 and kk.max() < 1.01)
src = open(__file__).read().lower()
_PARTS = ("w" + "20", "w" + "50")                                              # built from pieces: this source must not contain the literal column names
n_hits = sum(src.count(p) for p in _PARTS)
loader_keys = set(GALS[0].keys())
bad_keys = [k for k in loader_keys if any(p in k.lower() for p in _PARTS)]
check("C6 CONTROL (blind loader): the loader returns no width key, and this pre-flight's source contains the width column names nowhere (they live only in cfg260_core's forbidden list)",
      f"keys {sorted(loader_keys)}; width-like keys {bad_keys}; occurrences of the width column names in this source: {n_hits}", not bad_keys and n_hits == 0)
nPC = len(C.select(GALS, "PC"))
check("C9 CONTROL (Addendum 2 counts, non-width): the completeness-limited sets have the sizes the addendum states (PC 32, PC125 13, PC15 7)", f"PC {nPC}, PC125 {len(C.select(GALS, 'PC125'))}, PC15 {len(C.select(GALS, 'PC15'))}",
      nPC == 32 and len(C.select(GALS, "PC125")) == 13 and len(C.select(GALS, "PC15")) == 7)

# ================================================================================================ what the real inputs say (no width)
P("\n" + "=" * 110 + "\nTHE REAL NON-WIDTH INPUTS\n" + "=" * 110)
sub_n = {k: len(C.select(GALS, k)) for k in C.SUBSETS}
P("  subset sizes: " + "; ".join(f"{k} {v}" for k, v in sub_n.items()))
Mgas, Mstar, Mb, R = C.baryons(A, REC0)
y = (C.G * Mb * C.MSUN / R ** 2) / A0
qs = (5, 25, 50, 75, 95)
P(f"  {SETKEY}: N = {A.n}; log M_HI quantiles {np.round(np.log10(np.percentile(A.mhi, qs)), 2).tolist()}; log M* {np.round(np.log10(np.percentile(Mstar, qs)), 2).tolist()}; M*/M_gas median {float(np.median(Mstar / Mgas)):.2f}")
P(f"  y = g_bar/a0 at R_HI quantiles {np.round(np.percentile(y, qs), 3).tolist()}; fraction y < 0.3: {float((y < 0.3).mean()):.3f}; y < 0.1: {float((y < 0.1).mean()):.3f}; z median {float(np.median(A.z)):.3f} (range {A.z.min():.3f}-{A.z.max():.3f}); "
  f"completeness ratio c median {float(np.median([g['c'] for g in PRIM])):.2f}; beam attenuation median {float(np.median(A.pb)):.2f}; cluster members {sum(1 for g in PRIM if g['mem'])}, field {sum(1 for g in PRIM if not g['mem'])}")
RES["inputs"] = dict(N=A.n, subsets=sub_n, y_q=np.percentile(y, qs), frac_y03=float((y < 0.3).mean()), frac_y01=float((y < 0.1).mean()), z_med=float(np.median(A.z)), ms_over_mg=float(np.median(Mstar / Mgas)))

# ================================================================================================ C4 / C5: the estimator
P("\n" + "=" * 110 + "\nCONTROLS (estimator)\n" + "=" * 110)
W0 = gen_W(1, rng_for(1), 1.0, 1.0, None, None, 1, noise=0.0, sini_fixed=SINI60, scatter=False)[0]
l0, u0, _ = batch_s(W0[None, :], REC0)
Wr = gen_W(1, rng_for(2), 1.0, FAC_RIVAL, None, None, 1, noise=0.0, sini_fixed=SINI60, scatter=False)[0]
lr, ur, dr = batch_s(Wr[None, :], REC0)
from scipy.optimize import brentq
okr = dr["ok"][0]
fcond = lambda ls: float(np.median(np.log10(dr["D"][0][okr]) - np.log10(C.nuv(NU, dr["gb"][okr] / (A0 * 10 ** ls)))))
lb_ = brentq(fcond, -3, 3, xtol=1e-14, rtol=1e-14)
check("C4 CONTROL (noiseless identity): known inclination, no scatter or selection, nominal recipe: s* = s_true to 1e-6 for F = 1; for the RIVAL a value in [min F, max F] equal to an independent brentq of the median condition to 1e-9",
      f"FLAT: log10 s* = {float(l0[0]):+.2e}; RIVAL: s* = {10 ** float(lr[0]):.4f} (F in [{FAC_RIVAL.min():.4f}, {FAC_RIVAL.max():.4f}]), brentq difference {abs(float(lr[0]) - lb_):.1e}",
      abs(float(l0[0])) < 1e-6 and FAC_RIVAL.min() <= 10 ** float(lr[0]) <= FAC_RIVAL.max() and abs(float(lr[0]) - lb_) < 1e-9)
RES["noiseless"] = dict(flat=float(l0[0]), rival_s=10 ** float(lr[0]))
S_RIVAL_NL = float(lr[0])
src223 = open(os.path.join(C.LANES, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read()
i0 = src223.index("def implied("); i1 = src223.index("_IDX = {}")
ns = {"np": np, "nuv": C.nuv, "LO_LS": C.LO_LS, "HI_LS": C.HI_LS, "NIT": C.NIT}
exec(compile(src223[i0:i1], "cfg223_implied", "exec"), ns)
rt_ = np.random.default_rng(5); Dt = 10 ** rt_.normal(0.6, 0.3, (4, 60)); gt = 10 ** rt_.normal(-11.0, 0.3, (4, 60))
a1, _ = ns["implied"](Dt, gt, NU, A0); a2, _ = C.implied(Dt, gt, NU, A0)
check("C5 CONTROL: the solver equals CFG223's `implied` (exec'd from its source) on a test vector to 1e-12", f"max |d| = {float(np.max(np.abs(a1 - a2))):.1e}", float(np.max(np.abs(a1 - a2))) < 1e-12)

# ================================================================================================ the noiseless levers and the aligned worst case
P("\n" + "=" * 110 + "\nNOISELESS LEVERS (analyst's knobs on the identity sample; dex of log10 s* per knob step)\n" + "=" * 110)


def s_at(rec):
    return float(batch_s(W0[None, :], rec)[0][0])


LEV = {}
lev_b = (s_at(dict(REC0, tau_b=0.15)) - s_at(dict(REC0, tau_b=-0.15))) / 0.30
LEV["baryon_per_dex"] = lev_b
P(f"  baryon lever: d log10 s* / d(dex of the analyst's baryon masses) = {lev_b:+.3f}   (1 - 1/eta = -1.33 at y ~ 0.09; -1 in the deep limit)")
l_k0 = s_at(dict(REC0, k=0)); LEV["frame"] = l_k0
P(f"  frame lever: analyst k = 0 on observed-frame widths: {l_k0:+.3f} dex  (the analyst of the other frame reads s* higher by this; the misreading the other way is the negative)")
half = {}
for lv in ("A", "B"):
    b = BUDGET[lv]
    sh = {}
    sh["tau_ms"] = max(abs(s_at(dict(REC0, tau_ms=+b["tau_ms"]))), abs(s_at(dict(REC0, tau_ms=-b["tau_ms"]))))
    sh["tau_gas"] = max(abs(s_at(dict(REC0, tau_gas=+b["tau_gas"]))), abs(s_at(dict(REC0, tau_gas=-b["tau_gas"]))))
    sh["tau_w"] = max(abs(s_at(dict(REC0, delta=REC0["delta"] + b["tau_w"]))), abs(s_at(dict(REC0, delta=REC0["delta"] - b["tau_w"]))))
    sh["tau_i"] = max(abs(s_at(dict(REC0, sini=SINI60 * (1 + b["tau_i"])))), abs(s_at(dict(REC0, sini=SINI60 * (1 - b["tau_i"])))))
    sh["tau_r"] = max(abs(s_at(dict(REC0, rdex=+b["tau_r"]))), abs(s_at(dict(REC0, rdex=-b["tau_r"]))))
    sh["tau_d"] = max(abs(s_at(dict(REC0, hubble=C.H0_TAB / (1 + b["tau_d"])))), abs(s_at(dict(REC0, hubble=C.H0_TAB / (1 - b["tau_d"])))))
    half[lv] = sh
    P(f"  level {lv}: |shift| at the half-range: " + ", ".join(f"{k} {v:.3f}" for k, v in sh.items()) + f"  -> aligned worst case S_joint = {sum(sh.values()):.3f} dex")
S_JOINT = {lv: float(sum(v.values())) for lv, v in half.items()}
RES["levers"] = dict(LEV, half=half, S_joint=S_JOINT)
rows, hrec, single = C.recipe_band(A, W0, REC0)
P("  recipe-band knobs on the identity sample (frozen brackets; half-difference of log10 s*): " + "; ".join(f"{v['label']} {v['half']:.3f}" for v in rows.values()) + f"  -> quadrature half-width {hrec:.3f} dex")
P("  singly reported: " + "; ".join(f"{k} {v:+.3f}" for k, v in single.items()))
RES["recipe_band_noiseless"] = dict(rows=rows, half=hrec, single=single)

# ================================================================================================ the mock campaign
P("\n" + "=" * 110 + f"\nMOCK CAMPAIGN (M = 2,000 mocks per cell; analyst = nominal recipe{' with sin i_eff 0.70 (MUTATE=3)' if MUT == '3' else ''}; truth frame k = {K_TRUE}; detection at the galaxy's beam position, f x threshold)\n" + "=" * 110)
M = 2000
SC = {"FLAT": (1.0, 1.0, 0.0), "s2": (2.0, 1.0, math.log10(2.0)), "s0.5": (0.5, 1.0, math.log10(0.5)), "RIVAL": (1.0, FAC_RIVAL, S_RIVAL_NL)}
LV_ = {"none": None, "A": "A", "B": "B"}
CAMP = {}
t1 = time.time()
if not MUT:
    cells = [("FLAT", fk, lk) for fk in FDET for lk in LV_] + [("RIVAL", fk, lk) for fk in FDET for lk in LV_] + [("s2", F_PRIM, "none"), ("s0.5", F_PRIM, "none")] + [("s2", "f1", "none"), ("s0.5", "f1", "none")]      # the f = 1 cells of s_true = 2 and 0.5 were added AFTER MUTATE=1 did not bite at f = 1.25 (post hoc, labelled)
elif MUT == "1":
    cells = [("FLAT", F_PRIM, "none"), ("s2", F_PRIM, "none"), ("RIVAL", F_PRIM, "none"), ("RIVAL", F_PRIM, "B"), ("FLAT", F_PRIM, "B")]
else:
    cells = [("FLAT", F_PRIM, "none")]
for sc, fk, lk in cells:
    s_true, F, ltruth = SC[sc]
    W = gen_W(M, rng_for(10, seed_of(sc, fk, lk)), s_true, F, LV_[lk], FDET[fk], k_true=K_TRUE)         # the seed depends only on the cell's name: a MUTATE cell is paired with the main run's cell
    l, u, d = batch_s(W, REC_AN)
    st = stats(l); st["bias_median"] = st["median"] - ltruth; st["unb"] = float(np.mean(u)); st["truth"] = ltruth
    CAMP[(sc, fk, lk)] = st
P(f"  {len(cells)} cells in {time.time() - t1:.0f} s")
RES["campaign"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in CAMP.items()}

if not MUT:
    P(f"\n  {'truth':6s} {'selection':9s} {'shared':6s} | {'median bias':>11s} {'SD':>7s} {'P5':>8s} {'P95':>8s}   (log10 s* minus the truth value, dex)")
    for (sc, fk, lk), st in CAMP.items():
        if sc in ("FLAT", "RIVAL"):
            P(f"  {sc:6s} {fk:9s} {lk:6s} | {st['bias_median']:+11.3f} {st['sd']:7.3f} {st['p5'] - st['truth']:+8.3f} {st['p95'] - st['truth']:+8.3f}")
    P("  (the s_true = 2 and 0.5 cells at the primary detection scenario f = 1.25: " + "; ".join(f"{sc} median bias {CAMP[(sc, F_PRIM, 'none')]['bias_median']:+.3f}, SD {CAMP[(sc, F_PRIM, 'none')]['sd']:.3f}" for sc in ("s2", "s0.5")) + ")")
    P("  (POST HOC, added after MUTATE=1 did not bite at f = 1.25: the same cells at f = 1: " + "; ".join(f"{sc} median bias {CAMP[(sc, 'f1', 'none')]['bias_median']:+.3f}, SD {CAMP[(sc, 'f1', 'none')]['sd']:.3f}" for sc in ("s2", "s0.5")) + ")")

# ================================================================================================ BTFR route, coverage (C7) and reactivity (C8) at the complete scenario f = 1
if not MUT:
    Wb = gen_W(400, rng_for(20), 1.0, 1.0, None, FDET[F_CTRL])
    d_ = C.derive(A, Wb, REC0)
    lbtfr = np.array([np.log10(np.nanmedian(d_["V"][m][d_["ok"][m]] ** 4 / (C.G * d_["Mb"][d_["ok"][m]] * C.MSUN)) / A0) for m in range(Wb.shape[0])])
    lrar, _, _ = batch_s(Wb, REC0)
    P(f"\n  BTFR-route (V^4 / G M_b) minus the RAR-at-R_HI route, same mocks (FLAT, f = 1): median {float(np.median(lbtfr - lrar)):+.3f} dex (the regime effect y nu^2 at y ~ 0.05-0.2)")
    RES["btfr_minus_rar"] = float(np.median(lbtfr - lrar))
    K_COV, B_COV = 300, 1000
    Wc = gen_W(K_COV, rng_for(30), 1.0, 1.0, None, FDET[F_CTRL])
    dcov = C.derive(A, Wc, REC0)
    COV_D = np.where(dcov["ok"], dcov["D"], np.nan); COV_G = dcov["gb"]

    def cov_one(m):
        ok = ~np.isnan(COV_D[m])
        r_, lb2, I_ = C.boot_interval(COV_D[m][ok], COV_G[ok], NU, A0, B=B_COV, tag=m)
        return (r_["lo68"] <= 1.0 <= r_["hi68"], r_["lo95"] <= 1.0 <= r_["hi95"], r_["sd_log"])
    ctx = get_context("fork")
    with ctx.Pool(12) as pool:
        cov = pool.map(cov_one, range(K_COV))
    c68, c95, sdb = float(np.mean([c[0] for c in cov])), float(np.mean([c[1] for c in cov])), float(np.median([c[2] for c in cov]))
    check(f"C7 CONTROL (bootstrap coverage on FLAT mocks at f = 1, {SETKEY}, K = 300, B = 1,000): the 68 % interval covers in [0.55, 0.80], the 95 % interval in >= 0.88", f"68%: {c68:.3f}, 95%: {c95:.3f}; median bootstrap SD of log10 s*: {sdb:.3f}",
          0.55 <= c68 <= 0.80 and c95 >= 0.88)
    RES["coverage"] = dict(c68=c68, c95=c95, sd_boot_median=sdb)
    base = CAMP[("FLAT", F_CTRL, "none")]
    Wp = gen_W(M, rng_for(10, seed_of("FLAT", F_CTRL, "none")), 1.0, 1.0, None, FDET[F_CTRL], plant_tau_b=0.15)
    lp, _, _ = batch_s(Wp, REC0)
    shift = float(np.median(lp)) - base["median"]
    exp_shift = -LEV["baryon_per_dex"] * 0.15                         # the analyst UNDER-estimates the baryons by 0.15 dex
    cont = 0
    for m in range(0, 200):
        bb = C.baryon_bands(A, Wp[m], REC0)
        lo, hi = min(bb[-0.30][0], bb[0.30][0]), max(bb[-0.30][0], bb[0.30][0])
        cont += (lo <= 1.0 <= hi)
    sdB = CAMP[("FLAT", F_CTRL, "B")]["sd"]
    check(f"C8 CONTROL (reactivity, the CFG219 / CFG258 lesson; {SETKEY}, f = 1): a planted shared baryon offset of +0.15 dex shifts the median s* by the noiseless lever x 0.15 (within 20 %), the analyst's +-0.30 dex baryon band contains s_true in >= 95 % of mocks, and the level-B total SD exceeds the within-mock bootstrap SD by >= 1.5",
          f"shift {shift:+.3f} vs lever x 0.15 = {exp_shift:+.3f}; outer-band containment {cont / 200:.3f}; level-B SD {sdB:.3f} vs bootstrap SD {sdb:.3f} (ratio {sdB / sdb:.2f})",
          abs(shift - exp_shift) <= 0.2 * abs(exp_shift) and cont / 200 >= 0.95 and sdB >= 1.5 * sdb)
    RES["reactivity"] = dict(shift=shift, expected=exp_shift, containment=cont / 200, sd_B=sdB, sd_boot=sdb)

# ================================================================================================ decisions
if not MUT:
    P("\n" + "=" * 110 + f"\nDECISIONS (frozen section 4 with Addendum 2: primary detection scenario {F_PRIM})\n" + "=" * 110)
    fl, ri = CAMP[("FLAT", F_PRIM, "none")], CAMP[("RIVAL", F_PRIM, "none")]
    delta_nl = ri["median"] - fl["median"]
    sd_stat = fl["sd"]
    out_d1 = {}
    for lv in ("A", "B"):
        flv, riv = CAMP[("FLAT", F_PRIM, lv)], CAMP[("RIVAL", F_PRIM, lv)]
        r1 = riv["p5"] > flv["p95"]
        r2 = delta_nl > S_JOINT[lv] + 2 * sd_stat
        out_d1[lv] = dict(R1=bool(r1), R2=bool(r2), sd_tot=flv["sd"], p5_rival=riv["p5"], p95_flat=flv["p95"], S_joint=S_JOINT[lv])
        P(f"  level {lv}: SD_tot (FLAT mocks) {flv['sd']:.3f} dex; P5[RIVAL] {riv['p5']:+.3f} vs P95[FLAT] {flv['p95']:+.3f} -> R1 {r1}; Delta (RIVAL - FLAT, no shared) {delta_nl:+.3f} vs S_joint {S_JOINT[lv]:.3f} + 2 SD_stat {2 * sd_stat:.3f} -> R2 {r2}")
    pf1 = "POSSIBLE" if (out_d1["B"]["R1"] and out_d1["B"]["R2"]) else "NOT POSSIBLE"
    sdBB = CAMP[("FLAT", F_PRIM, "B")]["sd"]
    P(f"  PF-D1 (FLAT vs a0 ~ H(z) at z ~ 0.2): {pf1}   [required total precision Delta / 3.29 = {delta_nl / 3.29:.3f} dex; stat-only separation {delta_nl / sd_stat:.2f} sigma; level-B separation {delta_nl / sdBB:.2f} sigma]")
    b1, b125 = CAMP[("FLAT", "f1", "none")]["bias_median"], CAMP[("FLAT", "f1.25", "none")]["bias_median"]
    n_ok = A.n >= 25; b_ok = abs(b1) <= 0.10 and abs(b125) <= 0.10; s_ok = sd_stat <= 0.20; y_ok = float((y < 0.3).mean()) >= 0.80
    pf2 = "DRAWABLE" if (n_ok and b_ok and s_ok and y_ok) else "NOT DRAWABLE"
    P(f"  PF-D2 (is a coverage point drawable? Addendum 2): {pf2}   [N = {A.n} (>= 25: {n_ok}); |median bias| at f = 1 {abs(b1):.3f} and f = 1.25 {abs(b125):.3f} (<= 0.10: {b_ok}); SD_stat at f = 1.25 {sd_stat:.3f} (<= 0.20: {s_ok}); fraction y < 0.3 {float((y < 0.3).mean()):.3f} (>= 0.80: {y_ok})]")
    P(f"  PF-D3 (the frame): the analyst of the other frame reads s* {LEV['frame']:+.3f} dex higher on the same widths (k = 0 on observed-frame widths); the misreading the other way costs {-abs(LEV['frame']):+.3f}; BOTH branches will be reported by the measurement.")
    sel = {fk: CAMP[("FLAT", fk, "none")]["bias_median"] for fk in FDET}
    selsd = {fk: CAMP[("FLAT", fk, "none")]["sd"] for fk in FDET}
    P("  detection-selection bias (FLAT, no shared draw): " + "; ".join(f"{fk} {v:+.3f} (SD {selsd[fk]:.3f})" for fk, v in sel.items()))
    RES["decisions"] = dict(PF_D1=pf1, PF_D1_detail=out_d1, delta_nl=delta_nl, PF_D2=pf2, selection_bias=sel, selection_sd=selsd, sd_stat=sd_stat)

    P("\n" + "=" * 110 + "\nHAND ESTIMATES (Addendum 2, HE12-HE17, frozen before this run; scored for the set PC only)\n" + "=" * 110)
    HE = {}
    if SETKEY == "PC":
        HE["HE12"] = (abs(sel["f1"]) <= 0.06 and -0.20 <= sel["f1.25"] <= 0.02 and -0.45 <= sel["f1.5"] <= -0.05 and sel["f2"] < -0.15, f"bias f1 {sel['f1']:+.3f}, f1.25 {sel['f1.25']:+.3f}, f1.5 {sel['f1.5']:+.3f}, f2 {sel['f2']:+.3f}")
        HE["HE13"] = (0.10 <= selsd["none"] <= 0.17 and 0.11 <= selsd["f1.25"] <= 0.22, f"SD_stat none {selsd['none']:.3f}, f1.25 {selsd['f1.25']:.3f}")
        HE["HE14"] = (float((y < 0.3).mean()) >= 0.85, f"fraction y < 0.3 = {float((y < 0.3).mean()):.3f}")
        HE["HE15"] = (-1.5 <= LEV["baryon_per_dex"] <= -1.0 and 0.22 <= hrec <= 0.32 and 0.15 <= rows["tau_ms"]["half"] <= 0.25, f"baryon lever {LEV['baryon_per_dex']:+.3f}; recipe band {hrec:.3f}; M* term {rows['tau_ms']['half']:.3f}")
        HE["HE16"] = (0.55 <= c68 <= 0.80 and c95 >= 0.88 and RES["reactivity"]["containment"] >= 0.95, f"coverage {c68:.3f} / {c95:.3f}; outer-band containment {RES['reactivity']['containment']:.3f}")
        HE["HE17"] = (pf1 == "NOT POSSIBLE" and pf2 == "DRAWABLE", f"PF-D1 {pf1}; PF-D2 {pf2}")
        for k, (ok_, det) in HE.items():
            P(f"  {k}: {'PASS' if ok_ else 'MISS'}  {det}")
    else:
        P(f"  (set {SETKEY}: the Addendum 2 estimates are for PC; numbers above are reported for comparison only)")
    RES["hand"] = {k: dict(ok=bool(v[0]), detail=v[1]) for k, v in HE.items()}

# ================================================================================================ MUTATE verdicts
if MUT:
    P("\n" + "=" * 110 + f"\nMUTATE={MUT} (set {SETKEY}, detection scenario {F_PRIM})\n" + "=" * 110)
    if MUT == "1":
        a_ = CAMP[("s2", F_PRIM, "none")]; f_ = CAMP[("FLAT", F_PRIM, "none")]
        rec_ok = abs(a_["median"] - math.log10(2.0)) <= 0.10
        fl, ri = CAMP[("FLAT", F_PRIM, "B")], CAMP[("RIVAL", F_PRIM, "B")]
        r1 = ri["p5"] > fl["p95"]
        P(f"  s_true = 2 recovered: median log10 s* {a_['median']:+.3f} vs {math.log10(2.0):+.3f} (|diff| {abs(a_['median'] - math.log10(2.0)):.3f} <= 0.10: {rec_ok}); PF-D1 R1 at 0.045 dex, level B: {r1} (must stay False)")
        bites = rec_ok and not r1
        P(f"\n  [MUTATE CONTROL] MUTATE=1: the planted a0 shift of 0.30 dex is recovered while the 0.045 dex rival stays unseparated: the control {'BITES' if bites else 'DOES NOT BITE'}")
    else:
        base_path = os.path.join(HERE, f"cfg260_preflight_{SETKEY}_results.json")
        base = json.load(open(base_path))["campaign"][f"FLAT|{F_PRIM}|none"]["median"] if os.path.exists(base_path) else None
        cur = CAMP[("FLAT", F_PRIM, "none")]["median"]
        if base is None:
            P("  (no main-run JSON for this set: the paired baseline is unavailable and this MUTATE cannot be read)")
            bites = False
        else:
            shift = cur - base
            want, tol = (-0.36, 0.06) if MUT == "2" else (0.43, 0.07)
            bites = abs(shift - want) <= tol
            P(f"  median log10 s* shift against the main run's baseline cell (same seed): {shift:+.3f} (expected {want:+.2f} +- {tol})")
        P(f"\n  [MUTATE CONTROL] MUTATE={MUT}: the control {'BITES' if bites else 'DOES NOT BITE'}")
    RES["bites"] = bool(bites)
    finish()
    sys.exit(1 if bites else 0)

nf = sum(1 for c in CK if not c["ok"])
P(f"\n  {len(CK) - nf}/{len(CK)} controls pass" + ("" if not nf else " -> CONTROL FAILURES") + f"  ({time.time() - T0:.0f} s)")
finish()
sys.exit(1 if nf else 0)
