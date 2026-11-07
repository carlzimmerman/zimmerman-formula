# NA1 frozen criteria: the last two untested FA1 doors, I5 (disformal bulk-motion selector) and I7 (defect network of the a0 scalar)

Frozen before any NA1 script or NA1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle.
Footings graded separately, never pooled: canonical a0 9.360324825027975e-11 m/s^2, Lstar 21.7 pc; alt
1.1312035414413022e-10 m/s^2, Lstar 22.9 pc. A door SURVIVES only if it passes on both. Compute: one thread, nice 15,
under 1 GB RSS, minutes; no state kept (a SIGTERM handler writes a partial .out and exits). No downloads. Every input is
already committed and used read-only. Values marked PROVISIONAL are recalled literature, not fetched, not graded data.

**Not blind.** I have read FA1 PHASE1_IDEAS (I5, I7), PHASE2_RECORD_CHECK, I6_galileon, FA3 criteria/result, SEED 11-06,
DX1 ANALYSIS (D1: kinematics reach the khronon sector only at (v/c)^2 <= 1.1e-5), QX5 iter_c (khronon bulk velocity
DEAD on provisional inputs), AX1 AUDIT (TeVeS FAIL on GW170817). Expected, stated now: I5 DEAD BY REDUCTION; I7 DEAD.

Inputs (read-only): SV5 iter_1 web machinery `closure_2026_11_06/SV5_growth_mechanism/sv5_web.py` and
`iter_1_law_on_web/sv5_iter1.json` (W1 line |r - 1| <= 3 sigma_A = 0.072; KA r 74.742402 / 89.362969); the SV5 solver
background (ob, od, h, H(z)); FA3 `fa3.json` S_host (largest uniform phantom weight with GB1 G1 PASS: 0.883 / 0.816);
SPARC rotmod files (`real_research/data/sparc_data`, max V_obs per galaxy); needed extra-mass fractions f over the law
from `closure_2026_11_06/SEED_2026_11_06.md` (SPARC <= 0.33 / 0.19; X-COP ~4.2 / 3.8; groups 1.2-3.5 / 0.9-2.9; M31
dSphs 1.64 / 1.50; Coma UDGs >= 23.6 / 20.2; CMB cold at z 3400, w <= 0.01). GB1 G1-G8 are the source of those class
needs. GB1 itself is not re-run: no class carries a velocity or defect feature, so by GB1's own rule every G row would be
NO VERDICT; the needs above are the graded form of those rows.

## Labels (per door, per footing)
- **DEAD BY REDUCTION**: the door's selector is shown (sympy) to be a function only of keys already on the dead list,
  and the reduced key fails the graded rows below.
- **DEAD**: an analytic kill with numbers (or the no-particle rule) on a row every reading must pass.
- **FAILS (rows)**: graded rows fail, no reduction shown.
- **SURVIVES (scoped)**: passes every graded row both footings; still owes field equations, causality, well-posedness.
- **NO VERDICT (rows)**: a KA fails, a MUTATE does not bite, or a needed input is missing.

## Door I5: disformal bulk-motion selector

