import sympy as sp
import math

k, c, G, Lam, pi = sp.symbols('kappa c G Lambda pi', positive=True)

# ---------- R1 ----------
rho = Lam*c**2/(8*pi*G)
a0 = k*c*sp.sqrt(G*rho)
print("a0 =", sp.simplify(sp.powsimp(a0, force=True)))
HL = sp.sqrt(8*pi*G*rho/3)
print("H_L =", sp.simplify(sp.powsimp(HL, force=True)))
ratio = sp.simplify(sp.powsimp(a0/(c*HL), force=True))
print("ratio a0/(cH) =", ratio)
print("   sqrt(3/(8pi)) =", sp.sqrt(3/(8*pi)), float(sp.sqrt(3/(8*pi))))
print("   at k=1/2 :", sp.Rational(1,2)*sp.sqrt(3/(8*pi)), float(sp.Rational(1,2)*sp.sqrt(3/(8*pi))))
n = 2*sp.sqrt(32*sp.pi/3)
print("2sqrt(32pi/3) =", sp.simplify(n), float(n), "  12/(.) =", float(12/n), " 12/(.)-1 =", float(12/n-1))
print("1/sqrt(3/8pi) =", float(1/sp.sqrt(3/(8*sp.pi))))

cc=2.99792458e8; GG=6.67430e-11; LL=1.0890e-52
a0num = 0.5*cc*math.sqrt(GG*LL*cc**2/(8*math.pi*GG))
Hnum = cc*math.sqrt(LL/3)
print("a0(k=1/2) num = %.10e   a0_num/a0_can = %.6f" % (a0num, a0num/9.36e-11))
print("H_L num = %.10e   a0/(cH) = %.10f" % (Hnum, a0num/(cc*Hnum)))

# ---------- R2 ----------
y = sp.symbols('y', positive=True)
# canonical: g_N = g^2/(g+a0)  -> g = (gN + sqrt(gN^2+4 gN a0))/2
gc = (y + sp.sqrt(y**2 + 4*y))/2          # in units a0, y = gN/a0
ga = sp.sqrt(y**2 + y)
print("\n[canonical] g/a0 =", sp.simplify(gc))
print("[alt] g/a0 =", sp.simplify(ga))
print("canonical strong field: g-gN (units a0) ->", sp.limit(gc-y, y, sp.oo))
print("alt strong field: g-gN (units a0) ->", sp.limit(ga-y, y, sp.oo))
print("canonical series nu-1:", sp.series(gc/y-1, y, sp.oo, 5))
print("alt series nu-1:", sp.series(ga/y-1, y, sp.oo, 5))

f = sp.simplify((gc-ga)/gc)
print("frac diff f =", f)
df = sp.simplify(sp.diff(f, y))
print("df/dy =", df)
crit = sp.solve(sp.together(sp.numer(sp.together(df))), y)
print("critical points:", crit)
for cnd in crit:
    print("   y=", cnd, " f=", sp.nsimplify(f.subs(y,cnd)), float(f.subs(y,cnd)))
print("f at y=1/2:", sp.nsimplify(f.subs(y, sp.Rational(1,2))), float(f.subs(y,sp.Rational(1,2))))
print("limits: f(0+)=", sp.limit(f,y,0,'+'), " f(inf)=", sp.limit(f,y,sp.oo))
print("sqrt3/2 =", float(sp.sqrt(3)/2), " 1-sqrt3/2 =", float(1-sp.sqrt(3)/2))
print("relative to g_alt:", float((1-sp.sqrt(3)/2)/(sp.sqrt(3)/2)*100), "% ; relative to gN: ", float((1-sp.sqrt(3)/2)/sp.Rational(1,2)*100),"%")
# also diff defined other ways
print("alt-crit by numeric scan:")
import numpy as np
yy=np.logspace(-4,4,200001)
gyc=(yy+np.sqrt(yy**2+4*yy))/2; gya=np.sqrt(yy**2+yy)
ff=(gyc-gya)/gyc
i=np.argmax(ff); print("  max %.8f at y=%.6f" % (ff[i], yy[i]))
