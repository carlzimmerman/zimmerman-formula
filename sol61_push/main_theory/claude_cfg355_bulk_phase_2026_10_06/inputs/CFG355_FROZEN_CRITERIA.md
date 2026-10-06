# CFG355 FROZEN CRITERIA: tidal rule T1 with a cold-rank veto (f = T1 AND NOT rank sigma_c == 2)

Frozen before any script. kappa = 1/2 fixed (fitted); nu_mono; no DM particle (the cold MASS is still required).
Owner decision 2026-10-06: the switch may read the cold component (MS1 relaxed). Under the original MS1 this reader is
NOT ADMISSIBLE. Owner goal: "find a switch that does both".

## 1. Object
- T1 (CFG354, unchanged): psi = Phi_d/(4 pi G rho_bar), t = Hessian psi, l1 >= l2 >= l3, tau = (Delta_ta - 1)/3,
  T1 ON iff l2 >= tau. Delta_ta from CFG354's shell ODE.
- Rank (CFG351, unchanged): sigma_c = sum_s w_s (v_s - vbar)(v_s - vbar)^T, fine-grained stream sum; numerical rank
  with CFG351's tolerance. Single stream: rank 0. N streams: rank <= N - 1.
- **Combined rule:** f = H(l2 - tau) * V, V = 1 - [rank sigma_c == 2]. Equivalent state-function form
  V = 1 - H(e2(sigma_c)) (1 - H(det sigma_c)), e2 = sum of principal 2x2 minors (PSD: rank >= 2 iff e2 > 0).
