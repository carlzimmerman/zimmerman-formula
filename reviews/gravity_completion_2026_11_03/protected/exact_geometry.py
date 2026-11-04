"""Exact complex-metric and leading stationary-Goldstino discriminators."""
import sys
sys.dont_write_bytecode = True
import json, resource, time
from pathlib import Path
import sympy as s


def main(out):
    started = time.monotonic()
    H,P,Pb,Q,z,zb,n,W,Wb,F,Fb = s.symbols('H P Pb Q z zb n W Wb F Fb')
    Y=H-z*zb/n
    # Rows i, columns bar(j). Inverse has rows bar(j), columns i.
    metric=s.Matrix([[n*(P*Pb/Y**2-Q/Y),-P*z/Y**2],
                     [-Pb*zb/Y**2,1/Y+z*zb/(n*Y**2)]])
    D=s.Matrix([-n*P*W/Y,F+zb*W/Y])
    Db=s.Matrix([[-n*Pb*Wb/Y,Fb+z*Wb/Y]])
    direct=(Db*metric.inv()*D)[0]-3*W*Wb
    DH=P*Pb-H*Q
    reduced=Y*F*Fb+(n-3)*W*Wb+Y*Q*(z*F-n*W)*(zb*Fb-n*Wb)/(n*DH)
    checks={}
    checks['one_matter_exact_complex_identity']=s.factor(direct-reduced)==0
    checks['exact_no_scale_limit']=s.factor(reduced.subs({n:3,Q:0})-Y.subs(n,3)*F*Fb)==0
    checks['metric_determinant']=s.factor(metric.det()-n*DH/Y**3)==0
    # Exact multi-matter rational controls, with genuinely complex P,z,Wi.
    controls=[]
    for nm in (2,3,4):
        nn=s.Rational(29999,10000);HH=s.Rational(13,10)
        PP=s.Rational(6,5)+s.I/s.Integer(7);QQ=s.Rational(1,100)
        zz=s.Matrix([s.Rational(j+1,20)+s.I*s.Rational(2*j-1,30) for j in range(nm)])
        ff=s.Matrix([s.Rational(j+2,9)-s.I*s.Rational(j+1,11) for j in range(nm)])
        ww=s.Rational(7,3)+s.I*s.Rational(2,7)
        yy=HH-s.expand((zz.conjugate().T*zz)[0])/nn
        gg=s.zeros(nm+1)
        gg[0,0]=nn*(PP*s.conjugate(PP)/yy**2-QQ/yy)
        for i in range(nm):
            gg[0,i+1]=-PP*zz[i]/yy**2
            gg[i+1,0]=-s.conjugate(PP)*s.conjugate(zz[i])/yy**2
            for j in range(nm):
                gg[i+1,j+1]=s.KroneckerDelta(i,j)/yy+s.conjugate(zz[i])*zz[j]/(nn*yy**2)
        dd=s.Matrix([-nn*PP*ww/yy]+[ff[i]+s.conjugate(zz[i])*ww/yy for i in range(nm)])
        dv=(dd.conjugate().T*gg.inv()*dd)[0]-3*ww*s.conjugate(ww)
        ss=(zz.T*ff)[0]
        rv=yy*(ff.conjugate().T*ff)[0]+(nn-3)*ww*s.conjugate(ww)+yy*QQ*(ss-nn*ww)*s.conjugate(ss-nn*ww)/(nn*(PP*s.conjugate(PP)-HH*QQ))
        err=s.simplify(dv-rv)
        controls.append(dict(matter_count=nm,exact_difference=str(err),positive_leading_minors=all(gg[:j,:j].det()>0 for j in range(1,nm+2))))
    checks['multi_matter_exact_complex_controls']=all(c['exact_difference']=='0' for c in controls)
    checks['complex_control_metrics_positive']=all(c['positive_leading_minors'] for c in controls)
    # At small matter vev, tuned F^2=eps W^2 and stationary scalar Ward
    # identity. Canonical basis (sqrt(n) chi_tau, chi_T); M=1.
    ep=s.symbols('epsilon',positive=True)
    nn=3-ep
    # Loop stationarity supplies m_TT(raw)=eps*m32. Tree-only is off shell.
    unit=s.Matrix([[ep**2/(3*nn),ep*s.sqrt(ep)/(3*s.sqrt(nn))],
                   [ep*s.sqrt(ep)/(3*s.sqrt(nn)),ep/3]])
    gold=s.Matrix([s.sqrt(nn),-s.sqrt(ep)])
    orth=s.Matrix([s.sqrt(ep),s.sqrt(nn)])/s.sqrt(3)
    checks['stationary_unitary_goldstino_null']=all(s.simplify(v)==0 for v in unit*gold)
    checks['orthogonal_normalization']=s.simplify((orth.T*orth)[0]-1)==0
    checks['orthogonal_mass_epsilon_over_n']=s.simplify((orth.T*unit*orth)[0]-ep/nn)==0
    checks['matter_current_retained']=s.simplify(orth[1]**2-nn/3)==0
    result=dict(claim_id='PG06_EXACT_GEOMETRY',checks=checks,complex_controls=controls,
                identities={'potential':'Y^(-n) [Y F0+(n-3)|W|^2/M^2+Y QH |S-nW|^2/(n DH M^2)]',
                            'DH':'|H_tau|^2-H H_tau_taubar',
                            'orthogonal_mass_at_stationary_leading_order':'epsilon/(3-epsilon) m32',
                            'orthogonal_matter_current_amplitude':'sqrt((3-epsilon)/3)'},
                runtime_seconds=time.monotonic()-started,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                non_claims=['Goldstino matrix is a leading small-matter/M stationary Ward completion, not a finite SUGRA loop pole',
                            'No selected cosmological constant or all-field quantum stability theorem'])
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
