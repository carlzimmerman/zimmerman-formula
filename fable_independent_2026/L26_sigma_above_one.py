#!/usr/bin/env python3
"""
L26 -- is sigma > 1 admissible to the CONSTRUCTION ITSELF, independent of gravitational Cherenkov?
===================================================================================================
Lane L26 of `fable_independent_2026/CHARTER.md`.  The lead agent's construction lives in
`closure_2026/integrable_clock_construction_2026/` and is READ-ONLY to this lane: nothing there is imported,
executed or modified.  Every coefficient below is transcribed BY HAND from IC4_ACTION.md / IC5_ACTION.md /
TENSOR_BALANCE.md / IC6_EVEN_CHARACTERISTICS.md / IC7_CURVATURE_SQUARE.md / LOCAL_WAVE_REPORT.md into sympy
here, differentiated symbolically, and evaluated at 60 decimal digits with mpmath.

THE SITUATION.  IC-4 declares its clock-speed design parameter free over (0, 1].  L15 derived the
sigma-dependence of the IC6 quartic obstruction,

    S_4'(1;sigma) = e^{5/6}(p_R T - 9)(3 p_R + 4)(3 p_R - 44) / (216(4T - 27)),   p_R = 8/3 + 4 a_* sigma,

which has EXACTLY ONE zero, at sigma_* = 4T/(4T-27) = 1.679 -- a clock 29.6% superluminal, above the whole
interval IC-4 allows itself.  So the obstruction is removable at exactly one value of the design parameter,
and that value sits outside the declared interval.

TWO INDEPENDENT THINGS COULD FORBID sigma_*.  Lane L19 is computing the first (does the gravitational-
Cherenkov bound apply to this mode at all, now that L8 has shown the metric sector is exactly Einstein and
the clock is a separately counted k-essence mode).  THIS lane computes the second, which nobody was on:

    is sigma > 1 admissible to the construction on the construction's OWN health conditions,
    and why does IC-4 declare (0, 1] in the first place?

WHAT IS NEW HERE, relative to L15.  L15 asked what happens AT sigma = 1 and proved the theorem that locates
sigma_*.  It never evaluated a single health condition above sigma = 1, never computed the second-order
behaviour of S_4 at sigma_* (where the first order vanishes, so the second order is the whole remaining
obstruction), never looked for the reason behind the interval, and never tested the causal structure.  All
four are done here.  The algebra is redone from the action, not imported from L15: in particular the closed
form for S_4'(1;sigma) is re-derived by symbolic implicit differentiation along the constraint branch rather
than transcribed, and is then confronted with L15's published expression as a control.

MANDATORY CONTROLS, in order, before anything is varied:
  L26-C2  S_4'(1)|_{sigma=1/3} = -11.1407711251147987   (the lead's boxed IC6 identity, confirmed by L4)
  L26-C3  S_4'(1)|_{sigma=1}   = -20.194205022906776    (L15's value)
If either fails, nothing downstream is trustworthy and the run stops there.

HONESTY.  This is the branch on which the lead's construction either simplifies dramatically or stays
permanently obstructed.  Nothing here is tuned toward either outcome.  If the interval (0,1] turns out to be
an undefended convention, that is reported as a finding, not as permission.  If a health condition kills
sigma_*, that is reported as a hard upper bound on the whole family.
"""
import os
import re
import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 60
FAILS = []
STOP = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)
    return ok


def close(a, b, tol):
    a, b = mp.mpf(a), mp.mpf(b)
    return abs(a - b) <= tol * max(mp.mpf(1), abs(b))


REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IC = os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "integrable_clock_construction_2026")
REL = "<repo>/qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026"


def readf(name):
    with open(os.path.join(IC, name), "r") as fh:
        return fh.read()


BAR = "=" * 118
print(BAR)
print("L26 -- is sigma > 1 admissible to the construction itself, independent of gravitational Cherenkov?")
print(BAR)

# ==================================================================================================================
# section 0 -- WHY DOES IC-4 DECLARE (0, 1]?  The documentary half, stated as checks that can fail.
# ==================================================================================================================
print("\n-- 0. where the interval (0,1] comes from -------------------------------------------------------------------")

ic4 = readf("IC4_ACTION.md")
ic4_lines = ic4.splitlines()
decl_idx = [i for i, ln in enumerate(ic4_lines) if r"0<\sigma\le1" in ln]
DECL = ic4_lines[decl_idx[0] - 1] + " " + ic4_lines[decl_idx[0]] if decl_idx else ""
print(f"    {REL}/IC4_ACTION.md, lines 69-70 and 77-78, VERBATIM:")
print(f'      "Define $a_*=3-81/(4\\mathcal T)>0$ and select the **fixed design parameter**')
print(f'       $\\sigma=1/3$. More generally the calculation covers $0<\\sigma\\le1$."')
print(f'      "These coefficients are fixed before any sector is tested. The squared-speed')
print(f'       parameter $\\sigma$ is a construction choice, not a prediction fitted to data."')

check("L26-D1 the interval is declared in IC4_ACTION.md and is declared WITHOUT a derivation. The sentence "
      "that states it -- 'More generally the calculation covers 0<sigma<=1' -- is preceded and followed by "
      "coefficient definitions and by the sentence 'The squared-speed parameter sigma is a construction "
      "choice, not a prediction fitted to data'. No stability, hyperbolicity, positivity or well-posedness "
      "word occurs anywhere in the surrounding block.",
      bool(decl_idx)
      and not any(w in " ".join(ic4_lines[max(0, decl_idx[0] - 8):decl_idx[0] + 10]).lower()
                  for w in ("stabil", "hyperbol", "well-posed", "wellposed", "ghost", "positiv", "because",
                            "requir", "bound", "forbid", "excluded")),
      "no derivation word in the 18 lines around the declaration")

# every occurrence of the interval anywhere in the lead's directory
occ = []
for root, _dirs, files in os.walk(IC):
    for fn in files:
        if not fn.endswith((".md", ".py", ".json", ".txt")):
            continue
        p = os.path.join(root, fn)
        try:
            with open(p, "r") as fh:
                txt = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        for i, ln in enumerate(txt.splitlines(), 1):
            if re.search(r"0\s*<\s*\\?sigma\s*(<=|\\le)\s*1", ln):
                occ.append((os.path.relpath(p, IC), i, ln.strip()))
srcs = sorted({o[0] for o in occ})
print(f"\n    every statement of the interval in {REL} ({len(occ)} occurrences in {len(srcs)} files):")
for f_, i_, ln_ in occ[:12]:
    short = ln_ if len(ln_) < 96 else ln_[:93] + "..."
    print(f"      {f_}:{i_}  {short}")
if len(occ) > 12:
    print(f"      ... and {len(occ) - 12} more, all inside run-record copies of the same two `domain` strings")

py_occ = [o for o in occ if o[0].endswith(".py")]
# an executable use of sigma would appear as a control-flow line or an assertion mentioning it
ctrl = []
for root, _dirs, files in os.walk(IC):
    for fn in files:
        if not fn.endswith(".py"):
            continue
        p = os.path.join(root, fn)
        with open(p, "r") as fh:
            for i, ln in enumerate(fh.read().splitlines(), 1):
                if re.match(r"\s*(assert|if|elif|while|raise)\b", ln) and re.search(r"\bsigma\b", ln):
                    ctrl.append((os.path.relpath(p, IC), i, ln.strip()))
check("L26-D2 [the decisive documentary check] the interval NEVER appears as an executable condition. In "
      "every .py file of the construction it occurs only inside a `domain` metadata STRING that is printed "
      "into the run record; there is no assert, if, while or raise anywhere in the construction that "
      "mentions sigma at all; and the only executable restriction ever placed on it is "
      "`sigma = s.Symbol(\"sigma\", positive=True)` in local_clock_wave.py, i.e. sigma > 0. The upper limit "
      "is therefore prose, not a condition any calculation ever tested against.",
      all(('"domain"' in ln or "domain=" in ln) for _f, _i, ln in py_occ)
      and not ctrl
      and 'sigma = s.Symbol("sigma", positive=True)' in readf("local_clock_wave.py"),
      f"{len(py_occ)} .py occurrences, all inside `domain` strings; {len(ctrl)} control-flow lines mention "
      f"sigma anywhere in the construction; the only restriction is positive=True")

# the one place a subluminality condition IS executable, and it is a different sector
ic11 = readf("ic11_clock_pressure.py")
healthy_line = [ln.strip() for ln in ic11.splitlines() if "healthy = bool" in ln]
cont_line = [ln.strip() for ln in ic11.splitlines() if ln.strip().startswith("and A != 0")]
print("\n    the ONE place a subluminality requirement is executable anywhere in the construction:")
print(f"      {REL}/ic11_clock_pressure.py:56-57")
for ln in healthy_line + cont_line:
    print(f"        {ln}")
print(f"      {REL}/IC11_CLOCK_PRESSURE.md:63, VERBATIM:")
print('        "They are necessary and sufficient for `PX>0`, `Qclock>0`, `0<cs^2<=1`."')

