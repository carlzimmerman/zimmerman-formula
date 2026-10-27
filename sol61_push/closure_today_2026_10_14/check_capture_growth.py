"""Conditional test-carrier capture; prescribed baryon growth, no halo backreaction.
G=a0=Q_initial=1. Frozen full-law carrier background, finite supply S.
No radiation, friction, capture deletion or reflecting boundary.
"""
import json,sys
import numpy as np
from scipy.integrate import solve_ivp,quad

def model(S):
    edge=np.sqrt(S+S*S) if S else 0.
    def potential(r):
        if not S:return -1/r
        rr=max(r,edge)
        return -(1+S)/rr+np.sqrt(S)*np.arctanh(np.sqrt(S)/rr)
    def tether(r):
        if not S:return 0.
        if r<=edge:return 1/r**2 # exact equilibrium root R(m0/r^2)=1/r^2
        u=S/r**2
        return u*u/(1-u)
    return edge,potential,tether

def run(S,delta,center,width,rtol,atol,end=260.):
    edge,pot,tether=model(S)
    r0=np.hypot(30.,1.)
    speed=np.sqrt(2*(.02-pot(r0)))
    initial=[-30.,1.,speed,0.,0.]
    def growth(t):
        z=(t-(center-width))/(2*width)
        if z<=0:return 0.,0.
        if z>=1:return delta,0.
        return delta*(3*z*z-2*z**3),delta*6*z*(1-z)/(2*width)
    def rhs(t,y):
        x,yy,vx,vy,W=y
        r=np.hypot(x,yy)
        dq,dqdot=growth(t)
        ar=-(1+dq)/r**2+tether(r)
        return [vx,vy,ar*x/r,ar*yy/r,-dqdot/r]
    sol=solve_ivp(rhs,[0,end],initial,rtol=rtol,atol=atol,dense_output=True,max_step=.4)
    assert sol.success,sol.message
    times=np.linspace(0,end,2601);states=sol.sol(times)
    rs=np.hypot(states[0],states[1])
    dq=np.array([growth(t)[0] for t in times])
    energy=(states[2]**2+states[3]**2)/2+np.array([pot(r) for r in rs])-dq/rs
    L=states[0]*states[3]-states[1]*states[2]
    work_quad=quad(lambda t:-growth(t)[1]/np.hypot(*sol.sol(t)[:2]),
                   max(0,center-width),min(end,center+width),epsabs=2e-10,limit=200)[0]
    return dict(S=S,delta_Q=delta,center=center,width=width,edge=edge,
        initial_energy=float(energy[0]),final_energy=float(energy[-1]),
        work=float(states[4,-1]),independent_work_quadrature=float(work_quad),
        energy_work_error=float(np.max(np.abs(energy-energy[0]-states[4]))),
        angular_momentum_error=float(np.max(np.abs(L-L[0]))),
        minimum_radius=float(rs.min()),maximum_postgrowth_radius=float(rs[times>center+width].max()),
        endpoint=states[:4,-1].tolist(),pericenter_time=float(times[np.argmin(rs)]))

checks=[]; rows=[]
def check(name,cond):
    assert cond,name
    checks.append(name)

for S in [0.,5.]:
    static=run(S,0.,100.,5.,2e-10,2e-12)
    check(f'S{S} static incoming orbit remains positive energy',static['final_energy']>.019999)
    check(f'S{S} static energy control',static['energy_work_error']<2e-7)
    center=static['pericenter_time']
    # Frozen experiment design, not a rate estimate or prediction for any galaxy.
    delta=.2
    growth=run(S,delta,center,5.,2e-10,2e-12)
    fine=run(S,delta,center,5.,2e-12,2e-14)
    check(f'S{S} growing source gives bound energy',fine['final_energy']<0)
    check(f'S{S} source work accounts for energy',fine['energy_work_error']<2e-7)
    check(f'S{S} independent source-work quadrature',abs(fine['work']-fine['independent_work_quadrature'])<2e-7)
    check(f'S{S} torque-free angular momentum',fine['angular_momentum_error']<2e-7)
    check(f'S{S} tolerance comparison energy',abs(growth['final_energy']-fine['final_energy'])<2e-7)
    check(f'S{S} tolerance comparison endpoint',np.max(np.abs(np.array(growth['endpoint'])-fine['endpoint']))<2e-4)
    rows.append(dict(static=static,growth=growth,fine=fine))

json.dump({'claim_id':'CT-003','checks':checks,'count':len(checks),'cases':rows,
 'status':'conditional capture witnesses passed','limits':['Prescribed time-dependent baryon source, not a varied reciprocal parent',
 'Frozen test-carrier background and negligible captured mass','No capture rate, abundance or DF2/DF4/DF9 fit',
 'Negative final energy establishes binding to the final frozen potential, not cold equilibrium or stable halo formation']},open(sys.argv[1],'w'),indent=2)
