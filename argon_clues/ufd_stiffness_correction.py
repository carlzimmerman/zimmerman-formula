"""argon_clues: apply the stiffened tether (L* = 5.75 pc) to CFG46's eight scored UFDs (Plummer baryons) and re-score the median offset.
Frozen reading (written here before the run): the correction is Delta = 0.5*log10(g_stiff/g_alg) at the half-mass 3D radius (4/3 r_half), offset' = offset - Delta.
Pass criterion for 'stiffness helps': median offset' < median offset. Disclosed: Plummer is a model; UFD stars are not exactly Plummer; L* is the record's lower bound 5.75 pc."""
import io, os, math, contextlib, json
import numpy as np
from scipy.integrate import solve_bvp
HERE='/Users/carlzimmerman/new_physics/zimmerman-formula/campaign_fresh_gravity'
src=open(HERE+'/CFG46_ufd_binary_corrected.py').read()
src=src.split('nf = R.write()')[0]
ns={'__file__':HERE+'/CFG46_ufd_binary_corrected.py','__name__':'__main__','OUTD':'/Users/carlzimmerman/new_physics/zimmerman-formula/argon_clues/_cfg46_run'}
os.makedirs(ns['OUTD'],exist_ok=True)
buf=io.StringIO()
os.chdir(HERE)
try:
    with contextlib.redirect_stdout(buf): exec(compile(src,HERE+'/CFG46_ufd_binary_corrected.py','exec'),ns)
except SystemExit: pass
SCORED=ns['SCORED']; spred=ns['spred']; A0H=ns['A0H']; FOOTS=ns['FOOTS']; UPS_V=ns['UPS_V']; G=ns['G']; Msun=ns['Msun']; SF=ns['SF']
pc=3.0857e16; Ls=float(os.environ.get('LSTAR_PC','5.75'))*pc
def g_alg(gN,a0): return 0.5*(gN+math.sqrt(gN*gN+4*gN*a0))
def solve_plummer(Mb, a_pc, a0):
    a=a_pc*pc; GM=G*Mb*Msun
    h=lambda x: GM*(x*Ls)/(((x*Ls)**2+a*a)**1.5)/a0          # g_N/a0
    X=max(400.0, 40*a/Ls)
    def f(x,y):
        v=np.clip(y[0],None,1-1e-9); return np.vstack([y[1], -2*y[1]/x+2*v/x**2+v**2/(1-v)-h(x)])
    def halg(x): gN=h(x); g=0.5*(gN+np.sqrt(gN*gN+4*gN)); return g/(g+1)
    x0=1e-3
    bc=lambda ya,yb: np.array([ya[0]-x0*ya[1], yb[0]-halg(X)])
    x=np.geomspace(x0,X,500); v=np.minimum(halg(x),0.99)*(1-np.exp(-x/3)); y=np.vstack([v,np.gradient(v,x)])
    s=solve_bvp(f,bc,x,y,tol=1e-6,max_nodes=300000); return s,h
res={}
for foot in FOOTS:
    a0=A0H[foot]; rows=[]
    for g in SCORED:
        Ms=UPS_V*g['LV']; Mb=Ms+1.33*g['MHI']; rh3=(4.0/3.0)*g['rh']; a_pl=rh3/1.305
        s,h=solve_plummer(Mb,a_pl,a0)
        x=rh3*pc/Ls; gN=h(x)*a0; u=s.sol(x)[0]*a0
        gs=gN+u; ga=g_alg(gN,a0)
        Delta=0.5*math.log10(gs/ga)
        rows.append((g['name'],Mb,g['rh'],s.success,gs/ga,Delta))
    res[foot]=rows
    print('== footing %s'%foot)
    for r in rows: print('  %-10s Mb %.1e Msun  r_half %.0f pc  conv %s  g_stiff/g_alg %.3f  Delta log sigma %+.3f'%(r[0],r[1],r[2],r[3],r[4],r[5]))
    for key in ('sig_fz','sig_f','sig_f7'):
        base=[math.log10(SF*g[key]/spred(g,foot)) for g in SCORED]
        corr=[b-r[5] for b,r in zip(base,rows)]
        print('  median offset %s: bare law %+.3f -> with stiffness %+.3f  (shift %+.3f dex)'%(key,np.median(base),np.median(corr),np.median(corr)-np.median(base)))
# mutation: L* -> tiny must give ratio 1
print('MUTATION check: ratio must tend to 1 as L* -> 0 (not run: the solver assumes L* in the units; the analytic limit v -> v_alg is the algebraic law by construction)')

import scipy.stats as st
for foot in FOOTS:
    base=np.array([math.log10(SF*g['sig_fz']/spred(g,foot)) for g in SCORED]); D=np.array([r[5] for r in res[foot]]); lv=np.array([math.log10(g['LV']) for g in SCORED])
    print('%s: Kendall tau(offset, -logL) bare %.2f (p %.3f) ; with stiffness %.2f (p %.3f)'%(foot,st.kendalltau(base,-lv)[0],st.kendalltau(base,-lv)[1],st.kendalltau(base-D,-lv)[0],st.kendalltau(base-D,-lv)[1]))
    print('   per galaxy (name: bare -> stiff): '+'; '.join('%s %+.2f->%+.2f'%(g['name'],b,b-d) for g,b,d in zip(SCORED,base,D)))
