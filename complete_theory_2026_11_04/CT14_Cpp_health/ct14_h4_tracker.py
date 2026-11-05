#!/usr/bin/env python3
"""CT14 H4: the tracker / freezing branch of C''. Leaf-averaged phi Lagrangian L = X - V + <L_M>(rho), rho = X + V,
<L_M> = (kappa^2 rho / 4 pi) f(s_bar), s_bar = sqrt(8/3pi) fac g_lin(z) / a(rho), a(rho) = a0 sqrt(rho / rho_phi0)
(C'' ties a0 to rho_phi, so an early-rolling phi has a larger a0 and a smaller s_bar than CT12/CT13 assumed).
g_lin and the brackets fac = 10, 1, 0.1 are CT12's verbatim (ct12_leaf_tie.py:112-117, inputs :19-23).
Criteria: FROZEN_CRITERIA.md (H4), written first. 8 pi G = 1, H0 = 1. kappa = 1/2 FITTED; not theory closed."""
import os, math, json, time, resource
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

T0 = time.time(); CH = []
def check(n, ok, note=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"  ({note})" if note else ""), flush=True)

# ---- CT12 inputs verbatim
G = 6.6743e-11; C = 2.99792458e8; MPC = 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KAPPA = 0.5; EPS = KAPPA**2 / (8 * math.pi)
RHO100 = 3 * (1e5 / MPC) ** 2 / (8 * math.pi * G)
OL = 0.666; H = 0.5 * (0.6722 + 0.6856); OB = 0.0224
w_r = 2.4728e-5 * (1 + 0.22711 * 3.046)
X_OVER_B = 4.9; A_S = 2.1e-9
H0 = H * 1e5 / MPC
w_x = X_OVER_B * OB; w_m = OB + w_x
Ez12 = lambda z: math.sqrt(w_r / H**2 * (1 + z)**4 + w_m / H**2 * (1 + z)**3 + OL)       # CT12's E(z), used only inside g_lin
Phi = (2 / 3) * math.sqrt(A_S); delta = 2 * Phi
def g_lin(z):
    rho_t = w_x * RHO100 * (1 + z)**3
    return 4 * math.pi * G * rho_t * delta * C / (H0 * Ez12(z))
def dlng_dN(z):
    e2 = w_r / H**2 * (1 + z)**4 + w_m / H**2 * (1 + z)**3 + OL
    de2 = -4 * w_r / H**2 * (1 + z)**4 - 3 * w_m / H**2 * (1 + z)**3
    return -3 - 0.5 * de2 / e2
# own background (framework inputs as CT12; phi supplies the rest)
Om = w_m / H**2; Orad = w_r / H**2; Ophi0 = 1 - Om - Orad
RHOC = 3.0
hf = lambda x: 2 * (x - math.log1p(x)) - x * x / (1 + x) if x > 1e-3 else x**3 / 3 - x**4 / 2
hp = lambda x: x * x / (1 + x)**2
print("=" * 100); print("CT14 H4: tracker / freezing branch with the leaf-averaged a0 charge, a0 tied to rho_phi"); print("=" * 100)
print(f"  Omega_m {Om:.4f}, Omega_r {Orad:.3e}, Omega_phi0 {Ophi0:.4f}; eps {EPS:.6f}")
# check: CT12's epsbar at today's a0 (central, canonical) reproduced at z 1100/1e4/1e5/4e8
xm = lambda z, fac, a0: math.sqrt(8 / (3 * math.pi)) * fac * g_lin(z) / a0
rep = [EPS * hf(xm(z, 1.0, A0["canonical"])) for z in (1100, 1e4, 1e5, 4e8)]
check("K1 CT12's epsbar (central, canonical, a0 fixed) reproduced: 0.0473 / 1.2 / 14.4 / 5.92e4 (ct12_leaf_tie.out:30)",
      all(abs(a / b - 1) < 0.02 for a, b in zip(rep, [0.0473, 1.2, 14.4, 5.92e4])), " / ".join(f"{v:.3g}" for v in rep))

def make(Vf, dVf):
    def rhs(N, y, Eon, fac, a0):
        phi, pd = y                                   # pd = dphi/dt (units H0)
        a = math.exp(N); z = 1 / a - 1
        V = Vf(phi); dV = dVf(phi)
        rho = 0.5 * pd * pd + V
        Hh = math.sqrt((RHOC * Om / a**3 + RHOC * Orad / a**4 + rho) / 3)
        if Eon:
            rho0 = RHOC * Ophi0
            x = xm(z, fac, a0) / math.sqrt(max(rho, 1e-300) / rho0)
            E = EPS * hf(x); Er = -EPS * x * hp(x) / (2 * rho); Et = EPS * hp(x) * x * Hh * dlng_dN(z)
        else:
            E = Er = Et = 0.0
        Kt = 1 + E + Er * pd * pd
        pdd = (-3 * Hh * (1 + E) * pd - (1 - E) * dV - Er * dV * pd * pd - Et * pd) / Kt
        return [pd / Hh, pdd / Hh]
    return rhs

