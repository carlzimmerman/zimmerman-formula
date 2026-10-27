# Conversion, condensate exchange, and capture from the particle action

2026-10-18 local date. Requested parent base: CE-FM-084,
`3d8900c10d8b778e2756838f2d00779dc43510ab`. Concurrent repository commits
continued during this task; the successful bounded run observed
`b794fb5fdf44e8f239c5edb8e235a7d057bef295` with a dirty worktree.
Exact unchanged input hashes are in `run_002/manifest.json`. Only this
`micro_exchange/` directory was written. The physical research remains open.

The original action has an exact source-to-daughter conversion current.
Its low-energy scattering amplitude also supplies a conditional, microscopic
bound/free population exchange kernel. These are different processes. Neither
identifies the CE082 settled density with a condensate or derives its
constraint `rho=div P`. The bounded new bridge here is the scattering matching,
reciprocal capture kernel, its binding-energy recipient and detailed balance,
plus one exact nonzero capture overlap in a declared auxiliary host.

## 1. What is already present

The nearest records are:

* `../../closure_particle_bridge_2026_10_16/COLD_DARK_ENERGY_AND_PARTICLE_BRIDGE.tex`:
  the charge-one carrier/charge-two source action,
  positive NR square, and energy/charge bound.
* `THERMAL_PHASE_AND_CHARGE_KINETICS.tex` in that directory: charge-resolved
  elastic amplitudes, source decay/inverse-decay kernel, four-species kinetics,
  neutral-population caveat and reciprocal mass-work terms.
* `SOURCE_ASSISTED_MATCHING_AND_RATES.tex` and
  `ASSISTED_EVOLUTION_AND_GALAXY_BRIDGE.tex`: five-point source-assisted
  reactions and their pole matching. This task does not recompute those rates.
* `../../microscopic_carrier_2026_10_10/REPORT.md`: Bose-gas condensate exchange
  was already proposed, with no match to this Phi/X action or resolved capture
  matrix element.
* `../../cold_continuation_2026_10_18/occupied_action/OCCUPIED_ACTION.md`:
  CE082 conserves the settled stock; it explicitly supplies no settled/free
  conversion term. Its W and material density are conditional effective inputs.

The separate complex-host/real-mediator droplet action is not combined with
the Phi/X action here.

## 2. Exact Noether sources are species conversion, not a phase label

Use `hbar=c=1`, signature `+---`, real source coupling `g_s`, and

\[
\mathcal L=|\partial\Phi|^2+|\partial X|^2
 -m^2|\Phi|^2-M^2|X|^2
 -g_s(X^*\Phi^2+X\Phi^{*2})-\lambda_{\rm tot}|\Phi|^4,
\quad M>2m.
\]

The species currents, defined with unit coefficient for each field, are

\[
j_\Phi^\mu=i(\Phi^*\partial^\mu\Phi-\Phi\partial^\mu\Phi^*),
\quad j_X^\mu=i(X^*\partial^\mu X-X\partial^\mu X^*).
\]

Substituting the two exact equations of motion gives

\[
\mathcal R=-2g_s\operatorname{Im}(X^*\Phi^2),\qquad
\partial_\mu j_\Phi^\mu=2\mathcal R,\quad
\partial_\mu j_X^\mu=-\mathcal R,\quad
\partial_\mu(j_\Phi^\mu+2j_X^\mu)=0.                    \tag{1}
\]

`R` is a signed coherent correlator, not a prescribed positive reaction rate.
In a quasiparticle kinetic limit, let `D_+` count net `X -> Phi+ Phi+`
decays and `D_-` their conjugates, including inverse decays and stimulation.
Then `R` coarse-grains to `D_+ - D_-`, while

\[
\dot n_{\Phi+}|_D=2D_+,\quad \dot n_{X+}|_D=-D_+,
\quad \dot n_{\Phi-}|_D=2D_-,\quad \dot n_{X-}|_D=-D_- .       \tag{2}
\]

