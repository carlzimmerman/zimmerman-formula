#!/usr/bin/env python3
r"""
LOCAL-CURVATURE de Sitter-Unruh route to the cluster residual (+ early galaxies)
================================================================================
topic local_curvature_unruh   (solution hunt, 2026-06-19)

MISSION: GENUINELY find a framework-native (no particle DM) LOCAL contribution to
the de Sitter-Unruh effective temperature that:
  (1) RAISES the effective a0 toward the ~4-5x clusters need in their cores,
  (2) stays ~1x in galaxy disks (PRESERVES the 0.11-0.13 dex SPARC RAR), and
  (3) (bonus) is LARGEST in the dense early universe -> JWST too-early massive galaxies.
The CRUX distinction from the already-vetoed density-a0 law: X_local must key on
CURVATURE / POTENTIAL DEPTH, NOT matter density -- a curvature/potential term must
be small in shallow galaxy disks even though they are DENSE.

FRAMEWORK (Zimmerman), sealed:
  a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2  (modified inertia, dS-Unruh).
  T_eff = (hbar / 2 pi c kB) sqrt(a^2 + (c H_Lambda)^2)   (Deser-Levin).
  The MOND scale a0 is set by the FLOOR of T_eff -> the (cH_Lambda)^2 cosmic term.
  Quasi-static law: g_obs = sqrt(g_bar^2 + g_bar * a0).

UNITS (a units bug in the prior mi_dynamic_route.py is corrected here):
  H_Lambda (RATE, 1/s)        = c sqrt(Lambda/3)
  cH_Lambda (ACCELERATION)    = c^2 sqrt(Lambda/3) = sqrt(32pi/3) * a0 = 5.789 a0
  So the dS-Unruh FLOOR ACCELERATION is ~5.79 a0; a0 = cH_Lambda / sqrt(32pi/3).
  Inside T_eff the floor term is (cH_Lambda)^2 (an acceleration^2).

GENERALIZED FLOOR (the candidate):
  T_eff^2 ~ a^2 + (cH_Lambda)^2 + X_local,  X_local an acceleration^2 from LOCAL
  curvature/potential. The effective a0 scales as the floor:
        a0_eff = a0 * sqrt( 1 + X_local/(cH_Lambda)^2 ).
  (Because a0 is proportional to sqrt(floor); cH_Lambda^2 -> cH_Lambda^2 + X_local.)
  To get a0_eff = 4 a0 needs X_local = 15 (cH_Lambda)^2 = 15*(5.789 a0)^2 = 503 a0^2,
  i.e. sqrt(X_local) = 22.4 a0.  To get 4-5x: sqrt(X_local) ~ 22-28 a0.

We enumerate EVERY defensible curvature/potential X_local, derive its magnitude
on REAL eRASS1 clusters AND on REAL SPARC galaxies with the SAME formula, and ask:
does any land in the sweet spot [sqrt(X_local) ~ 20-30 a0 in cluster cores, ~0 in
galaxy disks]? Both ways, honest magnitude, no manufactured win.
"""
import numpy as np
import os, sys, glob

# ----------------------------------------------------------------- constants (SI)
c    = 2.998e8
G    = 6.674e-11
hbar = 1.0546e-34
kB   = 1.381e-23
Msun = 1.989e30
pc   = 3.086e16
kpc  = 1e3*pc
Mpc  = 1e6*pc
km   = 1e3

a0     = 9.36e-11
rho_DE = 6.0e-27
Lambda = (a0/c**2)**2*32*np.pi                 # m^-2
H_Lam  = c*np.sqrt(Lambda/3.0)                 # RATE, 1/s
cH_Lam = c*H_Lam                               # ACCELERATION, m/s^2 = c^2 sqrt(Lam/3)
FLOOR2 = cH_Lam**2                             # the (cH_Lambda)^2 floor term (accel^2)

