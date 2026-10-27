# The same attractive host has a fixed transition-overlap cost

Coordinator analytic derivation. Base: the exact existing orbital host in
`reviews/attraction_from_existing_2026_10_20/relaxation/RESULT.md`,
equations (6)-(8). The harmonic formulas below are a local approximation
to that host, not an added oscillator coupling or a canonical conversion
operator. A static density coupling cannot create an absent transition.

## 1. Quantize the already retained radial degree of freedom

The existing host radial kinetic energy is `p_q^2/(2M_h)`, with

\[
 V_h(n,q)={M_hj_h^2\over2q^2}
             -{GM_h(A+mn)\over q},\qquad
 A=M_0+M_h/2>0.
\]

Expand about `q_0=j_h^2/(GA)` at occupation zero and put `x=q-q_0`.
To harmonic order in `x/q_0` and leading order in `mn/A`,

\[
 H_h(n)={p_x^2\over2M_h}+{D x^2\over2}+fnx+c(n),
 \quad D={GM_hA\over q_0^3},\quad
 f={GM_hm\over q_0^2},\quad
 \Omega^2={D\over M_h}={GA\over q_0^3}.               \tag{1}
\]

The counted linear occupation energy `c(n)` includes the background
binding; it is not a free transition parameter. A branch-dependent
frequency and higher radial powers are corrections, not a second
receiver. Require `mn/A<<1`, small radial amplitude and zero-point width
compared with `q_0`, and occupied source/host/free supports separated as
in the prior proof. A thermal host additionally requires its actual
fluctuation amplitude to satisfy this same small-displacement condition.

The new minimum is displaced by `x_n=-fn/D`, giving

\[
 E_{h,\min}(n)=c(n)-{f^2n^2\over2D}+{\hbar\Omega\over2},
 \quad U_h=\Delta^2 E_{h,\min}=-{f^2\over D}.
\]

Here

\[
 {f^2\over D}={GM_hm^2\over Aq_0}
            ={G^2M_hm^2\over j_h^2},                 \tag{2}
\]

which agrees with the exact classical finite-curvature expression. This
agreement does not make the whole harmonic spectrum exact at finite `m`.

## 2. Derive the occupation-changing overlap, if an operator exists

Adjacent harmonic ground states differ in position by `d=f/D`. With
`x=sqrt(hbar/(2M_h Omega))(a+a^dagger)`, their coherent displacement has
squared amplitude

\[
 \boxed{S={M_h\Omega d^2\over2\hbar}
         ={f^2\over2\hbar M_h\Omega^3}
         ={|U_h|\over2\hbar\Omega}.}                 \tag{3}
\]

Thus the host reorganization energy is
`E_R=S hbar Omega=|U_h|/2`. The attraction and the receiver overlap are
fixed by the same existing parameters and state. They cannot be fitted
independently.

Suppose an actual existing cubic or quartic mode matrix element changes
the occupation by one. Call its value `v_fi`; this is a placeholder for
the computed original matrix element in the route notes, never a chosen
tunneling or attempt rate. If that matrix element varies negligibly over
the host's retained displacement and width, adiabatic factorization gives

\[
 \langle f,l|V|i,k\rangle
       =v_{fi}\langle l|\mathcal D(\pm\sqrt S)|k\rangle.
                                                               \tag{4}
\]

If the operator has appreciable `q` dependence, use the integral of the
two actual host wavefunctions and `v_fi(q)` instead. For an initially
unexcited host, the squared overlaps in (4) are exactly

\[
 F_{0l}=e^{-S}{S^l\over l!},\qquad
 \sum_{l=0}^{\infty}F_{0l}=1.                         \tag{5}
\]

Indeed `D(alpha)|0>=exp(-|alpha|^2/2)
sum_l alpha^l|l>/sqrt(l!)`. The zero-excitation probability is `e^-S`;
large `S` suppresses that line and redistributes probability to host
excitations. It does not suppress the inclusive sum to `e^-S`.

Given an actual continuum of incoming/outgoing scalar states, a justified
weak-coupling golden-rule kernel would be

\[
 W_{i k\to f l}={2\pi\over\hbar}|v_{fi}|^2F_{kl}\,
  \delta(E_f-E_i+\hbar\Omega(l-k)),                  \tag{6}
\]

integrated over the actual continuum density, occupations and host
initial probabilities. The energies in (6) already include the shifted
sector minima. Subtracting the reorganization energy again would double
count it. Hermiticity fixes the reverse amplitude with the same receiver
states. A host in its ground state cannot supply negative excitation
energy; an occupied excited host can return its stored energy.

## 3. What this receiver does and does not establish

Equation (6) is conditional on an actual continuum, initial state,
controlled weak-coupling/time-coarse-graining limit, and the original
nonzero scalar matrix element. A closed discrete host plus a few discrete
scalar modes instead has unitary oscillations/recurrences. It does not
produce a constant decay rate merely by writing a delta function. No
linewidth, external damping, stochastic noise, thermalization or attempt
frequency is inserted here.

In the collisionless spherical construction, the individual action
mismatch makes the desired transition absent; then `v_fi=0`, and a host
overlap cannot repair it. In the scalar routes, real collision partners
or a cubic reaction may supply the missing energy/angular-momentum
channel, but the common field-to-canonical-occupation dictionary must
still be derived. The host has finite energy storage; after loading it,
the same excited levels can promote reverse release unless its actual
transport removes that energy.

The result is therefore a calculable receiver factor tied to the derived
attraction, with no new coupling. It is not a numerical rate or a
retention prediction. Its interpretation is local to the stated harmonic
and adiabatic projection. Review provenance: coordinator self-review and
separately scoped reconstruction in `audit/RESULT.md`; no scientific
computation or external theorem is load-bearing.
