"""A37: modified inertia from the de Sitter Unruh effect (Milgrom 1999; quantised inertia; arXiv 2602.14515), per ../FROZEN_A37.md.
A rival modified-inertia route, not LCDM. Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
T0 = time.time()
s31 = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read(); exec(s31[s31.index('OR_H2 ='):s31.index('S30 =')])  # A29 backgrounds, unchanged
c_ = 2.998e8; MPC = kpc * 1e3; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); LAM = 8 * np.pi * G * RDE / c_**2
AL = c_**2 * np.sqrt(LAM / 3); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; ZS = [0., 1., 1.5, 2.33]
P = lambda b: 'PASS' if b else 'FAIL'
def chi_p(C, z):  # comoving particle horizon c int_z^inf dz/H, colossus (no radiation)
    u = np.linspace(np.log1p(z), np.log(1e6), 40001); zz = np.expm1(u); H = C.Hz(zz) * 1e3 / MPC
    return c_ * np.trapz((1 + zz) / H, u)
TH_C = 2 * chi_p(cos, 0.)
print(f'A37 recipe38; c sqrt(G rho_DE) {AC:.4e} (A0/that {A0 / AC:.4f}); a_L = c^2 sqrt(Lambda/3) = cH_inf {AL:.4e} ({AL / A0:.3f} A0); comoving horizon diameter of lib cosmology {TH_C:.3e} m')
# ---------- shapes (stable forms) ----------
def s9(gb, A): d = A / gb; return gb * np.sqrt(1 + d)                           # g = sqrt(gb^2 + A gb)
def s11(gb, A): e = 4 * A**2 / gb**2; return gb * np.sqrt((1 + np.sqrt(1 + e)) / 2)  # g mu(g/A) = gb, mu = x/sqrt(1+x^2)
def ssq(gb, A): return gb + np.sqrt(A * gb)                                   # A22-A24 family
def slaw(gb, A): return law(gb, A)
def slin(gb, A): return gb + A                                                # R2 Eq. 1 solved literally
def boost(fn, gb, A):  # g - gb without cancellation
    if fn is s9: d = A / gb; return gb * d / (np.sqrt(1 + d) + 1)
    if fn is s11: e = 4 * A**2 / gb**2; dl = e / (2 * (np.sqrt(1 + e) + 1)); return gb * dl / (np.sqrt(1 + dl) + 1)
    if fn is slaw: return 2 * A * gb / (np.sqrt(gb**2 + 4 * A * gb) + gb)
    if fn is ssq: return np.sqrt(A * gb)
    return A
# ---------- (a) 0-knob rows ----------
ROWS = {'M9': (s9, 2 * AL, 'R1 Eq. 9, A = 2 c^2 sqrt(Lambda/3)'), 'M11': (s11, AL, 'R1 Eq. 11 (standard mu), A = c^2 sqrt(Lambda/3)'),
        'QI': (s9, 2 * c_**2 / 8.8e26, 'R2 Eq. 8, Theta 8.8e26 m (published)'), 'QIe': (s9, 2 * c_**2 / 2.6e26, 'R2 Eq. 8, Theta 2.6e26 m (earlier value)'),
        'QIc': (s9, 2 * c_**2 / TH_C, f'R2 Eq. 8, Theta {TH_C:.3e} m (lib cosmology horizon)'), 'F26': (s9, AL / 2, 'R3 Eq. 21, A = 2 a_bg = c^2 sqrt(Lambda/3)/2'),
        'QIlin': (slin, 2 * c_**2 / 8.8e26, 'diagnostic, R2 Eq. 1 solved literally g = g_b + 2c^2/Theta')}
print('\n(a) 0 knobs')
for k, (fn, A, txt) in ROWS.items():
    grade(f'{k}: {txt}', [fn(g.gb, A) for g in GS], f'(A {A:.4e} = {A / A0:.3f} A0, kappa_eff {A / AC:.4f})')
# ---------- (a') 1 knob ----------
def rl(fn, A, sel): return np.sqrt(np.mean(np.concatenate([(np.log10(fn(GS[j].gb, A)) - np.log10(GS[j].gl))**2 for j in sel])))
ev, od, al = range(0, len(GS), 2), range(1, len(GS), 2), range(len(GS))
def fitA(fn, sel, tgt=None):
    if tgt is None: f = lambda x: rl(fn, 10**x, sel)
    else: f = lambda x: np.sqrt(np.mean((np.log10(fn(ALLB, 10**x)) - np.log10(ALLO))**2))
    r = minimize_scalar(f, bounds=(-12, -8), method='bounded'); return 10**r.x, min(abs(r.x + 12), abs(r.x + 8)) < 1e-3
print("\n(a') 1 knob (A free, log bounds 1e-12 to 1e-8)")
for nm, fn in (('S9 sqrt(g_b^2 + A g_b) [M9, QI, F26 family]', s9), ('S11 standard mu [M11]', s11), ('g_b + sqrt(A g_b) [A22-A24 family]', ssq), ('law form (control)', slaw)):
    Aa, ba = fitA(fn, al); Ae, _ = fitA(fn, ev); Ao, _ = fitA(fn, al, 'obs')
    grade(f'{nm}, tuned on all', [fn(g.gb, Aa) for g in GS], f'(1 knob: A {Aa:.4e} = {Aa / A0:.4f} A0, kappa_eff {Aa / AC:.4f}; at bound {ba})')
    hu = rl(fn, Ae, od); print(f' holdout: A tuned on GS[::2] {Ae:.4e}; unseen rms to law on GS[1::2] {hu:.4f} [{P(hu <= .025)}]; A fitted to observed {Ao:.4e} ({np.log10(Ao / A0):+.3f} dex vs A0)')
gsat0 = 1.327e20 / (9.537 * 1.496e11)**2
# DIAGNOSTIC added after the first run (post hoc, not a frozen row): S9 passed E1, E2 and holdout, failed E3; is there any A that passes all three?
def e123(fn, A):
    cur = [fn(g.gb, A) for g in GS]; gt = np.concatenate(cur); d = np.log10(gt) - np.log10(ALLL); idx = np.cumsum([0] + [len(c) for c in cur])
    per = np.array([np.sqrt((d[idx[i]:idx[i + 1]]**2).mean()) for i in range(len(cur))]); b = np.floor(np.log10(ALLB) * 2) / 2
    e3 = max(abs(d[b == v].mean()) for v in np.unique(b) if (b == v).sum() >= 50); return np.sqrt((d**2).mean()), np.percentile(per, 95), e3
LA = np.linspace(np.log10(.8 * A0), np.log10(2 * A0), 241); EE = np.array([e123(s9, 10**x) for x in LA]); i3 = EE[:, 2].argmin(); ok = (EE[:, 0] <= .02) & (EE[:, 1] <= .04) & (EE[:, 2] <= .02)
print(f'\nDIAG (post hoc) S9 scan A 0.8-2 A0 (241 pts): min worst bin {EE[i3, 2]:.4f} at A {10**LA[i3] / A0:.4f} A0 (E1 {EE[i3, 0]:.4f}, E2 {EE[i3, 1]:.4f}); A values passing E1+E2+E3 together: {ok.sum()}')
Af = fitA(s9, al)[0]; print(f'DIAG S9 at fitted A {Af / A0:.4f} A0: kappa_eff {Af / AC:.4f} ({np.log10(Af / AC / .5):+.3f} dex) [{P(abs(np.log10(Af / AC / .5)) <= .05)} G1]; Saturn anomaly {boost(s9, gsat0, Af) / A0:.2f} a0 [{P(boost(s9, gsat0, Af) < 1e-3 * A0)} A9 solar]; ratio to R1 Eq. 9 value 2 a_L: {Af / (2 * AL):.4f}; to R2 published 2c^2/Theta: {Af / (2 * c_**2 / 8.8e26):.4f}; to R3 a_L/2: {Af / (AL / 2):.4f}')
# shape comparison at fixed deep limit
x = np.array([.01, .1, .3, 1., 3., 10., 100.])
print('\nshape at equal deep-limit constant A (g/A against g_b/A): g_b/A ' + ' '.join(f'{v:g}' for v in x))
for nm, fn in (('law', slaw), ('S9', s9), ('S11', s11), ('g_b+sqrt', ssq)):
    print(f'  {nm:9s} ' + ' '.join(f'{fn(v, 1.):.4f}' for v in x) + '  log10 vs law ' + ' '.join(f'{np.log10(fn(v, 1.) / slaw(v, 1.)):+.3f}' for v in x))
# ---------- tie gates ----------
def rde_J(OLx, H0x): Hs = H0x * 1e3 / MPC; return OLx * 3 * Hs**2 / (8 * np.pi * G)
COS = [(.70, 67.4), (.685, 73.), (.65, 73.)]
CJ = [cc.Cosmology(name=f'a37J{i}', flat=True, H0=h, Om0=1 - o, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False, persistence='', print_warnings=False) for i, (o, h) in enumerate(COS)]
THJ = [2 * chi_p(C, 0.) for C in CJ]; cc.setCurrent(cos)
M2 = np.array([m200_of(g.Ms) for g in GS]); sel = (np.log10(M2) >= 11) & (np.log10(M2) <= 12.5)
gsat = 1.327e20 / (9.537 * 1.496e11)**2; THR = 1e-3 * A0
print(f'\nTIE GATES (A13 G1-G5, A24 rules); Saturn g_N {gsat:.3e}, A9 threshold {THR:.2e}')
for k in ('M9', 'M11', 'QI', 'QIe', 'QIc', 'F26'):
    fn, A, txt = ROWS[k]; ke = A / AC; g1 = abs(np.log10(ke / .5)) <= .05
    if k.startswith('QI'):
        aJ = [2 * c_**2 / (t if k == 'QIc' else {'QI': 8.8e26, 'QIe': 2.6e26}[k]) for t in THJ]; zr = {z: 1 + z for z in ZB}
    else:
        aJ = [A / AL * c_**2 * np.sqrt(8 * np.pi * G * rde_J(*j) / c_**2 / 3) for j in COS]; zr = {z: 1. for z in ZB}
    r0 = rde_J(*COS[0]); sl = [np.log(aJ[i] / aJ[0]) / np.log(rde_J(*COS[i]) / r0) for i in (1, 2)]; g2 = all(abs(s - .5) <= .05 for s in sl)
    g3 = all(ZB[z][0] <= zr[z] <= ZB[z][1] for z in ZB)
    ae = np.array([fit_a(g.gb, fn(g.gb, A)) for g in GS]); sp = np.log10(ae[sel]).std(); g4 = sp <= .1
    gN = G * 1e10 * Msun / (10 * kpc)**2; b5 = boost(fn, gN, A); g5 = b5 >= .1 * A0; bs = boost(fn, gsat, A)
    print(f'{k}: A {A / A0:.3f} A0, kappa_eff {ke:.4f} ({np.log10(ke / .5):+.3f} dex) [{P(g1)} G1]; slopes {sl[0]:+.3f} {sl[1]:+.3f} [{P(g2)} G2]; a(z)/a(0) '
          + ', '.join(f'{z}: {v:.3f}' for z, v in zr.items()) + f' [{P(g3)} G3]; per-galaxy effective a over {sel.sum()} hosts: median {np.median(ae[sel]) / A0:.3f} A0, rms {sp:.3f} dex [{P(g4)} G4]; '
          f'boost at 10 kpc (1e10 Msun) {b5 / A0:.2f} a0 [PASS G5 by posit]; Saturn anomaly {bs:.2e} m/s^2 = {bs / A0:.1e} a0 [{P(bs < THR)} A9 solar] -> {"TIES" if all((g1, g2, g3, g4, g5)) else "NO TIE"}')
print(f'QIc Theta in J cosmologies: ' + ', '.join(f'{t:.3e}' for t in THJ) + ' m')
bl = boost(slaw, gsat, A0); print(f'control, bare law at A0: Saturn anomaly {bl:.2e} m/s^2 = {bl / A0:.2f} a0 [{P(bl < THR)} A9 solar] (bare formula; not a verdict on the framework)')
print(f'reference: Milgrom coincidence 2 pi a0 = c^2 sqrt(Lambda/3) (A13 T2): kappa_eff {AL / (2 * np.pi) / AC:.4f}; not the value R1 Eq. 9 or 11 gives')
# ---------- (c) GT in A29 backgrounds ----------
print('\n(c) GT in A29 backgrounds (L1 hand generalisation Lambda -> rho_DE(z); L2 FRW horizon H(z); QIz R2 Eq. 9 (1+z); QIp physical horizon; F26q sqrt(-q) H/4)')
for bn, de in BG.items():
    C = mk(de, .811); cc.setCurrent(C); h = C.h
    rd = {z: C.rho_de(z) for z in ZS}; H = {z: C.Hz(z) * 1e3 / MPC for z in ZS}; w = {z: float(C.wz(z)) for z in ZS}
    q = {z: .5 * float(C.Om(z)) + .5 * float(C.Ode(z)) * (1 + 3 * w[z]) for z in ZS}
    r = {z: rd[z] / rd[0.] for z in ZS}; lnr = np.log(max(r.values()) / min(r.values())); meas = lnr >= .1
    chi = {z: chi_p(C, z) for z in ZS}
    R = {'L1': {z: np.sqrt(r[z]) for z in ZS}, 'L2': {z: H[z] / H[0.] for z in ZS}, 'QIz': {z: 1 + z for z in ZS},
         'QIp': {z: (chi[0.] * 1.) / (chi[z] / (1 + z)) for z in ZS}}
    print(f' {bn} {de.get("w0", "")} {de.get("wa", "")}: rho_DE(z)/rho_DE0 ' + ' '.join(f'{r[z]:.4f}' for z in ZB) + '; q(z) ' + ' '.join(f'{q[z]:+.3f}' for z in ZS)
          + f'; Theta_now {2 * chi[0.]:.3e} m; G2z {"measurable" if meas else "NOT MEASURABLE"}')
    for k, a in R.items():
        dv = {z: np.log10(a[z]) - .5 * np.log10(r[z]) for z in ZB}; gtp = all(abs(v) <= .05 for v in dv.values()); g3 = all(ZB[z][0] <= a[z] <= ZB[z][1] for z in ZB)
        s2 = float(np.polyfit(np.log([r[z] for z in ZS]), np.log([a[z] for z in ZS]), 1)[0]) if meas else None
        print(f'  {k:4s} a(z)/a(0) ' + ' '.join(f'{a[z]:.4f}' for z in ZB) + f' [{P(g3)} G3]; GT dev ' + ' '.join(f'{dv[z]:+.4f}' for z in ZB) + f' [{P(gtp)} GT]; G2z '
              + (f'{s2:+.4f} [{P(abs(s2 - .5) <= .05)}]' if meas else 'not measurable'))
    fq = {z: (np.sqrt(-q[z]) * c_ * H[z] / 4 if q[z] < 0 else np.nan) for z in ZS}
    print(f'  F26q a_bg(z) = sqrt(-q) H/4: ' + ' '.join(f'z {z}: ' + ('undefined (q > 0)' if np.isnan(fq[z]) else f'{fq[z] / fq[0.]:.4f} of today') for z in ZS) + (f'; today 2 a_bg {2 * fq[0.] / A0:.3f} A0' if not np.isnan(fq[0.]) else ''))
    cc.setCurrent(cos)
print(f'\nruntime {time.time() - T0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB (macOS bytes)')
print('Rival modified-inertia route, not LCDM. Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
