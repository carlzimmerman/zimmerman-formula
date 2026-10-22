# E1_input_audit: are the doors-push verdicts and the screened theory's inputs free of hidden ΛCDM or MOND?

## Verdict: CRISP FINDING

Most verdicts survive clean substitution. Four do not:
- D7c flips.
- D8's thermal-L★ exclusion flips.
- D8b's floor reading flips.
- D6's "u_gal excludes 0.47" flips under one substitute and moves materially under another.

Two record inputs of the screened theory move materially:
- the L★ ≥ 24 pc floor, mainly through the SPS Υ_V of the globulars;
- P4's u ≈ 0.47, through the h = 0.70 distance convention of the shear stack.

The a₀ canonical footing is clean to 3 %. The alt footing is a ΛCDM import.

- Criteria: `FROZEN_CRITERIA.md`, committed alone first (581d52210b).
- Ledger: `INPUT_LEDGER.md`, 43 inputs, each with a class, a source and the verdicts that use it.
- Script: `e1_input_audit.py`, 6/6 PASS, exit 0, about 70 s, one thread, peak memory 0.25 GB.
  - On the first run, K6 parsed the ledger's header row as a data row. That was a parser bug, fixed before the scored run.
- `E1_MUTATE=1` puts 2π in place of Z. K1 then fails and the run exits 1 (`*_MUTATE.*`).
- Rules held: κ = ½ is FITTED. Footings are never pooled. Not theory closed. Nothing here says the data favour the framework.

## 1. The background: what a framework-native H₀ does

A46 shows the model's background is an exact reparametrisation of flat ΛCDM. Its own H₀ comes out as H₀,ΛCDM·√Ω_Λ, so it is
**the very quantity the canonical footing already uses**.

| native H₀ source | H₀ (km/s/Mpc) | a₀ = cH₀/Z | vs canonical | vs alt |
|---|---|---|---|---|
| A46 2-pt fit | 54.99 | 9.23e-11 | −1.4 % | −18.4 % |
| A46 3-pt fit | 56.77 | 9.53e-11 | +1.8 % | −15.8 % |
| A46 exact map | 57.16 | 9.59e-11 | +2.5 % | −15.2 % |
| CFG886 (BAO + BBN, no CMB) | 57.46 | 9.64e-11 | +3.0 % | −14.7 % |

- **Canonical footing: clean to 3 %.** The alt footing (cH₀/Z at H₀ = 67.4) has no native counterpart. A46 prices it at
  Δχ² 58.8 / 749. This is already in the record (THEORY P3). The ledger now classes every "alt" number as ΛCDM-PROCESSED.
- **κ.** Measured in the dark-energy convention, κ moves by ≤ 3 %: CFG493 0.417 → 0.405–0.423.
  - In the P3 convention (A51/A71/A81), κ rises by 17–23 % and merges with the DE convention:
    A81 0.378 → 0.444–0.463.
  - The distance of ½ falls from 1.0σ to 0.25–0.46σ. That is CLEAN under the frozen 1σ line.
  - A51's 12.5 % H₀ term in the coherent floor shrinks to 2.2 %.
- **New flag (not in the record as a number).** The native H₀ band, 55.0–57.5, sits **15.5–18σ below** the local ladder
  73.0 ± 1.0 that is on disk (A51). Planck-ΛCDM's 67.4 sits 5.6σ below it.
  - SPARC's 97 Hubble-flow distances use 73.
  - No single H₀ makes the framework's background, ρ_Λ and the SPARC distances agree. The mixed-H₀ trap is not removed by
    going native.

## 2. Verdict by verdict

