#!/usr/bin/env python3
"""
CROSS-SCALE / DECLINE-COMPARISON lane for a0(z)-from-SNe.
Framework: de Sitter-Unruh MODIFIED-INERTIA (Carl Zimmerman).
  rho_DE(z) read off SNe point-by-point (NO Lambda, NO w(z) assumed),
  a0(z) = (c/2) sqrt(G rho_DE(z)) = (c/Z) sqrt(H(z)^2 - Om H0^2 (1+z)^3),
          Z = sqrt(32 pi / 3) = 5.789   [rho_DE / canonical footing]

Deliverables:
  (a) SNe-derived a0(0) vs SPARC-measured a0 = 1.181e-10 +/-16%  -> sigma-tension, both H0.
  (b) a0(z=3)/a0(0) from SNe (reconstructed rho_DE + DESI w0wa reference) vs framework 0.60-0.75.
  (c) Is the SNe a0(z) CONSTRAINING or merely consistent-with-flat?

Credits: Milgrom (a0 kernel); Brout+2022 / Scolnic (Pantheon+SH0ES);
         Seikel-Clarkson-Smith 2012 (GP model-independent H(z)).
Frozen inputs are READ-ONLY. Exit 0. Diagonal errors only (documented caveat).
"""
import json, warnings, numpy as np
warnings.filterwarnings("ignore")
np.seterr(all="ignore")
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, WhiteKernel

rng = np.random.default_rng(20260718)

# ---- constants ----
c_ms   = 2.99792458e8          # m/s
Mpc_m  = 3.0856775814913673e22 # m
Z      = np.sqrt(32*np.pi/3.0) # 5.78918...
SPARC  = 1.1814381247770623e-10
SPARC_ERR = 0.16*SPARC         # 16% (GLS gas-dominated, Lambda-blind)
OM_LIST = [0.29, 0.315, 0.35]  # matter is NOT dark energy -> no circularity
H0_LIST = [67.4, 73.0]         # SNe are M_B-H0 degenerate: a0(0) carries H0, shape does not
DESI_W0, DESI_WA = -0.83, -0.75
FRAME_LO, FRAME_HI = 0.60, 0.75

def H0_si(H0kms): return H0kms*1e3/Mpc_m   # s^-1

# ---- (a) a0(0): analytic z->0 limit, E(0)=1 exactly, NO reconstruction noise ----
# a0(0) = (c/Z) H0 sqrt(1-Om)   [rho_DE footing]
def a0_zero(H0kms, Om): return (c_ms/Z)*H0_si(H0kms)*np.sqrt(1.0-Om)

partA = {}
for H0 in H0_LIST:
    for Om in OM_LIST:
        a0 = a0_zero(H0, Om)
        # SNe-side error from Om spread only (H0 quoted separately, both shown)
        # combine with SPARC 16% in quadrature for the tension
        sig = np.hypot(SPARC_ERR, 0.0)  # a0(0) Om-error added below per-point
        partA[(H0,Om)] = a0
# Om-driven a0(0) uncertainty at each H0 (half-range of OM_LIST)
def a0_om_err(H0):
    vals = [a0_zero(H0,om) for om in OM_LIST]
    return (max(vals)-min(vals))/2.0

tensions = {}
for H0 in H0_LIST:
    a0 = a0_zero(H0, 0.315)
    e_om = a0_om_err(H0)
    sig = np.hypot(SPARC_ERR, e_om)
    tensions[H0] = dict(a0=a0, a0_om_err=e_om,
                        diff=SPARC-a0, sigma=(SPARC-a0)/sig)

# ---- load SNe (frozen, READ-ONLY) ----
DAT = "/Users/carlzimmerman/new_physics/prep_2026/sne_lambda/pantheonplus_full.dat"
hdr = open(DAT).readline().split()
ix = {n:i for i,n in enumerate(hdr)}
rows = np.genfromtxt(DAT, skip_header=1,
        usecols=(ix['zHD'], ix['m_b_corr'], ix['m_b_corr_err_DIAG'], ix['IS_CALIBRATOR']))
