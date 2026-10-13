# Full loading fluctuations and clock-speed sensitivity

Status: seven finite linear modes and four homogeneous perturbations have
been checked for the R=100 loading history. The corrected calculation passes
115 checks. It shows finite excitation and a demanding clock-speed tolerance;
it does not establish nonlinear stability or a generic attractor.

## Canonical perturbation equations

Use the source/clock potential of CLOCK_LOADING.md and canonical perturbations
v=(delta X,delta Y,delta sigma), with sigma=sqrt(J)L s and units M=L=1.
For k=p/M, v''+(k^2 I+H)v=0, where

    Hxx = 1, Hxy = 0, Hyy = 1+3W,
    Hx,sigma = -f'/sqrt(J),
    Hy,sigma = (-f'+3yW')/sqrt(J),
    Hsigma,sigma = [2 f'^2-(x+y-2f)f''+(3/2)y^2 W'']/J.

The symmetric counterparts complete H. This Hessian includes the loading
force, sharp release, and clock backreaction along the homogeneous solution.
The previous two-field pulse Hessian did not include these terms.

While W=0, the antisymmetric source direction (1,-1,0)/sqrt(2) is an exact
eigenvector with eigenvalue 1, including during release. Thus a pre-existing
source difference obeys delta(X-Y)''+(1+k^2)delta(X-Y)=0. It is not damped.
Starting both components at zero selects the symmetric solution, but the
loading force is not an attractor for arbitrary unequal initial components.

## Finite mode results

The 6-by-6 transfer maps canonical coordinates and momenta. At k>0 use the
incoming/outgoing free oscillator frequencies (sqrt(1+k^2),sqrt(1+k^2),k).
Occupations are computed directly from Bogoliubov beta blocks, avoiding
subtraction of the vacuum half. They refer to the three real fluctuation
oscillators, not a measured daughter yield or a momentum-integrated density.

| k=p/M | Largest normalized quadrature gain | nX | nY | nClock |
|---|---:|---:|---:|---:|
| 0.001 | 14.8641 | 20.8324 | 22.7562 | 50.9209 |
| 0.01 | 5.7204 | 2.0830 | 4.0204 | 5.1190 |
| 0.1 | 3.6404 | 0.2073 | 2.2550 | 0.7041 |
| 1 | 3.3275 | 0.01473 | 1.37160 | 1.03835 |
| 10 | 1.1733 | 0.0002073 | 0.0098806 | 0.0204133 |
| 30 | 1.1071 | 0.00002314 | 0.0011052 | 0.0094147 |

At k=0 the classical transfer gain in unit phase-space weights is 92.9478.
The massless clock has no zero-mode oscillator vacuum. The differently
normalized zero-mode gain must not be compared directly to the other rows;
even free clock displacement drifts with initial velocity over the long
loading duration. A large transfer norm alone is not proof of exponential
instability.

These sampled modes establish excitation in the full loading history. They
do not establish its integrated energy. The previous isolated-pulse energy
and tail bounds do not apply unchanged to the new sharp release.

## Clock speed tolerance

Let epsilon be a fractional change in the initial clock speed, holding the
potential, initial source data and tuned pulse width fixed. The k=0 transfer
predicts the first-order final circular residual

    r = (x'-y, y'+x),
    delta r = B S e_pClock sqrt(12) epsilon,
    B = [[0,-1,0,1,0,0], [1,0,0,0,1,0]].

Here S is the canonical zero-mode transfer, with coordinates ordered
(x,y,sigma,x',y',sigma'). Since Echi-Q/2=|r|^2/2 in these units,

    eta approximately eta_ideal + 32.40157 epsilon^2,
    eta_ideal = 4.99999625e-7.

The finite tuned residual is negligible at the tested perturbation sizes.
The predicted one-parameter tolerance for eta<1e-5 is
|epsilon| approximately below 0.00054148, or 0.05415 percent. This is a
local quadratic estimate, not a certified uniform tolerance or observational
constraint. It applies at preparation; it does not include later expansion.

Independent nonlinear homogeneous integrations, with no retuning, give:

| Fractional speed change | Final eta |
|---|---:|
| -0.001 | 3.30350e-5 |
| -0.0001 | 8.24149e-7 |
| +0.0001 | 8.23881e-7 |
| +0.001 | 3.27661e-5 |

The smaller perturbations agree with the tangent prediction within 0.05
percent of the excess above eta_ideal. This supports the local sensitivity
calculation. Other initial errors and spatial gradients require additional
analysis; a global width adjustment cannot automatically correct different
clock speeds in different regions.

## Numerical failure, correction and provenance

The original `loading_fluctuations.py` run is preserved. Its first calculation
failed three convergence checks and one mode integration. Energy conservation
or a small symplectic residual alone did not validate its transfers. The sharp
release lasts about 1e-4 natural time units after an approximately 91-unit
loading interval, making absolute-time evaluation sensitive to cancellation.

`loading_fluctuations_v2.py` restarts the independent time coordinate at zero
on each segment, resets the located crossing coordinate to its exact declared
edge, and integrates modes at relative tolerances 2e-11 and 5e-13. It rejects
an unsuccessful integrator result instead of carrying that partial transfer
forward. The physical equations, tuned width and convergence acceptance
threshold are unchanged.

The corrected run passes all 115 checks. The maximum difference between its
two normalized transfer matrices is below 2.3e-6, and tighter-run symplectic
residuals are below 7.6e-11. Its manifest is
`loading_fluctuations_run_v2/manifest.json` and validates. These diagnostics
support the finite results, not arbitrary precision or nonlinear validity.
All interpretation remains self-reviewed.

The formation route now has a quantitative initial-condition requirement.
It remains a tuned conservative preparation model with supplied clock energy
and coupling scales. Full-chain quantum energy, primordial perturbations,
cosmological abundance and the repo's halo/acceleration selection remain open.
