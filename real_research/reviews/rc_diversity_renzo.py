#!/usr/bin/env python3
"""
rc_diversity / Renzo's rule discriminator on the REAL 175 SPARC curves.
=======================================================================

Two linked, computable facts MOND/the framework forces STRUCTURALLY and LCDM
must engineer via feedback:

(i)  RENZO'S RULE (feature correspondence): every feature in the BARYONIC
     profile has a corresponding feature in the rotation curve. Computable
     proxy on this data: within a single galaxy, the POINT-TO-POINT WIGGLES of
     g_obs about its own smooth trend should track the wiggles of the MOND
     prediction g_pred = nu(g_bar/a0) g_bar (a LOCAL function of g_bar).
     If baryonic wiggles predict RC wiggles point-by-point, that is Renzo's
     rule operating. We measure the local correlation and the residual after
     the MOND map vs after a smooth (featureless) curve.

(ii) DIVERSITY AT FIXED V_flat: galaxies with the same outer V_flat have very
     different inner RC shapes (inner rise rate). In MOND this diversity is set
     entirely by the baryonic surface density (compact vs diffuse). We measure
     the diversity in inner slope at fixed V_flat and test whether the BARYONS
     (central baryonic surface density / g_bar at small r) predict it.

Footing: framework's OWN a0 = 9.36e-11, Upsilon_disk = 0.70, Upsilon_bulge=0.70
(per the working rule). Also reported at McGaugh Upsilon=0.5 / a0=1.2e-10 as a
robustness cross-check.
"""
import glob, os, math
import numpy as np

KPC_M = 3.0856775814913673e19
KMS_MS = 1.0e3
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")

def nu_mcgaugh(y):
    # y = g_bar/a0 ; RAR interpolating function g_obs = g_bar/(1-exp(-sqrt(y)))
    x = np.sqrt(y)
    return 1.0 / (1.0 - np.exp(-x))

def load_galaxy(path, ml_disk, ml_bulge):
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split()
            if len(p) < 6:
                continue
            try:
                r, vobs, everr, vgas, vdisk, vbul = (float(p[i]) for i in range(6))
            except ValueError:
                continue
            rows.append((r, vobs, everr, vgas, vdisk, vbul))
    if not rows:
        return None
    a = np.array(rows)
    r, vobs, everr, vgas, vdisk, vbul = a.T
    vbar2 = vgas*np.abs(vgas) + ml_disk*vdisk*np.abs(vdisk) + ml_bulge*vbul*np.abs(vbul)
    return dict(r=r, vobs=vobs, everr=everr, vbar2=vbar2,
                name=os.path.basename(path).replace("_rotmod.dat",""))

def analyze(a0, ml_disk, ml_bulge, label):
    paths = sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat")))
    # ---- (i) Renzo's rule: point-to-point feature correspondence ----
    # For each galaxy with enough points, compute g_obs, g_pred(MOND from baryons).
    # Detrend BOTH with a smooth (running-median over log r) curve, then correlate
    # the residual wiggles. MOND predicts these wiggles to be the SAME (the bumps
    # in v_obs come from bumps in the baryons). A smooth DM halo would NOT.
    corrs = []
    rms_mond = []   # residual of v_obs after MOND map
    rms_smooth = [] # residual of v_obs after a smooth (3-param) fit ignoring baryon features
    n_feat = 0
    for path in paths:
        g = load_galaxy(path, ml_disk, ml_bulge)
        if g is None:
            continue
        m = (g["r"] > 0) & (g["vobs"] > 0) & (g["vbar2"] > 0) & (g["everr"] > 0)
        if m.sum() < 8:   # need enough points to see features
            continue
        r = g["r"][m]; vobs = g["vobs"][m]; vbar2 = g["vbar2"][m]; everr = g["everr"][m]
        r_m = r*KPC_M
        g_bar = vbar2*KMS_MS**2 / r_m
        v_pred = np.sqrt(nu_mcgaugh(g_bar/a0) * vbar2)   # MOND-predicted v (km/s)
        if not np.all(np.isfinite(v_pred)):
            continue
        # smooth trend in log r for v_obs and v_pred (running median, window 5)
        lr = np.log10(r)
        def detrend(y):
            # local quadratic smooth in log r, then residual
            from numpy.polynomial import polynomial as P
            try:
                c = np.polyfit(lr, y, 3)
            except Exception:
                c = np.polyfit(lr, y, 1)
            sm = np.polyval(c, lr)
            return y - sm, sm
        # feature residual = v_obs minus its own smooth trend (the wiggles)
        wob, _ = detrend(vobs)
        # MOND-predicted wiggles: v_pred minus a smooth trend fit the SAME way
        wpr, _ = detrend(v_pred)
        # only count galaxies that actually HAVE features (baryon wiggle amplitude
        # exceeds the velocity error -> a real testable feature)
        if np.std(wpr) < np.median(everr):
            continue
        n_feat += 1
        # correlation of observed wiggles with MOND-predicted wiggles
        if np.std(wob) > 0 and np.std(wpr) > 0:
            cc = np.corrcoef(wob, wpr)[0,1]
            corrs.append(cc)
        # how well does the FULL MOND map (with features) reproduce v_obs vs a
        # smooth featureless model (cubic in log r fit to v_obs itself = best
        # possible smooth halo)?
        rms_mond.append(np.sqrt(np.mean(((vobs - v_pred)/everr)**2)))
        csm = np.polyfit(lr, vobs, 3)
        vsm = np.polyval(csm, lr)
        rms_smooth.append(np.sqrt(np.mean(((vobs - vsm)/everr)**2)))

    corrs = np.array(corrs)
    print(f"--- {label}: a0={a0:.3e}, Ups_d={ml_disk}, Ups_b={ml_bulge} ---")
    print(f"  galaxies with a real baryonic FEATURE (wiggle>median errV): {n_feat}")
    print(f"  Renzo correlation r(obs wiggle, MOND-predicted wiggle):")
    print(f"     median = {np.median(corrs):+.3f}   mean = {np.mean(corrs):+.3f}")
    print(f"     fraction with r>0 : {np.mean(corrs>0)*100:.0f}%   r>0.3 : {np.mean(corrs>0.3)*100:.0f}%")
    # sign test: under null (no correspondence) median ~0; binomial p
    npos = int(np.sum(corrs>0)); ntot = len(corrs)
    from scipy.stats import binomtest, wilcoxon
    bp = binomtest(npos, ntot, 0.5, alternative="greater").pvalue
    try:
        wp = wilcoxon(corrs, alternative="greater").pvalue
    except Exception:
        wp = float("nan")
    print(f"     sign test (>0): {npos}/{ntot}, binomial p(>0.5) = {bp:.2e}; Wilcoxon p = {wp:.2e}")
    print(f"  v_obs reproduction (chi-like, lower=better):")
    print(f"     MOND-from-baryons (LOCAL map) : median {np.median(rms_mond):.2f}")
    print(f"     best smooth cubic (featureless): median {np.median(rms_smooth):.2f}")
    return corrs

