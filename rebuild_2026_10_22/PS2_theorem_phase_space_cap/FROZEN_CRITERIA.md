# PS2_theorem_phase_space_cap: FROZEN CRITERIA (committed alone, before the graded script exists or any new graded number)

Written 2026-10-26, at the owner's request: "draft frozen criteria for a fresh lane grading the theorem-strength phase-space
cap (progenitor's central Q), disclosing everything PS1 showed, with G-OUT-M3 as the stated risk. Criteria only."

Standing rules:
- κ = ½ FITTED.
- Footings canonical / alt are graded separately and never pooled.
- Cold dark energy, not matter, never a particle.
- No new constant. No ΛCDM number enters the rule. Inherited inputs are listed in §8.
- Nothing here says the data favour the framework. Not "theory closed".

## 0. Why this lane, and what it cannot be

PS1 (748770f505 / 6ebe8911c9) graded the **mean**-Q posit, with result TRADES. It also **reported** this lane's rule as an
uncredited variant, so the 15-cell outcome below is already partly seen (§6).

**PS2's 15-cell class is therefore not a blind test.** It is graded and frozen so that the record carries it, and the
expected class is stated now: **TRADES via G-OUT-M3**.

The lane's new tests are the two lines PS1 never computed for this rule:
- **G-HSE:** does the capped core land on the gas's own hydrostatic core?
- **G-CF:** does the cluster inner band stop depending on the unconverged c_f?

## 1. Hypothesis PT (theorem-strength phase-space cap)

Cold dark energy is collisionless, so its fine-grained f is conserved along orbits. Coarse-graining can only lower the
maximum. So a halo's central coarse-grained phase-space density cannot exceed that of the material it was assembled from.

The rule uses the **progenitor's own central** value, which is the bound Liouville licenses. It does not use the
progenitor's mean, which PS1 showed is violated 107–252× by every halo in the record.

    Q_core(M) ≡ ρ_0 / σ_0³  ≤  Q_prog(M)

Q_prog(M) is exactly PS1's `q_form_thm`, unchanged:
- **Progenitor:** the half-mass object M/2 at M's Lacey–Cole formation epoch (X41's `zform`, `sigma_coll`), with
  R_out = r_f = (3(M/2)/(4π · 18π² ρ̄_m(1+z_f)³))^{1/3}.
- **Its core:** a Burkert at the **baseline** surface density, Σ_prog = max(a₀/(2πG), η(M/2) Σ_coll(M/2)), with η from X48's
  ng-48 c_f table. No baryons.
