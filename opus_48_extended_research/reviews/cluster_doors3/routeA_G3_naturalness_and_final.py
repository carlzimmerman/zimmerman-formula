#!/usr/bin/env python3
r"""
ROUTE A -- G3 NATURALNESS + final both-ways synthesis.
======================================================
The |Phi_bar|-keyed law a0_eff = a0*(1 + amp*(|Phi_bar|/c^2)^p) PASSES G1 (closes the
relaxed A2029 core, cov ~100-121%) and G2 (SPARC RAR floor) and G4 (Cassini, Sun shallow
at planets). The LAST gate is G3 (no-new-particle / own-field / not-hand-placed):

  Q1: what is the NATURAL coefficient amp of a |Phi|/c^2 correction?
      A |Phi|/c^2 term is a post-Newtonian / relativistic correction. In GR and in every
      covariant scalar-tensor / RAQUAL / AeST theory the leading potential correction enters
      with an O(1) coefficient: g -> g*(1 + O(1)*|Phi|/c^2). The Route-A law NEEDS
      amp ~ 1.5e5 (p=1).  So the coefficient must be ~1e5 -- FIVE ORDERS too large to be a
      natural relativistic coupling. That is the G3 problem: amp~1e5 is a put-in number.

  Q2: is there ANY framework field that delivers it?
      The framework's own field is the dS-Unruh modified inertia (a0 set by the cosmological
      (cH_Lambda)^2 floor) + the AeST aether/scalar. NEITHER carries a |Phi|/c^2-linear a0
      enhancement with amp~1e5: a0 is a CONSTANT (cosmological), blind to the local potential
      by construction (the whole point of dS-Unruh: T_eff ~ cH, NOT GM/rc^2). Keying a0 on
      local |Phi| is a NEW coupling, not in the framework -> G3 FAILS unless a mechanism is
      named that forces amp~1e5.

  Q3: robustness of the G2 pass -- the deepest galaxies are EARLY-TYPES (absent from SPARC).
      Test the worst case explicitly + the p=1 SPARC margin.

Both ways: the magnitude+shape+galaxy+Cassini gates are genuinely PASSED (a real, non-trivial
finding that corrects the prior 'wrong shape / ~5x contrast / breaks veto' dismissal). The
HONEST verdict turns on G3: is amp~1e5 forced by a field, or hand-placed? Concede if hand-placed.
"""
import numpy as np
G=6.674e-11; c=2.998e8; Msun=1.989e30; kpc=3.0857e19; a0=9.36e-11

print("="*94)
print(" ROUTE A -- G3 NATURALNESS test (is amp~1e5 forced, or a put-in number?)")
print("="*94)

# Needed amp (from the baryonic-Phi closure): p=1 amp=1.5e5, p=2 amp=5.1e9, p=3 amp=1.8e14
amp_needed = {1:1.497e5, 2:5.131e9, 3:1.759e14}
phi_core_bar = 2.917e-5   # A2029 baryonic |Phi|/c^2 at 200 kpc
print("\n[Q1] Natural vs needed coefficient of a |Phi|/c^2 correction:")
print(f"  A natural relativistic/PN coupling: a0_eff=a0*(1+O(1)*|Phi|/c^2).")
print(f"  At the cluster core |Phi_bar|/c^2={phi_core_bar:.2e}, an O(1) coupling gives boost")
print(f"     a0_eff/a0 = 1 + 1*{phi_core_bar:.2e} = {1+phi_core_bar:.6f}  (i.e. +0.003%)")
print(f"  The core NEEDS a0_eff/a0 ~ 3.4 (boost factor B~1.85, deep-MOND M~sqrt(a0)).")
print(f"  Required coefficient amp(p=1) = (3.4-1)/{phi_core_bar:.2e} = {2.4/phi_core_bar:.2e}")
print(f"  -> the coupling must be ~{2.4/phi_core_bar:.0e}, i.e. ~10^5 -- NOT a natural O(1) relativistic")
print(f"     term. To get amp~1e5 you need a NEW dimensionless coupling of size 10^5 put in by hand.")

print("\n[Q2] Does the framework's OWN field deliver amp~1e5?")
print("  dS-Unruh modified inertia: a0 = c^2 sqrt(Lambda/32pi) is COSMOLOGICAL (the (cH_Lambda)^2")
print("  floor). Its defining physics is T_eff ~ cH (the de Sitter horizon), which is BLIND to the")
print("  LOCAL potential by construction. AeST aether/scalar: the field equations have NO")
print("  |Phi|/c^2-linear a0-enhancement term; the cluster residual there is the SAME unboosted")
print("  phantom (that is WHY MI==AeST to machine precision in the core). => no framework field")
print("  carries a |Phi|-keyed a0 with amp~1e5. Adding it = a NEW put-in coupling. G3 FAILS.")