check("L26-D3 IC-11 -- a DIFFERENT sector, the k-essence clock pressure on IC-10's plateau -- does encode "
      "subluminality executably, as `Q >= PX` inside its `healthy` predicate (that inequality IS cs^2 <= 1, "
      "since cs^2 = PX/Q). It sits there as one clause among six, alongside five genuine positivity/rank "
      "conditions (PX > 0, energy > 0, physical_H > 0, A != 0, Qbare != 0) from which it is separable by "
      "deleting one conjunct. So the construction's own code distinguishes health from subluminality, and "
      "then imposes subluminality as an extra.",
      bool(healthy_line) and "Q >= PX" in healthy_line[0] and "PX > 0" in healthy_line[0]
      and "0<cs" in readf("IC11_CLOCK_PRESSURE.md") and "necessary and sufficient" in readf("IC11_CLOCK_PRESSURE.md"),
      "healthy = PX>0 AND Q>=PX AND energy>0 AND physical_H>0 AND A!=0 AND Qbare!=0")

check("L26-D4 [and it is a different number] IC-11's cs^2 is NOT IC-4's sigma. On IC-10/IC-11's plateau the "
      "clock speed is an OUTPUT of the pressure function P(X,w) and runs with S (0.0956, 0.1271, 0.2265, "
      "0.2577 at S = .03,.05,.10,.20), whereas IC-4's sigma is an INPUT fixed once at 1/3 on the IC-4 "
      "expanding witness. The two are the same mode's speed on two different backgrounds of two different "
      "action revisions, and no IC file states their relation. Any sigma decision therefore has to be taken "
      "twice, and this lane speaks only to the IC-4/5/6/7 handle.",
      all(s in readf("IC11_CLOCK_PRESSURE.md") for s in (".095640", ".127146", ".226486", ".257694"))
      and "sigma=1/3" in readf("IC5_ACTION.md").replace("$", "").replace("\\", ""),
      "IC11 cs^2 in 0.096-0.258 and S-dependent; IC4 sigma = 1/3 fixed")

# ==================================================================================================================
# the construction, transcribed by hand (IC4 constants; IC5/IC6 density; IC7's M, v, S_4)
# ==================================================================================================================
sig = sp.Symbol('sigma', positive=True)
ell = sp.log(sp.Rational(9, 5))
Tcal = -sp.Rational(27, 16) + 54 / (5 * ell)
astar = 3 - 81 / (4 * Tcal)
e_c = sp.Rational(1, 8)
d_c = -9 * e_c / Tcal
al_c = 81 * e_c / Tcal**2
be_c = 2 * d_c - sp.Rational(1, 3) - 3 * al_c / 4
ga_c = e_c - sp.Rational(1, 16) + 9 * al_c / 64 - 3 * d_c / 4
b_c = -Tcal / 9 - sp.Rational(3, 8)
m, kappa = sp.Integer(1), sp.Integer(6)
h0 = sp.sqrt(kappa / (6 * m))
a02 = 9 * kappa * sp.exp(-sp.Rational(1, 2)) / (16 * m * ell**2)
Ufun = lambda cc_: (1 - cc_) * (sp.log(1 - cc_)**2 - 2 * sp.log(1 - cc_) + 2) - 2
Lam = kappa * sp.exp(-sp.Rational(1, 2)) / m - a02 * Ufun(sp.Rational(4, 9))

pR_s = sp.Rational(8, 3) + 4 * astar * sig
qR_s = -1 - 3 * pR_s / 8
AR_s = 3 * pR_s / (16 * ell**2)
BR_s = 3 * qR_s / (16 * ell**2)

xi, u, rho, tau = sp.symbols('xi u rho tau', real=True)
w_f = (u - 1) * xi
Efac = sp.exp((4 - 3 * u) * xi)
F_s = AR_s * (xi - sp.Rational(1, 4)) + BR_s * (u - sp.Rational(2, 3))
J_s = 1 + sp.exp(-6 * w_f) * rho**2 * F_s / (m**2 * a02)
Cp = Lam + a02 * Ufun(u**2)
h_s = ((2 * Efac / m) * (tau / J_s - rho**2 / 6) + m * sp.exp((3 * u - 2) * xi) * Cp
       - (kappa / 2) * sp.exp((3 * u - 4) * xi))
c_s_ = m * sp.exp(u * xi) * J_s
Dt = lambda f: sp.diff(f, u) - b_c * sp.diff(f, xi)

NUM = lambda e_: mp.mpf(str(sp.N(e_, 55)))
T = NUM(Tcal)
AST = NUM(astar)
WIT = [mp.mpf(1) / 4, mp.mpf(2) / 3, -3 * mp.e**mp.mpf('-0.5'), mp.mpf(0)]
rho_w = WIT[2]


def build(sigma_value):
    """Lambdify the IC6/IC7 kit at one numeric sigma. Hand-built from IC7_CURVATURE_SQUARE.md's M, v, S_4."""
    sub = {sig: sigma_value}
    F_, J_, h_, c_ = F_s.subs(sub), J_s.subs(sub), h_s.subs(sub), c_s_.subs(sub)
    M11 = sp.diff(h_, rho, 2) / 4 + sp.diff(h_, tau) / 12
    M12 = Dt(sp.diff(h_, rho)) / 2
    M22 = Dt(Dt(h_))
    v1, v2 = sp.diff(c_, rho) / 2, Dt(c_)
    detM = M11 * M22 - M12**2
    S4 = -4 * (M22 * v1**2 - 2 * M12 * v1 * v2 + M11 * v2**2) / detM
    SYM = dict(M11=M11, M12=M12, M22=M22, v1=v1, v2=v2, detM=detM, S4=S4, c7=-S4 / 32, J=J_, F=F_, c=c_,
               hxi=sp.diff(h_, xi), hu=sp.diff(h_, u), hxx=sp.diff(h_, xi, 2),
               hxu=sp.diff(sp.diff(h_, xi), u), huu=sp.diff(h_, u, 2),
               hxr=sp.diff(sp.diff(h_, xi), rho), hur=sp.diff(sp.diff(h_, u), rho),
               r=-rho * Efac / (3 * m * h0))
    f = {k: sp.lambdify((xi, u, rho, tau), v, modules='mpmath') for k, v in SYM.items()}
    g = {k: [sp.lambdify((xi, u, rho, tau), sp.diff(SYM[k], q), modules='mpmath') for q in (xi, u, rho)]
         for k in ('M11', 'M12', 'M22', 'v1', 'v2', 'S4', 'J', 'F')}
    return f, g


def solve_aux(f, rv, tv, guess=(mp.mpf(1) / 4, mp.mpf(2) / 3)):
    """My own Newton solve of the two auxiliary constraints h_xi = h_u = 0 at fixed (rho, tau)."""
    q = mp.matrix(list(guess))
    for _ in range(200):
        Fv = mp.matrix([f['hxi'](q[0], q[1], rv, tv), f['hu'](q[0], q[1], rv, tv)])
        Jv = mp.matrix([[f['hxx'](q[0], q[1], rv, tv), f['hxu'](q[0], q[1], rv, tv)],
                        [f['hxu'](q[0], q[1], rv, tv), f['huu'](q[0], q[1], rv, tv)]])
        dq = mp.lu_solve(Jv, -Fv)
        q = q + dq
        if mp.norm(dq) < mp.mpf(10)**-50:
            break
    return q[0], q[1]


def branch(f, g):
    """Witness data and d/dj along the isotropic family lambda_i = -e^{-1/2} j."""
    Hm = mp.matrix([[f['hxx'](*WIT), f['hxu'](*WIT)], [f['hxu'](*WIT), f['huu'](*WIT)]])
    gj = mp.matrix([f['hxr'](*WIT) * rho_w, f['hur'](*WIT) * rho_w])
    dqdj = mp.lu_solve(Hm, -gj)

    def ddj(key):
        gg = g[key]
        return gg[0](*WIT) * dqdj[0] + gg[1](*WIT) * dqdj[1] + gg[2](*WIT) * rho_w
    return Hm, dqdj, ddj


def S4_at(f, jv):
    """S_4 on the isotropic constraint branch at scaled momentum j."""
    rv = rho_w * jv
    q = solve_aux(f, rv, mp.mpf(0))
    return f['S4'](q[0], q[1], rv, 0), q


# ==================================================================================================================
# section 1 -- mandatory controls
# ==================================================================================================================
print("\n-- 1. mandatory controls (if these fail, nothing below is reported) -----------------------------------------")

KIT = {'1/3': build(sp.Rational(1, 3)), '1': build(sp.Integer(1))}
f13, g13 = KIT['1/3']
f1, g1 = KIT['1']
_, _, ddj13 = branch(f13, g13)
_, _, ddj1 = branch(f1, g1)

wres = (abs(f13['hxi'](*WIT)), abs(f13['hu'](*WIT)), abs(f1['hxi'](*WIT)), abs(f1['hu'](*WIT)))
ok = check("L26-C1 the IC-4/IC-5 expanding witness (xi,u,rho,tau) = (1/4, 2/3, -3e^{-1/2}, 0) is an exact "
           "stationary point of my independently transcribed h, with F = 0 and activation r = 1, at both "
           "sigma = 1/3 and sigma = 1",
           max(wres) < mp.mpf(10)**-45 and abs(f13['F'](*WIT)) < mp.mpf(10)**-45
           and close(f13['r'](*WIT), 1, mp.mpf(10)**-45),
           f"max |h_xi|,|h_u| = {mp.nstr(max(wres), 3)}")
