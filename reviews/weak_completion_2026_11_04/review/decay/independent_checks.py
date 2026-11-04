"""Independent finite checks of CC11 decay leaves; no source modifications."""
import os, sys, math, json, resource, time
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import beta, gamma
ROOT = Path(__file__).resolve().parents[4]
DEC = ROOT/'reviews/weak_completion_2026_11_04/decay'
sys.path.insert(0, str(DEC))
import matching as author

def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)

def clifford_checks():
    sig = [np.array([[0,1],[1,0]],complex), np.array([[0,-1j],[1j,0]]), np.diag([1.,-1.])]
    eye=np.eye(2); zero=np.zeros((2,2))
    gam=[np.block([[zero,eye],[eye,zero]])]
    gam += [np.block([[zero,s],[-s,zero]]) for s in sig]
    met=np.array([1.,-1.,-1.,-1.])
    def slash(v): return sum(m*g*x for m,g,x in zip(met,gam,v))
    def dot(a,b): return float(np.dot(a*met,b))
    rows=[]
    for E,k in ((.5,[.31,.27,-.42,.19]),(1.3,[-.7,.12,.91,-1.7]),(.7,[1.5,-.8,.6,.2])):
        p1=np.array([E,0.,0.,E]);p2=np.array([E,0.,0.,-E]);k=np.array(k)
        kt=k+p1;kb=k-p2;ds=k+2*p1+p2;dv=k-p1-2*p2
        s=2*dot(p1,p2);u=dot(k,k);v=2*dot(k,p1);w=2*dot(k,p2)
        def project(X): return np.trace(slash(p1)@X@slash(p2))/np.trace(slash(p1)@slash(p2))
        computed={
          'FFS_kinetic':project(slash(kt)@slash(kb)),
          'FFV_transverse':project(sum(m*g@slash(kt)@slash(kb)@g for m,g in zip(met,gam))),
          'FFV_longitudinal':project(slash(k)@slash(kt)@slash(kb)@slash(k)),
          # Two vertex/current orientation signs give the displayed FSV chain.
          # Both mixed bridge fermions carry -k, never +k.
          'FSV_transverse':project(-slash(-k)@slash(ds)),
          'FVS_transverse':project(slash(dv)@slash(-k)),
          'FSV_longitudinal':-dot(ds,kb)*project(slash(-k)@slash(kb)),
          'FVS_longitudinal':dot(dv,kt)*project(slash(kt)@slash(-k)),
          'FVV_one_top':dot(kt,kt),
          'FVV_one_bottom':dot(kb,kb),
          'FVV_both':dot(kt,kb)*project(slash(kt)@slash(kb))}
        expected=dict(FFS_kinetic=u,FFV_transverse=4*(u+(v-w-s)/2),
          FFV_longitudinal=u*u+u*v-u*w-v*w,FSV_transverse=u+2*v,FVS_transverse=-u+2*w,
          FSV_longitudinal=u*u+u*v-s*u,FVS_longitudinal=-u*u+u*w+s*u,
          FVV_one_top=u+v,FVV_one_bottom=u-w,FVV_both=u*u+(u*v-u*w-s*u)/2)
        errors={key:abs(computed[key]-val)/max(1.,abs(val)) for key,val in expected.items()}
        g5=1j*gam[0]@gam[1]@gam[2]@gam[3];PL=(np.eye(4)-g5)/2;PR=(np.eye(4)+g5)/2
        spin=(np.trace(slash(p1)@PL@slash(p2)@PR)+np.trace(slash(p1)@PR@slash(p2)@PL)).real
        rows.append(dict(E=E,k=k.tolist(),numerator_scaled_errors=errors,
            spin_sum_over_s=spin/s,mixed_width_over_M_y2=spin/s/(16*math.pi)))
    return rows

