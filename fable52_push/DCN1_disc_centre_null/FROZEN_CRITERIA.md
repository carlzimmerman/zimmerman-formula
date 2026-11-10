# DCN1 (the disc-centre null): FROZEN CRITERIA, committed alone before any DCN1 script or number

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), reported separately, never pooled. The component is cold dark energy,
never a particle. No download. This lane writes only fable52_push/DCN1_disc_centre_null/; it does not edit
fable52_push/README.md, CLOSURE.md, SCS1 / SCS2 / SCS3's files or any paper (SCS3's copy of scs2_aqual.py is copied into this
folder unchanged and patched only at run time, in named variants).

Id check: `ls -d fable52_push/DCN1*` and `git log --all --oneline | grep -i dcn1` both empty. Started by the fable52 lead
session on the owner's instruction ("keep pushing all open lanes until we get closure").

## 0. The question

SCS3 (origin e6a6dc2cf2) found, on the thick-disc twin (log M_b 9.4, external field 0.1 a0 along the axis, both footings),
route L's growth rate at the disc's own null RATE UNBOUNDED on R4-R6 (e-fold 1.25 -> 0.87 -> 0.42 Myr canonical). SCS2 and
SCS3 masked isolated discs' centres (r < 0.002-0.010 R_d). Is the static clock's state (action (A), mu_K = 0, n_d = 0, the
law's halo, gravity coupled; SCS1-SCS3's system) at a null of the field inside baryons:
- (i) ill-posed (rate unbounded as the scale shrinks, at the null itself),
- (ii) a discretisation artefact, or
- (iii) unstable at a bounded rate?
Two problems:
- **P1, the external-field null:** the thick twin in a uniform field along the axis: log M_b 9.4, 10.45, 10.7, 10.9; g_e = 0.1
  and 0.01 a0; both footings (16 backgrounds). The 9.4 / 0.1 a0 pair is SCS3's flagged case and is the primary.
- **P2, the isolated centre:** SCS2's isolated discs with the centre unmasked: the thick disc (the only isolated family whose
  centre is a field null inside a smooth baryonic density), all four masses, both footings (8 backgrounds); and every SCS2
  isolated family (razor-thin exponential and Kuzmin at four masses, disc + bulge at four masses, R_d x 0.5 and x 2) mapped
  with the mask removed (shell 0 only masked), reported.

## 1. Part A: local analysis at the null (sympy, exact; graded as a structural statement)

Route L's local rate (SCS2 / SCS3, Lean growth_par): Gamma_loc^2 = -4 pi G D.P u (2 + u), u = |grad Phi|/a0,
4 pi G D.P = div[grad Phi/(1+u)] = lap Phi - 4 pi G rho_b on any background solving div[mu(u) grad Phi] = 4 pi G rho_b,
mu = u/(1+u). sympy must establish, exactly:
- **A1 (the identity).** On any such background, with n = grad Phi/|grad Phi| and Phi_nn = n.Hess(Phi).n,

      Gamma_loc^2 = (2 + u) [ u Phi_nn/(1 + u) - 4 pi G rho_b ],

  in 3D for a general (non-symmetric) Phi (checked symbolically, and numerically on random cubic Phi with rho_b defined by the
  law), so the rate is set by the field's own directional derivative u Phi_nn = n.grad(|grad Phi|^2)/(2 a0) and the baryon
  density, not by D.P alone.
