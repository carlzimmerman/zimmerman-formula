# Horizon normalization: independent checkpoint

**The derivation of kappa=1/2 was not obtained.** The exact saturation source
is CFG695, whose coefficient remains a fitted input. A normalization correction
and three discriminating calculations sharpen what a derivation must explain.
None is an impossibility theorem for all quantum field theory or horizon physics.

Checkpoint: **HORIZON-2026-10-20-01**. Base revision:
`431f22bd6fe998759b843d13113762d73356aec6`. Owner: horizon_normalization.
Write scope: this directory. The inherited checkout contains extensive
untracked work; relevant input bytes are pinned in the computation manifest.
Review: self-review, symbolic identities, and independent Fourier quadrature.
No proof-assistant or independent physics-referee certificate is claimed.

## 1. Target and the two different appearances of a0/2

Use mass-equivalent vacuum density and an asymptotically de Sitter background:

\[
H_\Lambda^2=8\pi G\rho_{\rm DE}/3,\quad
a_H=cH_\Lambda=c^2/R_{\rm dS},\quad
a_0=\kappa c\sqrt{G\rho_{\rm DE}}.
\]

At the target kappa=1/2,

\[
Z=\sqrt{32\pi/3}=5.7888100365,\qquad
a_0/a_H=1/Z=0.1727470747.
\]

**The saturation capacity a0 is 1/5.79 of the physical de Sitter surface
gravity, not 1/11.58.** The latter number occurs in two distinct statements:

1. In CFG695, half saturation occurs at **total** field `g=a0`, polarization
   acceleration `u=a0/2`, and **baryonic** field `gN=a0/2`. Thus the baryonic
   field at this defined transition point is `aH/(2Z)`.
2. In the older quadratic temperature-excess construction, the ambient
   parameter A satisfies `a0=2A`. The target therefore requires
   `A/aH=1/(2Z)=0.0863735374`. Ordinary de Sitter thermality has `A=aH`.

Neither is an independent switch-on mechanism. A smooth saturation law has no
sharp onset unless an operational fraction or observable is specified. The
target is a microscopic rule selecting a0 from independently specified vacuum
data, without inserting it into a gap, capacity, response map or energy offset.

## 2. Exact saturation source and the thermal-law mismatch

The source is `campaign_fresh_gravity/CFG695_saturating_vacuum/FROZEN_CRITERIA.md`
and `cfg695.py`, S1. Write `K=4 pi G`, `u=K|P|`:

\[
W_{\rm full}(u)=\frac{-a_0u-a_0^2\log(1-u/a_0)}K,
\qquad KW_{{\rm full},u}=\frac{u}{1-u/a_0}.
\]

The corrected expanded action uses `-W_full`; its completed-square form uses
`-W_rem`, where `W_rem=W_full-u²/(2K)`. Combining the completed square with
`W_full` double counts the critical quadratic. This correction already exists
in `sol61_push/cold_final_mile_2026_10_13/ACTION_CORRECTION.txt` and AG4.
In the radial static regime with negligible stiffness,

\[
g=KW_{{\rm full},u},\quad g_N=g-u,\qquad
u=\frac{a_0g}{a_0+g},\qquad g_N=\frac{g^2}{g+a_0}.
\]

The potential is postulated; CFG695 discloses its post-hoc origin. Its stability
and galaxy fits do not link it to a cosmological vacuum energy.

For the specified uniformly accelerated detector in the conformal de Sitter
vacuum, the established result is

\[
k_BT(a)=\frac{\hbar}{2\pi c}\sqrt{a^2+a_H^2}.
\]

An *additional* inertia hypothesis identifies the force per unit mass with
`2 pi c kB [T(a)-T(0)]/hbar`, giving

\[
g_N=\sqrt{g^2+A^2}-A,\quad a_0=2A,\qquad
g^2=g_N^2+a_0g_N.
\]

