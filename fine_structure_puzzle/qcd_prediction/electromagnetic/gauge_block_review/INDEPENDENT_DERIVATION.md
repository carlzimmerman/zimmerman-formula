# Independent static spherical phase/radial-gauge derivation

This derivation was saved before reading the vacuum agent's new phase_block. The only vacuum artifacts read were the frozen REPORT.md and determinant_followup/REPORT.md and VECTOR_BLOCK.md. It uses the fixed-circle BPS background, not an electromagnetic or cosmological approximation.

## Ansatz, residual gauge symmetry and action

Use \(D_i c^a=\partial_i c^a+\epsilon^{abc}A_i^bc^c\), \(n_i=x_i/r\), and
\[
A_i^a={1-w_1\over r}\epsilon_{aij}n_j
+{w_2\over r}(\delta_{ai}-n_an_i)+b\,n_an_i,\qquad
\Phi^a=n^a H.
\]
With \(w=w_1+iw_2\), the residual radial gauge group acts as
\[
w\mapsto e^{i\lambda}w,\qquad b\mapsto b+\lambda',
\qquad D_rw=w'-ibw.
\]
Apart from \(4\pi L/g^2\), the static reduced action is
\[
E=\int_0^Rdr\left[
|D_rw|^2+{(|w|^2-1)^2\over2r^2}
+{r^2H'^2\over2}+H^2|w|^2\right].
\]
The BPS saddle is \(w=K=mr/\sinh(mr)\), \(b=0\),
\(H=m\coth(mr)-1/r\), with
\[
K'=-KH,\qquad H'={1-K^2\over r^2},\qquad
K''=K[H^2+(K^2-1)/r^2].
\]

Set \(w=K+iv\) in the odd/phase sector. Its quadratic action is
\[
E_{\rm phase}^{(2)}=\int dr\left[
(v'-Kb)^2+2K'bv+
\left(H^2+{K^2-1\over r^2}\right)v^2\right].
\]
In particular the \(2K'bv\) term cannot be dropped. The infinitesimal gauge direction is
\[
\delta v=K\lambda,\qquad \delta b=\lambda'.
\]
For \(v=K\vartheta\), the action becomes
\[
E_{\rm phase}^{(2)}
=\int dr\,K^2(\vartheta'-b)^2
+[KK'\vartheta^2]_0^R.
\]
Thus a nonzero gauge-invariant combination remains; this entire sector is not pure gauge.

## Background gauge and canonical radial fields

Direct covariant divergence gives
\[
G^a=D_i\delta A_i^a=n^a
\left(b'+{2b\over r}-{2Kv\over r^2}\right).
\]
The Higgs variation belongs to the real sector and its commutator vanishes in this spherical channel. The background Feynman-gauge term is \(\frac12\int r^2G^2dr\).

The fluctuation norm is \(\int dr(2v^2+r^2b^2)\). Hence set
\[
Y=(u,w)^T=(\sqrt2v,rb)^T,\qquad a(r)={\sqrt2K\over r}.
\]
The reduced ghost field is \(s=r\lambda\). Define
\[
\mathcal R=\begin{pmatrix}a\\\partial_r-1/r\end{pmatrix},\qquad
\mathcal R^\dagger=(a,-\partial_r-1/r),\qquad
\mathcal T=(\partial_r+H,-a).
\]
Then
\[
Y_{\rm gauge}=\mathcal R s,\quad
rG=-\mathcal R^\dagger Y,\quad
\mathcal T\mathcal R=0,\quad
\mathcal R^\dagger\mathcal R
=-\partial_r^2+{2K^2\over r^2}\equiv\mathcal L_{\rm gh}.
\]
Modulo the stated boundary terms, the gauge-fixed Hessian is
\[
\mathcal H_{\rm phase}
=\mathcal T^\dagger\mathcal T+\mathcal R\mathcal R^\dagger
=-\partial_r^2+
\begin{pmatrix}
H^2+(3K^2-1)/r^2&2\sqrt2(K'/r-K/r^2)\\
2\sqrt2(K'/r-K/r^2)&2(K^2+1)/r^2
\end{pmatrix}.
\]
It obeys the formal intertwining
\(\mathcal H_{\rm phase}\mathcal R=\mathcal R\mathcal L_{\rm gh}\).
The ungauged action agrees with
\(\frac12\int|\mathcal TY|^2dr+[K'v^2/K]_0^R\).

The scalar physical partner is
\[
\mathcal P=\mathcal T\mathcal T^\dagger
=-\partial_r^2+H^2+H'+{2K^2\over r^2}
=-\partial_r^2+H^2+{1+K^2\over r^2}.
\]
It is different from \(\mathcal L_{\rm gh}\).

## Origin and wall domains

Near the origin the canonical phase potential is
\[
{1\over r^2}
\begin{pmatrix}2&-2\sqrt2\\-2\sqrt2&4\end{pmatrix}+O(1).
\]
Its eigenvalues are 0 and 6. Smooth spatial gauge fields select reduced behaviors \(r(\sqrt2,1)^T\) and \(r^3(1,-\sqrt2)^T\), with their smooth subleading corrections. The irregular/point-defect extensions are excluded. The scalar ghost and physical partner both have the usual regular \(r^2\) behavior.

Framed gauge transformations require \(\lambda(R)=0\), or \(s(R)=0\). Full vector Dirichlet data would impose \(u(R)=w(R)=0\). A framed ghost produces \(u(R)=0\) but \(w(R)=R\lambda'(R)\), generally nonzero. Thus those two Dirichlet operator domains are not paired by the gauge map. Requiring both \(\lambda(R)=\lambda'(R)=0\) would overdetermine the second-order ghost spectral problem.

The relative vector alternative is
\[
u(R)=0,\qquad (\mathcal R^\dagger Y)(R)=0,
\]
equivalently
\[
v(R)=0,\qquad b'(R)+2b(R)/R=0.
\]
It is a self-adjoint mixed vector problem. A Dirichlet ghost eigenfunction maps into this vector domain, since
\(\mathcal R^\dagger\mathcal R s=\lambda_{\rm eig}s\).

For an explicit first-order domain statement let
\(\mathcal D Y=(\mathcal TY,\mathcal R^\dagger Y)^T\).
Choose the form domain of \(\mathcal D\) to have \(u(R)=0\).
The Green boundary form is \(t^*u-z^*w\), so its adjoint domain requires \(z(R)=0\) and leaves \(t\) free. Consequently
\[
\mathcal D^\dagger\mathcal D=\mathcal H_{\rm phase,rel},
\qquad
\mathcal D\mathcal D^\dagger
=\operatorname{diag}(\mathcal P_{\rm Robin},\mathcal L_{\rm gh,D}),
\]
where
\[
t'(R)-H(R)t(R)=0,\qquad s(R)=0.
\]
This is a spectral domain pairing, not a pairing to two Dirichlet scalar problems.
For finite R, K is nonzero; the physical quadratic form
\(\|\mathcal T^\dagger t\|^2\) has no kernel, and the framed ghost has none.
Subject to the smooth-origin first-order domains, their nonzero spectra form the vector spectrum.
The phase/vector determinant is therefore the product of these two scalar determinants, with the displayed Robin and Dirichlet domains. A complex ghost then leaves a factor proportional to
\[
\left[{\det\mathcal L_{\rm gh,D}\over
\det\mathcal P_{\rm Robin}}\right]^{1/2}
\]
in this static channel, rather than complete cancellation.

This is a boundary-dependent reduction only. A physical relative determinant still needs the same admissible reference, wall action, regulator and subtraction; it is not a computed full monopole weight.

## BRST caveat

All-vector Dirichlet with only framed ghost Dirichlet already fails the essential-boundary transformation \(sA_n=D_nc\). Relative tangential Dirichlet is preserved by \(c|_\partial=0\). Its natural gauge-fixing condition \(G|_\partial=0\) is preserved by ghost eigenfunctions or a compatible common spectral core; it is not preserved by every smooth Dirichlet ghost off shell because \(sG=-\mathcal M_{\rm gh}c\). A full off-shell statement must specify antighost/auxiliary-field boundary data or the relative gauge complex before eliminating the auxiliary field. Self-adjointness alone is not that statement.
