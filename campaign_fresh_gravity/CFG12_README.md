# CFG12 — the turned-around share at the budget's own scale

Script: `CFG12_budget_scale.py`, about 3 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. The share is held at CFG4's value, the edges return to CFG4's, and H1 fails (rc = 1).
- The main run also exits 1, because H1 and H2 require both footings and the alt footing fails.

κ = ½ is fitted. Both footings are used.

## The question

CFG4's strict cold budget has a mismatch of scales:
- the sum covers the phantoms of every galaxy down to M_* = 1e7 M☉;
- it is compared with the cold matter turned around at one scale only, the Press–Schechter share at k = 1 h/Mpc (Lagrangian mass 5.45e11 M☉, f_ta = 0.602).

Every budgeted system lives inside a turned-around region at least as massive as its own turnaround mass. So the global necessary condition pairs the sum with the share above the smallest budgeted system's turnaround mass.

The stronger form is mass-resolved. At every threshold M, the phantoms of the systems with M_ta ≥ M must fit into the cold matter turned around above M.

## Results

**Controls**

| check | result |
|---|---|
| C1: CFG7's σ(M) against CFG4_switch's committed σ and f_ta | 0.22%, 0.0008 |
| C2: CFG4's strict edges, with CFG4's share | reproduced exactly |

**D1: the smallest budgeted system.** It is M_* = 1e7 with its SPARC gas.
- Its turnaround mass (CFG4's convention, the law's enclosed mass at r_ta) is 1.05e11 M☉ (canonical) or 1.21e11 (alt).
- The share above it is **0.672 / 0.667**, against CFG4's 0.602. Halving the mass gives 0.696 / 0.692.

**The strict edge**

| row | every galaxy (H1) | with FG001's grouping (H2; CFG11, D ≤ 15 Mpc) | KiDS floor (2-halo) | CFG4 |
|---|---|---|---|---|
| canonical P2 | **0.312** | **0.341** | 0.309 | 0.280 |
| canonical ν_mono | **0.309** | **0.338** | 0.303 | 0.278 |
| alt P2 | 0.268 | 0.293 (0.304 at M_ta/2) | 0.310 | 0.243 |
| alt ν_mono | 0.266 | 0.291 (0.302) | 0.306 | 0.241 |

- H1 and H2 were pre-declared for both footings, and both **FAILED** on the alt rows. They are kept.
- The canonical rows pass both.

**H3: the mass-resolved budget (reported).** At the KiDS floor it binds at the smallest threshold, M ≈ 1e11. The global condition is therefore the right one, and the high-mass end does not bind harder.

The largest ratio of phantoms to the available share:

| footing | every galaxy | FG001-scaled |
|---|---|---|
| canonical | 0.98–0.99 (holds) | 0.90–0.91 |
| alt | 1.15–1.16 | 1.05–1.06 (5–6% over) |

## Standing

Two consistency corrections to CFG4's strict budget point the same way:
- this lane's scale;
- CFG11's hierarchy.

**Canonical footing.** CFG4's minimal conflict is resolved. The strict window opens at x_e ∈ [0.31, 0.34].

**Alt footing.** It stays closed, about 5% short in the budget. Its remaining lever is the budget's own systematics (the HI-selected gas fractions and the SMF normalisation). That lever is not claimed here.

x_e remains declared, within the window. Nothing here says the theory is closed.


## Downgrade (CFG15, 2026-09-28)

The canonical window depends on the KiDS 2-halo amplitude, which is the lens bias.
- CFG4's floor of 0.303–0.309 allowed A ≤ 2, and the fit uses 1.7–1.9 in the massive bins.
- At the framework's own peak-background bias (1.1–1.6) the canonical window survives: floor 0.317–0.322 against edges of 0.338–0.341.
- With unbiased lenses (A ≤ 1) it closes by 0.01–0.02.

**"Resolved" is downgraded to marginal and bias-dependent.**

**Further (CFG16):** with the lens bias taken self-consistently from the truncated profile's own turnaround mass, the canonical window **closes**.
- P2's floor is 0.0003 above the edge.
- ν_mono's floor is 0.010 above it.

This bias is an upper estimate, since it ignores KiDS's isolation cut. The minimal conflict stands at about 3% (canonical) and about 15% (alt).
