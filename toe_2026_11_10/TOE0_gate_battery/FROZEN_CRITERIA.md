# TOE0: a swing at a theory of everything, as one frozen gate battery (2026-11-10)

Owner, 2026-11-10: "swing for TOE we have enough research that this isnt an unreasonable request".

TEST battery, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11 m/s^2)
and alt (1.1312e-10 m/s^2), never pooled. The cold component is cold dark energy (the clock's charge), never a particle.
Not a LCDM lane. No download. Committed alone, before any lane of this battery writes a script or a number.

Id check: no `TOE0`, `QG1` or `HZ1` folder exists (`find . -maxdepth 3 -type d -name 'TOE0_*'` etc. empty) and
`git log --oneline -i --grep='^TOE0'` / `QG1` / `HZ1` give nothing.

## 0. What is being swung at

The candidate is the record's adopted form: action (A) of QX17
(`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md` section 0), with rules 3 to 5 of
`closure_2026_11_10/THEORY_ASSEMBLED_2026-11-10.md`, plus the Standard Model as the matter action S_m. A theory of
everything is read in two senses, and both are graded:

- **Strong sense:** one action from which gravity, the dark sector AND the matter content (gauge group, three families,
  masses, alpha) follow with no fitted number.
- **Weak sense:** one action that holds gravity, the dark sector and the Standard Model (as input), is a consistent
  quantum theory with a UV completion, and fixes its own dark-sector constants.

## 1. The six gates

Each gate gets one label: **PASS**, **FAIL**, **OPEN** (not computed, or computed with no verdict) or **WALLED** (a
standing record no-go with a named reason, quoted, not re-run). A lane of this battery freezes its own detailed criteria
before its scripts. It may tighten a gate's numbers here; it may not loosen them.

**T1. Classical completeness.** One action whose solutions give GR in strong fields, the law in galaxies, the cold
component in the CMB and growth, and the joint (a falling clock becoming a standing one) as a solution, not a rule.
Read from the record at collection time. PASS needs a landed lane that derives the joint inside an action and meets the
seven conditions of `THEORY_ASSEMBLED_2026-11-10.md` section 4. Otherwise OPEN (or FAIL if a landed lane closes the last
named route). The lanes running on it when this file was written: AK1, CLS1, GRW1 (and DT2's line). This battery
launches nothing on T1.

**T2. Quantum health of (A) as an effective field theory.** Lane QG1 (`toe_2026_11_10/QG1_quantum_health_of_A/`).
On each background of the list below, both footings:
- (i) no ghost (every propagating mode has a positive kinetic term) and no gradient instability (no mode with
  omega^2 < 0 growing with k at large k; a Jeans-type growth slower than H on a cosmological background is allowed);
- (ii) the strong-coupling scale Lambda_s of the canonically normalized fluctuations satisfies Lambda_s * L >= 10,
  with L the shortest length on which the theory is used there;
- (iii) one-loop corrections (graviton and khronon loops, and matter loops), cut off at min(Lambda_s, M_Pl), shift a0 by
  at most 10 % and mu(x) by at most 0.1 anywhere in 0.01 <= x <= 100.

Backgrounds and L: Minkowski (L = 1 mm, laboratory gravity); FRW at z = 1100 and z = 1 (L = 10 Mpc comoving); a static
point mass M_b = 6e10 M_sun in the law, at the radii where x = g_N/a0 = 1e-2, 1 and 1e2 (L = 1 kpc), and at 1 AU from
the Sun (x about 6e7, L = 1 AU). PASS needs (i), (ii) and (iii) on every background and both footings. Null points
(g -> 0) are reported with the size of the region where (ii) fails, not graded.

**T3. A UV completion.** Lane HZ1 (`toe_2026_11_10/HZ1_uv_completion/`).
- (i) A stated UV action, power-counting renormalizable under its own scaling (every coupling of non-negative scaling
  dimension), whose IR limit gives (A)'s field equations with the law's mu(x) to within 0.1 on 0.01 <= x <= 100, the
  law's function either present in the UV action or computed (not asserted) to arise in the flow;
- (ii) the Lorentz violation it percolates into matter at one loop (photon speed, SME c-type coefficients of p, n, e)
  stays under current bounds for some window of its UV scale M_*;
- (iii) that window is non-empty together with |c_T - 1| <= 1e-15 (GW170817) and the solar-system and pulsar limits the
  record already passes.
PASS needs (i), (ii) and (iii). Reported, not part of the PASS: whether the UV fixes kappa or the 5.41, and whether its
higher-derivative terms resolve COL1's fold into a standing clock.

**T4. The dark-energy value.** rho_DE (equivalently Lambda, equivalently a0 through a0 = kappa c sqrt(G rho_DE)) derived
with no fit. Read from the record: leg (iv) "VALUE of Lambda = GAP" (June TOE path), KDE1 (2026-11-10: ALREADY IN THE
RECORD AS AC2s). QG1's (iii) also reports whether matter loops break the relation Lambda = 32 pi a0^2 / c^4 (the
cosmological-constant problem carried into a0); that report is placed here.

**T5. The matter content.** Gauge group, three families, masses, alpha, derived. Record: WALLED on three named reasons
(W1 flavor-blindness, W2 number field, W3 the 30-order scale gap; `real_research/TOE_POSITS_LEDGER_2026-06.md`), all on
the June actions. Graded item **TOE0-S** below asks whether action (A), which postdates those walls, changes W1.

**T6. The constants.** kappa and the cold share 5.41 derived with no fit. Record: both FREE (11-03 kappa closure; R541
note, `closure_2026_11_10/R541_why_the_cold_share/NOTE.md`). Graded item **TOE0-P** below tests the one route R541 set
aside as a total derivative.

**Verdict rule.** TOE (strong sense) only if T1 to T6 all PASS. TOE (weak sense) only if T1, T2, T3, T4 and T6 PASS,
with T5 allowed WALLED. Anything else is **NO TOE**, reported as the closest assembled candidate scored gate by gate.
Stated before any lane runs: T5 is WALLED going in unless TOE0-S finds otherwise, so the strong sense cannot pass in
this swing; the weak sense is what the lanes can move.

## 2. TOE0-S (graded here): does action (A) reopen the flavor wall?

W1 says the gravitational sector is blind to species because matter couples to it universally. Read (A) as printed in
QX17 section 0 and its metric equation E4: list every term in which a matter field appears.

- **WALL STANDS** if matter enters only through S_m[g, psi] (couples to the metric alone; tau, P and lambda absent from
  S_m). Then W1 holds for (A) exactly as for the June actions, and T5 stays WALLED.
- **WALL REOPENED** if any matter field couples to tau, P or lambda, or the coupling differs between species. Then T5 is
  OPEN and the coupling's equivalence-principle cost is reported against MICROSCOPE (eta below about 1e-15).

Hand expectation: WALL STANDS (rule 1 of THEORY_ASSEMBLED says matter couples to the metric only).

## 3. TOE0-P (graded here): can the clock make its own charge together with the baryons?

R541 lists three untested ways to fix the 5.41 and sets one aside: "Coupling the current to baryon number is a total
derivative and does nothing." That is true only while baryon number is conserved. With a B or B-L violating process in
equilibrium it is the spontaneous-genesis coupling (Cohen-Kaplan type), and it ties the clock's charge to the baryons.
Candidate: add to (A), for X = B (sphaleron era) or X = B - L (a lepton-number-violating era),

    L_c = c_X  d_m tau  J_X^m ,       c_X a constant of dimension mass.

**P1 (identity, sympy).** The clock's equation of (A) + L_c is the conservation of the total shift current,
nabla_m [ rho_Q n^m + (polarization flux) + c_X J_X^m ] = 0, so in FRW with P = 0:
d(a^3 rho_Q)/dt = - c_X d(a^3 n_X)/dt. Graded: the symbolic Noether current of the dust term plus L_c equals
rho_Q n^m + c_X J_X^m with rho_Q = mu_K^2 (Q - 1)/K (QX17 E3's dust part). PASS if the difference simplifies to 0.

**P2 (sign, sympy + mpmath).** In unitary gauge (tau = t, N = 1) L_c = c_X n_X, a chemical potential mu_X = c_X Q for X.
With the violating process in equilibrium the plasma relaxes to n_X(mu_X), and n_X(mu) has the sign of mu for any
stable plasma (dn/dmu > 0). So the change of the clock's charge, -c_X n_X(c_X Q), is never positive.
Graded on exact Fermi-Dirac and Bose-Einstein number densities (massless and massive, m/T in {0, 1, 5}, mu/T over
[-0.5, 0.5] on a fixed 41-point grid, g = 1, both signs of c_X):
- **DRAINS** if c_X n_X(c_X) >= 0 at every grid point (the clock can only lose charge to the plasma);
- **CREATES** if any grid point gives c_X n_X(c_X) < 0;
- UNDECIDED otherwise (numerical failure).

Label of TOE0-P: **CANNOT FIX 5.41** if P1 PASS and P2 DRAINS (the route can only lower the clock's charge, so a
positive 5.41 still needs a primordial charge: one free number remains). **CAN FIX 5.41 IN PRINCIPLE** if P1 PASS and
P2 CREATES (then the follow-up is a numerical lane with eta_B as the second number). Otherwise NO VERDICT.

Reported, not graded: the c_X that would move 5.41 rho_b of charge (c_X = 5.41 m_p in magnitude, since
Delta rho_Q = -c_X Delta n_X) and the baryon asymmetry that same c_X would give at sphaleron freeze-out
(T about 130 GeV) with the massless-fermion susceptibility, against eta = 6.1e-10 (n_B/n_gamma); and the drain the
observed eta implies.

**Known answers (must pass before any graded line is read):**
- KA1: the Noether current of the dust term alone is L_K'(Q) n^m = mu_K^2 (Q-1)/K n^m (QX17 E3, dust part).
- KA2: the massless Fermi-Dirac asymmetry is exactly g (mu T^2/6 + mu^3/(6 pi^2)); the numerical integral must match it
  to 1e-12 relative at three mu values.
- KA3: with X conserved (no violating process), d(a^3 n_X)/dt = 0 and the clock's charge is unchanged: R541's
  "does nothing" is reproduced.

**MUTATE twins (must bite):**
- M1: flip the sign of the susceptibility (a plasma with dn/dmu < 0). P2 must read CREATES.
- M2: drop c_X J_X from the current. P1 must FAIL.

Hand expectation: P1 PASS, P2 DRAINS, so CANNOT FIX 5.41. The clock is a rolling field; a rolling field that drives an
asymmetry pays for it out of its own charge (the second law), so it cannot make a positive cold share from nothing.

## 4. Collection

`toe_2026_11_10/TOE0_gate_battery/RESULT.md` places every gate's label with its lane and commit, after QG1 and HZ1 land
(or after a stated cutoff, with OPEN for a lane still running), re-runs each lane's main script before quoting it,
and opens with the verdict in one sentence. kappa = 1/2 FITTED; not theory closed.