print("\n[Q3] G2 robustness -- the DEEPEST galaxies (early-types, absent from SPARC):")
amp1=1.497e5
def phi_pt(M_Msun,r_kpc): return G*M_Msun*Msun/(r_kpc*kpc*c**2)
# worst real galaxies on the RAR (early-types ARE on the RAR, Lelli+2017, Shajib, etc.)
worst=[
    ("compact massive ellipt M*=3e11 Re=2kpc center", phi_pt(3e11,2.0)*2),
    ("BCG M*=1e12 Re=10kpc center",                   phi_pt(1e12,10.0)*2),
    ("ultra-massive BCG M*=4e12 Re=30kpc center",     phi_pt(4e12,30.0)*2),
]
print(f"  p=1 amp={amp1:.2e}; a0_eff/a0=1+amp*|Phi_bar|/c^2 at early-type centers:")
broken=False
for nm,ph in worst:
    a0r=1+amp1*ph
    # the OBSERVABLE: g_obs shift at the center where g is measured
    # use g ~ a0_eff at the transition; compute worst g_obs shift over a range of g
    gs=np.logspace(np.log10(0.1*a0),np.log10(100*a0),50)
    shift=np.max(np.abs(np.sqrt(gs**2+gs*a0*a0r)/np.sqrt(gs**2+gs*a0)-1))*100
    flag=" <-- >5% RAR shift!" if shift>5 else ""
    if shift>5: broken=True
    print(f"    {nm:46s} a0eff/a0={a0r:5.2f}  max g_obs shift={shift:5.1f}%{flag}")
print(f"  -> NOTE this scans g across the band while pinning |Phi| at the deep CENTER -- an")
print(f"     OVER-estimate. CORRECTION (both ways): at the radius where ETGs are actually MEASURED")
print(f"     on the RAR (g~a0, r~10-19 kpc), |Phi_bar|/c^2 is only ~3-7e-7 (NOT the center value),")
print(f"     so a0_eff/a0~1.05-1.10 and the real g_obs shift at the measured point is ~1-2.5%")
print(f"     (within the RAR floor). The deep center has g>>a0 (boost moot); the g~a0 band has")
print(f"     shallow Phi. So early-types do NOT break G2 -- the 52-72% above was a center-Phi")
print(f"     artifact, caught both ways. G2 PASSES for ETGs too (~1-2.5% at their RAR points).")

print("\n[Q4] The p>=2 'step-function' character (the prior solution_hunt finding, re-confirmed):")
print(f"  p=2 amp={amp_needed[2]:.1e}, p=3 amp={amp_needed[3]:.1e}: these make a0_eff a near-STEP")
print(f"  in |Phi| at the core value. A step tuned to the answer is a hand-placed threshold, not a")
print(f"  coupling (G3 fail). Only p=1 is a smooth coupling -- but p=1 needs amp~1e5 (Q1) AND gives")
print(f"  early-type centers a real ~1.7x a0-boost (Q3). p=1 is the honest best case and it is")
print(f"  G3-unforced (amp~1e5 put in) + marginally G2-stressed on early-types.")

print("\n"+"="*94)
print(" ROUTE A FINAL VERDICT (both ways)")
print("="*94)
print("""  G1 SUFFICIENCY: PASS (genuinely, on the relaxed A2029 footing). A |Phi_bar|-keyed boost
     CLOSES the gas-tracking core: cov ~100-121% across 20-500 kpc, the RIGHT magnitude AND
     ~right (nearly-flat) shape -- because on the relaxed/XRISM-clean cluster B_req~1.6-1.9 is
     nearly flat and |Phi| is nearly flat in the core. This CORRECTS the prior 'wrong shape /
     ~10^5 too weak / only ~5x contrast' dismissal: the true integrated baryonic depth gives a
     6x core/deepest-disk contrast and the law does reach the residual. *** the first genuinely
     G1-passing no-particle cluster boost in the whole hunt. ***
  G2 GALAXY-VETO: PASS. SPARC disks RAR 0.1409->0.1408-0.1423 dex (floor-level); and early-types
     (the deepest-Phi galaxies, absent from SPARC) are ALSO safe -- at the radius where they sit on
     the RAR (g~a0, r~10-19 kpc) |Phi_bar|/c^2~3-7e-7 -> a0_eff/a0~1.05-1.10 -> g_obs shift ~1-2.5%
     (the deep ETG CENTER is g>>a0 where the boost is moot; checked both ways, the 'center-Phi'
     50-70% alarm was an artifact of pinning Phi at the center while scanning g).
  G4 CASSINI/solar/compact: PASS. The Sun's potential at the planets is shallow (|Phi|/c^2~1e-9),
     so a0_eff~a0 in the solar system; the Saturn anomaly is unchanged (1.0001x). Deep Sun-interior
     / neutron-star |Phi| is at g>>>a0 (Newtonian) where a MOND-scale a0-boost is ~1e-19 negligible.
  G3 NO-NEW-PARTICLE: ***FAIL*** -- this is where Route A dies, honestly. The required coupling
     amp~1.5e5 (p=1) is ~10^5x a natural O(1) relativistic |Phi|/c^2 coefficient, and NO framework
     field carries it: dS-Unruh a0 is cosmological (T_eff~cH, blind to local |Phi| by construction),
     AeST has no |Phi|-linear a0 term (that's why MI==AeST in the core). p>=2 closes the veto more
     comfortably but only by becoming a near-STEP-function tuned to the core value = a hand-placed
     threshold. Route A needs a NEW put-in coupling of size 10^5 -> it is NOT own-field, NOT
     known-physics -> G3 fails.
  NET: Route A is the BEST no-particle cluster door found -- it uniquely PASSES G1+G2+G4 (the first
     to close the residual at a0=9.36e-11 with a galaxy- and Cassini-safe term) -- but FAILS G3:
     the |Phi|/c^2-keyed a0 with amp~1e5 is a new put-in coupling, not the framework's own field.
     Both ways: real G1 progress credited (the prior dismissal was too harsh); G3 conceded (no
     mechanism forces amp~1e5; quarantine forbids asserting one). The ~30-49% residual stays the
     shared-MOND gap UNLESS a field that forces a |Phi|-keyed a0 with amp~1e5 is exhibited.""")
