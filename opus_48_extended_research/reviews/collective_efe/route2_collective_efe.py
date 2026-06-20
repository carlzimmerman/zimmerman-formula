"""
ROUTE 2 -- the COLLECTIVE inter-galaxy EFE field (Carl's "the whole area gets more EFE").

CARL'S IDEA: in a relaxed cluster the member galaxies sit near each other; each
galaxy's long-range 1/r deep-MOND field (g ~ sqrt(G M a0)/r) reaches far out; the
fields OVERLAP in the inter-galaxy medium. Does that overlapping COLLECTIVE field
give the whole region an enhanced acceleration / a region-wide collective EFE that
ADDS cluster binding (extra effective gravitating mass) that the SMOOTH-baryon
cluster-MOND estimate MISSES -- with NO new mass?

THE HONEST PHYSICS, resolved BOTH WAYS by direct QUMOND computation:

  (A) The QUMOND phantom mass is set by the field-line FLUX (Gauss law):
        rho_ph = -(1/4piG) div[(nu-1) grad Phi_N]
      => M_ph(<r) = (1/4piG) oint_S (1-nu) grad Phi_N . dA   (a pure surface integral)
      The TOTAL phantom mass inside any closed surface is a FLUX integral of the
      Newtonian field times (1-nu). For a sphere enclosing the whole cluster the
      enclosed *baryonic* mass is the same whether the baryons are clumpy or smooth
      => the OUTWARD flux of g_N is the same => to the extent nu is the same on the
      bounding surface, M_ph is the same. Clumpiness changes nu LOCALLY (raises g_N
      near galaxies -> nu closer to 1 -> LESS phantom there; lowers g_N in voids ->
      nu bigger -> MORE phantom there). This is the enclosed-mass / sub-additivity
      crux. We COMPUTE it, not assert it.

  (B) The EFE SIGN. The collective inter-galaxy field is an EXTERNAL field on each
      member galaxy. The banked finding: g_ext DECREASES a member's internal boost
      (wrong sign for the members). But the collective field also SOURCES the
      inter-galaxy potential -- a different question. We resolve the sign by direct
      QUMOND on a realistic discrete cluster vs the equal-mass smooth cluster.

  (C) Is the collective inter-galaxy g_ext above or below a0? Eckert/Famaey 2024:
      the cluster's *cosmological* external field is ~0.001-0.002 a0 (deeply
      sub-a0). We compute the collective inter-galaxy field from the members.

METHOD: full discrete QUMOND. Place N member galaxies (realistic luminosity
function + NFW-like spatial distribution) as point/extended deep-MOND sources in
a relaxed cluster + the smooth ICM gas. Solve the Newtonian field on a 3D grid,
apply the framework's OWN interpolation nu(g_N) [from g_obs=sqrt(g_N^2+g_N*a0)],
take the QUMOND divergence to get rho_ph, integrate M_ph(<r). Compare to the
SMOOTH cluster (same total baryon mass, smooth). The DIFFERENCE is Carl's
collective/clumpy effect on the TOTAL gravitating mass.

Framework footing: a0=9.36e-11; nu from g_obs=sqrt(g_N^2+g_N*a0) => nu(y)=g_obs/g_N
with y=g_N/a0:  nu(y) = sqrt(1 + 1/y) = sqrt(1 + a0/g_N).  (the framework's OWN
dS-Unruh interpolation, MEMORY footing rule -- NOT McGaugh's nu).

Quarantine: a0/Z/kappa never asserted derived. Both ways: hunt the collective
enhancement HARD; concede honestly if the flux theorem / sub-additivity kills it.
"""
import numpy as np

# ----------------------------- constants -----------------------------
G    = 6.674e-11          # SI
Msun = 1.989e30           # kg
kpc  = 3.086e19           # m
Mpc  = 1000*kpc
a0   = 9.36e-11           # framework a0 (eta-worst footing)

# framework's OWN dS-Unruh interpolation:  g_obs = sqrt(g_N^2 + g_N a0)
#   => nu(g_N) = g_obs/g_N = sqrt(1 + a0/g_N)
def nu_fw(gN):
    gN = np.asarray(gN, dtype=float)
    out = np.ones_like(gN)
    m = gN > 0
    out[m] = np.sqrt(1.0 + a0/gN[m])
    return out

