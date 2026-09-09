# Shared constructive checkpoint: IC11 / IC12 and empirical targets

**Full goal OPEN. No complete or empirically confirmed theory is delivered.**
Started from `347950889570a839af41f6bef0c8bcba7531d02a`; concurrent Fable
commits are preserved, and unrelated working-tree changes are not included.
The target remains every requirement in [the specification](../FRIED_CHICKEN_SPEC.md).

## What is new and reusable

1. [IC11 convex pressure](IC11_CLOCK_PRESSURE.md): an explicit phase-action
   addition preserves the frozen U and vacuum auxiliary equation while changing
   the energy, activation domain and kinetic coefficient. The actual expanding
   plateau has a wider tested healthy range. This is a constructed pressure,
   not a fit to cluster data or a new measured law.
2. [IC11 matter response](IC11_MATTER_GATE.md): varying ordinary physical-metric
   matter exposes superluminal mixing in the pressure-only candidate. A balanced
   auxiliary-curvature coefficient repairs the weak-matter cone in tested
   samples without changing the vacuum pressure. A finite matter fold and its
   actual canonical bracket are computed; the fold is not a Dirac-rank loss.
3. [Full IC10 transition and spatial completion](IC11_TRANSITION.md): all
   switch derivatives and the omitted auxiliary spatial block are restored.
   A specified correction gives an isotropic luminal tensor and removes
   auxiliary poles at the tested backgrounds. Its scalar kinetic sign fails.
4. [IC12 combined action](IC12_COMBINED.md): pressure and spatial completion
   are varied TOGETHER, with new roots. This prevents combining passes from
   different theories. It still fails a necessary transition scalar kinetic
   condition, first at grid sample n=207. The balanced matter correction is
   a separate candidate and is not included in IC12.
5. [Exact-law cluster/pair targets](../cluster_pair_clock_target_2026/TARGET_REPORT.md):
   source profiles and raw-catalogue likelihoods are recomputed. An independent
   review found and corrected a too-short third-galaxy search, removing 11
   falsely isolated F=5 pairs and 77 F=8 pairs. Both the correction and its
   modest effect are retained; it does not solve the remaining discrepancy.

Carl Zimmerman's paddle/wake suggestion is credited in
[CARL_CLOCK_MEMORY_INSIGHT](CARL_CLOCK_MEMORY_INSIGHT.md). It adds an explicit
history-dependent, action-evolved clock-source task. The analogy itself is not
a scientific confirmation or a literature-wide novelty result.

## Best-supported next construction, not a declared winning theory

Keep the explicit local Einstein-clock structure as a starting component and
replace the transition kinetic design. The computed diagnostic

    aUV = E A/6 + h_rhorho/4

must be derived from the redesigned action and remain positive wherever the
full-rank auxiliary elimination applies. Merely changing the plateau pressure,
declaring cT=1, or removing the auxiliary determinant roots does not do this.
Immediately check the full characteristic operator after any kinetic repair:
momentum-dependent curvature coefficients can introduce additional high-k
terms, so positivity of aUV alone is not success. Preserve static first jets,
then recompute homogeneous roots and the actual k=0/k!=0 constraint algebra.

For matter, continue using fixed canonical variables around the computed fold
rather than dividing by L_ww and mistaking a velocity chart failure for lost
Dirac rank. The current balanced coefficient is only a local regular-chart
construction; the finite-density and global denominator problems remain.

For the empirical goal, compute the evolved clock stress and the exact-law
two-body boundary-value force. Use stress-surface force integration and grid,
box and body-size convergence. Fold the result through selection-aware pair
populations. Required inverse source profiles are not solutions of the clock
action, and A^4 cannot assign a mass to a diffuse pressureful clock halo.
The literal baryon-only galactic MOND requirement must also be preserved;
an added clock density cannot silently replace that requirement everywhere.

## What still prevents full closure

- Full physical-metric baryon-only AQUAL and independently derived Phi/Psi.
- Full field-theory constraint preservation/count, beyond homogeneous matrices
  and the regular Einstein-clock plateau action argument.
- Beta, gamma, alpha1/2/3 and measured Newton constant from this same action.
- Healthy physical characteristics across transitions, matter ranges and
  anisotropic backgrounds; a controlled strong-coupling scale and y=0 limit.
- A realistic cosmological history, sourced galactic branch and successful
  cluster/pair predictions from common initial/boundary conditions.

The ordinary matter Ward identity follows from unchanged minimal coupling;
it does not fill the other gaps. The a0–Lambda relation remains an input.
No Lean certificate or literature-wide novelty proof is asserted.

## Evidence and division of work

`clock_pressure_repair`, `transition_completion`, and `cluster_pair_target`
implemented disjoint computations. Root implemented the matter gate.
Read-only `ic11_review` independently checked the action corrections and
corrected catalogue selection; `matter_fold_audit` independently rederived the
coupled matrices and verified the fold at 70 digits. Agreement is supporting
evidence, not a formal proof certificate. Self-proofreading of new mathematical
notes made no mathematical-token substitutions.

The exact executed commands, input hashes, durations, output hashes and child
exit statuses are recorded under [ic11_run_001](ic11_run_001/run_index.json).
Ordinary scripts report partial results with exit0; strict full-closure flags
return exit2, not a theory PASS. The provenance runner reports those deliberate
nonzero child exits as failed runs; that is expected and must not be erased.
The empirical directory has its own manifest with explicitly disclosed legacy
provenance limits. Frozen previous scientific inputs and old runs are unchanged.

Recorded verification: all 232 construction regression tests passed (exit 0),
and all 32 lapse-braiding regression tests passed (exit 0). The six ordinary
recorded runs exited 0; the three strict closure runs exited 2 (runner exit 1).
All nine v2 manifests validated with exit 0; the separate empirical v1 manifest
validated with its legacy limitations reported. These are computational
verification results, not a full-theory PASS.
