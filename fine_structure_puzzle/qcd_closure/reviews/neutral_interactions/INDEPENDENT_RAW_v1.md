# Independent first-interaction derivation on closed S3

Saved before reading any `qcd_closure/neutral_interactions/` file or any
coordinator interaction coefficient. FSP-005 independent review task. This is
a hand derivation; no new mathematical experiment has been run. The prior
QED lane remains frozen. Existing knowledge used: elementary S3 scalar
harmonics and the meromorphic coth summation identity. No parent source
receipt is treated as independent source authentication for these formulas.

## 1. Model, loop counting and canonical modes

The supplied three-dimensional action is

    S=∫_(S3_R) sqrt(g) [(∇ϕ)²/2-u cos(ϕ/√κ)],
    u=κm²>0,   V=2π²R³,   L fixed,
    τ_s=(1/L)∂_V W,   W=-log Z.

The scalar is compact, period 2π√κ. We expand around a stable minimum, so
there is no cubic and

    S=-κm²V + (1/2)∫ϕ(-Δ+m²)ϕ
                       -m²/(24κ)∫ϕ⁴ + O(ϕ⁶/κ²).

Thus the conventional quartic coupling is λ=-m²/κ. Its negative sign is
consistent with the stable full cosine. We compute only the first vacuum
interaction order in m/κ, at mR>1, in this stable saddle expansion. A free
Gaussian determinant is counted once with all canonical modes; there is no
separate compact constant Gaussian determinant to multiply into it. Smooth
maps S3→S1 have no winding class; singular defects or additional UV sectors
are not computed by this perturbative diagram.

## 2. Coincident propagator in the determinant-consistent scheme

Set n=l+1, n=1,2,... . The scalar eigenvalues and multiplicities are

    A_n=(n²+z²)/R²,     d_n=n²,
    z=sqrt(m²R²-1)>0.

The finite-part/zeta coincident propagator is

    g_R(m)=(1/V)Tr A^-1
          =[1/(2π²R)] FP Σ_(n>=1) n²/(n²+z²)
          =-z coth(πz)/(4πR).

Indeed FPΣ1=ζ_Riemann(0)=-1/2 and
Σ_(n>=1)(n²+z²)^-1=[πz coth(πz)-1]/(2z²). The poles/finite parts give
FPΣn²/(n²+z²)=-(πz/2)coth(πz). This is the derivative of the same
regularized determinant, ∂_(m²)W_G=Vg_R/2. The flat limit is

    g_∞(m)=-m/(4π).

A negative finite coincident value is not a negative bare covariance. It is
the finite part after subtracting the positive linear UV divergence. All
products below mean products of consistently renormalized tadpoles, with
local mass/vacuum subdivergence counterterms supplied, not a claim that an
unregulated double sum equals an arbitrarily squared finite number.

For example, if G_bare=C_Λ+g_R, the quartic diagram is
-aV(C_Λ+g_R)² with a=m²/(8κ). A tadpole mass counterterm
δm²_UV=+m²C_Λ/(2κ) cancels the nonlocal subdivergence in W; its vacuum
insertion is +2aVC_Λ(C_Λ+g_R). A vacuum counterterm removes the remaining
+aVC_Λ². This leaves -aVg_R² in the chosen finite-part convention. Finite
local curvature terms must still be fixed in that convention. This explicit
subtraction is needed before interpreting a two-loop finite part.

## 3. Full quartic figure-eight at fixed Lagrangian mass (path A)

At this order W_int=<S4>_G. Wick's theorem gives <ϕ⁴>=3g_R², hence

    W_A,2=-m²V g_R²/(8κ),
    f_A,2=W_A,2/V=-m²(m²-R^-2)coth²(πz)/(128π²κ).

No factor 1/2 or second diagram is missing: the vertex has coefficient
-m²/(24κ), and the three pairings produce -m²/(8κ). The free Gaussian
W_G and classical -κm²V are separate orders.

For f=W/V on S3 at fixed L,

    τ_s=(1/L)[f+(R/3)∂_R f].

Writing c=coth(πz), s=csch²(πz), and using Rz'=m²R²/z,

    τ_A,2= -m²/(128π²κL)
           [(m²-1/(3R²))c² -(2π/3)m² z c s].

The infinite-volume value is -m⁴/(128π²κL). Therefore the flat-subtracted
stress obeys

    Δτ_A,2=+m²/(384π²κL R²)
                     + exponentially small terms as R→∞.

The algebraic part of this particular diagram is exactly a constant plus
R^-2. There is no algebraic R^-1, R^-3 or R^-6 term once all modes are
included. The exponential terms carry polynomial R prefactors after metric
differentiation and use z=sqrt(m²R²-1), not merely mR.

## 4. Fixed flat pole mass (path B)

The flat tadpole self-energy from λ=-m²/κ is

    Σ_∞=(λ/2)g_∞=+m³/(8πκ),
    M²=m²+Σ_∞+O(κ^-2),
    m²=M²+δm²,  δm²=-M³/(8πκ)+O(κ^-2).

At the retained vacuum-loop order the Gaussian mass-retuning insertion is

    W_mass=(δm²/2)V g_R(M).

Using δm²=M²g_∞(M)/(2κ), and evaluating the quartic at M to this order,

    f_B,2= -M²g_R²/(8κ)+M²g_∞g_R/(4κ)
           = M²/(8κ)[g_∞²-(g_R-g_∞)²].

