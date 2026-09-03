# CDE-L4C MOND — corrected status: OPEN / not a full-action certificate (2026-09-03)

The CDE-L4C directory contains a promising architecture, but it does not yet
contain one frozen nonlinear action whose complete Dirac chain, weak-field
equations, PPN parameters, FLRW branch, and perturbative stability have all
been derived together. In particular, the old claim that the displayed
cuscuton argument plus a four-constraint matrix established
\(N_{\rm grav}=2\) is withdrawn.

The architecture combines Einstein gravity, a cuscuton-like dark-energy
sector, lapse-gradient exponential MOND, a proposed no-slip constraint, and
four Laplacian auxiliary constraints. The independently reproducible pieces
are useful ingredients, not a closed theory.

## What survives

1. **Exact constitutive kernel.** Because Einstein gravity already supplies
   the Newtonian \(y^2\) term, the added function may be chosen as
   \[
   F'(y)=-2y e^{-y},\qquad F(y)=2(1+y)e^{-y}+C,
   \]
   so that
   \(1+F'(y)/(2y)=1-e^{-y}\). The combined small-\(y\) stiffness is
   \((2/3)y^3+O(y^4)\), while the correction decays exponentially at large
   \(y\).

2. **Velocity-free lapse-gradient term.** With
   \(y=c^2|D_i\ln N|/a_0(\chi)\), the MOND term contains no time derivative
   of the ADM variables or of \(\chi\). It does not itself change the kinetic
   Hessian.

3. **Linear no-slip identity as an ingredient.** The proposed
   \(C_{\rm slip}=3{}^{(3)}R-4D^2\ln N\) reduces to a Laplacian of
   \(\Psi-\Phi\) on the stated weak-field branch and vanishes on homogeneous
   FLRW. This has not yet been obtained as part of a closed full-action
   multiplier chain with both potentials sourced.

4. **Possible acceleration-scale constitutive relation.** The ansatz
   \(a_0^2(\chi)=G V(\chi)/4\) reproduces
   \(a_0=(c/2)\sqrt{G\rho_\Lambda}\) when
   \(V=\rho_\Lambda c^2\). This remains an imposed constitutive choice, not a
   derived cosmological prediction.

## What the corrected cuscuton calculation says

Let
\[
A=\dot\chi-N^iD_i\chi,\qquad S=D_i\chi D^i\chi,
\]
and use
\[
L_{\rm cusc}=\sqrt\gamma M^2\sqrt{A^2-N^2S}-N\sqrt\gamma V(\chi).
\]
Then
\[
p_\chi={\sqrt\gamma M^2 A\over\sqrt{A^2-N^2S}},\qquad
{\partial p_\chi\over\partial\dot\chi}
=-{\sqrt\gamma M^2N^2S\over(A^2-N^2S)^{3/2}}.
\]
For \(S>0\) the one-variable Legendre map is invertible. On its positive
timelike branch,
\[
\dot\chi=N^iD_i\chi+{Np_\chi\sqrt S\over
\sqrt{p_\chi^2-\gamma M^4}},
\]
and
\[
H_{\rm cusc}=N^i p_\chi D_i\chi
+N\sqrt S\sqrt{p_\chi^2-\gamma M^4}+N\sqrt\gamma V.
\]
The momentum approaches \(\sqrt\gamma M^2\) at large positive velocity but
diverges at the timelike/null boundary, so it is not globally bounded. At
\(S=0\), the Hessian vanishes and the positive branch has
\(p_\chi-\sqrt\gamma M^2\approx0\). Thus the displayed Legendre rank changes
between the homogeneous and inhomogeneous sectors. Standard cuscuton
nonpropagation may still emerge from the *complete coupled gravity analysis*;
it is not proved by the old one-variable argument.

## Why the old four-constraint certificate is insufficient

The script `gateA/cde_l4c_covariant_dirac_rank.py` declares only
\((\Phi,\Psi,B,\lambda)\) and their momenta. It omits
\((\chi,p_\chi)\), assigns a principal \(C_{\rm MOND}\) surrogate rather
than deriving it from one frozen nonlinear Hamiltonian, and does not close
the nonzero momentum-constraint brackets on constraints.

Its displayed determinant is genuinely computed,
\[
\det\Delta=c_s^2 k^8
\left(2B_p+\lambda_\parallel a_0^2\right)^2,
\]
but this means generic rank four only inside that truncated subsystem. The
rank drops to two on
\(B_p=-\lambda_\parallel a_0^2/2\). Neither the generic submatrix rank nor
its nonzero sourced-potential solution is a full-action DOF count.

## Unavoidable next calculation

Freeze one nonlinear ADM action and run the Dirac algorithm including lapse,
shift, metric, cuscuton, and every auxiliary/multiplier canonical pair. List
all primaries, preserve them through closure, compute the functional PB
matrix without preassigning its rank, and analyze \(k=0\) separately from
\(k\ne0\). Only if that yields exactly two tensor modes should the same action
be taken through independent \(\Phi\) and \(\Psi\) equations, the matter Ward
identity, boosted PPN, FLRW, and stability.

**Verdict: OPEN / NOT CERTIFIED.** The executable correction is
`cde_l4c_cuscuton_legendre_audit_2026.py`; a zero exit status means its
diagnostic claims reproduced, not that CDE-L4C passed the fried-chicken gates.
