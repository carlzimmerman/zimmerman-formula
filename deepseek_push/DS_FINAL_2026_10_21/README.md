# DS_FINAL_2026_10_21 — index

**Read in this order:** [THEORY.md](THEORY.md) (the finished statement: five postulates, everything
that follows) → [FINAL_THEORY.md](FINAL_THEORY.md) (the working document, including §7b's audit of
its own 32 defects) → [BRIEF.md](BRIEF.md) (the contract every lane worked to) →
[STATUS_BOARD.html](STATUS_BOARD.html) (one screen).

**Scale:** 44 lanes (A1–A16, A18–A44; there is no A17), **507 checks counted in the coordinator's
sweep plus ~56 in the three lanes that print a different format (A23, A31, A32) — ≈563 total**,
and **40 Lean theorems**, no `sorry`, axioms `{propext, Classical.choice, Quot.sound}`.

## The five coordinator scripts — the spine, run these first

| script | what it proves | checks |
|---|---|---|
| `_parent/parent_audit.py` | the κ–Z web, both laws, the separation, the length window | 21/21 |
| `_parent/closure_theorem.py` | P-sector closure (`η=γ` ⇒ `c_s=1`, `λ_P=L*/√2`) + κ is a modulus | 8/8 |
| `_parent/a3_gw_certificate.py` | `c_T² = 1` from the TT action | 6/6 |
| `_parent/a22_no_cosmic_aether.py` | `P = 0` is the unique homogeneous solution | 4/4 |
| `_parent/theory_prediction.py` | rotation curves from the postulates | 4/4 |

## Lanes

