#!/usr/bin/env python3
"""
DERIVE ell = r_DE (the dark-energy radius) FROM FIRST PRINCIPLES, then test the
density-law a0 = (c/2) sqrt(G rho_total, smoothed-over-r_DE) on the HARD double
constraint: galaxy SPARC RAR scatter (must stay ~0.13 dex) AND eRASS1 cluster eta
(must land ~1.2-1.5, not over-close <1).

THE CANDIDATE SCALE (framework-native, NOT tuned):
  ell = r_DE = the radius where the structure's mean enclosed matter density drops
  to rho_DE (the dark-energy density). Inside r_DE the structure's matter dominates
  (a0 boosted above 9.36e-11); outside, cosmic rho_DE dominates (a0 -> universal).
  This is the cleanest derived-not-tuned candidate: r_DE is fixed by the density
  profile itself + the ONE density already in the formula (rho_DE), no free knob.

THE PRESCRIPTION TESTED:
  a0(system) = (c/2) sqrt(G * rho_eff),  rho_eff = mean density enclosed within r_DE,
  i.e. rho_eff = rho_DE + <rho_matter>(<r_DE).  Equivalently a0 is set by the matter
  smoothed over the structure's OWN dark-energy radius.

HONESTY (#1 rule): r_DE is DERIVED (the rho=rho_DE crossover). We do NOT tune it to
hit eta~1.2-1.5. If it breaks galaxies (inflates RAR scatter) or needs tuning to help
clusters, we say so -- that closes the density-a0 route. Run both ways.

Run: python density_a0_rDE_crossover.py    (numpy, scipy, astropy)
"""
import glob, math, os
import numpy as np
from scipy.optimize import minimize_scalar

# ---- constants (SI) ----
C   = 2.99792458e8
G   = 6.674e-11
Msun= 1.989e30
kpc = 3.0856775814913673e19
Mpc = 3.0856775814913673e22
pc  = 3.0856775814913673e16
KMS = 1.0e3

H0  = 67.4e3/Mpc
rho_crit = 3*H0**2/(8*math.pi*G)          # 9e-27 kg/m^3
Omega_L  = 0.685
rho_DE   = Omega_L*rho_crit               # 6.4e-27 kg/m^3 dark-energy density
Omega_m  = 0.315

a0   = lambda rho: 0.5*C*np.sqrt(G*rho)    # THE FORMULA
A0_DE   = a0(rho_DE)                        # 9.36e-11 framework value (pure-Lambda)
A0_TOT  = a0(rho_crit)                      # 1.13e-10 rho_total cosmic footing
A0_FRAMEWORK = 9.36e-11

HERE = os.path.dirname(__file__)
SPARC = os.path.join(HERE, "..", "..", "real_research", "data", "sparc_data")

print("="*84)
print("DENSITY-LAW a0 at ell=r_DE (dark-energy crossover radius) -- DERIVED, not tuned")
print("="*84)
print(f"  rho_DE   = {rho_DE:.3e} kg/m^3   -> a0(rho_DE)   = {A0_DE:.3e}  (framework 9.36e-11)")
print(f"  rho_crit = {rho_crit:.3e} kg/m^3 -> a0(rho_crit) = {A0_TOT:.3e}  (rho_total cosmic)")
print(f"  Note a0 ~ sqrt(rho): a structure must be ~{(A0_FRAMEWORK*1.4/A0_DE)**2:.0f}x denser than rho_DE")
print(f"        (smoothed over r_DE) to boost a0 by ~1.4x, ~{(15)**2:.0f}x to boost ~15x.\n")


# ============================================================================
# PART 0: WHAT IS r_DE, and what density does it imply? (the derivation, by hand)
# ============================================================================
# For a structure of mean mass M within radius r, mean enclosed density is
#   rho_bar(<r) = M / (4/3 pi r^3).
# r_DE is defined by rho_bar(<r_DE) = rho_DE.  BUT inside that radius the mean
# enclosed density is BY DEFINITION exactly rho_DE (that's what r_DE means).
# So rho_eff = rho_DE + <rho_matter>(<r_DE).  Two readings of "<rho_matter within r_DE>":
#   (i)  the MEAN enclosed matter density within r_DE = rho_DE (by construction)
#        -> rho_eff = 2 rho_DE -> a0 = sqrt(2)*9.36e-11 = 1.32e-10  UNIVERSAL.
#   (ii) since the structure extends only to ~r_DE where its density = rho_DE, the
#        crossover gives the SAME small boost for ANY structure (galaxy or cluster).
# This is the crucial structural fact we test below.
def rho_bar_enclosed(M, r):
    return M / ((4.0/3.0)*math.pi*r**3)

