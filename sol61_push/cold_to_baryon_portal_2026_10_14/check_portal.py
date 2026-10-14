"""CBP-001: conditional baryon transfer with explicit spin and phase space."""
import json
from pathlib import Path
import sys
import numpy as np
import sympy as sy
from numpy.polynomial.legendre import leggauss

OUT=Path(sys.argv[1]); OUT.mkdir(parents=True,exist_ok=False)
checks=[]
def check(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
    if not ok: raise AssertionError(name)
def exact(name,expression): check(name,sy.simplify(expression)==0)

# Rational charge vectors: (hypercharge, dark charge, generalized baryon number).
R=sy.Rational
charge={'chi':sy.Matrix([0,1,1]),'chic':sy.Matrix([0,-1,-1]),
        'S':sy.Matrix([0,1,0]),'Sd':sy.Matrix([0,-1,0]),
        'uc':sy.Matrix([-R(2,3),0,-R(1,3)]),
        'dc':sy.Matrix([R(1,3),0,-R(1,3)]),
        'N':sy.Matrix([0,0,1]),'Nc':sy.Matrix([0,0,-1]),
        'Phi':sy.Matrix([R(1,3),0,R(2,3)]),
        'Phid':sy.Matrix([-R(1,3),0,-R(2,3)]),
        'nbar':sy.Matrix([0,0,-1])}
vertices=[['Phi','uc','dc'],['Phid','N','dc'],['Sd','chi','Nc'],
          ['N','Nc'],['chi','chic'],['Sd','chi','uc','dc','dc'],['Sd','nbar','chi']]
for i,fields in enumerate(vertices):
    check('vertex charges %d'%i,sum((charge[f] for f in fields),sy.zeros(3,1))==sy.zeros(3,1))
exact('dimension7 operator',1+4*R(3,2)-7)
exact('tree coefficient dimension',-2-1+3) # 1/(Mphi^2 MN)
# Species order chi, photon, neutron, S, proton, electron, antineutrino.
source=sy.Matrix([-1,-1,1,1,0,0,0]); beta_source=sy.Matrix([0,0,-1,0,1,1,1])
for name,weights in [('dark',[1,0,0,1,0,0,0]),('baryon',[1,0,1,0,1,0,0]),('electric',[0,0,0,0,1,-1,0]),('lepton',[0,0,0,0,0,1,-1])]:
    exact(name+' transfer conservation',sy.Matrix(weights).dot(source))
    exact(name+' beta conservation',sy.Matrix(weights).dot(beta_source))
M,m,ms=sy.symbols('M m ms',positive=True)
en=(M*M+m*m-ms*ms)/(2*M); es=(M*M-m*m+ms*ms)/(2*M)
psq=((M-m-ms)*(M+m+ms)*(M-m+ms)*(M+m-ms))/(4*M*M)
exact('two body energy',en+es-M)
exact('two body neutron shell',en*en-psq-m*m)
exact('two body scalar shell',es*es-psq-ms*ms)
eg=sy.symbols('eg',positive=True)
exact('photon lab threshold',(M*M+2*M*eg-(m+ms)**2).subs(eg,((m+ms)**2-M*M)/(2*M)))

I2=np.eye(2,dtype=complex); Z2=np.zeros((2,2),complex)
pauli=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.array([[1,0],[0,-1]],complex)]
g0=np.diag([1.,1.,-1.,-1.]).astype(complex)
gam=[g0]+[np.block([[Z2,s],[-s,Z2]]) for s in pauli]
g5=1j*gam[0]@gam[1]@gam[2]@gam[3]
PL=(np.eye(4)-g5)/2
metric=np.diag([1,-1,-1,-1])
for i in range(4):
    for j in range(4): check('Clifford %d %d'%(i,j),np.max(abs(gam[i]@gam[j]+gam[j]@gam[i]-2*metric[i,j]*np.eye(4)))<1e-14)
def slash(p): return p[0]*gam[0]-sum((p[i]*gam[i] for i in range(1,4)),np.zeros((4,4),complex))
def dot(p,q): return p[0]*q[0]-np.dot(p[1:],q[1:])
def bar(op): return g0@op.conj().T@g0
def spinors(p,mass):
    smat=sum((p[i+1]*pauli[i] for i in range(3)),np.zeros((2,2),complex))
    return [np.sqrt(p[0]+mass)*np.concatenate((I2[:,j],smat@I2[:,j]/(p[0]+mass))) for j in range(2)]
