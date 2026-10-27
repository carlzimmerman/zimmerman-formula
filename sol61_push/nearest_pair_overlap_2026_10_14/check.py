"""Ground and nearest p-p pair channels at fixed mediator resolvent energy."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.special import spherical_jn,spherical_kn,eval_legendre
from scipy.integrate import quad
from scipy.linalg import solve_banded,eigh
from numpy.polynomial.legendre import leggauss
prior=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())['preparation']
spectrum=json.loads(Path('sol61_push/confined_pair_spectrum_2026_10_14/run/results.json').read_text())
pulse=json.loads(Path('sol61_push/confined_pair_pulse_2026_10_14/run/results.json').read_text())
hc=1.973269804e-7; hb=6.582119569e-16; a=.02/hc; m=1.; MR=2.; h=.0005; lam=1e-6; mu=.002
F0=1e-20*(1e12/299792458.)/(1.602176634e-19/hc**3)/2
C=a*math.sqrt(2*MR*prior['below_mediator_gap_eV']); z=spectrum['z']
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
rows=[next(r for r in spectrum['levels'] if r['l']==l and r['n']==1) for l in [0,1]]
def radial(row):
    l=row['l']; k=row['x']; b=math.sqrt(z*z-k*k)
    def raw(x):
        x=np.asarray(x)
        return np.where(x<=1,x*spherical_jn(l,k*x),x*spherical_jn(l,k)*spherical_kn(l,b*np.maximum(x,1))/spherical_kn(l,b))
    norm=quad(lambda x:float(raw(x))**2,0,1,epsabs=1e-14)[0]+quad(lambda x:float(raw(x))**2,1,6,epsabs=1e-14)[0]
    return lambda x:raw(x)/math.sqrt(norm)
vs,vp=[radial(r) for r in rows]
c0=np.array([1,1,-1,-1]); c2=np.array([0,2,1,1])
def matrix(N,angular=192):
    dx=6/N; x=np.arange(1,N)*dx
    radial_density=np.array([vs(x)**2,vp(x)**2,vp(x)**2,vp(x)**2])/x
    us,ws=leggauss(angular)
    inside=x<=1+1e-12
    xin=x[inside]
    beam=np.exp(-200*xin[:,None]**2*(1-us[None,:]**2))
    sigma=np.zeros((4,4)); drive=np.zeros(4)
    for L,coef in [(0,c0),(2,c2)]:
        diag=2/dx**2+C*C+L*(L+1)/x**2
        band=np.zeros((3,len(x)));band[1]=diag;band[0,1:]=-1/dx**2;band[2,:-1]=-1/dx**2
        D=radial_density*coef[:,None]
        source=np.zeros_like(x);source[inside]=xin*(2*L+1)/2*(beam@(ws*eval_legendre(L,us)))
        source[np.isclose(x,1,atol=1e-12,rtol=0)]*=.5
        solved=solve_banded((1,1),band,np.column_stack((D.T,source)))
        sigma+=-MR*h*h/(2*math.pi*a)*(D@solved[:,:4])*dx/(2*L+1)
        drive+=-2*MR*a*a*h*F0*(D@solved[:,4])*dx/(2*L+1)
    contact=(lam-mu*mu/(4*MR*MR))/(4*math.pi*m*m*a**3)*(radial_density@radial_density.T)*dx*(np.outer(c0,c0)+np.outer(c2,c2)/5)
    energies=np.array([2*rows[0]['energy_eV']]+[2*rows[1]['energy_eV']]*3)
    H=np.diag(energies)+sigma+contact
    return H,drive,sigma
H,d,S=matrix(12000);Hf,df,Sf=matrix(24000);Ha,da,Sa=matrix(24000,256)
ck('radial_drive_relative',float(np.max(abs((d-df)/df))),5e-5)
ck('angular_drive_relative',float(np.max(abs((da-df)/df))),1e-7)
ck('radial_selfenergy_relative',float(np.max(abs(S-Sf)))/float(np.max(abs(Sf))),5e-5)
ck('ground_selfenergy_vs_parent_relative',abs(Sf[0,0]/prior['virtual_mediator_self_energy_eV']-1),5e-5)
ck('ground_drive_vs_parent_bare_relative',abs(df[0]*math.sqrt(prior['pair_component_residue'])/prior['pair_drive_matrix_element_eV']-1),5e-5)
ck('Hermitian_matrix_eV',float(np.max(abs(Ha-Ha.T))),1e-24)
e,U=eigh(Ha); coupling=U.T@da/hb
# Degenerate excited eigenvectors are arbitrary; aggregate populations are invariant.
T=pulse['pulse_duration_s'];ramp=pulse['ramp_s']
def f(t):
    if t<ramp:return .5*(1-math.cos(math.pi*t/ramp))
    if t>T-ramp:return .5*(1-math.cos(math.pi*(T-t)/ramp))
    return 1.
def propagate(steps):
    dt=T/steps; state=np.zeros(5,complex);state[0]=1
    H0=np.diag(np.r_[0,(e-e[0])/hb]); drive=np.zeros((5,5));drive[0,1:]=coupling;drive[1:,0]=coupling
    max_excited=0.
    for j in range(steps):
        vals,vec=eigh(H0+f((j+.5)*dt)*drive)
        state=vec@(np.exp(-1j*vals*dt)*(vec.T@state))
        max_excited=max(max_excited,float(np.sum(abs(state[2:])**2)))
    ck('unitary_norm',abs(float(np.vdot(state,state).real)-1),2e-10)
    return dict(steps=steps,ground_pair_probability=float(abs(state[1])**2),excited_eigenpair_probability=float(np.sum(abs(state[2:])**2)),maximum_sampled_excited_probability=max_excited)
p1=propagate(2000);p2=propagate(4000);p3=propagate(8000)
ck('propagation_ground_refinement',abs(p3['ground_pair_probability']-p2['ground_pair_probability']),2e-7)
ck('propagation_excited_refinement',abs(p3['excited_eigenpair_probability']-p2['excited_eigenpair_probability']),1e-14)
result=dict(scope='Lossless vacuum plus one pair in four channels; fixed-energy eliminated mediator; omits higher pair occupations and other orbitals',basis=['s0 s0','p0 p0','p+ p-','p- p+'],self_energy_matrix_eV=Sa.tolist(),optical_drive_bare_per_s=(da/hb).tolist(),eigenpair_energies_eV=e.tolist(),eigenpair_drives_per_s=coupling.tolist(),ground_pair_pp_admixture=float(np.sum(abs(U[1:,0])**2)),ground_eigenenergy_change_from_prior_eV=float(e[0]-prior['dressed_pair_excess_eV']),propagations=[p1,p2,p3],isolated_two_level_probability=math.sin(abs(coupling[0])*(T-ramp))**2,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
