# Independent L206 pressure and clock-equation audit

Primary verdict: **refuted, with the omitted counterterm identified**, for the assertion that the reconstructed canonical action has the pressure used in L206 lines 30–36 on its tracked background. The Lean theorem at `fable_independent_2026/lean_2026/Mondlean.lean:1151` is a valid conditional rearrangement of its assumed equation of state, but its assumption is not the pressure of the coefficient family written in L206's own header. No original files were edited.

The obstruction is exact, independent of the size of gamma. L206 drops the `-2 gamma qbar² qbar'` contribution to W0 when computing pressure, although it retains the corresponding P counterterm for density and current. This audit concerns Part A only.

## Which derivative is in the canonical coefficients?

Authoritative source: `nonlinear_evolution_2026/constitutive.py`, lines 19–33 and 53–67, relative to the enclosing `clock_response_repair_2026` directory. It defines a reference flow, computes `along(q)`, puts this in `first[0]`, and uses

`W0(tau) = U(tau) - 2 gamma qbar(tau)² qbar'(tau)`.

The coefficient-argument derivative is also the proper-time derivative **on the reference reconstruction**, whose clock rate equals one. It does not remain the actual proper-time derivative on another trajectory with arbitrary s. In the code, the jet argument called `t` supplies the clock-argument values and partial derivatives. Reading its variable name as universal physical proper time would change the action off the reference trajectory. A numerical derivative of `background(t).q` agrees with its stored `qdot` and the W0 counterterm is checked against the actual returned jets.

For actual homogeneous fields with positive lapse N and increasing tau,

`s = tau_dot/N`, `Q = chi_dot/N`, `H = a_dot/(Na)`,

and the tracked branch `Q=qbar(tau)` implies

`dQ/dt_proper = s qbar'(tau)`.

## Arbitrary-lapse action variation

For the action with constant gamma and metric signature -+++, the homogeneous scalar part, after one integration by parts, is

`Lhom = N a³[P(Q²,tau)-V(tau)] + a³ tau_dot W0(tau) - 2 gamma a² a_dot Q³`.

The Python audit derives the following by varying N, a, chi_dot and tau before fixing the lapse:

`rho = 2Q² P_X - P + V - 6 gamma H Q³`,

`p = P - V + s W0 + 2 gamma Q² dQ/dt_proper`,

`j = 2Q P_X - 6 gamma H Q²`,

`E_tau/(N a³) = P_tau - V_tau - 3H W0`.

The W0 derivative terms cancel between the explicit tau variation and the derivative of its momentum. In particular the **actual clock field equation** is the last expression set to zero. The equation-of-state definition `w=p/rho` is a different statement and is not conservation. No Einstein equation or H=Href assumption was used to derive these formulas. The script also checks the raw cubic-to-reduced action integration by parts at arbitrary N.

## Applying the coefficients without mixing sources

Write q=qbar(tau), q'=dqbar/dtau, Hb=Href(tau), and m=U-2dq². On Q=q and Y=0 the canonical coefficients give

`P=0`, `V=U`, `P_X=Ud/m+3 gamma q Hb`, `W0=U-2 gamma q²q'`.

Before using the tracked chain rule, pressure is

`p = U(s-1) + 2 gamma q²[Qdot_proper - s q']`.

On a tracked trajectory the bracket vanishes exactly:

`p = U(s-1)`.

L206 instead uses `p_bad=U(s-1)+2 gamma q²Qdot_proper`; its error is `p_bad-p=2 gamma s q²q'`. The correction is neither a residual effect to estimate nor a small nonzero term on this branch. At s=1 the reconstructed action has zero pressure, whereas L206's expression generically has `2 gamma q²q'`.

The cancellations in density and current require distinguishing the actual H from the coefficient Hb:

`rho = U²/m + 6 gamma q³(Hb-H)`,

`j = 2qUd/m + 6 gamma q²(Hb-H)`.

Thus the familiar `rho=U/m_rel` with `m_rel=m/U` follows on H=Hb. L206 lines 22–29 silently use the same H in both places. The cancellation can be justified on the reconstructed solution, but is not an identity for arbitrary H.

When Q=qbar, H=Hb, U and m_rel are nonzero, the corrected equation-of-state algebra gives

`s-1 = w/m_rel`,

even at nonzero gamma. This statement is conditional; it does not establish that an arbitrary-w trajectory satisfying those tracking assumptions exists.

## What the genuine clock equation adds

Differentiating `P(qbar²,tau)=0` gives `P_tau=-2q q'P_X`. Let `A=2qUd/m`. The clock equation restricted to the tracked branch is

`0 = -A q' - U' - 3H U + 6 gamma q²q'(H-Hb)`.

The reference reconstruction satisfies `U'=-A q'-3Hb U`. This follows directly in `constitutive.py` from `A=charge`, `q=1/(1+m_parameter)`, `U=(1-q)A`, and `A'=-3Hb A`. The latter identity follows by differentiating `charge=0.1/a³` along the stored reference flow `a'=a Hb`. The script additionally tests both derivative identities against the canonical stored q,U,d first derivatives at all three sample times, with absolute tolerance 1e-13. Inserting the U identity reduces the clock equation to

`0 = 3(Hb-H)W0`.

For W0 nonzero it enforces H=Hb. On that tracked regular branch j=A, and shift-current conservation gives

`0 = jdot_proper+3Hj = 3Hb A(1-s)`.

For nonzero Hb and A this enforces s=1, hence p=0. This is a restriction within the homogeneous minisuperspace calculation on the exact canonical reference branch; off-branch Q need not equal qbar, and then the simple density/pressure identities must not be transplanted. The cases W0=0, Hb=0, A=0 and nontracking Q require separate analysis. This is not an existence, stability, uniqueness or full four-dimensional clock-dynamics theorem.

## Lean scope and verification

The existing `clock_rate_from_conservation` assumes `w*(U/mrel)=U*(s0-1)+2 gamma q² qd`. Its proof can be correct while the action-to-premise implication fails. It does not derive a continuity equation or a clock Euler equation.

The new `PressureIdentity.lean` instead proves the exact tracked counterterm cancellation and the corrected equation-of-state implication. Both compiled with exit 0 and printed actual axioms `[propext, Classical.choice, Quot.sound]`; no sorry or custom axiom. They formalize the displayed algebra, not the calculus deriving the action variation.

`audit_pressure.py` ran successfully with exit 0. It verifies exact arbitrary-lapse variations, branch identities, the H distinction, and canonical numerical jets at tau=0,0.01,0.02 with s=1,1.2. Absolute pressure tolerance 1e-13; a centered derivative check uses step 1e-6 and tolerance 1e-8. The s=1.2 checks verify local constitutive algebra, not dynamical solutions. The initial run is preserved in `run_001`; the final script adds six canonical reconstruction-derivative checks, with current input hashes and logs in `run_002/manifest.json`. The final run and its validator returned exit 0. Source revision in the manifest is authoritative for the actual run; the parent identified the new claim with revision `0eee1a513`.

Exact commands from repository root:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/pressure/contract.json --input fable_independent_2026/L206_cubic_restored.py --input fable_independent_2026/lean_2026/Mondlean.lean --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/pressure/audit_pressure.py --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/pressure/run_002 --timeout 90 --max-output-bytes 1048576 --max-cpu-seconds 80 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/pressure/audit_pressure.py
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/pressure/run_002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

From the pinned directory `qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`:

```sh
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/pressure/PressureIdentity.lean
```

No original L206 or Mondlean script was executed or modified. No empirical inference about GW170817 or matter-clock measurements follows from this pressure audit.
