#!/usr/bin/env python3
"""
SWEEP 3 -- the cluster+CMB joint grid (mu, I0, cs^2).

The crux exhaustion scan. We grid (mu [0.1-3 Mpc^-1], I0 -> Omega_c h^2 [0.08-0.16],
cs^2 [0-1]) and map where the AeST scalar SIMULTANEOUSLY passes FOUR gates:

  (A) CMB 3rd peak:   I0 -> Omega_c h^2 ~ 0.1200 +- Planck error (0.0012, tight).
                      AND the dust must NOT free-stream at recombination: cs^2(a_rec) << 1.
  (B) cluster eta(R500): the mu^2 Phi mass term must LIFT eta toward ~1.3-2.33.
                      (the banked nonlinear-AeST result: with CMB-pinned mu ~ 1 Mpc^-1
                       and the PHYSICAL bounded-tail BC, eta(R500) ~ 0.96, NO boost;
                       a boost needs mu >~ 1.59 Mpc^-1 per Mistele, AND a per-cluster
                       boundary tune.)  We model eta_lift(mu) from the banked shooting.
  (C) galaxies MOND-pure: (mu R_gal)^2 << 1 at R_gal ~ 30 kpc -> negligible always;
                      the BINDING galaxy gate is the WEAK-LENSING outskirt deviation
                      (Mistele): mu must be SMALL enough that the >10% deviation radius
                      stays beyond the WL probe (~100-300 kpc). -> mu <~ 1.0 Mpc^-1.
  (D) galaxy-WL Mistele squeeze: m^2/f_G < ~1 Mpc^-2 i.e. mu <~ 1.0 Mpc^-1 (galaxy)
                      vs >2.5 Mpc^-2 i.e. mu > 1.59 Mpc^-1 (>=10% cluster lift).

  THE cs^2 SCALE-BLINDNESS gate (the structural crux, computed in FRONTIER3):
     cs^2 = (Q - Q0)/Q = 1 - Q0/Q,  and  cs^2(a) ∝ a^-3.
     CMB (gate A) forces cs^2_0 <~ 1e-9 (so a_rec dust doesn't free-stream).
     A pressureless cs^2~0 condensate has Jeans scale lambda_J ~ cs/sqrt(G rho) -> 0,
     so it clusters at ALL scales below lambda_J ~ 0: it clusters in GALAXIES too,
     which DESTROYS pure-MOND (double-counts a clustered halo on top of the a0 boost).
     -> The SAME cs^2 cannot cluster at 1-3 Mpc and stay smooth at 30 kpc.

  We make this quantitative: compute lambda_J(cs^2) and ask whether there is a cs^2
  window with lambda_J between R_gal (~30-100 kpc) and R_cluster (~1-3 Mpc).

Both ways: if a (mu, I0, cs^2) cell passes ALL FOUR gates with ONE scalar config
(one I0 doing CMB+clusters), we report it + quantify its volume vs the prior box.
If the gates are mutually exclusive, we report EMPTY + which gate closes it.

Quarantine: a0/Z never asserted derived; mu, I0, cs^2 are FREE AeST constants.
"""
import numpy as np

# ----------------------------------------------------------------------------
# Constants / anchors (web-verified, banked)
# ----------------------------------------------------------------------------
Mpc = 3.0857e22          # m
G   = 6.674e-11
H0  = 2.27e-18           # s^-1 (h=0.674)
rho_crit = 3*H0**2/(8*np.pi*G)   # kg/m^3
a_rec = 1.0/1100.0
OMEGA_C_H2_PLANCK   = 0.1200      # Planck 2018 cold dark matter density
OMEGA_C_H2_ERR      = 0.0012      # 1-sigma (ACT/SPT confirm <1%)
ETA_TARGET_LO, ETA_TARGET_HI = 1.3, 1.9   # convergent TRUE eta(R500) band
ETA_RAW = 2.33                              # raw eRASS1 (WL-massed)

