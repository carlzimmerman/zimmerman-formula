"""A48: is the law produced by data systematics on ordinary LCDM halos? (a) beam smearing, (b) sample selection,
(c) M/L trends, (d) gas systematics, per ../FROZEN_A48.md. Rival language, adopts nothing, not a framework result.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, time
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.optimize import minimize
T0 = time.time()
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE); AT = .5 * AC
ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; ZS = [0.] + list(ZB)
RHO = {'B0': (1., 1., 1.), 'B1': (1.0175, .8743, .6680), 'B1p': (.9779, .8668, .7037), 'B1u': (1.0628, .8879, .6415), 'B2': (1.1618, 1.1972, 1.2336),
       'B3': (1.3590, 1.5993, 2.0317), 'B4': (.9665, 1.0098, 1.0964), 'B5': (1., 1.0001, 1.0002)}
CK = os.path.join(HERE, 'recipe49.json')
OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
print(f'A48 recipe49; c sqrt(G rho_DE) {AC:.4e}, a_T {AT:.4e}, A0 {A0:.4e}', flush=True)
CGZ = {z: (CG if z == 0 else np.array([float(CM.concentration(10**m * cos.h, '200c', z, model='diemer19')) for m in LM])) for z in ZS}
def cz(M, z): return np.interp(np.log10(M), LM, CGZ[z])
TB = {}
for l in open(os.path.join(D, 'SPARC_Lelli2016c.mrt')):
    p_ = l.split()
    if len(p_) >= 17 and p_[1].isdigit() and len(l) > 90:
        try: TB[p_[0]] = dict(D=float(p_[2]), eD=float(p_[3]), i=float(p_[5]), ei=float(p_[6]), L=float(p_[7]), SBd=float(p_[12]), Rd=float(p_[11]),
                              MHI=float(p_[13]), RHI=float(p_[14]), Vf=float(p_[15]), Q=int(p_[17]))
        except (ValueError, IndexError): pass
for g in GS:
    a = np.loadtxt(os.path.join(D, 'sparc_data', g.n + '_rotmod.dat')); a = a[a[:, 0] > 0]
    vb2 = a[:, 3] * abs(a[:, 3]) + YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5]); a = a[vb2 > 0]
    g.vg2 = a[:, 3] * abs(a[:, 3]) * 1e6; g.vd2 = a[:, 4] * abs(a[:, 4]) * 1e6; g.vu2 = a[:, 5] * abs(a[:, 5]) * 1e6
    g.ev = a[:, 2] * 1e3; g.vo = a[:, 1] * 1e3; g.t = TB[g.n]
    assert np.allclose(g.vg2 + YD * g.vd2 + YB * g.vu2, g.vb2)
    Ld = 2 * np.pi * g.t['SBd'] * (g.t['Rd'] * 1e3)**2 / 1e9; g.Ld = Ld if 0 < Ld <= g.t['L'] else g.t['L']; g.fdisk = g.Ld / g.t['L']
    g.MHI = g.t['MHI'] * 1e9; g.lMs = np.log10(g.Ms); g.SBd = max(g.t['SBd'], 1.)
print(f'table: L_disk from 2 pi SBdisk Rd^2 clipped to L in {sum(1 for g in GS if g.fdisk == 1)} galaxies; RHI = 0 in {sum(1 for g in GS if g.t["RHI"] <= 0)}')
EV, OD = list(range(0, len(GS), 2)), list(range(1, len(GS), 2))

# ---------- baryons with systematics: k = dict(d, p, q, A, X, kg, fm, s) ----------
K0 = dict(d=0., p=0., q=0., A=0., X=1.33, kg=1., fm=0., s=0.)
def bary(g, k):
    lm = g.lMs - 10; fd = 10**(k['d'] + k['p'] * lm) * (g.SBd / 100.)**k['q']; fb = 10**(k['d'] + k['p'] * lm + k['A'] * np.clip(lm, 0, 1))
    Mmol = k['fm'] * g.Ms * 10**(k['s'] * lm); vm2 = g.vd2 * Mmol / (g.Ld * 1e9); gf = k['kg'] * k['X'] / 1.33
    vb2 = g.vg2 * gf + YD * fd * g.vd2 + YB * fb * g.vu2 + vm2
    gb = np.maximum(vb2, 1e-3 * g.vb2) / g.r
    Ms = g.Ms * (g.fdisk * fd + (1 - g.fdisk) * fb); Mb = Ms + 1.33 * g.MHI * gf + Mmol
    return gb, vb2, Ms, Mb
def nfwz(r, M, c, z):
    rc = cos.rho_c(z) * cos.h**2 * Msun / kpc**3; R = (3 * M * Msun / (800 * np.pi * rc))**(1 / 3); return M * Msun * mu(r * c / R) / mu(c)
def halo_m(g, gb, M, c, fb, contract, z):
    m0 = (1 - fb) * nfwz(g.r, M, c, z)
    if contract:
        mb = gb * g.r**2 / G; ri = g.r.copy()
        for _ in range(25):
            mi = nfwz(ri, M, c, z); ri = .5 * ri + .5 * g.r * (np.maximum(mb, 0) + (1 - fb) * mi) / mi
        m0 = np.maximum((1 - fb) * nfwz(ri, M, c, z), 1e-3 * m0)
    return m0
def n0(k=K0, z=0., contract=False, sel=None):
    """noiseless plain-LCDM mock (A20/A40 N0) with true baryons carrying the systematic; returns curves, true g_b, M200, halo pulls"""
    cur, gbs, Ms_, gd = [], [], [], []
    for j in (range(len(GS)) if sel is None else sel):
        g = GS[j]; gb, vb2, Ms, Mb = bary(g, k); M = m200_of(Ms); c = cz(M, z); fb = min(Mb / M, .5)
        md = halo_m(g, gb, M, c, fb, contract, z); cur.append(gb + G * md / g.r**2); gbs.append(gb); Ms_.append(M); gd.append(G * md / g.r**2)
    return cur, gbs, np.array(Ms_), gd
def egates(cur, sel=None, ref=None):
    sel = list(range(len(GS))) if sel is None else list(sel); ref = [GS[j].gl for j in sel] if ref is None else ref
    d_ = [np.log10(c) - np.log10(r) for c, r in zip(cur, ref)]; d = np.concatenate(d_)
    gb = np.concatenate([GS[j].gb for j in sel]); per = np.array([np.sqrt((x**2).mean()) for x in d_])
    b = np.floor(np.log10(gb) * 2) / 2; bins = [d[b == x].mean() for x in np.unique(b) if (b == x).sum() >= 50]
    return float(np.sqrt((d**2).mean())), float(np.percentile(per, 95)), float(max(abs(v) for v in bins)) if bins else float('nan')
def gtxt(e): return f'E1 {e[0]:.4f} E2 {e[1]:.4f} E3 {e[2]:.4f} [{"PASS" if e[0] <= .02 and e[1] <= .04 and e[2] <= .02 else "FAIL"} E]'
def gbu_k(vg2, vs2, g, u): return np.maximum(vg2 + 10**u * vs2, 1e-3 * g.vb2) / g.r
def observer(gobs, base=None):
    """A20 observer: per-galaxy log Upsilon offset u (prior 0.1, bound 0.3) + one global a0; base = list of (vg2, vs2) (default nominal)"""
    base = base or [(g.vg2, YD * g.vd2 + YB * g.vu2) for g in GS]
    lo = [np.log10(x) for x in gobs]; u = np.zeros(len(GS)); la = np.log10(A0)
    for _ in range(6):
        for j, g in enumerate(GS):
            vg, vs = base[j]
            u[j] = minimize_scalar(lambda x: (((lo[j] - np.log10(law(gbu_k(vg, vs, g, x), 10**la))) / .1)**2).sum() + (x / .1)**2, bounds=(-.3, .3), method='bounded').x
        gbs = [gbu_k(*base[j], g, x) for j, (g, x) in enumerate(zip(GS, u))]
        la = minimize_scalar(lambda x: sum(((l - np.log10(law(b, 10**x)))**2).sum() for l, b in zip(lo, gbs)), bounds=(-11, -9), method='bounded').x
    res = np.concatenate([l - np.log10(law(b, 10**la)) for l, b in zip(lo, gbs)])
    return float(np.sqrt((res**2).mean())), float(10**la), res
HP = np.concatenate([g.ev / g.vo <= .05 for g in GS])
def law_fit_data(k, obs=False, tag=''):
    """the law's own fit to observed SPARC with the systematic applied to SPARC baryons"""
    gb = np.concatenate([bary(g, k)[0] for g in GS]); a = fit_a(gb, ALLO)
    r_a = np.sqrt(np.mean((np.log10(law(gb, a)) - np.log10(ALLO))**2)); r_0 = np.sqrt(np.mean((np.log10(law(gb, A0)) - np.log10(ALLO))**2))
    s = f'  law on data{tag}: refit a0 {a:.3e} ({np.log10(a / A0):+.3f} dex), rms to observed {r_a:.4f} at refit, {r_0:.4f} at A0 (nominal 0.1951)'
    if obs:
        # observer's gas part = scaled gas + molecular (not refitted by u); star part = trended stars
        base = []
        for g in GS:
            gb_, vb2, _, _ = bary(g, k); lm = g.lMs - 10
            Mmol = k['fm'] * g.Ms * 10**(k['s'] * lm); vg = g.vg2 * k['kg'] * k['X'] / 1.33 + g.vd2 * Mmol / (g.Ld * 1e9); base.append((vg, vb2 - vg))
        so, ao, rr = observer([g.gobs for g in GS], base); s += f'; observer fit scatter all {so:.4f}, good {np.sqrt((rr[HP]**2).mean()):.4f}, a0 {ao:.3e}'
    print(s, flush=True); return a, r_a
