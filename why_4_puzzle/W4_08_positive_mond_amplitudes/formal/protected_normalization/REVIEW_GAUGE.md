# Independent review of the quantum-state and physical-metric packets

2026-10-20. Reviewer: critical_gauge_current. Read-only reconstruction of
the other agents' analytic derivations; no compilations, scripts or source
downloads. No unresolved mathematical objection was found within the
explicit scopes below. This is not certification of the full microscopic
normalization goal, which remains open.

## Exact reviewed texts

- `PHYSICAL_METRIC.md`, SHA256
  `893549d913e3004be8736c9398652682790af8271696e3c420cf1b206799f025`.
- `SOURCES_METRIC.md`, SHA256
  `6a54e7c17254de85448f6a551fac4213e1f8fae71fe4958a6e7275badae1e97e`.
- `QUANTUM_STATE.md`, SHA256
  `0a9f2b6e14b3fff3bea8a01ce7e8df14a58eb8c7cef31981f2162d70bf41a4fb`.
- `SOURCES_QUANTUM.md`, SHA256
  `e49b68ca26bbc72e0557e6ce5d652a81f63c51703cfb5ab55e2fd499b536b95e`.

The quantum text includes the smooth-profile relative determinant,
massless rank-one Schur complement and finite-cutoff interacting extension.
The hashes identify the actual reviewed content; later revisions require
checking their changed dependencies.

## Quantum response reconstructed independently

1. The S^D degeneracy and eigenvalue powers give derivative tails
   l^(D-1-2k); convergence requires 2k>D. For D=4 the third derivative
   is finite with the stated positive sign. Subtracting the first two
   mass-source powers leaves a uniform O(l^-3) tail. The gapped analytic
   domain excludes a leading positive z^(3/2) term. A third-derivative
   sign alone is not used to differentiate an uncontrolled remainder.
2. For an actual smooth profile, B>=0 bounded and
   K0=A0^-1/2 B A0^-1/2<=||B|| A0^-1 imply the stated Schatten-3 bound.
   The relative log determinant and its third derivative follow without
   assuming B commutes with A0. Resolvent identities identify its trace
   with Tr[(A_t^-1/2 B A_t^-1/2)^3]. The subtraction constants remain
   matching data; arbitrary finite higher operators are not constrained.
3. With m0=0, the positive mean of a nonzero nonnegative B gives a
   rank-one Schur factor t[b00+O(t)]. The gapped Q block is analytic,
   leaving log t rather than t^(3/2). At finite cutoff this factorization
   is exact; its stated continuum use retains the local subtraction
   contract. A smooth scalar's gradient may vanish at points without
   invalidating b00>0.
4. Direct quartic moments give <c^2>=2 Gamma(3/4)/Gamma(1/4)/sqrt(Vu4)
   and <c^4>=1/(Vu4). Differentiation gives the negative variance with
   the reported factors of V, lambda_s and 1/4. Quartic domination
   establishes entire finite-dimensional partition functions and local
   analyticity of their real logarithms. No regulator-uniform interacting
   continuum analyticity or Lorentzian local-response theorem is assumed.
5. Uniform metric scaling gives epsilon=W-H W_H/4 for the complete
   covariantly renormalized invariant family. Independently varying a
   local W(z,R) gives the directional gradient term and
   epsilon=W-R W_R/2 at zero gradient. The finite Einstein contribution
   and vanishing exact-dS R^2 variation have the displayed signs. An
   isolated zero-mode normalization is correctly not assigned this stress.

The constant-spurion diagnostic, genuine smooth Euclidean profile, and
Lorentzian inhomogeneous gravitational response remain distinct. A finite
positive-measure affine-source identity is not extended to fermion signs,
nonaffine matching operators or unspecified nonlocal sources. The stated
open continuation therefore survives this review as open, not disproved.

## Physical metric and operational normalization reconstructed independently

1. Rank-one inversion, determinant and U_mu=AB u_mu check directly.
   Varying phi gives alpha tilde_T-beta rho_U. Varying unconstrained
   contravariant u supplies the displayed clock current; integrating
   its diffeomorphism variation by parts gives the stated Ward signs.
2. The particle action -mABN dt gives Q=alpha+beta as both aligned dust
   source and test charge. Expanding the physical metric gives
   Phi=n+Q phi and Psi=n-alpha phi, so gamma=1 requires
   2alpha+beta=0 for a nonzero scalar fraction. The continuous family
   A=exp(-Qphi), B=exp(2Qphi) satisfies that relation for arbitrary Q.
3. General-n radial Gauss and both source/test factors give the listed
   Gs_n, a_s and n=3 force law. The resulting actual-vacuum ratio scales
   as f^3; substituting the inherited tensor/cosmological coefficients
   gives the reported inferred-density conversion. These are weak-source,
   local UV and leading-potential statements, not all-source PPN results.
4. The two-sided saturated-cone argument is a local-minimum derivative
   argument and is valid under its added assumptions. It is correctly
   separated from invertibility, strict unsaturated inclusion, global
   causality and the reference B0=1 convention.
5. Converting the static measure and spatial derivative with
   t_phys=A0B0 t, x_phys=A0 x gives all C2/C3/V factors in section7.
   Converting the homogeneous kinetic density gives
   Gcos_phys=A0^2 Gcos/B0, distinct from
   Guv_phys=A0^2 B0 Guv. Thus xi_actual is invariant while the
   Friedmann-inferred expression acquires B0^2. No constant-background
   conversion is used as a rolling-background theorem.

Invertibility and the Ward identity supply no numerical Q equation.
The physical-metric repair is a change of matter coupling to the fixed
action, not merely a field redefinition, and the text correctly retains
the earlier matter-free clock instability and independent health problem.

## Source and independence limits

The source cards were read for exact version and extraction scope. Their
authenticated external versions are Bekenstein astro-ph/0403694v6 and
gr-qc/9211017v1; Garcia-Consuegra--Rajantie 2511.23076v2;
Beneke--Moch 1212.3058v1; Guilleux--Serreau 1506.06183v2; and the primary
Gibbons--Hawking 1977 and Dowker--Critchley 1976 publisher records. I did
not repeat all of the other authors' external retrievals in this review;
in particular the abstract-only Q4/Q5 evidence is not upgraded to a
numbered full-text theorem. The new stress and relative-determinant
derivations were checked as derivations, not attributed to those abstracts.

I authored `PROTECTED_GAUGE.md` and `SOURCES_GAUGE.md`; this review is not
an independent review of those files. Their independent cross-review is
provided by the other agents. I also contributed the previous pure-BM
de Sitter packet, so inherited gravity coefficients/spectrum are marked
as prior inputs rather than newly independent evidence here. The P2
quantum and P3 metric reconstructions above were performed independently
after their authors saved the respective packets. No Lean theorem or
end-to-end formal proof is claimed by this analytic review.
