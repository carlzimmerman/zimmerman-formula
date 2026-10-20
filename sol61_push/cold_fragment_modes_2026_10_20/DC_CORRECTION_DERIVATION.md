# Fixed-total-charge quadratic DC correction

**The proposed bordered equations have the correct signs and angular factors**, provided the quadratic cross term is evaluated on the **local** mode fields \(Z/r\), and the selected mode has the amplitude/phase quadrature required for an amplitude-only static solve. The harmonic coefficients are

\[
 C_0=\frac1{\sqrt{4\pi}},\qquad
 C_2=-\frac{\sqrt5}{7\sqrt\pi},\qquad
 C_4=\frac1{14\sqrt\pi}.
\]

This is an analytic derivation and executable specification, not an executed DC calculation. No numerical or symbolic mathematical code was run for this derivation. Source-file hashes were read for provenance. It does not compute the parent oscillation's nonlinear frequency shift.

## 1. Expansion and quadratic source

Keep the same canonical reduced ordering \((u,s,\xi,v,t_X)\), background \((f,b,h)\), positive-time convention, unit-normalized angular harmonics, and unit-\(K\) mode \(Z\) used by `natural_mode_source_v2.py`. Write

\[
 z_1=A\left[q(r)Y_{22}e^{i\Omega t}+q(r)^*Y_{22}^*e^{-i\Omega t}\right],
 \qquad q(r)=Z(r)/r.
\]

The background is an angular constant, not a normalized \(Y_{00}\) amplitude. The carrier frequency and real static correction are parameterized by

\[
 \omega_A=\omega+A^2\delta\omega+O(A^4),\qquad
 z_{\rm DC}=\frac{A^2}{r}\sum_{\ell=0,2,4}w_\ell(r)Y_{\ell0}+O(A^4).
\]

Here \(\delta\omega\) is the charge-constrained **carrier/background** shift. It is distinct from the nonlinear shift of the parent frequency \(\Omega\), which requires the next-order fundamental solvability condition.

Let \(N_2\) be the homogeneous quadratic force in the natural-source calculation. The static cross coefficient is

\[
 \mathcal C(q)=N_2(q+q^*)-N_2(q)-N_2(q^*).
\]

It is real and already contains both conjugate cross terms. There is **no extra factor two** to multiply it by. The DC source is
\(A^2\mathcal C(q)|Y_{22}|^2\). If the stored reduced vector \(Z\) is used directly instead, the equivalent reduced source is \(-C_\ell\mathcal C(Z)/r\), not \(-C_\ell r\mathcal C(Z)\), because \(N_2\) is quadratic in the perturbations. Its background-dependent coefficients remain local functions of \(r\).

For local \(q=(u,s,\xi,v,t_X)\), the amplitude components are

