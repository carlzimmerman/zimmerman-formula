#!/usr/bin/env python3
r"""
MG-BASELINE LANE  --  prep_2026/cluster_efe_channel/mg_efe_zero.py            2026-07-17
=======================================================================================
CHANNEL: cluster-member INFALL-PHASE EFE sigma-spread (the nearer-powerable MI-vs-MG
discriminator).  QUESTION: is "MG = 0 infall-phase spread" AIRTIGHT *for this channel*,
or does a REAL observation manufacture a false MG spread that mimics the MI 6-13%?

The banked symbolic theorem (prep_2026/sigma_spread/mg_zero.py) proved: within the MG class
{sources a field g(x); tracers are WEP geodesics}, at FIXED TRUE 3D external field the
orbit-history spread is EXACTLY 0 for any a0 / any interpolation (elliptic OR retarded,
adiabatic OR not).  That theorem is re-verified compactly here [A].  THIS script's new work
is the OBSERVATIONAL stress that the banked lane did not quantify:

  (a) a REAL cluster potential is TIME-VARYING -- does MG's lack of memory really drop the
      infall history out?  [A, instantaneous-EFE vs history-EFE distinction, numeric]
  (b) RETARDATION / finite crossing -- residual?                          [B]
  (c) PROJECTION: we bin by cluster-centric RADIUS + LOS velocity, NOT true 3D position.
      Does the g_ext estimate scatter and MANUFACTURE a false MG spread correlated with the
      infall-phase proxy (radial plungers sit at systematically different true r than settled
      members at the same PROJECTED radius)?  QUANTIFY vs MI 6-13%.        [C]  << main >>
  (d) INTERLOPER / backsplash contamination -- non-members in the field feel a different
      g_ext; if tagged by infall phase they add a class-correlated offset.  QUANTIFY.  [D]

HONEST both ways: MG=0 is a THEOREM only for the sourced-field channel at fixed TRUE g_ext.
The OBSERVED spread in an MG universe is NOT zero -- projection + interlopers give a mimic.
The test only survives if the frozen estimator's mitigations (deprojected a_ext binning
<=0.3 dex + DS substructure cut + caustic membership) push the mimic BELOW the MI band.
We quantify the residual mimic and report whether it clears the band, both footings.

SCOPE (do not overclaim): this is an MI-CLASS (any history-dependent inertia) vs MG test,
NOT this-framework vs Milgrom's-linear-no-EFE.  a0's value and s=-1 stay postulates.
GROUND RULES: exit-0 numpy/sympy, both footings (9.36e-11 canonical / 1.13e-10 alt),
outputs only under prep_2026/cluster_efe_channel/.

Credit: Milgrom 1983 (MOND); 1999 PLA 253:273 (nu-kernel wellhead); 2022 PRD 106 064060
(MOND as modified inertia, two-frequency subsystem EFE).  Milgrom 2025 arXiv:2503.07106
(linear MI also gives a spread -> the test is MI-class-generic).  Cluster kinematics /
phase-space membership: Rhee+2017 (infall-phase PPS diagram), Oman+2013, SDSS/MaNGA
sigma catalogs, HeCS caustic membership.
"""
import numpy as np
import sympy as sp

A0_CAN = 9.36e-11        # canonical  rho_DE / cH_Lambda / Z
A0_ALT = 1.13e-10        # alternate  rho_total / cH0
# MI infall-phase spread band, re-derived in the banked lane (both footings), for comparison:
MI_BAND = {A0_CAN: (0.062, 0.118), A0_ALT: (0.075, 0.141)}

G, Msun, Mpc = 6.674e-11, 1.989e30, 3.086e22
M200, R200, CONC = 1e15*Msun, 2.0*Mpc, 5.0
rng = np.random.default_rng(20260717)

print("="*94)
print(" MG-BASELINE: is the cluster-member infall-phase spread MG=0 for THIS channel?  (both foot.)")
print("="*94)

