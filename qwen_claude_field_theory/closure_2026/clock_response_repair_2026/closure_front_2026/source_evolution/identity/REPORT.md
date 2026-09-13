# Exact source and no-slip identity from the quadratic ADM action

Base: `486edc78eaed87647c0b605cdbebccb996a464cf`. This derivation starts
from the fixed action's quadratic ADM density in
`../../finite_wavelength/adm/REPORT.md` and adds exactly the lapse source in
`../../finite_wavelength/PROBE.md`. It introduces no coefficient function,
background history, source coupling, or force law.

**Claim and verdict: proved as written.** For a differentiable solution of
the displayed on-background-shell quadratic scalar action with constant
nonzero Einstein coefficient, a nonzero Fourier wave number and the
minimally coupled conserved signed dust probe, the separately reconstructed
Newtonian potentials satisfy `Phi=Psi`. This is a linear finite-mode result,
conditional on using this quadratic action and its regular gauge. It is not
a nonlinear stress theorem, a PPN calculation, or a galaxy solution.

## Definitions and independent reconstruction

Use `M=M2` (so `M^2` in the following formulas means `(M2)^2`),
`r=k^2/a^2`, `ell=Delta B`, and `u=a^2 B=-ell/r`. The linear ADM metric is

    g00=-1-2n,   g0i=partial_i u,
    gij=a^2(1+2zeta)delta_ij.

Under a time shift `t_new=t+T`, the amplitudes transform as
`n_new=n-Tdot`, `zeta_new=zeta-H T`, and `u_new=u+T`.
Taking `T=-u` sets the shift to zero. Reading the lapse and spatial
curvature in that gauge, with `gij=a^2(1-2Psi)delta_ij`, gives independently

    Phi=n+udot,                  Psi=-zeta-Hu.

For fixed comoving `k`, `rdot=-2H r`. Thus these observables in the original
gauge are

    Phi=n-elldot/r-2H ell/r,     Psi=-zeta+H ell/r,
    Phi-Psi=n+zeta-(elldot+3H ell)/r.

No stress assumption or equality of potentials has entered these definitions.

## Vary the action before imposing constraints

Let `v=zetadot`, and use the normalization `L=2<action density>/a^3`.
The constant factor two has no effect on the equations; the canonical
momentum below is defined consistently from `a^3 L`.

    L=-3M v^2+6Theta n v+Sigma n^2+2(M v-Theta n)ell
      +M r zeta^2+2M r n zeta+D n sigma-3W sigma v+W sigma ell
      +(E-C r)sigma^2/2-rho n.

The coefficient names are exactly those of `PROBE.md`:

    Theta=M H+gamma q^3,
    Sigma=q^2 P_X+2q^4 P_XX-3M H^2-12gamma H q^3,
    C=W-2q^2 W_Y,
    D=P_tau-V_tau-2q^2 P_Xtau,
    E=P_tautau-V_tautau-3H W_tau.

The shift row and the velocity derivative are

    E_shift=L_ell=2M v-2Theta n+W sigma,
    m=L_v=-6M v+6Theta n+2M ell-3W sigma
         =2M ell-3E_shift.

The lapse source `-rho n` contributes neither a shift row nor a curvature
row. Direct differentiation gives

    L_zeta=2M r(zeta+n),
    E_zeta=(d/dt+3H)m-L_zeta.

Consequently the exact identity, before setting either perturbation row to
zero, is

    2M r(Phi-Psi)+E_zeta+3(d/dt+3H)E_shift=0.             (1)

All derivatives here act on the actual time-dependent coefficients. In
particular `Thetadot` and `Wdot` cancel between the last two terms; neither
is frozen. Equation (1) follows by expanding the two rows and the displayed
potential definitions. On a differentiable constrained solution,
`E_shift=dot(E_shift)=E_zeta=0`; dividing by `2M r` proves the claim.

This also explains exactly which residuals a numerical slip measurement
tests. Agreement obtained by substituting the analytic identity is a
consistency reconstruction, not an independent numerical evolution check.

## Canonical form and Schur-elimination check

For `p=a^3 m`, the shift row gives

    p=2M a^3 ell,
    pdot=2M a^3 r(zeta+n),
    u=-p/(2M a k^2).

Differentiating this expression for `u`, rather than substituting `Phi=Psi`,
gives

    Phi=n-pdot/(2M a k^2)+H p/(2M a k^2),
    Psi=-zeta+H p/(2M a k^2).

The curvature equation then proves equality. The symbolic script separately
eliminates lapse, clock, and shift directly from `L`, and checks both

    partial Leff/partial v = 2M ell,
    partial Leff/partial zeta = 2M r(zeta+n)

after reconstruction. These checks matter: replacing the lapse using the
shift equation alone does not yet set the lapse variation to zero. The
Schur-envelope identities hold after the lapse equation has also been used
to reconstruct `ell`.