# =====================================================================
# PART 1 -- the FLUX / enclosed-mass theorem, computed exactly (sub-additivity)
# =====================================================================
# QUMOND:  rho_ph = -(1/4 pi G) div[(nu-1) grad Phi_N]
# grad Phi_N = -g_N (g_N the Newtonian gravitational *acceleration* magnitude,
#   pointing inward).  Gauss:
#   M_bar+ph(<r) = (1/4piG) oint (nu) g_N . dA  (since g_MOND = nu g_N in QUMOND-radial)
#   M_ph(<r)     = (1/4piG) oint (nu-1) g_N . dA
# For a SPHERICAL shell of radius r enclosing baryonic mass M_b(<r):
#   oint g_N . dA = 4 pi G M_b(<r)   (Gauss, exact, clumpy or smooth)
#   => if nu were constant on the shell, M_tot(<r) = nu * M_b(<r) EXACTLY,
#      INDEPENDENT of clumpiness. Clumpiness enters ONLY through the VARIATION
#      of nu over the shell (Jensen / the angular average of nu g_N).

print("="*72)
print("PART 1 -- the QUMOND flux (enclosed-mass) theorem: is the TOTAL")
print("          gravitating mass clumpiness-independent? (sub-additivity)")
print("="*72)

# Two-body deep-MOND sub-additivity demonstration (Carl's sqrt(2M) vs 2 sqrt(M)).
# Field of an isolated deep-MOND point mass M at distance d:  g = sqrt(G M a0)/d.
# Put TWO masses M a distance s apart; evaluate the field far away (d >> s) along
# the symmetry axis. SMOOTH-equivalent = one mass 2M at the centroid.
def g_deepMOND_point(M, d):
    return np.sqrt(G*M*a0)/d

M_gal = 1e11*Msun
d_far = 2.0*Mpc
# collective (one merged source of 2M):
g_merged = g_deepMOND_point(2*M_gal, d_far)
# naive linear sum of two separate deep-MOND fields (what "overlap adds" would give):
g_sumlinear = 2*g_deepMOND_point(M_gal, d_far)
print(f"\nTwo {M_gal/Msun:.0e} Msun galaxies, field at {d_far/Mpc:.1f} Mpc:")
print(f"  merged 2M deep-MOND field   g = {g_merged:.3e}  (= sqrt(2)*single)")
print(f"  LINEAR sum of two fields    g = {g_sumlinear:.3e}  (= 2*single)")
print(f"  ratio merged/linear-sum     = {g_merged/g_sumlinear:.4f}  (= 1/sqrt(2)=0.707)")
print("  => the COLLECTIVE (correctly nonlinear) field is sqrt(2)/2 = 0.707x the")
print("     naive linear sum: deep-MOND is SUB-ADDITIVE. 'Overlap adds field' is")
print("     the linear-superposition fallacy; QUMOND/AQUAL does NOT superpose.")

# =====================================================================
# PART 2 -- full discrete-vs-smooth QUMOND on a realistic relaxed cluster
# =====================================================================
print("\n"+"="*72)
print("PART 2 -- discrete (N member galaxies + ICM) vs smooth QUMOND;")
print("          M_ph(<r) in the core. Does clumpiness ADD net mass?")
print("="*72)

rng = np.random.default_rng(42)

# --- cluster: rich relaxed, M500 = 1e15 Msun, R500 ~ 1.3 Mpc ---
M500   = 1e15*Msun
R500   = 1300.0*kpc
fgas500= 0.12
fstar500=0.015          # stars (galaxies) ~ 1.5% of M500 (typical rich cluster)
Mgas   = fgas500*M500
Mstar  = fstar500*M500   # total in member galaxies

# --- ICM gas: isothermal beta-model, rc=0.2 R500, beta=0.65 ---
rc_gas = 0.20*R500
beta   = 0.65
def rho_gas(r):
    return 1.0/(1+(r/rc_gas)**2)**(1.5*beta)   # un-normalized shape
# normalize to Mgas within R500
rr = np.linspace(1e-3*R500, R500, 6000)
norm_gas = np.trapz(4*np.pi*rr**2*rho_gas(rr), rr)
rho0_gas = Mgas/norm_gas

