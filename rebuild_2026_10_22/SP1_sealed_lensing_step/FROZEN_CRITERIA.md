# SP1_sealed_lensing_step: FROZEN CRITERIA (committed alone, before any SP1 number)

**Purpose.** A **sealed prediction** for data not yet released, committed with a content hash before release. The frozen
CL2 picture (b57ed8751f) has a switch. An isolated galaxy carries a cold dark energy halo only if its M200 exceeds
10^12.3 M☉, with M200 from EM1's relation applied to its baryons. Below the switch the galaxy law acts on baryons alone.

**Consequence.** Stacked weak lensing ΔΣ(R) of **isolated** central galaxies, binned by stellar mass, should follow the
law-only prediction below a stellar-mass threshold M★,sw and jump abruptly above it. The size of that jump and where it
sits are the prediction.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework. The prediction is made **for** future data; the lane makes no claim about it.

## 1. Model (frozen; X53's committed lens machinery, F2 inventory)

**Lens of native stellar mass M★:**
- cold gas from F2's relation;
- hot gas 0.5 M★ inside 100 kpc;
- M_b = M★ + M_cold;
- M200 from EM1 A_c2b_refit R1: log M200 = 11.18 + 0.90 (log M_b − 10).

**Below the switch (M200 ≤ 10^12.3):** the galaxy law, M_dyn(r) = M_b(r) ν(G M_b(r)/(r² a₀)), with
ν(y) = ½ + √(¼ + 1/y). ΔΣ uses F2's AQUAL projector in "linear" mode, as X62 does for the law branch.

**Above the switch:** route E. This is the Newtonian baryons plus a Burkert halo of total M200 cut at R200, with core
Σ = max(a₀/2πG, η Σ_coll), η = (4/(3B(1))) c_f(M200)^{5/4}, and c_f(M) = 4 × c_nat(M)/c_nat(10^14) (the S9 shape).
This is X53's `mass_H` with CL2's c_f. ΔΣ uses the "const" mode.

**Prediction grid:**
- log M★ from 10.3 to 11.7 in steps of 0.05;
- R = 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0 Mpc;
- lens redshift 0.3;
- both footings.

**Observable:** the ratio Q(M★, R) = ΔΣ_CL2 / ΔΣ_law-only, and ΔΣ_CL2 itself in M☉ pc⁻².

**The switch location:** M★,sw, the stellar mass at which M200 = 10^12.3. It is reported per footing.

**Scatter variant (reported; the primary carries no scatter):** the step smoothed by lognormal scatter of 0.15 dex in
log M200 at fixed M★.

## 2. Sealed statistic (frozen)

**S_step** = Q at R = 0.5 Mpc, averaged over a 0.2 dex bin just above M★,sw, divided by the same average over a 0.2 dex
bin just below. The prediction states its value, with and without scatter. A smooth-relation competitor predicts
S_step ≈ 1.

**Falsifier (frozen):** a future isolated-lens stack (KiDS-Legacy, Euclid DR1, or DESI × KiDS/HSC) that measures
S_step < 1 + 0.5 (S_pred − 1) at 3σ, or that finds the step more than 0.3 dex in M★ away from M★,sw.

## 3. Sealing

- The predictions are written to `sp1_predictions.json`.
- Its sha256 is recorded in `SEAL.md`.
- Both are committed and pushed before any comparison data are opened.
- No future data are downloaded by this lane.

## 4. Checks and twin

- **K1.** With the switch disabled (T = ∞), Q ≡ 1 at every grid point.
- **K2.** The machinery reproduces X53's committed law-only stacked χ² (160.7 canonical) through its own stack function.
- **K3.** Peak RSS < 1 GB.
- **MUTATE (`SP1_MUTATE=1`, separate outputs).** The switch is moved to 10^13.3. The twin must place M★,sw more than 0.5
  dex higher.
