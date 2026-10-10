# CFG544 FROZEN CRITERIA -- kinetic consistency of class-A settling (CFG541 open item 5)

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-09.

## Scope and settings

CFG541 (criteria 09e5d0a18, results a6c4c4e6f) wrote class A as Vlasov + a velocity-independent drift,
d_t f_c + div_x[(v + v_s) f_c] - grad Phi . grad_v f_c = 0, v_s = -alpha 1_B 1_C tau grad psi, lap psi = 4 pi G d,
d = 1_B 1_C max(rho_ph - rho_c, 0). Open item 5: the drift moves cold energy in position only (velocities kept), so nothing
makes the settled cold energy's velocity distribution the collisionless (Jeans) equilibrium of rho_ph in the law's potential
(SIS: sigma^2 = V_f^2/2; CFG461: no G9 mechanism sets the temperature); the one-sided deficit never removes an overfill; F is a
Lyapunov function of the drift sub-flow only. This lane tests whether the settled state is kinetically consistent, and whether
a forced fix with no new constant exists. CFG539/541/542 folders are read only (never edited). No PM runs. No downloads.
Compute: `nice -n 10`, <= 2 threads.

Settings: kappa = 1/2 FITTED; footings 9.3603e-11 (can) and 1.1312e-10 (alt), judged separately, never pooled; kernel
nu(y) = 1/(1 - exp(-sqrt y)); candidate B; G9; no EFE (round per-region phantom, CFG541 E7); f_b = 0.02237/0.14237. The cold
energy's MASS is still required. No dark-matter particle species. Not "theory closed". Energy sink (CFG541 S): heating the cold
energy beyond the Jeans value is excluded; the only allowed exchange is with dynamical, non-clustering dark energy.

**No knobs.** alpha = 1 (CFG541: O(1) FREE, not tuned here), tau = (4 pi G rho_m)^(-1/2). Any fix may use only G, the local
state, rho_ph (already a class-A input) and alpha, tau. A fix that needs another constant is NOT a fix (knob).

## Systems (inputs read from `CFG541_cold_energy_equations_precise/cfg541_results.json`, read only)

- MW-like: M_b = 6.0e10 Msun, Hernquist a = 2.5 kpc, f_ret, r_ta, r_* (= `r_analytic_kpc`, exhaustion radius) per footing.
- Cluster-like: point mass 1.5e14 Msun, f_ret, r_ta, r_* per footing.
- 2 systems x 2 footings = 4 cells. M_cat = 5.364 M_b/f_ret. Code units: r_*, V_f = (G M_b a0)^(1/4), G = 1.

## Analytic items (sympy)

- **K1 (moments of E3).** Derive the second-moment equation of E3 in 1-D/1-V. PASS (as a statement of fact) if the drift
  enters only as advection of sigma^2 (no compression-heating term in d sigma^2/dt along u + v_s): then the settled cold
  energy carries its source dispersion. For CFG541's reservoir at rest this gives sigma = 0 after drift-only settling.
- **K2 (equilibrium target).** sigma_eq(r): isotropic Jeans of rho_ph in the law's field, truncated at r_*
  (P(r_*) = 0). Control C1: untruncated, sigma_eq^2/V_f^2 -> 1/2 in the deep regime to within 2%.
- **K3 (fix structure).** For each fix term: first variation, gradient-flow form, mass conservation, and dF/dt sign.
  Full-system Lyapunov (Vlasov + drift [+ relaxation]): test the candidates F, E (Newtonian energy), E - T S, and E_law - F;
  label **ESTABLISHED** only if sympy proves dL/dt <= 0 for all states for some L; else **NOT ESTABLISHED** (cross terms shown).

## Toy model (numerics)

