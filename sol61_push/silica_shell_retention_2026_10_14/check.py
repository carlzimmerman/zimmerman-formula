import json,math,sys,subprocess
from scipy.integrate import solve_ivp
from pathlib import Path
import mpmath as mp
from scipy.integrate import quad
from scipy.special import spherical_jn
from numpy.polynomial.legendre import leggauss
import numpy as np
hc=1.973269804e-7; hb=6.582119569e-16; alpha=1/137.035999084; ml=105658375.5
m=1.; MR=2.; mu=.002; g=1e-20; NA=6.02214076e23; rho=2201.; molar=.0600843
ac=.717e6; r0=3*alpha*hc/(5*ac)
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
xg,wg=leggauss(64); ug=(xg+1)/2; wg=wg/2; ug=ug*(1-ug)
def loop(r):
    if r<.1:return float(np.dot(wg,6*ug/(1+r*r*ug)))
    return 6/r**2*(1-4/(r*math.sqrt(4+r*r))*math.atanh(r/math.sqrt(4+r*r)))
def ratio(b,L):
    total=0.
    for left in np.arange(0,L,math.pi):
        total+=quad(lambda x:(3*spherical_jn(1,x)/x)**2*loop(x/b) if x else 1,left,min(left+math.pi,L),epsabs=1e-13)[0]
    return total/(3*math.pi/5)
components=[]
for name,Z,A,count in [('Si',14,28,1),('O',8,16,2)]:
    radius=r0*A**(1/3); b=ml*radius/hc; ec=ac*Z*(Z-1)/A**(1/3)
    r200=ratio(b,200); r400=ratio(b,400)
    ck('loop_radial_refinement',abs(r200-r400),2.1e-7)
    assert 1/(1+.5/b**2)<=r400<=1
    components.append(dict(element=name,model_A=A,number_per_formula=count,
        model_radius_fm=radius*1e15,Coulomb_energy_eV=ec,loop_ratio=r400))
weighted=sum(t['number_per_formula']*t['Coulomb_energy_eV']*t['loop_ratio'] for t in components)
number=rho/molar*NA; U=mu*g*weighted*number*hc**3/(2*m*MR*MR)
mp.mp.dps=80
an=mp.mpf('.02')/mp.mpf(str(hc)); mm=mp.mpf(1)
def pole(Uvalue,dmetres):
    uu=mp.mpf(str(Uvalue)); d=mp.mpf(str(dmetres))/mp.mpf('.02')
    z0=an*mp.sqrt(2*mm*uu)
    root_inf=mp.findroot(lambda z:z/mp.tan(z)+mp.sqrt(z0*z0-z*z),(mp.pi/2+mp.mpf('1e-20'),mp.pi-mp.mpf('1e-20')),solver='bisect',tol=mp.mpf('1e-65'),maxsteps=300)
    def equation(z):
        q=mp.sqrt(z0*z0-z*z); th=mp.tanh(q*d)
        outgoing=(1j*z-q*th)/(1-1j*z*th/q)
        return z/mp.tan(z)-outgoing
    zz=mp.findroot(equation,(root_inf-1j*mp.mpf('1e-6'),root_inf-1j*mp.mpf('2e-6')),tol=mp.mpf('1e-65'))
    E=zz*zz/(2*mm*an*an); width=-2*mp.im(E)
    assert width>0 and 0<mp.re(E)<uu
    ck('outgoing_resonance_root',float(abs(equation(zz))),1e-55)
    # An independent transfer-matrix residual uses explicit exp propagation.
    q=mp.sqrt(z0*z0-zz*zz)
    ua=mp.sin(zz); upa=zz*mp.cos(zz)
    ub=ua*mp.cosh(q*d)+upa/q*mp.sinh(q*d)
    upb=q*ua*mp.sinh(q*d)+upa*mp.cosh(q*d)
    ck('outer_outgoing_boundary',float(abs(upb-1j*zz*ub)/max(abs(upb),abs(ub))),1e-50)
    return dict(barrier_scale=Uvalue/U,wall_thickness_m=dmetres,
        resonance_real_energy_eV=float(mp.re(E)),width_eV=float(width),
        single_particle_tunneling_lifetime_s=float(mp.mpf(str(hb))/width),
        independent_pair_no_escape_probability_at_10ms=float(mp.exp(-2*width*mp.mpf('.01')/mp.mpf(str(hb)))))
rows=[pole(U,d) for d in [.001,.005,.01]]+[pole(U*factor,.01) for factor in [.5,2.]]
assert rows[0]['width_eV']>rows[1]['width_eV']>rows[2]['width_eV']
# Malitson dispersion equation, wavelength in micrometres, 20 C.
wavelength=1.239841984; l2=wavelength*wavelength
n2=1+sum(B*l2/(l2-C*C) for B,C in [(.6961663,.0684043),(.4079426,.1162414),(.8974794,9.896161)])
nopt=math.sqrt(n2); reflect=((nopt-1)/(nopt+1))**2
result=dict(material_assumptions=dict(density_kg_per_m3=rho,molar_mass_kg_per_mol=molar,
    nuclear_radius_coefficient_fm=r0*1e15,warning='Nuclear Coulomb contribution only; isotope and bulk homogeneity approximations'),
    nuclear_components=components,matched_Coulomb_energy_per_formula_eV=weighted,
    barrier_eV=U,formula_units_per_m3=number,optical_wavelength_um=wavelength,
    refractive_index=nopt,uncoated_normal_single_interface_reflectance=reflect,
    spherical_cavity_radius_m=.02,resonances=rows,checks=checks,passed=len(checks),
    scope='Ideal spherical finite shell and Coulomb-only photon portal; tunneling loss alone, no total lifetime or high-power optics certificate')
out=Path(sys.argv[1]); material=out.parent/'material.json'; prepared=out.parent/'preparation.json'
material.write_text(json.dumps(result,indent=2)+'\n')
subprocess.run([sys.executable,str(Path(__file__).with_name('prepare.py')),str(material),str(prepared)],check=True,capture_output=True,text=True)
prep=json.loads(prepared.read_text()); t=prep['perturbative_time_for_probability_001_s']; drive=prep['pair_drive_angular_frequency_per_s']
for row in rows:
    tau=row['single_particle_tunneling_lifetime_s']
    pweak=(drive*tau*(-math.expm1(-t/tau)))**2
    sol=solve_ivp(lambda tt,y:[-y[0]/tau-drive],(0,t),[0.],rtol=1e-10,atol=1e-13)
    ck('weak_driven_loss_ODE',abs(sol.y[0,-1]**2/pweak-1),1e-7)
    row['fixed_drive_loss_only_pair_probability']=pweak
ck('reference_mode_vs_5mm_pole',abs(prep['single_particle_energy_eV']/rows[1]['resonance_real_energy_eV']-1),2e-6)
result['preparation']=prep
result['preparation_time_s']=t
result['checks']=checks;result['passed']=len(checks)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
