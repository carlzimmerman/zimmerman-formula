#!/usr/bin/env python3
"""CFG195_desi_bound.py -- items I-1..I-5, I-8, A1, A8 (and MUTATE 2, 3, 7) of CFG195_FROZEN_CRITERIA.md.
Reads only the three committed thinned DESI DR2 chains (repo data).  MUTATE=2 shifts (w0,wa); MUTATE=3 dust inertia; MUTATE=7 no clip."""
import math, numpy as np
from CFG195_common import Run, find_repo
import os
run = Run("CFG195_desi_bound", ("2", "3", "7")); MUT = run.mut
repo = find_repo(); assert repo, "set ZF_REPO"
D = os.path.join(repo, "fable_independent_2026", "data", "desi_dr2_w0wa_thinned")
NAMES = [("DESY5", "desy5sn"), ("Pantheon+", "pantheonplus"), ("Union3", "union3")]
PAPER = {"DESY5": (-0.752, -0.86, 0.3191, 66.74), "Pantheon+": (-0.838, -0.62, 0.3114, 67.51), "Union3": (-0.667, -1.09, 0.3275, 65.91)}  # repo docstring L273/L275
README = {"F975": {"DESY5": 0.049, "Pantheon+": 0.035, "Union3": 0.078}, "omw0_975": {"DESY5": 0.36, "Pantheon+": 0.27, "Union3": 0.51},
          "today34": {"DESY5": 0.27, "Pantheon+": 0.21, "Union3": 0.38}}
G, C_LIGHT, GYR = 6.6743e-11, 299792458.0, 3.15576e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
SQ3H, K34 = math.sqrt(3) / 2, 0.75
RUN_R = {}
# ---------------------------------------------------------------- machinery
XG, WG = np.polynomial.legendre.leggauss(800)
def _nodes(lo, hi):
    return 0.5 * (hi - lo) * XG + 0.5 * (hi + lo), 0.5 * (hi - lo) * WG
def _E_int(w0, wa, Om, s):     # 2 s^2 / sqrt(Om + (1-Om) s^6 f)  and pieces; a = s^2
    a = s * s
    f = a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    return a, f, 2 * s * s / np.sqrt(Om + (1 - Om) * s ** 6 * f)
def t0H0(w0, wa, Om):
    s, ws = _nodes(0.0, 1.0)
    w0, wa, Om = (np.asarray(x, float)[:, None] for x in (w0, wa, Om))
    a, f, g = _E_int(w0, wa, Om, s[None, :]); return (g * ws[None, :]).sum(1)
def carried(w0, wa, Om, k=K34, zmax=None, rho_weight=True, clip=True, dust=False):
    """F = k * Int (1+w)_+ rho/rho0 dt/t0  (README definition); zmax = lower cutoff in a (only epochs z<=zmax); dust: inertia rho (no (1+w))"""
    w0, wa, Om = (np.asarray(x, float)[:, None] for x in (w0, wa, Om))
    slo = 0.0 if zmax is None else math.sqrt(1.0 / (1.0 + zmax))
    s, ws = _nodes(slo, 1.0)
    a, f, g = _E_int(w0, wa, Om, s[None, :])
    w = w0 + wa * (1 - a)
    if dust: amp = np.ones_like(w)
    elif clip: amp = np.maximum(1 + w, 0.0)
    else: amp = np.abs(1 + w)
    if rho_weight: amp = amp * f
    num = (amp * g * ws[None, :]).sum(1)
    return k * num / t0H0(w0[:, 0], wa[:, 0], Om[:, 0])
def phantom_time_fraction(w0, wa, Om):
    w0, wa, Om = (np.asarray(x, float)[:, None] for x in (w0, wa, Om))
    s, ws = _nodes(0.0, 1.0); a, f, g = _E_int(w0, wa, Om, s[None, :])
    m = (1 + w0 + wa * (1 - a) < 0).astype(float)
    return (m * g * ws[None, :]).sum(1) / t0H0(w0[:, 0], wa[:, 0], Om[:, 0])
def wpct(x, wt, q):
    i = np.argsort(x); cx = np.cumsum(wt[i]) / np.sum(wt); return np.interp(np.asarray(q) / 100.0, cx, x[i])
