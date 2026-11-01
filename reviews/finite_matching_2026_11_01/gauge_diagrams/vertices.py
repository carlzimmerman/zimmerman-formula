"""Vector graph contractions in canonical real scalar and Takagi bases."""
import sys
sys.dont_write_bytecode=True
import numpy as np
import functions as vf


def group(m2, tol=2e-9):
    """Relative clustering after a relative machine-zero clip."""
    m2=np.asarray(m2,dtype=float).copy()
    scale=max(float(np.max(np.abs(m2))),1e-300)
    if np.min(m2)<-2e-10*scale:
        raise ValueError('tachyonic background')
    m2[abs(m2)<2e-11*scale]=0
    labels=np.empty(len(m2),int); values=[];members=[]
    for i in np.argsort(m2):
        if not values or abs(m2[i]-values[-1])>tol*scale:
            values.append(float(m2[i]));members.append([])
        labels[i]=len(values)-1;members[-1].append(int(i))
    values=[float(np.mean(m2[mm])) for mm in members]
    return np.array(values),labels


def aggregate(weights,labels):
    out=np.zeros(tuple(max(ll)+1 for ll in labels))
    grids=np.meshgrid(*labels,indexing='ij')
    np.add.at(out,tuple(g.ravel() for g in grids),weights.ravel())
    return out


def evaluate_weights(weights, masses, fun, Q2):
    total=0.;absolute=0.; terms=0
    threshold=max(np.max(abs(weights))*1e-17,1e-300)
    for idx in np.ndindex(weights.shape):
        w=weights[idx]
        if abs(w)<=threshold:
            continue
        term=w*fun(*(masses[j][i] for j,i in enumerate(idx)),Q2)
        total+=term;absolute+=abs(term);terms+=1
    return float(total),float(absolute),terms


def gauge_parts(z,R,g,ms,O,mf,U,mv,Ov,Q2=1.):
    """Return loop-stripped parts; U.T MF U is real nonnegative diagonal.

    mf contains masses, all other mass inputs contain squared masses.
    Eigenvectors are columns in the original field bases. z has 49 complex
    components; R is the conventional 24 x 49 x 49 Hermitian representation.
    """
    nr=len(ms);nf=len(mf);nv=len(mv);n=nr//2
    r=np.sqrt(2)*np.r_[z.real,z.imag]
    Jr=np.array([np.block([[-r0.imag,-r0.real],[r0.real,-r0.imag]]) for r0 in R])
    Jr=np.einsum('ba,bij->aij',Ov,Jr,optimize=True)
    Jm=np.einsum('ki,akl,lj->aij',O,Jr,O,optimize=True)
    # g^{aij}: sign irrelevant in the squared SSV contraction.
    ssv=g*g*np.transpose(Jm**2,(1,2,0))/4
    JO=np.einsum('aij,jk->aik',Jr,O,optimize=True)
    vs=2*g*g*np.sum(JO**2,axis=1)/4
    Jr0=np.einsum('aij,j->ai',Jr,r)
    dv=-g*g*(np.einsum('aij,bj->abi',Jr,Jr0)+np.einsum('bij,aj->abi',Jr,Jr0))
    dv=np.einsum('abk,ki->abi',dv,O,optimize=True)
    vvs=dv**2/4
    # The gaugino transforms in the same adjoint convention as A and B.
    RF=np.zeros((nv,nf,nf),complex);RF[:,:n,:n]=R
    RF[:,n:,n:]=R[:,1:25,1:25]
    G=g*np.einsum('ba,ki,bkl,lj->aij',Ov,U.conj(),RF,U,optimize=True)
    ffv=np.transpose(abs(G)**2,(1,2,0))/2
    bffv=np.transpose((G**2).real*mf[None,:,None]*mf[None,None,:],(1,2,0))/2
    # R_adj[a,b,c]=-i f[a,b,c], hence f=i R_adj in this index order.
    f=(1j*R[:,1:25,1:25]).real
    f=np.einsum('ia,jb,kc,ijk->abc',Ov,Ov,Ov,f,optimize=True)
    gw=g*g*f*f/12
    sm,sl=group(ms);fm,fl=group(mf*mf);vm,vl=group(mv)
    raw={'SSV':(ssv,[sl,sl,vl],[sm,sm,vm],vf.SSV),
         'VS':(vs,[vl,sl],[vm,sm],vf.VS),
         'VVS':(vvs,[vl,vl,sl],[vm,vm,sm],vf.VVS),
         'FFV':(ffv,[fl,fl,vl],[fm,fm,vm],vf.FFV),
         'barFFV':(bffv,[fl,fl,vl],[fm,fm,vm],vf.barFFV),
         'gauge':(gw,[vl,vl,vl],[vm,vm,vm],vf.gauge)}
    result={};diagnostic={}
    for name,(weights,labels,masses,fun) in raw.items():
        w=aggregate(weights,labels)
        result[name],ab,terms=evaluate_weights(w,masses,fun,Q2)
        diagnostic[name]={'absolute_sum':ab,'nonzero_mass_group_terms':terms}
    controls={'real_rep_antisymmetry':float(np.max(abs(Jr+Jr.transpose(0,2,1)))),
              'fermion_gauge_Hermiticity':float(np.max(abs(G-G.conj().transpose(0,2,1)))),
              'vector_mass_reconstruction_relative':float(np.max(abs(g*g*Jr0@Jr0.T-np.diag(mv))))/max(float(np.max(mv)),1e-300),
              'pure_gauge_sum_relative':float(abs(np.sum(f*f)-120))/120,
              'VVS_symmetry':float(np.max(abs(dv-dv.transpose(1,0,2))))}
    return {'parts':result,'sum':sum(result.values()),'controls':controls,'diagnostic':diagnostic,
            'mass_group_counts':[len(sm),len(fm),len(vm)]}
