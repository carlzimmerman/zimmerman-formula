# Individual proton response: normalization, finite calculation and missing sea term

This derivation is for the leading coefficient at e=0. Write
M_p(e^2)=M_p(0)+e^2 D_p+O(e^4), alpha=e^2/(4 pi), with rational quark charges fixed. The full D_p requires a declared renormalized quark-mass and strong-coupling path. For definiteness, the continuum reference is fixed MS-bar m_f(mu) and g_s(mu) at a specified mu; a physical calibration must additionally supply their values. The calculation below evaluates only a finite functional of a published pure-QCD Compton tensor, not this full derivative.

## 1. Complete insertion and connected vacuum subtraction

Let C_p(T)=<N_p(T) Nbar_p(0)>_0 and let the electromagnetic insertion in the Euclidean effective action be

\[
I={1\over2}\int d^4x\,d^4y\;j_\mu(x)D_{\mu\nu}(x-y)j_\nu(y)+I_{ct},
\qquad j_\mu=\sum_f Q_f\bar q_f\gamma_\mu q_f.
\]

Using S_eff=S_QCD+e^2 I, differentiation of the normalized path integral gives

\[
\partial_{e^2}\log C_p=-{\langle N_p\bar N_p I\rangle_0\over C_p}+\langle I\rangle_0,
\quad
D_p=\lim_{T\to\infty}{1\over T}
\left[{\langle N_p\bar N_p I\rangle_0\over C_p}-\langle I\rangle_0\right].
\]

The vacuum expectation is removed, but a sea loop correlated with the proton through gluons remains. Currents on the same valence line, different valence lines, valence plus sea, both on one sea loop, and on different sea loops all belong to jDj. Local lattice link expansions also have contact/tadpole terms. Replacing them by a renormalized continuum time-ordered product requires matching, not their deletion.

At finite photon mass, or a specified finite-volume QED prescription, extract the charged rest energy before the controlled infrared limit. In massless infinite-volume QED use the rest threshold rather than assume an isolated charged-particle pole. At order e^2 the stable e=0 QCD pole supplies the perturbative external state. A definite charged-source dressing or fixed gauge and the limiting order are part of this prescription. The positive-momentum stencil below avoids Q=0 and therefore tests no infrared extrapolation.

## 2. Cottingham convention and the factor audit

