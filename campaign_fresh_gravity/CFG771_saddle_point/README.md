# CFG771: the Sun–Earth saddle point (the proposed LISA Pathfinder test) under the framework's action

**Label: NULL PREDICTED.**
- The committed stiffened action gives an anomalous tidal stress of 2.8e-26 s⁻² at the saddle (L* = 5.75 pc), falling as
  L*⁻² across the window.
- That is a static signal-to-noise ratio of 3.4e-8 for a full year at LPF's noise floor.
- **The framework predicts that a saddle-point flyby sees nothing.**
- Context: the action *without* stiffness would have been strongly testable (idealised SNR ~10²).

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (d323d8de5). Block CFG770–779.
- **Script:** `python3 cfg771.py` (7 s, exit 0). `CFG771_MUTATE=1` exits 1 as designed (both teeth bite).

## Results

| item | result |
|---|---|
| S1 saddle | 2.588e8 m from Earth without the Moon (K1 to 1e-14); 2.529e8 m with the Moon on the line, 2.591e8 m at quadrature. Tidal eigenvalues (+4.6, −2.3, −2.3)e-11 s⁻², and (+5.4, −2.7, −2.7)e-11 with the Moon on the line |
| S2 γ = 0 (context; curl part neglected) | basin-rule "bubble" r_b = a₀/\|T\| = 1.7–2.5 m, not Bekenstein–Magueijo's 383 km (TeVeS κ scaling). The anomalous stress peaks at 2–9e-11 s⁻² within ~10 m and decays as ~a₀/r (the a₀ tail rotating around the saddle): 2e-12 s⁻² at 100 m. Idealised white-noise SNR 90–530 for miss distances of 1–100 m |
| **S3 stiffened (verdict)** | anomalous stress 2.83e-26 / 1.0e-27 / 9.4e-29 / 9.4e-31 s⁻² at L* = 5.75 / 30 / 100 / 1000 pc. Each body's screened pull GM_i/L*² is uniform in magnitude, so only its direction change makes a tide. The Sun dominates. 1-yr SNR ≤ 3.4e-8. **NULL PREDICTED** |
| MUTATE | M1: stress × 3.306e9 = (5.75e4)², exact. M2: T → 0 gives zero S2 stress everywhere (see Disclosures) |

## Reading
1. **Same mechanism as Cassini (CFG770).** The stiff P field cannot vary on scales below about 2 pc, so the saddle has no
   MOND bubble at all. A LISA-Pathfinder-type pass cannot confirm or refute the framework; it would only kill the unscreened
   (γ = 0) form, which the ephemerides already kill (CFG770 C0).
2. **A side result.** For any a₀-scale law, the saddle anomaly is metre-scale (a₀/|T| ≈ 2 m) with an a₀/r stress tail. It is
   not a 383-km bubble; that figure belongs to TeVeS's scalar normalisation.

## Disclosures
- The LPF noise figure (1.74e-15 m s⁻²/√Hz over 0.376 m) is quoted from memory and is provisional. The S2 SNR assumes white
  noise up to the crossing bandwidth, which is optimistic. S2 is context only.
- **M2 as frozen** ("the region becomes unbounded"): with T = 0 the field g_N,tot is uniform, so the S2 stress is identically
  zero. The script counts zero stress as the tooth biting. That tests "the S2 stress comes from the tide", not unboundedness.
  This wording is fixed here; the frozen file is unchanged.
- κ fitted; cold energy mass required; not theory closed.
