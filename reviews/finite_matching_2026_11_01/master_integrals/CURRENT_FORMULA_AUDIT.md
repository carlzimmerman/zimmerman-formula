# Independent component current reconstruction

Reviewer: `/root/independent_math_transport`, 1 November 2026. **Verdict:
the stated local one-loop component coefficient passes under the fixed
Landau, dimensional-reduction/minimal-subtraction and phase-state
conventions.** This is a finite coefficient around zero phase frequency;
it is not all occupied higher-derivative matching or an anomaly/lifetime
theorem. The raw kernels were independently derived before code review.
The author then supplied controls; the review is not blind and did not
rerun the current experiment.

The scalar phase charges are q_s=1 for X,B and 0 for A. With θ=arg X,
the Weyl charges are q_f=q_s−1/2, including q_f=+1/2 for gauginos.
This follows from the R action; θ is half the original R angle. All
normalizations below refer to a kinetic term δF(∂θ)², without an extra
factor 1/2.

## Scalar determinant: ordered versus unordered sums

In canonical real coordinates δz=(q+ip)/√2, let the antisymmetric charge
matrix be J_s. The real Hessian rotates as
H(θ)=exp(J_sθ)H exp(−J_sθ), so H_θ=[J_s,H]. Its scalar determinant is
(1/2)Tr ln. At second order the two linear vertices have coefficient
−1/4 Tr(G H_θ G H_θ), with the two external θ fields implicit. The quadratic seagull enforces the zero-momentum
isospectral Ward identity but contains no external momentum.

For D=t m_i²+(1−t)m_j² the p² bubble derivative gives

    δF_s=Σ_ordered |H_θ,ij|²/(64π²)
                       integral_0^1 t(1−t)/D dt.

In a real mass basis H_θ,ij=(m_j²−m_i²)J_s,ij. Define

    G(a,b)=(a+b)/2−ab ln(a/b)/(a−b).

Since (a−b)²∫t(1−t)/D=G(a,b), one **unordered** pair contributes
J_s,ij² G(a,b)/(32π²). Thus current.py's unordered-pair G/(2L), L=16π²,
is correct. G(a,a)=0 and G(a,0)=a/2. A commuting scalar Hessian gives
zero rather than an artificial charged-scalar wavefunction.

## Signed Majorana determinant

The CP slice permits a constant unitary congruence making the full fermion
mass matrix real symmetric. After a real orthogonal rotation keep signed
eigenmasses μ_i. The phase vertex is M_θ=−i{Q_f,M}=iA_θ, with A_θ real
symmetric. Replacing μ_i by |μ_i| in the chirality-flip numerator would
be wrong; its signs are retained by the implementation.

The Euclidean Majorana determinant −Tr ln/2 and its spin trace give a
bubble numerator proportional to k·(k+p)+μ_iμ_j. After the Feynman shift,
the p² term is

    A_ij² integral_0^1 t(1−t)
          [3 B(D)−1/L+μ_iμ_j/(L D)]dt,
    B(D)=L^−1[1/bar_epsilon−ln(D/Q²)].

Subtracting the pole therefore gives the ordered kernel

    δF_f=Σ_ij A_ij²/L integral_0^1 t(1−t)
                     [−3ln(D/Q²)+μ_iμ_j/D−1]dt.

For a single Majorana mass m exp(iθ) it reduces to
−m²ln(m²/Q²)/(32π²). The finite −1 term and the Majorana factor are both
necessary. current.py's weighted log, rational integral and −1/6 constants
implement this expression correctly.

The two adjoint and broken 3×3 signed-mass blocks reproduce the full
73-Weyl singular spectrum and current vertex norm. The remaining chiral
singlet block has no mass-phase vertex on this valley: its nonzero mixing
connects opposite phase charges, while its AA entry vanishes. Massless
unbroken gauginos likewise have no vacuum mass-phase vertex. They are not
silently counted as massive modes or as a selected occupied reservoir.

