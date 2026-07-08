#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mi_lensing_prescription.py -- SETUP A: the framework's OWN lensing prescription,
reasoned from the MODIFIED-INERTIA premises (NOT the AeST modified-metric reading).
================================================================================

FRAMEWORK PREMISES (reason from these, do not smuggle standard MOND/AeST-metric):
  * de Sitter-Unruh MODIFIED INERTIA. The modification is to how MASSIVE bodies
    respond to a force: m_inertial is reduced at a<a0, giving
        g_obs = sqrt(g_bar^2 + g_bar*a0),  a0 = c H_Lambda / Z = 9.36e-11 (canonical, rho_DE)
        (alt footing rho_total/cH0 -> 1.13e-10).
    This law governs the acceleration of MASSIVE test bodies (stars, gas).
  * The frame u^mu is PASSIVE (algebraic constitutive law / SME background).
  * The DARK SECTOR is a GHOST CONDENSATE scalar (AeST K(Q)=mu^2(Q-1)^2, Q-mode ->
    w=0 cold a^-3 dust). Its amount I0 ~ Omega_dm is a FREE shift-charge integration
    constant (established standing, ROUTE_C + GHOST_CONDENSATE verdicts).

THE MI LENSING PROBLEM (state precisely):
  LIGHT IS MASSLESS. It has NO inertia. So the de Sitter-Unruh MI modification --
  which acts on the inertial mass of a body responding to a force -- does NOTHING
  to a photon. There is no "reduced inertia" for light: F=ma has no content for m=0.
  Therefore, IN THE MI READING, the MI law does NOT bend light directly.

  Light follows null geodesics of the metric g_mu_nu. In the MI reading the metric
  is the ORDINARY GR metric sourced (Einstein equations, unmodified) by the ACTUAL
  stress-energy: T = T_baryon + T_condensate. There is NO extra "phantom" potential
  that photons see (that phantom potential is the AeST/modified-GRAVITY realization,
  which the task forbids here -- see CONTRAST block below).

  => MI lensing prescription:  alpha = GR lensing of ( baryons + ghost condensate ).
     The deflection is set by the REAL projected mass M_bar(<r) + M_cond(<r).

THE CRUX (what the DATA demand):
  Brouwer+2021 (arXiv:2106.11677) and Mistele-McGaugh 2024 (arXiv:2310.15248):
  the weak-LENSING RAR sits on TOP of the DYNAMICAL RAR at the SAME a0. Lensing and
  dynamics AGREE: both follow g_obs = sqrt(g_bar*a0) in the deep regime. So the
  lensing acceleration g_obs,lens (from REAL mass) must EQUAL the dynamical g_obs,dyn
  (from MI). For that:
        g_lens(r) = G[M_bar + M_cond](<r)/r^2  ==  g_obs,dyn(r) = sqrt(g_bar^2+g_bar a0)
  =>  M_cond(<r) must equal exactly the MI dynamical EXCESS:
        M_cond(<r) = (r^2/G)*[ g_obs,dyn(r) - g_bar(r) ] = M_bar(<r)*(nu(y)-1),  y=g_bar/a0.

  QUESTION: is that condensate profile (a) DETERMINED by the framework's physics
  (tied to the horizon/MI response), (b) a TENSION (a generic ghost condensate
  clusters on its OWN and does NOT track the MI excess), or (c) FINE-TUNED
  (M_cond placed BY HAND to match MI)?

This script: (1) states the prescription numerically on a fiducial isolated galaxy,
(2) computes the condensate profile the data REQUIRE (M_cond = MI excess), (3) asks
whether the framework's OWN condensate physics DELIVERS that profile or leaves it
FREE -- using the established standing (shift charge I0 free; orthogonality
dI0/da0 = 0; ROUTE_C: the condensate clusters like CDM, NOT keyed to the Y/MI gradient),
(4) verifies the AeST-metric contrast (that reading photons-see-phantom is DIFFERENT
physics, walled by Cassini in its MG realization).
Exit 0 = prescription reproduced + verdict printed. No fitted number asserted.
"""
import numpy as np

# ------------------------------------------------------------------ constants
G      = 6.674e-11
Msun   = 1.989e30
KPC    = 3.0857e19
A0_FW  = 9.36e-11          # canonical, rho_DE / cH_Lambda
A0_ALT = 1.13e-10          # alt footing rho_total / cH0
LN10   = np.log(10.0)

def nu(y):
    """framework dS-Unruh interpolation: g_obs = g_bar*nu(y), y=g_bar/a0."""
    return np.sqrt(1.0 + 1.0/y)

def g_obs_dyn(g_bar, a0):
    return np.sqrt(g_bar*g_bar + g_bar*a0)

print("#"*78)
print("# SETUP A -- the framework's OWN (MODIFIED-INERTIA) lensing prescription")
print("#"*78)

# ---------------------------------------------------------------------------
# (0) LIGHT HAS NO INERTIA -- the MI modification does not touch photons
# ---------------------------------------------------------------------------
print("""
(0) DOES THE MI MODIFICATION BEND LIGHT?  -- NO.
    The dS-Unruh modification reduces the INERTIAL MASS m of a body responding to
    a force (a<a0 => m_eff<m => larger a for the same force). A photon has m=0:
    'reduced inertia' is vacuous for m=0 (F=ma carries no information). Light
    follows null geodesics of the GR metric, which the MI law does NOT modify.
    => In the MI reading, lensing is GR lensing of REAL mass, NOT an MI-bent ray.
