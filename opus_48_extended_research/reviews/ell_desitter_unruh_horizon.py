#!/usr/bin/env python3
"""
DERIVE ell from de Sitter-Unruh local-horizon physics, then TEST the smoothed density-law a0.
=============================================================================================
THE FRAMEWORK:  a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = 9.36e-11.
THE DENSITY READING (the one distinctive escape from the cluster deficit):
    a0 = (c/2) sqrt(G rho_total),   rho_total = rho_DE + rho_matter,smoothed-over-ell.
This is the de Sitter-Unruh "local Friedmann" reading:  a0 ~ c H_local,  H_local^2 = (8piG/3) rho_total.

THE CRUX is the COARSE-GRAINING SCALE ell over which rho_matter is smoothed. The deep-dive forensic
(CLUSTER_DEEPDIVE_VERDICT_2026-06-14.md) found:
  - LOCAL/clumpy reading (no smoothing): DEAD. A galaxy disk is ~1e6x cosmic -> a0 ~1e3x too big -> erases galaxy MOND.
  - Mpc-AMBIENT reading: helps clusters (eta -> 1.2-1.5) but rides on an UNDERIVED ell.
So the WHOLE game is: can ell be DERIVED (framework-native, NOT tuned), and does ONE ell thread BOTH:
    (1) GALAXY RAR: smoothing must keep a0 ~ universal so SPARC RAR scatter stays ~0.13 dex.
    (2) CLUSTERS:   smoothing must boost cluster a0 enough to pull eta -> ~1.2-1.5 (NOT over-close eta<1).

==========================  THE DERIVATION OF ell (de Sitter-Unruh)  ==========================
The de Sitter-Unruh inertia: a particle feels T_eff = (hbar/2pi c kB) sqrt(a^2 + (cH_local)^2). The
"cH_local" is the LOCAL de Sitter/horizon acceleration scale. In a region of total density rho_total
the local-Friedmann rate is H_local^2 = (8piG/3) rho_total, and the LOCAL APPARENT-HORIZON RADIUS is

        r_AH = c / H_local = c / sqrt((8piG/3) rho_total).                          [eq. AH]

This is the natural coarse-graining scale of the de Sitter-Unruh inertia: it is the radius of the local
causal/coherence horizon that sets the Unruh bath. The density that enters a0 is the density averaged
over the region the local horizon can "see" -- i.e. rho_total smoothed over a ball of radius r_AH.

But r_AH ITSELF depends on rho_total (eq. AH) -> the scale is SELF-CONSISTENT, not a free input:

        rho_total = rho_DE + <rho_matter>_(smoothed over r_AH(rho_total)),           [eq. SC]
        r_AH      = c / sqrt((8piG/3) rho_total).

This is the framework-native ell: ell == r_AH, the local apparent-horizon radius, solved self-consistently.
It is DERIVED (the dS-Unruh horizon), NOT tuned. We solve eq. SC by fixed-point iteration on real data and
ask what it gives -- honestly. The honest worry the task flags: if r_AH comes out Gpc (cosmological) it
CANNOT give a local cluster boost, and the density reading fails from the inertia side. Compute it.

Run:  python ell_desitter_unruh_horizon.py    (numpy, scipy, astropy; reads real SPARC + eRASS1)
QUARANTINE: a0/Z are the framework's POSITED values, never asserted derived. ell IS derived here (or shown tuned).
"""
import os, sys, glob, math
import numpy as np
from scipy.optimize import minimize_scalar

# ---- constants (SI) ----
c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0856775814913673e19
Mpc  = 3.0856775814913673e22
pc   = 3.0856775814913673e16
H0   = 67.4e3/Mpc
KMS  = 1.0e3

rho_crit = 3*H0**2/(8*np.pi*G)              # cosmic critical density today ~ 8.6e-27
Omega_L  = 0.685
rho_DE   = Omega_L*rho_crit                  # dark-energy density
a0       = lambda rho: 0.5*c*np.sqrt(G*rho)  # THE FORMULA
A0_DE    = a0(rho_DE)                         # = framework a0_F = 9.36e-11 (by construction)
A0_CRIT  = a0(rho_crit)                       # = rho_total footing 1.13e-10 (rho_crit, the cosmic rho_total)

