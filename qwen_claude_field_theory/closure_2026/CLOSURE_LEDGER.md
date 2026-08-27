# CLOSURE LEDGER

Generated 2026-08-27 by the referee-to-closure audit (workflow wf_da5c9383-ca5, 11 agents, all evidence scripts committed).

| Gate | Result | Evidence | Assumptions |
|---|---|---|---|
| **FROZEN 12-GATE SUITE (MMG_constraint_first, re-run this freeze session)** | | | |
| G01 constitutive exact MOND law | PASS | scripts/01_constitutive.py; FINAL_GATE_RERUN.log "ALL GATES PASS" (tail verified this session) | G(y)=y^2+2(1+y)e^{-y}-2 => mu=1-e^{-y}, sympy==0 |
| G02 Newtonian limit (constraint) | PASS | scripts/02_newtonian_limit.py | C_M => div[mu grad Psi]=4piG rho exact; constraint only — matter EOM NOT derived here (see A3) |
| G03 Dirac matrix Pf=L_N*K | PASS (independently confirmed) | scripts/03_dirac_matrix.py + attack A1 24-term re-derivation | canonical ADM brackets; b,c cancel identically |
| G04 rank + ellipticity | PASS | scripts/04_rank_and_ellipticity.py | y>0: mu>0, 1+(y-1)e^{-y}>0 |
| G05 DOF count 20-12-4=4 => 2 | PASS-CONDITIONAL | scripts/05_dof_count.py; caveat from attack A4 check 0.6 | "6 first-class" now flagged: {D^2q,H_i} piece (1/3)D^2(D.xi) uncomputed |
| G06 constraint preservation | PASS-as-algebra, SUPERSEDED in content | scripts/06_constraint_preservation.py | r_4 left SYMBOLIC — evaluating it exposed the chi-force (A3) |
| G07 tensor sector Q_T>0, c_T=c | PASS | scripts/07_tensor_sector.py; FLRW extension A6 (Q_T=a^3/32piG, c_T^2=c^2) | MMG-chassis result, never transfer |
| G08 matter consistency O(v^2/c^2) | FALSIFIED | scripts/08_matter_consistency.py vs attack A3 (commit 3c771f0a) | violation enters at NEWTONIAN order, not O(v^2/c^2) |
| G09 Legendre / 4D covariance | FAIL-as-4D (honest) | scripts/09_legendre_check.py | preferred foliation, refoliation invariance False |
| G12 falsification sweep | PASS | scripts/12_falsification.py, 8/8 | generic branch only |
| G13 kernel-swap ellipticity | PASS | scripts/13_kernel_swap_ellipticity.py; gate13_freeze.log | transfers the 2-DOF/ellipticity certificate ONLY — explicitly does NOT cover PPN/lensing/matter defects |
| **SEVEN ATTACK GATES (this freeze)** | | | |
| A1 Dirac + branch proofs | PASS | scratchpad/gate_dirac_branch_proofs.py exit 0 (UNCOMMITTED — revision item) | canonical brackets; norm-linear y; symbol->operator via uniform ellipticity; kernel-agnostic (mu_exp + symbolic-n mu_n) |
| A2 exceptional sectors k=0, y=0 | PASS | sf54/sf55 commit fc2e28f1, both exit 0 | compact slices; strict minisuperspace truncation; dust; kernel-BLIND at k=0 |
| A3 matter conservation | FAIL | gate_matter_conservation_derivation.py/.out commit 3c771f0a; re-run exit 0 this session | four-multiplier H_T exactly as Gate 8 certifies; structural fork = invalidator 1 |
| A4 genuine PPN (gamma,beta,alpha_1,alpha_2,alpha_3) | FAIL | scratchpad/ppn_mmg_gate_2026.py 34/34 (UNCOMMITTED — revision item); cross-checked vs committed b6b3ced2 and audit3 | minimal ADM photon/matter coupling; preferred-frame matching; gamma=0, beta=1, alpha_1=4, alpha_2=0, alpha_3=-1 kernel-independent; Q2: mu_exp 4.6-6.9x ceiling FAIL, mu_5/mu_10 0.387/0.078 canonical clear (route1B confirmed) |
| A5 lensing derived | FAIL | gate_lensing_weakfield_derivation.py/.out commit b6b3ced2, 12/12; re-run exit 0 this session | minimal photon coupling; decaying BCs; Phi=0 exact, slip=0, half-light, kernel/footing-blind (6/6 cells 0.5000); M24 Delta-chi2 +403..+498; clusters 3.44-4.16x |
| A6 FLRW + linear perturbations | OPEN (derived, adverse) | scripts/14_flrw_perturbations.py commit 3ca1276d, 23/23 | k=0 prescription as written; empty linear scalar sector (theorem of mu(0)=0); eta=0; background a0-blind, no dark energy; tensor/vector = GR |
| A7 exact spherical + EFE | PASS | gate_spherical_efe_2026.py/.out commit e52b8412, 18 checks | static weak field; saturated EFE regime; EFE tensor DERIVED; DR4 fork: registered band unreachable, mu_n => gamma_v 1.0040/1.0001 |
| **NEGATIVE BRANCHES** | | | |
| DW_causal_nonlocal | REJECTED whole-branch (VERDICT B) | PAPER1 sect.4.2 DOI 10.5281/zenodo.22132648; sf50 14/14 exit 0 but UNCOMMITTED (G04) | decisive: Cassini Q2 x3.8-5.0 (10-14 sigma) STRUCTURAL — localization remnants <=8% vs 75-82% needed; 2T+2S ghost survives phase space; FLRW dead (no dS, w=0 dust, a0 free, kappa_fit~0.64); c_T^2-1~+3.9e-2 modulo one unverified cancellation; salvage = Z=0 crossing regularity + static ellipticity only; "2T+1S for DW" = G03 conflation, do not propagate |
| AeST_pressure_promotion | NOT FROZEN (passes BANKED) | mi_relativistic_completion_aest_2026.py 28/28; mi_aest_jeans_nonlinear_verdict 23/23; DEPENDENCY_MAP:125,210,315 | 6 DOF (external Hamiltonian, PRD 110.044015); "AeST-as-2-DOF" RETRACTED; a0 NOT structural; Cassini inherited, alpha_1/alpha_2 never computed; scalar = w=0 dust at full Omega_dm; 2.06-4.42x overshoot risk; kernel/lensing/CMB passes remain citable but a closure here certifies an external theory |
| BIMOND_DBI_khronon | NOT FROZEN (most open, 10/16) | STANDING.md; sf12 12/12; DOI 10.5281/zenodo.22015358 (construction-level R1/R3 only) | BD ghost UNCHECKED (standing rule: quote neither way); no nonlinear DOF count, no c_T, no combined lensing, no PPN, no Boltzmann; Lambda_D unpinned; ephemeris 1e-3458.7 interpolation-dependent; khronon risks E01 2T+1S no-go; freezing restarts the program from near zero |
