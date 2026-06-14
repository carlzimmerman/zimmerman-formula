#!/usr/bin/env python3
"""
DENSITY-LAW a0 AT ell = 1/mu ~ 1 Mpc (the AeST scalar Compton wavelength) -- the hard double constraint.
========================================================================================================
Framework: a0 = (c/2) sqrt(G rho_DE) = 9.36e-11  (the de Sitter-Unruh 'local Friedmann' a0 ~ c H_local).
The density reading generalizes this to a0(x) = (c/2) sqrt(G rho_total,smoothed-over-ell), where
rho_total = rho_DE + rho_matter,smoothed.  rho_DE = Omega_L rho_crit = 6.4e-27 kg/m^3.

CANDIDATE SCALE: ell = 1/mu, the AeST scalar Compton wavelength, CMB-pinned at ~1 Mpc (Skordis-Zlosnik
2021; Verwayen-Skordis-Zlosnik 2024 require m^2/f_G <~ 1 Mpc^-2 => 1/mu >~ 1 Mpc).  Below 1/mu the dark
field is locally uniform; above it tracks structure.  So the NATURAL smoothing kernel width for the
density that sets a0 is ell = 1/mu ~ 1 Mpc.

THE TWO TESTS (a SINGLE ell must do both):
 (1) GALAXY RAR: smooth rho_total over ell around each of 175 real SPARC galaxies, get a per-galaxy a0,
     refit the RAR, and measure the scatter.  If smoothing inflates scatter past ~0.13 dex, DEAD.
 (2) CLUSTERS: smooth rho_total over ell for real eRASS1 clusters, get the in-cluster a0 boost, and
     compute eta(R500).  Must land ~1.2-1.5 (not over-close eta<1).

HONESTY (#1 rule, both ways): ell is DERIVED from the framework (the AeST 1/mu), NOT tuned to hit
1.2-1.5.  Whatever the numbers say -- even if they break galaxies or leave a deficit -- is the answer.
a0/Z never asserted derived (quarantine).

Run:  python density_a0_ell_1mpc_test.py    (numpy, scipy, astropy)
"""
import glob, math, os, sys
import numpy as np
from scipy.optimize import minimize_scalar

# ---------- constants (SI) ----------
c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0856775814913673e19
Mpc  = 3.0856775814913673e22
mp   = 1.67262e-27

H0   = 67.4e3/Mpc
Om_L, Om_m = 0.685, 0.315
rho_crit = 3*H0**2/(8*np.pi*G)          # 9.0e-27 kg/m^3
rho_DE   = Om_L*rho_crit                # 6.2e-27 kg/m^3 (dark energy)
rho_m_cosmic = Om_m*rho_crit            # 2.8e-27 kg/m^3 (cosmic mean matter)

a0_formula = lambda rho: 0.5*c*np.sqrt(G*rho)
A0_DE   = a0_formula(rho_DE)            # = 9.36e-11   (the canonical framework a0)
A0_TOT  = a0_formula(rho_crit)          # = 1.13e-10   (the rho_total cosmic footing, ~cH0)

ELL = 1.0*Mpc                          # ell = 1/mu, CMB-pinned AeST scalar Compton wavelength
V_ELL = (4.0/3.0)*np.pi*ELL**3         # volume of the 1 Mpc smoothing ball

DATA_S = os.path.join(os.path.dirname(__file__), "..", "..", "real_research", "data", "sparc_data")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "real_research", "data"))
from _load_erass1 import load_clean


# ======================================================================================
#  PART 0 -- the scale and what a 1 Mpc smoothing does to the density (sanity anchors)
# ======================================================================================
def part0():
    print("="*92)
    print("PART 0 -- ell = 1/mu = 1 Mpc, and the density a0 = (c/2)sqrt(G rho_total,smoothed)")
    print("="*92)
    print(f"  rho_crit   = {rho_crit:.3e} kg/m^3")
    print(f"  rho_DE     = {rho_DE:.3e} kg/m^3   -> a0(rho_DE)   = {A0_DE:.3e}  (= 9.36e-11, canonical)")
    print(f"  rho_total  = {rho_crit:.3e} kg/m^3 -> a0(rho_crit) = {A0_TOT:.3e}  (~cH0, superset footing)")
    print(f"  ell = 1/mu = 1 Mpc;  smoothing ball V = (4/3)pi ell^3 = {V_ELL:.3e} m^3")
    print(f"                       = {V_ELL/Mpc**3:.3f} Mpc^3,  M for rho_crit = {rho_crit*V_ELL/Msun:.3e} Msun")
    print()


