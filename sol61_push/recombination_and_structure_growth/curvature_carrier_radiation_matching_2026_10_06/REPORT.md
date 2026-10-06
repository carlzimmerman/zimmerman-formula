# Backmatching the charged curvature carrier through a sharp radiation–EdS transition

The prescribed sharp transition exposes a concrete initial-history cost. The exact charged circular EdS carrier backmatches to radiation constant and decaying modes whose cancellation keeps its amplitude small at the join. Going backward destroys that cancellation. For fixed late coupling S_e/M=0.4 and large ξ, F=M−2ξ|χ|² reaches zero by t≈0.12524 t_e. This is a scalar history on a prescribed GR metric, not a self-consistent cosmological no-go: the carrier radiation stress is already nonzero immediately, and becomes order the prescribed radiation density before that F zero. A coupled smooth radiation–dust history remains the next missing implication.

## Actual action and declared matching toy

The retained action is

S=∫√−g [M R/2−|∂χ|²−ξR|χ|²]+S_ordinary,
F=M−2ξ|χ|², χ=(ϕ₁+iϕ₂)/√2.

Thus the complex kinetic normalization equals two canonical real scalars, not one unnormalized real field. The effective tensor coefficient is F. The parent reports reconstruct the exact circular EdS zero-stress solution and finite-ξ dust/metric transfer; these frozen inputs are not edited here.

Specify a prescribed C¹ scale factor:

for t≤t_e: a=a_e(t/t_e)^(1/2), H=1/(2t), R=0;
for t≥t_e: τ=t+t_e/3, τ_e=4t_e/3, a=a_e(τ/τ_e)^(2/3), H=2/(3τ), R=4/(3τ²).

At the join a and H are continuous, and R jumps by 3/(4t_e²), with no Dirac delta. Scalar equations □χ−ξRχ=0 therefore require continuity of χ and χ̇; χ̈ has a finite step. This is a controlled sharp-curvature prescription, not an action for a microscopic transition or a solution of all Einstein equations on the radiation side.

On the EdS side use χ_e≠0 and χ̇_e=χ_e(−1/2+iω)/τ_e, where ω²=4ξ/3−1/4>0. The corresponding exact circular EdS carrier has |χ_e|²=f_e=A/τ_e. Define

S_e=8ξ²f_e, s=S_e/M, δ_e=2ξf_e/M=s/(4ξ).

The charged branch requires ξ>3/16; initial tensor positivity requires δ_e<1. No cold mass or selector is assigned by fixing s in an illustrative control.

## Exact radiation solution and amplitude growth

For R=0 the scalar equation χ̈+3Hχ̇=0 gives χ=C₀+C₁t^(−1/2). Matching both value and derivative yields, without a freely adjustable extra mode,

C₀=χ_e(1/4+3iω/2),
C₁=(3/4)χ_e√t_e(1−2iω).

A constant overall phase is irrelevant. Define z=√(t_e/t)≥1 on the backward radiation interval. Then

|χ|²/f_e=(1/4+3z/4)²+(3ω/2)²(z−1)²
             =1+(3/2)(z−1)+3ξ(z−1)².

The second equality uses the *same* EdS relation ω²=4ξ/3−1/4. The derivative with respect to z is 3/2+6ξ(z−1)>0, so the fraction grows strictly backward. The constant/decaying modes carry opposite large imaginary components; their cancellation occurs at the join and is not preserved in the R=0 phase.

## Exact finite-start positivity bound and first zero

Let y=z−1. The effective-coupling fraction is

δ(z)=2ξ|χ|²/M=δ_e[1+3y/2+3ξy²]
     =s/(4ξ)+3sy/(8ξ)+3sy²/4.

For 0<δ_e<1 there is exactly one backward root F=0, at

y_*=[−b+√(b²+4a(1−δ_e))]/(2a), a=3ξδ_e, b=3δ_e/2,
t_*/t_e=(1+y_*)^(−2).

F>0 precisely on t_*<t≤t_e in this prescribed radiation history. For a finite desired start t_s≤t_e, with z_s=√(t_e/t_s), positivity over the entire interval is equivalent to

s<4ξ/[1+(3/2)(z_s−1)+3ξ(z_s−1)²].

This is a sharp necessary and sufficient bound within the prescribed scalar history, not an astrophysical observational bound. At fixed s>0 and ξ→∞,

δ(z)→(3s/4)(z−1)²,
y_*→2/√(3s), t_*/t_e→[1+2/√(3s)]^(−2),
s_max→4/[3(z_s−1)²].

For s=0.4 the limiting t_*/t_e is about 0.12523768; large ξ does not postpone the loss to arbitrarily early times. Starting instead at t_s=t_e/100 requires s≲0.01646 in the large-ξ limit. This dimensionless toy comparison is not transferred into a real cosmological age or cold abundance constraint. Extrapolating this prescribed metric all the way to t→0 at any nonzero charged amplitude necessarily loses F positivity; finite starts are the relevant scoped statement.

## Full radiation stress: exact self-consistency discrimination

The full Jordan carrier stress, in the retained complex normalization, is

T_cμν=∂μχ*∂νχ+∂νχ*∂μχ−gμν|∂χ|²
       +2ξ[fGμν+(gμν□−∇μ∇ν)f], f=|χ|².

