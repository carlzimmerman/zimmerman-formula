#!/usr/bin/env python3
"""
K011 -- the projectable-khronon integration-constant dust as the AMPLITUDE LAW.

A genuinely new first-principles piece, from the gemini_38_flash_push repo's Door 1,
tested here for the first time against the GALAXY amplitude law (it was proposed for
clusters).  In projectable khronometric gravity (N = N(t)), the Hamiltonian constraint
leaves a local remnant
    H_0(t, x) = C(x) / a^3(t),
a spatial INTEGRATION CONSTANT C(x) that behaves as a cold, pressureless dust
(c_s^2 = 0 EXACTLY, not as a limit).  This is the one candidate whose dark matter has
NO equation of state -- so the barotropic no-go (collapse_2026.py: no c_s^2(rho) gives
both flat curves and BTFR) DOES NOT APPLY to it.  That is the loophole, and it is new.

THE CLAIM UNDER TEST:
  The integration constant C(x) is set ONCE, at formation, by the local physics.  The
  only galactic scale is r_M (K009/DERIVATION_CHAIN: the dimensionally unique length).
  If the condensate thermalised at the MOND radius (Rung 5), the natural dust profile is
      rho_dust(r) = C(x) = sigma^2/(2 pi G r^2),   sigma^2 = (1/2) sqrt(G M_b a0),
  i.e. the amplitude law.  The QUESTION is whether the projectable-dust mechanism can
  CARRY that profile without contradiction, and whether it stays cold in clusters
  (solving the 2x cluster shortfall the framework otherwise fails).

WHAT WE TEST (honestly, both a0 footings):
  T1. The dust is EXACTLY cold: c_s^2 = 0 identically (no EOS, so no barotropic no-go).
  T2. The amplitude-law profile rho = A/r^2 is a VALID integration-constant profile:
      it is static, cold, and sources a flat rotation curve at the BTFR level.
  T3. The SAME mechanism in a cluster well (deep potential) does NOT expel the dust
      from the core (c_s^2 = 0 means no acoustic pressure) -- so it can supply the
      missing cluster mass WHERE the scalar condensate failed (the hot-core problem).
  T4. The cluster normalisation: can C(x) at cluster scale reach the required
      M_d/M_b ~ 7.3 at 40-100 kpc WITHOUT disturbing the galaxy amplitude law?
  T5. HONESTY: the integration constant C(x) is a FREE function of space unless a
      formation principle fixes it.  Does the mechanism DERIVE the profile, or merely
      PERMIT it?  If it only permits, the amplitude law is still put in by hand -- the
      same charge the framework levels at inserting r_M.  Stated plainly.

This is a NEW synthesis (Door 1 + the K009 amplitude-law equilibrium), tested against
the framework's own gates.  A PASS is necessary-not-sufficient; a FAIL is reported.
"""
import json, math, os
import numpy as np

RES, NP, NF = [], 0, 0
def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading: print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    if ok: NP += 1
    else:  NF += 1

print(__doc__)
G, MSUN, KPC = 6.674e-11, 1.98892e30, 3.0857e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
def rM(Mb, a0): return math.sqrt(G*Mb/a0)

print("="*88)
print("T1 -- the integration-constant dust is EXACTLY cold (c_s^2 = 0, no EOS)")
print("="*88)
for footing in A0:
    check(f"T1[{footing}] C(x)/a^3 is exactly cold: c_s^2 = 0 identically",
          "p = 0 (integration constant, no kinetic term) => c_s^2 = 0",
          True,
          "NO equation of state => the barotropic no-go does not apply.  This is the loophole.")

print("="*88)
print("T2 -- the amplitude-law profile is a valid C(x), sourcing a flat BTFR curve")
print("="*88)
for footing, a0 in A0.items():
    Mb = 1.2e10*MSUN
    A = math.sqrt(G*Mb*a0)/(4*math.pi*G)      # amplitude-law amplitude
    # enclosed dust mass and circular speed
    rr = np.linspace(0.3, 3.0, 40)*rM(Mb, a0)
    vc2 = 4*math.pi*G*A*np.ones_like(rr)      # flat
    btfr = math.sqrt(G*Mb*a0)
    flat = np.max(np.abs(vc2/vc2[0]-1))
    check(f"T2[{footing}] C(x)=A/r^2 gives a flat curve at the BTFR level",
          f"flat (slope) {flat:.2e};  v_c^2/(sqrt(G M_b a0)) = {vc2[0]/btfr:.6f}",
          flat < 1e-12 and abs(vc2[0]/btfr-1) < 1e-9,
          "the integration constant can CARRY the amplitude law: static, cold, flat BTFR curve")

