"""POST-HOC (after reading CFG58 .out): Omega_m = hunt_lib's 0.3134 with the ddof=0 + Upsilon-endpoint error reading; field dwarfs, statistic C."""
import numpy as np, math, importlib.util
exec(open('post2_diag.py').read().split("fd(1,(1,2,4)")[0])
c.OMEGA_M=0.14237/0.674**2; c.RHO_M=c.OMEGA_M*c.RHO_C; c._EP.clear()
fd(0,(1,4),"post-hoc Omega_m=0.3134, ddof=0, ups endpoints")
for foot in ('canonical','alt'):
    L=c.statC(ALL,base.copy(phi=0.0,foot=foot,est='K',re_key='Re_maj')); S=c.statC(ALL,base.copy(phi=1.0,foot=foot,est='K',re_key='Re_maj'))
    cs=[]
    for v in (0.1,1.0,10.0):
        # collapse floor for stat C as CFG58 declares: half range of predicted slope over M_c x0.1/x1/x10
        b=base.copy(phi=1.0,foot=foot,est='K',re_key='Re_maj',mcoll_div=1.0/v); cs.append(c.statC(ALL,b)['pred'])
    fl=0.5*(max(cs)-min(cs)); errS=math.sqrt(S['err']**2+fl**2)
    print(foot,f"obs {L['obs']:+.4f}+/-{L['err']:.4f} pL {L['pred']:+.4f} zL {L['z']:+.2f} pS {S['pred']:+.4f} floor {fl:.4f} errS {errS:.4f} zS {(S['obs']-S['pred'])/errS:+.2f} dslope {S['pred']-L['pred']:+.4f} nofloor zS {S['z']:+.2f}")
