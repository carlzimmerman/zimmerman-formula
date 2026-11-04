# FROZEN A31: dark energy and dark matter that exchange energy over time, or are one fluid

Frozen before any A31 number. Script `scripts/recipe33.py`, output `scripts/recipe33.out`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Known before freezing, from the record only: A15 U1 (`recipe17.out`): plain LCDM NFW central acceleration g = 2 pi G rho_s r_s on the SPARC SHMR halos, median 0.612 a0, kappa_eff 0.306, spread 0.156 dex. A20 (`recipe22.out`): constant coupling Q = xi H rho_v reaches kappa_eff 0.47 to 0.54 at xi -0.60 to -0.50 but its flat ratio kappa_eff(z)/kappa_eff(0) is 0.73 to 0.85 (drift); constant Q = xi H rho_c with xi -0.40 to -0.175 keeps the flat ratio inside 0.05 dex but kappa_eff stays 0.31. No A31 number has been computed.

Question: can a time-varying coupling, a running vacuum, or a unified dark fluid make the halo acceleration scale track rho_DE, a(z) = kappa c sqrt(G rho_DE(z)) with kappa 1/2, at galaxy radii?

## Gates (same for every route; tolerances fixed now)

- G1 kappa_eff = median_i g_i / (c sqrt(G rho_DE0)) within 0.05 dex of 0.5 (rho_DE0 = the model's own vacuum or dark-energy density today).
- G2 slope d ln a / d ln rho_DE0 = 0.50 +- 0.05, least squares over five cosmologies f = rho_DE0/rho_DE0,base in {0.5, 0.71, 1, 1.41, 2}, physical omega_m and omega_b held (the A26 C1 footing), coupling knobs held, primordial amplitude held (footing P below), M200 from the fixed SHMR.
- G3 a(z)/a(0) at the median M200 inside [0.76,1.03], [0.71,1.12], [0.33,1.21] at z 1, 1.5, 2.33.
- G4 one constant: rms of log g_i over the 171 SPARC hosts <= 0.1 dex (primary, as A20 K4); also reported over log M200 11 to 12.5 (secondary, as A26); the verdict uses the primary.
- G5 operative at galaxy radii: halo gravity passes by definition (A13); a fluid pressure force must be inward (adds to gravity) and >= 0.1 a0 at the last measured SPARC radius.
- GT tracking (new, frozen here): |log10[a(z)/a(0)] - 0.5 log10[rho_DE(z)/rho_DE(0)]| <= 0.05 dex at z 1, 1.5, 2.33, in each model's own evolving rho_DE (for the couplings, rho_DE = rho_v). This is A20's K2.
A route supplies the tie only if G1, G2, G3, G4, G5 and GT all pass at one knob setting.

## Machinery for (a) and (b) (recipe22 generalised)

Flat, no radiation, base H0 67.4, Om0 0.315, Ob0 0.0493 today (today's densities are the observed ones, units of base rho_crit0). Baryons a^-3 conserved. Prime = d/d ln a. rho_c' = -3 rho_c - Q/H, rho_v' = +Q/H. Background integrated backward from a = 1 to a = 1e-3 by fixed-step RK4 (2000 steps in ln a); perturbations forward from a = 1e-3 with delta_c = delta_b = u = 1e-3. Geodesic dark matter (energy transfer along the dark matter 4-velocity, no momentum transfer), vacuum homogeneous in that frame: delta_c' = u + q delta_c, q = Q/(H rho_c) - deltaQ/(H rho_c delta_c); delta_b' = u; u' = -(1 + dlnH/dlna) u + 1.5 (rho_c delta_c + rho_b delta_b)/E^2, dlnH/dlna = -1.5 (rho_b + rho_c)/E^2. Derived here, not checked against a paper; treated as from memory.

Two growth footings, both reported: S8 (primary for G1, G3, G4, GT, as recipe22): D normalised to 1 today in both the model and the LCDM reference (sigma8 held today). P (primordial amplitude held; the only footing for G2): raw D, equal in all models at a = 1e-3. Early transfer-function changes from a changed early rho_c are ignored (stated; as recipe22).

Concentration mapping (recipe22, Ludlow-style C = 400, from memory): z_f^LCDM from the base Diemer19 c; model z_f from 1/D_m(z_f) - 1/D_m(z) = 1/D_L(z_f^L) - 1/D_L(z); rhobar_s = C rho_crit,m(z_f); c solves 200 rho_crit,m(z) c^3 mu(1)/mu(c) = rhobar_s on c in [1.5, 60] (clipped values counted). rho_crit,m physical (E^2 in base units, so f != 1 rows carry their own h). g = 2 pi G rho_s r_s. M200 per galaxy from lib's SHMR at M_* = 0.5 L (unchanged). Control: zero coupling returns recipe22's control (0.612 a0, kappa_eff 0.306), and the xi1 = 0 rows of Q_v must reproduce recipe22's Q2 rows (xi -0.6, -0.5) to 0.002 in kappa_eff.

Models with rho_c <= 0 anywhere on [1e-3, 1] or rho_v < 0 below z 10 are skipped and counted.

### (a) Time-varying coupling, xi(a) = xi0 + xi1 (1 - a)

- Qc: Q = xi(a) H rho_c (xi > 0: dark matter decays into vacuum). deltaQ = Q delta_c, q = 0.
- Qv: Q = xi(a) H rho_v. deltaQ = 0, q = xi rho_v/rho_c.
- Qm: Q = xi(a) H rho_c rho_v/(rho_c + rho_v). deltaQ = Q delta_c rho_v/(rho_c + rho_v), q = xi rho_c rho_v/(rho_c + rho_v)^2.
Grid, frozen: xi0 and xi1 each in {-1.0, -0.9, ..., +1.0} (21 x 21 = 441 per form, 1323 points). Knobs: 2 per form (xi0, xi1) plus the choice of form (discrete). Plausible range (from memory, not verified, PROVISIONAL): constant-coupling fits to CMB+BAO allow |xi| of order 1e-3 to 1e-2 for Qc and of order 0.1 to 0.5 for Qv; a hit outside is reported as such.
Imposed, not derived: the form of Q, the sign and size of xi0, xi1, the energy-transfer frame. Derived: background, growth, concentrations, g.

### (b) Running vacuum (Sola et al. type, PROVISIONAL from memory)

rho_vac(H) = rho_vac0 + (3 nu/8 pi G)(H^2 - H0^2), exchange with cold dark matter only (baryons conserved). Then rho_v' = nu (E^2)' and (E^2)' = -3 (rho_b + rho_c), so Q/H = rho_v' = -3 nu (rho_b + rho_c). Vacuum homogeneous: deltaQ = 0, q = -3 nu (rho_b + rho_c)/rho_c. Grid, frozen: nu in {-0.30, -0.29, ..., +0.30} (61) plus {+-1e-4, +-3e-4, +-1e-3, +-3e-3}. Fitted values in the literature are nu ~ 1e-4 to 1e-3 (PROVISIONAL, from memory). Knobs: 1 (nu). Imposed: the H^2 running and the exchange partner; derived: the rest.

For (a) and (b): every point is graded on G1, G3, G4, GT on footing S8, and G2 on footing P; joint pass also checked with G1, G3, G4, GT on footing P. Reported per form: pass sets of G1, GT, G1 and GT jointly, all gates jointly; the minimum of J = (log10(kappa_eff/0.5)/0.05)^2 + sum_z (GT_z/0.05)^2 with all its gates; for the min-J point, the law swap a = g_i per galaxy graded by lib.grade (E1 <= 0.02, E2 <= 0.04, E3 <= 0.02), diagnostic only. "Does a time-varying coupling cure A20's drift" is answered by: is there any (a) point passing G1 and GT jointly, and how its G2, G3, G4 read.
Expected in advance: G1 and GT can be brought together by some (xi0, xi1) in Qv or Qm at large |xi| (two knobs, two targets at one mass), outside the plausible range; G4 fails everywhere (0.15 dex spread untouched); G2 fails (physical footing slope well below 0.5, as A26 C1 +0.25). RVM at plausible nu is LCDM to 1e-3: kappa_eff 0.31, G1 fails; at large |nu| no joint pass.

## (c) Unified dark fluids

(c1) Generalised Chaplygin gas, P = -A/rho^alpha (rho the dark-sector mass density, P/c^2). rho(a) = [A + B a^-3(1+alpha)]^(1/(1+alpha)). With alpha = 0 it is LCDM, so A_s = A/rho_0^(1+alpha) = Omega_v/(Omega_c + Omega_v) = 0.7205 (derived from base, held for all alpha). Pressure matters (w = -1/3) at rho_* = rho_0 (3 A_s)^(1/(1+alpha)). For each SPARC host, take its U1 NFW halo (base Diemer19 c, SHMR M200) as the fluid's clustered part: report rho at r_s and at the last measured radius, over rho_*, and w there. Pressure-gradient acceleration a_P = -grad P/rho = -c_s^2 dln rho/dr, c_s^2 = alpha A_s c^2 (rho_0/rho)^(1+alpha), at the last radius; sign (outward for alpha > 0). alpha in {1e-5, 1e-3, 1e-2, 0.1, 0.5, 1}. Gates on a_P: G1 median |a_P|/(c sqrt(G rho_DE0)), rho_DE0 = A_s rho_0 ... = Omega_v rho_crit0; G4 rms of log |a_P|; G2 analytic, a_P at fixed halo density goes as A, i.e. as rho_DE0^(1+alpha); GT with rho_DE(z) = -P(z)/c^2 = A/rho(z)^alpha, a_P at fixed halo constant in z; G3 then 1; G5 needs inward and >= 0.1 a0. Also the native combination c sqrt(G rho_*), graded G1, and G5 judged (it is not a force at galaxy radii; it is a T2-type coincidence). Structure-formation bound |alpha| below about 1e-5 (Sandvik et al. 2004, PROVISIONAL, from memory). Knobs: 2 (A, alpha), A fixed by Omega_v.
Expected: halo densities exceed rho_* by 1e4 to 1e7, w there of order -1e-5 or smaller; a_P outward and far below 0.1 a0 at the allowed alpha: G5 FAILS. c sqrt(G rho_*) gives a T2-type coincidence, G5 fails.

(c2) Logotropic dark fluid (Chavanis type, "dark matter that becomes dark energy", PROVISIONAL from memory): P = A ln(rho/rho_P), rho_P = c^5/(hbar G^2) the Planck density; dark-energy part of the energy density rho_DE c^2 = A [ln(rho_P/rho_m) - 1] with rho_m the rest-mass density (a^-3). A = B rho_DE0 c^2, B = 1/(ln(rho_P/rho_c0) - 1), rho_c0 = Omega_c rho_crit0 (derived; the Planck density is an added constant, hbar, stated). Halo of the fluid in hydrostatic equilibrium (dark fluid only, baryons not included in the profile): logotropic Lane-Emden, theta' = -theta^2 m/xi^2, m' = xi^2 theta, rho = rho_0 theta, r = r_0 xi, r_0 = sqrt(A/(4 pi G rho_0^2)); hence rho_0 r_0 = sqrt(A/(4 pi G)) is universal and g(r) = sqrt(4 pi G A) m/xi^2. kappa_eff(xi) = sqrt(4 pi B) m(xi)/xi^2, reported at the maximum of g, at the asymptote and at r_h (theta = 1/4). Gates: G1 at the maximum (most generous) of g, others reported; G2 analytic (A at fixed B scales as rho_DE0, slope 0.5 exactly at fixed rho_c0); G3 a(z)/a(0) = 1 (A constant); GT with the logotrope's own rho_DE(z); G4 by construction (one A for all hosts); G5 halo gravity, by definition. Diagnostic, frozen: per SPARC galaxy one knob r_0 (171 knobs), g = g_b + g_logo(r/r_0), no adiabatic response, fitted to the law curve in log; lib.grade E1 to E3 reported; also the halo surface density Sigma_0 = rho_0 r_h against 141 Msun/pc^2 (Donato et al. 2009, PROVISIONAL). Knobs: A (set by rho_DE0, 0 extra), hbar (added constant), per-galaxy rho_0.
Expected: G2, G3, GT, G4 pass by construction (A is a constant tied to rho_DE by the model's own equation), but G1 fails: kappa_eff about sqrt(2 pi B) = 0.15 at the asymptote, a factor near 3 low; and g tends to a constant at large r (rho ~ 1/r, rising curves), so the law's shape fails E1 even with 171 knobs.

## Not run, stated

Momentum-transfer couplings (elastic DM-DE scattering), coupled quintessence with a field (A14 T8: a G rescaling, no scale), RVM with an H-dot term, GCG non-adiabatic perturbations, any hydrodynamic or N-body run of the coupled models.

## RESULTS (written after the run; criteria above unchanged)

Runtime 7 s, peak RSS 423 MB, single thread. Line numbers refer to `scripts/recipe33.out`. No bug found; no wrong output exists.

Controls: zero coupling returns 0.612 a0, kappa_eff 0.306 (l.3); Qv xi1 = 0 reproduces recipe22's Q2 rows exactly, 0.539 and 0.465 (l.6). No concentration or formation-epoch clipping anywhere (l.1157).

(a) Time-varying coupling, frozen 21 x 21 grids. No point passes G1 and GT together on either footing, and no point passes all gates (l.233-236, 648-651, 1109-1112).
- Qc: 223 of 441 skipped (rho_v < 0 or rho_c <= 0); kappa_eff never reaches G1 (best GT-passing 0.337); G2 slope +0.08 to +0.12; G4 0.152 to 0.166 (l.227-238).
- Qv: G1 at 33 points, GT at 14, never together. Best G1-passing row (-0.5, +0.1) kappa_eff 0.450 with GT -0.087 (l.317); best GT-passing kappa_eff 0.388 at (-0.5, +0.7) (l.323); min-J (-0.6, +0.8) kappa_eff 0.418, GT -0.070 (l.653). G2 -0.21 to +0.26; G4 0.146 to 0.159 (l.652).
- Qm: G1 nowhere on the grid; GT at 65 points; best kappa_eff 0.354 (l.1114).
- Footing P (primordial amplitude held) is worse: kappa_eff falls to 0.1 to 0.27 at the same points (e.g. 0.245 at l.317).
- Answer to the lane question: on the frozen grid, letting the coupling vary in time does NOT fix A20's redshift drift at the coupling where kappa_eff is 0.5. The two pull against each other, as in A20. Law swap at the min-J points: E1 0.055 to 0.070 (l.241, 656, 1117).

(b) Running vacuum: valid only for -1e-3 <= nu <= 0.08. Below that, rho_v < 0 below z 10. Above it, rho_c goes negative at high z (checked after the run, rho_c min at z 999). At literature |nu| <= 3e-3 kappa_eff is 0.305 to 0.309, i.e. LCDM (l.1156). kappa_eff peaks at 0.405 at nu = 0.08 (G1 FAIL); G2 +0.08 to +0.18; G4 0.143 to 0.156; GT passes at nu 0.04 to 0.08 (l.1134-1150). No joint pass.

(c1) Generalised Chaplygin gas (l.1160-1166). The pressure matters only near rho_* = 1.5 to 2.2 rho_0. Halo densities at the last SPARC radius are about 1.4e4 rho_0, which is 6e3 to 9e3 rho_*, and w there is -5e-5 or smaller. The pressure-gradient force always points OUTWARD for alpha > 0, so it opposes gravity: G5 FAILS at every alpha. Its size is 2.8e-3 a0 at the allowed alpha 1e-5. For alpha >= 1e-3 it reaches or exceeds a0, which is incompatible with the halo being in place, and alpha that large is excluded (provisional bound). G4 0.36 to 0.75; G2 slope 1 + alpha. G1 passes in size only at alpha 0.5 (0.56), a coincidence: the force is outward and spread 0.54 dex. The native combination c sqrt(G rho_*) gives kappa_eff 1.43 to 1.73: G1 fails, and G5 fails as a T2-type coincidence.

(c2) Logotropic fluid (l.1169-1180). B = 3.533e-3 (derived from the Planck density). The halo acceleration is universal, g -> sqrt(2 pi G A), and it carries the tie by the fluid's own equation: G2 0.500, G3 1, GT residual under 0.003, G4 0, G5 halo gravity. But kappa_eff = 0.151 at the maximum of g (-0.521 dex): G1 FAILS by a factor of 3.3. Sigma_0 = 131.6 Msun/pc^2, near the provisional 141. With one r_0 per galaxy (171 knobs) the law fit fails, E1 0.104: g tends to a constant, so curves rise.

Post-result diagnostics, NOT gates, not frozen (`scripts/recipe33_diag.py`, `recipe33_diag.out`, `recipe33_diag2.py`, `recipe33_diag2.out`). A continuous minimax off the grid finds Qm at xi0 +2.18, xi1 -7.6 passing G1 (0.476), GT (residuals within 0.023) and G4 (0.082). It still fails G3 (a(z 2.33)/a(0) 1.63, because its rho_v triples by z 2.33, so tracking and the band disagree) and G2 (+0.24). On footing P it fails everything. Its universe has Omega_v 0.31 at z 10, H 30 % below LCDM there, and xi running from +2.2 today to -5.4 early, far outside any plausible range. Law swap E1 0.031. Off-grid minimax for Qv and Qc stays at 0.070 and 0.106 dex.

Verdict: NO ROUTE supplies the tie. Couplings and the running vacuum: no joint G1 and GT on the frozen grids, and G2 fails everywhere. The only off-grid G1 + GT + G4 point fails G3 and G2 and needs an extreme early-dark-energy history. GCG: pressure is outward and negligible, so G5 fails. Logotrope: the tie's form appears by construction, but G1 is a factor of 3.3 low and the curve shape fails.

Knobs, derived vs imposed. (a) 2 knobs plus the choice of form, with the coupling imposed. (b) 1 knob, with the running imposed. (c1) 2 knobs (A from Omega_v, alpha). (c2) 0 knobs beyond rho_DE0, but it adds hbar and an imposed log equation of state; Sigma_0 universality is derived, kappa ~ sqrt(2 pi B) is derived, and it is wrong by 3.3x. Inherited: Ludlow C = 400, Diemer19, SHMR, geodesic frame.

Deviations: diagnostic scripts added after the run (above). Secondary G4 (log M200 11-12.5) is 0.071 to 0.082 in every (a)/(b) row, so it passes everywhere. The verdict uses the primary, and the secondary changes nothing because G1 and GT never pass together on the grid. PROVISIONAL from memory: Ludlow C, coupling and nu ranges, the GCG alpha bound, Chavanis B, Donato Sigma_0.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## Correction, 4 November 2026 (after A32)

`scripts/recipe33.py` copied A20's growth equation with the wrong damping term, -(1 + d ln H/d ln a) in place of -(2 + d ln H/d ln a); its own control printed LCDM D(z=1) 0.4517 against colossus 0.6068. Fixed and rerun, with `recipe33_diag.py` and `recipe33_diag2.py` (which load recipe33's code). Wrong outputs kept as `*_before_growth_fix.out`.

After the fix, on the frozen grids: still no point passes G1 and GT together in any form, and no point passes all gates. G2 slope ranges become Qc +0.112 to +0.169, Qv +0.094 to +0.561, Qm -0.020 to +0.180. Running vacuum at literature nu (<= 3e-3) gives kappa_eff 0.304 to 0.312, still LCDM; its best point moves to nu 0.05 with kappa_eff 0.459, failing G2 (+0.212) and G3. The unified-fluid rows do not use the growth code and are unchanged. Post-result off-grid diagnostic: the Qm minimax point is now xi0 +1.574, xi1 -5.563, kappa_eff 0.470 with GT within 0.027 but G4 0.113 (fails), again at a coupling far outside any plausible range. Verdict unchanged: no tie.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
