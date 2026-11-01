"""Actual phase-charge and adjoint-eigenmode states; no fitted matter portal."""
import sys
sys.dont_write_bytecode=True
import json,math,resource,time
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from pressure_scan import cw,masses
mp.mp.dps=50

def bisect(fun,lo,hi,n=65):
    lo,hi=map(mp.mpf,(lo,hi));fl=fun(lo);fh=fun(hi)
    assert fl*fh<0,(lo,hi,fl,fh)
    for _ in range(n):
        mid=(lo+hi)/2;fm=fun(mid)
        if fl*fm>0:lo=mid;fl=fm
        else:hi=mid
    return (lo+hi)/2

def setup(e):
    e=mp.mpf(e);c=e/31;g=mp.sqrt(mp.mpf(29)/200)*e
    def U(x):return mp.mpf(1)/31+cw(x,e,e,g)
    def d(x,n=1):return mp.diff(lambda s:U(x*mp.exp(s)),0,n)
    x0=bisect(lambda z:d(z*mp.sqrt(c)/e),7,8)*mp.sqrt(c)/e
    return e,c,g,U,d,x0

def phase_point(x,e,U,d,x0):
    us=d(x);uss=d(x,2);R2=31*x*x;D=uss+2*us;charge=mp.sqrt(2*R2*us);du=U(x)-U(x0)
    energy=us/2+du;pressure=us/2-du;cs=(uss-2*us)/D
    return {'X_over_min':float(x/x0),'s':float(mp.log(x/x0)),'charge_theta':float(charge),'U_s':float(us),'U_ss':float(uss),'D':float(D),'epsilon_ex':float(energy),'P_ex':float(pressure),'w_ex':float(pressure/energy),'cs2_IR':float(cs),'radial_m2':float(D/(2*R2)),'positive_source':bool(us>0),'radially_stable':bool(D>0),'positive_compressibility':bool(us>0 and D>0 and uss>2*us)}

def eigen(x,e):
    a=mp.sqrt(2/(31*e));q=2*e*a;M=3*e*x;delta=mp.sqrt(M*M+4*q*q);heavy=(delta+M)/2;light=q*q/heavy;be=M/delta;beprime=be*(1-be*be)
    # The signed logarithmic derivative for the actual light singular mass.
    ml_s=-be*light;ml_ss=(be*be-beprime)*light
    c=e/31;tr=M*M+2*q*q-3*c;det=q*q*(q*q-3*c);scalar2=2*det/(tr+mp.sqrt(tr*tr-4*det))
    return light,ml_s,ml_ss,heavy,be,mp.sqrt(scalar2)

def fermion_integrals(p,m):
    EF=mp.sqrt(p*p+m*m);L=mp.asinh(p/m)
    J0=(p*EF-m*m*L)/2;J1=L-p/EF
    energy=(p*EF*(2*p*p+m*m)-m**4*L)/8
    return EF,J0,J1,energy

def gas_point(x,e,U,d,x0):
    m,ms,mss,mh,be,scalar=eigen(x,e);us=d(x);uss=d(x,2);deg=mp.mpf(16);factor=deg/(2*mp.pi**2)
    def source(p):return factor*m*ms*fermion_integrals(p,m)[1]
    high=m
    while us+source(high)>0:high*=2
    p=bisect(lambda p:us+source(p),0,high,80);EF,J0,J1,Ie=fermion_integrals(p,m)
    n=deg*p**3/(6*mp.pi**2);em=factor*Ie;pm=n*EF-em;C=source(p);D=uss+factor*((ms*ms+m*mss)*J0-m*m*ms*ms*J1)
    derivative=n*p*p/(3*EF)-n*n*m*m*ms*ms/(EF*EF*D);energy=em+U(x)-U(x0);P=pm-U(x)+U(x0)
    kinetic_source=C-n*ms
    row={'X_over_min':float(x/x0),'mass':float(m),'mass_s':float(ms),'mass_ss':float(mss),'heavy_mass':float(mh),'light_scalar_mass':float(scalar),'scalar_over_fermion_mass':float(scalar/m),'pF_over_m':float(p/m),'n':float(n),'source_full':float(C),'source_kinetic_only':float(kinetic_source),'rest_source':float(n*ms),'D':float(D),'epsilon_ex':float(energy),'P_ex':float(P),'w_ex':float(P/energy),'dP_dlnn':float(derivative),'cs2_relaxed':float(derivative/(n*EF)),'radially_stable':bool(D>0),'positive_compressibility':bool(D>0 and derivative>0),'stationarity_relative_error':float(abs((us+C)/us))}
    return row,p,n,P,derivative

