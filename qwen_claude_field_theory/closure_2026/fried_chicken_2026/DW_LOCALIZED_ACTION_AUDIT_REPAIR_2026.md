# Localized Deffayet–Woodard Action Audit Repair (2026-09-04)

## Result in one sentence

The unrestricted localized action is **DEAD** as a two-tensor-only theory: its
nondegenerate \((X,\xi)\) quadratic block has two scalar light-cone poles with
opposite kinetic residues.  A metric-only, retarded fixed-history reading is
**OPEN / noncanonical**, and the singular \(Q=0\) Legendre stratum is **OPEN**
until its full spatial, metric-coupled Dirac chain is restarted there.

An exit status of zero from either audit means only that the stated symbolic
claims were reproduced.  It is not a certification of the fried-chicken target.

## Audited action and claim boundary

The single local action audited here is

\[
S=\int d^4x\sqrt{-g}\left[
 \frac{R-a_0^2M}{\kappa}
 -\nabla_a\xi\nabla^aX
 -\xi R_{ab}u^a u^b
 +\lambda(u_a u^a+1)
 -(M+f(Z))u^a\nabla_a\nu
 +\mathcal L_m(g,\psi)
\right],
\]

where \(u_a=\nabla_a\phi\),
\(Z=4\nabla_aX\nabla^aX/a_0^2\), and \(Q=M+f(Z)\).
Ordinary matter is minimally coupled to the same metric.

This is a synthesized **local** representative of the DW auxiliary equations.
It is not automatically canonically equivalent to a metric-only functional
whose inverse d'Alembertian is assigned retarded data.  That history prescription
is boundary-condition data, not a constraint derived from this local Hamiltonian.

## 1. Curvature variation and Ward identity

For a fixed contravariant tensor \(V^{ab}\), the derivative part of the inverse-
metric variation of \(\sqrt{-g}V^{ab}R_{ab}\) is

\[
\mathcal D_{\mu\nu}[V]=
-\nabla_a\nabla_{(\mu}V_{\nu)}{}^a
+\frac12\Box V_{\mu\nu}
+\frac12g_{\mu\nu}\nabla_a\nabla_bV^{ab}.
\]

Here \(V^{ab}=-\xi u^a u^b\).  The previous audit used the opposite overall
sign for this block.  A direct Euler–Lagrange variation of four independent
metric functions \(N,A,C,D\) catches that error without referring back to the
hand-written covariant formula.

With the corrected sign, the local diffeomorphism identity is

\[
2\nabla^\mu E_{\mu\nu}+\sum_A E_A\nabla_\nu\Phi_A=0,
\qquad
\Phi_A=(X,\xi,\phi,\lambda,M,\nu,\psi).
\]

The brute-force audit passes all 26 checks for both a generic cubic \(f(Z)\)
and an undefined symbolic \(f\), including mutation controls.  On the auxiliary
shell, minimally coupled matter obeys

\[
\nabla^\mu T_{\mu\nu}=E_\psi\nabla_\nu\psi,
\]

and hence is conserved on its own matter equation.  This establishes the Ward
identity for the displayed local action, but not canonical equivalence to a
retarded metric-only nonlocal theory.

## 2. Generic \(Q\ne0\) Hamiltonian stratum

For the homogeneous frozen-metric auxiliary reduction,

\[
L=\frac{\dot X\dot\xi}{N}
+\lambda N\left(1-\frac{\dot\phi^2}{N^2}\right)
+Q\frac{\dot\phi\dot\nu}{N}-cMN,
\]

the exact velocity-Hessian determinant is \(Q^2/N^4\).  Thus the following
Legendre transform is valid only on the explicitly restricted chart \(Q\ne0\):

\[
H_c=N\left[p_Xp_\xi+\frac{p_\phi p_\nu}{Q}
+\lambda\left(\frac{p_\nu^2}{Q^2}-1\right)+cM\right].
\]

The primary constraints are
\(C_1=p_\lambda\) and \(C_2=p_M\).  Preservation gives denominator-free
secondaries

\[
C_3=p_\nu^2-Q^2,
\qquad
C_4=Qp_\phi p_\nu+2\lambda p_\nu^2-cQ^3.
\]

In the ordering \((C_1,C_2,C_3,C_4)\), the calculated Poisson matrix is

\[
\{C_A,C_B\}=\begin{pmatrix}
0&0&0&-2p_\nu^2\\
0&0&2Q&3cQ^2-p_\nu p_\phi\\
0&-2Q&0&0\\
2p_\nu^2&-3cQ^2+p_\nu p_\phi&0&0
\end{pmatrix}.
\]

It has

\[
\det\{C,C\}=16Q^2p_\nu^4,
\qquad
\det\{C,C\}\big|_{C_3}=16Q^6.
\]