ZG = [0.0, 1.0, 1.5, 2.33]
NS = np.linspace(-math.log(1 + 1e9), 0.0, 6001)
class Sol:
    """trajectory on a fixed N grid (no dense output: bounded memory)."""
    def __init__(self, r):
        self.t = r.t; self.y = r.y; self.success = r.success and r.status == 0; self.message = r.message
    def sol(self, N):
        return np.array([np.interp(N, self.t, self.y[0]), np.interp(N, self.t, self.y[1])])
def run(rhs, y0, Ni, Eon, fac=1.0, a0=A0["canonical"], dense=False):
    calls = [0]
    def f(N, y, *a):
        calls[0] += 1
        if calls[0] > 3_000_000: raise RuntimeError("step budget exceeded")
        return rhs(N, y, *a)
    def hit0(N, y, *a): return y[0] - 1e-3 * abs(y0[0])    # IPL: phi falling to 1e-3 of its start = runaway up the potential
    hit0.terminal = True; hit0.direction = -1
    grid = NS[NS >= Ni]
    try:
        r = solve_ivp(f, (Ni, 0.0), y0, args=(Eon, fac, a0), method="LSODA", rtol=1e-10, atol=1e-14, t_eval=grid, events=(hit0 if y0[0] > 0 else None))
    except (RuntimeError, ValueError, OverflowError, ZeroDivisionError) as ex:
        class R: pass
        r = R(); r.t = np.array([Ni]); r.y = np.array([[y0[0]], [y0[1]]]); r.success = False; r.status = -1; r.message = str(ex)
    return Sol(r)

def rho_at(sol, Vf, z):
    phi, pd = sol.sol(-math.log(1 + z)); return 0.5 * pd * pd + Vf(phi), pd, phi

def cpl_ratio(w0, wa, z):
    a = 1 / (1 + z); return a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a))
TARGETS = {"B2 thawing": lambda z: cpl_ratio(-0.9, -0.1, z), "B3 freezing": lambda z: cpl_ratio(-0.95, 0.35, z)}

ZI = 1e9; Ni = -math.log(1 + ZI)
members = {}
# thawing
lam = 1.0
members["T1 exp lambda 1, rest"] = dict(V=lambda p, M: M * math.exp(-lam * p), dV=lambda p, M: -lam * M * math.exp(-lam * p), ic=lambda M: [0.0, 0.0])
members["T2 pNGB f 1, phi_i 0.5, rest"] = dict(V=lambda p, M: M * (1 + math.cos(p)), dV=lambda p, M: -M * math.sin(p), ic=lambda M: [0.5, 0.0])
# freezing: inverse power law on the radiation-era tracker at z_i, and frozen undershoot
t_i = 1 / (2 * math.sqrt(RHOC * Orad / 3) * (1 + ZI)**2)          # radiation era t = 1/(2H)
for n in (0.5, 1.0, 2.0, 6.0):
    p_ = 2 / (n + 2)
    def trk(M, n=n, p_=p_):
        A = (n * M / (p_ * (p_ + 0.5))) ** (1 / (n + 2)); return [A * t_i**p_, A * p_ * t_i**(p_ - 1)]
    members[f"F{n:g} IPL tracker IC"] = dict(V=lambda p, M, n=n: M * abs(p)**(-n), dV=lambda p, M, n=n: -n * M * abs(p)**(-n - 1) * np.sign(p), ic=trk)
    def und(M, n=n, p_=p_):
        A = (n * M / (p_ * (p_ + 0.5))) ** (1 / (n + 2)); return [30 * A * t_i**p_, 0.0]
    members[f"F{n:g} IPL frozen undershoot (30x tracker phi)"] = dict(V=lambda p, M, n=n: M * abs(p)**(-n), dV=lambda p, M, n=n: -n * M * abs(p)**(-n - 1) * np.sign(p), ic=und)

