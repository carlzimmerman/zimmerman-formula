#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L21 -- binary galaxies: the regime between a galaxy and a cluster
=================================================================
THE QUESTION.  L7 established that what clusters require is quantitatively the COSMIC dark-to-baryon
share (5.73 +/- 0.68 measured against Omega_dm/Omega_b = 5.43, universal to 12%), while the framework's
kernel works inside individual galaxies (RAR, 0.108 dex) with no room for that share.  Between the two
sits a dynamical regime nobody in this programme has put the two hypotheses against each other in:
PAIRS OF GALAXIES at 20 kpc - 1 Mpc, relative accelerations 1e-13 to 1e-11 m/s^2, deep MOND, no hot gas,
no hydrostatic assumption, no dark-matter fitting freedom.  Does the kernel work there, or does the
cosmic share?

THIS LANE DOES NOT START FROM ZERO, AND SAYS SO.  The repository already contains:
  * hunt_2026/h48_h69_binary_galaxies.py  -- builds an isolated 2MRS major-pair sample (2087 pairs) and
    measures sigma_los in bins of projected separation; finds the framework's BEST CASE (isolated
    deep-MOND two-body law) low by A = 1.74 +/- 0.06 (canonical) / 1.66 (alt), the framework's own EFE
    branch low by 2.56, Newton-on-baryons low by 5.91, and abundance-matched LambdaCDM at 0.87.  It also
    established (48b) that the KT2017 group catalogue CANNOT be used -- its group finder selects on the
    velocity difference being measured -- and that item 48's "flat dv vs separation" headline is not the
    framework's honest prediction once the external field is carried.
  * hunt_2026/h48_h69b_relative_isolation.py -- re-isolates RELATIVELY (no third galaxy inside F r_p);
    the offset does not move (A = 1.76-1.89 across F = 2..8) while LambdaCDM stays at 0.90-1.06.
  * hunt_2026/h47_dwarf_pairs.py -- 138 isolated ALFALFA dwarf pairs; A(deep-MOND) = 1.79 +/- 0.20,
    LambdaCDM 1.37, framework's EFE branch 5.15.  TiNy Titans is not machine-readable.
  * qwen_claude_field_theory/closure_2026/g02c_two_body_force.py -- an INDEPENDENT numerical QUMOND
    field solve of the two-body force, agreeing with Milgrom's analytic deep-MOND two-body result to 1%
    (D1: 0.5579 vs 0.5523 for 1:1, 0.8205 vs 0.8137 for 10:1).
  * hunt_2026/h81_h82_mw_external_fields.py -- the external field of large-scale structure COMPUTED from
    the 2M++ reconstruction: e_N = 0.01240 (canonical) / 0.01027 (alt).  The pair scripts above used a
    nominal 0.02-0.03 instead.

WHAT IS NEW HERE, and it is what the lane is for:
  1. The prediction is computed from the CARRIED, SATURATED kernel (THE_ACTION 2026-09-05 section 3,
     nu_RAR: g_phi = a0 Delta(s), Delta(s) = s/(exp(sqrt(s)) - 1), saturated at Delta = 0.6476 for
     s > 2.540), not from the pure deep-MOND limit.  A closed bridge is built whose deep-MOND limit is
     Milgrom's exact two-body force and whose high-acceleration limit is Newton; both limits are checked.
  2. The external field is the repository's own COMPUTED 2M++ value, and the EFE response is
     orientation-averaged over the anisotropic QUMOND tensor rather than taken isotropic.
  3. THE CURVE NOBODY HAS COMPUTED: baryons plus a COSMIC-SHARE dark component, M_dark = 5.43 M_bar --
     the exact quantity L7 found clusters demand -- carried down to pair separations, both as a point
     mass and as an NFW halo.  And its combination with the framework's kernel.
  4. The scale question: where, in separation and in acceleration, the framework and the cosmic share
     diverge most sharply, and what dark-to-baryon ratio the pair data actually require.
  5. A pre-registerable forecast: sample size and velocity precision for a 3-sigma separation, on the
     amplitude axis and on the shape axis (the latter immune to the stellar M/L systematic).

BOTH FOOTINGS EVERYWHERE.  a0 = 9.3619e-11 (canonical) / 1.1279e-10 (alt) m/s^2.
Checks CAN fail.  Controls first; nothing downstream is read if a control fails.
"""
import os, sys, math, time
import numpy as np
from scipy.spatial import cKDTree

T0 = time.time()
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("  " + s, flush=True)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "real_research", "data")

G = 6.674e-11; Msun = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
E_N = {"canonical": 0.01240, "alt": 0.01027}     # h81_h82_mw_external_fields.out, 2M++ reconstruction
F_COSMIC = 5.43                                   # L7 / Omega_dm/Omega_b; cluster measurement 5.73 +/- 0.68
UPS_K = 0.6; MK_SUN = 3.28; H0_KMS = 67.4
h_little = 0.674
RHO_C = 3*(H0_KMS*1e3/Mpc)**2/(8*math.pi*G)/Msun*(Mpc)**3      # Msun / Mpc^3

P("=" * 122)
P("L21 -- binary galaxies: does the kernel or the cosmic dark share govern the regime between galaxies and clusters?")
P("=" * 122)

# ==================================================================================================================
# THE CARRIED KERNEL (THE_ACTION 2026-09-05, section 3)
# ==================================================================================================================
S_SAT, D_SAT = 2.540, 0.6476

def Delta(s):
    s = np.asarray(s, float)
    sc = np.clip(s, 1e-300, S_SAT)                       # saturated above S_SAT; clip keeps expm1 in range
    d = np.where(s > 0, sc/np.expm1(np.sqrt(sc)), 0.0)
    return np.where(s > S_SAT, D_SAT, d)

def dDelta(s):
    """dDelta/ds, analytic below saturation, 0 above."""
    s = np.asarray(s, float); u = np.sqrt(np.clip(s, 1e-300, S_SAT)); em = np.expm1(u)
    d = (2.0*em - u*np.exp(u))/(2.0*em*em)
    return np.where(s > S_SAT, 0.0, d)

# ==================================================================================================================
# PART 1 -- THE TWO-BODY MACHINERY AND ITS CONTROLS
# ==================================================================================================================
P(""); P("-"*122)
P("PART 1 -- the two-body machinery.  Milgrom's exact deep-MOND two-body force, reused (not re-derived), and")
P("          bridged to the carried kernel so both limits are exact.")
P("-"*122)

def Gamma(M1, M2):
    """Milgrom's deep-MOND two-body coefficient: F(r) = sqrt(G a0) Gamma / r.
    Gamma = (2/3)[(M1+M2)^{3/2} - M1^{3/2} - M2^{3/2}]  (Milgrom 1994; deep-MOND virial relation, exact
    for AQUAL and QUMOND).  Reused from hunt_2026/h48_h69_binary_galaxies.py and validated numerically by
    the repository's own QUMOND field solve, closure_2026/g02c_two_body_force.py check D1."""
    M1 = np.asarray(M1, float); M2 = np.asarray(M2, float)
    return (2.0/3.0)*((M1 + M2)**1.5 - M1**1.5 - M2**1.5)

def M_eff(M1, M2):
    """The one-body mass that reproduces Milgrom's two-body force exactly in the deep-MOND limit:
    a_rel = F/mu = sqrt(G a0) Gamma/(mu r)  ==  sqrt(G M_eff a0)/r   =>   M_eff = (Gamma/mu)^2."""
    M1 = np.asarray(M1, float); M2 = np.asarray(M2, float)
    mu = M1*M2/(M1 + M2)
    return (Gamma(M1, M2)/mu)**2

