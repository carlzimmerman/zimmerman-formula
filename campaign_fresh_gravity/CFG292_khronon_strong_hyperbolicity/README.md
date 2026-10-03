# CFG292: strong hyperbolicity of GR + the BPS khronon (the C-H/K principal symbol) and criterion B

**Status (frozen rule): OPEN, as a fall-through of the frozen decision rule. A post-hoc reading would be CONDITIONAL; the owner decides which stands.**
Criteria frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit 6eaa9ea60. Five post-run disclosures are appended
at its end; the frozen text is unchanged.

## What was asked

XC2 left one item OPEN: strong hyperbolicity of GR + the BPS khronon, i.e. the Cauchy-problem obligation of recipe G4/G5
under the 2026-09-26 user decision "causality = criterion B". The system is L340's C-H/K:
I_CH + c^3/(16 pi G) Int sqrt(-g) [alpha_c a.a - c_2 K^2], with beta = 0 (so c_T = 1) and lambda_K = 1 + c_2. The record
window is alpha_c in (9.62e-14, 3.2e-9) and c_2 in (7.29e-3, 0.0667) (L340 P1). The lane also evaluates L350's six
Planck-era c_2 ceilings and the recipe edge lambda_K = 1.10. That gives 18 points, all exact rationals.

## What was found

