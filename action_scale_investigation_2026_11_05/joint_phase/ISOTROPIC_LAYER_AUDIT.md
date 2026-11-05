# Vector sign repair and covariant orientation averaging

Base: 2ab4c0f06f. Previous goal turn: progress, establishing the actual
Dirac curvature threshold and the failure of intrinsic leaf curvature to
equal R_4. This route changes both the matter content and the embedding:
a massive vector changes the curvature threshold, and an isotropic
continuum of material foliations replaces one preferred layer direction.

Target discriminator: can these changes generate a positive cubic sector
and a viable four-dimensional gravitational action from the same quantum
medium? The final objective remains the vacuum/operational-MOND coefficient;
repairing a sign alone is not success. This is an analytic derivation with
self-review, not a numerical search or a new executable evidence run.

## 1. Constant-mass microscopic vector sector

For positive constant mass on a smooth three-dimensional leaf, use a
Stueckelberg vector, its scalar and the gauge-fixing ghosts. At quadratic
order the parity-even Euclidean determinant is

    Gamma_v=(1/2)Tr_1 log(Delta_1+m_v^2)
             -(1/2)Tr_0 log(Delta_0+m_v^2),
    Delta_1=-nabla^2 delta_a^b+R_a^b, Delta_0=-nabla^2.

The scalar subtraction is essential: there are two physical massive-vector
polarizations in 2+1 dimensions, not three. Gauge fixing gives one vector
determinant, one real Stueckelberg scalar determinant and one complex ghost
determinant. Their scalar coefficients add to -1/2, as displayed.

The bulk heat coefficients of the vector-minus-scalar combination are

    a0: 3-1=2,
    a2/R: (3/6-1)-1/6=-2/3.

In the same finite-threshold convention as NODAL_CURVATURE_RESULT.md,

    L_E,v=-1/[2(4pi)^(3/2)]
            [2 Gamma(-3/2)m_v^3-(2/3)Gamma(-1/2)m_v R_3]
          =-m_v^3/(6pi)-m_v R_3/(12pi),
    u_v=-m_v^3/(6pi), f_v=m_v/(6pi).

Here the leaf Lorentzian action is f_v R_3/2-u_v. The sign follows from
L_E=u_v-f_v R_3/2. A vector can supply positive f_v, unlike the preceding
minimal fermion threshold. The price is a negative cubic energy contribution.

Combine one such vector with a parity pair of two-component Dirac fields,
total spinor trace four. With m_f=h_f sigma and m_v=h_v sigma,

    u_3=(4h_f^3-2h_v^3)sigma^3/(12pi),
    f_3=(-4h_f+8h_v)sigma/(48pi).

Both are positive on the open interval

    1/2 < h_v/h_f < 2^(1/3).

For example equal positive masses lie inside this interval and give
u_3=h^3 sigma^3/(6pi), f_3=h sigma/(12pi). This is a sign demonstration,
not a selected mass ratio or a coefficient prediction. No symmetry
relating h_f and h_v has been supplied. Divergent and finite analytic
counterterms remain matching data. A field-dependent vector mass also
requires additional derivative terms; the constant-mass determinant does
not compute the full sigma kinetic coefficient or a Higgs completion.
This sector has not supplied the separate gapless polarization determinant.

### Source authentication and scope

