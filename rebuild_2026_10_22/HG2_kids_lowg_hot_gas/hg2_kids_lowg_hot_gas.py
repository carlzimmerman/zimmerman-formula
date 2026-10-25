"""HG2_kids_lowg_hot_gas -- frozen criteria in FROZEN_CRITERIA.md (2546ffbd10). Model-free: no a0 in the graded statistic.

Do KT2017 groups with an eRASS1 hot atmosphere sit further above the KiDS isolated blue-lens RAR than groups without one,
at matched sigma, after their hot gas is counted?  HG1's group builder is imported read-only.  MUTATE=1 runs the controls.
"""
import json, os, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / 'rebuild_2026_10_22' / 'HG1_hot_gas_selector'))
import hg1_hot_gas_selector as hg1                          # chdirs to the repo; builder, D statistic, classes, power

MUTATE = os.environ.get('MUTATE') == '1'
TAG = '_MUTATE' if MUTATE else ''
SEED = 20261025
B21 = REPO / 'real_research' / 'data' / 'lensing_rar' / 'brouwer2021_rar'
G_pc, PCm = 4.52e-30, 3.086e16
out_lines = []


def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out_lines.append(s)


# ---------- KiDS reference (CFG829's loader, unchanged) ----------
def load(esd, cov, binmin=None):
    d = np.loadtxt(B21/esd); gb, esdt, bias = d[:, 0], d[:, 1], d[:, 4]
    go = 4*G_pc*esdt/bias*PCm
    c = np.loadtxt(B21/cov); n = len(gb); C = np.zeros((n, n))
    sel = c if binmin is None else c[(np.isclose(c[:, 0], binmin)) & (np.isclose(c[:, 1], binmin))]
    def idx(x):
        k = int(np.argmin(np.abs(gb/x - 1))); return k if abs(gb[k]/x - 1) < 1e-3 else None
    for row in sel:
        i, j = idx(row[2]), idx(row[3])
        if i is not None and j is not None: C[i, j] = row[4]/row[6]
    C *= (4*G_pc*PCm)**2
    return gb, go, C

BLUE = ('Fig-8_RAR-KiDS-isolated_Colorbin_1.txt', 'Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt', 0.0)
ALL = ('Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt', 'Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt', None)


def k1_amp(gb, go, C):
    a0 = 9.3603e-11; gl = gb/(-np.expm1(-np.sqrt(gb/a0)))
    m = (gb >= 10**-13.3) & (gb < 10**-11.9)
    Ci = np.linalg.inv(C[np.ix_(m, m)]); a = gl[m] @ Ci @ gl[m]
    return float(gl[m] @ Ci @ go[m]/a), float(a**-0.5)


class Ref:
    """log-linear interpolation of log g_obs between adjacent reference points; no extrapolation."""
    def __init__(self, gb, go, C, shift=0.0):
        self.lx = np.log10(gb) + shift; self.go = go; self.C = C

    def weights(self, gbar):
        x = np.log10(gbar); k = np.searchsorted(self.lx, x) - 1
        ok = (x >= self.lx[0]) & (x <= self.lx[-1])
        k = np.clip(k, 0, len(self.lx) - 2)
        w = (x - self.lx[k])/(self.lx[k + 1] - self.lx[k])
        return k, w, ok

    def logref(self, gbar, go=None):
        go = self.go if go is None else go
        k, w, ok = self.weights(gbar); ly = np.log10(go)
        return np.where(ok, (1 - w)*ly[k] + w*ly[k + 1], np.nan)

    def draw(self, rng):
        g = rng.multivariate_normal(self.go, self.C)
        bad = g <= 0
        return np.where(bad, 0.01*self.go, g), int(bad.sum())


def deltas(rows, ref, go=None):
    gbar = np.array([r['gbar'] for r in rows]); gobs = np.array([r['gobs'] for r in rows])
    return np.log10(gobs) - ref.logref(gbar, go)


def bootstrap(rows, ref, rng, n=2000):
    idx_b = [i for i, r in enumerate(rows) if r['flag'] == 'BRIGHT']
    idx_f = [i for i, r in enumerate(rows) if r['flag'] == 'FAINT']
    out, nbad = [], 0
    for _ in range(n):
        g, b = ref.draw(rng); nbad += b
        dl = deltas(rows, ref, g)
        pick = list(rng.choice(idx_b, len(idx_b))) + list(rng.choice(idx_f, len(idx_f)))
        out.append(hg1.D_stat([rows[i] for i in pick], dl[pick])[0])
    out = np.array(out); out = out[np.isfinite(out)]
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), nbad


