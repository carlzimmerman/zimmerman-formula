# Spatial conversion pilot with moving source modes

2026-10-11. This tests the missing spatial channel identified in
[INVERSE_CHANNEL.md](INVERSE_CHANNEL.md) for the positive-contact extension.
It is a **seeded classical envelope calculation**, not a quantum-vacuum
production result and not a halo simulation.

## Model and normalization

Use normalized complex spatial envelopes A and B with mean |A|^2+|B|^2=1.
A represents daughters normalized to sqrt(2 n_s,0); B represents the source
normalized to sqrt(n_s,0). Thus their squared moduli are charge fractions,
not equal physical particle-number densities. Work in x=m epsilon t,
on a periodic box with dimensionless momentum q=p/(m u_*).

After rotating the daughter at M/2 and the source at M, retain their free
relativistic detunings but leading nonrelativistic vertices:

\[
 iA'=L_A A+B A^*+k|A|^2A,\qquad
 iB'=L_B B+A^2,
\]

where R=M/m=2sqrt(1+u_*^2),

\[
 L_A(q)={u_*^2(q^2-1)\over\epsilon[\sqrt{1+u_*^2q^2}+\sqrt{1+u_*^2}]},\qquad
 L_B(q)={u_*^2q^2\over\epsilon[\sqrt{R^2+u_*^2q^2}+R]}.
\]

Here u_*=0.001, epsilon=1e-7, k=0.2000001 is the total quartic coefficient
for the repulsive extension. Coupling factors from 1/omega are approximated
by their nonrelativistic values in the vertices; the retained dispersion
alone does not make this a full relativistic field simulation. Expansion,
gravity, antiparticles and counter-rotating vertices are absent.

The Hamiltonian per initial source quantum in these units is

\[
 E_r=\langle2A^*L_AA+B^*L_BB+2\operatorname{Re}(B^*A^2)+k|A|^4\rangle.
\]

The A equation is iA'=(1/2)delta E_r/delta A*, while B has unit symplectic
normalization. This factor of two is necessary for both conversion and
charge conservation. Differentiation proves conservation of E_r and
mean |A|^2+|B|^2. The source acquires arbitrary represented momenta through
A^2 rather than being constrained to its zero mode.

## Declared initial data and numerical method

Start with mean |A|^2=1e-8 and uniform B=sqrt(1-1e-8). A has reproducible
complex Gaussian Fourier coefficients at all nonzero lattice momenta with
q^2<=4, normalized to that charge. The seed is broad compared with the
instability band and is identical across grids. This is an imposed classical
seed, not the physical quantum vacuum and not the matched output of the
Gaussian quantum calculation.

The Fourier spacing is dq=0.4. Increasing N keeps the box and initial modes
fixed and adds higher momenta. This tests the ultraviolet spatial cutoff,
not box-size or continuum-of-momenta convergence. The code uses symmetric
half kinetic steps and a fourth-order Runge-Kutta local nonlinear step.
All Fourier modes remain available during evolution; daughters and moving
sources can scatter outside the initially occupied region. There is no
explicit dealiasing, so comparison across grids is essential.

[spatial_conversion.py](spatial_conversion.py) runs N=16 and 24 at dt=0.01,
then N=24 at dt=0.005, through x=30. It records daughter and source charge,
nonzero-momentum source charge, energy, and charge in outer Fourier modes
every 0.5 time unit. Numerical diagnostics are charge drift below 1e-4 and
energy drift below 0.01; these are pilot thresholds, not physical error bars.
The execution and scientific result are recorded in `spatial_conversion_run`.

This experiment answers whether substantial moving-source population is
present in one resolved classical trajectory. It cannot establish vacuum
production, a cosmic abundance, or the repository's universal halo profile.

## Results and controlled comparison

The spatial pilot completed. All six diagnostics pass.

| Grid / step | Daughters at x=30 | Moving source charge at x=30 | Max energy drift |
|---|---:|---:|---:|
| 16^3 / 0.01 | 0.63615218 | 0.24006864 | 5.64e-5 |
| 24^3 / 0.01 | 0.63615053 | 0.24006900 | 5.64e-5 |
| 24^3 / 0.005 | 0.63618321 | 0.24006944 | 1.41e-5 |

The last run conserves total charge to 5.11e-11. Halving the step reduces
energy drift by about four, consistent with the second-order splitting.
Its endpoint daughter fraction changes by 3.27e-5. Moving-source population
is robust at the displayed percent scale, not established to every table
digit. The finer grid's outer-mode charge is about 1e-8 at the endpoint.
This is evidence about this finite box, seed and time interval, not general
continuum or ensemble convergence. [Results](spatial_conversion_run/results.json)
and [manifest](spatial_conversion_run/manifest.json) retain the runs.

A separate [uniform-source control](spatial_uniform_control.py) uses exactly
the same initial field, N=24, dt=0.005 and Hamiltonian terms, but projects
B's nonlinear derivative to its spatial average. This variational restriction
preserves the reduced energy and charge; it changes the physical channels
rather than adding damping. Its two diagnostics pass, with charge drift
5.14e-12 and energy drift 6.61e-6. See [control results](spatial_uniform_control_run/results.json)
and [manifest](spatial_uniform_control_run/manifest.json).

At x=30 the control has daughter fraction 0.643884 rather than the spatial
run's 0.636183: a modest endpoint difference. But the largest difference
among the 0.5-spaced samples occurs at x=25.5:

* full spatial source: daughter fraction 0.480076;
* constrained uniform source: daughter fraction 0.981064.

This approximately 0.501 difference in fraction is far larger than the
observed grid or time-step differences. The endpoint alone obscures a large
change in conversion history. Neither result is a final relic yield.

## Consequence for the research claim

Substantial conversion occurs in this spatial seeded example, and moving
sources are populated without inserting them initially. The previously
identified inverse channel is therefore dynamically active in the envelope
model, not merely a kinematic possibility. A homogeneous pump cannot be
assumed accurate throughout the nonlinear conversion stage.

The earlier Gaussian runs have different initial quantum correlations and
include expansion; this classical comparison does not numerically correct
their 91.8% or 94.9% fractions. It instead demonstrates that their omitted
channel can have order-one effects in a closely related nonlinear regime.
Their fractions must stay labeled as uniform-source truncation results.

The strongest next continuation is a matched high-occupation quantum-to-
classical initialization, retaining its anomalous covariance, followed by
spatial evolution and box/ensemble checks. An arbitrary classical seed
cannot be relabeled as that matching. Full quantum evolution remains an
alternative. The galaxy-law and source-origin obligations also remain open.
