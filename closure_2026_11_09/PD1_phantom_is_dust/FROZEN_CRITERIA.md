# PD1 (the phantom IS the dust, the outside source's variant N): FROZEN CRITERIA, committed alone before any PD1 script or number

TEST lane, quarantined; registered RUNNING by the orchestrator. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11) and alt (1.1312e-10), never pooled. A FAIL is verified as hard as a PASS. Read-only machinery: WL1
(shell / turnaround solver, phantom formulas, GSMF; own transcription, verified by known answers), QX8 / GB1 loaders (as TS1),
SS1 halos, DB1's Bullet child (via WM1's wm1_local.py bchild), WM1's cold-reference cosmology numbers.

## 1. Construction N, frozen once

- **One conserved cold field** ("dust"), omega_d = 5.41 omega_b (QX15 footing values). Baryons move on the plain metric: no nu
  acts on baryons anywhere. Gravity is Newtonian (GR) with the total mass.
- **On the single-stream web** the field is cold dust. The linear cosmology is then exactly the record's cold reference (CMB,
  lensing, growth, forest, seeds).
- **Inside the shell-crossed region** of a halo, r <= R_ms, the field's density takes the law's phantom profile of the halo's
  baryons. For a spherical baryon mass M_b:
  - M_ph(<r) = M_b (sqrt(1/4 + 1/y) - 1/2), with y = G M_b / (r^2 a0) (WL1's Mph). So g = glaw(g_N,b), the law, exactly.
  - Elsewhere the record's law convention applies (SPARC: glaw on the measured g_N, QX8's exact-field term kept).