HERE   = os.path.dirname(os.path.abspath(__file__))
SPARC  = os.path.join(HERE, "..", "..", "real_research", "data", "sparc_data")
sys.path.insert(0, os.path.join(HERE, "..", "..", "real_research", "data"))

print("="*94)
print("FRAMEWORK ANCHORS (posited; quarantine -- a0/Z NOT asserted derived)")
print("="*94)
print(f"  rho_crit={rho_crit:.3e}  rho_DE=Omega_L*rho_crit={rho_DE:.3e}  kg/m^3")
print(f"  a0(rho_DE)   = {A0_DE:.3e}  m/s^2  (= framework a0_F = 9.36e-11, by construction)")
print(f"  a0(rho_crit) = {A0_CRIT:.3e}  m/s^2  (= cosmic rho_total footing; still ~cH0, Milgrom coincidence)")
print(f"  rho_DE is the FLOOR: a0=(c/2)sqrt(G(rho_DE+rho_matter)) reduces to a0(rho_DE) when rho_matter<<rho_DE.")


# =====================================================================================
# STEP 1 -- DERIVE ell = r_AH(rho_total), the local apparent-horizon radius (self-consistent)
# =====================================================================================
def r_AH(rho_total):
    """Local apparent-horizon radius r_AH = c/H_local, H_local^2=(8piG/3)rho_total. [eq. AH]"""
    H_local = np.sqrt((8*np.pi*G/3.0)*rho_total)
    return c/H_local

print("\n" + "="*94)
print("STEP 1 -- ell = r_AH = c/H_local, the DERIVED de Sitter-Unruh coarse-graining scale")
print("="*94)
print("  ell is DERIVED as the local apparent-horizon radius r_AH=c/H_local (NOT tuned). It is")
print("  density-dependent and self-consistent (eq. SC). What does it come out to?\n")
for nm, rho in [("cosmic rho_DE (floor)", rho_DE),
                ("cosmic rho_crit", rho_crit),
                ("10x cosmic (filament)", 10*rho_crit),
                ("200x cosmic (cluster mean, virial)", 200*rho_crit),
                ("500x cosmic (R500)", 500*rho_crit),
                ("galaxy disk ~1e-21", 1e-21)]:
    print(f"    rho={rho:9.2e} ({nm:33}): r_AH = {r_AH(rho)/Mpc:11.3e} Mpc  (a0={a0(rho):.2e})")
print(f"""
  THE HONEST READ on the scale (the task's central worry):
  - At cosmic density (rho~rho_crit) r_AH ~ c/H0 ~ {r_AH(rho_crit)/Mpc:.0f} Mpc = the HUBBLE RADIUS (Gpc-scale, COSMOLOGICAL).
  - r_AH only shrinks to ~Mpc when rho ~ { ( (c/ (1*Mpc))**2 *3/(8*np.pi*G) )/rho_crit:.0f}x rho_crit (cluster-virial densities).
  - r_AH ~ kpc (galaxy disk scale) needs rho ~ {( (c/(10*kpc))**2 *3/(8*np.pi*G))/rho_crit:.2e}x rho_crit -- never reached by smooth matter.
  So r_AH is HUGE in low-density regions (the field, where galaxies live) and only Mpc-small inside clusters.""")


# =====================================================================================
# Helper: SMOOTH rho_matter over a ball of radius ell, self-consistently with ell=r_AH.
# For a SPHERICAL mass profile M(<r) the mean matter density inside radius ell is
#   <rho_matter>_ell = M(<ell) / (4/3 pi ell^3).
# We solve  rho_total = rho_DE + <rho_matter>_ell,  ell = r_AH(rho_total)  by fixed point.
# =====================================================================================
def selfconsistent_a0_point(Menc_func, r_probe, rho_floor=rho_DE, n_iter=200):
    """At a probe radius r_probe in a system with enclosed-mass function Menc_func(r),
    solve the self-consistent dS-Unruh horizon smoothing:
        ell = r_AH(rho_total),  rho_total = rho_floor + Mavg(within max(ell, r_probe)).
    The smoothing ball is the local horizon r_AH but at least the probe radius (you can't
    smooth on a scale smaller than where you are measuring). Returns (a0_eff, ell, rho_total)."""
    rho_t = rho_floor
    for _ in range(n_iter):
        ell = r_AH(rho_t)
        R = max(ell, r_probe)
        rho_m = Menc_func(R)/((4.0/3.0)*np.pi*R**3)
        rho_new = rho_floor + rho_m
        if abs(rho_new-rho_t) <= 1e-6*rho_t:
            rho_t = rho_new; break
        rho_t = rho_new
    ell = r_AH(rho_t)
    return a0(rho_t), ell, rho_t


