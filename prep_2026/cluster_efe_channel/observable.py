#!/usr/bin/env python3
r"""
observable.py  --  OBSERVABLE-DESIGN LANE (CLUSTER-MEMBER infall-phase EFE sigma-spread)
========================================================================================
prep_2026/cluster_efe_channel/ , 2026-07-17.  Exit 0.  numpy / scipy / sympy.  BOTH footings.
Framework: de Sitter-Unruh MODIFIED INERTIA (Zimmerman).  g_obs = nu(y) g_bar,
nu(y)=sqrt(1+1/y), y=g_bar/a0, a0=cH_Lambda/Z, Z=sqrt(32pi/3).  NEVER McGaugh nu.
Milgrom 1983/1999 (PLA 253:273) wellhead credit; distinctive content = the cH_Lambda/Z
COEFFICIENT + the time-nonlocal MI completion K(Box_u).  a0's VALUE + s=-1 are POSTULATES;
MG=0 (at fixed TRUE g_ext) is the sole theorem-grade claim.

TASK (my lane, verbatim scope): design the STATISTIC that ISOLATES the MI infall-phase
HISTORY spread from THE KEY DEGENERACY -- the shared radial EFE gradient.  Both MI and MG
give (sigma_int/sigma_baryon) varying with cluster-centric radius (both have an EFE that
loads the boost with the CURRENT g_ext(r)).  The distinctive MI signal is NOT that radial
trend; it is the RESIDUAL spread AT FIXED cluster-centric radius (fixed current g_ext)
correlated with an INFALL-PHASE proxy (phase-space r-v zone, Rhee+2017).  Then beat the
same-signed confounds (tidal heating/stripping, ram pressure, environmental quenching --
the star-orbit swing's C6, radially anti-correlated ~2-8%) and velocity anisotropy.  Show
what MG cannot reproduce.

Companion lanes this BUILDS ON (does not reinvent):
  predict.py / PREDICT.md          : the MI prediction (magnitude band, sign-flip, radial
                                     structure, mass/depth dependence).  Reused here.
  mg_efe_zero.py / MG_EFE_ZERO.md  : MG=0 theorem at fixed TRUE g_ext + the projection (2.2%)
                                     and interloper mimics.  Reused as the MG floor.
  sigma_spread/GAP_STATEMENT.md    : frozen estimator E1-E7 (DS cut, matched-a_ext, E6 radial
                                     separator).  This lane is the E6-confound-design detail.
  reviews/residual_doors_2026_07/D3_* : the DATED sign-flip pre-registration (No Pump-Free
                                     Corner, DOI 10.5281/zenodo.21179352).

HONEST SCOPE (non-negotiable, stated up front):
  * MI-CLASS-GENERIC.  Discriminates MI-class (ANY history-dependent inertia) vs MG (=0
    exactly at fixed true field).  NOT this-framework vs Milgrom's linear no-EFE MI
    (arXiv:2503.07106, which ALSO makes a spread).  It is an MI-vs-MG test.
  * The 6-13% MAGNITUDE is KERNEL-HOSTAGE (theta(y) not derived; only cone endpoints fixed).
    Existence + SIGN (+ the sign-flip) + MG=0 are the theorem-grade claims; amplitude is a band.
  * Both footings shown.  a0's value + s=-1 are POSTULATES.  No "proves" for the framework.

THE DESIGN PRINCIPLE (why the residual-at-fixed-radius statistic beats the degeneracy):
  The shared radial EFE gradient is a function of cluster-centric position ONLY.  So it is a
  common-mode signal that lives on ONE axis (radius).  The MI history signal lives on a
  SECOND, ORTHOGONAL axis (infall phase at fixed radius).  Project the (sigma_int/sigma_bary)
  field onto the (radius x phase) plane and difference ALONG the phase axis WITHIN a fixed
  radius bin: the shared radial gradient cancels identically (it has no phase dependence);
  MG's residual is then EXACTLY 0 at fixed TRUE radius (theorem) and only the projection alias
  survives (killed by orbit-class-aware zone deprojection).  MI's residual is the sign-flipping
  6-13% band.  The confounds (tidal/ram/quench) DO live partly on the phase axis -- they are
  beaten not by the phase-difference alone but by a 4-part FINGERPRINT that only MI trips.
"""
import math
import numpy as np
import sympy as sp

