# Finite-fragment outgoing channels and the next radiation test

20 October 2026. Requested base: `e63b8b234`. **A finite-profile outgoing forced response is the cheapest useful radiation diagnostic. A scattering matrix alone gives conversion probabilities for an incident wave, not the fraction of merger energy radiated.** Neither calculation by itself closes the four-dwarf mass, orbital-energy, or angular-momentum budgets.

This derives a radial frequency-domain calculation for the explicit alternative three-field action in the earlier cold-completion packet. It performs no field evolution or original-source execution. `sources_outgoing.json` pins the action, stationary results, finite-profile source, this derivation, and the small symbolic checks. The new finite-profile experiment is being regenerated separately; no unfinalized result is assumed here.

## 1. Conventions and full radial operator

The action has complex fields of charges \(q_\Psi=1\), \(q_X=2\), a real neutral field, canonical complex kinetic terms, and a real kinetic term with coefficient one half:

\[
 V=|\Psi|^2+M_X^2|X|^2+g(X^*\Psi^2+X\Psi^{*2})
    +\lambda|\Psi|^4+a\chi|\Psi|^2+U(\chi),\qquad
 U(h)=\tfrac12M^2h^2-\tfrac18Mh^3+\tfrac14h^4.
\]

Use the real stationary profiles \(\Psi=f(r)e^{i\omega t}\), \(X=b(r)e^{2i\omega t}\), \(\chi=h(r)\). Parameters are \(M=100\), \(a=200\), \(g=0.002168\), \(M_X^2=4.0016\), \(\lambda=1.99+g^2/M_X^2\). Perturb by \(u+iv\), \(s+it_X\), and \(\xi\), and use canonical coordinates
\(z=(\sqrt2u,\sqrt2v,\sqrt2s,\sqrt2t_X,\xi)^T\).

For real \(\Omega>0\), choose

\[
 z(r,\theta,\phi,t)=Z(r)Y_{\ell m}(\theta,\phi)e^{i\Omega t}
             +Z(r)^*Y_{\ell m}^*e^{-i\Omega t},\qquad
 \int|Y_{\ell m}|^2d\Omega_{\rm angle}=1.
\]

Here the angular convention is \(\partial_\phi Y_{\ell m}=-imY_{\ell m}\), the conjugate of the usual positive-\(m\) convention. This makes a positive-frequency outgoing complex wave carry \(J_z/Q=m/q\). A different harmonic or time convention requires changing the corresponding signs consistently.

With \(y=rZ\), the five-component equation is

\[
 \mathcal A_\ell(\Omega)y=F,\qquad
 \mathcal A_\ell=-\frac{d^2}{dr^2}
       +\frac{\ell(\ell+1)}{r^2}\mathbf1+W_0(r)-\Omega^2\mathbf1+i\Omega G,
\]

\[
W_0(r)=\begin{pmatrix}
 V_u&0&2gf&0&\sqrt2af\\
 0&V_v&0&2gf&0\\
 2gf&0&D&0&0\\
 0&2gf&0&D&0\\
 \sqrt2af&0&0&0&B
\end{pmatrix},\quad
G=\begin{pmatrix}
 0&-2\omega&0&0&0\\2\omega&0&0&0&0\\
 0&0&0&-4\omega&0\\0&0&4\omega&0&0\\0&0&0&0&0
\end{pmatrix},
\]

\[
\begin{aligned}
 V_u(r)&=1-\omega^2+6\lambda f^2+ah+2gb,\\
 V_v(r)&=1-\omega^2+2\lambda f^2+ah-2gb,\\
 D&=M_X^2-4\omega^2,\qquad B(r)=M^2-\tfrac34Mh+3h^2.
\end{aligned}
\]

**Do not substitute the homogeneous equalities** \(V_u=4\lambda f^2\), \(V_v=-4gb\) into a finite profile. Radial derivatives in the background equations prevent that substitution. For real \(\Omega\), the displayed differential expression is Hermitian before imposing its outgoing boundary condition. This gives a direct flux control even if the unconstrained interior energy Hessian has a negative direction.

