"""Hypothetical added neutral resonance, finite bandwidth, and reciprocal loss."""
import json,math,sys
from pathlib import Path
from scipy.integrate import quad
from scipy.special import erfcx
checks=[]
def test(n,x):checks.append({'name':n,'passed':bool(x)});assert x,n
m=1e6;delta=2e-9;MR=2*m;partial=1e-12;hc=1.973269804e-7;hb=6.582119569e-16;c=299792458.;ev=1.602176634e-19
beta0=math.sqrt(delta/m);gg=math.sqrt(64*math.pi*partial/MR**3);mu=math.sqrt(16*math.pi*MR*partial/beta0)
MS=1e7;alpha=1/137.035999084;A=abs(gg)*12*math.pi*MS*MS/alpha
sigpeak=2*math.pi/MR**2*hc**2
# Hold mass prefactors constant at 2m, but retain threshold phase space and running phi width.
def ratio(eps):return math.sqrt(max(0.,eps)/delta)
def denom(eps):return 4*((eps-delta)/partial)**2+(1+ratio(eps))**2
def sigma(eps):return sigpeak*4*ratio(eps)/denom(eps)
def annih(eps):return 4*c*sigpeak/beta0*4/denom(eps)
test('peak width identity',math.isclose(sigma(delta),sigpeak,rel_tol=1e-14))
test('photon width',math.isclose(gg*gg*MR**3/(64*math.pi),partial,rel_tol=1e-14))
test('carrier width',math.isclose(mu*mu*beta0/(16*math.pi*MR),partial,rel_tol=1e-14))
# theta substitution resolves widths without subtracting MeV-valued masses.
def integrate(fn,lo,hi,tol=1e-9):
 a=math.atan((lo-delta)/partial);b=math.atan((hi-delta)/partial)
 return quad(lambda th:fn(delta+partial*math.tan(th))*partial/(math.cos(th)**2),a,b,epsabs=1e-300,epsrel=tol,points=[0.] if a<0<b else None,limit=300)[0]
rows=[];U=1.9208763923634617e-9
for width in [1e-12,1e-10,1e-9]:
 norm=math.sqrt(2*math.pi)*width
 pdf=lambda eps:math.exp(-.5*((eps-delta)/width)**2)/norm
 avg=integrate(lambda e:sigma(e)*pdf(e),0,delta+10*width)
 avg2=integrate(lambda e:sigma(e)*pdf(e),0,delta+10*width,1e-11)
 test('bandwidth quadrature '+str(width),abs(avg/avg2-1)<1e-8)
 trapped=integrate(lambda e:sigma(e)*pdf(e),0,min(2*U,delta+10*width))
 # Infinite-range constant-width Voigt average is an independent normalization control.
 exact=math.sqrt(math.pi/2)*partial/width*erfcx(partial/(math.sqrt(2)*width))
 direct=quad(lambda th:math.exp(-.5*(partial*math.tan(th)/width)**2)*partial/norm,-math.pi/2,math.pi/2,epsabs=1e-13,epsrel=1e-10,limit=300)[0]
 test('Voigt '+str(width),abs(direct/exact-1)<1e-8)
 ng=1e6/(1e-6*m*ev*c);volume=2e-9;R=2*c*ng*ng*avg
 # Isotropic monoenergetic carrier shell K=delta/2; relative excess spans [0,delta].
 aavg=integrate(annih,0,delta)/delta
 neq=math.sqrt(R/aavg)
 rows.append({'CM_energy_rms_eV':width,'averaged_sigma_m2':avg,'ideal_pairs_s_inv':R*volume,'fraction_produced_below_wall_energy':trapped/avg,'monoenergetic_isotropic_annihilation_a_m3_s':aavg,'diagnostic_equilibrium_particles_per_sign':neq*volume,'constant_width_average_over_peak':exact})
for e in [delta/10,delta,delta*2]:
 test('reciprocal rate '+str(e),math.isclose(annih(e),4*c*sigma(e)/math.sqrt(e/m),rel_tol=1e-12))
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'parameters':{'m_eV':m,'resonance_excess_eV':delta,'partial_width_each_eV':partial,'total_lifetime_s':hb/(2*partial),'g_R_gamma_eVminus1':gg,'mu_R_phi_eV':mu,'charged_messenger_A_eV':A,'peak_sigma_m2':sigpeak,'C_off_resonance_added_magnitude_eVminus2':abs(gg*mu/(4*MR*MR)),'static_quartic_attraction_magnitude':mu*mu/(2*MR*MR)},'rows':rows,'non_claims':['Hypothetical tuned resonance and prescribed beams/wall','No stable inventory or full phase-space kinetic evolution','Reciprocal loss diagnostic assumes isotropic single-energy particles, not evolved products']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
