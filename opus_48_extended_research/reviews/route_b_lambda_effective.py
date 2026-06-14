"""
ROUTE B — lambda_effective. Does a local matter overdensity induce an EFFECTIVE
local Lambda_eff that the a0<->Lambda spine inherits, yielding a shifted a0_local?

FOUNDATION (use THIS):
  a0 = c^2 sqrt(Lambda / 32pi) = (c/2) sqrt(G rho_DE) = cH_Lambda / Z = 9.36e-11
  dS-Unruh modified inertia: T_eff = (hbar/2pi c kB) sqrt(a^2 + (cH)^2)
  the (cH)^2 floor is the de Sitter horizon scale set by Lambda (vacuum).

Three sub-routes:
  (i)   trace/backreaction of local matter on the effective vacuum: does
        rho_matter,local enter Lambda_eff = Lambda + f(rho_local)?
  (ii)  emergent-gravity readings (Padmanabhan equipartition, CKN UV-IR bound,
        Verlinde local entropy) where "Lambda seen locally" includes a local term.
  (iii) the dS -> Schwarzschild-de Sitter transition: SdS has BOTH a BH and a
        cosmological horizon -- does the LOCAL effective Lambda the a0 relation
        sees change in an overdensity?

For each: derive a0_local(rho_local), its SCALE, and test cluster-window vs SPARC.
BOTH WAYS: is Lambda_eff(rho_local) a real derived effect or a CATEGORY ERROR
(Lambda is a vacuum property, rho_matter is not vacuum)? Be ruthless.
"""
import numpy as np
import sympy as sp

# ---------------- physical constants (SI) ----------------
c    = 2.99792458e8       # m/s
G    = 6.674e-11          # m^3/kg/s^2
hbar = 1.0546e-34
kB   = 1.381e-23
Mpc  = 3.0857e22          # m
kpc  = Mpc/1000.0
Msun = 1.989e30
H0   = 2.20e-18           # s^-1  (~67.7 km/s/Mpc)
OmegaL = 0.685
OmegaM = 0.315

# Lambda from OmegaL: Lambda = 3 H0^2 OmegaL / c^2
Lambda = 3*H0**2*OmegaL/c**2
rho_DE = OmegaL * 3*H0**2/(8*np.pi*G)     # dark energy density (kg/m^3)
rho_crit = 3*H0**2/(8*np.pi*G)

# a0 the framework way (pure Lambda)
a0_Lambda = c**2*np.sqrt(Lambda/(32*np.pi))
a0_rhoDE  = (c/2.0)*np.sqrt(G*rho_DE)
print("="*70)
print("FOUNDATION CHECK")
print("="*70)
print(f"Lambda          = {Lambda:.4e} m^-2")
print(f"rho_DE          = {rho_DE:.4e} kg/m^3")
print(f"rho_crit        = {rho_crit:.4e} kg/m^3")
print(f"a0 = c^2 sqrt(L/32pi)   = {a0_Lambda:.4e}")
print(f"a0 = (c/2)sqrt(G rho_DE)= {a0_rhoDE:.4e}")
print(f"(these should both be ~9.36e-11)")
print()

# ============================================================
# The KEY relation we need for ALL routes:
#   a0 ~ sqrt(Lambda_eff)  =>  a0_local/a0 = sqrt(Lambda_eff/Lambda)
# A cluster boost of ~2-25x in a0 needs Lambda_eff/Lambda = 4 - 625.
# SPARC-safe means: in a galaxy DISK, Lambda_eff/Lambda must be ~1 (<few %).
# ============================================================
def boost_from_LambdaRatio(ratio):
    return np.sqrt(ratio)

print("Required Lambda_eff/Lambda for target a0 boosts:")
for b in [1.02, 1.3, 2.0, 5.0, 17.0, 25.0]:
    print(f"  a0 boost {b:5.2f}x  needs Lambda_eff/Lambda = {b**2:8.2f}")
print()

