# Occupations and source spectra of a shared bound state

19 October 2026. Lane: `occupations`; parent CE-SCALAR-DIPOLES-2026-10-19 /
CE-FM090. Only this directory is written. The original objective remains open.
Input bytes and observed HEAD are pinned in `source_pins.json`.

**Result.** A specified stable shared equilibrium supplies a source-specific
joint mode measure, and a specified energy or preparation supplies its
occupations. The formulas below perform those two maps without inserting the
target weight. Harmonic modes have an occupation-independent response and
unbounded excitation ladders; their occupied counts do not become independent
saturating sites. A separate exact restriction is that a parity-symmetric,
isolated, gapped ground state with a bounded physical source operator cannot
have the rational response arbitrarily close to zero field. This restriction
applies also in an infinite-dimensional Hilbert space under the explicit gap
and bounded-source hypotheses. It does not assert a gap for every fluid,
collisionless, relativistic, or critical phase of the original action.

## 1. Conserved quantities and equilibrium selection

Use the original minimally coupled scalar model and its retained positive
nonrelativistic branch from the parent packet. In a daughter-only, source-
eliminated regime, the scalar inventory is `Q=N_d`, and the leading mass is
`mQ`. If the source branch is retained, `Q=N_Phi+2N_X` is conserved by the
retained conversion Hamiltonian, while `N_Phi` and `N_X` separately are not.
This positive NR inventory is not the full signed relativistic charge, and
the reference-mass density is not a substitute for the relativistic stress.
Ordinary baryon numbers are separately conserved in the stated model.

Let `H_{Q,N_b}` be the complete internal Hamiltonian of one shared object at
fixed inventories, with its common COM removed. A thermal state, if this
trace exists, is

\[
 Z_{Q,N_b}(\beta)=\operatorname{Tr}_{Q,N_b}e^{-\beta H},\qquad
 p_\alpha=Z^{-1}e^{-\beta E_\alpha}.                         \tag{1}
\]

The alternative grand canonical description is
`exp[-beta(H-mu_Q Q-sum_b mu_b N_b)]/Z`. Conversion chemical equilibrium
requires `mu_Phi=mu_Q`, `mu_X=2mu_Q`; two arbitrary scalar chemical potentials
would impose a nonexistent conservation law. These Lagrange multipliers are
fixed by specified mean inventories, not by a new action parameter.

For a closed object with energy in `[E,E+delta E]`, replace (1) by the
normalized spectral projector on that shell. Thus even an equilibrium
prediction is conditional on `Q,N_b,E` or entropy, angular momentum where
relevant, and the actual baryon stress/phase. The action and a static density
profile do not specify those data. A collisionless stationary distribution
has still more conserved fine-grained data and need not equal (1).

There is also an ensemble-domain issue. An isolated Newtonian object in
unbounded space has translational phase volume and evaporation/scattering
phase volume. Removing the COM removes only the former. A breakup channel
with asymptotically finite energy has arbitrarily large relative separation,
so its finite-temperature canonical trace is not normalizable without
confinement or another restriction. A finite-box Gibbs state, or a local
metastable mode ensemble inside a bound basin, must therefore be declared.
Neither is claimed to be an exact global Gibbs state of an open halo.

## 2. Actual normal-mode pushforward, with the complete source

Suppose another lane supplies a stable equilibrium and canonical positive
internal modes. In the conservative displacement description choose modes
`xi_{a nu}` normalized by the *shared* mass metric,

\[
 \sum_a\int\rho_{a0}\,\boldsymbol\xi_{a\nu}\cdot
          \boldsymbol\xi_{a\mu}\,d^3x=\delta_{\nu\mu},\qquad
 H_2=E_0+\frac12\sum_\nu(p_\nu^2+\Omega_\nu^2q_\nu^2).
                                                               \tag{2}
\]

