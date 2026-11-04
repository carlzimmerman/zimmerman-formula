"""Fast fixed-packet coherent scalar-pair pole; independent full-matrix control.

Normed units mu; e=.003. This keeps tree-pole vertices/neutral widths fixed.
It is a local Breit-Wigner model, not a full medium or higher-order threshold.
"""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_pole002/result.json'
DATA=json.loads(SOURCE.read_text())
GRAM=np.array(DATA['production_Gram_mu2']);WIDTH=np.array(DATA['Gamma_other_matrix_mu'])
M=DATA['Mpole'];E=.003;A2=2/(31*E)
lg,U=np.linalg.eigh(GRAM);LAMBDA=float(lg[-1]);VECTOR=U[:,-1]
GAMMA,V=np.linalg.eigh(WIDTH);WEIGHTS=abs(V.conj().T@VECTOR)**2
MEDIUM=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_medium001/result.json').read_text())
GAMMA_BOSON,V_BOSON=np.linalg.eigh(np.array(MEDIUM['Gamma_SSS_matrix_mu']))
WEIGHTS_BOSON=abs(V_BOSON.conj().T@VECTOR)**2
RANK1_RELATIVE_ERROR=float(np.linalg.norm(GRAM-LAMBDA*np.outer(VECTOR,VECTOR.conj()))/np.linalg.norm(GRAM))


def mass(x):
    return E/2*np.sqrt(np.asarray(x)**2+A2)


def sigma_cm(x,s,blocked_fermions=False):
    """Physical pair sigma v_CM, array broadcasting, normed mu^-2.

    Replace the Ecm=m nonrelativistic flux factor by its exact Ecm=sqrt(s)/2;
    all other vertices and neutral widths remain the on-pole packet values.
    blocked_fermions is a separate positive-rate extreme, not an actual bath.
    """
    ss=np.asarray(s,float);mm=mass(x);delta=ss-M*M
    beta=np.sqrt(np.maximum(0,1-4*mm*mm/ss));a=144*beta/(32*math.pi*np.sqrt(ss))
    if blocked_fermions:
        gg,weights=GAMMA_BOSON,WEIGHTS_BOSON
    else:gg,weights=GAMMA,WEIGHTS
    d=delta[...,None]
    z=np.sum(weights/(d+1j*M*gg),axis=-1)
    b=np.sum(weights*gg/(d*d+M*M*gg*gg),axis=-1)
    return 4/np.sqrt(ss)*LAMBDA*b/abs(1+1j*M*a*LAMBDA*z)**2


def pair_matrix(x,t,q,angular_nodes=24,blocked_fermions=False):
    """Isotropic cell-center <sigma v_Moller> for charged scalar bins.

    This is a midpoint radial-cell closure. Angular quadrature is split at
    the resonance and several widths, so a narrow angular pole is resolved.
    Output is positive and symmetric; bin weights/occupations are separate.
    No resonant NWA parent term may be counted again with this matrix.
    """
    from numpy.polynomial.legendre import leggauss
    q=np.asarray(q,float);p=t*q;m=float(mass(x));en=np.sqrt(m*m+p*p)
    out=np.zeros((len(q),len(q)))
    z,w=leggauss(angular_nodes)
    widthscale=M*float(max(GAMMA))
    for i in range(len(q)):
        for j in range(i,len(q)):
            s0=2*m*m+2*en[i]*en[j];d=2*p[i]*p[j]
            if d==0:
                value=float(sigma_cm(x,s0,blocked_fermions))*s0/(4*en[i]*en[j])
            else:
                center=(s0-M*M)/d
                offsets=[0.]+[sign*b for sign in (-1,1) for b in (1,3,10,30,100,300,1000,1e4,1e5,1e6)]
                cuts=sorted(set([-1.,1.]+[float(center+a*widthscale/d) for a in offsets if -1<center+a*widthscale/d<1]))
                value=0.
                for lo,hi in zip(cuts[:-1],cuts[1:]):
                    c=(hi+lo)/2+(hi-lo)*z/2;ss=s0-d*c
                    value+=float(w@(sigma_cm(x,ss,blocked_fermions)*ss/(4*en[i]*en[j])))*(hi-lo)/4
            out[i,j]=out[j,i]=value
    return out


def main(output):
    start=time.monotonic();rows=[]
    # The actual rank-one shortcut is checked against the full 4x4 inverse
    # for both sides of threshold and finite incoming widths.
    for x in (DATA['xpole']-.01,DATA['xpole']-.001,DATA['xpole'],DATA['xpole']+.001):
        m=float(mass(x))
        for vr in (0,1e-5,1e-4,.001,.01,.1):
            s=4*m*m+m*m*vr*vr;beta=math.sqrt(max(0,1-4*m*m/s))
            incoming=144*GRAM*beta/(32*math.pi*math.sqrt(s))
            D=np.linalg.inv((s-M*M)*np.eye(4)+1j*M*(WIDTH+incoming))
            full=4/math.sqrt(s)*float(np.trace(GRAM@D@WIDTH@D.conj().T).real)
            fast=float(sigma_cm(x,s))
            rows.append(dict(x=x,vrel_NR=vr,full=full,fast=fast,relative_error=abs(fast/full-1)))
    q=np.array([.01,.1,.3,1,2,3,5,8,13,20.])
    matrix_controls=[]
    for x,t in ((DATA['xpole']-.001,.0005),(DATA['xpole'],.00001)):
        a=pair_matrix(x,t,q,12);b=pair_matrix(x,t,q,32)
        weights=q*q/(np.exp(q)+1);norm=float(weights@b@weights)
        matrix_controls.append(dict(x=x,t=t,max_absolute_error=float(np.max(abs(a-b))),weighted_relative_repeat=abs(float(weights@a@weights)/norm-1),symmetric_error=float(np.max(abs(b-b.T))),minimum=float(np.min(b))))
    checks=dict(rank_one_Gram=RANK1_RELATIVE_ERROR<1e-12,
        full_matrix_agreement=max(r['relative_error'] for r in rows)<1e-9,
        positive_symmetric_pair_matrix=all(r['minimum']>=0 and r['symmetric_error']<1e-12 for r in matrix_controls),
        angular_repeat=max(r['weighted_relative_repeat'] for r in matrix_controls)<1e-3)
    result=dict(claim_id='CT09_FAST_COHERENT_POLE_KERNEL',checks={k:bool(v) for k,v in checks.items()},
        rank1_relative_error=RANK1_RELATIVE_ERROR,full_matrix_controls=rows,pair_matrix_controls=matrix_controls,
        scope='Fixed tree-pole couplings and absorptive matrix, rank-one production shortcut; center radial bins and split angular quadrature. No full medium, finite mass matching, cascade/inverse source or dynamic resonance theorem.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('checks','rank1_relative_error','runtime_seconds','peak_rss_bytes')}))
    assert all(checks.values()), checks
if __name__=='__main__':main(sys.argv[1])
