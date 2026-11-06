# QX23: is the law's hot/cold step keyed on cold gas (A), or a baryon gap (B)? NEITHER, on both footings

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: iter_1/FROZEN_CRITERIA.md (e01a2a59a7), committed and
pushed before any script. Script: iter_1/qx23.py (one thread, about a minute). Outputs: iter_1/qx23.out / qx23.json, and
qx23_MUTATE.* for M1-M3. A rerun gives a byte-identical qx23.json. Data are all on disk; nothing was downloaded.

## Label: NEITHER
Neither reading survives the frozen tests.
- **(A) Cold-gas key: KILLED across the f_HI range SPARC samples.**
- **(B) Uncounted-baryon gap: EXCLUDED** in every class against the stated ceilings, including both dSph classes.

### T1 (graded): SPARC, cold-gas fraction at fixed g_bar
Sample: 145 galaxies (QX20's anchor sample); 17 have f_HI < 0.10 and 90 have f_HI > 0.30.

| | canonical | alt |
|---|---|---|
| D1 (gas-poor minus gas-rich, dex) | +0.053 +- 0.038 | +0.049 +- 0.032 |
| A, M-step prediction | +0.351 (z -7.9) | +0.345 (z -9.1) |
| A, M-lin prediction | +0.268 (z -5.7) | +0.263 (z -6.6) |
| Label | A KILLED in SPARC's range | A KILLED in SPARC's range |

- In SPARC, gas-poor and gas-rich galaxies sit on the law alike at fixed g_bar. The partial Spearman is rho -0.02 / -0.08,
  p 0.82 / 0.34.
- A cold-gas key sized to QX20's step would show up here at 6-9 sigma.
- **Scope:** the kill covers the f_HI range SPARC samples. Its gas-poorest galaxies reach f_HI of about 0.01-0.1, all of them
  disc galaxies. A key that switches on only below that range, or only in non-disc systems, is not excluded by T1. That would
  be a morphology or type key, not a gas key.

### T2 (graded): LG field dwarfs with measured HI (LVD)
- Measured HI reassigns QX22's provisional types:
  - Leo T and Aquarius are gas-RICH (M_HI/M* about 1.5 / 1.3).
  - Antlia B, Pegasus dIrr, IC 1613, Leo A, NGC 6822 and WLM fall between the thresholds (0.1 to 1).
  - gas-poor: Cetus, Phoenix, Tucana, UGC 4879; gas-rich: Aquarius, Leo T, Sagittarius dIrr.
- **QX22's "+0.13 gas-poor vs -0.03 gas-rich" does not survive measured HI.**
- D2 (poor minus rich) = -0.050 / -0.051 +- 0.19 dex, with n 4 / 3. The label is NO VERDICT, since there are too few systems
  for 3 sigma either way.
- The bracket with all HI counted inside r_h is +0.23. It is an upper bound: the HI in dIrrs is mostly outside r_h.
- **Reported, not graded:** the satellites are almost all gas-poor (MW classical 8/8, bright M31 24/25), so their
  +0.20 / +0.22 step cannot be split by gas inside the satellite classes. The step there is confounded with host proximity
  and stripping.

### T3: NOT RUN
HI-MaNGA is not on disk (NEEDS_OWNER.md).

### T4 (graded against stated ceilings): reading B, uncounted baryons needed to null each class's step

| Class (canonical; alt within 0.06) | Delta | k (counted baryons x) | ceiling on uncounted | B |
|---|---|---|---|---|
| X-ray ellipticals | +0.18 | 1.72 | 0.2 | EXCLUDED |
| groups | +0.24 | 2.67 | 0.3 | EXCLUDED |
| X-COP | +0.44 | 4.76 | 0.3 | EXCLUDED |
| bright M31 dSphs | +0.20 | 2.50 | 0.1 | EXCLUDED |
| MW classical dSphs | +0.22 | 2.72 | 0.1 | EXCLUDED |
| LG gas-poor field dwarfs | +0.05 | 1.28 | 0.1 | EXCLUDED (0.28 vs 2 x 0.1; least secure) |

- The dSphs would need 1.4-1.7 times their stellar mass in invisible baryons inside r_h, and they hold no detected hot or
  cold gas. A baryon gap cannot carry the dSph step unless the baryons are dark (compact objects), which is a different
  hypothesis and not tested.
- The ceilings are literature-level bounds fixed in the criteria, not graded data.

## Reading (post-data, not the label)
The step does not follow cold gas inside SPARC, and it does not follow measured HI in the LG field. Undetected baryons
cannot carry it at stated ceilings. Every variable tried so far fails to separate the classes inside their own ranges:
- QX20: mass, field, depth, r_M, total gas;
- QX22: support;
- QX23: cold gas.

What still separates them is class membership itself:
- discs and field dIrrs on the law;
- satellites, ellipticals, early-type lenses and hot systems above it.

Two candidates are left untested:
- host environment, which covers satellite dSphs, cluster and group members, and early-type lenses that sit in denser
  environments;
- morphology or type as such.

The LG field gas-poor dwarfs (Cetus, Tucana, Phoenix, UGC 4879) sit only +0.05 above the anchor, against +0.20 to +0.22
for the satellites. That points toward environment, not gas. It is four systems, and post-data.

## Known answers and controls
- KA1: the SPARC mean reproduces QX20's sparc_mean exactly (|d| 0), both footings.
- KA2: QX22's T4 provisional medians are reproduced exactly.
- M1 (f_HI shuffled): D1 -0.024 / -0.022, inside 2 sigma. PASS.
- M2 (+0.20 dex planted into gas-poor galaxies): D1 rises by +0.2000. PASS, so T1 has power.
- M3 (Newton): the SPARC mean moves +0.40 / +0.43. PASS.

## Not covered
- SPARC f_HI uses total HI against 0.5 L[3.6]; no molecular gas.
- T2 uses LW1's stars-only baryons and its plain-law offsets (no EFE).
- MaNGA HI (T3) is not run.
- No environment control. That is the next target.

Kappa = 1/2 FITTED; not theory closed.
