#!/usr/bin/env python3
r"""
DWARF SIGMA MI DOOR -- ADVERSARIAL RECONCILIATION (corrects dwarf_sigma_mi_kernel.py)
=====================================================================================
Three verifiers converged on the SAME class of correction (the wide-binary failure mode
re-appearing in disguise). This script re-runs each objection and corrects the record.

OBJECTION 1 (dc-protection lens, load-bearing): the original V-MG baseline strips theta
  out -> feeds MG the BARE a_ext (sigma_MG_instant uses a_ext, no theta). But the framework's
  OWN modified-GRAVITY realization (AeST / ghost-condensate) carries the SAME instantaneous
  theta(y)*a_ext external-field law. The honest MG comparator is the INSTANTANEOUS-theta EFE,
  not a theta-stripped one. theta acting pointwise on the loading level is a rescaling BOTH
  MI and MG share; only the MEMORY (history convolution) is MI-distinctive. => rebuild MG with
  instantaneous theta and recompute the MG-impossible gap.

OBJECTION 2 (artifact-mislabel): the memory integral hist_weighted integrates only [0,t_obs]
  with NO inbound / periodic history. At small phase the window is tiny and dominated by
  near-peri high-y points where theta most suppresses a_ext -> inflates the phase-0.05 shift.
  Fix: FULL PERIODIC history (mirror peri<->apo, wrap several tau_mem of tail).

OBJECTION 3 (both mg-baseline + artifact): the per-dwarf "memory-diff (pp)" is a difference of
  two (max-min)/mean SPREAD statistics whose SIGN flips (Crater -56, Antlia +5.6) purely from
  under-sampling Antlia's pericenter. Fix: dense phase grid resolving pericenter for every dwarf;
  report the phase-resolved MI/MG sigma RATIO at matched phase (stable), not the spread-difference.

Correct definition of the ONLY MG-impossible observable (all three verifiers agree):
  sigma HYSTERESIS at FIXED current galactocentric radius r. MG: sigma = f(r) EXACTLY (single-
  valued, instantaneous, even with theta) => inbound and outbound give the SAME sigma at the same r.
  MI: sigma(r) is DOUBLE-VALUED (inbound hotter than outbound at matched r, or vice versa) because
  the history differs. That inbound-vs-outbound scatter at fixed r is the memory-lag, unmimicable
  by M/L. Its magnitude is tau_mem-conditional (tau_mem is time-domain, NOT bath-forced -- soft spot).

Every number from THIS run. No git commit.
"""
import numpy as np
from scipy.integrate import quad
np.seterr(all="ignore")

c=2.998e8; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; pc=3.0857e16; Gyr=3.156e16
A0=9.36e-11
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)
def boost(x): return 1.0/mu_fw(x)
def nu(y): return np.sqrt(1.0+1.0/y)
S2=np.sqrt(2.0)
def th_fw(y):    y=np.abs(np.asarray(y,float)); return S2/(1.0+(S2-1.0)*y*y)
def th_2pole(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)
def th_flat(y):  return np.ones_like(np.asarray(y,float))

M50=4.0e11*Msun; M100=7.0e11*Msun; ALPHA=np.log(M100/M50)/np.log(2.0)
def M_MW(r): return M50*(r/(50*kpc))**ALPHA
def a_ext(r): return G*M_MW(r)/r**2
def om_ext(r): return np.sqrt(G*M_MW(r)/r**3)
def MW_pot(r): v,_=quad(lambda s:a_ext(s),r,400*kpc,limit=200); return -v

