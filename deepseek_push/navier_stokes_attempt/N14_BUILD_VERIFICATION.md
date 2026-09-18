# N14 — THE MACHINE-VERIFICATION LANDING (2026-09-17)

We built the openai/NavierStokesAndEuler formalization on this machine and
re-verified the head theorems ourselves.

## What was done

1. Clone: `deepseek_push/navier_stokes_attempt/openai_NS_lean/` (47 MB,
   depth 1; the directory is UNTRACKED — kept out of the repo).
2. Cache: `lake exe cache get` — a FULL HIT against the repo's cached
   Mathlib (Lean 4.34.0-rc2, the same toolchain & Mathlib commit this repo's
   own Lean lane uses): "No files to download", 8,557 files decompressed,
   13 s. Toolchain identity confirmed by the cache itself.
3. Build: `lake build` — **exit 0, "Build completed successfully (11424
   jobs)"**, ~1 h on this M4 (19 workers). No warnings of any failed file.
4. Standalone recompile of the two head theorem modules:
   `NavierStokes/R3/Theorem.lean` → exit 0; `PeriodicPaperTheorem.lean` →
   exit 0.
5. Axiom audit (fresh probe file, `#print axioms`): every head theorem
   depends on exactly {propext, Classical.choice, Quot.sound}:
   - `NavierStokesR3.theorem_1_1` ✓
   - `NavierStokesR3.theorem_1_1_with_initial_rest` ✓
   - `NavierStokesR3.theorem_1_1_with_dissipation` ✓
   - `NavierStokesR3.breakdownStatement` ✓
   - `NavierStokes.Comparator.navier_stokes_breakdown_R3` /
     `_periodic` ✓
   No sorryAx anywhere in the proof terms.

## What the formalized statement says (read from source)

`breakdownStatement` (the (C)-alternative, energy-bounded form):
∃(u, p, f, K), CandidateProperties ν u p f K ∧ ¬ Nonempty
(GlobalFiniteEnergySolution ν f), where the properties carry: u, p smooth
on [0,1)×ℝ³ (ContDiffOn ∞), u(0) = 0, divergence-free, the residual
∂ₜu + (u·∇)u − νΔu + ∇p = f on (0,1) — with ordinary Fréchet derivatives —
periodic in the three spatial shifts, energy-bounded on [0,1) (L²-uniform),
SUP unbounded at t = 1 in every left neighborhood, u,p supported in a compact
K, f smooth everywhere with compact positive-time support — plus
`theorem_1_1_with_dissipation` carrying the explicit energy inequality
(∀T<1: ‖u‖²L2 + 2ν∫ᵀ₀D ≤ (∫ᵀ₀‖f‖norm)²) and interval-integrability of the
dissipation (Lemma 10.4's content, formally).

`periodic_corollary : breakdownStatement` — the torus (D)-alternative proved
from the ℝ³ result by compact support, as the paper claims.

## The honest ledger of this verification

| Check | Verdict |
|---|---|
| the formal system is self-consistent and complete (11,424 jobs, exit 0) | PASSED — reproduced here |
| the head theorems are real theorems of the formal system (axioms clean) | PASSED — reproduced here |
| the formal statements match the paper's Theorem 1.1 (C)/(D) + energy claims | PASSED at the statement level (read above); note f's spatial support is encoded as CompactPositiveTimeSupport in the R3 properties (the paper's C∞_c class modulo lift conventions) |
| the statements match Fefferman's Clay alternatives (C) with bounded energy | CONSISTENT as formalized: the force is part of the construction, u₀ = 0, blowup + bounded energy, no global smooth bounded-energy solution with the same f |
| the informal 600k-line argument is MATHEMATICALLY correct | NOT settled here: Lean rules on what is written; statement-drift and human review remain the open refereeing questions (N08's status stands: no referee process started) |
| (A)/(B) unforced regularity | UNTOUCHED, as always — out of this construction's scope |

## Interpretation

The resolution's machine-checkable core — that the 35,731 formal theorems
close — has now been independently reproduced on a second machine (ours),
on the same toolchain, with a cache-level identity check. This converts the
verification from "their audit says" to "we built it, it compiled, the head
theorems' axioms are clean". What the machine cannot certify is that the
formal statements say what the news release says — the statement read above
is our best-faith transcription, and the referee court remains the open
item. Everything else (the skeleton audit N13, the consistency with the
window theorem, the self-seeding story) is on the record.

How to rerun: `cd openai_NS_lean && lake exe cache get && lake build`
(the build tree is NOT committed; the clone script is the record).

— navier_stokes_attempt, N14 landing.