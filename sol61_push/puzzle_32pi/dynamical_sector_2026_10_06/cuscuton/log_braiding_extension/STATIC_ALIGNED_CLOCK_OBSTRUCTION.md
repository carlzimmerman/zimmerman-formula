# Strictly static zero-shift aligned clock: exact momentum obstruction

**Restricted verdict:** the fixed-positive-A P2 extension does not admit a nonzero gravitational lapse gradient on a strictly static, zero-shift, clock-aligned source branch with vanishing matter momentum. The logarithmic braid itself forces D_i ln N=0. This is an exact necessary constraint, not a claim that all static metrics or clock-flow galaxy solutions are excluded.

The completed extension REPORT.md, SHA256 234ef41a096b92467f4ba6d4f758ba2e9f4e51fd02de11004dd3bd603622221a, is not an execution input to main_b or any of the three b controls. Its prose-only dust clarification therefore did not stale those records. All four manifests' listed input hashes were independently compared with current files and remain identical. This separate note does not change the report, checks, contract or original b run inputs. The independent peer review accepts the completed quadratic/source report at its pinned revision; the exact constraint below is an additional discriminator.

## ADM integration by parts before imposing staticity

Work in four dimensions on X>0, φ=qt with q>0 constant, lapse N>0, ADM shift N^i, and spatial metric h_ij. Let v=√(2X)=q/N, u the future unit normal, θ=∇u, and b=2c/(3H*)>0. For the logarithmic model G(X)=−b/v. Since ∇^μφ=−v u^μ,

□φ=−u^μ∂μv−vθ,
−G□φ=−b u^μ∂μ ln v−bθ
= b u^μ∂μ ln N−bθ.

The scalar kinetic term is K(X)=2c ln N−c ln[q²/(2Xref)]. By the identity ∇μ(u^μ ln N)=u^μ∂μ ln N+θ ln N, integrating the first braid term by parts gives

L_scalar=2c ln N−b θ ln N−Veff,
Veff=ρv+c ln[q²/(2Xref)],

up to the divergences b∇μ(u^μ ln N)−b∇μu^μ. Boundary terms are held fixed, or the variations have compact support away from the boundary. They cannot be discarded if a different boundary variational problem is intended. The lapse is dimensionless, [c]=mass^4, [b]=mass^3, [θ]=mass, consistent with a four-dimensional density.

This derivation was performed before setting θ or the shift to zero. Substituting a static ansatz into −G□φ before variation would miss its momentum constraint.

## Shift variation

For the normal foliation,

θ=[∂t ln√h−D_i N^i]/N,
N√h(−bθ ln N)=−b√h ln N ∂t ln√h
+b√h ln N D_i N^i.

Spatial integration by parts turns the shift-dependent part into −b√h N^i D_i ln N. Its shift Euler derivative is therefore −b√h D_i ln N. Equivalently, varying the covariant shift N_i gives −b√h D^i ln N.

The Einstein ADM shift derivative is K_E√h D_j(K^{ij}−h^{ij}θ), with K_ij=(h_dot_ij−D_iN_j−D_jN_i)/(2N). The fixed-A acceleration response depends on the normal acceleration a_i=D_i ln N and on N,h; it has no shift dependence. This statement applies to the exact response, not just its quadratic expansion. Let J^i=(1/√h)δS_m/δN_i define the matter shift source, so no momentum-sign convention is hidden. The exact momentum constraint is

K_E D_j(K^{ij}−h^{ij}θ)−b D^i ln N+J^i=0.

## Static aligned limit and what it excludes

Impose h_dot_ij=0 and N^i=0 in a stationary metric, φ=qt, with matter momentum J^i=0 in these coordinates. Then K_ij=θ=0 and the Einstein term vanishes. Consequently

b D_i ln N=0 ⇒ D_iN=0.

The norm of the stationary timelike Killing vector is N. A stationary slow test body has gravitational acceleration determined by D_i ln N; hence this branch cannot provide a nonzero attractive radial force or the intended P2 metric force. Fixing N at the outer boundary also fixes the same N throughout each connected spatial region. Neither nonzero baryon density nor isotropic pressure changes this momentum constraint when the matter momentum vanishes; their separate conservation and lapse/spatial equations still must be satisfied for any complete solution.

This is a necessary obstruction even before attempting the radial boundary-value equations. It does not rule out stationary metrics with a nonzero radial clock flow (which require a shift in unitary gauge), time-dependent spatial foliation, matter momentum or additional operators. A metric can be static in one coordinate system while the rolling clock is not aligned with its Killing vector; that physically different possibility remains open. The geodesic comoving first-order source control in the main report likewise uses a nonzero shift and is not excluded by this lemma.

For A=βθ the proposed formula is outside its positive-scale domain at θ=0. Defining a limiting or absolute-value continuation would be a changed constitutive prescription whose θ/shift variation must be derived anew. It cannot simply be used to evade the fixed-A result by substituting A=0 in formulas requiring A>0.

The missing bound-galaxy arrow is thus concrete: if this repaired action supplies the physical MOND force, its solution must contain actual clock flow or time dependence (or a changed matter/operator premise), and that same flow must be included in the radial constraint and finite-gradient health calculation. The fixed static P2 constitutive dictionary alone does not supply it. No general no-go for all static metrics, no new coefficient selector, and no finite-gradient health conclusion is claimed.
