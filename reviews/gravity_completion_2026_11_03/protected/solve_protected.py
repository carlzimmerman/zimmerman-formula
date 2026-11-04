"""Neutral SU5 SUGRA tree plus full rigid CW valley, explicit accuracy contract."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import mpmath as mp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from pressure_scan import cw
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize

mp.mp.dps=80
E=mp.mpf('.003');EPS=mp.mpf('.0001');NEXP=3-EPS;BC=mp.mpf('1e8')
MU=mp.mpf('18170662.111498855');M=mp.mpf('2.435e18')/MU;ALPHA=1/M
F=1/mp.sqrt(31);AA=mp.sqrt(mp.mpf(30)/31);KK=E*mp.sqrt(mp.mpf(31)/30)
Q0=mp.sqrt(60/(31*E));Z=mp.mpf('7.3671437212785083116194');R0=Z/mp.sqrt(E)
WBASE=M*F/mp.sqrt(EPS)
G=mp.sqrt(mp.mpf(29)/200)*E


def data(tau,z,w):
    ss=tau+mp.conj(tau);dd=tau-mp.conj(tau)
    H=ss+BC*(ss-1)**4+BC*dd**4
    P=1+4*BC*(ss-1)**3+4*BC*dd**3
    Pb=mp.conj(P);QH=12*BC*((ss-1)**2-dd**2)
    Htt=12*BC*((ss-1)**2+dd**2)
    Httb=24*BC*((ss-1)-dd)
    Y=H-sum(abs(v)**2 for v in z)/(NEXP*M*M)
    T,N,q=z # q=-i A_D: all three real on this CP slice.
    W=F*T+AA*N-KK*N*q*q/2+WBASE*w
    Wi=mp.matrix([F,AA-KK*q*q/2,-KK*N*q])
    S=sum(z[i]*Wi[i] for i in range(3));F0=sum(abs(v)**2 for v in Wi)
    DH=abs(P)**2-H*QH
    V=Y**(-NEXP)*(Y*F0-EPS*abs(W)**2/(M*M)+Y*QH*abs(S-NEXP*W)**2/(NEXP*DH*M*M))
    return dict(H=H,P=P,Pb=Pb,QH=QH,Htt=Htt,Httb=Httb,Y=Y,W=W,Wi=Wi,S=S,F0=F0,DH=DH,V=mp.re(V))


def ucw(tau,z,w):
    d=data(tau,z,w);Y=mp.re(d['Y'])
    # Local canonical matter at small z/M: e_phys=e Y^(eps/2),
    # mu_phys^4=mu^4 Y^(1-n), X_phys/mu_phys=X Y^(-eps/4).
    # This retains the exact rigid finite splittings, not SUGRA soft splittings.
    ee=E*Y**(EPS/2)
    xx=abs(z[0])/mp.sqrt(31)*Y**(-EPS/4)
    return Y**(1-NEXP)*cw(xx,ee,ee,G)


def unpack(t,uu,qq,ds,ww):
    return mp.mpf('.5')+EPS/BC*ds/2, [R0*t,ALPHA*uu,Q0*(1+ALPHA**2*qq)],ww


def vscaled(t,uu,qq,ds,ww):
    tau,z,w=unpack(t,uu,qq,ds,ww)
    return data(tau,z,w)['V']+ucw(tau,z,w)


def equations(*args):
    val=vscaled(*args)
    ds=[mp.diff(lambda x:vscaled(*(list(args[:i])+[x]+list(args[i+1:]))),args[i]) for i in range(4)]
    return ds[0]/E**2,ds[1]/ALPHA**2,ds[2]/ALPHA**4,ds[3]/(EPS/BC),val


def neutral_matrices(tau,z,w):
    d=data(tau,z,w);Y=d['Y'];P=d['P'];QH=d['QH'];W=d['W']
    yi=mp.matrix([P/M]+[-mp.conj(v)/(NEXP*M*M) for v in z])
    yb=yi.conjugate();yib=mp.zeros(4);yib[0,0]=QH/(M*M)
    yhol=mp.zeros(4);yhol[0,0]=d['Htt']/(M*M)
    for i in range(1,4):yib[i,i]=-1/(NEXP*M*M)
    ki=-NEXP*M*M/Y*yi
    metric=-NEXP*M*M*(yib/Y-yi*yb.T/Y**2)
    khol=-NEXP*M*M*(yhol/Y-yi*yi.T/Y**2)
    metricinv=metric**-1
    wi=mp.matrix([0]+list(d['Wi']))
    wij=mp.zeros(4);wij[2,3]=wij[3,2]=-KK*z[2];wij[3,3]=-KK*z[1]
    Di=wi+ki*W/(M*M);ek=Y**(-NEXP/2)
    raw=mp.zeros(4)
    for i in range(4):
        for j in range(4):
            dg=mp.matrix([0]*4)
            for k in range(4):
                third=d['Httb']/M**3 if i==j==k==0 else 0
                dg[k]=-NEXP*M*M*(third/Y-(yib[j,k]*yi[i]+yhol[i,j]*yb[k]+yi[j]*yib[i,k])/Y**2+2*yi[j]*yb[k]*yi[i]/Y**3)
            gamma=metricinv.T*dg
            raw[i,j]=ek*(wij[i,j]+(ki[i]*wi[j]+ki[j]*wi[i]+khol[i,j]*W)/(M*M)+ki[i]*ki[j]*W/M**4-sum(gamma[k]*Di[k] for k in range(4)))
    vals,O=mp.eigsy(metric.apply(mp.re));C=O*mp.diag([1/mp.sqrt(v) for v in vals])*O.T
    aux=ek*metricinv.T*Di.conjugate()
    gold=C.T*Di
    gold=gold/mp.sqrt(sum(v*v for v in gold))
    # Independent exact scalar gradient/tree mass Ward identity at this point.
    def tree_real(i,x):
        tt=tau;zz=list(z)
        if i==0:tt+=x/M
        else:zz[i-1]+=x
        return data(tt,zz,w)['V']
    grads=mp.matrix([mp.diff(lambda x:tree_real(i,x),0)/2 for i in range(4)])
    ward=raw*aux-2*(ek*W/M**2)*ek*Di
    ward_error=max(abs(ward[i]-grads[i]) for i in range(4))
    # Required rigid current correction: scalar one-loop stationarity fixes the
    # TT zero-momentum self-energy. Modulus cross-loop matching is not claimed.
    def loop_real(i,x):
        tt=tau;zz=list(z)
        if i==0:tt+=x/M
        else:zz[i-1]+=x
        return ucw(tt,zz,w)
    loopgrad=mp.matrix([mp.diff(lambda x:loop_real(i,x),0)/2 for i in range(4)])
    completed=raw.copy();completed[1,1]+=loopgrad[1]/aux[1]
    # Do not infer physical poles from an off-shell tree null eigenvalue.
    # Project proper K-normalized Goldstino kernel directly.
    basis=[]
    for j in (1,2,3,0):
        v=mp.matrix([int(i==j) for i in range(4)])-gold*gold[j]
        for b in basis:v-=b*(b.T*v)[0]
        norm=mp.sqrt(sum(a*a for a in v))
        if norm>mp.mpf('1e-30'):basis.append(v/norm)
        if len(basis)==3:break
    B=mp.matrix([[basis[j][i] for j in range(3)] for i in range(4)])
    treeproj=B.T*C.T*raw*C*B
    poleproj=B.T*C.T*completed*C*B
    mt,Ot=mp.eigsy(treeproj);mf,Of=mp.eigsy(poleproj)
    imin=min(range(3),key=lambda j:abs(mf[j]));orth=B*Of[:,imin]
    # Local canonically normalized matter current direction is T to accuracy
    # O(z/M). Report the measured overlap and its asymptotic control.
    matter=mp.matrix([0,1,0,0]);matter-=gold*(gold.T*matter)[0]
    matter=mp.sqrt(sum(v*v for v in matter))
    # Scalar Hessian: real increments lack 1/sqrt(2), hence mass^2=H/2.
    def shifted(*r):
        tt=tau+(r[0]+1j*r[4])/M
        zz=[z[j]+r[j+1]+1j*r[j+5] for j in range(3)]
        return data(tt,zz,w)['V']+ucw(tt,zz,w)
    hess=mp.zeros(8)
    for i in range(8):
        for j in range(i,8):
            orders=[0]*8;orders[i]+=1;orders[j]+=1
            hess[i,j]=hess[j,i]=mp.diff(shifted,[0]*8,orders)/2
    CR=mp.zeros(8)
    for i in range(4):
        for j in range(4):CR[i,j]=CR[i+4,j+4]=C[i,j]
    hs=CR.T*hess*CR;ms,Os=mp.eigsy(hs.apply(mp.re))
    # Solve all raw physical gradients separately, so a scaled root cannot hide
    # a nonstationary imaginary direction.
    allgrad=[mp.diff(lambda x:shifted(*([0]*i+[x]+[0]*(7-i))),0)/2 for i in range(8)]
    return dict(metric_eigenvalues=list(vals),raw=raw,canonical=C,gold=gold,
                raw_ward_error=ward_error,tree_projected_masses=list(mt),
                ward_completed_projected_masses=list(mf),orth=orth,
                current_matter_projection=orth[1],expected_current_projection=mp.sqrt(NEXP/3),
                loop_TT=loopgrad[1]/aux[1],loop_modulus_force=loopgrad[0],
                scalar_masses2=list(ms),all_gradient=list(allgrad),
                full_stationary_ward_mismatch=list(completed*aux-2*(ek*W/M**2)*ek*Di),
                auxiliary=aux)


def main(out):
    start=time.monotonic()
    root=mp.findroot(equations,(mp.mpf('1.027'),0,0,-1/(24*NEXP),1),tol=mp.mpf('1e-60'),maxsteps=25)
    tau,z,w=unpack(*root);d=data(tau,z,w)
    eqres=equations(*root);res=neutral_matrices(tau,z,w)
    m32=d['Y']**(-NEXP/2)*d['W']/M**2*MU
    zeta=min(abs(v) for v in res['ward_completed_projected_masses'])*MU
    x=float(z[0]/mp.sqrt(31));dd=build_model(x,float(E),float(E),float(G),vertices=False)
    ext,labels=ext_basis(dd);groups,_=summarize(threshold(dd,ext),labels)
    mchi=MU*abs(groups['U1']['signed_mass'])
    Fphys=MU**2/mp.sqrt(31)
    projection=abs(res['current_matter_projection'])
    width=projection**2*mchi**5/(16*mp.pi*Fphys**2)*(1-(zeta/mchi)**2)**3
    hbar=mp.mpf('6.582119569e-25');life=hbar/width
    rho_ratio=mp.mpf('1.396e74')
    checks=dict(root_residual=max(abs(v) for v in eqres)<mp.mpf('1e-45'),
                K_positive=min(res['metric_eigenvalues'])>0 and d['Y']>0 and d['DH']>0,
                neutral_scalar_positive=min(res['scalar_masses2'])>0,
                complex_tree_Ward_identity=res['raw_ward_error']<mp.mpf('1e-60'),
                orthogonal_fermion_lighter_than_photino=zeta<mchi,
                current_not_Ftotal_suppressed=abs(projection-mp.sqrt(NEXP/3))<mp.mpf('1e-5'),
                leading_mass_matches_epsilon_over_n=abs(zeta/(EPS/NEXP*m32)-1)<mp.mpf('.001'),
                photino_partial_lifetime_exceeds_age=life>mp.mpf('4.354e17'))
    result=dict(claim_id='PG06_PROTECTED_LOCAL',checks={k:bool(v) for k,v in checks.items()},
                inputs=dict(e=float(E),epsilon=float(EPS),b=float(BC),c=float(BC),mu_GeV=float(MU),M_GeV=2.435e18),
                root=[str(v) for v in root],stationary_point=dict(T_GeV=str(z[0]*MU),N_GeV=str(z[1]*MU),Q_real_GeV=str(z[2]*MU),tau_real=str(tau),W0_GeV3=str(WBASE*w*MU**3)),
                stationarity=dict(scaled_equations=[str(v) for v in eqres],physical_complex_gradients_mu3=[str(v) for v in res['all_gradient']],net_V_over_mu4=str(vscaled(*root))),
                geometry=dict(Y=str(d['Y']),DH=str(d['DH']),metric_eigenvalues=[str(v) for v in res['metric_eigenvalues']]),
                spectrum=dict(m32_GeV=float(m32),neutral_scalar_masses_GeV=[float(mp.sqrt(v)*MU) for v in res['scalar_masses2']],tree_projected_neutral_fermions_GeV=[float(v*MU) for v in res['tree_projected_masses']],stationary_Ward_completed_fermions_GeV=[float(abs(v)*MU) for v in res['ward_completed_projected_masses']],zeta_GeV=float(zeta),photino_GeV=float(mchi),gauginos_GeV={k:float(MU*abs(v['signed_mass'])) for k,v in groups.items()}),
                goldstino=dict(canonical_components=[float(v) for v in res['gold']],orthogonal_components=[float(v) for v in res['orth']],orthogonal_matter_current_projection=float(projection),F_hidden_GeV2=float(Fphys),F_total_leading_GeV2=float(mp.sqrt(3)*m32*mp.mpf('2.435e18')),raw_tree_Ward_error=str(res['raw_ward_error']),loop_TT_GeV=float(res['loop_TT']*MU),remaining_modulus_loop_force_mu3=str(res['loop_modulus_force'])),
                decay=dict(channel='photino -> photon + uneaten neutral fermion',width_GeV=float(width),partial_lifetime_seconds=float(life),partial_survival_one_age=float(mp.exp(-mp.mpf('4.354e17')/life)),dipole_coefficient_GeV_minus1=float(projection*mchi/(mp.sqrt(2)*Fphys))),
                EFT=dict(quartic_geometric_scale_GeV=float(mp.mpf('2.435e18')/mp.sqrt(BC)),modulus_mass_over_geometric_scale=float(max(mp.sqrt(v)*MU for v in res['scalar_masses2'] if v<mp.mpf('1e-5'))/(mp.mpf('2.435e18')/mp.sqrt(BC)))),
                tuning=dict(raw_F2_over_rhoDE=float(rho_ratio),fractional_W0_precision_for_DE=float(1/(2*rho_ratio)),meaning='Numerically tuned Minkowski at stated accuracy; DE residual is a further prescribed W0 perturbation, not calculated at 80-digit precision.'),
                runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                accuracy='Exact neutral tree SUGRA plus full rigid finite-CW on collective valley; canonicalized neutral Hessian; leading stationary rigid Ward self-energy. Not a matched finite-SUGRA one-loop spectrum.',
                non_claims=['No finite SUGRA CW/current/anomaly threshold matching','No transverse one-loop stationarity or pole theorem','No all-orders total photino loss bound in gravity','No derived rho_DE, V3 action or kappa'])
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
