# DX1 frozen criteria: the perfect disc-only exclusion as an ORACLE BOUND on GB1

Frozen before any DX1 script or number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle. The
component is cold dark energy (KD1's captured K(Q) dust). Both footings, never pooled:
- canonical: a0 9.3603e-11 m/s^2, Lstar 21.7 pc;
- alt: a0 1.1312e-10 m/s^2, Lstar 22.9 pc.

One thread, < 1 GB, minutes. No downloads.

**Why this and not a candidate.** ANALYSIS.md finds every exclusion direction (D1-D4) dead. This lane grades the
best case any such mechanism could reach: exclusion by fiat. It is an **oracle bound, not a candidate**. It reads a
class tag, which GB1 forbids for candidates, and it can never be adopted. If the bound fails, no disc-only exclusion
of a universally captured cold component passes GB1 on its own.

## 1. Fixed inputs (no parameter is fitted or scanned)

- f_on = KD1's captured fraction, read from KD1_unpinned_kq_dust/kd1.json footings[f].uniform_f_diag.capture_f:
  4.11100 canonical / 4.11214 alt. This is the cosmic share FCAP omega_d/omega_b, with omega_d fixed by QX15's
  primary CMB.
- Profile: uniform b = 1 + f_on at every graded radius. This is KD1's own diagnostic convention: an extended profile,
  more generous than KD1's 0.35 pc core, which over-shoots.
- Disc set D (f = 0): every SPARC point, every KiDS late (blue) lens bin, the Solar System.
- Hot set H (f = f_on): X-COP, groups (f* 0 and 1), the 7 X-ray ellipticals, Coma UDGs, every dSph class including LG
  field, and KiDS early (red) lens bins.
  - Ellipticals are all in H, fast rotators included. QX22 requires this: at fixed M* and sigma, fast and slow
    rotators agree to +0.002 +- 0.045 ln.

## 2. Bounds graded (both through GB1's gate functions, executed read-only)

- **O1:** b = 1 in D, b = 1 + f_on in H; F = 1, T = 0.
- **O2 (with the IMF, QX26 / GB1 L1):** b = b_imf in D, b = b_imf (1 + f_on) in H; F = 1, T = 0.
  - The component scales with the true baryon mass.
  - GB1's missing-sigma rules apply unchanged: NO VERDICT plus the frozen bracket reading.

Gates G1-G8 are GB1's, with GB1's lines (GB1 FROZEN_CRITERIA §2), per footing.

G9 (CMB lensing, growth) is CARRIED from KD1 at mu_K* (PASS, chi^2 8.56). The exclusion acts only inside collapsed
discs at late times and does not change the linear spectrum at L <= 400. It is carried, not re-run.

## 3. Labels

Per bound and footing:
- **BOUND PASSES ALL STATIC GATES:** PASS on G1-G8 on both footings. Exit 3 is then not excluded by GB1, and a
  mechanism would still be needed (none exists: ANALYSIS.md).
- **BOUND FAILS (rows):** any FAIL. Even a perfect disc-only exclusion fails those rows, so exit 3 alone cannot pass
  GB1.
- **BOUND NOT GRADABLE (rows):** no FAIL, at least one NO VERDICT.

Reported only (no label):
- per-class f needed (KD1's diagnostic, re-read);
- O1 with LG field moved to D (it is dIrr-rich), as a classification sensitivity.

## 4. Known answers (KA FAIL means stop; nothing graded)

- **KA1:** GB1's L0 class means reproduce QX20's to 1e-6 per footing. UDG mean equals S1 to 1e-9 (GB1 KA1/KA2,
  recomputed on DX1's battery copy).
- **KA2:** O1 with f_on = 0 equals gb1.json's L0 rows on G1-G8: same status, numbers |d| <= 1e-12, both footings.
- **KA3:** O2 with f_on = 0 equals gb1.json's L1 rows on G1-G8: same status, graded numbers and bracket readings,
  |d| <= 1e-12.
- **KA4:** KD1's SPARC_f_max is re-derived by the same 60-step bisection to |d| <= 1e-9: 0.325672 canonical /
  0.193712 alt.

## 5. MUTATE twin (outputs dx1_MUTATE.*)

Inverted oracle: b = 1 + f_on in D, b = 1 in H. It must FAIL G1 on both footings. If it does not, the bound has no
power, and the run says so.

## 6. Outputs

- dx1.py writes dx1.json / dx1.out; dx1.py --mutate writes dx1_MUTATE.*.
- RESULT.md gives the label per direction (from ANALYSIS.md) and the bound x gate x footing table.
- Any post-freeze change is disclosed.

Kappa = 1/2 FITTED; not theory closed.
