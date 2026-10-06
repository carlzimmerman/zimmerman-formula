# Rolling kinetic braiding: a genuine classical vacuum map, but the sourced force is not MOND

This calculation moves beyond a frozen scalar P(X) block: Einstein lapse/shift mixing supplies a healthy rolling de Sitter branch even though K_X<0. A logarithmic/inverse-root action has an exact covariant classical vacuum-shift map, not merely a homogeneous cancellation. Its minimally sourced near-zone force, however, has Vainshtein rather than MOND scaling. Neither result selects 32π. The class of tadpole-free KGB self-tuning is established in Bernardo (2021); the useful project result here is the joint normalization, vacuum map, constraint stability, and sourced mass/radius scaling audit. No claim of new literature theorem is made.

Requested phase base and observed initial HEAD: `81af81ba8a7207bca2bc4f13375c757feee7afcd`; later concurrent HEAD: `6b0d8d04d2152c8bcc9c4f85c290d21905070514`. Actual file hashes, not either commit alone, determine run inputs. All writes belong to this directory. Earlier SELF_TUNING_GALAXY_BRIDGE_RESULTS and DERIVATIVE_BRIDGE_RESULTS use restricted auxiliary bridges and do not establish the coupled response below. Existing qwen cubic-debraiding and KGB tangency work was inspected; these are related established routes, not evidence of global project novelty.

## 1. Covariant action, matter, and general dimension

Use signature (−,+,…,+), X=−∇φ·∇φ/2, d=n+1, n>1, q=φ̇>0, and c_light=1:

S=∫√−g [M_* R/2 + K(X) − G(X)□φ − ρ_v] + S_m[g,ψ].

M_* is the Einstein coefficient (Mpl² in four dimensions); baryons follow g and ∇T_m=0. Their force is the metric force, not an assumed α∇φ. The exact shift current and homogeneous stress are

j^μ=(K_X−G_X□φ)∇^μφ−G_X∇^μX,  ∇_μj^μ=0,
J=−j⁰=qK_X+nHq²G_X,  (a^nJ)̇=0,
ρ_φ=qJ−K,  p_φ=K−2XG_X q̇,
A_n M_*H²=ρ_v+qJ−K,  A_n=n(n−1)/2.

For an exact rolling de Sitter state q,H constant, J=0 is necessary. Thus
H=−K_X/(nqG_X),  ρ_v=A_nM_*H²+K(X).
Constant G is a boundary term and cannot supply this branch. For K=kX^p,G=gX^r with kp gr≠0,
H=−kp/(n gr√2) X^(p−r−1/2).
A continuum of different X at the same H requires r=p−1/2. This is a functional tuning of action coefficients, not a predicted H. The general functional condition is
K_X+nH_*√(2X)G_X=0 on the visited X interval.
It is Bernardo eq. (3.28) at zero tadpole in n=3, with A=K,B=G,h=H_* and restored Mpl². His no-tempering result concerns a specified well-tempering degeneracy; it does not eliminate this trivial-scalar self-tuning branch.

## 2. Full four-dimensional cosmological constraint stability

Here and in the local force calculation n=3. Take Einstein G4=Mpl²/2, G5=0, G3=G, no φ dependence. Kobayashi–Yamaguchi–Yokoyama v2 eqs. (56),(57),(60)–(64), not the numbering of later versions, give
Θ=Mpl²H−qXG_X,
Σ=XK_X+2X²K_XX+12HqXG_X+6HqX²G_XX−3Mpl²H²,
G_S=Σ Mpl⁴/Θ²+3Mpl²,
F_S=(1/a)d[a Mpl⁴/Θ]/dt−Mpl².
These multiply ζ̇² and −a^−2(∇ζ)² after lapse and shift have been eliminated. On the functional branch and constant q,H_*, put z=XK_X/(3Mpl²H_*²). Differentiating the branch condition is essential; imposing J=0 only at a single point is insufficient. One obtains
Θ=Mpl²H_*(1+z), Σ=−3Mpl²H_*²(1+2z),
G_S=3Mpl² z²/(1+z)², F_S=−Mpl² z/(1+z), c_s²=−(1+z)/(3z).
Hence homogeneous scalar ghost/gradient health is −1<z<0. z=0 is degenerate; z=−1 is a singular constraint inversion. Tensor coefficients are Mpl²>0. Subluminal scalar speed, if additionally imposed, restricts z≤−1/4. This is the full cosmological scalar constraint action, not full finite-gradient stability or a quantum EFT proof. Bernardo eq. (3.71), −3H_*²/X<K_X<0 in his Mpl²=1 units, agrees exactly.

