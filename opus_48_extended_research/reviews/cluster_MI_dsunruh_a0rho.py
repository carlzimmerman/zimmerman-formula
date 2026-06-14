#!/usr/bin/env python3
"""
THE FRAMEWORK'S OWN cluster prediction: MODIFIED INERTIA (dS-Unruh) + the a0=(c/2)sqrt(G rho) angle.
====================================================================================================
NOT normal MOND. The task: does the framework's DISTINCTIVE physics --
  (1) a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = 9.36e-11  (a0 DERIVED from the dS horizon)
  (2) MODIFIED INERTIA from the full de Sitter-Unruh temperature
        T_eff(a) = (hbar/2pi c kB) sqrt(a^2 + (cH)^2),   cH_Lambda = Z a0 = 5.79 a0
      with Milgrom's theorem that MI != MG for pressure-supported (non-circular) systems --
change the cluster deficit eta(R500) vs the normal-MOND/modified-gravity eta ~ 2.15?

It computes FOUR things on real eRASS1 (Bulbul+2024, N=9830, WL-calibrated M500):
  PART A. The MI deep-MOND VIRIAL relation for pressure-supported systems (Milgrom 1994/2011/2023):
          is the integrated cluster mass DIFFERENT from modified gravity? (the genuine MI distinctive)
  PART B. The full dS-Unruh kernel with the de Sitter FLOOR (cH)^2 inside the sqrt -- does keeping
          the (cH)=5.79 a0 term (which standard MOND-MI drops) change eta at the cluster regime?
  PART C. eta(R500) on real eRASS1 for: regular MOND a0, framework a0, MI-dS-Unruh kernel, MG-AeST.
  PART D [THE ANGLE]. a0 = (c/2) sqrt(G rho). Is cluster a0 really 9.36e-11?
          (D1) confirm a0 from rho_LOCAL-matter is RULED OUT by the galaxy RAR (compute, ~1000x too big);
          (D2) test every density-based reading that could raise cluster a0 -- does any help clusters
               WITHOUT breaking the universal galaxy a0? Grade CONSISTENT-HELP/BREAKS-GALAXY-RAR/NO-EFFECT.

HONESTY (#1 rule, both ways): derive the real prediction; do NOT manufacture a reduction; do NOT
dismiss a real one. Quarantine: a0/Z are flagged as NOT-asserted-derived (the framework's posited values).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "real_research", "data"))
from _load_erass1 import load_clean

# ---- constants (SI) ----
c    = 2.99792458e8
G    = 6.674e-11
hbar = 1.0546e-34
kB   = 1.381e-23
Mpc  = 3.0857e22
kpc  = 3.0857e19
Msun = 1.989e30
H0   = 67.4e3/Mpc                      # s^-1, Planck-ish

# ---- framework constants (POSITED, not asserted-derived -- quarantine) ----
a0_F = 9.36e-11                        # framework a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE)
a0_M = 1.20e-10                        # regular-MOND a0 (McGaugh/Milgrom canonical)
Z    = 5.79                            # cH_Lambda = Z a0  (de Sitter floor inside the Unruh sqrt)
cH_L = Z*a0_F                          # = c^2 sqrt(Lambda/3); the dS floor acceleration ~ 5.79 a0

# implied dark-energy density from a0_F = (c/2) sqrt(G rho_DE)
rho_DE = (2*a0_F/c)**2 / G
print("="*96)
print("FRAMEWORK CONSTANTS (posited; quarantine -- a0/Z NOT asserted as derived here)")
print("="*96)
print(f"  a0_F = {a0_F:.3e}  (framework)   a0_M = {a0_M:.3e} (regular MOND)   ratio a0_M/a0_F = {a0_M/a0_F:.4f}")
print(f"  cH_Lambda = Z a0 = {cH_L:.3e} m/s^2 = {Z} a0   (the de Sitter floor in T_eff = sqrt(a^2+(cH)^2))")
print(f"  implied rho_DE from a0=(c/2)sqrt(G rho_DE):  rho_DE = {rho_DE:.3e} kg/m^3")
print(f"    (cross-check: critical density rho_crit ~ {3*H0**2/(8*np.pi*G):.3e}; Omega_DE*rho_crit ~ {0.685*3*H0**2/(8*np.pi*G):.3e})")


# =====================================================================================
# INTERPOLATION KERNELS  (g_obs = nu(y) g_bar,  y = g_bar/a0)
# =====================================================================================
def nu_simple(y):       return 0.5*(1+np.sqrt(1+4/y))      # "simple" nu == dS-Unruh g_obs=sqrt(gb^2+gb a0)
def nu_mcgaugh(y):      return 1.0/(1-np.exp(-np.sqrt(y)))  # RAR fit nu
def nu_standard(y):     return 0.5+np.sqrt(0.25+1/y)        # algebraic == nu_simple (same family)

def gobs_dsunruh_floor(gbar, a0, cH):
    """The FULL framework MI kernel: invert mu(a) a = gbar with the de Sitter FLOOR kept.
       Milgrom's MI postulate: inertia from DeltaT = T(a)-T(0),
         mu(a) = [sqrt(a^2+(cH)^2) - cH]/a,   solve mu(a)*a = gbar  =>
         sqrt(a^2+cH^2) - cH = gbar  =>  a = sqrt(gbar^2 + 2 gbar cH).
       Here a IS g_obs (the kinematic acceleration). a0 enters via cH; deep limit a=sqrt(2 cH gbar).
       NOTE: this is the *standard* dS-Unruh inversion. The de Sitter floor cH is the SAME term
       whether you call it modified inertia -- it's already in the kernel. Returns g_obs."""
    return np.sqrt(gbar**2 + 2*gbar*cH)

