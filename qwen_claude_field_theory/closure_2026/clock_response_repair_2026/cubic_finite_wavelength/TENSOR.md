# Same-action homogeneous tensor gate

## Action and exact scope

This checks the linear transverse-traceless sector of the same action

\[
S=\int d^4x\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
+P(X,\tau)+\sqrt{X_\tau}W(Y,\tau)-V(\tau)
+\gamma X\Box\chi\right]+S_m[g],
\]

with signature \((-+++)\), \(X=-\partial\chi\cdot\partial\chi\),
\(n_\mu=-\partial_\mu\tau/\sqrt{X_\tau}\), \(Q=n\cdot\partial\chi\),
\(Y=Q^2-X\), and constant \(\gamma\). The background has homogeneous
\(\chi,\tau\), positive lapse \(N(t)\), scale factor \(a(t)>0\), and
\(H=\dot a/(Na)\). The coefficient functions are arbitrary: no repair
profile, background field equation, or coefficient refit is used.

Only the two TT perturbations are varied. Their quadratic action is not a
count of all gravitational/scalar degrees of freedom, a nonlinear health
proof, or a tensor-speed claim on inhomogeneous clock backgrounds.

## Direct variation

Set the shift to zero and use

\[
h_{ij}=a^2[\exp(\epsilon t)]_{ij},\qquad
t=\begin{pmatrix}p&c&0\\c&-p&0\\0&0&0\end{pmatrix},
\qquad p=p(t,z),\quad c=c(t,z).
\]

This is TT for waves along \(z\). The exponential parametrization is
important at second order: \(\det\exp(\epsilon t)=1\) exactly, so
\(\sqrt h=a^3\) and \(K=\partial_t\log\sqrt h/N=3H\), with no tensor
variation. A Cartesian linear metric parametrization would instead require
the associated second-order volume/background-equation bookkeeping.

The executable constructs the metric and inverse through order
\(\epsilon^2\), differentiates the metric for \(K^i{}_j\), and constructs
the three-dimensional connection and Ricci tensor from spatial derivatives.
Their actual contractions give

\[
K^i{}_jK^j{}_i=3H^2+\frac{\epsilon^2}{2N^2}
(\dot p^2+\dot c^2)+O(\epsilon^3),\qquad
{}^{(3)}R=-\frac{\epsilon^2}{2a^2}(p_z^2+c_z^2)
+O(\epsilon^3).
\]

The Einstein-Hilbert term is evaluated in ADM form, with the usual temporal
boundary term omitted. Its order-two density is therefore

\[
\mathcal L^{(2)}_T=
\frac{M^2a^3}{4N}(\dot p^2+\dot c^2)
-\frac{M^2Na}{4}(p_z^2+c_z^2).
\]

No short-wavelength approximation is needed for this TT action.

## Why the same clock terms contribute zero

For homogeneous scalars the inverse four-metric gives
\(X=\dot\chi^2/N^2=Q^2\), \(X_\tau=\dot\tau^2/N^2\), and \(Y=0\),
all independent of the tensor amplitudes. Both their arguments and the
volume element have zero tensor variation. Consequently arbitrary
\(P(X,\tau)\), \(\sqrt{X_\tau}W(0,\tau)\), and \(-V(\tau)\) contribute
no quadratic tensor term.

The cubic term is checked directly rather than inferred from that result:

\[
\Box\chi=-\frac{1}{N\sqrt h}\partial_t
\left(\sqrt h\,\frac{\dot\chi}{N}\right)
=-\frac{\dot Q}{N}-3HQ.
\]

Since \(\sqrt h=a^3\), this also has no tensor variation. The code
independently checks the homogeneous boundary identity

\[
Na^3\gamma X\Box\chi
=-\frac23Na^3\gamma Q^3K
+\partial_t\left(-\frac{\gamma a^3Q^3}{3}\right),
\]

and verifies that its ADM representative has zero quadratic tensor
variation. This is why this cubic interaction produces neither a tensor
kinetic nor a tensor spatial-gradient correction on this branch.

An optional homogeneous minimal radiation proxy
\(\mathcal L_r=C_rX_r^2\) is checked in the same way. It is a perfect-fluid
proxy, **not a photon/neutrino free-streaming CMB model**. The calculation
does not remove tensor anisotropic-stress sources from more detailed matter.

## Computed two-polarization Hessian and speed

For \(p=p_+(t)\cos(kz)\), \(c=p_\times(t)\cos(kz)\), exact spatial period
averaging gives

\[
L^{(2)}_{T,k}=\frac{M^2a^3}{8N}
(\dot p_+^2+\dot p_\times^2)
-\frac{M^2Na k^2}{8}(p_+^2+p_\times^2).
\]

Differentiating this action, rather than supplying the answer, gives

\[
\mathsf K_T=\frac{M^2a^3}{4N}\mathbf1_2,\qquad
\mathsf G_T=\frac{M^2Na k^2}{4}\mathbf1_2,\qquad
\operatorname{rank}\mathsf K_T=2,
\]

\[
\frac{a^2}{N^2k^2}\mathsf K_T^{-1}\mathsf G_T=\mathbf1_2,
\qquad c_{T,+}^2=c_{T,\times}^2=1.
\]

Here \(M^2>0\), \(a,N>0\), and \(k\ne0\); the Hessian is positive.
The exact tensor mode equation is

\[
\ddot p_s+\left(3NH-\frac{\dot N}{N}\right)\dot p_s
+\frac{N^2k^2}{a^2}p_s=0,\qquad s\in\{+,\times\},
\]

in the absence of matter tensor anisotropic stress. Its proper-time
principal speed is one. The homogeneous \(k=0\) limit has no wave-speed
measurement but retains the same velocity Hessian.

## Reproducibility and controls

Run `python3 tensor_gate.py` in this directory. The script exposes
`derive() -> (facts, ctx)` and accepts `--result-file PATH` for the main
runner. It records the metric-derived intermediate expressions, each
zero-residual check, the differentiated Hessians, rank, and speed spectrum.

The answer is not hardcoded: a sensitivity control rescales only the
computed spatial-curvature contribution by \(\eta\), recomputes the
gradient Hessian, and obtains \(c_T^2=\eta\). A second control sets the EH
coefficient to zero and confirms that the computed tensor Hessian vanishes.
These controls would fail if the reported rank or speed were disconnected
from the varied action. No external theorem or generic GR citation is used
as a substitute for this local calculation.

Actual local run: Python 3.9.6 / SymPy 1.14.0, exit code 0; all 26 exact
checks passed. The computed tensor Hessian rank was 2, both speed-squared
eigenvalues were 1, and the curvature-deformation speed matrix was
\(\eta\mathbf1_2\). The encompassing finite-wavelength runner owns any
persisted run manifest/output; no separate tensor manifest is introduced.