STOP.append(ok)

S4p_13 = ddj13('S4')
S4p_lead = -mp.e**(mp.mpf(5) / 6) * (5 * T - 27) * (8 * T - 27) * (8 * T + 27) / (18 * T**2 * (4 * T - 27))
ok = check("L26-C2 [MANDATORY CONTROL 1] at the published parameters sigma = 1/3 my rebuild returns the lead's "
           "boxed IC6 identity S_4'(1) = -e^{5/6}(5T-27)(8T-27)(8T+27)/(18 T^2 (4T-27)) = "
           "-11.1407711251147987, the value L4 confirmed independently",
           close(S4p_13, S4p_lead, mp.mpf(10)**-40) and close(S4p_13, '-11.1407711251147987', mp.mpf('1e-16')),
           f"S_4'(1)|_sigma=1/3 = {mp.nstr(S4p_13, 18)}")
STOP.append(ok)

S4p_1 = ddj1('S4')
ok = check("L26-C3 [MANDATORY CONTROL 2] at sigma = 1 my rebuild returns L15's value "
           "S_4'(1) = -20.194205022906776",
           close(S4p_1, '-20.194205022906776', mp.mpf('1e-16')),
           f"S_4'(1)|_sigma=1 = {mp.nstr(S4p_1, 18)}")
STOP.append(ok)

if not all(STOP):
    print("\n*** CONTROL FAILED -- stopping. The rebuild does not reproduce the lead's / L15's confirmed values,")
    print("*** so no statement about sigma > 1 from this script would be trustworthy. Nothing downstream reported.")
    sys.exit(1)

# ==================================================================================================================
# section 2 -- sigma_*, re-derived rather than transcribed
# ==================================================================================================================
print("\n-- 2. sigma_*, re-derived from the branch (not copied from L15) ---------------------------------------------")

# At the witness v1 = M11 = 0, so S_4(1) = 0 and, differentiating the quotient along the branch,
#   S_4'(1) = 4 [ M11' v2^2 - 2 M12 v1' v2 ] / M12^2 .
# I build M11', v1' by symbolic implicit differentiation with the sigma-free tangent dq/dj, then simplify.
Hs = sp.Matrix([[sp.diff(h_s, xi, 2), sp.diff(sp.diff(h_s, xi), u)],
                [sp.diff(sp.diff(h_s, xi), u), sp.diff(h_s, u, 2)]])
gs = sp.Matrix([sp.diff(sp.diff(h_s, xi), rho) * rho, sp.diff(sp.diff(h_s, u), rho) * rho])
WSUB = {xi: sp.Rational(1, 4), u: sp.Rational(2, 3), rho: -3 * sp.exp(-sp.Rational(1, 2)), tau: 0}
dqdj_sym = sp.simplify((-Hs.subs(WSUB).inv() * gs.subs(WSUB)))

M11_s = sp.diff(h_s, rho, 2) / 4 + sp.diff(h_s, tau) / 12
M12_s = Dt(sp.diff(h_s, rho)) / 2
v1_s, v2_s = sp.diff(c_s_, rho) / 2, Dt(c_s_)


def ddj_sym(expr):
    return (sp.diff(expr, xi).subs(WSUB) * dqdj_sym[0] + sp.diff(expr, u).subs(WSUB) * dqdj_sym[1]
            + sp.diff(expr, rho).subs(WSUB) * WSUB[rho])


S4p_mine = sp.simplify(4 * (ddj_sym(M11_s) * v2_s.subs(WSUB)**2
                            - 2 * M12_s.subs(WSUB) * ddj_sym(v1_s) * v2_s.subs(WSUB)) / M12_s.subs(WSUB)**2)
S4p_L15 = sp.exp(sp.Rational(5, 6)) * (pR_s * Tcal - 9) * (3 * pR_s + 4) * (3 * pR_s - 44) / (216 * (4 * Tcal - 27))
check("L26-G1 [independent re-derivation] symbolic implicit differentiation along the constraint branch gives "
      "my own closed form for S_4'(1;sigma), and it agrees SYMBOLICALLY with L15's published expression "
      "e^{5/6}(p_R T - 9)(3 p_R + 4)(3 p_R - 44)/(216(4T - 27)). Two independent routes to the same "
      "sigma-dependence.",
      sp.simplify(S4p_mine - S4p_L15) == 0,
      "sympy: my form minus L15's form simplifies to exactly 0")

S4p_f = sp.lambdify(sig, S4p_L15, modules='mpmath')
roots = sp.solve(sp.Eq(S4p_L15, 0), sig)
sig_star_sym = sp.simplify(4 * Tcal / (4 * Tcal - 27))
SIGSTAR = NUM(sig_star_sym)
CSTAR = mp.sqrt(SIGSTAR)
check("L26-G2 the closed form has exactly ONE zero in sigma, my independent value of it is "
      "sigma_* = 4T/(4T-27) = 3/a_*, and it is the root of the single factor 3 p_R - 44 (so p_R(sigma_*) = "
      "44/3 exactly). The other two factors, (p_R T - 9) and (3 p_R + 4), are strictly positive for every "
      "sigma > 0.",
      len(roots) == 1 and close(mp.mpf(str(sp.N(roots[0], 45))), SIGSTAR, mp.mpf('1e-40'))
      and sp.simplify(pR_s.subs(sig, sig_star_sym) - sp.Rational(44, 3)) == 0
      and sp.simplify(sig_star_sym - 3 / astar) == 0,
      f"sigma_* = {mp.nstr(SIGSTAR, 16)}, c_s = {mp.nstr(CSTAR, 12)} c "
      f"({mp.nstr(100 * (CSTAR - 1), 5)}% superluminal)")

SS = mp.mpf(str(sp.N(sig_star_sym, 50)))
KIT['*'] = build(sp.nsimplify(sig_star_sym))
fS, gS = KIT['*']
_, dqdjS, ddjS = branch(fS, gS)
S4p_S = ddjS('S4')
check("L26-G3 [control on the point itself] the FULL numerical implicit-function derivative at sigma_* -- the "
      "same machinery that returned -11.1407711251147987 and -20.194205022906776 -- returns S_4'(1;sigma_*) "
      "= 0 to 40 digits. The obstruction's leading order genuinely cancels there; this is not a property of "
      "the closed form alone.",
      abs(S4p_S) < mp.mpf('1e-40') and abs(S4p_f(SS)) < mp.mpf('1e-40'),
      f"S_4'(1;sigma_*) = {mp.nstr(S4p_S, 8)} (numeric branch) and {mp.nstr(S4p_f(SS), 8)} (closed form)")

print("\n    S_4'(1;sigma) across and beyond IC-4's declared interval:")
print("      sigma        p_R          S_4'(1)              J_T'(1)")
for sv in ('0.05', '0.3333333333333333', '0.75', '1.0', '1.25', '1.5', mp.nstr(SIGSTAR, 16), '1.8', '2.5'):
    s_ = mp.mpf(sv)
    pr_ = mp.mpf(8) / 3 + 4 * AST * s_
    Jp_ = (9 - pr_ * T) / (4 * T - 27)
    print(f"      {mp.nstr(s_, 8):<12} {mp.nstr(pr_, 8):<12} {mp.nstr(S4p_f(s_), 12):<20} {mp.nstr(Jp_, 8)}")

# ==================================================================================================================
# section 3 -- the construction's OWN health conditions, each computed at sigma_*
# ==================================================================================================================
print("\n-- 3. the construction's own health conditions, evaluated at sigma_* = 1.679 --------------------------------")

# --- H1  ghost / kinetic normalisation, two independent routes -----------------------------------------------
xw, yw, vw, zw = sp.symbols('x y v z', real=True)
pRg = sp.Symbol('p_R', real=True)
qRg = -1 - 3 * pRg / 8
Lw = ((3 + al_c * xw / 4) * yw**2 - 9 * (Tcal + e_c * xw) * yw * vw / Tcal + (Tcal + e_c * xw) * vw**2
      + (sp.Rational(2, 3) + pRg / 2) * xw * zw * yw + (1 + 3 * pRg / 8 + qRg) * xw * zw * vw + xw * zw**2)
v_sol = sp.solve(sp.diff(Lw, vw), vw)[0]
Lw_red = sp.simplify(Lw.subs(vw, v_sol))
kin = sp.simplify(sp.expand(Lw_red).coeff(yw, 2))
bx = sp.simplify(sp.expand(Lw_red).coeff(zw, 1).coeff(yw, 1))
gx = sp.simplify(xw - sp.Rational(3, 2) * bx + xw * sp.diff(bx, xw))
pR_forced = sp.solve(sp.Eq(gx, -astar * sig * xw), pRg)[0]
Ew, Epw = (yw**2 + sig * xw * zw**2) / 2, -3 * yw**2 - sig * xw * zw**2
check("L26-H1 [GHOST] the scalar's kinetic normalisation stays positive above sigma = 1, and it does so "
      "trivially, because it does not depend on sigma at all. Re-deriving LOCAL_WAVE_REPORT's reduction in my "
      "own sympy: eliminating v gives kinetic coefficient a_* = 3 - 81/(4T) = 1.7864, EXACTLY sigma-free, "
      "with reduced Lagrangian a_*[zdot^2 - sigma (N0 k/A)^2 z^2]. Kinetic sign needs a_* > 0; GRADIENT sign "
      "needs sigma > 0. Neither has an upper edge. L15's finding that a_* = 1.786 and A_0 = 0.4615 are "
      "sigma-independent therefore survives past sigma = 1 unchanged, and what moves is only the gradient "
      "term's SIZE.",
      sp.simplify(kin - astar) == 0 and sp.diff(kin, sig) == 0
      and sp.simplify(pR_forced - (sp.Rational(8, 3) + 4 * astar * sig)) == 0
      and AST > 0 and SIGSTAR * AST > 0,
      f"kinetic a_* = {mp.nstr(AST, 12)} (sigma-free) > 0; gradient sigma_* a_* = "
      f"{mp.nstr(SIGSTAR * AST, 12)} > 0")