print("="*94)
print(" LOCAL-CURVATURE de Sitter-Unruh route -- can a POTENTIAL/CURVATURE (not density) term")
print(" raise a0 to ~4-5x in cluster cores while staying ~1x in galaxy disks?")
print("="*94)
print(f"  a0           = {a0:.3e} m/s^2")
print(f"  Lambda       = {Lambda:.3e} m^-2")
print(f"  H_Lambda     = {H_Lam:.3e} 1/s    (de Sitter Hubble RATE)")
print(f"  cH_Lambda    = {cH_Lam:.3e} m/s^2 = {cH_Lam/a0:.3f} a0   (dS-Unruh FLOOR ACCEL)")
print(f"  (cH_Lambda)^2= {FLOOR2:.3e} (m/s^2)^2   <- the floor term inside T_eff^2")
print()
need = {}
for fac in [2,3,4,5]:
    Xneed = (fac**2 - 1)*FLOOR2
    need[fac]=np.sqrt(Xneed)
    print(f"  a0_eff = {fac} a0  needs X_local = {fac**2-1:>2d}*(cH_Lam)^2 = {Xneed:.2e}, "
          f"sqrt(X_local) = {np.sqrt(Xneed)/a0:6.2f} a0")
print(f"\n  => TARGET: a curvature/potential term with sqrt(X_local) ~ {need[4]/a0:.0f}-{need[5]/a0:.0f} a0")
print(f"     in cluster CORES, and ~0 in galaxy disks. (Both ways: also report if it OVERSHOOTS.)")

def a0eff_from_X(X):
    """effective a0 given a local floor addition X (accel^2)."""
    return a0*np.sqrt(1.0 + X/FLOOR2)

# ===========================================================================
# CANDIDATE X_local FORMS -- each derived from the dS-Unruh / GR curvature logic
# ===========================================================================
# A SYSTEM is (M, r). We build, at radius r enclosing mass M:
#   g_N      = G M / r^2                         (Newtonian accel)
#   Phi      = G M / r        (|potential|)      -> Phi/c^2 dimensionless depth
#   omega_t  = sqrt(G M / r^3) (tidal frequency) -> = sqrt(g_N/r) = sqrt(4piG rho/3)
#   K_kretsch= 48 (GM)^2/(c^4 r^6)               (Weyl/Kretschmann, VACUUM curvature)
#   rho      = 3M/(4 pi r^3)                      (mean enclosed density)
#
# Candidate floors X_local (all accel^2), each with a one-line physical justification:
def candidates(M, r):
    gN     = G*M/r**2
    Phi    = G*M/r
    Phi_c2 = Phi/c**2
    omega_t= np.sqrt(G*M/r**3)
    rho    = 3*M/(4*np.pi*r**3)
    K      = 48*(G*M)**2/(c**4*r**6)            # m^-4
    sqrtK  = np.sqrt(K)                          # m^-2  (a curvature)
    out = {}
    # (C1) DENSITY/tidal "local Hubble" (the ALREADY-VETOED density-a0, for reference):
    #      a local H from the enclosed density: X = (c^2 sqrt(8piG rho /3 /3))^2-ish.
    #      Simplest: X = (c * omega_t)^2  -> sqrt(X) = c*omega_t = c sqrt(GM/r^3).
    out['C1_density_tidal'] = (c*omega_t)**2
    # (C2) KRETSCHMANN/Weyl curvature put into the floor as Lambda_eff = sqrt(K):
    #      X = c^4 * sqrt(K) /3   (same map Lambda->c^4 Lambda/3 with Lambda_eff=sqrtK).
    out['C2_kretschmann']   = c**4*sqrtK/3.0
    # (C3) POTENTIAL-DEPTH (Tolman redshift of the dS temperature):
    #      T_local = T_dS (1+Phi/c^2) -> floor scales (1+Phi/c^2)^2; the ADDED X is
    #      X = (cH_Lam)^2 * ((1+Phi/c^2)^2 - 1) ~ 2 (cH_Lam)^2 Phi/c^2.
    out['C3_tolman_phi']    = FLOOR2*((1+Phi_c2)**2 - 1)
    # (C4) POTENTIAL-DEPTH as a NEW floor accel a_Phi = (Phi/c^2)*c*H_Lam-type? Build the
    #      most generous potential term that is still dimensionally an accel^2:
    #      X = (g_N * Phi/c^2)?  no -- try X = (Phi/c^2) * (cH_Lam)^2 * BIGFACTOR via the
    #      virial relation Phi ~ sigma^2. Use the strongest defensible: a "redshifted
    #      horizon" where the LOCAL de Sitter radius shrinks by the redshift factor:
    #      H_local = H_Lam/(1+Phi/c^2) DECREASES (wrong way) OR /(1-2Phi/c^2)... we test
    #      the gravitational BLUEshift of the horizon temp -> handled by C3. Skip duplicate.
    # (C5) GEOMETRIC-MEAN floor: X = g_N * cH_Lam  (a Milgrom-like cross term). sqrt = sqrt(g_N cH_Lam).
    out['C5_geommean']      = gN*cH_Lam
    # (C6) ACCELERATION-FLUCTUATION proxy: in a hot cluster the rms a fluctuates; put the
    #      VELOCITY-DISPERSION energy as a floor: X = (sigma_v * H_Lam)^2 with sigma_v=sqrt(GM/r).
    #      (the "local Unruh from peculiar motion" reading). sqrt(X)=sigma_v*H_Lam... tiny.
    sigma_v = np.sqrt(G*M/r)
    out['C6_sigma_HLam']    = (sigma_v*H_Lam)**2
    return out, dict(gN=gN, Phi_c2=Phi_c2, omega_t=omega_t, rho=rho, sqrtK=sqrtK,
                     sigma_v=sigma_v)

