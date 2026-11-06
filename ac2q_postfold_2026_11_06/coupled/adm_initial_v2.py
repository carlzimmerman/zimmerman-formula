"""PF06a exact ADM identities and constraint-satisfying periodic initial data."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import sympy as S


def algebra():
    N,V3,M2,Kx,Ky,w,lx,bx,wx=S.symbols('N V3 M2 Kx Ky w lambda_x beta_x w_x',positive=True)
    lt,bt,pl,pb=S.symbols('lambda_t beta_t p_lambda p_beta',real=True)
    kinetic=M2*N*V3*(-2*((lt-w*lx-wx)/N)*((bt-w*bx)/N)-((bt-w*bx)/N)**2)
    pl0=S.diff(kinetic,lt);pb0=S.diff(kinetic,bt)
    rates=S.solve([S.Eq(pl,pl0),S.Eq(pb,pb0)],(lt,bt))
    ham=S.simplify((pl*lt+pb*bt-kinetic).subs(rates))
    checks={'Legendre_GR':S.simplify(ham-N*(pl**2-2*pl*pb)/(4*M2*V3)-w*(pl*lx+pb*bx)-wx*pl)==0,
       'beta_rate':S.simplify(rates[bt]-(-N*pl/(2*M2*V3)+w*bx))==0}
    D,X,g,W,V,s=S.symbols('D X gamma W V s',real=True)
    F=-D+X-V-W-g*D**2/2-2*g*D*X
    lapse_source=S.simplify(F-2*X*S.diff(F,X))
    checks['lapse_constraint_source']=S.simplify(lapse_source-(-D-X-V-W-g*D**2/2+2*g*D*X))==0
    checks['direct_lapse_derivative']=S.simplify(S.diff(N*F.subs(X,s*s/(2*N*N)),N)-lapse_source.subs(X,s*s/(2*N*N)))==0
    # Initial homogeneous p_lambda=-2M2H, p_beta=-4M2H.
    H=S.symbols('H',positive=True)
    checks['FRW_constraint']=S.simplify(((pl**2-2*pl*pb)/(4*M2)).subs({pl:-2*M2*H,pb:-4*M2*H})+3*M2*H*H)==0
    return checks,dict(hamiltonian=str(ham),p_lambda=str(pl0),p_beta=str(pb0),rates={str(k):str(v)for k,v in rates.items()},lapse_source=str(lapse_source))


def build(k,rtol):
    ga=.1; ss=.01; amp=.002; KK=.5; a0=.3; VV=.01; M2=1.
    eta=KK*amp/(k*a0);Z0=1+ga*amp+ga*ss
    def n_from(z,Y):
        Z=Z0+KK*amp*Y/k**2; a=1+ga*amp*z
        disc=Z*Z-4*a*ga*ss
        return (Z+np.sqrt(disc))/(2*a)
    def rhs(z,Y):
        N=n_from(z,Y[0])
        return [-N/(1-eta*np.sqrt(max(0,1-z*z)))]
    sol=solve_ivp(rhs,(1,-1),[0.],rtol=rtol,atol=rtol*.01,method='DOP853',dense_output=True)
    assert sol.success,sol.message
    rows=[]
    for count in (256,512,1024,2048):
        th=2*np.pi*(np.arange(count)+.5)/count;z=np.cos(th);dth=2*np.pi/count
        Y=sol.sol(z)[0];NN=n_from(z,Y);PP=amp/k*np.sin(th);DD=amp*z
        XX=ss/(2*NN**2);qq=DD+2*XX
        rr=KK*np.abs(PP)/a0
        WW=a0*a0/KK*(-rr-np.log1p(-rr))
        hsource=-DD-XX-VV-WW-ga*DD**2/2+2*ga*DD*XX
        H0=np.sqrt((ss/2+VV)/(3*M2));pl=-2*M2*H0
        pb=pl/2-2*M2*hsource/pl
        hkin=(pl*pl-2*pl*pb)/(4*M2)
        Yth=(np.roll(Y,-1)-np.roll(Y,1))/(2*dth)
        target=NN*np.sin(th)/(1-eta*np.abs(np.sin(th)))
        pol_res=Yth-target
        Z=NN*(1+ga*DD)+ga*ss/NN
        rows.append(dict(k=k,Ncells=count,rtol=rtol,
            polarization_relative_residual=float(np.max(np.abs(pol_res))/np.max(np.abs(target))),
            Hamiltonian_residual=float(np.max(np.abs(hkin-hsource))),momentum_residual=0.,
            lapse_min=float(NN.min()),lapse_max=float(NN.max()),X_min=float(XX.min()),
            q_min=float(qq.min()),flux_cap_ratio=float(rr.max()),
            current_algebra_residual=float(np.max(np.abs(Z-(Z0+KK*amp*Y/k**2)))),
            lapse_branch_gap=float(np.min(1+ga*DD-ga*ss/NN**2)),p_beta_min=float(pb.min()),p_beta_max=float(pb.max())))
    return rows,sol,n_from


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
    checks,alg=algebra();rows=[];comparisons=[]
    for k in (16,32,64,128):
        coarse,sc,nc=build(k,1e-10);fine,sf,nf=build(k,1e-12);rows.extend(fine)
        zz=np.linspace(-1,1,1001)
        dn=float(np.max(np.abs(nc(zz,sc.sol(zz)[0])-nf(zz,sf.sol(zz)[0]))))
        comparisons.append(dict(k=k,lapse_tolerance_change=dn))
        checks[f'positive_domain_k{k}']=all(r['X_min']>0 and r['q_min']>0 and r['flux_cap_ratio']<1 and r['lapse_branch_gap']>0 for r in fine)
        checks[f'constraints_algebra_k{k}']=all(r['Hamiltonian_residual']<1e-12 and r['current_algebra_residual']<1e-12 for r in fine)
        errs=[r['polarization_relative_residual']for r in fine]
        checks[f'polarization_refinement_k{k}']=all(b<a for a,b in zip(errs,errs[1:]))
        checks[f'lapse_tolerance_k{k}']=dn<1e-9
        # Counterfeit original equation sign: independent flux residual instead sums both terms.
        th=2*np.pi*(np.arange(1024)+.5)/1024;z=np.cos(th);Y=sf.sol(z)[0];NN=nf(z,Y)
        Yth=(np.roll(Y,-1)-np.roll(Y,1))/(4*np.pi/1024)
        target=NN*np.sin(th)/(1-(.5*.002/(k*.3))*np.abs(np.sin(th)))
        residual=Yth+target if args.mutate else Yth-target
        checks[f'pressure_sign_k{k}']=bool(np.max(np.abs(residual))<1e-4)
    out=dict(checks=checks,all_pass=all(checks.values()),mutation=args.mutate,algebra=alg,rows=rows,tolerance=comparisons,
       scope='Exact initial constraints, finite numerical reconstruction; not time evolution or empirical footing test')
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
    raise SystemExit(0 if out['all_pass'] else 1)


if __name__=='__main__':main()
