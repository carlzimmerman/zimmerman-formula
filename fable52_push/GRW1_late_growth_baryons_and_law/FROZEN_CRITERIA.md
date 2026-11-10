# GRW1 frozen criteria: can baryons under the a0 law build late structure when the cold component is warm late?

Frozen before any GRW1 script exists in the lane and before any graded number. TEST lane, quarantined: adopts nothing,
relabels nothing, registers nothing. Both footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2), graded separately,
never pooled. One thread, under 1.5 GB, each run checkpointed to `parts/`. No downloads: every data row below is on disk.

**Disclosed before freezing.** To check that the criteria can be run, I tested in a scratch folder (outside the repo):
CLASS's dark-energy fluid slot as the cold component (it refuses w >= 0, so w is set to -1e-10 with cs2 = x_T; see 1.4),
CLASS's transfer normalisation (P = 2 pi^2 / k^3 Delta_R^2 T^2, matched to 6e-4), CLASS's baryon temperature (no
photoheating: 5 K at z 3, so 1.5 below replaces it after reionization), and a law-off two-fluid engine against CLASS from
z 700 (cold reference within 0.2 % in P at k >= 0.04 / Mpc; 12 % off at k 0.01, a horizon-scale effect). While testing,
CLASS printed the law-off warm model at c_s 1000 km/s: sigma8 0.522 against the reference's 0.796. That is the M-OFF arm's
law-off model, not a graded number. **No law-on number of any kind was computed before this file was committed.**

## 0. The question and what it rests on

DT1's trade-off (certified with conditions in MK2) says a dust term cannot keep the cold component clumping on small
scales late and also keep galaxies empty of pooled dust. So a completion with clean galaxies has a cold component that is
warm late. MK2's exponential term is the concrete case: an isothermal cold component with one sound speed c_s, whose
comoving Jeans length today is 74 Mpc at 500 km/s and 148 Mpc at 1000 km/s. MK2 found every graded row except clusters
and groups met at c_s 1000-4481 km/s, and named three rows it could no longer carry: CMB lensing, growth, the forest.
GRW1 asks whether baryons, with the law on and the law's halo counted as real gravitating density, carry them instead.

What the record already settled (read, not recomputed):
- WG1-WG6 (`rebuild_2026_10_22/`): baryons-only start (no cold component at all), the law as QUMOND on the peculiar field
  in a PM box. Law off: CMB lensing far too low (r 2e-4 to 0.31). Law on: 11-14x too high in power with the measured-style
  expansion, and the shape is wrong under every rule (14x at L 28, 0.08x at L 377). The median web field is 0.002-0.004 a0.
- SV5, X4, Q6 D0: a0 is absent from the FRW background; the law on the linear web boosts a dust-target source 75-89x.
- CFG555 / CFG596: growth must be scored on the gravitating field, not on particles.
- QX3 iter2 G1: the baryons-only control fails the PR4 lensing shape at chi^2 869-929 against the 18.48 line.
- NC2 bracket (ii): baryons alone under Newton grow as a^0.29 and fail the forest by Delta chi^2 2.3e5.
- GAL1: a scale-independent boost q of growth and potential fails CMB lensing at 2 sigma once q exceeds about 0.03.
What is new here: the cold component is cold early (so baryons inherit its wells, unlike WG's Silk-damped start) and warm
late, and the law enters through the action's own linear theory (T-A below), not only through QUMOND.

## 1. The setup (frozen)

### 1.1 Background and species
The record's reference, the background GAL1 used (QX3 iter2 corner): omega_b 0.0215, omega_d 0.11958060485606123, H0 65,
n_s 0.95, A_s 2e-9, tau 0.06, N_ur 3.046, T_cmb 2.7255, flat, Lambda closing (the smooth dark-energy term, w = -1). So a0
is constant in time on each footing (a0 = kappa c sqrt(G rho_DE) with rho_DE constant). Photons and neutrinos enter the
background (CLASS H(z)) and are smooth in the growth equations after z_start. H(z) is CLASS's for each model.

### 1.2 What gravitates
Baryons; the cold component's whole gravitating density; nothing else. In action (A) read as form B (law on everywhere,
S = 1), the cold component's energy density at linear order is n_d + Pi (TPA1 E4: n n T^Q = n_d, n n T^L = Pi + O(P^2)),
and the conserved clock charge is N = n_d + Pi (TPA1 E3; lambda P/Q is second order). n_d is the dust part, which carries
the pressure p = L_K(Q); Pi = D.P is the law's halo. Both gravitate (QX17, FB1 note). The law's stiffness gamma_L F(Pi)
has F''(0) = 0 and, in its quadratic regime, acts only below Lstar (tens of pc), so it drops out on these scales (stated
assumption). The law's stress at linear order is zero, so Phi = Psi and lensing sees Phi.

