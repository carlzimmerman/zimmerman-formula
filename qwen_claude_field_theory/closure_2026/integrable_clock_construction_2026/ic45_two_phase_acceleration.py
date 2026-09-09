"""Second time tangent with an independently responding inactive clock.

The zero-boundary choice is a negative control: bulk constraint preservation
does not suffice for moving-interface compatibility. No evolution/existence
certificate is asserted. IC39 action coefficients and IC41 initial data stay
fixed; only the inactive w_tt response is newly allowed.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import mpmath as mp
import sympy as s
import ic30_radial_bridge as radial
import ic37_local_taylor as local
import ic41_free_initial_gradients as initial


@lru_cache(None)
def matter_identities():
    S,w,wc,Q,wf=s.symbols('S w wc Q wf',real=True)
    c,j,g=s.symbols('c j g',positive=True)
    # c is the barred-frame coefficient at wc, not a variable fundamental
    # coupling. Express the physical current and spatial gradient first.
    cp=c*s.exp(-(1-3*wf)*wc);jp=s.exp(-3*w)*j;kp=s.exp(-2*Q-2*w)*g*g
    vp=(1+wf)*cp*jp**wf
    physical=s.exp(S+4*w)*(cp*jp**(1+wf)+jp*kp/(2*vp))
    vf=(1+wf)*c*j**wf;dw=w-wc
    h0=s.exp(S+(1-3*wf)*dw)*c*j**(1+wf)
    hg=s.exp(S-2*Q-(1-3*wf)*dw)*j*g*g/(2*vf)
    return dict(frame_density=s.simplify(s.powdenest(physical,force=True)-h0-hg),
        lapse_variation=s.simplify(s.diff(h0+hg,S)-h0-hg),
        clock_variation=s.simplify(-s.diff(h0+hg,w)+(1-3*wf)*(h0-hg)),
        clock_linear_coefficient=s.simplify(-s.diff(h0+hg,w,2).subs({w:wc,g:0})
                                        +(1-3*wf)**2*h0.subs(w,wc)))


@lru_cache(None)
def operator():
    d=radial.radial_action();r=d['r'];S,w,Q,q,z,sh,beta,ell=d['fields']
    L=d['L'].subs(ell,0)
    C=-radial.euler(L,S,r)/d['J'];W=radial.euler(L,w,r)/d['J']
    variables=(S,s.diff(S,r),s.diff(S,r,2),w,s.diff(w,r),s.diff(w,r,2),
               Q,s.diff(Q,r),s.diff(Q,r,2),q,z,sh)
    symbols=s.symbols('S S1 S2 w w1 w2 Q Q1 Q2 q z shear',real=True)
    A,D,D1,E=s.symbols('A D D1 E',real=True)
    coefficients={d['A']:A,s.diff(d['A'],S):0,d['D']:D,s.diff(d['D'],S):D1,
                  d['E4']:E,s.diff(d['E4'],S):0}
    values=[C,W,*[s.diff(C,v) for v in variables[3:6]],*[s.diff(W,v) for v in variables[3:6]]]
    expressions=[s.simplify(v.subs(coefficients,simultaneous=True).subs(dict(zip(variables,symbols)),simultaneous=True)) for v in values]
    args=(r,*symbols,d['m'],d['a02'],d['lam'],d['kappa'],A,D,D1,E)
    return s.lambdify(args,expressions,'mpmath',cse=True)


@lru_cache(None)
def experiment(dps=40,degree=6,boundary='zero'):
    if degree<6:raise ValueError('Need degree >=6 for the independent inactive response')
    if boundary not in ('zero','compatible'):raise ValueError('Unknown boundary experiment')
    record=json.loads((Path(__file__).parent/'ic41_run_001/response80/stdout.txt').read_text())
    with mp.workdps(dps):
        p=record['input_parameters']
        engine=initial.FreeTimeJet(p['U0'],p['U1'],degree-4,qprime=p['qprime'],Sprime=p['Sprime'])
        m=engine.model;engine.step(0);engine.shift(1);engine.step(1)
        n=degree-2;fn=operator()
        def at(x):
            y=[local.polynomial(row,x) for row in engine.Y]
            point=m.details(m.r0+x,y);S,S1,Q,Q1,sh,beta,q,q1,U,U1=y
            S2,Q2=point['X'][2],point['X'][5]
            args=(m.r0+x,S,S1,S2,m.wc,0,0,Q,Q1,Q2,q,point['z'],sh,
                  m.m,m.a02,m.lam,m.kappa,m.A,m.D(S),m.D(S,1),m.E)
            out=fn(*args);cw=list(out[2:5]);ww=list(out[5:8])
            for f,h in zip(m.fluids,point['energies']):
                cw[0]+=(1-3*f['w'])*h;ww[0]-=(1-3*f['w'])**2*h
            return point,out,[*point['C'],*point['W'],*cw,*ww]
        coeff=local.series(lambda x:at(x)[2],n)
        C,W,Cw,Ww=coeff[:3],coeff[3:6],coeff[6:9],coeff[9:12]
        sources=local.series(lambda x:local.vector_derivative(lambda t:engine.constraints(x,t),2),n)
        FC,FW=sources[:2]
        if boundary=='compatible':
            bdata=local.boundary_from_coefficients(C,W,FC,FW,n)
            A0,A1=bdata['constants']
        else:A0=A1=mp.mpf(0)
        poly=local.polynomial
        def active_rhs(x,y):
            return [y[1],-(poly(C[0],x)*y[0]+poly(C[1],x)*y[1]+poly(FC,x))/poly(C[2],x)]
        active=local.ode_series(active_rhs,mp.mpf(0),[A0,A1],degree)[0]
        def inactive_rhs(x,y):
            A,A1,B,B1=y
            matrix=mp.matrix([[poly(C[2],x),poly(Cw[2],x)],
                              [poly(W[2],x),poly(Ww[2],x)]])
            rhs=mp.matrix([-poly(FC,x)-poly(C[0],x)*A-poly(C[1],x)*A1-poly(Cw[0],x)*B-poly(Cw[1],x)*B1,
                           -poly(FW,x)-poly(W[0],x)*A-poly(W[1],x)*A1-poly(Ww[0],x)*B-poly(Ww[1],x)*B1])
            A2,B2=mp.lu_solve(matrix,rhs)
            return [A1,A2,B1,B2]
        inactive=local.ode_series(inactive_rhs,mp.mpf(0),[A0,A1,0,0],degree)
        A,B=inactive[0],inactive[2]
        def apply(op,field,k):
            return mp.fsum(op[j][i]*field[k-i+j]*mp.factorial(k-i+j)/mp.factorial(k-i)
                           for j in range(3) for i in range(k+1))
        errors=[];off_values=[];active_W=[]
        for k in range(n+1):
            cc=apply(C,A,k)+apply(Cw,B,k)+FC[k]
            ww=apply(W,A,k)+apply(Ww,B,k)+FW[k]
            scale=max(1,abs(FC[k]),abs(FW[k]),abs(apply(C,A,k)),abs(apply(W,A,k)))
            errors.extend([abs(cc)/scale,abs(ww)/scale]);off_values.append([cc,ww])
            active_W.append(apply(W,active,k)+FW[k])
        point,out,_=at(mp.mpf(0))
        old=m.gradfn(m.r0,*point['X'],*m.params(m.initial[0]))
        reference_error=max(abs(out[0]-old[0]),abs(out[1]-old[10]))
        V=-engine.T[1][2][0]/m.initial[7]+m.initial[5]
        reaction_tt=-active_W[0]
        # q_tt is identical on the two initial sides because w_t=0 and S_t
        # and all first-time canonical fields coincide. The time^2 term in
        # [q_r]=-lambda/(2V) therefore requires lambda_tt=0 at this datum.
        boundary_residual=abs(reaction_tt/(2*V))
        fmt=lambda x:mp.nstr(x,dps-8)
        return dict(dps=dps,degree=degree,source_degree=engine.degree,boundary=boundary,
            boundary_constants=[fmt(A0),fmt(A1)],
            max_second_constraint_residual=fmt(max(errors)),residual_normalization='per-coefficient relative to source and lapse terms, floor 1',
            operator_reference_error=fmt(reference_error),active_reaction_tt=fmt(reaction_tt),
            necessary_second_interface_residual=fmt(boundary_residual),
            inactive_wtt_second_spatial_derivative=fmt(2*B[2]),
            inactive_wtt_sixth_spatial_derivative=fmt(mp.factorial(6)*B[6]),
            active_S_tt_coefficients=[fmt(v) for v in active],
            inactive_S_tt_coefficients=[fmt(v) for v in A],inactive_w_tt_coefficients=[fmt(v) for v in B],
            inactive_constraint_coefficients=[[fmt(v) for v in row] for row in off_values],
            active_W_tt_coefficients=[fmt(v) for v in active_W],
            relative_interface_speed=fmt(V),full_theory='OPEN',
            scope='Second time tangent only; compatible boundary cancels two edge jets, not global boundary preservation')


if __name__=='__main__':
    from ic43_weighted_multiplier import serial
    p=argparse.ArgumentParser();p.add_argument('--dps',type=int,default=40);p.add_argument('--degree',type=int,default=6)
    p.add_argument('--boundary',choices=['zero','compatible'],default='zero');p.add_argument('--strict',action='store_true');args=p.parse_args()
    print(json.dumps(serial(dict(matter=matter_identities(),result=experiment(args.dps,args.degree,args.boundary))),indent=2))
    raise SystemExit(2 if args.strict else 0)