def trace_sq(op,pin,min_,pout,mout):
    return np.trace((slash(pout)+mout*np.eye(4))@op@(slash(pin)+min_*np.eye(4))@bar(op))
def spin_sq(op,pin,min_,pout,mout):
    return sum(abs(uf.conj()@g0@op@ui)**2 for uf in spinors(pout,mout) for ui in spinors(pin,min_))

mn=.93956542194; mp=.93827208943; me=.00051099895069
alpha=.0072973525643; hb=6.582119569e-25
mu=-1.91304273*np.sqrt(4*np.pi*alpha)/(2*mp)
gev2_cm2=.3893793721e-27

def momentum(M,m,s):
    return np.sqrt(max(0.,(M-m-s)*(M+m+s)*(M-m+s)*(M+m-s)))/(2*M)

decays=[]
for qrelease in [1e-9,1e-6,.001,.01]:
    s=.1; parent=mn+s+qrelease; mom=momentum(parent,mn,s)
    pn=np.array([np.sqrt(mn*mn+mom*mom),0,0,mom]); pi=np.array([parent,0,0,0.])
    tr=trace_sq(PL,pi,parent,pn,mn)/2
    direct=spin_sq(PL,pi,parent,pn,mn)/2
    expected=(parent*parent+mn*mn-s*s)/2
    check('decay trace and spin %g'%qrelease,abs(tr-expected)<1e-12 and abs(direct-expected)<1e-12)
    width=mom*expected/(8*np.pi*parent*parent)
    check('decay width positive %g'%qrelease,width>0)
    decays.append(dict(Q_GeV=qrelease,mchi_GeV=parent,mS_GeV=s,p_GeV=mom,neutron_kinetic_GeV=pn[0]-mn,scalar_kinetic_GeV=np.sqrt(s*s+mom*mom)-s,width_over_y2_GeV=width,neutron_mass_fraction=mn/parent))

mchi=mn-.0005; mS=.001
threshold=((mn+mS)**2-mchi*mchi)/(2*mchi)
check('carrier neutron decay closed',mchi<mn+mS)
check('carrier beta-assisted decay closed',mchi<mp+me+mS)
check('free neutron dark decay closed',mn<mchi+mS)
check('proton final dark masses above proton',mp<mchi+mS)

def cm_kin(egamma,z):
    s=mchi*mchi+2*mchi*egamma; root=np.sqrt(s)
    ki=(s-mchi*mchi)/(2*root); pf=momentum(root,mn,mS)
    pin=np.array([(s+mchi*mchi)/(2*root),0.,0.,-ki])
    photon=np.array([ki,0.,0.,ki])
    pn=np.array([(s+mn*mn-mS*mS)/(2*root),pf*np.sqrt(max(0,1-z*z)),0.,pf*z])
    spectator=np.array([(s-mn*mn+mS*mS)/(2*root),-pn[1],0.,-pn[3]])
    return s,ki,pf,pin,photon,pn,spectator

def amplitude_operator(photon,pn,polarization):
    # Q is the outgoing neutron before absorption of the incoming photon.
    Q=pn-photon
    pauli_vertex=.5j*(slash(polarization)@slash(photon)-slash(photon)@slash(polarization))
    return mu*pauli_vertex@(slash(Q)+mn*np.eye(4))@PL/(dot(Q,Q)-mn*mn)

def squared(egamma,z,audit=False):
    s,ki,pf,pin,k,pn,ps=cm_kin(egamma,z)
    total=0.
    for eps in [np.array([0.,1.,0.,0.]),np.array([0.,0.,1.,0.])]:
        op=amplitude_operator(k,pn,eps); tr=trace_sq(op,pin,mchi,pn,mn)
        if audit:
            direct=spin_sq(op,pin,mchi,pn,mn)
            check('spin trace %g %g %s'%(egamma,z,str(eps)),abs(tr.imag)<1e-14 and abs(tr.real-direct)<1e-12*max(1,abs(tr)))
        total+=tr.real
    if audit:
        check('Ward %g %g'%(egamma,z),np.max(abs(amplitude_operator(k,pn,k)))<1e-14)
        check('on shell and energy %g %g'%(egamma,z),max(abs(dot(pin,pin)-mchi*mchi),abs(dot(pn,pn)-mn*mn),abs(dot(ps,ps)-mS*mS),max(abs(pin+k-pn-ps)))<1e-12)
    return total/4 # initial chi spin and photon polarization averages

