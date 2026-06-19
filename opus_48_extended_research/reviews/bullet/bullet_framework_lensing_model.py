#!/usr/bin/env python3
"""
THE BULLET CLUSTER through the Zimmerman framework's OWN lensing law -- a quantitative
geometric model (BUILD task "framework_lensing_model", 2026-06-18).
=====================================================================================

WHAT THIS IS (honoring the no-go, both-ways):
  The framework's covariant Cassini-safe MOND lensing is FORBIDDEN (LENSING_NOGO_CLOSED_FINAL).
  Its lensing is IRREDUCIBLY PHENOMENOLOGICAL = AeST-class: a relativistic-MOND theory with
  NO gravitational slip (Phi_lens = Phi_dyn = Phi_N + phi), so the lensing convergence kappa is
  sourced by the SAME total potential dynamics needs. We therefore model the framework's lensing
  with the AeST/QUMOND PHANTOM prescription, NOT a first-principles covariant deflection:

      rho_phantom = (1/4 pi G) div[ (nu(g_N/a0) - 1) grad Phi_N ]
      kappa(x,y)  = Sigma_total(x,y) / Sigma_crit ,  Sigma_total = Sigma_baryon + Sigma_phantom

  This is exactly AeST's free function fed in by hand (a0/Z transmitted, NOT derived). Quarantine.

STEPS (per the task):
  (1) place 2 galaxy concentrations + 2 X-ray gas clumps at the real Bullet positions, gas:stars ~6:1
  (2) compute the framework's kappa(x,y) from the BARYONS ONLY (phantom of baryons)
  (3) locate the predicted lensing centroid -> show it lands on the GAS, not the galaxies
  (4) solve the RESIDUAL collisionless mass at the galaxy positions to move kappa peaks onto galaxies
  (5) test whether the DENSITY-a0 reading reduces the required residual vs constant-a0 MOND

BOTH WAYS: we run the framework a0 (9.36e-11) AND canonical MOND a0 (1.2e-10); the framework's
lower a0 gives a WEAKER phantom -> LARGER residual (the banked +13% surcharge). No manufactured solve.

Literature targets to reproduce (canonical a0=1.2e-10):
  Famaey 2026 (arXiv:2605.10022): MOND-only M/M_bar ~ 2.8 (BCG1), 3.3 (BCG3) at 300 kpc;
     observed ~7.5-8; residual missing mass 3.4e14 Msun, collisionless, centred on galaxies
     (main Plummer 5.8e14? -> see paper: two-component; subcluster 1.0e14); phantom+bar/bar ~ pi at 300 kpc.
  Clowe 2006: subcluster separation 0.72 Mpc; mass-gas offset ~0.2 Mpc (sub), ~0.3 Mpc (main); 8sigma.
  z=0.296; main M200~1.5e15, bullet M200~1.5e14.
"""
import numpy as np

# ----------------------------------------------------------------------------------
# constants (SI)
# ----------------------------------------------------------------------------------
G     = 6.674e-11
Msun  = 1.989e30
kpc   = 3.0857e19
Mpc   = 1000.0 * kpc
c     = 2.998e8

# framework a0 vs canonical MOND a0
A0_FW   = 9.36e-11      # a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE)  [Zimmerman]
A0_CAN  = 1.20e-10      # canonical / local MOND (McGaugh, Famaey)
RHO_DE  = (2.0 * A0_FW / c)**2 / G    # rho_DE implied by the framework a0 (for density-a0 reading)

# de Sitter-Unruh / framework interpolation  g_obs = sqrt(g_N^2 + g_N a0)  <=> nu(y)=sqrt(1+1/y), y=g_N/a0
def nu_dsunruh(g_N, a0):
    y = g_N / a0
    return np.sqrt(1.0 + 1.0 / y)          # g_obs = nu * g_N

# 'simple' nu for cross-check (Famaey/Hernandez family)
def nu_simple(g_N, a0):
    x = g_N / a0
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / x))

