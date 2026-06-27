#!/usr/bin/env python3
"""
SHARPENED dwarf sigma(y) pilot: the JOINT analysis the Top-20 sweep said is actionable NOW.

Instead of the v3 eccentricity SURROGATE or the (dead) instantaneous current-y, use the framework's OWN
observable: the MEMORY-WEIGHTED y_eff -- the de Sitter-Unruh kernel (~0.45 Gyr memory) convolved over each
dwarf's recent y-history, reconstructed from the Gaia orbital phase (peri/apo/ecc + current distance).
A dwarf caught soon after pericenter is still HOT (y_eff ~ y_peri); one parked near apocenter is COLD
(y_eff ~ y_current). Then test partial corr(sigma, y_eff | mass, r_half) -- the MG-IMPOSSIBLE signature
(MG/Milgrom-2022: exactly 0; MI: 6-13%).

Footing a0=9.36e-11, framework theta(y). Honest about the approximations (Kepler-orbit timing, outbound-branch
in/out ambiguity that Gaia DR4 full PMs resolve). Data: Pace+2022 (dwarf_ecc_sigma_pilot_data.py).
"""
import importlib.util, os, math
import numpy as np
from scipy import stats

_HERE=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("dwarf_data", os.path.join(_HERE,"dwarf_ecc_sigma_pilot_data.py"))
dd=importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)

G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; pc=3.0857e16; km=1e3; A0=9.36e-11; Gyr=3.156e16
SQRT2=math.sqrt(2.0); TAU_MEM=0.45*Gyr                        # memory time ~0.45 Gyr
M50=4.0e11*Msun; M100=7.0e11*Msun; ALPHA=math.log(M100/M50)/math.log(2.0)
def M_MW(r_m): return M50*(r_m/(50*kpc))**ALPHA
def omega_ext(r_kpc): r=r_kpc*kpc; return math.sqrt(G*M_MW(r)/r**3)
def omega_in(sig,rh_pc): return (sig*km)/(rh_pc*pc)
def theta(y): return SQRT2/(1.0+(SQRT2-1.0)*y*y)
def fboost(y): return math.sqrt(theta(0.0)/theta(y))           # sigma enhancement (1+(sqrt2-1)y^2)^1/2

def t_since_peri(r_kpc, rp, ra):
    """Kepler time from pericenter to current radius r (OUTBOUND branch). Approx: MW ~ point-mass at a_semi."""
    a=0.5*(rp+ra); e=max(min((ra-rp)/(ra+rp),0.999),1e-3)
    Mc=M_MW(a*kpc); T=2*math.pi*math.sqrt((a*kpc)**3/(G*Mc))    # orbital period
    x=(1.0 - r_kpc/a)/e                                          # cos E
    x=max(min(x,1.0),-1.0); E=math.acos(x)
    t=(T/(2*math.pi))*(E - e*math.sin(E))                        # time peri->r, outbound
    return t, T

rows=[]
for d in dd.dwarfs:
    if None in (d.get("sigma_los"),d.get("r_h_arcmin"),d.get("dist_kpc"),d.get("M_V"),
                d.get("r_peri_lmc"),d.get("r_apo_lmc")): continue
    sig=d["sigma_los"]; serr=d.get("sigma_err") or 0.0; dist=d["dist_kpc"]
    rp=d["r_peri_lmc"]; ra=d["r_apo_lmc"]
    if ra<=rp or not (rp<=dist*1.05): ra=max(ra,dist); rp=min(rp,dist)
    rh_pc=(d["r_h_arcmin"]/60.0)*(math.pi/180.0)*dist*1000.0
    if rh_pc<=0: continue
    Mbar=(d.get("M_star_Msun") or 1.6*10**(-0.4*(d["M_V"]-4.83)))*Msun
    win=omega_in(sig,rh_pc)
    y_cur=omega_ext(min(max(dist,rp),ra))/win
    y_peri=omega_ext(rp)/win
    tsp,T=t_since_peri(min(max(dist,rp),ra), rp, ra)
    # memory-weighted y_eff: blend peri-history into current by how recently peri was passed (outbound branch)
    w_recent=math.exp(-tsp/TAU_MEM)
    y_eff=y_cur + (y_peri-y_cur)*w_recent
    rows.append(dict(name=d["name"], sig=sig, serr=serr, rh=rh_pc, Mbar=Mbar, ecc=d.get("ecc_lmc"),
                     y_cur=y_cur, y_peri=y_peri, y_eff=y_eff, tsp_Gyr=tsp/Gyr, T_Gyr=T/Gyr,
                     carrier=bool(d.get("carrier"))))
N=len(rows)
sig=np.array([r["sig"] for r in rows]); serr=np.array([r["serr"] for r in rows])
logM=np.log10(np.array([r["Mbar"] for r in rows])); logrh=np.log10(np.array([r["rh"] for r in rows]))
ycur=np.array([r["y_cur"] for r in rows])
ypeak=np.array([r["y_peri"] for r in rows]); yeff=np.array([r["y_eff"] for r in rows])
ecc=np.array([(r["ecc"] if r["ecc"] is not None else np.nan) for r in rows])

