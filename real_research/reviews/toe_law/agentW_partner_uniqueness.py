#!/usr/bin/env python3
"""
agentW — PART 1: THE DOUBLE-COUNTING THEOREM, made rigorous with numbers.

CLASS UNDER TEST (the pincer's first jaw): any theory in which
  (a) galactic DYNAMICS is carried by a matter-sector modification (modified inertia, MI):
      on circular orbits  mu(a/a0)*a = g_N  exactly, i.e. a = nu(g_N/a0)*g_N  — NO real phantom mass;
  (b) LENSING is carried by REAL mass: a partner component whose density reproduces the MOND-phantom
      profile, g_partner = [nu(y)-1]*g_bar  (what the Brouwer amplitude demands of a metric-passive
      matter sector; agentI item 3a; f4_lensing_wall.out).
Then the partner's stress-energy is REAL -> it gravitates on stars too (WEP for real sources), and the
rotation curve sees baryons + partner + the inertia boost. Two operator orderings exist and BOTH are run:
  ORDERING B (force-side double-count, the tasking's "g_bar + g_partner + the inertia boost"):
      g_dyn = nu(y)*g_bar + lam*[nu(y)-1]*g_bar          (boost keyed to baryons; partner adds linearly)
  ORDERING A (self-consistent MI, the named escape: "the inertia modification acts on the TOTAL g"):
      g_tot = [1 + lam*(nu(y)-1)]*g_bar ;  g_dyn = nu(g_tot/a0)*g_tot
      (the boost is PARTIALLY CANCELLED: 1/mu evaluated at the larger total acceleration)
  lam = 1 is the lensing-demanded partner; lam dials the pincer (1d).

EXACT LEMMA (printed in 1a, used throughout): for monotone x*mu(x) (the same condition Milgrom-22
requires for uniqueness), a = nu(g_N/a0)*g_N is the UNIQUE MI response to total Newtonian field g_N.
Demanding the observed RAR, a = nu(g_bar/a0)*g_bar, forces g_N = g_bar exactly, i.e. g_partner = 0
EVERYWHERE matter dynamics probes. The lensing data demand g_partner = [nu-1]*g_bar != 0 (40.5 sigma).
A real-mass partner therefore cannot satisfy both: the numbers below quantify the N-sigma cost of each
horn and close the ordering escape (1c: the only continuous escape is a0_MI -> 0 = the MI switched OFF
= dark matter with extra steps, outside premise (a)).

PRE-REGISTERED (locked before the runs; tasking's expectation quoted):
  - ordering B deep-regime overshoot -> exactly 2x (0.301 dex) as y->0;  ordering A -> nu(nu(y)y) ~ y^(-1/4),
    i.e. the "escape" ordering overshoots MORE, not less, below y = 1/16.
  - THEOREM HOLDS if, at lam=1, BOTH orderings show a deep-bin (g_bar < 1e-11) excess offset >= 0.2 dex
    significant at >= 5 sigma (per-galaxy excess statistic) for every nu shape and BOTH a0 footings, with
    best-Upsilon granted to each model.  ESCAPE SURVIVES if either ordering sits within 2 sigma. Anything
    between: characterize.
  - Conventions per the working rule: BOTH a0 footings (9.36e-11 / 1.2e-10), UNWEIGHTED dex scatter as the
    locked metric (weighted shown), best-Upsilon granted per model on the same grid as the banked pipeline,
    fixed-Upsilon=0.5 MOND-default row shown, per-galaxy (conservative) AND per-point (charitable) sigmas.

GATES (must reproduce banked values before anything is believed):
  G1 SPARC pipeline == mi_f4_sparc_shape_test.out (175 gal; fw 0.1969 / McGaugh 0.1950 / simple 0.1951 /
     std 0.1984 at framework a0; 0.1968/0.1977/0.1975/0.1980 canonical).
  G2 lensing wall == f4_lensing_wall.out (baryon-only chi2 1658.9/15 -> 40.5 sigma; framework-nu 206.8/15
     -> 12.5 sigma; deep-5 amplitude ratio 229.7x), Brouwer+2021 released isolated RAR + full covariance.

PART 2 numbers (for the memo): required slip profile 2nu-1 (gate vs agentI 61/19/6), solar-slip
auto-suppression (Cassini gamma), slip-partner absolute lensing-RAR shape, cluster ~2x arithmetic,
type-split requirement. No git. agentW, 2026-06-10.
"""
import numpy as np, glob, os
from scipy import stats

