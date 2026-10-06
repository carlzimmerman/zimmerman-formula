# Planar evolution and lapse preservation: no new local algebraic veto

The finite-acceleration planar jets survive the first time-consistency test. The two spatial metric equations have invertible velocity rank, generate the necessary anisotropic evolution, and preserve momentum once the initial Hamiltonian constraint holds. Preserving the Hamiltonian determines the lapse time derivative by a regular local spatial second-order ODE whenever Qaa≠0. It does not force Qaa positive or eliminate the previously found negative-kinetic sector.

This supplies a first-time-consistent field-equation jet and a formal all-orders continuation argument. It does **not** establish convergence of that formal time series, a full local on-shell spacetime, a global elliptic boundary solution, or hyperbolic/Hadamard well-posedness. Those are distinct remaining implications. No peer scientific inputs were edited.

## 1. General planar action before imposing isotropy

Use M=K_E>0, b=2c/(3H*), P(N)=2c lnN−Veff, and the same fixed-A even response Q. In unitary time,

 ds²=−N²dt²+e^(2α)(dx+vdt)²+e^(2β)(dy²+dz²).

The extrinsic-curvature eigenvalues are
 hx=(αdot−vα′−v′)/N, hy=(βdot−vβ′)/N, hy,
 θ=hx+2hy, a=e^(−α)N′/N.

A local time-dependent spatial threading can set v=0, but the momentum equation must be varied before imposing this gauge. After the spatial curvature boundary term, the zero-shift Lagrangian per transverse coordinate area is

 L=M e^(−α+2β)[2N′β′+N(β′)²]
 −M e^(α+2β)(2αdot βdot+βdot²)/N
 −b e^(α+2β)(αdot+2βdot)lnN
 +N e^(α+2β)P(N)+M N e^(α+2β)Q(a).

The velocity Hessian in (αdot,βdot) has determinant −4M²e^(2α+4β)/N². Thus both spatial evolution equations solve for their accelerations once Ndot and spatial jets are supplied. The indefinite uneliminated metric Hessian is not itself a physical ghost criterion; the prior constrained reduction fixes that question. The lapse has no independent time derivative in the raw action.

The exact zero-shift momentum constraint, written as a coordinate scalar, is
 C=2M[hy′−β′(hx−hy)]+b(lnN)′=0.

The lapse equation divided by e^(α+2β) is
 H=M(2hxhy+hy²)+P+2c−b(hx+2hy)
 +M e^(−2α)[−2β″−3(β′)²+2α′β′]
 +M[Q−aQa−e^(−α)(Qaa a′+2β′Qa)]=0.

In particular the spatial divergence of the acceleration response is retained. Neither its finite-gradient derivatives nor the required h′ can be discarded.

## 2. Exact spatial evolution on the initial flat/isotropic slice

At t=0 take α=β=0 as spatial functions, hx=hy=h(x), v=0, N=N0(x)>0. Put a=N′/N, λ=Ndot/N, D=h−b/(2M), and
 Aα=3Mh²+P+M(Q−aQa).

The actual spatial Euler equations reduce to

 2M dot hy+bλ+N Aα=0,
 M(dot hx+dot hy)+bλ+N[3Mh²+P+MQ]−MN″=0.

Here dot hx,dot hy are coordinate time derivatives of the physical K eigenvalues; αddot=N(dot hx+hλ), βddot=N(dot hy+hλ). Direct raw-action variation verifies both equations. Their difference gives

 dot hx−dot hy=N″−NaQa=N[a′+a²−aQa].

A finite-acceleration lapse generally generates anisotropy immediately. Requiring isotropic accelerations would add an artificial condition absent from the action. Isotropy is a legitimate initial slice, not an evolution ansatz.

On this slice the two initial constraints are
 2Mh′+ba=0,
 H=3Mh²+P+2c−3bh+M(Q−aQa−Qaa a′)=0.

Taking the time derivative of momentum and inserting the spatial evolution gives
 dot C=−(N Aα)′=−Na H.

The equality uses precisely h′=−ba/(2M). Thus both initial constraints imply dot C=0, with no new algebraic condition on λ or a. More generally the time-dependent spatial-diffeomorphism identity at v=0, once the spatial Euler equations hold, gives
 dot C+(αdot+2βdot)C=−N′H.
This propagates the momentum residual if the Hamiltonian is enforced. It does not supply a separate clock equation: the latter is the covariant diffeomorphism consequence for a timelike clock.

## 3. Hamiltonian preservation determines a local lapse-time ODE

At the initial slice,
 adot=λ′−Nh a,
 (adot)′=λ″−(Nh a)′,
 dot R3/2=−2(Nh)″.

After substituting the two spatial evolution equations, dot H=0 becomes

 Lλ+F=0,
 Lλ=−M Qaa λ″−M(aQaa+Qaaa a′)λ′+(2c−3bD)λ.

