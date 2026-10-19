# QCD-V: explicit monopole normalization, hyperbolic response, and the missing cosmological coefficient

Checkpoint FSP-003, parent FSP-002. Owner QCD-V. Checked 2026-10-18 America/New_York. This report calculates an actual contribution in the cited deformed-QCD construction and identifies a concrete determinant and boundary problem remaining before a physical ratio can be predicted. No dark-energy, proton-mass or electromagnetic measurement is used to choose a coefficient.

**Result:** the centered-ball BPS zero-mode normalization has the exact factor (V1) below, with leading correction \(-1/(2m_W\mathbb L)\). It is a contribution to a specified semiclassical measure. Its promotion to the full finite-boundary vacuum response is conditional. The claimed hyperbolic coefficient \(1/8\) is an estimate with an omitted determinant, separation moment and state/geometry bridge. Neither value calculates physical \(c_H\) or \(R=c_H/C_p^3\).

## 1. Exact reproduction of the controlled zero-mode term

Use the weakly coupled, center-stabilized gauge theory with a small **fixed** circle of circumference \(L\), and a spatial ball of radius \(\mathbb L\). The source prescription integrates the infinite-space BPS solution and zero modes over that ball; it does not solve a new boundary-value problem. Let

\[
x=m_W\mathbb L,\qquad
H(r)=m_W\left[\coth(m_Wr)-\frac1{m_Wr}\right],\qquad
K(r)=\frac{m_Wr}{\sinh(m_Wr)}.
\]

For a centered BPS hedgehog, \(D_i\Phi=B_i\) and \(D_iD_i\Phi=0\) give

\[
\int_{B_{\mathbb L}}(D\Phi)^2d^3x
=4\pi\mathbb L^2 H(\mathbb L)H'(\mathbb L).
\]

Relative to its infinite-space value \(4\pi m_W\), the norm is

\[
n(x)=\left(\coth x-\frac1x\right)
       \left(1-\frac{x^2}{\sinh^2x}\right).
\]

Rotational symmetry and self-duality make each translational norm have the same ratio. For the gauge-rotation denominator, normalize \(\int\Phi^2\) by \(m_W^2\) times the ball volume. Its ratio to the infinite-radius regularization is

\[
d(x)=\frac3{x^3}\int_0^x(t\coth t-1)^2dt
=1+\frac3{x^2}-\frac{3\coth x}{x}.
\]

The integral follows from
\((t\coth t-1)^2=d[t^3/3+t-t^2\coth t]/dt\), with zero lower endpoint. The rotation norm ratio is \(n/d\). Three translational coordinates and one rotation coordinate therefore give

\[
\boxed{M_{\rm zm}(x)=n(x)^{3/2}\sqrt{n(x)/d(x)}
=\frac{n(x)^2}{\sqrt{d(x)}}.}\tag{V1}
\]

At large \(x\), the exponentially small terms separate from the algebraic expansion:

\[
M_{\rm zm}(x)
=\frac{(1-x^{-1})^2}{\sqrt{1-3x^{-1}+3x^{-2}}}
  +O(x^2e^{-2x})
=1-\frac1{2x}-\frac1{8x^2}+O(x^{-3}).\tag{V2}
\]

