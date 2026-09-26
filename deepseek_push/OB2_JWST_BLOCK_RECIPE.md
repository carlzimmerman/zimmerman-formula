# OB2 - JWST observing-block recipe (OB1 follow-through, conductor tick 2026-09-26)

**Pre-registration:** Z2-WAVE_BRIEF.md R1/R2/R3. All numbers loaded from disk.

## R1 - minimal registered config reproduced
- L05 power key `central_N3_SN10_f20`: rate 0.9998 == OB1 registered 0.9998 (PASS)

## R2 - per-target T5 falsifier schedule (K11 verbatim)
- T5 J10-I a0-radius: J10-I = (r_B/R)*window in [4/3,2], r_B = sqrt(G M_b / a0(rho_B)), a0 = (c/2)sqrt(G rho_B); kill: >=3sigma outside with M_b,rho_B independent -> framework BLR-radius assignment fails; sharp: R > (3/2)r_B kills q=0, R > 2 r_B kills all q
- Targets (L05 sample, S/N=10, first N=3):
  - obj 1: truth=central t=2.39 q=2.3 rb_ld=38.2 lag_d=97.2 J10I=1.838
  - obj 4: truth=central t=1.64 q=2.5 rb_ld=23.7 lag_d=43.5 J10I=1.790
  - obj 7: truth=volume t=1.50 q=0.0 rb_ld=319.4 lag_d=153.5 J10I=1.652

## R3 - exposure recipe (L05 budget, loaded)
- SN=10 blocks are the unit; SN=30 on the same target costs x5.0 the SN=10 time; depth doubling recipes per bar from the loaded dict

## Program statement
- Feasible per OB1; this recipe is the block-level realization.
- Kill channel: any target's J10I measured >=3sigma outside [4/3,2] -> that geometry's reading dead per T5 (single-window violation is a discriminator, NOT a framework kill).
