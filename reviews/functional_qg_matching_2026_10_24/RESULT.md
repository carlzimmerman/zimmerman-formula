# Functional quantum gravity: nonlinear force and portal matching

The requested mechanism remains unestablished. This continuation checks functional kinetic-response and predicted matter-portal studies, rather than repeating the earlier curvature-ratio audit. It also derives an operational test that a proposed quantum-gravity matching must pass: control the physical quadratic contamination of the cubic MOND response.

Base 0fc9bade547ad11b2c1685815cefc82b130fff31; freeze 18c33c1688. Parent ../rg_joint_selector_2026_10_24/RESULT.md. Kappa=1/2 remains FITTED. CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are separate, unused. Dark-energy footing; c=hbar=1. No numeric kappa or new microscopic beta function is asserted.

## 1. A functional fixed-point equation is available, but its target differs

De Brito, Knorr and Schiffer, [On the weak-gravity bound for a shift-symmetric scalar field](https://arxiv.org/html/2302.10989v1), v1, 2023-02-21, was checked at equations 7-9, 21, 63-64 and section IV. It studies a kinetic function, with Kcal(0)=0 and Kcal'(0)=Z, using systematic expansions. Its gravity-scalar analysis fixes the cosmological parameter to zero and treats the dimensionless Newton coupling as external. The nontrivial functional equation therefore does not jointly select the vacuum amplitude and response. Baryon-source matching is absent. This is a partial fixed-point investigation, not the complete coupled mechanism requested here. The v2 HTML was unavailable, so these findings are explicitly pinned to v1.

The boundary normalization by itself does NOT prove that the physical infrared force has a finite positive quadratic coefficient. Wavefunction factors, RG limits, analytic continuation and the cosmological background must be matched first. A nonuniform limit could change the small-gradient response. It would be incorrect to turn a normalization convention in this paper into a general no-go for MOND.

What the source does establish for this investigation is the appropriate next mathematical object: the full kinetic functional. The missing implication is a controlled infrared, Lorentzian, sourced branch with the required nonanalytic term, followed by joint vacuum and matter matching. We have not reproduced or solved that full flow.

## 2. Compute the physical low-gradient test

Assume the static force branch actually matches to

L_static = -Z |grad theta|^2/2 - C |grad theta|^3/3 - q rho_b theta,

with Z,C,q>0 and dimensionless theta. Here Z is a quadratic coefficient, unrelated to the repository's historical use of Z for a cosmological ratio. In natural units [Z]=mass^2, [C]=mass and [q]=1.

Writing y=theta'>0, the regular sourced spherical flux in n spatial dimensions is

S_(n-1) r^(n-1) (Zy+Cy^2) = q m_b(<r).

In the exterior of a compact source, specialize to n=3 and define

g_theta=qy,  g_N=Gm_b/r^2,
a0=q^3/(4pi G C),  g_star=qZ/C.

The exact force equation for this stated static action is

g_theta^2+g_star g_theta=a0 g_N,
g_theta=[sqrt(g_star^2+4a0 g_N)-g_star]/2.              (1)

Two distinct regimes follow:

4a0 g_N >> g_star^2:  g_theta approximately sqrt(a0 g_N),
4a0 g_N << g_star^2:  g_theta approximately (a0/g_star)g_N.

The low-gradient limit returns to inverse-square behavior whenever g_star stays nonzero. The total baryonic force includes ordinary Newtonian gravity as well; adding it does not restore a 1/r tail when both contributions scale as 1/r^2.

The radius defined by 4a0 g_N=g_star^2 is

r_break=2sqrt(a0 Gm_b)/g_star.

It scales as sqrt(m_b), while its Newtonian acceleration g_N(r_break)=g_star^2/(4a0) is mass-independent. This differs from the mass-dependent acceleration crossover in the earlier KGB screening calculation; it must not be mislabeled the same obstruction.

Under theta_new=z theta, the coefficients transform as

Z_new=Z/z^2, C_new=C/z^3, q_new=q/z.

Both a0 and g_star are invariant. Choosing field units with a normalized quadratic coefficient cannot remove the physical crossover. Strict cubic asymptotics as g_N approaches zero would require g_star=0 in this model. A finite-domain galactic theory only needs it sufficiently small over that domain; no infinite-halo requirement or empirical bound has been imposed here. A different retained-mode structure may change (1) and must be calculated separately.

The asymptotic limits checked by the script are algebraic limits of the stated action, not assertions that a real halo, derivative expansion or weak-field approximation extends to r=0 or infinity. This calculation does not claim that the published functional RG study has the physical Z used here; it provides a conditional matching test for any such proposal.

## 3. Does quantum gravity predict the required matter portal?

Eichhorn and Pauly, [Constraining power of asymptotic safety for scalar fields](https://arxiv.org/html/2009.13543v2), v2, 2021-08-31: checked sections V.1-V.4 and Table 1. In their extended scalar-fermion model, fixed point FP3 predicts the canonically marginal matter couplings within the truncation. Two scalar masses and two gravitational directions remain relevant. The portal studied is a Higgs-type scalar interaction; it is not already the MOND source q rho_b theta. No cubic-gradient MOND coefficient is jointly matched there. This is genuine predictive structure, but it does not supply the requested ratio. Parameter counting alone would not disprove that ratio's universality; the physical matching map must still be calculated.

Converting a Higgs or Yukawa portal into q requires the scalar spectrum, mixing, source charges and low-energy state. Its kinetic sector must then be matched onto C and any surviving Z. Equating a tabulated portal fixed-point value with cb would bypass those steps. Combining this paper with the separate functional-response study does not give a self-consistent joint RG system: the field contents, truncations and backgrounds differ.

## 4. Exact remaining task

A proposed quantum-gravity mechanism must predict the physical invariant

cb^3/(c3 sqrt(c0))

over its entire admissible microscopic family, as derived in the parent packet. On a branch described by (1), it must also control qZ/C so the actual force remains MOND-like over the intended range. Neither property follows from naming a UV fixed point or normalizing fields. They require the complete infrared matching on a healthy sourced state.

This investigation found no theory supplying both properties. It did not establish impossibility. The full functional-gravity route and a combined matter-portal calculation remain open; their missing work is a new joint quantum calculation, not an algebraic value that can honestly be extracted from the two checked papers.

Verification: all 11 baseline symbolic identities pass. Doubling the physical source/force charge makes the corresponding baseline matching assertions fail in a separate nonzero-exit mutation run. No fitted acceleration, target coefficient or numerical parameter scan enters the executable. Published numerical RG flows were inspected through their primary statements, not reproduced.
