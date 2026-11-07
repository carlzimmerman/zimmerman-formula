# EW2: AeST (v4) on the web, in hot wells and in discs. NO-GO FOR THE CLASS: one length 1/mu cannot keep KiDS hosts (mu <= 0.063 Mpc^-1) and the lensing web (mu >= 10 Mpc^-1) at once; clusters FAIL; statics PASS at host-compatible mu

Kappa = 1/2 FITTED; not theory closed. Adopts nothing; the owner adopts. TEST lane under the owner's 11-07 instruction
("we need to get all actions that work everywhere"), which overrides DIRECTION_2026_11_07's STOP list for this lane.
SWARM_BRIEF rules bind. No particle (the AeST dust is the action's own scalar), no LCDM input, footings canonical
9.3603e-11 / alt 1.1312e-10 m/s^2 graded separately, never pooled. Not blind: the record's AeST lanes were read first.

- Criteria: `FROZEN_CRITERIA.md` + `iter_*/FROZEN_CRITERIA.md`, committed and pushed alone before any script or number
  (local 869b3d72ad, origin 041be83e4a).
- Scripts: `ew2_lib.py` (H2's exact spherical static solver, adaptive in mu r; SV5's web projection with AeST's switch),
  `ew2_iter2.py`, `ew2_iter3.py`, `ew2_iter4.py`, each with `--mutate` where frozen. One thread, nice 15: 74 s, 725 s, ~3 min.
- Lean: `fable_independent_2026/lean_2026/EW2_aest_window.lean` (4 theorems, 0 sorry, axioms propext / Classical.choice /
  Quot.sound; `.out` saved) and `EW2_aest_window_MUTATE.lean` (3 false claims, all rejected, `.out` saved). Compiled with
  `lake env lean` from the "new_physics copy" checkout.

## 1. The form graded (iter_1)

v4 = Skordis-Zlosnik AeST (arXiv:2007.00082 eq. 5, record transcription C1 / I1) + C1's capped free function
Jcal(Y) = 2 a0^2 [-y - ln(1-y) - y^2/2] (static limit = the canonical law exactly; lambda_s -> infinity) + K(Q) = -2 Lambda
+ K2 (Q - Q0)^2 (the dust-like part; mu^2 = 2 K2 Q0^2/(2 - K_B)) + the v3s stiffness gamma_L (screens the Sun; C1: AeST
alone has none). Free constants: mu, I0 (dust charge, an initial datum), the zero point Delta, K_B <= 0.078, L* (FITTED).
Static equations (H2's exact spherical form): lap Phi~ + mu^2 Phi = 4 pi G rho_b, div[Jcal' grad chi] = lap Phi~,
Phi = Phi~ + chi = Psi. On FRW, Jcal drops out at linear order; the scalar is dust for comoving k < a mu and sits in the
Jeans-type band above it.
KA1: C1's sympy script replayed from a scratch copy, 8/8 PASS (`iter_1_action_statement/ew2_c1_replay.out`); its MUTATE
4/8 (bites).

## 2. Labels

| Gate | Label | Key numbers (canonical / alt) |
|---|---|---|
| SV5 lensing amplitude W1 (line \|r-1\| <= 0.072) | PASS only for mu >= 10 Mpc^-1 | r = 1.037 / 1.045 at mu 10; 1.42 / 1.53 at 6.3; 59-92 at mu <= 3 (law on the band's modes); r = 1 at mu >= 15.8 |
| W2 shape (dchi2 <= 4) | PASS only for mu >= 10 | 0.93 / 1.99 at mu 10; 139 / 180 at 6.3 |
| KiDS G6 (QX10 line 0.05 dex) | PASS only for mu <= 0.063 (Delta = 0); <= 0.1 with a free universal Delta (canonical -1.25 to -0.5, alt -1.0 to -0.75) | at mu >= 0.1 the static mass term turns the pull negative inside the KiDS range (first g <= 0 at 1.3-2.3 Mpc for log Mb 9.4-10.9 at mu 0.1); G6 -0.16 / -0.16 at mu 10 |
| Web + KiDS together | **NO-GO FOR CLASS A_mu** | mu_w = 10, mu_h = 0.063 Mpc^-1 on both footings (gap x160; x100 with the Delta envelope); Lean `window_empty` |
| QX15 primary CMB | FAIL [C7 read, not rerun] | v4 runs away at linear order (C7 patched CLASS). Band edge at z* for host members: k_sw <= 6e-5 Mpc^-1, all acoustic modes in the band |
| Dust amount (I0) | NOT EVALUABLE as a prediction | initial datum (C2 K2): W1 grades the gain only, with SV5's target amount put in by hand |
| X-COP (QX10: \|mean\| <= 0.05, rms <= 0.10) | FAIL at every computed mu (Delta = 0 and every Delta in [-8, 2]) | static dust <= 0.03 M_b at mu <= 0.1 (0.001 at 0.0156, 0.024 / 0.025 at 0.1) vs need 2.39 / 2.07 M_b at the last X-COP point; X mean +0.467 / +0.434 at mu 0.0156, best +0.089 at mu 56.6 (alt) with M <= 0 somewhere |
| Groups (QX10 strict, >= 16 of 20 at fst 0 and 1) | FAIL at every computed mu | at most 1 group passes |
| Beyond hydrostatic, gate DB (mu R >= 1 on >= 90 % of X-COP points at host-compatible mu) | FAIL | 0 % at every host member (X-COP r 0.12-1.0 Mpc against 1/mu >= 16 Mpc) |
| Past the fold | NOT EVALUABLE | the single-valued field ends (AN1 v3, AN2; X14: a completion costs a constant) |
| SPARC (rms shift <= 0.096, \|mean\| <= 0.05) | PASS for mu <= 10; FAIL at 56.6 and above | rms <= 1e-4 dex at host members; 0.016 at mu 10; 0.076 with 171 points g <= 0 at 56.6; bound at 1.24e8 |
| Cassini / Solar System | PASS for mu <= 56.6 (v3s part: C6P, read); FAIL at 2.04e4 and 1.24e8 | mass term's anomaly at Saturn 4e-26-2e-20 m/s^2 for mu <= 10; 7.5e-14 at 2.04e4 against 7.0e-15 |
| c_T | PASS [read] | tensor modes couple only through R; c_T = c |
| Galaxy lensing = dynamics | PASS | Psi = Phi (iter_1 KA1); KiDS amplitude is G6 above |
| Health (not a gate here) | FAIL [I1 read] | v4 is Hadamard ill-posed where the aether twists (every disc galaxy, the Sun in the Galaxy) |

## 3. What it means

1. **The AeST switch is a length, and the gates want opposite lengths.** The scalar is dust only above 1/mu. The
   lensing web needs every lensing-weighted mode in the dust branch (any band mode carries the law's 40-90x gain): mu
   >= 10 Mpc^-1, 1/mu <= 100 kpc. KiDS hosts need the static mass term negligible out to 3 Mpc: mu <= 0.063 Mpc^-1,
   1/mu >= 16 Mpc. The same scale also decides clusters: a hot well can condense dust only inside the dust branch's
   reach, so X-COP needs 1/mu below ~0.1-1 Mpc, i.e. on the web's side, which KiDS forbids. That is DX1's lesson again
   in AeST's own variable: one scale cannot carry it.
2. **Hydrostatic dust is depth-keyed but far too small where hosts allow it.** delta rho = -mu^2 Phi/(4 pi G) does grow
   with depth, so it is larger in clusters than in discs, as the owner's question hoped. At mu <= 0.063 it is <= 3 % of
   the baryons inside the X-COP radii, against a need of 2.1-2.4 x. Where it reaches the need (mu ~ 56.6) its sign
   oscillates (M <= 0 inside some clusters), SPARC fails and KiDS fails.
3. **What SZ21's CMB fit uses is not v4.** SZ21 fit the CMB with finite lambda_s and K_B up to 0.5. H1 shows that loses
   the canonical law on SPARC once BBN's lambda_s >= 24.7 is imposed, and C7 finds v4 (lambda_s infinite, small K_B) runs
   away at linear order. So "AeST fits the CMB" and "AeST carries the canonical law" are different members.

## 4. Checks and MUTATEs

| Id | Result |
|---|---|
| iter_2 KA1 (mu 1e12, all dust) | r = 1, dchi2 = 0 to 1e-8: PASS |
| iter_2 KA2 (mu 1e-8, all band) | r = 74.74 / 89.36 = SV5 iter_1 exactly: PASS |
| iter_2 KA3 (H2 galaxy guard) | +0.0900, -0.1635, -1.7488 at H2's node 1.0037 Mpc (H2: +0.090, -0.163, -1.749); max200 0.0027 / 0.0165 / 0.0856: PASS |
| iter_2 KA4 (mu 1e-6) | G6 -4.9e-7: PASS |
| iter_2 KA5 (step halving) | mu 0.3: identical; **mu 10: -0.1644 vs -0.1778, FAIL** (line 1e-3). The mean drops LE points where g <= 0, and that set moves with the step. Both values are > 3x the 0.05 line and g <= 0 at LE radii in both, so no label moves |
| iter_2 MUTATE (K2 -> 0) | W1 fails at every member (r = 74.74 / 89.36), G6 = 0: bites |
| iter_3 KA1 (mu 1e-6) | X 0.467524 / 0.434548 vs QX20 0.467499 / 0.434523; groups 0.358645 / 0.320275 vs 0.358644 / 0.320274: PASS |
| iter_3 KA2 (dust bookkeeping) | rel 4.6e-10: PASS |
| iter_3 M1 (K2 -> 0) | X back to the plain law (+0.4675 / +0.4345); moves D by up to 0.25 dex: bites |
| iter_3 M2 (positive control) | X gate PASS (mean -5.8e-4 / -7.6e-4). The frozen parenthetical "|mean D| <= 1e-6" is NOT met: interpolation floor. A first M2 run applied the AeST mass term on top of the needed mass (not the frozen control); kept as `ew2_iter3_MUTATE_firstrun_M2_with_mass_term.out` |
| iter_4 KA1 (mu 1e-6 SPARC) | **rms 1.23e-4, FAIL** (line 1e-4). Post-result diagnostic: 3.1e-5 at a quarter of the step, so it is the interpolation of g between solver nodes; 3 orders below the SPARC line, no label moves |
| iter_4 KA2 (Sun's static dust) | rel 1.7e-4: PASS |
| iter_4 MUTATE (drop gamma_L) | AX1 engine, class AeST, from a scratch copy: output identical to the record, Q2/Hees 2.44-5.15: Cassini FAIL: bites |
| Lean | 4 theorems compiled, 0 sorry, standard axioms; MUTATE twin 3/3 rejected |

## 5. The bound H-inf (derived here; used only for hosts at mu > 1e3 and for SPARC at mu 1.24e8)

Spherical static form, M_b constant on [R/2, R]. Suppose |g/g_law - 1| <= eps there. g_AQUAL is monotone in |M_eff| with
g proportional to M_eff^(1/2 to 1), so |M_eff/M_b - 1| <= delta = 2 eps + eps^2, hence the extra mass
D = M_eff - M_b = -(mu^2/G) Int Phi r^2 changes by at most 2 delta M_b between any two points of the interval. Phi' = g >=
(1 - eps) G M_b/R^2 = s, so Phi is increasing and crosses zero at most once, at r0; one side of r0 inside [R/2, R] has
length >= R/4, on which |Phi(r)| >= s |r - r0|, so (mu^2/G) Int |Phi| r^2 >= (mu^2/G)(R^2/4) s (R/4)^2/2. Requiring this to
be <= 4 delta M_b gives (mu R)^2 <= 512 delta/(1 - eps). At eps = 10^0.05 - 1: mu R <= 12.3. Not Lean-certified (an
integral bound); it is used only where the solver cannot run and each use is labelled "[bound]".

## 6. Not done / limits

- QX15 not rerun: it needs C7's patched CLASS; graded by C7's computed result. The amount I0 is not predicted.
- The band's response is given the law's nonlinear B_W (generous); C7's linear runaway would be worse.
- Past the fold nothing is computed (no completion in the action). Gate DB is a reach argument from the linear dust
  branch plus AN1 v3's reduced-system reads, not a 3D collapse in a measured well.
- c_T is graded by reading the action, not by a computation.
- KiDS lenses are Hernquist (a_h 3 kpc) at the four Brouwer+21 bin masses; Delta = 0 is VSZ's fiducial, the envelope
  is reported only.
- Two frozen known answers missed (iter_2 KA5 at mu 10, iter_4 KA1) and the M2 parenthetical; all stated above, none
  moves a label.
