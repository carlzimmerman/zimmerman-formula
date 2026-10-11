"""Exact target flux-cap and orbit-residence audit; no population evolved."""
import json, math, pathlib, sys
S=5.364
qR=math.log1p(1/S)
checks=[]

def simp(f,a,b,n=4096):
    h=(b-a)/n
    return h/3*(f(a)+f(b)+sum((4 if k%2 else 2)*f(a+k*h) for k in range(1,n)))

def mass(r):
    return 1/math.expm1(1/r)

rows=[]
for q in (.5,1,4,10,20):
    r=1/q
    A=q*q*math.exp(-q)/(-math.expm1(-q))**2
    h=r*1e-5
    dM=(mass(r+h)-mass(r-h))/(2*h)
    phi_abs=qR/(-math.expm1(-qR))+math.log(math.expm1(q)/math.expm1(qR))
    independent=qR*(1+S)+simp(lambda u:1/(-math.expm1(-u)),qR,q)
    checks.extend([abs(dM/A-1)<1e-7,abs(independent/phi_abs-1)<1e-8])
    rows.append(dict(q=q,r_over_rM=r,A_over_V2_G=A,vesc_over_V=math.sqrt(2*phi_abs),
                     unsigned_flux_cap_over_V3_G=A*math.sqrt(2*phi_abs)))

# Equal tracer mass/energy, isotropically oriented angular-momentum vectors.
# G Mb=1, E=-1 => semimajor axis b=.5 for both populations.
b=.5
period=2*math.pi*b**1.5
orbit_rows=[]
def residence(r,j):
    vr2=2*(-1+1/r)-j*j/(r*r)
    return 2/(period*math.sqrt(vr2)) if vr2>0 else 0.

for j in (.3,.7):
    ecc=math.sqrt(1-j*j/b)
    n=4096
    norm=0.
    for k in range(n):
        t=(k+.5)*math.pi/n
        r=b*(1-ecc*math.cos(t))
        dr=b*ecc*math.sin(t)
        norm+=residence(r,j)*dr*math.pi/n
    checks.append(abs(norm-1)<1e-7)
    orbit_rows.append(dict(j=j,E=-1,mass=1,total_vector_J=[0,0,0],period=period,
                           rp=b*(1-ecc),ra=b*(1+ecc),normalization=norm,
                           A_at_half=residence(.5,j),A_at_point2=residence(.2,j)))
ratio=orbit_rows[1]['A_at_half']/orbit_rows[0]['A_at_half']
checks.extend([abs(ratio/math.sqrt(41)-1)<1e-13,
               orbit_rows[0]['A_at_point2']>0,orbit_rows[1]['A_at_point2']==0])
# Two dimensionless examples of the coefficient dictionary, not fits.
for Mb,rho in ((1.,1.),(7.,.03)):
    A=(rho*Mb*Mb/4)**.25  # G=c=1
    a=A*A/Mb
    k=a/math.sqrt(rho)
    C=8*math.pi*rho/a**2
    checks.extend([math.isclose(k,.5,rel_tol=1e-14),math.isclose(C,32*math.pi,rel_tol=1e-14)])
out=dict(passed=sum(checks),count=len(checks),supply_ratio=S,flux_caps=rows,
         orbit_populations=orbit_rows,residence_ratio=ratio,
         scope='Target-dependent necessary flux caps and fixed-Kepler tracer counterexample, not a simulated self-gravitating state or coefficient derivation.')
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
sys.exit(0 if all(checks) else 1)
