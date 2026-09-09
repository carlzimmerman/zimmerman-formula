"""High-precision local spatial jets of the same action, not polynomial fitting.

Binary-float action coefficients/initial fluid constants are lifted exactly to
mpmath; derived fluid energy and interface q are recomputed from their equations.
The fixed Hermite polynomial is used only in the interface's interior cell.
"""
from functools import lru_cache
import argparse
import json
import time
import mpmath as mp
import numpy as np
from scipy.optimize import root as solve_root
import ic36_second_preservation as previous
import ic37_analytic_second_jet as analytic


def polynomial(coeff,x,order=0):
    coeff=list(coeff)
    for _ in range(order):coeff=[i*coeff[i] for i in range(1,len(coeff))]
    return mp.polyval(list(reversed(coeff)),x) if coeff else mp.mpf(0)


def vector_derivative(fn,order):
    cache={}
    def value(x):
        key=(mp.mp.prec,x._mpf_)
        if key not in cache:cache[key]=fn(x)
        return cache[key]
    size=len(value(mp.mpf(0)))
    return [mp.diff(lambda x:value(x)[i],mp.mpf(0),order) for i in range(size)]


def series(fn,order):
    coefficients=None
    for n in range(order+1):
        values=vector_derivative(fn,n)
        if coefficients is None:coefficients=[[] for _ in values]
        for c,v in zip(coefficients,values):c.append(v/mp.factorial(n))
    return coefficients


def ode_series(rhs,r0,initial,order):
    coefficients=[[mp.mpf(v)] for v in initial]
    for n in range(order):
        values=vector_derivative(lambda x:rhs(r0+x,[polynomial(c,x) for c in coefficients]),n)
        for c,v in zip(coefficients,values):c.append(v/mp.factorial(n+1))
    return coefficients


@lru_cache(None)
def reference():return previous.previous.Collar(.006)


