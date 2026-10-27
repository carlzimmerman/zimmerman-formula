# Independent raw derivation: a four-dimensional regulator

Version 1, saved 2026-10-19 UTC. Author: independent subagent
`four_dimensional_regulator`. No target report or other author's derivation was
read before this file was saved. This is an analytic derivation, not a
computational experiment; no CAS, numerical sum, or fitted coefficient supports
the conclusion. The only mathematical inputs are the operators and conventions
in the assignment and elementary Gaussian/Feynman-parameter integrals derived
below. Corrections, if any, must be saved as a new version.

## Claim and conventions

Take connection-normalized fields, so that the charged adjoint frequencies are
`w_n = 2 pi n/L + h`; equivalently, the specified holonomy is
`nu = L h/(2 pi)`. Let `0 < nu < 1`, and work locally in this gapped chamber.
Define the two-derivative loop action **without an extra factor 1/2** by

\[
 \Gamma_{1,2}=\int_{\mathbb R^3}d^3x\,
 \{K_B(h) B_iB_i+K_E(h)\partial_i h\partial_i h\}.
\]

Here `B_i = epsilon_ijk F^3_jk/2`. These are coefficients in the
three-dimensional action after integrating the circle. Coefficients in the
circle-averaged four-dimensional density are `K/L`. The neutral adjoint sector
has no background-dependent two-derivative contribution. The charged real
adjoint plane is counted exactly once as the two roots below.

For the specified physical-minus-regulator subtraction, with the **same**
four-dimensional PV mass `M` in the vector and ghost operators, the bulk result
is

\[
 \boxed{\lim_{M\to\infty}(K_E^{\rm PV}-K_B^{\rm PV})
       ={L\over24\pi^2}.}
\]

Thus the difference in the four-dimensional density is `+1/(24 pi^2)`.
An equal electric/magnetic counterterm cannot change this difference. A density
convention `Gamma = (1/2) integral (k_B B^2 + k_E E^2)` instead has
`k_E-k_B = L/(12 pi^2)`.

This is a statement about the fully integrated-by-parts **bulk** density. The
local diagonal density has the opposite difference and contains a compensating
total derivative. A condition discarding that derivative is part of identifying
the bulk density with the full action on a region.

## 1. Multiplicity and scalar integrals

Continue the spatial dimension to `d`, if desired, and put `D=d+1`. For the two
charged roots, reality and the factor `1/2` in the vector determinant give

\[
 \Gamma_{\rm charged}=
 \sum_n\left\{\operatorname{tr}_{D}\log(K_n\delta+S)
                          -2\log K_n\right\},
 \qquad S_{\mu\nu}=-2iF^3_{\mu\nu}.
\]

The two root spectra have been identified by `n -> -n`. The remaining scalar
orbital multiplicity is `D-2=d-1`, not `D` and not `D-1`. Set

\[
 K_n=-D_i^2+m_n^2,\quad m_n^2=w_n^2+M^2,
 \quad I_r(m)=\int {d^d p\over(2\pi)^d}(p^2+m^2)^{-r}.
\]

For `r > d/2`, the proper-time representation and Gaussian integral give

\[
 I_r=(4\pi)^{-d/2}{\Gamma(r-d/2)\over\Gamma(r)}m^{d-2r},
 \qquad {I_3\over I_2}={4-d\over4m^2}.
\]

In particular, `I_2 = 1/(8 pi m)` and `I_3 = 1/(32 pi m^3)` for `d=3`.

## 2. Scalar orbital electric bubble, already in bulk form

Expand about constant `h`, with fluctuation `eta`. The scalar mass perturbation
is `delta V = 2w eta + eta^2`, even for a PV field: the regulator contributes
`M^2` to the propagator, but **does not** change `2w eta` to `2m eta`.
The momentum-dependent quadratic determinant term is

\[
 -2w^2\eta(k)\eta(-k)\,\mathcal B(k),\quad
 \mathcal B(k)=\int_0^1dx\int{d^dp\over(2\pi)^d}
 [p^2+m^2+x(1-x)k^2]^{-2}.
\]

Since `integral_0^1 x(1-x) dx = 1/6`,