\[
\begin{aligned}
 \mathcal C_u={}&6\lambda F|u|^2+2\lambda F|v|^2
       +2\sqrt2g\Re(su^*+t_Xv^*)+2a\Re(\xi u^*),\\
 \mathcal C_s={}&\sqrt2g(|u|^2-|v|^2),\\
 \mathcal C_\xi={}&U'''(h)|\xi|^2+a(|u|^2+|v|^2),
 \qquad F=\sqrt2f.
\end{aligned}
\]

The phase components are

\[
\begin{aligned}
 \mathcal C_v={}&4\lambda F\Re(uv^*)
      +2\sqrt2g\Re(-sv^*+t_Xu^*)+2a\Re(\xi v^*),\\
 \mathcal C_{t_X}={}&2\sqrt2g\Re(uv^*).
\end{aligned}
\]

A single nondegenerate imaginary-frequency eigenmode of the real amplitude/phase block system can be chosen with \((u,s,\xi)\) real and \((v,t_X)\) purely imaginary. In that quadrature both phase cross terms vanish. The cached numerical mode should explicitly satisfy this condition to tolerance before restricting the DC solve to the amplitude block. A general complex superposition need not satisfy it: if a phase source remains, solve the appropriate static phase sectors as well and impose the U(1) gauge/solvability condition. Do not discard a nonzero source by convention.

## 2. Angular coefficients

Using \(x=\cos\theta\),

\[
 |Y_{22}|^2=\frac{15}{32\pi}(1-x^2)^2
  =\frac1{4\pi}-\frac5{14\pi}P_2(x)+\frac3{28\pi}P_4(x)
  =C_0Y_{00}+C_2Y_{20}+C_4Y_{40}.
\]

Since \(Y_{\ell0}=\sqrt{(2\ell+1)/(4\pi)}P_\ell\), this gives the three coefficients stated above. Complex conjugating the chiral \(Y_{22}\) convention leaves these DC coefficients unchanged. The polynomial vanishes at the poles and equals \(15/(32\pi)\) at the equator, providing simple hand checks.

## 3. Carrier-frequency derivative and charge derivative

Use the radial inner product
\(\langle x,y\rangle=\int x^Ty\,dr\), or \(\Delta r\,x^Ty\) on the existing grid. Let

\[
 p=\begin{pmatrix}\sqrt2rf\\2\sqrt2rb\end{pmatrix},\qquad
 a_{\rm amp}=(-Gp)_{\rm amp}
  =\begin{pmatrix}2\sqrt2\omega rf\\8\sqrt2\omega rb\\0\end{pmatrix},
 \qquad \sigma=\sqrt{4\pi}.
\]

In \(-Gp\), \(p\) is embedded in the two phase slots of the full five-component vector. The same symbol `a` in `radial_tools.py` denotes this charge-gradient vector; it must not be confused with the action's coupling \(a=200\).

The stationary carrier-frequency derivative is \(-a_{\rm amp}\delta\omega\) in angular-constant radial variables: differentiating \(-\omega^2\sqrt2f\) gives \(-2\omega\sqrt2f\delta\omega\), and differentiating \(-4\omega^2\sqrt2b\) gives \(-8\omega\sqrt2b\delta\omega\). Expanding that angular constant into normalized \(Y_{00}\) multiplies it by \(\sigma\). This explains the minus sign and \(\sqrt{4\pi}\) in the monopole field equation.

The unperturbed charge is

\[
 Q_0=4\pi\omega\langle p,p\rangle
    =8\pi\omega\int r^2(f^2+4b^2)\,dr.
\]

Its linear change from the DC monopole is \(\sigma\langle a_{\rm amp},w_0\rangle\), while its explicit change from the carrier frequency at fixed profiles is \(4\pi\langle p,p\rangle\delta\omega\). No \(\ell>0\) DC component contributes to the total charge at this order, since its angular integral vanishes.

The raw quadratic charge of the first-order mode, before its DC correction, is

\[
\begin{aligned}
 Q_2^{\rm raw}=\int dr\big[&2\omega(|Z_u|^2+|Z_v|^2)
       -4\Omega\Im(Z_u^*Z_v)\\
      &+8\omega(|Z_s|^2+|Z_{t_X}|^2)
       -8\Omega\Im(Z_s^*Z_{t_X})\big].
\end{aligned}
\]

There is no extra \(4\pi\) in this term because \(\int|Y_{22}|^2=1\). This is the same physical Noether charge reconstructed in the radiation review. It is not the charge radiated per unit lost mode energy.

## 4. Bordered fixed-total-charge equations

Let \(W_{{\rm amp},\ell}\) be exactly the read-only variational amplitude operator in the chosen angular sector, and define
\(S_\ell=-C_\ell r\mathcal C_{\rm amp}(Z/r)\). At order \(A^2\), the desired system is

\[
 \boxed{W_{{\rm amp},0}w_0-\sigma a_{\rm amp}\delta\omega=S_0},
\]

\[
 \boxed{\sigma\langle a_{\rm amp},w_0\rangle
          +\sigma^2\langle p,p\rangle\delta\omega
          +Q_2^{\rm raw}=0},
\]

\[
 W_{{\rm amp},2}w_2=S_2,\qquad W_{{\rm amp},4}w_4=S_4.
\]

These are the proposed signs and factors. The charge condition sets the **total** initial bound charge to \(Q_0+O(A^4)\); it does not require the raw first-order mode charge to vanish or the DC/background charge separately to remain fixed.

Eliminating the carrier shift gives an equivalent monopole equation:

\[
 \left(W_{{\rm amp},0}
       +\frac{a_{\rm amp}\langle a_{\rm amp},\cdot\rangle}{\langle p,p\rangle}\right)w_0
   =S_0-\frac{a_{\rm amp}Q_2^{\rm raw}}{\sigma\langle p,p\rangle},
\]

\[
 \delta\omega=-\frac{Q_2^{\rm raw}
            +\sigma\langle a_{\rm amp},w_0\rangle}
                       {\sigma^2\langle p,p\rangle}.
\]

The positive rank-one term is the same fixed-charge correction already used in the finite energy calculation. On the uniform grid its matrix is \(aa^T/(p^Tp)\), because the inner-product weights cancel in that term. They **do not cancel** from the inhomogeneous raw-charge term. In Euclidean array notation the monopole right-hand correction is \(-aQ_2^{\rm raw}/[\sigma\Delta r\,p^Tp]\).

## 5. Solvability and next executable controls

This derivation does not establish that the bordered system is nonsingular in the continuum. On a declared grid, check its charge-constrained amplitude operator and the \(\ell=2,4\) static operators for invertibility, solve residuals, and measure the resulting correction norm and \(\delta\omega\). Use the same background, quadrature, action parameters and radial boundary convention as the mode cache, with box/grid refinements. For a continuum exterior all DC channels are decaying; a finite Dirichlet truncation still requires convergence checks.

Before an amplitude-only solve, verify the parent mode's quadrature and the discarded phase-source norm. The \(\ell=0\) static phase operator has the U(1) null direction \(p\); fix its gauge explicitly if it is retained. The DC angular sectors contain no translation \(\ell=1\) source. Their \(m=0\) fields carry no new intrinsic angular momentum at this order.

Verify that total-charge cancellation scales as \(A^4\) after including the order-\(A^2\) corrections, rather than merely restating the bordered row. The carrier shift is not yet a bound on the nonlinear parent \(\Omega\) shift or a proof that finite-amplitude fundamental radiation stays closed. This DC gate supplies a charge-consistent initialization and average deformation; it does not complete the decay trajectory, merger excitation, galactic torque transfer, or dwarf mass budgets.

The derivation was self-proofread for canonical order, local-versus-reduced fields, both conjugate cross terms, harmonic signs, charge weights, and radial quadrature factors. Source hashes and the unexecuted status are recorded in `sources_dc_derivation.json`.
