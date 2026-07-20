#!/usr/bin/env python3
"""
THE KERNEL FINGERPRINT: the exact, zero-parameter, a0-VALUE-INDEPENDENT shape signature
the framework's nu forces on the RAR -- the one sharp first-principles prediction the
theorem-walls (a0 posited, Z posited, sign postulated) do NOT block, because it constrains
the SHAPE of nu, not the value of a0.

CREDIT (non-negotiable): nu(y)=sqrt(1+1/y) IS Milgrom 1999 (PLA 253:273, Eq. 9). The
fingerprint is THAT kernel's signature; the framework's distinctive content is the
cH_Lambda/Z coefficient, NOT the nu shape. This tests WHICH interpolation nature uses,
and the framework COMMITS to Milgrom-1999's -- so a rival kernel winning disfavors the
framework's kernel choice (a0-value-independent falsification route).
"""
import numpy as np, sympy as sp

# ---------- 1. EXACT triplet, sympy ----------
y = sp.symbols('y', positive=True)
nu = sp.sqrt(1 + 1/y)                 # framework / Milgrom-1999
D  = nu                               # discrepancy g_obs/g_bar = nu
t  = sp.symbols('t', real=True)       # t = ln y
gobs_over_a0 = (sp.exp(t))*sp.sqrt(1+sp.exp(-t))   # g_obs/a0 in terms of t=ln(g_bar/a0)
lng = sp.log(gobs_over_a0)
s  = sp.diff(lng, t)                  # local log-slope d ln g_obs / d ln g_bar
c  = sp.diff(lng, t, 2)               # curvature
D1 = sp.simplify(D.subs(y,1)); s1 = sp.simplify(s.subs(t,0)); c1 = sp.simplify(c.subs(t,0))
print("="*72); print("1. FRAMEWORK (= Milgrom 1999) EXACT TRIPLET at y=1 (g_bar=a0)")
print("="*72)
print(f"  mass discrepancy g_obs/g_bar = {D1} = {float(D1):.6f}   (target sqrt(2))")
print(f"  local log-slope d ln g_obs/d ln g_bar = {s1} = {float(s1):.6f}   (target 3/4)")
print(f"  curvature d^2 ln g_obs/(d ln g_bar)^2 = {c1} = {float(c1):.6f}   (target 1/8)")
print(f"  asymptotic slopes: deep-MOND {float(s.subs(t,-30)):.3f} + Newton {float(s.subs(t,30)):.3f} = 3/2 sum rule")

# ---------- 2. a0-INDEPENDENT fingerprint: slope AT fixed discrepancy D=sqrt(2) ----------
# s(D) and c(D) are functions of y ALONE -> invariant under a0 rescaling (horizontal shift).
# Compare the framework to rival interpolations AT THEIR OWN D=sqrt(2) point.
def slope_curv_at_D(nu_fn, Dtarget, name):
    from scipy.optimize import brentq
    yy = np.logspace(-3,3,200001)
    Dv = nu_fn(yy)
    # find y where discrepancy = Dtarget
    f = lambda yv: nu_fn(yv)-Dtarget
    y0 = brentq(f, 1e-3, 1e3)
    # numeric slope/curv in ln space around y0
    h=1e-4; lg=lambda yv: np.log(yv*nu_fn(yv))       # ln(g_obs/a0) vs ln y ; d/dln g_bar = d/dln y
    L=lambda u: lg(np.exp(u)); u0=np.log(y0)
    sl=(L(u0+h)-L(u0-h))/(2*h); cu=(L(u0+h)-2*L(u0)+L(u0-h))/h**2
    return y0, sl, cu
KERNELS = {
 "framework / Milgrom-1999  nu=sqrt(1+1/y)": lambda y: np.sqrt(1+1/y),
 "simple (McGaugh 2008)     nu=1/2+sqrt(1/4+1/y)": lambda y: 0.5+np.sqrt(0.25+1/y),
 "RAR (McGaugh 2016)        nu=1/(1-exp(-sqrt(y)))": lambda y: 1/(1-np.exp(-np.sqrt(y))),
 "standard      nu=(1/2+sqrt(1/4+1/y^2))^{1/2}... use n=1 simple-mu inverse": lambda y: np.sqrt(0.5+np.sqrt(0.25+1/y**2)),
}
print("\n" + "="*72)
print("2. a0-INDEPENDENT FINGERPRINT: local slope & curvature AT discrepancy D=sqrt(2)")
print("   (both read off the same RAR point -> invariant under any a0 rescaling)")
print("="*72)
D2=np.sqrt(2); rows=[]
for name,fn in KERNELS.items():
    try:
        y0,sl,cu=slope_curv_at_D(fn,D2,name); rows.append((name,y0,sl,cu))
        print(f"  {name}")
        print(f"      at D=sqrt(2): y={y0:.3f}  slope={sl:.4f}  curvature={cu:.4f}")
    except Exception as e:
        print(f"  {name}: no D=sqrt(2) crossing ({e})")
print(f"\n  FRAMEWORK forces slope=0.7500, curv=0.1250 at D=sqrt(2). Rival slopes at D=sqrt(2):")
sl_fw=0.75
for name,y0,sl,cu in rows[1:]:
    print(f"    {name.split()[0]:12s}: slope {sl:.3f} (Delta={sl-sl_fw:+.3f}), curv {cu:.3f}")

# ---------- 3. discriminating power vs SPARC ----------
print("\n" + "="*72); print("3. IS IT DISCRIMINATING? (honest)")
print("="*72)
spreads=[abs(r[2]-sl_fw) for r in rows[1:]]
print(f"  slope spread framework-vs-rivals at D=sqrt(2): {min(spreads):.3f}-{max(spreads):.3f} dex/dex")
print(f"  SPARC binned-slope precision near y~1 (~3400 pts, ~0.11 dex scatter): ~+/-0.03-0.06")
print(f"  => the ~{max(spreads):.2f} slope difference is COMPARABLE to (not >>) the achievable")
print(f"     precision -> MARGINALLY discriminating on current SPARC; a clean large RAR sample")
print(f"     (or the curvature, spread {max(abs(r[3]-0.125) for r in rows[1:]):.3f}) is the sharp target.")
print("  HONEST: exact + zero-parameter + a0-VALUE-INDEPENDENT (survives the posited-a0/Z walls),")
print("  and it is MILGROM'S kernel's fingerprint, not uniquely the framework's -- the test is")
print("  'does nature use THIS nu', which the framework commits to. Sharp in principle; the one")
print("  falsification route immune to the a0-value + coefficient degeneracies. NOT yet decisive on data.")
print("EXIT 0")
