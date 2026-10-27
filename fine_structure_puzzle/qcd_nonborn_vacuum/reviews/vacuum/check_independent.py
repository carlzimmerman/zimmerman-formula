"""Independent direct analytic differentiation, no imports of author programs."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

t, u, eta = s.symbols('t u eta', real=True)
zero = {t: 0, u: 0}
checks = []


def equal(name, actual, expected=0):
    difference = s.simplify(actual - expected)
    if difference != 0:
        raise AssertionError((name, str(difference)))
    checks.append(name)


def moments(weights):
    total = sum(weights)
    def mean(a):
        return sum(w*x for w, x in zip(weights, a))/total
    def covariance(a, b):
        return mean([x*y for x, y in zip(a, b)]) - mean(a)*mean(b)
    def third(a, b, c):
        return mean([(x-mean(a))*(y-mean(b))*(z-mean(c))
                     for x, y, z in zip(a, b, c)])
    def fourth(a, b, c, d):
        centered = mean([(x-mean(a))*(y-mean(b))*(z-mean(c))*(v-mean(d))
                         for x, y, z, v in zip(a, b, c, d)])
        return (centered-covariance(a,b)*covariance(c,d)
                -covariance(a,c)*covariance(b,d)-covariance(a,d)*covariance(b,c))
    return mean, covariance, third, fourth


def ensemble(f):
    weights = [s.Rational(1, 2), s.Rational(1, 3), s.Rational(1, 6)]
    actions = []
    for i in range(3):
        # Independently chosen nonlinear analytic actions, all mixed contacts.
        a, b = i+1, f+1
        actions.append(s.Rational(a-b,3)*t + s.Rational(a*b+1,5)*t**2
                       + s.Rational(a+2*b,7)*t**3
                       + u*(s.Rational(a*a-b,4)+s.Rational(2*a+b,6)*t
                            +s.Rational(a-2*b,9)*t**2+s.Rational(a*b-2,11)*t**3))
    w = -s.log(sum(p*s.exp(-a) for p,a in zip(weights,actions)))
    def dw(nt, nu=0):
        return s.diff(w,t,nt,u,nu).subs(zero).doit()
    def da(nt, nu=0):
        return [s.diff(a,t,nt,u,nu).subs(zero) for a in actions]
    mean,cov,k3,k4 = moments(weights)
    x,y,z,j,xu,yu,zu = da(1),da(2),da(3),da(0,1),da(1,1),da(2,1),da(3,1)
    bvec = [yy-4*xx for xx,yy in zip(x,y)]
    cvec = [yy-4*xx for xx,yy in zip(xu,yu)]
    hvec = [zz-6*yy+8*xx for xx,yy,zz in zip(x,y,z)]
    huvec = [zz-6*yy+8*xx for xx,yy,zz in zip(xu,yu,zu)]
    fvec = [bb-(xx-mean(x))**2 for bb,xx in zip(bvec,x)]
    e = mean(bvec)-cov(x,x)
    eu = mean(cvec)-2*cov(x,xu)-cov(fvec,j)
    k = mean(hvec)-3*cov(x,y)+6*cov(x,x)+k3(x,x,x)
    ku = (mean(huvec)-cov(hvec,j)-3*cov(xu,y)-3*cov(x,yu)
          +3*k3(x,y,j)+12*cov(x,xu)-6*k3(x,x,j)
          +3*k3(xu,x,x)-k4(x,x,x,j))
    prefix='direct_analytic_%d_' % f
    equal(prefix+'Wt',dw(1),mean(x))
    equal(prefix+'Wtt',dw(2),mean(y)-cov(x,x))
    equal(prefix+'E',dw(2)-4*dw(1),e)
    equal(prefix+'Eu',dw(2,1)-4*dw(1,1),eu)
    equal(prefix+'K',dw(3)-6*dw(2)+8*dw(1),k)
    equal(prefix+'Ku',dw(3,1)-6*dw(2,1)+8*dw(1,1),ku)
    # Bound uses the exact nonnegative rational terms under the radicals.
    v1,v2 = cov(x,x)*cov(xu,xu),cov(fvec,fvec)*cov(j,j)
    assert v1>=0 and v2>=0
    assert cov(x,xu)**2<=v1 and cov(fvec,j)**2<=v2
    assert s.N(abs(mean(cvec))+2*s.sqrt(v1)+s.sqrt(v2)-abs(eu),80)>=0
    checks.append(prefix+'actual_CS_triangle_bound_80_digits')
    return {'fixture':f,'E':str(e),'Eu':str(eu),'K':str(k),'Ku':str(ku)}


def source_checks():
    # Different discriminator from the author's occupied-cell product measure:
    # scalar norm constant, parity-symmetric Hodge chirality including a zero-q state.
    weights = [s.Rational(1,4),s.Rational(1,2),s.Rational(1,4)]
    scalar = [s.Integer(1)]*3
    topo = [s.Integer(-1),s.Integer(0),s.Integer(1)]
    m,c,_,_ = moments(weights)
    for a,b in zip(scalar,topo):
        assert a>=abs(b)
    equal('constant_norm_scalar_variance',c(scalar,scalar))
    equal('parity_topological_mean',m(topo))
    equal('constant_norm_topological_variance',c(topo,topo),s.Rational(1,2))
    assert m([a*a for a in scalar]) >= m([q*q for q in topo])
    assert c(scalar,scalar)<c(topo,topo)
    checks.append('raw_order_does_not_imply_connected_order')
    j,theta = s.symbols('j theta',real=True)
    logz=s.log(sum(p*s.exp(-j*a+s.I*theta*q) for p,a,q in zip(weights,scalar,topo)))
    equal('independent_scalar_log_partition',s.diff(logz,j,2).subs({j:0,theta:0}),0)
    equal('independent_topological_log_partition',-s.diff(logz,theta,2).subs({j:0,theta:0}),s.Rational(1,2))

    # Read author's stored finite controls, compare to independent product-law
    # moment factorization rather than rerunning enumeration.
    path=Path('fine_structure_puzzle/qcd_nonborn_vacuum/coordinator/vacuum_let/run_001/RESULTS.json')
    author=json.loads(path.read_text())
    for row in author['rows']:
        p,n=s.Rational(row['p_zero']),row['N']
        equal('stored_LET_mean_%s_%d'%(p,n),s.Rational(row['mean_S']),n*(1-p))
        equal('stored_LET_scalar_%s_%d'%(p,n),s.Rational(row['variance_S']),n*p*(1-p))
        equal('stored_LET_topological_%s_%d'%(p,n),s.Rational(row['variance_Q']),n*(1-p))
        equal('stored_LET_raw_%s_%d'%(p,n),s.Rational(row['raw_gap']),n*(n-1)*(1-p)**2)
    equal('stored_LET_case_count',author['finite_cases'],24)
    equal('stored_LET_configuration_count',author['configurations_summed'],4*sum(3**n for n in range(1,7)))


def metric_checks():
    om,a,e0,c=s.symbols('Omega A E0 c', real=True)
    v=om*s.exp(4*t)
    w=e0*v+s.Rational(4,3)*om*a*s.exp(3*t)+c*s.exp(2*t)
    rho=s.diff(w,t)/(4*v)
    response=-s.exp(t)*s.diff(rho,t)
    equal('flat_plus_A_plus_Einstein_response',response,a+c*s.exp(-t)/om)
    equal('large_radius_A_limit',s.limit(response,t,s.oo),a)
    # Distinct paired thermal-action fixture with four reflected sites.
    coords=[-3,-1,1,3]
    ev=[s.Rational(1,7),s.Rational(2,5),s.Rational(3,4),s.Rational(1,2)]
    bv=[s.Rational(-1,12),s.Rational(1,6),s.Rational(2,9),s.Rational(4,3)]
    beta=s.Rational(5,2)
    action=beta*sum(ee/(1+eta*z)+(1+eta*z)*bb for z,ee,bb in zip(coords,ev,bv))
    reflected=action.subs(eta,-eta)
    w=-s.log((s.exp(-action)+s.exp(-reflected))/2)
    x=s.diff(action,eta).subs(eta,0)
    y=s.diff(action,eta,2).subs(eta,0)
    equal('Rindler_reflection_first',s.diff(w,eta).subs(eta,0))
    equal('Rindler_fixed_bare_contact_hessian',s.diff(w,eta,2).subs(eta,0),y-x*x)
    equal('Rindler_action_x',x,beta*sum(z*(bb-ee) for z,ee,bb in zip(coords,ev,bv)))
    equal('Rindler_action_y',y,2*beta*sum(z*z*ee for z,ee in zip(coords,ev)))


def pin_check():
    base=Path(__file__).parent
    inp=json.loads((base/'INPUTS.json').read_text())
    after={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in inp['author_sha256_before']}
    assert after==inp['author_sha256_before']
    source_after={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in inp['source_sha256']}
    assert source_after==inp['source_sha256']
    checks.append('all_27_author_artifacts_and_3_source_bytes_unchanged')
    return after,source_after


def main(result):
    fixtures=[ensemble(f) for f in range(3)]
    source_checks()
    metric_checks()
    after,source_after=pin_check()
    out={'status':'passed','assertion_tested':'Independent direct analytic normalized partition derivatives, source inference discriminator, author LET row moment checks and metric/contact fixtures',
         'checks':checks,'check_count':len(checks),'fixtures':fixtures,
         'author_sha256_after':after,'source_sha256_after':source_after,
         'physical_A':None,'physical_R':None,'physical_alpha':None,
         'non_claims':['No QCD ensemble simulated','No theorem about H-limit uniformity','No physical source numerical bound refuted','CS radical check alone is numerical; its bound is analytically derived in PRETARGET.md']}
    Path(result).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'passed','check_count':len(checks),'analytic_ensembles':len(fixtures),'physical_A':None,'physical_R':None,'physical_alpha':None}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--result',required=True)
    main(parser.parse_args().result)