- Width: T1 needs a width for well-posedness (CFG354: eps_min = c_d Delta/6 = 0.077, edge smearing <= 1.6% r_ta).
  Derivation attempt (scored as the constant count):
  - Candidate W0: a self-generated width eps = l1 - l2 (the tidal split; no number other than a unit coefficient,
    declared a convention). It counts as 0 constants iff eps_self >= c_d Delta/6 at EVERY sampled edge point
    (24 hosts x CFG354's c_d samples) AND there is no analytic obstruction. Known risk before any number: l1 = l2 on
    the edge surface at the normals of the circular sections of the external tide (codimension 2, isolated points),
    where eps_self = 0 while c_d need not vanish.
  - Framework scales: a0 gives per-system lengths (not a dimensionless tidal width); xi (chassis heat filter) has no
    fixed value in the record. These count only if they fix eps with no new number.
  - Otherwise n = 1 (eps_min as in CFG354).
- **Rank model for hosts (scored) = CFG351's self-similar model:** caustics lam1 = 0.359 r_ta (first), lam2 = 0.232
  r_ta (second), from cfg351_threeaxis_switch_results.json. r < lam2: >= 5 streams, rank 3. lam2 < r < lam1:
  3 streams, rank <= 2; GENERIC (non-collinear stream velocities, as with CFG351's angular-momentum regulator) rank = 2.
  r > lam1: single-stream infall, rank 0.
  - Known before any number: under the generic assignment the 3-stream shell lam2 < r < lam1 of every host is VETOED
    (OFF), and the T1 ON region is no longer continuous from 30 kpc to r_ta.
  - Reported, not scored: (R1) exactly radial orbits (3-stream rank 1, no veto); (R2) phase-mixed / substructured
    halo (many streams, rank 3 everywhere inside lam1, no veto).
- Action: S = CFG354's leaf constraint + Int sqrt(-g) H_eps(l2 - tau) V(sigma_c) L_MOND + L_cold(Vlasov sheet) + L_gas.

## 2. Tests and pass lines
- **L legality:** T1 part as CFG354 (L1-L4 re-run, identical). Rank part as CFG351: V is a state function of sigma_c;
  switch stress -2 L_M sigma dV/dsigma consists of delta(det) sigma adj(sigma) = det delta(det) I = 0 and
  delta(e2) sigma (tr sigma I - sigma) which vanishes on the support {rank <= 1} (identity tr(s) s - s^2 = 0 for
  rank-1 s). Numeric check on 1000 random rank-1 / rank-2 states to 1e-12 (relative). PASS iff all hold.
- **(a) linear:** ON(f) is a subset of ON(T1) (V <= 1), and FRW has rank 0. PASS iff CFG354's T1 linear results
  (ON = 0) are reproduced.
- **(a') filaments and sheets (scored, both must hold):**
  - A1: CFG353's compensated cells (CFG354 tables), with the virialised rank map: cylinder core (x < w) rank 2, plane
    core rank 1, outside rank 0. False ON = 0 in every EdS cell.
  - A2: CFG351's separable 3-axis Zel'dovich field (A = (1, 0.7, 0.45), periodic 2 pi box), at the sheet stage
    D = 1.3, the filament stage D = 1.8, and every stage D in {1.0, 1.1, ..., 2.2} where at most two axes have crossed
    (D A3 <= 1). Density = exact cell-averaged ZA stream sum on a 96^3 grid; t from FFT Poisson; T1 at EdS tau;
    rank = number of multistream axes (CFG351). Ground truth "turned around in all three axes" (TA3): on each axis
    some stream at that x has D A_i cos q_i >= 1/2 (ZA EdS turnaround). False ON = ON(f) and not TA3.
    PASS iff the false-ON volume fraction is 0 at all these stages.
  - Reported: false OFF in A2 (TA3 and T1 ON but vetoed: the proto-knot fed by a filament); the cylindrical top-hat
    transient (pre-crossing rank 0 with delta >= 2 tau: window in ln a before crossing); prolate Ferrers
    ellipsoids (homogeneous: rank uniform); finite-filament tips (A2 near the future knot).
  - Host volume vetoed (reported, also enters (c)/(d)): the generic shell (lam1^3 - lam2^3 of the r_ta volume;
    phantom-mass share lam1 - lam2 for an isothermal phantom), and filament-fed hosts: N_f = 3 filaments of core
    radius beta r_ta (beta = 0.1, 0.2, 0.3) crossing lam1 < r < 1 (rank 2, vetoed; inside lam1 the host's streams
    add, rank 3). Volume share N_f beta^2 (1 - lam1) 3/4; phantom-mass share N_f beta^2 (1/lam1 - 1)/4 (capped at 1).
- **(b) hosts (CFG354's 24):** PASS iff T1 P(ON at 30 kpc) >= 0.99 on 24/24 (CFG354), 30 kpc < lam2 r_ta on 24/24
  (rank 3), and no flicker: a 10% gas compression at 30 kpc flips neither T1 (CFG354 fidelity) nor the rank (rank is
  invariant under invertible congruence; caustic radii are tied to r_ta, which the compression does not move).
- **(c) edge (scored):**
  - c1: the edge, defined exactly as CFG354 (outermost radius continuously ON from 30 kpc), under the generic rank
    model, within 100 kpc of r_ta on 24/24 hosts. Reported: the outermost ON radius; R1 and R2 edges.
  - c2: well-posed: T1 with the width (eps_min or W0) so that V_b/V_c^2 <= 1; the rank part has zero switch stress
    at rank-transition (caustic) surfaces (L line). Reported: the front impulse at caustics (CFG351 numbers).
  - PASS iff c1 and c2.
- **(d) data:** CFG354's harness copied (cfg355_edge_harness.py), scoring unchanged (KiDS d chi2 <= +9 both
  footings, SPARC A3 + rotmod d rms, growth). The phantom density is multiplied by the actual f(r):
  - rows: control 1.0; T1 sharp min/max (must reproduce CFG354); T1 smeared min/max (linear ramp of full width
    2 x 0.0158 r_ta centred on the T1 edge: the gap CFG354 left open); COMBINED generic min/max (smeared T1 edge AND
    the shell veto lam2 < r < lam1): **scored**.
  - reported rows: smear x3; combined + filament-fed veto (beta 0.1, 0.2).
  - PASS iff all scored rows pass (control, T1 sharp, T1 smeared, combined).
- **Ownership / UFD (brief, reported):** classes E/A as CFG351; CFG344 UFD clumps full rank.

## 3. Verdict
- SWITCH DOES BOTH: L, a, a', b, c, d all pass with 0 constants.
- WITH COST: all pass with n >= 1.
- PARTIAL: at most one failure.
- NO-GO: two or more failures.

## 4. Controls
- K0: without the veto (V = 1), CFG354's T1 numbers are reproduced: (a) max ON, (a') T1 cells, hosts P30/edges/c_d,
  eps_min (identical, 1e-12).
- K1: ideal filament (uniform cylinder core, rank 2) is vetoed: combined ON = 0 there.
- K2: isothermal halo (isotropic dispersion, rank 3 everywhere) is ON to its edge (= T1 edge = r_ta, isolated).
- K3: plane: T1 middle eigenvalue 0 => OFF regardless of rank.
- MUTATE (CFG355_MUTATE=1, outputs *_MUTATE): veto rank == 3 instead. It must switch OFF halo interiors and fail (b)
  or (d); exit 1 when detected.

## 5. Lean (Lean 4 + Mathlib, no sorry)
- Veto logic on ideal triples: sphere (lt, lt, lr) with rank 3 ON iff lt >= tau; cylinder core (c, c, 0) rank 2 OFF;
  plane (d, 0, 0) OFF for tau > 0 at any rank.
- ON(f) subset ON(T1) (false-positive bound); rank-3 MUTATE veto turns the interior OFF.
- Three streams: weighted deviations sum to zero (rank <= 2).
- Conservation: rank-1 identity tr(s) s - s^2 = 0 (entrywise); sigma adj sigma = det I (entry 11 and an off-diagonal).
- Width: eps >= c_d Delta/6 and (g_ph/g)^2 <= 1 => V_b/V_c^2 <= 1; eps_min > 0 iff c_d > 0.
- Shell volume share lam1^3 - lam2^3 > 0.03 for lam1 = 0.358, lam2 = 0.233 (bounds).

## 6. Protocol
No downloads. At most 4 processes. No home paths or names in files. Only this directory is written.