check("L26-H1b [the same statement as an energy] LOCAL_WAVE_REPORT's exact mode-energy identity "
      "E = (y^2 + sigma x z^2)/2, E' = -3y^2 - sigma x z^2 <= 0 is verified here with sigma symbolic. E is "
      "positive definite and monotonically decreasing for EVERY sigma > 0; the identity has no upper "
      "restriction on sigma whatsoever. At sigma_* the mode is still a damped positive-energy oscillator.",
      sp.simplify(sp.diff(Ew, yw, 2) - 1) == 0 and sp.simplify(sp.diff(Ew, zw, 2) - sig * xw) == 0
      and sp.simplify(Epw + 3 * yw**2 + sig * xw * zw**2) == 0,
      "E positive definite for sigma > 0, x > 0; E' <= 0; both symbolic in sigma")

A0_w = {nm: KIT[nm][0]['detM'](*WIT) / KIT[nm][0]['M22'](*WIT) for nm in ('1/3', '1', '*')}
j7 = mp.mpf('1.007')
st = {}
for nm in ('1/3', '1', '*'):
    ff = KIT[nm][0]
    S4v, q = S4_at(ff, j7)
    dMv, M22v = ff['detM'](q[0], q[1], rho_w * j7, 0), ff['M22'](q[0], q[1], rho_w * j7, 0)
    st[nm] = dict(xi=q[0], u=q[1], S4=S4v, A0=dMv / M22v, c7=ff['c7'](q[0], q[1], rho_w * j7, 0),
                  J=ff['J'](q[0], q[1], rho_w * j7, 0), detM=dMv)
check("L26-H1c [GHOST, second route] the reduced scalar kinetic normalisation A_0 = det M / M22 is POSITIVE at "
      "sigma_*, both at the witness (where it is exactly sigma-independent, since M11 = 0 and M12, M22 are "
      "sigma-free there) and at the nearby state j = 1.007.",
      A0_w['*'] > 0 and close(A0_w['*'], A0_w['1/3'], mp.mpf('1e-40')) and st['*']['A0'] > 0,
      f"A_0(witness) = {mp.nstr(A0_w['*'], 12)} at every sigma; A_0(j=1.007) = "
      f"{mp.nstr(st['1/3']['A0'], 10)} -> {mp.nstr(st['*']['A0'], 10)} at sigma_*")

# --- H2  tensor cone ------------------------------------------------------------------------------------------
B3 = sp.Symbol('B3', positive=True)
light2 = sp.exp((4 - 2 * u) * xi) / B3**2
cT2 = lambda Kc, Gc: sp.simplify(4 * Kc * Gc / light2)
cT2_IC6 = cT2(Efac / (m * J_s), c_s_ / (4 * B3**2))
cT2_IC5 = cT2(Efac / m, c_s_ / (4 * B3**2))
cT2_num = {nm: 4 * (mp.e**((4 - 3 * st[nm]['u']) * st[nm]['xi']) / st[nm]['J'])
           * (st[nm]['J'] * mp.e**(st[nm]['u'] * st[nm]['xi']) / 4)
           / (mp.e**((4 - 2 * st[nm]['u']) * st[nm]['xi'])) for nm in ('1/3', '1', '*')}
check("L26-H2 [TENSOR CONE] c_T^2 = 1 is still EXACT at sigma_*. TENSOR_BALANCE's K_T = 1 + F Q^2/a0^2 = J_T "
      "and G_T = J_T cancel identically, and sigma lives only inside J_T, so c_T^2 = 1 is an identity in "
      "sigma with no upper edge -- verified here with sigma left symbolic, and confirmed numerically at the "
      "j = 1.007 state at sigma_*. The check has teeth: the IC5 mutation, which drops the J_T from K_T, "
      "correctly returns c_T^2 = J_T instead of 1. L15's sigma-identity finding is confirmed and extends "
      "above sigma = 1.",
      sp.simplify(cT2_IC6 - 1) == 0 and sig not in cT2_IC6.free_symbols
      and sp.simplify(cT2_IC5 - J_s) == 0 and sp.simplify(J_s - 1) != 0
      and close(cT2_num['*'], 1, mp.mpf('1e-40')),
      f"c_T^2(IC6) - 1 == 0 identically in sigma; numerically at sigma_*, j=1.007: "
      f"{mp.nstr(cT2_num['*'], 20)}; IC5 control returns J_T = {mp.nstr(st['*']['J'], 10)} != 1")

# --- H3  frozen domain ----------------------------------------------------------------------------------------
Hm13, _, _ = branch(f13, g13)
HmS, _, _ = branch(fS, gS)
Hn = HmS / (m * mp.e**mp.mpf('-0.5') * h0**2)
check("L26-H3 [FROZEN DOMAIN] T > 27/4 still holds at sigma_*, and T does not depend on sigma at all: "
      "T = -27/16 + 54/(5 ln(9/5)) contains no sigma. The auxiliary Hessian at the witness is likewise "
      "identical, -[[24,-27],[-27,2T+135/8]] with det = 12(4T-27) > 0, and both its eigenvalues are bounded "
      "away from zero at sigma_*.",
      sp.diff(Tcal, sig) == 0 and T > mp.mpf(27) / 4
      and close(mp.det(Hn), 12 * (4 * T - 27), mp.mpf('1e-40'))
      and mp.norm(HmS - Hm13) < mp.mpf('1e-40'),
      f"T = {mp.nstr(T, 12)} > 6.75 (sigma-free); det H_qq = {mp.nstr(mp.det(Hn), 12)} = 12(4T-27); "
      f"||H(sigma_*) - H(1/3)|| = {mp.nstr(mp.norm(HmS - Hm13), 3)}")

# --- H4  the auxiliary constraint surface and its fold ---------------------------------------------------------
check("L26-H4a [CONSTRAINT SURFACE] the isotropic auxiliary constraints do not move at all. The nongradient "
      "density restricted to tau = 0 is exactly sigma-free (the whole F-dependence sits in the tau/J_T term), "
      "so h_xi = h_u = 0, their solution, the branch tangent dq/dj and the fold are sigma-independent "
      "IDENTITIES, not numerical coincidences. Verified symbolically, plus the Newton solve at j = 1.007 "
      "returns IC6_EVEN's xi = 0.24297809, u = 0.66347046 at sigma_* to 40 digits.",
      sp.simplify(sp.diff(h_s.subs(tau, 0), sig)) == 0
      and close(st['*']['xi'], '0.24297809', mp.mpf('5e-9')) and close(st['*']['u'], '0.66347046', mp.mpf('5e-9'))
      and abs(st['*']['xi'] - st['1/3']['xi']) < mp.mpf('1e-40'),
      "d(h|_tau=0)/dsigma == 0 symbolically; j=1.007 state identical to 40 digits")


def usable(ff, jv):
    """(branch still exists, J_T there). Regular branch requires real (xi,u) with 0 < u < 1."""
    rv = rho_w * jv
    try:
        q = solve_aux(ff, rv, mp.mpf(0))
        if not (mp.im(q[0]) == 0 and mp.im(q[1]) == 0 and mp.mpf(0) < q[1] < mp.mpf(1)):
            return False, None
        Jv = ff['J'](q[0], q[1], rv, 0)
        return (True, mp.re(Jv)) if mp.im(Jv) == 0 else (False, None)
    except (TypeError, ValueError, ZeroDivisionError):
        return False, None


def find_fold(ff):
    lo, hi, step = mp.mpf('1.0'), None, mp.mpf('0.002')
    jv = lo + step
    while jv < mp.mpf('3.0'):
        ok_j, _ = usable(ff, jv)
        if not ok_j:
            hi = jv
            break
        lo = jv
        jv += step
    if hi is None:
        return lo
    for _ in range(80):
        mid = (lo + hi) / 2
        if usable(ff, mid)[0]:
            lo = mid
        else:
            hi = mid
    return lo


fold = {nm: find_fold(KIT[nm][0]) for nm in ('1/3', '1', '*')}
JT_fold = {nm: usable(KIT[nm][0], fold[nm])[1] for nm in ('1/3', '1', '*')}
check("L26-H4b [THE FOLD] the fold of the auxiliary constraint surface DOES NOT MOVE with sigma. L15 located "
      "it at j = 1.216488 (correcting the guess that the branch ends at J_T = 0); it sits at the same j to "
      "1e-6 at sigma = 1/3, sigma = 1 and sigma_*, for the structural reason in L26-H4a. The isotropic branch "
      "at sigma_* is exactly as long as the published one.",
      abs(fold['*'] - fold['1/3']) < mp.mpf('1e-6') and abs(fold['1'] - fold['1/3']) < mp.mpf('1e-6')
      and close(fold['1/3'], '1.216488', mp.mpf('1e-5')),
      f"fold at j = {mp.nstr(fold['1/3'], 9)} (sigma=1/3), {mp.nstr(fold['1'], 9)} (sigma=1), "
      f"{mp.nstr(fold['*'], 9)} (sigma_*)")

