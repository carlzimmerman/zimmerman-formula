# AN1_aest_nonlinear_dust: FROZEN CRITERIA

Committed alone, before any script or computed number of this lane. **Not blind:** the record's AeST, khronon and caustic lanes were read first (list below), including X14's analytic statement that the v3s khronon flow folds.

Authority: `OWNER_DECISION_2026-11-02_ONE_ACTION_LANE.md`. kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, never pooled. A gravitating field, never a particle. The cold sector stays retired by the decision of 2026-11-01: nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. No LCDM input in a grade. No download.

## 1. Question and what the record already says
What does the one-field class's dust do in a nonlinear spherical well beyond the hydrostatic branch: settle, fold, how much field mass is where when the solution ends?

Why the record does not already answer it, so the lane runs:
- X14 F4 has the shell equation and "phase-mix to crossing" analytically for v3s at mu_K where K(Q) is inert. It has no times, radii or capture numbers, no run at the BOLTZ1 floors where K(Q) is not inert, and no collapse from cosmological start.
- `real_research/aest_3d_nbody` and the 1D no-go it cites are about phase-pinning the free omega = mu c mode, not folds.
- H2 and UX2 row 4 say "needs a simulation" and "nobody has computed".
- DR2 N1 is a pressureless stream in a fixed well.

Standing obstacles, not solved here, stated in the README: H1's Y = 0 ghost for MOND-limit F (the negative-energy mode is the growth mode); planets need a screen outside F(Y, Q) (C1, M1); X14's caustic cure costs a new constant; BOLTZ1's mu floors; C7's K_B runaway at Q0 = 0.1 /Mpc; H2's and S4's static CANNOT for clusters.

## 2. Equations (derived by hand from C1's weak-field Lagrangian before any run; K0 checks them)
SZ21 action through C1, phi = Q0 t + chi, A_i = a_i, unit constraint kept to the order that matters, Phi = Psi, L_Q = Ktilde (Q - Q0)^2, n = dL_Q/dchi_dot, Pi = 2 K_B E + 2 (2-K_B) V, V = grad chi + Q0 a, E = a_dot + grad(a^2/2) + grad Psi.

