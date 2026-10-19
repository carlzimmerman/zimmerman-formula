# Full static J1 vector determinant on the relative mixed domain

The full ten-channel J1 vector operator has now been derived from the actual covariant Hessian and its mixed-boundary determinant evaluated. The seven-combination transverse determinant follows by the exact longitudinal/ghost spectral decomposition. The calculation uses the fixed-small-circle pure-SU2 BPS background and the common unbroken K=1,h=0 auxiliary reference; its different holonomy prevents identifying it with the physical QCD vacuum subtraction.

## Actual calculated finite determinants

Let Dvec denote the real vector determinant ratio per magnetic quantum number, and Dg=D_RE D_M the already exact complex-ghost determinant ratio per magnetic number. The full J1 Gaussian and transverse ratios are

\[
\mathcal Z_{J=1}=[D_g D_{\rm vec}^{-1/2}]^3,\qquad
D_T=D_{\rm vec}/D_g.
\]

Here DT is the determinant of the actual self-adjoint restriction to kerG relative to its reference restriction, not seven guessed scalar copies. All finite positive modes, including the lifted translation direction, remain in these unprimed determinants.

| x=m_W R | log Dvec | log DT | log Z_J1 |
|---:|---:|---:|---:|
| 2 | -1.71841054 | -1.50748284 | 1.94483271 |
| 4 | -2.44413650 | -2.72042047 | 4.49505667 |
| 6 | 0.62749397 | -1.24929169 | 4.68911602 |
| 8 | 6.32081522 | 2.16889429 | 2.97453994 |
| 10 | 13.45300332 | 6.63990626 | 0.25978618 |
| 12 | 21.47341507 | 11.75424634 | -3.05261641 |
| 16 | 39.18494813 | 23.19187181 | -10.79819322 |
| 20 | 58.30042900 | 35.64621398 | -19.48799845 |
| 24 | 78.3059 | 48.7456 | -28.7780 |

These are numerical approximations under declared finite stability tests, not interval-certified digits. The two independently varied origin/tolerance/step integrations differ by about4.0*10^-8 in relative determinant throughx16,8.4*10^-8 atx20 and2.23*10^-6 atx24. The roundoff condition estimate atx24 is1.03*10^-5, near the declared2*10^-5 threshold, so its displayed trailing digits must not be treated as certified. No further double-precision radius extrapolation is used.

## Exact operator and domains

DERIVATION.md gives the full construction; runs/derive-001/operator.json supplies the complete exact10x10 potential V_raw, constant angular Gram G, canonical transformation S, origin exponents and wall matrices. The Cartesian basis consists of seven spatial adjoint tensors and three A4 tensors. Every original Cartesian Hessian projection closes exactly, G V is symmetric, and an independent complete quaternion-intertwiner construction verifies both coefficients of H T=T M for all10 channels using scalar ghost J0,J1,J2. The principal intertwiner matrix has determinant1/6. The two invariant5blocks have3D+2R and4D+1R data.

Smooth Cartesian origin fields select reduced powers t^(l+1), where l=[0,0,1,1,1,1,2,2,2,3]. The actual relative wall fixes tangential spatial connection and A4 and sets background divergence to zero. In the raw tensor coordinates, T selects rows0,2,4,6,7,8,9, while N u=(u1,u0+u2+u3,-u4+u5). The wall conditions are exactly