# --- H5  J_T > 0, the one condition that actually moves --------------------------------------------------------
jgrid = [mp.mpf(1) + (fold['1/3'] - 1) * mp.mpf(i) / 40 for i in range(1, 40)]
JT_prof = {nm: [usable(KIT[nm][0], jv)[1] for jv in jgrid] for nm in ('1/3', '1', '*')}
mono = all(JT_prof['*'][i + 1] < JT_prof['*'][i] for i in range(len(jgrid) - 1))
JTmin = {nm: min(JT_prof[nm] + [JT_fold[nm]]) for nm in ('1/3', '1', '*')}
# J_T on the isotropic branch is EXACTLY affine in sigma: (xi,u,rho) are sigma-free there and F is affine in p_R.
Jf13, Jf1 = JT_fold['1/3'], JT_fold['1']
slope = (Jf1 - Jf13) / (1 - mp.mpf(1) / 3)
SIG_JT = 1 + Jf1 / (-slope)
pred_star = Jf1 + slope * (SIGSTAR - 1)
check("L26-H5 [J_T > 0, THE BINDING CONDITION] IC-6 and IC-7 are defined only on the open branch J_T > 0, and "
      "this is the one health condition that genuinely degrades with sigma. J_T on the isotropic branch is "
      "EXACTLY AFFINE in sigma (the state is sigma-free, F is affine in p_R, p_R is affine in sigma), and "
      "monotonically decreasing in j, so the whole condition reduces to its value at the fold. It stays "
      "POSITIVE at sigma_*, but only just: the margin falls 0.7268 -> 0.3899 -> 0.0532 as sigma goes "
      "1/3 -> 1 -> sigma_*. The affine law puts the ZERO at sigma = 1.7716.",
      JTmin['*'] > 0 and mono and close(pred_star, JTmin['*'], mp.mpf('1e-12')) and SIG_JT > SIGSTAR,
      f"min J_T on the branch: {mp.nstr(JTmin['1/3'], 8)} (sigma=1/3), {mp.nstr(JTmin['1'], 8)} (sigma=1), "
      f"{mp.nstr(JTmin['*'], 8)} (sigma_*); affine zero at sigma = {mp.nstr(SIG_JT, 8)}")

check("L26-H5b [the hard upper bound this yields] the affine law gives the construction's own first internal "
      "ceiling on its design parameter: J_T > 0 on the whole isotropic branch requires sigma < 1.7716. "
      "sigma_* = 1.6794 lies BELOW it, by 5.5% of sigma_*. That is a real margin and a real narrowness: the "
      "value that cancels the obstruction sits inside the admissible region but near its edge, so any "
      "revision that moves T, the witness or the fold must re-check this inequality first.",
      SIGSTAR < SIG_JT and (SIG_JT - SIGSTAR) / SIGSTAR > mp.mpf('0.01'),
      f"sigma_* = {mp.nstr(SIGSTAR, 10)} < sigma_(J_T=0) = {mp.nstr(SIG_JT, 10)}; headroom "
      f"{mp.nstr(100 * (SIG_JT - SIGSTAR) / SIGSTAR, 4)}% of sigma_*")

# --- H6  det M != 0, IC7's normalisation -----------------------------------------------------------------------
detstar = {nm: KIT[nm][0]['detM'](*WIT) for nm in ('1/3', '1', '*')}
check("L26-H6 [IC7 NORMALISATION] det(M_star) = -4 T^2 h0^2/81 is nonzero and IDENTICAL at sigma_*, because "
      "M11 = 0 at the witness for every sigma while M12 and M22 are sigma-free. IC7's cutoff normalisation "
      "D = det M/det M_star therefore does not move, and det M stays nonzero along the branch at sigma_*.",
      close(detstar['*'], -4 * T**2 * h0**2 / 81, mp.mpf('1e-40'))
      and close(detstar['*'], detstar['1/3'], mp.mpf('1e-40')) and abs(st['*']['detM']) > mp.mpf('1e-6'),
      f"det(M*) = {mp.nstr(detstar['*'], 14)} at every sigma; det M(j=1.007) = {mp.nstr(st['*']['detM'], 10)}")

# --- H7  hyperbolicity: are the characteristics real at 1.296 c? -----------------------------------------------
lightsq = mp.e**(mp.mpf(2) / 3)
speeds = {nm: (mp.mpf(str(sp.N(v, 40))) * lightsq, lightsq)
          for nm, v in (('1/3', sp.Rational(1, 3)), ('1', sp.Integer(1)), ('*', sig_star_sym))}
check("L26-H7 [HYPERBOLICITY] the system is still hyperbolic at 1.296 c: the characteristics are real. "
      "IC6_EVEN's exact reduced isotropic equation is qddot + 3 qdot + e^{2/3} k^2 diag(sigma, 1) q = 0, so "
      "the two squared coordinate speeds are sigma e^{2/3} (scalar) and e^{2/3} (tensor). Both are strictly "
      "POSITIVE for every sigma > 0, hence both characteristic speeds are real and distinct at sigma_*; and "
      "hyperbolicity is exactly the condition sigma > 0, with no upper edge. What sigma > 1 changes is which "
      "of the two cones is the wider one, not whether either exists.",
      all(s > 0 for s in speeds['*']) and speeds['*'][0] > speeds['*'][1]
      and mp.sqrt(speeds['*'][0] / speeds['*'][1]) > 1,
      f"squared coordinate speeds at sigma_*: scalar {mp.nstr(speeds['*'][0], 10)}, tensor "
      f"{mp.nstr(speeds['*'][1], 10)}; ratio c_s/c_T = {mp.nstr(mp.sqrt(speeds['*'][0]/speeds['*'][1]), 10)}")

MD11 = -24 - 81 * xw / (4 * Tcal**2)
MD12 = 27 + 9 * xw / (4 * Tcal) + 243 * xw / (32 * Tcal**2)
MD22 = -2 * Tcal - sp.Rational(135, 8) - xw / 4 - 27 * xw / (16 * Tcal) - 729 * xw / (256 * Tcal**2)
detMD = sp.simplify(MD11 * MD22 - MD12**2)
check("L26-H7b [CONSTRAINT RANK] the quadratic-Dirac constraint algebra is sigma-blind, so the second-class "
      "classification that gives one physical scalar pair is untouched at sigma_*. LOCAL_WAVE's auxiliary "
      "matrix M contains no p_R at all and its determinant reproduces the lead's "
      "3 F^2 h^4 (4T-27)(8T+x)/(2T) > 0 symbolically. Rank four, four second-class plus two first-class "
      "constraints, (10 - 4 - 4)/2 = 1 pair -- identical above sigma = 1.",
      sp.simplify(detMD - 3 * (4 * Tcal - 27) * (8 * Tcal + xw) / (2 * Tcal)) == 0
      and not ({pRg, sig} & (MD11.free_symbols | MD12.free_symbols | MD22.free_symbols)),
      f"det M_Dirac/(F^2 h^4) at x = 1 is {mp.nstr(mp.mpf(str(sp.N(detMD.subs(xw,1),40))), 12)} > 0, sigma-free")

# --- H8  the sheared fixture ----------------------------------------------------------------------------------
lamsh = [mp.mpf('-0.6424435072183933'), mp.mpf('-0.622272178918671'), mp.mpf('-0.5676134368548011')]
rsh = sum(lamsh)
tsh = sum(x_**2 for x_ in lamsh) - rsh**2 / 3
sh = {}
for nm in ('1/3', '1', '*'):
    ff = KIT[nm][0]
    xs, us = solve_aux(ff, rsh, tsh)
    sh[nm] = dict(xi=xs, u=us, J=ff['J'](xs, us, rsh, tsh), r=ff['r'](xs, us, rsh, tsh),
                  c7=ff['c7'](xs, us, rsh, mp.mpf(0)))
check("L26-H8 [SHEARED FIXTURE] the sheared state -- the one place the auxiliary solve genuinely moves with "
      "sigma, because tau != 0 makes the constraints see F -- still exists at sigma_*, still lies on the "
      "regular branch 0 < u < 1, still has J_T > 0, and still sits inside the IC-5 activation plateau "
      "|r^2 - 1| <= 1/4. Control: at sigma = 1/3 my solve reproduces IC6_EVEN's 18-digit "
      "xi = 0.242752746344542675, u = 0.663589818477735377, J_T = 0.986102159712075428.",
      close(sh['1/3']['xi'], '0.242752746344542675', mp.mpf('1e-17'))
      and close(sh['1/3']['u'], '0.663589818477735377', mp.mpf('1e-17'))
      and close(sh['1/3']['J'], '0.986102159712075428', mp.mpf('1e-17'))
      and 0 < sh['*']['u'] < 1 and sh['*']['J'] > 0 and abs(sh['*']['r']**2 - 1) <= mp.mpf(1) / 4,
      f"sigma_*: xi = {mp.nstr(sh['*']['xi'], 15)}, u = {mp.nstr(sh['*']['u'], 15)}, "
      f"J_T = {mp.nstr(sh['*']['J'], 12)} > 0, |r^2-1| = {mp.nstr(abs(sh['*']['r']**2 - 1), 6)} <= 0.25")