Its flat value is +M⁴/(128π²κ). The unambiguous flat-subtracted retained
interaction contribution is the completed square

    Δf_B,2= -M²/(8κ)[g_R(M)-g_∞(M)]²,
    Δτ_B,2= -M²/(8κL)
       [(g_R-g_∞)² +(2R/3)(g_R-g_∞)∂_R g_R].

The sign of W_mass is essential. It cancels the curvature term linear in
g_R-g_∞ at this order; omitting it gives the wrong fixed-pole result.
Since, apart from exponentials,

    g_R-g_∞ = 1/(8πM R²)+1/(32πM³R⁴)
                                      +1/(64πM⁵R⁶)+O(R^-8),

we find

    Δf_B,2= -1/(512π²κR⁴)
                         -1/(1024π²κM²R⁶)+O(R^-8),
    Δτ_B,2= +1/(1536π²κL R⁴)
                         +1/(1024π²κL M²R⁶)+O(R^-8)
                         + exponential terms.

Thus the leading soft diagram response changes from R^-2 on path A to R^-4
on path B, in the stated matching and local-curvature convention.

There is an important absolute-vacuum bookkeeping qualification. Retuning m²
in the *full supplied cosine* changes the classical constant too:

    δS_classical=-κδm² V=+M³V/(8π)+O(V/κ).

The displayed leading shift is extensive and cancels in a flat-subtracted
stress. For a full unsubtracted vacuum energy through order 1/κ, the next
(order κ^-2) pole-mass retuning times the classical κ term also matters,
as does independent vacuum matching. The one-tadpole mass relation alone
cannot fix that absolute local constant. It suffices for the geometry-dependent
retained two-loop difference above. Equivalently one can state the truncated
one-tadpole matching prescription exactly and keep its chosen vacuum
counterterm explicit. One must not silently discard the classical retuning
when claiming an absolute fixed-M vacuum energy.

## 5. Correct constant-mode isolation

The canonical normalized constant harmonic is V^-1/2 and has eigenvalue m²,
so

    g0=1/(Vm²),      g_>=g_R-g0.

The full figure-eight contains all three pieces

    W_A,2= -m²V/(8κ)[g0²+2g0g_>+g_>²].

The isolated constant-only diagram is

    W_00=-1/(8κm²V),
    f_00=-1/(8κm²V²),
    τ_00=+1/(8κLm²V²)=1/(32π⁴κLm²R⁶).

It is not an additive correction after the full g_R² result has already
been used. Cross and nonconstant terms cancel the spurious algebraic terms
that would be inferred from retaining W_00 alone. For instance, exact g_R²
has only the constant and R^-2 algebraic densities on path A.

The canonical compact constant integral provides an independent check. With
q0=√V ϕ0, dq0 measure μdq0/√(2π),

    Z0=μ sqrt(2πκV) I0(κm²V)
       ~ (μ/m)e^(κm²V)[1+1/(8κm²V)+...],
    W0=-κm²V+log(m/μ)-1/(8κm²V)+... .

The normalization cancels the Haar-integral log(V), and the quartic term
matches W_00. This integral still omits interactions involving nonconstant
modes. It does not supply the two-loop field result by itself.

At fixed M, the same split applies separately to g_R and the mass-counterterm
insertion. The full completed-square expression already contains the constant
mode once. It cannot be augmented by another W_00.

## 6. Curvature, hard modes and limits of the claim

The declared action is minimally coupled and the finite-part convention must
be used consistently in W_G, g_R, counterterms and W_2. If a dimensional
reduction or UV completion supplies additional local terms,

    W_hard=∫sqrt(g)[b0+b1 ℛ+b2 ℛ²+...],   ℛ=6/R²,

their contributions are

    τ_hard=(1/L)[b0+2b1/R²-12b2/R⁴+...].

A curvature mass coupling ξℛϕ²/2 is additional EFT matching data; fixing
only the flat mass does not determine it. Such data can alter the displayed
curvature response. The supplied minimal cosine model and a fixed common
local scheme define the soft benchmark, not the full hard-mode matching.
Local field/coupling counterterms tied to the same cosine must be treated
consistently; finite pole matching adds the mass insertion in section 4.

All quantities are at fixed L and κ. No dependence of these inputs on R is
included in ∂_V. Compact nonperturbative effects, higher cosine vertices,
higher vacuum loops and additional gauge/charged modes are outside this
calculation. No physical electromagnetic alpha or all-loop QCD result is
claimed.

## 7. Independent checks to carry into the audit

The coefficient and sign arise from (i) three Wick pairings, (ii) the
negative cosine quartic, (iii) the exact all-mode finite tadpole, (iv) the
positive flat tadpole self-energy and negative fixed-pole mass counterterm,
and (v) the actual spatial derivative f+R f'/3. The completed square is an
orthogonal matching check. The compact constant saddle is an orthogonal
check of the constant-only diagram and canonical normalization.

No numerical experiment was required for these identities. The next step is
to read the coordinator interaction packet and compare exact conventions,
subdivergence treatment, metric derivative, fixed-pole path, precision
coverage and claims about hard terms. This raw file is frozen before those
reads; corrections, if needed, will be in a separate review file.
