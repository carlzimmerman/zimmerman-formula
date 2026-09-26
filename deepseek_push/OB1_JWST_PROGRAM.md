# OB1 — JWST observation design (L05/K09 door)

**Spawned** by the conductor tick 2026-09-26 (Z-wave). House rules: LOOP_CONDUCTOR.md 1-10.
**Program verdict:** FEASIBLE-JWST: minimal registered config N=3, per-object S/N=10 (rate 0.9998, f=20); margin vs L03 pair reach S/N=50 is 5.00x

## 1. Minimal registered configurations (from L05 power grid, loaded, rate >= 0.95)

| f | N | per-object S/N | rate |
|---|---|---|---|
| 20 | 3 | 10 | 0.9998 |
| 15 | 10 | 10 | 0.9782 |
| 20 | 10 | 10 | 1.0000 |
| 15 | 30 | 10 | 1.0000 |
| 20 | 30 | 10 | 1.0000 |
| 20 | 1 | 30 | 0.9995 |
| 15 | 3 | 30 | 0.9940 |
| 20 | 3 | 30 | 1.0000 |
| 15 | 10 | 30 | 1.0000 |
| 20 | 10 | 30 | 1.0000 |
| 15 | 30 | 30 | 1.0000 |
| 20 | 30 | 30 | 1.0000 |

## 2. Reach fold-in (L03, loaded)

L03 jwst_reach_summary: pair reach S/N = 50 (q0), 50 (q2) -> SN_reach = 50.
Margin of the minimal registered config vs reach: 5.00x.

## 3. Falsifier schedule (K11 consolidated tests, verbatim)

- T1 J05/J06 width bound: E[D^2] >= B1 = 3E[Dv^2]^2/E[v^4] (density-free, source-agnostic); kill: measured E[D^2] < B1 at >=3sigma with model conditions verified -> Thomson reading dead for ANY density
- T2 J07 coherence envelope: |H(w)| >= max(0, 1 - w^2 L/2), L = 3E[Dv^2]^2/E[v^4], w E[D] < 1.5; kill: measured |H| below floor at >=3sigma -> conservative Thomson reading dead
- T3 J09-D central window: -lnA/dbar = (1+q/3)/(1/2+q/4) in [4/3,2], tau0-free, = inversion domain d/a in [1/2,3/4]; kill: >=3sigma outside [4/3,2] kills central quadratic-family reading (NOT any-geometry; general-p limit (p+2)/(p+1), J09p 21/21)
- T4 J11 geometry discrimination: volume window ~[1.3,1.9] tau0-CROSSING (2.049/1.894/1.629/1.423 at tau0 0.5-3 q=0; 1.897/1.710/1.314 at q=0/3/10 tau0=1; <chord>_vol=0.750000) vs central FLAT at 2.0022; shell TBD (K07); kill: curve missed at >=3sigma kills that geometry; single-window violation is a discriminator, NOT a framework kill
- T5 J10-I a0-radius: J10-I = (r_B/R)*window in [4/3,2], r_B = sqrt(G M_b / a0(rho_B)), a0 = (c/2)sqrt(G rho_B); kill: >=3sigma outside with M_b,rho_B independent -> framework BLR-radius assignment fails; sharp: R > (3/2)r_B kills q=0, R > 2 r_B kills all q

## 4. Kill condition (pre-registered in Z-WAVE_BRIEF.md)

Per-object S/N > 50 (L03 pair reach) at the minimal registered config -> INFEASIBLE-JWST.
This lane exits 0 only on a real pass; otherwise exit 1 with the honest verdict.
