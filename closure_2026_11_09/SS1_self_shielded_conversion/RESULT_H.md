# SS1 variant H RESULT: H-core FAIL / FAIL (first failing gate: groups); H-full FAIL / FAIL (first failing gate: KiDS)

AMENDMENT_A4 8bcceec033 (committed alone before any H number). Criteria b5adc7a90b. TEST lane, quarantined; adopts nothing; no
particle adopted. kappa = 1/2 FITTED; not theory closed. Footings never pooled.

H is the outside source's answer to SS1's repair list:
- G's onset and rate on the record's footings: z_dec 0.631, alpha 4.367 / 4.366, v_stiff 265.8 / 288.1 km/s.
- No switch. Instead, a smooth per-radius escape retention in the pre-conversion halo:
  f(r) = exp(-(alpha/pi)(v_stiff/v_vir)^2 / g(r)), with g = sigma(r)^2 / v_vir^2.
- An explicit bound-daughter rule (A4): a daughter with E = (1/2)(3 sigma^2 + v_kick^2) + Phi < 0 stays where it was made.

## Labels

| construction | canonical | alt | form choices beside the label |
|---|---|---|---|
| **H-core** (graded) | **FAIL at 2 groups** | **FAIL at 2 groups** | 0 fitted; 1/pi, exponential escape law, G's cube root / kick factor 4 / 4 pi |
| H-full (bracket: named added forms) | FAIL at 1 KiDS | FAIL at 1 KiDS | + resonant window v_vir > v_stiff/2, 180 kpc puff core, kick factor 2 |
| H-src (bracket: the source's fitted g_pot) | FAIL at 2 groups | FAIL at 2 groups | + the source's g_pot(u) = u/(0.08 + u)/(1 + 2.5 u^1.5) |

## H-core (canonical / alt)

| gate | canonical | alt |
|---|---|---|
| 1 KiDS | PASS (galaxy-scale halos drain completely: max shift 0.000) | PASS |
| **2 groups** | **FAIL** 7/20 (f* 0), 3/20 (f* 1); median +0.05 / -0.19 | **FAIL** 6/20, 3/20; +0.05 / -0.20 |
| 3 X-COP | FAIL mean -0.214; bins -0.30, -0.15, -0.16 (clusters keep everything, as in G) | FAIL -0.233 |
| 5 SPARC | PASS rms 0.0561 (line 0.0660) | PASS 0.0558 (0.0658) |
| 5b Ursa Major | PASS (Delta_pred -0.000) | PASS |
| 6 background | PASS (mass kept) | PASS |
| 7(b) lensing | NO VERDICT; reading 8.47 | NO VERDICT |
| 8 growth | FAIL: 69 % of the component escapes (58 % of matter); sigma8 0.640, S8 0.657; Rf BGS 0.09, LRG1 0.48 | FAIL: sigma8 0.624; Rf -0.00, 0.39 |
| 9 Bullet | FAIL (DB1 cls FAIL; Z +1.56, -1.16) | FAIL |
| 10 Cassini | PASS | PASS |

**The question the orchestrator called the real one: do daughters stay bound in their own halos?** Bound fractions on
SS1's primary SIS halos, canonical (alt within a few %):

| M_b | v_vir | bound at kick v_stiff | 2 v_stiff | 4 v_stiff (H-core) |
|---|---|---|---|---|
| 1e11 | 129 km/s | 0.15 | 0.00 | 0.00 |
| 1e12 | 277 | 0.80 | 0.20 | 0.00 |
| 1e13 | 597 | 1.00 | 0.86 | 0.26 |
| 1e14 | 1285 | 1.00 | 1.00 | 0.91 |

- **Galaxies:** no kick at or above v_stiff keeps a galaxy halo's daughters (v_vir < 300 km/s) bound. In H-core they all
  escape and stream about 6.7 Mpc, so growth fails as in G.
- **Groups and clusters:** they keep their bound daughters in place. Clusters therefore retain essentially everything, and
  X-COP is over-filled exactly as in G: retained / M_dyn 1.57 / 0.90 / 0.75 against TR1's 0.71 / 0.66 / 0.58. TR1's SHAPE
  statistic still FOLLOWS (RMS 0.075 / 0.071).

**Group retention inside R500** (f* 0), by pre-conversion R500: 200 kpc 0.13, 217 kpc 0.18, 253 kpc 0.30, 283 kpc 0.41,
338 kpc 0.61 (canonical); alt 0.09-0.52.
- These sit at or below the source's claim. KA-H3, from the escape law on the source's own masses: M500 2.1e13 gives 0.40 /
  0.34 (source 42-48 %), and 1.4e14 gives 0.77 / 0.74 (source 79-82 %).
- Small groups now fall below their need while the rest still over-fill, so only 7/20 and 3/20 pass.

## H-full (bracket)

- **KiDS FAILS** at +0.27 to +0.35 dex at 0.3-1.5 Mpc in every lens bin (the source claimed < +0.035). Halos below the window
  (v_vir < 133 / 144 km/s on primary halos) keep their 4.1 M_b puffed into the 180 kpc core. That is the WD1 rung: the
  isolated-lens outer bins see the puffed component.
- **SPARC PASSES** (rms 0.0569): the core is too large to matter inside the last measured radius.
- **Growth PASSES.** 19.7 % of the component converts and escapes (16.6 % of matter; the source claims 16 %). sigma8 0.787 /
  0.782, S8 0.807 / 0.802 (the source claims 0.766-0.771 / 0.78). Rf BGS 0.89, LRG1 0.97.
- **Groups FAIL** (6/0: at kick 2 v_stiff most group daughters stay bound, so groups over-fill). X-COP and the Bullet FAIL.

## H-src (the source's g_pot)

Groups 5/4 and 4/3 (median +0.09 / -0.16): FAIL. Growth FAILS (sigma8 0.635). The rest is as H-core.

## MUTATE (ss1h_MUTATE.out)

- **MH1 (v_stiff -> 0, no conversion): BITES.** KiDS 0.378 and SPARC FAIL.
- **MH2 (kick -> 0, every daughter bound): BITES.** Growth goes to PASS (sigma8 0.808), and KiDS / SPARC FAIL because
  galaxies keep their share.

## Known answers

- **KA-H1:** the code's SIS retention equals exp(-(2 alpha/pi)(v_stiff/v_vir)^2) (identical to print precision at every test
  mass; the bound daughters are added separately).