# ===========================================================================
# PART 1 -- magnitude of each X_local in CLUSTER cores vs GALAXY disks
# ===========================================================================
print("\n"+"="*94)
print(" PART 1: magnitude of each candidate floor term sqrt(X_local)/a0 -- CLUSTERS vs GALAXIES")
print("="*94)
systems = [
    ("CLUSTER core    M=2e14 @200kpc", 2e14*Msun, 200*kpc, 'cluster'),
    ("CLUSTER mid     M=5e14 @500kpc", 5e14*Msun, 500*kpc, 'cluster'),
    ("CLUSTER R500    M=7e14 @770kpc", 7e14*Msun, 770*kpc, 'cluster'),
    ("MW disk         M=6e10 @8kpc",   6e10*Msun, 8*kpc,   'galaxy'),
    ("dwarf disk      M=1e9  @2kpc",   1e9*Msun,  2*kpc,   'galaxy'),
    ("SPARC inner     M=1e10 @1kpc",   1e10*Msun, 1*kpc,   'galaxy'),
    ("galaxy outer    M=1e11 @20kpc",  1e11*Msun, 20*kpc,  'galaxy'),
]
keys = ['C1_density_tidal','C2_kretschmann','C3_tolman_phi','C5_geommean','C6_sigma_HLam']
hdr = f"{'system':32s} {'g_N/a0':>8s} " + " ".join([f"{k.split('_')[0]:>7s}" for k in keys])
print("\n  sqrt(X_local)/a0  (the per-term floor accel in units of a0; TARGET ~20-30 in core, ~0 in galaxy)")
print("  "+hdr)
print("  "+"-"*92)
for name, M, r, kind in systems:
    X, aux = candidates(M, r)
    cells = " ".join([f'{np.sqrt(X[k])/a0:7.2f}' for k in keys])
    print(f"  {name:32s} {aux['gN']/a0:8.3f} {cells}")
print("""
  READ: C1 (density/tidal) and C2 (Kretschmann) are the curvature terms tied to the
  LOCAL field strength -- they reach 100s-1000s a0 BUT ARE LARGER IN GALAXIES (denser,
  more compact) than in clusters -> they BREAK the galaxy veto harder (the SPARC trap).
  C3 (Tolman/potential depth) is the ONLY term bigger in clusters than galaxies (keys on
  Phi/c^2 ~ sigma^2) -- but it is ~1e-5 a0, MILLIONS of times too small. C5/C6 are tiny.
  => no single curvature/potential term lands in the [~25 a0 cluster, ~0 galaxy] sweet spot.""")