def manual_messenger():
    # Original charge basis, not the author's component builder or eigensystem.
    X,lam,g,mx=1.,.7,.2,.3;m=lam*X
    U=np.array([[1.,1j],[1.,-1j]])/math.sqrt(2)
    # Four canonical real scalars: qPhi,qPhibar,pPhi,pPhibar.
    ye=np.array([[g,0.,-1j*g,0.],[0.,-g,0.,1j*g]],complex)
    ym=U.T@ye; yp=U.T@np.array([[0,lam/math.sqrt(2)],[lam/math.sqrt(2),0]])@U
    cp=np.eye(4)*math.sqrt(2)*lam*lam*X
    cp[0,1]=cp[1,0]=mx*lam/math.sqrt(2)
    cp[2,3]=cp[3,2]=-mx*lam/math.sqrt(2)
    A=np.einsum('is,js,ij->',ym.conj(),ym.conj(),yp)
    B=m*m*np.einsum('is,js,ij->',ym.conj(),ym.conj(),yp.conj())
    C=m*np.einsum('st,is,it->',cp,ym.conj(),ym.conj())
    rows=[]
    for s in (0.,mx*mx,.49,1.5):
        # One-dimensional logarithmic C0, orthogonal to tensor moment quadrature.
        C0=-1/(2*m*m) if not s else quad(lambda x:math.log1p(-s*x*(1-x)/(m*m))/(s*x),0,1,epsabs=2e-13,epsrel=2e-13)[0]
        value=-(C*C0).conjugate()/(16*math.pi**2)
        tau=s/(4*m*m);ff=math.asin(math.sqrt(tau))**2/tau if s else 1.
        target=-math.sqrt(2)*g*g*mx/(16*math.pi**2*X)*ff
        src0=author.moments(s,m*m,m*m,m*m,n=96)['one']
        rows.append(dict(s=s,C0_adaptive=C0,C0_author=src0,C0_relative_error=rel(C0,src0),
            amplitude=[value.real,value.imag],closed_form=target,relative_error=rel(value,target)))
    return dict(FFS_A=[A.real,A.imag],FFS_B=[B.real,B.imag],FSS_C=[C.real,C.imag],
        expected_C=-2*math.sqrt(2)*g*g*mx*lam*lam*X,rows=rows,
        scope='Complete messenger FFS coefficients vanish; this is not a relative FFS/FSS sign benchmark.')

def radial_moments():
    # Wick-rotated radial integral and SO(4) angular average. The source uses
    # pretabulated Minkowski tensors plus product Gauss-Legendre quadrature.
    s,mt,mb,mr=.17,.8,1.1,.7;power=(2,2,1);D=sum(power)
    def radial(x,y,key):
        z=1-x-y;den=x*mt+y*mb+z*mr-x*y*s;u=-x*y*s;v=y*s;w=-x*s
        pref=(-1)**D*gamma(D)*x*y
        r0=beta(2,D-2)*den**(2-D)
        r1=beta(3,D-3)*den**(3-D)
        r2=beta(4,D-4)*den**(4-D)
        values=dict(one=r0,u=u*r0-r1,v=v*r0,w=w*r0,
          uu=u*u*r0-3*u*r1+r2,uv=u*v*r0-1.5*v*r1,
          uw=u*w*r0-1.5*w*r1,vw=v*w*r0-s*r1/2)
        return pref*values[key]
    source=author.moments(s,mt,mb,mr,power,n=48)
    rows=[]
    for key in source:
        value=quad(lambda x:quad(lambda y:radial(x,y,key),0,1-x,epsabs=2e-12,epsrel=2e-12)[0],0,1,epsabs=2e-12,epsrel=2e-12)[0]
        rows.append(dict(moment=key,radial_adaptive=value,source=source[key],relative_error=rel(value,source[key])))
    return dict(parameters=dict(s=s,mt=mt,mb=mb,mr=mr,power=power),rows=rows)

