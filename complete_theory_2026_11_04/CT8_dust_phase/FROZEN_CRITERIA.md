# CT8_dust_phase: frozen criteria (written before any number in this lane)

Lane under `CT_GATES_COMMON.md` after owner decision D1 ("Yes, grade it"). A go to GRADE, not to adopt: nothing here adopts a theory or reinstates the cold sector retired on 2026-11-01. No particle. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## Question
Is there a natural field-theory relation by which a P(X)/AeST-type dust phase (w = 0, c_s = 0, clustering, present by z >= 3e4) has its amount set by rho_DE (or by a0 = kappa c sqrt(G rho_DE)), so that omega_x/omega_b comes out 4.9 to 5.4 rather than fitted? Then G5 for any relation that predicts a number; G6 stated only.

## Gates, restated from the CT reports
- **G5** (CT3_REPORT.md section 2; ct3_cmb_checks.out): raw Planck PR3 TT H3/H2 = 0.979 +- 0.010, window [0.969, 0.989]; omega_x/omega_b in [4.9, 5.4] coming from the relation, not fitted. Dust must be present by z >= 3e4 (RF5, X34).
- **G6** (CT3 requirement 4, MC1): discs 66-82 % empty of the dust phase (N reading, measured response, below 250 km/s). Not run here: stated as the next gate only, no 3D run.

## Raw inputs (no Planck LCDM parameter values; 10-25 rule)
- rho_DE: raw SN shape Omega_L = 0.666 +- 0.018 (prep_2026/sne_lambda/VERIFY.md) times the native H0 band 67.22-68.56 (C2 K5: BAO + BBN, no CMB). omega_DE = Omega_L h^2, central at h 0.6789, range from the H0 band and the Omega_L error. Caveat recorded in advance: the native H0 uses a sound horizon that itself depends on omega_m, and the SN Omega_L is read in a flat background with matter.
- Sensitivity rows only (not graded): rho_DE from the rotation-curve-measured a0 at kappa = 1/2 (GLS 9.31e-27, median 6.31e-27 kg/m^3; same VERIFY.md).
- **Not used, recorded as circular:** the footings 9.3603e-11 / 1.1312e-10 encode Planck Omega_L = 0.6847 (VERIFY.md section 1: (1.1312/0.93603)^2 = 1/Omega_L). Pooling them (omega_tot - omega_DE) returns Planck's omega_c by construction and is not a prediction.
- omega_b: BBN D/H, 0.0224, range 0.0217-0.0229 (as reported in argon_push/AG6C_relativistic_completion/FROZEN_CRITERIA.md:66).
- omega_r: T_CMB 2.7255 K (FIRAS), N_eff 3.046.
- kappa = 1/2 FITTED where a relation uses it (counted).

## Candidate relations (frozen list; no relation is added after numbers are seen; no prefactor scans)
- **R1 shift charge** (AeST, mimetic, P(X) Higgs-phase dust): rho_x a^3 = Q0 I0 / (8 pi G~), I0 an integration constant (C2 K2: d rho/d a0 = d rho/d Lambda = 0). Predicts no number.
- **R2 rate tie**: the dust phase switches on when H(z) falls to a rate built from the tie, H = n sqrt(G rho_DE) (n = kappa, i.e. a0/c, and n = sqrt(8 pi/3), the de Sitter rate). Prediction: z_on, and the pure number n needed for z_on >= 3e4. If z_on < 1090 the dust is absent at recombination: omega_x(rec) = 0, graded through CLASS with omega_x = 0.
- **R3 hbar-scale misalignment**: mass m c^2 = (hbar c)^{3/4} (rho_DE c^2)^{1/4}. Onset epoch computed; amount proportional to theta_i^2 (free). It is a boson of definite mass: excluded by the standing no-particle rule. No number, no CLASS run.
- **R4 epoch-free invariant**: with dust a^-3, radiation a^-4 and rho_DE constant, the only time-independent dimensionless tie is rho_x^4 = N rho_r^3 rho_DE. Graded at N = 1 (the only value not put in by hand); the N the data need is reported.
- **R5 present-epoch equality**: rho_x(z=0) = rho_DE. Graded; flagged that "today" (a = 1) is a convention, so this tie is not dynamical (one hand-set epoch).
- **R6 Machian coincidence**: a0 = G M_m(<R_H)/R_H^2, R_H = c/H0, M_m the total matter (dust + baryons), H0 self-consistent with rho_tot = rho_m + rho_DE, kappa = 1/2. Canonical footing (a0 from rho_DE) is the graded reading; alt footing (a0 from rho_tot) reported beside it, never pooled. A disclosed second reading (M = dust only) is reported, not graded. Hand choices counted: R_H = c/H0, M = total matter, kappa. No action lies behind it; it is a coincidence relation.

## CLASS runs (G5)
Vanilla CLASS 3.3.4 via CT3's peak finder and raw TT file (reuse ct3_cmb_checks.py functions, no downloads). omega_x as linear dust (omega_cdm). h = 0.6789 (native), omega_b 0.0224, YHe 0.2454, tau 0.0544, A_s 2.1e-9 (the ratio is insensitive to A_s, tau; inherited from CT3 and disclosed). n_s is not measured natively: each predicted omega_x is run at n_s 0.93, 0.9649, 1.0.
- **PASS**: ratio in [4.9, 5.4] and H3/H2 in [0.969, 0.989] at all three n_s, at the central inputs.
- **FAIL**: H3/H2 outside the window at all three n_s, or ratio outside [4.9, 5.4] at central inputs with the input range also outside.
- Otherwise **NO VERDICT**.
- **NO PREDICTION** for R1, R3 (G5 can then pass only with a fitted omega_x, as AeST does).
- Check: the CT3 row omega_c 0.12 at CT3's base must reproduce H3/H2 0.992 within 0.002.

## Limits
Single thread, under 1 GB, minutes. Commit nothing. No 3D run.
