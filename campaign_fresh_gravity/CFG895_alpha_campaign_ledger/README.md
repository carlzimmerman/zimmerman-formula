# CFG895: the ledger, rules and doors for the alpha campaign

This lane builds the foundation for a new, honest set of attempts on the fine-structure constant. It does not attempt a derivation. **Nothing here derives alpha.** Alpha remains an INPUT, kappa = 1/2 remains FITTED, and the Standard-Model mass and coupling sector remains walled.

## Files

| File | Contents |
|---|---|
| `ALPHA_ATTEMPTS_LEDGER.md` | All 101 attempt rows found in the repository: ID, family, path, mechanism, value, verdict, trials and commit. It ends with a note on public pages that still carry old alpha claims. |
| `ALPHA_CAMPAIGN_RULES.md` | The rules for new attempts: pre-registration, kernel classes, the attempt counter, the precision each option-space size demands, hit criteria and grades. |
| `ALPHA_DOORS.md` | The 8 untried routes that survive the screen, ranked; the assessment of Codex's handoff; and 18 excluded ideas with their reasons. |
| `cfg895_check.py` | Tallies the ledger and computes every by-construction number the other files quote. |
| `cfg895_check.out`, `cfg895_check.json` | Output and values from the real run (exit 0, 13/13 checks PASS). |
| `cfg895_check_MUTATE.out` | The MUTATE control: replacing (1 − 8λ) by (1 + 8λ) in AS3's f_g makes K2, K3 and K5 fail, and the run exits 1. |

Run: `nice -n 10 python3 cfg895_check.py` (real) and `nice -n 10 python3 cfg895_check.py MUTATE` (control). Both take under a second and use one core.

## Counts (from `cfg895_check.py`)

Ledger rows per family:

| FP | GEO | QED | GRAV | WGC | HOR | STR | EMG | DIL | QCD | SEL | NUM | EXT | META | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16 | 4 | 2 | 2 | 2 | 12 | 5 | 4 | 3 | 13 | 2 | 19 | 5 | 12 | **101** |

* **Graded value trials at the level of mechanisms in the record (lower bound): N_mech = 359.** This is the starting value of the campaign's attempt counter.
* **Rule-search trials: N_rule = 78,586,900** (A1 + A2 + project_atomos + the legacy 34,073-formula space). The numerical-search budget is spent.
* **External claims audited:** 22.
* **Derivations:** 0.
* **Values ever produced at mechanism level:**
  * near the target, 1/alpha(0) from 70 to 152 (emergence 70–72; asymptotic safety 75–96; U3 133.2; B1 138.35 ± 8.28; heterotic 146.1; N2 128–152);
  * far-off outliers: U2 alpha = 2π; W2 alpha_c ≈ 1.05; MacDowell–Mansouri about 1e-120;
  * plus numerology close to 137.036, every case retracted or FDR-dead.

## New by-construction findings in this lane (scripted; not derivations)

1. **The FSP selection equation is NON-DIAGNOSTIC for alpha.** The equation is R(alpha) = c_H/C_p³ = H̄/(K G m_p³). Alpha enters it only through first-order electromagnetic corrections, d ln m_p/d ln alpha ≈ (4.9–5.8)e-4. Even allowing |d ln R/d ln alpha| up to 10 times that, the H0 bracket leaves σ(ln alpha) ≥ 11, and knowing the cosmological side to 1% still leaves 1.7. Inferring alpha to 1% would need the cosmological side and the QCD ratio to 5.8e-5. In FSP-002's form of the bridge kappa cancels, so it never involved kappa in substance.
2. **A single-coupling UV route cannot reach campaign-wide evidence.** With Y1's running error (8.8e-4) and N_mech = 359, it gets CONSISTENT at most. Joint predictions (two couplings, or a coupling together with M_W) are needed: P_single ≈ 9e-8.
3. **The asymptotic-safety map** 1/alpha(0) ≈ 41/(24π f_g) + 49.203 + 32.6 reproduces AS3 and AS4 to 0.24% and the required f_g to 0.4%. The slope is −55.2 per unit ln f_g, so 1% in alpha needs f_g to 2.5%. At AS3's g*, the required λ* is 0.107 or −7.83, against AS3's −1.22.

## Top 6 doors (full entries in `ALPHA_DOORS.md`)

1. **D01:** f_g from the fluctuation photon–graviton vertex, beyond the background field. K1. This is the record's untried rung and the Codex chat's open item. Medium cost.
2. **D02:** A Higgs boundary condition (AS-forced λ(M_P) ≈ 0, or MPP/Veltman) solved for g_Y jointly with M_W. A leverage pre-flight runs first. Low cost, and the only door able to reach EVIDENCE.
3. **D03:** f_g with the record's own matter content (SM + 3 ν_R from the FS11 door, plus any elementary dark fields from the canonical theory). Low cost; closes the content loophole.
4. **D04:** Unimodular AS f_g, with Λ as an integration constant. 137 needs g* ≈ 0.222 if the TT-only structure carries over. Low–medium cost.
5. **D05:** Photon–curvature operators (R F², Ric F F, C F F) in the AS truncation. Medium cost.
6. **D06:** Einstein–Cartan–Holst (first-order) AS f_g. Medium–high cost.

Doors 7 and 8 are the noncommutative-geometry spectral action with a forced cutoff function (expected KILLED, ×18–26) and closure of S1, the charged vector boson in dS₄.

## Parallel efforts (2026-10-20)

| Effort | State |
|---|---|
| Fine-structure puzzle programme (`fine_structure_puzzle/`, the "Fine structure constant with Codex" chat) | **IDLE.** The last step is FSP-011 (7db7931cf, on main), which reduced the proton side to one isoscalar lattice observable N0. That lattice production job has not been started. FSP-001 to FSP-010 are committed on branch `codex/fine-structure-claude-handoff` (6ce8eec12) and are untracked on main, as is the root handoff file. The live STATUS and HANDOFF files still describe FSP-010 (see the FSP-011 navigation note). The f_g photon–graviton vertex was noted and not started; it is D01. |
| The `real_research/alpha_principle_2026/` campaign | **IDLE** since the AS1–AS4 append (e54c33252, 2026-10-19). |
| CFG893 and CFG894 (kappa, in the same 890–899 block) | CFG893 reported NOT SELECTED (131bedf33). CFG894, the kappa attempt ledger, is a parallel lane that is not yet committed. Both concern kappa, not alpha. |
| 1024³ chain | Running: no alpha computation may run beside it (record rule). |

## Record rules restated

* The SM bridge is WALLED unless a NEW FORCED KERNEL appears.
* Schwinger/Unruh (AH1–AH4) is a NO-GO in dS₂ and dS₄.
* AS1–AS4 gave 1/alpha of 91–96, not 137. Their admissibility rule rejects the published pure-gravity fixed point (disclosed).
* kappa and Z play no part in alpha.
* The SM mass sector is walled, and the Koide doors are closed in Lean.
* Never manufacture a derivation, and check identities by construction.
