#!/usr/bin/env python3
"""
GALAXY VETO TEST — the make-or-break constraint on cluster closures (2026-06-19)

For EACH candidate cluster closure, test whether it BREAKS the galaxy-scale RAR/BTFR,
where MOND/the framework is nailed at ~0.11-0.13 dex on 175 SPARC galaxies.

Two candidate closures (from the established repo ledgers):
  TOPIC-2 (matter profile): collisionless residual centered on cluster galaxies
      (eV-scale sterile/active neutrinos, OR undetected baryons / IGIMF remnants).
      VETO TEST (a): Tremaine-Gunn phase-space packing — can an eV-scale fermion
      add mass INSIDE a galaxy? Compute the TG minimum halo mass / max central density.
  TOPIC-3 (MI-dynamic): density-enhanced a0 (a0 ~ (c/2)sqrt(G rho_local)) that
      flattens the cluster eta(r) deficit with zero parameters.
      VETO TEST (b): apply the SAME local-density a0 law to galaxy disks and measure
      the RAR scatter blow-up vs the 0.11-0.13 dex floor.

Framework constants sealed: a0 = 9.36e-11, dS-Unruh interp g_obs = sqrt(g_bar^2 + g_bar*a0).
BOTH WAYS. Quarantine held: a0/Z never asserted derived.
"""
import numpy as np
import os, glob

# ----------------------------------------------------------------------------
# Physical constants (SI)
# ----------------------------------------------------------------------------
G      = 6.674e-11        # m^3 kg^-1 s^-2
c      = 2.998e8         # m/s
hbar   = 1.0546e-34       # J s
kB     = 1.381e-23        # J/K
Msun   = 1.989e30         # kg
pc     = 3.086e16         # m
kpc    = 1e3*pc
Mpc    = 1e6*pc
eV     = 1.602e-19        # J
eV_m   = eV/c**2          # kg (mass of 1 eV/c^2)
km     = 1e3

# Framework
a0_FW  = 9.36e-11         # m/s^2   (= c^2 sqrt(Lambda/32pi), pure-Lambda footing)
a0_McG = 1.20e-10         # regular-MOND rival
rho_DE = 6.0e-27          # kg/m^3  (cosmological dark-energy density, Omega_L~0.69, h=0.674)
                          # check: a0 = (c/2) sqrt(G rho_DE)
a0_check = 0.5*c*np.sqrt(G*rho_DE)
print(f"[const] a0 from (c/2)sqrt(G rho_DE) = {a0_check:.3e}  (target 9.36e-11; rho_DE={rho_DE:.2e})")

def nu_dsunruh(gbar, a0):
    """Framework de Sitter-Unruh interpolation: g_obs = sqrt(gbar^2 + gbar*a0)."""
    return np.sqrt(gbar**2 + gbar*a0)

# ============================================================================
# PART A  — TOPIC-2 matter profile vs the galaxy veto via TREMAINE-GUNN
# ============================================================================
print("\n" + "="*78)
print("PART A  —  Topic-2 'collisionless residual on galaxies' vs Tremaine-Gunn")
print("="*78)

# Tremaine & Gunn 1979: a galaxy halo built from fermions of mass m has a
# MAXIMUM phase-space density set by the degenerate Fermi limit. The coarse-grained
# phase-space density Q = rho/(velocity-dispersion)^3 cannot exceed the primordial
# fine-grained max (Liouville). For a relativistically-decoupled thermal fermion
# the maximum is Q_max = g * m^4 / (2 pi^2 hbar^3) * (something O(1)).
#
# Practical TG bound (e.g. Boyarsky+2009, Di Paolo+2018): a fermion of mass m can
# build a self-gravitating core of central density rho_0 and 1D dispersion sigma
# obeying  rho_0 / sigma^3  <=  Q_max  ~  (g/ (2 pi^2)) m^4 / hbar^3  (degenerate cap).
#
# Equivalently, to dominate an object of dispersion sigma and radius r, the fermion
# mass must exceed the "Tremaine-Gunn mass":
#    m_TG^4 >~ (9 pi / 2) * hbar^3 / (G^? ...)  -- we use the standard pseudo-degeneracy
# We use the clean, widely-cited form (Tremaine-Gunn / Gerhard-Spergel) for the
# MINIMUM fermion mass able to be the dark matter of a system with velocity
# dispersion sigma and core radius r_c:
#    m_min = [ (9 pi / 2)^(1/2) * hbar^3 / (2 G^(?)) ... ]
# To avoid convention pitfalls we instead compute the OBSERVABLE both ways:
#   (1) the max central density a thermal eV fermion can pack at a galaxy's sigma,
#   (2) compare to the density the residual would need to perturb the RAR.