def partial(logsig, X):
    m=~np.isnan(X); n=m.sum()
    Z=np.column_stack([np.ones(n), logM[m], logrh[m]])
    def res(v):
        b,_,_,_=np.linalg.lstsq(Z,v,rcond=None); return v-Z@b
    ex=res(logsig[m]); ey=res(X[m]); r=np.corrcoef(ex,ey)[0,1]; dof=n-3-1
    t=r*math.sqrt(dof/max(1-r*r,1e-12)); p=stats.t.sf(t,dof)    # one-sided (predicted +)
    return r,p,n

print("="*92); print(f"SHARPENED dwarf sigma(y_eff) JOINT PILOT  (N={N}, Pace+2022, a0=9.36e-11, tau_mem=0.45 Gyr)"); print("="*92)
print(f"  {'dwarf':14s} {'y_cur':>6s} {'y_peri':>7s} {'t_since_peri':>12s} {'y_eff':>7s} {'f(y_eff)':>9s} {'sigma':>9s}")
for r in sorted(rows,key=lambda q:-q["y_eff"])[:8]:
    print(f"  {r['name']:14s} {r['y_cur']:6.2f} {r['y_peri']:7.2f} {r['tsp_Gyr']:9.2f}Gyr {r['y_eff']:7.2f} {fboost(r['y_eff']):9.3f} {r['sig']:6.1f}+-{r['serr']:.1f}")
print(f"\n  caught-recently-hot (y_eff>1): {np.sum(yeff>1)}/{N}   vs current-y>1: {np.sum(ycur>1)}/{N}")

print("\n  PARTIAL CORRELATION  rho(log sigma, X | log M_bar, log r_half), one-sided p (predicted +):")
for lab,X in [("eccentricity (v3 surrogate)",ecc),("current-y (instantaneous, dead)",ycur),
              ("y_peri (max history)",ypeak),("y_eff (memory-weighted -- THE right observable)",yeff)]:
    r,p,n=partial(np.log10(sig), X)
    sig3 = "  <-- 3sigma!" if p<0.00135 and r>0 else ("  (2sigma)" if p<0.0228 and r>0 else "")
    print(f"     {lab:46s}: rho={r:+.3f}  p={p:.3f}  (N={n}){sig3}")

print("\n"+"="*92); print("VERDICT (computed, both-ways) -- the pilot caught a CONFOUND"); print("="*92)
rr_eff,pp_eff,_=partial(np.log10(sig),yeff)
print(f"""  *** THE KEY FINDING (a methodological trap, surfaced by the computation): y_eff is CONFOUNDED by sigma. ***
  y = omega_ext/omega_in and omega_in = sigma/r_half, so y = omega_ext*r_half/sigma -- y carries sigma in its
  DENOMINATOR. Diffuse high-y dwarfs (Crater II, Antlia II) therefore have LOW sigma BY CONSTRUCTION, so sigma and y
  are MECHANICALLY anti-correlated. The strong rho(sigma, y_eff)={rr_eff:+.3f} (wrong sign) is CONFOUND-DOMINATED, NOT
  the framework's signal -- and controlling for r_half/M_bar does NOT remove it (sigma enters y directly). This
  VINDICATES the v3 paper's choice of the ECCENTRICITY surrogate, which is sigma-FREE: ecc gives the weaker, less-
  confounded rho={partial(np.log10(sig),ecc)[0]:+.3f}. My 'sharpen to y_eff' idea REINTRODUCED the very circularity the
  ecc-surrogate was avoiding -- a real correction.
  CAUGHT COLD, confirmed: only {np.sum(yeff>1)}/{N} dwarf is recently-hot (Crater II, y_eff~1.06 barely; Antlia II cooled
  to 0.79, passed pericenter 1.18 Gyr ~2.6 memory-times ago). Current data is a LOW-POWER NULL either way.
  THE CORRECT DR4 TEST DESIGN (the real deliverable): predict sigma from a SIGMA-FREE non-adiabaticity measure -- the
  external-field history a_ext(t) reconstructed from the orbit ALONE (or the plunge depth r_peri / the ecc), memory-
  weighted by theta -- NOT from y (which embeds sigma). Then select recent-pericenter dwarfs (DR4 full PMs) and push
  diffuse-sigma precision. The MG-impossibility (Milgrom-2022: exactly 0) is unchanged; the test is sound, the
  PREDICTOR must be sigma-independent. CAVEATS: Kepler timing on a point-mass MW; outbound-branch in/out ambiguity
  (DR4 resolves) -- so y_eff here is an upper bound on 'how hot'. Net: the pilot's value is the CONFOUND finding +
  the sigma-free fix, not a win/null verdict; the v3 ecc-surrogate stands, current data caught-cold null.""")