def tie(curfn, tag, w=None):
    """tie gates on a family's best mock-observed curves; curfn(z) -> (curves, M200 array, halo pulls)"""
    az = {}
    for z in ZS:
        cur, M_, gd = curfn(z); az[z] = fit_a(ALLB, np.concatenate(cur))
        if z == 0: c0, M0_, gd0 = cur, M_, gd
    ke = az[0.] / AC; rz = {z: az[z] / az[0.] for z in ZB}
    print(f'  TIE {tag}: fitted a {az[0.]:.3e}, kappa_eff {ke:.3f} ({np.log10(ke / .5):+.3f} dex) [{"PASS" if abs(np.log10(ke / .5)) <= .05 else "FAIL"} G1]; '
          f'G2 halo route slope not native [FAIL G2, from A26/A29]; a(z)/a(0) ' + ' '.join(f'{rz[z]:.3f}' for z in ZB) + f' [{"PASS" if all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB) else "FAIL"} G3]')
    gtp = []
    for bg, rr in RHO.items():
        dv = [np.log10(rz[z]) - .5 * np.log10(x) for z, x in zip(ZB, rr)]; gtp.append(max(map(abs, dv)) <= .05)
        print(f'   GT {bg:4s} (LCDM a(z) ratio, approximation): dev ' + ' '.join(f'{x:+.3f}' for x in dv) + f' [{"PASS" if gtp[-1] else "FAIL"} GT]')
    ai = np.array([fit_a(g.gb, c) for g, c in zip(GS, c0)]); sl = (np.log10(M0_) >= 11) & (np.log10(M0_) <= 12.5); g4 = np.log10(ai[sl]).std()
    op = [np.max(x[(g.r / kpc >= 1) & (g.r / kpc <= 30)] / AT) if ((g.r / kpc >= 1) & (g.r / kpc <= 30)).any() else np.nan for g, x in zip(GS, gd0)]
    g5 = np.nanmedian(op)
    print(f'   G4 per-galaxy fitted a over log M200 11-12.5 ({sl.sum()}) rms {g4:.3f} dex [{"PASS" if g4 <= .1 else "FAIL"} G4]; '
          f'G5 median galaxy max halo pull at 1-30 kpc {g5:.2f} a_T [{"PASS" if g5 >= .1 else "FAIL"} G5]', flush=True)