Set `hbar=1`; frequencies in this note are energy spacings. The sum includes
all participating scalar and baryon components once. Positive Hessian modes
and a valid mass metric are assumptions here, not an extra proof of the
equilibrium. More general canonical Bogoliubov modes give the same formulas
after a symplectic diagonalization and a direct source-matrix-element
calculation; a displacement ansatz does not cover all kinetic baryon phases.

For an external Newtonian potential `U_ext=-g h(x)`, define

\[
 D_h=\int h(x)\rho(x)d^3x,\quad H_{\rm src}=-gD_h,\quad
 c_\nu=\sum_a\int\rho_{a0}\boldsymbol\xi_{a\nu}\cdot\nabla h\,d^3x.
                                                               \tag{3}
\]

Mass conservation `delta rho_a=-div(rho_a xi_a)` proves (3) by integration
by parts, including the appropriate free-surface contribution. The linear
operator is `delta D_h=sum_nu c_nu q_nu`. Consequently

\[
 d_\nu=|\langle1_\nu|D_h|0\rangle|
       =\frac{|c_\nu|}{\sqrt{2\Omega_\nu}},\qquad
 \nu_{\rm mode}(dd\,d\Omega)=\sum_\nu
       \delta_{d_\nu}(dd)\delta_{\Omega_\nu}(d\Omega).          \tag{4}
\]

This is a source-specific joint measure derived from actual modes. Divide
by a declared averaging volume for a density. It need not be continuous,
and a different spatial probe has different `c_nu,d_nu`. For uniform
`h=e.x`, every internal COM-orthogonal mode has `c_nu=0`: the sum over all
components is essential. No baryonic host is replicated for each scalar
mode. A bounded finite-wavelength example is `h_k=sin(kz)/k`.

In the stated canonical quadratic approximation the trace factorizes:

\[
 \bar n_\nu=(e^{\beta\Omega_\nu}-1)^{-1},\quad
 E_{\rm exc}=\sum_\nu\Omega_\nu\bar n_\nu,\quad
 \nu_{\rm occ}=\sum_\nu\bar n_\nu
       \delta_{(d_\nu,\Omega_\nu)}.                            \tag{5}
\]

There is no independently conserved oscillator/phonon number in this
Hamiltonian. The Bose law in (5) follows from the declared oscillator trace;
it is not an exact finite-particle identity for the full scalar Hamiltonian.
Finite-inventory depletion, self-consistent condensate corrections and
nonbosonic corrections can change it. The exact sector trace (1) remains
the definition. At the quadratic level a specified energy fixes `beta`
uniquely when attainable, since

\[
 \frac{dE_{\rm exc}}{d\beta}
 =-\sum_\nu\Omega_\nu^2\bar n_\nu(1+\bar n_\nu)<0.            \tag{6}
\]

An explicit microcanonical version, for a finite mode set, is
`P({n_nu}) proportional to 1_{E<=sum Omega_nu n_nu<E+delta E}`;
then `nu_occ` uses the corresponding shell means. This determines conditional
occupations without postulating an independent chemical potential for each
mode. It does not determine the object's formation energy.

There is also a direct preparation map. A prescribed weak classical pulse
`g(t)` acting on (2) creates coherent amplitudes

\[
 |\alpha_\nu|^2=d_\nu^2|\widetilde g(\Omega_\nu)|^2,\qquad
 \bar n_{\nu,\mathrm{after}}=\bar n_{\nu,\mathrm{before}}
                                  +|\alpha_\nu|^2.            \tag{7}
\]

This follows by integrating the interaction-picture forced-oscillator
equation; it is exact for the driven quadratic system. For a Gaussian pulse
`g(t)=g0 exp[-t^2/(2 tau^2)]`, the actual created population is
`2 pi g0^2 tau^2 d_nu^2 exp[-Omega_nu^2 tau^2]`. Its energy is
`sum Omega_nu |alpha_nu|^2`. Specifying the pulse or physical capture process
is necessary; replacing its transform by a chosen gap weight is not a
production prediction.

