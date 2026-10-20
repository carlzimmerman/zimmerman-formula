# CFG919 AMENDMENT A1 (POST HOC, 2026-10-20 ~15:45 UTC): C1's comparison clause

Committed after the frozen INJECT control failed and BEFORE the main run. No main-run number (no real-data cell E, no C1/C2,
form fit or class) has been computed or seen. Frozen criteria: 8d34dc761.

## What failed

Frozen INJECT, requirement I1 (E = 1.0·f planted on the V0 cells; 200 realizations per footing): **SUPPORTED in 85.0% on both
footings, below the frozen 90%.** The run is in `cfg919_MUTATE_inject.out`, frozen section. I0 (0.5%, required ≤ 10%) and
I2 (92.0%, required ≥ 90%) passed. The MUTATE shuffle bit on both footings: 0.0% SUPPORTED after shuffling, median T −0.003
vs +0.827 true.

## Diagnosis

The diagnosis comes from a scratch harness that runs the lane script's own definitions on the canonical footing.
- **The C1 clause.** 21 of the 24 CONTRADICTED realizations were C1, every one a disc-lens cell (f = 0.20). The frozen clause
  flags a rotating cell with E/σ_tot ≥ 3 and E ≥ Ē_P − 2√(σ_tot² + σ_P²).
- **Why it misfires.** Under a true linear selector, a disc-lens cell carries 0.2 and the pressure cells carry about 1.0. The
  combined error is about 0.2–0.3, so the expected gap is only ~3–4σ. Noise of about +2σ in one of the five disc-lens cells
  puts it both "≥ 3σ above zero" and "within 2σ of the pressure mean". That happens in about 11% of realizations.
- **What the clause therefore tests.** It is a consistency test with low specificity. It does not detect "a rotating system
  carrying the excess".
- **The other non-SUPPORTED realizations** (2 C3, 1 C2, 6 MARGINAL fits) are at the expected false-alarm rates.
- **No NaN fits.** The RuntimeWarnings from matmul are spurious macOS Accelerate floating-point flags, checked against an
  explicit sum to 1e-15.

## The change (C1 only)

**C1 (A1): a rotating cell (f ≤ 0.3) with E/σ_tot ≥ 3 and:**
- if the window holds non-GC pressure cells: **E ≥ Ē_P**, i.e. the rotating system carries at least the inverse-variance mean
  excess of the pressure-supported cells at that g_bar (point estimate);
- otherwise: E ≥ 0.345 (0.15 dex), unchanged.

**Everything else is unchanged:**
- C2, the W tests, the forms, the thresholds, the variants, MUTATE and INJECT requirements;
- the frozen C1 is still computed;
- every class is reported **AS FROZEN and UNDER A1, side by side**.

The INJECT and shuffle controls are re-run with both rules and both are reported.

**Code hygiene (no numerical change):** the matmuls in the form fit run under np.errstate, and finiteness is asserted.

## Disclosure (what I had seen of the real data when writing this)

- The shuffle control's S2 line, which carries no class weight: real-cell ordering statistic T = +0.528 on both footings,
  permutation p = 0.002.
- The number of V0 cells per class: DW 6, SS 4, SL 8, LD 5, LS 5, CL 5, GC 4.
- The median σ_tot per class, canonical: GC 0.281, LS 0.146, DW 0.251, CL 0.151, SL 0.128, LD 0.188, SS 0.158.
- The globular ARot coverage: 10 of 31.
- The count of HI-bearing dwarfs: 8.

No real cell E value, C1/C2 element, fit or class had been computed.

κ = ½ FITTED; footings never pooled; not theory closed.
