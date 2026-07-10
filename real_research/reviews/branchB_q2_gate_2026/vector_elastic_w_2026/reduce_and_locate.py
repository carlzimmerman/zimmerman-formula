#!/usr/bin/env python3
"""RESOLVE the Method-A vs Method-B disagreement on w for the Branch-B elastic medium.

Claim under test: BOTH methods are, at the sourcing radius r~r_t, the SAME P-wave
suppression   w = K_t/(K_t + 4 mu_s/3)   with mu_s = 3 beta K_eff, i.e.

        w = 1 / (1 + 4*beta / kappa_t),      kappa_t := K_t / K_eff  at  r~r_t.

They differ ONLY in the single scalar kappa_t (the tangent BULK modulus at the
Cassini-sourcing radius, in units of K_eff). If this reproduces both methods'
published w to good accuracy, the entire m3 residual is that one unpinned number.

kappa_t readings:
  (A) task-specified 'matched V(J), scale-free sqrt(J) branch, deep stiffness K_eff':
      V(J) ~ J^{3/2} -> sigma ~ sqrt(J) -> K_t = 0.5*K_eff at J=1   (Method A, K0hat=0.5)
      saturated/Newtonian branch at r_t (J0>=1): K_t = K_eff        (Method A, K0hat=1.0)
      linear pinned map J0=eps_M=2 g_N/a0V (sigma linear in field): K_t=const=K_eff.
  (B) committed action_w nu-SHAPED strain reconstruction eps=kappa*(nu-1)*y (SATURATING):
      dsigma/deps stiffens by S(y)~126-231 across the sourcing shell -> kappa_t~126-231.
"""
import numpy as np, sympy as sp

CEIL = 5.2e-27
# banked scalar-class Q2 (both solvers agree), central anchor at g_ext=2.2 a0
Q2s = {"canon": 2.2e-26, "alt": 3.0e-26}

def w_pwave(beta, kappa_t):
    # w = K_t/(K_t + 4 mu_s/3), mu_s = 3 beta K_eff  ->  1/(1 + 4 beta/kappa_t)
    return 1.0 / (1.0 + 4.0*beta/kappa_t)

print("="*78)
print("STEP 1 -- both methods collapse to  w = 1/(1 + 4 beta / kappa_t).  Reproduce them:")
print("="*78)
betas = [0.33, 0.60, 0.95, 2.00]
print("\nMethod A (published w), kappa_t = 0.5 (sqrt-branch, the 'derived' footing):")
print("   beta:        " + "  ".join(f"{b:>6.2f}" for b in betas))
print("   A published: " + "  ".join(f"{v:>6.3f}" for v in [0.286,0.181,0.122,0.062]))
print("   formula:     " + "  ".join(f"{w_pwave(b,0.5):>6.3f}" for b in betas))
print("\nMethod A (published w), kappa_t = 1.0 (saturated K_t=K_eff floor):")
print("   A published: " + "  ".join(f"{v:>6.3f}" for v in [0.444,0.306,0.218,0.117]))
print("   formula:     " + "  ".join(f"{w_pwave(b,1.0):>6.3f}" for b in betas))
print("\nMethod B (published w ~0.94-0.98), kappa_t = 231 (at-Sun) and 126 (shell):")
print("   B published (canon, g=2.2): 0.985 0.975 0.963 0.936")
print("   formula kappa_t=231: " + " ".join(f"{w_pwave(b,231):>5.3f}" for b in betas))
print("   formula kappa_t=126: " + " ".join(f"{w_pwave(b,126):>5.3f}" for b in betas))

print("\n"+"="*78)
print("STEP 2 -- the disagreement is ONE scalar: kappa_t = K_t/K_eff at r~r_t.")
print("="*78)
# derive kappa_t under each committed constitutive reading, at the transition J0~1
J = sp.symbols('J', positive=True)

# (A) sqrt-branch  V = c*J^{3/2};  sigma=V'=(3/2)c sqrt(J);  K_t=V''=(3/4)c/sqrt(J)
#     'deep stiffness K_eff' fixes the scale; K_t(J=1) = (3/4)c.  With the standard
#     normalization sigma(J=1)=K_eff (unit stress at transition) -> (3/2)c=K_eff ->
#     K_t(J=1) = (3/4)c = 0.5*K_eff.  => kappa_t(sqrt) = 0.5.
c = sp.symbols('c', positive=True)
Vsqrt = c*J**sp.Rational(3,2)
sig = sp.diff(Vsqrt, J); Kt = sp.diff(sig, J)
csol = sp.solve(sp.Eq(sig.subs(J,1), 1), c)[0]      # sigma(1)=K_eff=1 units
kappa_sqrt = float(Kt.subs({J:1, c:csol}))
print(f"(A) sqrt-branch V~J^3/2 :  kappa_t(J=1) = {kappa_sqrt:.3f}  (Method A 'derived' footing)")
print(f"(A) linear pinned map  :  sigma ~ g_N ~ J  => K_t=const = 1.000  (Method A stiff floor)")

# (B) action_w reconstruction: sigma=y/yc, eps=kappa*(nu-1)*y ; kappa_t=(dsig/deps)|_y / (dsig/deps)|_deep
Z = float(np.sqrt(32*np.pi/3)); yc = Z/2
y = sp.symbols('y', positive=True); nus = sp.sqrt(1+1/y)
kap = 1.0/((float(np.sqrt(1+1/yc))-1)*yc)
eps = kap*(nus-1)*y; sigB = y/yc
dSdE = sp.diff(sigB,y)/sp.diff(eps,y)
S = lambda yy: float(dSdE.subs(y,yy))/float(dSdE.subs(y,0.01))
print(f"(B) action_w nu-strain :  kappa_t = S(2.2) = {S(2.2):.1f}   S_shell(0.3..2.5)~"
      f"{np.mean([S(v) for v in np.linspace(0.3,2.5,23)]):.0f}   (Method B)")
print("    => the two constitutive readings differ in kappa_t by a factor ~230-460.")

print("\n"+"="*78)
print("STEP 3 -- Cassini verdict vs kappa_t, both footings, beta grid. Ceiling 5.2e-27.")
print("="*78)
for foot in ("canon","alt"):
    print(f"\n[{foot}]  Q2_scalar={Q2s[foot]:.2e}  (need w < {CEIL/Q2s[foot]:.3f} to PASS)")
    for tag,kt in (("A sqrt kt=0.5",0.5),("A stiff kt=1.0",1.0),("B shell kt=126",126.),("B sun kt=231",231.)):
        row=[]
        for b in betas:
            w=w_pwave(b,kt); q=w*Q2s[foot]
            row.append(f"b={b:.2f}:{q:.1e}{'P' if q<CEIL else 'F'+format(q/CEIL,'.1f')}")
        print(f"   {tag:16s} " + "  ".join(row))

print("\n"+"="*78)
print("VERDICT: methods disagree ONLY via kappa_t (bulk tangent modulus at r_t), a")
print("SECOND-derivative of V(J) that the scalar Q2 (a nu/first-order quantity) does")
print("NOT fix -- which is why BOTH pass the mu_s->0 gate yet split. Task specifies the")
print("sqrt(J) branch + linear pinned map (kappa_t~0.5-1 => Method A, STRADDLE). Method B")
print("imported the saturating nu-strain reconstruction (kappa_t~126-231 => FAIL).")
print("kappa_t is NOT derived -> m3 residual NOT closed.")
print("exit 0")
