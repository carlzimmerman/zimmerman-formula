# TP01 coordinator primary-source checks

Checked 1 November 2026 using the exact primary PDFs. These checks concern
conventions and inputs, not a literature novelty claim or physical validation.
No full external text is retained.

## One-loop spectrum convention

Stephen P. Martin, *Two-loop effective potential for a general renormalizable
theory and softly broken supersymmetry*, hep-ph/0111209v2, 29 March 2002:
<https://arxiv.org/pdf/hep-ph/0111209v2>.

Section 3, equations (3.12)–(3.13), pp. 12–13, supplies the Landau-gauge
DR-bar-prime one-loop sum with weights 1, -2, 3 for each real scalar, Weyl
fermion and vector mass, and common subtraction constant 3/2. With its
overall loop normalization, the contribution is

    [sum_s H(m_s²) - 2 sum_f H(m_f²) + 3 sum_v H(m_v²)]/(64 pi²),
    H(z)=z²[ln(z/Q²)-3/2].

The MS-bar vector constant 5/6 in equation (3.4) belongs to a different
scheme. Equation (3.5) gives the vector squared-mass matrix
g_a g_b phi† {t_a,t_b} phi. The source explicitly treats the effective
potential as gauge-dependent away from physical stationary quantities.
Application to a displaced material state therefore retains the declared
portal, derivative-expansion and matching limitations.

Verdict: convention verified; model spectrum and material application are
separate internal obligations.

## Collective-model valley

David Shih, *Spontaneous R-Symmetry Breaking in O'Raifeartaigh Models*,
hep-th/0703196v3, 19 January 2012:
<https://arxiv.org/pdf/hep-th/0703196v3>.

Appendix A.2, equations (A.8)–(A.12), pp. 14–15, specifies the same
singlet/two-adjoint superpotential, the diagonal SU(5)-breaking valley,
and the canonical flat-direction transformation. The adjoints decompose
into SU(3), SU(2) and bifundamental sectors. Equation (A.13) concerns the
ungauged origin calculation; it is not a full gauged large-field result.

Verdict: source/action dictionary verified. Neither source derives a halo
portal or identifies the sector energy with observed dark energy.

## Independent tree-spectrum benchmark

For K=Tr(A†A)+Tr(B†B)+|X|², fundamental generators with
Tr(t_a t_b)=delta_ab/2, A=i a D, B=bD and
D=diag(2,2,2,-3,-3), the vector mass matrix above has twelve eigenvalues
25 g²(a²+b²) and twelve zeros. This follows by evaluating the off-block
commutators, whose diagonal-eigenvalue difference is 5. It is an internal
algebraic check, not a source-extracted spectral result.

At a generic nonzero-breaking point, 49 chiral complex coordinates provide
98 real scalar coordinates; quotienting twelve broken gauge directions
leaves 86. The twelve massive and twelve massless vectors supply 60
polarizations, matching the 146 fermionic degrees of freedom of 73 Weyl
coordinates (49 chiral plus 24 gaugino). Equal counts are a construction
check and do not establish spectral positivity or supersymmetric pairing.

## Stationary khronon equation and units

Luc Blanchet and Constantinos Skordis, *Relativistic Khronon Theory in
agreement with Modified Newtonian Dynamics and Large-Scale Cosmology*,
arXiv:2404.06584v1, 9 April 2024:
<https://arxiv.org/pdf/2404.06584v1>.

Section III.A.6, equation (3.21), p. 11, gives the stationary modified
Poisson/Helmholtz equation. Section III.A.7, equation (3.22), p. 12, identifies
the MOND kernel with 1+J_Y. These are the locators in the checked 32-page
version, which uses section-numbered equations. Section II.A, equations
(2.3) and (2.5), p. 4, defines A as physical acceleration and Y=A²/c⁴;
J has units of inverse length squared. Thus a_geo=a0/c² is needed in
the displayed geometric J function.

Verdict: the stationary equation, kernel dictionary and dimensional
conversion are source-verified. The particular simple kernel remains a
project choice. This source check supplies neither its physical health
nor an equivalence with the squared-excess kernel.