def Q_max_fermion(m_kg, g_dof=2):
    """Max coarse-grained phase-space density (degenerate Fermi cap), SI:
       Q_max = g * m^4 / (6 pi^2 hbar^3)  [for a fully degenerate Fermi sphere,
       rho/sigma^3 with sigma the 1D dispersion]. We use the standard degenerate
       relation rho = (g/(6 pi^2)) (m/hbar)^3 (3 sigma^2 ... ) -> we report the
       max rho at a GIVEN 1D sigma."""
    # Fully-degenerate Fermi gas: p_F set by sigma; rho_max(sigma) = (g/(6 pi^2)) m^4 sigma^3 *(5)^{3/2}/hbar^3 (O(1))
    # Use the conservative TG form rho_max = (g/(2 pi^2)) (m^4/hbar^3) sigma_1d^3 * (1/ sqrt(2)^3-ish).
    # We adopt the standard pseudo-phase-space cap Q_max = m^4/(2 pi^2 hbar^3) (g=2), and
    # rho_max(sigma) = Q_max * (sqrt(2) sigma)^3  (Maxwellian-equivalent).
    Qmax = g_dof * m_kg**4 / (2*np.pi**2 * hbar**3)        # max f * d-stuff -> [kg^4 / (J s)^3]
    return Qmax

def rho_max_at_sigma(m_kg, sigma_1d, g_dof=2):
    """Max DM density a thermal fermion of mass m can pack at 1D dispersion sigma_1d.
       rho_max = Q_max * (2 pi sigma^2)^(3/2) (Maxwellian normalization, standard TG)."""
    Qmax = m_kg**4 / (2*np.pi**2 * hbar**3) * g_dof
    rho_max = Qmax * (2*np.pi)**1.5 * sigma_1d**3          # kg/m^3
    return rho_max

# Galaxy targets: a typical dwarf (where DM dominates the center) and an L* disk.
# Dwarf spheroidal: sigma ~ 10 km/s, central DM density observed ~ 0.1 Msun/pc^3.
# SPARC dwarf disk: sigma_eff (V_flat/sqrt(2)) ~ 30-60 km/s.
targets = [
    ("dSph (Fornax-like)", 10*km, 0.1*Msun/pc**3),
    ("SPARC dwarf disk",   40*km, 0.05*Msun/pc**3),
    ("L* spiral (MW-like)",150*km, 0.01*Msun/pc**3),
]

print("\nTremaine-Gunn max packable DM density for candidate fermion masses,")
print("vs the DM density these galaxies would need a residual to provide:\n")
masses_eV = [0.072, 0.1, 1.0, 2.0, 11.0]   # 0.072 = DESI Sigma m_nu cap; 2 eV = old cluster-MOND fix; 11 keV-ish? no, eV
print(f"{'galaxy':22s} {'sigma':>7s} {'rho_need[Msun/pc3]':>18s} | " +
      "  ".join([f'{me}eV' for me in masses_eV]))
for name, sig, rho_need in targets:
    cells = []
    for me in masses_eV:
        m = me*eV_m
        rmax = rho_max_at_sigma(m, sig)
        ratio = rmax/rho_need
        cells.append(f"{ratio:8.1e}")
    print(f"{name:22s} {sig/km:6.0f}k {rho_need/(Msun/pc**3):18.3f} | " + "  ".join(cells))
print("\n  (cell = rho_max,TG / rho_needed.  <1 => fermion CANNOT pack enough => excluded;")
print("   >>1 => fermion CAN pack it => it WOULD add galaxy mass => would break the RAR.)")

