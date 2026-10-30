# PC1_perturber_ceiling_route_e — FROZEN CRITERIA (committed alone, before any script or graded number)

**Question.** CFG666/CFG671 graded strong-lens perturbers only under the law, where dark lumps do not exist (L99). Route E has dark
lumps, and below the ~1e12 crossover their cores sit on X43's floor, rho0 r0 = Sigma = a0/(2 pi G). A Burkert halo of fixed Sigma has
a maximum enclosed mass at any radius, whatever its M200 or r0. Do measured perturbers and the MW ultra-faints respect that ceiling?

Standing rules: kappa = 1/2 FITTED. Footings never pooled (9.3603e-11 / 1.1312e-10 m/s^2). Route E, Newtonian. Cold dark energy, not
matter; no particle species. No LCDM halo, mass function or merger tree enters. Not "theory closed". Nothing may say the data favour
the framework.

## 0. Seen before freezing (disclosed)

- Prompted by Leisher+ 2026 (ApJ 1005, 186), which is used for no number here; only its emphasis on low-mass lump statistics.
- Rough chat arithmetic: the ceiling is near M_max(<r) ~ 1.6 Sigma r^2, equivalently g_max ~ 0.26 a0. This is numerically close to
  X47's g_T = 0.254 a0, so it may be the same identity and is not new evidence.
- Rough expectation: J0946 dark above the ceiling by ~x30; B1938 V close to it; B1938 A above it if dark but with baryon room.
- X49's result is known: MW ultra-faints UNDER (Z +3.80 / +3.66), with the reading that they want more massive halos.
- CFG666's table g_obs/a0 is known. No UFD ceiling comparison has been computed.

## 1. Ceiling

Burkert: M3D(<r) = pi Sigma r0^2 B(r/r0), B as in X49. Projected M2D(<R) by numerical line-of-sight integration to 100 r0, with the
3D profile uncut (generous). For each radius, ceiling C = max over r0, free, with no M200 relation and no stripping. Stripping and
heating lower the inner mass, so C stays an upper bound for them. Baryonic contraction would raise it; X39 found contraction breaks
SPARC, so it is not included, and this is a stated limit. Sigma is the z = 0 value at every z (primary). Reported only: a0 lower by
6-9% at the lens redshifts (CFG689's 0.91-0.94), which tightens C.

Also reported: the r0 at the peak, and the M200 it would need from X49's solver (200 rho_c, X49's background h), to show whether the
ceiling is reached by a physically sized halo. Check that X43's collapse term stays below the floor uses X41's Sigma_coll(1e11) with
eta 25.94 (CE1).

## 2. Perturbers (inputs exactly CFG666's table)

| object | statistic | M_obs | sigma | baryon room M_b,max |
|---|---|---|---|---|
| J0946 dark, <0.3 kpc | 3D | 5.8e8 | 0.3e8 | 8 x 5.0e6 |
| J0946 dark, <0.6 kpc | 3D | 1.1e9 | 0.05e9 | 8 x 5.0e6 |
| B1938 A, <0.6 kpc | 3D | 1.13e8 | 0.06e8 | 8 x 5.4e7 |
| B1938 V, 80 pc | 2D | 1.13e6 | 0.04e6 | none published: dark reading, 0 |

R = (M_obs - 2 sigma - M_b,max) / C, per footing. Upsilon 8 is CFG666's ceiling.

Classes per object and footing: ALLOWED R <= 1; MARGINAL 1 < R <= 2 (a factor 2 covers profile-shape and spherical assumptions);
EXCEEDS R > 2. For B1938 A, also report R with M_b = 0 (the fully dark reading), not graded.

Luminous J0946 (projected M(<1 kpc) = 10^8.9, 95% 10^8.1 to 10^10.0; CFG666's M_b band 1.0e8 to 8.3e8): CONSISTENT if
[M_b low, M_b high + C] overlaps the 95% interval. Reported only: M_b + C over M_b at 0.3 and 1 kpc beside CFG667's sealed Q_max.
Sealed files are not edited.

## 3. Ultra-faints: can a heavier halo rescue X49?

X49's data and rows() conventions unchanged (X1 CSV, Arroyo-Polonio binary correction, g_obs = 3 sigma_c^2 / r12, r12 = 4/3 rh,
M_b(<r12) = M_b/2). E_C = log10(g_obs / (g_N + G C3D(r12)/r12^2)) per system with sdMC error. Same 10000-resample bootstrap, seed
20261026, on the median, per class, for X49's five classes.

- MW ultra-faint median Z_C > +2: **NO M200 RESCUES** (X49's "more massive halos" reading closed for pure floor halos).
- |Z_C| < 2: **CEILING ADMITS** (a heavier halo could fit; then report the needed M200 per system against X49's extrapolated M200).
- Z_C < -2: **BELOW CEILING** (same follow-up).

Also the count of ultra-faints with E_C > +2 s individually. Reported: Crater II, Antlia II, Sagittarius.

## 4. Lane label (per footing, footings separate)

- J0946 dark EXCEEDS: route E joins the law in needing the luminous solution; CFG671's deciding observation stands for both.
- B1938 V: ALLOWED or MARGINAL only means possible at a specific r0; this is not a detection or a pass for route E.
- If any object is EXCEEDS and has no alternate published solution, it is named as route E's stated falsifier.

## 5. Checks

K1: numerical C equals a direct dense-grid search to 1e-3. K2: M3D limit r/r0 -> 0 equals (4/3) pi Sigma r^3 / r0 to 1e-3. K3: at 1e12,
M(<R200) = M200 with X49's solver. K4: X49's MW ultra-faint E reproduced to 0.005 by this script's rows at X49's M200. MUTATE
(`--mutate`): Sigma / 10 must lower C by exactly 10 and move Z_C upward; exit 1 if it does not bite. Own outputs named `_MUTATE`.

## 6. Limits named now

Burkert shape is the record's choice, and other cored shapes give a different factor (hence MARGINAL's width). X81 found native zoom
halos are cusps through the epsilon cut at 1e12, while low-mass native profiles are unmeasured (X80 queued); if low-mass lumps are
cusps, the ceiling does not apply and the floor rule itself is wrong there. Lens masses depend on assumed lens profiles. Perturbers
may be line-of-sight objects. Ultra-faint errors omit tidal non-equilibrium and systematic r_h errors.