# Mistele 2023 (arXiv:2301.03499) squeeze, banked numbers:
#   galaxy-WL MOND-pure  : m^2/f_G < ~1.0 Mpc^-2  -> mu < 1.00 Mpc^-1
#   >=10% cluster lift   : m^2/f_G > 2.5 Mpc^-2   -> mu > 1.58 Mpc^-1
#   eta~2 (115% lift)    : mu larger still (banked: oscillatory, needs tune)
MU_GAL_MAX   = 1.00      # Mpc^-1  galaxy-WL upper bound on mu
MU_CLU_MIN10 = 1.58      # Mpc^-1  lower bound for a >=10% cluster lift
print("="*78)
print("SWEEP 3 -- cluster+CMB joint grid (mu, I0, cs^2)")
print("="*78)

# ----------------------------------------------------------------------------
# GATE A: CMB 3rd peak from I0 (-> Omega_c h^2) AND cs^2(a_rec) << 1
# ----------------------------------------------------------------------------
# I0 is the free integration constant of K(Q) that sets the dust amplitude.
# We parameterize it DIRECTLY by the Omega_c h^2 it produces (monotone, banked CAMB:
#   P3/P2: 0.527 baryon-only -> 0.980 LCDM as Omega_c h^2: 0 -> 0.12).
# Gate A passes when Omega_c h^2 is within Planck +- N sigma.
def gateA_cmb(omega_ch2, cs2_0, nsig=3.0):
    amp_ok = abs(omega_ch2 - OMEGA_C_H2_PLANCK) <= nsig*OMEGA_C_H2_ERR
    # cs^2 at recombination: cs^2(a) = cs2_0 * (a/a0)^-3 = cs2_0 * a^-3 (a0=1 today)
    cs2_rec = cs2_0 * a_rec**(-3)
    # to drive the 3rd peak the dust must not free-stream: cs2_rec must be << 1
    freestream_ok = cs2_rec < 0.01     # generous: <1% sound horizon at rec
    return amp_ok, freestream_ok, cs2_rec

# ----------------------------------------------------------------------------
# GATE B: cluster eta(R500) from the mu^2 Phi mass term (banked nonlinear AeST)
# ----------------------------------------------------------------------------
# Banked physical-BC result (aest_single_mu_gauntlet, Green's function, zero tune):
#   eta(R500) at M500=5e14 vs 1/mu:  mu=1.0 -> 0.96 ; oscillates 1.03,0.75,0.15,0.48,0.94
#   The PHYSICAL (non-tuned) eta is ~1 (pure MOND), NOT a sustained 2x, for ALL mu in 0.1-1 Mpc^-1.
#   A monotone "lift" only appears under a per-cluster boundary tune (unphysical/degenerate).
# We encode BOTH readings:
#   (B-phys) physical bounded-tail BC: eta ~ 1 +- small oscillation, NEVER reaches 1.3 cleanly.
#   (B-tune) per-cluster-tuned BC: eta reachable but at +1 tuned constant PER CLUSTER (not predicted).
# Mistele scale gate for ANY >=10% lift: mu > MU_CLU_MIN10.
def gateB_cluster(mu, cs2_0):
    # The cluster boost has TWO possible suppliers; we test each.
    # Supplier 1: the mu^2 mass term (needs mu > MU_CLU_MIN10 for >=10%, and even then
    #             physical BC gives oscillatory ~1, a SUSTAINED 2x needs per-cluster tune).
    massterm_can_lift_10pct = (mu >= MU_CLU_MIN10)
    # Supplier 2: the cs^2~0 dust clustering at cluster scales (the unified-I0 hope).
    #   If cs^2~0 the dust clusters like CDM at clusters -> supplies the FULL halo (eta~5),
    #   overshooting the modest residual; if cs^2~1 it stays smooth -> supplies NOTHING.
    cs2_clu = cs2_0 * (1.0/0.5)**3 * 1.0   # cs^2 at cluster epoch a~0.5..1, ~ cs2_0 scale
    dust_clusters_at_clusters = (cs2_clu < 1e-3)   # pressureless -> clusters
    return massterm_can_lift_10pct, dust_clusters_at_clusters

