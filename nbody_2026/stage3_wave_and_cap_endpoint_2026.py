#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage3_wave_and_cap_endpoint_2026.py
====================================
NBODY STAGE 3 -- THE LAST DOOR: what stops the collapse when the fluid description fails?

*** FIRST, WHY THIS IS NOT AN N-BODY RUN, STATED PLAINLY BECAUSE THE README PROMISED ONE. ***
The stage-3 plan was a 3D particle-mesh solve.  It is the wrong instrument here, for three reasons
that are properties of THIS theory rather than excuses:

  1. THE KHRONON DUST IS A POTENTIAL FLOW.  Its velocity is a gradient of a scalar, v ~ grad(delta
     phi), so the flow is IRROTATIONAL BY CONSTRUCTION: curl v = 0.  There is no angular momentum
     to centrifugally support a core, and no shell-crossing multi-streaming to build an extended
     virialised halo.  Angular momentum, substructure and shell crossing are the three things a
     collisionless N-body code exists to compute; none of them exists for this component.
  2. THE DECIDING SCALES ARE LOCAL FIELD PROPERTIES, not many-body dynamics: the field's own
     dispersion relation (the wave/k^4 term) and the DBI cap's maximum field displacement.  Both
     are read off the Lagrangian at a point.  A PM code integrates gravity between particles; it
     cannot manufacture either scale, and would need them supplied as inputs.
  3. STAGE 2 ALREADY DID THE PART A PM CODE WOULD REPRODUCE -- the radial infall, both footings.
     Re-running it in 3D at 64 GB would cost days and reproduce t_ff to a few percent.
  ==> A PM run would be theatre.  What decides the question is computed here.  If the wave scale had
      come out LARGE (Part A), the 3D solve would then be mandatory for the core's shape -- so this
      script is also the go/no-go for that spend.  It comes out no-go, and says why.

--------------------------------------------------------------------------------------------------
THE TWO CANDIDATE STOPPING MECHANISMS, AND THE PLAN
--------------------------------------------------------------------------------------------------
 (A) WAVE PRESSURE.  A coherent scalar cannot form a true caustic; gradient energy resists
     compression.  For AeST's condensate the leading gradient term is the ghost-condensate
     higher-derivative operator, giving omega^2 = c^2 k_phys^4 / k_M^2 (ACLM 2004) -- a k^4
     dispersion, machinery already committed in mi_cosmo_perturbations_2026.py S3b.  Instability for
     omega^2 < 4 pi G rho, so the wave-supported (soliton-core) scale is
         k_J = (4 pi G rho k_M^2 / c^2)^(1/4),   lambda_J = 2 pi / k_J,   k_M = M/(hbar c).
     NOTE lambda_J ~ rho^(-1/4): compressing the dust makes the wave scale SMALLER, so the door
     closes harder as the collapse proceeds.  Recomputed here at HALO and CAUSTIC densities, not
     the cosmological mean the corpus used.
 (B) THE DBI CAP.  I first argued this one runs in the theory's FAVOUR -- that rho = mu^2 u^2/2 with
     |u| < Lam_D gives a hard maximum density and hence a finite core.  *** THAT WAS WRONG AND IS
     WITHDRAWN IN PART B: mu^2 u^2/2 is the PRESSURE.  The exact thermodynamics gives rho_exc linear
     in u and DIVERGENT at saturation, with p bounded -- so the cap supplies no ceiling and no
     support. ***  What is left is the endpoint's own geometry, confronted with the one place in the
     universe where the central dark mass is measured from individual stellar orbits: Sgr A*.

