# One-shot Candidate B: curvature-sourced QUMOND

The second action tested in the one-shot attack is

\[
 S_B=\frac{1}{16\pi G}\int d^4x\sqrt{-g}\left[
 R-2\Lambda-2\lambda\left(\Delta_h\chi-R_{\mu\nu}n^\mu n^\nu\right)
 +2a_0^2Q(Y)\right]+S_m[g,\psi],
\]

with

\[
 n_\mu n^\mu=-1,\qquad h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu,
 \qquad Y=\frac{h^{\mu\nu}\nabla_\mu\chi\nabla_\nu\chi}{a_0^2},
\]

and

\[
 Q(y^2)=1-(1+y)e^{-y},\qquad Q_Y=\frac{e^{-y}}2
 =\frac{1-\mu(y)}2,\qquad \mu(y)=1-e^{-y}.
\]

`S_aux` contains no matter field. Thus ordinary matter remains minimally
coupled to `g` and the direct-matter Ward defect of Candidate A is absent.

## Weak static derivation

The varied scalar weak-static density is

\[
 \mathcal L=-2\Phi'\Psi'+\Psi'^2-8\pi G\rho\Phi
 +2\lambda'(\chi'-\Phi')+2a_0^2Q(\chi'^2/a_0^2).
\]

Its four Euler--Lagrange equations yield, on the asymptotically-flat scalar
branch, `chi=Phi`, `Psi=Phi`, and

\[
 \lambda'=(\mu-1)\Phi',\qquad
 \partial_i\!\left[\mu(|\nabla\Phi|/a_0)\partial_i\Phi\right]=4\pi G\rho.
\]

This is an action-derived exact exponential MOND result. It is not enough for
a relativistic theory: varying all spatial metric components gives the
trace-free stress

\[
 \Pi_Q^{\rm TF}=-2a_0^2y^2e^{-y},
\]

which is nonzero for every finite MOND gradient. On a constant-gradient patch
the `lambda R_nn` contribution is proportional to `D_iD_j lambda` and vanishes,
so it cannot cancel this stress. Candidate B therefore fails `Phi=Psi` in the
full metric equations.

## Foliation price

The action needs `n_mu`.

- A fixed normal gives a computed boosted elliptic coefficient `-1` in the
  alpha-2-like channel.
- A clock normal gives, already on FLRW, a velocity Hessian in `(a,lambda)`
  with determinant `-36 a^4`. This is nondegenerate and indefinite before any
  proposed constraint reduction.

The acceleration relation `a0=c^2 sqrt(Lambda/(32 pi))` is an external input
to this action; it is not derived.

**Candidate B verdict: DEAD.**