## 3. Response strengths are not occupied oscillator counts

For each mode, transitions from `n` to `n+1` have matrix element
`d_nu sqrt(n+1)`. Therefore its absorption and emission line strengths are
respectively `d_nu^2(nbar_nu+1)` and `d_nu^2 nbar_nu`. Their difference is
`d_nu^2`, independently of occupation. Explicitly, for any normalized
stationary oscillator distribution with a finite first moment,

\[
 \sum_{n\ge0}(p_n-p_{n+1})(n+1)=1.                          \tag{8}
\]

The boundary term vanishes for a Gibbs distribution. Thus

\[
 S_{\rm K}(\omega)=\sum_\nu d_\nu^2\delta(\omega-\Omega_\nu),\quad
 \chi_h(0)=2\sum_\nu\frac{d_\nu^2}{\Omega_\nu}
          =\sum_\nu\frac{c_\nu^2}{\Omega_\nu^2}.               \tag{9}
\]

Equivalently complete the square in (2):
`q_nu -> q_nu-g c_nu/Omega_nu^2`. The free energy shift is exactly
`-g^2 chi_h/2`, so `P_h=<D_h>-<D_h>_0=chi_h g` at every temperature for
which this quadratic approximation applies. There is no saturation. Even
the vacuum (`nbar=0`) has (9). Multiplying (9) by an occupied count double
counts thermal factors. Conversely, temperature can alter the equilibrium,
mode frequencies and source overlaps once nonlinear backreaction is kept;
occupation independence is not asserted across such different backgrounds.

For a general Gibbs state the positive response measure is instead

\[
 S_{\rm K}(\omega)=\sum_{E_\beta>E_\alpha}
 (p_\alpha-p_\beta)|D_{\alpha\beta}|^2
       \delta(\omega-E_\beta+E_\alpha).                       \tag{10}
\]

The off-diagonal susceptibility is `2 integral S_K/omega`; an isothermal
static susceptibility can additionally contain diagonal/degenerate
population terms. In the parity-symmetric nondegenerate situation used
below the diagonal matrix elements of the odd `D_h` vanish, and (10) is
the full static result. Formula (10), or its canonical-sector version,
is the exact source/state map. It does not decompose a many-level object
into independent saturating sites: different transitions share states.
The normal-mode formulas are an explicit tractable specialization.

## 4. A precise infrared restriction on the exact rational law

Consider the signed response along one axis. Rotationally symmetric
`P_vec=p_sat g_vec/(a+|g_vec|)` restricts to

\[
 P_*(g)=\frac{p_{\rm sat}g}{a+|g|}
 =\frac{p_{\rm sat}}a g-\frac{p_{\rm sat}}{a^2}g|g|+O(g^3).
                                                               \tag{11}
\]

This is continuously differentiable but has unequal one-sided second
derivatives at zero, `P_*''(0+)=-2p_sat/a^2` and the opposite sign on the
left. Treating `g` only as a nonnegative magnitude does not remove this
test: an isotropic constitutive law must extend to signed physical fields.

**Ground-state theorem.** Let `H(g)=H0-gD` be self-adjoint, `D` bounded,
and let the internal ground eigenvalue of `H0` be simple and isolated by
`gamma>0` from the rest of its spectrum. Let a unitary inversion `I` obey
`I H0 I^-1=H0`, `I D I^-1=-D`. Then its ground energy is an even real
analytic function near zero, and `P(g)=-E0'(g)` is odd analytic:

\[
 P(g)=\chi g+c_3g^3+O(g^5).                                \tag{12}
\]