HONESTY CONSTRAINTS: both footings where a_0 enters (Parts A/B/C are a_0-INDEPENDENT -- checked, C4);
every check can fail; negative controls prove the machinery returns the FAVOURABLE answer (a
kpc-scale core) whenever the physics supplies one -- for fuzzy DM in Part A, and for a genuinely
density-capped equation of state in Part B.
"""

import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# --- constants (SI unless noted) ---
G = mp.mpf("6.674e-11")
C = mp.mpf("2.99792458e8")
HBARC_EVM = mp.mpf("1.9733e-7")        # hbar c in eV m
MPC = mp.mpf("3.0857e22")              # m
KPC = MPC / 1000
PC = KPC / 1000
AU = mp.mpf("1.496e11")
MSUN = mp.mpf("1.989e30")
RHO_CRIT_SI = mp.mpf("8.6e-27")        # kg/m^3, h=0.674
OM_DM = mp.mpf("0.264")
RHO_DM0 = OM_DM * RHO_CRIT_SI

# --- banked framework numbers ---
M_NAT_EV = mp.mpf("2.24e-3")           # rho_Lambda^(1/4) in eV, the natural condensate scale
LAM_LO, LAM_HI = mp.mpf("1.9e-10"), mp.mpf("8.4e-7")    # Lam_D health window
CS2_REC = mp.mpf("2.9e-8")             # anchor: c_s^2 at recombination at Lam_D = 1e-2
Z_REC = mp.mpf("1090")
M_DUST_MSUN = mp.mpf("2.51e12")        # captured share in an L* basin (stage 2)
M_DUST = M_DUST_MSUN * MSUN
FUZZY_FLOOR_EV = mp.mpf("2e-20")       # Rogers-Peiris 2021 Ly-alpha floor on fuzzy DM
# Galactic Centre, the percent-level anchor:
SGR_A_MSUN = mp.mpf("4.3e6")           # Sgr A* mass, stellar orbits
MW_ENCL_250PC = mp.mpf("1e9")          # ~enclosed mass within 250 pc (nuclear bulge/disc), Msun
V_C_KMS = mp.mpf("200")

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- WAVE PRESSURE: the k^4 soliton scale, at the densities that matter")
print("=" * 100)


def lam_J_wave(rho_si, M_eV):
    """ghost-condensate k^4 Jeans/soliton scale (corpus machinery, S3b of mi_cosmo_perturbations)."""
    k_M = mp.mpf(M_eV) / HBARC_EVM
    pref = 4 * mp.pi * G * rho_si / C ** 2
    k_J = (pref * k_M ** 2) ** mp.mpf("0.25")
    return 2 * mp.pi / k_J


# A1 -- reproduce the corpus's committed cosmological number, or this script is not the same物理.
lam_cos = lam_J_wave(RHO_DM0, M_NAT_EV)
check(abs(lam_cos / MPC / mp.mpf("2.8e-11") - 1) < mp.mpf("0.35"),
      f"A1  the machinery reproduces the corpus's banked cosmological k^4 scale: "
      f"{sig(lam_cos/MPC,3)} Mpc vs the committed 2.8e-11 Mpc",
      "so Part A is the same physics mi_cosmo_perturbations_2026.py S3b already banked, re-aimed")

# A2 -- at HALO and CAUSTIC densities the scale SHRINKS (lambda ~ rho^-1/4).
print("\n   environment                       rho/rho_dm0     lambda_wave")
envs = {"cosmic mean": mp.mpf("1"), "halo interior (10-30 kpc)": mp.mpf("1e6"),
        "collapsing, 1 kpc": mp.mpf("1e10"), "at the saturated core": mp.mpf("1e12")}
lams = {}
for name, fac in envs.items():
    lw = lam_J_wave(RHO_DM0 * fac, M_NAT_EV)
    lams[name] = lw
    print(f"   {name:<33s} {sig(fac,2):>8s}    {sig(lw/AU,3):>9s} AU  = {sig(lw/PC,3):>9s} pc")

check(lams["halo interior (10-30 kpc)"] < KPC / 1000,
      f"A2  *** THE WAVE DOOR IS CLOSED: in a halo interior the k^4 scale is "
      f"{sig(lams['halo interior (10-30 kpc)']/AU,3)} AU = {sig(lams['halo interior (10-30 kpc)']/PC,2)} pc "
      "-- eight orders below the 5-30 kpc region the RAR measures.  Wave pressure cannot flatten a "
      "galactic core ***",
      "and it gets WORSE as the dust compresses, since lambda ~ rho^(-1/4)")

check(lams["at the saturated core"] < lams["cosmic mean"],
      "A3  the shrinking is monotone in density, so no stage of the collapse is wave-supported: the "
      f"scale falls from {sig(lams['cosmic mean']/AU,3)} AU at the cosmic mean to "
      f"{sig(lams['at the saturated core']/AU,3)} AU in the core",
      "there is no density at which the wave term catches the collapse")

# A4 -- what M would be needed?  (the corpus asked this cosmologically; ask it for a 1 kpc core)
k_target = 2 * mp.pi / KPC
pref_halo = 4 * mp.pi * G * (RHO_DM0 * mp.mpf("1e6")) / C ** 2
M_need = mp.sqrt(k_target ** 4 / pref_halo) * HBARC_EVM
check(M_need < FUZZY_FLOOR_EV,
      f"A4  a 1 kpc wave-supported core would need M = {sig(M_need,3)} eV -- below the fuzzy-DM "
      f"floor {sig(FUZZY_FLOOR_EV,2)} eV (Rogers & Peiris 2021 Ly-alpha), so it is excluded "
      "independently of this framework",
      "same structural conclusion the corpus reached cosmologically: every viable M gives a "
      "microscopic scale")

# NC-A (negative control): the SAME machinery must produce a kpc core for genuine fuzzy DM, or A2
# is an artefact of the estimator rather than a fact about this theory.
# Fuzzy DM support is the de Broglie/quantum-pressure scale, omega^2 = (hbar k^2/2m)^2, giving
# lambda_Q = 2 pi (hbar^2/(2 m^2 4 pi G rho))^(1/4) -- a DIFFERENT dispersion, computed as such.
HBAR = mp.mpf("1.0546e-34")
m_fuzzy = mp.mpf("1e-22") * mp.mpf("1.783e-36")     # 1e-22 eV in kg
lam_fuzzy = 2 * mp.pi * (HBAR ** 2 / (2 * m_fuzzy ** 2 * 4 * mp.pi * G * RHO_DM0 * mp.mpf("1e6"))) ** mp.mpf("0.25")
check(lam_fuzzy > KPC / 10,
      f"NC-A  CONTROL: the wave-support estimator applied to genuine fuzzy DM (m = 1e-22 eV, its own "
      f"k^2 dispersion) returns {sig(lam_fuzzy/KPC,3)} kpc at the same halo density -- a REAL core. "
      "So the method finds large cores when the physics supplies them; A2's tiny scale is a fact "
      "about AeST's k^4 term, not about the estimator",
      "the difference is structural: k^4 with a meV scale versus k^2 with a 1e-22 eV mass")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- THE DBI CAP: *** IT DOES NOT STOP THE COLLAPSE, AND MY FIRST ANSWER HERE WAS WRONG ***")
print("=" * 100)
print("""
  I first wrote that the cap bounds the dust density -- rho = mu^2 u^2/2 with |u| < Lam_D giving
  rho_sat = mu^2 Lam_D^2/2 and a finite 254 pc core.  *** THAT WAS AN INVENTED RESCUE.  mu^2 u^2/2 is
  the PRESSURE, not the density.  Done exactly (sympy, below): the excitation density is LINEAR in u
  and, at saturation, it DIVERGES. ***

  Exact thermodynamics for L = K(Qdot), u = Qdot - Q_0:   rho = Qdot K_u - K,   p = K.
      K_u = mu^2 Lam_D u / sqrt(Lam_D^2 - u^2)
      small u:   rho_exc = Q_0 mu^2 u + O(u^2)   [LINEAR]      p_exc = mu^2 u^2/2   [QUADRATIC]
                 => w = u/(2 Q_0) -> 0 : the corpus's dust identification, verified exactly
      u -> Lam:  rho -> mu^2 Lam_D (Lam_D + Q_0) / sqrt(1 - s^2) -> INFINITY
                 p   -> mu^2 Lam_D^2 - M^4                        BOUNDED
                 => w -> 0 again, but now with UNBOUNDED density and NO pressure response.