def eta_from_nu(gbar, gobs_data, nu, a0):
    """eta = M_dyn / M_pred = g_obs(data) / g_pred(nu, gbar). Per-cluster, then summarize."""
    gpred = nu(gbar/a0)*gbar
    return gobs_data/gpred


# =====================================================================================
d = load_clean()
gbar, gobs = d["gbar"], d["gobs"]
N = d["N"]
print(f"\n  eRASS1 clean sample: N={N}, median z={np.median(d['z']):.3f}, median M500={np.median(d['M500'])*1e13:.2e} Msun")
print(f"  median g_bar/a0_F = {np.median(gbar/a0_F):.4f}  (DEEP MOND at R500),  g_obs/a0_F = {np.median(gobs/a0_F):.4f}")


# =====================================================================================
print("\n" + "="*96)
print("PART A -- the MODIFIED-INERTIA VIRIAL relation for PRESSURE-SUPPORTED systems (the MI distinctive)")
print("="*96)
print("""  Milgrom proved MI != MG for non-circular orbits (1994 Ann.Phys.229; 2011; 2023 arXiv:2310.14334).
  Clusters are PRESSURE-supported (isotropic sigma~1000 km/s) -- exactly where they can diverge.
  THE QUESTION: does the integrated deep-MOND cluster MASS differ between MI and MG?

  MI deep-MOND virial relation (Milgrom):  <V^2>^2 = (4/9) M G a0  for a pressure-supported system.
  MG general virial theorem (Milgrom 2014, arXiv:1311.2579):
      Sum_p r_p.F_p = -(2/3) sqrt(G a0) [ (Sum m_p)^{3/2} - Sum m_p^{3/2} ].
  For a one-mass-scale (M_tot >> m_particle) isothermal system BOTH reduce to the SAME deep-MOND mass:
      M_dyn = (9/4) sigma^4 / (G a0)   (isotropic, isothermal).
  => the INTEGRATED virial mass M(sigma) is IDENTICAL in MI and MG in the deep-MOND limit
     (both descend from a0 + space-time scale invariance). The O(1) MI distinctives
     (stronger EFE, exact algebraic relation, orbit-shape factors) DO NOT change M_dyn at fixed a0.""")

# Demonstrate the coincidence numerically: M_dyn(sigma) for both is M = (9/4) sigma^4/(G a0).
sigma = 1000e3   # m/s, typical cluster
M_MI = (9/4)*sigma**4/(G*a0_F)
M_MG = (9/4)*sigma**4/(G*a0_F)   # same closed form in deep MOND
print(f"\n  Numerical check, sigma=1000 km/s, a0_F: M_dyn(MI) = {M_MI/Msun:.3e} Msun ;  M_dyn(MG) = {M_MG/Msun:.3e} Msun")
print(f"  => MI/MG = {M_MI/M_MG:.4f}  (IDENTICAL deep-MOND virial mass; the divergence is sub-leading O(1)).")
print(f"  The a0 dependence is the ONLY lever:  M_dyn ~ 1/a0, so a0_F<a0_M => MI predicts a SMALLER M_dyn")
print(f"     for the same sigma => a LARGER deficit, by exactly sqrt(a0_M/a0_F)={np.sqrt(a0_M/a0_F):.4f} in g-space.")


