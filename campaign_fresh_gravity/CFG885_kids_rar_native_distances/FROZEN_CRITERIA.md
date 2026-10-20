# CFG885 FROZEN CRITERIA: the KiDS lensing RAR results without B21's ΛCDM distances (before any script)

**ID note:** owner block 880–889 (CFG885 assigned in the LEDGER reservation row, 82082007b). Agent lane.

**Why.** Every KiDS lensing lane of the record (CFG829, CFG840, CFG849, CFG850, CFG851) uses the Brouwer et al. 2021 (B21)
public ESD profiles as released. B21 turned shear into excess surface density with critical surface densities from a
fiducial flat ΛCDM background: Ω_m = 0.2793, H0 = 70 (WMAP9; B21 Sect. 3, as the record's FP18 line 215 and FP21 line 43
read it; the ESD columns are labelled h70 M_⊙/pc²). That is a ΛCDM input inside "raw" data. This lane replaces it with
the framework-native background and rescores the headline statistics unchanged. A SHIFTED or CHANGED result is as useful
as a ROBUST one.

## Physics of the rescaling (analytic; each step re-checked in the script)
1. **g_bar does not move.** B21's g_bar = G M_b / R² per lens–source pair (point mass, stars + cold gas). At fixed flux and
   angle θ, M ∝ D_L² × flux and R = θ D_A with D_L = (1+z)² D_A, so g_bar ∝ (D_L/D_A)² flux/θ² = (1+z)⁴ flux/θ²: free of
   h and Ω_m. B21's g_bar bins, the window W and the law's prediction g_law(g_bar) are therefore unchanged.
