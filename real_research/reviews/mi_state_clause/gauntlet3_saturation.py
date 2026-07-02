#!/usr/bin/env python3
"""
GAUNTLET ITEM 3 -- SATURATION SHAPE: does gain saturation deliver mu(a/a0), or just
SOME saturating function with a free scale?

Target (framework's own interpolation): m_eff/m = sqrt(g/(g+a0)) = (1+a0/g)^(-1/2).
  - identity checks: equals the mu_fw form; deep-MOND m_eff/m -> (g/a0)^(1/2); Newtonian
    tail delta_m/m -> -a0/(2g)  [exponents 1/2 and -1].
Standard saturable-gain shapes (laser physics, Siegman ch.7/30; two-level Bloch):
  - homogeneous:    delta_m/m = -c/(1+s),      s = (g/g_s)^2 (intensity-like variable)
  - inhomogeneous:  delta_m/m = -c/sqrt(1+s),  s = (g/g_s)^2
Computed verdicts:
  S1: homogeneous: deep-MOND floor m_eff/m -> 1-c (needs c=1 EXACT to reach 0); with c=1
      the deep-MOND exponent is 2 (vs target 1/2) and the Newtonian tail is g^-2 (vs g^-1).
  S2: inhomogeneous: Newtonian tail g^-1 CAN match (c*g_s = a0/2) but deep-MOND exponent
      is 2 with c=1 (vs 1/2) and a floor 1-c for c<1. FAILS the deep-MOND limit either way.
  S3: solving for the saturation variable the target REQUIRES: s_req(g) ~ sqrt(g/a0) as
      g->0 and ~ 2g/a0 as g->infinity -- i.e. saturation LINEAR (not quadratic) in
      amplitude at high g and SQUARE-ROOT at low g. No standard gain nonlinearity does
      this; it must be designed by hand = the mu shape is INSERTED, not derived.
  S4: c=1 is a fine-tuning: the pump-supplied gain must cancel 100.000...% of the bare
      inertia in the g->0 limit for EVERY body (also an EP/universality condition:
      delta_m must be proportional to m exactly).
  S5: the scale: g_s = I_sat-derived = combination of pump rate / linewidth / dipole --
      free parameters of the medium; nothing forces g_s ~ a0 = cH_L/Z. The only
      horizon-derivable frequency is ~H_L itself (x700 below band). a0 NOT delivered.
Exit 0 = all assertions hold.
"""
import sympy as sp

ok = []
g, a0, gs, cpar, s = sp.symbols('g a_0 g_s c s', positive=True)

# --- target identities
target = (1 + a0/g)**(-sp.Rational(1, 2))
assert sp.simplify(target - sp.sqrt(g/(g + a0))) == 0
# mu_fw consistency: g_obs = sqrt(g^2+g*a0); with x = g_obs/a0, mu(x) = (sqrt(1+4x^2)-1)/(2x)
# must satisfy mu(x)*g_obs = g  (F = m mu(a/a0) a with a = g_obs).
g_obs = sp.sqrt(g**2 + g*a0)
x = g_obs/a0
# sqrt(1+4x^2) = (2g+a0)/a0 (both sides positive; proven by squaring):
assert sp.simplify(sp.expand((1 + 4*x**2) - ((2*g + a0)/a0)**2)) == 0
mu_fw_closed = ((2*g + a0)/a0 - 1)/(2*x)          # = mu_fw with the radical resolved
assert sp.simplify(mu_fw_closed*g_obs - g) == 0
assert sp.simplify(g/g_obs - target) == 0
# numeric spot-check of the unresolved radical form too:
mu_fw = (sp.sqrt(1 + 4*x**2) - 1)/(2*x)
assert abs(float((mu_fw*g_obs - g).subs({g: 3, a0: 7}))) < 1e-25
# limits/exponents of the target
deep = sp.limit(target/sp.sqrt(g/a0), g, 0)
assert deep == 1                                   # m_eff/m -> (g/a0)^{1/2}
tail = sp.series(target, a0, 0, 2).removeO() - 1   # -> -a0/(2g)
assert sp.simplify(tail + a0/(2*g)) == 0
ok.append("T: target m_eff/m = sqrt(g/(g+a0)) == mu_fw identity verified; deep-MOND exponent "
          "1/2 (m_eff/m -> sqrt(g/a0)), Newtonian tail delta_m/m = -a0/(2g) (power g^-1)")

