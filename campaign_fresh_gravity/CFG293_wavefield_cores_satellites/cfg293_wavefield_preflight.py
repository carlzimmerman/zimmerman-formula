#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG293 -- CFG288'S WAVE FIELD: SOLITONIC CORES AND THE SATELLITES.  ANALYTIC PRE-FLIGHT (generic systems only).

CFG288's only one-field construction that passes the behaviour gates is a linear complex wave field, V = rho_Lambda + m^2 |Phi|^2,
a classical field whose quanta would be light bosons, with m NOT derived (window 2e-20 to 37 eV).  A linear wave field forms a
solitonic core (the Schrodinger-Poisson ground state) in every self-gravitating system.  CFG286 found that the satellites need a
rule acting INSIDE ~r_half: UFDs keep their cold core, M31 LVD dwarfs lose cold mass there.  Question: at a declared m in the window,
does the soliton move the cold mass inside r_ev = (4/3) r_half the way the satellites need, or the wrong way?

Everything is frozen in FROZEN_CRITERIA.md (committed before this script existed; its sha256 is printed below).  In one line each:
  SP       dimensionless ground state chi'' + 2chi'/x = 2(V - E)chi, V'' + 2V'/x = chi^2, shot on E; x_c (half density), I, T, J;
           M r_c = (I x_c) hbar^2/(G m^2); rho0 r_c^4 = x_c^4 hbar^2/(4 pi G m^2); r_c = k hbar/(m sigma), k = x_c sqrt(J/(3I)).
  F-H      Schive+14 eq. 7 at a = 1 with the record's collapse halo (h48 halo_mass, M_200c) converted to Schive's virial mass.
  F-V      r_c = k hbar / (m sigma_obs) for the generic system's dispersion.
  COMPOSITE rho_sol inside r_eps, the record's NFW outside; P-C: r_eps = outermost crossing (fallback 3 r_c); P-3: r_eps = 3 r_c.
  q        [M_comp(<r_ev) - M_NFW(<r_ev)] / M_NFW(<r_ev); independent of f_ex, f_b and the footing.
  RULE     WINDOW iff some decision row D1-D4 (2e-20, 1e-19, 1e-18, 1e-17 eV), form and prescription has a classical generic
           system with q <= -0.116 AND the generic UFD with q >= -0.50.  NO WINDOW -> STOP (CFG286's harness is not run).
MODES: MUTATE=0 main; MUTATE=1 uncored (soliton off: must reproduce the NFW = reading S's cold term, q = 0 to 1e-12);
       MUTATE=2 m = 37 eV in every decision row (|q| < 1e-6, the no-core result).
kappa = 1/2 FITTED.  No dark-matter species is added by hand: the cold component is CFG288's field, and the cold mass is still
required.  Nothing here says the theory is closed or that the data favour the framework.
Run: python3 campaign_fresh_gravity/CFG293_wavefield_cores_satellites/cfg293_wavefield_preflight.py   (MUTATE=1/2 for the controls)
"""
import sys
sys.dont_write_bytecode = True
import os, math, json, time, hashlib
import numpy as np
from scipy.integrate import solve_ivp, quad, simpson
from scipy.optimize import brentq
from scipy import constants as SC

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
import CFG4_common as C4

MODE = int(os.environ.get("MUTATE", "0"))
assert MODE in (0, 1, 2)
SLUG = "cfg293_wavefield_preflight" + (f"_MUTATE{MODE}" if MODE else "")
R = C.Report(SLUG, False)
P, check = R.P, R.check
LB0 = MODE == 0                                   # in MUTATE runs only the mode's own check is load-bearing (frozen section 7)
P(__doc__.split("Run: python3")[0].strip())
FROZEN = os.path.join(HERE, "FROZEN_CRITERIA.md")
SHA = hashlib.sha256(open(FROZEN, "rb").read()).hexdigest()
P(f"\n  FROZEN_CRITERIA.md sha256 {SHA}")
R.num("frozen_sha256", SHA)
if MODE:
    P(f"\n  *** MUTATE={MODE}: " + {1: "uncored wave field (soliton switched off; composite = the record's NFW) -- q must be 0 to 1e-12",
                                 2: "m = 37 eV in every decision row (core negligible) -- |q| must be < 1e-6"}[MODE] + " ***")

# ================================================================================================ the record's machinery (read-only)
HUNT = os.path.join(C.REPO, "hunt_2026")
sys.path.insert(0, HUNT)
g48, _ = C4.exec_slices(os.path.join(HUNT, "h48_h69b_relative_isolation.py"), [(None, 'P("="*122); P("PART 1')], name="h48")
halo_mass, nfw_enclosed, RHO_C_MPC = g48["halo_mass"], g48["nfw_enclosed"], g48["_RHO_C"]
G_SI, MSUN, KPC_M = g48["G"], g48["Msun"], g48["kpc"]
PC_M = KPC_M / 1000.0
HBAR, EV, CL = SC.hbar, SC.e, SC.c
OM = C.OM_PL                                       # 0.3153, CFG7's Planck 2018 Omega_m
RHO_C_PC = RHO_C_MPC / 1e18                        # Msun / pc^3 (h48's, H0 = 67.4)
C45 = json.load(open(os.path.join(LANES, "CFG45_rule_readings_results.json")))["numbers"]
P(f"\n  constants: G {G_SI}, Msun {MSUN}, pc {PC_M} m (hunt_lib, as h48/FG001); hbar {HBAR}, eV {EV}, c {CL} (CODATA via scipy); "
  f"Omega_m {OM}; rho_crit {RHO_C_PC:.6e} Msun/pc^3")


def m_kg(m_ev):
    return m_ev * EV / CL ** 2


def HB(m_ev):
    """hbar^2 / (G m^2) in Msun pc."""
    return HBAR ** 2 / (G_SI * m_kg(m_ev) ** 2) / (MSUN * PC_M)


def hbar_over_m_sigma_pc(m_ev, sig_kms):
    return HBAR / (m_kg(m_ev) * sig_kms * 1e3) / PC_M


# ================================================================================================ 3.1 the Schrodinger-Poisson ground state
X0 = 1e-5


def sp_shoot(E, rtol, xend=60.0):
    y0 = [1.0 - E * X0 ** 2 / 3.0, -2.0 * E * X0 / 3.0, X0 ** 2 / 6.0, X0 / 3.0]

    def rhs(x, y):
        chi, dchi, V, dV = y
        return [dchi, 2.0 * (V - E) * chi - 2.0 * dchi / x, dV, chi * chi - 2.0 * dV / x]

    def ev_node(x, y):
        return y[0]
    ev_node.terminal, ev_node.direction = True, -1

    def ev_turn(x, y):
        return y[1]
    ev_turn.terminal, ev_turn.direction = True, 1
    s = solve_ivp(rhs, (X0, xend), y0, method="DOP853", rtol=rtol, atol=1e-24, events=(ev_node, ev_turn), dense_output=True)
    kind = "node" if len(s.t_events[0]) else ("turn" if len(s.t_events[1]) else "none")
    return kind, s


def sp_solve(rtol):
    lo, hi = 1e-3, 10.0
    assert sp_shoot(lo, rtol)[0] == "turn" and sp_shoot(hi, rtol)[0] == "node"
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid in (lo, hi):
            break
        k, _s = sp_shoot(mid, rtol)
        if k == "node":
            hi = mid
        else:
            lo = mid
    return lo, hi


E_A = sp_solve(1e-11)
E_B = sp_solve(1e-13)
E_SP = E_B[0]
kind, SOL = sp_shoot(E_SP, 1e-13)
x_turn = float(SOL.t[-1])
xg = np.linspace(X0, x_turn, 600001)
Yg = SOL.sol(xg)
chi_g = Yg[0]
below = np.where(chi_g ** 2 <= 1e-12)[0]
X_MAX = float(xg[below[0]]) if len(below) else x_turn
sel = xg <= X_MAX
xg, chi_g, dchi_g, dV_g = xg[sel], chi_g[sel], Yg[1][sel], Yg[3][sel]
I_g = xg ** 2 * dV_g                                # I(x) = int_0^x chi^2 x'^2 dx'
I_TOT = float(I_g[-1])
X_C = brentq(lambda x: SOL.sol(x)[0] ** 2 - 0.5, 0.1, 5.0, xtol=1e-14)
T_INT = float(simpson(dchi_g ** 2 * xg ** 2, x=xg))
J_INT = float(simpson(I_g * chi_g ** 2 * xg, x=xg))
K_V = X_C * math.sqrt(J_INT / (3.0 * I_TOT))
NODES = int(np.sum(np.diff(np.sign(chi_g)) != 0))
X_HALF = brentq(lambda x: float(np.interp(x, xg, I_g)) - 0.5 * I_TOT, 0.1, X_MAX)
F3 = float(np.interp(3.0 * X_C, xg, I_g)) / I_TOT
I_XC = float(np.interp(X_C, xg, I_g))


def chi2(x):
    x = np.asarray(x, float)
    out = np.where(x <= X_MAX, np.interp(np.clip(x, X0, X_MAX), xg, chi_g) ** 2, 0.0)
    return np.where(x < X0, 1.0, out)


def Icum(x):
    x = np.asarray(x, float)
    return np.where(x < X0, x ** 3 / 3.0, np.interp(np.clip(x, X0, X_MAX), xg, I_g))


R.banner("3.1  THE SCHRODINGER-POISSON GROUND STATE (derived)")
P(f"  eigenvalue E = {E_SP:.15f} (rtol 1e-13; bracket width {E_B[1] - E_B[0]:.1e});  rtol 1e-11 gives {E_A[0]:.15f}")
P(f"  x_c (half density) = {X_C:.6f};  I = {I_TOT:.6f};  T = {T_INT:.6f};  J = {J_INT:.6f};  x_max = {X_MAX:.3f} (turn at {x_turn:.3f})")
P(f"  M r_c = {I_TOT * X_C:.5f} hbar^2/(G m^2);  rho0 r_c^4 = {X_C ** 4 / (4 * math.pi):.5f} hbar^2/(G m^2);  k = x_c sqrt(J/3I) = {K_V:.5f}")
P(f"  half-mass radius = {X_HALF / X_C:.4f} r_c;  M(<3 r_c)/M = {F3:.5f};  M(<r_c)/M = {I_XC / I_TOT:.5f}")
for k_, v_ in dict(E=E_SP, x_c=X_C, I=I_TOT, T=T_INT, J=J_INT, k=K_V, x_max=X_MAX, half_mass_over_rc=X_HALF / X_C, frac_3rc=F3,
                   frac_rc=I_XC / I_TOT, Mrc_coef=I_TOT * X_C, rho0rc4_coef=X_C ** 4 / (4 * math.pi)).items():
    R.num("SP_" + k_, v_)

check("C-SP1 shooting converged and nodeless", f"E(rtol 1e-11) vs E(rtol 1e-13): rel diff {abs(E_A[0] - E_B[0]) / E_B[0]:.2e} (<= 1e-8); "
      f"sign changes of chi on [0, x_max]: {NODES}", abs(E_A[0] - E_B[0]) / E_B[0] <= 1e-8 and NODES == 0, LB0)
check("C-SP2 virial 2K + W = 0", f"T/J - 1 = {T_INT / J_INT - 1:.2e} (|.| < 1e-3)", abs(T_INT / J_INT - 1) < 1e-3, LB0)
xs3 = np.linspace(0.0, 3.0 * X_C, 3001)
fit = (1.0 + 0.091 * (xs3 / X_C) ** 2) ** -8
dev3 = float(np.max(np.abs(chi2(xs3) / fit - 1.0)))
check("C-SP3 shape vs Schive+14 eq. 3", f"max |rho_SP/rho_fit - 1| over 0 <= x <= 3 x_c = {dev3:.4f} (<= 0.03)", dev3 <= 0.03, LB0)
# POST-HOC DIAGNOSTIC (added after the first run's C-SP3 failure; not a check; the frozen tolerance is kept as written)
_rel = chi2(xs3) / fit - 1.0
_abs = float(np.max(np.abs(chi2(xs3) - fit)))
_rel2 = float(np.max(np.abs(_rel[xs3 <= 2.0 * X_C])))
P(f"  POST-HOC DIAGNOSTIC (not a check): eq. 3's fit vs the SP profile, in units of the peak density: max |diff| = {_abs:.4f} over 0..3 x_c; "
  f"relative: <= {_rel2:.4f} inside 2 x_c, peak {float(np.max(np.abs(_rel))):.4f} at x = {float(xs3[np.argmax(np.abs(_rel))] / X_C):.2f} x_c "
  "(the fit's tail is low).  The SP profile is the primary in every q; eq. 3 enters no decision number.")
R.num("posthoc_SP3", dict(max_abs_peak_units=_abs, max_rel_inside_2xc=_rel2, max_rel=float(np.max(np.abs(_rel))),
                         at_x_over_xc=float(xs3[np.argmax(np.abs(_rel))] / X_C)))
coef = X_C ** 4 * HB(1e-23) / (4 * math.pi) / 1e12            # Msun pc^-3 kpc^4
check("C-SP4 normalisation vs eq. 3's 1.9", f"x_c^4 hbar^2/(4 pi G m^2) at m = 1e-23 eV = {coef:.4f} Msun pc^-3 kpc^4; "
      f"/1.9 - 1 = {coef / 1.9 - 1:+.4f} (|.| <= 0.06)", abs(coef / 1.9 - 1) <= 0.06, LB0)
sp5 = []
for Mh in (1e9, 1e11):
    rc = 1600.0 * (Mh / 1e9) ** (-1 / 3.)
    Mrc = HB(1e-22) * I_XC * X_C / rc
    Mmin0 = 4.4e7
    Mc6 = 0.25 * (Mh / Mmin0) ** (1 / 3.) * Mmin0
    sp5.append((Mh, Mrc, Mc6, Mrc / Mc6 - 1))
check("C-SP5 eq. 6 vs eq. 7 through the SP profile (m22 = 1, a = 1)",
      "; ".join(f"M_h {a:.0e}: SP M(<r_c) {b:.3e} vs eq. 6 {c:.3e} ({d:+.3f})" for a, b, c, d in sp5) + "  (|.| <= 0.25)",
      all(abs(d) <= 0.25 for *_, d in sp5), LB0)
R.num("C_SP5", [dict(Mh=a, M_rc_SP=b, Mc_eq6=c, rel=d) for a, b, c, d in sp5])
check("C-SP6 Schive's stated fractions", f"M(<3 r_c)/M = {F3:.4f} (in [0.93, 0.97]); half-mass / r_c = {X_HALF / X_C:.4f} (in [1.40, 1.50])",
      0.93 <= F3 <= 0.97 and 1.40 <= X_HALF / X_C <= 1.50, LB0)
check("C-TAIL", f"chi(x_max)^2 = {float(chi_g[-1] ** 2):.2e} (<= 1e-12)", float(chi_g[-1] ** 2) <= 1e-12 * (1 + 1e-9), LB0)


# ================================================================================================ the record's NFW (analytic, unclipped)
def _m(t):
    t = np.asarray(t, float)
    small = t < 1e-3
    ts = np.where(small, t, 0.0)
    ser = ts ** 2 / 2 - 2 * ts ** 3 / 3 + 3 * ts ** 4 / 4 - 4 * ts ** 5 / 5 + 5 * ts ** 6 / 6 - 6 * ts ** 7 / 7
    tb = np.where(small, 1.0, t)
    return np.where(small, ser, np.log1p(tb) - tb / (1 + tb))


class NFW:
    def __init__(self, Mh):
        self.Mh = Mh
        self.c = 10 ** (0.905 - 0.101 * (math.log10(Mh * 0.674) - 12.0))
        self.R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C_MPC)) ** (1 / 3.) * 1e6        # pc
        self.rs = self.R200 / self.c
        self.mc = float(_m(self.c))
        self.rhos = Mh / (4 * math.pi * self.rs ** 3 * self.mc)

    def M(self, r):
        return self.Mh * _m(np.asarray(r, float) / self.rs) / self.mc

    def rho(self, r):
        t = np.asarray(r, float) / self.rs
        return self.rhos / (t * (1 + t) ** 2)

    def Mvir(self):
        z0 = (18 * math.pi ** 2 + 82 * (OM - 1) - 39 * (OM - 1) ** 2) / OM
        rhom = OM * RHO_C_PC
        f = lambda r: float(self.M(r)) - 4 * math.pi / 3 * r ** 3 * z0 * rhom
        rv = brentq(f, 0.3 * self.R200, 10 * self.R200, xtol=1e-10 * self.R200)
        return float(self.M(rv)), rv, z0


# ================================================================================================ core radius forms and the composite
def rc_FH(m_ev, Mh_schive):
    return 1600.0 * (m_ev / 1e-22) ** -1 * (Mh_schive / 1e9) ** (-1 / 3.)


def rc_FV(m_ev, sig):
    return K_V * hbar_over_m_sigma_pc(m_ev, sig)


def composite(m_ev, rc, nfw, r_ev, presc, uncored=False):
    """returns dict: q, r_eps, flag, rho_c, M_sol, dM, M_nfw(<r_ev)."""
    L = rc / X_C
    rho0 = HB(m_ev) / (4 * math.pi * L ** 4)
    rsol = lambda r: rho0 * chi2(np.asarray(r, float) / L)
    Msol = lambda r: 4 * math.pi * rho0 * L ** 3 * float(Icum(r / L))
    Mn_ev = float(nfw.M(r_ev))
    if uncored:
        r_eps, flag = 0.0, "uncored"
    elif presc == "P-3":
        r_eps, flag = 3.0 * rc, "fixed 3 r_c"
    else:
        rr = np.geomspace(1e-4 * rc, X_MAX * L, 4000)
        d = rsol(rr) - nfw.rho(rr)
        pos = np.where(d > 0)[0]
        if not len(pos):
            r_eps, flag = 3.0 * rc, "no crossing -> 3 r_c"
        elif pos[-1] == len(rr) - 1:
            r_eps, flag = X_MAX * L, "soliton above NFW at x_max"
        else:
            i = pos[-1]
            r_eps = brentq(lambda r: float(rsol(r)) - float(nfw.rho(r)), rr[i], rr[i + 1], xtol=1e-12 * rr[i], rtol=1e-13)
            flag = "crossing"
    re_ = min(r_ev, r_eps)
    dM = (Msol(re_) - float(nfw.M(re_))) if re_ > 0 else 0.0
    return dict(q=dM / Mn_ev, r_eps=r_eps, flag=flag, rho_c=rho0, M_sol=4 * math.pi * rho0 * L ** 3 * I_TOT, dM=dM, M_nfw=Mn_ev,
                M_comp=Mn_ev + dM, rc=rc, L=L)


# ================================================================================================ generic systems (section 4)
GU = dict(name="G-U", sig=3.0, rh=30.0, Ms=1e4)
GC = [dict(name=f"G-C s{s:g} rh{rh:g} M*{Ms:.0e}", sig=s, rh=rh, Ms=Ms) for Ms in (1e6, 1e7) for rh in (200.0, 500.0, 1000.0)
      for s in (8.0, 10.0, 12.0)]
for d in [GU] + GC:
    d["Mc"] = float(halo_mass(d["Ms"]))
    d["nfw"] = NFW(d["Mc"])
    d["Mvir"], d["rvir"], ZETA0 = d["nfw"].Mvir()
    d["rev"] = 4.0 / 3.0 * d["rh"]
R.banner("4  GENERIC SYSTEMS (the record's SHMR and NFW; not the samples)")
P(f"  zeta(0) = {ZETA0:.2f} (Schive's formula at Omega_m = {OM});  generic UFD M_c = halo_mass(1e4) = {GU['Mc']:.4e}")
for d in [GU] + [g for g in GC if g["sig"] == 10.0]:
    P(f"  {d['name']:<26} M_c {d['Mc']:.3e}  c {d['nfw'].c:.2f}  R200 {d['nfw'].R200 / 1e3:.2f} kpc  M_vir/M_200c {d['Mvir'] / d['Mc']:.3f}  "
      f"r_ev {d['rev']:.1f} pc  M_NFW(<r_ev) {float(d['nfw'].M(d['rev'])):.3e}")
cnfw = max(abs(float(d["nfw"].M(d["rev"])) / float(nfw_enclosed(d["Mc"], d["rev"] / 1e3)) - 1) for d in [GU] + GC)
check("C-NFW analytic NFW = h48's nfw_enclosed at every generic r_ev", f"max rel diff {cnfw:.2e} (<= 1e-12)", cnfw <= 1e-12, LB0)
R.num("generic", {d["name"]: dict(Mc=d["Mc"], Mvir=d["Mvir"], c=d["nfw"].c, rev=d["rev"], sig=d["sig"], M_nfw_rev=float(d["nfw"].M(d["rev"])))
                  for d in [GU] + GC})

# ================================================================================================ the rows
M37 = 37.0
ROWS = [("D1", 2e-20), ("D2", 1e-19), ("D3", 1e-18), ("D4", 1e-17)]
if MODE == 2:
    ROWS = [(k, M37) for k, _ in ROWS]
REP = [("R-top", M37), ("R-out", 1e-22)]
FORMS, PRESCS = ("F-H", "F-V"), ("P-C", "P-3")
UNC = MODE == 1
Q_BITE, Q_SPARE = -0.116, -0.50


def rc_for(form, m_ev, d, Mh_override=None):
    return rc_FH(m_ev, d["Mvir"] if Mh_override is None else Mh_override) if form == "F-H" else rc_FV(m_ev, d["sig"])


def run_row(m_ev):
    out = {}
    for form in FORMS:
        for pr in PRESCS:
            u = composite(m_ev, rc_for(form, m_ev, GU), GU["nfw"], GU["rev"], pr, UNC)
            cs = [composite(m_ev, rc_for(form, m_ev, g), g["nfw"], g["rev"], pr, UNC) for g in GC]
            qs = np.array([c["q"] for c in cs])
            out[(form, pr)] = dict(U=u, C=cs, qC_min=float(qs.min()), qC_max=float(qs.max()),
                                   rcC=(min(c["rc"] for c in cs), max(c["rc"] for c in cs)),
                                   reps_rc_C=(min(c["r_eps"] / c["rc"] for c in cs), max(c["r_eps"] / c["rc"] for c in cs)),
                                   flagsC=sorted(set(c["flag"] for c in cs)),
                                   window=bool(qs.min() <= Q_BITE and u["q"] >= Q_SPARE))
    return out


RES = {k: run_row(m) for k, m in ROWS + REP}


def show(k, m_ev):
    P(f"\n  --- {k}: m = {m_ev:.0e} eV" + ("  (OUTSIDE the window; reported / C-SIGN only)" if k == "R-out" else ""))
    P(f"  {'form':<4} {'presc':<5} | {'G-U r_c [pc]':>12} {'rho_c':>10} {'M_sol':>10} {'r_eps/r_c':>9} {'q_U':>10} | "
      f"{'G-C r_c [pc]':>17} {'r_eps/r_c':>11} {'q_C min':>10} {'q_C max':>10} | window")
    for (form, pr), v in RES[k].items():
        u = v["U"]
        P(f"  {form:<4} {pr:<5} | {u['rc']:12.4g} {u['rho_c']:10.3g} {u['M_sol']:10.3g} {u['r_eps'] / u['rc'] if u['rc'] else 0:9.2f} "
          f"{u['q']:+10.4f} | {v['rcC'][0]:8.3g}-{v['rcC'][1]:<8.3g} {v['reps_rc_C'][0]:5.2f}-{v['reps_rc_C'][1]:<5.2f} "
          f"{v['qC_min']:+10.5f} {v['qC_max']:+10.5f} | {'YES' if v['window'] else 'no'}   [U: {u['flag']}; C: {', '.join(v['flagsC'])}]")


R.banner("5  THE PRE-FLIGHT: q = dM(<r_ev)/M_NFW(<r_ev) per row, form and prescription (G-U: sigma 3, r_half 30 pc, M_c 1e9)")
P("  q > 0: the soliton ADDS cold mass inside r_ev; q < 0: it removes it.  Classical bite: q_C <= -0.116; UFD spared: q_U >= -0.50.")
for k, m in ROWS + REP:
    show(k, m)
RJ = {}
for k, m in ROWS + REP:
    RJ[k] = dict(m=m, combos={f"{f}|{p}": dict(q_U=v["U"]["q"], rc_U=v["U"]["rc"], rho_c_U=v["U"]["rho_c"], M_sol_U=v["U"]["M_sol"],
                                                reps_over_rc_U=(v["U"]["r_eps"] / v["U"]["rc"]) if v["U"]["rc"] else None, flag_U=v["U"]["flag"],
                                                qC_min=v["qC_min"], qC_max=v["qC_max"], rcC=v["rcC"], reps_rc_C=v["reps_rc_C"], window=v["window"],
                                                qC={g["name"]: c["q"] for g, c in zip(GC, v["C"])})
                                for (f, p), v in RES[k].items()})
R.num("rows", RJ)

# ratio of r_c / r_ev between the UFD and the classicals (scaling statement)
P("\n  scaling: (r_c/r_ev)_UFD / (r_c/r_ev)_classical, over the 18 G-C systems (independent of m):")
for form in FORMS:
    ratios = [(rc_for(form, 1e-19, GU) / GU["rev"]) / (rc_for(form, 1e-19, g) / g["rev"]) for g in GC]
    P(f"    {form}: {min(ratios):.1f} to {max(ratios):.1f}")
    R.num(f"rc_rev_ratio_UFD_over_C_{form}", [min(ratios), max(ratios)])

# ================================================================================================ decision
WIN = [(k, f, p) for k, _ in ROWS for (f, p), v in RES[k].items() if v["window"]]
R.banner("DECISION (frozen rule, section 5)")
allC = [v["qC_min"] for k, _ in ROWS for v in RES[k].values()]
allCmax = [v["qC_max"] for k, _ in ROWS for v in RES[k].values()]
allU = [v["U"]["q"] for k, _ in ROWS for v in RES[k].values()]
P(f"  over the decision rows, all forms and prescriptions: q_C in [{min(allC):+.5f}, {max(allCmax):+.5f}];  q_U in [{min(allU):+.4f}, {max(allU):+.4f}]")
P(f"  right-sign combinations: {WIN if WIN else 'NONE'}")
P("  => " + ("RIGHT-SIGN WINDOW EXISTS: the harness of section 6 must be run." if WIN else
             "NO WINDOW.  STOP: CFG286's harness is NOT run and no satellite is scored with a core (frozen rule)."))
R.num("decision", dict(window=bool(WIN), combos=[list(w) for w in WIN], qC_range=[min(allC), max(allCmax)], qU_range=[min(allU), max(allU)]))
check("PRE-FLIGHT: a right-sign window exists in the decision rows (finding; NO -> rc 1)",
      f"{len(WIN)} of {len(ROWS) * 4} (row, form, prescription) combinations have a classical bite (q_C <= -0.116) with the UFD spared "
      f"(q_U >= -0.50)", bool(WIN), LB0)

sig_out = [(f, p) for (f, p), v in RES["R-out"].items() if v["qC_min"] <= Q_BITE]
check("C-SIGN the instrument can see the right sign (R-out, 1e-22 eV, outside the window)",
      f"combinations with some G-C q <= -0.116 at R-out: {sig_out if sig_out else 'NONE'};  q_U there: "
      + ", ".join(f"{f}/{p} {v['U']['q']:+.4f}" for (f, p), v in RES["R-out"].items()), bool(sig_out), LB0)

# ================================================================================================ MUTATE checks
if MODE == 1:
    qa = max(abs(c["q"]) for k, _ in ROWS + REP for v in RES[k].values() for c in [v["U"]] + v["C"])
    ma = max(abs(c["M_comp"] / float(nfw_enclosed(g["Mc"], g["rev"] / 1e3)) - 1) for k, _ in ROWS + REP for v in RES[k].values()
             for c, g in zip([v["U"]] + v["C"], [GU] + GC))
    check("MUTATE=1 (load-bearing): uncored reproduces the record's NFW (reading S's cold term) exactly",
          f"max |q| = {qa:.1e} (<= 1e-12); max |M_comp/nfw_enclosed - 1| = {ma:.1e} (<= 1e-12)", qa <= 1e-12 and ma <= 1e-12, True)
if MODE == 2:
    qa = max(abs(c["q"]) for k, _ in ROWS for v in RES[k].values() for c in [v["U"]] + v["C"])
    check("MUTATE=2 (load-bearing): m = 37 eV in every decision row reproduces the no-core result",
          f"max |q| over every row, form, prescription and system = {qa:.2e} (< 1e-6)", qa < 1e-6, True)

# ================================================================================================ C-MASS (quadrature)
if MODE == 0:
    cm = []
    for form in FORMS:
        for d in (GU, GC[0]):
            c = composite(2e-20, rc_for(form, 2e-20, d), d["nfw"], d["rev"], "P-C")
            L, rho0, re_ = c["L"], c["rho_c"], min(d["rev"], c["r_eps"])
            xe = re_ / L
            brk = [b for b in (X_C, 3 * X_C, X_MAX) if b < xe]
            ms = 4 * math.pi * rho0 * L ** 3 * quad(lambda x: float(chi2(x)) * x * x, 0, xe, points=brk or None, limit=400,
                                                    epsabs=0, epsrel=1e-11)[0]
            mn = quad(lambda r: 4 * math.pi * r * r * float(d["nfw"].rho(r)), re_, d["rev"], limit=400, epsabs=0, epsrel=1e-12)[0] \
                if d["rev"] > re_ else 0.0
            cm.append(abs((ms + mn) / c["M_comp"] - 1))
    check("C-MASS composite enclosed mass by quadrature = closed form", f"max rel diff {max(cm):.2e} (<= 1e-5) over G-U and one G-C, D1, both forms, P-C",
          max(cm) <= 1e-5, LB0)

# ================================================================================================ reported rows
if MODE == 0:
    R.banner("REPORTED ROWS (never verdicts)")
    # R-floor
    P("  R-floor: G-U q at the record's collapse-mass floors (P-C | P-3)")
    rfl = {}
    for Mcf in (1e8, 3e8, 1e9, 3e9, 1e10):
        nf_ = NFW(Mcf); mv = nf_.Mvir()[0]
        line = []
        for k, m in ROWS:
            for form in FORMS:
                rc = rc_FH(m, mv) if form == "F-H" else rc_FV(m, GU["sig"])
                qq = [composite(m, rc, nf_, GU["rev"], pr)["q"] for pr in PRESCS]
                rfl[f"{Mcf:.0e}|{k}|{form}"] = qq
                line.append(f"{k} {form} {qq[0]:+.3f}|{qq[1]:+.3f}")
        P(f"    M_c {Mcf:.0e}: " + "  ".join(line))
    R.num("R_floor", rfl)
    # R-Mh
    P("\n  R-Mh: F-H with M_h = M_200c directly, and with M_vir/3 (q_U | q_C min..max), P-C and P-3")
    rmh = {}
    for lab, fn in (("M_200c", lambda d: d["Mc"]), ("M_vir/3", lambda d: d["Mvir"] / 3.0)):
        for k, m in ROWS:
            for pr in PRESCS:
                u = composite(m, rc_FH(m, fn(GU)), GU["nfw"], GU["rev"], pr)["q"]
                qc = [composite(m, rc_FH(m, fn(g)), g["nfw"], g["rev"], pr)["q"] for g in GC]
                rmh[f"{lab}|{k}|{pr}"] = dict(q_U=u, qC_min=min(qc), qC_max=max(qc))
                P(f"    {lab:<7} {k} {pr}: q_U {u:+.4f} | q_C {min(qc):+.5f} .. {max(qc):+.5f}")
    R.num("R_Mh", rmh)
    # R-edge
    P("\n  R-edge: the largest m in [1e-24, 2e-20] eV at which some G-C system reaches q <= -0.116 (bisection in log m where bracketed)")
    mg = np.geomspace(1e-24, 2e-20, 49)
    redge = {}
    for form in FORMS:
        for pr in PRESCS:
            best = None
            for g in GC:
                qf = lambda lm: composite(10 ** lm, rc_for(form, 10 ** lm, g), g["nfw"], g["rev"], pr)["q"] - Q_BITE
                vals = np.array([qf(math.log10(m)) for m in mg])
                if vals[-1] <= 0:
                    me = mg[-1]
                else:
                    ok = np.where(vals <= 0)[0]
                    if not len(ok):
                        continue
                    i = ok[-1]
                    me = 10 ** brentq(qf, math.log10(mg[i]), math.log10(mg[i + 1]), xtol=1e-6)
                if best is None or me > best[0]:
                    best = (me, g["name"])
            if best is None:
                redge[f"{form}|{pr}"] = None
                P(f"    {form} {pr}: no G-C system reaches q <= -0.116 anywhere in [1e-24, 2e-20] eV")
                continue
            me, gname = best
            qu = composite(me, rc_for(form, me, GU), GU["nfw"], GU["rev"], pr)["q"]
            redge[f"{form}|{pr}"] = dict(m_edge=me, system=gname, q_U_at_edge=qu, decades_below_floor=math.log10(2e-20 / me))
            P(f"    {form} {pr}: m_edge = {me:.3e} eV ({gname}), {math.log10(2e-20 / me):.2f} decades below the floor; G-U q there = {qu:+.4f}")
    R.num("R_edge", redge)
    # aggregate translation
    UFc, UFa = C45["UF"]["canonical|S"]["km"], C45["UF"]["alt|S"]["km"]
    sU = {f: 1 - 10 ** (-2 * (C45["UF"][f"{f}|L"]["km"] - C45["UF"][f"{f}|S"]["km"])) for f in ("canonical", "alt")}
    sM = {f: 1 - 10 ** (-2 * (C45["CL"][f"m31|{f}|L"]["med"] - C45["CL"][f"m31|{f}|S"]["med"])) for f in ("canonical", "alt")}
    thr = {f: 1 - 10 ** (-2 * (abs(C45["CL"][f"m31|{f}|S"]["med"]) - 2 * C45["CL"][f"m31|{f}|S"]["tot"])) for f in ("canonical", "alt")}
    P(f"\n  thresholds re-derived from CFG45's committed JSON: classical bite {thr['canonical']:.4f} (canonical) / {thr['alt']:.4f} (alt); "
      f"cold shares s_U {sU['canonical']:.3f} / {sU['alt']:.3f}, s_M31 {sM['canonical']:.3f} / {sM['alt']:.3f}")
    check("threshold derivation reproduces the frozen 0.116", f"{thr['canonical']:.4f} / {thr['alt']:.4f} (each within 0.001 of 0.116)",
          all(abs(v - 0.116) <= 0.001 for v in thr.values()), False)
    P("  aggregate translation (APPROXIMATE, not a harness score): dKM_UFD ~ -0.5 log10(1 + s_U q_U); dmed_M31 ~ -0.5 log10(1 + s_M31 q_C)")
    agg = {}
    for k, m in ROWS:
        for (f, p), v in RES[k].items():
            dU = -0.5 * math.log10(1 + sU["canonical"] * v["U"]["q"])
            dMlo = -0.5 * math.log10(1 + sM["canonical"] * v["qC_max"])
            dMhi = -0.5 * math.log10(1 + sM["canonical"] * v["qC_min"])
            agg[f"{k}|{f}|{p}"] = dict(dKM_UFD=dU, UFD_KM_new=UFc + dU, dM31_range=[dMlo, dMhi], M31_new_range=[C45["CL"]["m31|canonical|S"]["med"] + dMlo,
                                                                                                         C45["CL"]["m31|canonical|S"]["med"] + dMhi])
            P(f"    {k} {f} {p}: UFD KM median {UFc:+.4f} -> {UFc + dU:+.4f} ({dU:+.4f}; S error 0.1431 -> z ~ {(UFc + dU) / 0.1431:+.2f}); "
              f"M31 LVD median shift {dMlo:+.4f} .. {dMhi:+.4f} (from -0.1069)")
    R.num("aggregate_translation", agg)

    # ============================================================================================ hand predictions, scored (reported)
    R.banner("HAND PREDICTIONS (frozen section 8), scored -- reported")
    rows4 = [k for k, _ in ROWS]
    he = {}
    he["HE1"] = not WIN
    he["HE2a"] = min(allC) >= 0.0
    he["HE2b"] = max(max(abs(a) for a in allC), max(abs(a) for a in allCmax)) <= 0.15
    he["HE3a"] = all(RES[k][(f, p)]["U"]["q"] > 0 for k in ("D2", "D3", "D4") for f in FORMS for p in PRESCS)
    he["HE3b"] = all(1.0 <= RES["D1"][("F-H", p)]["U"]["q"] <= 4.0 for p in PRESCS) and \
        all(-0.2 <= RES["D1"][("F-V", p)]["U"]["q"] <= 0.8 for p in PRESCS)
    he["HE4"] = bool(sig_out) and all(v["U"]["q"] <= -0.9 for v in RES["R-out"].values())
    he["HE5"] = 1.2 <= X_C <= 1.4 and 0.40 <= K_V <= 0.60
    edges = [v for v in redge.values() if v]
    if edges:
        top = max(edges, key=lambda v: v["m_edge"])
        he["HE6"] = 1e-22 <= top["m_edge"] <= 2e-21 and top["q_U_at_edge"] <= -0.5
    else:
        he["HE6"] = False
    a1 = [agg[f"D1|F-H|{p}"] for p in PRESCS]
    he["HE7"] = all(-0.3 <= a["dKM_UFD"] <= -0.2 for a in a1) and all(-0.02 <= a["dM31_range"][0] <= 0.0 and -0.02 <= a["dM31_range"][1] <= 0.0 for a in a1)
    txt = {"HE1": "NO WINDOW", "HE2a": "q_C >= 0 at every decision row/form/prescription", "HE2b": "|q_C| <= 0.15 at every decision row",
           "HE3a": "q_U > 0 at D2-D4, both forms", "HE3b": "D1: F-H q_U in [1, 4], F-V q_U in [-0.2, 0.8]",
           "HE4": "C-SIGN passes and q_U(R-out) <= -0.9 in every combination", "HE5": "x_c in [1.2, 1.4] and k in [0.40, 0.60]",
           "HE6": "R-edge m_edge in [1e-22, 2e-21] eV with G-U q <= -0.5 there", "HE7": "D1 F-H: dKM_UFD in [-0.3, -0.2]; M31 shift in [-0.02, 0]"}
    for k_, v_ in he.items():
        check(f"HAND {k_}: {txt[k_]}", "held" if v_ else "MISSED", v_, False)
    R.num("hand", he)

P("\n  kappa = 1/2 FITTED.  The cold mass is still required (CFG288's amount is free).  Nothing here says the theory is closed.")
nf = R.write(HERE)
sys.exit(1 if nf else 0)