Canonical positive k has z>0 and a gradient instability, despite the braid. Negative k with G=g√X, g>0 gives H_*=−√2k/(3g)>0 and a healthy interval 0<ρ_v/(3Mpl²H_*²)=1+z<1. It cannot screen arbitrarily large positive vacuum density while remaining in this interval. More generally negative k,p>0 yields ρ_v/ρcrit=1+z/p. This is a result about those powers, not all KGB.

## 3. A legitimate escape: exact logarithmic vacuum map

Choose, on X>0,
K=−c ln(X/Xref), G=−√2 c/(nH_*) X^−1/2,
with c>0,Xref>0,H_*>0. An additive constant in G is irrelevant with appropriate boundary conditions. Then
J=√2 c X^−1/2(H/H_*−1),
ρ_v=A_nM_*H_*²−c ln(X/Xref),
X=Xref exp[(A_nM_*H_*²−ρ_v)/c].
In four dimensions z=−c/(3Mpl²H_*²) is independent of ρ_v. Thus 0<c<3Mpl²H_*² gives the healthy cosmological constraint branch for every finite ρ_v at formal classical level. This evades the canonical-power vacuum range restriction without claiming observational viability.

Stronger, define s=exp[−Δρ/(2c)] and φ_new=sφ, ρ_v,new=ρ_v+Δρ. Then X_new=s²X and □φ_new=s□φ:
K(s²X)=K(X)+Δρ,
G(s²X)□φ_new=G(X)□φ.
The whole covariant integrand −ρ_v+K−G□φ is identical pointwise under this map, while the Einstein and minimally coupled matter terms are unchanged. Consequently any classical solution in the X>0 domain maps to a solution with the identical metric and matter and different vacuum density. This is a map between theories with different constant vacuum parameters, not a shift symmetry inside one fixed-ρ_v theory. It does not prove dynamical tracking through an actual vacuum phase transition. Singular behavior as X→0, field-normalization dependence of a cutoff, radiative corrections, finite-gradient characteristics, and cosmological initial conditions remain open. H_* is explicitly an action parameter, and this map supplies no numerical a0/H_* selection.

## 4. Sourced near-zone force with the rolling background retained

A scalar φ=qT in static coordinates would incorrectly omit the background gradients. In de Sitter static coordinates f=1−H_*²r²,
φ_0=q[T+(1/(2H_*))ln f],  φ_0,r=−qH_*r/f,
X_0=q²/2, □φ_0=−nH_*q.
Perturb by a stationary χ(r), u=χ′. Direct expansion of j^r on the fixed de Sitter metric gives the exact linear-in-u coefficient
j^r_linear={G_XH_*q[(n−2)−nH_*²r²]−(K_XX+nH_*qG_XX)q²H_*²r²}u.
The differentiated functional branch gives K_XX+nH_*qG_XX=K_X/q²=−nH_*G_X/q, so this coefficient reduces to (n−2)H_*qG_X. This Hq term must be retained even in a subhorizon calculation.

For the following coupled leading near-zone expansion assume n=3, H_*r≪1, weak metric potentials, X close to positive X0, finite controlled K/G derivatives at X0, |u|/q≪1, and no singular homogeneous scalar charge at the center. Keep the linear rolling term and the quadratic braiding current; discard relative weak-potential, H²r², and higher δX/X0 corrections. In the inner nonlinear regime also require |u|≫qH_*r; this is compatible with small |u|/q. Keeping large derivative-current terms does not license arbitrarily large δX. The reduced source calculation is leading asymptotic, not an exact global solution of all Einstein equations.

In ds²=−(1+2Ψ)dt²+(1−2Φ)d x², the leading scalar density and Einstein constraint are
δρ_φ=−G_X q²∇²χ,  Φ=Ψ at this order,
Ψ′=G_N,b M_b/r²−G_Xq²u/(2Mpl²), G_N,b=1/(8πMpl²).
The rolling lapse tilt supplies ∂rX≈−q²Ψ′ and therefore +G_Xq²Ψ′ in the scalar current. Minimal matter does not directly inject shift charge. The regular integrated scalar equation is
0=j^r≈Z u−2G_Xu²/r+G_Xq²Ψ′, Z=H_*qG_X,
[Z−G_X²q⁴/(2Mpl²)]u−2G_Xu²/r=−G_Xq²G_N,bM_b/r².
The mixing subtraction is exactly the term in Bernardo's gradient coefficient (3.65); discarding it loses the (1+z) factor and misses the cosmological stability boundary. On the functional branch its linear coefficient is Z(1+z)>0 for −1<z<0.

