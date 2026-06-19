# ACCELERATION-FLUCTUATION TERM in dS-Unruh T_eff — verdict (2026-06-19)

*Solution-hunt for a framework-native (no particle DM) cluster + JWST cure. Tests whether the
rapidly-fluctuating acceleration field from cluster substructure raises the de Sitter–Unruh
effective temperature → raises the effective a0 FLOOR in cluster cores. Real data: eRASS1 N=9830
(Bulbul+2024) + 175 SPARC. Code+run: `fluctuation_term.py`. Both ways, quarantine held, galaxy veto
enforced.*

## The mechanism (genuinely-unexplored, grounded in literature)

Deser–Levin (CQG 14 L163, 1997, confirmed): `T_eff = (ℏ/2πckB)·√(|a|² + (cH_Λ)²)`, floor
`cH_Λ = c²√(Λ/3) = √(32π/3)·a0 ≈ 5.79 a0`. The MOND scale a0 is set by the (cH_Λ)² FLOOR inside the
√. **The new physics**: a cluster member's total |a|² = a_smooth² + ⟨a_fluct²⟩ (substructure), so the
floor is raised → `a0_eff = a0·√(1 + ⟨a_fluct²⟩/(cH_Λ)²) = a0·√(1 + ⟨a_fluct²⟩/(5.79 a0)²)`.
⟨a_fluct²⟩ computed via the Chandrasekhar–Holtsmark random-force variance (nearest-neighbor-
regularized — confirmed: the Holtsmark 2nd moment is set entirely by the nearest neighbor).

**Need for a cure**: a0_eff/a0 ~ 4–5 ⟹ ⟨a_fluct²⟩/(cH_Λ)² ~ 15–24 ⟹ √⟨a_fluct²⟩ ~ 23–28 a0 =
2.1–2.7×10⁻⁹ m/s².

## Result — magnitude both ways

| stage | cluster core a0_eff/a0 | galaxy a0_eff/a0 |
|---|---|---|
| ungated member/star granularity | **1.01–1.012x** (rich/HFF cores) | bulge centers **up to 11x** (Σ~1e4 Msun/pc²) — BREAKS veto |
| **+ time-correlation gate** (non-adiabatic) | **1.000x** | **1.0000x** — veto restored |
| needed | **4–5x** | 1.000x (RAR is the data) |

- **PART 1** (eRASS1-typical cores, member-galaxy field): rms a_fluct ~ 0.15–0.89 a0 → boost ≤1.012x.
  The floor cH_Λ ~ 5.79 a0 dilutes any few-a0 fluctuation.
- **PART 2** (a_smooth² in the floor): negligible in deep-MOND (where the residual lives, g_bar~0.04–0.3 a0);
  only matters at a >> 5.79 a0 — the Newtonian regime where MOND is already off (the (b2) sign trap).
- **PART 2b — THE DECISIVE GATE**: a fluctuation couples to T_eff only if it persists over the inertial-
  response time tau_dyn = 1/√(Gρ). The gate cutoff `b_gate = v_rel·tau_dyn ~ R_system` for ANY
  virialized system (since v² ~ GρR², tau_dyn ~ 1/√(Gρ)). So ALL substructure granularity is faster
  than tau_dyn and is adiabatically averaged out — only the smooth field survives. The variance
  self-cancels by construction. Gated boost = **1.000x in clusters AND galaxies**.
- **PART 4 — galaxy veto (both ways, disclosed not buried)**: the UNGATED Holtsmark law on real SPARC
  disks gives median 1.024x but up to **11x at inner bulges** — it does NOT pass trivially (correcting
  my first reading). The SAME gate that nullifies clusters removes the fast bulge-star fluctuations →
  gated boost 1.0000x. Galaxy-safe and cluster-weak together, self-consistently.
- **PART 5 — JWST**: the fluctuation variance is ~0 (gated). The cosmic-mean curvature
  a_curv = c√(Gρ_m(z)) reaches 25–50 a0 at z=6–10 → smooth-floor boost 4–9x (numerically in range),
  BUT that is the SMOOTH density-a0 law: locally it breaks SPARC, globally it is the already-banked
  a0(z) rising-cH branch (a separate mechanism). The fluctuation term itself does NOT unify clusters+JWST.

## Verdict

**FALLS SHORT.** The acceleration-fluctuation term supplies essentially **0% of the needed 4–5x floor
boost** in cluster cores (~1.0–1.1x ungated upper bound; 1.000x with the physically-required non-adiabatic
gate). Two compounding root causes: (i) the cosmological floor cH_Λ ~ 5.79 a0 is already large, so a few-a0
fluctuation is a small fractional perturbation; (ii) the time-correlation gate self-cancels the variance in
any virialized system (b_gate ~ R_sys). The prior estimate was √2≈1.41; the honest gated answer is SMALLER.

**The one genuine virtue** (self-consistent galaxy-safety: the gate that kills the cluster effect also kills
the bulge veto-break) buys nothing, because it nullifies the cluster effect in the same stroke. NOT a cure,
does NOT explain JWST. No manufactured win; the galaxy-bulge artifact is disclosed. QUARANTINE held: a0/Z
never asserted derived.

## Sources
- Deser & Levin, CQG 14 (1997) L163 (de Sitter–Unruh T = α√(a²+c²Λ/3)); thermal-equivalence form
  T_DL = √(T_dS² + (ℏa/2πc)²), T_dS = (ℏc²/2π)√(Λ/3).
- Chandrasekhar 1943 (ApJ 97, 255) + Chandrasekhar–von Neumann 1942/43: random gravitational force /
  Holtsmark variance dominated by the nearest neighbor (arXiv:2201.08478 confirms the 3D variance
  divergence is entirely the nearest neighbor).
- Real data: eRASS1 `erass1cl_primary_v3.2.fits` (Bulbul+2024, N=9830 clean), 175 SPARC rotmod.
- Prior repo: `cluster_closure/mi_dynamic_route.py`, `target_profile.py`, `galaxy_veto_test.py`.