[Ruf and Steinwachs, 1806.00485v2](https://arxiv.org/html/1806.00485v2),
11 July 2018, section V equation (38), verifies the vector-minus-scalar
structure for constant-mass Proca bulk divergences. Its four-dimensional
divergence coefficients are not substituted into our three-dimensional
finite terms; those are calculated above from the displayed operators.
[Barvinsky and Kalugin, 2408.16174v2](https://arxiv.org/html/2408.16174v2),
30 September 2024, sections 2-3, warns about total-derivative/determinant
issues for the nonminimal Proca operator. Here the Stueckelberg definition
uses minimal operators and only the bulk constant-mass terms through R.
Boundary contributions and variable-mass derivatives are not inferred.
Both sources were checked on 5 November 2026. Source application is limited
to that determinant structure; neither source supplies the cosmological
embedding or MOND matching below.

## 2. A specified spatially isotropic covariant embedding

Introduce three scalar material labels Phi^I, with internal SO(3), and
background Phi^I=x^I. For each fixed internal unit vector n_I define

    phi_n=n_I Phi^I,
    X_n=g^(mu nu) partial_mu phi_n partial_nu phi_n>0.

The level sets of phi_n are timelike hypersurfaces. Let R_n be their
intrinsic 2+1-dimensional curvature. Take normalized angular average over
the internal unit sphere, and fixed label density nu>0. The proposed
effective action is

    S_layer=nu integral d^4x sqrt(-g)
             <sqrt(X_n)[f_3(sigma) R_n/2-u_3(sigma)]>_n.

The sqrt(X_n) factor is not optional for this construction. By the coarea
formula, sqrt(-g)sqrt(X_n)d^4x becomes the induced leaf measure times
d phi_n. It describes a fixed number of leaves per label interval. Replacing
it with one would be a different theory of layer-density dynamics.

This is a covariant action with a material rest frame, not a Lorentz-invariant
vacuum. Its foliation fluctuations are the three fields delta Phi^I, not an
independent displacement field for every n. This distinction matters in the
tensor calculation below.

## 3. Stress of the zero-derivative term

On a spatially flat FRW metric ds^2=-N^2 dt^2+a^2 dx^2 with Phi^I=x^I,
X_n=a^(-2). For a held homogeneous sigma, the potential action per comoving
volume is

    L_potential=-nu N a^2 u_3.

Its stress, obtained by lapse and scale-factor variation, is

    rho_potential=nu u_3/a,
    p_potential=-2nu u_3/(3a),
    w_potential=-2/3.

Thus a constant loop energy on each leaf is an area-tension contribution,
not a four-dimensional cosmological constant. These are the stress components
of the potential term at held sigma. They are not a solved cosmology or the
total equation of state including curvature and sigma evolution. Introducing
a separate four-dimensional constant, changing density dynamics or evolving
sigma changes that question and supplies additional equations/data.

## 4. Tensor principal action: isotropy does not produce Einstein gravity

Work locally about the isotropic, slowly varying background, with sigma
held fixed and coefficients frozen, in the same derivative expansion used
to integrate out the massive fields. Choose a transverse-traceless spatial
metric perturbation h_ij. Set lapse one and shift zero in this helicity-two
sector. The amplitude, lapse, shift and the three material displacements
have helicity zero or one and do not mix linearly with helicity two on this
isotropic background. Non-derivative stresses can contribute mass terms;
the following calculation concerns only the two-derivative principal terms.

For one orientation put P_ij=delta_ij-n_i n_j. The intrinsic spatial leaf
has dimension two. Its extrinsic curvature with respect to time is
K_AB=(1/2)partial_t h_AB to first order. The intrinsic Einstein term gives

    S_time^(2)=nu f_3/8 integral d^4x
                <Tr(P dot h P dot h)-[Tr(P dot h)]^2>_n.

For a traceless symmetric matrix H,

    Tr(P H P H)=Tr(H^2)-2n.H^2.n+(n.H.n)^2,
    [Tr(P H)]^2=(n.H.n)^2.

Using <n_i n_j>=delta_ij/3, their difference averages to Tr(H^2)/3.
With F_bar=nu f_3 at the locally normalized background, this gives

    S_time^(2)=F_bar/24 integral d^4x dot h_ij dot h_ij.

For static h_ij and constant f_3, each leaf instead reduces to the integral
of its two-dimensional spatial scalar curvature. With compactly supported
perturbations (or consistently fixed boundary terms and data), this is a topological/boundary term
and has no bulk metric variation. The coarea measure makes its coefficient
constant on each leaf; no unmentioned normal-lapse factor multiplies it.
Therefore the bulk spatial-gradient term in this tensor sector is zero:

    S_tensor,principal^(2)=F_bar/24 integral d^4x dot h_ij dot h_ij,
    c_tensor^2=0 at two-derivative order, when F_bar>0.

This is not the Einstein tensor-wave action. Zero spatial stiffness is not
by itself a proof of a ghost or of an instability in a completed theory;
it means this truncation does not provide the required gravitational-wave
principal operator. Higher derivatives, interactions between leaves or new
embedding operators can change it and must actually be calculated.

As an independent normalization benchmark, in 4D Einstein gravity the same
perturbation has F/8 times [dot h^2-(grad h)^2]. If a bare Einstein term
F_b>0 is appended, the combined principal action becomes

    S_tensor^(2)=(1/8) integral d^4x
                 [(F_b+F_bar/3)dot h^2-F_b(grad h)^2],
    c_tensor^2=F_b/(F_b+F_bar/3).

Thus adding bare gravity can restore spatial propagation, but introduces
an independent coefficient. It does not turn F_bar into the same tensor
coupling used in the earlier scalar-tensor MOND formula. No observational
bound or target numerical ratio has been inserted here.

## 5. Audit and research handoff

Normalized claim: this specified mixed-matter, coarea-weighted isotropic
layer action repairs the finite-threshold sign on an open mass-ratio
interval, but its potential stress and tensor principal operator do not
match a cosmological constant plus Einstein gravity. Verdict: proved for
the displayed truncation and background assumptions, by analytic derivation;
the proposed transfer to a complete MOND theory remains incomplete.

Dependency audit:

- Constant-mass vector determinant: explicit Stueckelberg count and checked
  primary-source structure; no variable-mass or boundary extrapolation.
- Finite cubic/curvature signs: Gamma(-3/2)=4sqrt(pi)/3,
  Gamma(-1/2)=-2sqrt(pi), including the Euclidean-to-Lorentzian sign.
- Positive interval: direct inequalities in positive h_v/h_f, no scan.
- FRW potential stress: direct variation of -nu N a^2 u_3.
- Tensor kinetic coefficient: projector identity and isotropic second
  moment, with the 4D Einstein coefficient as a normalization check.
- Tensor spatial term: two-dimensional curvature boundary identity for
  fixed leaf topology, constant f_3 and coarea measure.
- Full nonlinear stability, dynamical background, quantum protection,
  gapless response and operational acceleration: not established.

All review is self-review. No executable was run for these analytic claims,
and no successful test count is asserted. The preceding Dirac sign result
was not a universal no-go: the vector calculation explicitly shows how its
scope can be escaped. The new obstruction concerns this covariant material
embedding, not every statistically isotropic quantum medium.

The cheapest next useful step is to derive, from a microscopic interaction
between orientations or a different embedding, the terms supplying tensor
spatial stiffness AND the vacuum stress. Arbitrarily appending the missing
Einstein term or replacing the coarea factor while retaining the same loop
coefficients does not establish that bridge. The already computed normal
dispersion repair changes the infrared cubic and cannot be imported without
its crossover and response matching. Variable-mass vector/Higgs completion
is also uncomputed; it needs a specified microscopic action before its
kinetic and gapless limits can be inferred. The original coefficient goal
remains active and unresolved. No action or shared campaign record is changed.
