import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import math,json,resource,time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];TP4=HERE.parent
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/current_matching'))
from current import assemble,R,d,L

def main(path):
    start=time.monotonic();e=.003;g=math.sqrt(29/200)*e;X=7.367143721278508/math.sqrt(31*e)
    o=assemble(X,e,e,g,1.);q=np.einsum('a,aij->ij',d.real/math.sqrt(30),R);qadj=q[1:25,1:25]
    J=np.block([[-q.imag,-q.real],[q.real,-q.imag]])
    rz=np.einsum('aij,j->ai',R,o['z']);Z=np.concatenate([-rz.imag,rz.real],axis=1).T
    H=o['H']+2*g*g*Z@Z.T;AF=o['MF'].conj().T@o['MF'];QF=np.zeros((73,73),complex);QF[:49,:49]=q;QF[49:,49:]=qadj
    es,Vs=eigh(H);ef,Vf=eigh(AF);ev,Vv=eigh(o['MV'])
    masks=[np.linalg.norm(J@Vs,axis=0)>1e-8,np.linalg.norm(QF@Vf,axis=0)>1e-8,np.linalg.norm(qadj@Vv,axis=0)>1e-8]
    spec=[es,ef,ev];M=math.sqrt(min(float(min(a[b])) for a,b in zip(spec,masks)));Mmax=math.sqrt(max(float(max(a)) for a in spec));counts=[int(sum(b)) for b in masks]
    authored=json.load(open(TP4/'gapless_charge/decay_bound/run_001/result.json'));units=json.load(open(TP4/'run_units/result.json'))
    Y2=32**2*5*g*g;B2=Y2*101**2;S=64*5*g*g
    integral_ratio=math.gamma(1.5)/math.gamma(3.5)
    loop=2*64*512*256*integral_ratio/L*Y2*max(B2,S);inclusive=math.sqrt(32768*16/2);c7=inclusive*loop
    mass=.001;mu=mass/(units['photino_mass_coefficient']*e**2.5);Mphys=M*mu;F=mu*mu/math.sqrt(31)
    gammaG=mass**5/(16*math.pi*F*F);phase_unit=mass**7/(256*math.pi**3*Mphys**6);gammahard=c7*c7*phase_unit
    hb=units['constants']['hbar_GeV_s'];age=units['constants']['required_lifetime_s'];surv=math.exp(-(gammaG+gammahard)*age/hb)
    checks=dict(counts=counts==[48,36,12],positive_charge_gap=M>0,xi1_gap_reconstruction=abs(M/authored['spectrum']['Mcharged_hat_xi1']-1)<1e-10,kappa_below100=Mmax/M<100,integral=abs(integral_ratio-4/15)<1e-15,inclusive_factor=inclusive==512,c7_reconstruction=abs(c7/authored['majorant']['inclusive_c7_effective_upper']-1)<1e-12,hard_width_reconstruction=abs(gammahard/authored['benchmark']['Gamma_hard_upper_GeV']-1)<1e-10,survival_above99=surv>.99)
    out=dict(claim_id='TP04_BOUND_RECONSTRUCTION',checks=checks,charged_counts=counts,Mhat=M,Mmaxhat=Mmax,mass_ratio=Mmax/M,integral_ratio=integral_ratio,inclusive_factor=inclusive,c7=c7,mu_GeV=mu,Mcharged_GeV=Mphys,GammaG_GeV=gammaG,Gammahard_upper_GeV=gammahard,hard_over_Goldstino=gammahard/gammaG,retained_survival=surv,retained_lifetime_s=hb/(gammaG+gammahard),runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Independent matrix/gap and finite arithmetic reconstruction; hard1loopclass plus namedWardpartial, not allorderstotal')
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