# Reference local densities (matter)
# galaxy DISK local matter density (mid-plane, solar neighborhood-ish to inner disk)
rho_disk = 0.1 * Msun / (kpc/1000.0)**3 *1e-9  # placeholder, recompute properly below
# Proper: solar neighborhood total ~0.1 Msun/pc^3
rho_disk = 0.1*Msun/( (3.0857e16)**3 )   # 0.1 Msun/pc^3 in kg/m^3
# inner-disk / bulge can be 1-10 Msun/pc^3
rho_disk_inner = 1.0*Msun/( (3.0857e16)**3 )
# cluster CORE (~300-450 kpc): eRASS1 R500 mean ~500 rho_crit; core can be higher
rho_cluster_core = 1e3 * rho_crit      # ~1e3 rho_crit near core
rho_cluster_R500 = 500.0 * rho_crit
print("Reference local MATTER densities:")
print(f"  rho_disk (0.1 Msun/pc^3)      = {rho_disk:.4e}  = {rho_disk/rho_DE:.3e} rho_DE  = {rho_disk/rho_crit:.3e} rho_crit")
print(f"  rho_disk_inner (1 Msun/pc^3)  = {rho_disk_inner:.4e}  = {rho_disk_inner/rho_DE:.3e} rho_DE")
print(f"  rho_cluster_core (~1e3 rcrit) = {rho_cluster_core:.4e}  = {rho_cluster_core/rho_DE:.3e} rho_DE")
print(f"  rho_cluster_R500 (500 rcrit)  = {rho_cluster_R500:.4e}  = {rho_cluster_R500/rho_DE:.3e} rho_DE")
print()
print("KEY FACT: rho_disk/rho_DE = %.2e -- galaxy disk matter is ~10^5-10^6 x rho_DE."%(rho_disk/rho_DE))
print("   so ANY scheme where Lambda_eff scales with rho_matter,local LINEARLY")
print("   boosts the DISK ~10^5-10^6x => destroys SPARC. The whole game is whether")
print("   the foundation picks a scheme that does NOT scale with local rho_matter")
print("   in the disk but DOES in the cluster core.")
print()

print("="*70)
print("SUB-ROUTE (i): TRACE / BACKREACTION of local matter on effective vacuum")
print("="*70)
print("""
The Einstein eq with Lambda:  G_mu_nu + Lambda g_mu_nu = (8piG/c^4) T_mu_nu.
'Effective Lambda' readings move matter to the LHS:
   Lambda_eff = Lambda - (8piG/c^4) * (something built from T).
The trace T = T^mu_mu = -rho c^2 + 3p (signature -+++; dust p=0 => T = -rho c^2).
A scalar 'effective vacuum shift' from the trace would read:
   delta_Lambda ~ (8piG/c^4) * |T|/4 ~ (8piG/c^4)*(rho c^2)/4 = 2piG rho / c^2.
Compare to Lambda = 8piG rho_DE/c^2 (since rho_DE = Lambda c^2/8piG):
   delta_Lambda / Lambda = (2piG rho/c^2)/(8piG rho_DE/c^2) = rho/(4 rho_DE).
""")
# So Lambda_eff/Lambda = 1 + rho_matter/(4 rho_DE)  (LINEAR in local matter density)
for name,rho in [("disk 0.1Msun/pc^3",rho_disk),
                 ("disk_inner 1Msun/pc^3",rho_disk_inner),
                 ("cluster core ~1e3 rcrit",rho_cluster_core),
                 ("cluster R500 ~500 rcrit",rho_cluster_R500)]:
    ratio = 1.0 + rho/(4*rho_DE)
    boost = np.sqrt(ratio)
    print(f"  {name:28s}: Lambda_eff/Lambda = {ratio:.4e}  -> a0 boost = {boost:.4e}")
print("""
VERDICT (i): the trace-backreaction Lambda_eff is LINEAR in rho_matter,local.
  => disk gets Lambda_eff/Lambda ~ 3e5 (a0 boost ~500x) -- ANNIHILATES SPARC.
  => and it boosts the DISK MORE than the cluster core (disk denser).
  This is the LOCAL/CLUMPY reading already proven dead (d log a0/d log(1+delta)
  = +0.5 predicted vs +0.052 measured, 10.5 sigma). WRONG SIGN for the goal
  (boosts dense GALAXY centers more than diffuse cluster cores) AND wrong scale.
  It is ALSO a CATEGORY ERROR: moving T to the LHS does NOT make a new VACUUM
  term -- it is just rewriting matter gravity. Lambda is a property of the
  vacuum (constant, Lorentz-invariant p=-rho); T_matter (dust, p=0) is NOT
  Lorentz-invariant, so it cannot masquerade as a cosmological constant. DEAD.
""")

