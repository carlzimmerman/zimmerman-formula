#!/usr/bin/env python3
"""
agentCC -- THE a* HUNT: do the deepest existing kinematic data constrain the predicted mu-floor from below?
===========================================================================================================
THE PREDICTION (agentV kernel-inversion boundary theorem, no-kernel corollary at a->0): ANY realization of
the linear field-bath class flattens mu to const + O(a^2) below some a* > 0 -- the deep-MOND sqrt law cannot
be exact. THE BAND CONSTRAINT (agentBB registry item v): the flattening must hide below x = a/a0 ~ 0.05,
i.e. a* < 0.05*a0 ~ 4.7e-12 m/s^2 (fw footing), else it is already excluded by the full-band SPARC fit.

THE QUESTION here: do SPARC's own deepest points (y = g_bar/a0 < 0.1) constrain a* from below -- or even
show the flattening? Plus the published ultra-deep kinematic points below SPARC's floor (dSphs, UDGs).

MODELS (all on the LOCKED SPARC conventions of mi_f4_sparc_shape_test.py: Vbar^2 = sign(Vgas)Vgas^2 +
Ud*Vdisk^2 + 1.4Ud*Vbul^2; unweighted dex RMS primary, weighted secondary; both a0 footings; Upsilon at the
locked full-sample best per footing -- the floor/EFE perturbations do not move the full-band optimum):
  M0  pure MOND        g_pred = nu(y)*g_bar,  nu = McGaugh 1/(1-exp(-sqrt y))   [the locked baseline]
  M1  MOND + floor     mu freezes at x* = a*/a0: below the transition y_t (nu(y_t)y_t = x*) the boost
                       freezes, g_pred = nu(y_t)*g_bar -- slope-1 quasi-Newtonian below g_obs = a*.
                       Keyed to ACCELERATION, environment-blind. 1 parameter (a*).
  M2  MOND + EFE       QUMOND radial (repo convention, sparc_efe_test.py):
                       g_pred = nu((y+eN))*(g_bar+g_ext) - nu(eN)*g_ext, g_ext = eN*a0.
                       Keyed to ENVIRONMENT. 1 global parameter (eN) here (Chae's per-galaxy fit is finer).
  M3  floor + EFE      2 parameters.
DEGENERACY: both M1 and M2 pull g_obs BELOW the sqrt line at the deep end (downward flattening). The
DISCRIMINATOR: M1's downturn sits at universal g_obs = a* regardless of environment; M2's tracks g_ext.
So we SPLIT the deep sample by external large-scale density (2M++ 1+delta, the same field Chae+2021 used;
repo table data/sparc_a0_environment_table.csv) and fit each half.

STATS: Gaussian profile likelihood, per-point sigma_dex = (2/ln10)*eV/Vobs (the locked weighting's error
model) plus a fitted intrinsic scatter sigma_int (profiled). One-sided 95% bound on a* at dlnL = -1.355
(Delta chi2 = 2.71, boundary parameter); two-sided 95% (3.84/2) also reported. Galaxy-level bootstrap for
robustness (points within a galaxy are correlated).

PRE-REGISTERED READINGS:
  FLATTENING-FAVORED : M1 improves on M0 by dlnL > 2 at BOTH footings AND the preferred a* is the same in
                       both environment halves (acceleration-keyed, not environment-keyed).
  EFE-NOT-FLOOR      : the downturn improvement concentrates in the dense half / is carried by eN.
  BOUND              : no preference; report a*_95 (the lower bound the data impose on the hiding scale).
  DATA-INSUFFICIENT  : if the bound lands above the agentBB band line 0.05*a0 -- SPARC's deep points add
                       nothing beyond the full-band constraint.
Working rule: both footings, both metrics, deficit claims checked for convention-artifacts both ways.
agentCC, 2026-06-11. Needs numpy+scipy. Runtime ~1-2 min.
"""
import numpy as np, glob, os, csv
from scipy.optimize import brentq