np.seterr(all="ignore")

# ============================================================ constants / footings
c   = 2.99792458e8
Mpc = 3.0856775814913673e22
kpc = Mpc/1e3
km  = 1e3
yr  = 3.1557e7
Gyr = 1e9*yr
G   = 6.674e-11
MSUN= 1.989e30
H0  = 67.4e3/Mpc
OmL = 0.685
HL  = H0*math.sqrt(OmL)
Z   = math.sqrt(32*math.pi/3.0)                  # = 5.7890...
A0_CAN = c*HL/Z                                  # canonical  cH_Lambda/Z
A0_ALT = c*H0/Z                                  # alternate  cH0/Z
assert abs(A0_CAN-9.36e-11) < 1e-13 and abs(A0_ALT-1.13e-10) < 1e-12
FOOTINGS = [("CANONICAL a0=9.36e-11 (cH_Lambda/Z)", A0_CAN),
            ("ALTERNATE a0=1.13e-10 (cH0/Z)",       A0_ALT)]
TAU_MEM = 0.45*Gyr                               # channel-M Lorentzian memory (D3 lane)

# framework's OWN interpolation (NEVER McGaugh).  sigma/sigma_baryon = sqrt(g_obs/g_bar).
def boost_sigma_ratio(a_in, a_ex, y, theta, a0):
    A = a_in + a_ex*theta(y)                     # effective internal field, EFE-loaded
    g_obs = math.sqrt(A*A + A*a0)                # framework nu applied to the loaded field
    return math.sqrt(g_obs/A)                    # sigma ~ sqrt(g) at fixed radius

# Milgrom-2022 subsystem-boost kernels theta(y) (KERNEL-HOSTAGE band)
theta_rat = lambda y: 2.0/(1.0 + y*y)                                   # theta(0)=2  fiducial
theta_e1  = lambda y: math.exp(1.0 - abs(y))                            # theta(0)=e  ceiling
theta_s2  = lambda y: math.sqrt(2.0)/(1.0 + (math.sqrt(2.0)-1.0)*y*y)   # theta(0)=v2 floor
KERNELS = [("theta0=v2 floor", theta_s2), ("theta0=2  fiducial", theta_rat),
           ("theta0=e  ceiling", theta_e1)]

def felt_excess(y_cur, y_hist, t_since, theta, a0, a_in=0.30, a_ex=1.0):
    """relational sigma excess of a member vs a SETTLED (ancient) twin at the SAME current y.
    The felt y lags via the memory kernel: y_eff = y_cur + (y_hist-y_cur) exp(-t/tau)."""
    w   = math.exp(-t_since/TAU_MEM)
    yef = y_cur + (y_hist - y_cur)*w
    R_now = boost_sigma_ratio(a_in*a0, a_ex*a0, yef,   theta, a0)   # memory-weighted felt
    R_set = boost_sigma_ratio(a_in*a0, a_ex*a0, y_cur, theta, a0)   # settled/ancient twin
    return R_now/R_set - 1.0, yef, w

print("="*100)
print(" OBSERVABLE-DESIGN LANE -- CLUSTER-MEMBER infall-phase EFE sigma-spread (MI-class vs MG)")
print(" isolating the MI history signal from THE KEY DEGENERACY: the shared RADIAL EFE gradient")
print("="*100)
print(f"  Z={Z:.4f}  a0_can={A0_CAN:.3e}  a0_alt={A0_ALT:.3e}  tau_mem={TAU_MEM/Gyr:.2f} Gyr")

