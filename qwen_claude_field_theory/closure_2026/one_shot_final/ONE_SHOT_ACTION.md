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

This is an action-derived exact exponential MOND result in the scalar-isotropic
truncation. It is not enough for a relativistic theory: varying all spatial
metric components gives the trace-free constitutive stress

\[
 \Pi_Q^{\rm TF}=-2a_0^2y^2e^{-y},
\]

which is nonzero for every finite nonzero MOND gradient.  On the same local
patch, the algebraic trace-free stresses from the complete multiplier pair are

\[
 \Pi^{\rm TF}_{-2\lambda\Delta_h\chi}=-4a_0y\lambda',\qquad
 \Pi^{\rm TF}_{+2\lambda R_{nn}}=+4a_0y\lambda'.
\]

They cancel on the auxiliary shell `D_i chi=D_i N`; the trace-free Hessian of
the affine `lambda` witness also vanishes.  The complete residual is therefore

\[
 \Pi^{\rm TF}_{\rm aux}=-2a_0^2y^2e^{-y}\ne0\qquad(y>0).
\]

The full trace-free metric equation thus cannot retain `Phi=Psi` on this
witness.  The `Phi=Psi` equation obtained by varying only the scalar-isotropic
density is not a valid full-metric no-slip derivation.

## ADM and finite-momentum Dirac closure

For the covariant clock realization, choose unitary gauge `T=t` and

\[
 K_{ij}=\frac{\dot\gamma_{ij}-\mathcal L_{\vec N}\gamma_{ij}}{2N}.
\]

The exact identity

\[
 R_{nn}=-\mathcal L_nK-K_{ij}K^{ij}+N^{-1}D^2N
\]

gives, after integration by parts,

\[
 \mathcal L_{\rm kin}=(1-2\lambda)(K_{ij}K^{ij}-K^2)
 +2K\mathcal L_n\lambda.
\]

The seven-velocity Hessian in the six components of `K_ij` and
`L_n lambda` has

\[
 \det H=-3072(1-2\lambda)^5.
\]

Thus `lambda` is not a nondynamical multiplier on the regular
`1-2 lambda != 0` branch.

More decisively, about the branch required for luminal tensors,

\[
 \Lambda=0,\quad \bar\lambda=0,\quad \bar\chi={\rm constant},\quad k>0,
\]

the quadratic scalar action is derived term by term from the same ADM action:

\[
\begin{aligned}
L^{(2)}={}&-6\dot\zeta^2+6\dot\zeta\dot\ell
-4k^2\beta\dot\zeta+2k^2\beta\dot\ell\\
&+2k^2\zeta^2+4k^2\alpha\zeta-2k^2\alpha\ell
+2k^2\ell\chi+k^2\chi^2.
\end{aligned}
\]

The three primaries are

\[
 p_\chi\approx0,\qquad p_\alpha\approx0,\qquad p_\beta\approx0,
\]

and preservation generates

\[
 C_\chi=2k^2(\chi+\ell),\quad
 C_\alpha=-2k^2(\ell-2\zeta),\quad
 C_\beta=\frac{k^2}{3}(4k^2\beta+p_\zeta).
\]

The generated six-by-six Poisson matrix has rank four.  Preservation fixes the
remaining multipliers and produces no tertiary constraint.  In the
ten-dimensional gauge-fixed scalar phase space the result is two first-class
and four second-class constraints, leaving one scalar degree of freedom.
Restoring the scalar shear gives a twelve-dimensional phase space with four
first-class and two second-class constraints and leaves the same one scalar;
therefore the pole is not a premature gauge-fixing artifact.  In either form,

\[
 \ell=2\zeta,\qquad \chi=-2\zeta,
\]

and

\[
 \boxed{L_{\rm red}=6\dot\zeta^2-2k^2\zeta^2},\qquad
 \boxed{\omega^2=k^2/3}.
\]

The scalar is not a quadratic ghost or gradient instability; it is a genuine
hidden propagating mode, which is already fatal to `N_grav=2`.  The transverse
vector constraints leave no vector pole.  The tensor sector has

\[
 Q_T=1-2\bar\lambda,\qquad
 c_T^2=\frac{1}{1-2\bar\lambda},
\]

so positive exactly luminal tensors select `bar(lambda)=0`—the very branch on
which the scalar proof applies.

## Separate homogeneous and zero-field sectors

For exactly homogeneous FLRW, `Delta_h chi=0` and

\[
 R_{nn}=-3\ddot a/a.
\]

The exact `lambda` equation therefore imposes `ddot(a)=0`.  It excludes de
Sitter and an accelerating Lambda-FLRW solution but permits coasting expansion
`a(t)=At+B`; it does not force `H=0`.

At `y=0`, the raw finite-`k` `p_chi` bracket remains proportional to `k^2` and
does not lose rank.  The eliminated MOND response does lose rank because both
of its principal eigenvalues vanish.  No nonlinear zero-field evolution rule
is supplied.  On frozen nonzero-gradient backgrounds the raw `chi` principal
coefficient also vanishes at `y=1` for a pure longitudinal wave and, for
`y>1`, on `k_perp^2=(y-1)k_parallel^2`.  This is a principal-bracket diagnostic,
not a claimed full nonlinear Dirac closure.

## Foliation price

The action needs `n_mu`.

- A fixed normal gives a computed boosted elliptic coefficient `-1` in the
  alpha-2-like channel.
- A clock normal gives, already on FLRW, a velocity Hessian in `(a,lambda)`
  with determinant `-36 a^4`.  The exact finite-`k` Dirac calculation above is
  the stronger result: the putative auxiliary carries a propagating scalar.

The acceleration relation `a0=c^2 sqrt(Lambda/(32 pi))` is an external input
to this action; it is not derived.

No complete PPN extraction is promoted after the action has already failed
both no slip and the two-tensor-only condition.  The acceleration relation
`a0=c^2 sqrt(Lambda/(32 pi))` remains external input.

**Candidate B verdict: DEAD.  The broader existential target remains OPEN.**
