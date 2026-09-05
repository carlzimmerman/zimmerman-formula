# Central tidal consistency relation for the filtered action

Date: 2026-09-04. Status: **analytically derived in linear response and
computationally checked in the stated range; no empirical confirmation or
relativistic closure.** This is a new calculation for the repository's
candidate, not a demonstrated first discovery of a law of nature.

## The useful result

Define H_ij=partial_i partial_j Phi_ph(0), the central Hessian of the
additional potential after subtracting Newtonian baryonic gravity and the
uniform external background. Let

\[
 Q_2=H_\perp-H_\parallel,\qquad
 D=\operatorname{tr}H=4\pi G\rho_{\rm ph}(0).
\]

Here parallel refers to the external field. The physical tidal acceleration
tensor is -H. D is the isotropic central curvature, not the total
phantom mass or the Newtonian point-source singularity.

For the action in `../smoothed_onset_action_2026/REPORT.md`, linearized about
a constant nonzero filtered Newtonian external field s_e a0, the relation is

\[
 \boxed{\frac{Q_2}{D}
 =\frac{2y}{5[3\lambda(y)-y]},\quad
 \lambda(y)=1+(y-1)e^{-y},\quad s_e=y(1-e^{-y}).}
\]

The ratio does not depend on source mass or the shape/length of an
isotropic smoothing filter, under the assumptions below. A spherical finite
source changes the common amplitude but not the ratio. Therefore changing
xi cannot independently tune the two central signals in this regime.
At y=1, Q2/D=1/5. As y tends to zero with source amplitude reduced enough
to preserve external dominance, Q2/D tends to 2/25. This latter number is
a generic deep-MOND limit, not unique to the exponential kernel.

The ratio is undefined where D=0. The correct nonsingular statement is

\[
 \boxed{(15A+5B)Q_2+2BD=0},\quad
 A=\nu(s_e)-1,\quad B=s_e\nu'(s_e).
\]

No phantom observable diverges merely because this ratio has a pole.

## Derivation from the same action

The existing action gives Delta u=4pi G rho and
Delta Phi=Delta u+S* div f(grad S u), where f(p)=[nu(|p|/a0)-1]p.
Varying the nonlinear flux about p_e=a0 s_e ehat gives the Jacobian

\[
 B_{ij}^{\rm flux}=A\delta_{ij}+B e_i e_j.
\]

For a normalized self-adjoint isotropic filter with Fourier multiplier
sigma(k), the additional potential of a point-source perturbation is

\[
 \widehat{\Phi}_{\rm ph}(\mathbf k)=
 -\frac{4\pi GM}{k^2}|\sigma(k)|^2
 [A+B(\hat{\mathbf k}\cdot\hat{\mathbf e})^2].
\]

Fourier convention: inverse transform integrates d^3k/(2pi)^3. The second
filter is the adjoint required by the action; it is not optional.
Differentiate twice before evaluating at the center. Angular integration
uses <n_i n_j>=delta_ij/3 and
<n_i n_j(n dot e)^2>=(delta_ij+2e_i e_j)/15. Hence

\[
 H_{ij}=\frac{4\pi GM I}{15}[(5A+B)\delta_{ij}+2B e_i e_j],
 \qquad I=\int\frac{d^3k}{(2\pi)^3}|\sigma(k)|^2.
\]

Gaussian sigma=exp(-xi^2 k^2/2) gives I=1/(8pi^(3/2)xi^3).
Helmholtz sigma=1/(1+xi^2 k^2) gives I=1/(8pi xi^3).
Their amplitudes differ, but I cancels from Q2/D. For the exact exponential
inverse law, A=exp(-y)/mu and B=-y exp(-y)/(mu lambda); substitution gives
the boxed relation. SymPy verifies the coefficients, identity and deep limit.

For finite spherical density replace MI by
J_rho=integral rho_hat(k)|sigma(k)|^2 d^3k/(2pi)^3. The angular argument is
unchanged when this converges. Positivity of J_rho is not guaranteed for
every real isotropic filter and every nonnegative density; it is secure
for the Gaussian/Helmholtz nonnegative convolution kernels. The computed
finite-source controls are Gaussian densities with nonnegative transforms.

## A related qualitative prediction

For positive point-source mass and the stated filters, the additional
parallel Hessian changes sign at y=1.8907779792, while the trace vanishes
at y=3.2602387018 and the perpendicular Hessian at y=5.1228414320.
These values are numerically solved from 3y=5lambda, y=3lambda and
y=5lambda, respectively, not inserted as expected outcomes.

Thus a range exists with a stretching additional tide along the background
field and a compressing additional tide across it. This concerns the small
additional tidal component, not a claim that total gravity becomes repulsive.
y is an inverse-kernel parameter; it is not automatically the measured
physical ambient acceleration divided by a0.

## Verification and limits

The script integrates the full directional Hessian, rather than assigning
its ratio. It covers 324 cases: six background values, three filters,
three widths, three Gaussian source radii, and two axis orientations.
The rational quartic filter is an algebraic control, not a claimed healthy
covariant completion. Maximum normalized identity residual is 1.10e-14;
the independently integrated Hessian differs from the analytical tensor
by at most 1.99e-14. These are numerical agreement measures, not empirical
errors or certified continuum error bounds.

Controls include direct finite differences of the exact nonlinear flux,
known Gaussian/Helmholtz radial integrals, increased angular resolution,
the trace-zero case and a deliberately anisotropic spectral weight.
The anisotropic control violates the relation by about 0.0667 under the
specified normalized residual, demonstrating why isotropy is necessary.

