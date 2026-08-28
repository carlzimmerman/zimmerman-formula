# FC-ISO REPORT — Adjudication of the isotropic second-class Legendre completion

**Verdict:** `UNIFIED-NO-GO-constraint-first-MOND`
**Date:** 2026-08-28
**Adjudicator basis:** re-ran all four local certificates + four committed cross-cited
scripts this session; all exit 0.

## Question
Does an ISOTROPIC second-class Legendre completion of the MOND law
`D_i[mu(y) D^i q] = 4 pi G rho` exist whose on-shell traceless metric stress vanishes
(`Sigma_P = 0 => Phi = Psi`, gamma_PPN = 1 = "Fried Chicken") while keeping (a) the
correct MOND Gauss law, (b) `N_grav = 2` (no new propagating DOF), and (c) `c_T = 1`?

## Certificate ledger (re-run this session)
| Script | Checks | Exit |
|---|---|---|
| `fc_iso_setup.py` (Setup: reproduce naive-Legendre slip + York stress + obstruction object) | 19/19 | 0 |
| `fc_iso_construct.py` (CONSTRUCT track) | 28/28 | 0 |
| `fc_iso_refute.py` (REFUTE track, the theorem) | 37/37 | 0 |
| `fc_iso_aest_contrast.py` (AeST 6-DOF mechanism) | 14/14 | 0 |
| committed `sf42_aux_legendre_dof_2026.py` | 9/9 | 0 |
| committed `fc_final_4ac/fc4ac_slip.py` | pass | 0 |
| committed `theory_2026/york/ppn_lensing_cassini_2026.py` | pass | 0 |
| committed `real_research/reviews/typeII_direct_variation_2026.py` | 44/44 | 0 |

Note: the string "FAIL" in outputs is a **physics label** (slip != 1 at the knee /
deep-MOND), not a failed check — every `[ok ]` marker passed; zero `[FAIL]`/`[bad]`
markers across all four scripts.

## Adjudication logic
- **CONSTRUCT** did NOT produce a certified `Sigma_P = 0`, 2-DOF, `c_T = 1`, correct-MOND
  completion. All three named mechanisms fail with a computed `Sigma_P` and identified
  cost => **no Fried Chicken**.
- **REFUTE** proved `Sigma_P != 0` FORCED for `mu' != 0` across both completion classes
  and against every constructed escape (basis: THEOREM).
- **AeST-contrast** confirms the cancellation requires the aether's extra propagating DOF
  (metric-independent projector `g^{munu}+A^mu A^nu` + transverse aether mode; cancelling
  term vanishes as `A_mu -> 0`).

Per the rubric: REFUTE-forced + AeST-confirms-extra-DOF => `UNIFIED-NO-GO-constraint-first-MOND`.

## The unified no-go, stated
> The anisotropic constitutive Hessian `A^{ij} = mu gamma^{ij} + (y mu') u^i u^j` of any
> nonlinear isotropic MOND law forces a nonzero traceless on-shell metric stress
> `Sigma_P != 0`, hence a lensing slip `Phi != Psi`, in any 2-DOF constraint construction.
> Reaching `Phi = Psi` (MOND-enhanced lensing with gamma_PPN = 1) requires AeST-type extra
> propagating structure (a unit-timelike vector whose orthogonal projector is
> metric-independent, plus its transverse mode) that a pure 2-DOF constraint theory lacks.
> This closes the constraint-first isotropic-Legendre program on the lensing axis, within
> the local, action-based, <= 2-derivative, algebraically-reducible class.

## Root cause (single sentence)
Because `J` depends on the metric **only** through `s = |Dq|`, the gravitating (Hilbert)
traceless stress and the MOND force are the SAME functional of `mu` — killing one kills the
other, so `Sigma_P = 0 <=> ` the metric-coupled MOND nonlinearity is OFF.

## Residual open doors (honestly flagged, not over-closed)
1. **C4 general symmetric-tensor Lagrange multiplier** enforcing `Phi = Psi`: only the
   mimetic-scalar instance is certified to add a dust DOF; the general Dirac count is the
   next gate.
2. **Non-local elliptic phantom-density (QUMOND-as-density):** `Phi = Psi` at single-metric
   2 DOF but sourced by an isotropic density, not a healthy Hilbert-stress action; causal
   acceptability = committed unsettled question. Leaves the local action-based class.

## Inputs untouched
`a0^2 = kappa^2 c^2 G rho_Lambda` phenomenological TARGET; `kappa = 1/2`, `Z ~ 21` FITTED;
frozen kernel `mu_10 = y/(1+y^10)^{1/10}` never tweaked (the obstruction is kernel-general,
holding for any `mu' != 0`).
