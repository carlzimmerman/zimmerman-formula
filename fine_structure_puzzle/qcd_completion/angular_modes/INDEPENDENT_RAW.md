# Independent raw angular derivation, before coordinator angular notes

2026-10-19. Base: FSP-003 checkpoint, qcd_completion/CONTRACT.md, frozen determinant/phase reports. No coordinator angular derivation has been read.

Conventions D_i c = partial_i c + A_i cross c, A_i=(1-K)(e_i cross n)/r, Phi=h n, K=r/sinh r, h=coth r-1/r. The actual static Faddeev-Popov quadratic form is integral (|D_i c|^2+|Phi cross c|^2). This follows by differentiating background divergence for the gauge generator P c=(D_i c,Phi cross c); P^dagger P=-D_iD_i-(ad Phi)^2.

Let C=J(J+1), J>=1, and take orthonormal isospin-vector harmonics R=nY_JM, E=grad_S Y_JM/sqrt(C), M=n cross grad_S Y_JM/sqrt(C). They transform as grand spin J=L+T, T=1. Adjoint scalars are isospin vectors; no spatial fluctuation-vector index is present in this basis. Write c=(u_R R+u_E E+u_M M)/r, giving canonical reduced norm integral |u|^2 dr.

D_i c=partial_i c +(1-K)(n c_i-e_i(n dot c))/r. On the sphere D R contains K P_i Y+n grad_iY. D E contains its intrinsic tangent derivative and normal component -K n E_i. The same applies to M. Integrating on S2, |grad^S E|^2=|grad^S M|^2=C-1, div E=-sqrt(C)Y, div M=0, gives

U_RE = [[(C+2K^2)/r^2, -2 sqrt(C) K/r^2],[-2 sqrt(C) K/r^2, h^2+(C-1+K^2)/r^2]],
U_M=h^2+(C-1+K^2)/r^2.

No R-M or E-M mixing is present. At J=0 only R exists and U=2K^2/r^2, reproducing the frozen static ghost. At K=1,h=0 the RE leading centrifugal matrix has eigenvalues J(J-1),(J+1)(J+2), the M eigenvalue is J(J+1). Thus smooth origin branches have u~r^J e_-, r^(J+2) e_+, r^(J+1) e_M (l=J-1,J+1,J). The J1 l0 field has u~r, not an r^2 scalar copy. All branches are selected by smooth Cartesian fields at the origin, including the limit-circle l0 channel; the irregular constant reduced branch is excluded. Framed ghosts have all u(x)=0.

For J1 the magnetic scalar block is exactly the prior *Robin partner differential expression* L_A, but here with actual ghost Dirichlet wall data. Its regular solution is u_M=3(sinh r/r-r/sinh r), normalized u_M/r^2 ->1. The unbroken K=1,h=0 reference has u_ref=r^2 on the same Dirichlet domain. Hence its new relative ghost determinant is D_J1,M=3(sinh x/x-x/sinh x)/x^2. The degeneracy is 2J+1=3 complex ghost components. At large x, log D=x-3log x+log(3/2)+O(x^2 exp(-2x)); all algebraic inverse-radius terms vanish in this explicit comparison. It is not the earlier scalar Robin determinant; replacing its boundary functional by u'-h u changes the result.

The full static gauge Hessian is H_{mu nu}=-D_lambda D_lambda delta_{mu nu}-2 ad F_{mu nu} (signs of F/ad consistently fixed by the quadratic form), obtained from Yang-Mills plus background Feynman gauge. P^dagger P=M, HP=PM on the background field equations. Relative mixed vector data are a_tan=0, a4=0, and G=D_i a_i+[Phi,a4]=0 at the wall. For a Dirichlet ghost eigenfunction, Pc has tangential and a4 data zero, and G(Pc)=-lambda c=0. Thus longitudinal gauge modes pair exactly with actual Dirichlet ghosts at finite x. The positive-mode isometry Pc/sqrt(lambda) retains every positive small eigenvalue. This proves only the one-gradient subspace pairing, not a replacement of the full physical-vector determinant by scalar copies.

At J1 the full spatial-vector/isospin representation has seven radial channels: coupling S=1,T=1 to k=0,1,2 gives l=1 for k0; l=0,1,2 for k1; l=1,2,3 for k2. The a4 sector adds three channels l=0,1,2. Therefore the actual J1 vector block has ten radial channels per m, whereas the ghost has three. A scalar-copy assumption already fails at the origin channel count and at the wall domain.

## Further independent exact reduction

Still before coordinator angular notes. In order (E,R), define the frozen real-block W=[[h,sqrt2 K/r],[sqrt2 K/r,-1/r]], Q=d+W. Direct BPS substitution gives Q Q^dagger equal to the J1 RE potential in this order, while Q^dagger Q is the frozen real J0 block. This is used as a differential identity, not an identification of wall spectra.

The old real-block first-order kernel is y0=(rK', r(h+rh')/sqrt2), with y0~r²e2/sqrt3; e0=(sqrt2,1)/sqrt3, e2=(-1,sqrt2)/sqrt3. Put f=sinh(r)/r² and J=[[0,-1],[1,0]]. A normalized regular J1 l0 solution is z0=-sqrt3 f J y0~r e0, and Q^dagger z0=0. If z2~r³e2 is the other regular second-order solution, Q^dagger z2=-5sqrt3 y0; this follows from its r² coefficient and regularity of the real J0 first-order kernel. The scalar determinant d=det[z0,z2] satisfies (d/f)'=15|y0|² and d/f ->0 at the origin. Thus det Z=15 sinh(x)/x² integral_0^x |y0|² dt.

Direct differentiation reduces the integral exactly:
|y0|² = t²/2 + (1/2)d/dt[t³ csch²t (1-t coth t)],
integral = x³/6 [1+3 csch²x(1-x coth x)].

Therefore with the unbroken reference fundamental determinant x^4,
D_RE=5 sinh(x)/(2x³) [1+3 csch²x(1-x coth x)].
This coupled determinant is positive by its integral expression. It tends to 1 at small x and to 5 exp(x)/(4x³) times exponentially small corrections at large x. There is no algebraic inverse-radius term of any order. The magnetic determinant D_M has the same no-algebraic-correction property. Hence the entire J1 static ghost factor per magnetic quantum number is
D_RE D_M=15 sinh²x/(2x6) [1+3csch²x(1-x coth x)] [1-x²csch²x].
The full degeneracy is three; this is a complex-ghost determinant contribution, not a full gauge Gaussian.
