"""A31: time-varying DM-DE coupling, running vacuum, unified dark fluids, per ../FROZEN_A31.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os, time; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.integrate import solve_ivp
T0 = time.time()
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
ZS = [0.] + list(ZB); OB, OC, OV = cos.Ob0, cos.Om0 - cos.Ob0, cos.Ode0; CL = 400.; FS = [.5, .71, 1., 1.41, 2.]
CGZ = {z: (CG if z == 0 else np.array([float(CM.concentration(10**m * cos.h, '200c', z, model='diemer19')) for m in LM])) for z in ZS}
def cz(M, z): return np.interp(np.log10(M), LM, CGZ[z])
CC = np.linspace(1.5, 60, 4000); YC = CC**3 * mu(1.) / mu(CC)
print(f'base OL {OV:.3f}; c sqrt(G rho_DE) {AC:.4e}; a0 {A0:.4e}; Ludlow C {CL:.0f} (from memory)')

# ---------- background + geodesic growth, vectorised RK4 over models ----------
NS = 2000; XS = np.linspace(0, np.log(1e-3), 2 * NS + 1); HB = XS[1] - XS[0]
def QH(typ, X0, X1, x, b, c, v):
    xi = X0 + X1 * (1 - np.exp(x))
    if typ == 'Qc': return xi * c
    if typ == 'Qv': return xi * v
    if typ == 'Qm': return xi * c * v / (c + v)
    return -3 * X0 * (b + c)                      # RVM, X0 = nu
def qf(typ, X0, X1, x, b, c, v):
    xi = X0 + X1 * (1 - np.exp(x))
    if typ == 'Qc': return 0. * c
    if typ == 'Qv': return xi * v / c
    if typ == 'Qm': return xi * c * v / (c + v)**2
    return -3 * X0 * (b + c) / c
def integ(typ, X0, X1, f=1.):
    X0 = np.asarray(X0, float); X1 = np.asarray(X1, float); n = len(X0)
    rc = np.empty((len(XS), n)); rv = np.empty((len(XS), n)); rc[0] = OC; rv[0] = f * OV; rb = OB * np.exp(-3 * XS)
    def bg(x, c, v):
        q = QH(typ, X0, X1, x, OB * np.exp(-3 * x), c, v); return -3 * c - q, q
    with np.errstate(all='ignore'):
        for j in range(len(XS) - 1):
            x, c, v = XS[j], rc[j], rv[j]
            a1, b1 = bg(x, c, v); a2, b2 = bg(x + HB / 2, c + HB / 2 * a1, v + HB / 2 * b1)
            a3, b3 = bg(x + HB / 2, c + HB / 2 * a2, v + HB / 2 * b2); a4, b4 = bg(x + HB, c + HB * a3, v + HB * b3)
            rc[j + 1] = c + HB / 6 * (a1 + 2 * a2 + 2 * a3 + a4); rv[j + 1] = v + HB / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
        ok = np.isfinite(rc).all(0) & np.isfinite(rv).all(0) & (rc > 0).all(0) & (rv[np.exp(XS) > 1 / 11] >= 0).all(0)
        def pt(j, dc, db, u):
            b, c, v, x = rb[j], rc[j], rv[j], XS[j]; E2 = b + c + v; dl = -1.5 * (b + c) / E2
            return u + qf(typ, X0, X1, x, b, c, v) * dc, u, -(2 + dl) * u + 1.5 * (c * dc + b * db) / E2
        y = [np.full(n, 1e-3)] * 3; Dr = np.empty((NS + 1, n)); H = -2 * HB
        j = len(XS) - 1; Dr[NS] = 1e-3
        while j > 0:
            k1 = pt(j, *y); k2 = pt(j - 1, *[a + H / 2 * k for a, k in zip(y, k1)]); k3 = pt(j - 1, *[a + H / 2 * k for a, k in zip(y, k2)])
            k4 = pt(j - 2, *[a + H * k for a, k in zip(y, k3)]); y = [a + H / 6 * (p + 2 * q + 2 * r + s) for a, p, q, r, s in zip(y, k1, k2, k3, k4)]
            j -= 2; Dr[j // 2] = (rc[j] * y[0] + rb[j] * y[1]) / (rb[j] + rc[j])
        ok &= np.isfinite(Dr).all(0) & (Dr > 0).all(0)
    E2 = (rb[:, None] + rc + rv)[::2]; rvf = rv[::2]
    a = np.exp(XS[::2])[::-1]; z = 1 / a - 1
    return dict(z=z, E2=E2[::-1], rv=rvf[::-1], D=Dr[::-1], ok=ok)
def mfun(R, i, foot):
    z, E2, rv, D = R['z'], R['E2'][:, i], R['rv'][:, i], R['D'][:, i]
    if foot == 'S8': D = D / D[-1]
    return dict(E2=lambda zz: np.interp(-zz, -z, E2), D=lambda zz: np.interp(-zz, -z, D), Dinv=lambda d: np.interp(d, D, z), rv=lambda zz: np.interp(-zz, -z, rv), zmax=z[0])
LR = integ('Qc', [0.], [0.]); LCF = {ft: mfun(LR, 0, ft) for ft in ('S8', 'P')}
ZG = np.linspace(0, 40, 40001); EL2 = OB * (1 + ZG)**3 + OC * (1 + ZG)**3 + OV
CLIP = [0, 0]
def g_iv(Mv, z, m, L):
    cL = cz(Mv, z); rb_ = 200 * np.interp(z, ZG, EL2) * cL**3 * mu(1.) / mu(cL); zfL = np.interp(rb_ / CL, EL2, ZG)
    dlt = 1 / L['D'](zfL) - 1 / L['D'](z); zf = m['Dinv'](1 / (dlt + 1 / m['D'](z)))
    rbar = CL * m['E2'](zf); y = rbar / (200 * m['E2'](z)); cI = np.interp(y, YC, CC)
    CLIP[0] += int(((y < YC[0]) | (y > YC[-1])).sum()); CLIP[1] += int((zf >= m['zmax'] - 1).sum())
    rc = m['E2'](z) * RHOC; R = (3 * Mv * Msun / (800 * np.pi * rc))**(1 / 3); rs = R / cI; rhos = Mv * Msun / (4 * np.pi * rs**3 * mu(cI))
    return 2 * np.pi * G * rhos * rs
M2 = np.array([m200_of(g.Ms) for g in GS]); Mm = np.median(M2); SEL = (np.log10(M2) >= 11) & (np.log10(M2) <= 12.5)
g0 = g_iv(M2, 0., LCF['S8'], LCF['S8'])
print(f'(a) control zero coupling: median g {np.median(g0) / A0:.3f} a0 (A15 0.612), kappa_eff {np.median(g0) / AC:.3f}; RK4 LCDM D(z=1)/D(0) {LCF["S8"]["D"](1.):.4f}')
print(f'median log M200 {np.log10(Mm):.2f}; hosts with log M200 11-12.5: {SEL.sum()} of {len(GS)}')
def grade_pt(m, L, f=1.):
    gi = g_iv(M2, 0., m, L); ke = np.median(gi) / (c_ * np.sqrt(G * f * RDE)); sp = np.log10(gi).std(); sp2 = np.log10(gi[SEL]).std()
    g00 = g_iv(np.array([Mm]), 0., m, L)[0]; gz = {z: float(g_iv(np.array([Mm]), z, m, L)[0] / g00) for z in ZB}
    gt = {z: np.log10(gz[z]) - .5 * np.log10(m['rv'](z) / m['rv'](0.)) for z in ZB}
    k = dict(G1=abs(np.log10(ke / .5)) <= .05, G3=all(ZB[z][0] <= gz[z] <= ZB[z][1] for z in ZB), G4=sp <= .1, GT=all(abs(gt[z]) <= .05 for z in ZB))
    return dict(gi=gi, ke=ke, sp=sp, sp2=sp2, gz=gz, gt=gt, k=k)
def scan(typ, X0, X1):
    R = {f: integ(typ, X0, X1, f) for f in FS}; rows = []
    for i in range(len(X0)):
        if not R[1.]['ok'][i]: rows.append(None); continue
        d = {ft: grade_pt(mfun(R[1.], i, ft), LCF[ft]) for ft in ('S8', 'P')}
        meds = []
        for f in FS:
            if not R[f]['ok'][i]: meds = None; break
            meds.append(np.median(g_iv(M2, 0., mfun(R[f], i, 'P'), LCF['P'])))
        sl = np.polyfit(np.log(FS), np.log(meds), 1)[0] if meds is not None else np.nan
        g2 = bool(abs(sl - .5) <= .05)
        for ft in d: d[ft]['k']['G2'] = g2
        rows.append(dict(x0=X0[i], x1=X1[i], d=d, sl=sl))
    return rows
def J(dd): return (np.log10(dd['ke'] / .5) / .05)**2 + sum((dd['gt'][z] / .05)**2 for z in ZB)
GN = ('G1', 'G2', 'G3', 'G4', 'GT')
def report(tag, typ, rows, nfmt):
    print(f'\n{tag}: columns {nfmt}; S8: kappa_eff, spread171, spread(11-12.5), g(z)/g0 z1,1.5,2.33, GT z1,1.5,2.33 | P: kappa_eff, GT | G2 slope (P) | flags G1 G2 G3 G4 GT on S8 / joint S8 joint P')
    sk = 0; ok = [r for r in rows if r is not None]
    for r in rows:
        if r is None: sk += 1; continue
        s, p = r['d']['S8'], r['d']['P']
        js, jp = all(s['k'][g] for g in GN), all(p['k'][g] for g in GN)
        print(f' {typ} {r["x0"]:+.4f} {r["x1"]:+.2f} | {s["ke"]:.3f} {s["sp"]:.3f} {s["sp2"]:.3f} ' + ' '.join(f'{s["gz"][z]:.3f}' for z in ZB) + ' ' + ' '.join(f'{s["gt"][z]:+.3f}' for z in ZB)
              + f' | {p["ke"]:.3f} ' + ' '.join(f'{p["gt"][z]:+.3f}' for z in ZB) + f' | {r["sl"]:+.3f} | ' + ''.join('P' if s['k'][g] else 'F' for g in GN) + f' {"J" if js else "-"}{"J" if jp else "-"}')
    print(f' {typ} skipped (rho_c <= 0 or rho_v < 0 below z 10, or non-finite): {sk} of {len(rows)}')
    for g in GN: print(f' {typ} {g} passes (S8) at {sum(r["d"]["S8"]["k"][g] for r in ok)} of {len(ok)}')
    both = [r for r in ok if r['d']['S8']['k']['G1'] and r['d']['S8']['k']['GT']]
    print(f' {typ} G1 and GT jointly (S8): {len(both)} points: ' + ', '.join(f'({r["x0"]:+.4g},{r["x1"]:+.2f}) G2 {r["sl"]:+.3f} G3 {"P" if r["d"]["S8"]["k"]["G3"] else "F"} G4 {r["d"]["S8"]["sp"]:.3f}' for r in both[:40]))
    bothP = [r for r in ok if r['d']['P']['k']['G1'] and r['d']['P']['k']['GT']]
    print(f' {typ} G1 and GT jointly (P): {len(bothP)} points: ' + ', '.join(f'({r["x0"]:+.4g},{r["x1"]:+.2f})' for r in bothP[:40]))
    for ft in ('S8', 'P'): print(f' {typ} ALL gates jointly ({ft}):', [f'({r["x0"]:+.4g},{r["x1"]:+.2f})' for r in ok if all(r['d'][ft]['k'][g] for g in GN)] or 'none')
    print(f' {typ} G2 slope range over valid points: {np.nanmin([r["sl"] for r in ok]):+.3f} to {np.nanmax([r["sl"] for r in ok]):+.3f}; G4 spread range {min(r["d"]["S8"]["sp"] for r in ok):.3f} to {max(r["d"]["S8"]["sp"] for r in ok):.3f}')
    b = min(ok, key=lambda r: J(r['d']['S8'])); s = b['d']['S8']
    print(f' {typ} min-J (S8) at ({b["x0"]:+.4g},{b["x1"]:+.2f}): J {J(s):.2f}, kappa_eff {s["ke"]:.3f}, GT ' + ' '.join(f'{s["gt"][z]:+.3f}' for z in ZB) + f', G2 {b["sl"]:+.3f}, G3 ' + ' '.join(f'{s["gz"][z]:.3f}' for z in ZB) + f', G4 {s["sp"]:.3f}/{s["sp2"]:.3f}; flags ' + ''.join('P' if s['k'][g] else 'F' for g in GN))
    grade(f'{typ} DIAG law swap a = g_i at min-J point', [law(g.gb, a) for g, a in zip(GS, s['gi'])])
    return ok

# ---------- (a) ----------
XG = np.round(np.linspace(-1, 1, 21), 2); X0, X1 = [v.ravel() for v in np.meshgrid(XG, XG, indexing='ij')]
CTL = scan('Qv', np.array([-.6, -.5, 0.]), np.zeros(3))
print('\n(a) recipe22 check, Qv xi1 = 0: ' + ', '.join(f'xi0 {r["x0"]:+.1f}: kappa_eff {r["d"]["S8"]["ke"]:.3f}' for r in CTL) + ' (recipe22 0.539, 0.465, 0.306)')
RES = {}
for typ in ('Qc', 'Qv', 'Qm'):
    RES[typ] = report(f'(a) {typ}, xi(a) = xi0 + xi1 (1 - a)', typ, scan(typ, X0, X1), 'xi0 xi1')
    print(f' elapsed {time.time() - T0:.0f} s')
# ---------- (b) ----------
NU = np.sort(np.concatenate([np.round(np.linspace(-.3, .3, 61), 3), [1e-4, -1e-4, 3e-4, -3e-4, 1e-3, -1e-3, 3e-3, -3e-3]]))
RES['RVM'] = report('(b) running vacuum, rho_v = rho_v0 + nu (E^2 - 1) rho_c0, exchange with dark matter', 'RVM', scan('RVM', NU, np.zeros(len(NU))), 'nu 0')
pl = [r for r in RES['RVM'] if abs(r['x0']) <= 3e-3]
print(f' RVM at |nu| <= 3e-3 (literature range, provisional): kappa_eff {min(r["d"]["S8"]["ke"] for r in pl):.3f} to {max(r["d"]["S8"]["ke"] for r in pl):.3f}')
print(f'mapping clips over the whole run: c outside [1.5, 60] {CLIP[0]}, z_f at grid top {CLIP[1]}; elapsed {time.time() - T0:.0f} s')

# ---------- (c1) generalised Chaplygin gas ----------
print('\n(c1) generalised Chaplygin gas P = -A/rho^alpha')
AS = OV / (OC + OV); RH0 = (OC + OV) * RHOC
def hal(M):
    rc = RHOC; R = (3 * M * Msun / (800 * np.pi * rc))**(1 / 3); c = cz(M, 0.); rs = R / c; rhos = M * Msun / (4 * np.pi * rs**3 * mu(c)); return rs, rhos
RS, RHS = hal(M2); RL = np.array([g.r[-1] for g in GS]); XL = RL / RS
rhoL = RHS / (XL * (1 + XL)**2); rhoS = RHS / 4; dlnr = (1 + 3 * XL) / (1 + XL) / RL   # |dln rho/dr| at r_last
print(f' A_s {AS:.4f} (derived from base); rho_0 dark today {RH0:.3e} kg/m^3; hosts: rho(r_s) median {np.median(rhoS) / RH0:.3e} rho_0, rho(r_last) median {np.median(rhoL) / RH0:.3e} rho_0 (range {rhoL.min() / RH0:.2e} to {rhoL.max() / RH0:.2e})')
for al in (1e-5, 1e-3, 1e-2, .1, .5, 1.):
    rst = RH0 * (3 * AS)**(1 / (1 + al)); wL = -AS * (RH0 / rhoL)**(1 + al); cs2 = al * AS * c_**2 * (RH0 / rhoL)**(1 + al); aP = cs2 * dlnr
    ke = np.median(aP) / AC; sp = np.log10(aP).std(); kst = c_ * np.sqrt(G * rst) / AC
    gtz = {z: .5 * al * np.log10((AS + (1 - AS) * (1 + z)**(3 * (1 + al)))**(1 / (1 + al))) for z in ZB}
    print(f' alpha {al:g}: rho_* {rst / RH0:.3f} rho_0; rho(r_last)/rho_* median {np.median(rhoL) / rst:.2e}; w at r_last median {np.median(wL):.2e}; a_P OUTWARD, median {np.median(aP) / A0:.2e} a0 (max {aP.max() / A0:.2e})'
          f' [G5 {"PASS" if False else "FAIL"}: outward]; G1 kappa_eff {ke:.2e} [{"PASS" if abs(np.log10(ke / .5)) <= .05 else "FAIL"}]; G4 {sp:.3f} [{"PASS" if sp <= .1 else "FAIL"}]; G2 slope {1 + al:.3f} (analytic) [{"PASS" if abs(1 + al - .5) <= .05 else "FAIL"}];'
          f' G3 1 [PASS]; GT ' + ' '.join(f'{gtz[z]:+.4f}' for z in ZB) + f' [{"PASS" if all(abs(v) <= .05 for v in gtz.values()) else "FAIL"}]; c sqrt(G rho_*) kappa_eff {kst:.3f} [G1 {"PASS" if abs(np.log10(kst / .5)) <= .05 else "FAIL"}, G5 FAIL: not a force at galaxy radii]')
# ---------- (c2) logotropic dark fluid ----------
print('\n(c2) logotropic dark fluid P = A ln(rho/rho_P)')
hbar = 1.0546e-34; RP = c_**5 / (hbar * G**2); B = 1 / (np.log(RP / (OC * RHOC)) - 1); A = B * RDE * c_**2; gA = np.sqrt(4 * np.pi * G * A)
s = solve_ivp(lambda t, y: [-y[0]**2 * y[1] / np.exp(2 * t) * np.exp(t), np.exp(3 * t) * y[0]], (np.log(1e-5), np.log(1e7)), [1 - 1e-10 / 6, 1e-15 / 3], dense_output=True, rtol=1e-10, atol=1e-30)
LX = np.linspace(np.log(1e-5), np.log(1e7), 20001); th, mm = s.sol(LX); xi_ = np.exp(LX); hh = mm / xi_**2
ih = np.argmin(abs(th - .25)); im = np.argmax(hh)
print(f' rho_P {RP:.3e} kg/m^3; B {B:.4e} (Chavanis ~3.53e-3, provisional); A {A:.3e} Pa; sqrt(4 pi G A) {gA:.3e} m/s^2 = {gA / A0:.3f} a0')
print(f' Lane-Emden: g/sqrt(4 pi G A) = m/xi^2: max {hh[im]:.4f} at xi {xi_[im]:.2f}; at r_h (theta 1/4, xi_h {xi_[ih]:.3f}) {hh[ih]:.4f}; at xi 1e7 {hh[-1]:.4f} (asymptote 1/sqrt 2 = 0.7071); theta xi at 1e7 {th[-1] * xi_[-1]:.4f} (asymptote sqrt 2 = 1.4142)')
for nm, v in (('max of g', hh[im]), ('asymptote', hh[-1]), ('r_h', hh[ih])):
    ke = np.sqrt(4 * np.pi * B) * v; print(f' kappa_eff at {nm}: {ke:.4f} ({np.log10(ke / .5):+.3f} dex) [G1 {"PASS" if abs(np.log10(ke / .5)) <= .05 else "FAIL"}]')
S0 = np.sqrt(A / (4 * np.pi * G)) * xi_[ih] * (3.0857e16)**2 / Msun
print(f' Sigma_0 = rho_0 r_h = {S0:.1f} Msun/pc^2 (Donato+09 ~141, provisional); G Sigma_0 = {G * S0 * Msun / 3.0857e16**2 / A0:.3f} a0')
rmc = OC * RHOC; gtz = {z: -.5 * np.log10((np.log(RP / (rmc * (1 + z)**3)) - 1) / (np.log(RP / rmc) - 1)) for z in ZB}
print(f' G2 slope 0.500 at fixed rho_c0 (A = B rho_DE0 c^2, analytic) [PASS]; G3 a(z)/a(0) = 1 [PASS]; GT ' + ' '.join(f'{gtz[z]:+.4f}' for z in ZB) + f' [{"PASS" if all(abs(v) <= .05 for v in gtz.values()) else "FAIL"}] (rho_DE(z)/rho_DE0 at z 2.33: {10**(-2 * gtz[2.33]):.4f}); G4 0 by construction [PASS]; G5 halo gravity [PASS by definition]')
def logo(g, lr0): return g.gb + gA * np.interp(np.log(g.r / (10**lr0 * kpc)), LX, hh)
fits = [minimize_scalar(lambda x: ((np.log10(logo(g, x)) - np.log10(g.gl))**2).sum(), bounds=(-3, 4), method='bounded').x for g in GS]
grade('(c2) DIAG logotropic halo per galaxy, 1 knob r_0 each (171 knobs), fitted to the law curve', [logo(g, x) for g, x in zip(GS, fits)], f'(log10 r_0/kpc median {np.median(fits):.2f}, at bound {sum(min(x + 3, 4 - x) < 1e-3 for x in fits)})')
print(f'\nruntime {time.time() - T0:.0f} s')
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
