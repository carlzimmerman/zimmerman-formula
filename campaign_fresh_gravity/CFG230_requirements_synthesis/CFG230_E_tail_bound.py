"""CFG230 script E (CROSS-CHECK of CFG188): R09 tail bound and Q2, R11 (yq)'. Definition adopted from the CFG188 script comments (read for
the definition only): the band is on g at fixed g_N; the anomaly s(y_g) = (g - g_N)/a0 is non-decreasing when (y q)' >= 0, so the tail
>= max over y_N of (eps g_target(y_N) - y_N), eps = 1 - band. MUTATE=M4 swaps the target kernel P2 -> simple; MUTATE=M5 widens the band to 20%."""
import math
import numpy as np, sympy as sp
from scipy.optimize import minimize_scalar
import CFG230_common as C
from CFG230_kernels import nu_p2, nu_simple, nu_mono, HMf

R = C.Run("CFG230_E_tail_bound")
M = C.mode()
band = 0.20 if M == "M5" else 0.10
target = "simple" if M == "M4" else "P2"
R.p(f"CFG230 E. repo=<repo> mode={M or 'main'} band=+-{band} target kernel={target}")

eps, y = sp.symbols("epsilon y", positive=True)
f = eps * sp.sqrt(y ** 2 + y) - y                      # P2: g_target/a0 = sqrt(y_N^2 + y_N)
ystar = sp.solve(sp.Eq(sp.diff(f, y), 0), y)
cl = [sp.simplify(f.subs(y, s_)) for s_ in ystar]
R.p("  P2: maximise f(y) = eps sqrt(y^2+y) - y (sympy); the two stationary points are compared numerically with the closed form at eps = 0.3, 0.5, 0.8, 0.9, 0.95 (the sympy expressions do not auto-simplify)")
closed = (1 - sp.sqrt(1 - eps ** 2)) / 2
ok = all(any(abs(float(c.subs(eps, e_)) - float(closed.subs(eps, e_))) < 1e-12 and float(ys.subs(eps, e_)) > 0 for c, ys in zip(cl, ystar)) for e_ in (0.3, 0.5, 0.8, 0.9, 0.95))
R.check("CROSS-CHECK", "closed form h(eps) = (1 - sqrt(1 - eps^2))/2 (CFG188)", ok)
tab = {b: float(closed.subs(eps, 1 - b)) for b in (0.10, 0.20, 0.50)}
R.p(f"  closed form at bands 10/20/50%: {tab}")
if M not in ("M4", "M5"):
    R.check("EXPECT", "E9 0.28206 / 0.2000 / 0.0670", abs(tab[0.10] - 0.28206) < 1e-4 and abs(tab[0.20] - 0.2) < 1e-4 and abs(tab[0.50] - 0.0670) < 1e-4, str(tab))

def gt(name, yy):
    yy = np.asarray(yy, float)
    if name == "P2": return np.sqrt(yy ** 2 + yy)
    return yy * (nu_simple(yy) if name == "simple" else nu_mono(yy))
def tail(name, b, lo=1e-6, hi=1e6):
    e = 1 - b
    ly = np.linspace(math.log(lo), math.log(hi), 6001)
    v = e * gt(name, np.exp(ly)) - np.exp(ly)
    i = int(np.argmax(v))
    return float(v[i]), float(np.exp(ly[i]))
res = {}
for nm in ("P2", "simple", "nu_mono"):
    res[nm] = {b: tail(nm, b) for b in (0.10, 0.20, 0.50)}
    res[nm]["G1range"] = tail(nm, 0.10, 1.1e-3, 100.0)
    R.p(f"  {nm}: forced tail band10 = {res[nm][0.10][0]:.5f} a0 at y_N = {res[nm][0.10][1]:.3f}; band20 {res[nm][0.20][0]:.4f}; band50 {res[nm][0.50][0]:.4f}; restricted to the G1 range y_N in [1.1e-3,100]: {res[nm]['G1range'][0]:.5f}")
