# Independent transverse-vector gate for the proposed alpha=1 operator

Status: analytic derivation of a constrained quadratic sector of the displayed action. No model evolution, source edit, numerical experiment, scalar-sector completion, or whole-theory verdict is supplied. Source action: CFG938 revision `92606e049be780aa6ac7d57de60d97e2324c74b3`; the alpha-family is the later proposal pinned in the accompanying receipt. Work in c=1, signature (-+++), K=4 pi G>0 and gamma>0.

The principal conclusion is conditional but stronger than the earlier frozen-metric sub-block. With the shift retained and eliminated, the medium-plus-Einstein transverse kinetic coefficient is

\[
 I_V(q)=\frac{A(q)G(q)}{A(q)+G(q)},\qquad
 A(q)=A_0-\frac{3\gamma C^2}{4K^2}q^2,\qquad G(q)=\frac{q^2}{4K}.
\]

There is an exact homogeneous lambda=0 branch on which A0>0 for the source's positive dust/radiation Friedmann background. On that branch the alpha=1 proposal has a negative reduced kinetic interval above the first zero of A, if that interval belongs to the EFT's valid wavenumber range and the unrestricted transverse label velocities are retained. At its zero and at a shift-rank loss, ordinary-mode language is invalid. A negative kinetic coefficient is not, by itself, a computed exponential transverse growth rate.

## 1. Definitions and fields that are retained

Write the action's relevant terms as

\[
 \mathcal L=\frac{R}{4K}-mn-W_{\rm full}(U)
 -\frac{3\gamma}{4K^2}\widetilde\tau_{\mu\nu}\widetilde\tau^{\mu\nu}
 +\lambda\bigl(h^{\mu\nu}\nabla_\mu\nabla_\nu\chi-Kmn\bigr),
\]

where h=g+uu, U^2=h^{mu nu} partial_mu chi partial_nu chi, C=u^mu partial_mu chi, and

\[
 \widetilde\tau_{\mu\nu}=\tau_{\mu\nu}+C\sigma_{\mu\nu}.
\]

Here tau is the source's trace-free projected **four-Hessian**, not a replacement spatial Hessian. The velocity shear convention is sigma_ij=partial_(i v_j)-delta_ij div(v)/3 in a local rest frame, with symmetrization carrying 1/2. W_full(U)=U^2/(2K)+O(U^3).

Choose spatial-flat vector gauge, but retain the transverse ADM shift:

\[
 ds^2=-dt^2+a^2\delta_{ij}(dx^i+S^i dt)(dx^j+S^j dt),\quad
 \partial_iS^i=0,\quad \phi^I=x^I-\xi_T^I,\quad\partial_i\xi_T^i=0.
\]

The quadratic lapse-fixed metric includes g00=-1+a^2 S^2. Omitting this quadratic piece gives incorrect velocity coefficients. Define physical Fourier variables

\[
 B=aS,\qquad v=a\dot\xi_T,\qquad V=v+B,\qquad q=k/a,
 \qquad\rho=m\bar n=m/a^3.
\]

V is the medium velocity relative to the normal of the ADM slices. At the order needed, u^0=1+V^2/2 and u_i=a V_i. Scalar delta chi and delta lambda cannot mix linearly with a transverse vector on an isotropic background. Their second-order corrections multiply background equations in the on-shell quadratic action; they do not authorize dropping the background multiplier. No static Poisson substitution is used.

Volume-preserving relabelings remove time-independent transverse changes of labels. Time-dependent xi_T changes the conserved current and vorticity. These zero-restoring-force fluid velocities are not removed by calling a transverse part of P a relabeling potential. A deliberately spherical/longitudinal restriction is a smaller field theory than the displayed unrestricted three-label covariant fluid action.

## 2. Tidal and Einstein terms, including the shift

Let A_mu=D_mu chi=partial_mu chi+C u_mu. The exact projected symmetric trace-free identity is

\[
 [h_\mu{}^\alpha h_\nu{}^\beta\nabla_{(\alpha}A_{\beta)}]_{\rm TF}
 =\tau_{\mu\nu}+C\sigma_{\mu\nu}.
\]

A_mu vanishes on the homogeneous background, while delta A_i=a C V_i. Therefore in an orthonormal spatial frame

\[
 \delta\widetilde\tau_{\hat i\hat j}=C\partial^{\rm phys}_{(i}V_{j)},
 \qquad |\delta\widetilde\tau|^2=\frac{C^2q^2}{2}|V|^2.
\]

