"""Finite-amplitude Y20 linear-coordinate Cauchy seeds; NO evolution.

K labels the prescribed linear coordinate only. No charge adjustment, DC
dressing, nonlinear normal-mode frequency or stationary monopole is inserted.
"""
from pathlib import Path
import hashlib,json,math,resource,struct,sys
import numpy as np
from scipy.interpolate import CubicHermiteSpline,CubicSpline
from pair_projection import analyze_snapshot,read_snapshot

ROOT=Path(__file__).resolve().parents[2]
P=json.loads((ROOT/'sol61_push/cold_completion_2026_10_20/run_001/results.json').read_text())['parameters']
mode_path,profile_path,out=map(Path,sys.argv[1:4])
with np.load(mode_path) as m:
    rmode=m['r'].copy();Z=m['mode'].copy();om=float(m['omega']);Om=float(m['Omega']);Qref=float(m['Q'])
with np.load(profile_path) as p:
    rp=p['r'].copy();yp=p['y'].copy();assert float(p['Q'])==Qref
Nr,Nz,dx=188,480,.75
rho=(np.arange(Nr)+.5)*dx;zz=(np.arange(Nz)+.5-Nz/2)*dx
radius=np.sqrt(rho[None,:]**2+zz[:,None]**2);mu=zz[:,None]/radius
Y20=math.sqrt(5/(16*math.pi))*(3*mu*mu-1)
L=rmode[-1]+float(np.median(np.diff(rmode)))
zs=CubicSpline(np.r_[0.,rmode,L],np.column_stack([np.zeros(5),Z,np.zeros(5)]),axis=1,bc_type='natural',extrapolate=False)
local=zs(np.minimum(radius,L))/radius[None,:,:];local[:,radius>L]=0.
canonical_unit=2*local.real*Y20
canonical_velocity_unit=2*np.real(1j*Om*local)*Y20
bg=[]
for row in [0,2,4]:
    f=CubicHermiteSpline(rp,yp[row],yp[row+1],extrapolate=False)
    bg.append(np.where(radius<=rp[-1],f(np.minimum(radius,rp[-1])),0.))
f,b,h=bg

def physical_arrays(A):
    u,s,x,v,t=A*canonical_unit;du,ds,dh,dv,dt=A*canonical_velocity_unit
    psi=f+(u+1j*v)/math.sqrt(2);xx=b+(s+1j*t)/math.sqrt(2)
    psit=(du+1j*dv)/math.sqrt(2)+1j*om*psi
    xt=(ds+1j*dt)/math.sqrt(2)+2j*om*xx
    return np.array([psi.real,psi.imag,xx.real,xx.imag,h+x,
                     psit.real,psit.imag,xt.real,xt.imag,dh],dtype='<f8')

def diagnostics(a):
    q=a[:5];v=a[5:];i=np.arange(Nr)[None,:]
    volume=2*math.pi*rho[None,:]*dx*dx
    lap=[];face=[];pz=0.
    for k,field in enumerate(q):
        rp=np.column_stack([field[:,1:],-field[:,-1]])
        rm=np.column_stack([field[:,0],field[:,:-1]])
        zp=np.row_stack([field[1:],-field[-1]])
        zm=np.row_stack([-field[0],field[:-1]])
        lap.append((((i+1)*(rp-field)-i*(field-rm))/(i+.5)+zp+zm-2*field)/(dx*dx))
        face.append(.5/(dx*dx)*(((i+1)*(rp-field)**2+i*(field-rm)**2)/(i+.5)+(zp-field)**2+(field-zm)**2))
        fac=.5 if k==4 else 1.
        pz+=float(np.sum(volume*(-2*fac*v[k]*(zp-zm)/(2*dx))))
    fac=np.array([1.,1.,1.,1.,.5])[:,None,None]
    kinetic=np.sum(fac*v*v,axis=0)
    gradient_lap=-np.sum(fac*q*np.array(lap),axis=0)
    gradient_face=np.sum(fac*np.array(face),axis=0)
    pr,pi,xr,xi,hh=q
    I=pr*pr+pi*pi;XX=xr*xr+xi*xi
    U=.5*P['M_chi']**2*hh*hh-P['M_chi']*hh**3/8+.25*hh**4
    potential=I+P['MX2']*XX+2*P['g']*(xr*(pr*pr-pi*pi)+2*xi*pr*pi)+P['lambda']*I*I+P['a']*hh*I+U
    charge=2*(pr*v[1]-pi*v[0])+4*(xr*v[3]-xi*v[2])
    E=float(np.sum(volume*(kinetic+gradient_lap+potential)))
    Ef=float(np.sum(volume*(kinetic+gradient_face+potential)))
    Q=float(np.sum(volume*charge))
    return {'E_discrete_laplacian':E,'E_discrete_positive_faces':Ef,'Q_discrete':Q,'Pz_discrete':pz,
            'E_face_vs_laplacian_relative':abs(E-Ef)/max(abs(E),1.),
            'positive_Q':float(np.sum(volume*np.maximum(charge,0.))),
            'negative_Q':float(np.sum(volume*np.minimum(charge,0.))),
            'charge_apertures':{str(R):float(np.sum(volume*charge*(radius<R))) for R in [10,15,20,30]},
            'Psi_peak_abs':float(np.sqrt(I).max()),'X_peak_abs':float(np.sqrt(XX).max()),'chi_peak_abs':float(abs(hh).max()),
            'Jz':'exactly zero by axisymmetry; not a numerical torque measurement'}

