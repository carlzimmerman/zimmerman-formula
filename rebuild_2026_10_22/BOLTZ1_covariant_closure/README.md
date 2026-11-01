# BOLTZ1_covariant_closure: NEEDS A SELECTED LAGRANGIAN. A dust-limit P(X) exists with a0 out of it, adds nothing beyond RF5's top cell, and cannot hold RF5's turn-on

Criteria `FROZEN_CRITERIA.md` (e7bc4064fa, alone first). Script `boltz1.py`; numbers `boltz1_part.json`, `cells/R1_inf*.json`; twin `boltz1_part_MUTATE.json`. kappa = 1/2 FITTED, unused. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework. v3s not reopened. No download. Queue item 11; the source text's hi_class proposal is not adopted, since no Lagrangian is selected for it to run.

| Part | Label | Key number |
|---|---|---|
| A | **NO TURN-ON IN P(X)** | unified c_s^2 = -(dlnS/dln a)/3 < 0 across the step at all 14 grid z_on; mean dP/drho -1.54, width 0.05 |
| B | **CEILINGS ONLY, NO PINCER**; **PRESSURE CORE EXCLUDED IN THIS FAMILY** | mu floors /Mpc: forest 56.6, crossing 2.04e4, BBN 1.24e8; R(mu_BBN) 0.025 pc |
| C | **DUST LIMIT PASSES GATES, FOREST NOT DIAGNOSTIC** | S 2324.13 (S - S_min 0.10); forest 424.0/327, p 2.4e-4 |

## What RF5's cell computes
CLASS 3.3.4, patched only in the background and the cold continuity equation. rho_c = rho_c0 a^-3 S(a), tanh in ln a, width 0.05, fed by a w = -1 reservoir that does not cluster; released mass is born with delta Q = 0 on synchronous slices. Cold w = 0, c_s = 0, geodesic. DE is a CPL fluid with PPF. No Lagrangian lies behind it, and no a0 enters at linear order. It computes a timing question, not an action.

## Does a covariant L exist for N's cold component with a0 out?
For the cold linear limit, yes: L = P(X), shift symmetric, in the limit K = mu^2 (Q-1)^2, mu -> infinity. No a0 and no new number; the abundance is an integration constant (G16 stays open). On comoving slices its linear equations are CLASS's cold equations. That identification is analytic; no field was evolved in CLASS.
What it does not reach (record, not redone):
- **The zooms.** A single-valued phi can't cross streams. It folds (DR2 N1, X14), so N's native profile isn't this L's prediction past the first caustic.
- **S_cold(M) = f_c eta(M_t) Sigma_coll(M_t).** M_t, eta and the hand-set core are not local functions of this field. G11, G13 stay open.
- **The law.** The a0 law's only worked covariant sector is the v3s family, closed by the owner. That verdict also calls a separate dust a double count in galaxies.

## Part A: the turn-on isn't in P(X)
For a healthy branch, d(rho a^3)/dln a = -3 P a^3 and dP/drho >= 0. rho a^3 can rise only with P < 0, and it must then reach P = 0 at lower rho, which needs dP/drho < 0. Treated as one fluid, RF5's step has c_s^2 from about -1.3e-5 to -13.3 at every grid z_on. So z_on isn't a parameter of any single healthy P(X).
Limits: this is one barotrope. Two sectors, or a shift-breaking potential, are outside it. Such a scalar (frozen, w = -1, then oscillating dust) would give a turn-on, with its mass playing z_on: a new number, and particle-like, against the standing rule. Not run. P(X)'s rest-frame c_s^2 also has no k in it, so the source's c_s^2(k, a) needs something beyond P(X).

## Part B: crossing against growth
For K = mu^2 (Q-1)^2 at Q - 1 << 1: c_s = sqrt(4 pi G rho)/mu, proper k_J = mu, n = 1 polytrope radius pi/mu.

| floor on mu | /Mpc | z where Q - 1 = 1 |
|---|---|---|
| Forest, X22 c_s <= 6 km/s at z = 3 | 56.6 | 5.4e3 |
| Crossing proxy, pi/mu <= epsilon(1e8) = 154 pc | 2.04e4 | 2.8e5 |
| BBN, Q6's arithmetic | 1.24e8 | 9.2e7 |

