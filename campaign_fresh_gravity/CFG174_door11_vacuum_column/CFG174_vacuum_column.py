# -*- coding: utf-8 -*-
"""CFG174 -- the owner's flowing Lambda-vacuum as a column budget (frozen: FROZEN_QUESTION.md, committed before this script).
Budget and scaling only, not a mechanism. MUTATE=1 sets t0 = 1 Gyr (the Q1 pass line must fail). kappa = 1/2 FITTED."""
import os, sys, math, json
import numpy as np, sympy as sp
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); MUTATE = int(os.environ.get("MUTATE", "0"))
tag = "" if MUTATE == 0 else "_MUTATE%d" % MUTATE
OUT = open(os.path.join(HERE, "CFG174_vacuum_column%s.out" % tag), "w", encoding="utf-8"); res = []; fails = 0
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n")
def check(t, st, meas, ok, lb=True):
    global fails
    res.append((t, bool(ok), lb)); fails += (not ok) and lb
    P("  [%s] %s %s" % ("PASS" if ok else ("FAIL" if lb else "FAIL(reported)"), t, st)); P("         measured: " + str(meas))
G = 6.6743e-11; C = 299792458.0; RHO_L = 5.8424e-27; MSUN = 1.98847e30; PC = 3.0856775814913673e16; MPC = 1e6 * PC; GYR = 3.15576e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; KAPPA = 0.5
H0 = 67.66 * 1e3 / MPC; OM = 0.3111; OL = 1 - OM
def age(z):  # flat LCDM, matter + Lambda
    f = lambda a: 1.0 / (a * H0 * math.sqrt(OM / a**3 + OL))
    return quad(f, 0, 1.0 / (1 + z), limit=200)[0]
t0 = age(0.0) if MUTATE != 1 else 1.0 * GYR
P("CFG174 (MUTATE=%d): t0 = %.3f Gyr; rho_L = %.4e kg/m3; H0 = 67.66, Om = 0.3111" % (MUTATE, t0 / GYR, RHO_L))
MSPC2 = MSUN / PC**2
# ---- Q1 symbolic
P("\n== Q1: the law's inner column vs the vacuum column swept at c over t0 ==")
a0s, Gs, Ms, r, rho, c, t, k = sp.symbols("a0 G M r rho c t kappa", positive=True)
x = r / sp.sqrt(Gs * Ms / a0s); Mc = Ms * (sp.sqrt(1 + x**2) - 1)
lead = sp.simplify(sp.series(Mc, r, 0, 3).removeO())
P("  M_c(<r) for r << r_M (P2 point mass): %s  (mass-independent: %s)" % (lead, not lead.has(Ms)))
Rsym = sp.simplify((a0s / (2 * sp.pi * Gs)).subs(a0s, k * c * sp.sqrt(Gs * rho)) / (rho * c * t))
P("  R = Sigma_M/(rho_L c t) with a0 = kappa c sqrt(G rho_L):  R = %s" % Rsym)
check("Q1a", "the inner column M_c(<r)/(pi r^2) = a0/(2 pi G) is independent of the baryon mass", str(lead), (not lead.has(Ms)) and sp.simplify(lead - a0s * r**2 / (2 * Gs)) == 0)
row = {}
for fn, a0 in A0.items():
    SigM = a0 / (2 * math.pi * G); col = RHO_L * C * t0; R = SigM / col
    row[fn] = dict(Sigma_M_Msun_pc2=SigM / MSPC2, column_Msun_pc2=col / MSPC2, R=R)
    P("  %-9s Sigma_M = %.1f Msun/pc2; rho_L c t0 = %.1f Msun/pc2; R = %.3f; u_min = %.3f c" % (fn, SigM / MSPC2, col / MSPC2, R, R))
    check("Q1b-" + fn, "0.1 <= R <= 1 (a light-speed flow over t0 carries enough vacuum column, no extra constant)", "R = %.3f" % R, 0.1 <= R <= 1.0)