# ================= control =================
c00, gb00, M00, gd00 = n0()
print('\nCONTROL: N0 noiseless plain LCDM, nominal baryons (A40 l.109: E1 0.1419 E2 0.2877 E3 0.1613, a 1.576e-10)')
grade('N0 control', c00); print(' holdout reference: N0 on GS[1::2] E1 %.4f' % egates([c00[j] for j in OD], OD)[0])
law_fit_data(K0, True, ' (nominal, control)')
SPOBS = observer([g.gobs for g in GS]); print(f' SPARC observer fit: scatter {SPOBS[0]:.4f}, good {np.sqrt((SPOBS[2][HP]**2).mean()):.4f}, a0 {SPOBS[1]:.3e} (A20 0.1489 / 0.0814 / 8.03e-11)')
SPHP = float(np.sqrt((SPOBS[2][HP]**2).mean()))

# ================= (a) beam smearing =================
print('\n================ (a) BEAM SMEARING')
def vfun_factory(g, vb2, halo=None):
    rk = g.r / kpc; R0 = np.concatenate([[0.], rk]); V0 = np.concatenate([[0.], np.sqrt(np.maximum(vb2, 0))])
    def V(R):
        R = np.maximum(R, 1e-3); vb = np.interp(R, R0, V0); out = R > rk[-1]
        vb2_ = vb**2; vb2_[out] = max(vb2[-1], 0) * rk[-1] / R[out]
        if halo is None: gb = vb2_ / (R * kpc); return np.sqrt(law(np.maximum(gb, 1e-16)) * R * kpc)
        M, c, fb, z = halo; return np.sqrt(vb2_ + G * (1 - fb) * np.maximum(nfwz(R * kpc, M, c, z), 0) / (R * kpc))
    return V
NXCAP = [1500]
def smear(g, V, theta):
    t = g.t; inc = np.radians(np.clip(t['i'], 15, 89)); si, ci = np.sin(inc), np.cos(inc); rk = g.r / kpc
    sig = theta * 4.8481e-3 * t['D'] / 2.3548; RHI = t['RHI'] if t['RHI'] > 0 else rk[-1]
    Rmax = max(rk[-1], RHI) * 1.6 + 4 * sig; dx = max(min(sig / 3, Rmax / 300), 2 * Rmax / NXCAP[0]); nx = int(2 * Rmax / dx) + 1
    x = np.linspace(-Rmax, Rmax, nx); ye = Rmax * ci + 4 * sig; ny = int(min(max(2 * ye / dx, 60), 400)); y = np.linspace(-ye, ye, ny)
    X, Y = np.meshgrid(x, y, indexing='ij'); R = np.sqrt(X**2 + (Y / ci)**2)
    S = np.where(R <= RHI, 1., np.exp(-(R - RHI) / (.2 * RHI))); S[R > Rmax] = 0
    vl = V(R.ravel()).reshape(R.shape) * si * X / np.maximum(R, 1e-9); Gy = np.exp(-y**2 / (2 * sig**2))
    Cv = (S * vl * Gy).sum(1); C = (S * Gy).sum(1)
    Gx = np.exp(-(x[None, :] - rk[:, None])**2 / (2 * sig**2))
    return (Gx @ Cv) / np.maximum(Gx @ C, 1e-300) / si
