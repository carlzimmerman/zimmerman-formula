# FINAL4 FROZEN CRITERIA: the structure-growth history the formation reading gives, graded

FINAL MILE, lane FINAL-4 (GROWTH). TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
Footings never pooled (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2). Cold dark energy is a gravitating field
component; no particle is added anywhere. kappa = 1/2 FITTED; not theory closed.

**Lane id.** The brief names this lane FINAL-4 (GROWTH). The short id used on the files is **FINAL4**. Checked free:
no `closure_2026_11_11/FINAL4*` exists, and no commit subject on any branch names FINAL4 or growth_history.

Committed alone, before any FINAL4 script exists and before any FINAL4 number is computed.

## 0. The question

FRZ1 computed form B's halo redistribution at the forest's own redshifts and the forest row failed (9916 / 9009 against
a gate of 4). FZS1 then asked whether confining the law's layout to a *settled radius* R_set = f R_fold rescues it; it
does not (38.7 / 36.7 at f = 1; it passes only near f = 0.5). SRH1 then asked whether one constant f passes the
forest, high-z rotation curves, present-day rotation curves and galaxy lensing together; the window is empty
(gap 1.39 / 1.45), and a window opens **only** with a *post hoc* redshift tilt f = f0 (1 + z)^beta.

All three of those lanes *parametrised* the settling and fitted it. This lane does not. It **takes the formation reading
seriously as a derivation**:

> the quantity set at formation is the ratio of the non-baryonic mass to the baryonic mass of a mass element, fixed by
> the law at the formation field, and conserved thereafter (FRM1 / HIS1; rule 5, counted once).

"Take the share as fixed at formation for each mass element" gives a *closed* growth history with **no free parameter**.
This lane writes it, computes what it does to P(k, z), and grades it on the record's own gates.

## 1. Part 1 — the linear growth equations

Sub-horizon, comoving, Newtonian gauge; x = ln a, prime = d/dx; epsilon(a) = d ln H / d ln a; Omega_b(a), Omega_c(a)
from form B's own CLASS background.

**Cold reference (Lambda CDM, cold dark matter + baryons).** Both components are free, pressureless after recombination
and share one source, so delta_c = delta_b = D(a) exactly:

    d_b'' + (2 + eps + R_T) d_b'  =  (3/2)[Omega_b d_b + Omega_c d_c]  -  (k/aH)^2 c_b^2(a) d_b      (R1)

    d_c'' + (2 + eps) d_c'        =  (3/2)[Omega_b d_b + Omega_c d_c]                              (R2)

    D''   + (2 + eps) D'          =  (3/2) Omega_m(a) D,      Omega_m = Omega_b + Omega_c          (R3)

**The formation reading (form B).** The charge has two states. Falling: P = 0, pressureless — it clusters exactly as in
(R2). Standing: reached after the fold, where the tether 4 pi G P = -g_c cancels the charge's own self-gravity (CFG698,
CFG743) and the charge sits on the law's isothermal layout, dispersion sigma^2 = (1/2) sqrt(G M_b a_0) (rule 4). Let
psi(a) be the settled (standing) fraction of the charge.

    d_b'' + (2 + eps + R_T) d_b'  =  (3/2)[Omega_b d_b + Omega_c d_c]  -  (k/aH)^2 c_b^2(a) d_b      (F1)

    d_c'' + (2 + eps) d_c'        =  (3/2)[Omega_b d_b + Omega_c (1 - psi(a)) d_c] - (k/aH)^2 c_Q^2(a) d_c   (F2)

    c_Q^2(a) = psi(a) * (1/2) sqrt(G M_b(a) a_0)                                                  (F3)

    k^2 Phi / a^2  =  - (3/2) H^2 [Omega_b d_b + Omega_c d_c]                                   (F4)

**Where they depart from the cold-reference form — precisely three places, all of them in (F2):**

- **(D1) the self-gravity coefficient of the cold component.** `1.5 * Omega_c * d_c` becomes
  `1.5 * Omega_c * (1 - psi(a)) * d_c`. The settled charge stops pulling on itself. In the cold reference this
  coefficient is 1.5*Omega_c for every a (psi == 0). **Poisson's equation (F4) and the baryon equation (F1) keep the
  full Omega_c d_c** — the charge is real gravitating mass and baryons and light still feel all of it. The departure is a
  change in the cold component's momentum equation only; it is not a modified gravity kernel and not a change of background.
- **(D2) a pressure term with no counterpart in the cold reference.** `- (k/aH)^2 c_Q^2(a) d_c`, with c_Q^2 from (F3) — the
  isothermal dispersion of the standing state. **In the cold reference the cold component has c_Q == 0 identically.**
- **(D3) the structural consequence.** D1 and D2 carry k, so the growth is **no longer scale-free**: D_c(k, a) != D_ref(a).
  On scales k R_set >> 1 the charge is frozen and **only the baryons keep clustering**; on k R_set << 1 the reference is
  recovered. Because a_0 = (1/2) c sqrt(G rho_DE) with rho_DE constant (flat branch, FRZ2), R_set is **fixed in physical
  units**, so the transition wavenumber does not track the comoving halo scale — **it drifts with z. That drift is the entire
  growth history, and it is what the forest sees.**

