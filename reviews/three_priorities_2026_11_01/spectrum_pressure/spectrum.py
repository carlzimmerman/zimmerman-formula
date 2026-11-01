"""Full canonical-K collective SU(5) tree spectrum; no leading-log spectrum surrogate."""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh, svdvals

def generators(n=5):
    basis=[]
    for i in range(n):
        for j in range(i+1,n):
            t=np.zeros((n,n),complex); t[i,j]=t[j,i]=1/math.sqrt(2); basis.append(t)
            t=np.zeros((n,n),complex); t[i,j]=-1j/math.sqrt(2);t[j,i]=1j/math.sqrt(2);basis.append(t)
    for j in range(1,n):
        t=np.zeros((n,n),complex)
        for i in range(j):t[i,i]=1/math.sqrt(j*(j+1))
        t[j,j]=-j/math.sqrt(j*(j+1));basis.append(t)
    return np.array(basis)

T=generators(); n=49; D=np.diag([2,2,2,-3,-3]); d=np.einsum('aij,ji->a',T,D)
R=np.zeros((24,n,n),complex); C=np.empty((24,24,24),complex)
for a in range(24):
    adj=np.array([np.einsum('kij,ji->k',T,(T[a]@tb-tb@T[a])/math.sqrt(2)) for tb in T]).T
    R[a,1:25,1:25]=adj;R[a,25:49,25:49]=adj
    for b in range(24):C[a,b]=np.einsum('kij,ji->k',T,(T[a]@T[b]+T[b]@T[a])/2)

def tensor(h,lam):
    y=np.zeros((n,n,n),complex)
    for a in range(24):
        y[0,1+a,1+a]=y[1+a,0,1+a]=y[1+a,1+a,0]=h
    for a in range(24):
        for b in range(24):
            for c in range(24):
                v=lam*C[a,b,c]
                y[1+a,1+b,25+c]=y[1+a,25+c,1+b]=y[25+c,1+a,1+b]=v
    return y

def cluster(vals,rel=2e-8):
    out=[]
    for v in sorted(float(x) for x in vals):
        if out and abs(v-out[-1]['m2'])<rel*max(1,abs(v),abs(out[-1]['m2'])):
            c=out[-1];c['m2']=(c['m2']*c['multiplicity']+v)/(c['multiplicity']+1);c['multiplicity']+=1
        else:out.append({'m2':v,'multiplicity':1})
    return out

def spectrum(X,h,lam,g,f=1.,y=None,full=False):
    if y is None:y=tensor(h,lam)
    aa=math.sqrt(2*f*h/(30*h*h+lam*lam));bb=h*X/lam
    z=np.r_[complex(X),1j*aa*d,bb*d]
    F=.5*np.einsum('ijk,j,k->i',y,z,z);F[0]+=f
    M=np.einsum('ijk,k->ij',y,z)
    rz=np.einsum('aij,j->ai',R,z)
    ds=g*np.einsum('i,ai->a',z.conj(),rz).real
    # A= W^dagger W; B_ij = conjugate(W_k) W_kij.
    A=M.conj().T@M;B=np.einsum('k,kij->ij',F.conj(),y)
    H=np.block([[A.real+B.real,-A.imag-B.imag],[A.imag-B.imag,A.real-B.real]])
    DL=math.sqrt(2)*g*np.concatenate([rz.real,rz.imag],axis=1)
    H+=DL.T@DL
    MV=2*g*g*(rz.conj()@rz.T).real
    mixing=math.sqrt(2)*g*np.einsum('i,aij->aj',z.conj(),R)
    MF=np.block([[M,mixing.T],[mixing,np.zeros((24,24),complex)]])
    es=eigvalsh(H);ev=eigvalsh(MV);ef=svdvals(MF)**2
    scale=max(1,float(max(es)),float(max(ev)),float(max(ef)))
    tol=1e-9*scale
    gold=np.concatenate([-rz.imag,rz.real],axis=1).T
    super2=float(sum(es)-2*sum(ef)+3*sum(ev))
    super4=float(es@es-2*ef@ef+3*ev@ev)
    neg=es[es < -tol]
    def term(v):
        p=v[v>1e-12*scale]
        return float(np.dot(p*p,np.log(p)-1.5))
    parts={'scalar':term(es),'Weyl':-2*term(ef),'vector':3*term(ev)}
    cw=sum(parts.values())/(64*math.pi**2) if len(neg)==0 else None
    out={'X':X,'h':h,'lambda':lam,'g':g,'f':f,'V_tree':float(np.vdot(F,F).real),
         'V_tree_reference':f*f*lam*lam/(lam*lam+30*h*h),
         'F_stationarity_max':float(max(abs(M@F.conj()))),'D_max':float(max(abs(ds))),
         'Goldstone_H_null_scaled':float(np.max(abs(H@gold)))/(scale*max(1,float(np.max(abs(gold))))),
         'Goldstino_M_null_scaled':float(max(abs(MF@np.r_[F.conj(),np.zeros(24)])))/(math.sqrt(scale)*max(1,float(max(abs(F))))),
         'STr_M2':super2,'STr_M2_scaled':super2/(146*scale),'STr_M4':super4,
         'scalar_negative_count':int(len(neg)),'scalar_min_m2':float(min(es)),
         'scalar_zero_count':int(sum(abs(es)<tol)),'Weyl_zero_count':int(sum(ef<tol)),
         'vector_zero_count':int(sum(abs(ev)<tol)),
         'vector_mass_reference':25*g*g*(aa*aa+bb*bb),
         'vector_reference_max_error':float(max(abs(np.sort(ev)-np.r_[np.zeros(12),np.full(12,25*g*g*(aa*aa+bb*bb))]))),
         'CW':cw,'CW_unweighted_parts':parts,'eigen_sign_tolerance':tol}
    if full:out.update(scalars=cluster(es),Weyls=cluster(ef),vectors=cluster(ev))
    return out

