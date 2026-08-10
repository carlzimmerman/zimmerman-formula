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
| 3 | `stage3_pm3d/` | The wave/field dynamics at and around the caustic — outside the fluid description, where scalar interference can flatten cores. 3D PM with nonlinear multigrid AQUAL solver | **now DECISIVE, not optional** — the last in-framework door |

## Ground rules (the program's standing ones)

- Framework's own premises only: a₀ = κc√(Gρ_Λ) = 9.3619×10⁻¹¹ (canonical) / 1.1279×10⁻¹⁰ (alt),
  Route A kernel ν(y) = 1/(1−e^(−√y)). Both footings on every dimensionful result.
- Every stage exits non-zero on failure, carries negative controls, and reports the verdict
  **whichever way it goes** — the fatal branch is a permissible answer and gets reported with the
  same prominence as the favorable one.
- Λ_D is scanned over its health window 1.9×10⁻¹⁰ ≪ Λ_D ≤ 8.4×10⁻⁷ (`mi_a0_bump_health_2026.py`);
  results that hold only in part of the window say so.