def main():
    rng = np.random.default_rng(SEED)
    say(f'HG2_kids_lowg_hot_gas{TAG}  (frozen 2546ffbd10; model-free, footing-independent; a0 only in K1)')
    gb, go, C = load(*BLUE)
    A, sA = k1_amp(gb, go, C)
    say(f'K1 CFG829 blue-lens A = {A:.4f} +- {sA:.4f} (target 1.016 +- 0.086, tol 0.001)')
    assert abs(A - 1.016) <= 1e-3 and abs(sA - 0.086) <= 1e-3, 'K1 FAIL'
    l, b = hg1.galactic(192.85948, 27.12825); assert abs(b - 90) < 0.01, 'K2 NGP FAIL'
    l, b = hg1.galactic(266.405, -28.936); assert min(l, 360 - l) < 0.1 and abs(b) < 0.1, 'K2 GC FAIL'
    say(f'K2 galactic transform OK (GC -> l {l:.3f}, b {b:.3f})')
    groups, mem = hg1.load_groups(); erass = hg1.load_erass()
    rows, drops = hg1.build(groups, mem, erass)
    rows2, _ = hg1.build(groups, mem, erass, dscale=1.1, match_scale=1.1)
    assert [r['flag'] for r in rows] == [r['flag'] for r in rows2], 'K3 flag mismatch'
    k3 = max(abs(a['gbar']/b_['gbar'] - 1) for a, b_ in zip(rows, rows2))
    say(f'K3 g_bar distance invariance: max rel diff {k3:.2e}'); assert k3 < 1e-6, 'K3 FAIL'
    nB = sum(r['flag'] == 'BRIGHT' for r in rows)
    say(f'K4 builder: {len(rows)} groups, BRIGHT {nB}, FAINT {len(rows) - nB} (target 190 / 14 / 176)')
    assert (len(rows), nB) == (190, 14), 'K4 FAIL'
    ref = Ref(gb, go, C)
    k5 = np.max(np.abs(10**ref.logref(gb[1:-1])/go[1:-1] - 1))
    say(f'K5 interpolation at the reference points: max rel diff {k5:.1e}'); assert k5 < 1e-9, 'K5 FAIL'
    say(f'reference: {len(gb)} blue-lens points, g_bar 10^{np.log10(gb[0]):.2f} .. 10^{np.log10(gb[-1]):.2f}')
    base = deltas(rows, ref)
    sup = [r for r, d in zip(rows, base) if np.isfinite(d)]
    nBs = sum(r['flag'] == 'BRIGHT' for r in sup)
    say(f'supported by the reference: {len(sup)} of {len(rows)} (BRIGHT {nBs}, FAINT {len(sup) - nBs})')
    pw = hg1.power(rows, base, rng)
    say(f'pre-flight power (plant +0.20, scatter 0.25): {pw:.2f}')
    if MUTATE:
        ok = True
        flags = [r['flag'] for r in rows]; big = []
        bins = {}
        for i, r in enumerate(rows): bins.setdefault(int(np.floor(np.log10(r['sigma'])/0.1)), []).append(i)
        for _ in range(200):
            sh = list(flags)
            for idx in bins.values():
                for i, f in zip(idx, rng.permutation([flags[i] for i in idx])): sh[i] = f
            D, _, _ = hg1.D_stat([dict(r, flag=f) for r, f in zip(rows, sh)], base)
            big.append(D >= 0.15)
        frac = 1 - np.mean(big); say(f'MUTATE (a) shuffle: fraction not HOT-TRACKS-sized = {frac:.3f} (need >= 0.90)')
        ok &= frac >= 0.90
        rows_p = [dict(r, gobs=r['gobs']*(10**0.30 if r['flag'] == 'BRIGHT' else 1)) for r in rows]
        bp = deltas(rows_p, ref); Dp, nb, nf = hg1.D_stat(rows_p, bp)
        lo, hi, _ = bootstrap(rows_p, ref, rng, n=500)
        cp = hg1.classify(Dp, lo, hi, nb, nf, 1.0)
        say(f'MUTATE (b) plant +0.30: D {Dp:+.3f} [{lo:+.3f}, {hi:+.3f}] -> {cp} (need HOT TRACKS)')
        ok &= cp == 'HOT TRACKS'
        say('MUTATE controls behave as required' if ok else 'MUTATE controls FAILED')
        finish({'mutate_ok': bool(ok), 'shuffle_frac_not_big': float(frac), 'plant': dict(D=Dp, ci95=[lo, hi], cls=cp)})
        sys.exit(1 if ok else 0)
    D, nb, nf = hg1.D_stat(rows, base)
    lo, hi, nbad = bootstrap(rows, ref, rng)
    cls = hg1.classify(D, lo, hi, nb, nf, pw)
    say(f'PRIMARY: D = {D:+.3f} dex, 95% [{lo:+.3f}, {hi:+.3f}], in shared sigma bins BRIGHT {nb} / FAINT {nf}'
        f'  (reference draws floored: {nbad})')
    say(f'CLASS: {cls}')
    say('per sigma bin (log sigma lower edge: n_B, n_F, median Delta B, median Delta F):')
    per = {}
    for r, d in zip(rows, base):
        if np.isfinite(d): per.setdefault(int(np.floor(np.log10(r['sigma'])/0.1)), {'BRIGHT': [], 'FAINT': []})[r['flag']].append(d)
    for k in sorted(per):
        v = per[k]
        if v['BRIGHT'] and v['FAINT']:
            say(f'  {k/10:.1f}: {len(v["BRIGHT"])}, {len(v["FAINT"])}, {np.median(v["BRIGHT"]):+.3f}, {np.median(v["FAINT"]):+.3f}')
    arms = {}
    for flag in ('BRIGHT', 'FAINT'):
        v = [d for r, d in zip(rows, base) if r['flag'] == flag and np.isfinite(d)]
        arms[flag] = dict(n=len(v), median=float(np.median(v)), p16=float(np.percentile(v, 16)), p84=float(np.percentile(v, 84)))
        say(f'  unstratified {flag} (reported, not graded): n {len(v)}, median Delta {np.median(v):+.3f}, '
            f'16-84 {np.percentile(v, 16):+.3f}..{np.percentile(v, 84):+.3f}')
    variants = {}
    def var(lab, rv, rf):
        bv = deltas(rv, rf); Dv, nbv, nfv = hg1.D_stat(rv, bv)
        variants[lab] = dict(D=Dv, n_bright=nbv, n_faint=nfv, n_supported=int(np.isfinite(bv).sum()))
        say(f'  variant {lab}: D {Dv:+.3f} (BRIGHT {nbv} / FAINT {nfv}; supported {int(np.isfinite(bv).sum())})')
    for lab, kw in [('Nm>=10', dict(nm_min=10)), ('H0=73', dict(h0=73.0)), ('Ups_K=0.5', dict(ups=0.5)),
                    ('Ups_K=0.8', dict(ups=0.8)), ('faint_gas=0.1Mstar', dict(faint_gas=0.1))]:
        rv, _ = hg1.build(groups, mem, erass, **kw); var(lab, rv, ref)
    var('reference g_bar -0.2 dex', rows, Ref(gb, go, C, -0.2))
    var('reference g_bar +0.2 dex', rows, Ref(gb, go, C, +0.2))
    var('reference = all isolated (D5)', rows, Ref(*load(*ALL)))
    for r, d in zip(rows, base): r['delta'] = None if not np.isfinite(d) else float(d)
    finish(dict(D=D, ci95=[lo, hi], n_bright=nb, n_faint=nf, power=pw, cls=cls, k1=[A, sA], k3=k3, k5=float(k5),
                n_supported=len(sup), ref_floored=nbad, arms=arms, variants=variants, drops=drops, groups=rows))


def finish(obj):
    (HERE/f'hg2_kids_lowg_hot_gas{TAG}.json').write_text(json.dumps(obj, indent=1, default=float) + '\n')
    (HERE/f'hg2_kids_lowg_hot_gas{TAG}.out').write_text('\n'.join(out_lines) + '\n')


if __name__ == '__main__':
    main()