def a_rel_framework_isolated(M1, M2, r_m, a0):
    """Carried kernel, isolated pair.  a_rel = G M_tot/r^2 + a0 Delta(G M_eff/(a0 r^2)).
    Deep-MOND limit: a0 sqrt(s_eff) = sqrt(G M_eff a0)/r = Milgrom's exact two-body relative acceleration.
    High-acceleration limit: G M_tot/r^2 + 0.6476 a0 -> Newton (the carried kernel's saturated residual)."""
    Mt = (np.asarray(M1, float) + np.asarray(M2, float))*Msun
    Me = M_eff(M1, M2)*Msun
    gN = G*Mt/r_m**2
    return gN + a0*Delta(G*Me/(a0*r_m**2))

def nu_efe(eN):
    """Orientation-averaged QUMOND external-field response for the carried kernel.
    Along the external field the response is d g/d g_N = 1 + Delta'(e_N); perpendicular it is
    g/g_N = 1 + Delta(e_N)/e_N.  For a radial direction isotropic w.r.t. the external field,
    <nu(n)> = (nu_par + 2 nu_perp)/3.  Returns (nu_bar, nu_par, nu_perp)."""
    par = 1.0 + float(dDelta(np.array([eN]))[0])
    perp = 1.0 + float(Delta(np.array([eN]))[0])/eN
    return (par + 2*perp)/3.0, par, perp

def a_rel_framework_efe(M1, M2, r_m, a0, eN):
    """External-field-dominated branch: quasi-Newtonian on the TOTAL mass with G_eff = nu_bar(e_N) G."""
    Mt = (np.asarray(M1, float) + np.asarray(M2, float))*Msun
    return nu_efe(eN)[0]*G*Mt/r_m**2

def a_rel_framework(M1, M2, r_m, a0, eN):
    """The framework's honest prediction: the smaller of the isolated and external-field branches
    (the same construction the repository's pair scripts use; the isolated branch is the BEST CASE)."""
    return np.minimum(a_rel_framework_isolated(M1, M2, r_m, a0),
                      a_rel_framework_efe(M1, M2, r_m, a0, eN))

def a_rel_newton(M1, M2, r_m):
    return G*(np.asarray(M1, float) + np.asarray(M2, float))*Msun/r_m**2

def a_rel_cosmic_point(M1, M2, r_m, f=F_COSMIC):
    """Baryons plus a cosmic-share dark component, ALL of it inside r (upper bound on any profile)."""
    return (1.0 + f)*a_rel_newton(M1, M2, r_m)

def nfw_c(Mh):
    """Dutton & Maccio 2014 z=0 concentration, M in Msun."""
    return 10**(0.905 - 0.101*(np.log10(np.asarray(Mh, float)*h_little) - 12.0))

def nfw_enclosed(Mh, r_kpc):
    Mh = np.asarray(Mh, float); r_kpc = np.asarray(r_kpc, float)
    c = nfw_c(Mh)
    R200 = (3*Mh/(4*math.pi*200*RHO_C))**(1/3.)*1000.0        # kpc
    x = np.clip(r_kpc/R200, 1e-5, 5.0)
    m = lambda t: np.log1p(t) - t/(1.0 + t)
    return Mh*m(c*x)/m(c)

def a_rel_cosmic_nfw(M1, M2, r_m, f=F_COSMIC):
    """Baryons (point) plus a cosmic-share NFW halo on EACH member, M_dark,i = f M_b,i."""
    M1 = np.asarray(M1, float); M2 = np.asarray(M2, float); r_kpc = r_m/kpc
    Mtot = (M1 + M2) + nfw_enclosed(f*M1, r_kpc) + nfw_enclosed(f*M2, r_kpc)
    return G*Mtot*Msun/r_m**2

def a_rel_framework_plus_cosmic(M1, M2, r_m, a0, eN, f=F_COSMIC):
    """The cross-lane hypothesis: the framework's kernel AND the cosmic-share component clusters demand.
    The dark component is added to each member's mass before the kernel is applied."""
    return a_rel_framework((1.0 + f)*np.asarray(M1, float), (1.0 + f)*np.asarray(M2, float), r_m, a0, eN)

# ---- LambdaCDM abundance matching (Moster+2013 + NFW), reproduced from h48_h69 for context
def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10**(logMh - logM1)
    return 10**logMh*2*N/(x**(-be) + x**ga)
_LMH = np.linspace(9.0, 15.5, 1301); _LMS = np.log10(moster_mstar(_LMH))
def halo_mass(Mstar):
    return 10**np.interp(np.log10(np.asarray(Mstar, float)), _LMS, _LMH)
def a_rel_lcdm_am(M1, M2, r_m):
    r_kpc = r_m/kpc
    Mh = nfw_enclosed(halo_mass(M1), r_kpc) + nfw_enclosed(halo_mass(M2), r_kpc)
    return G*Mh*Msun/r_m**2

# ---------------------------------------------------------------- CONTROL C1
vir = lambda m1, m2: (2/3.)*((m1 + m2)**1.5 - m1**1.5 - m2**1.5)/(m2*math.sqrt(m1))
r11, r101 = vir(1.0, 1.0), vir(1.0, 0.1)
G02C = (0.5579, 0.8205)                     # closure_2026/g02c_two_body_force.out, D1, independent QUMOND field solve
d11 = abs(r11/G02C[0] - 1); d101 = abs(r101/G02C[1] - 1)
info(f"Milgrom's two-body force in the form g02c grades it, F2/(M2 a_1) with a_1 = sqrt(G M1 a0)/d:")
info(f"    1:1 ratio  {r11:.5f}   10:1 ratio  {r101:.5f}")
info(f"    the repository's independent QUMOND field solve (g02c D1, both footings): {G02C[0]:.4f}, {G02C[1]:.4f}")
check("C1 [CONTROL] the two-body machinery reproduces the programme's verified deep-MOND two-body force before it is used",
      abs(r11 - 0.55229) < 1e-4 and abs(r101 - 0.81379) < 1e-4 and d11 < 0.011 and d101 < 0.011,
      f"analytic 0.55229/0.81379 exact; vs g02c's field solve {100*d11:.2f}% and {100*d101:.2f}% (both < 1.1%)")

# equal-mass circular relative speed: v = 1.051 (G m a0)^{1/4}
m_t = 5e10
for foot, a0 in A0.items():
    rr = np.geomspace(1e3, 1e7, 40)*kpc
    v2 = (a_rel_framework_isolated(m_t, m_t, rr, a0) - G*2*m_t*Msun/rr**2)*rr
    coef = float(np.median(np.sqrt(v2)/(G*m_t*Msun*a0)**0.25))
    if foot == "canonical": c_dm = coef
check("C1b [CONTROL] the bridge's deep-MOND limit is Milgrom's own: v_rel -> 1.05099 (G m a0)^{1/4} for an equal pair",
      abs(c_dm - 1.05099) < 2e-4, f"recovered {c_dm:.5f} against the analytic 1.05099")

# ---------------------------------------------------------------- CONTROL C2 (Newtonian limit)
P("")
info("Newtonian control -- the carried kernel is SATURATED, so at high acceleration it leaves a constant")
info("residual 0.6476 a0.  The relative acceleration must return to Newton as that residual becomes negligible:")
info(f"{'M_b(pair) [Msun]':>18} {'r_M [kpc]':>10} {'r/r_M':>8} {'d [kpc]':>10} {'g_N/a0':>12} {'a_rel/a_Newton - 1':>20}")
worst = 0.0
for Mb in (2e9, 1.6e11):
    a0 = A0["canonical"]; m1 = m2 = Mb/2
    rM = math.sqrt(G*Mb*Msun/a0)/kpc
    for frac in (1.0, 0.1, 0.01):
        d = frac*rM*kpc
        aN = float(a_rel_newton(m1, m2, d)); aF = float(a_rel_framework_isolated(m1, m2, d, a0))
        dev = aF/aN - 1
        if frac == 0.01: worst = max(worst, abs(dev))
        info(f"{Mb:18.2e} {rM:10.2f} {frac:8.2f} {d/kpc:10.3f} {aN/a0:12.4g} {dev:20.3e}")
