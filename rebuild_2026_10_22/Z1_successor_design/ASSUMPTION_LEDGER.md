# Z1_successor_design — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY, plus
LITERATURE-PROVISIONAL (read here from arXiv abstract or ar5iv pages; not checked against the published text),
RECORD (a number inherited from a verified lane, used as written), POSTULATED (a design choice of this lane) and
NON-VARIATIONAL (a design ingredient with no action).

## A. Requirement numbers (matrix)

| ingredient | class | note |
|---|---|---|
| every matrix number | RECORD | taken from lane READMEs and THEORY_V3_DRAFT rows the coordinator reran or reproduced; each carries its own ledger in its lane |
| the law μ = x/(1+x), AQUAL form | FRAMEWORK-NATIVE | the framework's own field equation (doors E2, covariant C4); not standard-MOND machinery here |
| footings 9.3603e-11 / 1.1312e-10 m/s² | FRAMEWORK-NATIVE, κ = ½ FITTED | never pooled |

## B. Family scorecard

| ingredient | class | source |
|---|---|---|
| verdicts for v3, v3s, v4, plain MOND, canonical rules | RECORD | lane READMEs; `explainers/crispy_fried_chicken_flavors.md` |
| Blanchet & Le Tiec 2008 (arXiv:0804.3518) action, NR equations (85)–(86), (90)–(105), stability and Solar-System remarks | LITERATURE-PROVISIONAL | ar5iv HTML summarised by a fetch tool; cross-checked by K1–K3 |
| Blanchet & Le Tiec 2009 (0901.3114), Blanchet & Heisenberg 2015 (1505.05146: a ghost in the DM sector in the decoupling limit) | LITERATURE-PROVISIONAL | abstracts |
| Boran, Desai, Kahya, Woodard 2018 (1710.06168: GW170817 falsifies "dark matter emulators") | LITERATURE-PROVISIONAL | abstract; it does not name TeVeS, so "TeVeS is in that class" is this lane's reading |
| Skordis & Złośnik 2019 (1905.09465: a TeVeS-type class with c_T = c) | LITERATURE-PROVISIONAL | abstract |
| Milgrom 2013 (1308.5388: BIMOND weak field, H₊ sector = linearised GR with its vacuum waves) | LITERATURE-PROVISIONAL | abstract; c_T = c is an inference from GR equivalence |
| Berezhiani & Khoury 2015 (1507.01019) | LITERATURE-PROVISIONAL | abstract; the model has an eV axion-like particle, so it is a reference only |
| Hertzberg+ 2105.02241, Mistele 2103.16954 | RECORD (literature status table) | `data_assembly/DOORS_LITERATURE_STATUS_2026-09-29.md` |
| P-medium action and parameters | RECORD via Y1 | `rebuild_2026_10_22/Y1_pmedium_flavor/ASSUMPTION_LEDGER.md` §A; Y1's verdicts are cited when they land |

## C. Design inputs

| ingredient | class | note |
|---|---|---|
| v3s action (GR + khronon J_x + covector P + switched stiffness −(γ_L/2)[max(D·P,0)]²) | FRAMEWORK-NATIVE (C4, C5, X3) | J_x POSTULATED in the record; γ_L POSTULATED in the record |
| removal of BS K(Q) (μ_K) | POSTULATED (this lane) | removes one FREE constant with no allowed value |
| cold medium = mimetic (geodesic) dust, abundance as an initial condition | POSTULATED form (X6 X-D2 shows it is the Q = 1 khronon), abundance FITTED as in v3 | adiabatic origin assumed, not derived |
| capacity rule R1: held density 0 ≤ D·P ≤ ρ_d (two-sided obstacle) | POSTULATED, variational inequality (same class as X3's switch) | zero continuous constants |
| ownership rule R2: the hold of each region acts in the free-fall rest frame of the smallest bound system containing it; medium bound to no system is unowned | POSTULATED, **NON-VARIATIONAL** | zero continuous constants; the one ingredient with no action (cf. CFG945 H1, CFG947) |
| supply ratio f_s = Ω_c/Ω_b = 5.364 | ΛCDM-PROCESSED (Planck-type abundance; the record's "catchment supply" input, CFG886) | used only in forecasts K10 |
| owner radius conventions: 200ρ_c (ΛCDM convention) and 18π²ρ̄_m (EdS spherical collapse of dust, native once the cold medium is dust at linear order) | ΛCDM-PROCESSED / FRAMEWORK-NATIVE | both reported; K10 is convention-sensitive and says so |
| H₀ for ρ_c | FRAMEWORK-NATIVE range 67.2–68.6 (C2); 67.9 used, both ends reported | |
| X2 tercile median gas masses 3.3e12 / 1.17e13 / 2.92e13 M☉ and a stellar share of 0.15 of baryons | SURVEY-CALIBRATION (catalogue M_gas,500) + POSTULATED share | forecast only; no lensing data enter this lane |
| X1 "iso AQUAL" residuals of hosted classes (+0.28 / +0.63 / +0.25 / +0.64 dex canonical) | RECORD | `rebuild_2026_10_22/X1_hosted_recount/README.md` L74–L80 |
| x ≈ 11–14 at z ≈ 1100 for linear-era fields | RECORD (audit estimate) | `rebuild_2026_10_22/X0_explanation_map/MAP.md` L22 |
| "linear field passes a₀ at z ≥ 84–101" | RECORD | CFG944 (`campaign_fresh_gravity/LEDGER.md` L705) |

## D. What this lane does not use
No lensing, kinematic or CMB data are read. No ΛCDM halo model, no QUMOND phantom, no ν_mono kernel, no EFE recipe.
