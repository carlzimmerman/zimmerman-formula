# IC-1: a constructive canonical identity and an expanding same-action branch

2026-09-08. Base `e9a8b4e05d48182947de4bd6d965960fa3428534`.
**The full gravity goal remains OPEN.** This package constructs and varies the
single action in [ACTION.md](ACTION.md); it is not a collection of exclusions.
No global novelty, empirical success, full PPN calculation or Lean proof is
claimed. The computation-audit workflow distinguishes exact identities,
finite numerical diagnostics and still-unproved physical implications.

**Subsequent same-day calculation:** IC-1's unmodified inhomogeneous scalar
has negative high-frequency kinetic energy. Its homogeneous claims below
remain valid but do not make IC-1 viable. The current constructed correction
and its explicitly limited scalar results are [IC-2](SCALAR_REPORT.md).
The pinned IC-1 code/output are preserved rather than rewritten as a success.

## 1. The concrete construction

Use the timelike varied clock T and auxiliary u defined in ACTION.md. Write
\(\pi=h_{ij}\pi^{ij}\). The kinetic modification is

\[
w=(u-1)\ln N,\quad W=n^\mu\nabla_\mu w,\quad
Q_{ij}=K_{ij}-h_{ij}W,
\qquad L_{\rm kin}=\frac m2N\sqrt h(Q_{ij}Q^{ij}-Q^2).
\]

In particular W includes **both** \((u-1)n\cdot\nabla\ln N\) and
\(\ln N\,n\cdot\nabla u\). The second term is fixed by integrability.
Differentiating the actual eight-velocity density gives

\[
\Psi_N=p_N+\frac{2(u-1)}N\pi,\qquad
\Psi_u=p_u+2\ln N\,\pi,
\qquad \{\Psi_N(x),\Psi_u(y)\}=0.
\]

The bracket is calculated over all six independent spatial metric coordinates
as well as N,u, not on a substituted background. Removing the second term
instead gives \(\{\Psi_N,p_u\}=2\pi/N\). This is a negative control for the
constructive identity, not a separate model advertised as the result.

The identity has a general-metric proof. The invertible point transformation
\(\bar h=e^{-2w}h\), with N,u retained, gives

\[
\pi^{ij}dh_{ij}+p_NdN+p_u du
=\bar\pi^{ij}d\bar h_{ij}+\Psi_NdN+\Psi_u du,
\quad\bar\pi^{ij}=e^{2w}\pi^{ij}.
\]

Thus these really are canonical auxiliary momenta. Its eight-coordinate
Jacobian determinant, calculated by the script, is \(e^{-12w}>0\) for N>0.
The six-metric-velocity block is the invertible DeWitt kinetic form; its
pullback through this point map has rank six and nullity two. SymPy computes
that rank and both null residuals in an orthonormal frame. Shift momenta are
also primary constraints; spatial covariance supplies the usual momentum
constraints, but their full functional Dirac chain is **not** replaced by
the pointwise Hessian calculation.

## 2. Auxiliary variation and the exponential branch

Put \(Q=K-3W\). The full u Euler equation, before specializing to static
fields, is

\[
\ln N\,\nabla_\mu(Qn^\mu)
 +u\{a_\mu a^\mu-a_0^2\ln^2(1-u^2)\}=0.
\]

This follows by integrating the variation
\(2mQ\,n\cdot\nabla(\ln N\,\delta u)\) by parts. The static branch
K=W=0, 0<u<1 then has

\[
u^2=1-e^{-y},\quad y=|a|/a_0,\qquad
f(a^2)=2a_0^2[1-(1+y)e^{-y}].
\]

The script differentiates U, varies u, eliminates its regular solution, and
checks the primitive and both asymptotic limits exactly. The endpoint is not
hidden: \(U(u^2)=-u^6/3-u^8/4+\cdots\), and the u equation at u=0 vanishes
on the static branch even for nonzero a. The boundary stationary branch and
its rank/selection require a separate treatment. The regular branch is not
a global uniqueness or stability theorem.

## 3. Independent static metric equations, with the clock source retained

For \(N=e^\Phi,h_{ij}=e^{-2\Psi}\delta_{ij}\), define
\(A_s=e^{\Phi-\Psi},B_s=e^{\Phi-3\Psi}\),
\(C=\Lambda+a_0^2U(u^2)\), and

