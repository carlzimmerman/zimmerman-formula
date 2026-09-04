# HPI-Delta: action lift, bounded Dirac chain, and final obstruction

Status: **DEAD as an exact classical regular-center theory**. Several intermediate gates pass, but the exact zero-field law produces divergent physical curvature in smooth positive-density cores. The action is therefore not a complete fried-chicken theory.

## 1. One explicit action

The configuration-space ADM action obtained by exact Legendre transformation of the committed HPI-$\Delta$ Hamiltonian is

\[
S=\frac{M_{\rm Pl}^2}{2}\int dt\,d^3x\,N\sqrt h
\left[
\bar K_{ij}\bar K^{ij}-\bar K^2+{}^{(3)}R-2\Lambda
-\frac{2}{\ell_0^2}F_{\exp}(y)
\right]+S_m[g,\psi],
\]

\[
\bar K_{ij}=K_{ij}-\frac{D^2\lambda}{2N}h_{ij},\qquad
y=\ell_0\sqrt{h^{ij}D_i\ln N D_j\ln N},
\]

\[
F_{\exp}(y)=2[(1+y)e^{-y}-1],\qquad \ell_0=\frac{c^2}{a_0}.
\]

One clock-covariant notation for the same unitary-gauge expression is

\[
X=-g^{\mu\nu}\nabla_\mu T\nabla_\nu T>0,
\quad n_\mu=-\frac{\nabla_\mu T}{\sqrt X},
\quad h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu,
\]

\[
b=\sqrt X D^2\lambda,\qquad
y=\ell_0\sqrt{a_\mu a^\mu},
\]

\[
S=\frac{M_{\rm Pl}^2}{2}\int d^4x\sqrt{-g}
\left[R-2\Lambda-\frac2{\ell_0^2}F_{\exp}(y)
+2Kb-\frac32b^2\right]+S_m[g,\psi].
\]

Here \(D\) is the induced spatial connection. In unitary gauge \(T=t\), \(\sqrt X=1/N\) and \(b=D^2\lambda/N\). This is a covariant notation and exact unitary-gauge bridge, not a completed nonlinear covariant Dirac proof.

The coefficient \(-3b^2/2\) is load-bearing. Removing it fails to reconstruct the first-order constraint Hamiltonian.

## 2. Euler–Lagrange equations and Legendre bridge

The exact metric-momentum elimination gives

\[
{\cal H}_{\rm kin}=\frac{2N}{M_{\rm Pl}^2\sqrt h}
\left(\pi_{ij}\pi^{ij}-\frac12\pi^2\right)
+(D^2\lambda)\pi,
\]

with zero symbolic residual against the committed first-order action.

Variation with respect to \(\lambda\) gives

\[
D^2\!\left[M_{\rm Pl}^2\left(K-\frac{3D^2\lambda}{2N}\right)\right]=0
=-D^2\!\left(\frac{\pi}{\sqrt h}\right).
\]

The unitary-gauge Hessian with respect to \(\dot\lambda\) is zero, so this auxiliary is elliptic at this level rather than a propagating scalar.

For minimally coupled matter, separate diffeomorphism invariance of \(S_m\) gives

\[
\nabla_\mu T_m^{\mu\nu}=E_\psi\nabla^\nu\psi,
\]

and hence \(\nabla_\mu T_m^{\mu\nu}=0\) on the matter equations. This is ordinary-matter conservation, not conservation of a combined effective stress.

## 3. Independent weak-static variations

Before imposing slip, variation of the reduced weak action gives

\[
E_\Phi=
2\nabla^2\Psi
-2\nabla\!\cdot(e^{-y}\nabla\Phi)
-8\pi G\rho=0,
\]

\[
E_\Psi=2\nabla^2(\Phi-\Psi)=0.
\]

Isolated boundary data select \(\Phi=\Psi\) on this leading static-dust branch. Substitution into the independently varied \(E_\Phi\) equation yields

\[
\nabla\!\cdot\left[\left(1-e^{-\lvert\nabla\Phi\rvert/a_0}\right)
\nabla\Phi\right]=4\pi G\rho.
\]

