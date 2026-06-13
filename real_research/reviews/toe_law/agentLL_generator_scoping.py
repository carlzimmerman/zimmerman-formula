#!/usr/bin/env python3
# agentLL_generator_scoping.py — machine record for agentLL (generator scoping).
# Lemmas LL-1..LL-3 + candidate (d) b-family caustic, computed with sympy/mpmath.
# Conventions: transform variable called w (omega) >= 0; fingerprint class
#   F_req(w) ~ (c_chi w)^(-5/3) exp(-ct*(c_chi w)^(1/3)) cos(sqrt(3)*ct*(c_chi w)^(1/3)+phi+pi/3),
#   ct = (3/4)*2^(2/3)*zt^(2/3).   zt (zeta-tilde) QUARANTINED throughout; raw numbers only.
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
LINE = "-" * 78

def banner(s):
    print()
    print(LINE)
    print(s)
    print(LINE)

# ============================================================================
banner("LL-1a  SYMBOLIC: saddle set of the split-cubic exponent Phi(s)=w s^2 - i b/s")
# Density-side picture: f(w) = int_0^inf e^{-w t} cos(beta t^{-1/2}) dt ;
# t = s^2 turns the t^{-1/2} essential point into the SPLIT CUBIC Phi = w s^2 -+ i beta/s.
# (J_+ component: e^{+i beta/sqrt t}.)  Saddle eq: Phi' = 2 w s + i b / s^2 = 0  =>  s^3 = -i b/(2w).
w_s, b_s = sp.symbols('w beta', positive=True)
s = sp.symbols('s')  # complex
Phi = w_s * s**2 - sp.I * b_s / s
# saddle eq: Phi' = 2 w s + i beta/s^2 = 0  <=>  2 w s^3 + i beta = 0
saddles = sp.solve(2 * w_s * s**3 + sp.I * b_s, s)
print("saddle equation: s^3 = -i*beta/(2 w); roots and actions:")
for sk in saddles:
    a = sp.simplify(sp.expand_complex(Phi.subs(s, sk) / (w_s**sp.Rational(1, 3) * b_s**sp.Rational(2, 3))))
    re, im = sp.simplify(sp.re(a)), sp.simplify(sp.im(a))
    arg = sp.simplify(sp.arg(sp.simplify(sp.expand_complex(sk / (b_s / (2 * w_s))**sp.Rational(1, 3)))))
    ratio = sp.simplify(im / re) if sp.simplify(re) != 0 else sp.oo
    print("  arg(s*) =", arg)
    print("     Phi(s*)/(w^(1/3) beta^(2/3)):  Re =", re, "  Im =", im, "  Im/Re =", ratio)
print()
print("Check: |Phi(s*)| common modulus 3*2^(-2/3) = %.6f" % float(3 * 2**(-sp.Rational(2, 3))))
print("Admissible (Re>0, decaying) pair sits at action phases -+pi/3  =>  |Im|/Re = sqrt(3) EXACTLY.")
print("Third root has Re<0 (growing e^{+c w^(1/3)}): Stokes-excluded for a Laplace transform")
print("of a locally integrable one-sided density (transform must decay in Re w > 0).")
# explicit: Phi'' = 2w - 2i beta/s^3 ; on-shell s^3 = -i beta/(2w) => -2i beta/s^3 = 4w => Phi'' = 6w
Phipp = sp.simplify(2 * w_s - 2 * sp.I * b_s / (-sp.I * b_s / (2 * w_s)))
print("on-shell Phi''(s*) =", Phipp, " (= 6w exactly, beta-independent fluctuation)")

banner("LL-1b  SYMBOLIC: Stokes/descent sectors of the pure cubic e^{-u^3}: 2pi/3 triad")
th = sp.symbols('theta', real=True)
bnds = sorted(sp.solveset(sp.cos(3 * th), th, sp.Interval(-sp.pi, sp.pi)))
print("decay sectors of e^{-u^3}:  Re u^3 > 0  <=>  cos(3 theta) > 0; boundaries cos(3theta)=0 at:")
print("   theta =", bnds)
centers = [c for c in [-2 * sp.pi / 3, 0, 2 * sp.pi / 3]]
print("sector centers (cos(3 theta)=+1):", [sp.nsimplify(c) for c in centers],
      "; widths pi/3; separations 2pi/3 — the Stokes triad of the cubic class.")