This independently reproduces the \(-1/2\) in [Thomas–Zhitnitsky, 1203.6073v2, equations (19)–(23)](https://arxiv.org/html/1203.6073v2). It does not rely on substituting a typical length. The source's Section III.C retains the variational boundary treatment and allows uncomputed boundary corrections; hence (V2) alone is not a calculation of the full determinant or total vacuum coefficient.

Conditional on identifying the leading vacuum potential with \(-N\zeta/L\), this contribution yields

\[
\Delta\epsilon_{\rm zm}(\mathbb L)
=\frac{N\zeta}{2Lm_W\mathbb L}+O(\mathbb L^{-2}).\tag{V3}
\]

This is a boundary/finite-size response in a deformed pure-gauge theory. It is not the \(H\to0\) response of physical QCD. No proton state or independent electromagnetic coupling is present in this calculation. With the pure-gauge action held fixed, its explicit derivative with respect to an absent electromagnetic \(\alpha\) is zero; that is a statement about this model only.

## 2. What the hyperbolic source actually reduces to

[Zhitnitsky, 1505.05151v2](https://arxiv.org/html/1505.05151v2) uses Euclidean \(H^3_\kappa\times S^1\), with sectional curvature \(-\kappa^2\), circle **radius** \(\kappa^{-1}\), and circumference \(\beta=2\pi/\kappa\). It defines a free energy \(F=-\beta^{-1}\log Z\). Its Section II.4 footnote 6 excludes a controlled small-circle deformed-QCD calculation on this linked family. Section III.1 assumes the required nontrivial-holonomy hyperbolic calorons; Section III.3 sets the unknown nonzero-mode response to zero and estimates a separation by \(\Lambda^{-1}\).

The 2026 source instead describes the circle's circumference as \(\kappa^{-1}\). Since it absorbs numerical factors into an uncomputed coefficient, this does not change its scaling claim, but an actual coefficient match must resolve the \(2\pi\) convention.

Keeping the omitted quantities explicit, write

\[
\frac{f_0}{f_\kappa}=1+\kappa a+o(\kappa),\qquad
a=a_{\rm zm}+a_{\rm nzm}+a_{\rm int}+a_{\rm ensemble}.
\]

Within the source's reduced ensemble at \(\nu=1/2\), \(\log Z\simeq8\pi fV\), so

\[
\Delta(F/V)=\frac{8\pi f_0}{\beta}\,a\kappa+o(\kappa),\qquad
c_\kappa=\frac{8\pi f_0}{\beta\Lambda^3}a.\tag{V4}
\]

Even accepting this reduction, the source's zero-mode estimate is

\[
a_{\rm zm}\simeq\frac{\nu(1-\nu)}2\langle r_{12}\rangle_{w},\tag{V5}
\]

where the weighted moment arises from differentiating an averaged measure. In general \(\langle r\rangle_w\) is not the unweighted mean: if \(c(\kappa)=\int dr\,P(r)w(r)[1+\kappa A r+\cdots]\), then \(\partial_\kappa\log\sqrt c=(A/2)\int Pwr/\int Pw\). Response of \(P\) itself is an additional term. Replacing this moment by \(1/\Lambda\), setting every other \(a\) to zero and absorbing \(8\pi f_0/\beta\) into \(\Lambda^4\) produces \(1/8\). Those operations do not evaluate (V4).

The source's fixed-holonomy path also has \(v=\nu\kappa\). At confining \(\nu=1/2\), \(m_W\sim\kappa\to0\), whereas a weakly coupled compactification requires its W-boson scale above the strong scale. The controlled regime of Section 1 does not approach this limit. Holding a small \(\beta\) fixed while varying \(\kappa\) would define a different two-scale problem.

## 3. Exact hyperbolic Coulomb check and neutral-sector cancellation

This section is a hand derivation, independently checked by the bounded script. It tests an inference used to motivate (V5); it is not a calculation of the non-Abelian determinant.

For a radial scalar on \(H^3_\kappa\),

\[
\Delta u=u''+2\kappa\coth(\kappa r)u'.
\]

Imposing \(-\Delta G=\delta\), unit Gauss flux and \(G(\infty)=0\) uniquely gives

\[
\boxed{G_\kappa(r)=\frac{\kappa}{4\pi}[\coth(\kappa r)-1]
=\frac{\kappa}{4\pi}\frac{e^{-\kappa r}}{\sinh(\kappa r)}.}\tag{V6}
\]

At every fixed positive separation,

\[
G_\kappa(r)=\frac1{4\pi r}-\frac\kappa{4\pi}
+\frac{\kappa^2r}{12\pi}+O(\kappa^4r^3).\tag{V7}
\]

Exponential decay at \(r\gg\kappa^{-1}\) therefore does not eliminate Coulomb interactions at \(r\sim\Lambda^{-1}\ll\kappa^{-1}\). The constant term depends on the boundary condition at infinity. For charges \(q_i\), consistently including the same regular part in self energies and pair energies yields

\[
\delta E=\frac12\sum_{ij}q_iq_j\delta G
=-\frac\kappa{8\pi}\left(\sum_iq_i\right)^2+O(\kappa^2).\tag{V8}
\]

Thus the linear Coulomb-kernel contribution cancels exactly in a finite neutral configuration. A self-energy/fugacity correction in isolation need not survive the cross terms. This does not prove cancellation of the zero-mode Jacobian or of the whole monopole gas.

The source explicitly permits total-charge fluctuations; mean neutrality is insufficient. For its ideal gas at \(\nu=1/2\), the two constituent counts in one self-dual sector are independent Poisson variables with equal mean \(2\pi fV\), giving \(\langle Q\rangle=0\) and \(\langle Q^2\rangle=4\pi fV\). A fixed-\(Q=0\) ensemble and that ensemble can respond differently. Moreover (V7) is not uniform for pair distances of order \(\kappa^{-1}\) or larger: its termwise use before an infinite-volume sum needs an additional bound. The neutral finite-configuration identity establishes neither an infinite-volume theorem nor vanishing physical \(c_H\).

## 4. A linear boundary ambiguity can be calculated exactly

For a geodesic ball of radius \(R\),

\[
V_\kappa(R)=\frac\pi{\kappa^3}[\sinh(2\kappa R)-2\kappa R],\qquad
A_\kappa(R)=\frac{4\pi}{\kappa^2}\sinh^2(\kappa R).
\]

At fixed \(R\), both are even analytic in \(\kappa\), and

\[
\left.\partial_\kappa[A_\kappa/V_\kappa-3/R]\right|_{0^+}=0.
\]

For every fixed positive \(\kappa\), instead,

\[
\lim_{R\to\infty}A_\kappa/V_\kappa=2\kappa.\tag{V9}
\]

A fixed boundary free-energy density \(\sigma\) allowed in the regulator contributes \(W_\partial=\sigma\beta A\). Its spatially averaged free energy changes after flat subtraction by

\[
\Delta(F_\partial/V)=\sigma[A_\kappa/V_\kappa-3/R]
\longrightarrow 2\sigma\kappa.\tag{V10}
\]

The resulting linear coefficient changes by \(2\sigma/\Lambda^3\), despite unchanged bulk equations. If \(\kappa\to0\) is taken first, its linear coefficient is zero. This explicitly proves dependence on boundary prescription/order of limits for a volume-averaged candidate coefficient. It does not imply an arbitrary counterterm in boundary-free de Sitter QCD. A local central stress tensor can also differ from a volume average on hyperbolic space; the latter retains a finite fraction near its boundary.

Matching flat and hyperbolic boundary induced metrics or subtracting all boundary terms could remove this particular ambiguity, but changes the comparison contract and still leaves the full fluctuation measure to be computed. Classical conformal equivalence does not fix that quantum measure. As an adjacent warning, [Franchetti–Harland, 2408.07145v2, Theorem 1](https://arxiv.org/html/2408.07145v2) requires half-integer monopole mass and modified complex gauge fixing to obtain finite bilinear pairings; the usual Coulomb-gauge monopole norm diverges. That theorem supplies no positive real KvBLL ensemble determinant.

## 5. Free energy is insufficient to obtain the metric stress tensor

For a static Euclidean background with independent \((\beta,h_{ij})\), let \(W=-\log Z=\beta V\mathfrak f(\beta,h)\). The thermal energy density is

\[
\rho=V^{-1}\partial_\beta W\big|_h
=\mathfrak f+\beta\partial_\beta\mathfrak f\big|_h.\tag{V11}
\]

The pressure requires a spatial metric variation, including curvature, boundary, holonomy and subtraction changes. Values of \(W\) only on the diagonal \(\beta=2\pi/\kappa\) give one total derivative, whereas (V11) requires a partial derivative. Explicitly, two extensions

\[
\mathfrak f_1(\beta,\kappa),\quad
\mathfrak f_2=\mathfrak f_1+(\beta\kappa-2\pi)q(\kappa)
\]

agree on every point of the diagonal but their energy densities differ there by \(2\pi q(\kappa)\). This is an information-theoretic nonuniqueness proof, not a proposal to add a local counterterm. A full action and state could select one extension. The one-parameter free-energy curve alone cannot.

Nor is the hyperbolic Euclidean product the Euclidean continuation \(S^4\) selecting the regular de Sitter state. Their curvature signs, topology, circle/boundary data and spectra differ. A conformal relation of the product to punctured flat space neither makes it \(S^4\) nor renders massive, running QCD Weyl invariant. An analytic continuation and a state prescription must be established before assigning its coefficient to de Sitter stress energy. [2506.14182v4, Section II.C](https://arxiv.org/abs/2506.14182v4) calls the \(\kappa\mapsto H\) step a central assumption.

There is also a direct obstruction to treating the specific confining-holonomy saddle as an ordinary smooth instanton on the compactification. The conformal identification is \(H^3\times S^1\cong S^4\setminus S^2\); the circle contracts as the omitted surface is approached. In a smooth local trivialization, the holonomy of any smooth connection around a shrinking contractible circle tends to the identity. The source's \(\tfrac12\operatorname{Tr}U=\cos(\pi\nu)=0\) at \(\nu=1/2\) has noncentral holonomy and cannot satisfy this condition. Its image therefore needs singular/surface-defect data or retained boundary data at that surface. Allowing a projective adjoint bundle can allow central monodromy, but does not make this noncentral value smooth. This is a non-extension statement for these boundary conditions, not a no-go theorem for other QCD configurations or all possible de Sitter states.

The distinction appears explicitly in [Franchetti–Harland, Proposition 6](https://arxiv.org/html/2408.07145v2): a smooth circle-invariant irreducible instanton on an \(SU(2)\) bundle over \(S^4\), with the specified lifted real-line action, gives half-integer mass \(p\) and central **lifted** monodromy \((-1)^{2p}\). This lifted group action is not the fundamental Wilson holonomy of a small loop in a smooth periodic trivialization; the gauge transformation to a static monopole can itself be nonperiodic by a central factor. It must not be used to permit fundamental Wilson holonomy \(-I\) on a shrinking contractible loop of a smooth \(SU(2)\) connection. Formally matching the static Higgs eigenvalues gives \(p=\nu/2\); the confining \(\nu=1/2\) has \(p=1/4\), outside the stated theorem. The sufficient obstruction used here is noncentral monodromy, which persists for the adjoint global form. Consequently neither equality of full moduli-space measures nor the smooth \(S^4\) state follows from classical conformal equivalence.

## 6. Remaining determinant and the next executable calculation

With fixed finite boundary, holonomy and UV subtraction, the one-monopole semiclassical weight has the schematic but operational form

\[
z_\kappa=\mathcal N\,e^{-S_\kappa}
\sqrt{\det\mathcal G_\kappa}\,
\frac{\det\mathcal M_{{\rm gh},\kappa}}
{\sqrt{\det{}'\mathcal M_{{\rm vec},\kappa}}}
\prod_f\det(\not D_\kappa+m_f).
\tag{V12}
\]

Here \(\mathcal G\) is the zero-mode Gram matrix in the path-integral inner product, the prime removes those zero modes, and each determinant means a background/vacuum ratio with the same boundary conditions. In background Feynman gauge, \(\mathcal M_{\rm gh}=-D^2\) and the vector operator contains \(-D^2\delta_\mu{}^\nu+R_\mu{}^\nu-2\operatorname{ad}F_\mu{}^\nu\), with the sign of the adjoint action fixed by the chosen anti-Hermitian/Hermitian convention. Curvature and boundary variation both enter.

For every such operator, the missing response is a genuine heat-kernel integral,

\[
\partial_\kappa\log\det{}'\mathcal M
=-\partial_\kappa\int_{0}^{\infty}\frac{ds}{s}
\operatorname{Tr}'\big[e^{-s\mathcal M_{\rm mono,\kappa}}
-e^{-s\mathcal M_{\rm vac,\kappa}}\big]_{\rm ren}.\tag{V13}
\]

One must include the derivative of the state/ensemble distribution and monopole interactions in addition to (V13). A positive zero-mode piece does not preclude cancellation at a specified matter content; non-universality across matter contents does not prove non-cancellation in any one theory. Neither (V12) nor (V13) has been evaluated here for the required hyperbolic KvBLL ensemble.

The immediate executable continuation is to keep the controlled small circle \(L\) fixed, specify framed boundary data for one centered BPS saddle in a finite ball, and compute the relative radial vector/ghost determinants with exactly those data. A Gel'fand–Yaglom or partial-wave phase-shift calculation can test whether the coefficient in (V2) survives in the complete saddle weight. Its asymptotic expansion must use \(m_W^{-1}\ll\mathbb L\), include ghost/zero-mode subtraction consistently, and estimate the angular-momentum tail. This is substantially narrower than a QCD cosmological simulation, but requires deriving the coupled radial fluctuation operators and admissible boundary conditions first. Installing a large simulation package or assigning an unknown determinant a value would not execute it.

The next physical-QCD step is different: compute the renormalized stress response in a specified de Sitter state, with Minkowski subtraction and matched masses/couplings. The controlled ball result supplies no proton coefficient \(C_p\), and replacing \(\mathbb L^{-1}\) by \(H\) supplies no such matching. Therefore this branch yields no physical \(R(\alpha)\) or isolated \(\alpha\) root.

## 7. Evidence, execution and review

Source authentication, exact-version formulas, applicability and unresolved arrows are separated in SOURCES.json. INPUTS.json pins the source PDFs/text and upstream contract/baseline. Full sources remain in temporary storage. No manuscript or older checkpoint was edited.

The current mathematical contract is COMPUTATION_CONTRACT_v4.json; current code is check_geometry_v4.py, with an explicit result-path argument for reproducibility. Bounded runs runs/geometry-003 and runs/geometry-004 completed, and their v2 manifests validate against the current inputs. They verify the symbolic primitives, Laplace/flux identities, area/volume limits, neutral-charge algebra and five direct BPS radial quadratures at \(x=1,2,5,10,30\), 70 decimal digits, residual tolerance \(10^{-55}\). The largest observed quadrature residual is below \(10^{-70}\); this is numerical consistency, not an interval bound. The universal conclusions rely on the displayed hand derivations.

Runs geometry-001 and geometry-002 failed at a SymPy 1.14.0 limit call on the cancellation-prone \(\coth\) expression, which returned \(-\infty\). The original scripts/contracts/manifests/logs are preserved. The third version extracts the exact Laurent coefficient; independent unit-flux derivation (V6) and the elementary expansion of \(\coth\) settle that limit without relying on the faulty call. These failures are implementation/library failures, not counterexamples to (V7).

The exact successful argv and input/output hashes are recorded in runs/geometry-004/manifest.json. Validate without recomputation:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_prediction/vacuum_geometry/runs/geometry-004/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

An executable new run, from the repository root, uses a fresh output directory:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/qcd_prediction/vacuum_geometry/COMPUTATION_CONTRACT_v4.json --input fine_structure_puzzle/qcd_prediction/vacuum_geometry/check_geometry_v4.py --output fine_structure_puzzle/qcd_prediction/vacuum_geometry/runs/geometry-rerun --result fine_structure_puzzle/qcd_prediction/vacuum_geometry/runs/geometry-rerun/results.json --timeout 40 --max-output-bytes 1048576 --max-cpu-seconds 30 --max-threads 1 -- python3 fine_structure_puzzle/qcd_prediction/vacuum_geometry/check_geometry_v4.py --result fine_structure_puzzle/qcd_prediction/vacuum_geometry/runs/geometry-rerun/results.json
```

Review provenance: derivations and source application received self-review; the coordinator independently checked the area/volume limiting argument and requested the neutral self-plus-pair check. There is no independent audit of the full determinant because it was not calculated. Proofreading self-review covered this report's displays and definitions; no source mathematical tokens were edited.

**Primary audit verdict for the claimed physical coefficient:** incomplete, with the smallest missing implication being the complete, consistently regulated monopole measure and its metric variation in the requested state. **Strongest safe result:** (V1)–(V2) exactly calculate one specified zero-mode contribution; (V8) and (V10) demonstrate concrete cancellation and boundary mechanisms that the cosmological coefficient must distinguish.
