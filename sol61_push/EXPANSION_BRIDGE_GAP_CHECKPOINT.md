# Gapped cubic: saved algebraic checkpoint

Status: conditional reduced-force repair and a minimal-model obstruction. The exact 32π coefficient remains unresolved. This checkpoint preserves the latest route before a broader source/dynamics audit.

Let p* > 0 and replace the polarization cubic by

W(P) = M²P² + C[(P²+p*²)^(3/2) − p*³], C = βM²/(3H), a0,b = 2H/β.

In the previously derived frozen-expansion weak-field reduction, polarization variation gives

g = P + P√(P²+p*²)/a0,b; b = g−P.

The flux derivative is (2P²+p*²)/(a0,b√(P²+p*²)) > 0. At P→0, g/b→1+a0,b/p*: the center becomes Newtonian in this reduced relation. A finite MOND window requires p* ≪ P ≪ a0,b. This is not strict infrared MOND, and is not a proof that a conserved-source solution exists. The subtracted operator vanishes at P=0 and therefore retains the independently chosen vacuum energy and coefficient freedom.

## Can the same operator generate the vacuum?

Test the specific alternative −βM²(P²+p*²)^(3/2)/Θ, without the subtraction and without independent U. In homogeneous vacuum Θ=3H, H=adot/(Na), S=3λ−1. Its minisuperspace Lagrangian is

L = −A a adot²/N − B N² a⁴/adot,
A = (3/2)M²S, B = βM²p*³/3.

Varying the lapse at fixed adot gives AH²−2B/H=0. The constant-H scale-factor equation gives the same condition. The factor two is essential: Θ depends on the lapse; this term is not a constant cosmological energy.

Consequently H³=4βp*³/(9S). With δ=p*/a0,b and Cb=Λ/a0,b²=3β²/4 (c=1),

δ³ = (3S/8) Cb.

For the λ>1 branch, S>2. Imposing the formal target Cb=32π therefore requires δ>(24π)^(1/3)≈4.225, eliminating the required MOND window. Even δ<1 requires Cb<8/(3S)<4/3. Here a0,b is a bare action coefficient; when the MOND window is absent it cannot be identified with an observed galaxy acceleration scale.

This excludes this minimal self-sourcing gapped operator as a joint explanation of the requested vacuum and MOND scales. It does not exclude additional operators, counterterms, other vacuum mechanisms, or other theories. The subtracted repair remains a candidate with independent vacuum input, not a solution of 32π.

## Evidence and next step

`expansion_bridge_gap_checkpoint.py` checks eight exact symbolic identities: force variation, flux derivative and limits, lapse variation, constant-H scale equation, vacuum relation, and joint coefficient relation. Its output is saved in `expansion_bridge_gap_checkpoint_results.json`. No finite computation is claimed as a full-theory proof. No global novelty claim is made.

The useful next step is to identify a physically protected vacuum mechanism and coefficient selector compatible with a small gap, then solve the conserved-source boundary problem and audit dynamics. The proposed microscopic Dirac interpretation and gap-dependent scalar health have not yet been audited and are not asserted here.
