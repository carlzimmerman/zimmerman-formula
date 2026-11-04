"""A47: measurement systematics (non-circular motions and bars, pressure support, disc thickness) on LCDM mocks and on SPARC,
per ../FROZEN_A47.md. Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, time, re, copy
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import gammainc
src = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read(); exec(src[src.index('def m200k'):src.index('def gal(')])
src = open(os.path.join(HERE, 'recipe18.py'), encoding='utf-8').read(); exec(src[src.index('K11B ='):src.index('def tune(')])
T0 = time.time()
c_ = 2.998e8; RDE = cos.Ode0 * RHOC; AC = c_ * np.sqrt(G * RDE)
ZB = {1.0: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; ZS = [0.] + list(ZB)
RHO = {'B0': (1., 1., 1.), 'B1': (1.0175, .8743, .6680), 'B1p': (.9779, .8668, .7037), 'B1u': (1.0628, .8879, .6415), 'B2': (1.1618, 1.1972, 1.2336),
       'B3': (1.3590, 1.5993, 2.0317), 'B4': (.9665, 1.0098, 1.0964), 'B5': (1., 1.0001, 1.0002)}   # recipe31.out, as recipe41
CK = os.path.join(HERE, 'recipe48.json')
OUT = json.load(open(CK)) if os.path.exists(CK) else {}
def ck(k, v): OUT[k] = v; json.dump(OUT, open(CK, 'w'), indent=1, default=float)
print(f'A47 recipe48; c sqrt(G rho_DE) {AC:.4e}, A0 {A0:.4e}', flush=True)
CGZ = {z: (CG if z == 0 else np.array([float(CM.concentration(10**m * cos.h, '200c', z, model='diemer19')) for m in LM])) for z in ZS}
def cz(M, z): return np.interp(np.log10(M), LM, CGZ[z])
# ---- table extras and bars ----
TB = {}
for l in open(os.path.join(D, 'SPARC_Lelli2016c.mrt')):
    p_ = l.split()
    if len(p_) >= 17 and p_[1].isdigit() and len(l) > 90:
        try: TB[p_[0]] = dict(D=float(p_[2]), eD=float(p_[3]), i=float(p_[5]), ei=float(p_[6]), MHI=float(p_[13]), RHI=float(p_[14]), Vf=float(p_[15]))
        except (ValueError, IndexError): pass
BF = {}
for l in open(os.path.join(D, 's4g_morph_buta2015_cvrhs.tsv')):
    if l.startswith(('#', 'Name', '-', ' ', '\t')) or not l.strip(): continue
    p_ = l.split('\t')
    try: BF[p_[0].replace(' ', '').upper()] = float(p_[4])
    except (ValueError, IndexError): pass
def norm(n):
    m = re.match(r'([A-Z]+)0*(\d+)$', n.upper()); return n.upper() if not m else m.group(1) + str(int(m.group(2)))
nmatch = 0
for g in GS:
    a = np.loadtxt(os.path.join(D, 'sparc_data', g.n + '_rotmod.dat')); a = a[a[:, 0] > 0]
    vb2 = a[:, 3] * abs(a[:, 3]) + YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5]); a = a[vb2 > 0]
    g.vg2 = a[:, 3] * abs(a[:, 3]) * 1e6; g.vd2 = YD * a[:, 4] * abs(a[:, 4]) * 1e6; g.vB2 = YB * a[:, 5] * abs(a[:, 5]) * 1e6
    g.vs2 = g.vd2 + g.vB2; g.ev = a[:, 2] * 1e3; g.vo = a[:, 1] * 1e3; g.t = TB[g.n]; assert np.allclose(g.vg2 + g.vs2, g.vb2)
    rk = g.r / kpc; Rdk = g.Rd / kpc
    vf = g.t['Vf'] if g.t['Vf'] > 0 else a[:, 1].max(); g.vf = vf
    g.dw, g.dw2 = vf < 120, 60 <= vf < 120
    f = BF.get(norm(g.n)); nmatch += f is not None; g.bar = f is not None and f >= .5
    g.wnc = np.where(rk <= 2, 1., np.exp(-(rk - 2) / 2)); Rb = 1.5 * Rdk; g.wbar = np.where(rk <= Rb, 1., np.exp(-(rk - Rb) / Rdk))
    g.wt = 1 / (1 + (rk / (2 * Rdk))**2); g.pg = rk / (g.t['RHI'] / 2) if g.t['RHI'] > 0 else np.zeros_like(rk)
print(f'dwarfs (V_flat < 120) {sum(g.dw for g in GS)}, of them 60-120 {sum(g.dw2 for g in GS)}; S4G matched {nmatch}, barred (F >= 0.5) {sum(g.bar for g in GS)}; '
      f'R_HI = 0 (pressure term off) {sum(g.t["RHI"] <= 0 for g in GS)}; galaxies {len(GS)}, points {len(ALLB)}', flush=True)
HP = np.concatenate([g.ev / g.vo <= .05 for g in GS])
def gbt(g, u, th, rg=1.):
    """true g_b: catalogue components with thickness reduction th x (5 % stars-disc, 10 % gas) x w_t."""
    return np.maximum(g.vg2 * (1 - .10 * th * g.wt) + 10**u * (g.vd2 * (1 - .05 * th * g.wt) + g.vB2), 1e-3 * g.vb2) / g.r
def observer(gobs, th=0.):
    lo = [np.log10(x) for x in gobs]; u = np.zeros(len(GS)); la = np.log10(A0)
    for _ in range(6):
        for j, g in enumerate(GS):
            u[j] = minimize_scalar(lambda x: (((lo[j] - np.log10(law(gbt(g, x, th), 10**la))) / .1)**2).sum() + (x / .1)**2, bounds=(-.3, .3), method='bounded').x
        gbs = [gbt(g, x, th) for g, x in zip(GS, u)]
        la = minimize_scalar(lambda x: sum(((l - np.log10(law(b, 10**x)))**2).sum() for l, b in zip(lo, gbs)), bounds=(-11, -9), method='bounded').x
    res = np.concatenate([l - np.log10(law(b, 10**la)) for l, b in zip(lo, gbs)])
    return float(np.sqrt((res**2).mean())), float(10**la), float(np.sqrt((res[HP]**2).mean()))
def nfwz(r, M, c, z):
    rc = cos.rho_c(z) * cos.h**2 * Msun / kpc**3; R = (3 * M * Msun / (800 * np.pi * rc))**(1 / 3); return M * Msun * mu(r * c / R) / mu(c)
def halo(g, gb, M, c, fb, z=0.): return gb + G * (1 - fb) * nfwz(g.r, M, c, z) / g.r**2
BASE = dict(nc=0., ncsd=0., dw='all', barA=0., bar='random', sig=0., th=0., rg=2.)
def S_(**k): s = dict(BASE); s.update(k); return s
def apply_obs(g, gt, S, dnc, dbar, rgf=None):
    """V_c^2 -> V_rot^2 with NC/bar factor and pressure term; returns g and clip count."""
    isdw = g.dw if S['dw'] == 'all' else g.dw2
    fac = 1 + (dnc * g.wnc if isdw else 0.) + (dbar * g.wbar if g.bar else 0.)
    pg = g.pg * 2. / S['rg']
    v2 = gt * g.r * fac**2 - (S['sig'] * 1e3)**2 * pg; ncl = int((v2 < 1e6).sum())
    return np.maximum(v2, 1e6) / g.r, ncl
def mock(S, seed, mode, z=0., r11b=False):
    rng = np.random.default_rng(seed); out, Ms_, ncl = [], [], 0
    for j, g in enumerate(GS):
        nu, x, e, q, ph = rng.normal(0, 1, 4).tolist() + [rng.uniform(0, np.pi)]
        noisy = mode != 'noiseless'; ut = .1 * nu if noisy else 0.
        gb_true = gbt(g, ut, S['th']); Mst = g.Ms * 10**ut; Mbt = Mst + 1.33 * g.t['MHI'] * 1e9
        if r11b:
            h = copy.copy(g); h.gb = gb_true; h.mb = gb_true * g.r**2 / G; gt = gal3(h, K11B, []); M = m200k(g.Ms, *K11B[:4])
        else:
            M = m200_of(Mst * 10**(.15 * x if noisy else 0.)); c = cz(M, z) * 10**(.11 * e if noisy else 0.); gt = halo(g, gb_true, M, c, min(Mbt / M, .5), z)
        Ms_.append(M)
        dnc = float(np.clip(S['nc'] + S['ncsd'] * q, -.7, .5)) if noisy else S['nc']
        dbar = -S['barA'] if S['bar'] == 'aligned' else (-S['barA'] * np.cos(2 * ph) if noisy else 0.)
        go, n_ = apply_obs(g, gt, S, dnc, dbar); ncl += n_
        dD, di = rng.normal(0, 1, 2); pn = rng.normal(0, 1, len(g.r))
        if mode == 'full':
            vt = np.sqrt(go * g.r); fD = max(1 + dD * g.t['eD'] / g.t['D'], .3); io = np.clip(g.t['i'] + di * g.t['ei'], 15, 89)
            vo = np.maximum(vt * np.sin(np.radians(g.t['i'])) / np.sin(np.radians(io)) + pn * g.ev, 1e3); go = vo**2 / (g.r * fD)
        out.append(go)
    return out, np.array(Ms_), ncl
def egates(cur, sel=None):
    sel = range(len(GS)) if sel is None else sel
    d_ = [np.log10(cur[j]) - np.log10(GS[j].gl) for j in sel]; d = np.concatenate(d_)
    gb = np.concatenate([GS[j].gb for j in sel]); per = np.array([np.sqrt((x**2).mean()) for x in d_])
    b = np.floor(np.log10(gb) * 2) / 2; bins = [(x, d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50]
    return [float(np.sqrt((d**2).mean())), float(np.percentile(per, 95)), float(max(abs(v) for _, v in bins))], [(float(x), float(v)) for x, v in bins]
def own_a(cur):
    gt = np.concatenate(cur); a = fit_a(ALLB, gt); return float(a), float(np.sqrt(np.mean((np.log10(gt) - np.log10(law(ALLB, a)))**2)))
SEEDS = (100, 101, 102); EV, OD = range(0, len(GS), 2), range(1, len(GS), 2)
def row(key, S):
    if key in OUT: return OUT[key]
    nl, _, c0 = mock(S, 0, 'noiseless'); en, bn = egates(nl); an, rn = own_a(nl)
    it, _, c1 = mock(S, SEEDS[0], 'intrinsic'); ei, _ = egates(it); ai, ri = own_a(it)
    fu = [observer(mock(S, s, 'full')[0]) for s in SEEDS]
    r = dict(En=en, bins=bn, an=an, rn=rn, ev=egates(nl, EV)[0][0], od=egates(nl, OD)[0][0], Ei=ei, ai=ai, ri=ri, clip=c0, clipi=c1,
             s_all=float(np.mean([f[0] for f in fu])), a=float(np.mean([f[1] for f in fu])), s_hp=float(np.mean([f[2] for f in fu])), s_hp_sd=float(np.std([f[2] for f in fu])))
    ck(key, r); return r
if 'sparc' not in OUT:
    s, a, h = observer([g.gobs for g in GS]); ck('sparc', dict(s=s, a=a, hp=h))
SP = OUT['sparc']; print(f'SPARC observer fit (control vs A20/A40 0.1489, 0.0814, 8.034e-11): all {SP["s"]:.4f}, good {SP["hp"]:.4f}, a0 {SP["a"]:.3e}', flush=True)
def show(tag, r):
    b1 = abs(r['s_hp'] - SP['hp']) <= .02; b2 = abs(np.log10(r['a'] / A0)) <= .05; P = lambda e: 'PASS' if e[0] <= .02 and e[1] <= .04 and e[2] <= .02 else 'FAIL'
    print(f' {tag}\n   noiseless E1 {r["En"][0]:.4f} E2 {r["En"][1]:.4f} E3 {r["En"][2]:.4f} [{P(r["En"])} E]; own a {r["an"]:.3e} ({np.log10(r["an"] / A0):+.3f} dex), rms at own a {r["rn"]:.4f}; '
          f'holdout unseen GS[1::2] {r["od"]:.4f} [{"PASS" if r["od"] <= .025 else "FAIL"}]; clipped pts {r["clip"]}\n'
          f'   intrinsic E1 {r["Ei"][0]:.4f} E2 {r["Ei"][1]:.4f} E3 {r["Ei"][2]:.4f} [{P(r["Ei"])} E]; own a {r["ai"]:.3e}, rms at own a (intrinsic scatter) {r["ri"]:.4f}\n'
          f'   observed mock (3 seeds): scatter all {r["s_all"]:.4f}, good {r["s_hp"]:.4f}+-{r["s_hp_sd"]:.4f} [{"PASS" if b1 else "FAIL"} B1]; a0 {r["a"]:.3e} ({np.log10(r["a"] / A0):+.3f} dex) [{"PASS" if b2 else "FAIL"} B2]\n'
          f'   noiseless bins ' + ' '.join(f'{x:.1f}:{v:+.3f}' for x, v in r['bins']), flush=True)
NC = dict(nc=-.10, ncsd=.15)
ROWS = [('R0 no systematic (control)', S_()),
        ('Sa1 NC dwarfs (V<120) mean -0.10 sd 0.15', S_(**NC)), ('Sa2 NC dwarfs 60-120 only', S_(dw='mid', **NC)),
        ('Sa3 bars A 0.2 random phi', S_(barA=.2)), ('Sa4 bars A 0.4 random phi', S_(barA=.4)), ('Sa5 bars aligned A 0.2', S_(barA=.2, bar='aligned')),
        ('Sa6 NC dwarfs + bars A 0.2', S_(barA=.2, **NC)),
        ('Sb1 pressure sigma 8', S_(sig=8.)), ('Sb2 pressure sigma 10', S_(sig=10.)), ('Sb3 pressure sigma 12', S_(sig=12.)), ('Sb4 pressure sigma 10, R_g = R_HI/3', S_(sig=10., rg=3.)),
        ('Sc thickness (5 % stars, 10 % gas)', S_(th=1.)),
        ('ALL Sa6 + Sb2 + Sc (literature amplitudes)', S_(barA=.2, sig=10., th=1., **NC))]
print('\n==== PART (1): systematics on LCDM mocks (plain Diemer19 + SHMR NFW, no contraction)', flush=True)
for tag, S in ROWS:
    t1 = time.time(); r = row(tag, S); show(tag, r)
print(f' runtime {time.time() - T0:.0f} s', flush=True)
print('\n R11b (K11B, 14 knobs) noiseless, diagnostic:')
for tag, S in (ROWS[0], ROWS[-1]):
    cur = mock(S, 0, 'noiseless', r11b=True)[0]; e, b = egates(cur); a_, r_ = own_a(cur)
    print(f'  R11b + {tag}: E1 {e[0]:.4f} E2 {e[1]:.4f} E3 {e[2]:.4f}; own a {a_:.3e} ({np.log10(a_ / A0):+.3f} dex), rms at own a {r_:.4f}')
print('\n==== STRENGTH SEARCH (amplitude tuned: 1 knob each, NOT literature)', flush=True)
ST = []
for s in (0, 1, 2, 3, 4, 5): ST.append((f'NC mean {-.1 * s:+.2f} sd 0.15', S_(nc=-.1 * s, ncsd=.15)))
for sg in (10., 15., 20., 25., 30.): ST.append((f'pressure sigma {sg:.0f}', S_(sig=sg)))
for th in (1., 2., 4.): ST.append((f'thickness x{th:.0f}', S_(th=th)))
for s, sg in ((3, 20.), (4, 25.), (5, 30.)): ST.append((f'NC {-.1 * s:+.2f} + sigma {sg:.0f} + thickness x2 + bars 0.2', S_(nc=-.1 * s, ncsd=.15, sig=sg, th=2., barA=.2)))
SR = []
for tag, S in ST:
    r = row('ST ' + tag, S); SR.append((tag, S, r)); show('ST ' + tag, r)
b2 = [t for t, S, r in SR if abs(np.log10(r['a'] / A0)) <= .05]; e1 = [t for t, S, r in SR if r['En'][0] <= .02]
print(f' B2 passes: {b2 or "none"}\n noiseless E1 passes: {e1 or "none"}')
bb = min(SR, key=lambda x: abs(np.log10(x[2]['a'] / A0))); print(f' closest to A0: {bb[0]} at {np.log10(bb[2]["a"] / A0):+.3f} dex')
hb = min(SR, key=lambda x: x[2]['ev']); print(f' holdout: chosen on GS[::2] -> {hb[0]} (even {hb[2]["ev"]:.4f}); unseen GS[1::2] {hb[2]["od"]:.4f} [{"PASS" if hb[2]["od"] <= .025 else "FAIL"}]', flush=True)

print('\n==== PART (2): corrections applied to real SPARC', flush=True)
MN = np.array([m200_of(g.Ms) for g in GS]); CN = cz(MN, 0)
def corr(S, alnbar=False):
    gbs, gos = [], []
    for g in GS:
        gb = gbt(g, 0., S['th']); isdw = g.dw if S['dw'] == 'all' else g.dw2
        fac = 1 + (S['nc'] * g.wnc if isdw else 0.) + (-S['barA'] * g.wbar if (g.bar and alnbar) else 0.)
        go = (g.gobs * g.r / fac**2 + (S['sig'] * 1e3)**2 * g.pg * 2. / S['rg']) / g.r; gbs.append(gb); gos.append(go)
    return gbs, gos
def dgrade(tag, S, alnbar=False):
    key = 'D ' + tag
    if key not in OUT:
        gbs, gos = corr(S, alnbar); B, O = np.concatenate(gbs), np.concatenate(gos)
        r0 = float(np.sqrt(np.mean((np.log10(O) - np.log10(law(B)))**2))); af = float(fit_a(B, O)); rf = float(np.sqrt(np.mean((np.log10(O) - np.log10(law(B, af)))**2)))
        s, a, h = observer(gos, S['th'])
        nfw = np.concatenate([halo(g, b, M, c, min(g.Mb / M, .5)) for g, b, M, c in zip(GS, gbs, MN, CN)])
        rr = []
        for g, b in zip(GS, gbs):
            hh = copy.copy(g); hh.gb = b; hh.mb = b * g.r**2 / G; rr.append(gal3(hh, K11B, []))
        rr = np.concatenate(rr)
        ck(key, dict(r0=r0, af=af, rf=rf, s=s, a=a, hp=h, nfw=float(np.sqrt(np.mean((np.log10(O) - np.log10(nfw))**2))), r11b=float(np.sqrt(np.mean((np.log10(O) - np.log10(rr))**2))),
                     mo=float(np.mean(np.log10(O) - np.log10(law(B))))))
    r = OUT[key]
    print(f' {tag}: law@A0 rms to obs {r["r0"]:.4f} (mean {r["mo"]:+.4f}); fitted a0 {r["af"]:.3e} ({np.log10(r["af"] / A0):+.3f} dex), rms {r["rf"]:.4f}; observer scatter all {r["s"]:.4f} good {r["hp"]:.4f} a0 {r["a"]:.3e} ({np.log10(r["a"] / A0):+.3f}); '
          f'LCDM rows rms to obs: mean NFW {r["nfw"]:.4f}, R11b {r["r11b"]:.4f}', flush=True)
    return r
D0 = dgrade('uncorrected SPARC', S_())
DR = [dgrade('NC dwarfs +10 % inner V', S_(nc=-.10)), dgrade('NC dwarfs 60-120 only', S_(nc=-.10, dw='mid')),
      dgrade('bars aligned 0.2 (worst case)', S_(barA=.2), True),
      dgrade('pressure sigma 8', S_(sig=8.)), dgrade('pressure sigma 10', S_(sig=10.)), dgrade('pressure sigma 12', S_(sig=12.)), dgrade('pressure sigma 10, R_g R_HI/3', S_(sig=10., rg=3.)),
      dgrade('thickness', S_(th=1.)), dgrade('ALL (NC + sigma 10 + thickness)', S_(nc=-.10, sig=10., th=1.))]
DA = DR[-1]; RA = OUT[ROWS[-1][0]]
dd = np.log10(RA['a'] / DA['a']); print(f' reconcile check: ALL-row mock observer a0 {RA["a"]:.3e} vs ALL-corrected SPARC observer a0 {DA["a"]:.3e}: {dd:+.3f} dex [{"PASS" if abs(dd) <= .05 else "FAIL"} within 0.05]')
d0 = np.log10(OUT[ROWS[0][0]]['a'] / D0['a']); print(f'   (no systematic: mock {OUT[ROWS[0][0]]["a"]:.3e} vs SPARC {D0["a"]:.3e}: {d0:+.3f} dex)')

l1 = np.log10(RA['a'] / D0['a']); l2 = np.log10(OUT[ROWS[0][0]]['a'] / DA['a'])
print(f' DIAG (post-result, not a gate; the frozen check above puts the systematic on the mock AND removes it from the data, counting it twice):')
print(f'   like-for-like 1, both observed WITH systematics: ALL-row mock a0 {RA["a"]:.3e} vs uncorrected SPARC {D0["a"]:.3e}: {l1:+.3f} dex [{"within" if abs(l1) <= .05 else "outside"} 0.05]')
print(f'   like-for-like 2, both WITHOUT systematics: R0 mock a0 {OUT[ROWS[0][0]]["a"]:.3e} vs ALL-corrected SPARC {DA["a"]:.3e}: {l2:+.3f} dex [{"within" if abs(l2) <= .05 else "outside"} 0.05]')
print(f'   good-point scatter: ALL mock {RA["s_hp"]:.4f} vs uncorrected SPARC {D0["hp"]:.4f}; R0 mock {OUT[ROWS[0][0]]["s_hp"]:.4f} vs corrected SPARC {DA["hp"]:.4f}')
print('\n==== PART (3): tie gates', flush=True)
def ties(tag, S):
    az = {z: fit_a(ALLB, np.concatenate(mock(S, 0, 'noiseless', z=z)[0])) for z in ZS}; ke = az[0.] / AC; rz = {z: az[z] / az[0.] for z in ZB}
    print(f' {tag}: fitted a {az[0.]:.3e}, kappa_eff {ke:.3f} [{"PASS" if abs(np.log10(ke / .5)) <= .05 else "FAIL"} G1]; a(z)/a(0) ' + ' '.join(f'{rz[z]:.3f}' for z in ZB)
          + f' [{"PASS" if all(ZB[z][0] <= rz[z] <= ZB[z][1] for z in ZB) else "FAIL"} G3]')
    for bg, rr in RHO.items():
        dv = [np.log10(rz[z]) - .5 * np.log10(x) for z, x in zip(ZB, rr)]
        print(f'   GT {bg:4s} (LCDM a(z), approximation): dev ' + ' '.join(f'{x:+.3f}' for x in dv) + f' [{"PASS" if max(map(abs, dv)) <= .05 else "FAIL"} GT]')
    nl, Mn, _ = mock(S, 0, 'noiseless'); ai = np.array([fit_a(g.gb, c) for g, c in zip(GS, nl)]); sel = (np.log10(Mn) >= 11) & (np.log10(Mn) <= 12.5)
    print(f'   G4 per-galaxy a over log M200 11-12.5 ({sel.sum()}): rms {np.log10(ai[sel]).std():.3f} dex [{"PASS" if np.log10(ai[sel]).std() <= .1 else "FAIL"} G4]; G2 no rho_DE in any systematic [FAIL natively]; G5 N/A (not a force)', flush=True)
ties('ALL (literature amplitudes)', ROWS[-1][1]); ties(f'strength row closest to A0: {bb[0]}', bb[1])
print('\nParameters: 11 literature amplitudes fixed (NC 0.10/0.15/120 km/s/2 kpc; bars 0.2/1.5 R_d/F 0.5; sigma 10; thickness 0.05/0.10/2 R_d), 0 tuned; '
      'A20 scatter amplitudes 3; observer 171 u + 1 a0; strength rows +1 tuned knob each.')
print(f'runtime {time.time() - T0:.0f} s\nRival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
