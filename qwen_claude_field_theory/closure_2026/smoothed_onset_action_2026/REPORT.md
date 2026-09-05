# Action-derived sixth-power onset: a conditional static prediction

## Result and status

The suggested fifth-power onset law is not the result of the natural
filtered action: variation necessarily inserts an outer adjoint filter.
The corrected Gaussian model instead yields

\[
 r_{\rm eq}^{6}\sim\frac{81}{4}\frac{GM\xi^{4}}{a_0},
 \qquad \epsilon=\frac{GM}{a_0\xi^2}\longrightarrow0.
\]

The measured small-mass log slope is 0.166681964, approaching 1/6.
At epsilon=1e-12 the sixth-power ratio differs from unity by 0.00702%;
at epsilon=1e-4 the difference is 3.97%. These are approximation errors,
not observational uncertainties. The exact numerical curve is in results.json.

**Status: OPEN as physics; the stated static construction and finite checks
are verified. Not yet a Kepler-grade empirical law or a novel relativistic
theory.** The exponent is a consequence of smoothing and deep-MOND response,
not a fingerprint unique to the exponential kernel. The full numerical curve
does use that exact kernel. No astronomical data were fitted or tested here.

## One explicit action, varied

Let u be the Newtonian potential, Phi the potential coupled to ordinary
nonrelativistic matter, and S convolution with a normalized isotropic Gaussian
of standard deviation xi. At fixed time, with compactly supported variations
or compatible boundary conditions, take

\[
 I=\int dt\,d^3x\left\{\mathcal L_{m,\rm kin}-\rho\Phi
 -\frac{1}{8\pi G}\left[2\nabla\Phi\cdot\nabla u-|\nabla u|^2
 -a_0^2q\!\left(\frac{|\nabla Su|^2}{a_0^2}\right)\right]\right\}.
\]

Define s=y(1-exp(-y)), nu(s)=y/s, and

\[
 \mathcal G(y)=y^2+2(1+y)e^{-y}-2,\qquad
 q(s^2)=2sy-\mathcal G(y)-s^2.
\]

Differentiation gives q'(s^2)=nu(s)-1. This uses the implicit inverse of
mu(y)=1-exp(-y), not the frequently substituted RAR fitting function.
Writing f(p)=[nu(|p|/a0)-1]p, the field variations give

\[
 \frac{\delta I}{\delta\Phi}=\frac{\Delta u}{4\pi G}-\rho=0,
 \qquad
 \frac{\delta I}{\delta u}=\frac{1}{4\pi G}
 \left[\Delta\Phi-\Delta u-S^*\nabla\cdot f(\nabla Su)\right]=0.
\]

Thus the field equations are

\[
 \boxed{\Delta u=4\pi G\rho,\qquad
 \Delta\Phi=4\pi G\rho+S\nabla\cdot f(\nabla Su).}
\]

The outer S equals S* for these boundary conventions. Removing it is not an
allowed simplification. A finite-difference first variation agrees with the
action equations to relative error below 2e-9 in the tested Gaussian and
Helmholtz examples; the omitted-filter equation differs by about 21.5%.
Matter feels -grad Phi from variation of its particle coordinates. This is
not a derivation of the relativistic matter Ward identity.

Isolated MOND potentials grow logarithmically: variations can be defined on
a finite domain or at fixed asymptotic mass, subtracting the common divergent
energy. No claim of a finite unrenormalized infinite-space action is made.

## Why the one-filter prescription is generally nonreciprocal

Fix the inverse Laplacian T on the nonzero-mode sector, with T=T* and ST=TS.
Linearize away from a zero filtered gradient. The constitutive Jacobian B=Df
is symmetric and A=div B grad is self-adjoint. For the original one-filter
prescription the source-response derivative is

\[
 D_\rho\Phi=4\pi G(T+TAST),\qquad
 D_\rho\Phi-(D_\rho\Phi)^*=4\pi G\,T[A,S]T.
\]

A twice-differentiable reduced stationary action with linear source coupling
-rho Phi has a symmetric second variation. Consequently a nonzero displayed
commutator obstructs that realization. The corrected action gives T+TSAST,
which is symmetric. Uniform constitutive coefficients can commute; the
obstruction concerns inhomogeneous backgrounds, not every special solution.