This establishes leading static no slip and exact AQUAL in the bounded branch. It does not by itself calculate the standard 1PN parameter \(\gamma_{\rm PPN}\), and it supplies none of \(\beta,\alpha_1,\alpha_2,\alpha_3\).

## 4. Generated finite-\(k\) Dirac chain

For scalar coordinates

\[
Q=(\Phi,\Psi,B,E,\eta),\qquad
P=(p_\Phi,p_\Psi,p_B,p_E,p_\eta),
\]

the program generates, rather than presupposes, the chain

\[
\begin{aligned}
&p_\Phi,\quad p_B,\quad p_\eta,\\
&C_N=2Ak^2[(1-\lambda_\parallel)\Phi-\Psi]-J_\rho,\\
&C_B=-p_E,\qquad C_\pi=-k^2p_\Psi,\\
&S=2Ak^4(\Phi-\Psi),\\
&Q=-4A^2k^8\lambda_\parallel\eta,
\end{aligned}
\]

where

\[
\lambda_\parallel=1+(y-1)e^{-y}>0\quad(y>0).
\]

Preservation through the last stage produces no further independent constraint. Removing the two spatial-diffeomorphism null directions, the actual six-dimensional second-class Poisson block in the order \((p_\Phi,p_\eta,C_N,C_\pi,S,Q)\) is

\[
\Delta=\begin{pmatrix}
0&0&2Ak^2(\lambda_\parallel-1)&0&-2Ak^4&0\\
0&0&0&0&0&4A^2k^8\lambda_\parallel\\
-2Ak^2(\lambda_\parallel-1)&0&0&2Ak^4&0&0\\
0&0&-2Ak^4&0&-2Ak^6&0\\
2Ak^4&0&0&2Ak^6&0&0\\
0&-4A^2k^8\lambda_\parallel&0&0&0&0
\end{pmatrix}.
\]

Its computed witness is

\[
\det\Delta=256A^8k^{32}\lambda_\parallel^4.
\]

For the full restored scalar phase space, the computed results are:

- phase-space dimension: 10;
- independent-constraint Jacobian rank: 8;
- Poisson rank: 6;
- first-class constraints: 2;
- second-class constraints: 6;
- scalar configuration degrees of freedom: \((10-2\times2-6)/2=0\).

The ranks, nullspace, witness minor, and degree count are outputs of the symbolic matrices; they are not supplied as target inputs.

## 5. Separate homogeneous \(k=0\) restart

On homogeneous flat FLRW, \(a_\mu=0\), \(D^2\lambda=0\), and \(F_{\exp}(0)=0\). The background reduces to Einstein gravity:

\[
L_{\rm FLRW}=-\frac{3M_{\rm Pl}^2a\dot a^2}{N}
-M_{\rm Pl}^2\Lambda Na^3.
\]

The homogeneous canonical restart generates

\[
p_N\approx0,\qquad p_{\lambda_0}\approx0,
\]

\[
{\cal C}_0=-\frac{p_a^2}{12M_{\rm Pl}^2a}
+M_{\rm Pl}^2\Lambda a^3\approx0.
\]

Their computed Jacobian rank is three and their Poisson matrix has rank zero. All three are first class, with zero homogeneous gravitational configuration degrees of freedom in this minisuperspace sector. Preservation closes, and the lapse equation gives

\[
H^2=\frac\Lambda3,
\]

so the action does not force \(H=0\). This proves background existence, not inhomogeneous FLRW scalar stability.

## 6. Tensor and high-acceleration blocks

On homogeneous FLRW the auxiliary terms do not couple to transverse-traceless perturbations. Per polarization,

\[
L_{\rm TT}=\frac{M_{\rm Pl}^2a^3}{8N}\dot h_T^2
-\frac{M_{\rm Pl}^2Na}{8}k^2h_T^2.
\]

The kinetic coefficient is positive and \(c_T^2=1\) in this quadratic block.

As \(y\to\infty\),