The full forcing, with all background derivatives displayed, is

 F=−3DN Aα+2MD(N″−NaQa)−2M(Nh)″
 +M[(aQaa+Qaaa a′)Nh a+Qaa(Nh a)′+Nh Qaa a′−2(Nh)′Qa].

Using h′=−ba/(2M), h″=−ba′/(2M), it equivalently is

 F=N[−3D Aα+b a²−4MD aQa
 +(2Mh−b/2)a²Qaa+2Mh a′Qaa+Mh a a′Qaaa].

The highest spatial coefficient is −M Qaa. At Qaa≠0 this is a regular second-order **local spatial ODE** for λ. Either sign admits a local solution with two specified point values λ(x0),λ′(x0). This fact does not establish an elliptic boundary-value problem over a galaxy or a complete Cauchy evolution; on a one-dimensional slice the local ODE is the appropriate limited conclusion. At Qaa=0 a separate compatibility/rank analysis is required. D≠0 remains necessary for the prior physical-symbol reduction, but is not needed to invert this lapse-preservation ODE's leading coefficient.

The Qaaa and lapse-gradient terms matter. Omitting λ″ would turn a legitimate spatial lapse solve into a spurious algebraic restriction. Constraint preservation therefore removes the specific worry that the negative-Qaa planar initial jets are immediately forbidden by an additional pointwise lapse condition.

## 4. Formal recursion and its precise limit

In an analytic acceleration interval away from a=0, Qaa=0 and inverse-source singularities, the cutoff response and the local constraint background are analytic. The velocity Hessian above solves the spatial equations for the next metric time derivatives, linearly in the highest lapse time derivative. The full zero-shift spatial equations are linear in Ndot and the metric accelerations. After their inversion, the full Hamiltonian time derivative is linear in λ and its spatial derivatives, with leading coefficient −M e^(−2α)Qaa on λ″; all other terms depend on the instantaneous spatial/velocity jets. Differentiating this general Hamiltonian-preservation equation further in time gives, at t=0, the same linear spatial operator L acting on each new highest λ time derivative; derivatives of coefficients multiply previously fixed lower time jets and move into the forcing. This is the usual highest-derivative chain-rule structure of a quasilinear equation, not a new PDE-existence theorem. All spatial derivatives of the lower jets are known at that recursive stage.

For each finite order, solve that inhomogeneous analytic spatial ODE locally with two chosen point values. Then use the invertible metric velocity equations to determine the next metric time derivatives. The spatial-diffeomorphism identity propagates momentum order by order when H and the spatial equations are enforced. Induction therefore constructs a formal field-equation Taylor jet of arbitrary finite time order. The two point-value sequences amount to formal spatial-boundary data; they have not been promoted to a physically acceptable global boundary condition.

No convergence estimate in time, common spatial radius for all orders, or theorem that this formal series represents a solution was proved. Cauchy–Kowalevski cannot be invoked merely because the background constraint ODE is analytic: the system contains a spatial lapse solve and its actual PDE normal form and hypotheses require a separate proof. Hyperbolic well-posedness is also not implied by a formal analytic jet. The calculation below explicitly verifies the first nontrivial preservation order; the all-order conclusion rests on the stated formal recursion argument, not a numerical assertion count.

A first-time-consistent jet fixes the background coefficients used by the previous constrained kinetic symbol and removes an immediate off-shell inconsistency. To claim a realized physical ghost, rather than a formal-jet negative kinetic sector, an actual convergent on-shell background or an appropriate local existence theorem is still needed.

## 5. Bounded constructive example and controls

Use the inherited cutoff T=128.9153707043 without a target fit; M=H*=A=1,c=1.5,b=1,Veff=3. At x0=0 choose N=1,h=1 and source-kernel y=100, so a=100.31138892715221, D=.5 and Qaa=−.004674614489946037. The initial momentum/Hamiltonian equations determine h′,a′. Choose λ=λ′=0 at x0, then the lapse-preservation equation determines λ″=−2110750.960304905. The spatial metric equations give dot hx−dot hy=5430.288956603162, finite and nonzero. These large gradients require a correspondingly short WKB wavelength and are not a slowly evolving astrophysical solution.

checks.py reconstructs the Euler equations directly from the general planar action, checks the momentum/Hamiltonian preservation identities, verifies the full forcing and velocity rank, and integrates the initial constraints plus λ ODE over x=±1e−7. It keeps the actual cutoff inverse and Q derivatives. Sampled Hamiltonian and its first time derivative, momentum first time derivative, negative response and nonzero D all pass. The background is initially flat/isotropic but its actual spatial accelerations are anisotropic.

Controls incorrectly impose preserved isotropy, remove λ″ from lapse preservation, or reverse the background momentum sign; each is expected to fail. The tested interval is tiny and supplies local time-consistent jets. No source, galaxy matching, force calibration, UV completion or32π selection is claimed. A finite EFT cutoff and possible higher operators remain separate from this action's formal high-frequency sign.
