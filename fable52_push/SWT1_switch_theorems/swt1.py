#!/usr/bin/env python3
"""SWT1 switch theorems (criteria 4d86f4d107, amendment A1 4af87eb9c0). TEST lane, quarantined; adopts nothing.
kappa = 1/2 FITTED; not theory closed. One thread. Usage: python3 swt1.py [--mutate]

T2: the compensated large-scale statistic of a variational switch on WL1's own inputs (WL1's shell solver and
    population sum are transcribed from closure_2026_11_07/WL1_web_law_switch/wl1.py, read-only).
T3: the wall pressure in closed form and the self-clearing gate.
"""
import os, sys, json, math, time
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
if not hasattr(np, 'trapz'): np.trapz = np.trapezoid

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "swt1_MUTATE" if MUT else "swt1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()

# ------------------------------------------------------------------ constants (SI) and footings
G, MS, PC, CL = 6.6743e-11, 1.98847e30, 3.0856775814913673e16, 2.99792458e8
MPC, KPC = 1e6 * PC, 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LINE = 0.0354                                   # WL1's stage-2 line (lensing amplitude)

# ------------------------------------------------------------------ the law
def u_in(y):
    """the law's field (units a0) for displacement y: mu(u) u = y, mu = u / (1 + u)."""
    y = np.asarray(y, float); return 0.5 * y + np.sqrt(0.25 * y * y + y)
def glaw(g, a0): return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))
def Wfun(u):
    u = np.asarray(u, float); return u - np.log1p(u) - u * u / (2.0 * (1.0 + u) ** 2)
def p_wall(y, a0):
    """force per unit area on the switch carrier across a wall where S falls 1 -> 0, at displacement y (SI, Pa)."""
    return a0 * a0 / (4 * math.pi * G) * Wfun(u_in(y))

# ------------------------------------------------------------------ WL1's background, shell solver, GSMF (transcribed)
OB, OD, H0 = 0.0215, 0.11958060485606123, 65.0
R_DUST = OD / OB; OR_h2 = 4.15e-5; h = H0 / 100
Om, Orr = (OB + OD) / h ** 2, OR_h2 / h ** 2; OL = 1 - Om - Orr
H0s = H0 * 1e3 / MPC
RHOC = 3 * H0s ** 2 / (8 * math.pi * G)
RHO_M0 = Om * RHOC
RHO_D0 = OD / h ** 2 * RHOC                     # mean component density today (kg / m^3)
def Hs(a): return H0s * math.sqrt(Orr / a ** 4 + Om / a ** 3 + OL)
ZI = 1000.0; AI = 1 / (1 + ZI)

def shell(xL, dM, a0, a_end=1.0):
    def rhs(t, s):
        a, r, v = s
        acc = -(4 * math.pi * G / 3) * (RHO_M0 / a ** 3 + 2 * Orr * RHOC / a ** 4 - 2 * OL * RHOC) * r
        gN = G * dM / r ** 2
        acc -= (float(glaw(gN, a0)) if a0 > 0 else gN)
        return [a * Hs(a), v, acc]
    def turn(t, s): return s[2]
    turn.terminal, turn.direction = True, -1
    def end(t, s): return s[0] - a_end
    end.terminal = True
    r0 = xL * AI; s0 = [AI, r0, Hs(AI) * r0]
    so = solve_ivp(rhs, (0, 3e18), s0, events=(turn, end), rtol=1e-9, atol=[1e-12, r0 * 1e-12, 1e-6], method="DOP853")
    if so.t_events[0].size: return "early", so.y_events[0][0]
    return "late", so.y_events[1][0] if so.t_events[1].size else so.y[:, -1]

_RTA = {}
def r_ta(dM, a0, a_end=1.0):
    key = (round(math.log10(dM), 9), a0, a_end)
    if key in _RTA: return _RTA[key]
    lo, hi = math.log(1e-6 * MPC), math.log(1e3 * MPC)
    for _ in range(60):
        mid = 0.5 * (lo + hi); kind, st = shell(math.exp(mid), dM, a0, a_end)
        if kind == "early": lo = mid
        else: hi = mid
        if hi - lo < 1e-7: break
    kind, st = shell(math.exp(hi), dM, a0, a_end)
    _RTA[key] = float(st[1]); return _RTA[key]
