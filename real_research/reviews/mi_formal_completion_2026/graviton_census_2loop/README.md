# Two-loop graviton-sector transverse-aether census (full cross-check record)

This directory is the **complete cross-check trail** behind the v13 result: *does any
two-graviton-loop diagram generate a transverse `(∇⊥δu)²` aether kinetic term in the
de Sitter–Unruh modified-inertia framework?* **Verdict: no** — `Z_perp = 0` (no
`k⊥²|δu⊥|²` cone) at the divergence level, p-free to all resolvent orders `n`.

Framework-first throughout: modified **inertia** with a **passive frame** (0 propagating
dof, second-class Dirac), `K(□_u)` acting on the frame `u` (never on matter/graviton loop
lines), `□_u = (u·∇)²`, `a₀` and the sign `s=−1` as inputs.

**The load-bearing scripts** (verdict-carrying) live in the parent directory as
`twoloop_graviton_{seagull_vertex,TTloop,cone_vs_mass_decider,kperp_rationing_alln,qfree_diagnosis}.py`.
This subdir holds the **rest of the census**: the all-`n` rigor passes, the induction-loop
audits, and the two-adversarial-skeptics-per-lane independent re-derivations (`*_verify_*`,
`*_MINE*`) that tried to *break* the result and failed.

**The three independent routes to `Z_perp = 0`:**
1. **q⊥ rationing** — the graviton's transverse momentum can ride the loop legs via the
   `h_TT`-dressed connection inside `□_u`, but the frame's external-momentum power is `0`
   for every `n`; a cone needs `2` (a different ≥4-frame-leg topology, not the 2-leg seagull).
2. **TT×δu⊥ vertex vanishing** — CAS at `n=1,2,3` (both polarizations) + all-`n` symbol
   induction + a skeptic-banked `n=6` pass.
3. **cone-vs-mass decider = BENIGN** — the transverse self-energy adds no dispersing spatial
   `q⊥²` cone (p-free vertex) and no `q₀`-pole on the frame line (pure branch cut); the
   constrained `h₀ᵢ` shift sector stays instantaneous. The detector is non-vacuous (a genuine
   `p²` kernel *does* disperse; breaking F1 by hand gives `Z_perp = −24H²/5`).

**Honest boundary:** this is a **divergence-level** census, *not* a full-sector closure.
One-loop and two-loop *finite* parts, genuinely higher loops, wiring the exact seagull tensor
into the loop integral, constraint-survival under loops, and the disformal `ρ_m` variant all
remain open. Sign `s=−1`, `a₀`, and `Z` remain inputs. See paper §radiative and Zenodo
[10.5281/zenodo.21297601](https://doi.org/10.5281/zenodo.21297601) (v13).

Provenance: computed in a parallel session (git worktree, 6-agent workflow
`twoloop-graviton-transverse-aether` + 2 skeptics/lane); the load-bearing and decisive
scripts were independently re-run and reproduced before merging into the paper.
