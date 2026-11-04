"""Independent finite controls of the final CC10 local interfaces and benchmarks."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource,decimal
import numpy as np
from scipy.integrate import quad,quad_vec,solve_ivp
from scipy.interpolate import PchipInterpolator
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'reviews/collision_completion_2026_11_04'
sys.path.insert(0,str(BASE/'cascades'))
from angular_exact import AngularExact,exact_events,exponential_moments
from angular_fast import exact_events_fast
sys.path.insert(0,str(BASE/'integration_solver'))
from protocol_holes import QuantumState,implicit_step
from protocol_average import AveragedNumberEvents


def passive_controls():
    old=ROOT/'reviews/coupled_trapping_2026_11_04'
    pole=json.loads((old/'microphysics/run_pole002/result.json').read_text())
    medium=json.loads((old/'microphysics/run_medium001/result.json').read_text())
    stage=json.loads((BASE/'memory/run_stage001/result.json').read_text())
    late=json.loads((old/'kinetics/run_hybrid_bw_001/result.json').read_text())['case'];h=late['history'][-1]
    G=np.array(pole['production_Gram_mu2']);M=pole['Mpole'];mu=late['mu_GeV'];Y=stage['final_Y_charged']
    Tmin=stage['rows'][-1]['Tc']*mu/.02;s=2*np.pi**2*106.75*Tmin**3/45
    H=np.sqrt(np.pi**2*106.75/90)*Tmin*Tmin/2.435e18;gate=.044e-9/(pole['mC']*mu)
    mmin=.0015*math.sqrt(h['x_inner']**2+2/(31*.003));correction=(M/(2*mmin))**2
    rows=[]
    for label,width in [('vacuum',pole['Gamma_other_matrix_mu']),('SSS',medium['Gamma_SSS_matrix_mu'])]:
        width=np.array(width);peak=4*np.trace(np.linalg.solve(width,G))/M**3
        L=s*(peak*correction/mu**2)/(2*H);Z0=Y/gate
        # Integrate the physical scaled yield, rather than its inverse, with
        # w=1-1/a. This is a separate nonlinear differential equation check.
        sol=solve_ivp(lambda w,z:-L*gate*z*z,[0,1],[Z0],rtol=2e-11,atol=1e-11)
        floor=1/(1/Y+L)
        rows.append(dict(width=label,peak=float(peak),floor=floor,floor_over_gate=floor/gate,
                         direct_yield_ODE_relative=abs(sol.y[0,-1]/(floor/gate)-1),
                         required_total_peak_multiplier=(1/gate-1/Y)/L))
    # Noncommuting periodic 3-state equation solved in Fourier space. The
    # output matrix itself varies above a fixed positive lower form bound.
    gamma=np.diag([.4,.8,1.3]);v=np.array([.4+.2j,-.3j,.7]);omega=1.2;N=24;ns=np.arange(-N,N+1)
    A=np.array([[.6,.2j,.1],[-.2j,-.4,.3],[.1,.3,.2]],complex)
    B=np.array([[.1,.2,0],[.2,-.1,.15j],[0,-.15j,.3]],complex)
    D=np.outer([.2,.3,.5],[.2,.3,.5]);C=np.outer([.4,-.1,.2],[.4,-.1,.2])
    H0=A;Hc=B;Hs=A*.3;L0=(gamma+D+C)/2+1j*H0
    Lp=(C*.6/2+D*.4/(2j))/2+1j*(Hc/2+Hs/(2j));Lm=(C*.6/2-D*.4/(2j))/2+1j*(Hc/2-Hs/(2j))
    mat=np.zeros((3*len(ns),3*len(ns)),complex);source=np.zeros(3*len(ns),complex)
    for i,n in enumerate(ns):
        mat[3*i:3*i+3,3*i:3*i+3]=L0+1j*n*omega*np.eye(3)
        if i>0:mat[3*i:3*i+3,3*(i-1):3*i]=Lp
        if i<len(ns)-1:mat[3*i:3*i+3,3*(i+1):3*(i+2)]=Lm
    source[3*N:3*N+3]=v;coeff=np.linalg.solve(mat,source).reshape(-1,3)
    theta=2*np.pi*np.arange(4096)/4096;a=np.exp(1j*theta[:,None]*ns)@coeff
    out=np.array([gamma+D*(1+.4*math.sin(t)) for t in theta]);absorb=np.array([C*(1+.6*math.cos(t)) for t in theta])
    rate=float(np.einsum('ti,tij,tj->',a.conj(),out,a).real/len(theta));loss=float(np.einsum('ti,tij,tj->',a.conj(),absorb,a).real/len(theta))
    current=float(np.mean(2*np.real(a.conj()@v)));bound=float(4*np.vdot(v,np.linalg.solve(gamma,v)).real)
    return dict(tail=rows,mass_correction=correction,noncommuting=dict(rate=rate,bound=bound,ratio=rate/bound,
                identity_relative=abs(rate+loss-current)/bound,Fourier_edge_relative=float(np.linalg.norm(coeff[[0,-1]])/np.linalg.norm(coeff))))


def moment_controls():
    rows=[]
    for B in (-1000.,-80.,-.10001,-.09999,-1e-8,0.,1e-8,.09999,.10001,80.,1000.):
        peak=-.3;A=peak-abs(B);got=exponential_moments(A-B,A+B)
        if abs(B)<20:
            ref=np.array([quad(lambda u:u**k*math.exp(A+B*u),-1,1,epsabs=1e-13,epsrel=1e-12)[0] for k in range(3)])
        else:
            x=abs(B);sign=1 if B>0 else -1
            ref=np.array([math.exp(peak)/x*quad(lambda y:(sign*(1-y/x))**k*math.exp(-y),0,min(2*x,80),epsabs=1e-13,epsrel=1e-12)[0] for k in range(3)])
        rows.append(dict(B=B,relative_scale_error=float(np.max(abs(got-ref))/max(abs(ref)))))
    return rows


def toy_data(duplicate=False):
    groups=[dict(id='P',kind='S',mass=3.,degeneracy=1,charged=False),dict(id='D',kind='F',mass=.4,degeneracy=2,charged=False)]
    if not duplicate:groups.append(dict(id='C',kind='F',mass=.7,degeneracy=2,charged=False))
    return dict(x=1.,groups=groups,channels=[dict(parent='P',daughters=['D','D' if duplicate else 'C'],width=.03,kind='FF')])


def direct_angular_rhs(data,t,q,W,f):
    n=len(q);ng=len(data['groups']);en=np.array([np.sqrt(g['mass']**2+(t*q)**2) for g in data['groups']])
    eta=np.repeat([1 if g['kind']=='S' else -1 for g in data['groups']],n);av=1+eta*f
    measures=np.concatenate([g['degeneracy']*W/(2*np.pi**2) for g in data['groups']]);out=np.zeros(ng*n)
    M=3.;m1=.4;m2=.4 if ng==2 else .7;child2=1 if ng==2 else 2
    estar=(M*M+m1*m1-m2*m2)/(2*M);pstar=math.sqrt((M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2))/(2*M)
    for i,ep in enumerate(en[0]):
        offset=ep*estar/M;slope=t*q[i]*pstar/M;cuts=[]
        if slope:
            cuts.extend(((en[1]-offset)/slope).tolist());cuts.extend(((en[child2]-(ep-offset))/(-slope)).tolist())
        cuts=sorted(set(z for z in cuts if -1<z<1))
        def value(z):
            targets=(offset+slope*z,ep-offset-slope*z);idx=[i];weights=[1.]
            for g,target in zip((1,child2),targets):
                if target<en[g,0] or target>en[g,-1]:return np.zeros(ng*n)
                lo=min(max(int(np.searchsorted(en[g],target)-1),0),n-2);alpha=(target-en[g,lo])/(en[g,lo+1]-en[g,lo]);idx.extend([g*n+lo,g*n+lo+1]);weights.extend([1-alpha,alpha])
            idx=np.array(idx);weights=np.array(weights);F=f[i]*np.prod(av[idx[1:]]**weights[1:]);R=av[i]*np.prod(f[idx[1:]]**weights[1:]);r=np.zeros(ng*n)
            np.add.at(r,idx,np.array([-1,1,1,1,1])*weights*(F-R));return r
        integral=quad_vec(value,-1,1,points=cuts,epsabs=1e-11,epsrel=1e-10)[0]
        out+=measures[i]*.03*M/ep/2*integral
    return out


def angular_protocol_controls():
    q=np.array([0.,.1,.7,1.6,4.,8.]);edges=np.r_[0.,(q[:-1]+q[1:])/2,10.];W=np.diff(edges**3)/3;rows=[]
    for duplicate in (False,True):
        data=toy_data(duplicate);ev=exact_events(data,.6,q,W);fast=exact_events_fast(data,.6,q,W)
        f=.25+.12*np.sin(np.arange(len(ev.measure)));av=1+ev.eta*f;rhs=ev.number_rhs(f,av);ref=direct_angular_rhs(data,.6,q,W,f)
        J=ev.number_jacobian(f,av).toarray();FD=np.empty_like(J);h=2e-6
        for j in range(len(f)):
            fp=f.copy();fm=f.copy();fp[j]+=h;fm[j]-=h
            FD[:,j]=(ev.number_rhs(fp,1+ev.eta*fp)-ev.number_rhs(fm,1+ev.eta*fm))/(2*h*ev.measure[j])
        coord=[]
        for mode in (0,1,2):
            holes=(ev.eta<0)&((np.arange(len(f))+mode)%3!=0);state=QuantumState(ev.measure,ev.eta,Z=np.where(holes,ev.measure*(1-f),ev.measure*f),holes=holes)
            exact=state.jacobian(ev).toarray();fd=np.zeros_like(exact);sign=np.where(holes,-1.,1.)
            for j in range(len(f)):
                step=ev.measure[j]*h;plus=state.copy();minus=state.copy();plus.Z[j]+=step;minus.Z[j]-=step
                fd[:,j]=sign*(plus.rhs(ev)-minus.rhs(ev))/(2*step)
            coord.append(float(np.linalg.norm(exact-fd)/np.linalg.norm(exact)))
        rows.append(dict(duplicate=duplicate,segments=len(ev.coefficient),direct_energy_quadrature_relative=float(np.linalg.norm(rhs-ref)/np.linalg.norm(rhs)),
                         number_Jacobian_relative=float(np.linalg.norm(J-FD)/np.linalg.norm(J)),coordinate_Jacobian_relative=coord,
                         fast_rhs_relative=float(np.linalg.norm(fast.number_rhs(f,av)-rhs)/np.linalg.norm(rhs)),
                         fast_Jacobian_relative=float(np.linalg.norm(fast.number_jacobian(f,av).toarray()-J)/np.linalg.norm(J)),energy_residual=ev.energy_residual))
    # Independent 80-digit scalar-extent backward Euler solve, including a
    # fermion bin so small that its hole cannot be recovered from 1-f.
    tiny=[];decimal.getcontext().prec=80;D=decimal.Decimal
    for m in (1e-12,1e-20,1e-24):
        ev=AngularExact([[0,1,1,2,2]],[[1,1,0,1,0]],[[0]*5],[.5],[2,3,m],[2,1,1],[-1,1,-1])
        state=QuantumState(ev.measure,ev.eta,Y=ev.measure*np.array([.5,1e-30,0.]))
        new,diag=implicit_step(ev,state,1.,tol=2e-10);mm=D(str(m));seed=D('1e-30')
        def residual(h):
            extent=mm*(1-h);p=D('.5')-extent/2;c=seed+extent/3
            return extent-(p*(1+c)*h-(1-p)*c*(1-h))
        lo=D(0);hi=D(1)
        for k in range(260):
            mid=(lo+hi)/2
            if residual(mid)>0:lo=mid
            else:hi=mid
        reference=float((lo+hi)/2);f,a=new.arrays()
        tiny.append(dict(measure=m,hole=float(a[2]),reference_hole=reference,relative=abs(a[2]/reference-1),rounded_f=float(f[2]),newton=diag))
    # A phase average must preserve its local collision energies without
    # treating the average energy as a local collision invariant.
    measure=np.array([2.,3.,4.,5.,6.]);eta=np.array([1.,-1.,-1.,-1.,-1.]);f=np.array([.3,.2,.4,.1,.35]);av=1+eta*f
    e1=AngularExact([[0,1,2,3,4]],[[1,.5,.5,.5,.5]],[[0]*5],[.3],measure,[3,1,2,1,2],eta)
    e2=AngularExact([[0,1,2,3,4]],[[1,.2,.8,.4,.6]],[[0]*5],[.7],measure,[5,1,4,1,2],eta)
    avg=AveragedNumberEvents([e1,e2],[1,2]);explicit=(e1.number_rhs(f,av)+2*e2.number_rhs(f,av))/3
    return dict(angular=rows,stiff_holes=tiny,phase_average=dict(rhs_relative=float(np.linalg.norm(avg.number_rhs(f,av)-explicit)/np.linalg.norm(explicit)),
                local_energy_rates=avg.local_energy_rates(f,av).tolist(),averaged_energy_collision_rate=float(avg.energy@avg.number_rhs(f,av))))


def production_controls():
    r=json.loads((BASE/'production/run001/result.json').read_text());T,gr,_,gs,_=np.loadtxt(BASE/'production/standardmodel2018.dat').T
    c=r['cosmology'];T0=c['Tgamma0_GeV'];hbar=6.582119569e-25;mpl=2.435e18;c_km=299792.458;mpc_km=3.0856775814913673e19;H0=67.4/mpc_km
    aa=T0/T*(gs[0]/gs)**(1/3);order=np.argsort(aa);x=np.log(aa[order]);H=np.sqrt(np.pi**2*gr[order]/90)*T[order]**2/mpl/hbar
    hi=PchipInterpolator(x,np.log(H));Ti=PchipInterpolator(x,np.log(T[order]));OR=(math.sqrt(np.pi**2*gr[0]/90)*T0*T0/mpl/hbar/H0)**2;OL=1-.315-OR
    # Log-time ODE, independent of the production table's cumulative trapezoid.
    sol=solve_ivp(lambda xx,lt:np.exp(-float(hi(xx))-lt),[x[0],x[-1]],[-math.log(2*H[0])],rtol=2e-11,atol=2e-11,max_step=.03,dense_output=True)
    xx=np.linspace(x[0],x[-1],16001);birth=PchipInterpolator(sol.sol(xx)[0],xx)
    def hubble(loga):
        a=math.exp(loga);hr=math.exp(float(hi(loga))) if loga<x[-1] else H0*math.sqrt(OR)/a**2
        return math.sqrt(hr*hr+H0*H0*(.315/a**3+OL))
    def free(logab,R):
        alpha=R*math.exp(logab)
        def integrand(loga):
            a=math.exp(loga);v=alpha/math.hypot(alpha,a)
            return c_km/mpc_km*v/(a*hubble(loga))
        points=[z for z in (math.log(alpha),math.log(OR/.315),x[-1]) if logab<z<0]
        return quad(integrand,logab,0,points=points,epsabs=1e-6,epsrel=2e-8,limit=160)[0]
    rows=[]
    for state,ref in zip(r['states'],r['baseline']):
        R=state['mass']/(2*state['mchi_mu']);width=state['gauge_width_mu']+state['soft_chi_width_mu'];branch=state['soft_chi_width_mu']/width;tau=hbar/(2e6*width)
        def integrand(rr):
            if rr==0:return 0.
            logab=float(birth(math.log(tau*rr*rr)))
            return 2*rr*math.exp(-rr*rr)*free(logab,R)
        mean=quad(integrand,0,math.sqrt(40),epsabs=2e-4,epsrel=3e-6,limit=100)[0]
        medianx=float(birth(math.log(tau*math.log(2))));Tmedian=math.exp(float(Ti(medianx)))
        rows.append(dict(id=state['id'],pstar_over_mchi=R,branch=branch,lifetime=tau,independent_mean_FS_Mpc=mean,
                         pinned_mean_FS_Mpc=ref['mean_free_streaming_kpc']/1000,FS_relative=abs(mean/(ref['mean_free_streaming_kpc']/1000)-1),
                         independent_median_T_GeV=Tmedian,pinned_median_T_GeV=ref['median_decay_temperature_GeV'],median_T_relative=abs(Tmedian/ref['median_decay_temperature_GeV']-1)))
    return dict(states=rows,EOS_source_sha256=__import__('hashlib').sha256((BASE/'production/standardmodel2018.dat').read_bytes()).hexdigest(),clock_ODE_success=bool(sol.success))


def main(out):
    start=time.monotonic();result=dict(passive=passive_controls(),moments=moment_controls(),angular_protocol=angular_protocol_controls(),production=production_controls())
    a=result['angular_protocol'];checks=dict(passive_tail=all(v['direct_yield_ODE_relative']<1e-8 for v in result['passive']['tail']),
        noncommuting_passive=result['passive']['noncommuting']['ratio']<=1 and result['passive']['noncommuting']['identity_relative']<1e-10,
        exponential_moments=max(v['relative_scale_error'] for v in result['moments'])<1e-10,
        direct_angular=max(v['direct_energy_quadrature_relative'] for v in a['angular'])<1e-8,
        angular_jacobian=max(v['number_Jacobian_relative'] for v in a['angular'])<1e-7,
        hole_sign_chain=max(max(v['coordinate_Jacobian_relative']) for v in a['angular'])<1e-7,
        fast_matches=max(v['fast_rhs_relative']+v['fast_Jacobian_relative'] for v in a['angular'])<1e-10,
        stiff_holes=max(v['relative'] for v in a['stiff_holes'])<1e-7,
        phase_local_energies=max(abs(v) for v in a['phase_average']['local_energy_rates'])<1e-12,
        independent_free_streaming=max(v['FS_relative'] for v in result['production']['states'])<.003)
    result['checks']={k:bool(v) for k,v in checks.items()};result['runtime_seconds']=time.monotonic()-start;result['peak_rss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes_macos')}));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