- **Q:** ρ_0 / σ_0³, with σ_0 the isotropic Jeans central dispersion (PS1's `q_core`).

The descendant core uses PS1's `q_core` unchanged: the Burkert at Σ in the total potential (cold + baryons), with the same
M_halo, R_out and baryon profiles as PS1 §"Implementation choices".

**Rule (graded).**

    Σ_core = max( a₀/(2πG),  min( η(c_f) Σ_coll(M),  Σ_PT(M) ) )

Σ_PT solves Q_core(Σ) = Q_prog(M). The a₀ floor is untouched, and the cap acts only on the collapse branch.

**Fixed now, not revisited.** The progenitor is evaluated at the **baseline** Σ, not at its own capped Σ. A recursive
version is a different rule, and choosing it after seeing PS1 would be post hoc. It is reported only (§4 item 3).

## 2. Model (graded run)

Everything is PS1's graded run except the cap's right-hand side:
- the same patched X43 copy;
- the X48 ng-48 c_f table;
- the same cluster, group and SPARC call sites;
- the same cells, C\*, weights, offsets and reduced shear;
- background A_c2b_refit (B is reported only);
- both footings, both h.

The baseline is X48 regrade ng 48, reproduced in PS1 to 1e-9.

## 3. Grades (per footing; a cell passes only if |Z| ≤ 2 at both h)

**G-15: the 15 X38/OS1 cluster cells, plus the SPARC line and groups |Z| ≤ 2.** These use PS1's classes, unchanged:
- INERT;
- PASS;
- IMPROVES;
- TRADES;
- FAILS.

The baseline-passing set is the 14 cells other than G-IN-Mall. **Expected now: TRADES via G-OUT-M3 (UNDER).**

**G-HSE: the X-ray core line, new.**
- **Sample and target:** the 106 KT clusters at h 0.672, against IB1's gas-equilibrium core,
  Σ_HG = 9β σ²/(4πG r_c), with β = 2/3, r_c = 0.15 R500 and σ² = kT/(0.6 m_p). This is the same formula as PS1's reported
  item 5.
- **Statistic:** the median of Σ_core/Σ_HG.

| class | rule |
|---|---|
| **HSE-MATCH** | the median is in [0.67, 1.5] (within 1.5×) |
| **HSE-MISS** | otherwise |

For reference, the baseline gives 2.56 and PS1's mean-Q cap gives 0.44 / 0.54. Both are misses.

**G-CF: c_f independence, new.**
- **Re-run:** the graded rule with the whole c_f table × 0.5 and × 2. That is X48's stated non-convergence, applied to η
  through c_f^{5/4} for both the descendant and the progenitor.

| class | rule |
|---|---|
| **CF-ROBUST** | G-IN-Mall passes at both h in both re-runs, **and** its pred moves by < 10 % from the graded run in both |
| **CF-FRAGILE** | otherwise |

**Headline (per footing).** The headline is the three labels together, e.g. "TRADES | HSE-MATCH | CF-ROBUST". There is no
pooled label. Both footings must agree on each label, else that label is UNDECIDED.

**What would count against PT outright:** HSE-MISS together with CF-FRAGILE. The cap would then neither land on the gas
core nor free the inner band from c_f.

## 4. Reported, not graded

1. **G-OUT-M3 in full:** pred/meas/Z at both h, and the M1–M3 tercile trend. This tells whether M3's miss is the same
   "outskirt mass does not track gas mass" failure IB1 found.
2. Per-bin pred/meas (all 326, h 0.672), as IB1 and PS1.
3. **Recursive progenitor:** Σ_prog itself capped by PT at M/4, one level only.
4. **Anisotropy bracket.** Q_core/Q_prog with σ_r at 0.1 r₀ for constant β = 0.5 on **both** sides, against isotropic on
   both. This asks whether the cap's binding survives when the anisotropy is shared.
5. Background B_cfg886_bg: the G-15 class.
6. The number of clusters where Σ_PT < Σ_a0 (the cap would cut below the floor, so the floor binds), per footing.

## 5. Checks

- **K0.** With the cap off, the script reproduces X48 ng 48 (G-IN-Mall pred at both h and the SPARC rms, to 1e-9).
- **K1.** The Plummer central dispersion matches G M/(6a) to a relative 1e-6.
- **K2 (as PS1 §4 intended; PS1's implementation tested a wider bracket and failed).**
  - **Monotonicity:** Q_core(Σ) is monotonic increasing on the solver's bracket [Σ_a0, η Σ_coll] for every graded cluster
    at h 0.672, on a 25-point log grid.
  - **No saturation:** the graded run has **0** Burkert saturations, in both the descendant and the progenitor solves.
  - **Residual:** the root residual is < 1e-8.
- **K3.** PS2's Q_prog equals PS1's `q_form_thm` to 1e-12, for 5 test masses.
- **K4.** Peak RSS < 2 GB, one thread.
- **MUTATE** (`--mutate`, separate `_MUTATE` outputs). K1's analytic side uses G M/(3a). K1 must FAIL, and the script exits
  1.

## 6. Seen before freezing (disclosed in full)

**From PS1 (6ebe8911c9), this rule as a reported variant, both footings:**
- It binds in 652/652 cluster-cells, all at interior roots, none at the floor.
- It binds in 0 SPARC galaxies and 0 group calls, so SPARC (0.0650 / 0.0657) and groups (Z +1.53) are unchanged from the
  baseline.
- G-IN-Mall Z: −1.65 (h 0.672) / −1.43 (h 0.686), PASS.
- The failing-cell list is ['G-OUT-M3 (UNDER)'] on both footings.

**Also seen from PS1:**
- The mean-Q rule's full output.
- The F0 map (Q_core/Q_form 107–252).
- The anisotropy factor: σ_r ratio ~3.1 at 0.1 r₀, on the descendant only.
- Σ/Σ_HG: baseline 2.56, mean-Q 0.44 / 0.54.
- K2's saturation behaviour for bare R200 halos at 10¹⁴ and 10¹⁵.

**Not seen, for this rule:**
- G-OUT-M3's pred and Z (only "FAIL, UNDER");
- any other cell's pred or Z;
- Σ_core/Σ_HG (G-HSE);
- the c_f × 0.5 / × 2 runs (G-CF);
- background B;
- per-bin;
- the recursive variant;
- the two-sided anisotropy.

**Stated risk: G-OUT-M3.** M3 sat at +1.80 in the baseline, just inside the line. PT lowers the inner cores, which moves
predicted mass outward. But PS1 shows M3 still ends UNDER, so the redistribution does not reach the gas-rich outskirts.

This is the same open piece IB1 named: the outskirt normalisation tied to M_b. PT is a core rule and is not expected to fix
it. **A G-15 PASS is therefore not expected.**

## 7. Outputs

`ps2_theorem_cap.py` → `ps2_theorem_cap.out` and `ps2_theorem_cap_results.json` (`_MUTATE` for the control). Run with
`PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`.

## 8. Inherited inputs (flagged)

| input | status |
|---|---|
| EPS formation (δ_c 1.686, ω̃ 0.974, Δ 18π², half-mass) | X41, unchanged |
| σ(M), D(z), Ω_m | EM1's own background |
| cluster cold mass = `prep`'s Mfair within r_ta | the flagship's (X43) budget. **Carries the 5.364 abundance the owner's 10-25 rule flags.** It is inherited unchanged, not introduced here. |
| c_f table | X48 ng 48, unconverged (×2); G-CF tests exactly this |
| isotropic σ_0 on both sides | modelling choice, fixed; §4 item 4 brackets it |
| R500, Mgas500, kT | eRASS1 catalogue: **ΛCDM-processed**, rescaled by qd to the h cell |
| β 2/3, r_c 0.15 R500, μ 0.6 (G-HSE target) | IB1 / F1 / X2 gas convention |
| C\* denominator, offsets, reduced shear, weights, boost | the record's (X2/X7/X30) |