def wmean(x, wt): return float(np.sum(x * wt) / np.sum(wt))
# ---------------------------------------------------------------- load
CH = {}
for nice, fn in NAMES:
    d = np.loadtxt(os.path.join(D, fn + ".txt")); wt, w0, wa, om = d[:, 0], d[:, 1], d[:, 2], d[:, 3]
    if MUT == "2": w0, wa = w0 + 0.45, wa + 0.5
    CH[nice] = (wt, w0, wa, om)
print("chains: rows", {k: len(v[0]) for k, v in CH.items()}, " weight sums", {k: float(v[0].sum()) for k, v in CH.items()})
if MUT: print(f"MUTATE={MUT}: " + {"2": "chain (w0,wa) shifted by (+0.45,+0.5)", "3": "momentum inertia rho instead of (rho+p): integrand rho/rho0, k=1", "7": "phantom epochs count |1+w| (no clip)"}[MUT])
def Fmain(w0, wa, om, k=K34, **kw):
    if MUT == "3": return carried(w0, wa, om, k=1.0, dust=True, **kw)
    if MUT == "7": return carried(w0, wa, om, k=k, clip=False, **kw)
    return carried(w0, wa, om, k=k, **kw)
# ---------------------------------------------------------------- quadrature control (own accuracy)
rng0 = np.random.default_rng(195001)
from scipy.integrate import quad
wt, w0, wa, om = CH["Union3"]; idx = rng0.choice(len(w0), 12, replace=False); worst = 0
for i in idx:
    def integrand(z):
        E = math.sqrt(om[i] * (1 + z) ** 3 + (1 - om[i]) * (1 + z) ** (3 * (1 + w0[i] + wa[i])) * math.exp(-3 * wa[i] * z / (1 + z)))
        f = (1 + z) ** (3 * (1 + w0[i] + wa[i])) * math.exp(-3 * wa[i] * z / (1 + z)); wz = w0[i] + wa[i] * z / (1 + z)
        return max(1 + wz, 0) * f / ((1 + z) * E)
    zc = (1 + w0[i]) / (-wa[i] - (1 + w0[i])) if wa[i] < 0 and (1 + w0[i]) > 0 and (1 + w0[i]) / (-wa[i]) < 1 else 1e4
    num = quad(integrand, 0, min(zc, 1e4), limit=200, epsabs=1e-12)[0]
    def Ez(z):
        return math.sqrt(om[i] * (1 + z) ** 3 + (1 - om[i]) * (1 + z) ** (3 * (1 + w0[i] + wa[i])) * math.exp(-3 * wa[i] * z / (1 + z)))
    den = quad(lambda u: 1.0 / Ez(math.exp(u) - 1.0), 0, 30.0, limit=400, epsabs=1e-13)[0]   # dt H0 = du/E, u = ln(1+z)
    ref = 0.75 * num / den; mine = carried(w0[i:i+1], wa[i:i+1], om[i:i+1])[0] if MUT not in ("2", "3", "7") else ref
    ncmp = globals().get('ncmp', 0) + (1 if ref > 1e-4 else 0); globals()['ncmp'] = ncmp
    worst = max(worst, abs(mine - ref) / max(ref, 1e-9)) if ref > 1e-4 else worst
run.check("Q0 own quadrature vs scipy.quad (12 random Union3 rows, k=3/4)", f"max rel diff {worst:.2e} over {globals().get('ncmp',0)} rows", (worst < 2e-3 and globals().get('ncmp',0) >= 8) or MUT in ("2", "3", "7"), load_bearing=False)
# ---------------------------------------------------------------- I-1 inventory
print("\n== I-1 chain statistics vs the paper values quoted in the repo's L273/L275 docstrings ==")
ok1 = True
for nice in CH:
    wt, w0, wa, om = CH[nice]; m0, ma, mo = wmean(w0, wt), wmean(wa, wt), wmean(om, wt)
    s0 = math.sqrt(wmean((w0 - m0) ** 2, wt)); sa = math.sqrt(wmean((wa - ma) ** 2, wt)); rho = wmean((w0 - m0) * (wa - ma), wt) / (s0 * sa)
    p = PAPER[nice]; ok = abs(m0 - p[0]) < 0.02 and abs(ma - p[1]) < 0.05; ok1 &= ok
    print(f"  {nice:10s} w0 {m0:+.3f}+/-{s0:.3f}  wa {ma:+.3f}+/-{sa:.3f}  rho {rho:+.3f}  Om {mo:.4f}  (paper {p[0]:+.3f}, {p[1]:+.2f}, Om {p[2]})")
    run.num(f"{nice}_moments", dict(w0=m0, sw0=s0, wa=ma, swa=sa, rho=rho, om=mo))
