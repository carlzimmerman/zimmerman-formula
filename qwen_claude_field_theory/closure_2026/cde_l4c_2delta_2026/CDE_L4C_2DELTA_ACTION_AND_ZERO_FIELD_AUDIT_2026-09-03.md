# CDE-L4C-2Delta: one-action variational and zero-field audit

## Status in one sentence

The frozen action below derives the exact exponential AQUAL equation, no
linear slip, and the separate ordinary-matter Ward identity in its reduced
finite-wavelength static branch. Its ADM-generated Minkowski principal block
leaves one scalar canonical pair with no quadratic spatial stiffness. The
candidate is therefore **OPEN overall and adverse on its zero-field,
zero-multiplier principal branch**, not a closed relativistic MOND theory.

## Frozen action

The candidate tested by `cde_l4c_2delta_action_gate_2026.py` is

\[
\begin{split}
S_\star={M_{\rm Pl}^2\over2}\int d^4x\sqrt{-g}\bigg[&R-2\Lambda
-{2\over\ell_0^2}F_{\exp}(y)
+\lambda_sD^2\!\left({}^{(3)}R-4D_\mu a^\mu\right)
+\lambda_KD^2K\bigg]\\
&+\int d^4x\sqrt{-g}\,[M_c^2\sqrt X-V(T)]+S_m[g,\psi],
\end{split}
\]

where

\[
X=-g^{\mu\nu}\partial_\mu T\partial_\nu T,
\quad u_\mu=-{\partial_\mu T\over\sqrt X},
\quad h_{\mu\nu}=g_{\mu\nu}+u_\mu u_\nu,
\]
\[
a_\mu=u^\nu\nabla_\nu u_\mu,
\quad K=\nabla_\mu u^\mu,
\quad y=\ell_0\sqrt{a_\mu a^\mu},
\quad \ell_0={c^2\over a_0},
\]
and
\[
F_{\exp}(y)=2[(1+y)e^{-y}-1].
\]

The exponential term is the correction to Einstein gravity, not the full
primitive added a second time. Indeed

