import json, math, os, sys
HERE = os.getcwd(); sys.path.insert(0, HERE)
sys.path.insert(0, HERE + '/../../fable52_push/COL1_clock_collapse')
import col1_lib as L, final18_shells as F
from multiprocessing import Pool
KD1 = json.load(open(HERE + '/../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json'))
G = L.G; C = 2.99792458e5
st = KD1['footings']['canonical']['setting']; cos = L.Cosmo(st['h'], st['omega_d'], st['omega_b'])
rhoL = cos.OL * cos.rhoc0; a0 = L.a0_of('canonical')
def one(s):
    o = F.run('canonical', 10.45, zi=10.0, N=1200, s=s, wallscale=True)
    R = o['R_fold_z0_kpc']; q = o['q_front_z0']; a0M = G * 10**10.45 * q * (1 + q) / R**2
    return (s, R, q, a0M, a0M / (C * math.sqrt(G * rhoL)), a0M / a0, o['eps_u_max_run'])
if __name__ == '__main__':
    with Pool(4) as p:
        res = p.map(one, [0.0018, 0.0017, 0.0016, 0.0015])
    print('   s       R_fold(kpc)  q_front   a_0^M(m/s^2)  kappa_M    s_out    max u/a_0')
    for s, R, q, a0M, k, so, eu in res:
        print(f'{s:8.4f} {R:11.3f} {q:9.5f} {a0M*1e6/3.0857e19:.4e} {k:.3e} {so:.3e} {eu:.3e}')
    json.dump(res, open('bracket_s3.json', 'w'), indent=1)
