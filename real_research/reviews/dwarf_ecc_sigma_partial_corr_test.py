#!/usr/bin/env python3
r"""
dwarf_ecc_sigma_partial_corr_test.py
================================================================================
THE PRE-SPECIFIED STATISTICAL TEST (extends dwarf_ecc_sigma_pilot_analysis.py).

H1 (framework, modified inertia): partial Spearman rho(sigma_los, ecc | controls)
   is POSITIVE -- at fixed pericenter, mass, r_half, a radial-plunge (high-ecc)
   diffuse dwarf runs HOTTER. SIGN = theorem.
H0 (MG/CDM): partial rho = 0 (instantaneous EFE -> no ecc dependence at fixed peri).

Pre-specified primary statistic: partial Spearman rho(sigma, ecc | r_peri, mass, r_half)
  on (a) full usable sample, (b) the non-adiabatic carrier subset.
PRIME CONFOUND = TIDAL HEATING: add a tidal proxy as an ADDITIONAL control and test
  whether the ecc-sigma correlation SURVIVES it or is explained by it.

Mass proxy: M_V (luminosity) -- NOT sigma-derived (avoids circularity; sigma is the
  response). Larger luminosity => more mass. We use -M_V (brighter = larger).
Normalized-sigma form: residual of sigma vs sqrt(M/r_half) virial baseline, using
  L (from M_V) as the mass proxy: sigma_pred ~ sqrt(L^p / r_half). We report the
  partial corr both on raw sigma and on this virial-deviation, both ways.

Anti-p-hack: run ONLY the pre-specified control set + the tidal control. Report
  coefficient, p-value, sign, N, and whether it survives tidal control. No fishing.
DO NOT git-push.
================================================================================
"""
import importlib.util, os, math
import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_HERE, "dwarf_ecc_sigma_pilot_data.py")
spec = importlib.util.spec_from_file_location("dwarf_data", _DATA)
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)

# ---- framework MW model (identical to pilot script) -------------------------
G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; pc=3.0857e16; km=1e3; A0=9.36e-11
M50=4.0e11*Msun; M100=7.0e11*Msun; ALPHA=math.log(M100/M50)/math.log(2.0)
def M_MW(r_m): return M50*(r_m/(50*kpc))**ALPHA
def omega_ext(r_kpc):
    r=r_kpc*kpc; return math.sqrt(G*M_MW(r)/r**3)
def omega_in(sig_kms, rh_pc): return (sig_kms*km)/(rh_pc*pc)

# ---- partial Spearman via rank-residual regression --------------------------
def partial_spearman(x, y, Z):
    """Spearman partial corr of x,y controlling for columns of Z (list of arrays).
    Rank-transform all, regress ranks of x and y on ranks of Z (+intercept),
    Pearson-correlate the residuals. p via t-dist on residual dof."""
    x=np.asarray(x,float); y=np.asarray(y,float)
    n=len(x)
    rx=stats.rankdata(x); ry=stats.rankdata(y)
    if Z:
        Zr=np.column_stack([stats.rankdata(np.asarray(z,float)) for z in Z])
        Zr=np.column_stack([np.ones(n), Zr])
    else:
        Zr=np.ones((n,1))
    # residualize
    def resid(v):
        beta,_,_,_=np.linalg.lstsq(Zr, v, rcond=None)
        return v - Zr@beta
    ex=resid(rx); ey=resid(ry)
    k=Zr.shape[1]                 # params used
    dof=n - k - 1                 # residual dof for the partial corr
    if dof < 1: return float('nan'), float('nan'), n, dof
    r=np.corrcoef(ex,ey)[0,1]
    if abs(r) >= 1.0: r=math.copysign(0.999999,r)
    t=r*math.sqrt(dof/(1-r*r))
    p=2*stats.t.sf(abs(t),dof)    # two-sided
    return r, p, n, dof

def spearman_simple(x,y):
    rho,p=stats.spearmanr(x,y); return rho,p

# ---- assemble the usable sample ---------------------------------------------
rows=[]
for d in dd.dwarfs:
    if d["sigma_los"] is None or d["ecc_lmc"] is None or d["r_half_pc"] is None:
        continue
    sig=d["sigma_los"]; ecc=d["ecc_lmc"]; rperi=d["r_peri_lmc"]; rh=d["r_half_pc"]
    MV=d["M_V"]
    if rperi is None or MV is None: continue
    win=omega_in(sig,rh); wext=omega_ext(rperi)
    y=wext/win
    L=10**(-0.4*MV)                          # luminosity proxy (mass proxy, NOT sigma-based)
    # virial-baseline-deviation sigma: log residual of sigma vs sqrt(L/r_half)
    # (we residualize in the regression, so just carry log L and log r_half as controls)
    rows.append(dict(name=d["name"], sig=sig, ecc=ecc, rperi=rperi, rh=rh, MV=MV,
                     L=L, y=y, conf=d["confidence"], carrier=d["carrier"],
                     regime=d["regime"]))