For the general radiation scalar χ=C₀+C₁t^(−1/2), direct variation gives

ρ_c=(3ξ/2)|C₀|²t^(−2)+(1/4−3ξ/2)|C₁|²t^(−3),
p_c=(ξ/2)|C₀|²t^(−2)+(1/4−3ξ/2)|C₁|²t^(−3).

All interference terms cancel from both stress components. These are full metric-variation expressions, not the positive canonical kinetic energy alone. The constant branch behaves as a radiation-type contribution/Planck shift; the decaying branch is stiff, and its full coefficient is negative for this ξ>3/16 branch. Neither is a gravitating dust stress.

Matching fixes |C₀|²=f_e(3ξ−1/2) and |C₁|²=3ξf_e t_e. Relative to the *prescribed GR radiation* ρ_r=3M/(4t²), p_r=M/(4t²),

ρ_c/ρ_r=δ_e(3ξ−1/2)(1−z²),
p_c/p_r=δ_e(3ξ−1/2)(1−3z²).

At the join ρ_c=0, but p_c/p_r=−2δ_e(3ξ−1/2)→−3s/2. For s=0.4 this is approximately −0.6. This is a finite pressure step, not a delta-function surface layer: χ,χ̇,a,H remain continuous while χ̈ and curvature step.

More fundamentally, exactly prescribed GR radiation with only ordinary traceless radiation would require the carrier trace to vanish. Here

−ρ_c+3p_c=2(1/4−3ξ/2)|C₁|²/t³≠0.

Thus the prescribed R=0 metric is not an exact full Einstein–carrier–ordinary-radiation solution even immediately before the join. The exceptions C₁=0 (zero U(1) charge) or ξ=1/6 (below the real circular EdS branch) do not realize the stipulated charged matching. Trivial χ_e=0 gives no carrier. Additional compensating matter or backreaction would change this toy's physical premises.

An illustrative density-backreaction threshold |ρ_c|=ρ_r occurs at

t_back/t_e=[1+1/(δ_e(3ξ−1/2))]^(−1)
→[1+4/(3s)]^(−1).

For s=0.4 this tends to 0.23076923, earlier in the backward trajectory than the F zero at 0.12524. In the large-ξ limit the density ratio at F=0 is 1+√(3s)>1. The tabulated finite ξ≥1 examples preserve this ordering; no universal ordering for all ξ>3/16 is claimed. Backreaction already invalidates the prescribed metric before the positivity diagnostic can be read as an actual evolution endpoint.

## Conserved charge survives, but is not cold mass

Define Q=a³ Im(χ*χ̇), one half of the usual canonical U(1) charge under this orientation. On the radiation branch

Im(C₀*C₁)=−(3/2)f_eω√t_e,
Q=(3/4)a_e³f_eω/t_e=a_e³f_eω/τ_e.

It is exactly conserved and equals the EdS charge at the join. Real time-dependent curvature and the finite curvature step do not break U(1). Charge preservation therefore does not supply a positive cold stress or protect F: this history retains charge while the prescribed radiation stress and coupling fail the desired interpretation.

## Bounded numerical evaluations and next arrow

At fixed s=0.4, exact radical evaluations give:

|ξ|t_Fzero/t_e|t_densityback/t_e|join p_c/p_r|
|---|---:|---:|---:|
|1|0.1600000|0.2000000|−0.5000|
|10|0.1283049|0.2277992|−0.5900|
|100|0.1255406|0.2304733|−0.5990|
|1000|0.1252679|0.2307396|−0.5999|
|10⁶|0.1252377|0.2307692|−0.6000|

These are dimensionless checks of the declared sharp prescription, not numerical astrophysical matching. They contrast a late small Planck fraction δ_e∝1/ξ with an order-one earlier fraction caused by the matching modes. The finite EdS transfer parent's healthy tested interval remains valid; this calculation challenges its chosen initial origin rather than changing those equations.

The first unresolved implication is a *self-consistent*, regular radiation–dust–carrier solution with the same charge and late circular response, F>0 throughout a declared finite early interval, and complete stress variation. A smooth transition can change the backmatched mode coefficients; backreaction can change R and the phase evolution. This sharp toy does not exclude either possibility, and does not prove such a history exists. No cold abundance, CMB/recombination prediction, MOND source matching or 32π selection follows.

Source/HEAD hashes are in provenance.json. All load-bearing algebra and bounded exact-radical evaluations are in checks.py. REPORT is excluded from execution inputs, and parent frozen reports/scripts are read-only.

## Authoritative evidence

`runs/main_a` passes 31/31 exact checks, including full covariant stress, matching and curvature step, unique backward coupling root, conserved charge, and five finite radical controls. Omitting the metric-improvement stress fails six identities; discarding the matched phase fails fourteen; asserting full on-shell prescribed GR radiation fails the additional pressure-vanishing check (31/32). These failures are expected negative controls. All four standard manifests validate against the frozen script/source/provenance inputs. Development `preflight_a` had 30 checks before addition of the exact carrier-trace identity and is explicitly non-authoritative. REPORT/run-summary are excluded execution inputs; no existing parent evidence was changed.
