# Actual homogeneous curvature feedback through dust–radiation histories

The coupled history changes the sharp-prescribed-radiation conclusion substantially. For the same late coupling S/M=0.4, finite ξ=100 and 1000 histories evolve backward through ordinary dust–radiation equality while retaining F>0 until a declared positive-F guard. They reach that guard at a≈0.009560 and 0.001871, respectively. Both stop before the requested a=10⁻⁴; these are bounded examples, not a no-go for other ξ, amplitudes or initial data.

The full Jordan carrier density is negative near the guard, and its pressure is nonzero. Neither charge conservation nor positive principal field kinetic coefficients makes this a positive cold dust component. A self-consistent homogeneous arrow is now explicit; perturbative response on this mixed history, initial-data selection, extension beyond the guard and nonlinear source matching remain open.

## Actual action and initial data

Retain the same four-dimensional canonical complex action:

S=∫√−g [M R/2−|∂χ|²−ξR|χ|²]+S_dust+S_radiation,
F=M−2ξf, f=|χ|², E=|χ̇|², D=Re(χ*χ̇), Ḟ=−4ξD,
B=F+12ξ²f=M+2ξ(6ξ−1)f.

Ordinary dust and radiation are minimally conserved: ρ_d=ρ_d0 a⁻³ and ρ_r=ρ_r0 a⁻⁴, p_r=ρ_r/3. They are not prescribed GR expansion histories. The numerical controls set M=1, a_i=1, τ_reference=1, ρ_d0=4/3, ρ_r0=0.01ρ_d0, S_i/M=0.4, ξ=100 or 1000, and

|χ_i|²=S_i/(8ξ²), χ_i positive real,
χ̇_i=χ_i(−1/2+iω), ω²=4ξ/3−1/4.

These are circular-*dust-reference* field data, not an assertion that the actual mixed background is circular EdS. In particular H_i is solved from the actual constraint, not set to 2/3. The constant phase convention only fixes the U(1) orientation. The reference τ does not specify a real cosmic age or radiation-era observation.

## Full Einstein trace, Friedmann and evolution

The scalar equation is χ̈=−3Hχ̇−ξRχ. Taking the full Einstein trace and using this scalar equation yields

R=[ρ_d+2(6ξ−1)E]/B.

Radiation has zero ordinary trace, but the carrier does not: for ξ>3/16 and a nonzero charged state, E>0 and R>0 even when ordinary radiation dominates. The preceding prescribed R=0 matching toy cannot predict this evolution.

The actual Friedmann constraint is

C=3F H²+3ḞH−(ρ_d+ρ_r+E)=0.

With F>0 and positive ordinary density, choose the expanding root

H=[−Ḟ+√(Ḟ²+4F(ρ_d+ρ_r+E)/3)]/(2F)>0.

When Ḟ≥0, evaluate the algebraically identical cancellation-safe expression

H=2(ρ_d+ρ_r+E)/[3(√(Ḟ²+4F(ρ_d+ρ_r+E)/3)+Ḟ)].

When Ḟ<0 the original numerator is safe. No equation is clamped or changed at small F.

Use x=ln a and state (Reχ,Imχ,Reχ̇,Imχ̇,elapsed proper time). The exact evolving equations are

dχ/dx=χ̇/H,
dχ̇/dx=−3χ̇−ξRχ/H,
d(elapsed time)/dx=1/H.

Ordinary densities are the conserved functions above. H and R are computed from the same action and state at each step. The elapsed-time zero is arbitrary; no inferred big-bang age is reported.

## Independent constraint/geometry closure

Raw complex-field evolution gives ḟ=2D, Ḋ=E−3HD−ξRf, Ė=−6HE−2ξRD. Independently differentiating C with Ḣ=R/6−2H² gives

Ċ=H[BR−ρ_d−2(6ξ−1)E]−4HC.

Thus the specified trace enforces Ċ=−4HC. Conversely, differentiating the algebraically solved C=0 is nonsingular because

∂C/∂H=3(2FH+Ḟ)=3√(Ḟ²+4F(ρ_d+ρ_r+E)/3)>0,