Eliminating the current W = E - (1+J')V through the a equation gives an exact conservation law for n_eff = n + div Pi / Q0, which is the charge that sources the metric:
    div grad Psi = 4 pi Gtilde (rho_b + rho_d),   rho_d = Q0 n_eff / (16 pi Gtilde).
**Frozen limit: Q0 -> infinity at fixed mu** (slow branch; W -> 0; fast modes at omega ~ mu c, Q0 not excited, consistent with the record's no-go that they stay decoupled). Then, with h = n/(2 Ktilde Q0), c_s^2 = h, and K_B entering as kappa = K_B/(2-K_B):
    (V(E) + kappa E) flux:  div[V(E) + kappa E] + mu^2 h = 4 pi G rho_d,   E = -grad h,   V = E/(1+|E|/a0)   [C1's capped J, law mu = x/(1+x)]
    d rho_d/dt + div(rho_d v) = 0
    dv/dt = -grad Psi + E  (field)
    dv_b/dt = -grad Psi  (baryons)
    grad Psi = (1 - K_B/2) G (M_b + M_d)/r^2 + Lambda term
This is BS24's and L1's PN system with Xi = -h, and is H2's static system when E = grad Psi. rho_d includes the part div V / 4 pi G: **the law's phantom mass is carried by this same conserved charge.** So two field masses are reported: M_d (all charge), and M_d - M_ph (charge beyond what the law needs), with M_ph = r^2 (g_law - g_N)/G.

Validity of the limit, reported per row: Q0_need = max(g/(c v)) over shells; below that the aether speed V/Q0 is not small against the flow. C7's v4 Q0 = 0.1 /Mpc will be outside it; that case is NOT RUN. A finite-Q0 run is not in this lane.

Quadratic K throughout. h_bar(z_i)/c^2 is reported per mu; a row with h_bar(z_i)/c^2 > 0.1 is flagged QUADRATIC K LAPSES AT START (SZ21 note quadratic K can't hold early). It still runs. a0 constant, as in the action.

## 3. Setup, frozen
- **Background:** flat, h 0.672, rho_x0 = 3.32e10, rho_b0 = rho_x0/5.35 Msun/Mpc^3 (RF5/UX2, native), constant Lambda closing flatness; radiation neglected at z <= z_i. Same background on both footings. Simplification of the CPL form, disclosed.
- **Start:** z_i = 20, field and baryons on the same Lagrangian coordinate q, Zel'dovich: r = a q (1 - D_bar/3), v = H r - a... growing-mode velocity from the dust limit. **This is generous:** the field's suppressed growth before z_i (H1's 1/(1+k^2/mu^2)) is not charged.
- **Peak:** Gaussian linear density, filter mass M_G = M_tot (P1). Amplitude A1: the shell q(M_tot), with Xi off (pure dust, same background) collapses at z = 0. Secondary profile P2: M_G = M_tot/8, same A1 rule, canonical only. Amplitude A2 = 3 x A1, for mu <= 1 /Mpc only, because A1 is expected not to collapse there. Not fits; declared before running.
- **Masses:** M_tot 1e12 (galaxy) and 1e15 Msun (cluster). Field share of charge 5.35/6.35 of mass, baryons the rest.
- **Baryons** are cold shells that stop (inelastically, no constant) at measured final radii:
  - Galaxy: first 6.72e10 Msun of baryon charge stops on a spherical exponential M(<r) = M(1 - (1+r/R_d) exp(-r/R_d)), R_d 3.565 kpc (LC1). The rest stops at its own turnaround (hot halo, never falls).
  - Cluster: beta-model beta 2/3, r_c 0.15 R500, R500 1.35 Mpc, normalised to M_gas(<R500) = 1.19e14 (X-COP dM 2.74e14 / 2.3, LM1); the rest stops at turnaround.
- **Domain:** q out to 2 q(M_tot), uniform in q, N = 1500 field cells, N baryon shells. Outer Dirichlet h = h_bar(t); outer shell follows the Hubble flow.
- **mu list (frozen, /Mpc), each reported:** 0.0156 (BS24), 0.1 (v3s), 1 (SZ21, H2 cap), 10 (S4, BS24 Eq. 39 cap), 56.6 (BOLTZ1 forest), 2.04e4 (crossing proxy), 1.24e8 (BBN). K_B = 0.
- **Rows:** {2 masses} x {7 mu} x {2 footings} P1 A1 (28). A2: 2 masses x 3 mu x 2 footings (12). P2: 2 masses x 7 mu canonical (14). K_B = 0.078: 2 masses x 7 mu, canonical (14). 68 rows.
- **Held start H:** the hydrostatic branch itself: M_tot's baryons in place, field set to the static solution (Xi = Psi, mu term on, rho_d from the hold equation), static, velocity kick 1 % of V_c at each shell with a smooth radial shape, sin(pi r/R_out). Isolated static background, R_out 300 kpc (galaxy) and 3 Mpc (cluster). mu = 0.1, 1 /Mpc, both footings. Reports fold time. This grades "(a) if it got there, does it stay".

## 4. Numerics and end of solution
Lagrangian shells, KDK, adaptive dt with eta = 0.1 (min over Delta r/|Delta v|, sqrt(Delta r/|Delta F|), r/|v|, sqrt(r/|F|), Delta r/c_eff). Hold equation: finite-volume, Newton with line search on its convex objective.

**Fold:** minimum over cells of (Delta r)/(a Delta q) < 1e-2 and closing; fold time extrapolated t + Delta r/|Delta v|. A central focus (r_1 -> 0) counts. No artificial viscosity, no continuation, no completion: the row ends there. No completion is run in this lane.
Budget: 4e5 steps or 20 min wall per row; else UNRESOLVED, with the state reached.

## 5. Row labels (each row)
- **FOLD FIRST:** folds before z = 0.
- **SETTLED:** no fold by z = 0, the centre has turned around, and inside R_test (R_last galaxy, R500 cluster) |dv/dt| <= 0.1 g_Psi and |v| <= 0.1 V_c at every field shell. Must also repeat at N = 3000 (verify a win as hard as a fail).
- **NO COLLAPSE:** no fold by z = 0, central shell never turned around.
- **OSCILLATING:** turned around, no fold, not settled.
- **UNRESOLVED.**

Reported each: z_fold, t_fold, r_fold, m_fold, whether r_fold is grid-limited (r_fold <= 3 cells), pi/mu, M_d and M_d - M_ph inside 2.2 R_d = 7.84 kpc and R_last = 36 kpc (10 R_d) or inside 0.3, 0.7, 1.0 R500, against M_b there; Q0_need; h_bar(z_i)/c^2, E/g_Psi at R_test, fraction of baryons stopped.

## 6. Comparison with what's needed (reads, at end of solution)
- Galaxy: (M_d - M_ph)/M_b at 2.2 R_d, against A8/D4 (no pass line in the sheet; X22's tolerated M_c(<R_last)/M_b 0.035 canonical, 0.0049 alt at R_last).
- Cluster: (M_d - M_ph)/M_gas at x = 0.3, 0.7, 1.0, against X-COP [HSE - 0.12 dex, HSE] = [4.3, 6.7], [2.1, 3.9], [0.7, 2.3] canonical, and LM1's lensing map (about 8 at 0.2-0.5, 5 at 0.5-1, projected).
- **A comparison counts only for a row defined to z = 0.** A row that ends earlier reads ENDS BEFORE THE WELL EXISTS, or ENDS AT z_f, and its masses are only the state at that time.

## 7. Lane label
- **FOLDS OR NEVER COLLAPSES, NO HYDROSTATIC SETTLING:** all frozen checks pass, no row SETTLED or OSCILLATING past z=0 with a met need, at most 10 % UNRESOLVED.
- **SETTLES AT [rows]:** any verified SETTLED row; then its comparison reads are the news.
- **DEFINED TO z = 0 AT [rows]:** OSCILLATING rows exist without a fold; reported as such.
- **NO VERDICT:** any frozen check fails. Numbers are then reported only.
Highest possible label is a statement about this reduced system: spherical, Q0 -> infinity, quadratic K, K_B <= 0.078, one peak. It never says the action class works.

## 8. Checks (frozen; a miss means NO VERDICT)
| Id | Known answer | Line |
|---|---|---|
| K0 | sympy: subtracting the hold equation from Poisson on E = grad Psi gives H2's div[mu grad Psi] + mu^2 Psi = 4 pi G rho_b, including K_B; linear kernel s = 1 - k^2/(k^2 + mu^2) at x -> 0 (M1 at f0 = 0, H1's side result) | residual 0 |
| K1 | Oppenheimer-Snyder top-hat: uniform field sphere, mu 1.24e8, interior shell collapse time against the exact Newtonian shell integral on the same background | <= 3e-3 |
| K2 | Bertschinger-type: EdS, point seed, mu 1.24e8: r_ta(t) slope against 8/9 over a decade | <= 0.01 |
| K3 | Static n = 1 polytrope, a0 -> 1e-6 of canonical, mu 1 /Mpc: net force / g in r < 0.9 pi/mu at start; radius of 50 % mass drift over one t_dyn | <= 5e-3; <= 0.02 |
| K4 | Static law branch: H row's start: hold solver returns E within this of g_law at r in [1, 100] kpc for mu = 0.1, both footings | <= 2e-3 |
| K5 | Charge and energy, isolated sphere, mu 10 /Mpc, Neumann outer, Psi from enclosed mass: mass exact; hold-charge identity; T + U drift before fold, with U from the action's functional | mass <= 1e-13, hold <= 1e-8, energy <= 3e-3 |
| K6 | Linear growth at mu 1 /Mpc: spherical j0 mode at x << 1, growth z 20 to 5 against the ODE with s(k_phys(t)) | <= 5 % |
| K7 | Convergence, 1e12 and 1e15 at mu 1 (A2), 56.6, 1.24e8, canonical: t_fold N 750, 1500, 3000; eta 0.05 at N 1500 | |t_1500 - t_3000|/t <= 3 %, same for eta; non-grid-limited r_fold within a factor 1.5 |
| K8 | SIGTERM mid-row, resume gives the same fold time | <= 1e-10 relative |
| K9 | MUTATE (dust force -grad Psi - E, sign flip): writes `_MUTATE` outputs, must fail K3 or K4 | fails |

## 9. Hand expectation (before any number)
- mu >= 56.6: Xi negligible above pi/mu, field collapses as dust; central focus or fold at about the Gaussian centre's collapse time, z_fold about 1 for P1, r_fold near grid or a few pi/mu; little mass in the core; FOLD FIRST.
- mu <= 1 on 1e12: self-gravity cancelled (kernel s small), A1 NO COLLAPSE; A2 baryon-pulled shells fold within about a free-fall time.
- 1e15 at mu 1, 10: collapses, feels pressure at about 3 Mpc and below, so a gentler core, but no dissipation, so a fold or oscillation; I expect fold.
- No row settles: Hamiltonian flow has no way to lose energy except crossing (X14).
- Held start: phase-mix fold within a few tens of oscillation periods at 1 % kick.
- Capture: solution ends before disc or cluster mass profile exists, so no row reads against the need. I'd be surprised by any SETTLED row.

## 10. What would change the label
A verified SETTLED row; or any row with folds absent at convergence through z = 0; or a failed check.

## 11. Compute
One thread, nice 15, under 1 GB, checkpoint on SIGTERM, outputs under 20 MB. Estimated at most about 3 minutes a row, 4 hours total; this is under the 6 h cap, no reduction taken beyond one peak shape plus P2. Budget cap per row bounds the worst case at 68 x 20 min; if the total crosses 6 h, remaining rows are reported NOT RUN, in the frozen order P1, A2, K_B, P2.
