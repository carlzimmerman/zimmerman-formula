"""Fresh CT09 controls: charge projection, unordered widths, expansion/action.

Does not import the CT09 pole implementation. The canonical component model
remains an explicit shared dependency. This file is confined to the review.
"""
import os, sys
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
from pathlib import Path
import json, math, time, resource
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'reviews/finite_matching_2026_11_01/two_loop'))
from model import build_model
from spectrum import d as dc


def action(beta):
    k, alpha, mass, n0, amp, p0 = 1., .7, 2., 1., .8, .9
    H, gam = 1e-4, 2e-4
    w0 = math.sqrt(k+alpha*n0)
    T = 2*math.pi/w0
    I0 = math.pi*w0*amp**2
    E0 = .5*w0*w0*amp**2+n0*(mass+p0*p0/(2*mass))
    def rhs(t,z):
        x,v,n,rad,work=z
        kin=p0*p0*math.exp(-2*H*t)/mass
        eps=mass+.5*alpha*x*x+.5*kin
        C=-gam*n*(1+beta*x*x)
        return [v,-3*H*v-(k+alpha*n)*x,-3*H*n+C,
                -4*H*rad-eps*C,3*H*(v*v+n*eps+n*kin/3)+4*H*rad]
    def avg(t,z):
        n,I=z;w=math.sqrt(k+alpha*n);A2=I/(math.pi*w)
        return [-3*H*n-gam*n*(1+beta*A2/2),
                -3*H*I-(2*math.pi/w)*gam*n*alpha*beta*A2*A2/16]
    def bad(t,z):
        n,I=z;w=math.sqrt(k+alpha*n);A2=I/(math.pi*w)
        return [-3*H*n-gam*n*(1+beta*A2/2),-3*H*I]
    def turn(t,z):return z[1]
    turn.direction=-1
    sol=solve_ivp(rhs,[0,80*T],[amp,0,n0,0,0],rtol=2e-11,atol=2e-14,
                  max_step=T/40,dense_output=True,events=turn)
    end=float(sol.t_events[0][-1]);x,v,n,rad,work=sol.sol(end)
    w=math.sqrt(k+alpha*n);If=math.pi*(v*v+w*w*x*x)/w
    av=solve_ivp(avg,[0,end],[n0,I0],rtol=2e-11,atol=2e-14)
    ba=solve_ivp(bad,[0,end],[n0,I0],rtol=2e-11,atol=2e-14)
    ts=np.linspace(0,end,2401);xx,vv,nn,rr,ww=sol.sol(ts)
    ep=mass+.5*alpha*xx*xx+p0*p0*np.exp(-2*H*ts)/(2*mass)
    energy=.5*vv*vv+.5*k*xx*xx+nn*ep+rr+ww
    return dict(beta=beta,H=H,gamma=gam,endpoint=end,
                relative_action_error=abs(If/av.y[1,-1]-1),
                relative_number_error=abs(n/av.y[0,-1]-1),
                omit_covariance_action_error=abs(If/ba.y[1,-1]-1),
                ledger_error=float(max(abs(energy/E0-1))),
                comoving_action_drift=math.exp(3*H*end)*If/I0-1,
                success=bool(sol.success and av.success and ba.success))


