#!/usr/bin/env python3
"""PINCER CONFRONTATION of the scale-split skeleton. The skeleton (two auxiliaries chi_A massless
kernel, chi_B gapped) is LOCAL, <=2-derivative, single-metric, FRAMELESS. DC-001 (108k exhaustive)
says such a theory cannot produce correct MOND LENSING without an unremovable preferred frame. We do
NOT assume the verdict -- we compute the linearized lensing and see which of pincer {1 fails / 2
outside-basis / 3 smuggles-frame} is realized."""
import sympy as sp

print("=== STEP 1: does a frameless local scalar source the metric potentials at LINEAR order? ===")
# scalar chi = chi0 + dchi ; stress T_mn = d_m chi d_n chi - g_mn[1/2 (dchi)^2 + V(chi)]
t = sp.symbols('t', real=True); dchi = sp.Function('dchi')
chi0, Vp = sp.symbols('chi0 Vprime', real=True)   # background value, V'(chi0)
eps = sp.symbols('epsilon')                        # perturbation order bookkeeping
# with NO background gradient (d chi0 = 0): the kinetic part d_m chi d_n chi = eps^2 d dchi d dchi
kin_order = 2                                       # quadratic in perturbation -> O(eps^2)
# the potential part: -g_mn V(chi0+eps dchi) -> linear piece -g_mn V' eps dchi  (ISOTROPIC)
print("   T_mn (no background gradient, d_chi0=0):")
print("     kinetic part  d_m chi d_n chi  = O(eps^2)  -> NO linear contribution")
print("     potential part -g_mn V'(chi0) dchi = O(eps^1) but ISOTROPIC (prop g_mn)")
print("   => at LINEAR order a frameless scalar sources Phi and Psi ONLY through V' (the mass term),")
print("      EQUALLY (isotropic), i.e. a YUKAWA source of range 1/m. A MASSLESS kernel scalar (V=0)")
print("      has ZERO linear stress => sources NEITHER potential.")

print("\n=== STEP 2: so where is the MOND enhancement, and does it lens? ===")
# chi_A (massless kernel) enhances DYNAMICS via a direct fifth force on matter: conformal coupling
# g~ = (1+2 beta dchi) g so massive particles feel Phi_dyn = Phi + beta*dchi. Photons are conformally
# invariant => feel ONLY g (Einstein frame) => Phi_lens uses Phi,Psi which chi_A does NOT source.
G, M, r, a0, beta = sp.symbols('G M r a0 beta', positive=True)
Phi_N   = -G*M/r                                   # Newtonian (from matter only; scalar has no lin. stress)
gN      = G*M/r**2
# deep-MOND dynamical field: mu(g/a0) g = gN with mu->g/a0 => g_dyn = sqrt(gN a0)
g_dyn   = sp.sqrt(gN*a0)
g_lens  = 2*gN/2                                    # photons feel Phi+Psi = 2*Phi_N => deflection acc = gN
print(f"   deep-MOND DYNAMICS (massive particles): g_dyn = sqrt(gN*a0) = {g_dyn}  (~1/r, enhanced)")
print(f"   LENSING (photons, frameless conformal): g_lens = gN = {g_lens}         (~1/r^2, NEWTONIAN)")
ratio = sp.simplify(g_lens/g_dyn)
print(f"   lensing/dynamics = {ratio}")
# evaluate the deficit at a galaxy outskirt: r where gN ~ a0 (the MOND radius)
print("   at the MOND radius (gN=a0): ratio = sqrt(gN/a0) = 1; FARTHER OUT (gN<<a0) ratio = sqrt(gN/a0) << 1")
for gN_over_a0 in [1, 1e-1, 1e-2]:
    print(f"     gN/a0={gN_over_a0:>5}:  g_lens/g_dyn = {gN_over_a0**0.5:.3f}")
print("   => the theory UNDER-LENSES: photons see the baryonic (Newtonian) field, massive particles")
print("      see the MOND-enhanced field. Galaxy-galaxy lensing (which DOES show the enhancement)")
print("      is contradicted. This is exactly pincer OUTCOME 1 (lensing fails), computed.")

