# HE1 (held-out envelope): FROZEN CRITERIA, committed alone before any HE1 script, Lean file or graded number

TEST lane, quarantined. Adopts nothing and relabels nothing. Not registered; does not edit fable52_push/README.md, any PAPER
file, the closure register or the memory index. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), graded
separately and never pooled. A FAIL is verified as hard as a PASS. No download; the 16 GB shear catalogue is not read.

Id check before writing: `ls -d fable52_push/HE1*` finds nothing; `git log --all --oneline | grep HE1` finds only hand-estimate
labels named HE1 inside other lanes (TR1, CFG566, CFG309 and older), no lane with this id.

## 0. Question

SWT1, KO1, SNP1, EMV1 and GAL1 (fable52_push, 2026-11-09) close the action-based switch on the law in its uniform form. Their
theorems leave room for one construction, which this lane builds and grades: **a cleared galaxy whose share of the cold
component is held outside the wall by its own velocity dispersion** (an envelope in Jeans equilibrium), not resting on the wall
as a shell (SNP1 A.2 shows that is unstable) and not swept by it.

## 1. The construction (frozen in my words; no new constant)

- **Inside the wall** (r < R_w) the law is on and there is no cold component. Outside it gravity is Newtonian. By SWT1 T1 the
  inside shows only M_b from outside (the wall carries the layer -M_ph(R_w), M_ph(r) = M_b (sqrt(1/4 + 1/y) - 1/2)).
- **The envelope** occupies R_w <= r <= R_out. It is isotropic and isothermal with one dispersion sigma and obeys the Jeans
  equation in the Newtonian field of M_b plus itself: sigma^2 d rho / dr = -rho G (M_b + M_env(< r)) / r^2, M_env(< R_w) = 0.
  Nothing lies beyond R_out in this construction (the envelope's pressure there is reported in G6, not used).
- **BC1, pressure balance at the wall:** rho(R_w) sigma^2 = p_wall(R_w) = (a0^2 / 4 pi G) W(u), W(u) = u - ln(1 + u)
  - u^2 / (2 (1 + u)^2), u = u_in(y_w), y_w = G M_b / (a0 R_w^2) (SWT1 T3; `p_wall`, `Wfun`, `u_in` of swt1.py).
- **BC2, the closure (singular isothermal at the wall):** rho(R_w) = sigma^2 / (2 pi G R_w^2), the density a singular isothermal
  exterior of dispersion sigma has at R_w. With BC1 this gives sigma^4 = 2 pi G R_w^2 p_wall(R_w): sigma is a function of R_w.
  The Jeans equation then carries the envelope outward from (R_w, rho(R_w), enclosed mass M_b), which is not the singular
  solution (its enclosed mass at R_w would be 2 sigma^2 R_w / G); that departure is reported.
  - Why a closure is needed: Jeans + BC1 + the share leave a one-parameter family. BC2 is the brief's Part A exterior applied at
    the boundary. It is my choice and it is stated as such.
  - **Closure bracket C (reported, no label):** sigma^2 = G (1 + X) M_b / (2 R_out) (the singular sphere holding baryons plus
    share inside R_out), with BC1 and the share condition fixing R_w.
- **BC3, the share:** M_env(< R_out) = X M_b. Solved for R_w on (0.05 r_M, R_out). If several roots exist the largest R_w is
  taken (the branch continuous with the deep closed form) and the others are reported. If none exists the (mass, X, R_out) has
  **NO BALANCE**.
- **X** (the record's, not fitted): X_share = OD / OB = 5.561889 (swt1.py `R_DUST`); X_census = 5.364 N(log M_b) with N from
  CFG902's declared fixed point (`campaign_fresh_gravity/CFG903_framework_two_halo_kids/cfg903_lib.py`, `N_of_declared`, read
  only); X_cap = 53.64.
- **R_out:** primary = r_ta((1 + X) M_b) today from swt1.py's `r_ta` with a0 = 0 (outside the wall gravity is Newtonian).
  Newtonian turnaround radii scale exactly as M^(1/3); the code computes one reference mass per epoch, scales, and checks the
  scaling directly on two masses (KA7). Brackets: 1.5 and 3 Mpc physical at z = 0 for every mass; at z 0.5 and 1 they keep their
  ratio to r_ta.
- **Masses:** KiDS's four bins log M_b 9.4, 10.45, 10.7, 10.9 (point baryons); SWT1's GSMF grid (log M* 9 to 12 by 0.25, M_b = M*,
  Driver+2022, as swt1.py); for G4 each lens's own Mgal (the record's stars plus cold gas) on a grid log M 9.1 to 11.1 by 0.1,
  interpolated (KA6 checks the interpolation).
