#!/usr/bin/env python3
"""
The coefficient under the event-horizon revision: Z = 2 sqrt(8pi/3) survives; the residual is WHICH density.
==========================================================================================================
With the horizon revision (a0 ~ sqrt(rho_DE), event horizon), does the framework's coefficient Z = 2 sqrt(8pi/3)
~ 5.79 still hold, or does the revision un-pin it? Worked out here, with the honest finding that the coefficient
MAGNITUDE is unchanged and not a free parameter -- the revision only relocates the density.

THE STRUCTURE. The coefficient comes entirely from the framework's premise a0 = (c/2) sqrt(G rho):
  - rho = rho_crit = 3H^2/(8 pi G)  (total density / APPARENT horizon)  =>  a0 = (c/2) H sqrt(3/(8pi)) = cH/Z,
  - rho = rho_Lambda = OmegaL rho_crit (dark energy / EVENT horizon)      =>  a0 = (c/2) H_L sqrt(3/(8pi)) = cH_L/Z,
  with the SAME Z = 1/[ (1/2) sqrt(3/(8pi)) ] = 2 sqrt(8pi/3) ~ 5.79 in BOTH cases. So Z is fixed by the (c/2)
  sqrt(G rho) form; it is not re-opened by choosing the event horizon. The revision changes only WHICH density
  enters -- a factor sqrt(OmegaLambda) ~ 0.83 between the two.

THE NUMBERS (H0=67, OmegaLambda=0.685):
  apparent (rho_crit): a0 = cH0/Z      = 1.124e-10   (matches observed 1.2 +- 0.26)
  event    (rho_DE)  : a0 = cH_L/Z     = 0.931e-10   (~sqrt(OL) lower, ~17% below; within errors at the low end)
  geom mean          : a0 = c(H0 H_L)^0.5/Z ~ 1.02e-10
So the z=0 NORMALIZATION mildly favors rho_crit (apparent); the z-EVOLUTION (high-z disks + DESI) favors rho_DE
(event). They pull oppositely only at the sqrt(OmegaLambda) level -- small TODAY (the why-now coincidence again).

WHAT IS STILL OPEN (the genuine dictionary problem). The clean part is the FORM-given Z = 2 sqrt(8pi/3). The
(c/2) prefactor itself is NOT derived from first principles: the de Sitter temperature T_dS = hbar H_L/2pi
corresponds (Unruh-matched) to an acceleration c H_L = 4.5 a0 -- so a0 is ~5.8x BELOW the naive Unruh-matched
de Sitter acceleration, and that factor (= Z) is the dictionary between the DSSYK freezing scale and the de
Sitter temperature. The framework reasons it to ~2pi; it is not closed. The event-horizon revision does not
help or hurt this -- it is orthogonal to the prefactor.

NET (honest): the revision leaves the coefficient MAGNITUDE pinned at the clean 2 sqrt(8pi/3) and relocates the
density to rho_DE; the residual open pieces are (a) the sqrt(OmegaLambda) density ambiguity (apparent vs event
vs geometric mean -- a normalization-vs-evolution tension, small today) and (b) whether the (c/2) prefactor is
derivable from the DSSYK->de Sitter dictionary (the unchanged hard problem). No new closure; a clean structural
map of what the coefficient is and is not. Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; H0 = 67*1e3/3.086e22
Om, OL = 0.315, 0.685
a0_obs = 1.2e-10
Z = 2*np.sqrt(8*np.pi/3)


def main():
    print("#"*92)
    print("# The coefficient under the event-horizon revision -- Z = 2 sqrt(8pi/3) survives; density relocates")
    print("#"*92 + "\n")
    print(f"  Z = 2 sqrt(8pi/3) = {Z:.4f};  sqrt(OmegaLambda) = {np.sqrt(OL):.4f}\n")

    rho_crit = 3*H0**2/(8*np.pi*G); rho_L = OL*rho_crit
    HL = H0*np.sqrt(OL)
    print("="*92); print("(1) THE SAME Z FOR BOTH HORIZONS -- it follows from a0=(c/2)sqrt(G rho), not a free fit"); print("="*92)
    print(f"  {'reading':28}{'density':14}{'a0 = (c/2)sqrt(G rho)':>24}{'= c*rate/Z, Z=':>16}")
    for lab, rho, rate in [("apparent (~H0)", "rho_crit", rho_crit), ("event (~H_L)", "rho_Lambda", rho_L)]:
        rt = H0 if lab.startswith("apparent") else HL
        a0 = (c/2)*np.sqrt(G*rho)
        print(f"  {lab:28}{rho:14}{a0/1e-10:>21.3f}e-10{c*rt/a0:>16.3f}")
    a0_gm = (c/2)*np.sqrt(G*np.sqrt(rho_crit*rho_L))
    print(f"  {'geometric mean':28}{'sqrt(crit*L)':14}{a0_gm/1e-10:>21.3f}e-10{'(Z*'+f'{np.sqrt(OL)**0.5:.2f}'+' eff)':>16}")
    print(f"  observed: a0 = {a0_obs/1e-10:.2f} +- 0.26 e-10\n")

    print("="*92); print("(2) THE RESIDUAL: which density (a sqrt(OmegaLambda) ambiguity, small today)"); print("="*92)
    print(f"  apparent/rho_crit -> 1.124e-10 (best at z=0); event/rho_DE -> 0.931e-10 (best z-evolution).")
    print(f"  ratio = sqrt(OmegaLambda) = {np.sqrt(OL):.3f}. z=0 normalization mildly favors apparent; the high-z")
    print(f"  disks + DESI favor event (declining). The geometric mean (1.02e-10) threads both. This is the SAME")
    print(f"  apparent-vs-event tension seen everywhere, now in the coefficient -- a normalization-vs-evolution")
    print(f"  split at the {100*(1-np.sqrt(OL)):.0f}% level.\n")

    print("="*92); print("(3) THE UNCLOSED PIECE: the (c/2) prefactor = the DSSYK->de Sitter dictionary"); print("="*92)
    a_unruh = c*HL
    print(f"  de Sitter temperature T_dS = hbar H_L/2pi <-> Unruh-matched acceleration a = c H_L = {a_unruh/1e-10:.2f}e-10")
    print(f"  = {a_unruh/a0_obs:.1f} a0. So a0 sits a factor ~{a_unruh/a0_obs:.1f} (= Z) BELOW the naive de Sitter-Unruh accel;")
    print(f"  that factor IS Z = 2 sqrt(8pi/3) -- the dictionary between the DSSYK freezing scale and T_dS. The")
    print(f"  framework reasons it to ~2pi; it is NOT derived. The event-horizon revision is orthogonal to it.\n")

    print("="*92); print("VERDICT"); print("="*92)
    print("""  The event-horizon revision does NOT un-pin the coefficient: Z = 2 sqrt(8pi/3) ~ 5.79 follows from the
  a0=(c/2)sqrt(G rho) form and is common to the apparent and event readings; the revision only relocates the
  density from rho_crit to rho_DE (a sqrt(OmegaLambda) ~ 0.83 shift). What is left genuinely open is exactly
  what was open before: (a) which density (apparent rho_crit fits z=0 best at 1.12e-10; event rho_DE fits the
  evolution best at 0.93e-10; geometric mean threads them) -- a normalization-vs-evolution tension small today
  by the why-now coincidence; and (b) the (c/2) prefactor, i.e. the factor ~5.8 between a0 and the de Sitter-
  Unruh acceleration cH_L, which is the DSSYK->de Sitter dictionary, reasoned to ~2pi and not closed. So: no new
  closure, but a clean map -- the coefficient magnitude is fixed and clean; the residuals are the density choice
  and the unchanged dictionary prefactor. The revision tidies the EVOLUTION question without disturbing the
  coefficient.""")
    print("="*92)


if __name__ == "__main__":
    main()
