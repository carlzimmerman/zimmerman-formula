# Independent NR-invisible quadratic completion audit

Primary verdict: **proved as written within the five displayed parity-even quadratic contraction types, leading stationary weak-NR variation, and conditional regular coincident-vacuum tensor block**. No blocking correction. The operator supplies a constructive curvature-mass repair of a regular subcritical tensor slope, but no critical tensor kinetic repair. Stationary action invisibility must not be enlarged to pointwise invisibility under arbitrary time-dependent connection jets.

Reviewed frozen REPORT.md SHA25619c7c29b14b2738cbae3e8d1373629fea8c17c84146e5ef30a14c991d9e412d6 and checks.py SHA25667385feb26a2b45618e02bef019fe4db8d072b91c75b7d2d1279e3699c98d6dd. No author inputs were edited or author scripts executed. The candidate has the repaired symmetric averaged contractions and volume; the regular negative-invariant vacuum extension and auxiliary admission are still separate hypotheses.

## Raw static values and all spatial first variations

Independently contract the prescribed static connections with η=diag(−1,1,...), q=1/(n−2), arbitrary static gradient a_i. Their traces are
C_i=(1−nq)a_i=−2q a_i, bar C^i=[−1+q(n−2)]a_i=0,
and the temporal traces vanish. This gives
S1=−(n−1)q a², S2=S3=0, S4=4q²a², S5=−3S1+S4.
In particular n=3 has(S1,S2,S3,S4,S5)=a²(−2,0,0,4,10), so J=3S1−2S2−S4+S5=0.

For arbitrary spatial Christoffel variation define P=a_k δC^k_(ii) and R=a_k δC^i_(ki), summing repeated indices. Direct index contraction gives
δS1=−2qP, δS2=−2qP, δS3=0,
δS4=−4qR, δS5=2qP−4qR.
For example n=3 and a alongx, choosing only ∂x h_yy=1 gives P=−1/2,R=1/2, and variations(+1,+1,0,−2,−3), whose J variation vanishes. This checks the independent trace/contraction normalization rather than adopting a symbolic nullspace's verdict. P and R can be independently varied using spatial trace and off-diagonal derivative jets for n≥3.

Thus δ(sum c_A S_A)=−2q(c1+c2−c5)P−4q(c4+c5)R. Vanishing for all spatial perturbations imposes c1+c2=c5 and c4=−c5. The static value then reduces to S1(c1−3c5), forcing c1=3c5 and c2=−2c5. c3 remains free. This proves exactly span{J,S3} in the stated contraction space for general n≥3; finite n checks are corroboration, not completeness proof.

## Independent lapse and time-dependent shift scope

The spatial result alone is not sufficient to establish lapse variation. Set temporal variations δC^0_(0i)=δC^0_(i0)=u_i and δC^i_(00)=v_i independently. Direct contraction yields
δS1=−2a·v, δS2=2q a·v, δS3=0,
δS4=−4q a·u, δS5=4a·u+2a·v,
therefore δJ=4(1+q)a·(u−v).
An independent lapse variation has u=v=−∂iδh00/2 and gives zero. A shift variation has u−v=−∂0δh0i at this weak order. Thus the nonzero temporal jet term is −4(1+q)a_i∂0δh0i. Its action integral is a time boundary when a_i, the background volume and xi are stationary; compact-support test variations yield no stationary shift source. If the background evolves, the coefficient's time derivative can contribute a bulk equation. The frozen report explicitly preserves this limitation.

Static shift spatial derivatives have the opposite temporal-index parity and no linear cross term with the scalar branch. Since J=δJ_spatial=0 and its remaining stationary action variation is a boundary, multiplying by a smooth stationary xi(z,T) preserves leading NR metric and auxiliary equations. This is not exact strong-field invisibility: variation of contracting metrics/volume and higher weak orders remain outside this argument.

## Independent tensor contractions and curvature term

