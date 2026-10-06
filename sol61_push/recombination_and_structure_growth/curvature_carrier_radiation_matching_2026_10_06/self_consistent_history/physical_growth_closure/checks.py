import argparse,json,pathlib,sys
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
import growth as g
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','dust_only','drop_trace'],default='none');args=ap.parse_args();checks=[];records=[]
def ck(name,v):checks.append({'name':name,'passed':bool(v)})
F,fd,H,p,Ph,Z,dF,dFd,drho,dq=s.symbols('F fd H p Ph Z dF dFd drho dq');Psi=Ph-dF/F
C00=2*F*p*Ph+6*F*H*Z+drho-(p+3*H*H)*dF-3*H*dFd+3*fd*(Z-H*Psi)+6*H*fd*Psi
CW=2*F*p*(Ph+Psi)/2+drho-3*H*dq-6*H*H*dF+3*fd*Z
ck('mixed00_to_Weyl_exact',s.simplify((C00-CW).subs(Z,(-dq+dFd-H*dF-fd*Psi)/(2*F)))==0)
C,P,Cdot=s.symbols('C P Cdot');div=Cdot+3*H*(C-P);trace=C+3*P
ck('Noether_constraint_propagator',s.simplify((div-fd*trace/(2*F)).subs(P,0).subs(Cdot,(-3*H+fd/(2*F))*C))==0)
M,xi,f,X,Ralg,Rgeo,rd=s.symbols('M xi f X Ralg Rgeo rd');FF=M-2*xi*f;BB=FF+12*xi*xi*f;boxF=-4*xi*X-4*xi*xi*Ralg*f
etrace=-FF*Rgeo+2*X+rd+3*boxF
ck('raw_trace_residual',s.simplify((etrace-FF*(Ralg-Rgeo)).subs(rd,BB*Ralg+2*(6*xi-1)*X))==0)
L,om,E=s.symbols('L om E');ph=-2*L*om/(2*F*p-2*E-3*fd*fd/(2*F));zz=-fd*ph/(2*F)
ck('charged_phase_velocity_Weyl_constraint',s.simplify(2*F*p*ph+2*L*om-2*ph*E+3*fd*zz)==0)
ck('phase_seed_not_dust_source',s.simplify(ph.subs(L,0))==0 and s.simplify(ph.subs(om,0))==0)
DROP=args.control=='drop_trace'
for xi0 in [100,1000]:
 b=g.bg.initial(xi0);u=g.bg.quantities(0,b,xi0);k=10*u['H'];eps=1e-22
 # Offconstraint identity, checked by an independent analytic complex-step directional derivative.
 rand=np.array([.03,-.02,.07,.015,.01,.08,.03,-.01,.04]);yy=np.r_[b,rand];v=g.rows(0,b,rand,xi0,k,DROP);dy=g.rhs(0,yy,xi0,k,DROP)
 Cp=np.imag(g.rows(1j*eps,b+1j*eps*dy[:5],rand+1j*eps*dy[5:],xi0,k,DROP)['C00'])/eps
 target=(-3+u['Fdot']/(2*u['F']*u['H']))*v['C00']
 ck('constraint_propagation_derivative_'+str(xi0),abs(Cp-target)<1e-10*(1+abs(target)))
 Pddx=np.imag(g.rows(1j*eps,b+1j*eps*dy[:5],rand+1j*eps*dy[5:],xi0,k,DROP)['Phi_dot'])/eps
 Pdd=Pddx*u['H'];Psidot=v['Phi_dot']-v['deltaFdot']/u['F']+v['deltaF']*u['Fdot']/u['F']**2
 Rgeo=-6*Pdd-6*u['H']*(Psidot+4*v['Phi_dot'])-2*u['R']*v['Psi']+2*k*k*(v['Psi']-2*v['Phi'])
 ck('actual_geometric_Ricci_constraint_'+str(xi0),abs(Rgeo-v['deltaR']+v['C00']/u['F'])<1e-10*(1+abs(Rgeo)))
 # Actual Noether charge density in Newton gauge and its phase-transport divergence.
 def charge(x,b,z):
  a=np.exp(x);cr,ci,qr,qi,_=b;dc1,dc2,dq1,dq2,Ph,*_=z;v=g.rows(x,b,z,xi0,k,DROP);LL=cr*qi-ci*qr;dLL=cr*dq2-ci*dq1+dc1*qi-dc2*qr
  return a**3*(dLL-LL*(v['Psi']+3*Ph))
 qp=np.imag(charge(1j*eps,b+1j*eps*dy[:5],rand+1j*eps*dy[5:]))/eps
 qtarget=-k*k*(b[0]*rand[1]-b[1]*rand[0])/u['H']
 ck('actual_charge_transport_'+str(xi0),abs(qp-qtarget)<1e-10*(1+abs(qtarget)))
 for mode in ['phase','dust']:
  y0,meta=g.initial(xi0,k,mode,dust_only=args.control=='dust_only');r0=g.rows(0,y0[:5],y0[5:],xi0,k,DROP)
  ck('initial_actual_Hamiltonian_'+str(xi0)+'_'+mode,abs(r0['C00'])<1e-11*(1+r0['constraint_scale']))
  if mode=='phase':
   ck('phase_changes_W_at_equal_dust_'+str(xi0),abs(r0['W'])>0 and y0[10]==0 and y0[11]==0)
   ck('phase_slip_and_momentum_zero_'+str(xi0),abs(r0['deltaF'])<1e-20 and abs(r0['deltaFdot'])<1e-20 and abs(r0['deltaq'])<1e-20)
  curves=[]
  for method in ['DOP853','Radau']:
   sol=solve_ivp(lambda x,y:g.rhs(x,y,xi0,k,DROP),(0,np.log(2)),y0,method=method,rtol=1e-9,atol=1e-12,t_eval=np.linspace(0,np.log(2),41))
   ck('finite_integration_'+str(xi0)+'_'+mode+'_'+method,sol.success and len(sol.t)==41 and sol.nfev<20000)
   vv=[g.rows(x,y[:5],y[5:],xi0,k,DROP) for x,y in zip(sol.t,sol.y.T)]
   defect=max(abs(t['C00'])/(1e-20+t['constraint_scale']) for t in vv)
   ck('Hamiltonian_preserved_'+str(xi0)+'_'+mode+'_'+method,defect<1e-6)
   ck('Weyl_constraint_same_'+str(xi0)+'_'+mode+'_'+method,max(abs(t['CW']-t['C00'])/(1e-20+t['constraint_scale']) for t in vv)<1e-10)
   ck('background_F_positive_'+str(xi0)+'_'+mode+'_'+method,min(t['background']['F'] for t in vv)>0)
   end=vv[-1];records.append({'xi':xi0,'mode':mode,'method':method,'nfev':sol.nfev,'Cmax_relative':defect,'initial_W':float(r0['W']),'final_W':float(end['W']),'final_dust_comoving':float(end['dust_comoving']),'final_radiation_density':float(sol.y[-2,-1]),'a_end':float(np.exp(sol.t[-1])),'Fmin':float(min(t['background']['F'] for t in vv)),'H_end':float(end['background']['H']),'seed_meta':{key:float(val) for key,val in meta.items()},'columns':{'x':sol.t.tolist(),'W':[float(t['W']) for t in vv],'dust_comoving':[float(t['dust_comoving']) for t in vv]}})
   # Physical common vector norm; avoids near-zero component divisions.
   amp=np.hypot(b[0],b[1]);sc=np.array([amp,amp,amp*u['H'],amp*u['H'],1,1,1/u['H'],1,1/u['H']]);curves.append(sol.y[5:]/sc[:,None])
  diff=float(np.max(np.linalg.norm(curves[0]-curves[1],axis=0)/(1+np.linalg.norm(curves[0],axis=0))))
  ck('independent_solver_agreement_'+str(xi0)+'_'+mode,diff<1e-6)
  records[-1]['solver_pair_common_norm_error']=diff
out={'passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'records':records,'control':args.control,'scope':'exact action identities plus 8 normalized unit-seed finite ideal-fluid transfer paths; no observed power-spectrum/CMB/cold-identity claim'}
pth=pathlib.Path(args.output);pth.parent.mkdir(parents=True,exist_ok=True);pth.write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failures':[c['name'] for c in checks if not c['passed']],'endpoints':[{k:v for k,v in rec.items() if k!='columns'} for rec in records]}));sys.exit(out['passed']!=out['total'])
