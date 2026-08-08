#!/usr/bin/env python3
"""
GAIA DR4 PREP -- DOOR 4A: WIDE-BINARY gamma PIPELINE + SYNTHETIC-INJECTION GATE
================================================================================
PREP ONLY. No new theory claims. Confrontation target: Gaia DR4 (Dec 2026).

FRAMEWORK TARGET (banked, judged on its OWN terms -- de Sitter-Unruh MODIFIED
INERTIA, nu(y)=sqrt(1+1/y), a0 = cH_Lambda/Z):
    Newton 1.00 < framework-MG 1.137 < framework-MI 1.1582 < MOND benchmark 1.33
  *** NOTE THE ORDERING INVERSION. *** Under Amendment 8's Route A kernel the
  framework-MI target (1.1582) now EXCEEDS the frozen framework-as-MG target
  (1.137), which sits INSIDE the MI range 1.1311-1.1964 (0.77 sigma_tot from the
  point value). MI-vs-MG therefore CANNOT be scored by proximity, and Amendment
  7(e)'s reporting rule is load-bearing rather than stylistic: report raw
  gamma_hat with sigma_fit and BOTH distances, never a single verdict word.
  gamma = deep-regime velocity-boost asymptote gamma_v = v_rms/v_rms(Newton).
  BANKED CORRECTION HONORED: the framework-MI number is ~1.09 (the per-star MI-EFE
  dynamical asymptote, upper edge 1.10, banked in
  zimmerman-formula/real_research/reviews/wb_dr4_prereg_framework_curve.py which
  asserts 1.095 < asy_MI < 1.105 and computes the MI band 1.05-1.10).
  1.137 is the modified-GRAVITY (AQUAL-EFE point-field, framework nu) asymptote
  from the SAME banked script (assertion |asy_MG - 1.137| < 0.005) -- NOT the MI
  target. 1.33 is the conventional-MOND dynamic-range BENCHMARK injection
  (Milgrom a0 + simple-nu-scale EFE asymptote, the WB-literature value); it is
  not a framework number. FROZEN DEGENERACY CAVEAT (banked script, computed):
  Milgrom-a0 MI (1.134) ~ framework-a0 MG (1.139): gamma_v constrains the
  nu+EFE PRESCRIPTION, not the a0 value (22% a0 shift -> 3.3% gamma_v shift).

BOTH a0 FOOTINGS (ground rule 4): canonical 9.36e-11 (rho_DE/cH_Lambda) and
alt 1.13e-10 (rho_total/cH0). a0 enters binning (y = g_N/a0) and the transition
shape; the recovery is run under both.

OBSERVABLE: vtilde = v_perp / v_circ(s_proj),  v_circ = sqrt(G M_tot / s_proj).
Statistic: median(vtilde) in bins of y_proj = g_N(s_proj)/a0, compared to a
noise-convolved Newtonian forward-model MC (thermal f(e)=2e default; flat f(e)
alternative bracketed). Fit: 1-parameter deep asymptote gamma_inf with the
EFE-saturated transition shape
    gamma(y) = 1 + (gamma_inf - 1) * y_extN / (y_extN + y),
y_extN = Newtonian-inverted external field (banked g_ext,obs = 1.9 a0 physical,
1.778e-10 m/s^2; solar-neighborhood, McMillan-2017-class). A free multiplicative
nuisance kappa (per-bin common) absorbs eccentricity-calibration mismatch; it is
profiled out analytically. The SHAPE is matched between injection and recovery
by construction -- the gate tests RECOVERY OF THE ASYMPTOTE, not shape
discrimination; shape mis-specification is a flagged systematic for the real
DR4 run (the exact framework curve is the banked prereg script above).

GAIA ERROR MODEL (cited, flagged APPROX):
  DR3 per-star sigma_pm / sigma_plx vs G from Lindegren et al. 2021, A&A 649,
  A2 (Gaia EDR3 astrometric solution; ~0.02 mas/yr, 0.02-0.03 mas at G=15;
  ~0.07 mas/yr, 0.05-0.07 mas at G=17).
  DR4 = 66 vs 34 months: sigma_pm scales t^-1.5 -> x0.372; sigma_plx t^-0.5
  -> x0.718 (Gaia mission nominal scaling; DR4 expected-performance pages).
  Mass calibration: per-pair 5% Gaussian (Banik & al. 2024 MNRAS 527, 4573
  quote few-%; their eq. 6 M_G->M cubic is used for the dry-run masses).

DRY RUN DATA (--dry-run): El-Badry, Rix & Heintz 2021 (MNRAS 506, 2269) Gaia
eDR3 wide-binary catalog, local copy
  zimmerman-formula/real_research/data/widebinaries/all_columns_catalog.fits.gz
(Zenodo 4435257). Cuts transcribed from the banked replication
  zimmerman-formula/real_research/data/widebinaries/wb_exact_replication.py
(Banik-like core + mass + parallax-consistency cuts, RUWE<1.4 substituting his
astrometric chi2/nu, + R_chance_align<0.01 added here to suppress chance
alignments). CLEARLY LABELED: DR3-ERA DRY RUN, NOT THE DR4 TEST. Known
caveats: no DR3-RV triple screen, no faint-companion search -> LOOSER than
Banik's 8,611 -> more contaminated -> gamma biased HIGH; Chae 2023 (ApJ 952,
128) vs Banik 2024 dispute is precisely about these choices. Result reported
as-is, honest either way.

GATE (no hard-coded passes): inject gamma_inf in {1.00, 1.09, 1.33} into
synthetic DR4-level catalogs (N=30,000 pairs; Banik DR3 strict = 8.6k, Chae
loose = 26k, DR4 66-month + fainter makes 30k plausible), recover, and require
|recovered - injected| < max(2 sigma_fit, 0.02). Reports the recovered values,
sigma(gamma_inf), and N needed to separate 1.09 from 1.00 at 3 sigma.

exit 0 iff all gates pass (dry run is reported, never gated).
C. Zimmerman prep campaign, 2026-07-16.
"""
import argparse, os, sys
import numpy as np