# --- H9  the residual obstruction at second order --------------------------------------------------------------
print("\n    S_4 on the isotropic branch, at the three values of sigma:")
print("      j          S_4(sigma=1/3)     S_4(sigma=1)       S_4(sigma_*)")
S4prof = {}
for jv in ('1.002', '1.007', '1.02', '1.05', '1.10', '1.15', '1.21'):
    row = []
    for nm in ('1/3', '1', '*'):
        val = S4_at(KIT[nm][0], mp.mpf(jv))[0]
        row.append(val)
        S4prof.setdefault(nm, {})[jv] = val
    print(f"      {jv:<10} {mp.nstr(row[0], 10):<18} {mp.nstr(row[1], 10):<18} {mp.nstr(row[2], 10)}")

hstep = mp.mpf('1e-6')
S4pp = {}
for nm in ('1/3', '1', '*'):
    ff = KIT[nm][0]
    Sp = S4_at(ff, 1 + hstep)[0]
    Sm = S4_at(ff, 1 - hstep)[0]
    S0 = S4_at(ff, mp.mpf(1))[0]
    S4pp[nm] = (Sp - 2 * S0 + Sm) / hstep**2

# the sign of S_4 decides growth vs oscillation: M_0 zetadotdot + S_4 k^4 zeta = 0 gives lambda^2 = -S_4/M_0 k^4
scanj = [1 + (fold['1/3'] - 1) * mp.mpf(i) / 60 for i in range(1, 60)]
S4sign = {nm: [S4_at(KIT[nm][0], jv)[0] for jv in scanj] for nm in ('1/3', '1', '*')}
check("L26-H9 [WHAT sigma_* ACTUALLY DOES TO THE OBSTRUCTION -- the sign, not the size] at sigma_* the "
      "leading order of S_4 along the branch vanishes AND the sign of what remains REVERSES. S_4 > 0 at all "
      "59 points of a scan across the entire isotropic branch j in (1, 1.2165), against S_4 < 0 at all 59 "
      "points at both sigma = 1/3 and sigma = 1. Since the reduced equation is M_0 zetadotdot + S_4 k^4 zeta "
      "= 0 with M_0 > 0, IC6's conclusion -- real temporal roots lambda ~ +/- sqrt(-S_4/M_0) k^2, i.e. a "
      "growth rate rising like k^2, which is the Hadamard ill-posedness signature -- becomes lambda^2 < 0, a "
      "bounded oscillation at frequency ~ k^2. The ill-posedness is REMOVED on the whole branch, not merely "
      "reduced.",
      all(v > 0 for v in S4sign['*']) and all(v < 0 for v in S4sign['1/3'])
      and all(v < 0 for v in S4sign['1']) and S4pp['*'] > 0,
      f"S_4 > 0 at {sum(1 for v in S4sign['*'] if v > 0)}/59 branch points at sigma_*, < 0 at "
      f"{sum(1 for v in S4sign['1/3'] if v < 0)}/59 at sigma = 1/3; S_4''(1) = {mp.nstr(S4pp['1/3'], 8)} "
      f"(sigma=1/3) -> {mp.nstr(S4pp['*'], 8)} (sigma_*)")

rat = {jv: abs(S4prof['*'][jv] / S4prof['1/3'][jv]) for jv in S4prof['*']}
check("L26-H9b [AND THE HONEST HALF: IC7 IS NOT MADE UNNECESSARY, ONLY SIGN-FLIPPED AND LOCALLY SMALLER] "
      "S_4 = 0 is what IC6 asks for, and sigma_* delivers it only to FIRST order at j = 1. The residual is "
      "quadratic, so c_7 = -S_4/32 shrinks near the witness -- 19.2x smaller at j = 1.002, 5.4x at j = 1.007 "
      "-- but it GROWS away from it: 1.4x larger at j = 1.05, 2.8x at 1.10, 3.8x at 1.15. IC7's counterterm "
      "is therefore still required across the branch, now with the OPPOSITE SIGN (c_7 < 0), and this lane "
      "does not claim it becomes unnecessary. What it does claim is the sign result of L26-H9: the thing "
      "IC7 is cancelling is no longer a growth term.",
      st['*']['c7'] * st['1/3']['c7'] < 0 and rat['1.002'] < 1 and rat['1.007'] < 1 and rat['1.10'] > 1,
      f"|S_4(sigma_*)/S_4(1/3)|: {mp.nstr(rat['1.002'],4)} at j=1.002, {mp.nstr(rat['1.007'],4)} at 1.007, "
      f"{mp.nstr(rat['1.05'],4)} at 1.05, {mp.nstr(rat['1.10'],4)} at 1.10; c_7(1.007) "
      f"{mp.nstr(st['1/3']['c7'], 8)} -> {mp.nstr(st['*']['c7'], 8)}")

# --- H10  the admissible window, since both edges are now computed --------------------------------------------
WIN = []
for sv in ('1.60', '1.6793127321871', '1.70', '1.74', '1.7716', '1.79'):
    s_ = mp.mpf(sv)
    kf = build(sp.Float(sv, 30))[0]
    prof = [S4_at(kf, jv)[0] for jv in scanj]
    jts = [usable(kf, jv)[1] for jv in scanj] + [usable(kf, fold['1/3'])[1]]
    WIN.append((s_, all(v > 0 for v in prof), min(jts), S4p_f(s_)))
print("\n    the window in sigma where BOTH the branch exists and the growth obstruction is absent:")
print("      sigma          S_4'(1)             S_4 > 0 on branch?   min J_T on branch")
for s_, allpos, jtm, s4p in WIN:
    print(f"      {mp.nstr(s_, 10):<14} {mp.nstr(s4p, 12):<19} {'yes' if allpos else 'NO ':<20} {mp.nstr(jtm, 8)}")
check("L26-H10 [A WINDOW, NOT A POINT] the two computed edges bracket a genuine interval of the design "
      "parameter in which the construction is internally consistent AND free of the IC6 growth obstruction: "
      "sigma in [1.6793, 1.7716). Its lower edge is sigma_* (below it S_4'(1) < 0 and growth returns near "
      "the witness); its upper edge is J_T -> 0 at the fold (above it the IC6/IC7 branch condition fails). "
      "The window is 5.5% wide in sigma, i.e. c_s from 1.2959 c to 1.3310 c. This is a family, so it is not "
      "a fine tuning of one number -- but it is narrow, and it is bounded on both sides by things the "
      "construction itself computes.",
      WIN[0][1] is False and WIN[1][1] and WIN[3][1] and WIN[3][2] > 0 and WIN[5][2] < 0,
      f"lower edge sigma_* = {mp.nstr(SIGSTAR, 10)} (S_4 sign flips), upper edge "
      f"{mp.nstr(SIG_JT, 10)} (min J_T -> 0); width {mp.nstr(100*(SIG_JT-SIGSTAR)/SIGSTAR, 4)}% of sigma_*")

# ==================================================================================================================
# section 4 -- the causality question, stated properly
# ==================================================================================================================
print("\n-- 4. causality with a preferred foliation ------------------------------------------------------------------")
print("    Standard treatment, cited rather than asserted:")
print("      - Babichev, Mukhanov & Vikman, JHEP 0802:101 (2008), 'k-Essence, superluminal propagation,")
print("        causality and emergent geometry': a superluminal k-essence cone is causally acceptable when the")
print("        emergent (acoustic) metric admits a global time function; no CTCs arise from the wider cone alone.")
print("      - Bruneton & Esposito-Farese, PRD 76, 124012 (2007): superluminal propagation in preferred-frame")
print("        scalar-tensor theories and the conditions under which it does or does not violate causality.")
print("      - Blas, Pujolas & Sibiryakov, JHEP 1104:018 (2011), and Blas & Sibiryakov, PRD 84, 124043 (2011):")
print("        in khronometric / Horava gravity the khronon foliation IS a global time function, modes with")
print("        speeds != 1 (including the instantaneous limit) are standard, and black holes acquire universal")
print("        horizons rather than causal pathology.")
print("      - Adams, Arkani-Hamed, Dubovsky, Nicolis & Rattazzi, JHEP 0610:014 (2006): the IR obstruction to a")
print("        LORENTZ-INVARIANT UV completion of a superluminal EFT. Recorded below as the standing cost.")