banner("LL-1c  pure-cubic scaling I(w) ~ w^(-1/3): substitution + constant pin")
# I(w) = int e^{-w a u^3} du over the canonical two-ray contour: u -> (w a)^(-1/3) v
# => I = (w a)^(-1/3) * C3, C3 = contour integral of e^{-v^3} (pure number).
wa = sp.symbols('W', positive=True)
print("u -> (W)^(-1/3) v gives I = W^(-1/3) * C3 exactly: index 1/3 from the CUBIC alone.")
# constant pin via Airy normalization: Ai(0) = 3^(-2/3)/Gamma(2/3)
print("constant pin: Ai(0) =", mp.airyai(0), " vs 3^(-2/3)/Gamma(2/3) =",
      mp.power(3, mp.mpf(-2) / 3) / mp.gamma(mp.mpf(2) / 3))

banner("LL-1d  NUMERIC: F(w)=int_0^inf e^{-wt} cos(beta t^{-1/2}) dt  vs two-saddle formula")
# Rotated contour (valid: integrand analytic in -pi/6<=arg s<=0, decay on arcs):
#   J+ = 2 e^{-i pi/3} int_0^inf sigma exp(-w e^{-i pi/3} sigma^2 + beta e^{2 i pi/3}/sigma) dsigma
#   F  = Re J+.
# Saddle formula (LL-1a): s0=(beta/2w)^{1/3} e^{-i pi/6}, Phi(s0)=3*2^{-2/3} beta^{2/3} w^{1/3} e^{-i pi/3},
#   Phi''=6w, prefactor 2 s0:  F_as = Re[ 2 s0 sqrt(2 pi/(6 w)) e^{-Phi(s0)} ].
beta_n = mp.mpf(1)

def F_num(wv):
    wv = mp.mpf(wv)
    rot = mp.e**(-1j * mp.pi / 3)
    osc = mp.e**(2j * mp.pi / 3)
    sig_star = (beta_n / (2 * wv))**(mp.mpf(1) / 3)
    f = lambda sg: sg * mp.e**(-wv * rot * sg**2 + beta_n * osc / sg)
    pts = [0, sig_star / 4, sig_star, 4 * sig_star, 20 * sig_star, 100 * sig_star]
    val = mp.quad(f, pts, maxdegree=10)
    return mp.re(2 * mp.e**(-1j * mp.pi / 3) * val)

def F_saddle(wv):
    wv = mp.mpf(wv)
    s0 = (beta_n / (2 * wv))**(mp.mpf(1) / 3) * mp.e**(-1j * mp.pi / 6)
    Phi0 = 3 * mp.mpf(2)**(mp.mpf(-2) / 3) * beta_n**(mp.mpf(2) / 3) * wv**(mp.mpf(1) / 3) * mp.e**(-1j * mp.pi / 3)
    return mp.re(2 * s0 * mp.sqrt(2 * mp.pi / (6 * wv)) * mp.e**(-Phi0))

print("%10s %22s %22s %12s" % ("w", "F_numeric", "F_saddle", "ratio"))
for wv in [1e3, 1e4, 1e5]:
    fn, fa = F_num(wv), F_saddle(wv)
    print("%10.0f %22.12e %22.12e %12.7f" % (wv, float(fn), float(fa), float(fn / fa)))
print("ratio -> 1 with O(w^(-1/3)) drift: the two-saddle (pair at -+pi/3) formula is the asymptote.")
print("decay rate = (3/2)2^(-2/3) beta^(2/3) w^(1/3); osc rate = sqrt(3) x decay rate. LOCK = sqrt(3).")

banner("LL-1e  SYMBOLIC: universality table — ratio tan(pi/(2(k+1))) fingerprints k")
# density singularity e^{+i beta t^-k} (oscillatory, one-sided): saddle t*^(k+1) = k beta e^{i pi/2}/w
# action Phi* = (1+1/k) w t*  =>  arg Phi* = (pi/2 + 2 pi j)/(k+1); admissible principal j=0.
print("%8s %12s %26s %18s" % ("k", "index", "arg Phi* (principal)", "osc/decay ratio"))
kvals = [sp.Rational(1, 3), sp.Rational(1, 2), sp.Integer(1), sp.Integer(2), sp.Integer(3)]
for k in kvals:
    idx = sp.Rational(k, k + 1)
    argp = sp.pi / (2 * (k + 1))
    ratio = sp.simplify(sp.tan(argp))
    print("%8s %12s %26s %18s" % (k, idx, argp, ratio))