# --- member galaxies: a Schechter-ish luminosity function, NFW-like positions ---
Ngal = 300                       # ~hundreds of members in a rich cluster
# masses: log-normal-ish around L*, spanning dwarfs..BCG; normalized to Mstar
mgal = rng.lognormal(mean=np.log(3e10*Msun), sigma=1.1, size=Ngal)
mgal *= Mstar/mgal.sum()         # exact total
# add a BCG ~ 1e12 Msun at center
mgal[0] = 1e12*Msun
mgal *= Mstar/mgal.sum()
# positions: NFW number density, c=4, within R500 (projected radius)
c_nfw = 4.0
rs_nfw = R500/c_nfw
def sample_nfw_radii(n):
    # inverse-CDF-ish via rejection on r^2 rho_NFW
    out = []
    while len(out) < n:
        r = rng.uniform(0, R500, size=n)
        rho = 1.0/((r/rs_nfw)*(1+r/rs_nfw)**2 + 1e-30)
        w = r**2 * rho
        w /= w.max()
        keep = rng.uniform(size=n) < w
        out.extend(r[keep].tolist())
    return np.array(out[:n])
rgal = sample_nfw_radii(Ngal)
cth  = rng.uniform(-1, 1, size=Ngal); sth = np.sqrt(1-cth**2)
ph   = rng.uniform(0, 2*np.pi, size=Ngal)
gx = rgal*sth*np.cos(ph); gy = rgal*sth*np.sin(ph); gz = rgal*cth
gpos = np.stack([gx, gy, gz], axis=1)
# galaxy "size" (Plummer softening) ~ a few kpc so the inter-galaxy field is finite
b_gal = 15.0*kpc

print(f"\nCluster: M500={M500/Msun:.1e}, R500={R500/kpc:.0f} kpc, "
      f"Mgas={Mgas/Msun:.2e}, Mstar={Mstar/Msun:.2e} ({Ngal} galaxies)")
print(f"  member mass range: {mgal.min()/Msun:.2e} .. {mgal.max()/Msun:.2e} Msun (BCG)")

# --- Newtonian field on a 3D grid (cartesian, core-focused) ---
# Core box +- 0.6 Mpc, fine grid. Compute g_N = grad Phi_N from gas (analytic
# spherical) + discrete galaxies (sum of softened point fields).
L  = 0.6*Mpc
Ng = 96                              # grid per axis (96^3 ~ 0.9M cells)
ax = np.linspace(-L, L, Ng)
dx = ax[1]-ax[0]
X, Y, Z = np.meshgrid(ax, ax, ax, indexing='ij')
Rr = np.sqrt(X**2+Y**2+Z**2) + 1e-12

# gas Newtonian g (spherical, enclosed-mass)
def Mgas_enc(r):
    r = np.atleast_1d(r)
    out = np.empty_like(r)
    for i, rv in enumerate(r):
        rr2 = np.linspace(1e-3*R500, max(rv,1e-3*R500), 400)
        out[i] = rho0_gas*np.trapz(4*np.pi*rr2**2*rho_gas(rr2), rr2)
    return out
# precompute gas g on a radial table then interpolate (fast)
rtab = np.linspace(0, np.sqrt(3)*L, 600)
Mtab = Mgas_enc(rtab)
gN_gas_tab = G*Mtab/(rtab**2 + (5*kpc)**2)   # softened at very center
gN_gas = np.interp(Rr.ravel(), rtab, gN_gas_tab).reshape(Rr.shape)
# gas g vector (radial inward)
gxg = -gN_gas*X/Rr; gyg = -gN_gas*Y/Rr; gzg = -gN_gas*Z/Rr

# DISCRETE galaxies: sum softened point fields (vectorized over galaxies in chunks)
gxd = np.zeros_like(X); gyd = np.zeros_like(X); gzd = np.zeros_like(X)
flat = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)   # (Ncell,3)
for i in range(Ngal):
    dvec = flat - gpos[i]                      # (Ncell,3)
    d2 = (dvec**2).sum(axis=1) + b_gal**2
    gmag = G*mgal[i]/d2                         # Plummer
    inv_d = 1.0/np.sqrt(d2)
    gxd += (-gmag*dvec[:,0]*inv_d).reshape(X.shape)
    gyd += (-gmag*dvec[:,1]*inv_d).reshape(X.shape)
    gzd += (-gmag*dvec[:,2]*inv_d).reshape(X.shape)

