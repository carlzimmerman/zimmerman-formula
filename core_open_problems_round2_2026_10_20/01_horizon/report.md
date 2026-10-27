# Horizon normalization, Round2 checkpoint

**Kappa=1/2 remains unproved.** Two explicit force calculations sharpen the
gap. A Gaussian oscillator coupled to the conformal de Sitter field has
acceleration-dependent noise but acceleration-independent linear mean
response. A gapless nodal-ring Hamiltonian does produce the required local
quadratic deep-field force, but fails the next coefficient of the saturation
law and retains independent source and vacuum-energy parameters.

Checkpoint **HORIZON-R2-2026-10-20**. Frozen predecessor publication:
`8aa3f7046a7ae14a99f3515fd42df5bf061fb1db`. Owner: horizon_normalization.
The main checkout's moving HEAD is not the research ancestry. Exact predecessor
copies and byte hashes are in `frozen_inputs/`. No other agents' Round2 work was
consulted. All writes are confined to this directory. Review is analytical
self-review plus independently formulated quadratures and symbolic checks;
it is not an independent referee certificate.

## The target retained

With K=4 pi G and energy density epsilon_DE=rho_DE c^2,

\[
a_0=\kappa\sqrt{G\epsilon_{\rm DE}},\qquad
a_H=cH_\Lambda,\qquad a_0/a_H=\kappa\sqrt{3/(8\pi)}.
\]

Kappa=1/2 means a0/aH=0.172747, not 0.086374. The smaller fraction is the
**baryonic** acceleration gN=a0/2 at CFG695 half saturation, or the separate
ambient parameter A=a0/2 in the temperature-excess construction. This round
does not interchange those two meanings.

Success would require one independently specified microscopic model to fix its
force observable, critical response, and relation to gravitating vacuum energy.
Matching a power or assigning a vacuum offset is partial progress.

## 1. In-in mechanical response: noise is not mean force

The action contains an actual driven coordinate,

\[
S_Q=\int d\tau\,[M(\dot Q^2-\Omega_b^2Q^2)/2+JQ+\lambda Q\phi(z)],
\]

with a free massless conformal scalar, conformal de Sitter vacuum, and prescribed
stationary accelerated worldline. The observable is delta<Q>/delta J, not an
unspecified conversion of temperature into acceleration. The exact spectral
subtraction of the frozen Wightman function gives, in hbar=c=kB=1,

\[
\rho_\phi(\omega)=\frac{\omega}{2\pi},\qquad
N_\phi(\omega)=\frac{\omega}{4\pi}\coth(\pi\omega/\alpha),
\quad \alpha=\sqrt{H^2+a^2}.
\]

The Gaussian influence action therefore yields, with a common local
renormalization,

\[
\chi_R(\omega)=
\frac1{M(\Omega_R^2-\omega^2)-i\lambda^2\omega/(4\pi)}.
\]

