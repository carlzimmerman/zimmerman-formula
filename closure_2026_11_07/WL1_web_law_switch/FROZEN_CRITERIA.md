# WL1 frozen criteria: the law's phantom keyed on khronon multi-streaming (SV5's untested two-switch escape, arm (i))

Frozen before any WL1 script or WL1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane: the
key below is NOT in v3s or AC2q; it is graded as a candidate law switch, nothing more. No particle, no LCDM input. Both
footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2), graded separately, never pooled. One thread, nice'd, under
1 GB, minutes; preemptible (no long job). No new data, no downloads.

## 0. The question and the record it rests on

SV5 (79a75ab40d) conclusion 4: the CMB wall is the a0 law acting on the linear web (lensing amplitude r = 74.7 / 89.4
against 1 +- 0.072). An escape needs two switches: (i) the law's phantom OFF on the linear web while ON in galaxies out to
KiDS's 3 Mpc, then (ii) the K(Q) dust's Jeans scale switched by the AC2q charge (hosts Sigma_* 8.0 / 6.0 rho_DE vs a
law-off web <= 2 rho_DE). OQ1 (048386c5fb) / OQ2 (7ab1a3edb7): the web needs F_web <= 0.005. WG6's by-hand Yukawa
screening is the record's only try at (i).

**Candidate key for (i), K_ms:** the law's phantom multiplier F = 1 where the khronon flow is multi-streamed (the
khronon label map has folded: J has changed sign, i.e. more than one leaf through the point; AC14/FS2 compute this J),
F = 0 where it is single-stream. The linear web is single-stream by definition of "linear", so (i)'s web side is
built in; the question is the host side.

## 1. Why K_ms is not already dead (checked before freezing)

- **SEED_2026_11_06.md dead keys** (p/rho, gas T, virial T, virial heating, khronon velocity, enclosed density, gas-g,
  clock depth, kinematic support, cold gas, morphology, environment / external field) and DIRECTION 11-07's STOP item
  are all keys for the DISC-vs-HOT split inside collapsed hosts. K_ms does not split discs from hot systems (both are
  multi-streamed); it splits collapsed hosts from the linear web, the split SV5 conclusion 4 asks for. "Khronon
  velocity" (dead) is the magnitude of the khronon frame's motion, not the stream count. "Environment / external
  field" (QX24, EV1) is the EFE magnitude; K_ms is a topological count of the flow.
- **DX1 D4 (history, DEAD):** D4 kills removing a COLD COMPONENT from discs by formation history (contraction has the
  wrong sign, feedback expulsion needs 5-23 % of SN energy with inverted ordering, capture at turnaround is
  history-blind). K_ms acts on the law's phantom, not on a component, and is a present-state variable (the current
  stream count), not an assembly record. D4's sign and energy arguments do not apply to it. GB1 carries no history
  feature; K_ms needs none for the gates below (it needs r and the host's turnaround, both derivable).
- **OUTER_EDGE_CHECK 11-07:** the action's own switch (D.P sign / Sigma) has no edge for an isolated galaxy. K_ms is
  an ADDED switch, so it is not excluded by that check; it is graded here as such and adopted by nobody.
- So K_ms is not in the dead list. It is graded below; it is stated in advance that the likely kill is KiDS.

## 2. The shell-crossing radius R_ms(M), frozen (the action's own spherical collapse, no LCDM input)

A shell can only have crossed another shell after it has turned around (pressureless spherical flow keeps its shell
order until the first infalling shell meets a re-expanding inner one). So the multi-streamed region around an isolated
host lies inside the radius of the shell turning around today: **R_ms <= r_ta(t0)**. The splashback radius is smaller
still; WL1 grades the most generous admissible value, R_ms = r_ta(t0) (the khronon's own pressure scale is
Hubble-sized, AC14, so on galaxy-to-Mpc scales its labels are carried by the same converging flow and fold no
farther out than the matter does).

r_ta(M) from the shell equation in physical radius r(t), the action's static law applied to the peculiar field (SV5
iter_1's reading: QUMOND on the peculiar field):

  d^2r/dt^2 = -(4 pi G/3) (rho_m(t) + 2 rho_r(t) - 2 rho_DE) r - g_law(G dM / r^2),
  g_law(g) = g/2 + sqrt(g^2/4 + a0 g),

background = QX3's framework-native corner as QX7 iter_4 / QX10 iter_2 load it (omega_b 0.0215, omega_d 0.11958060,
H0 65, flat, rho_DE constant, radiation omega_r 4.15e-5 photons + neutrinos), start z_i = 1000 on the unperturbed
Hubble flow (r_i = Lagrangian radius x a_i, dr/dt = H_i r_i), dM a point excess present from z_i (generous: in reality
the excess grows from ~0). Bisection on the Lagrangian radius for the shell with dr/dt = 0 at t0 (z = 0); r_ta is its
radius then. Today's r_ta is used for every lens (generous: KiDS lenses sit at z_l ~ 0.1-0.5, where r_ta is smaller).