# smearing controls: (i) a 1" beam on the nearest-resolved galaxies returns the input curve; (ii) grid resolution: cap 1500 vs 4000 cells at 15"
dv1, dv2 = [], []
for g_ in GS[::10]:
    Vt = vfun_factory(g_, g_.vb2); v0 = Vt(g_.r / kpc); vs1 = smear(g_, Vt, 1.); dv1.append(np.max(np.abs(vs1 / v0 - 1)))
    a15 = smear(g_, Vt, 15.); NXCAP[0] = 4000; b15 = smear(g_, Vt, 15.); NXCAP[0] = 1500; dv2.append(np.max(np.abs(a15 / b15 - 1)))
print(f' control: 1" beam, 18 galaxies, median max |V_s/V - 1| {np.median(dv1):.4f} (max {np.max(dv1):.4f}); grid 1500 vs 4000 at 15": max |dV/V| {np.max(dv2):.4f}')
THS, FBS = (15., 22.5, 30.), (.25, .5, 1.)
def smear_cells(z=0., only=None):
    """returns dict theta -> (V_smeared N0 list, V_true N0 list, V_s law list, V_true law list)"""
    out = {}
    for th in (THS if only is None else [only]):
        vsN, vtN, vsL, vtL = [], [], [], []
        for g in GS:
            gb, vb2, Ms, Mb = bary(g, K0); M = m200_of(Ms); c = cz(M, z); fb = min(Mb / M, .5)
            VN = vfun_factory(g, vb2, (M, c, fb, z)); VL = vfun_factory(g, g.vb2)
            vsN.append(smear(g, VN, th)); vtN.append(VN(g.r / kpc)); vsL.append(smear(g, VL, th)); vtL.append(VL(g.r / kpc))
        out[th] = (vsN, vtN, vsL, vtL)
    return out
t1 = time.time(); SM = smear_cells(); print(f' smearing of N0 and the law for 3 beams: {time.time() - t1:.1f} s', flush=True)
vt_chk = np.max([np.max(np.abs(np.log10(v**2 / g.r) - np.log10(c))) for v, g, c in zip(SM[15.][1], GS, c00)])
print(f' check: unsmeared N0 V(R) from the interpolator reproduces N0 curves to {vt_chk:.2e} dex')
def obsg(vs, vt, f, g): return (vt + f * (vs - vt))**2 / g.r
cells = {}
for th in THS:
    vsN, vtN, vsL, vtL = SM[th]
    fr = np.concatenate([np.abs(vs / vt - 1) for vs, vt in zip(vsL, vtL)])
    print(f'\n theta {th:.1f}": full first-moment smearing changes the law curve by >5 % at {np.mean(fr > .05):.3f} of points, >10 % at {np.mean(fr > .1):.3f}')
    for f in FBS:
        cN = [obsg(vs, vt, f, g) for vs, vt, g in zip(vsN, vtN, GS)]; cL = [obsg(vs, vt, f, g) for vs, vt, g in zip(vsL, vtL, GS)]
        e = egates(cN); eev = egates([cN[j] for j in EV], EV)[0]; eod = egates([cN[j] for j in OD], OD)[0]; cells[(th, f)] = (e, eev, eod, cN, cL)
        lL = np.concatenate(cL)
        rL = np.sqrt(np.mean((np.log10(lL) - np.log10(ALLO))**2)); dL = egates(cL)[0]; dNL = egates(cN, ref=cL)[0]
        print(f'  f_bs {f:.2f}: smeared N0 vs law {gtxt(e)}; a fit {fit_a(ALLB, np.concatenate(cN)):.3e} | smeared law vs law rms {dL:.4f}; smeared N0 vs smeared law {dNL:.4f}; '
              f'smeared law rms to observed {rL:.4f} (unsmeared 0.1951)', flush=True)
