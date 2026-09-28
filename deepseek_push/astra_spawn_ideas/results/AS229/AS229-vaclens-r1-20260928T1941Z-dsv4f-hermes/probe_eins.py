#!/usr/bin/env python3
"""Clean plane-wave probe of the nonlinear-Ricci builder (patched Christoffel)."""
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
def ddN(f, i, j):
    kk1 = [KX, KY, KZ][i]; kk2 = [KX, KY, KZ][j]
    return np.fft.ifftn(-kk1*kk2*np.fft.fftn(f)).real

def dg(garr, mu, nu, axis):
    return (np.roll(garr[mu,nu], -1, axis=axis) - np.roll(garr[mu,nu], +1, axis=axis))/(2.0*hstep)

def eins_full(PhiN, PsiN):
    h = np.zeros((4,4)+PhiN.shape)
    h[0,0] = -2.0*PhiN
    for i in range(3):
        h[i+1,i+1] = -2.0*PsiN
    g = np.zeros((4,4)+PhiN.shape)
    for mu in range(4):
        for nu in range(4):
            g[mu,nu] = eta[mu,nu] + h[mu,nu]
    gi = np.zeros_like(g)
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
ps = a*np.cos(X)   # test Phi = Psi = a cos x  -> linearized: S = 0, G00 = 2 Lap Phi = -2a cos x, G_ij = 0
Gt, Gamma, R = eins_full(ph, ps)
print("A) Phi=Psi=a cos x: max|G00 + 2a cosx| =", np.max(np.abs(Gt[0,0] + 2.0*a*np.cos(X))))
print("   max|G11| =", np.max(np.abs(Gt[1,1])), " max|G12| =", np.max(np.abs(Gt[0,1])), " max|G22| =", np.max(np.abs(Gt[2,2])))
print("   max|G01| =", np.max(np.abs(Gt[1,0])))
Gt2, Gamma2, R2 = eins_full(0.0*X, a*np.cos(X))
print("B) Phi=0, Psi=a cos x: max|G00 - 2 Lap Psi| =", np.max(np.abs(Gt2[0,0] - 2.0*lapN(ps))))
S = -ps
print("   max|G11 - (Lap S - S,11)| =", np.max(np.abs(Gt2[1,1] - (lapN(S) - ddN(S,0,0)))))
print("   max|G22 - Lap S| =", np.max(np.abs(Gt2[2,2] - lapN(S))))
print("   max|G01 - (-S,01)| =", np.max(np.abs(Gt2[0,1] - (-ddN(S,0,1)))))
print("   G00 stats: min/max =", Gt2[0,0].min(), Gt2[0,0].max())
print("   2 Lap Psi stats: min/max =", (2.0*lapN(ps)).min(), (2.0*lapN(ps)).max())
# also show Gamma^0_{0x}:
mask = np.abs(np.sin(X)) > 0.3
print("   Gamma^0_{01}/(-a sin x):", np.median(Gamma2[0,0,1][mask]/(-a*np.sin(X)[mask])))
print("   Gamma^1_{00}/(-a sin x):", np.median(Gamma2[1,0,0][mask]/(-a*np.sin(X)[mask])))