class LocalJet:
    def __init__(self,U0=0,U1=0,ref=None):
        self.ref=reference() if ref is None else ref;m=self.ref.model
        for k in ('m','wc','a02','lam','kappa','A','E'):setattr(self,k,mp.mpf(float(getattr(m,k))))
        self.S0=mp.mpf(float(self.ref.initial[0]));self.Q0=mp.mpf(float(m.Q));self.r0=mp.mpf(2)
        self.cell=int(np.searchsorted(m.table.x,float(self.S0),side='right')-1)
        self.knots=[mp.mpf(float(x)) for x in m.table.x[self.cell:self.cell+2]]
        self.jets=[[mp.mpf(float(x)) for x in row] for row in m.table.jets[self.cell:self.cell+2]]
        self.fluids=[{k:mp.mpf(float(f[k])) for k in ('w','c','j')} for f in self.ref.fluids]
        qcrit=-3*self.m*mp.mpf('.5')*mp.exp(3*self.wc)/mp.sqrt(2)
        self.initial=[self.S0,mp.mpf(0),self.Q0,mp.mpf(0),mp.mpf(0),mp.mpf(0),qcrit,mp.mpf(-100),mp.mpf(U0),mp.mpf(U1)]
        self.flowfn,self.sourcefn,self.gradfn=analytic.build()[2:]

    def D(self,S,order=0):
        if not self.knots[0]<S<self.knots[1]:raise ValueError('Local Taylor argument leaves the fixed coefficient cell')
        h=self.knots[1]-self.knots[0];x=(S-self.knots[0])/h
        a,b,c=self.jets[0];d,e,f=self.jets[1]
        R0=d-a-h*b-h*h*c/2;R1=h*(e-b)-h*h*c;R2=h*h*(f-c)
        coef=[a,h*b,h*h*c/2,10*R0-4*R1+R2/2,-15*R0+7*R1-R2,6*R0-3*R1+R2/2]
        return polynomial(coef,x,order)/h**order

    def params(self,S):
        return (self.m,self.wc,self.a02,self.lam,self.kappa,self.A,*[self.D(S,n) for n in range(4)],self.E)

    def details(self,r,y):
        S,S1,Q,Q1,sh,beta,q,q1,U,U1=y;params=self.params(S)
        D,D1,D2=(self.D(S,n) for n in range(3))
        z=2*mp.sqrt(D/(6*self.E))*mp.sinh(mp.asinh(-3*self.A*q*mp.sqrt(6*self.E/D)/(4*D))/3)
        Fz=2*D+12*self.E*z*z;t=2*mp.exp(S-2*self.wc)/self.m
        energies=[mp.exp(S)*f['c']*f['j']**(1+f['w']) for f in self.fluids]
        rho=mp.fsum(energies);pw=mp.fsum((1-3*f['w'])*h for f,h in zip(self.fluids,energies))
        pressure=mp.fsum(f['w']*h for f,h in zip(self.fluids,energies))
        ent=mp.fsum((1+f['w'])*h for f,h in zip(self.fluids,energies))
        pwent=mp.fsum((1-3*f['w'])*(1+f['w'])*h for f,h in zip(self.fluids,energies))
        def gradient(S2,Q2):
            values=self.gradfn(r,S,S1,S2,Q,Q1,Q2,q,z,sh,*params)
            names=('value','S','S1','S2','Q','Q1','Q2','q','z','sh')
            return [dict(zip(names,values[i:i+10])) for i in (0,10)]
        C,W=gradient(0,0);M=mp.matrix([[C['S2'],C['Q2']],[W['S2'],W['Q2']]])
        S2,Q2=mp.lu_solve(M,mp.matrix([-C['value']-rho,-W['value']+pw]))
        C,W=gradient(S2,Q2);sh1=-q1/2-3*(Q1+1/r)*sh;bp=beta/r-t*sh
        X=[S,S1,S2,Q,Q1,Q2,q,z,sh];extras=[q1,sh1,beta,bp]
        vals=self.flowfn(r,*X,*extras,*([mp.mpf(0)]*13),*params)
        Qd,qd,sd=vals[:3];qd+=3*pressure/2;HQ=-t*q/6-self.A*z/2
        z1=-(self.A*q1+2*D1*S1*z)/Fz
        spatial=dict(S=S1,S1=S2,Q=Q1,Q1=Q2,q=q1,z=z1,sh=sh1)
        c3=mp.fsum(C[k]*v for k,v in spatial.items())+rho*S1-2*(C['S2']*S1+C['Q2']*Q1)/r**2
        w3=mp.fsum(W[k]*v for k,v in spatial.items())-pw*S1-2*(W['S2']*S1+W['Q2']*Q1)/r**2
        S3,Q3=mp.lu_solve(M,mp.matrix([-c3,-w3]))
        # q2=0 source; the independently derived coefficient gamma is applied below.
        z2=-(2*(D2*S1*S1+D1*S2)*z+4*D1*S1*z1+24*self.E*z*z1*z1)/Fz
        sh2=-3*(Q2-1/r**2)*sh-3*(Q1+1/r)*sh1
        bp2=bp/r-beta/r**2-t*(S1*sh+sh1)
        bp3=bp2/r-2*bp/r**2+2*beta/r**3-t*((S2+S1*S1)*sh+2*S1*sh1+sh2)
        HQ1=-t*(S1*q+q1)/6-self.A*z1/2
        HQ2=-t*((S2+S1*S1)*q+2*S1*q1)/6-self.A*z2/2
        Qd1=HQ1+bp*Q1+beta*Q2+(bp2+2*bp/r-2*beta/r**2)/3
        Qd2=HQ2+bp2*Q1+2*bp*Q2+beta*Q3+(bp3+2*bp2/r-4*bp/r**2+4*beta/r**3)/3
        rates=dict(Q=Qd,Q1=Qd1,Q2=Qd2,q=qd,z=-self.A*qd/Fz,sh=sd)
        Cf=mp.fsum(C[k]*v for k,v in rates.items())-3*HQ*ent
        Wf=mp.fsum(W[k]*v for k,v in rates.items())+3*HQ*pwent
        C0=C['S']-C['z']*2*D1*z/Fz+rho;W0=W['S']-W['z']*2*D1*z/Fz-pw
        gamma=self.A*self.A/(2*Fz)
        K=mp.matrix([[C['S2'],C['Q2']*gamma],[W['S2'],W['Q2']*gamma]])
        U2,q2=mp.lu_solve(K,mp.matrix([-C0*U-C['S1']*U1-Cf,-W0*U-W['S1']*U1-Wf]))
        dy=[S1,S2,Q1,Q2,sh1,bp,q1,q2,U1,U2]
        return dict(dy=dy,X=X,extras=extras,z=z,Fz=Fz,HQ=HQ,t=t,energies=energies,
            flow=[Qd,qd,sd],Qd1=Qd1,Qd2=Qd2+gamma*q2,
            C=[C0,C['S1'],C['S2']],W=[W0,W['S1'],W['S2']],
            constraint=[C['value']+rho,W['value']-pw],params=params)

    def rhs(self,r,y):return self.details(r,y)['dy']


