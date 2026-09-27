#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR11 -- THE AUTHOR'S IDEA, READING (A): "the halos is like a fluid of dark energy swirling down between the bands" (the
bands = the MOND regions' edge layers).  Can the DARK FLUID carry the edge layer's stiffness, and can the gate's edge force
on it clear galaxies while clusters keep theirs?

WHY NOW.  DE12 (7f84b3546): varied as an action term, the MOND-sector gate f = W(U), U = C[lap(u - v) + div((nu - 1) grad
S w)] (CV3's reading A+), has a second variation that is a NEGATIVE bulk modulus on the transition-layer GAS, amplified by
the phantom's response squared, A^2 with A = nu + y nu' cos^2(theta) ~ 50-100: c_gate = 1500-3700 km/s against 37-117 km/s
gas.  The A = 1 control (the baryons alone) is ~18 km/s.  DE13 (6daea932c): gradient repairs fail or cost too much.
The dark fluid (FL1/FL2/FK1: a superfluid order parameter, phi_H the cold carrier, phi_L the kicked products) does not
source the phantom (L353, FL1 F2), so a gate that reads IT has A = 1 on its channel.  MS1 found the price: a gate reading
the carrier puts an edge potential on it.  This lane tests whether that trade can work.

THE DERIVATION (S1 checks it with sympy on CV1's Lagrangian, MS1's chassis term for term, two dark components).
  Let the gate read a dark-fluid density rho (phi_H's, or the total), U = U(rho), t = (U - 1)/(2w) + 1/2, and write
  V(rho) = W(t(U(rho))) for the gate as a function of that density.  With B = dL/df (DE12's kernel term a0^2 q/(8 pi G)):
    first variation:   V_H - u_N = -B V'(rho)       (MS1 A3's matter-door form restricted to the dark fluid)
       a WELL where V' > 0 (a density reading), a BARRIER where V' < 0 (a depletion reading).  The baryons and light feel
       nothing from it: U reads no metric field and no baryon (Phi = u_N + f Psi/2 unchanged).  phi_L is untouched if U
       reads phi_H only.
    second variation (the k^0, UV part):  delta^2 E = -(1/2) B V''(rho) (delta rho)^2 on the dark fluid only:
       c_gate,d^2 = rho B V''(rho), with A = 1 because the dark fluid is kernel-invisible.  The gas block is identically
       zero (dU/d rho_b = 0): no A^2 and no A.  (The gas-dark cross term through B(w) is O(1/k).)
    the weighted MOND-sector door U = U_MS g(rho): the gas keeps g^2 x DE12's A^2 term; the dark fluid adds its own.
  THE DARK FLUID'S OWN STIFFNESS.  FK1's quartic is the pure cross term: g_HH = 0, so phi_H has no pressure of its own.
  Quantum pressure gives c_q = hbar k/(2m), metres per second at kpc scales for m >= 2e-19 eV.  What is left is its
  velocity distribution.  Vlasov (WKB): a phase-mixed, single-humped distribution with dispersion sigma along k is stable
  iff sigma^2 > c_gate,d^2 (Penrose; a Maxwellian's static response is -rho/sigma^2).  A set of COLD streams is unstable for
  every c_gate,d > 0 (1 = -rho_s c^2 k^2 sum 1/(omega - k.V_s)^2 has no real roots), each stream growing at
  k c_gate,d sqrt(rho_s/rho) down to the quantum scale k_q = 2 m c_gate,d/hbar, fastest at Gamma_max = m c_gate,d^2/hbar.
  THE PINCER (exact).  A smooth gate that switches on or off in rho has V' = 0 at the layer's end, so by the mean-value
  theorem max(rho V'') >= rho_min max|V'|/Delta rho over the rising half.  Hence
      max c_gate,d^2 >= (B_min/B_max) (rho_min/Delta rho) |delta V|max,
  and for a power-law depletion reading U = (rho/rho_c)^n, n < 0, exactly c_gate,d^2 = (1 + |n|)(rho/rho_c)|delta V| at the
  layer's centre.  A barrier or well strong enough to move the fluid (|delta V| >~ sigma^2) is unstable unless the layer
  spans a density ratio of order v_esc^2/(2 sigma^2).

THE READINGS SCORED.  (e) the phi_H density door U = (x_d/x_c,eff)^n, n > 0, x_d = 4 pi G (rho_H - <rho_H>)/H^2 at the
vacuum gate's own threshold (p = 1, x_c0 = 2.5, w = 0.25, CV1/DE12's C-infinity W); (f) its depletion mirror, n < 0;
(g) the weighted MOND-sector door U = g U_MS.  Hosts: DE12's (point-mass baryons M_b = 1e10-1e14 in an NFW host continued
past r200, M_200 = M_b/(0.3 f_b) for galaxies, M_b/f_b above), the carrier (1 - f_b)(S rho_NFW + rho_bar) with retained
fraction S, and the KiDS L* bins from L375's own shell model (XR11_shell_model_velocities.py, bins 1-2, L390's masses).

CHECKS
  C1 CONTROL [load-bearing]: this lane's reimplementation of DE12's machinery (L352's kernel, DE12's hosts, gate and
     budget) reproduces DE12's committed c_gate_max on all 24 galaxy layers and its A = 1 control (z = 0.25 and 2.5) to 1e-9.
  S1 [sympy, load-bearing] on CV1's Lagrangian (MS1's, with phi_H and phi_L): MS1's matter-door leak and MOND-sector zero
     are reproduced (control); the varied Euler-Lagrange equations of the new doors have the stated closed form (zero
     residual); V_H - u_N = -(B/8 pi G) dW(U)/d rho_H and V_L - u_N = 0 for the phi_H door, and for the weighted door;
     the local Hessian of the gate term is (B/8 pi G) d^2W/d rho_H^2 on phi_H and zero on the gas and the cross term for
     the phi_H door, (B/8 pi G) C^2 W'' on the gas for the matter door.
  N0-N4, K1, B-table (reported): the fluid's stiffness (quantum, Jeans, shell model); the density and depletion doors on
     real layers (c_gate,d, sigma there, cold or phase-mixed, Gamma, the edge potential and its height against v_esc);
     placement (KiDS, flagship, web); the weighted door's gas term; the costs.
  PRE-DECLARED HYPOTHESES (written before the first run; kept as run whatever they return):
  H1 [load-bearing] A = 1 brings the dark channel down to the fluid's own velocity scale: on every z = 0.25 galaxy layer
     (M_b = 1e10, 1e11, 1e12, S = 1, n = 1, both footings) max c_gate,d < 300 km/s (DE12's gas channel: 1500-3700 km/s).
  H2 [load-bearing] it is still not a stable gate: at z = 2.5, on every galaxy layer (same hosts, S = 1, n = 1, both
     footings), max c_gate,d exceeds the host carrier's isotropic Jeans dispersion at the layer (untruncated NFW: the
     generous, phase-mixed stiffness).
  H3 [load-bearing] a dark-density door cannot place the regions: (i) on the shell model's kicked carrier (KiDS bins 1-2,
     fiducial) the phi_H door is off (t <= 0) in every model bin inside 50 kpc, where rotation curves live; (ii) uncleared
     (S = 1 on DE12's host convention with L390's masses, and the shell model's no-decay run) its L* edge (t = 1/2) lies
     inside 1.0 Mpc at z = 0.25, short of XR9's ~1.5 Mpc.
  H4 [load-bearing] the pincer on real layers: (i) the depletion lock c^2 = (1 + |n|)(rho/rho_c)|dV| at t = 1/2 to 1e-6 for
     n = -0.5, -1, -2; (ii) max c^2 >= (B_min/B_max)(rho_min/Delta rho)|dV|max on every layer (z = 0.25 and 2.5,
     1e10-1e12, both footings, n = +-0.5, +-1, +-2).
  H5 [load-bearing] the edge force cannot clear: on every z = 0.25 layer (n = +-1, S = 1, M_b = 1e10, 1e11, 1e12, 1e13,
     1e14, both footings) sqrt(2 |dV|max) is below the host's Newtonian escape speed from 0.1 r200 with its carrier
     removed (baryons + gas: the smaller escape speed).
  H1b [load-bearing; ADDED AFTER THE FIRST RUN as the MUTATE's target, because H1 failed there] the dark channel's
     anti-stiffness is below DE12's gas channel on the same host on every z = 0.25 galaxy layer (ratio < 1).
MUTATE=1 puts the phantom's amplification back on the dark channel (dU/d rho_d -> A dU/d rho_d, A = nu: as if the carrier
sourced the phantom, i.e. were not kernel-invisible): H1b must FAIL (rc = 1).
RECORD OF THE RUNS.  First run: 8/11.  H1 FAILED as declared -- max c_gate,d = 430 km/s at the 1e12 (group) host (148 km/s
at 1e10, 247-259 at 1e11); it is kept exactly as declared and fails in every run.  Two failures were this lane's own
evaluation bugs, fixed before the second run and recorded here: S1's weighted-door comparison simplified V_H first (sympy
rewrote a log, so an identical expression did not cancel; compared unsimplified it is exactly zero), and H4's depletion lock
was evaluated at a layer centre found on the interpolated profile (off by ~1e-5 in t, giving 5.8e-6 against the 1e-6
tolerance; solved on the analytic NFW it is 3e-14 -- tolerance unchanged).  H1b was added after the first run.  The shared
machinery was then moved to XR11_common.py; the results JSON is unchanged by that move (0 differences).

