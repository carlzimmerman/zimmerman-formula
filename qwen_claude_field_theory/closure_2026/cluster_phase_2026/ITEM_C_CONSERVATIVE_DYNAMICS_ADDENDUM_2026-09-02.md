# Item C addendum: conditional phase pinning and the conservative-selection obstruction

Date: 2026-09-02
Applies to: Zenodo `10.5281/zenodo.22242701` and `ITEM_C_PHASE_PINNING_VERDICT.md`.

## Bottom line

The published static result survives. Near the AeST condensate minimum, the Q sector is a Lane--Emden `n=1` polytrope to relative accuracy about `10^-5` at cluster potential depth. Its positive free-surface family is real, its shallow shape explains the core deficit, and the original 27-check calculation reruns with zero failures.

The stronger statement “the phase pins dynamically” must be narrowed to **conditional pinning**:

> Given a captured dust mass and the explicit dissipative shock prescription used by the numerical fluid solve, different tested radial density phases relax near the corresponding positive hydrostatic polytrope.

The calculation does not derive a unique captured mass or a dissipative selection law from the conservative AeST action.

## 1. The exact equation of state

For `L=A u^2`, with `u=Q-Q0`, the exact pressure and density are

    p = A u^2,
    rho = A(2 Q0 u + u^2).

Therefore

    c_s^2 = u/(Q0+u),
    gamma_eff = d ln p / d ln rho = (2Q0+u)/(Q0+u),

and

    p(rho) = A [sqrt(Q0^2+rho/A)-Q0]^2.

The exact residual from the quadratic polytropic law is

    p - rho^2/(4 A Q0^2) = -A u^3(4Q0+u)/(4Q0^2).

Thus `gamma=2` is the small-`u/Q0` limit, not an exact finite-field identity. At `u/Q0=10^-5`, representative of the paper's cluster wells, both the gamma error and pressure-law error are about `10^-5`. This does not materially change the published cluster numerics, but the title-level statement should be read asymptotically.

## 2. Positivity fixes a family, not a mass

For the isolated `n=1` Lane--Emden benchmark,

    rho(r) = rho_c sin(mu r)/(mu r),
    R_s = pi/mu,
    M = 4 pi^2 rho_c/mu^3.

The radius is independent of `rho_c`, while `dM/d rho_c=4 pi^2/mu^3` is nonzero. Positivity and the first-zero surface select the shape/branch but leave a continuum labeled by central density or captured mass. This is also visible in the paper's own Part D, which calls the physical solutions a one-parameter family.

The phase is therefore the captured mass; it is not fixed until a capture model or boundary history fixes that mass. Setting the mass equal to the cosmic dust share inside `R500` is a useful benchmark, not an action-derived selection.

## 3. Why the action alone does not make an attractor

For any conservative linearized phase mode with

    H = (p^2 + omega^2 q^2)/2,

Hamilton's equations give

    dH/dt = 0,
    div(q_dot,p_dot) = 0,
    eigenvalues = +/- i omega.

There is no phase-space contraction and no generic asymptotic attractor. Adding damping gives

    p_dot = -omega^2 q - nu p,
    dH/dt = -nu p^2,
    div flow = -nu,

which can relax to equilibrium.

The published simulation explicitly uses an artificial compression viscosity

    q_visc = cq rho (Delta v)^2,  cq=2,

and renormalizes every initial phase profile to the same `M_dust`. The observed five-percent spread therefore verifies robustness of a particular dissipative, fixed-mass numerical relaxation. It does not establish that the fundamental shift-symmetric scalar action supplies the same entropy production or selects the mass.

## 4. New falsifiable reframe

The unconstrained variable is no longer an abstract Helmholtz phase; it is a capture fraction. This gives a cleaner empirical target:

> At fixed baryonic potential and `mu`, cluster-to-cluster variation in captured Q-sector mass should map monotonically into the outer acceleration enhancement and approximately linearly into the dust mass of the shallow core.

In the pure `n=1` benchmark, the enclosed fraction is

    M(<r)/M_tot = [sin x - x cos x]/pi,  x=mu r.

For `mu^-1=1 Mpc`, the fraction inside 420 kpc is only `0.0077` of the full first-zero polytrope, and the ratio `M(<420 kpc)/M(<1.56 Mpc)` is `0.0247`. This analytic benchmark independently exposes why adding more captured mass mainly worsens the `R500` overshoot before filling the core. Baryons shift the published numerical fraction to about three percent but do not change the geometric mechanism.

The environmental prediction is assembly-history scatter, not a universal zero-scatter phase. A physical capture calculation should predict that scatter and its correlation with turnaround history.

## 5. Next unavoidable calculation

To promote conditional pinning to action-derived pinning, one must derive a well-posed weak/UV completion of the same AeST scalar action which:

1. resolves shell crossing or gradient catastrophe without an inserted viscosity;
2. supplies an entropy/causal prescription and proves positive energy;
3. evolves the total captured mass from cosmological initial data rather than fixing it;
4. converges as the regularization is removed or matched to specified higher-derivative operators;
5. retains the full vector/metric constraints and counts all propagating modes.

Until then, the static cluster result is **SUPPORTED**, the dissipative fixed-mass relaxation is **SUPPORTED**, and unique action-derived phase/mass pinning is **OPEN**. This does not close the fried-chicken target; AeST's additional gravitational modes and unclosed full PPN sector remain separate failures.

## Reproducibility

    python3 itemC_phase_pinning_dynamics_2026.py
    python3 test_itemC_phase_pinning_conservative_audit_2026.py
    python3 itemC_phase_pinning_conservative_audit_2026.py

Observed on the live tree: original item C `27` checks, `0` failures; independent audit `4` tests and `6` checks, all passing.
