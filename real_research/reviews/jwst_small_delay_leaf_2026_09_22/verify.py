import json,sys,pathlib,math
from scipy.integrate import quad
# Fixed before computation: main1e-10,refined1e-12; agreement1e-8abs+1e-5rel.
def angular(mu,iso=False):return .5 if iso else .375*(1+mu*mu)
def joint(e,tau,tol,iso=False):
    def outer(r):
        lower=max(-1.,1-e/r)
        def inner(mu):
            L=-r*mu+math.sqrt(1-r*r+r*r*mu*mu)
            return tau*angular(mu,iso)*math.exp(-tau*(r+L))
        return quad(inner,lower,1,epsabs=tol,epsrel=tol)[0]
    lo=quad(outer,0,e/2,epsabs=tol,epsrel=tol)
    hi=quad(outer,e/2,1,epsabs=tol,epsrel=tol)
    return lo[0]+hi[0],lo[1]+hi[1]
def density_cdf(e,tau,tol):
    def outer(x):
        d=e*x;logspan=math.log(2/d)
        def inner(u):
            r=(d/2)*math.exp(u*logspan);mu=1-d/r
            T=d+math.sqrt(1-2*r*d+d*d)
            return e*tau*logspan*angular(mu)*math.exp(-tau*T)
        return quad(inner,0,1,epsabs=tol,epsrel=tol)[0]
    return quad(outer,0,1,epsabs=tol,epsrel=tol)
checks={};rows=[]
for tau in [1.,4.]:
 for e in [.01,.003,.001]:
    j,je=joint(e,tau,1e-10);f,fe=density_cdf(e,tau,1e-10)
    jr,jre=joint(e,tau,1e-12);fr,fre=density_cdf(e,tau,1e-12);neg,ne=joint(e,tau,1e-12,True)
    K=.75*e*math.log(2/e)+.375*e*e-.0625*e**3
    upper=tau*math.exp(-tau)*K;lower=math.exp(-tau*e)*upper;threshold=1e-8+1e-5*max(abs(j),abs(f));tag=f'{tau}_{e}'
    checks[tag+'_coordinates_agree']=abs(j-f)<=threshold
    checks[tag+'_refinement']=max(abs(j-jr),abs(f-fr))<=threshold
    checks[tag+'_negative_rejected']=abs(neg-fr)>threshold
    checks[tag+'_analytic_sandwich']=lower<=fr<=upper
    rows.append(dict(tau=tau,epsilon=e,joint=j,density_integral=f,joint_refined=jr,density_refined=fr,outer_error_estimates=[je,fe,jre,fre],negative_isotropic=neg,lower=lower,upper=upper,threshold=threshold,ratio_to_leading=fr/(.75*tau*math.exp(-tau)*e*math.log(1/e))))
out={'checks':checks,'rows':rows,'scope':'Exactly one scattering only. Quadrature error estimates not interval proofs; analytic sandwich separately derived. Higher-scatter remainder unproved.'};pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print({'passed':sum(checks.values()),'total':len(checks)});assert all(checks.values())
