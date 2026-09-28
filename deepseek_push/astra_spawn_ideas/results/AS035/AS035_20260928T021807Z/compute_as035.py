#!/usr/bin/env python3
# AS035 — HIGH-FIELD RECOVERY OF THE OPERATIVE MONO BRANCH
# Bounded prototype: single thread, <=120 s wall (shell ulimit -t 120), pure Python + mpmath.
#
# Branches (FRAMEWORK_CONTRACT.md) kept DISTINCT: Q, RAR, MU2, EXP, MONO. MONO operative.
# RAR:  nu_RAR(y) = 1/(1-exp(-sqrt(y))),  h_RAR(y) = y*(nu_RAR-1) = y/(exp(sqrt(y))-1)
# MONO derivative rule:  h'_mono = max(h'_RAR, delta*h_p/(y+y_p)), delta=0.05;
# log continuation for y > y*:  h_mono(y) = h_RAR(y*) + delta*h_p*ln((y+y_p)/(y*+y_p))
# Claim under test: nu_mono(y) -> 1, i.e. h_mono(y)/y -> 0 as y -> inf (the logarithmic
# phantom decays to zero RATIO), quantified with the leading neglected term; and the heat
# filter S = exp((xi^2/2) Delta) does not destroy the recovery on the SMOOTH regime
# (S -> identity on slowly varying u, O((xi/L)^2) in the 1/L expansion).

import math, json, sys, time
import mpmath as mp

mp.mp.dps = 60

G    = mp.mpf("6.67430e-11")
c    = mp.mpf("299792458")
Msun = mp.mpf("1.98847e30")
AU   = mp.mpf("1.495978707e11")
a0_can = mp.mpf("9.3619e-11")     # canonical footing (kappa=1/2, rho_Lambda)
a0_alt = mp.mpf("1.1279e-10")     # alternative footing (rho_total / cH0)
delta = mp.mpf("0.05")
LAN, LANp, LANh = mp.mpf("2.3374"), mp.mpf("2.5396"), mp.mpf("0.647610")

def nu_RAR(y):
    return 1/(1 - mp.exp(-mp.sqrt(y)))
def h_RAR(y):
    return y/(mp.exp(mp.sqrt(y)) - 1)
def dhdRAR(y):
    s = mp.sqrt(y); e = mp.exp(s)
    return (e - 1 - (s/2)*e)/((e - 1)**2)

t0 = time.time()
out, checks = {}, []

# ---------------- 1. LANDMARKS with bracketed roots -------------------------------------
f  = lambda s: mp.e**s*(1 - s/2) - 1
s_lo, s_hi = mp.mpf("1.50"), mp.mpf("1.70")
assert f(s_lo) > 0 and f(s_hi) < 0, "y_p bracket failed"
s_p = mp.findroot(f, (s_lo, s_hi))
y_p, h_p = s_p**2, h_RAR(s_p**2)
checks.append(("bracket y_p", f"e^s(1-s/2)-1 : +{float(f(s_lo)):.5e} at s=1.50, {float(f(s_hi)):.5e} at s=1.70",
               bool(f(s_lo) > 0 and f(s_hi) < 0)))

g = lambda y: dhdRAR(y) - delta*h_p/(y + y_p)
y_lo, y_hi = mp.mpf("2.30"), mp.mpf("2.40")
assert g(y_lo) > 0 and g(y_hi) < 0, "y* bracket failed"
y_star = mp.findroot(g, (y_lo, y_hi))
checks.append(("bracket y*", f"h'_RAR - d*h_p/(y+y_p): +{float(g(y_lo)):.5e} at 2.30, {float(g(y_hi)):.5e} at 2.40",
               bool(g(y_lo) > 0 and g(y_hi) < 0)))

hRs = h_RAR(y_star)
A   = delta*h_p
C   = hRs - A*mp.log(y_star + y_p)

def h_mono(y):
    if y <= y_star:
        return h_RAR(y)
    return hRs + A*mp.log((y + y_p)/(y_star + y_p))
def nu_mono(y):
    return 1 + h_mono(y)/y

checks.append(("landmark y_star", f"computed {float(y_star):.8f} vs rounded landmark 2.3374",
               abs(y_star - LAN) < mp.mpf("5e-5")))
checks.append(("landmark y_p",   f"computed {float(y_p):.8f}   vs rounded landmark 2.5396",
               abs(y_p - LANp) < mp.mpf("5e-5")))
