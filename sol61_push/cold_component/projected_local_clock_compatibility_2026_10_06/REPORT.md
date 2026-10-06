# Local clock compatibility of the projected integration mode

The real finite-k decaying integration mode has no regular second-order continuation about coincident de Sitter in the **unchanged projected action**. Its linear metric equations are satisfied, but the actual local clock Euler equation has a nonzero second-order source. The clock's entire linearized Euler operator is zero, so second-order metric/clock corrections cannot cancel it. The spatially integrated clock equation is nevertheless zero, explaining why the previous homogeneous mean response did not detect this obstruction.

A uniform version excludes any nonzero real decaying superposition on one Laplace-eigenvalue shell of a connected flat torus. This is not an all-mode/theory no-go: mixtures of distinct eigenvalues, changed backgrounds/operators, nonperturbative or singular-amplitude continuations are not classified here. It does not retract the exact linear source dictionary or the formal necessary homogeneous rows; it closes their previously explicit missing **local** arrow negatively for this seed class.

## Actual normalized clock variation

Use signature −+++, n=3, K>0, coincident empty de Sitter a=exp(Ht), H>0, and the inherited covariant action

S_int=2K a0²∫v M_eff(I),
I=(P_g^{μν}+P_hat^{μν})A_μ A_ν/(2a0²),
A_μ=a_gμ−a_hatμ, M_eff,I(0)=1/2.

The shared clock defines u_μ=−N_θ∂_μθ, N_θ=(−g^{μν}θ_μθ_ν)^(−1/2), P_μ^ν=δ_μ^ν+u_μu^ν and a_μ=P_μ^ν∂_νln N_θ. The last identity follows from differentiating a unit, hypersurface-orthogonal normal; it includes temporal acceleration and metric connections.

At θ=t in an arbitrary ADM metric with lapse N and contravariant shift S^i, vary θ by π at fixed metric. Direct normalization gives

δln N_θ=−πdot+S^jπ_j,
δu^0=0, δu^i=−Nγ^{ij}π_j,
δP_i^0=−π_i, δP_i^j=S^jπ_i.

Thus the **exact** spatial acceleration variation at that unitary chart is

δa_i=−π_it+∂i(S^jπ_j)−[(∂t−S^j∂j)ln N]π_i.

Dropping the shift or reversing the time term changes the answer. No H-dependent term is silently discarded: the normalized mixed-projector identity contains all the metric dependence required here.

## Relative amplitude expansion and temporal/projector terms

Take pure-relative first-order metric perturbations with lnN_g=εν/2, lnN_hat=−εν/2, S_g^j=εΔS^j/2, S_hat^j=−εΔS^j/2, and opposite first-order spatial perturbations. The common −π_it cancels, while the advective S·∂lnN products agree between the two metrics. Hence to order ε,

δA_i=ε[∂i(ΔS^jπ_j)−νdotπ_i].

The actual A_i=ε∂iν+O(ε²). In unitary ADM, P^{00}=P^{0i}=0 exactly. The actual A_0=S_g·∇lnN_g−S_hat·∇lnN_hat has no first-order term (the two pure-relative products even agree at order two). Although δA_0 can be nonzero at order ε, it cannot enter the contraction with the background spatial projector. The background spatial δP^{ij} is zero when S=0. Therefore δP A A has no order-two contribution; the temporal/projector pieces have been checked rather than treating A_i as an arbitrary Euclidean vector.

Using v=a³ at leading order and m(0)=1/2, the actual second-order clock variation is

δS_θ,2=2Ka∫∂iν[∂i(ΔS^jπ_j)−νdotπ_i]dtd³x.

Periodic spatial integration by parts, with arbitrary compactly supported time variation, gives the clock Euler density

E_θ,2=2Ka∂j[(Δν)ΔS^j+νdot∂jν].

Δ here is the coordinate flat spatial Laplacian; the factor a rather than a³ is essential. The norm-cubic correction to m is O(ε), whereas the displayed clock variation is O(ε²), so that correction first enters the clock Euler equation at order three. Minimal matter has no direct clock variation. No bare quantum, fluid, or dust assumption enters this result.

## Plane mode and regular continuation obstruction

For ν(t,x)=ν_amp(t)cos(kx) and ΔS^x=−kβ(t)sin(kx)/a²,

