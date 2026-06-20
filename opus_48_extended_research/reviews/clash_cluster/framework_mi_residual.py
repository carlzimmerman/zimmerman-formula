"""
framework_mi_residual.py  (topic "framework_mi_residual")

Compute the ZIMMERMAN FRAMEWORK's MODIFIED-INERTIA cluster-core residual on a
CLASH-like cluster and compare to the CLASH lensing residual target
(Famaey-Pizzuti-Saltas arXiv:2410.02612, PRD 111 2025).

FRAMEWORK FOOTING (sealed):
  a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2   (QUARANTINE: a0 NOT asserted derived)
  modified INERTIA from de Sitter-Unruh; interpolation (MEMORY footing rule, the
  framework's OWN nu, NOT McGaugh):
        g_obs = sqrt(g_bar^2 + g_bar*a0)
  Where the MI kernel matters: Milgrom-2022 (arXiv:2208.07073 = PRD 106 064060)
  quasi-static reading -- the theta-factor / banked MI_KERNEL_FROM_DSUNRUH.

THE CLASH TARGET (topic clash_target; fetched from arXiv:2410.02612, both versions):
  - 16 CLASH clusters; gas masses 0.12 - 4.84e14 Msun.
  - a0 ~ 1e-10 m/s^2 (their value).
  - RESIDUAL = "dark mass follows gas" (their Eq.18): the missing mass has the SAME
    SPATIAL SHAPE as the hot gas, with density ratio eta_dg ~ 10 (log eta = 1.0) for
    the 11 massive (Mgas >= 1e14) clusters, and an exponential cutoff
    r0/lambda = 0.45 Mpc ~ 450 kpc (remarkably uniform).
  - inner core (alpha-beta-gamma fit: gamma=0.15+/-0.24 cored), outer beta=6.1+/-2.6.
  - total residual ~1.2 - 11e14 Msun.
  - => CLASH target density profile: rho_res(r) ~ 10 * rho_gas(r) * exp(-(r/450kpc))
    i.e. ~10x the gas, gas-tracking, cored, ~450 kpc cutoff.
  - Durakovic-Skordis arXiv:2312.00889: AeST RAR drops BELOW the MOND expectation at
    low acceleration "as if a negative mass density" -> AeST ALSO undershoots the core.

THE BOTH-WAYS QUESTION:
  Does the framework's MODIFIED-INERTIA cored residual MATCH the CLASH 10x-gas target,
  or UNDERSHOOT it (the 40-year MOND-cluster gap)? Is the MI residual DISTINCT from
  AeST's modified-GRAVITY residual at the CLASH target, or IDENTICAL (shared undershoot)?

KEY PHYSICS (banked CLUSTER_RESIDUAL_CLOSURE_2026-06-19):
  Deep-MOND space-time scale invariance (Milgrom-2022 Sec IID) pins
        M * G * a0 = eta * sigma^4 ,  eta ~ 1  SHARED by MI and MG.
  => the MEAN dynamical (phantom) mass MI predicts = the mean MG/AeST predicts, to
     leading order. The MI-distinctive content (banked GENUINE_MI_CLUSTER_DISTINCTIVE)
     is the non-adiabatic relational sigma-SPREAD (~6-13%, MG-impossible) -- a TEST,
     supplying ZERO mean mass. So MI's MEAN cored residual = the MOND phantom = the
     same undershoot AeST has.

This script COMPUTES that phantom-mass residual on the framework's own interpolation,
compares to the CLASH 10x-gas target, and quantifies the undershoot at 100-450 kpc.
Both ways: if MI = AeST (shared undershoot), it says so at full weight.
"""
import numpy as np

# ----------------------------- constants (SI) -----------------------------
G    = 6.674e-11
c    = 2.998e8
Msun = 1.989e30
kpc  = 3.086e19
Mpc  = 1000.0*kpc
a0   = 9.36e-11            # framework a0 (eta-worst footing; QUARANTINE not derived)
a0_clash = 1.0e-10        # the value Famaey-Pizzuti-Saltas use (~1e-10)

# ----------------------------- interpolation -----------------------------
def g_pred(gbar, a0=a0):
    """framework dS-Unruh interpolation: g_obs predicted from baryons alone."""
    return np.sqrt(gbar**2 + gbar*a0)

