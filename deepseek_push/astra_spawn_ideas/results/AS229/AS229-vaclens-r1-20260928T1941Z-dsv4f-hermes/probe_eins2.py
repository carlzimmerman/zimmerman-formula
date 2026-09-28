#!/usr/bin/env python3
"""Diagnose the G00 residual structure of the nonlinear-Ricci builder."""
import numpy as np

Ns = 16
L3 = 4.0*np.pi
ax = np.linspace(0, L3, Ns, endpoint=False)
X, Y, Zg = np.meshgrid(ax, ax, ax, indexing="ij")
hstep = L3/Ns
kvec = np.fft.fftfreq(Ns, d=hstep)
KX, KY, KZ = np.meshgrid(kvec, kvec, kvec, indexing="ij")
K2 = KX**2 + KY**2 + KZ**2
K2[0,0,0] = 1.0
eta = np.diag([-1.0,1.0,1.0,1.0])

def lapN(f):
    return np.fft.ifftn(-K2*np.fft.fftn(f)).real

def dg(garr, mu, nu, axis):
    return (np.roll(garr[mu,nu], -1, axis=axis) - np.roll(garr[mu,nu], +1, axis=axis))/(2.0*hstep)

def eins_full(PhiN, PsiN, linear_gamma=False):
    h = np.zeros((4,4)+PhiN.shape)
    h[0,0] = -2.0*PhiN
    for i in range(3):
        h[i+1,i+1] = -2.0*PsiN
    g = np.zeros((4,4)+PhiN.shape)
    for mu in range(4):
        for nu in range(4):
            g[mu,nu] = eta[mu,nu] + h[mu,nu]
    gi = eta[None,None]
    gi = np.broadcast_to(eta[:,:,None,None,None], (4,4)+PhiN.shape).copy()
    if not linear_gamma:
        for idx in np.ndindex(PhiN.shape):
            gi[:,:,idx[0],idx[1],idx[2]] = np.linalg.inv(g[:,:,idx[0],idx[1],idx[2]])
    Gamma = np.zeros((4,4,4)+PhiN.shape)
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                s = 0.0
                for sig in range(4):
                    if mu != 0:
                        s += gi[lam,sig]*dg(g,sig,nu,mu-1)
                    if nu != 0:
                        s += gi[lam,sig]*dg(g,sig,mu,nu-1)
                    if sig != 0:
                        s -= gi[lam,sig]*dg(g,mu,nu,sig-1)
                Gamma[lam,mu,nu] = 0.5*s
    def dG(lam, mu, nu, axis):
        return (np.roll(Gamma[lam,mu,nu], -1, axis=axis) - np.roll(Gamma[lam,mu,nu], +1, axis=axis))/(2.0*hstep)
    R = np.zeros((4,4)+PhiN.shape)
    for mu in range(4):
        for nu in range(4):
            acc = 0.0
            for lam in range(1,4):
                acc += dG(lam, mu, nu, lam-1)
            for lam in range(4):
                if nu != 0:
                    acc -= dG(lam, mu, lam, nu-1)
            for s in range(4):
                for l in range(4):
                    acc += Gamma[s,mu,nu]*Gamma[l,s,l] - Gamma[s,mu,l]*Gamma[l,nu,s]
            R[mu,nu] = acc
    Rt = -R[0,0] + sum(R[i,i] for i in range(1,4))
    Gt = np.zeros_like(R)
    for mu in range(4):
        for nu in range(4):
            Gt[mu,nu] = R[mu,nu] - 0.5*Rt*g[mu,nu]
    return Gt, Gamma, R

a = 1e-6
ph = a*np.cos(X)
ps = a*np.cos(X)
Gt, Gamma, R = eins_full(ph, ps)
res = Gt[0,0] - 2.0*lapN(ps)   # should be ~ FD error
print("A) Phi=Psi=a cos x: max|G00 - 2 Lap Psi| =", np.max(np.abs(res)))
# sample the residual field along x at y=z=0
smp = res[:,0,0]
print("   residual samples (x = 0, L/8, L/4, 3L/8, L/2, 5L/8, 3L/4):")
print("   ", [f"{v:.3e}" for v in smp[[0,2,4,6,8,10,12]]])
print("   cos field there:", [f"{np.cos(ax[i]):+.3f}" for i in (0,2,4,6,8,10,12)])
print("   G00 at those points:", [f"{Gt[0,0][i,0,0]:.3e}" for i in (0,2,4,6,8,10,12)])
print("   2 Lap Psi there:", [f"{(2.0*lapN(ps))[i,0,0]:.3e}" for i in (0,2,4,6,8,10,12)])
print("   phase arg of residual at x=L/4: res/LG00 =", res[4,0,0]/(2.0*lapN(ps))[4,0,0] if abs((2.0*lapN(ps))[4,0,0])>1e-12 else "nan")
# linear-gamma version
Gt2, _, _ = eins_full(ph, ps, linear_gamma=True)
res2 = Gt2[0,0] - 2.0*lapN(ps)
print("   linear-gamma version: max|G00 - 2 Lap Psi| =", np.max(np.abs(res2)))
# G11 residuals
S = ph - ps
G11exp = lapN(S) - np.fft.ifftn(-KX*KX*np.fft.fftn(S)).real
print("   max|G11 - (Lap S - S,11)| =", np.max(np.abs(Gt[1,1] - G11exp)))
print("   max|G22 - (Lap S - S,22)| =", np.max(np.abs(Gt[2,2] - (lapN(S) - np.fft.ifftn(-KZ*KZ*np.fft.fftn(S)).real))))
# spectrogram of residual
Fres = np.abs(np.fft.fftn(res))
Fres[0,0,0] = 0
top = np.unravel_index(np.argmax(Fres), Fres.shape)
print("   argmax FFT bin of residual:", top, " k =", (kvec[top[0]], kvec[top[1]], kvec[top[2]]),
      " amp =", Fres[top]/np.max(np.abs(2.0*lapN(ps))))