rng = np.random.default_rng(20260611)
kpc = 3.0857e19
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data", "sparc_data")
ENVT = os.path.join(HERE, "..", "..", "data", "sparc_a0_environment_table.csv")
LN10 = np.log(10.0)

# ---------------------------------------------------------------- load SPARC (locked loader)
gals = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try: d = np.genfromtxt(f, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    name = os.path.basename(f).replace("_rotmod.dat", "")
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    gals.append((name, R*kpc, Vobs, eV, Vgas, Vdisk, Vbul))
print(f"SPARC galaxies loaded: {len(gals)}")

def nu_mcg(y): return 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-300))))

def assemble(Ud, a0):
    """All valid points under the locked conventions -> arrays (gb, go, edex, gidx[galaxy index])."""
    GB, GO, ED, GI = [], [], [], []
    for gi, (name, Rm, Vobs, eV, Vgas, Vdisk, Vbul) in enumerate(gals):
        Vbar2 = np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + 1.4*Ud*Vbul**2
        gb = Vbar2*1e6/Rm; go = (Vobs*1e3)**2/Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        fr = np.clip(eV, 1, None)/np.clip(Vobs, 1, None)
        GB += list(gb[ok]); GO += list(go[ok]); ED += list((2.0/LN10)*fr[ok]); GI += [gi]*int(ok.sum())
    return (np.array(GB), np.array(GO), np.array(ED), np.array(GI, dtype=int))

# ---------------------------------------------------------------- models
def pred_floor(gb, a0, astar):
    """M1: nu_McGaugh with the boost frozen below the transition where g_pred = a* (mu-floor in MI form)."""
    y = gb/a0
    if astar <= 0: return nu_mcg(y)*gb
    xs = astar/a0
    f = lambda yy: nu_mcg(np.array([yy]))[0]*yy - xs
    if f(1e-9) > 0:   yt = 1e-9          # floor below any data: inert
    elif f(50.0) < 0: yt = 50.0          # floor above everything (never happens on our grids)
    else:             yt = brentq(f, 1e-9, 50.0, xtol=1e-15, rtol=1e-13)
    return np.where(y >= yt, nu_mcg(y)*gb, nu_mcg(np.full_like(y, yt))*gb)

def pred_efe(gb, a0, eN):
    """M2: QUMOND radial EFE (repo convention, sparc_efe_test.py)."""
    if eN <= 0: return nu_mcg(gb/a0)*gb
    gext = eN*a0
    return nu_mcg((gb + gext)/a0)*(gb + gext) - nu_mcg(np.array([eN]))[0]*gext

def pred_floor_efe(gb, a0, astar, eN):
    """M3: EFE applied on top of the floored law (floor freezes the boost in BOTH nu evaluations)."""
    if astar <= 0: return pred_efe(gb, a0, eN)
    xs = astar/a0
    f = lambda yy: nu_mcg(np.array([yy]))[0]*yy - xs
    yt = 1e-9 if f(1e-9) > 0 else brentq(f, 1e-9, 50.0, xtol=1e-15, rtol=1e-13)
    nfl = lambda y: nu_mcg(np.maximum(y, yt))
    if eN <= 0:
        y = gb/a0
        return nfl(y)*gb
    gext = eN*a0
    return nfl((gb + gext)/a0)*(gb + gext) - nfl(np.array([eN]))[0]*gext

# ---------------------------------------------------------------- stats
SIG_GRID = np.concatenate([[1e-4], np.logspace(-3, np.log10(0.6), 90)])
def profile_lnL(r, ed):
    """Max over sigma_int of Gaussian lnL for residuals r (dex) with per-point errors ed (dex)."""
    v = ed[:, None]**2 + SIG_GRID[None, :]**2
    lnL = -0.5*np.sum(r[:, None]**2/v + np.log(2*np.pi*v), axis=0)
    i = int(np.argmax(lnL))
    return lnL[i], SIG_GRID[i]