# SMOOTH stars: same total Mstar as a smooth NFW-number-density profile (spherical)
# build smooth stellar enclosed mass following the galaxy NFW radial profile
def Mstar_enc_smooth(r):
    # NFW cumulative shape normalized to Mstar within R500
    x = r/rs_nfw
    mu = np.log(1+x) - x/(1+x)
    xR = R500/rs_nfw
    muR = np.log(1+xR) - xR/(1+xR)
    return Mstar*mu/muR
gN_star_tab = G*Mstar_enc_smooth(rtab)/(rtab**2+(5*kpc)**2)
gN_star = np.interp(Rr.ravel(), rtab, gN_star_tab).reshape(Rr.shape)
gxs = -gN_star*X/Rr; gys = -gN_star*Y/Rr; gzs = -gN_star*Z/Rr

# total Newtonian field vectors:  DISCRETE = gas + galaxies ; SMOOTH = gas + smooth stars
gx_disc = gxg+gxd; gy_disc=gyg+gyd; gz_disc=gzg+gzd
gx_smo  = gxg+gxs; gy_smo =gyg+gys; gz_smo =gzg+gzs
gN_disc = np.sqrt(gx_disc**2+gy_disc**2+gz_disc**2)
gN_smo  = np.sqrt(gx_smo**2 +gy_smo**2 +gz_smo**2)

# QUMOND: g_MOND = nu(g_N) * g_N (vector along g_N).  Build the (nu) g_N field,
# take its divergence -> total (baryon+phantom) density; subtract baryon -> phantom.
def qumond_total_density(gx_, gy_, gz_):
    gN = np.sqrt(gx_**2+gy_**2+gz_**2) + 1e-30
    nu = nu_fw(gN)
    # nu * g_vector  (this is g_MOND in QUMOND)
    Gx = nu*gx_; Gy = nu*gy_; Gz = nu*gz_
    # div(g_MOND) = -4 pi G rho_total  => rho_total = -div/(4 pi G)
    dGx = np.gradient(Gx, dx, axis=0)
    dGy = np.gradient(Gy, dx, axis=1)
    dGz = np.gradient(Gz, dx, axis=2)
    div = dGx+dGy+dGz
    rho_tot = -div/(4*np.pi*G)
    return rho_tot, nu

rho_tot_disc, nu_disc = qumond_total_density(gx_disc, gy_disc, gz_disc)
rho_tot_smo,  nu_smo  = qumond_total_density(gx_smo,  gy_smo,  gz_smo)

# enclosed total mass within radius r (sum cells, dx^3 volume)
cellV = dx**3
def Menc(rho, r):
    mask = Rr <= r
    return (rho[mask].sum())*cellV

print("\n--- enclosed TOTAL (baryon+phantom) gravitating mass, QUMOND ---")
print(f"{'r [kpc]':>8} {'M_disc[Msun]':>14} {'M_smo[Msun]':>14} {'disc/smo':>9}")
for rk in [100, 200, 300, 420, 550]:
    r = rk*kpc
    Md = Menc(rho_tot_disc, r)/Msun
    Ms = Menc(rho_tot_smo,  r)/Msun
    print(f"{rk:>8} {Md:>14.3e} {Ms:>14.3e} {Md/Ms:>9.4f}")

# --- the inter-galaxy collective field: is it above or below a0? ---
# sample g_N (smooth-subtracted gas+galaxy) at random inter-galaxy points (>50 kpc
# from any galaxy) in the core
core_mask = (Rr < 420*kpc)
# distance to nearest galaxy for each cell (approx via min over galaxies, subsample)
sub = rng.choice(np.where(core_mask.ravel())[0], size=4000, replace=False)
pts = flat[sub]
dmin = np.full(len(pts), np.inf)
for i in range(Ngal):
    dd = np.sqrt(((pts-gpos[i])**2).sum(axis=1))
    dmin = np.minimum(dmin, dd)