""")

# ---------------------------------------------------------------------------
# (1) THE PRESCRIPTION on a fiducial isolated point-ish galaxy (Brouwer regime)
# ---------------------------------------------------------------------------
Mbar = 6.0e10*Msun           # ~L* baryonic mass, treated point-like at large r (Brouwer/M24 do this)
print("(1) PRESCRIPTION (fiducial isolated M_bar = 6e10 Msun, point-like):")
print("    alpha_lens set by projected REAL mass  M_bar(<r) + M_cond(<r)  via GR.\n")
print("    log10 gbar |  g_obs,dyn(MI) | g_bar(GR baryon) | REQUIRED M_cond(<r)/M_bar = nu-1")
r_kpc = np.array([50., 100., 200., 400., 800., 1600.])
for rk in r_kpc:
    r = rk*KPC
    g_bar = G*Mbar/r**2
    y = g_bar/A0_FW
    gdyn = g_obs_dyn(g_bar, A0_FW)
    excess_ratio = nu(y) - 1.0                     # M_cond/M_bar required for lensing=dynamics
    print(f"      r={rk:6.0f}kpc  {np.log10(g_bar):7.3f} | gdyn={gdyn:.3e} | gbar={g_bar:.3e} | "
          f"nu-1 = {excess_ratio:6.2f}")
print("""
    The RIGHT column is the condensate lensing mass the DATA require (M_cond = MI excess).
    In deep regime (y<<1): nu-1 -> sqrt(a0/g_bar) grows without bound; M_cond(<r) ~ r
    (isothermal-like, M_cond ~ sqrt(G M_bar a0)*r/G). THIS is what lensing must see.