Equal conjugate decays leave every net-charge source in (1) zero but create
four daughters per two decays. Thus exact charge conservation cannot be used
as a positive total-mass or total-number conservation law for a neutral bath.
Decay changes total rest energy at rate
`-(M-2m)(D_+ + D_-)`; on-shell daughter kinetic energy receives the opposite
amount. The full collision energy moment vanishes. Higher source-assisted
and number-changing channels already documented in the nearest records need
their own event stoichiometry and real-intermediate-state subtraction.

For example, the positive-source decay event rate is

\[
D_+=\frac1{2!}\int d\Pi_Xd\Pi_1d\Pi_2(2\pi)^4
 \delta^4(p_X-p_1-p_2)4g_s^2
 [f_X(1+f_1)(1+f_2)-(1+f_X)f_1f_2],                 \tag{3}
\]

with `dPi=d^3p/[(2pi)^3 2E]`. This is source/daughter conversion, even if a
final daughter happens to enter an occupied state. It is not automatically
capture of existing free daughters.

## 3. Fully matched contact coefficient and the older rotating-wave square

Set `Delta=M^2-4m^2` and
`lambda_tot=lambda_rep+g_s^2/Delta`, `lambda_rep>0` as in the original action.
Its existing vacuum same-charge tree amplitude is

\[
\mathcal M_{++}(s)=-4\left[\lambda_{\rm tot}
                 +\frac{g_s^2}{s-M^2}\right],\qquad
\mathcal M_{++}(4m^2)=-4\lambda_{\rm rep}.              \tag{4}
\]

The threshold-matched NR Hamiltonian is

\[
H_{\rm NR}=\int d^3x\left[\psi^*h\psi
       +\frac{g_N}{2}\psi^{\dagger2}\psi^2\right],\quad
g_N=\frac{\lambda_{\rm rep}}{2m^2},\quad
a=\frac{m g_N}{4\pi}=\frac{\lambda_{\rm rep}}{8\pi m}.       \tag{5}
\]

Indeed the identical-particle contact vertex is `-2i g_N`, and four external
relativistic normalization factors give `M=-8m^2 g_N=-4lambda_rep`.
Consequently `sigma_++(0)=8pi a^2=lambda_rep^2/(8pi m^2)`, agreeing with the
existing amplitude rather than assigning a separate capture coefficient.

This does not overwrite the previous positive-frequency NR square. With
`delta=M-2m`, that square used `c3=g_s/(2m sqrt(2M))` and
`k_c=lambda_tot/(4m^2)`, hence

\[
\lambda_{\rm RWA}=4m^2(k_c-c_3^2/\delta)
 =\lambda_{\rm rep}+\frac{g_s^2}{2M(M+2m)}.             \tag{6}
\]

The exact propagator decomposition identifies the missing analytic term:

\[
\frac1{4m^2-M^2}
 =\frac1{2M}\left[\frac1{2m-M}-\frac1{2m+M}\right].
\]

The second, negative-frequency term subtracts
`g_s^2/[2M(M+2m)]` from (6), giving (5). For
`lambda_min=g_s^2/Delta`, `M=2m sqrt(1+u_*^2)`,

\[
\frac{\lambda_{\rm RWA}-\lambda_{\rm rep}}{\lambda_{\min}}
 =\frac{M-2m}{2M}
 =\frac12\left(1-\frac1{\sqrt{1+u_*^2}}\right)
 =\frac{u_*^2}{4}+O(u_*^4).                            \tag{7}
\]

At fixed `lambda_min` it is a controlled `O(u_*^2)` correction; relative to
`lambda_rep=r_lambda lambda_min`, divide by `r_lambda`. The two coefficients
belong to two explicitly different approximations. Same-charge source-pole
energies, appreciable derivative corrections, and dense-medium scattering are
outside (5). In particular, require `|s-4m^2| << Delta` before using the
constant rather than the original amplitude.

## 4. A population exchange integral with no phenomenological alpha