def r_DE_of_profile(M_of_r, rmax_Mpc=50.0):
    """Radius where mean enclosed matter density = rho_DE, for a callable M_of_r (kg, r in m)."""
    lo, hi = 1e-4*Mpc, rmax_Mpc*Mpc
    # mean enclosed density is monotone decreasing in r for a centrally-concentrated profile
    f = lambda r: rho_bar_enclosed(M_of_r(r), r) - rho_DE
    if f(lo) < 0:   # even tiny r is below rho_DE: structure never crosses (shouldn't happen)
        return None
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        if f(mid) > 0: lo = mid
        else:          hi = mid
    return math.sqrt(lo*hi)


# ============================================================================
# PART 1: GALAXIES -- r_DE for a typical SPARC galaxy + the RAR scatter test
# ============================================================================
def load_sparc(ml_disk=0.70, ml_bulge=0.70):
    """RAR points + per-galaxy total baryonic mass profile info. err<0.1 cut."""
    gals = []
    for path in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
        rows = []
        with open(path) as fh:
            for line in fh:
                s = line.strip()
                if not s or s.startswith("#"): continue
                p = s.split()
                if len(p) < 6: continue
                try: r,vobs,everr,vgas,vdisk,vbul = (float(p[i]) for i in range(6))
                except ValueError: continue
                rows.append((r,vobs,everr,vgas,vdisk,vbul))
        if not rows: continue
        r   = np.array([x[0] for x in rows])
        vobs= np.array([x[1] for x in rows]); everr=np.array([x[2] for x in rows])
        vgas= np.array([x[3] for x in rows]); vdisk=np.array([x[4] for x in rows])
        vbul= np.array([x[5] for x in rows])
        vbar2 = vgas*np.abs(vgas) + ml_disk*vdisk*np.abs(vdisk) + ml_bulge*vbul*np.abs(vbul)
        name = os.path.basename(path).replace("_rotmod.dat","")
        gals.append(dict(name=name,r=r,vobs=vobs,everr=everr,vbar2=vbar2,
                         vgas=vgas,vdisk=vdisk,vbul=vbul))
    return gals

def galaxy_baryonic_mass(g, ml_disk=0.70):
    """Enclosed baryonic mass profile M_bar(<r) from v_bar^2: M = v_bar^2 r / G (point-mass-ish
    spherical proxy; standard for these estimates). Returns the OUTERMOST enclosed M_bar and the
    function M_bar(<r) via the outermost point's circular-velocity mass at each radius."""
    r_m = g['r']*kpc
    vbar2 = np.clip(g['vbar2'], 0, None)*KMS**2   # (m/s)^2
    Mbar_enc = vbar2*r_m/G                          # enclosed dynamical-baryonic mass at each r
    return r_m, Mbar_enc

def galaxy_rDE(g, ml_disk=0.70):
    """r_DE for a galaxy: extrapolate M_bar(<r) ~ const (flat outer) beyond last point,
    find where mean enclosed density = rho_DE. Outer baryonic mass is ~flat -> point mass."""
    r_m, Mbar_enc = galaxy_baryonic_mass(g, ml_disk)
    Mtot = Mbar_enc[-1]                 # total baryonic mass (outermost enclosed)
    if Mtot <= 0: return None, None, None
    # beyond the disk, M(<r) ~ Mtot (point mass): rho_bar(<r) = Mtot/(4/3 pi r^3) = rho_DE
    r_DE = (Mtot/((4.0/3.0)*math.pi*rho_DE))**(1.0/3.0)
    return r_DE, Mtot, r_m[-1]

def galaxy_a0_from_rDE(g, ml_disk=0.70):
    """rho_eff = mean total density (matter+DE) enclosed within r_DE.
    Within r_DE: M_matter(<r_DE) ~ Mtot (point mass, since disk << r_DE), so
    <rho_matter>(<r_DE) = Mtot/(4/3 pi r_DE^3) = rho_DE by construction => rho_eff=2 rho_DE.
    Return a0 for this galaxy under the r_DE prescription."""
    r_DE, Mtot, rlast = galaxy_rDE(g, ml_disk)
    if r_DE is None: return None
    rho_matter_in_rDE = Mtot/((4.0/3.0)*math.pi*r_DE**3)   # == rho_DE by definition of r_DE
    rho_eff = rho_DE + rho_matter_in_rDE
    return a0(rho_eff), r_DE, rho_eff

def rar_logmodel(log_gbar, a0v):
    gbar = 10.0**log_gbar
    x = np.sqrt(gbar/a0v)
    return np.log10(gbar/(1.0-np.exp(-x)))        # McGaugh nu

