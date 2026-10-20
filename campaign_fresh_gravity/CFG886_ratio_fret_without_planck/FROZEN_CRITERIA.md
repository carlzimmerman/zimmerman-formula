# CFG886 — FROZEN CRITERIA: rebuild Ω_c/Ω_b = 5.364 and the census f_ret without the Planck ΛCDM fit

Frozen before any script of this lane exists and before any number of this lane is computed (owner block 880–889; CFG884–886
assigned in the 880–889 reservation row, 82082007b; no CFG886 directory, row or commit existed). κ = ½ is FITTED. Footings
a0 = 9.3603e-11 (canonical) and 1.1312e-10 m/s² (alt), never pooled. "Cold energy" throughout; its mass is still required;
no particle species. Not "theory closed". Nothing here may say the data favour the framework over ΛCDM. Showing that an input
cannot be rebuilt cleanly is a valid result.

## 0. What was read before this file (blindness disclosure)

- **The inputs to be rebuilt.** THEORY_CANONICAL v2/v3: supply = 5.364 × (catchment baryons) = 5.364 N M_b, N = 1/f_ret;
  "derive 5.364 / f_ret" is on the open list. 5.364 = 0.1200/0.02237 (Planck 2018 ΛCDM, e.g. CFG4_clusters.py, CFG365 T0).
