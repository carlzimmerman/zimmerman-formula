# Exceptional single-scalar selector: a scoped obstruction, not 32π

Requiring complete exceptionality for generic planar simple waves excludes exact deep MOND in a regular, directly sourced single P(X) branch. It does not determine a vacuum-to-acceleration coefficient. Canonical/DBI classification is known; the result here is its explicit static source and weak-source discrimination.

## Raw principal derivation

Take signature −+++, fixed Minkowski, X=(τ²−χ²)/2, τ=φ_t, χ=φ_x, and f=P_X>0. Require P at least C³ on an open interval, f(f+2Xf′)>0, and a finite noncharacteristic time chart A=f+τ²f′≠0. This excludes degenerate cuscuton endpoints and does not assert full gravitational health. Equations are Aτ_t+2Bτ_x+Cχ_x=0, χ_t−τ_x=0, B=−τχf′, C=−f+χ²f′. Eigenvectors rλ=(−λ,1) correspond to roots

F(λ)=Aλ²−2Bλ+C=f(λ²−1)+f′(τλ+χ)²=0.

Differentiating with rλ while holding λ fixed first yields

rλ·∇F=−(τλ+χ)[f″(τλ+χ)²+3f′(λ²−1)].

Implicit differentiation on F=0 therefore gives

rλ·∇λ=(τλ+χ)³[ff″−3(f′)²]/[2f(Aλ−B)].

Strict hyperbolicity makes Aλ−B nonzero. Vanishing for both families throughout an open state domain forces ff″−3(f′)²=0: isolated τλ+χ=0 rays cannot cover that domain. In particular τ=0, χ=u>0 already gives necessity throughout a spacelike interval. Sufficiency follows from the displayed identity. Equivalent ODE (f^−2)″=0 implies f=(a+bX)^−1/2 on each positive branch; the b=0 case is constant. Integrating gives P=2√(a+bX)/b+P0 for b≠0, or P=f0X+P0. Hyperbolicity requires a>0 since f+2Xf′=a/(a+bX)^(3/2). Overall normalization is included in a,b. Thus a zero endpoint at X=0 (a=0) is not a strictly hyperbolic exception: it has f+2Xf′=0.

## Matter and acceleration dictionary

This is an additional explicit premise: weak conformal matter coupling gtilde_μν=e^(2γφ)g_μν, expanded nonrelativistically as Lmatter=−γρφ, with fixed finite γ>0 and Einstein metric nearly flat in the near zone. The vacuum scalar has shift symmetry; the stipulated direct matter coupling breaks that symmetry and is used only to define the source/force dictionary. The source equation is ∇·(f∇φ)=γρ. Matter measures scalar potential γφ and extra acceleration magnitude gs=γu, u=φ_r>0. Minimal Newtonian gravity may be added to the physical acceleration; for a scalar-dominated deep-MOND regime its contribution is subleading. We do not replace this dictionary by a clock acceleration or infer it from KGB.

Outside a spherical source mass M, r² f(−u²/2)u=γM/(4π), so j=γM/(4πr²). A regular exceptional branch reaching u=0 can be written

f(−u²/2)=f0/√(1+βu²),
u=j/√(f0²−βj²),   d(fu)/du=f0/(1+βu²)^(3/2)>0.

Admissibility includes both radicands positive. β>0 has bounded flux j<f0/√β; β<0 has a finite maximum u but unbounded flux. Both have u=j/f0+O(j³), hence gs∝M/r² as M→0 at fixed r, or r→∞ at fixed M. They cannot give the normalized √M/r weak-source law. Exact local mass slope is dlnu/dlnM=f0²/(f0²−βj²)=1+βu², and radial slope is −2 times this. β<0 permits mass slope 1/2 at one field u²=−1/(2β), not on an open interval. This rules out mistaking a crossover point for a MOND asymptotic regime.

Exact deep MOND requires f(−u²/2)=ku, so P_X=k√(−2X) and P=−k(−2X)^(3/2)/3+P0. Its static Hessian is positive for u>0, but ff″−3f′²=2k²/X<0. Matching gs²=GMa0/r² additionally requires k=γ³/(4πGa0); this is a supplied scale, not a consequence of exceptionality. If only asymptotic f/u→k is assumed, regular exceptional classification still forbids it at the u=0 endpoint. A rolling ansatz φ=qt+ϕ instead samples X=q²/2−u²/2: any regular exceptional branch there again has finite f and linear small-u response; a square-root pole gives f∼1/u and constant flux/rank failure rather than MOND. No timelike cosmological solution is inferred.

## Selector conclusion and scope

P0 leaves every source equation and CE condition unchanged; with dynamical Einstein gravity it changes vacuum stress P0g_μν. The DBI scale and direct coupling remain free. There is no action-derived Λ–a0 relation or response-integral C dictionary here, so neither C=32π nor any other C follows. The strong requirement makes this single-P(X) MOND premise incompatible, rather than selecting one interpolating kernel. The unresolved next arrow is a different covariant action with its actual constrained characteristics, source law and vacuum equation jointly derived. Fixed-Minkowski simple-wave results are not transplanted to our logKGB, clock-acceleration response, all Horndeski backgrounds, global shocks, or a UV-completed theory.

SOURCE_REVIEW.md authenticates the exact primary source and translation. checks.py verifies symbolic identities, exceptional/singular branches, static source inversion, calibration and three deliberately false controls. These finite algebra checks corroborate the derivation; the open-interval proof above supplies the uniform conclusion. All executed inputs are pinned by bounded standard-runner manifests under runs/. No astrophysical dataset or target fit is used.
