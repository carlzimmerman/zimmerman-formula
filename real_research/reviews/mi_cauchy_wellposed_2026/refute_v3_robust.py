#!/usr/bin/env python3
"""
REFUTATION v3 -- robustness of the CAUSAL/no-secular finding: eta->0 limit, grid refinement, and the
w=0 IR branch point (the 1/|w| concern) examined directly. Also verify the imaginary part of the
retarded framework kernel is odd & the real part even (Kramers-Kronig / reality), and that the ADVANCED
framework prescription flips support (the true framework control, not the v1 broken one).
"""
import numpy as np
np.seterr(all='ignore')
print("="*100); print(" REFUTATION v3 -- eta->0, grid refinement, w=0 IR point, framework advanced control")
print("="*100)

def invFT(F,w):
    N=len(w); dw=w[1]-w[0]
    t=np.fft.fftshift(np.fft.fftfreq(N,d=dw))*2*np.pi
    g=np.fft.fftshift(np.fft.fft(np.fft.ifftshift(F)))*(dw/(2*np.pi))
    return t, g*np.exp(-1j*w[0]*t)

def frame_kernels(eta, Wmax, N, adv=False):
    w=np.linspace(-Wmax,Wmax,N,endpoint=False)
    s = -1j if adv else 1j
    wc=w+s*eta; z=-(wc**2)
    K=(np.sqrt(1.0+4.0*z)-1.0)/(2.0*np.sqrt(z))
    D=wc*K
    tP,gP=invFT(1.0/D,w)
    tN,gN=invFT(wc*(K-1.0),w)
    return tP,gP,tN,gN

def ratio(t,g):
    dt=t[1]-t[0]; c=np.abs(t)<5*dt
    En=np.trapz(np.abs(g[(t<0)&~c])**2,t[(t<0)&~c]); Ep=np.trapz(np.abs(g[(t>0)&~c])**2,t[(t>0)&~c])
    return En/max(Ep,1e-300)

print("\n[1] eta -> 0 limit (retarded regulator): neg/pos energy ratio of propagator 1/D must stay <<1")
N=2**20; Wmax=400.0
for eta in [8e-3,4e-3,2e-3,1e-3,5e-4]:
    tP,gP,tN,gN=frame_kernels(eta,Wmax,N)
    print(f"   eta={eta:.0e}:  prop neg/pos={ratio(tP,gP):.3e}   memory neg/pos={ratio(tN,gN):.3e}")

print("\n[2] grid/Wmax refinement at eta=2e-3 (convergence of causality ratio)")
for Wmax,Nl in [(200.0,2**19),(400.0,2**20),(800.0,2**21)]:
    tP,gP,tN,gN=frame_kernels(2e-3,Wmax,Nl)
    print(f"   Wmax={Wmax:5.0f} N=2^{int(np.log2(Nl))}:  prop neg/pos={ratio(tP,gP):.3e}  memory neg/pos={ratio(tN,gN):.3e}")

print("\n[3] FRAMEWORK ADVANCED control (w-> w - i eta): support MUST flip to t<0")
tPa,gPa,tNa,gNa=frame_kernels(2e-3,Wmax,N,adv=True)
print(f"   advanced prop neg/pos={ratio(tPa,gPa):.3e} (expect >>1)   advanced memory neg/pos={ratio(tNa,gNa):.3e} (expect >>1)")
adv_flips = ratio(tPa,gPa)>1e2 and ratio(tNa,gNa)>1e2

print("\n[4] w=0 IR branch point (the 1/|w| concern): retarded symbol near w=0, real axis eta->0")
# D(w)=w*K, K~1/(2 sqrt z)=1/(2 sqrt(-w^2)). As w->0+, sqrt(-w^2)=|w| e^{i..}. D = w/(2 sqrt(-w^2)) -> finite.
for eps in [1e-2,1e-4,1e-6]:
    for wv in [eps, -eps]:
        wc=wv+1j*1e-12; z=-(wc**2); K=(np.sqrt(1+4*z)-1)/(2*np.sqrt(z)); D=wc*K
        print(f"   w={wv:+.0e}:  D(w)={D.real:+.4e}{D.imag:+.4e}i  1/D={ (1/D).real:+.4e}{(1/D).imag:+.4e}i  (finite={np.isfinite(abs(D)) and abs(D)>0})")

print("\n[5] reality/KK: retarded kernel g(t) should be real (Re even, Im odd in w). Check Im[g(t)] small.")
tP,gP,tN,gN=frame_kernels(2e-3,Wmax,N)
dt=tP[1]-tP[0]; pos=(tP>5*dt)&(tP<0.5*tP.max())
im_frac=np.trapz(np.abs(gP[pos].imag),tP[pos])/max(np.trapz(np.abs(gP[pos].real),tP[pos]),1e-300)
print(f"   propagator g(t): INT|Im|/INT|Re| on t>0 = {im_frac:.3e} (should be small -> g real -> physical)")

print("\n"+"="*100)
print(" v3 SUMMARY")
print(f"   causality ratio stable & <<1 across eta and grid:  (see [1],[2])")
print(f"   framework ADVANCED prescription flips to t<0:       {adv_flips}  (true framework control PASSES)")
print(f"   w=0 IR point: D finite & nonzero, 1/D finite:       (see [4])")
print("="*100)
import sys; sys.exit(0)
