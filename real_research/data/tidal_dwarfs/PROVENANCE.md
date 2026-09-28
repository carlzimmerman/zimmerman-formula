# Tidal dwarf galaxies: provenance

`lelli2015_tdg.csv` was transcribed on 2026-09-27 from the tables of **Lelli et al. 2015, A&A 584, A113**, "Gas dynamics
in tidal dwarf galaxies: disc formation at z = 0" (arXiv:1509.05404v1). The source is the arXiv PDF, read page by page.
Nothing was typed from memory.

| Columns | Source table |
|---|---|
| `dist_Mpc`, `host_LK_1e10Lsun` (the host's K-band luminosity) | Table 1 (galaxy sample) |
| `i_deg`, `R_out_kpc`, `V_rot_kms`, `sigma_HI_kms`, `t_orb_Gyr`, `tmerg_over_torb` | Table 7 (3D kinematic models) |
| `V_circ_kms`, `M_dyn_1e8`, `M_atom_1e8`, `M_star_1e8`, `M_mol_1e8`, `M_bar_1e8`, `Mdyn_over_Mbar` | Table 8 (mass budget assuming dynamical equilibrium) |
| `D_p_kpc`, `gNe_over_a0`, `gNi_over_a0`, `V_ISO1/2`, `V_EFE1/2` (the paper's own MOND predictions) | Table 9 (MOND analysis) |

Notes on the columns:
- `tmerg_over_torb` for VCC 2062 is printed as a range, 0.4–0.8; the file stores its midpoint, 0.6.
- `Rout_over_hHI` is taken from the text of Sect. 5.2.1, which gives R_out ≃ 2 h_HI except for NGC 5291N (R_out ≃ h_HI).
  The asymmetric-drift correction (the paper's eq. 2) is V_circ² = V_rot² + σ_HI² R/h_HI.
- The paper's MOND formula is its eq. 4, which is Famaey & McGaugh (2012) eq. 60:
  a_i = g_Ni ν((g_Ni + g_Ne)/a0) + g_Ne[ν((g_Ni + g_Ne)/a0) − ν(g_Ne/a0)], with a_i = V²/R_out.
  - The interpolation function is ν_n(y) = [1 − exp(−y^{n/2})]^{−1/n}, for n = 1 and 2.
  - g_Ni = G M_bar/R_out².
  - g_Ne = G M_host/D_p², with M_host = L_K × 0.6 M☉/L☉ and M_host varied by a factor of 2.

Caveat stated by the authors: the HI discs have completed less than one orbit since the interaction (t_merg/t_orb ≈
0.2–0.8). The dynamical masses therefore assume equilibrium. Their simulations (Fig. 12) suggest M_dyn/M_real → 1 ± ~0.1
within a few 100 Myr.

Public catalogue data. No personal information.
