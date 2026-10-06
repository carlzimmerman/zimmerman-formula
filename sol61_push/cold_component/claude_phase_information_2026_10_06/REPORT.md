# Equal cold moments do not identify phase equilibrium

**Verdict: refuted for the declared instantaneous observable set.** A reader of local density, Newtonian tidal tensor, mean velocity and the full second central velocity moment cannot universally distinguish a collisionless stationary host from nonstationary crossing cold streams. The explicit counterexample below matches these inputs everywhere, not just at one point. This is a continuation of Claude CFG345/354/355, not a replacement switch or a particle-identity claim.

## Actual Claude inputs and first lost information

CFG345 leaves the cold component's microphysics unspecified; its wave/condensate small-scale results are conditional on independent mass or pressure parameters. CFG354 removes potential zero-point dependence by using a Hessian reader. Its T1 middle eigenvalue cannot discriminate the declared dense filament and host geometries; its gradient-dependent T3 is contaminated by a uniform external field. CFG355 adds the actual stream covariance veto `f=H_eps(lambda2-tau)[1-(rank sigma_c==2)]`. Its script's `V(rank)` and assigned caustic/rank model are the inputs inspected here. Its reported rank-0/rank-1 false positives and rank-2 host hole motivate the question; these campaign scores were **not independently rerun or authenticated**.

The prior `main_theory/claude_cfg355_bulk_phase_2026_10_06/REPORT.md` proved that centered moments lose host-relative bulk velocity. The present example also fixes that velocity: `u=0` in both states everywhere. The first lost transport information is the third velocity tensor, or, in a parity-even control, the fourth. Rank is not enough; neither is replacing rank by the complete second tensor. All inspected paths/hashes and actual HEAD are in SOURCE_PROVENANCE.json. Requested base: `85251b027`.

## Exact self-gravitating comparison

Work in three-dimensional Newtonian collisionless gravity, with `G=M=b=1`, mass phase-space density f, isolated potential zero at infinity, and

`psi=(1+r²)^(-1/2), Phi=-psi, rho=3 psi^5/(4 pi)`.

Direct differentiation gives `lap Phi=4 pi rho`; total mass is one. The Plummer potential is smooth and bounded at its center. No external host or invisible boundary potential is needed.

The stationary comparison state is

`f_eq(x,v)=24 sqrt(2)/(7 pi³) [psi(x)-v²/2]_+^(7/2)`.

It is a function of the conserved one-particle energy `v²/2+Phi`. Therefore `v.grad_x f-grad Phi.grad_v f=0` wherever differentiable, with the cutoff also satisfying the weak equation. Direct radial velocity integration, using `v²=2 psi u`, gives

`<|v|^(2k)>=(2 psi)^k B(k+3/2,9/2)/B(3/2,9/2)`.

The normalization gives exactly rho; angular averages yield

`u_i=0, Pi_ij=rho psi delta_ij/6, Q_ijk=0`,

`R_xxxx=rho psi²/14, R_xxyy=rho psi²/42`.

Here Pi, Q and R denote unnormalized mass velocity tensors. All odd velocity moments vanish. The distribution is stationary and isotropic; “virialized host” here means this exact collisionless equilibrium, not a claim about a cosmological assembly history.

At each x put `sigma=sqrt(psi/6)`. Independently in each Cartesian velocity coordinate choose

`v=+sqrt(2) sigma with weight 1/3; v=-sigma/sqrt(2) with weight 2/3`.

The product gives eight positive stream weights w_s, summing to one. Define

`f_8(x,v)=rho(x) sum_s w_s delta³(v-v_s(x))`.

These are ordinary cold stream initial data: eight distinct smooth velocity graphs at each finite x, positive mass weights and finite total mass. Their common initial density supplies precisely the same Poisson potential as f_eq. The collisionless equation is an evolution law, not an extra instantaneous algebraic constraint forcing these graphs to be stationary. Its initial weak time derivative follows by applying the Hamiltonian transport operator to f_8; equivalently each graph initially evolves by `partial_t v_s+(v_s.grad)v_s=-grad Phi`, and its density by `partial_t rho_s+div(rho_s v_s)=0`. We do not assert a stationary stream solution, a global evolved halo, or a global smooth evolution through later caustics.

The elementary one-coordinate moments are

`<v>=0, <v²>=sigma², <v³>=sigma³/sqrt(2)`.

Product independence now proves, at **every x**, identical rho, u, Pi, covariance rank three, full potential and all its spatial derivatives. In particular any CFG355 veto and any instantaneous deterministic function of those identical fields and their spatial jets returns the same answer. The phase-space measures are different: f_eq has a continuous energy distribution while f_8 has eight intersecting cold velocity graphs. All eight speeds obey `|v_s|²<=6 sigma²=psi<2 psi`, so every stream initially has negative energy in this isolated potential. The distinction is **stationarity versus nonstationary streams**, not bound versus unbound; none of these statements predicts escape or thermalization.

The difference is

`Q_iii(f_8)=rho sigma³/sqrt(2), Q_ijk=0 for other index patterns`.

