"""A20: (a) interacting vacuum halo scale, (b) systematic reading of the relation, per ../FROZEN_A20.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.integrate import solve_ivp
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}
ZS = [0.] + list(ZB); OB, OC, OV = cos.Ob0, cos.Om0 - cos.Ob0, cos.Ode0; CL = 400.
CGZ = {z: (CG if z == 0 else np.array([float(CM.concentration(10**m * cos.h, '200c', z, model='diemer19')) for m in LM])) for z in ZS}
def cz(M, z): return np.interp(np.log10(M), LM, CGZ[z])
CC = np.linspace(1.5, 60, 4000); YC = CC**3 * mu(1.) / mu(CC)   # rhobar_s / (200 rho_crit) as function of c
print(f'base OL {OV:.3f}; c sqrt(G rho_DE) {AC:.4e}; a0 {A0:.4e}; Ludlow C {CL:.0f} (from memory)')

# ---------------- (a) interacting vacuum ----------------
def dens(typ, xi, a):
    if typ == 'Q1':
        rc = OC * a**-(3 + xi); rv = OV + xi * OC * (1 - a**-(3 + xi)) / (3 + xi)
    else:
        rv = OV * a**xi; rc = a**-3 * (OC - xi * OV * (a**(3 + xi) - 1) / (3 + xi))
    return OB * a**-3, rc, rv
def model(typ, xi):
    """background + geodesic growth; returns E2(z) and D(z) callables (D=1 today)."""
    lna = np.linspace(np.log(1e-3), 0, 1500); a = np.exp(lna); rb, rc, rv = dens(typ, xi, a)
    if (rc[a > 1 / 11] < 0).any() or (rv[a > 1 / 11] < 0).any(): return None
    def rhs(x, y):
        aa = np.exp(x); b, c, v = dens(typ, xi, aa); E2 = b + c + v
        Qn = xi * c if typ == 'Q1' else xi * v
        dl = .5 * (-3 * b - 3 * c - Qn + Qn) / E2   # d ln H / d ln a (Q cancels between c and v)
        q = 0. if typ == 'Q1' else xi * v / c
        dc, db, u = y
        return [u + q * dc, u, -(2 + dl) * u + 1.5 * (c * dc + b * db) / E2]
    s = solve_ivp(rhs, (lna[0], 0), [1e-3, 1e-3, 1e-3], t_eval=lna, rtol=1e-7, atol=1e-12)
    dm = (rc * s.y[0] + rb * s.y[1]) / (rb + rc); D = dm / dm[-1]; z = 1 / a - 1; E2 = rb + rc + rv
    return dict(E2=lambda zz: np.interp(-zz, -z, E2), D=lambda zz: np.interp(-zz, -z, D), Dinv=lambda d: np.interp(d, D, z), rv=lambda zz: np.interp(-zz, -z, rv))
LC = model('Q1', 0.)
ZG = np.linspace(0, 40, 40001); EL2 = OB * (1 + ZG)**3 + OC * (1 + ZG)**3 + OV
def g_iv(Mv, z, m):
    cL = cz(Mv, z); rb_ = 200 * EL2[0] * np.interp(z, ZG, EL2) * cL**3 * mu(1.) / mu(cL)   # rhobar_s / rho_c0, LCDM
    zfL = np.interp(rb_ / CL, EL2, ZG)
    dlt = 1 / LC['D'](zfL) - 1 / LC['D'](z); zf = m['Dinv'](1 / (dlt + 1 / m['D'](z)))
    rbar = CL * m['E2'](zf); cI = np.interp(rbar / (200 * m['E2'](z)), YC, CC)
    rc = m['E2'](z) * RHOC; R = (3 * Mv * Msun / (800 * np.pi * rc))**(1 / 3); rs = R / cI; rhos = Mv * Msun / (4 * np.pi * rs**3 * mu(cI))
    return 2 * np.pi * G * rhos * rs, cI
M2 = np.array([m200_of(g.Ms) for g in GS]); Mm = np.median(M2)
g0, c0 = g_iv(M2, 0., LC)
print(f'\n(a) control xi=0: median g {np.median(g0) / A0:.3f} a0 (A15 0.612), kappa_eff {np.median(g0) / AC:.3f}, max |c_map/c_D19 - 1| {np.abs(c0 / cz(M2, 0) - 1).max():.1e}')
rows = []
for typ, lo, hi in (('Q1', -.5, .5), ('Q2', -1., 1.)):
    for xi in np.linspace(lo, hi, 41):
        m = model(typ, xi)
        if m is None: rows.append((typ, xi, None)); continue
        gi = g_iv(M2, 0., m)[0]; ke = np.median(gi) / AC; sp = np.log10(gi).std()
        gz = {z: float(g_iv(np.array([Mm]), z, m)[0][0] / g_iv(np.array([Mm]), 0., m)[0][0]) for z in ZB}
        fl = {z: gz[z] / np.sqrt(m['rv'](z) / m['rv'](0.)) for z in ZB}
        k1 = abs(np.log10(ke / .5)) <= .05; k2 = all(abs(np.log10(fl[z])) <= .05 for z in ZB); k3 = all(ZB[z][0] <= gz[z] <= ZB[z][1] for z in ZB); k4 = sp <= .1
        rows.append((typ, xi, dict(gi=gi, ke=ke, sp=sp, gz=gz, fl=fl, k=(k1, k2, k3, k4))))
print(f'\n(a) scan (kappa_eff today; g(z)/g(0) at median log M200 {np.log10(Mm):.2f}; flat = kappa_eff(z)/kappa_eff(0)); skipped = rho_c or rho_v < 0 below z 10')
print(' type    xi  kappa_eff  spread   g(z)/g0 z1,1.5,2.33     flat z1,1.5,2.33   K1 K2 K3 K4')
nsk = {}
for typ, xi, d in rows:
    if d is None: nsk[typ] = nsk.get(typ, 0) + 1; continue
    print(f' {typ} {xi:+.3f}  {d["ke"]:.3f}  {d["sp"]:.3f}   ' + ' '.join(f'{d["gz"][z]:.3f}' for z in ZB) + '   ' + ' '.join(f'{d["fl"][z]:.3f}' for z in ZB) + '   ' + ' '.join('P' if k else 'F' for k in d['k']))
print(' skipped:', ', '.join(f'{t} {n} of 41' for t, n in nsk.items()) or 'none')
ok = [(t, x, d) for t, x, d in rows if d is not None]
for i, nm in enumerate(('K1', 'K2', 'K3', 'K4')): print(f' {nm} passes at:', [f'{t} {x:+.3f}' for t, x, d in ok if d['k'][i]] or 'none')
allk = [f'{t} {x:+.3f}' for t, x, d in ok if all(d['k'])]; print(' K1-K4 jointly at:', allk or 'none')
def lr(gi, sel): return np.sqrt(np.mean(np.concatenate([(np.log10(law(GS[j].gb, gi[j])) - np.log10(GS[j].gl))**2 for j in sel])))
ev, od = range(0, len(GS), 2), range(1, len(GS), 2)
bt, bx, bd = min(ok, key=lambda r: lr(r[2]['gi'], range(len(GS))))
xa = [r[1] for r in ok if r[0] == bt]
e1a = grade(f'(a) law swap a = g_i(xi), best xi on all data: {bt} xi {bx:+.3f}', [law(g.gb, a) for g, a in zip(GS, bd['gi'])], f'(1 knob; at scan edge: {bx in (min(xa), max(xa))}; kappa_eff {bd["ke"]:.3f})')
ht, hx, hd = min(ok, key=lambda r: lr(r[2]['gi'], ev))
hu = lr(hd['gi'], od); print(f'(a) holdout: tuned on GS[::2] -> {ht} xi {hx:+.3f}; unseen rms to law on GS[1::2] {hu:.4f} [{"PASS" if hu <= .025 else "FAIL"}]')
for t_, x_, d_ in ok:
    if d_['k'][0]:
        m_ = model(t_, x_); print(f'(a) DIAG (post-result, not a gate) {t_} xi {x_:+.3f}: H(z)/H_LCDM at z 0.5, 1, 2.33: ' + ', '.join(f"{np.sqrt(m_['E2'](z) / LC['E2'](z)):.3f}" for z in (.5, 1., 2.33)) + f'; Omega_m(z=1) {(m_["E2"](1.) - m_["rv"](1.)) / m_["E2"](1.):.3f} vs LCDM {(LC["E2"](1.) - LC["rv"](1.)) / LC["E2"](1.):.3f}')
print('(a) verdict:', 'SUPPLIES THE TIE' if (allk and e1a <= .02 and hu <= .025) else 'NO TIE (not exact)')

# ---------------- (b) systematic reading ----------------
TB = {}
for l in open(os.path.join(D, 'SPARC_Lelli2016c.mrt')):
    p = l.split()
    if len(p) >= 17 and p[1].isdigit() and len(l) > 90:
        try: TB[p[0]] = dict(D=float(p[2]), eD=float(p[3]), i=float(p[5]), ei=float(p[6]), MHI=float(p[13]))
        except (ValueError, IndexError): pass
for g in GS:
    a = np.loadtxt(os.path.join(D, 'sparc_data', g.n + '_rotmod.dat')); a = a[a[:, 0] > 0]
    vb2 = a[:, 3] * abs(a[:, 3]) + YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5]); ok_ = vb2 > 0; a = a[ok_]
    g.vg2 = a[:, 3] * abs(a[:, 3]) * 1e6; g.vs2 = (YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5])) * 1e6; g.ev = a[:, 2] * 1e3; g.vo = a[:, 1] * 1e3
    g.t = TB[g.n]; assert np.allclose(g.vg2 + g.vs2, g.vb2)
def gbu(g, u): return np.maximum(g.vg2 + 10**u * g.vs2, 1e-3 * g.vb2) / g.r
def observer(gobs):
    lo = [np.log10(x) for x in gobs]; u = np.zeros(len(GS)); la = np.log10(A0)
    for _ in range(6):
        for j, g in enumerate(GS):
            u[j] = minimize_scalar(lambda x: (((lo[j] - np.log10(law(gbu(g, x), 10**la))) / .1)**2).sum() + (x / .1)**2, bounds=(-.3, .3), method='bounded').x
        gbs = [gbu(g, x) for g, x in zip(GS, u)]
        la = minimize_scalar(lambda x: sum(((l - np.log10(law(b, 10**x)))**2).sum() for l, b in zip(lo, gbs)), bounds=(-11, -9), method='bounded').x
    res = np.concatenate([l - np.log10(law(b, 10**la)) for l, b in zip(lo, gbs)])
    return np.sqrt((res**2).mean()), 10**la, u, res
def nfwz(r, M, c, z):
    rc = cos.rho_c(z) * cos.h**2 * Msun / kpc**3; R = (3 * M * Msun / (800 * np.pi * rc))**(1 / 3); return M * Msun * mu(r * c / R) / mu(c)
def halo(g, gb, M, c, fb, contract, z=0.):
    m0 = (1 - fb) * nfwz(g.r, M, c, z)
    if contract:
        mb = gb * g.r**2 / G; ri = g.r.copy()
        for _ in range(25):
            mi = nfwz(ri, M, c, z); ri = .5 * ri + .5 * g.r * (np.maximum(mb, 0) + (1 - fb) * mi) / mi
        m0 = np.maximum((1 - fb) * nfwz(ri, M, c, z), 1e-3 * m0)
    return gb + G * m0 / g.r**2
sS, aS, uS, rS = observer([g.gobs for g in GS])
HP = np.concatenate([g.ev / g.vo <= .05 for g in GS])
print(f'\n(b) real SPARC, observer fit (Upsilon prior 0.1 dex, global a0): RAR scatter {sS:.4f} dex, a0 {aS:.3e} ({np.log10(aS / A0):+.3f} dex vs lib A0), median |u| {np.median(abs(uS)):.3f}, u at bound {(abs(abs(uS) - .3) < 1e-3).sum()}')
print(f'    real SPARC at nominal Upsilon and lib A0: rms {np.sqrt(np.mean((np.log10(ALLO) - np.log10(ALLL))**2)):.4f} dex')
for contract in (False, True):
    tag = 'contracted' if contract else 'no contraction'
    Mn = np.array([m200_of(g.Ms) for g in GS]); cn = cz(Mn, 0)
    clean = [halo(g, g.gb, M, c, min(g.Mb / M, .5), contract) for g, M, c in zip(GS, Mn, cn)]
    grade(f'(b) noiseless mock, {tag} (nominal Upsilon, mean SHMR and c, 0 knobs tuned on the law)', clean)
    un = np.sqrt(np.mean(np.concatenate([(np.log10(clean[j]) - np.log10(GS[j].gl))**2 for j in od]))); print(f' holdout (no tuning): unseen rms to law on GS[1::2] {un:.4f} [{"PASS" if un <= .025 else "FAIL"}]')
    az = {}
    for z in ZS:
        cur = [halo(g, g.gb, M, c, min(g.Mb / M, .5), contract, z) for g, M, c in zip(GS, Mn, cz(Mn, z))]
        az[z] = fit_a(ALLB, np.concatenate(cur))
    print(f' noiseless fitted a0 {az[0.]:.3e}, kappa_eff {az[0.] / AC:.3f}; a0(z)/a0(0) ' + ', '.join(f'{z}: {az[z] / az[0.]:.3f}' for z in ZB) + f' [{"PASS" if all(ZB[z][0] <= az[z] / az[0.] <= ZB[z][1] for z in ZB) else "FAIL"} band]')
    out = []
    for s in range(5):
        rng = np.random.default_rng(100 + s); gob = []
        for g in GS:
            ut = rng.normal(0, .1); gbt = gbu(g, ut); Mst = g.Ms * 10**ut; Mbt = Mst + 1.33 * g.t['MHI'] * 1e9
            M = m200_of(Mst * 10**rng.normal(0, .15)); c = cz(M, 0) * 10**rng.normal(0, .11)
            gt = halo(g, gbt, M, c, min(Mbt / M, .5), contract); vt = np.sqrt(gt * g.r)
            fD = max(1 + rng.normal(0, g.t['eD'] / g.t['D']), .3); io = np.clip(g.t['i'] + rng.normal(0, g.t['ei']), 15, 89)
            vo = np.maximum(vt * np.sin(np.radians(g.t['i'])) / np.sin(np.radians(io)) + rng.normal(0, 1, len(g.r)) * g.ev, 1e3)
            gob.append(vo**2 / (g.r * fD))
        out.append(observer(gob))
    sc = np.array([o[0] for o in out]); am = np.array([o[1] for o in out]); la = np.log10(am.mean() / A0)
    b1 = abs(sc.mean() - sS) <= .02; b2 = abs(la) <= .05; ke = am.mean() / AC
    print(f' MOCK {tag}, 5 realisations: RAR scatter {sc.mean():.4f} +- {sc.std():.4f} (SPARC {sS:.4f}; diff {sc.mean() - sS:+.4f}) [{"PASS" if b1 else "FAIL"} B1]; fitted a0 {am.mean():.3e} +- {am.std():.1e} ({la:+.3f} dex vs A0) [{"PASS" if b2 else "FAIL"} B2]; kappa_eff {ke:.3f} [{"PASS" if abs(np.log10(ke / .5)) <= .05 else "FAIL"}]')
    hp = np.array([np.sqrt((o[3][HP]**2).mean()) for o in out])
    print(f' DIAG (post-result, not a gate): scatter on points with errV/Vobs <= 0.05 ({HP.sum()} of {len(HP)}): mock {hp.mean():.4f} +- {hp.std():.4f}, SPARC {np.sqrt((rS[HP]**2).mean()):.4f}')
    rng = np.random.default_rng(7); gob = []
    for g in GS:
        ut = rng.normal(0, .1); gbt = gbu(g, ut); Mst = g.Ms * 10**ut; Mbt = Mst + 1.33 * g.t['MHI'] * 1e9
        M = m200_of(Mst * 10**rng.normal(0, .15)); c = cz(M, 0) * 10**rng.normal(0, .11); gob.append(halo(g, gbt, M, c, min(Mbt / M, .5), contract))
    oi = observer(gob); print(f' DIAG intrinsic only (Upsilon, SHMR, c scatter; no D, i, errV errors), 1 realisation: scatter {oi[0]:.4f}, a0 {oi[1]:.3e}')
    print(f' (b) {tag} verdict:', 'REPRODUCES THE RELATION' if (b1 and b2) else 'DOES NOT REPRODUCE the law relation on these gates')
print('\nRival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
