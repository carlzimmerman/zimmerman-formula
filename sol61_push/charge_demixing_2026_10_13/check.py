"""Leading two-component threshold matching and homogeneous stability audit."""
import json, math, sys
from pathlib import Path
import sympy as s
import numpy as np
checks=[]
def test(name,value):
    checks.append({'name':name,'passed':bool(value)})
    assert value,name
z=s.symbols('z',nonzero=True); p,pb,a,ab=s.symbols('p pb a ab'); m,M,g,lr=s.symbols('m M g lr',positive=True)
# Phi=(p z + anti* /z)/sqrt(2m); barPhi=(p*/z+anti z)/sqrt(2m).
phi=(p*z+ab/z)/s.sqrt(2*m); phib=(pb/z+a*z)/s.sqrt(2*m)
avg=s.expand((phi*phib)**2).coeff(z,0)
expect=(p*p*pb*pb+a*a*ab*ab+4*p*pb*a*ab)/(4*m*m)
test('secular quartic multiplicities',s.simplify(avg-expect)==0)
D=M*M-4*m*m; lam=lr+g*g/D
# Invert massive source on harmonics of Phi²: frequencies +/-2m and zero.
source_product=s.expand(phi**2)
exchange=0
for freq in [-2,0,2]:
    term=source_product.coeff(z,freq)
    conj=term.xreplace({p:pb,pb:p,a:ab,ab:a})
    exchange+=g*g*term*conj/(M*M-freq*freq*m*m)
energy=s.expand(lam*avg-exchange)
gself=s.simplify(2*energy.coeff(p,2).coeff(pb,2))
gcross=s.simplify(energy.coeff(p,1).coeff(pb,1).coeff(a,1).coeff(ab,1))
test('self threshold matching',s.simplify(gself-lr/(2*m*m))==0)
test('cross threshold matching',s.simplify(gcross-(lam-g*g/M**2)/m**2)==0)
diff=s.simplify(gcross-gself)
test('positive difference decomposition',s.simplify(diff-(lr/(2*m*m)+4*g*g/(M*M*D)))==0)
# Independent 4x4 linearized GP spectrum, including controls on both sides of miscibility.
rows=[]
for ratio in [.5,1.,2.,2.0002]:
  for k in [.2,.8,1.4,2.1,3.]:
    eps=k*k/2; B=np.array([[1.,ratio],[ratio,1.]])
    L=np.block([[eps*np.eye(2)+B,B],[-B,-eps*np.eye(2)-B]])
    vals=np.linalg.eigvals(L)
    target=[eps*(eps+2*(1+ratio)),eps*(eps+2*(1-ratio))]
    err=max(min(abs(v*v-t) for t in target) for v in vals)
    test('BdG ratio %g k %g'%(ratio,k),err<1e-10)
    rows.append({'ratio':ratio,'k':k,'growth':float(max(vals.imag)),'squared_eigenvalue_error':float(err)})
# Benchmark matching parameters close to earlier weak source coupling.
mv=1e6; Mv=2000005.; gv=math.sqrt(.002); ltot=1e-6
Dv=Mv*Mv-4*mv*mv; lrep=ltot-gv*gv/Dv
G=lrep/(2*mv*mv); H=(ltot-gv*gv/Mv**2)/(mv*mv); dg=H-G
n=1e12; hb=6.582119569e-16; hc=1.973269804e-7
qmax=math.sqrt(2*mv*n*dg); gamma=n*dg/hb
Lcrit=2*math.pi*hc/math.sqrt(4*mv*n*dg)
boxes=[]
for size in [.1,1.,10.]:
    k=2*math.pi*hc/(size*1e-6); eps=k*k/(2*mv)
    boxes.append({'L_um':size,'first_mode_unstable':bool(eps<2*n*dg),'first_mode_growth_s_inv':math.sqrt(max(0,eps*(2*n*dg-eps)))/hb})
Ccrit=math.sqrt(math.pi*dg/(2*mv*mv))
bench={'m_eV':mv,'M_eV':Mv,'cubic_g_eV':gv,'lambda_tot':ltot,'lambda_rep':lrep,'g_self_eVminus2':G,'g_cross_eVminus2':H,'ratio':H/G,'density_per_sign_eV3':n,'max_growth_s_inv':gamma,'fastest_wavelength_m':2*math.pi*hc/qmax,'periodic_box_critical_L_m':Lcrit,'chemical_potential_over_detuning':n*(G+H)/(Mv-2*mv),'C_equal_growth_annihilation_eVminus2':Ccrit,'growth_to_annihilation_at_C_1e_minus19':dg/(2*1e-38*mv*mv/math.pi),'boxes':boxes}
test('benchmark repulsive and immiscible',H>G>0)
test('small box control',not boxes[0]['first_mode_unstable'] and boxes[1]['first_mode_unstable'])
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'secular_quartic':str(avg),'g_self':str(gself),'g_cross':str(gcross),'difference':str(diff),'spectrum_cases':rows,'benchmark':bench,'non_claims':['Assumed coherent condensates and external confinement','No nonlinear domains, boundary loss, finite temperature, production or experimental observation','Threshold matching omits derivative and loop corrections']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(bench,indent=2))
