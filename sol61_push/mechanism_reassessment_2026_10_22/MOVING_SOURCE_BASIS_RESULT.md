# Source-adapted quantum representation and momentum tests

**Partial result:** the large coherent displacement and the supplied Gaussian squeezing can be represented without the small Fock-occupation cutoff. An exact non-Gaussian potential substep is implemented, and its initial interaction kernels have passed independent fixed-band momentum checks. **The actual source has not yet been evolved through bath formation, and no surviving cold abundance is calculated.** Full kinetic propagation of the non-Gaussian state, renormalization and the late reaction evolution remain outstanding.

## Removing the initial occupation burden without changing the state

For each nonzero real mode of the supplied high-H Hankel covariance, let F=<delta q²>, P=<delta p²>, C=<{delta q,delta p}>/2. The source has FP-C²=lambda²/4 in the conformal normalization. Write

\[
\binom{\delta q}{\delta p}=S\begin{pmatrix}Q\\P_r\end{pmatrix},\qquad
S=\begin{pmatrix}
\sqrt{2F/\lambda}&0\\
C\sqrt{2/(\lambda F)}&\sqrt{\lambda/(2F)}
\end{pmatrix}.
\]

Here the second entry on the right is the reference momentum P_r, not the covariance P. Equivalently use the column (Q,P_r)^T. Since det S=1, this is a canonical transformation. The reference covariance is lambda I/2. A separate displacement carries the saved mean fields and velocities.

Thus the large mean-field occupation estimates in the preceding report are not a fundamental barrier: they apply to the undisplaced basis. The supplied Gaussian mode state is the reference vacuum of this new basis even though the physical fields and their squeezing are large. **Reference vacuum does not mean an empty physical source or a cold population.**

`moving_source_basis.py` constructs this transformation and checks both its symplectic determinant and covariance reconstruction. No field amplitude is reduced to fit a small occupation cutoff. This covers the supplied nonzero-mode Gaussian ansatz and mean displacements; it does not determine the previously unspecified coarse/zero-mode density matrix or interacting initial higher cumulants.

## Residual interactions that must still be evolved

After including the displacement and Gaussian linear/quadratic terms in a reference generator, the higher-degree residual potential at the initial instant is

\[
V_R=\bar f:\!(f^3+fh^2)\!:
+\frac14:\!(f^2+h^2)^2\!:
+c\big[:\!x(f^2-h^2)\!:+2:\!yfh\!:\big].
\]

The four symbols f,h,x,y here denote fluctuations, with the Phi mean aligned along its first real component. c is the original conformal cubic coefficient. Normal ordering is with respect to the source Gaussian covariance. The compensating constant, linear and quadratic terms belong in the reference generator; discarding them would change the model. This decomposition is a representation of the original polynomial interactions, not a new action or an additional collision term.

`quantum_source_kick.py` implements the explicit residual polynomial and its force, including the source-covariance subtractions, and the map

\[
\Psi\longmapsto\exp[-i\,\Delta z\,H_R/\lambda]\Psi,
\qquad H_R=\int d^3y\,V_R.
\]

For a fixed reference basis and a potential-only substep this is exact, unitary and non-Gaussian. It has no occupation ceiling. The inverse substep is obtained by changing the sign of Delta z. It is **not** the full field evolution: the kinetic/reference generator must also act on the resulting non-Gaussian wavefunctional. Repeatedly replacing that state by a Gaussian would discard the correlations the user requested.

The elementary cubic and quartic vertices are retained, so their full evolution would retain the previously validated absorption reaction and inverse. However, neither the single-kick reversibility test nor the initial residual norm is a new calculation of the physical on-shell absorption/inverse rates. That reaction requires propagation between vertices. No independently appended rate is used, and no claim of completed late-time reaction evolution is made.

## Exact initial residual kernels

For diagonal initial equal-time covariance define

\[
K_a(r)=\int\frac{d^3k}{(2\pi)^3}F_a(k)e^{i\mathbf k\cdot\mathbf r}.
\]

Wick contraction across the normal-ordered residual vertices gives the initial excitation-probability coefficient per volume:

\[
D_3^\Phi=\lambda^{-2}\int d^3r\,\bar f^2(6K_f^3+2K_fK_h^2),
\]
\[
D_3^X=\lambda^{-2}\int d^3r\,c^2[2K_x(K_f^2+K_h^2)+4K_yK_fK_h],
\]
\[
D_4=\lambda^{-2}\int d^3r\,[\tfrac32(K_f^4+K_h^4)+K_f^2K_h^2].
\]

For a small interval, the residual-vacuum escape probability is V(D3Phi+D3X+D4) Delta z² to leading order. These coefficients are **not collision rates**; in particular the quadratic short-time law is not a Markovian loss law.