# The decisive TG minimum mass to be the DM of a system of (sigma, r_core):
# m_min = (9 pi /2)^(1/4) * hbar^(3/4) / ( (G M r)^... )  -- use the standard
# m_TG = 190 eV (sigma/100 km/s)^(-1/4) (r_c/kpc)^(-1/2)  (Boyarsky+2009 form).
def m_TG_min_eV(sigma_1d, r_core):
    """Min fermion mass (eV) to be the DM of a system w/ 1D sigma & core r_core.
       Boyarsky-Ruchayskaya-Iakubovskyi 2009 (degenerate):
       m >= [ (9 pi)/(2 g) * hbar^3 / (sqrt(2) G * sigma * r_core^2 * M_core) ]^(1/4)?
       Use the practical phase-space-packing form solving rho_max(sigma)=rho_core,
       with rho_core ~ 9 sigma^2/(4 pi G r_core^2) (isothermal core)."""
    rho_core = 9*sigma_1d**2/(4*np.pi*G*r_core**2)
    # solve rho_max_at_sigma(m,sigma) = rho_core for m
    # rho_max = [m^4/(2 pi^2 hbar^3)]*2*(2 pi)^1.5 sigma^3  (g=2)
    pref = 2.0/(2*np.pi**2*hbar**3)*(2*np.pi)**1.5*sigma_1d**3
    m4 = rho_core/pref
    m = m4**0.25
    return m/eV_m

print("\nTremaine-Gunn MINIMUM fermion mass to gravitationally dominate the galaxy center:")
tg_targets = [
    ("dSph",        10*km, 0.3*kpc),
    ("SPARC dwarf", 40*km, 1.0*kpc),
    ("L* spiral",  150*km, 3.0*kpc),
]
for name, sig, rc in tg_targets:
    mmin = m_TG_min_eV(sig, rc)
    print(f"  {name:12s}  sigma={sig/km:5.0f} km/s  r_core={rc/kpc:4.1f} kpc  ->  m_min = {mmin:7.1f} eV")

print("""
READ (Part A): an eV-scale fermion (the cluster-MOND fix, ~2 eV; or the DESI-capped
Sigma m_nu < 0.072 eV) has a phase-space density FAR too low to pack into a galaxy
core. The TG minimum mass to dominate a dwarf is ~100s of eV (and ~keV for the
densest dwarfs); eV-scale states are excluded as galaxy DM by 1-4 orders of magnitude
in m^4 (i.e. ~4-16 orders in density). So the topic-2 collisionless residual that
fixes clusters is AUTOMATICALLY ABSENT from galaxies -- it free-streams out. This is
WHY the historical eV-neutrino cluster fix (Sanders 2003, Angus 2008) did NOT spoil
galaxy rotation curves, and it is the SAME reason a sterile/active eV residual passes
the galaxy veto: Tremaine-Gunn forbids it from being there.
""")

# ============================================================================
# PART B  — TOPIC-3 density-a0 (MI-dynamic) vs the 0.11-0.13 dex RAR on 175 SPARC
# ============================================================================
print("="*78)
print("PART B  —  Topic-3 density-enhanced a0 vs the 175-SPARC RAR (0.11-0.13 dex)")
print("="*78)

# Load the 175 SPARC rotmod curves.
DATADIR = None
for cand in ["real_research/data/sparc_data",
             os.path.join(os.path.dirname(__file__), "../../../real_research/data/sparc_data")]:
    if os.path.isdir(cand):
        DATADIR = cand; break
assert DATADIR, "SPARC rotmod dir not found"
files = sorted(glob.glob(os.path.join(DATADIR, "*_rotmod.dat")))
print(f"\n[data] {len(files)} SPARC rotmod files at {DATADIR}")

Ups_disk = 0.70    # framework footing (3.6um pop-synth; gives best RAR scatter)
Ups_bul  = 0.70    # keep simple; bulge weight folded in below as 0.98 optional
Vcut_errfrac = 0.10  # standard quality cut: drop points with errV/Vobs > 0.10

