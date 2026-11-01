"""Finite-splitting one-loop unbroken gaugino masses, Martin0509115v2 §III.

Imported model is immutable TP03. No loop-log expansion in F/M² is made.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json, math, resource
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/two_loop'))
from model import build_model,component_data
L=16*math.pi**2
Z0=7.367143721278508

def B0(x,y,Q2):
    """Finite -integral_0^1 log[(tx+(1-t)y)/Q²] at p²=0."""
    if x==0 and y==0:return 0. # only multiplied by exactly zero internal mass
    if x==0:return 1-math.log(y/Q2)
    if y==0:return 1-math.log(x/Q2)
    if abs(x-y)<1e-5*max(x,y):
        u=(x-y)/y
        return -math.log(y/Q2)-sum((-1)**(k+1)*u**k/(k*(k+1)) for k in range(1,9))
    return 1-(x*math.log(x/Q2)-y*math.log(y/Q2))/(x-y)

def ext_basis(data):
    R=data['R'];z=data['z'];n=len(z);ng=len(R)
    rz=np.einsum('aij,j->ai',R,z)
    un=np.where(np.linalg.norm(rz,axis=1)<1e-10*max(np.linalg.norm(z),1e-300))[0]
    adj=R[:,1:25,1:25]
    C=np.einsum('aik,akj->ij',adj[un],adj[un]).real
    vals,V=eigh(C[np.ix_(un,un)])
    ext=np.zeros((n+ng,len(un)),complex);ext[n+un,:]=V
    return ext,vals

def threshold(data,ext,Q2=1.,xi=0.):
    n=len(data['z']);nf=len(data['mF']);ng=len(data['R']);m=data['mF'];U=data['U']
    R=data['R'];g=data['g'];z=data['z']
    if xi:
        rz=np.einsum('aij,j->ai',R,z)
        Gold=math.sqrt(2)*np.concatenate([-rz.imag,rz.real],axis=1).T
        ms,O=eigh(data['H']+xi*g*g*Gold@Gold.T)
        ms[abs(ms)<2e-11*max(np.max(abs(ms)),1e-300)]=0
    else:ms,O=data['mS2'],data['O']
    Em=data['E']@O
    dy=np.zeros((nf,nf,len(ms)),complex)
    dy[:n,:n]=np.einsum('ijk,ka->ija',data['Y'],Em)
    dJ=math.sqrt(2)*g*np.einsum('ka,pki->pia',Em.conj(),R,optimize=True)
    dy[n:,:n]=dJ;dy[:n,n:]=dJ.transpose(1,0,2)
    y=np.einsum('Ia,JK,IJk->aKk',ext,U,dy,optimize=True)
    bs=np.array([[B0(float(x),float(v),Q2) for v in ms] for x in m*m])
    scalar=-np.einsum('aIk,bIk,Ik,I->ab',y,y,bs,m,optimize=True)/L
    RF=np.zeros((ng,nf,nf),complex);RF[:,:n,:n]=R
    if n==49:RF[:,n:,n:]=R[:,1:25,1:25]
    elif ng:RF[:,n:,n:]=0 # U(1) benchmark has neutral gaugino
    # g^{aI}_K = row I (external dagger), column K (internal Weyl).
    G=g*np.einsum('ba,Iu,bIJ,JK->auK',data['Ov'],ext.conj(),RF,U,optimize=True)
    bv=np.array([[3*B0(float(x),float(v),Q2)+(xi*B0(float(x),float(xi*v),Q2) if xi else 0.) for x in m*m] for v in data['mV2']])
    vector=-np.einsum('auI,avI,aI,I->uv',G,G,bv,m,optimize=True)/L
    total=scalar+vector
    return {'matrix':total,'scalar':scalar,'vector':vector}

def summarize(out,C):
    total=out['matrix'];rows={}
    for c,name in [(3,'SU3'),(2,'SU2'),(0,'U1')]:
        ix=np.where(abs(C-c)<1e-7)[0]
        if not len(ix):continue
        rows[name]={'multiplicity':len(ix),'signed_mass':float(np.trace(total[np.ix_(ix,ix)]).real/len(ix)),
                    'scalar':float(np.trace(out['scalar'][np.ix_(ix,ix)]).real/len(ix)),
                    'vector':float(np.trace(out['vector'][np.ix_(ix,ix)]).real/len(ix))}
    target=np.zeros_like(total)
    for c,name in [(3,'SU3'),(2,'SU2'),(0,'U1')]:
        if name not in rows:continue
        ix=np.where(abs(C-c)<1e-7)[0];target[ix,ix]=rows[name]['signed_mass']
    scale=max(np.max(abs(total)),1e-300)
    return rows,float(np.max(abs(total-target))/scale)

def ordinary(F):
    Y=np.zeros((3,3,3),complex)
    import itertools
    for p in itertools.permutations([0,1,2]):Y[p]=1.
    d=component_data(Y,np.array([1.,0,0],complex),np.array([F,0,0],complex),np.array([np.diag([0.,1.,-1.])]),.2,vertices=False)
    ext=np.array([[0],[0],[0],[1]],complex)
    return float(threshold(d,ext)['matrix'][0,0].real)

def run(path):
    checks={};diagnostics={};rows=[]
    for F in [.1,.5]:
        # Here F denotes W_X; the superspace auxiliary is F_aux=-W_X*.
        # The signed ordinary-messenger mass therefore has the opposite sign.
        expected=-2*.2**2/L*((1+F)*math.log1p(F)+(1-F)*math.log1p(-F))/F
        got=ordinary(F);diagnostics['ordinary_'+str(F)]={'got':got,'expected':expected}
        checks['ordinary_finite_F_'+str(F)]=abs(got/expected-1)<2e-11
    for e,r in [(.01,1.),(.01,1.21),(.03,1.),(.03,1.21),(.0001,1.)]:
        X=r*Z0/math.sqrt(31*e);g=math.sqrt(29/200)*e
        d=build_model(X,e,e,g,vertices=False);ext,C=ext_basis(d)
        out=threshold(d,ext);groups,deg=summarize(out,C)
        alt=threshold(d,ext,Q2=7.);gauge=threshold(d,ext,xi=1.)
        scale=max(np.max(abs(out['matrix'])),1e-300)
        qerr=float(np.max(abs(alt['matrix']-out['matrix']))/scale)
        xerr=float(np.max(abs(gauge['matrix']-out['matrix']))/scale)
        row={'e':e,'r':r,'X':X,'groups':groups,'degeneracy_error':deg,'Q_error':qerr,'xi_error':xerr,
             'minimum_positive_tree_mass':float(math.sqrt(min(d['mS2'][d['mS2']>0].min(),d['mF2'][d['mF2']>0].min()))),
             'vector_mass':float(math.sqrt(max(d['mV2'])))}
        rows.append(row);tag=str(e)+'_'+str(r)
        checks['subgroup_degeneracy_'+tag]=deg<2e-8
        checks['Q_independence_'+tag]=qerr<2e-8
        checks['xi_independence_'+tag]=xerr<2e-8
    # Exact scaling follows from rescaling every mass and vertex; this checks implementation.
    for name in ['SU3','SU2','U1']:
        ref=rows[0]['groups'][name]['signed_mass']/.01**2.5
        errors=[abs(row['groups'][name]['signed_mass']/row['e']**2.5/ref-1) for row in rows if row['r']==1.]
        diagnostics['scaling_'+name]=max(errors);checks['e_scaling_'+name]=max(errors)<2e-8
    d=build_model(2.,.01,.01,math.sqrt(29/200)*.01,f=0.,vertices=False);ext,C=ext_basis(d)
    susy=threshold(d,ext)['matrix'];diagnostics['SUSY_zero_max']=float(np.max(abs(susy)))
    checks['SUSY_zero']=np.max(abs(susy))<1e-15
    # f scaling at the first point, holding z and e fixed.
    d=build_model(rows[0]['X']*2,.01,.01,math.sqrt(29/200)*.01,f=4.,vertices=False);ext,C=ext_basis(d)
    groups,_=summarize(threshold(d,ext),C)
    ferr=max(abs(groups[n]['signed_mass']/rows[0]['groups'][n]['signed_mass']/2-1) for n in groups)
    diagnostics['sqrt_f_scaling']=ferr;checks['sqrt_f_scaling']=ferr<2e-8
    checks={k:bool(v) for k,v in checks.items()}
    result={'claim_id':'TP04-FINITE-GAUGINO','checks':checks,'diagnostics':diagnostics,'cases':rows,
            'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'Leading one-loop pole mass, exact tree splittings; no finite two-loop self-energy or nonperturbative claim.'}
    Path(path).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    assert all(checks.values()),checks

if __name__=='__main__':run(sys.argv[1])
