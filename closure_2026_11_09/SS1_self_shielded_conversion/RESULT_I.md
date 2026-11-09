# SS1 variant I RESULT: FAIL / FAIL (first failing gate: KiDS), in every reading

AMENDMENT_A5 0499ce563c (committed alone before any I number). Criteria b5adc7a90b. TEST lane, quarantined; adopts nothing; no
particle adopted. kappa = 1/2 FITTED; not theory closed. Footings never pooled.

I is the outside source's round 12, written against SS2's numbers. Its pieces:
- G's onset and rate (z_dec 0.631, alpha 4.367 / 4.366);
- kick 1 x v_stiff;
- capped retention f(r) = e^-alpha + (1/sqrt3 - e^-alpha) exp(-3 (v_stiff/v_vir)^2 / g(r));
- daughters under A4's bound rule; unbound ones in a shell at R_FS.

## Labels

| reading | canonical | alt | constants beside the label (orchestrator flags) |
|---|---|---|---|
| **I-core** (own-halo g, bound rule; graded) | **FAIL at 1 KiDS** | **FAIL at 1 KiDS** | 1 fitted (the 1/sqrt3 ceiling, chosen after SS2's over-fill) + form choices (factor 3, exponential law, kick factor 1, G's cube root / 4 pi) |
| I-src (the source's g_vir) | FAIL at 1 KiDS | FAIL at 1 KiDS | 3 fitted (1/sqrt3, 0.07, 0.45) |
| I-nob (the source's accounting: bound daughters dropped) | FAIL at 1 KiDS | FAIL at 1 KiDS | I-core's + an accounting the bound-daughter physics does not allow |

## I-core (canonical / alt)

| gate | canonical | alt |
|---|---|---|
| **1 KiDS** | **FAIL** max 0.350 (21/59 over); per bin at 0.3 / 1 / 1.5 Mpc: 9.4 +0.011 / +0.011 / +0.011; 10.45 +0.019 / +0.030 / +0.177; 10.7 +0.045 / +0.054 / +0.188; 10.9 +0.086 / +0.090 / +0.183 | **FAIL** max 0.342 (19/59); 1.5 Mpc +0.14 to +0.15 |
| 2 groups | FAIL 3/20, 0/20; median -0.12 / -0.28 (over-filled) | FAIL 3/20, 0/20 |
| 3 X-COP | FAIL mean -0.214; bins -0.30, -0.15, -0.16 (as G) | FAIL -0.233 |
| 5 SPARC | FAIL rms 0.0673 (line 0.0660): the bound 10-15 % of galaxy daughters stay inside | FAIL 0.0704 (0.0658) |
| 5b Ursa Major | PASS (-0.015) | PASS (-0.020) |
| 6 background | PASS (mass kept) | PASS |
| 7(b) lensing | NO VERDICT (no validated method) | NO VERDICT |
| 8 forest + fsigma8 | PASS: 51 % of the component escapes but only to lambda 1.67 Mpc; sigma8 0.791 (ratio 0.979), S8 0.811; Rf BGS 0.940, LRG1 0.993 | PASS: sigma8 0.788, S8 0.808 |
| 9 Bullet | FAIL (DB1 cls FAIL; M300 Z +1.56, -0.90) | FAIL |
| 10 Cassini | PASS | PASS |

**Why.** A kick of v_stiff (266 / 288 km/s) is below the escape speed of every group and cluster halo, so all of their
daughters stay bound and they keep their whole share. That is why groups and X-COP are over-filled exactly as in G and H, and
why the 1/sqrt(3) ceiling has no effect (MI1: NO BITE). In galaxy halos, 85-90 % of the share escapes with little excess
energy and lands in a shell near R_FS 1.7-1.8 Mpc. That shell sits right on the isolated-lens outer bins: +0.18 dex at
1.5 Mpc in every massive bin. The source's own round-11 number for a v_stiff kick was +0.13 at 1 Mpc. Its round-12 +0.038 at
1.5 Mpc is not reproduced.

## The source's claims, computed

| claim | source | lane (canonical / alt) |
|---|---|---|
| R_FS | 1.68 / 1.82 Mpc | 1.673 / 1.814 (KA-I3, reproduced) |
| KiDS 1-halo retained at M* 10^11 / 11.3 / 11.5 | 1.3 / 2.1 / 4.0 % | primary halos 16 / 34 / 47 % (bound daughters included; 12 / 27 / 40 % alt); Moster halos 95-100 % |
| Delta Sigma-like shift at 1.5 Mpc, isolated lens | +0.038 | +0.18 / +0.23 / +0.26 (primary, by M*); about +1 dex on Moster halos |
| groups 2e13 / 4.5e13 / 1.4e14 | 22 / 32 / 45 %, residuals near 0 | 100 % inside R500 with bound daughters (I-core); 2-13 % under I-nob (residual +0.26 / +0.06: under-filled) |
| X-COP retained / M_dyn | 0.71 / 0.65 / 0.46 | 1.57 / 0.90 / 0.75 (I-core); 0.74 / 0.44 / 0.34 (I-nob) |
| sigma8 ratio, S8 | 0.95, 0.769 | 0.979, 0.811 (I-core); 0.970, 0.803 (I-nob) |

## I-nob (the source's accounting, bracket)

The source's X-COP "G x 0.5" needs bound daughters to be dropped from their cluster. With that accounting:
- X-COP PASSES (mean -0.007 / -0.023, rms 0.095 / 0.095; bins -0.07, +0.05, +0.02), and TR1's shape still follows;
- groups collapse (1/20 and 3/20; small groups keep 2-13 %);
- KiDS still FAILS (shelf +0.14 to +0.17 at 1.5 Mpc);
- the Bullet FAILS (M300 Z -1.3, -3.1).

A daughter with E < 0 does not leave its halo, so this reading is not the construction's own physics.

## MUTATE and known answers

- **MI2 (kick -> 0): BITES.** KiDS 0.378 and SPARC FAIL.
- **MI1 (ceiling -> 1): NO BITE.** The fitted ceiling changes nothing in I-core, because bound daughters already keep every
  group and cluster full.
- **KA-I1:** formula reproduced.
- **KA-I2:** law-only replay PASS.
- **KA-I3:** R_FS reproduced.

## Reading

- **I's slower kick keeps daughters bound** in groups and clusters (over-fill), and puts the escaping galaxy share into a
  1.7-1.8 Mpc shell. That shell fails KiDS at the outer bins, as the source's own round 11 found.
- **Its gains** are growth and S8 (the short streaming length).
- **Under the source's accounting** X-COP would pass, but groups would empty and KiDS would still fail.

**What a repair would need:**
- galaxies must lose their share to somewhere other than 0.2-2 Mpc around them, and not into the small-scale field;
- groups must keep 30-85 %, against the about 100 % (bound) or about 5 % (dropped) that this class gives.

Files:
- AMENDMENT_A5.md, ss1v.py (I branch), ss1i_grade.py, run_i_chain.sh;
- ss1i.json / .out, ss1i_MUTATE.json / .out, parts/*_VI*, *_I*, *_MI*.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