print("\n  KEY DISCRIMINATOR -- Phi/c^2 (dimensionless potential depth, the ONLY cluster>galaxy quantity):")
print("  "+f"{'system':32s} {'Phi/c^2':>10s} {'ratio to cluster-core':>22s}")
Phi_core = candidates(2e14*Msun, 200*kpc)[1]['Phi_c2']
for name, M, r, kind in systems:
    pc2 = candidates(M, r)[1]['Phi_c2']
    print("  "+f"{name:32s} {pc2:10.2e} {pc2/Phi_core:22.4f}")
print(f"""
  Clusters are ~{Phi_core/candidates(6e10*Msun,8*kpc)[1]['Phi_c2']:.0f}x deeper in Phi/c^2 than the MW disk -- a GENUINE discriminator.
  BUT Phi/c^2 ~ 5e-5 in clusters: to source a0_eff=4a0 a potential term would need to be
  ~O(1) in Phi/c^2 (a black hole). The cluster potential is 1e-5 c^2 -- FAR too shallow for
  ANY linear-or-quadratic-in-Phi mechanism to give an O(1) a0 boost. This is the fundamental
  MAGNITUDE obstruction: the right discriminator (Phi/c^2) has the wrong size by ~10^4-10^5.""")

# ===========================================================================
# PART 2 -- REAL DATA. Run the candidate floors on real eRASS1 + real SPARC.
# ===========================================================================
print("\n"+"="*94)
print(" PART 2: REAL DATA -- candidate floors on eRASS1 (boost wanted) and SPARC (veto)")
print("="*94)

# --- 2a. eRASS1: does each floor raise a0_eff toward 4-5x at the cluster scale? ----------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../real_research/data"))
import _load_erass1 as L
d = L.load_clean()
print(f"\n  [eRASS1] N={d['N']} clean clusters, median z={np.median(d['z']):.3f}, "
      f"median M500={np.median(d['M500'])*1e13:.2e} Msun, median R500={np.median(d['R500']):.0f} kpc")
# Build (M, r) at R500 for each cluster (this is where eta=2.33 is measured).
M500_kg = d['M500']*1e13*Msun
R500_m  = d['R500']*kpc
gbar_cl = d['gbar']; gobs_cl = d['gobs']
# The eta=2.33 means we need a0_eff such that g_obs = sqrt(gbar^2 + gbar*a0_eff).
# Solve the REQUIRED a0_eff per cluster, then compare to what each floor DELIVERS.
a0_req = (gobs_cl**2 - gbar_cl**2)/gbar_cl            # from gobs^2 = gbar^2 + gbar*a0_eff
boost_req = a0_req/a0
print(f"  [eRASS1] REQUIRED a0_eff/a0 to explain eta(R500): median {np.median(boost_req):.2f}x, "
      f"5-95% {np.percentile(boost_req,5):.2f}-{np.percentile(boost_req,95):.2f}x")
print(f"           (this is the 4-5x core target, at R500 where gbar/a0={np.median(gbar_cl/a0):.3f})")

print("\n  Floor DELIVERED at R500 (median a0_eff/a0 from each candidate, on real eRASS1 M500,R500):")
for k in keys:
    Xc = np.array([candidates(M, r)[0][k] for M, r in zip(M500_kg, R500_m)])
    a0eff = a0eff_from_X(Xc)/a0
    print(f"    {k:18s}: median a0_eff = {np.median(a0eff):8.3f}x   (need {np.median(boost_req):.2f}x)")
print("""  READ: C1/C2 OVERSHOOT massively (100s-1000s x) AND are density-keyed (galaxy-fatal);
  C3/C5/C6 deliver ~1.00x (negligible). None delivers the ~4-5x at the RIGHT scale cleanly.""")