Spherical N-body shell code (no PM): N = 30000 cold-energy particles, each (r, v_r, v_t); static baryons; Newtonian
self-gravity of the cold energy through M(<r) with Plummer-type softening eps = 0.01 r_*; reflecting inner boundary 1e-3 r_*.
Vlasov step: kick-drift-kick, L = r v_t conserved. Class-A drift step: rho_c, rho_ph, d on 100 log bins from 1e-3 r_* to r_ta,
grad psi = G M_d(<r)/r^2, v_s = -alpha tau grad psi inside r_ta, applied at fixed (v_r, v_t) (so L changes, as in CFG541);
numerical limiter |v_s dt| <= 0.5 bin width (fraction of limited moves reported). Static (non-expanding) background, like the
CFG541 1-D toy. Fixed step dt = 1e-3 r_*/V_f (MW-like), 5e-4 (cluster-like). Seeded RNG (seed 544).

Initial states:
- **IC-B (infall):** cold energy uniform inside r_ta at rest (CFG541's reservoir), with a small isotropic dispersion
  0.05 V_f to avoid exactly radial orbits (disclosed numerical choice). Run 10 Gyr.
- **IC-C (class-A settled, as delivered):** rho_c = rho_ph inside r_*, velocities = source (reservoir at rest; same
  0.05 V_f). Run 5 Gyr.
- **IC-E (equilibrium):** rho_c = rho_ph inside r_*, isotropic Maxwellian with sigma_eq(r) of K2 in the toy's softened field.

Diagnostics (shell S = 0.1-0.9 r_*): X = sum m v^2/3 / sum m sigma_eq^2(r_i) over particles in S (anisotropy-free virial
measure); D = median over 16 log bins in S of log10(rho_c/rho_ph); s(r) = sigma^2/sigma_eq^2 per bin (diagnostic);
steadiness = change of log10 X and of D over the last 2 Gyr; edge r_99 (radius enclosing 99% of the cold energy) vs the
analytic r_99 of rho_ph truncated at r_*.

**Kinetic gate (per cell, per run):** |log10 X| <= 0.1 AND |D| <= 0.1 at the end, AND both changed by <= 0.05 dex over the
last 2 Gyr.

## Q1 -- as is (CFG541 class A: one-sided deficit, no velocity term)

Runs: IC-B 10 Gyr and IC-C 5 Gyr, one-sided. Report sigma(r) vs sigma_eq(r), X, D; the sign (contract / puff up);
the time at which |D| first exceeds 0.1 for IC-C; T1 equality (rho_c = rho_ph) held or broken. Roundness itself cannot be
tested in a spherical toy (disclosed).
**KINETICALLY CONSISTENT (as is)** iff the kinetic gate passes for IC-B and IC-C in all 4 cells; otherwise not.

## Q2 -- fixes (declared now, before any number)

- **FIX-1 (primary): two-sided deficit**, d = 1_B 1_C (rho_ph - rho_c), same mobility, same alpha, tau; no new term, no
  constant. Its F = (1/8 pi G) int |grad psi|^2 is smooth with dF/drho_c = psi (to be confirmed, K3). Mechanism to test:
  a cold settled halo contracts, the overfill is pushed back out at fixed velocity, so infall-and-return cycles can raise
  the dispersion until Jeans balance; a hot halo is pulled in at fixed velocity and cools.
- **FIX-2 (secondary): FIX-1 + velocity relaxation** on B∩C at rate alpha/tau, Ornstein-Uhlenbeck toward an isotropic
  Maxwellian with sigma_J^2(r) = (1/rho_c) int_r^inf rho_c g dr' (Jeans dispersion of the CURRENT cold-energy density in the
  current field). No constant, but the target temperature is a closure (posited, not derived): reported as such.