| verdict | survives clean substitution? | shift (numbers in `e1_input_audit_results.json`) |
|---|---|---|
| D1 skew SCOPED NO-GO | **yes** | Obstruction 1 is law-only. Obstruction 2 has a 17–50× margin. A ≤ 3 % a₀ shift and ±0.2 dex Υ cannot reach either (bounded). |
| D2 corrections; fork DATA-GATED | **yes** | γ_v(20 kAU, PREREG primary): 1.175 → 1.1725–1.1806 at native a₀ (interpolated), below σ_sys 0.020. Solver is QUMOND: DEFERRED to E2. |
| D4 ALMA power | **yes** | Nothing is scored either way. a₀(z) "F-DESI" is a w₀w_a fit (ΛCDM-family). The M★ ±0.2 dex is already propagated (information only). |
| D5 κ-four no-go | **yes** | The theorem is mathematical. The κ bands move ≤ 3 % and P_cover stays 1.0. |
| D6 (1)–(3) | **yes** | r_sp (NFW c = 4.5, 0.83 r200m) × 0.8 / × 1.25: H-VR χ² 31.4 / 44.3 for 8 dof (record 39.0). Still rejected. |
| D6 (4) u_gal ≥ 0.66, 6.8σ above 0.47 | **no: FLIP + MATERIAL** | M★ −0.2 dex: u_gal 0.501, **+1.5σ (not excluded, canonical)**; alt 0.567, +4.2σ. At native h, the 0.47 benchmark itself moves to **0.643**; u_gal moves to 0.80–0.84. |
| D7 turn-off no-go | **yes** | Analytic. The y_t band is a κ band. Saturn sits at 5.5e-4 of its bound. |
| D7b canonical law fails Q₂ | **yes** | Native a₀: 3.65–3.73× the Hees 2σ line (record 1.70–3.70× canonical). Solver is QUMOND: DEFERRED to E2. |
| D7c "no law passes both" | **no: FLIP** | Native background (one footing, no alt): **β ≥ 3 passes Hees at all four fields and SPARC (primary) at all three native a₀; β = 2.5 at two of three** (Q₂/2σ 0.87–0.99; SPARC z −1.59 to −2.00, so the passes are knife-edge, with β = 4 at −1.999 and β = 2.5 at −2.00). D7c's only failing cell was alt-E0, a ΛCDM import. The outcome becomes **UNDECIDED**: S1 Δχ² still disfavours β ≥ 2.5 at z −5.39 to −5.83. The SPARC side also flips with the Υ prior: at −0.2 dex L −1.71 and β 2.5 −3.63; at +0.2 dex L −4.44 and β 2.5 +0.12. |
| D8 (2) thermal L★ "excluded at 95 %" (Δχ² 3.91) | **no: FLIP** | Native a₀ low end: 3.78 (allowed). Υ_V −0.2 dex: 0.32 (allowed). Υ_V +0.2 dex: 9.67. A 0.07 margin cannot carry a verdict. |
| D8 (3) tidal dwarfs, median 42 / 35 pc | **yes** (shifted) | Within the window unless Υ_V is +0.2 dex (floor 41 pc). |
| D8b (1), (2) | **yes** | Raw HI rank and scatter tests. A uniform M/L shift cannot change a rank. |
| D8b (3) "floor reading puts L★ below the globular floor" | **no: FLIP (both ways)** | Υ_V −0.2 dex: the floor falls to 12.5 pc, so the envelope (14–17 pc) sits above it. Υ_V +0.2 dex: the floor is 41.1 pc, so even the median 29.9 pc sits below it. Native a₀: 16.7–29.4 pc vs floor 23.7 (unchanged). |

## 3. Record inputs of the screened theory

| input | class | sensitivity | outcome |
|---|---|---|---|
| L★ ≥ 24 pc (CFG820) | SPS Υ_V 1.6 (SURVEY) + ν_RAR with algebraic EFE (**STANDARD-MOND-MACHINERY**) | Υ_V ±0.2 dex: **12.45 / 41.06 pc**. ν_L + same EFE: 23.87. Isolated ν_L: 28.85. Native a₀: 23.57–23.79 | **MATERIAL** (SPS-dominated; the MOND recipe adds +1 % to +22 %) |
| u ≈ 0.47 (CFG687 / A21 / P4) | ΛCDM-PROCESSED (h = 0.70 convention, eRASS1 M_gas / R500) | h 0.674: 0.497. h 0.730: 0.444. Native h: **0.643 / 0.658** (+4.7 / +5.1σ). f_s ±0.2 dex: 0.455 / 0.497. r_sp bracket: no effect on u_MID | **MATERIAL**: u is an h-dependent number (d u/d ln h = −0.67) |
| κ (CFG493, A51, A71, A81) | ΛCDM-PROCESSED via ρ_Λ | ≤ 3 % (DE convention); see §1 | CLEAN |
| Ω_c/Ω_b = 5.3643 | ΛCDM-PROCESSED | CFG886 (a) 5.272: R_req gap +0.58σ (record +0.44σ). (b) SH0ES 6.122: −1.07σ | CLEAN (a) / MATERIAL (b), no flip |
| Hees 2014 / Park 2026 Q₂ | RAW parametrised-anomaly bound: Q₂ is fitted with a GR ephemeris and no MOND function | — | clean input; the comparison side (QUMOND) is E2's |
| Cookson+26 | SURVEY (Newton template priors); its MOND template is reference only | not recomputable on disk | DEFERRED |
| Chae & Yoon 26 | SURVEY; only a one-line summary is on disk | — | DEFERRED (needs the paper) |

## 4. Record errors and stale text found

- `deepseek_push/DS_FINAL_2026_10_21/A9_lcdm_audit/report.md:34-51, 96` still says a₀ ∝ 1/D (exact). The physics is
  a₀ ∝ D⁻², because g_bar is distance-free. A14 D2 and A31 C109 already corrected this, but A9 was not fixed forward.
- THEORY P4 quotes u = 0.47 with no h caveat. The number belongs to h = 0.70, which is neither Planck nor the native value.
- `campaign_fresh_gravity/CFG820_stiffness_from_globulars/cfg820.py` scores the globulars with ν_RAR(y_int + y_ext). That is
  a MOND recipe, not the canonical law and not the action. The floor quoted as "the screened theory's L★ ≥ 24 pc" inherits it.

## What this does not show

- It does not solve the action's own (AQUAL-limit) field equation for Q₂, γ_v or the globulars. That is lane E2.
  S4 brackets only the globulars.
- It does not propagate the h dependence of u into the A71/A81 joint fit. The cluster channel there pulls κ by +0.36σ.
- It does not say which H₀ is right. It shows that the verdicts listed above depend on that choice, or on a 0.2 dex SPS shift.
- The u_gal and u_MID rescalings use the leading physical h-scalings. They do not include the 1 % distance-ratio change
  between Ω_m 0.2793 / 0.30 and the native Ω_eff.

**Most valuable next step:** re-derive the L★ floor with the action's own field equation (E2's solver) on the three outer
globulars, with Υ_V marginalised over its SPS range (prior ±0.2 dex), and report L★_95 as a band, not as 24 pc.