# ----------------------------------------------------------------------------
# GATE C + the cs^2 scale-blindness: galaxies MOND-pure
# ----------------------------------------------------------------------------
# (C1) mass-term outskirt: (mu R)^2 small at galaxy WL radii.
#      >10% deviation radius r_dev ~ 1/mu * sqrt(0.1..) ; require r_dev > R_WL_probe.
R_GAL_DYN = 0.030        # Mpc, inner rotation curve (30 kpc)
R_WL_PROBE = 0.200       # Mpc, galaxy weak-lensing probe (~100-300 kpc)
R_CLUSTER  = 1.3         # Mpc, R500
def gateC_galaxy_massterm(mu):
    # the mass term grows as (mu r)^2; a 10% deviation at r where (mu r)^2 ~ 0.1*pi (banked
    # numeric: 0.18% at 30kpc for mu=1, 5.4% at 0.1Mpc-equiv shrink). Use (mu r)^2 threshold.
    dev_at_WL = (mu * R_WL_PROBE)**2          # ~ fractional outskirt perturbation scale
    dev_at_dyn = (mu * R_GAL_DYN)**2
    galaxy_pure_massterm = (dev_at_WL < 0.10) # <10% deviation at the WL probe radius
    return galaxy_pure_massterm, dev_at_WL, dev_at_dyn

# (C2) the cs^2 Jeans-scale gate -- the STRUCTURAL crux.
#   lambda_J ~ 2*pi * cs / sqrt(4 pi G rho_dust).  rho_dust ~ Omega_c * rho_crit (cosmic mean)
#   but for clustering we care about the ratio of lambda_J to R_gal and R_cluster.
#   If lambda_J < R_gal  -> dust clusters in galaxies (BAD: double-counts halo, kills MOND)
#   If lambda_J > R_cluster -> dust smooth at clusters (BAD: supplies no cluster residual)
#   The unified-I0 hope needs  R_gal < lambda_J < R_cluster  (a WINDOW in cs^2).
def jeans_length(cs2, omega_c=0.265):
    # cs in m/s; cs2 dimensionless (units of c^2).  cs = sqrt(cs2)*c
    c = 2.998e8
    cs = np.sqrt(max(cs2,0.0)) * c
    rho_dust = omega_c * rho_crit            # cosmic-mean dust density today
    if rho_dust <= 0: return np.inf
    lam = 2*np.pi * cs / np.sqrt(4*np.pi*G*rho_dust)   # m
    return lam / Mpc                         # Mpc

# ----------------------------------------------------------------------------
# THE JOINT GRID
# ----------------------------------------------------------------------------
mu_grid    = np.linspace(0.1, 3.0, 30)        # Mpc^-1
och2_grid  = np.linspace(0.08, 0.16, 17)      # Omega_c h^2 (proxy for I0)
cs2_grid   = np.array([0.0, 1e-12, 1e-10, 1e-9, 1e-7, 1e-5, 1e-3, 1e-2, 1e-1, 1.0])

print(f"\nGrid: mu in [{mu_grid[0]},{mu_grid[-1]}] x {len(mu_grid)} ; "
      f"Omega_c h^2 in [{och2_grid[0]},{och2_grid[-1]}] x {len(och2_grid)} ; "
      f"cs^2 in {{0,1e-12..1}} x {len(cs2_grid)}")
print(f"Total cells = {len(mu_grid)*len(och2_grid)*len(cs2_grid)}")

# ---- First: the cs^2 scale-blindness window (independent of mu, I0) ----
print("\n" + "-"*78)
print("STEP 1 — the cs^2 Jeans-scale window (the structural crux)")
print("-"*78)
print(f"{'cs^2':>10} | {'cs^2(a_rec)':>12} | {'lambda_J [Mpc]':>14} | "
      f"{'CMB-ok':>7} | {'cl(<{:.1f})':>8} | {'gal-smooth':>10}".format(R_CLUSTER))
