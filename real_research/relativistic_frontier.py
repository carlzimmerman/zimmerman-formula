#!/usr/bin/env python3
"""
The hard frontier: can a relativistic MOND theory carry an EVOLVING a0 = cH(z)/Z?
=================================================================================

This is the boundary I have drawn honestly all along: the premise is non-relativistic
(MOND + Friedmann), so lensing and the CMB acoustic peaks lie OUTSIDE it -- they need a
covariant completion. The one relativistic MOND theory that fits the CMB is AeST (Aether-
Scalar-Tensor; Skordis & Zlosnik, PRL 127, 161302, 2021). So the sharp question is:

    does a covariant MOND theory ACCOMMODATE a0 ~ E(z), or does it FORBID it?

The answer is more interesting than either: vanilla AeST and the premise make DIFFERENT,
data-distinguishable predictions, and the a0(z) data already discriminates between them.

DISCIPLINE FOR THIS FILE (this is where overreach historically crept in):
  [COMPUTED]    arithmetic done here, reproducible.
  [KNOWN]       established facts about AeST (cited), not derived here.
  [PROPOSAL]    a constructive suggestion -- explicitly NOT a theorem.
  [OPEN]        a real calculation I do NOT do (and will not fake): flagged as the next task.
I scope what is required and forbidden; I do NOT claim a CMB fit I have not computed.

Run:  python real_research/relativistic_frontier.py
"""

import math

c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
Z = 2 * math.sqrt(8 * math.pi / 3)
OM, OL = 0.315, 0.685
H0 = 67.4 * 1e3 / MPC
A0 = 1.20e-10


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


# ====================================================================================
def part1_question():
    print("#" * 84)
    print("# PART 1 -- the question, and why it is the boundary")
    print("#" * 84)
    print("   The premise a0=(c/2)sqrt(G rho_c)=cH/Z is NON-relativistic: MOND in the weak")
    print("   field + Friedmann for rho_c(z). Strong lensing and the CMB peaks need a covariant")
    print("   theory. The only relativistic MOND that fits the CMB is AeST (Skordis-Zlosnik")
    print("   2021): metric g, a unit-timelike vector A (the 'aether'), and a scalar phi.")
    print("   Question: does AeST accommodate an EVOLVING a0 ~ E(z), or forbid it?\n")


# ====================================================================================
def part2_two_readings():
    print("#" * 84)
    print("# PART 2 [COMPUTED] two readings of the MOND scale -- the data tells them apart")
    print("#" * 84)
    print("   The MOND scale has TWO natural cosmological origins, degenerate now, not later:")
    print("     (i)  a0 ~ sqrt(Lambda)       (de Sitter / cosmological constant) -> CONSTANT (p=0)")
    print("     (ii) a0 ~ sqrt(rho_total) ~ H (THE PREMISE, total density)        -> EVOLVING (p=1)")
    sOL = math.sqrt(OL)
    print(f"   today they agree to {(1/sOL-1)*100:.0f}% (the de Sitter floor, edge E4: a0_floor={sOL:.3f} a0).")
    print("   at high z they SEPARATE -- and a0(z) data picks the winner:")
    print(f"   {'z':>5}{'premise 1.20 E(z)':>19}{'Lambda-reading (const)':>24}{'measured':>14}")
    meas = {0.0: "1.20 SPARC", 0.05: "1.69 Varast", 0.9: "2.38 MUSE-DK"}
    for z in (0.0, 0.05, 0.9, 2.0, 6.0):
        pr, lam = A0 * E(z), A0 * sOL
        print(f"   {z:>5}{pr*1e10:>19.2f}{lam*1e10:>24.2f}{meas.get(z,'-'):>14}")
    print("   the measured a0 RISES (tracks premise, ii); the Lambda-reading (i) is FLAT.")
    print("   constant a0 = p=0 was rejected at 5sigma (a0_powerlaw_confrontation.py). So the")
    print("   pure de Sitter / sqrt(Lambda) origin -- the DEFAULT of relativistic MOND -- is")
    print("   the disfavoured one. The data leans to the premise's total-density reading.")
    print("   [CAVEAT, inherited from the p-fit: small heterogeneous samples + a 1.7sigma local")
    print("   anchor tension; and an evolving RAR is ALSO expected in LCDM from halo evolution.")
    print("   So this DISTINGUISHES constant vs evolving a0 -- it does not by itself PROVE the")
    print("   premise, nor by itself KILL vanilla AeST. It is a live discriminator, not a verdict.]\n")


