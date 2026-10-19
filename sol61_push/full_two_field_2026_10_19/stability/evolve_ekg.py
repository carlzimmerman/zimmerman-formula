"""Spherical full two-complex-field EKG, polar-areal constrained RK4 evolution.

The carrier rotation removes equilibrium phase only; no NR/EOS approximation.
All arrays use scaled complex fields sqrt(4*pi*G) times physical fields.
"""
import argparse,json,math,time
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import eigh_tridiagonal

p=argparse.ArgumentParser()
p.add_argument('--profile',required=True);p.add_argument('--dx',type=float,default=.3)
p.add_argument('--R',type=float,default=400);p.add_argument('--T',type=float,default=500)
p.add_argument('--dt-factor',type=float,default=.2);p.add_argument('--eps-x',type=float,default=0)
p.add_argument('--eps-phi',type=float,default=0);p.add_argument('--lambda-total',type=float,default=.01)
p.add_argument('--result',required=True);args=p.parse_args()
start=time.monotonic();data=np.load(args.profile);oldr=data['r']
N=int(round(args.R/args.dx));dx=args.R/N;r=(np.arange(N)+.5)*dx;faces=np.arange(N+1)*dx
pure='omega_X' in data.files
if pure:
    M=float(data['source_mass']);m=M/(2*math.sqrt(1.0004));fourpiG=float(data['four_pi_G'])
    G=fourpiG/(4*math.pi);lam=args.lambda_total
    g=math.sqrt(lam*(M*M-4*m*m)/3);omegaX=float(data['omega_X'])
    oldmu=data['mass_G'];alpha=np.exp(data['logalpha']);norm=math.sqrt(1-2*oldmu[-1]/oldr[-1])/alpha[-1]
    alpha=alpha*norm;omega=.5*omegaX*norm;oldF=np.zeros_like(oldr);oldX=-data['h']
    olda=1/np.sqrt(1-2*oldmu/np.maximum(oldr,1e-100));olda[0]=1
else:
    M=float(data['M']);m=float(data['m']);G=float(data['G']);fourpiG=4*math.pi*G
    lam=float(data['lambda_total']);g=float(data['g']);omega=float(data['omega'])
    oldF=data['F'];oldX=-data['H'];alpha=data['alpha'];olda=data['a'];oldmu=data['U']
scale=math.sqrt(fourpiG);cc=g/scale;LL=lam/fourpiG
def interp_field(y,mass,frequency):
    spline=CubicSpline(oldr,y,bc_type=((1,0.),'natural'))
    out=spline(np.minimum(r,oldr[-1]))
    outside=r>oldr[-1]
    decay=math.sqrt(max(mass*mass-frequency*frequency,1e-16))
    out[outside]=y[-1]*(oldr[-1]/r[outside])*np.exp(-decay*(r[outside]-oldr[-1]))
    return out.astype(complex)
fields=np.array([interp_field(oldF,m,omega),interp_field(oldX,M,2*omega)])
aold=np.interp(r,oldr,olda);alold=np.interp(r,oldr,alpha)
outside=r>oldr[-1];aold[outside]=1/np.sqrt(1-2*oldmu[-1]/r[outside]);alold[outside]=1/aold[outside]
freq=np.array([omega,2*omega])[:,None]
Pi=-1j*freq*(aold/alold)*fields

def gradient(y):
    d=np.empty_like(y);d[:,1:-1]=(y[:,2:]-y[:,:-2])/(2*dx)
    d[:,0]=(y[:,1]-y[:,0])/(2*dx);d[:,-1]=(-y[:,-1]-y[:,-2])/(2*dx)
    return d

def ctrap(y,initial=0.):
    z=np.empty_like(y);z[0]=initial;z[1:]=initial+np.cumsum((y[1:]+y[:-1])*(.5*dx));return z