Declare a static host potential `U(x)` and let
`h=-nabla^2/(2m)+U(x)`. This is a conditional host (ordinary gravity may
provide one); it is not derived by the flat-space action above. Choose an
orthonormal spectral basis consisting of a bound mode `u_b`, energy
`epsilon_b=-B<0`, and continuum modes `u_p`, energies `epsilon_p>=0`.
Let `a_b` annihilate a bound daughter. Expand

\[
\psi=u_b a_b+\int d\nu_p\,u_p a_p,\qquad
I_{br;pq}=\int d^3x\,u_b^*u_r^*u_pu_q.                \tag{8}
\]

The quartic in (5) contains the actual operator
`2g_N I_br;pq a_b^dagger a_r^dagger a_p a_q + h.c.` for distinct modes and
each unordered incoming pair `p<q`. Its four contractions and the `1/2`
in the Hamiltonian fix this coefficient. Golden rule, a continuum/long-time
limit, and factorization of incoherent occupations give

\[
\begin{split}
\dot N_b|_{\rm cap}=\mathcal C_b={}&
\frac12\int d\nu_p d\nu_q d\nu_r\,2\pi
 |2g_N I_{br;pq}|^2\delta(\epsilon_p+\epsilon_q-\epsilon_b-\epsilon_r)\\
&\times\left[(N_b+1)(1+f_r)f_pf_q
       -N_b f_r(1+f_p)(1+f_q)\right].                 \tag{9}
\end{split}
\]

The `1/2` counts ordered continuum pairs only once. The diagonal `p=q` has
measure zero in this continuum expression. Discrete coincident modes require
their ladder factors `n_p(n_p-1)` and separate normalization; the finite Fock
controls here deliberately cover distinct modes. The `N_b+1` term permits
spontaneous seed population; replacing it by `N_b` is the macroscopic
condensate approximation, not an exact empty-state equation.

Here the residual contact interaction is treated perturbatively. If its
mean-field shift is appreciable, `epsilon_i` and the modes must first be
matched consistently to that background; the unshifted host energies alone
are then insufficient. The diagnostic below uses the leading weak-coupling
energies.

This is `Phi+_free + Phi+_free <-> Phi+_bound + Phi+_free`.
It converts no source and creates no daughter. Its integrated moments are

\[
\dot N_b=\mathcal C_b,\quad
\dot N_f=-\mathcal C_b,\quad
\dot M_b^{\rm carrier}=m\mathcal C_b=-\dot M_f^{\rm carrier},\qquad
\epsilon_r=\epsilon_p+\epsilon_q+B.                   \tag{10}
\]

For every event, the bound dynamical-energy moment is `-B`, and the free
moment is `+B`: their sum vanishes. The outgoing excitation carries both
incoming kinetic energies and the released binding energy. If it escapes,
an additional spatial boundary flux removes one free particle and energy
`epsilon_r`; that flux is not another conversion. A finite-mass dynamical
host must also receive recoil momentum and recoil energy. A fixed host is
the static, infinite-inertia approximation; a time-dependent potential adds
the reciprocal host work `integral n dot U`. Selfconsistent mean-field
energy must be differentiated as an energy functional to avoid counting its
pair interaction twice.

For Bose occupations at common temperature, allow separate bound and free
chemical potentials `mu_b,mu_f`. Using `1+f=e^{beta(epsilon-mu)} f` on the
energy shell, the ratio of the gain product to the loss product in (9) is

\[
\frac{G}{L}=e^{\beta(\mu_f-\mu_b)}.                 \tag{11}
\]

Thus the microscopic current vanishes at diffusive equilibrium and points
towards it, when the rate has nonzero support. An assigned positive capture
constant independent of inverse evaporation would violate this relation.
Occupation correlations, a time-dependent basis or broad spectral modes need
additional terms and are not part of this factorized Golden-rule closure.

The exact negative-charge copy of (9) can populate an opposite-charge bound
mode. Equal plus/minus capture increases positive rest mass in bound modes
while keeping net charge zero. There are also mixed-charge capture channels:
the existing threshold crossed amplitude gives
`g_cross=(lambda_tot-g_s^2/M^2)/m^2`, with no identical-species factor, so a
neutral calculation cannot substitute the single-sign coefficient everywhere.
Other inelastic processes remain capable of changing total daughter abundance.

