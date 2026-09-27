# CFG0 — the framework's own findings, and the parameter-reduction map

Third wave of the fresh campaign (CHARTER rule 0). The lane has two jobs.
- **Inventory** the framework's own results: [`CFG0_own_findings_inventory.md`](CFG0_own_findings_inventory.md), with 81
  findings, 12 numerology flags and 24 withdrawn items, each with its status, file and commit.
- **Test every free or declared constant** of the record's working constructions against those findings: can a finding fix
  it, tie it to another constant, or make it unnecessary? The test is `CFG0_parameter_reduction.py`.

κ = ½ is fitted (Z = 5.7888 is κ restated) and nothing here derives it. Both a₀ footings are carried wherever a₀ enters:
9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt). This lane closes nothing.

```
python3 campaign_fresh_gravity/CFG0_parameter_reduction.py            # 33/33, rc = 0
MUTATE=1 python3 campaign_fresh_gravity/CFG0_parameter_reduction.py   # 30/33, rc = 1 (N1, N2 fail as designed)
```

Both runs take a few seconds on one thread. The script reads committed JSON and text files and writes only its own
`CFG0_parameter_reduction*` outputs.

## The answer

**No own finding fixes, ties or removes any constant that the record had not already reduced.** One constant changed class
during this lane: λ became a regulator. The record made that move itself (XR18b, `3c0cf3c37`, committed while this lane
ran), and this lane re-verified it independently from XR25's committed numbers.

Every other candidate the brief asked for was computed and checked on the gates it touches. Each one either fails a gate or
is numerology: it lands in a window, but no action term produces it, and a grammar of the same size lands there by chance.

**The new count**, beyond (G, c, Λ, ħ) and the ΛCDM-shared parameters:

| class | at the lane's start | now (CFG0) | constants |
|---|---|---|---|
| fitted | 5 | 5 | κ; ε (v_k); ζ (δ_t0); q; m |
| declared (knobs) | 3 | 2 | ξ; L_Λ (λ has left this row) |
| declared (natural choices) | 3 | 3 | n = 2; the q = 0 ramp; c_y = 2 |
| tied | 1 | 1 | a₀, tied to Λ's integration constant (XR20 T1) with κ as its coupling |
| derived | 0 | 0 | — |
| regulators | 1 | 2 | α_c; λ in the declared range (0, 0.03] |
| eliminated | 1 | 1 | c₂ → ∞ (OPEN at black-hole universal horizons) |
| initial data | 2 | 2 | the amount (ΛCDM's ω_c status); the misalignment |

Forms that are postulated but carry no number: the kernel (P2, run as ν_mono); the cross quartic; FK1 on the Einstein-frame
metric (FP22). One postulate is now data-selected: P1's density is ρ_Λ, not the local density (the environment null,
13–34σ).

## Constant by constant