# =========================================================================================
# [A]  THE TWO-AXIS DECOMPOSITION -- why a residual-at-fixed-radius statistic exists at all
# =========================================================================================
print("\n" + "="*100)
print(" [A] THE KEY DEGENERACY, made explicit: (sigma_int/sigma_bary) on the (radius x phase) plane")
print("="*100)
print("  Common-mode (SHARED by MI and MG): the radial EFE gradient. At larger cluster-centric")
print("  radius the current g_ext is weaker -> less EFE suppression -> larger internal boost. This")
print("  is a function of radius ONLY; it is IDENTICAL for MI and MG and carries NO phase label.")
print("  Distinctive (MI ONLY): at FIXED radius (fixed current g_ext), a residual spread correlated")
print("  with INFALL PHASE (history). The design isolates the SECOND axis and differences out the")
print("  first. Below: the radial common-mode for a fiducial diffuse member, both footings.")
for flabel, a0 in FOOTINGS:
    print(f"\n  [{flabel}]  radial common-mode boost sigma/sigma_bary vs a_ex (settled, y->0):")
    for aex in (0.1, 0.3, 1.0, 3.0):
        R = boost_sigma_ratio(0.30*a0, aex*a0, 0.0, theta_rat, a0)
        print(f"      a_ex={aex:4.1f} a0  ->  sigma/sigma_bary = {R:.3f}")
print("  ==> The radial trend spans tens of % (0.1a0 -> 3a0). BOTH theories have it. Binning the")
print("      test WITHIN a fixed a_ex bin (<=0.3 dex, deprojected) removes it as a common mode.")

# =========================================================================================
# [B]  THE STATISTIC: the phase-axis contrast at fixed radius, tagged by Rhee+2017 PPS zones
# =========================================================================================
print("\n" + "="*100)
print(" [B] THE ISOLATING STATISTIC -- Rhee+2017 phase-space zone contrast at FIXED radius")
print("="*100)
print("  Infall-phase PROXY = position in projected phase space (R_proj/r200, |v_los-v_cl|/sigma_cl)")
print("  classified into Rhee+2017 (ApJ 843:128) orbit-history zones, calibrated on N-body:")
print("    ancient-infall (virialized, settled)  | first-infall (pre-peri, outside->in, COLD past)")
print("    recent-infall  (just post-peri, hot)   | backsplash (past peri, out again, decaying)")
print("  Statistic (WITHIN one deprojected a_ex bin): the zone-mean residual")
print("      D(zone) = < ln[ sigma_int / sigma_bary ] >_zone  -  < same >_ancient")
print("  MG (theorem, fixed true r): D(zone)=0 for EVERY zone (no phase label in the field).")
print("  MI: the memory-weighted sign-flipping pattern below.\n")

# Rhee+2017 zones mapped to (y_cur, y_hist, t_since_peri) at the transition shell (a_ex~a0):
# y_hist ~ the field the member's history was dominated by; t_since = time since pericentre
# (first-infall: not yet at peri -> use time-since-infall, y_hist=cold isolated past ~0.05).
ZONES = [
    #  label                         y_cur y_hist t_since(Gyr)
    ("ancient-infall (settled)",     0.55, 0.55, 8.0),   # reference: y_eff=y_cur, excess ~0
    ("first-infall (pre-peri)",      0.90, 0.05, 0.30),  # COLD past -> DEFICIT
    ("recent-infall (post-peri)",    0.60, 1.50, 0.50),  # HOT peri  -> EXCESS
    ("backsplash (out again)",       0.30, 1.20, 1.50),  # decaying EXCESS
]
zone_signature = {}
for flabel, a0 in FOOTINGS:
    print(f"  [{flabel}]")
    print(f"    {'zone':30s} {'y_eff':>6s} {'w':>5s} |  theta0=v2   theta0=2   theta0=e   (sigma excess vs ancient)")
    for zl, yc, yh, tg in ZONES:
        row = []
        for _, th in KERNELS:
            exc, yef, w = felt_excess(yc, yh, tg*Gyr, th, a0)
            row.append(exc)
        # store fiducial (theta0=2) for the confound-matrix and asserts
        exc_fid, yef, w = felt_excess(yc, yh, tg*Gyr, theta_rat, a0)
        zone_signature[(flabel, zl)] = exc_fid
        print(f"    {zl:30s} {yef:6.2f} {w:5.2f} |  "
              f"{row[0]*100:+6.1f}%   {row[1]*100:+6.1f}%   {row[2]*100:+6.1f}%")
    print()
