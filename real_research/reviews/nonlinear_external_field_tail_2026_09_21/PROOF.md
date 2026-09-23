# Derivation and exact claim boundary

## 1. Claim card

Let a compact baryonic source of positive total mass \(M_b\) satisfy the static
AQUAL equation with an asymptotically uniform potential gradient \(g_e\hat z\),
\(g_e>0\). Assume \(\mu\) is \(C^3\) near \(g_e\), \(\mu_e>0\), and
\(\Gamma=1+g_e\mu'_e/\mu_e>0\). Subtract the affine background and choose the
additive constant so the internal potential decays at infinity.

**Asymptotic hypothesis:** in stretched coordinates, the solution has an
expansion through homogeneous radial degree -3, with a remainder
\(o_2(s^{-3})\): its derivatives of orders j=0,1,2 are uniformly
\(o(s^{-3-j})\). Angular coefficients are smooth. The exterior leading term
is the decaying monopole, followed by the usual multipole orders. This is an
explicit hypothesis about the solution, not a consequence claimed from a finite
residual test. A global existence theorem and a proof of this hypothesis for all
allowed sources are outside this package.

Then the odd axial degree -3 coefficient is
\(B=L\mathcal K^2/g_e\), where \(\mathcal K=GM_b/\mu_e\) and
\(L=g_e\mu'_e/\mu_e\). The statistic in README therefore converges to L.
No baryonic reflection symmetry is needed for this conditional asymptotic claim.

For QUMOND assume the corresponding decaying physical solution, a compact
Newtonian source and a differentiable far-field expansion of its physical
potential. Take \(\nu\in C^3\) near the positive Newtonian background \(n_e\),
\(\nu_e>0\), and \(g_e=\nu_e n_e\). Then
\(B=-k_\nu\mathcal K^2/g_e\), \(\mathcal K=GM_b\nu_e\).

The additional orbital conclusion assumes an isolated spherical exterior with
constant enclosed baryonic mass, ordinary circular test-body kinematics, and
the same universal response at the same physical acceleration. Identifying the
two theories' isolated curves requires \(1+k_\nu>0\), which follows from the
positive AQUAL ellipticity when the duality is used.

## 2. Quadratic constitutive expansion

Use potential gradients, not gravitational acceleration vectors. For
\(F_i(v)=\mu(|v|)v_i\), write \(v=g_e\hat z+u\). Put
\(M=g_e^2\mu''_e/\mu_e\). At the background,

\[
J_{ij}=\mu_e(\delta_{ij}+L e_i e_j),
\]
\[
H_{ijk}=\frac{\mu_e}{g_e}
 \left[L(e_k\delta_{ij}+e_j\delta_{ik}+e_i\delta_{jk})
       +(M-L)e_i e_j e_k\right].
\]

Thus the quadratic flux \(B_i=H_{ijk}u_j u_k/2\) is

\[
B_i=\frac{\mu_e}{g_e}
 \left[L u_z u_i+\frac L2|u|^2 e_i+\frac{M-L}{2}u_z^2e_i\right].
\]

Outside the baryons the order-two equation is
\(\mu_e(\partial_x^2+\partial_y^2+\Gamma\partial_z^2)\phi_2
=-\nabla\cdot B(\nabla\phi_1)\).
All 27 Hessian components and this PDE identity are checked by differentiating
the original flux in `verify.py`.

## 3. Invert the exterior operator

Let \(\zeta=z/\sqrt\Gamma\), \(s^2=R^2+\zeta^2\), \(t=\zeta/s\),
\(R^2=x^2+y^2\), and \(C=GM_b/(\mu_e\sqrt\Gamma)\).
The leading potential \(\phi_1=-C/s\) has
\(u_R=CR/s^3\), \(u_z=C\zeta/(\sqrt\Gamma s^3)\).
Writing \(A=(L+M/2)/\Gamma\), direct differentiation gives

\[
\frac{\nabla\cdot B}{\mu_e}
=\frac{C^2}{g_e\sqrt\Gamma\,s^5}
 \left[(-7L+2A)t+(9L-6A)t^3\right].
\]

The normalization of C follows either from the known anisotropic Green function
or by integrating the linear flux in stretched coordinates. The coordinate
Jacobian is \(\sqrt\Gamma\), giving physical flux
\(4\pi\mu_e\sqrt\Gamma C=4\pi GM_b\). The nonlinear flux correction is
\(O(s^{-4})\); its flux integral tends to zero at infinity.

Use \(P_1=t\), \(P_3=(5t^3-3t)/2\). The forcing bracket becomes
\(-8(L+A)P_1/5+(18L-12A)P_3/5\). Since

\[
\Delta_s[s^{-3}P_\ell(t)]=(6-\ell(\ell+1))s^{-5}P_\ell(t),
\]

the decaying particular solution is

\[
\phi_2=\frac{C^2}{g_e\sqrt\Gamma\,s^3}
 \left[\frac{2(L+A)}5P_1+\frac{3L-2A}5P_3\right]
=\frac{C^2}{g_e\sqrt\Gamma\,s^3}
 \left[(A-L/2)t+(3L/2-A)t^3\right].
\]

The angular eigenvalues are 4 and -6; neither channel is resonant. At radial
degree -3, the homogeneous freedom is \(\ell=2\), which is **even** under
spatial inversion. It cannot alter the odd axial coefficient.

The previous degree -2 equation has only a homogeneous \(\ell=1\) dipole.
Its gradient is \(O(s^{-3})\), so its quadratic interaction with the monopole
first enters the field equation at \(O(s^{-6})\), one order later than the
forcing above. Higher source multipoles likewise cannot change this coefficient.

On the axis, \(s=r/\sqrt\Gamma\), \(t=\pm1\), and the angular sum is L.
The coefficient is therefore

\[
\phi_{2,\mathrm{axis}}(\pm r)=\pm\frac{L(GM_b/\mu_e)^2}{g_e r^3}.
\]

This establishes the coefficient under the asymptotic hypothesis. A fixed
translation of the source origin changes the degree -2 dipole and the even
degree -3 multipoles, but leaves this odd degree -3 coefficient unchanged.

## 4. Matching-dependent dipoles are real

Consider a perturbative family with baryonic density multiplied by a small
parameter. Choose its first-order potential radial in stretched coordinates,
\(\phi_1'(s)=q(s)=Cm(s)/s^2\), where \(m(0)=0\), \(m(s)=1\) outside a
compact source of radius a, \(m'\ge0\), and \(q=O(s)\) at the origin.
These are ellipsoidal sources in physical coordinates. The quadratic problem
is globally regular and has a decaying Green solution.

For arbitrary q the divergence bracket has coefficients

\[
a(s)=3Lqq'+(2A-L)q^2/s,\qquad
b(s)=(2A-3L)(qq'-q^2/s),
\]
\[
f_1=-\frac{a+3b/5}{g_e\sqrt\Gamma},\qquad
f_3=-\frac{2b/5}{g_e\sqrt\Gamma}.
\]

The radial inverse of \(\Delta\psi_\ell=f_\ell(s)P_\ell\) is

\[
\psi_\ell(s)=-\frac1{2\ell+1}
 \left[s^{-\ell-1}\int_0^s u^{\ell+2}f_\ell(u)\,du
       +s^\ell\int_s^\infty u^{1-\ell}f_\ell(u)\,du\right].
\]

For \(\ell=1\), the homogeneous coefficient \(D_1\) of \(P_1/s^2\) is

\[
D_1=-\frac13\int_0^\infty s^3f_1(s)\,ds
   =-\frac{L+A}{3g_e\sqrt\Gamma}\int_0^\infty s^2q(s)^2\,ds.
\]

The last equality follows by integration by parts, with boundary term
\(s^3q^2\) vanishing at both endpoints. The physical axial dipole is
\(d=\Gamma D_1\). It is nonzero, and negative when \(L+A>0\), even though
the baryonic source is inversion symmetric. Its size depends on the source
profile. The point-source limit of this weak-source construction is not uniform;
it cannot be used to extend external dominance through a singular source core.

Outside a, the exact second-order solution consists of this dipole, the forced
degree -3 term above, and a homogeneous \(P_3/s^4\) term. Hence the
three-radius filter removes both source-dependent coefficients **exactly at
second order** for this family. The 36 integrated cases test this statement.
They do not bound the third and higher orders at a finite source amplitude.

## 5. Why QUMOND differs

Its field equation is

\[
\Delta\Phi=\nabla\cdot[\nu(|\nabla\Phi_N|)\nabla\Phi_N],\qquad
\Delta\Phi_N=4\pi G\rho_b,
\]

with Newtonian background \(n_e\hat z\). Let
\(k_\nu=n_e\nu'_e/\nu_e\), \(m_\nu=n_e^2\nu''_e/\nu_e\),
\(A_N=k_\nu+m_\nu/2\). Here use ordinary spherical radius r and cosine t.
The leading physical potential is the known solution

\[
\phi_{Q,1}=-\frac{GM_b\nu_e}{r}
 \left[1+\frac{k_\nu}{2}(1-t^2)\right].
\]

The quadratic flux is now evaluated on the **Newtonian** monopole
\(u_N=GM_b\hat r/r^2\). The equation for the physical correction has
\(+\nabla\cdot B_\nu\) on its right, whereas AQUAL's inversion has a minus.
There is no coordinate stretch. Consequently

\[
\phi_{Q,2}=-\frac{\nu_e(GM_b)^2}{n_e r^3}
 \left[(A_N-k_\nu/2)t+(3k_\nu/2-A_N)t^3\right].
\]

The axial sum is \(-k_\nu\). Using \(g_e=\nu_e n_e\) and
\(\mathcal K=GM_b\nu_e\) gives \(B_Q=-k_\nu\mathcal K^2/g_e\).

For a general compact Newtonian source, its j-th multipole has potential degree
\(-j-1\) and parity \((-1)^j\). The linear QUMOND operator preserves this
parity and radial order. A baryonic dipole can thus contribute odd degree -2,
and a baryonic quadrupole even degree -3. Neither changes the forced odd
degree -3 term from the squared monopole. The radial filter applies as above.

## 6. Radial extraction and orbital elimination

Write the axial odd potential as
\(d/r^2+B/r^3+o_1(r^{-3})\). With the signs in README,
\(D(r)=-d\phi_{\mathrm{odd,axis}}/dr\). Therefore

\[
D(r)-8D(2r)=\frac{3B}{2r^4}+o(r^{-4}).
\]

The constant 8 is fixed by the unwanted force power -3; the normalization 2/3
is fixed by the remaining force power -4. A further odd potential term
\(o/r^4\) contributes \(3o/r^5\) to this two-radius difference. The
combination \(D(r)-40D(2r)+256D(4r)\) is instead
\(-3B/(2r^4)\), when only these three odd powers are retained.

Finally, differentiate \(r^2g\mu(g)=GM_b\) and use \(v_c^2=rg\):
\((1+L)(1-2\beta)=2\). It follows that
\(L=(1+2\beta)/(1-2\beta)\). Spherical duality is
\(n=g\mu(g)\), \(\nu(n)=1/\mu(g)\); logarithmic differentiation gives
\(k_\nu=-L/(1+L)\). Thus

\[
\mathcal N_A=\frac{1+2\beta}{1-2\beta},\qquad
\mathcal N_Q=\frac{1+2\beta}{2}.
\]

All accelerations in this comparison are matched physically. No separate
per-object choice of a0, kappa or response normalization is used to match them.