print("="*70)
print("SUB-ROUTE (iii): Schwarzschild-de Sitter (SdS) -- the SERIOUS route")
print("="*70)
print("""
SdS is the EXACT vacuum solution for a point mass M in a Lambda-vacuum:
   f(r) = 1 - 2GM/(c^2 r) - (Lambda/3) r^2.
It has TWO horizons: a black-hole horizon r_b and a cosmological horizon r_c,
roots of f(r)=0. The dS-Unruh / a0<->Lambda spine reads a0 off the COSMOLOGICAL
horizon (the de Sitter floor). QUESTION: in SdS, does the cosmological horizon
move in a way that the a0 relation would read as a SHIFTED effective Lambda?
""")
r, GM, Lam = sp.symbols('r GM Lambda', positive=True)
M_, c_ = sp.symbols('M c', positive=True)
# f(r) = 1 - 2GM/(c^2 r) - Lambda/3 r^2 ; write mu = 2GM/c^2
mu = sp.symbols('mu', positive=True)  # = 2GM/c^2
f = 1 - mu/r - Lam/3*r**2
print("f(r) =", f)
# The cosmological horizon: largest positive root.
# Exact cubic: (Lam/3) r^3 - r + mu = 0  (multiply f=0 by -r)
cubic = sp.expand(-r*f)
print("cubic (=0):", cubic, "  i.e. (Lam/3) r^3 - r + mu = 0")
print()
print("--- Perturbative shift of the cosmological horizon for small mu ---")
# r_c = r_c0 + delta, r_c0 = sqrt(3/Lam). Solve to first order in mu.
rc0 = sp.sqrt(3/Lam)
delta = sp.symbols('delta')
expr = (Lam/3)*(rc0+delta)**3 - (rc0+delta) + mu
expr_lin = sp.series(expr, delta, 0, 2).removeO()
sol_delta = sp.solve(sp.Eq(expr_lin,0), delta)[0]
sol_delta = sp.simplify(sol_delta)
print("delta r_c (first order in mu) =", sol_delta)
# The 'effective Lambda' the cosmological horizon implies: Lambda_eff = 3/r_c^2
rc = rc0 + sol_delta
Lam_eff = sp.simplify(3/rc**2)
Lam_eff_series = sp.series(Lam_eff, mu, 0, 2).removeO()
print("Lambda_eff = 3/r_c^2  (to O(mu)) =", sp.simplify(Lam_eff_series))
ratio = sp.simplify(Lam_eff_series/Lam)
ratio_series = sp.series(ratio, mu, 0, 2).removeO()
print("Lambda_eff/Lambda (to O(mu)) =", sp.simplify(ratio_series))
print()
print("So the cosmological horizon shrinks with enclosed mass M, and the")
print("'effective Lambda read off the cosmological horizon' = 3/r_c^2 INCREASES.")
print("delta(Lambda_eff)/Lambda = + mu * sqrt(Lam/3) + ... = (2GM/c^2)/r_c0  (positive!)")
print("This has the RIGHT SIGN (mass -> larger effective Lambda -> larger a0).")

print()
print("--- SdS MAGNITUDE: is the cosmological-horizon shift LOCAL or GLOBAL? ---")
r_c0 = c/(H0*np.sqrt(OmegaL))    # de Sitter horizon radius = sqrt(3/Lambda)
print(f"r_c0 = sqrt(3/Lambda) = {r_c0/Mpc:.1f} Mpc  (the cosmological horizon, Gpc)")
print()
print("Lambda_eff/Lambda = 1 + (2GM/c^2)/r_c0, M = total enclosed mass.")
print("The gravitational radius r_g=2GM/c^2 of various masses vs r_c0=4400 Mpc:")
for name,M in [("galaxy 1e11 Msun", 1e11*Msun),
               ("galaxy 1e12 Msun", 1e12*Msun),
               ("group 1e13 Msun", 1e13*Msun),
               ("cluster 1e14 Msun", 1e14*Msun),
               ("cluster 1e15 Msun", 1e15*Msun)]:
    rg = 2*G*M/c**2
    ratio = 1.0 + rg/r_c0
    boost = np.sqrt(ratio)
    print(f"  {name:20s}: r_g={rg/Mpc:.3e} Mpc, Lambda_eff/Lambda={ratio:.6e}, a0 boost={boost:.6e}")
print("""
FATAL: the SdS shift Lambda_eff/Lambda - 1 = (2GM/c^2)/r_c0 is TINY because
r_c0 ~ 4400 Mpc is in the DENOMINATOR. Even a 1e15 Msun cluster:
  2GM/c^2 = 0.096 Mpc, divided by 4400 Mpc = 2.2e-5 => a0 boost ~ 1.00001.
This is utterly negligible (10^-5), and SCALES WITH TOTAL MASS not local density,
so it boosts massive CLUSTERS slightly more than galaxies -- right sign! -- but
the magnitude is ~10^4-10^5 too small to matter (need 2-25x, get 1.00001x).

WHY: in SdS the 'effective Lambda from the cosmological horizon' is set by the
ratio (grav radius of enclosed mass)/(Hubble radius). That ratio is ~10^-5 even
for the biggest clusters. The cosmological horizon barely notices a cluster.
""")