- **ALT-S (thermodynamic, diagnostic only):** Smoluchowski drift v_s = -alpha tau grad(Phi + T ln rho_c) with T = V_f^2/2
  (the phantom's deep temperature; an inserted functional of the baryons). Has the Lyapunov function E - T S. Test: its
  stationary isothermal profile (self-consistent baryons + cold energy, mass M_cat inside r_ta) vs rho_ph and vs r_*.
  It is reported, never adopted, and gives no label.

Runs: FIX-1 and FIX-2 on IC-B (10 Gyr) and IC-C (5 Gyr), all 4 cells.

**Energy bookkeeping:** the energy exchanged with the sink = -(work of the drift + work of the relaxation), cumulative, per
M_cat in V_f^2; gross in and out reported, and the rate over the last 2 Gyr. COMPATIBLE with CFG541's sink iff the net
exchange at the end is an outflow (>= 0) and <= 1.0 V_f^2 per M_cat (so CFG541's cosmic bound stays negligible).

**Labels:**
- **CONSISTENT WITH FIX** iff FIX-1 passes the kinetic gate on IC-B and IC-C in all 4 cells, mass is exact, overfill is
  HANDLED, Q3 holds (UNCHANGED), and the energy is COMPATIBLE. FIX-1 is derived (gradient flow of a named F, no constant).
  The full-system Lyapunov result (K3) is attached to the label either way.
- **INCONSISTENT (named)** otherwise. If FIX-2 passes where FIX-1 fails, the name is "needs a posited velocity closure"
  and FIX-2 is reported as a candidate, not adopted.

## Overfill

IC-E plus an injected excess of 0.3 M_ph(<0.3 r_*) inside 0.3 r_* (rho_ph-shaped, sigma_eq velocities). Each run is paired
with a baseline from IC-E without the injection under the same rule. Persistence P = [excess M_c(<r_*) - M_ph(<r_*)]
(injected run minus baseline) / injected mass, at 5 Gyr. One-sided rule and two-sided rule (FIX-1), both with no velocity term.
**HANDLED** iff P <= 0.2 under FIX-1 AND P >= 0.5 under the one-sided rule (the persistence must be shown, not assumed);
**NOT HANDLED** if FIX-1 gives P > 0.2. If the one-sided rule itself gives P < 0.5 the label is reported with that fact.

## Q3 -- invariance of CFG541's edge and stationary profiles

(a) 1-D drift-only finite-volume model (CFG541's setup re-implemented: reservoir at rest, static baryons, 400 log cells), one-
sided vs two-sided: steady r_* and stationary profiles; (b) N-body FIX-1 IC-B end state: r_99 vs analytic.
**UNCHANGED** iff (a) |ln(r_*,two/r_*,one)| <= 0.01 and max |rho_two - rho_one|/M_cat-weighted <= 1e-3 inside r_*, AND
(b) |ln(r_99/r_99,analytic)| <= 0.1 in all 4 cells; else **CHANGED** (amount reported).

## Controls (must pass, else the toy is not trusted and no Q label is issued)

- C1: deep SIS sigma_eq^2 = V_f^2/2 within 2% (K2).
- C2: IC-E evolved by pure Vlasov (no drift) for 2 Gyr passes the kinetic gate (end-state part) in all 4 cells.
- C3: in that run |Delta E/E| <= 1e-2.
- C4: M_ph(<r_*) of the toy equals M_cat (CFG541 JSON) to 1e-4; particle mass conserved exactly in every run.

## MUTATE (`CFG544_MUTATE=1`, writes `_MUTATE` outputs, exit 1 if all teeth bite)

- MV: IC-E with velocities randomised at settling (sigma^2 x 2), pure Vlasov 2 Gyr: must FAIL the kinetic gate (|D| or
  |log10 X| > 0.1) in all 4 cells.
- MO: overfill run with FIX-1 replaced by the one-sided rule: P must exceed 0.2 (NOT HANDLED).
- MT: FIX-2 with the OU target sigma_J^2 x 2 on IC-C: must FAIL the kinetic gate.

## Reporting

`cfg544.py` -> `cfg544.out`, `cfg544_results.json`; MUTATE -> `cfg544_MUTATE.out`, `cfg544_results_MUTATE.json`;
`README.md`. Every number quoted from the JSON. Corrections after this commit are dated disclosures; this text is not edited.