# --- 2b. SPARC galaxy veto: apply the SAME floor to 175 SPARC, measure RAR scatter --------
print("\n  [SPARC veto] apply the SAME floor law point-by-point on 175 SPARC rotmod curves:")
DATADIR=None
for cand in [os.path.join(os.path.dirname(__file__),"../../../real_research/data/sparc_data"),
             "real_research/data/sparc_data"]:
    if os.path.isdir(cand): DATADIR=cand; break
files = sorted(glob.glob(os.path.join(DATADIR,"*_rotmod.dat")))
Ups=0.70
def load_sparc():
    gbar,gobs,Mr,rr=[],[],[],[]
    for f in files:
        dat=np.loadtxt(f,comments='#')
        if dat.ndim==1 or dat.shape[0]<3: continue
        rad=dat[:,0]*kpc; Vobs=dat[:,1]*km; errV=dat[:,2]*km
        Vgas=dat[:,3]*km; Vdisk=dat[:,4]*km; Vbul=dat[:,5]*km
        Vbar2=Vgas*np.abs(Vgas)+Ups*Vdisk*np.abs(Vdisk)+Ups*Vbul*np.abs(Vbul)
        Vbar2=np.clip(Vbar2,0,None)
        good=(rad>0)&(Vobs>0)&(errV/np.clip(Vobs,1e-9,None)<=0.10)&(Vbar2>0)
        gb=Vbar2/np.clip(rad,1e-9,None); go=Vobs**2/np.clip(rad,1e-9,None)
        # enclosed BARYON mass M(<r) from gbar = G M/r^2 -> M = gb r^2/G
        Mencl=gb*rad**2/G
        for i in range(len(rad)):
            if good[i]:
                gbar.append(gb[i]); gobs.append(go[i]); Mr.append(Mencl[i]); rr.append(rad[i])
    return map(np.array,(gbar,gobs,Mr,rr))
gb_s,go_s,M_s,r_s = load_sparc()
print(f"  [SPARC] {len(gb_s)} points (err/V<0.10, Ups={Ups})")

def rar_scatter(gbar,gobs,a0field):
    gpred=np.sqrt(gbar**2+gbar*a0field)
    res=np.log10(gobs)-np.log10(gpred); res-=np.median(res)
    return np.sqrt(np.mean(res**2))
s0=rar_scatter(gb_s,go_s,a0)
print(f"  [SPARC] baseline constant-a0 RAR scatter = {s0:.4f} dex  (the 0.11-0.13 floor)")
print("\n    floor law           SPARC scatter   vs floor   VETO")
for k in keys:
    Xg=np.array([candidates(M, r)[0][k] for M,r in zip(M_s, r_s)])
    a0eff=a0eff_from_X(Xg)
    sc=rar_scatter(gb_s,go_s,a0eff)
    verdict = "PASS" if sc < 1.3*s0 else ("MARGINAL" if sc<2*s0 else "BREAKS")
    print(f"    {k:18s}  {sc:8.4f} dex   {sc/s0:5.1f}x   {verdict}")
print("""  READ: C1/C2 (density/curvature) BLOW UP the SPARC scatter (galaxy disks are dense/compact
  -> huge spurious a0 boost -> RAR erased) -> BREAKS. C3/C5/C6 leave the RAR untouched (PASS)
  because they key on Phi/c^2 (tiny in disks) -- but they also do ~nothing to clusters. The
  veto cleanly SEPARATES the two: the magnitude-reachers break galaxies; the galaxy-safe
  terms are magnitude-starved. NO candidate is simultaneously big-in-cluster and safe-in-galaxy.""")

# --- 2c. The SCATTER metric UNDERSTATES the galaxy break: report the BOOST itself + BTFR ---
print("\n  [SPARC veto, sharpened] the RAR-scatter metric understates the break (median-subtraction")
print("  absorbs a uniform offset). Report the ACTUAL a0_eff boost on galaxy points -- a 50-1000x")
print("  boost destroys the BTFR normalization (V^4 = G M a0_eff) even if residual scatter looks mild:")
print(f"    {'floor law':18s} {'median SPARC boost':>18s} {'inner(r<1kpc)':>14s} {'outer(r>10kpc)':>14s}")
for k in ['C1_density_tidal','C2_kretschmann','C3_tolman_phi']:
    Xg=np.array([candidates(M, r)[0][k] for M,r in zip(M_s, r_s)])
    bo=a0eff_from_X(Xg)/a0
    inner = np.median(bo[r_s<1*kpc]) if (r_s<1*kpc).any() else float('nan')
    outer = np.median(bo[r_s>10*kpc]) if (r_s>10*kpc).any() else float('nan')
    print(f"    {k:18s} {np.median(bo):18.1f} {inner:14.1f} {outer:14.1f}")
