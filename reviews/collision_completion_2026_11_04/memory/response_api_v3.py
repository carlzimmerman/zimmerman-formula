"""Occupation-independent CC10 cell-pair Floquet kernel and parent moments.

Extends immutable v2. Mass/width/input conventions are identical. All radial
cells are represented; no f-dependent tail is silently dropped. The response
is the fixed neutral-width model, with a separate charged-width perturbation
test below. Does not invent a dynamically matched retarded charged selfenergy.
"""
import sys
sys.dont_write_bytecode=True
from response_api_v2 import *

def cell_modes(xmid,amplitude,omega,Tc,edges,radial=2,angular=12):
    edges=np.asarray(edges,float);nn=len(edges)-1
    z,w=leggauss(radial);az,aw=leggauss(angular)
    aa=edges[:-1];bb=edges[1:];W=(bb**3-aa**3)/3
    q=((aa+bb)[:,None]/2+(bb-aa)[:,None]/2*z).ravel()
    qw=(((bb-aa)[:,None]/2*w)*q.reshape(nn,radial)**2/W[:,None]).ravel()
    cells=np.repeat(np.arange(nn),radial)
    i,j,k=np.meshgrid(np.arange(len(q)),np.arange(len(q)),np.arange(angular),indexing='ij')
    ii=cells[i].ravel();jj=cells[j].ravel();p1=Tc*q[i].ravel();p2=Tc*q[j].ravel();c=az[k].ravel()
    weight=(qw[i]*qw[j]*aw[k]/2).ravel()
    m=float(charged_mass(xmid));dm=charged_mass_derivative(xmid)
    e1=np.sqrt(m*m+p1*p1);e2=np.sqrt(m*m+p2*p2);P2=p1*p1+p2*p2+2*p1*p2*c;ep=np.sqrt(M*M+P2)
    delta=((M-2*m)*(M+2*m)+P2)/(ep+2*m)-p1*p1/(e1+m)-p2*p2/(e2+m)
    A=amplitude*m*dm*(1/e1+1/e2)
    return dict(i=ii,j=jj,index=ii*nn+jj,weight=weight,delta=delta,A=A,z=A/omega,
                pref=LAMBDA/(4*e1*e2*ep),boost=M/ep,EN=ep,Echarged=e1+e2,
                e1=e1,e2=e2,p1=p1,p2=p2,c=c,ncell=nn)

def _bin(values,mode):
    nn=mode['ncell'];idx=mode['index'];w=mode['weight'];v=np.asarray(values)
    if v.ndim==1:return np.bincount(idx,weights=w*v,minlength=nn*nn).reshape(nn,nn)
    out=np.empty((nn,nn)+v.shape[1:],dtype=v.dtype)
    for multi in np.ndindex(v.shape[1:]):
        a=v[(slice(None),)+multi]
        if np.iscomplexobj(a):
            b=np.bincount(idx,weights=w*a.real,minlength=nn*nn)+1j*np.bincount(idx,weights=w*a.imag,minlength=nn*nn)
        else:b=np.bincount(idx,weights=w*a,minlength=nn*nn)
        out[(slice(None),slice(None))+multi]=b.reshape(nn,nn)
    return out

def band_kernel(xmid,amplitude,omega,Tc,edges,radial=2,angular=12,channels=None):
    """Physical Kij=<sigma*v_Moller>, independent of occupations.

    n_i±=12 Tc³/(2pi²) W_i fS_i. dfS_i/dtau=-fS_i*(K@n_minus)_i
    for the specified empty-parent neutral-exit model. Each pair creates one
    neutral parent and removes two charged carriers. Parent density moment
    rho_ij is per n_i+ n_j-. Exit-rho includes exact mode boost and contracts
    with rest-frame daughter-channel Gamma_a to give channel Kij.

    This supplies a positive orbit-averaged generator, not instantaneous
    positive phase rates. It cannot be inserted into the old action covariance
    at every phase without the separately supplied work bound/matching.
    """
    d=cell_modes(xmid,amplitude,omega,Tc,edges,radial,angular)
    delta,A,z,pref,b=(d[k] for k in ('delta','A','z','pref','boost'))
    nmax=int(math.ceil(float(max(z))+12+4*float(max(z))**(1/3)))
    rr=np.zeros((len(delta),4,4),complex);stat=np.zeros_like(rr)
    for n in range(-nmax,nmax+1):
        r=COEFF[None,:]/(WIDTH[None,:]*b[:,None]/2+1j*(delta+n*omega)[:,None])
        rr+=pref[:,None,None]*(jv(n,z)**2)[:,None,None]*r[:,:,None]*r[:,None,:].conj()
    aa=WIDTH[None,:]*b[:,None]/2+1j*delta[:,None]
    F=1/np.sqrt(aa*aa+A[:,None]**2)
    stat=pref[:,None,None]*(F[:,:,None]+F[:,None,:].conj())/(b[:,None,None]*(WIDTH[None,:,None]+WIDTH[None,None,:])/2)*COEFF[None,:,None]*COEFF.conj()[None,None,:]
    rate=b*np.sum(WIDTH[None,:]*rr.diagonal(axis1=1,axis2=2).real,axis=1)
    staticrate=b*np.sum(WIDTH[None,:]*stat.diagonal(axis1=1,axis2=2).real,axis=1)
    rhoeig=_bin(rr,d);exiteig=_bin(rr*b[:,None,None],d)
    rho=np.einsum('ab,ijbc,dc->ijad',U,rhoeig,U,optimize=True)
    exitrho=np.einsum('ab,ijbc,dc->ijad',U,exiteig,U,optimize=True)
    sqrtg=(U*np.sqrt(WIDTH)[None,:])@U.T
    positiveS=np.einsum('ab,ijbc,cd->ijad',sqrtg,exitrho,sqrtg,optimize=True)
    K=_bin(rate,d);Kstatic=_bin(staticrate,d)
    # Absolute bound on energy mismatched by identifying net charged removal
    # with on-shell neutral exits at a phase. It is deliberately conservative.
    energy_error_bound=_bin(rate*(abs(delta)+A),d)
    out=dict(K=K,K_stationary=Kstatic,parent_rho=rho,exit_rho=exitrho,
             positive_source=positiveS,
             parent_energy_density_pair=_bin(d['EN']*rr.trace(axis1=1,axis2=2).real,d),
             neutral_exit_energy_rate_pair=_bin(d['EN']*rate,d),
             charged_mean_energy_rate_pair=_bin(d['Echarged']*rate,d),
             absolute_energy_exchange_bound_pair=energy_error_bound,
             nmax=nmax,radial=radial,angular=angular,
             max_boost_error=float(max(1-b)))
    if channels is not None:
        out['channel_K']={key:np.einsum('ab,ijba->ij',np.asarray(g),exitrho,optimize=True).real for key,g in channels.items()}
    return out

