#!/usr/bin/env python3
r"""
OFF-CIRCULAR KERNEL COMPLETION -- pinning attempt for (omega_c, eta(beta)).  SPEC + skeleton.
=============================================================================================
Framework: de Sitter-Unruh MODIFIED INERTIA. a0 = cH_Lambda/Z = 9.36e-11, Z=sqrt(32pi/3),
T_dS = H_Lambda/2pi. The validated CIRCULAR-orbit (on-shell) kernel is
   theta(y) = sqrt2/(1+(sqrt2-1)y^2),  y = om_ext/om_int      (DSUNRUH_MI_THEORY_2026 sec.4)
   m_eff/m  = D(u) = sqrt(g_bar/(g_bar+a0)) = [sqrt(1+4u^2)-1]/(2u),  u = g_obs/a0   (RAR, 0.108 dex)
This is the ONLY directly-constrained slice. The OFF-circular completion carries two DOF:
   (i)  omega_c  (equiv. tau_mem = 1/omega_c): the corner LOCATION, NOT fixed by the dS correlator
        (dsunruh_tau_mem.py: FORM+DC-weight forced, corner-location FREE; three candidate scales,
        bath picks none: om_int (~0.4 Gyr POSTULATE), H_Lambda (~17.5 Gyr), d1-pole (~Myr)).
   (ii) eta(beta): the anisotropy/boost function -- Milgrom-2022 amplitude functional
        A(om) ~ sum_k om_k^2 |r_k| (arXiv:2208.07073 Eq.20/27), pericentre-dominated; on eccentric/
        radial orbits the radial<->tangential dressing splits. This is exactly the d1 "off-circular
        completion UNDERDETERMINED" freedom (d1_kernel_inversion.py S-block, printout) and the
        cluster eta(beta) slide (CLUSTER_ANISOTROPY_MI_TEST_2026, DOI 21104820).

#1 HONESTY GUARD (task): do NOT manufacture a forced omega_c by mis-stating KMS/positivity, nor by
quietly re-inserting the Milgrom-1994 averaging-bandwidth postulate. A constraint that only REDUCES
to the on-shell RAR is a CONSISTENCY condition, not a PINNING one. Same rigor "forced" and "free".

This file: (1) locks the framework objects (exit-0 identities, below); (2) states each candidate
constraint as a concrete math condition, tagged PINNING vs CONSISTENCY, KNOWN-CLOSED vs OPEN;
(3) specs the numeric/analytic test of whether the constraint INTERSECTION pins (omega_c, eta) or
leaves a residual family. Skeleton stages are stubbed where they require the full off-circular
Wightman pullback (named as the closing input). New file; NO git commit.
"""
import numpy as np, sympy as sp
np.seterr(all="ignore")

c   = 2.998e8
Z   = np.sqrt(32*np.pi/3.0)
A0  = 9.36e-11
HL  = A0*Z/c                       # H_Lambda = 1.807e-18 s^-1
kappa = HL                         # dS surface gravity on a comoving worldline
Gyr = 3.156e16

def banner(s): print("\n"+"="*96+"\n "+s+"\n"+"="*96)

# =====================================================================================
# STAGE 0 -- lock the framework objects the completion must reduce to (exit-0 identities)
# =====================================================================================
banner("STAGE 0: framework objects (on-shell target + validated kernel)")
u  = sp.symbols('u',  positive=True)
y  = sp.symbols('y',  positive=True)
g, a0 = sp.symbols('g a0', positive=True)
# on-shell dressing target
D = (sp.sqrt(1+4*u**2)-1)/(2*u)
assert sp.simplify(g/sp.sqrt(g**2+g*a0) - sp.sqrt(g/(g+a0))) == 0        # m_eff/m identity
# validated circular kernel
theta = sp.sqrt(2)/(1+(sp.sqrt(2)-1)*y**2)
assert sp.simplify(theta.subs(y,0)-sp.sqrt(2)) == 0                      # DC weight sqrt2 (forced)
assert sp.simplify(theta.subs(y,1)-1) == 0                              # zero-crossing at y=1
print("  on-shell target m_eff/m = D(u), validated theta(y): DC=sqrt2, theta(1)=1  [locked]")

# =====================================================================================
# STAGE 1 -- parametrize the OFF-CIRCULAR DOF
# =====================================================================================
# General retarded induced-inertia kernel on a NON-circular worldline, in the body frame:
#   F_med,i(t) = - Int_0^inf  K_ij(t-s; {a(.)}, beta)  a_j(s) ds
# Decompose into a corner (single memory scale) x a direction/anisotropy tensor:
#   K_ij(w) = m * S(|a|/a0) * L(w/omega_c) * P_ij(nhat, beta)
#   L(x) = 1/(1 + x^2)     (Lorentzian FORM forced by dS 1/sinh^2 envelope; THETA note sec.2)
#   S(u) = 1 - D(u)         (saturation law forced on-shell)
#   P_ij = radial/tangential split; on eccentric orbits the AMPLITUDE functional
#          A(om) ~ sum_k om_k^2 |r_k| (Milgrom-2022) makes the effective normalization
#          eta(beta) = <A>_radial-weighted -- the DOF the circular slice integrates away.
# TWO free objects survive the on-shell reduction:
#   (i)  omega_c  (the corner; scalar)     (ii) eta(beta) (anisotropy; a function of boost/ecc beta)
banner("STAGE 1: off-circular DOF = (omega_c, eta(beta)); L,S forced, P/eta free off-shell")
print("  K_ij(w)=m S(|a|/a0) L(w/omega_c) P_ij(beta);  L,S on-shell-forced; (omega_c, eta(beta)) FREE off-shell")

