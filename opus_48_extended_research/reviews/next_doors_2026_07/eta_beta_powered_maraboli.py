#!/usr/bin/env python3
"""
POWERED eta(beta) TEST -- LANE C1 (DOI 10.5281/zenodo.21104820 discriminator)
=============================================================================
Upgrade of real_research/reviews/eta_beta_first_crude_CLASHVLT.py using the
published stacked CLASH-VLT anisotropy work:

  [M26] Maraboli, Biviano, Grillo, Pizzuti, Rosati, Mercurio, D'Addona 2026,
        A&A 708, A264 (arXiv:2602.15934): stacked beta(r) of NINE massive
        CLASH-VLT clusters, 72 MAMPOSSt + 18 Jeans-inversion combos.
        VERIFIED from arXiv HTML today: Table 1 (U18 lensing M200c, c200c),
        stack <R200c>=2.13+/-0.20 Mpc, M200c=(1.51+/-0.41)e15, cbar=2.7+/-1.5,
        r_beta=r_-2=<R200c>/cbar; MAMPOSSt stack (gT/gOM x NFW/HERN, "All"):
        beta0 in [0.34,0.57], betainf in [0.75,0.98]; JI beta-drop at ~250 kpc.
  [B26] Biviano et al. 2026, A&A 707, A153 (arXiv:2508.05195): per-cluster
        MAMPOSSt NFW (r200,rs) posteriors WITH U18 Gaussian lensing priors
        (8/9; M1115 kinematic-only, 2.5 sigma below lensing) + beta_sym(r200)
        68% intervals. VERIFIED from arXiv HTML today (their Tables 1,2).
  [D14] Donahue et al. 2014, ApJ 794,136 (arXiv:1405.7876) CLASH-X: Chandra +
        XMM hydrostatic NFW (vmax,rs) + r2500,M2500,fg2500,r500. VERIFIED from
        ar5iv HTML today (Tables 8,9; NFW machinery reproduces their M2500).

FRAMEWORK FOOTING (own terms): modified INERTIA; a0 = c^2 sqrt(Lambda/32pi)
= 9.36e-11 m/s^2 (canonical; fork 1.13e-10 also shown); OWN interpolation
nu(y)=sqrt(1+1/y) => M_pred(R500) = M_bar*sqrt(1+1/y_bar). a0 enters eta's
NORMALIZATION only; the slope test is a0-independent.

THE DISCRIMINATOR (banked note, DOI 21104820):
  MI: the deep-MOND normalization G M a0 = eta(beta) sigma^4 SLIDES UP with
      radial anisotropy (2.15 iso -> 2.8-3.0 at beta 0.3-0.5): Milgrom's MI
      functional is keyed to the orbit's acceleration AMPLITUDE (pericentre-
      dominated, rises with eccentricity), so radial orbits get LESS boost.
      MG (Milgrom 2014 PRD 89,024016 virial universality: AQUAL/QUMOND/AeST)
      and LCDM: anisotropy-INDEPENDENT (slope exactly 0).
  Operational mapping: Newtonian/MAMPOSSt kinematic mass under MI-truth:
      sigma^2 propto per-orbit boost Lambda(beta), M_kin ~ sigma^(2..3)
      => dln M_kin/dbeta = (1..1.5)*dln Lambda/dbeta < 0  (mass space)
      => kernel space dln etahat/dbeta = -(4/3)*that  > 0 (the note's +).
  Part 1 COMPUTES dln Lambda/dbeta by orbit integration in the M26 stack
  potential at the TRUE cluster accelerations (dilution measured, not
  assumed), bracketing Milgrom-2022's amplitude functional by the note's own
  set {harmonic mean, mean, rms} of |a| along the orbit (all exact in the
  circular limit). Then three measured slopes with injection calibration:
      R1: ln eta = ln[M500_kin/M_pred(R500)]   vs beta(r200)   [task's eta]
      R2: ln[M200_kin/M200_lensU18]            vs beta(r200)
      R3: ln[M500_kin/M500_X(Chandra)]         vs beta(r200)
  U18 priors partially pin the MAMPOSSt masses => the MI signal in ALL
  observables is attenuated by the per-cluster kinematic weight w_kin
  (computed from prior-vs-posterior widths); injections carry w_kin too.

BOTH-WAYS: the first crude point leaned flat-to-anti-MI. If the powered run
confirms, that is reported AT FULL WEIGHT (evidence against the framework's
MI realization on this front and for MG). Kill (ledger): calibrated anti-MI
at >2 sigma = the banked lean becomes a strike.
"""
import numpy as np
from scipy import stats, optimize

rng = np.random.default_rng(21104820)

# ---------------------------------------------------------------- constants
G      = 6.674e-11          # SI
MSUN   = 1.989e30
MPC    = 3.0857e22
KMS    = 1e3
H0     = 70.0*KMS/MPC       # s^-1  (h70, matching B26/M26/D14)
OM, OL = 0.3, 0.7
A0_CAN = 9.36e-11           # framework canonical a0
A0_FORK= 1.13e-10           # rho_total/cH0 footing fork (rule: show both)