# ----------------------------------------------------------------------
# Constants + banked inputs
# ----------------------------------------------------------------------
G    = 6.674e-11
MSUN = 1.989e30
AU   = 1.496e11
KAU  = 1e3*AU
PC   = 3.0857e16

A0_CAN = 9.36e-11        # canonical: rho_DE / cH_Lambda footing (banked)
A0_ALT = 1.13e-10        # alt footing: rho_total / cH0 (banked fork)
GEXT_PHYS = 1.9*A0_CAN   # 1.778e-10 m/s^2 physical (banked solar-neighborhood)

# ----------------------------------------------------------------------
# TARGETS -- RETARGETED TO AMENDMENT 8 (2026-08-03), "Route A".
# The chain moved this constant four times and this file had not followed it:
#     frozen 1.09 -> Amdt 3 1.0246 -> Amdt 4(d)/7 1.0310 -> Amdt 8 1.1582
# Amendment 8 adopted the EXPONENTIAL kernel nu = 1/(1 - e^-sqrt(y)) because BOTH
# power-law kernels fail the solar system (alpha=1 by 1279x the Earth/Mars bound;
# alpha=2 by 8.5-12.4x the Mars ranging budget, its 1/g tail binding at the SUN via
# the Jupiter reflex ~2233 a0, not at a planet).
# Audited by real_research/reviews/mi_dr4_readiness_audit_2026.py (28 checks, exit 0).
# NOTHING FROZEN IS TOUCHED BY THIS EDIT: the cut table, estimator, error model,
# NSS screen, bin edges, kappa anchor and N = 30,000 are all unchanged.
# ----------------------------------------------------------------------
GAMMA_MI  = 1.1582       # IN FORCE, Amdt 8: orientation-averaged, radial convention
GAMMA_MI_RANGE_RAD = (1.1311, 1.1964)   # Amdt 8, radial convention
GAMMA_MI_RANGE_MAG = (1.1339, 1.2007)   # Amdt 8, MAGNITUDE convention (sec 1.1's headline)
GAMMA_MG  = 1.137        # framework-as-MG (AQUAL-EFE, framework nu; banked/frozen)
GAMMA_MOND= 1.33         # conventional-MOND benchmark injection (not framework)

# Amendment 8 declared risks, implemented below rather than left in the document:
KAPPA_WINDOW    = (0.95, 1.05)   # frozen; outside => "systematic-limited, no verdict"
NOVERDICT_EDGE  = 1.20           # frozen; a MAGNITUDE-convention result above this is
                                 # PRE-DECLARED UNSCOREABLE (Amdt 8 risk (d): the
                                 # alt-footing/primary corner is 1.20069, 0.00069 above)

# ----------------------------------------------------------------------
# FROZEN DR4 CUT LIST (pre-registered 2026-07-16; see PREREGISTRATION_DR4.md
# section 1 for the per-cut justifications + citations). The DR4 catalog fed
# to --catalog MUST be built with exactly these cuts; the strictness LADDER
# below is reported alongside, never substituted for the primary.
# ----------------------------------------------------------------------
FROZEN_DR4_CUTS = [
    ("|b_gal|",            "> 15 deg",                 "Banik+2024 sec 2.1"),
    ("G mag",              "< 17 both components",     "Banik+2024 sec 2.1"),
    ("distance",           "< 250 pc (plx > 4 mas)",   "Banik+2024 sec 2.1"),
    ("parallax S/N",       ">= 40 both components",    "dist err <2.5% -> vt err <4%, subdominant to 5% mass"),
    ("plx consistency",    "|d1-d2| < min(4 sigma, 8 pc)", "Banik+2024 sec 2.1"),
    ("proj. separation",   "2 < s < 30 kAU",           "Banik+2024; r_M(1Msun)~7 kAU inside window"),
    ("RUWE",               "< 1.4 both",               "Lindegren+2021; Belokurov+2020 companion tracer"),
    ("ipd_frac_multi_peak","<= 2 both",                "Banik+2024 sec 2.4.3 (resolved blends)"),
    ("extinction",         "A_V < 0.5",                "Banik+2024 sec 2.4.1"),
    ("total mass",         "0.464 < M_tot < 4.31 Msun","Banik+2024 eq.6 cubic validity M_G in [0.6,11.1]"),
    ("RV screen",          "reject |dRV| > max(3 sigma_dRV, 3 v_c(s))", "Banik+2024 sec 2.4.5, DR4 RVs both comps"),
    ("NSS screen (NEW)",   "reject any DR4 non-single-star soln either comp", "DR4 66-mo epoch astrometry: direct inner-companion detector"),
    ("triple search",      "no co-moving 3rd source G<20 within 30 kAU", "Banik+2024 faint-companion search analog"),
    ("chance alignment",   "R_chance_align < 0.01",    "Chae 2023 sec 2.1; El-Badry+2021 statistic"),
    ("vtilde error",       "sigma(vt) <= 0.1 max(1, vt/2)", "Banik+2024 eq.10 (bounds deep-bin noise inflation)"),
    ("vtilde cap",         "NONE at catalog level; estimator VTCAP=6.0 only",
                           "symmetric data/model treatment (Banik vt<=5 NOT adopted for DR4)"),
]
FROZEN_LADDER = ("RUWE 1.4->1.2 | R_chance 0.01->0.001 | sep 2-30 -> 3-20 kAU | "
                 "RV-screened subsample only | NSS screen off (contamination probe)")

def y_newt_from_obs(y_obs):
    """Invert g_obs = sqrt(g_N^2 + g_N a0) (framework nu) -> y_N."""
    return 0.5*(-1.0 + np.sqrt(1.0 + 4.0*y_obs**2))

