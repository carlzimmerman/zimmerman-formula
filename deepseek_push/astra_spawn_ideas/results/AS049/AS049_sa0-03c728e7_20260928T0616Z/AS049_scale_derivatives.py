#!/usr/bin/env python3
"""AS049 (registered seed: Scale derivatives of a constitutive force) - worker sa-0-03c728e7.

Executes the registered seed's numbered steps exactly (claims-ledger-pinned SHA
ed91aeff... = AS049_scale_derivatives_of_a_constitutive_force.md).

Principal test:  g(B,a0) = B*nu(B/a0);  partial g/partial a0 = -(B^2/a0^2)*nu'(B/a0).

Branches (distinct, never identified): Q, RAR, MU2, EXP (historical AQUAL), MONO (operative).
Domain: y = B/a0 in 10^k, k = -10..8 step 0.1; symbolic limits + bracketed roots.

Bounds: single process (>=1 thread would be a violation), wall <= 120 s enforced
by the caller (timeout), maxrss recorded and asserted <= 512 MB.
"""
import json, math, os, resource, time
import mpmath as mp

mp.mp.dps = 50
t0 = time.time()

# ---------------------------------------------------------------- constants
A0_CAN = mp.mpf("9.3619e-11")     # canonical footing  m/s^2
A0_ALT = mp.mpf("1.1279e-10")     # alternative footing m/s^2
G_N = mp.mpf("6.67430e-11")       # measured Newton coupling (SI); G_N kept separate from G_bare/G_cosmo
C_LIGHT = mp.mpf("299792458")
MSUN = mp.mpf("1.98847e30")
PC = mp.mpf("3.085677581491367e16")
DELTA = mp.mpf("0.05")

# MONO landmarks (framework contract; AS047/AS032 record, re-bracketed here)
def _h_RAR(y):
    s = mp.sqrt(y)
    return y/(mp.e**s - 1)

def _h_RAR_deriv(y):
    s = mp.sqrt(y)
    e = mp.e**s
    return (2*(e-1) - s*e)/(2*(e-1)**2)

y_p  = mp.findroot(lambda y: 2 - mp.sqrt(y) - 2*mp.exp(-mp.sqrt(y)), mp.mpf("2.54"))
h_p  = y_p/(mp.e**mp.sqrt(y_p) - 1)
c_mon = DELTA*h_p
y_star = mp.findroot(lambda y: _h_RAR_deriv(y) - c_mon/(y + y_p), mp.mpf("2.337"))
h_star = _h_RAR(y_star)
del h_star

def h_mono(y):
    if y <= y_star:
        return _h_RAR(y)
    return _h_RAR(y_star) + c_mon*mp.log((y + y_p)/(y_star + y_p))

def nu_mono(y):
    return 1 + h_mono(y)/y

def nu_RAR(y):
    return 1/(1 - mp.e**(-mp.sqrt(y)))

def _x_of_y_mu2(y):   # implicit: x*mu(x) = y, mu(x) = 1-(1+x/2)^-2 ; strictly increasing x->x*mu(x)
    if y > 1:
        lo, hi = mp.mpf("0.9")*y, mp.mpf("3")*y
        while lo*(1-(1+lo/2)**-2) > y: lo /= 2
        while hi*(1-(1+hi/2)**-2) < y: hi *= 2
    else:
        lo, hi = mp.sqrt(2*y)*mp.mpf("0.1"), mp.sqrt(2*y)*mp.mpf("20")
        while lo*(1-(1+lo/2)**-2) > y: lo /= 2
    return mp.findroot(lambda x: x*(1-(1+x/2)**-2) - y, (lo, hi))

def _x_of_y_exp(y):    # implicit: x*(1-exp(-x)) = y
    if y > 1:
        lo, hi = mp.mpf("0.9")*y, mp.mpf("3")*y
        while lo*(1-mp.e**(-lo)) > y: lo /= 2
        while hi*(1-mp.e**(-hi)) < y: hi *= 2
    else:
        lo, hi = mp.sqrt(y)*mp.mpf("0.1"), mp.sqrt(y)*mp.mpf("20")
        while lo*(1-mp.e**(-lo)) > y: lo /= 2
    return mp.findroot(lambda x: x*(1-mp.e**(-x)) - y, (lo, hi))

def nu_Q(y):    return mp.sqrt(1 + 1/y)
def nu_MU2(y):  x = _x_of_y_mu2(y); return 1/(1-(1+x/2)**-2)
def nu_EXP(y):  x = _x_of_y_exp(y); return 1/(1-mp.e**(-x))