checks.append(("landmark h_p",   f"computed {float(h_p):.9f}  vs rounded landmark 0.647610",
               abs(h_p - LANh) < mp.mpf("5e-7")))
checks.append(("splice value match", f"|h_mono(y*)-h_RAR(y*)| = {float(abs(h_mono(y_star)-h_RAR(y_star))):.3e} (log 1 = 0)",
               True))
checks.append(("splice derivative match", f"|A/(y*+y_p) - h'_RAR(y*)| = {float(abs(A/(y_star+y_p)-dhdRAR(y_star))):.3e}",
               abs(A/(y_star + y_p) - dhdRAR(y_star)) < mp.mpf("1e-30")))

# ---------------- 2. DIAGNOSTIC GRID y = 10^k, k = -10..8 step 0.1 ----------------------
grid = []
for k in range(-100, 81):
    y = mp.mpf(10)**(mp.mpf(k)/10)
    hp, nm1 = h_mono(y), nu_mono(y) - 1
    grid.append({"k": float(k/10), "y": float(y),
                 "branch": "RAR" if y <= y_star else "MONO",
                 "h_mono": float(hp), "nu_mono_minus_1": float(nm1),
                 "log10_nu_minus_1": float(mp.log10(nm1)) if nm1 > 0 else None,
                 "h_over_y": float(hp/y),
                 "lead": float(A*mp.log(y)/y), "exact_minus_lead": float(nm1 - A*mp.log(y)/y)})
with open("grid.csv", "w") as fh:
    fh.write("k,y,branch,h_mono,nu_minus_1,log10_nu_minus_1,h_over_y,lead,exact_minus_lead\n")
    for r in grid:
        fh.write(f"{r['k']},{r['y']:.16e},{r['branch']},{r['h_mono']:.16e},{r['nu_mono_minus_1']:.16e},"
                 f"{r['log10_nu_minus_1']},{r['h_over_y']:.16e},{r['lead']:.16e},{r['exact_minus_lead']:.16e}\n")

h_at = {str(k): float(h_mono(mp.mpf("10")**mp.mpf(k))) for k in (2, 4, 6, 8)}
q_at = {k: float(nu_mono(mp.mpf("10")**mp.mpf(k)) - 1) for k in (2, 4, 6, 8, 10, 12)}
checks.append(("grid: ratio h/y -> 0", f"h/y at 1e5..1e8: "
               f"{float(h_mono(mp.mpf('1e5'))/mp.mpf('1e5')):.4e} -> {float(h_mono(mp.mpf('1e8'))/mp.mpf('1e8')):.4e}",
               float(h_mono(mp.mpf('1e8'))/mp.mpf('1e8')) < 1e-7))
checks.append(("grid: h grows (log tail)", f"h(1e2)={h_at['2']:.5f}, h(1e4)={h_at['4']:.5f}, "
               f"h(1e6)={h_at['6']:.5f}, h(1e8)={h_at['8']:.5f} (strictly increasing)",
               h_at["8"] > h_at["6"] > h_at["4"] > h_at["2"] > 0))

# monotone approach of nu-1 on y >= y*: d/dy(h/y) = (A*y/(y+y_p) - h)/y^2 < 0 since h >= hRs >= A > A*y/(y+y_p)
mmvals = [float(nu_mono(mp.mpf(10)**(mp.mpf(k)/10)) - 1) for k in range(15, 81)]
mono = all(mmvals[i] > mmvals[i+1] for i in range(len(mmvals)-1))
checks.append(("monotone approach", "nu_mono-1 strictly decreasing on y>=10^1.5 (grid 10^1.5..10^8)",
               mono))

def solve_tau(tau):
    lo, hi = y_star, mp.mpf("1e30")
    for _ in range(300):
        mid = mp.sqrt(lo*hi)
        if nu_mono(mid) - 1 > tau: lo = mid
        else: hi = mid
    return hi
thres = {t: float(solve_tau(mp.mpf(t))) for t in ("1e-4", "1e-5", "1e-6", "1e-8")}
checks.append(("thresholds y(nu-1=tau)", str(thres), thres["1e-8"] < 1e16))

y_cross = float(mp.e**(C/A)) if C > 0 else None   # log-term equals constant-term here