def y_extN(a0):
    return y_newt_from_obs(GEXT_PHYS/a0)

def gamma_of_y(y, ginf, yE):
    """EFE-saturated velocity-boost transition (declared shape; see header)."""
    return 1.0 + (ginf-1.0)*yE/(yE + y)

# ----------------------------------------------------------------------
# Gaia error model (APPROX, cited in header)
# ----------------------------------------------------------------------
_GGRID    = np.array([ 6.,  12.,  14.,  15.,  16.,  17.,  18.,  19.,  20.])
_SPM_DR3  = np.array([.016, .014, .016, .020, .035, .070, .140, .300, .700])  # mas/yr
_SPLX_DR3 = np.array([.021, .016, .019, .025, .040, .070, .130, .250, .600])  # mas
PM_FAC_DR4, PLX_FAC_DR4 = (66/34.)**-1.5, (66/34.)**-0.5   # 0.372, 0.718

def sigma_pm(Gmag, dr4):  return np.interp(Gmag, _GGRID, _SPM_DR3) *(PM_FAC_DR4 if dr4 else 1.0)
def sigma_plx(Gmag, dr4): return np.interp(Gmag, _GGRID, _SPLX_DR3)*(PLX_FAC_DR4 if dr4 else 1.0)

# Banik+2024 eq.6 cubic M_G(ln M) -- used for G mags in the MC and dry-run masses
_xg  = np.linspace(-1.46, 0.99, 4000)
_MGg = 4.887 - 5.693*_xg + 0.4164*_xg**2 + 0.9611*_xg**3
_o   = np.argsort(_MGg); _MGs, _xs = _MGg[_o], _xg[_o]
def MG_of_mass(m):  return np.interp(np.log(m), _xg, _MGg)
def mass_of_MG(MG): return np.exp(np.interp(np.clip(MG, 0.6, 11.1), _MGs, _xs))

# ----------------------------------------------------------------------
# Population MC (Keplerian orbits, projection, Gaia noise)
# ----------------------------------------------------------------------
def make_population(N, rng, dr4=True, dmax_pc=250., smin_kAU=2., smax_kAU=30.,
                    Gcut=17., ecc='thermal'):
    """Returns observables sufficient to evaluate vtilde at ANY gamma_inf/a0:
    the boost multiplies the TRUE relative velocity (evaluated at the TRUE 3D
    internal acceleration), noise is added after. Phenomenological boost
    injection (velocity scaling at fixed orbit), the standard Chae/Banik-style
    MC shortcut; self-consistent modified-orbit integration is the flagged
    upgrade path (cf. banked wb_mond_orbit_mc.py)."""
    # oversample; selection trims
    M1 = rng.uniform(0.45, 1.25, N)
    q  = rng.uniform(0.30, 1.00, N)
    M2 = np.clip(q*M1, 0.15, None)
    Mt = M1 + M2
    d  = (rng.uniform(25.**3, dmax_pc**3, N))**(1/3.)          # volume-ish
    p  = -0.6                                                   # a^-1.6 (Opik-like)
    lo, hi = (smin_kAU*0.5)**p, (smax_kAU*2.0)**p
    a_sma = (rng.uniform(hi, lo, N))**(1/p) * KAU               # semi-major axis, m
    if ecc == 'thermal': e = np.sqrt(rng.uniform(0, 1, N))      # f(e)=2e
    else:                e = rng.uniform(0, 1, N)               # flat bracket
    # Kepler solve, mean anomaly uniform (uniform in time)
    Ma = rng.uniform(0, 2*np.pi, N); E = Ma.copy()
    for _ in range(60):
        E -= (E - e*np.sin(E) - Ma)/(1 - e*np.cos(E))
    n  = np.sqrt(G*Mt*MSUN/a_sma**3)
    b_ = a_sma*np.sqrt(1-e**2)
    xo, yo   = a_sma*(np.cos(E)-e), b_*np.sin(E)
    Ed       = n/(1-e*np.cos(E))
    vxo, vyo = -a_sma*np.sin(E)*Ed, b_*np.cos(E)*Ed
    # isotropic orientation: P,Q basis from (Om, cos i, w)
    Om, w = rng.uniform(0, 2*np.pi, N), rng.uniform(0, 2*np.pi, N)
    ci = rng.uniform(-1, 1, N); si = np.sqrt(1-ci**2)
    cO, sO, cw, sw = np.cos(Om), np.sin(Om), np.cos(w), np.sin(w)
    P = np.stack([cO*cw - ci*sO*sw,  sO*cw + ci*cO*sw, si*sw])
    Q = np.stack([-cO*sw - ci*sO*cw, -sO*sw + ci*cO*cw, si*cw])
    r3 = xo*P + yo*Q                                            # (3,N) m
    v3 = vxo*P + vyo*Q                                          # (3,N) m/s
    # vis-viva sanity (not a gate; numerical correctness check)
    r_ = np.linalg.norm(r3[:, :2000], axis=0)
    vv = np.sum(v3[:, :2000]**2, axis=0)
    assert np.allclose(vv, G*Mt[:2000]*MSUN*(2/r_ - 1/a_sma[:2000]), rtol=1e-8)
    r3d    = np.linalg.norm(r3, axis=0)
    s_proj = np.hypot(r3[0], r3[1])                             # z = LOS
    g_true = G*Mt*MSUN/r3d**2                                   # TRUE internal accel
    # Gaia noise
    G1 = MG_of_mass(M1) + 5*np.log10(d/10.)
    G2 = MG_of_mass(M2) + 5*np.log10(d/10.)
    spm  = np.sqrt(sigma_pm(G1, dr4)**2 + sigma_pm(G2, dr4)**2)         # rel-PM comp
    splx = 1/np.sqrt(sigma_plx(G1, dr4)**-2 + sigma_plx(G2, dr4)**-2)   # wtd-mean plx
    plx   = 1000./d
    d_obs = 1000./(plx + splx*rng.standard_normal(N))
    dkpc  = d/1000.
    pmx, pmy = v3[0]/(4.74e3*dkpc), v3[1]/(4.74e3*dkpc)         # TRUE rel PM, mas/yr
    npmx, npmy = spm*rng.standard_normal(N), spm*rng.standard_normal(N)
    s_obs = s_proj*(d_obs/d)
    M_obs = Mt*(1 + 0.05*rng.standard_normal(N))
    sel = ((s_obs > smin_kAU*KAU) & (s_obs < smax_kAU*KAU) & (d < dmax_pc)
           & (np.maximum(G1, G2) < Gcut) & (d_obs > 0) & (M_obs > 0.2))
    return dict(pmx=pmx[sel], pmy=pmy[sel], npmx=npmx[sel], npmy=npmy[sel],
                d_obs=d_obs[sel], s_obs=s_obs[sel], M_obs=M_obs[sel],
                g_true=g_true[sel],
                g_proj=G*M_obs[sel]*MSUN/s_obs[sel]**2,
                vc_obs=np.sqrt(G*M_obs[sel]*MSUN/s_obs[sel]))

