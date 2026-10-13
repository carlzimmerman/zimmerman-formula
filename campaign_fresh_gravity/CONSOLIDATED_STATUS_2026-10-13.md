# Consolidated status, 2026-10-13: everything landed on origin/main since 2026-10-09

Reading lane only. No new runs; no file other than this one was changed. Every label and number is copied from a committed
README, scorecard or commit message, with the commit cited. κ = ½ is FITTED (CFG493: 0.42 ± 0.10); footings 9.36e-11 /
1.13e-10 m s⁻², never pooled; "cold energy", whose MASS is required, with no particle species. Not "theory closed". Nothing here
says the data favour the framework.

**Scope and method.**
- **Window:** origin/main from 2026-10-09 to 3f05b3511, re-fetched on 2026-10-12 at 22:17. That is about 480 commits.
- **Sources:** six read-only inventories, one per block, each built from the lane READMEs, scorecards, LEDGER rows and commit
  messages:
  - CFG540–559
  - CFG579–602 + CFG700
  - CFG620–657
  - CFG660–679
  - CFG680–691 + dossier documents
  - astra/codex
- **Re-checks:** every conflict in §8 was re-checked directly against the committed files.
- **Rows marked †:** the label is quoted from the result commit message.
- **New after dc0bb478c:**
  - 0b259107d: CFG710 SEALED, the B1938 lens structure.
  - 097b2feee: CFG692 frozen criteria, "gravitating polarization". This is criteria only; no number exists yet.

---

## 0. Executive summary

1. **No candidate passes the one-action contract.** CFG678 (2ddb9c4ad): "NO candidate passes the contract." The gates that
   no candidate passes are B1 (switch from an action), B3/A2 (a well-posed cold-energy sector), C3 (massive early types) and
   D2 (growth vs raw KiDS).
2. **Raw-data passes on the record** (all footing-wise): SPARC RAR (CFG624 G1, rms 0.1003/0.1013), Tian groups (CFG543
   addendum), Local Group timing *with* cold energy (CFG624 contrast), primary CMB switch-off (CFG649). Also counted, with
   conditions: the CMB-free BAO Ω_m consistency for flat a₀ (CFG682: "0.65 sigma, CONSISTENT"; CFG684 "ROBUST") and NGC 1052
   (CFG655, "PASS CONDITIONAL ON THE FORMATION-CHANNEL LABEL").
3. **Raw-data failures and exclusions:** raw KiDS shear for candidate B (CFG596 "EXCLUDED (dchi2 +68.7)") and for the
   capped condensed source (CFG636 "EXCLUDED narrowly", +13.97). Massive early types: CFG529 FAIL, with every baryonic escape
   closed (CFG580–582, CFG644). The no-cold-energy universe fails X-COP, Bullet and Local Group timing (CFG624). The non-lensing
   response sector is EXCLUDED (CFG663). Isotropic stress is EXCLUDED on SPARC (CFG660). The dark-energy clock is "SHAPE
   DISFAVOURED" (CFG666_dark_energy_clock).
4. **Shear labels are RELATIVE** (codex audit d992929b9, accepted in eb4f5af3a). Absolute KiDS χ²: S0 144.3 (p 0.014),
   CFG636 158.2 (p 0.002), CFG596 213.0 (p < 0.001). Native PM verdicts are also conditional on inherited ΛCDM inputs, and the
   growth gate is a benchmark, not an exclusion (astra 5c31fcad4, accepted in e1524b26a).
5. **Theory v2 (aa8a34383) is untested on its own decisive gate.** CFG650 T12 (post-preview selection) is queued behind a
   waiter; T1 (the primary, pre-declared run) follows; the CFG654 native-input rerun is frozen but not started.
6. **The KiDS early-type age signal is now NOT ROBUST.** CFG667: "STELLAR-MASS ARTEFACT LIKELY". CFG669: T1 "PARTIAL",
   combined "NOT ROBUST". The early-type **excess** at matched baryonic mass **PERSISTS** on Ks masses (CFG669 T2, Z 3.37).
   CFG669 explicitly "corrects CFG668's tentative softening".
7. **Mechanism side: no derivation yet.**
   - CFG679 Part 2: "15 candidates: none passes".
   - CFG661: NO-GO for a local compression-responding stress with {G, a₀}.
   - CFG665: isothermal selector "VOID".
   - CFG645: "NOT DERIVABLE KNOB-FREE".
   - CFG643: heat-exchange door "CLOSED".
   - CFG642: Ω_c/Ω_b symbolic regression "CHANCE-LEVEL".
   - CFG690: cubic "R0-SHAPED, REDUCED, R0 still not passed".
   - CFG691: stiffness window "WINDOW OPEN, CONDITIONAL" (on a disclosed criteria error).