def diversity(a0, ml_disk, ml_bulge, label):
    # ---- (ii) diversity at fixed V_flat, and whether baryons predict it ----
    paths = sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat")))
    recs = []
    for path in paths:
        g = load_galaxy(path, ml_disk, ml_bulge)
        if g is None: continue
        m = (g["r"]>0)&(g["vobs"]>0)&(g["vbar2"]>0)&(g["everr"]>0)
        if m.sum() < 6: continue
        r = g["r"][m]; vobs = g["vobs"][m]; vbar2 = g["vbar2"][m]
        # V_flat: median of outer half
        n = len(r); outer = vobs[n//2:]
        vflat = np.median(outer)
        # inner shape: V(2 kpc)/V_flat (inner rise rate). interpolate.
        if r.min() > 2.0 or r.max() < 2.0:
            continue
        v2 = np.interp(2.0, r, vobs)
        inner_ratio = v2/vflat
        # baryonic central density proxy: g_bar at 2 kpc (compactness)
        gbar2 = np.interp(2.0, r, vbar2)*KMS_MS**2/(2.0*KPC_M)
        recs.append((vflat, inner_ratio, gbar2, g["name"]))
    recs = np.array([(a,b,c) for a,b,c,_ in recs])
    vflat, inner, gbar2 = recs.T
    # diversity: scatter in inner_ratio at fixed V_flat (bin in V_flat)
    bins = np.array([50,80,120,170,400])
    print(f"--- {label}: diversity at fixed V_flat ---")
    print(f"  galaxies used: {len(vflat)}")
    for i in range(len(bins)-1):
        sel = (vflat>=bins[i])&(vflat<bins[i+1])
        if sel.sum()<5: continue
        ir = inner[sel]
        print(f"  V_flat [{bins[i]:3.0f},{bins[i+1]:3.0f}): N={sel.sum():3d}  inner V2/Vflat range "
              f"{ir.min():.2f}-{ir.max():.2f} (spread {ir.max()-ir.min():.2f}), scatter {ir.std():.3f}")
    # does the baryon compactness (g_bar at 2kpc) predict the inner ratio at fixed Vflat?
    # partial correlation: residualize both vs Vflat, correlate residuals
    from numpy import log10
    lv = log10(vflat); lg = log10(gbar2+1e-30)
    # residualize inner and lg against lv (linear)
    def resid(y, x):
        c = np.polyfit(x, y, 1); return y - np.polyval(c, x)
    ri = resid(inner, lv); rg = resid(lg, lv)
    from scipy.stats import pearsonr
    pr, pp = pearsonr(rg, ri)
    print(f"  PARTIAL corr (inner-shape vs baryon-compactness at FIXED Vflat): r={pr:+.3f}, p={pp:.2e}")
    print(f"     -> MOND/framework predicts inner shape is SET by baryon compactness; r>0 confirms baryons drive the diversity")

if __name__ == "__main__":
    print("="*76)
    print("RENZO'S RULE + DIVERSITY on real 175 SPARC curves")
    print("="*76)
    # framework footing
    c_fr = analyze(9.36e-11, 0.70, 0.70, "FRAMEWORK footing")
    print()
    # McGaugh footing (robustness)
    c_mc = analyze(1.20e-10, 0.50, 0.70, "McGaugh footing")
    print()
    diversity(9.36e-11, 0.70, 0.70, "FRAMEWORK footing")
    print()
    diversity(1.20e-10, 0.50, 0.70, "McGaugh footing")
