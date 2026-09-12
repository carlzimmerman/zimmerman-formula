# A constructed current sector with a causal counterflow state and an unstable approach

Starting revision: `5a87447af`, 2026-09-12. This directory is the entire write
scope. Other agents' C003, Fable and Hermes implementations are not edited.

**Result:** an explicit conservative continuum action has a dust-like comoving
limit and a positive-energy, strictly subluminal quadratic counterflow state
in every propagation direction. The same action has a negative transverse
sound-speed squared throughout `0 < v <= 0.1c` at the tested equal proper
densities. The latter is an exact interval obstruction, not a sampling verdict.
This member **fails the required stability gate** and is not a complete gravity
theory. The constructive result and the obstruction are both retained.

Eight Lean theorems certify the displayed algebra, including the all-angle
polynomial root bound and the entire unstable small-velocity interval. They
do not formalize the variational calculus, the whole theory, or empirical truth.

## Explicit action and interpretation

Use signature `(-+++)`, `c=1`, and normalize the currents by a fixed density
unit. In these units define two future timelike field currents `j_A^mu`, two
scalar potentials `theta_A`, and

\[
 n_A=\sqrt{-g_{\mu\nu}j_A^\mu j_A^\nu}>0,\quad
 s=-g_{\mu\nu}j_1^\mu j_2^\nu,\quad R=s-n_1n_2.
\]

Here `R` denotes the relative-current invariant, **not Ricci curvature**.
For future timelike currents `R=n1*n2*(w-1)>=0`, where `w=-u1.u2`.
The prospective additional sector is

\[
 S_J=E_*\int d^4x\sqrt{-g}\left[\sum_{A=1}^2j_A^\mu\partial_\mu\theta_A
                      +F(n_1,n_2,s)\right],
\]
\[
 \boxed{F=-n_1-n_2+\frac{R}{16}
   +\left[\frac52-\frac{(n_1+n_2)^2}{8}
                   -\frac53(n_1-n_2)^2\right]R^2.}
\]

`E_*>0` is an energy-density unit; the potentials can be assigned length units
so the integrand in brackets is dimensionless. The rational coefficients were
chosen by a mathematical health search and rationalized, **not derived from
Carl's acceleration relation or from observations**. No MOND kernel was fit or
changed. This is a possible field sector for a future joint action; it has not
been identified with the existing clock charge or grafted into the background
solver. Adding it to that solver without rederiving the combined action would
double-count an unestablished component.

No microscopic particle decay or stochastic Poisson kick is assumed. These are
continuum fields that can carry gravitating dust-like energy. Their physical
scalar modes are explicitly counted; calling them currents does not make them
auxiliary or establish the requested two-mode gravity theory.

## Variation, stress, and conservation

Let `pi_{A mu}=partial F/partial j_A^mu`. Independent variations give

\[
 \nabla_\mu j_A^\mu=0,\qquad \partial_\mu\theta_A+\pi_{A\mu}=0,
\]
\[
 \pi_{1\mu}=-\frac{F_{n_1}}{n_1}j_{1\mu}-F_sj_{2\mu},\qquad
 \pi_{2\mu}=-\frac{F_{n_2}}{n_2}j_{2\mu}-F_sj_{1\mu}.
\]

The full on-shell integrand, including the current-potential terms, is
`Psi=F-n1*F_n1-n2*F_n2-2*s*F_s`. Hilbert variation yields

\[
 T^\mu{}_{\nu}/E_*=\Psi\delta^\mu{}_{\nu}
                         +\sum_Aj_A^\mu\pi_{A\nu}.
\]

`variation.py` independently compares this formula against all ten symmetric
inverse-metric variations, holding contravariant currents fixed. All residuals
are zero. In particular the current-potential term cannot be dropped before
varying the volume element. The on-shell identity is

\[
 \nabla_\mu T^\mu{}_{\nu}/E_*
 =\sum_A\left[\pi_{A\nu}\nabla_\mu j_A^\mu
       +j_A^\mu(\nabla_\mu\pi_{A\nu}-\nabla_\nu\pi_{A\mu})\right]=0.
\]

