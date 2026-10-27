# Charged gauge bulk action in the far exterior

**Correction, 2026-10-19:** the unqualified common-four-dimensional electric
matching and total Coulomb-tail interpretation below are superseded by
[ADDENDUM_2026-10-19_COMMON_PV.md](ADDENDUM_2026-10-19_COMMON_PV.md).
The common-PV all-IBP action has `K_E-K_B=L/(24pi^2)`; the source's finite
electric convention remains unresolved. Static and magnetic results remain
valid. Frozen raw derivations and run artifacts are unchanged.

**A controlled local bulk coefficient has been obtained, including all circle
frequencies and their common coupling subtraction.** It is an effective-action
contribution on a specified background. It is not the complete finite-wall
Gaussian, angular-mode sum, vacuum stress, or an electromagnetic-alpha result.

The conventions are the microscopic SU(2) trace normalization
`tr(Ta Tb)=delta_ab/2`, fixed circle circumference L, background Feynman gauge,
and `Gamma_1=1/2 Tr_vec,adj log H-Tr_adj log M`. The exterior is
`A4=h T3`, `h=v-1/r>0`, `B=n_mag r_hat/r^2`, with `r_c m_min>>1`.
Logweight means `-Gamma_1`. One circle frequency contributes a 3D integral,
without a further factor L. The contract and independent raw derivations were
saved before the corresponding project/source comparisons.

## 1. Static charged pair: orbital, ghost and spin counts

For a single charged frequency let `m=|2pi k/L+h|` and
`K=-(partial_i-i A_i)^2+m^2`. The two real charged adjoint colors have equal
spectral traces after charge/frequency conjugation. The factor 1/2 in the
vector action leaves one complex-vector trace, while the complex adjoint
ghost leaves minus two scalar traces. Consequently

`Gamma_k = Tr_4 log(K delta+V)-2 Tr log K`, `V=2i F`,

so the net orbital term is `2 Tr log K`. The Lorentz trace is
`tr V^2=8(E^2+B^2)`.
For nonzero k the conjugate pair is `(q,k)=(+1,k),(-1,-k)`;
pairing opposite charges at the same k would give unequal masses and the
wrong intermediate count. The final integer sum contains every such pair
once.

For one scalar trace, the momentum bubble is

`I(p)=atan(|p|/(2m))/(4pi|p|)`
`    =1/(8pi m)-p^2/(96pi m^3)+O(p^4)`.

The quadratic variation in `U=m^2` is `-I(p) deltaU(p)deltaU(-p)/2`.
Its derivative term is `+(partial U)^2/(192pi m^3)`, equivalently
`+E^2/(48pi m)` in an integrated-by-parts bulk density. Independently,
the constant-magnetic scalar heat kernel has multiplier `Bs/sinh(Bs)`;
its quadratic term gives `+B^2/(48pi m)`. An additional constant-electric
oscillator heat-kernel calculation reproduces the electric coefficient
without the bubble. The combined coefficients are therefore

| Contribution to Gamma_k density | E^2 coefficient | B^2 coefficient |
|---|---:|---:|
| Orbital vector minus ghosts | `+1/(24pi m)` | `+1/(24pi m)` |
| Vector spin, `-tr(V^2) I(0)/2` | `-1/(2pi m)` | `-1/(2pi m)` |
| Total | `-11/(24pi m)` | `-11/(24pi m)` |

For the static charged pair, `m=h`, the actual shell integral of this bulk
density is

`Gamma_static,2 = -11(1+n_mag^2)/6 log[h(R)/h(r_c)]`.

Its 1/R coefficient is `+11(1+n_mag^2)/(6v)` in Gamma, hence
`-11(1+n_mag^2)/(6v)` in logweight. In 3D dimensional regularization the
static zero-derivative density is `-h^3/(3pi)`; its exact Coulomb-shell
integral has no 1/R term.

## 2. Full charged circle tower and UV matching

Put `x=Lh/(2pi)` in the chamber `0<x<1`. Charge conjugation sends the
negative-charge tower to the positive-charge tower by `k -> -k`; it does not
introduce another multiplicity. For a symmetric cutoff `-N<=k<=N`,

