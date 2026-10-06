# CFG367: black-hole superradiance vs the cold-fluid wave field's mass window: NARROWS

Criteria 822a6f3ff. Script `cfg367_superradiance.py`, run as 2/2 checks plus MUTATE (spins = 0, union empty). Data: Reynolds 2021 (ARAA 59, 117; arXiv 2011.08948), Tables 1–2, transcribed by position into `bh_spins_reynolds2021.csv`. The PDF is kept outside the repo.

**Result, inside the record's window (2e-20 to 37 eV).**
- **Supermassive holes (primary)** exclude 4.5–7.5e-20, 1.0–1.05e-19, 1.5–1.95e-19 and 4.1e-19–5.1e-17 eV.
- **X-ray binaries (secondary, PROVISIONAL-MASS 5–20 Msun)** exclude 7.1e-13–8.5e-12 eV.
- **Surviving pieces and their tones:**
  - The light end, 2.0–4.4e-20 eV, which includes the CFG344 / G-PK edge at m ≥ 2.3e-20. Oscillation every 1.1–2.4 days; f_GW ≈ 1–2e-5 Hz, in the μHz gap where no detector runs.
  - Narrow gaps at 0.8–1.0e-19, 1.1–1.5e-19 and 2.2–3.9e-19 eV, which lie between the masses of measured holes. These are probably not real survivors: a denser hole census would close them. Their f_GW is 4e-5 to 2e-4 Hz, at the μHz gap and LISA's low edge.
  - 5.3e-17 to 6.8e-13 eV, with f_GW from 0.026 Hz (LISA) to 330 Hz (LIGO).
  - 8.8e-12 to 37 eV, above every gravitational-wave band.
- The record's L383 floor (2e-19 eV) sits in a gap and is not excluded.

**Fixes before commit (disclosed; neither changes the frozen physics).**
1. The hydrogenic bound-state frequency was applied outside its validity: at α ≳ n, ω turns negative and the rate overflowed. The first run therefore "excluded" everything above 2.5e-19 eV, including at a = 0, so MUTATE failed. The rate now returns 0 unless 0 < ω and α < l Ω_H.
2. The C1 test point α = 0.01 at a = 0.5 is not ≪ Ω_H = 0.134, which gave a ratio of 0.892. It was moved to α = 1e-4 (ratio 0.9989).

**Scope.**
- A gravity-only test, needing only that the field exists. It bounds where the field's mass can be; it does not detect it.
- The rates are Detweiler's approximation with the factor-2 correction, for l = 1–3. They are approximate at α ~ 0.3–0.5.
- The stellar masses are a bracket, not per-system values.
- The cold-fluid amount stays free. κ = ½ is fitted.

**Follow-up (10-06, read only, nothing computed or claimed).** I checked Capellupo et al. 2016 (MNRAS 460, 212; arXiv 1604.05310; Table 3, 37 quasars with thin-disc SED spins) as a way to close the light edge. It cannot, for two reasons:
- **The spins depend on the fit.** For the same quasar, the X-shooter-only and X-shooter+GALEX fits disagree. For example, J1152+0702 gives 0.98 (+0.05/−0.12) vs 0.15 (+0.63/−0.70). The conservative lower edge is therefore ≲ 0.2 for almost every object.
- **The well-measured holes are too heavy.** The cleanest high spins are at log M ≈ 9.3–9.5. At m = 2–4.4e-20 eV that gives α ≈ 0.4–1.0, outside superradiance for any spin. The light edge needs spins at M ≈ 0.5–1e9 Msun known to better than about ±0.2.
- The light edge stays open. Deciding it needs reflection-method or reverberation-calibrated spins near 1e9 Msun, which are not in hand.