def rar_logmodel_dsunruh(log_gbar, a0v):
    gbar = 10.0**log_gbar
    return np.log10(np.sqrt(gbar**2 + gbar*a0v))   # framework dS-Unruh nu

def collect_rar(gals, a0_per_galaxy=None, a0_const=None):
    """Build (log gbar, log gobs) with a PER-GALAXY a0 baked into gobs? No: a0 enters the
    MODEL, not the data. We return data points + the a0 to use per point."""
    lgbar, lgobs, a0pt = [], [], []
    for g in gals:
        r_m = g['r']*kpc
        vbar2 = np.clip(g['vbar2'],0,None)
        ok = (g['everr']>0)&(g['everr']/np.maximum(g['vobs'],1e-9)<=0.10)&(g['vobs']>0)&(vbar2>0)&(g['r']>0)
        if a0_per_galaxy is not None:
            a0g = a0_per_galaxy.get(g['name'])
            if a0g is None: continue
        else:
            a0g = a0_const
        for i in np.where(ok)[0]:
            gobs = (g['vobs'][i]*KMS)**2/r_m[i]
            gbar = (vbar2[i]*KMS**2)/r_m[i]
            if gbar<=0 or gobs<=0: continue
            lgbar.append(math.log10(gbar)); lgobs.append(math.log10(gobs)); a0pt.append(a0g)
    return np.array(lgbar), np.array(lgobs), np.array(a0pt)

def dex_scatter_pointwise(lgbar, lgobs, a0pt, model):
    """RMS dex residual with a PER-POINT a0 (each galaxy gets its own r_DE-derived a0)."""
    pred = np.array([model(lb, a)[()] if np.isscalar(a) else model(lb,a) for lb,a in zip(lgbar,a0pt)])
    # model returns scalar for scalar input
    pred = np.array([model(np.array([lb]), a)[0] for lb,a in zip(lgbar,a0pt)])
    return float(np.sqrt(np.mean((lgobs-pred)**2)))

def dex_scatter_const(lgbar, lgobs, a0v, model):
    return float(np.sqrt(np.mean((lgobs-model(lgbar,a0v))**2)))


def part1_galaxies():
    print("="*84); print("PART 1: GALAXIES -- r_DE and the SPARC RAR scatter"); print("="*84)
    gals = load_sparc(ml_disk=0.70, ml_bulge=0.70)
    print(f"  loaded {len(gals)} SPARC galaxies (Upsilon=0.70 framework footing)\n")

    # r_DE for each galaxy + the implied a0
    rows = []
    a0_per = {}
    for g in gals:
        out = galaxy_a0_from_rDE(g)
        if out is None: continue
        a0g, r_DE, rho_eff = out
        a0_per[g['name']] = a0g
        rows.append((g['name'], r_DE/Mpc, a0g, rho_eff/rho_DE))
    rDEs = np.array([x[1] for x in rows]); a0s=np.array([x[2] for x in rows])
    print(f"  r_DE (galaxy dark-energy radius): median={np.median(rDEs)*1000:.0f} kpc "
          f"= {np.median(rDEs):.3f} Mpc  range [{rDEs.min():.3f}, {rDEs.max():.3f}] Mpc")
    print(f"  a0 implied per galaxy (r_DE presc): median={np.median(a0s):.3e}  "
          f"range [{a0s.min():.3e}, {a0s.max():.3e}]")
    print(f"  -> a0/A0_DE: median={np.median(a0s)/A0_DE:.3f}  (sqrt(2)={math.sqrt(2):.3f} expected)")
    print(f"  KEY: every galaxy gets the SAME a0=sqrt(2)*9.36e-11 boost because, by the")
    print(f"       DEFINITION of r_DE, the mean matter density within r_DE is exactly rho_DE.\n")

    # ---- RAR scatter: baseline (const a0) vs r_DE per-galaxy a0 ----
    print("  RAR scatter (unweighted rms dex), framework dS-Unruh nu, Upsilon=0.70:")
    for model, mname in [(rar_logmodel_dsunruh,"dS-Unruh nu"), (rar_logmodel,"McGaugh nu")]:
        lgbar,lgobs,_ = collect_rar(gals, a0_const=A0_FRAMEWORK)
        # baseline: free-optimal const a0
        f = lambda la: dex_scatter_const(lgbar,lgobs,10**la,model)
        res = minimize_scalar(f, bounds=(math.log10(5e-11),math.log10(3e-10)),method="bounded")
        a0opt, sopt = 10**res.x, res.fun
        s_const_fw = dex_scatter_const(lgbar,lgobs,A0_FRAMEWORK,model)
        # r_DE per-galaxy a0
        lgb2,lgo2,a0pt = collect_rar(gals, a0_per_galaxy=a0_per)
        s_rDE = dex_scatter_pointwise(lgb2,lgo2,a0pt,model)
        # const at the r_DE median value (sqrt2 * A0_DE) -- to isolate "did per-galaxy spread hurt?"
        a0med = np.median(a0s)
        s_const_rDEmed = dex_scatter_const(lgbar,lgobs,a0med,model)
        print(f"   [{mname}]")
        print(f"     free-optimal const a0      : {a0opt:.3e}  scatter {sopt:.4f} dex")
        print(f"     const a0=9.36e-11          : scatter {s_const_fw:.4f} dex")
        print(f"     const a0=sqrt2*9.36={a0med:.2e}: scatter {s_const_rDEmed:.4f} dex")
        print(f"     r_DE PER-GALAXY a0          : scatter {s_rDE:.4f} dex  "
              f"(inflation vs const-9.36: {s_rDE-s_const_fw:+.4f} dex)")
        print()
    return a0_per, a0s, rDEs


