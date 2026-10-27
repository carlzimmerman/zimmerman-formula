import sympy as s,json,sys
from pathlib import Path
u,a,X0,rho0,K,b,k,omega=s.symbols('u a X0 rho0 K b k omega',positive=True)
phi,psi,v,w,eps,F,t=s.symbols('phi psi v w eps F t',real=True)
PX=a*(u**2/2-X0);q=PX*u;Kactual=PX+a*u**2;P0=-rho0+a*(u**2/2-X0)**2/2;rho=u**2*PX-P0
X=((u+eps*v)**2/(1+2*eps*phi)-eps**2*w**2/(1-2*eps*psi))/2
L=s.sqrt(1+2*eps*phi)*(1-2*eps*psi)**s.Rational(3,2)*(-rho0+a*(X-X0)**2/2)
checks=[]
def eq(n,x,y=0):
 z=s.factor(s.trigsimp(x-y));assert z==0,(n,z);checks.append(n)
L1=s.diff(L,eps).subs(eps,0);L2=s.diff(L,eps,2).subs(eps,0)/2
metricpure=L2.subs({v:0,w:0})
eq('actual_firstorder_covariant_action',L1,q*v-rho*phi-3*P0*psi)
eq('actual_secondorder_scalar_metric_mixing',L2-metricpure,Kactual*v**2/2-PX*w**2/2-u*Kactual*phi*v-3*q*psi*v)
# Independent symbol b represents backgroundPX>0, K its true kinetic dictionary.
eta=s.I*omega*u*(K*phi+3*b*psi)/(K*omega**2-b*k**2)
eq('actual_Fourier_phaseequation',(-K*omega**2+b*k**2)*eta,-s.I*omega*u*(K*phi+3*b*psi))
dr=K*(u*(-s.I*omega*eta)-u**2*phi)
eq('proper_density_response',dr,K*u**2*b*(k**2*phi+3*omega**2*psi)/(K*omega**2-b*k**2))
eq('GC_finite_frequency_density_cancellation',dr.subs(b,0))
eq('static_buffer_density_response',dr.subs(omega,0),-K*u**2*phi)
z=u*F/(2*omega)*(s.sin(omega*t)-omega*t*s.cos(omega*t));zd=s.diff(z,t);pot=F*(1-s.cos(omega*t))
eq('resonant_actual_metric_forcing',s.diff(z,t,2)+omega**2*z,u*s.diff(pot,t))
eq('initial_phase',z.subs(t,0));eq('initial_velocity',zd.subs(t,0));eq('initial_metric',pot.subs(t,0))
T=2*s.pi/omega
eq('final_phase',z.subs(t,T),-u*F*s.pi/omega)
eq('final_velocity',zd.subs(t,T));eq('final_metric',pot.subs(t,T));eq('final_metric_rate',s.diff(pot,t).subs(t,T))
E=K*(zd**2+omega**2*z**2)/2
eq('modal_energy_derivative_work',s.diff(E,t),K*zd*u*s.diff(pot,t))
eq('normalized_modal_final_energy',E.subs(t,T),K*u**2*F**2*s.pi**2/2)
x=s.Symbol('x',real=True)
ave=s.integrate(s.cos(k*x)**2,(x,0,2*s.pi/k))/(2*s.pi/k)
eq('cosine_average_normalization',ave,s.Rational(1,2))
eq('physical_cosine_average_quadratic_energy',ave*E.subs(t,T),K*u**2*F**2*s.pi**2/4)
# At the flat endpoint, actual T00 and charge include second-order zero-mode.
rr,du,grad2=s.symbols('rr du grad2',real=True)
XX=((u+rr**2*du)**2-rr**2*grad2)/2
pp=-rho0+a*(XX-X0)**2/2;px=a*(XX-X0)
charge=px*(u+rr**2*du);T00=px*(u+rr**2*du)**2-pp
cq2=s.diff(charge,rr,2).subs(rr,0)/2;ce2=s.diff(T00,rr,2).subs(rr,0)/2
eq('actual_quadratic_charge',cq2,Kactual*du-a*u*grad2/2)
eq('actual_quadratic_physical_energy',ce2,u*Kactual*du-(a*u**2-PX)*grad2/2)
correction=a*u*grad2/(2*Kactual)
eq('fixedQ_zero_mode_mean_correction',cq2.subs(du,correction))
eq('fixedQ_mean_physical_energy',ce2.subs(du,correction),PX*grad2/2)
eq('grandcanonical_quadratic_dictionary',ce2-u*cq2,PX*grad2/2)
result={'all_passed':True,'checks':checks,'count':len(checks),'scope':'CovariantC2 exactexpansion/linearresponse/prescribedmetricpulse; fixedQ quadraticdictionary only, no nonlineartrajectory or livegravitysolution','modal_energy':str(K*u**2*F**2*s.pi**2/2),'cosine_average_energy':str(K*u**2*F**2*s.pi**2/4)}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