Therefore all four constraints are second class at generic \(Q\ne0\); no
tertiary is produced before the multipliers are fixed.  The frozen homogeneous
auxiliary sector has \((12-4)/2=4\) canonical degrees of freedom.  This count is
not an ADM count and is not a claim about \(N_{\rm grav}\) in the full theory.

## 3. Singular \(Q=0\) stratum

No expression containing \(1/Q\) is used to analyze this stratum.  Returning to
the Lagrangian Hessian gives exact maximal-minor witnesses

\[
\operatorname{rank}H\big|_{Q=0,\lambda\ne0}=3,
\quad \det H_{3\times3}=\frac{2\lambda}{N^3},
\]

and

\[
\operatorname{rank}H\big|_{Q=0,\lambda=0}=2,
\quad \det H_{2\times2}=-\frac1{N^2}.
\]

The rank bifurcation proves that formally substituting \(Q=0\) into the generic
Hamiltonian chart is invalid.  It does **not** finish the \(Q=0\) Dirac analysis.
That branch remains OPEN and requires new primary constraints and their complete
preservation chain to be derived directly from the singular Lagrangian, with
spatial gradients and ADM metric variables retained.

## 4. Finite-\(k\), zero-mode, and retarded-energy audit

Around the fixed-background localization block, define \(f_1=f'(0)>0\).  The
quadratic kinetic matrix derived from the action is

\[
K=\begin{pmatrix}-8f_1/\kappa&1\\1&0\end{pmatrix},
\qquad \det K=-1.
\]

For \(k\ne0\),

\[
\det\mathcal O(\omega,k)=-(\omega^2-k^2)^2.
\]

There are two scalar light-cone channels and their residues have opposite signs.
Consequently the unrestricted localized theory contains a ghost scalar and is
DEAD for the requested two-tensor, stable construction.  The separate homogeneous
sector has \(\det\mathcal O(\omega,0)=-\omega^4\), not a license to discard it.
The clock/transport block independently has determinant \(-4\omega^4\), exposing
zero-frequency modes rather than Hamiltonian constraints.

For the DW normalization \(f'(0)=1/2\), the diagonal coefficient is
\(a=-4/\kappa\).  The equal-retarded particular branch has energy coefficient
\(-a/2=+2/\kappa\).  The old negative sign was incorrect.  This positive
restricted-branch value does not remove the opposite-residue pole of the
unrestricted local action: imposing retarded histories is an external solution
prescription, so that reading remains OPEN / noncanonical.

Exact past-source witnesses are evaluated in both \(k=1\) and \(k=0\) sectors;
both retain nonzero history data.  Therefore the zero mode cannot be silently
set to zero by the same local phase-space argument.

## 5. Status by mathematical object

| Object | Status | Exact reason |
|---|---|---|
| Unrestricted local representative | **DEAD** | Two finite-\(k\) scalar poles with opposite residues; generic homogeneous auxiliary sector has four canonical DOF. |
| Retarded fixed-history reading | **OPEN / noncanonical** | Its free data are removed by a history prescription, not by constraints generated from the audited Hamiltonian. |
| Singular \(Q=0\) branch | **OPEN** | Hessian rank bifurcates; the generic Legendre chart is invalid and the full Dirac chain has not been restarted. |
| Local-action matter Ward identity | **PASS (scoped)** | Off-shell identity and direct metric variations pass 26/26; minimally coupled matter is conserved on shell. |
| Full ADM \(N_{\rm grav}=2\) | **NOT COMPUTED** | A homogeneous frozen-metric auxiliary count cannot decide it. |

## 6. Reproduction and observed exits

Run from `qwen_claude_field_theory/closure_2026/fried_chicken_2026`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 test_dw_localized_repairs_2026.py
PYTHONDONTWRITEBYTECODE=1 python3 dw_localized_noether_identity_2026.py
PYTHONDONTWRITEBYTECODE=1 python3 dw_localized_dirac_count_2026.py
```

Post-repair exits were respectively 0, 0, and 0.  The two audit totals were
26/26 and 20/20.  Pre-repair failures and their exits are preserved in
`dw_localized_pre_repair_failures_2026.out`.

## 7. Next unavoidable calculation

To keep this architecture alive, derive a fresh ADM/Fourier Dirac chain directly
on \(Q=0\), separately for \(\lambda\ne0\) and \(\lambda=0\), including lapse,
shift, spatial metric, all new primaries, all secondary/tertiary preservation,
and the exact distributional Poisson operator at \(k\ne0\) and \(k=0\).  If the
intended theory instead keeps only retarded histories, it needs a genuine causal
variational framework (for example an explicitly doubled in-in construction)
and a proof that its reduced physical phase space and Ward identity reproduce
the metric-only retarded equations.  Without one of those calculations, an
\(N_{\rm grav}=2\) claim is not established.