print()
print("="*70)
print("SUB-ROUTE (ii): EMERGENT-GRAVITY local-Lambda readings")
print("="*70)
print("""
(ii-a) CKN / holographic-DE UV-IR bound:  rho_Lambda ~ Mp^2 / L^2  (L = IR cutoff).
Equivalently Lambda_eff ~ 1/L^2 (up to O(1)). The framework's a0<->Lambda lock
USES this: a0 ~ c^2 sqrt(Lambda_eff) ~ c^2 / L. With L = c/H_Lambda (the dS event
horizon), a0 = c H_Lambda / Z = 9.36e-11. The DERIVATION QUESTION: in an
overdensity, what IR cutoff L does the foundation pick, and does it shrink?
""")
# rho_Lambda ~ Mp^2/L^2 with L the IR cutoff. Lambda_eff/Lambda = (L_cosmo/L_local)^2.
# a0_local/a0 = sqrt(Lambda_eff/Lambda) = L_cosmo/L_local.
# So a0_local/a0 = (c/H_Lambda) / L_local. The boost is the ratio of IR scales!
L_cosmo = c/(H0*np.sqrt(OmegaL))   # the dS event horizon ~ r_c0
print(f"L_cosmo (dS event horizon) = {L_cosmo/Mpc:.0f} Mpc")
print("a0_local/a0 = L_cosmo / L_local.  For a boost 2-25x need L_local = L_cosmo/(2..25):")
for b in [1.3, 2.0, 5.0, 17.0, 25.0]:
    print(f"  a0 boost {b:5.1f}x needs L_local = {L_cosmo/b/Mpc:8.1f} Mpc")
print("""
So under CKN, the cluster boost needs the LOCAL IR cutoff to be ~200-4000 Mpc
(L_cosmo/25 .. L_cosmo/1.3). That is STILL Gpc-ish -- NOT the cluster core.
And here is the DERIVATION test: what sets L_local in an overdensity?
""")
print("Candidate IR cutoffs L_local in a region of total density rho_total:")
print(" (A) local apparent/Hubble horizon L = c/H_local, H_local^2 = 8piG/3 rho_total:")
for name,rho in [("disk (1e6 rho_DE)", rho_disk),
                 ("cluster core (1460 rho_DE)", rho_cluster_core),
                 ("cluster R500 (730 rho_DE)", rho_cluster_R500),
                 ("cosmic rho_crit", rho_crit)]:
    H_loc = np.sqrt(8*np.pi*G/3*rho)
    L_loc = c/H_loc
    boost = L_cosmo/L_loc
    print(f"    {name:26s}: H_local gives L={L_loc/Mpc:.3e} Mpc, a0 boost={boost:.4e}")
print("""
  --> This is EXACTLY the banked ELL_DESITTER horizon null re-derived from the
      CKN side: L = c/H_local. For the DISK, rho ~1e6 rho_DE so H_local is huge,
      L tiny (~5 Mpc), boost ~1000x -- DESTROYS SPARC. For clusters L~130-180 Mpc,
      boost ~30x. So the local-Hubble IR cutoff boosts the DENSE DISK MORE than the
      cluster (disk is denser) -- WRONG SIGN again, and breaks SPARC. SAME failure
      as banked ELL_DESITTER but now seen as the CKN cutoff. The mean-vs-local
      smoothing issue is the SAME ell problem -- not escaped by relabeling.
""")

print()
print(" (B) CKN with L = the SYSTEM SIZE itself (the literal HDE IR cutoff):")
print("     a0_local/a0 = L_cosmo / L_system.")
for name,Lsys in [("galaxy disk ~15 kpc", 15*kpc),
                  ("galaxy halo ~275 kpc", 275*kpc),
                  ("cluster core ~400 kpc", 400*kpc),
                  ("cluster R500 ~0.8 Mpc", 0.8*Mpc),
                  ("cluster virial ~2 Mpc", 2.0*Mpc)]:
    boost = L_cosmo/Lsys
    print(f"    {name:24s}: L_sys={Lsys/Mpc:.4f} Mpc, a0 boost = {boost:.3e}")