def contract_band(kernel,Tc,edges,f_number):
    e=np.asarray(edges);f=np.asarray(f_number);W=(e[1:]**3-e[:-1]**3)/3
    n=12*Tc**3/(2*math.pi**2)*W*f;pair=n[:,None]*n[None,:]
    K=kernel['K'];event=float(np.sum(pair*K))
    return dict(df_number_dtau=-f*(K@n),event_rate_mu4=event,
                charged_number_loss_mu4=2*event,
                parent_rho_mu3=np.einsum('ij,ijab->ab',pair,kernel['parent_rho'],optimize=True),
                positive_source_mu4=np.einsum('ij,ijab->ab',pair,kernel['positive_source'],optimize=True),
                parent_energy_mu4=float(np.sum(pair*kernel['parent_energy_density_pair'])),
                neutral_exit_energy_rate_mu5=float(np.sum(pair*kernel['neutral_exit_energy_rate_pair'])),
                charged_mean_energy_rate_mu5=float(np.sum(pair*kernel['charged_mean_energy_rate_pair'])),
                absolute_energy_exchange_bound_mu5=float(np.sum(pair*kernel['absolute_energy_exchange_bound_pair'])))

def charged_width_bound(xmid,amplitude):
    """Rigorous Floquet L2 perturbation bound for this LOCAL absorptive ΓC.

    L=dt+iδ+Γout/2 is accretive with gap γmin/2. B=ΓC(t)/2>=0.
    (L+B)^-1 has norm <=2/γmin; δa=-(L+B)^-1 B a0 gives
    ||δa||<=ε||a0||, ε=sup||ΓC||/γmin. Weighted exit norm error
    is <=η=sqrt(γmax/γmin)ε. This controls periodic derivative on its
    Hilbert space independently of detuning and source shape.
    It is NOT a bound on a dispersive/nonlocal charged retarded kernel.
    """
    m=float(charged_mass(xmid-abs(amplitude)))
    beta=math.sqrt(max(0,1-4*m*m/M**2));gin=144*LAMBDA*beta/(32*math.pi*M)
    epsilon=gin/min(WIDTH);eta=math.sqrt(max(WIDTH)/min(WIDTH))*epsilon
    return dict(max_GammaC_norm=gin,epsilon=epsilon,eta=eta,
                minimum_rate_ratio=max(0,1-eta)**2,maximum_rate_ratio=(1+eta)**2)

def local_charged_width_modes(delta,A,boost,xmid,amplitude,omega,nodes=256,iterations=10):
    """Actual 4-state periodic response with local ΓC(θ), FFT fixed point.

    Arrays label physical charged pair modes. Returned neutral exit response
    omits the common positive relativistic prefactor. Residual iterations
    contract under the reported ε; compare nodes/iterations explicitly.
    """
    delta=np.atleast_1d(delta);A=np.atleast_1d(A);boost=np.atleast_1d(boost)
    theta=2*math.pi*np.arange(nodes)/nodes;n=np.fft.fftfreq(nodes)*nodes
    m=charged_mass(xmid+amplitude*np.cos(theta))
    beta=np.sqrt(np.maximum(0,1-4*m*m/M**2));gc=144*LAMBDA*beta/(32*math.pi*M)
    source=np.exp(-1j*(A/omega)[:,None]*np.sin(theta)[None,:])[:,:,None]*COEFF[None,None,:]
    rhs=np.fft.fft(source,axis=1)/nodes
    denom=WIDTH[None,None,:]*boost[:,None,None]/2+1j*(delta[:,None,None]+omega*n[None,:,None])
    u=rhs/denom;initial=u.copy();last=math.inf
    for it in range(iterations):
        ut=np.fft.ifft(u*nodes,axis=1)
        projection=np.einsum('a,mta->mt',COEFF.conj(),ut,optimize=True)
        Bu=.5*boost[:,None,None]*gc[None,:,None]*projection[:,:,None]*COEFF[None,None,:]
        nxt=(rhs-np.fft.fft(Bu,axis=1)/nodes)/denom
        last=float(np.linalg.norm(nxt-u)/max(np.linalg.norm(nxt),1e-300));u=nxt
    rate=np.sum(abs(u)**2*WIDTH[None,None,:]*boost[:,None,None],axis=(1,2))
    rate0=np.sum(abs(initial)**2*WIDTH[None,None,:]*boost[:,None,None],axis=(1,2))
    return dict(rate=rate,rate_without_charged=rate0,last_iteration_relative=last)