best_a = min(cells, key=lambda k: cells[k][0][0]); hb_a = min(cells, key=lambda k: cells[k][1])
print(f'\n (a) best cell (all) theta {best_a[0]} f {best_a[1]}: {gtxt(cells[best_a][0])}')
print(f' (a) holdout: chosen on GS[::2] -> theta {hb_a[0]} f {hb_a[1]} (even {cells[hb_a][1]:.4f}); unseen GS[1::2] {cells[hb_a][2]:.4f} [{"PASS" if cells[hb_a][2] <= .025 else "FAIL"}]')
grade(f'(a) smeared N0, theta {best_a[0]} f_bs {best_a[1]}', cells[best_a][3])
# the law's own fit with smearing modelled: refit a0 by forward-smearing the law at each trial a (theta 30, f 1: the largest)
def law_smeared_rms(a, th, f):
    out = []
    for g in GS:
        def V(R, g=g):
            rk = g.r / kpc; R = np.maximum(R, 1e-6); vb = np.interp(R, np.concatenate([[0.], rk]), np.concatenate([[0.], np.sqrt(g.vb2)])); o = R > rk[-1]
            v2 = vb**2; v2[o] = g.vb2[-1] * rk[-1] / R[o]; return np.sqrt(law(np.maximum(v2 / (R * kpc), 1e-16), a) * R * kpc)
        vt = V(g.r / kpc); out.append(obsg(smear(g, V, th), vt, f, g))
    return float(np.sqrt(np.mean((np.log10(np.concatenate(out)) - np.log10(ALLO))**2)))
for th, f in ((30., 1.), (15., .25)):
    key = f'lawsm_{th}_{f}'
    if key not in OUT:
        r = minimize_scalar(lambda x: law_smeared_rms(10**x, th, f), bounds=(np.log10(A0) - .3, np.log10(A0) + .3), method='bounded', options=dict(xatol=2e-3))
        ck(key, [float(10**r.x), float(r.fun), law_smeared_rms(A0, th, f)])
    a_, r_, r0_ = OUT[key]
    print(f'  law on data with smearing theta {th} f {f} forward-modelled: refit a0 {a_:.3e} ({np.log10(a_ / A0):+.3f} dex), rms to observed {r_:.4f} at refit, {r0_:.4f} at A0 (unsmeared 0.1951)', flush=True)
th_b, f_b = best_a
def curfn_a(z):
    sm = smear_cells(z, th_b)[th_b]; cur = [obsg(vs, vt, f_b, g) for vs, vt, g in zip(sm[0], sm[1], GS)]
    _, _, M_, gd = n0(K0, z); return cur, M_, gd
tie(curfn_a, f'(a) theta {th_b} f_bs {f_b}')
print(f' (a) parameters: 2 grid knobs (theta_b, f_bs). runtime {time.time() - T0:.0f} s', flush=True)

# ================= (b) selection =================
print('\n================ (b) SAMPLE SELECTION\n b1 observable subsets of the real sample (N0 against the law on the subset; the law refit on the subset)')
rr = np.array([g.t['RHI'] / g.t['Rd'] if g.t['RHI'] > 0 else np.nan for g in GS]); rmed = np.nanmedian(rr)
SUB = {'all': [True] * len(GS), 'Q=1': [g.t['Q'] == 1 for g in GS], 'Q<=2': [g.t['Q'] <= 2 for g in GS], 'Inc>=30': [g.t['i'] >= 30 for g in GS],
       'Q<=2 & Inc>=30': [g.t['Q'] <= 2 and g.t['i'] >= 30 for g in GS], 'HI-rich MHI/M*>=1': [g.MHI >= g.Ms for g in GS],
       f'extended RHI/Rd>={rmed:.2f}': [x >= rmed for x in rr], 'Vflat>0': [g.t['Vf'] > 0 for g in GS]}
for nm, m in SUB.items():
    sel = [j for j in range(len(GS)) if m[j]]; e = egates([c00[j] for j in sel], sel)
    gbS = np.concatenate([GS[j].gb for j in sel]); goS = np.concatenate([GS[j].gobs for j in sel]); aN = fit_a(gbS, np.concatenate([c00[j] for j in sel])); aD = fit_a(gbS, goS)
    rD = np.sqrt(np.mean((np.log10(law(gbS, A0)) - np.log10(goS))**2))
    print(f'  {nm:24s} {len(sel):3d} gal: N0 {gtxt(e)}; N0 a {aN:.3e} ({np.log10(aN / A0):+.3f}); data law refit a0 {aD:.3e} ({np.log10(aD / A0):+.3f}), law rms to observed {rD:.4f}', flush=True)
print('\n b2 halo-dependent selection at fixed SPARC baryons, K = 40 realisations per galaxy (Upsilon 0.1, SHMR 0.15, c 0.11 dex)')
KR = 40; rng = np.random.default_rng(4900)
def flat(v): v = v[-3:]; return v.max() / v.min() - 1 <= .05
cls_obs = np.array([flat(g.vo) for g in GS]); vfl = np.array([g.t['Vf'] > 0 for g in GS])
print(f'  SF1 rule on real curves: flat {cls_obs.sum()} of {len(GS)}; agreement with table Vflat>0: {np.mean(cls_obs == vfl):.3f}')
DR = rng.normal(0, 1, (len(GS), KR, 3))
def realise(z=0.):
    R = []
    for j, g in enumerate(GS):
        rows = []
        for k_ in range(KR):
            nu, x, e = DR[j, k_]; u = .1 * nu; gbt = np.maximum(g.vg2 + 10**u * (YD * g.vd2 + YB * g.vu2), 1e-3 * g.vb2) / g.r
            Mst = g.Ms * 10**u; Mbt = Mst + 1.33 * g.MHI; M = m200_of(Mst * 10**(.15 * x)); dc = .11 * e; c = cz(M, z) * 10**dc
            md = halo_m(g, gbt, M, c, min(Mbt / M, .5), False, z); gt = gbt + G * md / g.r**2
            r22 = 2.2 * g.Rd; mh22 = (1 - min(Mbt / M, .5)) * nfwz(np.array([r22]), M, c, z)[0]
            rows.append(dict(gt=gt, Mres=np.log10(M) - np.log10(m200_of(Mst)), dc=dc, lh=np.log10(G * mh22 / r22**2), Mst=Mst, M=M, gd=G * md / g.r**2))
        R.append(rows)
    return R
