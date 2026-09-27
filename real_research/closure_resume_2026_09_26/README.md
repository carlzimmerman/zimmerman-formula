# Gravity closure review and constructive checkpoint — 2026-09-26

**Verdict: the requested theory remains open. There is a concrete particle-free
construction program, but the present results do not yet establish a clean path
all the way to closure.** The useful progress is substantial: the moving-source
problem has a candidate momentum channel, the environmental response has an
explicit nonrelativistic action, and the empirical conflicts are much more
specific. This review identifies which of those pieces can actually be joined,
adjusts the Crispy Fried Chicken recipe, and supplies new exact calculations and
scoped Lean certificates. It does not impose a particle dark-matter model or use
ΛCDM agreement as the definition of theoretical consistency.

## Scope and provenance

The starting checkout was `4e16ccf585f6fcc775a2f9d62ac30d329212e0af`, with substantial
pre-existing uncommitted research. The review concentrated on the September
19–26 action, clock, dark-energy, carrier and closure chain, including L330,
L340–L383, KM3, k04, H061, DE1/DE2 and XC1; it is not a line-by-line audit of the
entire repository or a rerun of all observational simulations.

During the review another process advanced the shared checkout to
`03524d209b7ca0c3900f47ccf5dfe42f9187d7c3`, adding the XC1 strong-coupling package.
`git ls-remote origin HEAD` and `git fetch origin main` verified that revision on
GitHub. This task did not merge, reset, commit or push. New evidence uses source
hashes as well as revisions, including the initially untracked files. The XC1
addition was incorporated in the review. The original thirteen-requirement
specification was preserved.

The task history confirms a usage-limit interruption in **Find new breakthrough**.
At inspection, DE2 had a partial log and no completed results JSON. Its advertised
joint window is therefore pending evidence, not a result assumed here.

## What first principles establish about dark energy

Separate three questions: the stress that accelerates expansion, the origin of
the MOND acceleration scale, and the dynamics that determine where a modified
response acts. Identifying all three with “the vacuum” does not derive their
couplings.

A concrete particle-free example is a classical clock with homogeneous action

\[
S_Q=\int dt\,Na^3\mathcal K(Q),\qquad Q=\dot\phi/N,\qquad
\mathcal K(Q)=-V+\frac A2(Q-Q_0)^2,\quad A>0.
\]

For a foliation clock take the future, monotone timelike branch Q>0 and Q0>0;
then the signed expression above agrees with its positive norm. Lapse variation,
scale-factor variation and shift symmetry give, in units c=1 with ρ, p and V
expressed as energy densities,

\[
I=a^3\mathcal K_Q,\qquad
\rho=V+\frac{Q_0 I}{a^3}+\frac{I^2}{2Aa^6},\qquad
p=-V+\frac{I^2}{2Aa^6}.
\]

This is an exact result for the stated homogeneous sector. It contains a vacuum
term, a dust term and a stiff correction in one field. For positive V, the vacuum
term has negative pressure and negative active density \(\rho+3p=-2V\), so it can
drive accelerated expansion when it dominates in an Einstein gravitational
sector. The conserved charge I sets the dust amplitude Q0 I and is independent
initial data; it is not fixed by V. Positive dust requires Q0 I>0 (take I>0 on
this branch). At I=0, Q=Q0>0 and the stress is exactly vacuum stress; the clock
still selects a foliation. Homogeneity
alone does not set I=0. In the algebraic scalar limit Q0=0 the dust term
disappears; I=Q0=0 would not define an admissible foliation clock. The simple
quadratic example is not a full cosmology:
its early-time stiff term and its nonlinear evolution need separate treatment.

The charge identity and quadratic dust example are known after a notation change
from Blanchet–Skordis, equations 47 and 52–54; our calculation independently
varies the stated action and adds an explicit constant V. See the source record
in [the dark-energy audit](dark_energy_audit.md). This is not a novelty claim.

The relation \(a_0=\kappa c\sqrt{G\rho_\Lambda}\), where the restored-SI
\(\rho_\Lambda\) denotes vacuum **mass density**, is a defensible structural target
when the available scales and couplings are specified. It does **not** determine
κ=1/2: an additive constant shifts vacuum stress while leaving a derivative
constitutive law unchanged. The four-form route k04 connects the scales but still
has a free coupling ratio and local feedback. Its result cannot be transferred
to C-H/K without incorporating its action and redoing the variations.