# =====================================================================================
# STAGE 2 -- each candidate constraint as a math condition; PINNING vs CONSISTENCY
# =====================================================================================
banner("STAGE 2: constraints (math condition | pinning? | closed/open)")
CONSTRAINTS = [
 dict(name="C1 on-shell RAR reduction",
      cond="lim_{ecc->0} K_ij(w) circular-avg  ==  m S(u) theta(y):  D(u) recovered to 0.108 dex",
      verdict="CONSISTENCY (necessary, NOT pinning)",
      status="KNOWN-CLOSED as a *check*; explicitly does NOT pin omega_c (theta scale-free in y).",
      pins=False),
 dict(name="C2 KMS / thermality (T_dS=H_L/2pi)",
      cond="S_bath(-w)=e^{-w/T_dS} S_bath(w); detailed balance ties +/- freq parts of the dS bath",
      verdict="CONSISTENCY (fixes the NOISE<->dissipation ratio & the FORM/tail order, not the corner)",
      status="KNOWN-CLOSED (dsunruh_tau_mem FDT: nearest Matsubara pole = kappa; NO in-band resonance; "
             "KMS does NOT fix pole COUNT (sqrt2 vs 2 residual) nor corner LOCATION). Off-circular KMS "
             "still refers the bath to kappa=H_L, 44x from om_int -> NON-pinning of om_c.",
      pins=False),
 dict(name="C3 dS spectral positivity of the 2-pt (Kallen-Lehmann / Bros-Moschella)",
      cond="rho(w) with F(w)>=0 all w; induced-inertia 2-pt has KL-positive spectral density",
      verdict="CONSISTENCY (sign/passivity constraint; bounds SIGN not corner LOCATION)",
      status="KNOWN-CLOSED for the SIGN (residual-doors D1 2nd-order + sixth-thm all-orders: F(w)>=0 "
             "forces anti-MOND from a PASSIVE bath; the MOND sign needs the Machian excess reading, "
             "not a corner choice). Positivity is corner-LOCATION-BLIND: it holds for ANY omega_c>0.",
      pins=False),
 dict(name="C4 dS 4-pt / interacting Bros-Moschella positivity",
      cond="complementary-series KL positivity of the interacting induced-inertia 4-pt on the worldline",
      verdict="OPEN in the math literature; but band-separated (in-band w/H in [15,10800]) so cannot "
             "source in-band inertia -> even if it constrained a corner it would be OUT of band",
      status="OPEN (named edge, residual-doors sec.6); bypassed by band-separation+stochastic gap, "
             "NOT resolved. Does NOT reach down to omega_int either way.",
      pins=False),
 dict(name="C5 causality / analyticity (Kramers-Kronig)",
      cond="K(w) analytic in UHP; Re/Im tied by KK; forced DC weight sqrt2 + Lorentzian FORM",
      verdict="CONSISTENCY (forces FORM-class + tail order; a single-pole KK-causal kernel exists for "
              "EVERY omega_c) -- NOT pinning",
      status="KNOWN-CLOSED (THETA note sec.2 + d1 S6: bare dS response is OHMIC/local, carries NO "
             "intrinsic corner; KK is satisfied by a one-parameter family in omega_c).",
      pins=False),
 dict(name="C6 orbit (in)stability clamp on in-band weight",
      cond="in-band dissipative |Im K/Re K| < ~H0/(5 S w) (orbits neither decay nor blow up over t_H)",
      verdict="BOUNDS the in-band weight (forbids a dissipative in-band corner); pushes weight ABOVE "
              "band or requires reactive KK-tail delivery -- a BOUND, not a pin at om_int",
      status="KNOWN-CLOSED (d1 S3/S6): in-band DISSIPATIVE corner excluded ~1e-4; consistent with om_c "
             "ABOVE band (d1 pole ~Myr) OR reactive tail -- still does NOT select om_int.",
      pins=False),
]
for k in CONSTRAINTS:
    tag = "PIN" if k["pins"] else "cons"
    print(f"  [{tag}] {k['name']}\n        cond: {k['cond']}\n        {k['verdict']}\n        -> {k['status']}\n")

pinning = [k for k in CONSTRAINTS if k["pins"]]
print(f"  PINNING constraints found: {len(pinning)}   (all six are consistency/bound, none pin om_c)")