def rms(r): return float(np.sqrt(np.mean(r**2)))
def wrms(r, ed):
    w = 1.0/ed**2
    return float(np.sqrt(np.sum(w*r**2)/np.sum(w)))

# ---------------------------------------------------------------- environment table
env = {}
with open(ENVT) as fh:
    for row in csv.DictReader(fh):
        try: env[row["name"]] = (float(row["onepd_2mpp"]), float(row["onepd_2mrs"]))
        except Exception: pass
print(f"environment table galaxies: {len(env)} (2M++ 1+delta = the Chae+2021 large-scale field axis)")

# ---------------------------------------------------------------- [0] REGRESSION GATE
print("\n" + "="*100)
print("[0] REGRESSION GATE -- reproduce the locked baseline (mi_f4_sparc_shape_test.out) before anything new")
print("="*100)
LOCKED = {9.36e-11: (0.52, 0.1950), 1.2e-10: (0.46, 0.1977)}
Uds = np.linspace(0.3, 1.2, 46)
for a0, (Ud_lock, s_lock) in LOCKED.items():
    best = (None, 9e9)
    for Ud in Uds:
        gb, go, ed, gi = assemble(Ud, a0)
        r = np.log10(go) - np.log10(nu_mcg(gb/a0)*gb)
        s = rms(r)
        if s < best[1]: best = (Ud, s)
    ok = (abs(best[0]-Ud_lock) < 1e-9) and (abs(best[1]-s_lock) < 5e-4)
    print(f"  a0={a0:.3g}: best-Ud {best[0]:.2f} scatter {best[1]:.4f}  vs locked ({Ud_lock:.2f}, {s_lock:.4f})"
          f"  -> {'PASS' if ok else 'FAIL'}")
    assert ok, "regression gate failed -- conventions drifted; stop."

# ---------------------------------------------------------------- main loop over footings
RESULTS = {}
ASTAR_GRID = np.concatenate([[0.0], np.logspace(-13.4, -10.6, 29)])
EN_GRID    = np.concatenate([[0.0], np.logspace(-3.0, -0.4, 27)])

