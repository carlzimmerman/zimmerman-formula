# SP2_sealed_basin_lensing: FROZEN CRITERIA (committed alone, before any SP2 number)

Written 2026-10-28, at the owner's request: "build on what works".

**What this lane does.** It turns the working picture into a sealed, falsifiable prediction unique to its newest piece.
The working picture is:
- the law;
- the max() surface-density rule for cold dark energy, keyed on the gravitational basin (BS1, 979363d820; CL3 variant
  passes every canonical line and the Milky Way);
- the fair-share budget.

**The basin prediction.** Take two central galaxies with the **same** stellar mass M★ below the own-mass switch.
- One alone in its basin, as KiDS isolated lenses are, follows the **law** on its baryons.
- One sharing a basin above the threshold, i.e. a central in a pair or group with log M_basin > T, carries a **route-E
  cold dark energy halo** of its own M200.

A smooth-relation competitor, whether ΛCDM halos or the law everywhere, predicts the same profile at fixed M★, up to
modest environment trends. **The step in the profile with basin mass at fixed M★ is the signature.**

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a particle.
- Not "theory closed". The lane makes no claim about the data; it is a prediction **for** future data.
- No downloads.

## 1. Model (frozen; SP1's machinery, 1048b648fa / 405bedd901)

- **Lens model:** SP1's lens model, i.e. X53's F2 inventory and AQUAL projector, EM1 R1 M200, X53's `mass_H` with CL2's
  S9 c_f(M) at L = 4, at lens redshift 0.3.
- **Law branch:** ΔΣ_law(R; M★), the law on baryons with the "linear" projector, as X62.
- **Basin branch:** ΔΣ_basin(R; M★), Newtonian baryons plus the route-E halo of the galaxy's **own** M200, with the
  "const" projector. The neighbours' own mass is **not** included; disclosed: a measurement must isolate the central's
  own profile, e.g. inner radii or stacks with satellites masked.
- **Grid:**
  - log M★ = 10.0 to 11.2 in steps of 0.1, all below SP1's own-mass switch at log M★ ≈ 11.21;
  - R = 0.05 to 2 Mpc (SP1's nine radii);
  - both footings.
- **Observable:** Q_env(M★, R) = ΔΣ_basin / ΔΣ_law.
- **Sealed statistic:** S_env = the mean of Q_env at R = 0.3 Mpc over log M★ 10.5–11.0.

## 2. Falsifier (frozen)

A future environment-split stack is the test: KiDS-Legacy, Euclid DR1, or DESI × HSC/KiDS, with centrals binned in
M★ and split by group or pair membership at a basin mass above 10^12.3 against isolated centrals.

**It falsifies the basin rule if:**
- (a) the measured ratio of the split at 0.3 Mpc is below 1 + 0.5 (S_env − 1) at 3σ; **or**
- (b) the isolated stack departs from the law-branch ΔΣ by more than its own 3σ.

## 3. Sealing

- The predictions are written to `sp2_predictions.json`.
- Its sha256 is recorded in `SEAL.md`.
- Both are committed and pushed before any comparison data are opened.
- The JSON is byte-reproducible.

## 4. Checks and twin

- **K1.** SP1's law-stack χ² against X53 is reproduced, within 5 %, through the same code.
- **K2.** At log M★ where SP1 put a galaxy above the switch, Q_env equals SP1's own Q there to 1e-9 (the same halo
  branch).
- **K3.** Peak RSS < 1 GB.
- **MUTATE (`SP2_MUTATE=1`, separate outputs).** The halo branch is replaced by the law branch, so Q_env ≡ 1 and K4
  fails. K4 requires S_env − 1 ≠ 0 by at least 0.05.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I sp2_predict.py`