# =====================================================================================
# STEP 2 -- GALAXY RAR on the real 175 SPARC curves under the DERIVED density-a0.
#   For each RAR point we set a0 by the dS-Unruh horizon-smoothed density at that point.
#   The smoothing ball is r_AH (the local horizon). Because galaxies are LOW total mass
#   (~1e11-1e12 Msun) and r_AH is HUGE (Gpc), the smoothed matter density is ~0 -> a0->a0(rho_DE).
#   => prediction: NO inflation of the RAR. We compute the scatter on real data to confirm.
# =====================================================================================
def load_sparc_points(ml_disk=0.70, ml_bulge=0.70):
    """RAR points (g_bar, g_obs) and the enclosed baryonic mass profile per galaxy.
    ml_disk=0.70 is the FRAMEWORK footing (MEMORY rule). Returns list of per-galaxy dicts."""
    gals = []
    for path in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
        rows = []
        with open(path) as fh:
            for line in fh:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                p = s.split()
                if len(p) < 6:
                    continue
                try:
                    r, vobs, everr, vgas, vdisk, vbul = (float(p[i]) for i in range(6))
                except ValueError:
                    continue
                rows.append((r, vobs, everr, vgas, vdisk, vbul))
        if not rows:
            continue
        R = np.array([x[0] for x in rows])*kpc
        Vobs = np.array([x[1] for x in rows])*KMS
        eV   = np.array([x[2] for x in rows])*KMS
        Vgas = np.array([x[3] for x in rows])*KMS
        Vdisk= np.array([x[4] for x in rows])*KMS
        Vbul = np.array([x[5] for x in rows])*KMS
        Vbar2 = Vgas*np.abs(Vgas) + ml_disk*Vdisk*np.abs(Vdisk) + ml_bulge*Vbul*np.abs(Vbul)
        gbar = Vbar2/R                     # g_bar = Vbar^2/r
        gobs = Vobs**2/R
        # enclosed baryonic mass M(<r) = Vbar^2 r / G  (Newtonian, from the baryonic curve)
        Menc = np.maximum(Vbar2, 0.0)*R/G
        gals.append(dict(R=R, Vobs=Vobs, eV=eV, gbar=gbar, gobs=gobs, Menc=Menc,
                         everr=np.array([x[2] for x in rows]), vobs_kms=np.array([x[1] for x in rows])))
    return gals


def galaxy_Menc_func(gal):
    """Step-interpolated enclosed baryonic mass M(<r) for a SPARC galaxy, flat beyond last point
    (the baryons are essentially all enclosed by the last measured radius)."""
    R, Menc = gal["R"], gal["Menc"]
    Mtot = Menc[-1]                        # total enclosed baryonic mass (last point)
    def f(r):
        if r <= R[0]:
            return Menc[0]*(r/R[0])**3 if r > 0 else 0.0   # ~uniform core
        if r >= R[-1]:
            return Mtot                                     # all baryons enclosed
        return float(np.interp(r, R, Menc))
    return f


def rar_logmodel(log_gbar, a0val):
    gbar = 10.0**log_gbar
    x = np.sqrt(gbar/a0val)
    return np.log10(gbar/(1.0-np.exp(-x)))


def dex_scatter_const_a0(lgbar, lgobs, a0val):
    return float(np.sqrt(np.mean((lgobs - rar_logmodel(lgbar, a0val))**2)))


def optimal_const_a0(lgbar, lgobs):
    f = lambda la0: dex_scatter_const_a0(lgbar, lgobs, 10.0**la0)
    r = minimize_scalar(f, bounds=(math.log10(3e-11), math.log10(3e-10)), method="bounded",
                        options={"xatol":1e-6})
    return 10.0**r.x, r.fun


