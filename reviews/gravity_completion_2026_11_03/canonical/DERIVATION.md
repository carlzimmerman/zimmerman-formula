# Canonical microscopic tree gravity and finite rigid matching

## Definitions and actual order

Write dimensionless fields in units mu=sqrt(f), p=Mp/mu, y=W0/(mu³ p), e=h=lambda=.003, g²=29e²/200, z0=7.3671437212785083116194. The retained chart is s=ln(t), x=z0 exp(s)/sqrt(31e). Put alpha=a0+u+ic, beta=x+v+id, a0²=2/(31e),

    X=x exp(i theta), A=i alpha D, B=beta exp(i theta) D,
    D=diag(2,2,2,-3,-3).

The canonical K and microscopic W on this slice are

    K=x²+30|alpha|²+30|beta|²,
    w=p y+exp(i theta)[x-15e x alpha²+15e alpha² beta].

The three covariant F coefficients are

    Dx=1-15e alpha²+x exp(-i theta) w/p²,
    Da=i alpha exp(i theta)e(x-beta)-i alpha* w/p²,
    Db=e alpha²/2+beta* exp(-i theta)w/p².

Thus Vsg=exp(K/p²)(|Dx|²+30|Da|²+30|Db|²-3|w|²/p²). All D auxiliaries vanish on this diagonal slice. This is the exact microscopic tree expression, with no constant added to the rigid potential.

The executed finite action is

    V(s,u,v)=Vsg(s,u,v)+CW(s)+ja(s)u+jb(s)v+V2_diagrams(s).

Here ja,jb are the exact rigid one-loop normal derivatives of CW, and V2_diagrams is the sum of all ten immutable TP03 graph classes BEFORE heavy relaxation. At p=infinity, Ha=120e and Hb=120e/31, so the normal solve gives u=-ja/Ha,v=-jb/Hb at first loop order. Substitution contributes -ja²/(2Ha)-jb²/(2Hb). Adding TP03 V2_reduced instead would count that contribution twice. No RG logarithm is added.

Keeping the exact tree normals in the displayed finite action resums some tree/normal terms beyond this order. It does not supply the uncomputed quadratic CW-normal term, V2 normal derivatives, full three-loop potential or gravity/current loops. The result is an explicitly specified truncated action, not an all-orders vacuum.

The fixed matching Q²=e/31+(e Xmin_one_loop)² is held fixed during field differentiation. At this critical g/e the valley supertrace M4 vanishes, so the inherited high-precision CW implementation at Q=1 gives the same valley value. The normal sources and all finite diagrams use the stated fixed Q. Coefficients are independently fitted with 21 and 29 Chebyshev nodes in s in [-.02,.3]; direct offnodes include e=.003 rather than only assuming scaling from .03.

## High precision solve and serialization

At fixed t, four equations determine u,v,mu,y: V_u=V_v=V_s=0 and mu⁴ V=rhoDE. The retained coordinate is x rather than a fictitious logarithmic field with constant metric. Using u,v relative to a0,b0(s)=x is essential: V_s is the tangent derivative and already differentiates b0.

The solver uses 100 decimal digits. The first run's short 45-digit parameter printout did not suffice to independently reconstruct a cancellation of about 69 orders. It remains an internal solver diagnostic. The preferred run_highprecision export stores 110-digit numerical parameters plus every interpolation coefficient as its actual decimal input string. A separately written potential reconstruction at 120 digits, using only that serialized payload, reproduces rhoDE=2.52e-47GeV4 to relative error 6.53e-34 and all three stationarity equations to 1.66e-101 dimensionless. No low-precision subtraction is presented as a DE determination. W0 is tuned, and omitted terms require retuning it.

At the candidate, |delta W0/W0| for a rhoDE change is 4.43914784e-69. The raw energy scale and this tuned residual are different physical claims. Neither rhoDE nor kappa has been derived.

## Light Hessian, metrics and cubic

Let n=(u,v). For the aligned phase, use the heavy-normal Schur complement

    Vred_ss=V_ss-V_sn Hnn^-1 V_ns,
    n_s=-Hnn^-1 V_ns.

The exact canonical pullback on the reduced tree graph is

    A_tree=x²+30(a_s)²+30(b_s)²,
    b_s=x+v_s, a_s=u_s.