- **Units used by the code:** x = r / r_M, r_M = sqrt(G M_b / a0), v_f^4 = G M_b a0; density in M_b / r_M^3; then
  p_wall = W / (4 pi), BC2 reads rho = s / (2 pi x^2) with s = sigma^2 / v_f^2, and A = 2 s.

## 2. Part A (exact; Lean 4 + Mathlib, `HE1.lean`, mutate twin `HE1_MUTATE.lean`)

Statements to certify (algebra and inequalities, not physics):

- **A1 deep balance.** With G M_b = a0 r_M^2, the deep wall pressure (a0^2 / 4 pi G)(2/3)(r_M / R)^3 equals the singular
  isothermal pressure sigma^4 / (2 pi G R^2) iff R = (r_M / 3)(v_f / sigma)^4 (v_f^4 = G M_b a0).
- **A2 amplitude form.** A = 2 sigma^2 / v_f^2 turns A1 into R_w / r_M = (4/3) / A^2.
- **A3 envelope mass.** The singular envelope's mass 2 sigma^2 R / G equals A (R / r_M) M_b (v_f^2 r_M = G M_b); the shell
  R_w..R holds A ((R - R_w) / r_M) M_b.
- **A4 new lower bound on W:** (2/3) u^3 / (1 + u)^2 <= W(u) for u >= 0 (derivative of the difference (1/3) u^3 / (1 + u)^3).
- **A5 exact wall slope.** With y = u^2 / (1 + u): W <= y (u - y) <= (3/2) W, so d ln p_wall / d ln R = -2 y (u - y) / W lies in
  [-3, -2] for every y (y (u - y) = u^3 / (1 + u)^2; upper side from SNP1's W_upper, lower side from A4).
- **A6 exact W against the closed form.** If the balance holds with the exact W, then R_w <= R_deep (from W <= (2/3) t^3,
  t = sqrt(y), SWT1) and R_w >= R_deep / (1 + t)^2 (from A4 with t <= u and u^3 / (1 + u)^2 increasing).
- **A7 stability.** If the envelope pressure falls as R^-n with n < 2 and the wall pressure falls at least as fast as R^-2
  outward and at most as fast inward (A5), a displacement of the wall either way meets a restoring net force. The brief's
  statement (n < 3 against the deep -3) is the special case. Swept-layer reading: with the displaced material carried at the wall
  the net outward force is p_wall(R) - p_wall(R_w), restoring whenever p_wall falls with R.
- **A8 slope at the wall of the exact Jeans solution.** d ln p / d ln r at R_w is -G M_b / (sigma^2 R_w); with A1-A3 it equals
  -(3/2) A, so the deep balance is stable iff A < 4/3.
A statement that cannot be proved is listed NOT CERTIFIED with its numerical check beside it. The twin carries false versions
(wrong power, wrong prefactor, a false bound) and must fail to compile.

## 3. Part B (numbers)

Per footing, per X and R_out (primary and the two brackets), for the four KiDS masses and the GSMF grid: R_w (kpc, / r_M,
/ R_K with R_K = sqrt(G M_b / 1.38e-15)), sigma (km/s and / v_f), A, envelope mass inside 200 kpc, 1 Mpc and 3 Mpc (in M_b),
every root found, and the departures of the exact solution from A1-A3 (R_w against (4/3) r_M / A^2; M_env against the singular
form).

## 4. Gates (per footing; each X separately; primary R_out unless stated)

- **G1 discs untouched.** R_w >= 10 r_M at all four KiDS masses and every GSMF grid mass, and no component inside R_w (checked:
  M_env(< R_w) = 0 by construction).
- **G2 filling.** The walls on the GSMF grid at z 0, 0.5 and 1 (R_out(z) = r_ta at that epoch, a0 unchanged) through SWT1's
  `compensated` (imported from swt1.py): q_tot <= 0.0354 at all three epochs. Reported beside it: the filling against GAL1's
  0.0197 (and 0.0134 for a z 6 switch-on), and the same with late types only (each mass weighted by the late fraction of
  `lr_lenses.npz` (`typ` == 0) in 0.25-dex bins of `logM`, ends held; a stated proxy).
- **G3 stability.** At every KiDS and GSMF mass the exact solution satisfies s_env > s_wall, with s_env = -G M_b / (sigma^2 R_w)
  the envelope's pressure log-slope at R_w (exact Jeans) and s_wall = d ln p_wall / d ln R at R_w (exact W): the envelope's
  pressure falls more slowly than the wall's. NO BALANCE anywhere fails G3 for that X. Reported: the swept-layer reading (A7)
  and the quasi-static reading (envelope re-solved at fixed sigma and share with the wall displaced by +-5 %).
- **G4 KiDS, cleared lenses.** Lens sets: W30 late (`f30` and `typ` == 0) and host-free late (KO1's host-free flag: no galaxy at
  least 0.3 dex more massive within the lens's own R_h = min(3 Mpc, sqrt(G Mgal / 1e-15)) projected and |dchi| < 230 Mpc;
  plain float comparison, KO1's tie rule, 40,667 host-free). Windows: outer bins 0-3, middle 4-6, inner 7-12. Data
  amplitudes A_w by KO1's estimator (per-bin stack over the law, weighted by the per-bin jackknife errors s_k). Joint 3 x 3
  jackknife covariance C of (A_outer, A_middle, A_inner) over the 50 patches.
  - Model per lens and bin: KO1's annulus average (24 Gauss-Legendre nodes in R^2) of glaw(g) P_model(R) / P_law(R),
    R = sqrt(G Mgal / g), where P = 4 G DeltaSigma by projection: P_law = point M_b + the law's phantom to infinity (numerical to
    1e4 R, analytic singular tail); P_model = point M_b + the phantom inside R_w + the thin layer -M_ph(R_w) at R_w + the
    envelope's own density R_w..R_out (projected, not a point). The ratio keeps KO1's law convention for everything the two
    share; the raw P_model / glaw is reported.
  - Model amplitude per window: the same estimator applied to the model's per-bin means (the data's s_k as weights).
  - Statistic: chi2 = D^T Cinv D, D = A_data - A_model, Cinv = (45/49) C^-1 (Hartlap, 50 patches, 3 dimensions); p from chi2
    with 3 dof. The same for the law alone (A_model = 1, 1, 1). Reported: without the Hartlap factor.
  - **PASS iff p > 0.05 on both stacks.** The late-type split was first seen post hoc in KO1 and shares its veto-edge effect,
    so a pass here is a consistency check, not a confirmation.
  - **G4b (frozen companion, stated beside the label, not in it):** one free calibration factor c on the model (GLS), chi2
    with 2 dof, p > 0.05 on both stacks; the same for the law. The record's lesson (KO1) is that absolute amplitudes are
    calibration-limited. If G4 and G4b disagree, RESULT.md says so in its first lines.
  - Reported: the shape ratio A_outer / A_inner for data and model; host-free late with the veto widened to 1.3 and 1.6 R_h.
  - KiDS models use the z = 0 construction (R_out today) for every lens (as SWT1 E3 and KO1 do); disclosed.