def Ez(z):  return np.sqrt(OM*(1+z)**3 + OL)
def rhoc(z): return 3*(H0*Ez(z))**2/(8*np.pi*G)

def mu_nfw(x): return np.log(1+x) - x/(1+x)

def M_nfw(r, r200, rs, z):
    M200 = (4*np.pi/3)*200*rhoc(z)*(r200*MPC)**3
    return M200*mu_nfw(r/rs)/mu_nfw(r200/rs)

def r500_of(r200, rs, z):
    f = lambda r: M_nfw(r, r200, rs, z)/((4*np.pi/3)*(r*MPC)**3) - 500*rhoc(z)
    return optimize.brentq(f, 0.2*r200, 0.99*r200)

def M_vmax(r, vmax, rs):
    rmax = 2.163*rs
    return vmax**2*(rmax*MPC)/G * mu_nfw(r/rs)/mu_nfw(2.163)

# ------------------------------------------------------------------- data
# [B26 Table 2] MAMPOSSt kinematic NFW posteriors + beta_sym(r200) 68% CIs.
# name,z, r200_kin,err, rs_kin,err, bsym_lo,bsym_hi, r200_U18,err
B26 = [
 ("A209",  0.209, 2.31, 0.050, 0.66, 0.095,  0.8,  1.4,  2.40, 0.15),
 ("A383",  0.187, 1.83, 0.060, 0.24, 0.120,  0.3,  1.3,  1.95, 0.27),
 ("M0329", 0.450, 1.84, 0.070, 0.33, 0.080, -0.5,  1.0,  1.90, 0.11),
 ("M1115", 0.352, 1.69, 0.155, 0.93, 0.425, -0.5,  0.4,  2.22, 0.16),
 ("M1206", 0.440, 2.06, 0.065, 0.25, 0.100,  0.2,  1.0,  2.02, 0.14),
 ("M1931", 0.352, 1.91, 0.070, 0.24, 0.060, -0.1,  1.4,  1.92, 0.16),
 ("MS2137",0.313, 1.70, 0.105, 0.46, 0.260, -0.8,  1.1,  1.90, 0.19),
 ("R2129", 0.234, 1.75, 0.085, 0.46, 0.250, -0.9,  0.3,  1.75, 0.18),
 ("R2248", 0.348, 2.40, 0.080, 0.76, 0.235,  0.6,  1.4,  2.30, 0.23),
]
# [D14 Table 8] Chandra: vmax,err[km/s], rs,err[Mpc], r2500,err, M2500,err
# [1e14], fg2500,err, r500,err
D14C = {
 "A209":  (1743,126, 0.745,0.653, 0.470,0.014, 2.49,0.36, 0.1100,0.0050, 1.31,0.160),
 "A383":  (1184, 29, 0.220,0.017, 0.436,0.007, 1.42,0.07, 0.1070,0.0030, 0.94,0.021),
 "M0329": (1485, 80, 0.360,0.100, 0.460,0.017, 2.24,0.24, 0.1170,0.0070, 1.05,0.056),
 "M1115": (1664,106, 0.450,0.097, 0.546,0.023, 3.30,0.42, 0.1130,0.0077, 1.25,0.091),
 "M1206": (2002,148, 0.710,0.507, 0.587,0.030, 4.59,0.68, 0.1220,0.0077, 1.43,0.160),
 "M1931": (1522, 33, 0.279,0.020, 0.511,0.008, 2.74,0.12, 0.1330,0.0035, 1.11,0.023),
 "MS2137":(1312, 44, 0.164,0.016, 0.449,0.010, 1.78,0.12, 0.1205,0.0048, 0.93,0.027),
 "R2129": (1488, 70, 0.340,0.043, 0.529,0.017, 2.67,0.25, 0.1050,0.0040, 1.17,0.048),
 "R2248": (2272,125, 0.828,0.326, 0.706,0.025, 7.19,0.79, 0.1226,0.0067, 1.71,0.140),
}
# [D14 Table 9] XMM (no M0329) -- alternative gas/X-ray set
D14X = {
 "A209":  (1506, 48, 0.81,0.17, 0.460,0.010, 1.73,0.11, 0.125,0.003, 1.20,0.03),
 "A383":  (1243, 27, 0.24,0.02, 0.450,0.007, 1.61,0.07, 0.095,0.003, 0.98,0.02),
 "M1115": (1546, 51, 0.25,0.03, 0.520,0.011, 2.89,0.19, 0.120,0.005, 1.10,0.03),
 "M1206": (1974, 70, 0.64,0.15, 0.590,0.013, 4.66,0.32, 0.120,0.006, 1.40,0.10),
 "M1931": (1489, 35, 0.23,0.03, 0.502,0.007, 2.59,0.12, 0.133,0.003, 1.07,0.03),
 "MS2137":(1297, 36, 0.06,0.01, 0.401,0.007, 1.27,0.07, 0.133,0.004, 0.78,0.02),
 "R2129": (1331, 30, 0.21,0.02, 0.478,0.008, 1.97,0.09, 0.122,0.003, 1.01,0.02),
 "R2248": (2265, 54, 1.02,0.18, 0.668,0.011, 6.08,0.29, 0.133,0.004, 1.70,0.07),
}
GAS_ALPHA, GAS_ALPHA_SIG = 1.1, 0.2      # Mgas ~ r^alpha, 2500 -> 500
FSTAR, FSTAR_SIG         = 0.011, 0.0045 # M*(<r500)/M500 (Chiu+18-level)

