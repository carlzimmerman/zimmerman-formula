"""HG1_hot_gas_selector -- frozen criteria in FROZEN_CRITERIA.md (25bb540d4d). Model-free: no a0, no law.

Do KT2017 groups with an eRASS1 hot atmosphere sit further above the matched-SPARC disc reference than groups
without one, at matched sigma, after their hot gas is counted?  Run from anywhere; MUTATE=1 runs the controls.
"""
import json, os, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
os.chdir(REPO)                                              # compare.py reads real_research/data relative to the repo
sys.path.insert(0, str(REPO / 'reviews' / 'matched_clumping_2026_10_24'))
import compare as mc                                        # the matched-clumping lane's SPARC rule, read-only

MUTATE = os.environ.get('MUTATE') == '1'
TAG = '_MUTATE' if MUTATE else ''
G, MSUN, PC = mc.G, mc.MSUN, mc.PC
MPC = 1e6 * PC
C_KMS = 299792.458
SEED = 20261025
ERASS = REPO.parent / '_external_data' / 'cfg687_inputs' / 'erass1_main.tsv'
out_lines = []


def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out_lines.append(s)


# ---------- Galactic transform (K2) ----------
RA_P, DE_P, L_NCP = np.radians(192.85948), np.radians(27.12825), np.radians(122.93192)

def galactic(ra, de):
    ra, de = np.radians(ra), np.radians(de)
    sb = np.sin(de)*np.sin(DE_P) + np.cos(de)*np.cos(DE_P)*np.cos(ra - RA_P)
    b = np.arcsin(np.clip(sb, -1, 1))
    y = np.cos(de)*np.sin(ra - RA_P)
    x = np.sin(de)*np.cos(DE_P) - np.cos(de)*np.sin(DE_P)*np.cos(ra - RA_P)
    l = (L_NCP - np.arctan2(y, x)) % (2*np.pi)
    return np.degrees(l), np.degrees(b)


def vizier_rows(path):
    rows = [l.rstrip('\n').split('\t') for l in open(path) if l.strip() and not l.startswith('#')]
    return rows[0], rows[3:]                                 # header, then units and dashes lines skipped


# ---------- data ----------
def load_groups():
    h, rows = vizier_rows('real_research/data/kt2017_groups.tsv')
    g = {}
    for r in rows:
        try: g[int(r[0])] = dict(Nm=int(r[1]), sigma=float(r[2]))
        except ValueError: continue
    h, rows = vizier_rows('real_research/data/kt2017_galaxies.tsv')
    mem = {}
    for r in rows:
        try: pgc, ra, de, hrv, ks, pgc1 = int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), int(r[5])
        except ValueError: continue
        mem.setdefault(pgc1, []).append((pgc, ra, de, hrv, ks))
    return g, mem


def load_erass():
    out = []
    for l in open(ERASS):
        r = l.rstrip('\n').split('\t')
        try: ra, de, z, mg, r5 = float(r[1]), float(r[2]), float(r[3]), float(r[5]), float(r[8])
        except (ValueError, IndexError): continue
        if mg > 0 and r5 > 0: out.append((r[0].strip(), ra, de, z, mg*1e11, r5/1e3))
    return out


def sep_rad(ra1, de1, ra2, de2):
    ra1, de1, ra2, de2 = map(np.radians, (ra1, de1, ra2, de2))
    c = np.sin(de1)*np.sin(de2) + np.cos(de1)*np.cos(de2)*np.cos(ra1 - ra2)
    return np.arccos(np.clip(c, -1, 1))


def beta_mass_fraction(r, r500, rc_f=0.15, beta=2/3):
    """M_gas(<r)/M_gas(<R500) for the beta model (numerical, same convention as F1/CFG687)."""
    def m(R):
        x = np.linspace(0, R, 4001); rc = rc_f*r500
        return np.trapz(4*np.pi*x**2*(1 + (x/rc)**2)**(-1.5*beta), x)
    return m(r)/m(r500)


