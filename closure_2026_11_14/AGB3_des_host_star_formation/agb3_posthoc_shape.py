"""AGB3, POST HOC 2 (written after AGB3's numbers and the noise post hoc were seen; no frozen word).

Does the brightness-age relation keep running among old stars? The whole-sample "today" result hangs on the legacy
hosts' old stars being older than the DES hosts' old stars, which matters only if 0.030 mag/Gyr holds linearly up
to 10 Gyr. Here the two-component age template is split at a break age t_b:
    young part  -0.030 x min(age, t_b)        old part  -0.030 x max(age - t_b, 0)
and each part gets its own amplitude in the D2 fit (mass step free) and in the U fit (no step), DES hosts, raw
magnitudes, 20 redshift bins. A linear law gives the same amplitude on both parts; a law that flattens gives an
old-part amplitude of zero. Break at 4 Gyr (stated before the run), with 3 and 5 Gyr beside it.
Also: the same split with the mass-only ages on the Pantheon+ sample of AGB2 (its fitter, diagonal weights).
Writes agb3_posthoc_shape.json; log to agb3_posthoc_shape.out."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["agb3_run.py", "none"]; sys.path.insert(0, HERE)
import numpy as np
import agb3_run as R
import agb3_twocomp as T2
import agb2_galaxy as G

log = lambda s: print(s, flush=True); out = {}
d = R.DES(); m = d.mask("des_only"); z = d.z[m]; w = 1/d.err[m]**2; n = int(m.sum()); b = R.bins_of(z, 20)
B = np.zeros((n, 20)); B[np.arange(n), b] = 1.0; age = T2.age(d.lm[m], d.ls[m], z); low = (d.lm[m] < 10).astype(float); y = R.yvec(d, m, "R")


def wls(cols, yv, ww):
    X = np.column_stack(cols); XW = X.T*ww; cov = np.linalg.inv(XW@X); beta = cov@(XW@yv); r = yv - X@beta
    M = XW*r[None, :]; sand = cov@(M@M.T)@cov
    return beta, cov, sand, float((ww*r*r).sum())


def split(name, base_cols, ages, yv, ww, tb):
    young = -0.030*np.minimum(ages, tb); old = -0.030*np.maximum(ages - tb, 0.0)
    beta, cov, sand, c2 = wls(base_cols + [young, old], yv, ww)
    b1, _, _, c1 = wls(base_cols + [young + old], yv, ww)
    ay, ao = beta[-2], beta[-1]; sy, so = np.sqrt(sand[-2, -2]), np.sqrt(sand[-1, -1])
    dv = ay - ao; sdv = np.sqrt(sand[-2, -2] + sand[-1, -1] - 2*sand[-2, -1])
    r = dict(break_gyr=tb, n_old=int((ages > tb).sum()), A_young=float(ay), sd_young=float(sy), A_old=float(ao), sd_old=float(so),
             diff=float(dv), sd_diff=float(sdv), dchi2_vs_linear=c1 - c2, A_linear=float(b1[-1]))
    log(f"   {name:34s} break {tb:.0f} Gyr ({r['n_old']:4d} hosts above): young part {ay:+.3f} +- {sy:.3f}; old part {ao:+.3f} +- {so:.3f};"
        f" difference {dv:+.3f} +- {sdv:.3f} ({dv/sdv:+.1f} sigma); chi2 gain over one slope {c1 - c2:.2f}")
    return r


log("DES hosts, two-component ages, raw magnitudes (errors from the residuals):")
for tb in (4.0, 3.0, 5.0):
    out[f"D2_break{tb:.0f}"] = split("D2 (mass step free)", [B, d.x1[m], d.c[m], low - 0.5], age, y, w, tb)
    out[f"U_break{tb:.0f}"] = split("U (no step)", [B, d.x1[m], d.c[m]], age, y, w, tb)

# Pantheon+ (AGB2's loader), mass-only ages, diagonal weights
AGB2 = os.path.normpath(os.path.join(HERE, "..", "AGB2_host_mass_step_redshift")); sys.path.insert(0, AGB2)
sys.argv = ["agb2_run.py", "none", HERE, "diag"]
import agb2_run as R2
pp = R2.PP(); mp = pp.mask("all"); zp = pp.z[mp]; wp = 1/np.diag(pp.C)[mp]; npp = int(mp.sum()); bp, _ = R2.bins_of(zp, 20)
Bp = np.zeros((npp, 20)); Bp[np.arange(npp), bp] = 1.0; agep = G.age(pp.lm[mp], zp); lowp = (pp.lm[mp] < 10).astype(float)
yp = pp.mB[mp] - R2.mu_fid(zp, pp.zh[mp])
log("Pantheon+ (AGB2's sample), mass-only ages, raw magnitudes:")
for tb in (4.0, 3.0, 5.0):
    out[f"PP_H2_break{tb:.0f}"] = split("per host (mass step free)", [Bp, pp.x1[mp], pp.c[mp], lowp - 0.5], agep, yp, wp, tb)
    out[f"PP_U_break{tb:.0f}"] = split("no step", [Bp, pp.x1[mp], pp.c[mp]], agep, yp, wp, tb)
# the legacy low-redshift hosts by themselves (197; the only hosts in the table with ages up to 10 Gyr), 5 redshift bins
ml = d.ids != 10; zl = d.z[ml]; wl = 1/d.err[ml]**2; nl = int(ml.sum()); bl = R.bins_of(zl, 5)
Bl = np.zeros((nl, 5)); Bl[np.arange(nl), bl] = 1.0; agel = T2.age(d.lm[ml], d.ls[ml], zl); yl = R.yvec(d, ml, "R"); lowl = (d.lm[ml] < 10).astype(float)
log(f"legacy low-redshift hosts alone ({nl}; two-component ages from {agel.min():.1f} to {agel.max():.1f} Gyr, {int((agel > 6).sum())} above 6 Gyr), raw magnitudes:")
beta, cov, sand, _ = wls([Bl, d.x1[ml], d.c[ml], -0.030*agel], yl, wl)
out["legacy_linear"] = dict(A=float(beta[-1]), sd=float(np.sqrt(sand[-1, -1])), sd_formula=float(np.sqrt(cov[-1, -1])))
log(f"   one slope, no step: A {beta[-1]:+.3f} +- {np.sqrt(sand[-1, -1]):.3f} (formula error {np.sqrt(cov[-1, -1]):.3f})")
for tb in (4.0, 6.0):
    out[f"legacy_U_break{tb:.0f}"] = split("legacy, no step", [Bl, d.x1[ml], d.c[ml]], agel, yl, wl, tb)
    out[f"legacy_D2_break{tb:.0f}"] = split("legacy, mass step free", [Bl, d.x1[ml], d.c[ml], lowl - 0.5], agel, yl, wl, tb)
json.dump(out, open(os.path.join(HERE, "agb3_posthoc_shape.json"), "w"), indent=1, default=float)
log("wrote agb3_posthoc_shape.json")