names = [d[0] for d in B26]
zs    = np.array([d[1] for d in B26])
r200k = np.array([d[2] for d in B26]); r200k_e = np.array([d[3] for d in B26])
rsk   = np.array([d[4] for d in B26]); rsk_e   = np.array([d[5] for d in B26])
bs_lo = np.array([d[6] for d in B26]); bs_hi   = np.array([d[7] for d in B26])
r200L = np.array([d[8] for d in B26]); r200L_e = np.array([d[9] for d in B26])
N     = len(names)

bs_mid  = 0.5*(bs_lo+bs_hi); bs_sig = 0.5*(bs_hi-bs_lo)
beta_mid = 2*bs_mid/(2+bs_mid)
# per-cluster kinematic weight vs U18 prior (attenuates MI signal in Mkin)
w_kin = 1 - (r200k_e/r200L_e)**2
w_kin[names.index("M1115")] = 1.0     # M1115 fit had NO lensing prior
w_kin = np.clip(w_kin, 0.1, 1.0)

# sanity: NFW(vmax,rs) reproduces D14's own tabulated M2500 (A383)
v_,ve_,rr_,rre_,r25_,r25e_,M25_,M25e_,fg_,fge_,r5_,r5e_ = D14C["A383"]
assert abs(M_vmax(r25_, v_*KMS, rr_)/MSUN/1e14 - M25_)/M25_ < 0.05
r200_stack = (1.51e15*MSUN/((4*np.pi/3)*200*rhoc(0.315)))**(1/3)/MPC
assert abs(r200_stack - 2.13) < 0.15, f"stack r200 {r200_stack:.2f}"

print("="*78)
print("POWERED eta(beta) TEST -- nine CLASH-VLT clusters (Maraboli+26 stack lineage)")
print("="*78)
print(f"[check] stack M200c=1.51e15 => r200={r200_stack:.2f} Mpc (M26: 2.13+/-0.20) OK")
print(f"[check] NFW(vmax,rs) reproduces D14 A383 M2500 within 5% OK")
print(f"per-cluster kinematic weights w_kin (prior dilution): " +
      ", ".join(f"{n}:{w:.2f}" for n,w in zip(names,w_kin)))

# =========================================================================
# PART 1 -- MI kernel slide computed at the actual cluster accelerations
# Self-consistent constant-beta ensemble (anisotropic Jeans sigma_r(r)) in
# the M26 stack potential; per-orbit Milgrom-2022 Fourier amplitude
# A = sum_k w_k^2 |r_k| (complex two-sided; = a_circ EXACTLY on circular
# orbits) with integer-radial-period windows; time-mean and rms of |a| as
# the note's bracketing functionals.
# =========================================================================
print("\nPART 1: MI kernel slide dln(Lambda)/dbeta in the M26 stack potential")
ZSTK, M200S, CSTK = 0.315, 1.51e15*MSUN, 2.7
R200S = (M200S/((4*np.pi/3)*200*rhoc(ZSTK)))**(1/3)          # m
RS_S  = R200S/CSTK
def g_stack(r):
    return G*M200S*mu_nfw(r/RS_S)/mu_nfw(CSTK)/r**2
def phi_stack(r):
    return -G*M200S/mu_nfw(CSTK)*np.log(1+r/RS_S)/r

# anisotropic Jeans sigma_r(r) for constant beta, NFW tracers in NFW field
rgrid = np.geomspace(0.02*R200S, 8*R200S, 800)
nu_tr = 1.0/((rgrid/RS_S)*(1+rgrid/RS_S)**2)                 # NFW tracer shape
def sigr2_of(beta):
    integ = nu_tr*rgrid**(2*beta)*g_stack(rgrid)
    I = np.concatenate([np.cumsum((integ[::-1][:-1]+integ[::-1][1:])*0.5*
                        -np.diff(rgrid[::-1]))[::-1], [0.0]])
    return I/(nu_tr*rgrid**(2*beta))

def sample_r(rg, n, lo=0.1, hi=1.36):
    m = (rgrid >= lo*R200S) & (rgrid <= hi*R200S)
    w = nu_tr[m]*rgrid[m]**2
    cdf = np.cumsum(w); cdf/=cdf[-1]
    return np.interp(rg.random(n), cdf, rgrid[m])

