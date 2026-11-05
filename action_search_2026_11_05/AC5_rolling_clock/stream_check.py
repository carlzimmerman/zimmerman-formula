import sys,time
sys.argv=['evolve.py','--out','/dev/null']
src=open('action_search_2026_11_05/AC5_rolling_clock/evolve.py').read().split("\nrows = json.loads")[0]
ns={};exec(src,ns);fn=ns['build'](False)
import math
for (e,m,L,k) in [(.05,.3,.001,100.),(.5,.9,.001,100.),(2.,.01,.001,100.),(.05,.3,1.,10000.)]:
  for on in (1.0,0.0):
    t=time.time();a=ns['run_case'](fn,e,m,L,k,on,1e-11,False,math.sqrt(2*e));t1=time.time()-t
    t=time.time();b=ns['run_case_stream'](fn,e,m,L,k,on,1e-11,False,math.sqrt(2*e));t2=time.time()-t
    print(e,m,L,k,on,'maxI rel %.1e maxII rel %.1e'%(abs(a['max_I']/b['max_I']-1),abs(a['max_II']/b['max_II']-1)),'steps',a['steps'],b['steps'],'drift',a['omega_drift'],b['omega_drift'],'t %.1f/%.1f'%(t1,t2),flush=True)