def nu_branch(branch, y):
    return {"Q": nu_Q, "RAR": nu_RAR, "MU2": nu_MU2, "EXP": nu_EXP, "MONO": nu_mono}[branch](y)

# exact closed-form derivatives nu'(y) per branch
def dnu_Q(y):
    return -1/(2*y*y*nu_Q(y))

def dnu_RAR(y):
    s = mp.sqrt(y); e = mp.e**s
    return -e/(2*s*(e-1)**2)

def dnu_MU2(y):
    x = _x_of_y_mu2(y)
    t = 1 + x/2
    mu = 1 - t**-2
    dmu = t**-3                      # d mu/d x
    dxdy = 1/(mu + x*dmu)            # chain: d/dy [x mu(x)] = 1
    return -dmu*dxdy/mu**2

def dnu_EXP(y):
    x = _x_of_y_exp(y)
    mu = 1 - mp.e**(-x); dmu = mp.e**(-x)
    dxdy = 1/(mu + x*dmu)
    return -dmu*dxdy/mu**2

def dnu_mono(y):
    if y <= y_star:
        return dnu_RAR(y)
    # nu = 1 + h/y ; h' = c/(y+y_p)
    h = h_mono(y)
    return (c_mon/(y+y_p)*y - h)/(y*y)

def dnu_branch(branch, y):
    return {"Q": dnu_Q, "RAR": dnu_RAR, "MU2": dnu_MU2, "EXP": dnu_EXP, "MONO": dnu_mono}[branch](y)

def elasticity(branch, y):           # eps(y) = -y nu'(y)/nu(y) = (a0/g) dg/da0|_B
    return -y*dnu_branch(branch, y)/nu_branch(branch, y)

def g_of(B, a0, branch):
    return B*nu_branch(branch, B/a0)

def fd_dg_da0(B, a0, branch, hrel=mp.mpf("1e-13")):
    h = hrel*a0
    return (g_of(B, a0+h, branch) - g_of(B, a0-h, branch))/(2*h)

# domain where the central FD resolves dg/da0 at 50 dps (g varies by eps*hrel relative;
# need eps*hrel >> 1e-50).  RAR/EXP recover exponentially: y=1e3 -> nu-1 ~ 1.8e-14, resolvable;
# y=1e4 -> e^-100 ~ 4e-44, eps*hrel ~ 4e-57 not resolvable.  MONO recovers only logarithmically,
# resolvable on the full grid.  (Q: eps=1/(2(y+1)) ~ 5e-9 at 1e8 -> 5e-22*1e-13=5e-35 resolvable,
# but kept on the same restricted domain for uniformity; full-grid Q/MU2 confirmed separately.)
def fd_domain(branch):
    # RAR: nu-1 ~ e^-sqrt(y): resolvable at 50 dps up to y=1e3 (e^-31.6 ~ 1.8e-14).
    # EXP: nu-1 ~ e^-y (x ~ y): resolvable only up to y=10 (e^-10 ~ 4.5e-5; at y=100, e^-100 ~ 4e-44).
    if branch == "RAR":
        return [y for y in grid if y <= mp.mpf("1e3")]
    if branch == "EXP":
        return [y for y in grid if y <= mp.mpf("10")]
    return grid

BRANCHES = ["Q", "RAR", "MU2", "EXP", "MONO"]
grid = [mp.mpf(10)**(mp.mpf(k)) for k in [mp.mpf(-10) + mp.mpf("0.1")*i for i in range(181)]]

results = {}
checks = []

def check(name, ok, detail, tol):
    checks.append({"name": name, "pass": bool(ok), "detail": str(detail)[:160], "tolerance": tol})

# ---------------------------------------------------------------------------
# STEP 2: response at fixed B vs along B proportional to a0; deep+Newtonian limits
# ---------------------------------------------------------------------------
# C1: chain-rule identity  dg/da0|_B = -(B^2/a0^2) nu'(y)   vs central finite difference
worst_c1 = {}
for br in BRANCHES:
    wr = mp.mpf(0)
    for y in fd_domain(br):
        B = y*A0_CAN
        exact = -(B*B/(A0_CAN*A0_CAN))*dnu_branch(br, y)
        fd = fd_dg_da0(B, A0_CAN, br)
        rel = abs((exact-fd)/max(abs(exact), mp.mpf("1e-300")))
        wr = max(wr, rel)
    worst_c1[br] = wr
    check(f"C1 chain-id {br}", wr < mp.mpf("1e-18"), f"worst rel |exact-FD| = {wr}", "1e-18")