z, mb, mberr, iscal = rows.T
sel = (iscal==0) & (z>0.01)
z, mb, mberr = z[sel], mb[sel], mberr[sel]
order = np.argsort(z); z, mb, mberr = z[order], mb[order], mberr[order]
zmax = z.max()

# ---- bin the Hubble diagram (log-z) for a stable derivative (Seikel-style) ----
nb = 25
edges = np.geomspace(z.min(), z.max(), nb+1)
zb, mbb, eb = [], [], []
for i in range(nb):
    m = (z>=edges[i]) & (z<edges[i+1] if i<nb-1 else z<=edges[i+1])
    if m.sum()<3: continue
    w = 1.0/mberr[m]**2
    zb.append(np.average(z[m], weights=w))
    mbb.append(np.average(mb[m], weights=w))
    eb.append(1.0/np.sqrt(w.sum()))          # error on the weighted mean
zb, mbb, eb = map(np.array, (zb, mbb, eb))

# ---- GP on binned m_b_corr(z) (Seikel-Clarkson-Smith 2012) ----
X = zb[:,None]
kern = C(1.0,(1e-2,1e3))*RBF(0.5,(0.05,5.0)) + WhiteKernel(1e-3,(1e-6,1.0))
gp = GaussianProcessRegressor(kernel=kern, alpha=eb**2, normalize_y=True,
                              n_restarts_optimizer=6, random_state=0).fit(X, mbb)

import sys, scipy.integrate as si
Om0 = 0.315
def E_lcdm(zz,Om): return np.sqrt(Om*(1+zz)**3 + (1-Om))
def cpl_rho_ratio(zz, w0, wa):                 # rho_DE(z)/rho_DE(0) for CPL w(a)=w0+wa(1-a)
    return (1+zz)**(3*(1+w0+wa)) * np.exp(-3*wa*zz/(1+zz))
def E_cpl(zz,Om,w0,wa): return np.sqrt(Om*(1+zz)**3 + (1-Om)*cpl_rho_ratio(zz,w0,wa))

# =====================================================================
# (b1) MODEL-INDEPENDENT GP RECONSTRUCTION of rho_DE(z)/rho_DE(0)
#      HONEST reliability envelope: differentiating d_L twice-over to get a
#      SMALL residual rho_DE = E^2 - Om(1+z)^3 (difference of large numbers) is
#      only stable where SNe are dense (z<~0.6). We VALIDATE per-z with a
#      synthetic-LCDM self-test and only trust z where the self-test recovers 1.
# =====================================================================
zgc = np.linspace(float(zb.min()), zmax, 220)
def E_from_m(mz, zg):
    # m=5log10(D)+const ; Dc=D/(1+z) ~ A z ; E=1/Dc' normalized by A=lim Dc/z (no diff).
    D = 10**(mz/5.0); Dc = D/(1.0+zg)
    lo = zg <= 0.12
    A  = np.polyfit(zg[lo], (Dc/zg)[lo], 1)[1]
    return A/np.gradient(Dc, zg)
def rhoratio(Ez, zg, Om): return (Ez**2 - Om*(1+zg)**3)/(1.0-Om)

NS = 600
msamp = gp.sample_y(zgc[:,None], n_samples=NS, random_state=1).T
Rho = np.array([rhoratio(E_from_m(msamp[i], zgc), zgc, Om0) for i in range(NS)])