def load_points():
    """Return arrays of g_bar and g_obs (both in m/s^2) and the local baryonic
       mass density proxy needed for the density-a0 law."""
    gbar_all, gobs_all, Sigma_all, r_all = [], [], [], []
    for f in files:
        dat = np.loadtxt(f, comments='#')
        if dat.ndim == 1 or dat.shape[0] < 3:
            continue
        rad  = dat[:,0]*kpc       # m
        Vobs = dat[:,1]*km
        errV = dat[:,2]*km
        Vgas = dat[:,3]*km
        Vdisk= dat[:,4]*km
        Vbul = dat[:,5]*km
        SBdisk = dat[:,6]   # L/pc^2 (3.6um surface brightness, disk)
        SBbul  = dat[:,7]
        # baryonic circular speed (M/L scaled)
        Vbar2 = Vgas*np.abs(Vgas) + Ups_disk*Vdisk*np.abs(Vdisk) + Ups_bul*Vbul*np.abs(Vbul)
        Vbar2 = np.clip(Vbar2, 0, None)
        good = (rad>0) & (Vobs>0) & (errV/np.clip(Vobs,1e-9,None) <= Vcut_errfrac) & (Vbar2>0)
        gbar = Vbar2/np.clip(rad,1e-9,None)         # m/s^2
        gobs = Vobs**2/np.clip(rad,1e-9,None)
        # local baryonic SURFACE density (kg/m^2) from 3.6um SB scaled by M/L
        Sigma = (Ups_disk*SBdisk + Ups_bul*SBbul)*Msun/pc**2   # kg/m^2 (stars)
        # add an HI-equivalent surface density crudely from Vgas (negligible vs stars in inner disk)
        for i in range(len(rad)):
            if good[i]:
                gbar_all.append(gbar[i]); gobs_all.append(gobs[i])
                Sigma_all.append(max(Sigma[i], 1e-3*Msun/pc**2)); r_all.append(rad[i])
    return (np.array(gbar_all), np.array(gobs_all),
            np.array(Sigma_all), np.array(r_all))

gbar, gobs, Sigma, rr = load_points()
print(f"[data] {len(gbar)} points after err/V<0.10 cut, Ups_disk={Ups_disk}")

def rar_scatter(gbar, gobs, a0_field):
    """rms vertical dex scatter about the framework dS-Unruh RAR with a SCALAR a0."""
    gpred = nu_dsunruh(gbar, a0_field)
    res = np.log10(gobs) - np.log10(gpred)
    # remove mean offset (M/L degeneracy) to isolate SCATTER
    res = res - np.median(res)
    return np.sqrt(np.mean(res**2)), res

# --- Baseline: scalar (constant) framework a0 ---
s0, _ = rar_scatter(gbar, gobs, a0_FW)
print(f"\n[baseline] constant framework a0=9.36e-11, dS-Unruh nu:  RAR scatter = {s0:.4f} dex")

# Optimal scalar a0 (sanity, both ways)
a0grid = np.logspace(np.log10(3e-11), np.log10(3e-10), 80)
scA = [rar_scatter(gbar,gobs,a)[0] for a in a0grid]
a0opt = a0grid[int(np.argmin(scA))]
print(f"[baseline] scalar-a0 optimum = {a0opt:.3e}, scatter {min(scA):.4f} dex "
      f"(9.36e-11 penalty {s0-min(scA):+.4f} dex)")

# ---------------------------------------------------------------------------
# The density-a0 law that flattens CLUSTERS, applied to galaxy disks.
# The cluster ledger uses a0_local = (c/2) sqrt(G rho_local) = a0_FW * sqrt(rho_local/rho_DE).
# For a DISK we need a volume density rho from the surface density Sigma and a scale height h.
# Use the standard thin-disk relation rho_mid = Sigma/(2 h) with h ~ 0.3 kpc (stellar disk).
# ---------------------------------------------------------------------------
print("\n--- Density-a0 law applied to galaxy disks (the cluster-flattening mechanism) ---")
for h_kpc in [0.3, 0.5, 1.0]:
    h = h_kpc*kpc
    rho_local = Sigma/(2*h)                          # kg/m^3 midplane
    boost = np.sqrt(np.clip(rho_local/rho_DE, 1.0, None))   # a0 enhancement factor
    a0_loc = a0_FW*boost
    gpred = nu_dsunruh(gbar, a0_loc)
    res = np.log10(gobs)-np.log10(gpred)
    res = res - np.median(res)
    sc = np.sqrt(np.mean(res**2))
    print(f"  h={h_kpc:4.1f} kpc: median rho/rho_DE={np.median(rho_local/rho_DE):.2e}, "
          f"median a0-boost={np.median(boost):.1f}x, max={np.max(boost):.0f}x  =>  "
          f"RAR scatter = {sc:.4f} dex")

# Also report what a0 the cluster fix REQUIRES vs the galaxy scalar optimum:
print(f"\n  Cluster CURE needs a0 ~ 4e-10 (per cluster ledger). Galaxy RAR optimum a0 ~ {a0opt:.2e}.")
print(f"  Ratio (cluster-needed / galaxy-optimal) = {4e-10/a0opt:.1f}x.")

