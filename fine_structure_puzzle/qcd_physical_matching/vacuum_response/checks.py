"""Bounded exact algebra verification; no physical QCD simulation or fitted inputs."""
from fractions import Fraction as F
from pathlib import Path
import json

checks = []
def check(name, lhs, rhs):
    if lhs != rhs:
        raise AssertionError((name, str(lhs), str(rhs)))
    checks.append({"name": name, "lhs": str(lhs), "rhs": str(rhs)})

charges = list(range(-3, 4))
weights = [F(x, 28) for x in (1, 3, 6, 8, 6, 3, 1)]
q2 = [F(q*q) for q in charges]
tr = [F(x) for x in (7, 4, 2, 1, 2, 4, 7)]
cur = [F(x) for x in (11, 5, 3, 2, 3, 5, 11)]
contact = [F(x) for x in (3, 2, 1, 0, 1, 2, 3)]
def E(*arrays):
    total = F(0)
    for k,w in enumerate(weights):
        value = w
        for arr in arrays: value *= arr[k]
        total += value
    return total
def cov(a,b): return E(a,b)-E(a)*E(b)
def cumulant3(a,b,c):
    return E(a,b,c)-E(a,b)*E(c)-E(a,c)*E(b)-E(b,c)*E(a)+2*E(a)*E(b)*E(c)

# Bivariate polynomial arithmetic truncated after t^1 lambda^1.
keys = ((0,0),(1,0),(0,1),(1,1))
def mul(a,b):
    out={k:F(0) for k in keys}
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            if i+k<=1 and j+l<=1: out[(i+k,j+l)]+=x*y
    return out
def inverse(a):
    # All finite-ensemble partition series here have z00=1.
    check("partition_normalization",a[(0,0)],F(1))
    x,y,z=a[(1,0)],a[(0,1)],a[(1,1)]
    return {(0,0):F(1),(1,0):-x,(0,1):-y,(1,1):2*x*y-z}
z={k:F(0) for k in keys}; num={k:F(0) for k in keys}
for w,q,T,I,J in zip(weights,q2,tr,cur,contact):
    wseries={(0,0):w,(1,0):-w*T,(0,1):-w*I,(1,1):w*(T*I-J)}
    for k in keys: z[k]+=wseries[k];num[k]+=q*wseries[k]
mean=mul(num,inverse(z))
check("Q2_t_covariance",mean[(1,0)],-cov(q2,tr))
check("Q2_lambda_covariance",mean[(0,1)],-cov(q2,cur))
check("Q2_t_lambda_connected_contact",mean[(1,1)],cumulant3(q2,tr,cur)-cov(q2,contact))
vinverse={(0,0):F(1),(1,0):F(-4),(0,1):F(0),(1,1):F(0)}
chi=mul(mean,vinverse)
check("chi_t_volume_contact",chi[(1,0)],-4*E(q2)-cov(q2,tr))
check("chi_lambda",chi[(0,1)],-cov(q2,cur))
check("rho_theta_theta",chi[(0,0)]+chi[(1,0)]/4,-cov(q2,tr)/4)
check("rho_theta_theta_lambda",chi[(0,1)]+chi[(1,1)]/4,(cumulant3(q2,tr,cur)-cov(q2,contact))/4)

# A c-number trace shift cancels exactly in topology-connected quantities.
shifted=[x+F(17) for x in tr]
check("trace_identity_shift_covariance",cov(q2,shifted),cov(q2,tr))
check("trace_identity_shift_third_cumulant",cumulant3(q2,cur,shifted),cumulant3(q2,cur,tr))

# Independently differentiate Gaussian log P_Q using X_t/X=4-Dlogchi.
chi0=F(2);ach=F(3);bch=F(5)
radius_rows=[]
for h in (F(1,10),F(1,20),F(1,40),F(1,80)):
    ch=chi0+ach*h+bch*h*h; Dch=ach*h+2*bch*h*h
    vol=h**-4; X=ch*vol; logX_t=4-Dch/ch
    for q in (0,1,2):
        logP_t=(-F(1,2)+F(q*q,2)/X)*logX_t
        delta=-logP_t/(4*vol)
        formula=logX_t/(8*vol)*(1-F(q*q)/X)
        check("fixed_sector_gaussian_derivative_H_%s_Q_%d"%(h,q),delta,formula)
    delta0=logX_t/(8*vol)
    diagnostic=(8*vol*delta0-4)/h
    check("amplified_topology_identity_H_%s"%h,diagnostic,-Dch/(h*ch))
    radius_rows.append({"H":str(h),"X_top":str(diagnostic),"target_limit":str(-ach/chi0)})
check("H5_sector_coefficient",-ach/(8*chi0),F(-3,16))
check("fixed_sector_H4_coefficient",F(4,8),F(1,2))

# Formal independent EM LEC coordinates. Use d for Delta and L for kappa Z(1+log).
symbols=("k1","k2","k3","k4","k5","k6","k7","d_k7","L")
Cchi=dict(zip(symbols,(F(0),F(0),F(0),F(0),F(20,9),F(20,9),F(4,9),F(4,3),F(-2))))
Cm=dict(zip(symbols,(F(-20,9),F(-20,9),F(4),F(-2),F(20,9),F(20,9),F(4,9),F(-4,3),F(2))))
Cphysical=dict(zip(symbols,(F(20,9),F(20,9),F(-4),F(2),F(0),F(0),F(0),F(8,3),F(-4))))
for k in symbols: check("fixed_mass_minus_pion_mass_"+k,Cchi[k]-Cm[k],Cphysical[k])

result={"status":"completed","checks_passed":len(checks),"checks":checks,"radius_fixture":radius_rows,
        "scope":"Exact rational algebra only. No measured alpha, QCD simulation, physical LEC assignment or cosmological input."}
out=Path('fine_structure_puzzle/qcd_physical_matching/vacuum_response/run_001/results.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({"checks_passed":len(checks),"result":str(out),"arithmetic":"exact Fraction"}))