On common FRW, set d=γ−hatγ TT. The raw connection components are C^0_(ij)=a²(Hd+dot d/2), C^i_(0j)=dot d/2 and the spatial half-gradient connection; both trace vectors vanish. The temporal norm in S5 is
−tr(Hd+dot d/2)²−tr(dot d²)/2,
while the spatial norm is3tr[(∂d)²]/(4a²) after transversality. Hence
S5=−3tr[dot d²−a^−2(∂d)²]/4−Htr(d dot d)−H²tr d².
With S1=tr[dot d²−a^−2(∂d)²]/4+Htr(d dot d), one gets
J=2Htr(d dot d)−H²tr d².
S2=S3=S4=0. Thus J and S3 have no TT kinetic or spatial-gradient coefficient. In the paper's notation S_q=(J−S3)/2, so choosing S_q instead changes non-TT terms but gives the same TT calculation; no two different full operators are silently equated.

Integration by parts gives∫a^nJ=−∫a^n[(n+1)H²+dot H]tr d² plus boundary. Constant xi0 therefore adds−Kxi0(n+1)H²tr d²/2 on de Sitter. Combined with the independently audited parent action this yields
q_T=K(1−2m)/8,
μ²=4[xi0(n+1)−mn]H²/(1−2m).
For m<1/2 and xi0≥mn/(n+1), the tensor has positive kinetic and nonnegative mass. Its exact comoving-mode energy decreases: dot E=−nHdot d²−H(k/a)²d². Strict inequality bounds amplitudes with a positive mass; equality is the bounded massless de Sitter equation. Example n=3,m=xi0=1/4 gives q_T=K/16 and μ²=2H², retaining the conditional NR radial boost3/2. This genuinely escapes the parent's curvature-induced regular-slope tachyon by changing the action, not by relabeling a frozen dispersion relation.

At m=1/2 q_T remains zero for every xi0. If n/2−xi0(n+1) is nonzero the relative-TT equation remains algebraic d=0; at xi0=n/[2(n+1)] the whole quadratic relative-TT block vanishes. Neither yields positive propagating kinetic. No ghost, nonlinear strong-coupling scale, or full nonlinear constraint count is inferred from this rank statement. At H=0 the J tensor effect is zero, consistent with its curvature origin.

## Primary and scope checks

Independently opened the exact primary [Milgrom, Broader view of bimetric MOND, arXiv:2208.10882v4](https://arxiv.org/pdf/2208.10882v4), on2026-10-06. Its equation55 matches S_q=(3S1−2S2−S3−S4+S5)/2. Equation51 gives a sufficient mixed-free class; the added equation99 allows a broader class when interaction derivatives vanish on the NR branch. These statements support the report's bounded attribution, not a necessary classification of every covariant completion. No new paper copy/hash or novelty claim is supplied.

The report's completeness claim is limited to five displayed quadratic types and smooth linear coefficients at leading weak order. Smooth interactions whose derivative vanishes at the origin cannot change the quadratic tensor block because each invariant starts at connection order two. Singular derivatives, added derivatives/nonlocal structures, other invariant tensors, a noncoincident vacuum, or a different auxiliary branch are not classified. Scalar/vector health, matter coupling, EFT scales and exact strong-field source preservation remain open. Xi0 supplies a new free dimensionless coefficient; a stable cone inequality does not select lambda, the offset, or32π. At coincident C=0 this additional quadratic invariant has zero value/first variation and does not alter the conditional background cosmological-constant value.

## Executable evidence

Independently validated all four standard manifests against current bytes: main_a39/39, control_H_a39/40, control_kinetic_a39/40, control_value_a39/40. Failure locations are the declared omitted-H contraction, false critical kinetic repair and false S5 static-value invisibility assertions. The implementation's raw contraction sums and spatial h_ij,k basis cover n=3,4,5,6; separate exact general-n identities supply the proof. Its temporal tests agree with the independently derived u−v coefficient. REPORT is a frozen execution input and remained unchanged during review.

The strongest result is a real stationary-NR-invisible curvature repair of regular-slope tensor growth, with a sharp inability to restore critical TT derivatives within this displayed operator class. The first unresolved implication remains a fully admitted Lorentzian/auxiliary action and its all-helicity nonlinear constraints; the constructive regular tensor example is not a complete healthy MOND/cold theory.
