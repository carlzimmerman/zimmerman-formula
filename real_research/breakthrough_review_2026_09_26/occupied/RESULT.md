# Occupied FRW: the kinetic stability equation

The actual expanding homogeneous carrier background has a positive reduced velocity Hessian and an invertible nonzero-mode auxiliary constraint block for both CA4-GNC-PQ and CA5-GNC-R. Occupation contributes a **positive** infrared kinetic term. This goes beyond the earlier empty de Sitter result. It does not prove finite-wavelength occupied gradient stability or nonlinear global evolution.

## Scope and action

Keep the complete centered-clock, projected-auxiliary, compensated-gate host. On a flat compact FRW leaf take \(U=Z=0\), an inactive gate, no ordinary matter, and homogeneous carrier fields \(\bar\varphi_A(t)\). Define

\[
\mathcal M=M_P^2>0,\quad v_A=\dot{\bar\varphi}_A,\quad
T=\tfrac12|\boldsymbol v|^2,\quad V=V_{\rm mix}\ge0.
\]

The calculation treats a general vacuum shape:

\[
\mathcal L_d=t_cK_d-W_{\rm exc}/t_c-V_0F(t_c),\qquad
t_c=1+P_hZ,\quad F(1)=1,\quad
f_1=F'(1),\quad f_2=F''(1).
\]

Here \(V_0>0\) and the bare Einstein constant is zero. The genuine background equations are

\[
3\mathcal M H^2=T+V+V_0,\qquad
\mathcal M\dot H=-T,\qquad
\dot v_A+3Hv_A+V_A=0.
\]

Neither \(H\) nor the occupied fields are frozen in the action derivation. The final ultraviolet limit freezes their finite local jets, as appropriate for a principal-symbol statement.

PQ has \(F(t_c)=1/t_c+\zeta(t_c-1)^2\), with
\(f_1=-1,\ f_2=2/r_0,\ \zeta=1/r_0-1\).
CA5-GNC-R has \(F(t_c)=1+(t_c+1/t_c-2)^2\), hence \(f_1=f_2=0\).
These are separate actions. The earlier suggested quartic-over-\(t_c\) barrier also has zero first two jets, but is not the final reciprocal candidate.

## Actual background and projector cancellations

Use \(h_{ij}=a^2e^{-2\psi}\delta_{ij}\), \(N=e^\phi\), \(N^i=a^{-2}\partial_i\beta\), and carrier perturbations \(\chi_A\). Set

\[
x=q^2=k^2/a^2>0,\quad r=r_0e^{-\xi^2x/2},\quad
r_0=\ell/4,\quad Q=1-r,\quad c_N=1-\alpha/2,
\]
\[
K=\frac{2(2+3c_2)}{c_2},\qquad
\alpha_e=2-(2-\alpha)Q^2.
\]

The first background-sensitive check expands ADM at nonconstant \(H\). After spatial and time integration by parts, its extra quadratic coefficients beyond the usual shift block are

\[
\frac{\mathcal M}{2}
[3H^2\phi^2-18H^2\phi\psi+(27H^2+18\dot H)\psi^2].
\]

The carrier background contributes
\((T-V-V_0)\phi^2/2+3(T+V+V_0)\phi\psi+
9(T-V-V_0)\psi^2/2\).
The displayed background equations cancel the \(\phi\psi,\psi^2\) terms and leave exactly \(T\phi^2\).

The spatial mean is varied. Because \(\int\sqrt h\,P_hZ=0\), second-order projector terms cancel every apparent background \(\psi Z\) term. The remaining carrier/vacuum vertices include

\[
\boldsymbol v\cdot\dot{\boldsymbol\chi}(Z-\phi-3\psi)
+(V-T-V_0f_1)\phi Z-(V+V_0f_2/2)Z^2.
\]

Integrating the \(-3\psi\,\boldsymbol v\cdot\dot{\boldsymbol\chi}\) term uses the homogeneous carrier equation and cancels its corresponding potential-volume vertex. The exact two-cell expansion in the code independently retains and checks the projector's second variation.

## Full quadratic action after constraints

The \(U\) equation remains \(Z=r\phi\) for nonzero modes; constant background heat fields make the otherwise necessary heat-metric vertices vanish at this quadratic order. The shift solution is

\[
x\beta=(3+2/c_2)(\dot\psi+H\phi)
-\frac{\boldsymbol v\cdot\boldsymbol\chi}{\mathcal M c_2}.
\]

Define

\[
\Delta=\alpha_e x+\frac2{\mathcal M}
\left[T+(V-T-V_0f_1)r-(V+V_0f_2/2)r^2\right],
\quad F_d=KH^2+\Delta,
\]
\[
\mathcal J=\mathcal M KH\dot\psi-Q\boldsymbol v\cdot\dot{\boldsymbol\chi}
-2\mathcal M x\psi-H(3+2/c_2)\boldsymbol v\cdot\boldsymbol\chi
-Q\boldsymbol V'\cdot\boldsymbol\chi .
\]

The lapse is \(\phi=-\mathcal J/(\mathcal M F_d)\). The full scalar quadratic density divided by \(a^3\) is

\[
\begin{split}
L_{\rm red}/a^3={}&
\tfrac12\mathcal M K\dot\psi^2+\tfrac12|\dot{\boldsymbol\chi}|^2
-\frac2{c_2}\dot\psi\,\boldsymbol v\cdot\boldsymbol\chi
+\frac{(\boldsymbol v\cdot\boldsymbol\chi)^2}{2\mathcal M c_2}\\
&-\tfrac12\boldsymbol\chi^T(xI+V'')\boldsymbol\chi
+\mathcal M x\psi^2-\frac{\mathcal J^2}{2\mathcal M F_d}.
\end{split}
\]

