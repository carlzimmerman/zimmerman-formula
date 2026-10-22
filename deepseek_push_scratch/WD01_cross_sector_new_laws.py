#!/usr/bin/env python3
"""WD01 -- NEW exact cross-sector consequences. Clean symbolic verification."""
import sympy as sp
import math

cs = 2.99792458e8; pc = 3.08567758e16; Mpc = 3.08567758e22
Msun = 1.989e30; Gv = 6.67430e-11

a0, G, Mb, R, R500, rM, f, M500, sigma = sp.symbols(
    'a0 G Mb R R500 rM f M500 sigma', positive=True)

def check(name, lhs, rhs):
    d = sp.simplify(sp.nsimplify(sp.simplify(lhs) - sp.simplify(rhs)))
    ok = d == 0
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}   residual = {d}")
    return ok

# --- framework primitives -------------------------------------------------
# a0-line phantom: g_phi = a0(sqrt(x^2+x) - x);  x = g_b/a0 = (rM/R)^2 ; Mb = a0 rM^2/G
x = (rM/R)**2
gphi = a0*(sp.sqrt(x**2 + x) - x)
Mdyn = Mb + R**2*gphi/G
# exact ceiling (ZD01, re-stated): g_phi <= a0/2  <=>  (x+1/2)^2 - (x^2+x) = 1/4
check("P0 ceiling: (x+1/2)^2-(x^2+x) = 1/4  => g_phi <= a0/2",
      sp.expand((x+sp.Rational(1,2))**2 - (x**2+x)), sp.Rational(1,4))

# virial identification used below: G*M500 = a0*rM*R500*sqrt(1+rM^2/R500^2)
RM500 = a0*rM*R500*sp.sqrt(1+rM**2/R500**2)
# surd identity helper (sqrt(1+y)*sqrt(y)=sqrt(y+y^2) denesting)
def sden(e):
    return sp.simplify(sp.powsimp(sp.expand(e), force=True, deep=True))

# --- C1: exact virial web -------------------------------------------------
print("C1 -- EXACT VIRIAL WEB (a0-line + virial + stripping)")
s2v = sp.simplify((G*Mdyn/R).subs(Mb, a0*rM**2/G))            # virial conv, no half
s2i = sp.simplify((G*Mdyn/(2*R)).subs(Mb, a0*rM**2/G))        # isothermal conv
check("C1a sigma^2_vir = a0*rM*sqrt(1+rM^2/R^2)", s2v, a0*rM*sp.sqrt(1+rM**2/R**2))
check("C1b sigma^2_iso = (a0*rM/2)*sqrt(1+rM^2/R^2)", s2i, a0*rM/2*sp.sqrt(1+rM**2/R**2))
check("C1c sigma^4_iso = (a0*G*Mb/4)(1+rM^2/R^2)",
      sp.simplify(s2i**2 - a0*G*(a0*rM**2/G)/4*(1+rM**2/R**2)), 0)
check("C1d sigma^4_vir = a0*G*Mb*(1+rM^2/R^2)",
      sp.simplify(s2v**2 - a0*G*(a0*rM**2/G)*(1+rM**2/R**2)), 0)
fexpr = sp.simplify((Mdyn/Mb).subs(Mb, a0*rM**2/G))
check("C1e f := M_dyn/M_b = sqrt(1+(R/rM)^2)", fexpr, sp.sqrt(1+(R/rM)**2))
check("C1e' at R500: rM/R500 = 1/sqrt(f^2-1)",
      sden(fexpr.subs(R, R500).subs(rM, R500/sp.sqrt(f**2-1)) - f), 0)
rstrip = sp.simplify((4*s2v/a0).subs(R, R500))
check("C1g r_strip = 4*rM*sqrt(1+rM^2/R500^2)", rstrip, 4*rM*sp.sqrt(1+rM**2/R500**2))
rstrip_f = sp.simplify((rstrip/R500).subs(R500, rM*sp.sqrt(f**2-1)))
check("C1h r_strip/R500 = 4f/(f^2-1) (pure function of baryon-content f)",
      rstrip_f, 4*f/(f**2-1))
check("C1i r_strip/R500 = 4f/(f^2-1) [surd-denst form, force]",
      sden(rstrip_f - 4*f/(f**2-1)), 0)