- **f_ret provenance already read (so T4 below is largely documentary, not blind):** CFG416 FROZEN_CRITERIA (the declared
  fret_of: 0.10 below 10^12.5 Msun/h, log-linear to 0.55 at 10^13.5 and 0.85 at 10^14.5, cap 0.90; "from the census and
  group/cluster baryon fractions, stated in advance"); CFG365 criteria/README (Shull, Smith & Danforth 2012 cosmic-mean census
  quoted: ~10% in galaxies, groups and clusters, 18 ± 4% in collapsed phases incl. CGM; "galaxies only" 0.07); CFG398; CFG515
  criteria/README/lib (fixed point M_b,now = f_ret f_b M_ta/h, f_b 0.157, h 0.674, M_ta in Msun/h); CFG525 D3 ("a declared step
  taken from the cosmic mean in Shull+12 (recalled, PROVISIONAL)"); CFG634 README (HC-1 calls the 0.10 floor "stars + cold gas");
  CFG640 README; CFG804 criteria/script/README (fixed point M_ta = M_b/(f_ret f_b) written WITHOUT the h of CFG416's Msun/h
  thresholds — noticed while reading, to be quantified in T5, not a result yet); CFG806 row (framework derivation of f_ret
  failed); CFG830 row (~6 hand-set census numbers); CFG379 README (record group/cluster levels use hydrostatic X-COP M_FORW and
  Lovisari+15 M500); the Shull citation file (bibliographic only; no census table is in the repo).
- **Ω_m and BAO already read:** CFG681 README/script (DESI DR2 table; X ≡ 1 BAO-only Ω_m 0.2970, χ² 10.55; X ≡ 1 BAO+SN
  0.3039 (no error in the JSON); free X: Ω_m runs to the floor). CFG682 README/criteria/output: **"flat a0 implies Ω_m =
  0.3085 ± 0.0075" is the P2 FORECAST row** — BAO + Pantheon+ shape with five free dark-energy nodes, conditioned on an
  ASSUMED measurement a0(2.33)/a0(0) = 1 with total error e = 0.02 dex (no such measurement exists; at e = 0.15 dex the same
  row gives 0.2929 ± 0.0205). It is therefore used here only as a labelled conditional variant, never as the primary.
- **BBN and r_d already read:** XR26_bbn (PRIMAT 2024 / PArthENoPE 2017 at ω_b 0.02236: D/H 2.448 / 2.587e-5; observed D/H
  2.547 ± 0.029e-5 (PDG 2024, as cited there) and 2.527 ± 0.030e-5 (Cooke+18, as cited there)); CFG254 criteria (CAMB r_drag
  147.049 Mpc at the Planck 2018 Table 1 best fit, ω_b 0.022383, ω_c 0.12011, N_eff 3.046, Σm_ν 0.06 eV); CFG654 criteria/ICs
  script (ω_b 0.02193 ± 0.00022 from Cooke+18 inverted with CAMB's PRIMAT 2024 table; SH0ES 73.04 ± 1.04, Riess+22, carried as
  "record value, CFG493 / CFG642"); real_research/reviews/project_independent_H0_a0_crossmatrix.py (record list: SH0ES
  73.04 ± 1.04, TDCOSMO 2025 71.6 ± 3.6, sirens 68.0 ± 4.1). CFG689 criteria (queued, uses the Planck A1 pair as its ruler).
- **Lanes whose sensitivity is reported (T5):** CFG876 script/README (supply-capped variant, cap 53.64 M_b), CFG878 README
  (stock note: 5.25e6 M⊙ clump > 53.64 M_b for M_b ≲ 1e5), CFG804 (bins and edge formula), cfg654_pm.py (FB = ω_b/(ω_b+ω_c)
  enters the census edge).
- **Hand expectations written before any script (expectations, never predictions):** from memory of DESI DR2's own BAO+BBN
  result (h ≈ 0.685, Ω_m ≈ 0.297; memory, UNVERIFIED) and r_d ∝ ω_b^−0.13 ω_m^−0.25: R(a) ≈ 5.2–5.3, i.e. 5.364 expected inside
  1σ; R(b) at SH0ES ≈ 6.1–6.4, i.e. outside +10%; so "a RECOVERED, NOT PINNED overall" is the expected outcome. R + 1 = ω_m/ω_b
  scales roughly as (h r_d)^4 Ω_m^2 ω_b^−0.5 under BAO+BBN, so R is far more sensitive to the BAO numbers than to D/H.
- **Disclosed:** BAO + an early-universe ω_b prior is standard cosmology in spirit (DESI publishes BAO+BBN). Under the tracking
  rule a0(z) = κ c √(G ρ_DE(z)) the framework's flat a0 means constant ρ_DE, which is ΛCDM's background; so no outcome here
  can favour the framework over ΛCDM. What is new is only removing the Planck fit from the framework's own constant.

## 1. Inputs (repo only; nothing downloaded)

| input | value | provenance |
|---|---|---|
| D/H primary | (2.547 ± 0.029) × 10⁻⁵ | PDG 2024 eq. 24.2 as cited in XR26_bbn.py / CFG254 |
| D/H variant | (2.527 ± 0.030) × 10⁻⁵ | Cooke, Pettini & Steidel 2018 as cited in XR26_bbn.py (CFG654's input) |
| BBN tables | PRIMAT 2024 (MC theory error column), PArthENoPE 2017 standard; PArthENoPE Marcucci reported | CAMB 1.6.6 `camb.bbn` |
| N_eff | 3.044 (ΔN = 0 in CAMB's table convention); T_CMB 2.7255 K (FIRAS) | standard; PArthENoPE's ΔN = 0 may be 3.046 (≤ 1e-5 in ω_b, disclosed) |
| Σm_ν | 0.06 eV, one massive (oscillation minimum, not a CMB fit); variant 0 | ω_ν read from CAMB's `omnuh2` |
| BAO | DESI DR2 table as committed in `CFG681_bao_raw_geometry/cfg681_bao.py` (ANISO six tracers D_M/r_d, D_H/r_d, r; BGS D_V/r_d) | parsed from that file at run time (ast) |
| H0, local ladder | SH0ES 73.04 ± 1.04 km/s/Mpc (Riess+22) | record value: cfg654_ics.py PROVENANCE, mi_kappa_sensitivity_census_2026.py |
| H0, reported only | TDCOSMO 2025 71.6 ± 3.6; standard sirens 68.0 ± 4.1 | record list, project_independent_H0_a0_crossmatrix.py |
| Ω_m conditional variant | 0.3085 ± 0.0075 | CFG682 P2 forecast row (BAO+SN, assumed flat a0 at z 2.33 to 0.02 dex) |
| free-X nodes | CFG682 committed BAO-only and BAO+SN best-fit nodes at fixed Ω_m (0.24–0.36) | `cfg682_results.json` |

## 2. Early-universe assumptions (labelled; they are assumptions about the early universe, not results)

E1 standard BBN (nuclear rates as in the two codes; their offset carried as a systematic); E2 N_eff = 3.044, no extra radiation;
E3 GR expansion before recombination with **cold energy behaving as pressureless matter before recombination** (the CFG654
principle); E4 standard recombination for z_drag (CAMB/RECFAST defaults); E5 cold mass conserved after recombination, so the
late-time BAO ω_m and the pre-recombination ω_m are the same (CFG253 bounds late creation at ≤ ~3%, record context);
E6 flat space. None of these uses the CMB anisotropy fit.

## 3. Tasks and statistics

**T1 ω_b from D/H.** For each table, invert DH(ω_b, ΔN = 0) = D/H_obs (brentq on [0.015, 0.030]). σ_obs = σ_DH/|dDH/dω_b|;
σ_th from PRIMAT 2024's sig(D/H) at the solution (applied to both codes; PArthENoPE has no error column). **Primary ω_b = the
midpoint of the PRIMAT 2024 and PArthENoPE-standard inversions, σ = √(σ_obs² + σ_th² + (Δ/2)²)**, Δ = their difference (the
nuclear-rate systematic). Each code alone, Marcucci, and the Cooke+18 variant are reported.

**T2 H0 without the CMB.**
- **(a) primary: joint BAO + BBN, flat a0 at all z.** Background flat, ρ_DE constant (X ≡ 1 = flat a0 under the tracking rule),
  E(z)² = Ω_m(1+z)³ + Ω_r(1+z)⁴ + (1 − Ω_m − Ω_r), Ω_m including the massive neutrino as matter, Ω_r = ω_γ(1 + 0.2271 N_rel)/h²,
  ω_γ = 2.4728e-5, N_rel = 3.044 × 2/3 with one massive species (3.044 when Σm_ν = 0). r_d(ω_b, ω_c) from CAMB 1.6.6 `rdrag`
  (mnu 0.06, one massive, nnu 3.044, TCMB 2.7255, bbn_predictor = PRIMAT 2024 table, H0 68) tabulated on a grid and splined in
  (ln ω_b, ln ω_c). Likelihood = DESI DR2 χ² (2×2 covariance per anisotropic tracer, BGS D_V; tracers independent, as CFG681)
  × Gaussian BBN prior on ω_b (T1 primary). Flat priors: Ω_m on [0.20, 0.42] (step 0.001), h on [0.60, 0.78] (step 0.0005);
  ω_b marginalised with 9-node Gauss–Hermite quadrature. Derived: h, Ω_m, ω_m = Ω_m h², ω_c = ω_m − ω_b − ω_ν, h r_d.
  Posterior mean, sd, and 2.5/16/50/84/97.5 percentiles from the grid weights.
- **(a) variants (reported):** V1 + Gaussian prior Ω_m = 0.3085 ± 0.0075 (CFG682 conditional; double-uses BAO, labelled);
  V2 Cooke+18 D/H; V3 PRIMAT alone / PArthENoPE alone; V4 Σm_ν = 0 (own r_d spline, R = ω_m/ω_b − 1 literally);
  V5 **free dark energy** (no flat-a0 assumption): at each CFG682 fixed-Ω_m row (BAO-only and BAO+SN), take the committed
  best-fit nodes, profile q = c/(H0 r_d) analytically (CFG681's form, its own radiation convention), solve 100 h r_d(ω_b,
  Ω_m h² − ω_b − ω_ν) = c/q for h with the T1 primary ω_b, and report R(Ω_m) and χ²(Ω_m) over 0.24–0.36.
- **(b) local ladder:** h = 0.7304 ± 0.0104 (Gaussian); Ω_m from the same DESI DR2 BAO with X ≡ 1 and the ruler FREE (shape
  only: flat prior on h r_d over [90, 112] Mpc, step 0.02, marginalised; r_d from BBN NOT used, since (b) and the BBN ruler are
  the two sides of the Hubble tension); ω_b from T1. R by Monte Carlo (10⁶ draws, seed 886). Variant: Ω_m from CFG682's
  conditional 0.3085 ± 0.0075. Reported only: the r_d that (b) implies, c/(100 h q), vs BBN's r_d.
- **Reported only:** R at TDCOSMO 71.6 ± 3.6 and sirens 68.0 ± 4.1 (same Ω_m and ω_b as (b)).

**T3 the rebuilt ratio.** R = ω_c/ω_b = (Ω_m h² − ω_ν)/ω_b − 1 (ν subtracted so R is comparable with Planck's ω_c/ω_b; the
literal Ω_m h²/ω_b − 1 is also printed), f_b = ω_b/(Ω_m h²) (task definition) and f_b,fw = 1/(1 + R) (the framework's
convention, CFG804's FB), with errors, for (a) and (b) and every variant. z = (R − 5.364)/σ_R (Planck's own σ on 5.364,
≈ 0.065, is stated, not added).

**T4 f_ret provenance and rebuild.** Two segments: G = galaxy floor 0.10 (log M_ta < 12.5 Msun/h), C = the group/cluster ramp.
For each: does the value or the mass coordinate where it is applied rest on (i) abundance matching, (ii) NFW/ΛCDM-profile lensing
fits, (iii) Newtonian hydrostatic total masses read as "baryons + cosmic-ratio dark matter", (iv) a ΛCDM mass function, (v) a
CMB-fitted Ω_b denominator; and is the source table in the repo (TRACEABLE) or recalled (NOT TRACEABLE IN REPO). Evidence = the
files listed in §0 plus a grep of the LEDGER/lanes for the ramp's source (the script prints the grep counts). Rebuild where
possible: (1) the census denominator — a luminosity/mass-function census fraction scales as f ∝ h/ω_b, so f_ret,new = 0.10 ×
(h_new/0.674)(0.02237/ω_b,new), labelled as assuming the census was computed at the record's constants (the census's own adopted
h and Ω_b are not in the repo); (2) the stock S/M_b = R/f_ret, ratio-only (f_ret held 0.10) and census-consistent (where ω_b
cancels: S/M_b = ρ_c/ρ_gal ∝ ω_c/h); (3) CFG804's fixed point per bin with f_b = 1/(1 + R) and the rebuilt h.

**T5 sensitivity (report only; no heavy reruns).**
- CFG876 supply-capped variant: cfg876.py exec'd read-only with its literal 53.64 replaced by the rebuilt stock and its two
  write statements removed (asserted present exactly once each); E, se, N_fail per footing; the stocks are (a), (a) ± 1σ, (b)
  ratio-only and (a), (b) census-consistent. Nothing is written into CFG876's directory.
- CFG878 stock note: M_b threshold = M_cl/(S/M_b), M_cl = 5.25e6 (canonical) / 4.24e6 M⊙ (alt), record ledger values.
- CFG804: per-bin N, R N and edge (r_M units, edge_of(N) with SUP → R) for the canonical and alt primary masses, in CFG804's own
  Msun convention and in CFG416's declared Msun/h convention; the KiDS demand N ≥ 3–4 at 5.364 (CFG803) re-expressed as a stock
  ≥ 16.1–21.5 M_b.
- CFG650/654 shear engines: factor on the census edge r_M(f_ret f_b M_ta)/ln(1 + f_ret f_b/(1 − f_b)) at fixed M_ta for f_ret
  0.10 and 0.55; the other Planck inputs still in those engines are listed (they are not rebuilt here).

## 4. Classes (frozen)

- **Recovery (per option and variant):** |z| ≤ 1 **5.364 RECOVERED**; 1 < |z| ≤ 2 CONSISTENT; 2 < |z| ≤ 3 TENSION; |z| > 3
  NOT RECOVERED. The headline uses (a) primary.
- **Pinning (task wording):** **NOT PINNED** if the central R of (a) primary or (b) primary lies outside 5.364 × [0.90, 1.10];
  else PINNED TO ±10%. The (b) − (a) spread as a fraction of 5.364 is printed. Both classes are reported together.
- **Precision flag:** if σ_R(a)/R(a) > 0.10, (a) is labelled NOT INFORMATIVE whatever its z.
- **f_ret:** per segment CLEAN (no input (i)–(iv); (v) allowed because BBN reproduces it and it is rebuilt here) /
  ΛCDM-DEPENDENT (any of (i)–(iv) in the value or the mass coordinate) / UNDETERMINED (the source is not in the repo and the
  record does not say how the number was made). Overall: CLEAN if every segment is CLEAN; ΛCDM-DEPENDENT if every segment is;
  MIXED otherwise (UNDETERMINED segments named). The TRACEABLE / NOT TRACEABLE flag is reported beside the class.

## 5. Controls

- **K1 (load-bearing):** (i) the lane's R function at ω_b 0.02237, ω_c 0.1200 returns 5.364 to ≤ 1e-3; (ii) CAMB rdrag at that
  point (Σm_ν 0.06, N_eff 3.044, h 0.6736) is within 0.1% of the record's 147.05 Mpc (CFG254/XR26); (ii′, reported) XR26's
  exact settings (ω_b 0.022383, ω_c 0.12011, N_eff 3.046, PArthENoPE, H0 67.32) give 147.049 within 0.01%.
- **K2 (load-bearing):** (a) the lane's BAO χ² in CFG681's conventions (radiation at h 0.68, N_eff 3.046 massless, X ≡ 1, q
  profiled) reproduces CFG681's T1 X ≡ 1 minimum (χ² 10.5515, Ω_m 0.29703) to 1e-3 in χ² and 2e-4 in Ω_m, and CFG682's
  committed BAO-only fixed-Ω_m χ² values at their nodes to 1e-6; (b) analytic background vs CAMB at the (a) posterior mean:
  D_M/r_d and D_H/r_d at the seven redshifts agree to 5e-4; (c) r_d spline vs direct CAMB at six interior points to 2e-4, and
  r_d varies by < 1e-4 over h 0.62–0.76.
- **K3 (load-bearing):** BBN round trip DH(ω_b,inv) = D/H_obs to 1e-8; Cooke+18 with PRIMAT 2024 reproduces CFG654's ω_b
  0.021932 within 1e-5 (σ 0.00022 within 1e-5); PArthENoPE at ω_b 0.02236 gives D/H within 1.5% of 2.587e-5.
- **K4 (load-bearing):** grid adequacy — posterior mass within 3 grid steps of any Ω_m or h boundary < 1e-6; posterior sd of
  Ω_m and of h each ≥ 5 grid steps.
- **K5 (load-bearing):** the CFG876 exec with stock 53.64 reproduces the committed cfg876_results.json E of "primary B" and
  "supply-capped (B)" on both footings to 1e-12.
- **K6 (load-bearing):** CFG804 fixed point in its own convention at its canonical primary masses reproduces the README's N
  10.0 / 8.8 / 7.4 / 5.6 to ≤ 0.05.
- **MUTATE (`CFG886_MUTATE=dh10`, separate outputs `*_MUTATE_dh10.*`):** D/H_obs × 1.10 (both measurements). Must give: ω_b
  (primary) lower by 4–8%; R(a) higher by +1% to +6%; R(b) + 1 higher by the inverse ω_b ratio to within 0.5%. Any miss = the
  control fails (rc 1).
- rc = 0 only if every load-bearing control passes (main run) / the MUTATE expectations hold (mutate run).

## 6. Outputs and limits

`cfg886.py`; `cfg886.out`, `cfg886_results.json`; `cfg886_MUTATE_dh10.out`, `cfg886_results_MUTATE_dh10.json`; README.md with
the results, controls, disclosures. One process, `OMP_NUM_THREADS=1 nice -n 10`, < 10 min, < 2 GB. a0 enters none of T1–T4
(both footings are identical there); footing-specific numbers appear only in T5. Any change after a number is seen goes in the
README as a dated, labelled departure; this file is never edited.

κ fitted; cold energy mass required; not theory closed.