An equivalent coordinate check keeps both separate pieces: delta tau_ij=a^2 C partial_(i S_j), delta sigma_ij=a^2 partial_(i dot xi_j), so their sum depends on dot xi+S. It is not a pure fluid velocity term with the shift frozen.

Thus

\[
 \mathcal L_{\rm tidal,V}^{(2)}/a^3=-\frac{3\gamma C^2q^2}{8K^2}|V|^2.
\]

ADM gives K_ij=a^2[H delta_ij-partial_(i S_j)] and K_i^i=3H. The Einstein-Hilbert term, after its usual time boundary term, supplies

\[
 \mathcal L_{\rm EH,V}^{(2)}/a^3=+\frac{q^2}{8K}|B|^2.
\]

There is no dot B. The transverse metric shift is an auxiliary constraint, not a propagating additional vector.

## 3. Low-derivative coefficient and homogeneous multiplier

The dust contribution is rho V^2/2. Indeed sqrt(-g)n=J0/Gamma, where J0 is the spatial label Jacobian and Gamma=1+V^2/2. For transverse xi and homogeneous coefficients the quadratic Jacobian term integrates to a spatial boundary; the fluid has no shear restoring potential. The -K lambda mn term contributes K lambda rho V^2/2.

The projected gradient has U^2=C^2 V^2+O(3), giving -C^2 V^2/(2K). The background lambda Hessian term must also be kept. With homogeneous chi(t), C=dot chi and lapse one,

\[
 \Box\chi=-\dot C-3HC,\qquad
 u^\mu u^\nu\nabla_\mu\nabla_\nu\chi
 =\dot C+(\dot C-HC)V^2+O(3).
\]

For example, the covariant Hessian decomposes as dot C n_mu n_nu-C K_mu nu, where n_mu is the slice normal and the lapse acceleration vanishes. Consequently

\[
 D^2\chi=-3HC+(\dot C-HC)V^2+O(3).
\]

The multiplier adds lambda(dot C-HC)V^2. Combining all terms yields

\[
 A_0=\rho(1+K\bar\lambda)-\frac{C^2}{K}
       +2\bar\lambda(\dot C-HC),
\]

and the principal quadratic vector action per transverse polarization is

\[
 S_V^{(2)}=\frac12\int dt\,d^3k\,a^3
  \{A(q)|v+B|^2+G(q)|B|^2\}.
\]

On a general background, a,H,rho,C,dot C,lambda and gamma must be specified by the actual background solution. In particular it is not consistent to omit lambda from A0 merely because scalar multiplier *perturbations* are absent from the vector representation. The original source has not selected all homogeneous multiplier integration constants or solved the altered-background family. The source dust/radiation Friedmann relation cannot simply be substituted on an arbitrary nonzero-lambda branch.

## 4. Exact homogeneous lambda=0 branch

On the homogeneous configuration, U=tau=sigma=0. Before enforcing the constraint, the chi/lambda/dust part of the action per coordinate volume is

\[
 L_{\rm bg}=-m(1+K\lambda)-3a^3H\lambda\dot\chi.
\]

Varying chi (not imposing the lambda equation first) gives

\[
 \frac{d}{dt}(a^3H\lambda)=0.
\]

Thus lambda=ell/(a^3 H) for H nonzero, and ell=0 selects lambda=0 as an exact consistent homogeneous branch. Variation of lambda still imposes

\[
 -3HC=K\rho.
\]

On lambda=0, the W and tidal sectors and their first homogeneous variations vanish, the multiplier stress vanishes, and ordinary comoving dust is consistent. If the remaining matter satisfies the source's positive dust/radiation Friedmann background,

\[
 H^2=\frac{2K}{3}\rho_{\rm tot},\qquad0<\rho\le\rho_{\rm tot},
\]

then

\[
 \frac{C^2}{K}=\frac{\rho^2}{6\rho_{\rm tot}},\qquad
 A_0=\rho\left(1-\frac{\rho}{6\rho_{\rm tot}}\right)
 \ge\frac56\rho>0.
\]

This establishes the positivity hypothesis on an actual branch rather than assuming it. It does not claim lambda=0 is the unique branch or insert ordinary Friedmann equations when lambda stress is present.

## 5. Eliminate the metric shift before testing signs

For q>0 and A+G nonzero, the exact transverse constraint and reduced action are

\[
 (A+G)B=-Av,\qquad B=-\frac{A}{A+G}v,\qquad
 V=\frac{G}{A+G}v,
\]