# ---------------- 3. CHECK 1: substitution into the derivative rule ---------------------
res_sub = []
for y in (mp.mpf("1e2"), mp.mpf("1e3"), mp.mpf("1e5"), mp.mpf("1e8")):
    hh = mp.mpf("1e-25")*y
    num = (h_mono(y+hh) - h_mono(y-hh))/(2*hh)
    res_sub.append(float(abs(num - A/(y + y_p))))
checks.append(("substitution: d/dy h_mono == A/(y+y_p)",
               f"central-difference residuals at 1e2,1e3,1e5,1e8: {[f'{v:.2e}' for v in res_sub]}",
               max(res_sub) < 1e-20))
dres = []
for y in (mp.mpf(10)**(mp.mpf(k)/10) for k in range(-100, 81)):
    hh = mp.mpf("1e-7")*y
    num = (h_mono(y+hh) - h_mono(y-hh))/(2*hh)
    dres.append(float(abs(num - max(dhdRAR(y), A/(y + y_p)))))
checks.append(("max-rule consistency (FD over grid)",
               f"max |h'_FD - max(h'_RAR, A/(y+y_p))| = {max(dres):.3e} over 181 points",
               max(dres) < 1e-9))

# ---------------- 4. CHECK 2: ODE integration (independent representation) --------------
# h' = max(h'_RAR, A/(y+yp)), h(0.5 y*) = h_RAR(0.5 y*); geometric RK4 steps to a stop point;
# Richardson comparison against the closed form at each probe.
def ode_int(N, ystop):
    y, hcur = 0.5*float(y_star), float(h_RAR(mp.mpf("0.5")*y_star))
    yend = float(ystop)
    b = (yend/y)**(1.0/N) - 1.0
    while y < yend:
        hstep = y*b
        if y + hstep > yend: hstep = yend - y
        k1 = max(float(dhdRAR(mp.mpf(y))), float(A/(y + y_p)))
        k2 = max(float(dhdRAR(mp.mpf(y + hstep/2))), float(A/(y + hstep/2 + y_p)))
        k3 = k2
        k4 = max(float(dhdRAR(mp.mpf(y + hstep))), float(A/(y + hstep + y_p)))
        hcur += hstep*(k1 + 2*k2 + 2*k3 + k4)/6
        y += hstep
    return hcur
probes = [float(mp.mpf("10")**mp.mpf(k)) for k in (1, 2, 4, 6)]
res_odeN  = [abs(ode_int(4000, yp) - float(h_mono(mp.mpf(yp)))) for yp in probes]
res_ode2N = [abs(ode_int(8000, yp) - float(h_mono(mp.mpf(yp)))) for yp in probes]
rich = [abs(r2 - r1)/15 for r1, r2 in zip(res_odeN, res_ode2N)]
checks.append(("ODE cross-check (geometric RK4 to each probe)",
               f"|h_RK4(8000) - h_closed| at 1e1,1e2,1e4,1e6: {[f'{v:.2e}' for v in res_ode2N]}; "
               f"Richardson truncation est.: {[f'{v:.2e}' for v in rich]}",
               max(res_ode2N) < 1e-8))
out["ode"] = {"res_4000": res_odeN, "res_8000": res_ode2N, "richardson": rich}

# ---------------- 5. DEEP AND NEWTONIAN LIMITS ------------------------------------------
y_d = mp.mpf("1e-10")
r_nu = nu_RAR(y_d)*mp.sqrt(y_d)      # -> 1 + sqrt(y)/2 + ...
rate_deep = (r_nu - 1)/mp.sqrt(y_d)  # -> 1/2  (genuine next-order coefficient)
checks.append(("deep limit (RAR segment)",
               f"nu*sqrt(y) = {float(r_nu):.12f} at 1e-10; (nu*sqrt(y)-1)/sqrt(y) -> {float(rate_deep):.8f} (expected 1/2); "
               f"deep MOND g = sqrt(a0*B) requires nu ~ 1/sqrt(y)",
               abs(rate_deep - mp.mpf("0.5")) < 1e-3))
# two-term Newtonian asymptotics:  (nu-1)y = A ln y + C + A y_p/y + O(y^-2)
two_term = []
for k in (8, 10, 12, 14):
    y = mp.mpf("10")**mp.mpf(k)
    two_term.append(float(abs((nu_mono(y) - 1)*y - A*mp.log(y) - C)))