P("  (declared in advance: this is the a0 ~ c sqrt(G rho_L) coincidence restated; a pass is not new evidence)")
# ---- Q2 shape
P("\n== Q2: deposit fraction the picture must supply, f(x) = M_c(<r) / (Sigma_M pi r^2) ==")
xs = np.array([0.1, 0.3, 1, 3, 10, 30])
f = (np.sqrt(1 + xs**2) - 1) / (xs**2 / 2)
for xi, fi in zip(xs, f): P("  x = %5.1f  f = %.4f" % (xi, fi))
slope = np.polyfit(np.log(xs[-3:]), np.log(f[-3:]), 1)[0]
check("Q2", "the needed deposit fraction falls as ~1/x at large x (a requirement the picture does not yet supply)", "d ln f / d ln x (x 3-30) = %.3f" % slope, -1.1 < slope < -0.85, lb=False)
# ---- Q3 accumulation reading
P("\n== Q3: accumulation reading, a0(z)/a0(0) = t(z)/t0 ==")
q3 = {}
for z in (0.85, 1.5, 2.5):
    ratio = age(z) / age(0.0); dla = math.log10(ratio); Hz = math.sqrt(OM * (1 + z)**3 + OL)
    q3[z] = dict(t_ratio=ratio, dlog_a0=dla, dlog_vflat=dla / 4, dlog_a0_H=math.log10(Hz))
    P("  z = %.2f  t/t0 = %.3f  dlog a0 = %+.3f  dlog v_flat = %+.3f   (flat: 0; a0 ~ H(z): %+.3f)" % (z, ratio, dla, dla / 4, math.log10(Hz)))
check("Q3", "the accumulation reading predicts a0 FALLING with z, opposite to both tested readings", "dlog a0(1.5) = %+.3f" % q3[1.5]["dlog_a0"], q3[1.5]["dlog_a0"] < -0.2, lb=False)
# ---- Q4 clusters
P("\n== Q4: clusters, column mass inside R500 vs needed dark mass (1 - 0.15) M500 ==")
rho_c = 3 * H0**2 / (8 * math.pi * G); q4 = []
for lm in (14.0, 14.5, 15.0):
    M5 = 10**lm * MSUN; R5 = (3 * M5 / (4 * math.pi * 500 * rho_c))**(1 / 3.0); need = 0.85 * M5
    for fn, a0 in A0.items():
        m_ss = a0 / (2 * math.pi * G) * math.pi * R5**2; m_full = RHO_L * C * t0 * math.pi * R5**2
        q4.append(dict(logM500=lm, footing=fn, R500_Mpc=R5 / MPC, steady_over_need=m_ss / need, full_over_need=m_full / need))
        P("  logM500 %.1f %-9s R500 %.2f Mpc  steady column/need = %.2f   full swept column/need = %.2f" % (lm, fn, R5 / MPC, m_ss / need, m_full / need))
ok4 = all(0.5 <= d["steady_over_need"] <= 2 for d in q4)
check("Q4", "steady column Sigma_M within a factor 2 of the needed cluster dark mass for logM500 14-15 (order-of-magnitude, cylinder vs sphere)", ", ".join("%.2f" % d["steady_over_need"] for d in q4), ok4, lb=False)
n = len(res); npass = sum(1 for r_ in res if r_[1])
P("\nSUMMARY CFG174 (MUTATE=%d): %d/%d checks pass; load-bearing failures = %d" % (MUTATE, npass, n, fails))
json.dump(dict(mutate=MUTATE, t0_Gyr=t0 / GYR, Q1=row, Q3={str(k_): v for k_, v in q3.items()}, Q4=q4, checks=[dict(id=a, ok=b, lb=c_) for a, b, c_ in res]),
          open(os.path.join(HERE, "CFG174_vacuum_column_results%s.json" % tag), "w"), indent=1)
OUT.close(); sys.exit(1 if fails else 0)