results = {}
for name, m in members.items():
    def om0(lM):
        M = math.exp(lM); Vf = lambda p: m["V"](p, M); dVf = lambda p: m["dV"](p, M)
        s_ = run(make(Vf, dVf), m["ic"](M), Ni, False)
        if not s_.success or s_.t[-1] < -1e-6: return float('nan')
        r0 = rho_at(s_, Vf, 0.0)[0]; return r0 / (RHOC * Ophi0) - 1
    # normalisation on the E-off run (a normalisation of V's scale, not a knob)
    grid = np.linspace(-24, 24, 25); vals = []
    for lM in grid:
        try: vals.append(om0(lM) if run is not None else np.nan)
        except Exception: vals.append(np.nan)
    vals = np.array(vals); idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
    if not len(idx):
        print(f"  {name}: no normalisation found"); continue
    lM = brentq(om0, grid[idx[0]], grid[idx[0] + 1], xtol=1e-12); M = math.exp(lM)
    Vf = lambda p, M=M, m=m: m["V"](p, M); dVf = lambda p, M=M, m=m: m["dV"](p, M)
    rhs = make(Vf, dVf); y0 = m["ic"](M)
    off = run(rhs, y0, Ni, False)
    rz_off = [rho_at(off, Vf, z)[0] for z in ZG]
    w0 = (lambda r, pd, ph: (0.5 * pd * pd - Vf(ph)) / r)(*rho_at(off, Vf, 0.0))
    row = dict(M=M, w0=w0, ratio=[r / rz_off[0] for r in rz_off], brackets={})
    worst = 0.0; first_bad = None; ktmin = 1.0; Emax = 0.0
    for fo, a0 in A0.items():
        for lab, fac in (("x10", 10.0), ("central", 1.0), ("div10", 0.1)):
            on = run(rhs, y0, Ni, True, fac, a0)
            ok_run = on.success and on.t[-1] >= -1e-6
            if not ok_run:
                row["brackets"][f"{fo}|{lab}"] = dict(status="integration broke", t=float(on.t[-1]), msg=on.message)
                worst = float("inf"); first_bad = first_bad or (fo, lab, "integration broke at z = %.3g" % (math.exp(-on.t[-1]) - 1)); continue
            dl = [abs(math.log(rho_at(on, Vf, z)[0] / r)) for z, r in zip(ZG, rz_off)]
            # scan history for E, K_t and the first z where |d ln rho| > 0.0023
            Ns = on.t[::2]; fb = None; em = 0.0; km = 1.0
            for N_ in Ns:
                z = math.exp(-N_) - 1
                ph1, pd1 = on.sol(N_); ph0, pd0 = off.sol(N_)
                r1 = 0.5 * pd1 * pd1 + Vf(ph1); r0 = 0.5 * pd0 * pd0 + Vf(ph0)
                x = xm(z, fac, a0) / math.sqrt(max(r1, 1e-300) / (RHOC * Ophi0))
                E = EPS * hf(x); Kt = 1 + E - EPS * x * hp(x) / (2 * r1) * pd1 * pd1
                em = max(em, E); km = min(km, Kt)
                if fb is None and r1 > 0 and r0 > 0 and abs(math.log(r1 / r0)) > 0.0023: fb = z
            row["brackets"][f"{fo}|{lab}"] = dict(dlnrho_late=max(dl), first_z_over_0p001dex=fb, E_max=em, Kt_min=km)
            worst = max(worst, max(dl)); Emax = max(Emax, em); ktmin = min(ktmin, km)
            if max(dl) > 0.0023 and first_bad is None: first_bad = (fo, lab, fb)
    row.update(worst_dlnrho_late=worst, survives=bool(worst <= 0.0023 and ktmin > 0), E_max=Emax, Kt_min=ktmin, first_bad=first_bad)
    reach = {}
    for tn, tf in TARGETS.items():
        dev = max(abs(0.5 * math.log10(row["ratio"][i] / tf(z))) for i, z in enumerate(ZG) if z > 0)
        reach[tn] = dev
    row["reach_dex"] = reach
    results[name] = row
    print(f"  {name:42s} w0 {w0:+.3f}; a0(z)/a0(0) at z 1/1.5/2.33 = {', '.join(f'{math.sqrt(r):.4f}' for r in row['ratio'][1:])}; "
          f"E on/off worst |d ln rho| (z<=2.33) {worst:.2e}; max E {Emax:.3g}; min K_t {ktmin:.3g}; {'SURVIVES' if row['survives'] else 'BROKEN'}"
          + ("" if row["survives"] else f" (first: {first_bad})") + f"; reach dev B2 {reach['B2 thawing']:.3f} B3 {reach['B3 freezing']:.3f} dex  ({time.time()-T0:.0f}s)", flush=True)
    for k_, v_ in row["brackets"].items():
        if "dlnrho_late" in v_:
            print(f"      {k_:18s} |d ln rho| late {v_['dlnrho_late']:.2e}; first z over 0.001 dex {v_['first_z_over_0p001dex']}; max E {v_['E_max']:.3g}; min K_t {v_['Kt_min']:.4g}")
        else:
            print(f"      {k_:18s} {v_}")
surv = [k_ for k_, v_ in results.items() if v_["survives"]]
brk = [k_ for k_, v_ in results.items() if not v_["survives"]]
print(f"\n  survivors: {surv}\n  broken: {brk}")
reachB3 = [k_ for k_ in surv if results[k_]["reach_dex"]["B3 freezing"] <= 0.05]
reachB2 = [k_ for k_ in surv if results[k_]["reach_dex"]["B2 thawing"] <= 0.05]
print(f"  survivors reaching B2 within 0.05 dex: {reachB2}\n  survivors reaching B3 within 0.05 dex: {reachB3}")
check("H4 at least one member survives (history unchanged to 0.001 dex, K_t > 0)", bool(surv))
json.dump(results, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ct14_h4_tracker.json"), "w"), indent=1, default=str)
print(f"\nchecks {sum(CH)}/{len(CH)}; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB; {time.time()-T0:.0f}s")
print("kappa = 1/2 FITTED; not theory closed.")
