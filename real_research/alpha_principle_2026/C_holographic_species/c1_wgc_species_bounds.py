#!/usr/bin/env python3
"""C1: WGC and species-scale relations (inequalities vs parametric equality). See C0_PREREGISTRATION.md.
Units hbar=c=1, Heaviside-Lorentz: e^2 = 4 pi alpha. M_red = reduced Planck mass 2.435e18 GeV, M_Pl = sqrt(8 pi) M_red = 1.221e19 GeV.
--mutate : flips the WGC electron ratio check to assert saturation (must FAIL) and asserts N_sat conventions agree (must FAIL)."""
import sys, math
from mpmath import mp, mpf, sqrt, pi, log
mp.dps = 30
MUT = '--mutate' in sys.argv
alpha = 1/mpf('137.035999177')
e = sqrt(4*pi*alpha)
Mred = mpf('2.435323e18'); Mpl = Mred*sqrt(8*pi)   # GeV
me = mpf('0.51099895e-3')
fails = []
def check(name, ok):
    print(('PASS ' if ok else 'FAIL ') + name)
    if not ok: fails.append(name)

print('e = %s ; e*M_red = %s GeV ; M_Pl = %s GeV' % (mp.nstr(e,8), mp.nstr(e*Mred,6), mp.nstr(Mpl,6)))
# C1a electron vs electric WGC (unit charge q=1): saturation would be m = sqrt2 e M_red
ratio = me/(sqrt(2)*e*Mred)
print('C1a  m_e/(sqrt2 e M_red) = %s   (log10 = %s)' % (mp.nstr(ratio,5), mp.nstr(mp.log10(ratio),5)))
sat = abs(ratio-1) < mpf('1e-3')
check('C1a electron does NOT saturate WGC (inequality holds with margin)', (not sat) and ratio < 1) if not MUT else check('C1a MUTATE: assert saturation', sat)
# Lower bound on alpha from WGC for the electron: alpha >= m_e^2/(8 pi M_red^2)
alpha_min = me**2/(8*pi*Mred**2)
print('C1a  WGC gives only alpha >= %s (actual alpha is %s times larger)' % (mp.nstr(alpha_min,4), mp.nstr(alpha/alpha_min,4)))

# C1b: N_sat for the three conventions
conv = {
 'C1: e M_red = M_red/sqrt(N)':        1/e**2,
 'C2: sqrt2 e M_red = M_red/sqrt(N)':  1/(2*e**2),
 'C3: e M_red = M_Pl/sqrt(N)':         8*pi/e**2,
}
counts = {'28 (bosonic dof)':28, '118 (all SM dof)':118, '126 (118+3RHnu+graviton)':126}
# verify dof counting arithmetic
bos = 2 + 16 + 3*3 + 1            # photon, gluons, W+,W-,Z massive, Higgs
fer = 6*3*4 + 3*4 + 3*2           # 6 quark flavours x 3 colours x 4, 3 charged leptons x 4, 3 Weyl neutrinos x 2
print('dof count: bosons %d, fermions %d, total %d' % (bos, fer, bos+fer))
check('dof arithmetic 28 + 90 = 118', bos == 28 and fer == 90 and bos+fer == 118)
hits = 0; trials = 0
print('%-36s %10s' % ('convention', 'N_sat'))
for k, v in conv.items():
    print('%-36s %10s' % (k, mp.nstr(v,6)))
    for kc, n in counts.items():
        trials += 1
        rel = abs(v-n)/n
        hit = rel < mpf('1e-3'); hits += hit
        print('      vs N=%-26s rel gap %s  hit=%s ; margin (eM_red)/(M_red/sqrt N) = %s' % (kc, mp.nstr(rel,4), hit, mp.nstr(e*sqrt(n),4)))
exp_chance = trials*2e-3/math.log(1e3)
print('C1b trials=%d hits=%d expected chance hits=%.2e' % (trials, hits, exp_chance))
check('C1b no convention/count pair hits within 1e-3', hits == 0)
vals = list(conv.values())
spread = max(vals)/min(vals)
print('C1c N_sat spread across conventions: factor %s' % mp.nstr(spread,5))
check('C1c conventions disagree (no forced O(1) coefficient)', spread > 1+1e-3) if not MUT else check('C1c MUTATE: assert conventions agree', spread < 1+1e-3)
# inequality reading: with the SM counts, e M_red exceeds the species scale in convention C1 for all counts >= 11
check('inequality e M_red >= M_red/sqrt(N) holds for N=118', e*sqrt(118) >= 1)
print('BOUND STATUS: WGC (C1a) and Lambda_WGC >= Lambda_sp are inequalities, satisfied with margin; no saturation; the species scale coefficient is parametric.')
print('exit', 1 if fails else 0)
sys.exit(1 if fails else 0)
