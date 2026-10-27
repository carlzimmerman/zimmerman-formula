# Microscopic gravitational pairs: exact spectrum, source weights and mass source

19 October 2026. Parent `CE-SHARED-STATE-2026-10-19 / CE-FM092`.
Scope: one resting charge-two source and its identical positive-mass daughter
pair, with the previously omitted attractive Newtonian relative potential.
All writes are confined to this lane. This is a dilute two-body calculation,
not a calculation of a many-body ground state or its formation.

**Result.** The infinite-space Coulomb Hamiltonian has an actual Rydberg
accumulation and changes the source-to-continuum threshold from a square root
to a constant. These features must be retained when discussing soft spectra.
For the declared bare-source preparation, the leading total bound spectral
weight is only `5.3031543e-134` per source at the original benchmark. A local
source creates S waves, not the full hydrogenic degeneracy. More decisively,
the complete COM-centered odd mass source of two equal positive daughter
masses vanishes as an operator. Neither the binding energies nor adjacent
level spacings supply the requested reduced-gap dipole measure. Even tidal
response remains possible and is a different physical channel.

## 1. The pair Hamiltonian and its exact spectral data

Use `hbar=c=1`, `alpha=alpha_G=G m^2`, relative coordinate `r=x1-x2`, COM
`R=(x1+x2)/2`, and excess energy above `2m`. The reduced mass is `mu=m/2`:

\[
 H_C={p^2\over m}-{\alpha\over r},\quad
 a_B={2\over m\alpha},\quad B={m\alpha^2\over4}={1\over ma_B^2},\qquad
 E_n=-{B\over n^2}.
\]

These energies are exact for this pair Hamiltonian; they are not the poles
of the full coupled source/contact Hamiltonian before its dressing shifts.
The regular decaying radial solution terminates its confluent-hypergeometric
series precisely when `1/(kappa a_B)=n`; with `E=-kappa^2/m` this gives the
displayed spectrum. For the normalized S wave,

\[
 R_{n0}(r)={2\over n^{5/2}a_B^{3/2}}
 e^{-r/(na_B)}L_{n-1}^{1}(2r/(na_B)),\qquad
 |\psi_{n00}(0)|^2={1\over\pi a_B^3n^3}.
\]