""")

# ---------------------------------------------------------------------------
# (2) DOES THE FRAMEWORK'S OWN CONDENSATE DELIVER M_cond = MI excess?
#     Reason from the ESTABLISHED ghost-condensate standing.
# ---------------------------------------------------------------------------
print("(2) IS M_cond(r) DETERMINED BY THE FRAMEWORK, OR A FREE DARK-FLUID PROFILE?")
print("""
    Established standing (GHOST_CONDENSATE_2026-06-19; ROUTE_C_CONDENSATE_ACCUMULATION):
      * The condensate dust amplitude is I0 = the CONSERVED shift charge (a^3 K'(Q)=I0),
        set by INITIAL CONDITIONS, not by the local acceleration field.
      * ORTHOGONALITY (shift Ward identity): dI0/d(grad phi) = 0, i.e.
        d rho_dust / d a0 = 0 and d rho_dust / d Lambda = 0. The Y-mode (the MI/a0
        gradient) does NOT source / pump the Q-mode (the dust). They are orthogonal
        flat directions.
      * ROUTE_C null: the condensate clusters like CDM (gravitational infall), its
        amount is DIALED by the free I0; there is NO mechanism keying its profile to
        the local MI excess. Making it track a0 needs a NEW free isocurvature function.

    CONSEQUENCE for lensing: a GENERIC ghost-condensate profile M_cond^GC(r) is set by
    its own gravitational clustering + free I0. There is NO framework law that forces
        M_cond^GC(r) == M_bar*(nu(g_bar/a0)-1)   (the MI excess, r-shape AND amount).
    The MI excess has a SPECIFIC radial shape (M_cond ~ r, isothermal, tied to a0 and
    M_bar) and a SPECIFIC amount (fixed by a0, no freedom). The condensate delivers
    neither automatically: amount is free (I0), shape is CDM-like (NFW cusp when
    self-gravitating, gas-tracking cored when subdominant) -- NOT the sqrt(G M a0) r
    isothermal MI profile.
""")

# Quantify the SHAPE mismatch: MI-excess enclosed mass vs a generic NFW-clustered condensate.
def M_MI_excess(r, Mbar, a0):
    g_bar = G*Mbar/r**2
    y = g_bar/a0
    return Mbar*(nu(y)-1.0)            # = (r^2/G)(gdyn-gbar)

def M_NFW(r, Mvir, c, Rvir):
    # generic CDM-like clustered condensate (ROUTE_C: dust clusters like CDM)
    rs = Rvir/c
    m = lambda x: np.log(1+x) - x/(1+x)
    return Mvir * m(r/rs)/m(c)

# pick an NFW that matches the MI excess at ONE radius (200 kpc) -> show it MISSES elsewhere
r_match = 200*KPC
Rvir = 300*KPC; c = 10.0
Mvir_dummy = 1.0
scale = M_MI_excess(r_match, Mbar, A0_FW)/M_NFW(r_match, Mvir_dummy, c, Rvir)
print("    SHAPE TEST -- normalize a CDM-like (NFW) condensate to the MI excess at r=200kpc,")
print("    then compare enclosed mass at other radii (perfect track => ratio 1.0 everywhere):")
print("      r(kpc) | M_MIexcess/M_NFW(tied@200)")
mism = []
for rk in [50., 100., 200., 400., 800.]:
    r = rk*KPC
    ratio = M_MI_excess(r, Mbar, A0_FW)/(scale*M_NFW(r, Mvir_dummy, c, Rvir))
    mism.append(ratio); print(f"        {rk:6.0f} | {ratio:6.3f}")
mism = np.array(mism)
print(f"    => a generic CDM-clustered condensate MISSES the MI-excess SHAPE by "
      f"{np.max(np.abs(np.log10(mism)))/LN10*LN10:.2f} (log10 spread "
      f"{np.max(np.log10(mism))-np.min(np.log10(mism)):.2f} dex). It does NOT auto-track.")

# ---------------------------------------------------------------------------
# (3) CONTRAST: the AeST / modified-GRAVITY reading (FORBIDDEN here) -- why it differs
# ---------------------------------------------------------------------------
print("""
(3) CONTRAST WITH AeST (the MODIFIED-GRAVITY realization -- NOT the MI reading):
    In AeST (Skordis-Zlosnik 2021) light bends in the SAME modified potential that
    governs dynamics: photons see a 'phantom' potential with the GR factor of 2, so
    lensing = dynamics is AUTOMATIC BY CONSTRUCTION (one metric, no separate mass).
    BUT that is a MODIFIED METRIC photons couple to -- MODIFIED GRAVITY, not modified
    inertia -- and its non-relativistic realization is Cassini-WALLED (the AeST=MG
    quadrupole tension, banked). It is ALSO not the honest MI premise: in true MI the
    modification is on the RESPONSE OF MASSIVE BODIES, which cannot touch a massless
    photon. So the framework, read as MI, CANNOT borrow AeST's automatic lensing=dyn.
    Its lensing MUST come from REAL condensate mass -- which, per (2), is FREE.
""")

# ---------------------------------------------------------------------------
# (4) VERDICT
# ---------------------------------------------------------------------------
print("#"*78)
print("# VERDICT (both footings a0=9.36e-11 and 1.13e-10 give the SAME structural answer)")
print("#"*78)
for a0, tag in [(A0_FW,"canonical 9.36e-11"),(A0_ALT,"alt 1.13e-10")]:
    r=200*KPC; g_bar=G*Mbar/r**2
    print(f"   footing {tag}: at r=200kpc required M_cond/M_bar = nu-1 = "
          f"{nu(g_bar/a0)-1:.2f}  (shape ~r isothermal either way)")
print("""
   MI LENSING PRESCRIPTION (SETUP A):
     alpha = GR lensing of ( baryons + ghost-condensate dark sector ).
     Light is massless -> the dS-Unruh MI modification does NOT bend light.
     NOT an MI-modified metric photons see (that is AeST/MG, Cassini-walled).

   IS THE CONDENSATE PROFILE DETERMINED OR FREE?  -> FREE.
     The condensate amount I0 (~Omega_dm) is a free shift charge; its profile
     clusters like CDM and is ORTHOGONAL to the MI/a0 gradient (dI0/da0=0). The
     framework has NO law forcing M_cond(r)=M_bar(nu-1). To make lensing=dynamics
     hold (as Brouwer+21 / Mistele-McGaugh24 observe), the condensate profile must
     be PLACED BY HAND to equal the MI dynamical excess in BOTH shape (~r isothermal)
     and amount (fixed by a0).

   => The observed lensing=dynamics is, in the MI reading, a FINE-TUNING (a fit),
      NOT a framework prediction. Honest: this is where many dark-sector theories
      sit. It is NOT a data TENSION (the profile CAN be placed to match -- the data
      are reproduced), and it is NOT a principled CONSISTENT_PREDICTED (nothing in
      the framework's two-sector physics ties the free condensate to the MI excess).
""")
print("SETUP A prescription + free/determined verdict printed. exit 0.")