At mu_BBN: c_s 9.4e-6, 1.9e-3, 0.019 km/s at 200 rho_crit, 1, 100 Msun/pc^3. At the crossing floor: 0.057, 11.4, 114 km/s.
These all bound c_s^2 from above, so c_s^2 -> 0 meets all of them and the comparison can't fail. Any floor would have to come from curing caustics or holding a core. X14 finds the first needs a new constant. The second fails here: 0.025 pc against kpc cores. The crossing line is a proxy of this lane's choosing, and a pressure-free coarse profile is not the same as true crossing. The BBN line holds for this quadratic form only; DBI (Q7) removes it, and that is another selected form with its own number.
The stiff branch is P(X)'s only early departure, and it has the opposite sign to RF5's: more early mass above a^-3, not less.

## Part C: z_on = infinity through RF5's harness
RF5's binary with the turn-on off, its fit, scale cut and forest recipe unchanged.

| | infinity | RF5 1e6 |
|---|---|---|
| plik /605, p | 581.78, 0.74 | 581.67, 0.75 |
| BAO /13 | 9.65 | 9.73 |
| SN | 1629.52 | 1629.53 |
| xi+ /101 points | 103.13, p 0.40 | 103.2 |
| S | 2324.13 | 2324.18 |
| sigma8 | 0.8252 | 0.8260 |
| forest /327 | 424.0, p 2.4e-4 | 420.1, p 3.8e-4 |
| V-Fbar | 1519 | 1618 |

Fit: h 0.6750, Omega_m 0.312, w0 -0.816, wa -0.651. G-A0 passes (sqrtX 1.003, 0.946, 0.853). The two footings share this surface; native a0 wasn't re-read here. The start point was already near the minimum, so this reads the same as the top cell, at a higher Delta S of 0.10 against S_min (grid 3e5).

**RF5's open pointer is answered.** RF5 said the forest's true edge "could lie above 1e6". Removing the turn-on gives no further fall: the climb 420, 555, 2548 stops at 1e6, so 1e6 is already the dust limit. G0's failure isn't a remnant of turn-on; it fails on plain early dust, narrowly, with z 4.4 near the per-z line (p 0.0020) and joint p 2.4e-4. This matches P1D4's V-hiz. The forest stays out of any verdict. A pass here means early dust and says nothing about galaxies.

## Can a new run decide anything?
No. mu -> infinity is this cell. A finite-mu run needs a chosen form and mu, and every line above is one-sided. hi_class would add no new test without a chosen L.

## Decision needed (owner)
Selecting a Lagrangian means choosing three things together:
1. **Law sector:** which covariant a0 sector, given v3s is closed. Either a named successor, or leave the law without an action.
2. **Cold sector and double count:** a separate P(X) dust beside the law, accepting the v3s verdict's double-count objection, or a single-field route.
3. **Past the first caustic:** a multi-stream completion (X14's C8, particle-like, against the standing rule), or a new constant, or accept the zooms as an effective rule with no action.
A turn-on would add a fourth choice (a potential and its mass), and RF5 gives no reason for it.

## Checks and twin
K1 plik, BAO, SN at RF5's 1e6 best fit, max |d| 6e-11. K2 forest table z 3.6, |d| 0. K3 patched off vs vanilla, 0.0. K4 mu_BBN, relative 1e-8 against Q6 (uses C7's fitted omega as Q6 did, tool check only, in no grade). K5 sympy all 0. K6 7e-8. All pass.
MUTATE: m1 pressure sign fails S2 and N1 (label flips to TURN-ON ALLOWED); m2 a^-3 fails K4 (no root); m3 turn-on on at 1e4 fails K3 (0.91). All bite.

Disclosed: not blind; the expectation in the criteria held, with forest 424 just above its 400-420 range. The first `algebra` run stopped on a path-parsing fault in the K4 input, before any number; fixed. The shear cut is RF5's file, copied. Part B has no CLASS run. Nothing else lanes own was edited.