- **G5 hot systems stay held.** X-COP: the seven clusters with measured stars (QX5's loader, files under
  `real_research/data/xcop/`), M_tot = hydrostatic M_FORW, M_b = gas + stars (stars held at their outermost value beyond their
  extent, inside the gas extent), M_c = M_tot - M_b, rho_c = (dM_c / dr) / (4 pi r^2) clipped at 0, p_c(r) = integral from r to the
  gas extent of rho_c G M_tot / r'^2 (no tail: a lower bound). Lovisari+2015 groups (the record's table,
  `real_research/data/lovisari2015_groups.tsv`): power laws through (R2500, R500) for M_tot and M_gas, M_b = M_gas (1 + f*),
  f* = 0 and 1 (GB1's brackets), extrapolated inward to 0.05 R500 (stated proxy), p_c integrated to 2 R500.
  p_wall(r) uses y = G M_b(< r) / (a0 r^2). **PASS iff p_wall < p_c at every radius in [0.05, 1] R500 for every cluster and group
  (both f*)**: no wall can sit outside 0.05 R500, so the law does not turn on there. This gate does not depend on X.
- **Reported, not gated.**
  - G6 formation: sigma against the virial dispersion sigma_vir^2 = G (1 + X) M_b / R_out (collapse to R_out / 2); envelope mass
    inside 200 kpc, 1 Mpc, 3 Mpc against a collapsed singular halo of the same share inside R_out / 2; the fraction of that halo
    inside R_w (the part that must never have been inside the wall, since SNP1 shows the wall cannot push a bound share out);
    for X_share also against SWT1's placement (singular to R_h = SWT1's NC radius). The envelope's pressure at R_out against
    the mean component density times sigma^2 and against the infall ram pressure rho_m (H R_out)^2. Formation is open and the
    RESULT says what it would take.
  - The record's pooled KiDS gate (B21 Fig. 9, 59 points, all lenses cleared): points with |log10(model / law)| > 0.05, and chi2
    against the data with the per-point errors (as SWT1 E3), differential and raw projections.