“No dark matter particle” is retained. A classical clock or gravitational field
may nevertheless have independent stress, charge and initial data. Introducing
a new wave field would require explaining its relation to the permitted clock;
calling its quanta non-particles would not supply that derivation. Conversely,
numerical particles sampling a continuum do not establish a particle ontology.

## Which gates and doors remain useful

| Piece | What can be retained | What it does not close |
|---|---|---|
| L330 → L340 momentum channel | A concrete linear mechanism for moving-source response | Full constraint count, nonlinear health or the exact recipe kernel |
| L353 reciprocity | A definite source/force compatibility requirement for a kernel-invisible component | A complete internal action or transport law for that component |
| L361 bound-region action | Explicit NR field variations with a prescribed environment gate | The metric/clock variation of a dynamical gate or relativistic matter conservation |
| L379 → L380 corrected clearing | A justified fixed-cell selection correction and finite pooled window | An action-level existence theorem or a window for a changed gate |
| L381 / GP5 / DE1 | Shape and high-redshift tests that genuinely discriminate constructions | A universal exclusion of particle-free gravity |
| XC1 | Cubic/quartic decoupling power counting with finite parameter checks | Full curved-background, filter/foliation interaction and causal closure |
| Existing Lean certificates | Exact implications from their displayed assumptions | Proof that the same physical action realizes all assumptions |

The source-level limits and equation locators are in
[the recipe audit](recipe_audit.md). Its amendment is now near the top of
[the Crispy Fried Chicken recipe](../../qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md).

## The exact-kernel compatibility problem

The frozen target is \(\mu(x)=1-e^{-x}\), with \(x=g/a_0\). In spherical symmetry,

\[
t=\frac{g_N}{a_0}=x(1-e^{-x}),\qquad
\frac{g-g_N}{a_0}=xe^{-x},\qquad
C_L=\frac{d[(g-g_N)/a_0]}{dt}
=\frac{1-x}{e^x+x-1}<0\quad(x>1).
\]

L340 instead constructs a positive-CL monotone phantom kernel. A close numerical
fit is not the same constitutive law. This sign is an exact compatibility
condition for the construction, not a proof that the user's gravity theory is
impossible. The follow-up independently reduces the scalar block, tests whether
kinetic coefficients and a filter can accommodate negative CL, and states the
costs of the surviving restricted branch. See
[the constructive scalar calculation](recipe_construction_followup.md).

For example, in L340's stated frozen scalar block, writing α=αc and b=c2>0,
the two regularity/stability combinations are
\(D=\alpha+(\alpha+2)C\) and \(N=2-\alpha(1+C)\), with
\(c_s^2=bN/[(2+3b)D]\). The explicit choice α=0.3, b=0.01 is healthy and
subluminal over a bounded constitutive range that includes negative C. It also
changes the static force response and lies outside the construction's quoted
PPN window. This witness prevents promoting the derivative sign into an
overbroad impossibility claim while stating why this particular repair does
not yet meet the user's target.

The requirement is to separate the static force-law derivative from the physical
inertia sufficiently to satisfy both. Adding a constant kinetic coefficient or
filter alone must be tested against the entire required field and momentum
domain, the measured Newton constant and the same-action PPN response.

## New constructive step: varying the gate rather than prescribing it

Let \(\mathcal L_0\) be L361's actual NR density, with
\(M^2=m^2(1-f)\). Its derivative with respect to the gate is

\[
B=\frac{\partial\mathcal L_0}{\partial f}
=\rho_b(\chi-\psi)+
\frac{2m^2\psi w+a_0^2 Q-|\nabla w|^2-m^2\chi^2}{8\pi G}.
\]