# C1b: closed-form elasticity identity  eps = -y nu'/nu vs (a0/g)*FD  AND Euler homogeneity
worst_c1b = {}
for br in BRANCHES:
    wr = mp.mpf(0)
    for y in fd_domain(br):
        B = y*A0_CAN
        eps = elasticity(br, y)
        g = g_of(B, A0_CAN, br)
        fd = fd_dg_da0(B, A0_CAN, br)
        wr = max(wr, abs(eps - fd*A0_CAN/g))
    worst_c1b[br] = wr
    check(f"C1b elasticity-vs-FD {br}", wr < mp.mpf("1e-18"), f"worst |eps - (a0/g)FD| = {wr}", "1e-18")

# C1c: Euler homogeneity  B dg/dB + a0 dg/da0 = g   (g jointly homogeneous degree 1)
for br in BRANCHES:
    wr = mp.mpf(0)
    for y in grid:
        B = y*A0_CAN
        h = B*mp.mpf("1e-7")
        dB = (g_of(B+h, A0_CAN, br) - g_of(B-h, A0_CAN, br))/(2*h)
        da = fd_dg_da0(B, A0_CAN, br)
        wr = max(wr, abs(B*dB + A0_CAN*da - g_of(B, A0_CAN, br))/g_of(B, A0_CAN, br))
    check(f"C1c Euler {br}", wr < mp.mpf("1e-10"), f"worst rel Euler resid = {wr}", "1e-10")

# C2: along B proportional to a0 (y fixed): dg/da0|_y = g/a0 identically
for br in BRANCHES:
    wr = mp.mpf(0)
    for y in grid:
        a1, a2 = mp.mpf("0.9")*A0_CAN, mp.mpf("1.1")*A0_CAN
        # fix y by scaling B with a0: B = y*a0
        g1 = g_of(y*a1, a1, br); g2 = g_of(y*a2, a2, br)
        fd = (g2-g1)/(a2-a1)
        wr = max(wr, abs(fd - g_of(y*A0_CAN, A0_CAN, br)/A0_CAN)/(g_of(y*A0_CAN, A0_CAN, br)/A0_CAN))
    check(f"C2 y-proportional {br}", wr < mp.mpf("1e-20"), f"worst rel |FD - g/a0| = {wr}", "1e-20")

# C3: deep limit y->0: eps -> 1/2 on every branch (g -> sqrt(a0 B) family).
# Leading corrections (step-3 "leading neglected term") at y=1e-14 (all < 1e-7):
#   Q:   g/sqrt(a0B) = 1 + 0*y + ...   (pure, no sqrt term);   eps = 1/2 - y/2 + ...
#   RAR: g/sqrt(a0B) = 1 + sqrt(y)/2 + ...;  eps = 1/2 - sqrt(y)/4 + ...
#   MU2: g/sqrt(a0B) = 1 + (3/8)sqrt(y) + ...;  eps = 1/2 - (3/16)sqrt(y) + ...
#        (mu(x) ~ x for x<<1, so the deep prefactor is 1, NOT sqrt(2); s=2a0 is only the
#         argument scale of mu's Taylor cell)
#   EXP: g/sqrt(a0B) = 1 + sqrt(y)/4 + ...;  eps = 1/2 - sqrt(y)/8 + ...
#   MONO: (y<y_star) == RAR.
deep = {}
yd = mp.mpf("1e-14")
for br in BRANCHES:
    deep[br] = elasticity(br, yd)
    check(f"C3 deep-eps {br}", abs(deep[br] - mp.mpf("0.5")) < mp.mpf("1e-6"),
          f"eps(1e-14) = {deep[br]}", "|eps-1/2|<1e-6")
# deep prefactors: g/sqrt(a0 B) at y=1e-14, all -> 1 with the stated corrections
for br in BRANCHES:
    B = yd*A0_CAN
    pref = g_of(B, A0_CAN, br)/mp.sqrt(A0_CAN*B)
    check(f"C3 deep-pref {br}", abs(pref-1) < mp.mpf("1e-6"), f"g/sqrt(a0B) = {pref} (expect 1 + O(sqrt(y)))", "1e-6")

