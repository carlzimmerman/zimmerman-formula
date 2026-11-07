# NC4 frozen criteria: the born-clumped cold dark energy clump spectrum (R3 / K3, R7, K5), both footings

**NC4 = Framework Candidate 2's NC1.** The candidate file (`FRAMEWORK_CANDIDATE_2_BORN_CLUMPED_2026_11_07.md`,
69d4583c8b, section 5) calls this lane "NC1"; that id is already taken on the record (CFG484 / CFG489, "NC1 chassis"),
so it runs as NC4. Committed alone, before any NC4 script or number. TEST lane. Adopts nothing. Kappa = 1/2 FITTED;
not theory closed.

Rules: no LCDM mass function or LCDM input, no particle, no downloads; the component is "cold dark energy". Both footings,
never pooled (canonical a0 9.3603e-11 m/s^2, Lstar 21.7 pc; alt a0 1.1312e-10 m/s^2, Lstar 22.9 pc); a pass needs both.
One thread, < 1 GB RSS per process, SIGTERM writes a partial JSON; peak RSS reported. Every input is on disk and read-only.
Not graded here: NC2 content (CMB bias, CMB lensing, forest, mu) and NC3 content (member vs field early types). No
CMB-lensing number built on QX3 iter2's limber_ratio is used (HOLD_KERNEL_REREAD_2026_11_07.md). L388 retention is not
used anywhere (LCDM-referenced).

## 0. The picture graded, in its own terms

The cold dark energy at the CMB's amount (QX15; native R = rho_d / rho_b = 5.562, QX12; omega_d 0.1209) is born in
clumps that fill a comoving volume fraction phi of space at density rho_d / phi; outside the clumps it is zero.
Baryons are born uniform. Every clump becomes a group or cluster host (R3: no baryon-free clumps); field galaxies form
outside clumps (f = 0 by construction, so SPARC <= 0.33 / 0.19 and the KiDS field rows read PASS BY CONSTRUCTION, stated,
not evidence). f is the cold dark energy mass over the baryon mass inside the host's radius, in GB1's L0 convention
(b = 1 + f), exactly as KD1's f-table.

## 1. Inputs (read-only)

- **KD1 f-table** (`closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json`, footings.*.uniform_f_diag): X-COP 4.1786 / 3.7833,
  groups f*1 1.2320 / 0.9323 to f*0 3.4640 / 2.8646, SPARC cap 0.3257 / 0.1937, capture 4.1110 / 4.1121; KD1's QX15
  footing setting (omega_b, omega_d, h) and Omega_r.
- **X-COP**: NA2's machinery verbatim (QX7 iter_5 prelude exec'd read-only; NA2's shape normalisation, x_eval, golden fit,
  bin edges 0 / 0.25 / 0.5 / 0.75 / 1.0 / 2.0 r/R500, gate |mean| <= 0.05, rms <= 0.10, every bin with >= 3 points
  |bin mean| <= 0.10). R500 from the fgas FITS header. HSE M500 / M200 per cluster from `xcop_r500_ettori2019.json`.
- **eRASS1** primary catalogue `real_research/data/erass1cl_primary_v3.2.fits`, read with NA2's census columns and cuts
  (BEST_Z, PCONT, MGAS500 x 1e11, M500 x 1e13; 0.02 <= z <= 0.10, PCONT <= 0.5) plus F500 (1e-14 erg/cm^2/s).
- **Lovisari+2015 groups** and **UA1 joint posterior** through CK3's data side (se2.py exec'd read-only to its main loop,
  ua1.py's groups-knob block verbatim; written to a temp dir outside the repo), at f = carrier f, eps = f / 5.4 in CK3's
  convention (the 5.4 cancels between need and prediction).
- NC3 (39940c070e) for the core rule (section 6); QX33 CLASH lensing-only slope s past the BCG, -0.08 to -0.13 (soft).

## 2. The collapse model (stated in advance; own terms, in the law's field)

A clump is a Lagrangian top-hat: cold dark energy at rho_d / phi plus baryons at the mean, i.e. born matter overdensity
Delta_b = (R / phi + 1) / (R + 1) - 1 with R = 5.562. Its outer shell is integrated in physical radius from z_b with the
Hubble velocity (zero peculiar velocity, the generous start: growth before equality is ignored),
r'' = -g_law(G M / r^2) - (8 pi G / 3) rho_r(t) r + (8 pi G / 3) rho_L r, with g_law the record's law (QX7 iter_5 `glaw`,
per footing a0), M the clump's matter, and the KD1 QX15 footing background (omega_b, omega_d, h, Omega_r; Omega_L = 1 -
Omega_m - Omega_r). It turns around at r_ta and virialises at r_f = lambda r_ta. If it has not turned around by z = 0, its
z = 0 radius is used (generous: an unvirialised extended clump). Profile after collapse: a uniform sphere of radius r_f
(the virialised top-hat is cored by construction, core = r_f); all of the clump inside r_f.