\[
F=|\nabla\Psi|^2-2\nabla\Phi\cdot\nabla\Psi
 +(1-u^2)|\nabla\Phi|^2.
\]

Up to a spatial boundary term the exact conformal-static density is
\(mA_sF-mB_sC+\kappa e^{-\Phi-3\Psi}/2\).
Independent lapse and conformal spatial variations give, with
\(S_m=h^{ij}T^m_{ij}\),

\[
2m\nabla\cdot[A_s(\nabla\Psi-(1-u^2)\nabla\Phi)]
 +mA_sF-mB_sC=B_s(\rho_m+\kappa X),
\]
\[
2m\nabla\cdot[A_s(\nabla\Phi-\nabla\Psi)]
 -mA_sF+3mB_sC=B_s(S_m+3\kappa X).
\]

Their sum has source \(B_s[\rho_m+S_m+4\kappa X-2mC]\).
The canonical clock has pressure: its active source is **4 kappa X**, not
baryonic density. Conformal variations alone do not check every spatial
metric equation or construct a full stationary solution.

In the controlled leading weak-field limit, negligible pressure and
clock/vacuum terms and appropriate slip boundary data give separately

\[
\Delta(\Phi-\Psi)=0,\qquad
\nabla\cdot[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi]
 =\rho_b/(2m)=4\pi G_N\rho_b.
\]

Here \(G_N=1/(8\pi m)\) is extracted from the high-acceleration lapse
equation, not equated to a bare coupling in advance. Spherical integration
with a regular isolated source yields \(\mu g=G_NM_b/r^2\) and the usual
deep-MOND \(v^4=G_Na_0M_b\); these are conditional consequences of this
leading equation, not new empirical laws.

One sufficient ordering is potentials O(epsilon), a0 L=O(epsilon), regular
fixed y>0, |Lambda|L^2=o(epsilon) and
kappa Xbar L^2/m=o(epsilon). Matching that ordering to the actual cosmological
clock and every full metric/clock equation remains open. No beta, alpha_1,
alpha_2 or alpha_3 is assigned, and the conditional static slip result is not
advertised as a completed PPN calculation.

## 4. Exact homogeneous Dirac closure and expansion

In unitary T=t, let \(B=Ae^{-w}\). Direct Legendre transformation gives

\[
H=-\frac{p_B^2N^{4-3u}}{12mB}
  +mB^3N^{3u-2}[\Lambda+a_0^2U(u^2)]
  -\frac\kappa2B^3N^{3u-4}.
\]

Primaries are p_N,p_u. Their preservation gives -H_N,-H_u. The script
calculates every entry of their Poisson matrix. Where the actual Hessian
H_ab, a,b=N,u, is invertible, secondary preservation fixes both multipliers
and produces no tertiary constraint. The two-by-two inverse identity and
the substituted Hamiltonian/constraint derivatives are separately checked.

A nonempty exact branch exists. Set \(\ell=\ln(9/5),f=e^{-1/2}\) and choose

\[
u=\frac23,\quad N=e^{1/4},\quad
a_0^2=\frac{9\kappa f}{16m\ell^2},\quad
\Lambda=\frac{\kappa f}{m}-a_0^2U(4/9)>0.
\]
\[
B=B_0e^{\sqrt{\kappa/(6m)}t},\quad A=e^{-1/12}B,
\qquad H_{\rm physical}=e^{-1/4}\sqrt{\kappa/(6m)}>0.
\]

For a prescribed positive a0, choose kappa accordingly; this does not change
the exponential law. It is one parameter-compatible background, **not** a
universal prediction of the observed a0/Lambda ratio or a viable cosmic history.

In coordinates \(\xi=\ln N,u\), the secondary Hessian is
\(\kappa B^3 f M\), with the matrix derived from H:

\[
M=\begin{pmatrix}-4&9/2\\9/2&-9/4-18/(5\ell)\end{pmatrix},
\quad D=\det M=\frac{72}{5\ell}-\frac{45}4>\frac{27}4.
\]

