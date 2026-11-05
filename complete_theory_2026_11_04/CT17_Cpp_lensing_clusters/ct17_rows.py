"""CT17: G7 rows for C''. Arithmetic on record numbers (sources in comments); no fitting, no scan.
kappa = 1/2 FITTED; not theory closed."""
import math
L = math.log10
# (a) local a0 shift in a 1e14 Msun cluster, CT13 ct13_review.out:23 (can), :27 (alt), dex
da0 = {"canonical": 9.97e-11, "alt": 7.78e-11}
# law mass response d ln M / d ln a0 <= 0.5 (deep-MOND limit; smaller at g > a0)
# (b) phi perturbation: delta rho_phi / rho_DE ~ max|grad dphi|/phidot, CT13 out:23,27
grad = {"canonical": 4.4e-6, "alt": 3.5e-6}
OmL, Delta500 = 0.6847, 500.0       # rho_DE/rho_crit (footing encoding, CT8 out:3); R500 mean overdensity
# (c) v3s static dust term = H2 AeST term at mu = mu_K <= 0.1 Mpc^-1 (V3_FULL_PICTURE.md:41,47)
# H2 h2_aest_clusters.out:19 (can), :20 (alt): bin ratios AeST/law, bins 1-5 (to ~1 Mpc) 1.00-1.01;
# best Delta lifts MID 1.657 -> 1.639 (can), i.e. <= 1.1 %; galaxy guard <= 0.003 at r <= 200 kpc (out:51)
boost_xcop_max = {"canonical": 1.02, "alt": 1.02}   # upper bound over bins 1-5 and the Delta scan
guard = 0.003
xcop_law = {"canonical": 2.934, "alt": 2.719}       # LW1 lw1_xcop.out:3, :11
kids_short = (0.089, 0.116)                          # LE1 README.md:97
red_need = {"canonical": 1.313, "alt": 1.200}        # CT4_REPORT.md:20 (CW6)
bullet_law = {"canonical": (40, -0.068), "alt": (51, -0.111)}  # (peak-gas offset main 40 / sub 51 kpc, X32 README:29; dkappa can -0.068 / alt -0.111, DB1 db1_checks.out:5)
for f in ("canonical", "alt"):
    dM_a0 = 0.5 * da0[f]
    dM_phi = L(1 + grad[f] * OmL / Delta500)
    print(f"[{f}] (a) a0 shift -> d log M <= {dM_a0:.1e} dex; (b) phi perturbation share in R500 -> {dM_phi:.1e} dex; inherit v3s rows: {max(dM_a0, dM_phi) < 1e-3}")
    lo, hi = xcop_law[f] / boost_xcop_max[f], xcop_law[f]
    print(f"[{f}] R1 X-COP: C'' M_HSE/M = {lo:.2f}-{hi:.2f} (needs ~1.0); C'' supplies x{1.0:.2f}-{boost_xcop_max[f]:.2f} of the x{xcop_law[f]:.2f} needed; gap {L(lo):+.3f} to {L(hi):+.3f} dex -> FAIL")
    add = L(1 + guard)
    print(f"[{f}] R3 KiDS R<=0.3 Mpc: C'' adds <= {add:+.4f} dex, colour-blind; gap {kids_short[0]-add:+.3f} to {kids_short[1]-add:+.3f} dex; red needs x{red_need[f]:.3f}, gets x{1+guard:.3f} -> FAIL")
print(f"R2 Bullet: dust term tracks |Phi| of the gas-dominated baryons (gal200 share {guard}); peaks stay on the gas, 40 / 51 kpc (main/sub), dkappa {bullet_law['canonical'][1]:+.3f} can / {bullet_law['alt'][1]:+.3f} alt; observed ~200 kpc on the galaxies -> FAIL, wrong sign, ~150-160 kpc short")
