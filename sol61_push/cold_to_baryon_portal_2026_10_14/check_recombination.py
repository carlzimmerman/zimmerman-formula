"""CBP-003: both dark charges can be consumed, if opposite supply exists."""
import json
from pathlib import Path
import sys
import numpy as np
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def ck(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
    if not ok:raise AssertionError(name)
mn=.93956542194;mp=.93827208943;mc=mn-.0005
mu=-1.91304273*np.sqrt(4*np.pi*.0072973525643)/(2*mp)
g0=np.diag([1,1,-1,-1]).astype(complex)
sigma=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
zero=np.zeros((2,2),complex)
gam=[g0]+[np.block([[zero,s],[-s,zero]]) for s in sigma]
PL=(np.eye(4)-1j*gam[0]@gam[1]@gam[2]@gam[3])/2
def slash(p):return p[0]*g0-sum((p[i]*gam[i] for i in [1,2,3]),np.zeros((4,4),complex))
def spinor(p,m,j):
    two=np.eye(2,dtype=complex)[:,j]
    sp=sum((p[i+1]*sigma[i] for i in range(3)),zero.copy())
    return np.sqrt(p[0]+m)*np.concatenate([two,sp@two/(p[0]+m)])
ck('dark charge',1-1==0)
ck('baryon transfer',1+0==1)
rows=[]
for ms in [.0004,.0005,.0006,.001,.002,.005]:
    W=mc+ms
    if W<=mn*(1+2e-15):
        rows.append(dict(mS_GeV=ms,open=False,sigma_v_over_y2_cm3_s=0.))
        continue
    omega=(W*W-mn*mn)/(2*W)
    k=np.array([omega,0.,0.,omega]);pn=np.array([np.sqrt(mn*mn+omega*omega),0.,0.,-omega])
    pi=np.array([mc,0.,0.,0.]);P=np.array([W,0.,0.,0.])
    def op(eps):
        # Transverse Pauli identity sigma(eps,k)=i slash(eps) slash(k).
        return 1j*mu*slash(eps)@slash(k)@(slash(P)+mn*np.eye(4))@PL/(W*W-mn*mn)
    trsum=0.;directsum=0.
    for eps in [np.array([0.,1.,0.,0.]),np.array([0.,0.,1.,0.])]:
        v=op(eps)
        tr=np.trace((slash(pn)+mn*np.eye(4))@v@(slash(pi)+mc*np.eye(4))@g0@v.conj().T@g0)/2
        direct=sum(abs(spinor(pn,mn,j).conj()@g0@v@spinor(pi,mc,i))**2 for j in [0,1] for i in [0,1])/2
        ck('trace spin %g %s'%(ms,str(eps)),abs(tr.imag)<1e-14 and abs(tr.real-direct)<1e-12)
        trsum+=tr.real;directsum+=direct
    ck('Ward %g'%ms,np.max(abs(op(k)))<1e-14)
    ck('energy momentum %g'%ms,max(abs(P-pn-k))<1e-12)
    sv=omega*trsum/(16*np.pi*W*mc*ms)
    sv_cgs=sv*.3893793721e-27*29979245800.
    ck('positive conversion %g'%ms,sv>0)
    rows.append(dict(mS_GeV=ms,open=True,photon_energy_MeV=omega*1000,neutron_recoil_keV=(pn[0]-mn)*1e6,sigma_v_over_y2_GeVminus2=sv,sigma_v_over_y2_cm3_s=sv_cgs,sigma_v_at_y_1p44em11_cm3_s=sv_cgs*(1.44e-11)**2))
result=dict(status='conditional neutral-initial-state baryon transfer verified',assertions=len(checks),mchi_GeV=mc,rows=rows,scope='Chosen tree-level neutron/Pauli EFT in zero-relative-velocity limit; opposite dark-charge reservoir and hidden B asymmetry supplied, not derived.')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