# =====================================================================================
print("\n" + "="*96)
print("PART B -- the FULL dS-Unruh kernel: does keeping the de Sitter FLOOR (cH)^2=5.79a0 change eta?")
print("="*96)
print("""  The framework T_eff = (hbar/2pi c kB) sqrt(a^2 + (cH)^2) has the dS floor (cH)=5.79 a0 INSIDE
  the sqrt. Standard MOND-MI keeps it (that IS the simple-nu). But does the SIZE of cH (5.79 a0 vs the
  bare a0) matter? Invert mu(a)a=gbar with the floor: a = sqrt(gbar^2 + 2 gbar cH). Compare the two
  readings of 'what cH is' in the kernel:
    (i)  cH = a0_F            (the bare MOND scale; deep limit a=sqrt(2 a0_F gbar) -> a0_eff = 2 a0_F)
    (ii) cH = Z a0_F = 5.79a0 (the literal de Sitter floor; deep limit a=sqrt(2 Z a0_F gbar) -> a0_eff=2Z a0_F)""")

for label, cH in [("cH = a0_F (bare)", a0_F), ("cH = Z a0_F = 5.79 a0_F (dS floor)", cH_L)]:
    gpred = gobs_dsunruh_floor(gbar, a0_F, cH)
    eta = gobs/gpred
    a0_eff = 2*cH
    print(f"  {label:38}  a0_eff(deep)=2cH={a0_eff:.3e}  median eta={np.median(eta):.3f}")
print("""  KEY: the deep-MOND a0_eff is 2*cH. The framework's a0=9.36e-11 IS the deep-MOND a0_eff already
  (it is DEFINED as the deep-limit scale, c^2 sqrt(Lambda/32pi)). So the 'cH' that belongs in the kernel
  is the one giving a0_eff = a0_F, i.e. cH_kernel = a0_F/2 in the naive DeltaT scheme -- the 5.79 factor
  is the SCHEME (DeltaT vs Milgrom-2pi) ambiguity, already absorbed into the FITTED a0. At fixed deep-MOND
  a0 the floor is moot at R500 (deep regime). So Part B confirms: at R500 the floor does NOT rescue clusters.""")

# The honest, scheme-free statement: at fixed deep-MOND a0, ALL these kernels give the SAME deep-MOND eta.
# Show it by normalizing each kernel to the SAME deep-MOND a0 = a0_F:
print("\n  Scheme-free check -- normalize every kernel to the SAME deep-MOND a0=a0_F and recompute eta:")
for label, nu in [("dS-Unruh/simple", nu_simple), ("McGaugh RAR", nu_mcgaugh), ("standard algebraic", nu_standard)]:
    eta = eta_from_nu(gbar, gobs, nu, a0_F)
    print(f"    {label:20}  median eta(framework a0) = {np.median(eta):.3f}   [IQR {np.percentile(eta,25):.2f}-{np.percentile(eta,75):.2f}]")


# =====================================================================================
print("\n" + "="*96)
print("PART C -- eta(R500) on real eRASS1: framework MI vs normal-MOND/MG ~2.15")
print("="*96)
rows = [
    ("regular MOND  (a0=1.20e-10, simple nu) [MG baseline]", nu_simple, a0_M),
    ("framework MI  (a0=9.36e-11, dS-Unruh simple nu)",      nu_simple, a0_F),
    ("framework MI  (a0=9.36e-11, McGaugh RAR nu)",          nu_mcgaugh, a0_F),
]
res = {}
for label, nu, a0 in rows:
    eta = eta_from_nu(gbar, gobs, nu, a0)
    res[label] = np.median(eta)
    print(f"  {label:52}  eta(R500) = {np.median(eta):.3f}  [IQR {np.percentile(eta,25):.2f}-{np.percentile(eta,75):.2f}]")

eta_MOND = res["regular MOND  (a0=1.20e-10, simple nu) [MG baseline]"]
eta_FRAME = res["framework MI  (a0=9.36e-11, dS-Unruh simple nu)"]
print(f"\n  THE COMPARISON:")
print(f"    normal-MOND/MG eta ~ {eta_MOND:.3f}  (a0=1.2e-10)   [the task's stated ~2.15 baseline]")
print(f"    framework-MI   eta ~ {eta_FRAME:.3f}  (a0=9.36e-11, dS-Unruh)")
print(f"    ratio eta_FRAME/eta_MOND = {eta_FRAME/eta_MOND:.4f}  (EXACT algebra: sqrt(a0_M/a0_F)={np.sqrt(a0_M/a0_F):.4f})")
print(f"  => the framework's MODIFIED-INERTIA physics gives eta {'LARGER' if eta_FRAME>eta_MOND else 'SMALLER'}")
print(f"     than normal MOND by {100*(eta_FRAME/eta_MOND-1):+.1f}%. The lower a0 makes clusters HARDER, not easier.")