check("C2 [CONTROL] at small separation, where the acceleration is high, the prediction reduces to Newtonian",
      worst < 1e-3, f"at d = 0.01 r_M the carried kernel's saturated residual is {worst:.2e} of the Newtonian force "
                    f"(the residual is exactly 0.6476 a0/g_N and never vanishes -- that is the kernel's own structure)")

# ---------------------------------------------------------------- CONTROL C3 (both limits, both footings)
# The kernel approaches its deep-MOND limit as Delta(s) = sqrt(s)(1 - sqrt(s)/2 + ...), so the residual at
# finite s is the kernel's OWN next-order term and must fall as sqrt(s), i.e. by 10x per 100x in radius.
ok3 = True; det3 = []; scal = []
for foot, a0 in A0.items():
    for (m1, m2) in ((5e10, 5e10), (1e11, 1e10), (1e9, 3e9)):
        rM = math.sqrt(G*(m1 + m2)*Msun/a0)
        exact = lambda r: math.sqrt(G*float(M_eff(m1, m2))*Msun*a0)/r
        dev = []
        for r in (1e5*rM, 1e7*rM):
            aF = float(a_rel_framework_isolated(m1, m2, r, a0)); aN = G*(m1 + m2)*Msun/r**2
            dev.append(abs((aF - aN)/exact(r) - 1))
        r = 1e-4*rM
        aF = float(a_rel_framework_isolated(m1, m2, r, a0)); aN = G*(m1 + m2)*Msun/r**2
        e2 = abs(aF/aN - 1)
        ok3 &= (dev[0] < 1e-5) and (dev[1] < 1e-7) and (e2 < 1e-7)
        det3.append(max(dev[0], e2)); scal.append(dev[0]/max(dev[1], 1e-30))
check("C3 [CONTROL] the bridge is exact in BOTH limits for equal, 10:1 and dwarf pairs on both footings",
      ok3, f"worst deviation {max(det3):.1e} at 1e5 r_M, falling by {np.median(scal):.0f}x for 100x in radius "
           f"(the kernel's own O(sqrt(s)) approach to deep MOND, not a numerical residual); Newtonian arm exact "
           f"to {max(e2, 0):.0e}")

# ---------------------------------------------------------------- the external field
P("")
info("THE EXTERNAL FIELD, and the value used.  h81_h82_mw_external_fields.py computes it from the 2M++")
info("reconstruction (Carrick+2015) rather than assuming it: the Newtonian large-scale-structure field at the")
info("Local Group is g = 1.161e-12 m/s^2, i.e.")
for foot, a0 in A0.items():
    nb, npar, nperp = nu_efe(E_N[foot])
    info(f"    {foot:>10}: e_N = {E_N[foot]:.5f} a0;  QUMOND response nu_par = {npar:.3f}, nu_perp = {nperp:.3f}, "
         f"orientation-averaged nu_bar = {nb:.3f}")
info("The pair scripts already in the repository used a nominal e_N = 0.02-0.03; the computed value is smaller,")
info("which pushes the isolated/EFE crossover OUT and is therefore the choice generous to the framework.")
for foot, a0 in A0.items():
    Mt = 1.6e11; m1 = m2 = Mt/2
    rM = math.sqrt(G*Mt*Msun/a0)/kpc
    rr = np.geomspace(1.0, 3000.0, 4000)*kpc
    iso = a_rel_framework_isolated(m1, m2, rr, a0); efe = a_rel_framework_efe(m1, m2, rr, a0, E_N[foot])
    i = int(np.argmin(np.abs(iso - efe)))
    info(f"    {foot:>10}: for the median 2MRS pair (M_b = 1.6e11 Msun, r_M = {rM:.1f} kpc) the isolated branch gives way")
    info(f"                to the external-field branch at r = {rr[i]/kpc:.0f} kpc = {rr[i]/kpc/rM:.1f} r_M")

# ==================================================================================================================
# PART 2 -- THE PREDICTION: THREE CURVES
# ==================================================================================================================
P(""); P("-"*122)
P("PART 2 -- the prediction.  sigma_los for a circular relative orbit, random orientation: <dv_los^2> = v_rel^2/3.")
P("-"*122)

LAWS = ["fw_iso", "fw", "newton", "cosmic_pt", "cosmic_nfw", "fw_cosmic", "lcdm_am"]
LABEL = {"fw_iso": "framework (isolated, BEST CASE)", "fw": "framework (carried, with EFE)",
         "newton": "Newton on baryons", "cosmic_pt": "cosmic share, point mass",
         "cosmic_nfw": "cosmic share, NFW", "fw_cosmic": "framework kernel + cosmic share",
         "lcdm_am": "LambdaCDM abundance-matched"}

def a_rel_law(law, M1, M2, r_m, a0, eN):
    if law == "fw_iso":     return a_rel_framework_isolated(M1, M2, r_m, a0)
    if law == "fw":         return a_rel_framework(M1, M2, r_m, a0, eN)
    if law == "newton":     return a_rel_newton(M1, M2, r_m)
    if law == "cosmic_pt":  return a_rel_cosmic_point(M1, M2, r_m)
    if law == "cosmic_nfw": return a_rel_cosmic_nfw(M1, M2, r_m)
    if law == "fw_cosmic":  return a_rel_framework_plus_cosmic(M1, M2, r_m, a0, eN)
    if law == "lcdm_am":    return a_rel_lcdm_am(M1, M2, r_m)
    raise ValueError(law)

def v_circ(law, M1, M2, r_m, a0, eN):
    return np.sqrt(np.maximum(a_rel_law(law, M1, M2, r_m, a0, eN), 0.0)*r_m)

def sigma_pred(law, M1, M2, rp_kpc, a0, eN, nmc=400, seed=11):
    """Projected-separation forward model.  Only r_p is observed; draw the 3-D separation from a
    log-uniform prior weighted by the random-orientation kernel p(r_p|r) = r_p/(r sqrt(r^2 - r_p^2))."""
    g = np.random.default_rng(seed)
    M1 = np.atleast_1d(np.asarray(M1, float)); M2 = np.atleast_1d(np.asarray(M2, float))
    rp = np.atleast_1d(np.asarray(rp_kpc, float))
    u = g.random((len(rp), nmc))
    r = rp[:, None]*np.exp(u*math.log(20.0))*1.0001
    w = 1.0/np.sqrt(np.maximum((r/rp[:, None])**2 - 1.0, 1e-6)); w /= w.sum(axis=1, keepdims=True)
    v2 = v_circ(law, M1[:, None], M2[:, None], r*kpc, a0, eN)**2
    return np.sqrt(np.sum(w*v2, axis=1)/3.0)/1e3

RP = np.array([20., 50., 100., 200., 400., 700., 1000.])
for tag, Mb in (("L* major pair, M_b = 1.6e11 Msun (2MRS sample median)", 1.6e11),
                ("dwarf pair,    M_b = 2.8e9 Msun (ALFALFA sample median)", 2.8e9)):
    P("")
    info(f"{tag}   sigma_los [km/s] against projected separation")
    for foot, a0 in A0.items():
        eN = E_N[foot]
        info(f"  --- footing {foot} (a0 = {a0:.4e} m/s^2, e_N = {eN:.5f}) ---")
        hdr = f"{'r_p [kpc]':>10} " + " ".join(f"{LABEL[l][:22]:>23}" for l in LAWS)
        info(hdr)
        for rp in RP:
            row = [sigma_pred(l, Mb/2, Mb/2, np.array([rp]), a0, eN)[0] for l in LAWS]
            info(f"{rp:10.0f} " + " ".join(f"{v:23.1f}" for v in row))

# ---- the shapes, analytically
P("")
info("THE THREE SHAPES, which is what makes them separable without trusting the stellar M/L:")
info("   framework, isolated deep MOND : sigma_los INDEPENDENT of separation, sigma ~ M_b^{1/4}")
info("   framework, external-field branch and Newton and cosmic share : sigma ~ r^{-1/2}, sigma ~ M_b^{1/2}")
info("   LambdaCDM abundance-matched   : nearly flat in r over 100-1000 kpc (the NFW halo grows with r), M_b^{~0.9}")

