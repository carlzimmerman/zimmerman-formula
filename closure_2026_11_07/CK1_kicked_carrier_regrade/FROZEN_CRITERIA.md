# CK1 frozen criteria: the L388 kicked collisionless carrier re-graded at today's needs

Frozen and committed alone, before any CK1 script or CK1 number exists. Adopts nothing. Kappa = 1/2 FITTED; not theory
closed. TEST lane under the owner's 11-04 rule: it reopens a retired cold-sector item (the "cold dark energy" carrier
shed at halo virialisation, L365-L390) to grade it, and adopts nothing. No particle claim, no downloads, no LCDM input
beyond what L365-L390 already used and disclosed (stated in section 1). Both footings, never pooled; a pass needs both:
canonical a0 9.3603e-11 m/s^2, Lstar 21.7 pc; alt a0 1.1312e-10 m/s^2, Lstar 22.9 pc. One thread per process, under
1 GB RSS, SIGTERM writes a partial JSON and exits; peak RSS reported.

Spec: closure_2026_11_07/RESOLUTION_2026_11_07.md (ab75dae2e3) sections 1-3, lane CK1; DEDUCTION_2026_11_07.md
(884824f15b) cell A; XR13 README lines 115-138. CK2 (release speed), CK3 (groups f-sigma slope against UA1's
posteriors) and CK4 (CMB lensing, fsigma8, forest, early black holes) are other sessions' lanes and are not graded here.
Scope addition from the coordinator (received before this file was committed): rows T (SPARC high-mass tail, per
galaxy) and MW (Milky Way) in section 5, the retention curve against v_esc(r_F) in the JSON, and the unit-consistent
X-COP placement (section 3).

## 1. What is reused, read-only, and what it already assumed

- **L388** (`real_research/dark_sector_2026/L388_linear_gate_pooled_results.json` and `_MUTATE.json`): per-halo retention
  eps = carrier mass in a 1 Mpc/h sphere around each peak of M(<1 Mpc/h) >= 6e13, divided by the same sphere in the
  matched no-decay run, at v_k 575/600/625/650 (three 100 Mpc/h boxes, 0.39 Mpc/h mesh), and at v_k = 0 (MUTATE runs).
  **Disclosed:** the reference of eps is L388's no-decay run, a LCDM-like collisionless halo with a LCDM-like initial
  spectrum; L388's own disclosure. CK1 therefore never grades against "a fraction of a LCDM-like halo". It converts eps to
  KD1's own-terms amount (section 2) and grades against KD1's f-table.
- The PM machinery cannot be re-run under this lane's limits (256^3 mesh with 2 x 192^3 particles is well over 1 GB per
  process, and L388 took 9834 s on 8 processes). So **v_k 500, 525, 550 and 2000 are not run in the box** (section 3).
- **XR13's** X-COP mass assignment (`XR13_door_cosmology.py` (g): the NFW fit in each `*_hydro_mass.fits`, M(<1 Mpc/h)
  with h = 0.6736) and its reading "every X-COP cluster is in L388's top bin, every Lovisari group above the lowest bin".
- **GB1** battery (`closure_2026_11_06/GB1_all_gates_battery/gb1.py`, loaded by prefix exactly as KD1 and NA2 load it),
  its gate functions and lines G1-G8 unchanged; **KD1** `kd1.json` (capture C_f = 4.1110 / 4.1121, f-table,
  omega_b, omega_d, h); **NA2** `na2.py` (X-COP shapes and per-bin grader, QX7 iter_5 prelude) loaded by prefix;
  **PB3** `pb3.json` (SE2 95 % intervals, model U); **UA1** `ua1.json`; **X5** best MW cells; **L376/L390** verdicts.
- The current law with the adopted blend stiffness (owner decision 71e4014cd5: v3s + Pi^6 blend, b = rho_DE): in the
  static weak field at r >> Lstar every row here reduces to the algebraic law g = g_law(g_N) per footing; the blend
  acts only inside ~Lstar (Solar System). G8 is therefore the record's number for the adopted action (GB1 L0, C6P lines).
- **The carrier feels and sources the law's field** (primary; the current law has one field equation for all matter).
  L353's September posit (kernel-invisible: the carrier feels Newton only and does not source the phantom) is reported
  as a reading only, never graded.

