# CFG912 FROZEN CRITERIA: is the red/spheroidal isolated-lens excess partly the framework's own catalogue two-halo term? (committed alone, before any script)

**ID:** block CFG910–919 (reserved in the LEDGER, 2026-10-20), CFG912 = "red-lens excess vs the catalogue two-halo term".

## Why

- The open sector. At 10^−13.3 ≤ g_bar < 10^−11.9 m/s², B21's isolated **red** lenses sit above the law and **blue** ones on it
  (CFG829/849). After CFG667's LePhare M★ offset (+0.123 dex on red g_bar) CFG850 has, canonical:
  **A_red 1.451, A_blue 1.016, split 4.0σ** (uncorrected 1.587 / 1.016, 5.0σ); alt 1.324 / 0.928 (4.0σ). CFG885: survives
  native distances. CFG851: a clean empirical excess law for red lenses; its cause is open.
- CFG903 built the framework's catalogue two-halo term (observed KiDS-bright neighbours, each with baryons + catchment cold
  energy, no free amplitude). Hosts of satellites that leak through the photo-z isolation carry 40–87% of it at 1 Mpc.
  Red galaxies live in denser environments, so their neighbour term may be larger at the radii of the RAR window.
- Question: how much of the red − blue amplitude split does the red − blue difference in that term explain?

## Inputs (on disk; read-only; no download)

- B21 colour-bin RAR files + covariance, read by CFG850's code path (cfg829.py `load`/`amp`/`nu_e`, exec'd read-only exactly as
  cfg850.py does). Window, law (ν_e), footings and shifts exactly as CFG850.
- CFG903's stage arrays `../_external_data/cfg903_work/cfg903_stage.npz` (lens table = I0 ∪ I5 lenses in B21's mass bins,
  random clones, B21-like weights W_l, C1′ completeness factors, jackknife patches, neighbour pool). CFG903's `cfg903_lib.py`
  imported read-only (distances, catchment fixed point N_of_declared, edge_of, NGRID, d and M_b cell definitions).
