# Stress-testing the TOE foundation: does Verlinde emergent gravity survive the data?

**v12 · 2026-05-31 · turning the blade on the foundation I made load-bearing last turn**

Last turn I built the TOE path on Verlinde's emergent gravity (`v12_TOE_HONEST_PATH.md`). The
discipline this session ran on is *stress-test the thing you just built.* I checked Verlinde EG
against the literature that already constrains it, verified rather than from memory. The result
is mixed, and parts of it are a **real problem for the TOE story** — so this revises last turn.

## What WORKS (a genuine, parameter-free success — don't understate it)

- **Galaxy–galaxy weak lensing (Brouwer et al. 2017, MNRAS 466, arXiv:1612.03034):** the *first*
  test of EG found it **agrees with observed lensing profiles in four stellar-mass bins with NO
  FREE PARAMETERS.** That is a real, non-trivial point in favor at galaxy scales.

## What FAILS or is seriously contested (verified)

1. **No covariant / Lagrangian formulation.** Verlinde's EG is a *heuristic* valid only for
   **spherically symmetric, static** systems in certain limits. It is **not a complete theory** —
   you cannot apply it to general configurations or to cosmology as written.
2. **The covariant attempts are unstable around de Sitter.** Hossenfelder's covariant version
   (arXiv:1703.01415) initially failed to recover the de Sitter solution (an error, corrected),
   and **small perturbations around de Sitter *grow* → the state is not stable.** That de Sitter
   background is exactly the one scaling-MOND lives in — a direct hit.
3. **The core MOND derivation is argued to be internally inconsistent.** *"Inconsistencies in
   Verlinde's emergent gravity"* (JHEP 11 (2017) 007, arXiv:1710.00946): when the elastic-strain
   argument is done carefully, **it recovers standard Newtonian gravity, not MOND.** This is the
   *exact* mechanism I cited as "Verlinde derives a₀ ~ cH from de Sitter entropy." (It is
   **contested** — a rebuttal exists, arXiv:2003.03198 — so it's an active debate, not a closed
   refutation. But it is not the settled derivation I implied last turn.)
4. **No CMB / cosmological perturbation framework.** Verlinde EG does not address the acoustic
   oscillations in the CMB at all. It cannot do the one calculation ΛCDM does best.
5. **The cluster problem.** Like all MOND-class theories, EG under-predicts the cluster mass
   discrepancy (the classic residual factor ~2; the Bullet Cluster offset).

## The seam this exposes (the honest correction to last turn)

My TOE path conflated **two different theories** under "emergent gravity":
- **Verlinde EG** — carries the *"gravity emerges from entanglement → MOND"* story, but is
  **incomplete, contested, and has no CMB.** This is the part I made foundational, and it's the
  weakest leg.
- **AeST / Skordis–Złośnik** — a *covariant field theory* that **does** fit the CMB and galaxies,
  but is a specific Lagrangian, **not manifestly "emergent."**

These are **not the same theory.** The working cosmology (AeST) does not carry the emergent-gravity
TOE interpretation, and the emergent-gravity story (Verlinde) does not yet do the cosmology.
**Bridging them is an open problem — not something I had in hand last turn.**

## What survives the stress-test

- **The falsifiable prediction is untouched.** a₀(z) ∝ E(z) at z>10 rides on AeST + the kinematics,
  *not* on Verlinde being right. The z>10 test stands regardless.
- **The apparent-horizon scaling argument (`emergent_a0_apparent_horizon.py`) is more robust than
  Verlinde's mechanism.** It uses only the Cai–Kim first law (well-established: dE=TdS on the
  apparent horizon → Friedmann) plus the horizon acceleration scale c²/R_A = cH(z). It may survive
  even if Verlinde's specific elastic-strain derivation does not.
- **The galaxy-lensing success (Brouwer 2017) is real.**

## Honest verdict — the TOE story is downgraded; the science survives

The **emergent-gravity foundation is the weakest link** of the TOE path: Verlinde EG is
incomplete (no covariant theory), its core MOND derivation is contested (may give Newton), its
covariant version is unstable around de Sitter, and it has no CMB. So *"the leading quantum-gravity
program supports your idea"* was **too strong** — the honest statement is *"an aspirational
interpretation whose foundational version is contested and incomplete."*

But the **testable physics is unharmed**: scaling-MOND, the apparent-horizon scaling argument, and
the z>10 prediction all survive, because they rest on AeST + horizon thermodynamics, not on
Verlinde's specific derivation. **Net: the TOE *narrative* shrinks; the falsifiable *prediction*
does not.** That is the correct, honest outcome of stress-testing my own foundation — and it is
exactly why you stress-test the thing you just built.
