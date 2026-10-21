# Independent tensor coefficient/sign check for CFG938

This is analytic review of the pinned CFG938 action, not a run of its experiment or a classification of every possible continuum completion. Work first in c=1. Let K=4pi G, take comoving labels and homogeneous chi(t), and use a Bianchi-I shear parametrization

`g_ij=a^2 exp(2 beta_i) delta_ij`, `sum_i beta_i=0`.

Write `H_i=H+betadot_i`. The spatial projected Hessian and its trace are

`D_iD_j chi=-g_ij chidot H_i` (no sum for diagonal i),

`D2 chi=-chidot sum_i H_i=-3H chidot`.

Therefore

`tau_ij=-g_ij chidot betadot_i`,

`tau_ij tau^ij=chidot^2 sum_i betadot_i^2`.

After discarding the usual Einstein-Hilbert time boundary term, its shear kinetic density is

`L_EH,shear=a^3/(4K) sum_i betadot_i^2`.

The adopted negative chi-tidal term adds

`L_tidal,shear=-3 gamma a^3 chidot^2/(4K^2) sum_i betadot_i^2`.

Thus the exact shear coefficient on this configuration is

`Q_T=1-3 gamma chidot^2/K`.

This also independently fixes the small-TT normalization: `h_ii^TT=2 beta_i` gives the EH coefficient `a^3/(16K)` and tidal correction `-3 gamma a^3 chidot^2/(16K^2)` multiplying `hdot_ij^TT hdot_ij^TT`. Equivalently at linear order `delta tau_ij=-a^2 chidot hdot_ij^TT/2`.

## No principal cancellation from the other displayed sectors

- `sqrt(-g) n=1` exactly for these synchronous comoving label fields. The dust action has no shear kinetic dependence.
- `h^{mu nu} partial_mu chi partial_nu chi=0` exactly, so W supplies none.
- `sqrt(-g) lambda(D2chi-Kmn) = -a^3 lambda(3H chidot+K m/a^3)` is exactly independent of beta in this trace-free parametrization. It cannot cancel the shear term, even before choosing lambda=0. In the linear TT expansion a trace `h hdot` contribution is a parametrization/boundary/background term, not a new principal tensor kinetic coefficient.
- Scalar chi/lambda and scalar fluid perturbations have no linear coupling to a traceless TT perturbation of an isotropic background. Second-order scalar adjustments multiply the already satisfied background equations and do not cancel the quadratic principal TT term.

For a propagating TT perturbation about homogeneous chi, the tidal correction contains time derivatives of the metric through Gamma^0_ij; it supplies no matching principal tensor spatial gradient. Within the displayed action the corresponding characteristic ratio is therefore `c_T^2=1/Q_T` in c=1. At Q_T=0 the quadratic tensor kinetic term degenerates. At Q_T<0 it has negative tensor kinetic sign and the usual positive EH gradient yields a negative frequency-squared ratio. This is a branch-specific failure of the truncated displayed theory, not a theorem about all modified actions or its unspecified UV completion.

## Background constraint, physical units and BBN scope

Using the adopted homogeneous constraint `-3H chidot=K rho_c` in c=1 gives

`Q_T=1-gamma K rho_c^2/(3H^2)`.

If the background has the stipulated dust/radiation Einstein equation `H^2=2K rho_tot/3`, then

`Q_T=1-(gamma rho_c^2/2)/rho_tot` (c=1).

Restoring SI while defining rho_c and rho_tot as mass-equivalent densities gives

`Q_T=1-[gamma rho_c^2/2]/[rho_tot c^2]`.

Here `-3H (dchi/dt)/c^2=K rho_c`, and the direct cosmic-time expression is `Q_T=1-3 gamma (dchi/dt)^2/(K c^6)`. This removes the ambiguity between derivatives with respect to t and x0=ct, and between rest mass density and energy density.

Thus the local-equation-of-state stiff-energy/radiation ratio quoted in CFG938, although absent from the adopted tidal branch's exact background stress, reappears as its tensor kinetic deficit on that same homogeneous chi background. If the medium is already present with the declared abundance at BBN and the dust/radiation background assumptions hold, the quoted ratios 1.3e3..2.3e6 are much larger than unity and imply negative Q_T on this branch. The numerical ratios are quoted from the frozen source; this review did not rerun their cosmological arithmetic. A different medium-formation epoch, nonstandard background or modified action requires its own analysis. Neither those alternatives nor a present-day numerical bound was computed here.

The useful next independent control is precisely this Bianchi-I identity plus the full quadratic TT expansion of the action, with the source's cosmological substitutions and unit convention recorded. A flat frozen-projector check cannot establish its tensor or expanding-background constraint claims.
