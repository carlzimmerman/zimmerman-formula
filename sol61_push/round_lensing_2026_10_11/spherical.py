"""Necessary 3D spherical positivity constraints, not a full deprojection."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack

HERE=Path(__file__).resolve().parent


def p(R,r):
    if r<=R:return 1.
    q=(R/r)**2
    return q/(1+np.sqrt(1-q))


def convert(A,annuli):
    cols=[]; ir=[]; jc=[]; vv=[]; offset=0; row=0; objective=np.zeros(A.shape[1])
    for block in annuli:
        rr=np.array(block['radii']); n=len(rr)
        sub=A[:,offset:offset+n].copy()
        sub[:,:-1]-=A[:,offset+1:offset+n]
        cols.append(sub)
        objective[offset+n-1]=1
        for i in range(n-1):
            ir.extend([row,row]); jc.extend([offset+i,offset+i+1]); vv.extend([1.,-1.]); row+=1
        for j in range(1,n):
            for i in range(j):
                ir.extend([row,row]); jc.extend([offset+i,offset+j]); vv.extend([-1.,p(rr[i],rr[j])]);row+=1
        offset+=n
    return np.concatenate(cols,axis=1),csr_matrix((vv,(ir,jc)),shape=(row,A.shape[1])),objective


def solve(A,b,C,objective,tol):
    m,n=A.shape
    opts=dict(primal_feasibility_tolerance=tol,dual_feasibility_tolerance=tol)
    B=vstack([hstack([csr_matrix(A),csr_matrix(-np.ones((m,1)))]),
              hstack([csr_matrix(-A),csr_matrix(-np.ones((m,1)))]),
              hstack([C,csr_matrix((C.shape[0],1))])],format='csr')
    rhs=np.r_[b,-b,np.zeros(C.shape[0])]
    c=np.r_[np.zeros(n),1.]
    fit=linprog(c,A_ub=B,b_ub=rhs,bounds=(0,None),method='highs',options=opts)
    if not fit.success:raise RuntimeError(fit.message)
    t=float(fit.x[-1]); mu=fit.ineqlin.marginals
    out=dict(t_min_arcsec=t,primal_violation=float(max(0,np.max(B@fit.x-rhs))),
             dual_column_violation=float(max(0,np.max(B.T@mu-c))),
             dual_gap=float(fit.fun-rhs@mu),shape_rows=C.shape[0],tolerance=tol)
    massB=vstack([csr_matrix(A),csr_matrix(-A),C],format='csr')
    massrhs=np.r_[b+t+1e-7,-b+t+1e-7,np.zeros(C.shape[0])]
    mf=linprog(objective,A_ub=massB,b_ub=massrhs,bounds=(0,None),method='highs',options=opts)
    if not mf.success:raise RuntimeError(mf.message)
    mm=mf.ineqlin.marginals
    out.update(angular_mass=float(mf.fun),mass_primal_violation=float(max(0,np.max(massB@mf.x-massrhs))),
               mass_dual_column_violation=float(max(0,np.max(massB.T@mm-objective))),
               mass_duality_gap=float(mf.fun-massrhs@mm))
    return out,mf.x,mu,mm


def main():
    checks=[]
    def ck(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    for q in (.01,.1,.5,.9,.999):
        bound=p(q,1)
        for r in (.005,.05,.25,.75,1,1.001,2,10,100):
            ck('shell_bound_%s_%s'%(q,r),p(q,r)-bound*p(1,r)>=-1e-12)
        ck('sharp_'+str(q),abs(p(q,1)-bound)<1e-12)
        radii=np.array([.03,.2,.8,1,2,10]);mass=np.arange(1,7)
        inner=sum(m*p(q,r) for m,r in zip(mass,radii));outer=sum(m*p(1,r) for m,r in zip(mass,radii))
        ck('positive_mixture_'+str(q),inner-bound*outer>=-1e-12)
        ck('MUTATE_projected_annulus_'+str(q),0-bound*1<0)
    prior=json.loads((HERE/'run/results.json').read_text())
    data=np.load(HERE/'run/certificates.npz');b=data['b']
    outputs=[];arrays={}
    for cell in prior['cells']:
        key=cell['background']+'_'+cell['geometry']
        original=data[key+'_A'];A,C,obj=convert(original,cell['annuli'])
        inc=1+np.arange(A.shape[1])%7;enc=[];off=0
        for block in cell['annuli']:
            n=len(block['radii']);enc.extend(np.cumsum(inc[off:off+n]));off+=n
        relative=float(np.max(np.abs(A@enc-original@inc))/max(1,np.max(np.abs(original@inc))))
        ck('operator_conversion_'+key,relative<1e-10,relative)
        solutions=[]
        for tol in (1e-9,1e-10):
            out,x,y,z=solve(A,b,C,obj,tol)
            ck('primal_dual_'+key+'_'+str(tol),out['primal_violation']<=1e-6 and
               out['dual_column_violation']<=1e-7 and abs(out['dual_gap'])<=1e-6*max(1,abs(out['t_min_arcsec'])) and
               out['mass_primal_violation']<=1e-6 and out['mass_dual_column_violation']<=1e-7 and
               abs(out['mass_duality_gap'])<=1e-6*max(1,abs(out['angular_mass'])),out)
            solutions.append(out)
            if tol==1e-10:
                arrays[key+'_enclosed_mass']=x; arrays[key+'_minimax_dual']=y;arrays[key+'_mass_dual']=z
        ck('refinement_'+key,abs(solutions[0]['t_min_arcsec']-solutions[1]['t_min_arcsec'])<1e-6)
        outputs.append(dict(background=cell['background'],geometry=cell['geometry'],solves=solutions))
    output=dict(status='necessary_spherical_inequalities_only',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,cells=outputs)
    outdir=HERE/'spherical_run'
    (outdir/'results.json').write_text(json.dumps(output,indent=2)+'\n')
    np.savez_compressed(outdir/'certificates.npz',**arrays)
    print('%d/%d checks'%(output['passed'],output['total']))
    for cell in outputs:print(cell['background'],cell['geometry'],json.dumps(cell['solves'][-1]))
    assert all(c['passed'] for c in checks)

if __name__=='__main__':main()
