# CLS1 (a cluster state solved in action (A)?): FROZEN CRITERIA, committed alone before any script, Lean file or number

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Both footings (canonical a0 9.3603e-11,
alt 1.1312e-10 m/s^2), never pooled. The component is cold dark energy (the clock's charge), never a particle. Not a
LCDM lane. No download. This lane writes only `closure_2026_11_10/CLS1_cluster_state_in_action/` (Lean files here,
compiled with the in-repo build: `cd fable_independent_2026/lean_2026 && lake env lean <absolute path>`).

Id check: `ls closure_2026_11_10/CLS1*` found nothing; `git log --all --oneline | grep -c CLS1` gave 0.

Lane XCV1 (another session) grades form B's X-COP ceiling against HeCS masses. CLS1 does not grade the share or the
ceiling; it asks only whether action (A) has a cluster state at all. Any share number printed here is reported, never
label-setting.

## 0. The question

`closure_2026_11_10/THEORY_ASSEMBLED_2026-11-10.md` section 3: no cluster state has been solved in the action; rule 5's
hot branch (RB1) is a rule. DT3 proved, by a shell enthalpy inequality, that one engineered kinetic function cannot hold
X-COP as a smooth spherical static-clock equilibrium. CLS1 applies the same necessary-condition method to action (A)
itself (QX17 section 0, with the adopted Pi^6-blend stiffness, F = gamma b^2 f(Sigma/b), b = rho_DE) and to its two
admissible clock states:

- **S1, static clock (law branch).** tau = Q_inf t, zero shift, zero tilt. The clock's charge is the phantom D.P (the
  law's halo) plus the dust term's charge n = mu_K^2 (Q - 1)/K. Free per cluster: Q_inf (equivalently the central x).
  Free globally: mu_K > 0 (one constant of the action, the same in every cluster).
- **S2, the share as a hot / multi-stream free-falling clock component.** Is any collisionless (velocity-dispersion)
  pressure support available in (A) at all? If not, is a static cold core of the clock's dust at the share a solution,
  with only the clock's own pressure (its own w)?

## 1. The physics used (to be checked symbolically, section 5)

c restored where stated; K = 4 pi G / c^2; x := Q - 1.

- Dust term L_K = mu_K^2 x^2 / (2K). Charge n = dL_K/dQ = mu_K^2 x / K (mass density, SI: n = mu_K^2 c^2 x / (4 pi G)),
  so **x = 4 pi G n / (c^2 mu_K^2), exactly linear in n with no offset** (Q = 1 is n = 0).
- Energy density e = (mu_K^2/2K)(Q^2 - 1) = n (1 + x/2) (QX17 K5); pressure p = L_K = n x / 2; enthalpy per charge
  (e + p)/n = Q. The clock fluid is a perfect fluid with 4-velocity n^m (single-valued; one stream per point).
- Static hydrostatic balance of that fluid: d ln Q / dr = -d ln N / dr = -g / c^2, i.e. N Q = Q_inf (Tolman). This is
  QX17's static khronon reduction (E3 with lambda = 0 in a static state).
- Gravitating (active) mass density of the dust in the static weak field: m = e + 3p = n (1 + 2x). Mapping m(n) is
  strictly increasing, so it is inverted exactly (no small-x expansion).
- Source mass: the action-exact simple law (mu(y) = y/(1+y)) gives, for measured enclosed dynamical mass M at r,
  M_src = F(M, r) = M^2 / (M + a0 r^2 / G) (DT3's inverse). The law's phantom D.P is inside F; the dust's active mass is
  M_dust = F - M_b (+ the background material (4 pi/3) rho_bg r^3 restored, as DT3; rho_bg = DT2's value).
- The blend: F' is bounded by gamma_L max(Pi, b) (f convex, f(s) = s^2/2 for s >= 1, so f'(s) <= max(s, 1)). Its two
  terms in the constitutive law are bounded relative to A by gamma_L max(Pi, b) and gamma_L max(Pi, b) / (r A), with
  gamma_L = K Lstar^2 / 2, Lstar = 21.7 / 22.9 pc (canonical / alt), Pi <= the node's material-density upper bound,
  b = rho_DE (Omega_DE 0.69, H0 70). Both must be <= 1e-6 at every node, else NO VERDICT (the blend cannot be dropped).

## 2. Data (as DT2 / DT3, read-only)

- Seven X-COP clusters (A1795, A2029, A2142, A2319, A644, A85, ZW1215), loader of
  `research_closure_2026_11_10/DT2_response_audit/cluster/check_shape.py` run read-only via runpy: five nodes at
  0.1, 0.2, 0.3, 0.5, 0.7 R500 (hydro FITS), M_FORW +- n EM_FORW, baryons = gas + stars, held fixed.
- Envelopes: **central** (n = 0) and **two-error** (n = 2). The label is set by the two-error envelope (the widest; a
  violation there implies one at the central masses). Central is reported.
- **HeCS node** (`../_external_data/hecs_omnibus_2026_11_10/table2.tsv`, read with `python3 -I`, untrusted): for the X-COP
  clusters in HeCS (expected A85, A1795, Zw1215, A2029, A2142), a sixth node at r = R200 (HeCS), M = M200 +- n e_M200
  (spectroscopic, dynamical; HeCS units 1e14 Msun, Mpc). Baryons at R200 from the X-COP gas + star profiles if they cover
  R200; otherwise bracketed [M_b(r_last), M_b(r_last) R200 / r_last] (gas density falling at least as r^-2 beyond the last
  measured radius; disclosed), with each bound used on the conservative side. The HeCS node is a second envelope
  family (**HSE+HeCS**); the label uses the HSE-only family; HSE+HeCS is reported (it can only add constraints).

## 3. Necessary conditions (no profile can beat them)

For radii r_i < r_j < r_k (all 10 ordered triples of the 5 nodes; 20 with the HeCS node), on the S1 state with
attractive g and positive dust charge in [r_1, r_last] (positivity frozen: the share is positive), x and n decrease
outward (N Q = Q_inf, g > 0), so mean-value bounds hold exactly:

- Upper density at r_i: m(n(r_i)) <= Mmax_dust(r_i) / V(r_i)  ->  n_i <= m^-1(.)
- Lower density at r_j: m(n(r_j)) >= [Mmin_dust(r_k) - Mmax_dust(r_j)] / V(r_j, r_k)
- Lower density at r_i (shell i..j) and upper density at r_k (shell j..k) likewise.
- D_min(i, j): integral r_i..r_j of the law acceleration with a nondecreasing source floor (DT3's staircase from below);
  D_max(i, k): the same with a ceiling (nondecreasing source mass bounded by the next node's upper value).

**UP (the cold bound; DT3's inequality):** ln[(1 + x(n_i,up)) / (1 + x(n_j,low))] >= D_min(i, j) / c^2.
Fails for every mu_K above some mu_hi (span -> 0 as mu_K -> infinity).

**LOW (the stiff bound; new here):** ln[(1 + x(n_i,low over shell i..j)) / (1 + x(n_k,up over shell j..k))] <= D_max(i, k) / c^2.
Fails for every mu_K below some mu_lo when the lower inner density exceeds the upper outer density by more than
exp(D_max/c^2).

A triple whose shell lower bound is <= 0 gives no UP constraint; a triple whose inner lower bound is <= the outer upper
bound gives no LOW constraint (kept, never read as failures).

**Necessary window** W(cluster, footing, envelope) = set of mu_K in (0, infinity) passing UP and LOW on every triple.
Evaluated on a log grid 1e-6 to 1e8 per Mpc (physical), 0.002 dex, edges refined by bisection to 1e-9 relative, and
cross-checked against the closed forms (s = 1/mu_K^2 exact for the leading-order linear map; KA5).

## 4. Construction (sufficiency), only where a window is non-empty

Static spherical ODE in r (from 1 kpc): dx/dr = -(1 + x) g / c^2, dM_dust/dr = 4 pi r^2 m(n(x)) with
n = mu_K^2 c^2 x / (4 pi G), g = law(G (M_b + M_dust) / r^2) (simple law, the footing's a0); M_b(r) log-log interpolated
from the X-COP profiles (inside the first profile radius extrapolated with the first two points' log slope; disclosed).
One free number per cluster, x(1 kpc) (log grid 1e-12 to 1 plus refinement), and mu_K on the window. A cluster is
**CONSTRUCTED** at mu_K if some x(1 kpc) gives M_dyn = g r^2 / G inside the two-error envelope at all its nodes, with
x > 0 on [1 kpc, r_last]. Reported with the dust / M_b at the outer node (against 5.41; not graded here).

## 5. S2 items

- **S2a (sympy, structural).** T^Q_mn = g_mn L_K + (mu_K^2/K) Q x n_m n_n: leaf-projected stress h T h = L_K h
  (isotropic), anisotropic part 0, one 4-velocity n^m per point. The P sector's stress (T^W, T^P) is the law's own,
  already inside F (its charge is D.P, fixed by g through (E2)). So (A) carries **no collisionless (dispersion) pressure**:
  the only support available to the clock's charge in a static well is the barotropic p = n x / 2 of S1. A multi-stream
  state would need d tau multi-valued (shell crossing), which is outside the action's smooth solutions (stated, not
  graded).
- **S2b (tilt, argued + numbers).** A stationary tilted clock (tau = Q_inf t + sigma(r)) in a spherical static metric,
  regular at r = 0 (no central sink), has zero radial khronon current, J^r = n^r [rho_Q - lambda' P^r / Q] = 0; with
  P.A / rho_Q post-Newtonian (printed per cluster, must be <= 1e-3), this forces n^r = 0: back to S1. Non-stationary
  (moving) configurations are outside this test, as in DT3.
- **S2c (the cold core).** The static cold core at the share is S1 at form B's admissible mu_K: the record's background
  line mu_K >= 198.25 / 198.24 per Mpc (KD1 B1a; MK1 row 1) and its Jeans line 2.512e4 (MK1 row 2). Printed per
  cluster: the UP violation factor (required span / allowed span) on the strongest triple at 198.25 and 2.512e4.

## 6. Labels (frozen), per footing, from the two-error HSE-only envelope

S = an S1 state (mu_K, Q_inf per cluster); S2 adds no state beyond S1 if S2a and S2b hold.

1. **NO VERDICT** if any known answer (section 7) fails, if the blend bound exceeds 1e-6, or if S2b's ratio exceeds
   1e-3.
2. **NO STATE** if W is empty for every one of the seven clusters (every mu_K > 0 violates a necessary condition on
   every cluster) and S2 adds nothing (S2a, S2b).
3. **STATE EXISTS** if one mu_K is CONSTRUCTED on all seven.
4. **STATE EXISTS-PARTIAL** otherwise, with the sub-reading: number of clusters with a non-empty W; whether the common
   window (intersection over the seven) is empty (then **no single mu_K serves all seven**: no S matches all seven);
   number CONSTRUCTED; where the windows sit against the record's mu_K values.

Second reading (reported with the label, same rules): **at form B's admissible mu_K** (mu_K >= 198.25 per Mpc, the
background line form B needs for its CMB rows). Also printed: membership of the record's values 1e-3 (TK1 floor),
0.912-1.514 / 0.759-1.380 (groups), <= 1.00 / 0.765 (KiDS), <= 7.08 / 5.62 (SPARC), 1.35 / 1.26 (MK1's X-COP closest
miss), 198.25, 6.22e3 (Saturn), 2.512e4 (Jeans line), 3e4 (TK1 mu_0) in each cluster's W.

## 7. Known answers (all must pass, else NO VERDICT)

- KA1: QX2's bare-law shortfall reproduced through DT2's loader: mean log10(M / M_law) = 0.46749899183464316 /
  0.4345230963151764 (to 1e-6).
- KA2: one DT3 inequality value reproduced by this lane's own code: A2029, triple (0, 2, 3), two-error envelope,
  canonical: D_min / c^2 = 1.49168e-5 and q_upper = 64918.38 (DT3 run001), relative 1e-4 or better.
- KA3 (sympy, residual 0): e = n(1 + x/2), p = n x/2, (e + p)/n = Q; static Euler equation dp/dr = -(e + p) dlnN/dr
  is equivalent to N Q = const; T^Q projected stress isotropic (S2a).
- KA4: planted S1 equilibrium: a synthetic cluster made by the section-4 ODE at a planted mu_K with a planted x(1 kpc)
  and 5 % envelopes; its W must contain the planted mu_K and the construction must recover it.
- KA5: window edges from the grid + bisection agree with the closed-form edges of the leading-order (linear-in-x) bound
  to 1e-3 relative wherever x <= 1e-3 at the edge.
- KA6: ODE check: with a0 = 0 and uniform background-free test (no baryons, mu_K r ~ 1) the ODE reproduces the
  Helmholtz solution x ∝ sin(mu_K r)/(mu_K r) to 1e-6 (weak-field limit x << 1).

## 8. MUTATE twins (each must bite: change a window edge by > 10 % or flip a cluster's emptiness)

- MU1: LOW dropped (UP only).
- MU2: D_min set to 0 (UP cannot fail).
- MU3: the linear map replaced by x = 4 pi G n / (c^2 mu_K^2) x 1e6 (a 1e6-times-hotter dust).

## 9. Lean

If the label rests on a structural claim, it is the window algebra: for E = exp(D) > 1, alpha, s > 0, u, l > 0,
E (1 + alpha l s) <= 1 + alpha u s implies u > l E and s >= (E - 1) / (alpha (u - l E)); and its LOW twin; and that a
lower edge above an upper edge empties the window. `CLS1.lean` (standard axioms only) and `CLS1_MUTATE.lean` (false
statements that must fail to compile).

## 10. Process

Amendments post hoc, each committed alone and disclosed. Commit with explicit paths only. Push by replaying the lane's
commits with git merge-tree + commit-tree onto origin/main (no full temp worktree; no history rewrite). No compute above
4 GB. RESULT.md leads with the label per footing, then a table, then commit ids (local / origin).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