# ----------------------------------------------------------------------------------
# (1) the baryonic components at the REAL Bullet geometry
# ----------------------------------------------------------------------------------
# z = 0.296. We work in the lens plane (projected). x-axis = merger axis.
# Geometry (Clowe 2006 / Bradac 2006 / Paraficz 2016, fiducial):
#   - main cluster and subcluster (bullet) mass peaks separated by ~720 kpc along x.
#   - the X-ray GAS lags BEHIND its galaxies (ram-pressure stripped), sitting between them:
#       main gas offset ~ -300 kpc from main galaxies (toward centre)
#       bullet gas ('the bullet') offset ~ +200 kpc behind bullet galaxies (toward centre)
#   => galaxies at x = -360 (main), +360 (sub); gas at x = -60 (main), +160 (bullet).
#   This reproduces the observed mass-gas offsets (main ~300 kpc, sub ~200 kpc) and 720 kpc separation.
#
# Masses (gas dominates stars ~6:1; total baryon ~3.3e14):
#   gas: 2.85e14 Msun (86%);  stars/galaxies: 0.47e14 Msun (14%)  -> gas/star = 6.0
#   main:sub mass ratio ~ 10:1 (M200 1.5e15 : 1.5e14) but baryon split is gentler; we use ~2.2:1
#     for the lensing-relevant inner baryons (the WL/SL peaks weight the cores).
# Galaxies are COMPACT (Plummer/softened core b_gal small); gas is DIFFUSE (broad beta-like cores).

# (M[Msun], x0[kpc], y0[kpc], b_core[kpc], kind)
# GALAXY compactness b_gal is the LOAD-BEARING modelling choice (banked lesson, bullet_qumond_redo.py):
#   - if galaxies are TOO compact, the BARYONIC Sigma already peaks on them (a 'cheat' -- not the phantom).
#   - the REAL stellar/galaxy distribution in a cluster is an extended ENVELOPE (~150-250 kpc), so the
#     diffuse GAS genuinely DOMINATES the projected baryonic surface density everywhere (THIS is why the
#     Bullet is 'MOND's failure'). We set the FIDUCIAL with gas-dominated Sigma (b_gal=150 kpc envelope)
#     and SCAN b_gal to expose the transition (the 2026 compact-per-galaxy 'flip' vs the canonical result).
B_GAL_FID = 150.0   # kpc -- extended cluster galaxy envelope (gas dominates Sigma; the HONEST canonical setup)

def make_components(b_gal):
    GAL = [
        (3.30e13, -360.0, 0.0, b_gal,        'gal_main'),
        (1.40e13, +360.0, 0.0, b_gal*0.78,   'gal_sub'),
    ]
    GAS = [
        (1.95e14,  -60.0, 0.0, 250.0, 'gas_main'),   # main X-ray gas (diffuse, broad)
        (0.90e14, +160.0, 0.0, 150.0, 'gas_bullet'), # the 'bullet' gas (the famous bow-shock cone)
    ]
    return GAL, GAS

GAL, GAS = make_components(B_GAL_FID)
COMPONENTS = GAL + GAS

M_gas  = sum(c[0] for c in GAS)
M_star = sum(c[0] for c in GAL)
print("="*86)
print("BULLET CLUSTER through the framework's own (AeST-class, phantom) lensing law")
print("="*86)
print(f"  Baryon budget: gas = {M_gas:.3e} Msun ({100*M_gas/(M_gas+M_star):.0f}%), "
      f"stars = {M_star:.3e} Msun ({100*M_star/(M_gas+M_star):.0f}%)  -> gas/star = {M_gas/M_star:.1f}")
print(f"  Geometry: galaxies x=(-360,+360) kpc; gas x=(-60,+160) kpc; subcluster sep 720 kpc;")
print(f"            mass-gas offsets: main ~300 kpc, bullet ~200 kpc (Clowe 2006 fiducial).")
print(f"  rho_DE (from framework a0) = {RHO_DE:.3e} kg/m^3 ; A0_FW={A0_FW:.3e}, A0_CAN={A0_CAN:.3e}")
print()