def r_qx10(Mb): return (Mb * (1 + R_DUST) / (4 * math.pi / 3 * 5.55 * RHO_M0)) ** (1 / 3)
def Rms(which, Mb, a0, aE=1.0):
    if which == "L": return r_ta(Mb, a0, aE)                                              # WL1's graded stage-2 reading
    if which == "C": return max(r_ta(Mb * (1 + R_DUST), a0, aE), r_qx10(Mb) * aE)         # ceiling
    if which == "NC": return max(r_ta(Mb * (1 + R_DUST), 0.0, aE), r_qx10(Mb) * aE)       # self-consistent, as WL1 reports it
    if which == "NL": return r_ta(Mb, 0.0, aE)
    raise ValueError(which)

def Mph(r, Mb, a0):
    if r <= 0: return 0.0
    y = G * Mb / r ** 2 / a0
    return Mb * (math.sqrt(0.25 + 1.0 / y) - 0.5)
def dMph(r, Mb, a0):
    y = G * Mb / r ** 2 / a0
    return Mb / (y * r * np.sqrt(0.25 + 1.0 / y))

DRV = json.load(open(os.path.join(REPO, "closure_program_2026_10_27", "population", "inputs.json")))["driver2022"]
h70 = h / 0.7
MSTAR = 10 ** DRV["log10_Mstar_h70_minus2"] / h70 ** 2
PHI = np.array([10 ** DRV[k] for k in ("log10_phi1_h70_cubed", "log10_phi2_h70_cubed")]) * 10 ** DRV["add_log10_phi_for_SDSS_and_z0"] * h70 ** 3
ALP = np.array([DRV["alpha1"], DRV["alpha2"]])
def per_dex(lm):
    x = 10 ** lm / MSTAR; return float(math.log(10) * np.sum(PHI * x ** (ALP + 1)) * math.exp(-x))
RHO_D_SUN = OD * 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G) * MPC ** 3 / MS               # comoving Msun / Mpc^3
LG = np.arange(9.0, 12.001, 0.25); LF = np.arange(9.0, 12.0001, 0.02)
PD = np.array([per_dex(m) for m in LF])

def radii_table(which, a0, z):
    aE = 1 / (1 + z)
    return np.array([Rms(which, 10 ** m * MS, a0, aE) for m in LG])
def fine(tab): return 10 ** np.interp(LF, LG, np.log10(np.maximum(tab, 1e-30)))
def q_pop_uncomp(tab, a0):
    """WL1's statistic: the retained phantom counted as mass."""
    Rm = fine(tab)
    mph = np.array([Mph(R, 10 ** m * MS, a0) / MS if R > 0 else 0.0 for R, m in zip(Rm, LF)])
    return float(np.trapz(PD * mph, LF)) / RHO_D_SUN

# ------------------------------------------------------------------ T2: polarizability of a law bubble
def alpha_generic(mur, mut, dlnmur, s0, s1, L0=1.0):
    """l = 1 response of a radially graded, radially anisotropic inclusion. s = ln r; L = d ln f / d ln r."""
    def rhs(s, L): return [-L[0] ** 2 - (1.0 + dlnmur(s)) * L[0] + 2.0 * mut(s) / mur(s)]
    so = solve_ivp(rhs, (s0, s1), [L0], rtol=1e-10, atol=1e-12, method="LSODA")
    Lam = mur(s1) * so.y[0, -1]
    return (Lam - 1.0) / (Lam + 2.0), Lam
def alpha_law(Mb, R, a0):
    def yy(s): return G * Mb / (math.exp(2 * s) * a0)
    def uu(s):
        y = yy(s); return 0.5 * y + math.sqrt(0.25 * y * y + y)
    def mur(s):
        u = uu(s); return u * (2 + u) / (1 + u) ** 2
    def mut(s):
        u = uu(s); return u / (1 + u)
    def dlnmur(s):
        y = yy(s); u = uu(s)
        dudy = 0.5 + (0.5 * y + 1.0) / (2.0 * math.sqrt(0.25 * y * y + y))
        return (2.0 / (1 + u) ** 3) * dudy * (-2.0 * y) / mur(s)
    r0 = math.sqrt(G * Mb / (1e8 * a0))                      # y = 1e8: Newtonian centre, mu = 1, f proportional to r
    if R <= r0: return 0.0, 1.0
    return alpha_generic(mur, mut, dlnmur, math.log(r0), math.log(R))

def uform(k_phys, R, Mb, a0, n=4000):
    """transform of the retained phantom minus its surface layer, normalised by the retained phantom."""
    r = np.logspace(math.log10(R) - 5, math.log10(R), n)
    dm = dMph(r, Mb, a0); x = k_phys * r
    sinc = np.where(x < 1e-4, 1 - x * x / 6, np.sin(x) / np.where(x == 0, 1, x))
    M = Mph(R, Mb, a0)
    core = Mph(r[0], Mb, a0)
    val = core + np.trapz(dm * sinc, r); xr = k_phys * R
    return (val - M * (math.sin(xr) / xr if xr > 1e-4 else 1 - xr * xr / 6)) / M

