# Conditional bound on the direct daughter self-interaction shift

2026-10-11. This is an analytic consistency screen for the retained Gaussian
modes in [ENVELOPE.md](ENVELOPE.md), not a full-field error estimate.

Let n_j and kappa_j denote occupation and anomalous pair covariance, with
|kappa_j|^2=n_j(n_j+1). The elementary inequality
sqrt(n(n+1)) <= n+1/2 follows by squaring: the difference is 1/4.
For a real daughter, counting each opposite-momentum pair once, its
vacuum-subtracted equal-point variance satisfies

\[
 |\sigma|=|\langle Y^2\rangle_{\rm sub}|
 \le {2n_{s,0}\over a^3}\sum_j{w_j\over\omega_j}
 (n_j+|\kappa_j|)
 \le {n_{s,0}\over m a^3}(4F+W),
\]

where F=sum_j w_j n_j, W=sum_j w_j, and n_s,0=rho_source/M.
The factor two is the two real-field momentum modes per pair. The anomalous
variance can oscillate and the subtracted variance need not be positive;
the absolute-value bound allows both. The conserved number combination
|B|^2+F=1 and positivity give 0<=F<=1. Thus this bound is uniform in time
within the stipulated Gaussian equations when a>=1.

In those equations rho_source=M^2 f^2 epsilon^2/2 and lambda=M^2/(2f^2).
Writing R=M/m gives

\[
 {|\sigma|\over f^2}\le 2R\epsilon^2(1+W/4)a^{-3},\qquad
 {3\lambda|\sigma|\over m^2}\le
 3R^3\epsilon^2(1+W/4)a^{-3}.
\]

The daughter equation has the direct Hartree term 3 lambda sigma Y from
lambda Y^3. Its instantaneous mass-squared correction therefore obeys the
second bound. This includes the possible magnitude of anomalous variance;
it does not average that variance away.

For the benchmark, W<=3.079e-66. At a=1 the bounds are:

| Quantity | Upper bound |
|---|---:|
| absolute variance / f^2 | 4.0000020e-14 |
| direct Hartree mass-squared shift / m^2 | 2.4000036e-13 |
| leading pair detuning shift / (m epsilon) | 2.4000036e-6 |
| integral of this leading detuning bound through x=200 | 4.8000072e-4 |

For the detuning estimate, expand 2 sqrt(omega^2+delta m^2): the leading
change is delta m^2/omega, with omega>=m. The omitted relative correction
is of order |delta m^2|/m^2, below 3e-13 here. The tabulated detuning and
phase numbers are bounds on the leading frequency correction, not a bound
on the difference between two nonlinear solutions. One could multiply by
1/sqrt(1-2.4000036e-13) to make the frequency inequality exact for all
allowed signed shifts. The integrated number also drops the a^-3 decay
and is deliberately conservative.

The variance force on the radial background contains resonant components.
Those already drive source depletion in the envelope equations; replacing
the entire radial response by a static displacement would double count or
remove that process. We have not made that replacement here.

## Verification and limits

[hartree_bound.py](hartree_bound.py) checks the direct and simplified formulas
and evaluates the bounds from the recorded benchmark. Its nine finite
checks pass; [results](hartree_bound_run/results.json) and
[manifest](hartree_bound_run/manifest.json) preserve the calculation.
The inequality above supplies the all-occupation argument; finite numerical
samples alone do not. This is self-review, not an independent proof audit.

The bound is conditional on the retained-mode Gaussian covariance and source
number conservation. It excludes vacuum contributions outside this interval,
which require a renormalized field calculation. It also excludes source
fluctuations, higher correlations, scattering into other modes, and changes
in the source spectrum. In an unstable dynamical system, a small coefficient
perturbation need not imply a comparably small population error.

**Decision:** direct daughter Hartree detuning is parametrically small at
this chosen weak-amplitude benchmark, even at full conversion. This removes
one obvious reason to reject the approximation. It does not validate the
whole production history or establish a permanent cold relic. The next
load-bearing missing calculation is the coupled response, including radial
fluctuations and scattering, or a controlled bound on those effects over
the production interval.