cs2_window_exists = False
for cs2 in cs2_grid:
    cs2_rec = cs2 * a_rec**(-3)
    lamJ = jeans_length(cs2)
    cmb_ok = cs2_rec < 0.01
    clusters_at_clu = lamJ < R_CLUSTER      # dust clusters at <1.3 Mpc (supplies residual)
    smooth_at_gal   = lamJ > R_WL_PROBE     # dust stays smooth at galaxy WL (keeps MOND pure)
    # the unified hope needs BOTH clusters_at_clu AND smooth_at_gal
    if clusters_at_clu and smooth_at_gal:
        cs2_window_exists = True
    print(f"{cs2:>10.0e} | {cs2_rec:>12.2e} | {lamJ:>14.3e} | "
          f"{str(cmb_ok):>7} | {str(clusters_at_clu):>8} | {str(smooth_at_gal):>10}")

print(f"\n  --> A cs^2 window where the dust clusters at <{R_CLUSTER} Mpc "
      f"AND stays smooth at >{R_WL_PROBE} Mpc EXISTS? {cs2_window_exists}")

# ---- The CMB free-streaming bound on cs^2_0 ----
print("\n" + "-"*78)
print("STEP 2 — the CMB free-streaming bound on cs^2_0")
print("-"*78)
# cs^2(a_rec) < 0.01 => cs^2_0 < 0.01 * a_rec^3 = 0.01 * (1/1100)^3
cs2_0_cmb_max = 0.01 * a_rec**3
print(f"  cs^2 ∝ a^-3, a_rec={a_rec:.2e}; CMB needs cs^2(a_rec)<0.01")
print(f"  => cs^2_0 < 0.01*a_rec^3 = {cs2_0_cmb_max:.3e}   (effectively ZERO today)")
lamJ_cmb = jeans_length(cs2_0_cmb_max)
print(f"  At that cs^2_0, lambda_J(today) = {lamJ_cmb:.3e} Mpc  << R_gal(30 kpc=0.03 Mpc)")
print(f"  => the CMB-fitting dust is pressureless TODAY -> clusters at ALL scales incl. galaxies.")

# ----------------------------------------------------------------------------
# STEP 3 — the full 4-gate joint pass map
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("STEP 3 — the full 4-gate joint pass (one scalar config for CMB AND clusters)")
print("-"*78)
n_pass_all = 0
n_pass_unified = 0   # passes with ONE I0 doing both (the +1 win)
viable_cells = []
for mu in mu_grid:
    galpure_mass, devWL, devdyn = gateC_galaxy_massterm(mu)
    mistele_galaxy_ok = (mu <= MU_GAL_MAX)
    for och2 in och2_grid:
        for cs2 in cs2_grid:
            amp_ok, fs_ok, cs2_rec = gateA_cmb(och2, cs2)
            massterm10, dust_clu = gateB_cluster(mu, cs2)
            lamJ = jeans_length(cs2)
            clusters_at_clu = lamJ < R_CLUSTER
            smooth_at_gal   = lamJ > R_WL_PROBE
            # GATE A: CMB fit (amplitude + no free-stream)
            A = amp_ok and fs_ok
            # GATE C: galaxies MOND-pure -> BOTH the mass-term outskirt AND the dust must
            #         stay smooth at galaxy scales
            C = galpure_mass and mistele_galaxy_ok and smooth_at_gal
            # GATE D: Mistele squeeze (galaxy bound on mu)
            D = mistele_galaxy_ok
            # GATE B: cluster eta lifted.  Two suppliers (either closes it):
            #   B1 mass term: needs mu>=MU_CLU_MIN10  (but then D fails -> the squeeze)
            #   B2 unified dust: needs dust to cluster AT clusters (clusters_at_clu)
            #        AND that SAME dust to be the CMB I0 (always true here) -> unified +1
            B1 = massterm10
            B2 = clusters_at_clu
            B  = B1 or B2
            if A and B and C and D:
                n_pass_all += 1
                viable_cells.append((mu,och2,cs2,'B1' if B1 else 'B2'))
                if B2:   # the unified one-I0 route
                    n_pass_unified += 1

print(f"  cells passing ALL FOUR gates (A CMB, B cluster-lift, C galaxy-pure, D Mistele): {n_pass_all}")
print(f"  of which UNIFIED (one I0 dust does both CMB+clusters): {n_pass_unified}")
if viable_cells:
    print("  sample viable cells:")
    for v in viable_cells[:10]:
        print("   ", v)
