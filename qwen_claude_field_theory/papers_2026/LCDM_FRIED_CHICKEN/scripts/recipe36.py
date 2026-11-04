"""A35: LCDM ingredients that carry rho_DE, new constructions, and the c-barrier, per ../FROZEN_A35.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
T0 = time.time(); c_ = 2.998e8; MPC = kpc * 1e3; BASE = cos; h0 = .674; ns = .965
src = open(os.path.join(HERE, 'recipe31.py'), encoding='utf-8').read(); exec(src[src.index('OR_H2 ='):src.index('# ---------- scales')])
ZS = [0., 1., 1.5, 2.33]; ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; LMH = np.arange(11, 12.51, .25)
RDE0 = BASE.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE0); AT = .5 * AC; R10 = 10 * kpc; DC = 1.686; FCOL = .01; LAMB = .035; GAM = 1.5
P = lambda b: 'PASS' if b else 'FAIL'
U = Msun / kpc**3  # colossus density unit (Msun h^2/kpc^3) times h^2 -> SI
# ---------- environment: background at z, epoch quantities, concentration and sigma (with optional c-rescale lambda) ----------
def mkenv(C, z, lam=1., amp=False):
    """lam: c -> lam c at fixed densities and A_s. amp=False: horizon rescale M -> M/lam^3 with sigma8 x lam^((1-ns)/2) (C must carry it);
    amp=True: amplitude channel alone (C carries sigma8 x lam^2), no mass shift."""
    cc.setCurrent(C); h = C.h; ms = 1. if amp else lam**3
    e = dict(C=C, z=z, h=h, lam=lam, ms=ms, rhoc=C.rho_c(z) * h**2 * U, rde=C.rho_de(z) * h**2 * U, rm=C.rho_m(z) * h**2 * U,
             H=C.Hz(z) * 1e3 / MPC, w=float(C.wz(z)), Om=float(C.Om(z)), Ode=float(C.Ode(z)), rhoc0=C.rho_c(0) * h**2 * U,
             cg=np.asarray(CM.concentration(10**LM / ms * h, '200c', z, model='diemer19'), float))
    D = lambda zz: float(C.growthFactor(zz)); e['D'] = D(z); dz = .01; e['f'] = -(1 + z) * (np.log(D(z + dz)) - np.log(D(max(z - dz, 0.)))) / (dz + min(dz, z))
    try: zde = brentq(lambda zz: C.rho_m(zz) - C.rho_de(zz), 0., 20.)
    except ValueError: zde = np.nan
    e['zde'] = zde; e['rhocDE'] = C.rho_c(zde) * h**2 * U; e['HDE'] = C.Hz(zde) * 1e3 / MPC; e['rdeDE'] = C.rho_de(zde) * h**2 * U
    zg = np.linspace(0, 30, 601); Dg = np.array([D(x) for x in zg]); e['Dg'] = (zg, Dg)
    rm0h = C.rho_m(0)  # Msun h^2/kpc^3
    e['sig0'] = lambda M: float(C.sigma((3 * M / ms * h / (4 * np.pi * rm0h))**(1 / 3) / 1e3, 0.))  # M in Msun -> Msun/h
    cc.setCurrent(BASE); return e
def zcoll(e, M):
    s = e['sig0'](FCOL * M); zg, Dg = e['Dg']; need = DC / s
    if np.interp(e['z'], zg, Dg) <= need: return e['z']
    return float(np.interp(need, Dg[::-1], zg[::-1]))
def rhoc_at(e, zz): C = e['C']; return C.rho_c(zz) * C.h**2 * U
def cD(e, M): return 10**np.interp(np.log10(M), LM, np.log10(e['cg']))
def R200(M, rc): return (3 * M * Msun / (800 * np.pi * rc))**(1 / 3)
def conc_from_rhos(rhos, rc): return brentq(lambda c: 200 / 3 * c**3 / mu(c) - rhos / rc, 1e-3, 1e4)
def gs_from_c(M, c, rc):
    R = R200(M, rc); rs = R / c; rhos = 200 / 3 * rc * c**3 / mu(c); return 2 * np.pi * G * rhos * rs, rs / kpc
def gs_from_rhos(M, rhos, rc): return gs_from_c(M, conc_from_rhos(rhos, rc), rc)
# ---------- constructions: each returns (a [m/s^2], radius where evaluated [kpc] or None) ----------
CAL = {}
def k_gsD(e, M): return gs_from_c(M, cD(e, M), e['rhoc'])
def k_tie(e, M): return e['lam'] * .5 * c_ * np.sqrt(G * e['rde']), None
def k_T2g(e, M): return e['lam'] * c_ * np.sqrt(8 * np.pi * G * e['rde'] / 3) / (2 * np.pi), None
def k_K1(e, M): R = R200(M, e['rhocDE']); return G * M * Msun / R**2, R / kpc
def k_K2(e, M): return gs_from_rhos(M, CAL['K2'] * e['rhocDE'], e['rhoc'])
def k_K2b(e, M): return gs_from_rhos(M, CAL['K2b'] * rhoc_at(e, zcoll(e, M)), e['rhoc'])
def k_K3(e, M): R = R200(M, e['rhoc']); V = np.sqrt(G * M * Msun / R); return V * np.sqrt(G * e['rde']), None
def k_K4(e, M): return e['lam'] * c_ * e['HDE'] / 8, None
def k_K5a(e, M): r0 = (3 * M * Msun / (4 * np.pi * e['rde'] * abs(1 + 3 * e['w'])))**(1 / 3); return G * M * Msun / r0**2, r0 / kpc
def k_K5b(e, M): return 4 * np.pi * G / 3 * e['rde'] * abs(1 + 3 * e['w']) * 30 * kpc, 30.
def k_K6(e, M):
    Rm = (3 * M * Msun / (800 * np.pi * e['rm']))**(1 / 3); Rsp = Rm * .54 * (1 + .53 * e['Om']) * (1 + 1.36 * np.exp(-GAM / 3.04))
    Msp = M * .59 * (1 + .35 * e['Om']) * (1 + .92 * np.exp(-GAM / 4.54)); return G * Msp * Msun / Rsp**2, Rsp / kpc
def k_K7(e, M):
    x = e['Om'] - 1; Dv = 18 * np.pi**2 + 82 * x - 39 * x**2; R = (3 * M * Msun / (4 * np.pi * Dv * e['rhoc']))**(1 / 3); return G * M * Msun / R**2, R / kpc
def k_K8(e, M): R = R200(M, e['rhoc']); Rd = LAMB * R / np.sqrt(2); return G * M * Msun / R / Rd, Rd / kpc
def k_K8b(e, M): R = R200(M, e['rhocDE']); Rd = LAMB * R / np.sqrt(2); return G * M * Msun / R / Rd, Rd / kpc
def k_K9(e, M): return np.sqrt(k_gsD(e, M)[0] * e['lam'] * c_ * np.sqrt(8 * np.pi * G * e['rde'] / 3)), None
def k_K10a(e, M): return CAL['K10a'] * e['lam'] * c_ * e['H'] * (1 - e['f']), None
def k_K10b(e, M): return CAL['K10b'] * e['lam'] * c_ * e['H'] * e['Ode'], None
KS = {'TIE': k_tie, 'T2g': k_T2g, 'gsD': k_gsD, 'K1': k_K1, 'K2': k_K2, 'K2b': k_K2b, 'K3': k_K3, 'K4': k_K4, 'K5a': k_K5a, 'K5b': k_K5b,
      'K6': k_K6, 'K7': k_K7, 'K8': k_K8, 'K8b': k_K8b, 'K9': k_K9, 'K10a': k_K10a, 'K10b': k_K10b}
KN = {'TIE': '1 (kappa by hand)', 'T2g': 0, 'gsD': 0, 'K1': 0, 'K2': 1, 'K2b': 1, 'K3': 0, 'K4': '1 (p=1/8 chosen)', 'K5a': 0, 'K5b': 0, 'K6': '0 (+Gamma held)',
      'K7': 0, 'K8': '0 (lambda 0.035)', 'K8b': '0 (lambda 0.035)', 'K9': 0, 'K10a': 1, 'K10b': 1}
G5KIND = {'TIE': 'bg', 'T2g': 'bg', 'gsD': 'halo', 'K1': 'edge', 'K2': 'halo', 'K2b': 'halo', 'K3': 'prod', 'K4': 'bg', 'K5a': 'edge', 'K5b': 'lam30',
          'K6': 'edge', 'K7': 'edge', 'K8': 'halo', 'K8b': 'edge', 'K9': 'prod', 'K10a': 'hub', 'K10b': 'hub'}
CURVE = {'K2', 'K2b'}
# ---------- base environment and calibrations ----------
C0, s80 = mkP(BG['B0']); E0 = mkenv(C0, 0.)
print(f'A35 recipe36; c sqrt(G rho_DE0) {AC:.4e}, a_T {AT:.4e}, A0 {A0:.4e}; B0 footing P sigma8 {s80:.4f}; base c-grid vs lib max rel {np.abs(E0["cg"] / CG - 1).max():.1e}', flush=True)
M12 = 1e12; cd12 = cD(E0, M12); rhosD = 200 / 3 * E0['rhoc'] * cd12**3 / mu(cd12)
CAL['K2'] = rhosD / E0['rhocDE']; CAL['K2b'] = rhosD / rhoc_at(E0, zcoll(E0, M12))
for k, raw in (('K10a', c_ * E0['H'] * (1 - E0['f'])), ('K10b', c_ * E0['H'] * E0['Ode'])): CAL[k] = AT / raw
print(f'calibrations: Diemer19 c(1e12, 0) {cd12:.3f}, rho_s {rhosD / E0["rhoc"]:.1f} rho_crit0; K2 C = {CAL["K2"]:.1f} (x rho_crit(a_DE)); '
      f'K2b C = {CAL["K2b"]:.1f} (x rho_crit(z_c), z_c(1e12) {zcoll(E0, M12):.3f}); K10a p {CAL["K10a"]:.4f}; K10b p {CAL["K10b"]:.4f}', flush=True)
# ---------- (a) inventory ----------
print('\n(a) INVENTORY, base Lambda (where rho_DE / Lambda enters LCDM structure)', flush=True)
for z in ZS:
    e = E0 if z == 0 else mkenv(C0, z)
    print(f' z {z}: I1 D {e["D"]:.4f}, f {e["f"]:.4f} (Om^0.55 {e["Om"]**.55:.4f}), D/a {e["D"] * (1 + z):.4f}; H/H0 {e["H"] / E0["H"]:.4f}; Om {e["Om"]:.4f} Ode {e["Ode"]:.4f}; '
          f'rho_crit/rho_DE {e["rhoc"] / e["rde"]:.3f}', flush=True)
ga = E0['D']; print(f' I1 growth suppression today: D(0)/a relative to matter-era normalisation: D(z 30)(1+30) = {float(C0.growthFactor(30.)) * 31:.4f} -> Lambda suppression g(0)/g(30) = {1 / (float(C0.growthFactor(30.)) * 31):.4f}')
for lm in (11., 12., 13., 14.):
    M = 10**lm; zc = zcoll(E0, M); print(f' I2 collapse epoch M 1e{lm:.0f}: sigma0(0.01 M) {E0["sig0"](FCOL * M):.3f}, z_c {zc:.3f}, rho_crit(z_c)/rho_DE {rhoc_at(E0, zc) / E0["rde"]:.3f}'
                                        f'{"  (FLOOR: collapses now, rho_s set by rho_crit(z_obs) -> rho_DE-dominated)" if zc == 0 else ""}', flush=True)
for lm in (11., 12., 13.):
    a5, r5 = k_K5a(E0, 10**lm); print(f' I3 zero-gravity radius M 1e{lm:.0f}: r_0 {r5:.0f} kpc, R200 {R200(10**lm, E0["rhoc"]) / kpc:.0f} kpc, g(r_0) {a5 / A0:.2e} a0')
a6, r6 = k_K6(E0, M12); print(f' I4 splashback 1e12 (Gamma {GAM}): R_sp {r6:.0f} kpc, g {a6 / A0:.3e} a0; Om(z) term 1 + 0.53 Om = {1 + .53 * E0["Om"]:.4f} (EdS 1.53)')
x = E0['Om'] - 1; print(f' I5 Delta_c(Om 0.315) = {18 * np.pi**2 + 82 * x - 39 * x**2:.1f} rho_crit (EdS 177.7); Delta_m = {(18 * np.pi**2 + 82 * x - 39 * x**2) / E0["Om"]:.1f}')
for r in (1, 10, 30): print(f' I6 Lambda force c^2 Lambda r/3 at {r} kpc: {8 * np.pi * G * RDE0 / 3 * r * kpc / A0:.2e} a0')
print(f' I7 a_DE: z_DE {E0["zde"]:.4f} (a {1 / (1 + E0["zde"]):.4f}; analytic (Om/OL)^(1/3) {(.315 / .685)**(1 / 3):.4f}); rho_crit(a_DE)/rho_DE {E0["rhocDE"] / RDE0:.4f}; '
      f'H(a_DE)/H0 {E0["HDE"] / E0["H"]:.4f}; c H(a_DE)/(c sqrt(G rho_DE)) {c_ * E0["HDE"] / AC:.4f} (sqrt(16 pi/3) {np.sqrt(16 * np.pi / 3):.4f})', flush=True)
# ---------- (b) gates ----------
def g5(k, e, a, r):
    kind = G5KIND[k]
    if kind == 'halo': ok = a >= .1 * A0 and 1 <= r <= 30; return ok, f'halo/disc gravity {a / A0:.3f} a0 at r {r:.1f} kpc'
    if kind == 'edge': ok = r is not None and r <= 30 and a >= .1 * A0; return ok, f'evaluated at {r:.0f} kpc (edge/other epoch), value {a / A0:.3f} a0'
    if kind == 'lam30': return a >= .1 * A0, f'Lambda force at 30 kpc {a / A0:.2e} a0'
    if kind == 'bg': v = 8 * np.pi * G * e['rde'] / 3 * R10; return v >= .1 * A0, f'Lambda pull at 10 kpc {v / A0:.2e} a0'
    if kind == 'hub': q = .5 * e['Om'] + .5 * e['Ode'] * (1 + 3 * e['w']); v = abs(q) * e['H']**2 * R10; return v >= .1 * A0, f'|q| H^2 r at 10 kpc {v / A0:.2e} a0'
    return False, 'product: no LCDM force produces it'
print('\n(b) CONSTRUCTIONS: base-cosmology environments ...', flush=True)
EZ = {z: (E0 if z == 0 else mkenv(C0, z)) for z in ZS}
print(' G2 cosmologies (A26 C1, footing P) ...', flush=True); FS = [.5, .71, 1., 1.41, 2.]; EF = []
for f in FS:
    wm, wb, wd = .315 * h0**2, .0493 * h0**2, f * .685 * h0**2; h = np.sqrt(wm + wd)
    C, s8 = mkP(BG['B0'], 100 * h, wm / h**2, wb / h**2, R=8. * h / h0); EF.append(mkenv(C, 0.)); print(f'  f {f}: h {h:.4f} sigma8 {s8:.4f} rho_DE0/base {EF[-1]["rde"] / RDE0:.4f}', flush=True)
print(' GT backgrounds B0-B5 (footing P) ...', flush=True); EB = {}
for bn, de in BG.items():
    C, s8 = mkP(de); EB[bn] = {z: mkenv(C, z) for z in ZS}; print(f'  {bn}: sigma8 {s8:.4f}, z_DE {EB[bn][0.]["zde"]:.3f}, rho_DE(z)/rho_DE0 ' + ' '.join(f'{EB[bn][z]["rde"] / EB[bn][0.]["rde"]:.3f}' for z in ZB), flush=True)
print(' c-rescale environments (lambda 0.5, 2) ...', flush=True); EC = {}
for lam in (.5, 2.):
    Ch = mk(BG['B0'], .811 * lam**((1 - ns) / 2)); EC[('H', lam)] = mkenv(Ch, 0., lam)
    Ca = mk(BG['B0'], .811 * lam**2); EC[('A', lam)] = mkenv(Ca, 0., lam, amp=True)
EC1 = mkenv(mk(BG['B0'], .811), 0.)
print(f' setup done ({time.time() - T0:.0f} s)\n', flush=True)
RES = {}
for k, fn in KS.items():
    a0v, r0v = fn(E0, M12); ke = a0v / AC; g1 = abs(np.log10(ke / .5)) <= .05
    af = [fn(e, M12)[0] for e in EF]; s2 = float(np.polyfit(np.log([e['rde'] for e in EF]), np.log(af), 1)[0]); g2 = abs(s2 - .5) <= .05
    rz = {z: fn(EZ[z], M12)[0] / a0v for z in ZB}; g3 = all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB)
    la = np.log10([fn(E0, 10**m)[0] for m in LMH]); g4v = float(la.std()); g4 = g4v <= .1
    g5p, g5s = g5(k, E0, a0v, r0v)
    gt = {}
    for bn in BG:
        ab = {z: fn(EB[bn][z], M12)[0] for z in ZS}; rr = {z: EB[bn][z]['rde'] / EB[bn][0.]['rde'] for z in ZS}
        gt[bn] = [float(np.log10(ab[z] / ab[0.]) - .5 * np.log10(rr[z])) for z in ZB]
    gtp = all(all(abs(v) <= .05 for v in gt[b]) for b in ('B1', 'B1p', 'B1u', 'B2', 'B3', 'B4', 'B5'))
    c1 = EC1; gc = {}
    for ch in ('H', 'A'):
        lo, hi = fn(EC[(ch, .5)], M12)[0], fn(EC[(ch, 2.)], M12)[0]; gc[ch] = float(np.log(hi / lo) / np.log(4.))
    veq = a0v / (.5 * np.sqrt(G * RDE0))
    ties = all((g1, g2, g3, g4, g5p, gtp)); RES[k] = dict(ties=ties, g=(g1, g2, g3, g4, g5p, gtp), ke=ke)
    print(f'{k:5s} knobs {KN[k]}: a(1e12, z0) {a0v:.3e} = {a0v / A0:.4f} a0, kappa_eff {ke:.4f} [{P(g1)} G1]; G2 slope {s2:+.4f} [{P(g2)} G2]; '
          f'a(z)/a(0) ' + ' '.join(f'{rz[z]:.3f}' for z in ZB) + f' [{P(g3)} G3]; G4 rms {g4v:.4f} [{P(g4)} G4]; G5 {g5s} [{P(g5p)} G5]', flush=True)
    print(f'      GT dev ' + '; '.join(f'{b} ' + ' '.join(f'{v:+.3f}' for v in gt[b]) for b in BG) + f' [{P(gtp)} GT]', flush=True)
    print(f'      c-barrier: GC d ln a/d ln c = {gc["H"]:+.4f} (horizon rescale), {gc["A"]:+.4f} (amplitude channel alone) [{P(abs(gc["H"] - 1) <= .05)} GC]; '
          f'V_eq = a/(kappa sqrt(G rho_DE)) = {veq / c_:.3e} c -> {"TIES" if ties else "NO TIE"}', flush=True)
# ---------- SPARC grade for curve-altering constructions ----------
print('\nSPARC grade (curve-altering K2, K2b): NFW with the rule rho_s at each galaxy SHMR M200, (1 - f_b) dark share; C fitted to the law (1 knob)', flush=True)
MG = [m200_of(g.Ms) for g in GS]; ZCG = [zcoll(E0, M) for M in MG]
def curve(g, M, rhos):
    rc = E0['rhoc']; c = conc_from_rhos(rhos, rc); R = R200(M, rc); rs = R / c; fb = min(g.Mb / M, .5)
    m = (1 - fb) * 4 * np.pi * rhos * rs**3 * mu(g.r / rs); return g.gb + G * m / g.r**2, c
def curves(kind, lC, idx):
    out, cs = [], []
    for i in idx:
        g = GS[i]; base = E0['rhocDE'] if kind == 'K2' else rhoc_at(E0, ZCG[i]); cv, cc_ = curve(g, MG[i], 10**lC * base); out.append(cv); cs.append(cc_)
    return out, cs
def rms_law(cur, idx): return float(np.sqrt(np.mean(np.concatenate([(np.log10(cv) - np.log10(GS[i].gl))**2 for cv, i in zip(cur, idx)]))))
ALLI = list(range(len(GS))); ODD = ALLI[::2]; EVN = ALLI[1::2]
for kind in ('K2', 'K2b'):
    l0 = np.log10(CAL[kind])
    cal_cur, cal_c = curves(kind, l0, ALLI); grade(f'{kind} at the G1 calibration C = {CAL[kind]:.1f} (0 fitted knobs)', cal_cur)
    print(f' concentrations: median {np.median(cal_c):.2f}, 16-84 {np.percentile(cal_c, 16):.2f}-{np.percentile(cal_c, 84):.2f}')
    fa = minimize_scalar(lambda l: rms_law(curves(kind, l, ALLI)[0], ALLI), bounds=(l0 - 1.5, l0 + 1.5), method='bounded').x
    cur, cs = curves(kind, fa, ALLI); grade(f'{kind} C fitted on all = {10**fa:.1f} (1 knob)', cur)
    fo = minimize_scalar(lambda l: rms_law(curves(kind, l, ODD)[0], ODD), bounds=(l0 - 1.5, l0 + 1.5), method='bounded').x
    print(f' holdout: C fitted on GS[::2] {10**fo:.1f}; rms to law on unseen GS[1::2] {rms_law(curves(kind, fo, EVN)[0], EVN):.4f} dex [{P(rms_law(curves(kind, fo, EVN)[0], EVN) <= .025)} holdout]', flush=True)
# ---------- (c) c-barrier ----------
print('\n(c) C-BARRIER', flush=True)
# c1 numerical check of sigma_lambda(M) = lambda^((1-ns)/2) sigma_0(M/lambda^3) by direct integration of P_lambda(k) = lambda^(4-ns) P_0(lambda k)
cc.setCurrent(C0); kk = np.logspace(-4.5, 3.5, 6000); lk = np.log(kk)
def sig_int(Pf, Rh):
    x = kk * Rh; W = 3 * (np.sin(x) - x * np.cos(x)) / x**3; return np.sqrt(np.trapz(kk**3 * Pf * W**2, lk) / (2 * np.pi**2))
P0 = lambda k: C0.matterPowerSpectrum(np.clip(k, 1e-4, 3e3), 0.)
for lm in (10., 12., 14.):
    M = 10**lm * C0.h; Rh = (3 * M / (4 * np.pi * C0.rho_m(0)))**(1 / 3) / 1e3
    s_col = float(C0.sigma(Rh, 0.)); s_int = sig_int(P0(kk), Rh); row = f' c1 check M 1e{lm:.0f}: sigma colossus {s_col:.4f}, my integral {s_int:.4f}'
    for lam in (.5, 2.):
        s_dir = sig_int(lam**(4 - ns) * P0(lam * kk), Rh); Rs = (3 * M / lam**3 / (4 * np.pi * C0.rho_m(0)))**(1 / 3) / 1e3; s_sc = lam**((1 - ns) / 2) * float(C0.sigma(Rs, 0.))
        row += f'; lambda {lam}: direct {s_dir:.4f}, scaling formula {s_sc:.4f} (rel {s_dir / s_sc - 1:+.1e})'
    print(row, flush=True)
cc.setCurrent(BASE)
# c3 missing factor
R = R200(M12, E0['rhoc']); V = np.sqrt(G * M12 * Msun / R); cd = cd12; gsv = k_gsD(E0, M12)[0]
f1, f2, f3, f4 = V / c_, 10 * np.sqrt(8 * np.pi / 3), np.sqrt(E0['rhoc'] / RDE0), cd**2 / (2 * mu(cd))
print(f' c3 host 1e12: V200 {V / 1e3:.1f} km/s, c/V200 {c_ / V:.0f}; g200 = 10 H V200 = {10 * E0["H"] * V:.3e} (check G M/R^2 {G * M12 * Msun / R**2:.3e})')
print(f' c3 factorisation g_s/a_T = (V200/c) {f1:.3e} x 10 sqrt(8 pi/3) {f2:.3f} x sqrt(rho_crit/rho_DE) {f3:.4f} x c_conc^2/(2 mu) {f4:.3f} / kappa 0.5 = {f1 * f2 * f3 * f4 / .5:.4f} '
      f'(direct g_s/a_T {gsv / AT:.4f}); the c/V200 deficit {c_ / V:.0f} is met by {f2 * f3 * f4 / .5:.0f} = overdensity (200 -> 10 sqrt(8pi/3)), Om_DE^-1/2 and concentration, none of which carries c')
for lm in LMH:
    M = 10**lm; R = R200(M, E0['rhoc']); V = np.sqrt(G * M * Msun / R); print(f'  log M {lm:.2f}: c/V200 {c_ / V:.0f}, g_s/a_T {k_gsD(E0, M)[0] / AT:.3f}, V_eq/c {k_gsD(E0, M)[0] / (.5 * np.sqrt(G * RDE0)) / c_:.3f}')
print(' Fixed-Lambda footing (stated, not computed): rho_DE = Lambda c^2/(8 pi G), so the tie goes as c^2 and halo forms gain c only through rho_DE.')
print('\nVERDICT TABLE: ' + '; '.join(f'{k} {"TIES" if v["ties"] else "no"} (' + ''.join('1' if b else '0' for b in v['g']) + ')' for k, v in RES.items()) + '   [flags G1 G2 G3 G4 G5 GT]')
print(f'\nruntime {time.time() - T0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB')
print('Rival language; adopts nothing. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