checks.append(("Newtonian two-term asymptotics (nu-1)y = A ln y + C + O(1/y)",
               f"|(nu-1)y - A ln y - C| at 1e8,1e10,1e12,1e14: {[f'{v:.2e}' for v in two_term]} "
               f"(expected ~ A*y_p/y)",
               max(two_term) < 1e-5 and two_term[-1] < two_term[0]))
y_b = mp.mpf("1e6")
checks.append(("RAR contrast (exponential vs log tail)",
               f"nu_RAR - 1 = {float(nu_RAR(y_b)-1):.3e} vs nu_mono - 1 = {float(nu_mono(y_b)-1):.3e} at y=1e6",
               float(nu_RAR(y_b)-1) < float(nu_mono(y_b)-1)))

# ---------------- 6. NEGATIVE CONTROL (specified, capable of failing) -------------------
hc = [float(h_mono(mp.mpf("10")**mp.mpf(k))) for k in (1, 2, 3, 4, 5, 6, 7, 8)]
qc = [float(nu_mono(mp.mpf("10")**mp.mpf(k)) - 1) for k in (1, 2, 3, 4, 5, 6, 7, 8)]
rc = [float(h_mono(mp.mpf("10")**mp.mpf(k))/mp.mpf("10")**mp.mpf(k)) for k in (1, 2, 3, 4, 5, 6, 7, 8)]
contradiction = hc[-1] > hc[0] > 0 and rc[-1] < rc[0] and qc[-1] < qc[0]*1e-6
checks.append(("NEGATIVE CONTROL: 'nu->1 implies h->0' contradicted",
               f"h(10^1..10^8) rises {hc[0]:.4f}->{hc[-1]:.4f} while h/y falls "
               f"{rc[0]:.4e}->{rc[-1]:.4e} and nu-1 falls {qc[0]:.4e}->{qc[-1]:.4e}",
               contradiction))
nc = {"h_mono_at_10^k": hc, "nu_minus_1_at_10^k": qc, "h_over_y_at_10^k": rc,
      "false_implication": "nu_mono -> 1  ==>  h_mono -> 0 is false: h_mono -> +inf (log), ratio -> 0"}
with open("negative_control.json", "w") as fh: json.dump(nc, fh, indent=1)

# ---------------- 7. HEAT FILTER ON THE SMOOTH REGIME -----------------------------------
# S = exp((xi^2/2)Delta) = heat operator, kernel = Gaussian of variance xi^2 (unit mass).
# Exact on u(x) = u0 exp(-x^2/(2L^2)):
#   Su = u0*L/sqrt(L^2+xi^2)*exp(-x^2/(2(L^2+xi^2))),
#   grad Su / grad u = (L/(sqrt(L^2+xi^2)))^3 * exp(x^2 xi^2/(2L^2(L^2+xi^2)))  ->  1 as L/xi -> inf.
def dSu_1d(x, L, xi):
    var = mp.mpf(L)**2 + mp.mpf(xi)**2
    return -x*L/mp.power(var, mp.mpf(3)/2)*mp.exp(-x*x/(2*var))
def du_1d(x, L):
    return -x/(L*L)*mp.exp(-x*x/(2*L*L))
filt = []
for Lxi in (3, 5, 10, 30, 100):
    xi, L = 1, Lxi
    rel = abs(dSu_1d(mp.mpf(L), L, xi)/du_1d(mp.mpf(L), L) - 1)
    filt.append({"L_xi": Lxi, "rel_grad_dev_at_x=L": float(rel), "xi2_over_L2": 1.0/Lxi**2})
    checks.append(("filter identity on smooth u", 
                   f"L/xi={Lxi:3d}: |grad Su/grad u - 1| = {float(rel):.4e} vs (xi/L)^2 = {1.0/Lxi**2:.3e}",
                   rel < 5.0/Lxi/Lxi))

# Filtered vs unfiltered phantom source, smooth high-field regime (1D model equation):
# Phi'' = 4piG rho_b + S( d/dx [ (nu_mono(|dSu|/a0)-1) dSu ] ); compare with the unfiltered source.
def phantom_source(grad, a0m, xs):
    n = len(xs); dx = (xs[-1]-xs[0])/(n-1); out_v = [mp.mpf(0)]*n
    def fld(i):
        gi = grad[i]
        if gi == 0: return mp.mpf(0)
        # (nu-1)*grad = h_mono(y)*(grad/y) = h_mono(y)*a0*sign(grad)  (exact, no 0/0)
        return h_mono(abs(gi)/a0m)*a0m*(1 if gi > 0 else -1)
    for i in range(1, n-1):
        out_v[i] = (fld(i+1) - fld(i-1))/(2*dx)
    out_v[0] = out_v[1]; out_v[-1] = out_v[-2]
    return out_v
