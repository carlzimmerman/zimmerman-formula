# DS_FINAL_2026_10_21 — index

Entry point: **[FINAL_THEORY.md](FINAL_THEORY.md)** (the synthesis), **[BRIEF.md](BRIEF.md)**
(the contract every lane worked to). Independent coordinator audit:
`_parent/parent_audit.py` → **21/21**, with `--mutate` breaking the κ identity as declared.

Every lane wrote only inside its own directory, introduced no silent fitted constant, and
carries a mutation that must break a check. All check counts below were re-run by the
coordinator after the lane finished; a lane's own summary is not the evidence.

| lane | question | status | checks | load-bearing number |
|---|---|---|---|---|
| [A1](A1_horizon/report.md) | can κ = ½ be derived; the "1/12" | **NO-GO** + exact arithmetic | 13/13 | κ = √(8π/3)/𝒩, requires 𝒩 = 2Z = 11.5776 (irrational); "1/12" ⇒ κ = 0.4824 |
| [A2](A2_medium/report.md) | medium; n = 1 vs n = 2 | **DERIVED n=1** / NO-GO n=2 lattice | 16/16 | μ = x/(1+x) exactly Langmuir; max split 2/√3−1 = 15.47 % |
| [A4](A4_ppn/report.md) | Solar System + stability | **CONDITIONAL**(turn-off) | 13/13 | anomaly a₀ = 2557×B_E; y_t = 100.40 closes Λ |
| [A5](A5_zenodo/report.md) | Zenodo clue mining | **NUMERICAL** | 10/10 | 178 records, 625 verbatim quotes, 14 un-integrated clues, 3 tensions |
| [A6](A6_assets/report.md) | unique assets | **NO-GO**(positive medium) | 21/21 | saddle −89.3× reproduced; net MW column −2.42 M⊙/pc² |
| [A7](A7_discriminator/report.md) | n = 1 vs n = 2 on SPARC | **NUMERICAL** (undecidable) | 8/8 | Δχ² +219 / −345 opposite; z = 0.75; need 1330–1980 galaxies |
| [A8](A8_lean/report.md) | Lean certificates | **CERTIFIED** | 5 files, 23 theorems | standard axioms only; `inv_twoZ_ne_twelfth` |
| [A9](A9_lcdm_audit/report.md) | ΛCDM assumptions in the data | **NUMERICAL** | 10/10 | κ ∝ Υ^−1.23 (IMF moves it 1.98×); 3 of 4 headlines immovable |
| [A10](A10_first_principles/report.md) | one principle for both postulates | **NO-GO** | 18/18 | P2 derives from a saturating current; P1's coefficient does not |
| [A11](A11_cold_normalization/report.md) | cold-sector normalization | DERIVED + **NO-GO** | 34/34 | M_ph/M_b = ½(√(1+4/y)−1); 25.04 vs 2.62; 5.364 = Ω_c/Ω_b |
| [A12](A12_slip_theorem/report.md) | slip theorem | **DERIVED** | 11/11 | (Φ−Ψ)/Ψ = O(Ψ) = 2.63e-7; charge sector, not stress |
| [A13](A13_saddle_forecast/report.md) | saddle-dip forecast | **CONDITIONAL**(EFE) | 12/12 | 2.7e5 pairs, 3280–12400 deg²; depths +11–14 % |
| [A14](A14_upsilon_free/report.md) | Υ-free κ | **NUMERICAL** (no-go for 5 %) | 13/13 | κ = 0.354 ± 0.106; 12 galaxies; 16.1 % distance floor |
| [A15](A15_closure_adjudication/report.md) | is GF2's ½ the law's κ? | **NO-GO** (different quantity) | 15/15 | exact symmetry (a₀,C,σ²,v²)→(μa₀,√μC,√μσ²,√μv²) |
| [A16](A16_cutoffs_edge/report.md) | cutoffs and the edge | **NO-GO**(one cutoff) + derived | 21/21 | r_switch ∝ L\* (density-free); spread ≥ 3.36 dex; M_J ∝ ρ^+1 |
| [A18](A18_two_ratios/report.md) | the two 5.364s | **NO-GO** + DECIDABLE | 20/20 | "cold = phantom" excluded at 7.7σ; A_MID 1.9102 vs 1.000/1.852 |
| [A19](A19_scale_functional/report.md) | the scale-setting functional | **NO-GO** | 17/17 | Euler charge is a₀-blind; channel count basis-dependent |
| [A20](A20_Lstar_cores/report.md) | L\* from inner cores | **NUMERICAL** | 18/18 | R_core = 53.31 pc; LITTLE THINGS bounds L\* ≤ 90 pc (window 24–90 pc); ngVLA 21 % dip at 30 pc |
| [A21](A21_u_half/report.md) | is u = ½? | **NO-GO** + NUMERICAL | 25/25 | u(MID) = 0.4716 ± 0.0362 (0.78σ), u(OUT) = 0.9865 ± 0.0984 (4.9σ); u = 1+3⟨w⟩ ⇒ ½ needs w = −1/6 |
| [A3](A3_lensing_gw/report.md) | lensing + GW speed | **DERIVED** (both gates) | 15/15 | c_T² = 1 exactly; slip 2.63e-7; scalar c_s = √(γ/η) ⇒ γ ≤ η |
| A22 | PPN α₁, α₂, β | in flight | — | — |
| A23 | no-EFE saddle redo | in flight | — | — |

## What this folder does not contain

No rewrite of the underlying corpus, no deletion, no retroactive edits: the eight
corrections in `FINAL_THEORY.md` §7 are fix-forward and name the file or deposit they
correct. The lanes are AI-assisted derivations and checks, not external peer review.

## Reproduce

```bash
python3 _parent/parent_audit.py                 # 21/21, independent
for d in A*/; do (cd "$d" && python3 *_checks.py); done
cd A8_lean && for f in A8_C*.lean; do lake env lean "$f"; done
```
