"""A24: Verlinde emergent gravity on SPARC and the de Sitter tie, per ../FROZEN_A24.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
c_ = 2.998e8; H0 = cos.H0 * 1e3 / (kpc * 1e3); OL = cos.Ode0; RDE = OL * RHOC; AC = c_ * np.sqrt(G * RDE)
ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
AH = c_ * H0 / 6; AI = c_ * H0 * np.sqrt(OL) / 6; LAM = 8 * np.pi * G * RDE / c_**2; AS = c_**2 * np.sqrt(LAM)
print(f'H0 {cos.H0} km/s/Mpc, Ode0 {OL:.3f}; c sqrt(G rho_DE) {AC:.4e}; lib A0 {A0:.4e} (A0/that {A0 / AC:.4f})')
print(f'a_M = cH0/6 {AH:.4e} ({AH / A0:.3f} a0); a_M = cH_inf/6 {AI:.4e} ({AI / A0:.3f} a0); Hossenfelder c^2 sqrt(Lambda) {AS:.4e} ({AS / A0:.2f} a0)')
for g in GS:
    s = np.gradient(np.log(g.mb), np.log(g.r)); g.s1 = 1 + s; g.neg = g.s1 < 0
def vpt(g, a): return g.gb + np.sqrt(a * g.gb)
def vext(g, a): return g.gb + np.sqrt(a * g.gb * np.maximum(g.s1, 0))
NEG = np.concatenate([g.neg for g in GS])
print(f'1+s < 0 (M_D^2 < 0, g_D set 0): {NEG.sum()} of {len(NEG)} points, in {sum(g.neg.any() for g in GS)} of {len(GS)} galaxies; median 1+s {np.median(np.concatenate([g.s1 for g in GS])):.3f}, max {max(g.s1.max() for g in GS):.2f}')
rows = {}
rows['V0'] = grade('V0 point mass, a_M = cH0/6, 0 knobs', [vpt(g, AH) for g in GS])
rows['V1'] = grade('V1 extended eq 7.40, a_M = cH0/6, 0 knobs', [vext(g, AH) for g in GS])
rows['V2'] = grade('V2 point mass, a_M = cH_inf/6 (de Sitter), 0 knobs', [vpt(g, AI) for g in GS])
rows['V3'] = grade('V3 extended eq 7.40, a_M = cH_inf/6 (de Sitter), 0 knobs', [vext(g, AI) for g in GS])
rows['V5'] = grade('V5 Hossenfelder order-of-magnitude a = c^2 sqrt(Lambda), point mass, 0 knobs', [vpt(g, AS) for g in GS])
def rl(fn, f, sel): return np.sqrt(np.mean(np.concatenate([(np.log10(fn(GS[j], f * AH)) - np.log10(GS[j].gl))**2 for j in sel])))
ev, od, al = range(0, len(GS), 2), range(1, len(GS), 2), range(len(GS))
for nm, fn in (('V4', vext), ('V4p', vpt)):
    fa = 10**minimize_scalar(lambda x: rl(fn, 10**x, al), bounds=(-1, 1), method='bounded').x
    fe = 10**minimize_scalar(lambda x: rl(fn, 10**x, ev), bounds=(-1, 1), method='bounded').x
    atb = min(abs(np.log10(fa) + 1), abs(np.log10(fa) - 1)) < 1e-3
    rows[nm] = grade(f'{nm} {"extended" if fn is vext else "point mass"}, one global factor f on cH0/6 tuned on all', [fn(g, fa * AH) for g in GS], f'(1 knob: f {fa:.3f}, a {fa * AH / A0:.3f} a0, kappa_eff {fa * AH / AC:.3f}; at bound {atb})')
    hu = rl(fn, fe, od); print(f'{nm} holdout: f tuned on GS[::2] {fe:.3f}; unseen rms to law on GS[1::2] {hu:.4f} [{"PASS" if hu <= .025 else "FAIL"}]')
# diagnostic: V1 on in-regime points only
SB = np.concatenate([g.gb < c_ * H0 / 2 for g in GS]); IN = SB & ~NEG
d1 = np.log10(np.concatenate([vext(g, AH) for g in GS])) - np.log10(ALLL); do = np.log10(np.concatenate([vext(g, AH) for g in GS])) - np.log10(ALLO)
print(f'\nDIAG (not a gate) V1 on in-regime points (g_b < cH0/2 and 1+s >= 0), {IN.sum()} of {len(IN)}: rms to law {np.sqrt((d1[IN]**2).mean()):.4f}, mean {d1[IN].mean():+.4f}; rms to observed {np.sqrt((do[IN]**2).mean()):.4f}; law to observed on same points {np.sqrt(((np.log10(ALLL) - np.log10(ALLO))[IN]**2).mean()):.4f}')
# regime counts
hi_any = sum((g.gb >= c_ * H0 / 2).any() for g in GS); hi_half = sum((g.gb >= c_ * H0 / 2).mean() > .5 for g in GS)
nb = 0
for g in GS:
    a = np.loadtxt(os.path.join(D, 'sparc_data', g.n + '_rotmod.dat')); nb += (a[:, 5] != 0).any()
print(f'\nREGIME: Sigma_B >= a0/(8 pi G) (g_b >= cH0/2 = {c_ * H0 / 2:.3e}) at {(~SB).sum()} of {len(SB)} points; galaxies with any such point {hi_any}, with more than half {hi_half}')
print(f'REGIME: galaxies with 1+s < 0 somewhere {sum(g.neg.any() for g in GS)}; with a bulge component {nb}; flattened discs (not spherical) {len(GS)} of {len(GS)}; isolation and quasi-static state not assessable from SPARC')
print(f'REGIME: galaxies with every point in regime (g_b < cH0/2 and 1+s >= 0): {sum(((g.gb < c_ * H0 / 2) & ~g.neg).all() for g in GS)} of {len(GS)}')
# tie gates
def rde(OLx, H0x): Hs = H0x * 1e3 / (kpc * 1e3); return OLx * 3 * Hs**2 / (8 * np.pi * G), Hs
COS = [(.70, 67.4), (.685, 73.), (.65, 73.)]
print('\nTIE GATES (A13 G1-G5)')
M2 = np.array([m200_of(g.Ms) for g in GS]); sel = (np.log10(M2) >= 11) & (np.log10(M2) <= 12.5)
for nm, rd in (('H (H0 today, H(z) at epoch)', False), ('H_inf de Sitter c sqrt(Lambda/3)', True)):
    am = lambda OLx, H0x: c_ * rde(OLx, H0x)[1] * (np.sqrt(OLx) if rd else 1) / 6
    a = AI if rd else AH; ke = a / AC; g1 = abs(np.log10(ke / .5)) <= .05
    r0 = rde(*COS[0])[0]; a0c = am(*COS[0]); sl = [np.log(am(*COS[i]) / a0c) / np.log(rde(*COS[i])[0] / r0) for i in (1, 2)]; g2 = all(abs(x - .5) <= .05 for x in sl)
    zr = {z: (1. if rd else float(cos.Hz(z) / cos.H0)) for z in ZB}; g3 = all(ZB[z][0] <= zr[z] <= ZB[z][1] for z in ZB)
    fn = vext; ae = np.array([fit_a(g.gb, fn(g, a)) for g in GS]); sp = np.log10(ae[sel]).std(); g4 = sp <= .1
    gd = np.sqrt(a * G * 1e10 * Msun / (10 * kpc)**2); g5 = gd >= .1 * A0
    print(f'{nm}: a_M {a / A0:.3f} a0, kappa_eff {ke:.3f} ({np.log10(ke / .5):+.3f} dex) [{"PASS" if g1 else "FAIL"} G1]; slopes {sl[0]:+.3f} {sl[1]:+.3f} [{"PASS" if g2 else "FAIL"} G2]; '
          f'a(z)/a(0) ' + ', '.join(f'{z}: {x:.3f}' for z, x in zr.items()) + f' [{"PASS" if g3 else "FAIL"} G3]; per-galaxy effective a (extended) over {sel.sum()} hosts log M200 11-12.5: median {np.median(ae[sel]) / A0:.3f} a0, rms {sp:.3f} dex [{"PASS" if g4 else "FAIL"} G4]; '
          f'g_D(10 kpc, 1e10 Msun) {gd / A0:.2f} a0 [PASS G5 by posit] -> {"TIES" if all((g1, g2, g3, g4, g5)) else "NO TIE"}')
    aep = np.array([fit_a(g.gb, vpt(g, a)) for g in GS]); print(f'   point-mass form per-galaxy effective a: median {np.median(aep[sel]) / A0:.3f} a0, rms {np.log10(aep[sel]).std():.3f} dex (diagnostic)')
ke5 = AS / AC; print(f'V5 Hossenfelder a = c^2 sqrt(Lambda): kappa_eff {ke5:.3f} = sqrt(8 pi) ({np.log10(ke5 / .5):+.3f} dex) [{"PASS" if abs(np.log10(ke5 / .5)) <= .05 else "FAIL"} G1]; slope 0.5 by construction; flat in z; prefactor not fixed in the paper')
print(f'\nlaw itself to observed: {np.sqrt(np.mean((np.log10(ALLL) - np.log10(ALLO))**2)):.4f} dex')
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
