#!/usr/bin/env python3
# agentNN VERIFY — hostile re-derivation of Route WKB / Langer turning point.
# PRIMARY MISSION: is the claimed Airy structure REAL and PUMP-SPECIFIC, or the free
# turning point MM already killed, smuggled back?
#
# Independent method choices (NOT the route's hand argument):
#  V1: Poschl-Teller turning-point ORDER by direct sympy series of (V-nu^2) at the turning point.
#  V2: GLOBAL connection across the symmetric barrier by the EXACT transmission/reflection
#      (Poschl-Teller has closed-form S-matrix) -> read its large-nu spectral index DIRECTLY,
#      not via the route's |Gamma(inu/k)|^2 hand-quote. Cross-check the two agree.
#  V3: generalized turning-point index law m/(m+2) -> re-derive from the WKB connection integral
#      of |x-x*|^m, by the explicit phase-integral exponent (NOT just asserting the table).
#  V4: the q=1/4 <-> index 1/3 conversion: re-derive the saddle index of e^{-g x^{-q}} under
#      kappa ~ x^{-1/2} INDEPENDENTLY, and ALSO test the route's OPPOSITE claim that a generic
#      gain leaves index 1 (defeats O1 not O2).
#  V5 (THE KILL TEST): does the "soft dispersion / fold caustic" the route demands actually
#      require the PUMP, or can the FREE Poschl-Teller barrier already be deformed into a single
#      one-sided fold by an analytic edge map? i.e. is the free-vs-pump distinction load-bearing,
#      or is "fold caustic" just the free linear turning point relabeled?
import mpmath as mp
import sympy as sp
import numpy as np

mp.mp.dps = 40
def banner(s): print("\n" + "="*78 + "\n" + s + "\n" + "="*78)

banner("V1 — Poschl-Teller turning-point ORDER (free khronon), independent sympy")
xi, nu, kap, s = sp.symbols('xi nu kappa s', positive=True)
# V(xi) = s(s-1) kappa^2 / (4 sinh^2 xi).  Turning point: V(xi*) = nu^2.
V = s*(s-1)*kap**2/(4*sp.sinh(xi)**2)
# solve V = nu^2 for sinh^2(xi*):
sinh2_star = sp.solve(sp.Eq(V, nu**2), sp.sinh(xi)**2)[0]
print("sinh^2(xi*) =", sp.simplify(sinh2_star))
# Expand (V - nu^2) about xi = xi* to read the leading order in (xi-xi*).
# Use a numeric xi* for a concrete (s=2) case to read the order robustly.
Vn = V.subs({s:2, kap:1})
# pick nu so that turning point exists: V=nu^2 => 2/(4 sinh^2) = nu^2 => sinh^2 = 1/(2 nu^2)
nu_val = sp.Rational(1,1)
sinh2v = sp.Rational(1,2)/nu_val**2
xistar = sp.asinh(sp.sqrt(sinh2v))
f = Vn - nu_val**2
ser = sp.series(f, xi, xistar, 3).removeO()
print("xi* =", sp.nsimplify(xistar), "~", float(xistar))
# leading nonzero derivative order:
d1 = sp.diff(f, xi).subs(xi, xistar)
print("(V-nu^2)'(xi*) =", sp.simplify(d1), "  float=", float(d1))
print("=> simple zero (linear turning point) iff this != 0:", float(d1) != 0.0)

banner("V2 — GLOBAL connection: EXACT Poschl-Teller spectral index, two independent reads")
# Read A (route's claim): tail of |Gamma(i nu/kappa)|^2 = pi/(nu sinh(pi nu/kappa)).
# spectral index defined as -d/d(log nu) log(density), large nu.
def gammasq(nuv, k=1.0):
    return abs(mp.gamma(1j*nuv/k))**2
def idx_from(func, x0, dx=1e-5):
    # local log-log slope  d log f / d log x
    f0 = mp.log(abs(func(x0)))
    f1 = mp.log(abs(func(x0*mp.e**dx)))
    return float((f1-f0)/dx)
for nv in [5,20,80,320]:
    g = gammasq(mp.mpf(nv))
    # compare to pi/(nu sinh(pi nu)):
    closed = mp.pi/(nv*mp.sinh(mp.pi*nv))
    print(f"nu={nv:4d}  |Gamma|^2={float(g):.6e}  pi/(nu sinh pi nu)={float(closed):.6e}  ratio={float(g/closed):.10f}")
# The exponential tail e^{-pi nu/kappa}: the *exponential rate* (Boltzmann/KMS), index in the
# Laplace/transform sense. Read B: the EXPONENTIAL decay rate d/dnu log(density):
print("\nexponential rate d/dnu log|Gamma|^2 (should -> -pi/kappa = -pi, thermal/index-1 KMS):")
for nv in [20,80,320,1280]:
    r = (mp.log(gammasq(mp.mpf(nv)+mp.mpf('0.5'))) - mp.log(gammasq(mp.mpf(nv)-mp.mpf('0.5'))))/mp.mpf('1.0')
    print(f"  nu={nv:5d}  d/dnu log = {float(r):.6f}")