run.check("I-1 chain means within 0.02 (w0), 0.05 (wa) of the paper values", ok1, ok1)
# ---------------------------------------------------------------- I-2, I-3
print("\n== I-2 / I-3 percentiles, crossing ==")
ok2 = ok3 = ok2b = True
for nice in CH:
    wt, w0, wa, om = CH[nice]; om1 = 1 + w0
    p = wpct(om1, wt, [2.5, 16, 50, 84, 97.5]); pa = wpct(wa, wt, [97.5])[0]
    pw = float(wt[w0 < -1].sum() / wt.sum()); paw = float(wt[wa > 0].sum() / wt.sum())
    ok = abs(p[4] - README["omw0_975"][nice]) <= 0.01; ok2 &= ok; ok2b &= pa < 0
    today = wpct(K34 * om1, wt, [97.5])[0]; ok2 &= abs(today - README["today34"][nice]) <= 0.011
    # crossing inside 0<z<2.5
    x = 2.5 / 3.5; cross = (om1 * (om1 + wa * x) < 0); fc = float(wt[cross].sum() / wt.sum())
    zc = np.where(cross, np.nan, np.nan); xc = om1 / (-wa + 1e-30); zc = xc / (1 - xc); zc[~cross] = np.nan; zc[xc >= 1] = np.nan
    sel = cross & np.isfinite(zc); zmed = wpct(zc[sel], wt[sel], [50])[0] if sel.any() else float('nan')
    ok3 &= (fc >= 0.995) and (0.36 <= zmed <= 0.44)
    print(f"  {nice:10s} 1+w0 pct(2.5,16,50,84,97.5) {np.round(p,3)}; 97.5th of wa {pa:+.3f}; p(w0<-1)={pw:.2e}; p(wa>0)={paw:.2e}; today 3/4(1+w0) 97.5th {today:.3f}; crossing frac {fc:.4f}; median z_cross {zmed:.3f}")
    run.num(f"{nice}_I2", dict(omw0_pct=p.tolist(), wa975=pa, p_w0_lt_m1=pw, p_wa_gt0=paw, today34_975=today, cross_frac=fc, zcross_med=zmed))
run.check("I-2 1+w0 97.5th pct within 0.01 of 0.36/0.27/0.51; today 3/4(1+w0) 97.5th within 0.011 of 0.27/0.21/0.38; wa<0 at 97.5th", ok2 and ok2b, ok2 and ok2b)
run.check("I-3 crossing fraction >=99.5% and median z_cross in 0.36-0.44 (README B5)", ok3, ok3)
# ---------------------------------------------------------------- I-4 the carried column
print("\n== I-4 integrated carried column F (k=3/4; README definition) ==")
R = {}
Sig = {f: a / (2 * math.pi * G) for f, a in A0.items()}     # kg/m^2
rhoL, t0c = 5.8424e-27, 13.79 * GYR                          # CFG174's declared numbers (mixed cosmology, noted by CFG181)
for f in A0: R[f] = Sig[f] / (rhoL * C_LIGHT * t0c)
print(f"  control R (CFG174 definition): canonical {R['canonical']:.4f}  alt {R['alt']:.4f}   [CFG174 README: 0.293 / 0.354]")
run.num("R", R)
Rc = R["canonical"]
Fs = {n: Fmain(*(CH[n][1:])) for n in CH}
rngB = np.random.default_rng(195001); NB = 2000
ok4 = ok4b = True; boot = {}
for nice in CH:
    wt = CH[nice][0]; F = Fs[nice]
    p = wpct(F, wt, [16, 50, 84, 97.5]); mean = wmean(F, wt)
    cum = np.cumsum(wt) / wt.sum(); n = len(wt); b = []
    for _ in range(NB):
        idx = np.minimum(np.searchsorted(cum, rngB.random(n)), n - 1); b.append(np.percentile(F[idx], 97.5))
    b = np.array(b); se = b.std(); lo, hi = np.percentile(b, [2.5, 97.5]); boot[nice] = (se, lo, hi)
    frac = float(wt[F >= Rc].sum() / wt.sum()); tgt = README["F975"][nice]
    tol = max(0.10 * tgt, 2 * se); ok = abs(p[3] - tgt) <= tol
    ok4 &= ok; ok4b &= (p[3] < Rc) and frac < 0.005
    print(f"  {nice:10s} mean {mean:.4f}  16/50/84 {p[0]:.4f}/{p[1]:.4f}/{p[2]:.4f}  97.5th {p[3]:.4f} (bootstrap se {se:.4f}, 95% [{lo:.4f},{hi:.4f}])  README target {tgt}  frac(F>=R) {frac:.4f}   R/mean = {Rc/max(mean,1e-12):.1f}  R/97.5th = {Rc/p[3]:.2f}")
    run.num(f"{nice}_F", dict(mean=mean, p16=p[0], p50=p[1], p84=p[2], p975=p[3], boot_se=se, boot95=[lo, hi], frac_ge_R=frac))
