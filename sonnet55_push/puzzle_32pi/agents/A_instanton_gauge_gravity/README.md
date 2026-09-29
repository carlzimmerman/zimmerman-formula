# Lane A: Yang-Mills instantons, topological charge, gauge formulations of gravity

## Bottom line
**Verdict: SHARP NO-GO (scoped), with one useful cross-check. NOTHING NEW as a derivation of the factor 1/2 (32 pi); kappa = 1/2 stays FITTED.**
1. The a0 relation is classical: a0^2 = c^4 Lambda/(32 pi) contains no G and no hbar (Pi_1 = 1/(32 pi)), while every instanton / gauge-gravity quantity is a function of Pi_2 = hbar G Lambda / c^3 ~ 3e-122 alone
   (g^2 = (16 pi/3) Pi_2, 8 pi^2/g^2 = S_dS/2, quantisation level K = 3/(4 Pi_2)). A quantisation condition (k integer, CS level, theta-sector) fixes Lambda in Planck units; it can never reach Pi_1.
   Any g-dependent contribution to Pi_1 is excluded by 10^60 to 10^240 (or e^(-1e122)); only a Pi_2-independent pure number could enter, i.e. a coefficient, not a quantisation.
2. The MacDowell-Mansouri dS action is entirely the Euler term (its SO(5) field strength vanishes on S^4): S_dS = chi (8 pi^2/g^2) with chi = 2 and 1/g^2 = L^2/(16 pi hbar G). The hbar-free ratio is chi = 2; the puzzle's ratio S_a0/(instanton action) = Z^2/2 = 16 pi/3 is irrational, i.e. it is the puzzle, not a consequence of the gauge structure.
3. Nothing with a scale selects a0: the k = 1 moduli space has a unique SO(5)-invariant point (size = L, the spin-connection instanton), no other special locus (rho = Z, Z L are not marked); the a0-Rindler cone contributes 32 pi^2 * 2(1 - Z) to the Euler integral (an integer number of instanton units only for half-integer Z); the only free length in gravitational topological terms is the Gauss-Bonnet alpha (free, not derived); the MM radius is forced to L.
4. Where the 1/2 can live, narrowed: NOT in any instanton number, CS level, theta-vacuum, moduli selection, or conical-defect count. It is a classical, hbar-free coefficient (agrees with the record's section 4 finding of no thermal 2 pi).

## What was done (5 scripts, 98 checks, all pass; every claim has a control that fails when it should)
| script | content | pass |
|---|---|---|
| `a01_mm_coupling.py` | MM SO(5) form; F_MM = 0 on S^4; eps F F = E4 - (4/L^2)(R - 6/L^2) (400 random curvature tensors); SU(2)+ x SU(2)- split; coupling; ratios | 21/21 |
| `a02_classicality_theorem.py` | Buckingham-pi theorem: Pi_1 vs Pi_2; power laws / instanton weights excluded; quantisation lattice density; a0 = (1/2) c sqrt(G rho) leaves Pi_1 independent of rho | 22/22 |
| `a03_moduli_k1.py` | k = 1 moduli space on S^4: T_mn = 0, unique SO(5)-invariant point, exact L^2-metric along the diameter and at the centre | 23/23 |
| `a04_cone_euler.py` | Euclidean dS cone with period 2 pi Z L: Euler/Pontryagin/EH contributions as functions of Z, tip smoothing, total-derivative structure | 16/16 |
| `a05_gravity_topological_terms.py` | MM with independent radius, Euler number as Lambda^2 V_4, Nieh-Yan inertness, Eguchi-Hanson size modulus, Kodama level | 16/16 |
Outputs are the `.out` files next to the scripts.

## (1) MacDowell-Mansouri: the coupling, the ratio, and the structural theorem
**Computed (`a01`).** With F^{ab} = R^{ab} - e^a e^b/ell^2 (the SO(4) block of the SO(5) curvature, torsion zero), the pointwise identity eps_{abcd}F^{ab}F^{cd}/vol = E4 - (4/ell^2)(R - 6/ell^2) holds
on 400 random algebraic curvature tensors, so (R - 2 Lambda) vol = (L^2/4)(eps R R - eps F F) with Lambda = 3/L^2, and the Euclidean EH action is
I = -(L^2/(64 pi G)) (Int eps R R - Int eps F F). On S^4, R^{ab} = e^a e^b/L^2 for all 256 components, so F = 0: the dS instanton is a *flat* SO(5) connection and the whole on-shell action, -pi L^2/G = -S_dS,
is the topological term (Int eps R R = 64 pi^2 = 32 pi^2 chi). The chiral split is exact: eps F F = 2(G_+^i G_+^i - G_-^i G_-^i), G_pm = (1/2)eps F^{jk} pm F^{i4}; on S^4 the spin-connection curvatures
(checked to equal F(A_pm) of p10, all 96 components) are BPST 2-forms, each integrating to 16 pi^2 (k = 1), so Int eps R R = 2(16 pi^2 + 16 pi^2). Matching to a YM-normalised action 8 pi^2 k/g^2:

    1/g^2 = L^2/(16 pi hbar G),   8 pi^2/g^2 = pi L^2/(2 hbar G) = S_dS/2,   g^2 = (16 pi/3) hbar G Lambda.

**Convention-independent, hbar-free ratios.** S_dS/(instanton action) = chi = 2 (any L, G, hbar). S_a0/(instanton action) = Z^2/2 = 16 pi/3 for the puzzle's Schwarzschild horizon (area pi/a0^2), equivalently S_a0/S_dS = 8 pi/3.
Rational normalisation conventions cannot rescue this: the ratio is irrational (Lindemann). The pi is the puzzle's own pi (Lambda = 32 pi a0^2), not produced by the gauge structure.
**The coupling g itself is hbar-full** (g^2 ~ hbar G Lambda), the a0 relation is not.

**Theorem (scoped; `a02`, 22/22).** Quantities (a0, Lambda, G, hbar, c) have exactly two dimensionless groups, Pi_1 = a0^2/(c^4 Lambda) and Pi_2 = hbar G Lambda/c^3, and only Pi_2 contains hbar.
The puzzle is Pi_1 = 1/(32 pi); all instanton data (g^2, 8 pi^2/g^2 = 3 pi/(2 Pi_2), S_dS = 3 pi/Pi_2, the CS level) are functions of Pi_2 and integers.
(a) With the observed Pi_2 ~ 3e-122 and Pi_1 ~ 1e-2, a contribution Pi_1 = C Pi_2^p needs |p| < 0.05 unless C is tuned (p = 1/2 needs C ~ 10^59, p = 1: 10^120, p = 2: 10^241); an instanton weight e^(-8 pi^2 k/g^2) = exp(-1.6e122 k) is zero. The control shows the argument uses the smallness of Pi_2 (at Pi_2 = 0.3 nothing is excluded).
(b) So the only admissible instanton content is a Pi_2-independent pure number (32 pi^2 chi etc.): a coefficient. A quantisation k in Z acts on 1/g^2 and thus fixes Pi_2 = 3 pi/(2k): Lambda in Planck units.
(c) Integer quantisation of both S_dS and S_a0 gives Pi_1 = M/(12 N), rational, but the lattice is ~1e-122 dense (a rational with denominator ~1e60 approximates 1/(32 pi) to 6e-122): it cannot select an O(1) value.
(d) In the framework's own form a0 = (1/2) c sqrt(G rho_Lambda) with Lambda = 8 pi G rho_Lambda/c^2, Pi_1 = 1/(32 pi) for every rho_Lambda: any mechanism that sets the vacuum density (QCD instantons, condensates) moves a0 and Lambda together and cannot touch the 1/2.
**Scope (not established beyond it).** The theorem is for the gravity/dS sector with the five constants above. A matter sector with extra dimensionless parameters could in principle carry a Pi_1(Pi_2, others); nothing in the puzzle supplies one, and the data (Pi_1 = O(1e-2) at Pi_2 = 1e-122) already say Pi_1 is Pi_2-independent to leading order. It is a dimensional-analysis argument, not a proof about every conceivable theory.

## (2) Gravitational topological terms (`a05`)
- **Euler / Gauss-Bonnet**: alpha (length^2) is the only dimensionful topological coupling, and it is *free* in EGB gravity. In MM form the Euler coefficient is fixed (L^2/64 pi G), and the connection radius is forced to L: with an independent ell, I_MM(ell) = (pi/G)(ell^2 - L^2)^2/ell^2, stationary only at ell = L; at ell = Z L it costs (Z^2 - 2 + Z^-2) pi L^2/G and is not stationary. The MM field equation itself sets ell = L: a second length 1/a0 has no place in it.
- **Pontryagin / signature**: R R~ = 0 on S^4 (also tr F_SO(5)^2 = 0 for every ell); theta terms are dimensionless. **Holst / Nieh-Yan / Immirzi**: dimensionless 1/gamma, and the Nieh-Yan form is inert for torsion-free e (eps^{abcd}R_abcd = 0 by the first Bianchi identity; control violates it).
- **Weyl instantons**: W = 0 on dS, so chi(S^4) = 2 comes entirely from the R^2/24 term: chi = Lambda^2 V_4/(12 pi^2) (V_4 = 24 pi^2/Lambda^2). Eguchi-Hanson (Ricci-flat, self-dual Weyl): Int E4 = 48 pi^2 and |R R~| = Riem^2 for every size a: a free length, fixed by no charge.
- **Quantisation that exists**: the chiral instanton action per unit charge is S_dS/2 = 2 pi K, so single-valuedness needs K = S_dS/(4 pi) = 3/(4 hbar G Lambda) in Z. This reproduces the published Chern-Simons-Kodama integrality condition kappa = 3/(4 G Lambda beta) at beta = 1 (arXiv gr-qc/0504010, opened; caution: its symbol "a_0" is a Planck area, unrelated to the MOND scale) and the theta = 12 pi^2/(Lambda l_Pl^2) mod 2 pi statement of arXiv 2506.14886 (opened). It quantises 1/(hbar G Lambda) and involves no acceleration scale; K ~ 3e121, so the lattice is far too fine to select anything. arXiv gr-qc/0306083 and gr-qc/0611073: only abstracts opened, nothing on quantisation seen there; not relied on.

## (3) Instanton moduli space, k = 1 on S^4(L) (`a03`)
- BPST field (regular gauge) is self-dual with T_mn = F F - delta F^2/4 = 0 identically: instantons do not back-react, all points of M_1 have the same action and zero energy-momentum: no classical potential on M_1 (control: an added anti-self-dual piece gives T != 0).
- **Unique symmetric point.** The gauge-invariant density |F|^2_phys is constant on S^4 iff x0 = 0 and rho = 1, i.e. physical size L (|F|^2 = 12/L^4): the SU(2)_pm spin connection. Every other point breaks SO(5). L (equivalently Lambda) selects this centre and nothing else; a size rho = Z L (or L/Z) is not distinguished by any symmetry.
- **L^2 metric.** Flat weight: translation norm 8 pi^2, dilation 16 pi^2 (ratio 2), units 1/g^2. With the S^4 weight: the dilation mode along x0 = 0 is horizontal for every radial weight; N(rho) = 64 pi^2 L^2 [p^3 + 9p^2 - 9p - 1 - 6p(p+1) ln p]/(p - 1)^5, p = rho^2, obeying the S^4 isometry N(1/p) = p^2 N(p) (deviation 1.7e-28); N(1) = 32 pi^2 L^2/5, N(0) = 64 pi^2 L^2. The translation zero mode at the centre has weighted horizontal representative d_nu A (exact solution of the Euler-Lagrange equation; the flat-space F_{nu mu} would give 48 pi^2/5), norm 32 pi^2/5 per direction, equal to N(1): the centre metric is (32 pi^2 L^2/5)(dx0^2 + d rho^2)/g^2, an SO(5) vector, as symmetry requires (an independent check of the whole computation).
- In u = ln rho the coefficient N_u is even, has one critical point (the centre, a maximum) and is not constant: the L^2 metric is not the scale-free SO(5,1)-invariant hyperbolic metric; the point-instanton boundary is at finite distance (14.97 L/g). At rho = Z, N_u is 0.21 of its central value, smooth and monotone; nothing marks it.
- **32 pi?** The numbers are 8 pi^2, 16 pi^2, 32 pi^2/5, 64 pi^2 (two pi's); in gravitational normalisation 1/g^2 = L^2/(16 pi hbar G) the centre metric is (2 pi/5)(L^4/hbar G)(dx0^2 + d rho^2): a single pi with a 1/5 from the weight average, not 32 pi. Nothing selects rho, and a one-loop moduli potential would be SO(5)-invariant and hence extremal at the centre (not computed: hbar-full, and it would not know about a0).
- Not scripted: that M_1 = B^5 = H^5 with SO(5) acting linearly (standard result, no source opened here); only the diameter and the centre tangent space were computed, not the metric at generic (x0 != 0, rho).

## (4) The Euclidean a0-Rindler-type cone (`a04`)
Thermal circle 2 pi Z L instead of 2 pi L (temperature a0/2 pi = T_dS/Z): a cone of total angle 2 pi Z on the horizon S^2. Symbolic E4 of the warped metric dchi^2 + h^2 dtheta^2 + c^2 dOmega_2^2: E4 h c^2 = 8 d[(c'^2 - 1) h']/dchi, a total derivative.
- Regular part of Int E4 = 64 pi^2 Z; smoothing the tip (h ~ chi/Z) gives a smooth S^4 with Int E4 = 64 pi^2 for Z = 1/2, 2, sqrt(32 pi/3) (deviation 2e-12 pi^2), so the conical (delta) contribution is 64 pi^2 (1 - Z) = 32 pi^2 * 2(1 - Z). Each SU(2)_pm sees k_reg = Z, tip 1 - Z; Pontryagin density is identically zero.
- **Is Z = sqrt(32 pi/3) special?** The tip is an integer number of instanton units only for half-integer Z. At Z = 5.7888, 2(1 - Z) = -9.578, 0.42 from the nearest integer; Z is transcendental (integer-relation search, control passes). Not one instanton unit, not an integer count.
- The Euclidean EH action of the cone (regular + delta) is -pi L^2/G for every Z (I_EH = -pi Z h'(0) analytically): E = 0 in dS, so I(beta) = -S_dS and no period beta is selected; eps F F (the MM action density) vanishes identically on the whole family. No thermodynamic or topological principle picks beta = 2 pi Z L.

## Errors of mine found and fixed (kept honest)
`a02`: my first run failed three checks that were script errors (a wrong 'unimodular over Z' claim: the lattice has index 2 because Pi_1 is a square; a stray c^4 in S_a0; a float-exactness test in the rational control). `a03`: the first M1 control was wrong (scaling one colour of a self-dual field keeps T = 0) and the first M4 control did not break the symmetry (the polynomial and log parts of N transform identically; mutating a polynomial coefficient does); a nonsense transcendence check in `a04` was replaced; an `a04` comment called the tip deviation O(eps^2), but it is exponentially small (total derivative), corrected. All fixed versions and outputs are left as they stand in this directory (nothing git-added or committed by me).

## What is NOT established
- No derivation of 1/2 or 32 pi. This lane shows the class of instanton / topological / quantisation mechanisms cannot produce it, within the scope stated above.
- The theorem is dimensional analysis in the {c, G, hbar, Lambda, a0} sector; the k = 1 moduli metric is computed only on the diameter and at the centre; H^5 identification and any quantum moduli potential are unverified.
- The instanton coupling normalisation (1/g^2 = L^2/(16 pi hbar G)) is defined by matching the Euler term to a YM-normalised instanton action; it is convention-dependent, the ratio chi = 2 is not.