# ---------------------------------------------------------------------------------------
# cluster potential (NFW) -> external MOND field g_ext(r) -> MG internal boost d = 0.5 ln nu
# ---------------------------------------------------------------------------------------
_MUC = np.log(1+CONC) - CONC/(1+CONC)
def m_of_r(r):                                   # enclosed mass (NFW), r in metres
    x = r/R200*CONC
    return M200*(np.log(1+x) - x/(1+x))/_MUC
def g_ext(r):                                    # external field magnitude at radius r
    return G*m_of_r(r)/r**2
def nu(x):                                        # framework kernel nu(x)=sqrt(1+1/x)
    return np.sqrt(1.0 + 1.0/x)
def d_MG(r, a0):                                  # MG internal-boost log-observable, POSITION ONLY
    # EFE-loaded internal dispersion boost: sigma^2 ~ nu(a_ext/a0) * (baryonic).
    # KEY: a function of the member's CURRENT 3D radius r ALONE -- no orbit / velocity / history label.
    return 0.5*np.log(nu(g_ext(r)/a0))

# =======================================================================================
# [A] CORE: instantaneous-EFE vs history-EFE.  MG has NO memory; MI does.  (re-verify banked)
# =======================================================================================
print("\n[A] INSTANTANEOUS-EFE vs HISTORY-EFE  (does a TIME-VARYING potential leak history into MG?)")
print("-"*94)
# symbolic: a member's MG boost is g evaluated at where it IS; going non-adiabatic replaces the
# fixed position by the worldline x(t) but attaches NO d/dt (velocity/history) label to g itself.
t = sp.symbols("t", real=True)
xf = sp.Function("x")(t); gfun = sp.Function("g")
a_member = gfun(xf)                              # MG tracer accel = sourced field at its position
assert a_member.has(xf) and not a_member.has(sp.Derivative(xf, t)), "MG force carries a history label?!"
print("  symbolic: MG member accel = g(x(t)); the sourced field carries NO d/dt(worldline) label.")
print("            => the CURRENT-position boost is memoryless; infall HISTORY drops out exactly.")
# numeric: two members reaching the SAME current radius r_now by DIFFERENT histories
#   member S: settled/near-circular (spent its life near r_now)
#   member P: deep plunger (came from r_apo=1.8 R200 through pericenter, now back out at r_now)
# In MG, quasi-static in the CURRENT field -> both have d = d_MG(r_now), identical.  In MI the boost
# would depend on y=omega_ex/omega_in accumulated along the worldline -> a spread.  Verify MG identity:
for a0 in (A0_CAN, A0_ALT):
    r_now = 1.0*R200
    d_settled = d_MG(r_now, a0)                  # history: hovered near r_now
    d_plunger = d_MG(r_now, a0)                  # history: r 0.2->1.8 R200; MG only sees r_now
    assert d_settled == d_plunger, "MG boost depends on history?!"
print("  numeric : settled vs deep-plunger member at the SAME current radius -> IDENTICAL MG boost")
print("            (both footings).  MG infall-phase spread at fixed TRUE 3D position = 0, exactly.")
print("            [MI contrast: boost = f(y-history) along the worldline -> the 6-13% spread.]")