rq = 4*f*R500/(f**2-1)   # equivalent root form
quad = sp.simplify(rq**2 - 4*rM**2/(f*R500)*rq - 16*rM**2).subs(R500, rM*sp.sqrt(f**2-1))
check("C1j quadratic: r_strip solves r^2-(4 rM^2/(fR500))r-16rM^2=0", quad, 0)
# local log-slope of T_obs/T_pred = 2 f(r) (rM/r)
u = rM/R
ratio = 2*sp.sqrt(1+u**2)*u
slope = sp.simplify(R*sp.diff(sp.log(ratio), R))
check("C1k slope = -(1+2u^2)/(1+u^2)", slope, -(1+2*u**2)/(1+u**2))
print(f"        slope@r=rM = {slope.subs(R,rM)} ; slope@r=2rM = {sp.nsimplify(slope.subs(R,2*rM))}; "
      f"single-scale range [-3/2,-1] for r>=rM")

# --- C2: saturated phantom gain = envelope at r_strip ----------------------
print("C2 -- SATURATED PHANTOM GAIN = ENVELOPE AT r_strip")
Msat = sp.simplify(a0*rstrip**2/(2*G))
M500_id = RM500/G    # G*M500 = a0*rM*R500*sqrt(1+rM^2/R500^2)  =>  M500 = ...
check("C2a M_phi,sat = 8*G*M500^2/(a0*R500^2)",
      sp.simplify(Msat.subs(rstrip, 4*G*M500/(a0*R500)).subs(M500, M500_id)),
      8*G*M500_id**2/(a0*R500**2))
check("C2b M_phi,sat = 8*sigma^4/(G a0) with sigma^2 = G M500/R500",
      sp.simplify(Msat.subs(rstrip, 4*G*M500/(a0*R500)).subs(M500, M500_id)),
      8*(G*M500_id/R500)**2/(G*a0))
check("C2c M_phi,sat = 8*Mb*f^2/(f^2-1)",
      sp.simplify(Msat.subs(rstrip, 4*G*M500/(a0*R500)).subs(M500, f*a0*rM**2/G)
                  .subs(R500, rM*sp.sqrt(f**2-1))),
      8*(a0*rM**2/G)*f**2/(f**2-1))
check("C2d M_phi,sat = (8f/(f^2-1))*M500 (f-units corollary)",
      sp.simplify(Msat.subs(rstrip, 4*G*M500/(a0*R500)).subs(M500, f*a0*rM**2/G)
                  .subs(R500, rM*sp.sqrt(f**2-1))),
      8*f*(f*a0*rM**2/G)/(f**2-1))

# --- C3: wedge arithmetic (exact rationals) --------------------------------
print("C3 -- WEDGE ARITHMETIC")
a0L = sp.Rational(12, 10**11)      # 1.2e-10 exactly
astar = sp.Rational(64, 10**12)    # 6.4e-11 exactly
check("C3a a0* = (8/15) a0_L", astar, sp.Rational(8,15)*a0L)
check("C3b a0* = (16/15)(a0_L/2)  cap overshoot", astar, sp.Rational(16,15)*a0L/2)
check("C3c a0_c = a0*^2/a0_L = (64/225) a0_L", astar**2/a0L, sp.Rational(64,225)*a0L)
check("C3d equal log spacing a0_L/a0* = a0*/a0_c = 15/8", a0L/astar, sp.Rational(15,8))
check("C3e (a0* - a0_L/2) = a0_L/30", astar - a0L/2, a0L/30)

# --- the a0-H0-Omega_L anchor (kappa = 1/2 DE identity), numeric verification
print("C3 -- the a0-H0-Omega_L anchor")
for a0n, Hkm in [(9.3619e-11, 67.36), (9.3619e-11, 67.4), (1.2e-10, 67.4), (1.1279e-10, 67.4)]:
    Om = 32*math.pi*a0n**2/(3*(Hkm*1e3/Mpc)**2*cs**2)
    print(f"  Omega_L(32pi a0^2/3H0^2c^2) a0={a0n:.4e}, H0={Hkm}: {Om:.4f} vs shipped 0.6857 "
          f"(residual {(Om-0.6857)/0.6857*100:+.2f}%)")
