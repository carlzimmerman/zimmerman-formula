# Independent Nf=2 constant-mode chiral/QED derivation

Saved before reading controlled_model/qcd_zero_modes or coordinator/ZERO_MODE_QED_RAW.md. No child was spawned and no mathematical computation was executed. The starting point is the standard leading SU(2) chiral action with the Dashen operator.

## Exact compact integral

Take two equal positive renormalized quark masses \(m\), \(F,\Sigma,C\) constant at this retained chiral order, \(M^2=2m\Sigma/F^2\), and physical four-volume \(V\). Write
\[
U=a_0{\bf1}+i a_j\tau_j,\qquad a_0^2+\mathbf a^2=1,\qquad
Q={1\over6}{\bf1}+{1\over2}\tau_3.
\]
Set \(\mu=m\Sigma V\), \(\eta=e^2CV\), \(c_\theta=\cos(\theta/2)\). The constant-mode Euclidean partition function with normalized Haar measure is
\[
Z_H(\theta,\mu,\eta)=\int_{SU(2)}dU\,
\exp[2\mu c_\theta a_0+\eta\operatorname{tr}(QUQU^\dagger)].
\]
The exact charge trace is
\[
\operatorname{tr}(QUQU^\dagger)=5/9-(a_1^2+a_2^2).
\]
Using Hopf coordinates
\[
a_1+ia_2=\sqrt t\,e^{i\psi},\qquad
a_0+ia_3=\sqrt{1-t}\,e^{i\phi},
\quad 0\le t\le1,
\]
normalized Haar is \(dt\,d\phi\,d\psi/(4\pi^2)\). Consequently
\[
\boxed{\quad
Z_H=e^{5\eta/9}\int_0^1dt\,e^{-\eta t}
 I_0(2\mu c_\theta\sqrt{1-t}).\quad}
\]
The omitted overall constant would matter for a free energy but not normalized expectations. At \(\eta=0\),
\[
Z_H={I_1(2\mu c_\theta)\over\mu c_\theta},\qquad
Z_H(0,0,0)=1.
\]
At \(\mu=0\), the continuous expression is
\(Z_H=e^{5\eta/9}(1-e^{-\eta})/\eta\).

## Susceptibility and condensate identity

All theta dependence enters through \(\mu c_\theta\); the Dashen term is theta independent. At theta zero,
\[
\chi=-{1\over V}\partial_\theta^2\log Z
={\mu\over4V}\partial_\mu\log Z.
\]
Define the positive flavour-averaged condensate by
\[
\Sigma_V={1\over2V}\partial_m\log Z
={\Sigma\over2}\partial_\mu\log Z.
\]
For any multiplicative measure factor independent of \(m,\theta\),
\[
\boxed{\chi={m\over2}\Sigma_V}
\]
at this retained action, for all positive \(\mu\) and allowed \(\eta\). QED distinguishes flavours, so this is the average, not an assumption of identical individual condensates.

At zero charge,
\[
\Sigma_V=\Sigma\,{I_2(2\mu)\over I_1(2\mu)},\qquad
\chi={m\Sigma\over2}{I_2(2\mu)\over I_1(2\mu)}.
\]
The susceptibility behaves as \(\mu^2/(4V)+O(\mu^4/V)\) at small \(\mu\), and \(m\Sigma/2-3/(8V)+O(1/(m\Sigma V^2))\) at large \(\mu\).

For a leading charge insertion, set \(T(\mu)=\langle a_1^2+a_2^2\rangle_{\eta=0}\). Rotational symmetry plus integration by parts on the unit S3 gives
\[
T(\mu)={1\over2\mu}\partial_\mu\log Z_H(\mu,0)
={I_2(2\mu)\over\mu I_1(2\mu)}.
\]
Hence
\[
\left.\partial_{e^2}\log Z_H\right|_0
=CV[5/9-T(\mu)],\qquad
\left.\partial_{e^2}\chi\right|_0=-{C\mu\over4}T'(\mu).
\]
The large-\(\mu\) leading value of the latter is \(C/(4\mu)\).

## Canonical constant-mode measure