def build(groups, mem, erass, nm_min=5, h0=67.70, ups=0.6, faint_gas=0.0, dscale=1.0, match_scale=1.0):
    rows, drops = [], {}
    def drop(k): drops[k] = drops.get(k, 0) + 1
    for pgc1, gi in groups.items():
        if gi['Nm'] < nm_min or gi['sigma'] <= 0: drop('Nm/sigma'); continue
        ms = [m for m in mem.get(pgc1, []) if np.isfinite(m[4])]
        if len(ms) < 5: drop('<5 members with Ks'); continue
        prin = next((m for m in ms if m[0] == pgc1), None)
        if prin is None: drop('no principal galaxy'); continue
        hrv = prin[3]
        if hrv < 600: drop('HRV<600'); continue
        l, b = galactic(prin[1], prin[2])
        if not (179.94 <= l <= 359.94 and abs(b) >= 10): drop('outside eRASS1 footprint'); continue
        d = hrv/h0*dscale                                     # Mpc
        lk = np.array([10**(-0.4*(m[4] - 5*np.log10(d*1e6) + 5 - 3.28)) for m in ms])
        ra = np.array([m[1] for m in ms]); de = np.array([m[2] for m in ms])
        cra, cde = np.average(ra, weights=lk), np.average(de, weights=lk)  # small-field centroid
        rp = sep_rad(ra, de, cra, cde)*d                      # Mpc
        Rh = np.median(rp); r = 4/3*Rh
        if r <= 0: drop('zero radius'); continue
        mstar = ups*lk.sum()
        # X flag
        best = None
        for (nm, era, ede, z, mg, r5) in erass:
            if abs(C_KMS*z - hrv) > 1500: continue
            s = sep_rad(prin[1], prin[2], era, ede)*d
            if s <= 0.5*match_scale and (best is None or s < best[0]): best = (s, nm, mg, r5*dscale/1.0)
        if best:
            mg500, r500 = best[2]*dscale**2, best[3]      # catalogue Mgas500 scales as d^2 with our distance
            mgas = mg500*beta_mass_fraction(r, r500)
            flag = 'BRIGHT'
        else:
            mgas = faint_gas*mstar; flag = 'FAINT'
        mb = 0.5*mstar + mgas
        rm = r*MPC
        rows.append(dict(kind='group', name=str(pgc1), flag=flag, sigma=gi['sigma'], Nm=gi['Nm'], d_mpc=d, r_mpc=r,
                         mstar=mstar, mgas=mgas, gbar=G*mb*MSUN/rm**2, gobs=3*(gi['sigma']*1e3)**2/rm,
                         erass=best[1] if best else None))
    return rows, drops


# ---------- statistic ----------
def D_stat(rows, deltas):
    bins = {}
    for r, dl in zip(rows, deltas):
        if not np.isfinite(dl): continue
        k = int(np.floor(np.log10(r['sigma'])/0.1))
        bins.setdefault(k, {'BRIGHT': [], 'FAINT': []})[r['flag']].append(dl)
    num = den = 0.0; nb = nf = 0
    for k, v in bins.items():
        if v['BRIGHT'] and v['FAINT']:
            w = min(len(v['BRIGHT']), len(v['FAINT']))
            num += w*(np.median(v['BRIGHT']) - np.median(v['FAINT'])); den += w
            nb += len(v['BRIGHT']); nf += len(v['FAINT'])
    return (num/den if den else np.nan), nb, nf


def deltas_from(matrix, rows, cols=None):
    m = matrix if cols is None else matrix[:, cols]
    out = []
    for j, r in enumerate(rows):
        v = m[j][np.isfinite(m[j])]
        out.append(np.log10(r['gobs']) - np.median(v) if len(v) >= 8 else np.nan)
    return np.array(out)


def classify(D, lo, hi, nb, nf, power):
    if nb < 6 or nf < 6 or power < 0.5: return 'UNDERPOWERED'
    if D >= 0.15 and lo > 0: return 'HOT TRACKS'
    if hi < 0.10: return 'HOT DOES NOT TRACK'
    return 'UNDECIDED'


