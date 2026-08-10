# nbody_2026 — the nonlinear settling of the khronon dust

**The question this project exists to answer** (THE_COMPLETION v3, non-claim 2d — the sharpest open
problem in the program):

> The smooth-accretion theorem (`mi_ic_route_1mpc_confrontation_2026.py`) implies the Q-sector dust
> falls into every collapsing basin, galaxies included. Does the settled condensate then relax to
> the Helmholtz-preferred, centrally-evacuated static profile (`mi_virialisation_verdict_2026.py`:
> ρ_c tracks Φ, ξ ∝ R², galaxy-interior cost ~6×10⁻⁵ dex — the **favorable branch**), or does it
> retain CDM-like central concentration and overshoot the RAR by the banked 2.06–4.42×
> (the **fatal branch**)?

Nobody — no group, anywhere — has ever done a nonlinear AeST calculation. This folder is the
program's attempt, staged so that each stage produces a committed, checkable verdict before the
next stage's cost is paid. Hardware target: Apple M4, 64 GB (single machine; the 3D stage is sized
for it).

## Stages

| stage | script | question it settles | status |
|---|---|---|---|
| 1 | `stage1_condensate_relaxation_2026.py` | Sound-crossing discriminant: CAN the condensate rearrange within t_H? (11/11) | **done — its favorable branch is WITHDRAWN by stage 2** (crossing is necessary, not sufficient; the Λ_D ≥ 1.2e-9 pinch dies) |
| 2 | `stage2_spherical_collapse_2026.py` | The energetics + shells: what FORCE holds the evacuated profile, and where does the captured dust actually go? (10/10) | **done — FATAL branch is the default at every Λ_D, within the fluid description**: bounded DBI pressure can't support galactic dust (near-miss: needs Λ_D ≈ 1.2e-6, 1.38× above the FRW ceiling ⇒ base_a now mortal); Helmholtz capacity ~1e-7 of the charge; basin free-falls to a sub-kpc caustic; RAR overshoot ~0.72 dex at 10 kpc |
| 2b | `stage2b_base_a_attribution_and_A_conflict_2026.py` | Does base_a bear on the galaxy problem? What replaces stage 2's doors? (15/15) | **done — TWO self-caught errors, opposite directions**: base_a does NOT move the FRW ceiling (hope withdrawn; its real load is the cluster pinch alone), and stage 2's "supported ⇒ survivable" was RIGHT (my tightening used a circular estimator, withdrawn). Replacement constraint is tighter: ceiling ∝ A^(−1/2) ⇒ galaxy support needs A ≤ 0.87 vs cluster calibration 1.65 (Mistele 6.6–56) — **opposite directions**. NEW: v_c = 170 km/s split predicts an unobserved RAR break ⇒ fluid branch **falsified** |
| 3 | `stage3_wave_and_cap_endpoint_2026.py` | The last door: what stops the collapse once the fluid description fails — wave (k⁴) pressure, or the DBI cap? (15/15) | **done — BOTH FAIL.** Wave scale at halo density is **0.18 AU**, eight orders below the RAR region, and *shrinks* as ρ grows (λ ∝ ρ^−¼); a 1 kpc wave core needs M below the Ly-α fuzzy-DM floor. The cap bounds the **pressure, not the density** (exact: ρ_exc ∝ u linear; at saturation ρ ∝ (1−s²)^−½ diverges, p bounded, w→0 ⇒ *pressureless*). ⇒ endpoint is a **black hole of the captured share**, falsified **5.8×10⁵×** against Sgr A* (stellar orbits) |

**Why stage 3 is not a 3D N-body run** (a documented change from the original plan): the khronon dust is an **irrotational potential flow** (v ∝ ∇δφ ⇒ curl v = 0), so it has no angular momentum, no shell-crossing, and no substructure — the three things a PM code exists to compute. The deciding scales are local Lagrangian properties (the dispersion relation and the DBI cap), which a PM code cannot manufacture and would need supplied as inputs. Stage 2 already did the radial infall a PM run would reproduce. Stage 3 was also the go/no-go for that spend, and it returns **no-go**: with the wave scale at 0.18 AU there is no core structure for a 3D solve to resolve.

## Ground rules (the program's standing ones)

- Framework's own premises only: a₀ = κc√(Gρ_Λ) = 9.3619×10⁻¹¹ (canonical) / 1.1279×10⁻¹⁰ (alt),
  Route A kernel ν(y) = 1/(1−e^(−√y)). Both footings on every dimensionful result.
- Every stage exits non-zero on failure, carries negative controls, and reports the verdict
  **whichever way it goes** — the fatal branch is a permissible answer and gets reported with the
  same prominence as the favorable one.
- Λ_D is scanned over its health window 1.9×10⁻¹⁰ ≪ Λ_D ≤ 8.4×10⁻⁷ (`mi_a0_bump_health_2026.py`);
  results that hold only in part of the window say so.