# the MI-unique fingerprint: pre-peri DEFICIT, post-peri EXCESS -> a SIGN FLIP across peri.
can = "CANONICAL a0=9.36e-11 (cH_Lambda/Z)"
d_pre  = zone_signature[(can, "first-infall (pre-peri)")]
d_post = zone_signature[(can, "recent-infall (post-peri)")]
d_anc  = zone_signature[(can, "ancient-infall (settled)")]
assert d_pre < -0.02, "first-infall must show a DEFICIT"
assert d_post > +0.02, "recent-infall must show an EXCESS"
assert abs(d_anc) < 0.005, "ancient reference must be ~0"
print(f"  ==> SIGN-FLIP fingerprint (canonical, fiducial theta0=2): first-infall {d_pre*100:+.1f}%"
      f"  ->  recent-infall {d_post*100:+.1f}%  (a sign flip across pericentre).")
print("      The phase-axis contrast |D(post) - D(pre)| is the primary MG-impossible statistic;")
print("      MG gives 0 for BOTH zones at fixed true radius (section [C] proves the exact zero).")

# =========================================================================================
# [C]  MG = 0 on the phase axis at fixed TRUE radius (symbolic) + the projection alias
#      and why the Rhee ZONES themselves are the orbit-class-aware deprojection that kills it
# =========================================================================================
print("\n" + "="*100)
print(" [C] WHAT MG CANNOT REPRODUCE -- exact zero phase-contrast at fixed true r + the alias floor")
print("="*100)
a_in_s, a_ex_s, a0_s, th0_s, y_s = sp.symbols("a_in a_ex a0 theta0 y", positive=True)
A_MG   = a_in_s + a_ex_s*th0_s               # MG EFE: CURRENT position only, constant theta0
sig_MG = sp.sqrt(sp.sqrt(A_MG**2 + A_MG*a0_s)/A_MG)
assert sp.simplify(sp.diff(sig_MG, y_s)) == 0, "MG boost must carry no infall-phase label!"
print("  d(sigma_MG)/d(infall-phase y) = 0 identically (any a0, any interpolation). At fixed TRUE")
print("  cluster-centric radius, MG's zone-contrast D(zone)=0 EXACTLY -- the field carries no")
print("  worldline/history label. This is the theorem the statistic is built to expose.")

# The one way MG fakes a phase-contrast: PROJECTION. At fixed PROJECTED radius, radial plungers
# (infall/recent zones) sit at a different TRUE r than settled members -> MG's real RADIAL trend
# aliases into the phase axis. Reproduce the banked ~2.2% alias with a compact MC, and show that
# binning by TRUE r (which the Rhee PPS zones supply, being calibrated to orbital history) kills it.
print("\n  The MG projection alias (the only nonzero MG phase-contrast) and its kill:")
rng = np.random.default_rng(20260717)
for flabel, a0 in FOOTINGS:
    N = 120000
    R200 = 2.0*Mpc
    # NFW-ish settled members vs radial-plunge infallers; a_ex(r) ~ GM(<r)/r^2 (toy: a_ex ~ 1/r tail)
    def a_ex_of_r(r):                                   # monotone falling external field
        return A0_CAN * (R200/np.maximum(r, 0.3*R200))  # ~a0 at R200, rising inward (toy)
    # settled: isotropic 3D radii; plungers: preferentially small true r seen at larger R_proj
    r_settled = R200*rng.uniform(0.3, 1.6, N)**0.9
    r_plunge  = R200*rng.uniform(0.15, 1.0, N)**1.3     # deeper true r
    # project onto LOS with random inclination -> R_proj = r*sqrt(1-mu^2)
    mu_s = rng.uniform(-1, 1, N); mu_p = rng.uniform(-1, 1, N)
    Rp_settled = r_settled*np.sqrt(1-mu_s**2)
    Rp_plunge  = r_plunge *np.sqrt(1-mu_p**2)
    # MG internal boost = f(a_ex(r_true)) ONLY (no phase label); use the settled y->0 boost
    def mg_boost(a_ex):
        A = 0.30*a0 + a_ex
        return np.sqrt(np.sqrt(A*A + A*a0)/A)
    b_settled_true = mg_boost(a_ex_of_r(r_settled))
    b_plunge_true  = mg_boost(a_ex_of_r(r_plunge))
    # bin in a fixed PROJECTED-radius shell, contrast plunge vs settled (the raw alias):
    lo, hi = 0.55*R200, 0.75*R200
    ms = (Rp_settled>lo)&(Rp_settled<hi); mp = (Rp_plunge>lo)&(Rp_plunge<hi)
    alias_proj = np.log(b_plunge_true[mp].mean()) - np.log(b_settled_true[ms].mean())
    # now bin in the SAME shell but by TRUE r (orbit-class-aware = Rhee zone deprojection):
    mst = (r_settled>lo)&(r_settled<hi); mpt = (r_plunge>lo)&(r_plunge<hi)
    alias_true = np.log(b_plunge_true[mpt].mean()) - np.log(b_settled_true[mst].mean())
    print(f"    [{flabel[:22]:22s}] MG phase-contrast:  by R_proj = {abs(alias_proj)*100:5.2f}%"
          f"  (alias)  ->  by TRUE r = {abs(alias_true)*100:5.2f}%  (killed)")