This formula retains the occupied constraint vertices and the potential Hessian. A claim about its finite-\(q\) restoring matrix would require further treatment of its evolving mixed terms. Such a claim is not made here.

## The decisive relation

For velocities \((\dot\psi,\dot{\boldsymbol\chi})\), let
\(G_0=\operatorname{diag}(\mathcal M K,I)\) and
\(u=(\mathcal M KH,-Q\boldsymbol v)\). The exact velocity Hessian is

\[
G=G_0-\frac{uu^T}{\mathcal M F_d}.
\]

Its controlling coefficient is

\[
\boxed{\mathcal D
=\Delta-\frac{2TQ^2}{\mathcal M}
=\alpha_e q^2+\frac{2r}{\mathcal M}
\left[(1-r)(T+V)-V_0(f_1+f_2r/2)\right].}
\]

Also \(F_d=KH^2+\mathcal D+2TQ^2/\mathcal M\). On the positive-\(F_d\) branch, the normalized matrix \(G_0^{-1/2}GG_0^{-1/2}\) has one eigenvalue \(\mathcal D/F_d\) and all its other eigenvalues equal to one. Thus

\[
G\succeq\frac{\mathcal D}{F_d}G_0>0
\qquad\text{whenever }\mathcal D>0.
\]

Every carrier direction perpendicular to \(\boldsymbol v\) retains its canonical unit velocity coefficient. In the host/parallel two-dimensional block,
\(\det G_\parallel=\mathcal M K\mathcal D/F_d\).

For PQ, the exact decomposition is

\[
\mathcal D_{\rm PQ}
=\alpha_e x+\frac2{\mathcal M}
[rQ(T+V)+V_0r(1-r/r_0)]>0.
\]

For CA5-GNC-R, it is simpler:

\[
\boxed{\mathcal D_R
=\alpha_e q^2+\frac{2r(1-r)}{\mathcal M}\rho_{\rm exc}>0,\qquad
\rho_{\rm exc}=T+V\ge0.}
\]

These signs hold for \(0<\alpha<2,\ c_2>0,\ 0<\ell<4,\ \xi>0,\ q>0\), without a bound on occupied energy or a filter-to-Hubble ratio. They use the actual positive-square potential's \(V\ge0\). If \(\rho_{\rm exc}>0\), both candidates have the infrared limit

\[
\mathcal D(0)=\frac{2r_0(1-r_0)}{\mathcal M}\rho_{\rm exc}>0.
\]

This is a positive instantaneous occupied-state kinetic floor. It is not uniform as occupation tends to zero or \(\ell\) tends to zero, and it does not justify inverting the exactly homogeneous constraint.

An independent four-variable Hessian check gives the full \((\beta,U,Z,\phi)\) constraint determinant

\[
\det C=4\mathcal M^4c_2c_N^2x^4F_d>0.
\]

Thus a pole inferred from one fixed-velocity auxiliary subblock would be spurious in this occupied background. The complete nonzero-mode block is invertible in the stated domain.

## Ultraviolet and the remaining gradient question

For fixed finite background jets, \(r\) decays faster than any inverse power of \(q\). Keeping all second-order principal terms of the actual reduced action gives

\[
L_{\rm UV}/a^3=
\tfrac12\mathcal M K\dot\psi^2
-\mathcal M\frac{2-\alpha}{\alpha}q^2\psi^2
+\tfrac12|\dot{\boldsymbol\chi}|^2-\tfrac12q^2|\boldsymbol\chi|^2.
\]

Hence the host speed squared is
\(c_2(2-\alpha)/[(2+3c_2)\alpha]>0\), and all carrier principal speeds squared are one on this homogeneous \(t_c=1\) branch. Background occupation changes lower-order mixing, not these ultraviolet speeds. This is not a metric-cone claim for the host.

Finite-wavelength occupied restoring signs and growth, excited-background potential instabilities, uniform mode-sum estimates, full homogeneous constraint counting, and nonlinear inhomogeneous continuation remain open. Positive velocity Hessian plus positive ultraviolet speeds do not settle those questions.

## Verification and independent vacuum audit

The bounded exact run passes **25 checks**: non-de-Sitter ADM terms, full projected matter jets, on-shell cancellations, shift/U/lapse elimination, the full reduced scalar action, complete constraint determinant, parallel/transverse kinetic structure, occupied infrared decompositions, and ultraviolet principal action. The run manifest validates. No numerical parameter scan or nonlinear simulation was used.

OccupiedBridge20260926.lean compiles **six declarations**, proving the occupation identity, parallel determinant, PQ and reciprocal positivity decompositions, infrared floor, and constraint determinant sign under explicit hypotheses. Its accepted output contains only propext, Classical.choice, and Quot.sound. It does not formalize the ADM or PDE derivation.

Independent review of the final reciprocal vacuum action's R5–R7 finds them consistent with this calculation: setting \(T=V=0\) gives \(D_F=\alpha_e x-6H^2r(f_1+f_2r/2)\); its infrared cancellation condition is \(f_1+r_0f_2/2=0\). Reciprocal \(F\) satisfies it with both jets zero. Then \(d=\alpha_e\), \(2xd_x\ge-4r_0\), and \(2+d+2xd_x\ge1\) for \(\ell\le1\), establishing that report's vacuum all-\(q\) sign window without a Hubble/filter restriction. This remains the empty de Sitter gradient theorem; it is not silently extended to occupied finite-\(q\) gradients.
