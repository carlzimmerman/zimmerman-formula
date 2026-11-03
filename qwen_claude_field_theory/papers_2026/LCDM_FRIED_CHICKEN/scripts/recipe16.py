"""A14: LCDM plus one ingredient, routes to the rho_DE tie, per ../FROZEN_RECIPE.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import numpy as np, warnings
from colossus.cosmology import cosmology as cc
from colossus.halo import concentration as CM
warnings.filterwarnings('ignore')
G, kpc, Msun, c_, A0 = 6.674e-11, 3.0857e19, 1.989e30, 2.998e8, 9.3625e-11
COS = [(.70, 67.4), (.685, 73.), (.65, 73.)]; ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
LM = np.arange(10.5, 15.01, .25)
def mu(x): return np.log(1 + x) - x / (1 + x)
def smhm(M): x = M / 10**11.59; return 2 * .0351 * M / (x**-1.376 + x**.608)
def setc(OL, H0): return cc.setCosmology(f'a14_{OL}_{H0}', dict(flat=True, H0=H0, Om0=1 - OL, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False))
def rde(C): return C.Ode0 * C.rho_c(0) * C.h**2 * Msun / kpc**3
def routes(C, lm, z=0):
    M = 10**lm * Msun; rc = C.rho_c(z) * C.h**2 * Msun / kpc**3; R = (3 * M / (800 * np.pi * rc))**(1 / 3)
    c = float(CM.concentration(10**lm * C.h, '200c', z, model='diemer19')); rs = R / c; rhos = 200 / 3 * rc * c**3 / mu(c)
    V2 = G * M / R; Vm2 = V2 * .2162 * c / mu(c); L = 8 * np.pi * G * rde(C) / c_**2
    r0 = (3 * G * M / (L * c_**2))**(1 / 3); gs = 2 * np.pi * G * rhos * rs
    return {'T6': Vm2**2 / (G * smhm(10**lm) * Msun), 'T7': G * M / r0**2, 'T9': np.sqrt(gs * L * c_**2 * rs / 3)}
C0 = setc(*COS[0]); r0 = rde(C0); rows = [(rde(setc(*p)), routes(setc(*p), 12.)) for p in COS]; C0 = setc(*COS[0])
print('T8 coupled quintessence: G -> G(1 + 2 beta^2), no acceleration scale, nothing for G1 to grade -> NO TIE')
G5 = {'T6': True, 'T7': True, 'T9': False}
for k in ('T6', 'T7', 'T9'):
    a = rows[0][1][k]; ke = a / (c_ * np.sqrt(G * r0)); g1 = abs(np.log10(ke / .5)) <= .05
    sl = [np.log(rows[i][1][k] / a) / np.log(rows[i][0] / r0) for i in (1, 2)]; g2 = all(abs(s - .5) <= .05 for s in sl)
    zr = {z: routes(C0, 12., z)[k] / a for z in ZB}; g3 = all(ZB[z][0] <= zr[z] <= ZB[z][1] for z in ZB)
    la = np.log10([routes(C0, m)[k] for m in LM]); g4 = la.std() <= .1
    ok = all((g1, g2, g3, g4, G5[k])); f = lambda b: 'PASS' if b else 'FAIL'
    print(f'{k}: a {a:.3e} ({a / A0:.3f} a0) at 1e12, kappa_eff {ke:.3f} [{f(g1)} G1]; slopes {sl[0]:+.3f} {sl[1]:+.3f} [{f(g2)} G2]; '
          f'a(z)/a(0) {", ".join(f"{z}: {x:.3f}" for z, x in zr.items())} [{f(g3)} G3]; rms over log M 10.5-15 {la.std():.3f} dex, '
          f'range {la.min() - np.log10(A0):+.2f} to {la.max() - np.log10(A0):+.2f} dex vs a0 [{f(g4)} G4]; [{f(G5[k])} G5] -> {"TIES" if ok else "NO TIE"}')
print('T9 G5: no LCDM term multiplies halo gravity by Lambda pull; the product is a posit.')
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