- **A2 (the null limit).** At a null inside baryons (rho_b > 0, u -> 0) with the deep-law scaling |grad Phi| ~ s^(1/2) (s the
  distance to the null; the 3-Laplacian's scaling), u Phi_nn tends to a finite, direction-dependent limit, so Gamma_loc^2 is
  bounded there. Closed limits: the slab (1D) gives Gamma_loc^2 -> -4 pi G rho_b, the uniform sphere -(5/3) 4 pi G rho_b
  (both decaying, i.e. STABLE at the null). D.P itself diverges as s^(-1/2) at such a null; u -> 0 cancels it.
- **A3 (the stiffness and the blend).** With the stiffness on, omega^2 = G (1 + gamma_L F'' m k^2 - K m)/m (SCS1/SCS2). The
  adopted stiffness is the Pi^6 blend F = gamma b^2 f(Sigma/b), which equals the raw switch -(gamma/2)[max(D.P,0)]^2, and so
  is identically zero with its first two derivatives, wherever Sigma = D.P < 0 (owner decision 71e4014cd5; TC1). sympy states
  the k -> infinity limit of omega^2 in the two cases: D.P < 0 (F'' = 0: omega^2 -> G (1 - K m)/m, bounded in k) and D.P > 0
  (omega^2 rises as + k^2, stable). So neither gamma_L nor the blend can bound or unbound a rate where D.P < 0; the only
  candidate for an unbounded rate at a null is the spatial one (D.P u as s -> 0), which A1-A2 address.
- A1-A3 are a pass if sympy simplifies the stated differences to 0 (and the random-cubic check to < 1e-10 relative).

## 2. Part B: numerics

**B0. Copied code.** scs2_aqual.py (SCS3's copy, unchanged) and SCS3's make_grid_res / gamma_maps logic (copied into
dcn1_global.py, not imported from SCS3's folder).

**B1. Global backgrounds.** SCS3's grids (A1 / A4 resolutions), solved by the copied solver. Two inner treatments, both run:
- **as frozen (SCS2/SCS3):** the thick deposit's mass inside r_min is the thin-disc estimate M [1 - (1 + r_min/R_d) e^(-r_min/R_d)];
- **corrected (variant C):** that mass is the thick disc's own, rho_0 (4/3) pi r_min^3 (rho_0 = M/(4 pi R_d^2 h_z)).
P1 boundary data come from the variant-C global solution at R4 (if one R4 solve takes more than 45 min wall, R3, disclosed).
P2's global unmasked maps run R0-R3 (half theta, cheap) in both treatments.

**B2. Local resolved solves (the graded numerics).** An axisymmetric finite-volume solve of the same law,
div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b, mu = x/(1+x), on a uniform cylindrical (R, z) grid around the null, with the
thick disc's density rho_0 exp(-R/R_d - |z|/h_z) (cell averages, 4 x 4 sub-samples) as the source, and Dirichlet data on the
outer faces interpolated (bilinear in ln r, theta) from the B1 global solution. Face mu from the normal difference and the
averaged tangential cell gradients (SCS2's rule, in (R, z)); R = 0 is a symmetry axis (zero flux; cell faces of zero area).
Picard iteration to relative residual 1e-10 (relaxation 0.7, max 800 iterations).
- **P1 box:** R in [0, L], z in [z_n - L, z_n + L], z_n the null on the axis of the global R4 solution (the axis cell with the
  smallest |grad Phi| between 1e-3 and 0.3 R_d below the disc on the side where the disc's pull opposes g_e), L = 0.4 |z_n|.
- **P2 box:** R in [0, L], z in [0, L], mirror (zero flux) at z = 0, L = min(0.5 h_z, 0.5 a0/(4 pi G rho_0)); the null is the
  corner (0, 0).
- **Resolutions** N_R = 48, 72, 108, 162, 243 (ratio 1.5; P1 has 2 N_R cells in z, P2 N_R).
- **Analysis region:** cells whose centres lie within L/2 of the null (no Dirichlet boundary within L/2).
- **Quantities per resolution:** Q = Gamma_max^2 = max over the analysis region of Gamma_loc^2 (route L, the FV D.P and the
  central-difference cell u, exactly SCS3's formula), its location and u, D.P there; the number of D.P < 0 cells; min D.P;
  Gamma_id^2 = the A1 identity evaluated with finite-difference Hessians (an independent discretisation; reported); and the
  scaling exponent of |D.P| and u against the distance s to the null (fits over s in [4 h, L/4]; reported).

**Convergence rule (graded): SCS3's A4 rule (b34295ebcd), no flat clause.** On the finest three: d1 = Q_mid - Q_coarse,
d2 = Q_fine - Q_mid. Monotone and |d2| < |d1|: p = ln(d1/d2)/ln 1.5, Q_inf = Q_fine + d2/(1.5^p - 1), E = 1.25 |d2|/(1.5^p - 1);
d2 = 0: Q_inf = Q_fine, E = |d1|; oscillating: Q_inf = mean of the finest two, E = max(|d1|, |d2|); with four or more
resolutions E = max(E, |Q_inf(finest three) - Q_inf(previous three)|). **Converged** iff p (when used) lies in [0.5, 6] and
E <= 0.20 |Q_inf|. **Diverging** iff monotone with |d2| >= |d1| on the finest three and on the previous three.
Before any use, the rule must pass KA3 below.

## 3. Labels (per footing; per problem, then the lane)

Per background b (P1 or P2's thick centres), on the local solves:
- **unbounded(b):** Q is Diverging, and the measured growth of Q with 1/h agrees in kind with Part A (i.e. Part A fails to
  bound it: A1 or A2 fails, or the identity Gamma_id^2 diverges too).
- **bounded-unstable(b):** Q converges and Q_inf - E > 0 (growth at a finite rate).
- **stable(b):** Q converges and Q_inf + E < 0, or no D.P < 0 cell exists in the analysis region on the finest two
  resolutions.
- **open(b):** otherwise.
Problem labels:
- **P1:** ILL-POSED AT THE NULL if unbounded(b) on any background (with every known answer passing); else NO VERDICT if any
  background is open; else BOUNDED if bounded-unstable on any background (reported: Q_inf, e-fold, against t_H = 13.8 Gyr and
  the local free-fall time 1/sqrt(4 pi G rho_0)); else ARTEFACT (the null is stable when resolved; SCS3's divergence is the
  global grid's).
- **P2:** the same with ARTEFACT read as **STABLE AT THE CENTRE** (there is no SCS3 divergence to remove).
- **The lane, per footing:** NO VERDICT if any graded known answer fails or Part A fails; else ILL-POSED AT THE NULL if P1 or
  P2 is; else BOUNDED if P1 or P2 is; else ARTEFACT (P1 ARTEFACT and P2 STABLE AT THE CENTRE); else NO VERDICT.
SCS3's own global sequence (R4-R6) is also put through the rule and its location reported (whether the maximum sits on the
global grid's axis cells, theta within one cell of 0 or pi).

**What each label means for SCS1 / SCS2's STABLE (stated in RESULT.md):**
- SCS1 (a point mass) has no null (|grad Phi| -> infinity at the centre); no label here changes it.
- P2 ILL-POSED: SCS2's isolated STABLE fails at every smooth disc centre: the static state is not well-posed there.
- P2 BOUNDED: SCS2's STABLE fails at the centre at the stated finite rate (a local instability of the disc centre).
- P2 STABLE AT THE CENTRE: SCS2's isolated STABLE extends to the centre (for these disc models).
- P1 (any label): concerns discs in an external field only, where SCS3 already excluded STABLE; ILL-POSED would add an
  ill-posed point inside the disc; ARTEFACT removes SCS3's open item.

## 4. Known answers (graded)

- **KA1 (SCS3's flagged rows):** the copied global solver, as frozen, at R4 on thick 9.4 / 0.1 a0 (both footings) reproduces
  SCS3's scs3_maps_THICK_AX_A4.json Gamma_L^2 and min D.P to 1e-6 relative. R5 and R6 also if one R5 solve stays under 4 GB
  and 60 min (else reported as not rerun; SCS3's stored R5/R6 rows are used for the rule).
- **KA2 (SCS2's isolated STABLE with the mask on):** the copied solver as frozen at R0 and R1 on SCS2's isolated thick and
  primary backgrounds reproduces D.P > 0 in every masked-in cell and SCS3's / SCS2's stored min D.P to 1e-6 relative where a
  stored value exists.
- **KA3 (the rule):** Q(h) = Q_inf (1 + c h^p), p = 1, 2, 0.75, random Q_inf (both signs) and c: Q_inf recovered to 1e-6
  relative and Converged; Q(h) = h^-1 and h^-0.5 labelled Diverging; Q(h) = 1 + h^0.3 not Converged.
- **KA4 (the local solver on an exact null): the uniform sphere.** rho_b = rho_0 everywhere in the box, Dirichlet data from
  the exact spherical solution g = (g_N + sqrt(g_N^2 + 4 a0 g_N))/2, g_N = (4/3) pi G rho_0 r, null on the axis at the box
  centre (P1 geometry) and at the corner (P2 geometry): Q converges by the rule to the exact sup of the closed-form
  Gamma_loc^2 over the analysis region within the rule's E and 2 % (both negative), at rho_0 and L of the canonical 9.4 thick
  disc.
- **KA5 (the local solver on a manufactured null with D.P < 0):** Phi = (c/2) z^2 - (a/4) R^2 + b z (a saddle, null on the
  axis at z = -b/c), rho_b manufactured from the law, Dirichlet data exact: Q converges to the exact sup of Gamma_loc^2 over
  the analysis region within E and 5 %.
- KA4 and KA5 must pass before the P1 / P2 local solves are graded.

## 5. MUTATE twins (separate outputs; each must bite)

- **M1 tilt sign flipped (G -> -D.P)** on every local solve: the labels must change on every background whose unmutated label
  is stable or bounded-unstable.
- **M2 planted divergence:** add to D.P at the analysis region's cell nearest the null a spike -(h_0/h)^2 |min D.P(N_R 48)|:
  the rule must call Q Diverging (unbounded) on every background.
- **M3 identity mutated:** drop the 1/(1+u) in A1: the sympy check must fail, and Gamma_id^2 must disagree with route L on the
  KA4 sphere by more than 5 %.
- **M4 Lean twin** (only if a Lean file is written): false versions must fail.

## 6. Lean (only for the structural claim)

If written (fable_independent_2026/lean_2026, built there): the algebraic identity behind A1 (given mu u-expansion, the
rate equals (2+u)[u Phi_nn/(1+u) - s]), the slab and sphere limits are negative, and the stiffness term vanishes where
Sigma <= 0 for the raw switch; with a twin of false versions.

## 7. Resources and rules

Under 4 GB per process, single-threaded BLAS, at most two heavy processes at once (other sessions share the machine);
checkpoint per background to a partial json; SIGTERM writes the partial file and exits; caches in the scratchpad. Commit
with explicit paths only; push by replaying the lane's commits with git merge-tree + commit-tree onto origin/main.

## 8. Disclosure: what I saw and expect before any DCN1 number

Read before freezing: SCS2 / SCS3 RESULT.md and criteria, and SCS3's stored THICK_AX_A4 rows for the flagged backgrounds:
the maximum sits at theta 167.8-179.7 deg (the first one to few cells off the axis) with u = 0.18-0.59 there (not small) and
D.P = -7.5e9 to -6.5e10 Msun/kpc^3, deepening about 2x per refinement. On paper (not run): the A1 identity, the slab /
sphere limits (-1 and -5/3 in units of 4 pi G rho_b), and that the frozen thick deposit puts the thin-disc mass inside r_min
(about 5e-9 M, some 2500 times the thick disc's own) at the centre as a point mass. A cell with u ~ 0.5 a few pc from a
null where g_e = 0.1 a0 needs the field to change by about 0.5 a0 over a few pc, some 30 times what the local density's
tide allows. So I expect P1 ARTEFACT or BOUNDED near the free-fall rate, and P2 STABLE AT THE CENTRE. Not results.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