## 5. The local condensate source and its support test

For a weak dilute condensate field `phi_c=<psi>` and fluctuation `eta`, the
same Hamiltonian gives the exact unclosed condensate-density source

\[
\partial_t n_c+\nabla\cdot(n_c v_c)
 =2g_N\operatorname{Im}\left[(\phi_c^*)^2\langle\eta\eta\rangle
        +\phi_c^*\langle\eta^\dagger\eta\eta\rangle\right].    \tag{12}
\]

With the weak-collision, Hartree-Fock, slowly varying closure, it reduces to
the known `C12` condensate/thermal exchange source with opposite thermal
number moment. The checked primary comparison is in `LITERATURE_CHECK.md`.
For a resting homogeneous condensate its support obeys

\[
\epsilon_p=\frac{p^2}{2m}+U,\quad
\mu_c=U_{\rm ext}+g_Nn_c+2g_Nn_f,\quad
U=U_{\rm ext}+2g_N(n_c+n_f),\quad
\mathbf p_1=\mathbf p_2+\mathbf p_3,
\]

and hence

\[
\boxed{\ \mathbf p_2\cdot\mathbf p_3=m(U-\mu_c)=m g_N n_c\ }. \tag{13}
\]

This yields a discriminating support obstruction in this closure: if all
incoming thermal modes have `p^2/(2m)<=Emax` and
`Emax<g_N n_c/2`, the capture integral is zero. At equality there is only the
parallel endpoint, of zero measure for an ordinary distribution; strictly
positive measure requires a larger cutoff and occupied on-shell modes.
Back-to-back incoming pairs cannot feed the resting repulsive HF condensate.
A thermal distribution without a hard cutoff has tails, so this is not a
zero-temperature cooling theorem. The Hartree-Fock treatment is also not a
Bogoliubov low-temperature calculation.

Bound/free and condensate/thermal are different partitions: a halo can contain
many incoherent bound excited modes; a condensate can move and be unbound.
For a nonlocal bound-state projector, reciprocal total population signs in
(10) do not by themselves provide a pointwise local exchange density. Projection
cross currents must be kept or a justified local/Wigner approximation made.
Only after that bridge could one insert matched `+m C, -m C` sources into
local settled/free continuity equations. No such identification is assumed.

The original dilute repulsive contact theory without a host supplies no
localized bound ground state: a stationary isolated GP state would require
`mu<0`, but `mu N=T+g_N integral |psi|^4>=0`. This is a restricted dilute
contact obstruction. Gravity, an added host, a different phase, or different
interactions change the hypotheses.

## 6. One explicit nonzero bound/free matrix element

To test that (9) is more than an unspecified rate, use the exactly solvable
**auxiliary one-dimensional host**

\[
h=-\frac{\partial_x^2}{2m}-\frac{\kappa}{m}\delta(x),\qquad
u_b=\sqrt\kappa e^{-\kappa|x|},\quad B=\frac{\kappa^2}{2m},
\]

with its actual delta-normalized scattering eigenfunctions (`k>0`),

\[
u_{k,o}=\frac{\sin kx}{\sqrt\pi},\qquad
u_{k,e}=\frac{k\cos kx-\kappa\sin(k|x|)}
 {\sqrt\pi\sqrt{k^2+\kappa^2}}.                        \tag{14}
\]

The even state satisfies the derivative jump at the host; the odd state is
unaffected. This avoids using mutually inconsistent free waves and a host
bound wave. A separable transverse ground state would give a quasi-1D
coupling `g_1D=g_N integral d^2x_perp |u_perp|^4`; the benchmark below is
per `g_1D^2`, not a new phenomenological constant or a 3D halo prediction.

Take `m=1,kappa=2,p=3,q=6,r=7` with two odd incoming modes and one even
outgoing mode. Then `r^2=p^2+q^2+kappa^2` and