For a canonically normalized pion field \(\pi^a\), the orthonormal constant harmonic is \(V^{-1/2}\), so its coefficient is \(q^a=\sqrt V\,\pi^a\). Near the identity \(a_j=\pi_j/F+\cdots=q_j/(F\sqrt V)+\cdots\). The L2 metric on the full constant SU(2) manifold is \((F\sqrt V)^2\) times the unit-S3 metric.

With canonical per-mode measure \(\nu\,dq/\sqrt{2\pi}\), where the fixed mass \(\nu\) defines the dimensionless Gaussian determinant, the induced constant-mode measure is
\[
d\mu_{\rm can}={\nu^3(F\sqrt V)^3\over(2\pi)^{3/2}}\,d\Omega_{S^3}
=N_{\rm can}(V)dU,
\]
\[
\boxed{\quad N_{\rm can}(V)=\sqrt{\pi/2}\,
(\nu F\sqrt V)^3.\quad}
\]
The normalized Haar group integral and the induced canonical constant-coordinate integral are different absolute normalizations. In a full chiral path integral the nonzero-mode decomposition, its Jacobians and measure convention must be matched too; the isolated group integral alone cannot fix the full partition function normalization.

## Charged Gaussian matching

For large positive \(\mu c_\theta\) and \(\mu c_\theta+\eta\), the identity saddle gives
\[
Z_H\sim {e^{2\mu c_\theta+5\eta/9}\over
2\sqrt\pi\,(\mu c_\theta)^{1/2}(\mu c_\theta+\eta)}.
\]
Since
\[
\mu={F^2VM^2\over2},\qquad
\eta={F^2V\Delta\over2},\qquad
\Delta={2e^2C\over F^2},
\]
multiplication by \(N_{\rm can}\) gives
\[
\boxed{\quad
Z_{\rm can}\sim e^{2\mu c_\theta+5\eta/9}
{\nu^3\over\sqrt{M^2c_\theta}\,[M^2c_\theta+\Delta]}.
\quad}
\]
After removing the classical Dashen constant, the charged-pair ratio at theta zero is \(M^2/(M^2+\Delta)\). This is exactly the determinant ratio of two real constant Gaussian modes, with no further doubling for the charge labels. The neutral constant Gaussian mode contributes \(\nu/M\).

This also reproduces the leading charge correction to the susceptibility:
\[
\chi_\gamma-\chi_0
={\Delta\over4V(M^2+\Delta)}+\cdots,\qquad
\left.\partial_{e^2}\chi\right|_0
={C\over2F^2VM^2}={C\over4\mu}+\cdots.
\]
The classical flat-volume terms are distinct from the finite-volume Gaussian correction.

## Radius, order of limits and normalization

On round S4, \(V=v_4H^{-4}\), \(v_4=8\pi^2/3\). Thus
\[
\mu={F^2M^2v_4\over2H^4},\qquad
\eta={e^2Cv_4\over H^4},\qquad
N_{\rm can}\propto V^{3/2}\propto H^{-6}.
\]
The epsilon regime keeps \(\mu\) and, if needed, \(\eta\) finite while the volume grows. It requires \(M^2\sim H^4/F^2\), and keeping \(\eta\) finite also requires \(e^2\sim H^4/C\). Then \(M/H\to0\), unlike the fixed-positive-mass regime \(H/M\to0\) of the ordinary massive pion determinant.

At fixed positive \(m,e^2\), instead \(\mu,\eta\propto V\to\infty\), and the compact integral approaches the Gaussian constant-mode result above. It still represents only the constant mode. Nonconstant modes are required to match a full four-dimensional determinant or its metric stress.

A factor \(N(V)\) independent of \(m,\theta\) preserves the condensate/susceptibility identity but changes \(-\log Z/V\) and its metric variation. Arbitrary \(N(V)\) cannot be used to infer a vacuum coefficient. The canonical polynomial factor contributes only order \(H^4\log H\) to the isolated action density, never a linear \(H\) term. Its role is to match the chosen canonical functional measure; it is not permission to add an arbitrary radius-dependent physical term.