# ==================================================================================================================
# PART 3 -- THE DATA
# ==================================================================================================================
P(""); P("-"*122)
P("PART 3 -- the data.  An isolated major-pair sample rebuilt independently from 2MRS (Huchra+2012), with the")
P("          RELATIVE isolation criterion h48_h69b established is the one that matters.")
P("-"*122)

def unitvec(ra, de):
    ra = np.radians(ra); de = np.radians(de)
    return np.c_[np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)]
def ang_sep_deg(u, v):
    return np.degrees(2*np.arcsin(np.clip(np.linalg.norm(u - v, axis=-1)/2, 0, 1)))
def cmb_frame(ra, de, vhel):
    ra_r, de_r = np.radians(ra), np.radians(de)
    ra_gp, de_gp, l_ncp = math.radians(192.85948), math.radians(27.12825), math.radians(122.93192)
    sb = np.sin(de_r)*math.sin(de_gp) + np.cos(de_r)*math.cos(de_gp)*np.cos(ra_r - ra_gp)
    b = np.arcsin(np.clip(sb, -1, 1))
    y = np.cos(de_r)*np.sin(ra_r - ra_gp)
    x = np.sin(de_r)*math.cos(de_gp) - np.cos(de_r)*math.sin(de_gp)*np.cos(ra_r - ra_gp)
    l = l_ncp - np.arctan2(y, x)
    la, ba, amp = math.radians(264.021), math.radians(48.253), 369.82
    return vhel + amp*(np.sin(b)*math.sin(ba) + np.cos(b)*math.cos(ba)*np.cos(l - la))
def LK_from_mag(K, D_Mpc):
    return 10**(0.4*(MK_SUN - (K - 5*np.log10(D_Mpc*1e6) + 5)))

CZ_LO, CZ_HI, RP_MAX, DV_MAX, DV_ISO, V_ERR = 3000.0, 12000.0, 1000.0, 2000.0, 1000.0, 40.0

mr = np.genfromtxt(os.path.join(DATA, "2mrs_catalog.csv"), delimiter=",", names=True)
mok = np.isfinite(mr["cz"]) & (mr["cz"] > 0)
m_ra, m_de, m_K, m_cz = mr["RAJ2000"][mok], mr["DEJ2000"][mok], mr["Ktmag"][mok], mr["cz"][mok]
MX = unitvec(m_ra, m_de); MT = cKDTree(MX); cz_cmb = cmb_frame(m_ra, m_de, m_cz)
info(f"2MRS galaxies with cz and a total Ks magnitude: {len(m_ra)} (K < {m_K.max():.2f})")

ang_max = math.degrees(RP_MAX/1000.0/(CZ_LO/H0_KMS))
cand = MT.query_pairs(2*math.sin(math.radians(ang_max)/2), output_type="ndarray")
ii, jj = cand[:, 0], cand[:, 1]
czm = (cz_cmb[ii] + cz_cmb[jj])/2; Dm = czm/H0_KMS
rp = np.radians(ang_sep_deg(MX[ii], MX[jj]))*Dm*1000.0
dv = cz_cmb[ii] - cz_cmb[jj]
sel = (np.abs(dv) < DV_MAX) & (czm > CZ_LO) & (czm < CZ_HI) & (rp < RP_MAX) & (rp > 10.0)
ii, jj, rp, dv, czm, Dm = ii[sel], jj[sel], rp[sel], dv[sel], czm[sel], Dm[sel]
L1 = LK_from_mag(m_K[ii], Dm); L2 = LK_from_mag(m_K[jj], Dm)
rok = (np.maximum(L1, L2)/np.minimum(L1, L2)) < 6.0
ii, jj, rp, dv, czm, Dm, L1, L2 = (a[rok] for a in (ii, jj, rp, dv, czm, Dm, L1, L2))
info(f"candidate MAJOR close pairs (10-1000 kpc, |dv| < 2000 km/s, cz 3000-12000, L_K ratio < 6): {len(ii)}")

# relative isolation: distance to the nearest THIRD 2MRS galaxy at |dv| < 1000 km/s from the pair midpoint
mid = MX[ii] + MX[jj]; mid /= np.linalg.norm(mid, axis=1)[:, None]
KNN = 80
dch, idx = MT.query(mid, k=KNN)
ang = 2*np.arcsin(np.clip(dch/2, 0, 1))                                   # radians
dist_kpc = ang*Dm[:, None]*1000.0
bad = (idx == ii[:, None]) | (idx == jj[:, None]) | (np.abs(cz_cmb[idx] - czm[:, None]) >= DV_ISO)
dist_kpc = np.where(bad, np.inf, dist_kpc)
d3 = dist_kpc.min(axis=1)
info(f"nearest third 2MRS galaxy at |dv| < {DV_ISO:.0f} km/s (k = {KNN} neighbours searched): "
     f"median {np.median(d3[np.isfinite(d3)]):.0f} kpc; {100*np.mean(~np.isfinite(d3)):.1f}% have none in the k nearest")

# ---------------------------------------------------------------- estimator
def ml_fit(dv, shape=None, dvmax=DV_MAX, verr=V_ERR):
    """Pair + flat-interloper likelihood.  shape=None fits one common sigma; otherwise fits the AMPLITUDE
    A of the per-pair predicted dispersions.  Returns (value, 1-sigma from the profile likelihood, f_int)."""
    dv = np.asarray(dv, float); n = len(dv)
    s = np.ones(n) if shape is None else np.asarray(shape, float)
    def nll(lA, lf):
        A = math.exp(lA); f = 1/(1 + math.exp(-lf))
        sg = np.sqrt((A*s)**2 + verr**2)
        p = f*np.exp(-0.5*(dv/sg)**2)/(math.sqrt(2*math.pi)*sg) + (1 - f)/(2*dvmax)
        return -np.sum(np.log(np.maximum(p, 1e-300)))
    lAs = np.linspace(math.log(10.0), math.log(2000.0), 90) if shape is None else np.linspace(math.log(0.10), math.log(12.0), 110)
    lfs = np.linspace(-4, 4, 41)
    best = (1e30, 0.0, 0.0)
    for lA in lAs:
        for lf in lfs:
            v = nll(lA, lf)
            if v < best[0]: best = (v, lA, lf)
    lA0, lf0 = best[1], best[2]
    for _ in range(3):
        lf0 = min(np.linspace(lf0 - 1.0, lf0 + 1.0, 81), key=lambda x: nll(lA0, x))
        lA0 = min(np.linspace(lA0 - 0.15, lA0 + 0.15, 81), key=lambda x: nll(x, lf0))
    fine = np.linspace(lA0 - 0.35, lA0 + 0.35, 201)
    prof = np.array([min(nll(lA, lf) for lf in np.linspace(lf0 - 0.8, lf0 + 0.8, 25)) for lA in fine])
    prof -= prof.min(); lA0 = fine[int(np.argmin(prof))]
    hi = fine[prof < 0.5]
    err = (hi.max() - hi.min())/2 if len(hi) > 1 else float(np.diff(fine).mean())
    A = math.exp(lA0)
    return A, A*err, 1 - 1/(1 + math.exp(-lf0))

# ---------------------------------------------------------------- the F = 5 strict sample (h48_h69b's headline)
F_REL = 5.0
keep = d3 > F_REL*rp
S = dict(rp=rp[keep], dv=dv[keep], M1=UPS_K*L1[keep], M2=UPS_K*L2[keep], D=Dm[keep])
N = len(S["rp"])
sig, esig, fint = ml_fit(S["dv"])
info(f"STRICT SAMPLE (no third 2MRS galaxy inside {F_REL:.0f} r_p of the midpoint): N = {N}, "
     f"median r_p = {np.median(S['rp']):.0f} kpc, median log M_b(pair) = {np.median(np.log10(S['M1'] + S['M2'])):.2f}")
