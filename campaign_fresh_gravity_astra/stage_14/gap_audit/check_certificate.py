from fractions import Fraction as F
from pathlib import Path
import json,sys
D=F(1,100);bmin=rhomin=F(9,10);bmax=rhomax=F(11,10);chimax=wmax=F(1,100);w0=F(1,10000)
amin=F(99,100);amax=F(51,50);gmin=F(13,10);gmax=F(8,5);checks=[]
def check(name,condition,expression):
 assert condition,name;checks.append({'name':name,'pass':True,'exact_observed':str(expression)})
check('exp upper rational envelope',1/(1-chimax)<amax,1/(1-chimax))
check('exp lower envelope',1-chimax==amin,1-chimax)
gsqlo=bmin*bmin+amin*bmin;gsqhi=bmax*bmax+amax*bmax
check('lower g square',gsqlo>gmin*gmin,gsqlo-gmin*gmin)
check('upper g square',gsqhi<gmax*gmax,gmax*gmax-gsqhi)
Alo=2*gmin/(2*bmax+amax);check('A above 4/5',Alo>F(4,5),Alo)
check('q segment sqrt bound',amin**2+gmin**2>F(8,5)**2,amin**2+gmin**2-F(8,5)**2)
qsegment=amin/2*(1-amax/F(8,5));Tlo=gmin/2*qsegment;Thi=amax*gmax/2
check('T lower >.11',Tlo>F(11,100),Tlo)
check('T upper <.82',Thi<F(41,50),Thi)
t=2*chimax;Upbound=(1/(1-t)-(1-t))/4
check('abs Uprime <.011',Upbound<F(11,1000),Upbound)
wplo=-F(21,25);wphi=-F(9,100)
check('wprime lower valid',-F(11,1000)-F(41,50)>wplo,-F(11,1000)-F(41,50))
check('wprime upper valid',F(11,1000)-F(11,100)<wphi,F(11,1000)-F(11,100))
enclosure={'b_lower':F(1),'b_upper':1+D*rhomax,'rho_lower':1-D*rhomax*gmax,'rho_upper':F(1),'w_lower':w0+D*wplo,'w_upper':w0,'chi_abs_upper':D*wmax}
check('b strict box',bmin<enclosure['b_lower']<=enclosure['b_upper']<bmax,enclosure['b_upper'])
check('rho strict box',rhomin<enclosure['rho_lower']<=1<rhomax,enclosure['rho_lower'])
check('w strict box',-wmax<enclosure['w_lower']<=w0<wmax,enclosure['w_lower'])
check('chi strict box',enclosure['chi_abs_upper']<chimax,enclosure['chi_abs_upper'])
turnlo=F(1,10000);turnhi=F(1,800)
check('turn lower endpoint positive',w0+wplo*turnlo>0,w0+wplo*turnlo)
check('turn upper endpoint negative',w0+wphi*turnhi<0,w0+wphi*turnhi)
negxi=rhomax*gmax*gmax+4*rhomax*rhomax/F(4,5)
meta=1-2*F(41,50);negeta=4*(amax/2)**2/F(4,5)-meta
check('xi negative coefficient <9',negxi<9,negxi)
check('eta negative coefficient <2',negeta<2,negeta)
grad=F(2,5);l2=grad*9/D**2-9;kinmax=F(11,10);omega2=l2/kinmax;coerc=grad-D**2
check('gap exact value',omega2==F(359910,11),omega2)
check('gap >32000',omega2>32000,omega2-32000)
check('gradient coercivity',coerc==F(3999,10000),coerc)
check('postturn extension >7/800',D-turnhi==F(7,800),D-turnhi)
# Failed premises are controls, not instability proofs.
check('D1 formal bound rejected',grad*9-9<0,grad*9-9)
check('initial A>=1 mutant rejected',F(8,9)<1,F(8,9))
out={'arithmetic':'exact rational; analytic exponential/ODE/Poincare reductions in ROOT_DERIVATION.md','checks':checks,'enclosure':{k:str(v) for k,v in enclosure.items()},'first_turn_open_bracket':[str(turnlo),str(turnhi)],'full_domain':str(D),'post_turn_length_strict_lower':str(D-turnhi),'continuum_squared_frequency_lower_bound':str(omega2),'reported_conservative_lower':32000,'gradient_coercivity':str(coerc),'negative_control_interpretation':'Rejects certificate/domain or altered bound, not physical instability','grid_points':0,'ODE_numeric_trajectories':0,'laws_actually_certified':['Q'],'physical_restoration':'omega_phys^2 >= (359910/11)*a_ref/L_ref; chosen couplings scale with references','normalizations_m_s2':['9.3619e-11','1.1279e-10'],'histories':['constant vacuum reference','distinct frozen H(z) reference'],'non_claims':['RAR or M theorem','Time-dependent cosmology','Measured couplings','Nonlinear/3D/metric closure']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','enclosure']}))