# ====================================================================================
def part3_aest():
    print("#" * 84)
    print("# PART 3 [KNOWN] what AeST is, and what it gives for a0")
    print("#" * 84)
    print("   AeST (Skordis-Zlosnik 2021), established facts (NOT derived here):")
    print("    * fields: metric + unit-timelike aether A_mu + scalar phi; shift-symmetric.")
    print("    * it REPRODUCES the CMB and matter power spectrum at LCDM level -- the first")
    print("      relativistic MOND to do so (TeVeS failed the 3rd peak).")
    print("    * gravitational waves travel at c (consistent with GW170817).")
    print("    * quasi-static weak field -> MOND, with a0 set by the free function's")
    print("      parameters -- i.e. AS CONSTRUCTED, a0 is a CONSTANT (standard MOND).")
    print()
    print("   Consequence: vanilla AeST sits on the p=0 (constant-a0) side of Part 2 -- the")
    print("   side the a0(z) data now disfavours at 5sigma. So the premise is NOT 'derived")
    print("   from' AeST; it is a SHARPER, different claim (a0 must track H, not be fixed).\n")


# ====================================================================================
def part4_aether_home():
    print("#" * 84)
    print("# PART 4 [PROPOSAL] the natural relativistic home for an evolving a0")
    print("#" * 84)
    print("   The premise needs LOCAL galaxy dynamics to 'know' the GLOBAL H(z) -- a Machian,")
    print("   non-local-looking requirement. An aether theory supplies exactly this, locally:")
    theta0 = 3 * H0
    print("     the aether expansion theta = div_mu A^mu is a LOCAL field; in FRW its")
    print(f"     background value is theta = 3H. So a0 ~ c*theta/(3Z) gives a0 = cH/Z:")
    print(f"       c*theta_0/(3Z) = {c*theta0/(3*Z):.3e}   vs   cH0/Z = {c*H0/Z:.3e}  [equal]")
    print("   Coupling the MOND scale to the aether EXPANSION (not to Lambda) makes a0 inherit")
    print("   H(z) through a local field -- the Machian channel, with no action-at-a-distance.")
    print("   a0 becomes a slowly-varying, background-dependent quantity (a 'running a0'),")
    print("   reducing to the standard value cH0/Z today and rising as E(z) into the past.")
    print("   [PROPOSAL, not theorem] this is a structural route, not a worked solution.\n")


# ====================================================================================
def part5_requires_forbids():
    print("#" * 84)
    print("# PART 5 the honest ledger: what this REQUIRES, FORBIDS, and CANNOT yet claim")
    print("#" * 84)
    print("   REQUIRES [from the data]:")
    print("    * the covariant theory's effective a0 must couple to the EVOLVING background")
    print("      (aether expansion theta = 3H), giving p ~ 1 -- not to Lambda alone.")
    print("   FORBIDS [data-excluded]:")
    print("    * a0 ~ sqrt(Lambda) = const (p=0): rejected at 5sigma. The pure de Sitter")
    print("      origin, and vanilla constant-a0 AeST, are on the wrong side.")
    print("   CANNOT YET CLAIM [OPEN -- the real calculation, not faked here]:")
    print("    * that a theta-coupled AeST variant STILL fits the CMB. Making a0 background-")
    print("      dependent modifies the scalar sector's perturbations; whether the 3rd-peak")
    print("      / matter-power success survives is a full Boltzmann calculation with the")
    print("      paper's free function K(Y) -- NOT reconstructable from memory, NOT done here.")
    print("    * that the theta-coupling is ghost-free / stable. Also an OPEN field-theory check.\n")


# ====================================================================================
def verdict():
    print("#" * 84)
    print("# VERDICT -- the frontier, scoped honestly")
    print("#" * 84)
    print("  1. The premise is NOT a corollary of AeST; it is a SHARPER claim. Vanilla AeST")
    print("     gives constant a0; the premise gives a0 ~ E(z). They differ observably.")
    print("  2. The a0(z) data already DISCRIMINATES, and leans to the premise: constant a0")
    print("     (the de Sitter / vanilla-AeST default) is out at 5sigma; p ~ 0.8 favours")
    print("     evolving. So this is a live test BETWEEN relativistic-MOND variants, now.")
    print("  3. The premise has a natural covariant home: couple a0 to the aether expansion")
    print("     theta = 3H (a local field), not to Lambda. That realises a0 ~ H(z) Machian-ly.")
    print("  4. The decisive OPEN task -- the honest next frontier -- is the CMB consistency")
    print("     of theta-coupled AeST. I scope it; I do not fake it. If it fits the peaks with")
    print("     a0 ~ E(z), the premise becomes a full relativistic theory. If it cannot, the")
    print("     premise stays a successful non-relativistic law with a known relativistic gap.")
    print()
    print("  Boundary held: no lensing prediction, no CMB fit claimed. What IS new here is")
    print("  that the boundary is now a SHARP, data-tested fork, not a vague 'needs more work'.")


def main():
    part1_question()
    part2_two_readings()
    part3_aest()
    part4_aether_home()
    part5_requires_forbids()
    verdict()


if __name__ == "__main__":
    main()