### 1.3 The law's treatments (frozen; the law is nonlinear, so "linear growth" needs one)
Notation: ' = d/d ln a; Omega_b, Omega_c are background fractions at a; q^2 = (k c_s / (a H))^2 / ((3/2) Omega_c) = (k/k_J)^2,
k_J the cold component's comoving Jeans wavenumber; mu_th = cos(angle between the mode's k and the local external field).

**T-A (primary): the action's own linear theory, with the law read on the clock's acceleration.** In the action the law
reads A, the clock frame's acceleration, and A = -grad ln Q = -c_s^2 grad delta_d (exactly, for the exponential term:
c_s^2 = n/(Q n')). A free-falling clock has A = 0 and carries no law (REL1, COL1); a pressure-held clock has A = grad Phi
(the static law). With K P = nu(|A|) A, nu = a0/(a0 + |A|) (TPA1 E2 at gamma_L = 0), linearised about an external |A_e|
= x a0: k.K dP = c(mu_th) k.dA, c = (1/(1+x)) (1 - x mu_th^2/(1+x)). Then delta_Pi = c q^2 delta_d, so
delta_d = delta_N / (1 + c q^2). Equations per mode (k, mu_th):

    delta_b' = D_b ;  D_b' = -(2 + dlnH/dlna + drag) D_b + (3/2)(Omega_b delta_b + Omega_c delta_N) - (k c_b/(aH))^2 delta_b
    delta_N' = D_N ;  D_N' = -(2 + dlnH/dlna) D_N + (3/2)(Omega_b delta_b + Omega_c delta_N) - (3/2) Omega_c q^2 delta_N/(1 + c q^2)

Lensing and Poisson source: delta_lens = (omega_b delta_b + omega_d delta_N)/(omega_b + omega_d). The external field is
mean-field and self-consistent: x = A_rms / a0, A_rms^2 = integral dln k Delta_R^2(k) < (c_s^2 (k/a) delta_d)^2 >_mu_th
over the mode grid (k 1e-3 to 10 / Mpc, physical units), solved for x by root-finding at every step.
Justification: it is derived from the action, reproduces TPA1 4.4's quasi-static dispersion exactly (c = epsilon), and
its equilibrium (where (1 - c) q^2 > 1) is the static law: total source = baryons x q^2/((1 - c) q^2 - 1) -> 1/(1 - c) =
1/(mu_e (1 + L_e mu_th^2)), the AQUAL response of the simple law. The law's halo must flow in with the clock.

**T-A-max (bound on T-A): c = 1 for every mode at every step, and every initial condition at z_start taken from the cold
reference.** The clock coefficient 1 - q^2/(1 + c q^2) rises with c (Lean), and c <= 1, so T-A-max is the most growth T-A can
give under any external-field treatment and any law history before z_start (the law can at most cancel the clock's
pressure; it cannot make it colder than cold). If T-A-max falls short, T-A falls short under every external-field choice.

**T-S (bracket; the lead's suggested treatment): the static law with the total field as external field.** The law's
halo is in place at once as the static law requires, on every scale, linearised about the rms total peculiar field (the
large-scale field acting as the external field of small scales). The cold component's dust part delta_d keeps its own
law-off Jeans pressure; the halo is extra gravitating density B - 1 times the Newtonian source:

    D_b' = -(2 + dlnH/dlna + drag) D_b + (3/2) B (Omega_b delta_b + Omega_c delta_d) - (k c_b/(aH))^2 delta_b
    D_d' = -(2 + dlnH/dlna) D_d + (3/2) B (Omega_b delta_b + Omega_c delta_d) - (3/2) Omega_c q^2 delta_d
    B(mu_th) = 1 / (mu_e (1 + L_e mu_th^2)),  mu_e = x/(1+x),  L_e = 1/(1+x),  x = g_rms / a0,
    g_rms^2 = integral dln k Delta_R^2 < (B (3/2) Omega_m(a) a H^2 delta_src / k)^2 >_mu_th  (self-consistent root),

delta_lens = B (omega_b delta_b + omega_d delta_d)/(omega_b + omega_d). This is the record's WG2 R1 rule in linear
mean-field form, with the cold component present. Reported beside it (counted once): the halo's contrast in units of the
cold mean, (B - 1)(omega_b delta_b + omega_d delta_d)/omega_d, rms over k <= 1 / Mpc; above 1 the linear T-S needs more
cold charge than the region holds.

All treatments: modes on k = 64 log points from 1e-3 to 10 / Mpc, mu_th on 6 Gauss-Legendre nodes in [0, 1]; power =
mu_th-average of |delta|^2. The law is on from z_start; before it, CLASS (law off).

### 1.4 The cold component (models)
The exponential term (DT1, MK2): an isothermal fluid with constant c_s, w = c_s^2 = x_T (to O(x)). In CLASS: omega_cdm 1e-8,
Omega_fld = omega_d/h^2, cs2_fld = x_T, w0_fld = -1e-10, wa 0, use_ppf no (CLASS forbids w >= 0 in the fluid slot; the
difference, ~1e-5 in w, changes only the background at the 1e-5 level and the adiabatic sound speed, which matters only
outside the horizon). Its comoving Jeans wavenumber falls as (1 + z)^(1/2), so it is cold early and warm late; its
"z_w" at wavenumber k is where k_J(z) = k.
- **Primary band (MK2's passing band): c_s = 1000, 1495, 2117, 3000, 4481 km/s.**
- **DT1 bracket (reported, own labels): c_s = 350, 500, 707 km/s.**
- **Step family W (reported, own labels, T-A and T-A-max only):** cold (c_s = 0) until z_w, then c_s = 1000 km/s;
  z_w = 3 and 1; initial conditions from the cold reference.
- The reference: CLASS with omega_cdm = omega_d (cold throughout, law off).

### 1.5 Baryons, initial conditions, numerics
- c_b^2 = max(CLASS c_b^2, 0) + w_re(z) 1.5 k_B T_IGM / (0.59 m_p c^2), T_IGM = 1.5e4 K, w_re = (1 - tanh((z - z_re)/0.5))/2,
  z_re = CLASS's z_reio (CLASS's T_b has no photoheating). Compton drag on the baryon velocity, photons at rest:
  drag = (4 rho_gamma / 3 rho_b) kappa' / (a H), kappa' from CLASS.
- z_start = 700. delta_b, delta_c from CLASS synchronous-gauge transfer functions at z_start (comoving for the cold part),
  D = d delta / d ln a by central difference over d ln a = 1e-3. Normalisation Delta_R^2 = A_s (k / 0.05)^(n_s - 1).
- Integration: scipy DOP853, rtol 1e-7, atol 1e-10 (per unit R), outputs on z 0-7 (141 points), 7-700 (60 points, log).
- Observables are ratios to the reference run through the same engine and initial redshift; absolute spectra are
  ratio x CLASS's reference P_lin(k, z). Above z_start, and outside k 1e-3 to 10, the ratio is held at its edge value.

## 2. Observables and the graded lines (frozen; every row is on disk in the record)

| line | quantity | row and lane | met when |
|---|---|---|---|
| **L1 CMB-lensing amplitude** | r_eff = A(X0)/A(S X0), S(L) the Limber ratio of C_L^phiphi with P_ref(k, z) R_lens(k, z), GAL1's kernel | PR4 amplitude of X0, sigma_A,rel 0.0241 (SV5 T0.4, GAL1 KA1); GAL1's 2 sigma line | \|r_eff - 1\| <= 2 sigma_A,rel (0.0481) |
| **L2 CMB-lensing shape** | Delta chi^2 = chi^2_refit(S X0) - chi^2_refit(X0), amplitude refit (as A_s is refit) | KD1 G9a on QX3 iter2's PR4 reader (9 bandpowers L 8-400, CMB-marginalised covariance) | Delta chi^2 <= 4 |
| **L3 f sigma8** | Rf(z) = f sigma8 ratio, f sigma8 = sigma_8 of the baryons' velocity divergence in units of aH (galaxies move with baryons) | DESI DR1 Table 9 ratios as CE2 transcribed, 4 bins x 2 panels (GAL1) | \|Rf - r\| <= 2 err, every bin and panel |
| **L4 S8** | s = sigma8 ratio at z 0 of the density lensing sees (Omega_m unchanged) | KiDS-1000 0.759 +- 0.0225 (SS4 CS line, GAL1) | \|s - 1\| <= 0.0593 |
| **L5 forest** | P_bb ratio (the gas) at 6 log-spaced k from 1.10 to 3.56 h/Mpc, z 2 and 3 | L346's standing line (`real_research/g03_audit_2026/L346_switch_forest_gate.py`) | every ratio in [0.8, 1.2] |

Reported, not graded: the lensing-density ratio R_lens(k, z) on k 0.01-10 at z 0, 0.5, 1, 2, 3, 4; the forest line on the
total (lensing) density and at z 4; S(L) at L 100, 200, 400 and per PR4 bin; sigma8 and f sigma8 absolute; x(z) for each
treatment (against WG1's measured web field 0.003-0.22 a0); delta_Pi and delta_d rms (T-A); T-S's counted-once diagnostic;
the KD1 G9a absolute line chi^2(S X0) <= 18.48; T-A from z_start 900 (sensitivity).

**Direction and factor.** Each failing line is SHORT (below its band) or OVER (above). Factor = obtained / nearest band
edge: for L1 r_eff/(1 -+ 0.0481); L3 Rf/(r -+ 2 err) at the worst bin; L4 s/(1 -+ 0.0593); L5 ratio/0.8 or ratio/1.2 at
the worst bin. L2 has no direction of its own: if L2 fails with L1 met, the miss is "shape".

## 3. Labels (per treatment, per footing; frozen first)

Per (treatment, footing, c_s): **BUILDS IT** if L1-L5 are all met; **FALLS SHORT** if every failing line among L1, L3,
L4, L5 is SHORT; **OVERSHOOTS** if every one is OVER; **FALLS SHORT AND OVERSHOOTS** if both occur (each named); if only
L2 fails, **MISSES THE SHAPE**.

Per (treatment, footing), over the primary band: **BUILDS IT** if any c_s builds it (named); else the common label of the
five c_s if they share one; if the band's c_s give SHORT on one side and OVER on the other with no c_s built, bisect in
log c_s between the neighbours to 1 % and label BUILDS IT if a pass is found, otherwise **FALLS SHORT AND OVERSHOOTS
ACROSS THE BAND** (named). **NO VERDICT** if any known answer fails or a frozen row cannot be read.

The headline gives T-A's label and T-S's label on both footings, and T-A-max's. If T-A and T-S differ, the first line says
the answer depends on the treatment of the nonlinear law, and gives both. Order of work, cheapest first: known answers,
closed forms, T-A-max, T-A, T-S, MUTATE. If T-A-max falls short at every c_s, T-A's label is decided by the bound; T-A is
still run for its numbers.

## 4. Known answers (each must pass, else NO VERDICT)

- **KA1** GAL1's PR4 row replays: A_X0 and sigma_A,rel equal sv5_t0.json within 1e-6 relative; chi^2_refit(X0) equals
  iter2.json's 8.5709 within 1e-3 relative.
- **KA2** cold reference, law off: (a) my D(z)/D(0), f(z) and f sigma8(z) against CLASS at GAL1's z 0, 0.295, 0.51, 0.706,
  0.919, 1.5, 2, 3, max relative difference <= 2e-3 (GAL1's KA2 line); (b) P_mine/P_CLASS at z 0, 1, 2, 3 within 1 % for
  k in [0.04, 10] / Mpc (k < 0.04 reported).
- **KA3** baryon-only suppression and the T-A exponents, EdS background (Omega = 1, dlnH/dlna = -3/2), started off the
  growing mode, late slope within 1e-6 of: (a) clock smooth (delta_N held 0), baryon fraction f in {0.157, 0.05, 0.5}:
  p = (-1 + sqrt(1 + 24 f))/4, the standard baryon-only suppression; (b) T-A at c = 1 and q -> infinity: p = (-1/2 +
  sqrt(1/4 + 6 lambda))/2, lambda = (f + sqrt(f^2 + 4 f (1 - f)))/2; (c) T-A at c = 0, q -> infinity: equals (a).
- **KA4** warm law-off engine against CLASS's fluid at c_s 1000 and 4481 km/s: |delta_m,mine - delta_m,CLASS| / |delta_m,ref,CLASS|
  <= 1e-2 for k in [0.04, 10] at z 0, 1, 3 (error in units of the reference, the unit every graded ratio uses).
- **KA5** the law's linear response: (a) 1 - c(mu_th) = mu_e (1 + L_e mu_th^2) at 100 random (x, mu_th), 1e-12; (b) T-A's clock
  coefficient with c = epsilon equals TPA1 4.4's 1 - k^2/(mu_K^2 + epsilon k^2) at q = k/mu_K, 1e-12; (c) a 1-D nonlinear
  AQUAL finite-difference solve (simple law, uniform external field x in {0.03, 0.3, 3}, small plane-wave source along and
  across it) reproduces B(1) and B(0) within 1e-3.
- **KA6** Limber: (a) a constant ratio R gives S = R^2 within 1e-10 (GAL1 KA4a); (b) my absolute Limber X_L equals CLASS's
  X0 within 2 % at L 100, 200, 300, 400 (GAL1 KA4b); (c) a scale-independent ratio fed through the k-dependent code equals
  the z-only code within 1e-10.

## 5. MUTATE twins (separate outputs; each must move in its stated direction)

Run at c_s 1000 and 4481 km/s, both footings, for T-A and T-S. "Moves" = every graded quantity (r_eff, s, Rf at the four
bins, the L5 ratios) changes in the stated direction by more than 1e-4 relative; otherwise the arm does not bite (disclosed).
- **M-OFF** (law off; c = 0 in T-A, B = 1 in T-S): every graded quantity moves DOWN from the treatment's primary.
- **M-COLD** (cold component cold throughout, c_s -> 0, law on): T-A: A = 0, so the law carries nothing and every ratio
  returns to the reference: moves UP to 1 within 1e-6. T-S: moves UP from its primary.
- **M-2A0** (a0 doubled): T-A moves UP (x halves, c rises); T-S moves UP (the boost rises).

## 6. Lean

`fable_independent_2026/lean_2026/GRW1.lean`, standard axioms: the clock coefficient's monotonicity in c and its value at
c = 1; 1 - c = mu_e (1 + L_e mu^2); the equilibrium total q^2/((1 - c) q^2 - 1) solves the static equations; the growth
exponents of KA3 solve their quadratics, with p_baryons < p_T-A < 1 for 0 < f < 1. Twin `GRW1_MUTATE.lean` states false
versions, one per theorem; it must fail with one error each.

## 7. Hand estimates before freezing (disclosed; they do not enter any gate)

- KA3's closed forms at f = 0.157: baryons alone grow as a^0.296; T-A at c = 1 as a^0.609; the reference as a^1. So I
  expect T-A to FALL SHORT: on the forest by a factor of tens in power (warm since z of order 100-500 at k ~ 1 / Mpc),
  and on CMB lensing, S8 and f sigma8 by tens of percent (warm since z ~ 5 at k ~ 0.1 / Mpc at 1000 km/s).
- I expect T-S to OVERSHOOT by more than WG2's 11-14x, because here the cold component builds the early wells.
- So I expect the answer to depend on the treatment. The lead's guess was "either side"; these are guesses too.

## 8. Files (planned)

`grw1_lib.py` (engine), `grw1_ka.py` -> `grw1_ka.json/.out`, `grw1_run.py` -> `grw1.json/.out` and `parts/`,
`grw1_run.py --mutate off|cold|2a0` -> `grw1_MUTATE_<arm>.json/.out`, `grw1_grade.py` -> `grw1_grade.json/.out`, Lean with
`compile.txt` and `compile_MUTATE.txt`, RESULT.md (label first, one table).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