def compensated(tab, a0, z, kcom=0.1 / MPC, insulating=False):
    """filling, Maxwell-Garnett statistic and form-factor term for a radii table (physical radii at z)."""
    Vt = 4 * math.pi / 3 * (tab / MPC) ** 3 * (1 + z) ** 3                                # proper Mpc^3 per comoving Mpc^-3
    al = np.array([(-0.5 if insulating else alpha_law(10 ** m * MS, R, a0)[0]) for m, R in zip(LG, tab)])
    Vf = np.interp(LF, LG, np.log10(np.maximum(Vt, 1e-300))); Vf = 10 ** Vf
    af = np.interp(LF, LG, al)
    fV = float(np.trapz(PD * Vf, LF)); beta = float(np.trapz(PD * Vf * af, LF))
    dilute = fV <= 0.30
    b = beta if dilute else beta * 0.30 / fV
    qC = -3 * b / (1 + 2 * b)
    Rm = fine(tab)
    uf = np.array([uform(kcom * (1 + z), R, 10 ** m * MS, a0) for m, R in zip(LG, tab)])
    uff = np.interp(LF, LG, uf)
    mph = np.array([Mph(R, 10 ** m * MS, a0) / MS for R, m in zip(Rm, LF)])
    qff = float(np.trapz(PD * mph * uff, LF)) / RHO_D_SUN
    return dict(f_V=fV, beta=beta, dilute=bool(dilute), q_C=float(qC), q_C_is_lower_bound=bool(not dilute), q_ff=qff,
                q_tot=float(qC + abs(qff)), alpha_at_9_10p5_12=[float(al[0]), float(np.interp(10.5, LG, al)), float(al[-1])],
                R_Mpc_at_9_10p5_12=[float(tab[0] / MPC), float(np.interp(10.5, LG, tab) / MPC), float(tab[-1] / MPC)])

RES = dict(lane="SWT1", criteria="4d86f4d107", amendment_A1="4af87eb9c0", tag=TAG,
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, T2={}, T3={}, reported={}, MUTATE={})
P(f"SWT1 {'MUTATE ' if MUT else ''}run. Background OB {OB} OD {OD:.5f} H0 {H0}; R = OD/OB = {R_DUST:.4f}; rho_d0 {RHO_D0:.3e} kg/m^3 "
  f"= {RHO_D_SUN:.3e} Msun/Mpc^3; line {LINE}")

# =================================================================== known answers
# KA-W1: closed form vs quadrature of integral_0^y (nu(t) - 1) t dt
kaw1 = []
for y in (1e-6, 1e-3, 0.1, 1.0, 10.0, 1e4):
    val, err = quad(lambda t: math.sqrt(0.25 * t * t + t) - 0.5 * t, 0.0, y, epsabs=0, epsrel=1e-13, limit=400)
    cf = float(Wfun(u_in(y))); kaw1.append(dict(y=y, closed=cf, quad=val, rel=abs(cf / val - 1)))
ok1 = all(r["rel"] < 1e-8 for r in kaw1)
RES["KA"]["KA_W1"] = dict(rows=kaw1, pass_=bool(ok1))
P("KA-W1 closed form vs quadrature: max rel " + f"{max(r['rel'] for r in kaw1):.2e} -> {'PASS' if ok1 else 'FAIL'}")
# KA-W2: limits
d2 = float(Wfun(u_in(1e-6)) / ((2 / 3) * 1e-6 ** 1.5)); n2 = float(Wfun(u_in(1e4)) / 1e4)
ok2 = abs(d2 - 1) < 2e-3 and abs(n2 - 1) < 2e-3
RES["KA"]["KA_W2"] = dict(deep_ratio=d2, newton_ratio=n2, pass_=bool(ok2))
P(f"KA-W2 limits: W / ((2/3) y^1.5) at 1e-6 = {d2:.6f}; W / y at 1e4 = {n2:.6f} -> {'PASS' if ok2 else 'FAIL'}")
# bounds checked on a grid (Lean carries the proof)
yg = np.logspace(-8, 8, 4001); Wg = Wfun(u_in(yg))
RES["KA"]["bounds_grid"] = dict(min_W=float(Wg.min()), max_W_over_y=float((Wg / yg).max()), max_W_over_deep=float((Wg / ((2 / 3) * yg ** 1.5)).max()))
P(f"bounds on a grid of 4001 y in [1e-8, 1e8]: min W {Wg.min():.3e} (>= 0), max W/y {(Wg/yg).max():.6f} (<= 1), "
  f"max W / ((2/3) y^1.5) {(Wg/((2/3)*yg**1.5)).max():.6f} (<= 1)")