print("""
  --> CATASTROPHIC and WRONG SIGN: L=system size makes a0 ~ 1/L_system, so the
      SMALLER galaxy (15 kpc) gets a0 boost ~360,000x while the cluster (0.4 Mpc)
      gets ~13,000x. Galaxies boosted MORE than clusters (smaller => bigger boost),
      and both absurdly large (10^4-10^5). The system-size IR cutoff is the OPPOSITE
      of what's needed and breaks everything. (This is the holographic-DE-with-
      system-size reading; it fails by orders of magnitude and the wrong sign.)

(ii-b) Padmanabhan equipartition + Verlinde local entropy:
  Padmanabhan's holographic equipartition gives a0 ~ cH at the HUBBLE radius
  (N_bulk = N_surf), a GLOBAL/cosmological balance -- it produces a0~cH0, NOT a
  local-density-dependent a0. Verlinde 2017's local entropy DISPLACEMENT is the
  emergent-DM mechanism, NOT an effective-Lambda shift; its dark-mass scale is
  M_D ~ sqrt(M a0 r^2/(G)) (the apparent dark mass), which is the MOND response
  at FIXED a0, not a shifted Lambda. Neither makes Lambda_eff(rho_local).
""")

print()
print("="*70)
print("THE CATEGORY QUESTION (ruthless, both ways): is Lambda_eff(rho_matter) real?")
print("="*70)
print("""
SdS Kretschmann / Ricci structure (sympy): the cosmological constant enters the
EINSTEIN tensor as a LORENTZ-INVARIANT term G_mu_nu = -Lambda g_mu_nu (vacuum,
p=-rho, equation of state w=-1). Local matter (dust) has w=0: T = diag(rho,0,0,0)
in its rest frame -- it is NOT Lorentz-invariant, it picks out a rest frame.
""")
# Ricci scalar of SdS: R = 4 Lambda (matter-free regions). The Schwarzschild part
# is Ricci-FLAT (vacuum). So the LOCAL Ricci scalar in a region with both is set by
# Lambda alone wherever T=0, and by rho where matter is present.
t,r_,th,ph = sp.symbols('t r theta phi')
M_s, c_s, Lam_s, G_s = sp.symbols('M c Lambda G', positive=True)
fr = 1 - 2*G_s*M_s/(c_s**2*r_) - Lam_s/3*r_**2
g = sp.diag(-fr*c_s**2, 1/fr, r_**2, r_**2*sp.sin(th)**2)
ginv = g.inv()
# Ricci scalar via Christoffel (compact)
coords = [t,r_,th,ph]
n=4
Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for cc in range(n):
            s=0
            for d in range(n):
                s+= ginv[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d]))
            Gamma[a][b][cc]=sp.simplify(s/2)
def Ricci(i,j):
    s=0
    for a in range(n):
        s+= sp.diff(Gamma[a][i][j],coords[a]) - sp.diff(Gamma[a][i][a],coords[j])
        for b in range(n):
            s+= Gamma[a][a][b]*Gamma[b][i][j] - Gamma[a][j][b]*Gamma[b][i][a]
    return sp.simplify(s)
Rs=0
for i in range(n):
    for j in range(n):
        Rs+= ginv[i,j]*Ricci(i,j)
Rs=sp.simplify(Rs)
print("Ricci scalar R of SdS (vacuum region) =", Rs, "  (expect 4*Lambda*c^2 or 4*Lambda)")
print("""
RESULT: in the VACUUM (matter-free) region the Ricci scalar is R = 4 Lambda*c^2
EVERYWHERE -- it does NOT pick up the mass M (Schwarzschild is Ricci-flat). So the
'local Lambda read off the curvature' in the space AROUND a mass is STILL the
background Lambda, unchanged. The mass only adds a Ricci-FLAT (Weyl/tidal) piece.

=> THE CATEGORY ANSWER: a local matter overdensity does NOT shift the local
   effective Lambda that the a0<->Lambda relation reads. Lambda is the w=-1
   vacuum trace; matter (w=0) contributes to the Weyl/tidal sector and the
   matter Einstein source, NOT to the vacuum Lambda term. Reading a0 off the
   local curvature gives R=4Lambda (background) in the vacuum around the cluster,
   and the matter source where matter sits -- but that matter source is just
   ordinary gravity g_bar, already in the a0 formula's g_bar argument, NOT a
   shifted a0. Double-counting matter as 'extra Lambda' is the category error.
""")
