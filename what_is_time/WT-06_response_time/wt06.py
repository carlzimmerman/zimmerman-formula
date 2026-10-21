#!/usr/bin/env python3
"""WT-06: how long does the framework's extra pull take to catch up after a sudden baryon change?

Criteria: FROZEN_CRITERIA.md (f11ca13c3, committed alone before this script existed).
Run:
  OMP_NUM_THREADS=1 nice -n 10 python3 wt06.py                 -> wt06.out, wt06_results.json        (exit 0 = K1-K4 pass, 2 = a K fails)
  WT06_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 wt06.py   -> wt06_MUTATE.out, wt06_results_MUTATE.json (exit 1 = all teeth bite, 3 = not)
Parent: CFG938 (criteria 7a0d41e8b). Readings: M-I (CFG938 ideal = CFG747/776 dynamics with the full R), M-D(alpha) (CFG541 FIX-1 /
CFG638 overdamped drift), M-ID(alpha) (parent + drift). MOND-I (u = u_law(g_N) instantly) is a same-pipeline comparison only.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; Z = 5.7888; cold energy's mass required; no particle species;
not theory closed; nothing here says the data favour the framework.
"""
import os, sys, io, json, math, time, resource, contextlib
import numpy as np
import sympy as sp
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("WT06_MUTATE", "0") == "1"
SMOKE = os.environ.get("WT06_SMOKE", "0") == "1"                      # code test only; never written into the lane dir
OUTDIR = os.environ.get("WT06_OUTDIR", HERE)
if SMOKE and os.path.abspath(OUTDIR) == HERE:
    sys.exit("smoke runs must set WT06_OUTDIR outside the lane directory")
TAG = "_MUTATE" if MUT else ""
CRIT = "f11ca13c3"
T0 = time.time(); WALL_CAP = 60 * 60.0; RSS_LIMIT = 1.0e9
OUT = []
RES = {"lane": "WT-06", "criteria": CRIT, "mutate": MUT, "smoke": SMOKE, "checks": {}, "derivation": {}, "cells": {},
       "classes": {}, "report_only": {}}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def guard(where):
    if rss() > RSS_LIMIT:
        P(f"RSS GUARD HIT at {where}: {rss()/1e9:.3f} GB"); dump(); sys.exit(4)


def elapsed():
    return time.time() - T0