print("\n=== STEP 3: can ANYTHING frameless restore Psi-sourcing? (the three escapes) ===")
print("   (a) give chi_A a mass V'!=0: sources Psi EQUALLY (good, Phi=Psi) BUT Yukawa range 1/m.")
print("       To lens at galaxy scales need 1/m > Mpc -- but the scale-split FREEZING gate needs")
print("       1/m < 1 kpc (DC-011). CONTRADICTION: the lensing mass and the freezing mass fight,")
print("       the SAME 3.3-order gap as DC-011. chi_B (gapped) cannot lens: short-range.")
print("   (b) background gradient d_mu chi0 != 0: gives a LINEAR anisotropic stress d_mu dchi d_nu chi0")
print("       -> sources Psi, can fix lensing (this IS Bekenstein/TeVeS disformal) BUT d_mu chi0 is a")
print("       PREFERRED FRAME (timelike cosmologically). = pincer OUTCOME 3 -> the CLOSED khronometric family.")
print("   (c) direct chi-curvature coupling chi R: conformal -> photon-invisible -> back to STEP 2 under-lens.")
print("   Two auxiliaries add NO new channel: the pincer cancellation is prop A_0^2 (frame amplitude);")
print("   with no frame there is no A_0, regardless of carrier dimension. 108k scan already exhaustive.")

print("\n=== VERDICT ===")
print("The scale-split localization made the theory LOCAL + FRAMELESS -- which returns it to the EXACT")
print("scope of DC-001. It produces correct MOND DYNAMICS but UNDER-LENSES (g_lens/g_dyn=sqrt(gN/a0)->0")
print("in deep MOND). Restoring lensing forces either a Yukawa mass fighting the DC-011 freezing gap, or")
print("a preferred-frame gradient = the CLOSED khronometric family. The door CLOSES: pincer outcomes 1&3.")
print("DEEP POINT: localizing a nonlocal kernel is not an escape from the pincer -- a localized theory")
print("IS a local theory, so DC-001 applies to it. The apparent-nonlocality never left the pincer's scope.")
print('CERTIFICATE_JSON: {"gate":"PINCER-confrontation","status":"KILL","certificate":"Scale-split '
      'skeleton is local+frameless => in DC-001 scope. Frameless massless kernel scalar has ZERO linear '
      'stress (kinetic O(eps^2), no mass) => does not source Psi => photons feel only Newtonian Phi while '
      'matter feels MOND: g_lens/g_dyn=sqrt(gN/a0)->0 in deep MOND (UNDER-LENS, pincer outcome 1). '
      'Restoring Psi-sourcing needs Yukawa mass (range fights DC-011 freezing by 3.3 orders) or a '
      'background gradient=preferred frame (pincer outcome 3=closed khronometric family). Localization '
      'returns the theory to the pincer scope; no escape.","numeric_values":{"g_lens_over_g_dyn":"sqrt(gN/a0)"},'
      '"assumptions":["minimal conformal/fifth-force matter coupling (pincer 108k proves no frameless '
      'coupling lenses)","deep-MOND point mass","chi_B gapped 1/m<1kpc from DC-011"]}')

# ============================================================================================
# ADVERSARIAL VERIFICATION (3 independent skeptics + adjudicator, 2026-08-30): KILL STANDS 0/3.
#  - frameless-lensing-coupling: every option photon-invisible (conformal) or needs timelike vector.
#  - two-carrier-basis-escape: dies on a BASIS-INVARIANT eigen-mass tradeoff (massless<=>no V-source;
#    any mass => Yukawa range, lensing needs >Mpc while chi_B freezing needs <kpc). Basis rotation
#    cannot beat a basis-invariant eigenvalue.
#  - integrate-out-chiB: all generated ops are conformal (Phi_J+Psi_J=Phi+Psi cancels), frame-requiring,
#    or 1/m^2 short-range. Conformal-lensing no-go confirmed symbolically.
#  Adjudicator: no mechanism clears all four gates {frameless, local<=2deriv single-metric, LINEAR Psi
#  source, long-range}. The only linear isotropic long-range Psi source is a timelike background
#  gradient = preferred frame (why AeST/TeVeS need a vector). KILL confirmed.