checks=[];rows=[]
def ck(name,value):checks.append({'name':name,'pass':bool(value)})
baseline=physical_arrays(0.);base_diag=diagnostics(baseline)
unit=physical_arrays(1.)-baseline
unit_charge=diagnostics(unit)['Q_discrete']
qlinear=diagnostics(baseline+unit)['Q_discrete']-base_diag['Q_discrete']-unit_charge
for K in [0.,50.,500.]:
    A=math.sqrt(K);arrays=physical_arrays(A)
    name=f'clean_Y20_K{int(K)}.bin';path=out/name
    with path.open('wb') as stream:
        stream.write(struct.pack('<8siidd',b'CEPAIR1\0',Nr,Nz,dx,0.));arrays.tofile(stream)
    roundtrip=read_snapshot(path)
    ck(name+' exact snapshot roundtrip',np.array_equal(roundtrip['fields'],arrays))
    ck(name+' all finite fields/momenta',np.all(np.isfinite(arrays)))
    diag=diagnostics(arrays)
    ck(name+' positive-face energy identity',diag['E_face_vs_laplacian_relative']<1e-10)
    ck(name+' zero centre momentum',abs(diag['Pz_discrete'])/diag['E_discrete_laplacian']<1e-10)
    ck(name+' positive E and Q',diag['E_discrete_laplacian']>0 and diag['Q_discrete']>0)
    qpredict=base_diag['Q_discrete']+A*qlinear+K*unit_charge
    ck(name+' exact quadratic charge polynomial',abs(diag['Q_discrete']-qpredict)<1e-6)
    fixed=analyze_snapshot(path,mode_path,profile_path,Qref=Qref,carrier_frequency=om,carrier_phase=0.)
    fitted=analyze_snapshot(path,mode_path,profile_path,Qref=Qref)
    c=complex(fixed['coordinate_real'],fixed['coordinate_imag'])
    if K:
        ck(name+' prescribed reference-frame c within2percent',abs(c-A)/A<.02)
        ck(name+' prescribed nominal K retrieval within4percent',abs(fixed['conditional_K_coordinate']/K-1)<.04)
    else:
        ck(name+' reference nuisance K<.01',fixed['conditional_K_coordinate']<.01)
        ck(name+' coarse background Q within1percent of radial reference',abs(diag['Q_discrete']/Qref-1)<.01)
    row={'nominal_K':K,'Q_actual':diag['Q_discrete'],'E_laplacian':diag['E_discrete_laplacian'],'nominal_linear_K':K,'prescribed_coordinate':[A,0.],'snapshot_file':name,'diagnostics':diag,
         'Delta_E_from_K0':diag['E_discrete_laplacian']-base_diag['E_discrete_laplacian'],
         'Delta_Q_from_K0':diag['Q_discrete']-base_diag['Q_discrete'],
         'actual_Delta_E_minus_omega_Delta_Q':diag['E_discrete_laplacian']-base_diag['E_discrete_laplacian']-om*(diag['Q_discrete']-base_diag['Q_discrete']),
         'reference_frame_projection':fixed,'fitted_carrier_projection':fitted}
    rows.append(row)
    print(json.dumps({'Knom':K,'E':diag['E_discrete_laplacian'],'Q':diag['Q_discrete'],
                      'coordinate_K':fixed['conditional_K_coordinate'],
                      'actual_DeltaK':row['actual_Delta_E_minus_omega_Delta_Q'],
                      'field_mismatch':fixed['full_canonical_field_mismatch_relative_L2']}),flush=True)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ck('measured RSS below1GB',rss<1_000_000_000)
size=sum(p.stat().st_size for p in out.iterdir() if p.is_file());ck('retained output below1GB',size<1_000_000_000)
result={'scope':'Initial-data generation/audit only: undressed finite-amplitude linear-coordinate seeds, not nonlinear normal modes or evolved solutions.',
        'reference_Q':Qref,'reference_omega':om,'linear_Omega':Om,
        'geometry':{'Nr':Nr,'Nz':Nz,'dx':dx},'parameters':P,
        'construction':'Canonical q=2sqrt(K)Re(Z/r)Y20, rotating velocity=2sqrt(K)Re(iOmega Z/r)Y20; exact lab charged velocities add iomegaPsi and2iomegaX. No DC, monopole/frequency/charge dressing.',
        'raw_charge_polynomial':{'Q0':base_diag['Q_discrete'],'linear_in_sqrtK':qlinear,'quadratic_in_sqrtK':unit_charge},
        'C_energy_stencil_source_sha256':hashlib.sha256((ROOT/'sol61_push/cold_pair_excitation_2026_10_20/pair_axisym_v2.c').read_bytes()).hexdigest(),
        'rows':rows,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(c['pass'] for c in checks),
        'peak_rss_bytes_macos':rss,'retained_output_bytes_before_result':size,
        'non_claims':['Nominal K is not the actual nonlinear excess grand potential',
                      'Actual Q is reported and not reset to136000','No corrected nonlinear Omega or periodic/DC solution',
                      'No evolution, frequency-softening measurement, radiated fraction or capture result',
                      'No physical mass/stock conversion or four-dwarf completion']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
