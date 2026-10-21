"""Bounded synthetic coordinate/extraction control; no pair field evolution."""
from pathlib import Path
import json
import math
import resource
import struct
import sys

import numpy as np
from scipy.interpolate import CubicHermiteSpline, CubicSpline
from pair_projection import analyze_snapshot

mode_path,profile_path,out=map(Path,sys.argv[1:4])
with np.load(mode_path) as m:
    rm=m['r'].copy();Z=m['mode'].copy();om=float(m['omega']);Om=float(m['Omega'])
with np.load(profile_path) as p:
    rp=p['r'].copy(); yp=p['y'].copy()
L=rm[-1]+float(np.median(np.diff(rm)))
mode_spline=CubicSpline(np.r_[0.,rm,L],np.column_stack([np.zeros(5),Z,np.zeros(5)]),axis=1,bc_type='natural',extrapolate=False)
bg=[CubicHermiteSpline(rp,yp[k],yp[k+1],extrapolate=False) for k in [0,2,4]]
theta=.37

def generate(path,dx,c):
    Nr=int(round(64/dx));Nz=2*Nr
    rho=(np.arange(Nr)+.5)*dx;zz=(np.arange(Nz)+.5-Nz/2)*dx
    radius=np.sqrt(zz[:,None]**2+rho[None,:]**2)
    mu=zz[:,None]/radius;Y=math.sqrt(5/(16*math.pi))*(3*mu*mu-1)
    safe=np.minimum(radius,L);shape=mode_spline(safe)/radius[None,:,:]
    shape[:,radius>L]=0.
    q=2*np.real(c*shape)*Y;v=2*np.real(1j*Om*c*shape)*Y
    fields=np.array([np.where(radius<=rp[-1],f(np.minimum(radius,rp[-1])),0.) for f in bg])
    psi0=fields[0]+(q[0]+1j*q[3])/math.sqrt(2)
    xx0=fields[1]+(q[1]+1j*q[4])/math.sqrt(2)
    psi=psi0*np.exp(1j*theta);xx=xx0*np.exp(2j*theta)
    psit=np.exp(1j*theta)*((v[0]+1j*v[3])/math.sqrt(2)+1j*om*psi0)
    xt=np.exp(2j*theta)*((v[1]+1j*v[4])/math.sqrt(2)+2j*om*xx0)
    arrays=np.array([psi.real,psi.imag,xx.real,xx.imag,fields[2]+q[2],
                     psit.real,psit.imag,xt.real,xt.imag,v[2]],dtype='<f8')
    with path.open('wb') as stream:
        stream.write(struct.pack('<8siidd',b'CEPAIR1\0',Nr,Nz,dx,0.))
        arrays.tofile(stream)

checks=[];rows=[]
def ck(name,passed,value=None):
    rec={'name':name,'pass':bool(passed)}
    if value is not None:rec['value']=float(value)
    checks.append(rec)

specs=[('reference_fine.bin',.2,0j),
       ('known_phi02_coarse.bin',.4,.1*np.exp(.2j)),
       ('known_phi02_fine.bin',.2,.1*np.exp(.2j)),
       ('known_phi11_fine.bin',.2,.1*np.exp(1.1j))]
for name,dx,c in specs:
    path=out/name;generate(path,dx,c)
    result=analyze_snapshot(path,mode_path,profile_path,Qref=160000,angular_nodes=48,interpolation_order=3)
    recovered=complex(result['coordinate_real'],result['coordinate_imag'])
    error=abs(recovered-c)
    row={'name':name,'dx':dx,'known_coordinate':[float(c.real),float(c.imag)],
         'coordinate_error_absolute':error,'analysis':result}
    if c:
        relative=error/abs(c); row['coordinate_error_relative']=relative
        ck(name+' known complex coordinate within2percent',relative<.02,relative)
        ck(name+' known K within4percent',abs(result['conditional_K_coordinate']/abs(c)**2-1)<.04)
        ck(name+' reconstructed ell2 state residual fraction <2percent',result['ell2_reconstruction_state_residual_fraction']<.02)
        # Explicit reference-frame recovery separates interpolation from fitted-frame bias.
        fixed=analyze_snapshot(path,mode_path,profile_path,Qref=160000,angular_nodes=48,
                               interpolation_order=3,carrier_frequency=om,carrier_phase=theta)
        row['explicit_reference_frame_analysis']=fixed
        fixedc=complex(fixed['coordinate_real'],fixed['coordinate_imag'])
        ck(name+' explicit frame coordinate within2percent',abs(fixedc-c)/abs(c)<.02)
    else:
        ck('spherical reference negative control K<1e-6',result['conditional_K_coordinate']<1e-6,result['conditional_K_coordinate'])
    ck(name+' shared carrier phase recovered within1e-3',abs(np.angle(np.exp(1j*(result['carrier_phase_used']-theta))))<1e-3)
    ck(name+' fitted carrier frequency within1e-4',abs(result['carrier_frequency_used']-om)<1e-4)
    ck(name+' projection retains mode L2 fraction>.9999',result['mode_canonical_L2_fraction_inside_projection']>.9999)
    rows.append(row)
    print(json.dumps({'name':name,'error':error,'K':result['conditional_K_coordinate'],
                      'residual_fraction':result['ell2_reconstruction_state_residual_fraction']}),flush=True)
coarse=next(r for r in rows if r['name']=='known_phi02_coarse.bin')
fine=next(r for r in rows if r['name']=='known_phi02_fine.bin')
ck('coordinate interpolation error improves on dx halving',fine['coordinate_error_absolute']<coarse['coordinate_error_absolute'])
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ck('measured RSS<1GB',rss<1_000_000_000,rss)
size=sum(p.stat().st_size for p in out.iterdir() if p.is_file())
ck('retained synthetic output<1GB',size<1_000_000_000,size)
result={'scope':'Synthetic snapshot/projection controls only; no field evolution or measured merger excitation.',
        'rows':rows,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(c['pass'] for c in checks),
        'peak_rss_bytes_macos':rss,'retained_output_bytes_before_result':size,
        'non_claims':['No collision solution','No persistent bound-mode measurement','No remnant charge/stock inference','No physical cooling or dwarf closure']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