def orbit_ensemble(beta, n_orb, seed, circular=False):
    """Constant-beta equilibrium member ensemble in the stack potential.
    Per-orbit amplitude functionals:
      A_F   = sum_k |a_k| (Hann-windowed FFT of the complex acceleration)
              -- Milgrom 2022's A = sum_k w_k^2 |r_k| rewritten in
              acceleration space (a_k = -w_k^2 r_k); normalized on the
              circular ensemble where A must equal g (framework anchor:
              circular orbit => algebraic nu exactly, Milgrom22 Eq.29);
      A_mean, A_rms of |a(t)| (the note's bracketing averages).
    Returns (A_F_raw, A_mean, A_rms, ok mask)."""
    rg = np.random.default_rng(seed)
    r0 = sample_r(rg, n_orb)
    s2 = np.interp(r0, rgrid, sigr2_of(beta))
    if circular:
        vr = np.zeros(n_orb); vt = np.sqrt(g_stack(r0)*r0)
    else:
        vr = rg.normal(0,1,n_orb)*np.sqrt(s2)
        st = np.sqrt(s2*max(1e-3, 1-beta))
        vt = np.sqrt((rg.normal(0,1,n_orb)*st)**2 + (rg.normal(0,1,n_orb)*st)**2)
    E0 = 0.5*(vr**2+vt**2) + phi_stack(r0)
    z  = (r0 + 0j)
    vz = (vr + 1j*vt)
    Tc = 2*np.pi*np.sqrt(r0/g_stack(r0))
    nst = 6000
    dt  = 5.0*Tc/nst                              # ~5 circular periods
    def accz(z):
        r = np.abs(z); r = np.clip(r, 0.005*R200S, None)
        return -g_stack(r)*z/r
    ACC = np.empty((nst, n_orb), complex); rmax = np.zeros(n_orb)
    for i in range(nst):
        k1v = accz(z);               k1x = vz
        k2v = accz(z+0.5*dt*k1x);    k2x = vz+0.5*dt*k1v
        k3v = accz(z+0.5*dt*k2x);    k3x = vz+0.5*dt*k2v
        k4v = accz(z+dt*k3x);        k4x = vz+dt*k3v
        z  = z  + dt*(k1x+2*k2x+2*k3x+k4x)/6
        vz = vz + dt*(k1v+2*k2v+2*k3v+k4v)/6
        ACC[i] = accz(z); rmax = np.maximum(rmax, np.abs(z))
    E1 = 0.5*np.abs(vz)**2 + phi_stack(np.abs(z))
    ok = (np.abs((E1-E0)/np.abs(E0)) < 0.02) & (rmax < 3.0*R200S)
    hann = 0.5*(1-np.cos(2*np.pi*np.arange(nst)/nst))
    C = np.fft.fft(ACC*hann[:,None], axis=0)/hann.sum()
    A_F = np.sum(np.abs(C), axis=0)               # l1 of acceleration spectrum
    AM  = np.abs(ACC)
    return A_F, AM.mean(0), np.sqrt((AM**2).mean(0)), ok

# circular-limit calibration -> normalization constant kappa (self-calibrated)
AFc, Amc, Arc, okc = orbit_ensemble(0.0, 80, 7, circular=True)
rg7 = np.random.default_rng(7); r0c = sample_r(rg7, 80)
kappa = np.nanmedian(AFc[okc]/g_stack(r0c[okc]))
scat  = np.nanstd(AFc[okc]/g_stack(r0c[okc])/kappa)
print(f"  circular-limit: kappa = A_F/g_circ = {kappa:.3f} (normalizing out), "
      f"scatter {scat*100:.1f}%")
assert scat < 0.2, "Fourier amplitude circular scatter"
assert abs(np.nanmedian(Amc[okc]/g_stack(r0c[okc])) - 1) < 0.05, "mean|a| circ"

BETAS = [-0.5, 0.0, 0.25, 0.5, 0.75]

def build_and_slide(lo, hi, seed0, tag):
    """Build 5 beta-ensembles with members sampled in [lo,hi]*R200 and
    return slides for Fourier/mean/rms at true a0 and deep limit."""
    global sample_r
    def sample_r_local(rg, n, lo=lo, hi=hi):
        m = (rgrid >= lo*R200S) & (rgrid <= hi*R200S)
        w = nu_tr[m]*rgrid[m]**2
        cdf = np.cumsum(w); cdf/=cdf[-1]
        return np.interp(rg.random(n), cdf, rgrid[m])
    old = sample_r; sample_r = sample_r_local
    ENS = {b: orbit_ensemble(b, 500, seed0+k) for k,b in enumerate(BETAS)}
    sample_r = old
    nok = {b: int(ENS[b][3].sum()) for b in BETAS}
    def slide_from(est, a0):
        lnL = {}
        for b in BETAS:
            A_F, A_m, A_r, ok = ENS[b]
            A = [A_F/kappa, A_m, A_r][est][ok]
            A = A[np.isfinite(A) & (A > 0)]
            lnL[b] = np.mean(np.log(np.sqrt(1 + a0/A)))
        return (lnL[0.5]-lnL[0.0])/0.5
    DEEP = A0_CAN*3e3
    res = dict(F=slide_from(0,A0_CAN), mn=slide_from(1,A0_CAN),
               rm=slide_from(2,A0_CAN),
               FD=slide_from(0,DEEP), mnD=slide_from(1,DEEP),
               rmD=slide_from(2,DEEP))
    ymed = np.nanmedian(ENS[0.0][0][ENS[0.0][3]]/kappa)/A0_CAN
    print(f"  [{tag}] valid/beta: {min(nok.values())}-{max(nok.values())};"
          f" median y=A_F/a0 (iso): {ymed:.2f}")
    print(f"    dlnLambda/dbeta (0->0.5) true a0: Fourier {res['F']:+.3f} |"
          f" mean {res['mn']:+.3f} | rms {res['rm']:+.3f}")
    print(f"    deep limit:                       Fourier {res['FD']:+.3f} |"
          f" mean {res['mnD']:+.3f} | rms {res['rmD']:+.3f}")
    return res