and recovers Ḣ=R/6−2H². The scalar, Friedmann, trace and spatial Einstein evolution are mutually consistent; no radiation GR Poisson/curvature assumption is inserted.

The numerical geometric-curvature monitor differentiates H(x,state) along the *actual* evolving vector by a complex-step directional derivative, independently of the formula Ḣ_trace=R/6−2H². It compares 6(H dH/dx+2H²) with R. In the zero-curvature negative control it differentiates along the mutated vector, so a false R=0 scalar prescription cannot pass by checking the unmutated equations.

The charge Q=a³ Im(χ*χ̇), one half the canonical complex Noether normalization under this orientation, is exactly conserved. Keeping this factor convention explicit prevents assigning a charge-to-cold-mass dictionary silently.

## Full density and pressure, not canonical energy

Direct metric variation gives

ρ_c=E+2ξ[3H²f+3Hḟ]
   =E−3HḞ+3(M−F)H²,
p_c=E+2ξ[−(2Ḣ+3H²)f−f̈−2Hḟ].

Using the scalar equations and geometric curvature, the pressure becomes

p_c=(1−4ξ)E+4ξHD+2ξf[(2ξ−1/3)R+H²].

These expressions are independently checked against the solved metric dictionary

ρ_c=3M H²−ρ_d−ρ_r,
p_c=−M(2Ḣ+3H²)−ρ_r/3,

and satisfy ρ̇_c+3H(ρ_c+p_c)=0. The stress is not E alone. The scripts output signed ρ_c and p_c, their raw metric-variation counterparts, and the carrier fraction of 3M H²; no w_c ratio is used at a nearly zero density.

For the stipulated initial χ,χ̇ and ρ_d0, the trace gives exactly R_i=4/3 regardless of the added ρ_r0. Consequently the initial carrier obeys 3p_ci−ρ_ci=0 on the actual constraint: its tiny positive initial stress is radiation-type, not dust. Indeed ρ_ci=6ξf_i(H_i−2/3)(H_i−1/3)>0: adding positive ordinary radiation raises the expanding constraint root above 2/3. H_i≈0.66999 differs from the circular dust value 2/3.

## Principal field kinetic scope

This retained canonical curvature action has a useful independent local dictionary. Set ϕ₁+iϕ₂=√2χ and g_E=(F/M)g_J. The Einstein-frame scalar kinetic matrix is

K_ab=(M/F)δ_ab+3M F_aF_b/(2F²), F_a=−2ξϕ_a.

Its tangential eigenvalue is M/F and its radial eigenvalue is MB/F², since ΣF_a²=8ξ²f. They are positive for F>0; the pure graviton and canonical-field principal cones are luminal and conformal frames share the null cone. Ordinary matter's scalar-dependent metric coupling is algebraic. This is a principal-field statement for this specific action, not the log-KGB/cutoff model and not a proof of low-frequency stability, all coupled fluid-state health, quantum/EFT validity or absence of Jeans growth. As F tends toward zero the frame/kinetic coefficients become singular; no continuation across that boundary is claimed.

## Bounded backward and forward experiments

For each ξ integrate backward from a=1 toward a=10⁻⁴, with a terminal guard F/M=10⁻⁸. The guard is deliberately still positive: it is not a certified F zero or a proof of a spacetime singularity. Three implementations are used: DOP853 rtol10⁻⁹ and 3×10⁻¹⁰, and independent Radau rtol10⁻⁹; atol=rtol×10⁻⁵. Sample 81 logarithmically spaced achieved points and record F,B,H, curvature, actual density/pressure, charge and constraint residuals. Integrate forward from each achieved endpoint with the same equations to recover the declared initial state.

Development output is:

| ξ | achieved a at F guard | ordinary ρ_r/ρ_d | carrier ρ_c/(3M H²) | R/H² |
|---|---:|---:|---:|---:|
|100|0.0095599066|1.0460353|−0.1066587|1.8583495|
|1000|0.0018709254|5.3449487|−0.1579719|0.8362458|

