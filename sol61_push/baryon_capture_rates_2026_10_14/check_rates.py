"""BCR-001 conditional rates in specified one-body nuclear and atomic models."""
import json
from pathlib import Path
import sys
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
from spin import gamma,g5,PR,eye,g0,slash,adjoint,dot,spinor

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def ck(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
    if not ok:raise AssertionError(name)
mn=.93956542194;mp=.93827208943;me=.00051099895069;md=1.875612945
mc=mn-.0005;ms=.001;alpha=.0072973525643;GF=1.1663785e-5;V=.974;ga=1.27
conversion=.3893793721e-27*29979245800.;hb=6.582119569e-25;yr=31557600.
bd=mn+mp-md;mu_np=mn*mp/(mn+mp);g=np.sqrt(2*mu_np*bd)
share=mp/(mn+mp)
def momentum(W,m1,m2):return np.sqrt(max(0.,(W-m1-m2)*(W+m1+m2)*(W-m1+m2)*(W+m1-m2)))/(2*W)

triplet=np.array([[1,0,0,0],[0,1/np.sqrt(2),1/np.sqrt(2),0],[0,0,0,1]])
ck('independent spin triplet sum',abs(np.sum(abs(triplet)**2)/4-.75)<1e-14)
def zr(q):return np.sqrt(8*np.pi*g)/(q*q+g*g)

wells=[]
for radius in [1.,1.5,2.]:
    R=radius/.1973269804
    z=brentq(lambda z:z/np.tan(z)+g*R,np.pi/2+1e-10,np.pi-1e-10)
    a=z/R
    norm=1/np.sqrt(R/2-np.sin(2*z)/(4*a)+np.sin(z)**2/(2*g))
    def radial(r,a=a,R=R,norm=norm):return norm*np.sin(a*r) if r<R else norm*np.sin(a*R)*np.exp(-g*(r-R))
    ck('radial normalization %g'%radius,abs(quad(lambda r:radial(r)**2,0,R,epsabs=1e-12)[0]+quad(lambda r:radial(r)**2,R,np.inf,epsabs=1e-12)[0]-1)<1e-10)
    ck('derivative continuity %g'%radius,abs(a/np.tan(a*R)+g)<1e-12)
    def wf(q,a=a,R=R,norm=norm):
        q=np.asarray(q)
        # All sampled q are far from a. q=0 uses its analytic limit.
        qs=np.where(abs(q)<1e-9,1.,q)
        interior=(np.sin((a-qs)*R)/(a-qs)-np.sin((a+qs)*R)/(a+qs))/2
        exterior=np.sin(a*R)*(g*np.sin(qs*R)+qs*np.cos(qs*R))/(g*g+qs*qs)
        general=np.sqrt(4*np.pi)*norm*(interior+exterior)/qs
        lim=np.sqrt(4*np.pi)*norm*(np.sin(a*R)/a**2-R*np.cos(a*R)/a+np.sin(a*R)*(R/g+1/g**2))
        return np.where(abs(q)<1e-9,lim,general)
    for q in [0.,.0007,.005,.02]:
        numerical=np.sqrt(4*np.pi)*(quad(lambda r:r*radial(r)*np.sinc(q*r/np.pi),0,R,epsabs=1e-10)[0]+quad(lambda r:r*radial(r)*np.sinc(q*r/np.pi),R,np.inf,epsabs=1e-10)[0])
        ck('independent Fourier integral %g %g'%(radius,q),abs(float(wf(q))/numerical-1)<1e-9)
    wells.append(dict(radius_fm=radius,depth_MeV=(a*a+g*g)/(2*mu_np)*1000,wf=wf))

capture=[]
for v in [0.,1e-5,1e-4,1e-3,1e-2]:
    ki=mc*mp/(mc+mp)*v
    Ec=np.sqrt(mc*mc+ki*ki);Ep=np.sqrt(mp*mp+ki*ki);W=Ec+Ep
    pf=momentum(W,md,ms)
    pref=3*pf*md/(32*np.pi*W)*mc*mp/(Ec*Ep)
    A=ki*ki+share*share*pf*pf+g*g;B=2*ki*share*pf
    analytic=pref*8*np.pi*g/(A*A-B*B)
    for label,func in [('zero_range',zr)]+[('well_%gfm'%w['radius_fm'],w['wf']) for w in wells]:
        vals=[]
        for count in [64,128]:
            z,weights=leggauss(count);q=np.sqrt(np.maximum(0.,ki*ki+share*share*pf*pf-2*ki*share*pf*z))
            vals.append(pref*np.dot(weights,func(q)**2)/2)
        ck('capture quadrature %s %g'%(label,v),vals[1]>0 and abs(vals[0]/vals[1]-1)<1e-9)
        if label=='zero_range':ck('closed angular integral %g'%v,abs(vals[1]/analytic-1)<1e-12)
        capture.append(dict(model=label,v_over_c=v,sigma_v_over_y2_GeVminus2=vals[1],sigma_v_over_y2_cm3_s=vals[1]*conversion))

# Four-spin average for unpolarized hydrogen, no hyperfine population model.
mH=mp+me;reduced=mp*me/mH;psi2=(alpha*reduced)**3/np.pi
pe=np.array([me,0.,0.,0.]);pp=np.array([mp,0.,0.,0.])
lepton=[(1 if i==0 else -1)*gamma[i]@(eye-g5) for i in range(4)]
def weak_matrix(mass_chi,pchi,pnu,propagator):
    hadron=[propagator@gamma[i]@(eye-ga*g5) for i in range(4)]
    tr=0j
    for i in range(4):
        for j in range(4):
            H=np.trace((slash(pchi)+mass_chi*eye)@hadron[i]@(slash(pp)+mp*eye)@adjoint(hadron[j]))
            L=np.trace(slash(pnu)@lepton[i]@(slash(pe)+me*eye)@adjoint(lepton[j]))
            tr+=H*L
    direct=0.
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    amp=sum((spinor(pchi,mass_chi,c).conj()@g0@hadron[i]@spinor(pp,mp,a))*(spinor(pnu,0.,d).conj()@g0@lepton[i]@spinor(pe,me,b)) for i in range(4))
                    direct+=abs(amp)**2
    ck('weak trace spin %g %g'%(mass_chi,pnu[0]),abs(tr.imag)<1e-12*max(1,abs(tr.real)) and abs(tr.real-direct)<1e-10*max(1,abs(tr.real)))
    # Initial proton/electron spin average, Fermi coupling, initial-atom projection.
    return tr.real/4*(GF*V)**2/2 *mH/(2*mp*me)*psi2

bench=[]
for release in [.0001,.0003,.0005]:
    mass=mH-release;p=(mH*mH-mass*mass)/(2*mH)
    pn=np.array([p,0.,0.,p]);pc=np.array([np.sqrt(mass*mass+p*p),0.,0.,-p])
    amp2=weak_matrix(mass,pc,pn,eye)
    width=p*amp2/(8*np.pi*mH*mH)
    approx=psi2*(GF*V)**2/(2*np.pi)*(1+3*ga*ga)*release**2
    ck('known small Q EC normalization %g'%release,abs(width/approx-1)<.005)
    bench.append(dict(Q_MeV=release*1000,width_over_theta2_GeV=width,leading_formula_GeV=approx,ratio=width/approx))

hydrogen=[]
for scalar in [.0006,.001,.002,.005]:
    W=mH+scalar;p=(W*W-mc*mc)/(2*W)
    pn=np.array([p,0.,0.,p]);pc=np.array([np.sqrt(mc*mc+p*p),0.,0.,-p])
    ps=np.array([scalar,0.,0.,0.]);Q=pc-ps
    prop=PR@(slash(Q)+mn*eye)/(dot(Q,Q)-mn*mn)
    amp2=weak_matrix(mc,pc,pn,prop)
    sv=p*amp2/(16*np.pi*W*mH*scalar)
    delta=mn+scalar-mc;release=W-mc
    static=psi2*(GF*V)**2/(2*np.pi)*(1+3*ga*ga)*release**2/(8*scalar*delta**2)
    ck('H absorption static normalization %g'%scalar,sv>0 and abs(sv/static-1)<.02)
    hydrogen.append(dict(mS_MeV=scalar*1000,Q_MeV=release*1000,neutrino_energy_MeV=p*1000,sigma_v_over_y2_cm3_s=sv*conversion,static_ratio=sv/static))

ch,sc,pr,el,de,bh=sp.symbols('chi S p e d B_H')
Q1=ch+pr-de-sc;Q2=pr+el-bh+sc-ch
ck('catalytic energy identity',sp.expand(Q1+Q2-(2*pr+el-bh-de))==0)
binding_H=13.6e-9
q1=mc+mp-md-ms;q2=mp+me-binding_H+ms-mc;net=2*mp+me-binding_H-md
ck('numeric catalytic energy sum',abs(q1+q2-net)<1e-15)
ck('H absorption open for stable chi',mc<mp+me-binding_H+ms and q2>0)
ck('H alone dark decay closed',mp+me-binding_H<mc+ms)

base=next(x for x in capture if x['model']=='zero_range' and x['v_over_c']==0)['sigma_v_over_y2_cm3_s']
sample_y=1.44e-11
rates=[]
for density in [1.,1e6,6.7e22]:
    rates.append(dict(proton_density_cmminus3=density,half_conversion_years=np.log(2)/(density*base*sample_y**2)/yr))
needed=np.sqrt(np.log(2)/(6.7e22*base*yr))
result=dict(status='conditional one-body nuclear and atomic rates verified',assertions=len(checks),capture=capture,square_wells=[{k:v for k,v in w.items() if k!='wf'} for w in wells],atomic_mixing_benchmarks=bench,hydrogen_absorption=hydrogen,energy_ledger=dict(capture_Q_MeV=q1*1000,H_absorption_Q_MeV=q2*1000,net_pep_Q_MeV=net*1000),sample_y=sample_y,assigned_density_examples=rates,y_for_half_conversion_1year_at_assigned_solid_density=needed,scope='Defined nuclear potentials, leading one-body current and atomic1s impulse approximation only. Not matched physical rates, prepared cycle, observed cold identity or experimental viability.')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
