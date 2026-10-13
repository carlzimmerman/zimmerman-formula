# The initial shell cannot be frozen during condensate growth

2026-10-11. The preceding turn constructed a conserving source collision
operator. Before evolving it, this turn tests the initial inverse reaction
and whether a sharp on-shell approximation is uniformly appropriate. The
inputs are the revised alpha=2 production spectrum, not a prescribed thermal
bath. The result strengthens the earlier moving-source warning with an
independent, conditional kinetic calculation.

## Exact decay geometry, approximate statistical description

Let e_b be source kinetic energy, P=sqrt[e_b(2M+e_b)] its momentum and
p_star=sqrt(M²-4m²)/2 the rest-frame daughter momentum. The daughter kinetic
energy is uniform in the exact interval

    center=(M-2m+e_b)/2,
    half_width=P p_star/M,
    e_1=center+half_width*cos(theta),
    e_2=M-2m+e_b-e_1.

The lab decay rate is Gamma_lab=Gamma_vac M/(M+e_b). For a held-fixed,
isotropic daughter occupation f(e), define uniform angular averages over
this interval. An incoherent source-mode occupation B obeys

    dB/dt = Gamma_lab [<f1 f2> - (1+<f1+f2>)B].

This follows by subtracting inverse and forward Bose products, as in the
rest-source calculation. The initial gain at B=0 is Gamma_lab <f1 f2>;
the fixed-bath relaxation rate is Gamma_rel=Gamma_lab(1+<f1+f2>).
The source density of states per kinetic energy is exactly

    g_b(e_b)=P(M+e_b)/(2pi²).

Integrating g_b times the initial gain gives the initial source number flux R.
Each source removes two daughters, giving charge-depletion slope 2R/n_daughter.
The reciprocal is a local slope timescale, not a finite-time depletion solution.

The bath occupations are reconstructed from the saved Gaussian mode numbers,
with piecewise-linear interpolation and zero occupation outside the computed
band. Anomalous correlations, coherent source amplitudes and feedback are
excluded. Therefore this is still a conditional quantum-to-kinetic diagnostic;
exact vacuum kinematics does not validate that handoff.

## Resolved calculation

The source recoil integral uses e_b=e_max*u² to resolve the origin. Daughter
energy integrals are restricted to the actual occupied support rather than
sampling the whole much-wider kinematic interval. Four saved production grids
and 96/192/256-point integration rules give:

| Production modes / half-band | Quadrature | Initial fractional daughter depletion rate (/s) | Reciprocal slope time (s) |
| --- | ---: | ---: | ---: |
| 512 / 2 | 96 | 1.83121e8 | 5.46086e-9 |
| 1024 / 2 | 192 | 1.83183e8 | 5.45901e-9 |
| 1536 / 3 | 256 | 1.83309e8 | 5.45527e-9 |
| 1024 / 2, tighter production tolerance | 192 | 1.83183e8 | 5.45901e-9 |

The integrated flux agrees within the declared 1% threshold, with the sampled
spread about 0.1%. This is consistent in scale with the earlier frozen-field
moving-source response. Neither approximation is an evolved source fraction.
The inverse-conversion slope is about a million times faster than the previous
184.76 /s condensate gain coefficient computed on the same fixed cloud.
Thus that condensate coefficient cannot be integrated through milliseconds
while leaving the production cloud unchanged.

## Broadening diagnostic

Use W=hbar*Gamma_rel as a width estimate from the fixed-bath occupation
relaxation law. This is not a self-consistent spectral function or a calculated
memory kernel. Across the sampled quadratures:

- Flux-weighted source recoil energy is about 1.11e-5 eV.
- Flux-weighted W is about 3.75-3.84e-6 eV.
- Daughter rms shell energy spread is 9.66544e-6 eV.
- About 22-24% of the estimated initial source flux comes from modes with
  W greater than their recoil energy.
- About 4-5% comes from modes with W greater than the daughter rms spread.

The threshold fractions have not been independently converged and are quoted
as ranges, not precision results. A width exceeding recoil is a warning about
uniformly resolving the near-zero source dispersion; it is not by itself a
proof that every quasiparticle or kinetic approximation fails. In particular,
recoil is not the source rest mass or the full mass gap. A broadened treatment
must determine how much these low-recoil modes change the integrated dynamics.

## Evidence and next decision

`source_initial_width.py` uses the exact boosted daughter mass shell as a
kinematic control and compares the integrated initial flux across the four
runs. All seven finite checks pass. The manifest validates input/output
provenance. The checks do not establish a spectral width or an actual
nonlinear reaction timescale.

The previous source operator remains a useful conserving kinetic component,
but starting it from a coarse bin or treating the initial source spectrum as
uniformly sharp would not be justified by the available evidence. The next
coupled calculation must evolve the rapidly changing source/daughter spectrum
and account for the low-recoil region, or establish a later kinetic initial
state after the coherent stage. Broadening and correlations should be tested
where they matter instead of replacing them with an imposed equilibrium.

This does not negate the quantum low-pressure bound or the conditional Bose
endpoint. It identifies why a fast, favorable condensate gain coefficient is
insufficient to connect them dynamically. No condensation yield, halo profile,
or complete cold-energy realization is claimed here.