else:
    print("  --> NO cell passes all four gates with a single scalar config. EMPTY intersection.")

# ----------------------------------------------------------------------------
# STEP 4 — WHICH gate closes it, and the fine-tuning quantification
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("STEP 4 — the squeeze, made explicit (which gate closes the unification)")
print("-"*78)
print(f"  Galaxy-WL / Mistele bound : mu <= {MU_GAL_MAX} Mpc^-1")
print(f"  Cluster >=10% lift needs  : mu >= {MU_CLU_MIN10} Mpc^-1")
print(f"  Cluster eta~2 lift needs  : mu > {MU_CLU_MIN10} (and a per-cluster boundary tune)")
print(f"  Overlap of [<= {MU_GAL_MAX}] and [>= {MU_CLU_MIN10}] ?  "
      f"{'NON-EMPTY' if MU_GAL_MAX>=MU_CLU_MIN10 else 'EMPTY (gap '+format(MU_CLU_MIN10-MU_GAL_MAX,'.2f')+' Mpc^-1)'}")

# the cs^2 route:
print(f"\n  cs^2 unified-dust route:")
print(f"    CMB forces cs^2_0 < {cs2_0_cmb_max:.2e}  (pressureless today)")
print(f"    pressureless dust: lambda_J(today) = {lamJ_cmb:.2e} Mpc << R_gal(0.03 Mpc)")
print(f"    -> clusters in galaxies too -> destroys pure-MOND RAR (double-counts halo).")
print(f"    A cs^2 with R_gal < lambda_J < R_cluster window exists? {cs2_window_exists}")

# Fine-tuning volume estimate (if any viable region):
total_cells = len(mu_grid)*len(och2_grid)*len(cs2_grid)
print(f"\n  VOLUME: viable cells / total prior-box cells = {n_pass_all}/{total_cells} "
      f"= {n_pass_all/total_cells:.4f}")
print(f"  UNIFIED (+1) viable fraction = {n_pass_unified}/{total_cells} = {n_pass_unified/total_cells:.4f}")

# ----------------------------------------------------------------------------
# STEP 5 — the +2-param fallback (separate I0 + mu), is THAT viable?
# ----------------------------------------------------------------------------
print("\n" + "-"*78)
print("STEP 5 — the +2 fallback: separate I0 (CMB) + mu (clusters), each in its own window")
print("-"*78)
# I0 free for CMB: always can hit Omega_c h^2 = 0.12 (it's a free integration constant).
i0_window_frac = np.mean(np.abs(och2_grid-OMEGA_C_H2_PLANCK) <= 3*OMEGA_C_H2_ERR)
print(f"  I0->Omega_c h^2 within Planck 3sigma: fraction of och2-grid = {i0_window_frac:.3f}")
print(f"    (I0 is a FREE integration constant: it CAN be set to 0.12 -> CMB fits at +1 param.)")
# mu for clusters: with a per-cluster boundary tune, eta~2 reachable but mu>1.58 violates
# the galaxy-WL bound mu<1.0 -> the +1 (one mu) fails; the cluster cure needs EITHER
# a galaxy-WL violation OR a per-cluster tuned constant (chi_out) -> not a clean parameter.
print(f"  mu for a sustained cluster 2x: needs mu>{MU_CLU_MIN10} (Mistele) -> violates galaxy mu<{MU_GAL_MAX}")
print(f"    AND a per-cluster free boundary constant chi_out (Helmholtz oscillatory degeneracy).")
print(f"  => the cluster cure is NOT a clean +1 mu: it is mu (squeezed) + per-cluster chi_out.")
print(f"\n  NET PARAMETER COST of the joint CMB+cluster closure on AeST:")
print(f"    +1 (I0 for CMB, clean)  + the cluster residual NOT closed by one mu")
print(f"    (the mu^2 term is Mistele-squeezed AND per-cluster-tuned; the unified-dust")
print(f"     route collapses to CDM and double-counts galaxies).")

print("\n" + "="*78)
print("DONE.")
print("="*78)