## Source-compatible finite-time initial slice

Write

    Dcal=C r-E-D W/Theta-Sigma W^2/(2Theta^2),
    J=M(Sigma W+D Theta)/Theta^2,
    f=rho W/(2Theta),
    F=-rho M/Theta-J f/Dcal.

For the initial choice `zeta=zetadot=0`, the original auxiliary rows force

    sigma0=-f0/Dcal0,
    n0=-rho0 W0^2/(4Theta0^2 Dcal0),
    p0=a0^3 F0,
    ell0=F0/(2M),
    u0=-F0/(2M r0),
    Phi0=Psi0=H0 F0/(2M r0).

In particular, a nonzero source generally has nonzero constrained metric
and clock perturbations on this slice. Choosing `p0=0` instead gives
`zetadot0=-F0/A0` at `zeta0=0`, where `A0=partial_v^2 Leff` is the effective
kinetic coefficient; it is a different initial condition unless `F0=0`.
The equality at the initial time uses `pdot0=2M a0^3 r0 n0`, which is fixed
by evolution. It does not assume `udot0=0`.

The signed density is `rho=rho_star/a^3` multiplying `cos(kx)`, with zero
homogeneous density, pressure and momentum. At this perturbative order,
background conservation is `rhodot+3H rho=0`; corrections involving the
metric perturbations multiply `rho` and are higher order. The script checks
this continuity equation exactly. The slip algebra alone would still
cancel for a lapse-only prescribed forcing with arbitrary time dependence;
that fact does not make a nonconserved source covariantly admissible.

## Hypotheses, exclusions, and audit record

The same action's ADM expansion contains the background residual terms

    3E0 n zeta+3Et zeta sigma+(9/2)Ea zeta^2.

They vanish only on a background satisfying the lapse, clock and spatial
Einstein equations defined in the ADM report. If those terms are retained,
equation (1) acquires the additional term
`3E0 n+3Et sigma+9Ea zeta` on its left-hand side. The script verifies this
remainder, so the background restriction is explicit.

The identity needs `M!=0`, `a>0`, `k!=0`, and a differentiable solution in
the unitary-chi gauge (`q!=0`). The identity itself never divides by `H`,
`Theta`, the clock Schur denominator, or the kinetic coefficient. Explicit
Schur reconstruction and the canonical numerical system additionally need
their respective denominators nonzero. This proof supplies no continuation
through a singular elimination branch and no statement for the homogeneous
mode, which lacks an independent longitudinal shift row.

The dependency graph is: fixed quadratic ADM action and lapse-only source
-> direct variation and gauge transformation -> identity (1) -> no slip on
differentiable solutions. The action-to-quadratic expansion is the existing
ADM artifact; this package does not replace it with a newly fitted action.

| Obligation | Status | Evidence |
| --- | --- | --- |
| Input action, normalization and coefficient map | Passed within the supplied action | Explicit density and raw ADM code inspected |
| Independent potential definitions | Passed | Time-gauge calculation and two exact checks |
| Perturbation-row cancellation | Passed | Identity (1), exact symbolic check, Lean algebra |
| Full auxiliary reconstruction | Passed on regular branch | Three original rows and two Schur-envelope checks |
| Nonzero-source initial data | Passed on regular branch | Six exact initial-data checks |
| Conserved source | Passed at stated perturbative order | Exact background continuity equation |
| Background residual exclusion | Passed | Explicit off-background-shell remainder |
| Covariant action formalization in Lean | Not addressed | External to the three algebra lemmas |
| Nonlinear slip, galaxy, PPN, numerical force | Out of scope | No such inference |

`derive_identity.py` uses exact rational-function algebra, with no random
sampling or numerical tolerance. It does not import `probe.py` or reuse its
assigned formulas to compute the varied rows. `NoSlip.lean` proves three
real-algebra lemmas for the displayed rows. Its derivative jets are supplied
real numbers, so it does not formalize differentiation, the action, the
background equations, source conservation, or solution existence. It uses
no custom axioms and no `sorry`; printed dependencies are the standard
`propext`, `Classical.choice`, and `Quot.sound`.

The reproducible run contracts pin the new code and the relevant input
artifacts. `run_001/manifest.json` records the symbolic run;
`lean_run_001/manifest.json` records compilation against the repository's
Lean/Mathlib toolchain. All 22 exact checks passed in 1.442 seconds with
Python 3.9.6 / SymPy 1.14.0. All three Lean lemmas compiled in 1.603 seconds
with Lean/Mathlib 4.34.0-rc2. Both processes exited zero, stderr was empty,
and both version 2 manifests passed the computation-audit validator with
`--root`, including input/output hashes. Revalidate the manifests before
reuse if any inputs change.

Mathematical proofreading self-review is limited to this new report and
the corresponding script and Lean notation; no unrelated manuscript was
edited. No unresolved notation issue or mathematical-token correction was
found during that review.
