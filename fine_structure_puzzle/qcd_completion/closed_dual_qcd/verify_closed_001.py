"""CDQ-001 finite checks; immutable after first execution. See contract_001.json."""
import json
from pathlib import Path
import mpmath as mp

OUT = Path("fine_structure_puzzle/qcd_completion/closed_dual_qcd/runs/closed-001/result.json")


def calculate(dps):
    mp.mp.dps = dps
    checks = []
    tables = {}

    def check(name, left, right, tolerance="1e-40", scale=None):
        scl = max(mp.mpf(1), abs(left), abs(right)) if scale is None else scale
        error = abs(left - right) / scl
        checks.append({"name": name, "scaled_error": mp.nstr(error, 25),
                       "tolerance": tolerance, "passed": bool(error < mp.mpf(tolerance))})
        assert error < mp.mpf(tolerance), (name, mp.nstr(error), tolerance)

    # Independent compact quadrature, Bessel evaluation, and integer-topology sum.
    topology = []
    qmax = 120
    for lam in map(mp.mpf, ["0.05", "0.5", "2", "8"]):
        weights = [mp.besseli(q, 2*lam)**2 for q in range(qmax+1)]
        # I_n(2lambda) <= lambda^n/n! exp(lambda²/(n+1)).
        n0 = qmax+1
        first_bound = (lam**n0/mp.factorial(n0))**2 * mp.exp(2*lam**2/(n0+1))
        ratio_bound = (lam/(n0+1))**2
        abs_tail = 2*first_bound/(1-ratio_bound)
        for theta in [mp.mpf("0"), mp.mpf("0.7"), mp.mpf("2"), mp.pi, mp.mpf("3.8")]:
            z = 4*lam*mp.cos(theta/2)
            integral = mp.quad(lambda t: mp.exp(z*mp.cos(t)), [0, mp.pi, 2*mp.pi])/(2*mp.pi)
            bessel = mp.besseli(0, z)
            topo = weights[0]+2*sum(weights[q]*mp.cos(q*theta) for q in range(1,qmax+1))
            check("uniform integral = I0", integral, bessel)
            check("integer topology = I0", topo, bessel)
            check("theta 2pi periodicity", mp.besseli(0,4*lam*mp.cos((theta+2*mp.pi)/2)), bessel)
            assert abs_tail < mp.mpf("1e-140")
            topology.append({"lambda":mp.nstr(lam),"theta":mp.nstr(theta,25),
                             "Z":mp.nstr(bessel,45),"absolute_tail_bound":mp.nstr(abs_tail,15)})
    tables["topology"] = topology

    # Orthogonal Poisson and direct spectral sums for the S3 heat trace.
    heat = []
    nmax, kmax = 200, 40
    for s in map(mp.mpf,["0.03","0.1","0.4","1","3","10"]):
        direct = sum(n*n*mp.exp(-s*(n*n-1)) for n in range(1,nmax+1))
        poisson = mp.exp(s)*mp.sqrt(mp.pi)/(4*s**mp.mpf("1.5"))*(1+2*sum(
            (1-2*mp.pi**2*k*k/s)*mp.exp(-mp.pi**2*k*k/s) for k in range(1,kmax+1)))
        check("S3 heat Poisson/direct", direct, poisson)
        # Explicit geometric bounds for each fixed grid point.
        n=nmax+1
        ratio=((mp.mpf(n+1)/n)**2)*mp.exp(-s*(2*n+1))
        n_tail=n*n*mp.exp(-s*(n*n-1))/(1-ratio)
        k=kmax+1
        # For k>=41 and s<=10, positive magnitudes grow polynomially but
        # their adjacent ratio is bounded by 4 exp[-pi²(2k+1)/s].
        mag=(1+2*mp.pi**2*k*k/s)*mp.exp(-mp.pi**2*k*k/s)
        ratio_k=4*mp.exp(-mp.pi**2*(2*k+1)/s)
        k_tail=mp.exp(s)*mp.sqrt(mp.pi)/(2*s**mp.mpf("1.5"))*mag/(1-ratio_k)
        assert max(n_tail,k_tail) < mp.mpf("1e-400")
        heat.append({"s":str(s),"K":mp.nstr(direct,45),
                     "spectral_tail_bound":mp.nstr(n_tail,12),"Poisson_tail_bound":mp.nstr(k_tail,12)})
    tables["heat_trace"] = heat

    def wrap(a):
        q=mp.exp(-2*mp.pi*a)
        return a*a*mp.polylog(1,q)/2+a*mp.polylog(2,q)/(2*mp.pi)+mp.polylog(3,q)/(4*mp.pi**2)

    def determinant(R,m=mp.mpf(1)):
        a=mp.sqrt((m*R)**2-1)
        return -mp.pi*a**3/6+wrap(a)

    # Winding integral independently fixes the integration constant.
    winding=[]
    for a in map(mp.mpf,["0.2","1","4"]):
        integral=mp.pi*mp.quad(lambda t:t*t/mp.expm1(2*mp.pi*t),[a,a+1,a+4,mp.inf])
        check("winding integral/polylogs",integral,wrap(a))
        winding.append({"a":str(a),"W_wrap":mp.nstr(wrap(a),45)})
    tables["winding"] = winding

    # Absolutely convergent independent mass Hessian, with an analytic tail.
    hessians=[]
    ncut, orders=200,28
    for a in map(mp.mpf,["0.2","0.5","1","3","10"]):
        y=a*a
        finite=sum(mp.mpf(n*n)/(n*n+y)**2 for n in range(1,ncut+1))
        tail=sum((-1)**k*(k+1)*y**k*mp.zeta(2*k+2,ncut+1) for k in range(orders+1))
        bound=(orders+2)*y**(orders+1)*mp.zeta(2*orders+4,ncut+1)
        hessian=-mp.pi*mp.coth(mp.pi*a)/(8*a)+mp.pi**2/(8*mp.sinh(mp.pi*a)**2)
        check("mass Hessian spectral/closed",-(finite+tail)/2,hessian)
        assert bound < mp.mpf("1e-75")
        hessians.append({"a":str(a),"hessian":mp.nstr(hessian,45),"tail_bound":mp.nstr(bound,15)})
    tables["mass_hessians"] = hessians

    # Spatial metric variation independently differentiates the determinant.
    responses=[]
    for R in map(mp.mpf,["1.05","1.2","2","4","8","16","32","64"]):
        a=mp.sqrt(R*R-1)
        exact=(1-a/R*mp.coth(mp.pi*a))/(12*mp.pi)
        by_metric=mp.diff(determinant,R)/(6*mp.pi**2*R*R)+1/(12*mp.pi)
        check("spatial metric derivative",exact,by_metric)
        deltaW=determinant(R)+mp.pi*R**3/6
        responses.append({"mR":str(R),"delta_tau_s_L1_m1":mp.nstr(exact,45),
                          "R_delta_tau_s":mp.nstr(R*exact,45),
                          "R2_delta_tau_s":mp.nstr(R*R*exact,45),
                          "deltaW":mp.nstr(deltaW,45)})
    tables["responses"] = responses

    # Canonical constant-mode saddle removes the exact Gaussian volume term.
    uniform=[]
    u,kappa,mu=mp.mpf("0.7"),mp.mpf("2"),mp.mpf("1.3")
    for z in map(mp.mpf,["10","100","1000","10000"]):
        V=z/u
        def wconst(v):
            return -mp.log(mu*mp.sqrt(2*mp.pi*kappa*v))-mp.log(mp.besseli(0,u*v))
        exact=-u*mp.besseli(1,z)/mp.besseli(0,z)-1/(2*V)
        check("canonical compact metric derivative",exact,mp.diff(wconst,V))
        gaussian=lambda v:-mp.log(mu*mp.sqrt(2*mp.pi*kappa*v))-u*v+mp.log(2*mp.pi*u*v)/2
        check("Gaussian constant canonical cancellation",mp.diff(gaussian,V),-u)
        uniform.append({"z":str(z),"scaled_residual":mp.nstr(z*z*(exact+u)/u,45)})
    tables["uniform_measure"] = uniform

    # Response to unspecified matching shifts, derived from local F.
    u0,k0,u1,k1=map(mp.mpf,["0.7","2","0.03","-0.02"])
    F=lambda u,k:-u-(u/k)**mp.mpf("1.5")/(12*mp.pi)
    m=mp.sqrt(u0/k0)
    analytic=-(1+m/(8*mp.pi*k0))*u1+m**3*k1/(8*mp.pi*k0)
    numeric=mp.diff(lambda h:F(u0+u1*h,k0+k1*h),mp.mpf(0))
    check("matching-shift chain rule",analytic,numeric)
    tables["matching_shift"]={"C1":mp.nstr(analytic,45),"spatial_A_L1":mp.nstr(2*analytic/3,45)}
    return {"dps":dps,"checks":checks,"count":len(checks),"tables":tables}


first=calculate(60)
second=calculate(85)
# Compare all returned numerical scientific tables at independent precision.
def leaves(obj):
    if isinstance(obj,dict):
        for key in sorted(obj):
            yield from leaves(obj[key])
    elif isinstance(obj,list):
        for value in obj:
            yield from leaves(value)
    else:
        yield obj

errors=[]
for a,b in zip(leaves(first["tables"]),leaves(second["tables"])):
    try:
        a,b=mp.mpf(a),mp.mpf(b)
    except (TypeError,ValueError):
        assert a==b
        continue
    errors.append(abs(a-b)/max(1,abs(a),abs(b)))
max_error=max(errors)
assert max_error < mp.mpf("1e-40")
result={"claim_id":"CDQ-001","outcome":"finite assertions verified within declared tolerances",
        "precisions":[60,85],"checks_per_precision":first["count"],
        "repeated_precision_max_scaled_table_error":mp.nstr(max_error,25),
        "records":[first,second],
        "non_claims":["No interval certification", "No full interacting ensemble beyond Gaussian order", "No curved hard matching", "No physical QCD, alpha dependence or proton ratio"]}
OUT.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"checks_per_precision":first["count"],"max_scaled_precision_error":str(max_error),
                  "result":str(OUT)}))