An explicit continuum perturbation illustrates noncommutation: on periodic
perturbations about a fixed uniform field, take the dimensionless filtered
gradient s0+eta cos(x), where s0=1-exp(-1). The longitudinal tangent is
B=1/[1+(y-1)exp(-y)]-1, and dB/ds at y=1 equals -1/e. Therefore its first
Fourier coefficient is -eta/(2e)+O(eta^2), and

\[
 [A,S]_{2,1}=\frac{\eta}{e}(s_1-s_2)+O(\eta^2)\ne0
\]

for sufficiently small nonzero eta and positive smoothing length, where s_n
now denotes the smoothing multiplier of Fourier mode n (not acceleration).
This is a local signed-source/periodic-perturbation illustration; it is not
a complete theorem restricted to isolated, everywhere-positive baryon sources.

The script additionally computes an exact rational graph commutator and
actual exponential-kernel response matrices on rings of 8, 12 and 20 sites.
One-filter relative antisymmetries range from 0.0499 to 0.1773, while the
action responses are symmetric to below 4.4e-15. These grids are distinct
finite tests, not a continuum mesh-convergence sequence. The Laplacian
constant mode is projected out, with its nullity calculated, not asserted.
No inference about homogeneous cosmological dynamics follows.

## Derivation of the sixth-power relation

For a point source define x=r/xi and

\[
 F(t)=\operatorname{erf}(t/\sqrt2)-\sqrt{2/\pi}\,t e^{-t^2/2},
 \qquad K(t)=(2\pi)^{-3/2}e^{-t^2/2}.
\]

The inner Newtonian field is a0 epsilon F(t)/t^2. The exact inverse law
has phantom response y-s=y exp(-y)=sqrt(s)-3s/4+O(s^(3/2)).
Convolving this radial vector (not its scalar magnitude) once more gives
the regular central gradient