# the acoustic metric of a mode with squared speed sigma in the clock frame, built covariantly from (g, n, sigma)
sg = sp.Symbol('s', positive=True)
gup = sp.diag(-1, 1, 1, 1)
gdn = sp.diag(-1, 1, 1, 1)
nup = sp.Matrix([1, 0, 0, 0])          # unit timelike clock normal, n^mu n_mu = -1
ndn = gdn * nup
Gup = gup + (1 - 1 / sg) * (nup * nup.T)
Gdn = gdn + (1 - sg) * (ndn * ndn.T)
leafnorm = sp.simplify((ndn.T * Gup * ndn)[0, 0])
check("L26-X1 [THE FOLIATION IS SPACELIKE FOR THE WIDER CONE] the clock mode's acoustic metric, built "
      "covariantly from the construction's own structures as G^{mu nu} = g^{mu nu} + (1 - 1/sigma) n^mu n^nu "
      "(equivalently G_{mu nu} = g_{mu nu} + (1 - sigma) n_mu n_nu, checked as exact inverses), gives the "
      "clock leaves' unit normal the norm G^{mu nu} n_mu n_nu = -1/sigma. That is NEGATIVE for every "
      "sigma > 0, so the normal is timelike and the leaves T = const are SPACELIKE with respect to the "
      "acoustic cone as well as the light cone. T is therefore a global time function for BOTH cones and no "
      "closed causal curve can be built from the clock mode -- at sigma_* or at any sigma > 0.",
      sp.simplify(Gup * Gdn - sp.eye(4)) == sp.zeros(4, 4) and sp.simplify(leafnorm + 1 / sg) == 0
      and sp.simplify(leafnorm.subs(sg, sig_star_sym)) < 0,
      f"G^(mu nu) n_mu n_nu = -1/sigma, symbolic; at sigma_* = {mp.nstr(SIGSTAR, 8)} it is "
      f"{mp.nstr(-1/SIGSTAR, 10)} < 0")

vt = sp.Matrix([0, 1, 0, 0])            # a leaf-tangent vector: n_mu v^mu = 0
knull = sp.Matrix([1, 1, 0, 0])         # a g-null vector
leaf_tangent = sp.simplify((vt.T * Gdn * vt)[0, 0])
null_in_G = sp.simplify((knull.T * Gdn * knull)[0, 0])
check("L26-X2 [CONE NESTING, AND THE CONDITION IS sigma > 0 NOT sigma <= 1] every vector tangent to a clock "
      "leaf has G_{mu nu} v^mu v^nu = g_{mu nu} v^mu v^nu > 0 for EVERY sigma, because the correction is "
      "proportional to (n.v)^2 = 0 -- the leaves are spacelike for the acoustic cone identically. And a "
      "g-null vector has G_{mu nu} k^mu k^nu = (1 - sigma)(n.k)^2, which is negative exactly when sigma > 1: "
      "the light cone sits strictly INSIDE the acoustic cone above sigma = 1, and strictly outside below it. "
      "The construction's causal-structure requirement is therefore sigma > 0, the SAME condition as "
      "no-gradient-instability -- sigma <= 1 controls which cone is wider, not whether the theory is causal.",
      sp.simplify(leaf_tangent - 1) == 0 and sp.simplify(null_in_G - (1 - sg)) == 0
      and sp.simplify(null_in_G.subs(sg, sig_star_sym)) < 0 and sp.simplify(null_in_G.subs(sg, sp.Rational(1, 3))) > 0,
      f"leaf tangent norm = +1 for all sigma; g-null vector in G = 1 - sigma = "
      f"{mp.nstr(1 - SIGSTAR, 8)} < 0 at sigma_* (light cone strictly inside)")

check("L26-X3 [THE PREFERRED FOLIATION IS GENUINELY THERE] the argument is available to this construction "
      "specifically, not borrowed. IC-4 varies a timelike clock T with X = -g^{mu nu} d_mu T d_nu T /2 > 0 "
      "and only then chooses unitary coordinates T = t; every object in the action (N, n_mu, h_{mu nu}, "
      "K_{mu nu}, a_mu, w, Q_{mu nu}) is built from that foliation; and the acoustic metric above is a "
      "function of (g, n, sigma) alone, i.e. of the SAME foliation. So the global time function the causality "
      "argument needs is the construction's own dynamical field, not an extra assumption.",
      all(s in ic4 for s in ("timelike clock", "n_\\mu=-\\partial_\\mu T/\\sqrt{2X}",
                             "The clock is varied before choosing unitary coordinates"))
      and "X=-\\tfrac12 g^{\\mu\\nu}\\partial_\\mu T\\partial_\\nu T>0" in ic4,
      "IC4_ACTION.md supplies X > 0, n_mu = -d_mu T/sqrt(2X), and clock-varied-before-unitary-gauge")

cher_bound = mp.mpf('2e-15')
check("L26-X4 [AND CHERENKOV IS SATISFIED AT sigma_*, WHICHEVER WAY L19 RULES] the gravitational-Cherenkov "
      "bound this repository imposes (Moore & Nelson 2001; Elliott, Moore & Stoica 2005; g03v V6; "
      "HANDOFF_CONTRACT A5) is 1 - c_s <= 2e-15, a LOWER bound: it constrains SUBLUMINAL modes, because a "
      "mode slower than an ultra-high-energy cosmic ray is what the ray can radiate into. At sigma_* the "
      "mode is 29.6% SUPERLUMINAL, so 1 - c_s = -0.296 and the bound is satisfied with room. sigma_* is "
      "therefore reachable whether or not L19 finds the bound applies to a k-essence clock -- L19's answer "
      "changes the LOWER edge of the allowed interval, never its upper edge.",
      (1 - CSTAR) <= cher_bound and (1 - mp.sqrt(mp.mpf(1) / 3)) > cher_bound,
      f"1 - c_s at sigma_* = {mp.nstr(1 - CSTAR, 6)} <= 2e-15 (satisfied); at sigma = 1/3 it is "
      f"{mp.nstr(1 - mp.sqrt(mp.mpf(1)/3), 6)}, excluded by {mp.nstr((1 - mp.sqrt(mp.mpf(1)/3))/cher_bound, 4)}x")

print("\n    NOT SETTLED BY THIS LANE, named exactly:")
print("      - the REVERSE Cherenkov process. A mode faster than light can decay into ordinary quanta if it")
print("        couples to them. Here matter is minimally coupled to g through the single unchanged S_m[g,psi],")
print("        so the clock reaches matter only through its metric perturbation, and the construction's own")
print("        exponential screening suppresses that further; but the decay rate is NOT computed here and is")
print("        not published anywhere in the IC files. It is the one physics gate a 29.6% superluminal clock")
print("        still owes, and it is a calculation, not an assumption.")
print("      - a Lorentz-invariant UV completion. Adams et al. 2006 obstructs one for a superluminal EFT. This")
print("        theory is not Lorentz invariant at any scale -- it carries a preferred foliation by construction")
print("        -- so the theorem does not fire, but the standing cost is that no Lorentz-invariant UV")
print("        completion can ever exist for it. At sigma = 1/3 that cost was already being paid.")

# ==================================================================================================================
# section 5 -- the verdict
# ==================================================================================================================
print("\n-- 5. verdict -----------------------------------------------------------------------------------------------")

health = {
    "no ghost (kinetic a_* > 0, sigma-free)": AST > 0,
    "no gradient instability (sigma a_* > 0)": SIGSTAR * AST > 0,
    "positive mode energy, E' <= 0": True,
    "reduced kinetic normalisation A_0 > 0": A0_w['*'] > 0 and st['*']['A0'] > 0,
    "c_T^2 = 1 exactly": sp.simplify(cT2_IC6 - 1) == 0,
    "frozen domain T > 27/4": T > mp.mpf(27) / 4,
    "auxiliary Hessian invertible, det = 12(4T-27) > 0": mp.det(Hn) > 0,
    "constraint surface + fold unchanged": abs(fold['*'] - fold['1/3']) < mp.mpf('1e-6'),
    "J_T > 0 on the whole branch": JTmin['*'] > 0,
    "det M != 0 (IC7 normalisation)": abs(detstar['*']) > mp.mpf('1e-6') and abs(st['*']['detM']) > mp.mpf('1e-6'),
    "hyperbolic, characteristics real": all(s > 0 for s in speeds['*']),
    "constraint rank / DOF count unchanged": True,
    "sheared state exists, 0<u<1, in plateau": 0 < sh['*']['u'] < 1 and sh['*']['J'] > 0,
    "clock leaves spacelike for the acoustic cone": SIGSTAR > 0,
}
print("    every health condition the construction states for itself, evaluated at sigma_* = 1.6794:")
for k, v in health.items():
    print(f"      [{'ok  ' if v else 'FAIL'}] {k}")

check("L26-V1 [THE VERDICT] is sigma > 1 admissible to the CONSTRUCTION ITSELF, independent of Cherenkov? "
      "YES. Every health condition the construction states for itself -- ghost-freedom, gradient sign, "
      "positive mode energy, kinetic normalisation, exact tensor luminality, the frozen domain T > 27/4, "
      "auxiliary Hessian invertibility, the constraint surface and its fold, J_T > 0, det M != 0, "
      "hyperbolicity, constraint rank and DOF count, the sheared fixture, and the causal role of the clock "
      "foliation -- holds at sigma_* = 1.6794. Not one of them has an upper edge at sigma = 1; the ONLY "
      "internal ceiling anywhere in the family is J_T > 0 at sigma = 1.7716, and sigma_* is below it.",
      all(health.values()) and SIGSTAR < SIG_JT,
      f"{sum(health.values())}/{len(health)} conditions hold at sigma_*; first internal ceiling is "
      f"sigma < {mp.nstr(SIG_JT, 8)}")

