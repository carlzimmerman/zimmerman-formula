# AX1 / BIMOND: FAIL on both footings. Alt fails G2a at E0 (1.19–1.20× Hees) for every candidate; canonical survives G1–G2 only with a sharper β ≥ 2.5 function and fails G4 on a PROVISIONAL published claim

Criteria `FROZEN_CRITERIA.md` + `../common/FROZEN_CRITERIA.md` (fd417eea04), committed alone before any script or number. Engine `../common/ax1_engine.py`. Outputs `ax1_BIMOND.{json,out}`, byte-identical rerun `ax1_BIMOND_RERUN.json` (SHA-256 de0ae361…), twin `ax1_BIMOND_MUTATE.{json,out}`. 10 s, one thread, no download. **Not blind**, and my by-hand expectation in the criteria came true on every line. κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. The cold sector stays retired. CMB and clusters out of scope, open.

## Result (both footings, exact footing a0)

| candidate static ν | G1 SPARC (D7c z vs the law) | G2a Q2 / Hees at E0–E3 (QUMOND) | G2b Saturn monopole / 7.0e-15 | survives G1–G2 |
|---|---|---|---|---|
| law, canonical | identity | 1.69, 2.64, 3.10, 3.68 **F** | 1.34e4 **F** | no |
| law + turn-off, canonical | identity | 1.70–3.70 **F** | 1.2e-4 P | no |
| β = 2.5 … 6, canonical | −0.19 to −0.39 P | 0.95–0.89 at E0, ≤ 0.77 elsewhere: P | ≤ 4.7e-6 P | **yes** |
| law, alt | identity | 1.91–4.02 **F** | 1.62e4 **F** | no |
| law + turn-off, alt | identity | 1.91–4.03 **F** | 2.2e-4 P | no |
| β = 2.5 … 6, alt | +0.86 to +1.17 P | **1.19–1.20 at E0 F** | P | no |

- G2c γ, α1, α2: P [PROVISIONAL, memory, not derived]. G3 Φ = Ψ: P [PROVISIONAL, memory].
- **G4: F [PROVISIONAL].** Chesler & Loeb 2017 (arXiv:1704.05116) conclude that BIMOND "in its present form is not an acceptable theory". I read only the snippet, not their argument.
- **Label: canonical FAIL [G4]; alt FAIL [G2a for every candidate].** The law's own ν fails G2 on both footings regardless of G4.

## Checks
K1 law QUMOND Q2 reproduces D7c / PAPER58's QUMOND numbers, max rel 3.8e-6. K2 β members, 40 cells, 6.9e-8. K3 grid doubling 5.3e-6. K4 spherical identity exact. B1 sympy flat split exact. MUTATE (ν ≡ 1): K1 and K2 fail, every Q2 is 0, exit 1. Rerun byte-identical. The macOS BLAS matmul raises spurious floating-point warnings; they are silenced in the script, and K1–K3 guard the numbers.

## Reading
- **The only non-v3s static escape on record lives here, and it is canonical-only.** A QUMOND-type limit with a sharper interpolation (β ≥ 2.5) passes Q2 at all four fields and matches the law on SPARC within D7c's line. But it is a different function from g²/(g + a0). D7c's secondary S1 statistic is against every β member (z −5.5 to −5.8), and on alt the framework's own Milky Way field (E0) breaks it by 1.19–1.20×. No β crosses that floor.
- **G4, argued (reported only, not a derivation).** On flat space with M′(0) = 0 the quadratic action splits exactly into a mode that couples with weight α + β and the difference mode δ = h − ĥ, and δ carries a share α/(α + β) of any matter-emitted wave (B1). The wave's own gradient acceleration 2π f h c at the detector is 3.0 / 2.5 a0 (GW150914) and 0.60 / 0.50 a0 (GW170817). So the δ mode sits in M's non-linear range along the path, which is where Chesler & Loeb place the problem. A speed for δ on a MOND-regime background is not derived here.
- G5: a0 enters M by hand.