\[
 \mathcal B(k)=I_2-{k^2\over3}I_3+O(k^4),
 \qquad C^{\rm scalar}_{E,\,bulk}={2\over3}w^2I_3
          ={4-d\over6}{w^2\over m^2}I_2.
\]

The seagull `eta^2` contributes no momentum dependence. The coefficient above
is the one in the action, i.e. it has no unremoved `h Delta h` term.

## 3. Scalar orbital magnetic term

For a single magnetic plane, the scalar heat kernel relative to the free one
contains `Bs/sinh(Bs) = 1 - B^2s^2/6 + O(B^4)`. Using
`Tr log K = - integral_0^infty ds Tr exp(-sK)/s` therefore yields

\[
 C_B^{\rm scalar}={1\over6}I_2.
\]

This factor also follows by expanding the minimal scalar gauge-field bubble
and its seagull. It refers to `B^2 = F_ij F_ij/2`, for a selected magnetic plane.

## 4. Vector spin term

The linear spin trace vanishes. At two derivatives,

\[
 \delta\Gamma_{\rm spin}
 =-{1\over2}I_2\operatorname{tr}_{D}S^2,
 \qquad \operatorname{tr}_{D}S^2=4F_{\mu\nu}F_{\mu\nu}.
\]

Consequently,

\[
 \delta\Gamma_{\rm spin}=-4I_2(B^2+E^2),\qquad E_i=\partial_i h.
\]

At this order the propagator can be evaluated at constant `h`. Derivatives of
it accompanying two spin insertions would be higher order. There is no mixed
one-spin/orbital contribution because its Lorentz trace is zero. The spin term
does not affect `K_E-K_B`.

## 5. Four-dimensional PV subtraction

At exactly `d=3`, including both charged roots,

\[
 K_B(w,M)=\left({2\over6}-4\right)I_2(m)=-{11\over3}I_2(m),
\]

\[
 K_E(w,M)=\left({1\over3}{w^2\over m^2}-4\right)I_2(m),
\]

and hence

\[
 K_E(w,M)-K_B(w,M)
     =-{M^2\over3m^2}I_2(m)
     =-{M^2\over24\pi(w^2+M^2)^{3/2}}.
\]

The physical massless operator has zero difference at every gapped KK mode.
The physical-minus-regulator action therefore has

\[
 \Delta K^{\rm PV}(M)
 ={1\over24\pi}\sum_{n\in\mathbb Z}
 {M^2\over[(2\pi n/L+h)^2+M^2]^{3/2}}.
\]

This sum is absolutely convergent at finite `M`. Let `a=ML/(2pi)`. It equals

\[
 \Delta K^{\rm PV}(M)
 ={L\over48\pi^2}\sum_n
 {a^2\over[(n+\nu)^2+a^2]^{3/2}}.
\]

The sum is a Riemann sum with mesh `1/a`:

\[
 \sum_n {a^2\over[(n+\nu)^2+a^2]^{3/2}}
 ={1\over a}\sum_n[1+((n+\nu)/a)^2]^{-3/2}
 \longrightarrow\int_{-\infty}^{\infty}{dt\over(1+t^2)^{3/2}}=2.
\]

The integrand and its tails are integrable; a central compact interval plus
uniform tail bounds justify this limit for each fixed gapped `nu`. Thus
`Delta K -> L/(24 pi^2)` independently of `nu`.

For completeness the common, logarithmically divergent magnetic coefficient is
specified without choosing a renormalization convention by

\[
 K_B^{\rm PV}(M)=-{11\over24\pi}\sum_n
 \left\{{1\over|w_n|}-{1\over\sqrt{w_n^2+M^2}}\right\}.
\]

The electric coefficient is this expression plus `Delta K^PV(M)`. Both sums are
well defined at finite `M`; the common logarithm is removed by the ordinary
equal electric/magnetic gauge kinetic counterterm.

## 6. Independent spatial-dimensional continuation

Put `d=3-2epsilon`, with the vector having `D=d+1=4-2epsilon` components and the
ghost multiplicity unchanged. At `M=0`,

\[
 K_B(d)=\left({d-1\over6}-4\right)\sum_n I_2(|w_n|),
\]

