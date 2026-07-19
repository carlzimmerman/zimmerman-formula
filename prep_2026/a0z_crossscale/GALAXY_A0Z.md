# Galaxy-side a0(z): the Λ-blind BTFR-zero-point measurement

**Lane of the cross-scale a0(z) test** (de Sitter–Unruh modified-inertia framework, C. P. Zimmerman).
Backing script: `galaxy_a0z.py` (exit 0, numpy/scipy, both footings). Figure: `galaxy_a0z.png`.

## The test (non-circular content)
The framework forces the galaxy acceleration scale to track the cosmic dark-energy density,
a0(z) = c²√(ρ_DE(z)/32π) ⇒ **a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE0)**. ΛCDM gives *no* reason for a galaxy's
acceleration scale to track cosmic expansion; the framework does. The **galaxy-side** measurement is the
BTFR zero-point at each z: in the deep-MOND regime V⁴ = a0·G·M_bar is exact (slope forced to 4), so
**a0(z)/a0(0) = (V_z/V_0)⁴ / (M_bar,z/M_bar,0)** read straight off the zero-point.

Confronted against two cosmic tracks: **flat-Λ → 1.0** (w=−1) vs **DESI-DR2 evolving → 0.69 at z=3.25**
(declining). Framework distinctive prediction: **a0(3)/a0(0) ≈ 0.60–0.75** (V ≈ −7%, −0.03 dex below the
z=0 BTFR at fixed M_bar). Alt cH0 footing instead **rises** (a0∝cH(z)·E(z) → ~5× by z≈3).

## Data compiled (galaxy-side a0(z)/a0(0))

| z | source | N | a0(z)/a0(0) | ±dex | clean deep-MOND? |
|---|---|---|---|---|---|
| 0.0 | **SPARC** BTFR (Λ-blind, gas-dom dwarfs) | 175 | **1.00** (anchor) | 0.07 | **yes** |
| 0.9 | Übler+2017 KMOS³D bTFR (fixed slope 3.75) | ~120 | 2.75 [2.5,3.0] | — | no (g≳a0) |
| 1.0 | Di Teodoro+2016 / Tiley+2019 (null) | ~tens | ~1.0 | 0.10–0.15 | no |
| 1.5 | Sharma+2024 bTFR (free slope 3.21) | ~100 | 0.07 [0.02,0.28] | — | no |
| 2.3 | Übler+2017 KMOS³D bTFR (fixed slope 3.75) | ~30 | 1.86 [1.7,2.1] | — | no (g≳a0) |
| 3.25 | **Big Wheel** V⁴/GM_bar (clean RC) | 1 | **1.31** (+0.93/−0.52) | 0.23 | **yes** |

(Übler Δ_b = −0.44, −0.27 dex below local bTFR at fixed V; naive slope-4 map → a0 above local.)

## The crux caveat — why intermediate-z is NOT a clean a0 probe
The map a0 = V⁴/(G M_bar) requires the fitted BTFR slope to be **exactly 4** (deep-MOND). The massive
z~1–2.3 rotators sit at **g ≳ a0** (not deep-MOND); their fitted slopes are **3.0–3.85, not 4**, and the
zero-point is then **degenerate with the slope/pivot and with baryon/DM-fraction evolution**. The *sign*
of the inferred "a0 evolution" **flips with the analysis**: Übler (fixed slope 3.75) → a0 **rising** ~2–3×;
Sharma+2024 (free shallow slope 3.21) → opposite; Di Teodoro+2016 / Tiley+2019 (V/σ>3) → **null**. The
scatter across analyses (factor ~2–3, *either* direction) dwarfs the 0.70-vs-1.0 signal. **Only clean
deep-MOND objects read a0**: SPARC dwarfs (z=0) and the Big Wheel (z=3.25, large low-acceleration RC).

## Does the data show the zero-point shifting (a0 declining)?
**No detection, either way.** z=0 is solid at 1.0; z=3.25 (clean, single object) is ~1.0–1.3, **consistent
with flat, disfavors the 5× rise (~2σ, banked), and cannot see the 0.70 decline** — the ~2× M_bar
systematic on one object is itself larger than the 0.30 decline signal. The intermediate-z BTFR is
systematics-dominated and **sign-contested**; its naive fixed-slope reading leans *rising* — the **wrong
sign** for the framework's decline — but is not a valid a0 measurement. The predicted decline
(a0(3)/a0(0)≈0.70, −0.15 dex) is **NOT detected**; the data are consistent with **both** flat and the
decline. **The galaxy-side test is currently underpowered — not passed and not failed.**

## Both footings
Reported as **ratios** a0(z)/a0(0), so the footing (canonical 9.36e-11 / alt 1.13e-10 / SPARC 1.181e-10)
**cancels**. It re-enters only in the Big Wheel's absolute value: a0_eff = 1.54(+1.10/−0.61)e-10 gives
a0(3.25)/a0(0) = **1.31** (vs SPARC), **1.65** (vs canonical), **1.37** (vs alt) — all consistent with
constant on their own footing. The alt cH0 footing (rising) is the one the Big Wheel disfavors.

## M_bar, IMF, dust, and distance caveats (stated plainly)
- **M_bar is the dominant systematic at high z**: gas fractions (CO α_CO, dust-based), IMF, and SED
  stellar masses (over-estimated for the Big Wheel — M_dyn caps M_star below the SED value). The Big
  Wheel a0 error is ~2× from M_bar alone.
- **Distance ⇒ mild cosmology dependence**: M_bar ∝ D², and D(z) needs a cosmology. But this test asks
  whether galaxy-a0 *tracks* ρ_DE(z); it does **not** assume the DE evolution — so it is **not circular in
  the fatal sense** (a wrong background shifts all points together, it does not manufacture a decline).
- **Velocity definition / pressure support**: high-z σ is large; asymmetric-drift corrections and the
  V/σ cut move the zero-point by tenths of a dex (Tiley's null vs others' evolution).
- **a0 magnitude inherits the posited Z** (the coefficient is not derived here); only the *ratio* is tested.

## Forecast (the decisive future test)
To detect a0(3)/a0(0)=0.70 (0.15 dex) at **3σ** vs flat: σ_mean = 0.052 dex ⇒ **N≈4** clean deep-MOND
rotators per z~2–3 bin at SPARC-like M_bar precision (0.10 dex), or **N≈24** at realistic high-z
per-object precision (~0.25 dex). Feasible: JWST/ALMA already yield ~tens of z~2–3 gas-traced rotators;
**ELT/HARMONI** resolves individual outer (deep-MOND) rotation curves. A sample of **~20–40 clean
deep-MOND z~2–3 disks** (Big-Wheel-like), with M_bar to ~0.1 dex, reaches 3σ on the declining track.

## Credits
Milgrom 1999 (ν-kernel + BTFR, a0∝√ρ_vac); McGaugh & Lelli (SPARC BTFR); Übler+2017, Tiley+2019,
Di Teodoro+2016, Sharma+2024 (high-z TFR); Big Wheel (arXiv:2409.17956); Limbach–Psaltis–Özel 2008
(a0∝√ρ_DE); Brout+2022 / DESI DR2 (ρ_DE(z)).
