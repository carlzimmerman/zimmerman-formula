# L205 scalar sign and clock health checkpoint

Verdict: **refuted, with a counterexample**, for L205's asserted physical healthy domain. Its algebraic expression for `2 F_Y` is correct on its explicitly restricted Q=0, gamma=0 branch; its interpretation as a positive spatial kinetic coefficient has the opposite sign to the action. The identification with a physical gravitational MOND function is incomplete.

Scope: base supplied by parent `ac2052ae0`; original source `fable_independent_2026/L205_does_the_family_give_mond.py` unchanged. Freeze positive U,d,ell,m0 at one clock time. Signature -+++, tau=t, chi=Qt+v.x, X=Q²-Y, Y=|v|², logarithm domain m=U-2d(Q²-Y)>0. P=-U/2 log(m/m0); W=U+2dell(sqrt(1+Y/ell)-1). The metric is held Minkowski for this local principal-action diagnostic. This is not a full gravitating health theorem.

## Decisive sign and leading-power results

On Q=0, F(Y)=P(-Y)+W(Y), and the scalar quadratic kinetic coefficient is P_X=Ud/(U+2dY)>0. Its transverse spatial coefficient in L is F_Y, so positive gradient energy requires **-F_Y>0**, not F_Y>0. The physical scalar stiffness convention used here is C_T=-2F_Y. Radial stiffness is C_L=-2(F_Y+2YF_YY). Changing the overall convention for writing a scalar equation does not change these energy signs.

L205's expression is

`mu_L205 = 2F_Y = 2d/sqrt(1+Y/ell) - 2Ud/(U+2dY)`.

Its leading term is `(4d²/U-d/ell)Y`. Consequently the generic Q=0 near-origin gradient-health domain is **U>4dell**. Both stiffnesses vanish at Y=0 itself, which is a degenerate endpoint and not strict positive-speed health. For U=d=ell=1, Y=1/100, L205's claimed condition 4dell>U holds but C_T=-0.02929006669 and C_L=-0.08647986246: both scalar spatial energies are negative. For U=10,d=ell=1,Y=1/100 both are positive (0.00593360361, 0.01766921460). The clock block is regular at these small-gradient points.

At U=4dell the Y coefficient vanishes; the next coefficient is `d Y²/(4ell²)` in mu_L205. Thus the tuned branch has fourth power in |grad chi|, with the wrong energy sign on Q=0. The generic power is quadratic in |grad chi|, not linear. These are scalar constitutive powers; rotation-curve claims additionally require scalar sourcing and a proven mapping from chi to the physical metric potential.

Exact transverse Q=0 sign range for Y>0: C_T>0 iff `0<Y<U(U-4dell)/(4d²ell)`; this interval exists only for U>4dell. Radial health must also hold. At high Y, mu_L205 tends to zero as `2d sqrt(ell)/sqrt(Y)`, while its radial counterpart `mu_L205+2Y mu_L205'` tends as U/Y. Both corresponding physical stiffnesses are negative asymptotically. It does not tend to a nonzero Newtonian interpolating coefficient. This observation alone does not exclude a Newtonian metric sector supplied by Einstein gravity.

## Clock perturbation derived from the same invariants

Set tau=t+pi and chi=Qt+v.x+sigma. For a wave direction n write a=v.n, and denote derivatives by sigma_t,sigma_n,pi_n. Direct expansion of X, s and Y to second order yields, modulo a spacetime divergence with frozen coefficients,

`L2 = K sigma_t² - 4Q P_XX a sigma_t sigma_n + A sigma_n² - 2Q T sigma_n pi_n + D pi_n²`,

where

* K=P_X+2Q²P_XX;
* A=-P_X+W_Y+2(P_XX+W_YY)a²;
* T=W_Y+2W_YY a²;
* D=Q²W_Y-W/2+(W_Y+2Q²W_YY)a².