def vtilde_of(pop, ginf, a0):
    """Observed vtilde with boost gamma(y_true) applied to the TRUE velocity."""
    gam = gamma_of_y(pop['g_true']/a0, ginf, y_extN(a0))
    vX  = (gam*pop['pmx'] + pop['npmx'])*4.74e3*(pop['d_obs']/1000.)
    vY  = (gam*pop['pmy'] + pop['npmy'])*4.74e3*(pop['d_obs']/1000.)
    return np.hypot(vX, vY)/pop['vc_obs']

# ----------------------------------------------------------------------
# Estimator: per-bin medians -> profile-chi2 fit of gamma_inf
# ----------------------------------------------------------------------
EDGES = np.array([-1.5, -1.1, -0.8, -0.5, -0.2, 0.1, 0.5, 1.0, 2.2])  # log10 y_proj
VTCAP = 6.0
MINBIN = 80

def bin_medians(logy, vt, boot=0, rng=None):
    med  = np.full(len(EDGES)-1, np.nan)
    sig  = np.full(len(EDGES)-1, np.nan)
    cnt  = np.zeros(len(EDGES)-1, int)
    for b in range(len(EDGES)-1):
        m = (logy >= EDGES[b]) & (logy < EDGES[b+1]) & (vt < VTCAP)
        cnt[b] = m.sum()
        if cnt[b] < MINBIN: continue
        v = vt[m]
        med[b] = np.median(v)
        if boot:
            bs = np.median(v[rng.integers(0, len(v), (boot, len(v)))], axis=1)
            sig[b] = bs.std(ddof=1)
    return med, sig, cnt

def model_medians(pop_master, a0, grid, rng):
    """Grid of model bin-medians + the model's own finite-MC median error
    (bootstrap at a reference gamma; the error scale is gamma-insensitive).
    The model error MUST be propagated: it is coherent across the grid and,
    if ignored, shows up as a +-1-2% pseudo-bias on gamma (found at the gate
    with a 5e5 master; the master is sized so it is subdominant)."""
    logy = np.log10(pop_master['g_proj']/a0)
    out = np.full((len(grid), len(EDGES)-1), np.nan)
    for i, g in enumerate(grid):
        vt = vtilde_of(pop_master, g, a0)
        out[i], _, _ = bin_medians(logy, vt)
    vt_ref = vtilde_of(pop_master, 1.15, a0)
    _, sig_m, _ = bin_medians(logy, vt_ref, boot=100, rng=rng)
    return out, sig_m

ANCHOR = EDGES[:-1] >= 0.5   # high-acceleration bins: pin kappa there (boost ~1)

def fit_gamma(med_d, sig_d, mod, grid):
    """chi2 over gamma grid. The nuisance kappa is ANCHORED on the
    high-acceleration bins (log10 y_proj >= 0.5, where the boost is ~1 for all
    gamma on the grid) as a Gaussian prior, then profiled analytically over the
    deep bins. A fully-free kappa is DEGENERATE with gamma (flat chi2 valley)
    and biases the recovery low by ~0.01-0.05 -- found and fixed at the gate.
    sig combines the data bootstrap error and the model's finite-MC error."""
    mod_med, mod_sig = mod
    sig_d = np.sqrt(sig_d**2 + mod_sig**2)
    ok = np.isfinite(med_d) & np.isfinite(sig_d) & np.all(np.isfinite(mod_med), 0)
    anc, dep = ok & ANCHOR, ok & ~ANCHOR
    if anc.sum() < 1 or dep.sum() < 2:      # fallback: free-kappa profile
        anc, dep = ok, ok
    da, sa, Ma = med_d[anc], sig_d[anc], mod_med[:, anc]
    dd, sd, Md = med_d[dep], sig_d[dep], mod_med[:, dep]
    k_hat = (Ma*da/sa**2).sum(1)/(Ma**2/sa**2).sum(1)          # per grid pt
    vk    = 1.0/(Ma**2/sa**2).sum(1)                            # sigma_k^2
    # profile k over deep bins with prior N(k_hat, vk):
    A = (Md**2/sd**2).sum(1) + 1.0/vk
    B = (Md*dd/sd**2).sum(1) + k_hat/vk
    kap  = B/A
    chi2 = ((dd**2/sd**2).sum() + k_hat**2/vk) - B**2/A
    i0 = int(np.argmin(chi2))
    c = chi2 - chi2[i0]
    lo = grid[c <= 1.0].min(); hi = grid[c <= 1.0].max()
    return grid[i0], max(0.5*(hi-lo), 0.5*(grid[1]-grid[0])), chi2[i0], \
        int(ok.sum()), kap[i0]