\[
1+{F'_{\exp}(y)\over2y}=1-e^{-y}=\mu(y),
\qquad y^2+F_{\exp}(y)={2\over3}y^3-{1\over4}y^4+O(y^5).
\]

Ordinary matter occurs only in the minimally coupled `S_m[g,psi]`.

## Euler--Lagrange equations actually derived

Variation of the two multiplier fields gives

\[
{\delta S\over\delta\lambda_s}=D^2C_{\rm slip}=0,
\quad C_{\rm slip}={}^{(3)}R-4D_\mu a^\mu,
\qquad
{\delta S\over\delta\lambda_K}=D^2K=0.
\]

For the one-dimensional weak-static reduction, with \(\Phi\), \(\Psi\), and
\(\lambda_s\) kept independent, the tested Lagrangian density is

\[
L_{\rm ws}=-2\Phi'\Psi'+(\Psi')^2-a_0^2F_{\exp}(\Phi'/a_0)
-8\pi G\rho\Phi+4\lambda_s(\Psi''''-\Phi'''').
\]

Its three higher-derivative Euler equations are calculated directly by the
script. At \(k\ne0\), the multiplier equation and the independent \(\Psi\)
equation give

\[
\Psi_k=\Phi_k,\qquad (\lambda_s)_k=0.
\]

Only after solving those equations is the \(\Phi\) equation reduced. It is

\[
2\left[1+(y-1)e^{-y}\right]\Phi''-8\pi G\rho=0,
\qquad y={\Phi'\over a_0},
\]

which is the longitudinal form of

\[
\nabla\!\cdot\!\left[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi\right]
=4\pi G\rho.
\]

Thus this reduced branch derives \(\Phi\) and \(\Psi\) separately and has
\(\gamma_{\rm PPN}=\Psi/\Phi=1\) at linear static order. It is not a full
boosted PPN calculation and does not determine \(\beta\) or
\(\alpha_{1,2,3}\).

Separate diffeomorphism invariance of the minimally coupled matter action
gives

\[
\nabla_\mu T_m^{\mu\nu}=-E_\psi\nabla^\nu\psi=0
\]

on the matter equation. This is the baryonic Ward identity, not conservation
of a combined matter-plus-auxiliary tensor.

## ADM generation and Dirac chain of the exact-zero-field principal block

The principal Lagrangian is not inserted independently. The script expands
the ADM ingredients \(N\sqrt h\,{}^{(3)}R\),
\(N\sqrt h(K_{ij}K^{ij}-K^2)\), \(a_i a^i\),
\(D^2C_{\rm slip}\), and \(D^2K\) for a real scalar Fourier mode and performs
the spatial average. On the zero-multiplier, locally flat, unitary-gauge
branch, after the scalar spatial gauge has been removed, this gives

\[
L_0=A\left[-3\dot\Psi^2+2k^2B\dot\Psi+k^2(\Phi-\Psi)^2
-2k^4\lambda_s(\Phi-\Psi)
+{\lambda_K\over2}(3k^2\dot\Psi-k^4B)\right],
\quad A>0.
\]

The only nonzero momentum is

\[
p_\Psi=A\left(2k^2B+{3\over2}k^2\lambda_K-6\dot\Psi\right),
\]

and the four primaries are

\[
p_\Phi=p_B=p_{\lambda_s}=p_{\lambda_K}=0.
\]

Their preservation produces four secondaries,

\[
\begin{aligned}
C_\Phi&=2Ak^2(\Phi-\Psi-k^2\lambda_s),\\
C_B&={k^2\over3}(2Ak^2B-p_\Psi),\\
C_s&=-2Ak^4(\Phi-\Psi),\\
C_K&={k^2\over8}(3Ak^2\lambda_K-2p_\Psi).
\end{aligned}
\]

The program constructs every Poisson bracket from the five canonical pairs;
it does not insert a rank or determinant. For \(A>0,k\ne0\) it obtains

\[
\det\Delta=A^8k^{32},\qquad
\operatorname{rank}\Delta=8,
\]

and independently finds constraint-Jacobian rank eight. All eight constraints
are second class. Preservation fixes all four primary multipliers and produces
no tertiary constraint. The constraint surface is

\[
\Phi=\Psi,\quad\lambda_s=0,\quad
B={p_\Psi\over2Ak^2},\quad
\lambda_K={2p_\Psi\over3Ak^2}.
\]

The pulled-back canonical one-form and Hamiltonian are

\[
\Theta_{\rm red}=p_\Psi d\Psi,
\qquad H_{\rm red}={p_\Psi^2\over12A}.
\]

Therefore the displayed ten-dimensional scalar phase block has

\[
N_{\rm scalar}={10-8\over2}=1.
\]

The same calculation about a nonzero longitudinal background replaces the
static quadratic term by

\[
k^2[(1-\lambda_\parallel)\Phi^2-2\Phi\Psi+\Psi^2],
\qquad
\lambda_\parallel=1+(y-1)e^{-y}>0.
\]

The bracket determinant and rank remain unchanged, while the solved
multiplier is \(\lambda_s=-\lambda_\parallel\Psi/k^2\) and

\[
H_{\rm red}={p_\Psi^2\over12A}
+A\lambda_\parallel k^2\Psi^2,
\qquad
\boxed{\omega^2={\lambda_\parallel\over3}k^2}.
\]

Thus the reduced scalar has positive kinetic and longitudinal gradient energy
for \(y>0\); it is not removed by the two multipliers. In the exact
exponential theory

\[
\omega^2=k^2{1+(y-1)e^{-y}\over3}
=k^2\left({2y\over3}-{y^2\over2}+O(y^3)\right).
\]

At \(y=0\), the exact cancellation of the quadratic spatial term sends this
sound cone to zero and spatial dynamics begins at order
\(|\nabla\Psi|^3/a_0\). At \(k=0\), all four Laplacian secondaries vanish and
the same formal bracket symbol drops from rank eight to rank zero. The
homogeneous sector therefore cannot be inferred from the local one.

## Homogeneous FLRW existence and principal-family follow-on

Direct variation of the flat-FLRW minisuperspace action gives

\[
3M_{\rm Pl}^2H^2=M_{\rm Pl}^2\Lambda+V+\rho,
\qquad
3M_c^2H+V'(T)=0,
\]
\[
{2M_{\rm Pl}^2\dot H\over N}
+\rho+p+{M_c^2\dot T\over N}=0.
\]

The two spatial-Laplacian multiplier equations vanish identically on the
homogeneous flat background. Consequently \(\bar\lambda_s(t)\) and
\(\bar\lambda_K(t)\) are arbitrary zero modes; setting them to zero is a
branch choice rather than an equation.

There is an explicit expanding vacuum witness. For

\[
V=V_0+{1\over2}m_T^2T^2,
\quad
V_0=-M_{\rm Pl}^2\Lambda,
\quad
m_T^2={3M_c^4\over2M_{\rm Pl}^2},
\]

take

\[
T=t-T_*,\qquad
H={M_c^2(T_*-t)\over2M_{\rm Pl}^2},\qquad
a(t)=a_*\exp\!\left[{M_c^2t(2T_*-t)\over4M_{\rm Pl}^2}\right].
\]

All three background equations vanish exactly, and \(H>0\) on \(t<T_*\).
This is an existence result, not a late-time cosmology fit.

On FLRW a geometry-motivated principal family promotes the ADM-generated
Minkowski block using \(\Theta=\dot\Psi+H\Phi\) and includes both arbitrary
multiplier zero modes. This promotion is not the complete quadratic FLRW
expansion. Its generated bracket gives

\[
\det\Delta=A^8(k/a)^{32},
\]

independent of \(H,\bar\lambda_s,\bar\lambda_K\), and its reduced Hamiltonian
is

\[
H_{\rm red}={p_\Psi^2\over12A}-H\Psi p_\Psi.
\]

Thus expansion and homogeneous multiplier freedom do not remove the scalar
pair inside this promoted family. Restarting directly at \(k=0\) instead gives
the lapse secondary \(Hp_\Psi\), proving that substituting \(k=0\) into the
finite-\(k\) bracket matrix is not a homogeneous Dirac analysis. Lower-
derivative terms are not included, so the FLRW conclusion is conditional.

## Precise strength and limitation of the obstruction

This calculation rejects a claim that the candidate already has a regular
two-tensor-only Minkowski/local-inertial perturbation theory at \(y=0\). It
exhibits an ultralocal/eaten-clock scalar and a linearization/constraint-rank
singularity exactly where \(\mu(0)=0\).

It is not yet a theorem that the full nonlinear covariant action propagates
three gravitational degrees of freedom on every background. The nonlinear
MOND constraint is irregular at zero field; an on-shell FLRW background can
have nonzero multiplier values; and lower-derivative cuscuton/background
terms were omitted from this principal block. They can change the secondary
constraints and must be included before making a full-action statement; the
nonzero principal determinant alone is not a substitute for that derivation.

## Verdict and next unavoidable calculation

- Exact target kernel from the frozen action: **passes the reduced static gate**.
- Independent \(\Phi,\Psi\), linear no slip: **passes only the reduced finite-\(k\) static gate**.
- Separate ordinary-matter Ward identity: **passes**.
- Expanding homogeneous FLRW solution: **exists exactly; viability against cosmological data is untested**.
- Controlled \(y=0\) two-tensor perturbation theory: **adverse in the ADM-generated principal block; full-action count still open**.
- Full theory: **OPEN, adverse; not fried chicken**.

The next unavoidable action calculation is the complete quadratic scalar ADM
action on the explicit on-shell FLRW solution, including the lower-derivative
cuscuton, potential, matter, lapse/measure, and multiplier-background terms.
Only then should the Dirac chain be rerun and followed by the nonlinear
constraint rank as \(\bar y\to0^+\). If the scalar pair survives there, this
frozen candidate is dead on the DOF/stability gates before a full preferred-
frame PPN expansion is worth doing.
