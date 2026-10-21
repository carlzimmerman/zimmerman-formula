"""Read-only FV-face continuity audit of immutable actual-pair snapshots.

No field advancement. The local energy is v2's positive half-link energy;
all radii select whole cell centres, giving a voxel spherical boundary.
"""
from pathlib import Path
import json, struct, sys, math, time, resource
import numpy as np

config, out = Path(sys.argv[1]), Path(sys.argv[2])
cases = json.loads(config.read_text())['cases']
start = time.monotonic()
checks, results = [], []
fac = np.array([1.,1.,1.,1.,.5])[:,None,None]
M,a,g,MX2 = 100.,200.,.002168,4.0016
lam = 1.99+g*g/MX2
def ck(name, value): checks.append({'name':name,'pass':bool(value)})

def read(path):
    path=Path(path)
    with path.open('rb') as f: raw=f.read(32)
    magic,nr,nz,dx,t=struct.unpack('<8siidd',raw)
    if magic!=b'CEPAIR1\0' or path.stat().st_size!=32+10*nr*nz*8: raise ValueError('invalid snapshot')
    z=np.memmap(path,dtype='<f8',mode='r',offset=32,shape=(10,nz,nr))
    return z[:5],z[5:],nr,nz,dx,t

def evaluate(path,radii):
    q,v,nr,nz,h,t=read(path)
    R=(np.arange(nr)+.5)*h
    zz=(np.arange(nz)+.5-nz/2)*h
    w=2*math.pi*R*h*h
    Cr=2*math.pi*np.arange(1,nr)*h
    Cz=2*math.pi*R
    pr,pi,xr,xi,chi=q
    I=pr*pr+pi*pi
    V=I+MX2*(xr*xr+xi*xi)+2*g*(xr*(pr*pr-pi*pi)+2*xi*pr*pi)+lam*I*I+a*chi*I+.5*M*M*chi*chi-M*chi**3/8+chi**4/4
    E=w*(np.sum(fac*v*v,axis=0)+V)
    Q=w*(2*(pr*v[1]-pi*v[0])+4*(xr*v[3]-xi*v[2]))
    dq_r=q[:,:,1:]-q[:,:,:-1]
    dq_z=q[:,1:,:]-q[:,:-1,:]
    er=.5*np.sum(fac*Cr*dq_r*dq_r,axis=0)
    ez=.5*np.sum(fac*Cz*dq_z*dq_z,axis=0)
    E[:,:-1]+=er;E[:,1:]+=er
    E[:-1,:]+=ez;E[1:,:]+=ez
    # Fixed zero boundary at a half cell; the axis face has zero area.
    E[:,-1]+=2*(2*math.pi*nr*h)*np.sum(fac[:,:,0]*q[:,:,-1]**2,axis=0)
    E[0,:]+=2*Cz*np.sum(fac[:,0,:]*q[:,0,:]**2,axis=0)
    E[-1,:]+=2*Cz*np.sum(fac[:,0,:]*q[:,-1,:]**2,axis=0)
    FE_r=-np.sum(fac*Cr*dq_r*(v[:,:,:-1]+v[:,:,1:]),axis=0)
    FE_z=-np.sum(fac*Cz*dq_z*(v[:,:-1,:]+v[:,1:,:]),axis=0)
    FQ_r=-2*Cr*(pr[:,:-1]*pi[:,1:]-pi[:,:-1]*pr[:,1:]+2*(xr[:,:-1]*xi[:,1:]-xi[:,:-1]*xr[:,1:]))
    FQ_z=-2*Cz*(pr[:-1,:]*pi[1:,:]-pi[:-1,:]*pr[1:,:]+2*(xr[:-1,:]*xi[1:,:]-xi[:-1,:]*xr[1:,:]))
    # Independent continuous-time ODE derivative of local energy and charge.
    lap=np.zeros_like(q)
    force_r=Cr*dq_r
    force_z=Cz*dq_z
    lap[:,:,:-1]+=force_r/w[:-1];lap[:,:,1:]-=force_r/w[1:]
    lap[:,:-1,:]+=force_z/w;lap[:,1:,:]-=force_z/w
    lap[:,:,-1]-=2*(2*math.pi*nr*h)*q[:,:,-1]/w[-1]
    lap[:,0,:]-=2*Cz*q[:,0,:]/w;lap[:,-1,:]-=2*Cz*q[:,-1,:]/w
    mass=1+2*lam*I+a*chi
    gradV=np.array([2*mass*pr+4*g*(xr*pr+xi*pi),
                    2*mass*pi+4*g*(xi*pr-xr*pi),
                    2*MX2*xr+2*g*(pr*pr-pi*pi),
                    2*MX2*xi+4*g*pr*pi,
                    M*M*chi-3*M*chi*chi/8+chi**3+a*I])
    acc=lap-gradV/(2*fac)
    Edot=w*np.sum(2*fac*v*acc+gradV*v,axis=0)
    dlink_r=np.sum(fac*Cr*dq_r*(v[:,:,1:]-v[:,:,:-1]),axis=0)
    dlink_z=np.sum(fac*Cz*dq_z*(v[:,1:,:]-v[:,:-1,:]),axis=0)
    Edot[:,:-1]+=dlink_r;Edot[:,1:]+=dlink_r
    Edot[:-1,:]+=dlink_z;Edot[1:,:]+=dlink_z
    Edot[:,-1]+=4*(2*math.pi*nr*h)*np.sum(fac[:,:,0]*q[:,:,-1]*v[:,:,-1],axis=0)
    Edot[0,:]+=4*Cz*np.sum(fac[:,0,:]*q[:,0,:]*v[:,0,:],axis=0)
    Edot[-1,:]+=4*Cz*np.sum(fac[:,0,:]*q[:,-1,:]*v[:,-1,:],axis=0)
    Qdot=w*(2*(pr*acc[1]-pi*acc[0])+4*(xr*acc[3]-xi*acc[2]))
    row={'time':float(t),'nr':nr,'nz':nz,'dx':h,'E_box':float(E.sum()),'Q_box':float(Q.sum()),'radii':{}}
    r2=zz[:,None]**2+R[None,:]**2
    for radius in radii:
        mask=r2<radius*radius
        if mask[:,0].all() or mask[:,-1].any() or mask[0,:].any() or mask[-1,:].any():
            raise ValueError('audit aperture reaches a box boundary')
        sr=mask[:,:-1].astype(np.int8)-mask[:,1:].astype(np.int8)
        sz=mask[:-1,:].astype(np.int8)-mask[1:,:].astype(np.int8)
        er=FE_r*sr;ez=FE_z*sz;qr=FQ_r*sr;qz=FQ_z*sz
        fluxE=float(er.sum()+ez.sum());fluxQ=float(qr.sum()+qz.sum())
        ed=float(Edot[mask].sum());qd=float(Qdot[mask].sum())
        Eerr=abs(ed+fluxE)/max(1,abs(ed)+abs(fluxE))
        Qerr=abs(qd+fluxQ)/max(1,abs(qd)+abs(fluxQ))
        row['radii'][str(radius)]={'E':float(E[mask].sum()),'Q':float(Q[mask].sum()),
            'E_flux':fluxE,'Q_flux':fluxQ,
            'E_positive_face_flux':float(np.maximum(er,0).sum()+np.maximum(ez,0).sum()),
            'E_negative_face_flux':float(np.minimum(er,0).sum()+np.minimum(ez,0).sum()),
            'Q_positive_signed_face_flux':float(np.maximum(qr,0).sum()+np.maximum(qz,0).sum()),
            'Q_negative_signed_face_flux':float(np.minimum(qr,0).sum()+np.minimum(qz,0).sum()),
            'E_ODE_dot':ed,'Q_ODE_dot':qd,'E_instant_continuity_relative':Eerr,'Q_instant_continuity_relative':Qerr,
            'crossing_faces':int(np.count_nonzero(sr)+np.count_nonzero(sz))}
    return row