resA = build_and_slide(0.10, 1.36, 100, "all-tracer weighting r/R200 in [0.10,1.36]")
resB = build_and_slide(0.50, 1.36, 300, "outer-shell weighting r/R200 in [0.50,1.36]")
# PRIMARY kernel = Milgrom-2022 Fourier amplitude; weighting band A..B
sF    = 0.5*(resA['F']+resB['F']);  sF_lo, sF_hi = resA['F'], resB['F']
sDeep = 0.5*(resA['FD']+resB['FD'])
d_eta_deep = -2*sDeep*0.4
lo_note, hi_note = np.log(2.8/2.15), np.log(3.0/2.15)
tag = ('CONSISTENT' if 0.5*lo_note < d_eta_deep < 2.0*hi_note
       else 'SMALLER than the note -- BOTH kernels carried forward')
print(f"  deep-limit kernel-eta rise (beta 0->0.4): {d_eta_deep:.3f} vs the"
      f" note's [{lo_note:.3f},{hi_note:.3f}]  => {tag}")
D_dil = sF/sDeep if sDeep else np.nan
print(f"  DILUTION at true accelerations: D = {D_dil:.2f}")
P_M_mid  = 1.25*sF                          # computed-kernel MI mass-space pred
P_M_note = -0.56*D_dil                      # banked-note deep -0.56 x same D
P_A_mid  = -(4/3)*P_M_mid
print(f"  MI predicted mass-space slopes dln(Mkin/Mref)/dbeta (pre-w_kin,")
print(f"  per unit PHYSICAL beta):")
print(f"    computed kernel: {P_M_mid:+.3f}   (weighting band "
      f"[{1.25*min(sF_lo,sF_hi):+.3f},{1.25*max(sF_lo,sF_hi):+.3f}])")
print(f"    banked-note kernel x same dilution: {P_M_note:+.3f}")
print(f"    kernel-space counterparts: {P_A_mid:+.3f} / {-(4/3)*P_M_note:+.3f}"
      f" (note deep +0.75)")
print(f"    MG (Milgrom 2014 virial thm) and LCDM: 0 exactly")

# =========================================================================
# PART 2 -- per-cluster eta(R500) on the framework's own nu + a0
# =========================================================================
print("\nPART 2: per-cluster eta(R500) = M500_kin/M_pred(R500), framework nu")
def cluster_quantities(r2k, rsk_, z, name, alpha, fstar, a0, gasset=D14C):
    R500 = r500_of(r2k, rsk_, z)
    M500k = M_nfw(R500, r2k, rsk_, z)
    v,ve,rr,rre,r25,r25e,M25,M25e,fg,fge,r5,r5e = gasset[name]
    Mgas = fg*M25*1e14*MSUN*(R500/r25)**alpha
    Mbar = Mgas + fstar*M500k
    gbar = G*Mbar/(R500*MPC)**2
    Mpred= Mbar*np.sqrt(1+a0/gbar)
    MX   = M_vmax(r5, v*KMS, rr)
    return R500, M500k, Mbar, Mpred, MX, gbar/a0

print(f"{'cluster':8s}{'z':>6s}{'beta200':>8s}{'w_kin':>6s}{'R500k':>7s}{'M500k':>7s}"
      f"{'Mbar':>6s}{'y_bar':>6s}{'eta':>6s}{'Mk/ML':>6s}{'Mk/MX':>6s}")
eta0=np.zeros(N); lnMkL0=np.zeros(N); lnMkX0=np.zeros(N); fbar=np.zeros(N)
for i,nm in enumerate(names):
    R500,M500k,Mbar,Mpred,MX,yb = cluster_quantities(
        r200k[i], rsk[i], zs[i], nm, GAS_ALPHA, FSTAR, A0_CAN)
    eta0[i]=M500k/Mpred; lnMkL0[i]=3*np.log(r200k[i]/r200L[i])
    lnMkX0[i]=np.log(M500k/MX); fbar[i]=Mbar/M500k
    print(f"{nm:8s}{zs[i]:6.3f}{beta_mid[i]:8.2f}{w_kin[i]:6.2f}{R500:7.2f}"
          f"{M500k/MSUN/1e14:7.1f}{Mbar/MSUN/1e14:6.2f}{yb:6.2f}"
          f"{eta0[i]:6.2f}{np.exp(lnMkL0[i]):6.2f}{np.exp(lnMkX0[i]):6.2f}")