inter = dmin > 60*kpc     # genuinely inter-galaxy
gN_at = gN_disc.ravel()[sub]
print(f"\n--- collective field in the INTER-GALAXY medium (core) ---")
print(f"  N inter-galaxy sample points (>60 kpc from any galaxy): {inter.sum()}")
print(f"  median g_N / a0 inter-galaxy = {np.median(gN_at[inter])/a0:.3f}")
print(f"  10-90% g_N/a0                = {np.percentile(gN_at[inter],10)/a0:.3f} .. "
      f"{np.percentile(gN_at[inter],90)/a0:.3f}")
print(f"  (gas-only g_N/a0 at 300 kpc  = {np.interp(300*kpc,rtab,gN_gas_tab)/a0:.3f})")

# --- EFE sign: external field a member galaxy feels FROM THE REST of the cluster ---
# For each galaxy, g_ext = field from gas + ALL OTHER galaxies at its position.
print(f"\n--- EFE on member galaxies: g_ext (from rest of cluster) vs g_int, vs a0 ---")
gext_list = []
for i in range(Ngal):
    # gas field at galaxy i
    ri = rgal[i]
    gg = np.interp(ri, rtab, gN_gas_tab)
    # other galaxies
    dvec = gpos - gpos[i]
    d2 = (dvec**2).sum(axis=1) + b_gal**2
    d2[i] = np.inf
    gother = (G*mgal/d2)
    # vector sum magnitude (approx: add gas radial + other-galaxy vectors)
    ovec = -(dvec*(G*mgal/d2/np.sqrt(d2))[:,None])
    ovec[i] = 0
    gvec_other = ovec.sum(axis=0)
    # gas vector (radial inward) at galaxy i
    rhat = gpos[i]/(np.linalg.norm(gpos[i])+1e-30)
    gvec_gas = -gg*rhat
    gext = np.linalg.norm(gvec_gas+gvec_other)
    gext_list.append(gext)
gext = np.array(gext_list)
# internal field of an L* member at its edge (~ a few kpc, deep MOND): g_int ~ sqrt(GM a0)/R
Rmem = 5*kpc
gint = np.sqrt(G*mgal*a0)/Rmem
print(f"  median g_ext/a0 on members   = {np.median(gext)/a0:.3f}")
print(f"  10-90% g_ext/a0              = {np.percentile(gext,10)/a0:.3f} .. {np.percentile(gext,90)/a0:.3f}")
print(f"  median g_int/a0 (member edge)= {np.median(gint)/a0:.3f}")
print(f"  fraction with g_ext > g_int  = {(gext>gint).mean():.2f}")
print(f"  fraction with g_ext > a0     = {(gext>a0).mean():.2f}")

# --- net: collective/clumpy effect on TOTAL core gravitating mass ---
r_core = 420*kpc
Md = Menc(rho_tot_disc, r_core)/Msun
Ms = Menc(rho_tot_smo,  r_core)/Msun
Mbar_core = (Mgas_enc(r_core)[0] + Mstar_enc_smooth(r_core))/Msun
print("\n"+"="*72)
print("NET RESULT (core <420 kpc):")
print(f"  baryon mass in core          = {Mbar_core:.3e} Msun")
print(f"  TOTAL grav mass DISCRETE      = {Md:.3e} Msun  (eta_disc={Md/Mbar_core:.3f})")
print(f"  TOTAL grav mass SMOOTH        = {Ms:.3e} Msun  (eta_smo ={Ms/Mbar_core:.3f})")
print(f"  collective/clumpy DELTA       = {(Md-Ms):.3e} Msun  ({100*(Md/Ms-1):+.2f}%)")
print("="*72)

# residual context: rich-core target M_res ~ 1.0e14 Msun bare gap (CLUSTER_STACK)
M_res_target = 1.006e14
print(f"\nResidual context: bare core gap (CLUSTER_STACK) ~ {M_res_target:.2e} Msun.")
print(f"  Carl's collective DELTA covers {100*(Md-Ms)*Msun/(M_res_target*Msun):+.1f}% of the gap"
      if abs(Md-Ms) > 0 else "  DELTA ~ 0")