# ======================================================================================
#  PART 1 -- GALAXY RAR (the make-or-break)
# ======================================================================================
# Each SPARC galaxy + its ~Mpc environment.  The density that sets a0 is rho_total smoothed
# over a 1 Mpc ball CENTERED ON THE GALAXY.  rho_smoothed = rho_DE + (M_within_1Mpc)/V_ELL.
# M_within_1Mpc = the galaxy's own halo + group/field environment inside 1 Mpc.
#
# We estimate M_within_1Mpc per galaxy from the baryonic mass via abundance matching, then
# add the cosmic-mean matter as the floor (a field galaxy at least sits in the cosmic web at
# ~mean density).  This is the framework-favorable reading: a galaxy disk is NOT smoothed to
# its clumpy 1e-21 density (that is the dead local reading) -- it is smoothed to its 1 Mpc
# environment, which for an isolated L* galaxy is a ~1e12 Msun halo in a 1 Mpc ball.

def galaxy_baryonic_mass(path, ml_disk=0.70, ml_bulge=0.70):
    """Total baryonic mass of a SPARC galaxy from the outermost rotmod point: M_b = V_bar^2 R / G."""
    last = None
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"): continue
            p = line.split()
            if len(p) < 6: continue
            try: r, vobs, ev, vgas, vdisk, vbul = (float(p[i]) for i in range(6))
            except ValueError: continue
            last = (r, vgas, vdisk, vbul)
    if last is None: return None
    r, vgas, vdisk, vbul = last
    vbar2 = vgas*abs(vgas) + ml_disk*vdisk*abs(vdisk) + ml_bulge*vbul*abs(vbul)
    if vbar2 <= 0 or r <= 0: return None
    # M_b(<R_last) = V_bar^2 R / G  (km/s, kpc)
    Mb = (vbar2*1e6)*(r*kpc)/G
    return Mb   # kg


def halo_from_baryon(Mb_kg):
    """Stellar-to-halo: Mb ~ f_b_eff * Mhalo.  Use the standard SHM peak ~ f_b/5 = 0.03 baryon
    retention at L* (Mbar/Mhalo ~ 0.03 near 1e12 Mhalo).  We invert conservatively."""
    Mb = Mb_kg/Msun
    # piecewise SHMR-ish: low-mass dwarfs retain less, L* ~ 0.03
    # Use Moster-like ratio Mb/Mh ~ 0.03 at L*, falling toward dwarfs.  A simple robust proxy:
    # Mhalo ~ Mb / 0.03 (i.e. baryon-to-halo ~ 0.03 typical for SPARC), floored at Mb/0.17 (no DM).
    Mh = Mb/0.03
    return Mh*Msun   # kg