# KA-W3: the full Lagrangian of a Plummer sphere, differenced in the switch radius
def ka_w3(a0, sign=+1.0):
    Mp, b = 1e11 * MS, 3.0 * KPC
    def Mb_in(r): return Mp * r ** 3 / (r * r + b * b) ** 1.5
    def gN(r): return G * Mb_in(r) / r ** 2
    def J(g):
        u = g / a0; return a0 * a0 / (4 * math.pi * G) * (u - math.log1p(u))
    def g_on(r):
        y = gN(r) / a0
        if sign > 0: return a0 * float(u_in(y))                       # the law: (1 - 1/(1+u)) u = y
        return a0 * (-(2 - y) + math.sqrt((2 - y) ** 2 + 4 * y)) / 2  # sign-flipped Lagrangian: (1 + 1/(1+u)) u = y
    def f_in(r):
        g = g_on(r); return 4 * math.pi * r * r * (-g * g / (8 * math.pi * G) + sign * J(g)) + Mb_in(r) * g
    def f_out(r):
        g = gN(r); return 4 * math.pi * r * r * (-g * g / (8 * math.pi * G)) + Mb_in(r) * g
    rows = []
    for Rk in (5.0, 20.0, 100.0, 500.0):
        R = Rk * KPC; d = 1e-4 * R
        num = quad(lambda r: f_in(r) - f_out(r), R - d, R + d, epsabs=0, epsrel=1e-13)[0] / (2 * d)
        cf = 4 * math.pi * R * R * float(p_wall(gN(R) / a0, a0))
        rows.append(dict(R_kpc=Rk, dL_dR=num, closed=cf, rel=abs(num / cf - 1), outward=bool(num > 0)))
    return rows
kw3 = ka_w3(A0["canonical"])
ok3 = all(r["rel"] < 1e-5 and r["outward"] for r in kw3)
RES["KA"]["KA_W3"] = dict(rows=kw3, pass_=bool(ok3))
P("KA-W3 Plummer sphere, d L_total / d R against 4 pi R^2 p_wall: max rel " + f"{max(r['rel'] for r in kw3):.2e}, outward "
  f"{all(r['outward'] for r in kw3)} -> {'PASS' if ok3 else 'FAIL'}")

# KA-CP2: uniform inclusion
kc2 = []
for mu in (0.1, 0.5, 2.0):
    al, Lam = alpha_generic(lambda s: mu, lambda s: mu, lambda s: 0.0, -10.0, 0.0)
    kc2.append(dict(mu=mu, alpha=al, exact=(mu - 1) / (mu + 2), err=abs(al - (mu - 1) / (mu + 2))))
okc2 = all(r["err"] < 1e-6 for r in kc2)
RES["KA"]["KA_CP2"] = dict(rows=kc2, pass_=bool(okc2))
P("KA-CP2 uniform inclusion, alpha against (mu - 1)/(mu + 2): max err " + f"{max(r['err'] for r in kc2):.2e} -> {'PASS' if okc2 else 'FAIL'}")
# KA-CP3: smooth spherical switch, exterior effective mass
def ka_cp3(a0):
    Mb, R = 1e10 * MS, 300 * KPC; w = 0.02 * R; worst = 0.0
    for r in np.linspace(1.2 * R, 3 * R, 40):
        S = 0.5 * (1 - math.tanh((r - R) / w)); y = G * Mb / r ** 2 / a0
        u = brentq(lambda u: (1 - S / (1 + u)) * u - y, 0.0, y + 2.0, xtol=1e-300, rtol=1e-15)
        worst = max(worst, abs(u / y - 1))
    S_in = 0.5 * (1 - math.tanh((0.5 * R - R) / w)); y = G * Mb / (0.5 * R) ** 2 / a0
    u = brentq(lambda u: (1 - S_in / (1 + u)) * u - y, 0.0, 10 * (y + math.sqrt(y)) + 2.0, rtol=1e-15)
    return worst, u / y, float(u_in(y) / y)