# method-bias check on NOISE-FREE LCDM mu (diagnoses METHOD bias only, not data reach)
zz_fine = np.linspace(1e-4, zmax, 4000)
Dc_l = si.cumulative_trapezoid(1.0/E_lcdm(zz_fine,Om0), zz_fine, initial=0)
mu_l = 5*np.log10((1+zgc)*np.interp(zgc, zz_fine, Dc_l)) + 43.0
rho_st = rhoratio(E_from_m(mu_l, zgc), zgc, Om0)
# RELIABILITY horizon from the REAL-DATA posterior: contiguous-from-low-z region where
# the SIGN of rho_DE is pinned (f_phys>=0.9). Beyond it, differentiating d_L to extract
# the small DE residual (difference of large numbers) is noise-dominated.
fphys_grid = np.mean(Rho>0, axis=0)
zrel = zgc[0]
for i in range(len(zgc)):
    if fphys_grid[i] >= 0.90: zrel = zgc[i]
    else: break
print(f"[reliability] real-data rho_DE(z)>0 pinned (f_phys>=0.9) out to z~{zrel:.2f}", file=sys.stderr)

def at(zt):
    j = int(np.argmin(np.abs(zgc-zt)))
    col = Rho[:,j]
    med, lo, hi = np.percentile(col,[50,16,84])
    a0r = np.sqrt(col[col>0]); a0med = float(np.median(a0r)) if a0r.size else float('nan')
    return dict(z=float(zgc[j]), rho_med=float(med), rho_lo=float(lo), rho_hi=float(hi),
                f_phys=float(np.mean(col>0)), a0_med=a0med, reliable=bool(zgc[j]<=zrel+1e-9),
                selftest=float(rho_st[j]))
r_zrel = at(zrel)          # deepest RELIABLE model-indep point
r_z1, r_z2 = at(1.0), at(2.0)
scan = [at(zt) for zt in (0.2,0.3,0.4,0.5,0.7,1.0)]   # degradation scan

# =====================================================================
# (b2) ROBUST, DIFFERENTIATION-FREE decline constraint:
#      offset-marginalized chi^2 fit of flat-LCDM vs DESI-CPL to the SNe.
#      (M_B + 5log10 c/H0 is a single degenerate additive const -> marginalized.)
# =====================================================================
def mu_template(zdat, Efun):
    zf = np.linspace(1e-5, zdat.max()*1.001, 6000)
    dc = si.cumulative_trapezoid(1.0/Efun(zf), zf, initial=0)   # Hubble-free comoving
    dl = (1+zdat)*np.interp(zdat, zf, dc)
    return 5*np.log10(dl)                                        # + const (marginalized)
def chi2_marg(zdat, mdat, sig, Efun):
    t = mu_template(zdat, Efun); r = mdat - t; w = 1.0/sig**2
    off = np.sum(w*r)/np.sum(w)                 # analytic best offset (=M_B+...)
    return float(np.sum(w*(r-off)**2))
chi2_lcdm = chi2_marg(z, mb, mberr, lambda zz: E_lcdm(zz,Om0))
chi2_cpl  = chi2_marg(z, mb, mberr, lambda zz: E_cpl(zz,Om0,DESI_W0,DESI_WA))
dchi2 = chi2_cpl - chi2_lcdm    # >0: CPL worse; ~O(1): SNe cannot tell them apart
# Om-FRAGILITY of the decline hint (verifier fix): the sign of Delta-chi2 REVERSES
# across the stated Om range -> the -3.10 is NOT a standalone decline detection.
dchi2_om = {}
for Om in OM_LIST:
    cl = chi2_marg(z, mb, mberr, lambda zz,_Om=Om: E_lcdm(zz,_Om))
    cc = chi2_marg(z, mb, mberr, lambda zz,_Om=Om: E_cpl(zz,_Om,DESI_W0,DESI_WA))
    dchi2_om[Om] = float(cc-cl)

# DESI / LCDM reference ratios (clean analytic)
desi = {str(zz): dict(rho_ratio=float(cpl_rho_ratio(zz,DESI_W0,DESI_WA)),
                      a0_ratio=float(np.sqrt(cpl_rho_ratio(zz,DESI_W0,DESI_WA))))
        for zz in (1.0,2.0,3.0)}