def actual_packet():
    data=author.model();d=data['d'];T=author.T
    # Read transpose parity by direct matrix equality, not the recorded eta trace.
    eta=np.array([1. if np.max(abs(t.T-t))<1e-14 else -1. for t in T])
    cc=np.r_[1.,eta,eta];cf=np.r_[cc,-eta]
    gold=np.r_[d['F'].conj(),np.zeros(24)];gold/=np.linalg.norm(gold)
    rz=np.einsum('aij,j->ai',d['R'],d['z'])
    tangent=np.sqrt(2)*np.concatenate([-rz.imag.T,rz.real.T],axis=0)
    Q,sv,_=np.linalg.svd(tangent,full_matrices=False);rank=int(sum(sv>1e-10));Pg=Q[:,:rank]@Q[:,:rank].T
    Os=data['O'][:,data['gold']];Psource=Os@Os.T
    zero=data['O'][:,d['mS2']==0];Pzero=zero@zero.T
    symmetry=dict(transpose_parity_error=float(max(np.max(abs(t.T-e*t)) for t,e in zip(T,eta))),
      Goldstino_even=float(np.max(abs(cf*gold-gold))),
      gold_projector_error=float(np.max(abs(Pg-Psource))),
      physical_flat_scalar_rank=float(np.trace(Pzero-Pg)),
      gold_and_physical_overlap=float(np.max(abs(Pg@(Pzero-Pg)))))
    # Independent fundamental SU(3) d tensor, all ordered daughter colors.
    tf=author.fundamental_basis();dd=np.array([[[2*np.trace((a@b+b@a)@c).real for c in tf[:8]] for b in tf[:8]] for a in tf[:8]])
    dnorm=np.sum(dd*dd,axis=(1,2));symmetry['SU3_d_norm_error']=float(np.max(abs(dnorm-5/3)))
    rows=[]
    for name in ('S8_0','S3_0'):
        p=author.parent(data,name);ts=author.coefficients(data,p);base=sum(author.amplitude(data,p,ts).values())
        # This is a convention-covariance discriminator: external undaggered
        # mass coefficients must transform with +i(theta_a+theta_b).
        angles=np.linspace(-.43,.61,12);phase=np.exp(1j*angles)
        alt=dict(data,Y=data['Y']*phase[:,None,None],G=data['G']*phase.conj()[None,:,None])
        phased=sum(author.amplitude(alt,p,author.coefficients(alt,p)).values())
        expected=base*phase[p['b']]*phase[11]
        allamp=sum(author.amplitude(data,p,author.coefficients(data,p,charged_only=False)).values())
        Ftree=np.einsum('IJa,a->IJ',data['dy'],p['weights'])
        parentcc=np.r_[cc,cc]*p['weights'];parentparity=float(np.dot(parentcc,p['weights']))
        lamvec=data['ext'][:,p['b']];lamparity=complex(np.vdot(lamvec,cf*lamvec))
        # Enumerate every actually open physical tree FFS/SSS channel.
        yp=p['yp'];openf=d['mF'][:,None]+d['mF'][None,:]<p['mass']*(1-1e-10)
        mS=np.sqrt(np.maximum(d['mS2'],0));physical=~data['gold']
        opens=(mS[:,None]+mS[None,:]<p['mass']*(1-1e-10))&physical[:,None]&physical[None,:]
        rows.append(dict(id=name,amplitude=[base.real,base.imag],width=p['mass']*abs(base)**2/(8*math.pi),
          external_phase_relative_error=rel(phased,expected),all_vs_charged_relative_error=rel(allamp,base),
          tree_chi_vertex_norm=float(np.linalg.norm(Ftree@data['ext'][:,11])),
          tree_Goldstino_vertex=float(abs(lamvec.T@Ftree@gold)),parent_C_parity=parentparity,
          lambda_C_parity=[lamparity.real,lamparity.imag],
          max_open_tree_FFS=float(np.max(abs(yp[openf]))),max_open_tree_SSS=float(np.max(abs(p['cp'][opens]))),
          physical_open_FFS_pairs=int(sum(openf.flat)),physical_open_SSS_pairs=int(sum(opens.flat))))
    # The old G G mass formula has the opposite external rephasing weight.
    G=np.array([[.2+.3j,.4-.1j],[-.1+.6j,.7+.2j]])
    phases=np.exp(1j*np.array([.32,-.71]));mass=np.diag([.6,1.3])
    correct=G.conj()@mass@G.conj().T;newG=phases.conj()[:,None]*G
    newcorrect=newG.conj()@mass@newG.conj().T
    wrong=G@mass@G.T;newwrong=newG@mass@newG.T
    expected=phases[:,None]*phases[None,:]
    orientation=dict(correct_covariance_error=float(np.max(abs(newcorrect-expected*correct))),
        historical_covariance_error=float(np.max(abs(newwrong-expected*wrong))))
    return dict(symmetry=symmetry,states=rows,orientation=orientation)