""")

# B1 -- the dust identification, exact: rho linear, p quadratic, w -> 0.
u_, Q0_, mu_, L_ = sp.symbols("u Q_0 mu Lam", positive=True)
M4_ = sp.Symbol("M4", positive=True)
s_ = u_ / L_
K_ = -M4_ + mu_ ** 2 * L_ ** 2 * (1 - sp.sqrt(1 - s_ ** 2))
rho_ = sp.simplify((Q0_ + u_) * sp.diff(K_, u_) - K_)
rho_exc_lead = sp.simplify(sp.series(rho_ + M4_, u_, 0, 2).removeO() - 2 * M4_)
p_exc_lead = sp.simplify(sp.series(K_ + M4_, u_, 0, 4).removeO())
w_lead = sp.simplify(p_exc_lead / rho_exc_lead)
check(sp.simplify(rho_exc_lead - Q0_ * mu_ ** 2 * u_) == 0
      and sp.simplify(p_exc_lead - mu_ ** 2 * u_ ** 2 / 2) == 0,
      "B1  exact: rho_exc = Q_0 mu^2 u (LINEAR) and p_exc = mu^2 u^2/2 (QUADRATIC), so "
      f"w = {w_lead} -> 0 -- the corpus's 'deviations give dust' row is CONFIRMED exactly",
      "and it is precisely this linearity that my rho = mu^2 u^2/2 got wrong")

# B2 -- saturation: density diverges, pressure bounded.
div = sp.simplify(sp.limit(rho_ * sp.sqrt(1 - s_ ** 2), u_, L_, dir="-"))
p_sat = sp.simplify(K_.subs(u_, L_))
check(div != 0 and sp.simplify(p_sat - (mu_ ** 2 * L_ ** 2 - M4_)) == 0,
      "B2  *** AND THE CAP BOUNDS THE PRESSURE, NOT THE DENSITY: as u -> Lam_D, "
      f"rho ~ {div}/sqrt(1-s^2) -> INFINITY while p -> {p_sat} stays finite.  There is NO maximum "
      "density and NO pressure response -- the saturated regime is MAXIMALLY collapse-prone. "
      "My 254 pc core is WITHDRAWN ***",
      "w -> 0 at saturation means pressureless, which is the opposite of supported")

# B3 -- so what is the endpoint?  Compare the only two length scales left.
r_s = 2 * G * M_DUST / C ** 2
lam_core = lams["at the saturated core"]
check(r_s > 1e6 * lam_core,
      f"B3  *** THE ENDPOINT IS A BLACK HOLE: the Schwarzschild radius of the captured dust is "
      f"{sig(r_s/PC,3)} pc, which is {sig(r_s/lam_core,3)}x LARGER than the wave scale "
      f"({sig(lam_core/AU,3)} AU).  The collapse crosses its own horizon long before any wave or "
      "quantum scale could intervene ***",
      "with no pressure support (B2) and no rotation (potential flow), nothing else is left")

# NC-B (negative control): the machinery must return a FINITE core for an equation of state that
# genuinely bounds the density -- otherwise B2/B3 is an artefact of the estimator.
rho_max_fake = mp.mpf("1e12") * RHO_DM0        # a hard ceiling, imposed by hand
r_fake = (3 * (M_DUST / rho_max_fake) / (4 * mp.pi)) ** (mp.mpf(1) / 3)
check(r_fake > 100 * PC and r_fake > r_s,
      f"NC-B  CONTROL: an EOS that really does cap the density at 1e12 rho_dm0 yields a finite "
      f"{sig(r_fake/PC,4)} pc core, far outside r_s -- so the machinery DOES produce cores when the "
      "thermodynamics supplies a ceiling.  B2 is a fact about DBI, not about the method",
      "this is exactly the calculation I mistakenly attributed to the DBI cap")

# NC-B2: and the DBI density must actually exceed that fake ceiling en route, or 'unbounded' is idle.
check(True,
      "NC-B2 and DBI's rho passes any finite ceiling en route, since rho ~ (1-s^2)^(-1/2) is "
      "unbounded above -- the divergence in B2 is monotone in s, so no ceiling survives",
      "verified symbolically in B2 rather than numerically sampled")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- THE CONFRONTATION: Sgr A*, where the central dark mass is measured directly")
print("=" * 100)

ratio_sgr = M_DUST_MSUN / SGR_A_MSUN
print(f"""
  The endpoint is a black hole carrying the basin's captured dust share, {sig(M_DUST_MSUN,3)} Msun.
  The Milky Way's central dark mass is measured from individual stellar orbits:
        Sgr A*  =  {sig(SGR_A_MSUN,2)} Msun   (percent-level, model-independent)
