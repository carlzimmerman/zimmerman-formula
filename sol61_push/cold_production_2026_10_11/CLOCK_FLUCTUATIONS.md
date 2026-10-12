# Linear fluctuations of the autonomous preparation pulse

Status: finite linear mode calculation for the tuned J=10 background in
AUTONOMOUS_CLOCK.md. It finds nonzero amplification and vacuum excitation.
It does not establish nonlinear stability or quantify total contamination of
the cold source. The previous uniform preparation result remains conditional.

## Equations and normalization

Use canonical fluctuations of the source component Y and clock sigma.
In units M=L=1, let v=(delta Y,delta sigma). For a Fourier mode with
k=|physical momentum|/M,

    v'' + [k^2 I + H(t)] v = 0,
    Hyy = 1 + 3 W,
    Hy,sigma = 3 y W'/sqrt(J),
    Hsigma,sigma = (3/2) y^2 W''/J.

The X fluctuation is an uncoupled oscillator and is omitted from this matrix.
W, W' and W'' are evaluated along the backreacting homogeneous clock solution.
For a rising edge, W''=60 z(1-z)(1-2z)/delta^2; the falling edge has the
opposite sign, with its own local z. These expressions were checked against
finite differences of the potential at five interior locations.

The transfer S maps (v,v') from pulse entry to exit and must satisfy
S^T Omega S=Omega. Before and after the pulse the frequencies are
omegaY=sqrt(1+k^2) and omegaSigma=k. For k>0 define
T=diag(sqrt(omegaY),sqrt(omegaSigma),1/sqrt(omegaY),1/sqrt(omegaSigma)).
R=T S T^-1 acts on oscillator-normalized quadratures. For an incoming free
oscillator vacuum, the outgoing occupation of species i is

    n_i = [sum_j R_ij^2 + sum_j R_(i+2),j^2]/4 - 1/2.

This is the linear Gaussian vacuum result on the prescribed classical
background, not a quantum simulation of its backreaction. The largest
singular value of R measures worst-case quadrature amplification. At k=0
the massless clock has no oscillator vacuum; only a classical transfer is
reported, using unit weights for its coordinate and momentum.

## Finite results

| Dimensionless momentum k=p/M | Largest quadrature gain | Source Y occupation | Clock occupation |
|---|---:|---:|---:|
| 0.01 | 2.4472 | 1.02738 | 0.01162 |
| 0.1 | 2.6026 | 1.11764 | 0.11616 |
| 0.3 | 2.8505 | 1.23997 | 0.34627 |
| 1 | 2.8241 | 0.96713 | 0.65934 |
| 3 | 1.5660 | 0.03573 | 0.18644 |
| 10 | 1.1005 | 0.008755 | 0.008736 |
| 30 | 1.0348 | 0.0009832 | 0.0010113 |
| 100 | 1.0202 | 0.00007580 | 0.0003373 |
| 300 | 1.0198 | 0.000001820 | 0.0003814 |

The differently normalized classical zero-mode gain is 4.4886; it should not
be compared directly with the oscillator-normalized nonzero-mode entries.
The sampled minimum eigenvalue of H is about -8660.54, during a narrow edge.
Negative instantaneous curvature permits transient growth but does not alone
prove a large final amplification. The actual finite transfers above include
both edges and the intervening evolution.

The sampled occupation is not identically zero at momenta comparable to and
larger than M. These excitations are not automatically part of the cold
p/m about 0.001 daughter band. Nor does an order-one occupation per mode mean
order-one energy relative to the macroscopic source: the density requires a
momentum integral and the physical mass normalization. The clock occupation
at k=300 exceeds its value at k=100, so even monotone tail suppression has
not been established by this sample.

The result therefore changes the next required check: integrate the produced
energy with controlled momentum resolution and test the high-momentum tail.
Only then can it be compared with the very small initial excess-energy
budget. Primordial classical fluctuations would require their own spectrum
and cannot be inferred from the vacuum calculation.

## Evidence and limitations

`clock_fluctuations.py` reads the pinned tuned J=10 parameters, recomputes the
background at rtol=2e-13, and integrates ten linear modes at rtol=1e-9 and
2e-11. All 113 checks pass. At tighter tolerance the largest symplectic
residual is below 8.2e-11; the largest difference between the two tolerance
runs in the normalized transfer matrix is below 8.1e-7. The manifest
`clock_fluctuations_run/manifest.json` validates the run's inputs and outputs.
This is self-reviewed evidence over the declared finite sample.

No nonlinear spatial evolution, momentum-integrated density, UV convergence,
renormalization, inflaton perturbation spectrum or daughter fluctuations
is covered. The extra clock and source displacement still have supplied
initial conditions. Nothing here establishes the repo's abundance or galaxy
law, and the complete cold-energy formation goal remains open.
