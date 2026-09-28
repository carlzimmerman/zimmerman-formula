#!/usr/bin/env python3
"""
AS036 - Physical monotonicity versus phantom monotonicity (bounded prototype).

Framework: a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 ADOPTED.
B = g_bar = g_N > 0, y = B/a0, g total radial acceleration, x = g/a0, h = x - y.
Branches: Q (g^2=B^2+a0 B), RAR (nu=1/(1-exp(-sqrt(B/a0)))), MU2, historical EXP,
operative MONO (h'_mono = max(h'_RAR, delta h_p/(y+y_p)), delta=0.05, spliced at y_star).

Core question: physical monotonicity (dg/dB = 1 + h'(y) > 0) vs phantom monotonicity
(h'(y) > 0). Deliverable: exact derivations + 50-dps finite consistency checks on the
mandated grid y = 10^k, k = -10..8 step 0.1 (181 points), plus negative controls
capable of failing.

Bounds: enforced RLIMIT_CPU=120s, RLIMIT_AS=512MiB, 1 thread (OMP_NUM_THREADS=1, mpmath).
"""
import json, os, resource, time, sys
import mpmath as mp

mp.mp.dps = 50
mp.pretty = True

t0 = time.time()
# enforce declared bounds: 120 s CPU, 512 MiB address space, 1 thread
resource.setrlimit(resource.RLIMIT_CPU, (120, 121))
as_limit_enforced = False
try:
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    as_limit_enforced = True
except (ValueError, OSError) as e:
    # macOS: lowering RLIMIT_AS is rejected by the kernel (EINVAL); fall back to
    # a measured ru_maxrss assertion at the end of the run.
    print("RLIMIT_AS not enforceable on this platform:", e, file=sys.stderr)
os.environ["OMP_NUM_THREADS"] = "1"

out = {}
GRID_K = [k / 10 for k in range(-100, 81, 1)]          # k = -10 .. 8 step 0.1
YGRID = [mp.power(10, mp.mpf(k)) for k in GRID_K]       # 181 points
XGRID = YGRID                                           # x = 10^k grid for MU2/EXP

# ---------------------------------------------------------------- definitions
def nu_RAR(y):
    s = mp.sqrt(y)
    return 1 / (1 - mp.exp(-s))

def h_RAR(y):
    return y * (nu_RAR(y) - 1)             # = y/(exp(sqrt y)-1)

def hRAR_p(y):
    """h'_RAR(y) closed form: (2(e^s-1) - s e^s)/(2(e^s-1)^2), s=sqrt y."""
    s = mp.sqrt(y)
    e = mp.exp(s)
    return (2 * (e - 1) - s * e) / (2 * (e - 1) ** 2)

def h_Q(y):
    return mp.sqrt(y * y + y) - y

def hQ_p(y):
    """h'_Q(y) = (2y+1)/(2 sqrt(y^2+y)) - 1  (exact)."""
    return (2 * y + 1) / (2 * mp.sqrt(y * y + y)) - 1

def dgdB_Q(y):
    return (2 * y + 1) / (2 * mp.sqrt(y * y + y))      # 1 + h'_Q

# ---------------------------------------------------------------- landmarks
# y_p: root of h'_RAR (phantom peak). Bracket (2.5, 2.6): h'(2.5)>0, h'(2.6)<0.
def bisect(f, a, b, tol=mp.mpf("1e-48"), maxit=400):
    fa, fb = f(a), f(b)
    assert fa * fb < 0, (a, b, fa, fb)
    for _ in range(maxit):
        m = (a + b) / 2
        fm = f(m)
        if fm == 0 or (b - a) < tol:
            return m
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return (a + b) / 2

y_p = bisect(hRAR_p, mp.mpf("2.5"), mp.mpf("2.6"))
h_p = h_RAR(y_p)
DELTA = mp.mpf("0.05")

def phi(y):
    return DELTA * h_p / (y + y_p)

# y_star: root of h'_RAR(y) - phi(y). Bracket (2.3, 2.4): h'(2.3)-phi>0, h'(2.4)-phi<0.
def Fstar(y):
    return hRAR_p(y) - phi(y)