lcdm = {str(zz): 1.0 for zz in (1.0,2.0,3.0)}

detect = dict(deepest_reliable=r_zrel, z1=r_z1, z2=r_z2,
              chi2_lcdm=float(chi2_lcdm), chi2_cpl=float(chi2_cpl), dchi2=float(dchi2),
              zrel=float(zrel))

# alt footing note (rho_total/cH0 vs rho_DE/cH_Lambda): a0(0) magnitudes only
alt = {'canonical_rhoDE_cHLambda_H0_67p4_Om0p315': a0_zero(67.4,0.315),
       'alt_rhoDE_H0_73_Om0p315': a0_zero(73.0,0.315),
       'note': 'rho_total/cH0 footing (~1.13e-10) differs by using full H^2 not the DE part; '
               'Z is POSITED so the a0 magnitude inherits it. Ratios below are footing-robust.'}

# ---- report ----
def f(x): return f"{x:.4e}"
lines = []
P = lines.append
P("="*72); P("CROSS-SCALE / DECLINE-COMPARISON  --  a0(z) from Pantheon+SH0ES SNe")
P("="*72)
P(f"Z = sqrt(32pi/3) = {Z:.5f}   (POSITED; a0 magnitude inherits it)")
P(f"SNe cut: IS_CALIBRATOR==0 & zHD>0.01  ->  N={sel.sum()}  (zmax={zmax:.3f})")
P("")
P("(a) a0(0) = (c/Z) H0 sqrt(1-Om)   [z->0 limit, E(0)=1 exact, NO recon noise]")
P(f"    SPARC-measured a0 (GLS gas-dom, Lambda-BLIND) = {f(SPARC)} +/- {f(SPARC_ERR)} (16%)")
P("    SNe-derived a0(0) grid [rho_DE footing]:")
for H0 in H0_LIST:
    s=f"      H0={H0:5.1f}: "
    for Om in OM_LIST: s+=f" Om={Om}:{f(a0_zero(H0,Om))} "
    P(s)
P("    sigma-tension vs SPARC (Om=0.315, err=quad[SPARC16%, Om-spread]):")
for H0 in H0_LIST:
    t=tensions[H0]
    P(f"      H0={H0:5.1f}: a0(0)={f(t['a0'])}  diff={f(t['diff'])}  ->  {t['sigma']:+.2f} sigma")
P("")
P("(b) a0(z)/a0(0) = sqrt[(E^2-Om(1+z)^3)/(1-Om)]   (H0-INDEPENDENT ratio; Om=0.315)")
P(f"    framework target at z=3: {FRAME_LO}-{FRAME_HI}   (=> rho_DE-ratio {FRAME_LO**2:.2f}-{FRAME_HI**2:.2f})")
P("    -- REFERENCE hypotheses (clean analytic) --")
for zz in ('1.0','2.0','3.0'):
    P(f"      DESI w0wa=(-0.83,-0.75): z={zz}: a0-ratio={desi[zz]['a0_ratio']:.3f}  (rho-ratio={desi[zz]['rho_ratio']:.3f})")
P("      LCDM (constant Lambda): a0-ratio = 1.000 at all z (FLAT)")
P(f"      NOTE: DESI-CPL a0-ratio(z=3)={desi['3.0']['a0_ratio']:.3f} lands INSIDE the framework 0.60-0.75 band.")
P("    -- model-indep SNe GP reconstruction of rho_DE(z)/rho_DE(0) (signed, 16/50/84) --")
P(f"      real-data rho_DE(z) sign pinned (f_phys>=0.9) only out to z~{zrel:.2f}; degradation scan:")
for d in scan:
    flag = "OK " if d['reliable'] else "BAD"
    P(f"        {flag} z={d['z']:.2f}: rho-ratio {d['rho_med']:+6.2f} [{d['rho_lo']:+6.2f},{d['rho_hi']:+7.2f}]"
      f"  f(rho>0)={d['f_phys']:.2f}")