The origin value follows from `L_{n-1}^1(0)=n` and `Y00=1/sqrt(4pi)`.
All `l>0` wavefunctions vanish at the origin. Exchange symmetry allows only
even `l` for the identical spin-zero daughters; a local rotationally scalar
source couples only `l=0`. Counting an `n^2` degeneracy as locally produced
would therefore be an error. This hydrogenic radial construction is also
identified in [NIST DLMF 33.22(v)](https://dlmf.nist.gov/33.22#v).

## 2. Deriving the identical-pair source normalization

The existing canonical source convention is

\[
 c_3={g\over2m\sqrt{2M}},\quad \gamma=2c_3,\quad
 F_{\{p,-p\}}={1\over\sqrt V},\quad
 v_p={2c_3\over\sqrt V}
 \quad\hbox{(leading NR normalization).}
\]

Write a normalized symmetric relative wavefunction with full-box momentum
coefficients `psi_p=psi_-p`. In the unordered-pair basis its coefficient is
`sqrt(2) psi_p`. Consequently, up to the zero-mode normalization whose
continuum weight vanishes,

\[
 \langle F|nS\rangle={1\over\sqrt V}
 \sum_{\{p,-p\}}\sqrt2\,\psi_p
 ={\psi_{nS}(0)\over\sqrt2}.
\]

It follows that the bound part of the *coupling measure* is

\[
 \boxed{v_n=\sqrt2c_3\psi_{nS}(0)},\qquad
 \boxed{w_n^{(J)}=|v_n|^2={w_1\over n^3},\quad
 w_1={g^2m\alpha^3\over32\pi M}}.
\]

Here `w_n^(J)` has energy squared units; it is not a probability or an
occupied dipole magnitude. Equivalently `L_C=<F|(z-H_C)^-1|F>` has bound
residue `|psi_n(0)|^2/2`, and `Sigma_C=gamma^2 L_C`.

## 3. Coulomb continuum and its threshold

For positive excess energy `epsilon=k^2/m`, define
`v_rel=2k/m`, `eta=alpha/v_rel=m alpha/(2k)>0`. A unit-incident-wave
attractive Coulomb solution has origin normalization

\[
 |\psi_{\bf k}^{(+)}(0)|^2
 =e^{\pi\eta}|\Gamma(1-i\eta)|^2
 ={2\pi\eta\over1-e^{-2\pi\eta}}\equiv S(\eta).
\]

The gamma identity follows from reflection and recurrence. This precise
velocity convention agrees with Cassel, [arXiv:0903.5307v1](https://arxiv.org/html/0903.5307v1),
Eqs. (22), (29), (44)-(45): his common mass is our `m`, his speed `beta=k/m`,
and his `x=alpha/beta=2eta`. DLMF's conventional Coulomb parameter is `-eta`
for attraction; its [33.2.6](https://dlmf.nist.gov/33.2#E6) gives the same
origin factor with that sign. No Yukawa approximation is used here.

Multiplying the already normalized local source phase space gives

\[
 A={g^2\over16\pi^2M\sqrt m},\qquad
 \boxed{J_C(\epsilon)=A\sqrt\epsilon\,
 {\pi\alpha\sqrt{m/\epsilon}\over
 1-e^{-\pi\alpha\sqrt{m/\epsilon}}}}.
\]

Thus

\[
 \boxed{J_C(0+)={g^2\alpha\over16\pi M}\equiv J_*},\qquad
 w_1=2BJ_*.
\]

This is an enhancement of the source spectral density, not an additional
independent collision or decay channel. For `epsilon >> B` the flat-space
square root is recovered. The constant threshold concerns `epsilon << B`,
an extraordinarily small band for microscopic gravity at this benchmark.

The complete regulated self-energy contains both parts:

\[
 \Sigma_C(z)=\sum_{n\ge1}{w_1/n^3\over z+B/n^2}
       +\int_0^\infty{J_C(x)f_\Lambda(x)^2\over z-x}\,dx,
\]

with compatible source smearing/contact matching at short distances.
The pure-Coulomb bound values presume a source pointlike relative to `a_B`;
its UV self-energy still requires a regulator/subtraction. One must not
keep only the continuum's constant-density threshold logarithm. In fact,

\[
 {w_1\over B}\sum_{n\ge1}{1\over n(1+tn^2)}
 ={w_1\over B}\left[\Re\psi(1+i/\sqrt t)+\gamma_E\right],
 \qquad t=z/B>0.
\]

As `z->0+` this is `J_* log(B/z)+constant+O(z/B)`. The positive continuum
contributes `J_* log(z/Lambda)+constant`, canceling that infrared logarithm.
This is also the direct coarse-graining identity
`w_n^(J)/(dE_n/dn)=w_1/(2B)=J_*`. A finite renormalized real threshold
self-energy and a constant imaginary part are therefore consistent.

## 4. Actual source preparation and bound spectral weights

At a fixed regulator the source resolvent is

\[
 G_s(z)=[z-\delta_b-\Sigma_C(z)]^{-1},\qquad
 \rho_s(\epsilon)={J_C(\epsilon)\over
 [\epsilon-\delta_b-\Re\Sigma_C]^2+\pi^2J_C(\epsilon)^2}.
\]

The actual spectral measure of the normalized initial bare vector `|s>` is
`sum_j Z_j delta_(z_j)+rho_s(epsilon)d epsilon`, with full negative-energy
poles `z_j` and

\[
 Z_j=[1-\Sigma_C'(z_j)]^{-1}.
\]

This formula uses the full self-energy derivative, not a separate damping
constant. Near an isolated pair pole let
`D_n=E_n-delta_b-Sigma_bg(E_n)` be the source denominator with that pole
removed. Weak dressing gives

\[
 z_n=E_n+{w_n^{(J)}\over D_n}+\cdots,\qquad
 \boxed{P_n=|\langle\Psi_n|s\rangle|^2
       ={w_n^{(J)}\over D_n^2}+\cdots}.
\]

At weak short-distance dressing and physical detuning
`delta approximately M-2m approximately 400 eV`, `D_n approximately
-(delta+B/n^2)`. Therefore the leading pure-Coulomb estimate is

\[
 P_n\simeq {w_1\over n^3(\delta+B/n^2)^2},\qquad
 {w_1\zeta(3)\over(\delta+B)^2}
 \le P_{\rm bound}^{\rm leading}\le
 {w_1\zeta(3)\over\delta^2}.
\]

The interval is an exact bound on this displayed leading expression, not
an error bar for omitted source/contact matching. Source-mediated shifts
are tiny compared with Coulomb spacings for this benchmark. The continuum
occupation density tends to `J_*/(nu^2+pi^2 J_*^2)` for finite threshold
detuning `nu=delta_b+Re Sigma_C(0+)`. It is generically constant, not linear.

These probabilities are bound *spectral projections* of the declared
bare-source vector. The asymptotic bound projection is a coherent persistent
source/pair cloud; it is not an inventory of independently formed atoms.
The continuum outgoing probability is the absolutely continuous part.
If a preparation is `F(H)|s>` instead, every displayed spectral weight is
multiplied by `|F(E)|^2` and the complete measure is renormalized. An on-shell
incoming energy at `M` cannot turn into an isolated lower-mass bound pair
without another carrier of its excess energy. Gravitational radiation or
collisions could do that, but their rates and initial states were not
computed. Multiplying by a prescribed number of initial sources predicts
counts conditional on that number, not the number itself.

## 5. The soft-spectrum distinction and the exact mass-source obstruction

There are three different energy quantities:

\[
 b_n=B/n^2\quad\hbox{(ionization binding)},\qquad
 \Omega_{n,n+1}=B[n^{-2}-(n+1)^{-2}]\sim2B/n^3,
 \qquad \Delta=\Omega/(2d).
\]

The infinite series of excited levels has genuinely arbitrarily small
adjacent spacings. This is a possible soft excited-state ensemble beyond
an isolated finite-gap ground-state argument. The individual Coulomb
ground state nevertheless has a gap `E2-E1=3B/4`; Rydberg accumulation at
the ionization threshold does not close its ground-state gap. In pure
Coulomb theory there are also same-n angular degeneracies; local source
production does not populate all of them. Lifting such degeneracies and
computing their physical response require the specified perturbations.

Even as an energy measure, the actual `P_n~n^-3` behaves differently from
mode counting: the coarse-grained density in `b_n` tends to a constant.
If one merely relabels each occupied `n` by its adjacent spacing, that
conditional density is proportional to `Omega^-1/3`. Neither relabeling
is the target dipole weight. A thermal bound-only partition sum is not
automatically defined: even the S-wave sum `sum_n exp(beta B/n^2)` diverges
without a volume/ionization cutoff.

The decisive common gravitational source must include *both* daughters.
For their COM fixed at the origin,

\[
 D_{\rm odd}(k)={m\over k}
 [\sin(kr_z/2)+\sin(-kr_z/2)]\equiv0.
\]

This is an operator identity, so all its diagonal and transition matrix
elements vanish in the pair Hilbert space, including the bound states and
continuum. The uniform mass dipole `m x1+m x2=2mR` is purely COM. Replacing
the full source by one daughter's dipole would erase the exact cancellation.
For this physical odd probe `d=0`, and `Delta=Omega/(2d)` is undefined as a
finite reduced-gap variable. The sought occupied dipole measure is zero
in this channel despite the available Rydberg energies.

Even sources can carry internal structure:

\[
 \rho_{\bf k}=m e^{i{\bf k}\cdot r/2}
             +m e^{-i{\bf k}\cdot r/2}
 =2m\cos({\bf k}\cdot r/2)
 =2m-{m\over4}({\bf k}\cdot r)^2+O(k^4r^4).
\]

A tidal potential `Phi_ext(x)=T_ij x_i x_j/2` therefore produces
`V_internal=m T_ij r_i r_j/4`. The tensor `m r_i r_j/4` is the physical
tidal operator, rather than a gravitational acceleration dipole. A traceless
tidal field couples an S wave to `l=2`. As an exact finite-wavelength
benchmark, the 1S expectation is
`<rho_k>=2m/[1+(k a_B/4)^2]^2`. Its connected transition amplitudes, occupations,
ionization threshold and nonlinear response would need a separate tidal
calculation. They cannot normalize an odd acceleration response that is zero.

## 6. Matched repulsive contact: what can and cannot be inferred

The matched low-energy contact is `g2=lambda_rep/(2m^2)=4pi a_s/m`, hence

\[
 a_s={\lambda_{\rm rep}\over8\pi m},\qquad
 \delta E_{nS}=g_2|\psi_{nS}(0)|^2+\cdots,\qquad
 {\delta E_{nS}\over B/n^2}={4a_s\over a_B n}+\cdots.
\]

This is first-order short-range matching, valid for small range relative
to `a_B`, `a_s/a_B << 1`, no extra short-distance resonance, and a local
operator matched in the same convention. It is not the definition of a
naive unregulated three-dimensional delta-function Hamiltonian. Local
wavefunction-at-origin corrections are not bounded solely by `a_s/a_B`:
they also depend on the regulator, short-distance potential and source
Wilson coefficient. Tiny level shifts alone do not prove tiny relative
renormalization of a bare local production operator.

With a declared finite common form factor, the original explicit-source
rank-one representation remains valid with the free resolvent replaced by
the Coulomb one:

\[
 H_{\rm pair}=H_C+U|F_\Lambda\rangle\langle F_\Lambda|,
 \quad \Sigma(z)=\gamma^2{L_C(z)\over1-U L_C(z)},
 \quad J(\epsilon)=\gamma^2{j_C(\epsilon)\over
 |1-U L_C(\epsilon+i0)|^2}.
\]

Here `U=4 k_c`, `k_c=lambda_tot/(4m^2)`, `gamma=2c3` belong to the retained
original NR source/contact block. The Coulomb poles move under the repulsive
rank-one perturbation. Keeping this explicit source and simultaneously using
`lambda_rep` as its already source-eliminated contact would double count the
matching subtraction. The small `a_s` estimate instead describes the
low-energy pair Hamiltonian after proper matching. These alternative
representations must not be mixed. The negative Coulomb tail survives
short-range repulsion and supports high-n bound states in infinite space;
this does not revive the exact odd mass source.

## 7. Physical benchmark and controlled size/time restrictions

The declared SI input is `G=6.67430e-11 m^3 kg^-1 s^-2`, consistent with
[NIST's 2022 CODATA table](https://physics.nist.gov/cuu/Constants/Table/allascii.txt).
Planck's constant, the electronvolt and `c` use their SI exact definitions.
Consequently the displayed `G` dependence is an input, not a normalization
derived from the scalar theory. For `m=1 MeV, u*=.02, g/m=.002168,
lambda_rep=.00587528`, the verified leading values are:

| Quantity | Value |
|---|---:|
| `alpha_G` | `6.7088307462e-45` |
| `a_B` | `5.8826042249e31 m` |
| `B` | `1.1252102495e-83 eV` |
| `J_*` | `3.1360190964e-46 eV` |
| `w_1` | `7.0573616600e-129 eV^2` |
| Leading `P_bound` per bare source | `5.3031543042e-134` |
| Leading `P_1` | `4.4117331636e-134` |
| `S(delta)-1` in the NR benchmark | `5.2693667689e-43` |
| `a_s/a_B` | `7.8416155938e-49` |
| Leading relative ground contact shift | `3.1366462375e-48` |
| `hbar/B` | `5.8496797129e67 s` |

No ordinary object-size cutoff is automatically present in the infinite-space
two-body Hamiltonian. It must be stated as a physical localization or
environment condition. An `nS` pair has
`<r^2>=a_B^2 n^2(5n^2+1)/2`. Requiring its rms separation below a declared
`R` therefore cuts off `n` at order `sqrt(R/a_B)`; already the ground rms
radius is `sqrt(3) a_B`. For the exact 1S state,

\[
 \Pr(r<R)=1-e^{-2R/a_B}[1+2R/a_B+2(R/a_B)^2]
 \sim{4\over3}(R/a_B)^3.
\]

At `R=1e22 m` this probability is `6.5498272e-30`; at `R=1e26 m` it is
`6.5498105e-18`. These are localization diagnostics for the isolated state,
not probabilities of making an atom inside those bodies.

There is also a rigorous confined control. Impose a Dirichlet boundary on
the relative coordinate at `r=R`. For every radial component `u(0)=u(R)=0`,
Cauchy-Schwarz gives `int |u|^2/r <= R int |u'|^2`. Thus, including the
nonnegative angular kinetic term,

\[
 E\ge(1/m-\alpha R)\int|u'|^2
 \ge(1/m-\alpha R){\pi^2\over R^2}\int|u|^2>0
 \quad\hbox{if}\quad R<a_B/2.
\]

A nonnegative regulated repulsion preserves this bound. All the listed
`R=1,1e22,1e26,c*1e18 m` controls satisfy it. The result applies to this
explicit confinement and does not assert that a finite physical body
deletes the unrestricted free-space gravitational tail.

For the declared illustrative observation time `T=1e18 s`, the resolution
`hbar/T=6.5821195695e-34 eV` exceeds `B` by about `5.85e49`. Resolving a
binding `B/n^2` requires `n <= sqrt(BT/hbar)=1.3075e-25`, so no integer
`n>=1` qualifies. The large-n adjacent-spacing diagnostic similarly gives
`n <= (2BT/hbar)^(1/3)=3.2456e-17`; its asymptotic expression is not valid
as a quantitative `n<1` spectrum, but the exact first adjacent spacing is
already unresolved. The causal radius `cT=2.99792458e26 m` is much smaller
than `a_B`. Finite time limits spectroscopic resolution and formation
claims; it does not remove mathematical eigenstates or calculate a rate.

## 8. Verification and remaining scope

`gravitational_checks.py` independently integrates normalized hydrogenic
radial functions for `n=1,2,3,7`, compares gamma/closed Sommerfeld factors
at four specified `eta`, checks four threshold ratios and the exact
`w1=2B J_*` identity, checks the bound digamma sum at three energies,
brackets the remaining zeta tail after `n=10000`, and integrates the even
1S form factor at three finite wavelengths. Algebra and source cancellation
are proved above; the finite checks do not prove the infinite claims.

The first bounded run failed a deliberately stringent relative-accuracy
check on an integral of order `1e-96`: integrating directly over the tiny
interval lost relative accuracy under absolute quadrature stopping. That
record is preserved in `run_001`. Rescaling the interval to `[0,1]` fixes
the numerical conditioning. `run_002` completed within the same caps and
its v2 manifest validates against its present pinned inputs. Its runtime
is recorded in the manifest; no memory or affinity hard cap was used.

Finite assertion outcome: **implementation and finite assertion verified
in the stated range**, using mpmath rather than certified intervals.
External authentication/notation checks are in `SOURCE_CHECKS.md`.
`ARTIFACTS.json` pins the source bytes and this lane's durable outputs.

No formation, cosmic abundance, local independently saturating dipoles,
target reduced-gap weight, universal `a0`, or universal gravity normalization
has been derived. The Coulomb/Rydberg loophole is real as spectral structure,
but the declared actual source state and complete physical mass source do
not satisfy the requested medium dictionary. Collective many-body phases,
environmental production and even tidal response remain outside this lane.