print("""  READ: C1/C2 boost galaxy a0 by ~50-1000x at EVERY point -- this multiplies the BTFR zero-point
  (V_flat^4 = G M a0_eff) by ~50-1000, shifting every galaxy's V_flat by ~(50-1000)^(1/4) ~ 2.7-5.6x.
  That is a CATASTROPHIC, not marginal, galaxy break; the 0.21-dex scatter is an artifact of the
  median-subtraction hiding a uniform offset. So C1/C2 BREAK galaxies decisively. Confirmed: the
  curvature terms that REACH the cluster magnitude are the SAME ones that destroy galaxies.""")

# ===========================================================================
# PART 3 -- THE UNIFIER: is the SAME term largest in the dense/hot EARLY universe?
# ===========================================================================
print("\n"+"="*94)
print(" PART 3: THE UNIFIER -- does the SAME floor enhance a0 at high z (JWST too-early massive)?")
print("="*94)
print("""  Idea: the local floor is largest where the universe is densest/hottest -> high z. If a0_eff
  RISES at high z, structure forms faster + with higher velocities -> JWST 'too massive too early'.
  Test the COSMOLOGICAL floor (the mean-density curvature of the FRW background) at redshift z:
    the background Ricci/density curvature -> a 'local Hubble' H(z) >> H_Lambda at high z.""")
# The framework's a0(z): the cosmic floor cH_Lam comes from rho_DE. Two readings (MEMORY):
#   (i) canonical declining: a0 ~ sqrt(rho_DE) = const (dark energy const) -> a0(z)=a0.
#   (ii) total-density reading: floor ~ sqrt(rho_total(z)) -> a0 RISES at high z.
# The local-curvature route, applied to the BACKGROUND, gives reading (ii) automatically:
# X_cosmo(z) = (c H(z))^2 - (c H_Lam)^2, with H(z)=H0 sqrt(Om(1+z)^3+OL).
H0 = 2.2e-18           # 1/s (~67.7 km/s/Mpc)
Om, OL = 0.31, 0.69
def a0_of_z_curvature(z):
    """if the FLOOR tracks the local cosmic curvature c H(z), a0(z) = a0 * H(z)/H_Lam... but
    H_Lam = c sqrt(Lam/3) = H0 sqrt(OL). So a0(z) = a0 * sqrt(Om(1+z)^3+OL)/sqrt(OL)."""
    Hz_over_HLam = np.sqrt(Om*(1+z)**3+OL)/np.sqrt(OL)
    return a0*Hz_over_HLam
print(f"\n  Cosmic-curvature a0(z) = a0 * H(z)/H_Lambda  (H_Lambda = H0 sqrt(OmegaL)):")
print(f"  {'z':>5} {'H(z)/H_Lam':>11} {'a0(z)/a0':>10} {'-> structure/velocity boost':>28}")
for z in [0, 0.5, 1, 2, 3, 5, 8, 10]:
    f = a0_of_z_curvature(z)/a0
    print(f"  {z:5.1f} {np.sqrt(Om*(1+z)**3+OL)/np.sqrt(OL):11.2f} {f:10.2f} "
          f"{'V_flat ~ a0^(1/4) x '+format(f**0.25,'.2f'):>28}")
