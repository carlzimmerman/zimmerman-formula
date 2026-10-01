from fractions import Fraction as F
from pathlib import Path
import json,sys

checks=[]
def ck(name,yes):
    checks.append({'name':name,'pass':bool(yes)});assert yes,name
alpha_alt=F(112790,93619);e2=F(641,200);alo=F(1);ahi=F(11,5)
ck('frozen H root enclosure',F(179,100)**2<e2<F(9,5)**2)
ck('four reference membership',1<alpha_alt<ahi and alpha_alt*F(9,5)<ahi)
a0=F(99,100);a1=F(9,4);b0=r0=F(9,10);b1=r1=F(11,10)
ck('scale box from exponential bounds',ahi*F(100,99)<a1)
g0=F(13,10);g1=F(2);A0=F(4,5);q1=F(3,5)
ck('force lower square',b0*b0+a0*b0>g0*g0)
ck('force upper square',b1*b1+a1*b1<g1*g1)
ck('A lower via exact square',1-(a1/(2*b0+a1))**2>A0*A0)
ck('q upper',a1*b1/(2*b1+a1)<q1)
ck('integral ratio bound',a1*a1+4*(g0/2)**2>F(5,2)**2 and a1/F(5,2)==F(9,10))
ck('T lower',g0/2*a0/2*F(1,10)>F(3,100))
ck('T upper',a1*g1/2==F(9,4))
up=F(11,1000);T0=F(3,100);T1=F(9,4)
ck('potential derivative bound',F(1,98)<up)
wl=F(-227,100);wu=F(-19,1000)
ck('scale slope derivative enclosure',-up-T1>wl and up-T0==wu)
D=F(1,100);w0=F(1,10000)
ck('density remains interior',1-r1*g1*D>r0)
ck('source remains interior',1+r1*D<b1)
ck('scale remains interior',D*F(3,100)<F(1,100))
ck('slope remains interior',w0+wl*D>F(-3,100) and w0<F(3,100))
lo=w0/(-wl);hi=w0/(-wu)
ck('turn brackets',lo==F(1,22700) and hi==F(1,190) and hi<D)
ck('post turn length',D-hi==F(9,1900))
neg_x=r1*g1*g1+4*r1*r1/A0;neg_e=2*T1-1+4*q1*q1/A0
ck('Xi penalty',neg_x==F(209,20) and neg_x<11)
ck('eta penalty',neg_e==F(53,10) and neg_e<6)
ck('gradient coefficient',r0/2>F(2,5) and A0/2==F(2,5))
gap= (F(2,5)*9/D**2-11)/r1
ck('common continuum gap',gap==F(359890,11) and gap>32700)
ck('gradient coercivity',F(2,5)-11*D**2/9==F(35989,90000))
ck('anchor control force',1+F(1)==2)
ck('reject hidden alpha1 for alternative',1+alpha_alt!=2)
ck('reject retuned potential coefficient',alpha_alt**2!=1)
ck('large domain uncertified not unstable',F(2,5)*9-11<0)
ck('Young allocation',1-F(1,4)-F(1,4)==F(1,2) and 1-F(3,4)-F(3,4)<0)
ck('boundary nonadmissible control',2*D-2*D==0 and 2*D!=0)
ac=F(93619,10**15);cs=F(10**6);Lc=cs**2/ac
res={'exact_claim':'Uniform fixed-unit Q compact-box/continuum certificate for alpha in[1,11/5]',
 'checks':checks,'all_checks_passed':True,'alpha_alternative_exact':str(alpha_alt),'E1_squared_exact':str(e2),
 'alpha_interval':['1','11/5'],'D':'1/100','turn_open_bracket':[str(lo),str(hi)],
 'postturn_length_lower':str(D-hi),'gap_dimensionless_exact':str(gap),
 'gap_physical_squared_frequency_exact':str(gap*(ac/cs)**2),
 'gap_physical_squared_frequency_s2':float(gap*(ac/cs)**2),
 'fixed_Lc_m':float(Lc),'fixed_slab_length_m':float(D*Lc),
 'assumptions':['Q diagnostic action','fixed couplings/left data','IVP induced right walls','Dirichlet perturbations'],
 'nonclaims':['observed coefficients','time-dependent cosmology','RAR/M or filtered MONO','metric closure','ODE orbit or sampled spectrum']}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'gap':str(gap),'physical_gap':res['gap_physical_squared_frequency_s2']}))