## Scalar-vector graph and the finite +1/2

Expanding the canonical covariant kinetic term around a slowly rotating
background and using the linear Landau condition gives

    L_mix=−2√2 g (∂_μθ) A_a^μ C_aI χ_I,
    C=(Re[R_a Q_s z],Im[R_a Q_s z]).

The real scalar/vector block determinant has second-order coefficient
−1/2 times the square of this mixed vertex. Averaging the transverse
projector over a d-dimensional loop direction gives

    δF_SV=−4g²(d−1)/d Σ C_aI² B(m_SI²,m_Va²),
    d=4−2ε,  (d−1)/d=3/4−ε/8+O(ε²),
    B=L^−1[1/bar_epsilon−integral_0^1 ln(D/Q²)dt].

Multiplying before subtracting the pole yields

    δF_SV=g²/L Σ C_aI²[3 integral_0^1 ln(D/Q²)dt+1/2].

The positive finite 1/2 follows from the evanescent −ε/8 projector term
times the pole. Setting d=4 before subtraction incorrectly removes it.
In dimensional reduction the external phase momentum has no extra-
dimensional component, so epsilon vectors have no such SV derivative
vertex. Their background mass is common-phase independent. Pure vector
mass derivatives and linear Landau ghosts therefore supply no additional
one-loop θ derivative graph of this type. Gauge Goldstones remain in the
scalar basis and the mixed graph; no unitary-gauge deletion is made.

This derivation fixes the stipulated component subtraction convention;
a different finite field normalization requires an explicit scheme change.
No finite counterterm has been chosen to manufacture a pressure outcome.

## Independent ultraviolet and code checks

The fermion vertex norm can be reconstructed without a numerical mass
rotation. Its AA sectors contribute

    8(3hX)²+3(−2hX)²+12(hX/2)²=87h²X².

The ordered B/gaugino entries add 2×12(5gb)²=600g²b². The SV norm is
Σ C²=C_adj Tr B†B=5×30b²=150b². Thus

    ∂_lnQ δF=[87h²X²+600g²b²−900g²b²]/L
             =[87h²X²−300g²b²]/L.

It equals twice the tree angular metric weighted by the **Landau component
scalar** anomalous dimensions, γ_X=12h²/L and
γ_B=[21λ²/20−5g²]/L. Substituting the chiral-superfield gauge term −10g²/L
would fail this identity. The retained X is a singlet, but the charged B
component still matters in this current calculation.

The code's equal-mass series for G, ∫t(1−t)/D, ∫t(1−t)ln D and ∫ln D
follow by expanding D=m[1+δ(2t−1)]. Its massless formulas also integrate
directly. The general weighted-log antiderivative and both eigenbasis
rotations were checked. The final null cutoff is relative to the positive
spectrum, rather than an absolute unit floor.

The completed run checks eight full cases: e=.01,.03 and reference-field
ratios 1,1.15,1.21,1.3, with Q fixed separately for each e. Parameter
quadratures agree within 4.95×10⁻¹³; raw phase matrix derivatives within
2.15×10⁻¹¹; isospectral Ward tests within 1.56×10⁻¹⁵; full/block mass
squares within 2.67×10⁻¹⁵; UV group residual within 3.47×10⁻¹⁷; and the
explicit Q finite difference within 2.56×10⁻¹⁵. The genuine f=0,g=0
supersymmetric chiral limit and g=0 SV decoupling pass. A supersymmetric
wavefunction need not vanish, so that limit is checked against its actual
nonzero Majorana result.

All massless SV vertices vanish at the stated tolerance; no nonzero
massless denominator is evaluated as a harmless zero. These are finite
validation results, not interval certificates. The local one-loop graph
sum excludes the separately computed heavy geometric pullback and cannot
be double counted when the two are combined. Finite occupied higher-
derivative terms, radial kinetic matching, anomaly/current lifetime,
gauge/IR dynamics and a selected physical state remain separate.
