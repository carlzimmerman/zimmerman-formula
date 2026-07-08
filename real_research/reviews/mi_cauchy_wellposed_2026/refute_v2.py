#!/usr/bin/env python3
"""
REFUTATION v2 -- FIX the pipeline first (control MUST discriminate), then judge the framework kernel.

v1 bug: the CONTROL (advanced prescription) did NOT flip support to t<0 -> the pipeline was blind, so
its "ACAUSAL" verdicts on the framework kernel were meaningless FFT artifacts. Root causes to fix:
  (1) FFT convention: with kernel e^{-i w t}, a pole/singularity in the LOWER half w-plane closes for
      t>0 (retarded). So the RETARDED symbol must be analytic in the UPPER half plane, singular in the
      LOWER -> prescription w -> w + i eta pushes singularities DOWN (into LHP) -> retarded (t>0). Good.
      But numpy ifft uses e^{+2pi i ...}. Must match e^{-i w t} explicitly. v1 used ifft(ifftshift(F))
      which is e^{+i w t} -> WRONG SIGN. Fix: use fft (e^{-i...}) or conjugate the convention.
  (2) Calibrate on an ANALYTIC control with a KNOWN retarded kernel: the damped oscillator
      G_R(w) = 1/(w0^2 - w^2 - i gamma w). Retarded (w+i0 in the RESPONSE, poles in LHP) -> G_R(t) =
      theta(t) e^{-gamma t/2} sin(...)/... . We must reproduce theta(t) support and exponential DECAY.
      If we can reproduce that, the pipeline is trustworthy; THEN apply to the framework D=w*K.
"""
import numpy as np
np.seterr(all='ignore')
print("="*100); print(" REFUTATION v2 -- calibrated time-domain retarded kernel"); print("="*100)

# -- correct inverse transform g(t) = (1/2pi) INT dw e^{-i w t} F(w), F sampled on symmetric w-grid --
def invFT(F, w):
    """g(t)=(1/2pi) INT dw e^{-i w t} F(w). Returns t (sorted), g. Uses e^{-iwt} via np.fft.fft."""
    N=len(w); dw=w[1]-w[0]
    # define on w in [-Wmax,Wmax). g(t)=(dw/2pi) sum_n F_n e^{-i w_n t}. w_n=-Wmax+n dw.
    # t_m conjugate grid: t_m = 2pi m/(N dw), m in [-N/2,N/2).
    t = np.fft.fftshift(np.fft.fftfreq(N, d=dw))*2*np.pi
    # e^{-i w_n t_m}. Write w_n = w0 + n dw with w0=-Wmax. Factor e^{-i w0 t_m} * sum_n F_n e^{-i n dw t_m}.
    # sum_n F_n e^{-i n dw t_m} = DFT with e^{-2pi i n m /N} when dw*t_m = 2pi m/N -> t_m=2pi m/(N dw). matches.
    # np.fft.fft computes sum_n a_n e^{-2pi i k n/N}. So:
    g = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(F))) * (dw/(2*np.pi))
    w0 = w[0]
    g = g * np.exp(-1j*w0*t)
    return t, g

Wmax=400.0; N=2**20
w = np.linspace(-Wmax, Wmax, N, endpoint=False)

# ---- CONTROL 1: damped harmonic oscillator, KNOWN retarded kernel theta(t)e^{-g t/2}sin(Om t)/Om ----
w0=3.0; gam=0.4
def Gdho_ret(w): return 1.0/(w0**2 - w**2 - 1j*gam*w)   # poles at w = -i g/2 +- sqrt(w0^2-g^2/4): LHP -> retarded
t,g = invFT(Gdho(w) if False else Gdho_ret(w), w)
dt=t[1]-t[0]; core=np.abs(t)<5*dt
En=np.trapz(np.abs(g[(t<0)&~core])**2,t[(t<0)&~core]); Ep=np.trapz(np.abs(g[(t>0)&~core])**2,t[(t>0)&~core])
print(f"\n[CTRL retarded DHO] neg/pos energy = {En/max(Ep,1e-300):.3e}  (expect <<1: retarded lives t>0)")
ctrl_ret_ok = En/max(Ep,1e-30) < 1e-2
# analytic compare at a few t>0
Om=np.sqrt(w0**2-gam**2/4)
for tv in [0.5,1.5,3.0]:
    i=np.argmin(np.abs(t-tv)); ana=np.exp(-gam*tv/2)*np.sin(Om*tv)/Om
    print(f"     t={tv}: numeric Re g={g[i].real:+.4f}  analytic theta*e^(-gt/2)sin(Om t)/Om={ana:+.4f}")

