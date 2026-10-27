import sympy as s,numpy as np,json
from scipy.integrate import solve_ivp,simpson
x,a,n,k=s.symbols('x a n k',positive=True)
N=1-n;w=(k-a)/(1-k);f=s.sqrt(x/(1+7*x));f2=x/(1+7*x)
u=n-2*N*a+N*w*w/(2*f2)
xd=-2*(1+x)*w
nd=-2*N*a+N*w*w/f2
ad=-((1-u)*a+u)/N
rhs=[xd,ad,nd]
def dot(v):return sum(s.diff(v,z)*dz for z,dz in zip([x,a,n],rhs))
ch=-w/f
G=N*(dot(ch)+(1+a-nd/(2*N))*ch) # r² U_chi from scalar equation
checks=[]
def check(name,v):
    assert s.factor(v)==0,name
    checks.append(name)
check('flat physical speed identity',(a+w)/(1+w)-k)
check('potential reconstruction obeys scalar equation',(dot(u)-2*u)/ch-G)
cc=(dot(G)-2*G)/ch # r² U_chichi
# The constrained radial perturbation adds r² DeltaV=2 chi_dot G-(1-u)chi_dot² (M=1).
coupled_cc=cc+2*ch*G-(1-u)*ch**2
functions=s.lambdify((x,a,n,k),rhs+[u,w,cc,coupled_cc],modules='numpy',cse=True)
kk=1e-6;x0=.5;a0=1e-10;u0=1e-12
w0=(kk-a0)/(1-kk);f20=x0/(1+7*x0)
N0=(1-u0)/(1+2*a0-w0*w0/(2*f20));n0=1-N0
# Re-evaluate tiny n0 using the algebraically stable equivalent.
n0=(u0+2*a0-w0*w0/(2*f20))/(1+2*a0-w0*w0/(2*f20))
y0=[x0,a0,n0,0.]
L=np.log(20.);ts=np.linspace(0,L,801)
solutions=[]
for tol,step in [(1e-10,.01),(1e-12,.005)]:
    def fun(t,z):
        values=functions(*z[:3],kk)
        return [*values[:3],z[1]] # nu_dot=a
    sol=solve_ivp(fun,[0,L],y0,rtol=tol,atol=tol*1e-5,max_step=step,dense_output=True)
    assert sol.success
    solutions.append(sol.sol(ts))
z=solutions[-1];values=np.array([functions(*z[:3,i],kk) for i in range(len(ts))]).T
us,ws,ccs,coupled_ccs=values[3:];Ns=1-z[2];nus=z[3];rs=np.exp(ts)
assert np.all(Ns>0) and np.all(z[0]>0) and np.all(ws>0) and np.all(us>0)
# Fixed-metric scalar second variation, Dirichlet perturbation delta_chi=r^-1/2 sin(pi log(r)/L).
sn=np.sin(np.pi*ts/L);cs=np.cos(np.pi*ts/L)
q_integrand=np.exp(nus)*np.sqrt(Ns)*((-.5*sn+np.pi/L*cs)**2+ccs/Ns*sn**2)
q_actual=float(simpson(q_integrand,x=ts))
q_coupled=float(simpson(np.exp(nus)*np.sqrt(Ns)*((-.5*sn+np.pi/L*cs)**2+coupled_ccs/Ns*sn**2),x=ts))
assert q_coupled<0
q_coarse=float(simpson((np.exp(nus)*np.sqrt(Ns)*((-.5*sn+np.pi/L*cs)**2+coupled_ccs/Ns*sn**2))[::2],x=ts[::2]))
q_limit=L/2*((np.pi/L)**2-7/4)
assert q_actual<0
C,r,r0,chi,chi0,U0=s.symbols('C r r0 chi chi0 U0',positive=True)
profile=chi0-C*s.log(r/r0)
V=U0-C*C/(2*r0*r0)*s.exp(2*(chi-chi0)/C)
check('log profile solves flat radial scalar equation',s.diff(profile,r,2)+2/r*s.diff(profile,r)-s.diff(V,chi).subs(chi,profile))
check('universal negative curvature',s.diff(V,chi,2).subs(chi,profile)+2/r**2)
t,LL=s.symbols('t LL',positive=True)
trial=s.sin(s.pi*t/LL)
q=s.integrate((s.diff(trial,t)-trial/2)**2-2*trial**2,(t,0,LL))
check('exact Dirichlet trial quadratic form',q-(s.pi**2/(2*LL)-7*LL/8))
# Independent linearized-constraint check, general M, N and canonical scalar.
rr,mm,nn,cp,pot,pot1,eta,etap=s.symbols('rr mm nn cp pot pot1 eta etap',nonzero=True)
rho=nn*cp**2/2+pot;pr=nn*cp**2/2-pot
Np=(1-nn)/rr-rr*rho/mm**2
vp=(1-nn)/(2*rr*nn)+rr*pr/(2*mm**2*nn)
cpp=pot1/nn-(2/rr+vp+Np/(2*nn))*cp
dN=-rr*nn*cp*eta/mm**2
dNp=-(nn*cp*eta+rr*Np*cp*eta+rr*nn*cpp*eta+rr*nn*cp*etap)/mm**2
mass_constraint=-dN/rr-rr*(dN*cp**2/2+nn*cp*etap+pot1*eta)/mm**2
check('momentum solution satisfies linear Hamiltonian constraint',dNp-mass_constraint)
dvp=(rr**2*pot/mm**2-1)*dN/(2*rr*nn**2)+rr*cp*etap/(2*mm**2)-rr*pot1*eta/(2*mm**2*nn)
dB=dvp+dNp/(2*nn)-Np*dN/(2*nn**2)
check('linear lapse combination',dB-((1-rr**2*pot/mm**2)*cp-rr*pot1)*eta/(mm**2*nn))
metric_source=dN*pot1/nn+nn*dB*cp
check('constrained scalar effective mass correction',-metric_source/eta-(2*rr*cp*pot1-(1-rr**2*pot/mm**2)*cp**2)/mm**2)
print(json.dumps({'symbolic_checks':checks,'reconstruction_parameters':{'xi':1,'M':1,'speed_squared':kk,'x_initial':x0,'a_initial':a0,'u_initial':u0,'Einstein_radius_span':20},'sample_count':len(ts),'max_state_refinement_difference':float(np.max(abs(solutions[0]-solutions[1]))),'max_abs_N_minus_1':float(np.max(abs(Ns-1))),'min_U':float(np.min(us/rs**2)),'r_squared_U_chichi_range':[float(ccs.min()),float(ccs.max())],'fixed_metric_trial_quadratic_form':q_actual,'constrained_radial_trial_quadratic_form':q_coupled,'trial_quadrature_coarsening_difference':abs(q_coarse-q_coupled),'max_abs_dimensionless_metric_correction':float(np.max(abs(coupled_ccs-ccs))),'analytic_weak_field_trial_form':q_limit,'sufficient_negative_trial_radius_ratio':float(np.exp(2*np.pi/np.sqrt(7))),'physical_radius_span':float(20*np.sqrt((1+x0)/(1+z[0,-1]))),'non_claims':['Potential reconstructed along one interval, not the prior quartic action','No interior or cosmological matching','Radial Dirichlet annulus instability only; no global matched spacetime or other perturbation sectors','No 32pi prediction']},indent=2))
