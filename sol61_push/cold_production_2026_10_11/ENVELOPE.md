# A depleted source with cosmological mode occupation

2026-10-11. This is a narrow-band Gaussian quantum model derived from the
candidate conversion vertex. It addresses the very large mode occupation
that invalidated a dilute exponential-decay treatment. It is still a
reduction of the proposed action, not the full nonlinear field evolution.

## Physical benchmark

Choose daughter mass m=1e-12 eV, radial amplitude epsilon=1e-7,
u_*=0.001 and M=2m sqrt(1+u_*^2). The exact nonexpanding linear instability
band was obtained in [LINEAR_BAND.md](LINEAR_BAND.md). Set the initial epoch
to z=1e6 and use inherited normalization omega_c=0.120, h=0.6736 and an
illustrative radiation density Omega_r=9.2e-5. These are inputs, not a new
fit to cosmological data.

For a source energy density chosen equal to that cold rest-energy density
scaled to the initial epoch, the numbers are

| Input or consequence | Value |
|---|---:|
| source energy density | 9.7151062e6 eV^4 |
| H in energy units | 1.3781995e-23 eV |
| symmetry-breaking field scale f | 2.2039846e22 eV |
| quartic lambda | 4.1173075e-69 |
| H/(m epsilon) | 1.3781995e-4 |

Here f=sqrt(2 rho_source)/(M epsilon) uses the harmonic source-energy
relation, and lambda=M^2/(2f^2). The exact initial potential energy differs
by the factor (1+epsilon/2)^2. **The abundance has been supplied as source
energy; none of these equations predicts it.** The masses, splitting and
source preparation remain independent choices. The source is about 0.29%
of the chosen radiation density at this epoch, making radiation domination
a useful approximation, not a self-consistent Friedmann solution.

## Quantum source and pair equations

Use dimensionless time x=m epsilon t and an imposed radiation background
a^2=1+2 h_e x, where h_e=H_initial/(m epsilon). Let B be the coherent source
amplitude divided by its initial amplitude. For each opposite-momentum pair
let n_j be its occupation and kappa_j its anomalous pair expectation.

The numerical variables are F_j=w_j n_j and C_j=w_j kappa_j, where w_j is
the number of physical pair states in a quadrature cell divided by the
initial number of source quanta. This rescaling permits enormous physical
occupations without treating them as dilute.

Parameterize initial physical momenta by p^2/m^2=u_*^2+2 epsilon v. For a
real daughter, unordered pairs have phase-space measure p^2 dp/(4 pi^2).
With source number density n_source=rho_source/M, the quadrature weights are

\[
 w_j=\frac{m^3\epsilon\sqrt{u_*^2+2\epsilon v_j}}
 {4\pi^2 n_{\rm source}}\,\Delta v_j.
\]

The factor one-half relative to the full momentum-space measure avoids
counting the same real-field pair twice. Write s_j^2=u_*^2+2 epsilon v_j,
omega_j/m=sqrt(1+s_j^2/a^2). In the leading rotating-wave and harmonic-source
approximation, define

\[
 \Delta_j=\frac{2(s_j^2/a^2-u_*^2)}
 {\epsilon[\sqrt{1+s_j^2/a^2}+\sqrt{1+u_*^2}]},\qquad
 G_j=\frac{1+u_*^2}{\sqrt{1+s_j^2/a^2}}a^{-3/2}.
\]

The depleted-source Gaussian equations are

\[
 B'=-i\sum_jG_j C_j,\quad
 C_j'=-i\Delta_j C_j-iG_jB(2F_j+w_j),\quad
 F_j'=-2\operatorname{Im}(G_jB^*C_j).
\]

Initial data are B=1, F_j=C_j=0. The term w_j is the spontaneous quantum
source; omitting it would leave the daughters empty. Stimulated production
and reverse transfer are both retained. The source is not a fixed pump.

Direct differentiation proves

\[
 |B|^2+\sum_jF_j=1,\qquad
 F_j(F_j+w_j)-|C_j|^2=0
\]

for exact evolution from these data. The second is the pure Gaussian pair
covariance identity. At huge occupation its evaluation subtracts nearly
equal numbers, so the script reports the relative numerical residual rather
than treating it as a rigorous uncertainty certificate.

The reduced energy and its expansion work satisfy

\[
 E=\sum_j\Delta_jF_j+2\operatorname{Re}
 [B^*\sum_jG_jC_j],\quad
 E'=\sum_j\Delta_j'F_j+2\operatorname{Re}
 [B^*\sum_jG_j'C_j].
\]

The second run integrates this work independently as a state variable. The
energy identity follows algebraically from the moment equations; no bath or
unaccounted damping is added.

## Resolution is a physical check

The initial run uses Gauss-Legendre quadrature with 64, 128 and 256 cells
over v in [-2,2], and a 128-cell wider interval [-3,3], up to x=200.
Although it conserves source-plus-pair number accurately, its late fractions
do not converge: the 128- and 256-cell fractions at x=200 differ by about
0.066. The 64-cell result even disagrees noticeably at x=100. These
differences are retained in [the original output](envelope_run/results.json).
Its 16 passing checks are conservation/positivity checks, not convergence
or a physical-yield verdict.

The follow-up increases to 512 and 1024 cells on [-2,2], and 768 cells on
[-3,3], while adding the explicit work check. Its results are stored in
[the follow-up output](envelope_run_v2/results.json); no original result is
overwritten. All 15 checks pass, and the manifest validates against the
recorded inputs and outputs.

| Cells and interval | Pair fraction at x=100 | Pair fraction at x=200 |
|---|---:|---:|
| 512, [-2,2] | 0.683533122731 | 0.928523045912 |
| 1024, [-2,2] | 0.683533122731 | 0.928523045912 |
| 768, [-3,3] | 0.683533122726 | 0.928523045912 |

The maximum sampled fraction is 0.996666739 near x=79.2. Subsequent reverse
transfer reduces it, so the maximum is not a relic yield. The endpoint
x=200 corresponds to about 15.24 days after the chosen initial epoch, with
a=1.0272. Source-plus-pair conservation residuals stay below 2.6e-9 and
explicit-work residuals below 2.8e-10. Agreement across these quadratures
supports convergence of these sampled fractions in the reduced model;
it does not certify all times, the omitted momentum region, or the full
quantum field theory. These are numerical results, not interval bounds.

At the endpoint the included wider momentum interval has p/m below 0.00124;
its populated modes remain nonrelativistic. This last statement uses the
chosen interval and expansion, not a simulation of every physical mode.

## What this calculation does not include

The momentum interval covers the cold instability band and adjacent modes,
guided by the exact linear calculation. It is not the full continuum:
off-resonant mode elimination, ultraviolet renormalization and its error
bounds have not been derived. The coherent source and Gaussian daughters
omit source fragmentation, higher correlations and quartic rescattering.
The source's contribution to expansion is neglected. Parameters are chosen,
including the initial energy amount. A late cold relic, halo attractor and
the repository's acceleration law do not follow from a transient fraction.

The purpose of increasing momentum resolution is to determine which
production statement survives this model's own numerical limit before
attempting those missing physical steps.

A subsequent [inverse-channel check](INVERSE_CHANNEL.md) shows that the
produced spectrum permits regeneration of moving source particles, which
the homogeneous-source truncation excludes. The channel may redistribute
energy while staying cold; its rate and backreaction have not been computed.
The 0.928523 endpoint fraction must therefore remain a truncation result.
