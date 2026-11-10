# W4-24: the vacuum constant in the two-phase action. SWITCHED VACUUM EXCLUDED; κ FREE

**Label (frozen rule, second run, after AMENDMENT A1): SWITCHED VACUUM EXCLUDED; THE FREE CONSTANT STAYS OUTSIDE THE
SWITCH; κ FREE (class CLOSURE).** κ = ½ is FITTED. No κ is derived or output. Not theory closed. Adopts nothing.

Criteria `FROZEN_CRITERIA.md` (180b1ff772, committed alone). Amendment `AMENDMENT_A1.md` (603285f007, committed alone
between the two runs). Script `w4_24.py`; outputs `w4_24.out`, `w4_24_results.json`; mutation run `w4_24_MUTATE.out`,
`w4_24_results_MUTATE.json`; first run kept as `w4_24_firstrun_K1bfail.out`, `w4_24_results_firstrun_K1bfail.json`.

## The question

The 2026-11-03 closure rests on a zero mode: a constant can be added to the law's sector, so a₀ and Λ decouple (k01,
rule S6). The two-phase action (SWT1's class, TPA1's action) multiplies the law's Lagrangian by a switch. Is the constant
still free there, and does any part of it tie a₀ to ρ_DE?

## What the checks show

- **The constant splits in two.** L ∋ −V_out − S·V_in. V_out, outside the switch, is still the zero mode. V_in, inside the
  switch, is the energy difference between the two phases, so it is a pressure step on every wall. The net outward wall
  pressure is (a₀²/4πG)·[W(u₁) − Ξ] with Ξ = 4πG·V_in/a₀² (K1; SWT1's identity re-derived by quadrature to 1e-27 and matched
  to `swt1.json`).
- **If dark energy is the switched part** (hypothesis H1, V_in = η ρ_DE c²), then **Ξ = 4πη/κ²** (K2, symbolic).
- **η = +1 (dark energy in the law-on phase).** The law can be on at a place only if W there is at least Ξ. That needs
  **κ ≥ 5.20** for the law to be on at the MOND radius and **κ ≥ 139.9** for a wall at 10 MOND radii (HE1's disc gate).
  The top of today's window is 0.607, so the bound sits 8.6 and 230 times above it (K3).
- **η = +1/f (the same, with the cosmic mean matched; law-on regions fill at most f = 0.0231).** κ ≥ 34.2 and 920 (K5).
- **η = −1 (dark energy in the law-off phase).** The wall is pushed outward by at least ρ_DE c² everywhere. It stops only
  where the dust is denser than ρ_DE·(c/σ)²: 9.0e6, 1.0e6 and 9.0e4 times ρ_DE at σ = 100, 300 and 1000 km/s. This holds for
  every κ. Law-on regions would fill space, against SWT1's allowance of 0.0231 (K4).
- **η = 0 is the action as frozen.** J(0) = 0 in SWT1's class and W(0) = 0 in TPA1's Lagrangian, where Λ sits outside the
  switch (K6). There the zero mode is intact and κ is free, exactly as in the 2026-11-03 closure.

Reported, not graded:
- The largest |η| the gates allow for a κ at the top of the window is 1.36e-2 (MOND radius) and **1.88e-5** (disc gate). So
  the switched part of the vacuum constant must be under about two parts in 10⁵ of the dark energy.
- For η = +1 and κ anywhere in the window the law would be off wherever g_N is below 37 to 249 a₀. At the fitted κ = ½
  the step is 16π = 50.27 wall units and the law would be off below 53.8 a₀.

## Reading

In the two-phase action the vacuum constant is no longer entirely free: the part inside the switch is physical. But the
walls fix that part to about zero, not to a value that relates a₀ to ρ_DE. The free part stays outside the switch, so the
"4" is as free in this action as in every earlier one. This is one more reason the switched class cannot explain the
coefficient, not a new route to it.

## Controls and disclosures

- **MUTATE: 3 of 3 bite** (exit 1), run one at a time. Poisson 4πG → 8πG moves κ_min by √2 (7.35, 197.8). A pressure step
  of 0.9 V_in moves it by √0.9 (4.93, 132.7). The constant outside the switch gives κ_min = 0 and the verdict rule no longer
  returns the label.
- **First run: CHECK FAILED** by the frozen rule. K1b failed at one row (y = 1e-6) by 1.47e-10 against a line of 1e-10.
  The cause is double-precision cancellation in the value stored in `swt1.json`, which records the same gap to its own
  quadrature. AMENDMENT A1 changed that one line (1e-9 against the stored closed form, 1e-12 against the stored quadrature)
  and nothing else. Apart from K1b's lines and the verdict, the two runs' outputs are identical.
- **A wrong wording of mine, corrected in the criteria.** Before freezing I told the owner the law's wall pressure is "at
  most 0.18" wall units. W has no upper limit inward; 0.18 is its value at g = a₀.
- **All hand values were met within 1 %** (W 0.4646 and 6.421e-4; κ_min 5.20 and 139.9; 34.2 and 920; the three stop
  densities).
- Identity checks: I1 no forbidden constant in the script; I3 Ξ invariant under G, ρ, c rescalings; I8 κ_min² carries one π
  over a transcendental W. No law κ is read upstream; the window and the fitted ½ appear only in the last reported lines.

## Limits

- Weak-field, static, sharp wall (SWT1's class). A thick wall lowers the wall pressure and raises the bounds.
- H1 is a hypothesis. A continuous η is a TRADE and is reported only as the largest allowed value.
- Nothing here bears on what dark energy is, only on whether it can sit inside the switch.
- TPA1 had not landed when this was run; only its frozen Lagrangian was read. If its result treats the vacuum differently,
  a new register row will reference this one.

Register: K847 (family VM, class audit; no determinate trial added, P_LEE unchanged).