## 2. Amount: KD1's own terms

- Per system the carrier adds a baryon-like mass fraction (GB1 / KD1 interface, b = 1 + f inside the law).
- **Clusters and groups (from L388):** F = C_f x eps, C_f = KD1's capture 4.1110 (canonical) / 4.1121 (alt). At v_k = 0
  this is KD1's capture by construction when eps(0) = 1, which MUTATE checks against L388's own v_k = 0 runs.
- Reading only (not graded): the RESOLUTION's normalisation F = 5.40 x eps (omega_d / omega_b from kd1.json).

## 3. Retention at each v_k in {500, 525, 550, 575, 600, 650} (and 625 reported)

- **Bins** (L388's): 6e13-1e14, 1e14-1.5e14, 1.5e14-2.5e14, >= 2.5e14 in M(<1 Mpc/h); eps_bin(v) = pooled median.
- v_k 575-650: L388's numbers (KA: recomputed from the per-halo JSON, equal to the stored medians to 0).
- v_k 500-550 (not run): **graded central** = per-bin least-squares line in v through L388's four kicks, evaluated at
  v and clipped to [eps(575), eps(0)] (eps(0) = the v_k = 0 MUTATE runs' bin median). **Bracket** = [eps(575), eps(0)]
  (monotone: a smaller kick cannot retain less). A gate cell at 500-550 reads PASS / FAIL only if the central value and
  both bracket ends agree; otherwise NO VERDICT (MIXED).
- **Unit slip in XR13's placement (disclosed; coordinator, from CK3 f3db8c0425):** L388's bins are in Msun/h (box units),
  while XR13 compared X-COP's M(<1 Mpc/h) in Msun (5.0-8.7e14) against them. CK1 places every system unit-consistently:
  M[Msun/h] = M[Msun] x h with h = 0.6736 (XR13's), inside the same 1 Mpc/h = 1484.6 kpc sphere. The bin of every X-COP
  cluster is reported per footing (the masses are footing-free; the bin is the same on both).
- **X-COP**: each cluster gets the bin its unit-consistent M(<1 Mpc/h) falls in (graded). If any cluster lies within
  10 % of a bin edge, or above the most massive L388 halo by more than 10 %, it is graded over the bracket of the two
  adjacent bins (PASS / FAIL only if both agree, else NO VERDICT). Reading: a per-halo log-linear fit eps(log M) over
  L388's halos >= 1e14 Msun/h, evaluated at each cluster, clipped to [0, eps(0)].
- **Groups**: every Lovisari group gets the lowest bin (graded, XR13's assignment). Retention falls with mass in L388, so
  for groups below 6e13 Msun/h this is an UPPER bound on retention: a G3 fail for too little carrier is robust; a fail
  for too much is not, and is then NO VERDICT. CK3's finding (groups effectively NO POWER below L388's lowest node) is
  quoted, not regraded.
- **A new resolution run for 2e13-1e14 Msun/h halos is not feasible here**: an L388-type box (256^3 mesh, 2 x 192^3
  particles) is several GB per process; a smaller mesh would not reproduce L388's bins (its KA). Said, not attempted.

## 4. Galaxies: the resolved release model RM (no box; the law's field; built from on-disk baryons only)

For each galaxy-scale system (SPARC, ellipticals, KiDS lenses, the Milky Way, dSphs) and for X-COP shapes:
- Baryons M_b(<r) from the record's own profiles (SPARC: QX5 rotmod vb2 r/G at the fixed Upsilon, monotone, constant
  beyond r_last; ellipticals: GB1/QX18's Mbar(r); X-COP: QX7 iter_5's baryon profile; MW: Hernquist, M_b = X5's best-cell
  M* 6.02e10 / 5.36e10 Msun, a = 3 (M_b/1e11)^0.3 kpc as L375; dSphs: Plummer with M*/r_h from GB1's feature rows;
  KiDS lenses: Hernquist with the bin's Mb at its R_med as GB1 carries it).
- Parents: carrier mass C_f M_b(<r) distributed like the baryons (KD1's v_k = 0 state exactly), isotropic Gaussian
  velocities from the Jeans equation in the release potential (zero pressure at the outermost baryon radius).
- Trigger: L388's / L365's (shed at halo virialisation): every parent decays once at z_F and its daughter gets an
  isotropic kick v_k. r_F (the release radius reported per system) = the parents' half-mass radius.
- Escape boundary R_out = the radius where the law's mean enclosed dynamical density 3 g/(4 pi G r) falls to the cosmic
  mean matter density at z_F (joining the Hubble flow), with Omega_m = (omega_b + omega_d)/h^2 from kd1.json (QX15 footing
  fit). Retained iff v^2/2 + phi(r) < phi(R_out). v_esc(r) = sqrt(2 [phi(R_out) - phi(r)]).
- **Bracket cells (4):** potential {release: law field of (1 + C_f) M_b; after loss: law field of M_b only} x z_F {0, 2}.
  The retained daughters are orbit-averaged in the same potential (static afterwards: disclosed) to give M_c(<r).
- Per point f(r) = M_c(<r)/M_b(<r). Monte Carlo N = 20000 parents per system, seed 11, deterministic.
- **Cell rule for any RM row:** PASS only if all 4 cells pass; FAIL only if all 4 fail; otherwise NO VERDICT (MIXED).
- L353 reading (not graded): the same with the carrier feeling g_N only (baryons + carrier), release potential, z_F 0.

## 5. The gates (per v_k, per footing; GB1 lines unchanged)

| Row | Built from | PASS line |
|---|---|---|
| G1 SPARC | RM f per point, b = 1 + f | GB1 G1 (\|Z\| <= 0.057, rms <= L0 rms + 0.010) |
| T SPARC tail (coordinator) | RM, galaxies with v_flat >= 250 km/s (v_flat = mean of the three outermost V of QX5's mask) | max f over each galaxy's points <= 0.3257 / 0.1937 (KD1 SPARC cap) in EVERY tail galaxy |
| G2 X-COP | F_i = C_f eps_top(v), shape = the cluster's RM retained shape (normalised at Mb_last's radius, NA2 convention) | GB1 G2 (\|mean\| <= 0.05, rms <= 0.10) on the 35 points; also NA2's bin rule (every bin with n >= 3 within 0.10) reported |
| P X-COP profile vs NA2's band | the RM shape's per-bin residual pattern at the graded amount, and the shape's position between gas and stars | reported per cluster (inner/outer mass ratio M(<0.25 R500)/M(<0.7 R500) of RM shape vs gas, HSE, stars); not a separate label |
| G3 groups | F = C_f eps_low(v), uniform (b = 1 + F) | GB1 G3 (>= 16 / 20, both f* 0 and 1) |
| G4 ellipticals | RM f at 2, 4, 8 Re | GB1 G4 |
| G5 Coma UDGs | own RM term + Coma's carrier (X-COP A1656 graded profile) density at r = 300 kpc times (4/3) pi r_h^3, over M*/2 | GB1 G5 (UA1's NOT A TEST stated alongside) |
| G6 dSph classes | own RM term + host term at D = 50 and 150 kpc (MW RM host for MW classical and bright M31, disclosed); LG field own term only | GB1 G6 (each graded class CI contains 0); D bracket: PASS only if both D pass |
| G7 KiDS split | RM f per KiDS early / late point | GB1 G7 |
| G8 Solar System | carrier density at the Sun from the MW RM inside 9.58 AU, b = 1 + f | GB1 G8 (C6P lines) |
| MW (coordinator) | MW RM | at R0 = 8.122 kpc: Delta K_z/2piG = 2 x 1.1 kpc x rho_c(R0) <= 4.4 Msun/pc^2 (2 sigma of Bovy & Rix 66.4 +- 2.2, X5 D2); Delta v_c(R0) <= 229.053 + 9.290 - v_c(X5 best cell) = 8.633 / 16.023 km/s; inner: max over r <= 30 kpc of Delta log g <= 0.057 dex (L376's RAR line) |
| G9 CMB lensing / growth / forest | not graded here (CK4) | "deferred to CK4" |

- **Residue rows (SE2 / UA1), reported as a second label:** per class the carrier's median F inside SE2's 95 % interval
  (PB3 model U: SPARC, X-COP, groups f* 0 / 1, ellipticals, bright M31; Coma UDGs NOT A TEST per UA1), and the groups'
  median carrier offset (median over the 40 group points of Delta = log10[g_law((1+F) g_N)/g_law(g_N)]) inside UA1's
  95 % step interval [+0.052, +0.459] / [+0.009, +0.415]. Residue label: PASSES RESIDUE at a v_k if every graded residue
  row plus T and MW pass on both footings; otherwise FAILS RESIDUE (rows).
- **Label per v_k:** CANDIDATE (static; G9 with CK4) only if G1-G8, T and MW all PASS on both footings at that v_k.
  Lane label: CANDIDATE if some v_k is; otherwise **FAILS (rows)** with the binding gate = the row that fails at the most
  v_k on both footings (ties: the row nearest X-COP's passing kicks); NO VERDICT if no FAIL but some NO VERDICT, or if
  KA or MUTATE fails.
- **Coordinator rule:** if T or MW fails at a v_k where G2 passes, the label is FAIL and the window is closed from both
  ends (stated as such).
- JSON also carries: for every v_k, the RM retention against v_esc(r_F) per system, plus the single-shell curve
  P(|v_p + v_k n| < v_esc) on a grid of v_esc 100-3000 km/s and sigma = v_esc/sqrt(6) and v_esc/sqrt(3), and L388's
  bin retention against each bin's Newtonian proxy sqrt(2 G M / 1 Mpc/h), so CK3 can interpolate groups.

## 6. Known answers (any KA FAIL: stop, NO VERDICT)

- KA1: L388's pooled bin medians at 575-650 recomputed from its per-halo JSON equal the stored retention_by_mass to 0.
- KA2: L388's top-bin and lowest-bin values reproduce the RESOLUTION's 0.79-0.85 and 0.17-0.34 (rounded).
- KA3: GB1 L0 through CK1's b-candidate with f = 0 equals gb1.json's L0 numbers on G1-G8 (\|d\| <= 1e-9).
- KA4: NA2's X-COP baryon-traced grader at F = KD1's need (4.1786 / 3.7833) gives NA2's -0.0017 / 0.0818 and
  -0.0017 / 0.0835 (1e-3).
- KA5: RM at v_k = 0 returns all parents (f_ret = 1) and f = C_f at every point (1e-6).
- KA6: XR13's X-COP M(<1 Mpc/h) range 5.0e14-8.7e14 Msun reproduced (2 %) before conversion to Msun/h.

## 7. MUTATE (separate *_MUTATE* outputs; must bite, else NO VERDICT)

- M1 v_k = 0: L388's v_k = 0 runs give F = C_f eps(0) within 5 % of 4.111 for the top bin and for the pooled X-COP
  sample (KD1's capture), both footings.
- M2 v_k = 2000 km/s: the graded amount path (section 3 extrapolation, clipped) must empty X-COP: F <= 0.1 C_f in every
  cluster and G2 FAILS on both footings. The RM's own X-COP retention at 2000 is reported (a physical reading; it may
  not empty, and that is said).
- M3 RM with the kick off (v_k = 0) must FAIL T on both footings (the tail row can see a retained carrier).

## 8. Expected outcome, written before any number

FAILS (rows). Galaxy rows fail in the law's field: a log-like potential out to the Hubble-flow radius gives escape speeds
of several hundred to ~1000 km/s even in L* galaxies, so a 500-650 km/s kick leaves much of C_f in SPARC's high-mass tail
and the Milky Way (T, MW, likely G1) at every v_k, unlike L376's Newtonian-only shells, where galaxies were cleared. G4,
G5, G6 and G7 likely FAIL as for the plain law (hosts' carrier does not reach UDGs, dSphs or the colour split). X-COP:
at C_f eps_top = 3.2-3.5 against the uniform need 4.18 / 3.78, G2 is marginal (likelier to pass on alt than canonical),
and the 500-550 cells may be MIXED. Groups G3 FAIL (strict 16/20 with f* 0 needing 3.46). Binding gate expected: T / MW
(the coordinator's rule then closes the window from both ends). An RM reading that keeps galaxies clear would contradict
this expectation and will be reported as such.

Kappa = 1/2 FITTED; not theory closed.
