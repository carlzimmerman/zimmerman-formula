# PN28-GRAD: finite scalar gradients admit conditional static halos

Owner `/root/empirical_audit`, 2026-10-28. Requested base
`66c45c5082f651dd54e171f98c11acd9cb3d9086`; live design HEAD
`7954d48377463cafcae3e8dbb09454134aef384f`. Only this directory was written.

**Result.** The independently varied equations have six regular numerical
solutions with finite matter radius and a decaying exterior scalar. Independent
mass and scalar integrals, the full anisotropic stress balance, the virial
identity, and two longer-domain/tighter-tolerance repetitions pass. Finite
scalar gradients therefore do not destroy the tested static halo branch.
They change its central density substantially in the concentrated cases.
This is a conditional static construction, not formation, a stability theorem,
an all-parameter existence theorem, or a selection of the pressure/vacuum ratio.

## 1. Inputs and the precisely restricted static problem

The actual execution inputs and SHA256 values, recorded identically before
and after the run, are:

| Input | SHA256 |
|---|---|
| `../dispersion_coupling/EOS.md` | `05f919345cb73c8b96e3f07d5fdb421ae8ee1d24a01e177abc9551aab4092274` |
| `../dispersion_coupling/REPORT.md` | `6deea173491b9c8e4d88b528ac0895faf2c6ec99273aa86c9d6e73d7c7d8537d` |
| `../halo/DERIVATION.md` | `aa79f50d4b78ce204a805f4962e53b87778ed7a17d8ec5e30a7be3bea529991a` |

The earlier design-time snapshot of REPORT.md had SHA256
`c4046a7d35128321f5d3a7c0fdef0f92b50ab68c2a27a5cb23d82506ef9391ae`.
It changed before execution began at `2026-10-28T17:59:16.717227+00:00`;
the runner's before/after hashes both equal the current `6deea173...` revision.
The first version of this table incorrectly labeled the design-time hash as
the actual execution input. `INPUT_PROVENANCE.json` now preserves the design
snapshot separately from the authoritative execution and current hashes.
No computational source, contract, run output, or manifest was changed to
make that documentary correction, and no numerical rerun was required.

The exact source delta is preserved in `SOURCE_REVISION_DIFF.patch`. Removing
its three added blocks from the execution revision reconstructs the complete
design revision with the recorded `c4046a7d...` hash. The additions are the
positive-density/vacuum-domain restriction, the stationary-waterbag reference
with its static-vacuum qualification, and the derived high-density energy
asymptote with its pressure-invisible density-linear term. The last addition
is new explanatory algebra, not merely prose. No pre-existing action, EOS,
gradient, mode, or BVP equation was changed. The added energy expansion is
consistent with the exact EOS: `rho/rho_*=y-3/5+O(1/y)` gives
`W_min-V=(5B/(2rho_*))rho-B log(rho/rho_*)-B+o(1)`.

See `INPUT_PROVENANCE.json` and the run manifest. The decisive definitions are
EOS.md sections 1-2 (canonical waterbag and density scale), REPORT.md sections
1-2 (full relative kinetic metric Hamiltonian), and halo/DERIVATION.md sections
1 and 3 (auxiliary enthalpy variable and quarter-density column).

Use fixed `k,B,C_s>0`, with `C_s=F^2 c_chi^2`, and the energy relative to the
constant vacuum baseline,

    E = integral [k rho^(5/3) exp(-2s)
          + B(exp(3s)-3s-1) + (C_s/2)|grad s|^2 + rho Phi/2] d^3x,
    Delta Phi = 4pi G rho,       Phi(infinity)=0,
    rho>=0,       integral rho d^3x=M.                         (1)

Adding the constant `V` to the local energy does not change these static
variations. Its infinite homogeneous baseline is subtracted in the displayed
finite excess energy. Only conserved rest mass sources the Newtonian Poisson
equation; scalar/internal-energy gravity and cosmological vacuum force are
not included. Physical use requires those approximations to be valid.

The underlying stream action contains `u=j/rho` and `pi_s/rho`, which are not
defined for arbitrary variations through vacuum. This calculation specifies
the static continuation `u=0, pi_s=0` in the exterior. The restricted energy
(1), including `rho^(5/3)=0` at vacuum, has a continuous extension there. We
do not infer a well-posed general vacuum-crossing parent evolution from it.

## 2. Variation: signs, normalizations, and free matter boundary

Write `E_rel=k rho^(5/3)exp(-2s)`. For the Poisson solution with its fixed
infinity gauge, variation of `integral rho Phi/2` is `integral Phi delta rho`.
Stationarity under the mass constraint gives, wherever `rho>0`,

    (5/3)k rho^(2/3)exp(-2s)+Phi=mu.                          (2)