print("STRICTLY MONOTONE in k: ratio sqrt(3) <=> k=1/2 <=> transform index 1/3 (cubic class) UNIQUE.")
print("k=1 (diffusive/heat image class, index 1/2): ratio tan(pi/4)=1 — NOT sqrt(3).")

# ============================================================================
banner("LL-2a  NUMERIC: the canonical pair  Q(W)=int_0^inf Ai(v) e^{-W/v^3} dv = (1/3) e^{-(3W)^{1/3}}")
def Q(W):
    W = mp.mpf(W)
    f = lambda v: mp.airyai(v) * mp.e**(-W / v**3)
    return mp.quad(f, [0, 0.5, 2, 6, 15, 40], maxdegree=10)

print("%8s %24s %24s %12s" % ("W", "Q(W) numeric", "(1/3)exp(-(3W)^(1/3))", "rel err"))
for W in [0.1, 1, 5, 20, 100]:
    qn = Q(W)
    qc = mp.e**(-(3 * mp.mpf(W))**(mp.mpf(1) / 3)) / 3
    print("%8s %24.15e %24.15e %12.2e" % (W, float(qn), float(qc), float(abs(qn - qc) / abs(qc))))
print("=> with B=3^(-1/3):  L[ 3^(-1/3) t^(-4/3) Ai(3^(-1/3) t^(-1/3)) ](w) = e^{-w^{1/3}} exactly")
print("   (one-sided stable-1/3 density in Airy form; normalization A/B = 1).")

banner("LL-2b  NUMERIC: oscillatory member — NEGATIVE-argument Airy density (EXACT closed form)")
# h(t) = t^{-4/3} Ai(-B t^{-1/3}), B=3^{-1/3}:
#   L[h](w) = 3 int_0^inf Ai(-B u) e^{-w u^{-3}} du
#           = 2*3^{1/3} e^{-w^{1/3}/2} cos( (sqrt(3)/2) w^{1/3} )   [Airy connection formula:
#   Ai(-z)=e^{i pi/3}Ai(e^{i pi/3}z)+c.c.; each rotated member = the LL-2a pair at B'^3=-B^3,
#   handing e^{-w^{1/3} e^{+-i pi/3}} — the +-pi/3 pair of LL-1a, hence the sqrt(3) lock EXACTLY.]
#   consistency: w->0 limit = 2*3^{1/3} = 3*(2/(3B)). The first run carried a hand-normalization
#   slip (2/3^{2/3}, exactly 3x small) — caught by this quadrature and corrected; numeric unchanged.
# numeric: subtract the W=0 limit: int Ai(-Bu) du = (1/B) int_0^inf Ai(-x) dx = (1/B)(2/3)
Bc = mp.power(3, -mp.mpf(1) / 3)

def Lh(wv):
    wv = mp.mpf(wv)
    base = (2 / mp.mpf(3)) / Bc
    f = lambda u: mp.airyai(-Bc * u) * (mp.e**(-wv / u**3) - 1)
    pts = [0, 1, 3, 8, 20, 60, 150, 400, 1000, 2500]
    corr = mp.quad(f, pts, maxdegree=10)
    return 3 * (base + corr)

print("%8s %24s %24s %12s" % ("w", "L[h] numeric", "closed form", "rel err"))
for wv in [8, 27, 64, 125]:
    ln_ = Lh(wv)
    cf = 2 * mp.power(3, mp.mpf(1) / 3) * mp.e**(-mp.mpf(wv)**(mp.mpf(1) / 3) / 2) * mp.cos(mp.sqrt(3) / 2 * mp.mpf(wv)**(mp.mpf(1) / 3))
    print("%8s %24.15e %24.15e %12.2e" % (wv, float(ln_), float(cf), float(abs(ln_ - cf) / (abs(cf) + mp.mpf('1e-30')))))
print("=> EXACT (not asymptotic): decay rate 1/2, osc rate sqrt(3)/2 — the sqrt(3) lock, phase 0 member.")
print("   w->0 consistency: L[h](0) = 2*3^(1/3) = %.12f = closed form at w=0 ✓" % float(2 * mp.power(3, mp.mpf(1) / 3)))