- **R_ms = the Newtonian turnaround radius at the epoch** (physical). It comes from WL1's shell solver with a0 = 0 and the excess
  dM = M_b (1 + R). This is the largest region that can have shell-crossed (generous; WL1's "ceiling" convention).
- **The share (stated).** The conserved dust a halo owns at epoch z is the dust in the Lagrangian sphere of the shell that turns
  around at z: share = rho_bar_d (4 pi / 3) x_ta^3 + R M_b. Here x_ta is the comoving Lagrangian radius of that shell, and R M_b
  is the dust part of the excess.
  - Bracket S-AM (reported, never graded): share = (omega_d / omega_m) M_h, with M_h the Moster 2013 halo of M_* = M_b (SS1's
    moster_halo).
  - Bracket S-src (reported): the source's R_trunc of 1.35 Mpc for an L* galaxy, translated into its implied share.
- **Truncation:**
  - If M_ph(<R_ms) > share, the phantom profile stops at R_trunc, where M_ph(<R_trunc) = share. No dust is left over, and outside
    R_trunc the halo is Newtonian with M_b + share.
  - If M_ph(<R_ms) <= share, the leftover share - M_ph(<R_ms) sits in its own profile: an isothermal sphere (M proportional to r)
    truncated at R_ms. It is Newtonian: the law never acts on it.
- **Form choices beside the label:** R_ms = turnaround; the share's Lagrangian definition and seed dM = M_b (1 + R); the leftover
  profile; the spherical phantom formula. Fitted: 0.

## 2. Gates and lines (order P1, P2-KiDS, P2-SPARC, P3-groups, P3-X-COP, P4, P5, P6)

| gate | quantity | line |
|---|---|---|
| **P1 conservation (population)** | q_N(z) = [GSMF-summed M_ph(<R_ms)] / rho_bar_d at z 0.5, 1, 2 (WL1's q_pop with R_ms Newtonian, no truncation) | q_N <= 1 at every z (the orchestrator's line: the phantom cannot exceed the dust) |
| P1 per halo (reported; drives the truncation) | M_ph(<R_ms) / share and R_trunc at log M_b 7-15, z 0, 0.5, 1, 2 | reported |
| **P2 KiDS** | 59 points, pointwise g with the truncated phantom (+ leftover) at z 0 (as WL1); WL1's projected mean shift reported beside | \|shift\| <= 0.05 at every point (SS1 gate 1) |
| **P2 SPARC** | QX8 fit with g = glaw(g_N) inside R_trunc; outside, g_N + (glaw - g_N)(R_t)(R_t / R)^2 (+ leftover). R_trunc from M_b at Upsilon 0.5 | SS1 G5 (rms <= L0 + 0.010, \|mean\| <= 0.05, same for the massive tail) |
| **P3 groups** | g = glaw(g_N,b) inside R_trunc + leftover's Newtonian pull; share from M_b,sys = g5 (1 + f*) | >= 16 of 20 at f* 0 and 1 |
| **P3 X-COP** | likewise, share from Mb_last. (phantom + leftover) / M_dyn per bin vs TR1 0.71 / 0.66 / 0.58 reported | SS1 gate 3 lines |
| **P4 cosmology** | cold dust + Newtonian baryons is the record's cold reference. Carried: CMB primary (QX15 L1 PASS, Delta -64.7), CMB lensing 8.56 (line 18.48), forest Delta chi^2 0, fsigma8 ratio 1, S8 change 0, seeding 1. Plus WM1 A2's KA-S2: the Newton two-fluid ODE equals CLASS cold to 1.4 %. The 1-halo redistribution (total conserved) is NOT EVALUATED: the record has no halo-model lensing machinery; stated | the WM1 lines |
| **P5 Bullet** | DB1 child. The phantom follows the baryons (the law on each subcluster's baryons, DB1's law-only row, which is the KA row); the leftover is collisionless and galaxy-traced | DB1 label |
| P6 | Coma UDGs (UA1, reported: law only; the host's leftover reported); Ursa Major and Cassini carried as law-only (N equals the law inside R_trunc; the record's law PASS) | carried / reported |
| **P7 dynamics** | statement: does a conserved dust's equation of motion produce rho_ph, or is it a closure? | reported |

**Label:** PASS iff P1, P2-KiDS, P2-SPARC, P3-groups, P3-X-COP, P4 and P5 pass on that footing. Otherwise FAIL, naming the first
failing gate in that order.

## 3. Known answers (NO VERDICT if KA-P1 or KA-P2 fails)

- **KA-P1:** the transcribed solver on WL1's own background (OB 0.0215, OD 0.11958, H0 65) reproduces WL1's q_pop at z 1
  (law-on R_ms): 0.936 / 1.079 within 1 %.
- **KA-P2:** WL1's KiDS ceiling mean projected shift +0.0011 / +0.0009 within 0.0005.
- **KA-P3:** with truncation off (R_trunc = infinity, no leftover), every local gate equals law-only: KiDS 0, X-COP +0.4675 /
  +0.4345, groups 0/0.
- **KA-P4:** spherical closed form. M_ph(<r) -> r sqrt(M_b a0 / G) in the deep limit, to 1e-3 at y = 1e-6.

## 4. Hand estimates (before any number)

- **The share is far smaller than the phantom.** The deep phantom inside r is sqrt(M_b a0 / G) r.
  - For L* (M_b about 8e10), that is about 8e12 Msun per Mpc.
  - The turnaround region (about 5.5 rho_bar inside r_ta) holds about 8e11 (r_ta / Mpc)^3 Msun of dust.
  - With r_ta about 1.5 Mpc, the share is about 3e12 against a phantom of about 1.2e13: **per-halo conservation fails by about 4x**,
    and R_trunc is about 0.3 Mpc, not the source's 1.35.
  - **Dwarfs:** M_ph / M_b = r / r_M, with r_M = sqrt(G M_b / a0) = 0.34 kpc at 1e8. A share of about 6-10 M_b truncates at
    2-4 kpc.
- **Expected kills:**
  - P1: q_N > 1 at z 0.5, as WL1's 1.31 / 1.51.
  - P2-KiDS: about -0.5 dex at 1-3 Mpc.
  - P2-SPARC: dwarf and LSB outer points fall to Newtonian.
- **Clusters:** the leftover is large. X-COP should be over-filled like WM1 (phantom + nearly the full share).
- **Bullet:** phantom on the gas, the classic failure, with the leftover galaxy-traced. Expected FAIL.
- **P4:** passes (the cold reference).
- **P7:** a collisionless dust's Jeans equilibrium gives rho proportional to sigma^2 / (G r^2). Nothing in a dust action ties
  sigma^4 to G M_b a0, so the normalisation is a closure. Moreover a single scalar field's stress tensor is single-stream
  (h_mn T^mn = 0): its "own dispersion" S^2 vanishes identically and cannot act as the switch.
- **Expected label: FAIL / FAIL, first failing gate P1.**

## 5. MUTATE

- **MP1, share x 10:** truncation radii grow. The KiDS / SPARC statistic must move (power).
- **MP2, truncation off:** reproduces law-only (KA-P3) and makes P1's per-halo violation explicit.

## 6. Operational

- One thread, nice 10; RSS < 1 GB; small json / out.
- Explicit-path commits via a sparse temporary worktree, removed after.
- Files: pd1.py (P1, P2, P3, KA, MUTATE), pd1_bullet via WM1's bchild, pd1_grade.py, pd1.json / .out, pd1_MUTATE.json / .out,
  RESULT.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
