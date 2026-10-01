"""Exact rational arithmetic audit; no ODE integration, spectra or random data."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
checks=[]
def ck(name,left,relation,right):
    ok={'<':left<right,'<=':left<=right,'>':left>right,'>=':left>=right,'==':left==right}[relation]
    checks.append(dict(name=name,left=str(left),relation=relation,right=str(right),passed=ok))
    if not ok: raise AssertionError(checks[-1])
D=F(1,100);Bmin=F(9,10);Bmax=F(11,10);amin=F(99,100);amax=F(51,50)
gmin=F(13,10);gmax=F(8,5);wi=F(1,10000)
ck('exponential upper enclosure',F(100,99),'<',amax)
ck('g squared lower',Bmin**2+amin*Bmin,'>',gmin**2)
ck('g squared upper',Bmax**2+amax*Bmax,'<',gmax**2)
ck('T integrand denominator lower',amin**2+4*F(13,20)**2,'>',F(8,5)**2)
qsub=amin/2*(1-amax/F(8,5));Tlo=F(13,20)*qsub;Thi=amax*gmax/2
ck('q subinterval exact',qsub,'==',F(2871,16000))
ck('T strict lower slack',Tlo,'>',F(11,100))
ck('T strict upper slack',Thi,'<',F(41,50))
ck('U prime upper slack',F(1,98),'<',F(11,1000))
ck('w prime lower slack',-F(11,1000)-F(41,50),'>',-F(21,25))
ck('w prime upper slack',F(11,1000)-F(11,100),'<',-F(9,100))
ck('B box upper',1+Bmax*D,'<',Bmax)
ck('rho box lower',1-Bmax*gmax*D,'>',Bmin)
ck('chi box strict margin',D*F(1,100),'<',F(1,100))
ck('w box lower',wi-F(21,25)*D,'>',-F(1,100))
ck('w box upper',wi,'<',F(1,100))
ck('first turn lower bound',wi/F(21,25),'==',F(1,8400))
ck('first turn upper bound',wi/F(9,100),'==',F(1,900))
ck('endpoint strictly past turn',F(1,900),'<',D)
ck('extension length',D-F(1,900),'==',F(2,225))
ck('endpoint negative upper',wi-F(9,100)*D,'==',-F(8,10000))
Amin=F(4,5);qmax=F(51,100)
ck('A lower slack',2*gmin/(2*Bmax+amax),'>',Amin)
fluidloss=Bmax*gmax**2;gravityloss=4*Bmax**2/Amin
etaloss=F(16,25)+4*qmax**2/Amin
ck('fluid coefficient',fluidloss,'==',F(352,125))
ck('fluid plus cross loss',fluidloss+gravityloss,'==',F(8866,1000))
ck('xi loss rounded safely',fluidloss+gravityloss,'<',F(9))
ck('eta loss exact',etaloss,'==',F(3881,2000))
ck('eta loss rounded safely',etaloss,'<',F(2))
ck('valid Young gradient budget',1-F(1,4)-F(1,4),'==',F(1,2))
ck('minimum derivative coefficient',min(Bmin/2,Amin/2,F(1)),'==',F(2,5))
coerc=F(2,5)-9*D**2/9
l2gap=F(2,5)*9/D**2-9
gap=l2gap/F(11,10)
ck('gradient coercivity',coerc,'==',F(3999,10000))
ck('L2 gap',l2gap,'==',F(35991))
ck('kinetic generalized gap',gap,'==',F(359910,11))
ck('rounded continuum lower bound',gap,'>',F(32700))
# Controls evaluate explicit wrong hypotheses, not altered scientific solutions.
ck('reject too-small T upper bound',F(1,10),'<',Tlo)
ck('reject no-turn endpoint premise',wi-F(9,100)*D,'<',F(0))
ck('reject overspent Young budget',1-F(3,4)-F(3,4),'<',F(0))
# rho=xi=1, psi=x algebraic fixture: original zero = integrated 2D - boundary 2D.
ck('inadmissible endpoint restores identity',2*D-2*D,'==',F(0))
ck('dropping inadmissible endpoint fails',2*D,'>',F(0))
cs=F(10**6);c=F(299792458)
refs=[]
for a0 in [F(93619,10**15),F(11279,10**14)]:
    for branch,E2 in [('constant_vacuum',F(1)),('frozen_H_z3',F(4169,200))]:
        refs.append(dict(a0_m_s2=str(a0),branch=branch,E_squared=str(E2),
            a_star='a0*sqrt(E_squared)',length_m='cs^2/(100*a_star)',
            turn_interval_m=['cs^2/(8400*a_star)','cs^2/(900*a_star)'],
            extension_m_lower='2*cs^2/(225*a_star)',
            omega_squared_lower_s_inv2_exact=str(F(32700)*a0*a0*E2/(cs*cs))))
out=dict(status='passed',arithmetic='exact rational Fraction',
    experiment='certificate comparisons only; no ODE or spectral discretization',
    checks=checks,check_count=len(checks),dimensionless_gap_lower=str(F(32700)),
    unrounded_gap_lower=str(gap),first_turn_bracket=[str(F(1,8400)),str(F(1,900))],
    certified_full_endpoint=str(D),restorations=refs,
    physical_parameters=dict(cs_m_s=str(cs),K_exact=str(c*c/(cs*cs)),
        J_m4_s4=str(cs**4),v_chi_m_s=str(cs),S0='a_star^2',
        initial_rho='a_star^2/(4*pi*G*cs^2)'),randomness=False)
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','arithmetic','check_count','dimensionless_gap_lower','first_turn_bracket','certified_full_endpoint']},indent=2))
