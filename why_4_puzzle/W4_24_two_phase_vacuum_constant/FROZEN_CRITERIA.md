# W4-24: the vacuum constant in the two-phase action (frozen criteria, committed alone)

**Status: FROZEN 2026-11-09, before any W4-24 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Audit lane. It asks one question that the 2026-11-03 closure (`KAPPA_CLOSURE_2026-11-03.md`, K840) could not ask, because
the action did not exist then: in the two-phase action, where a switch multiplies the law's Lagrangian, is the vacuum
constant still a free zero mode, and if part of it becomes physical, does that part tie a₀ to ρ_DE?
**κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095; not used upstream of any result). Not theory closed. Adopts nothing.

## Inherited (paths; read before freezing, nothing computed)

- **I-a. The zero mode.** `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` (K205): in a local classical
  action a constant can be added to the law's sector, so a₀ and Λ decouple. Rule S6 rests on it.
- **I-b. The slot.** K010 and K014 (`sonnet55_push/puzzle_32pi/p09…`, `p13…`): "dark energy = the vacuum value of the
  a₀ sector" is a slot, W_v = 4 at κ = ½, with nothing fixing it.
- **I-c. The switched class.** `fable52_push/SWT1_switch_theorems/FROZEN_CRITERIA.md` (4d86f4d107), weak field:
  L = −|∇Φ|²/(8πG) + S·J(|∇Φ|) − ρΦ, J(g) = (a₀²/4πG)[u − ln(1 + u)], u = g/a₀, 0 ≤ S ≤ 1, J(0) = 0.
- **I-d. The wall pressure.** SWT1 T3 (same file; certified in `SWT1.lean`): at fixed displacement y = g_N/a₀ the outward
  force per unit area on the carrier across a wall where S falls from 1 to 0 is
  p_wall = ∫₀¹ J(u(S, y)) dS = (a₀²/4πG)·W(u₁), W(u) = u − ln(1 + u) − u²/(2(1 + u)²), u₁ = ν(y)·y,
  ν(y) = ½ + √(¼ + 1/y). Known answers: `fable52_push/SWT1_switch_theorems/swt1.json`, block KA_W1.
- **I-e. The filling allowance.** SWT1 T2 (`RESULT.md`, 5d93ad2ad9): law-on regions may fill at most f = 0.0231 of space.
- **I-f. The disc gate.** HE1 G1 (`fable52_push/HE1_held_out_envelope/FROZEN_CRITERIA.md`, 0e67f3c64a): a wall must sit
  at R_w ≥ 10 r_M, i.e. y ≤ 1/100.
- **I-g. The relativistic action as frozen.** `fable52_push/TPA1_two_phase_action/FROZEN_CRITERIA.md` (b81c28d00c):
  L/√−g = [R − 2Λ]/(4K) + L_K(Q) + S(n_d)·Lam_law + λ n·P + L_m, with W(p) = (a₀²/K)[−p/a₀ − ln(1 − p/a₀)].
  Λ sits outside the switch and W(0) = 0. W4-24 reads that file only; it does not touch TPA1's folder or wait for its result.

## Mechanism and hypotheses

Split the vacuum constant in two: L ∋ −V_out − S·V_in.
- V_out is outside the switch. It is I-a's zero mode and stays free.
- V_in is inside the switch. It is the energy-density difference between the law-on phase (S = 1) and the law-off phase
  (S = 0), so it is a pressure step on every wall.

**Claim C1 (to be checked, K1).** The same integral as I-d gives the net outward wall pressure
p_net = p_wall − V_in = (a₀²/4πG)·[W(u₁) − Ξ], with Ξ = 4πG·V_in/a₀².

**Hypothesis H1 (named, added).** Dark energy is the switched constant: V_in = η·ρ_DE c², with a₀ = κ c √(G ρ_DE) the law's
definition of κ. Then Ξ = 4πη/κ² (K2). Branches:
- η = +1: dark energy lives in the law-on phase (V_out = 0).
- η = +1/f: the same, with the cosmic mean matched (law-on regions fill f of space).
- η = −1: dark energy lives in the law-off phase (V_out = ρ_DE c², V_in = −ρ_DE c²); the law-on phase is the lower one.
- η = 0: the action as frozen in I-g.
- Continuous η is a TRADE (S6: nothing names its value) and is reported only as the largest |η| the gates allow.

## Inputs, footing, declarations

- **Inputs:** G, c, ρ_DE, κ, η symbolic. Pure numbers: 4π from Poisson's equation (I-c), the two gate values of y, f from
  I-e, and three dispersions (100, 300, 1000 km/s) for K4. No a₀ value, no measured κ, no measured density ratio, no H₀.
- **Footing:** ρ_DE, declared. The other footing is not used. The window W_data = [0.227, 0.607] (rules §7) enters only the
  final comparison lines, after every bound is computed.
- **Option space Ω:** the route outputs **no κ**. It outputs lower bounds κ_min per branch and gate. p_exact = 0; it adds no
  determinate trial to P_LEE. Register class `audit`, family VM. It cannot produce an EXACT CANDIDATE: wall equilibrium
  gives inequalities.
- **π-parity:** κ_min² = 4π|η|/W(u₁(y)); one π over a transcendental number. Not a value.
- **ħ:** absent. Classical.

## Entry screen (rules §3), stated before computing

- **S1** c enters through the vacuum energy ρ_DE c² acting as a pressure. Cleared.
- **S2** The bounds depend on κ through Ξ ∝ 1/κ². K4 (η = −1) is κ-independent and is labelled as such.
- **S3** In n space dimensions Poisson's coupling is Ω_{n−1}G, the wall unit is a₀²/(Ω_{n−1}G), W(u) keeps its form (it
  follows from μ = u/(1 + u) alone), and κ_min² = Ω_{n−1}|η|/W. The gates are stated in y. Nothing is special at n = 3.
