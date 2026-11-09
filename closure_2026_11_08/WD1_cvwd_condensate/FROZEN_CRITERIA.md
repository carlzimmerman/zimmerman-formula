# WD1 frozen criteria: outside proposal, a merger-decohered condensate supplement with a 1.6 Mpc Thomas-Fermi core

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing; the
owner adopts. No dark-matter particle is adopted: the proposal's component is graded as a declared supplementary component
under the record's gates, exactly as PJ1 (e3c9bc7d3c) and BG1 (d5b23bf2d4) were. TEST lane, quarantined (owner decision
closure_2026_11_08/OWNER_DECISION_2026-11-08_WD1_LAUNCH.md). Both footings (canonical a0 1.2e-10 / alt 1.1e-10 as the
record's lanes define them) graded separately, never pooled. Outside text and code are reference only, in the untracked
folder `_external_data/wd1_proposal/`; nothing from it is committed or executed from inside it; the lane writes its own
implementation and uses the proposal's printed self-test numbers as known answers (numbers, not text).

## Mechanism under test (in the record's words)

A pressureless component of cosmic amount f M_b with f = 4.40, clustering like cold dust before first shell-crossing
(linear theory and the CMB unchanged from a cold component of that amount), which after shell-crossing acquires an n^2
polytropic pressure that puffs it into a Thomas-Fermi core of radius R_c0 = 1.60 Mpc around every collisionless baryonic
centroid, enclosed mass M(<r) = f M_b r^3/(r^2 + R_c^2)^(3/2). Mergers lower the core radius through a "decoherence"
scalar s driven by the tidal (Weyl) tensor's lag behind its relaxed value: in the quasistatic form W_lag(r) = 16 mu^2
(d^2/(r^2 + d^2))^2, s(r) = 2.0 N W_lag^2/(W_lag + 0.020), R_c(r) = R_c0 e^(-s/2), with per-system inputs N (number of
major mergers), d (progenitor separation), mu (reduced mass ratio, 0.25 default); in the dynamic form s is integrated
along tracers through a two-halo inspiral (the proposal's integrator). Satellites keep only min[1, (v_esc/sigma_host)^3]
of their share. The total source (baryons + component) is then run through the law with the external field.

Declared constants: f 4.40, R_c0 1.60 Mpc, W_crit 0.020, gamma 2.0, Omega_crit (inert inside halos, exact zero in linear
theory). Declared per-class inputs (the proposal's own table): isolated spirals N 0; isolated ellipticals N 1, d 35 kpc;
groups N 4 (4.5), d 400 (420) kpc; clusters N 6, d 600 kpc; Bullet main/sub N 6/5, d 600/500 kpc. These per-class inputs
are the proposal's free choices; the lane grades them as written (primary) and, as the derived bracket, the proposal's own
dynamic integrator with ONE merger event per system and d_sep0 = the system's R500 (groups, clusters) or 40 kpc (ellipticals),
mass ratio 3:2. No other values are scanned.

Law: the adopted law g = (g_N + sqrt(g_N^2 + 4 a0 g_N))/2 on the total Newtonian source, with the record's external-field
treatment (as the record's lanes). The proposal's own interpolation nu(y) = 1/(1 - e^(-sqrt y)) and its EFE prescription
are run as a reported bracket, never graded.

## Gates (the record's, as PJ1 G1-G10, with the component from the mechanism above)

- G1 SPARC (as BG1/PJ1 G1): rms not above law-only + 0.010 dex, |mean| <= 0.05, with each galaxy's component at N 0
  (field spirals) inside its last measured radius; G1b massive tail v_flat >= 250 km/s alone; G1c AGC 114905 and Malin 1
  reported (the proposal concedes AGC 114905 at i 32 deg).
- G2 KiDS isolated lenses (Brouwer 2021, 59 points; QX7 iter_4 FROZEN_CRITERIA.md:26): |shift| <= 0.05 dex in every
  g_bar bin INCLUDING the outermost bins (0.3-1.5 Mpc, and the points beyond where the data reach), stacked with the
  lenses' own depths, with the lenses' components at N 0 (the isolated selection) and, as a bracket, at the ETG values.
  Hand estimate frozen: the 1.6 Mpc puffball holds 0.12 M_b inside 500 kpc but 0.65 M_b inside 1 Mpc and 1.9 M_b inside
  1.5 Mpc, so the outer bins should fail by 0.2-0.4 dex.
- G3 X-COP (|mean| <= 0.05, rms <= 0.10 over 50 kpc-r500 with the amount AS GIVEN by the mechanism, f and R_c(r) from the
  declared cluster inputs, no fitted amplitude) AND the per-bin shape gate of NA2 (d) (bins r/R500 0-0.25, 0.25-0.5,
  0.5-0.75, every graded bin within 0.10 dex of 0). Hand estimate: R_c ~ 65 kpc puts 2.6 M_b inside 100 kpc and nearly all
  4.4 M_b inside 500 kpc, more concentrated than the stars-traced shape NA2 already failed; expect the inner bin < -0.2 dex.
- G4 Groups (Lovisari 20): >= 16/20 in the need band at the declared group inputs (one N, one d for the class).
- G5 Coma UDGs (EV1 gate): within 2 sigma of the need, with each UDG's component at the satellite capture factor
  min[1, (v_esc/sigma_host)^3] (v_esc from its own baryons, sigma_host Coma's 1000 km/s) and Coma's own component (declared
  cluster inputs) in the external field. Hand estimate: capture ~1e-5, the UDGs get nothing, the shortfall stays ~+1.1 dex.
  G5b MW classical and M31 dSphs (X1 rows) reported the same way.
- G6 Bullet (DB1 machinery): two readings, both reported, the label resting on (b): (a) the proposal's centering rule as
  asserted (component on the galaxies by fiat); (b) the component as its own equation of state makes it: an n^2 polytrope
  with c_max 750 km/s meeting a 4,700 km/s encounter is a Mach ~6 fluid, so it shocks and lags with the gas; graded with
  the record's gas-traced Bullet treatment. The lensing peak must sit within the offset band on the galaxies' side.
- G7 Primary CMB (F1A machinery, PJ1's pj1_cmb.py grid at constant weight): a fully clustered cold component of amount
  f = 4.40 x omega_b on each footing's background; Delta chi^2 vs the F1A best constant-weight fit <= 10 on raw Planck
  TT/TE/EE bandpowers to ell 2500, before and after the 5-parameter refit. (The record's F1 need is 5.41 x on canonical.)
- G8 Growth and lensing: raw fsigma8 within 2 sigma (passes by construction before shell-crossing; stated); raw PR4 CMB
  lensing Delta chi^2 <= 4 with the post-shell-crossing suppression: every collapsed halo's component sits in a core of
  R_c0 = 1.6 Mpc physical (field halos, N 0 by the proposal's own rule), entered as a halo-model one-halo suppression of
  the nonlinear matter power on the record's lensing kernel (WG machinery); NOT EVALUABLE with the missing piece named if
  the kernel cannot take a halo-model term.
- G9 Forest (NC2 gate, PJ1's pj1_web.py): the component's post-shell-crossing pressure is a Jeans-type suppression with
  the Thomas-Fermi scale 1.6 Mpc PHYSICAL from the first shell-crossing of minihalos (z 10-20) onward; the Ly-alpha P1D at
  z 2-4 must sit within the NC2 band. Hand estimate: a 1.6 Mpc physical core at z 3 erases power at k > ~0.5 h/Mpc; FAIL.
- G10 Solar System / Cassini (KT16 gate) with the MW's component (N 0 for the MW, or N 1 d 35 kpc as a bracket) at the
  Sun's radius: M(<8.2 kpc) = 4.4 M_b (8.2/1600)^3, state it; and c_T = 1 (a dust component; state it).

## Label rule
PASS on a footing iff the as-written declared inputs pass G1-G10. FAIL iff they do not. The derived bracket (dynamic
integrator, one event, d_sep0 = R500) is reported beside every gate; it cannot turn a FAIL into a PASS (it is not the
proposal as written) but a PASS of the bracket where the as-written fails is written into RESULT.md. NO VERDICT only for a
NOT EVALUABLE gate named by its missing framework-native input.

## Known answers (own implementation must reproduce the proposal's printed self-tests; numbers only)
- KA1: at r 500 kpc, M_b 1.2e11, N 0: component 0.12 M_b (0.117), and with the proposal's own nu a shift of +0.025 dex;
  with the adopted law the shift is reported. KA2: group proxy r 200 kpc, M_b 1.5e12, N 4.5, d 420 kpc: R_c <= 150 kpc and
  component/M_b >= 3.0 (the proposal prints ~3.8). KA3: the dynamic integrator rebuilt from its equations gives, for the
  proposal's Case A (6e10 + 6e10, d_sep0 40 kpc, v 220, 1200 Myr, dt 2) s(300 kpc) within [0.005, 0.02] and for Case B
  (1.2e13 + 8e12, d_sep0 450 kpc, v 650, 2500 Myr, dt 4) s(200 kpc) within [4.5, 6.5]; if the rebuilt integrator does
  not reproduce these, the mismatch is printed and the quasistatic form is graded alone (stated). KA4: f -> 0 reproduces
  the record's law-only numbers on G1, G2, G3, G4, G5 to 1e-6 (the record's own values from BG1/PJ1 outputs). KA5: the
  F1A constant-weight CMB chi^2 at the record's own cold amount reproduces F1A's value (PJ1 KA_C1).

## MUTATE (must bite; separate *_MUTATE.json)
- M1 R_c0 -> 50 kpc for every system (no puffing): G1/G2 must FAIL hard (every isolated galaxy carries 4.4 M_b inside
  300 kpc). M2 W_crit -> infinity (no decoherence anywhere): G3 and G4 must FAIL (clusters keep the 1.6 Mpc core, nothing
  inside R500). M3 f -> 0: every hot gate must read the record's law-only FAIL and every galaxy gate the record's law-only
  PASS (KA4 replay). Criteria hash in every output.

## Operational
Preemptible (checkpoint per gate; CMB and Bullet children as PJ1 ran them, peak RSS recorded; the DB1 Bullet child's 1.39 GB
and the F1A CMB child's ~1.0 GB are the record's existing machinery and are allowed, everything else under 1 GB), one
process at a time per child, nice 10. Check `df -h` before each child; stop under 2 GiB free and message the orchestrator.
No edits to other lanes' files; PJ1's pj1_cmb.py / pj1_web.py / pj1_bullet.py are exec'd from source or imported read-only.
Outputs under this directory: wd1.py, wd1_cmb.py (if a wrapper is needed), wd1_grade.py, wd1.json, wd1.out,
wd1_MUTATE.json/.out, parts/, RESULT.md (label per footing, every gate's number and the bracket beside it, G6 (a) and (b),
hand estimates HIT/MISS, disclosures). Explicit-path commits; push via a temp detached worktree of origin/main. Message
"Theory completion": "WD1 RESULT: <label can / alt> (criteria <hash>, result <origin hash>)".