w3, in_num, in_law = ka_cp3(A0["canonical"])
okc3 = w3 < 1e-6
RES["KA"]["KA_CP3"] = dict(max_exterior_excess=w3, interior_Meff_over_Mb=in_num, law_nu=in_law, pass_=bool(okc3))
P(f"KA-CP3 smooth switch: |M_eff/M_b - 1| beyond 1.2 R <= {w3:.2e}; at 0.5 R M_eff/M_b {in_num:.4f} (law nu {in_law:.4f}) -> {'PASS' if okc3 else 'FAIL'}")

# =================================================================== T2
READ = ("L", "C", "NC", "NL"); ZS = (1.0, 0.5, 2.0, 0.0)
P("")
P("T2. Radii tables (WL1's shell solver) ...")
TAB = {}
for f, a0 in A0.items():
    for wch in READ:
        for z in ZS:
            TAB[(f, wch, z)] = radii_table(wch, a0 if wch in ("L", "C") else a0, z)
P(f"   tables done ({time.time() - T0:.0f} s)")

# KA-CP1: WL1's own statistic
REF = {"canonical": {"L": 0.936, "NC": 0.384}, "alt": {"L": 1.079, "NC": 0.423}}
kc1 = {}; okc1 = True
for f, a0 in A0.items():
    kc1[f] = {}
    for wch in ("L", "NC"):
        q = q_pop_uncomp(TAB[(f, wch, 1.0)], a0); rel = abs(q / REF[f][wch] - 1)
        kc1[f][wch] = dict(q_pop=q, wl1=REF[f][wch], rel=rel); okc1 &= rel < 0.01
        P(f"KA-CP1 [{f}] reading {wch}, z 1: uncompensated q_pop {q:.4f} (WL1 {REF[f][wch]}), rel {rel:.2e}")
RES["KA"]["KA_CP1"] = dict(rows=kc1, pass_=bool(okc1))
P(f"KA-CP1 -> {'PASS' if okc1 else 'FAIL'}")

T2 = {}
for f, a0 in A0.items():
    T2[f] = {}
    for wch in READ:
        T2[f][wch] = {}
        for z in ZS:
            tab = TAB[(f, wch, z)]
            if MUT:
                q = q_pop_uncomp(tab, a0)
                d = dict(q_uncompensated=q, pass_=bool(q <= LINE))
                P(f"[{f}] MUTATE M-CP reading {wch} z {z}: phantom counted as exterior mass, q {q:.3f} (line {LINE}) -> {'PASS' if q <= LINE else 'FAIL'}")
            else:
                d = compensated(tab, a0, z); d["insulating_bracket"] = compensated(tab, a0, z, insulating=True)["q_C"]
                d["q_uncompensated_WL1"] = q_pop_uncomp(tab, a0); d["pass_"] = bool(d["q_tot"] <= LINE); d["graded"] = bool(z == 1.0)
                P(f"[{f}] reading {wch} z {z}: R(1e9 / 1e10.5 / 1e12) {d['R_Mpc_at_9_10p5_12'][0]:.3f} / {d['R_Mpc_at_9_10p5_12'][1]:.3f} / "
                  f"{d['R_Mpc_at_9_10p5_12'][2]:.3f} Mpc; filling {d['f_V']:.4f}{'' if d['dilute'] else ' NOT DILUTE'}; alpha "
                  f"{d['alpha_at_9_10p5_12'][1]:.3f}; q_C {'>= ' if not d['dilute'] else ''}{d['q_C']:.4f} (insulating {d['insulating_bracket']:.4f}); "
                  f"q_ff {d['q_ff']:+.2e}; total {d['q_tot']:.4f} vs {LINE} -> {'PASS' if d['pass_'] else 'FAIL'}"
                  f"{' [GRADED EPOCH]' if z == 1.0 else ''}; WL1's own statistic {d['q_uncompensated_WL1']:.3f}")
            T2[f][wch][str(z)] = d
RES["T2"] = T2