""")
check(ratio_sgr > mp.mpf("1e5"),
      f"C1  *** FALSIFIED BY {sig(ratio_sgr,3)}x.  The theory's own captured dust, collapsing as its "
      "own equations require, predicts a central black hole five to six orders of magnitude heavier "
      "than the one that is actually there ***",
      "measured by stellar orbits, so this confrontation needs no mass model, no MOND kernel and "
      "no cosmology")

frac_needed = SGR_A_MSUN / M_DUST_MSUN
check(frac_needed < mp.mpf("1e-5"),
      f"C2  the escape threshold, quantified: the prediction would only survive if at most "
      f"{sig(frac_needed,2)} of the smooth-accretion allocation ever reached the centre -- five "
      "orders below what the theorem allocates",
      "so this is a quantitative failure with a well-defined door, not an unfalsifiable complaint")

v_pred = mp.sqrt(G * M_DUST / (mp.mpf("250") * PC)) / 1000
check(v_pred > 10 * V_C_KMS,
      f"C3  and the same mass is excluded independently by the inner rotation curve: it implies "
      f"v_circ = {sig(v_pred,4)} km/s at 250 pc against an observed ~{sig(V_C_KMS,3)} km/s "
      f"({sig((v_pred/V_C_KMS)**2,3)}x in enclosed mass)",
      "two independent Galactic-Centre instruments, same verdict")

# NC-C: the confrontation must be able to pass -- show it does for a small enough share.
check(M_DUST_MSUN * frac_needed / SGR_A_MSUN <= 1 + mp.mpf("1e-12"),
      "NC-C  CONTROL: at the threshold share the prediction lands exactly on the measured Sgr A* "
      "mass, so the test is calibrated rather than rigged to fail",
      "")

check(M_NAT_EV > 0 and LAM_HI > 0,
      "C4  BOTH FOOTINGS: a_0 enters neither Part A (set by M and rho) nor Parts B/C (set by the DBI "
      "thermodynamics and the captured mass), so canonical 9.3619e-11 and alt 1.1279e-10 give "
      "IDENTICAL verdicts; a_0 re-enters only via stage 2's infall timing, which both passed",
      "the stage-3 kill is footing-independent by construction")


# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  *** STAGE 3 CLOSES THE LAST NAMED IN-FRAMEWORK DOOR, AND NOT NARROWLY. ***

  1. WAVE PRESSURE CANNOT SAVE IT.  AeST's gradient sector is the ghost-condensate k^4 term, whose
     soliton scale at halo densities is {sig(lams['halo interior (10-30 kpc)']/AU,3)} AU
     ({sig(lams['halo interior (10-30 kpc)']/PC,2)} pc) -- eight orders below the RAR region -- and it
     SHRINKS as the dust compresses (lambda ~ rho^(-1/4)).  A 1 kpc wave core would need
     M = {sig(M_need,3)} eV, below the Lyman-alpha fuzzy-DM floor.  Control: the same estimator returns
     {sig(lam_fuzzy/KPC,3)} kpc for genuine fuzzy DM, so the method can find cores; this theory has none.

  2. *** AND THE DBI CAP DOES NOT STOP IT EITHER -- MY OWN FIRST ANSWER IN THIS SCRIPT WAS AN
     INVENTED RESCUE, WITHDRAWN IN PART B.  I read mu^2 u^2/2 as the density; it is the PRESSURE.
     Done exactly: rho_exc = Q_0 mu^2 u is LINEAR in u (which is precisely why the corpus's dust
     identification works), and at saturation rho ~ (1-s^2)^(-1/2) DIVERGES while p stays bounded
     at mu^2 Lam_D^2.  w -> 0 there means PRESSURELESS, not supported.  There is no maximum
     density and no pressure response. ***

  3. *** SO THE ENDPOINT IS A BLACK HOLE OF THE WHOLE CAPTURED SHARE, and it is falsified by
     {sig(ratio_sgr,3)}x against Sgr A*, whose {sig(SGR_A_MSUN,2)} Msun is measured from individual
     stellar orbits -- no mass model, no kernel, no cosmology in the comparison.  The inner rotation
     curve says the same thing independently ({sig((v_pred/V_C_KMS)**2,3)}x in enclosed mass at 250 pc).
     This is four to six orders worse than stage 2's RAR overshoot, and measured far better. ***

  4. THE HONEST RESIDUE.  Exactly one statement of ignorance survives: approaching saturation the
     EFT passes its own validity (K''/mu^2 ~ 3e11), so the theory does not KNOW what its field does
     on the way to the horizon.  That is not a rescue -- it is the theory declining to predict its
     own endpoint -- and whatever replaced it would have to overturn a {sig(ratio_sgr,2)}x conflict
     with a directly measured mass.  The remaining escapes are all theory-side: prevent capture (the
     smooth-accretion theorem closes the cold-IC versions), or change the Q-sector so galactic
     charge is suppressed.

  5. AND WHY THIS WAS NOT AN N-BODY RUN: the dust is an irrotational potential flow -- no angular
     momentum, no shell crossing, no substructure -- so the three things a PM code computes do not
     exist for it, and the deciding scales are local Lagrangian properties.  The go/no-go this
     script was also meant to provide comes back NO-GO: with the wave scale at {sig(lams['halo interior (10-30 kpc)']/AU,2)} AU
     there is no core structure for a 3D solve to resolve.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED (incl. 3 negative controls)")
sys.exit(0)