def controls():
    gram=np.einsum('aij,bji->ab',T,T)
    sym=np.einsum('abc,abd->cd',C,C.conj())
    cas=np.einsum('aij,ajk->ik',R[:,:25,:25],R[:,:25,:25])
    return {'TrTaTb_max_error':float(max(abs(gram-np.eye(24)).flat)),
            'symmetric_contraction_21_over_10_max_error':float(max(abs(sym-2.1*np.eye(24)).flat)),
            'adjoint_Casimir5_max_error':float(max(abs(cas[1:,1:]-5*np.eye(24)).flat)),
            'R_Hermitian_max_error':float(max(abs(R-R.conj().transpose(0,2,1)).flat)),
            'D2_traceless_equals_minusD':float(np.max(abs(D@D-np.eye(5)*np.trace(D@D)/5+D)))}

def main(path,mode='diagnostic'):
    h=lam=.6;g=math.sqrt(29/200)*lam;y=tensor(h,lam)
    rows=[spectrum(x,h,lam,g,y=y,full=True) for x in (0.,.1,1.,3.,10.)]
    checks={k:v<1e-8 for k,v in controls().items()}
    checks.update(valley_stationarity=all(r['F_stationarity_max']<1e-8 and r['D_max']<1e-8 for r in rows),
                  tree_height=all(abs(r['V_tree']/r['V_tree_reference']-1)<1e-10 for r in rows),
                  Goldstone_null=all(r['Goldstone_H_null_scaled']<1e-8 for r in rows),
                  Goldstino_null=all(r['Goldstino_M_null_scaled']<1e-8 for r in rows),
                  vector_multiplicity=all(r['vector_zero_count']==12 for r in rows),
                  vector_reference=all(r['vector_reference_max_error']<1e-8 for r in rows),
                  supertrace2=all(abs(r['STr_M2_scaled'])<1e-8 for r in rows))
    result={'claim_id':'TP01_FULL_SU5','mode':mode,'controls':controls(),'checks':checks,'cases':rows,
            'schema_note':'Negative eigenvalues are physical outcomes, not failed implementation checks.',
            'non_claims':['No derived portal','No higher-loop/IR/gravity completion','No coupling or ratio selection']}
    Path(path).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks':checks,'cases':[{k:r[k] for k in ['X','scalar_negative_count','scalar_min_m2','scalar_zero_count','Weyl_zero_count','STr_M2_scaled','STr_M4','CW']} for r in rows]},indent=2))
    assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'diagnostic')
