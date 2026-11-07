# QX27 frozen criteria: a cold dark energy sector heated at z_h into a power-law-tail velocity distribution

Frozen before any QX27 script or graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane:
COLD DARK ENERGY sector, no particle, no LCDM inputs. Rules: ../SWARM_BRIEF.md. Inputs reused read-only: QX10 iter_2
(hosts, r_ta, R, background corner), QX12 iter_3 (Amendment A1 hosts: KiDS exponential discs, regular cluster cores),
QX8 (SPARC exact-field parts and line), QX18 (ellipticals line), QX3 iter2/iter3 (growth ODE, PR4 lensing, forest line).
No heating microphysics is built: the heating epoch is a parameter.

## The class

- Before z_h the sector is cold (pressureless): it is the CMB-era cold component (QX15).
- At z_h it is heated once into an isotropic, NON-THERMAL speed distribution with a power-law tail:
  p_n(v) = N v^2 (1 + v^2/(m v0^2))^(-m), m = (n + 2)/2, so p ~ v^-n above v0. Finite kinetic energy needs n > 3.
  The CDF is F_n(v) = I_t(3/2, m - 3/2), t = u/(1 + u), u = v^2/(m v0^2) (regularised incomplete beta).
  After z_h the sector is collisionless; peculiar speeds decay adiabatically (v ~ 1/a). v0 is the value today.
- Retention in a host (the class as posed): the host gathers the cosmic share R = omega_d/omega_b = 5.562 of its
  baryons (QX12 iter_2's T1 amplitude; profile frozen: the sector traces the baryons), and each shell keeps the part
  slower than the local escape speed:
  dM_X = R F_n(v_esc(r)) dM_b, v_esc(r) = sqrt(2 H(r)), H(r) = integral from r to r_ta of g_tot,
  g_tot = glaw(G (M_b + M_X)/r^2) (the a0 law on), solved self-consistently (damped Picard, as QX12 iter_3).
  r_ta: QX10's rule. Hosts: QX12 iter_3 / A1 (SPARC G5 list and KiDS as exponential discs, ellipticals from QX5,
  X-COP and groups from measured baryon profiles with uniform cores).
- Reported variant only: capture amplitude f_cap R (f_cap 0.76, QX10's convention) instead of R.

## Constants fixed by non-cluster data only

- z_h = 10, the latest heating T1 allows. Static gates do not depend on z_h; growth is most favourable at the latest
  heating. z_h = 20 is reported for G6.
- n grid: {3.5, 4, 5, 6, 8, 12}. No non-cluster datum on the record fixes n, so every n is graded.
- v0 per (n, footing): v0_min = the smallest value on a 71-point log grid 100-30000 km/s at which both calibration gates
  pass there and at every larger grid value (retention falls with v0). This is the most retention galaxies allow.
  - C1 (SPARC G5 list, QX10 line): M_X(<R_opt)/M_b <= 0.3.
  - C2 (KiDS isolated lenses, QX10/QX12 line): |mean shift| <= 0.05 dex.
- No cluster or group number enters any constant. No scan against cluster data is used to pick anything.

## Gates, graded at (v0_min(n), n), both footings separately (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2)

- G1 SPARC: QX8's exact-field grade (algebraic law + QX8's per-point T from its saved parts), with the sector's
  g_X = G M_X(<r)/r^2 added to g_bar. Sector per galaxy from an exponential-disc host, M_b = 0.5 L[3.6] + 1.33 M_HI,
  R_opt = 3.2 Rdisk, held fixed across the U grid. Line (QX8): rms <= 0.110 and median U in [0.50, 0.80].
- G2 KiDS: |mean shift| <= 0.05 dex. This is calibration gate C2, so it passes at v0_min by construction; it is
  reported as such, not counted as a prediction.