**The share, fixed at formation (the closing condition).** M_C = X M_b with X = X_L(g_{b,f}) = (sqrt(1 + 4 a_0/g_{b,f}) - 1)/2
(PD1: X = 59.4861 canonical / 59.5029 alt). The law's phantom grows as M_ph(r) = sqrt(G M_b a_0) r/G - M_b, so the whole
share is used up where M_ph = X M_b, i.e. at

    **R_set = (1 + X) sqrt(G M_b / a_0) = r_ta .**

**This is the derivation's result and it is a number, not a parameter.** The settled region is the region the halo's charge
has filled, and the charge fills it out to the turnaround shell by construction. So the formation reading gives
**f_der = r_ta / R_fold**, which is `inf` in `ratios_S`'s units — i.e. FRZ1's baseline is not an assumption here, it is
what the fixed share implies. FZS1's f = 1 (settled region = fold reach) is then the weaker variant in which only
what the fold has *reached* is settled; it is graded beside, as a bracket.

## 2. Part 2 — P(k, z) through FRZ1's own forest gate

Graded on both footings, separately:

- **H_A (derived):** R_set = r_ta (`fac = inf`) — what the fixed share gives.
- **H_B (bracket, FZS1's primary):** R_set = R_fold (`fac = 1`).
- **H_C (bracket, the value that passes):** R_set = 0.5 R_fold (`fac = 0.5`).
- **H_0 (comparator):** R_set = 0, the cold reference.
- **Tilt H5:** f = 1.5 (1+z)^-1, 2.0 (1+z)^-1, 1.25 (1+z)^-0.5 — SRH1's A1 cases, re-graded here on this lane's own path.
- **H6 (control):** f = 1.0 (1+z)^-1 — SRH1's frozen tilt case that fails.

**Gate (FRZ1's, unchanged):** DESI DR1 P1D, 755 points, all twelve bins z 2.2 to 4.4, full covariance, form B's own CLASS
reference. **Passes iff Delta chi^2 <= 4.** Per-bin values reported.

## 3. Part 3 — CMB lensing and f sigma8

- **CMB lensing:** GAL1's PR4 best-amplitude rule (QX3 iter2's `amp_fit`) applied to the history's own linear content.
  Graded against the record's line, |A - 1| <= 2 sigma_A and chi^2_shape <= 18.48, and reported beside CO1's
  **0.9617 +- 0.0231 (canonical) / 0.9564 +- 0.0230 (alt)**.
- **f sigma8:** DESI DR1, four bins z 0.295 / 0.510 / 0.706 / 0.919, **passes iff every |pull| <= 2**, chi^2 over
  4 bins reported, beside CO1's **2.23 / 2.20 (canonical) and 2.29 / 2.23 (alt)**.

## 4. Part 4 — the tilt verdict, and the test that is frozen now

The tilt f = f0 (1 + z)^beta is a two-parameter family fitted to four gates after they were seen. The verdict printed is:

- **TILT POST HOC, NOT EXCLUDED** iff the tilt cases pass the gates here and the derived history does not.
- **TILT EXCLUDED** iff the tilt cases fail the gates here too.
- **NO VERDICT** otherwise.

**PR-F4, frozen now whatever the verdict (it does not depend on any number this lane computes):**

- **Statistic.** The settled radius read at two epochs, from the same estimator, on data not used by G1 to G4:
  (i) ONE1's KiDS host-free model R_s at 1.6 R_h, evaluated on a lens sample **split at z_l = 0.5** into two stacks with
  its own jackknife errors; discriminating quantity Delta R_s = R_s(z_l > 0.5) - R_s(z_l < 0.5).
  (ii) DESI DR1 f sigma8, the difference between its lowest (z 0.295) and highest (z 0.919) bins.
- **Grid (frozen, 35 cases):** f0 in {1.00, 1.25, 1.50, 2.00, 2.50}, beta in {-1.50, -1.25, -1.00, -0.75, -0.50,
  -0.25, 0.00}. Both footings. No case dropped or added after the run, no sub-grid selected after the fact.
- **Decision rule (frozen).** Confirmed iff, for at least one grid case that also passes C2 to C5, the predicted
  |Delta R_s| exceeds 2 sigma of the split statistic with the sign the case predicts. Excluded iff **every** grid case
  that passes C2 to C5 predicts |Delta R_s| below 1 sigma. Anything between is NO VERDICT, and the run says which.
- **Why it is not run here.** ONE1's KiDS lens sample is z 0.16 to 0.43 (median 0.31); **it contains no lens above
  z_l = 0.5**. Running PR-F4 needs a KiDS-like galaxy-galaxy lensing stack with lenses at z 0.5 to 0.9 — KiDS-1000's own
  deeper lens bins, HSC-Y1 / HSC-Y3, DES Y3's redMaGiC high-z bin, or BOSS / eBOSS lenses against an overlapping source
  catalogue — with ONE1's host-free veto applied at that redshift. **None of those catalogues is in this repository**, so
  PR-F4 is frozen and not run.

## 5. Known answers (each must pass)

- **KA-E1.** With psi == 0 and c_Q == 0, (F1)-(F2) reproduce the cold reference: max |D_form/D_ref - 1| <= 1e-6 over
  k in [1e-3, 10] and z in [0, 7], both footings. (The departure is a change of coefficients, not of the solver.)
- **KA-E2.** D(z) against CLASS's `scale_independent_growth_factor` (GRW1's KA4 line): relative difference <= 5e-3 at
  z 2.2, 3.0, 4.4 — inherited from FRZ1's KA4.