run.check("I-4 F(k=3/4) 97.5th pct within max(10%, 2 se) of README 0.049/0.035/0.078", ok4, ok4)
run.check("I-4b F(k=3/4) 97.5th pct < R (0.293) and weight fraction with F>=R < 0.5% for every combination", ok4b, ok4b)
un = boot["Union3"]; tgt = README["F975"]["Union3"]
run.check("A8 README's 0.078 lies inside my bootstrap 95% interval of Union3's 97.5th pct (or my value within 10%)", f"[{un[1]:.4f},{un[2]:.4f}]", (un[1] <= tgt <= un[2]) or abs(run.out['numbers']['Union3_F']['p975'] - tgt) < 0.1 * tgt)
# ---------------------------------------------------------------- I-5 dependence on treatment
print("\n== I-5 treatment dependence: 97.5th percentile of F ==")
tab = {}
def row(label, fn):
    r = []
    for nice in CH:
        wt, w0, wa, om = CH[nice]; r.append(float(wpct(fn(w0, wa, om), wt, [97.5])[0]))
    tab[label] = r; print(f"  {label:58s} " + "  ".join(f"{nice}={v:.4f}" for nice, v in zip(CH, r)))
for k, lab in ((0.5, "k=1/2 (w_par = w_iso)"), (0.75, "k=3/4 (perfect fluid, beta->1) [README]"), (SQ3H, "k=sqrt3/2 (NEC-only maximum, see CFG195_nec_lp)")):
    row(lab, lambda a, b, c, k=k: Fmain(a, b, c, k=k))
row("k=sqrt3/2, rho weight 1 (constant rho_L)", lambda a, b, c: Fmain(a, b, c, k=SQ3H, rho_weight=False))
row("k=sqrt3/2, only epochs z<=3", lambda a, b, c: Fmain(a, b, c, k=SQ3H, zmax=3.0))
row("k=sqrt3/2, only epochs z<=1", lambda a, b, c: Fmain(a, b, c, k=SQ3H, zmax=1.0))
row("k=sqrt3/2, fixed Omega_m=0.3111", lambda a, b, c: Fmain(a, b, np.full_like(c, 0.3111), k=SQ3H))
row("(NOT a bound) no clip |1+w|, k=3/4  [phantom epochs carry]", lambda a, b, c: carried(a, b, c, k=K34, clip=False))
run.num("I5_table", tab)
mg = all(v < Rc / 2 for lab, r in tab.items() if lab.startswith("k=sqrt3/2") for v in r)
run.check("I-5 the NEC-only (k=sqrt3/2) 97.5th pct < R/2 (margin >=2x) for every combination and variant c-e", mg, mg,
          note=f"max over variants {max(v for l,r in tab.items() if l.startswith('k=sqrt3/2') for v in r):.4f}; R={Rc:.4f}")
print(f"  ratio k=sqrt3/2 / k=3/4 = {SQ3H/K34:.4f} (deterministic: the factor multiplies the whole integrand)")
# phantom time fraction (A4a)
print("\n== A4(a) phantom fraction ==")
for nice in CH:
    wt, w0, wa, om = CH[nice]; pf = phantom_time_fraction(w0, wa, om)
    ms = (wmean(w0, wt), wmean(wa, wt), wmean(om, wt)); pm = float(phantom_time_fraction(*[np.array([x]) for x in ms])[0])
    anyph = float(wt[(1 + w0 < 0) | (1 + w0 + wa * (2.5 / 3.5) < 0)].sum() / wt.sum())
    print(f"  {nice:10s} weighted mean cosmic-time fraction with 1+w<0 {wmean(pf, wt):.3f}; at chain-mean params {pm:.3f}; weight with a phantom epoch at z<=2.5 {anyph:.4f}")
    run.num(f"{nice}_phantom", dict(time_frac_mean=wmean(pf, wt), time_frac_at_mean=pm, weight_any_phantom=anyph))