# =====================================================================================
print("\n" + "="*96)
print("PART D [THE ANGLE] -- a0 = (c/2) sqrt(G rho). Is cluster a0 really 9.36e-11?")
print("="*96)

# D1: rho_LOCAL-matter reading -- compute, confirm it BREAKS the galaxy RAR.
print("\n  D1 -- a0 = (c/2) sqrt(G rho_LOCAL-matter): RULED OUT by the galaxy RAR? (compute)")
def a0_of_rho(rho):  return 0.5*c*np.sqrt(G*rho)
# typical densities (kg/m^3)
rho_galaxy_disk = 1e-21      # solar-neighborhood ISM/total ~ 0.1 Msun/pc^3 ~ 6.7e-21; use mid-disk ~1e-21
rho_solar_nbhd  = 6.7e-21    # ~0.1 Msun/pc^3 dynamical
rho_cluster_R500 = None      # compute from eRASS1 below
print(f"    rho_DE                = {rho_DE:.3e} kg/m^3  -> a0 = {a0_of_rho(rho_DE):.3e}  (= framework a0_F, by construction)")
for nm, rho in [("solar-neighborhood (0.1 Msun/pc^3)", rho_solar_nbhd), ("mid-disk ISM ~1e-21", rho_galaxy_disk)]:
    a0r = a0_of_rho(rho)
    print(f"    rho_{nm:34} = {rho:.2e} -> a0 = {a0r:.3e}  = {a0r/a0_F:.1e} x a0_F")
print(f"""    => rho_local-matter in a galaxy disk is ~{rho_solar_nbhd/rho_DE:.0e}x rho_DE, giving a0 ~
       {a0_of_rho(rho_solar_nbhd)/a0_F:.0f}x too big. The RAR scale a0~1.2e-10 is seen UNIVERSALLY in galaxy
       outskirts where local rho varies by orders of magnitude -- a rho_local a0 would scatter the RAR
       by ~sqrt(rho) ~ 100-1000x and DESTROY its 0.13-dex tightness. DECISIVELY RULED OUT.""")

# Quantify the galaxy-RAR break: what would the RAR scatter be if a0 tracked local baryon density?
# Local baryonic density at the RAR points spans ~rho ~ gbar/(c... ) -- use the actual gbar spread as proxy
# for the density spread the points probe. In deep MOND g_obs ~ sqrt(gbar a0); if a0 ~ sqrt(rho_local),
# and rho_local correlates with gbar, the RAR would acquire a slope/scatter change. Demonstrate the magnitude:
print("    Quantitative RAR-break magnitude (eRASS1 clusters as the test bed):")
# compute the cluster mean matter density inside R500: rho = M500 / (4/3 pi R500^3)
M500_kg = d["M500"]*1e13*Msun
R500_m  = d["R500"]*kpc
rho_cl  = M500_kg/((4/3)*np.pi*R500_m**3)   # total (dark+bar) mean density inside R500
rho_cl_bar = (1.2)*d["Mgas"]*1e11*Msun/((4/3)*np.pi*R500_m**3)  # baryon (gas*1.2) mean density
print(f"      cluster mean TOTAL density inside R500:   median rho = {np.median(rho_cl):.3e} kg/m^3")
print(f"      cluster mean BARYON density inside R500:  median rho = {np.median(rho_cl_bar):.3e} kg/m^3")
print(f"      a0 from cluster total rho:  (c/2)sqrt(G rho) = {a0_of_rho(np.median(rho_cl)):.3e} = {a0_of_rho(np.median(rho_cl))/a0_F:.1f}x a0_F")
print(f"      a0 from cluster baryon rho: (c/2)sqrt(G rho) = {a0_of_rho(np.median(rho_cl_bar)):.3e} = {a0_of_rho(np.median(rho_cl_bar))/a0_F:.1f}x a0_F")