- Colour: u−r = LePhare MAG_ABS_u − MAG_ABS_r from `KiDS_DR4_brightsample_LePhare.fits` for each table lens (rows located with
  CFG903's pool definition). The record's label is u−r > 2.0 (lr_lenses `typ`); B21's cut is 2.5 in B21's own photometry.
- CFG903's committed-run pair histograms `cfg903_hist_bin{1-4}.npz` (only for control K0b).

## The two-halo term per colour class, on B21's g_bar bins (framework-native; no ΛCDM halo model; no free amplitude)

**Neighbours and their mass: CFG903 primary, unchanged.**
- Pool objects (masked = 0) with projected physical separation d < 4.61 Mpc and |Δχ_phot| < W (W = 500 Mpc primary).
- Each carries its baryons (point) + 5.364 N_j M_b,j catchment cold energy (N_j from CFG902's declared fixed point at the
  centre of its 0.05-dex log M_b cell) on CFG804's truncated law profile (P1), r_M = √(G M_b/a0) per footing.
- C1′ per-pair completeness weight 1 + f_C1′(z_l)·[m_lim ≤ log M★_j < m_lim + 0.5] (CFG903 A1).
- Random-clone subtraction: ΔΣ_2h = ΔΣ(lenses) − ΔΣ(clones); each clone inherits its lens's class, mass and weight.

**Exclusion E1 (primary).** Neighbours less massive than the lens (catalogue M_b,j < M_l) with d < r_x are dropped;
r_x = edge(N_l,snap) · √(G M_l/a0), N_l from N_of_declared(log M_l) snapped to NGRID (as CFG903's `rx_of`). Here M_l is the
lens's **catalogue** M_gal (no profiled mass: this lane has no one-halo fit). In an M★-shifted variant the shifted classes use
M_l·10^shift for r_x (the flag stays on catalogue masses, so lens and neighbour masses are compared on one scale).

**Mapping onto B21's RAR bins.**
- B21's 15 log g_bar bins, nominal edges g_k = 10^(−15 + 0.246606 k), k = 0…15 (1e-15 to 5e-12).
- Lens–source pairs of lens l fall in bin k at R ∈ [√(G M_l/g_{k+1}), √(G M_l/g_k)]. These radii are set by the masses
  used to bin; an M★ shift relabels g_bar but does not move the source pairs, so annuli always use catalogue M_l.
- Per-lens weight in bin k = W_l × annulus area (∝ W_l M_l). Annulus-area-averaged ΔΣ (the CFG903 identity
  ΔΣ̄ = [∫2M(<R)/R dR − ΔM]/A). Stacked: Δg_k = 4 G ΔΣ_2h,k (B21 Eq. 7, the convention of cfg829's g_obs).
- Implementation (exact for point masses): separations are histogrammed in x = d/ρ_l, ρ_l = √(G M_l/g_10), on log bins of
  0.0246606 dex aligned so every annulus edge is a bin edge; neighbour mass in CFG903's 0.05-dex cells; lens mass in 0.1-dex
  cells (used only for the extended-profile scale ratio ρ_l/r_M,j and for N_l); flag (less massive) and |Δχ| bins
  [0,300), [300,500), [500,1000) kept. Histogram weight W_l × c1w × M_b,j; normalisation Σ W_l M_l per class. Extended
  cold-energy kernels come from tabulated off-centre enclosed fractions F(u, v) and G(u, v) = ∫₀ᵘ 2F/u′ du′ per neighbour
  shape (CFG903's F2 on CFG903's profiles), averaged over each x bin assuming neighbours uniform in area within the bin.
- Bins k = 5…13 are computed; the window picks bins by the (shifted) file g_bar exactly as CFG850.

## Statistic (per footing: canonical 9.3603e-11, alt 1.1312e-10; never pooled)

For colour class c ∈ {red, blue} in a variant with shifts (s_red, s_blue):
- A_c = CFG850's amplitude (g_bar,s = g_bar·10^s_c; law g_bar,s ν_e(g_bar,s/a0); window on g_bar,s).
- A_c^corr = the same amplitude fitted to g_obs − Δg_c (equivalently, model = A·g_law + Δg_c). δA_c = A_c − A_c^corr.
- S0 = A_red − A_blue.  **f_env = (δA_red − δA_blue)/S0** (the share of the split the environment difference explains).
- **z_corr = (A_red^corr − A_blue^corr)/√(σA_red² + σA_blue²)**, σ from the data covariance exactly as CFG850.

**Primary variant:** I0, colour cut u−r 2.0, shifts (+0.123, 0) [CFG850's corrected row], W 500, P1, E1, C1′, nominal edges.

## Classes (per footing; canonical is the headline, alt gets its own class)

- **ENVIRONMENT EXPLAINS:** f_env ≥ 0.80 AND z_corr < 2.
- **PARTIAL:** f_env ≥ 0.20 and not EXPLAINS.
- **NOT ENVIRONMENT:** f_env < 0.20 (labelled "OPPOSITE SIGN" if f_env < 0).
- Jackknife (50 sky patches, delete-one, primary only): σ_jk(f_env) reported; a class whose boundary (0.20 or 0.80) lies
  within 2σ_jk of f_env is flagged "near boundary".

## Brackets (one at a time from the primary; class each; the robustness line lists every bracket that changes the class)

| id | change |
|---|---|
| ISO-f30 | I1 (CFG903's f30: W 30 Mpc) instead of I0 |
| ISO-B21n | I5 (CFG903's count-matched sample, W_B 6.1 Mpc, 259,963 vs B21's 259,383) |
| P0 / P2 | neighbour cold energy as a point / on the law shape cut at 2 s_max |
| W300 / W1000 | photo-z window |
| CUT-2.5 | colour cut u−r 2.5 (on the same LePhare MAG_ABS system) |
| MSTAR-0 | no M★ correction: shifts (0, 0) (CFG829/849 amplitudes) |

**Reported only (no class weight):** shifts (+0.20, 0) and (+0.123, +0.05); E0 (no exclusion; double counts) and E2 (hosts
inside r_x dropped too); host share (flag 0) of each class's term; annulus edges centred on the file's g_bar values
(± 0.123303 dex); z_corr with the jackknife variance of δA_red − δA_blue added; A_blue^corr against 1 (what the term does to
the "blue lenses on the law" statement); the multiplier on Δg_red − Δg_blue that would give z_corr = 2 and S = 0; the
Sérsic split corrected with the colour-proxy vectors (red → spheroid, blue → disc), since there are no Sérsic indices on disk.

## Controls (binding unless marked)

- **K0a:** CFG903's stage table restricted to I0 equals lr_lenses (ra, dec, z, Mgal) for the 181,431 table lenses, and the
  reconstructed u−r > 2.0 label equals lr_lenses `typ` exactly; I1 ⊂ I0 ⊂ I5.
- **K0b:** this lane's pair loop, accumulated with CFG903's v0 weights and cells, reproduces CFG903's committed-run lens and
  random histograms for each bin (max |Δ| ≤ 1e-9 × max cell).
- **K1:** with Δg ≡ 0 the lane reproduces every row of CFG850's committed `cfg850_results.json` (A_red, A_blue, z_colour,
  A_sph, A_disc, z_sersic; 10 rows) with max |Δ| = 0.
- **K2a:** F and G table interpolation vs direct CFG903 F2 at random points: |ΔF| ≤ 2e-3. Annulus kernel (table route) vs
  CFG903's independent brute-force polar F with Gauss–Legendre quadrature: |Δ| ≤ 3e-3 × the point-mass kernel 2 ln(X₂/X₁).
- **K2c:** a uniform neighbour field gives |Δg| ≤ 2e-3 of its Σ₀-equivalent in every computed bin (P1 and P2; log M_b 10.5 and
  12.0; lowest and highest lens-mass cell; both footings).
- **K3:** random halves A − B: the window-mean of the red and blue two-halo vectors is within 3σ_jk of zero.
- **MUTATE** (`CFG912_MUTATE=1`, pairs rerun, separate outputs): one synthetic host of log M_b 11.325 (above every lens; its
  cold energy assigned by the same rule; c1w = 1) at physical d = 0.4 Mpc, Δχ = 0, injected around every 10th I0 red (u−r > 2.0)
  lens in table order and seen only by that lens. **Recovered** if (i) the blue vectors are unchanged (max |Δ| = 0) and (ii) with
  P0 the red Δg change in every window bin matches a direct per-lens computation (each lens's exact annulus radii and d) to ≤ 1%.
  f_env must rise. Zeroing the two-halo term is K1.

## Hand expectation (stated before any number; not binding)

The red excess in the window is about 2.5–8 Msun/pc² of ESD (0.45 × g_law/4G), while CFG903's all-lens catalogue term at
0.4 Mpc is 0.3–0.5 Msun/pc². The window annuli (X = R/ρ_l ≤ 2.34; ≤ 3.11 for the shifted red window) lie inside or at the
lens's own edge (x_x ≈ 3.03 canonical, 2.75 alt; × 1.15 for shifted red), so mainly hosts and the outer parts of neighbours'
cold energy act there. Expected: NOT ENVIRONMENT or low PARTIAL.

## Limits and disclosures (stated in advance)

- **Proxy sample.** The amplitudes are B21's published colour bins (B21's sample, isolation and u−r 2.5 cut, not reproducible
  on disk); the two-halo term is computed for the record's reconstruction (I0, LePhare u−r 2.0). ISO-B21n and CUT-2.5 bracket
  this; nothing more can be done with stacked public files.
- B21's radial limits on lens–source pairs in the RAR stack (if any) are not modelled; no annulus clipping.
- Catalogue lens masses (no profiling); neighbours' photo-z mass errors, true-z lensing efficiency, catchment sharing (sharing
  can only lower the term), faint neighbours beyond C1′, and the lens's own share of a host's catchment are not modelled.
- The split σ ignores cross-covariance between the two colour bins (as CFG850). The two-halo term's own noise enters only
  through the jackknife (reported).
- **Compute.** One core (OMP_NUM_THREADS=1, nice 10); each process < 1.2 GB current RSS and < 20 min, enforced by a watchdog;
  staged `cfg912_colour.py` → `cfg912_pairs.py BIN` (4 processes) → `cfg912_score.py`. Large arrays go to
  `../_external_data/cfg912_work/` (not committed). If a stage cannot fit, the lane stops and reports what it needs.

κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10, never pooled; raw KiDS data, framework-native neighbours (no ΛCDM halo-model
two-halo term); not theory closed; nothing here can say the data favour the framework.