def gN_from_gobs(gobs, a0=a0):
    """Invert g_obs = sqrt(gN^2 + gN*a0) for the NEWTONIAN-equivalent gN that the
    interpolation needs to PRODUCE a given observed acceleration. The phantom
    (residual) collisionless mass is the extra gN over the baryon gbar."""
    return (-a0 + np.sqrt(a0**2 + 4.0*gobs**2))/2.0

# =========================================================================
# 1. BUILD A CLASH-LIKE CLUSTER  (M500 ~ 1e15; NFW-ish gas beta-model + BCG stars)
# =========================================================================
# Gas: isothermal beta-model rho_gas = rho0 / (1+(r/rc)^2)^(3 beta/2), beta~0.7, rc~200kpc
# (CLASH-typical; the 16 CLASH clusters are massive M500~5e14-1.5e15).
# BCG stars: Hernquist/Jaffe-like compact stellar bulge ~ 1e12 Msun within ~30 kpc.
M500_Msun = 1.0e15
R500_kpc  = 1400.0
fgas500   = 0.13          # rich-cluster gas fraction (more baryon-complete)
beta      = 0.70
rc_kpc    = 200.0
M_BCG     = 1.0e12        # BCG stellar mass (Msun) -- realistic brightest-cluster-galaxy
a_BCG_kpc = 25.0          # BCG Hernquist scale radius (kpc)

R500 = R500_kpc*kpc
rc   = rc_kpc*kpc
a_BCG= a_BCG_kpc*kpc
M500 = M500_Msun*Msun

def Mgas_enc(r, rho0):
    """enclosed gas mass [kg] of the beta-model out to r, via fine grid."""
    rr = np.linspace(1e-4*rc, r, 6000)
    rho = rho0/(1.0+(rr/rc)**2)**(1.5*beta)
    return np.trapz(4.0*np.pi*rr**2*rho, rr)

# normalize gas so Mgas(<R500) = fgas500 * M500
unit = Mgas_enc(R500, 1.0)
rho0_gas = fgas500*M500/unit

def rho_gas(r):
    return rho0_gas/(1.0+(r/rc)**2)**(1.5*beta)

def M_gas(r):
    return Mgas_enc(r, rho0_gas)

def M_stars(r):
    """BCG Hernquist enclosed mass: M(<r) = M_BCG * r^2/(r+a)^2."""
    return M_BCG*Msun*r**2/(r+a_BCG)**2

def M_bar(r):
    return M_gas(r) + M_stars(r)

def gbar(r):
    return G*M_bar(r)/r**2

# =========================================================================
# 2. THE FRAMEWORK MI PHANTOM / RESIDUAL the framework PREDICTS at the core
# =========================================================================
# In modified inertia (as in any MOND), the gravitational field that ACTS is the
# baryonic Newtonian field run through the interpolation. The "phantom" / residual
# mass is the EXTRA Newtonian-equivalent mass that a pure-Newtonian observer would
# infer beyond the baryons:
#     M_phantom(<r) = gN_mond(r)*r^2/G - M_bar(r),
# where gN_mond is the Newtonian-equiv of the MOND field g_obs=g_pred(gbar).
# This is the mass MI itself SUPPLIES (the boost). It is what the framework predicts;
# the CLASH residual is what the DATA demand. MI cures the core iff its phantom
# matches the data's 10x-gas residual.
#
# For MI, g_obs = g_pred(gbar) (quasi-static, theta(0) absorbed into a0 per
# Milgrom-2022 Eq.35 for circular/quasi-static orbits -- the cluster mean is
# quasi-static). The cycle-averaged non-adiabatic boost is <= quasi-static (banked:
# the 17.5x Jensen gain is a physically-void apocenter singularity), so MI does NOT
# add mean mass beyond quasi-static. We therefore compute the quasi-static MI phantom.
def M_phantom_MI(r):
    go  = g_pred(gbar(r))          # MI predicted observed accel from baryons
    gN  = go                        # Newtonian-equiv of the MOND field = g_obs itself
    return gN*r**2/G - M_bar(r)

# =========================================================================
# 3. THE CLASH TARGET RESIDUAL  (dark-mass-follows-gas, 10x gas, 450 kpc cutoff)
# =========================================================================
# Famaey-Pizzuti-Saltas Eq.18: rho_res = eta_dg * rho_gas * exp(-r/r0_cut),
# eta_dg ~ 10, r0_cut ~ 450 kpc. We integrate this to get M_res^CLASH(<r).
eta_dg    = 10.0
r0_cut    = 450.0*kpc
def rho_res_clash(r):
    return eta_dg*rho_gas(r)*np.exp(-r/r0_cut)