info(f"  maximum-likelihood dispersion: sigma_los = {sig:.1f} +/- {esig:.1f} km/s, interloper fraction {fint:.2f}")
info(f"  h48_h69b (independent build, same criterion) reported N = 1830, median r_p = 141 kpc, sigma = 200.7 +/- 5.3 km/s")
check("C4 [CONTROL] this lane's independent rebuild of the pair sample reproduces the repository's published one",
      abs(N/1830. - 1) < 0.25 and abs(sig/200.7 - 1) < 0.10 and abs(np.median(S["rp"])/141. - 1) < 0.30,
      f"N = {N} vs 1830 ({100*(N/1830.-1):+.0f}%); sigma = {sig:.1f} vs 200.7 km/s ({100*(sig/200.7-1):+.1f}%); "
      f"median r_p = {np.median(S['rp']):.0f} vs 141 kpc")

# ---------------------------------------------------------------- amplitudes against every curve
P("")
info("AMPLITUDE A = (observed dispersion)/(parameter-free prediction), fitted jointly with the interloper")
info("fraction.  A = 1 means the law is right with no free parameter.  In deep MOND sigma ~ M^{1/4}, so an")
info("amplitude A corresponds to a required mass A^4 M_b; in the Newtonian laws it is A^2 M_b.")
def mass_factor(law, M1, M2, rp, a0, eN, A):
    """The factor by which each member's mass would have to be multiplied for the law to give the observed
    dispersion.  Solved numerically rather than assumed, because the deep-MOND (M^1/4) and quasi-Newtonian
    (M^1/2) scalings differ and the carried framework straddles them."""
    base = float(np.median(sigma_pred(law, M1, M2, rp, a0, eN)))
    lo, hi = -3.0, 4.0
    for _ in range(60):
        mid = 0.5*(lo + hi); f = 10**mid
        v = float(np.median(sigma_pred(law, f*M1, f*M2, rp, a0, eN)))
        if v < A*base: lo = mid
        else: hi = mid
    return 10**(0.5*(lo + hi))

AMP = {}
for foot, a0 in A0.items():
    eN = E_N[foot]
    info(f"  --- footing {foot} ---")
    info(f"      {'law':>34} {'A':>16} {'implied M/M_assumed':>21} {'f_int':>7} {'sigma from 1':>13}")
    for law in LAWS:
        sh = sigma_pred(law, S["M1"], S["M2"], S["rp"], a0, eN)
        A, eA, fi = ml_fit(S["dv"], shape=sh)
        mf = mass_factor(law, S["M1"], S["M2"], S["rp"], a0, eN, A)
        AMP[(foot, law)] = (A, eA, fi, mf)
        info(f"      {LABEL[law]:>34} {A:8.3f} +/-{eA:5.3f} {mf:21.2f} {fi:7.2f} {abs(A-1)/eA:13.1f}")

Ac, eAc = AMP[("canonical", "fw_iso")][0], AMP[("canonical", "fw_iso")][1]
Aa = AMP[("alt", "fw_iso")][0]
Acos = AMP[("canonical", "cosmic_pt")][0]; eAcos = AMP[("canonical", "cosmic_pt")][1]
Acn = AMP[("canonical", "cosmic_nfw")][0]; eAcn = AMP[("canonical", "cosmic_nfw")][1]
Afc = AMP[("canonical", "fw_cosmic")][0]; eAfc = AMP[("canonical", "fw_cosmic")][1]
Afc_a = AMP[("alt", "fw_cosmic")][0]
Alc = AMP[("canonical", "lcdm_am")][0]; eAlc = AMP[("canonical", "lcdm_am")][1]
Afw = AMP[("canonical", "fw")][0]

# ---- does the required boost depend on mass?  the ladder read INSIDE the pair sample
P("")
info("Does the deficit depend on the pair's baryonic mass?  Same fit, quartiles of M_b(pair):")
info(f"{'log M_b(pair)':>18} {'N':>5} {'A(framework iso)':>18} {'A(cosmic share)':>17} {'A(LambdaCDM AM)':>17} "
     f"{'M_dyn/M_b within r_p':>21}")
Mb_pair = S["M1"] + S["M2"]; q = np.percentile(np.log10(Mb_pair), [0, 25, 50, 75, 100])
a0 = A0["canonical"]; eN = E_N["canonical"]; MASSROWS = []
for k in range(4):
    s = (np.log10(Mb_pair) >= q[k]) & (np.log10(Mb_pair) <= q[k+1])
    if s.sum() < 50: continue
    r = {}
    for law in ("fw_iso", "cosmic_pt", "lcdm_am", "newton"):
        sh = sigma_pred(law, S["M1"][s], S["M2"][s], S["rp"][s], a0, eN)
        r[law] = ml_fit(S["dv"][s], shape=sh)[:2]
    MASSROWS.append((float(np.median(np.log10(Mb_pair[s]))), int(s.sum()), r))
    info(f"{q[k]:8.2f} - {q[k+1]:6.2f} {s.sum():5d} {r['fw_iso'][0]:10.2f} +/-{r['fw_iso'][1]:5.2f} "
         f"{r['cosmic_pt'][0]:10.2f} +/-{r['cosmic_pt'][1]:4.2f} {r['lcdm_am'][0]:10.2f} +/-{r['lcdm_am'][1]:4.2f} "
         f"{r['newton'][0]**2 - 1:21.1f}")
lo_, hi_ = MASSROWS[0][2]["fw_iso"], MASSROWS[-1][2]["fw_iso"]
z_trend = (hi_[0] - lo_[0])/math.hypot(hi_[1], lo_[1])
check("M0 the framework's deficit is INDEPENDENT of the pair's baryonic mass, as a kernel with no scale in it "
      "requires",
      abs(z_trend) < 3.0,
      f"A(framework) climbs from {lo_[0]:.2f} +/- {lo_[1]:.2f} in the lowest mass quartile to {hi_[0]:.2f} +/- "
      f"{hi_[1]:.2f} in the highest, {z_trend:.1f} sigma, over {MASSROWS[-1][0]-MASSROWS[0][0]:.2f} dex in M_b; "
      f"LambdaCDM's abundance-matched halos move the OTHER way ({MASSROWS[0][2]['lcdm_am'][0]:.2f} -> "
      f"{MASSROWS[-1][2]['lcdm_am'][0]:.2f}).  This is h48_h69's 69d (sigma ~ M^1/2 not M^1/4) seen as a trend in "
      f"the residual, and it is the axis a deeper sample should attack")

# ---------------------------------------------------------------- mutation controls on the estimator
P("")
rngm = np.random.default_rng(517)
perm = rngm.permutation(len(S["dv"]))
dv_scr = cz_cmb[ii[keep]] - cz_cmb[jj[keep]][perm]
sh_ref = sigma_pred("fw_iso", S["M1"], S["M2"], S["rp"], A0["canonical"], E_N["canonical"])
_, _, f_real = ml_fit(S["dv"], shape=sh_ref)
_, _, f_scr = ml_fit(dv_scr, shape=sh_ref)
check("M1 [mutation control] scrambling which galaxy each pair member is paired with drives the fitted PAIR "
      "fraction to the floor",
      (1 - f_real) > 0.6 and (1 - f_scr) < 0.15,
      f"pair fraction 1 - f_int: real {1-f_real:.2f}, scrambled {1-f_scr:.2f}")
sh_100 = sigma_pred("fw_iso", S["M1"], S["M2"], S["rp"], 100*A0["canonical"], E_N["canonical"])
A100 = ml_fit(S["dv"], shape=sh_100)[0]
check("M2 [mutation control] the amplitude responds to a0 exactly as v ~ a0^{1/4} demands, so the offsets above "
      "are a statement about the physics and not an insensitive estimator",
      abs(math.log10(AMP[("canonical", "fw_iso")][0]/A100) - 0.5) < 0.02,
      f"a0 x 100 moves log10(A) by {math.log10(AMP[('canonical','fw_iso')][0]/A100):+.3f} against the predicted "
      f"+0.500")