2. **g_obs moves by a multiplicative factor only.** g_obs = 4 G ESD_t / bias (B21 Eq. 7, README) has no radius term.
   B21's estimator is ESD = Σ w_s Σc⁻¹ e_t / Σ w_s Σc⁻² (w_ls = w_s Σc⁻²). If the native background is the true one,
   ⟨e_t⟩ = ΔΣ Σc,nat⁻¹, so ESD_B21 = ΔΣ ⟨r⟩ with r = Σc,nat⁻¹ / Σc,fid⁻¹ averaged with weights w_s Σc,fid⁻² over the pairs.
   Hence g_obs,native = T · g_obs,B21 with **T = (h / 0.70) / ⟨r⟩** (r computed in h-free units; the h70 part is exact).
   A slope-dependent deprojection correction (B21's beyond-SIS discussion) would be invariant under a constant rescaling at
   fixed g_bar; the released files and the lanes use Eq. 7 only.
3. **Per-point factor.** For a data point at g_bar with neighbour spacing q, the lens L contributes with weight
   a_L = M_gal,L × [area of the annulus R² ∈ (G M_gal/(g√q), G M_gal/(g/√q)) inside B21's 0.03–3 h70⁻¹ Mpc] / D_A(z_L)²,
   times S2(z_L) = Σ_b ν_b f_b(z_L) ∫ n_b(z_s) Σc,fid⁻²(z_L, z_s) dz_s; ⟨r⟩ = Σ_L a_L S2r(z_L) / Σ_L a_L S2(z_L) with
   S2r using Σc,fid⁻¹ Σc,nat⁻¹. g_obs_i → T_i g_obs_i, C_ij → T_i T_j C_ij.

## Inputs
- **Native background:** flat, E² = Ω_m(1+z)³ + Ω_r(1+z)⁴ + (1 − Ω_m − Ω_r) (flat a0 ⇔ constant ρ_DE under the tracking law;
  CFG681's form and Ω_r), **Ω_m = 0.3085 ± 0.0075** (CFG682 P2: raw BAO + SN, flat a0, no CMB). **h is not fixed by the
  framework:** bracket h ∈ {0.674 (BAO+BBN-like), 0.70 (B21's own), 0.73 (distance ladder)}. A parallel lane (CFG886) is
  computing a BBN+BAO H0; this lane does not wait for it.
- **Fiducial:** flat, Ω_m = 0.2793, h = 0.70, no radiation term (checked: its effect on T < 1e-4).
- **Sources (S1, primary):** KiDS-1000 SOM n(z) (`../_external_data/cfg592_work/kids/*/data_fits/xipm_KIDS1000_*.fits`,
  NZ_SOURCE, Z_MID, BIN1..BIN5) weighted by the header's NGAL_1..5; tomographic Z_B ranges (0.1,0.3], (0.3,0.5], (0.5,0.7],
  (0.7,0.9], (0.9,1.2]; B21's cut Z_B > z_l + 0.2 applied as the fraction f_b of each bin's Z_B range above z_l + 0.2 (Z_B
  uniform inside a bin, declared). **S2 (variant):** point-Z_B: true z = Z_B, uniform inside each bin's range, NGAL weights,
  hard cut (B21's exact Σc⁻¹ treatment is not recorded in the repo, so both are bracketed).
- **Lenses (L1, primary):** photo-z of the record's 181,477-lens reconstruction of B21's isolated sample
  (`real_research/data/lensing_rar/lr_lenses.npz`, columns z, logM, Mgal, typ). Proxies (declared): blue ↔ typ 0, red ↔ typ 1
  (LePhare u−r 2.0, not B21's 2.5); disc n<2 ↔ blue, spheroidal n>2 ↔ red (no Sérsic indices on disk); all isolated ↔ all;
  isolated dwarfs ↔ logM < 10.0 (B21's exact dwarf cut is not in the repo); GAMA (CFG840 V4) ↔ all.
  **L2–L4 (envelope):** one effective lens redshift for every dataset, z_l ∈ {0.15, 0.25, 0.35}.
- **Class-deciding bracket:** h (3) × Ω_m,nat ∈ {0.3010, 0.3085, 0.3160} (3) × lens model {L1, L2, L3, L4} (4) × source model
  {S1, S2} (2) = **72 points**, fiducial Ω_m 0.2793. **Reported only:** fiducial Ω_m over [0.25, 0.32] (h 0.70, Ω_m,nat 0.3085,
  L1/S1), because 0.2793 is confirmed in the repo only through the record's reading of B21, not from B21's own files.

## Rescored statistics (code reused unchanged)
cfg829.py's `load` and `amp` are exec'd exactly as CFG840/849/850/851 do; cfg851.py's definitions (`calibrate`, `predict`,
`RED`, `BLUE`, `R28`) are exec'd from its file; `load` is wrapped (g_obs·T, C·TTᵀ) in those namespaces. The lanes'
classification lines are copied verbatim into the driver; K1 proves the copy.
- **CFG829:** A ± σ_A in W = [10^−13.3, 10^−11.9) for blue, red, all isolated, isolated dwarfs (canonical ν_e, alt ν_e; canonical
  simple-ν reported); blue class by CFG829's rule (LAW HOLDS AT LOW g / LAW-SHAPE / INTERMEDIATE) on each footing; (A−1)/σ_A;
  the dwarf ×2.75 exclusion (2.75 − A)/σ_A; CFG829's calibration-window check.
- **CFG840:** its 8 variants + V4 (GAMA vs KiDS), class ROBUST / FRAGILE by its rule; min (2.75 − A)/σ_A over the variants.
- **CFG849:** colour and Sérsic splits, class by its rule, both footings.
- **CFG850:** its five shift rows, both footings; class by its rule (canonical; the same rule applied to alt, reported).
- **CFG851:** b, log g†, χ², dSph z and class for canonical/alt × red M★ shift 0.123 / 0. Its 1σ on log g† is not in CFG851;
  it is computed here at T ≡ 1 by profile Δχ² = 1 over b (declared, used only for the 1σ comparison).

## Classes (CFG885; both footings)
- **ROBUST:** every classification below equals its T ≡ 1 value at all 72 points, AND every tracked amplitude moves by less
  than its own T ≡ 1 σ at every point. Classifications: CFG829 blue class (canonical, alt); CFG840 class; CFG849 class
  (canonical, alt); CFG850 class (canonical; alt by the same rule); CFG851 class (canonical, alt × shift 0.123, 0). Tracked
  amplitudes: A_blue, A_red, A_all, A_dwarf (CFG829, canonical and alt, ν_e); CFG851 b and log g† (shift 0.123, both footings).
- **SHIFTED, SAME CLASS:** every classification holds, some tracked amplitude moves ≥ 1σ (named, with the bracket point).
- **CHANGED:** any classification flips at any bracket point (named, with the point).
- **Secondary flag (not a class):** CFG851's "g† ≈ a0 (canonical, M★-corrected)" coincidence. Report the range of
  log g† − log a0 over the bracket: STABLE if within ±0.1 dex everywhere, otherwise DISTANCE-DEPENDENT.

## Hand expectation (written before any run)
Ω_m 0.2793 → 0.3085 shrinks the h-free distances and raises Σc by ~1–2% at z_l ~ 0.25, so T_Ω ≈ 1.01–1.02; h dominates,
T ≈ 0.97–1.06 over the bracket. A near-uniform T scales A and σ_A together, so the colour/Sérsic split significances (CFG849,
CFG850) barely move, while A_all (σ 0.050) and A_red (σ 0.076) can move ≥ 1σ at h = 0.73. When g† sits above every data
point, log g† shifts by log10(T)/b ≈ 17 log10(T), i.e. ~±0.3 dex. Expected: SHIFTED, SAME CLASS; g† flag DISTANCE-DEPENDENT.

## Controls
- **K1 (code identity):** with T ≡ 1 the driver reproduces every committed number in cfg829/840/849/850/851_results.json
  (A, σ_A, χ², splits, z's, b, lgd, χ², b_lo, b_hi, d_pred, z) to < 1e-9 absolute, and every class string.
- **K2 (distances):** comoving distance vs analytic Einstein–de Sitter (Ω_m = 1) and pure Λ (Ω_m = 0) to < 1e-6 relative;
  T(h 0.70, Ω_m,nat = Ω_m,fid, no radiation) = 1 to < 1e-12; the g_bar identity (D_L/D_A)²/(1+z)⁴ = 1 to < 1e-12.
- **K3 (inputs):** NZ_SOURCE has 5 non-negative bins; lr_lenses has 181,477 lenses with 93,398 typ 0 / 88,079 typ 1 (CFG61 C3).
- **MUTATE** (`CFG885_MUTATE=1`, outputs `*_MUTATE`): T ≡ 1.3 on every dataset. Required responses: every A scales by 1.3 (to
  1e-9 relative); CFG829 blue canonical flips LAW HOLDS AT LOW g → INTERMEDIATE, so CFG885 classes CHANGED; CFG849/CFG850 split
  significances and classes unchanged (uniform-factor invariance); CFG851 b unchanged within 0.005 and log g† shifted by
  log10(1.3)/b within 0.05 dex (DSPHS ABOVE expected to hold, z ≈ 2.5–3). Any missing response is reported as a MUTATE fail.

## Not covered (disclosed in advance)
B21's selections are defined in fiducial units: isolation (3 h70⁻¹ Mpc, 10% of M★), M★ < 10^11 and the mass / colour / Sérsic
boundaries, the 0.03–3 h70⁻¹ Mpc radial range. Native distances move radii by ≲ 0.02 dex and M★ by ≲ 0.03 dex, shifting
memberships slightly; this cannot be redone from stacked public files and is not modelled. B21's cold-gas fraction f_cold(M★)
shifts at second order. The KiDS-1000 cosmic-shear SOM n(z) stands in for B21's source n(z). Lensing is assumed to trace the
dynamical g (as CFG801–805).

κ = ½ fitted; cold energy mass required; not theory closed; nothing here can favour the framework over ΛCDM.