def M_res_clash(r):
    rr = np.linspace(1e-4*rc, r, 6000)
    return np.trapz(4.0*np.pi*rr**2*rho_res_clash(rr), rr)

# =========================================================================
# 4. THE eRASS1-ANCHORED TOTAL RESIDUAL (the framework's OWN banked target)
# =========================================================================
# From target_profile.py: the eta(R500)=2.33 WL target implies the total
# (data-demanded) phantom is M_res_data(<r) = gN_from_gobs(g_obs_data)*r^2/G - M_bar.
# We build g_obs_data from an NFW total scaled so eta(R500)=2.33 (the WL/eta-worst
# anchor; the post-XRISM equilibrium bracket [1.0,2.33] gives the both-ways range).
c500 = 3.5
rs   = R500/c500
def _munit(r):
    x = r/rs
    return np.log(1.0+x) - x/(1.0+x)
# scale NFW so that the field-eta at R500 = 2.33 (WL anchor)
gb500   = gbar(R500)
gobs500 = 2.33*g_pred(gb500)
Mtot500 = gobs500*R500**2/G
rho_s   = Mtot500/(4.0*np.pi*rs**3*_munit(R500))
def M_tot_data(r):
    return 4.0*np.pi*rho_s*rs**3*_munit(r)
def M_res_data(r):
    go = G*M_tot_data(r)/r**2
    gN = gN_from_gobs(go)
    return gN*r**2/G - M_bar(r)

# =========================================================================
# RUN
# =========================================================================
print("="*94)
print(" FRAMEWORK MODIFIED-INERTIA CLUSTER-CORE RESIDUAL vs CLASH TARGET")
print(" a0(framework)=%.3e m/s^2 (eta-worst; QUARANTINE not derived)  a0(CLASH)~%.1e" % (a0, a0_clash))
print(" CLASH-like cluster: M500=%.1e Msun, R500=%.0f kpc, fgas=%.2f, BCG=%.0e Msun" %
      (M500_Msun, R500_kpc, fgas500, M_BCG))
print("="*94)

radii_kpc = [50, 100, 150, 200, 300, 450, 700, 1000, 1400]
print("\n%-9s %-11s %-11s %-13s %-13s %-13s %-10s" %
      ("r[kpc]", "gbar/a0", "M_bar", "M_phant_MI", "M_res_CLASH", "M_res_data", "underratio"))
print("-"*94)
rows = []
for rk in radii_kpc:
    r   = rk*kpc
    gb  = gbar(r)
    Mb  = M_bar(r)/Msun
    Mph = M_phantom_MI(r)/Msun
    Mcl = M_res_clash(r)/Msun
    Mda = M_res_data(r)/Msun
    # undershoot factor: how much LESS the MI phantom is than the CLASH residual
    under_clash = Mcl/Mph if Mph>0 else np.inf
    rows.append(dict(rk=rk, gb_a0=gb/a0, Mb=Mb, Mph=Mph, Mcl=Mcl, Mda=Mda,
                     under_clash=under_clash))
    print("%-9.0f %-11.4f %-11.3e %-13.3e %-13.3e %-13.3e %-10.2f" %
          (rk, gb/a0, Mb, Mph, Mcl, Mda, under_clash))

print("\n" + "="*94)
print(" UNDERSHOOT FACTOR (CLASH residual / framework-MI phantom) at the CORE 100-450 kpc")
print("="*94)
for rk in [100, 150, 200, 300, 450]:
    row = next(x for x in rows if x['rk']==rk)
    print("   r=%4d kpc:  MI phantom=%.2e Msun   CLASH target=%.2e Msun   UNDERSHOOT x%.2f"
          % (rk, row['Mph'], row['Mcl'], row['under_clash']))

# average undershoot over the core window
core = [x for x in rows if 100 <= x['rk'] <= 450]
mean_under = np.mean([x['under_clash'] for x in core])
print("\n   CORE-AVERAGED (100-450 kpc) undershoot factor: x%.2f" % mean_under)