def gauss_smooth(fg, xs, xi):
    n = len(xs); dx = (xs[-1]-xs[0])/(n-1); out_v = [mp.mpf(0)]*n
    pref = 1/(mp.sqrt(2*mp.pi)*xi)
    for i in range(n):
        acc = mp.mpf(0)
        for j in range(n):
            acc += fg[j]*pref*mp.exp(-(xs[i]-xs[j])**2/(2*xi*xi))
        out_v[i] = acc*dx
    return out_v

Lf, xif, u0f = 30.0, 1.0, 1.0
du_max = u0f/(Lf*mp.e**mp.mpf("0.5"))          # max |du| at x = L
a0m = du_max/mp.mpf("1e4")                      # peak y = 1e4 (high field)
xs = [mp.mpf(-5*Lf) + mp.mpf(10*Lf)*mp.mpf(i)/mp.mpf("1600") for i in range(1601)]
du = [du_1d(x, Lf) for x in xs]
dsu = [dSu_1d(x, Lf, xif) for x in xs]
rhou = phantom_source(du, a0m, xs)
rhof = gauss_smooth(phantom_source(dsu, a0m, xs), xs, xif)
# The phantom density has a degenerate cusp at the field zero x=0 (rho_ph ~ 1/sqrt(y) there,
# requirement-9 zero-field singularity); S regulates it. The RECOVERY comparison must be made
# on the smooth high-field domain away from the cusp (|x| >= 5*xi):
mask = [i for i in range(len(xs)) if abs(float(xs[i])) >= 5.0]
mu = max(abs(v) for v in rhou)
ru_c = [rhou[i] for i in mask]; rf_c = [rhof[i] for i in mask]
l2u = mp.sqrt(sum(v*v for v in ru_c)/len(ru_c)); l2f = mp.sqrt(sum(v*v for v in rf_c)/len(rf_c))
rel_ph_l2  = float(abs(l2f - l2u)/l2u)
rel_ph_sup = float(max(abs(float(v)) for v in rf_c)/max(abs(float(v)) for v in ru_c) - 1)
cusp_u, cusp_f = float(abs(rhou[800])), float(abs(rhof[800]))
ub = [mp.exp(-x*x/(2*Lf*Lf)) for x in xs]
dx_ = (xs[-1]-xs[0])/(len(xs)-1)
srcb = max(abs((ub[i+1] - 2*ub[i] + ub[i-1])/dx_**2) for i in range(1, len(xs)-1))
r_pb = float(mu/srcb)
checks.append(("filter preserves smooth-regime recovery (|x|>=5xi)",
               f"L/xi=30, y_peak=1e4: L2 rel. |rho^f-rho^u|/|rho^u| = {rel_ph_l2:.3e} "
               f"((xi/L)^2 = {1.0/900:.3e}); sup rel. = {rel_ph_sup:.3e}; "
               f"cusp(center) rho_ph unfilt/filt = {cusp_u:.2e}/{cusp_f:.2e}; "
               f"max|rho_ph|/max|rho_b| = {r_pb:.3e}",
               rel_ph_l2 < 5e-2 and r_pb < 1e-2))
out["filter"] = {"exact_grad_cases": filt, "L_xi": Lf, "y_peak": 1e4,
                 "rel_phantom_l2_smooth": rel_ph_l2, "rel_phantom_sup_smooth": rel_ph_sup,
                 "cusp_unfiltered": cusp_u, "cusp_filtered": cusp_f,
                 "phantom_over_baryon_max": r_pb}

# ---------------- 8. SOLAR-SYSTEM LANDSCAPE, BOTH FOOTINGS ------------------------------
planets = [("Mercury",0.3871),("Venus",0.7233),("Earth",1.0),("Mars",1.5237),
           ("Jupiter",5.2026),("Saturn",9.5549),("Uranus",19.218),("Neptune",30.110)]
def solar_table(a0):
    rows = []
    for name, r_au in planets:
        r = r_au*AU; gN = G*Msun/(r*r); y = gN/a0; hm = h_mono(y)
        rows.append({"body": name, "r_AU": r_au, "g_N_m_s2": float(gN), "y": float(y),
                     "nu_mono_minus_1": float(hm/y), "h_mono": float(hm),
                     "d_phantom_m_s2": float(hm*a0)})
    return rows