Add the actual immutable TP04 radial graph, not the angular graph. At first loop order its geometric term is60x v_s; the angular counterpart is60x v. The code retains the exact tree pullback and adds each one-loop graph once.

For the phase, the CP-odd normal variables (c,d) have source C=V_(c,d),theta and Hessian Hodd. Their response is (c_theta,d_theta)=-Hodd^-1 C. Set

    B=V_theta,theta-C^T Hodd^-1 C,
    F_tree=x²+30 c_theta²+30(b+d_theta)².

Then add the actual TP03 angular graph. The normal phase response at the candidate is below 5e-33 in these coordinates, as expected from the absence of a linear-W0 heavy source. The normalized light masses are m_sigma²=mu² Vred_ss/(2A), m_a²=mu² B/(2F). Analytic Schur derivatives agree with the frozen .005/.0025 field stencils and were independently reconstructed by the coordinator.

For the general two-derivative L=A(s)(partial s)²+F(s)(partial theta)²-V(s,theta), the on-shell sigma-aa amplitude at an aligned stationary point is

    g_sigma_aa=[(Fs/(2F))(m_sigma²-2m_a²)+mu² Bs/(2F)]/(mu sqrt(2A)).

Both the polar kinetic and potential vertices are included. At the canonical leading-tilt limit this gives (m_sigma²-m_a²)/(sqrt2 R), agreeing with TP05. The width is g² sqrt(1-4m_a²/m_sigma²)/(32pi m_sigma) when open. It is exactly zero for every displayed phase-closed candidate.

## Small-field gravitational orders

For the full all-field superpotential W=fX+W3, Euler homogeneity gives sum zi Wi=fX+3W3. The term linear in W0 in the canonical scalar potential is consequently

    delta V=2 Re[W0* (sum zi Wi-3W)]/Mp²
           =-4 Re(f W0* X)/Mp².

This is independent of every heavy field, not only true after their elimination. It gives neither a heavy tadpole nor a scalar Hessian insertion at this order. It cannot be used to ignore the light tilt: that tilt is the leading CW competitor.

The pre-unitary canonical chiral fermion matrix is

    exp(K/(2p²))[Wij+(zi* Wj+zj* Wi)/p²+zi* zj* W/p⁴].

It has no direct O(1/p) insertion in a massive matter block. Gauge/gaugino-Higgsino mixing is unchanged at this order, and vector masses depend only on the field background. The leading super-Higgs rank-one term is proportional to DiW DjW/W. On the rigid stationary valley the rigid Goldstino is annihilated by the tree fermion matrix; the rank-one term lies in that neutral direction and does not shift the massive eigenvalues to first order. Thus the direct heavy-mass contribution to the one-loop CW potential has no O(1/p) term on this valley. This tree-valley mass argument is conditional on correct quantum/current matching when promoted to a full off-shell 1PI statement.

run_order checks all 84 heavy scalar and 60 heavy fermion directions with formal q=1/p of 2e-4,1e-4,5e-5. Their odd derivative norms scale as q² (halving ratios 4.00297,4.00074 and4.00150,4.00038), while gauge mixing's odd derivative is identically zero. The artificial q values are controls, not physical parameter points.

At the actual candidate R/Mp=3.49e-11. The exact-tree/normal solve differs from the consistently vacuum-tuned finite leading-tilt action in mu by 4.38e-10 at t=1.16004 and 5.83e-10 near the fold. This comparison also includes the different normal resummations, so it is a measured truncation comparison, not a bound on every omitted gravitational operator.

## Transverse and super-Higgs scope

The full98-real canonical tree-SUGRA Hessian is constructed by differentiating DiW and exp(K/p²). It includes the D-term Hessian. Its restriction orthogonal to the14 rigid light/gauge directions has 84 positive eigenvalues at the finite candidate; the least heavy scalar is 1308.851046GeV. Removing the tree Goldstino constraint leaves 60 heavy fermions (minimum 1651.929813GeV) and 12 unbroken gauginos. The latter receive the already computed complete leading rigid one-loop masses. Two microscopic normal Hessian entries independently agree with the full tensor Hessian below 8.7e-19 dimensionless.

