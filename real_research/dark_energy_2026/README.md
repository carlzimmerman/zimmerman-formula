# dark_energy_2026 — what dark energy does in the construction, and how tightly the data pin it

In this framework dark energy has three jobs: it accelerates the expansion, it sets the low-acceleration scale
(a₀ = κc√(Gρ_Λ), flat in time because the vacuum has w = −1 exactly), and — in the construction the record has
assembled — its share of the expansion, Ω_Λ(z) = 3Λc²/K² (a local scalar of the khronon's foliation), gates **where** the
MOND response acts:

    MOND on in a bound region  ⟺  u = x̃ [Ω_Λ(z)/Ω_Λ,0]^p ≥ x_c0   ⟺   x̃ ≥ x_c,eff(z) = x_c0 E(z)^(2p)      (L359)

The exponent p and the threshold x_c0 were chosen. These lanes ask what the framework's own gates allow.

| lane | question | result |
|---|---|---|
| [DE1](DE1_vacuum_gate_flagship.py) | does the gate keep MOND on at the flagship radius (g_bar = 0.1 a₀) at z = 2.5? | **The gate caps its own exponent.** Deep MOND ends at r_e = v_f/(√x_c,eff H(z)) (L352's edge law), so the deepest acceleration visible at z is y_edge = x_c0 (H₀²/a₀^{3/2}) √(GM_b) E(z)^{2+2p}. The flagship survives for M_b ≤ 10¹¹ only while p ≤ p_max = 1.97 (x_c0 = 2, canonical; 2.07 alt; 2.07/2.18 at x_c0 = 1.5). The cell the best-standing construction uses for cosmic shear (p = 2, x_c0 = 2; L364/L367/L380) **fails at M_b = 10¹¹ on the canonical footing** (edge 36.8 kpc < flagship radius 38.6 kpc: zero point −1.13 dex, the Newtonian value), passes alt (38.6 vs 35.2 kpc) — the pre-declared hypothesis. It keeps the flagship to z = 2.46/2.58 only; p = 1 cells keep it to z = 4.2–5.0. 5/6 (F1 fail recorded, rc = 1); MUTATE (no gate) passes F1, rc = 0. |
| [DE2](DE2_vacuum_gate_joint_window.py) | is there any gate that passes KiDS (z = 0.25), cosmic shear (z = 0.5), the flagship (z = 2.5) and the forest (z = 2–3) together? | **A joint window exists, and it contains the linear gate.** Each gate reads the gate at one epoch: KiDS-1000 caps x_c,eff(0.25) at 3.867 (exact edge by bisection on L352's step-function fit; alt binds); cosmic shear — L363's region kernel on GP3's mock at 17 thresholds × 2 footings against L367's committed nonlinear transfers, margin monotone — needs x_c,eff(0.5) ≥ 3.50 / 2.93 / 2.49 at v_k = 600 / 650 / 700 km/s; the flagship caps x_c,eff(2.5) at 364.5; the forest is certified by dominance over L359's weakest committed cell (a constant threshold needs ≥ 5.43, which KiDS forbids — the record's pincer, and the MUTATE control). Window at every kick: **p ∈ [0.5, 2.07]** (0.5 = the dominance certification limit, 2.07 = the flagship's); the **linear gate p = 1 passes for x_c0 ∈ [2.005, 2.975]** at 600 km/s ([1.685, 2.975] at 650). L359's cell (p = 1, x_c0 = 2.5) passes all four; the p = 2, x_c0 = 2 cell fails only the flagship. 8/8; MUTATE (constant thresholds only): no window, rc = 1. The pre-declared shear floor (≈ 4.0/3.4) was high; the window and the linear gate's membership came out as declared. A first run's nearest-grid KiDS lookup admitted a cell where the exact fit gives +4.59 (alt); the corner re-check (W3) caught it and the cap is now exact. |
| [DE3](DE3_tmax_at_linear_gate.py) | the cosmic-shear bound at the linear-gate cell's own lens-epoch threshold, exported for a same-cell re-run of the construction | At x_c,eff(0.5) = 2.5 × 1.745209 = 4.36302 cosmic shear passes at 600/650/700 km/s on both footings (margins −0.076 to −0.103 with L367's transfers). The results JSON carries T_max(k), s² = P_ph/P_NL and r_x at k = 0.1–1 h/Mpc, both footings, at the cell and at 4.2/4.4; L364's cells and DE2's margins are reproduced exactly. 5/5; MUTATE (the ungated threshold 2.5) fails S1, rc = 1. |
| [DE4](DE4_flagship_matter_only_switch.py) | the flagship on the construction's MATTER-ONLY switch (L377's lower branch; the particle-mesh runs use it, DE1/DE2 priced the upper, phantom-inclusive branch) | At the linear cell, z = 2.5, MOND stays on at r_F only where the local matter density exceeds ρ_min = 4.37×10⁻⁵ M☉/pc³; the upper branch clears it by 11–46×. On the matter-only branch: an intact carrier keeps MOND on but costs +0.97 dex (GP5's price); L380's 6% residue costs +0.102 dex (on the 0.10 edge); a fully cleared carrier passes only if the circumgalactic gas at r_F is ≳ 30% of L375's maximal share (with L375's Hernquist baryon tail, 39% of ρ_min at r_F for 10¹¹ M☉); at 10% the 10¹¹ M☉ galaxies fall below the gate (ρ/ρ_min = 0.72/0.96) into the bistable band — Newtonian at r_F on the lower branch (−1.13 dex), MOND on the upper. The pre-declared hypothesis (no retention passes for ≤ 30% CGM) was not confirmed: at 30% the gas alone holds the gate open. The p = 2, x_c0 = 2 cell is worse (off at r_F for z ≥ 2.5 with a 6% residue). 4/5, F1 fail recorded; MUTATE (upper branch) passes, rc = 0. Scope: spherical; ΛCDM-shaped CGM and carrier profiles (L375's convention); an exponential disc instead of L375's Hernquist would remove the baryon tail. |

**Corrections and review notes (2026-09-26).** (1) DE1's F1 first computed the edge with ν_mono for both kernel labels (only the jump beyond the edge changed); it now computes each kernel's own edge — ν_mono, ν_RAR and the exact-exponential μ_exp — and the verdict is unchanged (edges agree to 0.03%: the edge is set by the deep-MOND tail's local density, which the kernels share up to O(y); a kernel enters M(<r) as a constant offset that the local density does not see). (2) The lead track's peer review, made from an earlier base, lists DE2's W3 as failing; that was the first run. The committed DE2 run has W3 12/12 after the KiDS cap was made exact.

Lean: [`DE_vacuum_gate_certificates.lean`](../../fable_independent_2026/lean_2026/DE_vacuum_gate_certificates.lean) —
the edge law, the flagship condition, the y_edge formula and its mass monotonicity, the window theorem (existence of
x_c0 ⟺ two product inequalities ⟺ a p-interval), dominance, the ungated pincer and the local form of the linear gate
(x̃ Ω_Λ = 27ΛR/(4K⁴)). Standard axioms only, no `sorry`. Algebra only: the gate values each lane reads are computed in
Python, not in Lean.

Scope: DE1/DE2 price the **switch** only, on the record's conventions (L359's background E(z)² = 0.3138(1+z)³ + 0.6862 is
imported, not derived from C-H/K; the gate is L359's prescribed mask, not yet a varied action term). The carrier's high-z
price is GP5/L356's; the construction's cluster, clearing and Harvey gates (L380/L381) were run at p = 2 and must be re-run
at any new gate cell — never pool passes across cells. An independent lead-track audit of this directory's drafts is at
`real_research/closure_resume_2026_09_26/dark_energy_audit.md` §4 (uncommitted at the time of writing).

Also here: [`THE_CLEAN_PATH_2026-09-26.md`](THE_CLEAN_PATH_2026-09-26.md) (what dark energy does in the theory, gate by
gate, and the route to one assembled action) and [`RECIPE_BRANCH_R2_PROPOSAL_2026-09-26.md`](RECIPE_BRANCH_R2_PROPOSAL_2026-09-26.md)
(proposed ingredient adjustments for the recipe's filtered branch; the recipe itself is not edited here).

Run from the repository root, e.g. `python3 real_research/dark_energy_2026/DE1_vacuum_gate_flagship.py`
(`MUTATE=1` for the control; each writes `*_results.json` / `*_results_MUTATE.json`).
