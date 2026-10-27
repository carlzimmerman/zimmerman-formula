import json,sys,math
import numpy as np
import sympy as s
a,b,q,x=s.symbols('a b q x',positive=True)
S=(1-x)*(a+q)/(a+1+q)+x*(b+q)/(b+1+q)
BB=a+b+1;CC=a*b+a+(b-a)*x;nn=b+1-(b-a)*x
assert s.simplify(1/S-1-(q+nn)/(q*q+BB*q+CC))==0
checks=1;d=json.load(open('campaign_fresh_gravity/CFG770_cassini_stiff_action/cfg770_results.json'));out={}
GM=1.32712440018e20;Lam=5.75*3.0856775814913673e16/math.sqrt(2)
for key,bg in d['numbers']['backgrounds'].items():
 aa=bg['Aperp'];bb=bg['Apar'];vals=[]
 for order in [64,128]:
  c,w=np.polynomial.legendre.leggauss(order);xx=c*c;B=aa+bb+1;C=aa*bb+aa+(bb-aa)*xx
  H=(aa+(bb-aa)*xx+np.sqrt(C))/np.sqrt(B+2*np.sqrt(C))
  P2=(3*xx-1)/2
  # Subtract H(0) exactly under the angular integral to avoid isotropic roundoff.
  H0=(aa+math.sqrt(aa*bb+aa))/math.sqrt(B+2*math.sqrt(aa*bb+aa))
  vals.append(-GM/(2*Lam**3)*float(np.dot(w,P2*(H-H0))))
 assert abs(vals[0]/vals[1]-1)<1e-10;checks+=1
 rel=abs(vals[1]/d['numbers']['T1_Q2'][key]-1)
 assert rel<.001;checks+=1
 out[key]=dict(closed_radial_integral_Q2=vals[1],recorded_Q2=d['numbers']['T1_Q2'][key],relative_difference=rel)
json.dump(dict(checks=checks,comparisons=out,scope='Independent radial-integration reduction of prescribed static linear response; no observational ceiling or covariant carrier validation'),open(sys.argv[1],'w'),indent=2)