def rhs_audit():
    first=previous.FirstJet()
    with mp.workdps(60):
        local=LocalJet(ref=first.c);out=local.details(local.r0,local.initial)
        y=np.array([float(x) for x in local.initial]);other=first.rhs(2.,y)
        error=np.max(abs(np.array([float(x) for x in out['dy']])-other)/np.maximum(1,abs(other)))
        return dict(max_relative_rhs_error=float(error),max_initial_constraint=float(max(abs(x) for x in out['constraint'])),
                    coefficient_cell=local.cell,full_theory='OPEN')


def boundary_from_coefficients(C,W,FC,FW,order):
    families=[]
    for initial,inhomogeneous in (([0,0],True),([1,0],False),([0,1],False)):
        def rhs(x,y):
            return [y[1],-(polynomial(C[0],x)*y[0]+polynomial(C[1],x)*y[1]
                     +(polynomial(FC,x) if inhomogeneous else 0))/polynomial(C[2],x)]
        A=ode_series(rhs,mp.mpf(0),initial,order+2)[0]
        residual=[]
        for n in range(order+1):
            value=mp.fsum(W[0][i]*A[n-i]+W[1][i]*(n-i+1)*A[n-i+1]
                         +W[2][i]*(n-i+2)*(n-i+1)*A[n-i+2] for i in range(n+1))
            residual.append(value+(FW[n] if inhomogeneous else 0))
        families.append(residual)
    matrix=mp.matrix([[families[1][n],families[2][n]] for n in (0,1)])
    constants=mp.lu_solve(matrix,mp.matrix([-families[0][n] for n in (0,1)]))
    edges=[mp.factorial(n)*(families[0][n]+constants[0]*families[1][n]+constants[1]*families[2][n]) for n in range(order+1)]
    normalized=matrix.copy()
    for j in range(2):
        norm=mp.sqrt(mp.fsum(matrix[i,j]**2 for i in range(2)))
        for i in range(2):normalized[i,j]/=norm
    sv=mp.svd(normalized,compute_uv=False)
    rank=sum(v>64*mp.eps*sv[0] for v in sv)
    return dict(edge_jets=edges,constants=list(constants),matrix=matrix,determinant=mp.det(matrix),
                normalized_singular_values=list(sv),rank=rank)