def metric(y,q):
    dy=gradient(y)
    S=np.sum(np.abs(q)**2+np.abs(dy)**2,axis=0)
    F,X=y
    U=m*m*np.abs(F)**2+M*M*np.abs(X)**2+2*cc*np.real(np.conj(X)*F*F)+LL*np.abs(F)**4
    I=ctrap(2*r*S,S[0]*r[0]**2)
    massint=ctrap(r*r*(S+U)*np.exp(I),(S[0]+U[0])*r[0]**3/3)
    mu=np.exp(-I)*massint
    NN=1-2*mu/r
    if NN.min()<=0:raise RuntimeError('Areal coordinate horizon/collapse encountered')
    aa=1/np.sqrt(NN)
    logder=(mu/r**2+r*(S*NN-U))/NN
    intlog=ctrap(logder)
    al=np.sqrt(NN[-1])*np.exp(intlog-intlog[-1])
    return aa,al,mu,dy,S,U

def charge(y,q):return float(-2*dx*np.sum(r*r*np.imag(np.conj(y[0])*q[0]+2*np.conj(y[1])*q[1])))

Qtarget=charge(fields,Pi)
if args.eps_x:
    width=max(oldr[np.searchsorted(np.cumsum(oldr*oldr*oldX*oldX),.5*np.sum(oldr*oldr*oldX*oldX))],1.)
    shape=np.exp(-(r/width)**2)
    weight=r*r*np.abs(fields[1])**2*(aold/alold)
    shape-=np.sum(weight*shape)/np.sum(weight)
    fields[1]*=1+args.eps_x*shape;Pi[1]*=1+args.eps_x*shape
if args.eps_phi:
    width=max(1.,.5*oldr[np.searchsorted(np.cumsum(oldr*oldr*oldX*oldX),.5*np.sum(oldr*oldr*oldX*oldX))])
    fields[0]+=args.eps_phi*np.max(np.abs(oldX))*np.exp(-(r/width)**2)
    Pi[0]=-1j*omega*(aold/alold)*fields[0]
Pi*=Qtarget/charge(fields,Pi)

def rhs(y,q):
    aa,al,mu,dy,S,U=metric(y,q);speed=al/aa
    sf=np.empty(N+1);sf[1:-1]=.5*(speed[:-1]+speed[1:]);sf[0]=speed[0];sf[-1]=speed[-1]
    flux=np.zeros((2,N+1),dtype=complex)
    flux[:,1:-1]=faces[1:-1]**2*sf[1:-1]*(y[:,1:]-y[:,:-1])/dx
    flux[:,-1]=faces[-1]**2*sf[-1]*(-2*y[:,-1])/dx
    F,X=y
    deriv=np.array([m*m*F+2*cc*X*np.conj(F)+2*LL*np.abs(F)**2*F,
                    M*M*X+cc*F*F])
    return speed*q+1j*freq*y,(flux[:,1:]-flux[:,:-1])/(dx*r*r)-al*aa*deriv+1j*freq*q

def daughter_modes():
    if not pure:return None
    # Use the unperturbed equilibrium metric for a decoupled first-order Phi test.
    h=np.abs(interp_field(oldX,M,2*omega));a=np.interp(r,oldr,olda);al=np.interp(r,oldr,alpha)
    a[outside]=aold[outside];al[outside]=alold[outside]
    P=al*r*r/a;W=a*r*r/al
    pf=np.empty(N+1);pf[1:-1]=.5*(P[:-1]+P[1:]);pf[0]=0.;pf[-1]=P[-1]*(faces[-1]/r[-1])**2
    kin=(pf[:-1]+pf[1:])/dx**2;kin[-1]+=pf[-1]/dx**2
    off=-pf[1:-1]/dx**2/np.sqrt(W[:-1]*W[1:])
    answer={}
    for name,sign in [('minus',-1),('plus',1),('free_daughter',0)]:
        pot=al*a*r*r*(m*m+(sign*2*cc*h if sign else 0))
        diag=(kin+pot)/W-(omega*omega if sign else 0)
        vals=eigh_tridiagonal(diag,off,select='i',select_range=(0,4),check_finite=False,eigvals_only=True)
        answer[name]=[float(x) for x in vals]
    answer['omega_squared']=omega*omega
    return answer