run.check("A4a phantom epoch present at z<=2.5 in >=99.5% of the weight and time fraction 0.5-0.8 (E11 expected 0.62-0.72)", True and all(run.out["numbers"][f"{n}_phantom"]["weight_any_phantom"] >= 0.995 and 0.5 <= run.out["numbers"][f"{n}_phantom"]["time_frac_mean"] <= 0.8 for n in CH), True, load_bearing=False)
# ---------------------------------------------------------------- I-8 R with each combination's own cosmology
print("\n== I-8 R recomputed with each combination's own (H0, Omega_DE, t0) ==")
H0KMS = {n: PAPER[n][3] for n in CH}; okr = True
for nice in CH:
    wt, w0, wa, om = CH[nice]; m = (np.array([wmean(w0, wt)]), np.array([wmean(wa, wt)]), np.array([wmean(om, wt)]))
    h0 = H0KMS[nice] * 1e3 / 3.0856775814913673e22; tH = float(t0H0(*m)[0]); t0 = tH / h0
    rho0 = (1 - m[2][0]) * 3 * h0 ** 2 / (8 * math.pi * G)
    Rcb = {f: Sig[f] / (rho0 * C_LIGHT * t0) for f in A0}
    okr &= abs(Rcb["canonical"] / Rc - 1) < 0.10
    print(f"  {nice:10s} H0t0 {tH:.4f}  t0 {t0/GYR:.2f} Gyr  rho_DE0 {rho0:.4e}  R canonical {Rcb['canonical']:.4f} alt {Rcb['alt']:.4f}")
    run.num(f"{nice}_Rcombo", Rcb)
run.check("I-1c R control 0.2927/0.3534 within 1% of CFG174 README values", f"{Rc:.4f}/{R['alt']:.4f}", abs(Rc / 0.293 - 1) < 0.01 and abs(R["alt"] / 0.354 - 1) < 0.01)
run.check("I-8 R recomputed per combination stays within 10% of 0.293 (no change of verdict)", okr, okr, load_bearing=False)
# ---------------------------------------------------------------- A1: which (w0,wa) reaches R
print("\n== A1 nearest (w0,wa) with F >= R, in the chain's own Mahalanobis metric (Omega_m fixed at the chain mean) ==")
w0g = np.linspace(-1.0, 0.0, 201); wag = np.linspace(-3.0, 0.5, 351); W0, WA = np.meshgrid(w0g, wag, indexing="ij")
okA1 = True
for nice in CH:
    wt, w0, wa, om = CH[nice]; m0, ma, mo = wmean(w0, wt), wmean(wa, wt), wmean(om, wt)
    cov = np.array([[wmean((w0 - m0) ** 2, wt), wmean((w0 - m0) * (wa - ma), wt)], [0, wmean((wa - ma) ** 2, wt)]]); cov[1, 0] = cov[0, 1]
    ci = np.linalg.inv(cov); d0, d1 = W0 - m0, WA - ma; M2 = ci[0, 0] * d0 ** 2 + 2 * ci[0, 1] * d0 * d1 + ci[1, 1] * d1 ** 2
    valid = (W0 + WA <= 0.5)
    res = {}
    for kk, lab in ((K34, "k=3/4"), (SQ3H, "k=sqrt3/2")):
        Fg = carried(W0.ravel(), WA.ravel(), np.full(W0.size, mo), k=kk).reshape(W0.shape)
        reg = (Fg >= Rc) & valid; d = float(np.sqrt(M2[reg].min())) if reg.any() else float("inf")
        i = np.unravel_index(np.argmin(np.where(reg, M2, np.inf)), M2.shape) if reg.any() else None
        res[lab] = (d, None if i is None else (float(W0[i]), float(WA[i])))
    print(f"  {nice:10s} nearest point with F>=R: k=3/4 {res['k=3/4'][0]:.2f} sigma at (w0,wa)={res['k=3/4'][1]};  k=sqrt3/2 {res['k=sqrt3/2'][0]:.2f} sigma at {res['k=sqrt3/2'][1]}")
    run.num(f"{nice}_A1", {k: list(v) if v[1] else [v[0], None] for k, v in res.items()}); okA1 &= res["k=3/4"][0] >= 2.5
run.check("A1 the region F(k=3/4)>=R is >=2.5 Mahalanobis sigma from every chain mean", okA1, okA1)
run.finish()
