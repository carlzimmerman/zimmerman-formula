# Exact static source variation of the shared-leaf repair

The geometric repair preserves the coincident weak-field action through cubic order, but changes both lapse and spatial metric Euler equations at **cubic field order**. In particular the first added relative lapse source is 2K(1+λ) div[d1² grad r1] at order ε³. This is a genuine source correction, not a transfer of the old fitted static solution. The leading MOND norm-cube contribution is unchanged; exact noncoincident source equations are different. No observational verdict, cold abundance or 32π selection follows.

This is an action-level static variation with both independent leaf metrics and lapses. It applies to any spatial dimension n≥3, common timelike clock θ=t, stationary zero shifts, positive lapses and positive definite leaf metrics. Boundaries require compactly supported variations or the displayed surface flux. Matter, Einstein and shear terms are unchanged and must still be solved together. The statements are not obtained by freezing the spatial metric in the full source problem.

## 1. Actual static interaction

Use the parent covariant action, individual Einstein coefficient M=2K>0 and interaction

S_int=2K a0²∫dt d^n x v M_eff(I),
v=sqrt(NL)(det γ det γhat)^(1/4),
r=ln(N/L), w_i=∂i r,
h=(γ+γhat)/2, d=(γ−γhat)/2,
Hλ=h+λ d h^-1 d, Bλ=Hλ^-1,
I=w^T Bλ w/a0².

Here λ>0, a0>0; h,d are covariant matrices. The inherited envelope satisfies M_eff(I)=−A+I/2−I^(3/2)/12+O(I²) near the coincident weak-field regime. The exact variations below can use any differentiable M_eff on I≥0 with finite first derivative at zero; they do not insert a new fit. The arithmetic parent uses Ba=(γ^-1+γhat^-1)/2 instead. All covariant operator dependence is varied before choosing a source branch.

For stationary zero shifts, normalized acceleration restricted to the clock leaf is ∂i ln lapse. Shear and its first variation vanish because each extrinsic curvature vanishes. Thus the retained shear repair adds no static first-order source row. The clock equation is also admitted at θ=t: a fixed-metric clock variation gives δa_g,i=δa_h,i=−∂i πdot, while induced leaf metrics have no first variation. Their relative projected acceleration therefore has zero first variation. This is a static first-variation statement, not static clock health.

## 2. Exact lapse variations and boundary

For log-lapse variations δn=δ ln N and δl=δ ln L, δv=v(δn+δl)/2 and δI=2Bλ^{ij}w_j∂i(δn−δl)/a0². Denote m=M_eff(I), m1=M_eff'(I). Integration by parts gives the interaction Euler densities

E_n=K a0² v m−4K ∂i(v m1 Bλ^{ij}w_j),
E_l=K a0² v m+4K ∂i(v m1 Bλ^{ij}w_j).

The boundary term is 4K∫∂Ω v m1 Bλ^{ij}w_j n_i(δn−δl). Thus E_n+E_l=2K a0² v m exactly. The normal energy densities are ρg,int=−E_n/(N sqrt(det γ)) and ρh,int=−E_l/(L sqrt(det γhat)). Constant m=−A produces the retained geometric-mean vacuum source; it must be subtracted consistently in a source interpretation. These formulas include the direct volume term as well as the divergence and are not a Poisson law by themselves.

## 3. Full spatial metric differential and stress

Set z=Bλ w and q=h^-1 d z. The matrix differential is

δHλ=δh+λ(δd h^-1d+d h^-1δd−d h^-1δh h^-1d),
δBλ=−Bλ δHλ Bλ.

Contracting with w gives

w^T δBλ w=−(zz^T−λqq^T):δh−λ(zq^T+qz^T):δd.

With δh=(δγ+δγhat)/2 and δd=(δγ−δγhat)/2, define

Ug=[zz^T−λqq^T+λ(zq^T+qz^T)]/2,
Uh=[zz^T−λqq^T−λ(zq^T+qz^T)]/2.

The exact coordinate Euler densities for the covariant spatial metrics are

Eγ=(K a0²/2) v m γ^-1−2K v m1 Ug,
Eγhat=(K a0²/2) v m γhat^-1−2K v m1 Uh.

