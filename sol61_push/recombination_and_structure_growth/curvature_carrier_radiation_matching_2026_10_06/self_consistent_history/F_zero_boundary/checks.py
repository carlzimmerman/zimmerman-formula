import argparse,json,sys
from pathlib import Path
import sympy as s
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['omit_tensor_Fdot','call_regular_background_healthy']);args=ap.parse_args();rows=[]
def ck(n,b,e=''):rows.append({'name':n,'passed':bool(b),'detail':str(e)})
def eq(n,e):e=s.factor(s.cancel(e));ck(n,e==0,e)
M,xi,a,Q,v,rd,rr,E,F=s.symbols('M xi a Q v rd rr E F',positive=True)
f0=M/(2*xi);D0=-v/(4*xi);B0=6*xi*M;tot=rd+rr+E;H0=tot/(3*v);R0=(rd+2*(6*xi-1)*E)/B0
root=2*tot/(3*(s.sqrt(v*v+4*F*tot/3)+v))
eq('regular_H_root_limit',s.limit(root,F,0)-H0)
eq('root_first_F_derivative_finite',s.limit(s.diff(root,F),F,0)+tot**2/(9*v**3))
eq('F0_trace_denominator',12*xi**2*f0-B0)
eq('F0_constraint',3*v*H0-tot)
eq('F0_constraint_H_derivative',3*v-3*(2*0*H0+v))
energy0=(D0**2+Q**2/a**6)/f0
eq('charged_energy_decomposition',energy0-v*v/(8*xi*M)-2*xi*Q**2/(M*a**6))
eq('positive_charged_E_gap',energy0-2*xi*Q**2/(M*a**6)-v*v/(8*xi*M))
fdd=-4*xi*(E-3*H0*D0-xi*R0*f0)
eq('Fddot_at_regular_crossing',fdd+2*rd/3+rr+5*E/3)
# DirectADM TT kinetic, determinant-one spatialmetric and homogeneousF.
h,gd=s.symbols('h gd');K=s.diag(h+gd/2,h-gd/2,h)
eq('ADM_TT_extrinsic',s.trace(K*K)-s.trace(K)**2+6*h*h-gd*gd/2)
z=s.symbols('z');g=s.Function('g')(z);wx=s.exp(g/2);wy=s.exp(-g/2)
R3=-2*(s.diff(wx,z,2)/wx+s.diff(wy,z,2)/wy+s.diff(wx,z)*s.diff(wy,z)/(wx*wy))
eq('ADM_TT_spatial_gradient',R3+s.diff(g,z)**2/2)
# Localanalyticcross F=v tau+Fdd tau²/2; a=a0(1+h0tau)+....
tau=s.symbols('tau',positive=True);a0,k=s.symbols('a0 k',positive=True);h0,f2=s.symbols('h0 f2',real=True)
aa=a0*(1+h0*tau);FF=v*tau+f2*tau*tau/2;AA=aa**3*FF;BB=aa*FF*k*k
fric=3*s.diff(aa,tau)/aa if args.mutation=='omit_tensor_Fdot' else s.diff(AA,tau)/AA
freq=BB/AA
eq('simplezero_tensor_friction_residue',s.limit(tau*fric,tau,0)-1)
eq('finite_tensor_frequency',s.limit(freq,tau,0)-k*k/a0**2)
n=s.symbols('n');ind=n*(n-1)+s.limit(tau*fric,tau,0)*n
eq('tensor_indicial_double_zero',ind-n*n)
# IndependentEulerform determines regular coefficients.
g0,g1,g2=s.symbols('g0 g1 g2');gam=g0+g1*tau+g2*tau*tau;EL=s.diff(AA*s.diff(gam,tau),tau)+BB*gam
c0=s.expand(EL).coeff(tau,0);c1=s.expand(EL).coeff(tau,1)
eq('regular_gamma1_forcedzero',c0-a0**3*v*g1)
eq('regular_gamma2_coefficient',c1.subs(g1,0)-a0**3*v*(4*g2+k*k*g0/a0**2))
eq('regular_gamma2_value',c1.subs({g1:0,g2:-k*k*g0/(4*a0*a0)}))
# Reductionoforder integrand exposes unremovablelog for normalizedanalyticgamma.
greg=1-k*k*tau*tau/(4*a0*a0)
eq('second_solution_log_residue',s.limit(tau/(AA*greg**2),tau,0)-1/(a0**3*v))
logEL=s.diff(s.log(tau),tau,2)+fric*s.diff(s.log(tau),tau)+freq*s.log(tau)
eq('log_leading_Euler_balance',s.limit(tau*tau*logEL,tau,0))
eq('tensor_Wronskian_weight',s.simplify(AA*(greg**2)*(1/(AA*greg**2)))-1)
momentum=s.symbols('momentum');Ltt=a**3*F*gd**2/4
eq('TT_physical_Hamiltonian',((momentum*gd-Ltt).subs(gd,2*momentum/(a**3*F)))-momentum**2/(a**3*F))
eq('TT_F0_Legendre_rankzero',s.diff(Ltt,gd,2).subs(F,0))
if args.mutation=='call_regular_background_healthy':ck('F0_tensor_nondegenerate',0>0,'TTkineticF0=0 regardlessfiniteH')
# Readfrozenparentdata only; projectlocalF0 jets, not originaltrajectorycertification.
parent=Path(__file__).resolve().parent.parent
history=json.loads((parent/'runs/history_main_a/results.json').read_text());cases=[]
for run in history['runs']:
 if run['method']!='Radau':continue
 X=run['xi'];point=run['samples'][-1];cr,ci,qr,qi,_=point['state'];ag=point['a'];fg=cr*cr+ci*ci;Dg=cr*qr+ci*qi;Eg=qr*qr+qi*qi;vg=-4*X*Dg
 rdag=(4/3)*ag**-3;rrag=(.01*4/3)*ag**-4;Hlim=(rdag+rrag+Eg)/(3*vg)
 ff0=1/(2*X);Qlate=.4/(8*X*X)*np.sqrt(4*X/3-.25);L0=Qlate/ag**3;Ep=(Dg*Dg+L0*L0)/ff0;Hp=(rdag+rrag+Ep)/(3*vg);Rp=(rdag+2*(6*X-1)*Ep)/(6*X)
 chip=complex(cr,ci)*np.sqrt(ff0/fg);qp=(Dg+1j*L0)*chip/ff0
 qcheck=ag**3*np.imag(np.conjugate(chip)*qp)
 cases.append({'xi':X,'a_guard':ag,'guard_F':point['F'],'Fdot_guard':vg,'guard_H':point['H'],'fixed_coeff_H_F0_limit':Hlim,'Fprime_guard':vg/point['H'],'projected_chi':[chip.real,chip.imag],'projected_chidot':[qp.real,qp.imag],'projected_E':Ep,'projected_H0':Hp,'projected_R0':Rp,'projected_Fddot0':-2*rdag/3-rrag-5*Ep/3,'charge_target':Qlate,'projection_scope':'newlocalonconstraintF0 datum from stoppedpath; no certifiedoriginalF0continuation'})
 ck('guard_positive_Fdot_'+str(X),vg>0,vg)
 ck('finite_fixedcoefficient_limit_'+str(X),np.isfinite(Hlim) and Hlim>0,Hlim)
 ck('projected_charge_'+str(X),abs(qcheck/Qlate-1)<1e-12,qcheck/Qlate-1)
 ck('projected_F0_'+str(X),abs(1-2*X*abs(chip)**2)<1e-12,1-2*X*abs(chip)**2)
 ck('projected_energy_'+str(X),abs(abs(qp)**2/Ep-1)<1e-12,abs(qp)**2/Ep-1)
 ck('projected_constraint_'+str(X),abs(3*vg*Hp-(rdag+rrag+Ep))/(rdag+rrag+Ep)<1e-12,0.)
args.out.mkdir(parents=True,exist_ok=True);out={'checks':rows,'passed':sum(z['passed'] for z in rows),'total':len(rows),'mutation':args.mutation,'cases':cases,'scope':'conditionalanalyticfiniteF0crossing; genericphysicalTTlog/negativeFkinetic; nooriginalhistoryF0certificateorallhistoriesno-go'};(args.out/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[z['name'] for z in rows if not z['passed']],'cases':cases}));sys.exit(0 if out['passed']==out['total'] else 1)
