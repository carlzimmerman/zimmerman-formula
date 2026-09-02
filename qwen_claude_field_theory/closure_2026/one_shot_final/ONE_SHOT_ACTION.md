# Curvature-sourced QUMOND: action, equations, and obstruction

## One explicit action

The tested candidate is

\[
S={1\over16\pi G}\int d^4x\sqrt{-g}\left[
R-2\Lambda-2\lambda(\Delta_h\chi-R_{\mu\nu}n^\mu n^\nu)
+2a_0^2Q(Y)\right]+S_m[g,\psi],
\]

where

\[
n_\mu=-{\nabla_\mu T\over\sqrt{-\nabla T\cdot\nabla T}},\quad
h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu,\quad
Y={h^{\mu\nu}\nabla_\mu\chi\nabla_\nu\chi\over a_0^2},
\]

and

\[
Q(y^2)=1-(1+y)e^{-y},\qquad Q_Y={e^{-y}\over2},
\qquad \mu(y)=1-e^{-y}.
\]

Ordinary matter and photons couple minimally to the same metric. No matter
field appears in the auxiliary action.

## Varied weak-static equations

For the isolated/asymptotically flat scalar-isotropic static branch, variation
with respect to all four fields and removal of the harmonic integration modes
gives

\[
\chi=\Phi,\qquad \Psi=\Phi,\qquad
\nabla\lambda=(\mu-1)\nabla\Phi,
\]

and

\[
\nabla\!\cdot\!\left[\mu(|\nabla\Phi|/a_0)\nabla\Phi\right]
=4\pi G\rho_b.
\]

In spherical symmetry,

\[
\mu(g/a_0)g=g_N,
\]

so \(g^2=a_0g_N\) in the deep-MOND limit and
\(v^4=Ga_0M_b\). At high acceleration \(\mu\to1\), and this normalization
gives \(G_{\rm measured}=G\) in the same weak branch.

The scalar-isotropic variation alone is not a complete no-slip proof. The
complete static trace-free spatial equation is

\[
\left[N R_{ij}-D_iD_jN
+2N D_{(i}\lambda D_{j)}\chi
+2\lambda D_{(i}N D_{j)}\chi
-2D_{(i}\lambda D_{j)}N
+2NQ_YD_i\chi D_j\chi\right]^{\rm TF}=0.
\]

Its finite-momentum linearization gives

\[
k^2(\Phi-\Psi)=0,
\]

and therefore \(\gamma=1\) for \(k\ne0\). At second order, on the leading
shell \(\chi=\Phi=\Psi=u\), it gives

\[
(p_2-n_2)''+u u''-\mu(u')^2=0.
\]

This determines second-order slip; it is not a linear PPN failure and it does
not yet establish exact nonlinear \(\Phi=\Psi\) or \(\beta=1\).

## Canonical finite-momentum branch

In unitary clock gauge the kinetic terms are

\[
\mathcal L_{\rm kin}=(1-2\lambda)(K_{ij}K^{ij}-K^2)
+2K\mathcal L_n\lambda.
\]

The generated seven-velocity Hessian has

\[
\det H=-3072(1-2\lambda)^5.
\]

On the flat \(\bar\lambda=0\), \(\bar\chi={\rm constant}\), finite-\(k\)
branch, the gauge-fixed scalar calculation generates three primaries

\[
p_\chi\approx0,\qquad p_\alpha\approx0,\qquad p_\beta\approx0,
\]

and three secondaries

\[
C_\chi=2k^2(\chi+\ell),\quad
C_\alpha=-2k^2(\ell-2\zeta),\quad
C_\beta={k^2\over3}(4k^2\beta+p_\zeta).
\]

The generated six-by-six Poisson matrix has rank four. Preservation fixes the
remaining relevant multipliers and generates no tertiary constraint. In the
ten-dimensional scalar phase space there are two first-class and four
second-class constraints, leaving one scalar degree of freedom. Restoring the
spatial scalar shear gives a twelve-dimensional phase space with four
first-class and two second-class constraints and the same one scalar.

Restoring \(T=t+\pi\) shows that \(\pi\) contributes only a boundary term on
this special branch. The surviving pole has zero clock projection:

\[
L_{\rm red}=6\dot\zeta^2-2k^2\zeta^2,
\qquad \omega^2=k^2/3.
\]

Thus it is a healthy-sign but forbidden non-clock scalar on this branch. The
transverse vector constraint chain leaves no vector pole. This is not promoted
to a generic nonlinear degree count.

## Exact action-class obstruction

The regular radial \(\chi\) equation, varied before integration, is

\[
{d\over dr}\left[r^2(\lambda_r+e^{-y}\chi_r)\right]=0.
\]

Regularity removes the singular auxiliary flux and gives

\[
\lambda_r=-a_0y e^{-y}<0\qquad(0<y<\infty).
\]

The TT principal action from the same action is

\[
\mathcal L_{TT}^{\rm principal}
={1-2\lambda\over2}\dot h_{TT}^2-{1\over2}(\nabla h_{TT})^2,
\qquad c_T^2={1\over1-2\lambda}.
\]

Exact physical-metric luminality requires \(\lambda=0\) pointwise and hence
\(\lambda_r=0\), contradicting the exact finite-\(y\) MOND branch. This is the
load-bearing no-go.

A finite-shell numerical check solves the implicit relation
\(y(1-e^{-y})=g_N/a_0\). The resulting action-forced variation is
\(O(v_{\rm flat}^2/c^2)\). For every additive integration constant, at least
one shell endpoint has \(|\lambda|\geq|\Delta\lambda|/2\), leaving the local
tensor-speed shift far above the stated multimessenger bound. This numerical
strengthening is not needed for the exact proof.

## Separate homogeneous, zero-field, and Ward sectors

On homogeneous FLRW, \(\Delta_h\chi=0\) and
\(R_{nn}=-3\ddot a/a\). The multiplier equation requires \(\ddot a=0\), so
coasting expansion with \(H\ne0\) is possible but accelerating FLRW is not
obtained on this branch. The remaining homogeneous equations and perturbations
do not establish a viable cosmology.

At \(y=0\), both principal eigenvalues of the eliminated MOND operator vanish.
The finite-\(k\) raw \(p_\chi,C_\chi\) bracket does not vanish there. This
distinction is computed explicitly; no nonlinear continuation through the
rank-changing response is supplied.

Because \(S_m[g,\psi]\) is separately diffeomorphism invariant and minimally
coupled, its on-shell Noether identity gives
\(\nabla_\mu T^{\mu\nu}=0\) for ordinary matter. The fixed-normal alternative
breaks this covariant setup and has a nonzero boosted preferred-frame
diagnostic; the clock-normal realization retains the Ward identity but pays
the canonical price above.

The relation \(a_0=c^2\sqrt{\Lambda/(32\pi)}\) is not derived by this action.

## Verdict

The displayed scalar curvature-sourced QUMOND action class is **DEAD** under
exact tensor luminality. Linear \(\gamma=1\) is retained, but complete PPN,
nonlinear no slip, viable FLRW, and controlled zero-field evolution remain
unclosed. The general relativistic-MOND existence problem remains **OPEN**.