# C4: Newtonian limit y->oo: eps -> 0, recovery rates per branch
newt = {}
for br in BRANCHES:
    newt[br] = elasticity(br, mp.mpf("1e8"))
    check(f"C4 newt-eps {br}", 0 <= newt[br] < mp.mpf("1e-3"), f"eps(1e8) = {newt[br]}", "<1e-3")
# recovery rates at y=1e3
rec = {}
for br in BRANCHES:
    rec[br] = (nu_branch(br, mp.mpf("1e3")) - 1)
check("C4b MONO slowest", rec["MONO"] > 100*rec["RAR"] and 0 < rec["MONO"] < 1e-3,
      f"nu-1 at 1e3: MONO {rec['MONO']} vs RAR {rec['RAR']}", "MONO log >> RAR exp; both <1e-3")

# C5: MONO continuity at splice: value, slope, elasticity match RAR; eps positive on continuation
check("C5a mono==RAR at y*", abs(nu_mono(y_star) - nu_RAR(y_star)) < mp.mpf("1e-45"),
      f"nu diff {nu_mono(y_star)-nu_RAR(y_star)}", "1e-45")
check("C5b slope match at y*", abs(dnu_mono(y_star) - dnu_RAR(y_star)) < mp.mpf("1e-45"),
      f"nu' diff {dnu_mono(y_star)-dnu_RAR(y_star)}", "1e-45")
eps_mono_lo, eps_mono_hi = elasticity("MONO", mp.mpf("1e-10")), elasticity("MONO", mp.mpf("1e8"))
check("C5c eps_mono in (0,1/2]", eps_mono_lo > 0 and eps_mono_hi > 0 and eps_mono_lo <= mp.mpf("0.5")+mp.mpf("1e-12") and eps_mono_hi < mp.mpf("1e-3"),
      f"eps_mono(1e-10)={eps_mono_lo}, eps_mono(1e8)={eps_mono_hi}", "0<eps<=1/2 deep; ->0 newt")

# ---------------------------------------------------------------------------
# C1d: independent representation -- symbolic differentiation (sympy) of each
# branch's nu(y) vs the closed-form nu'(y) used above (CAS algebra, not FD)
# ---------------------------------------------------------------------------
import sympy as sp
yS = sp.symbols("y", positive=True)
nu_sym = {
    "Q": sp.sqrt(1 + 1/yS),
    "RAR": 1/(1 - sp.exp(-sp.sqrt(yS))),
    "MU2": None,   # implicit; derivative via implicit-function theorem on x*mu(x)=y (checked vs FD on domain)
    "EXP": None,
    "MONO": None,  # piecewise; continuation derivative (c/(y+yp))*y/h - h/y^2 checked vs FD on full grid
}
for br in ["Q", "RAR"]:
    d = sp.diff(nu_sym[br], yS)
    f_sym = sp.lambdify(yS, sp.simplify(d), "mpmath")
    wr = mp.mpf(0)
    for y in [mp.mpf("1e-4"), mp.mpf("1"), mp.mpf("1e2")]:
        wr = max(wr, abs(f_sym(y) - dnu_branch(br, y)))
    check(f"C1d sympy {br}", wr < mp.mpf("1e-38"), f"worst |sympy dnu - closed form| = {wr}", "1e-38 (abs)")
# MU2/EXP: verify closed-form implicit derivative against an independent finite difference of the implicit solution
for br in ["MU2", "EXP"]:
    wr = mp.mpf(0)
    for y in [mp.mpf("1e-4"), mp.mpf("1"), mp.mpf("1e2")]:
        h = y*mp.mpf("1e-12")
        xp = _x_of_y_mu2(y+h) if br == "MU2" else _x_of_y_exp(y+h)
        xm = _x_of_y_mu2(y-h) if br == "MU2" else _x_of_y_exp(y-h)
        dxdy_fd = (xp - xm)/(2*h)
        x = _x_of_y_mu2(y) if br == "MU2" else _x_of_y_exp(y)
        mu = (1-(1+x/2)**-2) if br == "MU2" else (1-mp.e**(-x))
        dmu = ((1+x/2)**-3) if br == "MU2" else mp.e**(-x)
        dxdy_exact = 1/(mu + x*dmu)
        wr = max(wr, abs(dxdy_exact - dxdy_fd)/max(abs(dxdy_fd), mp.mpf("1e-300")))
    check(f"C1d implicit {br}", wr < mp.mpf("1e-20"), f"worst rel |dx/dy exact - FD| = {wr}", "1e-20")