Regularity at the origin requires \(y_i\sim r^{\ell+1}\). A finite-\(\epsilon\) implementation must refine \(\epsilon\) or use a regular series, rather than assume a leading-power condition is exact. The \(\Omega=0\) controls are the \(\ell=0\) phase vector
\((0,\sqrt2rf,0,2\sqrt2rb,0)^T\) and the \(\ell=1\) translation vector
\((\sqrt2rf',0,\sqrt2rb',0,rh')^T\), up to overall normalization and sign.

## 2. Sidebands, thresholds, and the conjugated negative-charge channel

Apply a constant unitary circular transform:

\[
 c_{\Psi\pm}=\frac{y_1\pm iy_2}{\sqrt2},\qquad
 c_{X\pm}=\frac{y_3\pm iy_4}{\sqrt2},\qquad c_\chi=y_5.
\]

The actual complex-field waves are

\[
 \delta\Psi=\frac{c_{\Psi+}}rY_{\ell m}e^{i(\omega+\Omega)t}
       +\frac{c_{\Psi-}^*}rY_{\ell m}^*e^{i(\omega-\Omega)t},
\]

with the analogous formula for \(X\) using \(2\omega\). Thus the minus-channel physical amplitude is the **conjugate** of the circular phasor amplitude. The real neutral field is \(c_\chi Y_{\ell m}e^{i\Omega t}/r+\mathrm{c.c.}\).

At infinity the channel frequencies and squared wave numbers are

| Channel | Lab frequency \(\nu\) | \(p^2\) | Opening for \(0<\omega<1\), \(2\omega<M_X\) |
|---|---|---|---|
| \(\Psi+\) | \(\omega+\Omega\) | \((\omega+\Omega)^2-1\) | \(\Omega>1-\omega\) |
| \(\Psi-\) | \(\omega-\Omega\) | \((\omega-\Omega)^2-1\) | \(\Omega>1+\omega\) |
| \(X+\) | \(2\omega+\Omega\) | \((2\omega+\Omega)^2-M_X^2\) | \(\Omega>M_X-2\omega\) |
| \(X-\) | \(2\omega-\Omega\) | \((2\omega-\Omega)^2-M_X^2\) | \(\Omega>M_X+2\omega\) |
| \(\chi\) | \(\Omega\) | \(\Omega^2-M^2\) | \(\Omega>M\) |

Equality is a zero-flux threshold and should be approached from either side, not used as a generic invertible test point. The pinned earlier stationary results give:

| \(Q\) | \(\omega\) | \(\Psi+\) | \(X+\) | \(\Psi-\) | \(X-\) |
|---:|---:|---:|---:|---:|---:|
| 80,000 | 0.9217883883 | 0.0782116117 | 0.1568231835 | 1.9217883883 | 3.8439767366 |
| 160,000 | 0.9095170227 | 0.0904829773 | 0.1813659146 | 1.9095170227 | 3.8194340054 |

The neutral threshold is 100. These numbers must be recomputed from any newly regenerated profile's own \(\omega\). They describe small vacuum waves, not the nonlinear production or escape of intact daughter solitons.

## 3. Exact free exterior Robin conditions

For an **actual lab wave** proportional to \(e^{i\nu t}\), positive outward group velocity requires signed radial wave number \(k=\operatorname{sgn}(\nu)p\), \(p>0\), so its outgoing reduced radial function is proportional to \(\widehat h_\ell^{(2)}(pr)\) for \(\nu>0\) and \(\widehat h_\ell^{(1)}(pr)\) for \(\nu<0\). Here \(\widehat h_\ell^{(a)}(z)=z h_\ell^{(a)}(z)\).

For a circular **minus phasor**, conjugate that condition because the actual amplitude is \(c_-^*\). Consequently, under the bound-background assumptions above and \(\Omega>0\), **every open circular channel** has

\[
 c_j'(R)=\beta_j^{\rm out}c_j(R),\qquad
 \beta_j^{\rm out}=p_j\,
   \frac{[\widehat h_\ell^{(2)}]'(p_jR)}{\widehat h_\ell^{(2)}(p_jR)}.
\]

Using \(h^{(1)}\) directly for the open minus phasor would make its physical negative-frequency wave incoming. The incoming circular condition uses \(h^{(1)}\), the complex conjugate of the displayed outgoing logarithmic derivative.

For a closed channel, let \(\kappa_j=\sqrt{\mu_j^2-\nu_j^2}>0\) and use the real decaying solution:

\[
 \beta_j^{\rm dec}=\kappa_j\frac{[\widehat k_\ell]'(\kappa_jR)}{\widehat k_\ell(\kappa_jR)},
 \qquad \widehat k_\ell(z)=z k_\ell(z).
\]

For \(\ell=0,1,2\), constants cancel from logarithmic derivatives, so convenient reduced functions are

\[
\begin{array}{c|c|c}
\ell&H_\ell(z)\ \hbox{outgoing}&K_\ell(z)\ \hbox{decaying}\\\hline
0&e^{-iz}&e^{-z}\\
1&e^{-iz}(1-i/z)&e^{-z}(1+1/z)\\
2&e^{-iz}(1-3i/z-3/z^2)&e^{-z}(1+3/z+3/z^2).
\end{array}
\]

They satisfy the free radial equation and \(\Im(H_\ell^*H_\ell')=-1\) for real \(z>0\). Thus the coefficient of \(H_\ell\) has a unit-modulus asymptotic radial normalization for every tested \(\ell\). At a threshold, the reduced decaying power has logarithmic derivative \(-\ell/R\); \(\ell=0\) is the marginal constant solution. Large-argument scaled functions or these explicit expressions avoid modified-Bessel underflow.

If \(c=Ty\), implement \(y'=T^\dagger\operatorname{diag}(\beta_j)Ty\). For unreduced \(Z\), subtract \(1/R\) from each reduced logarithmic derivative. The free Robin condition is exact only after the profile-dependent couplings are negligible: check those tails and increase \(R\), or integrate an exterior Jost solution including the residual tails. A bare \(-ip\) Robin omits the finite-radius centrifugal correction for \(\ell>0\).

## 4. Signed laboratory flux and the conserved rotating flux

Take \(c_j=A_jH_\ell(p_jr)\) in an open channel. For an actual charged wave of frequency \(\nu_j\), angular index \(m_j\), charge weight \(q_j\), and signed \(k_j\), the integrated flux is

\[
 \dot E_j=2\nu_jk_j|A_j|^2,\quad
 \dot Q_j=2q_jk_j|A_j|^2,\quad
 \dot J_{z,j}=2m_jk_j|A_j|^2.
\]

For the minus branch, \(\nu_j<0\), \(k_j=-p_j\), and \(m_j=-m\); its outgoing energy is positive and its outgoing charge is negative. The neutral real wave has \(\dot E_\chi=2\Omega p_\chi|A_\chi|^2\), \(\dot Q_\chi=0\), and \(\dot J_{z,\chi}=2mp_\chi|A_\chi|^2\). These factors use the explicit phasor-plus-conjugate convention above; adding a `Re` or one-half convention changes amplitude factors.

The conserved quadratic scattering flux is that of \(K=E-\omega Q\):

\[
 \boxed{\dot K_j=2\Omega p_j|A_j|^2},\qquad
 \dot K=-2\Omega\Im(y^\dagger y').
\]

Use flux-normalized coefficients \(a_j=\sqrt{2\Omega p_j}A_j\). For either charged species, with \(\sigma=+1\) for its plus channel and \(-1\) for its open minus channel,

\[
 \dot K_j=|a_j|^2,\qquad
 \dot E_j=\left(1+\frac{\sigma q_j\omega}{\Omega}\right)|a_j|^2,\quad
 \dot Q_j=\frac{\sigma q_j}{\Omega}|a_j|^2,\quad
 \dot J_{z,j}=\frac{m}{\Omega}|a_j|^2.
\]

For \(\chi\), set \(q_j=0\). Closed channels carry no asymptotic flux. \(\dot J_z/\dot K=m/\Omega\) is common to this coherent \((\Omega,\ell,m)\) sector; \(\dot J_z/\dot E=m_j/\nu_j\) is channel-dependent.

For source-free real-frequency scattering with no absorption, the flux-normalized open-channel matrix must satisfy \(S^\dagger S=\mathbf1\). Do not impose laboratory-energy unitarity across mixed sidebands: the background can exchange energy and charge at second order while preserving \(\Delta E=\omega\Delta Q\). The linear solution does not evolve that backreaction. These positive \(K\)-flux normalizations rely on the bound-vacuum inequalities; an arbitrary background with \(q\omega\) above its vacuum mass needs a separate branch-sign analysis.

## 5. Scattering versus an explicit local drive

For a unit incoming open channel at \(R\), impose outgoing conditions on the remainder. In circular coordinates the inhomogeneous boundary condition is

\[
 c'-\beta^{\rm out}c=(\beta^{\rm in}-\beta^{\rm out})c^{\rm in}.
\]

This measures conversion and centrifugal suppression for a specified incident flux. With zero incoming amplitude and no force, a generic real-frequency solution is zero: outgoing boundary conditions alone do not create a radiation rate.

For a merger-relevant first diagnostic, instead prescribe a smooth compact canonical force \(F(r)\), solve \(\mathcal A_\ell(\Omega)y=F\), and extract each outgoing coefficient from its value and derivative. Report the force norm, support, phase, amplitude, and channel-resolved flux. A useful declared drive comes from the U(1)-invariant real modulation \(\delta V=\epsilon s(r,\theta,\phi,t)|\Psi|^2\), with \(s=S(r)Y_{\ell m}e^{i\Omega t}+\mathrm{c.c.}\). Its leading reduced force has \(F_1=-\sqrt2\epsilon r f S\) and other components zero. The full modulation preserves charge but can supply energy and angular momentum; an arbitrary imposed canonical force may also supply charge. Track those source budgets explicitly. For the stated phasor convention the exact steady work balance is

\[
 \dot K_{\rm out}=2\Omega\Im\int_0^R y^\dagger F\,dr
              =-2\Omega\Im\int_0^R F^\dagger y\,dr.
\]

This is a strong normalization and Robin control. The force power is supplied externally in this test; it is not a measured merger source. A response pole or outgoing power per unit force does not yet give power per unit stored excitation.

A compact \(\ell=0\) amplitude drive tests compressional leakage; a compact \(\ell=2\) drive tests a deformation channel. An \(\ell=1\) drive must distinguish pure translation and externally forced COM acceleration. Useful first frequencies for both pinned profiles are 0.05 (all vacuum channels closed), 0.12 (only \(\Psi+\) open), and 0.25 (\(\Psi+\) and \(X+\) open). Avoid a true bound-mode pole in the no-flux control. The upper thresholds can initially be checked in the analytic free-channel controls without resolving \(\Omega\sim100\) on a coarse interior grid.

To turn the result into a linear damping rate, identify a localized finite-fragment mode, its source overlap and appropriate excitation energy. For an isolated weakly damped pole with **positive** quadratic excitation energy, outgoing power divided by that energy gives its energy-decay rate. In the convention \(e^{i\Omega t}\), a damped pole has \(\Im\Omega>0\) and energy decay \(\Gamma_E=2\Im\Omega\). A negative-energy mode needs a separate stability analysis; radiating positive \(K\) need not damp it. A true below-threshold mode has zero linear vacuum leakage; nonlinear harmonics and daughter formation require additional calculations.

For a retarded driven solution in this time convention, the adiabatic prescription is \(\Omega\to\Omega-i\eta\), \(\eta>0\), followed by convergence as \(\eta\downarrow0\). A finite artificial \(\eta\) absorbs energy and must not be counted as physical radiation. If a real bound pole is approached, there may be no bounded monochromatic steady response; divergent drive response is not a finite damping measurement.

## 6. Executable test obligations and interpretation limits

1. Pin a regenerated profile, its charge, energy, \(\omega\), grid, tail errors, and exact action parameters. Reproduce the phase and translation controls before outgoing solves.
2. Verify free-channel circular diagonalization, outgoing/decaying \(\ell=0,1,2\) residuals, and Wronskian signs. Preserve the minus-channel conjugation explicitly in output metadata.
3. At the three low frequencies above, run declared compact drives on at least two radial resolutions and exterior radii; test origin, residual, amplitude-squared flux scaling, and work balance. All-closed flux must converge to zero away from poles.
4. If a narrow feature is found, distinguish a box level from an outgoing pole using exterior-radius independence and \(\eta\) convergence. Report trapped energy, emitted \(E,Q,J_z\), and the signed background charge drift needed to balance them.
5. Supply a merger excitation spectrum or a normalized physical internal-mode amplitude before interpreting the response as a merger efficiency or a cooling time. Intact-fragment ejection remains outside this linear test.

An \(\ell=0\) calculation carries no intrinsic \(J_z\). A real standing angular pattern with equal \(+m\) and \(-m\) powers also has zero net intrinsic flux; nonzero \(\ell\) alone is insufficient. The outgoing intrinsic angular momentum is about the fragment centre. Galaxy-centred export additionally includes \(\mathbf R_{\rm fragment}\times\dot{\mathbf P}_{\rm out}\) and requires a directional correlation with the galaxy's orbital angular momentum. Neither an imposed chiral drive nor a formal large \(m/\Omega\) ratio establishes that correlation or closes the outer-envelope receiver and four-dwarf budgets.
