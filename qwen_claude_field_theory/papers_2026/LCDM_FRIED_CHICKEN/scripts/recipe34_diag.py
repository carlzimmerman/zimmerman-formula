"""A32 post-result diagnostics (written after reading recipe34.out; not frozen gates). Per ../FROZEN_A32.md, section
'Post-result diagnostics'. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [os.path.join(HERE, 'recipe34.py')]
_src = open(os.path.join(HERE, 'recipe34.py'), encoding='utf-8').read(); __file__ = os.path.join(HERE, 'recipe34.py')
exec(_src[:_src.index("if os.environ.get('A32_TEST')")])
ST = json.load(open(os.path.join(HERE, 'recipe34.json')))
S3 = sload(ST['S3']); S1 = sload(ST['S1'][0])
def show(tag, S, idx=ALLI):
    o = evaluate(S, idx); e = stats(o['cur0'], idx)
    print(f'{tag}: E1 {e["e1"]:.4f} E2 {e["e2"]:.4f}; slope {o["slope"]:+.3f}; a(z)/a(0) ' + ' '.join(f'{o["rz"][z]:.3f}' for z in ZL) + '; rho_DE ratio ' + ' '.join(f'{o["rde"][z]:.3f}' for z in ZL)
          + '; GT ' + ' '.join(f'{o["gt"][z]:+.3f}' for z in ZL) + '; S(z) ' + ' '.join(f'{o["S"][(1., z)]:.3f}' for z in ZL) + '; S(f 0.5, 2) ' + f'{o["S"][(.5, 0.)]:.3f} {o["S"][(2., 0.)]:.3f}'
          + '; a at fit bound ' + str([k for k, a in o['a'].items() if not (1.01e-12 < a < .99e-8)]), flush=True)
    return o
print('(d1) attribution for S3 (DESI-constrained best) and S1:')
for tag, S in (('S3', S3), ('S1', S1)):
    show(f' {tag} as fitted', S)
    show(f' {tag} DE kept, all H exponents zeroed', Par(S.P, S.de, np.zeros(5), np.zeros(5)))
    show(f' {tag} DE at LCDM, H exponents kept', Par(S.P, DE_L, S.pH, np.zeros(5)))
    for k, fam in enumerate(FAM):
        pH = S.pH.copy(); pH[k] = 0.; show(f' {tag} drop H exponent {fam} only', Par(S.P, S.de, pH, np.zeros(5)))
print('\n(d2) what the S3 exponents do to the halos at z (base cosmology, all 171):')
for z in [0.] + ZL:
    E = ENV[1.]; b = bg(E['Om'], E['Ob'], *S3.de); XH = np.sqrt(e2at(b, z)); md = {fam: XH**S3.pH[k] for k, fam in enumerate(FAM)}
    cg = cmap(E['CG'][z], z, E['bL'], b); lM = shmr_z(S3.P, ALLI, z, np.log10(md['SHMR'])); p = dict(zip(NAMES, S3.P))
    cs = [float(np.interp(l, LM, cg)) * 10**p['dc'] * (10**l / 1e12)**p['sc'] * GS[i].sb**p['N2'] * md['CONC'] for i, l in zip(ALLI, lM)]
    fs = [np.clip(np.clip(p['f0'] + p['Df0g'] * GS[i].gr + p['f1'] * (np.log10(GS[i].Mb) - 9.5), -1, 1) * md['CONTR'], -1, 1) for i in ALLI]
    print(f' z {z}: H/H0 {XH:.3f}; SHMR N x {md["SHMR"]:.2f}, feedback e x {md["FB"]:.2f}, core x {md["CORE"]:.2f}, contraction x {md["CONTR"]:.2f}, c x {md["CONC"]:.2f}; '
          f'median log M200 {np.median(lM):.2f}; median c {np.median(cs):.1f}, c clipped (<1.01 or >200) {sum((c < 1.01) or (c > 200) for c in cs)}; contraction f at +-1 {sum(abs(f) >= 1 for f in fs)} of 171', flush=True)
print('\n(d3) holdout from the S3 point (leaky start, S3 bounds, tuned on GS[::2], 30 evaluations; not the frozen clean holdout):')
names, lo, hi = layout('pri'); lo3, hi3 = lo.copy(), hi.copy(); lo3[15:19] = [-.866, -1.29, -.01, -.01]; hi3[15:19] = [-.638, -.43, .01, .01]
Sh, cost, atb, _ = tune(S3, 'pri', ODD, 1., 30, lo3, hi3); print(f' tuned cost {cost:.2f}, at bound {atb}')
show(' unseen GS[1::2]', Sh, EVEN)
print('\nRival language; adopts nothing. Diagnostics, not gates. kappa = 1/2 FITTED; not theory closed.')