The last strict bound follows from 0<ln(1+4/5)<4/5. The full four-constraint
matrix on this branch is \(\left(\begin{smallmatrix}0&H_{ab}\\-H_{ab}&0\end{smallmatrix}\right)\)
for constraints (p_a,-H_a), and has nonzero determinant. Consequently there
are four second-class constraints, no first-class constraints in this
clock-gauge minisuperspace system, and one homogeneous canonical pair.
The numerical rank is independently calculated by SVD at m=kappa=B=1;
its smallest singular value is about 0.48754. Rank/count are not script inputs.

The actual Schur complement, not the unreduced conformal kinetic coefficient,
gives

\[
(H_{\rm red})_{p_Bp_B}=\frac{3}{2mBfD}>0.
\]

All constraints, the B and p_B evolution equations and secondary drifts vanish
exactly after the branch substitution; dot N=dot u=0 follows from preservation.
This is a positive **homogeneous** reduced kinetic sign, not a local scalar
stability or gravitational-versus-matter mode classification.

## 5. Tensor and ordinary-matter checks

For TT perturbations on the homogeneous background, Q's change from K is pure
trace. Direct curvature/kinetic differentiation gives

\[
S_T^{(2)}=\frac m8\int NA^3
 [(\dot\gamma_{ij}/N)^2-A^{-2}(\partial_k\gamma_{ij})^2].
\]

Thus m>0 and physical tensor speed squared equals one in this principal block.
The script independently computes the spatial Ricci scalar for an exponential
TT polarization and differentiates both derivative coefficients. This is not
a full nonlinear characteristic analysis on arbitrary backgrounds.

For ordinary minimally coupled matter, diffeomorphism invariance of S_m alone
gives its own Ward identity on its own matter equations; no auxiliary stress
must be added to obtain conservation. The script explicitly differentiates
the stress tensor of a minimally coupled scalar psi with arbitrary first and
second jets, obtaining
\(\nabla_\mu T_m^{\mu\nu}=(\Box\psi-V')\nabla^\nu\psi\).
This tensorial identity holds in curved spacetime by normal coordinates and
commutation of scalar Hessians. For other matter, the same Noether argument
requires its own covariant action/equations.

The clock's canonical term alone instead has
\(\nabla_\mu T_T^{\mu\nu}=\kappa\Box T\nabla^\nu T\); its full equation
also includes the clock-dependent gravitational terms. No independent
Box T=0 is imposed in the dynamical theory.

## 6. The next coupled calculation (already being attacked)

The same point transformation gives the spatial Hamiltonian ingredient

\[
N^u[\bar R+4u\ln N\,\bar D\ln N\cdot\bar D u
             +2\ln^2N|\bar D u|^2].
\]

The pure lapse-gradient square cancels, but the mixed/u-gradient terms do not.
The script verifies this integration-by-parts identity. They must be retained
in the actual secondary functional Hessian and the scalar perturbation action
for **k!=0**. Homogeneous positivity cannot answer that question. Next: reduce
the shift/lapse/u equations on the displayed expanding branch, calculate all
scalar poles and kinetic/gradient signs, and derive any needed correction from
those equations while preserving the same static law and primary integrability.

Full functional closure, scalar/vector health, causality, zero-field branch
control, full PPN, global solutions and empirical cosmology remain unproved.
The explicit action is a construction candidate, not a final theory.

## 7. Attribution and independent checks

Lapse-velocity mixing and degeneracy are established ideas, not claimed here
as inventions. Related primary source checked: Langlois, Mancarella, Noui and
Vernizzi, *Effective Description of Higher-Order Scalar-Tensor Theories*,
[arXiv:1703.03797v2](https://arxiv.org/html/1703.03797v2), 2017-05-15,
especially introduction and Eq.1.2; accessed 2026-09-08. That source describes
degenerate lapse-derivative scalar-tensor frameworks. It does not certify this
extra-u action. Source classification: adjacent mechanism only. This was one
targeted primary-source query, not a novelty survey or exhaustive citation graph.

Three independent read-only workers derived the primary identity, static/tensor
equations and homogeneous branch. The retained script independently recomputes
their central identities; reviewer agreement itself is not a proof certificate.
The project's NavierStokesAndEuler-inspired blueprint supplies the separation
of fixed action/claims from computations and review, not a gravity theorem.
