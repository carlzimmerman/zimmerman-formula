"""Independent three-canonical-field reconstruction of a serialized candidate.

No canonical/ solver code is imported. Loop coefficients are frozen data;
the microscopic F potential is constructed from holomorphic W derivatives.
"""
import sys
sys.dont_write_bytecode = True
import json
from pathlib import Path
import resource
import time
import mpmath as mp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from pressure_scan import cw
mp.mp.dps = 120


def main(path):
    start = time.monotonic()
    source = json.loads((HERE/'canonical/run_highprecision/result.json').read_text())
    data = source['export']
    p = data['parameters']
    e, z0, Planck, mu, s, u, v, ratio, y = [mp.mpf(p[k]) for k in
        ('e','z0','Mp_GeV','mu','s','u','v','p','y')]
    x0 = z0/mp.sqrt(31*e)
    a0 = mp.sqrt(2/(31*e))
    root30 = mp.sqrt(30)
    domain = list(map(mp.mpf, data['coefficient_domain']))

    def coeff(key, ss):
        xi = (2*ss-sum(domain))/(domain[1]-domain[0])
        # Direct Chebyshev evaluation is independent of the solver's recurrence.
        co = list(map(mp.mpf, data['coefficient_strings'][key]))
        value = sum(c*mp.chebyt(j,xi) for j,c in enumerate(co))
        return value*(e/mp.mpf(data['coefficient_e0']))**mp.mpf(data['powers'][key])

    def tree(ss, uu, vv, theta=mp.mpf(0), ca=mp.mpf(0), cb=mp.mpf(0)):
        x = x0*mp.exp(ss)
        a, b = a0+uu+1j*ca, x+vv+1j*cb
        phase = mp.exp(1j*theta)
        z = [x*phase, 1j*root30*a, root30*b*phase]
        w = z[0]+e*z[0]*z[1]**2/2-e*z[1]**2*z[2]/(2*root30)+ratio*y
        dw = [1+e*z[1]**2/2, e*z[1]*(z[0]-z[2]/root30), -e*z[1]**2/(2*root30)]
        K = sum(abs(a)**2 for a in z)
        D = [wi+mp.conj(zi)*w/ratio**2 for zi,wi in zip(z,dw)]
        return mp.re(mp.exp(K/ratio**2)*(sum(abs(a)**2 for a in D)-3*abs(w)**2/ratio**2))

    def potential(ss,uu,vv):
        x = x0*mp.exp(ss)
        return tree(ss,uu,vv)+cw(x,e,e,mp.sqrt(mp.mpf(29)/200)*e)+coeff('ja',ss)*uu+coeff('jb',ss)*vv+coeff('U2diag',ss)

    point = [s,u,v]
    gradient = mp.matrix([mp.diff(lambda z:potential(*(point[:i]+[z]+point[i+1:])),point[i]) for i in range(3)])
    H = mp.matrix(3,3)
    for i in range(3):
        for j in range(i,3):
            if i==j:
                H[i,j] = mp.diff(lambda z:potential(*(point[:i]+[z]+point[i+1:])),point[i],2)
            else:
                def mixed(z,w):
                    q=point[:];q[i]=z;q[j]=w
                    return potential(*q)
                H[i,j]=mp.diff(lambda z:mp.diff(lambda w:mixed(z,w),point[j]),point[i])
            H[j,i]=H[i,j]
    heavy = H[1:3,1:3]
    mixing = H[1:3,0:1]
    response = -mp.lu_solve(heavy,mixing)
    curvature = H[0,0]+(mixing.T*response)[0]
    x=x0*mp.exp(s);b=x+v
    A=x*x+30*response[0]**2+30*(x+response[1])**2+coeff('rgraph',s)
    F=x*x+30*b*b+coeff('kgraph',s)
    phase_curvature=mp.diff(lambda q:tree(s,u,v,q),0,2)
    ms=mu*mp.sqrt(curvature/(2*A))
    ma=mu*mp.sqrt(phase_curvature/(2*F))
    net=potential(s,u,v)*mu**4
    rho=mp.mpf(p['rhoDE_GeV4'])
    expected=source['candidate']
    # Candidate export's clean row names are source-defined data, not code.
    reference=json.loads((HERE/'canonical/run_solve/result.json').read_text())['points'][-1]
    last=reference['rows'][-1]
    controls={
        'serialized_net_V_GeV4':mp.nstr(net,80),
        'DE_relative_error':mp.nstr(abs(net/rho-1),20),
        'max_dimensionless_gradient':mp.nstr(max(abs(z) for z in gradient),20),
        'm_sigma_GeV':float(ms), 'm_phase_GeV':float(ma),
        'radial_relative_difference_from_five_point':float(abs(ms/mp.mpf(str(last['m_sigma_GeV']))-1)),
        'phase_relative_difference':float(abs(ma/mp.mpf(str(last['m_phase_GeV']))-1)),
        'heavy_H_determinant':float(mp.det(heavy)),
        'radial_reduced_curvature':float(curvature),
        'A_over_R2':float(A/(31*x*x)), 'F_over_R2':float(F/(31*x*x)),
        'high_precision_scale_difference':mp.nstr(abs(ratio*mu/Planck-1),20),
    }
    checks={
        'independent_matrix_F_potential_reproduces_tuned_action':abs(net/rho-1)<mp.mpf('1e-25'),
        'independent_stationarity':max(abs(z) for z in gradient)<mp.mpf('1e-90'),
        'heavy_normal_positive':heavy[0,0]>0 and mp.det(heavy)>0,
        'radial_Schur_positive':curvature>0,
        'kinetic_positive':A>0 and F>0,
        'analytic_curvature_matches_stencil':controls['radial_relative_difference_from_five_point']<1e-8,
        'phase_mass_matches':controls['phase_relative_difference']<1e-10,
        'phase_pair_closed':ma*2>ms,
        'serialized_scale_consistent':abs(ratio*mu/Planck-1)<mp.mpf('1e-95'),
    }
    result=dict(claim_id='TP06_INDEPENDENT_CANONICAL_MATRIX_AUDIT',checks={k:bool(v) for k,v in checks.items()},controls=controls,
                scope='Independent canonical3complex singlet F potential plus same frozen finite rigid loop coefficients. Checks truncated local stationary vacuum, not full physical loop super-Higgs, transverse99-field proof, total lifetime or cosmology.',
                runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(path).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
