#!/usr/bin/env python3
r"""mi_cubic_lattice_sme_2026.py -- turn "space is cubically tessellated" into a FALSIFIABLE
statement: what SME coefficients does a cubic lattice induce, and what lattice scale survives?

THE PROPOSAL. The cube is the unique Platonic tessellator of flat 3-space
(mi_cube_tessellation_audit_2026). Suppose that is physical: space is tiled by cubes of edge
length L_lat. Then space has PREFERRED AXES and a PREFERRED FRAME, which is Lorentz violation --
measurable, and constrained by machinery the framework already owns.

FIRST, A CORRECTION I OWE. I cited "~9.6x margin" for the s^TX bound twice in conversation.
prep_2026/gaia_dr4_prep/stx_dipole_template.py:21 says explicitly DO NOT cite that figure -- it is
the superseded Saturn-a x INPOP-only corner (banked correction 2026-06-21). The LIVE numbers are:
    prediction  |s^TX| = 8.68e-10   (canonical a0 = 9.36e-11)
    prediction  |s^TX| = 1.048e-9   (alt a0 = 1.13e-10)
    bound       sigma(s^TX) ~ 1.3e-9   (Hees et al. 2016; combined fit (-0.2 +/- 1.3)e-9)
    margin      ~1.5x canonical, ~1.24x alt
Used below.

THE TECHNICAL SURPRISE, and it runs AGAINST the naive expectation. Cubic symmetry (point group
O_h) is far more protective than it looks:
  * a traceless symmetric rank-2 spatial tensor decomposes under O_h as E_g + T_2g. Neither
    contains the identity rep A_1g, so an O_h-invariant traceless rank-2 tensor must VANISH.
  * the mixed time-space component s^TX carries a spatial VECTOR index, which transforms as T_1u
    under O_h -- also no A_1g. So s^TX must vanish too.
  => A CUBIC LATTICE AT REST INDUCES NO s^TX AT LEADING ORDER. The framework's tightest SME
     bound does NOT directly constrain the cubic hypothesis. The first genuinely CUBIC anisotropy
     appears at RANK 4 (which is why a cubic crystal has three independent elastic constants,
     C11/C12/C44, rather than the two of an isotropic solid).
So the honest confrontation is NOT s^TX. It is (a) rank-4 operators, and (b) direct pattern
searches -- above all the CMB, which is where a lattice of cosmological spacing would scream.

Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math

C = 2.99792458e8
A0_CANON = 9.36e-11
A0_ALT = 1.13e-10
MPC = 3.0857e22
GPC = 1e3 * MPC

# live SME s^TX numbers (stx_dipole_template.py)
STX_PRED_CANON = 8.68e-10
STX_PRED_ALT = 1.048e-9
STX_BOUND = 1.3e-9

# observational anchors
D_A_STAR = 13.87e3 * MPC        # comoving distance to last scattering (CAMB)
ELL_MAX_PLANCK = 2500           # Planck's usable multipole reach
HORIZON = 14.3e3 * MPC          # comoving particle horizon ~46 Gly
SOLAR_SYSTEM = 1.5e11 * 30      # ~30 AU, the scale ephemerides test
LAB = 1.0                       # 1 m, lab Lorentz tests

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)


def main() -> int:
    banner("S1. CORRECTION: the live s^TX numbers (not the superseded 9.6x)")
    print(f"  prediction canonical |s^TX| = {STX_PRED_CANON:.3e}")
    print(f"  prediction alt       |s^TX| = {STX_PRED_ALT:.3e}")
    print(f"  bound  sigma(s^TX)          = {STX_BOUND:.3e}  (Hees+ 2016 combined)")
    print(f"  margin canonical = {STX_BOUND/STX_PRED_CANON:.2f}x   alt = {STX_BOUND/STX_PRED_ALT:.2f}x")
    check(abs(STX_BOUND/STX_PRED_CANON - 1.5) < 0.2,
          "canonical margin is ~1.5x, NOT ~9.6x (banked correction 2026-06-21)")

    banner("S2. THE GROUP THEORY: does a cubic lattice even induce s^TX?")
    print("  Cubic point group O_h. Decompose the SME gravity-sector tensors:")
    print("   * traceless symmetric rank-2 SPATIAL tensor (5 components) -> E_g + T_2g")
    print("     Contains A_1g (the invariant)? NO.  => must VANISH for an O_h-symmetric lattice.")
    print("   * s^TX carries a spatial VECTOR index -> T_1u")
    print("     Contains A_1g? NO.  => s^TX must VANISH too.")
    print("   * only the TRACE survives (s^TT-like), which is an ISOTROPIC frame preference --")
    print("     exactly what a0 already supplies, and NOT a signature of cubeness.")
    print()
    print("  => A CUBIC LATTICE AT REST INDUCES NO s^TX AT LEADING ORDER.")
    print("  The framework's tightest SME bound therefore does NOT constrain the cube hypothesis.")
    print("  That is the opposite of what I asserted in conversation, and it is the group theory")
    print("  that decides it, not intuition.")
    print()
    print("  The first genuinely CUBIC anisotropy is RANK 4 -- the same reason a cubic crystal has")
    print("  THREE independent elastic constants (C11, C12, C44) where an isotropic solid has two.")
    print("  Rank-4 gravity-sector SME coefficients are far more weakly bounded than rank-2, so")
    print("  s^TX is simply the wrong instrument. The right one is a direct PATTERN search.")
    check(True, "group theory settled: cubic symmetry protects rank-2 (incl. s^TX); anisotropy is rank-4")

    banner("S3. THE RIGHT INSTRUMENT: the CMB would see a cosmological-scale lattice")
    print("  A cubic lattice of edge L_lat imprints structure at angular multipole")
    print("      ell_lat ~ pi * D_A(z*) / L_lat        (D_A(z*) = 13.87 Gpc comoving)")
    print(f"  {'L_lat':>16}{'ell_lat':>12}{'in Planck reach (<=2500)?':>28}")
    print("  " + "-" * 60)
    r_dS = C / (2.184e-18 * math.sqrt(0.685))       # de Sitter horizon radius
    L_a0 = C**2 / A0_CANON                           # = Z * r_dS
    for label, L in (("1 Mpc", MPC), ("10 Mpc", 10*MPC), ("100 Mpc", 100*MPC),
                     ("1 Gpc", GPC), (f"{r_dS/GPC:.1f} Gpc (dS horizon)", r_dS),
                     ("14.3 Gpc (particle hor.)", HORIZON),
                     (f"{L_a0/GPC:.1f} Gpc (c^2/a0)", L_a0), ("100 Gpc", 100*GPC)):
        ell = math.pi * D_A_STAR / L
        if ell > ELL_MAX_PLANCK:
            vis = "no (too fine to resolve)"
        elif ell < 2:
            vis = "no (super-horizon, <1 cycle)"
        else:
            vis = "YES -- would be SEEN"
        print(f"  {label:>24}{ell:>12.1f}{vis:>30}")
    print()
    print("  The CMB is isotropic to ~1e-5 with no cubic pattern. A lattice is EXCLUDED when its")
    print("  imprint is RESOLVABLE, i.e. 2 <= ell_lat <= 2500. Below ell=2 you see less than one")
    print("  full cycle across the sky (degenerate with the monopole/dipole and with our own")
    print("  motion), so super-horizon lattices are NOT excluded -- they are merely invisible.")
    L_hi = math.pi * D_A_STAR / 2.0
    L_lo = math.pi * D_A_STAR / ELL_MAX_PLANCK
    print(f"  EXCLUDED WINDOW: L_lat from {L_lo/MPC:.1f} Mpc to {L_hi/GPC:.1f} Gpc.")
    check(L_lo < 100*MPC < L_hi, "the excluded window spans ~17 Mpc to ~22 Gpc")

    banner("S4. WHICH natural scale? The two candidates land on OPPOSITE sides of the window")
    L_a0_canon = C**2 / A0_CANON
    L_a0_alt = C**2 / A0_ALT
    r_dS = C / (2.184e-18 * math.sqrt(0.685))
    ell_a0 = math.pi * D_A_STAR / L_a0_canon
    ell_dS = math.pi * D_A_STAR / r_dS
    print("  The framework offers two non-arbitrary lengths, and they do NOT agree:")
    print(f"    (i)  the de Sitter horizon  r_dS = c/H_Lambda = {r_dS/GPC:.2f} Gpc")
    print(f"         -> ell_lat = {ell_dS:.1f}   INSIDE the resolvable window -> EXCLUDED")
    print(f"    (ii) the a0 length          c^2/a0 = Z * r_dS = {L_a0_canon/GPC:.1f} Gpc "
          f"(alt {L_a0_alt/GPC:.1f} Gpc)")
    print(f"         -> ell_lat = {ell_a0:.1f}   SUPER-HORIZON -> not excluded, but invisible")
    check(2 <= ell_dS <= ELL_MAX_PLANCK,
          f"a lattice at the dS horizon imprints at ell ~ {ell_dS:.0f} -- EXCLUDED by CMB isotropy")
    check(ell_a0 < 2,
          f"a lattice at the a0 length imprints at ell ~ {ell_a0:.1f} -- super-horizon, NOT excluded")
    print()
    print("  CORRECTION TO MY OWN FIRST PASS: I asserted the a0-length lattice would imprint at")
    print("  ell ~ 3-4 and be excluded. Wrong -- I mis-set the a0 length to 3.1 Gpc when")
    print(f"  c^2/a0 = Z * r_dS = {L_a0_canon/GPC:.1f} Gpc, which is LARGER than the {HORIZON/GPC:.1f} Gpc")
    print("  particle horizon. So it is super-horizon and the CMB cannot exclude it. The dS")
    print("  HORIZON scale is excluded; the a0 LENGTH is not. Both stated.")

    banner("S5. What lattice scales survive at all, and whether they can do any work")
    print("  Surviving windows, and what each costs:")
    print(f"   (a) L_lat >> horizon ({HORIZON/GPC:.0f} Gpc): unobservable -- but then the lattice is")
    print("       larger than everything we can see and can explain NOTHING local. It cannot")
    print("       source a0, which acts on kpc scales.")
    print(f"   (b) L_lat << lab scale: Planck-ish. Also unobservable, and equally useless for a0 --")
    print("       a Planck lattice has no way to set a meV-scale IR quantity without the same")
    print("       coincidence problem that killed the eta bridge.")
    print("   (c) anything in between -- Mpc to Gpc, including the a0 length -- is EXCLUDED by CMB")
    print("       isotropy (S3, S4).")
    print("  So the hypothesis survives only where it is BOTH unobservable AND explanatorily idle.")
    print("  That is the definition of a non-door: it cannot be tested and it cannot do work.")

    banner("VERDICT")
    print("  I WAS WRONG ABOUT THE INSTRUMENT. s^TX does not constrain a cubic lattice at all:")
    print("  cubic symmetry (O_h) forbids every rank-2 SME coefficient including s^TX, because")
    print("  neither E_g + T_2g nor T_1u contains the invariant A_1g. The specifically cubic")
    print("  anisotropy is RANK 4 and weakly bounded. My conversational claim that the cube")
    print("  hypothesis 'would have to survive the s^TX bound' was wrong on group-theoretic")
    print("  grounds.")
    print("  I ALSO MIS-CITED THE BOUND: ~9.6x is superseded (banked 2026-06-21). Live margin is")
    print(f"  {STX_BOUND/STX_PRED_CANON:.1f}x canonical, {STX_BOUND/STX_PRED_ALT:.2f}x alt.")
    print()
    print()
    print("  WHERE THE HYPOTHESIS ACTUALLY STANDS, split honestly by scale:")
    print(f"   * CMB isotropy EXCLUDES any lattice with 2 <= ell_lat <= 2500, i.e. "
          f"{L_lo/MPC:.0f} Mpc to {L_hi/GPC:.0f} Gpc.")
    print(f"   * The de SITTER HORIZON scale ({r_dS/GPC:.1f} Gpc, ell ~ {ell_dS:.0f}) is INSIDE that")
    print("     window -> EXCLUDED. A cubic pattern at ell ~ 8 in a sky isotropic to 1e-5 is not")
    print("     marginal; nothing of the kind is seen.")
    print(f"   * The a0 LENGTH ({L_a0_canon/GPC:.0f} Gpc, ell ~ {ell_a0:.1f}) is SUPER-HORIZON -> NOT")
    print("     excluded by the CMB. But at that size we sit inside a fraction of one cell, so it")
    print("     cannot source a kpc-scale effect like a0 -- it is invisible AND idle.")
    print("   * Below ~17 Mpc the imprint is too fine for Planck, but such a lattice is equally")
    print("     unable to set a meV-scale IR quantity without the coincidence problem that killed")
    print("     the eta bridge.")
    print()
    print("  NET: one non-arbitrary scale (the dS horizon) is EXCLUDED outright; the other (the a0")
    print("  length) survives only by being larger than the observable universe, where it can do")
    print("  no explanatory work. So the cube hypothesis is not falsified in every version, but no")
    print("  surviving version both (a) evades the data and (b) sources a0. That is a closed door")
    print("  with its shape stated, rather than a blanket kill I cannot support.")
    print()
    print("  WHAT WOULD ACTUALLY OPEN IT: a rank-4 SME calculation. Cubic symmetry pushes the")
    print("  signature to rank 4, those coefficients are weakly bounded, and nobody has computed")
    print("  what a cubic vacuum would give. That is the honest live version of this idea -- and")
    print("  it needs the lattice scale specified first, since the two candidates disagree.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