- **KA-G1a.** The derived history H_A reproduces FRZ1's stored primary: Delta chi^2 = 9916.246 / 9008.690 to 0.01, per
  bin to 0.01.
- **KA-G1b.** H_B reproduces FZS1's primary 38.741 / 36.658 to 0.01; H_C reproduces FZS1's x0.5 arm 0.189 / 0.185 to
  0.01; H_0 gives exactly 0.
- **KA-G4.** At f = 1 the lens path reproduces SRH1's stored row (model R_s 1.003 / 0.847, z -1.15 / -0.23) within
  SRH1's KA-G4c tolerance.

## 6. MUTATE (each must bite on both footings)

- **MU1.** H_A with the tether coefficient psi set to 0 (the settled charge left self-gravitating): the derived growth
  must differ, and the forest Delta chi^2 must change by more than 1 %. (Says the result is the tether's, not the
  background's.)
- **MU2.** The share X held at its z = 0 value while a_0 is left at the footing: the CMB-lensing amplitude A must move by
  more than 0.001.
- **MU3.** The isothermal dispersion in (F3) set to zero: the largest DESI f sigma8 |pull| must change by more than 0.01.

## 7. Labels (per footing)

- **DERIVED HISTORY SURVIVES** — the derived history passes the forest gate, CMB lensing and f sigma8.
- **DERIVED HISTORY EXCLUDED** — it fails any of them; the RESULT names the row and the size of the miss.
- **NO VERDICT** — a known answer fails, a MUTATE arm does not bite, or a row cannot be evaluated.
The tilt verdict is printed beside the label, and PR-F4 is printed either way.

## 8. What counts against (stated now)

- The derivation's closing step is rule 5's "counted once"; the record does not derive the joint, so R_set = r_ta is a
  *reading*, not a solution. It has no free number, but it is not the joint either.
- Inherited: G1's halo model (Tinker 2008 z-scaling and Duffy c(M, z) from memory, PROVISIONAL; present-day baryon
  shapes; linear 1D projection); G4's neighbours keep ONE1's counted-once halos; the f sigma8 row is linear theory while
  R_cold is halo model — a hybrid, as in CO1.
- psi(a) is derived from FLD1's R_fold and the halo model, both inherited.

## 9. Hand estimates (written before any number)

- **H_A (derived, R_set = r_ta).** This is FRZ1's own primary. I expect Delta chi^2 = 9916 / 9009, i.e. **FAIL** by a
  factor of about 2500 / 2250, with every bin failing. I do not expect the fixed-share reading to soften this at all:
  it *implies* it.
- **CMB lensing under H_A.** Form B's linear content is CO1's C2 = 0.9617 (canonical), i.e. -1.66 sigma. The
  redistribution at k 0.1 to 1 and z 1 to 3 removes power, and C4 (which does carry it) reads +0.00003 — three
  orders of magnitude inside its 0.0481 line. So I expect **A to move by well under its error and the row to pass.**
- **f sigma8 under H_A.** The suppressions are at k >~ 0.3 h/Mpc and z >~ 2; f sigma8 at z 0.3 to 0.9 reads scales
  of order 0.05 to 0.2 h/Mpc. I expect the pulls to move by **well under 0.05** and the row to stay inside 2.
- **So my expectation is: DERIVED HISTORY EXCLUDED by the forest gate alone, both footings, with the two independent
  rows (CMB lensing, f sigma8) passing and unable to rescue it — and therefore TILT POST HOC, NOT EXCLUDED.**
- **Where I could be wrong.** If the settled radius at the forest's redshifts is much smaller than r_ta (which is what FZS1's
  x0.5 bracket and SRH1's tilt both amount to), H_A is the wrong reading and the forest could pass. I have frozen the
  derivation before computing, so this run decides it, not me.

## 10. Files (planned)

- `final4.py` -> `final4.json` / `final4.out` (parts 1 to 4, the known answers, MUTATE, the label). One thread.
- `RESULT.md`, with the label and the tilt verdict on both footings, and PR-F4 verbatim.
- Nothing is written outside this folder; every reused lane's folder stays read-only.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
