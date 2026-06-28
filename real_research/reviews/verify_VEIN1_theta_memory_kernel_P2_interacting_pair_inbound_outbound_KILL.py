#!/usr/bin/env python3
r"""
ADVERSARIAL KILL TEST -- VEIN 1 / P2: interacting-pair INBOUND-vs-OUTBOUND internal-sigma asymmetry.
====================================================================================================
B4 DISCIPLINE (what killed B4: beta_MG was HARDCODED >0; beta_MI used a fake sigma^2~1/mu proxy; the
real Jeans calc showed MG~0 and MI ill-defined). Here we TRY TO KILL win-flavored P2 with a REAL
dynamical calc -- NO assumed sign, NO ad-hoc memory proxy.

FRAMEWORK (its OWN terms; Milgrom 2022 arXiv:2208.07073v3 MI formulation):
  a0 = cH_Lambda/Z = 9.36e-11.  nu(y)=sqrt(1+1/y); mu_fw(x)=(sqrt(1+4x^2)-1)/(2x).
  Eq (34) two-frequency EFE: A(omega_in) = a_in + a_ex * theta(omega_ex/omega_in),
    omega_ex = THE FREQUENCY AT WHICH THE EXTERNAL FIELD VARIES = |d ln a_ex/dt| (INSTANTANEOUS),
    theta evaluated at the INSTANTANEOUS y = omega_ex/omega_in. theta(1)=1, decreasing, theta(0)~few,
    FORM UNKNOWN. The kernel is a spectral weight on the frequency content present NOW (Eq 28), NOT a
    hand-built "where was the body tau_mem ago" lookback.

POSIT'S CENTRAL CLAIM (attacked): at MATCHED momentary separation, an OUTBOUND galaxy ran HIGH y
recently and an inbound one ran LOW y, so theta(y_in)!=theta(y_out) -> ~20% sigma asymmetry; MG=0.
The existing reviews/v1_merger_memory_kernel.py PRODUCED ~20% by SETTING
    y_inbound  = omega_orbit(d_match + v*tau_mem)/omega_in   (forced to a larger past-separation)
    y_outbound = omega_orbit(d_match - v*tau_mem)/omega_in   (forced to a smaller past-separation)
i.e. it evaluated theta at where the galaxy WAS a memory-time ago, with inbound and outbound forced to
OPPOSITE past separations. THAT IS THE ASSUMED-SIGN MOVE.

KILL HYPOTHESIS: omega_ex=|d ln a_ex/dt| is a STATE FUNCTION of the orbit (D and v_radial only). On a
two-body orbit at MATCHED D the speed |v| and |v_radial| are IDENTICAL inbound vs outbound (energy
conservation + time-reversal symmetry) -> omega_ex identical -> theta identical -> MI asymmetry = 0,
SAME as MG. The 20% is the hand-built lookback, not the kernel. We compute instantaneous omega_ex from
the real orbit; then steelman with a genuine causal memory convolution; then a0-degeneracy + the swamp.
Footing sealed. No git push.
"""
import numpy as np

A0=9.36e-11; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; km=1.0e3; Myr=3.156e13
def mu_fw(x):  x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)
def theta_rat(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)
def theta_exp(y): y=np.abs(np.asarray(y,float)); return np.exp(1.0-np.abs(y))

print("="*104)
print(" ADVERSARIAL KILL TEST -- P2 inbound-vs-outbound sigma asymmetry (real instantaneous omega_ex, both-ways)")
print("="*104)

M1=5e10*Msun; M2=5e10*Msun; Mtot=M1+M2
sig_in_kms=50.0; R_in_kpc=8.0
omega_in=(sig_in_kms*km)/(R_in_kpc*kpc)
g_in    =(sig_in_kms*km)**2/(R_in_kpc*kpc)
def a_ext(D):  return G*M2/D**2
def dlnaext_dt(D,vr):  return np.abs(-2.0*vr/D)   # a_ex ~ D^-2 -> |d ln a_ex/dt| = |2 vr/D|

D_apo=120.0*kpc; D_peri=18.0*kpc
Phi=lambda D:-G*Mtot/D
L2=2*(Phi(D_peri)-Phi(D_apo))/(1.0/D_apo**2-1.0/D_peri**2)
E =Phi(D_apo)+L2/(2*D_apo**2)
def vr_of_D(D):
    val=2*(E-Phi(D))-L2/D**2; return np.sqrt(np.maximum(val,0.0))

print(f"\n  Relative orbit: M_tot={Mtot/Msun:.1e} Msun, apo={D_apo/kpc:.0f} kpc, peri={D_peri/kpc:.0f} kpc.")
print(f"  Target(diffuse): sigma_in={sig_in_kms} km/s, R={R_in_kpc} kpc -> omega_in={omega_in:.3e}/s, a_in={g_in/A0:.3f} a0.")
Dgrid=np.linspace(D_peri*1.001,D_apo*0.999,4000); vr=vr_of_D(Dgrid)
y_inst=dlnaext_dt(Dgrid,vr)/omega_in
print(f"  peak instantaneous y=omega_ex/omega_in over orbit = {y_inst.max():.3f} (where vr/D peaks; vr->0 at peri).")

