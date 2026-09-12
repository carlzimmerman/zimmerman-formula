# Concurrent PAPER19/L193: valid identity, missing physical implications

Reviewed after the main audit was staged: L193 commit `bc71158f0` and the
local PAPER19 LaTeX source in `c627a56d9`. That concurrent PAPER19 commit
also collected the staged audit files. `9c0702162` contains only the final
five-line command-log clarification. No shared history was rewritten.

The PAPER19 abstract, sections “The attractor” and “What the critical
surface is”, and L193's V4 interpretation retain the claim that this state
has non-propagating perturbations and supplies a clustering cold component.
**The computations do not establish those implications.**

The stress identity is correct:

    det(T_mixed_tx - L I) = -s0 b^2 W N_T.

We independently derived it in the metric-stress audit. Re-running L193
also passes its five symbolic checks. A third eigenvalue equal to L is an
algebraic degeneracy, not a derivation of an evolution equation or all
directional characteristic speeds. A perfect-fluid interpretation further
requires the appropriate timelike eigendirection; equality of eigenvalues
alone is not an unrestricted fluid-type theorem.

Three missing implications remain decisive:

1. **Non-propagation is not established.** At the very transverse root used
   for the stress degeneracy, the directly varied fixed-metric gamma=0
   subsystem has longitudinal speeds approximately 0.03621 and -0.06949.
   At L192's proposed longitudinal root it instead has complex speeds.
   Neither result is zero propagation in every direction. PAPER19's
   assertion that the zero-gradient constraint structure carries over
   unchanged is the step refuted by the principal audit. The full
   Einstein/cubic reduction is still an open calculation.
2. **Pure pressureless stress does not follow.** At the first source root,
   the repeated eigenvalue is L/U=0.03039926, not zero. Nonzero L alone does
   not exclude a possible dust-plus-vacuum interpretation, but that would
   require additional conservation and pressure-perturbation dynamics; it
   is not proved by stress degeneracy. No constant pressure or separately
   conserved dust component has been derived here.
3. **Attraction is unproved.** The exact gradient-transport identity in
   GRADIENT_TRACKING.md requires a definite source and restoring response.
   Opposite signs of a substituted speed at two selected gradients do not
   determine that response. PAPER19 acknowledges missing tracking
   dynamics but nevertheless calls the state an established attractor.

Thus L193 confirms useful off-shell algebra, not the advertised complete
physical interpretation. Publication metadata or additional conditional
Lean lemmas cannot supply the missing implications. We do not modify the
paper, publication record, or another agent's source in this addendum.

## Reproduction and cutoff

Executed from `/Users/carlzimmerman/new_physics/zimmerman-formula`:

```bash
python3 -B fable_independent_2026/L193_stress_degeneracy.py
shasum -a 256 fable_independent_2026/L193_stress_degeneracy.py qwen_claude_field_theory/papers_2026/PAPER19_gradient_criticality_2026.tex
```

Both commands exited 0. L193 reported five symbolic checks passing; no
background evolution, directional propagation or cold-component test was
executed by that script. Source SHA256 values were respectively
`5d26137b01f583c502fd5d0c7826e1e54a7faf5730fb2135e8638798023318fa` and
`297af08c0dd508bf444d47948a717b7391c6d71d5eb4a7653c15e92d11f2ee27`.
This is a source-and-executable audit of those exact revisions, not a
review of future edits or independent verification of Zenodo publication.