def part1():
    print("="*92)
    print("PART 1 -- GALAXY RAR under the density-a0 smoothed over ell = 1 Mpc")
    print("="*92)
    paths = sorted(glob.glob(os.path.join(DATA_S, "*_rotmod.dat")))
    print(f"  SPARC galaxies found: {len(paths)}")

    # ---- per-galaxy a0 from the 1 Mpc-smoothed total density ----
    per = {}   # path -> a0_gal
    rho_list, a0_list, Mh_list = [], [], []
    for p in paths:
        Mb = galaxy_baryonic_mass(p)
        if Mb is None:
            per[p] = A0_DE; continue
        Mh = halo_from_baryon(Mb)
        # mass of total matter inside the 1 Mpc smoothing ball centered on the galaxy:
        #   the galaxy's halo (fits entirely well within 1 Mpc; halo r_vir ~ 200-300 kpc)
        #   + the cosmic-mean matter filling the rest of the ball (the field floor).
        # Conservative framework-FAVORABLE: take max(halo-in-ball, cosmic-mean-ball).
        M_halo_in_ball = Mh                               # halo sits inside the 1 Mpc ball
        M_cosmic_floor = rho_m_cosmic*V_ELL               # cosmic-mean matter in the ball
        M_matter = M_halo_in_ball + M_cosmic_floor
        rho_sm = rho_DE + M_matter/V_ELL                  # rho_total smoothed over 1 Mpc
        a0g = a0_formula(rho_sm)
        per[p] = a0g
        rho_list.append(rho_sm); a0_list.append(a0g); Mh_list.append(Mh/Msun)
    rho_list = np.array(rho_list); a0_list = np.array(a0_list); Mh_list = np.array(Mh_list)
    print(f"  per-galaxy halo mass (1e12 Msun)  : median {np.median(Mh_list)/1e12:.2f}, "
          f"[{np.percentile(Mh_list,10)/1e12:.2f}, {np.percentile(Mh_list,90)/1e12:.2f}] (10-90%)")
    print(f"  smoothed rho/rho_DE               : median {np.median(rho_list)/rho_DE:.2f}, "
          f"[{np.percentile(rho_list,10)/rho_DE:.2f}, {np.percentile(rho_list,90)/rho_DE:.2f}]")
    print(f"  per-galaxy a0 (1e-10)             : median {np.median(a0_list)/1e-10:.3f}, "
          f"[{np.percentile(a0_list,10)/1e-10:.3f}, {np.percentile(a0_list,90)/1e-10:.3f}]")
    print(f"  a0 spread (max/min)               : {a0_list.max()/a0_list.min():.2f}x")
    print()

    # ---- build the RAR points, then measure scatter for: (a) universal a0; (b) per-galaxy a0 ----
    def load_pts(per_a0=None, a0_uni=A0_DE, ml_disk=0.70, ml_bulge=0.70):
        gbar, gobs, a0arr = [], [], []
        for p in paths:
            a0g = per_a0[p] if per_a0 is not None else a0_uni
            with open(p) as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#"): continue
                    q = line.split()
                    if len(q) < 6: continue
                    try: r, vobs, ev, vgas, vdisk, vbul = (float(q[i]) for i in range(6))
                    except ValueError: continue
                    if r <= 0 or vobs <= 0: continue
                    if ev <= 0 or ev/vobs > 0.10: continue
                    vbar2 = vgas*abs(vgas)+ml_disk*vdisk*abs(vdisk)+ml_bulge*vbul*abs(vbul)
                    if vbar2 <= 0: continue
                    rm = r*kpc
                    go = (vobs*1e3)**2/rm
                    gb = (vbar2*1e6)/rm
                    if gb <= 0 or go <= 0: continue
                    gbar.append(gb); gobs.append(go); a0arr.append(a0g)
        return np.array(gbar), np.array(gobs), np.array(a0arr)

    # dS-Unruh (framework's own) interpolation: g_obs = sqrt(g_bar^2 + g_bar a0)
    def model_dsunruh(gbar, a0): return np.sqrt(gbar**2 + gbar*a0)
    # McGaugh interpolation for cross-check
    def model_mcgaugh(gbar, a0):
        x = np.sqrt(gbar/a0); return gbar/(1.0-np.exp(-x))

    def scatter(gbar, gobs, a0arr, model):
        pred = model(gbar, a0arr)
        return float(np.sqrt(np.mean((np.log10(gobs)-np.log10(pred))**2)))

    print("  RAR scatter (dex), Upsilon=0.70, framework dS-Unruh nu  g_obs=sqrt(gbar^2+gbar a0):")
    # baseline: single universal a0 (the standard RAR)
    gb0, go0, _ = load_pts(per_a0=None, a0_uni=A0_DE)
    # also fit the single best universal a0 (the true baseline floor)
    def best_uni(gbar, gobs, model):
        f = lambda la: scatter(gbar, gobs, np.full_like(gbar, 10**la), model)
        r = minimize_scalar(f, bounds=(math.log10(3e-11), math.log10(3e-10)), method="bounded")
        return 10**r.x, r.fun
    a0u, s_uni_opt = best_uni(gb0, go0, model_dsunruh)
    s_uni_936 = scatter(gb0, go0, np.full_like(gb0, A0_DE), model_dsunruh)
    print(f"    (baseline) universal a0 free-optimal = {a0u:.3e} -> scatter {s_uni_opt:.4f} dex")
    print(f"    (baseline) universal a0 = 9.36e-11               -> scatter {s_uni_936:.4f} dex")

    # the density reading: per-galaxy a0 from the 1 Mpc smoothing
    gbP, goP, a0P = load_pts(per_a0=per)
    s_per = scatter(gbP, goP, a0P, model_dsunruh)
    print(f"    DENSITY a0 (per-galaxy, 1 Mpc smoothed) -> scatter {s_per:.4f} dex   "
          f"<<< the make-or-break number")
    print(f"    inflation vs universal-9.36e-11         : {s_per - s_uni_936:+.4f} dex "
          f"({(s_per/s_uni_936-1)*100:+.1f}%)")
    # McGaugh cross-check
    s_uni_mc = scatter(gb0, go0, np.full_like(gb0, A0_DE), model_mcgaugh)
    s_per_mc = scatter(gbP, goP, a0P, model_mcgaugh)
    print(f"    [McGaugh nu cross-check] universal {s_uni_mc:.4f} -> per-galaxy {s_per_mc:.4f} dex "
          f"({s_per_mc - s_uni_mc:+.4f})")
    print()
    return s_uni_936, s_per, a0_list