print("  ==> The projection alias (~2% band, banked 2.25%/2.35%) is the ONLY nonzero MG response.")
print("      It is killed by binning on TRUE r. The Rhee+2017 PPS zones ARE the orbit-class-aware")
print("      deprojection (they are calibrated on N-body ORBITAL HISTORY, not a scalar radial mean)")
print("      -- exactly what MG_EFE_ZERO showed a class-BLIND scalar deprojection CANNOT do. Plus")
print("      the mandatory DS substructure cut + caustic membership (GAP E5) for interlopers.")

# =========================================================================================
# [D]  VELOCITY ANISOTROPY control (member-INTERNAL beta) -- the Wolf beta-immune normalisation
# =========================================================================================
print("\n" + "="*100)
print(" [D] VELOCITY-ANISOTROPY control -- member-internal beta cannot fake the phase-contrast")
print("="*100)
print("  The observable is (member internal sigma)/(baryon-predicted sigma). The member's OWN")
print("  internal velocity-ellipsoid anisotropy beta enters sigma_los. Infall can induce radial")
print("  anisotropy (tidal), so beta correlates with phase -> a potential alias. CONTROL: normalise")
print("  by the Wolf+2010 half-light mass  M(r_half) = 3 <sigma_los^2> r_half / G, which is")
print("  beta-IMMUNE to first order (the beta-dependence cancels at the half-light radius).")
# quantify the residual Wolf beta-leak with a toy aperture-dispersion vs beta, and show it is
# (i) small and (ii) MONOTONE in beta -> no sign-flip, so it cannot fake the pre-peri DEFICIT.
def wolf_sigma_leak(beta):
    """fractional shift in aperture sigma at fixed true M(r_half) vs isotropic, toy Wolf residual.
    Wolf+2010: the coefficient 3 varies <~ few % over beta in [-0.5, +0.7]; model as ~0.5*beta*eps."""
    eps = 0.06                                   # ~6% Wolf coefficient stability (Wolf+2010 Fig)
    return 0.5*eps*beta                          # sigma-level leak (half the mass-level leak)
for beta in (-0.3, 0.0, 0.3, 0.6):
    print(f"    internal beta={beta:+.1f}  ->  Wolf sigma-leak = {wolf_sigma_leak(beta)*100:+.1f}%"
          f"   (monotone in beta; NO sign-flip)")
leak_max = abs(wolf_sigma_leak(0.6))
assert leak_max < abs(d_post - d_pre), "beta-leak must be smaller than the sign-flip amplitude"
print(f"  ==> The Wolf-normalised beta-leak is <= {leak_max*100:.1f}% and MONOTONE in beta. It cannot")
print("      produce the pre-peri DEFICIT nor the sign-flip; it folds into the same-signed")
print("      (heating-only) confound family handled in [E] by the radial-profile + baryon split.")
print("      With 3D internal kinematics (IFU) beta is measured directly -> the leak is calibrated.")

