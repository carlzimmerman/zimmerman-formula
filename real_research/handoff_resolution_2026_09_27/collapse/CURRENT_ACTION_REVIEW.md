# Independent review of the conditional current action

Reviewed parent `constitutive/CURRENT_ACTION.md` and `current_action_check.py` read-only on 2026-09-27. The current variation, on-shell pressure, perfect-fluid stress tensor, constitutive identities and stated SI sound-speed ratio are correct under the displayed conventions. The document appropriately restricts the result to a local conserved-fluid realization with externally supplied material state and boundary data. It establishes neither the original complex-field theory nor a globally healthy EOS.

## Current and metric variation

Use signature (−,+,+,+), c=1, and vary the independent **contravariant vector** J^mu while rho=sqrt(−g_mu_nu J^mu J^nu). At fixed metric, partial rho/partial J^mu=−u_mu. Hence variation of L=−epsilon+J^mu A_mu gives A_mu=−epsilon_rho u_mu, where A_mu=partial_mu theta+beta partial_mu s. Since J^mu u_mu=−rho, the on-shell contraction is J^mu A_mu=rho epsilon_rho and L_on-shell=rho epsilon_rho−epsilon=P. Both signs are correct.

For metric variation with J^mu held fixed, varying the inverse metric gives

    delta rho = (rho/2) u_mu u_nu delta g^{mu nu},
    delta(sqrt(−g)L)/sqrt(−g)
        = −(rho epsilon_rho/2)u_mu u_nu delta g^{mu nu}
          −(L/2)g_mu_nu delta g^{mu nu}.

Thus T_mu_nu=rho epsilon_rho u_mu u_nu+L g_mu_nu, and **after** imposing the matter equation this becomes (epsilon+P)u_mu u_nu+P g_mu_nu. Holding a covariant current or a densitized current fixed would require a different intermediate variation. Likewise substituting L=P before metric variation while treating P as an unconstrained function is not a justified shortcut. The parent construction uses the correct independent variable and order of operations.

Theta variation supplies nabla_mu J^mu=0; beta variation supplies J^mu partial_mu s=0. The remaining label equation is J^mu partial_mu beta=−epsilon_s after using current conservation. All matter equations, including that equation, are needed for the usual on-shell diffeomorphism identity implying stress conservation. The single Clebsch pair is sufficient for the stated spherical irrotational sector; the parent's restriction concerning general vorticity is appropriate. This construction supplies an independently conserved fluid, not conversion/exchange equations tying it to another carrier sector.

## EOS and sound speed

At fixed material label, write t=sqrt(1+y), rho=(Pc/V)y/t. Then

    d rho/dy = (Pc/V)(1+y/2)/(1+y)^(3/2) > 0,
    F'(y) = (y+2)/(2y sqrt(1+y)),
    P = rho epsilon_rho−epsilon = Pc y,
    P_rho = V(1+y)^(3/2)/(1+y/2).

In SI, epsilon and P both have energy-density units (J/m³=Pa), rho is mass density, and V and e0 have units m²/s². Consequently

    h := epsilon_rho
       = c²+e0+V[2 sqrt(1+y)+log((sqrt(1+y)−1)/(sqrt(1+y)+1))],
    c_s² = c² P_rho/h,
    c_s²/c² = P_rho/epsilon_rho.

The parent's displayed ratio is dimensionally correct. P_rho is the Newtonian compressibility speed squared; it is not by itself the relativistic sound speed squared. A physical relativistic domain needs h>0 and 0≤P_rho/h≤1, as well as the appropriate energy conditions. An arbitrary e0 changes h even though it cancels from P; there is no right to remove it from a cosmological or perturbative analysis merely because the equilibrium pressure gradient is unaffected.

As y tends to zero, F(y)=1+log(y/4)+o(1) and h=c²+e0+V[2+log(y/4)+o(1)]. For every finite e0 and V>0, both epsilon/rho and h eventually become negative. Thus the statement that no finite e0 repairs this **unshifted all-density** EOS is correct. A finite healthy interval is a conditional possibility, requiring actual inequalities and a justified interface/vacuum completion; no general healthy-domain or nonlinear stability theorem was proved here.

The host relation V(s_host)=sqrt(G Mb a0)/2 remains additional initial/formation data. Current conservation advects an assigned label; it neither computes the host mass nor selects a new label after mergers. The material functions are exposed rather than eliminated by this action.

## Offset and boundary scope

Adding Pe(s) to epsilon at fixed s changes P by −Pe and contributes a vacuum-form stress −Pe g_mu_nu. The pressure gradient is unchanged only inside a uniform-s region where Pe is constant. Across varying labels or a boundary there are genuine stress/interface terms. This is not an innocuous gauge shift. Neither the value Pe nor the edge follows from the displayed bulk action, and a separately prescribed host-dependent pressure zero is not a universal EOS derivation.

## What the executable checks establish

The parent's checker exactly verifies pressure, enthalpy, cancellation of rest-energy/material integration constants, and the constant offset identity. Its logarithm-deletion mutation is meaningful: the pressure becomes Pc y²/(y+2), so the declared P=Pc y relation fails. Its code does not independently calculate the metric variation, full Euler system, sound speed, energy conditions or boundary matching; the parent prose must remain responsible for those derivations.

The independent `current_action_review_check.py` checks nine exact symbolic identities, including the derivative and low-density expansion above and metric variation at an arbitrary local Lorentz frame with an arbitrary timelike current and symmetric inverse-metric variation. All nine pass. Tensoriality extends that local-frame identity to a general metric point; it does not address global field configurations. A first symbolic comparison used structural equality for equivalent logarithms; replacing it with exact simplification resolved the serialization-level mismatch without changing any identity.

No parent source was changed. Read-only source hashes and the independent check provenance are recorded in `current_action_review_manifest.json`. The strongest warranted conclusion is the one already stated in the parent document: a local conserved matter action realizes the conditional pressure law while leaving material-state selection, energy normalization, boundaries and observational viability unresolved.