For the exact single frozen potential kick the mean reference occupation obeys the stronger identity

\[
\frac{\langle N_R\rangle}{V}
=(\Delta z)^2[3D_3^\Phi+3D_3^X+4D_4].
\]

The identity follows by transforming the reference momenta under the potential kick and evaluating their squared shift. An independent four-variable Gauss–Hermite integration verifies it against the normal-ordered polynomial sector norms. It is a statement about reference excitations under this substep, not about physical cold particles.

## Momentum convergence: what passed and what did not

We held the physical momentum band fixed at k in [2pi/32,pi/2], in conformal units. This is a specified finite-band test using the high-H source covariance ansatz, not a UV/IR-complete cosmological state.

The first Cartesian test varied momentum spacing using L=32,48,64,96,128. FFT padding removes wraparound momentum aliasing; an independent padding choice agrees. Nevertheless, the final spacing refinement changed the cubic and quartic kernels by about 11–12%. That sequence was **not** declared converged. The sharp low-momentum boundary is poorly sampled on these grids.

An independent isotropic continuum calculation uses

\[
K_a(r)=\frac1{2\pi^2}\int_{k_{\min}}^{k_{\max}}
 dk\,k^2F_a(k)\operatorname{sinc}(kr).
\]

Gauss–Legendre momentum integration and radial integration were refined from 256 momentum points and rmax=128 to 1024 points and rmax=512. A second method integrates the three-momentum convolution directly over the triangle domain:

\[
\int d^3r K_aK_bK_c
=\frac1{8\pi^4}\int dk\,dp\,kpF_a(k)F_b(p)
\int_{\max(|k-p|,k_{\min})}^{\min(k+p,k_{\max})}dq\,qF_c(q),
\]

with an empty inner interval contributing zero. The two methods agree on the Phi cubic coefficient to **1.18e-6 relative**. The last radial refinements change the cubic coefficients by less than 4.6e-8 and the quartic coefficient by 5.4e-10. These are numerical convergence diagnostics for these initial fixed-band kernels, not certified bounds on a full quantum evolution.

| Fixed-band continuum coefficient | Value |
|---|---:|
| D3Phi | 0.0102622305835 |
| D3X | 1.29280900017e-30 |
| D4 | 0.000114702549026 |
| 3 D3Phi + 3 D3X + 4 D4 | 0.0312455019465 |

The initial residual self-interaction of Phi dominates this diagnostic. The tiny initial X term does not bound late conversion: the background and conformal coupling evolve substantially before X oscillates, and the absorption channel involves more than one vertex.

A separate UV scan changes the upper cutoff at fixed box size; it is explicitly separated from the spacing test. It does not demonstrate cutoff removal or renormalization. At the continuum fixed-band coefficient, a single potential kick Delta z=0.1 gives a mean of about 10.24 reference excitations when multiplied by volume 32³. This illustrates why a global cutoff of eight excitations is restrictive even after the coherent displacement is removed. **It is not a count of cold survivors, and multiplying the continuum density by that volume does not make it the discrete L=32 result.**

## What remains before an abundance can be reported

The occupation ceiling is removed for the initial Gaussian representation and the implemented potential substep. It is not yet removed by a practical, converged algorithm for the entire many-mode quantum trajectory. The missing operation is kinetic/reference propagation of the non-Gaussian wavefunctional between successive interaction steps, or an independently validated conserving approximation to that operation. Source higher cumulants and consistent UV renormalization must also be addressed.

Without those steps, neither the actual thermalization history nor the forward/inverse conversion balance and subsequent losses have been evolved. Replacing the state by a fitted thermal bath here would repeat the assumption explicitly rejected by the user. No matching time, cold seed or surviving abundance is supplied.

## Reproducible evidence

- `moving_source_basis.py`, `moving_source_basis_run/manifest.json`: canonical source representation, Cartesian spacing test, separate UV test and aliasing check.
- `moving_source_continuum.py`, `moving_source_continuum_run/manifest.json`: radial and independent direct momentum integration.
- `quantum_source_kick.py`, `audit_quantum_source_kick.py`, `quantum_source_kick_run/manifest.json`: exact potential substep, inverse, force-gradient and independent Gaussian identity checks.

All three bounded runs completed with their declared checks passing. The Cartesian spacing changes are recorded as unresolved convergence rather than hidden behind a passing flag. Existing action and prior evidence were not overwritten.

**Status:** a source-adapted representation, a non-Gaussian quantum substep without an occupation cutoff, and an independently checked fixed-band momentum kernel are implemented. The full formation mechanism and cold abundance remain open.
