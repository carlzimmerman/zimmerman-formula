# The physical COM-relative internal oscillator-strength budget

19 October 2026. Supplement to `OCCUPATIONS.md`; no frozen scientific input
or script is changed. The parent independently checked the source derivative,
weighted-variance identity and small-k coefficient below. This is a leading
Newtonian fixed-mass statement, not the full relativistic stress sum rule.

**Result.** Removing common free fall changes the *physical internal*
source-strength budget. For a smooth source profile `h`, the first moment
is half the mass-weighted variance of `grad h`, rather than half its
unprojected squared norm. For `h=sin(kz)/k`, both this internal first moment
and the shared n=1 state's static susceptibility vanish as `k^4`.
Their ratio nevertheless gives a finite, source-weighted internal gravity
frequency. This is a normalization test for the actual shared modes; it
does not select their occupations or create saturating sites.

## 1. Contract and exact source operator

Take fixed positive point masses `m_i`, total mass `M=sum_i m_i`, canonical
commutators `[x_i,p_j]=i delta_ij`, and

\[
 H=\sum_i\frac{\boldsymbol p_i^2}{2m_i}+V(\{\boldsymbol x_i-\boldsymbol x_j\}).
                                                               \tag{1}
\]

Here `V` contains position-only interactions: the daughter repulsion and
Newtonian self/baryon gravity in the retained model are of this form once
properly defined/regulated. Let `R=M^-1 sum_i m_i x_i` and `y_i=x_i-R`.
The total kinetic energy separates into `P^2/(2M)+T_int`; all the operators
below commute with the common COM coordinate and momentum as appropriate.
The COM-relative physical source is

\[
 D_h=\sum_i m_i h(\boldsymbol y_i),\qquad H_{\rm src}=-gD_h. \tag{2}
\]

This describes a prescribed probe centered on the object's reference COM,
or its internal response in the accelerating COM frame. It is not a
species-dependent coupling. For odd `h`, the equilibrium source expectation
vanishes in an inversion-symmetric state.

The exact identity requires a common operator domain on which the double
commutator and its expectation exist. A finite regulator is one control;
continuum contact/gravity limits must keep the stated domain and finite
moments. For the following sine profile, `h` and its derivatives are
bounded. The small-k expansion additionally requires a finite internal
fourth position moment (and a finite sixth moment for the displayed
`O(k^6)` remainder); otherwise use the exact bounded-gradient formula.

The applicable scalar branch is daughter-only with conserved daughter
number after the matched source elimination, together with fixed ordinary
baryon masses. The identity is not asserted when an unresolved molecule has
kinetic mass `M_X` differing from reference charge mass `2m`, when conversion
changes the assigned inventory, for momentum-dependent interactions, or
for the full relativistic gravitational stress at fixed signed charge.
Those cases require their own matched kinetic and source operators.

## 2. Derivative and double commutator

Differentiate (2) in the unreduced particle coordinates. Since
`partial y_j/partial x_i=delta_ij-m_i/M`, one obtains

\[
 \nabla_{x_i}D_h=m_i[\boldsymbol f_i-\bar{\boldsymbol f}],\qquad
 \boldsymbol f_i=\nabla h(\boldsymbol y_i),\qquad
 \bar{\boldsymbol f}=\frac1M\sum_jm_j\boldsymbol f_j.        \tag{3}
\]

The derivatives sum to zero, expressing translation invariance. All
position interactions commute with `D_h`. Applying the kinetic operator
directly to a test wavefunction gives

\[
 [D_h,[H,D_h]]=
 \sum_i\frac{|\nabla_{x_i}D_h|^2}{m_i}
 =\sum_i m_i|\boldsymbol f_i|^2
       -\frac1M\left|\sum_i m_i\boldsymbol f_i\right|^2.    \tag{4}
\]

The first equality follows because the terms differentiating the test
wavefunction cancel in the double commutator. The last equality is the
weighted-variance expansion, so the result is positive. It is unchanged
if `H` in (4) is replaced by the internal Hamiltonian, since (2) commutes
with the COM kinetic term.

For a stationary ground state with positive-frequency source spectrum
`S_h(omega)=sum_n!=0 |<n|D_h|0>|^2 delta(omega-E_n+E_0)`, completeness gives

\[
 M_{1,h}:=\int_0^\infty\omega S_h(\omega)d\omega
 =\frac12\left\langle
       \sum_i m_i|\boldsymbol f_i|^2
       -\frac1M\left|\sum_i m_i\boldsymbol f_i\right|^2
                  \right\rangle.                           \tag{5}
\]

In a Gibbs state the same formula holds for the population-difference Kubo
spectrum, rather than raw absorption/emission counts. In an arbitrary
stationary nonpassive state the double commutator still exists when its
domain assumptions hold, but a positive response measure is not automatic.
For uniform `h=e.y`, all `f_i=e`, so (2) and (5) vanish exactly. Thus the
free-fall cancellation is present in the moment itself.

## 3. A bounded finite-k profile and its infrared moment