print("\n"+"-"*104)
print(" (A) INSTANTANEOUS omega_ex at MATCHED separation D: inbound vs outbound (the kernel's ACTUAL argument)")
print("-"*104)
print(f"  {'D[kpc]':>8} {'|vr|_in[km/s]':>13} {'|vr|_out[km/s]':>14} {'y_in':>8} {'y_out':>8} {'th_in':>7} {'th_out':>7} {'sig_out/sig_in':>14}")
maxasym=0.0
for Dk in (25.0,30.0,40.0,60.0,90.0):
    D=Dk*kpc; vrin=vr_of_D(D); vrout=vr_of_D(D)
    yin=dlnaext_dt(D,vrin)/omega_in; yout=dlnaext_dt(D,vrout)/omega_in; ae=a_ext(D)
    Bin=1.0/mu_fw((g_in+theta_rat(yin)*ae)/A0); Bout=1.0/mu_fw((g_in+theta_rat(yout)*ae)/A0)
    asym=np.sqrt(Bout/Bin); maxasym=max(maxasym,abs(asym-1))
    print(f"  {Dk:8.0f} {vrin/km:13.2f} {vrout/km:14.2f} {yin:8.4f} {yout:8.4f} {theta_rat(yin):7.4f} {theta_rat(yout):7.4f} {asym:14.5f}")
print(f"\n  -> instantaneous omega_ex IDENTICAL inbound vs outbound at every matched D (energy conservation +")
print(f"     time-reversal). MAX MI sigma asymmetry = {maxasym*100:.4f}% ==> ~0, SAME AS MG. The 20% was the")
print(f"     hand-built lookback proxy, NOT the framework kernel (which sees only instantaneous omega_ex).")

print("\n"+"-"*104)
print(" (B) STEELMAN -- genuine causal finite-memory convolution theta_eff(t)=<theta(y)>_K over recent history")
print("-"*104)
dt=0.05*Myr; D=D_apo; vrad=-1e-6; t=0.0
ts=[];Ds=[];vrs=[]
for _ in range(400000):
    acc=-G*Mtot/D**2+L2/D**3; vrad+=acc*dt; D+=vrad*dt; t+=dt
    if D<=D_peri: D=D_peri; vrad=abs(vrad)
    ts.append(t);Ds.append(D);vrs.append(vrad)
    if D>=D_apo and vrad>0 and t>dt*10: break
ts=np.array(ts);Ds=np.array(Ds);vrs=np.array(vrs)
y_t=np.abs(2.0*vrs/Ds)/omega_in
peri_idx=int(np.argmin(Ds))
for tau_fac in (1.0,3.0):
    tau=tau_fac/omega_in; al=np.exp(-dt/tau)
    thy=theta_rat(y_t); theta_eff=np.zeros_like(thy); theta_eff[0]=thy[0]
    for i in range(1,len(thy)): theta_eff[i]=al*theta_eff[i-1]+(1-al)*thy[i]
    inb=np.arange(0,peri_idx); outb=np.arange(peri_idx,len(Ds))
    Dmatch=np.linspace(D_peri*1.3,D_apo*0.7,12); asyms=[];mg=[]
    for Dm in Dmatch:
        i_in=inb[np.argmin(np.abs(Ds[inb]-Dm))]; i_out=outb[np.argmin(np.abs(Ds[outb]-Dm))]; ae=a_ext(Dm)
        Bin=1.0/mu_fw((g_in+theta_eff[i_in]*ae)/A0); Bout=1.0/mu_fw((g_in+theta_eff[i_out]*ae)/A0)
        asyms.append(np.sqrt(Bout/Bin)); mg.append(1.0)
    asyms=np.array(asyms)
    print(f"  tau_mem={tau_fac:.0f}/omega_in={tau/Myr:.0f} Myr: MI median |sig_out/sig_in-1|={np.median(np.abs(asyms-1))*100:5.2f}% "
          f"(max {np.max(np.abs(asyms-1))*100:.2f}%);  MG = 0.0000%")
print("""  READ (B): a GENUINE causal convolution DOES give nonzero asymmetry (history differs: outbound just
  passed the y-peak), but only a FEW percent -- an order below the posit's 20-24%, washed out by averaging
  over the pass. MG = 0. But the convolution FORM is an ADDED assumption (founded-not-derived) -> (C),(D).""")

print("-"*104)
print(" (C) a0-DEGENERACY: can free-a0 MG reproduce the steelman MI sig(D) over BOTH branches?")
print("-"*104)
from scipy.optimize import minimize_scalar
tau=1.0/omega_in; al=np.exp(-dt/tau); thy=theta_rat(y_t); theta_eff=np.zeros_like(thy); theta_eff[0]=thy[0]
for i in range(1,len(thy)): theta_eff[i]=al*theta_eff[i-1]+(1-al)*thy[i]
sampl=np.arange(0,len(Ds),200); ae_s=a_ext(Ds[sampl]); th_s=theta_eff[sampl]
sig_mi=np.sqrt(1.0/mu_fw((g_in+th_s*ae_s)/A0))
def mis(loga0):
    a0u=np.exp(loga0); s=np.sqrt(1.0/mu_fw((g_in+ae_s)/a0u)); return np.sum((np.log(s)-np.log(sig_mi))**2)
