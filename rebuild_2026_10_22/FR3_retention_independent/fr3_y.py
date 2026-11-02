#!/usr/bin/env python3
"""FR3 part B (FROZEN_CRITERIA.md): carry R500 to R200 from ACT DR6.02 y, eRASS1 gas bin. Strips read only by memmap, not copied. python3 -I fr3_y.py [--map X] [--mutate]. Reinstates nothing. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); EXT = os.path.join(os.path.dirname(REPO), "_external_data", "act_dr6_nilc")
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import gaussian_filter
MUT = "--mutate" in sys.argv; MAP = sys.argv[sys.argv.index("--map") + 1] if "--map" in sys.argv else "ComptonY"; OUT = []; CK = {}; RES = dict(map=MAP)
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(k, ok, v): CK[k] = bool(ok); P(f"  {k}: {'PASS' if ok else 'FAIL'} ({v})")
NX, R0, R1 = 43200, 3239, 8040; NR = R1 - R0 + 1; ST = os.path.join(EXT, f"strip_{MAP}.f32be"); assert os.path.getsize(ST) == NR * NX * 4
Y = np.memmap(ST, dtype=">f4", mode="r", shape=(NR, NX))
cof = lambda ra: 21600.0 - 120.0 * (ra - 360 if ra >= 180 else ra); rof = lambda de: 7559.5 + 120.0 * de
hd = fits.Header.fromstring(open(os.path.join(EXT, f"header_{MAP}.fits"), "rb").read(2880).decode("ascii")); tp = np.array([[12.3, -5.0], [133.7, 1.2], [200.1, -30.5], [355.2, 2.9]]); px = WCS(hd).all_world2pix(tp, 0); d3 = max(max(abs(cof(a) - p[0]), abs(rof(b) - p[1])) for (a, b), p in zip(tp, px)); check("K4a map geometry vs WCS", d3 < .01, f"{d3:.1e} pix")
h = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data
Mg = np.array(h["MGAS500"], float) * 1e11; Z = np.array(h["BEST_Z"], float); R5 = np.array(h["R500"], float); RA = np.array(h["RA"], float); DE = np.array(h["DEC"], float); PC = np.array(h["PCONT"], float)
def DA(z, Om=.3): zz = np.linspace(0, z, 200); return 299792.458 / 70 * np.trapz(1 / np.sqrt(Om * (1 + zz) ** 3 + 1 - Om), zz) / (1 + z)
sel = np.where((Mg > 0) & (np.log10(np.clip(Mg, 1, None)) >= 13.1) & (np.log10(np.clip(Mg, 1, None)) < 13.6) & (Z >= .05) & (Z <= .30) & (DE > -35) & (DE < 3.5))[0]
XE = np.array([0, .5, 1, 1.523, 2, 3]); NA = len(XE) - 1; PIX = .5; BM = 1.6 / (2 * math.sqrt(2 * math.log(2))) / PIX
rg0 = np.random.default_rng(20261101)
def ann(img, cx, cy, th, cosd, y0=None):
    n = img.shape[0]; yy, xx = np.indices(img.shape); rr = np.hypot((xx - cx) * cosd, yy - cy) * PIX / th; rows = np.empty(NA + 1)
    for k in range(NA): m = (rr >= XE[k]) & (rr < XE[k + 1]); rows[k] = img[m].mean()
    m = (rr >= 4) & (rr < 5); rows[NA] = img[m].mean(); return rows
# Onion: shell j, annulus i
def VI(R1_, R2_, r1, r2):
    f = lambda a, b: (2 / 3) * ((max(b * b - a * a, 0)) ** 1.5) * 2 * math.pi  # volume of sphere b inside cylinder radius a, outside a... use: V(cyl<a, sphere<b)
    def V(a, b): return 4 / 3 * math.pi * (b ** 3 - max(b * b - a * a, 0) ** 1.5) if b > 0 else 0.0
    return V(R2_, r2) - V(R1_, r2) - V(R2_, r1) + V(R1_, r1)
A = np.array([[VI(XE[i], XE[i + 1], XE[j], XE[j + 1]) / (math.pi * (XE[i + 1] ** 2 - XE[i] ** 2)) for j in range(NA)] for i in range(NA)])
Vs = np.array([4 / 3 * math.pi * (XE[j + 1] ** 3 - XE[j] ** 3) for j in range(NA)])
def carry_R(y):
    p = np.linalg.solve(A, y); return p, (p[0] * Vs[0] + p[1] * Vs[1] + p[2] * Vs[2]) / (p[0] * Vs[0] + p[1] * Vs[1]), (p[0] * Vs[0] + p[1] * Vs[1])
def gnfw(x): c, a, b, g = 1.177, 1.051, 5.4905, .3081; u = c * x; return u ** -g * (1 + u ** a) ** ((g - b) / a)
ss = np.geomspace(1e-3, 30, 4000)
yprof_R = lambda R: 2 * np.trapz(gnfw(np.sqrt(R * R + ss * ss)) * 1.0, ss)
RG = np.geomspace(.01, 7.5, 300); YG = np.array([yprof_R(r) for r in RG])
yp_truth = (lambda rr: np.trapz((gnfw(ss) * ss ** 2)[ss <= rr], ss[ss <= rr])); TRUTH = yp_truth(1.523) / yp_truth(1.0)
P(f"Sample: {len(sel)} eRASS1 clusters, lg Mg 13.1-13.6, z 0.05-0.30, Dec in strip"); T0 = time.time(); ROW = []; TK = []; AA = []
for i in sel:
    z = Z[i]; th = R5[i] / 1e3 / DA(z) * 180 / math.pi * 60; cosd = math.cos(math.radians(DE[i])); hw = int(math.ceil(5.3 * th / PIX / cosd)) + 1
    ra = RA[i]; de = DE[i]
    if MUT: ra = (ra + rg0.uniform(1, 3)) % 360; de = np.clip(de + rg0.uniform(-1, 1), -34.9, 3.4)
    cx = cof(ra); cy = rof(de) - R0; ic = int(round(cx)); iy = int(round(cy))
    if iy - hw < 0 or iy + hw + 1 > NR or ic - hw < 0 or ic + hw + 1 > NX: continue
    img = np.array(Y[iy - hw:iy + hw + 1, ic - hw:ic + hw + 1], dtype=float)
    if (img == 0).mean() > 0.0 or not np.isfinite(img).all(): continue
    ROW.append(ann(img, cx - (ic - hw), cy - (iy - hw), th, cosd)); AA.append(dict(i=int(i), th=th, cosd=cosd, hw=hw))
    TK.append(PC[i])
ROW = np.array(ROW); PC_ = np.array(TK); n = len(ROW); P(f"  used {n}; median theta500 {np.median([a['th'] for a in AA]):.1f}', time {time.time() - T0:.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB")
# beam: noise-free injected Arnaud shape, same geometry, subset
idx = rg0.choice(n, min(150, n), replace=False); M_ = []
for j in idx:
    a = AA[j]; hw = a["hw"]; yy, xx = np.indices((2 * hw + 1, 2 * hw + 1)); rr = np.hypot((xx - hw) * a["cosd"], yy - hw) * PIX / a["th"]; im = np.interp(rr, RG, YG, right=0.0); M_.append(ann(gaussian_filter(im, BM), hw, hw, a["th"], a["cosd"]))
M_ = np.array(M_); m_y = M_.mean(0); pm, rm, ym = carry_R(m_y[:NA] - m_y[NA]); CB = TRUTH / rm; Ytr = yp_truth(1.0) * 4 * math.pi; P(f"Beam mock, Arnaud shape: truth Y200/Y500 {TRUTH:.3f}, recovered with beam + pedestal + truncation {rm:.3f}, correction {CB:.3f}; Y500 recovered / truth {ym / Ytr:.3f}"); check("K4b injected y recovered within 10 % (Y500, and Y200/Y500)", abs(ym / Ytr - 1) <= .10 and abs(rm / TRUTH - 1) <= .10, f"{ym / Ytr:.3f}, {rm / TRUTH:.3f}")
def stack(ix, ped=True): v = ROW[ix].mean(0); return v[:NA] - (v[NA] if ped else 0)
rg = np.random.default_rng(20261101); all_ = np.arange(n); y0 = stack(all_); p0, R0_, Y50 = carry_R(y0); By = np.array([carry_R(stack(rg.choice(all_, n)))[1:] for _ in range(2000)]); sR = By[:, 0].std(); Syy = By[:, 1].std()
P("Stack, annuli x edges " + str(XE.tolist()) + ": mean y, pedestal 4-5 subtracted, 1e-7: " + " ".join(f"{v * 1e7:.2f}" for v in y0) + f"; pedestal {ROW[:, NA].mean() * 1e7:.2f}"); P(f"  Y500 S/N {Y50 / Syy:.1f}; raw Y200/Y500 {R0_:.3f} +- {sR:.3f}, corrected {R0_ * CB:.3f}")
if MUT: P(f"MUTATE off-cluster positions: Y500 S/N {Y50 / Syy:.1f}: {'BITES' if abs(Y50 / Syy) < 4 else 'DOES NOT BITE'}"); open(os.path.join(HERE, "fr3_y_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit()
LG141 = math.log10(1.41)
carry = lambda R, tau: math.log10(1 + (R - 1) / tau) - LG141
c0 = carry(R0_ * CB, .77); cb = [carry(r * CB, .77) for r in By[:, 0]]; sb = float(np.std(cb)); st = .5 * abs(carry(R0_ * CB, .63) - carry(R0_ * CB, .91)); ciso = carry(R0_ * CB, 1.0)
p1, R1_, _ = carry_R(stack(all_, False)); cnp = carry(R1_ * CB, .77); P(f"Carry, tau 0.77: {c0:+.3f} +- {sb:.3f} boot +- {st:.3f} tau. Isothermal tau 1: {ciso:+.3f}. No pedestal subtraction: {cnp:+.3f} (R {R1_:.3f}). Self-similar T(r) and HSE from X-COP assumed; two-halo not separated, biased high by an unmeasured amount.")
lo = PC_ <= .1; pc = carry(carry_R(stack(all_[lo]))[1] * CB, .77); P(f"PCONT <= 0.1 (N {int(lo.sum())}): {pc:+.3f}")
RES.update(n=n, c=c0, sb=sb, st=st, iso=ciso, nop=cnp, R=R0_, CB=CB, pc=pc, Y500_sn=Y50 / Syy, checks=CK); json.dump(RES, open(os.path.join(HERE, f"fr3_y_{MAP}.json"), "w"), indent=0, default=float); open(os.path.join(HERE, f"fr3_y_{MAP}.out"), "w").write("\n".join(OUT) + "\n")