For `h_k(y)=sin(k y_z)/k`, equation (5) becomes

\[
 M_{1,k}=\frac12\left\langle
       \sum_i m_i\cos^2(ky_{iz})
       -\frac1M\left[\sum_i m_i\cos(ky_{iz})\right]^2
                         \right\rangle.                     \tag{6}
\]

Let `A_j=sum_i m_i y_{iz}^j`. The constant and quadratic terms in `k`
cancel between the two terms. Expanding the cosine gives

\[
 M_{1,k}=\frac{k^4}{8}
       \left\langle A_4-\frac{A_2^2}{M}\right\rangle
          +O(k^6).                                          \tag{7}
\]

The coefficient is nonnegative by the weighted Cauchy inequality. With
only a finite fourth moment, dominated convergence gives the same leading
coefficient and an `o(k^4)` remainder, rather than an asserted sixth-order
bound. This result also follows from `D_k=-(k^2/6)A_3+O(k^4)` and
`nabla_i A3=3m_i(y_iz^2-A2/M)e_z` in (4).

The full expectation in (7) contains `expectation(A2^2)`, not automatically
the square of `expectation(A2)`. Substituting a smooth equilibrium density
for these many-body correlations is a mean-field/fluid approximation.

In a complete canonical displacement-mode description about a specified
smooth equilibrium `rho0`, projecting `grad h` orthogonally to the common
translation gives the corresponding fluid completeness identity

\[
 \sum_\nu\Omega_\nu d_\nu^2
 =\frac12\sum_\nu c_\nu^2
 =\frac12\left[\int\rho_0|\nabla h|^2
       -\frac1M\left|\int\rho_0\nabla h\right|^2\right].   \tag{8}
\]

Only source-carrying internal modes contribute. A restricted mode subset
has at most this budget, and equality requires exhaustion of the retained
displacement space. Static density-kernel eigenfunctions alone do not
provide a dynamical exhaustion proof. A harmonic linearized operator is
unbounded in displacement; its use must stay within small deformations of
the finite object even though the full sine source is bounded.

## 4. n=1 fluid moments and a concrete dynamical matching target

For the common-profile fluid `rho0(r)=rho_c sin(pi r/R)/(pi r/R)`, radial
integration and spherical angular averages give

\[
 \frac{\langle z^2\rangle_{\rho}}{R^2}=\frac13-\frac2{\pi^2},
 \qquad
 \frac{\langle z^4\rangle_{\rho}}{R^4}
             =\frac15-\frac4{\pi^2}+\frac{24}{\pi^4}.
                                                               \tag{9}
\]

Here `average_rho f=M^-1 int rho0 f`. For example, the mass radial
integral in units `R=1` is `int r^2 sinc(pi r)dr=1/pi^2`, while inserting
`r^2` or `r^4` gives `1/pi^2-6/pi^4` or
`1/pi^2-20/pi^4+120/pi^6`; angular factors are `1/3` and `1/5`.
Consequently the variance of `z^2`, in `R^4` units, is

\[
 V_z=\frac4{45}-\frac8{3\pi^2}+\frac{20}{\pi^4}>0,
 \qquad
 M_{1,k}=\frac{M R^4 k^4}{8}V_z+O(k^6).                  \tag{10}
\]

This is the deterministic fluid version of (7), not an exact finite-N
factorization assertion. The independently reviewed static fluid result is

\[
 \chi_{D,k}=\frac{k^4R^7}{G}C+O(k^6),\qquad
 C=\frac2{9\pi^2}-\frac4{189}>0.                            \tag{11}
\]

The frequency moment tested by a complete dynamical shared-mode
calculation is therefore

\[
 \Omega_{\rm eff}^2:=\frac{M_{1,k}}{M_{-1,k}}
       =\frac{2M_{1,k}}{\chi_{D,k}}
       \longrightarrow\frac{GM}{R^3}\frac{V_z}{4C}.
                                                               \tag{12}
\]

This is an inverse-moment weighted squared frequency, not a claim that a
single pole or all modes have this frequency. It incorporates both the
cubic l=1 and l=3 physical source components. Equations (8), (11) and
(12) are an independent normalization target for their actual dynamical
mode sums. The source dependence still suppresses the susceptibility by
`(kR)^4`; cancellation in the ratio does not turn it into a local
acceleration susceptibility or predict the target `1/(4pi G)`.

## 5. Evidence and boundary of the result

Equations (3)–(7) are exact commutator algebra under (1)–(2) and the domain
conditions above. Equations (8)–(12) are conditional fluid/mode statements
in the declared n=1 common-profile approximation. They are derived here
without another numerical run or modifications to the completed occupation
runner. The parent separately checked (3), (4), (7) and (9) before this
supplement was written; that review is scoped separately in its packet.

The static input (11) was independently audited in `FINITE_K_REVIEW.md`,
which pins its exact source bytes and validates its completed finite
controls. No assertion of microscopic formation, stable baryon closure,
finite-GP surface convergence, state occupations or saturation follows from
the new internal sum rule alone.