| constant | verdict | the numbers that decide it | what would still reduce it |
|---|---|---|---|
| **κ** | FITTED | measured 0.465 ± 0.076 (BTFR) and 0.547 ± 0.175 (distance-free), pulls of ½ +0.46 / −0.27; the horizon coefficient 0.461 is within 1σ of both; underivable in the present action class (k01–k03, KS01, capstone, L313–L314) | nothing on the record; a precision problem (M/L zero point, gas scale, H₀) |
| **ξ** | KNOB | window [0.0243 / 0.0268, ~100] pc (FP7 A4, both footings). Compton ħ/(mc) = 1.2–3.4e-5 pc, **721× below the floor**. ħ/(m v_k) = 0.0057–0.0175 pc, below the floor for every m (FP17 B1). ONE_NEW_THING's ħc/ξ ≤ 2.6e-22 eV, 721× below the m floor. ħ/(m·200 km/s) = 0.050 pc at 1.9e-19 eV but 0.018 pc at 5.2e-19 (the floor is reached at m = 3.9e-19 / 3.6e-19 eV), and 200 km/s is no constant of the theory. h/(m v_k) = 0.036–0.110 pc is inside for every (m, v_k) and would predict γ̂(DR4) = 1.011–1.076, but the h-over-ħ choice is post hoc, no action couples the heat filter to the dark field (FP17 B4), and the field has been cleared from galaxies (FP17 B3). The family of 48 such lengths lands with chance 0.96. | **Gaia DR4** (Dec 2026) with a separation-resolved statistic: σ(ln ξ) ~ 0.2 (XR22). A **coherence-keyed ξ** would become a real tie only in a construction where the dark field stays in bound systems (CFG2, CFG5), and it must pass FP14's readout-gradient test. |
| **m** | FITTED | pinned near its floor on the canonical footing (the forest's minihalos against the flagship's cap, FP15 M1); floor 1.9–5.2e-19 eV (L383). GDM does not pin it: at the floor the field's c_s² ≤ 3.4e-16 and w_rec = 3.2e-20, and the record's own CMB bound (w₀ ≤ 2e-14) allows m ≥ 6.6e-27 eV, 7.5 decades lower | a mechanism for m; none exists (FP15 M5 numerology) |
| **ε (v_k)** | FITTED (irreducible) | (ħa₀/m)^⅓ = 2.2–3.3 km/s, 175× below v_k. c κ⁹ = 585.5 km/s lands in [575, 650] with chance 0.18 (0.35 for ε/m² = κ¹⁹, FP15 E3). (GM a₀)^¼ = v_k at a selection mass of 0.7–1.4e13 M☉ across both footings (FP4 L10l). **The construction's window is empty** (FP16; unchanged by FP20b) | a construction that does not need the kick |
| **ζ (δ_t0)** | FITTED | ΛCDM spherical collapse gives a turnaround contrast today of **1 + δ_ta(0) = 11.76**, **6.6% below FP15's floor-mass band** [12.59, 14.63] and 7.6% below the web's filament line (δ_t0 ≥ 12.74), but inside XR12's plain-reading band [7.54, 14.6]. The full turnaround gate, R(z) = 1 + δ_ta(z), gives 5.71 at z = 2.5 against a needed ≥ 59.2 (×10.4 short): it fails the forest. The virial contrast for collapse today (329.6) is far above the cap. | the near miss is within the forest proxy's own ~2× systematic (FP15 L15r, OPEN), so it is **not excluded at a level that matters**. It is still not a tie: it keeps FK1's declared q = 7/4 running, which the turnaround does not have. |
| **q** | FITTED | the turnaround contrast runs the wrong way: R_ta(2.5)/R_ta(0) = 0.49 against the 4.71 the gates need (effective q_ta = 0.89; the window is q = 7/4 canonical, [1.5, 1.75] alt). q = n − ¼ = 7/4 (n_t ∝ L⁻² with H_K1's n = 2) hits exactly, but post hoc: chance 0.50 / 0.75 for a unit-spaced family, and no action term selects the exponent (FP15 T1) | a derived identification of the trigger's running with the separator's |
| **λ** | REGULATOR (declared ≤ 0.03) | over (0, 0.03]: tracking speed 0.50%, galaxy α₂v² 1.00%, σ₈ 2.5e-4 (H_S, XR25) and 3.6e-7 (H_K1, XR18b); tracking margin ×9.6 over the moving-source gate; ℓ_sc ≤ 1.53 cm; BBN's bound is on initial data (XR26 F1). Needs c₂ → ∞ (at FP2's c₂ floor there is no λ window). | done: made by the record (XR18b), re-verified here |
| **α_c** | REGULATOR | [8.2e-16, 3.2e-9]; every observable moves ≤ 1.6e-9 (FP14, XR25) | — |
| **c₂** | ELIMINATED | c₂ → ∞ is regular on Minkowski and FRW (FP14); singular at O(α_c) at black-hole universal horizons (XR25): OPEN | the black-hole question |
| **L_Λ** | DECLARED | window now [2.8, 4.6] Mpc with the exact projector (FP20b); σ₈-tight [2.8, 3.0]. FP19 B1 reproduced (κ⁸ a₀/H_Λ² = 3.63 Mpc; chance 80%). No power of κ or Z times a₀/H_Λ² or c/H_Λ lands in the tight window. A 518-member grammar of own lengths gives 4 hits in [2.8, 3.0] (for example v_k/(3H₀) = 2.84 Mpc, ½ × 0.555 v_k/H_Λ = 2.86 Mpc), and it lands in a window that wide with chance 0.90: numerology. **The turnaround separator as a response gate fails KiDS in all four Brouwer bins on both footings**: the chain's own zero-velocity radius at the bins' masses (0.97–1.41 Mpc, an upper bound on the turned-around region) sits ×1.7–2.7 below h72's 3σ lower bounds on where the boost ends (1.67 / 2.07 / 3.44 / 2.77 Mpc). | a **source-gate** turnaround switch (only turned-around matter sources MOND; the field still extends outward) is not decided here. It must keep the lensing phantom out to h72's bounds and still pass σ₈, the forest and CMB lensing. That is a lane (CFG4). |
| **n, the ramp, c_y** | NATURAL CHOICES | n_eff = 2.06 from the web's running (FP13, under H_S); c_y = 2 is the Hamiltonian constraint's normalisation, chosen after scoring (FP19) | — |
| **the amount** | INITIAL DATA | no committed relation to (κ, Ω_Λ); the ghost-condensate reading proves the mean is not set by thermal or fluctuation physics. κ² = ¼ misses Planck's Ω_c by −5.4σ. The grammar κᵃ(8π/3)^(b/2)πᶜΩ_Λᵈ (625 members) gives 3 hits within 1σ against 1.86 expected by chance. **Its best hit, κ⁴√(8π/3)/Ω_Λ = 0.2642, equals Planck's central Ω_c: numerology.** | as ΛCDM: a fitted amount |
| **the misalignment** | INITIAL DATA | bounded by the flagship's allowance S ≤ 0.059: θ ≤ 14.06° (prior 14/90 = 0.156) | goes with the kick construction |