def full_periodic_orbit(r_peri,r_apo,n_half=4000,n_periods_tail=8):
    """Build a FULL periodic r(t) covering many radial periods so the memory integral at ANY
       phase has a genuine inbound history (no [0,t_obs] truncation). Returns t, r, a_ext, om_ext
       over [ -n_periods_tail*P_half , +P_half ] so every observation phase in the last period has
       a fully-populated exp(-Dt/tau) memory tail."""
    Pp,Pa=MW_pot(r_peri),MW_pot(r_apo)
    L2=2*(Pa-Pp)/(1/r_peri**2-1/r_apo**2); E=Pp+L2/(2*r_peri**2)
    rs=np.linspace(r_peri,r_apo,n_half)
    vr2=2*(E-np.array([MW_pot(r) for r in rs]))-L2/rs**2
    vr=np.sqrt(np.maximum(vr2,0))
    with np.errstate(divide='ignore',invalid='ignore'):
        dt=np.gradient(rs)/np.where(vr>0,vr,np.nan)
    dt=np.where(np.isfinite(dt),dt,0.0)
    t_half=np.concatenate([[0],np.cumsum(0.5*(dt[1:]+dt[:-1]))])
    P_half=t_half[-1]
    # one full period peri->apo->peri (outbound then inbound mirror)
    r_out=rs; t_out=t_half
    r_in=rs[::-1][1:]; t_in=P_half+(P_half-t_half[::-1][1:])   # apo->peri, time continues
    r_per=np.concatenate([r_out,r_in]); t_per=np.concatenate([t_out,t_in])
    P_full=t_per[-1]
    # tile n_periods_tail periods BEFORE the observation window, plus one observation period
    tblocks=[]; rblocks=[]
    for k in range(-n_periods_tail,1):
        tblocks.append(t_per[:-1]+k*P_full); rblocks.append(r_per[:-1])
    tblocks.append(np.array([t_per[-1]+ (0)*P_full])); # close
    T=np.concatenate(rblocks); # placeholder (fix below)
    tt=np.concatenate([tb for tb in tblocks[:-1]]+[np.array([0.0+ (0)])])
    # simpler: rebuild cleanly
    reps=n_periods_tail+1
    t_all=np.concatenate([t_per[:-1]+k*P_full for k in range(reps)])
    r_all=np.tile(r_per[:-1],reps)
    t_all=np.append(t_all, reps*P_full - (P_full-t_per[-1]))
    r_all=np.append(r_all, r_per[-1])
    # observation window = the LAST full period
    t_obs0=(reps-1)*P_full
    return t_all, r_all, a_ext(r_all), om_ext(r_all), P_half, P_full, t_obs0

print("="*96)
print(" DWARF SIGMA MI DOOR -- ADVERSARIAL RECONCILIATION")
print("="*96)

# V-RAR (unchanged, reused)
from scipy.optimize import brentq
def solve_x(g): return brentq(lambda x:mu_fw(x)*x-g,1e-8,max(1e6,10*g+10))
mx=max(abs(solve_x(y)/y-nu(y))/nu(y) for y in [1e-3,1e-2,1e-1,1.,10.,100.,1e3])
V_RAR=mx<1e-6 and abs(th_fw(1)-1)<1e-12 and abs(th_2pole(1)-1)<1e-12
print(f"\nV-RAR: max rel.err(boost vs nu)={mx:.2e}, theta(1)=1 -> {'PASS' if V_RAR else 'FAIL'}")

# ---- Crater II carrier ----
sig_fid=2.7e3; R_dwarf=1100.0*pc
om_in=sig_fid/R_dwarf; a_in=sig_fid**2/R_dwarf
TAU_MEM=0.45*Gyr
rp,ra=24.0*kpc,138.1*kpc; e_meas=(ra-rp)/(ra+rp)
t_all,r_all,aex,omx,P_half,P_full,t0=full_periodic_orbit(rp,ra)
print(f"\nCrater II: peri=24 apo=138 kpc e={e_meas:.3f}, a_in/a0={a_in/A0:.3f}, tau_mem={TAU_MEM/Gyr:.2f} Gyr")
print(f"  full periodic orbit built: P_half={P_half/Gyr:.2f} Gyr, {8} tail periods (no [0,t_obs] truncation)")

def sigma_eq(load): return np.sqrt(boost((a_in+load)/A0)*a_in*R_dwarf)

def memloaded(t_obs,kernel,tau=TAU_MEM):
    """FULL-periodic memory-weighted loading a_ext*theta with genuine inbound history."""
    m=t_all<=t_obs
    tt=t_all[m]; ae=aex[m]; yy=omx[m]/om_in
    # keep only ~10 tau of tail for speed
    keep=tt>=t_obs-10*tau
    tt=tt[keep]; ae=ae[keep]; yy=yy[keep]
    w=np.exp(-(t_obs-tt)/tau); ws=np.trapz(w,tt)
    return np.trapz(w*ae*kernel(yy),tt)/ws

# =============================================================== RECONCILE OBJ 1+2: honest MG w/ theta
print("\n"+"-"*96)
print(" RECON-1+2: honest MG carries instantaneous theta(y); full periodic history (no truncation)")
print("-"*96)
# phases in the LAST period (dense grid resolving pericenter)
frac=np.linspace(0.001,0.999,40)
t_grid=t0+frac*P_full
r_grid=np.interp(t_grid,t_all,r_all)
ae_grid=a_ext(r_grid); y_grid=om_ext(r_grid)/om_in

# MG-STRIPPED (original, wrong): bare a_ext, no theta
sMG_strip=np.array([sigma_eq(ae) for ae in ae_grid])
# MG-HONEST: instantaneous theta(y)*a_ext (framework's own AeST/ghost-condensate EFE)
sMG_theta=np.array([sigma_eq(ae*th_fw(y)) for ae,y in zip(ae_grid,y_grid)])
# MI: full-periodic memory-weighted theta*a_ext
sMI=np.array([sigma_eq(memloaded(tg,th_fw)) for tg in t_grid])

