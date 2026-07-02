#!/usr/bin/env python3
"""
ADVERSARIAL VERIFY of l2_cluster_gravz_discriminator.py -- independent method.
Analytic potentials (NFW ln-formula, Hernquist closed form) instead of the lane's
numeric cumulative-trapezoid of g(r); independent LOS projection grid.
Targets to reproduce (lane values):
  (1) GR+DM integrated R<6 Mpc: -8.09 (M200=2e14), -12.44 (4e14)
  (3) baryon-only: -1.58, -2.19 ; fraction 0.176-0.195
  (4a) framework-nu canonical: -4.93, -6.31
  sigma: pure-MI vs R23 = 2.9 ; MG-MOND canonical vs R23 = 1.8
"""
import numpy as np

G, c, Msun, Mpc = 6.674e-11, 2.998e8, 1.989e30, 3.0857e22
kpc = Mpc/1e3
rho_cr = 9.20e-27
A0 = 9.36e-11
FB = 0.14; M_BCG = 1.0e12*Msun; A_BCG = 30*kpc

def pars(M200, c200=5.0):
    r200 = (3*M200/(4*np.pi*200*rho_cr))**(1/3)
    rs = r200/c200
    mc = np.log(1+c200)-c200/(1+c200)
    Ms = M200/mc
    rho_s_rs3 = Ms/(4*np.pi)          # rho_s*rs^3
    return r200, rs, Ms, rho_s_rs3

# analytic: Phi_NFW(r)-Phi_NFW(0) = 4 pi G rho_s rs^2 * [1 - ln(1+x)/x]
def dphi_nfw(r, rs, rho_s_rs3):
    x = r/rs
    return 4*np.pi*G*(rho_s_rs3/rs)*(1 - np.log(1+x)/x)

# analytic Hernquist: Phi = -GM/(r+a); dphi = GM/a - GM/(r+a)
def dphi_hern(r, M, a):
    return G*M/a - G*M/(r+a)

def dphi_numeric_from_g(gfunc, r):
    g = gfunc(r)
    return np.concatenate([[0.0], np.cumsum(0.5*(g[1:]+g[:-1])*np.diff(r))])

def integrated(dphi_of_r, rs, Rmax=6.0*Mpc):
    """count-weighted <Delta(R)> over R<Rmax, NFW tracer, independent grid."""
    R_arr = np.linspace(0.03*Mpc, Rmax, 121)
    dvals, Sig = [], []
    for R in R_arr:
        zmax = np.sqrt(max(Rmax**2 - R**2, 0))
        zz = np.linspace(0, zmax, 3001)[1:]
        rr = np.sqrt(R**2+zz**2); x = rr/rs
        w = 1.0/(x*(1+x)**2)
        dp = dphi_of_r(rr)
        dvals.append(-np.sum(w*dp)/np.sum(w)/c/1e3)
        Sig.append(np.sum(w))
    d = np.array(dvals); wgt = np.array(Sig)*R_arr
    return np.sum(wgt*d)/np.sum(wgt)

print("independent re-derivation (analytic Phi where possible):")
res = {}
for M200s in (2e14, 4e14):
    M200 = M200s*Msun
    r200, rs, Ms, rr3 = pars(M200)
    # (1) GR+DM
    f_gr = lambda r: dphi_nfw(r, rs, rr3)
    # (3) baryon-only: fb*NFW + BCG Hernquist, both analytic
    f_bar = lambda r: FB*dphi_nfw(r, rs, rr3) + dphi_hern(r, M_BCG, A_BCG)
    # (4a) framework nu on baryons: numeric (no closed form)
    rgrid = np.logspace(np.log10(0.5*kpc), np.log10(10*Mpc), 20000)
    def gbar(r):
        x = r/rs
        Mb = FB*Ms*(np.log(1+x)-x/(1+x)) + M_BCG*r**2/(r+A_BCG)**2
        return G*Mb/r**2
    gmi = np.sqrt(gbar(rgrid)**2 + gbar(rgrid)*A0)   # framework's OWN nu
    dp_mi = np.concatenate([[0.0], np.cumsum(0.5*(gmi[1:]+gmi[:-1])*np.diff(rgrid))])
    f_mi = lambda r: np.interp(r, rgrid, dp_mi)
    v_gr  = integrated(f_gr, rs)
    v_bar = integrated(f_bar, rs)
    v_mi  = integrated(f_mi, rs)
    res[M200s] = (v_gr, v_bar, v_mi)
    print(f"  M200={M200s:.0e}: r200={r200/Mpc:.2f} Mpc | GR+DM {v_gr:7.2f} | "
          f"baryon-only {v_bar:6.2f} | framework-nu MOND {v_mi:6.2f} km/s | "
          f"frac={v_bar/v_gr:.3f}")

pred_bar = np.mean([res[2e14][1], res[4e14][1]])
pred_mi  = np.mean([res[2e14][2], res[4e14][2]])
print(f"\n  pure-MI vs R23 (-11.4+/-3.3): {(pred_bar+11.4)/3.3:.2f} sigma")
print(f"  pure-MI vs W11 (-7.7+/-3.0) : {(pred_bar+7.7)/3.0:.2f} sigma")
print(f"  MG-MOND(fw nu) vs R23       : {(pred_mi+11.4)/3.3:.2f} sigma")
print(f"  MG-MOND(fw nu) vs W11       : {(pred_mi+7.7)/3.0:.2f} sigma")

# sign sanity: dphi>=0 everywhere -> Delta<0 (blueshift) for ALL readings
r_t = np.logspace(np.log10(kpc), np.log10(6*Mpc), 50)
r200, rs, Ms, rr3 = pars(2e14*Msun)
assert np.all(dphi_nfw(r_t, rs, rr3) >= 0), "sign error"
print("\n  sign check: Phi(r)-Phi(0) >= 0 everywhere -> net BLUEshift (Delta<0). OK")

# W11 Kaiser caution quantified: TD term ~ +sigma_v^2/(2c); sigma~600 km/s -> +0.6 km/s? no:
sig_v = 600e3
td = sig_v**2/(2*c)/1e3
print(f"  transverse-Doppler scale for sigma_v=600 km/s: +{td:.1f} km/s (redshift, "
      f"i.e. W11's raw -7.7 understates |grav-z|; corrections make pure-MI tension WORSE)")
print("exit 0")