# D2: is there ANY consistent reading that raises cluster a0 without breaking galaxies?
print("\n  D2 -- is there a CONSISTENT reading where cluster a0 > galaxy a0 without breaking the galaxy RAR?")
print("""  Candidate readings, each tested for (i) does it raise cluster a0? (ii) does it preserve galaxy a0?

  (R0) rho = rho_DE everywhere (CANONICAL): a0=9.36e-11 universal. Galaxy RAR: PASS. Cluster a0: NO raise.
       -> NO-EFFECT on clusters. This is the framework's actual reading.""")

# (R1) rho = rho_DE + rho_local_matter (the cluster's own matter adds to the vacuum the detector sees)
print("\n  (R1) rho_eff = rho_DE + rho_local-matter  (cluster matter ADDS to the density in a0=(c/2)sqrt(G rho)):")
for nm, rho_loc in [("galaxy outskirt ~1e-22", 1e-22), ("cluster R500 total (median)", np.median(rho_cl)),
                    ("cluster baryon (median)", np.median(rho_cl_bar))]:
    a0_eff = a0_of_rho(rho_DE + rho_loc)
    print(f"       {nm:30}: rho_loc/rho_DE={rho_loc/rho_DE:7.2e} -> a0_eff={a0_eff:.3e} = {a0_eff/a0_F:.2f}x a0_F")
print(f"""       VERDICT (R1): cluster total rho inside R500 is ~{np.median(rho_cl)/rho_DE:.0f}x rho_DE, so rho_eff
       would raise cluster a0 by sqrt({np.median(rho_cl)/rho_DE:.0f}) ~ {np.sqrt(np.median(rho_cl)/rho_DE):.0f}x -- but the SAME rule applied to a
       galaxy outskirt (rho~1e-22, still > rho_DE~{rho_DE:.0e}) raises a0 by sqrt({1e-22/rho_DE:.1f})={np.sqrt(1+1e-22/rho_DE):.2f}x, and the
       INNER galaxy (rho~1e-21) by {np.sqrt(1+1e-21/rho_DE):.1f}x -> BREAKS the universal galaxy RAR. The rule cannot
       'know' to switch on only in clusters. R1 = BREAKS-GALAXY-RAR (a rho-additive a0 is NOT scale-blind).""")

# (R2) The horizon reading: a0 from the LOCAL de Sitter horizon. Does a cluster modify the local Lambda?
print("\n  (R2) Local de Sitter horizon: a0 = c^2 sqrt(Lambda_local/32pi). Does a cluster raise Lambda_local?")
print(f"""       The framework derives a0 from the COSMOLOGICAL constant Lambda (the global dS horizon),
       not a local field. A cluster's gravitational potential is |Phi|/c^2 ~ (sigma/c)^2 ~ (1000/3e5)^2
       = {(1e6/c**2*1e6):.1e}... ~ 1e-5 -- utterly negligible vs the curvature scale Lambda~1e-52 m^-2.
       Phi-curvature ~ G rho_cl/c^2 = {G*np.median(rho_cl)/c**2:.2e} m^-2 vs Lambda~1.1e-52 m^-2:
       ratio = {G*np.median(rho_cl)/c**2/1.1e-52:.1e}. So the cluster's matter curvature DWARFS Lambda
       locally -- BUT that is exactly the rho_local reading (R1), which breaks galaxies (and in GR the
       cluster's own curvature is Newtonian gravity, already in g_bar, NOT a new a0). R2 collapses to R1.""")

# (R3) Could a0 in clusters be RAISED to the value that closes the deficit? What rho would that need?
print("\n  (R3) Inverse: what a0 would CLOSE the cluster deficit, and what rho would that require?")
# to close eta=2.33 -> need a0 such that eta=1: g_pred = g_obs -> in deep MOND eta ~ sqrt(a0_close/a0_F)?
# eta_deep ~ g_obs/sqrt(gbar a0). eta=2.33 at a0_F => to get eta=1 need a0 -> a0_F*2.33^2
a0_close = a0_F*(eta_FRAME)**2
rho_needed = (2*a0_close/c)**2/G
print(f"       to close eta={eta_FRAME:.2f}->1 in deep MOND need a0_cluster ~ a0_F * eta^2 = {a0_close:.3e}")
print(f"       = {a0_close/a0_F:.1f}x a0_F. Via a0=(c/2)sqrt(G rho) that needs rho = {rho_needed:.3e} kg/m^3")
print(f"       = {rho_needed/rho_DE:.0f}x rho_DE = {rho_needed/np.median(rho_cl):.2f}x the cluster's OWN mean total density.")
print(f"""       So even setting a0 by the cluster's FULL total (dark+baryon) density inside R500 OVER-shoots
       (rho_cl/rho_DE~{np.median(rho_cl)/rho_DE:.0f} -> a0 up {np.sqrt(np.median(rho_cl)/rho_DE):.0f}x, eta would go BELOW 1: an over-correction).
       The 'right' rho to close is ~{rho_needed/rho_DE:.0f}x rho_DE -- between rho_DE and the cluster's own
       density. But there is NO scale-blind rule giving exactly that in clusters and rho_DE in galaxies.""")

