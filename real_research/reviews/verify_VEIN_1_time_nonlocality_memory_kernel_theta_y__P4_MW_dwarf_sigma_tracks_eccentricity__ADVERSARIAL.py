#!/usr/bin/env python3
r"""
ADVERSARIAL VERIFICATION of P4 -- "MW dwarf sigma tracks orbital eccentricity"
================================================================================
VEIN 1: TIME-NONLOCALITY / MEMORY KERNEL theta(y). Framework's inertia = a body's
NONLOCAL-IN-TIME response to the dS-Unruh horizon bath (Milgrom 2022 MI formulation,
a0=cH_Lambda/Z=9.36e-11). The MOND magnification of an internal frequency reads the
OTHER frequencies present, weighted by theta(omega_ext/omega_in); theta(1)=1,
theta decreasing, theta(0)~few, FORM UNKNOWN. MG's EFE is INSTANTANEOUS (internal
dynamics depend only on the momentary a_ex -- Milgrom verbatim).

POSIT P4 (win-flavored): at fixed pericenter + mass, a radial-PLUNGE diffuse MW dwarf
runs ~19-28% HOTTER than a circular-orbit one. The plunge drives omega_ext->omega_in
near peri (non-adiabatic), the kernel theta(y) sheds the adiabatic theta(0) external
loading, the dwarf drops deeper into deep-MOND.
  CLAIMED:  SIGN = theorem (theta decreasing => plunge HOTTER), magnitude theta-hostage.
  CLAIMED:  MG/AeST EFE instantaneous => exactly 0 sigma-vs-ecc at fixed peri => discriminator.

THE B4 DISCIPLINE (why B4 died): B4 hardcoded a sign (beta_MG>0) and used an ad-hoc
sigma^2~1/mu proxy. When the REAL energy-DF Jeans calc was done, MG gave beta~0 not >0.
RULE: every "forced/MG-impossible/distinctive" claim must be DERIVED with a real
dynamical calc, NOT an assumed sign or ad-hoc proxy.

So we DO NOT assume "theta(0)>theta(1) => plunge hotter." We INTEGRATE the actual
non-local kernel response over the real MW orbit for a matched-pericenter plunge-vs-
circular pair, build the dwarf's equilibrium sigma in each theory by the SAME virial
relation, and READ the sign off the dynamics. Four adversarial kills below.

Footing sealed: a0 = c*H_Lambda/Z = 9.36e-11 m/s^2. Framework's OWN interpolation
nu(y)=sqrt(1+1/y), mu_fw(x)=(sqrt(1+4x^2)-1)/(2x). McGaugh nu NEVER used.
Milgrom 2022 arXiv:2208.07073v3 theta forms (theta(1)=1, decreasing, theta(0)~few).
DO NOT git-push.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

c=2.998e8; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; pc=3.0857e16
A0=9.36e-11
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)

def th_rat(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)        # theta(0)=2
def th_e1(y):  y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)        # theta(0)=e
def th_e2(y):  y=np.abs(np.asarray(y,float)); return np.exp((1.0-y)/2.0)  # theta(0)=e^0.5
THETAS=[("rat 2/(1+y^2)",th_rat,2.0),("exp e^(1-y)",th_e1,np.e),("exp e^((1-y)/2)",th_e2,np.exp(0.5))]

print("="*100)
print(" ADVERSARIAL VERIFICATION of P4 (dwarf sigma vs eccentricity / non-adiabatic MI)")
print(" B4 discipline: DERIVE the sign from real kernel dynamics, do not assume theta(0)>theta(1)=>hotter.")
print("="*100)
print(f"  a0={A0:.3e} (sealed);  mu_fw inverse of nu=sqrt(1+1/y).  Milgrom theta forms carried.\n")

# ---- MW model + matched-pericenter plunge-vs-circular pair --------------------------
M50=4.0e11*Msun; M100=7.0e11*Msun; ALPHA=np.log(M100/M50)/np.log(2.0)
def M_MW(r): return M50*(r/(50*kpc))**ALPHA
def a_ext_of(r): return G*M_MW(r)/r**2
def om_ext_of(r): return np.sqrt(G*M_MW(r)/r**3)
def MW_potential(r):
    val,_=quad(lambda s: a_ext_of(s), r, 400*kpc, limit=200); return -val
def orbit(r_peri, r_apo, n=1500):
    Pp,Pa=MW_potential(r_peri),MW_potential(r_apo)
    L2=2*(Pa-Pp)/(1/r_peri**2-1/r_apo**2); E=Pp+L2/(2*r_peri**2)
    rs=np.linspace(r_peri,r_apo,n)
    vr2=2*(E-np.array([MW_potential(r) for r in rs]))-L2/rs**2
    vr=np.sqrt(np.maximum(vr2,0))
    with np.errstate(divide='ignore',invalid='ignore'):
        dt=np.gradient(rs)/np.where(vr>0,vr,np.nan)
    return rs,vr,dt

sig_fid=2.7e3; R_dwarf=1100.0*pc           # Crater II-ish (only regime reaching y~O(1))
om_in=sig_fid/R_dwarf; a_in=sig_fid**2/R_dwarf
print(f"  Diffuse dwarf (Crater-II-like): sigma_fid={sig_fid/1e3:.1f} km/s, R={R_dwarf/pc:.0f} pc")
print(f"    -> om_in={om_in:.3e}/s, a_in={a_in/A0:.3f} a0 (deep-MOND internal)\n")

r_peri=24.0*kpc
PL="PLUNGE  (peri=24, apo=140 kpc, ecc~0.71)"
CI="CIRCULAR(peri=24, apo=30  kpc, ecc~0.11)"
orbits={PL:(r_peri,140.0*kpc), CI:(r_peri,30.0*kpc)}

# ==== KILL 1: DERIVE the sign (history-integrated equilibrium loading) ===============
print("-"*100)
print(" KILL 1: DERIVE sigma_plunge/sigma_circular at MATCHED peri+mass (history-integrated kernel)")
print("-"*100)
print(r"""  Equilibrium sigma ~ sqrt(boost*a_in*R), boost=1/mu_fw(A_eff/a0),
   A_eff = a_in + < a_ex(t)*theta(om_ex(t)/om_in) >_orbit-time-average.
   A dwarf relaxes to the TIME-AVERAGED loading (t_relax >> the brief peri passage), so the
   equilibrium external term is the dt-weighted orbit average, NOT the pericenter instant.""")
def eff_terms(rs,dt,thf):
    a_ex=a_ext_of(rs); y=om_ext_of(rs)/om_in; w=dt/np.nansum(dt)
    return np.nansum(w*a_ex*thf(y)), np.nansum(w*a_ex), np.nansum(w*y)
print(f"\n  {'theta':16s} | {'orbit':42s} | {'<a_ex*th>/a0':>12} {'<a_ex>/a0':>10} {'<y>':>6} | {'sig/sig_fid':>11}")
print("  "+"-"*110)
S={}
for nm,thf,_ in THETAS:
    S[nm]={}
    for olbl,(rp,ra) in orbits.items():
        rs,_,dt=orbit(rp,ra)
        aex_th,aex_bar,ybar=eff_terms(rs,dt,thf)
        sig_eq=np.sqrt((1.0/mu_fw((a_in+aex_th)/A0))*a_in*R_dwarf); S[nm][olbl]=sig_eq
        print(f"  {nm:16s} | {olbl:42s} | {aex_th/A0:12.4f} {aex_bar/A0:10.4f} {ybar:6.3f} | {sig_eq/sig_fid:11.4f}")
print(f"\n  {'theta':16s} | sigma_PLUNGE/sigma_CIRCULAR (matched peri,mass) | claim +19..28% (>1)")
print("  "+"-"*80)
ratios=[]
for nm,_,_ in THETAS:
    rr=S[nm][PL]/S[nm][CI]; ratios.append(rr)
    print(f"  {nm:16s} | {rr:46.4f} | {'HOTTER (holds)' if rr>1 else 'COLDER (FAILS)'}")
plunge_hotter=all(r>1.0 for r in ratios)
print(f"\n  DERIVED SIGN: plunge {'HOTTER' if plunge_hotter else 'COLDER/MIXED'} (ratios {min(ratios):.3f}-{max(ratios):.3f}).")

# ==== KILL 1b: WHY -- which dwarf is more loaded, kinematics vs kernel ===============
print("\n"+"-"*100)
print(" KILL 1b: decompose -- which dwarf is MORE externally loaded in equilibrium?")
print("-"*100)
for olbl,(rp,ra) in orbits.items():
    rs,_,dt=orbit(rp,ra); w=dt/np.nansum(dt)
    print(f"  {olbl:42s}: <a_ex>/a0={np.nansum(w*a_ext_of(rs))/A0:.4f}  "
          f"frac-time within 1.3*r_peri = {np.nansum(w[rs<1.3*rp])*100:4.1f}%")
print(r"""  READ: circular dwarf stays near peri ~100% of time -> HIGH time-averaged a_ex; plunge dwarf is near
   peri only a few % of time -> LOW time-averaged a_ex. Equilibrium sigma responds to the TIME-AVERAGED
   loading, so "plunge less loaded => hotter" can be right -- but DOMINANTLY because the plunge spends
   time at large r (orbit kinematics), NOT because of the kernel theta(y). Isolate the theta-only part.""")

# ==== KILL 2 + KILL 3: a0-degeneracy + is MG REALLY 0? ==============================
print("\n"+"-"*100)
print(" KILL 2/3: does MG ALSO predict nonzero sigma-vs-ecc? + isolate the theta-ONLY (MG-impossible) part")
print("-"*100)
def sigma_eq(rp,ra,thf):
    rs,_,dt=orbit(rp,ra); w=dt/np.nansum(dt)
    a_ex=a_ext_of(rs); y=om_ext_of(rs)/om_in
    return np.sqrt((1.0/mu_fw((a_in+np.nansum(w*a_ex*thf(y)))/A0))*a_in*R_dwarf)
theta_one=lambda y: np.ones_like(np.asarray(y,float))   # MG-equivalent (momentary, no kernel)
sP=sigma_eq(*orbits[PL],theta_one); sC=sigma_eq(*orbits[CI],theta_one); mg_ratio=sP/sC
print(f"\n  (a) MG (instantaneous EFE, theta==1): sigma_PLUNGE/sigma_CIRCULAR = {mg_ratio:.4f}")
print(f"      != 1 => MG ALSO predicts nonzero sigma-vs-ecc at fixed PERICENTER (via orbit-averaged a_ex).")
print(f"      The 'MG exactly 0' claim holds only at fixed MOMENTARY a_ex (same instant), NOT fixed pericenter.")
print(f"\n  (b) theta-ONLY MG-impossible residual: MI(theta) vs MI(theta==1) at SAME orbit (same <a_ex>):")
print(f"  {'theta':16s} | {'PLUNGE sig(th)/sig(1)':>22} | {'CIRC sig(th)/sig(1)':>22} | diff(P/C)")
print("  "+"-"*80)
diffs=[]
for nm,thf,_ in THETAS:
    rP=sigma_eq(*orbits[PL],thf)/sigma_eq(*orbits[PL],theta_one)
    rC=sigma_eq(*orbits[CI],thf)/sigma_eq(*orbits[CI],theta_one)
    diffs.append(rP/rC)
    print(f"  {nm:16s} | {rP:22.4f} | {rC:22.4f} | {rP/rC:.4f}")
print(f"\n  theta-ONLY differential (plunge/circ), the part NO a0 can absorb: {min(diffs):.4f}-{max(diffs):.4f}")
print(f"  (~{abs(np.mean(diffs)-1)*100:.1f}% -- compare claimed headline +19-28%)")
print(f"\n  (c) a0-DEGENERACY (single PLUNGE orbit): refit a single MG a0 to MI(theta) sigma along orbit:")
rs,_,dt=orbit(*orbits[PL]); w=dt/np.nansum(dt); a_ex=a_ext_of(rs); y=om_ext_of(rs)/om_in
for nm,thf,_ in THETAS:
    sig_mi=np.sqrt(np.array([1.0/mu_fw((a_in+ae*thf(yy))/A0) for ae,yy in zip(a_ex,y)])*a_in*R_dwarf)
    def mis(la0):
        a0u=np.exp(la0); s=np.sqrt(np.array([1.0/mu_fw((a_in+ae)/a0u) for ae in a_ex])*a_in*R_dwarf)
        return np.nansum(w*(np.log(s)-np.log(sig_mi))**2)
    rfit=minimize_scalar(mis,bounds=(np.log(A0/30),np.log(A0*30)),method='bounded'); a0f=np.exp(rfit.x)
    s_fit=np.sqrt(np.array([1.0/mu_fw((a_in+ae)/a0f) for ae in a_ex])*a_in*R_dwarf)
    print(f"     {nm:16s}: best MG a0={a0f/A0:.3f}a0, residual along orbit = {np.nansum(w*np.abs(s_fit/sig_mi-1))*100:.2f}%  (->0 => a0-degenerate)")

# ==== KILL 4: empirical + self-consistency ==========================================
print("\n"+"-"*100)
print(" KILL 4: empirical (banked Pace+2022) + internal self-consistency of the SIGN claim")
print("-"*100)
import importlib.util, os
_HERE=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("dd",os.path.join(_HERE,"dwarf_ecc_sigma_pilot_data.py"))
dd=importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
from scipy import stats
rows=[d for d in dd.dwarfs if d["sigma_los"] and d["ecc_lmc"] and d["r_half_pc"] and d["M_V"] is not None]
sig=np.array([d["sigma_los"] for d in rows]); ecc=np.array([d["ecc_lmc"] for d in rows])
peri=np.array([d["r_peri_lmc"] for d in rows]); rh=np.array([d["r_half_pc"] for d in rows])
MV=np.array([d["M_V"] for d in rows]); L=10**(-0.4*MV)
def pspear(x,y,Z):
    n=len(x); Zr=np.column_stack([np.ones(n)]+[stats.rankdata(z) for z in Z])
    res=lambda v: v-Zr@np.linalg.lstsq(Zr,v,rcond=None)[0]
    ex,ey=res(stats.rankdata(x)),res(stats.rankdata(y)); dof=n-Zr.shape[1]-1
    r=np.corrcoef(ex,ey)[0,1]; t=r*np.sqrt(dof/(1-r*r)); return r,2*stats.t.sf(abs(t),dof),n
r,p,n=pspear(ecc,sig,[peri,np.log10(L),np.log10(rh)])
print(f"  Banked partial Spearman rho(sigma, ecc | peri, mass, r_half), N={n}: rho={r:+.3f} p={p:.3f}")
print(f"    predicted POSITIVE; OBSERVED {'POSITIVE' if r>0 else 'NEGATIVE'} => "
      f"{'consistent' if r>0 else 'WRONG-SIGNED'} (null, p>0.05).")
logL=np.log10(L); logrh=np.log10(rh); Zr=np.column_stack([np.ones(len(rows)),logL,logrh])
sig_dev=np.log10(sig)-Zr@np.linalg.lstsq(Zr,np.log10(sig),rcond=None)[0]
print(f"\n  Framework's OWN carriers (only y>=0.8 dwarfs) are high-ecc PLUNGERS:")
for i,d in enumerate(rows):
    if d["name"] in ("Crater II","Antlia II"):
        print(f"    {d['name']:12s}: ecc={d['ecc_lmc']:.2f} sig_dev={sig_dev[i]:+.3f} => "
              f"{'HOT' if sig_dev[i]>0 else 'COLD'} for its mass/size")
print(r"""  SELF-CONSISTENCY PROBLEM: the framework's OWN carriers are high-ecc plungers yet both are COLD --
   the OPPOSITE of "plunge=>hot". The defense (y built from sigma => low-sigma dwarfs high-y => carriers
   cold by construction) ALSO removes the predictive content: if "diffuse carrier" and "cold" are the
   same selection, the sigma response cannot be independently confirmed on these objects.""")

# ==== VERDICT =======================================================================
print("\n"+"="*100)
print(" VERDICT (both ways, no thumb on the scale)")
print("="*100)
print(f"""  KILL 1 (DERIVED?): 'plunge HOTTER at matched peri' comes out {'POSITIVE' if plunge_hotter else 'MIXED/NEGATIVE'} from the
     history-integrated kernel, but KILL 1b shows it is DOMINATED by orbit kinematics (plunge spends
     most time at large r, low a_ex), NOT by theta(y). The theta-ONLY (genuinely MG-impossible)
     differential is only {min(diffs):.3f}-{max(diffs):.3f} (~{abs(np.mean(diffs)-1)*100:.1f}%), FAR below the headline "+19-28%".
  KILL 3 (MG=0?): FALSE as stated. At fixed PERICENTER (not fixed momentary a_ex) MG ALSO predicts
     nonzero sigma-vs-ecc (ratio {mg_ratio:.3f}) via orbit-averaged a_ex. Both "+19-28%" and "MG exactly 0"
     silently assume the dwarf feels the INSTANTANEOUS peri loading; equilibrium dwarfs feel the
     TIME-AVERAGE, where MG is not zero and the kernel part is small.
  KILL 2 (a0-degenerate): a single dwarf's single orbit IS a0-degenerate (residual ~few %); the only
     non-degenerate content is RELATIONAL at matched MOMENTARY a_ex -- which "fixed pericenter" does NOT
     deliver. (Reconfirms the banked member_MI_nonadiabatic_plunge.py cross-cutting finding.)
  KILL 4 (empirical/self-consistency): banked pilot rho=-0.196 WRONG-SIGNED null (p=0.40); the
     framework's OWN two carriers are high-ecc plungers that are self-consistently COLD.

  NET: the WIN-FLAVORED P4 framing ("+19-28% hotter, SIGN=theorem, MG exactly 0 at fixed pericenter")
  DIES on its own terms -- it conflates the instantaneous-peri loading with the equilibrium time-average.
  Done honestly: (i) the theta-only differential is ~few %, not 19-28%; (ii) MG is NOT exactly zero at
  fixed pericenter; (iii) the per-object effect is a0-degenerate; (iv) the empirical sign is wrong and
  the carriers are self-consistently cold. What SURVIVES is the WEAKER, ALREADY-BANKED relational
  statement (matched MOMENTARY a_ex, cross-object theta-tag spread), NOT a sigma-vs-eccentricity
  correlation at fixed pericenter. P4 as a win is KILLED; the relational core is founded-not-derived.""")