def bootstrap(rows, matrix, rng, n=2000):
    base = deltas_from(matrix, rows)
    idx_b = [i for i, r in enumerate(rows) if r['flag'] == 'BRIGHT']
    idx_f = [i for i, r in enumerate(rows) if r['flag'] == 'FAINT']
    out = []
    for _ in range(n):
        cols = rng.integers(0, matrix.shape[1], matrix.shape[1])
        dl = deltas_from(matrix, rows, cols)
        pick = list(rng.choice(idx_b, len(idx_b))) + list(rng.choice(idx_f, len(idx_f)))
        out.append(D_stat([rows[i] for i in pick], dl[pick])[0])
    out = np.array(out); out = out[np.isfinite(out)]
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), base


def power(rows, base, rng, n=500, plant=0.20, scat=0.25):
    ok = [i for i, d in enumerate(base) if np.isfinite(d)]
    hits = 0
    for _ in range(n):
        dl = np.full(len(rows), np.nan)
        for i in ok:
            dl[i] = rng.normal(plant if rows[i]['flag'] == 'BRIGHT' else 0.0, scat)
        D, nb, nf = D_stat(rows, dl)
        # interval from the same bootstrap rule on the synthetic deltas (groups only; reference fixed)
        idx_b = [i for i in ok if rows[i]['flag'] == 'BRIGHT']; idx_f = [i for i in ok if rows[i]['flag'] == 'FAINT']
        if len(idx_b) < 2 or len(idx_f) < 2: continue
        bs = []
        for _ in range(200):
            pick = list(rng.choice(idx_b, len(idx_b))) + list(rng.choice(idx_f, len(idx_f)))
            bs.append(D_stat([rows[i] for i in pick], dl[pick])[0])
        bs = np.array(bs); bs = bs[np.isfinite(bs)]
        if len(bs) and D >= 0.15 and np.percentile(bs, 2.5) > 0: hits += 1
    return hits/n