dd=r_zrel
P(f"      deepest reliable z={dd['z']:.2f}: rho-ratio {dd['rho_med']:+.2f} [{dd['rho_lo']:+.2f},{dd['rho_hi']:+.2f}]"
  f"  -> a0-ratio~{dd['a0_med']:.2f}  (band overlaps BOTH flat=1 and framework {FRAME_LO**2:.2f}-{FRAME_HI**2:.2f})")
P(f"      => beyond z~{zrel:.2f} the model-indep rho_DE(z) is UNCONSTRAINED (sign not even pinned);")
P("         z=3 is EXTRAPOLATED beyond the data (zmax=2.26). No SNe a0(z=3) measurement is possible.")
P("")
P("(c) CONSTRAINING vs consistent-with-flat  (robust, differentiation-free):")
P(f"      offset-marginalized fit to all N={sel.sum()} SNe (Om=0.315):")
P(f"        chi2(flat-LCDM) = {chi2_lcdm:8.2f}")
P(f"        chi2(DESI-CPL)  = {chi2_cpl:8.2f}   ->  Delta-chi2 = {dchi2:+.2f}")
nsig = np.sqrt(abs(dchi2))     # 0 extra free params (both models fixed) -> ~sqrt(dchi2) sigma
favor = "the DESI decline" if dchi2<0 else "flat-LCDM"
P(f"      |Delta-chi2|={abs(dchi2):.2f} (~{nsig:.1f} sigma, mild preference for {favor}) "
  f"-> NON-DECISIVE: SNe cannot separate flat from the DESI-like decline at 2sigma.")
P("      Om-FRAGILITY (Delta-chi2 SIGN reverses across Om -> not a standalone decline hint):")
_sfl = "  ".join(f"Om={Om}:{dchi2_om[Om]:+.2f}" for Om in OM_LIST)
P(f"        {_sfl}   (favors decline at low Om, FLIPS to favor flat at Om=0.35)")
P("      Both the model-indep reconstruction (band overlaps flat=1 AND 0.60-0.75 AND rho<0)")
P("      and the direct fit say: SNe alone are NON-CONSTRAINING on a0(z) evolution.")
P("      a0(0) is the robust SNe output; the decline is NOT detectable from SNe alone.")
P("      Clean decline numbers come from the DESI-CPL / LCDM references, not a SNe measurement.")
P("")
for L in lines: print(L)

out = dict(
  Z=Z, N_sne=int(sel.sum()), zmax=float(zmax),
  SPARC=SPARC, SPARC_ERR=SPARC_ERR,
  a0_zero={f"H0={H0}_Om={Om}": a0_zero(H0,Om) for H0 in H0_LIST for Om in OM_LIST},
  tensions={str(H0): {k:(float(v)) for k,v in t.items()} for H0,t in tensions.items()},
  ratio_SNe_rhoDE_signed=dict(zrel=float(zrel), deepest_reliable=r_zrel,
                              z1=r_z1, z2=r_z2, degradation_scan=scan),
  ratio_DESI_cpl=desi, ratio_LCDM=lcdm,
  chi2_test=dict(chi2_lcdm=float(chi2_lcdm), chi2_cpl=float(chi2_cpl), dchi2=float(dchi2),
                 dchi2_vs_Om={str(k):v for k,v in dchi2_om.items()}),
  framework_band=[FRAME_LO,FRAME_HI],
  framework_band_rhoratio=[FRAME_LO**2,FRAME_HI**2],
  detect=detect, alt_footing=alt)
with open("/Users/carlzimmerman/new_physics/prep_2026/a0z_from_sne/crossscale_results.json","w") as fh:
    json.dump(out, fh, indent=1, default=float)
print("wrote crossscale_results.json")