\[
F_{\exp}\to-2,\qquad F'_{\exp},F''_{\exp}\to0,
\]

so the formal local action tends to GR in constant-mean-curvature gauge with \(\Lambda_{\rm eff}=\Lambda-2/\ell_0^2\). This is not a global Solar-System matching or full PPN calculation. The \(a_0\)-\(\Lambda\) relation is an input, not derived.

## 7. Exact zero-field obstruction

The finite-\(k\), positive-gradient Dirac result does not extend regularly to \(y=0\): both constitutive eigenvalues vanish there and the Poisson rank bifurcates. A sourced quadratic expansion exactly at zero field demands \(J_\rho=0\), while the full nonlinear spherical flux does have a finite-action weak solution.

The nonlinear result is nevertheless fatal to a classical regular center. For \(\rho(r)=\rho_0+O(r^2)\),

\[
g(r)=\sqrt{\frac{4\pi}{3}Ga_0\rho_0\,r}+O(r),
\]

and the no-slip Ricci scalar diverges as \(r^{-1/2}\). An Einstein-plus-phantom-density rewrite inherits an integrable \(r^{-1/2}\) effective-density cusp. The accompanying executable theorem is in `../exact_mond_regular_center_no_go_2026/`.

This is the exact obstruction. A regulator \(\mu(0)>0\) restores finite curvature but changes the demanded law. An external field makes the geometric center non-force-free and breaks the isolated spherical branch, but it need not eliminate displaced critical points; their existence and regularity are not analyzed here.

The standard external-field branch is independently adverse. Because the same candidate's derived static equation is exact AQUAL, its Galactic-external-field Solar-System branch is the boundary-value problem solved in `../exact_exponential_aqual_q2_2026/`. At the frozen parameters that direct nonlinear solve gives

\[
|Q_2|=(2.093\pm0.030_{\rm num})\times10^{-26}\ {\rm s^{-2}},
\]

or \(4.025\) times the stated positive two-sigma Cassini ceiling. The solver reproduces the published exact-AQUAL exponential-kernel benchmark to \(0.087\%\). Thus adding the measured external field makes the geometric center non-force-free but does not rescue this unscreened exact-AQUAL branch. This statement does not assume that all displaced critical points disappear. An action-derived Solar-System screening mechanism would be a new candidate, not a property established by the action above.

## 8. Gate verdict

| Requirement | Result from this same candidate |
|---|---|
| exact \(\mu=1-e^{-y}\) | derived on the weak-static branch |
| \(N_{\rm grav}=2\) | zero scalar pair only in the bounded finite-\(k\) chain; full nonlinear covariant count not proved |
| \(\Phi=\Psi\) | derived at leading static-dust order |
| full PPN | uncomputed; no value is inferred from instantaneous response |
| ordinary matter Ward identity | derived from separate minimal \(S_m\) |
| \(c_T=c\), positive tensor kinetic term | derived on homogeneous quadratic TT block |
| expanding FLRW | de Sitter background and homogeneous Dirac restart pass |
| full stability | unproved; regular-center curvature gate fails |
| controlled \(y=0\) | fails as a classical \(C^2\) physical metric |
| standard-external-field Solar branch | direct exact-AQUAL \(Q_2\) exceeds the stated positive two-sigma ceiling by \(4.025\times\) |
| Newtonian/GR recovery | formal high-\(y\) local limit only |
| one physical matter/light metric | yes in the written action |
| \(a_0\)-\(\Lambda\) relation | not derived |

Final classification: **DEAD**, specifically as an exact classical regular-center theory. The wider architectural class remains logically open if the exact law is relaxed at zero field or nonclassical weak metrics are admitted.

## 9. Reproduction

From this directory:

```bash
python3 -m unittest -v test_hpi_delta_covariant_lift_2026.py
python3 hpi_delta_covariant_lift_2026.py
```

The script imports the committed HPI-$\Delta$ action gate for the finite-\(k\) matrix and explicitly checks that the new configuration action Legendre-transforms back to that same Hamiltonian.
