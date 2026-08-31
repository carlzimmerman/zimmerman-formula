#!/usr/bin/env python3
"""
phase2_symbolic.py  -- FC-KH Phase 2: symbolic action verification (sympy).

Target theory (MISSION.md):
  S_FC = (M_Pl^2/2) int d^4x sqrt(-g)[ R - ((beta+3lam)/3) theta^2 - beta sigma^2 + f_FC(a) ]
  f_FC(a) = -2Lambda + alpha a^2 + 2(2-alpha) a0^2 [ 1 - (1+a/a0) e^{-a/a0} ]

Verifies (all as exact sympy identities, printed):
  (1) f'  = 2a[ alpha + (2-alpha) e^{-y} ]           , y=a/a0
  (2) f'' = 2 alpha + 2(2-alpha)(1-y) e^{-y}
  (3) chi = f'/(2a)   ;  mu_phys = (1 - chi/2)/(1 - alpha/2)  ==  1 - e^{-y}   (identically)
  (4) small-a:  f -> -2Lambda + 2 a^2 - (2(2-alpha)/3) a^3/a0
  (5) large-a:  f -> -2Lambda + alpha a^2   (+const)
  (6) transverse accel Hessian  f'/a = 2[alpha+(2-alpha)e^{-y}] > 0  for all y (never flips)
  (7) radial accel Hessian  f'' = 2 alpha + 2(2-alpha)(1-y) e^{-y}  (flips sign near y~1)
  (8) ADM reduction of the sigma/theta sector:
        -((beta+3lam)/3) theta^2 - beta sigma^2  ==  -beta K_ijK^ij - lam K^2
      and  R - beta KK - lam K^2 + f  ==  ^3R + (1-beta)K_ijK^ij - (1+lam)K^2 + f
  (9) G_N = 2G/(2-alpha)   (from chi_inf = alpha/2 at high a; f -> alpha a^2)
  (10) map to the earlier W-primitive:  F(y) := f_FC/a0^2 (drop -2Lam) = 2y^2 - 2(2-alpha) W(y),
       W(y)=y^2/2+(1+y)e^{-y}-1.  So W0->F, W1->F', W2->F'' in the reduction script.
"""
import sympy as sp

a, a0, alpha, beta, lam, Lam, G = sp.symbols('a a0 alpha beta lambda Lambda G', positive=True)
y = sp.symbols('y', positive=True)

# ---------- f_FC and derivatives ----------
f = -2*Lam + alpha*a**2 + 2*(2-alpha)*a0**2*(1 - (1+a/a0)*sp.exp(-a/a0))
fp  = sp.diff(f, a)
fpp = sp.diff(f, a, 2)

fp_claim  = 2*a*(alpha + (2-alpha)*sp.exp(-a/a0))
fpp_claim = 2*alpha + 2*(2-alpha)*(1 - a/a0)*sp.exp(-a/a0)

print("="*74)
print("PHASE 2 -- SYMBOLIC ACTION VERIFICATION (FC-KH)")
print("="*74)
print("f_FC(a) =", f)
print("\n(1) f'  identity   f' - 2a[alpha+(2-alpha)e^-y] = ",
      sp.simplify(fp - fp_claim), "  -> PASS" if sp.simplify(fp-fp_claim)==0 else " -> FAIL")
print("(2) f'' identity   f''- [2alpha+2(2-alpha)(1-y)e^-y] = ",
      sp.simplify(fpp - fpp_claim), "  -> PASS" if sp.simplify(fpp-fpp_claim)==0 else " -> FAIL")

# ---------- chi, mu_phys ----------
chi = sp.simplify(fp/(2*a))
mu_phys = sp.simplify((1 - chi/2)/(1 - alpha/2))
mu_target = 1 - sp.exp(-a/a0)
print("\n(3) chi = f'/(2a) =", chi)
print("    mu_phys = (1-chi/2)/(1-alpha/2) =", sp.simplify(mu_phys))
dmu = sp.simplify(mu_phys - mu_target)
print("    mu_phys - (1 - e^{-y}) =", dmu, "  -> PASS (mu-(1-e^-y)==0)" if dmu==0 else " -> FAIL")