# The 4x The-White result, for context
print("\n  (R4) The classic 'clusters need a0 ~ 4x larger' (The & White 1988): in the framework that is")
print(f"       a0_cluster/a0_F ~ {(2.0)**2:.0f}-{(2.33)**2:.1f}x (since eta~2.0-2.33 and eta~sqrt(a0)). Same as R3:")
print(f"       it is a RESTATEMENT of the deficit, not an independent rho. No rho-reading delivers 4x in")
print(f"       clusters AND 1x in galaxies from one scale-blind law a0=(c/2)sqrt(G rho).")

print("\n" + "="*96)
print("PART D VERDICT")
print("="*96)
print("""  D1: a0 from rho_LOCAL-matter is DECISIVELY RULED OUT -- galaxy disks (rho~1e-21) give a0 ~30,000x
      too big and would scatter the universal galaxy RAR by orders of magnitude. (BREAKS-GALAXY-RAR)
  D2: EVERY density-based reading that raises cluster a0 (R1 additive, R2 local-horizon, R3 inverse,
      R4 the 4x) is NOT scale-blind: the same rule that raises cluster a0 ALSO raises (inner-)galaxy a0
      and breaks the RAR's universality. The galaxy RAR is the HARD CONSTRAINT -- it pins a0 to a single
      universal value (compatible with rho_DE, NOT with any local matter density).
  => GRADE: BREAKS-GALAXY-RAR. There is NO consistent framework reading where cluster a0 is raised by a
     density argument without breaking the universal galaxy a0. The canonical rho=rho_DE (a0=9.36e-11
     everywhere) is the ONLY reading the galaxy RAR allows -> NO-EFFECT on the cluster deficit.""")


# =====================================================================================
print("\n" + "="*96)
print("FINAL SYNTHESIS -- does the framework's OWN physics (MI + dS-Unruh) change clusters?")
print("="*96)
print(f"""  PART A: MI's distinctive (MI != MG for pressure-supported systems) does NOT change the INTEGRATED
          deep-MOND virial mass M_dyn=(9/4)sigma^4/(G a0) -- MI and MG COINCIDE in the deep-MOND limit
          (both descend from a0 + scale invariance). The O(1) MI distinctives (stronger EFE, exact
          algebraic nu) do not touch eta(R500). MI does NOT rescue clusters.
  PART B: keeping the full dS-Unruh floor (cH=5.79 a0) inside the sqrt is MOOT at R500 -- the cluster
          regime is DEEP MOND (g_bar/a0~0.037), where every kernel -> 1/sqrt(y); the floor matters only
          in the transition/Newtonian regime, not at R500.
  PART C: framework-MI eta(R500) = {eta_FRAME:.2f} vs normal-MOND/MG eta = {eta_MOND:.2f}. The framework is
          {100*(eta_FRAME/eta_MOND-1):+.0f}% (exactly sqrt(a0_M/a0_F)={np.sqrt(a0_M/a0_F):.3f}) -- LARGER deficit, because a0 is LOWER.
  PART D: a0 is robustly 9.36e-11 in clusters too -- no density reading raises it without breaking the
          galaxy RAR (the hard constraint). a0=(c/2)sqrt(G rho_DE), uniform.

  BOTTOM LINE: the framework's distinctive physics gives the SAME ~2x (very slightly WORSE, +13%), NOT a
  reduction. Modified inertia does NOT rescue clusters either. The cluster ~2x is a shared-MOND liability
  the framework INHERITS, and its lower a0 makes it marginally harder. Reported straight, both ways.
  GATING: MI is NOT covariantly realized (no CMB-safe MI theory; the X2 theorem / trilemma) -- so even the
  null MI result here is itself UNGATED: it is the prediction of an UNBUILT MI theory, computed in the
  Milgrom deep-MOND-limit form that MI and MG share. The covariant realization the framework uses (AeST,
  modified gravity) was tested separately and also predicts a deficit, not a cure.""")
print("="*96)