The minimal algebraic construction
\(\mathcal L_c=\mathcal L_0+\lambda[f-F(u)]\) gives
\(f=F(u)\), \(\lambda=-B\), and the extra variation
\(B F'(u)\delta u\). Thus a multiplier makes the missing term explicit; it
does not delete it. Here R means \(R^{(3)}+\sigma_{ij}\sigma^{ij}\), rather than
spacetime Ricci curvature, and K is the trace of the extrinsic curvature. For
\(u=27\Lambda R/(4K^4)\), the fixed-R clock-momentum
contribution is \(-4u B F'(u)/K\). This term belongs in the constraint,
perturbation and stress equations of a completed construction.

There is a useful local regularization: write
\(A_g=27\Lambda R/4\) and take
\(f=A_g/(A_g+x_c K^4)\). With Λ>0 and xc>0, for fixed R>0 it extends smoothly
through K=0, with
f=1 and \(f_K=0\). This construction has been checked exactly, including a
nonzero negative-control witness for the omitted clock term. It is a partial
construction lemma, not the selected final gate: it has no continuous joint
extension at R=K=0, negative curvature requires a different domain treatment,
and its smooth tails change the prior empirical switch. The independently
derived second derivatives also show why the kinetic analysis cannot be skipped.
See [the independent gate review](gate_review.md) and
[the checked computation](gate_action_run/results.json).

## Construction path and present stopping point

1. **Fix one action identity and the permitted field content.** Preserve exact
   exponential MOND as the target. Keep Λ and κ's status explicit. A same-clock
   charge is a possible nonparticle source; an independent wave field is not
   silently equivalent to it.
2. **Solve the response/inertia and gate constraints together.** Derive both
   physical potentials, the gate's Bδf terms, actual constraints and physical
   characteristic speeds. The exact slope and scalar-block calculations above
   make this a concrete compatibility problem. Its full functional solution
   remains open.
3. **Complete nonlinear transport for the same field.** The limited condensate
   failure at shell crossing is a serious diagnostic. A proposed regularization
   must survive converging streams while conserving the action's stress and
   respecting its allowed initial data. The current phenomenological kick or
   decay law is not a substitute for that derivation.
4. **Only then assemble the empirical checks on that action.** Reuse the existing
   data and negative controls, while recalculating any prediction changed by the
   kernel, gate, coupling or field content. Require one overlapping parameter
   and solution domain for cosmology, galaxies, lensing, Solar-System physics
   and mergers. Empirical bounds based on a reference cosmology must retain
   their conditional interpretation.

Three distinct routes were executed in this review: homogeneous stress/charge
separation; exact-kernel scalar compatibility with a genuine restricted health
witness; and action-level gate promotion with a locally regular gate. None
establishes the full target. The remaining full covariant constraint calculation,
global gate domain and nonlinear transport are unexecuted continuations, not
exhausted routes or no-go theorems. This checkpoint completes the requested
review and recipe reconciliation; it does not label the research goal solved.

## Verification and handoff

- [Homogeneous-sector check](dark_energy_homogeneous_check.py): 15 exact symbolic
  residuals, continuity identity and two same-action counterexample states;
  [validated provenance](dark_energy_homogeneous_run/manifest.json).
- [Gate-action check](gate_action_check.py): 18 exact identity/control checks;
  [validated provenance](gate_action_run/manifest.json).
- [Scalar-block check](recipe_followup_check.py): 12 exact residuals and a
  nonzero sign-error control, including an exact rational stable/subluminal
  interval; [validated provenance](recipe_followup_run/manifest.json).
- [Lean audit](lean_audit.md): commands, exact theorem inventory, toolchain,
  source hashes, allowed dependencies and scope limits; new source
  [ClosureResume20260926.lean](../../fable_independent_2026/lean_2026/ClosureResume20260926.lean).
  Eight files compiled successfully: 54 existing theorem declarations and
  16 new ones, 70 total. Accepted axiom reports contain only `propext`,
  `Classical.choice` and `Quot.sound`; no `sorryAx`. One harmless tactic-style
  linter warning remains in the new file. These are standard Lean kernel checks,
  not a second-kernel/Comparator certification.
- [Recipe source review](recipe_audit.md),
  [scalar construction follow-up](recipe_construction_followup.md),
  [dark-energy source review](dark_energy_audit.md), and
  [independent gate review](gate_review.md).

Lean certification here means acceptance of those declarations under their
explicit hypotheses. It does not certify observational truth, a completed
action-to-observable bridge, novelty, or the full thirteen-requirement theory.

Final review: the synthesis received an independent mathematical reading, with
clock orientation, vacuum-stress terminology, density units and gate curvature
conventions clarified. Local links resolve, the three computation manifests
validate against their source hashes, and `git diff --check` passes. The spec's
SHA-256 remains `be0400679673b0bb9463dd399ab8e05b8889659ad97736e1b9926276887361c2`.