\[
 K_E(d)=\left({(d-1)(4-d)\over6}-4\right)\sum_n I_2(|w_n|),
\]

so that

\[
 K_E(d)-K_B(d)={(d-1)(3-d)\over6}\sum_n I_2(|w_n|).
\]

For `epsilon>0`, the sum is absolutely convergent and is exactly

\[
 \sum_n I_2=(4\pi)^{-3/2+\epsilon}\Gamma(1/2+\epsilon)
 (L/2\pi)^{1+2\epsilon}
 \{\zeta(1+2\epsilon,\nu)+\zeta(1+2\epsilon,1-\nu)\}.
\]

An optional renormalization factor `mu^(2epsilon)` cannot change the following
finite difference. The pole is obtained directly from comparison of the large
`n` tails with `2 sum n^(-1-2epsilon)`:

\[
 \sum_n I_2={L\over16\pi^2\epsilon}+O(1),\qquad
 {(d-1)(3-d)\over6}={2\epsilon\over3}+O(\epsilon^2).
\]

Thus the dimensionally regulated bulk difference is also `L/(24 pi^2)`.
Setting `d=3` mode by mode before summation discards this epsilon-times-pole
term. Correct vector multiplicity is displayed explicitly; even a different
vector-count prescription must first be analyzed before assuming finite parts
agree.

## 7. Local diagonal versus integrated-by-parts bulk density

For the scalar operator `-partial^2+V(x)`, the two-derivative diagonal heat
kernel is

\[
 \langle x|e^{-sK}|x\rangle
 ={e^{-sV}\over(4\pi s)^{d/2}}
 \{1-{s^2\over6}\Delta V+{s^3\over12}(\partial V)^2+O(\partial^4)\}.
\]

For `V=w^2+M^2`, the corresponding logarithmic diagonal density is

\[
 \mathcal L^{\rm scalar}_{2,diag}
 =\left({I_2\over3}-{2w^2I_3\over3}\right)E^2
       +{wI_2\over3}\Delta h.
\]

Because `dI_2/dw=-4wI_3`, this identity can be rewritten exactly as

\[
 \mathcal L^{\rm scalar}_{2,diag}
 ={2w^2I_3\over3}E^2
       +\partial_i\left({wI_2\over3}\partial_i h\right).
\]

The first term agrees with the electric bubble. The second term is a genuine
local total derivative, not a zero identity.

After summing the two charged-root orbital multiplicity and subtracting PV at
`d=3`, the total derivative has coefficient

\[
 A_M(h)={1\over12\pi}\sum_n
 \left\{\operatorname{sgn}(w_n)-{w_n\over\sqrt{w_n^2+M^2}}\right\},
 \quad\mathcal L_{diag}^{PV}=\mathcal L_{bulk}^{PV}
           +\partial_i[A_M(h)\partial_i h].
\]

At finite `M`, this sum is absolutely convergent. Within the chamber, where the
derivative of `sgn(w_n)` is zero,

\[
 A'_M(h)=-{1\over12\pi}\sum_n
 {M^2\over(w_n^2+M^2)^{3/2}}
        =-2\Delta K^{PV}(M).
\]

Reflection about `nu=1/2` gives `A_M(pi/L)=0`, while the same Riemann-sum limit
as above gives, uniformly on compact subintervals of the chamber,

\[
 A_\infty(h)={1-2\nu\over12\pi},\qquad
 A'_\infty(h)=-{L\over12\pi^2}.
\]

Therefore the coefficient of `E^2` in a local diagonal density with the
`A(h) Delta h` term left present has

\[
 (K_{E,diag}-K_B)=-{L\over24\pi^2},
\]

whereas the fully IBP bulk density has the positive value stated at the start.
They differ by the displayed divergence. In dimensional continuation the local
diagonal difference is `(d-1)(d-3) sum I_2/6`, and gives the same negative finite
answer; analytic continuation of the coefficient of `Delta h` gives
`A_infinity(h)` above.

