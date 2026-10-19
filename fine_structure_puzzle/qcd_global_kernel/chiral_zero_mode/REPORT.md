# A matched compact chiral correction, with its first nonconstant-pion interaction

FSP-008 now has an evaluated continuation of FSP-003's compact chiral
calculation. The raw SU(2) Haar/Dashen partition was already known in this
project; the initial dispatch overlooked that antecedent. It is not claimed
as a new result here, and its old numerical grids were not rerun.

The new result is the exact finite-charge replacement of an already present
Gaussian constant mode, its fixed-parameter sphere stress/charge derivative,
and the first nonconstant-PION interaction with the compact mode. Two
distinct double-counting subtractions are now explicit.

Let x=F²M²V, y=uCV, u=e², V=8π²/(3H⁴), and use the inherited normalized
partition Z(x,y)=∫₀¹exp(−ys)I₀(x√(1−s))ds. For x>0,x+2y>0,

    Qrep=Z(x,y) / [sqrt(2/pi) exp(x)/(sqrt(x)(x+2y))].

A scalar determinant that includes its massive constant modes is multiplied
by Qrep. The aligned classical mass vacuum exp(x) has been removed in this
replacement convention. With m=⟨a₀⟩, q=⟨s⟩, c=Cov(a₀,s), vₛ=Var(s),
the new finite-radius responses are

    V rho_rep=x(1−m)+yq−3/2,
    partial_u rho_rep=C[q+x c−y vₛ].

These include the change in the probability distribution. In the formal
positive-mass large-volume saddle, writing a=F²M²,b=uC,

    rho_rep=k(a,b)/V²+O(V^-3),
    k=1/[2(a+2b)]+1/(8a)−a/(a+2b)²,
    partial_u rho_rep=C(3a−2b)/[(a+2b)³V²]+O(V^-3).

Thus the isolated differential charge response can be negative at finite
positive charge. At the new test point a=1,b=2,V=768, the run obtains
V²rho_rep=0.185272721906446… (saddle limit 0.185) and
V²partial_u rho_rep/C=−0.00803658055754… (limit −0.008).
These are dimensionless mathematical checks, not fitted physical inputs.

The first nonconstant-pion contraction is also calculated. Put
g=Gbar_S4(H)/F², with the constant harmonic omitted and a UV prescription
specified. Quaternion expansion gives

    ⟨a₀(z)⟩_pi=(1−3g/2)a₀,
    ⟨s(z)⟩_pi=(1−4g)s+2g.

Relative to a massless nonconstant Gaussian baseline this gives
δW=gT, T=2y+(3x/2)m−4yq. The indispensable +2y term is the induced
source-independent-in-U factor exp(−2yg).

For assembly with a MASSIVE nonconstant determinant, g(3x/2+2y) is
already present as its aligned mass tadpole. The genuinely extra correction
is consequently

    δW_extra=g B, B=(3x/2)(m−1)−4yq.

Its normalized charge difference is
g[(3x/2)(m(x,y)−m(x,0))−4yq(x,y)]. DERIVATION.md gives the complete
fixed-parameter metric and charge derivative, including third cumulants.
At x=0 the unsubtracted contraction has T=y²/3+O(y⁴), while the extra
piece B=−2y+y²/3+… cancels the +2yg already in the massive determinant.

The S4 nonconstant tadpole has a curvature UV pole R/(96π²ε). In one
explicitly defined zeta finite-part scheme,

    Gbar=H²/(8pi²)[log(mu²/H²)+2 EulerGamma−8/3].

This finite number is not a matching prediction. Curvature times quark-mass
and curvature times electromagnetic source operators occur at the SAME
epsilon order as gT. Their independent finite coefficients, source contacts,
and a common subtraction convention are required. In particular this zeta
finite part is not silently combined with the frozen sphere determinant's
mass-dependent decoupling prescription.

The authoritative bounded mathbox v2 run completed in 4.14 seconds and its
manifest validates with unchanged current inputs. It passed 143 controls:
exact source contractions, independent numerical metric/charge differences,
third-cumulant identities, doubled quadrature and a second precision, a
separate tanh-sinh integral, new saddle points, and a bounded S4 spectral
Laurent calculation. The 40/60-digit discrepancy is at most 1.82×10⁻³⁶;
the Laurent finite-part difference is 3.96×10⁻²⁴. Numerical quadrature is
not interval-certified. See run_001/RESULTS.json, run_001/manifest.json and
REPRODUCE.md for the actual domain and command.

This is not the full NLO QCD+QED epsilon partition. A charged compact
orientation induces a photon seagull/determinant; pion-photon mixing graphs
can enter at this same order. Those terms, gauge factors, independent
curvature matching, heavy modes and the absolute QCD normalization remain
absent. Source-independent collective/kinetic factors cancel the stated
normalized ratios, but cannot be discarded in an absolute sphere stress.

Controlled epsilon use requires F/H≫1 and both M/H≪1 and M_charged/H≪1.
Fixed x,y scaling changes M² and u as H⁴. The large-x saddle checks cannot
be promoted to a physical fixed-mass, fixed-alpha H→0 limit. The genuinely
massless compact partition is finite, but Qrep alone has a singular
Gaussian denominator; the product must be combined before that limit.
DERIVATION.md records the noncommuting charge/mass derivative orders.

No full QCD H-linear coefficient, proton denominator, R(alpha), Thomson
matching or value of alpha is determined. The surviving new result is an
explicit unfitted interaction and response, with the missing same-order
photon, curvature and normalization data identified precisely.