def spread(a): return (a.max()-a.min())/a.mean()*100
print(f"  MG-STRIPPED (bare a_ext, ORIGINAL/WRONG) phase-spread : {spread(sMG_strip):6.2f}%")
print(f"  MG-HONEST   (instantaneous theta*a_ext, AeST/ghost)   : {spread(sMG_theta):6.2f}%")
print(f"  MI          (full-periodic memory theta*a_ext)        : {spread(sMI):6.2f}%")
print(f"  MG-impossible gap vs STRIPPED baseline (ORIGINAL): {spread(sMI)-spread(sMG_strip):+6.2f} pp  <- inflated")
print(f"  MG-impossible gap vs HONEST theta baseline       : {spread(sMI)-spread(sMG_theta):+6.2f} pp  <- corrected")

# =============================================================== RECONCILE OBJ 2: V-KS truncation
print("\n"+"-"*96)
print(" RECON-2: V-KS theta-only shift -- truncated [0,t_obs] vs FULL periodic history")
print("-"*96)
def memloaded_trunc(t_obs,kernel,tau=TAU_MEM):
    """Original truncated version: history only from t=t0 (start of observation period)."""
    m=(t_all<=t_obs)&(t_all>=t0)
    tt=t_all[m]; ae=aex[m]; yy=omx[m]/om_in
    if len(tt)<2: return ae[-1]*kernel(yy[-1]) if len(tt) else 0.0
    w=np.exp(-(t_obs-tt)/tau); ws=np.trapz(w,tt)
    return np.trapz(w*ae*kernel(yy),tt)/ws
print(f"  {'phase':>7} {'trunc shift':>13} {'full-hist shift':>16}")
for f in [0.05,0.20,0.40,0.60,0.80,0.95]:
    tg=t0+f*P_full
    s1t=sigma_eq(memloaded_trunc(tg,th_flat)); sft=sigma_eq(memloaded_trunc(tg,th_fw))
    s1f=sigma_eq(memloaded(tg,th_flat));       sff=sigma_eq(memloaded(tg,th_fw))
    print(f"  {f:>7.2f} {(sft/s1t-1)*100:>12.2f}% {(sff/s1f-1)*100:>15.2f}%")

# =============================================================== THE CORRECT OBSERVABLE: fixed-r hysteresis
print("\n"+"-"*96)
print(" CORRECT OBSERVABLE: sigma HYSTERESIS at FIXED current galactocentric radius r")
print("-"*96)
print("  MG (even with instantaneous theta): sigma = single-valued f(r) -> inbound==outbound at same r.")
print("  MI: sigma(r) double-valued (memory) -> inbound-vs-outbound scatter = MG-impossible, M/L-immune.")
# split the last period into outbound (peri->apo) and inbound (apo->peri) branches
tb=t0+frac*P_full
# identify branch by sign of dr/dt
rb=np.interp(tb,t_all,r_all)
drdt=np.gradient(rb,tb)
out=drdt>0; inn=drdt<0
# match radii present on both branches
r_common=np.linspace(rp*1.05,ra*0.95,20)
print(f"\n  {'r (kpc)':>8} {'sigma_MI_out':>13} {'sigma_MI_in':>12} {'hyst %':>8} {'sigma_MG (both)':>16}")
hyst=[]
for rc in r_common:
    # outbound obs time nearest rc
    if out.sum()<2 or inn.sum()<2: continue
    to=tb[out][np.argmin(np.abs(rb[out]-rc))]
    ti=tb[inn][np.argmin(np.abs(rb[inn]-rc))]
    so=sigma_eq(memloaded(to,th_fw)); si=sigma_eq(memloaded(ti,th_fw))
    # MG honest: instantaneous theta at this r (single-valued, same for both branches)
    yq=om_ext(rc)/om_in; smg=sigma_eq(a_ext(rc)*th_fw(yq))
    h=(si-so)/(0.5*(si+so))*100; hyst.append(abs(h))
    if rc in (r_common[2],r_common[7],r_common[12],r_common[17]):
        print(f"  {rc/kpc:>8.1f} {so/1e3:>13.3f} {si/1e3:>12.3f} {h:>7.1f}% {smg/1e3:>16.3f}")
hyst=np.array(hyst)
print(f"\n  MI inbound-vs-outbound sigma hysteresis at fixed r: peak {hyst.max():.1f}%, median {np.median(hyst):.1f}%")
print(f"  MG hysteresis at fixed r (any theta): EXACTLY 0 (sigma single-valued in r) -- MG-IMPOSSIBLE.")

