"""Electron scalar-density wall and competing source decay, conditional model."""
import json,sys,math
from pathlib import Path
import mpmath as mp
from scipy.integrate import quad
mp.mp.dps=65; D=mp.mpf
prior=json.loads(Path('sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())
case=prior['reduced_muon_case'];mu=D(str(case['equal_width_mu_R_phi_eV']))
m=D('1e6');me=D('510998.95');mmu=D('105658375.5');ymu=D('.0002');alpha=1/D('137.035999084');hc=D('1.973269804e-7');ne=D('1e30');ns=ne*hc**3
checks=[]
def ck(n,v): checks.append({'name':n,'passed':bool(v)});assert v,n
def form(t):
 f=mp.asin(mp.sqrt(t))**2 if t<=1 else -(mp.log((1+mp.sqrt(1-1/t))/(1-mp.sqrt(1-1/t)))-1j*mp.pi)**2/4
 return 2*(t+(t-1)*f)/t**2
def widths(MR,ye):
 amp=ymu/mmu*form(MR**2/(4*mmu**2))+ye/me*form(MR**2/(4*me**2))
 gg=alpha**2*MR**3/(256*mp.pi**3)*abs(amp)**2
 ee=ye**2*MR/(8*mp.pi)*(1-4*me**2/MR**2)**D('1.5')
 pp=mu**2/(16*mp.pi*MR)*mp.sqrt(1-4*m*m/MR**2)
 total=gg+ee+pp
 return gg,ee,pp,total
MR0=2*m+D('2e-9')
J=mp.quad(lambda z:(1-z)**2*(1+z)/((1-z)**2+(MR0/me)**2*z),[0,.25,.5,1])/(8*mp.pi**2)
Jq=quad(lambda z:(1-z)**2*(1+z)/((1-z)**2+float(MR0/me)**2*z),0,1,epsabs=1e-12)[0]/(8*math.pi**2)
ck('electron moment independent quadrature',abs(float(J)/Jq-1)<1e-10)
rows=[]
for yabs in ['1e-8','1e-6','1e-5']:
 ye=-D(yabs) # mu*ye<0 gives a repulsive wall
 U=-mu*ye*ns/(2*m*MR0**2)
 mr=m*me/(m+me)
 asc=-mu*ye*mr/(4*mp.pi*m*MR0**2)
 ck('forward potential consistency '+yabs,abs((2*mp.pi*ns*asc/mr)/U-1)<D('1e-55'))
 gg,ee,pp,total=widths(MR0,ye)
 # Analytic wall/width tradeoff, eliminating electron coupling at fixed mu.
 relation=MR0/(8*mp.pi)*(1-4*me**2/MR0**2)**D('1.5')*(2*m*MR0**2*U/(mu*ns))**2
 ck('wall-decay elimination '+yabs,abs(relation/ee-1)<D('1e-55'))
 # Alternate assigned source mass: delta=U gives K=U/2 at vacuum center.
 Mt=2*m+U
 ggt,eet,ppt,tt=widths(Mt,ye)
 # U shifts by negligible MR difference, but retain it for barrier K check.
 Ut=-mu*ye*ns/(2*m*Mt**2);K=U/2
 exponent=2*D('.01')*mp.sqrt(2*m*(Ut-K))/hc
 rows.append({'ye':float(ye),'wall_eV':float(U),'delta_ae':float(J*ye*ye),
 'electron_width_eV':float(ee),'coherent_photon_width_eV':float(gg),
 'carrier_width_eV':float(pp),'carrier_branch_at_original_pole':float(pp/total),
 'original_pole_factor_4_gamma_gamma_gamma_phi_over_total2':float(4*gg*pp/total**2),
 'wall_over_original_K':float(U/D('1e-9')),
 'max_gravitational_drop_height_m':float(U*D(299792458)**2/(m*D('9.80665'))),
 'retuned_delta_eV':float(U),'retuned_carrier_width_eV':float(ppt),
 'retuned_carrier_branch_at_pole':float(ppt/tt),
 'retuned_pole_factor':float(4*ggt*ppt/tt**2),
 'retuned_total_width_over_wall':float(tt/Ut),
 'retuned_1cm_wall_WKB_exponent':float(exponent),
 'electron_Born_scattering_length_m':float(asc*hc)})
# Reconstruct unchanged muon-only photon and daughter widths.
gg,ee,pp,tt=widths(MR0,D(0))
ck('inherited photon width',abs(float(gg)/case['photon_width_eV']-1)<1e-12)
ck('inherited daughter width',abs(float(pp)/case['photon_width_eV']-1)<1e-12)
req=2*m*MR0**2*D('1e-9')/(mu*ns)
result={'all_pass':all(v['passed'] for v in checks),'checks':checks,'rows':rows,
 'scalar_electron_density_per_m3':float(ne),'assumption':'<ebar e>=electron number density; nonrelativistic homogenized medium',
 'ye_magnitude_wall_equals_original_K':float(req),'delta_ae_at_that_yukawa':float(J*req**2),
 'magnetic_moment_coefficient_delta_ae_over_ye2':float(J),
 'non_claims':['No material response, losses, thermal scattering, global allowed point or capture rate',
 'Pole factors use partial widths, not an integrated near-threshold line shape',
 'Retuned masses are assignments; not controllable knobs or measured relations']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