if not MUT:
    # reported: filling needed for the law to stay on out to fixed radii / to KiDS's lowest tabulated acceleration, lenses >= 10^9.4
    rep = {}
    sel = LF >= 9.4
    ntot = float(np.trapz(PD[sel], LF[sel]))
    for Rfix in (0.43, 1.0, 2.8):
        nV = ntot * 4 * math.pi / 3 * Rfix ** 3
        rep[f"R_{Rfix}_Mpc"] = dict(n_per_Mpc3=ntot, sum_nV=nV, poisson_union=1 - math.exp(-nV), q_C_insulating_if_dilute=(1.5 * nV / (1 - nV) if nV <= 0.30 else None))
        P(f"reported: law on to {Rfix} Mpc for every lens with log M* >= 9.4 (n {ntot:.4f} / Mpc^3): sum nV {nV:.3f}, Poisson union "
          f"{1 - math.exp(-nV):.3f}; needs <= {LINE / (1.5 + LINE):.4f}")
    GK = 1.38e-15
    RK = np.sqrt(G * 10 ** LF * MS / GK) / MPC
    nVK = float(np.trapz(PD[sel] * 4 * math.pi / 3 * RK[sel] ** 3, LF[sel]))
    rep["KiDS_lowest_gbar"] = dict(gbar=GK, R_K_Mpc_at_9p4_10p9=[float(np.interp(9.4, LF, RK)), float(np.interp(10.9, LF, RK))], sum_nV=nVK,
                                   poisson_union=1 - math.exp(-nVK))
    P(f"reported: law on down to g_bar {GK:.2e} (R_K {np.interp(9.4, LF, RK):.2f} to {np.interp(10.9, LF, RK):.2f} Mpc at log M 9.4 to 10.9): "
      f"sum nV {nVK:.3f}, Poisson union {1 - math.exp(-nVK):.3f}")
    fmax = LINE / (1.5 + LINE)
    rep["filling_allowed_insulating"] = fmax
    # largest common fraction x of R_K that meets the filling bound (insulating)
    xK = (fmax / nVK) ** (1 / 3)
    rep["fraction_of_R_K_allowed"] = xK; rep["gbar_floor_allowed"] = GK / xK ** 2
    P(f"reported: the bound f_V <= {fmax:.4f} lets the law reach {xK:.3f} of R_K for every lens, i.e. down to g_bar {GK / xK ** 2:.2e} m/s^2")
    RES["reported"]["kids_reach"] = rep

    # reported: bubbles held by pressure balance against mean-density component
    pb = {}
    for f, a0 in A0.items():
        pb[f] = {}
        for z in (0.0, 1.0):
            rho = RHO_D0 * (1 + z) ** 3
            for sig in (17.5, 35.0, 52.5):
                pamb = rho * (sig * 1e3) ** 2
                def Rbal(Mb): return brentq(lambda lr: math.log(float(p_wall(G * Mb / math.exp(2 * lr) / a0, a0)) / pamb), math.log(1e-3 * KPC), math.log(1e4 * MPC))
                tab = np.array([math.exp(Rbal(10 ** m * MS)) for m in LG])
                d = compensated(tab, a0, z)
                reach = {str(lm): float(np.interp(lm, LG, tab) / math.sqrt(G * 10 ** lm * MS / GK)) for lm in (9.4, 10.45, 10.7, 10.9)}
                pb[f][f"z{z}_sig{sig}"] = dict(R_Mpc_at_9_10p5_12=d["R_Mpc_at_9_10p5_12"], f_V=d["f_V"], dilute=d["dilute"], q_C=d["q_C"], q_tot=d["q_tot"],
                                               pass_line=bool(d["q_tot"] <= LINE), reach_over_R_K=reach)
                P(f"reported [{f}] pressure-balance bubbles, z {z}, dispersion {sig} km/s: R(1e10.5) {d['R_Mpc_at_9_10p5_12'][1]:.2f} Mpc, "
                  f"filling {d['f_V']:.3f}{'' if d['dilute'] else ' NOT DILUTE'}, q_C {'>= ' if not d['dilute'] else ''}{d['q_C']:.3f} "
                  f"({'PASS' if d['q_tot'] <= LINE else 'FAIL'} the line), reach / R_K {min(reach.values()):.2f}-{max(reach.values()):.2f}")
    RES["reported"]["pressure_balance_bubbles"] = pb