- G3 X-ray ellipticals: QX18's line on the absolute offset, |D| <= 0.15 dex, D = mean log(M_obs/M_pred) at 2, 4,
  8 Re (Kroupa hosts, QX5's EL), with the sector included. KA2 checks the plain-law D against QX18.
- G4 X-COP: HO1 line, |mean| <= 0.05 and rms <= 0.10 dex on log(M_obs/M_law(M_b + M_X)).
- G5 groups: QX5's mean-band rule over the two stellar allowances (band [f_st 1, f_st 0] meets 0 within 0.05).
  QX10's strict count (>= 16/20) is reported.
- G6 T1 / growth (n-dependent, a0 does not enter at linear order: QX3 assumption A-web):
  - G6a: cold for z > z_h, by construction (stated).
  - G6b: QX3 iter2/iter3 growth ODE at iter2's worst corner, with the sector's physical Jeans wavenumber
    k_J = sqrt(4 pi G rho_X(a)) / sigma(a) for z < z_h and no Jeans term for z > z_h; sigma = 1D dispersion of p_n,
    sigma(a) = sigma0/a (adiabatic, graded). Line: Delta chi^2 <= 4 on PR4 lensing against the cold reference (QX3
    iter2 G2 line). Reported: sigma constant after z_h (generous), and z_h = 20.
  - G6c: forest (QX3 iter3 G4'): comoving Jeans length 2 pi (1+z)/k_J <= 0.42/h Mpc at z = 3.
  - G6 PASS needs G6b and G6c. If CLASS or the PR4 package cannot run in small compute, G6 is NOT EVALUABLE and the
    missing input is stated.
- G7 dSphs: the 8 MW classical dSphs in McConnachie 2012 (Carina, Draco, Fornax, Leo I, Leo II, Sculptor, Sextans,
  Ursa Minor), Plummer hosts with M_* = 2 L_V and r_half = R2. Shift = log10(g_law(with sector)/g_law(without)) at
  r_half. Line: median shift <= 0.05 dex (not over-boosted).
- G8 phase-space (Liouville) consistency of the capture the class assumes. The heated sea is collisionless after
  z_h, before any X-COP cluster or group assembles, so its coarse-grained phase-space density cannot exceed the sea's
  maximum f_max = rho_sea N/(4 pi) (rho_sea = cosmic mean sector density today, QX10's RHO_D0; N from p_n with
  today's v0). The bound density inside the local escape sphere is then at most rho_max(r) = rho_sea N v_esc(r)^3/3,
  plus the sea itself. PASS if M_X(<r) <= integral of 4 pi r^2 (rho_max + rho_sea) at every graded X-COP and group
  radius (both stellar allowances). Reported for galaxies too.

## Labels

- Per gate, per footing, per n: PASS / FAIL (NOT EVALUABLE only for G6 as stated).
- PASSES ALL only if, at some n, G1 and G3-G8 pass on both footings, and that holds for every n on the grid. If it
  holds only for some n, the label is CLUSTER-SET (a FAIL by the no-tuning rule), reported as a lead.
- Otherwise FAILS at <gates>: the gates that fail at every n on at least one footing. Say which corner of the
  triangle (T1 / T2 / T3) each failure is.

## Known answers

- KA1: F_n -> 1 for v -> infinity; F_n at n = 400 matches the Maxwellian CDF of the same v0 to 2e-3.
- KA2: the plain-law ellipticals D equals QX18's +0.210 / +0.189 within 1e-3 (if not, reported and G3 graded as
  computed).
- KA3: R = 0 returns the plain-law X-COP +0.4675 / +0.4345 within 2e-3.
- KA4: G1 with R = 0 returns QX8's exact-field rms 0.0560 @ 0.58 / 0.0558 @ 0.52 within 1e-4.
- KA5: v0 = 30000 km/s returns plain-law galaxy shifts (|C2| <= 0.02).

## MUTATE and controls (separate outputs)

- M1 (the required twin): replace the tail with a Maxwellian of the same v0, p ~ v^2 exp(-v^2/v0^2) (QX12 iter_3's
  thermal class, its n -> infinity limit), at each n's v0_min. It must FAIL at least one of G1, G3-G5, G7, G8 on both
  footings, else it does not bite. Reported: the Maxwellian with its own calibrated v0_min.
- M2: R = 0 must return KA3's numbers (the sector amplitude is what the cluster grade rests on).
- M3: v0 = 30 km/s, n = 4 must fail C1 or C2 (the calibration gates have power).
