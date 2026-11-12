# FINAL-7 RESULT: what the medium IS — the M5 hypothesis triage

**Lane label — canonical / alt, in the frozen vocabulary of criteria §6:
NO MEDIUM — CLOSED AT (ii) MOMENTUM-CONSERVING / NO MEDIUM — CLOSED AT (ii) MOMENTUM-CONSERVING.**

The one structural gate the brief asked to grade, **K6 (no ghost, no superluminal), HOLDS** on both
footings. Every other pre-registered kill fires: K1, K2, K3, K4, K5, K7. The elastic solid is
dynamically healthy and physically impossible, which is the outcome the criteria predicted in §1.

**The finding, in one line.** No medium carries the law's static halo. The only carrier compatible with
property (2) (interpenetration — the Bullet) is the **sourced field** `-Pi = T[phi]`, `grad phi = g`;
it passes (2) and (4) and fails (1) and (3). So the class of media is closed, and `sigma_r^2 < 0` is a
**radial tension along grad Phi** (the field's Maxwell tension), not a velocity dispersion.

TEST lane, quarantined. Criteria `FROZEN_CRITERIA.md`, committed alone before any FINAL-7 script or
number. Footings graded separately, never pooled (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10
m/s^2). Cold dark energy is a gravitating field component, never a particle. kappa = 1/2 FITTED; not
theory closed. Adopts nothing.

**No new compute.** This file reads `fin7.out`, `fin7.json` and the five `fin7_MUTATE_M*.out/.json`
already in the folder. Nothing was re-run.

---

## 1. The pre-registered kills

| # | kill | expectation | result |
|---|---|---|---|
| K1 | the solid is not elastic: its own solution strains it by \|u\| >> 1 | FIRES | **FIRES** (max \|u\| 120–249 over the 24 rows) |
| K2 | the Bullet: no material continuum interpenetrates; at 4700 km/s it yields | FIRES | **FIRES** (Q3a homeomorphism: a solid delivers 0 of the >= 1.4715e14 Msun the data require; Q3b Mach 11.9–26.0, Y = 141–677) |
| K3 | property 1: a carrier with no material identity has no conserved cold rest mass | FIRES | **FIRES** (see §3) |
| K4 | property 3: a field is not hot; the cluster dispersion needs matter | FIRES | **FIRES** |
| K5 | locality is forced: smoothing the field destroys the equilibrium | FIRES | **FIRES** (Arm N: rms \|div sigma/(rho_c g) - 1\| 0.98–1.00 at L = 10–200 kpc, 4.14 at L = 0) |
| **K6** | **no ghost, no superluminal** | **HOLDS** | **HOLDS** — 0/24 rows with c_T^2 < 0, 0/24 with c_L^2 < 0, 0/24 with a sound speed above c; largest c_T 69.3 km/s, c_L 83.8 km/s against c = 2.998e5 km/s |
| K7 | the multi-stream escape does not rescue interpenetration | FIRES | **FIRES** (Arm M5': each constituent's map is 2-to-1, so det F must vanish; c_L^2 crosses zero at y = 6/5 and 3lam+2mu diverges at y = 9/7) |

Known answers KA1–KA10 all pass before any row is graded (KA9: mean div(sigma)/(rho_c g) = +1.000000
over the 24 rows; KA10: the Maxwell signature `-Pi -> diag(+J, -J, -J)`, with
`Pi_rr/(-Pi_tt) -> -0.99989` and the leading correction O(u)).

## 2. Q1 — the grade the brief asked for

- **Q1a HOLDS, Q1b HOLDS.** All 24 rows (2 footings x 4 masses x 3 profiles) have c_T^2 > 0,
  c_L^2 > 0 and both below c everywhere on [0.2, 60] r_M; mu_s > 0 and 3lam+2mu > 0 on 24/24.
- **Q1c HOLDS.** The unstable shell (c_L^2 < 0 for 6/5 < y < 9/7) lies outside every physical halo:
  min r(y = 9/7)/r_200 = 9.72.
- **Q1d/e.** Deep-field closed forms confirmed: c_T^2 -> (3/4) v_inf^2/y, c_L^2/c_T^2 -> 1.4636
  (against the predicted 10/7 = 1.4286), and c_T^2/sigma_t^2 = 3/(2y) = 0.304 — the elastic sound
  speed is *below* the dispersion the halo must carry, which is the melt condition used in Q4.

## 3. Q2 — which hypothesis must break (the verdict)

| arm | hypothesis dropped | properties | result |
|---|---|---|---|
| Arm N | (i) LOCAL | breaks the equilibrium; and locality never touches (2) | FIRES |
| Arm P1 | (ii) by a contact coupling | fails (1) (Gamma/H = 0.84 at z 1100, 4.58 at z 3400 — the cold component is dragged when it must stay decoupled) and (2) (dragged with the gas, where RB1 puts the mass with the galaxies) | FIRES |
| **Arm P2** | **(ii), no material identity: the carrier is the sourced field** | **(2) PASSES (fields superpose), (4) PASSES; (1) FAILS, (3) FAILS** | **the unique break compatible with (2)** |
| Arm S | (iii) NORMALLY SELF-GRAVITATING | not at full share in clusters (RB1 gate 1); lensing deficit the whole cold share; still a continuum, so (2) fails | FIRES |
| Arm M5' | the multi-stream escape | each constituent's map is 2-to-1 | FIRES |

**Q2's rule is satisfied by exactly one arm**, so this is not the NO VERDICT branch of §2: the answer
is (ii). The price is explicit and quantified:

| footing | log M_b | M_c/M_b at 272 kpc | at 637 kpc | budget | excess |
|---|---|---|---|---|---|
| canonical | 10.45 | 41.49 | 97.83 | 5.41 | 7.7x / 18.1x |
| canonical | 10.90 | 24.51 | 58.07 | 5.41 | 4.5x / 10.7x |
| alt | 10.45 | 45.66 | 107.60 | 5.41 | 8.4x / 19.9x |
| alt | 10.90 | 27.00 | 63.89 | 5.41 | 5.0x / 11.8x |

`M_c(<r) ~ r` without bound: the settled halo is **phantom**, not substance. That is the same amount
gap AMT1 measured at the KiDS radii, now derived from the stress rather than from the budget.

## 4. Q4 — what sigma_r^2 < 0 means

Kinetic reading: `P_r = int f v_r^2 d^3v >= 0` for every f >= 0, so the law's `P_r = -J < 0` demands a
**negative measure** — no kinetic medium (cold, warm, hot, collisional, collisionless, anisotropic)
can carry it. The required deficit is exactly -1/2 of the halo's own v_inf^2: at log M_b 10.45
canonical, v_inf = 136.8 km/s and sigma_r^2 = -9.3525e3 (km/s)^2 = -(96.7 km/s)^2 = -(v_inf/sqrt2)^2.

Maxwell reading: in the deep field `sigma = -Pi -> diag(+J, -J, -J) = T[phi]`, `grad phi = g` — tension
along the field equal to the energy density (w_par = -1) and equal transverse pressure. That is the
canonical (Maxwell) stress of a classical field. So the carrier of the law's static halo is the field,
and form B's "cold dark energy" is that field's polarization charge; rho_c is not a conserved rest-mass
density.

## 5. MUTATE — all five arms bite

| arm | planted defect | detected |
|---|---|---|
| M1 | sigma = +Pi | equilibrium fails (div(sigma)/(rho_c g) = -1.000000) and c_T^2 < 0 on 24/24 — BITES |
| M2 | isotropic pressure P = J | mu_s == 0 identically (S4 disease returns) and the anisotropy Pi_rr - Pi_tt = -eps is left uncarried (relative size 2.00 in the deep field) — BITES |
| M3 | Newtonian limit (a0 x 1e-6, x 1e-9) | the halo, the moduli and both sound speeds vanish with a0 (M_c ratio 1.01e-3) — BITES |
| M4 | mass conservation dropped | every member is unphysical (rigid at C = 0; the map folds and rho < 0 at C != 0) and none reproduces the law (2.93–3.30 dex) — BITES (recorded as two True booleans, not a printed "BITES" line) |
| M5 | multi-stream escape | the escape closes on itself: c_L^2 = 0 at y = 6/5, 3lam+2mu diverges at y = 9/7 — BITES |

## 6. Disclosures

- **The blind spot is flagged, as the criteria require (Q3c).** DB1's two tests
  (Sigma_c >= 3x the swept ICM column; G Sigma_c^2 >= rho_ICM v^2) are **self-gravity** tests. The
  solid passes both (Sigma_c 9.1252e09 against 4.7746e09 and 5.5366e09) and still cannot
  interpenetrate. A solid passes them and remains excluded.
- **The surviving carrier is not a medium.** P2 is the answer to "which hypothesis must break", not a
  candidate medium: it fails (1) and (3) by construction. The label is therefore NO MEDIUM, and the
  "5.41 x baryons, conserved and cold" component of form B has nothing to be carried by.
- **Inherited and provisional:** R50 = 0.10 kpc (M/Msun)^0.14 (1 + M/3.98e10)^0.25 is SCS2's
  transcription, as-read and not re-sourced; the Bullet's ICM central density and column are
  PROVISIONAL (Plummer b = 200 kpc); DB1's and RB1's numbers are transcribed, not recomputed.
- **Post hoc kernel note (not in the criteria):** nothing in this lane depends on which kernel is used;
  the stress `Pi` is the law's own, and KA9 fixes the sign that ELA1's amendment A1 corrected.

## 7. Files

`FROZEN_CRITERIA.md` (committed alone), `fin7.py` -> `fin7.out` / `fin7.json`,
`fin7_MUTATE_M{1..5}.out/.json`, and this file.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