a0k = 0.5*cs*(67.4e3/Mpc)*math.sqrt(3*0.6857/(8*math.pi))
print(f"  inverse anchor: a0 = (c/2)H0*sqrt(3 Omega_L/8pi) = {a0k:.4e} (canonical 9.3619e-11, "
      f"residual {(a0k-9.3619e-11)/9.3619e-11*100:+.3f}%)")

# NUMERICS: shipped numbers vs the new exact laws
print("NUMERICS -- shipped constants vs new laws")
A0 = 1.2e-10
for a0n, tag in [(9.3619e-11,'canonical a0'), (1.2e-10,'task a0=1.2e-10')]:
    rhoDE = 4*a0n**2/(Gv*cs**2)
    H0_imp = math.sqrt(32*math.pi*a0n**2/(3*cs**2*0.6857))   # s^-1
    print(f"  Omega_L({tag}) at H0=67.4: {rhoDE/(3*(67.4e3/Mpc)**2/(8*math.pi*Gv)):.4f} "
          f"(shipped 0.6857); H0 implied = {H0_imp*Mpc/1e3:.2f} km/s/Mpc")
print(f"  z* = (1-0.6857)^(-1/3)-1 = {(1-0.6857)**(-1/3)-1:.4f} (shipped ~0.49; 4% off => z* is not the exact Lambda-matter equality)")
astar, a0L_ = 6.4e-11, 1.2e-10
print(f"  a0*/a0_L = {astar/a0L_:.5f} = 8/15 = {8/15:.5f}; a0_c = a0*^2/a0_L = {astar**2/a0L_:.4e} "
      f"(vs (64/225)a0_L = {(64/225)*a0L_:.4e}); a0*/(a0_L/2) = {astar/(a0L_/2):.5f} = 16/15")
Omstar = 32*math.pi*astar**2/(3*(67.4e3/Mpc)**2*cs**2)
print(f"  Omega(a0*) = 32pi a0*^2/(3H0^2 c^2) = {Omstar:.4f} vs Omega_m = {1-0.6857:.4f} "
      f"({Omstar/(1-0.6857)*100-100:+.1f}% -- near-miss, EXCLUDED as numerology)")
# G008
sig, R500g = 809e3, 1.38*Mpc
rsG = 4*sig**2/A0; M500g = sig**2*R500g/Gv
print(f"  G008: r_strip = {rsG/Mpc:.3f} Mpc ({rsG/R500g:.3f} R500); M500 = {M500g/Msun/1e14:.2f}e14 Msun")
MsatG = 8*Gv*M500g**2/(A0*R500g**2)
print(f"  M_phi,sat(G008) = 8G M500^2/(a0 R500^2) = {MsatG/Msun/1e14:.2f}e14 Msun = a0 r_strip^2/2G "
      f"({A0*rsG**2/(2*Gv)/Msun/1e14:.2f}) -- INSIDE shipped pie band 2-3e14 Msun")
freg = 5.66
print(f"  shipped f=5.66 -> r_strip/R500 = 4f/(f^2-1) = {4*freg/(freg**2-1):.3f} vs shipped census 1.46-2.05  [TENSION]")
for rv in (2.05, 1.46):
    fv = (4/rv + math.sqrt(16/rv**2+4))/2
    print(f"    census r_strip/R500 = {rv} requires f = {fv:.3f}")
print(f"  T-ratio 3.57 at R500 needs r_M/R500 = 3.57/(2*5.66) = {3.57/(2*5.66):.3f} "
      f"vs exact 1/sqrt(f^2-1) = {1/math.sqrt(freg**2-1):.3f} -> T aperture r = {1/math.sqrt(freg**2-1)/(3.57/(2*5.66)):.2f} R500")
print(f"  M_phi,sat in M500 units = 8f/(f^2-1) = {8*freg/(freg**2-1):.3f} -> {8*freg/(freg**2-1)*M500g/Msun/1e14:.2f}e14 Msun")
# triad floor check (isothermal sigma^4 = a0 G Mb/4), galaxy triad
Mb_g = 7.0e10*Msun
for a0n, tag in [(9.3619e-11, 'canonical'), (1.2e-10, 'task a0')]:
    s4 = (a0n*Gv*Mb_g)**0.25/math.sqrt(2)/1e3
    print(f"  deep-MOND floor sigma = (a0 G Mb)^(1/4)/sqrt(2) ({tag}) = {s4:.1f} km/s "
          f"(shipped triad 119.2 km/s @7e10 Msun)")
print("\nDONE.")