GRID = np.arange(0.90, 1.5001, 0.0025)

def report_7e(g, sg, kap, label):
    """AMENDMENT 7(e)/8 SCORING, implemented rather than left in the document.

    The rule: report the RAW gamma_hat with sigma_fit and BOTH distances -- to
    Newton (1.000) and to the in-force framework-MI target -- and NEVER a single
    verdict word. It is load-bearing here because Amendment 8's own prediction
    1.1582 falls in the frozen table's bin pre-declared "MG-side; MI disfavored",
    and the frozen MG target 1.137 lies INSIDE the MI range, so any
    proximity-based label would misreport the framework's own prediction.

    Also emits Amendment 8's two declared risks:
      (c) kappa outside the frozen window => "systematic-limited, no verdict";
      (d) a MAGNITUDE-convention result above 1.20 => PRE-DECLARED UNSCOREABLE.
    """
    d_newt = (g - 1.0) / sg if sg > 0 else float("nan")
    d_mi = (g - GAMMA_MI) / sg if sg > 0 else float("nan")
    print(f"    [7(e)] raw gamma_hat = {g:.4f}, sigma_fit = {sg:.4f}; "
          f"distance to Newton 1.000 = {d_newt:+.2f} sigma_fit; "
          f"to framework-MI {GAMMA_MI:.4f} = {d_mi:+.2f} sigma_fit")
    print(f"    [7(e)] MI ranges carried: radial {GAMMA_MI_RANGE_RAD}, "
          f"magnitude {GAMMA_MI_RANGE_MAG}.  No verdict word is emitted by design.")
    flags = []
    if not (KAPPA_WINDOW[0] <= kap <= KAPPA_WINDOW[1]):
        flags.append(f"SYSTEMATIC-LIMITED, NO VERDICT -- nuisance kappa = {kap:.4f} is "
                     f"OUTSIDE the frozen window {KAPPA_WINDOW} (Amdt 8 risk (c); its "
                     f"declared consequence is 'reported, not repaired')")
    if g > NOVERDICT_EDGE:
        flags.append(f"PRE-DECLARED UNSCOREABLE on the MAGNITUDE convention -- "
                     f"gamma_hat = {g:.4f} exceeds the {NOVERDICT_EDGE} no-verdict edge "
                     f"(Amdt 8 risk (d))")
    for f_ in flags:
        print(f"    [7(e)] *** {f_} ***")
    if not flags:
        print(f"    [7(e)] no declared risk tripped (kappa = {kap:.4f} inside "
              f"{KAPPA_WINDOW}; gamma_hat below the {NOVERDICT_EDGE} edge)")
    return d_newt, d_mi, flags


def run_fit(data_logy, data_vt, mod, rng, label, kap_note=""):
    med_d, sig_d, cnt = bin_medians(data_logy, data_vt, boot=200, rng=rng)
    g, sg, chi2, nb, kap = fit_gamma(med_d, sig_d, mod, GRID)
    print(f"  {label:34s} gamma_inf = {g:.4f} +- {sg:.4f}  "
          f"(chi2/bin={chi2/max(nb-2,1):.2f}, bins={nb}, kappa={kap:.4f}){kap_note}")
    report_7e(g, sg, kap, label)
    return g, sg, med_d, sig_d, cnt

# ----------------------------------------------------------------------
# Generic catalog ingestion (the DR4 entry point)
# ----------------------------------------------------------------------
def ingest_csv(path):
    """CSV columns: sep_kAU, v_perp_kms, M1_msun, M2_msun, d_pc.
    OPTIONAL, for the anisotropy falsifier: l_gal, b_gal (degrees) and pa_deg, the
    separation's position angle east of north.  If absent the anisotropy check declines
    to run and says so -- it must never silently skip."""
    import csv
    rows = list(csv.DictReader(open(path)))
    s  = np.array([float(r['sep_kAU'])   for r in rows])*KAU
    vp = np.array([float(r['v_perp_kms'])for r in rows])*1e3
    Mt = np.array([float(r['M1_msun'])+float(r['M2_msun']) for r in rows])
    gN = G*Mt*MSUN/s**2
    vt = vp/np.sqrt(G*Mt*MSUN/s)
    extra = {}
    for col in ('l_gal', 'b_gal', 'pa_deg'):
        if rows and col in rows[0]:
            extra[col] = np.array([float(r[col]) for r in rows])
    return gN, vt, extra


# ----------------------------------------------------------------------
# CHECKLIST ITEM 5 -- THE ANISOTROPY FALSIFIER (Amendment 2's pre-declared SIGN,
# strengthened by Amendment 8's Route A).  Perpendicular pairs must show the LARGER
# boost; the OPPOSITE sense at >= 3 sigma falsifies the derived external-field effect
# independently of the aggregate gamma_v.
#   Route A eigenvalues:  canonical gamma_par 1.03800 / gamma_perp 1.21385 (spread 0.17585)
#                         alt       gamma_par 1.05977 / gamma_perp 1.25916 (spread 0.19939)
# POWER, computed in real_research/reviews/mi_dr4_anisotropy_and_gated_2026.py (20/20):
# only the SKY-PROJECTED angle is observable, and the projection dilution over the frozen
# |b| > 15 deg sky is D = 0.2367 (in-plane closed form 4/(3 pi) = 0.4244), so the
# OBSERVABLE split is 0.042-0.047 and reaches only 1.00-1.13 sigma at N = 30,000.
# *** 3 sigma needs N ~ 2.1-2.7e5, SEVEN TO NINE TIMES the frozen sample. ***  Reported as
# a directional check with its N attached, never as a test this sample settles.
# ----------------------------------------------------------------------
ANISO_EIG = {"canonical": (1.03800, 1.21385), "alt": (1.05977, 1.25916)}
ANISO_DILUTION = 0.2367