def dump():
    RES["runtime_s"] = round(elapsed(), 1); RES["peak_rss_GB"] = round(rss() / 1e9, 3)
    json.dump(RES, open(os.path.join(OUTDIR, f"wt06_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(OUTDIR, f"wt06{TAG}.out"), "w").write("\n".join(OUT) + "\n")


def chk(name, ok, detail):
    RES["checks"][name] = {"pass": bool(ok), "detail": detail}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


# ------------------------------------------------------------------------------------------------ constants
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                          # read only: the record's footings
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G, C_SI, KPC, PC = 6.67430e-11, 299792458.0, 3.0856775814913673e19, 3.0856775814913673e16
MYR = 3.15576e13; GYR = 1e3 * MYR
UPS = 0.61                                                            # CFG938's Upsilon
ALPHAS = (0.5, 1.186)
K764 = {"canonical": (0.457088189614875, 1.1956707992771565), "alt": (0.5248074602497725, 1.1956707992771565)}
T763 = {"canonical": (0.72443596007499, 8.0 / math.log(10.0)), "alt": (0.831763771102671, 8.0 / math.log(10.0))}
SYSTEMS = {"NGC3198": (3.14, 35.66), "DDO154": (0.37, 4.96)}         # R_d, R_HI [kpc] from SPARC_Lelli2016c.mrt
FRACS = (0.0, 0.2, 0.5)                                               # 0.0 = unperturbed control (K1b)
READINGS = [("M-I", 1.0, 0.0), ("M-D(0.5)", 0.0, 0.5), ("M-D(1.186)", 0.0, 1.186),
            ("M-ID(0.5)", 1.0, 0.5), ("M-ID(1.186)", 1.0, 1.186)]
CELLS = ("2Rd", "5Rd", "RHI")
LAGCELLS = ("2Rd", "5Rd")


def ulaw(gN, a0):                                                     # u = g_law - g_N, stable form
    return 2.0 * gN * a0 / (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def glaw(gN, a0):
    return gN + ulaw(gN, a0)


def Rfun(u, a0):                                                      # R(u) = K W_rem' = u^2/(a0 - u)  (MU2: u^2/a0)
    return u * u / a0 if (MUT and MU2_ON) else u * u / (a0 - u)


MU2_ON = True                                                         # only read when MUT

P("WT-06: response time of the extra pull after a sudden baryon change")
P(f"  criteria {CRIT}; kappa = 1/2 FITTED; footings never pooled; Z = 5.7888; not theory closed; MUTATE={MUT}; SMOKE={SMOKE}")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2")

# ================================================================================================ (a) sympy derivations
P("\n(a) DERIVATION (sympy)")
r, Gs, a0s, us, gNs, al, ta, mus, Mbs, Mcs, cs = sp.symbols("r G a_0 u g_N alpha tau mu M_b M_c c", positive=True)
Ks = 4 * sp.pi * Gs
Rs = us ** 2 / (a0s - us)
Wfull = (-a0s * us - a0s ** 2 * sp.log(1 - us / a0s)) / Ks
Dfull = sp.simplify(Ks * sp.diff(Wfull, us))
ok_D = sp.simplify(Dfull - us - Rs) == 0
# S1: the medium's potential chi is sourced by rho_c only; Phi by rho_b + rho_c
Mc_f = sp.Function("M_c")(r); Mb_f = sp.Function("M_b")(r)
chip = Gs * Mc_f / r ** 2
ok_S1 = sp.simplify(sp.diff(r ** 2 * chip, r) / r ** 2 - Ks * sp.diff(Mc_f, r) / (4 * sp.pi * r ** 2)) == 0
ok_S1b = not chip.has(Mb_f)
phip = Gs * (Mb_f + Mc_f) / r ** 2
ok_S1c = sp.simplify(sp.diff(r ** 2 * phip, r) / r ** 2 - Ks * sp.diff(Mb_f + Mc_f, r) / (4 * sp.pi * r ** 2)) == 0
# S2: force on a medium marker from the parent energy E = int dr [-G(M_b+M_c)^2/(2r^2) + 4 pi r^2 W_full(G M_c/r^2)]
e_dens = -Gs * (Mbs + Mcs) ** 2 / (2 * r ** 2) + 4 * sp.pi * r ** 2 * Wfull.subs(us, Gs * Mcs / r ** 2)
F_per_m = sp.diff(e_dens, Mcs)                                         # moving mass m outward by dr: dE = -m dr de/dM_c
u_e = Gs * Mcs / r ** 2; gN_e = Gs * Mbs / r ** 2
ok_S2 = sp.simplify(F_per_m - (Rs.subs(us, u_e) - gN_e)) == 0
# S3: marker with fixed enclosed mass mu: f(r) = R(G mu/r^2) - g_N(r); omega^2 = -df/dr
gNf = sp.Function("g_N")(r)
f_mark = Rs.subs(us, Gs * mus / r ** 2) - gNf
w2 = sp.simplify(-sp.diff(f_mark, r))
Rp = sp.diff(Rs, us)
w2_claim = (2 * us * Rp / r).subs(us, Gs * mus / r ** 2) + sp.diff(gNf, r)
ok_S3 = sp.simplify(w2 - w2_claim) == 0
ok_Rp = sp.simplify(Rp - us * (2 * a0s - us) / (a0s - us) ** 2) == 0
# deep point-mass limit: R -> u^2/a0, g_N = G M/r^2, equilibrium u = sqrt(a0 g_N): omega^2 = 2 g_N/r, (omega t_dyn)^2 = 2 g_N/g
Mpt = sp.symbols("M", positive=True)
w2_deep = (2 * us * sp.diff(us ** 2 / a0s, us) / r + sp.diff(Gs * Mpt / r ** 2, r)).subs(us, sp.sqrt(a0s * Gs * Mpt / r ** 2))
ok_S3d = sp.simplify(w2_deep - 2 * Gs * Mpt / r ** 3) == 0
gtot_deep = Gs * Mpt / r ** 2 + sp.sqrt(a0s * Gs * Mpt / r ** 2)
wt_deep = sp.simplify(w2_deep * r / gtot_deep - 2 * (Gs * Mpt / r ** 2) / gtot_deep)
ok_S3e = wt_deep == 0
# S4: drift v = alpha tau (G mu/r^2 - u_law(r)); Gamma = -dv/dr at equilibrium = alpha tau 4 pi G rho_ph
uLf = sp.Function("u_L")(r)
v_dr = al * ta * (Gs * mus / r ** 2 - uLf)
Gam = sp.simplify(-sp.diff(v_dr, r))                                   # tau held locally constant (linear test)
Mph = r ** 2 * uLf / Gs; rho_ph = sp.diff(Mph, r) / (4 * sp.pi * r ** 2)
ok_S4 = sp.simplify(Gam.subs(mus, r ** 2 * uLf / Gs) - al * ta * 4 * sp.pi * Gs * rho_ph) == 0
# S5: M-ID linear: d(dr)/dt = dv - Gamma dr, d(dv)/dt = -omega^2 dr  ->  s^2 + Gamma s + omega^2 = 0
Gm, wm, s_ = sp.symbols("Gamma omega s")
Mlin = sp.Matrix([[-Gm, 1], [-wm ** 2, 0]])
ok_S5 = sp.expand(Mlin.charpoly(s_).as_expr() - (s_ ** 2 + Gm * s_ + wm ** 2)) == 0
# S6: residual right after the blowout (field part unchanged, u = u_old): D(0+) = log10[(g_N' + u_old)/g_law(g_N')]
# S7: gradual loss over T for a first-order relaxer: residual d' = -Gamma d + Delta/T, d(0) = 0  ->  d(T)/Delta
tt, TT, Dl = sp.symbols("t T Delta", positive=True)
dfun = sp.Function("d")
sol = sp.dsolve(sp.Eq(dfun(tt).diff(tt), -Gm * dfun(tt) + Dl / TT), dfun(tt), ics={dfun(0): 0}).rhs
supp = sp.simplify(sol.subs(tt, TT) / Dl)
ok_S7 = sp.simplify(supp - (1 - sp.exp(-Gm * TT)) / (Gm * TT)) == 0
P(f"  S0 D_full = u + R(u), R = u^2/(a0-u)                         : {ok_D}")
P(f"  S1 chi' = G M_c(<r)/r^2 solves D^2 chi = K rho_c; no M_b in it : {ok_S1} / {ok_S1b}  (Phi: {ok_S1c})")
P(f"  S2 parent force on a medium marker = R(u) - g_N              : {ok_S2}")
P(f"  S3 omega^2 = 2 u R'(u)/r + dg_N/dr; R' = u(2a0-u)/(a0-u)^2     : {ok_S3} / {ok_Rp}")
P(f"  S3 deep point mass: omega^2 = 2 g_N/r, (omega t_dyn)^2 = 2 g_N/g: {ok_S3d} / {ok_S3e}")
P(f"  S4 drift rate Gamma = alpha tau 4 pi G rho_ph                 : {ok_S4}")
P(f"  S5 parent + drift: s^2 + Gamma s + omega^2 = 0                 : {ok_S5}")
P(f"  S7 gradual loss over T: peak residual x (1 - e^-GT)/(G T)      : {ok_S7}")
sym_ok = all([ok_D, ok_S1, ok_S1b, ok_S1c, ok_S2, ok_S3, ok_Rp, ok_S3d, ok_S3e, ok_S4, ok_S5, ok_S7])
RES["derivation"] = {"S0_Dfull_eq_u_plus_R": ok_D, "S1_chi_constraint_rho_c_only": ok_S1 and ok_S1b, "S1_Phi_total": ok_S1c,
                     "S2_marker_force_R_minus_gN": ok_S2, "S3_omega2": ok_S3 and ok_Rp, "S3_deep_point_mass": ok_S3d and ok_S3e,
                     "S4_drift_rate": ok_S4, "S5_damped_oscillator": ok_S5, "S7_gradual_suppression": ok_S7, "all": sym_ok}
P("  Reading: the extra pull on baryons and light is u = chi' = G M_c(<r)/r^2, the medium's own Newtonian pull. chi has no")
P("  baryon source, so at t = 0+ the extra pull is EXACTLY unchanged; only the medium's motion can change it. The field part")
P("  (Phi, chi) is a constraint: Phi re-forms at c (time r/c), chi instantly in the medium frame. The mass part moves under")
P("  R(u) - g_N: self-gravity cancelled, restoring force from the baryons only.")

# ================================================================================================ profiles
NG = 60001


class System:
    def __init__(self, name):
        Rd, RHI = SYSTEMS[name]
        d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", f"{name}_rotmod.dat"), comments="#")
        self.name = name; self.R = d[:, 0] * KPC
        Vg, Vd, Vb = d[:, 3] * 1e3, d[:, 4] * 1e3, d[:, 5] * 1e3
        self.Vbar2 = Vg * np.abs(Vg) + UPS * (Vd * np.abs(Vd) + Vb * np.abs(Vb))
        self.Ms_pts = UPS * self.R * (Vd * np.abs(Vd) + Vb * np.abs(Vb)) / G
        self.Mg_pts = self.R * Vg * np.abs(Vg) / G
        self.Rd = Rd * KPC; self.RHI = RHI * KPC
        self.cells = np.array([2 * self.Rd, 5 * self.Rd, self.RHI])
        self.lg = np.linspace(math.log(1e-3 * self.Rd), math.log(1e5 * self.Rd), NG)
        self.LG0 = self.lg[0]; self.IDL = 1.0 / (self.lg[1] - self.lg[0]); self.rg = np.exp(self.lg)
        self.Ms = self._comp(self.rg, self.Ms_pts); self.Mg = self._comp(self.rg, self.Mg_pts)
        self.tab = {}
        for f in FRACS:
            Mb = np.maximum.accumulate(self.Ms + (1.0 - f) * self.Mg)
            rho_b = np.gradient(Mb, self.rg) / (4 * np.pi * self.rg ** 2)
            for foot in FOOTS:
                a0 = A0[foot]; gN = G * Mb / self.rg ** 2
                Mph = self.rg ** 2 * ulaw(gN, a0) / G
                rho_ph = np.gradient(Mph, self.rg) / (4 * np.pi * self.rg ** 2)
                tau = 1.0 / np.sqrt(4 * np.pi * G * np.maximum(rho_b + rho_ph, 1e-300))
                self.tab[(f, foot)] = {"Mb": Mb, "tau": tau, "rho_ph": rho_ph, "rho_b": rho_b, "Mph": Mph}

    def _comp(self, rr, pts):
        p = PchipInterpolator(self.R, pts)
        out = np.empty_like(rr); lo = rr < self.R[0]; hi = rr > self.R[-1]; mid = ~(lo | hi)
        out[mid] = p(rr[mid]); out[lo] = pts[0] * (rr[lo] / self.R[0]) ** 3; out[hi] = pts[-1]
        return out

    def lk1(self, arr, rr):                                           # linear in log r on the grid (scalar / 1-D)
        x = (np.log(rr) - self.LG0) * self.IDL
        i = np.clip(np.asarray(x).astype(np.int64), 0, NG - 2); w = np.clip(x - i, 0.0, 1.0)
        return arr[i] + w * (arr[i + 1] - arr[i])

    def gN(self, f, rr):
        return G * self.lk1(self.tab[(f, "canonical")]["Mb"], rr) / rr ** 2

    def tdyn(self, foot, rr):
        return np.sqrt(rr / glaw(self.gN(0.0, rr), A0[foot]))


P("\nPROFILES (spherical-equivalent SPARC baryons, Upsilon 0.61, PCHIP; r^3 inside, constant outside)")
SYS = {}
for nm in SYSTEMS:
    S_ = System(nm); SYS[nm] = S_
    for foot in FOOTS:
        td = S_.tdyn(foot, S_.cells)
        gfrac = S_.lk1(S_.Mg, S_.cells) / S_.lk1(S_.tab[(0.0, foot)]["Mb"], S_.cells)
        gN0 = S_.gN(0.0, S_.cells)
        P(f"  {nm:8s} {foot:9s} cells 2Rd/5Rd/RHI = {', '.join(f'{c/KPC:.2f}' for c in S_.cells)} kpc; t_dyn = "
          f"{', '.join(f'{t/MYR:.1f}' for t in td)} Myr; gas share of M_b = {', '.join(f'{g:.3f}' for g in gfrac)}; "
          f"g_N/a0 = {', '.join(f'{x/A0[foot]:.3f}' for x in gN0)}")
        RES["cells"].setdefault(nm, {})[foot] = {"r_kpc": (S_.cells / KPC).tolist(), "t_dyn_Myr": (td / MYR).tolist(),
                                                  "gas_share": gfrac.tolist(), "gN_over_a0": (gN0 / A0[foot]).tolist()}
    mph_ok = all((np.diff(S_.tab[(0.0, ft)]["Mph"][S_.rg >= 0.01 * S_.Rd]) >= 0).all() for ft in FOOTS)
    P(f"  {nm}: law phantom mass monotone (positive rho_ph) from 0.01 R_d: {mph_ok}")

# ================================================================================================ K1a static limit
P("\nK1a static limit of the parent (identity: R is built from the law; this checks the code)")
k1max = 0.0
for nm, S_ in SYS.items():
    good = S_.Vbar2 > 0
    for foot in FOOTS:
        a0 = A0[foot]
        for rr, v2 in zip(S_.R[good], S_.Vbar2[good]):
            gn = v2 / rr
            fn = lambda x: Rfun(x, a0) - gn
            hi = a0 * (1 - 1e-15) if not (MUT and MU2_ON) else 1e3 * a0
            uu = brentq(fn, 1e-300, hi, xtol=1e-40, rtol=1e-15, maxiter=500)
            k1max = max(k1max, abs((gn + uu) / float(glaw(gn, a0)) - 1.0))
k1a = chk("K1a_static_limit_is_law", k1max <= 1e-12, f"max |g/g_law - 1| over SPARC radii of both systems, both footings = {k1max:.2e} (line 1e-12)")

# ================================================================================================ generic RK4
def rk4(deriv, y, h):
    k1 = deriv(y); y2 = [a + 0.5 * h * b for a, b in zip(y, k1)]
    k2 = deriv(y2); y3 = [a + 0.5 * h * b for a, b in zip(y, k2)]
    k3 = deriv(y3); y4 = [a + h * b for a, b in zip(y, k3)]
    k4 = deriv(y4)
    return [a + h / 6.0 * (b1 + 2 * b2 + 2 * b3 + b4) for a, b1, b2, b3, b4 in zip(y, k1, k2, k3, k4)]


# ================================================================================================ K2 Newtonian textbook mass loss
k2 = True
if not MUT:
    P("\nK2 Newtonian textbook mass loss (test particle, point mass, units G = M = r0 = 1; same RK4 as the shell code)")

    def orbit_deriv(Mfun, j2):
        def d(y):
            rr, vv, tt_ = y
            return [vv, j2 / rr ** 3 - Mfun(tt_) / rr ** 2, 1.0]
        return d

    dl = 0.2
    a_sm = (1 - dl) / (1 - 2 * dl); Pr = 2 * math.pi * a_sm ** 1.5 / math.sqrt(1 - dl); h = Pr / 20000
    y = [1.0, 0.0, 0.0]; der = orbit_deriv(lambda t: 1 - dl, 1.0)
    rs_, vs_, ts_ = [1.0], [0.0], [0.0]
    for _ in range(int(1.2 * 20000)):
        y = rk4(der, y, h); rs_.append(y[0]); vs_.append(y[1]); ts_.append(y[2])
    rs_, vs_, ts_ = map(np.array, (rs_, vs_, ts_))
    i = int(np.argmax(rs_)); x0, x1, x2 = rs_[i - 1], rs_[i], rs_[i + 1]
    apo = x1 - 0.25 * (x2 - x0) ** 2 / (x2 - 2 * x1 + x0)
    up = np.where((vs_[1:-1] < 0) & (vs_[2:] >= 0))[0]
    j = up[0] + 1; tper = ts_[j] - vs_[j] * (ts_[j + 1] - ts_[j]) / (vs_[j + 1] - vs_[j])
    e_apo = abs(apo / (1 / (1 - 2 * dl)) - 1); e_per = abs(tper / Pr - 1)
    E05 = 0.5 * 1.0 ** 2 - (1 - 0.5) * 1.0 / 1.0                      # tangential v = 1 at r = 1 after losing 0.5
    TL = 300 * 2 * math.pi; hA = 2 * math.pi / 400
    der = orbit_deriv(lambda t: 1 - dl * min(t, TL) / TL, 1.0)
    y = [1.0, 0.0, 0.0]
    nA = int((TL + 20 * 2 * math.pi * 1.25 ** 1.5 / math.sqrt(0.8)) / hA); acc = []; tcut = TL
    for _ in range(nA):
        y = rk4(der, y, hA)
        if y[2] > tcut:
            acc.append(y[0])
    rA = float(np.mean(acc)); e_ad = abs(rA / 1.25 - 1)
    k2 = chk("K2_impulsive_apocentre", e_apo <= 1e-4, f"delta 0.2: apocentre {apo:.6f} vs 5/3, rel {e_apo:.1e} (line 1e-4)")
    k2 &= chk("K2_impulsive_period", e_per <= 1e-4, f"radial period {tper:.6f} vs {Pr:.6f}, rel {e_per:.1e} (line 1e-4)")
    k2 &= chk("K2_half_loss_unbound", abs(E05) <= 1e-12, f"delta 0.5: specific energy {E05:.1e} (line 1e-12)")
    k2 &= chk("K2_adiabatic", e_ad <= 2e-3, f"delta 0.2 over 300 orbits: <r> = {rA:.5f} vs 1.25, rel {e_ad:.1e} (line 2e-3)")

# ================================================================================================ K3 single-marker clocks
def prony(x, dt, nterm):
    x = np.asarray(x)
    if nterm == 1:
        a = np.dot(x[1:], x[:-1]) / np.dot(x[:-1], x[:-1]); return np.array([np.log(a + 0j) / dt])
    A = np.vstack([x[1:-1], x[:-2]]).T; b = x[2:]
    (a1, a2), *_ = np.linalg.lstsq(A, b, rcond=None)
    z = np.roots([1.0, -a1, -a2]); return np.log(z.astype(complex)) / dt


P("\nK3 clocks: single marker, linear displacement 1e-5 r, NGC 3198 canonical, f = 0 field (MU3 flips the drift sign)")
S_ = SYS["NGC3198"]; foot = "canonical"; a0 = A0[foot]; tb = S_.tab[(0.0, foot)]
drift_sign = -1.0 if MUT else 1.0
k3 = True; K3rows = {}
for cname, rc in zip(("2Rd", "5Rd"), S_.cells[:2]):
    gN = lambda x: G * S_.lk1(tb["Mb"], x) / x ** 2
    taur = lambda x: S_.lk1(tb["tau"], x)
    muc = rc ** 2 * float(ulaw(gN(rc), a0)) / G
    uc = G * muc / rc ** 2; hh = 1e-7 * rc
    dgdr = (gN(rc + hh) - gN(rc - hh)) / (2 * hh)
    duLdr = (ulaw(gN(rc + hh), a0) - ulaw(gN(rc - hh), a0)) / (2 * hh)
    Rp_ = uc * (2 * a0 - uc) / (a0 - uc) ** 2
    w2n = 2 * uc * Rp_ / rc + dgdr
    for rd, cin, alp in READINGS:
        Gam_p = alp * float(taur(rc)) * (2 * uc / rc + duLdr)
        if cin and alp == 0:
            sp_ = np.array([1j * math.sqrt(w2n), -1j * math.sqrt(w2n)])
        elif cin:
            sp_ = np.roots([1.0, Gam_p, w2n]).astype(complex)
        else:
            sp_ = np.array([-Gam_p + 0j])
        tsc = 1.0 / max(abs(sp_).max(), 1e-300); hstep = tsc / 400; nst = int(40 * tsc / hstep)

        def der(y, cin=cin, alp=alp):
            rr, vv = y
            u_ = G * muc / rr ** 2
            vs = drift_sign * alp * taur(rr) * (u_ - ulaw(gN(rr), a0))
            return [cin * vv + vs, cin * (Rfun(u_, a0) - gN(rr))]
        y = [np.array([rc * (1 + 1e-5)]), np.array([0.0])]; xs = [1e-5 * rc]
        for _ in range(nst):
            y = rk4(der, y, hstep); xs.append(y[0][0] - rc)
        xs = np.array(xs)
        if not np.all(np.isfinite(xs)) or np.abs(xs).max() > 0.5 * rc:
            meas = np.array([np.inf + 0j]); err = np.inf
        else:
            meas = prony(xs, hstep, 1 if cin == 0 else 2)
            err = max(min(abs(m - p) for m in meas) / abs(p) for p in sp_)
        line = 0.01 if (cin and alp > 0) else 0.005
        K3rows[f"{cname}:{rd}"] = {"pred": [complex(p) for p in sp_], "meas": [complex(m) for m in meas], "rel_err": err, "line": line}
        ok = err <= line
        k3 &= ok
        P(f"    {cname} {rd:12s} pred s t_dyn = {', '.join(f'{(p*S_.tdyn(foot, rc)).real:+.4f}{(p*S_.tdyn(foot, rc)).imag:+.4f}i' for p in sp_)}"
          f"  rel err {err:.1e} (line {line}) {'ok' if ok else 'FAIL'}")
    K3rows[f"{cname}:omega_tdyn"] = math.sqrt(w2n) * float(S_.tdyn(foot, rc))
    K3rows[f"{cname}:Gamma_tdyn(alpha=1)"] = float(taur(rc)) * (2 * uc / rc + duLdr) * float(S_.tdyn(foot, rc))
    K3rows[f"{cname}:sqrt(2gN/g)"] = math.sqrt(2 * gN(rc) / float(glaw(gN(rc), a0)))
k3 = chk("K3_clocks_match_sympy", k3, "M-I period, M-D rate, M-ID roots vs the derived formulas (lines 0.5% / 0.5% / 1%)")
k3_md = all(v["rel_err"] <= v["line"] for k_, v in K3rows.items() if isinstance(v, dict) and "M-D" in k_)
RES["K3"] = K3rows
P(f"  linear clocks at NGC 3198 (canonical): omega t_dyn = {K3rows['2Rd:omega_tdyn']:.3f} (2Rd), {K3rows['5Rd:omega_tdyn']:.3f} (5Rd);"
  f" deep-point-mass sqrt(2gN/g) = {K3rows['2Rd:sqrt(2gN/g)']:.3f}, {K3rows['5Rd:sqrt(2gN/g)']:.3f};"
  f" Gamma t_dyn / alpha = {K3rows['2Rd:Gamma_tdyn(alpha=1)']:.3f}, {K3rows['5Rd:Gamma_tdyn(alpha=1)']:.3f}")
guard("K3")


# ================================================================================================ B-F shell runs (primary)
def run_BF(S_, rows, Nc=2000, dt_fac=1.0, rin_fac=1.0, rout_fac=1.0, Tfac=60.0, label=""):
    """rows: list of dicts with foot, f, cin, alpha, mond. Returns t (s), D (rows, cells, nt), diagnostics."""
    n = len(rows)
    a0r = np.array([A0[q["foot"]] for q in rows])[:, None]
    cin = np.array([q["cin"] for q in rows], float)[:, None]
    cdr = np.array([q["alpha"] for q in rows], float)[:, None]
    mond = np.array([q["mond"] for q in rows], bool)
    rin, rout = 0.02 * S_.Rd * rin_fac, 50 * S_.Rd * rout_fac
    rm = np.exp(np.linspace(math.log(rin), math.log(rout), Nc + 1))[1:]
    rm = np.unique(np.concatenate([rm, S_.cells])); N = rm.size
    keys_b = sorted(set(q["f"] for q in rows)); keys_t = sorted(set((q["f"], q["foot"]) for q in rows))
    MB = np.vstack([S_.tab[(f, "canonical")]["Mb"] for f in keys_b]); tidB = np.array([keys_b.index(q["f"]) for q in rows])[:, None]
    TAU = np.vstack([S_.tab[k]["tau"] for k in keys_t]); tidT = np.array([keys_t.index((q["f"], q["foot"])) for q in rows])[:, None]
    MB0 = S_.tab[(0.0, "canonical")]["Mb"]

    def lk(T, tid, rr):
        x = (np.log(rr) - S_.LG0) * S_.IDL
        i = x.astype(np.int64); np.clip(i, 0, NG - 2, out=i); w = x - i; np.clip(w, 0.0, 1.0, out=w)
        t0 = T[tid, i]; return t0 + w * (T[tid, i + 1] - t0)

    # initial law state of the ORIGINAL baryons (t = 0-); markers carry inclusive enclosed mass mu_k
    gN0 = G * S_.lk1(MB0, rm) / rm ** 2
    mu0 = rm[None, :] ** 2 * ulaw(gN0[None, :], a0r) / G
    core = (rin ** 2 * ulaw(G * S_.lk1(MB0, np.array([rin])) / rin ** 2, a0r[:, 0]) / G)
    m = np.diff(np.concatenate([core[:, None], mu0], axis=1), axis=1)
    if (m <= 0).any():
        P(f"  WARNING {label}: {int((m <= 0).sum())} non-positive marker masses")
    mu0 = core[:, None] + np.cumsum(m, axis=1)                        # exactly what the code evaluates
    td_rows = np.array([[float(S_.tdyn(q["foot"], np.array([c]))[0]) for c in S_.cells] for q in rows])
    tdmin = min(float(S_.tdyn(ft, rm).min()) for ft in FOOTS)
    dt = 0.02 * tdmin * dt_fac
    Tmax = Tfac * max(float(S_.tdyn(ft, np.array([S_.cells[1]]))[0]) for ft in FOOTS)
    dtout = 0.02 * min(float(S_.tdyn(ft, np.array([S_.cells[0]]))[0]) for ft in FOOTS)
    nout = max(1, int(round(dtout / dt))); nsteps = int(math.ceil(Tmax / dt / nout)) * nout
    r = np.repeat(rm[None, :], n, axis=0); v = np.zeros_like(r)
    st = {"order": np.repeat(np.arange(N)[None, :], n, axis=0), "perm": np.zeros(n, bool), "resorts": np.zeros(n, int)}
    gNc = G * np.vstack([S_.lk1(S_.tab[(q["f"], "canonical")]["Mb"], S_.cells) for q in rows]) / S_.cells[None, :] ** 2
    integrate = ~mond & ((cin[:, 0] > 0) | (cdr[:, 0] > 0))

    def get_mu(rr):
        o = st["order"]; rs = np.take_along_axis(rr, o, 1)
        bad = (np.diff(rs, axis=1) < 0).any(axis=1)
        if bad.any():
            ib = np.where(bad)[0]
            sub = np.argsort(np.take_along_axis(rr[ib], o[ib], 1), axis=1, kind="stable")
            o[ib] = np.take_along_axis(o[ib], sub, 1)
            st["resorts"][ib] += 1
            st["perm"][ib] = (o[ib] != np.arange(N)[None, :]).any(axis=1)
        mu = mu0
        if st["perm"].any():
            mu = mu0.copy(); ip = np.where(st["perm"])[0]
            ms = core[ip, None] + np.cumsum(np.take_along_axis(m[ip], o[ip], 1), axis=1)
            tmp = np.empty_like(ms); np.put_along_axis(tmp, o[ip], ms, 1); mu[ip] = tmp
        return mu

    def deriv(y):
        rr, vv = y
        mu = get_mu(rr); u = G * mu / rr ** 2
        gN = G * lk(MB, tidB, rr) / rr ** 2
        dr = cin * vv
        if (cdr > 0).any():
            vs = drift_sign_run * cdr * lk(TAU, tidT, rr) * (u - ulaw(gN, a0r)); dr = dr + vs
        dv = cin * (Rfun(u, a0r) - gN)
        return [dr * integrate[:, None], dv * integrate[:, None]]

    nt = nsteps // nout + 1
    Dser = np.zeros((n, 3, nt)); tser = np.zeros(nt); umax = np.zeros(n); maxdisp = np.zeros(n)
    ar = np.arange(N); fx = [None] * n; fxr = [None] * n; fxc = [[None, None, None] for _ in range(n)]   # A4: crossing onset

    def record(k, rr):
        o = st["order"]
        tnow = k * nout * dt
        for i in np.where(st["perm"])[0]:
            disp = np.where(o[i] != ar)[0]
            if disp.size == 0:
                continue
            rdx = rr[i, o[i][disp]]
            if fx[i] is None:
                fx[i] = tnow / MYR; fxr[i] = [float(rdx.min() / KPC), float(rdx.max() / KPC)]
            for ci in range(3):
                if fxc[i][ci] is None and (np.abs(np.log(rdx / S_.cells[ci])) <= math.log(1.25)).any():
                    fxc[i][ci] = tnow / MYR
        for i in range(n):
            if mond[i]:
                uc = ulaw(gNc[i], a0r[i, 0])
            else:
                rs = rr[i, o[i]]; mus = core[i] + np.cumsum(m[i, o[i]])
                uc = G * np.interp(S_.cells, rs, mus, left=core[i]) / S_.cells ** 2
            Dser[i, :, k] = np.log10((gNc[i] + uc) / glaw(gNc[i], a0r[i, 0]))
        tser[k] = k * nout * dt

    y = [r, v]; record(0, r)
    if integrate.any():
        for s in range(1, nsteps + 1):
            y = rk4(deriv, y, dt)
            if s % nout == 0:
                k = s // nout; record(k, y[0])
                mu = get_mu(y[0]); umax = np.maximum(umax, (G * mu / y[0] ** 2 / a0r).max(axis=1))
                if k % 500 == 0:
                    guard(f"run_BF {label}")
                    if not np.all(np.isfinite(y[0])):
                        P(f"  NON-FINITE state in {label} at t = {tser[k]/MYR:.1f} Myr"); break
        maxdisp = np.abs(np.log(y[0] / rm[None, :])).max(axis=1)
    else:
        for k in range(1, nt):
            tser[k] = k * nout * dt; Dser[:, :, k] = Dser[:, :, 0]
    info = {"N": int(N), "dt_Myr": dt / MYR, "Tmax_Myr": Tmax / MYR, "dtout_Myr": nout * dt / MYR, "nsteps": int(nsteps),
            "resorts": st["resorts"].tolist(), "perm_end": st["perm"].tolist(), "umax_over_a0": umax.tolist(),
            "max_|ln r/r0|": maxdisp.tolist(), "first_cross_Myr": fx, "first_cross_r_kpc": fxr, "first_cross_near_cell_Myr": fxc}
    return tser, Dser, td_rows, info


drift_sign_run = 1.0


def lag_times(t, D):
    """t_50: first F >= 0.5; t_90: earliest t with |1 - F| <= 0.1 for every later sample (None = censored, > T_max)."""
    D0 = D[0]
    if abs(D0) < 1e-12:
        return 0.0, 0.0, D0
    F = 1.0 - D / D0
    i50 = np.where(F >= 0.5)[0]; t50 = float(t[i50[0]]) if i50.size else None
    badi = np.where(np.abs(1.0 - F) > 0.1)[0]
    if badi.size == 0:
        t90 = 0.0
    elif badi[-1] + 1 < t.size:
        t90 = float(t[badi[-1] + 1])
    else:
        t90 = None
    return t50, t90, D0


def above_runs(t, x, line):
    """longest contiguous stretch (t_last - t_first) with x >= line, and total time above.
    A2 (reporting only): the start time of the longest stretch is kept in LAST_START."""
    global LAST_START
    LAST_START = None
    ab = x >= line
    if not ab.any():
        return 0.0, 0.0
    best = -1.0; start = None
    for k in range(t.size):
        if ab[k] and start is None:
            start = k
        if (not ab[k] or k == t.size - 1) and start is not None:
            end = k if ab[k] else k - 1
            if t[end] - t[start] > best:
                best = t[end] - t[start]; LAST_START = float(t[start])
            start = None
    dtot = float(ab.sum()) * (t[1] - t[0])
    return float(best), dtot


LAST_START = None


TFAC = 6.0 if SMOKE else 60.0
if MUT:
    READ_USED = [(rd, 0.0, 0.0, True) for rd, _, _ in READINGS]        # MU1: every framework reading -> MOND-I
else:
    READ_USED = [(rd, cin, alp, False) for rd, cin, alp in READINGS]

BF = {}
P(f"\n(b) B-F SHELL RUNS (baryons frozen after the blowout; N_c = 2000 medium markers; T_max = {TFAC:.0f} t_dyn(5Rd))"
  + ("  [MU1: all readings replaced by MOND-I]" if MUT else ""))
for nm in ("DDO154", "NGC3198"):
    S_ = SYS[nm]
    rows = [{"reading": rd, "foot": ft, "f": f, "cin": cin, "alpha": alp, "mond": mo}
            for rd, cin, alp, mo in READ_USED for ft in FOOTS for f in FRACS]
    t1 = time.time()
    tser, Dser, tdr, info = run_BF(S_, rows, Tfac=TFAC, label=nm)
    P(f"  {nm}: {len(rows)} rows, N = {info['N']}, dt = {info['dt_Myr']:.4f} Myr, T_max = {info['Tmax_Myr']:.0f} Myr, "
      f"{info['nsteps']} steps, wall {time.time()-t1:.0f} s; max u/a0 {max(info['umax_over_a0']):.3f}; "
      f"rows with shell crossing at end {sum(info['perm_end'])}/{len(rows)}")
    BF[nm] = (rows, tser, Dser, tdr, info)
    RES.setdefault("runs", {})[nm] = {"rows": [f"{q['reading']}|{q['foot']}|{q['f']}" for q in rows], "info": info}
    guard(nm)
    dump()

# ------------------------------------------------------------------------------------------------ cell table + K1b
P("\nCELL RESULTS (B-F). D in dex of g; D_V = D/2 in dex of V_c; times in Myr and in t_dyn(r); '>' = censored at T_max")
cellres = []
k1b_max = 0.0
for nm, (rows, tser, Dser, tdr, info) in BF.items():
    for i, q in enumerate(rows):
        for ci, cn in enumerate(CELLS):
            D = Dser[i, ci]
            if q["f"] == 0.0:
                k1b_max = max(k1b_max, float(np.abs(D).max())); continue
            t50, t90, D0 = lag_times(tser, D)
            tdyn = tdr[i, ci]
            lon05, tot05 = above_runs(tser, np.abs(D) / 2, 0.05); st05 = LAST_START
            lon02, tot02 = above_runs(tser, np.abs(D) / 2, 0.02)
            late = float(np.abs(D[int(0.9 * D.size):]).max() / 2)
            rec = {"system": nm, "reading": q["reading"], "foot": q["foot"], "f": q["f"], "cell": cn,
                   "r_kpc": float(SYS[nm].cells[ci] / KPC), "t_dyn_Myr": tdyn / MYR, "DV0": D0 / 2,
                   "t50_Myr": None if t50 is None else t50 / MYR, "t90_Myr": None if t90 is None else t90 / MYR,
                   "t50_tdyn": None if t50 is None else t50 / tdyn, "t90_tdyn": None if t90 is None else t90 / tdyn,
                   "Tmax_tdyn": tser[-1] / tdyn, "peak_absDV": float(np.abs(D).max() / 2),
                   "min_DV": float(D.min() / 2), "longest_DV>=0.05_Myr": lon05 / MYR, "longest_DV>=0.02_Myr": lon02 / MYR,
                   "longest05_start_Myr": None if st05 is None else st05 / MYR, "late_max_absDV(last10%)": late,
                   "first_cross_any_Myr": info["first_cross_Myr"][i], "first_cross_near_cell_Myr": info["first_cross_near_cell_Myr"][i][ci]}
            cellres.append(rec)
k1b = True
if not MUT:
    k1b = chk("K1b_unperturbed_stationary", k1b_max <= 1e-8, f"max |D| over T_max, f = 0 rows, all readings, 3 radii = {k1b_max:.1e} dex (line 1e-8)")


def fmt(x, d=2):
    return ">Tmax" if x is None else f"{x:.{d}f}"


for rec in cellres:
    if rec["cell"] in LAGCELLS or True:
        P(f"  {rec['system']:7s} {rec['reading']:11s} {rec['foot']:9s} f={rec['f']:.1f} {rec['cell']:3s} "
          f"r={rec['r_kpc']:6.2f} t_dyn={rec['t_dyn_Myr']:6.1f}  D_V(0+)={rec['DV0']:+.4f}  "
          f"t50={fmt(rec['t50_Myr'],1):>7s} Myr ({fmt(rec['t50_tdyn'])} t_dyn)  t90={fmt(rec['t90_Myr'],1):>7s} Myr "
          f"({fmt(rec['t90_tdyn'])} t_dyn)  peak|D_V|={rec['peak_absDV']:.4f} min D_V={rec['min_DV']:+.4f} "
          f"longest>=0.05: {rec['longest_DV>=0.05_Myr']:.0f} Myr (from {fmt(rec['longest05_start_Myr'],0)}); late |D_V| {rec['late_max_absDV(last10%)']:.4f}; "
          f"crossing near cell from {fmt(rec['first_cross_near_cell_Myr'],0)} Myr")
RES["cell_results"] = cellres

# ------------------------------------------------------------------------------------------------ V1 lag class
P("\nV1 LAG CLASS (cells: 2 systems x 2 footings x {2Rd, 5Rd} x f {0.2, 0.5}; L = t90 in t_dyn)")
V1 = {}
for rd, _, _, _ in READ_USED:
    Ls = []; t50s = []
    for rec in cellres:
        if rec["reading"] == rd and rec["cell"] in LAGCELLS:
            L = rec["t90_tdyn"] if rec["t90_tdyn"] is not None else float("inf")
            Ls.append(L); t50s.append(rec["t50_tdyn"] if rec["t50_tdyn"] is not None else float("inf"))
    if all(L <= 1 for L in Ls):
        cl = "INSTANT"
    elif all(L >= 2 for L in Ls):
        cl = "FLOW-LIMITED LAG"
    elif all(1 < L < 2 for L in Ls):
        cl = "SHORT LAG"
    else:
        cl = "MIXED"
    V1[rd] = {"class": cl, "n": len(Ls), "L_min": min(Ls), "L_max": max(Ls), "t50_min": min(t50s), "t50_max": max(t50s)}
    P(f"  {rd:11s}: {cl:16s} L in [{min(Ls):.2f}, {max(Ls):.2f}] t_dyn; t50 in [{min(t50s):.2f}, {max(t50s):.2f}] t_dyn  (n = {len(Ls)})")
cls = set(v["class"] for v in V1.values())
overall = cls.pop() if len(cls) == 1 else "READING-DEPENDENT"
P(f"  OVERALL (mass part): {overall}")
# field part: r/c vs t_dyn
fp_ratio = max(float(S_.cells[ci] / C_SI / S_.tdyn(ft, np.array([S_.cells[ci]]))[0]) for S_ in SYS.values() for ft in FOOTS for ci in range(2))
fp_class = "INSTANT" if fp_ratio <= 1e-3 else "NOT INSTANT"
P(f"  FIELD PART (Phi re-forms at c; chi has no baryon source): max (r/c)/t_dyn = {fp_ratio:.2e} -> {fp_class}")
for rd in V1:
    after = [rec for rec in cellres if rec["reading"] == rd and rec["cell"] in LAGCELLS and rec["first_cross_near_cell_Myr"] is not None
             and (rec["t90_Myr"] is None or rec["t90_Myr"] > rec["first_cross_near_cell_Myr"])]
    V1[rd]["cells_t90_after_crossing"] = len(after)
    P(f"  {rd:11s}: cells whose t90 lies after shell crossing near the cell (single-stream EFT ended; report only): {len(after)}/16")
lag_detected = all(v["t50_min"] > 0 for v in V1.values())
chk("LAG_DETECTED_in_every_reading", lag_detected, "t_50 > 0 in every reading cell (result check; MU1's tooth)")
RES["classes"]["V1"] = {"per_reading": V1, "overall_mass_part": overall, "field_part": fp_class, "field_part_max_r_over_c_tdyn": fp_ratio}

# ------------------------------------------------------------------------------------------------ V2 CFG763/764
P("\nV2 RELATION TO CFG763 / CFG764 (tau_resp = t50/ln 2)")
V2 = {}
for rd, _, _, _ in READ_USED:
    c764 = []; c763 = []; vals = []
    for rec in cellres:
        if rec["reading"] != rd or rec["cell"] not in LAGCELLS:
            continue
        if rec["t50_Myr"] is None:
            tr = float("inf")
        else:
            tr = rec["t50_Myr"] / math.log(2)
        korb = tr / (2 * math.pi * rec["t_dyn_Myr"])
        kmin, kmax = K764[rec["foot"]]; tmin, tmax = T763[rec["foot"]]
        c764.append("CONSISTENT" if kmin <= korb <= kmax else ("FASTER" if korb < kmin else "SLOWER"))
        c763.append("CONSISTENT" if tmin <= tr / 1e3 <= tmax else ("FASTER" if tr / 1e3 < tmin else "SLOWER"))
        vals.append((korb, tr / 1e3)); rec["tau_resp_Myr"] = tr; rec["tau_resp_over_torb"] = korb

    def agg(lst):
        if all(x == "CONSISTENT" for x in lst):
            return "CONSISTENT"
        if all(x == "FASTER" for x in lst):
            return "INCONSISTENT-FASTER"
        if all(x == "SLOWER" for x in lst):
            return "INCONSISTENT-SLOWER"
        return f"PARTLY CONSISTENT ({sum(x == 'CONSISTENT' for x in lst)}/{len(lst)})"
    a764, a763 = agg(c764), agg(c763)
    txt764 = "DIFFERENT PHYSICS" if a764 == "INCONSISTENT-FASTER" else ("SAME CLOCK POSSIBLE" if a764 == "CONSISTENT" else "-")
    txt763 = "DIFFERENT PHYSICS" if a763 == "INCONSISTENT-FASTER" else ("SAME CLOCK POSSIBLE" if a763 == "CONSISTENT" else "-")
    ks = [v[0] for v in vals]; gs_ = [v[1] for v in vals]
    V2[rd] = {"CFG764": a764, "CFG764_text": txt764, "CFG763": a763, "CFG763_text": txt763,
              "tau_over_torb_range": [min(ks), max(ks)], "tau_Gyr_range": [min(gs_), max(gs_)]}
    P(f"  {rd:11s}: CFG764 {a764:22s} ({txt764}); tau/t_orb in [{min(ks):.3f}, {max(ks):.3f}] vs [0.457/0.525, 1.196]")
    P(f"  {'':11s}  CFG763 {a763:22s} ({txt763}); tau in [{min(gs_):.4f}, {max(gs_):.4f}] Gyr vs [0.724/0.832, 3.474]")
RES["classes"]["V2"] = V2

# ------------------------------------------------------------------------------------------------ V3 observability
P("\nV3 OBSERVABILITY (|D_V| >= 0.05 dex continuously >= 100 Myr; cells incl. R_HI)")
V3 = {}
for rd, _, _, _ in READ_USED:
    hits = [rec for rec in cellres if rec["reading"] == rd and rec["longest_DV>=0.05_Myr"] >= 100.0]
    best = max((rec for rec in cellres if rec["reading"] == rd), key=lambda x: x["peak_absDV"])
    V3[rd] = {"class": "OBSERVABLE" if hits else "NOT OBSERVABLE", "n_hits": len(hits),
              "hits": [(h["system"], h["foot"], h["f"], h["cell"], h["longest_DV>=0.05_Myr"]) for h in hits],
              "largest_peak": (best["system"], best["foot"], best["f"], best["cell"], best["peak_absDV"], best["longest_DV>=0.05_Myr"],
                               best["longest_DV>=0.02_Myr"])}
    P(f"  {rd:11s}: {V3[rd]['class']:15s} largest peak |D_V| {best['peak_absDV']:.4f} dex ({best['system']} {best['foot']} f={best['f']} "
      f"{best['cell']}); longest >= 0.05: {best['longest_DV>=0.05_Myr']:.0f} Myr; >= 0.02: {best['longest_DV>=0.02_Myr']:.0f} Myr")
for rd in V3:
    for h in [rec for rec in cellres if rec["reading"] == rd and rec["longest_DV>=0.05_Myr"] >= 100.0]:
        fxn = h["first_cross_near_cell_Myr"]; st_ = h["longest05_start_Myr"]
        where = ("inside the single-stream regime" if (fxn is None or st_ + h["longest_DV>=0.05_Myr"] < fxn) else
                 ("after shell crossing near the cell (beyond CFG938 condition 5)" if st_ >= fxn else "straddles the onset of shell crossing near the cell"))
        P(f"    hit {h['system']} {h['foot']} f={h['f']} {h['cell']}: stretch {st_:.0f}-{st_ + h['longest_DV>=0.05_Myr']:.0f} Myr "
          f"(min D_V {h['min_DV']:+.4f}); crossing near cell from {fmt(fxn,0)} Myr -> {where}")
        V3[rd].setdefault("single_stream", []).append({"cell": f"{h['system']}|{h['foot']}|{h['f']}|{h['cell']}", "stretch_start_Myr": st_,
                                                       "first_cross_near_cell_Myr": fxn, "reading": where})
c3 = set(v["class"] for v in V3.values())
v3all = ("OBSERVABLE (ALL READINGS)" if c3 == {"OBSERVABLE"} else "NOT OBSERVABLE" if c3 == {"NOT OBSERVABLE"}
         else "OBSERVABLE (SOME READINGS: " + ", ".join(k for k, v in V3.items() if v["class"] == "OBSERVABLE") + ")")
P(f"  OVERALL: {v3all}")
RES["classes"]["V3"] = {"per_reading": V3, "overall": v3all}
dump()

# ================================================================================================ MUTATE exit
if MUT:
    P("\nMUTATE TEETH")
    mu1 = (not lag_detected) and all(v["class"] == "INSTANT" for v in V1.values())
    mu2 = not k1a
    mu3 = not k3_md
    P(f"  MU1 (medium removed -> MOND-I): lag check FAILS and every class INSTANT: {mu1}")
    P(f"  MU2 (deep tether R = u^2/a0): K1a FAILS: {mu2}")
    P(f"  MU3 (drift sign flipped): K3 M-D clock FAILS: {mu3}")
    RES["mutate_teeth"] = {"MU1": mu1, "MU2": mu2, "MU3": mu3}
    allbite = mu1 and mu2 and mu3
    P(f"  {'ALL TEETH BITE' if allbite else 'A TOOTH DID NOT BITE'}")
    dump(); sys.exit(1 if allbite else 3)

# ================================================================================================ K4 convergence
P("\nK4 CONVERGENCE (NGC 3198 canonical, f = 0.5, M-I and M-ID(0.5); one change at a time)")
S_ = SYS["NGC3198"]
k4rows = [{"reading": "M-I", "foot": "canonical", "f": 0.5, "cin": 1.0, "alpha": 0.0, "mond": False},
          {"reading": "M-ID(0.5)", "foot": "canonical", "f": 0.5, "cin": 1.0, "alpha": 0.5, "mond": False}]
base = {}
for rec in cellres:
    if rec["system"] == "NGC3198" and rec["foot"] == "canonical" and rec["f"] == 0.5 and rec["reading"] in ("M-I", "M-ID(0.5)") and rec["cell"] in LAGCELLS:
        base[(rec["reading"], rec["cell"])] = (rec["t50_Myr"], rec["t90_Myr"])
dtout_base = BF["NGC3198"][4]["dtout_Myr"]
k4 = True; K4res = {}
for vname, kw in (("Nc_x2", {"Nc": 4000}), ("dt_half", {"dt_fac": 0.5}), ("inner_half", {"rin_fac": 0.5}), ("outer_x2", {"rout_fac": 2.0})):
    if elapsed() > WALL_CAP - 600:
        P(f"  WALL CAP: K4 variant {vname} not run"); k4 = False; continue
    t1 = time.time()
    tser, Dser, tdr, info = run_BF(S_, k4rows, Tfac=TFAC, label=f"K4 {vname}", **kw)
    for i, q in enumerate(k4rows):
        for ci, cn in enumerate(LAGCELLS):
            t50, t90, _ = lag_times(tser, Dser[i, ci])
            b50, b90 = base[(q["reading"], cn)]
            res_ = []
            for new, old in ((t50, b50), (t90, b90)):
                new = None if new is None else new / MYR
                if new is None and old is None:
                    res_.append(True)
                elif new is None or old is None:
                    res_.append(False)
                else:
                    res_.append(abs(new - old) <= max(0.05 * abs(old), dtout_base + 1e-9))
            ok = all(res_); k4 &= ok
            K4res[f"{vname}:{q['reading']}:{cn}"] = {"t50": None if t50 is None else t50 / MYR, "t90": None if t90 is None else t90 / MYR,
                                                    "base": [b50, b90], "ok": ok}
            P(f"  {vname:10s} {q['reading']:10s} {cn}: t50 {fmt(None if t50 is None else t50/MYR,1)} (base {fmt(b50,1)}), "
              f"t90 {fmt(None if t90 is None else t90/MYR,1)} (base {fmt(b90,1)}) Myr  {'ok' if ok else 'DIFFERS'}  [{time.time()-t1:.0f} s]")
    guard("K4"); dump()
RES["K4"] = K4res
# frozen K4 consequence (criteria section 6): a reading whose K4 rerun differs is reported as UNRESOLVED
unres = sorted(set(k_.split(":")[1] for k_, v_ in K4res.items() if not v_["ok"]))
V1k = {rd: (dict(v_, **{"class": "UNRESOLVED", "class_before_K4": v_["class"]}) if rd in unres else dict(v_)) for rd, v_ in V1.items()}
clk = set(v_["class"] for v_ in V1k.values()); overall_k = clk.pop() if len(clk) == 1 else "READING-DEPENDENT"
P(f"  K4 frozen consequence: UNRESOLVED readings = {unres or 'none'}; V1 after K4: " + "; ".join(f"{k_} {v_['class']}" for k_, v_ in V1k.items())
  + f"; OVERALL {overall_k}")
RES["classes"]["V1_after_K4"] = {"per_reading": V1k, "overall_mass_part": overall_k, "unresolved": unres}
overall = overall_k; V1 = V1k
k4 = chk("K4_convergence", k4, "t50 and uncensored t90 within 5% or one output interval under N_c x2, dt/2, inner/2, outer x2")

# ---- Amendment A1 (post hoc, report only): fragility probe of V3's nearest-to-line cell (DDO 154 R_HI, M-I, f = 0.5)
P("\nA1 FRAGILITY PROBE (report only; DDO 154 R_HI, M-I, f = 0.5; longest stretch with |D_V| >= 0.05 dex)")
a1rows = [{"reading": "M-I", "foot": ft, "f": 0.5, "cin": 1.0, "alpha": 0.0, "mond": False} for ft in FOOTS]
A1res = {}
for rec in cellres:
    if rec["system"] == "DDO154" and rec["reading"] == "M-I" and rec["f"] == 0.5 and rec["cell"] == "RHI":
        A1res[f"primary:{rec['foot']}"] = rec["longest_DV>=0.05_Myr"]; A1res[f"primary:{rec['foot']}:start_Myr"] = rec["longest05_start_Myr"]
for vname, kw in (("Nc_x2", {"Nc": 4000}), ("dt_half", {"dt_fac": 0.5}), ("outer_x2", {"rout_fac": 2.0}), ("inner_half", {"rin_fac": 0.5})):
    tser, Dser, tdr, info = run_BF(SYS["DDO154"], a1rows, Tfac=TFAC, label=f"A1 {vname}", **kw)   # A2: full T_max (first run used 10)
    for i, q in enumerate(a1rows):
        lon, _ = above_runs(tser, np.abs(Dser[i, 2]) / 2, 0.05)
        A1res[f"{vname}:{q['foot']}"] = lon / MYR; A1res[f"{vname}:{q['foot']}:start_Myr"] = LAST_START / MYR if LAST_START else None
for k_, v_ in A1res.items():
    if not k_.endswith("start_Myr"):
        P(f"  {k_:20s} longest >= 0.05 dex: {v_:.1f} Myr (from {fmt(A1res.get(k_ + ':start_Myr'), 0)} Myr)")
a1_vals = [v_ for k_, v_ in A1res.items() if not k_.endswith("start_Myr") and not k_.startswith("primary")]
prim_side = max(A1res[f"primary:{ft}"] for ft in FOOTS) >= 100.0          # side of the 100 Myr line the primary is on
a1_fragile = any((v_ >= 100.0) != prim_side for v_ in a1_vals)
P(f"  V3 {'FRAGILE (a probe lands on the other side of the 100 Myr line)' if a1_fragile else 'every probe on the same side of the 100 Myr line as the primary'}")
RES["report_only"]["A1_fragility_probe"] = {"longest_Myr": A1res, "fragile": a1_fragile}
dump()

# ================================================================================================ report-only extras
P("\nREPORT ONLY (no class weight)")
ro = {}
# f* for D_V(0+) = 0.05 at DDO 154's R_HI
S_ = SYS["DDO154"]
for foot in FOOTS:
    a0 = A0[foot]; rc = S_.RHI
    gN0 = float(S_.gN(0.0, np.array([rc]))[0]); qg = float(S_.lk1(S_.Mg, np.array([rc]))[0] / S_.lk1(S_.tab[(0.0, foot)]["Mb"], np.array([rc]))[0])
    uold = float(ulaw(gN0, a0))
    DV = lambda f: 0.5 * math.log10((gN0 * (1 - f * qg) + uold) / float(glaw(gN0 * (1 - f * qg), a0)))
    fstar = brentq(lambda f: DV(f) - 0.05, 1e-6, 1.0) if DV(1.0) > 0.05 else None
    ro[f"fstar_DDO154_RHI_{foot}"] = {"f_star": fstar, "DV0_f1": DV(1.0), "gas_share": qg}
    P(f"  DDO 154 R_HI {foot}: D_V(0+) reaches 0.05 dex at gas fraction removed f* = {fmt(fstar,3)} (D_V(0+) at f = 1: {DV(1.0):.4f}; gas share {qg:.3f})")
# gradual-loss suppression using the M-D(0.5) half-time at DDO 154 R_HI, f = 0.5
for rec in cellres:
    if rec["system"] == "DDO154" and rec["reading"] == "M-D(0.5)" and rec["cell"] == "RHI" and rec["f"] == 0.5 and rec["t50_Myr"]:
        Gm_ = math.log(2) / rec["t50_Myr"]
        sup = {f"T_loss={k} t_dyn": (1 - math.exp(-Gm_ * k * rec["t_dyn_Myr"])) / (Gm_ * k * rec["t_dyn_Myr"]) for k in (1, 3, 10)}
        ro[f"gradual_suppression_DDO154_RHI_{rec['foot']}"] = sup
        P(f"  gradual loss, DDO 154 R_HI {rec['foot']} (M-D(0.5) clock t50 {rec['t50_Myr']:.0f} Myr): peak residual x " +
          ", ".join(f"{k}: {v:.3f}" for k, v in sup.items()))
# field share of the extra pull: tether-stress slip s = 4 pi G r |p_r|/(c^2 g), p_r = -W_full(u)
for nm, S_ in SYS.items():
    for foot in FOOTS:
        a0 = A0[foot]; gN0 = S_.gN(0.0, S_.cells); uu = ulaw(gN0, a0)
        W = (-a0 * uu - a0 ** 2 * np.log1p(-uu / a0)) / (4 * np.pi * G)
        sl = 4 * np.pi * G * S_.cells * np.abs(W) / (C_SI ** 2 * glaw(gN0, a0))
        stiff = {Ls: (2 * np.pi * G * (Ls * PC) ** 2 * S_.lk1(S_.tab[(0.0, foot)]["rho_ph"], S_.cells) / S_.cells ** 2) for Ls in (24.0, 1000.0)}
        Rp_ = uu * (2 * a0 - uu) / (a0 - uu) ** 2; hh = 1e-7 * S_.cells
        dg = (S_.gN(0.0, S_.cells + hh) - S_.gN(0.0, S_.cells - hh)) / (2 * hh); w2c = 2 * uu * Rp_ / S_.cells + dg
        ro[f"field_share_{nm}_{foot}"] = {"slip_s": sl.tolist(), "stiff_over_tether_L24pc": (stiff[24.0] / w2c).tolist(),
                                         "stiff_over_tether_L1kpc": (stiff[1000.0] / w2c).tolist(),
                                         "r_over_c_Myr": (S_.cells / C_SI / MYR).tolist()}
        P(f"  {nm} {foot}: tether-stress (field) share of the pull s = {', '.join(f'{x:.1e}' for x in sl)}; stiffness/tether in "
          f"omega^2: L*=24 pc {', '.join(f'{x:.1e}' for x in stiff[24.0]/w2c)}, 1 kpc {', '.join(f'{x:.1e}' for x in stiff[1000.0]/w2c)}; "
          f"r/c = {', '.join(f'{x*1e3:.1f}' for x in S_.cells/C_SI/MYR)} kyr")
P(f"  Israel-Stewart pressure clock (kinetic reading only; the cold parent has p = 0, so it does not enter): tau_pi/t_dyn = 1/(2 alpha)"
  f" = {1/(2*ALPHAS[0]):.2f} (alpha 0.5), {1/(2*ALPHAS[1]):.2f} (alpha 1.186) for an SIS (CFG638 K7)")
RES["report_only"].update(ro)
dump()

# ================================================================================================ B-L variant (report only)
P("\nB-L VARIANT (report only): baryons as cold rotating shells, N_b = 2000; readings M-I, M-ID(0.5), MOND-I")


def run_BL(S_, rows, Nc=2000, Nb=2000, Tfac=60.0, label=""):
    n = len(rows)
    a0r = np.array([A0[q["foot"]] for q in rows])[:, None]
    cin = np.array([q["cin"] for q in rows], float)[:, None]; cdr = np.array([q["alpha"] for q in rows], float)[:, None]
    mond = np.array([q["mond"] for q in rows], bool)[:, None]
    rin, rout = 0.02 * S_.Rd, 50 * S_.Rd
    rm = np.unique(np.concatenate([np.exp(np.linspace(math.log(rin), math.log(rout), Nc + 1))[1:], S_.cells])); N = rm.size
    lb = np.linspace(math.log(rin), math.log(rout), Nb + 1); rb0 = np.exp(0.5 * (lb[1:] + lb[:-1]))   # midpoints: no ties
    keys_t = sorted(set((q["f"], q["foot"]) for q in rows)); TAU = np.vstack([S_.tab[k]["tau"] for k in keys_t])
    tidT = np.array([keys_t.index((q["f"], q["foot"])) for q in rows])[:, None]
    # baryon marker masses (monotone tables), before and after the blowout
    Mb_old = S_.lk1(S_.tab[(0.0, "canonical")]["Mb"], rb0); coreb_old = float(S_.lk1(S_.tab[(0.0, "canonical")]["Mb"], np.array([rin]))[0])
    mb_old = np.diff(np.concatenate([[coreb_old], Mb_old]))
    mb = np.zeros((n, Nb)); coreb = np.zeros(n); nviol = 0
    for i, q in enumerate(rows):
        Mn = S_.lk1(S_.tab[(q["f"], "canonical")]["Mb"], rb0); cn_ = float(S_.lk1(S_.tab[(q["f"], "canonical")]["Mb"], np.array([rin]))[0])
        mb[i] = np.diff(np.concatenate([[cn_], Mn])); coreb[i] = cn_
        nviol += int((mb[i] > mb_old * (1 + 1e-12)).sum())
    allr0 = np.concatenate([rm, rb0]); o0 = np.argsort(allr0, kind="stable")
    isb = np.concatenate([np.zeros(N, bool), np.ones(Nb, bool)])
    # t = 0-: exact discrete equilibrium with the ORIGINAL baryon masses
    cumb = coreb_old + np.cumsum(np.where(isb[o0], np.concatenate([np.zeros(N), mb_old])[o0], 0.0))
    Mbenc = np.empty(N + Nb); Mbenc[o0] = cumb
    gNm = G * Mbenc[:N] / rm ** 2
    mu0 = rm[None, :] ** 2 * ulaw(gNm[None, :], a0r) / G
    core = rin ** 2 * ulaw(G * coreb_old / rin ** 2, a0r[:, 0]) / G
    m = np.diff(np.concatenate([core[:, None], mu0], axis=1), axis=1)
    mu0 = core[:, None] + np.cumsum(m, axis=1)
    cumc = core[:, None] + np.cumsum(np.where(~isb[o0], np.concatenate([m, np.zeros((n, Nb))], axis=1)[:, o0], 0.0), axis=1)
    Mcenc = np.empty((n, N + Nb)); Mcenc[:, o0] = cumc
    gNb0 = G * Mbenc[N:] / rb0 ** 2; ub0 = G * Mcenc[:, N:] / rb0 ** 2
    gtot0 = np.where(mond, glaw(gNb0[None, :], a0r), gNb0[None, :] + ub0)
    j2 = rb0[None, :] ** 3 * gtot0
    tdmin = min(float(S_.tdyn(ft, rm).min()) for ft in FOOTS); dt = 0.02 * tdmin
    Tmax = Tfac * max(float(S_.tdyn(ft, np.array([S_.cells[1]]))[0]) for ft in FOOTS)
    dtout = 0.02 * min(float(S_.tdyn(ft, np.array([S_.cells[0]]))[0]) for ft in FOOTS)
    nout = max(1, int(round(dtout / dt))); nsteps = int(math.ceil(Tmax / dt / nout)) * nout
    mall = np.concatenate([m, np.zeros((n, Nb))], axis=1); ball = np.concatenate([np.zeros((n, N)), mb], axis=1)
    order = np.repeat(o0[None, :], n, axis=0)
    medium_moves = (~mond[:, 0]) & ((cin[:, 0] > 0) | (cdr[:, 0] > 0))

    def enclosed(allr):
        rs = np.take_along_axis(allr, order, 1); bad = (np.diff(rs, axis=1) < 0).any(axis=1)
        if bad.any():
            ib = np.where(bad)[0]
            sub = np.argsort(np.take_along_axis(allr[ib], order[ib], 1), axis=1, kind="stable")
            order[ib] = np.take_along_axis(order[ib], sub, 1)
        cc = core[:, None] + np.cumsum(np.take_along_axis(mall, order, 1), axis=1)
        cb = coreb[:, None] + np.cumsum(np.take_along_axis(ball, order, 1), axis=1)
        Mc_ = np.empty_like(cc); Mb_ = np.empty_like(cb)
        np.put_along_axis(Mc_, order, cc, 1); np.put_along_axis(Mb_, order, cb, 1)
        return Mc_, Mb_

    def deriv(y):
        rr, vv, rb, vb = y
        Mc_, Mb_ = enclosed(np.concatenate([rr, rb], axis=1))
        u = G * Mc_[:, :N] / rr ** 2; gN = G * Mb_[:, :N] / rr ** 2
        drr = cin * vv + cdr * S_lk(TAU, tidT, rr) * (u - ulaw(gN, a0r))
        dvv = cin * (Rfun(u, a0r) - gN)
        gNb = G * Mb_[:, N:] / rb ** 2; ub = G * Mc_[:, N:] / rb ** 2
        gt = np.where(mond, glaw(gNb, a0r), gNb + ub)
        mm = medium_moves[:, None]
        return [drr * mm, dvv * mm, vb, j2 / rb ** 3 - gt]

    def S_lk(T, tid, rr):
        x = (np.log(rr) - S_.LG0) * S_.IDL
        i = x.astype(np.int64); np.clip(i, 0, NG - 2, out=i); w = x - i; np.clip(w, 0.0, 1.0, out=w)
        t0 = T[tid, i]; return t0 + w * (T[tid, i + 1] - t0)

    nt = nsteps // nout + 1; Dser = np.zeros((n, 3, nt)); Vser = np.zeros((n, 3, nt)); tser = np.zeros(nt)

    def record(k, y):
        rr, _, rb, _ = y
        for i in range(n):
            ob = np.argsort(rb[i]); cbb = coreb[i] + np.cumsum(mb[i, ob])
            idx = np.searchsorted(rb[i, ob], S_.cells, side="right")
            Mb_c = np.where(idx > 0, cbb[np.maximum(idx - 1, 0)], coreb[i])          # inclusive step function (as the forces)
            gNc = G * Mb_c / S_.cells ** 2
            if mond[i, 0]:
                g = glaw(gNc, a0r[i, 0])
            else:
                oc = np.argsort(rr[i]); ccc = core[i] + np.cumsum(m[i, oc])
                uc = G * np.interp(S_.cells, rr[i, oc], ccc, left=core[i]) / S_.cells ** 2; g = gNc + uc
            Dser[i, :, k] = np.log10(g / glaw(gNc, a0r[i, 0])); Vser[i, :, k] = np.sqrt(S_.cells * g)
        tser[k] = k * nout * dt

    y = [np.repeat(rm[None, :], n, axis=0), np.zeros((n, N)), np.repeat(rb0[None, :], n, axis=0), np.zeros((n, Nb))]
    record(0, y)
    for s in range(1, nsteps + 1):
        y = rk4(deriv, y, dt)
        if s % nout == 0:
            record(s // nout, y)
            if (s // nout) % 500 == 0:
                guard(f"run_BL {label}")
                if elapsed() > WALL_CAP - 120:
                    P(f"  WALL CAP inside B-L {label} at t = {tser[s//nout]/MYR:.0f} Myr: truncated"); tser = tser[:s // nout + 1]
                    Dser = Dser[:, :, :s // nout + 1]; Vser = Vser[:, :, :s // nout + 1]; break
    return tser, Dser, Vser, {"N": N, "Nb": Nb, "dt_Myr": dt / MYR, "Tmax_Myr": Tmax / MYR, "nsteps": nsteps, "mass_increase_violations": nviol}


BL = {}
blres = []
for nm in ("DDO154", "NGC3198"):
    S_ = SYS[nm]
    rows = [{"reading": rd, "foot": ft, "f": f, "cin": cin, "alpha": alp, "mond": mo}
            for rd, cin, alp, mo in (("M-I", 1.0, 0.0, False), ("M-ID(0.5)", 1.0, 0.5, False), ("MOND-I", 0.0, 0.0, True))
            for ft in FOOTS for f in FRACS]
    est = BF[nm][4]["nsteps"] * 0.0                                    # placeholder; timing printed after the run
    if elapsed() > WALL_CAP - 300:
        P(f"  WALL CAP: B-L {nm} not run"); continue
    t1 = time.time()
    tser, Dser, Vser, info = run_BL(S_, rows, Tfac=TFAC, label=nm)
    P(f"  {nm}: {len(rows)} rows, {info['nsteps']} steps, wall {time.time()-t1:.0f} s; marker-mass increases after blowout: {info['mass_increase_violations']}")
    for i, q in enumerate(rows):
        for ci, cn in enumerate(CELLS):
            D = Dser[i, ci]
            if q["f"] == 0.0:
                blres.append({"system": nm, "reading": q["reading"], "foot": q["foot"], "f": 0.0, "cell": cn, "max_absD": float(np.abs(D).max())})
                continue
            t50, t90, D0 = lag_times(tser, D)
            td = float(S_.tdyn(q["foot"], np.array([S_.cells[ci]]))[0])
            lon05, _ = above_runs(tser, np.abs(D) / 2, 0.05)
            dV0 = math.log10(Vser[i, ci, 1] / Vser[i, ci, 0]) if Vser.shape[2] > 1 else float("nan")
            blres.append({"system": nm, "reading": q["reading"], "foot": q["foot"], "f": q["f"], "cell": cn, "DV0": D0 / 2,
                          "t50_tdyn": None if t50 is None else t50 / td, "t90_tdyn": None if t90 is None else t90 / td,
                          "peak_absDV": float(np.abs(D).max() / 2), "longest_DV>=0.05_Myr": lon05 / MYR,
                          "logVc_end_minus_start": float(math.log10(Vser[i, ci, -1] / Vser[i, ci, 0]))})
    BL[nm] = info; guard("B-L"); dump()
k1bl = max([x["max_absD"] for x in blres if x["f"] == 0.0] or [0.0])
P(f"  B-L unperturbed rows: max |D| = {k1bl:.1e} dex (stationarity, report only)")
for x in blres:
    if x["f"] > 0 and x["cell"] in LAGCELLS + ("RHI",):
        P(f"  {x['system']:7s} {x['reading']:9s} {x['foot']:9s} f={x['f']:.1f} {x['cell']:3s} D_V(0+)={x['DV0']:+.4f} "
          f"t50={fmt(x['t50_tdyn'])} t90={fmt(x['t90_tdyn'])} t_dyn  peak|D_V|={x['peak_absDV']:.4f} "
          f"longest>=0.05 {x['longest_DV>=0.05_Myr']:.0f} Myr  dlogVc(end-start)={x['logVc_end_minus_start']:+.4f}")
RES["report_only"]["B_L"] = {"rows": blres, "info": BL, "unperturbed_max_absD": k1bl}

# ================================================================================================ summary + exit
P("\nSUMMARY")
P(f"  Field part: INSTANT ((r/c)/t_dyn <= {fp_ratio:.1e}); the extra pull is the medium's own mass (tether-stress share ~1e-6 or less).")
P(f"  Mass part (V1): {overall}; per reading: " + "; ".join(f"{k} {v['class']} (L {v['L_min']:.2f}-{v['L_max']:.2f}, t50 {v['t50_min']:.2f}-{v['t50_max']:.2f} t_dyn)" for k, v in V1.items()))
P("  CFG764: " + "; ".join(f"{k} {v['CFG764']}" for k, v in V2.items()))
P("  CFG763: " + "; ".join(f"{k} {v['CFG763']}" for k, v in V2.items()))
P(f"  Observability (V3): {v3all}")
P("  kappa = 1/2 FITTED; footings never pooled; cold energy's mass required; not theory closed; nothing here says the data favour the framework.")
allK = k1a and k1b and k2 and k3 and k4 and sym_ok
RES["all_K_pass"] = allK
P(f"  K1a {k1a}  K1b {k1b}  K2 {k2}  K3 {k3}  K4 {k4}  sympy {sym_ok}  -> {'ALL K PASS' if allK else 'A K CHECK FAILS'}")
P(f"  runtime {elapsed():.0f} s; peak RSS {rss()/1e9:.3f} GB")
dump()
sys.exit(0 if allK else 2)