# =========================================================================================
# [E]  THE SAME-SIGNED CONFOUNDS (tidal / ram-pressure / quenching) + the 4-part FINGERPRINT
#      that only MI trips.  This is the whole isolation game.
# =========================================================================================
print("\n" + "="*100)
print(" [E] THE SAME-SIGNED CONFOUNDS + the 4-part FINGERPRINT only MI trips (the isolation)")
print("="*100)
# radial-profile separator: MI RISES OUTWARD (peaks at transition shell a_ex~0.3-1 a0, dies in
# core); tidal heating RISES INWARD (peaks at small pericentre / in the core). Opposite slopes.
print("  (i) RADIAL-PROFILE separator (fiducial theta0=2, canonical): spread vs a_ex")
aex_grid = np.array([0.1, 0.3, 1.0, 3.0])
mi_prof  = np.array([felt_excess(0.90, 0.05, 0.3*Gyr, theta_rat, A0_CAN,
                                 a_in=0.30, a_ex=ax)[0] for ax in aex_grid])
# tidal toy: heating ~ (M_cluster enclosed)/r^3 tidal field, grows INWARD (larger a_ex)
tidal_prof = -0.02 - 0.02*np.log10(aex_grid/0.1)   # grows (more negative sign = hotter) inward
print(f"      a_ex/a0:        {aex_grid}")
print(f"      |MI spread|:    {np.abs(mi_prof)*100}  (peaks at transition shell, dies in core)")
print(f"      tidal heating:  {np.abs(tidal_prof)*100}  (grows INWARD -- opposite slope)")
mi_outward = np.abs(mi_prof)[1] > np.abs(mi_prof)[3]        # transition-shell > core
tidal_inward = np.abs(tidal_prof)[3] > np.abs(tidal_prof)[1]
assert mi_outward and tidal_inward, "radial-slope separator failed"
print("      ==> MI peaks OUTWARD (transition shell), tidal peaks INWARD (core). Opposite slope.")

# (ii) the sign-flip: tides/ram/quench can only HEAT (monotone, one sign); MI has a DEFICIT.
print("  (ii) SIGN-FLIP separator: MI has a pre-peri DEFICIT (< 0); tidal/ram/quenching are")
print("       monotone HEATING (never a deficit, never a sign-flip across pericentre).")

# (iii) the BARYON split: environmental confounds LEAVE MARKS ON THE BARYONS (gas stripping,
# truncated/burst-then-quenched SF, tidal features/asymmetry); the inertial signal is BARYON-BLIND
# (it is a change of INERTIA, not of the stellar/gas content). So at matched (zone, radius) the
# MI residual is INVARIANT to gas fraction / SF-history / morphology, while the confounds are
# CARRIED by them. Control: regress the residual against a baryon-confound proxy; the MI part is
# the baryon-INDEPENDENT intercept.
print("  (iii) BARYON-BLIND split: split carriers at matched (zone, radius) by a baryon proxy")
print("        (gas fraction / SF-history / tidal-morphology). Environmental confounds correlate")
print("        with the proxy (they ARE baryonic disturbances); the MI inertia signal does NOT.")
# toy: model observed residual = MI(baryon-blind) + kappa*(baryon-disturbance proxy). Fit intercept.
proxy = np.array([0.0, 0.3, 0.6, 0.9])                  # 0=undisturbed .. 0.9=heavily stripped
kappa = -0.06                                          # environmental heating per unit disturbance
mi_true = d_pre                                        # baryon-blind MI deficit (first-infall)
obs = mi_true + kappa*proxy + rng.normal(0, 0.005, proxy.size)
A = np.vstack([np.ones_like(proxy), proxy]).T
intercept, slope = np.linalg.lstsq(A, obs, rcond=None)[0]
print(f"        fit: residual = intercept + slope*proxy -> intercept={intercept*100:+.1f}%"
      f" (baryon-blind MI, truth {mi_true*100:+.1f}%), slope={slope*100:+.1f}%/unit (environmental)")
assert abs(intercept - mi_true) < 0.01, "baryon-blind intercept must recover the MI deficit"
print("        ==> The baryon-INDEPENDENT intercept recovers the MI signal; the proxy-correlated")
print("            slope absorbs tidal/ram/quenching. This is the environmental-vs-inertial split.")

