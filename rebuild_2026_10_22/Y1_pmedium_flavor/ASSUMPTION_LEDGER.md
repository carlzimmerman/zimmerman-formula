# Y1_pmedium_flavor — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY, plus PRESCRIBED (an
input chosen by the parent lane, neither data nor derived), FITTED (chosen to meet a target) and NUMERICAL.
The `sol61_push/` sources are untracked in git; their sha256 at reading time (both CHECKPOINT.sha256 files verified OK):
XP DERIVATION.md 29d3e7a0…9c56, MINISUPERSPACE.md 766616a0…36af, growth.py 158ac163…127f, growth/result.json 6f2905a5…2f48;
SE DERIVATION.md efd0511c…a42d, model.py a27cd6a3…7082; reciprocal_field RESULT.md 4e1393d0…e769; parent_compliance
RESULT.md 4ae07ba9…66e3; radiating_collapse CONTRACT.md 61500e67…35aa; cooling_assembly CONTRACT.md 82a6b00c…a42d.

## A. The flavor's action and parameters

| ingredient | value | class | source |
|---|---|---|---|
| reduced preferred-frame action (cold + baryon matter, P, χ, Poisson Φ), mismatch e = δρ_c − D·P, h = e/χ | — | FRAMEWORK-NATIVE construction (not derived from v3 or any covariant parent) | XP `DERIVATION.md` "Completion choices" |
| W(p) = −p − ln(1−p), \|P\| < 1 (force P/(1−\|P\|)) | — | FRAMEWORK-NATIVE (the record's saturating vacuum W) | XP `DERIVATION.md`; parent_compliance §2 |
| η (P inertia) | .005 | PRESCRIBED | `radiating_collapse_2026_10_22/CONTRACT.md` L8 ("eps=.005") |
| α (χ potential) | .005 = 1/(2λ), λ = 100 | PRESCRIBED | `cooling_assembly_2026_10_23/CONTRACT.md` L4 |
| b, d (χ inertia, gradient) | .125 = α/gap², gap .2; d = b·(phase speed 1)² | PRESCRIBED | same, L4 |
| ℓ₀ | 0.4404221297174536 kpc, both footings | **FITTED to a growth criterion**: the largest ℓ with the quasi-static EdS growing exponent ≥ .999 at k = 0.1 Mpc⁻¹, z = 1100 ("early-growth upper ell") | `parent_compliance_2026_10_22/RESULT.md` L80–L85; the galaxy-law side needs ℓ ≥ 133.787 / 140.005 kpc (same table) |
| a₀ (unit only: t₀ = √(ℓ₀/a₀), M₀ = a₀ℓ₀²/G) | 9.3603e-11 / 1.1312e-10 m/s² | FRAMEWORK-NATIVE, κ = ½ FITTED | W1 ledger; radiating_collapse CONTRACT L8 |
| χ ≥ 1 at static solutions | — | DERIVED (minimum principle on −d∇²χ + α(χ−1) = e²/(2χ²) ≥ 0, χ → 1) | SE `DERIVATION.md` "discrete maximum principle"; re-derived in this lane |
| cold sector = conserved collisionless particles (pressureless, any distribution function) | — | FRAMEWORK-NATIVE (the record's "cold energy"; no dark-matter particle is claimed by this lane) | SE `DERIVATION.md` |
| baryons pressureless, feel Φ only | — | PRESCRIBED (cosmology runs) / FRAMEWORK-NATIVE (force law) | XP, SE |
| reference density ρ̄_c = M_c/(A³V) subtracted globally | — | FRAMEWORK-NATIVE, NON-LOCAL (a slice average) | XP AUDIT item 7 |
| no metric sector beyond the homogeneous minisuperspace; no tensor modes | — | absence noted | XP `DERIVATION.md`, `MINISUPERSPACE.md` |
| no μ-function, QUMOND or EFE recipe anywhere in the action | — | absence noted (no STANDARD-MOND-MACHINERY) | XP, SE |

## B. Background and cosmological inputs

| ingredient | class | source | used in |
|---|---|---|---|
| imposed EdS H = H₀√Ω_m a^(−3/2), H₀ = 67.4, Ω_m = .315, no radiation, z_i = 1100 | ΛCDM-PROCESSED (Planck-2018 values; 67.4 inside the native 67.2–68.6) | XP `growth.py` | G1 (Codex reproduction), H3 |
| f_b = 1/6.364 (cold : baryon = 5.364) | ΛCDM-PROCESSED / FITTED abundance | XP `growth.py` | G1, H3 |
| F3 backgrounds A (C2 plik-lite ΛCDM refit) and B (CFG886 native Ω_m .2976, h .6856) with radiation, CLASS P(k) | ΛCDM-PROCESSED (as F3) | F3 `f3_growth_audit.py` L160–L175 | σ8 score |
| Λ in the growth score | PRESCRIBED: the minisuperspace allows an optional ρ_Λ; the flavor does not derive it | XP `MINISUPERSPACE.md` | σ8 score |

## C. Data (all on disk; no downloads)

| data | class | source | tile |
|---|---|---|---|
| SPARC 175 rotmod + Table 1 (`real_research/data/sparc_data/`, `SPARC_Lelli2016c.mrt`) | RAW (Υ per galaxy fitted, CFG4 convention V_bar² = sgn·V_gas² + ΥV_disk² + 1.4ΥV_bul²) | P4 T1 | Y-T3 |
| Lelli+15 TDGs (`real_research/data/tidal_dwarfs/lelli2015_tdg.csv`); DF2/DF4 constants (CFG657 via U1) | RAW (masses SPS/HI) | U1, P4 | Y-T5 |
| S1 per-system satellites (`S1_v3_hosted_small/s1_per_system.csv`: d_host, M★, r_h, x_e, log g_obs/g_bar) | RAW data side (E3 clean primary) + FRAMEWORK host fields (x_e from the host law: STANDARD-MOND-adjacent, used only as the host's field strength) | S1 | Y-T5 diagnostic |
| Solar-System gates: M(<Saturn) < 6.7e-11 M☉ (Pitjev & Pitjeva 2013), sunward 3.66e-14 m/s² (FP1), Q₂ 9.0e-27 s⁻² (Hees 2014) | RAW (published bounds as quoted by the record) | CFG3_solar_system.py L21, L67; D7d; C6 | Y-T4 |
| local cold density 0.013 M☉/pc³ (and 0.1 generous) | PRESCRIBED (a halo-like density; this flavor does not predict it) | this lane | Y-T4 S-a |

## D. Re-checks of the record's earlier P-medium assessments (to be done against the NEW action, not assumed)

| record statement | was about | how this lane treats it |
|---|---|---|
| CFG938 covariant parent CONDITIONAL; tethered medium has no linear self-gravity (δ ∝ a^0.61–0.69); CFG941 theorem D-T | the exact tether ∇·P = ρ − ρ̄ (e ≡ 0) | the new action has finite e²/(2χ); G3 derives its self-gravity fraction S = 1/(1+(kℓ₀/a)²) |
| WT-02 / CFG961: CFG938 ill-posed on FRW (χ forward-parabolic, multiplier backward-parabolic); c_T ≠ c (Christoffel² term) | CFG938's fluid-EFT parent with a multiplier | the new action has no multiplier and a second-order χ (b > 0) and no metric sector: H3 tests FRW; Y-T1 states c_T as not computable |
| CFG939: S4 not derivable; no-capture iff v_rel > V_esc,b | conservative S2+S3 dynamics | used as the no-capture criterion in Y-T4/Y-T5 after checking that this action is conservative (XP: one variational principle, expansion-work identity) |
| reciprocal_field theorem R_positive_e ≤ πℓ₀ (passive static spherical branch, no P-gradient) | the reciprocal action (X mediator, χ ≥ χ₀) | re-derived for this action (χ ≥ 1, no P-gradient term) in R1/R3 |
| parent_compliance: law needs ℓ ≥ 133.8 kpc, growth needs ℓ ≤ 0.44 kpc, "no overlap" | constant-A compliance | re-checked: here the effective length is ℓ₀/√χ ≤ ℓ₀ |
| H4: v3 ill-posed where the khronon density D·P + dust < 0 | v3's khronon fluid with γ_L | this action has no fluid with a sign-indefinite density (ρ_c ≥ 0 particles; e enters only as e²/(2χ)); H1 tests the frozen-coefficient dispersion on all admissible backgrounds instead |
| W1: SE reproduced; strong peak not converged; no certified bound core at z = 10 | this action's 3D evolution | cited as the state of core formation (no derived core population) |
| U1 T3: held dust weightless in a static v3 host | v3's khronon dust coupling | checked: here cold matter feels Φ + h, so it has weight |

## E. This lane's own choices

| choice | class |
|---|---|
| "T = 0 branch" = zero-dispersion, non-rotating, single central connected support (the minimum-energy static state at given cold mass) | PRESCRIBED (declared: the only static state fixed without a distribution function) |
| spherical approximation for SPARC (as P4 T1) | NUMERICAL / PRESCRIBED |
| R_s bound computed with g ≥ g_N,b at Υ = 0.30 and r₁ = πℓ₀ (most generous) | this lane (derivation in README) |
| off-support P tail neglected as a χ source in the T = 0 solver (it only raises χ, which the bound already allows) | NUMERICAL, declared |
| satellites treated as pure cold cores (baryons neglected) in the Y-T5 diagnostic | PRESCRIBED simplification (g_obs/g_bar ≫ 1 for the S1 sample) |
| Jacobi radius r_J = (G M d/(2 g_host))^{1/3} (flat-rotation-curve host) | standard Newtonian tidal estimate |
