#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG463 POST-HOC (written after the main and MUTATE runs; no verdict depends on it).

P1  REPRODUCTION: the main script's sections 1-5 are exec'd read-only and the L6-canonical S2 orbits are integrated again; every
    per-object median infall lookback must equal the main run's committed JSON value.
P2  INDEPENDENT INTEGRATOR: the 26 central orbits are re-integrated with scipy's DOP853 (rtol 1e-10) in the radial equation
    r'' = L^2/r^3 - g(r, tau), the crossings refined on the dense output; |t_inf(DOP853) - t_inf(leapfrog)| is reported.
P3  CONSISTENCY WITH CFG344's OWN SLOPE: the main run's power mocks (same seed, same sequence) are regenerated; reported is the
    fraction of mocks whose Z is at least the observed L6-canonical Z (how often CFG344's predicted slope, plus the observed
    scatter, would produce a lean as positive as the data's).  The power numbers must reproduce the main run's.
kappa = 1/2 FITTED.  No dark-matter particle; the cold fluid's MASS is still required.
Run: python3 campaign_fresh_gravity/CFG463_ufd_infall_order/cfg463_posthoc.py   (~1 min)
"""
import sys
sys.dont_write_bytecode = True
import os, io, math, json, contextlib, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C

R = C.Report("cfg463_posthoc", False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
os.environ.pop("CFG463_MUTATE", None)
MAIN = os.path.join(HERE, "cfg463_ufd_infall.py")
src = open(MAIN).read()
J = json.load(open(os.path.join(HERE, "cfg463_ufd_infall_results.json")))["numbers"]

ns = {"__file__": MAIN, "__name__": "cfg463_main_prefix"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ 6. C-ORB")], MAIN, "exec"), ns)
    i0 = src.index("def zof(rho, n):"); i1 = src.index("def sub(names, base):")
    exec(compile("\n" * src[:i0].count("\n") + src[i0:i1], MAIN, "exec"), ns)
    i0 = src.index("# CFG344's predicted shift"); i1 = src.index('P(f"\\n    CFG344 committed offsets')
    exec(compile("\n" * src[:i0].count("\n") + src[i0:i1], MAIN, "exec"), ns)
S2, S1, RF, VRF, VTF, Host, integrate = ns["S2"], ns["S1"], ns["RF"], ns["VRF"], ns["VTF"], ns["Host"], ns["integrate"]
MB6, KMS, TMAX, EXC, NMC = ns["MB6"], ns["KMS"], ns["TMAX"], ns["EXC"], ns["NMC"]
zof, rho_of, dx_pred, z_of_tl = ns["zof"], ns["rho_of"], ns["dx_pred"], ns["z_of_tl"]
TAUG, R200G = ns["TAUG"], ns["R200G"]
NO = len(S2)

# ------------------------------------------------------------------------------------------------ P1
R.banner("P1  REPRODUCTION of the main run's L6-canonical infall times")
host = Host("law", MB6, "canonical")
t1 = time.time()
ti, _ = integrate(RF.ravel(), VRF.ravel(), VTF.ravel(), host)
T = ti["R200"].reshape(NO, NMC + 1)
med = np.median(T, axis=1)
dev = max(abs(med[i] - J["per_object"][n]["t_inf"]["L6|canonical|R200"][0]) for i, n in enumerate(S2))
check("P1: the per-object median infall lookbacks (L6 canonical, S2) equal the main run's JSON", f"max |d| {dev:.1e} Gyr ({time.time() - t1:.0f} s)",
      dev <= 1e-12)

# ------------------------------------------------------------------------------------------------ P2
R.banner("P2  INDEPENDENT INTEGRATOR (DOP853, radial equation) on the 26 central orbits, L6 canonical")
Rb = lambda tau: float(np.interp(tau, TAUG, R200G))
out = []
for i, n in enumerate(S2):
    r0, vr0, vt0 = RF[i, 0], VRF[i, 0] * KMS, VTF[i, 0] * KMS
    L = r0 * vt0
    rhs = lambda tau, y: [y[1], L * L / y[0] ** 3 - float(host.g(np.array([y[0]]), tau)[0])]
    sol = solve_ivp(rhs, (0.0, TMAX), [r0, -vr0], method="DOP853", rtol=1e-10, atol=1e-10, dense_output=True, max_step=2.0)
    tg = np.arange(0.0, TMAX + 1e-9, 0.25)
    f = np.array([Rb(t) for t in tg]) - sol.sol(tg)[0]
    ex = np.where((f[:-1] >= 0) & (f[1:] < 0))[0]
    if f[-1] >= 0:
        tinf = TMAX
    elif len(ex):
        k = ex[-1]
        tinf = brentq(lambda t: Rb(t) - sol.sol(t)[0], tg[k], tg[k + 1], xtol=1e-6)
    else:
        tinf = 0.0
    out.append((n, tinf / 1e3, T[i, 0]))
d2 = np.array([abs(a - b) for _, a, b in out])
P("    " + "; ".join(f"{n} {a:.3f}/{b:.3f}" for n, a, b in out))
check("P2 (reported): DOP853 vs leapfrog central t_inf (Gyr), L6 canonical", f"max |d| {d2.max():.4f} Gyr; median {np.median(d2):.1e}; "
      f"{int(np.sum(d2 > 0.01))} of {NO} differ by > 0.01 Gyr", True, load_bearing=False)
R.num("P2", {n: [a, b] for n, a, b in out})

# ------------------------------------------------------------------------------------------------ P3
R.banner("P3  CONSISTENCY OF THE OBSERVED LEAN WITH CFG344's OWN PREDICTED SLOPE (L6 canonical, S1)")
idx = [S2.index(n) for n in S1]
x = np.array([EXC[n]["x"]["canonical"] for n in S1]); t = med[idx]; TT = T[idx]; n_ = len(S1)
Zobs = zof(rho_of(x, t), n_)
res = {}
for prof in ("nfw", "sis"):
    pw = np.random.default_rng(4633); Zs = []
    for _ in range(2000):
        kk = pw.integers(1, NMC + 1, n_)
        ttrue = TT[np.arange(n_), kk]
        xm = x[pw.permutation(n_)] + dx_pred(z_of_tl(ttrue), prof)
        Zs.append(zof(rho_of(xm, t), n_))
    Zs = np.array(Zs)
    res[prof] = dict(power=float(np.mean(Zs <= -2)), p_ge_obs=float(np.mean(Zs >= Zobs)), Z_med=float(np.median(Zs)),
                     Z_16_84=[float(np.percentile(Zs, 16)), float(np.percentile(Zs, 84))])
    P(f"    {prof.upper()}: power {res[prof]['power']:.3f} (main {J['power'][prof]['power']:.3f}); mock Z median {res[prof]['Z_med']:+.2f} "
      f"[16-84 {res[prof]['Z_16_84'][0]:+.2f}, {res[prof]['Z_16_84'][1]:+.2f}]; observed Z {Zobs:+.2f}; P(Z_mock >= Z_obs) = {res[prof]['p_ge_obs']:.4f}")
pdev = max(abs(res[p]["power"] - J["power"][p]["power"]) for p in res)
check("P3: the power mocks reproduce the main run's power exactly", f"max |d| {pdev:.1e}", pdev == 0.0)
R.num("P3", dict(Z_obs=Zobs, **res))

# ------------------------------------------------------------------------------------------------ P4 (added after reading P3)
R.banner("P4  P3 AT FIXED LUMINOSITY (added after P3: P3's mocks drop CFG344's own luminosity term, see the README)")
P("    Under CFG344 the excess also rises for fainter fossils (one M_c for all, so cold mass dominates more), and the faintest systems")
P("    are found nearby and fell in early: that alone makes rho(x, t) positive.  P4 removes it: statistic = partial Spearman of (x, t)")
P("    given M_V; mocks x = a + b M_V + permuted residual + Delta_x(t_true) (OLS a, b from the data; 2000, seed 4637).")
MV = np.array([EXC[n]["MV"] for n in S1])


def partial(xx, tt, cc):
    rxt, rxc, rtc = rho_of(xx, tt), rho_of(xx, cc), rho_of(tt, cc)
    p_ = (rxt - rxc * rtc) / math.sqrt((1 - rxc ** 2) * (1 - rtc ** 2))
    return p_, math.atanh(max(min(p_, 0.999999), -0.999999)) * math.sqrt((n_ - 4) / 1.06)


pobs, zpobs = partial(x, t, MV)
b_, a_ = np.polyfit(MV, x, 1); e_ = x - (a_ + b_ * MV)
res4 = {}
for prof in ("nfw", "sis"):
    pw = np.random.default_rng(4637); Zp = []
    for _ in range(2000):
        kk = pw.integers(1, NMC + 1, n_)
        ttrue = TT[np.arange(n_), kk]
        xm = a_ + b_ * MV + e_[pw.permutation(n_)] + dx_pred(z_of_tl(ttrue), prof)
        Zp.append(partial(xm, t, MV)[1])
    Zp = np.array(Zp)
    res4[prof] = dict(power=float(np.mean(Zp <= -2)), p_ge_obs=float(np.mean(Zp >= zpobs)), Z_med=float(np.median(Zp)),
                      Z_16_84=[float(np.percentile(Zp, 16)), float(np.percentile(Zp, 84))])
    P(f"    {prof.upper()}: partial-Z power {res4[prof]['power']:.3f}; mock partial Z median {res4[prof]['Z_med']:+.2f} [16-84 "
      f"{res4[prof]['Z_16_84'][0]:+.2f}, {res4[prof]['Z_16_84'][1]:+.2f}]; observed partial rho {pobs:+.3f} (Z {zpobs:+.2f}); "
      f"P(Z_mock >= Z_obs) = {res4[prof]['p_ge_obs']:.4f}")
P(f"    OLS x = {a_:+.3f} {b_:+.4f} M_V (dex per mag)")
R.num("P4", dict(partial_obs=pobs, Z_obs=zpobs, a=float(a_), b=float(b_), **res4))
P("\n  kappa = 1/2 FITTED.  No dark-matter particle; the cold fluid's MASS is still required.  POST-HOC: no verdict depends on this file.")
nf = R.write(HERE)
sys.exit(1 if nf else 0)