def main():
    rng = np.random.default_rng(SEED)
    say(f'HG1_hot_gas_selector{TAG}  (frozen 25bb540d4d; model-free, footing-independent)')
    curves = mc.sparc()
    # K1
    crow, _ = mc.clusters(); cm, _ = mc.match(crow, curves)
    k1 = mc.summarize(crow)['cluster']['median_dex']
    say(f'K1 X-COP median Delta = {k1:+.4f} (target +0.416 +/- 0.005)'); assert abs(k1 - 0.416) <= 0.005, 'K1 FAIL'
    # K2
    l, b = galactic(192.85948, 27.12825); assert abs(b - 90) < 0.01, 'K2 NGP FAIL'
    l, b = galactic(266.405, -28.936); assert min(l, 360 - l) < 0.1 and abs(b) < 0.1, f'K2 GC FAIL {l} {b}'
    say(f'K2 galactic transform OK (GC -> l {l:.3f}, b {b:.3f})')
    groups, mem = load_groups(); erass = load_erass()
    say(f'data: {len(groups)} KT2017 groups, {sum(len(v) for v in mem.values())} member rows, {len(erass)} eRASS1 entries')
    rows, drops = build(groups, mem, erass)
    rows2, _ = build(groups, mem, erass, dscale=1.1, match_scale=1.1)  # A1: X flags held fixed
    assert [r['flag'] for r in rows] == [r['flag'] for r in rows2], 'K3 flag mismatch'
    k3 = max(abs(a['gbar']/b_['gbar'] - 1) for a, b_ in zip(rows, rows2))
    say(f'K3 g_bar distance invariance: max rel diff {k3:.2e}'); assert k3 < 1e-6, 'K3 FAIL'
    say('drops:', json.dumps(drops))
    matrix, names = mc.match(rows, curves)
    base = deltas_from(matrix, rows)
    sup = [r for r, d in zip(rows, base) if np.isfinite(d)]
    say(f'groups built {len(rows)}: BRIGHT {sum(r["flag"]=="BRIGHT" for r in rows)}, FAINT {sum(r["flag"]=="FAINT" for r in rows)}; '
        f'SPARC-supported {len(sup)} (BRIGHT {sum(r["flag"]=="BRIGHT" for r in sup)})')
    pw = power(rows, base, rng)
    say(f'pre-flight power (plant +0.20, scatter 0.25): {pw:.2f}')
    if MUTATE:
        ok = True
        flags = [r['flag'] for r in rows]; classes = []
        for _ in range(200):
            bins = {}
            for i, r in enumerate(rows): bins.setdefault(int(np.floor(np.log10(r['sigma'])/0.1)), []).append(i)
            sh = list(flags)
            for idx in bins.values():
                perm = rng.permutation([flags[i] for i in idx])
                for i, f in zip(idx, perm): sh[i] = f
            rr = [dict(r, flag=f) for r, f in zip(rows, sh)]
            D, nb, nf = D_stat(rr, base)
            classes.append(D >= 0.15)
        frac = 1 - np.mean(classes); say(f'MUTATE (a) shuffle: fraction not HOT-TRACKS-sized = {frac:.3f} (need >= 0.90)')
        ok &= frac >= 0.90
        rows_p = [dict(r, gobs=r['gobs']*(10**0.30 if r['flag'] == 'BRIGHT' else 1)) for r in rows]
        mp, _ = mc.match(rows_p, curves)
        lo, hi, bp = bootstrap(rows_p, mp, rng, n=500)
        Dp, nb, nf = D_stat(rows_p, bp)
        cp = classify(Dp, lo, hi, nb, nf, 1.0)
        say(f'MUTATE (b) plant +0.30: D {Dp:+.3f} [{lo:+.3f}, {hi:+.3f}] -> {cp} (need HOT TRACKS)')
        ok &= cp == 'HOT TRACKS'
        say('MUTATE controls behave as required' if ok else 'MUTATE controls FAILED')
        finish({'mutate_ok': bool(ok)}); sys.exit(1 if ok else 0)
    D, nb, nf = D_stat(rows, base)
    lo, hi, _ = bootstrap(rows, matrix, rng)
    cls = classify(D, lo, hi, nb, nf, pw)
    say(f'PRIMARY: D = {D:+.3f} dex, 95% [{lo:+.3f}, {hi:+.3f}], in shared sigma bins BRIGHT {nb} / FAINT {nf}')
    say(f'CLASS: {cls}')
    for flag in ('BRIGHT', 'FAINT'):
        v = [d for r, d in zip(rows, base) if r['flag'] == flag and np.isfinite(d)]
        if v: say(f'  unstratified {flag}: n {len(v)}, median Delta {np.median(v):+.3f}, 16-84 {np.percentile(v,16):+.3f}..{np.percentile(v,84):+.3f}')
    variants = {}
    for lab, kw in [('Nm>=10', dict(nm_min=10)), ('H0=73', dict(h0=73.0)), ('Ups_K=0.5', dict(ups=0.5)),
                    ('Ups_K=0.8', dict(ups=0.8)), ('faint_gas=0.1Mstar', dict(faint_gas=0.1))]:
        rv, _ = build(groups, mem, erass, **kw); mv, _ = mc.match(rv, curves); bv = deltas_from(mv, rv)
        Dv, nbv, nfv = D_stat(rv, bv); variants[lab] = dict(D=Dv, n_bright=nbv, n_faint=nfv)
        say(f'  variant {lab}: D {Dv:+.3f} (BRIGHT {nbv} / FAINT {nfv})')
    for r, d in zip(rows, base): r['delta'] = None if not np.isfinite(d) else float(d)
    finish(dict(D=D, ci95=[lo, hi], n_bright=nb, n_faint=nf, power=pw, cls=cls, drops=drops, k1=k1, k3=k3,
                variants=variants, groups=[{k: v for k, v in r.items()} for r in rows]))


def finish(obj):
    (HERE/f'hg1_hot_gas_selector{TAG}.json').write_text(json.dumps(obj, indent=1, default=float) + '\n')
    (HERE/f'hg1_hot_gas_selector{TAG}.out').write_text('\n'.join(out_lines) + '\n')


if __name__ == '__main__':
    main()