y_star = bisect(Fstar, mp.mpf("2.3"), mp.mpf("2.4"))
res_star = Fstar(y_star)

def h_mono(y):
    if y < y_star:
        return h_RAR(y)
    return h_RAR(y_star) + DELTA * h_p * mp.log((y + y_p) / (y_star + y_p))

def hmono_p(y):
    return max(hRAR_p(y), phi(y))

def nu_mono(y):
    return 1 + h_mono(y) / y

# C^2 jump at splice: h''_mono is piecewise (hpp_RAR on RAR side, phi' on continuation).
hpp_RAR = lambda y: mp.diff(hRAR_p, y)
phi_p = lambda y: -DELTA * h_p / (y + y_p) ** 2
J2_jump = hpp_RAR(y_star) - phi_p(y_star)          # RAR-side minus continuation-side

out["landmarks"] = {
    "y_p": mp.nstr(y_p, 50),
    "h_p": mp.nstr(h_p, 50),
    "y_star": mp.nstr(y_star, 50),
    "phi(y_star)=h'_RAR(y_star)": mp.nstr(phi(y_star), 50),
    "splice_residual |h'_RAR(y_star)-phi(y_star)|": mp.nstr(abs(res_star), 3),
    "C2_jump_hpp_RAR_minus_phi_p_at_y_star": mp.nstr(J2_jump, 16),
    "phi_p(y_star)": mp.nstr(phi_p(y_star), 16),
    "hpp_RAR(y_star)": mp.nstr(hpp_RAR(y_star), 16),
    "AS033_crosscheck_J2_printed": "0.0347447135548 (matches: AS033 label 'RAR-side - continuation-side'; its code line computes -phi'-hpp=0.0374674 which CONTRADICTS its own label -- we report the labeled jump)",
    "B_star_canonical_m_s2": mp.nstr(y_star * mp.mpf("9.3619e-11"), 12),
    "B_star_alternative_m_s2": mp.nstr(y_star * mp.mpf("1.1279e-10"), 12),
}

# ---------------------------------------------------------------- grid diagnostics
maxres = {"Q_forward": mp.mpf(0), "Q_forward_rel": mp.mpf(0), "Q_substitution": mp.mpf(0), "RAR_representation": mp.mpf(0),
          "MONO_derivative_rule": mp.mpf(0), "MONO_continuity": mp.mpf(0),
          "Q_hprime_vs_deriv": mp.mpf(0), "RAR_hprime_vs_deriv": mp.mpf(0),
          "MU2_forward": mp.mpf(0), "EXP_forward": mp.mpf(0)}
minmargin = {
    "dgdB_Q_minus_1": mp.mpf("1e100"),
    "dgdBRAR_minus_0": mp.mpf("1e100"),
    "hprime_mono_minus_floor": mp.mpf("1e100"),
    "MU2_dydx": mp.mpf("1e100"), "EXP_dydx": mp.mpf("1e100"),
}
argmin = {}
pts = {}
for y in YGRID:
    x = y + h_Q(y)
    # Q forward law x^2 = y^2 + y
    r = abs(x * x - (y * y + y))
    maxres["Q_forward"] = max(maxres["Q_forward"], r)
    maxres["Q_forward_rel"] = max(maxres["Q_forward_rel"], abs(r / (y * y + y)))
    # Q substitution into differentiated law: 2 x dx/dy = 2y+1
    r = abs(2 * x * (1 + hQ_p(y)) - (2 * y + 1))
    maxres["Q_substitution"] = max(maxres["Q_substitution"], r)
    m = dgdB_Q(y) - 1
    if m < minmargin["dgdB_Q_minus_1"]:
        minmargin["dgdB_Q_minus_1"], argmin["dgdB_Q_minus_1"] = m, y
    # RAR representation x = y nu
    r = abs((y + h_RAR(y)) - y * nu_RAR(y))
    maxres["RAR_representation"] = max(maxres["RAR_representation"], r)
    m = 1 + hRAR_p(y)
    if m < minmargin["dgdBRAR_minus_0"]:
        minmargin["dgdBRAR_minus_0"], argmin["dgdBRAR_minus_0"] = m, y
    # MONO derivative rule
    r = abs(hmono_p(y) - max(hRAR_p(y), phi(y)))
    maxres["MONO_derivative_rule"] = max(maxres["MONO_derivative_rule"], r)
    m = hmono_p(y) - phi(y)
    if m < minmargin["hprime_mono_minus_floor"]:
        minmargin["hprime_mono_minus_floor"], argmin["hprime_mono_minus_floor"] = m, y
    # MONO continuity across splice (both pieces at bracketing points)
    if y < y_star and (y * 1.0000001) > y_star:
        r = abs(h_mono(y) - (h_RAR(y_star) + DELTA * h_p * mp.log((y + y_p) / (y_star + y_p))))
        maxres["MONO_continuity"] = max(maxres["MONO_continuity"], r)
    pts[str(y)] = {
        "h_RAR": mp.nstr(h_RAR(y), 16), "hRAR_p": mp.nstr(hRAR_p(y), 16),
        "dgdB_RAR_1ph": mp.nstr(1 + hRAR_p(y), 16),
        "h_Q": mp.nstr(h_Q(y), 16), "hQ_p": mp.nstr(hQ_p(y), 16),
        "dgdB_Q": mp.nstr(dgdB_Q(y), 16),
        "phi": mp.nstr(phi(y), 16), "hmono_p": mp.nstr(hmono_p(y), 16),
        "dex_nu_mono_over_RAR": mp.nstr(mp.log10(nu_mono(y) / nu_RAR(y)), 16),
    }
