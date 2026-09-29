#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG171 S1 -- door 11A, Step 1 and the symbolic half of Step 2 (sympy).  Frozen criteria: FROZEN_QUESTION.md.

  1a  Schwarzschild-de Sitter in Painleve-Gullstrand form: v^2 = 2GM/r + Lambda c^2 r^2/3 EXACTLY, no M-Lambda cross term;
      the PG congruence (lapse 1) is geodesic for ANY v(r), with d^2r/dtau^2 = v v'.
  1b  a LINEAR velocity superposition v = v_N + v_Lambda: the cross-term acceleration is s H sqrt(GM/(2r)) ~ r^(-1/2);
      rotation speed ~ r^(1/4); not the deep-MOND r^(-1).
  1c  NO algebraic superposition term v_N^a v_L^b c^(2-a-b) gives the deep-MOND force sqrt(M)/r: the exponents it forces
      (a = 1, b = 1/2) make the term r-independent, so its force is ZERO.  The constant tail (a = 0, b = 1) is origin-centred
      and M-independent.
  1d  a pure Lambda vacuum (P = -rho c^2) has T^{mu nu} independent of u^mu: it has no velocity (w != -1 control depends on u).
  1e  conserved barotropic medium, steady radial inflow outside its sink: attraction falling slower than r^-5 needs c_s^2 < 0;
      a Lambda-like EOS P = w rho c^2 gives c_s,eff^2 = w c^2/(1+w) (< 0, |c_s| >~ c for w near -1: incompressible).
  1f  isothermal c_s^2 = -K < 0: g_in = (2K/r) v^2/(v^2 + K)  ->  2K/r supersonic (flat curve set by K), ~ r^-5 subsonic.
  1g  Hamilton-Jacobi (Bernoulli) potential flow: D(grad chi)/Dt = -grad Phi identically (parcels = test particles).
  1h  P2's AQUAL form is elliptic: d(mu(z) z)/dz = 2z/sqrt(1+4z^2) > 0; the scale a0^2/(8 pi G) = (kappa^2/8 pi) rho_L c^2;
      c H_Lambda/a0 = sqrt(8 pi/3)/kappa = sqrt(32 pi/3) at kappa = 1/2.