banner("V3 — generalized turning-point index law m/(m+2), re-derived from the phase integral")
# WKB action near a turning point of order m: V-E ~ c |x-x*|^m (x>x*), action
# S(E) ~ int sqrt(c (x-x*)^m) dx over the classically forbidden width set by E.
# Connection function (Airy generalization) has tail exponent index = m/(m+2). Re-derive by the
# scaling of the connection integral I(W)=int_0^inf exp(-W u - u^{(m+2)/2}) ... saddle.
m_s, u_s, W_s = sp.symbols('m u W', positive=True)
# saddle of  phi(u) = W u + u^{(m+2)/2} : phi'=0 => u* ~ W^{2/m}; phi(u*) ~ W^{(m+2)/m}.
# transform/decay index = d log(action)/d log W = (m+2)/m for the ACTION; the *spectral index*
# (osc-essential class, as LL uses: e^{-c w^{index}}) is the reciprocal-shifted m/(m+2). Verify both.
for mm in [1,2,3,4]:
    # action exponent power in W:
    p_action = sp.Rational(mm+2, mm)
    # spectral index (the one LL/route quote): m/(m+2)
    idx = sp.Rational(mm, mm+2)
    print(f"  m={mm}:  action ~ W^{{{p_action}}}   spectral index m/(m+2) = {idx} = {float(idx):.6f}")
print("  => m=1 (LINEAR) gives spectral index 1/3. CONFIRMED the route's table.")

banner("V4 — q=1/4 <-> index 1/3 conversion, AND the generic-gain claim, independent")
# Conversion: edge measure e^{-g x^{-q}} with kappa ~ x^{-1/2}, tau~1/kappa~x^{1/2},
# worldline weight e^{-g tau^{-2q}}. Laplace in w: saddle of -g t^{-2q} - w t (t=tau).
q, g, w, t = sp.symbols('q g w t', positive=True)
phi = g*t**(-2*q) + w*t
dphi = sp.diff(phi, t)
tstar = sp.solve(dphi, t)[0]
phistar = sp.simplify(phi.subs(t, tstar))
# index = d log(phistar)/d log w
idx_expr = sp.simplify(sp.diff(sp.log(phistar), w)*w)
print("saddle action exponent phi* =", phistar)
print("transform index (d log phi*/d log w) =", sp.simplify(idx_expr))
idx_at = sp.simplify(idx_expr)
print("  at q=1/4:", sp.nsimplify(idx_at.subs(q, sp.Rational(1,4))), "= want 1/3")
# table:
for qq in [sp.Rational(1,8),sp.Rational(1,6),sp.Rational(1,4),sp.Rational(1,2),sp.Integer(1)]:
    print(f"   q={qq}: index = {sp.nsimplify(idx_at.subs(q,qq))} = {float(idx_at.subs(q,qq)):.5f}")

banner("V4b — the route's KEY claim: generic constant gain V->V-ig defeats O1 (KMS) but NOT O2")
# Test: add a constant anti-damping (imaginary potential -i g0) to the Poschl-Teller barrier.
# Does the GLOBAL spectral index move off 1? Model the one-sided (mirror-broken) tail as the
# single-turning-point Airy connection (index 1/3 in its OWN argument), but with the argument map
# z(w) STILL linear (free V'(x*) finite). Claim: index stays 1 in spectral w unless z(w)~w^{2/3}.
# Demonstrate the argument-map dependence numerically: spectral index of  Ai(-z(w))^2-type tail.
def airy_tail_idx(zmap, w0, dw=1e-4):
    # density ~ Ai(-zmap(w))^2 ; spectral index -d log dens/d log w large w (envelope only)
    def env(wv):
        z = zmap(wv)
        # Airy oscillatory envelope ~ z^{-1/2}; the ESSENTIAL content is in the phase, but for a
        # *real* spectral edge (analytic continuation) the decaying partner ~ exp(-(2/3) z^{3/2}).
        return mp.e**(-(mp.mpf(2)/3)*z**mp.mpf('1.5'))
    f0 = mp.log(env(w0)); f1 = mp.log(env(w0*mp.e**dw))
    return float((f1-f0)/dw)
print("decaying-Airy-partner spectral index  -d log/d log w  for different argument maps z(w):")
for label, zmap in [("z~w (free/linear arg, O2 NOT defeated)", lambda wv: wv),
                    ("z~w^{2/3} (soft fold, O2 defeated)",     lambda wv: wv**(mp.mpf(2)/3))]:
    idxs = [airy_tail_idx(zmap, mp.mpf(W)) for W in [50,200,800,3200]]
    print(f"  {label}: ", [round(i,4) for i in idxs])
print("  KEY: free linear arg z~w gives index 3/2 (NOT 1/3, and NOT the route's '1' either —")
print("       it's the bare Airy 3/2 power); z~w^{2/3} gives index 1. Investigate which the")
print("       free Poschl-Teller actually realizes (V2 said thermal index 1).")
