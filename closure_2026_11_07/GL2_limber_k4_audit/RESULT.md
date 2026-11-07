# GL2: independent audit of CK4's finding that QX3 iter2 `limber_ratio` omits the lensing potential's k^-4

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Audit lane; footings graded separately, never pooled.
- Criteria: FROZEN_CRITERIA.md (7a585d8aa9), committed alone before any script or number.
- Code: gl2.py -> gl2.json / gl2.out; MUTATE outputs gl2_MUTATE.json / gl2_MUTATE.out. The code is my own and imports
  nothing from QX3, QX7, CE2 or CK4. It reads iter2.py as text for step 3, and iter2.json only for BG2's omega_d.
- One thread, 8 s, peak RSS 0.26 GB. Nothing downloaded.

## Label: CONFIRMED on both footings (canonical a0 9.3603e-11, alt 1.1312e-10)

a0 does not enter the linear background, so both footings use the record background (omega_b 0.0215, omega_d 0.11958,
H0 65, n_s 0.95). They are graded separately and give the same numbers.

**Q(L)** is my Limber C_L^pp divided by CLASS raw_cl pp, normalised to 1 at L 100. The line is max |Q - 1| <= 0.02 over every
integer L from 20 to 400.

| Kernel | Q at L 20 / 50 / 200 / 300 / 400 | max abs(Q - 1) | Verdict |
|---|---|---|---|
| K: k^-4 present, full domain (z 1e-3 to 1000) | 1.0002 / 1.0000 / 1.0005 / 1.0000 / 1.0003 | 0.0007 | holds the 2 % line |
| K on QX3's domain (z 0.02-20, k <= 10 /Mpc), reported | 1.003 / 1.006 / 0.991 / 0.984 / 0.980 | 0.020 | CK4's restored 0.98-1.006, reproduced |
| **M1: k^-4 dropped, QX3's domain** | **0.0446 / 0.237 / 5.32 / 15.35 / 33.89** | 32.9 | leaves the line |
| CK4's frozen-kernel run (claimed) | 0.045 / 0.239 / 5.26 / 15.0 / 33.0 | | |
| M1 on the full domain, reported | 0.068 / 0.272 / 4.82 / 12.50 / 23.86 | | |

- M1 reproduces CK4's run to within -1.0 % to +2.7 % at every quoted L. The frozen tolerance was 10 %.
- With k^-4 present, the absolute Limber/CLASS ratio at L 100 is 0.9997. So the constants are right too, not just the
  shape (KA2).
- KA1: the background gives Om_b0 0.05089 and Om_d0 0.28303, matching CK4's print. **PASS.**
- **Reported, BG2** (omega_b 0.0230, H0 75, n_s 0.98, omega_d 0.11749): kernel K gives max abs(Q - 1) 0.0007. M1 gives
  0.046 / 0.236 / 5.37 / 15.56 / 34.46. The finding does not depend on the background.

## Reading of iter2.py `limber_ratio`: k^-4 ABSENT

    w = ((chis - chi) / (chi * chis)) ** 2 * (1 + np.asarray(zgrid)) ** 2 / np.array([M.Hubble(z) for z in zgrid])
    num[m] += w[j] * Pj * Rj**2 / chi[j]**2; den[m] += w[j] * Pj / chi[j]**2

- Pj is `M.pk_lin`, the matter density power, and Rj is a dimensionless growth ratio.
- The per-slice weight is therefore (chi*-chi)^2 (1+z)^2 / (chi*^2 H) x chi^-4 x P_delta.
- The lensing potential's power is P_Psi ∝ (1+z)^2 P_delta / k^4, and k^4 = L^4 / chi^4. The L^-4 part is the same for
  every slice at fixed L, so it cancels. The chi^4 part does not cancel. The correct net power of chi is 0; the code has -4.
- The k^-4 appears nowhere in the function. This is the fault CK4 reported.

## What this means (stated, not re-graded here; GL1 owns the re-read)

- `limber_ratio` returns S(L), the ratio of two Limber integrals with the same wrong weight. So the error does not show up
  as a wrong C_L. It shows up as the wrong redshifts weighting the growth ratio R(k, z).
- The chi^-4 weight is dominated by z ~ 0.02-0.1, which sits at k ~ 1-3 /Mpc for L <= 400.
- So every dchi^2 built from `limber_ratio` measures suppression where PR4 lensing has almost no weight. That covers:
  - QX3 iter1-3 G2 (mu_min);
  - QX7 iter_3 and iter_4 G2' (the Jeans window lines);
  - KD1's mu_J;
  - CE2's GL and M3 bite;
  - the CK4 GL column.
- **These dchi^2 overstate the kill.** CK4's restored reading (CE2 cells dchi^2 0.00) points the same way. GL2 confirms the
  kernel; it does not re-grade those lanes.

## Disclosed

- The criteria named z up to 1088. CLASS refuses z_max_pk above z_rec (1087.9 for BG2), so the full domain stops at
  z 1000. The kernel (chi*-chi)^2 is near zero there. Q differs from the 1088 run by less than 2e-6 on the record
  background, which was the first launch; that launch crashed only at BG2.
- Step 3 is graded by reading the code. The script's regex check and the stated chi-power count agree with the reading.

Kappa = 1/2 FITTED; not theory closed.