def source_ledger():
    result=json.loads((DEC/'run_production002/result.json').read_text());rows=[]
    masses=result['masses_GeV']
    for state in result['sources']:
        name=state['id'];M=state['parent_mass_GeV'];energy=number=chi=partner=0.
        for co in result['cohorts']:
            if co['parent']!=name:continue
            weights=np.asarray(co['probability_weights_per_parent']);ab=np.asarray(co['birth_scale_factor']);q=np.asarray(co['comoving_momentum_GeV'])
            Es=np.sqrt(co['mass_GeV']**2+(q/ab)**2)
            energy+=float(np.dot(weights,Es));number+=float(sum(weights))
            if co['daughter']=='chi':chi+=float(sum(weights))
            if co['daughter'].startswith('lambda'):partner+=float(sum(weights))
        rows.append(dict(id=name,birth_energy_over_M=energy/M,total_daughter_number=number,
          chi_number=chi,expected_chi=state['chi_partner_branch'],partner_number=partner,
          expected_partner=state['partner_number_per_parent'],branch_sum=sum(c['branch'] for c in state['channels']),
          energy_fraction_sum=sum(state['birth_energy_fractions'].values())))
    return rows

def main(out):
    start=time.monotonic()
    result=dict(clifford=clifford_checks(),messenger=manual_messenger(),moments=radial_moments(),actual=actual_packet(),ledger=source_ledger())
    checks=dict(clifford=max(max(r['numerator_scaled_errors'].values()) for r in result['clifford'])<1e-12,
      width_spin=max(abs(r['spin_sum_over_s']-2) for r in result['clifford'])<1e-12,
      messenger=max(r['relative_error'] for r in result['messenger']['rows'])<1e-12,
      scalar_C0=max(r['C0_relative_error'] for r in result['messenger']['rows'])<1e-10,
      radial_tensor=max(r['relative_error'] for r in result['moments']['rows'])<1e-10,
      gold_projector=result['actual']['symmetry']['gold_projector_error']<1e-10,
      actual_phase=max(r['external_phase_relative_error'] for r in result['actual']['states'])<1e-10,
      charged_coverage=max(r['all_vs_charged_relative_error'] for r in result['actual']['states'])<1e-10,
      tree_open=max(max(r['max_open_tree_FFS'],r['max_open_tree_SSS']) for r in result['actual']['states'])<1e-12,
      cohort_energy=max(abs(r['birth_energy_over_M']-1) for r in result['ledger'])<1e-12,
      cohort_number=max(abs(r['total_daughter_number']-2) for r in result['ledger'])<1e-12)
    result.update(checks={k:bool(v) for k,v in checks.items()},runtime_seconds=time.monotonic()-start,
      peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      scope='Independent critical algebra/normalization/tensor/cohort leaves plus source covariance checks; not a separate six-diagram generator or all-parameter proof.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes_macos')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
