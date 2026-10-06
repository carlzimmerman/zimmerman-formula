# A self-accelerating negative-K branch must lose a homogeneous scalar cone somewhere

Base `81af81ba8a7207bca2bc4f13375c757feee7afcd`. This is a conditional theorem for the generalized-aether class being tested in the sibling report, not all vector theories. Conventions are deliberately fixed: hypersurface-orthogonal unit aether, Einstein coefficient K_E>0, n≥2 spatial dimensions, c₁<0, c₁+c₃=0, c₂<0, no c₄ term, F(0)=0, no ordinary matter vacuum source for the self-accelerating root, and M>0. The function is C² on the negative-K interval, with F′>0 there and at its zero endpoint. General vector scalar perturbations share this hypersurface-orthogonal scalar sector; transverse health requires separate tests.

## Same action and root equation

The gravitational action is K_E/2 times ∫sqrt(−g)[R+M²F(K)], plus the unit constraint. For the declared hypersurface-orthogonal flow,

    K=[c₂θ²−c₁a_i a^i]/M²,
    α=n c₂,
    K_FRW=nαH²/M²<0.

The flat-FRW lapse equation in vacuum gives (the common factor −2K/α is specific to n=3)

    1−[2α/(n−1)]F′+[α/(n−1)]F/K=0,
    F−2KF′=−(n−1)K/α.

Write z=−K>0, h(z)=F′(−z)>0 and I(z)=∫₀ᶻh(s)ds. With F(0)=0, F(−z)=−I(z), so a positive self-accelerating root obeys

    I(z)−2zh(z)=−(n−1)z/α>0.                         (1)

Let Q=1+2zh′/h=(F′+2KF″)/F′. If Q>0 throughout (0,z], sqrt(z)h(z) is strictly increasing. For 0<s<z, h(s)<sqrt(z)h(z)/sqrt(s), whence I(z)<2zh(z), contradicting (1). Even nonnegative Q everywhere is incompatible with the strictly positive right side. Therefore Q must be negative somewhere on any such interval. Q→1 at zero for the C², finite-positive-h endpoint.

## Coupled high-frequency scalar reduction on a geodesic isotropic state

Take the scalar ADM metric h_ij=e^(2ζ)δ_ij, N=1+ν, N_i=∂_iB. At a locally homogeneous geodesic FRW point with a_i=0, keep the high-frequency principal terms with k/a much larger than H and background coefficient-variation rates. Background H is retained inside F′,F″. Expand the same action, including its metric constraints. Its extrinsic and lapse-gradient coefficients are

    λ_eff=1−c₂[F′+2KF″]=1−c₂hQ,
    η_eff=−c₁F′=−c₁h>0.

This follows because the second variation of M²F(c₂θ²/M²) adds c₂(F′+2KF″)(δθ)², whereas the a_i² term adds −c₁F′(∂ν)². The ordinary Einstein extrinsic term is δK_ij²−(δθ)². Terms proportional to Hν or lower derivatives do not change the nondegenerate high-frequency principal symbol; the limiting degenerate points need separate treatment.

Before eliminating the shift, the time-derivative part, up to K_E/2, is

    n(1−nλ)ζdot²+2(nλ−1)ζdot ΔB+(1−λ)(ΔB)².

For λ≠1 its shift equation gives ΔB=(nλ−1)ζdot/(λ−1). Substitution gives

    A_ζ=(n−1)(nλ−1)/(λ−1).

The spatial/lapse part is

    (n−1)(n−2)|∇ζ|²+2(n−1)∇ν·∇ζ+η|∇ν|².

For η>0, lapse elimination gives ν=−(n−1)ζ/η on nonzero Fourier modes and the spatial action becomes −B_ζ|∇ζ|², with

    B_ζ=(n−1)[(n−1)/η−(n−2)],
    c_s²=(λ−1)/(nλ−1)[(n−1)/η−(n−2)].

These are derived constrained scalar coefficients, not a frozen-aether Poisson guess. For n=3, positive ordinary spatial coefficient requires 0<η<2. Regardless of that spatial test, 1/n<λ<1 gives A_ζ<0, an ordinary negative kinetic scalar mode in this nondegenerate high-frequency limit.

## Precise no-go and its limits

Since c₂<0, λ=1−c₂hQ is greater than one near K=0 and less than one wherever Q is negative. Along a continuous path between these states it crosses one and necessarily visits 1/n<λ<1. Thus the action cannot have a positive reduced homogeneous scalar kinetic coefficient at **every geodesic isotropic state across the entire interval from K=0 to its nonzero negative-K self-accelerating root**, under these assumptions. At λ=1 shift elimination itself degenerates; the open negative-kinetic interval on its far side supplies the exclusion without assigning a regular formula at the singular point.

This is stronger than imposing Q>0 as a guessed health condition: it derives the actual coupled high-frequency scalar sign for this declared homogeneous sector. It does **not** imply that every cosmological history passes through that interval. A universe always on the negative-K linear endpoint can avoid it; the constructive family being tested does just that on its expanding vacuum branch. Nor is the same λ formula automatically valid in an accelerated, anisotropic galaxy transition: F″θa δθδa terms and lapse mixing must then be retained. A spatial matching route could potentially evade this homogeneous test, but needs an actual solution and its full constrained symbol.

An additive F(0), extra vacuum matter, c₁+c₃≠0, c₄, modified curvature couplings, sign-changing F′, additional fields or a nonsmooth branch changes the proof obligations. The theorem derives no preferred coefficient and rules out no such broader theory. It tells the 32π investigation exactly why endpoint cone checks cannot certify a global same-function bridge.

`aether_cone_checks.py` checks the general-n shift/lapse elimination and explicit nondegenerate signs. The integral argument and continuity proof are uniform mathematics, not conclusions from sampled dimensions.