## 5. Labels (per footing)

- **PASSES STATIC GATES:** G1 to G5 all pass for at least one X of {X_share, X_census, X_cap} at the primary R_out, and every
  known answer passes.
- **FAILS:** otherwise, naming the failing gates for each X.
- **NO VERDICT:** a known answer fails, or A1-A3, A5 or A8 is not certified in Lean.
- The brackets (R_out 1.5 and 3 Mpc; closure C) are graded the same way and reported; a bracket that passes while the primary
  fails is stated in the first lines of RESULT.md and is not a pass label.

## 6. Known answers (must pass)

- KA1 deep limit: BC1 + BC2 with the exact W against (r_M / 3)(v_f / sigma)^4 at R_w / r_M = 1e3 and 1e4: relative difference
  <= 3 r_M / R_w (A6's bracket). The Jeans solver started on the singular solution (enclosed mass 2 sigma^2 R_w / G) stays
  singular to 1e-6 over three decades; started with negligible density it matches rho_w exp((G M_b / sigma^2)(1/r - 1/R_w))
  to 1e-6.
- KA2 p_wall: an independent implementation in he1.py against swt1.py's `p_wall` at 20 values of y from 1e-8 to 1e4: 1e-12
  relative.
- KA3 projection: a thin shell (Sigma and M_cyl) and a truncated singular isothermal sphere (Sigma = (2K / R)(arcsec(b / R)
  - arcsec(max(a, R) / R)) and its M_cyl closed form) at R / b = 0.05 to 1.5: 1e-4 relative; an untruncated singular sphere
  gives 4 G DeltaSigma = 2 sigma^2 / R to 1e-3.
- KA4 KO1 reproduced: host-free count 40,667; window amplitudes and errors for host-free late and W30 late on both footings equal
  ko1_extra.out's printed digits (three decimals).
- KA5 limits of the lens model: no wall (law everywhere) gives window amplitudes 1, 1, 1 to 1e-9; the raw projection of the
  point baryons alone equals (4 / pi) g to 1e-4.
- KA6 interpolation: the per-lens ratio interpolated at mid-grid masses against a direct solve: 2e-3 relative in every bin.
- KA7 r_ta scaling: r_ta(M) = r_ta(M_ref)(M / M_ref)^(1/3) against direct swt1.r_ta at two masses: 1e-5.
- KA8 the import of `compensated`: SWT1's NC table at z 1 gives q_tot 0.0180 / 0.0182 (SWT1's printed values).