t1 = time.time(); RL = realise(); print(f'  realisations built {time.time() - t1:.1f} s', flush=True)
SF1 = np.array([[flat(np.sqrt(r['gt'] * g.r)) == cls_obs[j] for r in RL[j]] for j, g in enumerate(GS)])
SF2 = np.array([[np.sqrt(r['gt'] * g.r).max() / np.sqrt(G * r['Mst'] * Msun / g.Rd) >= 1.1 for r in RL[j]] for j, g in enumerate(GS)])
LH = np.array([[r['lh'] for r in RL[j]] for j in range(len(GS))]); ZH = (LH - LH.mean(1, keepdims=True)) / LH.std(1, keepdims=True)
MR = np.array([[r['Mres'] for r in RL[j]] for j in range(len(GS))]); DC = np.array([[r['dc'] for r in RL[j]] for j in range(len(GS))])
print(f'  SF1 keeps {SF1.mean():.3f} of realisations; SF2 keeps {SF2.mean():.3f}; both {(SF1 & SF2).mean():.3f}')
def weights(beta, s1, s2):
    w = np.exp(beta * ZH)
    if s1: w = w * SF1
    if s2: w = w * SF2
    return w
def wgates(w, sel):
    num, den, per, bins_n, bins_d, gbl = 0., 0, [], {}, {}, []
    used = [j for j in sel if w[j].sum() > 0]
    for j in used:
        ww = w[j] / w[j].sum(); g = GS[j]; d2 = np.zeros(len(g.r)); dm = np.zeros(len(g.r))
        for k_ in range(KR):
            if ww[k_] == 0: continue
            d = np.log10(RL[j][k_]['gt']) - np.log10(g.gl); d2 += ww[k_] * d**2; dm += ww[k_] * d
        num += d2.sum(); den += len(g.r); per.append(np.sqrt(d2.mean()))
        b = np.floor(np.log10(g.gb) * 2) / 2
        for x_, v_ in zip(b, dm): bins_n[x_] = bins_n.get(x_, 0) + v_; bins_d[x_] = bins_d.get(x_, 0) + 1
    bn = [bins_n[x_] / bins_d[x_] for x_ in bins_n if bins_d[x_] >= 50]
    return (float(np.sqrt(num / den)), float(np.percentile(per, 95)), float(max(abs(v) for v in bn))), len(sel) - len(used)
def wshift(w):
    ok = w.sum(1) > 0; wn = w[ok] / w[ok].sum(1, keepdims=True)
    return float((wn * MR[ok]).sum(1).mean() - MR[ok].mean()), float((wn * DC[ok]).sum(1).mean() - DC[ok].mean())
def wobs(w, seed):
    """one weighted-drawn realisation per galaxy, A20 observation errors, observer fit; dropped galaxies keep their nominal-draw curve? no: they are excluded by giving the SPARC curve"""
    rg = np.random.default_rng(seed); cur = []
    for j, g in enumerate(GS):
        if w[j].sum() > 0: k_ = rg.choice(KR, p=w[j] / w[j].sum())
        else: k_ = rg.integers(KR)
        vt = np.sqrt(RL[j][k_]['gt'] * g.r); fD = max(1 + rg.normal(0, g.t['eD'] / g.t['D']), .3); io = np.clip(g.t['i'] + rg.normal(0, g.t['ei']), 15, 89)
        vo = np.maximum(vt * np.sin(np.radians(g.t['i'])) / np.sin(np.radians(io)) + rg.normal(0, 1, len(g.r)) * g.ev, 1e3); cur.append(vo**2 / (g.r * fD))
    s, a, r = observer(cur); return float(np.sqrt((r[HP]**2).mean())), a
