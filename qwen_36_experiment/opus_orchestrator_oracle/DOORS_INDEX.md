# DOORS INDEX — pick the highest-ranked `OPEN` door whose prerequisites are done

38 doors. Read **only** the one you pick (`DOORS/<file>`), plus `02_HOUSE_RULES.md` and `04_FRAMEWORK_FACTS.md`.
Update the STATUS column when you finish. Statuses: `OPEN` `IN PROGRESS` `CLOSED` `CONFIRMED` `SPLIT`
`PARKED` `NEEDS_CARL`. **`CLOSED` is a success.**

Ranked by (information gained) / (effort). Doors that can **kill fast** are ranked high on purpose: a cheap
calculation that ends a line of work is worth more than an expensive one that might extend it.

## Tier 1 — do these first (cheap, and each one settles something)

| # | door | file | cost | kills fast | status |
|---|---|---|---|---|---|
| 1 | Knob-free **a₀(z)**, two curves, vs MUSE — the framework's sharpest live observational fork, no new mechanism needed | `E1_knobfree_a0_of_z.md` | S | **YES** | OPEN |
| 2 | **Feed the trajectory in**: ω_star = 2πT_eff = √(a²+H²). The fix already exists at `tn15:194` and is never used | `C1_feed_the_trajectory_in.md` | M | **YES** | OPEN |
| 3 | **The T³ test** — can the mechanism produce an acceleration scale at all? One regression | `C2_T_cubed_band_weight_test.md` | S | **YES** | OPEN |
| 4 | **Can a linear τ-convolution break KMS at all?** A theorem either way, and cheap | `F3_can_linear_dressing_break_kms.md` | S | **YES** | OPEN |
| 5 | **Publish the strong no-go**, correctly scoped: ρ = ω/π² state-independently | `A1_strong_nogo_scoped.md` | S | — | OPEN |
| 6 | **Super-ohmic in equilibrium** — if any admissible s flips the sign, the whole NESS detour was unnecessary | `F4_superohmic_equilibrium_escape.md` | S | **YES** | OPEN |
| 7 | **Repaired tn16** + stationarity gate — stops the −6.7e43 artefact recurring | `B1_repaired_tn16_stationarity_gate.md` | S | — | OPEN |
| 8 | **Specify α(ω) and ω₀** — fixes the exact 1/ω_min divergence; yields the first finite magnitude | `C4_specify_alpha_omega_and_omega0.md` | S | — | OPEN |

## Tier 2 — the real escapes from the wall

| # | door | file | cost | kills fast | status |
|---|---|---|---|---|---|
| 9 | **Bounded-spectrum sector** — where population inversion is legal | `A2_bounded_spectrum_inversion.md` | M | **YES** | OPEN |
| 10 | **Composite operator** φ²/T_μν — ρ genuinely state-dependent; also repairs the q-independence defect | `A3_composite_operator.md` | M | **YES** | OPEN |
| 11 | **Complete positivity** — is the MOND state a physical density matrix? | `A5_complete_positivity_test.md` | S | **YES** | OPEN |
| 12 | **Two-reservoir NESS** from T_GH and T_a — the framework's own two temperatures | `B2_two_reservoir_ness.md` | M | **YES** | OPEN |
| 13 | **Identify the pump** — orbital motion supplies 8.6e-07; the mechanism needs ~3e-2 | `B3_identify_the_pump.md` | S | **YES** | OPEN |
| 14 | **Finite-past IVP** — the memory time is 7.4× the age of the universe | `F1_finite_past_ivp.md` | M | **YES** | OPEN |
| 15 | **Positivity cap on deep MOND** — ghost-freedom vs the observed y range | `D4_positivity_cap_on_deep_mond.md` | S | **YES** | OPEN |
| 16 | **Negative band vs stationarity** — they coincide to <1%; theorem or exception? | `B6_negative_band_vs_positivity.md` | S | **YES** | OPEN |

## Tier 3 — structure, action, and the coefficient

| # | door | file | cost | kills fast | status |
|---|---|---|---|---|---|
| 17 | **Collect the CTP variational prize** — a retarded kernel *can* be variational in-in | `D1_ctp_variational_prize.md` | M | — | OPEN |
| 18 | **Single-scale derivation** from ρ_Λ alone — the one route the relabelling theorem leaves open | `C5_single_scale_derivation.md` | M | — | OPEN |
| 19 | **Derive ω_c**, the free fifth constant that decides the whole suppression question | `C6_derive_omega_c.md` | M | — | OPEN |
| 20 | **Derive η** from dS QFT — q²_crit is η in disguise (2η/A tracks it exactly) | `B5_derive_eta.md` | M | — | OPEN |
| 21 | **Is NESS in the κ-linear relabelling class?** q enters nonlinearly, so the theorem may not apply | `C3_is_ness_in_the_relabelling_class.md` | S | **YES** | OPEN |
| 22 | **Volterra boundedness** with the real dS kernel (every q²_crit so far used a toy) | `F2_volterra_boundedness_real_kernel.md` | S | **YES** | OPEN |
| 23 | **Exact resolvent** instead of Picard — the equation is linear and analytically solvable | `B4_exact_resolvent.md` | S | — | OPEN |
| 24 | **Disformal matter coupling** — on the corpus's own open-escape list | `D2_disformal_matter_coupling.md` | L | — | OPEN |
| 25 | **Ghost-condensate amount** — φ̇ is selected by the extremum of P, not by hand | `D6_ghost_condensate_amount.md` | M | — | OPEN |
| 26 | **Squeezed dS states** — KMS does not apply to them | `A4_squeezed_states.md` | S | — | OPEN |
| 27 | **The b-projector**, at the cost of third derivatives | `D3_b_projector_third_derivatives.md` | M | — | OPEN |
| 28 | **The torsion-free split** — find a system where the action is EXACT | `D5_torsion_free_split.md` | S | — | OPEN |

