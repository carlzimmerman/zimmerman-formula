# CFG838 — is the satellite-dwarf excess driven by the host's tides?

Criteria: `FROZEN_CRITERIA.md` (19d9754bb, before the script). Run: `python3 cfg838.py` (MUTATE `CFG838_MUTATE=1`). Seconds.

## Result — CLASS: **NO TIDAL SIGNAL**
- 24 MW/M31 satellites: ρ(Δ, log T) = −0.00 (p 0.50); M31-mass bracket −0.04. Distance to the host: ρ = −0.02.
- The law's tidal acceleration across r_1/2 is tiny for almost all of them (log T = −3.6 to −1.9); only Andromeda I (−0.9)
  and Sagittarius (+0.1) are tidally exposed at r_1/2, and they carry no excess (+0.26, +0.00).
- Informational (not a class): Δ correlates with the host-field ratio g_host/g_int,N (ρ +0.34, p 0.053; bracket p 0.044),
  but g_int,N sits in that ratio's denominator, so this is the same signal as CFG828's Δ–g_bar anticorrelation, not a
  separate one. Note: in the framework a strong external field LOWERS the predicted boost, so an external-field effect
  would push the wrong way.
- Field dwarfs: gas-free Cetus +0.13 and Tucana +0.17 dex sit lower than the satellite mean (+0.39); gas-bearing Aquarius,
  Phoenix, Leo T (+0.26 to +0.59) are upper bounds (gas omitted). Two gas-free objects only: suggestive, not a test.
- **Reading:** the excess is not explained by present-day tides at r_1/2. Remaining satellite-specific candidates: past
  tidal heating on eccentric orbits (not captured by today's T), binaries (handled for UFDs only), non-equilibrium, or a
  genuine extra bound mass in satellites. CFG829 still stands: isolated discs at the same g_bar show no excess.

## Controls
- K1: Draco D 81.5 kpc, log T −2.31, log g_host/g_int,N 1.28 (as computed by hand from LVD r_h and the law).
- MUTATE bites: injected Δ = 0.3 log T is classed IMPLICATED (ρ +0.77); a shuffle is not (ρ −0.50).

κ = ½ fitted; cold energy mass required; not theory closed.
