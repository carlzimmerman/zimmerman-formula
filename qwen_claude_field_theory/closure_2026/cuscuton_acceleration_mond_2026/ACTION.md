# CAM action (constructive branch)

Let

\[
X_\tau=-g^{\mu\nu}\nabla_\mu\tau\nabla_\nu\tau>0,\quad
n_\mu=-\nabla_\mu\tau/\sqrt{X_\tau},\quad
h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu ,
\]

\[
D_\mu=h_\mu{}^\nu\nabla_\nu,\qquad
a_\mu=n^\nu\nabla_\nu n_\mu,\qquad
y={\sqrt{D_\mu uD^\mu u}\over a_0}.
\]

The constrained cuscuton/acceleration action is

\[
S_{\rm CAM}=\int d^4x\sqrt{-g}\left[
{M^2\over2}(R-2\Lambda)
\;+\;2M^2a_0^2Q(y)
\;+\;\sqrt{X_\tau}\,\ell^\mu(D_\mu u-a_\mu)
\;+\;\sqrt{X_\tau}\,\Lambda^{\mu\nu}
\bigl[D_\mu D_\nu u-D_\mu a_\nu\bigr]^{\rm TF}
\right]+S_m[g,\psi],
\]

with \(n_\mu\ell^\mu=0\) and

\[
Q(y)=y^2+2(1+y)e^{-y}-2,\qquad
\mu(y)={Q'(y)\over2y}=1-e^{-y}.
\]

In unitary gauge \(\tau=t\), \(a_i=D_i\log N\) and \(D_i u=\partial_i u\).
The factor \(\sqrt{X_\tau}\) is essential: it makes the relation term carry
the spatial measure \(\sqrt h\), not an extra lapse prefactor, so its lapse
variation is the intended elliptic multiplier divergence.
The field \(u\) is therefore leafwise elliptic; no \(u\)- or \(\ell^i\)-time
velocity occurs.  The transformation \(u\mapsto u+f(\tau)\) is a homogeneous
zero-mode redundancy.  The full covariant \(\tau\)-clock constraint algebra is
the next required calculation.
