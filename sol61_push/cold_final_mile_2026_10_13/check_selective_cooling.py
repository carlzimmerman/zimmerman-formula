"""CE-FM-008: equilibrium-relative capture budget and optimal frozen Maxwell tail."""
import json,sys,math
from pathlib import Path
from scipy.integrate import quad
from scipy.special import gammaincc,gammainccinv,gamma

checks=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)

def mass(r,N=1.):
    S=math.sqrt(N*N+4*N*r*r)
    return 2*N*r*r/(S+N)
def law_u_gap(r,N):
    S=math.sqrt(N*N+4*N*r*r)
    return 2*N/(S+N),4*N*r*r/(S+N)**2
def w(u,gap=None):
    if u<.05:return sum(u**n/n for n in range(3,30))
    gap=1-u if gap is None else gap
    if not gap>0:raise ValueError('full wall reached')
    return -.5*u*u-u-math.log(gap)
def integrate(f,a,b):
    return quad(f,a,b,epsabs=2e-11,epsrel=2e-11,limit=200)[0]
def tail_energy(N,Q,R):
    return integrate(lambda q:w(Q*q*q)/q**4-N*Q,0,1/R)
def ground_energy(N,Q):
    R=math.sqrt(Q*(Q+N)/N)
    def inside(r):
        u,gap=law_u_gap(r,N)
        return r*r*w(u,gap)-N*u
    return integrate(inside,0,R)+tail_energy(N,Q,R)

R0=50.;Q0=mass(R0);E0=ground_energy(1.,Q0)
B=math.asinh(2*R0)
rootQ=math.sqrt(Q0)
tailforce=-Q0/R0+.5*rootQ*math.log((R0+rootQ)/(R0-rootQ))
chemical=-1/R0+tailforce
h=1e-5
fdN=(ground_energy(1+h,Q0)-ground_energy(1-h,Q0))/(2*h)
fdQ=(ground_energy(1,Q0+h)-ground_energy(1,Q0-h))/(2*h)
check('source envelope derivative',abs(fdN/(-B)-1)<1e-5,{'finite_difference':fdN,'exact':-B})
check('mass envelope derivative',abs(fdQ/chemical-1)<1e-5,{'finite_difference':fdQ,'exact':chemical})

rc=2.;mc=mass(rc)
def capture_potential(d):
    rb=math.sqrt((mc+d)*(mc+d+1));N=1+d;remaining=Q0-d
    def first(r):
        u,gap=law_u_gap(r,1.)
        return r*r*w(u,gap)-N*u
    def strip(r):
        u=mc/r**2
        return r*r*w(u)-N*u
    def outside_strip(r):
        u=(mass(r)-d)/r**2
        return r*r*w(u)-N*u
    return integrate(first,0,rc)+integrate(strip,rc,rb)+integrate(outside_strip,rb,R0)+tail_energy(N,remaining,R0)

captures=[]
for d in (.01,.001,.0001):
    after=capture_potential(d);minimum=ground_energy(1+d,Q0-d);defect=after-minimum
    check(f'nonnegative postcapture rearrangement cost d={d}',defect>=-1e-9,defect)
    captures.append(dict(captured_mass=d,receiver_nonkinetic_release=E0-after,
                         equilibrium_energy_decrease=E0-minimum,excess_potential_cost=defect,
                         first_order_binding_release=(B+chemical)*d,
                         kinetic_removed_if_specific_KE_0_5=.5*d,
                         change_in_excess_if_specific_KE_0_5=defect-.5*d))
ratio=captures[1]['excess_potential_cost']/captures[2]['excess_potential_cost']
check('quadratic spatial mismatch cost',abs(ratio/100-1)<.15,ratio)

tails=[]
for budget in (.001,.01,.05):
    p=budget/Q0;cut=float(gammainccinv(1.5,p));energy_fraction=float(gammaincc(2.5,cut))
    independent=quad(lambda x:x**1.5*math.exp(-x)/gamma(2.5),cut,math.inf,epsabs=1e-13,epsrel=1e-11)[0]
    check(f'gamma tail vs quadrature budget={budget}',abs(independent/energy_fraction-1)<1e-8,independent/energy_fraction-1)
    check(f'optimal frozen tail remains a small cooling fraction budget={budget}',p<energy_fraction<.02,energy_fraction)
    tails.append(dict(capture_budget=budget,captured_mass_fraction=p,velocity_cut_sigma=math.sqrt(2*cut),
                      fraction_initial_KE_removed=energy_fraction,KE_per_captured_mass_over_mean=energy_fraction/p,
                      remaining_specific_KE_ratio=(1-energy_fraction)/(1-p)))
result=dict(checks=checks,initial_ground_mass=Q0,initial_potential_energy=E0,
            B=B,chemical_potential=chemical,capture_rearrangement=captures,optimal_frozen_Maxwell_tail=tails,
            scope='Specified frozen distributions and compact-radius removal; no physical capture selection, collective energy transfer or universal cooling no-go.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