for a0, (Ud_lock, _) in LOCKED.items():
    lab = "fw 9.36e-11" if a0 < 1e-10 else "canon 1.2e-10"
    print("\n" + "="*100)
    print(f"FOOTING: a0 = {lab}  (Upsilon locked at full-sample best {Ud_lock:.2f})")
    print("="*100)
    gb, go, ed, gi = assemble(Ud_lock, a0)
    y = gb/a0
    deep = y < 0.1
    GB, GO, ED, GI = gb[deep], go[deep], ed[deep], gi[deep]
    Y = GB/a0
    names = np.array([g[0] for g in gals])
    dnames = names[np.unique(GI)]
    print(f"\n[1] DEEP SAMPLE (y = g_bar/a0 < 0.1): {deep.sum()} points in {len(dnames)} galaxies "
          f"(of {len(gb)} pts / {len(gals)} gals)")
    print(f"    y range: {Y.min():.2e} .. 0.1 | g_bar: {GB.min():.2e} .. {GB.max():.2e} m/s^2")
    print(f"    g_obs at the deep points: {GO.min():.2e} .. {GO.max():.2e} m/s^2 "
          f"(min g_obs/a0 = {GO.min()/a0:.3f})")
    print(f"    points below y=0.01: {(Y<0.01).sum()}   below y=0.005: {(Y<0.005).sum()}   "
          f"below y=0.0025: {(Y<0.0025).sum()}")
    order = np.argsort(Y)[:12]
    print("    12 deepest points (galaxy, y, g_obs/a0, resid_vs_sqrt[dex]):")
    for j in order:
        rs = np.log10(GO[j]) - 0.5*np.log10(GB[j]*a0)
        print(f"      {names[GI[j]]:12s} y={Y[j]:.4f}  g_obs/a0={GO[j]/a0:.4f}  dsqrt={rs:+.3f}")

    # ---- [2] binned deep-end residuals (the shape, model-free)
    print("\n[2] BINNED RESIDUALS log10 g_obs - log10 model  (median / mean+-SEM / N) -- the raw shape:")
    bins = [(0.0, 0.005), (0.005, 0.01), (0.01, 0.02), (0.02, 0.04), (0.04, 0.07), (0.07, 0.1)]
    r_sq = np.log10(GO) - 0.5*np.log10(GB*a0)            # vs pure deep-MOND sqrt
    r_nu = np.log10(GO) - np.log10(nu_mcg(Y)*GB)         # vs full McGaugh nu (the locked law)
    print(f"    {'y bin':16s} {'N':>4s} {'med vs sqrt':>12s} {'mean vs sqrt':>14s} {'med vs nu':>11s} {'mean vs nu':>13s}")
    for lo, hi in bins:
        m = (Y >= lo) & (Y < hi)
        if m.sum() == 0: continue
        sem_s = r_sq[m].std()/np.sqrt(m.sum()); sem_n = r_nu[m].std()/np.sqrt(m.sum())
        print(f"    [{lo:.4f},{hi:.3f}) {m.sum():4d} {np.median(r_sq[m]):+12.3f} "
              f"{r_sq[m].mean():+8.3f}+-{sem_s:.3f} {np.median(r_nu[m]):+11.3f} {r_nu[m].mean():+7.3f}+-{sem_n:.3f}")
    print("    (floor/EFE signature = the deepest bins diving NEGATIVE vs nu; positive = above the law)")

    # ---- [3] model fits on the deep sample
    print("\n[3] MODEL FITS on the deep sample (profile lnL over sigma_int; unweighted dex RMS primary):")
    lg_go = np.log10(GO)
    r0 = lg_go - np.log10(nu_mcg(Y)*GB)
    L0, s0 = profile_lnL(r0, ED)
    print(f"    M0 pure MOND (locked)          : RMS {rms(r0):.4f}  wRMS {wrms(r0,ED):.4f}  "
          f"lnL {L0:.2f}  sig_int {s0:.3f}")

    # M1 profile over a*
    prof1 = []
    for ast in ASTAR_GRID:
        r = lg_go - np.log10(pred_floor(GB, a0, ast))
        L, s = profile_lnL(r, ED)
        prof1.append((ast, L, rms(r)))
    prof1 = np.array(prof1)
    i1 = int(np.argmax(prof1[:, 1]))
    a1, L1 = prof1[i1, 0], prof1[i1, 1]
    print(f"    M1 + floor a*  (best)          : RMS {prof1[i1,2]:.4f}  lnL {L1:.2f}  "
          f"a* = {a1:.3e} m/s^2 ({a1/a0:.4f} a0)   dlnL vs M0 = {L1-L0:+.2f}")
    # one-sided 95% upper bound on a*: where lnL falls 1.355 below the max (boundary-parameter convention)
    Lmax = prof1[:, 1].max()
    above = prof1[prof1[:, 1] >= Lmax - 1.355]
    a95 = above[:, 0].max()
    nxt = prof1[prof1[:, 0] > a95]
    a95u = nxt[0, 0] if len(nxt) else np.nan       # first grid point already excluded
    above2 = prof1[prof1[:, 1] >= Lmax - 1.92]
    a95_2 = above2[:, 0].max()
    print(f"    M1 95% one-sided bound         : a* <= {a95:.3e} m/s^2 = {a95/a0:.4f} a0 "
          f"(last allowed grid pt; next pt {a95u:.2e} excluded)")
    print(f"    M1 95% two-sided (dchi2=3.84)  : a* <= {a95_2:.3e} m/s^2 = {a95_2/a0:.4f} a0")
    print(f"    [context] agentBB band line 0.05*a0 = {0.05*a0:.3e};  deepest-point reach "
          f"~ min g_obs = {GO.min():.2e}")

    # M2 profile over eN
    prof2 = []
    for eN in EN_GRID:
        r = lg_go - np.log10(pred_efe(GB, a0, eN))
        L, s = profile_lnL(r, ED)
        prof2.append((eN, L, rms(r)))
    prof2 = np.array(prof2)
    i2 = int(np.argmax(prof2[:, 1]))
    e2, L2 = prof2[i2, 0], prof2[i2, 1]
    print(f"    M2 + global EFE eN (best)      : RMS {prof2[i2,2]:.4f}  lnL {L2:.2f}  "
          f"eN = {e2:.4f}   dlnL vs M0 = {L2-L0:+.2f}")

    # M3 joint (FINE grid -- the coarse grid missed offset-degenerate directions on the first run)
    best3 = (0, 0, -9e9, 9e9)
    for ast in ASTAR_GRID:
        for eN in EN_GRID:
            r = lg_go - np.log10(pred_floor_efe(GB, a0, ast, eN))
            L, s = profile_lnL(r, ED)
            if L > best3[2]: best3 = (ast, eN, L, rms(r))
    print(f"    M3 floor+EFE (fine joint)      : RMS {best3[3]:.4f}  lnL {best3[2]:.2f}  "
          f"a* = {best3[0]:.3e}, eN = {best3[1]:.4f}   dlnL vs M0 = {best3[2]-L0:+.2f}")
    print(f"    AIC (2k - 2lnL, vs M0): M1 {2*1-2*(L1-L0):+.2f}  M2 {2*1-2*(L2-L0):+.2f}  "
          f"M3 {2*2-2*(best3[2]-L0):+.2f}  (negative = preferred over M0)")

    # ---- [3b] NORMALIZATION CONTROL (working rule: is any 'gain' an a0/Upsilon offset artifact?)
    print("\n[3b] NORMALIZATION CONTROL -- pure dex-offset model g_pred = nu(y)*g_bar*10^c (NOT a floor; the")
    print("     offset direction = deep-band a0/Upsilon renormalization). If it matches M3's gain, the gain")
    print("     is a normalization artifact, not flattening:")
    cs = np.linspace(-0.15, 0.15, 121)
    Lc = []
    for c in cs:
        L, s = profile_lnL(r0 - c, ED)
        Lc.append(L)
    Lc = np.array(Lc); jc = int(np.argmax(Lc))
    print(f"    OFFSET control: best c = {cs[jc]:+.3f} dex, lnL {Lc[jc]:.2f}, dlnL vs M0 = {Lc[jc]-L0:+.2f}")
    print(f"    -> M3 gain {best3[2]-L0:+.2f} vs offset gain {Lc[jc]-L0:+.2f}: "
          f"{'OFFSET-DEGENERATE (artifact)' if best3[2]-L0 <= Lc[jc]-L0 + 2.0 else 'EXCEEDS the offset direction'}")
    print(f"    deep-sample mean residual vs nu: {r0.mean():+.4f} dex (the offset the control absorbs)")

    # ---- [3c] SHAPE-ONLY bound: profile a* with a free nuisance offset per model (immune to the
    #      normalization direction; the floor must then show as the y-DEPENDENT dive, not a shift)
    prof1s = []
    for ast in ASTAR_GRID:
        r = lg_go - np.log10(pred_floor(GB, a0, ast))
        Ls = max(profile_lnL(r - c, ED)[0] for c in np.linspace(r.mean()-0.06, r.mean()+0.06, 25))
        prof1s.append((ast, Ls))
    prof1s = np.array(prof1s)
    j1s = int(np.argmax(prof1s[:, 1]))
    Lsmax = prof1s[:, 1].max()
    a95s = prof1s[prof1s[:, 1] >= Lsmax - 1.355][:, 0].max()
    print(f"[3c] SHAPE-ONLY (free offset nuisance): best a* = {prof1s[j1s,0]:.3e} "
          f"(dlnL {prof1s[j1s,1]-prof1s[0,1]:+.2f} vs a*=0) | 95% one-sided a* <= {a95s:.3e} m/s^2 "
          f"= {a95s/a0:.4f} a0")

    # ---- [3d] baseline-shape robustness: the framework's OWN nu (test on its own terms, working rule)
    nu_fw = lambda yy: np.sqrt(1.0 + 1.0/np.maximum(yy, 1e-300))
    Ud_fw = 0.60 if a0 < 1e-10 else 0.52          # locked full-sample best-Ud for the fw shape
    gbf, gof, edf, gif = assemble(Ud_fw, a0)
    yf = gbf/a0; df = yf < 0.1
    GBf, GOf, EDf = gbf[df], gof[df], edf[df]
    lgf = np.log10(GOf)

    def pred_floor_fw(gb_, astar):
        y_ = gb_/a0
        if astar <= 0: return nu_fw(y_)*gb_
        xs = astar/a0
        g = lambda yy: nu_fw(yy)*yy - xs          # nu_fw*y = sqrt(y+y^2), monotone
        yt = 1e-9 if g(1e-9) > 0 else brentq(g, 1e-9, 50.0, xtol=1e-15, rtol=1e-13)
        return np.where(y_ >= yt, nu_fw(y_)*gb_, nu_fw(yt)*gb_)

    pf = []
    for ast in ASTAR_GRID:
        r = lgf - np.log10(pred_floor_fw(GBf, ast))
        L, s = profile_lnL(r, EDf)
        pf.append((ast, L))
    pf = np.array(pf); jf = int(np.argmax(pf[:, 1]))
    bf = pf[pf[:, 1] >= pf[:, 1].max() - 1.355][:, 0].max()
    print(f"[3d] FW-SHAPE baseline nu=sqrt(1+1/y), Ud={Ud_fw:.2f} (own-terms robustness): "
          f"best a* = {pf[jf,0]:.3e} (dlnL {pf[jf,1]-pf[0,1]:+.2f} vs 0) | a*_95 <= {bf:.3e} "
          f"= {bf/a0:.4f} a0")

    # robustness: deep-sample-optimized Upsilon (off-convention; artifact check per the working rule)
    bestU = (None, -9e9, None)
    for Ud in Uds:
        gb2, go2, ed2, gi2 = assemble(Ud, a0)
        y2 = gb2/a0; d2 = y2 < 0.1
        r = np.log10(go2[d2]) - np.log10(nu_mcg(y2[d2])*gb2[d2])
        L, s = profile_lnL(r, ed2[d2])
        if L > bestU[1]: bestU = (Ud, L, rms(r))
    print(f"    [robustness] deep-sample best-Ud for M0: {bestU[0]:.2f} (RMS {bestU[2]:.4f}) -- "
          f"locked Ud={Ud_lock:.2f} retained for all fits above")

    # ---- [4] galaxy bootstrap of the M1 profile
    ug = np.unique(GI)
    by_gal = {g: np.where(GI == g)[0] for g in ug}
    AB = ASTAR_GRID[::2]   # coarser grid for speed
    nb = 1000
    R1 = np.array([lg_go - np.log10(pred_floor(GB, a0, ast)) for ast in AB])   # (nA, N) precomputed
    SIGB = np.logspace(-2, np.log10(0.5), 30)
    best_a, bound_a = [], []
    for b in range(nb):
        pick = rng.choice(ug, size=len(ug), replace=True)
        idx = np.concatenate([by_gal[g] for g in pick])
        r, edb = R1[:, idx], ED[idx]
        v = edb[None, :, None]**2 + SIGB[None, None, :]**2          # (1, n, S)
        lnL = -0.5*np.sum(r[:, :, None]**2/v + np.log(2*np.pi*v), axis=1)   # (nA, S)
        Ls = lnL.max(axis=1)
        j = int(np.argmax(Ls))
        best_a.append(AB[j])
        al = AB[Ls >= Ls.max() - 1.355]
        bound_a.append(al.max())
    best_a, bound_a = np.array(best_a), np.array(bound_a)
    print(f"\n[4] GALAXY BOOTSTRAP ({nb} resamples, coarse a* grid):")
    print(f"    best a* = 0 (no floor) in {100*np.mean(best_a==0):.0f}% of resamples; "
          f"best a* > {0.05*a0:.2e} (band line) in {100*np.mean(best_a>0.05*a0):.0f}%")
    print(f"    95% bound a*_95: median {np.median(bound_a):.3e}, "
          f"[16,84]% = [{np.percentile(bound_a,16):.3e}, {np.percentile(bound_a,84):.3e}] m/s^2")
    print(f"    bound in a0 units: median {np.median(bound_a)/a0:.4f} a0")

    # ---- [5] environment split (the floor-vs-EFE discriminator)
    print("\n[5] ENVIRONMENT SPLIT (2M++ 1+delta; the field Chae+2021 keyed eN to):")
    dens = np.array([env.get(names[g], (np.nan, np.nan))[0] for g in GI])
    have = np.isfinite(dens)
    med = np.nanmedian([env[n][0] for n in dnames if n in env])
    print(f"    deep points with environment data: {have.sum()}/{len(GI)} "
          f"(galaxy-level median 1+delta = {med:.3f})")
    for half, m in [("ISOLATED (1+delta < median)", have & (dens < med)),
                    ("DENSE    (1+delta >= median)", have & (dens >= med))]:
        if m.sum() < 30:
            print(f"    {half}: too few points ({m.sum()})"); continue
        lg, gbb, edb, yb = lg_go[m], GB[m], ED[m], Y[m]
        r0h = lg - np.log10(nu_mcg(yb)*gbb)
        L0h, _ = profile_lnL(r0h, edb)
        p1 = [];  p2 = []
        for ast in ASTAR_GRID:
            r = lg - np.log10(pred_floor(gbb, a0, ast)); L, s = profile_lnL(r, edb); p1.append((ast, L))
        for eN in EN_GRID:
            r = lg - np.log10(pred_efe(gbb, a0, eN));    L, s = profile_lnL(r, edb); p2.append((eN, L))
        p1, p2 = np.array(p1), np.array(p2)
        j1, j2 = int(np.argmax(p1[:, 1])), int(np.argmax(p2[:, 1]))
        b1 = p1[p1[:, 1] >= p1[:, 1].max()-1.355][:, 0].max()
        deepm = yb < 0.01
        dd = (f"{np.median(lg[deepm] - np.log10(nu_mcg(yb[deepm])*gbb[deepm])):+.3f}"
              if deepm.sum() >= 3 else "n/a")
        print(f"    {half}: N={m.sum()} (gals {len(np.unique(GI[m]))}, y<0.01 pts {deepm.sum()}) | "
              f"best a* {p1[j1,0]:.2e} (dlnL {p1[j1,1]-L0h:+.2f}; a*_95 {b1:.2e}) | "
              f"best eN {p2[j2,0]:.4f} (dlnL {p2[j2,1]-L0h:+.2f}) | med resid(y<0.01) {dd} dex")
    print("    [reading] floor predicts the SAME a* both halves; EFE predicts the downturn only/stronger DENSE.")
    RESULTS[a0] = dict(a95=a95, a95_2=a95_2, boot=np.median(bound_a), L0=L0, dL1=L1-L0, dL2=L2-L0,
                       a_best=a1, e_best=e2, npts=int(deep.sum()), ngal=len(dnames), gomin=GO.min())