Ordinary minimally coupled matter would have its own Ward identity from
`S_m[g,psi]`, without an extra baryon force. This does not yet compute the
combined clock-sector Ward identity or the response of the physical metric.
The current action conserves each charge and total stress; it has no imposed
entropy production or prescribed kick rate.

At exact coflow the interaction and **all its first variations** vanish for
arbitrary positive densities. Its spatial second variation is nonzero. On
FLRW this sector therefore has `P_J=0`, `rho_J=E_*(n1+n2)` and conserved
`a^3*n_A`. It admits the usual expanding dust contribution when coupled to EH,
but that is not a CMB spectrum calculation or a viable full MOND background.

## Canonical calculation and its boundary

On a fixed inertial metric the nonlinear canonical coordinates are the two
potentials and eight currents. The primary constraints are

\[
 p_{\theta_A}-j_A^0=0,\quad p_{j_A^0}=0,\quad p_{j_A^i}=0.
\]

Preserving the six spatial-current momenta generates the six spatial current
Euler equations `partial_i theta_A+F_{j_A^i}=0`. If the six-dimensional spatial
current Hessian `W` is invertible, they determine the spatial currents locally.
Preservation then fixes the remaining multipliers. A zero determinant of `W`
requires a new constraint analysis and is not passed over by this statement.

The executable builds the **actual canonical Poisson matrix** from the
quadratic action, including both real Fourier quadratures at nonzero k and
all mixed density/current Hessian entries. It computes its rank, determinant,
constraint nullspace, and multiplier solution, and checks the entire
preservation residual on that nullspace.

| Background | Sector | Phase dimension | Primary / secondary | PB rank | First / second class | Canonical pairs |
|---|---:|---:|---:|---:|---:|---:|
| Coflow | k=0 | 20 | 10 / 6 | 16 | 0 / 16 | 2 |
| Coflow | k=1, two real quadratures | 40 | 20 / 12 | 32 | 0 / 32 | 4 |
| Counterflow v=3/5 | k=0 | 20 | 10 / 6 | 16 | 0 / 16 | 2 |
| Counterflow v=3/5 | k=1, two real quadratures | 40 | 20 / 12 | 32 | 0 / 32 | 4 |

The four pairs in the sine/cosine representation mean two field modes, with
two quadratures each. All stabilization residuals vanish and all multipliers
are fixed. This is a **current-sector calculation**. It is not the complete
metric-clock-current nonlinear Dirac algebra, and cannot certify `N_grav=2`.
Global constant shifts of `theta_A` are global symmetries, not local gauge
constraints removing these zero-mode canonical pairs.

## Constructive all-angle state

At `n1=n2=1`, `u1=(5/4,3/4,0,0)` and `u2=(5/4,-3/4,0,0)`, calculate
`H_AB=partial^2 F/partial j_A partial j_B`. Its computed block eigenvalues are:

- Temporal block: `-9/128`, `-14607/2048`.
- Spatial block: `4401/128`, `6017/2048`, `1377/128` twice, `209/128` twice.

Thus the temporal block is negative definite and the spatial block is positive
definite. Their Schur complements give positive reduced scalar kinetic energy
and positive spatial energy. In detail, eliminating the algebraic currents
gives

\[
 L^{(2)}_{\rm red}=-\tfrac12(\partial\delta\theta)^T H^{-1}
                                         (\partial\delta\theta).
\]

Both the two-by-two temporal kinetic block `-(H^-1)_tt` and the six-by-six
spatial energy block `(H^-1)_jj` are positive definite. The mixed block shifts
canonical momenta; completing the square preserves positive Hamiltonian
energy. This assertion is about the two irrotational modes of this action.
It is not a theorem for unrestricted vortical two-fluid models.

Set `t=cos(angle)^2` and `u=(omega/|k|)^2`. Axial symmetry covers every wave
direction. Direct current elimination gives, up to a nonzero factor,

\[
 \boxed{2851101297u^2+(1613336721t-3790090569)u
       +637297632t^2-1820247721t+1197104272=0.}
\]

For every `0<=t<=1`, the discriminant is strictly positive and both roots
satisfy **`0<u<1`**. The proof uses exact positive Bernstein coefficients of
the constant coefficient, discriminant and value at `u=1`, together with the
sign of the linear coefficient and positive derivative at `u=1`. This is an
all-angle phase-speed result, supported by positive quadratic energy. A full
nonlinear causal domain and its invariant evolution have not been proved.