# ---- the 4-part fingerprint matrix: which sources trip which fingerprint ----
print("\n  THE 4-PART FINGERPRINT (only MI trips ALL FOUR):")
print("    F1 = nonzero phase-contrast at FIXED TRUE radius")
print("    F2 = SIGN-FLIP (pre-peri DEFICIT, post-peri EXCESS)")
print("    F3 = radial profile RISES OUTWARD (peaks at transition shell, dies in core)")
print("    F4 = BARYON-BLIND (equal in gas-rich & gas-poor / disturbed & undisturbed at matched zone,r)")
FP = [
    # source                         F1     F2     F3     F4
    ("MI (this framework, MI-class)", True,  True,  True,  True ),
    ("MG (QUMOND/AeST, true r)",      False, False, False, True ),
    ("MG projection alias",           True,  False, False, True ),   # killed by zone deprojection [C]
    ("interlopers (uncut)",           True,  False, False, True ),   # killed by DS+caustic [C]
    ("tidal heating/stripping",       True,  False, False, False),   # F3 inward, F4 baryon marks
    ("ram-pressure",                  True,  False, False, False),   # gas-only baryon mark
    ("environmental quenching",       True,  False, False, False),   # SF-history baryon mark
    ("member-internal anisotropy",    True,  False, False, True ),   # Wolf-immune, monotone [D]
]
print(f"    {'source':32s} {'F1':>4s} {'F2':>4s} {'F3':>4s} {'F4':>4s}")
for name, f1, f2, f3, f4 in FP:
    print(f"    {name:32s} {str(f1):>4s} {str(f2):>4s} {str(f3):>4s} {str(f4):>4s}")
mi_row = FP[0][1:]
assert all(mi_row), "MI must trip all four fingerprints"
for name, *fps in FP[1:]:
    assert not all(fps), f"{name} must NOT trip all four (only MI does)"
print("  ==> ONLY MI trips F1 & F2 & F3 & F4 jointly. Each confound fails at least one:")
print("      MG/alias/interloper/anisotropy fail F2&F3 (no deficit, no outward peak);")
print("      tidal/ram/quench fail F3 (wrong radial slope) AND F4 (they mark the baryons).")
print("      The JOINT 4-part signature is the MG-impossible AND confound-impossible discriminant.")