`sum_k 1/m_k = L/(2pi) [psi(N+1+x)+psi(N+1-x)-psi(x)-psi(1-x)]`.

Subtract `L H_N/pi` and define

`F(x)=-psi(x)-psi(1-x)-2 gamma_E`
`    =1/x+sum_(k>=1)[1/(k+x)+1/(k-x)-2/k]`.

Thus `F(1/2)=4 log 2`, and the harmonic-subtracted loop density is

`Gamma_1,2 density = -11 L F(x)/(48pi^2) (E^2+B^2)`.

The divergence has the sign and normalization of the pure SU(2) one-loop
strong-coupling beta function. Define the harmonic-scheme coupling by

`1/g_H^2(mu)=1/g_b^2-11/(12pi^2)[H_N-log(mu L/(2pi))]`.

The finite classical-plus-loop coefficient in Gamma is

`C(h;mu)=L/(2g_H^2(mu))-11L/(24pi^2)log(mu L/(2pi))`
`         -11L/(48pi^2)F(x)`.

It satisfies scale independence to this order because
`d(1/g_H^2)/dlog mu=11/(12pi^2)`, equivalently
`beta(g_H)=-11 g_H^3/(24pi^2)+O(g_H^5)`.
This is a definition of a finite subtraction scheme, not a numerical
identification of the strong coupling.
As an independent ultraviolet check, the four-dimensional constant-B
charged vector-minus-ghost heat-kernel multiplier is
`(Bs/sinh(Bs))*2 cosh(2Bs)=2+(11/3)B^2s^2+...`.
Its proper-time logarithm gives precisely the same coupling divergence.