## Tier 4 — observational fronts already partly armed

| # | door | file | cost | kills fast | status |
|---|---|---|---|---|---|
| 29 | **EFE through the committed AQUAL solver** — a real dSph/wide-binary discriminator | `E2_efe_through_committed_machinery.md` | M | — | OPEN |
| 30 | **Directional-EFE kill switch** — armed, fired once at 1.2σ, needs N ~ 1157 | `E3_directional_efe_killswitch.md` | M | **YES** | OPEN |
| 31 | **Gaia DR4 wide binaries** at the in-force γ_v = 1.0310 (3σ unreachable at any N — cap 1.55σ) | `E5_gaia_dr4_wide_binaries.md` | S | partial | OPEN |
| 32 | **σ-spread across the frozen cluster shell** — the one MI-distinctive cluster signature | `E4_sigma_spread_cluster_shell.md` | M | — | OPEN |
| 33 | **SN-Ia host step** — get the power (18% at the observed 0.06 mag) or retire the lever | `E6_snia_host_step_power.md` | M | — | OPEN |

## Tier 5 — unification-adjacent ⚠️ read the warning in each file first

Carl **publicly retracted** the TOE/SM overclaims on 2026-06-23. An 18-route survey found **every** route
PARTIAL, the three signature numbers derived by **none**, and **no SM bridge**. These are the honest remaining
leads, not near-misses. **G4 is the one to do** — it explains why the rest are hard, and it is cheap.

| # | door | file | cost | kills fast | status |
|---|---|---|---|---|---|
| 34 | **Make the number-field obstruction a theorem** — Z carries √π (transcendental), flavour data is algebraic | `G4_number_field_obstruction.md` | S | **YES** | OPEN |
| 35 | **The SME bridge** — the framework *induces* a computable s_μν (recompute under α=2) | `G3_sme_lorentz_bridge.md` | M | — | OPEN |
| 36 | **Koide Q = 2/3** — the one real flavour lead; expect relabelling, count the parameters | `G1_koide_relation.md` | M | — | OPEN |
| 37 | **E6 × SU(3)_F** — right neighbourhood, HOSTS but does not FORCE | `G2_e6_su3f_neighbourhood.md` | L | — | OPEN |
| 38 | **DSSYK-dS and triality** — two live external leads; DSSYK could settle the floor fork from outside | `G5_dssyk_and_triality_leads.md` | L | — | OPEN |

## Not doors — read once

- `H_CLOSED_do_not_reopen.md` — **18 closed routes with the number that closed each.** Read this before
  proposing anything new, so no cycle is wasted and no withdrawn claim gets re-asserted.

---

## How the doors relate

```
A1 (the wall, correctly scoped)
 ├─ A2 bounded spectrum ──┐
 ├─ A3 composite operator ─┼─→ A5 complete positivity ─→ D4 positivity cap
 └─ A4 squeezed states  ──┘
F3 (can linear dressing break KMS?) ──→ if YES: B2 two-reservoir is the only NESS route left
F4 (super-ohmic in equilibrium)     ──→ if YES: delete q, η, q²_crit entirely; NESS unnecessary
C1 (feed the trajectory in) ──→ C2 (T³ test) ──→ C3 (relabelling class?) ──→ the coefficient verdict
C4 (α(ω), ω₀) ──→ needed before ANY magnitude is quotable (δm ∝ 1/ω_min exactly)
C6 (ω_c) ──→ decides F1, and decides whether the nonlocal reading is suppressed at all
E1 (a₀(z)) ──→ decides the floor fork WITHOUT any new mechanism ← start here
G4 (number-field theorem) ──→ explains G1, G2, and the whole 18-route null
```

## The honest state of play

The mechanism is **untouched** by anything in the review: nothing found is an argument that modified inertia
from the de Sitter vacuum is wrong. What the review found is that the *implementation* did not do what the paper
said. Four doors (**A2, C2, A3, F4**) can each kill or vindicate the mechanism in a single calculation, and three
(**A1, B1, D1**) are cheap and publishable now.

**κ = ½ remains FITTED, NOT DERIVED.** The theory is not closed.
