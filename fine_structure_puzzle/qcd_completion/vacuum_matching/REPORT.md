# Physical reference matching: full neutral caloron and a screened charged exterior

FSP-004, physical-vacuum-matching assignment. Earlier inputs are frozen. **The common-holonomy neutral-caloron reference can be fixed; the finite-ball isolated-monopole determinant cannot be inferred from it.** Two additional calculations identify the missing long-distance prescription: the known complete caloron measure has a logarithmic inverse-*separation* correction, and an explicitly screened Abelian monopole exterior has exponential scalar wall dependence but an unscreened magnetic inverse-*radius* term. Neither is the cosmological vacuum stress.

## 1. First discriminator: a full all-mode source-to-target calculation

Use Diakonov–Gromov–Petrov–Slizovskiy (DGPS), [hep-th/0404042v2](https://arxiv.org/abs/hep-th/0404042v2), equations (54)–(56), (70), (74), (83)–(84), in the exact 10 April 2004 revision. Its background is the neutral SU(2) KvBLL caloron on spatial **R3** times a periodic circle of circumference L=1/T. The Green-function trace includes all angular and circle-frequency modes. The vector Hessian is in background Lorenz gauge, the ghost is a complex adjoint ghost, and the eight exact collective zero modes are removed from the vector determinant and restored through the moduli metric. No outer spatial wall is present.

Set d=r12, D=dT, nu=v/(2pi T), vbar=2pi T-v. Hold 0<nu<1 fixed and require D>>1, vd>>1 and vbar d>>1. The complete leading measure density, per d3z1 d3z2, has the form

\[
w_0={\cal N}(T,g,\Lambda)\,
\nu^{8\nu/3}(1-\nu)^{8(1-\nu)/3}
e^{-VP(v)}
\exp\{-2\pi D[2/3-4\nu(1-\nu)]\},
\]

where the source fixes the Pauli–Villars normalization N and
P(v)=v^2 vbar^2/(12 pi^2 T). This is an action density per three-volume. The source normalizes determinants initially to zero background. Dividing by the perturbative vacuum at the **same constant holonomy** multiplies this measure by exp[VP(v)]. A constant connection has no field strength or derivative terms; therefore this removes precisely its GPY volume term in the same regulator. It leaves the separation interaction intact. This construction is a neutral infinite-space common-holonomy benchmark, not the earlier K=1,h=0 finite-ball reference.

Including the moduli Jacobian, the controlled next term is

\[
\boxed{\log(w/w_0)=
{1\over D}\left\{ {4\over3\pi}
\log[4\nu(1-\nu)D^2]+c\right\}+O(D^{-2}),}
\qquad
c={74\over9\pi}+{8\gamma_E\over3\pi}-{23\pi\over54}.
\tag{M1}
\]

This is the analytic expression in the source's equation (84), now with the physical length distinguished from the ball radius. It is **not** a constant coefficient divided by a cosmological radius. At the center holonomy nu=1/2, its numerator is 8 log D/(3pi)+c, with the displayed analytic constant evaluating to c=1.76908473346655857… . The source instead prints the decimal 1.946 beside that expression, an internal inconsistency. We retain the analytic expression: differentiating equation (55) reproduces equation (54) exactly. Independently, adding the constants from the source's core and far integrals gives 2pi/27-pi/2=-23pi/54 and (46+4)/(9pi)=50/(9pi) in the derivative, fixing the same analytic coefficient upon integration. This checks consistency of the printed formulas, not a fresh derivation of the Green function. In undeformed Yang–Mills the leading center-holonomy separation factor is exp(+2pi D/3); its integral over separation diverges. It does not define a finite dilute caloron fugacity there.

There is a normalization-sensitive cancellation before (M1). Put a=v/T, b=vbar/T. The determinant correction in equation (55) is

\[
F(D)={1\over D}\left\{{1\over a}+{1\over b}-c
-{4\over3\pi}\log(abD^2/\pi^2)\right\}.
\]

The zero-mode Jacobian in constituent-position variables contributes
log(J/J0)=(1/a+1/b)/D+O(D^-2), since a+b=2pi. The Gaussian factor has **minus** F and the Jacobian has **plus** this term; the individual inverse-core-mass pieces cancel. This checks the all-mode/zero-mode prescription rather than assigning a radial coefficient. Adding the old four-zero-mode ball normalization would double count unrelated measures.

Important source qualification: the paper constructs its full Green function analytically, but its equation (46), used for the interpolation/normalization in equation (47), is checked numerically rather than proved analytically there. The controlled inverse-separation expression (54)–(56) is separately obtained from the stated current integrals. We have authenticated and translated these results, not independently rebuilt that Green-function calculation.

## 2. Why this does not fix the physical finite-wall determinant

DGPS equation (70) explicitly limits det'(W)=det(-D2)^4 to the appropriate decay and Hilbert space, and explicitly excludes a single BPS dyon with Coulomb asymptotics. Its R in the core/far separation is an **intermediate matching cutoff** satisfying core size << R << d, and cancels in the neutral answer. It is not an outer boundary. Equation (24) integrates the infinite-space single-dyon current over a ball; no chosen finite-wall Green function or self-adjoint gauge boundary problem is thereby supplied. Its cutoff dependence cannot be promoted to a finite-ball spectral determinant.

A smooth unit monopole also carries magnetic flux through the wall. Specifying a nonzero Higgs/holonomy magnitude alone does not equate that boundary sector to the zero-flux vacuum. To define a charged insertion one must specify the induced gauge/Higgs data or boundary state, framed gauge group, ghost/antighost prescription, boundary action and collective-coordinate/lifted-mode treatment. To define a vacuum one must instead say how magnetic neutrality and the surrounding ensemble are imposed. The fixed-wall versus fixed-asymptotic Higgs distinction in the frozen phase-block calculation remains real; none of these infinite-space formulas chooses that finite-wall path.

## 3. Deformed GPY subtraction: an actual nonuniform-tail test

Take the explicit SU(2) double-trace deformation from [Unsal–Yaffe, 0803.0344v2](https://arxiv.org/abs/0803.0344v2), equations (2.4)–(2.5). Denote its fixed dimensionless coefficient by a_def, with no target fit. For a local eigenvalue difference q,

\[
V_{\rm eff}(q)=P(q)+4a_{\rm def}T^3\cos^2(q/2T),
\quad V_{\rm eff}''(\pi T)=T(2a_{\rm def}-1/3).
\tag{M2}
\]

Local center stability requires a_def>1/6 in this one-loop SU(2) potential. This is a local condition; no global-minimum assertion is needed. The vacuum subtraction is V_eff(q)-V_eff(v). Subtracting the **whole field-dependent** V_eff(q) would change the theory, rather than normalize its vacuum.

Evaluate only this local potential on the declared undeformed BPS tail q=v-1/r, outside a fixed core cutoff r0 where q stays in the same GPY branch. For the GPY quartic the exterior primitive is exactly

\[
4\pi\int^R dr\,r^2[P(v-1/r)-P(v)]
=-2\pi P'(v)R^2+2\pi P''(v)R
-{2\pi\over3}P'''(v)\log(R/r_0)-{\pi P''''(v)\over6R}+C.
\tag{M3}
\]

At v=pi T, adding the deformation gives

\[
\boxed{\Delta S_{\rm potential}(R)=
2\pi T(2a_{\rm def}-1/3)R
+{\pi a_{\rm def}/3-1/(3\pi)\over TR}
+C+O((TR)^{-3}).}\tag{M4}
\]

The inverse-radius term in (M4) is **potential only**, not a full determinant coefficient: derivative terms and the changed saddle have not been evaluated. The linear term is the decisive mismatch. At fixed a_def>1/6 the Coulomb scalar tail is not the large-distance saddle of the deformed theory.

With the leading kinetic normalization kappa=L/g^2, the scalar screening mass is

\[
m_h^2=V_{\rm eff}''(\pi T)/\kappa
=g^2T^2(2a_{\rm def}-1/3).
\tag{M5}
\]

The correct exterior equation is q''+2q'/r=V_eff'(q)/kappa, coupled to the magnetic core; its linearized decaying solution has q-v proportional to exp(-m_h r)/r. At weak g and fixed positive curvature there is a near/far overlap mW^-1 << r_c << m_h^-1, with mW=pi T. The BPS core is useful there, but the fixed-g limit R→infinity necessarily reaches the screened region. This is a specific failure to interchange limits, not a no-go for semiclassics. Unsal–Yaffe's leading fugacity scaling and dimensionless prefactor do not supply its finite-geometry completion.

## 4. Additional calculation: a completely specified screened exterior

Here is a solvable matching component with no assigned coefficient. Fix r_c, psi_c, kappa, m>0; impose psi(r_c)=psi_c, psi(R)=0, with psi=q-v and magnetic field B=1/r^2 (flux 4pi in the BPS field conventions). Define the exterior action, with the uniform vacuum potential removed, by

\[
S_{\rm ext}=4\pi\int_{r_c}^{R}dr\,r^2
\left[{\kappa\over2}(\psi'^2+B^2)
+{\kappa m^2\over2}\psi^2\right].
\tag{M6}
\]

This is a declared linear Abelian EFT calculation. It contains no fluctuation determinant and no finite UV counterterm is chosen. The matching radius is an input separating the exterior from the uncomputed core. The solution and action are

\[
\psi(r)={\psi_c r_c\sinh[m(R-r)]\over r\sinh[m(R-r_c)]},
\quad
S_\psi(R)=2\pi\kappa\psi_c^2r_c
\{1+mr_c\coth[m(R-r_c)]\},
\]
\[
S_B(R)=2\pi\kappa(1/r_c-1/R).
\tag{M7}
\]

For this **charged insertion with fixed core boundary values**, its exterior log-weight relative to infinite radius is therefore

\[
\boxed{\delta\log w_{\rm ext}(R)=
{2\pi\kappa\over R}
-2\pi\kappa\psi_c^2r_c^2m
\{\coth[m(R-r_c)]-1\}.}\tag{M8}
\]

The scalar term is exponential for m(R-r_c)>>1. The magnetic term remains algebraic because this model fixes an unscreened net magnetic charge. Sending m→0 first instead gives S_psi=2pi kappa psi_c^2 r_c R/(R-r_c). The massless and screened large-radius expansions are different. Magnetic plasma screening or neutral exterior fields change the boundary problem and are deliberately not imported here.

One can also extract a leading conditional core-cloud action. Match a unit scalar-charge Yukawa tail psi=-exp(-mr)/r to the BPS core H≈v_core-1/r in the overlap. Its constant term fixes v_core=v+m+o(m). The core action through r_c is 4pi kappa(v_core-1/r_c), the magnetic exterior is 2pi kappa/r_c, and its scalar exterior is 2pi kappa exp(-2mr_c)(m+1/r_c). Adding and expanding gives

\[
\boxed{S_{\rm core+cloud}=4\pi\kappa v+2\pi\kappa m+o(\kappa m).}\tag{M9}
\]

This is conditional matched asymptotics: the core potential and higher operators must be subleading, and m/v→0 with an overlap maintained. It is not an exact nonlinear saddle or the full normalized fugacity. In the specified leading EFT the classical cloud suppresses its monopole insertion by exp(-2pi kappa m). With (M5) it scales as exp[-(2pi/g)sqrt(2a_def-1/3)], a relative O(g) action correction to the O(g^-2) BPS action. This nonuniform cloud scaling is not established by the literal O(1) remainder stated in Unsal–Yaffe equation (3.16); their statement cannot be used as a proof that this explicitly declared exterior has no such correction. No claim about a corrected all-mode prefactor is made.

The leading cloud correction is a known classical benchmark: [Forgacs–Obadia–Reuillon, hep-th/0412057v2](https://arxiv.org/abs/hep-th/0412057v2), Section 5, gives M/M0=1+beta/2+O(beta^2 log beta). Its normalizations translate to L M0=4pi kappa v and beta=m/v, reproducing (M9). The primary publisher's note was checked and affects only a table entry. SMALL_BETA_SOURCE_CHECK.md records the exact domain, translation and hashes. This establishes overlap, without identifying the polynomial source potential with the double-trace potential or upgrading the conditional matching calculation.

## 5. Observable, subtraction and remaining discriminator

M1 is a neutral two-constituent measure at fixed L, holonomy, coupling and renormalization scheme. M8 is an exterior **charged-sector** action with explicit boundary data. M9 is a conditional leading classical cloud correction. A vacuum generating functional requires the specified neutral ensemble, matter determinants, its matched metric-dependent coefficients and a common gravitational subtraction. The stress is obtained by varying that complete functional with the metric while holding the physical parameters and state fixed. A fugacity is a coefficient multiplying a magnetic disorder insertion; it is not by itself the partition function or its stress. Neither d nor the cutoff R can be set equal to H^-1 without specifying that geometry/state variation.

The constant-holonomy volume subtraction, coupling scheme, core matching, defect normalization and any local bulk/boundary counterterms must be common before a finite-volume comparison is called a physical stress. None is fixed by fitting alpha or a cosmological value here. The specific next step is to match the deformed core determinant to the screened exterior and then to the chosen neutral geometry, including the metric derivative of the resulting Wilson coefficient. The independent closed-ensemble assignment addresses the neutral dynamics; this report does not duplicate it. Quark, strong-coupling, proton and electromagnetic charge matching remain open. Pure Yang–Mills g is not electromagnetic alpha.

## 6. Execution and evidence

`matching-002` completed eleven symbolic identities and three independent 60-digit GPY-tail quadratures. `screened-001` completed twelve symbolic identities and three independent 60-digit exterior-action quadratures. Numerical checks are finite and not interval certified; the exact displayed identities carry the algebraic scope. No source determinant was independently recomputed. Scripts, contracts, outputs and v2 manifests are immutable. An initial CPU-affinity request was unsupported on macOS before a run directory existed; `matching-001` then recorded `launch-failed` in pre-exec with the address-space cap. The successful runs retained wall, CPU, output and thread limits and omitted the unsupported affinity/address-space request. These are environment failures, not physics evidence.

Source authentication, extraction/application verdicts, exact-version hashes and base-input pins are in SOURCES.json and BASE_INPUTS.json. Only short extracted equations/metadata are tracked; PDFs and extracted texts remain at their transient `/private/tmp/` paths pending coordinator-managed retention. No `.mathbox` ledger entry was requested or recorded.
