"""Prescribed common mean-field potential; fixed neutral pole and source spectrum."""
import json, math, sys
from pathlib import Path
from scipy.integrate import quad
from scipy.special import ndtr
checks=[]
def test(name,x):
 checks.append(dict(name=name,passed=bool(x)))
 assert x,name
m=1e6;delta=2e-9;w=1e-12;U0=1.9208763923634617e-9
hc=1.973269804e-7;c=299792458.;ev=1.602176634e-19
sigpeak=2*math.pi/(2*m)**2*hc**2
ng=1e6/(1e-6*m*ev*c);volume=2e-9;peak_rate=2*c*ng*ng*sigpeak*volume
band=1e-10
# x=incident total CM energy minus fixed vacuum resonance energy.
# D=vacuum excess minus twice the interior carrier shift.
def sig(x,D):
 if x+D<=0:return 0.
 r=math.sqrt((x+D)/delta)
 return 4*r/(4*(x/w)**2+(1+r)**2)
def pdf(x):return math.exp(-.5*(x/band)**2)/(math.sqrt(2*math.pi)*band)
def folded(D):
 lo=max(-D,-12*band);hi=12*band
 if lo>=hi:return 0.
 # Dimensionless pole-width coordinate, independent adaptive subintervals.
 zlo=lo/w;zhi=hi/w
 pts=sorted(set([zlo,zhi]+[v for v in [-100,-10,-1,0,1,10,100] if zlo<v<zhi]))
 direct=sum(quad(lambda z:sig(w*z,D)*pdf(w*z)*w,a,b,epsabs=1e-14,epsrel=1e-10,limit=300)[0] for a,b in zip(pts,pts[1:]))
 # Independent tangent coordinate resolves the pole differently.
 thlo=math.atan(zlo);thhi=math.atan(zhi)
 angled=quad(lambda th:sig(w*math.tan(th),D)*pdf(w*math.tan(th))*w/math.cos(th)**2,thlo,thhi,points=[0] if thlo<0<thhi else None,epsabs=1e-14,epsrel=1e-10,limit=300)[0]
 test('independent fold '+str(D),abs(direct-angled)<1e-8*max(direct,1e-10))
 return direct
rows=[]
for f in [0,.1,.25,.5,.52,.6,1.]:
 U=f*U0;D=delta-2*U;barrier=U0-U
 tail=float(ndtr(D/band)) # photons above shifted threshold, all angles CM at rest
 # Since sigma/sigma_peak<=1, this is a rigorous spectral upper bound
 # within the prescribed line shape, including Gaussian tails beyond integration.
 bound=peak_rate*tail
 rate=peak_rate*folded(D) if -D<12*band else None
 test('spectral upper bound '+str(f),rate is None or 0<=rate<=bound*(1+1e-10))
 K=D/2 if D>0 else None
 if K is not None:test('barrier margin cancellation '+str(f),math.isclose(barrier-K,U0-delta/2,rel_tol=1e-12))
 rows.append(dict(bath_density_fraction=f,bath_density_m3=f*1e25,D_eV=D,pole_open=D>0,pole_product_K_eV=K,relative_barrier_eV=barrier,ideal_pairs_s=rate,all_spectrum_pairs_s_upper_bound=bound))
# The line shape's upper bound follows from (1+r)^2-4r=(r-1)^2.
test('vacuum source reproduction',abs(rows[0]['ideal_pairs_s']/395287-1)<1e-5)
out=dict(checks=checks,all_pass=all(t['passed'] for t in checks),critical_density_m3=delta/(2*U0)*1e25,beam_CM_rms_eV=band,peak_rate_s=peak_rate,rows=rows,non_claims=['Fixed R pole, omitted dynamical self-energy and medium response','Prescribed gamma beams and messenger medium, no empirical viability','Energy acceptance is not trapping probability or stable inventory'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