# --- S1 homogeneous saturation, s = (g/gs)^2
hom = 1 - cpar/(1 + (g/gs)**2)
floor = sp.limit(hom, g, 0)
assert sp.simplify(floor - (1 - cpar)) == 0        # floor 1-c > 0 unless c=1 exactly
hom1 = hom.subs(cpar, 1)
lead = sp.limit(hom1/(g/gs)**2, g, 0)
assert lead == 1                                   # deep-MOND exponent 2, not 1/2
tail_h = sp.series(hom1.subs(g, 1/sp.Symbol('u', positive=True)), sp.Symbol('u', positive=True), 0, 3)
# Newtonian tail: 1 - gs^2/g^2 + ... -> delta ~ g^-2, not g^-1
tail_pow = sp.limit((1 - hom1)*g**2, g, sp.oo)
assert sp.simplify(tail_pow - gs**2) == 0
ok.append("S1: homogeneous 1-c/(1+(g/gs)^2): floor 1-c at g->0 (c=1 tuning needed); with c=1 "
          "deep-MOND exponent 2 (target 1/2) and Newtonian tail g^-2 (target g^-1): FAILS both ends")

# --- S2 inhomogeneous saturation, 1/sqrt(1+s)
inh = 1 - cpar/sp.sqrt(1 + (g/gs)**2)
tail_i = sp.limit((1 - inh)*g, g, sp.oo)
assert sp.simplify(tail_i - cpar*gs) == 0          # g^-1 tail: can match a0/2 = c*gs
inh1 = inh.subs(cpar, 1)
lead_i = sp.limit(inh1/(g/gs)**2, g, 0)
assert sp.simplify(lead_i - sp.Rational(1, 2)) == 0  # deep-MOND exponent 2 again
ok.append("S2: inhomogeneous 1-c/sqrt(1+(g/gs)^2): Newtonian tail -c*gs/g CAN match -a0/(2g) "
          "(one condition c*gs=a0/2), but deep-MOND exponent is 2 (target 1/2) and any c<1 "
          "leaves a floor: FAILS the deep-MOND limit -- the RAR's low-g half is unreproduced")

# --- S3 the saturation variable the target would REQUIRE (homogeneous form, c=1)
# 1 - 1/(1+s_req) = (1+a0/g)^(-1/2)  =>  s_req = target/(1-target)
s_req = sp.simplify(target/(1 - target))
lo = sp.limit(s_req/sp.sqrt(g/a0), g, 0)
hi = sp.limit(s_req/g, g, sp.oo)
assert lo == 1                                     # s_req ~ sqrt(g/a0) at low g
assert sp.simplify(hi - 2/a0) == 0                 # s_req ~ 2g/a0 at high g
ok.append("S3: required saturation variable s_req(g) = target/(1-target): ~sqrt(g/a0) (g->0), "
          "~2g/a0 (g->inf) -- LINEAR-to-SQRT in amplitude, whereas physical gain saturation is "
          "QUADRATIC (intensity) in amplitude: the mu shape must be inserted by hand")

# --- S4 the c=1 tuning, stated as an equation the pump must satisfy identically
# delta_m(g->0) = -m exactly, i.e. gain cancels 100% of bare inertia for every worldline mass:
# c == lam^2 * |chi_bath(0)| / m == 1 for all m -> coupling^2 must scale EXACTLY like m.
ok.append("S4: reaching m_eff->0 needs c = lam^2|chi_B(0)|/m = 1 IDENTICALLY (every body, "
          "every composition): a 100%-cancellation fine-tuning + an EP condition (delta_m "
          "strictly proportional to m) that nothing in the pump construction enforces")

# --- S5 the scale is I_sat = free; dimensional statement
# two-level: s = a_orb^2/a_sat^2 with a_sat^2 ~ (hbar w0/d)^2 * gamma1*gamma2 / (coupling...)
# every factor is a property of the MEDIUM (pump rate, linewidth, dipole), none is cH_L/Z.
ok.append("S5: g_s = I_sat-derived: g_s^2 ~ gamma_1*gamma_2*(w0/lam b)^2-type medium constants "
          "(pump rate, linewidth, dipole) -- a FREE scale; the only horizon-derivable frequency "
          "is ~H_L (x700 below band, gauntlet2b) so a0 = cH_L/Z is NOT delivered. The honest "
          "default holds: saturation gives SOME saturating function with a free scale.")

print("ALL ASSERTIONS PASSED (gauntlet 3)")
for line in ok:
    print(" *", line)
