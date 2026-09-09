"""All six compact conserved stress polarizations, high-acceleration principal limit.

V3 scales both tensor kinetic and gradient terms by C/2 using York-TT
operators. The calculation derives the entire electric Riemann response
for T00=partial_i partial_j Aij, T0i=-partial_t partial_j Aij,
Tij=partial_t^2 Aij. It does not certify nonlinear/galactic causal health.
"""
import json
import sympy as s


def response_matrix(tensor_norm, C=s.Rational(5,3), ell=s.Rational(1,100)):
    x,z,r=s.symbols('kx kz rate',real=True)
    K=x*x+z*z
    kv=s.Matrix([x,0,z])
    I=s.eye(3)
    P=I-kv*kv.T/K
    psi,n,B,v=s.symbols('psi n B v')
    src,Tr=s.symbols('src Tr')
    alpha=2-C
    L=(-3*C*v*v+2*C*K*v*B-ell*(3*v-K*B)**2
       +K*(2*psi*psi-4*n*psi+alpha*n*n))
    Lm=-src*n+r*src*B-r*r*Tr*psi
    sol=s.solve([s.diff(L+Lm,n).subs(v,r*psi),
                 s.diff(L+Lm,B).subs(v,r*psi),
                 r*s.diff(L,v).subs(v,r*psi)-s.diff(L+Lm,psi)], [psi,n,B])
    # Scalar, vector and tensor equations are independently varied.
    S,j=s.symbols('S j')
    vector_L=C*K*S*S/4+j*S
    Ssolution=s.solve(s.diff(vector_L,S),S)[0]
    ht,hdot,stress=s.symbols('ht hdot stress')
    tensor_L=tensor_norm*(hdot*hdot-K*ht*ht)/2+stress*ht
    ht_solution=s.solve(r*s.diff(tensor_L,hdot).subs(hdot,r*ht)
                        -s.diff(tensor_L,ht),ht)[0]
    assert s.simplify(Ssolution+2*j/(C*K))==0
    assert s.simplify(ht_solution-stress/(tensor_norm*(r*r+K)))==0
    modes=[(0,0),(0,1),(0,2),(1,1),(1,2),(2,2)]
    rows=[]
    spatial_poles=[]
    denominators=set()
    for i,jj in modes:
        A=s.zeros(3)
        A[i,jj]=1;A[jj,i]=1
        # 16pi Gb is absorbed into A, consistently for every sector.
        substitutions={src:-(kv.T*A*kv)[0],Tr:s.trace(A)}
        ps,nn,bb=[s.cancel(sol[q].subs(substitutions)) for q in [psi,n,B]]
        ATT=P*A*P-P*s.trace(P*A)/2
        jT=P*A*kv
        E=(-kv*kv.T*(nn+r*bb)+r*r*ps*I
           -r*r/(C*K)*(kv*jT.T+jT*kv.T)
           -r**4*ATT/(2*tensor_norm*(r*r+K)))
        for h,m in modes:
            entry=s.cancel(E[h,m])
            denominator=s.denom(entry)
            if s.rem(denominator,K,x)==0:
                spatial_poles.append([i,jj,h,m])
            denominators.add(str(s.factor(denominator)))
            rows.append(dict(source=[i,jj],curvature=[h,m],
                             numerator=str(s.factor(s.numer(entry))),
                             denominator=str(s.factor(denominator))))
    return dict(rows=rows,spatial_poles=spatial_poles,
                denominators=sorted(denominators),
                coordinates=[x,z,r],source_count=len(modes),entry_count=len(rows))


def audit():
    C=s.Rational(5,3);ell=s.Rational(1,100)
    v2=response_matrix(s.Integer(1))
    v3=response_matrix(C/2)
    assert v2['spatial_poles']  # negative control: scalar repair is insufficient
    assert not v3['spatial_poles']
    x,z,r=v3.pop('coordinates')
    v2.pop('coordinates')
    # Check the FULL denominator factors; absence of k² alone would not
    # establish hyperbolicity or exclude another noncausal pole.
    light=r*r+x*x+z*z
    clock=(2-C)*(C+3*ell)*r*r+2*ell*(x*x+z*z)
    for row in v3['rows']:
        den=s.sympify(row['denominator'],locals={'kx':x,'kz':z,'rate':r})
        residual=s.cancel(den/(light*clock))
        # Every denominator divides a product of the two local wave symbols.
        assert not s.denom(s.cancel(light*clock/den)).free_symbols
    cs2=s.factor(2*ell/((2-C)*(C+3*ell)))
    assert 0<float(cs2)<1
    return dict(status='V3_LINEAR_CONSERVED_RESPONSE_CONSTRUCTED; FULL_THEORY_OPEN',
                C=str(C),ell=str(ell),etaV=str(C-2),etaU=str((2-C)/4),
                etaX=str(2-C),etaTT=str(C/2-1),
                v2_uncancelled_spatial_poles=len(v2['spatial_poles']),
                v3_uncancelled_spatial_poles=len(v3['spatial_poles']),
                v3_entry_count=v3['entry_count'],tensor_speed_squared='1',
                tensor_kinetic_normalization=str(C/2),
                clock_speed_squared=str(cs2),
                characteristic_factors=[str(light),str(clock)],
                v3_response=v3['rows'],
                scope=['fixed rational witness, constant high-acceleration coefficients',
                       'all six symmetric compact-source seed polarizations',
                       'rotational invariance permits k=(kx,0,kz); source basis remains full',
                       'retarded zero-past solutions; no freely added instantaneous homogeneous modes',
                       'curved and nonlinear York-TT variations remain uncomputed'])


if __name__=='__main__':
    print(json.dumps(audit(),indent=2))