\[
 \mathcal L_{V,\rm red}^{(2)}=\frac{a^3}{2}I_V(q)|v|^2
 =\frac{a^5}{2}I_V(q)|\dot\xi_T|^2,\qquad
 I_V=\frac{AG}{A+G}.
\]

Time-dependent a and A may give Hubble-type terms in the equation of motion; they do not change the instantaneous principal kinetic sign. The absence of a transverse shear potential means this calculation is not a computation of an exponential instability frequency. Negative I_V is a negative constrained quadratic kinetic direction.

On the A0>0 branch, define

\[
 x=\frac{q^2}{4K A_0}>0,\qquad
 z=\frac{3\gamma C^2}{K}>0,\qquad
 \frac{I_V}{A_0}=\frac{x(1-zx)}{1+(1-z)x}.
\]

The first zero is x_A=1/z, or q_A^2=4K A0/z. Sign intervals are:

| background z | positive kinetic interval | negative kinetic interval | special second locus |
|---|---|---|---|
| 0<z<1 | 0<x<x_A | x>x_A | denominator stays positive |
| z=1 | 0<x<1 | x>1 | denominator equals 1 |
| z>1 | 0<x<x_A and x>x_D | x_A<x<x_D | x_D=1/(z-1)>x_A is shift-rank loss |

At A=0, the shift equation sets B=0 but the fluid velocity has zero quadratic kinetic coefficient. This is a degeneracy requiring a separate constraint/nonlinear analysis, not an ordinary healthy propagating mode. At A+G=0, A=-G is nonzero for q>0; the shift equation instead imposes v=0. The elimination formula is invalid there. Its pole is not an infinite-frequency solution. For z>1, the eventual positive formal high-q coefficient does not remove the intervening negative band or rank-changing locus. q=0 is the homogeneous vector/gauge limit and is excluded from the division by G. If C=0 or gamma=0, the adverse q^2 term is absent and the familiar positive medium-plus-Einstein reduction is recovered for A0>0.

## 6. Other background matter: explicit scope of the simple pole

The source leaves S_b's perturbation field content unspecified. The exact formula and pole above describe the medium-plus-Einstein transverse block, including any background components that have no independent vector contribution. Additional dynamical perfect-fluid vector velocities must be retained if present; their positive enthalpy coefficients cannot silently be set to zero.

For positive coefficients A_b, write all physical velocities v_i and a common shift B. The full principal kinetic form before reduction is

\[
 \frac12\left[\sum_i A_i|v_i+B|^2+G|B|^2\right],\quad
 A_1=A(q),\qquad A_b>0.
\]

The reduced matrix is

\[
 (K_V)_{ij}=A_i\delta_{ij}-\frac{A_iA_j}{G+\sum_i A_i}.
\]

The full shift-rank locus is G+sum_i A_i=0, not necessarily A+G=0. Nevertheless, immediately above A=0 its denominator is positive (G+sum_b A_b>0), while the unreduced complete-square form has one negative direction. By Schur-complement inertia, that negative direction remains after eliminating the positive shift block. Thus positive spectator fluid vectors do not remove the onset of a negative-kinetic interval; they can move its far endpoint and pole. If P=sum_b A_b is q independent, the pole for z>1 moves to q_D^2=4K(A0+P)/(z-1). This extension is conditional on those spectator models and kinetic signs, not a solution of unspecified S_b.

## 7. What this rules out, and the next gate

The alpha=1 operator's homogeneous tensor cancellation remains a valid identity; this vector obstruction does not reverse it. It shows why that identity is insufficient to certify the proposed action. On its consistent lambda=0 branch with the displayed unrestricted fluid content, the same operator produces a constrained negative vector kinetic interval if q_A and a nonempty interval above it lie inside the action's valid EFT range.

A defensible EFT evasion requires a physical cutoff strictly below q_A, or new degrees/operators that change the quadratic system before that scale. No such cutoff or ultraviolet repair is derived in the source or here. At fixed epoch, the sign conclusion is local in time and uses actual branch coefficients. It is not an all-background exclusion, a solution of the scalar sector, a finite-amplitude evolution, or a four-dwarf mass-budget test.

The cheapest decisive next work is to pin the intended homogeneous branch and valid physical wavenumber range, keep the source's full scalar constraints and any specified spectator vectors, and test the complete constrained quadratic action. If the declared range includes this adverse interval, retain the failed alpha=1 candidate rather than announcing a viable completion. If it excludes it, derive and justify that cutoff and then continue the remaining scalar/principal-symbol gate.

No changes to frozen criteria, source action, publications, or repository files were made for this note.