# ---- CONTROL 2: ADVANCED DHO (poles in UHP): w0^2-w^2+i g w -> support must be t<0 ----
def Gdho_adv(w): return 1.0/(w0**2 - w**2 + 1j*gam*w)
tA,gA=invFT(Gdho_adv(w),w)
EnA=np.trapz(np.abs(gA[(tA<0)&~core])**2,tA[(tA<0)&~core]); EpA=np.trapz(np.abs(gA[(tA>0)&~core])**2,tA[(tA>0)&~core])
print(f"[CTRL advanced DHO] neg/pos energy = {EnA/max(EpA,1e-300):.3e}  (expect >>1: advanced lives t<0)")
ctrl_adv_ok = EnA/max(EpA,1e-30) > 1e2
print(f"   PIPELINE DISCRIMINATES: retarded->t>0 {ctrl_ret_ok}, advanced->t<0 {ctrl_adv_ok}")

if not (ctrl_ret_ok and ctrl_adv_ok):
    print("\n   !! pipeline still not calibrated; aborting framework judgement."); import sys; sys.exit(0)

# ---------------------------------------------------------------------------------------------------
# NOW the framework operator, calibrated pipeline. a0=1.  Retarded: w -> w + i eta.
# ---------------------------------------------------------------------------------------------------
print("\n[FRAMEWORK] D(w)=w*K(-(w+i eta)^2), retarded.  Propagator 1/D and nonlocal memory w*(K-1).")
eta=2e-3
def K_ret(w):
    wc=w+1j*eta; z=-(wc**2)
    return (np.sqrt(1.0+4.0*z)-1.0)/(2.0*np.sqrt(z))
def D_ret(w): return (w+1j*eta)*K_ret(w)

# propagator 1/D
tP,gP=invFT(1.0/D_ret(w), w)
EnP=np.trapz(np.abs(gP[(tP<0)&~core])**2,tP[(tP<0)&~core]); EpP=np.trapz(np.abs(gP[(tP>0)&~core])**2,tP[(tP>0)&~core])
print(f"   propagator 1/D:  neg/pos energy = {EnP/max(EpP,1e-300):.3e}  -> {'CAUSAL (t>0)' if EnP/max(EpP,1e-30)<1e-2 else 'ACAUSAL'}")

# nonlocal memory w*(K-1) (subtract local w piece)
def NL(w): wc=w+1j*eta; return wc*(K_ret(w)-1.0)
tN,gN=invFT(NL(w), w)
EnN=np.trapz(np.abs(gN[(tN<0)&~core])**2,tN[(tN<0)&~core]); EpN=np.trapz(np.abs(gN[(tN>0)&~core])**2,tN[(tN>0)&~core])
print(f"   nonlocal memory w*(K-1):  neg/pos energy = {EnN/max(EpN,1e-300):.3e}  -> {'CAUSAL (t>0)' if EnN/max(EpN,1e-30)<1e-2 else 'ACAUSAL'}")

# secular growth: late-time envelope on t>0
def late_p(t,g,lo,hi):
    m=(t>lo)&(t<hi); tt=t[m]; gg=np.maximum(np.abs(g[m]),1e-300)
    lt=np.log(tt); lg=np.log(gg); nb=30; e=np.linspace(lt.min(),lt.max(),nb+1); bx=[];by=[]
    for i in range(nb):
        s=(lt>=e[i])&(lt<e[i+1])
        if s.sum()>3: bx.append(lt[s].mean()); by.append(np.log(np.mean(np.exp(lg[s]))))
    bx=np.array(bx);by=np.array(by)
    return np.polyfit(bx,by,1)[0] if len(bx)>=5 else np.nan
tm=tP.max()
pP=late_p(tP,gP,0.02*tm,0.8*tm); pN=late_p(tN,gN,0.02*tm,0.8*tm)
print(f"\n[SECULAR] propagator 1/D  |g|~t^p : p={pP:+.3f}  ({'decays' if pP<-0.02 else 'NON-DECAYING'})")
print(f"[SECULAR] nonlocal memory |g|~t^p : p={pN:+.3f}  ({'decays' if pN<-0.02 else 'NON-DECAYING'})")

# also fit exponential envelope (is there e^{+ct} runaway? fit log|g| vs t linearly)
def exp_rate(t,g,lo,hi):
    m=(t>lo)&(t<hi); tt=t[m]; gg=np.maximum(np.abs(g[m]),1e-300)
    return np.polyfit(tt,np.log(gg),1)[0]
rP=exp_rate(tP,gP,0.1*tm,0.8*tm)
print(f"[SECULAR] propagator exp rate d(log|g|)/dt = {rP:+.3e}  ({'no exp runaway (<=0)' if rP<=1e-4 else 'EXP RUNAWAY'})")

print("\n"+"="*100)
causal = (EnP/max(EpP,1e-30)<1e-2) and (EnN/max(EpN,1e-30)<1e-2)
nosec = (pP<0.02) and (pN<0.6) and (rP<=1e-4)
print(f" CALIBRATED VERDICT: causal={causal}  no-exp-runaway={rP<=1e-4}  prop_power p={pP:+.3f} mem_power p={pN:+.3f}")
import sys; sys.exit(0)