E_θ,2=2Ka k²ν_amp(Pβ−ν_amp_dot)cos(2kx), P=k²/a².

The actual linear constraints/evolution for the pure decay mode are ν_amp=−B/a, β=2Hν_amp/P, ν_amp_dot=−Hν_amp. They yield

E_θ,2=6KaHk²ν_amp²cos(2kx)
       =6KHk²B²a^(−1)cos(2kx).

For any B≠0 this is nonzero locally. Its torus integral vanishes; an integrated-clock check is therefore insufficient.

The parent raw quadratic action has no common clock perturbation and hence E_θ^(1) is identically zero for arbitrary first-order metric/clock fields. In a regular perturbative solution q=q_background+εq_1+ε²q_2+o(ε²), the clock equation at order two is E_θ^(1)[q_2]+E_θ^(2)[q_1,q_1]=0. Its first term is zero; the calculated second term is not. No choice of ordinary second-order corrections, including their mean Bianchi-I components, can extend this specified linear seed to a solution. By diagonal covariance the same obstruction must appear as compatibility of the second-order metric equations; it is not an extra independent propagating equation added by hand.

Adding an arbitrary common first-order perturbation cannot change this leading quadratic clock coefficient. The clock functional is invariant under metric exchange, so it is even in relative perturbations; it vanishes identically for exactly equal metrics, with any common metric/clock. Its lowest nonzero term is therefore quadratic in relative data, evaluated at the common background. Common first-order data enter that coefficient only at higher order. This is distinct from modifying the admitted background or adding a new clock operator.

For a single mode with also a constant Z0, the residual contains ν_amp[3Hν_amp−PZ0/H]. With ν_amp=−B/a these are different powers of a; for B≠0 no constant Z0 cancels the equation on an open time interval. Frozen B=0 data have no obstruction from this particular order-two clock term, but their nonlinear admission/physical source is not proved here.

## Compact real eigenshell theorem

Let ν=a^(−1)f(x), with real smooth f on a connected flat three-torus and Δf=−k²f, k>0. The same linear constraints give ΔS=2H∇ν/k² and νdot=−Hν. Consequently

E_θ,2=−3KaH Δ(ν²).

If the local clock condition holds, Δ(f²)=0. Multiply by f² and integrate over the torus: periodic integration by parts gives ∫|∇(f²)|²=0. Thus f² is constant. A nonzero constant square would force real continuous f to have constant sign on the connected torus, incompatible with the zero mean of a k>0 Laplace eigenfunction (or with its eigenvalue equation). Hence f=0. Superposing different directions on the **same** eigenvalue shell does not cure the obstruction. Reality and compactness are used explicitly; complex formal Fourier amplitudes must represent a real physical field before this theorem is applied.

This proof makes no claim about general superpositions with distinct eigenvalues, noncompact boundary flux, other backgrounds, finite nonlinear branches without a regular tangent expansion, or a changed projected operator.

## Relation to the prior mean calculation and cold arrow

The previous projected_mode_mean_geometry calculation solved formal homogeneous lapse/shear/trace rows and obtained cancellation in preferred-normal mean expansion. Its stated local clock compatibility obligation was not tested there. The nonzero cos(2kx) result here explains how all its zero-mode rows could agree while the full local seed is not extendible. The geometric cancellation remains a necessary-row identity, not an admitted nonlinear family from which to infer cold abundance.

The exact linear signed pressureless stress remains an algebraic fact, but it cannot by itself supply cold matter or an actual cosmological growth history if its perturbative seed fails this local equation. Closing the cold arrow now requires a different admitted mode/background or a changed clock/operator with a derived constraint structure. No particle identity, positive abundance, primordial spectrum, likelihood or 32π selection is supplied.

## Bounded evidence

checks.py reconstructs N_θ,u,P from an actual inverse ADM metric and differentiates them before amplitude expansion. It verifies temporal/projector cancellations, the raw clock Euler density, plane and two-direction eigenshell witnesses, the zero integral and the distinct-time-power mixture. Controls omit the shift term, reverse the time term, or retain only the spatially averaged clock row. Thirty-five exact checks corroborate the raw derivation; the compact eigenshell proof above carries its uniform scope. Current standard records and hash validation are in RUNS.md. No full nonlinear numerical evolution or author/Claude script execution is performed.