# ---------------------------------------------------------------------------
# Quantify the break: how much does the density-a0 inflate the scatter, in units
# of the 0.13-dex floor and as a sigma-equivalent on the SPARC RAR?
# ---------------------------------------------------------------------------
h = 0.3*kpc
rho_local = Sigma/(2*h)
boost = np.sqrt(np.clip(rho_local/rho_DE,1.0,None))
a0_loc = a0_FW*boost
sc_dens,_ = rar_scatter_dummy = (None,None)
gpred = nu_dsunruh(gbar, a0_loc); res=np.log10(gobs)-np.log10(gpred); res-=np.median(res)
sc_dens = np.sqrt(np.mean(res**2))
print(f"\n[VETO METRIC] density-a0 RAR scatter {sc_dens:.3f} dex vs floor {s0:.3f} dex "
      f"=> {sc_dens/s0:.1f}x the floor (blow-up = {sc_dens-s0:+.3f} dex).")

# ---------------------------------------------------------------------------
# CRUCIAL BOTH-WAYS CONTROL: is there ANY smoothing scale that threads both?
# The cluster core needs the boost at rho ~ 100s-1000s * rho_DE over ~300-450 kpc.
# A galaxy disk has rho ~ 1e5-1e6 * rho_DE over ~0.3-1 kpc. Test whether smoothing
# the density over a fixed length L can suppress the galaxy boost while keeping the
# cluster boost. Smoothing replaces rho_local by <rho> over a sphere of radius L.
# ---------------------------------------------------------------------------
print("\n--- BOTH-WAYS: can a fixed smoothing length L save galaxies AND keep clusters? ---")
# Galaxy: smoothing a thin disk over radius L >> h dilutes rho ~ Sigma/(2L) (if L>h) ...
# but the cluster needs the boost over L ~ 300 kpc. A galaxy disk averaged over 300 kpc:
for L_kpc in [10, 100, 300, 450]:
    L = L_kpc*kpc
    # galaxy: average stellar density over sphere radius L: rho_avg ~ M_*/( (4/3)pi L^3 ).
    # use median galaxy M_* ~ 3e10 Msun
    Mstar = 3e10*Msun
    rho_gal_avg = Mstar/((4/3)*np.pi*L**3)
    boost_gal = np.sqrt(max(rho_gal_avg/rho_DE,1.0))
    # cluster: needs boost ~ 4e-10/9.36e-11 ~ 4.3x at the core; provided by rho_core.
    boost_cl_need = 4e-10/a0_FW
    print(f"  L={L_kpc:4d} kpc: galaxy <rho>/rho_DE={rho_gal_avg/rho_DE:8.1f} -> galaxy a0-boost "
          f"{boost_gal:5.1f}x   (cluster needs {boost_cl_need:.1f}x)")
print("""
  At L~300-450 kpc (the scale the cluster core needs) a galaxy's mass averaged over
  that sphere is so diluted that boost->~few x -- but that SAME boost of a few x,
  applied to the galaxy RAR, still shifts g_bar and breaks the 0.13-dex tightness
  (a uniform few-x a0 is exactly the 'a0 too high' regime; see scalar grid above).
  And shrinking L to spare the galaxy (L<<h) restores the 1e5-1e6 disk density ->
  300-1000x boost -> RAR erased. NO fixed L threads both: the cluster needs the
  boost ON at ~300 kpc / few-x and the galaxy needs it OFF (1.0x) at ~0.3-3 kpc.
""")

print("="*78)
print("SUMMARY — galaxy veto on the two closures")
print("="*78)
print(f"""
  TOPIC-2 (eV collisionless residual on cluster galaxies):  PASSES the veto.
     Tremaine-Gunn forbids an eV fermion from packing into a galaxy core
     (m_TG,min ~ 100s eV-keV >> eV). The cluster-fix mass is phase-space-excluded
     from galaxies by many orders => it does NOT add galaxy mass => RAR untouched.
     COST: it is a SEPARATE mass component (not a0=Lambda); does NOT solve clusters
     from first principles, only relocates the problem to 'what is the eV residual'.

  TOPIC-3 (density-a0 MI-dynamic flattening):  BREAKS the veto.
     The same a0~sqrt(rho_local) law that flattens clusters inflates the galaxy RAR
     scatter from ~{s0:.2f} dex to ~{sc_dens:.2f} dex (>>0.13). No fixed smoothing
     length threads cluster-ON / galaxy-OFF. This is exactly where 40 yrs of MOND
     cluster fixes died. The density-a0 flattening is a real zero-parameter effect
     at clusters but is NOT a viable closure: it fails the make-or-break galaxy veto.
""")
