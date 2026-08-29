import time,sys,sympy as sp
sys.path.insert(0,'.')
import fc_alpha2_fp_solve as M
T=[time.time()]
def lap(s):
    now=time.time(); print(f'{s}: {now-T[0]:.1f}s',flush=True); T[0]=now
L2=M.build('iso',0.3,10.0,0.2,1.0); lap('build(iso) [nterms=%d]'%len(sp.Add.make_args(L2)))
r=M.solve('iso',0.3,10.0,0.2,1.0); lap('solve(iso) full')
print('ISO result:',r[0],(f'alpha_1={r[1].real:+.5f} (target -1.2)  a2p={r[2].real:.4g} a2l={r[3].real:.4g}' if r[0]=='ok' else ''),flush=True)
