# Discrete Rindler reflection qualification

This issue was investigated after the coordinator raised a discrete-action precision question. The primary PDF text at equation 34 says that both barred loop variables are clover-type averages of four loops; section III.B says that z boundaries are open and centered. It does not provide a complete boundary-loop construction or implementation.

For a standard site-centered clover, the four quadrants of a mu-z plaquette or rectangle permute under z -> -z; orientation reversal leaves ReTr unchanged. If the same reflected stencil and boundary weights are used at the two ends, E_x(RU)=E_Rx(U) and B_x(RU)=B_Rx(U). Haar invariance then gives S_eta(RU)=S_-eta(U) and Z(eta)=Z(-eta). This is a sufficient discrete proof, with no continuum approximation.

Centered coordinates by themselves do not establish these identities. For example, reflection of a single forward plaquette generally changes its anchor in the reflected direction. A z-dependent coefficient evaluated at the old anchor need not transform to the coefficient at the new anchor. Likewise, asymmetric loop removal at open ends can spoil the clover identity. The exact paper's boundary stencil has not been authenticated at that implementation level.

Consequently:

- The stated eta derivatives of equation 34 and W_etaeta=E[S_etaeta]-Var(S_eta) are verified for eta-independent loop/boundary definitions, without any reflection premise.
- Exact evenness and W_eta(0)=0 are verified only for an explicitly reflection-covariant centered clover and boundary prescription. They are not certified as a measured property of the authors' simulation code.
- The independent source fixture is paired by construction and checks the conditional algebra, not the missing implementation detail.
- The author's phrase “for a reflection-invariant centered domain/measure” can be retained as a hypothesis. Describing actual source simulation evenness as unconditionally verified would overstate this audit.

This qualification does not affect the independent sphere response derivation or the Bai--Chen connected/contact admission issue. It supplies no H map or thermodynamic uniformity.