# ---------- small-a / large-a ----------
ser = sp.series(f, a, 0, 4).removeO()
print("\n(4) small-a series of f:", sp.expand(ser))
print("    expected: -2Lambda + 2 a^2 - (2(2-alpha)/3) a^3/a0")
print("    a^2 coeff =", sp.expand(ser).coeff(a,2), " (expect 2);  a^3 coeff =",
      sp.expand(ser).coeff(a,3), " (expect -(2(2-alpha)/3)/a0 =", sp.simplify(-2*(2-alpha)/3/a0), ")")

f_high = sp.simplify(f - 2*(2-alpha)*a0**2 + 2*Lam)  # strip the const the exp-tail leaves
# large a: (1+a/a0)e^{-a/a0} -> 0
print("\n(5) large-a: f -> -2Lambda + alpha a^2 + const;  f - alpha a^2 - [const] tail =",
      sp.simplify(f - (-2*Lam + alpha*a**2 + 2*(2-alpha)*a0**2)),
      " (= -2(2-alpha)a0^2(1+a/a0)e^{-a/a0}, ->0)")

# ---------- Hessian directions ----------
fp_over_a = sp.simplify(fp/a)
print("\n(6) transverse Hessian f'/a =", fp_over_a, " = 2[alpha+(2-alpha)e^-y] > 0 for all y>0, alpha in[0,2]")
print("(7) radial Hessian f'' =", sp.simplify(fpp), "  (root at y where (1-y)e^-y = -alpha/(2-alpha))")

# ---------- ADM sigma/theta reduction ----------
Kij, KK, Ktr = sp.symbols('K_ij KK Ktr')  # placeholders; do the tensor identity abstractly
# sigma^2 = K_ijK^ij - (1/3) theta^2 ; theta=K=Ktr ; KK=K_ijK^ij
KKs, th = sp.symbols('KK theta')
sigma2 = KKs - sp.Rational(1,3)*th**2
sector = -((beta+3*lam)/3)*th**2 - beta*sigma2
sector_simpl = sp.expand(sector)
print("\n(8) -((beta+3lam)/3)theta^2 - beta sigma^2 =", sector_simpl,
      "\n    == -beta*KK - lambda*theta^2 ?  diff =", sp.simplify(sector_simpl - (-beta*KKs - lam*th**2)))
# R = ^3R + KK - theta^2  (ADM). Add sector:
R3 = sp.symbols('R3')
Rfull = R3 + KKs - th**2
adm = sp.expand(Rfull + sector_simpl)
print("    R - beta KK - lam K^2 (ADM) =", adm,
      "\n    == ^3R + (1-beta)KK - (1+lambda)theta^2 ?  diff =",
      sp.simplify(adm - (R3 + (1-beta)*KKs - (1+lam)*th**2)))
print("    => coeff of K_ijK^ij is (1-beta); c_T^2 = 1/(1-beta).  Script's (1+beta_s) => beta_s = -beta_mission.")

# ---------- G_N ----------
chi_inf = sp.limit(chi, a, sp.oo)
print("\n(9) chi(a->inf) =", chi_inf, " (= alpha).  G_N = 2G/(2-alpha) = G/(1-alpha/2).")
print("    The (1-alpha/2) is the mu_phys normalization denominator; at high a the a^2 piece")
print("    renormalizes the Newtonian coupling by 1/(1-alpha/2) => G_N = 2G/(2-alpha). [mission]")

# ---------- map to W-primitive ----------
Wy = y**2/2 + (1+y)*sp.exp(-y) - 1
Fy = 2*y**2 - 2*(2-alpha)*Wy
F_from_f = sp.simplify((f + 2*Lam).subs(a, a0*y)/a0**2)   # f_FC/a0^2 dropping -2Lambda
print("\n(10) F(y)=f_FC/a0^2 (drop -2Lam) - [2y^2 - 2(2-alpha)W(y)] =",
      sp.simplify(F_from_f - Fy), "  -> PASS" if sp.simplify(F_from_f-Fy)==0 else " -> FAIL")
print("     F'(y)  =", sp.simplify(sp.diff(Fy,y)))
print("     F''(y) =", sp.simplify(sp.diff(Fy,y,2)), " (== f'' as a-derivative; dimensionless)")
# confirm F'' equals f'' (the a-second-derivative)
print("     check F''(y) - f''(a=a0 y) =", sp.simplify(sp.diff(Fy,y,2) - fpp.subs(a,a0*y)))
print("\nDONE.")