SCOPE.  Frozen background, WKB (k >> 1/layer), spherical hosts; the k^0 part of the second variation (field responses are
O(1/k^2)); the Vlasov criterion in its Penrose (static) form; the shell model's limits (no cold carrier beyond ~2 r200 at
z = 0.25; a single accretion history); the flagship on DE12's host convention (point-mass baryons), not DE4's galaxy.
Not a simulation of the instability's outcome.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR11_dark_channel_gate.py
(needs XR11_shell_model_velocities_results.json; run XR11_shell_model_velocities.py first)
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR11_dark_channel_gate"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR11", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT = {"H1": True, "H2": True, "H3": True, "H4": True, "H5": True}      # set before the first run


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the phantom's amplification A = nu is put back on the dark channel; H1 must FAIL ***")

# ---------------------------------------------------------------------------------- the shared machinery (XR11_common.py)
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True                                     # write nothing outside XR11_ files
from XR11_common import *                                        # noqa: E402,F401,F403
from XR11_common import (c_l, Mpc, G, h, H0, rho_crit0, Om, OL, A0, MS, KPC, FB, E2, Hz, h_of, dh_of, q_of, nu_of,  # noqa: E402
                         ynup_of, CS, HBAR, EV, W_M, TU, FOOT, Wd, host, transition12, cgate_max12, dark_layer,
                         layer_stats, menc_nfw, jeans_sigma, v_esc)
P(f"  constants loaded (XR11_common)   [{time.time() - T0:.0f}s]")

