# TP02 independent RG and threshold matching dictionary

1 November 2026. Base `40d43dbb8a9f1517e214302380f7659df7626e6a`, dirty
shared checkout. All writes in this route are under `rg_derivation/`.
TP01 is an immutable mathematical input. **Verdict: the specialized one-
and two-loop running coefficients and one-loop CS identity are established
in the rigid canonical-K model. Full finite two-loop matching and a
microscopic material-pressure prediction remain conditional/open.**

## 1. Primary source, conventions and exact model

The checked source is Martin–Vaughn,
[hep-ph/9311340v4, 24 July 2008](https://arxiv.org/pdf/hep-ph/9311340v4),
Eqs. (2.2)–(2.3), (2.7)–(2.11), printed pp.6–7. The version header and
actual formulas were read through the primary PDF service. No source file
was downloaded or added to the repository. The transfer is the rigid
supersymmetric DR running, not soft-mass or gravity matching.

Let L=16π², t=ln Q, γ_i=G1_i/L+G2_i/L², and dot φ_i=−γ_iφ_i.
The linear superpotential parameter f has mass dimension two; its running
below refers to the dimensional renormalized f, not f/Q². Thus there is
no additional engineering-dimension −2 in dot f/f. The raw action is

    W=fX+(h/2)X Tr A²+(λ/2)Tr A²B,
    K=|X|²+Tr A†A+Tr B†B.

Use 49 chiral coordinates (X,A_a,B_a), Tr(T_aT_b)=δ_ab and gauge generators
T_a/√2. The symmetric Yukawa entries are hδ_ab for X,A_a,A_b and
λ Tr[{T_a,T_b}T_c]/2 for A_a,A_b,B_c, with all permutations.
The gauge data are C_X=0, C_A=C_B=5, d(G)=24, ΣS(R)=10 and ΣS(R)C(R)=50.

The source's nonrenormalization formula gives

    dot h=h(γ_X+2γ_A), dot λ=λ(γ_B+2γ_A), dot f=fγ_X.

The specialized coefficients below are independently derived from its
Yukawa contractions. The two-loop gauge polynomial also includes its
Yukawa trace; it is not a pure-gauge estimate.

## 2. Independent contraction reduction

Define P_i^j=(1/2)Y_ipq Y^jpq. Its diagonal blocks are

    P_X=12h²,
    P_A=h²+(21/10)λ²,
    P_B=(21/20)λ².

The symmetric SU(5) contraction is exact, not fitted to the numerical
tensor. For Tr(T_aT_b)=δ_ab, completeness gives

    Σ_a T_a M T_a=Tr(M)I−M/5,
    Σ_a T_a²=(24/5)I.

Put S_ab={T_a,T_b}/2 and C_abc=Tr(S_ab T_c). Summing over c first gives
Σ_ac C_abc C_adc=Σ_a Tr(S_ab S_ad)−δ_bd/5. Expanding the two
anticommutators, the four traces sum to
[−1/5+24/5+24/5−1/5]δ_bd/4=(23/10)δ_bd. Subtracting δ_bd/5
therefore yields (21/10)δ_bd. The h Yukawa gives two ordered X/A
contributions for an external A but one ordered A/A pair for an external
X or B, explaining the factors in P above.

In the two-loop quartic term, inserting the diagonal P reduces
the source's four-Y contraction to −Σ_mn |Y_imn|² P_n. Hence its three
diagonal coefficients before gauge terms are

    X: −24h² P_A,
    A: −h²(P_X+P_A)−(21/10)λ²(P_A+P_B),
    B: −(21/10)λ² P_A.

The gauge-Yukawa contribution gives 240g²h² for X, 21g²λ² for A and
(21/2)g²λ² for B. In the A block the two h terms cancel because their
internal Casimirs are 0 and 5. The pure-gauge two-loop term is zero for X
and 50g⁴ for each adjoint. Therefore

| Field | G1 | G2 |
|---|---|---|
| X | 12h² | −24h⁴−(252/5)h²λ²+240g²h² |
| A | h²+(21/10)λ²−10g² | −13h⁴−(21/5)h²λ²−(1323/200)λ⁴+21g²λ²+50g⁴ |
| B | (21/20)λ²−10g² | −(21/10)h²λ²−(441/100)λ⁴+(21/2)g²λ²+50g⁴ |

For the gauge beta function, the ordered Yukawa contraction is

    Σ_ijk |Y_ijk|² C(k)/24=10h²+(63/2)λ².

Together with the gauge invariants this yields

    dot g=−5g³/L+g³[150g²−10h²−(63/2)λ²]/L².

These formulas and the nonrenormalization relations specify the complete
two-loop dimensionless and f running of this rigid model in this scheme.
They are not a complete two-loop effective potential or finite kinetic
threshold calculation.

As a separate implementation check, `check_rg.py` builds all 24 generators
and all 49³ Yukawa entries without importing the TP01 implementation. It
contracts the full P matrix and full two-loop gamma matrix before comparing
with these polynomials. Seven deterministic triples include isolated h,
isolated λ, gauge cross terms and a weak unequal-coupling point. Unit
couplings are coefficient tests, not claimed perturbative physical cases.
The maximum full two-loop matrix discrepancy is 2.85×10⁻¹⁴; all eight
symbolic transport/CS identities pass. The bounded run is `run_001/`.

## 3. Finite threshold CS identity and the critical surface

Let Δ=30h²+λ² and U0=f²λ²/Δ, the actual tree valley energy. Write D1 for
the one-loop coupling vector field, including its factor 1/L. Directly,

    γ_eff=(λ²γ_X+30h²γ_B)/Δ,
    D1 U0=2U0 γ_eff,1
          =3f²h²λ²(29λ²−200g²)/(LΔ²).

The complete TP01 spectrum has

    STr M⁴=6f²h²λ²(29λ²−200g²)/Δ².

Since Q∂_Q CW=−STr M⁴/(32π²), the exact one-loop reduced identity is

    D1 U0+Q∂_Q CW=0.

It uses the complete spectrum, not one radial logarithm. The field term
annihilates U0 because the full classical background is stationary and
its energy is constant along X. Parameter differentiation of the minimum
therefore agrees with differentiation before minimization at this order.

The old comparator relation 29λ²−200g²=0 is not an RG constraint. On it,

    d(29λ²−200g²)/dt=29λ²(16h²+13λ²)/(4L)>0.

Thus imposing it after every RG step changes the model's flow. Although
γ_eff vanishes at the reference comparator, its derivative does not.
Differentiating γ_eff with the one-loop flow reproduces the old leading-
log curvature relation; adding that curvature separately to a running
tree-plus-full-threshold potential would double count the retained logs.

## 4. Canonical field transport and the heavy valley

The canonical classical flat coordinate and effective linear parameter are

    T=(√Δ/λ)X,       f_eff=fλ/√Δ.

Under nonrenormalization running and dot X=−γ_X X, exact differentiation
gives

    dot T/T=−γ_eff,     dot f_eff/f_eff=γ_eff.

Thus f_eff T=fX is invariant under this coordinate/running dictionary.
The identities hold with either consistently truncated loop order. T and
X have different anomalous dimensions; neither is constant-canonical s.
At the reference scale T is a fixed multiple of X, so their logarithmic
radial derivatives coincide there. Along running characteristics that
factor itself runs and must be differentiated.

On the re-minimized tree valley a²=2fh/Δ and b=hX/λ,

    dot b/b=−γ_B,
    dot a/a=−γ_A+[λ²/Δ](γ_X−γ_B).

The second equation exposes the heavy-normal drift: re-minimizing the
classical valley at each scale is not the same as transporting the full
initial A background. When acting on the one-loop potential the mismatch
contributes at two-loop order. It is not licensed to drop it while claiming
a complete two-loop full-background matching.

## 5. What reduced two-loop logarithms can determine

There is a consistent reduced formulation. At fixed original singlet X,
define U_red by minimizing the full quantum potential over the physical
heavy normal fields, with gauge directions quotiented. Assume a local
smooth heavy branch and diagonal multiplicative field renormalization.
Then V_y=0 makes its CS equation exactly

    [Q∂_Q+β·∂_c−γ_X X∂_X] U_red=0.

At second order the reduced potential contains both genuine two-loop
graphs and the heavy-branch relaxation contribution

    U_red,2=V2|y0−(1/2)(V1_y)ᵀ H0_perp^−1 V1_y,

in real physical normal coordinates. A running classical-valley evaluation
of U0+V1 does not calculate that complete term. The heavy-normal derivatives
need not vanish and can themselves contain logarithms.

Nevertheless, the CS-determined Q logarithms of the *reduced* two-loop
potential can be reconstructed without separately evaluating that normal
gradient. Hold a chosen matching scale Q_m fixed during the partial CS
derivatives, and put δ=ln(Q/Q_m). Let

    C1=D1 U0, C2=D2 U0=2U0γ_eff,2,
    D1_red=β1·∂_c−γ_X,1 X∂_X,
    U1=U1bar−C1δ,       U1bar=U1(X,c,Q_m).

Then

    U2_log=−δ[D1_red U1bar+C2]+(δ²/2)D1 C1.

The signs follow by differentiating with respect to ln Q at fixed X,c.
C1 has no X dependence, so D1_red C1=D1 C1. A Q-independent finite
function U2bar(X,c,Q_m) remains unconstrained at this perturbative order.
It contains physical finite thresholds and finite normal relaxation.
Adding the known log polynomial is not evidence that this function is
zero, constant or negligible in pressure derivatives.

Evaluating the polynomial coefficients at the running endpoint rather
than at the central-scale coupling changes terms of higher perturbative
order. A field-dependent Q_m(X_reference) is a permitted scale prescription;
its derivatives must be retained in the final reference-field pressure
profile. During D1_red differentiation, Q_m is an independently held
matching parameter, not differentiated as an implicit coupling function.

For general f the complete threshold scales as

    CW(X,h,λ,g,f,Q)=f² CW_f=1(X/√f,h,λ,g,Q=1)
                       −ln(Q/√f) C1(h,λ,g,f).

This provides a useful factor-of-two/log convention check on the numerical
interface. It assumes the f=1 threshold uses the same full spectrum and
subtraction convention.

### A calculable finite normal-relaxation subset

The main route subsequently computes one finite part of U2bar, rather than
only its scale logs. On the invariant singlet slice at fixed original X,
directly from W,

    V0(a,b;X)=(f−15ha²)²+(15/2)λ²a⁴+30a²(hX−λb)².

At the classical valley the constrained Hessian is diagonal,

    Haa=120fh, Hbb=60λ²a², Hab=0.

Thus the full one-loop normal tadpoles g_a=CW_a and g_b=CW_b give

    δa=−g_a/Haa, δb=−g_b/Hbb,
    ΔU_relax=−(1/2)[g_a²/Haa+g_b²/Hbb].

These are coordinates on the fixed-X fiber, not an assumption that b is
orthogonal to the flat T direction. The scalar correction formula is
coordinate covariant with its corresponding Hessian and gradients.

The independent matrix-derivative inspection checks the full scalar,
gaugino-mixed Weyl and vector contributions to these tadpoles. For
h(v)=v²[ln(v/Q²)−3/2], h'(v)=2v[ln(v/Q²)−1] extends to h'(0)=0.
The first Fréchet trace derivative is therefore meaningful at Goldstone
zeros without substituting an off-shell negative mass into a real stable
potential. Arbitrary higher off-shell derivatives at that zero are not
justified by this first-derivative statement.

The R phase rotates X and B, giving F0=X²+30b² and δF=60bδb. This is a
geometric pullback from the shifted valley, not the direct finite one-loop
kinetic/two-point threshold. At fixed small phase frequency ω the same
constrained elimination gives the known subset of the Routhian

    Ω=U−ω²F0−(1/2)[g_a²/Haa+(g_b−ω²60b)²/Hbb].

The source square includes its ω⁴ term. On a loop-induced phase branch
ω² scales as fε³/L, while Hbb scales as fε, so the pure source-square,
cross and vacuum pieces all have the retained ε⁴f²/L² order. Dropping only
the ω⁴ term while retaining the others would be inconsistent. Corrections
from the ω-dependent normal Hessian enter at the next order under this
small-source hierarchy; its use away from that hierarchy needs a new check.

This subset uses an off-shell CW normal gradient in a fixed gauge and
subtraction convention. Its gauge/scheme dependence generally cancels only
after the genuine two-loop graphs and other matched terms are included.
Its pressure/root shifts are sensitivity calculations, not physical upper
or lower bounds on the remaining finite correction. The actual occupied-
phase analysis and state restrictions belong to `matter_coupling/`.

## 6. Controlled scope and pressure comparison

The exact one-loop CS cancellation and the two-loop RG coefficient
polynomials are earned. RG-resummed one-loop thresholds, optionally with
the displayed CS-required second-order scale logs, are partial higher-order
approximations. They are not a complete finite two-loop potential, a finite
matched kinetic action or a physical error bound. Small η scale variation
tests the retained logarithms; an unknown Q-independent U2bar can change
pressure derivatives without appearing in that variation.

Under h=ε ĥ, λ=ε λ̂, g=ε ĝ with fixed ratios and fixed positive f, use
z=hX/√c, c=fhλ²/Δ. On a compact nonsingular z interval the classical
backgrounds scale as √(f/ε), tree masses squared as εf, one-loop thresholds
as ε²f²/L, and ordinary two-loop/normal-relaxation terms by power counting
as ε⁴f²/L², possibly with logarithms. Thus a weak-coupling comparison is
better posed than the old order-one coupling grid. A uniform bound on the
coefficient functions and their derivatives, including the light/IR sectors,
has not been proved; the scaling is conditional perturbative counting.
Sending ε arbitrarily small at fixed f also grows field values in Planck
units, so the rigid limit alone is not a gravitational UV hierarchy theorem.

In particular the unbroken SU(3), SU(2), U(1) gauge/gaugino sectors, the
Goldstino and the R phase are not covered by a positive heavy transverse
gap. Gauge Goldstone modes also need the same consistent gauge/resummation
convention as the effective potential. Massless propagators can require IR
resummation or produce nonlocal occupied-state response; non-Abelian gauge
sectors additionally require their IR matching. Tree heavy-mode positivity
does not prove that the missing C² coefficient functions are uniformly
bounded. These are named obligations, not an assumed universal small-loop
theorem.

A precise conditional continuity test can be stated without pretending
that scale variation bounds finite matching. For the comparator portal,
write at a reference state

    u=U_s>0, W=2U_s+U_ss>0, N=U_ss−3U_s<0.

If an omitted matched correction obeys |δU_s|≤e1 and |δU_ss|≤e2 with

    e1<u,       2e1+e2<W,       3e1+e2<−N,

then positive source, radial stability and negative compressibility all
persist there. At a simple pressure root the first root shift is

    δs_root=−(δU_ss−3δU_s)/(U_sss−3U_ss)+higher orders.

These are exact local implications with explicit hypotheses. The unknown
finite two-loop and kinetic matching functions currently supply no proved
e1,e2 for the microscopic model. A numerically persistent root in several
partial schemes is therefore useful finite evidence, not a universal
quantum pressure exclusion.

This particular bound keeps the comparator portal fixed. A change in the
microscopic field-dependent kinetic/charge coupling changes the pressure
problem itself; potential C² bounds alone then do not suffice. For example
an angular metric's logarithmic derivative can receive a one-loop finite
matching correction, affecting its pressure numerator at the same order
as a two-loop potential derivative. Such metric derivatives must be matched
or bounded as well. This route does not identify the comparator's factor
three with a native occupied-phase condition.

`persistence_001/` turns this conditional criterion into a numerical budget
without calculating the missing correction. It rescales the immutable TP01
negative-numerator states X/X_min=1.2,1.3,1.5 to equal weak couplings
ε=.01,.03,.05,.1, using exact critical-shape homogeneity. For example at
ε=.03 and X/X_min=1.3, a common bound on the absolute first and second
logarithmic derivatives must be strictly below 1.95751771×10⁻¹⁰. If one had
proved the hypothetical bounds |δU_s|,|δU_ss|≤C ε⁴/L², this would require
C<6.02643029 at that state. Other states and couplings are retained in the
12-case output. No such C has been measured or bounded here; the numbers
are the missing obligation, not a positive conclusion at ε=.03.

For a fixed uniformly bounded derivative coefficient, the allowed C scales
as ε⁻² and formal asymptotic persistence follows as ε tends to zero. The
same follows for bounded polynomial logarithmic enhancements dominated by
ε². This conditional asymptotic statement is distinct from a certified
result at any of the four finite couplings. The numerical baseline itself
is high-precision evidence, not an interval certificate.

Finally the old exp(2s) matter portal remains a comparator. If occupied
microscopic modes instead generate a different field-dependent rest mass,
kinetic factor, charge constraint or phase metric, their pressure problem
must be rederived. The RG and threshold dictionary does not select that
state or import a portal by itself.

## 7. Evidence and review boundaries

`contract.json` was frozen before the tensor run. `run_001/manifest.json`
records a completed bounded execution, seven coefficient cases and eight
exact symbolic identities, with 89,505,792 bytes observed RSS. Only supported
wall/CPU/thread caps were requested; no unsupported hard memory or affinity
cap is claimed. `INPUTS.json` pins raw action and TP01 source bytes.

The separate `persistence_contract.json` was frozen before its 12-case
arithmetic budget calculation; `persistence_001/manifest.json` records that
completed run. It reads the pinned existing TP01 derivative output, rather
than evolving the system or estimating unknown two-loop corrections.

This route independently reconstructed the formulas before reading the
coordinator's algebra or reviewing the RG implementation. External transfer
was checked against the exact primary source; no novelty claim is made.
The separate implementation review and final checks are recorded in
`IMPLEMENTATION_REVIEW.md` and `VERIFICATION.json`. Agent agreement is not a
physical validation or a formal proof-assistant certificate.