def local_result(U0=0,U1=0,dps=60,order=3,with_coefficients=False):
    with mp.workdps(dps):
        local=LocalJet(U0,U1);spatial_order=order+4
        Y=ode_series(local.rhs,local.r0,local.initial,spatial_order)
        point_cache={}
        def point(x):
            key=(mp.mp.prec,x._mpf_)
            if key not in point_cache:
                y=[polynomial(c,x) for c in Y];point_cache[key]=(y,local.details(local.r0+x,y))
            return point_cache[key]
        nf=len(local.fluids)
        def first_time(x):
            y,d=point(x);S,S1=y[:2]
            jd=[-3*d['HQ']*f['j'] for f in local.fluids]
            gd=[mp.exp(S)*(1+f['w'])*f['c']*f['j']**f['w']*S1 for f in local.fluids]
            return [*d['flow'],*jd,*gd]
        V=series(first_time,spatial_order)
        def shift_source(x):
            y,d=point(x);return [-d['t']*(polynomial(V[2],x)+y[4]*y[8])/(local.r0+x)]
        G=series(shift_source,spatial_order)[0]
        BV=[mp.mpf(0)]*(len(G)+2)
        for n,g in enumerate(G):BV[n+1]+=local.r0*g/(n+1);BV[n+2]+=g/(n+1)
        def timejets(x):
            y,d=point(x);U=y[8];qd=polynomial(V[1],x)
            zd=-(local.A*qd+2*local.D(y[0],1)*d['z']*U)/d['Fz']
            rates=[U,y[9],d['dy'][9],polynomial(V[0],x),polynomial(V[0],x,1),
                   polynomial(V[0],x,2),qd,zd,polynomial(V[2],x)]
            erates=[polynomial(V[1],x,1),polynomial(V[2],x,1),polynomial(BV,x),polynomial(BV,x,1)]
            return rates,erates
        def second_time(x):
            y,d=point(x);rates,erates=timejets(x)
            out=list(local.flowfn(local.r0+x,*d['X'],*d['extras'],*rates,*erates,*d['params'])[3:])
            out[1]+=mp.fsum(3*f['w']*h*(y[8]+(1+f['w'])*polynomial(V[3+i],x)/f['j'])/2
                           for i,(f,h) in enumerate(zip(local.fluids,d['energies'])))
            return out
        acceleration=series(second_time,order+2)
        def forcing(x):
            y,d=point(x);rates,_=timejets(x);S,S1,Q,Q1,sh,beta=y[:6];U=y[8];r=local.r0+x
            Qa,qa,sha=(polynomial(c,x) for c in acceleration);zd=rates[7]
            za=-(local.A*qa+2*local.D(S,2)*d['z']*U*U+4*local.D(S,1)*U*zd+24*local.E*d['z']*zd*zd)/d['Fz']
            avec=[Qa,polynomial(acceleration[0],x,1),polynomial(acceleration[0],x,2),qa,za,sha]
            vals=local.sourcefn(r,*d['X'],*rates,*avec,*d['params']);FC,FW=vals[2:]
            HQd=-d['t']*(U*y[6]+rates[6])/6-local.A*zd/2
            for i,(f,h) in enumerate(zip(local.fluids,d['energies'])):
                j,w=f['j'],f['w'];vf=(1+w)*f['c']*j**w
                jd=polynomial(V[3+i],x);jdp=polynomial(V[3+i],x,1)
                gd=polynomial(V[3+nf+i],x);gdp=polynomial(V[3+nf+i],x,1)
                jdd=beta*jdp-3*HQd*j-3*d['HQ']*jd+j*mp.exp(S-2*Q)/vf*(gdp+(2/r+Q1+S1)*gd)
                zero=h*(U*U+2*(1+w)*U*jd/j+(1+w)*w*(jd/j)**2+(1+w)*jdd/j)
                grad=mp.exp(S-2*Q)*j*gd*gd/vf
                FC+=zero+grad;FW-=(1-3*w)*(zero-grad)
            return [*d['C'],*d['W'],FC,FW]
        source_coefficients=series(forcing,order)
        out=boundary_from_coefficients(source_coefficients[:3],source_coefficients[3:6],
                                       source_coefficients[6],source_coefficients[7],order)
        d0=point(mp.mpf(0))[1]
        qjet_error=max(abs(polynomial(V[0],mp.mpf(0),n)-d0['Qd'+str(n)]) for n in (1,2))
        spatial_error=max(abs((n+1)*Y[0][n+1]-Y[1][n]) for n in range(spatial_order))
        digits=dps-10;fmt=lambda v:mp.nstr(v,digits)
        result=dict(U0=str(U0),U1=str(U1),dps=dps,order=order,spatial_order=spatial_order,
            edge_jets=[fmt(x) for x in out['edge_jets']],constants=[fmt(x) for x in out['constants']],
            matrix=[[fmt(out['matrix'][i,j]) for j in range(2)] for i in range(2)],
            determinant=fmt(out['determinant']),rank=out['rank'],
            normalized_singular_values=[fmt(x) for x in out['normalized_singular_values']],
            independent_Qdot_spatial_jet_error=fmt(qjet_error),kinematic_series_error=fmt(spatial_error),
            initial_constraint_error=fmt(max(abs(x) for x in d0['constraint'])),
            activation_square=fmt((mp.exp(-3*local.wc)*local.initial[6]/(3*local.m*mp.mpf('.5')))**2),
            activation_radial_derivative=fmt(2*(mp.exp(-3*local.wc)/(3*local.m*mp.mpf('.5')))**2*local.initial[6]*local.initial[7]),
            auxiliary_convexity=fmt(d0['Fz']),lapse_second_coefficient=fmt(d0['C'][2]),
            coefficient_cell=local.cell,coefficient_margin=fmt(min(local.S0-local.knots[0],local.knots[1]-local.S0)),
            full_theory='OPEN')
        if with_coefficients:
            result['source_coefficients']=[[fmt(v) for v in row] for row in source_coefficients]
        return result