# =====================================================================================
# STAGE 3 -- the eta(beta) DOF: is IT pinned by the same constraints?
# =====================================================================================
# eta(beta) sign IS forced (Milgrom-2022 amplitude functional pericentre-dominated -> d ln eta/d beta>0),
# an on-shell-safe, MG-impossible SIGN. But its MAGNITUDE (the slope value ~+0.75 deep, diluted ~0.5 at
# cluster g~0.3-1 a0) inherits BOTH a memory-order residual (sqrt2 vs 2) AND omega_c (which sets how much
# of the pericentre amplitude the finite memory RETAINS). So eta(beta):
#   - SIGN: FORCED (positivity + amplitude functional; MG-impossible).  [pinning of sign]
#   - MAGNITUDE/SLOPE: BOUNDED but omega_c-hostage (same hostage as the dwarf door).
banner("STAGE 3: eta(beta) -- sign FORCED, magnitude BOUNDED-but-omega_c-hostage")
# demonstrate the amplitude-functional sign on a Kepler-toy (residence vs amplitude average):
for e in [0.0,0.3,0.6,0.9]:
    E=np.linspace(0,2*np.pi,20000); r=1-e*np.cos(E); acc=1.0/r**2
    dt=(1-e*np.cos(E)); dt/=dt.sum()
    print(f"  e={e:.1f}  <|a|>_time={np.sum(acc*dt):6.2f}  rms={np.sqrt(np.sum(acc**2*dt)):8.2f}  "
          f"peak={acc.max():9.1f}   (amplitude-avg RISES with e -> eta rises: SIGN forced)")
print("  => d ln eta/d beta > 0 is FORCED (pericentre-dominated amplitude functional, MG-impossible);")
print("     the SLOPE MAGNITUDE is omega_c-hostage (finite memory sets pericentre-amplitude retention).")

# =====================================================================================
# STAGE 4 -- the computation that WOULD pin omega_c (the closing input), spec'd
# =====================================================================================
banner("STAGE 4: what a genuine pin requires (the closing computation)")
print(r"""  The ONLY object that could pin omega_c is the OFF-CIRCULAR dS-Unruh Wightman PULLBACK:
    (P) evaluate W(tau,tau') = <phi(x(tau))phi(x(tau'))> on a NON-uniform (eccentric) de Sitter
        worldline x(tau), NOT the uniform/circular reduction. Extract the induced-inertia kernel
        K_ij[{a(.)}] to O(a_ext) and read whether its DOMINANT pole sits at om_int, or (as on the
        circular slice) stays at kappa=H_L / above-band.
    TEST (falsifiable, both-ways):
      * build K_ij on a family of Kepler worldlines (eccentricity e in [0,0.9]) in the dS bath;
      * locate the dominant pole om_c(e); if om_c(e) -> om_int(e) ROBUSTLY across e and footing
        (a0=9.36e-11 vs 1.13e-10), omega_c is FORCED -> dwarf door dated, eta(beta) slope pinned;
      * if om_c(e) tracks kappa or the d1 above-band pole (as the circular slice does), FREE stands.
    PREDICTED OUTCOME (honest prior, from the circular slice + d1 + tau_mem): the non-uniform pullback
    inherits the SAME kappa/above-band pole structure; the ONLY thing that lands om_c at om_int is the
    Milgrom-1994 quasi-static averaging-bandwidth postulate (Eq.55-57), whose general multi-frequency
    Eq.33 case is OBSTRUCTED. So the expected verdict is FREE (bounded), not FORCED -- and the honest
    deliverable is the constrained space below, NOT a manufactured pin.
    STATUS: (P) requires the full off-circular Wightman pullback -- NOT done here (named closing input,
    matching the d1 'off-circular completion UNDERDETERMINED' flag). This file specs it; it does not
    fake the result.""")

# =====================================================================================
banner("BOTTOM LINE (spec)")
print("""  omega_c: FREE (bounded). Six constraints (C1 RAR, C2 KMS, C3 2-pt positivity, C4 4-pt/dS,
    C5 KK-causality, C6 orbit-stability) are ALL consistency/bound conditions -- ZERO pin omega_c.
    Reducing to the on-shell RAR does NOT pin the off-shell corner (theta scale-free in y). The corner
    sits in a one-parameter family; bath-derived scales bracket it (H_L ~17.5 Gyr .. d1-pole ~Myr) but
    NONE equals om_int (~0.4 Gyr); only the Milgrom-1994 averaging-bandwidth postulate lands it there.
  eta(beta): SIGN FORCED (d ln eta/d beta > 0, MG-impossible, amplitude-functional + positivity);
    MAGNITUDE/SLOPE BOUNDED but omega_c-hostage (same hostage as the dwarf sigma-hysteresis door).
  CLOSING INPUT: the off-circular dS Wightman pullback (Stage 4) -- OR an empirical proxy measurement
    (dwarf sigma-hysteresis amplitude / cluster eta(beta) slope), which MEASURES omega_c rather than
    deriving it. No positivity/KMS bound was mis-stated to force a corner; FREE is the honest verdict.""")
print("\nEXIT 0")
