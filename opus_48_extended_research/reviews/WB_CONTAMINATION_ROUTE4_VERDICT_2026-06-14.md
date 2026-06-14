# Wide-Binary Contamination Model (Route 4) — Verdict

**C. Zimmerman machinery, 2026-06-14.** Script: `wb_contamination_route4.py`. numpy-only forward MC.
Both-ways honesty rule applied. Quarantine held (a0/Z never asserted derived; a0=9.36e-11 is the framework's
empirical pure-Lambda value).

## The two framework gammas (the load-bearing tension)
- g_ext(Sun) = 2.08e-10 = **2.22 a0_DE** (vs 1.73 a0_MOND) — lower a0 => deeper EFE suppression.
- Framework's **OWN derived (DSSYK-sharp / F4) interp: gamma = 1.084** (vel boost +4.1%). THIS is the honest number.
- The "banked gamma~1.32" is the **soft (simple-mu) interp: gamma = 1.336** — NOT the framework's own interp.
- So the framework's true forward signal is **gamma 1.08–1.34** depending on interp, with the own-interp end
  at 1.08 being *barely super-Newtonian*.

## Contamination calibration (validated against the real literature)
- f_multi (undetected close companion / triple fraction) ≈ **0.2–0.5** (Chae self-cal; Moe&DiStefano 2017; Raghavan 2010).
- Eccentricity: super-thermal **f(e)∝e^1.3** (Hwang 2022), median e=0.74, 22% e>0.9.
- Chance alignment: El-Badry R<0.1 cut; residual ~few% at widest s, broad high tail.
- **Independent cross-check PASSED**: my pure-Newton v-tilde_90 = **0.942** matches Chae's clean-binary 0.94±0.01;
  frac(v-tilde>0.9)=12.7% matches Chae's Newton ~12%.

## Result 1 — uncorrected contamination FAKES the framework signal from pure Newton
| f_multi | inferred gamma (from pure Newton) |
|---|---|
| 0.00 | 1.000 |
| **0.10** | **1.197** (fakes framework-own 1.08) |
| **0.20** | **1.507** (fakes even soft 1.34) |
| 0.30+ | 1.69 (saturates) |
At the survey-typical f_multi=0.2–0.5, uncorrected triples manufacture gamma ≥ 1.5 from a Newtonian population —
**larger than ANY framework prediction.** The test cannot confirm the framework without contamination control.

## Result 2 — cleaning CAN expose the signal, but the bar is interp-dependent
Recovered gamma at residual f_multi (0.30 / 0.10 / 0.05 / 0):
- Newton(1.00):            1.69 / 1.20 / 1.09 / 1.00
- framework-OWN(1.08):     1.69 / 1.28 / 1.17 / 1.08
- soft-interp(1.34):       1.69 / 1.56 / 1.44 / 1.34
At residual f_multi=0.05 the bias is +0.09 in gamma — **larger than the framework-own's entire signal (0.08)**.

## Result 3 — the REAL wall is the SYSTEMATIC f_multi floor, not statistics
- d(v90)/d(f_multi) = 0.89. Framework-own v90 gap vs Newton = 0.039; soft-interp gap = 0.147.
- **To expose framework-OWN gamma=1.08 you must know f_multi to ±4%** — HARDER than Chae's current ±5–10% self-cal.
- To expose soft-interp gamma=1.34 you need f_multi to ±16% — within reach of Chae-class self-calibration.

## DR4 separability (statistical SNR, clean f_multi=0.05; the OPTIMISTIC bound)
| comparison | 2k pairs | 8k pairs | 20k pairs |
|---|---|---|---|
| framework-OWN(1.08) vs Newton | 2.9σ | 5.8σ | 9.2σ |
| soft-interp(1.34) vs Newton | 10.9σ | 21.8σ | 34.5σ |
| soft-interp vs framework-OWN | 8.0σ | 16.1σ | 25.4σ |
| Chae-1.49 vs soft-1.34 | 4.6σ | 9.3σ | 14.6σ |
**These are statistics-only.** The systematic f_multi floor (Result 3) is the binding constraint:
framework-own's 2.9–9σ statistical separation is gated by needing f_multi to ±4%, which the current field cannot deliver.

## BOTTOM LINE (both ways)
- **NO manufactured win**: at the framework's OWN sharp interp, gamma=1.08 is barely super-Newtonian; its
  v-tilde signature (gap 0.039) is SMALLER than the contamination bias at survey-typical f_multi, and exposing it
  needs f_multi known to ±4% — beyond current control. On its own interp the lower a0 **does blunt** wide binaries
  toward a Newton-marginal, contamination-degenerate signal.
- **NO high-priest dismissal**: under the SOFT interp (gamma=1.34) the signal is robust — clean DR4 separates it
  from Newton at 10–30σ and needs only ±16% f_multi knowledge (Chae-achievable). And the framework's distinctive
  bet is the *low* end: a CLEAN Newtonian DR4 null at ~3% sensitivity KILLS soft-MOND while the framework-own
  SURVIVES (it lives at/below that floor) — an asymmetric, genuinely discriminating outcome.
- The discriminator is real but **interp-fragile and contamination-gated**, not a clean 3σ+ at the framework's own interp.