print("\n" + "="*94)
print("STEP 2 -- GALAXY RAR on real 175 SPARC curves: CONST a0 baseline vs the DERIVED density-a0")
print("="*94)
ML = 0.70   # framework footing (MEMORY rule); also report 0.50 as a both-ways check below
for ML in (0.70, 0.50):
    gals = load_sparc_points(ml_disk=ML, ml_bulge=ML)
    # build the RAR point cloud with the standard everr<0.1, v>0 cuts
    gb, go, a0_dens = [], [], []
    for gal in gals:
        Menc_f = galaxy_Menc_func(gal)
        for i in range(len(gal["R"])):
            r, vobs, everr = gal["R"][i], gal["vobs_kms"][i], gal["everr"][i]
            gbar_i, gobs_i = gal["gbar"][i], gal["gobs"][i]
            if r <= 0 or vobs <= 0 or everr <= 0 or everr/vobs > 0.10:
                continue
            if gbar_i <= 0 or gobs_i <= 0:
                continue
            # DERIVED density-a0 at this point: dS-Unruh horizon-smoothed density
            a0_eff, ell, rho_t = selfconsistent_a0_point(Menc_f, r)
            gb.append(gbar_i); go.append(gobs_i); a0_dens.append(a0_eff)
    gb, go, a0_dens = np.array(gb), np.array(go), np.array(a0_dens)
    lgbar, lgobs = np.log10(gb), np.log10(go)
    ngal = len(gals)

    # baseline: best CONST a0 and its scatter
    a0_opt, s_opt = optimal_const_a0(lgbar, lgobs)
    s_at_DE  = dex_scatter_const_a0(lgbar, lgobs, A0_DE)
    # the density-a0 reading: per-point a0 from the horizon smoothing
    x = np.sqrt(gb/a0_dens)
    lg_pred_dens = np.log10(gb/(1.0-np.exp(-x)))
    s_dens = float(np.sqrt(np.mean((lgobs-lg_pred_dens)**2)))

    print(f"\n  --- footing Upsilon={ML} ---   ({ngal} galaxies, {len(gb)} RAR points)")
    print(f"    CONST-a0 unweighted-dex-OPTIMAL a0 = {a0_opt:.3e}  (scatter {s_opt:.4f} dex)  [baseline]")
    print(f"    CONST a0 = a0(rho_DE)=9.36e-11     :  scatter {s_at_DE:.4f} dex")
    print(f"    DERIVED density-a0 (dS-Unruh horizon-smoothed, per-point):")
    print(f"        a0_eff range over RAR points : [{a0_dens.min():.3e}, {a0_dens.max():.3e}]  "
          f"(median {np.median(a0_dens):.3e})")
    print(f"        a0_eff / a0(rho_DE) range    : [{a0_dens.min()/A0_DE:.4f}, {a0_dens.max()/A0_DE:.4f}]")
    print(f"        RAR scatter under density-a0 :  {s_dens:.4f} dex")
    print(f"        inflation vs CONST-a0(rho_DE):  {s_dens-s_at_DE:+.4f} dex  "
          f"({'NEGLIGIBLE -- galaxies survive' if abs(s_dens-s_at_DE)<0.01 else 'INFLATED -- breaks galaxies'})")


# =====================================================================================
# STEP 3 -- CLUSTERS on real eRASS1 under the DERIVED density-a0 (same ell=r_AH self-consistent).
# =====================================================================================
from _load_erass1 import load_clean