r=minimize_scalar(mis,bounds=(np.log(A0/30),np.log(A0*30)),method='bounded')
a0fit=np.exp(r.x); s_fit=np.sqrt(1.0/mu_fw((g_in+ae_s)/a0fit)); resid=np.max(np.abs(s_fit/sig_mi-1))
print(f"  best-fit MG a0={a0fit/A0:.3f} a0; max fractional residual MG-vs-MI over full pass = {resid*100:.2f}%")
print(f"  (the part a single a0 cannot absorb = the relational, history-dependent residue -- IF the causal")
print(f"   convolution is the true dynamics; the framework only POSITS theta as a spectral weight, not a")
print(f"   causal relaxation kernel, so this residue rides an ADDED founded-not-derived modeling choice.)")

print("-"*104)
print(" (D) THE SWAMP: non-equilibrium / tidal heating vs the steelman asymmetry (the B4 killer)")
print("-"*104)
# tidal (differential) acceleration across the target at pericenter: g_tid = 2 G M2 R_in / D_peri^3
g_tid=2*G*M2*(R_in_kpc*kpc)/D_peri**3
v_peri=np.sqrt(2*(E-Phi(D_peri))) if (E-Phi(D_peri))>0 else np.sqrt(G*Mtot/D_peri)
# effective passage time while companion is within ~2 D_peri:  t_pass ~ 2 D_peri / v_peri
t_pass=2.0*D_peri/v_peri
# impulse velocity kick to an outer star: Delta_v ~ g_tid * t_pass  (accel x time)
dv=g_tid*t_pass
f_heat=(dv/(sig_in_kms*km))**2
print(f"  peri tidal accel across target g_tid={g_tid:.2e} m/s^2; v_peri={v_peri/km:.0f} km/s; t_pass={t_pass/Myr:.0f} Myr.")
print(f"  impulsive internal kick Delta_v~g_tid*t_pass={dv/km:.2f} km/s = {dv/(sig_in_kms*km):.3f} sigma_in.")
print(f"  -> fractional NON-EQUILIBRIUM sigma heating per close pass ~ {f_heat*100:.1f}% (order-of-magnitude).")
print(f"  This tidal heating is ITSELF inbound/outbound-asymmetric with the SAME sign (outbound already")
print(f"  heated, inbound not yet) and is COMPARABLE TO/LARGER THAN the steelman MI asymmetry -- a Newtonian/")
print(f"  MG-SHARED confound on the SAME axis. The pass that creates the signal wrecks the clean sigma (B4 trap).")

print("\n"+"="*104)
print(" VERDICT -- P2 inbound-vs-outbound sigma asymmetry")
print("="*104)
print(f"""  KILL on the AS-STATED claim; only a weakened, non-deliverable residue survives.

  (A) The headline ~20-24% is an ARTIFACT of a hand-built lookback toggle in v1_merger_memory_kernel.py
      (inbound forced to a larger past-separation, outbound to a smaller one). The framework kernel
      theta(y) reads the INSTANTANEOUS omega_ex=|d ln a_ex/dt|, which by energy conservation + time-
      reversal is IDENTICAL inbound vs outbound at matched separation. Computed instantaneous MI asymmetry
      = {maxasym*100:.4f}% ~ 0 -- the SAME as MG. As stated, the asymmetry does NOT exist on the framework's
      own kernel. This is precisely the B4 failure mode (assumed-sign proxy stood in for the real calc).

  (B) STEELMAN: a genuine causal finite-memory convolution gives a nonzero asymmetry (history differs),
      but only a FEW percent -- an order below 20%, washed out by averaging. MG stays 0.

  (C) That residue is not fully a0-degenerate (branches differ at matched D), but ONLY IF the framework's
      inertia is literally a causal relaxation convolution -- which it does not posit; the convolution form
      is an ADDED, founded-not-derived choice that sets the magnitude. Fragile.

  (D) SWAMP: the close fast pass tidally heats the target by ~{f_heat*100:.0f}% and that heating is itself
      inbound/outbound-asymmetric with the SAME sign -- an MG-shared non-equilibrium confound comparable to
      or larger than the steelman MI signal, on the same axis. The pass that makes the signal wrecks it.

  NET: win-flavored P2 does NOT survive as stated. The 20% is ASSUMED (lookback proxy), not derived from
  the kernel; the honest kernel gives ~0 (instantaneous) / few-% (steelman, with an added founded-not-
  derived kernel form); and even that is swamped by same-signed tidal non-equilibrium heating. A single
  orbit is time-reversal-symmetric at fixed separation -> it cannot carry a CLOCK-driven history contrast
  the way the banked relational sigma-spread (different-history parcels at matched a_ext) does. KILLED.""")
print("="*104)
