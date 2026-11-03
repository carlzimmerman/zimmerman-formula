"""A13: LCDM-native routes to the rho_DE tie, no hand terms, per ../FROZEN_RECIPE.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import numpy as np, warnings
from colossus.cosmology import cosmology as cc
from colossus.halo import concentration as CM
warnings.filterwarnings('ignore')
G, kpc, Msun, c_, A0 = 6.674e-11, 3.0857e19, 1.989e30, 2.998e8, 9.3625e-11
COS = [(.70, 67.4), (.685, 73.), (.65, 73.)]; ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
LM = np.arange(10, 15.01, .25)
def mu(x): return np.log(1 + x) - x / (1 + x)
def setc(OL, H0): return cc.setCosmology(f'a13_{OL}_{H0}', dict(flat=True, H0=H0, Om0=1 - OL, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False))
def rde(C): return C.Ode0 * C.rho_c(0) * C.h**2 * Msun / kpc**3
def Hz(C, z): return C.Hz(z) * 1e3 / (kpc * 1e3)
def halo(C, lm, z=0):
    M = 10**lm; rc = C.rho_c(z) * C.h**2 * Msun / kpc**3; R = (3 * M * Msun / (800 * np.pi * rc))**(1 / 3)
    c = float(CM.concentration(M * C.h, '200c', z, model='diemer19')); rs = R / c; rhos = 200 / 3 * rc * c**3 / mu(c)
    V = np.sqrt(G * M * Msun / R); return 2 * np.pi * G * rhos * rs, V**4 / (G * C.Ob0 / C.Om0 * M * Msun), R
def routes(C, z=0, lm=12.):
    L = 8 * np.pi * G * rde(C) / c_**2
    return {'T1': c_ * Hz(C, z) / (2 * np.pi), 'T2': c_**2 * np.sqrt(L / 3) / (2 * np.pi), 'T3': halo(C, lm, z)[0], 'T4': halo(C, lm, z)[1]}
rows = [(rde(setc(*p)), routes(setc(*p))) for p in COS]
C0 = setc(*COS[0]); r0 = rows[0][0]; R12 = halo(C0, 12.)[2]
print(f'base OL 0.70, H0 67.4: rho_DE {r0:.3e} kg/m^3, c sqrt(G rho_DE) {c_ * np.sqrt(G * r0):.4e}; repo a0 {A0:.4e}')
L0 = 8 * np.pi * G * r0 / c_**2; q0 = .5 * C0.Om0 - C0.Ode0
T5 = {r: (L0 * c_**2 * r / 3, abs(q0) * Hz(C0, 0)**2 * r) for r in (10 * kpc, R12)}
for r, (aL, aH) in T5.items(): print(f'T5 at r {r / kpc:.0f} kpc: Lambda pull {aL / A0:.2e} a0, Hubble acceleration |q| H^2 r {aH / A0:.2e} a0')
op = all(v[0] >= .1 * A0 for v in [T5[10 * kpc]]), T5[10 * kpc][1] >= .1 * A0
verdict = {}
for k in ('T1', 'T2', 'T3', 'T4'):
    a = rows[0][1][k]; ke = a / (c_ * np.sqrt(G * r0)); g1 = abs(np.log10(ke / .5)) <= .05
    sl = [np.log(rows[i][1][k] / a) / np.log(rows[i][0] / r0) for i in (1, 2)]; g2 = all(abs(s - .5) <= .05 for s in sl)
    zr = {z: routes(C0, z)[k] / a for z in ZB}; g3 = all(ZB[z][0] <= zr[z] <= ZB[z][1] for z in ZB)
    if k in ('T3', 'T4'):
        la = np.log10([halo(C0, m)[0 if k == 'T3' else 1] for m in LM]); g4 = la.std() <= .1; s4 = f'rms over mass {la.std():.3f} dex, range {la.min() - np.log10(A0):+.2f} to {la.max() - np.log10(A0):+.2f} dex vs a0'; g5 = True
    else: g4 = True; s4 = 'mass-free'; g5 = op[0] if k == 'T2' else op[1]
    v = dict(G1=g1, G2=g2, G3=g3, G4=g4, G5=g5); verdict[k] = all(v.values())
    print(f'{k}: a {a:.3e} ({a / A0:.3f} a0), kappa_eff {ke:.3f} [{"PASS" if g1 else "FAIL"} G1]; slopes {sl[0]:+.3f} {sl[1]:+.3f} [{"PASS" if g2 else "FAIL"} G2]; '
          f'a(z)/a(0) {", ".join(f"{z}: {x:.3f}" for z, x in zr.items())} [{"PASS" if g3 else "FAIL"} G3]; {s4} [{"PASS" if g4 else "FAIL"} G4]; [{"PASS" if g5 else "FAIL"} G5] -> {"TIES" if verdict[k] else "NO TIE"}')
print('A13 verdict:', 'a native LCDM route ties a to rho_DE' if any(verdict.values()) else 'NO native LCDM route ties a to rho_DE; the tie stays a hand term')
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