BETAS = (0., -.5, -1., -2., -3., -5.); res_b = {}
for s1, s2 in ((0, 0), (1, 0), (0, 1), (1, 1)):
    for be in BETAS:
        key = f'b2_{s1}{s2}_{be}'
        w = weights(be, s1, s2); e, ndrop = wgates(w, range(len(GS))); eev = wgates(w, EV)[0][0]; eod = wgates(w, OD)[0][0]; sh = wshift(w)
        if key not in OUT:
            ob = [wobs(w, 4910 + i) for i in range(3)]; ck(key, ob)
        ob = OUT[key]; shp = np.mean([o[0] for o in ob]); aob = np.mean([o[1] for o in ob])
        real = -.3 <= sh[0] <= 1e-9 and -.11 <= sh[1] <= 1e-9 or (abs(sh[0]) < .02 and abs(sh[1]) < .02)
        res_b[(s1, s2, be)] = (e, eev, eod, sh, real)
        print(f'  SF1 {s1} SF2 {s2} beta {be:+.1f}: {gtxt(e)} (dropped {ndrop}); shift log M200 {sh[0]:+.3f}, log c {sh[1]:+.3f} [{"REALISTIC" if real else "NOT REALISTIC"}]; '
              f'obs good-pt scatter {shp:.4f} [{"PASS" if abs(shp - SPHP) <= .02 else "FAIL"} B1], a0 {aob:.3e} ({np.log10(aob / A0):+.3f}) [{"PASS" if abs(np.log10(aob / A0)) <= .05 else "FAIL"} B2]', flush=True)
bb = min(res_b, key=lambda k: res_b[k][0][0]); bbr = min([k for k in res_b if res_b[k][4]], key=lambda k: res_b[k][0][0]); hb = min(res_b, key=lambda k: res_b[k][1])
print(f'\n (b2) best overall: SF1 {bb[0]} SF2 {bb[1]} beta {bb[2]}: {gtxt(res_b[bb][0])} [{"REALISTIC" if res_b[bb][4] else "NOT REALISTIC"}]')
print(f' (b2) best realistic: SF1 {bbr[0]} SF2 {bbr[1]} beta {bbr[2]}: {gtxt(res_b[bbr][0])}')
print(f' (b2) holdout: chosen on GS[::2] -> SF1 {hb[0]} SF2 {hb[1]} beta {hb[2]} (even {res_b[hb][1]:.4f}); unseen {res_b[hb][2]:.4f} [{"PASS" if res_b[hb][2] <= .025 else "FAIL"}]')
# strength diagnostic: beta further, to see if any strength reaches E1 0.02
for be in (-8., -12., -20.):
    w = weights(be, 1, 0); e, nd = wgates(w, range(len(GS))); sh = wshift(w)
    print(f'  diagnostic SF1 beta {be:+.0f}: {gtxt(e)}; shift log M200 {sh[0]:+.3f}, log c {sh[1]:+.3f} (not realistic if outside [-0.3,0], [-0.11,0])')
wb = weights(bbr[2], bbr[0], bbr[1])
def curfn_b(z):
    Rz = RL if z == 0 else realise(z); cur, Ms_, gd = [], [], []
    for j, g in enumerate(GS):
        ww = wb[j] / wb[j].sum() if wb[j].sum() > 0 else np.ones(KR) / KR
        cur.append(10**sum(ww[k_] * np.log10(Rz[j][k_]['gt']) for k_ in range(KR))); Ms_.append(10**sum(ww[k_] * np.log10(Rz[j][k_]['M']) for k_ in range(KR)))
        gd.append(sum(ww[k_] * Rz[j][k_]['gd'] for k_ in range(KR)))
    return cur, np.array(Ms_), gd
print(' tie gates on the best realistic selection (per galaxy, weighted geometric-mean curve)')
tie(curfn_b, f'(b2) SF1 {bbr[0]} SF2 {bbr[1]} beta {bbr[2]}')
print(f' (b) parameters: beta + 2 switches; thresholds fixed; 3 literature scatter amplitudes. runtime {time.time() - T0:.0f} s', flush=True)

# ================= (c), (d), combined =================
BOX_C = dict(d=(-.097, .041), p=(-.05, .10), q=(-.05, .05), A=(0., .25))
BOX_D = dict(X=(1.33, 1.40), kg=(.9, 1.1), fm=(0., .15), s=(-.5, 0.))
WIDE_C = dict(d=(-.5, .5), p=(-.5, .5), q=(-.5, .5), A=(-.5, .5)); WIDE_D = dict(X=(1.33, 1.40), kg=(.3, 3.), fm=(0., 1.), s=(-.5, 0.))
def kd(names, x): k = dict(K0); k.update(dict(zip(names, x))); return k
def e1_alpha(k, sel=None): cur = n0(k, sel=sel)[0]; return egates(cur, sel)
def e1_beta(k):
    cur, gbs, _, _ = n0(k); return egates(cur, ref=[law(b) for b in gbs])