The cycle-averaged mechanical work for a unit sinusoidal source is
omega Im(chi_R)/2. It is independent of alpha. A separate convergent dispersion
integral gives GR(i nu)-GR(0)=-nu/(4 pi), checking the retarded part without
assuming the oscillator equation. The Minkowski damping normalization agrees
with [Lin–Hu, equations (4) and (7)](https://arxiv.org/pdf/gr-qc/0610024v1);
the de Sitter extension here follows from the explicit commutator calculation.

For M=1, Omega_R=1.3, lambda=0.7 and source frequency 0.4:

| alpha | Mean work rate | Stationary variance of Q |
|---:|---:|---:|
| 0.2 | 0.001332441684 | 0.381000506827 |
| 1 | 0.001332441684 | 0.381628330573 |
| 5 | 0.001332441684 | 0.570681980761 |

These are illustrative dimensionless parameters. They distinguish the mean
force observable from its noise; neither column selects a universal a0.
The conclusion is limited to this linear internal-coordinate response.
Varying the trajectory to obtain a center-of-mass self-force, nonlinear
detectors, other fields and finite-size couplings are different problems.
Worldline curvature/acceleration operators can also introduce new coefficients.
The broader horizon-response route stays open.

## 2. Gapless medium: correct leading power, wrong full law

Use the historical nodal Hamiltonian, now coupled to canonically normalized
physical P through P dot grad Phi. The explicit four-by-four Clifford matrices,
action, degeneracies and SI dimensions are in `raw_derivation.md`. Its energies
are +/-sqrt(q1^2+q2^2+h^2P^2), its occupied negative-band degeneracy is N, and

\[
A=\frac{Nm_*}{2\pi v\hbar^3},\quad \Delta=hP,\quad
\epsilon_f(P)=-\frac A3[(\Lambda^2+h^2P^2)^{3/2}-h^3P^3].
\]

The cutoff is a full energy tube of radius Lambda below p0^2/(2m*), at zero
temperature and chemical potential. Add C0+b2 P^2/2. Critical susceptibility
requires **b2=K+A h^2 Lambda**, which remains a tuning. With it the source
equations are exactly

\[
g_N=R(P)=A h^2P[\Lambda-\sqrt{\Lambda^2+h^2P^2}+hP],
\qquad g=KP+R(P).
\]

This establishes a concrete local force map. It gives

\[
\boxed{a_0=K^2/(A h^3)},\qquad
g_N=\frac{g^2}{a_0}
-\left[\frac2{a_0^2}+\frac{A h^4}{2\Lambda K^3}\right]g^3+O(g^4).
\]

**The next coefficient already disagrees with CFG695**, whose cubic term is
-g^3/a0^2. Positive parameters cannot repair it within this bare-quadratic
model. A new potential term d4 P^4/4 can repair that coefficient only by
choosing d4=(A h^3)^2/K+A h^4/(2 Lambda); it is an additional matching input.

The exact regulated force has R>0 and R'>0, but no bounded polarization:
u=KP tends to infinity. At formally large gap it approaches a linear law with
gN/g tending to A h^2 Lambda/(K+A h^2 Lambda). This high-gap statement is about
the fixed-cutoff model, not unknown microscopic bands. The low-field mismatch
does not require extrapolation above the cutoff.

The gravitational source P dot grad Phi has been specified, not derived from
the fermion Hamiltonian. Its normalization makes h a physical free portal.
The historical nonlocal spatial and anisotropy obstructions still apply:
the homogeneous determinant alone is not a galaxy solution. In particular,
P~B/r requires hB>>hbar v for the local gapped approximation; larger radius
does not automatically establish that inequality.

## 3. The same determinant at finite temperature and with gravity

Directly differentiating its finite-temperature free energy gives two distinct
outcomes. Keeping the zero-temperature tuning leaves a positive linear residual:

\[
g_N/P\longrightarrow A h^2[\Lambda-2T\log\cosh(\Lambda/(2T))].
\]

Retuning the quadratic term at each positive T instead gives

\[
g_N=A h^4\left[\frac1{4T}-\frac{\tanh(\Lambda/(2T))}{2\Lambda}\right]P^3+O(P^5).
\]

Thus finite equilibrium temperature does not retain the quadratic asymptote.
Thermal rounding was known in the predecessor; this calculation retains the
same finite cutoff and distinguishes the two tuning choices. A nodal medium
is not automatically in the relativistic de Sitter KMS state. If such
equilibration were established, the thermal crossover would still depend on
the independent portal c h/(hbar K).

The zero-field energy from the same regulator is
epsilon_vac=C0-A Lambda^3/3. Even provisionally granting a covariant dark-energy
completion, for **any** positive desired kappa_* the choice

\[
C_0=\frac{A\Lambda^3}3+\frac{K^4}{A^2h^6G\kappa_*^2}
\]

leaves every P-dependent response unchanged and gives that kappa_*. Fixing the
observed vacuum energy instead leaves h free and hence a0 free. Susceptibility,
deep coefficient and constant energy have independent parameter directions,
demonstrated by a nonzero Jacobian in the raw derivation. These are different
cosmological solutions, not identical metrics with different labels.

This is the established vacuum-zero-mode obstruction exhibited inside one
regulated microscopic candidate. It is not a new impossibility theorem. Also,
a preferred-frame band cutoff by itself supplies neither a covariant stress
tensor nor w=-1; equating its energy with dark energy is an additional gap.

## Evidence and reproducibility

`run_002/manifest.json` records a completed bounded run, **156 checks**, 60-digit
numerical arithmetic, and current input/output hashes. The validator passed
with the repository root. The script uses no repository imports or external
data. It checks Clifford algebra and degeneracy, spectral identities and a
separate dispersion integral, energy/force quadratures, inverse-series matching,
finite-temperature derivatives and the independent constant deformation.
The exact grids and tolerances are in the contract and results. Finite samples
support implementation; the uniform deductions are the explicit analytical
steps, not the number of checks.

From repository root with Python >=3.9 and `requirements.txt` installed:

```sh
python3 core_open_problems_round2_2026_10_20/01_horizon/check_round2.py /tmp/horizon-round2-results.json
```

The portable `reproduce.sh` wrapper accepts an output path. No installed Mathbox
runtime or frozen-input path is required for this direct command. Tested
versions: Python 3.9.6, SymPy 1.14.0, mpmath 1.3.0. `artifact_hashes.json` pins
the delivered files. Optional manifest validation with an installed Mathbox:

```sh
python3 "$MATHBOX_AUDIT_DIR/scripts/validate_manifest.py" core_open_problems_round2_2026_10_20/01_horizon/run_002/manifest.json --root .
```

`run_001` is preserved as historical evidence. It completed, but self-review
found that its illustrative counterterm table set both K and G to one despite
K=4 pi G. The analytical formulas and force calculations were unaffected.
The corrected table uses K=1 and G=1/(4 pi), with four added consistency checks;
only run_002 is current evidence for the delivered script.

## Continuation with precise resumption conditions

| Route | Checkpoint disposition | Next discriminating step |
|---|---|---|
| Gaussian conformal detector | This linear internal observable cannot supply the proposed acceleration-dependent mean force | Specify a dynamical worldline/finite-size coupling, vary the in-in action with respect to that worldline, and distinguish mass/local curvature renormalization from a finite observable force. Its parameters and galaxy worldlines must be fixed before testing kappa. |
| Nodal microscopic response | Local nonanalytic term obtained; this regulated bare-quadratic model fails full-law matching and saturation | A proposed ultraviolet or interacting completion must predict, rather than fit, the quartic coefficient above and a bounded capacity; then solve its nonlocal source problem. Existing spatial obstructions cannot be dropped. |
| Vacuum/thermal consistency | Independent constant and susceptibility terms remain; equilibrium finite T rounds the response | Supply a covariant microscopic constraint or Ward identity that forbids the independent constant deformation, and an actual state-selection rule. Test that same constraint against the physical portal and critical tuning. No such identity has been supplied here. |

The open target is the joint source, state and vacuum constraint. Neither
temperature matching nor the local cubic determinant supplies it.
