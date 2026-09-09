# Localized V4 clock--York candidate

This directory is a constructive continuation of the V3 exponential clock
branch.  It replaces the spatial pseudoinverses by explicit elliptic fields
and multipliers, then asks the phase-space calculation whether those fields
are genuinely auxiliary.

With (c=1), normalized clock normal (n^μ), induced metric (h_{ij}),
extrinsic curvature (K_{ij}), and (J_i=D^mK_{im}), the local prototype is

\[
\begin{aligned}
S_{\rm loc}=S_{\rm EH}+{1\over16\pi G_b}\int\sqrt{-g}\,[
&-\ell\theta^2+a_0^2f(a/a_0)+\eta_U U^2+\eta_XU\chi\\
&+\eta_V(2A^iJ_i-A^i{\cal H}_1A_i)\\
&+\eta_{TT}(K_{TT}^{ij}K^{TT}_{ij}-2Q^{ij}R^{TT}_{ij}
                +Q^{ij}{\cal H}_{TT}Q_{ij})\\
&+\lambda_\chi(\Delta_h\chi-D_iD_jK^{ij})
 +\lambda_A D_iA^i+\lambda_Q^{ij}(D^kQ_{ki},Q^i{}_i)] .
\end{aligned}
\]

The flat nonzero-mode constraints are solved explicitly rather than asserted.
The zero mode is handled by a separate minisuperspace block.  The exact
coefficient witness is `C=5/3`, `ell=1/100`, `eta_U=1/12`, `eta_X=1/3`,
`eta_V=-1/3`, `eta_TT=-1/6`.

The present implementation is a prototype, not a completed covariant theory:
the York TT constraints are represented in the flat principal block, and the
metric-variation test is a finite weighted-cochain surrogate.  A positive
Dirac count in this directory would therefore be a constructive checkpoint,
not certification of the ten-gate target.
