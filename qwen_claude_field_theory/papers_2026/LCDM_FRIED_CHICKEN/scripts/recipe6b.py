"""A5 post-result diagnostic of ../FROZEN_RECIPE.md: per-bin mass shift. Not part of the frozen grade. Rival language for the recipes, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
src = open('recipe6.py', encoding='utf-8').read().split("print('\\nMain rows')")[0]
exec(src)
GR = np.round(np.arange(-.3, .51, .1), 1)
def b1(fn, S, dm, **k): return np.mean([fn(a * 10**dm, b * 10**dm, **k) for a, b in zip(*S)], axis=0)
for tag, fn, k in (('L plain law', LAW, {}), ('R11 12 knobs', REC, dict(k=K11)), ('R11b 14 knobs', REC, dict(k=K14))):
    out, sh = [], []
    for i, S in enumerate(SETS):
        sl = slice(i * n, (i + 1) * n); ci = np.linalg.inv(COV[sl, sl]); best = None
        for dm in GR:
            m = b1(fn, S, dm, **k); x_ = (DAT[sl] - m) @ ci @ (DAT[sl] - m)
            if best is None or x_ < best[0]: best = (x_, dm, m)
        out.append(best[2]); sh.append(float(best[1]))
    m = np.concatenate(out); r = DAT - m; X = r @ ICOV @ r; print(f'{tag:16s} shifts {sh}; chi2 {X:.1f}/56 p {CH.sf(X, 56):.1e}', flush=True)
print('Post hoc, four extra parameters, not a grade. kappa = 1/2 FITTED; not theory closed.')
