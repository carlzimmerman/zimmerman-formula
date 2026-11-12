# CK1 amendment A1 (criteria f6f15f9e05), committed before any graded CK1 number

Adopts nothing. Kappa = 1/2 FITTED; not theory closed. No CK1 gate number exists when this is committed (only the
criteria and the script are on disk; the script has not been run).

## From the coordinator (CK4 ea06286d99 context; HOLD_KERNEL_REREAD_2026_11_07.md)

1. **(b) X-COP and groups at 500-550 km/s are bracketed, never extrapolated into a pass.** No own resolution run is
   feasible (section 3 of the criteria). At 500, 525, 550 the amount is the monotone bracket [eps(575), eps(0)]: these
   are bounds (a smaller kick cannot retain less than at 575, nor more than with no kick), not readings of a node. The
   per-bin line value is computed and reported but carries no verdict weight on its own: the cell is PASS only if both
   bracket ends (and the line value) pass, FAIL only if all fail, otherwise NO VERDICT. This is the frozen cell rule,
   restated so that no 500-550 pass can come from the extrapolation.
2. **(c) Trigger mass.** L388's trigger (and CK1's RM) has no halo-mass threshold: decay wherever the local x~ > 5
   (L365), i.e. every system that virialises sheds. Reported row (not graded): M_min = 1e11 and 1e12 Msun applied to the
   system's own mass (1 + C_f) M_b; SPARC galaxies below M_min keep f = C_f (nothing shed), G1 re-read at the release /
   z_F 0 cell; whether the MW sheds is stated. CK4's forest window (v_k < ~560 km/s at M_min >= 1e11) is quoted, not
   regraded.
3. **(d) / HOLD.** No QX3 iter2 lensing-shape number and no SV5 web-row number is used anywhere in CK1. G9 / the web row
   is reported as "PENDING GL1/GL3", not graded. The lane label is at most "CANDIDATE on G1-G8 + T + MW (G9 pending
   GL1/GL3)".

## Implementation choices fixed now (before numbers)

4. **Coma UDGs (G5): Coma (A1656) is not among the X-COP clusters on disk.** The host term uses A2319 (M500 7.3e14,
   the on-disk cluster closest to Coma) as a proxy: carrier density at r = 300 kpc = C_f x eps_top(hi end) x the
   baryon density of A2319's profile there (baryon-traced, the densest reading). Own term from RM on a Plummer UDG.
5. **G2 is graded on GB1's 35 X-COP points (7 clusters: A1795, A2029, A2142, A2319, A644, A85, ZW1215).** KA6 uses
   XR13's 12-cluster set. The X-COP G2 cell is the cell rule over {line value, lo end, hi end} x the 4 RM shape cells.
   The NA2-band profile reading uses fixed shapes (HSE, baryon, gas, stars) at the graded amount, release / z_F 0.
6. **KiDS (G7):** GB1 carries no lens baryon mass; each K1 point's enclosed baryon mass is taken from its own
   g_bar R_med^2 / G (Hernquist host, a = 3 (M_b/1e11)^0.3 kpc), and f = M_c(<R_med)/M_b.
7. **MW:** the v_c(R0) shift is taken on the Hernquist model (law with and without the carrier), added to X5's slack.
   Delta K_z uses the frozen 2 x 1.1 kpc x rho_c(R0) (a nu-boosted version is reported only). rho at R0 and at the
   dSph host distances is from M_c at +-5 % of the radius.
8. **G8:** GB1's G8 with b = 1 (the carrier mass inside 9.58 AU at the solar-circle density is reported; it is
   negligible against M_sun). The blend acts there; the record's G8 numbers for the adopted action stand.
9. **G3 too-little / too-much:** a G3 FAIL is kept only if the f* 0 median residual is positive (carrier too little)
   in every bracket end; otherwise G3 reads NO VERDICT (criteria section 3).
10. **SPARC tail:** v_flat = mean of the three outermost V in QX5's mask; RM evaluated at each galaxy's own radii;
    r_F reported = the parents' median radius; retention f_ret and v_esc(r_F) per tail galaxy per v_k and cell in
    the JSON (for CK3, with the single-shell curve and L388's bins against the Newtonian proxy sqrt(2 G M/1 Mpc/h)).

Kappa = 1/2 FITTED; not theory closed.