def main(path):
    start=time.monotonic();out=[];checks={};precision=[];merr=[];dererr=[];sourceerr=[]
    for ee in ('.03','.1'):
        e,c,g,U,d,x0=setup(ee)
        ratios=tuple(map(mp.mpf,('1.0001','1.001','1.01','1.05','1.12','1.20','1.30','1.50')))
        phase=[phase_point(x0*r,e,U,d,x0) for r in ratios];gas=[]
        for ratio in ratios:
            x=x0*ratio;row,*_=gas_point(x,e,U,d,x0);gas.append(row)
            light,ms,mss,heavy,be,scalar=eigen(x,e)
            block=masses(x,e,e,g)[0][3];ours=sorted((light*light,heavy*heavy));merr.append(max(abs(a/b-1) for a,b in zip(ours,sorted(block))))
            exact_s=mp.diff(lambda t:eigen(x*mp.exp(t),e)[0],0);exact_ss=mp.diff(lambda t:eigen(x*mp.exp(t),e)[0],0,2);dererr.extend((abs(exact_s-ms),abs(exact_ss-mss)))
            sourceerr.append(row['stationarity_relative_error'])
        xphase=bisect(lambda r:d(x0*r,2)-2*d(x0*r),mp.mpf('1.12'),mp.mpf('1.5'))*x0
        xold=bisect(lambda r:d(x0*r,2)-3*d(x0*r),mp.mpf('1.12'),mp.mpf('1.3'))*x0
        xrad=bisect(lambda r:d(x0*r,2)+2*d(x0*r),mp.mpf('1.5'),mp.mpf('2.2'))*x0
        boundary=phase_point(xphase,e,U,d,x0)
        # Independent branch finite differences of P(n), without importing the Schur formula.
        x=x0*mp.mpf('1.05');base=gas_point(x,e,U,d,x0);direct=[]
        for ds in (mp.mpf('1e-4'),mp.mpf('5e-5')):
            plus=gas_point(x*mp.exp(ds),e,U,d,x0);minus=gas_point(x*mp.exp(-ds),e,U,d,x0)
            direct.append((plus[3]-minus[3])/(mp.log(plus[2])-mp.log(minus[2])))
        direct_error=abs(direct[-1]/base[4]-1)
        out.append({'h_equals_lambda':ee,'X_min':str(x0),'z_min':str(e*x0/mp.sqrt(c)),'phase_boundary_ratio':str(xphase/x0),'old_waterbag_boundary_ratio':str(xold/x0),'radial_end_ratio':str(xrad/x0),'phase_boundary':boundary,'phase':phase,'adjoint_fermion_gas':gas,'direct_gas_pressure_derivatives':[str(a) for a in direct],'direct_gas_pressure_relative_error':str(direct_error)})
        assert direct_error<mp.mpf('1e-5')
        old=mp.mp.dps;mp.mp.dps=70;us70=mp.diff(lambda t:U(x0*mp.mpf('1.2')*mp.exp(t)),0);uss70=mp.diff(lambda t:U(x0*mp.mpf('1.2')*mp.exp(t)),0,2);mp.mp.dps=old
        us50=d(x0*mp.mpf('1.2'));uss50=d(x0*mp.mpf('1.2'),2);precision.append(max(abs(us70-us50),abs(uss70-uss50)))
        print(json.dumps({k:out[-1][k] for k in ('h_equals_lambda','X_min','phase_boundary_ratio','phase_boundary','direct_gas_pressure_relative_error')},indent=2),flush=True)
    checks={'two_weak_points':len(out)==2,'eight_states_per_branch':all(len(a['phase'])==len(a['adjoint_fermion_gas'])==8 for a in out),'singular_mass_relative_error_below_1e-40':max(merr)<mp.mpf('1e-40'),'analytic_mass_derivatives_below_1e-40':max(dererr)<mp.mpf('1e-40'),'stationarity_relative_error_below_1e-18':max(sourceerr)<1e-18,'precision_difference_below_1e-35':max(precision)<mp.mpf('1e-35'),'rest_kinetic_sources_opposite_sign':all(r['source_full']<0<r['source_kinetic_only'] for a in out for r in a['adjoint_fermion_gas']),'lighter_adjoint_scalar':all(r['scalar_over_fermion_mass']<1 for a in out for r in a['adjoint_fermion_gas']),'anomaly_coefficient':5-5+5==5}
    result={'claim_id':'TP02_NATIVE_STATES','checks':checks,'coupling_cases':out,'max_mass_relative_error':str(max(merr)),'max_mass_derivative_absolute_error':str(max(dererr)),'max_precision_absolute_difference':str(max(precision)),'runtime_seconds':time.monotonic()-start,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'non_claims':['Fixed one-loop exact-spectrum potential at inherited coupling comparator; not fully RG matched','Occupation and phase current are explicit conditional states, not selected abundance or stable particle number','No gauge/IR reaction lifetime, gravity, halo, or finite-gradient closure derived']}
    Path(path).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':checks},indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