Ordinary equality is a=0.01 by conserved density normalization. Reaching equality does not mean the total expansion is a GR radiation era: the carrier stress is active, its density fraction is negative at the endpoints, and the recorded nonzero curvature differs from a prescribed radiation metric. The signed endpoint pressures are approximately −1.74207×10⁵ and −9.45331×10⁷ in the declared M=τ_reference=1 units. These numbers are toy-unit source stresses, not cold densities or observational parameters.

The field and endpoint differences across solvers, charge errors and geometric errors are stored in results.json. The initial matching toy's positivity bound is not transplanted here. Curvature feedback delays its rapid backward amplitude growth substantially, but both bounded examples still stop at the positive-F guard before the requested a=10⁻⁴. This neither selects S nor proves all histories fail; changing ξ or initial data can change the reachable interval and must be audited separately.

## Numerical conditioning and preserved failures

The first development `preflight_a` had 37/38 checks, with one forward-recovery failure: its componentwise norm divided zero initial components by 10⁻⁶ and gave 2.15056×10⁻⁴ against a 2×10⁻⁴ criterion. The actual scripts used for that development output are preserved, with hashes, in historical_inputs/preflight_a/. The new norm uses common physical vector scales: |χ_i| for both field components, |χ̇_i| for both velocity components and the reference time 1 for elapsed time. It keeps the same 2×10⁻⁴ threshold and is a different declared norm; the earlier failed criterion is not relabeled passed. Forward errors with this norm are about 10⁻⁸–3.4×10⁻⁷ in the development results.

Radau's internal finite-difference Jacobian adaptation emits overflow warnings in its factor update. Solver success, finite sampled physical states, charge/geometry closure, method agreement and forward recovery are recorded separately; the warning is retained in stderr and is not evidence of a physical overflow or an excuse to suppress a failed run. These are bounded floating-point integrations, not interval-arithmetic certificates or full perturbative stability calculations.

## Exact remaining implication

The next physical arrow is a regular complete mixed-era carrier history and its perturbative density/velocity/Weyl transfer on that actual backreacting background, with independently specified initial charge/amplitude data. An extension reaching a chosen earlier interval with positive F cannot be inferred from these stopped runs. The earlier finite EdS transfer remains correct on its frozen background, but is not automatically the transfer of this mixed history.

No positive pressureless cold sector, source/MOND matching, CMB prediction, empirical early-time bound or 32π selector follows. This computation genuinely replaces the prescribed-R=0 history with coupled curvature feedback; it does not turn a scoped boundary into a universal theory no-go.

Inputs/HEAD hashes and tested range are in provenance.json and contract.json. Parent reports/scripts are read-only. REPORT is excluded from execution inputs so final evidence-summary prose does not stale the actual runs.

## Authoritative runs and freeze

`runs/exact_main_a` passes 22/22 exact identities; `history_main_a` passes 40/40 bounded checks. Omitting the carrier kinetic term in the trace fails four symbolic closure/stress checks; using canonical energy as full carrier density fails one; forcing the evolving scalar to use R=0 fails all six independent trajectory-geometry checks while retaining charge and an algebraically solved Friedmann root. Those are intended negative controls, illustrating why a single conserved quantity or imposed constraint is insufficient. All five standard manifests validate against current frozen inputs.

Relative to the tighter DOP853 reference, endpoint ln(a) differences are at most 1.72×10⁻⁸ and endpoint state discrepancies in the declared physical vector norm are at most 7.67×10⁻⁷. Sampled charge relative errors are below 3.0×10⁻⁸ and geometric-curvature scaled errors below 5.2×10⁻¹³. Forward recovery errors in the declared common-vector norm are at most 3.4×10⁻⁷; this does not pass or replace the old zero-component criterion. Radau internal adaptation warnings remain in stderr.

Development `preflight_exact_a` originally had an unnecessary added C term in an identity tested off the constraint surface; its 20/21 output is retained and is not a model failure. Removing that extra term gives the correct direct initial trace identity; the old exact script was not separately captured and has no authenticated historical input hash. The corrected 22-identity script alone supports the authoritative exact run. No frozen parent source was modified.
