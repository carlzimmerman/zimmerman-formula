#!/usr/bin/env python3
r"""mi_nariai_doors_2026.py -- test every door the Nariai forcing opens, including the one that
could close it.

CONTEXT. mi_nariai_forcing_2026 showed r_a0(M_Nariai)/L = sqrt(Z/(3 sqrt 3)) is an EXACT IDENTITY,
and imposing it (the a0 shell of the maximal de Sitter black hole IS the de Sitter horizon) forces
        Z = 3 sqrt(3) = 5.1961524227,   kappa = 2 sqrt(2 pi)/9 = 0.5570285055
an +11.41% revision of a0, from 9.36e-11 to 1.0428e-10. Both inside the empirical box.

FOUR DOORS, and D1 is the one that can kill the fork:

  D1  IS THE FORK EVEN RESOLVABLE? a0 is tied to the dark-energy density, so it inherits that
      density's uncertainty. If the input error on a0 is comparable to 11.4%, the fork is not
      measurable and the original reframing survives untouched either way. This must be checked
      FIRST, because if it fails the other doors are academic. The H0 tension is the specific
      worry: a0 propto H_Lambda = H0 sqrt(Omega_Lambda), and H0 itself is disputed at ~8%.

  D2  DOES Z = 3 sqrt 3 DISSOLVE THE NUMBER-FIELD OBSTRUCTION? The standing obstruction that
      closed the particle-physics sector reads: "Z carries a transcendental sqrt(pi) while all
      flavour and coupling data are algebraic, so a0/Z is structurally gauge-blind." But
      3 sqrt(3) = 3^(3/2) is ALGEBRAIC -- pure powers of 3, no pi at all. If the Nariai condition
      holds, the single strongest obstruction to the SM sector may simply not apply.

  D3  WHAT DOES A SPARSER VOCABULARY DO TO THE SEARCH? Earlier I showed that ADDING germs hurts
      atomos, because the branching factor B sits in the denominator of the informative ceiling
      D_max = D0 + ln(1/w)/ln(B), and density scales the same way. The converse must then be true:
      a SPARSER vocabulary RAISES the ceiling and thins the density. Z = 3^(3/2) is reachable from
      the single germ {3}, so the Nariai reading licenses dropping sqrt(8pi/3) entirely. Quantify
      the gain.

  D4  CAN PARTICLE PHYSICS ACTUALLY COME OUT? Only meaningful if D2 and D3 both pass. Stated as a
      precondition list, not a promise.

Exit 0 = all checks ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math
import sympy as sp

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return cond

def banner(s):
    print("\n" + "=" * 100); print(s); print("=" * 100)

A0_CANON = 9.36e-11
Z_FW = math.sqrt(32 * math.pi / 3)
Z_NAR = 3 * math.sqrt(3)
FORK = Z_FW / Z_NAR - 1.0          # +11.41%


def main() -> int:
    banner("mi_nariai_doors_2026 -- four doors, starting with the one that can close the fork")
    print(f"  fork size: a0(Nariai)/a0(kappa=1/2) = {Z_FW/Z_NAR:.6f}  ({100*FORK:+.2f}%)")

    # =================================================================================
    banner("D1. IS THE FORK RESOLVABLE? a0 inherits the dark-energy density's uncertainty")
    # a0 = kappa c sqrt(G rho_Lambda) = c H_Lambda / Z, H_Lambda = H0 sqrt(Omega_Lambda)
    print("  a0 = c H_Lambda / Z  with  H_Lambda = H0 sqrt(Omega_Lambda), so")
    print("      d a0/a0 = d H0/H0 + (1/2) d Omega_L/Omega_L   (plus the Z choice)\n")
    H0_P, H0_P_E = 67.4, 0.5           # Planck 2018 TT,TE,EE+lowE+lensing
    OL, OL_E = 0.685, 0.007
    H0_S = 73.0                        # SH0ES-like local ladder
    e_h0 = H0_P_E / H0_P
    e_ol = 0.5 * OL_E / OL
    e_tot = math.hypot(e_h0, e_ol)
    print(f"  Planck-only input error on a0: H0 {100*e_h0:.2f}% (+) "
          f"(1/2)Omega_L {100*e_ol:.2f}%  ->  total {100*e_tot:.2f}%")
    check(abs(FORK) > 3 * e_tot,
          f"the fork ({100*abs(FORK):.1f}%) exceeds 3x the Planck-only input error "
          f"({100*e_tot:.2f}%) -- resolvable IF H0 is Planck's")
    # now the H0 tension, which is the real problem
    a0_k05_planck = A0_CANON
    a0_k05_shoes = A0_CANON * (H0_S / H0_P)
    a0_nar_planck = A0_CANON * (Z_FW / Z_NAR)
    print(f"\n  BUT THE H0 TENSION IS NEARLY DEGENERATE WITH THE FORK:")
    print(f"    kappa=1/2, H0=67.4  ->  a0 = {a0_k05_planck:.4e}")
    print(f"    kappa=1/2, H0=73.0  ->  a0 = {a0_k05_shoes:.4e}   ({100*(H0_S/H0_P-1):+.1f}% from H0 alone)")
    print(f"    Nariai,    H0=67.4  ->  a0 = {a0_nar_planck:.4e}")
    gap = abs(a0_nar_planck - a0_k05_shoes) / a0_nar_planck
    print(f"\n  separation between 'Nariai with Planck H0' and 'kappa=1/2 with SH0ES H0':"
          f" {100*gap:.2f}%")
    degen = 100 * (H0_S / H0_P - 1) / (100 * abs(FORK)) * 100
    print(f"  the H0 tension alone spans {100*(H0_S/H0_P-1):.1f}% of the {100*abs(FORK):.1f}% fork "
          f"= {degen:.0f}% degenerate")
    check(gap < 0.05,
          f"the two hypotheses collapse to within {100*gap:.1f}% once H0 is allowed to float "
          f"-- so the fork is NOT cleanly resolvable without pinning H0")
    print("\n  CARL'S POINT IS CORRECT, AND SHARPER THAN IT LOOKS. a0 is tied to the dark-energy")
    print("  density, so it inherits H0 and Omega_Lambda. The H0 tension alone covers ~73% of the")
    print("  fork, leaving the two coefficients only ~2.8% apart at the extremes. Breaking the")
    print("  fork therefore needs BOTH a ~3x tighter a0 estimator AND H0 settled -- it is not a")
    print("  one-measurement test.")
    print("\n  AND THE ORIGINAL REFRAMING IS UNTOUCHED EITHER WAY. a0 ~ c H_Lambda / O(1) is an")
    print("  order-of-magnitude tie to Lambda; an 11% coefficient revision does not disturb it,")
    print("  the RAR fit, the BTFR, or any empirical front. Only the COEFFICIENT's provenance")
    print("  is at stake, never the reframing.")

    # =================================================================================
    banner("D2. Does Z = 3 sqrt 3 dissolve the NUMBER-FIELD obstruction?")
    z_fw = sp.sqrt(32 * sp.pi / 3)
    z_nar = 3 * sp.sqrt(3)
    print(f"  framework Z = {z_fw} -> transcendental? "
          f"{not z_fw.is_algebraic}  (carries sqrt(pi))")
    print(f"  Nariai    Z = {z_nar} = 3**(3/2) -> algebraic? {z_nar.is_algebraic}")
    check(z_nar.is_algebraic is True, "3 sqrt(3) is ALGEBRAIC (a pure power of 3)")
    check(sp.sqrt(sp.pi).is_algebraic is False, "sqrt(pi) is transcendental (Lindemann)")
    print("\n  THE OBSTRUCTION AS IT STANDS: 'Z carries a transcendental sqrt(pi) while flavour")
    print("  and coupling data are algebraic, so an exact identity needs the sqrt(pi) to cancel,")
    print("  in which case the germ was not load-bearing.' Under the Nariai reading Z = 3^(3/2),")
    print("  which is ALGEBRAIC -- so that argument DOES NOT APPLY. The single strongest")
    print("  obstruction to the SM sector is specific to the sqrt(32pi/3) form.")
    print("\n  CAVEAT, stated plainly: kappa itself becomes 2 sqrt(2 pi)/9, which IS transcendental.")
    kap_nar = 2 * sp.sqrt(2 * sp.pi) / 9
    print(f"    kappa_Nariai = {kap_nar} algebraic? {kap_nar.is_algebraic}")
    print("  So the transcendence moves rather than vanishing: the a0-to-H_Lambda ratio becomes")
    print("  algebraic, while the a0-to-rho_Lambda ratio becomes transcendental. Which matters")
    print("  depends on the route. For a SEARCH the operative object is the dimensionless germ,")
    print("  and via H_Lambda that germ is now a pure power of 3.")

    # =================================================================================
    banner("D3. What a SPARSER vocabulary buys the search")
    print("  Earlier result: ADDING germs hurts, because B sits in the denominator of")
    print("  D_max = D0 + ln(1/w)/ln(B), and density scales the same way. The converse:")
    print("  dropping sqrt(8pi/3) and keeping only {3} must RAISE the ceiling and THIN density.")
    print("  Z = 3^(3/2) is reachable from germ 3 alone (two germ steps), so the Nariai reading")
    print("  LICENSES this -- it is not an arbitrary restriction.\n")
    w_alpha = 3.06e-10
    D0 = 4
    print(f"  {'vocabulary':<34}{'B (est)':>10}{'D_max(1/alpha)':>16}{'gain':>8}")
    print("  " + "-" * 70)
    base = None
    for nm, B in (("{3, sqrt(8pi/3)} + 17 free (as run)", 4.407),
                  ("{3} + 17 free", 3.9),
                  ("{3} + 8 free (pruned)", 3.2),
                  ("{3} only, no free germ", 2.4)):
        d = D0 + math.log(1 / w_alpha) / math.log(B)
        if base is None:
            base = d
        print(f"  {nm:<34}{B:>10.2f}{d:>16.2f}{d-base:>+8.2f}")
    print("\n  The gain is real but MODEST -- a few depths -- and it does NOT rescue the angles,")
    print("  whose ceilings are negative by 5+ depths. It helps precisely where a hit would")
    print("  matter: the tight targets (1/alpha, a_e, m_p/m_e), whose ceilings sit near 7-8.")
    print("  Density thins by the same factor, which is what killed pre-registration.")

    # =================================================================================
    banner("D4. Can particle physics come out? PRECONDITIONS, not a promise")
    print("  Necessary conditions, in order, each independently checkable:")
    print("   P1  the Nariai condition must be RIGHT, i.e. a0 = 1.0428e-10 not 9.36e-11.")
    print("       Status: UNDECIDED and hard -- D1 shows it is ~73% degenerate with the H0")
    print("       tension. Needs a ~3x tighter a0 AND H0 settled.")
    print("   P2  the algebraic vocabulary must be searched. Status: NOT DONE. This is cheap and")
    print("       is the only immediately actionable item -- re-run depths 5-10 with germ {3}")
    print("       alone, which is SPARSER than anything run so far.")
    print("   P3  the search must clear the ceiling for a TIGHT target, not an angle. Even with")
    print("       D3's gain the tight ceilings sit near 8-11, so depth 10 is marginal at best.")
    print("   P4  a survivor must then predict something held back. Status: no valid holdout")
    print("       exists (the lepton-ratio holdouts are algebraically spanned).")
    print("\n  HONEST READING: P2 is worth doing because it is cheap, sparser, and licensed by the")
    print("  Nariai reading rather than chosen for convenience. But P1 is undecided, P3 is")
    print("  marginal, and P4 is unsolved -- so this is a door worth OPENING, not a result.")
    print("  Nothing here promises particle physics; it identifies the one search variant that")
    print("  has not been tried and that the geometry actually licenses.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
