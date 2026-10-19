# CDQ-002: exact neutral Coulomb kernel on the closed sphere

Supplement to immutable CDQ-001 DERIVATION.md. This checks the possible 1/R term before Debye resummation, directly in the regulated compact neutral gas. It is a finite-configuration identity at fixed geodesic separations, not a termwise infinite-volume plasma proof.

For chi=d(x,y)/R in (0,pi), solve the radial Green equation with a neutralizing constant background and zero spatial mean:

    G_R(chi)= [(pi-chi) cot(chi)-1/2]/(4pi²R).                         (G1)

Its unit-sphere radial Laplacian is G''+2cot(chi)G'. Acting on the numerator gives 2. Therefore away from its source Delta G=1/(2pi²R³)=1/V. The singularity is G~1/(4pi r), so unit Gauss flux fixes the delta coefficient, yielding -Delta G=delta_g-1/V. The numerator tends to -3/2 at chi=pi and its derivative tends to zero; the Green function is regular at the antipode. Finally

    integral_0^pi sin²(chi) [(pi-chi)cot(chi)-1/2] dchi=0,

since the first term integrates to pi/4 and the second to -pi/4. This fixes the additive constant; it was not chosen as a self-energy convention.

At fixed r while R grows,

    G_R(r)=1/(4pi r)-3/(8pi²R)-r/(12pi R²)
                           +r²/(12pi²R³)+O(r³/R^4).                  (G2)

The finite regular coincidence term after subtracting the same flat singular core is -3/(8pi²R). The identical constant occurs in every pair entry. With the same self subtraction used for fugacity and interactions, the 1/R contribution to the full Coulomb action is exactly

    delta S_(1/R)= -3/(16pi² kappa R) (sum_e q_e)²=0                 (G3)

for every magnetically neutral finite configuration. Keeping only the regular self energies would instead give a nonzero sum q_e² term; the pair entries cancel it. Omitting self terms from the action requires absorbing their entire regular part into f_R; including it in both places double counts. The canonical compact zero mode is what imposes this exact neutrality.

The fixed-r expansion is not uniform at separations r~R. It does not justify interchanging a many-particle thermodynamic sum with the expansion. The independently calculated, all-mode Gaussian Debye resummation in CDQ-001 handles the leading weak-plasma contribution at fixed positive screening mass and supplies its own explicit no-1/R result. Equation (G3) is an additional microscopic cancellation check, not a replacement for that resummation or for hard matching.
