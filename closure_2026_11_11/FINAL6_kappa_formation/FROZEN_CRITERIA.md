# FINAL6 FROZEN CRITERIA: is kappa an OUTPUT of the formation reading? (2026-11-11)

FINAL MILE, lane **FINAL-6 (KAPPA)**. TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
Footings never pooled (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2). Cold dark energy is a gravitating
field component; no particle is added anywhere. **kappa = 1/2 FITTED; not theory closed.** This lane edits nothing
outside its own folder.

**Lane id.** The brief names this lane FINAL-6 (KAPPA). Short id on files: **FINAL6**. Checked free: no
`closure_2026_11_11/FINAL6*` exists; no commit subject on any branch names FINAL6, FINAL-6 or kappa_formation.
Siblings consulted, not redone: FINAL2 (EPOCH, which event), FINAL3 (share derivation), FINAL4 (GROWTH, the history the
formation reading gives, R_set = r_ta), NPJ1 (nine non-perturbative sectors), ROOT/HZ1/QG1 (why the law is not a
fundamental term).

Committed alone, before any FINAL6 script exists and before any FINAL6 number is computed.

## 0. The question

The record's normalisation is

    a_0 = kappa * c * sqrt(G * rho_DE),      kappa = 1/2 adopted.

FINAL4 takes the formation reading as a derivation: the charge-to-baryon share is fixed at the assembly event by the law
at the formation field, X = X_L(g_{b,f}), and is conserved afterwards. That fixes the *amount*. It does not touch the
*normalisation*.

This lane asks the further question, in one line:

> Under the formation reading — the amount is fixed at the event and the law's normalisation is set by that event —
> is kappa an output? Does a_0 follow from the formation physics, and does 1/2 come out?

Two parts, graded separately, because they are likely to have different answers:
- **Q1 (form).** Does the formation reading output the *form* a_0 ∝ c sqrt(G rho_*), and pick which rho_*?
- **Q2 (coefficient).** Does it output the dimensionless number 1/2?

## 1. Conventions