Here is an operator-level proof, including an infinite-dimensional
continuum Hilbert space when these hypotheses hold. On a spectral contour
of radius `gamma/2` about the ground eigenvalue,
`||(z-H0)^-1||<=2/gamma`. For `|g| ||D||<gamma/2` the resolvent of `H(g)`
has an operator-norm convergent Neumann series in `g`. Its contour integral
is an analytic rank-one spectral projector. The continued eigenvalue is
analytic, remains isolated locally, and inversion equates its values at
`g` and `-g`. Differentiating its eigenvalue gives (12). Taking the contour
away from a threshold is essential. Thus (11) cannot equal (12) on any
neighborhood of zero. If the linear slopes match, the discrepancy is
`P(g)-P_*(g)=(p_sat/a^2)g|g|+O(g^3)`.

This has a useful physical application beyond a finite matrix regulator.
For a fixed positive Newtonian mass inventory and bounded `h_k`,
`D_k=sum_i m_i h_k(x_i)` has

\[
 \|D_k\|\le M_{\rm tot}/|k|.                              \tag{13}
\]

The COM-reduced source remains bounded. The theorem applies to such a
finite object *if* its internal ground state is isolated below every
fragmentation/continuum channel and has the stated inversion symmetry.
Infinite spatial volume alone does not invalidate this proof. Conversely,
positive classical stability alone does not establish its spectral gap.
No claim of a gap is made for a collisionless continuum, zero-frequency
vortical sector, singular free-surface limit, marginal state or infinite
object. The full relativistic stress operator with unrestricted pair
sectors is not bounded by (13) at fixed signed charge, and lies outside
this theorem. The leading uniform gravitational source gives the already
known internal cancellation rather than a nonzero rational response.

At finite temperature a finite-dimensional Gibbs partition function is
analytic and positive for real `g`. Inversion makes it even, hence its
response is again odd analytic. The same conclusion in an infinite
Hilbert space requires a trace-class Gibbs operator and analytic trace
domination near zero. We do not assume this for an unconfined halo. A
finite mode harmonic Gibbs model has that property directly by completing
the square and yields exactly (9).

The restriction is local in field. It permits finite-window approximation,
nonanalytic critical/infinite-volume limits, ensembles whose gap distribution
extends to zero, or an action/state outside these hypotheses. It does not
constitute a universal all-phase no-go for the original theory.

## 5. What a finite reduced-gap window actually does

For comparison only, assume genuine independent *ground-state two-level
sites* have already been established. With their proposed target weight
`w(Delta)=p_sat a Delta/(a^2+Delta^2)^(3/2)`, truncate to
`epsilon<=Delta<=L`. This is an imposed diagnostic spectrum, not the
normal-mode measure (4). For `g>0`, its response is exactly

\[
 P_{\epsilon,L}(g)=\frac{p_{\rm sat}ag}{g^2-a^2}
 \left[\sqrt{\frac{g^2+\epsilon^2}{a^2+\epsilon^2}}
       -\sqrt{\frac{g^2+L^2}{a^2+L^2}}\right].               \tag{14}
\]

The removable `g=a` value is
`p_sat a^2[1/(a^2+epsilon^2)-1/(a^2+L^2)]/2`. The antiderivative follows
by setting `u=(a^2+Delta^2)^(-1/2)` in the site integral. The limits
`epsilon->0,L->infinity` give `P_*(g)=p_sat g/(a+g)`.

For every fixed positive cutoff, the small-field expansion is odd analytic,

\[
 \chi_{\epsilon,L}=\frac{p_{\rm sat}}a
 \left[\frac{L}{\sqrt{a^2+L^2}}-
       \frac{\epsilon}{\sqrt{a^2+\epsilon^2}}\right],\qquad
 c_3=-\frac12\int_\epsilon^L\frac{w(\Delta)}{\Delta^3}d\Delta.
                                                               \tag{15}
\]

