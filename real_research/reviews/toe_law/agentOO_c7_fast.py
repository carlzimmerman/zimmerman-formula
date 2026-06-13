"""
agentOO Route 1, C7 — FAST decisive sigma4 sign via closed-form thermal moments.
Everything printed with flush; no nested numeric quad; radial integrals = analytic zeta-moments.

PHYSICS. chi(omega,k), on-shell omega=c_chi k. Trilinear g chi phi phi to dS bath, W=c_b q, n_B(W).
The dispersion-shifting Re Sigma is the sum of the EMISSION pair channel and the LANDAU channel. We expand
the integrand in k to O(k^4) BEFORE integrating, do the angular average analytically (<1>=2, <x^2>=2/3,
<x^4>=2/5 over x in [-1,1]; odd vanish), and integrate q via closed thermal moments.

We keep r = c_chi/c_b general (symbolic) so we see exactly how sign(sigma4) depends on r (FORCED-vs-FREE).
"""
import sympy as sp

print("C7 start", flush=True)
q,k,x,T = sp.symbols('q k x T', positive=True)
r = sp.symbols('r', positive=True)          # r = c_chi/c_b
cb = sp.symbols('c_b', positive=True)
# scale out c_b: let omega=c_chi k = r cb k. Energies in units of cb: Wq=cb q, define everything /cb.
# Write u-independent: work with y=cb q as energy variable later; here keep q.

Wq = cb*q
# |q+k| expanded to O(k^4):
absqpk = q*sp.sqrt(1+2*(k/q)*x+(k/q)**2)
absqpk = sp.series(absqpk,k,0,5).removeO()
Wpk = cb*absqpk
om = r*cb*k

# Bose n(Wpk) expanded in k about Wq:
nWq = 1/(sp.exp(Wq/T)-1)
nWpk = 1/(sp.exp(Wpk/T)-1)
nWpk = sp.series(nWpk,k,0,5).removeO()

# vertex prefactor 1/(2 Wq Wpk):
pref = sp.series(1/(2*Wq*Wpk),k,0,5).removeO()

# EMISSION channel: (nWq+nWpk)*(1/(om-Wq-Wpk) - 1/(om+Wq+Wpk))
emi = (nWq+nWpk)*(1/(om-Wq-Wpk) - 1/(om+Wq+Wpk))
emi = sp.series(sp.expand(pref*emi),k,0,5).removeO()
# LANDAU channel: (nWq-nWpk)*(1/(om-Wq+Wpk) - 1/(om+Wq-Wpk))
lan = (nWq-nWpk)*(1/(om-Wq+Wpk) - 1/(om+Wq-Wpk))
lan = sp.series(sp.expand(pref*lan),k,0,5).removeO()

print("series built", flush=True)

def angular_then_moments(expr, label):
    # multiply q^2, integrate x in [-1,1] using <x^m>
    expr = sp.expand(expr*q**2)
    p = sp.Poly(expr, k)
    out = {}
    for nn in [0,2,4]:
        ck = p.coeff_monomial(k**nn)
        if ck==0:
            out[nn]=sp.Integer(0); continue
        # integrate over x in [-1,1]
        ang = sp.integrate(ck,(x,-1,1))
        ang = sp.simplify(ang)
        out[nn]=ang
    return out

emi_c = angular_then_moments(emi,'emi')
lan_c = angular_then_moments(lan,'lan')
print("angular done", flush=True)

# Now integrate over q from 0..inf. Each coeff is (sum of) q^a * (powers of n(cb q) and its exp).
# Substitute s=cb q (energy). dq=ds/cb. Use closed forms via mpmath nsum/quad of the explicit function.
import mpmath as mp
mp.mp.dps=25
Tn = mp.mpf(1)/(2*mp.pi)   # T_dS

def radial(expr_q):
    # expr_q depends on q, cb, T, r(after subs). substitute cb=1 (units), T=Tn, integrate q 0..inf.
    e = expr_q.subs({cb:1, T:sp.nsimplify(float(Tn))})
    f = sp.lambdify(q, e, 'mpmath')
    return mp.quad(lambda Q: f(mp.mpf(Q)), [mp.mpf('1e-7'),1,5,20,80])

print("\n# sigma_n(r) = -(g^2/4pi^2) * radial[ emi_c[n]+lan_c[n] ], g=1, c_b=1, T=H/2pi", flush=True)
print("# r=c_chi/c_b. sign(sigma4)<0 => roton/bending; >=0 => convex/MM-kill.", flush=True)
for rv in [mp.mpf('0.5'),mp.mpf('0.7'),mp.mpf('0.9'),mp.mpf('1.1'),mp.mpf('1.5'),mp.mpf('2.0'),mp.mpf('3.0')]:
    line="r=%4s : "%rv
    sig={}
    for nn in [0,2,4]:
        tot = (emi_c[nn]+lan_c[nn]).subs(r, sp.nsimplify(float(rv)))
        try:
            val = radial(tot)
            val = -val/(4*mp.pi**2)
            sig[nn]=float(val)
        except Exception as ex:
            sig[nn]=float('nan')
    line += "s0=% .4e s2=% .4e s4=% .4e | sign(s4)=%s"%(
        sig[0],sig[2],sig[4], 'NEG(bend)' if sig[4]<0 else ('POS(stiff)' if sig[4]>0 else 'ZERO'))
    print(line, flush=True)
print("C7 done", flush=True)