# A travelling positive-charge phase tests signs and the lab E/Q ratio.
theta=.37;nu=1.21;left=1+0j;right=np.exp(-1j*theta)
energy=float(np.real((left-right).conjugate()*(1j*nu*left+1j*nu*right)))
charge=float(-2*np.imag(left.conjugate()*right))
ck('positive travelling-wave outward E and Q',energy>0 and charge>0)
ck('travelling wave exact E over Q',abs(energy/charge-nu)<1e-14)
ck('charge-two travelling wave E over Q',abs(energy/(2*charge)-nu/2)<1e-14)

for case in cases:
    log=[json.loads(x) for x in Path(case['log']).read_text().splitlines()]
    encl=[json.loads(x) for x in Path(case['enclosed']).read_text().splitlines()]
    log_by={round(x['t'],8):x for x in log};encl_by={round(x['t'],8):x for x in encl}
    rows=[]
    for snap in case['snapshots']:
        row=evaluate(snap,[20,30,40]);t=round(row['time'],8)
        ck(case['name']+f' t{t} box E matches v2 log',abs(row['E_box']/log_by[t]['E']-1)<1e-10)
        ck(case['name']+f' t{t} box Q matches v2 log',abs(row['Q_box']/log_by[t]['Q']-1)<1e-10)
        ck(case['name']+f' t{t} E20 matches positive half-link log',abs(row['radii']['20']['E']/encl_by[t]['E20']-1)<1e-10)
        ck(case['name']+f' t{t} Q20 matches log',abs(row['radii']['20']['Q']/log_by[t]['Q20']-1)<1e-10)
        for r,x in row['radii'].items():
            ck(case['name']+f' t{t} R{r} instant E continuity',x['E_instant_continuity_relative']<1e-8)
            ck(case['name']+f' t{t} R{r} instant Q continuity',x['Q_instant_continuity_relative']<1e-8)
        rows.append(row)
    ts=np.array([x['time'] for x in rows]);summaries={}
    for radius in [20,30,40]:
        key=str(radius);rr=[x['radii'][key] for x in rows]
        windows={}
        for lo,hi in [(0,240),(120,240)]:
            ids=np.where((ts>=lo)&(ts<=hi))[0];tt=ts[ids]
            vals={}
            for kind in ['E','Q']:
                drop=rr[ids[0]][kind]-rr[ids[-1]][kind]
                net=float(np.trapz([rr[i][kind+'_flux'] for i in ids],tt))
                vals[kind+'_aperture_drop']=drop
                vals[kind+'_snapshot_flux_integral']=net
                vals[kind+'_flux_minus_aperture_drop']=net-drop
                vals[kind+'_relative_reconstruction_error']=abs(net-drop)/max(abs(drop),1)
            for field in ['E_positive_face_flux','E_negative_face_flux','Q_positive_signed_face_flux','Q_negative_signed_face_flux']:
                vals[field+'_integral']=float(np.trapz([rr[i][field] for i in ids],tt))
            vals['net_aperture_E_drop_over_Q_drop']=vals['E_aperture_drop']/vals['Q_aperture_drop'] if abs(vals['Q_aperture_drop'])>1e-12 else None
            vals['net_snapshot_flux_E_over_Q']=vals['E_snapshot_flux_integral']/vals['Q_snapshot_flux_integral'] if abs(vals['Q_snapshot_flux_integral'])>1e-12 else None
            windows[f'{lo}_{hi}']=vals
        summaries[key]={'initial_E':rr[0]['E'],'final_E':rr[-1]['E'],'initial_Q':rr[0]['Q'],'final_Q':rr[-1]['Q'],'windows':windows,
            'snapshot_positive_E_net_count':sum(x['E_flux']>0 for x in rr),'snapshot_negative_E_net_count':sum(x['E_flux']<0 for x in rr),
            'max_instant_E_continuity_relative':max(x['E_instant_continuity_relative'] for x in rr),
            'max_instant_Q_continuity_relative':max(x['Q_instant_continuity_relative'] for x in rr)}
    result={'name':case['name'],'snapshot_times':ts.tolist(),'cadence':np.diff(ts).tolist(),'rows':rows,'aperture_summary':summaries}
    results.append(result)
    print(json.dumps({'case':case['name'],'R20':summaries['20']['windows']['0_240'],'R30':summaries['30']['windows']['0_240']}),flush=True)

rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ck('measured RSS below 1GB',rss<1_000_000_000)
result={'scope':'Signed FV-face energy and Noether-charge transport from saved actual-pair snapshots; no field advancement.',
        'allocation':'Same positive half-link energy as pair_axisym_v2.c; strict cell-centre spherical mask, summing all oriented interior cut faces.',
        'conventions':{'E_face_i_to_j':'sum_a fac_a Cij (qai-qaj)(vai+vaj), fac=1 for complex Cartesian components and1/2 chi',
                       'Q_face_i_to_j':'-2 Cij Im(Psi_i* Psi_j)-4 Cij Im(X_i* X_j)',
                       'sampling':'20 natural-time-unit snapshots, trapezoidal integrals; numerical reconstruction error is measured, not assumed small.',
                       'signed_charge':'Positive signed Q flux is not by itself a particle mass or direction classifier if opposite charges exist.'},
        'cases':results,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(x['pass'] for x in checks),
        'peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
        'non_claims':['No bound-stock or asymptotic escape classification from aperture transport','No continuum error bound or high-cadence flux reconstruction',
                      'No spectral identification of outgoing quanta from aggregate E/Q','No isolated mode attribution, cooling efficiency or galaxy mass-budget closure',
                      'Axisymmetry and head-on initial conditions have zero total angular momentum']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