MUTATE (--mutate a): a linear-superposition cross term is inserted into the SdS metric function; claim 1a must FAIL (exit 1).
Runs in a few seconds.
"""
import sys
sys.dont_write_bytecode = True
import sympy as sp  # noqa: E402
from cfg171_common import Report, parse_mode  # noqa: E402

MODE = parse_mode(sys.argv, ["a"])
R = Report("cfg171_s1_symbolic", MODE)
P, check = R.P, R.check
R.P(f"CFG171 S1 -- symbolic checks (mode: {'MAIN' if MODE is None else 'MUTATE_' + MODE})")

G, M, c, Lam, r, t, H, a0, kappa, rho = sp.symbols("G M c Lambda r t H a_0 kappa rho", positive=True)

# ================================================================================================================== 1a
R.banner("1a  Schwarzschild-de Sitter -> Painleve-Gullstrand: v^2 = 2GM/r + Lambda c^2 r^2/3, no cross term; geodesic congruence")
f = 1 - 2 * G * M / (r * c ** 2) - Lam * r ** 2 / 3
if MODE == "a":
    # MUTATE: the metric that a LINEAR superposition v = v_N - v_L would need: c^2(1 - f) = (sqrt(2GM/r) + c sqrt(Lambda/3) r)^2
    f = f - 2 * sp.sqrt(2 * G * M / r) * sp.sqrt(Lam / 3) * r / c
    P("    MUTATE a: f(r) carries the cross term -2 sqrt(2GM/r) sqrt(Lambda/3) r / c")
T_, dT, dt, dr = sp.symbols("T dT dt dr")
psi_p = sp.sqrt(1 - f) / (c * f)                         # T = t + psi(r),  psi' = sqrt(1-f)/(c f)
ds2_static = -f * c ** 2 * dT ** 2 + dr ** 2 / f
ds2 = sp.expand(ds2_static.subs(dT, dt + psi_p * dr))
coef_dr2 = ds2.coeff(dr, 2)
coef_dtdr = ds2.coeff(dt, 1).coeff(dr, 1)
coef_dt2 = ds2.coeff(dt, 2)
v2 = sp.expand(c ** 2 * (1 - f))
P(f"    PG form -c^2 dt^2 + (dr - v dt)^2 requires g_rr = 1, g_tt = -c^2 + v^2, (2 g_tr)^2 = 4 v^2 with v^2 = c^2(1 - f) = {v2}")
# the PG-form identities are checked exactly at 6 rational points inside the static patch (fast and exact; no simplify of radicals)
pts = [dict(G=sp.Rational(1), M=sp.Rational(1, 10), c=sp.Rational(1), Lambda=sp.Rational(1, 1000), r=sp.Rational(k, 1)) for k in (1, 2, 3, 5, 7, 11)]
res_form = []
for pt in pts:
    sub = {G: pt["G"], M: pt["M"], c: pt["c"], Lam: pt["Lambda"], r: pt["r"]}
    res_form.append((sp.nsimplify(sp.simplify(coef_dr2.subs(sub) - 1)), sp.simplify(coef_dt2.subs(sub) - (-c ** 2 + v2).subs(sub)),
                     sp.simplify(coef_dtdr.subs(sub) ** 2 - 4 * v2.subs(sub))))
ok_form = all(all(abs(float(q_)) < 1e-30 for q_ in trip) for trip in res_form)
P(f"    exact residuals of (g_rr - 1, g_tt + c^2 - v^2, (2g_tr)^2 - 4v^2) at 6 points: {[tuple(float(q_) for q_ in trip) for trip in res_form]}")
target_v2 = 2 * G * M / r + Lam * c ** 2 * r ** 2 / 3
cross = sp.simplify(sp.diff(v2, M, Lam))
ok_1a = ok_form and sp.simplify(v2 - target_v2) == 0 and cross == 0
check("1a PG-SdS: the transformed metric is exactly -c^2 dt^2 + (dr - v dt)^2 with v^2 = 2GM/r + Lambda c^2 r^2/3; the mixed derivative "
      "d^2(v^2)/dM dLambda = 0 (the Newtonian and Lambda flows add in v^2, with NO cross term)",
      f"PG form {ok_form}; v^2 - target = {sp.simplify(v2 - target_v2)}; d2(v^2)/dMdLambda = {cross}", ok_1a)

# geodesic congruence for ANY v(r): metric in (t, r, th, ph) = (-(c^2 - v^2), -v; -v, 1; r^2; r^2 sin^2)
th, ph = sp.symbols("theta phi")
vf = sp.Function("v")(r)
X = [t, r, th, ph]
g = sp.Matrix([[-(c ** 2 - vf ** 2), -vf, 0, 0], [-vf, 1, 0, 0], [0, 0, r ** 2, 0], [0, 0, 0, r ** 2 * sp.sin(th) ** 2]])
gi = sp.simplify(g.inv())
Gam = [[[sp.simplify(sum(gi[m, l] * (sp.diff(g[l, a], X[b]) + sp.diff(g[l, b], X[a]) - sp.diff(g[a, b], X[l])) for l in range(4)) / 2)
         for b in range(4)] for a in range(4)] for m in range(4)]
u = [1, vf, 0, 0]                                        # dt/dtau = 1, dr/dtau = v(r)
norm = sp.simplify(sum(g[a, b] * u[a] * u[b] for a in range(4) for b in range(4)))
acc = [sp.simplify(-sum(Gam[m][a][b] * u[a] * u[b] for a in range(4) for b in range(4))) for m in range(4)]
dudtau = [0, vf * sp.diff(vf, r), 0, 0]                  # along the congruence d/dtau = v d/dr
ok_geo = sp.simplify(norm + c ** 2) == 0 and all(sp.simplify(acc[m] - dudtau[m]) == 0 for m in range(4))
check("1a' for ANY v(r) the PG flow observers u = (1, v, 0, 0) are unit timelike and geodesic, with d^2r/dtau^2 = v v' = d(v^2/2)/dr exactly "
      "(so the inward acceleration is g = -d(v^2/2)/dr, the door's formula)",
      f"u.u = {norm}; -Gamma^r uu = {acc[1]}; -Gamma^t uu = {acc[0]}", ok_geo)

# ================================================================================================================== 1b
R.banner("1b  linear velocity superposition v = v_N + s H r (s = +1 Lambda outflow, -1 inflow)")
s = sp.symbols("s")
vN = -sp.sqrt(2 * G * M / r)
vlin = vN + s * H * r
v2lin = sp.expand(vlin ** 2)
cross_v2 = sp.simplify(v2lin - (vN ** 2 + H ** 2 * r ** 2 * s ** 2))
g_cross = sp.simplify(-sp.diff(cross_v2 / 2, r))
slope = sp.simplify(r * sp.diff(sp.log(g_cross.subs(s, 1)), r))
Vrot2 = sp.simplify(r * g_cross.subs(s, 1))
slopeV = sp.simplify(r * sp.diff(sp.log(sp.sqrt(Vrot2)), r))
ratio_deep = sp.simplify(g_cross.subs(s, 1) / (sp.sqrt(G * M * a0) / r))
P(f"    cross term in v^2 = {cross_v2};  its inward acceleration = {g_cross}")
P(f"    d ln g_cross/d ln r = {slope};  rotation speed V ~ r^{slopeV};  g_cross / (deep-MOND sqrt(G M a0)/r) = {ratio_deep}")
ok_1b = sp.simplify(g_cross - s * H * sp.sqrt(G * M / (2 * r))) == 0 and slope == sp.Rational(-1, 2) and slopeV == sp.Rational(1, 4)
check("1b linear superposition: cross-term acceleration = s H sqrt(GM/(2r)) ~ r^(-1/2) (attractive for the Lambda OUTFLOW s = +1), "
      "V ~ r^(1/4); its ratio to deep MOND grows as H sqrt(r/(2 a0)) (not a constant): not the deep-MOND law",
      f"g_cross = {g_cross}; slope {slope}; V slope {slopeV}", ok_1b)

# ================================================================================================================== 1c
R.banner("1c  no algebraic superposition of the Newtonian and Lambda flows gives the deep-MOND force")
aa, bb, Cc = sp.symbols("a b C", real=True)
term = Cc * (sp.sqrt(2 * G * M / r)) ** aa * (H * r) ** bb * c ** (2 - aa - bb)          # a v^2-type term
g_term = sp.simplify(-sp.diff(term / 2, r))
# exponents of M and r in the force
eM = sp.simplify(M * sp.diff(sp.log(g_term), M))
er = sp.simplify(r * sp.diff(sp.log(g_term), r))
sol = sp.solve([sp.Eq(eM, sp.Rational(1, 2)), sp.Eq(er, -1)], [aa, bb], dict=True)
P(f"    force of the term: M-exponent {eM}, r-exponent {er}; deep MOND (M^1/2 r^-1) requires {sol}")
g_at = sp.simplify(g_term.subs({aa: 1, bb: sp.Rational(1, 2)}))
term_at = sp.simplify(term.subs({aa: 1, bb: sp.Rational(1, 2)}))
P(f"    at a = 1, b = 1/2 the v^2 term is {term_at} (r-independent) and its force is {g_at}")
tail = sp.simplify(g_term.subs({aa: 0, bb: 1}))
P(f"    the M-independent constant force (a = 0, b = 1) is {tail}: equal to the P2 tail a0/2 only for C = -a0/(c H) = -1/Z (origin-centred)")
ok_1c = len(sol) == 1 and sol[0][aa] == 1 and sol[0][bb] == sp.Rational(1, 2) and g_at == 0 and sp.diff(term_at, r) == 0
check("1c the only algebraic term with the deep-MOND scalings (sqrt(M), 1/r in the force) is v_N (c v_L)^(1/2) = sqrt(2 G M c H): r-independent, "
      "so its force is identically ZERO; the 1/r force needs a logarithm, i.e. a differential (field) law, not a superposition rule",
      f"solution {sol}; term {term_at}; force {g_at}", ok_1c)

# ================================================================================================================== 1d
R.banner("1d  a pure Lambda vacuum has no velocity: T^{mu nu} = (rho + P/c^2) u u + P eta^-1 is u-independent at P = -rho c^2")
beta = sp.symbols("beta", real=True)
gam = 1 / sp.sqrt(1 - beta ** 2)
U = sp.Matrix([gam * c, gam * beta * c, 0, 0])
eta_inv = sp.diag(-1, 1, 1, 1)


def Tmunu(w):
    Pp = w * rho * c ** 2
    return sp.simplify((rho + Pp / c ** 2) * U * U.T + Pp * eta_inv)


dT_L = sp.simplify(sp.diff(Tmunu(-1), beta))
dT_dust = sp.simplify(sp.diff(Tmunu(sp.Rational(-9, 10)), beta))
ok_1d = dT_L == sp.zeros(4, 4) and dT_dust != sp.zeros(4, 4)
check("1d at w = -1 dT/dbeta = 0 for every component (the Lambda vacuum is boost-invariant: it has no rest frame and no flow velocity); "
      "control: at w = -0.9 T depends on beta. A 'flowing Lambda-vacuum' therefore needs a medium that is NOT exactly Lambda (or a vector/khronon, 11C)",
      f"w=-1: {dT_L == sp.zeros(4, 4)}; w=-0.9 u-dependent: {dT_dust != sp.zeros(4, 4)}", ok_1d)

# ================================================================================================================== 1e
R.banner("1e  conserved barotropic medium, steady radial inflow outside its sink: the sign of c_s^2 needed for attraction")
n, cs2, w = sp.symbols("n c_s2 w", real=True)
vv = sp.symbols("v", positive=True)                       # |v|
# continuity rho v r^2 = const -> rho'/rho = -2/r - v'/v ; Euler v v' = -c_s^2 rho'/rho ; |v| ~ r^-n -> v'/v = -n/r
rho_log = -2 / r - (-n / r)
g_in_kin = n * vv ** 2 / r                                # -d(v^2/2)/dr for v^2 ~ r^(-2n)
cs2_req = sp.solve(sp.Eq(g_in_kin, cs2 * rho_log), cs2)[0]
P(f"    required c_s^2 = {sp.simplify(cs2_req)}  (Newton n = 1/2: {sp.simplify(cs2_req.subs(n, sp.Rational(1, 2)))};  n -> 0: {sp.limit(cs2_req, n, 0)})")
# the deep-MOND log profile v^2 = 2 V^2 ln(R/r), general-v form c_s^2 = g_in / (rho'/rho)
V, Rr = sp.symbols("V R", positive=True)
Lsym = sp.symbols("L", positive=True)
Lf = sp.Function("Lf")(r)                                 # L(r) = ln(R/r), L' = -1/r (substituted after differentiating)
vlog = -sp.sqrt(2 * V ** 2 * Lf)
dsub = {sp.Derivative(Lf, r): -1 / r}
g_log = sp.simplify((-sp.diff(vlog ** 2 / 2, r)).subs(dsub))
rholog = sp.simplify((-2 / r - sp.diff(vlog, r) / vlog).subs(dsub))
cs2_log = sp.simplify(g_log / rholog)
cs2_logL = sp.simplify(cs2_log.subs(Lf, Lsym))
chk_log = sp.simplify(cs2_logL + V ** 2 / (2 - 1 / (2 * Lsym)))
P(f"    deep-MOND log flow: g = {g_log}; rho'/rho = {rholog}; required c_s^2 = {cs2_logL} (L = ln(R/r))")
# Lambda-like EOS: relativistic Euler, Newtonian velocities: (1+w) rho v v' = -w c^2 rho'
cs2_eff = sp.simplify(w * c ** 2 / (1 + w))
ok_1e = (sp.simplify(cs2_req + n * vv ** 2 / (2 - n)) == 0
         and all(sp.simplify(cs2_req.subs(n, q)).is_negative for q in (sp.Rational(1, 4), sp.Rational(1, 2), 1, sp.Rational(3, 2)))
         and chk_log == 0 and sp.simplify(cs2_logL.subs(Lsym, 3)).is_negative and sp.simplify(cs2_eff.subs(w, sp.Rational(-1, 2)) + c ** 2) == 0
         and sp.simplify(cs2_eff.subs(w, sp.Rational(1, 3)) - c ** 2 / 4) == 0)
P(f"    Addendum 2 (massless medium): w = 1/3 (radiation-like) gives c_s,eff^2 = {sp.simplify(cs2_eff.subs(w, sp.Rational(1, 3)))} > 0 -> no attraction "
  f"outside the sink; w = -1 has no velocity (1d)")
check("1e attraction outside the sink with |v| ~ r^-n, 0 < n < 2 (force slower than r^-5) requires c_s^2 = -n v^2/(2 - n) < 0; the deep-MOND "
      "log flow requires c_s^2 = -V^2/(2 - 1/(2L)) < 0; a Lambda-like EOS gives c_s,eff^2 = w c^2/(1+w) (= -c^2 at w = -1/2): negative, "
      "i.e. a gradient instability, and |c_s| ~ c makes the flow incompressible at galactic speeds (v ~ r^-2, force ~ r^-5); the massless "
      "radiation-like w = 1/3 gives +c^2/4: no attraction at all",
      f"c_s^2(n) = {sp.simplify(cs2_req)}; log flow {cs2_logL}; Lambda EOS {cs2_eff}", ok_1e)

# ================================================================================================================== 1f
R.banner("1f  isothermal c_s^2 = -K < 0: Bernoulli v^2/2 - K ln rho = E with rho = Q/(4 pi r^2 |v|)")
K = sp.symbols("K", positive=True)
vr = sp.Function("u")(r)                                  # |v|
bern = vr ** 2 / 2 + K * sp.log(vr) + 2 * K * sp.log(r)   # = const
dv = sp.solve(sp.diff(bern, r), sp.diff(vr, r))[0]
g_iso = sp.simplify(-(vr * dv))
P(f"    g_in = -v v' = {g_iso}")
sup = sp.limit(g_iso.subs(vr, sp.Symbol("q", positive=True)), sp.Symbol("q", positive=True), sp.oo)
q = sp.Symbol("q", positive=True)
sub_lead = sp.series(g_iso.subs(vr, q), q, 0, 3).removeO()
ok_1f = sp.simplify(g_iso - 2 * K * vr ** 2 / (r * (vr ** 2 + K))) == 0 and sp.simplify(sup - 2 * K / r) == 0
check("1f isothermal negative-c_s^2 medium: g_in = (2K/r) v^2/(v^2 + K): supersonic limit 2K/r (a 1/r force whose amplitude V_c^2 = 2K is a "
      "property of the MEDIUM, the same for every mass -- the BTFR needs K = sqrt(G M a0)/2, i.e. the medium slaved to the enclosed mass, "
      "CFG44's postulate again); subsonic limit 2 v^2/r with v ~ r^-2 (force ~ r^-5)",
      f"g = {g_iso}; supersonic -> {sup}; subsonic leading {sub_lead}", ok_1f)

# ================================================================================================================== 1g
R.banner("1g  Hamilton-Jacobi potential flow: D(grad chi)/Dt = -grad Phi identically (3-D, time-dependent)")
x, y, z = sp.symbols("x y z", real=True)
chi = sp.Function("chi")(t, x, y, z)
Phi = sp.Function("Phi")(t, x, y, z)
XS = (x, y, z)
vel = [sp.diff(chi, q_) for q_ in XS]
chi_t = -(sum(vi ** 2 for vi in vel) / 2 + Phi)            # the HJ / unsteady-Bernoulli law
res = []
for i, qi in enumerate(XS):
    dvdt = sp.diff(chi_t, qi)                               # d/dt grad chi = grad chi_t
    adv = sum(vel[j] * sp.diff(vel[i], XS[j]) for j in range(3))
    res.append(sp.simplify(dvdt + adv + sp.diff(Phi, qi)))
ok_1g = all(rr_ == 0 for rr_ in res)
check("1g for v = grad chi with chi_t + |grad chi|^2/2 + Phi = 0, Dv/Dt + grad Phi = 0 identically: the flow's parcels are ordinary test particles "
      "in Phi; the flow adds no dynamics and no frame (the law is Galilean-covariant)", f"residuals {res}", ok_1g)

# ================================================================================================================== 1h
R.banner("1h  P2 as an AQUAL flow-potential equation: ellipticity and the Lambda reading of its scale")
zz = sp.symbols("z", positive=True)
yofz = (-1 + sp.sqrt(1 + 4 * zz ** 2)) / 2                 # g^2 = gN^2 + a0 gN  ->  y = mu(z) z
chk_inv = sp.simplify((yofz ** 2 + yofz) - zz ** 2)
dmu = sp.simplify(sp.diff(yofz, zz))
Pcap = sp.simplify((kappa * c * sp.sqrt(G * rho)) ** 2 / (8 * sp.pi * G))
HL = sp.sqrt(8 * sp.pi * G * rho / 3)
Zexpr = sp.simplify(c * HL / (kappa * c * sp.sqrt(G * rho)))
ok_1h = chk_inv == 0 and sp.simplify(dmu - 2 * zz / sp.sqrt(1 + 4 * zz ** 2)) == 0 and sp.simplify(Pcap - kappa ** 2 * rho * c ** 2 / (8 * sp.pi)) == 0 \
    and sp.simplify(Zexpr.subs(kappa, sp.Rational(1, 2)) - sp.sqrt(32 * sp.pi / 3)) == 0
check("1h P2 inverts to mu(z) z = (sqrt(1+4z^2) - 1)/2 with d(mu z)/dz = 2z/sqrt(1+4z^2) > 0 (AQUAL elliptic); the scale a0^2/(8 pi G) = "
      "(kappa^2/8 pi) rho_Lambda c^2 (CFG43's P_cap); c H_Lambda/a0 = sqrt(8 pi/3)/kappa = sqrt(32 pi/3) at kappa = 1/2 (Z = kappa restated, FITTED)",
      f"inverse check {chk_inv}; d(mu z)/dz = {dmu}; P_cap = {Pcap}; Z = {Zexpr}", ok_1h)

nf = R.write()
if MODE is not None:
    P("  MUTATE run: claim 1a must fail -> exit 1" if not ok_1a else "  MUTATE run: claim 1a did NOT fail -- the control is broken")
    sys.exit(1 if not ok_1a else 0)
sys.exit(1 if nf else 0)