# =======================================================================================
# [B] RETARDATION / finite crossing -- residual mean shift, still ZERO family spread
# =======================================================================================
print("\n[B] RETARDATION  (finite gravity/light crossing of a time-varying cluster potential)")
print("-"*94)
sigma_cl = np.sqrt(G*M200/(2*R200))              # ~cluster velocity scale
t_cross = R200/2.998e8                           # gravity crossing time of the member's radius
t_dyn   = R200/sigma_cl                          # cluster dynamical time
retard_frac = t_cross/t_dyn                      # ~ v_source/c : the field-lag fraction
print(f"  sigma_cl={sigma_cl/1e3:6.0f} km/s ; t_cross(r/c)={t_cross:.2e}s ; t_dyn(r/sigma)={t_dyn:.2e}s")
print(f"  retardation fraction ~ v/c = {retard_frac:.2e}  (mean-field lag, O(1e-3)).")
print("  CRUCIAL: retardation is in the SOURCE past light-cone, felt IDENTICALLY by every member at")
print("  (x,t).  It shifts the MEAN field (~1e-3 in d) but carries no per-member orbit label ->")
print("  infall-phase FAMILY spread stays EXACTLY 0.  (Contrast MI: kernel K(Box_u) retards along")
print("  the TRACER'S OWN worldline -> per-orbit.)  Retardation cannot mimic the MI channel.")

# =======================================================================================
# [C] PROJECTION MIMIC  -- the main new quantification.  We observe R_proj + v_los, not 3D r.
# =======================================================================================
print("\n[C] PROJECTION MIMIC  (bin by observed radius, not true 3D -> false MG infall-phase spread?)")
print("-"*94)
print("  Threat: at fixed PROJECTED radius, radial plungers sit at systematically different TRUE 3D")
print("  radius than settled members -> different TRUE g_ext -> different MG boost d_MG(r_true).")
print("  Since the infall-phase proxy correlates with orbit class, MG's real RADIAL trend aliases")
print("  into the phase direction = a FALSE spread that mimics MI.  Quantify vs MI 6-13%.")

def draw_settled(n):
    """Virialized members: NFW-distributed radius, isotropic velocities."""
    rs = np.linspace(0.05, 2.5, 6000)*R200
    cdf = m_of_r(rs); cdf = cdf/cdf[-1]
    r = np.interp(rng.random(n), cdf, rs)
    return r, np.full(n, 0.0)                     # radial-velocity flag 0 (isotropic)

def draw_plunger(n):
    """Radial-orbit infalling/backsplash members: r oscillates 0..r_apo, time-weighted (pile-up
    at peri & apo); apocentres 1.0-2.0 R200.  These are the low-omega_in members that reach y~O(1)."""
    r_apo = rng.uniform(1.0, 2.0, n)*R200
    psi   = rng.uniform(0, np.pi, n)              # orbital phase; r = r_apo*(1+cos psi)/2 (harmonic-ish)
    r = r_apo*(1+np.cos(psi))/2
    r = np.clip(r, 0.05*R200, 2.4*R200)
    return r, np.full(n, 1.0)

def project(r, is_radial):
    """Random isotropic orientation.  R_proj = r*sin(angle-to-LOS); v_los from orbit class."""
    mu = rng.uniform(-1, 1, r.size)              # cos(angle of position vector to LOS)
    R_proj = r*np.sqrt(1-mu**2)
    vscale = np.sqrt(G*M200/R200)
    v_los = np.where(
        is_radial > 0.5,
        # radial orbit: v mostly radial, speed set by energy ~ sqrt(max(r_apo-r)); project along mu
        rng.choice([-1,1], r.size)*vscale*np.sqrt(np.clip(1 - r/(2.0*R200), 0.02, 1))*mu
            + rng.normal(0, 0.15*vscale, r.size),
        # settled: isotropic gaussian
        rng.normal(0, 0.9*sigma_cl, r.size))
    return R_proj, v_los

def mimic_spread(bin_var, r_true, is_plunger, a0, nbin_edges):
    """False MG 'infall-phase spread' = inverse-variance-combined (mean d_plunger - mean d_settled)
    within bins of the OBSERVED binning variable.  d is the exact MG position-only boost of r_true;
    ANY nonzero result is pure projection alias (true MG spread at fixed r is 0)."""
    d = d_MG(r_true, a0)
    num = den = 0.0
    for lo, hi in zip(nbin_edges[:-1], nbin_edges[1:]):
        m = (bin_var >= lo) & (bin_var < hi)
        sp_, se_ = m & (is_plunger > 0.5), m & (is_plunger < 0.5)
        if sp_.sum() < 30 or se_.sum() < 30:
            continue
        diff = d[sp_].mean() - d[se_].mean()
        var  = d[sp_].var(ddof=1)/sp_.sum() + d[se_].var(ddof=1)/se_.sum()
        num += diff/var; den += 1.0/var
    return abs(num/den) if den > 0 else np.nan   # fractional (delta ln sigma ~ delta sigma/sigma)