assert 0.08 < np.median(fbar) < 0.20, "baryon fraction sanity"
print(f"  median f_bar(R500) = {np.median(fbar):.3f} (sane 0.10-0.16)")
for a0v, tag in [(A0_CAN,"canonical 9.36e-11"), (A0_FORK,"fork 1.13e-10  ")]:
    et = np.array([cluster_quantities(r200k[i],rsk[i],zs[i],names[i],
                   GAS_ALPHA,FSTAR,a0v)[1] /
                   cluster_quantities(r200k[i],rsk[i],zs[i],names[i],
                   GAS_ALPHA,FSTAR,a0v)[3] for i in range(N)])
    print(f"  mean kinematic eta(R500) [{tag}]: {et.mean():.2f} "
          f"(median {np.median(et):.2f})   [banked X-ray eRASS1 ref ~2.33]")
# XMM gas cross-check (8 clusters)
etX=[]
for i,nm in enumerate(names):
    if nm in D14X:
        _,Mk,_,Mp,_,_ = cluster_quantities(r200k[i],rsk[i],zs[i],nm,
                                           GAS_ALPHA,FSTAR,A0_CAN,D14X)
        etX.append(Mk/Mp)
print(f"  XMM-gas cross-check mean eta (8 cl): {np.mean(etX):.2f}")

# =========================================================================
# PART 3 -- regressions with full MC + injection calibration
# =========================================================================
print("\nPART 3: slopes vs beta_sym(r200)  [MI mass-space < 0; MG/LCDM = 0]")
print("  (regression in beta_sym space -- the tabulated, bounded variable;")
print("   the beta_sym->beta map is singular at -2, so beta-space draws are")
print("   ill-conditioned. Injections keyed to PHYSICAL beta; confrontation")
print("   is shift-vs-shift in the same space. <dbeta/dbeta_sym> at mids =")
dbdbs = 4/(2+bs_mid)**2
print(f"   {dbdbs.mean():.2f} for unit conversion of slopes.)")
def draw_and_fit(rg, inject=0.0):
    """inject = TRUE mass-space MI slope per unit PHYSICAL beta; observed
    Mkin biased by exp(inject * w_kin * beta_true) (U18 priors attenuate)."""
    bs  = rg.normal(bs_mid, bs_sig)
    r2k = rg.normal(r200k, r200k_e)
    rs_ = np.clip(rg.normal(rsk, rsk_e), 0.05, None)
    r2L = rg.normal(r200L, r200L_e)
    al  = rg.normal(GAS_ALPHA, GAS_ALPHA_SIG)
    fs  = max(rg.normal(FSTAR, FSTAR_SIG), 0.002)
    y1=np.zeros(N); y2=np.zeros(N); y3=np.zeros(N)
    for i,nm in enumerate(names):
        v,ve,rr,rre,r25,r25e,M25,M25e,fg,fge,r5,r5e = D14C[nm]
        vv  = rg.normal(v,ve)*KMS; rrx = max(rg.normal(rr,rre), 0.03)
        M25x= rg.normal(M25,M25e)*1e14*MSUN
        fgx = max(rg.normal(fg,fge), 0.02); r5x = max(rg.normal(r5,r5e), 0.4)
        try: R500 = r500_of(r2k[i], rs_[i], zs[i])
        except ValueError: R500 = 0.65*r2k[i]
        bias = np.exp(inject*w_kin[i]*beta_mid[i])
        M500k = M_nfw(R500, r2k[i], rs_[i], zs[i])*bias
        Mgas = fgx*M25x*(R500/r25)**al
        Mbar = Mgas + fs*M500k
        gbar = G*Mbar/(R500*MPC)**2
        y1[i] = np.log(M500k/(Mbar*np.sqrt(1+A0_CAN/gbar)))
        y2[i] = 3*np.log(r2k[i]/r2L[i]) + np.log(bias)
        y3[i] = np.log(M500k/M_vmax(r5x, vv, rrx))
    A = np.vstack([bs, np.ones(N)]).T          # beta_sym regressor
    s1 = np.linalg.lstsq(A, y1, rcond=None)[0][0]
    s2 = np.linalg.lstsq(A, y2, rcond=None)[0][0]
    s3 = np.linalg.lstsq(A, y3, rcond=None)[0][0]
    return s1, s2, s3, stats.spearmanr(bs, y1).statistic