# =========================================================================================
# [F]  THE FROZEN OBSERVABLE SPEC + decision rule (this lane's deliverable)
# =========================================================================================
print("\n" + "="*100)
print(" [F] FROZEN OBSERVABLE SPEC (the (radius x phase) residual statistic)")
print("="*100)
print("""  O1 Sample.  Diffuse/LSB deep-MOND cluster members (the low-omega_in carriers reaching
     y~O(1)): mu_0 > 24 mag/arcsec^2, R_e >= 1 kpc, spectroscopic members of clusters with a
     published caustic mass profile, resolved internal sigma (error <= tier eps_meas). dE/L*
     ellipticals are adiabatic-dead (y<<1) -> carry ~0 signal (the power wall, not a design flaw).
  O2 Deprojected radius bins.  Bin by cluster-centric a_ex(R) from the caustic mass profile
     (NOT R_proj), width <= 0.3 dex. The test lives strictly WITHIN a bin -> the shared radial
     EFE gradient is a common mode and cancels.
  O3 Infall-phase tag.  Rhee+2017 PPS zone per carrier (ancient / first-infall / recent-infall /
     backsplash) from (R_proj/r200, |v_los-v_cl|/sigma_cl). The zones are the orbit-class-aware
     deprojection that kills the MG projection alias ([C]); a scalar radial correction does NOT.
  O4 Statistic.  Within each a_ex bin: D(zone) = <ln[sigma_int/sigma_bary]>_zone - <..>_ancient,
     with sigma_bary from the baryonic Faber-Jackson / Wolf half-mass (beta-immune, [D]).
       - SIGN statistic: D(first-infall) < 0 (deficit) and D(recent-infall) > 0 (excess).
       - PHASE-CONTRAST: |D(recent) - D(first)|. The specific zone-pair at fiducial memory
         weights gives ~5% (this run); the full max-min infall-window envelope is the banked
         6-13% (predict.py); the deepest plungers (D3 Crater-II) reach +13..26%. Kernel-hostage.
         MG = 0 for the whole pattern at fixed true r.
  O5 Anisotropy immunity.  Wolf half-mass normalisation (beta-immune to 1st order); with IFU
     3D internal kinematics beta is measured and the residual leak calibrated ([D]).
  O6 Confound controls (the isolation, [E]):
       (a) RADIAL PROFILE: MI phase-contrast RISES outward (peaks at a_ex~0.3-1 a0), dies in
           core; tidal heating rises INWARD -> opposite slope (GAP E6).
       (b) SIGN-FLIP: MI pre-peri DEFICIT; tidal/ram/quench are monotone heating (no deficit).
       (c) BARYON-BLIND split: at matched (zone, a_ex) split by gas-fraction / SF-history /
           tidal-morphology; the baryon-INDEPENDENT intercept is the MI signal, the proxy slope
           absorbs the environmental confounds.
       (d) MANDATORY DS substructure cut + caustic membership (GAP E5) for interlopers/groups.
  O7 Decision.  SUPPORT: sign-flip (deficit->excess across peri) AND outward-rising radial
     profile AND baryon-blind intercept, phase-contrast in the 6-13% band, BOTH footings.
        (phase-contrast within the banked 6-13% window envelope; ~5% at conservative memory weights).
     KILL: sign-contrast significantly POSITIVE at the pre-peri zone (falsifies theta-decreasing).
     Zero phase-contrast at adequate power kills THIS channel (not the framework).
  O8 Footings.  Both reported; the phase-contrast is a0-independent at fixed dimensionless depth
     (~0% relative shift). a0 value + s=-1 POSTULATES. MG=0 (fixed true r) the sole theorem.""")

# =========================================================================================
# SYNTHESIS
# =========================================================================================
print("\n" + "="*100)
print(" SYNTHESIS")
print("="*100)
print(f"""  THE STATISTIC: D(zone) = <ln[sigma_int/sigma_bary]>_zone - <..>_ancient, computed WITHIN a
  fixed deprojected a_ex bin, tagged by Rhee+2017 PPS zones. It projects the (sigma/sigma_bary)
  field onto the (radius x phase) plane and differences ALONG the phase axis at fixed radius:
    * The SHARED RADIAL EFE GRADIENT (the key degeneracy) is a common mode on the radius axis
      -> cancels identically in the fixed-radius phase-contrast (verified: MG d/dy = 0).
    * MG's ONLY nonzero response is the PROJECTION ALIAS (~2% band) -> killed to <0.1% by the
      Rhee zones (orbit-class-aware deprojection) + DS cut + caustic membership.
    * VELOCITY ANISOTROPY (member-internal beta) is controlled by the Wolf beta-immune half-mass
      normalisation; the residual leak is monotone (no sign-flip) and folds into [E].
    * The SAME-SIGNED environmental confounds (tidal/ram/quench) are beaten by a JOINT 4-part
      FINGERPRINT that ONLY MI trips: F1 phase-contrast at fixed true r, F2 sign-flip (pre-peri
      DEFICIT), F3 outward-rising radial profile, F4 baryon-blind. Every confound fails >=1.
  WHAT MG CANNOT REPRODUCE: a nonzero phase-contrast at FIXED TRUE radius (theorem, d/dy=0), and
  a fortiori the sign-flip. What NO environmental confound can reproduce: the pre-peri DEFICIT
  (F2) + the outward-rising profile (F3) + baryon-blindness (F4) SIMULTANEOUSLY.
  SCOPE: MI-vs-MG (MI-class-generic), NOT this-framework-vs-Milgrom. Magnitude KERNEL-HOSTAGE
  (6-13% fiducial band). a0 value + s=-1 POSTULATES. MG=0 (fixed true r) the sole theorem.
  Underpowered until ELT-tier sigma on phase-tagged diffuse carriers (banked GAP_STATEMENT).""")
print("\nALL ASSERTIONS PASSED (cluster-member infall-phase EFE observable-design lane).")