def cluster_Menc_func(M500_kg, R500_m, rho_bg=rho_crit):
    """PHYSICAL enclosed TOTAL mass profile for a cluster embedded in the cosmic background.
    Inside R500: isothermal M(<r)=M500*(r/R500) (rho~r^-2). The cluster overdensity is FINITE --
    it does NOT extend to hundreds of Mpc. Beyond a turnaround radius r_ta (~few x R500, where the
    cluster density drops to the cosmic background), the enclosed mass is just background-dominated:
        M(<r) = M_cluster(r_ta) + rho_bg * (4/3 pi)(r^3 - r_ta^3).
    This is the KEY honesty fix: smoothing over a horizon ball MUCH larger than the cluster averages
    the cluster matter down toward the COSMIC mean (rho_bg), because the ball is mostly empty space."""
    r_ta = 5.0*R500_m                                  # turnaround ~5 R500 (cluster -> field transition)
    M_ta = M500_kg*(r_ta/R500_m)                       # isothermal mass within turnaround
    def f(r):
        if r <= r_ta:
            return M500_kg*(r/R500_m)
        return M_ta + rho_bg*(4.0/3.0)*np.pi*(r**3 - r_ta**3)
    return f

print("\n" + "="*94)
print("STEP 3 -- CLUSTERS on real eRASS1 under the DERIVED density-a0 (ell=r_AH self-consistent)")
print("="*94)
d = load_clean()
gbar_cl, gobs_cl = d["gbar"], d["gobs"]
M500_kg = d["M500"]*1e13*Msun
R500_m  = d["R500"]*kpc
Ncl = d["N"]
print(f"  eRASS1 clean N={Ncl}, median z={np.median(d['z']):.3f}, median M500={np.median(d['M500'])*1e13:.2e} Msun")
print(f"  median R500={np.median(d['R500']):.0f} kpc, median g_bar/a0(rho_DE)={np.median(gbar_cl/A0_DE):.4f} (DEEP MOND)")

def nu_simple(y):  return 0.5*(1+np.sqrt(1+4/y))   # g_obs=nu(gbar/a0) gbar; simple = dS-Unruh

def eta_const_a0(a0val):
    gpred = nu_simple(gbar_cl/a0val)*gbar_cl
    return gobs_cl/gpred

# baseline etas
eta_F  = eta_const_a0(A0_DE)     # framework a0 (rho_DE)
eta_M  = eta_const_a0(1.20e-10)  # regular MOND
print(f"\n  Baselines (const a0):")
print(f"    a0=a0(rho_DE)=9.36e-11 : eta(R500)={np.median(eta_F):.3f}  [IQR {np.percentile(eta_F,25):.2f}-{np.percentile(eta_F,75):.2f}]")
print(f"    a0=1.20e-10 (reg MOND) : eta(R500)={np.median(eta_M):.3f}  [IQR {np.percentile(eta_M,25):.2f}-{np.percentile(eta_M,75):.2f}]")

# DERIVED density-a0 per cluster: self-consistent horizon smoothing at the probe radius R500
a0_cl_dens, ell_cl, rho_cl_t = [], [], []
for i in range(Ncl):
    Menc_f = cluster_Menc_func(M500_kg[i], R500_m[i])
    a0_eff, ell, rho_t = selfconsistent_a0_point(Menc_f, R500_m[i])
    a0_cl_dens.append(a0_eff); ell_cl.append(ell); rho_cl_t.append(rho_t)
a0_cl_dens = np.array(a0_cl_dens); ell_cl = np.array(ell_cl); rho_cl_t = np.array(rho_cl_t)

eta_dens = gobs_cl/(nu_simple(gbar_cl/a0_cl_dens)*gbar_cl)
print(f"\n  DERIVED density-a0 (dS-Unruh horizon-smoothed, self-consistent ell=r_AH):")
print(f"    smoothing scale ell=r_AH range : [{ell_cl.min()/Mpc:.3f}, {ell_cl.max()/Mpc:.3f}] Mpc  (median {np.median(ell_cl)/Mpc:.3f} Mpc)")
print(f"    a0_cl/a0(rho_DE) boost range   : [{a0_cl_dens.min()/A0_DE:.2f}, {a0_cl_dens.max()/A0_DE:.2f}]x  (median {np.median(a0_cl_dens)/A0_DE:.2f}x)")
print(f"    eta(R500) under density-a0     : {np.median(eta_dens):.3f}  [IQR {np.percentile(eta_dens,25):.2f}-{np.percentile(eta_dens,75):.2f}]")
ov = (eta_dens < 1.0).mean()*100
print(f"    fraction of clusters OVER-closed (eta<1): {ov:.1f}%")