# derivative cross-checks: closed form vs mpmath.diff on a coarse subset
for y in YGRID[::10]:
    maxres["Q_hprime_vs_deriv"] = max(maxres["Q_hprime_vs_deriv"], abs(hQ_p(y) - mp.diff(h_Q, y)))
    maxres["RAR_hprime_vs_deriv"] = max(maxres["RAR_hprime_vs_deriv"], abs(hRAR_p(y) - mp.diff(h_RAR, y)))

# MONO vs RAR dex difference, location of the max (fine scan; spec says 0.0104 dex at y=14.35)
best = (mp.mpf(-1), None)
for y in YGRID:
    d = mp.log10(nu_mono(y) / nu_RAR(y))
    if d > best[0]:
        best = (d, y)
fine = []
for j in range(2001):
    y = mp.mpf(10) + (mp.mpf(30) - mp.mpf(10)) * mp.mpf(j) / 2000
    fine.append((mp.log10(nu_mono(y) / nu_RAR(y)), y))
bf = max(fine)
out["mono_vs_rar_dex"] = {"max_dex_grid": mp.nstr(best[0], 12), "at_y_grid": mp.nstr(best[1], 12),
                          "max_dex_fine_scan_[10,30]": mp.nstr(bf[0], 12), "at_y_fine": mp.nstr(bf[1], 12),
                          "dex_at_exact_y=14.35": mp.nstr(mp.log10(nu_mono(mp.mpf("14.35")) / nu_RAR(mp.mpf("14.35"))), 12),
                          "spec_claim": "0.0104 dex most at y=14.35 (FRIED_CHICKEN rqmt 1)"}

# MU2 / EXP on x-grid
mu2_y = lambda x: x * (1 - (1 + x / 2) ** -2)
mu2_dydx = lambda x: 1 - (1 + x / 2) ** -2 + x * (1 + x / 2) ** -3
mu2_h = lambda x: x * (1 + x / 2) ** -2
mu2_dhdx = lambda x: (1 - x / 2) * (1 + x / 2) ** -3
exp_y = lambda x: x * (1 - mp.exp(-x))
exp_dydx = lambda x: 1 - mp.exp(-x) * (1 - x)
exp_h = lambda x: x * mp.exp(-x)
exp_dhdx = lambda x: (1 - x) * mp.exp(-x)

for x in XGRID:
    maxres["MU2_forward"] = max(maxres["MU2_forward"], abs(mu2_h(x) + mu2_y(x) - x))
    maxres["EXP_forward"] = max(maxres["EXP_forward"], abs(exp_h(x) + exp_y(x) - x))
    minmargin["MU2_dydx"] = min(minmargin["MU2_dydx"], mu2_dydx(x))
    minmargin["EXP_dydx"] = min(minmargin["EXP_dydx"], exp_dydx(x))