- **Graded (ceiling) R_ms^C:** dM = M_b (1 + R), R = omega_d / omega_b (the cold component counted as extra excess,
  most generous), and R_ms^C = max(that law-on r_ta, QX10 iter_2's r_ta rule M_b(1+R) / (5.55 rho_m0)).
- **Lower reading R_ms^L:** dM = M_b only, law on (no dust), r_ta from the same equation. (Still >= splashback.)
- Monotone: the KiDS shift below can only move toward 0 as R_ms grows (more phantom kept), so the ceiling failing is a
  fail for every admissible R_ms.

## 3. Gates, in order (the first FAIL sets the label; later stages are reported NOT REACHED and not computed)

**Stage 1, arm (i) host side.**
- **K-G6 (graded kill gate): KiDS isolated-galaxy lensing, Brouwer+2021 Fig. 9, 59 points (QX5's lensing() loader,
  4 mass bins M_b 10^9.4, 10^10.45, 10^10.7, 10^10.9, each lens a point mass, R = sqrt(G M_b / g_bar) as the record
  does).** Line: |mean log10(g_key / g_base)| <= 0.05 dex (QX7 iter_4/5's G6 line, QX5's lensing recheck), both
  footings.
  - g is computed in the convention KiDS measures, g = 4 G DeltaSigma(R) (Brouwer's conversion, exact for an SIS),
    from the 3D effective mass M_eff(r) = r^2 g_law(G M_b / r^2) / G. Base: phantom to infinity. Key: phantom density
    kept for r <= R_ms, zero outside (the phantom mass inside R_ms is retained; generous: in projection it keeps
    lensing beyond R_ms).
  - Reported, not graded: the pointwise reading g_key = G (M_b + M_ph(<min(r, R_ms))) / r^2 against g_law(G M_b/r^2).
  - Reading: FAIL if the ceiling R_ms^C fails on either footing; PASS if the lower reading R_ms^L passes on both;
    NO VERDICT (bracket [R_ms^L, R_ms^C]) otherwise.
- **GB1 G1-G8 (read-only battery, criteria e9464bc8ce, executed from gb1.py's source up to its main block):** the
  candidate is GB1's (b = 1, F, T = 0) with F = 1 if r <= R_ms^C(M) else 0, M = g_N r^2 / G at the point (the
  enclosed baryons, as the battery's features carry them). Line: every row's status equals L0's status on both
  footings (L0: PASS G1, G8; FAIL G2-G7). A row that goes from PASS to FAIL is a FAIL of this stage; G7's numbers are
  reported. (Hosts' radii lie far inside R_ms for every class but KiDS, so the rows are expected to equal L0; the
  script prints max r / R_ms per class.)

**Stage 2, arm (i) web side** (only if stage 1 passes): SV5 iter_1's web amplitude r <= 1.072 with F = 1 on the
multi-streamed cells of SV5's own field (Zel'dovich criterion: largest deformation eigenvalue D lambda_1 >= 1), and
the multi-streamed mass fraction F_web <= 0.005 (OQ1/OQ2 row), every z of SV5's grid, both footings.

**Stage 3, arm (ii)** (only if stage 2 passes): SV5 iter_2's C2-C4 on the law-off web (C2: web cells above Sigma_*
<= 3.6 % mass-weighted; C3: G5/G6/G7 by QX10's convention; C4: stiff Sun).

**Stage 4** (only if stage 3 passes): QX3's PR4 lensing shape chi^2 <= 18.5 with both arms on.

## 4. Known answers (must replay before any grade; else stop, nothing graded)

- KA-SV5: sv5_iter1.json proj r = 74.7424 (canonical) and the alt value (89.4 to the quoted rounding); sv5_iter2.json
  Sigma_*/rho_DE = 7.969 / 5.998. Read exactly, |d| = 0 against the JSON.
- KA-GB1: the rebuilt battery's L0 class means equal gb1.json's KA1 values to 1e-9 on both footings, and L0's row
  statuses equal gb1.json's.
- KA-K: the pointwise baseline mean log10(g_obs / g_law) over the 59 KiDS points equals QX7 iter_4's BASE L
  (0.141707 canonical / 0.101597 alt) to 1e-9.
- KA-P: the projected base for a pure deep-MOND point mass reproduces g_law at x << 1 to 1 % (4 G DeltaSigma = sqrt(G M a0)/R
  for an SIS) - a check of the projection code.
- KA-T: r_ta with a0 -> 0 (Newton) for the QX10 mass excess lies within 20 % of QX10's 5.55 rho_m0 rule at
  M_b = 1e11 (the shell code reproduces the record's Newtonian turnaround scale; reported if outside, and then the
  ceiling still takes the max).

## 5. MUTATE (each must bite)

- M-ON: switch always on (R_ms = infinity): K-G6 shift = 0 exactly (PASS), GB1 rows = L0, and the web arm's amplitude is
  SV5 iter_1's own 74.7 / 89.4 (identity: the candidate IS the law on the web; read from sv5_iter1.json). Bites if the
  graded key's K-G6 shift differs from 0 by more than 1e-6.
- M-OFF: switch always off (R_ms = 0): GB1 G1 SPARC must FAIL on both footings (it is GB1's Newton MUTATE), and K-G6
  must FAIL.
- M-R: R_ms x 100 must move the K-G6 shift toward 0 (monotone check).

## 6. Labels

- **PASS (both walls' CMB arm):** stages 1-4 pass on both footings. (Would still adopt nothing.)
- **FAIL (row named):** the first failing row, with its numbers on both footings and margins read from the JSON.
- **NO VERDICT (bracket):** stage 1's K-G6 between the lower and ceiling readings, or a later stage not computable;
  the bracket is stated.

Outputs: wl1.py -> wl1.json / wl1.out; wl1.py --mutate -> wl1_MUTATE.json / .out; RESULT.md. One row in
closure_2026_11_06/CLOSURE_FINAL.md. Kappa = 1/2 FITTED; not theory closed.
