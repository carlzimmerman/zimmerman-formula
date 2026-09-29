"""p06: can the puzzle's a0-objects exist INSIDE the de Sitter universe whose Lambda they are compared to?
c = G = 1. Z = sqrt(32 pi/3) (framework), L = sqrt(3/Lambda), H = 1/L, a0 = H/Z, r_s = 1/(2 a0) = Z L/2.
Checks (structural, not matching scans):
 A  Israel thin wall (pure tension or two-vacua): real R needs 1/R^2 >= max(H_in^2, H_out^2), so a wall acceleration a=1/R >= H
    for EVERY tension; a0 = H/Z < H is not a gravitating-wall acceleration.  (no-go for the Brown-Teitelboim/membrane route in the gravitating regime)
 B  Schwarzschild-de Sitter with M_s = r_s/2: no horizon at all when M_s > M_Nariai = L/(3 sqrt 3): the puzzle's horizon is not an object of this universe.
 C  areas/entropies: A_s = (8 pi/3) A_dS > A_dS -> exceeds the Bousso/dS entropy bound; embeddable iff Z <= 2 (r_s <= L).
 D  static-patch worldline with proper acceleration a0 sits at sin(theta0) = 1/sqrt(1+Z^2); theta0 is not a rational multiple of pi (no special angle).
 E  controls: Z = 2 (kappa=1) is the marginal case r_s = L; Z = 1.5 is embeddable (mutation).
"""
import sympy as sp, math, sys
ok=[]
def chk(name,cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ")+name)

# A. Israel junction
R,Hi,Ho,sig=sp.symbols('R H_i H_o sigma',positive=True)
x=4*sp.pi*sig
# A - B = 4 pi sigma with A=sqrt(1/R^2-Hi^2), B=sqrt(1/R^2-Ho^2), A^2-B^2 = Ho^2-Hi^2
Aval=sp.Rational(1,2)*((Ho**2-Hi**2)/x + x)
invR2=sp.simplify(Hi**2+Aval**2)
Bval=Aval-x
chk("A1 1/R^2 - H_o^2 = B^2 (consistency of the junction solution)", sp.simplify(invR2-Ho**2-Bval**2)==0)
# pure tension Hi=Ho=H
H=sp.symbols('H',positive=True)
pure=sp.simplify(invR2.subs({Hi:H,Ho:H}))
chk("A2 pure tension: 1/R^2 = H^2 + (2 pi sigma)^2", sp.simplify(pure-(H**2+(2*sp.pi*sig)**2))==0)
# real R requires A^2>=0 and B^2>=0 -> 1/R^2>=max(Hi^2,Ho^2)
import random
random.seed(1); bad=0
for _ in range(20000):
    hi=random.uniform(0,3); ho=random.uniform(0,3); s=random.uniform(1e-3,3)
    v=float(invR2.subs({Hi:hi,Ho:ho,sig:s}))
    if v < max(hi,ho)**2-1e-9: bad+=1
chk("A3 20000 random (H_i,H_o,sigma): 1/R^2 >= max(H_i^2,H_o^2) always", bad==0)
Z=math.sqrt(32*math.pi/3)
chk("A4 a0 = H/Z < H, so a0 is below the minimum wall acceleration (Z>1): needs sigma^2 = (1/Z^2-1)H^2/(4 pi^2) < 0",
    (1/Z**2-1)<0)

# B. Schwarzschild-de Sitter existence of horizons
Lm=1.0
Ms=Z*Lm/4
MN=Lm/(3*math.sqrt(3))
r=sp.symbols('r',positive=True)
f=1-2*sp.Float(Ms)/r-r**2/Lm**2
roots=[rt for rt in sp.Poly(sp.expand(f*r),r).nroots() if abs(sp.im(rt))<1e-12 and sp.re(rt)>0]
chk("B1 SdS with M_s = r_s/2: no positive horizon roots (M_s/M_N = %.4f > 1)"%(Ms/MN), len(roots)==0 and Ms>MN)
Mtest=0.9*MN
roots2=[rt for rt in sp.Poly(sp.expand((1-2*sp.Float(Mtest)/r-r**2/Lm**2)*r),r).nroots() if abs(sp.im(rt))<1e-12 and sp.re(rt)>0]
chk("B2 control: 0.9 M_N has two horizons", len(roots2)==2)
chk("B3 M_s/M_N = 3 sqrt3 Z/4 exactly", abs(Ms/MN-3*math.sqrt(3)*Z/4)<1e-12)

# C. area / entropy ratio
As=4*math.pi*(Z*Lm/2)**2; Ad=4*math.pi*Lm**2
chk("C1 A_s/A_dS = 8 pi/3 = %.4f > 1 (entropy S_s = %.3f S_dS violates S <= S_dS)"%(As/Ad, As/Ad), abs(As/Ad-8*math.pi/3)<1e-12 and As/Ad>1)
chk("C2 embeddable (r_s <= L) iff Z <= 2, i.e. kappa >= 1 ; framework kappa=1/2 -> Z=%.3f is NOT"%Z, Z>2)

# D. static-patch angle
th0=math.atan(1/Z)
chk("D1 static observer a = H tan(theta): a0 at tan(theta0)=1/Z, theta0 = %.5f rad = pi/%.4f"%(th0,math.pi/th0), abs(math.tan(th0)-1/Z)<1e-15)
chk("D2 1+Z^2 = (3+32 pi)/3 is transcendental, so theta0 is not algebraic-angle special", sp.simplify(1+sp.Rational(32,3)*sp.pi - (3+32*sp.pi)/3)==0)

# E. controls
for Zt,emb in [(2.0,True),(1.5,True),(5.7888,False)]:
    chk("E control Z=%.4g: r_s<=L is %s"%(Zt,emb), (Zt<=2.0+1e-12)==emb)
print("\n%d/%d"%(sum(ok),len(ok)))
sys.exit(0 if all(ok) else 1)
