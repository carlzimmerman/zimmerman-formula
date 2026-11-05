# Claude → astra handoff, 2026-11-04: covariant push, rebuild lanes, open problems

All lanes below are committed and pushed. Each was rerun by the coordinator, and the rerun was identical apart from runtime and RSS unless noted. The single running summary is `covariant_push_2026_10_22/THEORY_V3_DRAFT.md`: one row per lane, with commits. Lane write-ups are in `rebuild_2026_10_22/<LANE>/README.md`. κ = ½ FITTED; footings never pooled; not theory closed.

## 1. Where things stand (one paragraph)
The law g_N = g²/(g + a₀), with a₀ = ½c√(Gρ_DE), holds in isolated galaxies: SPARC, MeerKAT, groups. No single cold sector tested gives both that law and the dust-like clumping that satellites, cluster cores and linear growth need. Every formulation tried hits the same wall:
- v3, v3s, velocity-screened v3, Z★, the PAPER49 tether, the two-phase medium, the equilibrium medium and Codex's P-medium.
- The medium that makes the law cannot self-gravitate.
- A self-gravitating medium has no law, or double-counts.
These are theorems, not just failed fits: U1 T1/T3, O1, M5 S1–S5, PH1, TM1.

## 2. Verified lanes (most decisive first)
| lane | result |
|---|---|
| O1 | Ownership cannot come from a local action in the v3s family. A held host's phantom makes a satellite's held dust hover (ε = 1). Velocity screening (literal v3, NO γ_L) passes Cassini (estimate), outer globulars, TDGs/DF2 and the isolated RAR; it fails satellites and UDGs. |
| M5 | The only stress that makes the law an equilibrium for any baryons is AQUAL minus Newton. It is ill-posed as dynamics, and at low g it cancels the medium's self-gravity (halos collapse at a ≈ 4–7). |
| TM1 | PAPER49's tether gives the law but no clumping. The medium has no self-gravity in its own action: growth δ ∝ a^0.61, σ₈ 0.04–0.08 of dust. Satellites, clusters and saddles fail. |
| PH1 | Two-phase cold energy: NO-GO (needs f_n ≥ 0.855, double-counts SPARC 0.054 → 0.10 dex). |
| Y1 | Codex's P-medium: growth PASS, cores bind, NO galaxy law (history-free branch rms 0.24 dex), no tensor sector. |
| Z1 / ZT | Successor design Z★ = v3s-OC. It survives: Z-T3 well-posed with a dust buffer; Coma passes; Z-T1 undecided on disk data; clusters red. Its ownership rule R2 has no action, per O1. |
| Z2 | The satellite excess is REAL, not tides. At fixed M_V the satellites show NO EFE (−0.05 ± 0.19 vs v3 −0.55, AQUAL −0.76). |
| U1 | T1: held dust ≤ phantom. T3: held dust is weightless in a static host. TDGs/DF2 natively Newtonian (PASS); satellites +2.0 dex STRUCTURAL. |
| H4 / H5 | v3 with γ_L is ill-posed where ρ_τ < 0. v3s (switched stiffness, parallel lane X3) is well-posed. v3s lobes are benign (the khronon streams through, N ≤ 0.05). |
| v3 algebra | `reviews/v3_constraint_algebra_2026_10_23/`: closes with 3 DOF; H4 is a gradient instability, not a rank change. |
| V1 | Density screen: NO-GO (3 constants, breaks SPARC). |
| Q6 / Q7 | Literal v3 has no radiation era (BBN). BS25's DBI K fixes BBN only; growth R_B 0.26–0.32; BS ran no Boltzmann code. |
| L1 A5/A6 | No nonlinear growth restoration at 128/256/384³. BBN-consistent DBI ICs form no halos; cold energy is under-represented in cores. |
| NU1 | Known mass (neutrinos at allowed masses, hidden baryons) does not close the cluster-core gap. A sterile ν would be a new constant. |
| X1 (yours to extend) | A seed-free truncated-Wigner lattice from your stochastic high-H state. Abundance UNDETERMINED; every computed point fails isocurvature by 2e8–6e8 in power. Lattice jobs done; final analysis in progress. |
| W1 (yours) | Your SE-20261023 code reproduced byte-identical and ported 15× faster (preemptible). The strong-seed peak is not converged to 64³; core mass in 2.88 kpc converged; binding not certified. 128³ jobs done; final analysis in progress. |
| T1, S1–S4, P2–P4, F1–F3, P1, D6 | See THEORY_V3_DRAFT rows. |

## 3. Open problems, in order of leverage
1. **Derive a held ↔ free switch from an action**, so one cold medium is held (the law) around quiet, condensed baryons and self-gravitating in hosts, hot gas and early cosmology.
   - What a derivation must evade, and how: O1's ε = 1 theorem, M5's stress uniqueness, and TM1's "no self-gravity". Direct baryon coupling and elastic media are outside M5's scope; that is the open door.
2. **Cluster cores:** ×1.5–1.8 short in the middle and heavy terciles, even with all known mass (NU1). The parallel session's X7 lane is re-measuring the significance.
3. **Cold abundance origin:** an inflationary spectator origin fails isocurvature (X1). It needs an adiabatic production route.
4. **Your W1 formation runs:** finish the convergence and binding verdicts at 128³. The engine is preemptible and on `compute_queue/heavyq.py`.

## 4. Decisive data dates
- **ALMA U4: 2026-11-06.** The CFG942 harness is ready. Four labelled readings are sealed: ν_mono (the verdict kernel), n = 1, n = 2, and v3 AQUAL disc (addendum F, f6f0ba66a4).
- **ALMA GS4: 2026-11-28.**
- **Gaia DR4: December.** The WB prediction is Newtonian for every screened or velocity-screened flavor. The v3 MW seal is `rebuild_2026_10_22/S3_v3_mw_seals/SEALED_V3_MW_DR4.json`.

## 5. Tools
- **Compute queue** `compute_queue/heavyq.py`: preemptible; jobs follow `compute_queue/JOB_CONTRACT.md`.
  - 41 jobs done. The remaining 512³ L1 production needs about 47 GB free; it is stalled at 43 GB.
  - Finished L1 checkpoints (≈ 43 GB) are kept on purpose.
- **Status board:** `explainers/make_status_board.py` (v3 main) and `explainers/make_flavor_boards.py`, which covers 7 flavors: v3, v4, canonical rules, plain MOND, ΛCDM reference, P-medium and v3v. Both have `--selftest` / `--mutate` guards; colour comes only from verified lanes.
- **PAPER59 v1.1:** drafted and audited (392/392). NOT published; it awaits the owner's approval.
