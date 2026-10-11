# Next: capture during assembly, then retention

2026-10-11. Proposed experiment, not an executed result or a claim of novelty
in the wider literature. Scope: the inspected repository routes listed below.

The rotor experiment shows why changing angular momentum alone is insufficient:
longer visits can outweigh fewer entries. The next question is whether a growing
potential selects a retained distribution of initially passing material, and
whether the same dynamics distinguish a galaxy from a star embedded in it.

## What previous failures actually exclude

[CFG461](../../campaign_fresh_gravity/CFG461_settling_temperature_mechanism/README.md)
tests temperature selectors and exposes the missing relativistic scale in the
tested scaling class.
[CFG462](../../campaign_fresh_gravity/CFG462_lapse_settling_edge/README.md)
tests four settling rules whose edges reflect supply exhaustion.
[CFG488](../../campaign_fresh_gravity/CFG488_cosettling_supply/README.md)
applies settling after spherical infall.
[CFG494](../../campaign_fresh_gravity/CFG494_supply_from_adiabatic_ics/README.md)
and [CFG497](../../campaign_fresh_gravity/CFG497_binding_energy_selection/README.md)
classify that supply using labels and instantaneous cuts. Their underlying
[shell code](../../campaign_fresh_gravity/CFG118_secondary_infall/shellcore.c)
starts with a static baryonic core; it does not evolve baryonic contraction.
[through_stream.py](../through_stream.py) also has a fixed potential. These
records do not decisively exclude capture during an evolving potential.

## A stellar exclusion assumption that needs testing

[CFG484's frozen criteria](../../campaign_fresh_gravity/CFG484_alternative_chassis_search/FROZEN_CRITERIA.md)
use a coarse-grained Maxwellian peak
`f_max = rho_host / [(2 pi)^(3/2) sigma_host^3]` in a Liouville bound on
Sun-bound mass. That bound is conditional on the stipulated incident
distribution. A coarse-grained peak is not automatically an upper bound on
the fine-grained density of cold substreams. This is an assumption audit;
it does not alter those criteria or show that their calculation is wrong.

For an explicit counterexample to a bound inferred from moments alone, let
`N_sigma(v)` be the normalized, zero-mean isotropic Gaussian in three velocity
dimensions with one-dimensional variance `sigma^2`. Set

\[
 f_\epsilon(v)=\rho[\epsilon N_{\sigma_c}(v)
 +(1-\epsilon)N_{\sigma_h}(v)],\qquad
 \sigma_h^2=\frac{\sigma_H^2-\epsilon\sigma_c^2}{1-\epsilon}.
\]

For fixed `0 < epsilon < 1` and sufficiently small positive `sigma_c`, this
keeps density, mean velocity and covariance fixed, while
`f_epsilon(0) >= epsilon rho / [(2 pi)^(3/2) sigma_c^3]` diverges as
`sigma_c -> 0`. The construction proves only that those moments do not fix
the peak. It neither predicts the actual incident distribution nor guarantees
capture, a cold stream at rest relative to the Sun, or a large stellar halo.

## Exact capture accounting

Let `f` be mass density on canonical phase space, evolving by
`partial_t f + {f,H}=0`, and let `E_s(t)` be a scalar escape threshold in
the same Hamiltonian convention. Assuming integrable distributions, vanishing
outer boundary flux and a regular energy boundary, define

\[
 M_B=\int f\,\Theta(E_s-H)\,d\Gamma.
\]

Integration by parts in the Poisson bracket gives

\[
 \boxed{\dot M_B=\int f\,\delta(E_s-H)
 [\dot E_s-\partial_tH],d\Gamma.}
\]

This is an instantaneous energy-domain flux, not a theorem of permanent
capture. Both inward and reverse crossings count. Use a finite incident
population: an infinite uniform bath can make the bound-mass integral diverge
in a Kepler tail. For an isolated potential with zero at infinity, use specific
Hamiltonian `H=v^2/2+Phi` and `E_s=0`. A fixed-mass contracting Plummer source
has

\[
 \Phi=-\frac{GM}{\sqrt{r^2+b(t)^2}},\qquad
 \partial_t\Phi=\frac{GM b\dot b}{[r^2+b^2]^{3/2}}.
\]

Contraction (`dot b < 0`) allows inward flux across the energy boundary if
that boundary is populated. Prescribing `b(t)` requires an explicit work
ledger; it does not supply a closed energy-conserving theory of assembly.

For an embedded star, a global energy cut alone can include the host or
disconnected regions. A weight `W` selecting the relevant connected region
(or a smooth approximation to its indicator) instead gives

\[
 \dot M_W=\int f\left[(\partial_tW+\{W,H\})\Theta(E_s-H)
 +W\delta(E_s-H)(\dot E_s-\partial_tH)\right]d\Gamma.
\]

The first term accounts for transport across the region boundary and must
not be discarded. Sharp indicators require weak derivatives or smooth
regularization; saddle energies need care beyond regular-surface delta
evaluation. W must describe a physical region, not encode desired ownership.
A rotating-frame calculation must use its proper canonical
Hamiltonian, including frame terms. An energy threshold in a changing tidal
field still needs a trajectory-based retention check.

## Smallest useful next experiment

1. Compare a static source with a contracting source of the same final mass
   and profile, using an explicitly specified initially unbound distribution.
   Record each orbit's energy change and the matching baryonic work.
2. Measure energy-boundary flux, then retained mass, angular momentum and
   residence after contraction ends. Vary assembly time and incident velocity
   dispersion; do not impose a target enclosed mass or a partner label.
3. Repeat the retention test for a star embedded in a host tide, with both
   the stipulated smooth incident distribution and resolved cold substreams.
   Use the physical escape region and the full boundary-flux accounting.

The first decision is whether assembly produces a robust separation between
galaxy retention and stellar retention. A negative result constrains this
mechanism; a positive one earns a self-consistent baryonic evolution test.
Neither outcome by itself identifies a microscopic cold carrier or derives
its abundance, the universal density law, or the vacuum normalization.

Keep the normalization problem separate and explicit: if
`a0 = kappa c sqrt(G rho_DE)` and `Lambda = 8 pi G rho_DE / c^2`, then
`Lambda c^4 / a0^2 = 8 pi / kappa^2`. The choice `kappa=1/2` yields `32 pi`,
not `32 pi^2`, in these conventions. Capture must eventually connect to an
independently specified vacuum coupling before it can determine kappa.
