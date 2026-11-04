"""Follow protected local minimum with finite rigid normal/two-loop action."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,time,resource
from pathlib import Path
import mpmath as mp
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import solve_protected as p
mp.mp.dps=100
DATA=json.loads((HERE/'canonical_coefficients_snapshot.json').read_text())
DOMAIN=list(map(lambda x:mp.mpf(str(x)),DATA['domain']))
A0=p.Q0/mp.sqrt(30);DE=mp.mpf('2.52e-47')/p.MU**4


def cf(key,s,nodes):
    co=[mp.mpf(str(v)) for v in DATA['fits'][str(nodes)][key]]
    x=(2*s-sum(DOMAIN))/(DOMAIN[1]-DOMAIN[0]);v0=mp.mpf(1);v1=x;ans=co[0]+co[1]*x
    for a in co[2:]:v0,v1=v1,2*x*v1-v0;ans+=a*v1
    return ans*(p.E/mp.mpf(str(DATA['e0'])))**mp.mpf(str(DATA['powers'][key]))


def loop(tau,z,w,nodes):
    T,N,q=z;X=(T+mp.sqrt(30)*N)/mp.sqrt(31);BD=(mp.sqrt(30)*T-N)/mp.sqrt(31)
    s=mp.log(abs(X)/(p.R0/mp.sqrt(31)))
    # Linear normal expansion of rigid CW; invariant under common X,B R phase.
    u=mp.re(q)/mp.sqrt(30)-A0
    v=mp.re(BD*mp.conj(X)/abs(X))/mp.sqrt(30)-abs(X)
    return p.cw(abs(X),p.E,p.E,p.G)+cf('ja',s,nodes)*u+cf('jb',s,nodes)*v+cf('U2diag',s,nodes)


def unpack(t,ns,qa,ds,ww):
    nn=mp.mpf('1e-6')*ns
    return mp.mpf('.5')+p.EPS/p.BC*ds/2,[p.R0*t-mp.sqrt(30)*nn,nn,p.Q0*(1+mp.mpf('1e-8')*qa)],ww


def solve(nodes):
    def pot(*args):
        tau,z,w=unpack(*args)
        return p.data(tau,z,w)['V']+loop(tau,z,w,nodes)
    def eq(*args):
        ds=[mp.diff(lambda x:pot(*(list(args[:i])+[x]+list(args[i+1:]))),args[i]) for i in range(4)]
        return ds[0]/p.E**2,ds[1]/mp.mpf('1e-12'),ds[2]/(p.Q0**2*mp.mpf('1e-16')),ds[3]/(p.EPS/p.BC),pot(*args)-DE
    s=mp.log(mp.mpf('1.027'));da=-cf('ja',s,nodes)/(120*p.E);db=-cf('jb',s,nodes)/(120*p.E/31)
    root=mp.findroot(eq,(mp.mpf('1.027'),-mp.sqrt(mp.mpf(30)/31)*db/mp.mpf('1e-6'),da/A0/mp.mpf('1e-8'),-1/(24*p.NEXP),1),tol=mp.mpf('1e-80'),maxsteps=30)
    tau,z,w=unpack(*root);d=p.data(tau,z,w)
    # Neutral Hessian from this finite action. Its heavy scalar mass accuracy
    # excludes quadratic normal CW, while light Schur masses use the linear
    # normal source consistently through the finite two-loop energy order.
    p.ucw=lambda tau,z,w:loop(tau,z,w,nodes)
    mats=p.neutral_matrices(tau,z,w)
    masses=[mp.sqrt(v)*p.MU for v in mats['scalar_masses2']]
    m32=d['Y']**(-p.NEXP/2)*d['W']/p.M**2*p.MU
    x=(z[0]+mp.sqrt(30)*z[1])/mp.sqrt(31)
    dd=p.build_model(float(x),float(p.E),float(p.E),float(p.G),vertices=False);ext,labels=p.ext_basis(dd);gg,_=p.summarize(p.threshold(dd,ext),labels)
    mchi=p.MU*abs(gg['U1']['signed_mass'])
    zeta=p.EPS/p.NEXP*m32
    life=mp.mpf('6.582119569e-25')*16*mp.pi*(p.MU**4/31)/(mchi**5*(p.NEXP/3))
    return dict(nodes=nodes,t=str(root[0]),tau_real=str(tau),W0_GeV3=str(p.WBASE*w*p.MU**3),net_V_GeV4=str(pot(*root)*p.MU**4),target_V_GeV4='2.52e-47',equation_residual=str(max(abs(v) for v in eq(*root))),T_GeV=str(z[0]*p.MU),X_GeV=str(x*p.MU),N_GeV=str(z[1]*p.MU),Q_GeV=str(z[2]*p.MU),relative_a_shift=str(z[2]/p.Q0-1),relative_b_shift=str(-mp.sqrt(mp.mpf(31)/30)*z[1]/x),neutral_scalar_masses_GeV=[float(v) for v in masses],m32_GeV=float(m32),leading_Ward_zeta_GeV=float(zeta),photino_GeV=float(mchi),leading_current_partial_lifetime_seconds=float(life),phase_pair_open=bool(masses[1]>2*masses[0]),min_metric_eigenvalue=str(min(mats['metric_eigenvalues'])),DH=str(d['DH']),Y=str(d['Y']),fermion_scope='Leading epsilon/n m32 estimate; full loop neutral matrix is not replaced by the incomplete tree+TT-only matrix at displaced normals.')


def main(out):
    start=time.monotonic();rows=[solve(n) for n in (21,29)]
    conv={k:abs(float(rows[1][k])/float(rows[0][k])-1) for k in ('t','m32_GeV','photino_GeV')}
    conv['sigma']=abs(rows[1]['neutral_scalar_masses_GeV'][1]/rows[0]['neutral_scalar_masses_GeV'][1]-1)
    checks=dict(converged=max(conv.values())<1e-6,neutral_scalar_positive=all(min(r['neutral_scalar_masses_GeV'])>0 for r in rows),phase_open=all(r['phase_pair_open'] for r in rows),DE_residual_tuned=all(abs(mp.mpf(r['net_V_GeV4'])/mp.mpf('2.52e-47')-1)<mp.mpf('1e-15') for r in rows),equation_residual=all(mp.mpf(r['equation_residual'])<mp.mpf('1e-60') for r in rows))
    result=dict(claim_id='PG06_FINITE_NORMAL_LOCAL',checks={k:bool(v) for k,v in checks.items()},rows=rows,convergence=conv,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                scope='Exact neutral tree SUGRA plus rigid CW valley, linear CW heavy-normal sources and unreduced two-loop diagrams; no double-counted U2red. Canonicalized neutral tree+finite-action Hessian.',
                non_claims=['No finite SUGRA loops/current/anomaly threshold matching','No full transverse quantum Hessian','No physical neutral fermion pole from the partially completed matrix','DE is tuned within the finite action, not predicted'])
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
