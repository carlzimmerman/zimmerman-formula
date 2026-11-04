"""A17 post-result diagnostic (not frozen, disclosed in ../FROZEN_A17.md): M2-M4 restarted from the cored M1 local minimum, log m22 = -0.644.
Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe19.py')).read()
exec(src[:src.index('# M1 scan')]); exec(src[src.index('def m1fit'):src.index('NAMES =')])
NAMES = ['log m22', 'log A', 'beta', 's', 'dn', 'dc']; x = [-.644]
print(f'M1 cored local minimum: rms to law {rms(GS, x):.4f}')
for n in [3, 4, 6]:
    x, at = tune(GS, n, x + [0, 1 / 3, 0, 0, 0][len(x) - 1:n - 1]); k = full(x, n)
    ns = sum(halo(g, k)[1]['rt'] > 0 for g in GS)
    print(f'\n{n} knobs from cored start', dict(zip(NAMES, np.round(x, 3).tolist())), 'at bound', [NAMES[i] for i in at], f'soliton in {ns}/171')
    grade(f'A17b {n} knobs, cored start', tot(GS, k), f'({n} knobs)')
