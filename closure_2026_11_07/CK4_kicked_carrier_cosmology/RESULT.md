# CK4: cosmology under the kicked collisionless carrier. NO VERDICT (GL has no power); at 550 km/s every gate with power passes, 575/600 fail the forest

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane (RESOLUTION_2026_11_07 lane CK4). Criteria:
FROZEN_CRITERIA.md (16d0b4c6a5), pushed alone before any script. Scripts: ck4.py (GL, GF, GFo; 29 s, 434 MB), ck4_geb.py
(GEB, built by a subagent; 40 s, 268 MB). Outputs: ck4.json / ck4.out, ck4_MUTATE.*, ck4_geb.*, ck4_geb_MUTATE.*,
run_main.txt, run_mutate.txt. QX7 iter_4 / QX3 are exec'd read-only. Cold dark energy (the carrier's cold phase), never
dark matter; no particle. Every gate is footing-independent (a0 does not enter).

**Label (frozen rule): NO VERDICT.** MUTATE M1 (daughters at 3000 km/s) does not fail GL, so GL is NO VERDICT for this
physics, and no v_k can pass all four gates. Among the gates with power, the readings are:
- **v_k 550: PASS** on GF, GFo and GEB.
- **575 and 600: FAIL** on GFo (the forest at z = 2), by 0.6 and 1.5 points of the 10 % band.

A reported post-freeze finding: the record's CMB-lensing Limber kernel omits the k^-4 factor of the lensing potential.
With it restored, GL has no power on any late small-scale suppression. That includes iter_4's window, which drops to
Delta chi^2 0.00 at all four CE2 cells. See section 3.

## 1. Primary (reading B: daughters escape halos with v_esc = 2.69 v_vir < v_k; M_min 1e11 Msun)

| v_k | GL frozen chi^2 (dchi^2) | GLc, k^-4 restored | GF Rf, BGS / LRG1-3 | GFo P1D ratio min (z 2 / 3 / 4) | GEB | F_esc z 0 / 1 / 3 / 7 | sigma8(0) ratio |
|---|---|---|---|---|---|---|---|
| 550 | 14.62 (+6.05) FAIL | 8.58 (+0.01) | PASS 0.996-0.997 | **PASS** 0.903 / 0.954 / 0.982 | PASS | 0.091 / 0.087 / 0.038 / 8.6e-4 | 0.998 |
| 575 | 15.99 (+7.42) FAIL | 8.58 (+0.01) | PASS 0.995-0.996 | **FAIL** 0.894 / 0.949 / 0.980 | PASS | 0.098 / 0.094 / 0.041 / 9.4e-4 | 0.997 |
| 600 | 17.36 (+8.79) FAIL | 8.58 (+0.01) | PASS 0.994-0.995 | **FAIL** 0.885 / 0.944 / 0.978 | PASS | 0.106 / 0.101 / 0.044 / 9.9e-4 | 0.997 |

- **GL** is NO VERDICT under the frozen rule, because M1 does not bite: at 3000 km/s the frozen kernel gives chi^2 11.56
  (+2.98) and the corrected one gives 9.19 (+0.62).
  - The frozen kernel's FAIL at 550-600 comes from z < 0.1, where it puts almost all its weight (section 3).
- **GF** passes. The suppression stays in the S8 direction (Rf <= 1) and well inside both DESI DR1 panels. GF has power:
  M1 fails it at Rf 0.62-0.71.
- **GFo** sits in the right place. Daughters escape about 9-11 % of the dark component by z 0 and about 4 % by z 3. The
  linear 1D power at z = 2 drops at the top of k_par 0.2-2 h/Mpc, to 0.903 / 0.894 / 0.885. The frozen line is 0.90.
  - This is a linear proxy for the flux power: no thermal smoothing, no FGPA.
  - The 575/600 misses are 0.6 and 1.5 points. A hydrodynamic flux-power test could move them either way.
- **GEB** passes. The A2744-QSO1 seed clump (M_h 6.6e6 Msun with the cold parent) collapses in time:
  - log M_BH 7.7: nu_req 3 (RARE), z_coll 14.6, t_seed 446 Myr.
  - log M_BH 6.9: nu_req 2 (EASY), z_coll 9.4, t_seed 539 Myr.
  - The escaped fraction at z 7.05 is 8.6-9.9e-4, below the frozen 1e-3, so the daughters do not enter.
  - EB1's no-go was baryons-only; a cold parent at the CMB's amount removes it, as expected.

## 2. Brackets (reported and labelled, not in the label)

- **M_min 1e10, reading B:**
  - GFo FAILS at every v_k (0.744-0.762), because more daughters escape earlier (10-11 % by z 3).
  - GF passes. GL frozen fails (+30 to +35), and GLc passes (+0.02).
- **M_min 1e12, reading B:** every gate passes at every v_k. Very little escapes (1-2 % by z 0, 0 by z 3).
- **Reading A** (every daughter escapes, no halo binding): GFo fails at every v_k and every M_min (0.64-0.90). GF passes
  (Rf 0.95-0.99). GL frozen fails (+77 to +270), and GLc passes.