names=[r["name"] for r in rows]
sig =np.array([r["sig"]   for r in rows])
ecc =np.array([r["ecc"]   for r in rows])
peri=np.array([r["rperi"] for r in rows])
rh  =np.array([r["rh"]    for r in rows])
L   =np.array([r["L"]     for r in rows])
yv  =np.array([r["y"]     for r in rows])
logL=np.log10(L); logrh=np.log10(rh)

# virial-deviation sigma: residual of log sigma after log L, log r_half
def log_resid(target, controls):
    Zr=np.column_stack([np.ones(len(target))]+controls)
    beta,_,_,_=np.linalg.lstsq(Zr,target,rcond=None)
    return target - Zr@beta
sig_dev = log_resid(np.log10(sig), [logL, logrh])   # "hotter than virial baseline"

print("="*100)
print(" PRE-SPECIFIED PARTIAL-CORRELATION TEST  (a0=9.36e-11; framework MI; Pace+2022 data)")
print("="*100)
print(f"  N usable (sigma & ecc & peri & M_V & r_half) = {len(rows)}")
print(f"  predicted sign of partial rho(sigma, ecc | controls) = POSITIVE (H1) ; 0 = H0 (MG/CDM)")
print(f"  mass proxy = luminosity from M_V (NOT sigma-derived). tidal proxy = 1/r_peri.\n")

# Controls sets ----------------------------------------------------------------
# Pre-specified primary: control for pericenter, mass(L), r_half.
ctrl_primary = [peri, logL, logrh]
# Tidal control = ADD 1/r_peri as an explicit tidal-susceptibility proxy.
# (r_peri itself is already in primary; the killer-alternative tidal proxy is the
#  tidal field strength ~ M_MW(<peri)/peri^3, i.e. the Jacobi/tidal susceptibility.)
tidal_proxy = np.array([ M_MW(p*kpc)/(p*kpc)**3 for p in peri ])   # ~ d^2Phi/dr^2 scale
ctrl_tidal = [peri, logL, logrh, tidal_proxy]

def report(label, xresp, xname, controls_list, ctrl_label, mask=None):
    if mask is not None:
        xr=xresp[mask]; ec=ecc[mask]; ctl=[c[mask] for c in controls_list]; nm=np.array(names)[mask]
    else:
        xr=xresp; ec=ecc; ctl=controls_list; nm=np.array(names)
    r,p,n,dof=partial_spearman(ec, xr, ctl)
    print(f"  [{label}] partial Spearman rho({xname}, ecc | {ctrl_label})")
    print(f"       rho = {r:+.3f}   p = {p:.3f} (two-sided)   N = {n}   dof = {dof}")
    return r,p,n

print("-"*100)
print(" (A) FULL SAMPLE -- raw sigma")
print("-"*100)
ra,pa,_=report("A1", sig, "sigma", ctrl_primary, "r_peri, M_L, r_half")
print()
ra2,pa2,_=report("A2-TIDAL", sig, "sigma", ctrl_tidal, "r_peri, M_L, r_half, +TIDAL(Jacobi)")

print("\n"+"-"*100)
print(" (B) FULL SAMPLE -- virial-deviation sigma (log sigma residual vs sqrt(L/r_half))")
print("-"*100)
rb,pb,_=report("B1", sig_dev, "sig_dev", [peri], "r_peri  (mass+size already in dev)")
print()
rb2,pb2,_=report("B2-TIDAL", sig_dev, "sig_dev", [peri, tidal_proxy], "r_peri, +TIDAL(Jacobi)")

print("\n"+"-"*100)
print(" (C) CARRIER subset (non-adiabatic y>=0.8) vs sample -- N too small for partial;")
print("     report the carriers explicitly + simple ecc-sigma Spearman on diffuse subsets")
print("-"*100)
car_mask = yv>=0.8
print(f"  carriers (y>=0.8): {list(np.array(names)[car_mask])}  (N={car_mask.sum()})")
print("  -> N_carrier=2: a partial correlation is UNDEFINED (need >control_count+2). Reported as the")
print("     physics carriers, not a statistic. The test runs on the population.")
# diffuse subset: lowest internal-frequency half (by dens_proxy ~ sig^2/rh)
densp = sig**2/rh
diffuse_mask = densp <= np.median(densp)
print(f"\n  DIFFUSE half (dens_proxy <= median, the low-omega_in non-adiabatic-leaning carriers): "
      f"N={diffuse_mask.sum()}")