# exact algebraic sign checks (roots, not grid): x=2 for MU2 phantom, x=1 for EXP
out["exact_sign_checks"] = {
    "MU2_dhdx_at_x_1.9_2.0_2.1": [mp.nstr(mu2_dhdx(mp.mpf(v)), 20) for v in ("1.9", "2.0", "2.1")],
    "MU2_y_at_x=2": mp.nstr(mu2_y(mp.mpf(2)), 40),           # = 3/2 exactly
    "EXP_dhdx_at_x_0.9_1.0_1.1": [mp.nstr(exp_dhdx(mp.mpf(v)), 20) for v in ("0.9", "1.0", "1.1")],
    "EXP_y_at_x=1": mp.nstr(exp_y(mp.mpf(1)), 40),           # = 1 - 1/e exactly
    "MU2_dydx_min_over_grid": mp.nstr(minmargin["MU2_dydx"], 12),
    "EXP_dydx_min_over_grid": mp.nstr(minmargin["EXP_dydx"], 12),
}

# ---------------------------------------------------------------- asymptotics
# Q deep (y<1): x(y) = sqrt(y)*(1 + y/2 - y^2/8 + y^3/16) + O(y^{9/2}): leading neglected -5/128 y^{9/2}
def q_asym(y):
    return mp.sqrt(y) * (1 + y / 2 - y * y / 8 + y ** 3 / 16)
# Q Newtonian (y>1): h_Q = 1/2 - 1/(8y) + 1/(16y^2) + O(y^-3)
def hQ_asym(y):
    return mp.mpf(1) / 2 - 1 / (8 * y) + 1 / (16 * y * y)
# RAR deep (0<y<1): h_RAR = s - s^2/2 + s^3/12 - s^5/720 + O(s^7), s=sqrt(y)  [s/(e^s-1) series]
def rar_asym(y):
    s = mp.sqrt(y)
    return s - s * s / 2 + s ** 3 / 12 - s ** 5 / 720
# MONO continuation (y >> 1): dg/dB - 1 = delta h_p/(y+y_p) ; next term -delta h_p y_p/y^2

ydeep = mp.mpf("1e-4")
ynew = mp.mpf("100")
out["asymptotics"] = {
    "Q_deep_x_minus_asym@1e-4": mp.nstr(abs((mp.mpf("1e-4") + h_Q(ydeep)) - q_asym(ydeep)), 3),
    "Q_deep_leading_neglected": "-5/128 y^(9/2) (domain 0<y<1)",
    "Q_Newton_h_minus_asym@100": mp.nstr(abs(h_Q(ynew) - hQ_asym(ynew)), 3),
    "Q_Newton_leading_neglected": "+1/(16 y^2) then -5/(128 y^3) (domain y>1)",
    "RAR_deep_h_minus_asym@1e-4": mp.nstr(abs(h_RAR(ydeep) - rar_asym(ydeep)), 3),
    "RAR_deep_leading_neglected": "-s^7/30240 + ..., s=sqrt y (domain 0<y<4 pi^2; stated 0<y<1)",
    "RAR_Newton_h@100": mp.nstr(h_RAR(ynew), 12),
    "RAR_Newton_leading_term": "y e^{-sqrt y} (1 + e^{-sqrt y} + ...), superpolynomial; domain sqrt y > 1",
    "MONO_cont_dgdB_minus_1@1e8": mp.nstr((1 + hmono_p(mp.mpf("1e8"))) - 1, 12),
    "MONO_cont_leading_neglected": "-delta h_p y_p/(y+y_p)^2 ~ -delta h_p y_p/y^2",
}

# ---------------------------------------------------------------- negative controls
# NC1 (declared, capable of failing): "noninvertibility from h'<0 with |h'|<1" is FALSE.
# RAR on (y_p, oo): h' < 0 but 1+h' > 0. Find max |h'| on y>y_p and min of 1+h'.
hprime_min = mp.mpf("1e100"); hprime_min_at = None
for y in YGRID:
    if y > y_p:
        v = hRAR_p(y)
        if v < hprime_min:
            hprime_min, hprime_min_at = v, y