## 7. MUTATE (separate output files; must fail)

- M1 opposite sign of the wall pressure (p_wall -> -p_wall): BC1 then needs rho(R_w) < 0. Bites iff NO BALANCE for every mass,
  X and R_out on both footings.
- M2 p_wall / 100: bites iff G1 fails for every X at the primary R_out on both footings (the walls move inside 10 r_M).
- M3 the envelope treated as a point mass at the lens centre in G4 (4 G DeltaSigma_env = 4 G M_env(< R) / (pi R^2)): bites iff
  KA3's singular-sphere check fails under it (by the factor 4 / pi) and at least one window amplitude of the model moves.
- Lean twin, as in section 2.

## 8. Disclosure: what I looked at and estimated before freezing

Read: fable52_push/README.md, the RESULT.md of SWT1, KO1, SNP1, EMV1, GAL1, the sibling hand-over notes, swt1.py, swt1_extra.py,
ko1_extra.py and ko1_extra.out (the late-type window amplitudes are known to me: host-free late -0.19 +- 0.39 / 1.53 +- 0.40 /
1.58 +- 0.27 canonical; W30 late 0.53 +- 0.23 / 1.54 +- 0.26 / 0.92 +- 0.16), the loaders of PD1 / SS1 / GB1 / QX5, SNP1.lean.
Computed before freezing, as inputs only: N = 10 for log M_b 9.4, 10.45, 10.7 and 9.52 for 10.9 (X_census 53.64 / 51.08);
Newtonian r_ta((1 + X) M_b) today 0.237 / 0.530 / 0.642 / 0.748 Mpc for X_share and 0.479 / 1.073 / 1.300 / 1.492 (1.516 cap) for
the census share; r_M 1.93 / 6.48 / 8.64 / 10.88 kpc (canonical); R_K 0.504 / 1.687 / 2.250 / 2.833 Mpc; lens log Mgal spans
9.20-11.05; the X-COP radial coverage (hydro 0.02-2.9 R500; gas to 1.5-2.1 R500; stars of A2319 end at 1.06 R500). No envelope,
wall, filling or lensing model number has been computed.

My hand estimate (deep singular closed forms; unverified, and the lead's two-of-three record says to distrust it):
- X_share at its own r_ta: R_w about 40-55 r_M (0.15-0.2 R_K at L*), A about 0.15-0.18, sigma about 0.28-0.30 v_f.
- X_census / X_cap at r_ta: R_w about 9-12 r_M (0.04 R_K), A about 0.35; G1 marginal, likely FAIL. At 3 Mpc: R_w about 43 r_M
  (0.16 R_K), A about 0.18 (the lead's estimate was 65 r_M, 0.14, 0.37 R_K).
- G2 PASS (filling under 1 % at r_ta). G3 PASS (envelope slope about -1.5 A, near -0.3, against the wall's -2 to -3).
- **G4 FAIL for every X:** with the wall near 0.15-0.2 R_K the middle window (0.16-0.38 R_K) sits outside the wall, where the
  model gives about 0.1-0.3 of the law, while both late stacks sit near 1.5 there. The law alone also misses host-free late
  (outer -0.19).
- G5 PASS by a wide margin. Expected label: FAILS (G4 for every X; G1 for the census share at r_ta).
- The pooled B21 gate fails at most points outside the wall.

## 9. Operational

One thread (thread variables set to 1), under 1.5 GB, minutes. Files: he1.py -> he1.json / he1.out; he1.py --mutate M1|M2|M3 ->
he1_MUTATE_M1/M2/M3.json / .out; HE1.lean, HE1_MUTATE.lean, compile.txt, compile_MUTATE.txt (no home paths); RESULT.md (label
first, a table per gate, what works, what is open). Commits with explicit paths only; push via a temporary sparse worktree.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
