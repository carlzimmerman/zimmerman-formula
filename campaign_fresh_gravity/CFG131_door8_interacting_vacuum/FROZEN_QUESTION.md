# CFG131 (Door 8: interacting vacuum) -- the frozen question and criteria

Written before any script or number in this directory (2026-09-29). The ten-door menu (closure_map/TEN_DOORS_GATES_2026-09-29.md) was written knowing the target
rho_c g_tot = a0 M_b(<r)/(4 pi r^3) (CFG44). Rule 1 asks for a commit before the first script; the orchestrator's instruction for this run is NOT to commit, so the file's
sha256 is printed at the top of every script output instead (a later edit changes the printed hash and is visible).

## The question (verbatim from the request)

Can an interacting-vacuum coupling, a conserved energy transfer Q between the vacuum (Lambda field of the HT sector) and the cold fluid, with Q a function of Lambda and
the fluid density only (no other field), produce the halo target rho_c g_tot = a0 M_b(<r)/(4 pi r^3) inside bound systems while leaving the linear cold behaviour (G2:
growth within 5% of LCDM to k = 30/Mpc; CMB unchanged) intact?

## Exact hypotheses (H) -- everything below is scoped to these

- H1 GR, and the vacuum stress is Lorentz invariant: T_vac^{mu nu} = -rho_L g^{mu nu}, rho_L = M_P^2 Lambda (the HT sector's stress).
- H2 The exchange is Q^mu = Q u_c^mu (energy transfer along the cold fluid's 4-velocity), with Q = Q(rho_L, rho_c) a scalar function of the two densities and nothing else:
  nabla_mu T_c^{mu nu} = +Q u^nu, nabla_mu T_vac^{mu nu} = -Q u^nu, total conserved.
- H3 The cold fluid is one irrotational perfect-fluid congruence with pressure p (dust p = 0 is the limit); baryons are a second pressureless fluid coupled only through gravity.
- H4 No other field, no gradient of rho_c in Q, no momentum-transfer component (Q^mu has no piece orthogonal to u).

Not tested (stated up front): a vacuum with a non-Lorentz-invariant stress; Q^mu with a spatial piece or derivative dependence on rho_c or the metric; a collisionless
(anisotropic-stress) cold component beyond the fluid limit; nonlinear collapse; a Boltzmann-code CMB run (G2's CMB clause is checked only through the background and the
growth equations, and is labelled so).

## What is derived (the deliverables)

1. The covariant conservation equations with Q = Q(Lambda, rho_c), and their consequence for the vacuum gradient (D1).
2. The background evolution, whether Lambda stays a constant, and a0(z) (D2).
3. The linear perturbation equations for delta_c with Q and the growth ratio to LCDM in CFG43's two-fluid solver conventions (D3).
4. Whether Q(Lambda, rho_c) can depend on the enclosed baryon mass M_b(<r), argued from locality and tested against the target's required equation of state (D1).
5. The reaction on baryons (G3) and the constant count (G4) (D4).

## Pre-declared pass/fail lines (mine; the shared G1-G5 are not weakened)

- G1 PASS iff ONE relation p = p(rho_c) (plus at most a global Lambda that is the same in every halo at the same epoch) makes the hydrostatic target hold within 10% in the
  required pressure at matched density for point masses of 1e9, 1e10, 1e11, 1e12 Msun and for the exponential sphere, over x in [0.1, 30]. Equivalent statement: the
  required p at fixed rho_c must not depend on M_b by more than 10%.
- G2 PASS iff the total-matter growth ratio to z = 0 (CFG43 conventions: two fluids, Omega_c = 0.265, Omega_b = 0.050, start z = 1000, delta = a) is >= 0.95 at k = 0.5, 2, 10,
  30 /Mpc for the Q-consistent cold fluid.
- G3 PASS iff the reaction on baryons <= 0.10 g_law over x in [0.3, 30] and the energy the mechanism must supply <= the baryons' orbital energy (M_b V_c^2/2 per baryon
  mass). The energy that this door supplies is evaluated by the vacuum energy needed for any cold mass beyond the cosmic share (Omega_c/Omega_b) M_b, which does not depend on r_ta.
- G4 PASS iff no constant beyond kappa = 1/2 and Omega_c h^2 = 0.12 is needed (a constant tied to Lambda or kappa in the same action does not count).
- G5 PASS iff no ghost or gradient instability (c_s^2 >= 0 and real) and Solar System safe by an explicit statement.
- The flat-a0(z) law is kept iff |a0(z)/a0(0) - 1| < 1% for z <= 5 (the record's standing).

## Controls (MUTATE) that must change the headline

- MUTATE=1: give the equation of state a hand-fed dependence on the enclosed baryon mass (the postulate the door was supposed to avoid). G1 must flip to PASS (so the test
  can pass, and the failure is due to the locality hypothesis). Exit code 1 (the headline "G1 FAIL" is contradicted).
- MUTATE=2: give the vacuum a momentum of its own (drop H1: rho_L allowed a spatial gradient). The dust structure theorem must fail. Exit code 1.
- MUTATE=3 (growth script): force delta rho_com = 0 not to be imposed, i.e. drop the constraint and evolve dust with Q_rho != 0 as if free. The growth ratio must
  return to LCDM (contradicting the derived collapse of growth). Exit code 1.
Declared control failures are kept and disclosed.