In particular `c3~-p_sat/(2a^2 epsilon)` as the IR cutoff vanishes.
The nonlinear Taylor coefficients do not have a uniform cutoff limit;
that failure produces the cusp. Bounded source matrix elements `d<=Dmax`
and actual ground-state transition gaps `Omega>=gamma` imply
`Delta>=gamma/(2Dmax)`, so a single object satisfying the theorem cannot
supply the exact soft endpoint. An ensemble of different object masses or
softness scales may evade a *uniform* lower cutoff, but its inventory
distribution then requires separate selection. The variable-d integrability
loophole from the parent is preserved; its divergent soft `d` cannot be
realized as matrix elements of one fixed bounded `D`.

A useful finite-window, nonasymptotic error certificate is

\[
 0\le\frac{P_*(g)-P_{\epsilon,L}(g)}{P_*(g)}
 \le\frac{\epsilon^2(a+g_{\min})}{2a^2g_{\min}}
  +\frac{a+g_{\max}}a
       \left[1-\frac{L}{\sqrt{a^2+L^2}}\right]               \tag{16}
\]

for `0<g_min<=g<=g_max`. The IR bound uses
`int_0^epsilon w<=p_sat epsilon^2/(2a^2)` and a kernel at most one; the UV
bound uses the kernel at most `g/Delta` and its exact inverse moment.
For example, in units `a=p_sat=1`, `epsilon=.01,L=100` gives an upper
relative error below `.00110` on `.1<=g<=10`. This demonstrates that the
exact analytic obstruction alone need not be observationally large on a
finite field interval. The cutoffs and the site's physical existence
remain unpredicted. No production-energy or f-sum obstruction is retested.

If such sites are instead genuinely thermal, their exact two-level response
contains an additional state factor,

\[
 P_\beta(g)=\int w(\Delta)\frac{g}{\sqrt{g^2+\Delta^2}}
 \tanh\!\left[\beta d(\Delta)\sqrt{g^2+\Delta^2}\right]d\Delta,
\quad
 \chi_\beta=\int\frac{w(\Delta)}\Delta
                 \tanh[\beta d(\Delta)\Delta]d\Delta.       \tag{17}
\]

For finite temperature and finite `d(Delta)` almost everywhere with positive
weight, `chi_beta<chi_0`. Thus the same ground-state target weight no longer
has its target normalization, even before the source-overlap test. A thermal
population is not innocuous in a saturating two-level construction, in
contrast to a harmonic oscillator. Retuning its inventory would itself be a
new state-selection requirement.

## 6. Source check, verification and remaining arrow

Gardiner and Morgan, [cond-mat/0610623v2](https://arxiv.org/html/cond-mat/0610623v2),
Section V.2.3, equations (98)–(101), and Section V.3 explicitly discuss
number-conserving quasiparticle thermodynamics, finite-number corrections
and the approximate bosonic algebra. Their population formula includes
the `mu-lambda0` correction. This is a guardrail on extending (5); it is
not cited as proof of exact Bose occupations at finite scalar inventory.
The source was authenticated by its arXiv version header and the formulas
were read directly on 2026-10-19. No source text or PDF is copied here.
Equations (1)–(17) are derived in this note; no novelty claim is made.

`check_occupations.py` supplies bounded algebra controls: a three-mode
positive oscillator system, spectral response versus stiffness inverse,
thermal and driven populations, complete small microcanonical shells, a
four-state parity-symmetric exact quantum model, and independent quadrature
checks of (14)–(17). These controls do not construct an original-model
shared equilibrium. The command, tested range, versions, source pins and
runner-v2 manifest are recorded alongside it. Results are self-review;
an independent parent review, if performed, must state its exact scope.

The missing physical arrow is now specific: a state/formation model must
supply the shared equilibrium, source-carrying normal modes and their
inventories/energy, then an actual nonlinear continuation or genuine
finite-level local objects. It must explain a sufficiently soft family if
the rational law is intended to be exact at zero field. Neither a static
equilibrium, an arbitrary occupation count, nor its harmonic spectrum
already fixes saturation or `p_sat/a=1/(4pi G)`.