`CounterflowCone.lean` proves those polynomial statements. The unit tests
compare the Lean polynomial with the polynomial actually derived from `F`.
The 101-direction numerical table is a cross-check, not the all-angle proof.

## Immediately following gate: the same-action path

At equal proper densities, the symmetric transverse mode has the exact speed

\[
 c_{\perp,+}^2(v)=
 \frac{v^2(717v^6-1753v^4+235v^2+1)}
 {(3v^4-2v^2+1)(239v^4-374v^2-9)},\qquad
 \lim_{v\to0^+}\frac{c_{\perp,+}^2}{v^2}=-\frac19.
\]

Lean proves this rational expression is **negative for every `0<v<=1/10`**.
The script derives the expression directly from `H^-1`, and a test links it
to the formalized formula. At `v=1/1000`,

\[
 c_{\perp,+}^2=-\frac{1000234998247000717}{9000355999040001599999283}
              \simeq-1.1113282612\,10^{-7}.
\]

The reduced kinetic matrix also has a negative eigenvalue there. The spatial
current Hessian is nonsingular at this witness, so the bad mode has not been
removed by the primary/secondary constraints. A healthy state at `0.6c` cannot
therefore be promoted to a viable galaxy model or a smooth healthy history.
The coflow point itself is degenerate in the density kinetic reduction and
must be treated by the canonical calculation above, not by inverting its
singular full current Hessian. Caustics and strong coupling are unresolved.

The next construction should repair this small-relative-velocity principal
symbol while preserving the comoving dust limit. Removing the linear
entrainment term, or supplying a dynamically derived compressibility, changes
that leading-order problem. Either requires rederiving the action and its
principal symbol; selecting another large-velocity healthy point does not.

## Attribution, prior work, and corrections to the handoff

Carl Zimmerman's insistence on conserved field/clock energy, no new
dark-matter particle, and a derived redistribution mechanism motivates the
calculation. The explicit polynomial witness and audit were constructed here;
its coefficients and any empirical novelty remain unestablished.

Variational current master functions and two-stream instabilities are existing
research, not a newly invented architecture. Relevant primary references are
[Samuelsson et al., Relativistic Two-stream Instability (2009)](https://arxiv.org/abs/0906.4002)
and [Andersson and Comer, Relativistic fluid dynamics (2020)](https://arxiv.org/abs/2008.12069).
Only the source abstracts were checked for attribution; none of their theorems
is imported as a proof dependency for the computations here. This is not an
exhaustive novelty search. In particular the scalar-potential restriction here
does not represent every vortical mode of their general fluid systems.

Two prior handoff claims need qualification:

1. The stored L191 result had a different parameter grid/schema from its current
   source. Its numbers in the previous chat answer are not current verified
   orbit evidence. No L191 physical result is used in this construction.
2. Specifying functions of a varied clock scalar, such as `U(tau)`, can already
   define a covariant action. Such functions need not become new fields. Their
   origin and predictive content are separate questions from covariance.

No new empirical prediction follows from this checkpoint. In particular it
does not establish MOND, lensing, acceptable PPN, CMB viability, halo depletion,
the acceleration-scale relation, or the full coupled gravitational mode count.
The full research objective remains open.

## Reproduction and verification

Run from the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/entrained_current_construction_2026/current_action.py --result /tmp/entrained_current_result.json
python3 -B qwen_claude_field_theory/closure_2026/entrained_current_construction_2026/variation.py
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/entrained_current_construction_2026 -p 'test_current_action.py' -v
python3 -B qwen_claude_field_theory/closure_2026/entrained_current_construction_2026/check_lean.py
```

`run_001/manifest.json` records the exact bounded suite command, input/output
hashes, software, Git state and actual exit status. `run_001/results.json`
stores the complete Poisson matrices and the internal command exit codes.
All eight final Lean theorems compile using the installed pinned Lean build,
with only the reported standard Lean axioms. An intermediate compile failed
because a real-division definition needed `noncomputable`; that annotation
was added before the final suite. No axiom or `sorry` was added.