The actual interaction spatial stresses are Tg^{ij}=2Eγ^{ij}/(N sqrt(det γ)), and the hatted counterpart. These are symmetric stresses; they are not assumed isotropic or pressureless. The inverse variation is ultralocal in γ,γhat, while the lapse variation has the spatial boundary divergence. There are no hidden derivatives of a fixed external reference metric.

For direct comparison the arithmetic metric contraction tensors are Ua,g=(γ^-1 w)(γ^-1 w)^T/2 and Ua,h=(γhat^-1 w)(γhat^-1 w)^T/2. The same volume and lapse formulas then apply with its own I,m,m1. Thus exact subtraction must vary both the inverse and the envelope evaluation, not merely replace the flux coefficient at fixed I.

## 4. First weak-field difference and leading MOND scope

Expand about a coincident flat leaf, using bounded smooth coefficient fields with derivatives not increasing as ε shrinks:

γ=1+εG1+O(ε²), γhat=1+εGhat1+O(ε²),
d=εd1+O(ε²), d1=(G1−Ghat1)/2,
r=εr1+O(ε²), w=εw1+O(ε²), w1=grad r1.

Matrix inverse expansion, without assuming commuting perturbations, gives

Bλ−Ba=−(1+λ)ε² d1²+O(ε³),
Iλ−Ia=−(1+λ)ε⁴ w1^T d1² w1/a0²+O(ε⁵).

Since M_eff'(0)=1/2, the first action difference is

ΔS_int=−K(1+λ)ε⁴∫w1^T d1²w1+O(ε⁵).

The norm-cube changes only at order ε⁵; the constant vacuum cancels in this comparison. In the Euler equations, differentiating the quartic term lowers field order. The leading differences are

ΔE_n=+2K(1+λ)ε³ div(d1²w1)+O(ε⁴),
ΔE_l=−2K(1+λ)ε³ div(d1²w1)+O(ε⁴),
ΔEγ=−[K(1+λ)/2]ε³[w1(d1w1)^T+(d1w1)w1^T]+O(ε⁴),
ΔEγhat=−ΔEγ+O(ε⁴).

The leading direct volume difference is order ε⁴ and enters the sum row, not the cubic relative divergence. Normal stress conversion can add only higher-order factors to these leading differences. The source correction has no definite local sign, though the action difference is nonpositive for real d1,w1 and λ>0.

The leading nonrelativistic MOND relation obtained from the retained critical quadratic action plus the cubic norm term is consequently unchanged in this simultaneous weak-field expansion. Its norm-cube Euler source is quadratic in field amplitude; the new relative lapse source is cubic. This is a perturbative statement about the same leading action, not exact conservation of the old spherical response at finite fields. Strong derivatives, a noncoincident background, degenerate leading balances or finite post-Newtonian effects require the new full equations. Neither a uniform force error bound nor an observational score is claimed.

## 5. Exact isotropic radial diagnostic

For γ=G(r)1, γhat=Ghat(r)1 with positive scalar coefficients, hs=(G+Ghat)/2 and ds=(G−Ghat)/2,

Bλ=hs/(hs²+λds²), Ba=hs/(hs²−ds²),
Bλ−Ba=−(1+λ)hs ds²/[(hs²+λds²)(hs²−ds²)].

The radial lapse divergence in n dimensions is r^(1−n) d_r[r^(n−1) v m1 B r']. Here v=sqrt(NL)(G Ghat)^(n/4), in Cartesian coordinate measure before the usual radial Jacobian. This exact example demonstrates altered flux and spatial stress at finite metric mismatch, even though both inverses coincide at ds=0. The envelope derivative generally changes as well because I changes. No QUMOND nonspherical field law is inferred from this diagnostic.

## 6. Evidence and first remaining implication

Exact checks reconstruct the general matrix differential from nonsingular noncommuting SPD data, lapse direct and divergence coefficients, metric stress tensors, exchange covariance, inverse/action weak-field orders, first Euler corrections and isotropic radial difference. Controls omit the direct volume, freeze the leaf inverse during spatial variation, or assert exact flux preservation off coincidence. The analytic formulas carry the general-dimensional claim; fixtures are only bounded corroboration.

The next source obligation is to solve the new coupled static Einstein/lapse/spatial/clock boundary problem, with a specified conserved matter action and physical force/lensing dictionary. Leading-kernel preservation is insufficient for carrying over Claude's field-PDE or observational results. The independently positive radiation principal repair and the open finite-k canonical problem concern this same changed action, but do not complete static source matching or select A.