\[
 \frac{g_{\rm ph}}{a_0}
 =\sqrt\epsilon\,x\,\frac{4\pi}{3}
   \int_0^\infty[-K'(t)]t\sqrt{F(t)}\,dt
   +O(\epsilon x)+O(\sqrt\epsilon x^3).
\]

Since K'=-tK and F'=4pi t^2 K, the coefficient is exactly

\[
 \frac13\int_0^1\sqrt F\,dF=\frac29.
\]

Equality with the unsmoothed Newtonian acceleration a0 epsilon/x^2 yields
x_eq^6~81 epsilon/4. The leading relative finite-radius correction is
O(epsilon^(1/3)). Regularity excludes an extra harmonic 1/r phantom term.
For universal fixed xi, 100 times the source mass increases the asymptotic
onset radius by 100^(1/6)=2.15443. Both source extent R << r_eq and
r_eq << xi are required. This is a test-particle field, not a derivation of
the comparable-mass binary force law.

For comparison, the nonvariational one-filter law has the exact spherical
onset equation epsilon=x^2 log(1+F)/(1+F). It gives the previously suggested
fifth power for Gaussian filtering and fourth power for Helmholtz filtering.
Those exponents must not be assigned to the corrected action.

## What this does not solve

- Finite xi changes the original exact AQUAL equation. This model preserves
  the exponential constitutive kernel, not that universal observable equation.
- As xi goes to zero the action reduces to QUMOND; QUMOND and AQUAL agree
  in spherical symmetry, but not for general mass distributions.
- The unsmoothed Newtonian term is retained exactly. The code checks the
  high-field constitutive limit and far-field deep-MOND normalization, not
  Solar-System viability or recovery of a relativistic GR action.
- There is no metric, tensor sector, Dirac count for a covariant theory,
  lensing calculation, PPN derivation, FLRW solution, or stability proof here.
- Spatial Gaussian convolution is nonlocal. Its causal covariant realization
  remains unresolved; elliptic behavior alone is not evidence of health.
- The zero-gradient tangent diverges before outer smoothing. The isolated
  central integral is finite, but that does not certify all perturbations.
- A dominating external field makes the response approximately linear;
  at fixed background the enhancement/source ratio can become independent
  of mass, eliminating this isolated onset exponent.
- Neither a0 nor xi is derived, and xi must not be fitted object by object
  to manufacture the mass law.

A dimensional feasibility check makes the scale limitation concrete. Using
a0=9.3619e-11 m/s^2, G=6.6743e-11 SI, pc=3.085677581491367e16 m and
solar mass=1.98847e30 kg, define M_xi=a0 xi^2/G. At xi=0.05, 0.1 and 84 pc,
M_xi is respectively 1.6791, 6.7165 and 4.7391e6 solar masses. The largest
epsilon in the tested central-asymptote range, 1e-4, therefore corresponds
to masses 0.0001679, 0.0006716 and 473.9 solar masses. In particular the
0.05–0.1 pc proposal does not put galaxies in this sixth-power regime.
This is a unit conversion/feasibility check, not empirical validation.

The next efficient physics calculation is the external-field response of
this same action, including the Solar-System quadrupole; it must precede
claims based on local wide binaries. An empirical test needs isolated
compact systems with onset well inside a single universal xi, independently
estimated baryonic masses, and an observational forward model.

## Prior art and current repository context

Milgrom, *Quasi-linear formulation of MOND*, arXiv:0911.5464v2 (2 March 2010),
equations (3)-(6), gives the unsmoothed two-potential action and its variations:
[primary source](https://arxiv.org/pdf/0911.5464v2), checked 4 September 2026.
Its phi^N is our u, phi is Phi, and Q(z)=z+q(z) at S=identity. This establishes
the known parent structure, not the new filtered action or sixth-power result.
No source document was downloaded into this study. A bounded web search for
`MOND Gaussian smoothing action adjoint sixth power transition radius mass`
did not establish priority; novelty remains unverified.

The inspected f29 display smooths the entire source, while its phantom
quadrature uses the RAR kernel. Neither is identical to this action. The f30
Gaussian/Helmholtz core distinction was already present. New commit
5807a46b9 reports failure of the simple biharmonic AeST screening proposal;
its PPN calculations were not rerun here and do not transfer to this model.

## Reproduction and files

All six study files are new; no pre-existing theory code is changed:
CONTRACT.md, REPORT.md, onset_action_gate.py, test_onset_action_gate.py,
results.json, computation_manifest.json. The manifest records source hashes,
the actual pre-commit HEAD, dirty state, versions, bounds and output hash.

Commands from the repository root and outcomes are recorded below after the
final verification run. Initial test-first run: nine expected failures
(implementation absent), exit 1. The first CLI run and its added regression
test exposed a NumPy boolean JSON-serialization error, exit 1; it was fixed
by normalizing check flags to Python booleans. No physical tolerance was changed.

The initial unittest discovery command on elliptic_phantom_action_gate_2026
found zero tests (exit 0); it is not counted as verification. Pytest is not
installed in this Python environment (import check exit 1), so the existing
test file's own executable runner is used below. Tests exiting 0 do not
certify the full theory.

Final verification (all commands from repository root):

| Command | Exit / result |
|---|---|
| `python3 qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026/onset_action_gate.py` | 0; eight finite assertion groups pass |
| `python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026 -v` | 0; 10 tests, including executable CLI run |
| `python3 qwen_claude_field_theory/closure_2026/elliptic_phantom_action_gate_2026/test_elliptic_phantom_action_gate_2026.py` | 0; 2 existing tests |
| `python3 -m unittest discover -s hunt_2026/exact_mu_cassini_2026 -q` | 0; 6 existing tests |
| `python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.2.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026/computation_manifest.json` | 0; schema valid |
| `git diff --check` | 0 |

All six recorded input/output SHA-256 hashes were independently recomputed
and matched (Python verification exit 0). An independent read-only reviewer
checked the implementation, tests and coefficient, finding no critical or
important issue. Mathematical prose was self-reviewed for notation, signs,
dimensions and limitations. No claim-supporting result relies solely on the
overall script exit code.

The dimensional check was executed with:

```bash
python3 -c 'G=6.6743e-11; a0=9.3619e-11; pc=3.085677581491367e16; solar_mass=1.98847e30; print("xi_pc  M_xi_solar  mass_at_epsilon_1e-4_solar"); [(print(xi,a0*(xi*pc)**2/(G*solar_mass),1e-4*a0*(xi*pc)**2/(G*solar_mass))) for xi in (0.05,0.1,84.0)]'
```

Exit 0. Only this folder is to be committed; unrelated working-tree edits
are deliberately preserved. No push is included in this commit request.