The tree Hessian is being evaluated at a loop-stationary point. Its raw gauge/light eigenvalues are not physical pole masses. Likewise the tree Goldstino mass residual is 2.93e-8 dimensionless; multiplying by mu gives about 16 MeV, but this is NOT a physical extra 16 MeV particle or an instability. A consistent loop effective action must include the fermion self-energy/current terms that implement the quantum Ward identity. Tree projection alone cannot supply those terms. The tree Ward algebra, with its nonzero tree gradient retained, agrees to 9.3e-22. Canonical-K curvature, weak couplings and the large heavy gaps support the expansion, but no rigorous norm bound on all transverse quantum self-energies was computed. Full transverse quantum/Goldstone resummation and loop super-Higgs certification remain open. Photino/matter mixing is additionally constrained by the residual charge-conjugation symmetry; no extra neutral chiral particle is inferred from a projected matrix zero.

## Gravitino and photino order

The reported gravitino parameter is the exact microscopic tree value mu exp(K/(2p²))|w|/p² with the tuned W0. F_tree_SUGRA is mu² exp(K/(2p²))sqrt(sum|DiW|²), clearly labelled tree normalization. The photino table is the complete leading rigid one-loop pole mass at the actual retained X, with finite F/M² splittings and actual dlnm/ds. CW normal shifts in that threshold start at the next loop order and are not silently included as a complete two-loop result.

Constant gauge kinetic function gives no tree unbroken gaugino mass. In the full SU5 UV theory TG=5,TR=10, so the explicitly evaluated UV anomaly counterterm from the stated primary-source convention is

    delta m_UV=-g²/(16pi²)[5m32-5 KiFi/Mp²]
              =-5.21959e-16GeV,

relative to the candidate photino, -2.02e-11. The KiFi term is smaller still. This is a UV counterterm, not by itself a complete matched IR pole correction. An IR beta coefficient of zero does not alone settle a nonsupersymmetric dynamical threshold; regulator/contact/current and threshold contributions must be combined. A coefficient100 sensitivity scale is 1.044e-14GeV, or4.04e-10 of the photino mass. It is explicitly not a proved bound. The residual finite gravitational threshold coefficient remains conditional; it is far below the uncomputed ordinary relative two-loop photino matching scale by power counting, but no coefficient-free all-orders claim follows.

The finite near-threshold radial positions are tunable. At epsilon=m_sigma/(2m_chi)-1 as small as1e-8, leading pole masses and interpolation-location convergence do not certify a fixed-t physical beta. Production may instead parameterize the actual physical threshold as a free tuned input and must state that distinction.

## Primary sources inspected

[Cheung, D'Eramo and Thaler, arXiv1104.2598v2](https://arxiv.org/pdf/1104.2598),12May2011, Eq36--37/AppF supplies the tree Goldstino and pre-unitary fermion matrix convention. Its tree scope does not prove a loop identity at our displaced stationary point. A rank-one Goldstino correction vanishes between vectors obeying the same Goldstino constraint, which explains the projected-matrix equivalence used here.

[D'Eramo, Thaler and Thomas, arXiv1202.1280v3](https://arxiv.org/pdf/1202.1280),12June2012, Eq3.11--3.15 separates the one-loop anomaly gaugino mass from the associated Goldstino coupling. This is the convention for the quoted UV counterterm and the reason a mass shift alone cannot certify the decay current. [Dine and Draper, arXiv1310.2196v3](https://arxiv.org/pdf/1310.2196),21February2014, sections1--3 discusses local contact terms, Higgs thresholds and decoupling. It does not perform this broken-SUSY SU5 finite threshold calculation for us.

## Fixed-vacuum outer barrier and primordial radial energy

The near-fold branch has an outer unstable stationary point at fixed mu,W0. Changing mu along the family when searching for that point would compute a different potential. run_barrier instead holds each solved p,y fixed, solves the heavy normals at each s, and finds the second root of the reduced tangent derivative. Both roots remain inside the original interpolation domain; no fit extrapolation is used.

For m_sigma/m_chi=2.01, the stable and outer unstable roots are t=1.266721741421881 and1.2667404330462477. Their potential difference is .00210341686684315GeV4. Define the energy diagnostic Sigma_bar=sqrt(2 DeltaV_bar/m_sigma²); it equals 1233.82636684GeV, or1.20479824e-5 R. For mass ratios 2.1,3,4,10 the corresponding Sigma_bar/R values are 1.31510e-5,2.68383e-5,4.77110e-5,2.98080e-4. These are limits for a sub-barrier trapped harmonic energy description. They are not a proof about arbitrary initial velocity, cosmological damping, capture from another basin or a specified large-amplitude trajectory.