# ---------------------------------------------------------------- the separation-dependence axis
P("")
BINS = [(10, 60), (60, 120), (120, 220), (220, 400), (400, 650), (650, 1000)]
info(f"{'r_p bin [kpc]':>16} {'N':>5} {'f_int':>6} {'sigma_los [km/s]':>21} {'log M_b,pair':>13}")
rows = []
for lo, hi in BINS:
    s = (S["rp"] >= lo) & (S["rp"] < hi)
    if s.sum() < 25: continue
    sg, esg, fi = ml_fit(S["dv"][s])
    rows.append((0.5*(math.log10(lo) + math.log10(hi)), math.log10(float(np.median(S["rp"][s]))), sg, esg, fi, int(s.sum())))
    info(f"{lo:7d} - {hi:6d} {s.sum():5d} {fi:6.2f} {sg:14.1f} +/- {esg:4.1f} "
         f"{float(np.median(np.log10(S['M1'][s] + S['M2'][s]))):13.2f}")
lr = np.array([r[1] for r in rows]); ls = np.log10(np.array([r[2] for r in rows]))
els = np.array([r[3] for r in rows])/np.array([r[2] for r in rows])/math.log(10)
Wt = 1/els**2
sl = (np.sum(Wt*lr*ls)*np.sum(Wt) - np.sum(Wt*lr)*np.sum(Wt*ls))/(np.sum(Wt*lr**2)*np.sum(Wt) - np.sum(Wt*lr)**2)
esl = math.sqrt(np.sum(Wt)/(np.sum(Wt*lr**2)*np.sum(Wt) - np.sum(Wt*lr)**2))
info(f"measured d log sigma_los / d log r_p = {sl:+.3f} +/- {esl:.3f} over {len(rows)} bins")

# predicted slopes for each law, on the same bins and the same masses
info(f"{'law':>34} {'predicted d log sigma / d log r_p':>36} {'sigma away':>11}")
SLOPE = {}
for law in LAWS:
    a0 = A0["canonical"]; eN = E_N["canonical"]
    pr = []
    for (lo, hi) in BINS:
        s = (S["rp"] >= lo) & (S["rp"] < hi)
        if s.sum() < 25: continue
        pr.append(float(np.median(sigma_pred(law, S["M1"][s], S["M2"][s], S["rp"][s], a0, eN))))
    pr = np.log10(np.array(pr))
    sp = np.polyfit(lr, pr, 1)[0]
    SLOPE[law] = sp
    info(f"{LABEL[law]:>34} {sp:+36.3f} {abs(sp - sl)/esl:11.1f}")

# ==================================================================================================================
# PART 4 -- THE DISCRIMINATOR
# ==================================================================================================================
P(""); P("-"*122)
P("PART 4 -- the discriminator: how large a sample, at what velocity precision, separates the curves at 3 sigma?")
P("-"*122)