# ---------------------------------------------------------------- [6] literature ultra-deep points
print("\n" + "="*100)
print("[6] PUBLISHED ULTRA-DEEP KINEMATIC POINTS BELOW SPARC'S FLOOR (pinned 2026-06-11; sqrt comparisons")
print("    computed at BOTH footings; convention g_obs = 3 sigma^2 / r_1/2 [Lelli+2017], r_1/2 = (4/3) R_e)")
print("="*100)
G = 6.674e-11; Msun = 1.989e30; pc = 3.0857e16

def dsph(name, sig_kms, Re_pc, Mstar_Msun, gext_over_a0_fw, note):
    r12 = (4.0/3.0)*Re_pc*pc
    gobs = 3*(sig_kms*1e3)**2/r12
    gbar = G*(Mstar_Msun*Msun/2.0)/r12**2
    line = f"  {name:14s} g_bar={gbar:.2e} g_obs={gobs:.2e}"
    for a0, tag in [(9.36e-11, "fw"), (1.2e-10, "cn")]:
        line += f"  d_sqrt({tag})={np.log10(gobs)-0.5*np.log10(gbar*a0):+.2f}"
    print(line + f"  g_ext~{gext_over_a0_fw:.3f}a0  {note}")
    return gbar, gobs

print("-- Milky Way satellites (EFE-dominated environments):")
dsph("Crater II",  2.7, 1066, 3.2e5, 0.143, "Caldwell+17 sigma; McGaugh PRE-predicted 2.1 km/s via EFE")
dsph("Draco",      9.1,  221, 6.4e5, 0.18,  "classical dSph; sits HIGH (EDGE-25 'twin' anomaly vs Carina)")
dsph("Fornax",    11.7,  710, 4.0e7, 0.07,  "classical dSph; the one EDGE-25 object ON/below the RAR")
print("-- weak-external-field ultrafaints (MUSE-Faint / EDGE-25 sample; offsets are theirs, not refit):")
print("  Eridanus II / Grus 1 / Leo T / Antlia B + 8 classical dSphs: g_bar 1e-14..1e-10, the dwarfs sit")
print("  SYSTEMATICALLY +0.3..+0.5 dex ABOVE the RAR extrapolation (arXiv:2510.06905, A&A 2025) -- and the")
print("  paper itself notes EFE-regime galaxies should scatter BELOW the RAR, 'the opposite is what we see'.")
print("-- isolated gas-rich UDG (the one DOWNWARD ultra-deep candidate):")
V, R, Mb = 23e3, 10*kpc, 1.4e9*Msun
gobs = V**2/R; gbar = G*Mb/R**2
print(f"  AGC 114905     g_bar={gbar:.2e} g_obs={gobs:.2e}  d_sqrt(fw)={np.log10(gobs)-0.5*np.log10(gbar*9.36e-11):+.2f}"
      f"  d_sqrt(cn)={np.log10(gobs)-0.5*np.log10(gbar*1.2e-10):+.2f}  ISOLATED (eN~0.01)")