def newton_refine(fn,initial,maxsteps=6):
    x=mp.matrix(initial);history=[];h=mp.mpf('1e-12')
    for _ in range(maxsteps):
        f=mp.matrix(fn(x));history.append([mp.nstr(v,40) for v in f])
        if max(abs(v) for v in f)<mp.mpf('1e-32'):break
        columns=[]
        for j in range(len(x)):
            xp=x.copy();xm=x.copy();xp[j]+=h;xm[j]-=h
            columns.append((mp.matrix(fn(xp))-mp.matrix(fn(xm)))/(2*h))
        J=mp.matrix([[col[i] for col in columns] for i in range(len(x))])
        x-=mp.lu_solve(J,f)
    return list(x),history


def joint_search(start,scales):
    history=[]
    def target(x):
        out=local_result(U0=str(float(x[0])),U1=str(float(x[1])),dps=35,order=3)
        values=np.array([float(v) for v in out['edge_jets'][2:4]])/scales
        history.append(dict(U0=float(x[0]),U1=float(x[1]),scaled_residual=values.tolist()))
        return values
    solution=solve_root(target,np.array([0.,float(start)]),method='hybr',options={'xtol':1e-9,'maxfev':45})
    out=dict(search_success=bool(solution.success),message=str(solution.message),evaluations=history)
    if not solution.success or np.max(abs(solution.fun))>1e-7:return out
    with mp.workdps(60):
        def precise(x):
            result=local_result(U0=x[0],U1=x[1],dps=50,order=3)
            return [mp.mpf(v)/mp.mpf(float(scale)) for v,scale in zip(result['edge_jets'][2:4],scales)]
        initial=[mp.mpf(str(float(v))) for v in solution.x]
        refined,steps=newton_refine(precise,initial)
        u0,u1=(mp.nstr(v,50) for v in refined)
    out.update(U0=u0,U1=u1,refinement_residuals=steps,
               audits=[local_result(U0=u0,U1=u1,dps=d,order=4) for d in (50,80)])
    return out


def study():
    started=time.perf_counter()
    rows=[local_result(dps=d,order=4) for d in (50,80)]
    rows.append(local_result(U1='-2.6400382455715268',dps=60,order=4))
    roots=[]
    for guesses in (('-2.7','-2.6'),('6.5','6.7')):
        history=[]
        with mp.workdps(50):
            def target(u):
                out=local_result(U1=u,dps=45,order=2);value=mp.mpf(out['edge_jets'][2])
                history.append(dict(U1=mp.nstr(u,40),curvature=str(value)))
                return value
            root=mp.findroot(target,tuple(mp.mpf(x) for x in guesses),solver='secant',tol=mp.mpf('1e-40'),maxsteps=12)
            root_text=mp.nstr(root,40)
        audits=[local_result(U1=root_text,dps=d,order=4) for d in (50,80)]
        roots.append(dict(guesses=guesses,U1=root_text,evaluations=history,audits=audits))
    scales=np.maximum(1.,abs(np.array([float(x) for x in rows[0]['edge_jets'][2:4]])))
    joint=[joint_search(r['U1'],scales) for r in roots]
    return dict(rows=rows,roots=roots,joint=joint,runtime_seconds=time.perf_counter()-started,full_theory='OPEN')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--dps',type=int,default=50)
    parser.add_argument('--order',type=int,default=3);parser.add_argument('--U1',default='0')
    parser.add_argument('--study',action='store_true');parser.add_argument('--strict',action='store_true')
    args=parser.parse_args()
    print(json.dumps(study() if args.study else local_result(U1=args.U1,dps=args.dps,order=args.order),indent=2))
    raise SystemExit(2 if args.strict else 0)
