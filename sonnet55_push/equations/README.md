# sonnet55_push/equations -- equation advancement (2026-09-28)

Each item is an exact statement or reframing with a committed script that recomputes it. None of them derives kappa,
V0 or the carrier mass. "Novelty" is graded against what the repo already says, not against the literature.

| item | statement | script | novelty |
|---|---|---|---|
| EQ01 | Milgrom's cH/2pi is kappa_M = sqrt(2/(3 pi)) = 0.4607 in the framework's kappa*c*sqrt(G rho) convention; (kappa_F/kappa_M)^2 = 3 pi/8 exactly; the record's 8.2% gap is ln(2 pi/Z). SPARC's a0 read as kappa: 0.476 +- 0.026 on the rho_total footing (1/2 at +0.93 sigma, kappa_M at -0.59 sigma), 0.575 +- 0.031 on rho_Lambda (1/2 at -2.40 sigma). | `eq01_kappa_convention.py` (9/9) | bookkeeping: exact re-expression, no new physics. Consequential because it shows the "1/2 beats 1/2pi" comparison in the record was footing-mismatched. |
| EQ02 | Empty-de-Sitter psi (host-scalar) mode of CA5-GNC-R at EVERY wavenumber, closed form: G = a^3 M K alpha_e x/F; P + bdot = a^3 M x^2 N/F with N = 4 - 2 alpha_e + 4 K H^2 (alpha_e + x alpha_e')/F; sound speed c_s^2 = N/(K alpha_e); friction Gdot/G = H[1 - 2 x alpha_e'/alpha_e + 2 x F'/F] (3H in the UV, H in the IR). UV c_s^2 reproduces the record's host speed; IR limit (4 + 2 alpha_0)/(K alpha_0). N > 0 at all 50,625 x 400 scanned points, minimum +7.2e-3 in the alpha -> 2, ell -> 4 corner. | `eq02_vacuum_psi_mode.py` (6/6) | I did not find the exact P + bdot cancellation at leading order in x, or these closed forms, stated in the record (I read occupied/RESULT.md and the vacuum notes, not every file); the UV limit is a consistency check on them. Scope: empty dS only. |
| EQ03 | One-parameter footing family a0(z)^2 = kappa^2 (3/8pi)(cH0)^2 [Om_L + lambda Om_m (1+z)^3]: lambda = 0 canonical/flat, lambda = 1 alternative/tracks E(z). The z = 0 amplitude fixes kappa^2(Om_L + lambda Om_m); the z = 2.5 rise fixes lambda alone. lambda = 0.043 already gives +0.13 dex at z = 2.5, lambda = 0.20 gives the LCDM-native +0.33 dex. At kappa = 1/2 SPARC's a0 gives lambda = 0.70 +- 0.31 (flat law 2.2 sigma away, lambda = 1 at 0.96 sigma). | `eq03_footing_lambda.py` (8/8) | no earlier interpolation family found in the repo (grep). It is a parametrisation, not a derivation; radiation and curvature neglected. The dex figures are a0 shifts, not zero-point shifts (dilution 7-55% outside deep MOND). |

## What none of these says
- kappa = 1/2 is still fitted; EQ01 shows the data do not separate 1/2 from sqrt(2/3 pi) unless the footing is fixed.
- EQ03's lambda is not physics until a mechanism ties a0 to a density that includes matter; it is a way to make the record's fork measurable.
- EQ02 is the empty vacuum. The occupied case is in `../occupied_matrix/`.