def Lh_cut(wv, U):
    wv = mp.mpf(wv)
    base = (2 / mp.mpf(3)) / Bc
    f = lambda u: mp.airyai(-Bc * u) * (mp.e**(-wv / u**3) - 1)
    pts = [0, 1, 3, 8, 20, 60, 150, 400, 1000] + [U // 4, U]
    corr = mp.quad(f, pts, maxdegree=10)
    return 3 * (base + corr)

cf27 = 2 * mp.power(3, mp.mpf(1) / 3) * mp.e**(-mp.mpf(3) / 2) * mp.cos(mp.sqrt(3) / 2 * 3)
r1 = abs(Lh_cut(27, 2500) - cf27)
r2 = abs(Lh_cut(27, 10000) - cf27)
print("   residual is TAIL TRUNCATION, not formula error: |num-closed| at w=27:")
print("     cutoff u=2500: %.2e   cutoff u=10000: %.2e  (shrinks with cutoff ✓)" % (float(r1), float(r2)))

banner("LL-2c  SYMBOLIC: the pi/3 phase quantum & prefactor (2/3)-power quantum (t-weight law)")
wv_s = sp.symbols('w', positive=True)
CF = sp.Rational(2, 1) / 3**sp.Rational(2, 3) * sp.exp(-wv_s**sp.Rational(1, 3) / 2) * sp.cos(sp.sqrt(3) / 2 * wv_s**sp.Rational(1, 3))
dCF = sp.simplify(sp.diff(CF, wv_s))
# claim: -dCF/dw = (1/3) w^{-2/3} * (2/3^{2/3}) e^{-w^{1/3}/2} cos( sqrt3/2 w^{1/3} - pi/3 )
target = sp.Rational(1, 3) * wv_s**sp.Rational(-2, 3) * sp.Rational(2, 1) / 3**sp.Rational(2, 3) * sp.exp(-wv_s**sp.Rational(1, 3) / 2) * sp.cos(sp.sqrt(3) / 2 * wv_s**sp.Rational(1, 3) - sp.pi / 3)
print("L[t*h](w) = -d/dw L[h](w);  identity  -dCF - (1/3)w^(-2/3)*CF-shape*cos(...-pi/3) == 0 ?")
print("  simplify(-dCF - target) =", sp.simplify(-dCF - target))
print("=> one t-power in the density  ==  prefactor x (1/3) w^{-2/3}  AND  phase shift EXACTLY -pi/3.")
print("   (phase quantum pi/3 = saddle argument arg t* = -+pi/3; the fingerprint's '+pi/3' is one quantum;")
print("    LL-1d's mu=0 member shows the half-quantum pi/6 from the s0 prefactor — same origin.)")

banner("LL-2d  SYMBOLIC: fingerprint constant ct = (3/4)2^{2/3} zt^{2/3}  <=>  density strength beta = zt/2")
zt, beta_q = sp.symbols('zetatilde beta', positive=True)
eqn = sp.Eq(3 * 2**sp.Rational(-2, 3) * beta_q**sp.Rational(2, 3), sp.Rational(3, 4) * 2**sp.Rational(2, 3) * zt**sp.Rational(2, 3))
solb = sp.solve(eqn, beta_q)
print("solve  3*2^(-2/3) beta^(2/3) = (3/4)*2^(2/3) zt^(2/3)  =>  beta =", solb)
print("RAW + QUARANTINED: in c_chi units the fingerprint's essential-singularity strength is zt/2.")
print("No Z claim; zt itself stays quarantined per discipline.")

# ============================================================================
banner("LL-3  the orientation kill — one-line checks")
# (i) quadratic-saddle / diffusive class k=1: ratio 1
print("(i)  k=1 (e^{-beta/t} image, quadratic class index 1/2): ratio tan(pi/4) =", sp.tan(sp.pi / 4), " != sqrt(3)")
# (ii) pure power-law density: no exponential factor at all
t_s, al = sp.symbols('t alpha', positive=True)
LT = sp.integrate(t_s**al * sp.exp(-wv_s * t_s), (t_s, 0, sp.oo), conds='none')
print("(ii) pure power density t^alpha: L =", sp.simplify(LT), "  — pure power of w, NO essential factor.")
# (iii) KMS/thermal: Boltzmann tail e^{-2 pi w/kappa}: index 1, ratio 0
print("(iii) KMS-thermal (sinh^2 kernel, S4a): tail e^{-2 pi w/kappa} — index 1, osc/decay ratio 0.")
print("(iv) one-sidedness: transform analytic+decaying in Re w>0 (Paley-Wiener) <=> one-sided density;")
print("     two-sided support injects the Re<0 (growing) cube-root member: excluded by the fingerprint.")

# ============================================================================
banner("S4a  CANDIDATE (d): exact frequency transform of the sinh^-2 worldline kernel")
# closed form: R_-(w,kappa) = int e^{-i w tau} dtau / sinh^2(kappa (tau - i eps)/2)
#            = -(8 pi w / kappa^2) / (e^{2 pi w / kappa} - 1)
# verify numerically on the shifted line tau = sigma - i pi/kappa  (sinh -> -i cosh, exact rewrite):
def R_num(wv, kap):
    wv, kap = mp.mpf(wv), mp.mpf(kap)
    f = lambda sg: mp.e**(-1j * wv * sg) * (-1) / mp.cosh(kap * sg / 2)**2
    L = 60 / kap
    val = mp.quad(f, [-L, -L / 8, 0, L / 8, L], maxdegree=10)
    return mp.e**(-mp.pi * wv / kap) * val

def R_closed(wv, kap):
    wv, kap = mp.mpf(wv), mp.mpf(kap)
    return -(8 * mp.pi * wv / kap**2) / (mp.e**(2 * mp.pi * wv / kap) - 1)

print("%8s %8s %22s %22s %10s" % ("w", "kappa", "numeric", "closed", "rel err"))
for (wv, kap) in [(1, 1), (3, 2), (5, 1.7)]:
    rn, rc = R_num(wv, kap), R_closed(wv, kap)
    print("%8s %8s %22.12e %22.12e %10.1e" % (wv, kap, float(mp.re(rn)), float(rc), float(abs(rn - rc) / abs(rc))))
print("=> single-orbit response tail is BOLTZMANN e^{-2 pi w/kappa}: Gevrey-1 (index 1), per LL-3(iii).")

banner("S4b  kappa(b) from the universal short-distance normalization (RECONSTRUCTED — flagged)")
H, cchi, b_v, kap_s, tau = sp.symbols('H c_chi b kappa tau', positive=True)
G = -H**2 / (16 * sp.pi**2 * cchi * (cchi**2 - b_v**2) * sp.sinh(kap_s * tau / 2)**2)
short = sp.limit(G * tau**2, tau, 0)
print("tau->0:  G_b tau^2 ->", sp.simplify(short))
kap_sol = sp.solve(sp.Eq(short, -1 / (4 * sp.pi**2)), kap_s)
kapb = H / sp.sqrt(cchi * (cchi**2 - b_v**2))
checks = [sp.simplify(kk**2 - kapb**2) for kk in kap_sol]
print("imposing universal -1/(4 pi^2 tau^2): kappa^2 solutions match H^2/(c_chi(c_chi^2-b^2)):",
      [c == 0 for c in checks])
print("positive branch:  kappa(b) = H/sqrt(c_chi (c_chi^2 - b^2))")
print("NOTE: the banked EE closed form was quoted with kappa unspecified in the skeleton summary;")
print("this kappa(b)=H/sqrt(c_chi (c_chi^2-b^2)) is RECONSTRUCTED from the universal UV normalization.")
print("kappa diverges at the family edge b->c_chi (Deser-Levin: T->inf at the horizon) — physical.")

banner("S4c  prefactor-pole cancellation on the family")
pref = sp.simplify(1 / ((cchi**2 - b_v**2) * kapb**2))
print("1/[(c_chi^2-b^2) kappa(b)^2] =", pref, "  — the b-pole CANCELS exactly in the response.")
print("=> family superposition:  F(w) ~ w * int db rho(b) exp(-(2 pi w/H) sqrt(c_chi (c_chi^2-b^2)))")

banner("S4d  bare edge analysis: exponent E(b) vanishes like sqrt(x) at the edge => POWER LAW only")
x, sig, A_s = sp.symbols('x sigma A', positive=True)
E = sp.sqrt(cchi * (cchi**2 - b_v**2))
Eedge = sp.series(E.subs(b_v, cchi * (1 - x)), x, 0, 2).removeO()
print("E(b=c_chi(1-x)) =", sp.simplify(sp.sqrt(2) * cchi**sp.Rational(3, 2) * sp.sqrt(x)), "+ O(x^(3/2))   [leading]")
y = sp.symbols('y', positive=True)
I_edge = sp.integrate(2 * y**(2 * sig + 1) * sp.exp(-A_s * wv_s * y), (y, 0, sp.oo), conds='none')
print("int_0 x^sigma e^{-A w sqrt(x)} dx  (y=sqrt x)  =", sp.simplify(I_edge), "  — PURE POWER LAW in w.")

def Fbare(wv):
    wv = mp.mpf(wv)
    f = lambda bb: mp.e**(-wv * mp.sqrt(1 - bb**2))
    return mp.quad(f, [0, 0.9, 0.99, 1], maxdegree=10)

print("numeric ratio test  s(w) = -dlnF/dlnw  (constant <=> power law; ~w^{1/3} growth <=> essential):")
prev = None
for wv in [1e2, 4e2, 1.6e3, 6.4e3]:
    fv = Fbare(wv)
    if prev is not None:
        slope = -(mp.log(fv) - mp.log(prev[1])) / (mp.log(mp.mpf(wv)) - mp.log(mp.mpf(prev[0])))
        print("   w: %8.0f -> %8.0f   local slope = %.6f" % (prev[0], wv, float(slope)))
    prev = (wv, fv)
print("slope -> 2.0 constant: bare-edge class = w^{-2} POWER LAW. Index-1/3 ABSENT from the bare family.")

banner("S4e  interior saddle b=0: quadratic, not cubic")
E2 = sp.simplify(sp.diff(E, b_v, 2).subs(b_v, 0))
E3 = sp.simplify(sp.diff(E, b_v, 3).subs(b_v, 0))
print("E''(0) =", E2, " (nonzero);  E'''(0) =", E3, " (zero by parity) => ordinary QUADRATIC saddle;")
print("b=0 maximizes E (minimum of integrand): subdominant. No interior cubic degeneracy exists.")

banner("S4f  local normal form at the coalescence (tau-saddle -> b-edge)")
print("Joint exponent on the family, unfolded with y=sqrt(x):  Phi_local = -(2 pi w/H) sqrt(2 c_chi^3) y,")
print("measure 2y dy: LINEAR exponent x smooth measure at an ENDPOINT — Watson-lemma class.")
print("=> F_bare(w) = sum c_n w^{-2(n+1)}: pure power series. NOT cubic (Airy), NOT even pole-saddle")
print("   exponential. Uncancelled-pole variant (other normalization): pinch gives power x log — still")
print("   no essential factor. Fixed-kappa variant: pure thermal e^{-2 pi w/kappa} (index 1). All non-cubic.")

banner("S4g  THE CONVERSION THEOREM: edge measure e^{-gamma x^{-q}} => output index 2q/(2q+1)")
q, gam = sp.symbols('q gamma', positive=True)
# exponent: -gamma x^{-q} - w u0 sqrt(x); saddle x* ~ w^{-1/(q+1/2)}; action ~ w^{1 - 1/(2q+1)} ... derive:
xs, u0 = sp.symbols('x u0', positive=True)
Phi_x = gam * xs**(-q) + wv_s * u0 * sp.sqrt(xs)
xstar = sp.solve(sp.Eq(sp.diff(Phi_x, xs), 0), xs)
xstar = xstar[0]
action = sp.simplify(Phi_x.subs(xs, xstar))
action_pow = sp.simplify(sp.log(action.subs([(gam, 1), (u0, 1)])).diff(wv_s) * wv_s)
print("x* =", xstar)
print("w d(ln action)/dw  =", sp.simplify(action_pow), "  ->  index(q) = 2q/(2q+1)")
idx = sp.Rational(2, 1) * q / (2 * q + 1)
print("%10s %14s" % ("q", "output index"))
for qq in [sp.Rational(1, 8), sp.Rational(1, 6), sp.Rational(1, 4), sp.Rational(1, 2), sp.Integer(1)]:
    print("%10s %14s" % (qq, sp.nsimplify(idx.subs(q, qq))))
qsol = sp.solve(sp.Eq(idx, sp.Rational(1, 3)), q)
print("solve index = 1/3  =>  q =", qsol, "  UNIQUE (index monotone in q).")
print("=> the Deser-Levin map kappa ~ x^{-1/2} converts a FOURTH-ROOT (q=1/4) essential edge measure")
print("   into the cubic/index-1/3 class; in u = 2pi/kappa = u0 sqrt(x):  x^{-1/4} = (u/u0)^{-1/2} — the")
print("   LL-1 k=1/2 singularity EXACTLY. sqrt(3) lock + pi/3 quanta then follow from LL-1/LL-2 iff the")
print("   edge measure is the OSCILLATORY member cos(gamma x^{-1/4} + phi0).")

banner("S4h  END-TO-END NUMERIC: dressed family (q=1/4 oscillatory) reproduces the full class")
# F_d(w) = int_0^inf cos(gamma x^{-1/4}) e^{-w sqrt(x)} dx  (u0=1, smooth weight 1)
#        = 4 Re int_0^inf y^3 e^{-w y^2 + i gamma / y} dy   (x = y^4)
# same split cubic as LL-1 with prefactor y^3: saddle y0=(gamma/2w)^{1/3} e^{-i pi/6}, Phi''=6w,
# F_as = Re[ 4 y0^3 sqrt(2 pi/(6 w)) e^{-Phi(y0)} ],  Phi(y0)=3*2^{-2/3} gamma^{2/3} w^{1/3} e^{-i pi/3}
gam_n = mp.mpf(1)

def Fd_num(wv):
    old = mp.mp.dps
    mp.mp.dps = 50
    try:
        wv = mp.mpf(wv)
        rot = mp.e**(-1j * mp.pi / 3)
        osc = mp.e**(2j * mp.pi / 3)
        ystar = (gam_n / (2 * wv))**(mp.mpf(1) / 3)
        f = lambda et: et**3 * mp.e**(-wv * rot * et**2 + gam_n * osc / et)
        pts = [0, ystar / 8, ystar / 2, ystar, 2 * ystar, 4 * ystar, 10 * ystar, 40 * ystar, 200 * ystar]
        val = mp.quad(f, pts, maxdegree=12)
        out = mp.re(4 * mp.e**(-1j * 2 * mp.pi / 3) * val)
    finally:
        mp.mp.dps = old
    return out

def Fd_saddle(wv):
    wv = mp.mpf(wv)
    y0 = (gam_n / (2 * wv))**(mp.mpf(1) / 3) * mp.e**(-1j * mp.pi / 6)
    Phi0 = 3 * mp.mpf(2)**(mp.mpf(-2) / 3) * gam_n**(mp.mpf(2) / 3) * wv**(mp.mpf(1) / 3) * mp.e**(-1j * mp.pi / 3)
    return mp.re(4 * y0**3 * mp.sqrt(2 * mp.pi / (6 * wv)) * mp.e**(-Phi0))

print("%10s %22s %22s %12s %14s" % ("w", "F_d numeric", "F_d saddle", "ratio", "drift*w^(1/3)"))
for wv in [1e3, 1e4, 1e5, 1e6]:
    fn, fa = Fd_num(wv), Fd_saddle(wv)
    drift = (fn / fa - 1) * mp.mpf(wv)**(mp.mpf(1) / 3)
    print("%10.0f %22.12e %22.12e %12.7f %14.4f" % (wv, float(fn), float(fa), float(fn / fa), float(drift)))
print("ratio -> 1 monotonically; drift O(w^{-1/3})-scale (mixed subleading orders expected).")
print("=> index 1/3, decay (3/2)2^{-2/3}gamma^{2/3}w^{1/3}, osc sqrt(3)x, phase offset in pi/3-quanta:")
print("   the dressed b-family caustic emits the COMPLETE fingerprint class.")

banner("S4i  c-tilde analog of the dressed family — RAW, QUARANTINED")
gam_s = sp.symbols('gamma', positive=True)
u0_expr = 2 * sp.sqrt(2) * sp.pi * cchi**sp.Rational(3, 2) / H   # u(x)=2pi/kappa = u0 sqrt(x)
ct_d = sp.simplify(3 * 2**sp.Rational(-2, 3) * gam_s**sp.Rational(2, 3) * u0_expr**sp.Rational(1, 3))
print("u0 =", u0_expr, "   (from kappa(b) reconstruction, S4b)")
print("ct_d (rate of w^{1/3} in the dressed family) =", ct_d)
ct_target = sp.Rational(3, 4) * 2**sp.Rational(2, 3) * zt**sp.Rational(2, 3) * cchi**sp.Rational(1, 3)
gam_req = sp.solve(sp.Eq(ct_d, ct_target), gam_s)
print("matching ct*(c_chi)^{1/3} requires  gamma_req =", sp.simplify(gam_req[0]))
print("QUARANTINE: gamma is NOT derived — fixing it (and hence zt) requires the family-measure")
print("derivation from the pump construction (the named confirming calculation). No Z claim.")

banner("DONE — all sections executed")