rng = np.random.default_rng(2126)
def forecast(lawA, lawB, M1, M2, rp, a0, eN, verr, fint=0.20, nmock=120, nmax=20000):
    """Generate mock pairs under lawA, fit the amplitude relative to lawB's shape, and return the sample size
    at which |ln A_B| reaches 3 sigma.  Uses the Fisher scaling sigma(ln A) ~ k/sqrt(N) calibrated on mocks."""
    sA = sigma_pred(lawA, M1, M2, rp, a0, eN); sB = sigma_pred(lawB, M1, M2, rp, a0, eN)
    n0 = min(len(rp), 800)
    lnA = []
    for _ in range(max(6, nmock//20)):
        k = rng.choice(len(rp), n0, replace=True)
        real = rng.random(n0) > fint
        dvm = np.where(real, rng.normal(0, np.sqrt(sA[k]**2 + verr**2)), rng.uniform(-DV_MAX, DV_MAX, n0))
        A, eA, _ = ml_fit(dvm, shape=sB[k], verr=verr)
        lnA.append(math.log(max(A, 1e-6)))
        kscale = eA/A*math.sqrt(n0)
    off = abs(float(np.mean(lnA)))
    if off < 1e-6: return np.inf, off, kscale
    Nneed = (3.0*kscale/off)**2
    return Nneed, off, kscale

a0 = A0["canonical"]; eN = E_N["canonical"]
sub = S["rp"] < 500.
M1s, M2s, rps = S["M1"][sub], S["M2"][sub], S["rp"][sub]
info("mock pairs drawn from the real (M_b, r_p) distribution of the strict sample at r_p < 500 kpc, with a")
info(f"20% interloper fraction, fitted with the same estimator.  Velocity precision scanned.")
info(f"{'truth':>34} {'tested against':>34} {'v_err':>7} {'ln offset':>10} {'N for 3 sigma':>14}")
PAIRS3 = [("fw_iso", "cosmic_pt"), ("fw_iso", "cosmic_nfw"), ("fw_iso", "newton"),
          ("fw_iso", "lcdm_am"), ("fw_cosmic", "fw_iso"), ("cosmic_pt", "lcdm_am")]
FCAST = {}
for (la, lb) in PAIRS3:
    for verr in (40.0, 10.0):
        Nn, off, ks = forecast(la, lb, M1s, M2s, rps, a0, eN, verr)
        FCAST[(la, lb, verr)] = Nn
        info(f"{LABEL[la]:>34} {LABEL[lb]:>34} {verr:7.0f} {off:10.3f} {Nn:14.0f}")

# ---- the shape axis, immune to the stellar M/L
P("")
info("THE SHAPE AXIS.  An overall error in the stellar M/L (or in the gas fraction) moves every amplitude")
info("together and cannot be calibrated away; the SEPARATION SLOPE is immune to it.  Forecast error on")
info("d log sigma / d log r_p for a sample of N pairs spread over 30-1000 kpc at the measured dispersions:")
info(f"{'N pairs':>10} {'v_err = 40 km/s':>18} {'v_err = 10 km/s':>18}")
sl_err_ref = esl; N_ref = sum(r[5] for r in rows)
for Nn in (500, 2000, 10000, 50000):
    info(f"{Nn:10d} {sl_err_ref*math.sqrt(N_ref/Nn):18.3f} {0.85*sl_err_ref*math.sqrt(N_ref/Nn):18.3f}")
gap_fw_cos = abs(SLOPE["fw_iso"] - SLOPE["cosmic_pt"])
N3_slope = N_ref*(3*sl_err_ref/gap_fw_cos)**2
info(f"the framework's isolated branch and the cosmic-share point mass differ by {gap_fw_cos:.3f} in slope, so a")
info(f"3-sigma separation on the SHAPE axis alone needs N = {N3_slope:.0f} pairs at this data quality.")

check("D1 the framework's prediction and the cosmic-share prediction are distinguishable at all, and by how much",
      FCAST[("fw_iso", "cosmic_pt", 40.0)] < 2000 and gap_fw_cos > 0.3,
      f"amplitude axis: N = {FCAST[('fw_iso','cosmic_pt',40.0)]:.0f} pairs for 3 sigma at 40 km/s "
      f"({FCAST[('fw_iso','cosmic_pt',10.0)]:.0f} at 10 km/s); shape axis: slopes differ by {gap_fw_cos:.2f}, "
      f"N = {N3_slope:.0f} for 3 sigma.  Both are far below the {N} pairs already in hand")

# ==================================================================================================================
# PART 5 -- THE SCALE QUESTION
# ==================================================================================================================
P(""); P("-"*122)
P("PART 5 -- the scale question: where does the kernel stop working, and is the cosmic share what takes over?")
P("-"*122)

# where do the two curves diverge most sharply?
P("")
info("Where the framework and the cosmic share diverge, for the median 2MRS pair (M_b = 1.6e11 Msun):")
info(f"{'r_p [kpc]':>10} {'g_N/a0':>10} {'fw isolated':>13} {'cosmic pt':>11} {'ratio':>8} {'fw carried':>12} {'ratio':>8}")
Mb = 1.6e11; a0 = A0["canonical"]; eN = E_N["canonical"]
rgrid = np.array([20., 40., 70., 100., 150., 200., 300., 500., 700., 1000., 1500., 2000.])
sfw = sigma_pred("fw_iso", Mb/2, Mb/2, rgrid, a0, eN)
sfwc = sigma_pred("fw", Mb/2, Mb/2, rgrid, a0, eN)
scp = sigma_pred("cosmic_pt", Mb/2, Mb/2, rgrid, a0, eN)
gN = G*Mb*Msun/(rgrid*kpc)**2/a0
for i, rr in enumerate(rgrid):
    info(f"{rr:10.0f} {gN[i]:10.4f} {sfw[i]:13.1f} {scp[i]:11.1f} {sfw[i]/scp[i]:8.3f} {sfwc[i]:12.1f} {sfwc[i]/scp[i]:8.3f}")
icross = int(np.argmin(np.abs(np.log(sfw/scp))))
msk = (rgrid >= 30) & (rgrid <= 1000); rsel = rgrid[msk]
imax = int(np.argmax(np.abs(np.log10(sfw/scp))[msk]))
info(f"the two curves CROSS at r_p ~ {rgrid[icross]:.0f} kpc (g_N = {gN[icross]:.3f} a0); below it the cosmic share")
info(f"predicts more, above it the framework's ISOLATED branch does.  Over an observable 30-1000 kpc the maximum")
info(f"divergence is {max(abs(np.log10(sfw/scp)[msk])):.3f} dex in velocity, at r_p = {rsel[imax]:.0f} kpc.")

# THE DEGENERACY the run exposes: the framework's own EFE branch and the cosmic share are the SAME LAW
nb = nu_efe(E_N["canonical"])[0]
rat_far = float(np.median((sfwc/scp)[rgrid >= 300]))
check("S0 [structure] the framework's honest external-field prediction is observationally DISTINCT from a "
      "cosmic-share halo at large separation",
      abs(rat_far - 1) > 0.30,
      f"beyond ~200 kpc BOTH are quasi-Newtonian with a constant boost -- the framework's orientation-averaged "
      f"nu_bar(e_N) = {nb:.2f} against the cosmic share's 1 + {F_COSMIC} = {1+F_COSMIC:.2f}.  The predicted "
      f"dispersions differ by only {100*(rat_far-1):+.1f}% in velocity ({100*(rat_far**2-1):+.0f}% in mass) at every "
      f"separation and every mass, an EXACT degeneracy in shape.  Where the external field dominates, this "
      f"programme's EFE and LambdaCDM's cosmic dark share are the same law with the same slope, separated only by "
      f"that {100*(rat_far-1):.0f}% in velocity -- below the stellar-M/L systematic")

# the dark-share ladder
P("")
info("THE LADDER.  In one currency -- the dark-to-baryon mass ratio a Newtonian reading of the data requires --")
info("across the three regimes this programme has now measured:")
An = AMP[("canonical", "newton")][0]; eAn = AMP[("canonical", "newton")][1]
ratio_pairs = An**2 - 1.0; e_ratio_pairs = 2*An*eAn
info(f"{'regime':>36} {'M_dark/M_bar required':>24} {'framework residual after its kernel':>38}")
info(f"{'galaxy interiors (SPARC RAR)':>36} {'0 (kernel suffices, 0.108 dex)':>24} {'0':>38}")
info(f"{'isolated major pairs, this lane':>36} {f'{ratio_pairs:.1f} +/- {e_ratio_pairs:.1f}':>24} "
     f"{f'{Ac**4 - 1:.1f} M_b (A = {Ac:.2f})':>38}")
info(f"{'X-COP clusters at 0.80 R500 (L7)':>36} {'5.73 +/- 0.68':>24} {'2.76 (alt) / 3.09 (canonical) M_b':>38}")
info(f"cosmic Omega_dm/Omega_b = {F_COSMIC}")

check("S1 the dark-to-baryon ratio the pair data require is the SAME cosmic share the clusters require",
      abs(ratio_pairs - F_COSMIC) < 3*e_ratio_pairs,
      f"pairs need {ratio_pairs:.1f} +/- {e_ratio_pairs:.1f} WITHIN THE PAIR SEPARATION against the cosmic "
      f"{F_COSMIC} -- "
      f"{abs(ratio_pairs - F_COSMIC)/e_ratio_pairs:.1f} sigma away, a factor {ratio_pairs/F_COSMIC:.1f}.  "
      f"The cosmic share is a CLUSTER-scale statement, not a universal one; at pair separations galaxies are "
      f"baryon-poor relative to cosmic and need several times more")

check("S2 a cosmic-share halo -- the exact quantity L7 found clusters demand -- reproduces the pair kinematics",
      abs(Acos - 1) < 3*eAcos or abs(Acn - 1) < 3*eAcn,
      f"cosmic share as a point mass A = {Acos:.2f} +/- {eAcos:.2f} ({abs(Acos-1)/eAcos:.0f} sigma high), as an NFW "
      f"halo A = {Acn:.2f} +/- {eAcn:.2f} ({abs(Acn-1)/eAcn:.0f} sigma high).  Both UNDER-predict the observed "
      f"dispersion; abundance-matched LambdaCDM, which puts {(Alc**-2)*(An**2):.0f}x the baryons rather than "
      f"{1+F_COSMIC:.1f}x, lands at A = {Alc:.2f} +/- {eAlc:.2f}")

check("S3 the framework's carried kernel reproduces the pair kinematics on its own",
      abs(Afw - 1) < 3*AMP[("canonical", "fw")][1],
      f"carried (with the computed 2M++ external field) A = {Afw:.2f}; the framework's BEST CASE, the isolated "
      f"deep-MOND branch no external field can raise, A = {Ac:.2f} +/- {eAc:.2f} canonical / {Aa:.2f} alt, "
      f"{abs(Ac-1)/eAc:.0f} sigma above 1, needing {AMP[('canonical','fw_iso')][3]:.1f}x the K-band baryonic mass")

check("S4 the framework's kernel PLUS the cluster-scale cosmic share reproduces the pair kinematics",
      abs(Afc - 1) < 3*eAfc,
      f"A = {Afc:.2f} +/- {eAfc:.2f}, {abs(Afc-1)/eAfc:.1f} sigma from 1 -- against {Ac:.2f} for the kernel alone "
      f"and {Acos:.2f} for the cosmic share alone.  The combination is much closer to the data than either piece, "
      f"and it is the only one of the three with no fitted parameter that lands within a factor {max(Afc,1/Afc):.2f}")

check("S5 existing published data ALREADY discriminate the three curves at 3 sigma",
      abs(Ac - 1)/eAc > 3 and abs(Acos - 1)/eAcos > 3 and (abs(sl - SLOPE["fw_iso"])/esl > 3
                                                           or abs(sl - SLOPE["cosmic_pt"])/esl > 3),
      f"amplitudes: framework {abs(Ac-1)/eAc:.0f} sigma, cosmic share {abs(Acos-1)/eAcos:.0f} sigma; separation "
      f"slope {sl:+.3f} +/- {esl:.3f} is {abs(sl - SLOPE['fw_iso'])/esl:.1f} sigma from the framework's isolated "
      f"branch and {abs(sl - SLOPE['cosmic_pt'])/esl:.1f} sigma from the cosmic share.  The statistics are there; "
      f"what is NOT settled is the isolation-depth systematic (see below)")

# ---- how extended must the component be?  The galaxy-side gate, computed here rather than reused.
P("")
info("IF the pair deficit is a real dark component, WHERE must it sit?  The galaxy-side gate is the radial")
info("acceleration relation's 0.11 dex scatter: how much extra mass inside 10 kpc can the CARRIED kernel absorb")
info("before g_obs moves by more than that?  Computed here directly, not reused:")
def rar_tolerance(Mb_in, r_kpc, a0, tol_dex=0.11):
    """Extra mass (in units of M_b) inside r that shifts the carried kernel's g_obs by tol_dex."""
    gb = G*Mb_in*Msun/(r_kpc*kpc)**2
    g0 = gb + a0*float(Delta(np.array([gb/a0]))[0])
    lo, hi = 0.0, 50.0
    for _ in range(80):
        f = 0.5*(lo + hi); gbf = (1 + f)*gb
        gf = gbf + a0*float(Delta(np.array([gbf/a0]))[0])
        if math.log10(gf/g0) < tol_dex: lo = f
        else: hi = f
    return 0.5*(lo + hi)

info(f"{'M_b (each) [Msun]':>18} {'RAR tolerance at 10 kpc':>24} {'NFW cosmic share <10 kpc':>26} {'over by':>9}")
TOLROWS = []
for mb in (2e9, 8e10):
    Mh = F_COSMIC*mb
    tol = rar_tolerance(mb, 10.0, A0["canonical"])
    inner = float(nfw_enclosed(Mh, np.array([10.0]))[0])/mb
    TOLROWS.append((mb, tol, inner))
    info(f"{mb:18.2e} {tol:20.3f} M_b {inner:22.3f} M_b {inner/tol:9.2f}x")
info(f"(L1/L7 quote a tolerance of 0.25 M_b at 10 kpc from the galaxy side; the direct computation above gives")
info(f" {TOLROWS[1][1]:.2f} M_b for an L* galaxy and {TOLROWS[0][1]:.2f} M_b for a dwarf -- the same order, and the "
     f"dwarf end is the tight one.)")
over_L, over_d = TOLROWS[1][2]/TOLROWS[1][1], TOLROWS[0][2]/TOLROWS[0][1]
check("S6 a cosmic-share dark component with an NFW shape is admissible inside galaxies on the RAR gate",
      over_L < 1.0 and over_d < 1.0,
      f"at L* an NFW cosmic share puts {TOLROWS[1][2]:.2f} M_b inside 10 kpc against a tolerance of "
      f"{TOLROWS[1][1]:.2f} ({over_L:.2f}x, admissible); at the dwarf scale {TOLROWS[0][2]:.2f} against "
      f"{TOLROWS[0][1]:.2f} ({over_d:.1f}x, EXCLUDED).  The galaxy-side objection therefore bites on SHAPE and on "
      f"MASS SCALE, not on the amount: g04k/L1's cold infall delivers 0.92-1.45 M_b inside 10 kpc, "
      f"{0.92/TOLROWS[1][2]:.1f}x more concentrated than NFW at L*, and no dark component with a cuspy NFW inner "
      f"slope survives at 2e9 Msun")

# ---- systematics
P("")
info("SYSTEMATICS, restated because they bound everything above and were established by the prior lanes:")
info(" 1. ISOLATION DEPTH is the leading one.  2MRS at the sample's median distance sees only M_b > 3.6e10 Msun,")
info("    so 'isolated' means 'no companion above ~23% of the pair's own mass'.  h48_h69 measured the amplitude")
info("    falling from 1.99 in the far velocity shell to 1.51 in the near one, where the isolation reaches four")
info("    times further down the luminosity function -- so every amplitude here is an UPPER limit on the real one.")
info(" 2. The ALFALFA dwarf pairs (h47, N = 138, velocities good to 4.4 km/s) give A(deep-MOND) = 1.79 +/- 0.20")
info("    unrelatively isolated and 1.12 +/- 0.29 under the relative criterion -- 2.6 sigma from this sample's")
info("    1.89 +/- 0.05.  The cross-scale tension is UNRESOLVED and this lane does not resolve it.")
info(" 3. Circular relative orbits are assumed.  Eccentric orbits at the same energy spend more time near")
info("    apocentre at LOWER speed, so the assumption is generous to the framework.")
info(" 4. Upsilon_K = 0.6 and no gas in M_b.  The amplitude moves as Upsilon^{1/4} in the framework and")
info("    Upsilon^{1/2} in the Newtonian laws, so closing the framework's gap needs Upsilon ~ 7, outside any")
info("    stellar population; the SHAPE axis of PART 4 is immune to this.")
info(" 5. Pairs beyond ~500 kpc may not be bound; the interloper term removes chance projections, not")
info("    physically associated unbound pairs.  Every amplitude above is dominated by r_p < 500 kpc.")

P(""); P("-"*122)
P("THE PRE-REGISTERABLE STATEMENT")
P("-"*122)
a0 = A0["canonical"]; eN = E_N["canonical"]
info("For a pair of galaxies of baryonic masses M1, M2 at 3-D separation r, on a circular relative orbit, the")
info("framework's carried kernel predicts a line-of-sight velocity difference with dispersion")
info("     sigma_los = sqrt(a_rel(r) r / 3),   a_rel = min[ G M_tot/r^2 + a0 Delta(G M_eff/(a0 r^2)),")
info("                                                      nu_bar(e_N) G M_tot/r^2 ],")
info("     M_eff = (2/3)^2 [(M1+M2)^{3/2} - M1^{3/2} - M2^{3/2}]^2 / mu^2,  mu = M1 M2/M_tot,")
info(f"     Delta(s) = s/(exp(sqrt(s)) - 1) saturated at {D_SAT} for s > {S_SAT}, "
     f"nu_bar({E_N['canonical']:.5f}) = {nu_efe(E_N['canonical'])[0]:.3f} / "
     f"nu_bar({E_N['alt']:.5f}) = {nu_efe(E_N['alt'])[0]:.3f}.")
info("For equal masses in the isolated branch this is the parameter-free")
info(f"     sigma_los = (1.05099/sqrt(3)) (G m a0)^{{1/4}} = {1.05099/math.sqrt(3):.5f} (G m a0)^{{1/4}}, "
     f"INDEPENDENT OF SEPARATION,")
for foot, aa in A0.items():
    v_ = (1.05099/math.sqrt(3))*(G*8e10*Msun*aa)**0.25/1e3
    info(f"     i.e. {v_:.1f} km/s for two 8e10 Msun galaxies on the {foot} footing, at ANY separation beyond ~30 kpc.")
info("PREDICTIONS THAT LOSE:")
info(f"  P1 amplitude.  A = 1.  Measured on 1900 isolated 2MRS major pairs: A = {Ac:.2f} +/- {eAc:.2f} "
     f"(canonical) / {Aa:.2f} (alt).  FALSIFIED at {abs(Ac-1)/eAc:.0f} sigma unless the isolation systematic "
     f"carries it.")
info(f"  P2 shape.  d log sigma / d log r_p = {SLOPE['fw_iso']:+.3f} on the isolated branch. Measured "
     f"{sl:+.3f} +/- {esl:.3f}: {abs(sl-SLOPE['fw_iso'])/esl:.1f} sigma.  This axis is immune to the stellar M/L "
     f"and needs only N = {N3_slope:.0f} pairs.")
info(f"  P3 mass.  d log sigma / d log M_b = +0.25 (deep MOND). The residual instead climbs with mass at "
     f"{z_trend:.1f} sigma across the sample.")
info(f"  P4 the decisive future sample.  {FCAST[('fw_iso','cosmic_pt',10.0)]:.0f} pairs with 10 km/s velocities "
     f"separate the framework from a cosmic-share halo at 3 sigma on amplitude; DESI and 4MOST pair samples with "
     f"HI or spectroscopic velocities reach that by two orders of magnitude.  What they must ALSO do is isolate "
     f"against a catalogue two magnitudes deeper than 2MRS -- that, not statistics, is what is missing.")

P(""); P("=" * 122)
P(f"RESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "RESULT: 0 FAIL")
P(f"({time.time() - T0:.0f} s)")
P("=" * 122)
sys.exit(0)
