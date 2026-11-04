"""Independent pointwise differentiated quadrature and FD step discrimination."""
import critical_checks as c

def differentiated_quadrature(data,t,q,W,f):
    np=c.np;math=c.math;n=len(q);ng=len(data['groups']);en=np.array([np.sqrt(g['mass']**2+(t*q)**2) for g in data['groups']])
    eta=np.repeat([1 if g['kind']=='S' else -1 for g in data['groups']],n);av=1+eta*f
    measure=np.concatenate([g['degeneracy']*W/(2*np.pi**2) for g in data['groups']]);out=np.zeros((ng*n,ng*n))
    M=3.;m1=.4;m2=.4 if ng==2 else .7;k=1 if ng==2 else 2
    estar=(M*M+m1*m1-m2*m2)/(2*M);pstar=math.sqrt((M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2))/(2*M)
    for i,ep in enumerate(en[0]):
        e10=ep*estar/M;slope=t*q[i]*pstar/M;cuts=[]
        if slope:
            cuts.extend(((en[1]-e10)/slope).tolist());cuts.extend(((en[k]-(ep-e10))/(-slope)).tolist())
        cuts=sorted(set(z for z in cuts if -1<z<1))
        def derivative(z):
            idx=[i];weights=[1.]
            for g,target in zip((1,k),(e10+slope*z,ep-e10-slope*z)):
                if target<en[g,0] or target>en[g,-1]:return np.zeros_like(out)
                lo=min(max(int(np.searchsorted(en[g],target)-1),0),n-2);b=(target-en[g,lo])/(en[g,lo+1]-en[g,lo]);idx.extend([g*n+lo,g*n+lo+1]);weights.extend([1-b,b])
            idx=np.array(idx);weights=np.array(weights);F=f[i]*np.prod(av[idx[1:]]**weights[1:]);R=av[i]*np.prod(f[idx[1:]]**weights[1:]);grad=np.zeros(ng*n);nu=np.zeros(ng*n)
            grad[i]=(F/f[i]-R*eta[i]/av[i])/measure[i]
            np.add.at(grad,idx[1:],weights[1:]*(F*eta[idx[1:]]/av[idx[1:]]-R/f[idx[1:]])/measure[idx[1:]])
            np.add.at(nu,idx,np.array([-1,1,1,1,1])*weights)
            return nu[:,None]*grad[None,:]
        integral=c.quad_vec(derivative,-1,1,points=cuts,epsabs=1e-10,epsrel=1e-11)[0]
        out+=measure[i]*.03*M/ep/2*integral
    return out


def main(out):
    start=c.time.monotonic();np=c.np;q=np.array([0.,.1,.7,1.6,4.,8.]);edges=np.r_[0.,(q[:-1]+q[1:])/2,10.];W=np.diff(edges**3)/3;rows=[]
    for duplicate in (False,True):
        data=c.toy_data(duplicate);ev=c.exact_events(data,.6,q,W);f=.25+.12*np.sin(np.arange(len(ev.measure)));av=1+ev.eta*f;J=ev.number_jacobian(f,av).toarray();ref=differentiated_quadrature(data,.6,q,W,f);steps=[]
        for h in (1e-3,3e-4,1e-4,3e-5,1e-5,2e-6):
            FD=np.zeros_like(J)
            for j in range(len(f)):
                plus=f.copy();minus=f.copy();plus[j]+=h;minus[j]-=h
                FD[:,j]=(ev.number_rhs(plus,1+ev.eta*plus)-ev.number_rhs(minus,1+ev.eta*minus))/(2*h*ev.measure[j])
            steps.append(dict(occupation_step=h,relative=float(np.linalg.norm(FD-ref)/np.linalg.norm(ref))))
        signs=[]
        for mode in (0,1,2):
            holes=(ev.eta<0)&((np.arange(len(f))+mode)%3!=0);state=c.QuantumState(ev.measure,ev.eta,Z=np.where(holes,ev.measure*(1-f),ev.measure*f),holes=holes);s=np.where(holes,-1.,1.)
            expected=s[:,None]*ref*s[None,:];signs.append(float(np.linalg.norm(state.jacobian(ev).toarray()-expected)/np.linalg.norm(expected)))
        rows.append(dict(duplicate=duplicate,differentiated_quadrature_relative=float(np.linalg.norm(J-ref)/np.linalg.norm(ref)),coordinate_chain_relative=signs,finite_difference_steps=steps))
    checks=dict(pointwise_derivative=max(r['differentiated_quadrature_relative'] for r in rows)<1e-11,coordinate_sign_chain=max(max(r['coordinate_chain_relative']) for r in rows)<1e-11,FD_discrimination=max(min(v['relative'] for v in r['finite_difference_steps']) for r in rows)<1e-7)
    r=dict(rows=rows,checks=checks,runtime_seconds=c.time.monotonic()-start,peak_rss_bytes_macos=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss)
    c.Path(out).write_text(c.json.dumps(r,indent=2)+'\n');print(c.json.dumps(r));assert all(checks.values()),checks

if __name__=='__main__':main(c.sys.argv[1])