**Free numbers:** phi (grid 0.01, 0.03, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99, 0.995, 0.999, 0.9995, 0.9999);
z_b = z_eq of the footing background (primary) and 1100 (bracket, later and more favourable); lambda = 1/2.
The clump's total mass = (1 + f) M_b(<R500) X per X-COP cluster, X from section 3. Nothing is fitted to K5.

## 3. R3 / K3: abundance and cosmic share

**Statistic and volume.** The 1/Vmax host baryon mass function of eRASS1: hosts with M500 >= 1e13 Msun in
0.02 <= z <= 0.10, PCONT <= 0.5, F500 >= F_lim; D = cz / H0 (Euclidean, h 0.70, the catalogue's convention as NA2;
bracket h 0.674 and 0.74, with M_gas scaled by (h / 0.70)^-2.5 as in NA2's census); V_max,i = (Omega / 3)
[min(D_i sqrt(F500_i / F_lim), D(0.10))^3 - D(0.02)^3]; Omega = 20,626 deg^2 (NA2 primary), bracket 13,116 deg^2.
F_lim = the smallest value on the grid {2, 5, 10, 20, 50} x 1e-14 erg/cm^2/s at which the Schmidt test passes (mean
V/V_max within 2 sigma = 2 / sqrt(12 N) of 0.5); neighbouring grid values reported as brackets. Host baryons
M_b = M_gas500 (1 + s): clusters (M500 >= 1e14) s = X-COP mean M*/M_gas at R500 (NA2's sX); groups s in {0, 1}.
The cosmic share: rho_d = R rho_b, rho_b = 0.02166 x 2.775e11 Msun/Mpc^3 (NA2's BBN number) with native omega_b
0.1209 / 5.562 as bracket.

**The spectrum.** f(M500) = f_X + s_f log10(M500 / M_X), f_X = KD1's X-COP need, M_X = median HSE M500 of NA2's X-COP set,
s_f on 0, 0.1, ..., 4.0 per dex; f floored at 0 (hosts below the floor carry none) and not capped above (generous). One clump per host: the clump number spectrum is the observed host spectrum times a normalisation A.
Each clump carries M_cde = X f(M500) M_b. The capacity C = Sum_i X f_i M_b,i / V_max,i / rho_d is the fraction of the
cosmic cold dark energy the observed hosts can hold; the abundance the spectrum needs is A = 1 / C times the observed.
X = 1 in the collapse model when r_f <= R500 (all of the clump inside R500), else M_c,tot / M_c(<R500) of the section-2
sphere. Bracket X_HSE (generous, reported and used for the "best" reading): X = 1 + (M200 - M500)_HSE / (f M_b(<R500))
per X-COP cluster, median applied to every host (the most cold dark energy the HSE masses allow between R500 and R200).
Also reported: extension below 1e13 by a power law fitted to the two lowest populated bins, down to f's floor; the
theorem bound C <= max f / R x (host baryons / rho_b) <= max f / R.

**Gate K3 / R3 (per footing):** PASS iff A <= 2 (the observed host abundance times at most 2, a generous completeness and
mass-systematics allowance) in the most generous bracket combination (largest C over area, h, F_lim, s, X_HSE,
extension), AND the f-table holds (X-COP f_X by construction; the spectrum's f at the median Lovisari group M500 inside
[1.2320, 3.4640] / [0.9323, 2.8646]). Otherwise FAIL, with A reported. X-COP (12 clusters, 0.04 <= z <= 0.10) and
Lovisari (no selection volume on disk) are not complete samples: X-COP is reported as a lower bound n(> M) >= N / V
over the whole sky (generous, the smallest density) and checked against the spectrum's implied n(> M); Lovisari's
abundance is NOT EVALUABLE (no volume), its masses enter R7 only.

## 4. R7: the f-mass trend against UA1 (CK3's tests)

The spectrum's f at each Lovisari group's M500, eps = f / 5.4, through CK3's data side: test A (slope of eps vs log10
M500: 95 % of data minus prediction contains 0; data need +0.21 / +0.20 per dex, 95 % [+0.04, +0.49] / [+0.05, +0.45])
and test B (UA1 class step with the component: 95 % contains 0). R7 PASS iff A and B pass. Graded at every s_f; the
graded spectrum is the "best" one (section 7).

## 5. K5: the early-collapsed clump's profile at X-COP's radii

Per X-COP cluster (NA2's set), per footing, per phi and z_b: the section-2 clump's concentration
c = M(<0.25 R500) / M(<0.7 R500) against NA2's gas-to-stars band per cluster [c_gas,i, c_stars,i] (reported against the
HSE need c_HSE,i, record range 0.21-0.30), and NA2's per-bin X-COP gate for the clump shape (normalised as NA2's shapes
at Mb_last's radius) at the NA2-fitted amount (golden on [0, 30]) and, reported, at the f-table amount.
K5 PASS at a phi iff (a) the core rule (section 6) holds, (b) c is inside the band for every cluster, (c) NA2's per-bin
gate passes at the fitted amount. K5 PASS overall iff one phi passes on both footings at z_b = z_eq (the bracket z_b 1100
reported).

## 6. NC3 addition (from 39940c070e, folded in before freeze): the core rule

NC3 found that cluster-member early types carry no residue at r_half (+0.011 / +0.012 dex, at most ~16 % extra mass);
stripping cannot hide one. So inside a clump the component must be smooth below a galaxy's half-light radius, minimum
clustering scale ~0.1 Mpc. **Core rule, stated in advance:** the clump density profile is flat inside 20 kpc
(|d ln rho / d ln r| <= 0.5 at r <= 20 kpc, i.e. a core radius r_c >= 20 kpc; an NFW-type cusp fails) and the clump's
smallest scale (r_f, or r_c) is >= 0.1 Mpc. The virialised top-hat satisfies the flatness by construction; its size rule
r_f >= 0.1 Mpc is graded.
**Cored-profile question (reported, both footings):** independent of the collapse model, does any cored profile meeting
the core rule sit in NA2's band and pass NA2's per-bin rule? Family rho = rho_0 (1 + (r / r_c)^2)^(-gamma / 2),
gamma in {2, 3}, r_c on 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000 kpc, amount fitted per NA2's rule. Reported:
which (gamma, r_c) pass band + gate on both footings.
**CLASH (soft, no label):** each profile's slope s = d log10(M_cde / M_b) / d log10 r over X-COP's points past 100 kpc,
cluster median, next to CLASH's -0.08 to -0.13.

## 7. Labels (per footing; overall the worse; "one spectrum" means one (s_f, phi, X) on both footings)

- **NO VERDICT**: a KA fails, or a MUTATE that must bite does not.
- **CANDIDATE ON NC1 ROWS (scoped)**: R3 / K3, R7 and K5 all pass on both footings with one spectrum.
- **FAILS (rows)**: otherwise, the binding row named (the row with the largest miss).
- The best spectrum is the one with the largest C among those passing R7 and the f-table (if none pass R7, the largest C
  overall); its A, R7 and K5 numbers are reported whatever the label.

## 8. Known answers (fail = stop; nothing graded before they pass)

- KA1 KD1's f-table read exactly: X-COP 4.1786 / 3.7833, SPARC cap 0.3257 / 0.1937, groups 1.2320-3.4640 /
  0.9323-2.8646, capture 4.1110 / 4.1121 (|d| <= 1e-4).
- KA2 NA2's band and shapes: concentrations per cluster, ranges gas 0.16-0.24, HSE 0.21-0.30, stars 0.32-0.51 (to 0.01,
  CK1's report); NA2 stars fit F 1.723 / 1.560, rms 0.1208 / 0.1138 (to 1e-3); baryon-traced at KD1's need mean 0, rms
  0.0818 / 0.0835 (to 1e-3).
- KA3 NA2's eRASS1 census: 467 clusters, 590 groups, V 1.63e8 Mpc^3, host baryons 0.0108 of rho_b (to the printed digits).
- KA4 UA1 / CK3: f = 0 reproduces UA1's step +0.259 / +0.221 (array_equal with post_groups2), and the data slope +0.21 /
  +0.20 with 95 % [+0.04, +0.49] / [+0.05, +0.45] (to the printed digits).

## 9. MUTATE (separate *_MUTATE* outputs; must bite / hold)

- M1 flat spectrum (equal cold dark energy per dex of M500 from 1e13 to 10^15.5 Msun, normalised to rho_d, f by the
  spectrum): its implied host number per 0.25 dex bin against eRASS1's 1/Vmax per bin (bins with >= 5 hosts); must FAIL
  the per-bin abundance (some bin off by more than a factor 2), else NO VERDICT.
- M2 uniform component (phi = 1, every system captures at model P f_cap 0.76): f = 0.76 omega_d / omega_b at KD1's
  setting must reproduce 4.111 / 4.112 (|d| <= 1e-3); it must also fail the field (f > SPARC cap): bites.
- M3 planted abundance: hosts multiplied by 1 / C (the abundance that closes the budget) must read K3 PASS (the gate can
  pass), and the planted top-hat with r_f set to 0.4 R500 must land inside the band for at least one cluster (the band
  test can pass).

## 10. Expected outcome (stated in advance, honestly)

**FAILS (rows), binding K3.** With every host at f <= 4.18 / 3.78 < R = 5.562, the hosts cannot hold the cosmic cold dark
energy even if every baryon sat in them (C <= 0.75 / 0.68); eRASS1's hosts hold a few per cent of the baryons inside
R500, so A ~ 20-100. K5 is also expected to FAIL: an early-collapsed top-hat with the field empty (phi <~ 0.99) virialises
at z >~ 15 into r_f << 0.25 R500, so c = 1, far above the band; only phi -> 1 (the uniform component KD1 already failed on
the galaxies) collapses late. R7 is expected to PASS for a range of s_f (a fitted slope, consistent rather than
predicted). The cored-profile question is expected to find cored profiles with r_c ~ 100-300 kpc that sit near HSE; the
collapse model does not produce them.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