Since density is constrained to be nonnegative, the empty region has
`Phi>=mu`. Thus the positive part used below is the density constraint, not
an exterior profile installed separately. Scalar variation gives

    C_s Delta s = 3B(exp(3s)-1)-2k rho^(5/3)exp(-2s).         (3)

These signs follow directly by integration by parts on the positive scalar
gradient term. The conventional gravitational factor `1/2` in (1) must not
be retained in (2).

Define

    rho_*=(3B/(2k))^(3/5),       h_*=5B/(2rho_*),
    ell^2=h_*/(4pi G rho_*)=5B/(8pi G rho_*^2),
    psi=(mu-Phi)/h_*,           n=rho/rho_*,
    epsilon=C_s/(3B ell^2),     r=r_phys/ell.

`psi,n,s,epsilon,r` are dimensionless. `h_*` is specific energy; `C_s` has
units energy per length so its gradient energy has units energy per volume.
Equation (2) yields

    n=psi_+^(3/2) exp(3s),       psi_+=max(psi,0).

In particular `E_rel/B=(3/2)psi_+^(5/2)exp(3s)`. Equations (3) and Poisson
therefore become

    psi''+(2/r)psi' = -psi_+^(3/2)exp(3s),
    epsilon[s''+(2/r)s'] = exp(3s)(1-psi_+^(5/2))-1.          (4)

The central conditions are

    psi(0)=psi_c in (0,1),       psi'(0)=s'(0)=0,
    s(infinity)=0.                                             (5)

There is no additional independent condition on `psi(infinity)`: its
constant is the unknown mass multiplier. The chosen central depth labels a
family with different masses. In the exterior, `n=0`, so

    psi=mu/h_*+m/r,       m=integral_0^R n r^2 dr,
    M=4pi rho_* ell^3 m.                                      (6)

Setting both `psi_c` and `psi(infinity)=0` would generally overconstrain this
problem. The numerically determined `mu/h_*` is negative in all six cases.

Near the center, regularity gives

    psi=psi_c-n_c r^2/6+O(r^4),
    s=s_c+[exp(3s_c)(1-psi_c^(5/2))-1]r^2/(6epsilon)+O(r^4).

In vacuum the scalar equation is still nonlinear. Its small-amplitude tail
is `s proportional to exp[-sqrt(3/epsilon)r]/r`; the growing solution is
excluded. At finite outer radius `L`, the experiment imposes the corresponding
Robin condition `s'(L)+(sqrt(3/epsilon)+1/L)s(L)=0`. The resulting far-field
amplitude and a longer-domain repetition test this approximation.

## 3. What is established analytically about a regular branch

These observations condition on existence of a regular solution of (4)-(5);
the finite numerical experiment below supplies evidence for particular cases,
not a proof of existence or uniqueness for all parameters.

Poisson gives `psi'=-m(r)/r^2<=0`, so `psi<=psi_c<1`. The scalar maximum
principle then gives

    0<=s(r)<=-(1/3)log(1-psi_c^(5/2)).                         (7)

A negative minimum would make the scalar right-hand side negative while
`Delta s>=0`; a positive maximum larger than the displayed bound would make
that right-hand side positive while `Delta s<=0`. The limiting exterior
value is zero. Consequently density is bounded on every such branch.

If the matter stayed positive to arbitrarily large radius, its decreasing
potential depth would have limit zero: a positive limit would give a positive
lower bound on `n` and force a finite zero. Since `s>=0`, `n>=psi^(3/2)` in
the matter region. Then

    psi(r)=integral_r^infinity m(t)/t^2 dt >= m(r)/r,
    m(r)>=r^3 psi(r)^(3/2)/3,

so `psi(r)<=9/r^4`. But the first inequality also gives
`psi(r)>=m(r0)/r` for any fixed positive `r0`, a contradiction at large `r`.
Hence an existing regular decaying branch has finite matter radius. The scalar
tail is not compactly supported; its exponential decay gives finite exterior
gradient and excess potential energy. At the matter edge `psi'(R)<0`, with
finite `s(R)`, density vanishes as `(R-r)^(3/2)`.

The exact auxiliary profile has
`s_0=-(1/3)log(1-psi_0^(5/2))` and `n_0=psi_0^(3/2)/(1-psi_0^(5/2))`.
Its central scalar Laplacian is

    Delta s_0(0)=-(5/6)n_0(0)^2.                              (8)

Thus the neglected dimensionless central residual has magnitude
`5epsilon n_0^2/6`; small epsilon alone is not sufficient at large concentration.
If a regular expansion in epsilon at fixed `psi_c` is applicable, its formal
leading central correction is `delta s_c=-(5/18)epsilon n_0^2`. This follows
because the right-hand side of the scalar equation has derivative `3` with
respect to `s` at fixed `psi` on the auxiliary solution, and `delta psi_c=0`.
It is a diagnostic, not a uniform error bound. It differs from perturbing at
fixed canonical kinetic energy or fixed central density.

## 4. Total stress and independent conservation checks

Define `a=psi_+^(5/2)exp(3s)` and `u_s=exp(3s)-3s-1`. The matter pressure is
`P_kin=B a`. Scalar gradients are anisotropic: after subtracting the uniform
vacuum stress, the total radial and tangential stresses divided by `B` are

    pi_r = a-u_s+(3epsilon/2)(s')^2,
    pi_t = a-u_s-(3epsilon/2)(s')^2.                           (9)

The scalar stress divergence is
`[C_s Delta s-U'(s)]grad s=-2E_rel grad s`; combining it with the gradient
of `2E_rel/3` gives `rho grad[(5/3)E_rel/rho]`. Equation (2) consequently
requires the radial force balance

    pi_r'+2(pi_r-pi_t)/r=(5/2)n psi'.                        (10)

It would be incorrect to test `P_total'=-rho Phi'` while discarding the
anisotropic term. The script differentiates the computed stresses with a
symmetric five-point stencil, separately from the ODE right-hand side.

Additional independent integral checks are

    m(R)=-R^2 psi'(R)=integral_0^R n r^2 dr,
    epsilon L^2 s'(L)=integral_0^L [exp(3s)(1-psi_+^(5/2))-1]r^2 dr.

In units `4pi B ell^3`, the gravitational energy has two equivalent forms,

    W=(5/2)integral_0^R n psi' r^3 dr
     =(5/4)integral_0^R n[mu/h_*-psi]r^2 dr.

The finite-domain virial identity including scalar gradient energy is

    2E_rel-3E_U-E_grad+W=L^3 pi_r(L),                         (11)

where the three nongravitational energies are integrated in the same units.
The boundary term tends to zero at infinity. All six checks use numerical
quadrature of the solved profile and retain the finite boundary term.

## 5. Conditional stationary kinetic realization

For the full Hamiltonian stated in REPORT.md, let `f(x,p)` denote canonical
phase-space mass density, `j_p=integral p f d^3p`, and
`K=integral |p|^2 f d^3p/2-|j_p|^2/(2rho)`. In the positive-density static
interior with `j_p=pi_s=0`, first variation of the complete Hamiltonian with
respect to `f` gives exactly

    h(x,p)=exp(-2s(x))|p|^2/2+Phi(x).                         (12)

The squared common-momentum term has vanishing first variation at zero, and
the mean-subtraction term in `K` does too. There is no missing common scalar
offset in (12). A single global canonical waterbag

    f=f_* 1_{h<mu}

is constant along the static Hamiltonian trajectories and is a stationary
weak Vlasov distribution for this specified static Hamiltonian. Its local
momentum radius is `p_F=[2 exp(2s)(mu-Phi)]^(1/2)`, giving

    rho=(4pi/3)f_* p_F^3,
    K=(3/10)rho p_F^2=k rho^(5/3),
    k=(3/10)[3/(4pi f_*)]^(2/3).

It therefore reproduces (2)-(4). This supplies a stationary kinetic interior
and an energy-cutoff edge under the specified static vacuum continuation.
It does not derive `f_*`, establish dynamical isotropization, or establish the
parent Hamiltonian's well-posedness under arbitrary variations at `rho=0`.

## 6. Frozen finite experiment and results

`contract.json` was written before the first run. `check_gradient.py` uses
SciPy `solve_bvp` with singular matrix `diag(0,-2,0,-2)` in variables
`(psi,psi',s,s')`, analytic Jacobian, the regular central conditions, and the
outer Robin condition. The initial guess is independently integrated from
the auxiliary local equation. No result-derived tuning or second attempt was
needed; there are no discarded failed cases.

The six cases are `psi_c={0.8,0.95,0.99}` crossed with
`epsilon={1e-4,1e-2}`. The initial outer radius is
`max(R_aux+12sqrt(epsilon/3),1.15 R_aux)`. For both `psi_c=0.99` cases the
outer radius is increased by `max(6sqrt(epsilon/3),0.25 R_aux)` and the BVP
tolerance tightened from `1e-6` to `2e-7`. The node cap is 20,000; the
completed main runs used 998-1,947 nodes.

Define the dimensionless quarter-density column coefficient

    C_q = rho_c r_(rho_c/4) / sqrt(B/(4pi G))
        =sqrt(5/2)n_c r_(n_c/4).                             (13)

Each comparison below holds the parameter `psi_c` fixed, **not** central
density, mass, or an observationally specified halo. The auxiliary column is
computed from the exact local EOS at that same `psi_c`.

| psi_c | epsilon | n_c | R/ell | C_q | Auxiliary C_q | Column change |
|---:|---:|---:|---:|---:|---:|---:|
| 0.80 | 0.0001 | 1.673131 | 3.610597 | 3.583586 | 3.583802 | -0.00603% |
| 0.80 | 0.01 | 1.638135 | 3.608306 | 3.564215 | 3.583802 | -0.54653% |
| 0.95 | 0.0001 | 7.656406 | 3.494013 | 5.211541 | 5.212259 | -0.01377% |
| 0.95 | 0.01 | 5.958631 | 3.473763 | 5.165667 | 5.212259 | -0.89389% |
| 0.99 | 0.0001 | 35.918294 | 3.513311 | 5.746734 | 5.717729 | +0.50727% |
| 0.99 | 0.01 | 11.925083 | 3.491619 | 5.817851 | 5.717729 | +1.75108% |

For the last two cases the exact auxiliary central density is
`39.698746249805936`. In the stronger-gradient case its reduction to `11.925083`
is substantial despite the relatively modest column change. Closeness to the
logotropic limiting number `5.84477...` therefore does not establish a small
scalar-gradient correction or a universal finite-gradient column law.

All predetermined checks passed. Across the six main cases, the maximum mass
quadrature relative error was `7.90e-9`, the scaled scalar integral error
`3.64e-11`, the finite-difference force error `7.44e-8`, and the scaled virial
error `4.33e-12`. The largest far-boundary scalar amplitude was `1.33e-11`.
The combined domain/tolerance repetitions changed radius, mass, central
density, and column by at most `6.82e-9` fractionally. These are finite
numerical diagnostics, not interval-certified error bounds. PPoly second
derivatives exactly at the singular endpoint are stored as unverified auxiliary
diagnostics, not as evidence of pointwise center accuracy. Their reconstructed
central Laplacian differs from the scalar equation by up to about `2.1e-4`
relatively in the main cases. Zero central first derivatives are separately
enforced. This discrepancy was not a tested gate and is not silently promoted
to a passing curvature-accuracy claim.

The runner reports `completed`, elapsed `0.620` seconds, with 180-second wall,
150-second CPU, one-thread, and 262,144-byte output caps. No warnings were
written to stderr. Its v2 manifest passed the installed manifest validator
against the current source hashes. Machine-readable results and sampled
profiles are in `run/result.json` and `run/profiles.npz`.

## 7. Reproducibility and interpretation

The decisive artifacts and hashes are:

| Artifact | SHA256 |
|---|---|
| `check_gradient.py` | `1f5cb1020eda2238f65a624a8eebac8a77ec2fb07f22fdfec9bd2dca8c562652` |
| `contract.json` | `916b5d77bb02dfacbd5b75c4bda2e6ecaf503f3d6aa38fa5f3bbcc8594260d42` |
| `run/result.json` | `239525486ad8bdc0484e9b47f9d54a111efc0487085ba8ae9fb09b6195f35dbf` |
| `run/manifest.json` | `6fe558e44b2eddf1d85d6329d9d4125e9986c00eacc8eccdc50dea3a460301b7` |

The exact executed argv, software versions, before/after input hashes, dirty
Git state, output hashes, and resource limits are in the manifest. To rerun,
use its documented runner arguments with a fresh output directory and matching
new result/profile paths; existing results must not be overwritten. The direct
scientific command is

    python3 pressure_selection_2026_10_28/finite_gradient/check_gradient.py NEW_RUN/result.json

after the new output directory is created, preferably by the bounded runner.
This code is reusable evidence, not a command inferred from a third-party log.

**Outcome label:** conditional on numerical tolerance and the stated static
model, the implementation and finite assertion pass in the six tested cases.
The derivation and checks here are the route author's self-audit; independent
peer reconstruction must be recorded separately.

This closes the question whether retaining this scalar gradient necessarily
eliminates the demonstrated static halo branch: it does not in the tested
range. The free occupancy `f_*`, constants `B,C_s,V`, central state, physical
validity of the Newtonian/static-vacuum assumptions, stability, and formation
remain outstanding. No matching relation between `B` and `V` was installed.