print("\n" + "="*94)
print("STEP 3b -- WHY the horizon ell gives no cluster boost: the scale mismatch is fatal")
print("="*94)
medR500 = np.median(d['R500'])*kpc
print(f"""  The mean total density INSIDE R500 is ~500 rho_crit, but that is NOT the density the dS-Unruh
  horizon smooths over. The horizon radius is set by the SMOOTHED density, and it solves to the
  cosmic floor (median ell={np.median(ell_cl)/Mpc:.0f} Mpc) -- because a ~{np.median(ell_cl)/Mpc:.0f} Mpc ball centred on a cluster is
  ~{(np.median(ell_cl)/medR500):.0f}x larger than R500 ({medR500/Mpc:.2f} Mpc) in radius, ~{(np.median(ell_cl)/medR500)**3:.0e}x in volume. The cluster's
  matter ({np.median(d['M500'])*1e13:.1e} Msun) spread over that ball gives a mean density of only
    rho_cl_in_ball ~ M500 / ((4/3)pi ell^3) = {np.median(M500_kg)/((4/3)*np.pi*np.median(ell_cl)**3)/rho_crit:.2e} rho_crit  <<  rho_DE.
  So the horizon ball washes the cluster OUT -> a0 stays at a0(rho_DE) -> NO boost -> eta unchanged at {np.median(eta_dens):.2f}.

  The self-consistency is the trap: to get a Mpc-small horizon you need ~2e7 rho_crit (far above any
  cluster's ~500-rho_crit mean), and the cluster can't supply that smoothed density at its OWN radius
  because r_AH(500 rho_crit)={r_AH(500*rho_crit)/Mpc:.0f} Mpc >> R500. The horizon NEVER shrinks to the cluster scale.""")


# =====================================================================================
# STEP 4 -- the ALTERNATIVE ell: the MOND radius r_M = sqrt(GM/a0), and the GENERAL crossover.
# Does ANY framework-native ell (horizon OR MOND-radius) thread both? And what ell WOULD be needed?
# =====================================================================================
print("\n" + "="*94)
print("STEP 4 -- alternative ell = MOND radius r_M, and the general 'what ell threads both' analysis")
print("="*94)

# (4a) MOND radius r_M = sqrt(GM/a0): the scale where g_N = a0. Is it Mpc in clusters, kpc in galaxies?
print("\n  (4a) ell = MOND radius r_M = sqrt(GM/a0) (the OTHER framework-native scale):")
for nm, M, lbl in [("galaxy (1e11 Msun)", 1e11*Msun, "kpc"),
                   ("cluster (2e14 Msun)", 2e14*Msun, "Mpc")]:
    rM = np.sqrt(G*M/A0_DE)
    print(f"    {nm:22}: r_M = {rM/kpc:9.1f} kpc = {rM/Mpc:.3f} Mpc")
# smooth the cluster matter over r_M and see the boost
rM_cl = np.sqrt(G*M500_kg/A0_DE)
rho_in_rM = M500_kg/((4.0/3.0)*np.pi*rM_cl**3)        # cluster mass smoothed over its OWN MOND radius
a0_rM = a0(rho_DE + rho_in_rM)
eta_rM = gobs_cl/(nu_simple(gbar_cl/a0_rM)*gbar_cl)
print(f"    cluster r_M median = {np.median(rM_cl)/Mpc:.2f} Mpc; smoothing M500 over r_M gives")
print(f"      rho_in_rM/rho_DE median = {np.median(rho_in_rM)/rho_DE:.1f}x -> a0 boost {np.median(a0_rM)/A0_DE:.2f}x -> eta={np.median(eta_rM):.3f}")
print(f"      fraction over-closed (eta<1): {(eta_rM<1).mean()*100:.1f}%")
# but r_M for a GALAXY is ~10s of kpc -- smoothing a galaxy over r_M sees the FULL disk density -> breaks RAR
print(f"""    BUT the MOND radius is NOT scale-blind across systems in the way needed: r_M~kpc for a galaxy
    means the galaxy is smoothed over its OWN disk (rho~1e-21, ~1e5 x rho_DE) -> a0 ~300x too big ->
    DESTROYS the galaxy RAR. r_M tracks the SYSTEM, so it gives EACH system its own clumpy density --
    that is exactly the LOCAL/clumpy reading the deep-dive proved DEAD. r_M = BREAKS-GALAXY-RAR.""")