def cross_section(egamma,nodes):
    if egamma<=threshold*(1+2e-15): return 0.
    s,ki,pf,*_=cm_kin(egamma,0.)
    z,w=leggauss(nodes)
    return pf/(32*np.pi*s*ki)*sum(wi*squared(egamma,zi) for zi,wi in zip(z,w))

scattering=[]; max_quad_error=0.
for ratio in [.9,1.,1.001,1.01,1.1,2.,5.,10.]:
    egamma=ratio*threshold
    c64=cross_section(egamma,64); c128=cross_section(egamma,128)
    if ratio<=1:
        check('closed photon channel %g'%ratio,c64==0 and c128==0)
    else:
        rel=abs(c64-c128)/c128; max_quad_error=max(max_quad_error,rel)
        check('photon positive converged %g'%ratio,c128>0 and rel<1e-8)
        for z in [-.9,0.,.9]: squared(egamma,z,True)
    scattering.append(dict(photon_over_threshold=ratio,photon_MeV=1000*egamma,sigma_over_y2_GeVminus2=c128,sigma_over_y2_cm2=c128*gev2_cm2))

beta_had=.0144; benchmarks=[]
for heavy in [1e3,1e4,1e5]:
    y=beta_had/heavy**3
    for lifetime in [1.,1e9*31557600.]:
        width=decays[1]['width_over_y2_GeV']
        needed=np.sqrt(hb/(width*lifetime))
        check('lifetime reconstruction %g %g'%(heavy,lifetime),abs(hb/(needed*needed*width)/lifetime-1)<1e-12)
    sigma=scattering[-3]['sigma_over_y2_cm2']*y*y # twice threshold
    fluence=np.log(2)/sigma
    benchmarks.append(dict(MPhi_GeV=heavy,MN_GeV=heavy,assigned_y=y,spontaneous_witness_lifetime_s=hb/(y*y*decays[1]['width_over_y2_GeV']),photon_twice_threshold_sigma_cm2=sigma,fluence_for_half_cmminus2=fluence,photon_energy_fluence_J_cmminus2=fluence*2*threshold*1.602176634e-10))

# Curvature-mass gate: show the weak channel that survives a neutron-only gate.
parent=decays[1]['mchi_GeV']; base=.1
neutron_mass_threshold=parent-mn; complete_mass_threshold=parent-mp-me
check('neutron-only gate insufficient',complete_mass_threshold>neutron_mass_threshold)
G=6.67430e-11; c=299792458.; solar=1.98847e30; hbc=1.973269804e-16 # GeV m
rh_m=2*G*10*solar/c**2; rh_natural=rh_m/hbc
gb=12/rh_natural**4
delta_ms2=complete_mass_threshold**2-base**2
cutoff=np.sqrt(gb/delta_ms2)
curvature=dict(source_mass_solar=10,rh_m=rh_m,GB_GeV4=gb,required_mass_squared_shift_GeV2=delta_ms2,required_LambdaC_GeV_at_kappa1=cutoff,curvature_energy_GeV=gb**.25,cutoff_over_curvature_energy=cutoff/gb**.25,neutron_only_mass_threshold_GeV=neutron_mass_threshold,complete_weak_threshold_GeV=complete_mass_threshold)
check('simple order1 curvature gate outside derivative hierarchy',cutoff<gb**.25*1e-10)

result=dict(status='conditional EFT construction verified in stated scope',assertions=len(checks),stable_photon_witness=dict(mchi_GeV=mchi,mS_GeV=mS,threshold_MeV=threshold*1000,mu_neutron_GeVminus1=mu,minimum_total_rest_mass_in_beta_channel_GeV=mp+me+mS,beta_release_MeV=(mn-mp-me)*1000,net_baryon_source='pre-existing hidden baryon number carried by chi'),decays=decays,scattering=scattering,max_64_128_quadrature_relative_error=max_quad_error,heavy_mediator_benchmarks=benchmarks,curvature_mass_gate=curvature,non_claim='No physical carrier identification, full medium/portal completion, experimental viability, asymmetry generation or practical production shown.')
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