This force identification is not detector QFT. The primary source explicitly
leaves its mechanical meaning and circular-motion transfer open:
[Milgrom (1999), section IV](https://arxiv.org/html/astro-ph/9805346v2).
The temperature is checked against
[Deser–Levin, equation (8)](https://arxiv.org/html/gr-qc/9706018v1).

| At the same deep coefficient a0 | CFG695 simple-mu | Temperature-excess quadratic law |
|---|---|---|
| gN at g=a0 | a0/2 | (sqrt(5)-1)a0/2 |
| maximum u=g-gN | a0 | a0/2 |
| low-field gN | g²/a0 - g³/a0² + ... | g²/a0 - g⁴/a0³ + ... |

AG4 already separates these laws. Keeping the quadratic function while claiming
the CFG695 capacity changes the theory.

**Scoped analytic-readout obstruction.** If a scalar force magnitude is an
analytic function F(T) near nonzero T0 and acceleration enters only through
the above T(a), then F[T(a)] is analytic in a². It cannot contain CFG695's
nonzero a³ term, for any finite positive a0. In dimensionless variables
`q=g/aH`, `zeta=a0/aH`, `t=T/T0`, the exact required inverse readout is

\[
\frac{g_N}{a_H}=F_\zeta(t)=
\frac{t^2-1}{\sqrt{t^2-1}+\zeta}
=\frac{2(t-1)}\zeta-
\frac{2\sqrt2(t-1)^{3/2}}{\zeta^2}+O((t-1)^2).
\]

A temperature-only explanation therefore needs a nonanalytic readout,
additional variables or nonlocal response. Changing the temperature scale
alone cannot fix the full law. This does not forbid a microscopic phase
transition or acceleration dependence through more than temperature.

The RT17/RT19 dispute is **already resolved** by CFG904: `cH/(2pi)` is a free
frequency assignment, not a coefficient fixed by KMS. The factor 4pi between
it and `2cH` splits into a 2pi assignment and the factor 2 in the
temperature-excess series. We do not revive kappa=0.4607 as derived. Nor do we
use broad “pi parity” language as a theorem about arbitrary quantum theories;
the valid arithmetic restriction depends on a restricted class of operations
and constants.

## 3. Route QFT: actual detector response

For a weakly coupled point detector with positive angular-frequency gap omega,
a real massless conformally coupled scalar, conformal vacuum, and stationary
uniformly accelerated trajectory, set `alpha=sqrt(H²+a²/c²)`. Dividing out the
coupling and transition matrix element, its excitation rate is

\[
\dot{\mathcal F}(\omega,a)=
\frac{\omega}{2\pi}\frac1{e^{2\pi\omega/\alpha}-1}.
\]

The comoving formula is checked in
[Ali–Bhattacharya–Lochan, equation (15), vacuum parameter set to zero](https://arxiv.org/html/2003.11046v2).
The acceleration extension is independently checked through

\[
W^+(s)=-\frac{\alpha^2}{16\pi^2}
\operatorname{csch}^2[\alpha(s-i0)/2].
\]

Here alpha is an acceleration rate, not that paper's vacuum parameter. Shift
the Fourier contour to `s=t-i pi/alpha` inside its analytic strip. The integral
becomes a convergent sech² Fourier transform. Five quadratures at
`omega/alpha=0.05,0.2,0.5,1,2`, with 60-digit arithmetic, agree with the Planck
expression to relative error below 1e-35. This checks a rate, not a force.

Let `x0=E/(kB T0)=2 pi omega/H` and `q=a/aH`. Then

\[
\frac{\dot{\mathcal F}(a)}{\dot{\mathcal F}(0)}=
\frac{e^{x_0}-1}{e^{x_0/\sqrt{1+q^2}}-1}.
\]

| x0 | q where rate doubles | Rate ratio at q=1/(2Z) |
|---:|---:|---:|
| 0.1 | 1.675510 | 1.003913 |
| 1 | 1.265107 | 1.005892 |
| 10 | 0.393052 | 1.037793 |
| 100 | 0.118357 | 1.449104 |

At `q=1/(2Z)` the temperature rises by **0.372326%**; at `q=1/Z` it rises
by **1.481109%**. Putting rate doubling at the former requires
`x0=186.8597565`; the equilibrium two-level population at zero acceleration is
then about `7.04e-82`. This is a selected probe, not a universal activation
point. Relative doubling does not imply observable event counts: the absolute
rate still contains coupling and gap.

KMS fixes detailed balance, not gap, coupling, matrix element, relaxation time
or the response-to-force map. Its a is **proper acceleration**. A freely
falling star has zero four-acceleration while its Newtonian orbital coordinate
acceleration is nonzero. A medium or modified-inertia theory must specify
which worldline samples which correlator before substituting galaxy g.

**Disposition:** this regular stationary detector plus an unspecified threshold
does not select kappa. Nonlocal trajectory-dependent influence functionals,
interacting critical detectors and specified medium worldlines remain open.

## 4. Route information: finite Gibbs probes

Use a two-level probe equilibrated with the same bath:
`p(q)=1/[1+exp(x0/sqrt(1+q²))]`. Relative entropy against its q=0 state is

\[
D(q)=p(q)\log\frac{p(q)}{p(0)}+
[1-p(q)]\log\frac{1-p(q)}{1-p(0)}.
\]

The trace expression and Gibbs differentiation give

\[
D(q)=\frac{x_0^2p(0)[1-p(0)]}{8}q^4+O(q^6).
\]

Both forms are checked independently. At `x0=1`, `q=1/(2Z)`,
`D=1.3542380e-6` nats. For N independent probes relative entropy is exactly
`N D`, so even a one-nat threshold depends on gap and probe count. Nothing
singles out 1/(2Z).

This finite-probe check illustrates the spectral-dependence problem already
studied in `agentYY_modular_a0.md`; it is not a calculation of the full
quantum-gravity observer algebra. A horizon-information proposal still needs
an operationally selected algebra, state, observable and force coupling.

**Disposition:** finite thermal information thresholds do not select the
coefficient under these assumptions. A specified interacting horizon/medium
theory remains open.

## 5. Route material saturation: regular dipoles give the wrong power

Consider a finite-dimensional thermal system `H(g)=H0-g D` at finite
temperature with a symmetry sending `D -> -D`. The trace exponential is
analytic near g=0 and its partition function is even. Thus polarization is
odd analytic:

\[
u(g)=\chi g+b_3g^3+b_5g^5+\cdots.
\]

The isotropic vector version is `u_vec=g_vec f(|g|²)`. To get a deep modified
gravity limit through `gN=g-u`, susceptibility must be critically tuned to
chi=1. The leading residual is generically **g³**, not g². If that coefficient
vanishes, the next regular odd power still cannot supply g². CFG695 instead
requires the nonanalytic signed/vector response containing `g |g|`.

Two bounded saturators make the distinction explicit:

\[
u_{\rm Ising}=u_m\tanh(g/u_m),\quad
g_N=\frac{g^3}{3u_m^2}+O(g^5),
\]
\[
u_{\rm Langevin}=u_m\left[\coth(3g/u_m)-\frac{u_m}{3g}\right],\quad
g_N=\frac{3g^3}{5u_m^2}+O(g^5).
\]

Both have unit initial susceptibility and capacity um. Outside a point mass,
their leading law gives `g proportional to r^(-2/3)` and
`v proportional to r^(1/6)`, rather than flat circular speed. Thus ordinary
dielectric saturation does not derive the required cubic potential.
Infinite critical systems, gapless zero-temperature sectors and non-equilibrium
states evade these regular finite-system assumptions.

Capacity normalization is also free. Classical isotropic dipoles of moment d,
density n and coupling energy `-d dot g` have susceptibility
`K n d²/(3 kB T)`. Unit susceptibility gives `um=K n d=3 kB T/d`.
Identifying T with T0 would yield

\[
u_m/a_H=3\hbar/(2\pi c d).
\]

The free dipole moment remains. This hypothetical model does not establish
gravitational dipoles in nature. Taking d to be a multiple of hbar/c only
trades the coefficient for that multiple.

The nodal-ring candidate is a serious existing evasion: it computes a positive
nonanalytic cubic at zero temperature but retains free parameters and
thermal/occupancy rounding, as `NODAL_RING_ORIGIN.md` states. We do not close it.

**Disposition:** finite regular equilibrium dipoles cannot give the exact
asymptotic law. An interacting thermodynamic or gapless medium remains open;
its state, criticality, force coupling and normalization must all be derived.

## 6. Remaining gap and continuation

A derivation must supply from one independently specified model:

1. The physical response observable and worldline/source coupling.
2. Critical susceptibility and the required nonanalytic deep response,
   including the choice between simple-mu and the quadratic law.
3. A relation tying capacity or deep coefficient to the *gravitating* vacuum
   energy, selecting kappa and surviving the allowed counterterms.

The third condition is independent of the first two. A constant shift of the
local polarization potential leaves its response unchanged while changing
vacuum stress once gravity is included. The repository's zero-mode and
nonselection results already establish this in their respective action
classes. We do not present it as a new theorem or extend it to all nonlocal
theories.

The next useful attempt is a specified in-in effective action or microscopic
Hamiltonian whose correlators generate the force. Then vary its allowed vacuum
offset and response couplings. Equating temperatures or choosing a gap does
not clear the contract. For a critical model, first check the nonanalytic
response term; then audit its vacuum normalization. These continuations are
deferred and open, not exhausted by the present checkpoint.

## Reproduction and evidence

With Python >=3.9 and `requirements.txt` installed, from repository root:

```sh
python3 core_open_problems_2026_10_20/01_horizon/check_horizon.py /tmp/horizon-results.json
```

The script is self-contained. Source paths in `contract.json` are documentary
inputs, not imports. `sh .../reproduce.sh` is a portable wrapper accepting an
optional output path. Historical `run_002/` used the Mathbox bounded runner:
**completed, 43 checks, manifest validated**. Its input hashes include the
current script. The runner's machine-specific location is recorded in the
manifest but is unnecessary for numerical reproduction. Optional validation:

```sh
python3 "$MATHBOX_AUDIT_DIR/scripts/validate_manifest.py" core_open_problems_2026_10_20/01_horizon/run_002/manifest.json --root .
```

`run_001/` preserves a failed attempt: SymPy 1.14.0 incorrectly returned infinity
for a coth-based limit. Its exponential rewrite and independent series both
give 3/5. No physics criterion changed. That run's script hash is historical;
it is not fresh successful evidence. Numerical claims are confined to stated
points and tolerances, separate from the analytical regularity arguments.
