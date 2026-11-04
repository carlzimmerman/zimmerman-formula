"""Independent differentiation and Ward/current controls; no author code import."""
import sys
sys.dont_write_bytecode = True
import json, resource, time
from pathlib import Path
import sympy as s
import mpmath as mp


def main(out):
    start = time.monotonic()
    # Independent holomorphic/antiholomorphic variables and a third-order H
    # jet around the leading stabilized point; its stated range is the
    # small-field, leading-gravity jet, not the exact finite vacuum.
    x, xb, t, tb = s.symbols('x xb t tb', real=True)
    n, w, f = s.symbols('n w f', positive=True)
    ep = 3-n
    H = 1+x+xb-ep/(2*n)*(x*x*xb+x*xb*xb)
    K = -n*s.log(H-t*tb/n)
    W = w+f*t
    zz, bb = [x,t], [xb,tb]
    origin = {x:0,xb:0,t:0,tb:0}
    ev = lambda a: s.simplify(a.subs(origin))
    metric = s.Matrix([[ev(s.diff(K,zi,bj)) for bj in bb] for zi in zz])
    gi = metric.inv()
    D = [s.diff(W,zi)+s.diff(K,zi)*W for zi in zz]
    raw = s.zeros(2)
    for i in range(2):
        for j in range(2):
            gam = [sum(gi[k,l]*ev(s.diff(K,zz[i],zz[j],bb[l])) for l in range(2)) for k in range(2)]
            raw[i,j] = ev(s.diff(D[j],zz[i])+s.diff(K,zz[i])*D[j])-sum(gam[k]*ev(D[k]) for k in range(2))
    C = s.diag(1/s.sqrt(n),1)
    raw_can = s.simplify((C.T*raw*C/w).subs(f,s.sqrt(ep)*w))
    Fvec = s.Matrix([-s.sqrt(n),s.sqrt(ep)])
    eta = Fvec/s.sqrt(3)
    zeta = s.Matrix([s.sqrt(ep),s.sqrt(n)])/s.sqrt(3)
    # Reconstruct exactly the added TT correction used by the leading
    # rigid-current Ward prescription; it is an input, not a pole derivation.
    prescription = raw_can+s.diag(0,ep)
    unitary = s.simplify(prescription-s.Rational(2,3)*Fvec*Fvec.T)
    a = s.symbols('a',real=True)
    family = unitary+a*zeta*zeta.T
    checks = {
        'metric_is_diag_n_1': metric == s.diag(n,1),
        'raw00': s.simplify(raw_can[0,0]-(n-1+ep/n))==0,
        'raw01': s.simplify(raw_can[0,1]+(n-1)*s.sqrt(ep/n))==0,
        'raw11_zero': raw_can[1,1]==0,
        'modulus_tree_ward_stationary': s.simplify((raw_can*Fvec-2*Fvec)[0])==0,
        'matter_tree_ward_requires_eps_correction': s.simplify((raw_can*Fvec-2*Fvec)[1]+ep*s.sqrt(ep))==0,
        'prescription_satisfies_all_leading_ward': all(s.simplify(v)==0 for v in prescription*Fvec-2*Fvec),
        'family_satisfies_same_ward_null': all(s.simplify(v)==0 for v in family*eta),
        'family_uneaten_eigenvalue_eps_over_n_plus_a': s.simplify((zeta.T*family*zeta)[0]-(ep/n+a))==0,
        'current_projection_squared_n_over_3': s.simplify(zeta[1]**2-n/3)==0,
    }
    # Finite packet: independently construct full complex metric and D W.
    mp.mp.dps=100
    here=Path(__file__).resolve().parent
    packet=json.loads((here.parent/'protected/run_export_002/result.json').read_text())
    p=packet['normalized_packet'];co={k:mp.mpf(v) for k,v in p['constants'].items()}
    tau=mp.mpf(p['tau']);z=list(map(mp.mpf,p['z']))
    M,MU,nn=co['M'],co['MU'],co['NEXP'];eps=3-nn
    w0=co['WBASE']*mp.mpf(p['w0_normalized'])
    T,N,q=z;ss=2*tau
    H=ss+co['BC']*(ss-1)**4
    P=1+4*co['BC']*(ss-1)**3
    Q=12*co['BC']*(ss-1)**2
    Y=H-sum(v*v for v in z)/(nn*M*M)
    g=mp.zeros(4);g[0,0]=nn*M*M*(P*P/Y**2-Q/Y)
    for i in range(3):
        g[0,i+1]=g[i+1,0]=-P*z[i]/Y**2
        for j in range(3):g[i+1,j+1]=(int(i==j)/Y+z[i]*z[j]/(nn*M*M*Y**2))
    gi=g**-1
    Wi=[co['F'],co['AA']-co['KK']*q*q/2,-co['KK']*N*q]
    Ki=mp.matrix([-nn*M*M*P/Y]+[v/Y for v in z])
    Wmatter=co['F']*T+co['AA']*N-co['KK']*N*q*q/2
    def pieces(ww):
        W=Wmatter+ww
        D=mp.matrix([0]+Wi)+Ki*W/(M*M)
        pos=Y**(-nn)*(D.T*gi*D)[0]
        neg=-3*Y**(-nn)*W*W/(M*M)
        return pos,neg,pos+neg
    pos,neg,V=pieces(w0)
    dV=mp.diff(lambda ww:pieces(ww)[2],w0)
    dp=mp.diff(lambda ww:pieces(ww)[0],w0)
    dn=mp.diff(lambda ww:pieces(ww)[1],w0)
    de=mp.mpf('2.52e-47')/MU**4
    fhidden=co['F']*MU**2
    mchi=mp.mpf(str(packet['preferred_row']['photino_GeV']))
    hbar=mp.mpf('6.582119569e-25')
    width0=nn/3*mchi**5/(16*mp.pi*fhidden*fhidden)
    checks['direct_metric_W0_slope_matches_eps'] = abs(dV/(-2*eps*(Wmatter+w0)/(M*M))-1)<mp.mpf('1e-10')
    checks['slope_not_unadjusted_total_auxiliary'] = abs(dp/dn+1)<mp.mpf('1e-3') and abs(dV/dn)<mp.mpf('1e-3')
    result={
        'claim_id':'PG06_INDEPENDENT_WARD_CURRENT_AUDIT',
        'checks':checks,
        'raw_canonical_over_m32':str(raw_can),
        'unitary_prescription_over_m32':str(unitary),
        'ward_null_deformation_over_m32':str(a*zeta*zeta.T),
        'uneaten_family_eigenvalue_over_m32':str(ep/n+a),
        'finite_packet':{
            'Fhidden_GeV2':str(fhidden),'positive_auxiliary_GeV4':str(pos*MU**4),
            'negative_universal_GeV4':str(neg*MU**4),
            'positive_auxiliary_over_rhoDE':str(pos/de),
            'Fhidden2_over_rhoDE':str(fhidden*fhidden/mp.mpf('2.52e-47')),
            'fractional_W0_precision_from_envelope_slope':str(abs(de/(w0*dV))),
            'dV_dW0_GeV':str(dV*MU),
            'slope_relative_to_minus_2epsW_over_M2':str(dV/(-2*eps*(Wmatter+w0)/(M*M))),
            'positive_auxiliary_slope_GeV':str(dp*MU),
            'negative_term_slope_GeV':str(dn*MU),
            'leading_fixed_current_massless_width_GeV':str(width0),
            'leading_fixed_current_partial_lifetime_lower_bound_s':str(hbar/width0),
            'incorrect_Ftotal_lifetime_enhancement':str(3/eps)
        },
        'runtime_seconds':time.monotonic()-start,
        'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'scope':'Exact symbolic leading-jet/Ward reconstruction and one finite-packet direct-metric derivative. No matched pole/current or total loss bound.'
    }
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert all(checks.values()),checks


if __name__=='__main__': main(sys.argv[1])
