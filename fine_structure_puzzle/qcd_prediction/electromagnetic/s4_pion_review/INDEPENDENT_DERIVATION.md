# Independent real-scalar S4 determinant derivation

This packet was derived without reading the coordinator's S4 packet. A fresh child received only the scalar problem, not the proposed coefficient list; its hand derivation was returned before these notes were written. The QCD-E parent independently checked the harmonic-sum arithmetic and real/complex multiplicities. No numerical or symbolic experiment was executed.

For one real minimally coupled scalar on a round Euclidean four-sphere of radius \(H^{-1}\), restrict degree-\(\ell\) harmonic homogeneous polynomials in \(\mathbb R^5\). Radial separation and removal of polynomials divisible by \(r^2\) give
\[
\lambda_\ell=M^2+H^2\ell(\ell+3),\quad
d_\ell=\binom{\ell+4}{4}-\binom{\ell+2}{4}
={(\ell+1)(\ell+2)(2\ell+3)\over6}.
\]
The volume is \(V=8\pi^2/(3H^4)\). At fixed \(M>0\), the constant harmonic has eigenvalue \(M^2\), not a zero eigenvalue.

Put \(t=H^2s\), \(x=\ell+3/2\). Then
\[
\ell(\ell+3)=x^2-9/4,\quad
d_\ell=(x^3-x/4)/3.
\]
The added \(x=1/2\) term vanishes identically. Therefore
\[
{K_0(s)\over V}
={H^4\over8\pi^2}e^{9t/4}S(t),\qquad
S(t)=\sum_{n=0}^\infty[(n+1/2)^3-(n+1/2)/4]e^{-t(n+1/2)^2}.
\]
Mellin inversion gives the Euler–Maclaurin/Hurwitz expansion
\[
\sum_{n=0}^\infty(n+a)^p e^{-t(n+a)^2}
\sim {1\over2}\Gamma((p+1)/2)t^{-(p+1)/2}
+\sum_{k=0}^\infty {(-t)^k\over k!}\zeta(-p-2k,a).
\]
Using \(\zeta(s,1/2)=(2^s-1)\zeta(s)\),
\[
\zeta(-1,1/2)=1/24,\quad
\zeta(-3,1/2)=-7/960,\quad
\zeta(-5,1/2)=31/8064,
\]
one obtains
\[
S(t)\sim {1\over2t^2}-{1\over8t}-{17\over960}
-{457\over80640}t+O(t^2).
\]
Multiplication by the exact curvature prefactor gives
\[
2t^2e^{9t/4}S(t)
=1+2t+{29\over15}t^2+{74\over63}t^3+O(t^4).
\]
Hence
\[
{K_M(s)\over V}
={e^{-M^2s}\over(4\pi s)^2}
\left[1+2H^2s+{29\over15}H^4s^2
+{74\over63}H^6s^3+\cdots\right].
\]

The real scalar has \(\Gamma=\frac12\log\det(-\nabla^2+M^2)\).
Writing \(K_0/V=(4\pi s)^{-2}F(H^2s)\), a precise local-subtraction prescription is
\[
f_{\rm rem}=-{1\over32\pi^2}\int_0^\infty ds\,s^{-3}e^{-M^2s}
\left[F(H^2s)-1-2H^2s-{29\over15}H^4s^2\right].
\]
For fixed positive \(M\), it is finite at both endpoints. Watson-type small-\(H/M\) asymptotics give
\[
f_{\rm rem}
=-{74/63\over32\pi^2}{H^6\over M^2}
+O(H^8/M^4)
=-{37H^6\over1008\pi^2M^2}+O(H^8/M^4).
\]
The sign is from \(\log\det=-\int ds\,K(s)/s\), with the real-scalar factor \(1/2\).

Under \(g\mapsto e^{2\sigma}g\), \(V\mapsto e^{4\sigma}V\), \(H\mapsto e^{-\sigma}H\), with \(M\) fixed. The maximally symmetric stress coefficient is
\[
\rho={1\over4V}{d\Gamma\over d\sigma}
=f-{H\over4}\partial_Hf.
\]
The \(H^6\) term acquires \(1-6/4=-1/2\), giving
\[
\rho_{\rm rem}
=+{74/63\over64\pi^2}{H^6\over M^2}
+O(H^8/M^4)
=+{37H^6\over2016\pi^2M^2}+O(H^8/M^4).
\]

For the charged complex pion there are two real modes, with no additional doubling for the two charge labels. Define the shifted-minus-unshifted difference using \(\Delta>0\):
\[
\delta X=X_{\pi^\pm}(M^2+\Delta)-X_{\pi^\pm}(M^2).
\]
Then
\[
\delta f={37H^6\over504\pi^2}
{\Delta\over M^2(M^2+\Delta)}+O(H^8),
\]
\[
\delta\rho=-{37H^6\over1008\pi^2}
{\Delta\over M^2(M^2+\Delta)}+O(H^8)
={74/63\over32\pi^2}H^6
\left[{1\over M^2+\Delta}-{1\over M^2}\right]+O(H^8).
\]
These leading coefficients are exact in \(\Delta\) within the stipulated one-loop mass-shift comparison.

The fixed-positive-mass determinant has a small-curvature asymptotic expansion in even powers of \(H\); after the specified local terms it starts at \(H^6\). It has no algebraic linear-\(H\) coefficient. This is not a convergence claim, not a uniform massless-limit expansion, and not an assertion about additional QCD topological/global sectors.