## Real, numerology, failed

- **Real reductions.** Only λ → regulator, and the record made it itself (XR18b); this lane verified it. Two ties already on
  the record stay: a₀ ↔ Λ (XR20 T1, XR30) and FK1's Einstein-frame coupling (FP22, no new constant). P1's density is
  data-selected against the local density.
- **Numerology (new flags N8–N12 in the inventory).**
  - Ω_c = κ⁴√(8π/3)/Ω_Λ.
  - ξ = h/(m v_k).
  - L_Λ ≈ v_k/(3H₀).
  - q = n − ¼.
  - δ_t0 ≈ 1 + δ_ta(0).

  Each lands, and each lands with a large chance rate or keeps a declared running. None is counted.
- **Failed on a gate.**
  - ξ = ħ/(mc) (×721) and ξ = ħ/(m v_k) (below the Saturn-monopole floor).
  - The full turnaround trigger (the forest, ×10).
  - The turnaround response separator (KiDS, ×1.7–2.7, in 4 of 4 bins).
  - κ² as Ω_c (−5.4σ).
  - (ħa₀/m)^⅓ as v_k (×175).
- **Neither.**
  - The SN-Ia step fixes nothing: acceleration adds ~0.8 SE beyond mass, so the location is a coincidence, and the null is
    underpowered.
  - The environment null fixes P1's density choice but not the kernel's shape, and no constant.
  - The GDM theorem fixes the dark component's cosmological form (a cold fluid plus an amount), not m.

**Where the parameter space can actually shrink** (each is a lane, not a result):
1. **The dark sector's five numbers** (ε, ζ, q, m, the misalignment) belong to FK1's kick, whose window is empty (FP16). A
   construction in which the dark field is not cleared from galaxies (CFG2, CFG5) needs none of ε, ζ, q or the
   misalignment; m keeps its floor (L383). That is the largest available reduction, 4 constants, conditional on such a
   construction passing the cluster gates (6.8× baryons, r^−1.53, X-COP).
2. **L_Λ plus the three natural choices** go away if the switch between bound and Hubble-flow matter comes from turnaround.
   The response-gate version fails KiDS (above); the source-gate version is open.
3. **ξ** becomes FITTED-BY-DATA in December 2026 (DR4, XR22). It becomes TIED only if a construction couples the MOND
   source's smoothing to a field that is present in the Solar neighbourhood.

## What each lane must build on

Cite by inventory number, never a withdrawn item (W1–W24).

- **Every lane.** F1–F4 (the form is forced; κ is fitted and underivable, so do not try); F10 and F16 (flat a₀ through the
  unimodular tie); F19 (the galaxy law, with the a₀/2 tail constraint); F23 (the closure theorem: single-radius statistics
  are the RAR); F42 (clusters: 48% accounted for, 6.8× baryons, r^−1.53); F48 (GDM); F31 (h72: the lensing boost continues
  past 1.7–3.4 Mpc); F75 (the early universe is GR + CDM); F28 (the EFE is measured against the framework).