[Can et al., v2](https://arxiv.org/abs/2501.08619v2), equations (1)-(3), and [Walker-Loud, Carlson and Miller, v2](https://arxiv.org/abs/1203.0254v2), equations (2)-(5), use the same first scalar amplitude: its tensor is (-g_munu+q_mu q_nu/q^2) T_1. Can's spin-averaged state notation includes the spin average that Walker-Loud writes explicitly as (1/2) sum_sigma. The differing second tensor normalization changes T_2 only.

Can's prefactor is -i alpha/[2M(2pi)^3] times 1/(Q^2-i epsilon), Q^2=-q^2. It is exactly +i alpha/[2M(2pi)^3] times 1/(q^2+i epsilon), the Walker-Loud convention. There is no extra spin factor or sign. For S_1(Q^2)=T_1(0,Q^2), the subtraction part of the first tensor has trace -3 S_1. Wick rotation gives d^4q=i d^4Q and q^2=-Q^2. Since

\[
\int {d^4Q\over Q^2}\,S_1(Q^2)=\pi^2\int dQ^2\,S_1(Q^2),
\]

the subtraction contribution in any finite window is

\[
\delta M_p^{sub}=-{3\alpha\over16\pi M_p}\int dQ^2\,S_1^p(Q^2),
\qquad
{D_p^{sub}\over M_p}=-{3\over64\pi^2M_p^2}\int dQ^2\,S_1^p(Q^2).
\]

This agrees with Walker-Loud equation (13). This equation alone is not the full Cottingham result: elastic and inelastic dispersive pieces and renormalization are separate. A subtraction piece can be negative even if the complete electromagnetic mass shift is positive.

## 3. Exact finite stencil in native lattice units

Use the middle ensemble of Can Tables I-III. All imported numerical inputs and their uncertainties are in INPUTS.json. The six momentum vectors have n^2=(10,13,20,34,50,65), with a^2 Q^2=(2pi/48)^2 n^2. The six S_1 values are (.688,.596,.208,.080,.136,.135), and aM=.3860. Define the finite trapezoidal estimator with endpoint half weights, rather than assert a controlled interpolation of the continuum function. In n^2 its weights are

\[
w=(3/2,5,21/2,15,31/2,15/2),\qquad \sum_iw_i S_{1,i}={21033\over2000}.
\]

The prefactor and native momentum unit cancel pi^2 exactly:

\[
K_p^{sub,conn,window}:=-{3\over16 N_L^2(aM)^2}\sum_iw_iS_{1,i}
=-{876375\over152571904}
=-0.005744012999929529.
\]

No numerical alpha, physical proton mass, hbar*c, lattice spacing in fm, or fitted target enters this calculation. Rounded Q^2 values in GeV^2 are context only. The source's plateau/Feynman-Hellmann and current-renormalization extractions involve fits; our finite transformation introduces no new fit. The input beta, equal quark kappa, improvement prescription, rational charge weights, and aM are declared, so this is not a no-input selection of QCD parameters.

The source provides marginal errors but not a usable covariance matrix. For any positive semidefinite covariance with these marginal errors,

\[
\sigma(K)\le {3\over16 N_L^2(aM)^2}\sum_i|w_i|\sigma_i
={166375\over76285952}=0.002180938896849580,
\]

conditional on fixed aM. This is a ceiling on the standard deviation of this linear stencil under those marginal statistical errors, not a confidence bound on the physical answer. The corresponding minimum over all covariance matrices is zero. The uncorrelated illustration is .0010142653, with no claim that source errors are independent. The aM error gives a first-order relative sensitivity 2 sigma(aM)/(aM)=22/965; its correlations are unknown. Interpolation error, finite volume, residual lattice artefacts, omitted sea terms, momentum tails and mass-scheme matching have no bound here.

## 4. The surviving independent sea observable

At SU(3)-degenerate masses, each flavor has the same quark propagator S[A]. Set

\[
L_\mu(x)=\operatorname{tr}[\gamma_\mu S(x,x)],\quad
B_{\mu\nu}(x,y)=-\operatorname{tr}[\gamma_\mu S(x,y)\gamma_\nu S(y,x)].
\]

The charge factor of a one-current sea loop is Tr Q=2/3-1/3-1/3=0. A pair of separate one-current loops is proportional to (Tr Q)^2=0. The same-loop two-current term instead has Tr Q^2=4/9+1/9+1/9=2/3. Its surviving hadronic covariance is explicitly

\[
H_{\mu\nu}^{sea,2}(x,y;T)={2\over3}
\left[{\langle N_p(T)\bar N_p(0)B_{\mu\nu}(x,y)\rangle\over C_p(T)}
-\langle B_{\mu\nu}(x,y)\rangle\right].
\]

This is absent from a calculation that differentiates only valence propagators. It is not the discarded vacuum bubble; the covariance connects it to the baryon through the QCD gauge ensemble. The displayed charge factor is evaluated exactly. Its nonperturbative amplitude is not evaluated and is not proved nonzero. At isospin symmetry this insertion is identical for proton and neutron; its coefficient is zero in p-n and 4/3 in p+n, while it remains 2/3 for the individual proton. Thus no accuracy in the p-n splitting determines this observable. Away from the degenerate limit even the one-current-loop cancellation must be re-evaluated with the actual flavor propagators.

## 5. UV subtraction is an actual matching obligation

The full current product requires quark-mass, strong-coupling and identity counterterms. In [Gasser et al., corrected v3](https://arxiv.org/abs/1506.06747v3), equations (56)-(57),(64), the relevant local structures are 1, qbar q and G^2; the electromagnetic shifts include delta m_q proportional to e^2 Q_q^2 m_q and delta g proportional to e^2 g^3 sum Q_q^2. The identity drops out of the connected proton energy, but the scalar and gluonic matrix elements do not. This is the individual-nucleon obligation; the isovector simplification cannot remove its isoscalar matching.

For two matching conventions related by m_f'=m_f+e^2 c_f m_f and g_s'=g_s+e^2 c_g, the derivative at fixed primed parameters is

\[
D_p'=D_p-\sum_f c_fm_f\,\partial_{m_f}M_p-c_g\partial_{g_s}M_p.
\]

Thus a quoted electromagnetic proton mass without its fixed-parameter convention cannot be substituted into a constrained R(alpha) derivative. The finite stencil above supplies neither these counterterms nor their matching Jacobian.

For R=A_rho/M_p^3 on one common path,

\[
\partial_{e^2}\log R=\partial_{e^2}\log A_\rho-3D_p/M_p.
\]

The value K_p is only one bounded data functional in the second term. It cannot replace the complete D_p or the independent stress response in the first term.