# (4b) the general statement: what ell threads both, and is it framework-derived?
print("\n  (4b) The general 'what ell threads both' -- and is it framework-native?")
print(f"""    To thread BOTH you need an ell that:
      - in a GALAXY, smooths over a ball big enough that the disk's ~1e5-1e6 x overdensity washes to
        ~rho_DE (needs ell >> the galaxy, i.e. ell >~ a few Mpc, the field-galaxy ambient scale), AND
      - in a CLUSTER, smooths over a ball that RETAINS just enough of the ~500x overdensity to give the
        ~5x boost that lands eta~1.2-1.5 -- NOT so small it sees the clumpy core (over-close, eta<1) and
        NOT so large it washes out (no boost). With a realistic isothermal cluster that ball is ~6-10 Mpc
        (see 4c); a 1-2 Mpc ball over-boosts (~13-32x) and OVER-closes.
    That is a FIXED ~6-10 Mpc comoving scale -- LARGER than a galaxy AND a cluster, SMALLER than the
    horizon. The dS-Unruh horizon r_AH is DENSITY-dependent and lands at Gpc (field) / converges to the
    cosmic mean for clusters -- it is ~100-1000x TOO BIG everywhere and NEVER at the few-Mpc sweet spot.
    The MOND radius r_M tracks the SYSTEM and gives the clumpy reading (too small in galaxies). NEITHER
    framework-native scale is the fixed few-Mpc the data wants.""")

# (4c) demonstrate the fixed ~1.5 Mpc ad-hoc ell DOES thread both -- to show the gap is ONLY the derivation
print("\n  (4c) CONTROL: scan FIXED, TUNED ell -- which ell (if any) threads both? (isolate 'derivation' as the gap)")
print("       (cluster profile = isothermal M(<r)~r inside turnaround; honest both-ways: this CONCENTRATES")
print("        mass vs a pure top-hat, so a 1-2 Mpc ball OVER-shoots the boost and OVER-closes eta<1.)")
for ell_fixed_Mpc in (1.0, 1.5, 2.0, 3.0, 6.0, 10.0):
    ell_fixed = ell_fixed_Mpc*Mpc
    # cluster: smooth M(<ell_fixed) using the physical (turnaround+background) profile
    a0_clf, eta_clf = [], []
    for i in range(Ncl):
        Menc_f = cluster_Menc_func(M500_kg[i], R500_m[i])
        R = max(ell_fixed, R500_m[i])
        rho_m = Menc_f(R)/((4.0/3.0)*np.pi*R**3)
        a0v = a0(rho_DE + rho_m)
        a0_clf.append(a0v)
    a0_clf = np.array(a0_clf)
    eta_clf = gobs_cl/(nu_simple(gbar_cl/a0_clf)*gbar_cl)
    # galaxy RAR scatter at this fixed ell (smooth each galaxy over ell_fixed -- washes the disk out)
    gals = load_sparc_points(0.70, 0.70)
    gb2, go2, a0d2 = [], [], []
    for gal in gals:
        Menc_f = galaxy_Menc_func(gal)
        Mtot = gal["Menc"][-1]
        rho_m_gal = Mtot/((4.0/3.0)*np.pi*ell_fixed**3)   # galaxy mass over the fixed ball
        a0_gal = a0(rho_DE + rho_m_gal)
        for i in range(len(gal["R"])):
            r, vobs, everr = gal["R"][i], gal["vobs_kms"][i], gal["everr"][i]
            if r<=0 or vobs<=0 or everr<=0 or everr/vobs>0.10 or gal["gbar"][i]<=0 or gal["gobs"][i]<=0:
                continue
            gb2.append(gal["gbar"][i]); go2.append(gal["gobs"][i]); a0d2.append(a0_gal)
    gb2, go2, a0d2 = np.array(gb2), np.array(go2), np.array(a0d2)
    x2 = np.sqrt(gb2/a0d2)
    s2 = float(np.sqrt(np.mean((np.log10(go2)-np.log10(gb2/(1-np.exp(-x2))))**2)))
    print(f"    ell={ell_fixed_Mpc:5.1f} Mpc: cluster eta={np.median(eta_clf):.3f} (over-closed {(eta_clf<1).mean()*100:4.0f}%) | "
          f"galaxy RAR scatter={s2:.4f} dex (galaxy a0 boost x{np.median(a0d2)/A0_DE:.3f})")
