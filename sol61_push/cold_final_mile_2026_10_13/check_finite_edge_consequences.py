"""CE-FM-053: fixed-charge exterior enthalpy budget and truncated lensing."""
import sys,json
from pathlib import Path
import sympy as sp
import mpmath as mp
mp.mp.dps=40
r,s,eps=sp.symbols('r s eps',positive=True)
checks=[]
def exact(label, expr):
    assert sp.simplify(expr)==0,(label,expr)
    checks.append(label)
x=s/r**2
hc=x**3/(4*sp.pi*(1-x)**2)
measure=eps*4*sp.pi*r**2*hc
exact('enthalpy radial measure', measure-eps*s**3/(r**2-s)**2)
# Integral from r to infinity of threshold enthalpy/c^2 in G=a0=Mb=1.
budget=eps/2*(s**2*r/(r**2-s)-s**sp.Rational(3,2)*sp.atanh(sp.sqrt(s)/r))
exact('budget derivative',sp.diff(budget,r)+measure)
assert sp.limit(budget,r,sp.oo)==0; checks.append('budget infinity limit')
exact('threshold tail power',sp.limit(hc*r**6,r,sp.oo)-s**3/(4*sp.pi))
edge=sp.sqrt(s+s**2)
edge_budget=eps/2*(edge-s**sp.Rational(3,2)*sp.atanh(1/sp.sqrt(1+s)))
exact('finite supply edge substitution',budget.subs(r,edge)-edge_budget)
# Truncated projected density has Sigma=0 outside; aperture mass=s.
R=sp.symbols('R',positive=True)
DS=s/(sp.pi*R**2)
exact('outside projected slope',R*sp.diff(DS,R)/DS+2)
exact('outside normalized amplitude',DS/(1/(4*R))-4*s/(sp.pi*R))
M=(sp.sqrt(1+4*r*r)-1)/2
rho=1/(2*sp.pi*r*sp.sqrt(1+4*r*r))
exact('density derivative',sp.diff(M,r)-4*sp.pi*r*r*rho)
# Nonzero 1/r cusp, despite report's cored terminology.
exact('central density cusp',sp.limit(r*rho,r,0)-1/(2*sp.pi))
rows=[]
for sv in [mp.mpf(1),mp.mpf('5.364'),mp.mpf(20)]:
    Re=mp.sqrt(sv+sv**2)
    analytic=(sv**2*Re/(Re**2-sv)-sv**mp.mpf('1.5')*mp.atanh(mp.sqrt(sv)/Re))/2
    numeric=mp.quad(lambda rr:sv**3/(rr**2-sv)**2,[Re,2*Re,mp.inf])
    assert abs(analytic-numeric)<mp.mpf('1e-35'); checks.append('threshold quadrature '+str(sv))
    rows.append({'supply':str(sv),'edge':str(Re),'threshold_budget_over_Mb_per_epsilon':str(analytic)})
sv=mp.mpf('5.364'); Re=mp.sqrt(sv+sv**2)
rhof=lambda rr:1/(2*mp.pi*rr*mp.sqrt(1+4*rr*rr))
Mprime=lambda rr:2*rr/mp.sqrt(1+4*rr*rr)
Mf=lambda rr:(mp.sqrt(1+4*rr*rr)-1)/2
projections=[]
for RR in map(mp.mpf,['.2','1','2.5','5','5.8','10','20']):
    if RR<Re:
        sig=2*mp.quad(lambda z:rhof(mp.sqrt(RR*RR+z*z)),[0,mp.sqrt(Re*Re-RR*RR)])
        proj=Mf(RR)+mp.quad(lambda rr:Mprime(rr)*(RR/rr)**2/(1+mp.sqrt(1-(RR/rr)**2)),[RR,Re])
        # Independent shell exclusion representation of aperture mass.
        proj2=sv-mp.quad(lambda rr:Mprime(rr)*mp.sqrt(1-(RR/rr)**2),[RR,Re])
        assert abs(proj-proj2)<mp.mpf('1e-35'); checks.append('cylinder mass '+str(RR))
        trunc=proj/(mp.pi*RR*RR)-sig
    else:
        trunc=sv/(mp.pi*RR*RR)
    siginf=2*mp.quad(lambda z:rhof(mp.sqrt(RR*RR+z*z)),[0,RR,mp.inf])
    projinf=Mf(RR)+mp.quad(lambda rr:Mprime(rr)*(RR/rr)**2/(1+mp.sqrt(1-(RR/rr)**2)),[RR,2*RR,mp.inf])
    infinite=projinf/(mp.pi*RR*RR)-siginf
    assert trunc>0 and infinite>0; checks.append('positive ESD '+str(RR))
    projections.append({'R_over_rM':str(RR),'truncated_DeltaSigma_in_Mb_per_rM2':str(trunc),'infinite_DeltaSigma':str(infinite),'truncated_over_infinite':str(trunc/infinite)})
result={'claim_id':'CE-FM-053','checks_passed':len(checks),'checks':checks,'exterior_threshold':rows,'projection_rows':projections,'scope':'Formal scalar local gate and fixed spherical mass projection only; no occupied halo, altered frame proof, metric completion or observational test'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