def anisotropy_split(gN, vt, extra, mod, rng, a0, label):
    """Split by the projected angle between the separation and the Galactic-centre
    direction, fit gamma in each half, and report the difference against the
    pre-declared sign.  Declines loudly if the needed columns are absent."""
    need = ('l_gal', 'b_gal', 'pa_deg')
    if not all(c in extra for c in need):
        print(f"  [aniso] {label}: DECLINED -- needs columns {need}; "
              f"present: {sorted(extra) or 'none'}.  Not skipped silently.")
        return None
    l, b, pa = np.radians(extra['l_gal']), np.radians(extra['b_gal']), np.radians(extra['pa_deg'])
    # position angle of the projected Galactic-centre direction at (l, b):
    # the GC lies at l=0,b=0; its projection onto the sky at the star's position has
    # PA_gc = atan2(-sin(l) cos(b_gc)=... ) -- for |b|>15 deg the dominant term is the
    # gradient of Galactic longitude, so use the standard great-circle bearing to (0,0).
    pa_gc = np.arctan2(np.sin(-l), np.cos(b)*np.tan(0.0) - np.sin(b)*np.cos(-l))
    dphi = np.abs(np.arctan2(np.sin(pa - pa_gc), np.cos(pa - pa_gc)))
    dphi = np.minimum(dphi, np.pi - dphi)            # fold to [0, pi/2]
    par = dphi < np.pi/4
    out = {}
    for nm, sel in (("proj-PARALLEL", par), ("proj-PERPENDICULAR", ~par)):
        if sel.sum() < 200:
            print(f"  [aniso] {label}: {nm} half has only {sel.sum()} pairs (<200); not fitted")
            continue
        g, sg, *_ = run_fit(np.log10(gN[sel]/a0), vt[sel], mod, rng, f"{label} {nm}")
        out[nm] = (g, sg)
    if len(out) == 2:
        (gp, sp_), (gq, sq) = out["proj-PARALLEL"], out["proj-PERPENDICULAR"]
        d, sd = gq - gp, np.hypot(sp_, sq)
        z = d/sd if sd > 0 else float('nan')
        print(f"  [aniso] {label}: gamma_perp - gamma_par = {d:+.4f} +- {sd:.4f} "
              f"({z:+.2f} sigma).  PRE-DECLARED SIGN: POSITIVE (perpendicular larger).")
        print(f"  [aniso] expected observable split {ANISO_DILUTION*ANISO_EIG['canonical'][1]-ANISO_DILUTION*ANISO_EIG['canonical'][0]:+.4f} "
              f"(3-D spread x dilution {ANISO_DILUTION}); 3 sigma needs N ~ 2.1-2.7e5, so at the "
              f"frozen N this is a DIRECTIONAL check, not decisive.")
        if z <= -3:
            print("  [aniso] *** WRONG SENSE AT >= 3 SIGMA: this FALSIFIES the derived "
                  "external-field effect independently of the aggregate gamma_v (Amendment 2) ***")
    return out


# ----------------------------------------------------------------------
# CHECKLIST ITEM 6 -- THE GATED BRANCH AS A SECOND SCORED HYPOTHESIS.  Trap count STAYS 2,
# so both branches are scored.  Amendment 8: gamma_gated = 1.00064-1.00117 at 10 kAU, with
# Route A making the amplitude EXACTLY the kernel's Newtonian residual S = 1 - mu =
# e^-sqrt(y); NOT flat across the window -- 0.001 sigma_fit at 2 kAU rising to 1.56
# sigma_fit by 30 kAU, so falsifiable WITHIN the window by its SHAPE.
# *** AGAINST INTEREST, computed: in the AGGREGATE the gated branch is 0.03-0.06 sigma from
# Newton at the frozen N and would need N ~ 8.6e7 to separate.  An aggregate-only scorer
# would report "Newtonian" for a universe in which the gated branch is TRUE. ***
# ----------------------------------------------------------------------
GAMMA_GATED_10KAU = (1.00064, 1.00117)
GATED_RISE_SIGMA  = (0.001, 1.56)        # at 2 kAU and at 30 kAU (Amendment 8)

def score_gated(g, sg, label):
    """Report the gated branch alongside the ungated one, with its own power."""
    lo, hi = GAMMA_GATED_10KAU
    d_lo, d_hi = (g - lo)/sg, (g - hi)/sg
    print(f"  [gated] {label}: distance to the GATED branch "
          f"({lo:.5f}-{hi:.5f} at 10 kAU) = {d_hi:+.2f} to {d_lo:+.2f} sigma_fit")
    print(f"  [gated] its aggregate separation from Newton is only "
          f"{(hi-1)/sg:.3f} sigma at this precision (needs N ~ 8.6e7), so the AGGREGATE "
          f"cannot distinguish gated from Newtonian -- the handle is the INTERNAL RISE, "
          f"{GATED_RISE_SIGMA[0]} sigma_fit at 2 kAU to {GATED_RISE_SIGMA[1]} at 30 kAU.")
    print(f"  [gated] 1.56 sigma is not 3: registered as a WATCH item, not a decisive test.")
    return d_lo, d_hi

# ----------------------------------------------------------------------
# DR3-era dry run: El-Badry+2021 catalog, Banik-like cuts (transcribed from
# the banked wb_exact_replication.py)
# ----------------------------------------------------------------------
ELBADRY = ('/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/'
           'data/widebinaries/all_columns_catalog.fits.gz')