NMC = 4000
S     = np.array([draw_and_fit(rng)           for _ in range(NMC)])
S_mi  = np.array([draw_and_fit(rng, P_M_mid)  for _ in range(NMC//2)])
S_nt  = np.array([draw_and_fit(rng, P_M_note) for _ in range(NMC//2)])
q = lambda a: (np.percentile(a,50), 0.5*(np.percentile(a,84)-np.percentile(a,16)))
s1,e1 = q(S[:,0]); s2,e2 = q(S[:,1]); s3,e3 = q(S[:,2])
m1mi,_ = q(S_mi[:,0]); m2mi,_ = q(S_mi[:,1]); m3mi,_ = q(S_mi[:,2])
m1nt,_ = q(S_nt[:,0]); m2nt,_ = q(S_nt[:,1]); m3nt,_ = q(S_nt[:,2])
# attenuated EXPECTED SHIFT under MI-truth = (injected median) - (no-injection median)
D1mi, D2mi, D3mi = m1mi-s1, m2mi-s2, m3mi-s3
D1nt, D2nt, D3nt = m1nt-s1, m2nt-s2, m3nt-s3
att = D1mi/(P_M_mid*dbdbs.mean()) if P_M_mid else np.nan
print(f"  R1 dln[M500kin/Mpred]/dbeta_sym    = {s1:+.3f} +/- {e1:.3f}  (task's eta)")
print(f"  R2 dln[M200kin/M200lens]/dbeta_sym = {s2:+.3f} +/- {e2:.3f}")
print(f"  R3 dln[M500kin/M500X]/dbeta_sym    = {s3:+.3f} +/- {e3:.3f}")
print(f"  (approx per-unit-beta: x{1/dbdbs.mean():.2f} => R1 ~ {s1/dbdbs.mean():+.3f})")
print(f"  Spearman(beta_sym, ln eta) median  = {np.median(S[:,3]):+.2f}; "
      f"P(R1<0) = {np.mean(S[:,0]<0):.3f}")
print(f"  kernel-space (A): dln(etahat)/dbeta_sym = {-(4/3)*s1:+.3f} +/- "
      f"{(4/3)*e1:.3f}   [MG/LCDM 0; MI positive]")
print(f"\n  INJECTION CALIBRATION (attenuated expected SHIFT under MI-truth,")
print(f"  = injected-pipeline median minus no-injection median; includes beta")
print(f"  x-error attenuation x{att:.2f} and w_kin prior dilution):")
print(f"    computed kernel  ({P_M_mid:+.3f} true): R1 {D1mi:+.3f}; "
      f"R2 {D2mi:+.3f}; R3 {D3mi:+.3f}")
print(f"    note kernel      ({P_M_note:+.3f} true): R1 {D1nt:+.3f}; "
      f"R2 {D2nt:+.3f}; R3 {D3nt:+.3f}")
z1n = s1/e1
z1mi, z1nt = (s1-D1mi)/e1, (s1-D1nt)/e1
z2n, z2mi, z2nt = s2/e2, (s2-D2mi)/e2, (s2-D2nt)/e2
z3n, z3mi, z3nt = s3/e3, (s3-D3mi)/e3, (s3-D3nt)/e3
print(f"  significance:  R1: vs null {z1n:+.2f}s | vs MI(computed) {z1mi:+.2f}s"
      f" | vs MI(note) {z1nt:+.2f}s")
print(f"                 R2: vs null {z2n:+.2f}s | vs MI(computed) {z2mi:+.2f}s"
      f" | vs MI(note) {z2nt:+.2f}s")
print(f"                 R3: vs null {z3n:+.2f}s | vs MI(computed) {z3mi:+.2f}s"
      f" | vs MI(note) {z3nt:+.2f}s")

# confound + robustness (central values, beta_sym space)
pc = lambda x,y,c: ((stats.pearsonr(x,y)[0]-stats.pearsonr(x,c)[0]*stats.pearsonr(y,c)[0])
                    /np.sqrt((1-stats.pearsonr(x,c)[0]**2)*(1-stats.pearsonr(y,c)[0]**2)))
lnM = np.log(r200k**3)
print(f"  confound: Spearman(beta_sym, lnMkin) = "
      f"{stats.spearmanr(bs_mid, lnM).statistic:+.2f} (massive=more radial, physical);"
      f" partial corr(ln eta, beta_sym | lnM) = {pc(np.log(eta0), bs_mid, lnM):+.2f}")
A_ = np.vstack([bs_mid, np.ones(N)]).T
s_full = np.linalg.lstsq(A_, np.log(eta0), rcond=None)[0][0]
jk = []
for i in range(N):
    m = np.ones(N, bool); m[i]=False
    jk.append(np.linalg.lstsq(A_[m], np.log(eta0)[m], rcond=None)[0][0])
imax = int(np.argmax(np.abs(np.array(jk)-s_full)))
print(f"  jackknife (central values): full {s_full:+.3f}; "
      f"max shift dropping {names[imax]}: {jk[imax]:+.3f}")
hi = beta_mid > 0.45
dln = np.log(eta0[hi]).mean()-np.log(eta0[~hi]).mean()
dbe = beta_mid[hi].mean()-beta_mid[~hi].mean()
print(f"  2-bin split ({hi.sum()} radial vs {(~hi).sum()} iso/tang): "
      f"Dln(eta)={dln:+.3f} over Dbeta={dbe:.2f} => per-unit-beta slope "
      f"{dln/dbe:+.3f} [MI: computed {P_M_mid:+.3f} / note {P_M_note:+.3f}"
      f" (pre-attenuation); MG/LCDM 0]")

# =========================================================================
# PART 4 -- stack-level anchors (M26) + the 250-kpc beta-drop
# =========================================================================
print("\nPART 4: stack-level anchors (Maraboli+26)")
r_2 = 2.13/2.7
R500S_mpc = r500_of(2.13, r_2, 0.315)
combos = [("gT",0.49,0.82),("gT",0.34,0.98),("gT",0.49,0.88),("gT",0.43,0.98),
          ("gOM",0.57,0.75)]
bR500 = [b0+(bi-b0)*(R500S_mpc/(R500S_mpc+r_2)) if m=="gT"
         else b0+(bi-b0)*(R500S_mpc**2/(R500S_mpc**2+r_2**2)) for m,b0,bi in combos]
bR200 = [b0+(bi-b0)*(2.13/(2.13+r_2)) if m=="gT"
         else b0+(bi-b0)*(2.13**2/(2.13**2+r_2**2)) for m,b0,bi in combos]
print(f"  stack beta(R500) = {np.mean(bR500):.2f} [{min(bR500):.2f},{max(bR500):.2f}];"
      f" beta(r200) = {np.mean(bR200):.2f} [{min(bR200):.2f},{max(bR200):.2f}]"
      f" (M26 abstract: >~0.8 at r200)")
print(f"  per-cluster mean beta(r200) = {beta_mid.mean():.2f}: the stack is member-"
      f"weighted (A209+AS1063 = 40% of 5348 members, both radial) => radial end.")
bst = np.mean(bR500)
eta_mi_c = 2.15*np.exp(-2*sF*bst)                 # computed kernel
eta_mi_n = 2.15*np.exp(-2*(P_M_note/1.25)*bst)    # note kernel, same D
print(f"  MI ensemble expectation at stack beta(R500)={bst:.2f}: kernel-eta = "
      f"2.15 -> {eta_mi_c:.2f} (computed kernel) / {eta_mi_n:.2f} (note kernel); "
      f"kinematic-mass counterpart: Mkin {100*(1-np.exp(P_M_mid*bst)):.0f}% / "
      f"{100*(1-np.exp(P_M_note*bst)):.0f}% below the MG value at the same baryons.")
print("  250-kpc beta-drop (M26 JI): beta dips toward isotropy at ~250 kpc =>")
print("  the MI slide RELAXES TOWARD THE 2.15 FLOOR there -- it neither absorbs")
print("  nor aggravates the central deficit (floor theorem: no orbit population")
print("  beats circular). Radius-resolved eta(r)-vs-beta(r) would need radius-")
print("  resolved kinematic masses (not published) -- flagged, not run.")

# =========================================================================
# PART 5 -- verdict + power
# =========================================================================
print("\nPART 5: VERDICT (both-ways, injection-calibrated)")
sep_c = abs(D1mi)/e1; sep_n = abs(D1nt)/e1
print(f"  achievable MI-vs-null separation at N=9 (R1): computed kernel "
      f"{sep_c:.2f} sigma | note kernel {sep_n:.2f} sigma")
print(f"  => {'POWERED' if max(sep_c,sep_n)>=3 else 'NOT a powered test at N=9 with published per-cluster beta errors'}")
for lbl, sep in [("computed", sep_c), ("note", sep_n)]:
    nreq = 9*(3/sep)**2 if sep>0 else np.inf
    print(f"  N(clusters) at this quality for 3 sigma [{lbl} kernel]: ~{nreq:.0f}")
print(f"  measured R1 = {s1:+.3f} +/- {e1:.3f}:")
print(f"    vs NULL (MG/LCDM flat): {z1n:+.2f} sigma"
      f"  -- sign is {'ANTI-MI (positive)' if s1>0 else 'MI-side (negative)'}")
print(f"    vs MI (computed kernel): {z1mi:+.2f} sigma")
print(f"    vs MI (note kernel):     {z1nt:+.2f} sigma")
kill = max(z1mi, z1nt) > 2 and s1 > 0
print(f"  LEDGER KILL CHECK (calibrated anti-MI >2 sigma): "
      f"{'MET -- strike against the MI realization' if kill else 'NOT met'}")
print(f"  cross-checks vs MI(note): R2 {z2nt:+.2f}s; R3 {z3nt:+.2f}s")
print("\nDONE (exit 0). Inputs verified against arXiv/ar5iv HTML today:")
print("  B26 arXiv:2508.05195 Tab.1-2; M26 arXiv:2602.15934 Tab.1+stack grids;")
print("  D14 arXiv:1405.7876 Tab.8-9 (M2500 reproduction check passed).")