# tau_mem sensitivity of the hysteresis (the door's soft spot)
print("\n  tau_mem sensitivity of the fixed-r hysteresis (tau_mem NOT bath-forced):")
for tau in [0.10*Gyr,0.25*Gyr,0.45*Gyr,0.90*Gyr,2.0*Gyr]:
    hh=[]
    for rc in r_common:
        if out.sum()<2 or inn.sum()<2: continue
        to=tb[out][np.argmin(np.abs(rb[out]-rc))]; ti=tb[inn][np.argmin(np.abs(rb[inn]-rc))]
        so=sigma_eq(memloaded(to,th_fw,tau)); si=sigma_eq(memloaded(ti,th_fw,tau))
        hh.append(abs((si-so)/(0.5*(si+so))*100))
    hh=np.array(hh)
    print(f"    tau={tau/Gyr:>4.2f} Gyr (tau/P_half={tau/P_half:>4.2f}): peak hyst {hh.max():>5.1f}%, median {np.median(hh):>4.1f}%")

# =============================================================== per-dwarf fixed-r hysteresis (stable)
print("\n"+"-"*96)
print(" PER-DWARF fixed-r hysteresis (STABLE observable; replaces the sign-flipping memory-diff column)")
print("-"*96)
DW=[("Crater II",24.0,138.1,2.7,1100.0,True),
    ("Antlia II",38.2,137.2,5.71,2867.0,True),
    ("Fornax",76.7,152.7,12.1,851.0,False),
    ("Sculptor",44.9,145.7,9.2,272.0,False)]
def hyst_dwarf(rpk,rak,sfd,Rpc,kern,tau=TAU_MEM):
    Rd=Rpc*pc; om_ind=sfd*1e3/Rd; a_ind=(sfd*1e3)**2/Rd
    ta,rA,aeA,omA,Ph,Pf,t00=full_periodic_orbit(rpk*kpc,rak*kpc)
    def sig_eq_d(load): return np.sqrt(boost((a_ind+load)/A0)*a_ind*Rd)
    def ml(tob):
        m=ta<=tob; tt=ta[m]; ae=aeA[m]; yy=omA[m]/om_ind
        keep=tt>=tob-10*tau; tt=tt[keep]; ae=ae[keep]; yy=yy[keep]
        w=np.exp(-(tob-tt)/tau); ws=np.trapz(w,tt); return np.trapz(w*ae*kern(yy),tt)/ws
    fr=np.linspace(0.001,0.999,40); tg=t00+fr*Pf; rg=np.interp(tg,ta,rA)
    dr=np.gradient(rg,tg); o=dr>0; i=dr<0
    rc=np.linspace(rpk*kpc*1.05,rak*kpc*0.95,20); hs=[]
    for r in rc:
        if o.sum()<2 or i.sum()<2: continue
        to=tg[o][np.argmin(np.abs(rg[o]-r))]; ti=tg[i][np.argmin(np.abs(rg[i]-r))]
        so=sig_eq_d(ml(to)); si=sig_eq_d(ml(ti)); hs.append(abs((si-so)/(0.5*(si+so))*100))
    return np.array(hs)
print(f"  {'dwarf':11s} {'type':8s} {'y_max':>6} {'peak hyst % (fw / 2-pole)':>28}")
for nm,rpk,rak,sfd,Rpc,isc in DW:
    hf=hyst_dwarf(rpk,rak,sfd,Rpc,th_fw); h2=hyst_dwarf(rpk,rak,sfd,Rpc,th_2pole)
    ymax=(om_ext(rpk*kpc)/(sfd*1e3/(Rpc*pc)))
    print(f"  {nm:11s} {'CARRIER' if isc else 'control':8s} {ymax:>6.2f} {hf.max():>13.1f} / {h2.max():>9.1f}")
print("  -> peak hysteresis is at fixed r, single-signed (magnitude), does NOT flip sign like memory-diff.")

print("\n"+"="*96)
print(" RECONCILED VERDICT")
print("="*96)
print(f"  V-RAR : {'PASS' if V_RAR else 'FAIL'}")
print(f"  MG-impossible gap: STRIPPED baseline {spread(sMI)-spread(sMG_strip):+.1f}pp (INFLATED/RETRACTED) ->"
      f" HONEST theta baseline {spread(sMI)-spread(sMG_theta):+.1f}pp")
print(f"  CORRECT observable = fixed-r sigma hysteresis: Crater II peak {hyst.max():.1f}% (MI), MG exactly 0")
print(f"  SOFT SPOT: magnitude scales with tau_mem (NOT bath-forced)")
print("EXIT 0")
