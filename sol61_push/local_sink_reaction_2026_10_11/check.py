"""Exact necessary conservation identities for a specified local vacuum deposit."""
import json, math
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent

def main():
    t,x,y,z=s.symbols('t x y z',real=True)
    c,L,tau,rho0,v,eta,V0=s.symbols('c L tau rho0 v eta V0',positive=True)
    xyz=[x,y,z]; rr=x*x+y*y+z*z
    g=s.exp(-rr/(2*L**2)); F=1-s.exp(-t/tau)
    V=V0+eta*rho0*v*v*F*g; rho=rho0*g
    metric=s.diag(-1,1,1,1); T=-V*metric
    def D(f,k):return s.diff(f,t)/c if k==0 else s.diff(f,xyz[k-1])
    div=s.Matrix([sum(D(T[k,j],k) for k in range(4)) for j in range(4)])
    Q=s.diff(V,t); grad=s.Matrix([s.diff(V,q) for q in xyz])
    expected=s.Matrix([Q/c,*list(-grad)])
    checks=[]
    def ck(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(e):return s.simplify(e)==0
    for k in range(4):ck('vacuum_divergence_'+str(k),zero(div[k]-expected[k]))
    cold=-div
    ck('cold_energy_loss',zero(c*cold[0]+Q))
    for i in range(3):ck('cold_momentum_reaction_'+str(i),zero(cold[i+1]-grad[i]))
    cov=metric*div
    for i in range(4):
        for j in range(i+1,4):ck('exchange_integrability_%s_%s'%(i,j),zero(D(cov[j],i)-D(cov[i],j)))
    acc=grad/rho
    for i,q in enumerate(xyz):ck('reaction_acceleration_'+str(i),zero(acc[i]+eta*F*v*v*q/L**2))
    ck('rest_energy_fraction',zero((V-V0)/(rho*c*c)-eta*F*(v/c)**2))
    ck('zero_deposit',all(zero(a.subs(eta,0)) for a in div))
    U=s.Function('U')(t)
    uniform=s.Matrix([s.diff(U,t)/c,0,0,0])
    ck('uniform_sink_has_no_spatial_exchange',all(a==0 for a in uniform[1:]))
    # Hold the deposited energy but omit, or reverse, its necessary reaction.
    deleted=s.Matrix([-Q/c,0,0,0]); reversed_force=s.Matrix([-Q/c,*list(-grad)])
    sample={t:1,tau:1,x:1,y:0,z:0,L:1,c:1,rho0:1,v:1,eta:1,V0:1}
    ck('MUTATE_deleted_momentum_rejected',abs(float((div+deleted)[1].subs(sample)))>.1)
    ck('MUTATE_reversed_reaction_rejected',abs(float((div+reversed_force)[1].subs(sample)))>.1)
    ck('MUTATE_wrong_c_energy_rejected',not zero(cold[0]+Q))
    H,W,power=s.symbols('H W power',positive=True)
    weff=-1-power/(3*H*W)
    ck('effective_w_continuity',zero(power+3*H*(1+weff)*W))
    ck('intrinsic_w_stays_minus_one',zero((-W)/W+1))
    ck('effective_w_phantom_side',s.simplify(weff+1).is_negative is True)
    rows=[]
    for speed in (200000.,1000000.):
        f=1-math.exp(-1)
        rows.append(dict(speed_m_per_s=speed,eta=1.,time_over_tau=1.,rest_energy_fraction=f*(speed/299792458.)**2,acceleration_over_reference=f))
    out=dict(status='conditional_local_vacuum_reaction_identity_not_full_dynamics',passed=sum(k['passed'] for k in checks),total=len(checks),checks=checks,illustrations=rows,formulae=dict(Q=str(s.simplify(Q)),cold_acceleration=[str(s.simplify(a)) for a in acc],rest_energy_fraction='eta F (v/c)^2',force_ratio='eta F',effective_w='-1-Q/(3 H V)'),sympy_version=s.__version__)
    (P/'run/results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['passed'],out['total']);print(json.dumps(rows));print(s.__version__)
    assert all(k['passed'] for k in checks)
if __name__=='__main__':main()