- **S4** Second predictions: for η > 0 the law is off wherever y < y*(κ), W(u₁(y*)) = Ξ, so the radial acceleration relation
  would be Newtonian below y* (tested by the record's SPARC gate; no data read here). For η < 0 the law-on phase fills space
  (tested by I-e).
- **S5** Not a reparametrisation of κ; η is declared a TRADE when continuous.
- **S6** **Expected to fail as a derivation:** the two-phase action fixes only V_in, and the hand estimate says it fixes it
  to about zero. V_out stays free.
- **S7** H1 is the K010/K014 slot. The lane does not match energies at g = a₀; it tests whether the slot survives the switch.
- **S8** ρ_DE is read locally at each epoch.

## Checks (`w4_24.out`; light, single core, sympy and mpmath, seconds)

- **K1. Wall pressure with the constant.** (a) Quadrature of ∫₀¹ J(u(S, y)) dS, with u(S, y) the positive root of
  (1 − S/(1 + u))·u = y, equals W(u₁) to 1e-8 relative at y = 1e-4, 1e-2, 1/3, 1, 3, 100, 1e4. (b) The closed form equals
  `swt1.json` KA_W1 "closed" at that file's six y values to 1e-10 relative. (c) Symbolic: ∫₀¹ [J − V_in] dS = p_wall − V_in.
- **K2. Ξ.** Symbolic: with a₀ = κ c √(G ρ) and V_in = η ρ c², V_in/(a₀²/4πG) = 4πη/κ².
- **K3. Bounds for η = +1.** The law-on region reaches a gate y only if W(u₁(y)) ≥ Ξ (dust pressure is non-negative and
  only raises the bar), so κ ≥ κ_min(y) = √(4π/W(u₁(y))).
  Gates: **G-M** y = 1 (the law must be on at the MOND radius) and **G-D** y = 1/100 (I-f).
  Hand values, to be met within 1 %: W = 0.4646 and 6.421e-4; κ_min = 5.20 and 139.9.
- **K4. η = −1 (κ-independent).** The outward pressure is at least ρ_DE c² everywhere, so a wall stops only where the dust
  pressure ρ_d σ² ≥ ρ_DE c², i.e. ρ_d/ρ_DE ≥ (c/σ)². Hand values: 8.99e6, 9.99e5, 8.99e4 at σ = 100, 300, 1000 km/s. For the
  step not to exceed the law's own wall pressure at a gate the same κ_min as K3 applies.
- **K5. η = +1/f, f = 0.0231.** κ_min rises by 1/√f = 6.58: 34.2 (G-M) and 920 (G-D).
- **K6. The action as frozen has η = 0.** Symbolic: J(0) = 0 (I-c) and W(0) = 0 (I-g).
- **Reported, not graded:** the largest |η| the gates allow at the top of the window, |η| ≤ κ² W/(4π) (hand: 1.36e-2 at
  G-M, 1.88e-5 at G-D); y*(κ) at the two window edges (hand: 249 and 37.3); Ξ and y* at the fitted κ = ½ (hand: 16π = 50.27
  and 53.8), on the last line only.
- **I-checks:** I1 grep for forbidden constants. I2 symbolic κ-dependence printed. I3 Ξ invariant under G → λG, ρ → μρ,
  c → νc. I4 no law κ read upstream; the fitted ½ appears only in the last reported line. I5 no Friedmann. I6 footing ρ_DE.
  I7 ħ-free. I8 π-weight of κ_min² printed.

## MUTATE (`W4_24_MUTATE=1`, separate `_MUTATE` outputs, exit 1 when all controls bite, 2 otherwise)

- **MU1. Poisson's coupling 4πG → 8πG** in the wall unit. Expected: Ξ doubles, both κ_min rise by √2 (7.35 and 197.8),
  and K3's hand-value check fails.
- **MU2. Pressure step |w|·V_in with w = −0.9.** Expected: both κ_min fall by √0.9 (4.93 and 132.7), K3 fails.
- **MU3. The constant moved outside the switch (η = 0).** Expected: κ_min = 0 at both gates, K3 fails, and the verdict rule
  no longer returns the first label.
- All three must bite.

## Verdict (frozen)

- **SWITCHED VACUUM EXCLUDED; THE FREE CONSTANT STAYS OUTSIDE THE SWITCH; κ FREE** (class CLOSURE) if K1–K6 pass and, for
  η = +1, η = +1/f and η = −1, κ_min exceeds the top of W_data (0.607) at both gates.
- **BOUND REACHES THE WINDOW** if κ_min at G-M is ≤ 0.607 for η = +1. Not expected; it would call for a second lane.
- **CHECK FAILED** otherwise, reported as is.

**Hand expectation (disclosed):** the first label. Before freezing I told the owner in chat that at the fitted κ the step is
16π ≈ 50 wall units against 0.18 at u = 1 and 0.0006 at 10 r_M, and called 0.18 "at most". That wording was wrong: W grows
without bound inward, and 0.18 is its value at g = a₀. The gate used here is y = 1 (the MOND radius, W = 0.4646), fixed in
this file before any script.

## Limits

- Weak-field, static, sharp wall: SWT1's class. A thick wall lowers p_wall (I-d) and only raises κ_min.
- H1 is a hypothesis. The lane does not say what dark energy is; it says the switched part of the constant cannot be it.
- V_out is untouched: k01's zero mode survives in the two-phase action, and with it the closure of 2026-11-03.
- The action-based switch class is itself closed on every exit (PAPER71). This lane adds one more reason, not a new exit.
- If TPA1's result treats the vacuum differently, a new register row will reference this one.

κ = ½ FITTED; not theory closed.