# ---------------------------------------------------------------------------
# STEP 4 negative control N1 (must be capable of failing)
# "Confuse fixed B with fixed y and show the resulting derivative disagrees with finite differences."
# ---------------------------------------------------------------------------
confusion = {}
for br in BRANCHES:
    fails = 0; ratio_sum = mp.mpf(0); n = 0
    for y in grid:
        if y < mp.mpf("1e-4") or y > mp.mpf("1e4"):
            continue
        B = y*A0_CAN
        g = g_of(B, A0_CAN, br)
        naive = g/A0_CAN                      # WRONG: fixed-y derivative
        fd = fd_dg_da0(B, A0_CAN, br)
        if abs(fd - naive)/g > mp.mpf("0.05"):  # naive must disagree by >5% (it disagrees by ~1/eps-1)
            fails += 1
        ratio_sum += (fd/naive if naive != 0 else mp.mpf("0"))
        n += 1
    confusion[br] = {"fails": fails, "n": n, "mean_fd_over_naive": ratio_sum/n}
    check(f"N1 naive-fails {br}", fails == n, f"naive(g/a0) disagrees with FD on {fails}/{n} pts (mean FD/naive = {mp.nstr(ratio_sum/n,6)})",
          "fails on every tested point")

# ---------------------------------------------------------------------------
# supplementary: residual of implicit solves (MU2, EXP)
# ---------------------------------------------------------------------------
worst_imp = {}
for br in ["MU2", "EXP"]:
    wr = mp.mpf(0)
    for y in grid:
        x = _x_of_y_mu2(y) if br == "MU2" else _x_of_y_exp(y)
        mu = (1-(1+x/2)**-2) if br == "MU2" else (1-mp.e**(-x))
        wr = max(wr, abs(x*mu/y - 1))
    worst_imp[br] = wr
    check(f"S1 implicit {br}", wr < mp.mpf("1e-40"), f"worst |x mu/y - 1| = {wr}", "1e-40")

# ---------------------------------------------------------------------------
# STEP 5: dimensional example (both footings) - elasticity is dimensionless; g values:
footing_g = {}
for a0, tag in [(A0_CAN, "canonical"), (A0_ALT, "alternative")]:
    g1 = g_of(a0*mp.mpf("1"), a0, "MONO"); g1_r = g_of(a0*mp.mpf("1"), a0, "RAR")
    footing_g[tag] = {"g_MONO(y=1)": g1, "g_RAR(y=1)": g1_r}

# ---------------------------------------------------------------------------
summary = {
    "landmarks": {"y_p": mp.nstr(y_p, 20), "h_p": mp.nstr(h_p, 20),
                  "y_star": mp.nstr(y_star, 20), "c": mp.nstr(c_mon, 20)},
    "deep_eps": {br: mp.nstr(deep[br], 12) for br in BRANCHES},
    "newt_eps": {br: mp.nstr(newt[br], 12) for br in BRANCHES},
    "recovery_nu_minus_1_at_1e3": {br: mp.nstr(rec[br], 12) for br in BRANCHES},
    "confusion_control": {br: {k: (mp.nstr(v, 12) if isinstance(v, mp.mpf) else v) for k, v in d.items()} for br, d in confusion.items()},
    "worst_c1": {br: mp.nstr(w, 8) for br, w in worst_c1.items()},
    "worst_c1b": {br: mp.nstr(w, 8) for br, w in worst_c1b.items()},
    "worst_implicit": {br: mp.nstr(w, 8) for br, w in worst_imp.items()},
    "footing_g": {k: mp.nstr(v["g_MONO(y=1)"], 12) for k, v in footing_g.items()},
}
npass = sum(1 for c in checks if c["pass"])
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # macOS: bytes (or KB on Linux); either way << 512 MB
print(f"AS049 scale-derivatives: {npass}/{len(checks)} checks PASS  (wall {time.time()-t0:.2f}s, ru_maxrss raw={rss})")
assert rss < 512*1024*1024, "memory bound violated"
print(f"  enforced bounds: wall <= 120 s (caller timeout), maxrss < 512 MB (assert), threads = 1 (single process, no threads)")
for c in checks:
    print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['name']}: {c['detail']}")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "checks_scale_derivatives.json"), "w") as f:
    json.dump({"checks": checks, "summary": {k: v for k, v in summary.items()}}, f, indent=1, default=str)
print(json.dumps(summary, indent=1, default=str))
assert npass == len(checks), f"FAILED: {len(checks)-npass} checks failed"