8. **Sealed predictions** waiting on data: CFG553 (Gaia DR4, 2026-12-02), CFG570/571 (ALMA, 2026-11-06 / 11-28), CFG672
   (JWST GO 12088), CFG673 (GO 8281; the record's own photometry is NOT DIAGNOSTIC, CFG674), CFG675 (LISA), CFG676 (a₀-siren).
9. **Reconciled conflicts (§8).**
   - **Ω_c/Ω_b:** both values are arithmetically right. 5.481 mixes BBN ω_b with CMB ω_c. Use the self-consistent CMB pair
     (5.364/5.376) as primary and carry BBN 5.47–5.48 as a declared bracket. The effect is at most +2.2% supply, a disclosure
     item, not a verdict changer.
   - **Age signal:** NOT ROBUST. It appears only with LePhare masses (Taylor Z 0.46, Ks Z 0.93).
   - **Early-type excess:** PERSISTS. CFG669 on Ks gives Z 3.37; CFG668's "explains" label rests on a failed matching control.
   - **CFG678 duplicate:** resolved on main (alias CFG710).
   - **CFG679 duplicate:** open. Proposed CFG720 (or CFG603) for the untracked DES Y3 lane.
   - **Also found:** the TOE_BEST_ATTEMPT v2 Lean file was reverted to v1 on main (§7.1).
10. **Theory v2 needs text edits** (§3b, items (a)–(o)). Each is marked VERIFIED or NOT VERIFIED against the committed
    lane text. None has been applied.

---

## 1. Inventory by lane (since 2026-10-09)

Owning chat is inferred from commit messages and LEDGER rows. "orch" = orchestrator chat; "owner" = owner chat; "Lean/GW" =
the GW/lensing-perturber + Lean chat (block CFG670–679); "BAO" = count-magnification/BAO chat (block CFG680–689); "astra" =
astra/codex. The sealed hashes are prefixes of the committed sha256 values.

### 1a. CFG540–559 (orch, 10-09/10-10)
| ID | question | frozen label (verbatim) | key numbers (verbatim) | caveats | commit |
|---|---|---|---|---|---|
| CFG539 † | cold-energy equation of motion | "NO cold-energy equation of motion is VIABLE" | — | — | ad875dbd6 |
| CFG540 † | Tian+26 BFJR under the law | (assessment) "law tracks slope with +0.1 dex offset; MaNGA ellipticals = stellar mass scale; groups expose the census edge" | — | — | bf797b8f9 / 654f256ef |
| CFG541 † | class-A cold energy made precise | "SPECIFIED WITH OPEN ITEMS" | — | theory | a6c4c4e6f |
| CFG542 † | one dissipative principle | "CONSISTENT WITH OPEN ITEMS" | Q DERIVED = ρ_c α τ_ff 1_B 1_C ∇ψ·∇Φ | α free | 92c45e9fc |
| CFG543 + add. † | group supply gap | addendum: "groups RESOLVED (Tian M_bar includes X-ray gas; consistent supply closes at every radius conversion)" | — | paper text fetched outside git | d78e674c9 / 0ba52614a |
| CFG544 † | kinetic consistency of class A | "As frozen NO LABEL" (assessment: "class A kinetically inconsistent; velocity relaxation passes but posited") | — | — | c2be5aa17 |
| CFG546 † | drained shell vs splashback | "TEST NOT RUN; no candidate at Z >= 3; one MARGINAL" | D2 DES-Y3 redMaPPer Z 2.06/2.19 (forecast) | forecast | c8ea4c91d |
| CFG547 † | cosmic-time triangulation | a₀/cH "TAUTOLOGICAL" (0.143 today, 0.014 at z=6) | — | descriptive | 638450256 |
| CFG548 † | LG zero-velocity surface | "NOT DIAGNOSTIC, shared timing-vs-flow tension with LCDM" | M_flow 1.12e12, R0 830 kpc | — | 1d901b57d |
| CFG549 † | predict ρ_DE(z) | "Only Lambda plus an unobservable settling trickle" | — | firewalled, hashed | 0dfb051c9 |
| CFG550 † | velocity part from a principle | (Theory v1) "derived law-temperature target fails; self-consistent Jeans target is the open step" | — | theory | ac69319c9 |
| CFG551 † | splashback shift | "NOT DIAGNOSTIC (data precision), FEW MEASUREMENTS" | Z +1.11 can / +0.81 alt | K-S0 FAIL (mesh) | b96cdd186 |
| CFG552 † | DES cluster ΔΣ | "BLOCKED" | — | data not public | 1b1b912a2 |
| CFG553 | sealed Gaia DR4 MW predictions | SEALED | sha256 f8bea44f… | release 2026-12-02 | 8fb1f2c62 |
| CFG554 † | self-consistent Jeans target | "NO LABEL (control C6 fails …)" | — | — | f0e7065ff |
| CFG555 | growth on the gravitating field | "PAPER45 growth claim FAILS ON GRAVITATING FIELD at 512^3" | 0.15–0.19 | supersedes PAPER45 v2.0/2.1 growth; PAPER45 v2.2 DOI 23240863 | 71f3fc4d9 / 24eff06fa |
| CFG556 † | halo-model matter power | "INTRINSIC on both footings (VARIANT-SENSITIVE …)" | — | halo model = context per 10-10 rule | 038221231 |
| CFG557 † | catchment derived | (assessment) "catchment not derivable; finite-age ceiling halves growth excess but fails" | — | — | c608430ba |
| CFG558 † | velocity isotropy | "ISOTROPY CHOSEN" (Theory v1: "overfill rule fails; not alpha-robust; FIX-2 stays posited") | — | — | 415e3dc85 |
| CFG559 † | kinetic settled profile | (assessment) "kinetic settled profile does not resolve growth vs KiDS" | edge softens +26..+72% in r_99 | — | ad69978d1 |

### 1b. CFG579–602 and CFG700 (owner chat for 579–589 and 700; orch for 590–599; 600–602 as labelled)
| ID | question | frozen label (verbatim) | key numbers | caveats | commit |
|---|---|---|---|---|---|
| CFG579 † (owner) | KiDS N/S split of the census-edge fail | "LOW POWER as frozen" | — | needs DES Y3 | fb20f21aa |
| CFG580 † (owner) | hidden hot gas | "ESCAPE OPEN as frozen" | — | then closed by 581 | 187dd02c1 |
| CFG581 † (owner) | can it persist | "ESCAPE UNPHYSICAL as frozen" | — | — | 0c288d4cf |
| CFG582 † (owner) | cool CGM | "RULED OUT as frozen" | COS-LRG 1.5(+0.7/−0.3)e10 | — | 8e9d06303 |
| CFG583 † (owner) | residual vs baryon mix | "NO RELATION as frozen" | — | — | f56c5ad23 |
| CFG584 † (owner) | residual vs M_b | "CONTRADICTED as frozen …, marginally" | — | — | f0bad3adf |
| CFG585 † (owner) | old vs young early types | "NOT CONFIRMED [LOW POWER] as frozen" | — | — | 2336bd045 |
| CFG586 † (owner) | environment? | "AGE SIGNAL SURVIVES as frozen" | — | superseded in standing by CFG667/669 | 1be8e7e5f |
| CFG587 † (owner) | ACE colour clock | "UNDECIDED as frozen" | — | — | 9a6efc81e |
| CFG588 † (owner) | within-class clock | "SPLIT as frozen …, on a threshold edge" | slope +1.9–2.05 per mag | — | e7bd0a443 |
| CFG589 † (owner) | late-type clock, matched mass | "UNDECIDED as frozen" | early clock Z +3.44 | — | b06d4afb3 |
| CFG590 † | P(k) vs shear A_mod (HMcode) | was "current settling rules EXCLUDED by cosmic shear at equal feedback (Z 5.3 / 8.2)" | — | **downgraded to CONTEXT** (owner raw-data rule, b5cf2ade2) | e0d4655af |
| CFG591 † | z-dependent R(k) | "alt EXCLUDED, canonical NOT DIAGNOSTIC; NO LABEL by HZ1" | — | context only (59ab94e03) | 83ebd41c6 |
| CFG592 † | real shear likelihood | "NOT DIAGNOSTIC on every track by the declared rules" | native Δχ² +23.85/+4.20 can, +30.04/+5.56 alt | HMcode track = context | 6c201b673 |
| CFG594 † | halo-assumption audit | 59 ingredients: DATA-FORCED 10, FRAMEWORK-DERIVED 13, LCDM-INHERITED 17, STANDARD-MOND-INHERITED 7, CONVENTION 12 | — | audit | 4a00ca5b0 |
| CFG595 † | measured cold supply | "MEASURED SUPPLY LARGER, not smaller" | Q 2.26 (can) / 2.12 (alt) | "NOT CONVERGED" | ee02f6513 |
| CFG596 | native 1024³ shear | "EXCLUDED (dchi2 +68.7; robust min +43.9; T-OWN pass; NZ1 bites). DES Y3 dchi2 +22.4 NOT DIAGNOSTIC" | own boost 1.19/1.25/1.21 | **relative** classifier; ΛCDM-input conditional; **alt (P2) not completed** per CFG678 | 41efda383 |
| CFG598 † | settling front, partial | "ONE-alpha PARTIAL SETTLING DOES NOT WORK" | — | ID collision → other lane renamed CFG620 | 0a867f5c4 |
| CFG600/601 † | KiDS catchment / SHMR | CFG600 "VOID by frozen MU1/MU2"; CFG601 "SHMR swap immaterial" | — | — | 3bcb88095 |
| CFG602 † | ALPAKA JWST RAR | "NOT INFORMATIVE for a0" | — | K1 failed | 4e9e250d5 |
| CFG700 (owner) | age signal, raw lensing | "AGE SIGNAL ON RAW DATA" | ×1.46, A +0.166, Z +2.33 | "colour-dependent stellar-mass bias not excluded"; later read as M* artefact (CFG667/669) | 2f560b9dc |

Task-runner block CFG603–619: **nothing on origin/main or any origin branch** carries these IDs.

### 1c. CFG620–657 (orch unless marked)
| ID | question | frozen label (verbatim) | key numbers | caveats | commit |
|---|---|---|---|---|---|
| CFG620 † | anisotropic velocity target | (Theory v1) "passes by the age at alpha>=1; frozen label INCONSISTENT on 10-Gyr steadiness" | — | renamed from CFG598 | 166840941 |
| CFG621–623 † | merger stopwatch v3–v5 | CFG623 step 1 hypothesis "NOT CONFIRMED" | — | α verdicts "provisional" | cadc71eef / 1539fd142 |
| CFG624 (owner) | no-cold-energy universe | G1 SPARC PASS; G2 X-COP FAIL; G3 Bullet EXCLUDED; G4 LG timing FAIL | rms 0.1003/0.1013; M_HSE/M_NCE 1.82/1.68; Z_B +7.87/+7.88 | — | 9f625b5e2 |
| CFG625 † | merger baryon inputs | "NO VARIANT TESTED" | — | — | d04731da7 |
| CFG626 † | kernel recheck of CFG620 | "KERNEL-DEPENDENT (both footings)" | — | — | 7896a9bee |
| CFG627/633 † | Keating clue; Nature reads | read-and-map notes | — | context | bb7f1e086 / b554a8cd3 |
| CFG628 † | FRB halo partition | "NON-DIAGNOSTIC on both footings"; "MUTATE control is NOT detected" | — | — | 800f8153d |
| CFG629 † | cluster supply check | withdraws "law cannot reach the core mass" | main 0.33 → 0.84 | — | bc78a0f9c |
| CFG630 † | settling feeds DE | Δρ_DE/ρ_DE0 since z=1 = 0.98–1.10e-6 / 1.12–1.25e-6 | Q(0) 7.4–7.9e-34 W/m³ can | "untestable by 4-5 orders" | 9dc98d1a8 |
| CFG631 † | residual search | "Discs INCONCLUSIVE"; "KiDS early-type age signal holds, fw p 0.035" | — | age reading later NOT ROBUST | f97419fb2 |
| CFG632 † | FRB DM scatter | "CONSISTENT with 114 raw FRB DMs both footings" | — | **downgraded to CONTEXT only** (Tinker HMF etc.; 79e803632) | 43a3e6622 |
| CFG634 † | condensed-baryon source H-CB | "NOT DECIDED (reservoir-limited)" | T2 +0.067/+0.050 | — | 7a8d9f042 |
| CFG635 † | one dark sector | "No single field does both jobs without knobs" | mass ratio 1.4e13 | — | d1fc69b9f |
| CFG636 | H-CB native 1024³ | "EXCLUDED narrowly" | Δχ² +13.97 (CFG596 +68.73); robust min +9.19; DES +7.01 NOT DIAGNOSTIC; boost 1.058/1.056/1.056; growth benchmark G 0.089 | relative; tests a "uniform 10% census cap, not a phase-sensitive source" (6815ab246) | 54c6a393f |
| CFG637 † | derived reservoir | (assessment) "no single rule passes groups+X-COP+Bullet; B's cluster pass rested on the RI convention; H-CB gets inner clusters and Bullet main, short at R200" | — | — | e56fe96ba / 1667f7ee5 |
| CFG638 † (owner) | cold-energy fluid equations | "Sympy 11/11 PASS" | — | derivation | 28ce71974 |
| CFG639 † (owner) | deficit-gated mobility | "Part A … NOT DIAGNOSTIC as frozen" | dD 0.0094 < 0.02 | — | 0ff0121fd |
| CFG640 | phase-source PM | engine validated, queued; **H1 ABORTED by swap guard** | — | rerun pending | 6b8a3776c / 8dc870744 |
| CFG641 (owner) | H-CB + gate merger | running (renamed from CFG640) | — | — | 74f5b31eb |
| CFG642 | Ω_c/Ω_b symbolic regression | "CHANCE-LEVEL" | target 5.364 ± 0.065; clean best 16/3 "fails the BBN D/H omega_b check (z -1.8)" | — | fb0d1172d |
| CFG643 | baryon heat exchange | "CLOSED on both footings" | C 0.22/0.075/0.22 can | — | 05a464d08 |
| CFG644 | neighbour-bounded edge | "RULED OUT" | — | — | 959fd0fb1 |
| CFG645 | energy-bounded settling | "NOT DERIVABLE KNOB-FREE" | C/E_Φ ≥ 8.0e3 | — | 0a09db487 |
| CFG646 | KiDS anatomy + gas expulsion | "Expulsion is a FEW-PERCENT effect; CFG596 verdict unchanged" | k<1 share +52.1 of +68.726 | native run NOT RUN | 41a9dd3a9 |
| CFG647 † | accounting audit | (assessment) "no PM bug; supply pooling across overlapping catchments worth ~1/3 of the excess" | — | — | 5f01217e8 |
| CFG648 | phase-mixed settling H-SP | "FAILS for both sources" | settled 0.73 of B | combined run → T1x | 1d3520b44 |
| CFG649 | CMB safety | "SWITCH-OFF CONFIRMED, no loophole"; CMB lensing conditional +1.3% (candidate B canonical) | log10 N = −1232 | in-box switch-on not measured | 966658646 |
| CFG650 | Theory v2 combined PM | "No verdict yet"; 256³ PREVIEW "NOT a verdict" | M1+M2 ΔP_grav/P_S0 +0.005/+0.014/+0.031 | T12 = "POST-PREVIEW selection" (addendum A1); T1 primary | d0f8d3f38 / c1c03ad5b |
| CFG651 | A5 vs age signal (POST-HOC) | "FAILS to predict … WRONG SIGN" | A_pred −0.061/−0.061 vs +0.166 ± 0.071 | post-hoc; signal itself later NOT ROBUST | 97f815fd4 |
| CFG652 | hot-group discriminator | THEORY (no data touched) + criteria; test running | — | — | bc0dd7975 / 11c7906ef |
| CFG653 | nonlocal filter length L | criteria only; running | — | — | d44fee295 |
| CFG654 | independent native inputs | "No verdict here"; README RESULTS_PLACEHOLDER | ω_b 0.02193 (BBN), ω_c 0.1202, implied linear σ8 0.827 | 256³ validation running; 1024³ NOT started | 293f7a87b |
| CFG655 | NGC 1052 trail supply | "PASS CONDITIONAL ON THE FORMATION-CHANNEL LABEL" | debris Z +0.37/−0.30/−0.44; Newton fails LEDA +3.11 | the label is external | ec4a7d14d |
| CFG656 | X-COP native supply | criteria only; running | — | — | c1236bf88 |
| CFG657 | trail capture rule | "BRACKET-DEPENDENT; KNOB (alpha), both footings" | f_cap DF2 0.076/0.052 … LEDA 0.335/0.242 | knob | 3e8e03c53 |

### 1d. CFG660–679 (owner chat 660–669; Lean/GW chat for the aliases CFG670–674 and for 675–679)
| ID (alias) | question | frozen label (verbatim) | key numbers | caveats | commit |
|---|---|---|---|---|---|
| CFG660 (owner) | law as cold energy's stress equilibrium | anisotropic = law; "isotropic EoS EXCLUDED" | rms 0.1766/0.1870 vs 0.1003/0.1013 | sector ill-posed (WKB √k) | 53e9e6e56 |
| CFG661 (owner) | compression-responding stress | "NO-GO (local, first-order, spherical, {G, a0})" | — | theorem | 1c7839dfe |
| CFG663 (owner) | lensing fork | "H-NL (response does not lens) EXCLUDED on both footings" | +0.155/+0.158 dex | — | f5a9d1fe5 |
| CFG665 (owner) | isothermal selector | "VOID as frozen" | σ⁴ +4.96 dex | post hoc: no regular solution | 73daa549e |
| CFG666 (owner) | dark-energy clock | "SHAPE DISFAVOURED on raw SPARC" | alt −0.063; can TENSION −0.042 | — | 0769d53dd |
| CFG667 (owner) | KiDS age anatomy | "STELLAR-MASS ARTEFACT LIKELY" (Part A NOT DECIDED; Part B "M* BIAS EXPLAINS") | A_T +0.032 ± 0.080, Z +0.40; OLD−YOUNG +0.123 dex | MUTATE M2 "does not bite" | bb1ba0729 |
| CFG668_early_type_rescore (owner) | early-type excess, Taylor masses | "ARTEFACT EXPLAINS THE EXCESS — but the frozen matching control failed …" | LePhare +0.308 (Z 3.41) → Taylor +0.185 (Z 1.70) | corrected by CFG669 | 1be76f204 |
| CFG669_nearir_mass_rescore (owner) | Ks masses | T1 "PARTIAL"; T2 "EXCESS PERSISTS"; combined "NOT ROBUST" | T1 +0.082 ± 0.089 (Z 0.93); T2 +0.280 ± 0.083 (Z 3.37) | — | 600c41c1e |
| CFG670 (dir CFG665_gw_messenger_lean) | GW messenger theorems | "CERTIFIED in Lean, zero sorry, standard axioms (14 theorems)" | light delay ≥ 2.36e6 s can / 2.60e6 s alt | T3 kernel form corrected in 5e0b67a13 | aeff2112a |
| CFG671 (dir CFG666_lens_perturbers) | strong-lens perturbers | "NOT DIAGNOSTIC (model-selection-limited)" | J0946 dark ×13.5/×13.3 the light limit → EXCLUDED as dark object | — | bf98ea04d |
| CFG672 (dir CFG667_j0946_jwst_prereg) | J0946 GO 12088 | SEALED | sha256 7c3029fa… | unobserved | 52f4363bf |
| CFG673 (dir CFG668_b1938_jwst_prereg) | B1938 A GO 8281 | SEALED | sha256 9162427f… | — | 90c0618be |
| CFG674 (dir CFG669_b1938_A_photometry) | own photometry, parts 1–3 | "NOT DIAGNOSTIC" (each part) | F115W perfect-model floor 31.4 AB | part 4 PyAutoLens fit running | 9d982d94f / 1f548f8a8 / d199d99b1 |
| CFG675 | no BH cold-energy spike | SEALED | sha256 d153665c…; v2 dephasing 1.6e-4/1.9e-4 cycles | v1 kernel error corrected | e12d4881d / 5e0b67a13 |
| CFG676 | a₀-siren relation | SEALED | sha256 9defe322…; DESI w0wa: +0.01/+0.04 dex z 0.5, −0.06/−0.07 z 2, −0.11/−0.15 z 3 | — | 634f276da |
| CFG677 † | GW question forecasts | result in 5e0b67a13 | — | — | 5e0b67a13 |
| **CFG678** (one_action_contract) | one-action scorecard | "NO candidate passes the contract" | MUTATE Newton rms 0.2755 > 0.110 | two citation corrections | 2ddb9c4ad |
| **CFG710** (dir CFG678_b1938_lens_structure) | blind B1938 mass structure | SEALED | γ_eff(θ_E) 2.30 can / 2.23 alt (pure stars 3.26); mass PA 130.4 ± 10°, q_M 0.79–0.89; m=3,4 ≤ 0.02; sha256 ef0a780b… | the duplicate ID was resolved forward by the LEDGER alias (block CFG710–719) | ef9d750d0 / 0b259107d |
| CFG679 | mechanism contract | Part 2: "Controls K1-K4 all fail as required"; "15 candidates: none passes" | — | — | 11629ff57 |
| TOE_BEST_ATTEMPT (Lean) | what the record forces | v2: "19 theorems, 0 sorry, standard axioms only" | 5.788 < Z < 5.789; a₀(z)/a₀(0) = √(ρ_DE ratio), flat for w = −1 | **v2 reverted to v1 on origin/main**: 5e0b67a13 rewrote the file; `git diff 5cc389f49 origin/main` on it is empty and it has 13 theorems, so main carries v1's wrong "uninhabited" wording. See §7 | 5cc389f49 / 40657f946 |
| CFG692 | gravitating polarization (the bound charge div P as the cold mass) | FROZEN CRITERIA only | — | new, 22:15 | 097b2feee |

### 1e. CFG680–691 (BAO chat for 680–685; 690–691 owner-approved block, chat as in commits)
| ID | question | frozen label (verbatim) | key numbers | caveats | commit |
|---|---|---|---|---|---|
| CFG680 (dir CFG668_count_magnification) | counts behind clusters | SDSS "NOT DIAGNOSTIC"; A1 "LENSING NOT DETECTED as frozen"; A2 "NOT DETECTED as frozen"; A3 "NULL" | κ(8–40′) < 0.0026 (2σ); A3 K = +0.0008 ± 0.0021 | law amplitude not frozen ("~1.5 sigma above") | 33ff902b3 / 3698e6452 / 6d14c0450 / a5b5c1f87 |
| CFG681 | BAO from raw distances | T1 fine (Δχ² 7.4/5, 1.3σ); T2 "HINT (12.1/5, 2.1 sigma)" | raw BAO cannot fix a₀(z) without an independent Ω_m | — | e6d43c49a |
| CFG682 | a₀(z)+BAO → Ω_m | "0.65 sigma, CONSISTENT" | Ω_m = 0.3085 ± 0.0075 vs Planck 0.3153 ± 0.0073 | "perfect a0"; MUTATE PARTIAL | 468748e2e |
| CFG683 | separate tracking vs a₀ ∝ H | rival pinned "to +-1.5%"; tracking "Omega_m-degenerate" | gap 0.13–0.20 dex | "no record sample decides the fork" | 0568d6fa4 |
| CFG684 | CC + SN swaps | "dark degeneracy NOT broken (dchi2_max <= 1.7)"; flat-a₀ Ω_m "ROBUST" | 0.3082/0.3070/0.3154 | — | 0a580fd32 |
| CFG685 | deciding sample | "NONE among public data" | best e 0.4–0.5 dex vs 0.15 | proposal spec only | 0a580fd32 |
| CFG686–689 | — | not on origin/main | — | — | — |
| CFG690 | origin of the cubic | "cubic R0-SHAPED, REDUCED, R0 still not passed"; γ=0 interpolation on SPARC "FAIL (post-hoc …)" | rms 0.1012/0.1007, Υ_disk 0.46/0.42 | — | 9b2d40d35 |
| CFG691 | stiffness window | "WINDOW OPEN, CONDITIONAL on a disclosed K1 criteria error" | L* ≥ 5.75 pc; SPARC unaffected to ≥ 1000 pc | "Never a C2 pass"; galactic EFE not modelled | d7c9b9a25 |

---

## 2. What is established on raw data

**Passes and consistents** (verbatim labels):
- SPARC RAR: G1 PASS, rms 0.1003/0.1013 (CFG624). Also CFG678 C2 PASS, ν_mono 0.1003/0.0991 ≤ 0.110 (CFG4).
- Tian groups: "groups RESOLVED" (CFG543 addendum).
- Local Group timing with cold energy: the no-cold-energy universe fails it (CFG624 G4), so this pass is conditional on cold
  energy.
- Primary CMB: "SWITCH-OFF CONFIRMED" (CFG649).
- Flat-a₀ Ω_m from CMB-free BAO: "CONSISTENT" (CFG682) and "ROBUST" (CFG684).
- NGC 1052 trail: "PASS CONDITIONAL ON THE FORMATION-CHANNEL LABEL" (CFG655).
- Context only, by the owner's 10-10 rule: CFG632 FRB "CONSISTENT"; CFG590/591 HMcode shear.

**Fails, exclusions and tensions:**
- Raw KiDS shear: candidate B "EXCLUDED" Δχ² +68.7 (CFG596); capped H-CB "EXCLUDED narrowly" +13.97 (CFG636). Both labels are
  relative, and both are conditional on ΛCDM inputs (§4).
- Massive early types: CFG529 FAIL; escapes closed (CFG580–582, CFG644). CFG669 T2 "EXCESS PERSISTS" (Z 3.37, Ks).
- The no-cold-energy universe: X-COP FAIL, Bullet EXCLUDED, LG FAIL (CFG624).
- The non-lensing response sector: "EXCLUDED" (CFG663).
- Isotropic stress: "EXCLUDED" on SPARC (CFG660).
- The dark-energy clock: "SHAPE DISFAVOURED" (CFG666_dark_energy_clock).
- PAPER45 growth: "FAILS ON GRAVITATING FIELD at 512^3" (CFG555).
- J0946 dark solution: "EXCLUDED as a dark object" under the law (CFG671).

**Not diagnostic:** CFG548, CFG551, CFG592, CFG628, CFG671 (overall), CFG674, CFG680 (counts), CFG585 (LOW POWER).

**Evidence dossier** (2f3e1a1f6): "14 pass/consistent incl. conditional, 18 fail/excluded/tension incl. 5 excluded variants +
1 benchmark, 16 not diagnostic/context".

---

## 3. What each chat's latest results imply for Theory v2 (THEORY_v2_CANDIDATE_2026-10-12.md, aa8a34383)

### 3a. Agreements and contradictions

**Agreements:**
- CFG663 (the response must lens) supports A7.
- CFG649 supports the primary-CMB row.
- CFG682/684 are consistent with A4 at today's Ω_m.
- CFG670 (Lean) requires one shared metric; Theory v2 adds no second metric.
- CFG636 and CFG646 match the §4 figures (+14.0; expulsion ~¼).

**Contradictions or tensions:**
- **Age signal.** §5 and §8.4 treat the early-type age signal as a real effect that "any mechanism must overcome". CFG667 and
  CFG669 now read it as "STELLAR-MASS ARTEFACT LIKELY" / "NOT ROBUST". CFG651's wrong-sign result is therefore a constraint
  only if the signal is real.
- **Matched-mass excess.** The excess persists (CFG669 T2) and stands as CFG678 C3 FAIL. Theory v2's §5 does not list C3.
- **Ω_c/Ω_b.** CFG654's native inputs imply 5.481, not 5.364 (reconciled in §8.1).
- **Shear wording.** CFG596/636 "EXCLUDED" and the T12 kill line are relative labels. The absolute χ² must be reported too
  (eb4f5af3a).
- **Mechanism side.** CFG678 does not score Theory v2 itself. B1, B3/A2, C3 and D2 are open for it by the same reasoning
  (CFG678: "An action that only formalises B would inherit both failures").
- **Receiver.** The cited ghost-condensate receiver is a "sketch for export only" (CFG635 assessment, 6bc0e8e4e). CFG679 Part 2
  found no catalogue mechanism that passes.

### 3b. Proposed Theory v2 edits (not applied)
| # | location | proposed text change | status |
|---|---|---|---|
| (a) | status line; §6 row 1 | call T12 "POST-PREVIEW selection (CFG650 addendum A1, c1c03ad5b); T1 (M1+M2+M3+M4) is the primary pre-declared run" | **VERIFIED** (addendum text) |
| (b) | §4 row 2 | label "256³ preview M1+M2 within +0.5–3.1% of S0" as "PREVIEW, benchmark against the inherited-input S0, not a verdict" | **VERIFIED** (CFG650 README: "NOT a verdict"; addendum A1) |
| (c) | §5 open list; §8.4 | replace "age dependence in early types (CFG585/631/700 …)" with "early-type age signal NOT ROBUST (CFG667 'STELLAR-MASS ARTEFACT LIKELY'; CFG669 T1 'PARTIAL', combined 'NOT ROBUST'); CFG651's wrong-sign result binds only if the signal is real" | **VERIFIED** (CFG667/669 READMEs) |
| (c′) | §5 failing list | add "massive early types at matched baryonic mass: EXCESS PERSISTS on Ks masses (CFG669 T2 +0.280 ± 0.083, Z 3.37); CFG678 C3 FAIL (CFG529)" | **VERIFIED** |
| (d) | A3; §3 eq. 3 | state which Ω_c/Ω_b each run uses: 5.364 (Planck ω_b 0.02237, ω_c 0.1200; CFG650 inherited) vs 0.1202/0.02193 = 5.481 (CFG654 native: FB = ω_b/(ω_b+ω_c) in cfg654_pm.py). Quote CFG642's 5.364 ± 0.065 | **VERIFIED** (code lines read; cfg654_ics.out prints "omega_c/omega_b 5.4807"; CFG656 FROZEN_CRITERIA says "cold/b 5.481"). The reconciled recommendation is in §8.1 |
| (k) | §3 eq. 9 | relabel eq. 9 as "an AQUAL-family representation of the law; it has an external-field effect and its ρ_eff is inferred from Φ, not an independent substance (astra FIELD_ORIGIN b77b37018; RIGOROUS_AUDIT dc37c12f1: 'refuted for this candidate under the exact no-external-field requirement'). It is in tension with A8 unless the nonlocal filter route (87f8ae5a9, new length L; CFG653) works" | **VERIFIED** (astra inventory quotes) |
| (l) | §3 eq. 6 | replace "Q … ≥ 0" with "Q's sign is not established: the v2 REVIEW gives a counterexample, and the IC-B and IC-C benchmarks need exchange of opposite signs (21d6bb2fe). A strictly constant vacuum cannot accept nonzero Q" | **VERIFIED** (paper/v2_release_2026-10-12/REVIEW.txt; MASTER Supplement C) |
| (m) | §6 new row | "finite supply forces an outer edge r ≤ (1+S/M_d)√(GM_d/a₀) (Lean `supply_radius_bound`, 33ec30852; audit §8); predicted per host from eq. 3" | **VERIFIED** (Lean README line quoted by the astra inventory) |
| (n) | §5 passes | the SPARC entry should carry astra's own caveat: "agreement with observations, but not independent validation … No model-selection significance follows"; the exponential kernel gives 0.13714 vs 0.13712, so the data show no preference for the repaired kernel | **VERIFIED** (cold_production/empirical_2026_10_12/EVIDENCE.md, 0b6b4e567) |
| (o) | §5 passes ("Tian groups") | add CFG540's frozen labels: GROUPS "ABOVE LAW / ABOVE LAW" (+0.153/+0.145); ELLIPTICALS "ABOVE LAW". The groups pass is the CFG543 addendum reading ("MECHANISM FOUND (progenitor containment) + NOT DIAGNOSTIC trigger", frozen text unchanged); "groups RESOLVED" is the assessment's wording, which is stronger than the frozen label | **VERIFIED** (CFG540/543 inventory) |
| (e) | §6 row 2 | "a₀ ∝ √ρ_DE(z): flat for constant ρ_DE (TOE_BEST_ATTEMPT: 'flat for w=-1'); with DESI DR2 w0wa it moves +0.01/+0.04 dex at z 0.5 and −0.06/−0.07 at z 2 (CFG676 sealed). CMB-free BAO pins the rival a₀ ∝ H(z) to ±1.5% but leaves tracking Ω_m-degenerate (CFG683/684)" | **VERIFIED** (commit messages 634f276da, 0568d6fa4, 0a580fd32, 5cc389f49) |
| (f) | new line in §5 or §8 | "CFG678 has not scored Theory v2; gates B1, B3/A2, C3, D2 are open for it" | **VERIFIED** (SCORECARD lists only CH, B, CE) |
| (g) | A7 status | add "the response must lens: H-NL EXCLUDED both footings (CFG663)" | **VERIFIED** (f5a9d1fe5) |
| (h) | §5 scoreboard | add "NGC 1052 trail: PASS CONDITIONAL ON THE FORMATION-CHANNEL LABEL (CFG655); capture rule BRACKET-DEPENDENT; KNOB (alpha) (CFG657)" | **VERIFIED** (ec4a7d14d, 3e8e03c53) |
| (i) | §3 eq. 6 / §8.3 | add context: "astra stiff sector: WINDOW OPEN, CONDITIONAL on a disclosed K1 criteria error (CFG691); cubic R0 still not passed (CFG690)" | **VERIFIED** (d7c9b9a25, 9b2d40d35); context, not a pass |
| (j) | §5 and §7 | "shear labels are relative; report absolute KiDS χ²/p (S0 144.3, p 0.014; CFG636 158.2, p 0.002; CFG596 213.0, p < 0.001)" | **VERIFIED** (eb4f5af3a) |

---

## 4. Open gates ranked (CFG678's 20-gate backbone; every lane mapped)

Rank 1 is the most binding: a data failure that no candidate passes.

| rank | gate | status for B / CE / chassis (CFG678) | lanes mapped |
|---|---|---|---|
| 1 | **D2 growth vs raw KiDS/DES** | B FAIL canonical; alt not completed | CFG596, CFG636, CFG646, CFG647, CFG648, CFG650 (T12/T1 queued), CFG654 (native rerun frozen), CFG640, CFG590–592 (context), CFG555/556/557/559, CFG594/595, CFG600/601. Caveats: relative label (d992929b9); ΛCDM inputs (5c31fcad4) |
| 2 | **C3 massive early types** | FAIL (B, chassis) | CFG529, CFG579, CFG580–582, CFG644, CFG585–589, CFG631, CFG651, CFG667, CFG668_early_type_rescore, CFG669_nearir_mass_rescore, CFG700, CFG679D (untracked DES Y3, running) |
| 3 | **B3/A2 cold-energy sector** | CE FAIL; B via CE | CFG660, CFG661, CFG663, CFG665 (owner), CFG635, CFG638, CFG639, CFG641, CFG643, CFG645, CFG653 (running), CFG690, CFG691, CFG679; astra polarization/nonlocal/stress/receiver reports (§6) |
| 4 | **B1 switch from variation** | NO CONSTRUCTION (CFG48) | CFG542, CFG544, CFG550, CFG554, CFG558, CFG620, CFG626 |
| 5 | **C4 lensing beyond baryons** | NOT DECIDED | CFG680 A3/A3G, CFG663, CFG671, CFG546, CFG551, CFG552 (blocked) |
| 6 | **D3 flat a₀(z)** | PENDING (2026-11-06, 11-28) | CFG570/571, CFG547, CFG549, CFG602, CFG676, CFG681–685 |
| 7 | **B2 a₀–Λ tie** | UNTESTED | CFG630, CFG635, CFG642, TOE_BEST_ATTEMPT |
| 8 | A1/A3/A4/A6 structure | B UNTESTED (no action) | — |
| 9 | A5 GW | chassis PASS; constraint on CE | CFG670, CFG675, CFG677 |
| 10 | C1 Cassini | chassis COND | CFG691 (L* window) |
| 11 | C2 SPARC | PASS | CFG624 G1, CFG660, CFG666_dark_energy_clock, CFG690, CFG583/584/631 |
| 12 | D1 zero field | chassis FAIL; B UNTESTED | CFG468 |
| 13 | A7, E1–E3 | DECLARED | TOE_BEST_ATTEMPT (E1: Z² irrational) |

Cluster and merger lanes (CFG621–625, CFG629, CFG634, CFG637, CFG655–657, CFG624 G2/G3) have no CFG678 gate. They test the
supply/reservoir rules directly and should become a gate in the next contract revision.

---

## 5. Running and queued jobs (seen with ps on 2026-10-12; read only, nothing touched)

| job | state | next |
|---|---|---|
| CFG650 T12 (M1+M2, canonical, 1024³) | waiter running; starts when free+inactive ≥ 48 GB (handoff 8dc870744) | then T1 chained; T1x if the CFG648 clause applies; score with `CFG650_JOBSET=T12` MUTATE first |
| CFG654 native rerun (N12 + NS0) | 256³ validation running (cfg654_pm.py S0 canonical 256); README RESULTS_PLACEHOLDER | 1024³ NOT started; criteria e7bc41fb9 |
| CFG640 H1 | ABORTED by swap guard (+4.5 GB) | rerun after moving H1 aside |
| CFG596 alt (P2) | per CFG678 "alt not completed" | rerun queued per handoff |
| CFG636 alt C2 | "by hand later" (handoff) | — |
| CFG641 merger (owner) | running | — |
| CFG652 test, CFG653 filter, CFG656 derive | running | criteria committed (11c7906ef, d44fee295, c1236bf88) |
| CFG674 part 4 PyAutoLens | running | criteria c29c55493 |
| "CFG679" DES Y3 early-type shortfall | running (cfg679_probe.py) from an untracked directory, CFG679D_des_y3_early_type_shortfall; **no committed criteria** | see §8.4 |

---

## 6. astra / codex (sol61_push, paper/v2_release_2026-10-12), committed verdict lines

| item | commit | committed status line (verbatim) | bearing on Theory v2 |
|---|---|---|---|
| ΛCDM dependency audit (sol61_push/lcdm_dependency_audit_2026_10_12/RESULT.txt) | 5c31fcad4 | "Primary verdict: correct only after a stated restriction."; "The 10% control-spectrum gate is a benchmark, not a raw-data exclusion." | accepted (e1524b26a); Theory v2 §5 "Conditional on" line already cites it |
| v2 independent audit (paper/v2_release_2026-10-12/INDEPENDENT_TEST_AUDIT.txt) | d992929b9 | "DECISIVE FINDING: THE LABEL IS RELATIVE, NOT ABSOLUTE"; "It turns finite supply into an explicit prediction obligation" | accepted (eb4f5af3a) → edit (j) |
| MASTER_COLD_ENERGY_EQUATIONS.md + scoped Lean certificates | 33ec30852 | consolidated equations; independence audit | the source of Theory v2 eq. 9 family; equations not re-derived here |
| COLD_ENERGY_MECHANISM.md (integrated account) | cc721354a | "Assemble cold-energy mechanism into an integrated theory account" | candidate account, not a verdict |
| nonlocal response | 87f8ae5a9 | "Test conservative nonlocal response and document cold-mass limits"; RESULT: "This bounds one box change; it is not an infinite-domain proof." | CFG653 (filter length L) is testing it |
| nonlinear sourced polarization | e1a69041a | "Solve nonlinear sourced polarization and audit finite-time formation failure" | B3/A2 lane (CFG678 brief 68cc91073) |
| profile robustness / EFE | dc37c12f1 | "prove external-field incompatibility of local response candidate" | consistent with A8 (no EFE) |
| phase-source discriminator | bd8981d3d | accepted: CFG636 tests "a uniform 10% census cap, not a phase-sensitive source" (6815ab246) | CFG640 carries the phase memory |
| FRB machinery review | a9bba9f84 | "Keep inherited FRB machinery outside native framework verdicts" | CFG632 → context (79e803632) |
| local sink reaction | b626126ed | "Audit local momentum reaction of a vacuum settling sink" | Theory v2 eq. 6: "passive vacuum excluded" |

More astra results, as committed:
- stress_closure RESULT (b22e3bb14): "NO." for local compressive support.
- Sourced polarization (e1a69041a): "Formation gate: FAIL" (25.74% force error).
- Gradual assembly (5869e2cdc): passes for 2 of 3 histories.
- receiver_capacity (957c4935d): "REGULARITY IS NOT REACHABILITY".
- regular_receiver_lift (9c7e7cb2e): a canonical receiver cannot cross w = −1.
- MASTER_COLD_ENERGY_EQUATIONS (33ec30852): "not a claim that a complete physical theory has been solved". It leaves the
  selector 𝒞_sel OPEN, and its 36 Lean theorems certify implications only.
- COLD_ENERGY_MECHANISM (cc721354a): "a candidate framework with explicit missing connections". Its carrier adds a species,
  which the record's no-particle rule does not allow inside the framework.

Astra marks these do-not-promote:
- "polarization waves export energy" → "cold matter settles into the law";
- the local polarization/AQUAL candidate as the full mechanism;
- CFG660's stress as "a new material";
- CFG632 FRB as more than context;
- CFG631 age as a formation mechanism.

Withdrawn or corrected:
- CFG635 K2 "spatial exchange exclusion withdrawn at the inference level";
- CFG428 thermal rejection has a "factor-1000 unit error".

---

## 7. Other conflicts and stale text found (recommendations; no other chat's file was edited)

| # | conflict | evidence | recommendation |
|---|---|---|---|
| 7.1 | TOE_BEST_ATTEMPT v2 silently reverted | 40657f946 (v2, 19 theorems) was overwritten at 21:28 by 5e0b67a13 (CFG675/677 commit, −74/+5 lines). The origin/main file equals 5cc389f49 and has 13 theorems | The Lean chat should restore v2 by a forward commit. Until then cite 40657f946, not the main-branch file |
| 7.2 | Shear "EXCLUDED/CONSISTENT" read as absolute | eb4f5af3a; INDEPENDENT_TEST_AUDIT §1. CFG636's +13.97 is "a difference of penalized objectives"; the data-only χ² is 138.12 (S0) vs 149.42 | Quote absolute χ²/p beside every label (edit j) |
| 7.3 | STANDING_2026-10-09_law says the law works for "large-scale growth" | superseded by CFG555 (10-10) and PAPER45 v2.2 | Do not cite that STANDING growth line |
| 7.4 | CFG636 README header still says "QUEUED"; CFG650 README says CFG649 has no checklist and the waiter is not started | both stale against later commits (54c6a393f, 966658646, handoff 8dc870744) | The owning chat should fix forward |
| 7.5 | CFG678 D2 cell scores candidate B with CFG596 (the v1 rule), not Theory v2 | SCORECARD D2 row | Re-score D2 for Theory v2 after CFG650 T12/T1 |
| 7.6 | Flat-a₀ Ω_m at the same reference configuration | CFG682 0.3085 ± 0.0075 vs CFG684 BAO+PP ref 0.3086 ± 0.0078 | Negligible; the BAO chat should state which one is canonical |
| 7.7 | Alt-footing SPARC rms | 0.0991 (CFG4 H2, cited by CFG678) vs 0.1013 (CFG660/CFG624 harness) | Two harnesses; cite each with its lane, never interchangeably |
| 7.8 | LEDGER gaps | no rows for CFG590–602, CFG620–630, 633–637, 649–654, 656, 657 | The orchestrator should add rows by a forward commit |

---

## 8. RECONCILIATION (verdict per conflict, with the evidence)

### 8.1 Ω_c/Ω_b: 5.364 vs 5.481

**Computed from the committed inputs** (tiny arithmetic, scratch only):

| input pair (ω_c / ω_b) | source | Ω_c/Ω_b | f_b | supply vs 5.364 |
|---|---|---|---|---|
| 0.1200 / 0.02237 | inherited constants (cfg596/cfg650_pm.py; Planck 2018 ΛCDM fit) | **5.3643** | 0.15713 | 1.0000 |
| 0.1202 / 0.02193 | CFG654 native mode (Planck TT,TE,EE+lowE ω_c with BBN D/H ω_b, Cooke+18) | **5.4811** (cfg654_ics.out prints 5.4807) | 0.15430 | **1.0218** |
| 0.1202 / 0.02236 | CFG654's own "omega_b_CMB" bracket with the same ω_c | 5.3757 | 0.15685 | 1.0021 |
| 0.1200 / 0.02193 | CFG642 BBN route | 5.472 (CFG642: 5.4715 ± 0.0770) | 0.15451 | 1.0201 |

- BBN ω_b (0.02193 ± 0.00022) vs CMB ω_b (0.02236 ± 0.00015) differ by **1.6σ**.
- 5.481 sits **1.8σ** above CFG642's 5.364 ± 0.065.

**Verdict.** Both numbers are computed correctly, and neither is an error. The conflict is that CFG654 mixes sources.
- Its ω_c comes from the CMB fit, in which ω_c and ω_b are fitted jointly.
- Its ω_b comes from BBN.
- That pair is not one measurement. Taken together they give an abundance (5.481) that no single dataset returns.

**What the framework should use for the supply.**
- **Primary: the self-consistent CMB pair.** Before any bound system exists, the switch is off (CFG649). The pre-switch CMB is
  therefore framework-native physics, as CFG654's own README principle says. Its jointly fitted pair gives 5.364 (2018 baseline)
  or 5.376 (CFG654's TT,TE,EE+lowE ω_c with its CMB ω_b).
- **Declared bracket: the BBN-ω_b ratio (5.47–5.48).** It should be quoted as a supply bracket, not used silently.
- Concretely: CFG654's native N12/NS0 run should either switch ω_b to the CMB value from the same column, or keep BBN and
  disclose in its README that the supply rises by +2.2%. This should happen before the 1024³ run starts. Its criteria are
  frozen, so this is a disclosure, not a change of rule.
- The astra ΛCDM audit's point stands: any CMB-fitted ratio is a "conditional inferred abundance". Theory v2's A3 wording
  "measured" should say "CMB-inferred, pre-switch".

**Impact on supply and settled mass.**
- Supply = ratio × catchment baryons, so it scales by **+2.2%** at 5.481 and +0.2% at 5.376.
- Settled mass = min(target, supply).
  - It is unchanged wherever settling is target-limited: galaxies inside the edge, and every SPARC/RAR gate.
  - It rises by at most +2.2% where settling is supply-limited: cluster outskirts, census edges, the X-COP R200 band.
- The X-COP R200 shortfall is 33–40% (Theory v2 §5, CFG637), so this choice cannot close it. Nor can it move CFG636/650 by more
  than a few percent of the own-boost excess.
- **Classification:** a disclosure item, not a verdict changer.

### 8.2 The KiDS early-type age signal (CFG585/586/631/700 vs CFG667/669)

**What each lane used.** All six lanes share the same KiDS f30 early types, CFG585's head and CFG531's `esd_loo` raw-ESD
estimator. They differ only in the stellar mass that defines "fixed mass":

| lane | mass that defines "fixed M*" | old/young result |
|---|---|---|
| CFG585 | LePhare | K9 D +0.941 ± 0.354 (Z +2.66, post hoc); K-in Z +1.51 → "NOT CONFIRMED [LOW POWER]" |
| CFG586 | LePhare | "AGE SIGNAL SURVIVES" (environment not the cause) |
| CFG631 | LePhare + partialled properties | "AGE CONFIRMED, HOLDS" (family-wise p 0.035); known-signal control FAILS |
| CFG700 | LePhare (CFG589 tertiles) | "AGE SIGNAL ON RAW DATA", A +0.166, Z +2.33; caveat in its own README: LePhare masses of the reddest galaxies may be biased low |
| CFG667 | Taylor+11 colour-M/L (independent) | OLD − YOUNG mass offset +0.123 dex; matched on Taylor A_T = +0.032 ± 0.080 (Z 0.40) → "M* BIAS EXPLAINS" |
| CFG669 | Ks light (constant M/L_K), on one common sample with LePhare and Taylor | LePhare +0.186 ± 0.081 (Z 2.29); Taylor +0.036 (Z 0.46); **Ks +0.082 ± 0.089 (Z 0.93)** |

**Verdict: NOT ROBUST.** The signal appears only with LePhare masses.
- On both independent estimators it falls below 1σ: Taylor Z 0.46, Ks Z 0.93.
- CFG700's own named nuisance (LePhare bias against the reddest galaxies) is the mechanism CFG667 measured: +0.123 dex.
- Ks is the least colour-dependent estimator, and its constant M/L_K biases the test **in favour of** an age signal. Older
  populations have higher near-IR M/L (CFG669 caveat), so constant M/L_K underestimates the OLD group's mass and inflates
  OLD/YOUNG. The Ks Z 0.93 is therefore if anything an upper bound.
- What is not shown: that the signal is zero. Ks +0.082 ± 0.089 is 1.2σ below the common-sample LePhare value, and CFG667's
  MUTATE M2 did not bite, so Part A is power-limited.

**Consequences.**
- CFG586/631/700 keep their frozen labels but are superseded in standing.
- CFG651's "WRONG SIGN" result binds only if a real signal exists, so it is now a conditional constraint.
- Theory v2 §5 and §8.4 should change per edit (c).
- The ACE model (MODEL_accumulating_cold_energy_2026-10-10) loses its motivating signal.

### 8.3 The early-type excess (CFG668 "ARTEFACT EXPLAINS", Z 3.4 → 1.7, vs CFG669 "EXCESS PERSISTS")

**What is the same.** Both use the same morphology-blind test: early vs late KiDS f30 lenses at matched baryonic mass, with
raw ESD from CFG585's head and CFG531's `esd_loo`, scored on K9. Both MUTATEs bite, and neither uses a ΛCDM ingredient.

**What differs.** Only the mass estimator and the matching:

| | CFG668 frozen | CFG668 post-hoc 40 bins | CFG669 (40-bin matching, one common sample) |
|---|---|---|---|
| LePhare | +0.308 ± 0.090 (Z 3.41) | +0.249 ± 0.103 (Z 2.40) | +0.249 ± 0.103 (Z 2.40) |
| Taylor+11 (optical colour–M/L) | +0.185 ± 0.109 (Z 1.70) | +0.181 ± 0.109 (Z 1.66) | +0.181 ± 0.109 (Z 1.66) |
| Ks light | — | — | **+0.280 ± 0.083 (Z 3.37)** |
| matching control (early − late median log M_b) | **FAILED**: max 0.161 (L) / 0.125 (T) dex vs 0.02 | mean +0.005 / +0.003 | Ks +0.001 / max 0.044 |

**Verdict: CFG669's reading holds, and the excess persists.** Four reasons:
1. CFG668's frozen label rests on a failed matching control. Its own README says the fine-bin diagnostic "does not support
   'explains'" and the excess is "not shown to vanish".
2. The drop from LePhare to Taylor comes from a colour-dependent estimator. Early and late types differ in colour by
   construction, so optical colour–M/L is the estimator most entangled with the class split. Taylor assigns early types
   +0.084 dex more mass relative to LePhare; Ks assigns −0.060.
3. On the least colour-dependent estimator, with the tightest matching (+0.001 dex mean), the excess is +0.280 ± 0.083,
   Z 3.37.
4. CFG669 explicitly "corrects CFG668's tentative softening".

**Remaining caveat.** CFG669 notes that constant M/L_K ignores the higher near-IR M/L of older populations, and that cuts
against the excess "plausibly by ~0.05–0.15, leaving it positive". That leaves about +0.13 to +0.23 dex, still positive.

**Consequences.** C3 stays FAIL (CFG678; CFG529; dossier F4). Theory v2 should list it (edit c′).

### 8.4 Duplicate IDs: CFG678 and CFG679

**CFG678: RESOLVED on origin/main.** 0b259107d, after this document's first draft, added LEDGER block "CFG710–719 RESERVED
(owner, 2026-10-12) for the GW/lensing-perturber chat" and the row "CFG710 = dir CFG678_b1938_lens_structure". CFG678 now
means only the one-action contract (72577e919 / 2ddb9c4ad). The directory name stays, fixed forward with no rename. No action
is needed beyond reading the LEDGER row.

**CFG679: OPEN.** The committed CFG679_mechanism_contract (8b77a75fc / 41ad7a730 / 11629ff57) holds the ID. A second lane is
running from an **untracked** directory, `CFG679D_des_y3_early_type_shortfall` (cfg679_probe.py, "CFG679D probe: HDF5
metadata of the DES Y3 public catalogues"), with no committed criteria.

Free numbers, checked against `git log --all` and the LEDGER:
- CFG603–619 are unused on every branch.
- CFG686–689 are unused but sit in the BAO chat's reserved block.
- CFG693–699 sit in the CFG690–699 block of the chat that holds CFG690–692.
- CFG711–719 are reserved for the GW chat.
- CFG720 and above are unused, with no reservation.

**Proposal** (no file renamed here):
- Before its FROZEN_CRITERIA is committed, the DES Y3 lane takes **CFG720**, with **CFG720–729 reserved** by a LEDGER row for
  the chat that owns it.
- If its owner is the Task-runner chat, it takes **CFG603** from that chat's unused CFG600–619 block instead.
- Either way, the directory should be renamed by its owner before first commit, so that no CFG679 alias is ever needed. Its
  scripts' internal "CFG679D" names change with it.

---

*Not to cite* (from the record's standing rules): "growth fixed" (CFG555); κ as derived (the GF2 "κ derived" is the SIS ratio);
"theory closed"; "the data favour the framework"; and any HMcode/BAHAMAS/ΛCDM-halo-model shear size as a verdict (owner 10-10
rule).