- **CFG1 (the evidence audit).** F9, F14, F15, F18, F20, F29, F31, F44, F45, F46, F47, F61 and F72, and the whole withdrawn
  list. The record's approximation errata: FP20 (the projector), FP22 (the all-matter reading), XR21's forest kernel
  argument, the T_EH98 units error (XR23), and F14's "decides nothing".
- **CFG2 (GR plus a vacuum-regulated dark field).**
  - The field: F48–F51 (a wave field, not dust; m ≳ 2–5e-19 eV; the amount free with its sign forced).
  - What the field must do: F33 (the bounded-boost ceiling a halo cannot impose); F32 and W22 (a bounded "halo is the
    phantom" cannot source lensing to 3 Mpc); F54 (reciprocity).
  - The kick's failures, so its constants are not inherited: F56, F58, F59.
  - The pointer from R2 here: this is the construction where a coherence-keyed ξ could become a real tie.
- **CFG3 (vacuum-regulated gravity).**
  - The Solar-System side: F36 and F37 (every Solar-System screen is a threshold mass; the floors); F38 (DR4).
  - The action's constraints: F64 (the concave-gate lemma and the chord bound); F65 (Gauss compensation); F66 (the AQUAL
    repair); F73 (who feels MOND).
  - Tests it must pass or explain: F30 (the linear regime is Newtonian); F74 (strong field); F44 (SLACS).
- **CFG4 (the target law).** F23, F28, F31, F42, F45, F46, F18, F13, F30 and F67; F71 (H_K1 and its prices). From this lane:
  a switch that truncates the phantom at the turnaround radius fails KiDS, and a switch must leave the lensing phantom out
  to ≥ 1.7–3.4 Mpc for M_b = 1.5–9e10 M☉.
