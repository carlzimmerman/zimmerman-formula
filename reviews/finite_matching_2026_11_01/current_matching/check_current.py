import sys,os
sys.dont_write_bytecode=True
for _v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[_v]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh,svdvals
from scipy.integrate import quad
from current import calculate,assemble,fermion_blocks,kernels,L,JS,QF

def main(path):
    start=time.monotonic();controls={};table=[];kernel_errors=[]
    for a,b in [(1,1),(1,1.00001),(1,.01),(1,0),(.001,.000001)]:
        G,I,LW,LU=kernels(a,b,.7)
        directI=quad(lambda x:x*(1-x)/(x*a+(1-x)*b),0,1,epsabs=1e-12)[0]
        directLW=quad(lambda x:x*(1-x)*math.log((x*a+(1-x)*b)/.7),0,1,epsabs=1e-12)[0]
        directLU=quad(lambda x:math.log((x*a+(1-x)*b)/.7),0,1,epsabs=1e-12)[0]
        kernel_errors.append(max(abs(I-directI)/max(1,abs(directI)),abs(LW-directLW),abs(LU-directLU),abs(G-(a-b)**2*directI)))
    controls['kernel_quadrature_max_error']=max(kernel_errors)
    controls['single_Majorana_limit_error']=abs((-.36*math.log(.36/.7)/(2*L))-(.36/L*(-3*kernels(.36,.36,.7)[2]+.36*kernels(.36,.36,.7)[1]-1/6)))
    matrix=[];mass=[];ward=[];UV=[]
    for e in (.01,.03):
        c=e/31;x0=7.367143721278508*math.sqrt(c)/e;Q2=c+(e*x0)**2;g=math.sqrt(29/200)*e
        for ratio in (1.,1.15,1.21,1.3):
            X=x0*ratio;r=calculate(X,e,e,g,1.,Q2);table.append(dict(e=e,X_over_treeCWmin=ratio,Q2=Q2,**r));o=assemble(X,e,e,g,1.);dt=1e-5;plus=assemble(X,e,e,g,1.,dt);minus=assemble(X,e,e,g,1.,-dt)
            expectedH=JS@o['H']-o['H']@JS;expectedM=-1j*(QF[:,None]*o['MF']+o['MF']*QF[None,:]);matrix.extend([float(np.max(abs((plus['H']-minus['H'])/(2*dt)-expectedH))),float(np.max(abs((plus['MF']-minus['MF'])/(2*dt)-expectedM)))])
            _,uv,fm=fermion_blocks(X,e,e,g,1.,Q2);full=np.sort(svdvals(o['MF'])**2);rep=np.sort(fm+[0.]*13+[2*e]*2);mass.append(float(np.max(abs(full-rep))))
            uv_full=float(np.sum(abs(expectedM)**2));matrix.append(abs(uv_full-uv))
            ward.extend([float(np.max(abs(eigvalsh(plus['H'])-eigvalsh(o['H'])))),float(np.max(abs(svdvals(plus['MF'])-svdvals(o['MF'])))),float(np.max(abs(plus['MV']-o['MV'])))])
            shifted=calculate(X,e,e,g,1.,Q2*math.exp(.04));UV.append(abs((shifted['total']-r['total'])/.02-r['UV_expected']))
        # Genuinely SUSY f=0,g=0 limit: scalar H commutes with phase, gauge graph decouples.
        ss=calculate(x0,e,e,0.,0.,Q2);expected=-sum(mult*((1+rr)*e*x0)**2*math.log(((1+rr)*e*x0)**2/Q2)/(2*L) for rr,mult in [(2.,8),(-3.,3),(-.5,12)])
        controls[f'SUSY_nongauge_limit_error_e{e}']=abs(ss['total']-expected)
        controls[f'SUSY_scalar_zero_e{e}']=abs(ss['scalar']);controls[f'gauge_decoupling_e{e}']=abs(ss['scalar_vector'])
        # Phase Ward/ispectral invariance also on the SUSY Higgs background.
        zz=assemble(x0,e,e,g,0.);zt=assemble(x0,e,e,g,0.,.07)
        ward.extend([float(np.max(abs(eigvalsh(zt['H'])-eigvalsh(zz['H'])))),float(np.max(abs(svdvals(zt['MF'])-svdvals(zz['MF']))))])
    controls.update(phase_matrix_derivative_max_error=max(matrix),representation_mass2_max_error=max(mass),phase_Ward_isospectral_max_error=max(ward),UV_scale_finite_difference_max_error=max(UV),UV_group_max_residual=max(abs(r['UV_residual']) for r in table),SV_Casimir_norm_relative_error=max(abs(r['SV_current_norm']/r['SV_current_norm_expected']-1) for r in table),null_counts_exact=all(r['scalar_null_count']==14 and r['vector_null_count']==12 for r in table))
    # Fixed-reference-scale equal-e rescaling predicts deltaF/e constant exactly in this model.
    small=table[:4];large=table[4:];controls['equal_e_scaling_max_error']=max(abs(a['total']/.01-b['total']/.03) for a,b in zip(small,large))
    checks={k:(bool(v) if isinstance(v,bool) else v<1e-8) for k,v in controls.items()};checks['eight_full_cases']=len(table)==8
    result=dict(claim_id='TP03_FULL_PHASE_CURRENT',checks=checks,controls=controls,cases=table,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['Actual local one-loop component coefficient at omega0, not all occupied derivative orders','No extra heavy geometric shift here','No anomaly/current lifetime, lightIR or physical halo state selected'])
    Path(path).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