- **KA-H2:** law-only replay PASS.
- **KA-H3:** as above, 0.40 / 0.77 against the source's 42-48 % / 79-82 %.

## Disclosure: fsigma8 derivative corrected for every variant (labels unchanged)

**What was wrong.** While grading H-full, its fsigma8 FAIL came from LRG2 (z 0.706, before onset) reading Rf = 1.002 against
the 1.001 cap. Before onset the ratio must be exactly 1. The coarse-grid (dz about 0.17) cubic-spline derivative of sigma8
rang across the onset kink.

**The fix.** fsigma8 now comes from central differences on a fine low-z grid (dz 0.005) recorded inside the growth ODE.
Before-onset rows now read exactly 1.000. This is a numerical fix, not a construction change.

**Reruns.** Every variant cosmology was rerun:
- SS1 B-G, MG1-4 and the M_min 1e10 brackets;
- SS2's G set.

**Effect on the labels.** No B-G or SS2 label changes.
- D's growth gate flips FAIL -> PASS (BGS 0.53, LRG1 0.97), but D still fails first at KiDS.
- G's growth FAIL is unchanged (Rf BGS 0.090 / 0.008).

The coarse-spline values are kept in each JSON as `Rf_coarse_spline_reported`.

## Reading

H fixes neither failure the repair list named.
- **Groups and clusters.** Whatever H converts in a group or cluster stays bound there (v_esc > kick), so clusters keep their
  whole pre-conversion share and stay 1.3-2x over-filled. Groups split: small ones drain below their need, large ones
  over-fill.
- **Galaxies.** Daughters cannot stay bound in galaxy halos, so H-core's conversion of every sub-threshold halo erases
  small-scale growth as in G.
- **The H-full fix.** H-full's window rescues growth (about 17 % of matter converts) only by keeping the small halos' share in
  a 180 kpc core, which fails KiDS by 0.3 dex.

**What a repair would need:**
- Galaxies must lose their share without it either leaving the small-scale matter field (growth) or sitting at 0.2-1.5 Mpc
  (KiDS). Within this class those two requirements conflict.
- Clusters must keep only about half of their share, which a v_esc-bound daughter cannot give.

Files:
- AMENDMENT_A4.md, ss1v.py (H branch), ss1h_grade.py, run_h_chain.sh, run_fs8_fix_chain.sh;
- ss1h.json / .out, ss1h_MUTATE.json / .out, parts/*_VH*, parts/*_H*, parts/*_MH*.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