1. **The MOND sector really is lower order (R0).**
   - The claim was re-verified in-lane before it was used: XC2 B5's committed numbers pass under its own rule, the
     frozen symbol e^{-xi^2 k^2} k^T C k is order -infinity (sympy), and the U-elimination Schur complement is
     2 C E/(1 + C E) k^2 with E = e^{-xi^2 k^2}, which is positive and order -infinity.
   - An independent power iteration on a zero-free background agrees, and XC6 D3/D4 (the filter's own variation) passed.
   - So the principal symbol is that of GR + the BPS khronon.
   - Limitation: C_T = nu - 1 grows like y^(-1/2) where the filtered field vanishes. Open zero-field regions are therefore
     outside the scope (as in XC5).
2. **The characteristic determinant factors exactly, for symbolic (alpha, beta, c_2) (T1):**
   - tensor: (1 - beta) lambda^2 = k^2, so c_T^2 = 1/(1 - beta), which is 1 at beta = 0;
   - **no vector mode**: the vector blocks carry only the gauge speed 1 (hypersurface orthogonality removes the
     aether's vector). So c_V does not exist here;
   - scalar: k^2 x (gauge/constraint factors at speed 1) x [alpha(1-beta)(2+beta+3c_2) lambda^2 - (beta+c_2)(2-alpha) k^2],
     so **c_S^2 = (beta + c_2)(2 - alpha)/(alpha (1 - beta)(2 + beta + 3 c_2))**. This is exactly Jacobson-Mattingly's
     s_0^2 under (c14, c13, c2) -> (alpha, beta, c_2);
   - the bare **k^2 is the leaf-elliptic factor**: the lapse's elliptic equation, i.e. the instantaneous mode.
3. **Strong hyperbolicity depends on the gauge.**
   - **F2a is strongly hyperbolic at all 18 points.** F2a = khronon time t = tau + spatial harmonic coordinates (the
     spatial components of the de Donder condition), with the lapse eliminated through its leaf-elliptic equation.
     - The leading matrix is invertible, all roots are real (+-1 and +-c_S), and the eigenvectors are complete (exact
       arithmetic, every helicity block).
     - The result is identical in 6 directions (exact rational unit vectors). The eigenvector-matrix condition number
       is direction-independent, 8.2e2 .. 2.0e6 over the window; it grows with c_S.
   - **F1 (fully covariant de Donder gauge + khronon) is only weakly hyperbolic at every point**:
     - there is a Jordan block at the gauge speed 1 in the scalar sector (multiplicity 4, nullity 3);
     - physical speeds are identical to F2a's;
     - it is a gauge-sector defect: pi shifts under the residual harmonic gauge modes.
   - **F2b (spatial-trace variant) is also only weakly hyperbolic** (multiplicity 2, nullity 1).
4. **General frozen background (T6).**
   - Background: lapse 1.3, a non-zero shift, non-diagonal gamma_ij, tau = t.
   - det P = [(xi_0 - N^i k_i)^2 - N^2 gamma^{ij} k_i k_j]^m x [same with c_S^2] x (a xi_0-free factor proportional to
     gamma^{ij} k_i k_j). The division is exact.
   - F2a's eigenvectors stay complete there.
   - Every cone is centred on the leaf normal. The aligned computation is the general frozen-coefficient one, because the
     principal symbol depends only on (g, d tau) at the point.
5. **Criterion B (CB, T7).**
   - Every cone is (u.xi)^2 = s_A^2 h(xi, xi) with the common axis u and 0 < s_A^2 < infinity: s = 1 for tensor and gauge
     modes, and s = c_S = 443.8 .. 9.505e5 c for the scalar. The top value is at the recipe edge c_2 = 0.10; XC1 A9's
     443.8 .. 7.9e5 c did not include that edge.
   - So every leaf is spacelike for every cone, however superluminal. Every characteristic ray crosses the leaves
     transversally, and none points backward in tau.
   - The leaf-elliptic factor's only characteristic conormal is d tau. Its propagation is instantaneous within a leaf,
     which the user decision explicitly allows.
   - With respect to any other slicing (aether boosted by 3/5), the elliptic factor has non-real roots. So does the
     superluminal scalar cone, because Q_S(dt) < 0. **The Cauchy problem must be posed on the khronon's leaves**: the
     preferred time of criterion B is forced, not merely allowed.

## Conditions (derived, F2a)

| Condition | What it does / why |
|---|---|
| **alpha_c != 0** | Keeps the leading matrix invertible: det A ∝ alpha(1-beta)(2+beta+3c_2)/(2 alpha - 1). |
| **0 < c_S^2 < infinity** | Real speeds and criterion B. For c_2 > 0 (lambda_K > 1) and 0 < alpha_c < 2 this means **alpha_c > 0**. |
| **beta = 0** | Gives complete eigenvectors at the gauge speed, in this gauge. beta != 0 puts c_T != the gauge speed and the block degenerates, so another gauge would be needed. The chassis has beta = 0 exactly. |
| **alpha_c != 1/2** | Keeps the lapse equation elliptic in this gauge; a gauge artefact. |
| c_S = 1 | **Not** a condition: at c_S^2 = 1 the merged eigenvalue stays semisimple (C5). |

The whole record window meets every condition with a wide margin.

## Controls (all behave)

- **C1** GR alone in harmonic gauge: strongly hyperbolic, all speeds 1.
- **C2** minimal Horava (alpha = 0): NOT strongly hyperbolic in F1 or F2a, because the scalar's xi_0^2 coefficient vanishes.
  That is the predicted reason: a first-order-in-time mode (Jacobson & Pulakkat 2025, J. Phys. A 58 315404).
- **C3** Einstein-aether: all three Jacobson-Mattingly speeds (tensor, vector, scalar) are reproduced exactly at a test
  point.
- **C4** MUTATE, alpha_c -> -alpha_c: c_S^2 < 0, so the speeds are non-real. F2a fails, T5 fails, CB fails, rc = 1.

## Verdict, scope, caveats

- **Frozen rule.** Sec. 6's CONDITIONAL clause required F1 to be strongly hyperbolic as well, and F1 is not (a gauge
  Jordan block). Neither the KILL clause nor the OPEN clause applies as written, so the script reports an **OPEN
  fall-through**.
  - Sec. 2 of the same file designated F2 as "the formulation that carries the verdict".
  - Read that way, the result is **CONDITIONAL**: strongly hyperbolic on the stated domain.
  - The rule was not rewritten after the fact; the gap is disclosed in FROZEN_CRITERIA.md (appendix, item 5).
- **Scope.** The results hold for the linearised, frozen-coefficient, high-frequency principal symbol, in the stated
  gauges, on backgrounds whose filtered field does not vanish. Say "no ill-posedness in the tested sector and scope",
  never "well-posed".
- **Not proven:**
  - nonlinear local well-posedness (a smooth symmetriser for the quasilinear system, constraint propagation for the C_i,
    and an elliptic-hyperbolic coupling theorem);
  - open zero-field regions;
  - beta != 0 in any gauge.
- **Implementation changes, disclosed** (FROZEN_CRITERIA appendix): T5 used exact spectra at rational unit directions
  after mpmath's QR failed on the defective F1 matrices; T6 used univariate determinants at s = 1, 2.
- **Literature look-ups** went through arXiv abstract/HTML pages via a summarising fetch and are PROVISIONAL as
  quotations: Sarbach, Barausse & Preciado-Lopez 2019; Jacobson & Pulakkat 2025; Jacobson & Mattingly 2004; Jacobson
  2008. The speed formulas are independently checked by C3's exact algebra.
- **Context, not computed here:** L350 found the c_2 window, in the plain K^2 form, excluded by Planck-era cosmology; its
  leaf-average form has the same principal symbol. kappa = 1/2 is FITTED and plays no role here. Nothing here bears on
  data.

## Files

- `cfg292_khronon_strong_hyperbolicity.py` is the lane script. `cfg292_lib.py` holds the jet-variable machinery for the
  quadratic Lagrangians and principal symbols.
- `cfg292_khronon_strong_hyperbolicity.out` and `cfg292_khronon_strong_hyperbolicity_results.json` are the normal run.
- `cfg292_khronon_strong_hyperbolicity_MUTATE.out` and `cfg292_khronon_strong_hyperbolicity_results_MUTATE.json` are the
  C4 run.

Run from the repository root (under a minute each):

    python3 campaign_fresh_gravity/CFG292_khronon_strong_hyperbolicity/cfg292_khronon_strong_hyperbolicity.py
    MUTATE=1 python3 campaign_fresh_gravity/CFG292_khronon_strong_hyperbolicity/cfg292_khronon_strong_hyperbolicity.py
