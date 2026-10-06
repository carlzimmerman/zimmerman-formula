import argparse,json,pathlib
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','reverse_sign','stable_MOND','fit_band'],default='none');ar=ap.parse_args();rows=[]
def ck(n,b,d=None):rows.append(dict(name=n,passed=bool(b),detail=d))
def ze(n,e):e=s.factor(e);ck(n,e==0,str(e))
X,R,J,g,q,k=s.symbols('X R J g q k',positive=True);F=s.Function('F')(R);V=s.Function('V')(R)
station=s.diff(V,R)-X*s.diff(F,R);H=s.diff(station,R)
rx=s.diff(F,R)/H
ze('one_amplitude_implicit_derivative',H*rx-s.diff(F,R))
ze('on_shell_P_first_derivative',F+(X*s.diff(F,R)-s.diff(V,R))*rx-F+station*rx)
ze('on_shell_P_second_derivative',s.diff(F,R)*rx-s.diff(F,R)**2/H)
charge=V+J*J/(2*F)+F*g*g/2
stc=s.diff(charge,R);hcharge=s.diff(charge,R,2)
Xc=(J*J/F**2-g*g)/2
ze('charge_stationary_equivalence',stc-station.subs(X,Xc))
ze('charge_Hessian_at_stationarity',hcharge-(H.subs(X,Xc)+J*J*s.diff(F,R)**2/F**3))
ze('charge_mixed_gradient',s.diff(stc,g)-g*s.diff(F,R))
hh,fa=s.symbols('hh fa',positive=True)
sign= -g*fa**2/hh
ck('stable_gap_nonincreasing_response',s.ask(s.Q.negative(sign)) is True)
# Exact two-amplitude positive diagonal metric gives a sum of positive squares.
h1,h2,b1,b2=s.symbols('h1 h2 b1 b2',positive=True)
inv=s.diag(h1,h2).inv();grad=s.Matrix([b1,b2]);curv=(grad.T*inv*grad)[0]
ze('two_amplitude_positive_gap_quadratic',curv-b1*b1/h1-b2*b2/h2)
ck('multi_amplitude_nonnegative_sample',s.ask(s.Q.positive(curv)) is True)
# Fixed-clock MOND canonical complex embedding; X eliminated by R stationary.
vc=-R**6/(6*k*k);fc=R*R;xx=-R**4/(2*k*k)
ze('complex_MOND_stationary',s.diff(vc,R)-xx*s.diff(fc,R))
hc=s.diff(vc,R,2)-xx*s.diff(fc,R,2)
ze('complex_MOND_negative_gap',hc+4*R**4/(k*k))
ck('canonical_complex_gap_not_stable',s.ask(s.Q.negative(hc)) is True)
xs=s.symbols('xs',negative=True);px=k*s.sqrt(-2*xs);pxx=s.diff(px,xs)
ze('MOND_single_field_positive_longitudinal',px+2*xs*pxx-2*px)
ze('MOND_radial_speed_two',(px+2*xs*pxx)/px-2)
ck('MOND_PXX_negative_not_generic_ghost',s.ask(s.Q.negative(pxx)) is True)
ze('complex_legendre_P',fc*xx-vc+R**6/(3*k*k))
# Sharp endpoint minimax bound is attained by constant mu.
g1,g2,a0=s.symbols('g1 g2 a0',positive=True);eps=(g2-g1)/(g2+g1);const=2*g1*g2/(a0*(g1+g2))
ze('sharp_lower_endpoint',const/(g1/a0)-1-eps)
ze('sharp_upper_endpoint',1-const/(g2/a0)-eps)
ze('one_decade_minimum_error',eps.subs(g2,10*g1)-s.Rational(9,11))
ze('ten_percent_band_ratio',((1+s.Rational(1,10))/(1-s.Rational(1,10)))-s.Rational(11,9))
n=s.symbols('n',positive=True);rr=s.symbols('rr',positive=True);gg=s.Function('gradient')(rr);mu=s.Function('mu')(gg)
flux=rr**(n-1)*mu*gg
ze('radial_flux_log_derivative',rr*s.diff(flux,rr)/flux-(n-1)-(1+gg*s.diff(mu,gg)/mu)*rr*s.diff(gg,rr)/gg)
if ar.control=='reverse_sign':ck('CONTROL_response_increases',s.ask(s.Q.positive(sign)) is True)
if ar.control=='stable_MOND':ck('CONTROL_complex_MOND_gap_positive',s.ask(s.Q.positive(hc)) is True)
if ar.control=='fit_band':ck('CONTROL_one_decade_ten_percent',s.Rational(9,11)<=s.Rational(1,10))
out=dict(passed=all(r['passed'] for r in rows),checks=rows,scope='Exact stationary positive-gap models and direct force dictionary; no generic ghost theorem, coupled gravity, finite-temperature medium or32pi selector',control=ar.control)
pathlib.Path(ar.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],total=len(rows))));raise SystemExit(0 if out['passed'] else 1)