# ============================================================================================ C1 DE12 reproduced
banner("C1  CONTROL: DE12's committed numbers from this lane's reimplementation")
R12 = json.load(open(os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness_results.json")))["numbers"]
dev = []
for key, row in R12["budget"].items():
    z, Mb, foot = key.split("/"); z, Mb = float(z), float(Mb)
    cm, re_ = cgate_max12(transition12(z, Mb, foot, 0.25))
    dev.append(abs(cm / row["c_gate_max"] - 1)); dev.append(abs(re_ / KPC / row["r_edge_kpc"] - 1))
a1 = {}
for key, val in R12["A1_control"].items():
    z, Mb = key.split("/"); cm, _ = cgate_max12(transition12(float(z), float(Mb), "canonical", 0.25, amp=False))
    a1[key] = cm; dev.append(abs(cm / val - 1))
check("C1 CONTROL: DE12's c_gate_max and edge on all 24 galaxy layers, and its A = 1 control, reproduced (1e-9)",
      f"max rel dev {max(dev):.1e} over {len(R12['budget'])} layers; A = 1 control: " +
      ", ".join(f"{k}: {v / 1e3:.2f} km/s" for k, v in a1.items()) +
      f" (DE12: {', '.join(f'{v / 1e3:.2f}' for v in R12['A1_control'].values())})", max(dev) < 1e-9)
OUT["numbers"]["C1"] = dict(max_rel_dev=max(dev), A1=a1)

# ============================================================================================ S1 sympy on CV1's chassis
banner("S1  THE DARK DOORS ON CV1's LAGRANGIAN (MS1's chassis, two dark components): first and second variations")
x = sp.symbols("x", real=True)
G_, a0_, c1, d1, m2, C = sp.symbols("G a0 c1 d1 m2 C", positive=True)
sig, rdbar = sp.symbols("sigma rhobar_d", real=True)
Phi, u, v, lam, w, Psi = [sp.Function(nm)(x) for nm in ("Phi", "u", "v", "lam", "w", "Psi")]
rb, rH, rL = [sp.Function(nm)(x) for nm in ("rho_b", "rho_H", "rho_L")]
Wf, Ff, Gf = sp.Function("W"), sp.Function("F"), sp.Function("g")
qc = lambda s: c1 * s ** sp.Rational(3, 2) + d1 * sp.log(1 + s)
qcp = lambda s: sp.Rational(3, 2) * c1 * sp.sqrt(s) + d1 / (1 + s)
d_ = lambda F_, n=1: sp.diff(F_, x, n)
wp = d_(w); s_w = wp ** 2 / a0_ ** 2
EPG = 8 * sp.pi * G_
rd = rH + rL


def lagrangian(f, M2):
    """MS1's (CV1's) L with the dark slot split into phi_H and phi_L (both couple as MS1's rho_d)."""
    return (-(rb + rd) * Phi - (2 * d_(Phi) * d_(u) - d_(u) ** 2) / EPG
            + a0_ ** 2 * f * qc(s_w) / EPG
            + Psi * (d_(w, 2) - M2 * w - f * (d_(u, 2) - d_(v, 2))) / EPG
            + lam * (d_(v, 2) - 4 * sp.pi * G_ * (rd - rdbar)) / EPG
            - sig * M2 * w ** 2 / EPG)


FIELDS = (Phi, u, v, lam, w, Psi)
fs_ = sp.Symbol("fs")
Bsym = sp.expand(sp.diff(lagrangian(fs_, m2 * (1 - fs_)), fs_) * EPG)       # B = 8 pi G dL/df (MS1's convention)
xi = sp.Symbol("xi")
DOORS = {
    "b_matter (MS1 control)": (C * (rb + rd), False),
    "c_mond_sector (MS1 control)": (C * (d_(Phi, 2) - d_(v, 2)), True),
    "e_phiH_door": (C * Ff(rH), False),
    "g_weighted_MS": (C * (d_(Phi, 2) - d_(v, 2)) * Gf(rH), True),
}
uN = sp.Function("u_N")(x)
Bs, Wps, fsym = sp.symbols("B Wp fval")
rHs, rLs, rbs = sp.symbols("rHs rLs rbs")


def clean(expr):
    """W'(U) -> Wp (the gate slope on the solution), then W(U) -> fval (its value) -- MS1 A3's replacement order."""
    expr = expr.replace(lambda e: isinstance(e, sp.Subs), lambda e: Wps)
    return expr.replace(lambda e: isinstance(e, sp.Function) and e.func == Wf, lambda e: fsym)


S1, SOLS = {}, {}
ok_all = True
for door, (U, reads_field) in DOORS.items():
    f = Wf(U)
    L = lagrangian(f, m2 * (1 - f))
    EL = {str(F_.func): sp.expand(sp.euler_equations(L, [F_], x)[0].lhs * EPG) for F_ in FIELDS}
    kf = sp.diff(U, d_(Phi, 2)) if reads_field else sp.Integer(0)       # dU/dPhi'' (= -dU/dv'')
    BW = sp.Subs(sp.Derivative(Wf(xi), xi), xi, U) * Bsym * kf
    tgt = {
        "Phi": 2 * d_(u, 2) - EPG * (rb + rd) + d_(BW, 2),
        "lam": d_(v, 2) - 4 * sp.pi * G_ * (rd - rdbar),
        "Psi": d_(w, 2) - m2 * (1 - f) * w - f * (d_(u, 2) - d_(v, 2)),
        "w": d_(Psi, 2) - m2 * (1 - f) * Psi - 2 * d_(f * qcp(s_w) * wp) - 2 * sig * m2 * (1 - f) * w,
        "u": 2 * d_(Phi, 2) - 2 * d_(u, 2) - d_(f * Psi, 2),
        "v": d_(lam, 2) + d_(f * Psi, 2) - d_(BW, 2),
    }
    res = {k_: sp.simplify(sp.expand(EL[k_] - tgt[k_])) for k_ in tgt}
    # the integrated solution (MS1's convention): the gate's parts of u and lam when U reads lap(Phi - v)
    Phi_s = uN - sp.Rational(1, 2) * kf * Wps * Bs + fsym * Psi / 2
    lam_s = -fsym * Psi + kf * Wps * Bs
    SOLS[door] = (Phi_s, lam_s)

    def potential(rsym, rfun):
        """V = -dL/d rho for one component, on the integrated solution, kept in the symbol rsym."""
        return sp.expand(clean(-sp.diff(L.subs(rfun, rsym), rsym)).subs({Phi: Phi_s, lam: lam_s}))
    VH_raw = sp.expand(potential(rHs, rH) - uN)
    VL_raw = sp.expand(potential(rLs, rL) - uN)
    VH, VL = sp.simplify(VH_raw), sp.simplify(VL_raw)                   # for printing; the checks use the raw forms
    # the local Hessian of L in (rho_b, rho_H) at fixed fields (the k^0 part of the second variation)
    Lloc = L.subs({rH: rHs, rb: rbs})
    Hbb = sp.simplify(sp.diff(Lloc, rbs, 2)); HbH = sp.simplify(sp.diff(Lloc, rbs, rHs)); HHH = sp.diff(Lloc, rHs, 2)
    S1[door] = dict(res=res, VH=VH, VL=VL, VH_raw=VH_raw, VL_raw=VL_raw, Hbb=Hbb, HbH=HbH, HHH=HHH)
    P(f"    {door:28s}: EL residuals {[str(v_) for v_ in res.values()]}; V_H - u_N = {VH if len(str(VH)) < 160 else str(VH)[:160] + '...'}; "
      f"V_L - u_N = {VL}")
    ok_all &= all(v_ == 0 for v_ in res.values())
# the stated leaks, built as the chain rule with the same solution substituted
e_ = S1["e_phiH_door"]; g_ = S1["g_weighted_MS"]
exp_b = -C * Wps * Bsym / EPG
exp_e = -C * Wps * sp.Derivative(Ff(rHs), rHs) * Bsym / EPG
exp_g = (-C * Wps * (d_(Phi, 2) - d_(v, 2)) * sp.Derivative(Gf(rHs), rHs) * Bsym / EPG).subs({Phi: SOLS["g_weighted_MS"][0]})
same = lambda a, b_: sp.simplify(sp.expand(a - b_)) == 0
ok_b = same(S1["b_matter (MS1 control)"]["VH_raw"], exp_b)
ok_c = same(S1["c_mond_sector (MS1 control)"]["VH_raw"], sp.Integer(0))
ok_e = same(e_["VH_raw"], exp_e) and same(e_["VL_raw"], sp.Integer(0))
ok_g = same(g_["VH_raw"], exp_g) and same(g_["VL_raw"], sp.Integer(0))
# Hessians: phi_H door -> gas block 0, cross 0, phi_H block (B/8piG) d^2 W(C F(rho))/d rho^2 ; matter door -> gas (B/8piG) d^2W/d rho_b^2
He = sp.simplify(e_["HHH"] - (Bsym / EPG) * sp.diff(Wf(C * Ff(rHs)), rHs, 2))
ok_h = (e_["Hbb"] == 0) and (e_["HbH"] == 0) and He == 0
Hb_matter = S1["b_matter (MS1 control)"]["Hbb"]
ok_hm = sp.simplify(Hb_matter - (Bsym / EPG) * sp.diff(Wf(C * (rbs + rHs + rL)), rbs, 2)) == 0 and Hb_matter != 0
P(f"    B = 8 pi G dL/df = {Bsym}")
P(f"    phi_H door: d2L/drho_b^2 = {e_['Hbb']}, d2L/drho_b drho_H = {e_['HbH']}, d2L/drho_H^2 - (B/8piG) d2W/drho_H^2 = {sp.simplify(He)}")
P(f"    matter door (control): d2L/drho_b^2 = (B/8piG) C^2 W'' : {ok_hm}")
check("S1 [sympy] the varied EL equations of every door have the stated closed form; MS1's leak (matter) and zero (MOND "
      "sector) are reproduced; the phi_H door leaks -(B/8piG) C W'(U) F'(rho_H) onto phi_H only, the weighted door "
      "-(B/8piG) C W'(U) lap(Phi - v) g'(rho_H); the phi_H door's gate Hessian is (B/8piG) W''-type on phi_H and exactly zero "
      "on the gas and the gas-dark cross term",
      f"EL residuals zero: {ok_all}; matter leak {ok_b}; MOND-sector zero {ok_c}; phi_H door leak {ok_e}; weighted leak {ok_g}; "
      f"Hessian (gas 0, cross 0, phi_H) {ok_h}; matter door gas Hessian {ok_hm}",
      ok_all and ok_b and ok_c and ok_e and ok_g and ok_h and ok_hm,
      "moving the gate's reading onto the dark fluid moves the whole second variation onto it: the gas sees no gate term at "
      "all (no A^2, no A); the price is MS1's edge potential, now on phi_H")
OUT["numbers"]["S1"] = {k_: {"VH": str(v_["VH"]), "VL": str(v_["VL"]), "Hbb": str(v_["Hbb"]), "HbH": str(v_["HbH"])} for k_, v_ in S1.items()}
P(f"  [{time.time() - T0:.0f}s]")


# ============================================================================================ N0 the fluid's own stiffness
banner("N0  THE DARK FLUID'S OWN STIFFNESS: quantum pressure, FK1's quartic, Jeans, and L375's shell model")
MASSES_EV = (2e-19, 1e-17, 1e-15)
N0 = {}
for m_ev in MASSES_EV:
    mk = m_ev * EV / c_l ** 2
    N0[f"{m_ev:g}"] = dict(c_q_1kpc=HBAR * (1 / KPC) / (2 * mk), c_q_10pc=HBAR * (100 / KPC) / (2 * mk))
    P(f"    m = {m_ev:g} eV: quantum pressure c_q = hbar k/2m = {N0[f'{m_ev:g}']['c_q_1kpc']:.2e} m/s at k = 1/kpc, "
      f"{N0[f'{m_ev:g}']['c_q_10pc']:.2e} m/s at k = 1/(10 pc)")
P("    FK1 K5: with the pure cross quartic lambda (Im Phi^2)^2 the cold carrier has g_HH = 0 -- no pressure of its own")
SH = json.load(open(os.path.join(HERE, "XR11_shell_model_velocities_results.json")))["numbers"]
RM_SH = np.array(SH["r_mid_kpc"])
for key, R in SH["runs"].items():
    c_ = R["cold"]
    zone = [i for i in range(len(RM_SH)) if c_["n"][i] and c_["n"][i] >= 20 and c_["sig_r"][i] is not None]
    sr = [c_["sig_r"][i] for i in zone]; st = [c_["sig_t1"][i] for i in zone]
    P(f"    shell model {key:11s}: cold carrier present {RM_SH[zone[0]]:.0f}-{RM_SH[zone[-1]]:.0f} kpc; sigma_r {min(sr):.0f}-{max(sr):.0f}, "
      f"sigma_t1 {min(st):.0f}-{max(st):.0f} km/s; multistream to {R['r_splash_kpc']:.0f} kpc; shells injected cold at "
      f"{R['r_inject_kpc']:.0f} kpc (r200 {R['r200_kpc']:.0f})")
OUT["numbers"]["N0"] = N0
check("N0 (reported) the fluid's own stiffness: quantum pressure is m/s at kpc scales; phi_H has no self-pressure (FK1); its "
      "velocity dispersion is phase-mixed only inside the shell model's multistream zone (~2 r200), cold outside",
      {k_: f"{v_['c_q_1kpc']:.1e} m/s" for k_, v_ in N0.items()}, True, load_bearing=False)

# ============================================================================================ N1 the phi_H density door
banner("N1  THE phi_H DENSITY DOOR (n = 1, vacuum threshold, w = 0.25) ON DE12's HOSTS: stiffness, sigma, growth, edge force")
ZS = (0.25, 1.0, 2.5, 4.0)
MBS = (1e10, 1e11, 1e12, 1e13, 1e14)
N1 = {}
for z in ZS:
    for Mb in MBS:
        for foot in FOOT:
            L_ = dark_layer(z, Mb, foot, n=1.0, S=1.0, ampA=MUTATE)
            st = layer_stats(L_)
            if st is None: continue
            hs = L_["hs"]
            sJ = jeans_sigma(z, Mb, st["r_e"])
            ic = st["i_cmax"]
            c = st["c_max"]
            mk = 2e-19 * EV / c_l ** 2
            gam1 = (1 / KPC) * math.sqrt(max(c ** 2 - sJ ** 2, 0.0)) / L_["H"]                # phase-mixed (Jeans) rate
            gam1c = (1 / KPC) * c / L_["H"]                                                     # a cold stream
            gmax = mk * c ** 2 / HBAR / L_["H"]                                                 # cold wave field, fastest
            rF = math.sqrt(G * Mb * MS / (0.1 * L_["a0"]))
            ve_full = v_esc(z, Mb, 0.1 * hs["r200"], 1.0); ve_clr = v_esc(z, Mb, 0.1 * hs["r200"], 0.0)
            gN = G * (Mb * MS + menc_nfw(hs, L_["r"])) / L_["r"] ** 2
            m = (L_["t"] > 0) & (L_["t"] < 1)
            Fl = -np.gradient(L_["dV"], L_["r"])
            key = f"{z}/{Mb:.0e}/{foot}"
            N1[key] = dict(r_e_kpc=st["r_e"] / KPC, r_e_over_r200=st["r_e"] / hs["r200"], c_gate_d=c, sigma_J=sJ,
                           multistream=bool(st["r_e"] < 2 * hs["r200"]), Gamma_mixed_H=gam1, Gamma_cold_H=gam1c,
                           Gamma_max_H=gmax, dV_max=st["dV_max"], v_dV=math.sqrt(2 * st["dV_max"]), dV_sign=st["dV_sign"],
                           v_esc_full=ve_full, v_esc_cleared=ve_clr, F_leak_over_gN=float(np.max(np.abs(Fl[m]) / gN[m])),
                           r200_kpc=hs["r200"] / KPC, rF_kpc=rF / KPC)
            if foot == "canonical" or Mb in (1e11,):
                P(f"    z {z:4.2f} M_b {Mb:.0e} {foot:9s}: edge {st['r_e'] / KPC:7.0f} kpc ({st['r_e'] / hs['r200']:.2f} r200); "
                  f"c_gate,d {c / 1e3:6.0f} km/s vs sigma_J {sJ / 1e3:4.0f}; Gamma(1/kpc)/H mixed {gam1:.1e} cold {gam1c:.1e}; "
                  f"well sqrt(2|dV|) {math.sqrt(2 * st['dV_max']) / 1e3:5.0f} km/s vs v_esc {ve_clr / 1e3:.0f}-{ve_full / 1e3:.0f}; "
                  f"F_leak/g_N {N1[key]['F_leak_over_gN']:.2f}")
OUT["numbers"]["N1"] = N1
P(f"  [{time.time() - T0:.0f}s]")

# ---------------------------------------------------------------------------------------- the shell model's KiDS hosts
banner("N1b  THE phi_H DOOR ON L375's SHELL-MODEL KiDS HOSTS (z = 0.25): where it is on, and the stiffness at its layers")
z = 0.25; H25 = Hz(z); xce25 = 2.5 * E2(z); rho_c25 = xce25 * H25 ** 2 / (4 * math.pi * G)
rho_bar_d25 = (1 - FB) * Om * rho_crit0 * (1 + z) ** 3
MSUN_KPC3 = MS / KPC ** 3
tt_ = np.linspace(1e-4, 1 - 1e-4, 20001)
_, W1t, W2t = Wd(tt_)
N1b = {}
for key, R in SH["runs"].items():
    for comp in ("cold", "all"):
        if comp == "all" and "nodecay" in key: continue
        rho_c = np.array([x_ if x_ is not None else 0.0 for x_ in R["cold"]["rho"]])
        rho_k = np.array([x_ if x_ is not None else 0.0 for x_ in R["kicked"]["rho"]])
        rho = (rho_c + (rho_k if comp == "all" else 0.0)) * MSUN_KPC3
        Ug = rho / rho_c25
        tg = (Ug - 1) / (2 * W_M) + 0.5
        on = [float(RM_SH[i]) for i in range(len(RM_SH)) if tg[i] >= 1]
        half = [float(RM_SH[i]) for i in range(len(RM_SH)) if tg[i] >= 0.5]
        off_in50 = all(tg[i] <= 0 for i in range(len(RM_SH)) if RM_SH[i] <= 50)
        # layers: crossings of U = 1 between adjacent bins
        lay = []
        for i in range(len(RM_SH) - 1):
            if (Ug[i] - 1) * (Ug[i + 1] - 1) < 0:
                lr = math.exp(np.interp(0.0, sorted([Ug[i] - 1, Ug[i + 1] - 1]),
                                        [math.log(RM_SH[i]), math.log(RM_SH[i + 1])] if Ug[i] < Ug[i + 1] else
                                        [math.log(RM_SH[i + 1]), math.log(RM_SH[i])]))
                y_ = G * R["Mb"] * MS / ((lr * KPC) ** 2 * A0["canonical"])
                B_ = A0["canonical"] ** 2 * float(q_of(np.array([y_]))[0]) / (8 * math.pi * G)
                Ut = 1 + 2 * W_M * (tt_ - 0.5)
                c2max = float(np.max(B_ * W2t * TU ** 2 * (Ut * rho_c25 + rho_bar_d25) / rho_c25 ** 2 * (nu_of(y_) ** 2 if MUTATE else 1.0)))
                j = int(np.argmin(np.abs(RM_SH - lr)))
                sr, st1, fo = R["cold"]["sig_r"][j], R["cold"]["sig_t1"][j], R["cold"]["f_out"][j]
                lay.append(dict(r_kpc=lr, c_gate_d=math.sqrt(max(c2max, 0)), sigma_r=sr, sigma_t1=st1, f_out=fo,
                                dV=B_ * float(W1t.max()) * TU / rho_c25 * (nu_of(y_) if MUTATE else 1.0), inside_multistream=bool(R["r_splash_kpc"] and lr <= R["r_splash_kpc"])))
        N1b[f"{key}/{comp}"] = dict(on_kpc=on, half_kpc=half, off_inside_50kpc=off_in50, layers=lay)
        P(f"    {key:11s} {comp:4s}: on (t >= 1) at {[round(v_) for v_ in on]} kpc; off inside 50 kpc: {off_in50}")
        for l_ in lay:
            P(f"        layer at {l_['r_kpc']:6.0f} kpc: c_gate,d {l_['c_gate_d'] / 1e3:5.0f} km/s vs cold sigma_r "
              f"{l_['sigma_r'] if l_['sigma_r'] is None else round(l_['sigma_r'])} / sigma_t1 "
              f"{l_['sigma_t1'] if l_['sigma_t1'] is None else round(l_['sigma_t1'])} km/s (outgoing share "
              f"{l_['f_out'] if l_['f_out'] is None else round(l_['f_out'], 2)}); well sqrt(2|dV|) {math.sqrt(2 * l_['dV']) / 1e3:.0f} km/s")
OUT["numbers"]["N1b"] = N1b

# ============================================================================================ H1 H2
banner("H1 H2  THE PRE-DECLARED HYPOTHESES ON THE DARK CHANNEL'S SIZE AND STABILITY")
gal25 = [v_ for k_, v_ in N1.items() if k_.startswith("0.25/") and float(k_.split("/")[1]) <= 1e12]
h1_max = max(v_["c_gate_d"] for v_ in gal25)
check("H1 [pre-declared] with A = 1 the dark channel's anti-stiffness on every z = 0.25 galaxy layer (1e10-1e12, S = 1, n = 1, "
      "both footings) is below 300 km/s",
      f"max c_gate,d = {h1_max / 1e3:.0f} km/s over {len(gal25)} layers (DE12's gas channel: 1526-3741 km/s)",
      (h1_max < 300e3) == EXPECT["H1"],
      ("A = 1 brings the channel down to the fluid's own velocity scale" if h1_max < 300e3 else
       f"FAILED as declared and kept: {min(v_['c_gate_d'] for v_ in gal25) / 1e3:.0f}-{h1_max / 1e3:.0f} km/s; the 1e12 (group) host "
       "exceeds 300 km/s, the galaxies 1e10-1e11 do not; A = 1 lowers the channel ~10x (H1b) but not below 300 km/s everywhere"))
ratio_dg = {k_: v_["c_gate_d"] / R12["budget"][k_]["c_gate_max"] for k_, v_ in N1.items()
            if k_.startswith("0.25/") and float(k_.split("/")[1]) <= 1e12}
check("H1b [added after the first run, the MUTATE's target] the dark channel's anti-stiffness is below DE12's gas channel on "
      "the same host on every z = 0.25 galaxy layer (ratio < 1)",
      "c_gate,d / c_gate,DE12: " + ", ".join(f"{k_}: {v_:.3f}" for k_, v_ in ratio_dg.items()),
      all(v_ < 1 for v_ in ratio_dg.values()),
      "A = 1 lowers the channel by the phantom's amplification (~10x here); it does not bring it below the fluid's own "
      "stiffness at the layer (H1, N1, H2)")
OUT["numbers"]["H1b"] = ratio_dg
gal2p5 = {k_: v_ for k_, v_ in N1.items() if k_.startswith("2.5/") and float(k_.split("/")[1]) <= 1e12}
h2 = all(v_["c_gate_d"] > v_["sigma_J"] for v_ in gal2p5.values())
check("H2 [pre-declared] at z = 2.5 the dark channel beats even the phase-mixed (Jeans) dispersion on every galaxy layer",
      "; ".join(f"{k_}: {v_['c_gate_d'] / 1e3:.0f} vs {v_['sigma_J'] / 1e3:.0f} km/s" for k_, v_ in gal2p5.items()),
      h2 == EXPECT["H2"], "the dark-fluid gate is unstable where the flagship lives, before any cold-stream argument; the "
      f"thinnest margin is the 1e12 host, c_gate,d/sigma_J = {min(v_['c_gate_d'] / v_['sigma_J'] for v_ in gal2p5.values()):.3f}")

# ============================================================================================ N2 placement
banner("N1c  A DARK READING TUNED TO THE MOND-SECTOR DOOR'S OWN EDGE (where KiDS wants the regions): stiffness there")
N1c = {}
for z in (0.25, 2.5):
    for Mb in (1e10, 1e11, 1e12):
        for foot in FOOT:
            _, r_ms = cgate_max12(transition12(z, Mb, foot, W_M))
            L0 = dark_layer(z, Mb, foot, n=1.0, S=1.0)
            rcp = float(np.interp(r_ms, L0["r"], L0["drho"]))
            L_ = dark_layer(z, Mb, foot, n=1.0, S=1.0, rho_c_override=rcp)
            st = layer_stats(L_)
            sJ = jeans_sigma(z, Mb, r_ms)
            N1c[f"{z}/{Mb:.0e}/{foot}"] = dict(r_ms_kpc=r_ms / KPC, c_gate_d=st["c_max"], sigma_J=sJ, v_dV=math.sqrt(2 * st["dV_max"]),
                                               web_delta_on=rcp / L0["rho_bar_d"], threshold_factor=rcp / L0["rho_c"])
            if foot == "canonical":
                P(f"    z {z:4.2f} M_b {Mb:.0e}: MOND-sector edge {r_ms / KPC:6.0f} kpc; a phi_H reading placed there: c_gate,d "
                  f"{st['c_max'] / 1e3:5.0f} km/s vs sigma_J {sJ / 1e3:4.0f} (cold stream: 0); edge potential sqrt(2|dV|) "
                  f"{math.sqrt(2 * st['dV_max']) / 1e3:4.0f} km/s; its threshold (x {rcp / L0['rho_c']:.3f} of the vacuum one) switches on "
                  f"every dark overdensity delta_d >= {rcp / L0['rho_bar_d']:.2f}")
OUT["numbers"]["N1c"] = N1c
check("N1c (reported) placed where KiDS wants the regions, a dark reading's layer has c_gate,d above the Jeans dispersion and a "
      "threshold that switches on every overdensity delta_d >~ 0.1-1",
      {k_: f"{v_['c_gate_d'] / 1e3:.0f} vs {v_['sigma_J'] / 1e3:.0f} km/s, web delta >= {v_['web_delta_on']:.2f}" for k_, v_ in N1c.items()
       if k_.endswith("canonical")}, True, load_bearing=False)

banner("N2  PLACEMENT: KiDS (~1.5 Mpc around L*), the flagship (on at r_F, z = 2.5, S <= 0.059), the web")
MB390 = [3.1622776601683792e10, 6.3095734448019424e10, 1.0e11, 1.2589254117941661e11]
N2 = {"kids": {}, "flagship": {}, "web": {}}
for b in (1, 2):
    for foot in FOOT:
        L_ = dark_layer(0.25, MB390[b], foot, n=1.0, S=1.0)
        st = layer_stats(L_)
        # the threshold that would put the edge at 1.5 Mpc, and the web contrast that threshold switches on
        i15 = int(np.argmin(np.abs(L_["r"] - 1500 * KPC)))
        fac = float(L_["drho"][i15] / L_["rho_c"])
        dweb = fac * L_["rho_c"] / L_["rho_bar_d"]
        N2["kids"][f"b{b}/{foot}"] = dict(edge_kpc=st["r_e"] / KPC, threshold_factor_for_1p5Mpc=fac, web_delta_on=dweb)
        P(f"    KiDS bin {b} (M_b {MB390[b]:.2e}) {foot:9s}: phi_H-door edge (S = 1) {st['r_e'] / KPC:5.0f} kpc; an edge at 1.5 Mpc "
          f"needs the threshold x {fac:.3f}, which switches on every dark overdensity delta_d >= {dweb:.2f} (XR4 filaments 3.7-6.3)")
for key, R in SH["runs"].items():
    if "nodecay" not in key: continue
    lay = N1b[f"{key}/cold"]["layers"]
    N2["kids"][f"shell/{key}"] = dict(edge_kpc=max(l_["r_kpc"] for l_ in lay) if lay else None, r_inject_kpc=R["r_inject_kpc"])
    P(f"    shell model {key}: outermost phi_H-door layer {N2['kids'][f'shell/{key}']['edge_kpc']:.0f} kpc (the model injects "
      f"cold shells at {R['r_inject_kpc']:.0f} kpc)")
for Mb in (1e10, 10 ** 10.5, 1e11):
    for foot in FOOT:
        L1 = dark_layer(2.5, Mb, foot, n=1.0, S=1.0)
        rF = math.sqrt(G * Mb * MS / (0.1 * L1["a0"]))
        X1 = float(np.interp(rF, L1["r"], L1["drho"])) / L1["rho_c"]
        S_on, S_half = (1 + W_M) / X1, 1 / X1
        Lf = dark_layer(2.5, Mb, foot, n=1.0, S=0.059)
        stf = layer_stats(Lf)
        tF = float(np.interp(rF, Lf["r"], Lf["t"]))
        pile = stf["dV_max"] / jeans_sigma(2.5, Mb, stf["r_e"], S=1.0) ** 2 if stf else None   # exponent, generous sigma (S = 1)
        rho_dF = 0.059 * X1 * L1["rho_c"] + L1["rho_bar_d"]               # the carrier at r_F with S = 0.059, + its mean
        dep_on = (L1["rho_c"] + L1["rho_bar_d"]) / rho_dF >= 1 + W_M       # the depletion mirror (n = -1, vacuum reference)
        dep_web = rho_dF / L1["rho_bar_d"] - 1                            # a reference that turns r_F on turns on every delta_d below this
        N2["flagship"][f"{Mb:.1e}/{foot}"] = dict(rF_kpc=rF / KPC, S_full_on=S_on, S_half_on=S_half, t_rF_at_S0059=tF,
                                                   edge_at_S0059_kpc=stf["r_e"] / KPC if stf else None,
                                                   c_gate_d_at_S0059=stf["c_max"] if stf else None,
                                                   v_dV_at_S0059=math.sqrt(2 * stf["dV_max"]) if stf else None,
                                                   depletion_on_at_S0059=bool(dep_on), depletion_web_on_below_if_rF_on=dep_web,
                                                   well_over_sigmaJ2_at_layer=pile)
        P(f"    flagship M_b {Mb:.1e} {foot:9s}: r_F {rF / KPC:4.1f} kpc; phi_H door fully on at r_F needs S >= {S_on:.3f} (half: "
          f"{S_half:.3f}); MS2's zero point needs S <= 0.059; at S = 0.059 t(r_F) = {tF:.2f}, edge {stf['r_e'] / KPC if stf else float('nan'):.0f} kpc, "
          f"c_gate,d {stf['c_max'] / 1e3 if stf else float('nan'):.0f} km/s, well {math.sqrt(2 * stf['dV_max']) / 1e3 if stf else float('nan'):.0f} km/s "
          f"= {pile:.1f} sigma_J^2 (a phase-mixed carrier would pile up by e^{pile:.0f}); "
          f"depletion mirror (vacuum reference) on at r_F: {dep_on}; a reference that turns r_F on turns on every delta_d <= {dep_web:.1f}")
for z in (0.25, 2.5):
    Omz = Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + OL)
    dth = 2.5 * E2(z) / (1.5 * Omz * (1 - FB))
    dep = (1 + dth) / (1 + W_M) - 1
    N2["web"][str(z)] = dict(density_door_on_above=dth, depletion_door_on_below=dep)
    P(f"    web, z = {z}: the phi_H density door switches on at delta_d >= {dth:.1f}; its depletion mirror (n = -1, vacuum reference) "
      f"is ON wherever delta_d <= {dep:.1f} -- voids, sheets, most filaments and the forest's IGM")
for b in (1, 2):                                                        # the depletion mirror on the shell model's kicked hosts
    R = SH["runs"][f"b{b}_fid"]
    rho_H = np.array([x_ if x_ is not None else 0.0 for x_ in R["cold"]["rho"]]) * MSUN_KPC3 + rho_bar_d25   # + its mean
    Ud = (rho_c25 + rho_bar_d25) / rho_H
    td = (Ud - 1) / (2 * W_M) + 0.5
    on_r = [round(float(RM_SH[i])) for i in range(len(RM_SH)) if td[i] >= 1 and RM_SH[i] <= 3000]
    off_r = [round(float(RM_SH[i])) for i in range(len(RM_SH)) if td[i] <= 0 and RM_SH[i] <= 3000]
    N2["web"][f"depletion_on_shell_b{b}"] = dict(on_kpc=on_r, off_kpc=off_r)
    P(f"    depletion mirror (vacuum reference) on the shell model's kicked bin {b}: ON at {on_r} kpc, OFF at {off_r} kpc "
      f"(the model has no carrier beyond ~2 r200 but its mean: the web beyond is ON wherever delta_d <= "
      f"{N2['web']['0.25']['depletion_door_on_below']:.1f})")
OUT["numbers"]["N2"] = N2
kids_in = [v_["edge_kpc"] for k_, v_ in N2["kids"].items() if v_["edge_kpc"] is not None]
off50 = all(N1b[f"b{b}_fid/cold"]["off_inside_50kpc"] for b in (1, 2))
check("H3 [pre-declared] a dark-density door cannot place the regions: (i) on the kicked carrier the phi_H door is off inside "
      "50 kpc; (ii) uncleared, the L* edge lies inside 1.0 Mpc (KiDS needs ~1.5)",
      f"(i) off inside 50 kpc, bins 1-2: {off50}; (ii) edges {', '.join(f'{e_:.0f}' for e_ in kids_in)} kpc",
      (off50 and max(kids_in) < 1000) == EXPECT["H3"],
      "the kick clears phi_H exactly where MOND must be on, and the uncleared carrier's density falls as r^-3, not the "
      "phantom's r^-2: the regions follow the fluid, not the galaxies")

# ============================================================================================ N3 N4 depletion mirror; weighted door
banner("N3  THE DEPLETION MIRROR (n < 0): a barrier, locked to its own instability")
N3 = {}
for z in (0.25, 2.5):
    for Mb in (1e10, 1e11, 1e12):
        for foot in FOOT:
            for n in (-0.5, -1.0, -2.0):
                L_ = dark_layer(z, Mb, foot, n=n, S=1.0)
                # the exact layer centre U = 1  <=>  drho = rho_c, solved on the analytic NFW (xtol 1e-15 of r)
                hs_ = L_["hs"]
                f_ = lambda rr_: (1 - FB) * hs_["rho_s"] / ((rr_ / hs_["rs"]) * (1 + rr_ / hs_["rs"]) ** 2) / L_["rho_c"] - 1.0
                i0 = int(np.argmin(np.abs(L_["t"] - 0.5)))
                rc_ = brentq(f_, L_["r"][max(i0 - 50, 0)], L_["r"][min(i0 + 50, len(L_["r"]) - 1)], xtol=1e-15 * L_["r"][i0], rtol=1e-15)
                Lc = dark_layer(z, Mb, foot, n=n, S=1.0, r=np.array([rc_]))
                ratio = float(Lc["c2"][0] / abs(Lc["dV"][0]))
                pred = (1 + abs(n)) * float(Lc["rho_d"][0] / Lc["read"][0])
                st = layer_stats(L_)
                N3[f"{z}/{Mb:.0e}/{foot}/n{n}"] = dict(lock_ratio=ratio, lock_pred=pred, c_max=st["c_max"], v_dV=math.sqrt(2 * st["dV_max"]),
                                                       barrier=st["dV_sign"] > 0)
            if foot == "canonical":
                rr = N3[f"{z}/{Mb:.0e}/{foot}/n-1.0"]
                P(f"    z {z} M_b {Mb:.0e}: n = -1 barrier sqrt(2 dV) {rr['v_dV'] / 1e3:.0f} km/s, c_gate,d {rr['c_max'] / 1e3:.0f} km/s; "
                  f"lock c^2/|dV| at t = 1/2 = {rr['lock_ratio']:.6f} vs (1 + |n|) rho/rho_c = {rr['lock_pred']:.6f}")
OUT["numbers"]["N3"] = N3

banner("N4  THE WEIGHTED MOND-SECTOR DOOR U = g U_MS: the gas keeps g^2 A^2; how small must g be for 1e6 K gas?")
N4 = {}
GS = np.logspace(0, -4, 81)
for z in ZS:
    for Mb in (1e10, 1e11, 1e12):
        foot = "canonical"
        g_ok, re_ok, trace, last = None, None, {}, None
        for g in GS:
            tr = transition12(z, Mb, foot, W_M, g=g)
            cm, re_ = cgate_max12(tr)
            if cm is None or re_ / KPC < 1.5: break                    # the region has left the grid (edge < 1.5 kpc)
            last = (float(g), cm, re_)
            if any(abs(math.log10(g) - lg) < 1e-9 for lg in (0, -1, -2, -3)): trace[f"{g:.0e}"] = (cm / 1e3, re_ / KPC)
            if cm <= CS["1e6K"]:
                g_ok, re_ok = float(g), re_; break
        N4[f"{z}/{Mb:.0e}"] = dict(g_needed=g_ok, edge_kpc=re_ok / KPC if re_ok else None, trace=trace,
                                   smallest_g_with_region=last[0] if last else None, c_gate_there=last[1] if last else None,
                                   edge_there_kpc=last[2] / KPC if last else None,
                                   x_c_eff_equiv=2.5 * E2(z) / g_ok if g_ok else None)
        P(f"    z {z:4.2f} M_b {Mb:.0e}: c_gate [km/s] (edge [kpc]) vs g: " +
          ", ".join(f"g {k_}: {v_[0]:.0f} ({v_[1]:.0f})" for k_, v_ in trace.items()) +
          (f"; stable (<= 117 km/s) first at g = {g_ok:.1e}, edge {re_ok / KPC:.1f} kpc, x_c,eff = {2.5 * E2(z) / g_ok:.0f}" if g_ok else
           f"; never stable before the region leaves the grid (g = {last[0]:.1e}: c_gate {last[1] / 1e3:.0f} km/s at "
           f"{last[2] / KPC:.1f} kpc)"))
OUT["numbers"]["N4"] = N4
check("N4 (reported) the weighted door keeps DE12's gas term times g^2 (S1); a uniform g is a threshold rise, and none makes "
      "1e6 K gas stable while a region survives outside ~1-2 kpc (XR9's KiDS cap: x_c,eff(0.25) <= 4.42)",
      {k_: (f"never (g {v_['smallest_g_with_region']:.0e}: {v_['c_gate_there'] / 1e3:.0f} km/s)" if v_["g_needed"] is None
            else f"g {v_['g_needed']:.1e}, edge {v_['edge_kpc']:.1f} kpc") for k_, v_ in N4.items()},
      True, "the gas instability is nearly scale-free in the MOND-sector door: moving the layer inward raises B and rho_b "
      "as fast as g and A fall", load_bearing=False)

# ============================================================================================ H4 the pincer on real layers
banner("H4  THE PINCER ON REAL LAYERS: the depletion lock, and max c^2 >= (B_min/B_max)(rho_min/Delta rho)|dV|max")
H4rows, h4_ok = {}, True
for z in (0.25, 2.5):
    for Mb in (1e10, 1e11, 1e12):
        for foot in FOOT:
            for n in (-2.0, -1.0, -0.5, 0.5, 1.0, 2.0):
                L_ = dark_layer(z, Mb, foot, n=n, S=1.0)
                m = (L_["t"] > 0) & (L_["t"] < 1)
                idx = np.where(m)[0]
                V1a = np.abs(L_["V1"][idx])
                j = int(np.argmax(V1a))
                # the rising half: from the end where V' = 0 (t = 0 side) to the steepest point
                t_ = L_["t"][idx]
                side = idx[t_ <= t_[j]]
                seg = np.sort(np.concatenate([side, [idx[j]]]))
                dr_seg = float(np.max(L_["drho"][seg]) - np.min(L_["drho"][seg]))
                rhs = (float(np.min(L_["B"][idx])) / float(np.max(L_["B"][idx]))) * float(np.min(L_["rho_d"][seg])) / dr_seg * float(np.max(np.abs(L_["dV"][idx])))
                lhs = float(np.max(L_["c2"][idx]))
                ok_ = lhs >= rhs
                h4_ok &= ok_
                H4rows[f"{z}/{Mb:.0e}/{foot}/n{n}"] = dict(max_c2=lhs, bound=rhs, ratio=lhs / rhs,
                                                          span=float(np.max(L_["drho"][seg]) / np.min(L_["drho"][seg])))
lock_dev = max(abs(v_["lock_ratio"] / v_["lock_pred"] - 1) for v_ in N3.values())
rat = [v_["ratio"] for v_ in H4rows.values()]
P(f"    MVT bound: max c^2 / bound over {len(H4rows)} layer-readings: min {min(rat):.3f}, median {np.median(rat):.2f}; rising-half "
  f"density span (w = 0.25): {min(v_['span'] for v_ in H4rows.values()):.2f}-{max(v_['span'] for v_ in H4rows.values()):.2f}")
P(f"    depletion lock: max |c^2/|dV| / ((1 + |n|) rho/rho_c) - 1| = {lock_dev:.1e} over {len(N3)} layers")
check("H4 [pre-declared] the pincer holds on real layers: the depletion lock (1e-6) and the mean-value bound on every layer "
      "and reading", f"lock dev {lock_dev:.1e}; bound satisfied on {sum(1 for v_ in H4rows.values() if v_['ratio'] >= 1)}/{len(H4rows)}",
      (lock_dev < 1e-6 and h4_ok) == EXPECT["H4"],
      "a gate on the dark fluid cannot push or hold it harder than its own anti-stiffness allows: a clearing-strength "
      "edge force (|dV| ~ v_esc^2/2) at sigma ~ 100-150 km/s needs a rising half-layer spanning a density ratio ~ v_esc^2/sigma^2")
OUT["numbers"]["H4"] = dict(rows=H4rows, lock_dev=lock_dev)

# ============================================================================================ H5 the edge force against escape
banner("H5  CAN THE EDGE FORCE CLEAR?  sqrt(2|dV|max) against escape speeds (z = 0.25; well for n = +1, barrier for n = -1)")
H5rows = {}
for Mb in MBS:
    for foot in FOOT:
        for n in (1.0, -1.0):
            L_ = dark_layer(0.25, Mb, foot, n=n, S=1.0, ampA=MUTATE)
            st = layer_stats(L_)
            hs = L_["hs"]
            ve_c = v_esc(0.25, Mb, 0.1 * hs["r200"], 0.0); ve_f = v_esc(0.25, Mb, 0.1 * hs["r200"], 1.0)
            vd = math.sqrt(2 * st["dV_max"])
            H5rows[f"{Mb:.0e}/{foot}/n{n:+.0f}"] = dict(v_dV=vd, v_esc_cleared=ve_c, v_esc_full=ve_f, r_e_kpc=st["r_e"] / KPC,
                                                       kind="barrier" if st["dV_sign"] > 0 else "well")
        r_ = H5rows[f"{Mb:.0e}/{foot}/n+1"]
        P(f"    M_b {Mb:.0e} {foot:9s}: edge {r_['r_e_kpc']:6.0f} kpc; well/barrier sqrt(2|dV|) {r_['v_dV'] / 1e3:5.0f} km/s; "
          f"v_esc(0.1 r200) {r_['v_esc_cleared'] / 1e3:.0f} (carrier removed) - {r_['v_esc_full'] / 1e3:.0f} (carrier kept) km/s")
h5 = all(v_["v_dV"] < v_["v_esc_cleared"] for v_ in H5rows.values())
check("H5 [pre-declared] the edge force cannot clear or hold: sqrt(2|dV|max) < the host's escape speed (carrier removed) on "
      "every z = 0.25 layer, galaxies to clusters, both footings, well and barrier",
      "max sqrt(2|dV|)/v_esc = " + f"{max(v_['v_dV'] / v_['v_esc_cleared'] for v_ in H5rows.values()):.3f}",
      h5 == EXPECT["H5"], "the edge potential is a small perturbation on every host's own well at z = 0.25")
OUT["numbers"]["H5"] = H5rows

# ============================================================================================ K1 costs
banner("K1  THE COSTS: kernel invisibility at the edges; would KiDS or the flagship notice?")
K1 = {}
for z, Mb in ((0.25, 6.3095734448019424e10), (0.25, 1e11), (2.5, 1e11)):
    for foot in FOOT:
        L_ = dark_layer(z, Mb, foot, n=1.0, S=1.0)
        st = layer_stats(L_)
        m = (L_["t"] > 0) & (L_["t"] < 1)
        hs = L_["hs"]
        sJ = jeans_sigma(z, Mb, st["r_e"])
        gN = G * (Mb * MS + menc_nfw(hs, L_["r"])) / L_["r"] ** 2
        Fl = -np.gradient(L_["dV"], L_["r"])
        rr, rho = L_["r"][m], L_["rho_d"][m]
        dM = float(np.sum(4 * math.pi * rr ** 2 * rho * np.expm1(-L_["dV"][m] / sJ ** 2) * np.gradient(rr)))  # equilibrium excess
        Mc2 = float((1 - FB) * menc_nfw(hs, np.array([2000 * KPC]))[0])
        _, r_ms = cgate_max12(transition12(z, Mb, foot, W_M))
        x_eq = 2.5 * E2(z) * (r_ms / st["r_e"]) ** 2                  # the MOND-sector door's threshold with an edge this small
        K1[f"{z}/{Mb:.2e}/{foot}"] = dict(F_leak_over_gN=float(np.max(np.abs(Fl[m]) / gN[m])), dV_over_sigJ2=st["dV_max"] / sJ ** 2,
                                          dM_over_Mcarrier_2Mpc=dM / Mc2, edge_kpc=st["r_e"] / KPC, ms_edge_kpc=r_ms / KPC,
                                          x_c_eff_equiv=x_eq)
        k_ = K1[f"{z}/{Mb:.2e}/{foot}"]
        P(f"    z {z:4.2f} M_b {Mb:.2e} {foot:9s}: edge force / the carrier's Newtonian gravity at the layer, max {k_['F_leak_over_gN']:.1f}; "
          f"|dV|/sigma_J^2 = {k_['dV_over_sigJ2']:.2f}; an equilibrium (phase-mixed) carrier gains {100 * k_['dM_over_Mcarrier_2Mpc']:.1f}% "
          f"of its mass inside 2 Mpc in the layer; edge {k_['edge_kpc']:.0f} kpc against the MOND-sector door's {k_['ms_edge_kpc']:.0f} kpc "
          f"(= that door at x_c,eff {x_eq:.1f})")
P("    KiDS (DE10, XR9): the carrier's whole lensing is worth ~8 in Delta chi^2 (-32.3/-29.3 with it, -24.6/-20.7 switch-only);")
P("    XR9's scan puts the MOND-sector door at x_c,eff(0.25) = 18.2 at Delta chi^2 = +161 and caps KiDS at 4.42.  The dark door's")
P("    edge is where that door would sit at the x_c,eff printed above -- KiDS sees the placement before it sees the edge force.")
OUT["numbers"]["K1"] = K1
check("K1 (reported) the costs: the carrier stops being kernel-invisible at every edge (a force several times its own gravity "
      "there, an O(1) equilibrium response at z = 0.25); KiDS sees the regions' size first; the flagship's window sits next to "
      "a well that piles the carrier up", {k_: f"F/g_N {v_['F_leak_over_gN']:.1f}, dM/M {v_['dM_over_Mcarrier_2Mpc']:.3f}, "
                                               f"x_equiv {v_['x_c_eff_equiv']:.1f}" for k_, v_ in K1.items()}, True, load_bearing=False)

# ============================================================================================ the barrier table
banner("BARRIER/WELL TABLE for the review: L*, groups, clusters, z = 0.25 and 2.5, both footings (n = +1 well, n = -1 barrier)")
BT = {}
for z in (0.25, 2.5):
    for Mb, lab in ((6.3e10, "L*"), (1e12, "group"), (1e13, "rich group"), (1e14, "cluster")):
        for foot in FOOT:
            row = {}
            for n in (1.0, -1.0):
                L_ = dark_layer(z, Mb, foot, n=n, S=1.0, ampA=MUTATE)
                st = layer_stats(L_)
                row[f"n{n:+.0f}"] = math.sqrt(2 * st["dV_max"])
            hs = host(Mb, z)
            ve_c, ve_f = v_esc(z, Mb, 0.1 * hs["r200"], 0.0), v_esc(z, Mb, 0.1 * hs["r200"], 1.0)
            BT[f"{z}/{lab}/{foot}"] = dict(well=row["n+1"], barrier=row["n-1"], v_esc_cleared=ve_c, v_esc_full=ve_f,
                                           r_e_kpc=layer_stats(dark_layer(z, Mb, foot))["r_e"] / KPC)
            P(f"    z {z:4.2f} {lab:10s} (M_b {Mb:.1e}) {foot:9s}: edge {BT[f'{z}/{lab}/{foot}']['r_e_kpc']:6.0f} kpc; well {row['n+1'] / 1e3:5.0f} / "
              f"barrier {row['n-1'] / 1e3:5.0f} km/s against v_esc {ve_c / 1e3:5.0f}-{ve_f / 1e3:5.0f} km/s")
OUT["numbers"]["barrier_table"] = BT
check("BT (reported) the edge potential's height against escape speeds, L* to clusters, z = 0.25 and 2.5, both footings",
      "see table", True, load_bearing=False)

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