rc,pc,_=report("C1-diffuse", sig, "sigma", ctrl_primary, "r_peri, M_L, r_half", mask=diffuse_mask)
print()
rc2,pc2,_=report("C2-diffuse-TIDAL", sig, "sigma", ctrl_tidal,
                 "r_peri, M_L, r_half, +TIDAL", mask=diffuse_mask)

print("\n"+"="*100)
print(" RAW SIMPLE CORRELATIONS (no controls -- context only)")
print("="*100)
print(f"  Spearman(sigma, ecc) full   : rho={spearman_simple(sig,ecc)[0]:+.3f} p={spearman_simple(sig,ecc)[1]:.3f}")
print(f"  Spearman(sigma, r_peri) full: rho={spearman_simple(sig,peri)[0]:+.3f} p={spearman_simple(sig,peri)[1]:.3f}  (denser=closer? confound check)")
print(f"  Spearman(ecc, r_peri) full  : rho={spearman_simple(ecc,peri)[0]:+.3f} p={spearman_simple(ecc,peri)[1]:.3f}  (ecc-peri coupling)")
print(f"  Spearman(sigma, -M_V) full  : rho={spearman_simple(sig,-np.array([r['MV'] for r in rows]))[0]:+.3f}  (mass-sigma, expected +)")

print("\n"+"="*100)
print(" VERDICT (straight numbers)")
print("="*100)
print(f"  Primary partial rho(sigma,ecc | peri,mass,r_half), full N={len(rows)}: {ra:+.3f}  p={pa:.3f}")
print(f"  Survives +TIDAL(Jacobi) control                                : {ra2:+.3f}  p={pa2:.3f}")
print(f"  Virial-deviation form                                          : {rb:+.3f}  p={pb:.3f} (+tidal {rb2:+.3f} p={pb2:.3f})")
print(f"  Diffuse-half partial                                           : {rc:+.3f}  p={pc:.3f} (+tidal {rc2:+.3f} p={pc2:.3f})")
print("="*100)

# =============================================================================
# ROBUSTNESS: (1) no-LMC eccentricity; (2) does the framework's OWN predicted
# per-dwarf boost (which encodes y, the real carrier axis) correlate w/ residual
# sigma? -- the most generous framework-native test (uses y not ecc).
# =============================================================================
print("\n"+"#"*100)
print(" ROBUSTNESS / BOTH-WAYS")
print("#"*100)

# no-LMC ecc
ecc_nl=[]
ok_nl=[]
for r in rows:
    d=[x for x in dd.dwarfs if x["name"]==r["name"]][0]
    ecc_nl.append(d["ecc_nl"]); ok_nl.append(d["ecc_nl"] is not None)
ecc_nl=np.array([e if e is not None else np.nan for e in ecc_nl])
m=~np.isnan(ecc_nl)
r_nl,p_nl,n_nl,_=partial_spearman(ecc_nl[m], sig[m], [peri[m], logL[m], logrh[m]])
print(f"  no-LMC ecc, primary partial rho(sigma,ecc_nl|peri,M,rh): {r_nl:+.3f} p={p_nl:.3f} N={n_nl}")

# framework's OWN predicted carrier axis = y (omega_ext/omega_in). The framework
# says the boost tracks y, not ecc directly. Partial corr of sigma-deviation with y:
r_y,p_y,n_y,_=partial_spearman(yv, sig_dev, [peri])
print(f"  framework axis: partial rho(sig_dev, y | peri):           {r_y:+.3f} p={p_y:.3f} N={n_y}")
print(f"    (note: y is BUILT from sigma via omega_in=sigma/r_half -> ANTI-correlated by construction;")
print(f"     low-sigma diffuse dwarfs have HIGH y. This is why the carriers are COLD, not hot.)")

# Are the two carriers hot or cold for their mass/size? (virial-deviation sign)
print("\n  Per-dwarf virial-deviation (log sigma residual vs sqrt(L/r_half)); + = hotter than baseline:")
order=np.argsort(-yv)
for i in order[:6]:
    print(f"    {names[i]:18s} y={yv[i]:4.2f} ecc={ecc[i]:.2f} sigma={sig[i]:4.1f}  sig_dev={sig_dev[i]:+.3f}")
print("    ... (top-6 by y) ...")