| lane | question | status | checks | load-bearing number |
|---|---|---|---|---|
| [A1](A1_horizon/report.md) | can κ = ½ be derived; the "1/12" | **NO-GO** + exact arithmetic | 13 | 𝒩 = 2Z = 11.5776 irrational; "1/12" ⇒ κ = 0.4824; control a₀/cH₀ = 1/7 to 5.6e-4 |
| [A2](A2_medium/report.md) | medium; n=1 vs n=2 | **DERIVED** n=1 | 16 | μ = x/(1+x); 1/A = 1/g + 1/a₀; split 2/√3−1 = 15.470 % |
| [A3](A3_lensing_gw/report.md) | lensing + GW speed | **DERIVED** | 15 | `c_T² = 1`; slip 2.63e-7; scalar speed γ/η |
| [A4](A4_ppn/report.md) | Solar System + stability | CONDITIONAL | 13 | anomaly a₀ = 2557 B_E; `y_t = 66.30`; planets 9.14× |
| [A5](A5_zenodo/report.md) | 178 Zenodo records | COMPLETE | 10 | 625 verbatim quotes, 14 un-integrated clues, 3 tensions |
| [A6](A6_assets/report.md) | unique assets | NO-GO + corrected | 21 | saddle −89.32×; net MW column −2.424 |
| [A7](A7_discriminator/report.md) | n=1 vs n=2 on SPARC | undecidable | 8 | Δχ² +219/−345; z = 0.75; need 1330–1980 galaxies |
| [A8](A8_lean/report.md) | Lean | **CERTIFIED** | 8 + 40 thms | `1/12 < 1/(2Z) < 1/11`; strict `g_q < g_c` |
| [A9](A9_lcdm_audit/report.md) | ΛCDM assumptions | COMPLETE | 10 | κ ∝ Υ^−1.23 (IMF moves it 1.98×) |
| [A10](A10_first_principles/report.md) | one principle | NO-GO | 18 | P2 derives; P1's coefficient does not |
| [A11](A11_cold_normalization/report.md) | cold normalisation | DERIVED + NO-GO | 34 | `M_ph/M_b = ½(√(1+4/y)−1)`; **25.90 / 3.77 (A31-corrected)** |
| [A12](A12_slip_theorem/report.md) | slip theorem | **DERIVED** | 11 | `(Φ−Ψ)/Ψ = O(Ψ)`; charge sector |
| [A13](A13_saddle_forecast/report.md) | saddle forecast | superseded | 12 | depths 2.16–2.37 (**disagrees with A6, unresolved**) |
| [A14](A14_upsilon_free/report.md) | Υ-free κ | NO-GO for 5 % | 13 | κ = 0.354 ± 0.106; 16.1 % distance floor |
| [A15](A15_closure_adjudication/report.md) | is GF2's ½ κ? | **DIFFERENT QUANTITY** | 15 | exact symmetry of the chain |
| [A16](A16_cutoffs_edge/report.md) | cutoffs | NO-GO (one cutoff) | 21 | spread ≥ 3.36 dex; `M_J ∝ ρ^{+1}` |
| [A18](A18_two_ratios/report.md) | the two 5.364s | NO-GO + DECIDABLE | 20 | "cold = phantom" out at 7.7σ |
| [A19](A19_scale_functional/report.md) | scale-setting functional | NO-GO | 17 | Euler charge a₀-blind; channels basis-dependent |
| [A20](A20_Lstar_cores/report.md) | L\* from cores | NUMERICAL | 18 | `R_core = 53.31 pc`; LITTLE THINGS ≤ 90 pc at `f_c→1` |
| [A21](A21_u_half/report.md) | is u = ½? | **NO** | 25 | u = 1+3⟨w⟩ ⇒ ½ needs w = −1/6 |
| [A22](A22_ppn_frames/report.md) | PPN α₁, α₂, β | closed **near-source** | 13 | α₁=α₂=0, β=1 for `r ≪ λ`; `a_P = 6.61e-3 B_E` |
| [A23](A23_no_efe_saddle/report.md) | saddle with EFE | NO-GO (not runnable) | 12 | needs e ≤ 0.22; void is 0.68 |
| [A24](A24_wide_binaries/report.md) | wide binaries | **DERIVED** (corrects the record) | 10 | law IS AQUAL ⇒ EFE; γ_v = 1.18 not 1.51 |
| [A25](A25_kernel_conflict/report.md) | which kernel | **CLOSED** | 14 | Langmuir; 12.99 = 2π⁴/15; RAR cannot close Λ |
| [A26](A26_fork_decider/report.md) | law-first vs medium-first | **CLOSED: LAW-FIRST** | 11 | step +0.453±0.099 vs required −1.622; 21σ |
| [A27](A27_factor_two/report.md) | why `L = 2ℓ₁` | NO-GO | 16 | κ = ½ is the curve `β√χ = 2` |
| [A28](A28_turnoff_origin/report.md) | where `y_t` comes from | NO-GO | 16 | `Λc⁴/a₀² = 8π/κ²` ⇒ `y_t` is κ |
| [A29](A29_u_radial/report.md) | u(r) mechanism | PARTIAL | 25 | step at `1.367 r200c = 1.414 Mpc`; outer u=1 forced |
| [A30](A30_aP_solarsystem/report.md) | `a_P` | unobservable | 11 | 0.17σ joint; 5.7–151× below bounds |
| [A31](A31_referee/report.md) | **adversarial referee** | 32 defects / 130 claims | 35 | the audit in `FINAL_THEORY.md` §7b |
| [A32](A32_cleanroom/report.md) | **clean-room** | all four core results match | 9 | independent of every lane |
| [A33](A33_master_action/MASTER_ACTION.md) | **master action** | DELIVERED | 28 | `Λ_bare ≥ 1.462Λ_obs`; footing closed |
| [A34](A34_dimension_route/report.md) | dimension route | **NUMEROLOGY** | 13 | codim of a point is 3, not 2 |
| [A35](A35_series_parallel/report.md) | least dissipation | **DERIVES n=1** | 22 | `Ψ(A)` minimum = the law; n=2 not a state |
| A36–A44 | α₁, three lengths, saddle resolution, tensor mass, growth, cluster profile, minimal vacuum, cold EoS, no-edge | in flight | — | — |

## Corrections (fix-forward; nothing deleted)

Full list in `FINAL_THEORY.md` §7 (24 items). Largest: **GF2's ½ is not the law's κ**; **"no
external-field effect" is wrong** (the law is simple-μ AQUAL); **the 5.6× kernel tension dissolves**;
**the saddle's net column is negative**; **`y_t` is not independent**; **the footings are the bare
and observed vacuum**, and the action lives at the bare one (`a₀ = 1.132×10⁻¹⁰`).

§7b records 32 defects in this document's own earlier draft — including a self-contradiction on
α₁/α₂ and a cherry-picked rotation-curve subset — found by A31 and corrected in place.

## Reproduce

```bash
python3 _parent/parent_audit.py
python3 _parent/closure_theorem.py
python3 _parent/a3_gw_certificate.py
python3 _parent/a22_no_cosmic_aether.py
python3 _parent/theory_prediction.py
for d in A*/; do (cd "$d" && python3 *_checks.py); done
cd A8_lean && for f in A8_C*.lean; do lake env lean "$f"; done
```