- **CFG5 (the RAR as a fossil of collapse).**
  - From the lensing side: F31, F32/W22 and F33 (the fossil must not truncate the lensing phantom inside h72's bounds).
  - From the dark sector: F42, F48–F51, F54, F56, F58, F59; F76 (the high-z halo abundance equals ΛCDM's).
  - From this lane's R4: ΛCDM's turnaround contrast is 11.76 today and 5.7 at z ≥ 2.5, so a collapse-keyed process acting
    at turnaround would act on every z ≥ 3 structure, which the forest forbids unless it is gated in time.
- **CFG6 (a₀ following the dark energy).** F10–F16, F8 (κ-blind), and C3's reproduced tracks: √ρ_DE (FP0 R3b), √V and the
  pressure mapping (XR20 E2), and L274's chart row. **Open conflict to resolve first**: PAPER7 v3 and L273 say the density
  mapping is rejected by the pressure law; FP0 R3b adopts it; XR20 says a field tie reads √V.

## Controls, MUTATE, hypotheses

**Controls.** All load-bearing; all reproduce committed numbers.

| control | what it reproduces |
|---|---|
| C1 | FP0's a₀ on both footings, Z, ρ_Λ and H_Λ, to 1e-16; the uniqueness of the form (\|det\| = 2) |
| C2 | the measured κ: A = 0.46511 from a₀ = 8.7091e-11; B = 0.54704 ± 0.17471 as the quadrature of its budget; the pulls of ½; k03's 0.460659 — all exactly as in `paper_numbers.json` |
| C3 | PAPER7's flat law (exactly 1 at w = −1); FP0's E(z) and R3b's 0.7956404958; XR20 E2's 21 track values (to 4e-17 dex); L274's z = 2.5 row (0.000 own, +0.334 ΛCDM) |
| C4 | XR20 T1: Λ/α² = 32π = 100.530965 (alt 68.833552); the vacuum caveat values; Λ; XR30's K_∞ form equals a₀ |
| C5 | FP7's AQUAL floors 0.02428 / 0.02683 pc; FP17 B1's 8 de Broglie lengths and B2's Compton and ξ_q lengths (exact); B1's monopole ratio at the kick, 1.925 / 2.551 |
| C6 | XR25 L4: the tracking-speed law to 1e-9; α₂v² affine in λ to 1e-6 |
| C7 | FP15 T6d's natural numbers and its δ_t0 band |
| C8 | FP19 B1: κ⁸ → 3.627 Mpc; chances 0.796 / 0.314 |
| C9 | FL1 F5's GDM rows, exact |
| C10 | h72's bounds and bin masses |
| C11 | FP12's and FP11's R0 rows; the slope 0.19 |
| C12 | the ΛCDM top-hat solver. EdS limits 9π²/16 and 18π²; Δ_vir(0) = 329.6 against Bryan & Norman's 327.4 (a literature fit, used only to check the code); the turnaround time against a direct ODE integration (agreement 1.3e-11) |

**MUTATE.** Declared in the docstring before the first run. It adopts the parameter-free tie ξ = ħ/(m_floor c), the Compton
length at 1.9e-19 eV, as a reduction. The tie sits 721× below the Saturn-monopole floor, so N1 and N2 fail and rc = 1. The
reported H16 also fails, because two constants move.

**Hypotheses.** H1–H16 (with H8a/b/c) were written into the docstring before the first run, from pencil-and-paper estimates
(the turnaround contrast today was estimated by hand at ~11.8 before the solver ran). All held as declared. H7 held, but the
reclassification it anticipated was made by the record itself (XR18b) while this lane ran. H10 is evaluated on the window
declared in it ([2.65, 3.0], FP19's committed B1) and is reported on the current window [2.8, 3.0] too.

## Disclosures

- **Development runs** wrote to a scratch directory outside the repository, through the `CFG0_OUTDIR` variable. Only the
  final ordered pair (MUTATE, then main) is kept here.
  - Run 1, main: rc = 1. C6 failed: the script had assumed α₂v² ∝ (λ + 3), but the committed entries are affine with a
    slightly different offset (max deviation 3.3e-3). C6 now checks the tracking-speed law and α₂v²'s linearity, and the λ
    test reads the committed λ = 0 and 0.03 entries directly.
  - Run 1 also showed that **the record had moved since this lane began**:
    - XR18b (`3c0cf3c37`, README `3b22289d7`) made λ a regulator in a declared range;
    - FP20b (`3924bb8c2`, README `535c64435`) narrowed L_Λ's window to [2.8, 4.6] Mpc.

    The script now reads the knob ledger live (by each row's leading status word), keeps the lane-start baseline explicit
    (λ a knob, as in the README at `08548fc85`), cross-checks XR18b's R5/R6 numbers, and reports L_Λ on both windows. N1 and
    N2 were re-worded so that the count credits a move made by the record only when this lane re-verifies it. No hypothesis
    was changed.
  - Runs 2 and 3: rc = 0 (main) and rc = 1 (MUTATE). Between them, a round-off warning from `quad` at a root bracket
    (ω → 1, used only for the bracket's sign) was silenced, a duplicated "(reported)" label and a print format were fixed,
    and one context line for the ζ near miss was added. No number changed.
- **Not done here.**
  - No particle-mesh run.
  - No new KiDS likelihood: the turnaround separator is judged against h72's committed bounds, using the chain's own R0 as
    an upper bound on the turned-around region.
  - The source-gate turnaround version was not computed.
  - Nothing was downloaded; nothing outside `CFG0_*` was written.
- **XR36 and FP25** (named in the brief as turnaround-gate lanes) are not in the record at `3b22289d7`. This lane's R4 and R8
  test the turnaround gate in the two readings the committed gates allow. If those lanes land with a different
  construction, R4 and R8 should be re-checked against them.
- **External inputs.**
  - Planck 2018's ω_c = 0.1200 ± 0.0012, used as the gate for the dark amount.
  - Bryan & Norman 1998's Δ_vir fit, used only as a code control.
  - The ΛCDM spherical top hat is GR's own collapse on the chain's background (Ω_m = 0.3153, Ω_Λ = 0.6847).
- **The SN-Ia and environment numbers** are read from committed text (`mi_snia_power_curve_2026.py`'s docstring;
  `A0_COSMICWEB_ENVIRONMENT_2026-06.md`). No committed outputs exist for those scripts, so they are reported, not used as
  controls.

## Files

- `CFG0_own_findings_inventory.md` — the inventory (A).
- `CFG0_parameter_reduction.py` — the reduction map (B), with its outputs:
  - `CFG0_parameter_reduction.out` and `CFG0_parameter_reduction_results.json` (main);
  - `CFG0_parameter_reduction_MUTATE.out` and `CFG0_parameter_reduction_results_MUTATE.json` (the control).
- `CFG0_README.md` — this page.