# =================================================================== T3 gate
P("")
P("T3. Self-clearing gate (A1: local isothermal carrier pressure).")
def gate(lm, a0, share=1.0, pscale=1.0):
    Mb = 10 ** lm * MS; Rh = Rms("NC", Mb, 0.0, 1.0); rM = math.sqrt(G * Mb / a0)
    r = np.logspace(math.log10(1e-2 * KPC), math.log10(Rh), 6001)
    Md = share * R_DUST * Mb * r / Rh
    pd = pscale * G * share * R_DUST * Mb ** 2 * (1 + share * R_DUST * r / Rh) / (8 * math.pi * Rh * r ** 3)
    pw = p_wall(G * Mb / r ** 2 / a0, a0); ratio = pw / pd
    rmax = min(200 * KPC, Rh); inside = r <= rmax
    dM = np.diff(np.concatenate([[0.0], Md]))
    unc = float(np.sum(dM[inside & (ratio < 1)])) / Mb
    tot = float(np.sum(dM[inside])) / Mb
    cl = r[ratio >= 1]
    return dict(logMb=lm, R_h_Mpc=Rh / MPC, r_M_kpc=rM / KPC, M_unc_over_Mb=unc, carrier_inside_over_Mb=tot,
                cleared_from_kpc=(float(cl.min() / KPC) if cl.size else None), cleared_to_kpc=(float(cl.max() / KPC) if cl.size else None),
                min_ratio=float(ratio.min()), ratio_at_30_100_Rh=[float(np.interp(x, r, ratio)) for x in (30 * KPC, 100 * KPC, Rh)],
                ram_bracket_ratio_at_100kpc=float(np.interp(100 * KPC, r, ratio)) / 4.0, clears=bool(unc <= 0.9))
BINS = (9.4, 10.45, 10.7, 10.9)
T3 = {}
PSC = 100.0 if MUT else 1.0
for f, a0 in A0.items():
    T3[f] = {}
    for lm in BINS:
        d = gate(lm, a0, pscale=PSC)
        if not MUT:
            # share multiple at which the uncleared mass meets the line
            fs = np.logspace(0, 4, 161); un = np.array([gate(lm, a0, share=x)["M_unc_over_Mb"] for x in fs])
            d["share_multiple_at_line"] = (float(fs[np.argmax(un > 0.9)]) if np.any(un > 0.9) else None)
        T3[f][str(lm)] = d
        P(f"[{f}] log M_b {lm}{' (carrier pressure x100, MUTATE)' if MUT else ''}: R_h {d['R_h_Mpc']:.3f} Mpc, r_M {d['r_M_kpc']:.2f} kpc; "
          f"p_wall / p_d at 30 kpc, 100 kpc, R_h: " + " / ".join(f"{x:.2f}" for x in d["ratio_at_30_100_Rh"]) + f"; min {d['min_ratio']:.2f}; "
          f"cleared {d['cleared_from_kpc']} to {d['cleared_to_kpc']} kpc; uncleared inside 200 kpc {d['M_unc_over_Mb']:.3f} M_b "
          f"of {d['carrier_inside_over_Mb']:.2f} (line 0.9) -> {'CLEARS' if d['clears'] else 'DOES NOT CLEAR'}"
          + (f"; clearing fails only above {d['share_multiple_at_line']:.1f} x the share" if (not MUT and d.get('share_multiple_at_line')) else ""))
RES["T3"]["gate"] = T3

if not MUT:
    # carrier B: Tully-Fisher-normalised singular isothermal halo
    cb = {}
    for f, a0 in A0.items():
        cb[f] = {}
        for lm in BINS:
            Mb = 10 ** lm * MS; vh2 = math.sqrt(G * Mb * a0); rM = math.sqrt(G * Mb / a0)
            r = np.logspace(math.log10(1e-3 * rM), math.log10(3 * MPC), 8001)
            pd = vh2 / (4 * math.pi * G * r * r) * (G * Mb / r + vh2) / 2
            ratio = p_wall(G * Mb / r ** 2 / a0, a0) / pd; cl = r[ratio >= 1]
            cb[f][str(lm)] = dict(r_M_kpc=rM / KPC, cleared_from_rM=(float(cl.min() / rM) if cl.size else None),
                                  cleared_to_rM=(float(cl.max() / rM) if cl.size else None), max_ratio=float(ratio.max()),
                                  ratio_at_3_10_30_rM=[float(np.interp(x * rM, r, ratio)) for x in (3, 10, 30)])
        d = cb[f]["10.9"]
        P(f"reported [{f}] carrier B (v_h^4 = G M_b a0): cleared set {d['cleared_from_rM']} to {d['cleared_to_rM']} r_M (max ratio {d['max_ratio']:.3f}); "
          f"ratio at 3 / 10 / 30 r_M " + " / ".join(f"{x:.3f}" for x in d["ratio_at_3_10_30_rM"]) + " (same for every mass by scaling)")
    RES["T3"]["carrier_B"] = cb
    # groups and clusters: baryons enclosed in proportion to r, share in the same isothermal sphere
    gc = {}
    for f, a0 in A0.items():
        gc[f] = {}
        for name, Mb, Rh in (("group", 3e12 * MS, 0.45 * MPC), ("cluster", 1.4e14 * MS, 1.4 * MPC)):
            rows = []
            for x in (0.1, 0.3, 1.0):
                r = x * Rh; y = G * (Mb * x) / r ** 2 / a0
                pd = (R_DUST * Mb / (4 * math.pi * Rh * r * r)) * G * Mb * (1 + R_DUST) / (2 * Rh)
                rows.append(dict(x=x, y=y, ratio=float(p_wall(y, a0)) / pd))
            gc[f][name] = rows
            P(f"reported [{f}] {name}: p_wall / p_d at 0.1 / 0.3 / 1 R_h = " + " / ".join(f"{r_['ratio']:.3f}" for r_ in rows)
              + " (y " + " / ".join(f"{r_['y']:.3f}" for r_ in rows) + ")")
    RES["T3"]["groups_clusters"] = gc