# ============================================================================
# PART 2: CLUSTERS -- r_DE for clusters + eta(R500) under the r_DE-density a0
# ============================================================================
import sys
sys.path.insert(0, os.path.join(HERE, "..", "..", "real_research", "data"))
import _load_erass1 as L

def nu_simple(y):
    """The banked cluster convention's interpolation (simple nu)."""
    return 0.5 + np.sqrt(0.25 + 1.0/y)

def part2_clusters():
    print("="*84); print("PART 2: CLUSTERS -- r_DE and eRASS1 eta(R500)"); print("="*84)
    d = L.load_clean()
    N = d['N']
    z=d['z']; M500=d['M500']*1e13*Msun; Mgas=d['Mgas']*1e11*Msun
    fstar=0.2
    Mbar=(1+fstar)*Mgas
    R500=d['R500']*kpc
    gobs = G*M500/R500**2
    gbar = G*Mbar/R500**2
    print(f"  {N} clean clusters. median M500={np.median(d['M500'])*1e13:.2e} Msun, "
          f"R500={np.median(d['R500']):.0f} kpc, z={np.median(z):.2f}\n")

    # --- BASELINE eta: framework a0=9.36e-11 (reproduce the banked figure) ---
    # Banked convention (cluster_eta_independent_regrade.py): Def A, simple nu, fstar=0.2:
    #   eta = gobs / (nu_simple(gbar/a0) * gbar).  >1 = deficit (need more mass).
    def eta_for_a0(a0v):
        return gobs/(nu_simple(gbar/a0v)*gbar)
    eta_fw = eta_for_a0(A0_FRAMEWORK)
    print(f"  BASELINE eta(R500), const a0=9.36e-11 : median={np.median(eta_fw):.3f}  "
          f"[{np.percentile(eta_fw,25):.2f},{np.percentile(eta_fw,75):.2f}]   (banked: 2.149)")
    eta_tot = eta_for_a0(A0_TOT)
    print(f"  BASELINE eta(R500), const a0=1.13e-10 : median={np.median(eta_tot):.3f}  (rho_total cosmic, banked 1.974)\n")

    # --- r_DE for each cluster: where mean enclosed matter density = rho_DE ---
    # Cluster total (dynamical) mass profile: use M500 within R500, extrapolate outward.
    # Mean enclosed density at R500 is 500*rho_crit(z). It DROPS as we go out. r_DE is where it
    # hits rho_DE. For an NFW-ish outskirt M(<r)~r (logarithmic) we approximate the OUTER profile.
    # Simplest framework-native estimate: use the SPHERICAL TOP-HAT extrapolation
    #   rho_bar(<r) = rho_bar(<R500)*(R500/r)^s  with the cluster mean profile slope.
    # We bracket with two outer slopes and ALSO the model-independent "isothermal" M~r.
    rhoc_z = 3*(H0*np.sqrt(Omega_m*(1+z)**3+Omega_L))**2/(8*math.pi*G)   # rho_crit(z)
    rho_bar_R500 = 500*rhoc_z                                            # mean density within R500
    # within R500 the total (dyn) mass is M500; the BARYON mean density within R500:
    rho_bar_bar_R500 = Mbar/((4.0/3.0)*math.pi*R500**3)

    print("  r_DE for clusters (radius where MEAN ENCLOSED matter density = rho_DE):")
    print(f"    mean TOTAL density within R500 = 500*rho_crit(z) ~ {np.median(rho_bar_R500)/rho_DE:.0f} rho_DE")
    print(f"    mean BARYON density within R500 ~ {np.median(rho_bar_bar_R500)/rho_DE:.0f} rho_DE\n")

    # Outer mass profile: M(<r) = M500 * (r/R500)^p for r>R500 (p=1 isothermal, p=0.5 steep NFW outskirt).
    # rho_bar(<r) = rho_bar(<R500)*(r/R500)^(p-3). Set = rho_DE:
    #   (r/R500)^(3-p) = rho_bar(<R500)/rho_DE  -> r_DE = R500 * (rho_bar(<R500)/rho_DE)^(1/(3-p))
    for use_density, dlabel in [(rho_bar_R500,"TOTAL (dyn) mass profile"),
                                 (rho_bar_bar_R500,"BARYON-only mass profile")]:
        for p in [1.0]:   # isothermal outskirt (standard cluster outer slope ~ -2 in rho -> M~r)
            r_DE = R500*(use_density/rho_DE)**(1.0/(3.0-p))
            # rho_eff = mean MATTER density enclosed within r_DE = rho_DE (by construction) + rho_DE bg
            # => same sqrt(2) universal boost!  Verify, and also compute the in-R500-boosted reading.
            rho_eff_meandef = 2*rho_DE*np.ones_like(z)
            a0_meandef = a0(rho_eff_meandef)
            eta_meandef = eta_for_a0(a0_meandef)
            print(f"  [{dlabel}, isothermal p=1] r_DE: median={np.median(r_DE)/Mpc:.2f} Mpc "
                  f"[{np.percentile(r_DE,25)/Mpc:.2f},{np.percentile(r_DE,75)/Mpc:.2f}]")
            print(f"     rho_eff=<rho_matter within r_DE>+rho_DE = 2 rho_DE (BY r_DE DEFINITION)")
            print(f"     -> a0 = sqrt(2)*9.36e-11 = {np.median(a0_meandef):.3e} (UNIVERSAL, same as galaxies)")
            print(f"     -> eta(R500) median = {np.median(eta_meandef):.3f}  "
                  f"[{np.percentile(eta_meandef,25):.2f},{np.percentile(eta_meandef,75):.2f}]\n")

    # --- ALTERNATIVE READING: a0 set by the in-R500 mean density (NOT smoothed to r_DE) ---
    # This is the "smooth over the structure's dense interior" reading the deep-dive floated.
    print("  ALTERNATIVE (NOT the r_DE prescription, for contrast): a0 from MEAN density within")
    print("  R500 itself (the dense interior), capped/smoothed:")
    a0_R500tot = a0(rho_bar_R500)            # uses 500 rho_crit -> huge boost
    eta_R500tot = eta_for_a0(a0_R500tot)
    print(f"    a0(500 rho_crit) median = {np.median(a0_R500tot):.3e} "
          f"(~{np.median(a0_R500tot)/A0_DE:.0f}x) -> eta median = {np.median(eta_R500tot):.3f} (OVER-CLOSES)")
    a0_R500bar = a0(rho_bar_bar_R500)
    eta_R500bar = eta_for_a0(a0_R500bar)
    print(f"    a0(mean baryon dens <R500) median = {np.median(a0_R500bar):.3e} "
          f"(~{np.median(a0_R500bar)/A0_DE:.1f}x) -> eta median = {np.median(eta_R500bar):.3f}")
    # what boost is NEEDED to reach eta~1.2-1.5? Solve median eta_for_a0(a0)=target numerically.
    print()
    from scipy.optimize import brentq
    for target in [1.5,1.3,1.2]:
        g = lambda a0v: np.median(eta_for_a0(a0v)) - target
        a0_need = brentq(g, 1e-11, 1e-7)
        print(f"    to hit median eta={target}: need a0 ~ {a0_need:.3e} = {a0_need/A0_DE:.1f}x a0_DE "
              f"=> rho_eff ~ {(a0_need/A0_DE)**2:.0f} rho_DE")
    return eta_fw, eta_meandef


if __name__ == "__main__":
    a0_per, a0s, rDEs = part1_galaxies()
    eta_fw, eta_rDE = part2_clusters()
    print("="*84); print("GRADE"); print("="*84)
    print(f"  galaxy r_DE-a0: median {np.median(a0s):.3e} = sqrt(2)*9.36e-11 (UNIVERSAL across galaxies)")
    print(f"  cluster r_DE-a0: ALSO sqrt(2)*9.36e-11 (SAME, by the r_DE crossover definition)")
    print(f"  cluster eta under r_DE-a0: median {np.median(eta_rDE):.3f}  (baseline 9.36e-11: {np.median(eta_fw):.3f})")
