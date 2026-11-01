import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import mpmath as mp
from scipy.optimize import brentq
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from pressure_scan import cw
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize
mp.mp.dps=45
Z=mp.mpf('7.3671437212785083116194');P=mp.mpf('2.435e18');E=mp.mpf('.003')
def psi(t,e=E):
    t=mp.mpf(t);return cw(Z/mp.sqrt(31*e)*t,e,e,mp.sqrt(mp.mpf(29)/200)*e)/(e*e)
def der(t,n=1):return mp.diff(psi,mp.mpf(t),n)
def masses(t,e=.003):
    X=float(Z)/math.sqrt(31*e)*float(t);g=math.sqrt(29/200)*e;data=build_model(X,e,e,g,vertices=False);ext,labels=ext_basis(data);out,_=summarize(threshold(data,ext),labels)
    return {k:v['signed_mass']/e**2.5 for k,v in out.items()}
def main(path):
    start=time.monotonic();t0=mp.findroot(lambda t:der(t),(.99,1.01));grid=[float(t0)+(10-float(t0))*j/90 for j in range(91)];vals=[float(der(t,2)) for t in grid];brackets=[(a,b) for a,b,va,vb in zip(grid,grid[1:],vals,vals[1:]) if va>0>vb];assert brackets
    tf=mp.findroot(lambda t:der(t,2),brackets[0],solver='anderson');tk=mp.findroot(lambda t:t*der(t,2)-4*der(t),(t0,tf),solver='anderson');pref=31*mp.sqrt(3)*P/(4*Z)
    ts=[t0+(tf-t0)*mp.mpf(f) for f in ('.02','.15','.35','.6','.85','.98')]+[tk]
    rows=[]
    for t in sorted(ts):
        d1,d2=der(t),der(t,2);cs=masses(t);rr=d1/(t*d2)
        for ee in ('.001','.003','.005','.01'):
            e=mp.mpf(ee);mu=pref*e**mp.mpf('2.5')*d1;v=mu*Z/mp.sqrt(e)*t;m2=mu*mu*e**3*d2/(2*Z*Z);ma2=mu*mu*e**3*d1/(2*Z*Z*t);m=mp.sqrt(m2);ma=mp.sqrt(ma2);F=mu*mu/mp.sqrt(31);m32=F/(mp.sqrt(3)*P);beta=mp.sqrt(max(mp.mpf(0),1-4*rr));Gamma=m**3/(64*mp.pi*v*v)*(1-rr)**2*beta if 4*rr<1 else mp.mpf(0)
            rows.append(dict(t=float(t),e=float(e),mu_GeV=float(mu),R_GeV=float(v),m_sigma_GeV=float(m),m_phase_GeV=float(ma),phase_over_radial=float(mp.sqrt(rr)),phase_open=bool(4*rr<1),Gamma_phase_GeV=float(Gamma),m32_GeV=float(m32),photino_GeV=float(mu*e**mp.mpf('2.5')*cs['U1']),gauginos_GeV={k:float(mu*e**mp.mpf('2.5')*c) for k,c in cs.items()},cchi=cs['U1'],CW_force=float(d1),CW_radial_second=float(d2)))
    scales=[abs(psi(mp.mpf('1.2'),mp.mpf(e))/psi(mp.mpf('1.2'))-1) for e in ('.001','.01')]
    Lcrit=der(tf);muref=pref*E**mp.mpf('2.5')*Lcrit;Mcoeff=masses(tf)['U1'];mfold=muref*E**mp.mpf('2.5')*Mcoeff
    # Compare the old physical benchmark with the maximum actual CW force.
    oldmu=mp.mpf('18170662.111498855');Lold=oldmu/(pref*E**mp.mpf('2.5'))
    checks=dict(scaling=max(scales)<mp.mpf('1e-30'),ordered=t0<tk<tf,fold_has_positive_force=Lcrit>0,all_sample_radial_positive=all(r['m_sigma_GeV']>0 for r in rows),old_benchmark_above_fold=Lold>Lcrit,phase_both_sides=any(r['phase_open'] for r in rows) and any(not r['phase_open'] for r in rows))
    out=dict(claim_id='TP05_CANONICAL_FIRST_PROFILE',checks={k:bool(v) for k,v in checks.items()},t0=float(t0),t_phase_closure=float(tk),t_fold=float(tf),Lcrit=float(Lcrit),mu_fold_e003_GeV=float(muref),mchi_at_fold_e003_GeV=float(mfold),old_benchmark_force_over_max=float(Lold/Lcrit),scaling_errors=list(map(float,scales)),points=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ExactoneLoop rigidshape plus leading tunedW0tilt; finiteSUGRA/heavynormal/twoLoop completion follows')
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