modes=daughter_modes();records=[];aa,al,mu,dy,S,U=metric(fields,Pi);M0=mu[-1];Q0=charge(fields,Pi)
initial_fields=fields.copy();initial_Pi=Pi.copy();initial_metric=[aa.copy(),al.copy(),mu.copy()]
dt=args.dt_factor*dx;steps=int(math.ceil(args.T/dt));dt=args.T/steps
sample_every=max(1,steps//200)
max_mass_drift=0.;max_charge_drift=0.;max_momentum_residual=0.;prevmu=mu.copy()
for step in range(steps+1):
    if step%sample_every==0 or step==steps:
        aa,al,mu,dy,S,U=metric(fields,Pi)
        Mnow=mu[-1];Qnow=charge(fields,Pi)
        max_mass_drift=max(max_mass_drift,abs(Mnow/M0-1));max_charge_drift=max(max_charge_drift,abs(Qnow/Q0-1))
        massrhs=r*r*(S/aa**2+U)
        radial=np.gradient(mu,dx)-massrhs
        records.append({'t':step*dt,'ADM_mass_G':float(Mnow),'Q_times_G':float(Qnow),
          'phi_center_abs':float(abs(fields[0,0])),'X_center_abs':float(abs(fields[1,0])),
          'phi_norm':float(np.sqrt(dx*np.sum(r*r*np.abs(fields[0])**2))),
          'X_norm':float(np.sqrt(dx*np.sum(r*r*np.abs(fields[1])**2))),
          'min_N':float(np.min(1/aa**2)),
          'radial_mass_constraint_linf':float(np.max(abs(radial[2:-2]))),
          'radial_mass_constraint_relative':float(np.max(abs(radial[2:-2]))/max(np.max(abs(massrhs)),1e-100))})
        if len(records)%40==0:print(json.dumps({'progress_t':step*dt,'mass_drift':max_mass_drift,'charge_drift':max_charge_drift}),flush=True)
    if step==steps:break
    a1,b1=rhs(fields,Pi);a2,b2=rhs(fields+.5*dt*a1,Pi+.5*dt*b1)
    a3,b3=rhs(fields+.5*dt*a2,Pi+.5*dt*b2);a4,b4=rhs(fields+dt*a3,Pi+dt*b3)
    fields+=dt/6*(a1+2*a2+2*a3+a4);Pi+=dt/6*(b1+2*b2+2*b3+b4)
    if not np.isfinite(fields).all():raise RuntimeError('Nonfinite evolution')

finala,finalal,finalmu,*_=metric(fields,Pi)
output=Path(args.result);output.parent.mkdir(parents=True,exist_ok=True)
np.savez(output.with_suffix('.npz'),r=r,fields_initial=initial_fields,Pi_initial=initial_Pi,
         fields_final=fields,Pi_final=Pi,a_initial=initial_metric[0],alpha_initial=initial_metric[1],
         mass_G_initial=initial_metric[2],a_final=finala,alpha_final=finalal,mass_G_final=finalmu)
report={'status':'completed','model':'full canonical two-complex-field EKG in spherical polar-areal gauge; no EOS/NR evolution',
 'profile':args.profile,'pure_X_background':pure,'m':m,'M':M,'G':G,'g':g,'lambda_total':lam,
 'lambda_rep':lam-g*g/(M*M-4*m*m),'omega_Phi_frame':omega,'omega_X':2*omega,
 'grid':{'N':N,'dx':dx,'R':args.R,'T':args.T,'dt':dt,'steps':steps},
 'seeds':{'relative_X_shape':args.eps_x,'relative_Phi_amplitude':args.eps_phi,'total_charge_renormalized':True},
 'max_relative_ADM_drift':max_mass_drift,'max_relative_charge_drift':max_charge_drift,
 'daughter_stiffness_eigenvalues':modes,'records':records,'runtime_seconds':time.monotonic()-start,
 'non_claims':['Finite-time radial evolution does not prove nonlinear or nonradial stability','Dirichlet boundary must be causally distant over claimed central diagnostics','Positive daughter stiffness is a sufficient sector test, not proof of mother/metric stability','No preparation or galaxy force law']}
output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','max_relative_ADM_drift','max_relative_charge_drift','runtime_seconds']}),flush=True)