**Action made definite.** Khronon phi, unit normal u_mu = d_mu phi / sqrt(X), X = -g^{mn} d_m phi d_n phi.
g~_mn = g_mn + B(X) d_m phi d_n phi = g_mn + B X u_m u_n. Two placements, both graded:
- P1 (Phase 1's text): baryons and photons minimally on g; the extra-gravity sector is weighted by F(Y), with Y any
  local scalar built from (g, g~, u, X) and the matter stress T^mn = (rho + p) U U + p g (fluid; collisionless matter
  coarse-grained to its mean velocity U and stress).
- P2 (TeVeS-like): matter (incl. photons) on g~.

**R (reduction, sympy, graded).** Enumerate the scalars: g~ mixed-tensor eigenvalues; g~(U,U); g~^{-1} contractions;
g~_mn T^mn; T^m_n T^n_m with g~; det g~ / det g. PASS (reduction shown) if every one is a function of
{gamma = -u.U, X, B, rho, p} only. Then F = F(gamma; X, p/rho): gamma = khronon velocity (QX5 iter_c reading 3, DEAD key);
p/rho = dead key (QX5 iter_b / record); X = clock depth (QX5 iter_a / QX6, DEAD). Also reported: the gamma-dependent part
of g~(U,U) is B X (v/c)^2 [1 + O(v^2)], i.e. DX1 D1's (v/c)^2 <= 1.1e-5 times B X.

**GW (graded).** Light cone of g~ in the khronon frame: c~ / c = sqrt(1 - B X) (sympy). P2: photons on g~, gravitons on
g, so |c_T - c_light| / c = 1 - sqrt(1 - B X); GW170817 (-3e-15 < dc/c < 7e-16, Abbott et al. 2017, PROVISIONAL) gives
|B X| <= 1.4e-15 (sign-dependent). The selector's argument then varies by <= 1.4e-15 x 1.1e-5 across all classes:
P2 FAIL (no order-1 switch). P1: photons and gravitons both on g, c_T = c_light: PASS (CONDITIONAL on no photon coupling
to g~).

**S (reduced key graded, both footings; reading A = F weights the dust, reading B = F weights the law's phantom).**
- Speed of a class's matter relative to the khronon frame (= the cosmic frame: matter reaches the khronon only at
  (v/c)^2, DX1 D1, so the khronon is not dragged): |V_flow + V_int|, sampled by Monte Carlo (seed 11, 2e5 per class).
  V_flow is common to all low-z hosts (all sit in the same web): 3D, each sample drawn from SV5's own linear velocity
  field at z 0.25 (mass-weighted cells; v_k = i a H f delta_k k / k^2, f from the field's own growth by finite
  difference). V_int, random direction (PROVISIONAL constants):
  SPARC: max V_obs of a random SPARC galaxy (on-disk rotmod); X-COP ICM: 3D Gaussian sigma_1D 200 km/s (turbulence);
  groups IGM: sigma_1D 100; M31 dSphs: sigma_1D 100 (orbit about M31); Coma UDGs: sigma_1D 1000 (Coma).
  CMB z 3400: speed uniform on [0, 30] km/s (generous upper; thermal protons ~15 km/s).
- Needs (generous windows on SEED): SPARC <F> <= 0.33 / 0.19; X-COP in [2.1, 8.4] / [1.9, 7.6]; groups
  [0.6, 7.0] / [0.45, 5.8]; M31 dSphs [0.82, 3.28] / [0.75, 3.00]; Coma UDGs >= 23.6 / 20.2; CMB >= 1 (generous; the
  solver's own od/ob is reported).
- **S1 sandwich (graded, F any monotone function):** first-order stochastic dominance (FOSD) read off the sampled
  speed CDFs. Increasing F: if SPARC FOSD CMB then <F>_CMB <= <F>_SPARC, so CMB >= 1 and SPARC <= 0.33 contradict.
  Decreasing F: if Coma UDGs FOSD SPARC then <F>_UDG <= <F>_SPARC, so >= 23.6 and <= 0.33 contradict. FOSD is graded
  as CDF_A(v) <= CDF_B(v) + 0.005 at every v on a 1 km/s grid. Both hold -> S1 FAIL (no monotone F) for reading A.
- **S2 LP (graded, no CMB row, increasing F):** linear program on a 25 km/s speed grid to 6000 km/s, F >= 0
  nondecreasing, the class windows above on the empirical samples. Infeasible -> FAIL; feasible -> reported with F and
  the row read as NO VERDICT (tail-dependent). Decreasing F is already closed by S1's UDG/SPARC leg.
- **W1 web (reading B, graded).** F multiplies W = (nu - 1) g_N per web cell, as a function of that cell's speed, at
  every SV5 ZG. G1 needs F = 1 on a fraction >= q of hosts, q = FA3 S_host per footing (generous: a binary F is harsher
  on G1 than a uniform weight). Host speeds = the z 0.25 web speed distribution (tracer reading). Most generous monotone
  F: increasing step F = 1[v >= v_(1-q)], decreasing step F = 1[v <= v_q] (quantiles of the z 0.25 mass-weighted
  speeds), applied at every ZG with that z's speeds. W1 PASS if |r - 1| <= 0.072. Both steps FAIL -> reading B FAIL W1.
  Reading A leaves the phantom untouched: W1 = KA1's r (FAIL as the plain law).

**I5 label:** DEAD BY REDUCTION if R passes and the reduced key fails S1 (reading A) and W1 (reading B), both footings;
P2 additionally FAIL (GW). FAILS (rows) if R fails but rows fail. SURVIVES only if some reading passes S1/S2 and W1.

**KA (KA FAIL = stop, nothing graded):** KA1: web code with F = 1 reproduces SV5 r to 1e-6 rel per footing.
KA2: F = 0 gives r = 1 to 1e-9. KA3 (sympy): g~(U,U) = -1 + B X gamma^2 and c~/c = sqrt(1 - B X). KA4: linear
velocity field parallel to g_N (mass-weighted cosine >= 0.999999).
**MUTATE (separate outputs, must bite):** M1: planted speeds reversed (CMB samples at 2000-2030 km/s, UDG sigma_1D 1 km/s
and no flow): S1 must lose both contradictions. M2: planted F = 1[v <= 1 km/s] on the web: W1 must PASS on both
footings (shows the web grader can see a pass). M3: a planted scalar Y = U.U_2 with a second, matter-independent
vector U_2 must fail R's reduction test (shows R can see a non-reduction).

## Door I7: defect network of the a0 scalar

**Action made definite.** O(N) scalar Phi_a, L = -(1/2) d Phi.d Phi - (lambda/4)(Phi.Phi - eta^2)^2, eta tied to the
a0 field's own scale: eta^4 = rho_DE c^2 (hbar c)^3, rho_DE = (a0 / (kappa c))^2 / G per footing (kappa = 1/2 FITTED).
N = 1 walls, N = 2 strings, N = 3 global monopoles (gauged: monopoles), N = 4 textures. Defects form by the Kibble
mechanism at T ~ eta (generous: T_c = eta, full thermal contact).

**Rows (graded per footing, analytic with numbers, sympy checks):**
- **D0 existence at z 3400:** 1 + z_form = eta / (k_B T0), T0 2.7255 K. FAIL if z_form < 3400 (no network at the CMB
  epoch, so zero extra gravity there).
- **D1 equation of state at z 3400 (line |w| <= 0.01)**, eta treated as free (generous, beyond D0):
  frozen (stretched) networks w = -1/3 strings, -2/3 walls; scaling networks (strings, global monopoles, textures)
  rho ~ 1/t^2, so w_def = w_tot (sympy from the continuity equation), w_tot(z 3400) from the solver's H(z) by finite
  difference; gauge monopoles w = 0 (non-relativistic).
- **D2 amplitude at z 3400**, need rho_def / rho_b >= 1 (generous; solver od/ob reported). Strings: rho_str / rho_m =
  6 pi zeta G mu / c^2 (matter-era scaling, zeta = 10 PROVISIONAL) at G mu / c^2 <= 1.5e-7 (CMB string bound,
  PROVISIONAL), and at the a0 value G mu / c^2 = pi (eta / E_Pl)^2. Walls: one wall per Hubble volume, delta T / T =
  (3/4) Omega_wall <= 1e-5 (PROVISIONAL) -> Omega_wall cap; and at the a0 value sigma = eta^3 / (hbar c)^2.
- **D3 cluster amplitude**, need 4.2 / 3.8 (X-COP): relativistic networks (rms speed ~0.5 c, PROVISIONAL) are not
  captured by cluster wells (escape ~ 0.01 c), so f_cl <= Omega_def / (rho_b,cl / rho_crit) with
  rho_b,cl / rho_crit >= 1e3 inside 300 kpc (Phase 1's 6e3 total, PROVISIONAL).
- **D4 no-particle rule:** gauge monopoles (the only w = 0 option) are particle-like: DEAD by rule.
- **D5 isotropy (walls):** the D2 wall cap is the isotropy bound itself; reported with D2.

**I7 label:** DEAD if every defect type fails D0, or fails D1 or D2 (and D3), or is a particle (D4), both footings.

**KA:** KA5: eta -> rho_DE -> a0 round trip to 1e-12. KA6 (sympy): rho ~ a^{-3(1+w)} with w = -1/3, -2/3 gives
a^{-2}, a^{-1}; rho ~ H^2 gives w_def = w_tot. KA7: solver w_tot at z 1e5 within 0.01 of 1/3 and at z 50 within 0.01
of 0 (the background behaves as radiation then matter).
**MUTATE (must bite):** M4: planted non-relativistic network (w = 0, rho_def / rho_b = od/ob, captured like dust): D1,
D2 and D3 must PASS on both footings (shows the rows can see a pass); its label must then be DEAD by D4 only.

## Outputs
`na1.py` -> `na1.json` / `na1.out`; `na1.py --mutate` -> `na1_MUTATE.json` / `na1_MUTATE.out`. RESULT.md gives the
door x row x footing table with margins read from the JSON and the peak RSS. Any change after this freeze is disclosed
in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
