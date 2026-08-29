import time,sys; sys.path.insert(0,'.')
import fc_alpha2_fp_solve as M
T=time.time()
for kbv in [0.05,0.3]:
    t0=time.time(); r=M.solve('iso',kbv,10.0,0.2,1.0)
    print(f'K_B={kbv}: {r[0]}',(f'alpha_1={r[1].real:+.5f} (target {-4*kbv:+.3f})  a2p={r[2].real:.5g} a2l={r[3].real:.5g}' if r[0]=='ok' else ''),f'[{time.time()-t0:.0f}s]',flush=True)
print(f'ISO total {time.time()-T:.0f}s (1st includes build; 2nd reuses cache)',flush=True)