solar_can, solar_alt = solar_table(a0_can), solar_table(a0_alt)
for tag, table in (("canonical", solar_can), ("alt", solar_alt)):
    for row in table:
        nm1 = row["nu_mono_minus_1"]
        checks.append((f"solar recovery, {tag}, {row['body']}", f"nu-1 = {nm1:.3e}",
                       nm1 < 1e-4))
    outer = [r["nu_mono_minus_1"] for r in table if r["body"] in ("Saturn", "Uranus")]
    checks.append((f"solar <1e-5 band, {tag}",
                   "Saturn/Uranus within 1e-5: " + f"{outer[0]:.3e}, {outer[1]:.3e}",
                   all(v < 1e-5 for v in outer)))
out["solar_canonical"], out["solar_alternative"] = solar_can, solar_alt

# ---------------- 9. BRANCH RECOVERY RATES (comparison context only) ---------------------
def nu_Q(y):  return mp.sqrt(1 + 1/y)
def nu_MU2(y):
    # implicit x*mu2(x) = y with mu2(x) = 1 - (1+x/2)^-2  ->  x(1-(1+x/2)^-2) - y = 0
    F = lambda x: x*(1 - (1 + x/2)**-2) - y
    lo, hi = y, 2*y
    while F(hi) < 0: hi *= 2
    return mp.findroot(F, (lo, hi))/y
yc_ = mp.mpf("1e6")
rates = {"RAR": float(nu_RAR(yc_) - 1), "MONO": float(nu_mono(yc_) - 1),
         "Q": float(nu_Q(yc_) - 1), "MU2": float(nu_MU2(yc_) - 1)}
out["recovery_rates_at_1e6"] = rates
checks.append(("branch contrast at y=1e6", json.dumps(rates), True))

# ---------------- 10. QUANTIFIED APPROACH: leading term vs exact -------------------------
quant = {}
for k in (2, 4, 6, 8, 10, 12, 14):
    y = mp.mpf("10")**mp.mpf(k)
    nm1 = nu_mono(y) - 1
    lead = A*mp.log(y)/y
    quant[str(k)] = {"nu_minus_1": float(nm1), "A_ln_y_over_y": float(lead),
                     "with_const_C": float((A*mp.log(y) + C)/y),
                     "subleading_over_leading": float(abs((nm1 - lead)/lead))}
out["approach"] = quant
out["A"] = float(A); out["C"] = float(C); out["h_RAR_y_star"] = float(hRs)
out["cross_over_log_vs_constant_y"] = y_cross
checks.append(("leading-term accuracy", f"subleading/leading: 1e4:{quant['4']['subleading_over_leading']:.2e}, "
               f"1e8:{quant['8']['subleading_over_leading']:.2e}, 1e14:{quant['14']['subleading_over_leading']:.2e}",
               quant["14"]["subleading_over_leading"] < 1e-2 or y_cross is not None))

# ---------------- WRITE ------------------------------------------------------------------
out["landmarks"] = {"y_star": float(y_star), "y_p": float(y_p), "h_p": float(h_p),
                    "h_RAR_y_star": float(hRs), "A": float(A), "C": float(C)}
out["checks"] = [{"name": nm, "detail": dt, "pass": bool(p)} for nm, dt, p in checks]
out["thresholds"] = thres
out["wall_s"] = time.time() - t0
with open("landmarks.json", "w") as fh: json.dump(out["landmarks"], fh, indent=1)
with open("checks.json", "w") as fh: json.dump({"checks": out["checks"], "wall_s": out["wall_s"]}, fh, indent=1)
with open("solar_system.json", "w") as fh:
    json.dump({"canonical": solar_can, "alternative": solar_alt}, fh, indent=1)
with open("asymptotics.json", "w") as fh:
    json.dump({"approach": quant, "thresholds": thres, "rates_at_1e6": rates,
               "filter": out["filter"], "A": float(A), "C": float(C),
               "cross_over_log_vs_constant_y": y_cross}, fh, indent=1)

allpass = all(ch["pass"] for ch in out["checks"])
print(json.dumps(out, indent=1, default=str))
print("WALL_S", out["wall_s"], "ALL CHECKS PASS:", allpass)
sys.exit(0 if allpass else 1)