Required assumptions: linear response in source amplitude, a spatially
constant nonzero constitutive background, spherical source, isotropic
filter, convergent integral and the stated fixed boundary prescription.
For physical application require the filtered source gradient to remain
small compared with the ambient gradient over the response region. A
filter must have unit DC gain and a defined action on affine potentials
to identify that background with the unfiltered Newtonian external field.

This calculation is not the nonlinear Solar-System quadrupole. It does
not clear Cassini, identify an observed test system, derive PPN parameters,
show Phi=Psi, or complete a metric action. Both central components can
become small together as xi grows, so their ratio alone is not an
unconditional empirical exclusion. At exactly zero background the
linearization is singular; the isolated sixth-power result is a different
limit. Nonspherical sources can destroy the common angular factor.

## Prior art: what is and is not new

The external-field operator is known. Banik and Zhao,
*The External Field Dominated Solution In QUMOND & AQUAL: Application To
Tidal Streams*, [arXiv:1509.08457v2](https://arxiv.org/pdf/1509.08457v2),
4 May 2018 revision, equation (24), gives the unfiltered operator with
K0=d ln nu/d ln s. Our B=nu K0 and A=nu-1 subtracts ordinary Newtonian
gravity. Their real-space anisotropic point-source solution is not itself
our regularized central Hessian.

Milgrom's [QUMOND paper, arXiv:0911.5464v2](https://arxiv.org/pdf/0911.5464v2),
2 March 2010, equations (57)-(63), already supplies external-field
monopole/anisotropy relations. The repository's k03_efe_phantom_theorem.py
also contains the environment-dependent total mass/flux relation, using
a different RAR kernel. None of those statements should be rebranded as
new. Our central filtered identity is a formal corollary of the known
linear response combined with isotropic regularization and angular averages.

A bounded English-language web and repository search on 2026-09-04 used
`MOND external field Gaussian smoothing central tidal tensor quadrupole density universal ratio`,
`QUMOND external field tidal tensor phantom density central quadrupole interpolation derivative`,
and `MOND external field "quadrupole" "central density"`.
The specific central filtered formula was not identified in the inspected
passages, but that is not a priority proof. No global novelty claim is made.
Source PDFs were inspected through the web reader, not retained locally.

### Paper-stage prior-art and notation correction

The subsequent paper check identified an important architectural antecedent:
Milgrom, *Generalizations of quasilinear MOND (QUMOND)*,
[arXiv:2305.01589v2](https://arxiv.org/pdf/2305.01589v2), section II.B,
explicitly permits possibly nonlocal functionals of the Newtonian potential.
Our action is a specialization with
P[u]=|grad u|^2/a0^2+q(|grad S u|^2/a0^2), not a new action architecture.
The finite-derivative examples in that paper also investigate extra scales
and screening. The bounded novelty claim is only the central-response
corollary; priority remains unverified.

Our Q2 has the same sign and normalization as the traceless coefficient in
[Hees et al., arXiv:1402.6950v2](https://arxiv.org/pdf/1402.6950v2), equation (6).
The local anomalous potential here also contains D r^2/6, so matching that
notation does not license importing a pure-quadrupole Cassini fit. The phrase
"spherical/harmonic response" formerly used above was corrected to
"isotropic central curvature": a nonzero trace is not Laplace-harmonic.

The six-page paper and its commands/source audit are in `paper/`.
The paper-stage rerun additionally includes the ten parent-action tests,
for 24 distinct tests total (6 tidal + 10 parent + 6 exact-mu + 2 elliptic),
all exit 0. No physical model code was changed for the paper.

## Reproduction

New files only: CONTRACT.md, REPORT.md, tidal_relation.py,
test_tidal_relation.py, results.json, computation_manifest.json.
No existing theory code or roadmap is modified; this study is not committed.

| Command from repository root | Outcome |
|---|---|
| `python3 qwen_claude_field_theory/closure_2026/filtered_tidal_relation_2026/tidal_relation.py` | 0; all six finite check groups pass |
| `python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/filtered_tidal_relation_2026 -v` | 0; six tests pass, including executable output generation |
| `python3 qwen_claude_field_theory/closure_2026/filtered_tidal_relation_2026/test_tidal_relation.py -q` | 0; six tests pass through the direct runner |
| `python3 -m unittest discover -s hunt_2026/exact_mu_cassini_2026 -q` | 0; six existing tests pass |
| `python3 qwen_claude_field_theory/closure_2026/elliptic_phantom_action_gate_2026/test_elliptic_phantom_action_gate_2026.py` | 0; two existing tests pass |
| `python3 <home>/.codex/plugins/cache/openai-curated-remote/mathbox/2.2.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/filtered_tidal_relation_2026/computation_manifest.json` | 0; manifest valid |

Development failures are retained as history, not physics failures: five
test-first failures before implementation (exit 1); a CLI NumPy-boolean
serialization failure and reproducing regression test (exit 1); an initial
manifest validation failed because the CLI had not yet produced its file.
Normalizing flags to Python booleans fixed the serialization, with no
physical tolerance changes. The manifest records sources, versions, bounds,
commit, dirty state and the results checksum.

An independent read-only reviewer checked the implementation, tests and
contract and found no critical or important issue. The derivation was also
independently checked before implementation. The report received a notation,
dimension and scope self-review; no full empirical or covariant review is implied.

Next decisive work: evaluate corrections to this relation with the fully
nonlinear external-field solve of the same action, then determine whether
both anomalous tidal components are observationally identifiable. The
point of the relation is that smoothing parameters cannot fit them
independently once the stated linear regime is established.