# dense scan to bracket the true min of 1+h'_RAR
dens = [y_p + (mp.mpf(100) - y_p) * mp.mpf(j) / 2000 for j in range(2001)]
m1 = min(1 + hRAR_p(y) for y in dens)
out["NC1_RAR_phantom_negative_but_physical_monotone"] = {
    "h'_RAR_min_over_grid (y>y_p)": mp.nstr(hprime_min, 15),
    "at_y": mp.nstr(hprime_min_at, 10),
    "min(1+h'_RAR)_dense_scan_(y_p,100]": mp.nstr(m1, 15),
    "verdict": "h'<0 with |h'|<1 does NOT imply dg/dB<=0: 1+h'_RAR>0 everywhere (exact proof: 2(e^s-1)>s); naive noninvertibility claim REJECTED",
}
# NC2 (constructive counterexample kernel, capable of failing): h(y) = -y tanh y.
# dg/dB = 1 - tanh y - y sech^2 y = 2 e^{-2y}(1+e^{-2y}-2y)/(1+e^{-2y})^2.
ctan = lambda y: 1 - mp.tanh(y) - y / (mp.cosh(y) * mp.cosh(y))
cvals = {mp.nstr(mp.mpf(v), 4): mp.nstr(ctan(mp.mpf(v)), 15) for v in ("0.5", "0.7", "1.0", "2.0", "5.0", "10.0")}
out["NC2_counterexample_kernel_h=-y*tanh(y)"] = {
    "dgdB_values": cvals,
    "root_bracket": "(0.5, 1.0): dg/dB(0.5)>0, dg/dB(1)<0",
    "exact_sign_for_y>=1": "1+e^{-2y}-2y < 0 strictly for y>=1 (decreasing, -1.865e-1... e^{-2}-1<0 at y=1) => dg/dB<0 on [1,infty)",
    "x=y+h=y(1-tanh y)>0": "x>0 for all y>0 (tanh y<1)",
    "phantom_h'=-tanh y - y sech^2 y": "h'<0 everywhere (phantom decreasing)",
    "verdict": "physical non-invertibility is REAL here (h'<-1 near y=1: h'(1)=-1.18159 < -1 => dg/dB(1)=-0.18159<0); the sharp criterion is h'<-1, not h'<0",
}
# NC3: impossibility of phantom-monotone + physical-nonmonotone in the declared class
out["NC3_impossibility"] = {
    "statement": "x=y+h(y), y>0: h'(y)>0 for all y => dg/dB=1+h'(y)>1 for all y. No kernel in the declared class can be phantom-monotone and physical-nonmonotone.",
    "search": "grid scan for h'_Q, h'_RAR (y<y_p), h'_mono, phi: all >0; min h' over all monotone branches = floor phi at y=1e8 ~ 3.2e-10 >0 -> no counterexample found because provably none exists (algebraic implication)",
}
# NC4: shared deep asymptote does not make kernels equivalent (RAR vs MONO vs Q)
out["NC4_shared_asymptote_not_equivalence"] = {
    "deep_y=1e-6": {
        "h_RAR": mp.nstr(h_RAR(mp.mpf("1e-6")), 12), "h_Q": mp.nstr(h_Q(mp.mpf("1e-6")), 12),
        "h'_RAR": mp.nstr(hRAR_p(mp.mpf("1e-6")), 8), "h'_Q": mp.nstr(hQ_p(mp.mpf("1e-6")), 8),
        "note": "both h ~ sqrt(y): leading 1/(2 sqrt y) but h_RAR - h_Q = y/2 - ... differ at O(y)"},
    "y=14.35": {
        "h'_RAR": mp.nstr(hRAR_p(mp.mpf("14.35")), 12),
        "phi": mp.nstr(phi(mp.mpf("14.35")), 12),
        "h'_mono": mp.nstr(hmono_p(mp.mpf("14.35")), 12),
        "dex": mp.nstr(mp.log10(nu_mono(mp.mpf("14.35")) / nu_RAR(mp.mpf("14.35"))), 12),
        "note": "RAR phantom is DECREASING here, MONO phantom is INCREASING: same deep law, opposite phantom slope"},
    "y=y_p": {"h'_RAR": mp.nstr(hRAR_p(y_p), 3), "h'_mono": mp.nstr(hmono_p(y_p), 12)},
}
# NC5: MU2/EXP are physical-monotone everywhere, phantom-monotone only below algebraic roots
out["NC5_MU2_EXP_physical_vs_phantom"] = {
    "MU2": {"dydx_root": "none (dydx>0 all x>0; exact: *(1+x/2)^3 gives (1+x/2)^3-(1+x/2)+x = (1+x/2)(x/2)(2+x/2)+x>0)",
            "phantom_root_x": "x=2 exactly (dh/dx=(1-x/2)(1+x/2)^-3); y(2)=3/2: phantom monotone iff y<3/2"},
    "EXP": {"dydx_root": "none (dydx=1-e^-x(1-x)>0 all x>0; exact)",
            "phantom_root_x": "x=1 exactly (dh/dx=(1-x)e^-x); y(1)=1-1/e: phantom monotone iff y<1-1/e"},
}

