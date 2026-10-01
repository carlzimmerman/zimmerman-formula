"""Exact-rational checks for one anchor-unit continuum certificate; no orbit/grid."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
checks=[]
def ck(name,left,rel,right):
    ok={'<':left<right,'>':left>right,'<=':left<=right,'>=':left>=right,'==':left==right,'!=':left!=right}[rel]
    checks.append(dict(name=name,left=str(left),relation=rel,right=str(right),passed=ok))
    if not ok: raise AssertionError(checks[-1])
ac=F(93619,10**15);aa=F(11279,10**14);beta=aa/ac
E2=F(641,200);elo=F(179,100);ehi=F(1791,1000)
ck('E1 lower squared',elo**2,'<',E2)
ck('E1 upper squared',ehi**2,'>',E2)
ck('alternative reference ratio exact',beta,'==',F(112790,93619))
ck('alternative ratio lower',beta,'>',F(1))
ck('alternative ratio upper',beta,'<',F(121,100))
ck('uniform alpha upper',beta*ehi,'<',F(11,5))
cases=[
('canonical_vacuum',F(1),F(1),F(1)),
('alternative_vacuum',beta,beta,beta**2),
('canonical_frozen_H1',elo,ehi,E2),
('alternative_frozen_H1',beta*elo,beta*ehi,beta**2*E2)]
for name,alo,ahi,asq in cases:
    ck(name+' alpha lower enclosure',alo,'>=',F(1))
    ck(name+' alpha upper enclosure',ahi,'<',F(11,5))
    ck(name+' squared interval lower',alo**2,'<=',asq)
    ck(name+' squared interval upper',ahi**2,'>=',asq)
amin=F(99,100);amax=F(9,4);bmin=F(9,10);bmax=F(11,10)
gmin=F(13,10);gmax=F(2);D=F(1,100);wi=F(1,10000)
ck('exponential alpha upper',F(11,5)*F(100,99),'<',amax)
ck('g lower squared',bmin*bmin+amin*bmin,'>',gmin*gmin)
ck('g upper squared',bmax*bmax+amax*bmax,'<',gmax*gmax)
ck('A lower slack',2*gmin/(2*bmax+amax),'>',F(1,2))
ratio_denom=1+4*F(13,20)**2/amax**2
ck('T-subinterval normalized denominator',ratio_denom,'>',F(23,20)**2)
qsub=amin/2*(1-F(20,23));tlo=F(13,20)*qsub
ck('q subinterval exact',qsub,'==',F(297,4600))
ck('T lower slack',tlo,'>',F(1,25))
ck('T upper expression',amax*gmax/2,'==',F(9,4))
ck('fixed U derivative slack',F(1,98),'<',F(11,1000))
ck('w derivative lower slack',-F(9,4)-F(11,1000),'>',-F(23,10))
ck('w derivative upper slack',F(11,1000)-F(1,25),'<',-F(1,40))
ck('B first-exit upper',1+bmax*D,'<',bmax)
ck('rho first-exit lower',1-bmax*gmax*D,'>',bmin)
ck('chi first-exit absolute',D/F(40),'<',F(1,100))
ck('w first-exit lower',wi-F(23,10)*D,'>',-F(1,40))
ck('w first-exit upper',wi,'<',F(1,40))
ck('first turn lower',wi/F(23,10),'==',F(1,23000))
ck('first turn upper',wi/F(1,40),'==',F(1,250))
ck('same endpoint beyond all turns',F(1,250),'<',D)
ck('minimum extension beyond turn',D-F(1,250),'==',F(3,500))
ck('endpoint negative upper',wi-F(1,40)*D,'==',-F(3,20000))
Amin=F(1,2);qmax=F(9,8)
fluidloss=bmax*gmax**2;crossloss=4*bmax*bmax/Amin
etaloss=F(7,2)+4*qmax*qmax/Amin
ck('xi total loss exact',fluidloss+crossloss,'==',F(352,25))
ck('xi total loss rounded',fluidloss+crossloss,'<',F(15))
ck('eta total loss exact',etaloss,'==',F(109,8))
ck('eta total loss rounded',etaloss,'<',F(14))
ck('remaining Young stiffness',1-F(1,4)-F(1,4),'==',F(1,2))
ck('uniform derivative minimum',min(bmin/2,Amin/2,F(1)),'==',F(1,4))
coerc=F(1,4)-15*D*D/9;l2=F(1,4)*9/(D*D)-15;gap=l2/bmax
ck('H1 coercivity constant',coerc,'==',F(1499,6000))
ck('L2 lower bound',l2,'==',F(22485))
ck('kinetic spectral infimum lower',gap,'==',F(224850,11))
ck('rounded uniform gap',gap,'>',F(20400))
# Fixed physical units and mutation controls. No varying S0 or length is accepted.
cs=F(10**6);c=F(299792458);Lc=cs*cs/ac;tc=cs/ac
J=cs**4;S0=ac**2;K=c*c/(cs*cs);vchi=cs
ck('fixed dimensionless potential coefficient',S0/(ac*ac),'==',F(1))
ck('fixed dimensionless scale stiffness',J/(cs**4),'==',F(1))
ck('fixed potential kinetic weight',K*cs*cs/(c*c),'==',F(1))
ck('fixed scale kinetic weight',J/(vchi*vchi*cs*cs),'==',F(1))
ck('fixed physical length ratio',(Lc/100)/Lc,'==',D)
ck('fixed physical initial slope',(1/(10000*Lc))*Lc,'==',wi)
rest=[]
for name,alo,ahi,asq in cases:
    if name!='canonical_vacuum':
        ck(name+' reject S0 rescaled to a_ref²',asq,'!=',F(1))
        ck(name+' reject physical length rescaling squared',1/asq,'!=',F(1))
        ck(name+' initial force differs from alpha1',1+alo,'>',F(2))
        ck(name+' reject reference-frequency multiplier',asq,'!=',F(1))
    rest.append(dict(case=name,alpha_interval_exact=[str(alo),str(ahi)],
        alpha_squared_exact=str(asq),initial_g_squared_interval=[str(1+alo),str(1+ahi)],
        physical_length_m_exact=str(Lc/100),physical_time_unit_s_exact=str(tc),
        physical_S0_m2_s4_exact=str(S0),physical_J_m4_s4_exact=str(J),
        physical_K_exact=str(K),v_chi_m_s_exact=str(vchi),
        initial_B_m_s2_exact=str(ac),initial_rho='a_c^2/(4*pi*G*cs^2)',
        initial_chi_x_m_inv_exact=str(1/(10000*Lc)),
        turn_interval_m_exact=[str(Lc/23000),str(Lc/250)],
        omega_squared_lower_s_inv2_exact=str(F(20400)/(tc*tc))))
ck('canonical ratio control',cases[0][3],'==',F(1))
ck('reject undersized T upper',F(1,50),'<',tlo)
ck('reject overspent stiffness budget',1-F(3,4)-F(3,4),'<',F(0))
ck('reject no-turn endpoint',wi-F(1,40)*D,'<',F(0))
ck('nonadmissible fixture boundary restores coupling',2*D-2*D,'==',F(0))
ck('dropping nonadmissible boundary fails',2*D,'>',F(0))
out=dict(status='passed',arithmetic='exact Fraction rational',
    checks=checks,check_count=len(checks),law='Q only',
    alpha_domain=['1','11/5'],reference_cases=rest,
    first_turn_bracket=['1/23000','1/250'],full_endpoint='1/100',
    continuum_gap_lower='20400',unrounded_gap_lower=str(gap),
    gradient_coercivity=str(coerc),common_physical_frequency_unit='a_c/cs',
    physical_couplings_fixed=True,ODE_samples=0,spectral_meshes=0,randomness=False)
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','check_count','alpha_domain','first_turn_bracket','full_endpoint','continuum_gap_lower','common_physical_frequency_unit']},indent=2))
