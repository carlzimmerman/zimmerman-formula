# Route 5 — Gaia DR4 Wide-Binary Forecast + Current-Data Confrontation

*Opus 4.8, 2026-06-14. Framework a0 = 9.36e-11 m/s^2 (= c^2 sqrt(Lambda/32pi), pure rho_DE). Built on banked
machinery (mi_f4_widebinary_efe.py, widebinary_chae2601_confront.py). Both ways — the lower-a0 tension reported
honestly. Calc: /tmp/dr4_forecast.py (numpy-only, reproducible). Quarantine held: a0/Z never asserted derived.*

## TL;DR (honest, both ways)
Wide binaries are **NOT a clean a0=9.36e-11 discriminator**. The framework's distinctness lives entirely in the
interpolation SHAPE (sharp vs soft), not in a0 — a0=9.36 vs 1.20 shifts gamma by only ~0.03-0.07, **below the most
optimistic DR4 systematic floor (~0.03-0.05)**. The framework's LOWER a0 makes its predicted signal the SMALLEST of
any MOND variant, pushing it CLOSEST to the Newton null and HARDEST to confirm. Currently gamma_framework sits in a
**no-win straddle**: ~2-3sigma BELOW the pro-MOND camp (Chae) AND ~1-2sigma ABOVE the Newtonian camp (Banik/PS) —
consistent-with-neither rather than consistent-with-all. DR4 is statistically capable but **systematics-limited**;
it will cleanly test the PREMISE (is there any low-a boost?) but is unlikely to cleanly isolate gamma=1.32 from
either Newton or standard-MOND.

## The mechanism subtlety that reframes the whole route
The framework is **modified inertia** with a **sharp (DSSYK/standard-mu) interpolation**. Run through the vector-MI
prescription at framework a0 (y_ext = g_ext/a0 = 2.22), the asymptotic deep-regime boost is:

| reading | gamma = G_eff/G_N (plateau) | vel boost | note |
|---|---|---|---|
| **MI-sharp (framework's OWN DSSYK interp)** | **1.083** | **+4.1%** | the framework's actual prediction |
| MI-soft (simple-mu, generic MOND-as-MI) | 1.337 | +15.6% | ≈ the prompt's banked "1.32" |
| QUMOND-soft (field-theory MOND) | ~1.067 | +3.3% | even weaker in transition regime |

**The prompt's banked gamma~1.32 is the SOFT-interp reading, not the framework's own.** On its own sharp
interpolation the framework predicts gamma~1.08 — barely super-Newtonian. This is the single most important honesty
correction: the framework's true WB signal is ~4x SMALLER than the 1.32 figure suggests.

## (1) Per-separation gamma(s) forward model (Mtot=1.5 Msun, framework a0, MW EFE)
```
 s[kau]  g_int/a0 | MI-sharp  MI-soft | QUMOND-sharp QUMOND-soft
      5     3.802 |   1.035    1.213  |    1.000        1.033
     10     0.951 |   1.085    1.334  |    1.000        1.053
     20     0.238 |   1.083    1.337  |    1.000        1.063
     30     0.106 |   1.083    1.337  |    1.000        1.066
```
gamma(s) rises through the transition (s~5-10 kau) to a plateau by s~10 kau. The discriminating regime is s~5-20 kau
(g_int ~ a0). MI-sharp plateaus at 1.083; the gap to Newton (gamma-1) is only **~0.08**.

## (2) Contamination model — the dominant systematic
The signal is a velocity-ratio excess. At s=10 kau the Keplerian velocity is v_kep=365 m/s; the framework MI-sharp
excess is only **+15 m/s** (+4%), soft-MOND is +57 m/s (+16%). An undetected close tertiary (m3~0.3 Msun at
a3~10 AU) adds a projected ~2000 m/s — **>500% of v_kepler**. Triples ONLY inflate the ratio -> they **bias gamma
HIGH (toward MOND)**. This is why stringent-cut analyses push gamma DOWN toward Newton. A residual contamination
bias of even +5-8% on gamma **swamps the framework's +8% MI-sharp signal entirely.** The field's own disagreement
(Chae 5.8sigma MOND vs Banik 16-19sigma Newton on overlapping data) is proof the error budget is
SYSTEMATICS-DOMINATED, not statistics-limited.

## (3) DR4 SNR forecast — statistics vs systematics
**Statistics-only (misleading):** with N~2000 clean deep-bin pairs at sigma_v=50 m/s (DR4 PM precision),
SNR(MI-sharp vs Newton)~13, N for 3sigma is only ~100 pairs. By counting statistics DR4 is trivially capable.

**Systematics-limited (the real forecast):** the floor is the residual contamination bias delta_gamma_sys
(Chae quotes +/-0.10 syst; Chae-vs-Banik disagreement ~0.4). Post-DR4 (epoch astrometry flags inner orbits)
optimistic floor ~0.03-0.05:

| comparison | \|dgamma\| | sys-SNR @floor=0.05 | @floor=0.03 | verdict |
|---|---|---|---|---|
| MI-sharp(1.08) vs Newton(1.0) | 0.083 | **1.7** | **2.8** | BLURRED→MARGINAL |
| MI-sharp(1.08) vs std-MOND-soft(1.37) | 0.287 | 5.7 | 9.6 | CLEAN (shape, not a0) |
| MI-soft(1.34) vs std-MOND-soft(1.37) | 0.033 | **0.7** | **1.1** | BLURRED (degenerate) |

The framework's own gamma=1.08 separates from Newton at only **~1.7-2.8 sigma** even at the optimistic DR4 floor —
**not a clean 3sigma+ discriminator from Newton.**

## (4) Current-data confrontation — where gamma sits NOW
| prediction | Chae24 (1.37±0.13) | Chae26 3D (1.60±0.16) | Banik24 (1.00±0.05) | PS/2602 (1.00±0.08) |
|---|---|---|---|---|
| gamma=1.32 (soft) | **−0.4σ** | −1.8σ | **+6.4σ** | +4.0σ |
| gamma=1.08 (framework MI-sharp) | **−2.2σ** | −3.2σ | **+1.7σ** | +1.0σ |

**The straddle:** gamma=1.32 (soft reading) is consistent with Chae but ruled out at 4-6sigma by Banik/PS.
gamma=1.08 (framework's own sharp reading) is disfavored ~2-3sigma by Chae AND mildly above the Newtonian camp by
~1-2sigma. **Neither reading is confirmed by the field; the framework is consistent-with-NEITHER camp**, sitting in
the contested gap. Given the camps contradict each other, "currently non-diagnostic / contested" is the honest
verdict — but it is NOT "consistent-with-all" (the prompt's degeneracy hypothesis): the framework is in mild tension
with BOTH the pro-MOND high gamma and the Newtonian null, depending on which interpolation you adopt.

## (5) BOTH-WAYS CRUX — does the lower a0 keep it clean or blunt it?
**It BLUNTS it**, three ways:
1. **vs Newton:** lower a0 shrinks the super-Newtonian excess (MI-sharp 0.124→0.083, a 33% reduction). The
   discriminating gap to Newton is already only ~0.08; the lower a0 makes the smallest-signal case smaller still.
2. **vs std-MOND:** if both are read soft, framework gamma=1.34 sits only 0.03-0.06 below std-MOND's 1.37-1.4 —
   MOND-DEGENERATE (~0.5-1.1 sys-SNR, below any DR4 floor). Separation from std-MOND requires the SHARP interp
   (the framework's distinctive claim), NOT a0.
3. **The a0 lever itself:** gamma(9.36) vs gamma(1.20) differ by only ~0.04-0.07 — **below the optimistic DR4
   systematic floor.** WB cannot measure the framework's a0.

## Verdict
- **DR4 decisive on the PREMISE, not on a0.** DR4 (Dec 2026, + ground RV follow-up for 3D) can cleanly answer "is
  there any low-acceleration boost?" at the systematic floor. It CANNOT cleanly isolate gamma=1.32, nor measure
  a0=9.36e-11, because the a0 lever (~0.04-0.07 in gamma) sits below the floor.
- **The framework is NOT cleanly distinguished from Newton by WB** at its own sharp interpolation (1.7-2.8 sys-SNR).
- **The framework is MOND-degenerate** against standard MOND unless one trusts the sharp-vs-soft interpolation shape.
- **The lower a0 is a genuine downside here, not a win:** it makes the framework's WB signal the smallest of any
  MOND variant, closest to the Newton null, hardest to confirm. Reported honestly per the #1 rule.
- The strongest framework-distinctive WB bet is the **DR4 fork** (pre-registered in mi_f4_widebinary_efe.py): a
  clean null at ~3% sensitivity SURVIVES for the framework (sharp) but KILLS soft-MOND; a +10-15% boost KILLS the
  framework (sharp) and confirms soft-MOND. That fork tests the SHAPE, not a0 — and a clean Newtonian-leaning DR4
  result would be a serious blow to the framework's PREMISE (local low-a boost), the foundation the a0(z) program
  assumes.

*Sources: Chae 2024 ApJ (arXiv:2402.05720, gamma=1.37±0.13, 5.8σ, N=6389); Chae 2026 (arXiv:2601.21728,
gamma=1.60+0.17/-0.14, 4.9σ, N=36 3D); Banik 2024 (MNRAS 527, alpha_grav=-0.021, MOND excluded 16-19σ, N=8611);
Pittordis-Sutherland 2023 (arXiv:2210.07781); "No evidence for MOND" 2026 (arXiv:2602.24035, Newtonian null,
N~900 stringent). El-Badry 2021 catalog ~1.3M bound pairs, ~26,615 within 200pc, clean MOND-test subset few
thousand. DR4 Dec 2026: ~3-5x PM precision over DR3; 3D test still needs ground RV <100 m/s (Gaia RVs ~km/s).*
