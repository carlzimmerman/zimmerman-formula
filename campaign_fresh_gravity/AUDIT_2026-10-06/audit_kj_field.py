# Audit: field-level size of the CFG372 k_J(a) error on a LINEAR Gaussian field (no PM run). Engine imported read-only.
import os, sys, math, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CFG372_pressure_filtered_phantom'))
os.environ['CFG372_THREADS'] = '2'
import cfg372_pm as E
from scipy import fft as sfft
N = 128; m = E.Mesh(N)
rng = np.random.default_rng(359)
wk = sfft.rfftn(rng.standard_normal((N,)*3)) / N**1.5
kk = np.sqrt(m.kx**2 + m.ky**2 + m.kz**2).astype(np.float64)
dk0 = wk * np.sqrt(E.P_lin0(kk) / (E.L / N)**3) * N**1.5; dk0[0,0,0] = 0
def src(a, kJ):
    D = E.Dgrow(a); dk = dk0 * D
    phik = (-1.5 * E.Om / a) * dk * m.ik2
    Wk = 1.0 / (1.0 + kk**2 / kJ**2) if kJ else 1.0
    gb = [E.FB * (-m.inv(1j * kv * phik * Wk)) for kv in m.kvec]
    y = np.sqrt(sum(g**2 for g in gb)) / (a * E.a0_code(a, 'FLAT', 'canonical'))
    w = E.nu_mono(y).astype(np.float32) - 1.0
    s = -m.inv(sum(1j * kv * m.fwd(w * g) for kv, g in zip(m.kvec, gb)))
    sk = m.fwd(s); band = (kk > 0.7) & (kk < 1.3)
    return float(np.sqrt(np.mean(s**2))), float(np.sqrt(np.mean(np.abs(sk[band])**2)))
cs = lambda T: math.sqrt(5*1.380649e-23*T/(3*0.6*1.67262192e-27))/1e3
print('a   T     rms(code)/rms(T0)  rms(correct)/rms(T0)   k~1 band: code  correct   correct/code')
for T in (1e6, 1e4):
    for a in (1.0, 0.667, 0.5, 0.333, 0.2):
        r0, b0 = src(a, None)
        kc = math.sqrt(1.5*E.Om*a)*100/cs(T); kr = math.sqrt(1.5*E.Om/a)*100/cs(T)
        rc, bc = src(a, kc); rr, br = src(a, kr)
        print(f'{a:.3f} {T:.0e}  {rc/r0:.3f}  {rr/r0:.3f}   {bc/b0:.3f}  {br/b0:.3f}  {br/bc:.2f}')
