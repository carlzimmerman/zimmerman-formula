"""p07: probe-membrane (Brown-Teitelboim) reading of a0. G = c = 1, Heaviside 4-form: rho = E^2/2, Gauss jump DeltaE = e,
membrane action -sigma*Area + e*Int(A3).  Wall between E_out = E and E_in = E - e.
Question: is a0 = 1/R_wall (the Euclidean wall radius, i.e. the wall's proper acceleration) reachable, and what does kappa = 1/2 demand of e/sigma?
Israel (Euclid, same as p06): A - B = 4 pi sigma, A^2 - B^2 = H_out^2 - H_in^2, 1/R^2 = H_in^2 + A^2, H^2 = 8 pi rho/3.
"""
import sympy as sp, math, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
E,e,s,H=sp.symbols('E e sigma H',positive=True)
Hi2=sp.Rational(8,3)*sp.pi*(E-e)**2/2; Ho2=sp.Rational(8,3)*sp.pi*E**2/2
x=4*sp.pi*s
A=sp.Rational(1,2)*((Ho2-Hi2)/x+x)
invR2=Hi2+A**2
# probe limit: sigma -> 0 with e, E fixed  =>  1/R -> DeltaP/(3 sigma), DeltaP = e E - e^2/2
DP=e*E-e**2/2
lim=sp.limit(sp.sqrt(invR2)*s, s, 0, '+')
chk("1 Schwinger radius from Israel: sigma/R -> |DeltaP|/3 (= DeltaP/3 for e < 2E), R = 3 sigma/DeltaP", sp.simplify(lim**2-(DP/3)**2)==0)
# hence in the probe limit a = 1/R = DeltaP/(3 sigma); leading e-small: eE/(3 sigma)
# demand a = a0 = H_out/Z with Z = sqrt(32 pi/3):  e E/(3 sigma) = H_out/Z  (e << E)
Z=sp.sqrt(32*sp.pi/3); Hout=sp.sqrt(Ho2)
ratio=sp.simplify(sp.solve(sp.Eq(e*E/(3*s), Hout/Z), e/s)[0] if False else (3*Hout/(Z*E)))
chk("2 kappa=1/2 requires e/sigma = 3 H/(Z E) = 3/(2 sqrt2) = %.6f (E-independent)"%float(ratio), sp.simplify(ratio-3/(2*sp.sqrt(2)))==0)
# kappa general: Z = sqrt(8 pi/3)/kappa -> e/sigma = 3 sqrt2 kappa /2 ... show it is a free coupling ratio
k=sp.symbols('kappa',positive=True)
r_k=sp.simplify(3*Hout/((sp.sqrt(8*sp.pi/3)/k)*E))
chk("3 general kappa: e/sigma = (3/sqrt2) kappa ... = %s ; every kappa needs a different charge-to-tension ratio"%sp.simplify(r_k), sp.simplify(r_k-3*sp.sqrt(2)*k/2)==0)
# is the probe regime consistent?  need 4 pi sigma << H (gravity of the wall negligible)
val=float(3/(2*math.sqrt(2)))
chk("4 e/sigma target %.4f is O(1): no small/large parameter singles it out (compare 1, sqrt(3/2)=%.4f, 3/2=1.5)"%(val,math.sqrt(1.5)), 0.5<val<2)
# distances of the target from natural extremality-type values -- reported, not claimed
for nm,v in [("1",1.0),("sqrt(3/2)",math.sqrt(1.5)),("3/2",1.5),("sqrt(2)",math.sqrt(2))]:
    print("   target/%s = %.4f"%(nm,val/v))
chk("5 none of the natural values equals the target (control against a hidden hit)", all(abs(val/v-1)>1e-3 for v in [1.0,math.sqrt(1.5),1.5,math.sqrt(2)]))

# 6. consistency: the probe formula a = DeltaP/(3 sigma) is valid only if it is >> H.  At the kappa=1/2 target it equals H/Z << H,
#    so the full junction solution must be used, and it gives 1/R >= H (p06).  Numerical check at the target ratio, E = 1:
import mpmath as mp
Ev=1.0; r=3/(2*math.sqrt(2))
for sv in [1e-2,1e-4,1e-6]:
    ev=r*sv
    hi2=(8*math.pi/3)*(Ev-ev)**2/2; ho2=(8*math.pi/3)*Ev**2/2; xx=4*math.pi*sv
    Av=0.5*((ho2-hi2)/xx+xx); invR=math.sqrt(hi2+Av**2)
    probe=(ev*Ev-ev**2/2)/(3*sv); Hn=math.sqrt(ho2)
    print("   sigma=%.0e: probe a=%.4f  (H/Z=%.4f)  full 1/R=%.4f  H=%.4f"%(sv,probe,Hn/math.sqrt(32*math.pi/3),invR,Hn))
chk("6 at the kappa=1/2 target the probe formula gives H/Z < H but the full solution gives 1/R >= H: the probe reading is inconsistent (wall sits at the horizon, a -> H)", invR>=Hn-1e-9 and probe<Hn)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