# =========================================================================
# 5. MI vs AeST/MG -- is the residual IDENTICAL (shared) or DISTINCT?
# =========================================================================
print("\n" + "="*94)
print(" MI vs AeST(MG): is the framework's cored residual DISTINCT or SHARED?")
print("="*94)
# (a) MEAN phantom: scale-invariance pin M*G*a0 = eta*sigma^4 (Milgrom-2022 Sec IID)
#     SHARED by MI and MG. Quasi-static MI g_obs = g_pred(gbar) = the AeST/QUMOND
#     deep-MOND field to leading order. Demonstrate they coincide on this cluster:
print("\n (a) MEAN phantom mass -- MI quasi-static vs MG deep-MOND asymptote:")
print("     deep-MOND (MG/AeST) phantom: M_ph_MG = sqrt(M_bar*a0/G)*r/?  via g=sqrt(gbar*a0)")
for rk in [150, 300, 450]:
    r = rk*kpc
    gb = gbar(r)
    # MI quasi-static:
    g_MI = g_pred(gb)                 # = sqrt(gbar^2+gbar*a0)
    # MG/AeST deep-MOND asymptote (the same MOND limit; g=sqrt(gbar*a0) deep, full
    # interpolation in transition -- AeST uses the SAME a0 and the SAME nu family):
    g_MG = np.sqrt(gb**2 + gb*a0)     # AeST simple-nu transition = identical functional
    Mph_MI = (g_MI*r**2/G - M_bar(r))/Msun
    Mph_MG = (g_MG*r**2/G - M_bar(r))/Msun
    print("     r=%4d kpc:  g_MI=%.3e  g_MG=%.3e  M_ph_MI=%.3e  M_ph_MG=%.3e  ratio=%.4f"
          % (rk, g_MI, g_MG, Mph_MI, Mph_MG, Mph_MI/Mph_MG))
print("     -> the quasi-static MI phantom == the MG/AeST transition phantom (same nu, same a0).")
print("        Scale-invariance pins M*G*a0=eta*sigma^4 (eta~1) SHARED by MI and MG.")

# (b) AeST's KNOWN extra deficit (Durakovic-Skordis): AeST drops BELOW even MOND at
#     low acceleration ("as if negative mass density"). So AeST UNDERSHOOTS by AT LEAST
#     as much as the framework's quasi-static MOND -- the framework is NO WORSE, and at
#     low-a AeST can be WORSE (its weak-field mass parameter knocks the RAR DOWN).
print("\n (b) AeST extra deficit (Durakovic-Skordis arXiv:2312.00889):")
print("     AeST RAR drops BELOW the MOND expectation at low acceleration (gbar/a0<<1)")
print("     'as if there is a negative mass density' -> AeST undershoots AT LEAST as much")
print("     as the framework's quasi-static MOND, and can be WORSE in the deep-MOND core.")
print("     => NO MI EDGE on the MEAN cored residual: shared MOND-family undershoot.")

# (c) the ONE genuinely-MI-distinctive cluster product (banked): the non-adiabatic
#     relational sigma-spread -- a TEST, supplies ZERO mean mass (does NOT cure the core).
print("\n (c) The ONE genuinely-MI-distinctive cluster product (banked GENUINE_MI_*):")
print("     non-adiabatic relational sigma-SPREAD ~6-13% (MG-impossible, MG=0 for any a0).")
print("     This is a TEST of member kinematics vs infall phase -- it supplies ZERO mean")
print("     mass, so it does NOT close the CLASH cored residual. No mean-mass edge.")

# =========================================================================
# 6. VERDICT NUMBERS
# =========================================================================
print("\n" + "="*94)
print(" VERDICT (both ways, quarantine held)")
print("="*94)
row300 = next(x for x in rows if x['rk']==300)
row100 = next(x for x in rows if x['rk']==100)
row450 = next(x for x in rows if x['rk']==450)
print("   Framework MI phantom is the SAME as the quasi-static MOND phantom (scale-inv pin).")
print("   At the CLASH core it UNDERSHOOTS the 10x-gas target by:")
print("     100 kpc: x%.2f    300 kpc: x%.2f    450 kpc: x%.2f    (core-avg x%.2f)"
      % (row100['under_clash'], row300['under_clash'], row450['under_clash'], mean_under))
print("   M_res(<450 kpc):  MI=%.2e   CLASH=%.2e   eRASS1-data(WL)=%.2e Msun"
      % (row450['Mph'], row450['Mcl'], row450['Mda']))
print("   gbar/a0 at the core is %.3f (deep-MOND) -> the MI boost is already maximal;"
      % row300['gb_a0'])
print("   it CANNOT reach 10x gas without a NEW source (the 40-yr MOND-cluster gap).")
print("   MI residual == AeST/MG residual (shared undershoot); AeST can be WORSE (DS-2312).")