\[
\frac92+18=-2+\frac{49}{2}.
\]

For `C(a)=kappa/(kappa^2+a^2)`, `S(a)=a/(kappa^2+a^2)`, define
`a=(r+p-q,r-p+q,r+p+q,r-p-q)` and signs `(+, +, -, -)`.
The elementary exponential integrals give

\[
I_{b r;p q}=\frac{2\sqrt\kappa}{\pi^{3/2}\sqrt{r^2+\kappa^2}}
 \frac14\sum_j s_j[r C(a_j)-\kappa S(a_j)]
 =\frac{2\sqrt2}{\pi^{3/2}\sqrt{53}}\left(-\frac{63}{130}\right).
                                                               \tag{15}
\]

Thus `I=-0.03381266850843357` and
`|2g_1D I|^2/g_1D^2=0.004573186206644861` in the stated normalization.
The overlap is strictly nonzero by the exact rational coefficient in (15),
not merely by a numerical tolerance. The displayed momenta are dimensionless
fixture values, not a relativistically valid `p/m=7` application. For an
explicit NR scaling take `(kappa,p,q,r)/m=10^-5(2,3,6,7)` and `u_*=.02`:
the largest momentum is `7e-5 m` and its squared ratio to `m u_*` is
`1.225e-5`. Scaling (14) preserves the nonzero overlap and on-shell identity;
one may choose `g_1D=1e-8`, giving `m g_1D/kappa=5e-4`, with small occupation
shifts, for a weak-coupling diagnostic. No rate at these values was integrated.
This is an
existence witness for an added host's channel, not a host-production model.

## 7. Finite evidence and what it establishes

`run_002` completed with **128 controls**, including five rational propagator
matching cases, 81 distinct-mode Fock occupation controls, exact energy and
number moments, three exact common-fugacity detailed-balance controls, two
chemical-imbalance controls, six HF cutoff controls and direct overlap
quadrature on 24,000 and 48,000 Simpson panels over `[0,12]`.
The overlap error is below `2e-10`; the rigorous absolute omitted-tail bound
is `1.1852970342612802e-11`. Its two quadratures are
`-0.03381266850721943` and `-0.033812668507288056`.
For an independent discretization bound, expand the integrand into its four
frequencies, all at most 16. Its fourth derivative is bounded by
`0.07(7+2)(2^2+16^2)^2=42588`, since the prefactor is below `.07`.
The composite Simpson error at 24,000 panels is therefore at most
`(12/180)(12/24000)^4 42588 <1.775e-10`; adding the tail gives less than
`1.894e-10`. The finer-grid bound is smaller by 16 before adding the tail.
These are analytic truncation/discretization bounds; floating summation
roundoff is not interval-certified, and is supported by agreement with the
elementary exact expression.

The contraction controls check the stated finite distinct-mode coefficient
and ladder factors, not arbitrary quantum kinetic correlations. Universal
claims (1), (7), (10), (11), (13) and the nonzero (15) have analytic arguments
above; their truth is not inferred from a count of numerical controls.

The preserved `run_001` failed only because its tail-bound assertion had been
set too tightly at `6e-12`. Correcting it to `2e-11` did not change the
integrand, integration grid, physical model or reported overlap. Run 001 is
historical failure evidence, and its input hash is intentionally different.

Outcome: **implementation and finite assertion verified in the stated range**,
with floating quadrature explicitly bounded and exact rational nonzero
overlap independently known. Source status is conditional for the physical
halo application. No observational evidence, empirical species identification,
formation timescale, finite-host three-dimensional rate, microscopic CE082
density/W constraint, vacuum-energy transfer or gravitational-law selection
has been established. Next discrimination is a specified three-dimensional
selfconsistent host and incident distribution, retaining the outgoing energy,
inverse evaporation, charge channels and time-dependent host work in one
calculation. Research remains open.

Self-review: all equations and nearby prose in this file were proofread for
notation and delimiters; no external manuscript was edited. This was analytic
self-review plus finite computational controls, not independent proof audit.