def pole():
    e=.003;g=math.sqrt(29/200)*e;M=math.sqrt(2*e)
    xp=math.sqrt(2/e-2/(31*e))
    d=build_model(xp,e,e,g,vertices=True)
    RY=np.einsum('a,aij->ij',dc/math.sqrt(30),d['R'])
    J=np.block([[-RY.imag,-RY.real],[RY.real,-RY.imag]])
    Q2=-J@J
    O=d['O'].copy();ms2=d['mS2'];used=np.zeros(98,bool)
    for i in range(98):
        if used[i]:continue
        ids=np.where(abs(ms2-ms2[i])<1e-11)[0];used[ids]=True
        b=O[:,ids];_,v=np.linalg.eigh(b.T@Q2@b);O[:,ids]=b@v
    qs=np.einsum('ia,ia->a',O,Q2@O)
    ms=np.sqrt(np.maximum(ms2,0));physical=(ms>1e-12)|(qs<.01)
    P=np.where((abs(ms-M)<1e-8)&(qs<.01))[0]
    m=min(ms[physical&(qs>.1)])
    L=np.where((abs(ms-m)<1e-8)&(qs>.1))[0]
    assert len(P)==4 and len(L)==12
    RS=d['O'].T@O
    cubic=np.einsum('ia,jb,kc,ijk->abc',RS,RS,RS,d['cubic'],optimize=True)
    yy=np.einsum('ijb,ba->ija',d['yukawa'],RS,optimize=True)
    C=cubic[P];prod=np.einsum('aij,bij->ab',C[:,L][:,:,L],C[:,L][:,:,L])/144
    # Incoming complex states are signed-charge eigenvectors of -i J.
    charge=-1j*O[:,L].T@J@O[:,L]
    q,V=np.linalg.eigh(charge)
    plus=V[:,q>.1];minus=V[:,q<-.1]
    assert plus.shape[1]==minus.shape[1]==6
    amp=np.einsum('iu,aij,jv->auv',plus,C[:,L][:,:,L],minus)
    pairgram=np.einsum('aij,bij->ab',amp,amp.conj()).real/36
    ss=np.zeros((4,4));ff=np.zeros((4,4));mf=d['mF']
    # Unordered two-body final states explicitly display the identical factor.
    for i in range(98):
        for j in range(i,98):
            if not (physical[i] and physical[j]) or ms[i]+ms[j]>=M*(1-1e-10):continue
            ri=(ms[i]/M)**2;rj=(ms[j]/M)**2
            beta=math.sqrt(max(0,(1-ri-rj)**2-4*ri*rj))
            ss+=np.outer(C[:,i,j],C[:,i,j])*beta/(16*math.pi*M*(1+(i==j)))
    for i in range(73):
        for j in range(i,73):
            if mf[i]+mf[j]>=M*(1-1e-10):continue
            zi=mf[i]/M;zj=mf[j]/M;ri=zi*zi;rj=zj*zj
            beta=math.sqrt(max(0,(1-ri-rj)**2-4*ri*rj));y=yy[i,j,P]
            term=(np.outer(y,y.conj()).real*(1-ri-rj)-2*np.outer(y,y).real*zi*zj)
            ff+=M*beta/(8*math.pi*(1+(i==j)))*term
    vac=ss+ff
    smax=2/(m*M*M)*float(np.trace(prod@np.linalg.inv(vac)))
    sssmax=2/(m*M*M)*float(np.trace(prod@np.linalg.inv(ss)))
    # Cubic normalization via a direct mixed third derivative of V_F+V_D.
    strongest=int(np.argmax([np.linalg.norm(C[a][np.ix_(L,L)]) for a in range(4)]))
    pa=O[:,P[strongest]];vv=O[:,L[0]];h=.25
    def pot(r):
        z=d['z']+(r[:49]+1j*r[49:])/math.sqrt(2)
        F=.5*np.einsum('ijk,j,k->i',d['Y'],z,z);F[0]+=1
        ds=g*np.einsum('i,aij,j->a',z.conj(),d['R'],z).real
        return float(np.vdot(F,F).real+.5*ds@ds)
    deriv=(pot(h*(pa+vv))+pot(h*(pa-vv))-2*pot(h*pa)
           -pot(h*(-pa+vv))-pot(h*(-pa-vv))+2*pot(-h*pa))/(2*h**3)
    stored=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_pole002/result.json').read_text())
    med=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_medium001/result.json').read_text())
    rng=np.random.default_rng(281114)
    residual=[]
    inv=np.linalg.inv(vac)/(M*M);scale=np.linalg.norm(inv,2)
    for j in range(128):
        a=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        H=(a+a.conj().T)*M*np.linalg.norm(vac)*10**((j%9-4)/2)
        b=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        incoming=b@b.conj().T*np.linalg.norm(vac)*10**((j%7-4)/2)
        D=np.linalg.inv(H+1j*M*(vac+incoming))
        r=inv-D@vac@D.conj().T
        residual.append(float(min(np.linalg.eigvalsh((r+r.conj().T)/2)))/scale)
    return dict(xpole=xp,m=m,M=M,charge_eigenvalues=q.tolist(),
        physical_pair_Gram_over_twice_real_relative_error=float(np.linalg.norm(pairgram-2*prod)/np.linalg.norm(pairgram)),
        direct_potential_cubic=deriv,vertex_cubic=float(C[strongest,L[0],L[0]]),
        potential_cubic_relative_error=float(abs(deriv/C[strongest,L[0],L[0]]-1)),
        sigma_max_mu_minus2=smax,sigma_bosonic_floor_mu_minus2=sssmax,
        recorded_sigma_relative_error=abs(smax/stored['sigma_pair_v_at_rest_mu_minus2']-1),
        recorded_bosonic_sigma_relative_error=abs(sssmax/med['sigma_pair_v_all_FFS_blocked_uniform_bound_mu_minus2']-1),
        vac_eigenvalues=np.linalg.eigvalsh(vac).tolist(),SSS_eigenvalues=np.linalg.eigvalsh(ss).tolist(),
        random_controls=128,min_normalized_order_residual=min(residual),
        uniform_component_averaging=6,correlated_component_upper_multiplier=6)


def main(output):
    start=time.monotonic();a=[action(b) for b in (-.8,0,.8)];p=pole()
    checks=dict(action_expansion_average=max(z['relative_action_error'] for z in a)<2e-5,
        action_energy_ledger=max(z['ledger_error'] for z in a)<1e-7,
        action_correct_sign=all(z['comoving_action_drift']*z['beta']<0 for z in a if z['beta']),
        covariance_material=all(z['omit_covariance_action_error']>10*z['relative_action_error'] for z in a if z['beta']),
        physical_pair_projection=p['physical_pair_Gram_over_twice_real_relative_error']<1e-10,
        direct_potential_cubic=p['potential_cubic_relative_error']<1e-7,
        reconstructed_vacuum_peak=p['recorded_sigma_relative_error']<1e-9,
        reconstructed_bosonic_peak=p['recorded_bosonic_sigma_relative_error']<1e-9,
        random_matrix_order=p['min_normalized_order_residual']>-1e-10)
    checks={k:bool(v) for k,v in checks.items()}
    result=dict(claim_id='CT09_INDEPENDENT_CONTROLS',checks=checks,action=a,pole=p,
        runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Finite independent controls only; shared canonical component model; no full collision history or finite physical pole match.')
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
