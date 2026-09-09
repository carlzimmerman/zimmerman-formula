# Affine (F(Q)\Theta): local scalar Dirac gate

This gate is the next calculation after the homogeneous affine-charge result.
It is derived from the same candidate action as `fqtheta_gate.py`, on the
background-independent affine degeneracy locus

\[
 F_{QQ}=0,\qquad K_{QQ}=\frac{3F_Q^2}{2M^2}.
\]

It keeps the scalar metric perturbation \(\zeta\), the MOND auxiliary
perturbation \(\pi\), lapse \(n\), and scalar shift \(\beta\) for one spatial
Fourier mode.  The lower-derivative, no-velocity part is represented by its
local quadratic jet \(U_{zz},U_{\pi\pi},U_{n z},U_{n\pi},U_{nn}\).  The jet is
not used to assume a rank: the script differentiates the Hamiltonian and all
Poisson brackets symbolically.

## Exact principal Lagrangian

Writing \(\alpha=F_Q/(2M^2)\), \(Q_0=\bar Q\), and

\[
s=\dot\zeta-\alpha(\dot\pi-Q_0 n),
\]

the affine locus gives

\[
L_2=-3M^2s^2+2M^2 k^2\beta s+U.
\]

The velocity Hessian is

\[
W=\begin{pmatrix}-6M^2&3F_Q\\3F_Q&-3F_Q^2/(2M^2)\end{pmatrix},
\qquad \det W=0,
\]

which is the expected tuned null direction.  This is only a necessary kinetic
condition; it does not by itself remove a field.

## Dirac chain and actual Poisson matrix

The three primary constraints are

\[
p_\beta\approx0,\qquad p_n\approx0,\qquad
\Phi_0=p_\pi+\alpha p_\zeta\approx0.
\]

Preservation gives

\[
\begin{aligned}
\Phi_\beta&=\frac{k^2}{3}(2M^2k^2\beta-p_\zeta),\\
\Phi_n&=\alpha Q_0p_\zeta+U_n,\\
\Phi_0^{(2)}&=U_\pi+\alpha U_\zeta.
\end{aligned}
\]

The executable output records the full 6-by-6 antisymmetric bracket matrix.
Its determinant is

\[
\det C=\frac{k^{12}}{36M^2}\Big[
-F_Q^2U_{nn}U_{zz}+F_Q^2U_{nz}^2k^2
 +4F_QM^2U_{n\pi}U_{nz}k^2
 -4M^4U_{nn}U_{\pi\pi}+4M^4U_{n\pi}^2k^2
\Big]^2.
\]

For the GR-compatible local jet \(U_{nn}=U_{n\pi}=0) with nonzero lapse-
curvature mixing \(U_{nz}\ne0), this is nonzero for every \(k\ne0).  The
constraint Jacobian and bracket matrix both have rank six on the exact sample
evaluated by the script.  Hence all six constraints are second class, the
chain closes with no tertiary constraint on this open stratum, and

\[
N_q=4,\quad N_{\rm SC}=6,\quad N_{\rm FC}=0
\quad\Longrightarrow\quad N_{\rm scalar}=1.
\]

This is a propagating MOND-sector scalar, not an auxiliary removed by the
affine tuning.  It violates the requested “no hidden propagating auxiliary
scalar” gate unless \(\pi\) is promoted to an explicitly counted matter field.

## (k=0) versus (k\ne0\)

At \(k=0\), \(\Phi_\beta\) and the spatial-gradient part of
\(\Phi_0^{(2)}\) vanish identically.  With the lapse kept as a multiplier
\((U_{nn}=0)\), the active constraints are

\[
p_\beta,\ p_n,\ p_\pi+\alpha p_\zeta,\ \alpha Q_0p_\zeta,
\]

and the computed bracket rank is zero: all four are first class in this
principal homogeneous jet, giving zero scalar configuration degrees of
freedom.  Thus the scalar count jumps from zero at \(k=0\) to one at every
generic \(k\ne0\).  The reduced symplectic form makes the singular limit
explicit:

\[
\Omega_{\zeta\pi}=\frac{U_{nz}}{Q_0}k^2,
\qquad
H_{\rm red}=-\frac{k^2}{2}(U_{\pi\pi}\pi^2+U_{zz}\zeta^2).
\]

The reduced characteristic polynomial is

\[
\lambda^2+\frac{Q_0^2U_{\pi\pi}U_{zz}}{U_{nz}^2}=0,
\]

so the local mode has a \(k\)-independent gap (or an exponential instability
when the product has the opposite sign), while its symplectic coefficient
collapses as \(k^2\to0\).  This is a non-uniform/strong-coupling warning even
before the omitted khronon/aether sector is restored.

## Status and scope

The affine route remains **OPEN**, but it does not close the grand-prize
requirements.  The calculation is an exact obstruction for the displayed
local scalar principal sector: generic nonzero modes retain one scalar.  It is
not a universal no-go for every relativistic MOND action, and it does not yet
include the khronon/aether scalar, vector/tensor principal symbols, PPN
parameters, or matter Ward identity.  Those omissions are precisely why the
overall candidate cannot be marked closed.

Reproduce with:

```sh
python3 -B qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/fqtheta_adm_scalar_dirac.py \
  --output qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/run_001/adm_scalar_dirac.json
python3 -B -m unittest discover \
  -s qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026 \
  -p 'test_*.py' -v
```