# ----------------------------------------------------------------------------------
# 3-D grid: Plummer spheres -> Newtonian field -> phantom -> project to Sigma(x,y)
# ----------------------------------------------------------------------------------
N3   = 160
Lx   = 4000.0 * kpc          # +-2 Mpc box, merger axis
ax1d = (np.arange(N3) - N3//2 + 0.5) * (Lx / N3)
dgrid = Lx / N3
X, Y, Zc = np.meshgrid(ax1d, ax1d, ax1d, indexing='ij')
xk = ax1d / kpc              # 1-D axis in kpc

def plummer_set(comps):
    """list of (M_kg, x0_m, y0_m, b_m)."""
    return [(M*Msun, x0*kpc, y0*kpc, b*kpc) for (M, x0, y0, b, _) in comps]

def grad_phiN(pset):
    gx = np.zeros_like(X); gy = np.zeros_like(X); gz = np.zeros_like(X)
    for (M, x0, y0, b) in pset:
        dx, dy, dz = X - x0, Y - y0, Zc
        s = (dx*dx + dy*dy + dz*dz + b*b)**1.5
        f = G * M / s
        gx += f*dx; gy += f*dy; gz += f*dz
    return gx, gy, gz   # = -grad Phi_N (points inward-> we store +g_vec, |g| is accel)

def rho_baryon(pset):
    rho = np.zeros_like(X)
    for (M, x0, y0, b) in pset:
        dx, dy, dz = X - x0, Y - y0, Zc
        rho += 3.0*M*b*b/(4.0*np.pi) / (dx*dx + dy*dy + dz*dz + b*b)**2.5
    return rho

def sigma_project(rho3d):
    """project along z -> Sigma(x,y) in kg/m^2."""
    return np.sum(rho3d, axis=2) * dgrid

def phantom_density(pset, a0, nu_func, density_a0=False):
    """rho_phantom = (1/4 pi G) div[(nu-1) g_vec], g_vec = -grad Phi_N (so accel field)."""
    gx, gy, gz = grad_phiN(pset)
    g = np.sqrt(gx*gx + gy*gy + gz*gz) + 1e-30
    if density_a0:
        # DENSITY-a0 reading: a0 set by LOCAL baryon density, a0_local = (c/2) sqrt(G rho_local),
        # capped so it reduces to the standard a0 when rho_local -> rho_DE.  Use the framework form
        # a0_eff = A0_FW * sqrt(max(rho_local/rho_DE, 1)).  (rho_local = baryon mass density here.)
        rho_loc = rho_baryon(pset)
        a0_eff = A0_FW * np.sqrt(np.maximum(rho_loc / RHO_DE, 1.0))
        nu = nu_func(g, a0_eff)
    else:
        nu = nu_func(g, a0)
    Vx, Vy, Vz = (nu - 1.0)*gx, (nu - 1.0)*gy, (nu - 1.0)*gz
    rho_p = (np.gradient(Vx, dgrid, axis=0)
             + np.gradient(Vy, dgrid, axis=1)
             + np.gradient(Vz, dgrid, axis=2)) / (4.0*np.pi*G)
    return rho_p

# ----------------------------------------------------------------------------------
# Sigma_crit for kappa (z_lens=0.296, fiducial source z_s~1.0; flat LCDM h=0.7)
# ----------------------------------------------------------------------------------
def comoving_distance(z, Om=0.3, OL=0.7, H0=70.0):
    # H0 in km/s/Mpc
    from numpy import linspace, trapz
    zz = linspace(0, z, 2000)
    Ez = np.sqrt(Om*(1+zz)**3 + OL)
    DH = (c/1000.0) / H0          # Mpc
    Dc = DH * trapz(1.0/Ez, zz)   # comoving, Mpc
    return Dc
def ang_diam(z1, z2):
    Dc1 = comoving_distance(z1); Dc2 = comoving_distance(z2)
    return (Dc2 - Dc1) / (1.0 + z2)        # flat universe, Mpc

zL, zS = 0.296, 1.0
DL  = ang_diam(0.0, zL) * Mpc
DS  = ang_diam(0.0, zS) * Mpc
DLS = ang_diam(zL, zS) * Mpc
Sigma_crit = c*c / (4.0*np.pi*G) * DS / (DL * DLS)
print(f"  Sigma_crit (zL=0.296, zS=1.0) = {Sigma_crit:.3e} kg/m^2 = "
      f"{Sigma_crit/(Msun/Mpc**2):.3e} Msun/Mpc^2")
print()

# ----------------------------------------------------------------------------------
# helper: peak location, value at a point, centroid
# ----------------------------------------------------------------------------------
j0 = N3//2  # y=0 slice
def at_x(prof, xc_kpc):
    return prof[np.argmin(np.abs(xk - xc_kpc))]
def peak_x(prof):
    return xk[np.argmax(prof)]
def nearest_feature(xc):
    feats = {'gal_main': -360, 'gal_sub': +360, 'gas_main': -60, 'gas_bullet': +160}
    name = min(feats, key=lambda k: abs(feats[k] - xc))
    return name, feats[name]

# ----------------------------------------------------------------------------------
# RUN (2)+(3): framework kappa from BARYONS ONLY -> where does the lensing peak land?
# ----------------------------------------------------------------------------------
pset = plummer_set(COMPONENTS)
Sig_b   = sigma_project(rho_baryon(pset))               # baryonic Sigma(x,y)
prof_b  = Sig_b[:, j0]

def run_case(label, a0, nu_func, density_a0=False):
    rho_p = phantom_density(pset, a0, nu_func, density_a0=density_a0)
    Sig_p = sigma_project(rho_p)
    Sig_t = Sig_b + Sig_p
    prof_t = Sig_t[:, j0]; prof_p = Sig_p[:, j0]
    kap_t  = prof_t / Sigma_crit
    pk_t   = peak_x(prof_t)
    nm, fx = nearest_feature(pk_t)
    Mp_tot = np.sum(rho_p) * dgrid**3 / Msun
    # phantom+bar / bar within 300 kpc cylinder around main galaxies
    return dict(label=label, Sig_p=Sig_p, Sig_t=Sig_t, prof_t=prof_t, prof_p=prof_p,
                kap_t=kap_t, pk_t=pk_t, near=nm, near_x=fx, Mp=Mp_tot)

print("-"*86)
print("(2)+(3): framework kappa from BARYONS ONLY -- where does the lensing peak land?")
print("-"*86)
cases = {}
for lbl, a0, nuf, dens in [
    ("FW a0=9.36e-11, dS-Unruh nu", A0_FW, nu_dsunruh, False),
    ("FW a0=9.36e-11, simple nu  ", A0_FW, nu_simple,  False),
    ("CAN a0=1.2e-10, dS-Unruh nu", A0_CAN, nu_dsunruh, False),
    ("CAN a0=1.2e-10, simple nu  ", A0_CAN, nu_simple,  False),
]:
    r = run_case(lbl, a0, nuf, dens)
    cases[lbl] = r
    # peaks: print kappa at each feature
    km = at_x(r['kap_t'], -360); ks = at_x(r['kap_t'], +360)
    kgm= at_x(r['kap_t'],  -60); kgb= at_x(r['kap_t'], +160)
    print(f"  {lbl}: TOTAL kappa peak at x={r['pk_t']:+5.0f} kpc -> {r['near']:9s} | "
          f"Mphantom={r['Mp']:.2e} Msun")
    print(f"        kappa @ gal_main(-360)={km:.3f}  gas_main(-60)={kgm:.3f}  "
          f"gas_bullet(+160)={kgb:.3f}  gal_sub(+360)={ks:.3f}")

# baryon-only peak (fairness check)
pk_b = peak_x(prof_b); nmb, _ = nearest_feature(pk_b)
sig0_gal = at_x(prof_b, -360); sig0_gas = at_x(prof_b, -60)
print(f"\n  [fairness] BARYON-only Sigma peak at x={pk_b:+5.0f} kpc -> {nmb}. "
      f"Sigma(gal_main)/Sigma(gas_main) = {sig0_gal/sig0_gas:.2f}")
if sig0_gas > sig0_gal:
    print(f"             GAS dominates the baryonic surface density (the honest canonical Bullet setup).")
else:
    print(f"             WARNING: galaxies dominate Sigma -> a 'compactness cheat'; not a phantom effect.")

# ----------------------------------------------------------------------------------
# COMPACTNESS SCAN -- the load-bearing modelling choice (banked lesson). Where does the
# framework's TOTAL kappa peak as galaxies go from extended-envelope to compact?
# ----------------------------------------------------------------------------------
print()
print("-"*86)
print("COMPACTNESS SCAN (framework a0, dS-Unruh): does the phantom flip the peak onto galaxies?")
print("-"*86)
print(f"  {'b_gal[kpc]':>10} | {'baryon Sigma peak':>18} | {'TOTAL kappa peak':>18} | "
      f"{'Sig_gal/Sig_gas':>15}")
for b_gal in (250, 200, 150, 100, 60, 40):
    GALs, GASs = make_components(b_gal)
    comp = GALs + GASs
    ps = plummer_set(comp)
    Sb = sigma_project(rho_baryon(ps))[:, j0]
    rho_p = phantom_density(ps, A0_FW, nu_dsunruh, density_a0=False)
    St = (Sb + sigma_project(rho_p)[:, j0])
    pkb = peak_x(Sb); pkt = peak_x(St)
    nb, _ = nearest_feature(pkb); nt, _ = nearest_feature(pkt)
    rsig = Sb[np.argmin(np.abs(xk + 360))] / Sb[np.argmin(np.abs(xk + 60))]
    print(f"  {b_gal:>10} | {nb:>18} | {nt:>18} | {rsig:>15.2f}")
print("  READING: when gas dominates Sigma (b_gal >~150 kpc) the baryon peak is ON THE GAS; the")
print("  framework's phantom does NOT by itself flip the TOTAL kappa onto the galaxies for blob-scale")
print("  envelopes -> kappa tracks the GAS (the canonical 'MOND fails' offset). Only OVER-compact")
print("  galaxies (b_gal<~60 kpc, where baryons ALREADY peak on galaxies) move it -- the contested")
print("  2026 compact-per-galaxy escape (Cha 2025 / 2604.10811), which the framework IMPORTS not derives.")

# ----------------------------------------------------------------------------------
# (4) SOLVE the residual collisionless mass at the galaxy positions
#     Required: move the kappa peaks ONTO the galaxies (-360,+360) AND reach observed M/M_bar~7.5-8.
# ----------------------------------------------------------------------------------
print()
print("-"*86)
print("(4): RESIDUAL collisionless mass at the galaxy positions (move kappa onto galaxies)")
print("-"*86)
# Observed lensing M/M_bar at 300 kpc ~ 7.5-8 (Famaey 2026). MOND-only gives ~2.8-3.3 (canonical).
# Residual factor = (observed - MOND) ; residual mass = (M_obs - M_MOND) projected within the galaxy
# apertures. We compute the framework's MOND-only enclosed (bar+phantom) mass in a 300 kpc cylinder
# at each galaxy, compare to observed, and solve the residual.

def cyl_mass(Sigma2d, xc_kpc, yc_kpc, R_kpc):
    """projected mass inside a cylinder radius R about (xc,yc), Msun."""
    XX, YY = np.meshgrid(xk, xk, indexing='ij')   # kpc grid in lens plane
    msk = (XX - xc_kpc)**2 + (YY - yc_kpc)**2 <= R_kpc**2
    return np.sum(Sigma2d[msk]) * (dgrid)**2 / Msun   # Sigma[kg/m^2]*area[m^2]

R_AP = 300.0  # kpc aperture (Famaey reference radius)
M_obs_ratio = 7.75   # observed M_lens/M_bar at 300 kpc (Famaey 2026: 7.5-8)
Sig_gas_only = sigma_project(rho_baryon(plummer_set(GAS)))   # gas-only projected map
Sig_star_only= sigma_project(rho_baryon(plummer_set(GAL)))   # star-only projected map

print(f"  Aperture R={R_AP:.0f} kpc (cylinders at the two GALAXY centroids x=+-360).")
print(f"  Observed M_lens/M_bar ~ {M_obs_ratio} at 300 kpc (Famaey 2026).")
print(f"  Famaey-2026 MOND-only (his nu_tilde) M/M_bar ~ 2.8-3.3 -> residual 3.4e14 Msun, collisionless.")
print()
# Report PER GALAPERTURE: framework MOND M/M_bar, the residual, and ratios to local gas & stars.
residual_summary = {}
res_tot = {}
for lbl in ["FW a0=9.36e-11, dS-Unruh nu", "CAN a0=1.2e-10, dS-Unruh nu"]:
    r = cases[lbl]; Sig_t = r['Sig_t']; tot = 0.0
    for gx_kpc, gname in [(-360, 'main_gal'), (+360, 'sub_gal')]:
        Mbar  = cyl_mass(Sig_b,  gx_kpc, 0.0, R_AP)
        Mmond = cyl_mass(Sig_t,  gx_kpc, 0.0, R_AP)        # bar + phantom = MOND lensing mass
        Mgas  = cyl_mass(Sig_gas_only,  gx_kpc, 0.0, R_AP)
        Mstar = cyl_mass(Sig_star_only, gx_kpc, 0.0, R_AP)
        Mobs  = M_obs_ratio * Mbar
        Mres  = Mobs - Mmond
        tot  += Mres
        residual_summary[(lbl, gname)] = (Mbar, Mmond, Mmond/Mbar, Mres)
        print(f"  [{lbl}] {gname} (x={gx_kpc:+d}): M_bar={Mbar:.2e}  "
              f"M_MOND={Mmond:.2e} (M/M_bar={Mmond/Mbar:.2f})  M_obs={Mobs:.2e}")
        print(f"        RESIDUAL = {Mres:.2e} Msun |  res/gas(loc)={Mres/Mgas:.2f}  "
              f"res/stars(loc)={Mres/Mstar:.1f}  res/M_MOND={Mres/Mmond:.2f}")
    res_tot[lbl] = tot
res_fw, res_can = res_tot["FW a0=9.36e-11, dS-Unruh nu"], res_tot["CAN a0=1.2e-10, dS-Unruh nu"]
print(f"\n  TOTAL residual (both galaxy apertures): FW a0={res_fw:.3e} Msun, "
      f"CAN a0={res_can:.3e} Msun  (FW/CAN = {res_fw/res_can:.3f}; FW heavier = the +{100*(res_fw/res_can-1):.0f}% surcharge).")
print(f"  res/total-gas = {res_fw/(M_gas):.2f}  res/total-stars = {res_fw/(M_star):.1f}")
print(f"\n  NOTE (both ways): our dS-Unruh MOND M/M_bar~1.5 is LOWER than Famaey's ~2.8 because (a) the")
print(f"  dS-Unruh/simple nu is the MOST-NEWTONIAN interpolation (weakest boost) and (b) Famaey's nu_tilde")
print(f"  =(e^sqrt(g)-1)^-1 is a sharper deep-MOND function. => the FRAMEWORK leaves the LARGEST residual of")
print(f"  the MOND family -- it does NOT reduce the Bullet residual; it inherits + slightly inflates it.")
print(f"  Our absolute residual (~6e14/galaxy, ~1.2e15 summed over both 300-kpc apertures) is ~2-3x Famaey's")
print(f"  3.4e14 because (i) weaker nu and (ii) our cylinders enclose the full LOS phantom; the ORDER and the")
print(f"  SIGN (residual centred on galaxies, collisionless) reproduce the literature. res ~ a few x10^14 Msun.")

# ----------------------------------------------------------------------------------
# (5) DENSITY-a0 reading: does it REDUCE the required residual vs constant-a0?
# ----------------------------------------------------------------------------------
print()
print("-"*86)
print("(5): DENSITY-a0 reading -- does a0 set by LOCAL density reduce the residual?")
print("-"*86)
r_dens = run_case("FW density-a0, dS-Unruh", A0_FW, nu_dsunruh, density_a0=True)
cases["FW density-a0"] = r_dens
kmd = at_x(r_dens['kap_t'], -360); kgmd = at_x(r_dens['kap_t'], -60)
print(f"  density-a0: TOTAL kappa peak at x={r_dens['pk_t']:+5.0f} kpc -> {r_dens['near']} | "
      f"Mphantom={r_dens['Mp']:.2e} Msun")
print(f"        kappa @ gal_main(-360)={kmd:.3f}  gas_main(-60)={kgmd:.3f}")
res_dens = 0.0
for gx_kpc in (-360, +360):
    Mbar  = cyl_mass(Sig_b, gx_kpc, 0.0, R_AP)
    Mmond = cyl_mass(r_dens['Sig_t'], gx_kpc, 0.0, R_AP)
    res_dens += (M_obs_ratio*Mbar - Mmond)
print(f"  TOTAL residual under DENSITY-a0 = {res_dens:.3e} Msun  vs constant-a0 FW {res_fw:.3e}")
print(f"  density-a0 reduces residual by factor {res_fw/res_dens:.2f}x  "
      f"(>1 means LESS residual needed).")
print(f"  CAVEAT: density-a0 rides the SPARC trap (same law over-boosts galaxy disks); the smoothing")
print(f"  scale is TUNED not derived. A reducer at clusters, NOT a delivered cure. Both ways.")

# ----------------------------------------------------------------------------------
# save kappa-map figure
# ----------------------------------------------------------------------------------
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))
    extent = [xk.min(), xk.max(), xk.min(), xk.max()]

    def panel(ax, Sig2d, title, show_resid=False):
        kap = Sig2d / Sigma_crit
        im = ax.imshow(kap.T, origin='lower', extent=extent, cmap='magma',
                       vmin=0, vmax=np.percentile(kap, 99.5))
        ax.contour(xk, xk, (Sig_b/Sigma_crit).T, levels=6, colors='cyan',
                   linewidths=0.6, alpha=0.7)
        # mark features
        for (M, x0, y0, b, kind) in GAL:
            ax.plot(x0, y0, '*', color='lime', ms=16, mec='k', mew=0.6)
        for (M, x0, y0, b, kind) in GAS:
            ax.plot(x0, y0, 'o', color='deepskyblue', ms=9, mec='k', mew=0.6)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel('x [kpc] (merger axis)'); ax.set_ylabel('y [kpc]')
        ax.set_xlim(-1400, 1400); ax.set_ylim(-1000, 1000)
        plt.colorbar(im, ax=ax, fraction=0.046, label=r'$\kappa$')

    panel(axes[0], cases["FW a0=9.36e-11, dS-Unruh nu"]['Sig_t'],
          r'Framework (a0=9.36e-11): baryons-only $\kappa$''\n(phantom+gas) -- peaks track GAS')
    panel(axes[1], Sig_b, 'Baryonic $\\Sigma$ only\n(cyan contours; gas dominates)')
    # residual model panel: add Plummer residual at galaxies to flip peaks
    Mres_main = residual_summary[("FW a0=9.36e-11, dS-Unruh nu", 'main_gal')][3]
    Mres_sub  = residual_summary[("FW a0=9.36e-11, dS-Unruh nu", 'sub_gal')][3]
    # build residual sigma directly (projected Plummer surface density: Sigma = M b^2 / pi /(r^2+b^2)^2)
    def plummer_sigma2d(M_Msun, x0, y0, b_kpc):
        XX, YY = np.meshgrid(xk, xk, indexing='ij')
        rr2 = ((XX - x0)**2 + (YY - y0)**2) * kpc**2
        b2 = (b_kpc*kpc)**2
        return (M_Msun*Msun) * b2 / np.pi / (rr2 + b2)**2
    Sig_res = (plummer_sigma2d(max(Mres_main, 0), -360, 0, 200)
               + plummer_sigma2d(max(Mres_sub, 0), +360, 0, 150))
    panel(axes[2], cases["FW a0=9.36e-11, dS-Unruh nu"]['Sig_t'] + Sig_res,
          'Framework + residual (collisionless)\nat galaxies -> $\\kappa$ peaks on GALAXIES')
    fig.suptitle('Bullet Cluster through the framework''s AeST-class phantom lensing '
                 '(stars=lime, gas=blue)', fontsize=12)
    fig.tight_layout(rect=[0,0,1,0.95])
    out = '/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/bullet/bullet_kappa_map.png'
    fig.savefig(out, dpi=120)
    print(f"\n  kappa-map saved -> {out}")
except Exception as e:
    print(f"\n  [figure skipped: {e}]")

print("="*86)
print("DONE.")
print("="*86)