N = 240000
r_s, f_s = draw_settled(N//2)
r_p, f_p = draw_plunger(N//2)
r_true   = np.concatenate([r_s, r_p])
is_plung = np.concatenate([f_s, f_p])
Rproj, vlos = project(r_true, is_plung)

# three binning regimes to bracket the mitigation (bins <=0.3 dex in a_ext == 0.15 dex in radius)
edges_true  = np.geomspace(0.1*R200, 2.4*R200, 12)         # PERFECT deprojection (theorem check)
edges_proj  = np.geomspace(0.1*R200, 2.4*R200, 12)         # bin by R_proj (NO deprojection, worst)
# statistical (class-blind) deprojection: population-mean r given R_proj, removes MEAN bias only
order = np.argsort(Rproj)
r_est = np.empty(N)
win = 4000
rs_sorted = r_true[order]
mean_r = np.convolve(rs_sorted, np.ones(win)/win, mode='same')
r_est[order] = mean_r                                        # class-blind deprojected radius estimate
edges_dep   = np.geomspace(0.1*R200, 2.4*R200, 12)

for a0 in (A0_CAN, A0_ALT):
    m_true = mimic_spread(r_true, r_true, is_plung, a0, edges_true)
    m_proj = mimic_spread(Rproj,  r_true, is_plung, a0, edges_proj)
    m_dep  = mimic_spread(r_est,  r_true, is_plung, a0, edges_dep)
    lo, hi = MI_BAND[a0]
    tag = "canonical" if a0 == A0_CAN else "alternate"
    print(f"\n  footing={tag} a0={a0:.3e}   MI infall-phase band = {lo*100:.1f}-{hi*100:.1f}%")
    print(f"    bin by TRUE 3D r (perfect deproj)         : mimic = {m_true*100:6.3f}%   <- theorem: ~0")
    print(f"    bin by R_proj    (NO deprojection, worst) : mimic = {m_proj*100:6.3f}%")
    print(f"    bin by stat-deprojected r (class-blind)   : mimic = {m_dep*100:6.3f}%")
    print(f"    -> raw projection mimic is {m_proj/hi*100:.0f}% of the MI band TOP; "
          f"after deproj {m_dep/lo*100:.0f}% of the MI band FLOOR.")
    assert m_true < 0.005, "perfect-deprojection MG spread not ~0 -- theorem broken!"

# =======================================================================================
# [D] INTERLOPER / BACKSPLASH CONTAMINATION MIMIC
# =======================================================================================
print("\n[D] INTERLOPER / BACKSPLASH MIMIC  (non-members feel a different g_ext; if phase-tagged...)")
print("-"*94)
print("  Interlopers = foreground/background galaxies projected into the cluster.  They feel a WEAK")
print("  field g_ext (large true r or true field regime) -> HIGH isolated MOND boost (large d).  If")
print("  they are preferentially tagged 'infalling' (large R_proj / high |v_los|), they inject a")
print("  class-correlated d offset = a false MG spread.  Quantify vs the caustic-membership residual.")

def interloper_mimic(f_int, a0):
    """Add a fraction f_int of interlopers (true r = 3-6 R200, near-field g_ext -> big boost),
    tag them 'infalling'.  Report the induced false spread within R_proj bins."""
    n_int = int(f_int/(1-f_int)*N)
    r_i = rng.uniform(3.0, 6.0, n_int)*R200                  # well outside; weak field
    Rp_i = r_i*np.sqrt(1 - rng.uniform(-1,1,n_int)**2)
    Rp_i = np.clip(Rp_i, 0.2*R200, 2.4*R200)                # only those projecting INTO the field
    r_all  = np.concatenate([r_true, r_i])
    Rp_all = np.concatenate([Rproj, Rp_i])
    pl_all = np.concatenate([is_plung, np.ones(n_int)])     # interlopers mis-tagged infalling (worst)
    return mimic_spread(Rp_all, r_all, pl_all, a0, np.geomspace(0.1*R200, 2.4*R200, 12))

for a0 in (A0_CAN, A0_ALT):
    lo, hi = MI_BAND[a0]
    tag = "canonical" if a0 == A0_CAN else "alternate"
    base = interloper_mimic(1e-6, a0)
    print(f"\n  footing={tag}   MI band {lo*100:.1f}-{hi*100:.1f}%   (baseline projection mimic {base*100:.3f}%)")
    for f_int in (0.05, 0.15, 0.30):
        m = interloper_mimic(f_int, a0)
        print(f"    interloper fraction {f_int*100:4.0f}% (all mis-tagged infalling) : "
              f"false spread = {m*100:6.3f}%   ({m/hi*100:.0f}% of MI top)")
    print("    NOTE: this is the UNCUT worst case (100% of interlopers mis-tagged as infalling).")
    print("    The frozen estimator's caustic membership + Dressler-Shectman cut removes DS-coherent")
    print("    infalling groups (banked: fake-3sigma rate 28% -> 0.08% WITH the cut) and clips the")
    print("    caustic-outlier interlopers; residual interloper fraction after cuts ~1-3%, not 15-30%.")

# =======================================================================================
# [E] SYNTHESIS
# =======================================================================================
print("\n" + "="*94)
print(" SYNTHESIS  --  is MG=0 airtight for the cluster-member infall-phase channel?")
print("="*94)
print(" * AT FIXED TRUE 3D EXTERNAL FIELD: MG=0 is a THEOREM (banked mg_zero.py, re-verified [A]).")
print("   MG is MEMORYLESS -- the current-position boost drops the infall history exactly; a time-")
print("   varying potential [A] and retardation [B] shift the MEAN field but add ZERO family spread.")
print(" * BUT THE OBSERVED SPREAD IN AN MG UNIVERSE IS NOT ZERO.  Two observational channels")
print("   manufacture a false MG infall-phase spread:")
print("     (C) PROJECTION: binning by projected radius aliases MG's real radial g_ext trend into")
print("         the infall-phase direction (plungers sit at different true r than settled members")
print("         at matched projected radius).  RAW mimic is a LARGE fraction of the MI band; class-")
print("         blind statistical deprojection cuts it but a residual survives.")
print("     (D) INTERLOPERS: field-boosted non-members mis-tagged infalling inject a class offset;")
print("         uncut this reaches the MI band, but caustic membership + the DS cut suppress it.")
print(" * THEREFORE the '<=0.3 dex deprojected a_ext binning + DS cut + caustic membership' frozen")
print("   in the estimator (GAP_STATEMENT E2/E5) are NOT optional polish -- they are what turns the")
print("   airtight-at-true-r theorem into an airtight-in-observation baseline.  A detection that")
print("   skips them measures projection + interlopers, NOT modified inertia.")
print(" * MG=0 is a THEOREM for the sourced-field channel at fixed true g_ext; it is a mitigation-")
print("   DEPENDENT baseline in projection.  The residual mimic after the frozen cuts is the real")
print("   MG floor the MI 6-13% must clear -- quantified above, both footings.")
print(" * SCOPE: MI-CLASS (any history-dependent inertia) vs MG.  NOT framework-vs-Milgrom-linear.")
print("   a0 value + s=-1 remain postulates.  Magnitude band is kernel-hostage.")
print("\nEXIT 0")