The initial integrated kinetic and potential energies even coincide: `K=3 pi/64`, `W=-3 pi/32`, hence `2K+W=0` in both states. This finite scalar energy balance is not a stationarity test. No claim about a finite inertia integral is made: Plummer's second spatial mass moment diverges.

## Actual transport hierarchy and decisive evolution

Start from `partial_t f+v_k partial_k f-Phi_,k partial_(v_k) f=0`. Multiply by a velocity monomial and integrate (distributionally for streams). Integrating the force term by parts gives the full raw moment hierarchy

`partial_t M_(i1...im)+partial_k M_(i1...im k)+sum_a Phi_,ia M_(i1...omit ia...im)=0`.

For the first levels:

`rho_dot+partial_i(rho u_i)=0`,

`(rho u_i)_dot+partial_j P_ij+rho Phi_,i=0`,

`P_ij_dot+partial_k T_ijk+Phi_,i rho u_j+Phi_,j rho u_i=0`,

`T_ijk_dot+partial_l R_ijkl+Phi_,i P_jk+Phi_,j P_ik+Phi_,k P_ij=0`.

At the shared u=0 instant, raw P,T coincide with Pi,Q. The common fields satisfy exact Jeans balance `partial_j Pi_ij+rho Phi_,i=0`; thus rho_dot=u_dot=0 in both states. This does not close stress evolution: it requires the independent third moment. For the eight-stream state at x=(r,0,0),

`Pi_xx_dot=-d_r [rho sigma³/sqrt(2)]`,

while the equilibrium derivative is zero. Since `rho sigma³ ∝(1+r²)^(-13/4)`, at r=1 the difference is exactly

`Pi_xx_dot(f_8)-Pi_xx_dot(f_eq)=(13/4) rho(1) sigma(1)³/sqrt(2)>0`.

There is no unspecified force prescription in this result. The common Poisson acceleration and actual conservation laws were used. The central-moment equation more generally is

`D_t Pi_ij+Pi_ij partial_k u_k+Pi_ik partial_k u_j+Pi_jk partial_k u_i+partial_k Q_ijk=0`.

A local density+tidal+second-moment closure cannot assign this derivative correctly to both states. A relevant extra datum for this example is the third central tensor and its transport divergence. Its contracted heat flux `q_i=Q_ijj/2` is a measurable energy-transport quantity relative to u, not a proposed fitted switch or a conserved scalar invariant. It is independent of the covariance; it is not itself a sufficient universal equilibrium classifier.

## Parity-even control: hiding the third moment

Define six equally weighted velocities `v=+/-sqrt(3) sigma e_i`. Their density, mean and second moments equal the same equilibrium everywhere, and all third moments vanish. Thus even the first stress derivative is now identical. However

`R_xxxx(f_6)=rho psi²/12, R_xxyy(f_6)=0`.

At x=(r,0,0) the equal force terms in the third-moment equations cancel between the two states. Consequently

`Q_xxx_dot(f_6)-Q_xxx_dot(f_eq)=-d_r[rho psi²/84]`.

At r=1 this is `(7/2) rho(1) psi(1)²/84>0`. Initially the third moment itself is zero in both states, yet its evolved value differs. The six-stream speed satisfies `v²=psi/2<2psi`. This is an explicit next-level failure of the third-moment repair, not a proof against every finite observable set. Spatial variation of the higher moment is essential: a locally constant flux need not produce the same immediate discriminator.

## What is learned and what is still missing

The exact lost information is how mass occupies velocity space and transports stress across the leaf. The local moment inputs can match even while the collisionless state changes. A growing-mode or caustic-history prior may restrict the allowed stream configurations and evade this unrestricted comparison; that prior must then be specified and evolved, rather than inferred from rank. Exact equilibrium can be tested by Hamiltonian transport of the complete distribution; using a distribution function, labeled streams, or a justified kinetic closure is new physical content. No universal finite-moment impossibility theorem or unique replacement reader is claimed.

This directly sharpens CFG355's premise: covariance rank is informative about stream geometry, but cannot identify phase equilibrium. It does not alter its frozen numerical verdicts, MS1 legality permission, width issue, source reaction, or same-action obligations. Vlasov dynamics is explicitly the declared cold collisionless model for this discriminator. Whether CFG288's wave field admits the same kinetic approximation, how its mass/charge abundance is set, and how this helps a reciprocal MOND source are separate unproved implications. No particle label, vacuum relation or 32pi selection follows.

## Bounded verification

`checks.py` performs exact symbolic velocity sums, equilibrium beta/gamma integrals, Poisson/Jeans identities and the two nonzero transport derivatives. The analytic construction above supplies the full-domain argument; 18 passing checks are corroboration, not a proof count. `runs/main_a` passes all 18. `control_skew_a` replaces the asymmetric two-point law by a symmetric one and rejects the claimed nonzero third moment. `control_fourth_a` replaces the six-stream fourth moment by the equilibrium value and rejects the explicit fourth-moment difference. Both controls retain intended failures and raw logs. Standard runner bounds: 45 s wall, 30 s CPU, one cooperative numerical-library thread, 100000 log bytes; no hard memory or affinity cap. All three manifests validate with current input/result hashes. No Claude script was executed. No external named theorem, observational number or novelty claim is imported.
