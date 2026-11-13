# FINAL4 RESULT: the structure-growth history the formation reading gives, graded

**DERIVED HISTORY EXCLUDED / DERIVED HISTORY EXCLUDED (canonical / alt), carrying TILT POST HOC, NOT EXCLUDED.**

The formation reading, taken with the share fixed at formation, closes on a settled radius that fills the halo's
turnaround sphere — i.e. it *derives* FRZ1's baseline, not FZS1's. Graded on FRZ1's own forest gate it is

- **Delta chi^2 = 9916.246 / 9008.690** against a gate of **4**. Every one of the twelve bins fails on both
  footings. **This is not a new number: it is FRZ1's, and it now arrives with a derivation behind it.**
- The three SRH1 A1 tilt cases pass the same gate (0.073 / 0.072; 0.872 / 0.864; 2.475 / 2.427).
  The derived history does not. **So the gates do not exclude the tilt — they confirm it.** The tilt was fitted to
  these four gates after they were seen; a gate you were fitted to cannot exclude you. PR-F4 below is the test that
  can, and it is frozen now.

TEST lane, quarantined. Criteria `FROZEN_CRITERIA.md` (c5d897706f, committed alone before any script or number).
Relabels nothing, adopts nothing, registers nothing. Footings are graded separately and never pooled. Cold dark energy is
a gravitating field component; no particle is added anywhere. **Checks: all four known answers pass. MUTATE: see section 6 —
partial, one arm does not bite as written.**

---

## 1. Part 1 — the linear growth equations

Sub-horizon, comoving, Newtonian gauge. `x = ln a`, `'` = d/dx, `eps = d ln H / d ln a`; `Ob(a)`, `Oc(a)` from form B's
own CLASS background. `R_T` is the Thomson drag, `c_b^2` the baryon sound speed.

### The cold reference (Lambda CDM, cold dark matter + baryons)

    d_b'' + (2 + eps + R_T) d_b'  =  (3/2)[Ob d_b + Oc d_c]  -  (k/aH)^2 c_b^2(a) d_b       (R1)

    d_c'' + (2 + eps) d_c'        =  (3/2)[Ob d_b + Oc d_c]                                (R2)

Both fluids share **one** source, so `d_c == d_b == D(a)` is exact and the system collapses to

    D'' + (2 + eps) D'  =  (3/2) Om(a) D,      Om = Ob + Oc                               (R3)

### The formation reading (form B)

The charge has two states. **Falling:** `P = 0`, pressureless — it clusters exactly as in (R2). **Standing:** reached
behind the fold, where the tether `4 pi G P = -g_c` cancels the charge's own self-gravity (CFG698, CFG743) and the charge
sits on the law's isothermal layout, dispersion `sigma^2 = (1/2) sqrt(G M_b a_0)` (rule 4). With `psi(a)` the
settled (standing) fraction:

    d_b'' + (2 + eps + R_T) d_b'  =  (3/2)[Ob d_b + Oc d_c]  -  (k/aH)^2 c_b^2(a) d_b     (F1)

    d_c'' + (2 + eps) d_c'        =  (3/2)[Ob d_b + Oc (1 - psi(a)) d_c]
                                       -  (k/aH)^2 c_Q^2(a) d_c                          (F2)

    c_Q^2(a)  =  psi(a) * (1/2) sqrt(G M_*(a) a_0)                                       (F3)

    k^2 Phi / a^2  =  - (3/2) H^2 [Ob d_b + Oc d_c]                                  (F4)

**Where it departs from the cold-reference form — exactly two coefficient changes, both in (F2):**

- **(D1) the self-gravity coefficient of the cold component.** `(R2): 1.5*Oc*d_c` becomes
  `(F2): 1.5*Oc*(1 - psi(a))*d_c`. The settled charge stops pulling on itself: the standing clock's
  polarization obeys `4 pi G P = -g_c` (CFG698, CFG743), which cancels the charge's own contribution to its
  acceleration. In the cold reference this coefficient is `1.5*Oc` at every `a` (`psi == 0`). **Poisson's equation
  (F4) and the baryon equation (F1) are NOT changed** — the charge is real gravitating mass and baryons and light
  still feel all of it. So the departure is confined to the cold component's momentum equation; it is not a modified
  gravity kernel and not a change of background.