SI throughout unless a line says eV. G = 6.67430e-11, c = 2.99792458e8.
Background (Planck 2018 TT,TE,EE+lowE+lensing): H0 = 67.36 km/s/Mpc, Omega_m = 0.3153, Omega_Lambda = 0.6847,
Omega_b = 0.0493. Derived, printed once: rho_crit,0 = 3 H0^2/(8 pi G), rho_Lambda = Omega_Lambda rho_crit,0,
rho_m,0 = Omega_m rho_crit,0, f_cdm ≡ Omega_c/Omega_b = 5.3640, f_b ≡ Omega_b/Omega_m.
E(z) = sqrt(Omega_m (1+z)^3 + Omega_Lambda), rho_crit(z) = rho_crit,0 E(z)^2, rho_m(z) = rho_m,0 (1+z)^3.
Footing tie (the record's own, never pooled): rho_ref = 4 a0^2/(c^2 G) for kappa = 1/2; H_Lambda = sqrt(8 pi G rho_ref/3);
Z ≡ c H_Lambda / a0 = sqrt(32 pi/3) = 5.78881.

**The formation reading F (this lane's operational definition).**
- **F1 (amount).** The settled charge-to-baryon ratio of a mass element is fixed at its assembly event and conserved
  thereafter: X = X_L(g_{b,f}) with X_L(y) = (sqrt(1 + 4 a_0/g_b) − 1)/2 (FINAL4/PD1: X = 59.4861 can / 59.5029 alt).
- **F2 (normalisation).** The a_0 that enters the law is the value the formation datum gives:
  a_0 = kappa * c * sqrt(G * rho_*(z_f)) with rho_* the cosmic density whose value the event imprints.
- **F3 (universality — empirical, not derived).** One a_0 fits the RAR sample; the two footings differ by
  0.5 log10(1.1312/0.93603) = 0.0411 dex, which this lane uses as the observationally allowed non-universality.

**Dimensionless formation data (all that F makes available).**
delta_c = 1.686 (spherical-collapse linear threshold), Delta_v = 178 (virial overdensity, ~18 pi^2),
f_cdm = 5.3640, f_b = 0.15636, Omega_Lambda/Omega_m = 2.1716, X ≈ 59.49/59.50. Any derived kappa must be a function
of these alone.

## 2. The graded items

**K1 — dimensional closure (exact; sympy nullspace).** Take the dimensionful inputs the formation event offers,
{G, c, rho_*} plus the host baryon mass M, and solve for every monomial G^a c^b rho^g M^m with the dimension of an
acceleration. Claim: the solution space is one-dimensional,
(a, b, g, m) = (3g − 1, 4 − 6g, g, 2g − 1), i.e. a_0 = c sqrt(G rho_*) * w^p with w ≡ G M sqrt(G rho_*)/c^3
(dimensionless) and p any rational. **K1 PASSES iff the nullspace is exactly 1-dimensional and m = 0 forces p = 0**,
i.e. c sqrt(G rho_*) is the unique mass-independent member.
*Consequence, recorded: universality (F3) forces the FORM a_0 = kappa c sqrt(G rho_*). That Q1 gain is real. It says
nothing about kappa.*

**K2 — what the two footings are (numerical).** For each footing compute
kappa_foot = a_0 / (c sqrt(G rho_cosm)) with rho_cosm = rho_Lambda (Planck) and rho_crit,0:
- Reading A (the record's tie): rho_ref = 4 a0^2/(c^2 G); verify rho_ref/rho_Lambda and rho_ref/rho_crit,0.
- Reading B (the fitted values taken as data): kappa = a_0,fit/(c sqrt(G rho_Lambda)) etc.
**K2 PASSES iff, under Reading A, |kappa − 1/2| <= 0.005 on BOTH footings and the two footings' kappa differ by
<= 0.001** — i.e. the two a0 values are two *conventions* over one posited kappa, **not two measurements of kappa**.
(Reported, never graded: the kappa each footing would need if the *other* footing's density were the cosmic one.)

**K3 — the pure-number requirement.** Under F2 + F3, kappa = Phi(dimensionless formation data). Grade by exhaustion
over a **frozen finite list** of closed forms in {delta_c, Delta_v, f_cdm, f_b, Omega_Lambda/Omega_m, X, pi}:
`1/delta_c`, `1/(2 delta_c)`, `f_b`, `sqrt(f_b)`, `1/f_cdm`, `1/sqrt(f_cdm)`, `(Delta_v/18)^(1/3)` (=2),
`delta_c/Delta_v * 100`, `3/(4 pi)`, `1/(2 pi)`, `sqrt(3/(8 pi))`, `1/2` (the claim itself), `X^{-1/2}`,
`X^{-1/2}*delta_c/2`, `Omega_Lambda/Omega_m/4`, `f_cdm*f_b`, `delta_c^2/(2 pi^2)`, `sqrt(3/32)`, `3/5` (virial),
`1/(2*sqrt(2))` (acceleration-epoch reading).
**K3 PASSES for a route iff |Phi − 1/2| <= 0.025 (5 %) AND the route's Phi is derived, not asserted.**
The scan is reported in full; no item added or dropped after the run.

**K4 — the matching condition (the one quantitative output of the reading).** Take F2 with rho_* = rho_m(z_f) — the
background matter density the freezing element sees. The fitted a_0 then requires
rho_m(z_f) = a_0^2/(kappa^2 c^2 G) = rho_ref * (1/2 kappa)^2... in the record's own units: with kappa = 1/2 this is
exactly rho_ref. So each footing implies a required freeze-out redshift

    1 + z_f = ( rho_ref / (Omega_m rho_crit,0) )^{1/3} ,      and  kappa = 1 / (2 sqrt(beta)),  beta ≡ rho_m(z_f)/rho_Lambda .

Compute z_f per footing, and compare it with FINAL2's six candidate epochs and with matter–Lambda equality
z_L = (Omega_Lambda/Omega_m)^{1/3} − 1. **Consistency test (not a derivation):** PASS iff 0 <= z_f <= 3.
**Sensitivity (graded):** beta defined by acceleration onset (rho_m = 2 rho_Lambda) instead of equality gives
kappa = 1/(2 sqrt 2) = 0.3536; report the shift against the footing spread 0.0411 dex. **K4 FAILS as a derivation**
iff the shift exceeds the footing spread (it is a restatement otherwise).

**K5 — universality refutes the two routes that set the scale from the halo itself.** Both keep F1 and F2 but take
rho_*, or the scale, from the forming halo rather than from cosmology.
- **R-A (internal-acceleration route).** From the BTFR and virial equilibrium, a_0 = f_b^{-1} * G M_vir / R_vir^2
  (exact algebra; printed). With M_vir = (4 pi/3) Delta_v rho_crit(z) R_vir^3 this gives
  a_0 ∝ (G M_vir)^{1/3} (G rho_crit(z))^{2/3} * Delta_v^{2/3} (4 pi/3)^{2/3} / f_b — i.e. **∝ M_vir^{1/3}**.
- **R-B (catchment-saturation route).** The paper's own budget identity solved the other way: the settled region
  exhausts the catchment supply, R_set = R_c with M_b = (4 pi/3) R_c^3 rho_b, giving
  a_0 = f_cdm^2 (4 pi/3)^{2/3} G M_b^{1/3} rho_b^{2/3} — also **∝ M_b^{1/3}**.
  (Uses FINAL4's R_set = (1 + X) r_M only through the same identity; X enters neither A nor B.)
Compute both a_0(M) at M_b = 1e8, 1e10, 6e10, 1e12 Msun (baryonic), their spread in dex, and their absolute
ratio to the fitted a_0. **Grade REFUTED iff either the predicted spread > 0.5 dex OR the absolute ratio to the
fitted value misses by more than 0.5 dex, on either footing.** The observed allowance is the footing spread 0.0411 dex.

**K6 — the cosmic-budget closure is vacuous (reported).** Show algebraically that the integrated statement
"total phantom mass = f_cdm × total baryons" is an identity once f_cdm is *defined* as the cosmic cold-to-baryon ratio:
it contains no kappa. Print the identity and report VACUOUS. Not used for a label.

**K7 — the discriminator the reading does supply (reported).** Under F2, a constant rho_* = rho_Lambda makes a_0
epoch-independent; rho_* = rho_crit(z) (the alt footing's density) makes a_0(z) = a_0(0) E(z). Print E(z) and the implied
a_0(z)/a_0(0) at z = 0.3, 0.5, 1.0, 2.0, 6.0, per footing, and cite FINAL2's bound on any a_0(z). Reported, not graded
(FINAL2's own verdict stands).

## 3. Known answers (each must pass)

- **KA-1.** Z = c H_Lambda/a_0 reproduces sqrt(32 pi/3) = 5.78881 to 1e-4 on BOTH footings (the record's tie).
- **KA-2.** rho_ref(can)/rho_Lambda(Planck) = 1 to within 2e-3, and rho_ref(alt)/rho_crit,0 = 1 to within 2e-3 — i.e. the
  canonical footing is the Lambda-only density and the alt footing is the total (critical) density. Printed to 6 digits.
- **KA-3.** R_set from FINAL4, R_set = (1 + X) sqrt(G M_b/a_0), reproduces FINAL4's r_ta at M_b = 6e10 Msun to 1e-6
  relative, both footings, using PD1's X.

## 4. MUTATE (each must bite, on both footings)

- **MU1.** Replace kappa = 1/2 by kappa = 1 in F2's matching condition: the required rho_* drops by 4 and the implied
  z_f must move below 0 (into the future) by more than 0.05.
- **MU2.** Compute the canonical footing's kappa against rho_crit,0 instead of rho_Lambda: |kappa − 1/2| must exceed 0.05.
- **MU3.** Drop F3: allow the mass-dependent monomial p = 1/3 in K1's family. The predicted a_0 across the four
  decades 1e8 -> 1e12 Msun must then spread by more than 0.5 dex.

## 5. Labels

- **KAPPA DERIVED.** Some route outputs kappa with no free dimensionless input and |kappa_out − 1/2| <= 0.025 on both
  footings.
- **KAPPA NOT DERIVED (FITTED).** No route outputs kappa; kappa = 1/2 remains an input. The formation reading may still
  output the FORM (Q1) and must say so.
- **KAPPA REFUTED (FORMATION).** Additionally: the formation reading, taken per-galaxy (each element freezing at its own
  assembly epoch), is excluded by the universality of the RAR — print the excluded spread.
- **OPEN** if any known answer fails or a numerical step fails.

Lane label = the conjunction that the printed numbers support. The default expectation, stated before the run, is
**KAPPA NOT DERIVED (FITTED)** with Q1 = FORM OUTPUT and Q2 = NO. A negative answer is a real result, not a failure.

## 6. Scope

Dimensional analysis, the prescription's own budget identity, the BTFR/virial algebra, and a flat-LambdaCDM background.
No new data, no data download, no CLASS run, no refit of a_0, no new sector, no Lean claim beyond what is proved inline.
Literature attributions PROVISIONAL.