\[
T u(x)=0,\qquad N[u'(x)+u(x)/x]=0.
\]

Thus the domain is7D+3R. The fundamental boundary determinant is

\[
F(x)=\det\begin{pmatrix}TSY(x)\\NS[Y'(x)+Y(x)/x]\end{pmatrix},
\qquad D_{\rm vec}=\frac{F(x)}{(5103/8)x^{20}}.
\]

The denominator is calculated exactly from the same wall functionals and the free regular origin columns. It includes every endpoint normalization. A common positive-origin-cutoff matrix determinant theorem followed by cancellation of shared centrifugal factors justifies this ratio. The source is the previously authenticated [Kirsten–McKane math-ph/0403050v1, Section4, equations40–42 and the following ratio](https://arxiv.org/abs/math-ph/0403050v1); no theorem for a regular interval is silently applied directly at the singular origin.

The translation variation solves H a=0 and G=0 in the bulk exactly, but its Dirichlet trace has an algebraic1/x defect and its normal Robin trace is exponential. It is therefore retained as a positive finite-wall state. DERIVATION.md also gives the first-order uniqueness/ghost-positivity argument excluding exact finite-wall vector zeros.

## Large-radius result and qualification

The exact far-field matrix separates four neutral channels with centrifugal values0,2,2,6 from six charged Coulomb channels with centrifugal values0,0,2,2,6,6. The charge projector commutes with the normal wall projector. Exact charged asymptotics and mixed-boundary algebra give a combined relative -2/x in logDvec. The neutral translation/gauge-gradient argument removes possible earlier neutral inverse powers.

**The inverse-radius coefficient is established within the stated auxiliary model.** The independent [kernel/rank audit](/Users/carlzimmerman/new_physics/zimmerman-formula/fine_structure_puzzle/qcd_completion/reviews/kernel_rank/RAW_DERIVATION_v1.md) closes the whole-space kernel and threshold ranks using [Kottke1310.2974v3, Theorem4.7](https://arxiv.org/abs/1310.2974v3) and the explicit hybrid-domain/weighted-adjoint bridges, including [1210.3275v5, Definition2.3 and Theorem2.4](https://arxiv.org/abs/1210.3275v5). REMAINDER_CONTROL.md supplies the actual exterior Green estimates and charge-adapted mixed-wall Schur complement. Together they give

\[
\log D_{\rm vec}=6x-22\log x+C_{\rm vec}-2/x+O(x^{-2}),
\]
\[
\boxed{\log\mathcal Z_{J=1}=-3x+15\log x+C_Z+3/x+O(x^{-2}).}
\]

The full finite determinant table does not depend on the infinity proof. The coefficient comes from operator/outer-mode/boundary algebra and the source-audited kernel argument, not a fit. The scalar ghost contributes no algebraic inverse-radius term in this reference. The executed asymptotic-003 output retains its original conditional wording: the subsequent hand kernel/rank and exterior remainder proofs close those named obligations without editing that run. Charged growing solutions can have algebraic neutral tails; the Schur proof explicitly controls them rather than discarding them. The coefficient concerns fixed asymptotic m_W and this auxiliary boundary matching path only.

## Provenance and first remaining gap

Authoritative completed records are runs/derive-001, runs/full-001, runs/full-002 and runs/asymptotic-003. Each has an immutable contract/code/output and a validated v2 manifest. The original asymptotic-001 run failed due to inconsistent symbolic assumptions when parsing t from JSON; asymptotic-002 failed because it compared structurally different exact rational expressions instead of their zero difference. Both are preserved; asymptotic-003 fixes the representation checks without changing the mathematics. Their failures are implementation evidence, not counterexamples.

The finite computations cover the actual full J1 vector Gaussian and its transverse restriction under the stated domain. They do not compute higherJ, nonzero Fourier modes, the common UV subtraction, a physical same-holonomy vacuum matching, or the strong-coupling/metric bridge to QCD. Physical A_rho, R(alpha) and an alpha root remain open. The weighted-domain/kernel, connection-rank and exterior remainder obligations for this J1 coefficient are closed in the linked hand proofs. The first remaining calculation is the higher-angular/Fourier determinant sum with a common UV subtraction and physical same-holonomy matching; the current J1 result does not supply it.

Final mathematical proofreading self-review covers only the two new reports: basis order, radial powers, ghost multiplicity, boundary determinant exponent and finite/conditional scope were checked. No mathematical-token proofreading correction was needed. This is separate from the Cartesian/quaternion algebra checks and independent source/rank audits.