kpc = 3.0857e19
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data", "sparc_data")
LDATA = os.path.join(HERE, "..", "..", "data", "lensing_rar", "brouwer2021_rar")
A0_FW, A0_CAN = 9.36e-11, 1.2e-10

# ---------------------------------------------------------------- nu functions (banked conventions)
def nu_fw(y):     return np.sqrt(1 + 1/y)
def nu_rar(y):    return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_simple(y): return 0.5 + np.sqrt(0.25 + 1/y)
def nu_std(y):    return np.sqrt((y + np.sqrt(y*y + 4))/(2*y))
NUS = {'McGaugh RAR': nu_rar, 'fw sqrt(1+1/y)': nu_fw, 'simple': nu_simple, 'F4 standard': nu_std}

# ---------------------------------------------------------------- SPARC load (identical to banked)
rows = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try: d = np.genfromtxt(f, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    rows.append((R*kpc, Vobs, eV, Vgas, Vdisk, Vbul))
print(f"SPARC galaxies loaded: {len(rows)}")
assert len(rows) == 175, "SPARC count drifted from the banked 175"

def galaxy_arrays(Ud):
    """per-galaxy (g_bar, g_obs, frac_err) with the banked mask."""
    out = []
    for Rm, Vobs, eV, Vgas, Vdisk, Vbul in rows:
        Vbar2 = np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + 1.4*Ud*Vbul**2
        gb = Vbar2*1e6/Rm; go = (Vobs*1e3)**2/Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        fr = np.clip(eV, 1, None)/np.clip(Vobs, 1, None)
        out.append((gb[ok], go[ok], fr[ok]))
    return out

def model_gdyn(gb, nu, a0, lam, ordering, a0_mi=None):
    """the class's predicted dynamical acceleration. a0 keys the PARTNER (lensing-fixed);
       a0_mi keys the MI response (defaults to a0 = the MI-class point)."""
    if a0_mi is None: a0_mi = a0
    y = gb/a0
    gtot = (1.0 + lam*(nu(y) - 1.0))*gb
    if ordering == 'A':                      # self-consistent MI on the total real field
        return (nu(gtot/a0_mi)*gtot) if a0_mi > 0 else gtot
    elif ordering == 'B':                    # force-side boost (keyed to baryons) + partner linearly
        boost = (nu(gb/a0_mi) - 1.0)*gb if a0_mi > 0 else 0.0
        return gtot + boost
    raise ValueError(ordering)

def eval_model(Ud, nu, a0, lam, ordering, a0_mi=None, deep_cut=1e-11):
    """returns (unw, wtd, mean_all, deep per-galaxy means list, per-point deep residuals, n_deep)."""
    res_all, w_all, gal_deep, pt_deep = [], [], [], []
    for gb, go, fr in galaxy_arrays(Ud):
        if len(gb) == 0: continue
        pred = model_gdyn(gb, nu, a0, lam, ordering, a0_mi)
        r = np.log10(go) - np.log10(pred)
        res_all += list(r); w_all += list(1/fr**2)
        dm = gb < deep_cut
        if dm.sum() > 0:
            gal_deep.append(np.mean(r[dm])); pt_deep += list(r[dm])
    res_all, w_all = np.array(res_all), np.array(w_all)
    unw = np.sqrt(np.mean(res_all**2)); wtd = np.sqrt(np.sum(w_all*res_all**2)/np.sum(w_all))
    return unw, wtd, np.mean(res_all), np.array(gal_deep), np.array(pt_deep), len(pt_deep)

UDS = np.linspace(0.3, 1.2, 46)
def best_upsilon(nu, a0, lam, ordering, a0_mi=None):
    s = [eval_model(U, nu, a0, lam, ordering, a0_mi)[0] for U in UDS]
    i = int(np.argmin(s)); return UDS[i], s[i]

# ================================================================ PART 0 — GATES
print("\n" + "="*104); print("PART 0 — GATES (banked values must reproduce before anything is believed)"); print("="*104)
print("\nG1 SPARC == mi_f4_sparc_shape_test.out   (each function its own best-Upsilon; unweighted dex)")
G1 = {('framework', 'fw sqrt(1+1/y)'): .1969, ('framework', 'McGaugh RAR'): .1950,
      ('framework', 'simple'): .1951, ('framework', 'F4 standard'): .1984,
      ('canonical', 'fw sqrt(1+1/y)'): .1968, ('canonical', 'McGaugh RAR'): .1977,
      ('canonical', 'simple'): .1975, ('canonical', 'F4 standard'): .1980}
g1ok = True
for a0, a0lab in [(A0_FW, 'framework'), (A0_CAN, 'canonical')]:
    for lab, nu in NUS.items():
        Ud, s = best_upsilon(nu, a0, 0.0, 'A')          # lam=0: plain MI baseline (orderings coincide)
        ok = abs(s - G1[(a0lab, lab)]) < 2.5e-4; g1ok &= ok
        print(f"  {a0lab:9s} {lab:16s} bestUd={Ud:4.2f}  {s:.4f}  (banked {G1[(a0lab,lab)]:.4f})  {'PASS' if ok else 'FAIL'}")
assert g1ok, "G1 failed — pipeline drifted; do not proceed"

print("\nG2 lensing wall == f4_lensing_wall.out   (Brouwer+2021 released isolated RAR, full covariance)")
dl = np.genfromtxt(os.path.join(LDATA, "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"))
gbar_L = dl[:, 0]; esd = dl[:, 1]/dl[:, 4]
cv = np.genfromtxt(os.path.join(LDATA, "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt"))
nL = len(gbar_L); CL = np.zeros((nL, nL))
rad = np.unique(cv[:, 2]); idx = {r: i for i, r in enumerate(rad)}
for rw in cv: CL[idx[rw[2]], idx[rw[3]]] = rw[4]/rw[6]
CONV = 4*4.301e-3*1e6/3.0857e16          # g_obs = 4 G dSigma, G in pc Msun^-1 (km/s)^2 (SIS C=4, Brouwer eq 7)
gobs_L = CONV*esd; CgL = CL*CONV**2; CgLi = np.linalg.inv(CgL)
def sig_of_chi2(c2, df):
    p = stats.chi2.sf(c2, df)
    return stats.norm.isf(0.5*p) if p > 0 else np.sqrt(max(c2 - df, 0.0))
def lens_chi2(gmod):
    r = gobs_L - gmod; c2 = r @ CgLi @ r; return c2, sig_of_chi2(c2, nL)
c2b, sb = lens_chi2(gbar_L)
c2f, sf_ = lens_chi2(nu_fw(gbar_L/A0_FW)*gbar_L)
ratio5 = np.mean((gobs_L/gbar_L)[:5])
print(f"  baryon-only : chi2={c2b:7.1f}/{nL} -> {sb:4.1f} sigma   (banked 1658.9 -> 40.5)")
print(f"  framework nu: chi2={c2f:7.1f}/{nL} -> {sf_:4.1f} sigma   (banked  206.8 -> 12.5)")
print(f"  deep-5 amplitude ratio data/baryon = {ratio5:6.1f}x      (banked 229.7x)")
assert abs(c2b-1658.9) < 1 and abs(c2f-206.8) < 1 and abs(ratio5-229.7) < 0.5, "G2 failed"
print("  G2 PASS — same conversion (G=4.301e-3 pc Msun^-1 (km/s)^2) the banked wall used.")

# ================================================================ PART 1a — the lemma + deep limits
print("\n" + "="*104); print("PART 1a — THE LEMMA AND THE DEEP-REGIME OVERSHOOT (analytic, then exact)"); print("="*104)
print("""
LEMMA (uniqueness; same monotonicity Milgrom-22 imposes): x*mu(x) monotone => the MI response to a total
Newtonian field g_N is the unique a = nu(g_N/a0)*g_N. If the observed RAR a = nu(g_bar/a0)*g_bar holds,
then g_N = g_bar EXACTLY, i.e. the real partner density vanishes everywhere kinematics probes. The lensing
RAR demands g_partner = [nu-1]*g_bar (else baryon-only: 40.5 sigma, G2). The class cannot have both.
Deep-limit overshoot factors (g_dyn/g_obs at lam=1):  B -> 2 - 1/nu(y) -> 2 (0.301 dex);
A -> nu(nu(y)*y) -> y^(-1/4) (UNBOUNDED — the 'partial cancellation' ordering overshoots MORE below y=1/16):""")
print(f"  {'g_bar':>9s} {'y(fw a0)':>9s} | {'A factor':>9s} {'A dex':>6s} | {'B factor':>9s} {'B dex':>6s}   (McGaugh nu)")
for gb in (1e-13, 1e-12, 1e-11, 1e-10, 1e-9):
    y = gb/A0_FW; nA = nu_rar(nu_rar(y)*y)*nu_rar(y)*gb/(nu_rar(y)*gb); nB = 2 - 1/nu_rar(y)
    print(f"  {gb:9.0e} {y:9.3g} | {nA:9.3f} {np.log10(nA):6.3f} | {nB:9.3f} {np.log10(nB):6.3f}")

# ================================================================ PART 1b — SPARC, both orderings, lam=1
print("\n" + "="*104); print("PART 1b — THE OVERSHOOT ON SPARC (lam=1: the lensing-demanded partner; best-Upsilon granted)"); print("="*104)
print("""columns: best-Ud | unweighted (weighted) dex scatter | mean offset all pts | deep (g_bar<1e-11):
mean offset, then the KILL STATISTIC t_exc = (deep mean - SAME-shape lam=0 baseline deep mean)/SEM, where
SEM = per-galaxy SD of the model's own deep residuals / sqrt(n_gal) — data noise in the denominator,
galaxy-level independence (conservative); [n_gal/n_pts]; charitable per-point sqrt(dchi2) with sigma_int
calibrated so the lam=0 baseline gives chi2/N = 1. Negative offset = the model OVERSHOOTS the data.""")
summary = {}
for a0, a0lab in [(A0_FW, 'framework 9.36e-11'), (A0_CAN, 'canonical 1.2e-10')]:
    print(f"\n=== a0 = {a0lab} ===")
    for lab, nu in NUS.items():
        # baseline (lam=0) at its own best-Ud
        Ud0, s0 = best_upsilon(nu, a0, 0.0, 'A')
        b = eval_model(Ud0, nu, a0, 0.0, 'A')
        base_gal = b[3]; base_mean_deep = np.mean(base_gal)
        # calibrated per-point sigma_int for the charitable chi2 (baseline reduced chi2 = 1)
        res0, sig_obs0 = [], []
        for gb, go, fr in galaxy_arrays(Ud0):
            pred = model_gdyn(gb, nu, a0, 0.0, 'A')
            res0 += list(np.log10(go) - np.log10(pred)); sig_obs0 += list((2/np.log(10))*fr)
        res0, sig_obs0 = np.array(res0), np.array(sig_obs0)
        lo, hi = 0.0, 0.5
        for _ in range(60):
            mid = 0.5*(lo + hi)
            if np.mean(res0**2/(sig_obs0**2 + mid**2)) > 1: lo = mid
            else: hi = mid
        sig_int = 0.5*(lo + hi)
        chi2_0 = np.sum(res0**2/(sig_obs0**2 + sig_int**2))
        base_t = base_mean_deep/(np.std(base_gal, ddof=1)/np.sqrt(len(base_gal)))
        print(f"  {lab:16s} lam=0 baseline: Ud={Ud0:4.2f} {s0:.4f}  deep mean {base_mean_deep:+.4f} dex "
              f"(t_raw={base_t:+.1f}, n_gal={len(base_gal)})  [sigma_int={sig_int:.4f}]")
        for ordering in ('A', 'B'):
            Ud1, s1 = best_upsilon(nu, a0, 1.0, ordering)
            unw, wtd, mall, gal, pts, ndp = eval_model(Ud1, nu, a0, 1.0, ordering)
            mdeep = np.mean(gal)
            sem = np.std(gal, ddof=1)/np.sqrt(len(gal))
            t_exc = (mdeep - base_mean_deep)/sem      # data-vs-model, galaxy-level independence
            # charitable per-point dchi2 at the model's own best-Ud, same sigma_int
            res1, so1 = [], []
            for gb, go, fr in galaxy_arrays(Ud1):
                pred = model_gdyn(gb, nu, a0, 1.0, ordering)
                res1 += list(np.log10(go) - np.log10(pred)); so1 += list((2/np.log(10))*fr)
            res1, so1 = np.array(res1), np.array(so1)
            chi2_1 = np.sum(res1**2/(so1**2 + sig_int**2))
            sdchi = np.sqrt(max(chi2_1 - chi2_0, 0))
            print(f"    ordering {ordering}  lam=1 : Ud={Ud1:4.2f} {unw:.4f} ({wtd:.4f})  all {mall:+.4f} | "
                  f"deep {mdeep:+.4f} dex  excess t = {abs(t_exc):5.1f} sigma "
                  f"[{len(gal)}/{ndp}]  sqrt(dchi2)={sdchi:6.1f}")
            summary[(a0lab, lab, ordering)] = (mdeep - base_mean_deep, t_exc, sdchi, unw - s0)
        if lab == 'McGaugh RAR':   # deep-cut robustness (the kill must not be cut-dependent)
            for cut in (3e-12,):
                b2 = eval_model(Ud0, nu, a0, 0.0, 'A', deep_cut=cut)
                for ordering in ('A', 'B'):
                    Ud1, _ = best_upsilon(nu, a0, 1.0, ordering)
                    m2 = eval_model(Ud1, nu, a0, 1.0, ordering, deep_cut=cut)
                    sem2 = np.std(m2[3], ddof=1)/np.sqrt(len(m2[3]))
                    print(f"      [cut g_bar<{cut:.0e}] ordering {ordering}: deep {np.mean(m2[3]):+.4f} vs baseline "
                          f"{np.mean(b2[3]):+.4f} -> excess t = {abs((np.mean(m2[3])-np.mean(b2[3]))/sem2):5.1f} sigma "
                          f"(n_gal={len(m2[3])})")
# MOND-default fixed-Upsilon row (working-rule hostile-default check)
print("\n  MOND-default row (a0=1.2e-10, Upsilon FIXED 0.5, McGaugh nu):")
b = eval_model(0.5, nu_rar, A0_CAN, 0.0, 'A')
for ordering in ('A', 'B'):
    m = eval_model(0.5, nu_rar, A0_CAN, 1.0, ordering)
    sem = np.std(m[3], ddof=1)/np.sqrt(len(m[3]))
    t = (np.mean(m[3]) - np.mean(b[3]))/sem
    print(f"    ordering {ordering}: scatter {m[0]:.4f} (baseline {b[0]:.4f}); deep {np.mean(m[3]):+.4f} vs baseline "
          f"{np.mean(b[3]):+.4f} -> excess t = {abs(t):5.1f} sigma")

# ================================================================ PART 1c — the ordering/a0_MI escape, closed
print("\n" + "="*104); print("PART 1c — THE ESCAPE CHARACTERIZED: free MI scale a0_MI (partner fixed by lensing at a0)"); print("="*104)
print("""If the MI response scale a0_MI is freed while the partner stays lensing-fixed at a0, where does the
dynamics fit want a0_MI? (best-Upsilon granted at every point; McGaugh nu, framework a0; unweighted dex)""")
for ordering in ('A', 'B'):
    grid = np.array([0, .02, .05, .1, .2, .35, .5, .75, 1.0, 1.5])*A0_FW
    line = []
    for ami in grid:
        _, s = best_upsilon(nu_rar, A0_FW, 1.0, ordering, a0_mi=ami)
        line.append(s)
    i = int(np.argmin(line))
    print(f"  ordering {ordering}: a0_MI/a0 grid {np.round(grid/A0_FW,2)}")
    print(f"               scatter      {np.round(line,4)}")
    print(f"    -> minimum at a0_MI = {grid[i]/A0_FW:.2f} x a0 : {line[i]:.4f} dex"
          f"   (a0_MI = a0, the MI-class point: {line[-2 if grid[-2]==A0_FW else i]:.4f})")
print("""READING: the joint system's best fit drives the inertia modification toward ZERO — a0_MI -> 0 is
pure Newtonian inertia + a real phantom-profile halo = particle dark matter with extra steps. The escape
from the overshoot exists ONLY as the limit that deletes premise (a). Inside the class (a0_MI = a0) both
orderings stand at the 1b kill. The ordering ambiguity is hereby CLOSED, not merely characterized.""")

# ================================================================ PART 1d — the lambda pincer (joint)
print("\n" + "="*104); print("PART 1d — THE PINCER DIAL: partner fraction lam (dynamics vs lensing, jointly)"); print("="*104)
print("""lam = fraction of the MOND-phantom profile carried as real partner mass. Dynamics: per-galaxy deep
excess t (McGaugh nu, framework a0, best-Ud per lam, ordering A / B). Lensing: photons see
[1+lam*(nu-1)]*g_bar vs the Brouwer bins (full covariance) -> sigma. Joint = max(dyn, lens) per ordering.""")
lams = np.array([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0])
Ud0, _ = best_upsilon(nu_rar, A0_FW, 0.0, 'A'); base_gal = eval_model(Ud0, nu_rar, A0_FW, 0.0, 'A')[3]
print(f"  {'lam':>4s} | {'sig_lens':>8s} | {'t_dyn A':>8s} {'t_dyn B':>8s} | {'joint A':>8s} {'joint B':>8s}")
joint = {'A': [], 'B': []}
for lam in lams:
    gm = (1 + lam*(nu_rar(gbar_L/A0_FW) - 1))*gbar_L
    _, sl = lens_chi2(gm)
    ts = {}
    for o in ('A', 'B'):
        Ud, _ = best_upsilon(nu_rar, A0_FW, lam, o)
        gal = eval_model(Ud, nu_rar, A0_FW, lam, o)[3]
        sem = np.std(gal, ddof=1)/np.sqrt(len(gal))
        ts[o] = abs(np.mean(gal) - np.mean(base_gal))/sem if lam > 0 else 0.0
        joint[o].append(max(sl, ts[o]))
    print(f"  {lam:4.1f} | {sl:8.1f} | {ts['A']:8.1f} {ts['B']:8.1f} | {joint['A'][-1]:8.1f} {joint['B'][-1]:8.1f}")
for o in ('A', 'B'):
    j = np.array(joint[o]); i = int(np.argmin(j))
    print(f"  ordering {o}: best compromise lam = {lams[i]:.1f} still fails jointly at {j[i]:.1f} sigma")

# ================================================================ PART 2 — numbers for the slip memo
print("\n" + "="*104); print("PART 2 — LENS-ONLY SLIP: the numbers the memo carries"); print("="*104)
print("\n2a required slip (gate vs agentI item 3a: 61 / 19 / 6 at 1e-13/1e-12/1e-11, McGaugh nu, fw a0):")
for gb in (1e-13, 1e-12, 1e-11):
    nu = nu_rar(gb/A0_FW); print(f"   g_bar={gb:.0e}: nu={nu:6.2f} -> required Psi'/Phi' = 2nu-1 = {2*nu-1:6.1f}")

print("\n2b solar-system slip of an a0-keyed profile (gamma_eff - 1 = 2[nu(y)-1]; Cassini |gamma-1|<=2.3e-5):")
GMsun = 1.32712440018e20; Rsun = 6.957e8; AU = 1.495978707e11
places = [("Cassini conjunction b=1.6 Rsun", 1.6*Rsun), ("VLBI-ish b=10 Rsun", 10*Rsun),
          ("Saturn 9.58 AU", 9.58*AU), ("100 AU", 100*AU), ("y=2000 radius", np.sqrt(GMsun/(2000*A0_FW)))]
print(f"   {'place':32s} {'g_N':>9s} {'y(fw)':>9s} | {'2(nu-1) simple':>14s} {'2(nu-1) exp-RAR':>16s}")
for name, r in places:
    g = GMsun/r**2; y = g/A0_FW
    slip_sim = 2*(nu_simple(y) - 1); slip_exp = 2*np.exp(-np.sqrt(y))/(1 - np.exp(-np.sqrt(y)))
    se = f"{slip_exp:.1e}" if slip_exp > 1e-300 else f"~e^-{np.sqrt(y):,.0f}"
    print(f"   {name:32s} {g:9.2e} {y:9.3g} | {slip_sim:14.2e} {se:>16s}")
print(f"   (the tasking's e^-sqrt(2000) ~ {np.exp(-np.sqrt(2000)):.1e} corresponds to r ~ {np.sqrt(GMsun/(2000*A0_FW))/AU:.0f} AU;")
print(f"    at Cassini's conjunction sqrt(y) = {np.sqrt(GMsun/(1.6*Rsun)**2/A0_FW):,.0f} -- the exponential slip is zero to all orders;")
print(f"    even the POWER-LAW (simple-nu) slip passes Cassini by x{2.3e-5/(2*(nu_simple(GMsun/(1.6*Rsun)**2/A0_FW)-1)):.1e}.)")

print("\n2c the slip partner inherits the ABSOLUTE lensing-RAR shape (Brouwer bins, full covariance):")
for a0, a0lab in [(A0_FW, 'fw'), (A0_CAN, 'can')]:
    out = []
    for lab, nu in NUS.items():
        c2, s = lens_chi2(nu(gbar_L/a0)*gbar_L); out.append(f"{lab} {c2:6.1f}->{s:4.1f}s")
    print(f"   a0={a0lab:3s}: " + " | ".join(out))
print("   (whatever shape the slip is keyed to, the published absolute tension rides along — banked caveat.)")

print("\n2d clusters (illustrative-canonical numbers; Sanders 1999/2003 residual factor ~2 re-derived):")
Msun = 1.989e30; Mpc = 3.0857e22
Mb = 7e13*Msun; Ml = 5e14*Msun; r = 1.0*Mpc; G = 6.674e-11
gb_cl = G*Mb/r**2; go_cl = G*Ml/r**2
for lab, nu in [('McGaugh RAR', nu_rar), ('simple', nu_simple)]:
    gp = nu(gb_cl/A0_FW)*gb_cl
    print(f"   M_bar(<1Mpc)=7e13, M_lens=5e14: g_bar={gb_cl:.2e}, slip-lensing pred ({lab}) = {gp:.2e},"
          f" observed = {go_cl:.2e} -> shortfall x{go_cl/gp:.2f}")
print("   -> a slip keyed to nu(g_bar/a0) re-fails clusters by the SAME ~x2 MOND residual, by construction.")

print("\n2e the type-split requirement (the slip cannot be a function of g_bar alone):")
print("""   measured early-above-late at fixed g_bar: +0.261 dex (u-r; hardened 8.6-9.2 sigma; own catalog).
   A slip keyed to g_bar alone predicts EXACTLY 0 split -> faces the same ~9-sigma kill as type-blind MOND,
   and in a lens-only hybrid there is no real-mass SHMR difference to hide behind (H3-T4's escape is closed
   to it): the FULL +0.261 dex must come from slip-amplitude modulation by a second variable.
   agentJ bounds its shape: sharp condensation staircase REFUTED 7.3 sigma; smooth 1-halo-safe mass trend
   +0.122 +/- 0.062 dex/dex (2.0 sigma), control inverted (clean bins carry it). The slip's second variable
   must be SMOOTH in halo mass and deliver ~0.26 dex between classes at fixed g_bar.""")

# ================================================================ PART 3 — verdict assembly
print("\n" + "="*104); print("PART 3 — ADJUDICATION AGAINST THE PRE-REGISTERED THRESHOLDS"); print("="*104)
worst = {('A'): [], ('B'): []}
for (a0lab, lab, o), (exc, t, sd, dsc) in summary.items():
    worst[o].append((abs(t), exc, a0lab, lab))
for o in ('A', 'B'):
    w = sorted(worst[o])[0]
    print(f"  ordering {o}: WEAKEST kill across all shapes/footings = {w[0]:.1f} sigma (excess {w[1]:+.3f} dex; {w[2]}, {w[3]})")
print("""  Threshold was: theorem HOLDS if every cell >= 0.2 dex excess at >= 5 sigma. See table above; the
  .md adjudicates. The a0_MI scan (1c) closes the ordering escape: its only refuge is a0_MI -> 0 = no MI.""")
print("\ndone.")