# =================================================================== MUTATE extras and labels
if MUT:
    mw = ka_w3(A0["canonical"], sign=-1.0)
    bite_w = all(r["dL_dR"] < 0 for r in mw)
    RES["MUTATE"]["M_W"] = dict(rows=mw, bites=bool(bite_w))
    P("MUTATE M-W (sign of the S J term flipped): d L / d R " + ", ".join(f"{r['dL_dR']:+.3e}" for r in mw) + f" -> {'BITES (inward)' if bite_w else 'NO BITE'}")
    bite_cp = all(not T2[f][w]["1.0"]["pass_"] for f in A0 for w in READ)
    RES["MUTATE"]["M_CP"] = dict(bites=bool(bite_cp))
    P(f"MUTATE M-CP: uncompensated statistic fails the line on every reading at z 1 -> {'BITES' if bite_cp else 'NO BITE'}")
    bite_wp = any(not T3[f][str(lm)]["clears"] for f in A0 for lm in BINS)
    RES["MUTATE"]["M_WP_x100"] = dict(bites=bool(bite_wp), note="pressure x 100 (added: the frozen / 100 has no power once the gate clears)")
    P(f"MUTATE M-WP (carrier pressure x100): at least one mass no longer clears -> {'BITES' if bite_wp else 'NO BITE'}")
    d100 = {f: {str(lm): gate(lm, a0, pscale=0.01)["clears"] for lm in BINS} for f, a0 in A0.items()}
    RES["MUTATE"]["M_WP_div100_as_frozen"] = dict(clears=d100, note="as frozen; cannot flip a gate that already clears")
    P(f"MUTATE M-WP as frozen (pressure / 100): clears {d100} (no power in this direction; disclosed)")
else:
    ka_ok_cp = RES["KA"]["KA_CP1"]["pass_"] and RES["KA"]["KA_CP2"]["pass_"] and RES["KA"]["KA_CP3"]["pass_"]
    ka_ok_wp = RES["KA"]["KA_W1"]["pass_"] and RES["KA"]["KA_W2"]["pass_"] and RES["KA"]["KA_W3"]["pass_"]
    lab = {}
    Lf = {f: T2[f]["L"]["1.0"]["pass_"] for f in A0}
    Sf = {f: (T2[f]["NC"]["1.0"]["pass_"] or T2[f]["NL"]["1.0"]["pass_"]) for f in A0}
    allfail = all(not T2[f][w]["1.0"]["pass_"] for f in A0 for w in READ)
    if not ka_ok_cp: cp = "NO VERDICT (known answer failed)"
    elif any(Lf.values()): cp = "WL1 LABEL MOVES (reading L passes the compensated line on " + ", ".join(k for k, v in Lf.items() if v) + ")"
    elif all(Sf.values()): cp = "KEY-DEPENDENT"
    elif allfail: cp = "KEY-INDEPENDENT (WL1 scope stands)"
    else: cp = "MIXED: " + json.dumps({f: {w: T2[f][w]['1.0']['pass_'] for w in READ} for f in A0})
    clears = {f: {str(lm): T3[f][str(lm)]["clears"] for lm in BINS} for f in A0}
    if not ka_ok_wp: wp = "NO VERDICT (known answer failed)"
    elif all(not v for f in clears for v in clears[f].values()): wp = "SELF-CLEARING NO-GO"
    else: wp = "NOT A NO-GO AS FROZEN (clears: " + json.dumps(clears) + ")"
    RES["labels_before_lean"] = dict(SWT1_CP=cp, SWT1_WP=wp, lean="see compile.txt; T1 and T3's identity must be certified for the labels to stand")
    P("")
    P(f"LABEL SWT1-CP (pending Lean T1): {cp}")
    P(f"LABEL SWT1-WP (pending Lean T3 identity): {wp}")
P(f"runtime {time.time() - T0:.0f} s. kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