# ======================================================================================
#  PART 2 -- CLUSTERS (eRASS1)
# ======================================================================================
# Smooth rho_total over a 1 Mpc ball for each eRASS1 cluster.  The relevant density is the
# mean TOTAL (dynamical) mass within the 1 Mpc smoothing scale at the cluster.  We compute it
# two physically-bracketing ways:
#   (A) MEAN-ENCLOSED within min(R500, 1 Mpc): rho = 3 M(<R)/ (4 pi R^3) using the eRASS1
#       WL-calibrated M500, R500.  This is the cluster's own overdensity averaged over the
#       smoothing scale.
#   (B) FIXED 1 Mpc ball: M(<1 Mpc) estimated by extrapolating M500 with an NFW-like M(<r) ~ r
#       outer slope (M ~ r at large r in deep-MOND/NFW outskirts), then rho = M(<1Mpc)/V_ELL.
# rho_smoothed = rho_DE + rho_matter(cluster, smoothed).  a0_cl = (c/2)sqrt(G rho_smoothed).
# Then recompute eta(R500) = g_obs / g_pred(g_bar, a0_cl).

def part2():
    print("="*92)
    print("PART 2 -- eRASS1 CLUSTERS under the density-a0 smoothed over ell = 1 Mpc")
    print("="*92)
    cl = load_clean()
    N = cl['N']
    z, M500, R500, gobs, gbar = cl['z'], cl['M500'], cl['R500'], cl['gobs'], cl['gbar']
    M500_kg = M500*1e13*Msun
    R500_m  = R500*kpc
    print(f"  eRASS1 clean clusters: {N}")
    print(f"  M500 median {np.median(M500)*1e13:.2e} Msun;  R500 median {np.median(R500):.0f} kpc "
          f"= {np.median(R500_m)/Mpc:.2f} Mpc")

    # ---- baseline eta with universal a0 = 9.36e-11, dS-Unruh nu ----
    def eta_at(a0_arr):
        gpred = np.sqrt(gbar**2 + gbar*a0_arr)
        return gobs/gpred
    eta0 = eta_at(np.full_like(gbar, A0_DE))
    print(f"\n  BASELINE  (universal a0 = 9.36e-11):  eta(R500) median = {np.median(eta0):.3f}")
    print(f"            gbar/a0 median = {np.median(gbar/A0_DE):.4f}  (deep MOND)")

    # ---- reading (A): mean-enclosed total density within min(R500, ell) ----
    # For most clusters R500 < 1 Mpc, so the smoothing ball (1 Mpc) is LARGER than R500.
    # Smoothing the cluster mass over the full 1 Mpc ball DILUTES the overdensity. We bracket:
    #   (A1) rho = mean enclosed within R500 (the cluster's own overdensity, ~500 rho_crit)
    #   (A2) rho = M500 spread over the FULL 1 Mpc ball (dilutes if R500<1Mpc), + cosmic floor
    rho_A1 = 3*M500_kg/(4*np.pi*R500_m**3) + rho_DE
    a0_A1  = a0_formula(rho_A1)
    eta_A1 = eta_at(a0_A1)

    # (A2): mass within 1 Mpc.  If R500 < 1 Mpc, extrapolate M(<1Mpc). In deep-MOND/NFW
    # outskirts M(<r) grows ~ r (isothermal-ish). Use M(<1Mpc) = M500 * (1Mpc/R500) when
    # R500<1Mpc, capped; if R500>1Mpc use enclosed at 1 Mpc = M500*(1Mpc/R500)^? -> use M500.
    Mpc1 = 1.0*Mpc
    ratio = Mpc1/R500_m
    # M(<1Mpc): isothermal M~r extrapolation outward (ratio>1), interpolate inward as M~r (ratio<1)
    M_1mpc = np.where(ratio >= 1.0, M500_kg*ratio, M500_kg*ratio)  # M~r both ways (linear)
    rho_A2 = rho_DE + M_1mpc/V_ELL + rho_m_cosmic       # + cosmic floor for the rest of the ball
    a0_A2  = a0_formula(rho_A2)
    eta_A2 = eta_at(a0_A2)

    print(f"\n  READING (A1) -- rho = mean-enclosed total within R500 (cluster's own overdensity):")
    print(f"    rho/rho_DE median = {np.median(rho_A1/rho_DE):.1f}  (=> ~{np.median(M500_kg*3/(4*np.pi*R500_m**3))/rho_crit:.0f} rho_crit)")
    print(f"    a0_cluster median = {np.median(a0_A1):.3e}  = {np.median(a0_A1)/A0_DE:.1f}x cosmic a0")
    print(f"    eta(R500) median  = {np.median(eta_A1):.3f}   "
          f"{'(OVER-CLOSES eta<1)' if np.median(eta_A1)<1 else '(in 1.2-1.5 band!)' if 1.2<=np.median(eta_A1)<=1.5 else ''}")

    print(f"\n  READING (A2) -- rho = total mass within the FULL 1 Mpc ball (the literal ell smoothing):")
    print(f"    rho/rho_DE median = {np.median(rho_A2/rho_DE):.1f}")
    print(f"    a0_cluster median = {np.median(a0_A2):.3e}  = {np.median(a0_A2)/A0_DE:.1f}x cosmic a0")
    print(f"    eta(R500) median  = {np.median(eta_A2):.3f}   "
          f"{'(OVER-CLOSES eta<1)' if np.median(eta_A2)<1 else '(in 1.2-1.5 band!)' if 1.2<=np.median(eta_A2)<=1.5 else ''}")

    # ---- eta band fractions for the literal-ell reading (A2), the framework's actual claim ----
    fr_band = np.mean((eta_A2 >= 1.2) & (eta_A2 <= 1.5))
    fr_over = np.mean(eta_A2 < 1.0)
    print(f"\n    (A2) fraction of clusters with eta in [1.2,1.5]: {fr_band*100:.0f}%;  "
          f"fraction over-closed eta<1: {fr_over*100:.0f}%")
    print()
    return np.median(eta0), np.median(eta_A1), np.median(eta_A2), np.median(a0_A2/A0_DE)


if __name__ == "__main__":
    part0()
    s_uni, s_per, a0gal = part1()
    eta0, etaA1, etaA2, boostA2 = part2()
    print("="*92)
    print("SUMMARY")
    print("="*92)
    print(f"  ell = 1/mu = 1 Mpc (AeST scalar Compton wavelength, CMB-pinned)")
    print(f"  GALAXY RAR scatter: universal 9.36e-11 = {s_uni:.4f} dex  ->  density-a0 (1 Mpc) = {s_per:.4f} dex")
    print(f"  CLUSTER eta(R500):  baseline {eta0:.2f}  ->  (A1 enclosed-R500) {etaA1:.2f}  "
          f"->  (A2 literal 1 Mpc ball) {etaA2:.2f}")
    print(f"  cluster a0 boost (A2 literal ell): {boostA2:.1f}x cosmic")