Vc = 23e3*np.sin(np.deg2rad(32))/np.sin(np.deg2rad(15))
print(f"                 at i=32deg (Mancera Pina+22/24: BELOW sqrt, isolated -- the floor-shaped object);")
print(f"                 at i=15deg (A&A 2024 reanalysis) V->%.0f km/s, g_obs x%.1f -> d_sqrt(fw)=%+.2f: consistent."
      % (Vc/1e3, (Vc/V)**2, np.log10(gobs*(Vc/V)**2)-0.5*np.log10(gbar*9.36e-11)))
print("-- quarantined: weak-lensing RAR extensions (Mistele+24: sqrt holds to g_bar~1e-13) test the LENSING")
print("   channel, which in THIS framework carries the Psi-slip partner (agentW) -- not a kinematic a* probe.")

# ---------------------------------------------------------------- [7] verdict block
print("\n" + "="*100)
print("[7] SUMMARY (machine verdict inputs)")
print("="*100)
for a0, R in RESULTS.items():
    lab = "fw   " if a0 < 1e-10 else "canon"
    print(f"  {lab}: deep N={R['npts']} gals={R['ngal']} | min g_obs={R['gomin']:.2e} | "
          f"M1 dlnL={R['dL1']:+.2f} (best a*={R['a_best']:.2e}) M2 dlnL={R['dL2']:+.2f} (eN={R['e_best']:.3f}) | "
          f"a*_95={R['a95']:.3e} ({R['a95']/a0:.4f} a0), boot median {R['boot']:.3e} | band line {0.05*a0:.2e}")
print("\ndone.")