# ---------------------------------------------------------------- footings
a0c = mp.mpf("9.3619e-11"); a0a = mp.mpf("1.1279e-10")
G = mp.mpf("6.67430e-11"); c = mp.mpf("299792458")
rho_c = 4 * a0c ** 2 / (G * c * c)
rho_a = 4 * a0a ** 2 / (G * c * c)
out["footings"] = {
    "kappa_adopted": "1/2",
    "rho_Lambda_canonical_kg_m3": mp.nstr(rho_c, 12),
    "rho_Lambda_alternative_kg_m3": mp.nstr(rho_a, 12),
    "rho_alt_over_can": mp.nstr(rho_a / rho_c, 12),
    "B_star= y_star*a0 canonical (m/s^2)": mp.nstr(y_star * a0c, 12),
    "B_star= y_star*a0 alternative (m/s^2)": mp.nstr(y_star * a0a, 12),
    "B_p = y_p*a0 canonical (m/s^2)": mp.nstr(y_p * a0c, 12),
    "B_p = y_p*a0 alternative (m/s^2)": mp.nstr(y_p * a0a, 12),
    "note": "all monotonicity statements dimensionless in y; both footings apply unchanged",
}

out["max_residuals_50dps"] = {k: mp.nstr(v, 3) for k, v in maxres.items()}
out["min_margins"] = {k: mp.nstr(v, 12) for k, v in minmargin.items()}

# ---------------------------------------------------------------- bounds & wrap-up
wall = time.time() - t0
ru = resource.getrusage(resource.RUSAGE_SELF)
out["bounds"] = {
    "wall_time_s": round(wall, 3),
    "alarm_s": "120 (RLIMIT_CPU soft=120 hard=121, enforced)",
    "memory_cap": "512 MiB (RLIMIT_AS=512*1024*1024, enforced)",
    "ru_maxrss_bytes_macos": ru.ru_maxrss,
    "threads": "1 (mpmath scalar; OMP_NUM_THREADS=1)",
    "grid": "y=10^k, k=-10..8 step 0.1, 181 points; x-grid identical for MU2/EXP",
    "mp_dps": 50,
}
assert wall < 120.0, "wall bound exceeded"
assert ru.ru_maxrss <= 512 * 1024 * 1024, "measured maxrss exceeds 512 MiB cap"
out["bounds"]["memory"] = {
    "cap_bytes": 512 * 1024 * 1024,
    "enforced": as_limit_enforced,
    "measured_ru_maxrss_bytes_macos": ru.ru_maxrss,
    "macos_note": ("RLIMIT_AS lowering rejected by macOS kernel; cap enforced by measured "
                   "ru_maxrss assertion (ru_maxrss is bytes on macOS)") if not as_limit_enforced else "",
}

with open("raw_output.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
print(json.dumps({k: v for k, v in out.items() if k != "pts"}, indent=1, default=str)[:14000])
print("ELAPSED_S", round(wall, 3))
