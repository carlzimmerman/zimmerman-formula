# CT11_one_reservoir: frozen criteria (written before any number in this lane)

Lane under `CT_GATES_COMMON.md` after owner decision D1 ("Yes, grade it"). A go to GRADE, not to adopt: nothing here adopts a theory or reinstates the cold sector retired on 2026-11-01. No particle. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## Question
CT8 left one structural door: a single reservoir whose dust-like phase converts into the dark-energy phase, so that omega_x at recombination and rho_DE today are linked by the conversion dynamics. Does any concrete conversion model turn CT8's pure number (N ~ 1e10 on the epoch-free invariant) into something derived, or does it only move it into a rate, an onset, a seed or a threshold? For each model with a prediction: G5 and a background check; G5 pass only then opens a growth check and the a0 tie.

## Record checked before writing (what this lane must not re-derive or contradict)
- Route C (commit 840d6ccfea): conversion "as late as possible" must keep the clustering to z < 0.30 (CMB lensing); rested on Planck LCDM numbers (pre 10-25 rule), so cited, not graded on.
- X37 (rebuild_2026_10_22/X37_orbit_conversion): orbit-keyed conversion FAILS clusters (cores empty first). Not time-keyed.
- CFG131 (campaign_fresh_gravity/CFG131_door8_interacting_vacuum): with a Lorentz-invariant vacuum and Q^mu = Q u_c^mu, d_mu rho_L = Q u_mu; if Q depends on rho_c (Q_rho != 0), dust has delta rho_com = 0 (no clustering; growth ratio 2.7e-3, D3 R1). Q = Q(Lambda) only is the one cold-safe entry, and the flat a0(z) needs |xi| < 0.0275. Q != 0 breaks the shift symmetry (Lambda becomes a field).
- W4_09 (why_4_puzzle): generalized Chaplygin graded as a TRADE for a0.
- CT8: R5 (rho_x(0) = rho_DE) gives ratio 13.7 and H3/H2 1.35-1.37; R2: no rate built from G rho_DE switches dust on by z 3e4.

## Models (frozen list; nothing added after numbers are seen; no scans of a free constant to find a pass)
Receiver: a w = -1 phase (rho_DE' = +Q), donor dust (rho_x' + 3H rho_x = -Q), Lambda_bare = 0 (otherwise the link is absent by construction and the model is NO PREDICTION). Conversion starts at z_on (dust phase present) with rho_DE(z_on) = 0.
- **M1 dust-proportional constant rate, Q = Gamma rho_x**, Gamma a fixed field scale. Natural values graded: Gamma = kappa sqrt(G rho_DE0) (= a0/c) and Gamma = sqrt(8 pi G rho_DE0/3) (de Sitter rate). Onset z_on = 3e4 (latest allowed by RF5/X34; most favourable, since the produced rho_DE grows with z_on) and 1e6 reported. Prediction: given the measured rho_DE0, omega_x(rec). Reported: the Gamma/H_Lambda that the CMB window needs.
- **M2 Hubble-rate transfer, Q = xi H rho_x** (standard interacting-DE form). (a) onset at a -> 0 with Lambda_bare = 0: sign of rho_DE stated; (b) onset z_on = 3e4: the xi the window needs. There is no natural xi: NO PREDICTION unless one is listed here; xi = kappa = 1/2 is graded as the only number the framework owns (disclosed as a hand choice).
- **M3 threshold / unified fluid** (generalized Chaplygin p = -A/rho^alpha; purely kinetic k-essence near its minimum; sharp phase transition at rho_x = rho_*): early dust omega_x,early = omega_DE (B/A)^(1/(1+alpha)) or a_*^3 for the sharp case. The ratio is an integration constant. Natural reading graded: the transition happens when the dust density reaches the vacuum it becomes, at a_* = 1 (today), full conversion, which gives omega_x,early = omega_DE0. Any other a_* is a free epoch.
- **M4 receiver-proportional (autocatalytic), Q = xi H rho_DE** (CFG131's only cold-safe entry): rho_DE grows from a seed; seed is an integration constant: NO PREDICTION expected; stated with CFG131's bound.

For every model: count the free constants and say where CT8's pure number goes.

## Clustering precondition (record, not recomputed)
Any model with Q depending on rho_x (M1, M2) inherits CFG131 D1: with a Lorentz-invariant receiver the dust does not cluster at linear order. A pass on amount alone is therefore not a pass of G5 for M1/M2; stated alongside the CLASS numbers, which treat the dust as clustering (the most favourable reading).

## Raw inputs (10-25 rule; same as CT8)
rho_DE0: SN shape Omega_L 0.666 +- 0.018 x native H0 band 67.22-68.56 (central h 0.6789); omega_b 0.0224 [0.0217, 0.0229] (BBN D/H); T_CMB 2.7255, N_eff 3.046. kappa = 1/2 FITTED (counted). Planck footings not used (circular, CT8).

## Gates
- **G5** (CT3): raw Planck PR3 TT H3/H2 window [0.969, 0.989], omega_x/omega_b in [4.9, 5.4] from the model. CLASS 3.3.4 with CT3's peak finder and base (A_s 2.1e-9, tau 0.0544, YHe 0.2454), h 0.6789, omega_b 0.0224, n_s 0.93 / 0.9649 / 1.0. PASS: ratio in window and H3/H2 in window at all three n_s; FAIL: H3/H2 outside at all three n_s or ratio outside [4.9, 5.4] with its input range also outside; else NO VERDICT. Approximation stated: for M1/M2/M3 the dust at z >= 1090 is run as omega_cdm with the predicted early amount and the DE as a constant Lambda; justified only if the fraction converted after z 1090 (M1/M2) is below 1 %, which the script prints (else the run is flagged APPROX FAIL and a fluid run is required). M3's late full conversion does not affect the TT peaks (ISW only), stated.
- **Background check** (graded only for models that predict): DESI DR2 BAO table as transcribed in campaign_fresh_gravity/CFG681_bao_raw_geometry/cfg681_bao.py (D_M/r_d, D_H/r_d with correlations, BGS D_V/r_d; 13 numbers), r_d from CLASS for the model, h 0.6789; PASS chi2 <= 13 + 3 sqrt(26) = 28.3, else FAIL. Pantheon+ (prep_2026/sne_lambda/pantheonplus_full.dat, non-calibrators, zHD > 0.01, diagonal errors, offset marginalised) reported as chi2, not graded (diagonal errors).
- **Growth / a0 tie** (only if a model passes G5): sigma8 order of magnitude ~0.8, and whether a0 = kappa c sqrt(G rho_DE(z)) holds with that model's rho_DE(z) (G3 slope and 0.05 dex tracking statements).
- Check: CT3 row omega_c 0.12 at CT3 base reproduces H3/H2 0.992 within 0.002.

## Limits
Single thread, < 1 GB, minutes. No downloads. Commit nothing. Literature statements (Chaplygin perturbations, Scherrer 2004 kinetic k-essence) are from memory, provisional, not graded.