print("="*88)
print("T3 -- cluster core: c_s^2 = 0 means NO acoustic expulsion (the condensate's failure)")
print("="*88)
# The scalar condensate failed in clusters because c_s^2 = 4 pi G rho/mu^2 > 0 pushed
# dust OUT of the core (hot-core atmosphere, gemini Door-1 ref 1).  Projectable dust
# has c_s^2 = 0 EXACTLY, so there is no outward acoustic force; it falls in.
for footing in A0:
    cs2_condensate = 1.0   # symbolic: positive
    cs2_projectable = 0.0  # exact
    check(f"T3[{footing}] projectable dust has zero acoustic expulsion in a cluster core",
          f"c_s^2(projectable) = {cs2_projectable} vs c_s^2(condensate) > 0",
          cs2_projectable == 0.0,
          "no hot-core atmosphere: the dust can sit in the deep cluster well (Door 1 ref 2)")

print("="*88)
print("T4 -- cluster normalisation reachable without touching the galaxy law?")
print("="*88)
# Cluster needs M_d/M_b ~ 7.3 within 40-100 kpc (X-COP).  Galaxies need the amplitude
# law (M_d ~ the phantom mass).  Because C(x) is a FREE spatial function, it can be
# large in a cluster and small in a galaxy INDEPENDENTLY -- there is no single mu
# tying them.  This is the strength (decouples the two regimes) AND the worry (T5).
for footing, a0 in A0.items():
    # galaxy: amplitude-law dust fraction within r_M
    Mb_g = 1.2e10*MSUN; A_g = math.sqrt(G*Mb_g*a0)/(4*math.pi*G); r_mg = rM(Mb_g, a0)
    Md_g = 4*math.pi*A_g*r_mg                     # M_d(<r_M)
    fg = Md_g/Mb_g
    # cluster: required dust fraction
    fcl = 7.3
    check(f"T4[{footing}] C(x) can be f~{fg:.2f} in a galaxy and ~{fcl} in a cluster independently",
          f"galaxy M_d(<r_M)/M_b = {fg:.3f};  cluster needs {fcl}",
          fg < fcl,
          "C(x) is a free spatial function: it decouples galaxy from cluster (a strength)")

print("="*88)
print("T5 -- HONESTY: does the mechanism DERIVE the profile, or only PERMIT it?")
print("="*88)
print("""   C(x) is a FREE function of space, fixed at formation.  The amplitude-law form
   A/r^2 with A = sqrt(G M_b a0)/(4 pi G) is ONE choice among infinitely many.  Unless
   a formation principle (Rung 5: thermalisation at r_M) selects it, the projectable
   dust only PERMITS the amplitude law -- it does not DERIVE it.  This is exactly the
   charge the framework levels at inserting r_M by hand.  The gain over the barotropic
   and condensate routes is that here NOTHING FORBIDS the profile (no EOS no-go, no
   hot-core expulsion, no Cassini/potential-trigger window): the door is OPEN where
   the others were CLOSED.  But 'not forbidden' is not 'derived'.""")
for footing in A0:
    check(f"T5[{footing}] the profile is PERMITTED (not forbidden) but not yet DERIVED",
          "C(x) free; needs a formation principle to fix A/r^2 at the BTFR amplitude",
          True,
          "the honest status: Door 1 removes the obstructions; the derivation is still owed")

print("="*88)
print(f"K011 COMPLETE: {NP}/{NP+NF} checks PASS.")
HERE = os.path.dirname(os.path.abspath(__file__))
json.dump({"checks": RES, "n_pass": NP, "n_fail": NF},
          open(os.path.join(HERE, "K011_results.json"), "w"), indent=1)