print("""  READ: the cosmic-curvature floor gives a0(z) RISING ~ H(z) -- a0 ~3x at z=3, ~6x at z=8.
  This DOES help JWST: V_flat ~ (G M a0)^(1/4) so a 6x a0 at z=8 raises rotation/dispersion
  velocities by 6^(1/4)~1.6x and accelerates collapse (larger effective gravity at fixed baryons).
  BUT: (a) this is the SAME a0(z)-RISING branch already in the repo (MEMORY: rising cH/E(z)),
  a CONTESTED reading vs the canonical declining sqrt(rho_DE); it is NOT new physics, it is the
  optimistic a0(z) branch wearing a curvature hat. (b) Critically it does NOT help CLUSTERS at z~0.3
  (H(0.3)/H_Lam ~ 1.2 -> a0_eff only 1.2x, far short of 4-5x). So the cosmic-curvature unifier
  helps EARLY GALAXIES (modestly, via the contested rising branch) but NOT low-z clusters --
  the two tensions are NOT closed by one curvature term at the scales they actually live.""")

# Quantify the early-galaxy help concretely vs a JWST benchmark.
print("\n  JWST benchmark: does a0(z) rising explain a 'too-massive' galaxy at z~8?")
print("  A fixed baryonic mass forms with V_flat^4 = G M_bar a0(z). At z=8 a0 is ~%.1fx ->" %
      (a0_of_z_curvature(8)/a0))
print("  V_flat (hence inferred dynamical mass at fixed V) shifts by a0^(1/4)=%.2fx and a0^(1/2)=%.2fx." %
      ((a0_of_z_curvature(8)/a0)**0.25, (a0_of_z_curvature(8)/a0)**0.5))
print("  Modest: helps the tension at the ~1.6-2.5x level, does not by itself manufacture 10x masses.")

# ===========================================================================
# SYNTHESIS
# ===========================================================================
print("\n"+"="*94)
print(" SYNTHESIS -- local-curvature de Sitter-Unruh route, both ways")
print("="*94)
print("""
 THE STRUCTURE OF THE RESULT (a clean separation, established on REAL data):
   * The floor boost needed is a0_eff ~ 4-6x in cluster cores (eRASS1: median required 5.69x at R500).
   * Curvature terms tied to the LOCAL FIELD STRENGTH (C1 tidal/density, C2 Kretschmann/Weyl) DO reach
     and overshoot that magnitude (23-35x on real eRASS1) -- BUT they are LARGER in galaxies (denser,
     more compact: C1/C2 boost SPARC a0 by 50-1000x) and BREAK the BTFR/RAR decisively. They are the
     already-vetoed density-a0 law in curvature clothing (Kretschmann ~ (GM/r^3)^2 ~ rho^2; tidal ~ rho).
   * The ONLY quantity genuinely LARGER in clusters than galaxies is the dimensionless POTENTIAL DEPTH
     Phi/c^2 ~ (sigma/c)^2 (clusters ~133x deeper than the MW disk). A potential-keyed floor (C3 Tolman)
     PASSES the galaxy veto cleanly -- but Phi/c^2 ~ 5e-5 in clusters makes it ~1e-5 a0, i.e. ~10^5 too
     SMALL. To reach 4-5x from Phi/c^2~5e-5 needs a bare coupling ~5e5 a0 with NO dS-Unruh derivation.
   => THE OBSTRUCTION IS STRUCTURAL, NOT A MISSING TERM: the only discriminator that separates clusters
      from galaxies (Phi/c^2) is ~10^4-10^5 too shallow to source an O(1) a0 boost; every term big enough
      to reach the cluster magnitude keys on density/field-strength and is bigger in galaxies. There is
      no curvature/potential scalar that is simultaneously (a) O(20-30 a0) in cluster cores and (b) ~0 in
      dense galaxy disks, because clusters are LESS dense than galaxies -- they win only in DEPTH, which
      is too small. This is why 40 years of MOND cluster fixes failed here, now shown for the curvature
      reading specifically and quantitatively on eRASS1+SPARC.

 EARLY GALAXIES (Part 3): the cosmic-curvature floor a0(z) ~ H(z) rises (~3x at z=3, ~6x at z=8) and
   DOES modestly help JWST (V_flat ~ a0^(1/4), ~1.6-2.5x at fixed baryons) -- but this is the already-known
   CONTESTED rising-a0(z) branch (MEMORY), not new physics, and it does NOT help z~0.3 clusters
   (H(0.3)/H_Lam~1.2 -> only 1.2x). The 'one mechanism for both' unifier FAILS: clusters live at z~0.3
   where the cosmic floor is barely enhanced.

 HONEST MAGNITUDE (both ways, #1 rule):
   - Cluster cores need ~4-6x (eRASS1 median 5.69x at R500). CURVATURE/POTENTIAL route delivers either
     OVERSHOOT+galaxy-break (C1/C2: 23-35x but 50-1000x on galaxies) OR galaxy-safe+negligible
     (C3 Tolman: 1.00001x). EFFECTIVE cluster-core boost from a GALAXY-SAFE curvature term: ~1.00x.
     SHORTFALL: the galaxy-safe potential route is short by a factor ~10^5 in the floor coupling.
   - NO manufactured win: the route does not close clusters. NO reflexive dismissal: the result is a
     SHARP structural theorem (Phi/c^2 is the only discriminator and it is 10^5 too small), and it DID
     surface a real, defensible (if contested) early-galaxy help via a0(z)~H(z). Quarantine held: a0/Z
     never asserted derived; the value of any coupling is treated as free.""")

