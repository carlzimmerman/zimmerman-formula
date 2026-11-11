#!/usr/bin/env python3
"""HLF1 (FROZEN_CRITERIA.md, 123947b9dc) Part A step 1: the record's own halo list from CFG596's S0 run.
Spherical-overdensity finder on the 256^3 z = 0 block-mean density (the run left no particle positions).
  KA-A1 planted NFW halos -> M_lo;  own catalogue -> bins, r_j (counts against Tinker 2008), own bias (cross ratio, bootstrap);
  KA-A2 counts against Tinker (reported);  KA-A4 bias code on a Poisson field with a known bias.
  HLF1_MUTATE=1: MA1 (cells permuted), MA2 (z = 1 grid)  -> hlf1_halos_MUTATE.json / .out
Tinker 2008 / Tinker 2010 / c(M) from CFG556's library part, executed read-only.
  nice -n 19 python3 hlf1_halos.py   -> hlf1_halos.json, hlf1_halos.out
kappa = 1/2 FITTED; footings never pooled (the list is footing-free: S0 has no a0); not theory closed; adopts nothing."""
import os, sys, json, math, time, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.ndimage import maximum_filter

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
MUT = os.environ.get("HLF1_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
os.environ["CFG556_MUTATE"] = "0"
L = {"__file__": SRC, "__name__": "cfg556_lib"}; exec(compile(code[:cut], SRC, "exec"), L)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
RHO_M, MM, LM, W_M_T, BIAS_T, conc, m_nfw = (L[k] for k in ("RHO_M", "MM", "LM", "W_M", "BIAS", "conc", "m_nfw"))
BOX = 100.0; NG = 256; CELL = BOX / NG; VOL = BOX ** 3; MCELL = RHO_M * CELL ** 3
P0 = os.path.join(EXT, "cfg596_work", "P0"); TAG = "cfg596_S0_canonical_N1024_L100_ns1024_lean"
RES = dict(lane="HLF1", part="A1 halo list", criteria="123947b9dc", note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           cell_Mpch=CELL, m_cell=MCELL, rho_m=RHO_M, KA={}, MUTATE={})
P(f"HLF1 halos: S0 256^3 block mean, cell {CELL:.6f} Mpc/h, cell mass {MCELL:.4e} Msun/h. kappa = 1/2 FITTED; not theory closed.")

# ------------------------------------------------------------------ the finder (frozen in A.1)
RG = np.round(np.arange(0.25, 12.0 + 1e-9, 0.05), 10)
_o = np.arange(-14, 15); OX, OY, OZ = np.meshgrid(_o, _o, _o, indexing="ij")
OFF = np.stack([OX.ravel(), OY.ravel(), OZ.ravel()], 1); OFF = OFF[(OFF ** 2).sum(1) <= 14 ** 2]
C3 = np.stack(np.meshgrid([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], indexing="ij"), -1).reshape(-1, 3)

def find_halos(rho1):
    """rho1 = 1 + delta on an n^3 periodic grid (cell units). Returns list of (centre[3] in cells, r200m in cells, M200m in m_cell units)."""
    n = rho1.shape[0]
    pk = (rho1 == maximum_filter(rho1, size=3, mode="wrap")) & (rho1 >= 200.0)
    idx = np.argwhere(pk); idx = idx[np.argsort(-rho1[tuple(idx.T)], kind="stable")]
    acc_c, acc_r, acc_m = [], [], []
    V = (4 * math.pi / 3) * RG ** 3
    for p in idx:
        cc = (p[None, :] + C3) % n; w = rho1[tuple(cc.T)]
        cen = p + 0.5 + (w[:, None] * C3).sum(0) / w.sum()
        if acc_c:
            d = np.array(acc_c) - cen; d -= n * np.round(d / n)
            if np.any(np.sqrt((d ** 2).sum(1)) < np.array(acc_r)): continue
        base = np.floor(cen).astype(int); cells = base[None, :] + OFF
        dist = np.sqrt((((cells + 0.5) - cen) ** 2).sum(1)); mass = rho1[tuple((cells % n).T)]
        o = np.argsort(dist); cm = np.cumsum(mass[o]); ds = dist[o]
        Menc = np.concatenate([[0.0], cm])[np.searchsorted(ds, RG, side="left")]
        Dl = Menc / V
        j = np.where((RG >= 0.75 - 1e-12) & (Dl < 200.0))[0]
        if len(j) == 0: continue
        k = j[0]
        if Dl[k - 1] < 200.0: continue                      # already below at the step before 0.75 cells: unresolved
        r2 = RG[k - 1] + (RG[k] - RG[k - 1]) * (Dl[k - 1] - 200.0) / (Dl[k - 1] - Dl[k])
        acc_c.append(cen); acc_r.append(r2); acc_m.append(200.0 * (4 * math.pi / 3) * r2 ** 3)
    return np.array(acc_c).reshape(-1, 3), np.array(acc_r), np.array(acc_m)

# ------------------------------------------------------------------ KA-A1: planted halos -> M_lo
def r200m(M): return (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3)
def planted(M, cen, n=40, f=4):
    """uniform background + NFW (CFG556 c(M)) to 2 r200m, sampled on an f-times finer grid, block-averaged. cell units."""
    r2 = r200m(M) / CELL; c = float(conc(M)); rs = r2 / c
    rhos = (M / MCELL) / (4 * math.pi * rs ** 3 * m_nfw(c))                     # in m_cell per cell^3
    x1 = (np.arange(n * f) + 0.5) / f
    X, Y, Z = np.meshgrid(x1 - cen[0], x1 - cen[1], x1 - cen[2], indexing="ij")
    r = np.maximum(np.sqrt(X * X + Y * Y + Z * Z), 0.25 / f)
    rho = np.where(r <= 2 * r2, rhos / ((r / rs) * (1 + r / rs) ** 2), 0.0)
    target = (M / MCELL) * m_nfw(2 * c) / m_nfw(c); rho *= target / (rho.sum() / f ** 3)
    fine = 1.0 + rho
    coarse = fine.reshape(n, f, n, f, n, f).mean(axis=(1, 3, 5))
    # true M200m with the background, on the analytic profile
    from scipy.optimize import brentq
    menc = lambda rr: (M / MCELL) * m_nfw(min(rr, 2 * r2) / rs) / m_nfw(c) + (4 * math.pi / 3) * rr ** 3
    rt = brentq(lambda rr: menc(rr) / ((4 * math.pi / 3) * rr ** 3) - 200.0, 0.5 * r2, 2 * r2)
    return coarse, 200.0 * (4 * math.pi / 3) * rt ** 3 * MCELL
rng = np.random.default_rng(7)
MP = [1e13, 2e13, 3e13, 5e13, 1e14, 3e14, 1e15]; ka1 = {}
for Mx in MP:
    rat = []
    for t in range(8):
        cen = 20.0 + rng.random(3)
        g, Mt = planted(Mx, cen)
        c_, r_, m_ = find_halos(g)
        rat.append(float(m_.max() * MCELL / Mt) if len(m_) else 0.0)
    a = np.abs(np.array(rat) - 1)
    ka1[f"{Mx:.0e}"] = dict(ratios=rat, median_abs=float(np.median(a)), max_abs=float(a.max()))
    P(f"KA-A1 planted M200m {Mx:.0e} (r200m {r200m(Mx) / CELL:.2f} cells, c {float(conc(Mx)):.2f}): M_found / M_true " + " ".join(f"{x:.3f}" for x in rat)
      + f" | median |dev| {np.median(a):.3f}, max {a.max():.3f}")
ok = [ka1[f"{Mx:.0e}"]["median_abs"] <= 0.15 and ka1[f"{Mx:.0e}"]["max_abs"] <= 0.30 for Mx in MP]
M_LO = None
for i in range(len(MP)):
    if all(ok[i:]): M_LO = MP[i]; break
big_ok = all(ka1[f"{Mx:.0e}"]["max_abs"] <= 0.15 for Mx in (3e14, 1e15))
RES["KA"]["KA_A1"] = dict(rows=ka1, M_lo=M_LO, big_within_0p15=big_ok, pass_=bool(M_LO is not None and big_ok))
P(f"KA-A1: M_lo = {M_LO}; 3e14 and 1e15 every one within 0.15: {big_ok} -> {'PASS' if RES['KA']['KA_A1']['pass_'] else 'FAIL'}   [{time.time() - T0:.0f} s]")

# ------------------------------------------------------------------ the run
def load(name):
    return np.load(os.path.join(P0, f"{TAG}_{name}_mesh256.npz"))["dpart"].astype(np.float64)
d0 = load("z0"); rho1 = 1.0 + d0
cat_c, cat_r, cat_m = find_halos(rho1); Mh = cat_m * MCELL
P(f"S0 z = 0: {len(Mh)} halos found; above M_lo: {int((Mh >= (M_LO or np.inf)).sum())}; largest {Mh.max():.3e} Msun/h   [{time.time() - T0:.0f} s]")
RES["catalogue"] = dict(M200m=Mh.tolist(), r200m_Mpch=(cat_r * CELL).tolist(), centre_Mpch=(cat_c * CELL).tolist())

if MUT:
    nA = int((Mh >= M_LO).sum())
    perm = np.random.default_rng(1).permutation(rho1.ravel()).reshape(rho1.shape)
    _, _, mp_ = find_halos(perm); n1 = int((mp_ * MCELL >= M_LO).sum())
    RES["MUTATE"]["MA1"] = dict(n_permuted=n1, n_z0=nA, bites=bool(n1 <= 0.10 * nA))
    P(f"MA1 cells permuted: {n1} halos above M_lo against {nA} -> {'bites' if n1 <= 0.10 * nA else 'DOES NOT BITE'}")
    _, _, m1_ = find_halos(1.0 + load("z1")); n2 = int((m1_ * MCELL >= M_LO).sum())
    RES["MUTATE"]["MA2"] = dict(n_z1=n2, n_z0=nA, bites=bool(n2 <= 0.80 * nA))
    P(f"MA2 z = 1 grid: {n2} halos above M_lo against {nA} -> {'bites' if n2 <= 0.80 * nA else 'DOES NOT BITE'}")
    json.dump(RES, open(os.path.join(HERE, f"hlf1_halos{SUF}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"hlf1_halos{SUF}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0)

# ------------------------------------------------------------------ bins, r_j, KA-A2
bins = []; lo = math.log10(M_LO) if M_LO else None
NT = lambda a, b: float(VOL * W_M_T[(MM >= a) & (MM < b)].sum())
if M_LO:
    e = lo
    while True:
        a, b = 10 ** e, 10 ** (e + 0.25); n = int(((Mh >= a) & (Mh < b)).sum())
        if n < 5: break
        bins.append(dict(lo=a, hi=b, N_own=n, N_tinker=NT(a, b), r=n / NT(a, b))); e += 0.25
M_HI = bins[-1]["hi"] if bins else None
chi2 = float(sum((x["N_own"] - x["N_tinker"]) ** 2 / x["N_tinker"] for x in bins))
flag = [f"{x['lo']:.2e}" for x in bins if not (0.5 <= x["r"] <= 2.0)]
RES.update(M_lo=M_LO, M_hi=M_HI, bins=bins)
RES["KA"]["KA_A2"] = dict(chi2_poisson=chi2, nbins=len(bins), flagged_outside_0p5_2=flag, note="reported only")
P(f"Resolved range [{M_LO:.2e}, {M_HI:.2e}] Msun/h, {len(bins)} bins of 0.25 dex" if bins else "No resolved bin with >= 5 halos")
for x in bins:
    P(f"  bin {x['lo']:.3e} - {x['hi']:.3e}: N_own {x['N_own']:4d}, Tinker 2008 {x['N_tinker']:8.2f}, r_j {x['r']:.3f}")
P(f"KA-A2 (reported): Poisson chi^2 {chi2:.2f} on {len(bins)} bins; bins outside [0.5, 2]: {flag or 'none'}")

# ------------------------------------------------------------------ own bias (0.5 dex bins), KA-A4
kf = 2 * math.pi / BOX
kx = np.fft.fftfreq(NG, d=CELL) * 2 * math.pi; kz = np.fft.rfftfreq(NG, d=CELL) * 2 * math.pi
KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij"); KMAG = np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2)
half = (KZ > 0) | ((KZ == 0) & ((KY > 0) | ((KY == 0) & (KX > 0))))
SEL = half & (KMAG >= kf * (1 - 1e-9)) & (KMAG <= 0.2)
dm_k = np.fft.rfftn(d0)[SEL]
def bias_of(field, nboot=500):
    dh = np.fft.rfftn(field)[SEL]; num = np.real(dh * np.conj(dm_k)); den = np.abs(dm_k) ** 2
    b = num.sum() / den.sum(); r = np.random.default_rng(1); bb = []
    for _ in range(nboot):
        i = r.integers(0, len(num), len(num)); bb.append(num[i].sum() / den[i].sum())
    return float(b), float(np.std(bb))
def halo_field(cen):
    g = np.zeros((NG, NG, NG)); ii = np.floor(cen).astype(int) % NG
    np.add.at(g, tuple(ii.T), 1.0); return g / g.mean() - 1.0
P(f"Bias modes: {int(SEL.sum())} half-space modes with {kf:.4f} <= k <= 0.2 h/Mpc")
bb = []
if bins:
    e = lo
    while e < math.log10(M_HI) - 1e-9:
        a, b = 10 ** e, min(10 ** (e + 0.5), M_HI); m = (Mh >= a) & (Mh < b)
        bm, be = bias_of(halo_field(cat_c[m]))
        g = (MM >= a) & (MM < b); bT = float((W_M_T[g] * BIAS_T[g]).sum() / W_M_T[g].sum())
        use = bool(be <= 0.20 * abs(bm))
        bb.append(dict(lo=a, hi=b, N=int(m.sum()), b=bm, err=be, b_tinker=bT, ratio=bm / bT, used=use))
        P(f"  bias {a:.3e} - {b:.3e}: N {int(m.sum())}, b {bm:.3f} +- {be:.3f}, Tinker 2010 {bT:.3f}, ratio {bm / bT:.3f} -> "
          + ("used" if use else "NOT RESOLVED in this bin (error > 20 %): inherited bias kept"))
        e += 0.5
RES["bias_bins"] = bb
# KA-A4: Poisson field with a known bias (b0 = 2), number density of the 1e13.5 - 1e14 bin
from scipy.ndimage import gaussian_filter
ds = gaussian_filter(d0, sigma=2.0 / CELL, mode="wrap"); lam = np.clip(1 + 2.0 * ds, 0, None)
nref = int(((Mh >= 10 ** 13.5) & (Mh < 1e14)).sum()) or 50
lam *= nref / lam.sum(); b_exp, _ = bias_of(lam / lam.mean() - 1.0, nboot=1)
cnt = np.random.default_rng(3).poisson(lam).astype(float); b_po, e_po = bias_of(cnt / cnt.mean() - 1.0)
ok4 = bool(abs(b_po - b_exp) <= 2 * e_po)
RES["KA"]["KA_A4"] = dict(N=int(cnt.sum()), b_expected=b_exp, b_poisson=b_po, err=e_po, pass_=ok4)
P(f"KA-A4 bias code: Poisson field with b0 = 2 (smoothed 2 Mpc/h), N {int(cnt.sum())}: expected {b_exp:.3f}, measured {b_po:.3f} +- {e_po:.3f} -> {'PASS' if ok4 else 'FAIL'}")
P(f"({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, f"hlf1_halos{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"hlf1_halos{SUF}.out"), "w").write("\n".join(OUT) + "\n")
