# QX20: the plain law's failure ladder is a STEP between hot and cold systems, not a curve in any measured variable

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (f3967a1aa9), frozen before any
script. Script: qx20.py, which imports QX5's QX16-fixed loaders read-only. One thread, about a minute.

**Label: NO SINGLE VARIABLE, on both footings.** None of the six measured variables tracks the missing boost. A power
law fitted on the hot systems (7 ellipticals, 20 groups, X-COP; 75 points) reaches the HO1 rms line on none of them,
and every one over-predicts SPARC's offset. Where SPARC and the hot systems overlap in a variable, the hot systems sit
**+0.32 to +0.37 dex** above SPARC at the same value of the variable (+0.18 in v_obs, which has only 48 overlapping
points). The plain law's miss is a **step between X-ray-hot systems and cold discs**. No continuous function of mass,
speed, gas fraction, g_N, r/r_M or potential depth produces it.

## Ranked table (canonical / alt)

| Rank | Variable | hot fit b | hot rms (line 0.10) | SPARC pred - obs (line 0.057) | Step in the overlap (hot - SPARC) | UDGs pred vs obs |
|---|---|---|---|---|---|---|
| 1 | V2 v_obs (sigma proxy) | +0.55 / +0.59 | 0.155 / 0.155 | +0.106 / +0.114 | +0.188 / +0.178 (48 pts) | -4.1 / -4.0 sigma |
| 2 | V6 depth Phi/c^2 | +0.23 / +0.25 | 0.145 / 0.143 | +0.136 / +0.140 | +0.343 / +0.322 | N/A (not on disk) |
| 3 | V1 M_b(<r) | +0.07 / +0.08 | 0.179 / 0.178 | +0.195 / +0.190 | +0.372 / +0.361 | -3.7 / -3.6 sigma |
| 4 | V4 g_N/a0 (= surface density) | -0.02 / -0.01 | 0.185 / 0.183 | +0.293 / +0.292 | +0.351 / +0.345 | -3.0 / -3.0 sigma |
| 5 | V3 f_gas | -0.00 / -0.00 | 0.185 / 0.183 | +0.299 / +0.294 | +0.355 / +0.346 | -3.0 / -3.0 sigma |
| 6 | V5 r/r_M | -0.16 / -0.19 | 0.176 / 0.173 | +0.315 / +0.313 | +0.340 / +0.336 | -3.3 / -3.3 sigma |

Every row reads STEP, and H and Z fail on both footings.

- **Class means (plain law):** SPARC +0.027 / -0.001, ellipticals +0.210 / +0.189, groups (f* = 0.5) +0.264 / +0.226,
  X-COP +0.467 / +0.435, Coma UDGs +1.12 / +1.08 (the UDGs are measured against the action with Coma's EFE).
- **Flat in g_N and in f_gas:** b is about 0 for both, so inside the hot class the offset is essentially flat. The
  0.18-dex scatter within the hot class is not ordered by either variable.
- **UDGs:** every variable predicts their offset 3-4 sigma too low. Nothing that fits the hot systems reaches the
  Coma UDGs (as QX5 iter_a2 found: F 22-26 against X-COP's 4).

## What a mechanism must hit (the target)

1. Zero boost in cold, rotation-supported discs (SPARC), at any value of the six variables.
2. About +0.2 to +0.45 dex of extra mass in X-ray-hot, pressure-supported systems at the SAME g_N, M_b, depth and
   r/r_M as discs. Within the hot class it is flat in g_N and f_gas, and weakly rising with v_obs and depth.
3. About +1.1 dex for UDGs embedded in Coma.

A key that is constant across discs and switches between "cold disc" and "hot system" is the only shape left. The
record's tries at hot keys (p/rho, QX5 b; host temperature, QX12 iter_2; virial heating, QX13) all failed, on the
profile shape or the groups. The Lean logic is QX5_monotone_sandwich (mono_dead / anti_dead): a monotone F(key) with
the cold and hot points overlapping in the key cannot be about 1 on one and >= 1 + delta on the other. Here the
overlap holds for all six variables (V2's is small).

## Known answers and controls

- KA1: class means equal QX16's fixed qx5 baseline (max |d| 4.3e-7 canonical, 4.5e-7 alt; QX16's printed values are
  rounded to 1e-6) -> PASS.
- KA2: the UDG mean equals S1's to 2e-16 -> PASS.
- M1 shuffle: the best variable V2 has shuffle fraction 0.000 on both footings. Its hot fit is informative, just not
  good enough. V4 and V3 are not informative inside the hot class (shuffle 0.44-0.67 and 1.000).
- M2 Newton (qx20_MUTATE.*): SPARC's mean becomes +0.431 and Z fails for every variable on both footings -> BITES.

## Disclosed

- The first run printed nan for V3. The ellipticals' f_gas = 0 with b < 0 gives an infinite x. Non-finite b candidates
  are now skipped (a code fix; no line or rule moved). That output is kept as qx20_first_run_fgas_nan.out.
- V2 shares M_obs with the offset, so part of its correlation is built in, as stated in the criteria.
- Ellipticals exclude hot gas (QX18): their offsets are upper bounds and their f_gas = 0.

Kappa = 1/2 FITTED; not theory closed.