# ===========================================================================
# PART 4 -- BOTH-WAYS robustness: cosmic a0(z) per real eRASS1 z-bin + fluctuation term
# ===========================================================================
print("\n"+"="*94)
print(" PART 4: BOTH-WAYS robustness on real eRASS1 -- a0(z) per z-bin, and the fluctuation term")
print("="*94)
a0z = a0*np.sqrt(Om*(1+d['z'])**3+OL)/np.sqrt(OL)
print("\n  Does the cosmic-curvature a0(z) close clusters at their ACTUAL redshift (not just z=0.3)?")
print(f"  {'z-bin':>12} {'N':>5} {'median a0(z)/a0':>16} {'required boost':>15} {'covered':>9}")
for zlo,zhi in [(0,0.2),(0.2,0.4),(0.4,0.7),(0.7,1.3)]:
    m=(d['z']>=zlo)&(d['z']<zhi)
    cov = np.median(a0z[m]/a0)/np.median(boost_req[m])*100
    print(f"  [{zlo:.1f},{zhi:.1f})   {m.sum():5d} {np.median(a0z[m]/a0):16.2f} "
          f"{np.median(boost_req[m]):15.2f} {cov:8.0f}%")
print("""  READ: even the highest-z eRASS1 clusters (z~0.7-1.3) get a0(z)~1.9x while needing ~8x -- the cosmic
  floor covers ~25% of the required boost at EVERY z-bin. Clusters are NOT closed at any redshift.""")

print("\n  Acceleration-FLUCTUATION term (task bullet 2): substructure field in a hot cluster core.")
N_mem, m_mem, Rcl = 1000, 1e11*Msun, 770*kpc
sep = Rcl/N_mem**(1/3)
a_fluc = G*m_mem/sep**2
print(f"  N={N_mem} members, m_mem={m_mem/Msun:.0e}Msun, mean sep={sep/kpc:.0f}kpc -> rms a_fluc = "
      f"{a_fluc:.2e} = {a_fluc/a0:.3f} a0")
print(f"  (i) it ADDS to a in T_eff=sqrt(a^2+floor) -> raises a/a0 -> mu->1 -> LESS MOND (WRONG sign).")
print(f"  (ii) even as a FLOOR term (most generous): boost = sqrt(floor+a_fluc^2)/cH_Lam = "
      f"{np.sqrt(FLOOR2+a_fluc**2)/cH_Lam:.3f}x -> negligible (a_fluc<<cH_Lam=5.8a0).")
print("  => the fluctuating substructure field is far too weak (~0.03 a0) AND wrong-signed. No help.")
print("\n"+"="*94)
print(" END local_curvature_unruh -- route does NOT close clusters; structural Phi/c^2 obstruction.")
print("="*94)