The apparent time mixing `2W_Y a(pi_t sigma_n-sigma_t pi_n)` is a divergence. There is no quadratic clock time kinetic term on this frozen affine background. Thus demanding a separate positive clock kinetic coefficient would misclassify this constrained field. Its constraint must instead be nondegenerate and elliptic with appropriate boundary conditions. For each nonzero wavevector and D!=0, elimination gives `A_eff=A-Q²T²/D`. A sufficient strict positive reduced Hamiltonian criterion is K>0 and A_eff<0 for every direction. The regular clock branch continuously connected to small Y has D<0. Real characteristic roots alone are weaker than this energy criterion because the time-space drift is nonzero when Qa!=0. K is positive for the stated positive parameters and m>0.

On Q=0 the scalar/clock mixing vanishes and these formulas reduce to the transverse/radial sign test above. Merely setting the clock at rest does **not** imply Q=0. On the timelike Y=0 branch, the fixed-clock transverse stiffness would be `2(P_X-W_Y)=4d²Q²/(U-2dQ²)`, which is nonzero when Q!=0. But after solving the clock constraint A_eff=0 exactly for every Q with U>2dQ². Therefore the fixed-clock inference misses a degeneracy of the coupled system.

For reference, direct symbolic differentiation gives these near-Y=0 reduced coefficients with Delta=U-2dQ²>0:

`A_eff,T = -d(4Q²d²ell+U²-4Udell)Y/(2ell Delta²)+O(Y²)`;

`A_eff,L = d(4Q²d²ell-3U²+12Udell)Y/(2ell Delta²)+O(Y²)`.

At this order, the strict longitudinal energy condition is `3U²-12Udell-4Q²d²ell>0`; it also implies the transverse condition. These are frozen-background small-Y statements, not all-gradient or cosmological bounds.

## Limits and missing physical implications

The constant-gamma cubic term has no bulk quadratic scalar contribution on an affine flat background: its quadratic term is proportional to `(constant grad chi).grad sigma Box sigma`, a divergence. It can affect non-affine backgrounds and the coupled metric principal system, neither computed here. Explicit clock-time coefficient derivatives and V enter lower derivative terms and background equations. Holding the metric fixed cannot certify or refute the full constrained metric-scalar theory by itself.

For minimally coupled Sm[g,matter], there is no direct chi matter source from varying Sm. An identification chi=Phi, a baryonic scalar source, the metric force law, and boundary selection have not been established by L205. Its rotation-curve exponent is conditional on those missing steps. Its `nu(x)` numerical check also mixes labels: the square-root deep behavior uses x=g_N/a0; conversion to a function of g/a0 requires y=x nu(x), after which mu(y)~y. Calling its numerical x directly g/a0 is not consistent with that conversion.

Dependency audit: F algebra **passed**; sign-to-health implication **failed**; generic leading exponent **passed with restriction**; tuned endpoint **omitted by L205**; clock Q=0 inference **failed**; coupled clock elimination **passed in frozen scalar diagnostic**; chi-to-Phi mapping **not addressed**; full metric/gamma characteristics **out of scope**.

## Executed evidence

`audit_health.py` derives the quadratic action from exact s,X,Y before comparing coefficient formulas, checks the clock elimination and family restrictions, and checks asymptotics plus two rational test points. **19 checks passed**. Python 3.9.6, SymPy 1.14.0. Runtime and input hashes are recorded in `run_001/manifest.json`; stdout is `run_001/stdout.txt`.

From repository root, executed successfully (exit 0):

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/contract.json --input fable_independent_2026/L205_does_the_family_give_mond.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/audit_health.py --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/run_001 --timeout 60 --max-output-bytes 1048576 --max-cpu-seconds 45 --max-threads 1 -- python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/audit_health.py
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The original L205 script was read as the audited input, not rerun or edited. Its emitted PASS labels are not used as evidence for this audit. No external theorem or source is required for the elementary variations and sign implications here.

`HealthSign.lean` also compiled successfully, exit 0, using this exact command from the existing pinned project directory `qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`:

```sh
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/HealthSign.lean
```

All three theorem outputs printed the actual axiom set `[propext, Classical.choice, Quot.sound]`; no custom axiom and no sorry. The compiler emitted only an unused/unreachable `ring` tactic warning. This formalizes the rational coefficient factorization, sufficient positive-sign domain, and the U=d=ell=1 wrong-sign counterexample. It does not formalize action variation or physical health.