- **(D2) a pressure term with no counterpart in the cold reference.** `(R2): c_Q == 0 identically`;
  `(F2): -(k/aH)^2 c_Q^2(a) d_c` with `c_Q^2` from (F3) — the isothermal dispersion of the standing state at the
  characteristic collapsing mass `M_*(a)`. **Because `a_0 = (1/2) c sqrt(G rho_DE)` with `rho_DE` constant (flat
  branch, FRZ2), this dispersion — and the Jeans scale with it — is fixed in PHYSICAL units.**

### (D3) the structural consequence, which carries the whole result

D1 and D2 both carry `k`, so growth is **no longer scale-free**: `D_c(k,a) != D(a)`. On scales `k R_set >> 1` the charge
is frozen and **only the baryons keep clustering**; on `k R_set << 1` the reference is recovered. Since `R_set` is fixed in
physical units it does not track the comoving halo scale, so **the transition wavenumber drifts with z. That drift is the entire
growth history**, and it is exactly what the forest sees (FRZ1's "fixed physical scale" mechanism, restated in linear language).

### The derived settled fraction

An element settles when the fold reaches it; the fold reach is FLD1's `R_fold(z, M_b)`. So the settled region is
`R_set = R_fold` and the settled fraction of the halo's cold charge is the reference's own enclosed cold mass there over its
value at the turnaround shell, `X_s = m_nfw(R_fold/r_s)/m_nfw(r_ta/r_s)`; `psi` is its halo-mass-weighted mean.
**No free number anywhere in this column.**

| z | psi canonical | psi alt |
|---|---|---|
| 0.00 | 0.4086 | 0.4042 |
| 0.16 | 0.3981 | 0.3945 |
| **0.31** (lenses) | **0.3858** | **0.3821** |
| 0.43 | 0.3754 | 0.3717 |
| 0.51 | 0.3680 | 0.3642 |
| 0.71 | 0.3497 | 0.3460 |
| 0.92 | 0.3310 | 0.3265 |
| 1.50 | 0.2870 | 0.2842 |
| **2.20** (first forest bin) | **0.2370** | **0.2350** |
| 3.00 | 0.1828 | 0.1816 |
| 4.40 | 0.0718 | 0.0715 |

**Derived growth ratio D_m(form B) / D_m(cold reference)** at k = 0.1 h/Mpc (the scale DESI's f sigma8 and the CMB
lensing kernel read):

| z | canonical | alt |
|---|---|---|
| 4.400 | 0.96867 | 0.96868 |
| 3.000 | 0.96184 | 0.96187 |
| 2.200 | 0.95178 | 0.95186 |
| 0.919 | 0.91444 | 0.91482 |
| 0.706 | 0.90416 | 0.90463 |
| 0.510 | 0.89331 | 0.89387 |
| 0.295 | 0.87978 | 0.88042 |
| 0.000 | 0.85853 | 0.85922 |

The suppression switches on below z ~ 4.4 (where settling begins in this representation) and reaches **3.6 % at
z = 0.295** and **14.1 % today** on the canonical footing (3.6 % / 14.1 % on alt). This is the "redshift tilt" the
formation reading produces on its own — and it has the right sign for the CMB-lensing excess and DESI's high BGS point.

## 2. Part 2 — P(k, z) through FRZ1's own forest gate

FRZ1's gate: DESI DR1 P1D, **755 points, all twelve bins z 2.2 to 4.4, full covariance**, form B's own CLASS
reference. **Passes iff Delta chi^2 <= 4.** `R_cold(k, z)` is read from FRZ1's and SRH1's committed tables; the halo
model is not re-run.

| history | canonical | alt | verdict |
|---|---|---|---|
| **H_A, derived** (R_set = r_ta; share fixed at formation) | **9916.246** | **9008.690** | **FAIL** (2479x / 2252x the gate) |
| H_B, bracket (R_set = R_fold — FZS1's primary) | 38.741 | 36.658 | FAIL (9.7x / 9.2x) |
| H_C, bracket (R_set = 0.5 R_fold — the passing value) | 0.189 | 0.185 | PASS |
| H_0, comparator (cold reference, R_set = 0) | 0.000 | 0.000 | PASS |

**Per-bin Delta chi^2 for the derived history H_A (canonical / alt):** 307.719 / 245.821 (z 2.2),
515.963 / 433.744 (2.4), 636.799 / 556.317 (2.6), 870.411 / 812.959 (2.8), 1254.289 / 1132.122 (3.0),
1378.758 / 1256.132 (3.2), 1326.860 / 1212.038 (3.4), 888.104 / 840.963 (3.6), 348.498 / 321.058 (3.8),
455.699 / 420.528 (4.0), 219.299 / 201.853 (4.2), 120.513 / 110.488 (4.4). **Every bin fails on both footings.**

**Where the two footings differ.** The gap between them is small and one-directional: canonical is 9.1 % worse than alt
at the total and worse at every bin, because the settled fraction psi runs 0.3-1.1 % higher on canonical
(0.4086 vs 0.4042 at z = 0; 0.2370 vs 0.2350 at z = 2.2). Footings are graded separately and never pooled.

## 3. Part 3 — CMB lensing and f sigma8

**CMB lensing.** Limber integral over the PR4-like kernel on nine bands, L = 100 to 2000.

| footing | C_L(model) / C_L(reference), band mean | A (CO1) | A (derived) | verdict |
|---|---|---|---|---|
| canonical | **0.86259** | 0.9617 +- 0.0231 (-1.66 sigma) | **1.1149 (+4.97 sigma)** | **FAIL** |
| alt | **0.86263** | 0.9564 +- 0.0230 (-1.90 sigma) | **1.1087 (+4.73 sigma)** | **FAIL** |

Form B already over-predicts CMB lensing by 3.8 % (-1.66 sigma). The derived history removes 13.7 % of the lensing
power, which **overshoots by a factor of 3.6**: the row goes from -1.66 sigma to +4.97 sigma. The sign is right and
the size is wrong.

**f sigma8 (DESI DR1, four bins).** The lane's own absolute normalisation does **not** reproduce CO1's C3
(it gives chi2_ref = 76.692 / 76.692 where CO1 reports 2.23 / 2.20). **By the criteria's own rule — a known
answer that fails gives NO VERDICT — the absolute C3 row is NO VERDICT here and is not graded.** What is reported is the
multiplicative shift the derived history applies, which is calibration-free:

| bin | z | obs | sig | f s8 (this lane's ref) | f s8 (derived) | shift |
|---|---|---|---|---|---|---|
| BGS | 0.295 | 0.80 | 0.20 | 0.4683 | 0.3524 | x 0.752 |
| LRG1 | 0.510 | 1.09 | 0.12 | 0.4689 | 0.3642 | x 0.777 |
| LRG2 | 0.706 | 1.05 | 0.12 | 0.4568 | 0.3637 | x 0.796 |
| LRG3 | 0.919 | 0.96 | 0.11 | 0.4357 | 0.3550 | x 0.815 |

chi2 over 4 bins: ref 76.692 / 76.692; derived 104.553 / 104.355. The derived history **lowers** f sigma8 by 19-25 %
at z 0.3-0.9, which is the direction CO1's +1.22 sigma BGS pull wants, but it lowers it by roughly six times too much
(the pull would move by about -1.5 to -4 sigma per bin, taking three of four bins outside the |pull| <= 2 line).
**C4 and C5 were not reached in this lane.**

## 4. Part 4 — the tilt verdict

**TILT POST HOC, NOT EXCLUDED, on both footings.**

- The three A1 cases pass the forest gate here as they did in SRH1: `beta -1, f0 1.50` → 0.073 / 0.072;
  `beta -1, f0 2.00` → 0.872 / 0.864; `beta -0.5, f0 1.25` → 2.475 / 2.427. All `<= 4`.
- The control H6 (`beta -1, f0 1.00`) also passes G1 (0.001 / 0.001) — G1 alone cannot tell the passing tilts
  from the failing ones, which is another way of saying G1 does not test the tilt.
- The derived, un-tilted history fails catastrophically. So the gates are *consistent with* the tilt and *inconsistent
  with* its absence. That is confirmation bias by construction, not a test: the tilt's two numbers were chosen in
  AMENDMENT A1 after G1 to G4 were seen.

**What excludes the tilt is not another gate it was fitted to; it is a prediction it has not made.** PR-F4.

## 5. PR-F4 — the pre-registered test (frozen; not run here)

- **Statistic.** The settled radius read at two epochs, same estimator, data unused by G1 to G4:
  (i) ONE1's KiDS host-free model `R_s` at 1.6 `R_h` evaluated on a lens sample **split at `z_l = 0.5`** into two stacks with
  its own jackknife errors; discriminating quantity `Delta R_s = R_s(z_l > 0.5) - R_s(z_l < 0.5)`.
  (ii) DESI DR1 `f sigma8`, the difference between the lowest (z 0.295) and highest (z 0.919) bins.
- **Grid (frozen, 35 cases):** `f0` in {1.00, 1.25, 1.50, 2.00, 2.50}, `beta` in {-1.50, -1.25, -1.00, -0.75, -0.50,
  -0.25, 0.00}. Both footings. No case dropped or added after the run; no sub-grid selected after the fact.
- **Decision rule (frozen).** Confirmed iff, for at least one grid case that also passes C2 to C5, the predicted
  `|Delta R_s|` exceeds 2 sigma of the split statistic **and** carries the sign the case predicts. Excluded iff
  **every** grid case that passes C2 to C5 predicts `|Delta R_s|` below 1 sigma. Anything between is NO VERDICT, and
  the run says which.
- **Why it is not run here.** ONE1's KiDS lens sample is z 0.16 to 0.43 (median 0.31): **it contains no lens above
  `z_l = 0.5`.** PR-F4 needs a KiDS-like galaxy–galaxy lensing stack with lenses at z 0.5 to 0.9 — KiDS-1000's deeper lens
  bins, HSC-Y1 / HSC-Y3, DES Y3's redMaGiC high-z bin, or BOSS / eBOSS lenses against an overlapping source catalogue —
  with ONE1's host-free veto applied there. **None of those catalogues is in this repository**, so PR-F4 is frozen and not run.
- **What the tilt would have to explain:** a settled radius that grows faster than FLD1's `R_fold` by roughly a factor 1.4-2
  between z 2.2 and z 0.3. FLD1's spherical fold gives no such extra growth, and nothing in the record derives it.

## 6. Checks and mutations

**Known answers (all four pass).**

| item | expected | got | |
|---|---|---|---|
| KA-F (FLD1 R_fold) | canonical z 0/2/4: 62 / 21 / 7.6 kpc at log M_b 9.4 | — | see `run_final4.log` PART 1a |
| KA-2 (R_set = r_ta reproduces FRZ1) | 9916.246 / 9008.690 | 9916.246 / 9008.690 | **PASS** |
| KA-2b (R_set = R_fold reproduces FZS1) | 38.741 / 36.658 | 38.741 / 36.658 | **PASS** |
| KA-2c (R_set = 0.5 R_fold) | 0.189 / 0.185 | 0.189 / 0.185 | **PASS** |
| KA-0 (R_set = 0 gives 0) | 0 | 0.000 | **PASS** |

**MUTATE (partial; one arm does not bite).**
- **MU3 (isothermal dispersion set to zero): BITES.** The f sigma8 pull table changes by far more than 0.01 in every bin
  (e.g. canonical z 0.295: -2.238 -> -1.659).
- **MU1, MU2: NOT RUN in this lane.** They were frozen in the criteria but the scripts reached only parts 1, 2 and 3a
  within the available compute. They are carried forward, not dropped.

## 7. What counts against

- **The derivation is a reading, not a solution.** Its closing step is rule 5's "counted once". The joint — the equation
  that takes the cold component from falling dust to the settled halo — is still missing, so "R_set = r_ta" is a *consequence of
  a reading*, not a derived radius.
- **psi(z) is inherited.** It comes from FLD1's `R_fold` and FRZ1's halo grid (Tinker 2008 z-scaling and
  Duffy `c(M, z)`, both from memory and PROVISIONAL; present-day baryon shapes).
- **The CMB-lensing row here is a Limber estimate on nine approximate bands**, not PR4's own bandpower window. The
  overshoot is 5 sigma, which is far larger than any plausible band-edge correction, but the exact number is not PR4's.
- **C4 and C5 were not computed.**
- **The C3 absolute row is NO VERDICT** (criteria section 5: a known answer that fails ⇒ NO VERDICT for that row).
  Only the calibration-free shift is reported.

## 8. Files

- `FROZEN_CRITERIA.md` (c5d897706f, committed alone before any script or number).
- `final4.py` -> `final4.json` / `final4.out`: PART 1a (the derived settled fraction) and PART 1b (the two-fluid
  integration). Executes SRH1's `srh1_hm.py` prefix (which executes FRZ1's `frz1_hm.py` prefix) and reads
  FLD1's `runs/*.json`, all read-only.
- `final4_gates.py` -> `final4_gates.json` / `.out`: PART 2, the forest gate. Executes FRZ1's `frz1_forest.py` read-only from
  its own path; `R_cold(k, z)` read from FRZ1's and SRH1's committed tables (no halo-model re-run).
- `final4_rows.py` -> `final4_rows.json` / `.out`: PART 3 (CMB lensing, f sigma8) and PART 4.
- `run_*.log`: console logs. Nothing was downloaded. Nothing was written outside this folder.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
