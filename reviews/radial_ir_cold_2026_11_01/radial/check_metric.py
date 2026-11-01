import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from radial_metric import calculate,derivative,K,L,assemble
from current import calculate as angular

def main(path):
    start=time.monotonic();cases=[];controls={};de=[];uv=[];norm=[]
    for e in (.01,.03):
        x0=7.367143721278508/math.sqrt(31*e);g=math.sqrt(29/200)*e;Q2=e/31+(e*x0)**2
        for ratio in (1.,1.15,1.21,1.3):
            X=x0*ratio;r=calculate(X,e,e,g,1.,Q2);ang=angular(X,e,e,g,1.,Q2);o,dH,dM,dV,_=derivative(X,e,e,g,1.);dt=1e-5;plus=assemble(X*math.exp(dt),e,e,g,1.);minus=assemble(X*math.exp(-dt),e,e,g,1.)
            de.extend([float(np.max(abs((plus[k]-minus[k])/(2*dt)-v))) for k,v in [('H',dH),('MF',dM),('MV',dV)]])
            norm.append(abs(float(np.sum(abs(dM)**2))-sum(ang['fermion_vertex_norm'] for _ in [0])))
            shifted=calculate(X,e,e,g,1.,Q2*math.exp(.04));uv.append(abs((shifted['total']-r['total'])/.02-r['UV_expected']))
            cases.append(dict(e=e,X_over_treeCWmin=ratio,Q2=Q2,angular_graph=ang['total'],radial_minus_angular=r['total']-ang['total'],**r))
        rr=calculate(x0,e,e,0,0,Q2);aa=angular(x0,e,e,0,0,Q2);controls[f'SUSY_nongauge_metric_equality_e{e}']=abs(rr['total']-aa['total']);controls[f'g0_SV_e{e}']=abs(rr['scalar_vector']);controls[f'g0_VV_e{e}']=abs(rr['vector_vector'])
        # The gauged SUSY slice has an extra light modulus; record, do not enforce A=F.
        rs=calculate(x0,e,e,g,0,Q2);aas=angular(x0,e,e,g,0,Q2);controls[f'gauged_SUSY_offshell_difference_e{e}']=rs['total']-aas['total']
    controls.update(radial_matrix_derivative_max_error=max(de),full_fermion_vertex_norm_error=max(norm),UV_scale_difference_error=max(uv),UV_group_residual=max(abs(r['UV_residual']) for r in cases),equal_e_scaling_error=max(abs(a['total']/.01-b['total']/.03) for a,b in zip(cases[:4],cases[4:])),null_counts=all(r['scalar_null_count']==14 and r['vector_null_count']==12 for r in cases))
    # Independent VV equal-mass projector integral: B'= -1/(6Lx), K0=1/(Lx).
    x=.7;yp=.31;fromformula=yp*yp*(3/(6*x)+.75*K(x,x))/(4*L);expected=5*yp*yp/(16*L*x);controls['VV_equal_mass_error']=abs(fromformula-expected)
    checks={k:(v if isinstance(v,bool) else v<1e-8) for k,v in controls.items() if not k.startswith('gauged_SUSY_offshell_difference')};checks['eight_cases']=len(cases)==8
    out=dict(claim_id='TP04_RADIAL_METRIC',checks=checks,controls=controls,cases=cases,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['Isolated Landau offshell graph, add actual radial heavy pullback before reduced mode interpretation','No complete occupied radial higherderivative matching or gaugevariation audit','No physical cold state or lifetime selected'])
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