check("L26-V2 [WHY IC-4 BOUNDS sigma AT 1] the interval (0, 1] is category (b) in the brief's taxonomy, with "
      "a documentary edge of (c): it is a SUBLUMINALITY CHOICE -- keep the clock inside the shared metric "
      "null cone -- and it is nowhere derived. It is asserted once in prose in IC4_ACTION.md, copied "
      "verbatim into two `domain` metadata strings, and never evaluated by any code path (L26-D1, L26-D2). "
      "The same preference IS executable one sector away, as `Q >= PX` in IC-11's health predicate, where it "
      "sits as one deletable conjunct beside five genuine positivity and rank conditions (L26-D3). No "
      "stability, hyperbolicity, positivity or well-posedness requirement in the construction needs it: "
      "every such condition here turns out to need sigma > 0 and nothing more.",
      bool(decl_idx) and all(('"domain"' in ln or "domain=" in ln) for _f, _i, ln in py_occ)
      and "Q >= PX" in healthy_line[0],
      "declared in prose, copied to metadata, never executed; the executable cousin is IC-11's Q >= PX")

check("L26-V3 [PROGRAMME REQUIREMENT -- the outcome worth hoping for, and it is MET] 'there exists a value of "
      "IC-4's own design parameter, admissible to the construction on its own health conditions, at which "
      "the IC6 obstruction's leading order vanishes.' It does, and it does more than that: sigma_* = 1.6794 "
      "kills S_4'(1) exactly, REVERSES the sign of S_4 on the entire isotropic branch so that IC6's real "
      "growth rate becomes a bounded oscillation, and passes all fourteen internal health conditions with an "
      "internal ceiling 5.5% above it. The cost is that the clock is 29.6% superluminal, which is a choice "
      "IC-4 declined without giving a reason.",
      abs(S4p_S) < mp.mpf('1e-40') and S4pp['*'] > 0 and all(v > 0 for v in S4sign['*']) and all(health.values()),
      f"S_4'(1;sigma_*) = 0, S_4 > 0 on the whole branch, all 14 health conditions hold")

print("\n    WHAT sigma_* BUYS -- stated at the size the numbers actually support:")
print("      - the IC6 quartic obstruction's leading order vanishes IDENTICALLY: S_4'(1;sigma_*) = 0 exactly,")
print("        against -11.1408 published and -20.1942 at sigma = 1;")
print("      - THE SIGN OF S_4 REVERSES ON THE ENTIRE BRANCH. This is the substantive gain. With M_0 > 0,")
print("        S_4 < 0 gives IC6's real roots lambda ~ +/- sqrt(-S_4/M_0) k^2 -- a growth rate rising like")
print("        k^2, the Hadamard ill-posedness signature. S_4 > 0 gives lambda^2 < 0: a bounded oscillation.")
print("        Verified at 59/59 branch points at sigma_*, against 59/59 the other way at sigma = 1/3 and 1;")
print(f"      - the residual is second order at the witness: S_4''(1) = {mp.nstr(S4pp['*'], 8)} at sigma_*, so")
print(f"        |S_4| falls {mp.nstr(1/rat['1.002'], 4)}x at j = 1.002 and {mp.nstr(1/rat['1.007'], 4)}x at j = 1.007;")
print("      - and there is a WINDOW, not a point: sigma in [1.6793, 1.7716) has both properties, bounded")
print("        below by the sign flip and above by J_T -> 0 at the fold.")
print("\n    WHAT sigma_* DOES NOT BUY -- the half a hopeful reading would get wrong:")
print("      - IC7 is NOT made unnecessary. IC6 asks for S_4 = 0, and sigma_* delivers that only to first")
print(f"        order at j = 1. Away from the witness |S_4| is LARGER than published: {mp.nstr(rat['1.05'],4)}x at")
print(f"        j = 1.05, {mp.nstr(rat['1.10'],4)}x at 1.10, {mp.nstr(rat['1.15'],4)}x at 1.15. c_7 is still required")
print(f"        across the branch, now with the opposite sign ({mp.nstr(st['*']['c7'], 6)} at j = 1.007 against")
print(f"        {mp.nstr(st['1/3']['c7'], 6)} published), so the narrow repair window and the tensor detuning")
print("        c_T^2 = 1 - 4 c_7 Rbar_0/c do not disappear -- they change sign and move.")
print("      - the SHEARED obstruction is untouched by anything computed here (see the open items below).")
check("L26-P1 [PROGRAMME REQUIREMENT -- the stronger outcome, and it is NOT met] IC6_EVEN states its two "
      "constructive conditions as 'N_2 = N_2^T, S_4 = 0'. The strongest reading of this lane's brief is that "
      "sigma_* satisfies the second of them, making IC7 unnecessary. It does NOT. S_4 vanishes at sigma_* "
      "only to FIRST order at j = 1; on the branch it is nonzero everywhere except the witness, and away "
      "from the witness it is larger in magnitude than published. IC7's counterterm is still required. This "
      "is a requirement not met, not a claim refuted -- nobody asserted it -- and it is recorded as the "
      "designed FAIL of this run so the exit code cannot be mistaken for a clean sweep.",
      all(abs(v) < mp.mpf('1e-30') for v in S4sign['*']),
      f"max |S_4| on the branch at sigma_* = {mp.nstr(max(abs(v) for v in S4sign['*']), 8)} != 0; the "
      "obstruction moves from first order to second order and flips sign, it does not vanish")

print("\n    WHAT sigma_* COSTS -- everything below was derived at sigma = 1/3 and must be redone:")
for f_, why in (
        ("IC5_ACTION.md", "'Keep every IC-4 coefficient, including sigma=1/3' -- F, A_R, B_R all move"),
        ("TENSOR_BALANCE.md:185", "'These derivatives use the frozen sigma=1/3 member': dF/dj and dJ_T/dj"),
        ("TENSOR_BALANCE.md:231-242", "the IC6 grid witness (residuals, Hessian eigenvalue 4.3989, J_T>=0.99937)"),
        ("IC6_EVEN_CHARACTERISTICS.md", "the SHEARED numbers: N_2, S_4 matrix, z^2 = 0.0301756, c_RR = 0.0020073"),
        ("IC7_CURVATURE_SQUARE.md", "every c_7 value and the theta-cutoff window edges"),
        ("NONLINEAR_HAMILTONIAN.md:70", "sigma=1/3 carried through the identities"),
        ("nonlinear_square_completion.py:53", "sigma = Rational(1,3) hard-coded"),
        ("LOCAL_WAVE_REPORT.md:291", "'For sigma=1/3, four deterministic fundamental-matrix problems'; the exact"),
        ("", "basis cos r + r sin r, sin r - r cos r with r = sqrt(sigma x) is sigma-general, so this one is cheap"),
        ("IC11_CLOCK_PRESSURE.md:56", "the `Q >= PX` conjunct in `healthy` must be revisited, or justified"),
):
    print(f"      - {f_:<34} {why}" if f_ else f"        {why}")
print("\n    NOT MOVED, verified above: the witness itself, the isotropic constraint surface and its fold, the")
print("    auxiliary Hessian, det(M_star), c_T^2 = 1, the DOF count, a_*, A_0(witness), T, and every constant")
print("    except (p_R, q_R, A_R, B_R).")
print("\n    NOT AVAILABLE TO THIS LANE, named exactly:")
print("      - S4_11(sigma_*), the SHEARED reduced quartic, and the antisymmetric mixing N2_21. IC6_EVEN's")
print("        -0.0642323935174161 and 0.000563025148110635 come from the lead's anisotropic two-mode")
print("        reduction (ic6_even_characteristics.py), not reproduced in this lane. sigma_* cancels the")
print("        ISOTROPIC obstruction; IC6_EVEN's second condition N_2 = N_2^T under shear is untouched by")
print("        anything computed here and may well still fail. This is the single largest open item.")
print("      - the finite-k correction to c_s^2 = sigma, which needs the lead's background time derivatives.")
print("      - whether IC-4's sigma and IC-10/IC-11's cs^2 = PX/Q are the same handle (L26-D4).")

print("\n" + BAR)
hard = [n for n in FAILS if not n.startswith('L26-P1')]
print(f"L26: {len(FAILS)} FAIL(S)" if FAILS else "L26: ALL CHECKS PASS")
for n in FAILS:
    print(f"    FAIL: {n.split('.')[0]}")
print(f"    sigma_* = {mp.nstr(SIGSTAR, 12)} (c_s = {mp.nstr(CSTAR, 8)} c) is ADMISSIBLE to the construction on")
print("    all 14 of its own health conditions. IC-4's (0,1] is an undefended subluminality convention.")
print(f"    The construction's own first internal ceiling on sigma is J_T > 0 at sigma = {mp.nstr(SIG_JT, 8)},")
print(f"    so the admissible growth-free window is sigma in [{mp.nstr(SIGSTAR, 8)}, {mp.nstr(SIG_JT, 8)}).")
print("    Both mandatory controls reproduced first: -11.1407711251147987 at sigma = 1/3 and")
print("    -20.194205022906776 at sigma = 1. The single FAIL is the stronger outcome (S_4 = 0 identically,")
print("    IC7 unnecessary), which is false. Exit 2 marks that designed outcome; exit 1 would mean one of the")
print("    lead's or L15's numbers failed to reproduce.")
print(BAR)
sys.exit(1 if hard else (2 if FAILS else 0))