def load_elbadry():
    from astropy.io import fits
    C = ['ra1','dec1','parallax1','parallax2','parallax_error1','parallax_error2',
         'pmra1','pmra2','pmdec1','pmdec2','pmra_error1','pmra_error2',
         'pmdec_error1','pmdec_error2','ruwe1','ruwe2','ipd_frac_multi_peak1',
         'ipd_frac_multi_peak2','phot_g_mean_mag1','phot_g_mean_mag2','sep_AU',
         'R_chance_align']
    with fits.open(ELBADRY, memmap=True) as h:
        d = h[1].data
        D = {k: np.array(d[k], dtype='f8') for k in C}
    aN, dN = np.radians(192.85948), np.radians(27.12825)
    ra, dec = np.radians(D['ra1']), np.radians(D['dec1'])
    b = np.degrees(np.arcsin(np.sin(dec)*np.sin(dN)
                             + np.cos(dec)*np.cos(dN)*np.cos(ra-aN)))
    d1, d2 = 1000/D['parallax1'], 1000/D['parallax2']
    dist = 0.5*(d1+d2); skAU = D['sep_AU']/1e3
    sd1 = 1000*D['parallax_error1']/D['parallax1']**2
    sd2 = 1000*D['parallax_error2']/D['parallax2']**2
    sdd = np.hypot(sd1, sd2)
    MG1 = D['phot_g_mean_mag1'] - 5*np.log10(dist/10)
    MG2 = D['phot_g_mean_mag2'] - 5*np.log10(dist/10)
    Mt  = mass_of_MG(MG1) + mass_of_MG(MG2)
    s   = D['sep_AU']*AU
    dpm = np.hypot(D['pmra1']-D['pmra2'], D['pmdec1']-D['pmdec2'])
    vsky = 4.74*dpm*(dist/1000)                                  # km/s
    vN  = np.sqrt(G*Mt*MSUN/s)/1e3
    vt  = vsky/vN
    mask = ((np.abs(b) > 15) & (D['phot_g_mean_mag1'] < 17)
            & (D['phot_g_mean_mag2'] < 17) & (dist < 250)
            & (D['ruwe1'] < 1.4) & (D['ruwe2'] < 1.4)
            & (skAU > 2) & (skAU < 30)
            & (D['ipd_frac_multi_peak1'] <= 2) & (D['ipd_frac_multi_peak2'] <= 2)
            & (Mt > 0.464) & (Mt < 4.31) & (vt <= 5)
            & (np.abs(d1-d2) < np.minimum(4*sdd, 8))
            & (D['R_chance_align'] < 0.01))
    gN = G*Mt*MSUN/s**2
    return gN[mask], vt[mask], int(mask.sum())

# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true',
                    help='run the DR3-era El-Badry dry run (slow: 1.4 GB fits.gz)')
    ap.add_argument('--catalog', default=None,
                    help='CSV catalog (sep_kAU,v_perp_kms,M1_msun,M2_msun,d_pc)')
    ap.add_argument('--n-data', type=int, default=30000)
    ap.add_argument('--seed', type=int, default=20261216)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    print("="*78)
    print("DOOR 4A -- GAIA DR4 WIDE-BINARY PIPELINE (prep, 2026-07-16)")
    print("="*78)
    print(f"a0 canonical {A0_CAN:.3e} (y_extN={y_extN(A0_CAN):.4f}) | "
          f"alt {A0_ALT:.3e} (y_extN={y_extN(A0_ALT):.4f})")
    print(f"targets: Newton 1.00 < MI {GAMMA_MI} (banked; NOT 1.137) < "
          f"MG {GAMMA_MG} < MOND benchmark {GAMMA_MOND}")
    print("\n[FROZEN DR4 CUTS] (pre-registered 2026-07-16; PREREGISTRATION_DR4.md)")
    for cut, val, why in FROZEN_DR4_CUTS:
        print(f"  {cut:20s} {val:48s} [{why}]")
    print(f"  strictness ladder: {FROZEN_LADDER}")

    # -------- master model MC (DR4 noise) --------
    print("\n[model MC] building master population (DR4-level noise) ...")
    NM = 3_000_000   # sized so the model's finite-MC error is subdominant
    pop_m = make_population(NM, rng, dr4=True)
    print(f"  master MC pairs after selection: {len(pop_m['s_obs'])}")
    mod_can = model_medians(pop_m, A0_CAN, GRID, rng)
    mod_alt = model_medians(pop_m, A0_ALT, GRID, rng)

    # -------- GATE: synthetic injections --------
    print(f"\n[GATE] synthetic DR4 catalogs, N_data={args.n_data} "
          f"(injection: boost at TRUE 3D y, canonical a0; recovery below)")
    gate_ok, results = True, {}
    for ginj in (1.00, GAMMA_MI, GAMMA_MOND):
        pop_d = make_population(int(args.n_data*2.7), rng, dr4=True)
        keep = rng.permutation(len(pop_d['s_obs']))[:args.n_data]
        pop_d = {k: v[keep] for k, v in pop_d.items()}
        vt_d   = vtilde_of(pop_d, ginj, A0_CAN)
        ly_can = np.log10(pop_d['g_proj']/A0_CAN)
        ly_alt = np.log10(pop_d['g_proj']/A0_ALT)
        ndeep = int(((pop_d['g_proj']/A0_CAN) < 0.3).sum())
        print(f" inject gamma_inf = {ginj:.2f}  (N={args.n_data}, deep y<0.3: {ndeep})")
        g_c, s_c, *_ = run_fit(ly_can, vt_d, mod_can, rng, "recover [a0 canonical]")
        g_a, s_a, *_ = run_fit(ly_alt, vt_d, mod_alt, rng, "recover [a0 alt footing]")
        tol = max(2*s_c, 0.02)
        ok = abs(g_c - ginj) < tol
        gate_ok &= ok
        results[ginj] = (g_c, s_c, g_a, s_a, ndeep)
        print(f"  GATE @{ginj:.2f}: |{g_c:.4f}-{ginj:.2f}|={abs(g_c-ginj):.4f} "
              f"< tol {tol:.4f} -> {'PASS' if ok else 'FAIL'}")

    # spread check: independent realizations at the MI target
    print("\n[spread check] 8 independent catalogs @ gamma=1.09 (canonical fit)")
    gs = []
    for _ in range(8):
        pop_d = make_population(int(args.n_data*2.7), rng, dr4=True)
        keep = rng.permutation(len(pop_d['s_obs']))[:args.n_data]
        pop_d = {k: v[keep] for k, v in pop_d.items()}
        vt_d = vtilde_of(pop_d, GAMMA_MI, A0_CAN)
        med_d, sig_d, _ = bin_medians(np.log10(pop_d['g_proj']/A0_CAN), vt_d,
                                      boot=200, rng=rng)
        g, sg, *_ = fit_gamma(med_d, sig_d, mod_can, GRID)
        gs.append(g)
    gs = np.array(gs)
    print(f"  realizations: mean={gs.mean():.4f} rms={gs.std(ddof=1):.4f} "
          f"(profile-sigma above should be comparable)")

    # -------- sample size for 3-sigma separation 1.09 vs 1.00 --------
    s09 = results[GAMMA_MI][1]
    sig_eff = max(s09, gs.std(ddof=1))         # conservative of the two
    N3 = args.n_data * (3*sig_eff/(GAMMA_MI-1.00))**2
    fdeep = results[GAMMA_MI][4]/args.n_data
    print(f"\n[separation] sigma(gamma) = {sig_eff:.4f} at N={args.n_data} "
          f"-> 3-sigma separation of 1.09 vs 1.00 needs N ~ {N3:,.0f} pairs "
          f"(~{N3*fdeep:,.0f} deep y<0.3), under this population/selection.")
    N3_mond = args.n_data * (3*sig_eff/(GAMMA_MOND-GAMMA_MI))**2
    print(f"             separating MOND benchmark 1.33 from MI 1.09 at 3 sigma: "
          f"N ~ {N3_mond:,.0f}.")
    N3_mg = args.n_data * (3*sig_eff/(GAMMA_MG-GAMMA_MI))**2
    print(f"             separating MG {GAMMA_MG} from MI {GAMMA_MI} at 3 sigma: "
          f"N ~ {N3_mg:,.0f} (statistical only; the frozen sys allowance 0.02 "
          f"makes MI-vs-MG UNDECIDED unless systematics beat ~0.01).")

    # -------- eccentricity-bracket systematic --------
    print("\n[ecc bracket] recovery of 1.09 when the TRUE population is FLAT f(e)")
    pop_f = make_population(int(args.n_data*2.7), rng, dr4=True, ecc='flat')
    keep = rng.permutation(len(pop_f['s_obs']))[:args.n_data]
    pop_f = {k: v[keep] for k, v in pop_f.items()}
    vt_f = vtilde_of(pop_f, GAMMA_MI, A0_CAN)
    gf, sf, *_ = run_fit(np.log10(pop_f['g_proj']/A0_CAN), vt_f, mod_can, rng,
                         "flat-e truth vs thermal-e model",
                         "  <- ecc systematic (kappa absorbs most)")
    print(f"  ecc-mismatch shift on gamma: {gf-GAMMA_MI:+.4f} "
          f"(FLAGGED systematic; Hwang+2022 superthermal at wide s)")

    # -------- optional real-catalog runs --------
    if args.catalog:
        gN, vt, extra = ingest_csv(args.catalog)
        print(f"\n[catalog] {args.catalog}: N={len(vt)}")
        for fnm, a0v, modv in (("canonical", A0_CAN, mod_can), ("alt footing", A0_ALT, mod_alt)):
            gc, sgc, *_ = run_fit(np.log10(gN/a0v), vt, modv, rng, f"catalog [a0 {fnm}]")
            score_gated(gc, sgc, f"catalog [a0 {fnm}]")          # checklist item 6
            anisotropy_split(gN, vt, extra, modv, rng, a0v, f"catalog [a0 {fnm}]")  # item 5

    if args.dry_run:
        print("\n" + "-"*78)
        print("DR3-ERA DRY RUN (El-Badry+2021 eDR3, Banik-like cuts) -- NOT the DR4 test")
        print("-"*78)
        gN, vt, n = load_elbadry()
        print(f"  pairs after cuts: {n} "
              f"(looser than Banik's 8,611: no chi2/nu, no faint-companion, no RV")
        print(f"   screen -> contamination biases gamma HIGH; interpret as a")
        print(f"   pipeline shakeout, not a verdict)")
        # DR3-noise model MC for an apples-to-apples forward model
        print("  building DR3-noise model MC ...")
        pop_m3 = make_population(NM, rng, dr4=False)
        mod3_can = model_medians(pop_m3, A0_CAN, GRID, rng)
        mod3_alt = model_medians(pop_m3, A0_ALT, GRID, rng)
        run_fit(np.log10(gN/A0_CAN), vt, mod3_can, rng, "El-Badry [a0 canonical]")
        run_fit(np.log10(gN/A0_ALT), vt, mod3_alt, rng, "El-Badry [a0 alt footing]")
        ndeep3 = int((gN/A0_CAN < 0.3).sum())
        print(f"  deep pairs (y<0.3, canonical): {ndeep3}")

    print("\n" + "="*78)
    print(f"PIPELINE SELF-TEST: {'PASS' if gate_ok else 'FAIL'} "
          f"(injected/recovered 1.00/{GAMMA_MI:.4f}/{GAMMA_MOND} within "
          f"max(2sigma, 0.02))")
    print("  This is a SELF-TEST of the estimator, NOT a scientific verdict on any")
    print("  measurement.  Per Amendment 7(e) no verdict word is emitted for data:")
    print("  see the [7(e)] lines above for raw gamma_hat, sigma_fit and both distances.")
    print("="*78)
    sys.exit(0 if gate_ok else 1)

if __name__ == '__main__':
    main()
