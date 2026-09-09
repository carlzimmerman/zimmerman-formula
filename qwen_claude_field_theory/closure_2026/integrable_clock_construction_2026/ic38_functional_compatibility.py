"""Exact operator elimination; numerical field jets are not existence proofs."""
import sympy as s
import mpmath as mp
import argparse
import json
import ic37_local_taylor as local


def reduce_exact(x,C,W,f,g):
    c0,c1,c2=map(s.sympify,C);w0,w1,w2=map(s.sympify,W)
    f,g=map(s.sympify,(f,g))
    if c2==0:raise ValueError('The lapse operator must have a nonzero leading coefficient')
    p,q,h=c0/c2,c1/c2,f/c2
    b0,b1,bF=w0-w2*p,w1-w2*q,g-w2*h
    d0=s.diff(b0,x)-b1*p;d1=b0+s.diff(b1,x)-b1*q;dF=s.diff(bF,x)-b1*h
    M=s.Matrix([[b0,b1],[d0,d1]]);det=s.factor(M.det())
    out=dict(matrix=M,determinant=det)
    if det==0:return dict(out,status='singular_reduction')
    A=s.simplify((b1*dF-d1*bF)/det);V=s.simplify((d0*bF-b0*dF)/det)
    return dict(out,status='regular_where_determinant_nonzero',A=A,V=V,
                R1=s.simplify(s.diff(A,x)-V),R2=s.simplify(s.diff(V,x)+p*A+q*V+h))


def identities():
    x=s.Symbol('x',real=True)
    p,q,h,b0,b1,bF,A,V=[s.Function(k)(x) for k in ('p','q','h','b0','b1','bF','A','V')]
    d0=s.diff(b0,x)-b1*p;d1=b0+s.diff(b1,x)-b1*q;dF=s.diff(bF,x)-b1*h
    row=b0*A+b1*V+bF;drow=d0*A+d1*V+dF
    syzygy=s.diff(row,x)-drow-b0*(s.diff(A,x)-V)-b1*(s.diff(V,x)+p*A+q*V+h)
    B0,B1,D0,D1,BF,DF=s.symbols('B0 B1 D0 D1 BF DF')
    det=s.det(s.Matrix([[B0,B1],[D0,D1]]))
    ah=(B1*DF-D1*BF)/det;vh=(D0*BF-B0*DF)/det
    return dict(differentiated_row_identity=s.simplify(syzygy),
                algebraic_first_row=s.factor(B0*ah+B1*vh+BF),
                algebraic_second_row=s.factor(D0*ah+D1*vh+DF))


def reduce_series(C,W,f,g,order):
    if min(map(len,(*C,*W,f,g)))<order+3:
        raise ValueError('Need source coefficients through residual order plus two')
    C,W=[[list(map(mp.mpf,row)) for row in group] for group in (C,W)]
    f,g=list(map(mp.mpf,f)),list(map(mp.mpf,g))
    def candidate(x):
        c0,c1,c2=(local.polynomial(row,x) for row in C)
        if not c2:raise ValueError('Zero leading lapse coefficient')
        cp0,cp1,cp2=(local.polynomial(row,x,1) for row in C)
        w0,w1,w2=(local.polynomial(row,x) for row in W)
        wp0,wp1,wp2=(local.polynomial(row,x,1) for row in W)
        fv,gv=local.polynomial(f,x),local.polynomial(g,x)
        fp,gp=local.polynomial(f,x,1),local.polynomial(g,x,1)
        p,q,h=c0/c2,c1/c2,fv/c2
        pp,qp,hp=(cp0-p*cp2)/c2,(cp1-q*cp2)/c2,(fp-h*cp2)/c2
        b0,b1,bF=w0-w2*p,w1-w2*q,gv-w2*h
        d0=wp0-wp2*p-w2*pp-b1*p
        d1=b0+wp1-wp2*q-w2*qp-b1*q
        dF=gp-wp2*h-w2*hp-b1*h
        M=mp.matrix([[b0,b1],[d0,d1]]);det=mp.det(M)
        if not det:raise ValueError('Singular operator reduction, undecided')
        a,v=mp.lu_solve(M,mp.matrix([-bF,-dF]))
        return a,v,p,q,h,det,b0,b1,M
    def residual(x):
        a,v,p,q,h,*_=candidate(x)
        return [mp.diff(lambda t:candidate(t)[0],x)-v,
                mp.diff(lambda t:candidate(t)[1],x)+p*a+q*v+h]
    coefficients=local.series(residual,order)
    a,v,p,q,h,det,b0,b1,M=candidate(mp.mpf(0))
    return dict(A=a,V=v,determinant=det,matrix=M,b0=b0,b1=b1,
                R1_jets=[mp.factorial(n)*v for n,v in enumerate(coefficients[0])],
                R2_jets=[mp.factorial(n)*v for n,v in enumerate(coefficients[1])])


def field_result(U0='0',U1='0',dps=50):
    source=local.local_result(U0=U0,U1=U1,dps=dps,order=4,with_coefficients=True)
    with mp.workdps(dps):
        data=source.pop('source_coefficients')
        out=reduce_series(data[:3],data[3:6],data[6],data[7],2)
        fmt=lambda v:mp.nstr(v,dps-15)
        result={k:fmt(out[k]) for k in ('A','V','determinant','b0','b1')}
        result.update({k:[fmt(v) for v in out[k]] for k in ('R1_jets','R2_jets')})
        result['matrix']=[[fmt(out['matrix'][i,j]) for j in range(2)] for i in range(2)]
        result['boundary_A_agreement']=fmt(abs(out['A']-mp.mpf(source['constants'][0])))
        result['boundary_V_agreement']=fmt(abs(out['V']-mp.mpf(source['constants'][1])))
        return dict(source=source,operator=result,full_theory='OPEN')


def study():
    search=local.study()
    choices=[dict(label='baseline',U0='0',U1='0')]
    choices.extend(dict(label='joint_'+str(i),U0=row['U0'],U1=row['U1'])
                   for i,row in enumerate(search['joint']) if 'U0' in row)
    return dict(identities={k:str(v) for k,v in identities().items()},
                selection=search['joint'],
                rows=[dict(label=row['label'],audits=[field_result(row['U0'],row['U1'],d) for d in (50,80)])
                      for row in choices],full_theory='OPEN')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--study',action='store_true')
    parser.add_argument('--strict',action='store_true');args=parser.parse_args()
    report=study() if args.study else dict(identities={k:str(v) for k,v in identities().items()},field=field_result())
    print(json.dumps(report,indent=2))
    raise SystemExit(2 if args.strict else 0)