The exact-version primary comparison is Diakonov--Oswald,
[hep-ph/0303129v2](https://arxiv.org/abs/hep-ph/0303129v2), equations
(67), (69), (72), (73), (91), (92). Their action is logweight, so its
sign is opposite to Gamma. Their parallel electric and magnetic coefficients
coincide and give exactly the same digamma function and UV coefficient.
Matching their Pauli--Villars convention yields

`1/g_H^2(mu)=1/g_PV^2(mu)+11/(12pi^2)(log 2-gamma_E)`.

Equivalently the natural harmonic scale `2pi/L` uses
`g_H(2pi/L)=g_PV(4pi exp(-gamma_E)/L)` to one-loop accuracy. No
unverified conversion to a measured QCD or electromagnetic coupling is made.

## 3. The potential also contributes a 1/R term

Summing the zero-derivative scalar determinants with the full periodic tower,
or equivalently using the Bernoulli-polynomial continuation, gives

`V3(h)-V3(0)=4pi^2/(3L^3) x^2(1-x)^2`
`           =h^2/(3L)-h^3/(3pi)+Lh^4/(12pi^2)`.

This agrees with the same primary source, equations (48)--(49). The exact
quartic on `h=v-1/r` gives a Gamma 1/R coefficient `-L/(3pi)`.
Removing only the constant vacuum reference leaves the separate R^2, R,
and log R contributions; extracting the inverse term does not remove those
divergences or define a finite full determinant.

For a smooth derivative coefficient c(h),

`4pi(1+n_mag^2) integral_(r_c)^R dr c(v-1/r)/r^2`

has 1/R coefficient `-4pi(1+n_mag^2)c(v)`. Consequently, at
`mu=2pi/L`, the local one-loop bulk logweight coefficient is

`a_bulk,loop = L/(3pi)-11L(1+n_mag^2)F(Lv/(2pi))/(12pi)`.

Including the classical bulk action adds
`2pi L(1+n_mag^2)/g_H^2(2pi/L)`. At center holonomy and unit magnetic
tail, `v=pi/L`, `n_mag=1`, the combined coefficient is

`a_bulk,class+loop = 4pi L/g_H^2(2pi/L)`
`                    + L(1-22 log 2)/(3pi)`.

The loop term is negative, approximately `-1.5118911057 L`; this number
is merely evaluation of exact constants, not a fit. A center-stabilizing
deformation changes the local potential and has to be included separately.

## 4. Surface convention and the actual large-R saddle

All displayed coefficients use the explicitly specified bulk density with
scalar-potential gradients integrated by parts. A surface contribution can
carry the same inverse power. In the exact harmonic Coulomb exterior,

`(partial h)^2/h = div(log h grad h)`, since `Delta h=0`.

Thus even the whole displayed electric bulk term can be moved into a local
surface functional. The finite-wall determinant must include its matching
surface/domain contribution before any total coefficient is invariant under
such rearrangements. The local bulk number above cannot be identified with
the complete finite-wall Gaussian coefficient.

The primary source retains an additional equation-of-motion term, equation
(82). For a Cartan field of positive h it reduces in logweight conventions to
`(1/(12pi)) integral (Lh/pi-1) Delta h`, which is identically zero on the
declared exterior profile. Its later printed integration-by-parts formula
(83) has an inconsistent sign; SOURCE_AUDIT.md gives the direct check. We
use (82), not (83), and do not discard a nonzero surface functional.

The Coulomb holonomy profile is also not the stationary large-R configuration
of a theory with a positive holonomy-scalar mass at fixed g and L. On the
actual screened profile, `h-v` and E decay exponentially. The magnetic bulk
coefficient remains useful. Writing

`Gamma_mag = (kappa_B^eff/2) integral B^2`,

gives

`kappa_B^eff=L/g_H^2(mu)-11L/(12pi^2)log(mu L/(2pi))`
`              -11L F(Lv/(2pi))/(24pi^2)`.

Equivalently `delta kappa_B=-11/(12pi) sum_k^ren 1/m_k`.
For a unit magnetic exterior the conditional bulk logweight tail is then
`+2pi kappa_B^eff/R`. The microscopic flux normalization `div B=4pi rho`
implies dual stiffness `kappa_d^eff=1/(16pi^2 kappa_B^eff)`, consistent with
the corrected normalization bridge. This is a bulk matching relation; a
charged exterior is not an exactly neutral compact vacuum ensemble.

## 5. Relation to the angular calculation and evidence

The full J1 relative-domain logweight coefficient `+3/(vR)` in
`angular_modes/transverse_followup/REPORT.md` uses the unbroken `h=0`
reference and includes that partial wave's wall algebra. This calculation
uses a local same-chamber far-exterior subtraction and all charged circle
frequencies. The two numbers are neither additive without a matching
calculation nor contradictory. A local bulk derivative expansion determines
the bulk part of the high-angular/frequency sum but leaves the relative
boundary kernel, reference conversion, core and nonlocal neutral/core data.

`runs/bulk-002` has `run.status=completed` and a validated v2 manifest.
It checks the exact Lorentz trace and series, nine Feynman-parameter bubble
integrals, three spin/magnetic heat-integral pairs, twelve finite KK sums
with analytic remainder bounds, the static radial primitive and the GPY
quartic tail. Numerical work uses 60 decimal digits; its declared finite
tests are not a global proof certificate. The uniform tail bound is

`0<F(x)-F_N(x)<=x^2/[N^2(1-x^2/(N+1)^2)]`, for `0<x<1`.

`runs/bulk-001` is retained with `launch-failed`: the macOS child preexec
failed under the requested address-space cap. No mathematical assertion ran
there. The successful run omitted that cap and retained the wall-clock,
CPU-time, output and thread bounds. REPRODUCE.md records the exact command.

Outcome: the static and full-KK local charged bulk coefficient and its
one-loop coupling match are derived and checked in the stated domain.
The full angular/boundary determinant, physical same-vacuum subtraction,
deformation matching, stress/metric response and electromagnetic bridge
remain uncomputed. No measured alpha or cosmic vacuum input was used.

Self-proofreading covered this report and SOURCE_AUDIT.md: normalization,
sign of logweight, frequency counts, units and inverse-radius notation were
checked. No mathematical-token proofreading correction was made to frozen
inputs or runs.

