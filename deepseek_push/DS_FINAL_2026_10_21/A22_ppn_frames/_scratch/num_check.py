"""Independent numerical cross-check of the exact static solution
   Phi = -GM/r + (GM/L*^2) r ,  psi = GM/(gamma r)
by solving  lap^2 psi = -K rho/gamma ,  lap^2 Phi = K(rho+psi)  on a periodic FFT grid,
then averaging over spherical shells.
"""
import numpy as np

c = 2.99792458e8
G = 6.67430e-11
pc = 3.0856775814913673e16
Ls = 24.0*pc
M = 1.98892e30
K = 4*np.pi*G/c**2
gam = K*Ls**2/2
mu = G*M/c**2

N = 160
Lbox = 3e15
sig = 3e13
dx = Lbox/N
x = (np.arange(N) - N//2)*dx
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
R = np.sqrt(X**2 + Y**2 + Z**2)
rhov = M/((2*np.pi*sig**2)**1.5)*np.exp(-R**2/(2*sig**2))
rho_k = np.fft.fftn(rhov)*dx**3

k1 = 2*np.pi*np.fft.fftfreq(N, d=dx)
kx, ky, kz = np.meshgrid(k1, k1, k1, indexing='ij')
k2 = kx**2 + ky**2 + kz**2
k2[0, 0, 0] = np.inf

psi_k = K*rho_k/(gam*k2)
V = Lbox**3
psi = np.fft.ifftn(psi_k).real*N**3/V
Phi = np.fft.ifftn(-K*(rho_k + psi_k)/k2).real*N**3/V

edges = np.linspace(4*sig, 45*sig, 24)
idx = np.digitize(R.ravel(), edges)
rc, Pc, Sc = [], [], []
for i in range(1, len(edges)):
    m = idx == i
    if m.sum() > 50:
        rc.append(R.ravel()[m].mean()); Pc.append(Phi.ravel()[m].mean()); Sc.append(psi.ravel()[m].mean())
rc = np.array(rc); Pc = np.array(Pc); Sc = np.array(Sc)
Pan = -mu/rc + (mu/Ls**2)*rc
San = mu/(gam*rc)
Pc_c = Pc - Pc[0] + Pan[0]
Sc_c = Sc - Sc[0] + San[0]
eP = np.max(np.abs(Pc_c - Pan))/np.max(np.abs(Pan))
eS = np.max(np.abs(Sc_c - San))/np.max(np.abs(San))
print("N=%d Lbox=%.1e sigma=%.1e lam=%.3e" % (N, Lbox, sig, np.sqrt(gam/K)))
print("shells: %d, r from %.2e to %.2e" % (len(rc), rc[0], rc[-1]))
print("max rel err Phi = %.3e ; max rel err psi = %.3e" % (eP, eS))
print("r=%.2e  Phi_num=%.6e  Phi_analytic=%.6e" % (rc[len(rc)//2], Pc_c[len(rc)//2], Pan[len(rc)//2]))
