"""
DRIVER: build a realistic rich cluster TWO WAYS and compute QUMOND total phantom
mass in the core both ways. The clumpy minus smooth difference IS Carl's collective
effect (if positive: overlapping fields ADD mass; if <=0: redistribute-only/sub-additive).

Rich cluster (matches the banked target):
  M500_tot ~ 1e15 Msun, R500 ~ 2100 kpc, core = 420 kpc.
  Gas: beta-model, fgas500 ~ 0.10 -> Mgas(<R500) ~ 1e14; in core ~ a few e13.
  Galaxies: Schechter LF, ~hundreds of members; M_stars_total in core ~ 1-3e13.
  (The point/clump mass is the STELLAR + any galaxy-scale gas; the smooth-baryon
   cluster-MOND estimate uses the same total but as a smooth shell.)

We compute the phantom in the CORE region. To resolve discrete galaxies (Plummer
a ~ 5-20 kpc) AND the core (420 kpc) in one periodic box, we use a box L and grid n
chosen for convergence; we run a box/resolution convergence check.

Output: M_ph(<R) for DISCRETE and SMOOTH, their ratio, and the inter-galaxy phantom.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from qumond_clumpy_vs_smooth import (G, Msun, kpc, Mpc, a0, Grid, qumond_phantom,
                                      beta_rho, beta_norm, plummer_rho, M_enclosed,
                                      nu_simple)

np.random.seed(42)

# ----------------------------- cluster parameters -----------------------------
R500_kpc   = 2100.0
R500       = R500_kpc*kpc
Rcore_kpc  = 420.0
Rcore      = Rcore_kpc*kpc
M500_tot   = 1.0e15*Msun        # apparent dynamical (for context; we work with BARYONS)

# Gas beta-model (rich relaxed): rc=0.20 R500, beta=0.65, fgas500=0.10
fgas500    = 0.10
rc_gas     = 0.20*R500
beta_gas   = 0.65
Mgas500    = fgas500*M500_tot

# Stars / galaxies: fstar = stars/gas ~ 0.15-0.2; total galaxy(stellar) mass
fstar      = 0.18
Mstar500   = fstar*Mgas500

# galaxy population: Schechter-like; ~300 members inside R500, steeper-massed BCG
N_gal      = 300                # members modeled as discrete clumps
# stellar mass function: draw from a Schechter; normalize so sum = Mstar500-ish in box
# We'll place galaxies following the gas/number radial profile (NFW-ish concentration).

print("="*78)
print("RICH CLUSTER -- QUMOND clumpy-vs-smooth phantom mass (Carl's collective EFE)")
print("="*78)
print(f"a0 = {a0:.3e} m/s^2 (framework, INPUT not derived)")
print(f"R500={R500_kpc:.0f} kpc, core={Rcore_kpc:.0f} kpc")
print(f"Mgas(<R500)={Mgas500/Msun:.3e} Msun, Mstar(<R500)={Mstar500/Msun:.3e} Msun")

# ----------------------------- build galaxy catalog -----------------------------
# radial positions: follow an NFW number density (c=4) truncated at R500 -> realistic
def sample_nfw_radii(n, rs, Rmax):
    out=[]
    while len(out)<n:
        r = np.random.uniform(0, Rmax, n*4)
        # NFW mass profile weight ~ r^2 rho_nfw(r); rho ~ 1/[(r/rs)(1+r/rs)^2]
        x=r/rs
        w = r**2/(x*(1+x)**2 + 1e-9)
        w/=w.max()
        keep = r[np.random.uniform(0,1,len(r))<w]
        out.extend(keep.tolist())
    return np.array(out[:n])

rs_gal = R500/4.0
r_gal = sample_nfw_radii(N_gal, rs_gal, R500)
# isotropic angles
ct = np.random.uniform(-1,1,N_gal); ph = np.random.uniform(0,2*np.pi,N_gal)
st = np.sqrt(1-ct**2)
gx = r_gal*st*np.cos(ph); gy = r_gal*st*np.sin(ph); gz = r_gal*ct

# stellar masses: Schechter draw, Mstar* ~ 1e11, alpha=-1.1; BCG forced ~ 1e12
Mstar_char = 1e11*Msun
def schechter_draw(n, Mchar, alpha=-1.1, Mmin=2e9*Msun, Mmax=8e11*Msun):
    # rejection sample dN/dM ~ (M/Mchar)^alpha exp(-M/Mchar)
    out=[]
    while len(out)<n:
        M = np.exp(np.random.uniform(np.log(Mmin), np.log(Mmax), n*5))
        w = (M/Mchar)**(alpha+1)*np.exp(-M/Mchar)  # +1 for log sampling
        w/=w.max()
        keep = M[np.random.uniform(0,1,len(M))<w]
        out.extend(keep.tolist())
    return np.array(out[:n])
gal_M = schechter_draw(N_gal, Mstar_char)
gal_M[0] = 1.2e12*Msun                 # BCG at center
r_gal[0]=0; gx[0]=gy[0]=gz[0]=0.0
# normalize total galaxy mass inside R500 to Mstar500
gal_M *= Mstar500/gal_M.sum()
print(f"N_gal={N_gal}, total galaxy mass={gal_M.sum()/Msun:.3e} Msun "
      f"(BCG={gal_M[0]/Msun:.2e}, median={np.median(gal_M)/Msun:.2e})")

# Plummer scale per galaxy: a ~ 5 kpc (stellar half-light-ish; conservative -> compact = max collective effect)
a_plummer = 5.0*kpc

# ----------------------------- the two configurations on a grid -----------------------------
def build_rho(grid, discrete=True):
    """gas beta-model (always smooth) + galaxies (discrete Plummers OR smooth shell)."""
    # gas normalization: rho0 such that Mgas(<R500)=Mgas500
    rho0_gas = Mgas500/beta_norm(1.0, rc_gas, beta_gas, R500)
    rho = beta_rho(grid, rho0_gas, rc_gas, beta_gas)
    if discrete:
        for i in range(len(gal_M)):
            # only add galaxies whose center is inside the box footprint
            if max(abs(gx[i]),abs(gy[i]),abs(gz[i])) < grid.L/2 - 3*a_plummer:
                rho += plummer_rho(grid, gal_M[i], a_plummer, (gx[i],gy[i],gz[i]))
    else:
        # SMOOTH: smear galaxy mass into spherical shells matching the galaxy radial profile.
        # Build radial number-weighted-mass density of the galaxy ensemble and lay it down
        # spherically -> identical M_gal(<r), zero clumpiness.
        rr = grid.r
        # histogram galaxy mass vs radius -> rho_gal_smooth(r)
        rbins = np.linspace(0, grid.L/2, 200)
        rc_bins = 0.5*(rbins[1:]+rbins[:-1])
        Min_r = np.zeros_like(rc_bins)
        for i in range(len(gal_M)):
            idx = np.searchsorted(rbins, r_gal[i])-1
            if 0<=idx<len(Min_r):
                Min_r[idx]+=gal_M[i]
        shell_vol = 4/3*np.pi*(rbins[1:]**3 - rbins[:-1]**3)
        rho_gal_r = Min_r/shell_vol
        # interpolate onto grid radius
        rho_smooth_gal = np.interp(rr, rc_bins, rho_gal_r, left=rho_gal_r[0], right=0.0)
        rho += rho_smooth_gal
    return rho

# ----------------------------- run with convergence -----------------------------
def run_config(L_kpc, n, label):
    L = L_kpc*kpc
    grid = Grid(L, n)
    rho_d = build_rho(grid, discrete=True)
    rho_s = build_rho(grid, discrete=False)
    # sanity: enclosed baryon mass must match between discrete and smooth in the core
    Mb_d = M_enclosed(grid, rho_d, Rcore)/Msun
    Mb_s = M_enclosed(grid, rho_s, Rcore)/Msun
    ph_d, eff_d, _, gmag_d = qumond_phantom(grid, rho_d)
    ph_s, eff_s, _, gmag_s = qumond_phantom(grid, rho_s)
    Mph_d = M_enclosed(grid, ph_d, Rcore)/Msun
    Mph_s = M_enclosed(grid, ph_s, Rcore)/Msun
    print(f"\n--- {label}: L={L_kpc:.0f} kpc, n={n}, cell={L_kpc/n:.1f} kpc ---")
    print(f"  baryon M(<core): discrete={Mb_d:.4e}  smooth={Mb_s:.4e}  (match={Mb_d/Mb_s:.4f})")
    print(f"  PHANTOM M(<core): discrete={Mph_d:.4e}  smooth={Mph_s:.4e}")
    print(f"  >>> clumpy/smooth phantom ratio = {Mph_d/Mph_s:.4f}  "
          f"(delta = {(Mph_d-Mph_s):.3e} Msun = {100*(Mph_d/Mph_s-1):+.1f}%)")
    return dict(L_kpc=L_kpc, n=n, Mb_d=Mb_d, Mb_s=Mb_s, Mph_d=Mph_d, Mph_s=Mph_s,
                grid=grid, ph_d=ph_d, ph_s=ph_s, rho_d=rho_d, rho_s=rho_s)

if __name__=="__main__":
    print("\n" + "#"*78)
    print("# CONVERGENCE: box size and resolution")
    print("#"*78)
    res=[]
    # core=420 kpc; want box >> core to suppress periodic images; cell << a_plummer*? (a=5kpc)
    res.append(run_config(L_kpc=3360, n=112, label="baseline"))   # cell=30 kpc
    res.append(run_config(L_kpc=3360, n=168, label="finer-res"))  # cell=20 kpc
    res.append(run_config(L_kpc=5040, n=168, label="bigger-box")) # cell=30 kpc, box 1.5x
    print("\n" + "="*78)
    print("SUMMARY (Carl's collective effect = discrete phantom - smooth phantom):")
    print("="*78)
    for r in res:
        print(f"  L={r['L_kpc']:.0f} n={r['n']}: clumpy/smooth = {r['Mph_d']/r['Mph_s']:.4f}  "
              f"({100*(r['Mph_d']/r['Mph_s']-1):+.1f}%), "
              f"M_ph_smooth={r['Mph_s']:.3e}, M_ph_disc={r['Mph_d']:.3e} Msun")
