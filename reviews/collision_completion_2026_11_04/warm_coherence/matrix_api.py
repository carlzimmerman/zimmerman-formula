"""Actual-x four-singlet matrix collision diagnostic on stored warm states."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import math,json
import numpy as np
from scipy.linalg import solve_sylvester,expm
from numpy.polynomial.legendre import leggauss
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from network import state,E,build_model,DCOEF,T,adapt
from vertices import VertexBackground

def basis_at(x,P):
    d=build_model(x,E,E,math.sqrt(29/200)*E,vertices=False);R=d['R']
    ry=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),R);q=ry@ry;qs=np.block([[q.real,-q.imag],[q.imag,q.real]])
    vacuum=np.diag([2,2,2,-3,-3]);un=[a for a,t in enumerate(T) if np.max(abs(t@vacuum-vacuum@t))<1e-12]
    c=np.einsum('aij,ajk->ik',R[un],R[un]);cs=np.block([[c.real,-c.imag],[c.imag,c.real]])
    old=adapt(d['O'],d['mS2'],qs)
    new=adapt(old,d['mS2']+np.einsum('ia,ia->a',old,qs@old).real,cs)
    charges=np.einsum('ia,ia->a',new,qs@new).real
    actual=np.flatnonzero((abs(d['mS2']-2*E)<1e-12)&(charges<.1))
    if len(actual)!=4:raise ValueError('basis check cannot identify four actual massive singlets')
    return new[:,actual]

def snapshot(path):
    d=json.loads(Path(path).read_text());c=d['case'];s=d['state'];q=np.asarray(c['q']);W=np.asarray(c['W'])
    bg=VertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json')
    groups=bg.groups;deg=np.asarray([g['degeneracy'] for g in groups]);measure=deg[:,None]*W[None,:]/(2*math.pi**2)
    eta=np.asarray([1 if g['kind']=='S' else -1 for g in groups])[:,None]
    if 'Z' in s:
        z=np.asarray(s['Z']).reshape(len(groups),len(q))/measure;holes=np.asarray(s['hole_flags']).reshape(z.shape)
        f=np.where(holes,1-z,z);availability=np.where(holes,z,1+eta*f);hole_source='independent stored Z/hole_flags'
    else:
        f=np.asarray(s['Y']).reshape(len(groups),len(q))/measure;availability=1+eta*f;hole_source='availability reconstructed from recorded rounded Y; sub-ulp holes unavailable'
    return dict(raw=d,q=q,W=W,f=f,availability=availability,groups=groups,by={g['id']:i for i,g in enumerate(groups)},
                N=s['N'],t=c['history'][-1]['Tc_over_mu'],x=s['xmid'],bg=bg,hole_source=hole_source,history=c['history'][-1])

def actual_matrices(x,background=None):
    """Actual-x full-basis vertex matrices; optional warm common masses.

    Scalar-parent spin sum is isotropic. Group-isotropic daughter occupations
    therefore weight each matrix by one scalar angular factor. Actual tree
    indices/couplings are rebuilt; only kinematics can use common warm masses.
    """
    s=state(float(x));rawgroups=s['groups'];by={g['id']:g for g in rawgroups}
    P=[i for i in range(98) if s['physical'][i] and not s['charged'][i] and abs(s['mass'][i]-math.sqrt(2*E))<1e-8]
    if len(P)!=4:raise ValueError('actual parent multiplicity is not four')
    parent=next(g for g in rawgroups if set(P)<=set(g['indices']));pid=parent['id']
    data=background.at(float(x)) if background is not None else None
    masses={g['id']:g['mass'] for g in (data['groups'] if data else rawgroups)}
    M=masses[pid];ci=s['c3'][P];yy=s['yy'][:,:,P].transpose(2,0,1);out={};invariants={}
    for typ,offset in (('SS',0),('FF',98)):
        eligible=[g for g in rawgroups if g['kind']==('S' if typ=='SS' else 'F')]
        for j,J in enumerate(eligible):
            for K in eligible[j:]:
                ids=np.asarray(J['indices'])-offset;kds=np.asarray(K['indices'])-offset
                if typ=='SS':
                    v=ci[:,ids][:,:,kds];C=np.einsum('aij,bij->ab',v,v,optimize=True)*(1 if J['id']==K['id'] else 2)
                    A=B=None
                else:
                    v=yy[:,ids][:,:,kds];fac=1 if J['id']==K['id'] else 2
                    A=np.einsum('aij,bij->ab',v,v.conj(),optimize=True).real*fac
                    B=np.einsum('aij,bij->ab',v,v,optimize=True).real*fac;C=None
                norm=np.linalg.norm(C if C is not None else A)
                if norm<1e-27:continue
                m1,m2=masses[J['id']],masses[K['id']]
                if M<=m1+m2+1e-14:continue
                z1,z2=m1/M,m2/M;phase=math.sqrt(max(0,(1-(z1+z2)**2)*(1-(z1-z2)**2)))
                mat=C*phase/(32*math.pi*M) if typ=='SS' else M/(16*math.pi)*phase*((1-z1*z1-z2*z2)*A-2*z1*z2*B)
                if np.linalg.norm(mat)<1e-24:continue
                key=J['id']+'|'+K['id'];out[key]=mat;invariants[key]=dict(kind=typ,first=J['id'],second=K['id'],charged_carriers=int(J['charged'])+int(K['charged']))
    # Parent-as-daughter coverage is checked using all actual-x invariant
    # vertices reconstructed by the independent grouped background builder.
    actual_daughter_channels=[]
    for Agroup in rawgroups:
        MA=masses[Agroup['id']]
        for Bgroup in rawgroups:
            if Agroup['kind']!=Bgroup['kind']:continue
            mb=masses[Bgroup['id']]
            if MA<=M+mb+1e-14:continue
            za,zb=M/MA,mb/MA;phase=math.sqrt(max(0,(1-(za+zb)**2)*(1-(za-zb)**2)))
            if Agroup['kind']=='S':
                vv=s['c3'][np.ix_(Agroup['indices'],P,Bgroup['indices'])]
                C=float(np.sum(vv*vv))/len(Agroup['indices'])
                width=C*phase/(16*math.pi*MA)
            else:
                vv=s['yy'][np.ix_(np.asarray(Agroup['indices'])-98,np.asarray(Bgroup['indices'])-98,P)]
                AA=float(np.sum(abs(vv)**2))/len(Agroup['indices']);BB=float(np.sum((vv*vv).real))/len(Agroup['indices'])
                width=MA*phase/(16*math.pi)*(AA*(1+zb*zb-za*za)+2*BB*zb)
            if width>1e-25:actual_daughter_channels.append(dict(parent=Agroup['id'],other=Bgroup['id'],width=width))
    if data:
        daughter_channels=[c for c in data['channels'] if pid in c['daughters']]
        traced={ '|'.join(c['daughters']):c['width'] for c in data['channels'] if c['parent']==pid}
        interp_error={key:abs(float(np.trace(mat))/4/traced[key]-1) for key,mat in out.items() if key in traced and traced[key]>1e-24}
    else:daughter_channels=[];interp_error={}
    return dict(x=float(x),M=M,P=P,parent_id=pid,matrices=out,channels=invariants,masses=masses,
                physical_basis=basis_at(float(x),P),
                raw_state=s,parent_as_daughter_channels=actual_daughter_channels,parent_as_daughter_background=daughter_channels,
                interpolation_width_relative=interp_error)

def _mean_exp(l0,l1):
    if not (math.isfinite(l0) and math.isfinite(l1)):return 0.
    d=abs(l1-l0);v=math.exp(max(l0,l1))
    return v if d<1e-14 else v*(-math.expm1(-d))/d

def angular_factors(M,m1,m2,p,energies1,energies2,f1,f2,av1,av2,gauss=None):
    """Exact angular factors in the declared finite log-product projection."""
    Ep=math.sqrt(M*M+p*p);estar=(M*M+m1*m1-m2*m2)/(2*M)
    ps=math.sqrt(max(0,(M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2)))/(2*M)
    base=Ep*estar/M;slope=p*ps/M;other=Ep-base
    cuts=[-1.,1.]
    if slope>0:
        for en,off,sl in ((energies1,base,slope),(energies2,other,-slope)):
            z=(en-off)/sl;cuts.extend(z[(z>-1+1e-14)&(z<1-1e-14)].tolist())
    cuts=np.unique(cuts);loss=gain=coverage=0.
    with np.errstate(divide='ignore'):
        lf1=np.log(f1);lf2=np.log(f2);la1=np.log(av1);la2=np.log(av2)
    def weights(en,target):
        pos=int(np.clip(np.searchsorted(en,target)-1,0,len(en)-2));a=(target-en[pos])/(en[pos+1]-en[pos]);return pos,float(np.clip(a,0,1))
    def interp(logs,pos,a):
        if a==0:return float(logs[pos])
        if a==1:return float(logs[pos+1])
        return float((1-a)*logs[pos]+a*logs[pos+1])
    gz,gw=leggauss(gauss) if gauss is not None else (None,None)
    for left,right in zip(cuts[:-1],cuts[1:]):
        mid=(left+right)/2;half=(right-left)/2;e1=base+slope*mid;e2=Ep-e1
        if e1<energies1[0]-1e-13 or e1>energies1[-1]+1e-13 or e2<energies2[0]-1e-13 or e2>energies2[-1]+1e-13:continue
        coverage+=half
        def logs_at(z):
            i,a=weights(energies1,base+slope*z);j,b=weights(energies2,other-slope*z)
            return interp(la1,i,a)+interp(la2,j,b),interp(lf1,i,a)+interp(lf2,j,b)
        if gauss is None:
            ll,lg=logs_at(left);rl,rg=logs_at(right);loss+=half*_mean_exp(ll,rl);gain+=half*_mean_exp(lg,rg)
        else:
            for z,w in zip(mid+half*gz,gw):
                ll,lg=logs_at(float(z));loss+=half*w/2*math.exp(ll);gain+=half*w/2*math.exp(lg)
    return loss,gain,coverage

def weighted_matrices(packet,snap,gauss=None,f_override=None,av_override=None):
    q=snap['q'];t=snap['t'];f=snap['f'] if f_override is None else f_override;av=snap['availability'] if av_override is None else av_override
    n=len(q);M=packet['M'];en={g:np.sqrt(m*m+(t*q)**2) for g,m in packet['masses'].items()}
    out={};coverage={}
    for key,mat in packet['matrices'].items():
        ch=packet['channels'][key];j,k=ch['first'],ch['second'];jj=snap['by'][j];kk=snap['by'][k]
        L=[];G=[];C=[]
        for p in t*q:
            l,g,c=angular_factors(M,packet['masses'][j],packet['masses'][k],p,en[j],en[k],f[jj],f[kk],av[jj],av[kk],gauss)
            boost=M/math.sqrt(M*M+p*p);L.append(l*boost);G.append(g*boost);C.append(c)
        out[key]=dict(loss=np.asarray(L)[:,None,None]*mat,gain=np.asarray(G)[:,None,None]*mat)
        coverage[key]=np.asarray(C)
    return out,coverage

def summarize(packet,snap,weighted):
    n=len(snap['q']);loss=sum(v['loss'] for v in weighted.values());gain=sum(v['gain'] for v in weighted.values());D=loss-gain
    actual=snap['f'][snap['by'][packet['parent_id']]];W=snap['t']**3*snap['W']/(2*math.pi**2)
    rows=[];coh_channels={key:0. for key in weighted};iso_channels={key:0. for key in weighted};current_channels={key:0. for key in weighted};equal_channels={key:0. for key in weighted}
    for i in range(n):
        dd=(D[i]+D[i].T)/2;ev=np.linalg.eigvalsh(dd);g=gain[i];cur=actual[i]*np.eye(4)
        rhs=g-.5*(dd@cur+cur@dd);anis=rhs-np.eye(4)*np.trace(rhs)/4
        item=dict(q=float(snap['q'][i]),p=float(snap['t']*snap['q'][i]),actual_parent_f=float(actual[i]),net_width_eigenvalues=ev.tolist(),
             instantaneous_isotropy_driving=float(np.linalg.norm(anis)/max(np.linalg.norm(rhs),1e-300)),stable=bool(ev.min()>0))
        if ev.min()>0:
            rho=solve_sylvester(dd/2,dd/2,g);rho=(rho+rho.T)/2
            iso=float(np.trace(g)/np.trace(dd));riso=iso*np.eye(4);equal=np.eye(4)*np.trace(rho)/4
            item.update(rho_steady=rho.tolist(),rho_eigenvalues=np.linalg.eigvalsh(rho).tolist(),isotropic_steady_f=iso,
                steady_number_ratio_to_isotropic=float(np.trace(rho)/(4*iso)) if iso>0 else None,
                invariant_isotropy_defect=float(np.linalg.norm(rho-equal)/max(np.linalg.norm(rho),1e-300)),
                normalized_commutator=float(np.linalg.norm(dd@g-g@dd)/max(np.linalg.norm(dd)*np.linalg.norm(g),1e-300)),
                coherence_relaxation_over_orbit=float(ev.min()/snap['history']['omega']))
            currents={};ci={};ca={};ce={}
            for key,w in weighted.items():
                da=w['loss'][i]-w['gain'][i];gg=w['gain'][i]
                currents[key]=float(np.trace(da@rho-gg));ci[key]=float(np.trace(da@riso-gg));ca[key]=float(np.trace(da@cur-gg));ce[key]=float(np.trace(da@equal-gg))
                coh_channels[key]+=W[i]*currents[key];iso_channels[key]+=W[i]*ci[key];current_channels[key]+=W[i]*ca[key];equal_channels[key]+=W[i]*ce[key]
            item['coherent_channel_net_decay_currents']=currents;item['isotropic_channel_net_decay_currents']=ci
            item['stationary_trace_residual']=abs(sum(currents.values()))/max(float(np.trace(g)+np.trace(loss[i]@rho)),1e-300)
            item['minimum_rho_eigenvalue']=float(np.linalg.eigvalsh(rho).min())
        rows.append(item)
    def charged(ch):return -sum(packet['channels'][key]['charged_carriers']*v for key,v in ch.items())
    C=charged(coh_channels);I=charged(iso_channels);A=charged(current_channels);EQ=charged(equal_channels)
    return dict(parent_id=packet['parent_id'],parent_indices=packet['P'],momentum_rows=rows,
          coherent_stationary_channel_current_mu4=coh_channels,isotropic_stationary_channel_current_mu4=iso_channels,
          actual_isotropic_channel_current_mu4=current_channels,equal_coherent_trace_isotropic_channel_current_mu4=equal_channels,
          coherent_stationary_charged_loss_mu4=C,isotropic_stationary_charged_loss_mu4=I,
          actual_isotropic_charged_loss_mu4=A,equal_coherent_trace_isotropic_charged_loss_mu4=EQ,
          coherent_over_isotropic_stationary_charged_loss=C/I if I else None,
          coherent_over_equal_trace_isotropic_charged_loss=C/EQ if EQ else None,
          min_net_width=float(np.linalg.eigvalsh(D).min()),max_net_width=float(np.linalg.eigvalsh(D).max()),
          parent_number_coherent_mu3=float(sum(W[i]*sum(r.get('rho_eigenvalues',[0.])) for i,r in enumerate(rows))),
          parent_number_isotropic_mu3=float(sum(W[i]*4*r.get('isotropic_steady_f',0.) for i,r in enumerate(rows))))

def serialize(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    if isinstance(v,dict):return {k:serialize(x) for k,x in v.items()}
    if isinstance(v,list):return [serialize(x) for x in v]
    return v