- So the forest decides it. It needs the trigger at M_min >~ 1e11 Msun **and** halo binding (reading B) **and** v_k <~ 560
  km/s (linear proxy). This also bounds CK1/CK2: a release speed above about 560 km/s with a 1e11 trigger costs the forest.

## 3. Post-freeze finding: the record's lensing kernel (QX3 iter2 `limber_ratio`) omits k^-4

- `I2.limber_ratio` weights each z by (chi*-chi)^2 (1+z)^2 / (chi^2 chi*^2 H) / chi^2 times P_delta. The lensing potential's
  power carries P_Psi ∝ P_delta / k^4, with k = L/chi. That leaves a missing factor (chi/L)^4.
  - Its weight therefore runs as chi^-4, and the ratio S(L) is dominated by z ~ 0.02-0.1, at k ~ 1-3 /Mpc.
- **Check (KA_LC):** the absolute Limber C_L^pp shape divided by CLASS's own raw_cl pp, normalised at L 100, for L
  20 / 50 / 100 / 200 / 300 / 400:
  - frozen kernel: 0.045 / 0.239 / 1 / 5.26 / 15.0 / 33.0;
  - with k^-4 restored: 1.005 / 1.006 / 1 / 0.991 / 0.984 / 0.980.
  - The restored kernel matches CLASS to 2 %; the frozen one is off by up to 30x.
- **Consequence for the record (reported only; no other lane's files touched):**
  - CE2's four cells re-read with the restored kernel give Delta chi^2 0.00 (frozen 0.31 / 0.13 / 3.12 / 0.27, reproduced).
  - QX3's and QX7 iter_3/iter_4's G2' Jeans lines, KD1's G9a mu_J = 2.5e4, and CE2's M3 bite (dchi^2 265) all rest on the
    frozen kernel and need a re-read.
  - At L <= 400 the real PR4 shape is close to blind to suppression at k >~ 0.3 /Mpc.
- The frozen label above uses the frozen kernel, as frozen. The corrected column is a reported reading, disclosed as
  post-freeze.

## 4. Known answers and MUTATE

- KA1: v_k = 0 with the new 3-species solver gives max |R - 1| 6.7e-16 against iter_4's ref.
  - chi^2 is 8.570836 = c0, and Rf = 1 to 2.6e-15.
  - iter_4's K1 55.6403 is reproduced. **PASS.**
- KA2: the all-dark Jeans term at CE2's C1 gives Delta chi^2 0.311065, equal to iter_4's 0.311065. **PASS.**
- KA3: Sheth-Tormen F(>M) is bounded and decreasing in M. k_fs(z 1, 575 km/s) = 0.219 /Mpc. **PASS.**
- KA_MF: the extended CLASS model (P_k_max 400) matches MC at k 0.1 and 1 to 2e-5. **PASS.**
- GEB K1: sigma8 0.795853 equals MC.sigma8() to 5.6e-7. GEB K2: EB1's t_obs / t_seed are reproduced as 771.40 / 460.21 /
  552.41 Myr. **PASS.**
- MUTATE:
  - M1 (3000 km/s) must fail GL: it **does NOT bite** (chi^2 11.56, +2.98), so GL is NO VERDICT. M1 does fail GF (Rf 0.62)
    and GFo (0.75).
  - M2 (v_k 0) reproduces the cold case (max |R - 1| 6.7e-16) and passes every gate. **OK.**
  - M3 (reading A, M_min 1e8) fails GFo (0.45). **BITES.**
  - GEB MUTATE (parent not clustering): NO on both masses. **BITES.**

## 5. Limits and disclosures

- **Linear fluid treatment of a collisionless population.**
  - Sound speed = 1D dispersion (k_fs matching).
  - Daughters are born with the parent's delta: halo bias at birth is not modelled.
  - Recapture by growing wells enters only through linear gravity.
  - Free streaming past k_fs is approximated by Jeans oscillation.
- **Declared quantities.** The trigger is posited, with no action. v_esc = 2.69 v_vir (NFW c 5 at r_s) is declared.
  Delta_vir = 18 pi^2 x rho_crit(z) is a fill-in, disclosed: the criteria said only "18 pi^2 in the parent's background".
- **The forest** is a linear 1D matter-power proxy (L365's 10 % band), not FGPA flux power.
- **GEB fill-ins (subagent):**
  - z_coll is the earliest z with nu sigma(z) >= 1.686.
  - sigma comes from a CLASS model with N3's exact parameters, P_k_max 1500 and z_max_pk 60. It reproduces MC to 5e-11.
  - T_sal uses EB1's constants formula (450.49 Myr), which EB1's K2 requires.
  - Sheth-Tormen F(>1e11, z 7.05) = 1.15e-3 is converted. The escaped part is 8.6-9.9e-4, below the 1e-3 line, so the
    daughters do not enter GEB.
- **Background** is iter_4's (QX3 iter2 worst corner, A_s 2e-9), the one CE2 used, not QX15's footing fit.

Kappa = 1/2 FITTED; not theory closed.