def search(box, sel=None, tag=''):
    nm = list(box); lo = np.array([box[n][0] for n in nm]); hi = np.array([box[n][1] for n in nm]); best = None
    for s in range(4):
        x0 = (lo + hi) / 2 if s == 0 else np.random.default_rng(49 + s).uniform(lo, hi)
        r = minimize(lambda x: e1_alpha(kd(nm, x), sel)[0], x0, method='L-BFGS-B', bounds=list(zip(lo, hi)), options=dict(maxiter=60, eps=1e-3))
        if best is None or r.fun < best.fun: best = r
    atb = [n for n, v, a, b in zip(nm, best.x, lo, hi) if min(v - a, b - v) < 1e-3 * (b - a)]
    print(f'  search {tag}: E1 {best.fun:.4f} at ' + ', '.join(f'{n} {v:+.3f}' for n, v in zip(nm, best.x)) + f'; at bound {atb}', flush=True)
    return kd(nm, best.x)
def family(tag, box, wide):
    print(f'\n================ {tag}')
    nm = list(box); import itertools
    cor = []
    for xs in itertools.product(*[box[n] for n in nm]):
        k = kd(nm, xs); e = e1_alpha(k); a = fit_a(ALLB, np.concatenate(n0(k)[0])); ad = fit_a(np.concatenate([bary(g, k)[0] for g in GS]), ALLO); cor.append((xs, e, a, ad))
    print(f'  {len(cor)} corners, reading alpha: E1 {min(c[1][0] for c in cor):.4f} to {max(c[1][0] for c in cor):.4f}; mock a {min(c[2] for c in cor):.3e} to {max(c[2] for c in cor):.3e}; '
          f'law refit a0 on data {min(c[3] for c in cor):.3e} ({np.log10(min(c[3] for c in cor) / A0):+.3f}) to {max(c[3] for c in cor):.3e} ({np.log10(max(c[3] for c in cor) / A0):+.3f})')
    kb = search(box, None, 'all galaxies, allowed box'); ke = search(box, EV, 'GS[::2], allowed box')
    ea = e1_alpha(kb); eb = e1_beta(kb); un = e1_alpha(ke, OD)[0]
    print(f'  best allowed (all): alpha {gtxt(ea)}; beta {gtxt(eb)}')
    print(f'  holdout: unseen GS[1::2] alpha E1 {un:.4f} [{"PASS" if un <= .025 else "FAIL"}]')
    grade(f'{tag} best allowed, reading alpha', n0(kb)[0])
    law_fit_data(kb, True, ' at best allowed knobs')
    lo_ = min(cor, key=lambda c: c[3]); hi_ = max(cor, key=lambda c: c[3])
    law_fit_data(kd(nm, lo_[0]), True, ' at the corner with lowest a0'); law_fit_data(kd(nm, hi_[0]), True, ' at the corner with highest a0')
    ec = egates(n0(kb, contract=True)[0]); print(f'  N0c (contracted) at best allowed: alpha {gtxt(ec)}')
    kw = search(wide, None, 'all galaxies, WIDENED diagnostic'); print(f'  widened: alpha {gtxt(e1_alpha(kw))}')
    return kb, ke
kc, kce = family('(c) M/L TREND (d, p, q, A_imf)', BOX_C, WIDE_C)
tie(lambda z: (lambda r: (r[0], r[2], r[3]))(n0(kc, z)), '(c) best allowed')
kdd, kde = family('(d) GAS (X, k_g, f_mol, s)', BOX_D, WIDE_D)
tie(lambda z: (lambda r: (r[0], r[2], r[3]))(n0(kdd, z)), '(d) best allowed')
print('\n================ COMBINED (c) + (d), 8 knobs in their boxes')
BOX_CD = dict(BOX_C); BOX_CD.update(BOX_D)
kcd = search(BOX_CD, None, 'all, combined box'); kcde = search(BOX_CD, EV, 'GS[::2], combined box')
print(f'  combined best: alpha {gtxt(e1_alpha(kcd))}; beta {gtxt(e1_beta(kcd))}; holdout unseen {e1_alpha(kcde, OD)[0]:.4f} [{"PASS" if e1_alpha(kcde, OD)[0] <= .025 else "FAIL"}]')
law_fit_data(kcd, True, ' at combined best')
# add the best beam cell on top (smearing of the combined truth; theta and f from (a) on GS[::2])
th_h, f_h = hb_a; cur = []
for g in GS:
    gb, vb2, Ms, Mb = bary(g, kcd); M = m200_of(Ms); c = cz(M, 0.); fb = min(Mb / M, .5); V = vfun_factory(g, vb2, (M, c, fb, 0.)); vt = V(g.r / kpc)
    cur.append(obsg(smear(g, V, th_h), vt, f_h, g))
e = egates(cur); print(f'  combined + beam theta {th_h} f {f_h}: alpha {gtxt(e)}; unseen GS[1::2] {egates([cur[j] for j in OD], OD)[0]:.4f}')
tie(lambda z: (lambda r: (r[0], r[2], r[3]))(n0(kcd, z)), 'combined (c)+(d) best allowed (no beam)')
print(f'\nparameters: (a) 2; (b) beta + 2 switches; (c) 4; (d) 4 (3 effective); combined 8 (+2 beam). runtime {time.time() - T0:.0f} s')
print('Rival language; adopts nothing. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