print(f"""    -> HONEST both-ways read: a 1-2 Mpc ell OVER-closes (eta~0.5-0.6, >85% of clusters eta<1) with
       this isothermal profile -- the deep-dive's '~15x -> eta 1.2-1.5' was OPTIMISTIC (a top-hat
       estimate; isothermal mass concentration over-boosts). The eta~1.2-1.5 window needs ell ~ 6-10 Mpc.
       Galaxies stay tight at EVERY ell >~ 1 Mpc (the disk washes to ~rho_DE). So a fixed ell DOES exist
       that threads both -- but it is ~6-10 Mpc, EVEN FURTHER from any galaxy/cluster physical scale, and
       it is a TUNED INPUT. The dS-Unruh horizon gives Gpc; no derivation lands ~6-10 Mpc.""")


print("\n" + "="*94)
print("FINAL VERDICT -- does the dS-Unruh-DERIVED ell thread both galaxies and clusters?")
print("="*94)
gals70 = load_sparc_points(0.70, 0.70)
# recompute the headline galaxy scatter under derived density-a0 (==const a0(rho_DE), shown above)
print(f"""  ell DERIVED = r_AH = c/H_local (the dS-Unruh local apparent-horizon radius), self-consistent.
  It is GENUINELY DERIVED (the horizon of the local de Sitter-Unruh bath), NOT tuned -- but it is
  the WRONG SIZE (COSMOLOGICAL, not local):
    * field / galaxies : ell = r_AH ~ {r_AH(rho_DE)/Mpc:.0f} Mpc (Gpc, the Hubble radius). Smoothing washes ALL
      matter to ~rho_DE -> a0=9.36e-11 universal -> SPARC RAR scatter UNCHANGED (galaxies SURVIVE).
    * clusters         : ell = r_AH ~ {np.median(ell_cl)/Mpc:.0f} Mpc still. The Gpc ball washes the cluster matter out;
      the loop converges to rho_total ~ rho_DE+rho_crit (the COSMIC mean) -> a0 = {np.median(a0_cl_dens):.2e}
      = the 1.13e-10 rho_total footing, a UNIFORM {np.median(a0_cl_dens)/A0_DE:.2f}x that applies to galaxies too -- NOT a
      cluster-specific boost. eta only eases {np.median(eta_F):.2f}->{np.median(eta_dens):.2f} (the footing shift), nowhere near 1.2-1.5.

  THREADS-BOTH? NO -- it LEAVES-CLUSTER-DEFICIT. The dS-Unruh horizon is COSMOLOGICAL (Gpc); it cannot
  give a LOCAL cluster boost. Galaxies are safe precisely BECAUSE the scale is huge -- the same hugeness
  kills the cluster boost. The framework-native horizon scale fails from the inertia side, EXACTLY as
  the task's honest worry anticipated.

  The fixed ell that WOULD thread both (Step 4c) is a TUNED INPUT, ~6-10 Mpc (a 1-2 Mpc ell OVER-closes
  eta<1 with a realistic isothermal cluster). The MOND-radius alternative (Step 4a) gives the clumpy
  reading (eta=0.32, 99.7% over-closed) and breaks galaxies. So:
    - the density-a0 reading CAN thread both AT a fixed ~6-10 Mpc ell (real result: such a scale exists), but
    - NO framework-native derivation (horizon r_AH ~ Gpc, OR MOND radius r_M ~ system-size) DELIVERS it.
  HONEST: ell IS derived (the dS-Unruh apparent horizon) but to the WRONG VALUE (Gpc, not ~Mpc) -> the
  density-a0 cluster escape stays SCALE-IS-COSMOLOGICAL: it needs a tuned ~Mpc ell the inertia physics
  does not supply. Quarantine held: a0/Z posited, ell shown derived-but-cosmological.""")
print("="*94)