Write v=u/q and m=G_N,bM_b. The physical force is
H_*(1+z)v−2v²/r=−m/r²,  δg=zH_*v,
v=−2m/{r²[H_*(1+z)+√(H_*²(1+z)²+8m/r³)]}.
This is the normal root v→0 as M_b→0. It is sourced even without a direct scalar coupling, through Einstein mixing. Its limits are
inner: v≈−√(m/(2r)), δg≈(−z)H_*√(m/(2r));
outer: v≈−m/[H_*(1+z)r²], g_total≈m/[(1+z)r²].
Inner mass exponent 1/2 matches one MOND feature, but radius exponent −1/2 does not match MOND −1. The transition r_V³=8m/[H_*²(1+z)²] has mass dependence M_b^(1/3); the acceleration at that radius scales M_b^(1/3), not as a universal a0. The numerical derivative controls test both exponents independently.

For logarithmic K, z is fixed, so the metric response above is independent of q and ρ_v, consistently with the exact covariant vacuum map. Inner weak gravity m/r≪1 gives |u|/q≈√(m/(2r))≪1, so the regular galaxy branch remains timelike and does not reach a spacelike MOND kinetic branch merely by going below the horizon scale. Static reduced radial/tangential eigenvalues of the eliminated current are positive on this root: a−4G_Xu/r and [a²−2aG_Xu/r+4G_X²u²/r²]/[a−4G_Xu/r], a=Z(1+z). This is ellipticity of the reduced spatial operator, not positivity of the whole covariant action at finite gradients.

## 5. Attempted same-operator MOND escape and its precise failure

The power p=3/2 requires G=gX for constant H_*, with K=−C X^3/2 and H_*=C/(2√2g). An even continuation K=−C|X|^3/2 has positive K_X on the spacelike side. If one *also* changes the theory to give baryons a conformal coupling e^(2αφ)g, the flat spacelike |u|≫q current would be
j^r≈[γ−2g/r]u², γ=3C/(2√2)=3gH_*.
Kinetic dominance would yield the desired u∝√M/r. But |braid/kinetic|=2/(3H_*r) is large throughout the subhorizon region: the same braid needed for the rolling functional branch defeats that balance. Moreover the minimally sourced weak-field solution in section 4 does not satisfy |u|≫q. It is therefore invalid to transplant this spacelike balance to that solution. Pure G∝(−X)^r braiding dominance instead gives u∝M^(1/(2r)) r^−1/(2r) in three spatial dimensions; no single power has both desired exponents.

A conformal baryon coupling explicitly changes the matter conservation dictionary: ∇μT_m^μν=αT_m∇νφ and ∇μj^μ≈αρ_b in the nonrelativistic limit, and the test force includes αu. At fixed α it also breaks the logarithmic vacuum-rescaling map. Neglecting the braid in this different toy theory would give a0=α³/(4πγG_N,b), whose ratio to H_* is an independent action combination, not 32π. No all-KGB MOND no-go is claimed: separate timelike/spacelike functions, G4/G5 operators, nonminimal matter, additional fields or boundary data are possible new theories needing their own source/constraint calculation.

## 6. Sources, evidence and missing implication

Primary verified copies: Bernardo arXiv:2101.00965v2 (27 Feb 2021), eqs. (2.1),(2.4),(3.28),(3.57),(3.65)–(3.71); Kobayashi–Yamaguchi–Yokoyama arXiv:1105.5723v2 (3 Jun 2011), eqs. (56)–(64). Version numbering matters. sources.json contains exact URLs and PDF/text hashes. Cached complete source files are locally ignored; source-audit reruns require restoring those exact files and verifying hashes. Search scope was these primary KGB/self-tuning and Horndeski constraint sources, existing project bridges/tangency/debraiding, not a literature-wide novelty search.

checks.py checks exact algebra, including the rolling radial current before branch substitution, the coupled mixing coefficient, vacuum map, constraints, and bounded numerical force slopes. Negative controls deliberately omit mixing, claim an unstable canonical branch is healthy, or equate Vainshtein radial scaling with MOND. Standard runner manifests authenticate all declared inputs and actual executable/software environment. These checks support the stated derivations; counts alone do not establish a full theory.

First unresolved full-theory step: obtain a covariant, stable sourced galaxy branch of the *same* action with physical g∼√(G_NM_b a0)/r and an action-derived a0/H_* (rather than prescribing it), while maintaining acceptable matter/radiation evolution and EFT control. The logarithmic map solves a formal classical vacuum-adjustment problem; its actual sourced derivative operator fails this MOND bridge. It leaves no derivation of C=32π.