For a bounded spatial region the action also contains the surface integral
`integral_boundary A(h) normal_dot_grad h`. It may not be dropped if the
boundary conditions or falloff make it nonzero. For a smooth perturbation of a
constant gapped holonomy with sufficiently rapid falloff (or compatible periodic
boundary conditions within a single smooth chamber), that surface integral
vanishes. Crossing an integer holonomy leaves the gapped regime and requires
separate treatment; it cannot be used to discard chamber-wall distributions.

## 8. Exact constant-electric oscillator check

Choose `h(x_1)=h_0+E x_1`, with `A_i=0`, and consider a local point with signed
frequency `w=w_n(x_1)`. For each mode the `x_1` operator is a harmonic oscillator
with potential `(w_n(0)+E x_1)^2+M^2`. Its exact diagonal kernel is

\[
 K_{scalar}(x,x;s)={(4\pi s)^{-3/2}}e^{-sM^2}
 \left({2Es\over\sinh(2Es)}\right)^{1/2}
 \exp\left[-{w^2\over E}\tanh(Es)\right].
\]

Its small-`E` expansion at fixed local `w` is

\[
 {(4\pi s)^{-3/2}}e^{-s(w^2+M^2)}
 \{1-E^2s^2/3+w^2E^2s^3/3+O(E^4)\}.
\]

This exactly checks both diagonal scalar derivative coefficients above when
`Delta h=0`: `Delta V=2E^2`, `(partial V)^2=4w^2E^2`.

For the charged vector-plus-ghost determinant in four dimensions, the spin
weight is

\[
 \operatorname{tr}_4e^{-sS}-2=2\cosh(2Es).
\]

Multiplying the scalar expansion by this factor gives

\[
 2+{10\over3}E^2s^2+{2\over3}w^2E^2s^3+O(E^4).
\]

The logarithmic density therefore has electric coefficient

\[
 K_{E,diag}(w,M)=-{10\over3}I_2-{4\over3}w^2I_3
       =-{11\over3}I_2+{M^2\over3m^2}I_2.
\]

The exact constant-magnetic heat kernel has scalar factor `Bs/sinh Bs` and
vector-plus-ghost spin factor `2cosh(2Bs)`. Its quadratic coefficient gives
`K_B=-11 I_2/3`. Thus the oscillator independently checks the local diagonal
PV difference (negative after subtraction), and the explicit divergence in
section 7 converts it to the bulk bubble result (positive after subtraction).

An affine `h` over the whole real line crosses gapless chamber walls and fails
the falloff assumptions. Its globally integrated oscillator trace cannot be
substituted for the action of a compact, everywhere-gapped perturbation. The
oscillator is used here as an exact *local diagonal* check only.

## Audit obligations and scope

Dependency graph: operator and real-adjoint determinant convention -> charged
root counting -> scalar bubble plus magnetic scalar kernel and vector spin
trace -> PV subtraction and convergent Riemann-sum limit -> bulk difference.
Independent branch: the same elementary Gaussian integral -> dimensional pole
and epsilon factor -> matching bulk difference. Exact oscillator -> local
diagonal coefficients -> displayed IBP identity -> matching bulk difference.

Passed analytically: root/vector/ghost multiplicity; electric scalar bubble;
massive PV holonomy vertex; magnetic coefficient; spin equality; convergent
PV sum; dimensional pole; explicit divergence; exact oscillator expansion.
Conditional for identifying bulk with full action: vanishing of the displayed
surface integral. Out of scope: endpoints/gap closing, nonlocal derivative
terms, unstable globally constant backgrounds, interactions beyond one loop,
any physical fine-structure or QCD prediction. No external theorem or numerical
computation is a leaf of this argument.

Primary analytic verdict: **proved as written**, for the boxed claim with the
density convention and local gapped derivative-expansion scope specified here.
This is a self-review of the raw derivation, independent of the target reports;
comparison/audit of those reports has not yet occurred.

## Executed-input provenance before this save

No mathematical computation was executed. Tools were used only to read the
proof-audit/using-superpowers skill text, look for applicable `AGENTS.md`, and
create the permitted report directory. The initial attempted read of a
nonexistent `.codex/skills/superpowers/SKILL.md` failed and was corrected to the
catalog path. No target report or candidate coefficient was supplied or read.
The exact formulas, normalizations, and integral reductions used for the
analytic result are preserved in this versioned file.