R.res["tails"] = {k: {str(b): v for b, v in d.items()} for k, d in res.items()}
if M not in ("M4", "M5"):
    R.check("CROSS-CHECK", "P2 tail 0.28206 (CFG188 R2.c)", abs(res["P2"][0.10][0] - 0.28206) < 3e-3, f"{res['P2'][0.10][0]:.5f}")
    R.check("CROSS-CHECK", "simple-kernel tail 0.4675 (CFG188)", abs(res["simple"][0.10][0] - 0.4675) < 3e-3, f"{res['simple'][0.10][0]:.5f}")
    R.check("CROSS-CHECK", "nu_mono tail 0.424 (CFG188; nu_mono is my transcription)", abs(res["nu_mono"][0.10][0] - 0.424) < 0.01, f"{res['nu_mono'][0.10][0]:.5f}")

# (y q)' >= 0 for P2
yy = np.logspace(-4, 6, 2000)
ypq = 1 - 2 * yy / np.sqrt(1 + 4 * yy ** 2)
R.check("CROSS-CHECK", "(y q)' = 1 - 2y/sqrt(1+4y^2) > 0 for all y (P2 stable channel; CFG188 row 6)", bool(np.all(ypq > 0)), f"min {ypq.min():.3e} at y = 1e6 (-> 1/(8 y^2) = {1/(8*1e12):.2e})")

# Q2 at Saturn: constant radial anomaly A gives tide A/R (recipe A of CFG188: max(|dg/dR|, g/R), dg/dR = 0)
Q2bound = 5.2e-27
def q2_ratio(tail_a0, Rm): return tail_a0 * C.A0 / Rm / Q2bound
for nm_, Rm in (("Saturn 9.58 AU", 9.58 * C.AU), ("Saturn 9.54 AU", 9.54 * C.AU)):
    R.p(f"  {nm_}: Q2 ratio for the isolated P2 tail a0/2: {q2_ratio(0.5, Rm):.3e}; for the minimal tail {res[target][band][0]:.4f} a0: {q2_ratio(res[target][band][0], Rm):.3e}")
q_iso = q2_ratio(0.5, 9.58 * C.AU); q_min = q2_ratio(res[target][band][0], 9.58 * C.AU)
R.res.update(Q2_isolated=q_iso, Q2_minimal=q_min)
if M not in ("M4", "M5"):
    R.check("EXPECT", "E8 Q2 isolated tail 6.3e3 (+-5%), minimal tail 3.5e3-3.6e3 (+-5%)", abs(q_iso / 6.3e3 - 1) < 0.05 and abs(q_min / 3.55e3 - 1) < 0.05, f"{q_iso:.3e}, {q_min:.3e}")
    r188 = C.read_norm("campaign_fresh_gravity/CFG188_door11C_referee/README.md")
    R.check("CITATION-AUDIT", "CFG188 README prints 0.28206 / 0.46754 / 0.42405 and the 98.2% band", "0.28206" in r188 and "0.46754" in r188 and "98.2%" in r188)
# nu_mono non-decaying tail (CFG171 spin-off): (nu - 1) y_N = HM(y_N)
for yv, lab in ((1e6, "y_N = 1e6"), (C.G * C.MSUN / C.AU ** 2 / C.A0, "Earth (Sun at 1 AU)")):
    R.p(f"  nu_mono anomaly (nu-1) y_N at {lab} (y_N = {yv:.3e}): {float(HMf(yv)):.4f} a0")
if M not in ("M4", "M5"):
    R.check("CROSS-CHECK", "nu_mono tail >= 0.648 a0 and 1.18 a0 at Earth (CFG171 spin-off)", float(HMf(1e6)) >= 0.64 and abs(float(HMf(C.G * C.MSUN / C.AU ** 2 / C.A0)) / 1.18 - 1) < 0.05, "")

if M == "M4":
    a = res["P2"][0.10][0]; b = res["simple"][0.10][0]
    C.bite(R, abs(b / a - 1) > 0.10, f"R09 tail {a:.3f} -> {b:.3f} a0 ({(b/a-1)*100:+.0f}%), Q2 {q2_ratio(a, 9.58*C.AU):.2e} -> {q2_ratio(b, 9.58*C.AU):.2e}; R01 window, R02 dimensional statement and R08 dichotomy do not depend on the kernel")
if M == "M5":
    a = float(closed.subs(eps, 0.9)); b = res["P2"][0.20][0]
    C.bite(R, abs(b / a - 1) > 0.10, f"R09 tail {a:.3f} -> {b:.3f} a0 when the band widens to 20% (closed form 0.200); R05, R06 numbers unaffected")
R.write()
