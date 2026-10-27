"""Necessary tree partial-wave screen for one chosen scalar completion."""
import json,math,sys
from pathlib import Path
import sympy as s
checks=[]
def test(name,x):
 checks.append(dict(name=name,passed=bool(x)))
 assert x,name
alpha,g,M,A,lam=s.symbols('alpha g M A lam',positive=True)
x=s.symbols('x',real=True)
a0=s.integrate(-lam,(x,-1,1))/(32*s.pi)
test('distinguishable contact partial wave',s.simplify(a0+lam/(16*s.pi))==0)
Areq=12*s.pi*g*M*M/alpha
lreq=s.simplify(Areq**2/(2*M*M))
test('minimal square quartic at fixed photon coupling',s.simplify(lreq-72*s.pi**2*g*g*M*M/alpha**2)==0)
Mmax=alpha/(3*s.sqrt(s.pi)*g)
test('necessary ceiling saturation',s.simplify(lreq.subs(M,Mmax)-8*s.pi)==0)
av=1/137.035999084;gv=5.0132565492620005e-15
ceiling=av/(3*math.sqrt(math.pi)*gv)
rows=[]
for GeV in [100.,200.,300.,520.,600.,1000.]:
 mass=GeV*1e9;ac=12*math.pi*gv*mass*mass/av;l=ac*ac/(2*mass*mass)
 gcap=av/(3*math.sqrt(math.pi)*mass)
 test('g cap reciprocity '+str(GeV),math.isclose(gcap/gv,ceiling/mass,rel_tol=1e-12))
 rows.append(dict(messenger_mass_GeV=GeV,required_A_over_M=ac/mass,required_minimum_lambda_RS=l,abs_contact_a0=l/(16*math.pi),passes_necessary_tree_screen=l<=8*math.pi,max_photon_width_over_original=(gcap/gv)**2))
# Lower photon-width choices with equal gamma and daughter partial widths.
# Broad-source isolated-line area then scales with the common partial width.
diagnostic=[]
for GeV in [600.,1000.]:
 mass=GeV*1e9
 for lv in [.1,1.]:
  ac=math.sqrt(2*lv)*mass;gg=av*ac/(12*math.pi*mass*mass);r=(gg/gv)**2
  mu=47.41245315244753*math.sqrt(r)
  h_eff=1-mu*ac/(2e6)**2 # leading static tadpole contribution with positive mu*A
  diagnostic.append(dict(messenger_mass_GeV=GeV,lambda_RS=lv,gamma_partial_width_eV=1e-12*r,mu_R_phi_eV=mu,equal_width_broad_spectrum_area_over_original=r,h_effective_static=h_eff,wall_density_for_old_U_m3=1e25*(mass/1e7)/h_eff))
out=dict(checks=checks,all_pass=all(t['passed'] for t in checks),fixed_photon_coupling_eVminus1=gv,necessary_tree_mass_ceiling_GeV=ceiling/1e9,CMS_reference_right_stau_limit_GeV=520,rows=rows,reduced_width_diagnostics=diagnostic,non_claims=['CMS limit requires explicit singlet embedding, stable lifetime and matching signal efficiencies','No blanket exclusion below the simulated range or all charged particles','Tree screen is necessary not sufficient for controlled perturbation theory','Lower width rows are coupled scaling diagnostics, not complete production or material solutions'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
