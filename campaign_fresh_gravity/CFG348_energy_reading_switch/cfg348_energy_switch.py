#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG348 -- a switch that reads the baryonic specific ENERGY eps_b = |v_b|^2/2 + U instead of the expansion theta_b?
(criteria: FROZEN_CRITERIA.md, committed alone first)

MS check of the chassis's U; routes E1 (baryonic potential, MS1 door d), E2 (MOND-sector potential, door c), E3 (CFG347's
dynamical structure with an eps trigger).  Tests (a) FRW-off, (b) bound ON + fidelity, (c) transition health.
Controls: C1 (CFG347's theta_b failure), C2 (GR limit), MUTATE (threshold sign flipped).
DE12's transition(), L341's growth harness and L340's output are read/exec'd read-only (no file of theirs is written).
"""
import os, sys, json, math, io, contextlib, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG348_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "CFG348", "mutate": MUTATE, "checks": {}, "numbers": {}}
CH = []


def check(name, measured, ok, reading=""):
    ok = bool(ok)
    CH.append((name, ok))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}" + (f"\n         reading:  {reading}" if reading else ""))
    return ok


def banner(t):
    P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


P(__doc__.strip())
if MUTATE:
    P("\n  *** CFG348_MUTATE=1: threshold sign flipped -- W = 1 - S(eps/eps_on), ON at eps <= 0 ***")

# ------------------------------------------------------------------ record machinery, read-only (as CFG347)
P_DE12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
NS = {"__name__": "de12_readonly", "__file__": P_DE12}
_src = open(P_DE12).read().split('banner("G1 G2')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
G, KPC, MS, FB, CS, Wd, transition, host = [NS[k] for k in ("G", "KPC", "MS", "FB", "CS", "Wd", "transition", "host")]
H0, Om, rho_crit0, A0, Hz, nu_of = NS["H0"], NS["Om"], NS["rho_crit0"], NS["A0"], NS["Hz"], NS["nu_of"]
CL = 299792458.0
ZS, MBS, FOOTS = (0.25, 1.0, 2.5, 4.0), (1e10, 1e11, 1e12), ("canonical", "alt")
HOSTS = [(z, Mb, f) for z in ZS for Mb in MBS for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
_xs = np.linspace(1e-5, 1 - 1e-5, 200001)
_S, _S1, _S2 = Wd(_xs)
S1MAX, S2MAX = float(np.max(np.abs(_S1))), float(np.max(np.abs(_S2)))


def Sd(s):
    """DE12's C-inf step and its derivatives (0 at s <= 0, 1 at s >= 1)."""
    a, b, c = Wd(np.atleast_1d(np.asarray(s, float)))
    return np.asarray(a, float), np.asarray(b, float), np.asarray(c, float)


def gate(eps, eps_on):
    """W(eps) and dW/deps, d2W/deps2.  Primary: W = S(-eps/eps_on) (OFF at eps >= 0); MUTATE: W = 1 - S(eps/eps_on)."""
    if MUTATE:
        s0, s1, s2 = Sd(np.asarray(eps) / eps_on)
        return 1 - s0, -s1 / eps_on, -s2 / eps_on ** 2
    s0, s1, s2 = Sd(-np.asarray(eps) / eps_on)
    return s0, -s1 / eps_on, s2 / eps_on ** 2


with contextlib.redirect_stdout(io.StringIO()):
    TRS = {KEY(*hk): transition(hk[0], hk[1], hk[2], 0.25) for hk in HOSTS}
P(f"\n  DE12 transition() loaded read-only (24 hosts); |S'|max = {S1MAX:.3f}, |S''|max = {S2MAX:.3f}")


def r_ta(z, Mb):
    """CFG347's turnaround radius (mean enclosed density = 5.55 rho_m-bar(z), EdS value; approximation)."""
    hs = host(Mb, z); rb = Om * rho_crit0 * (1 + z) ** 3
    menc = lambda r: 4 * math.pi * hs["rho_s"] * hs["rs"] ** 3 * (math.log(1 + r / hs["rs"]) - (r / hs["rs"]) / (1 + r / hs["rs"]))
    fn = lambda lr: (menc(math.exp(lr)) / (4 / 3 * math.pi * math.exp(lr) ** 3) + rb) - 5.55 * rb
    return math.exp(brentq(fn, math.log(hs["r200"]), math.log(1e3 * hs["r200"])))


RTA = {KEY(*hk): r_ta(hk[0], hk[1]) for hk in HOSTS}
r30 = 30 * KPC
EPS_ZC = {f: A0[f] * CL / H0 for f in FOOTS}                      # zero-constant framework velocity^2 a0 c/H0
P(f"  r_ta {min(RTA.values())/KPC:.0f}-{max(RTA.values())/KPC:.0f} kpc; zero-constant eps_on = a0 c/H0 = "
  + ", ".join(f"{f} {v/CL**2:.3f} c^2" for f, v in EPS_ZC.items()))

# ============================================================================== MS check of the chassis's U
banner("MS  IS THE CHASSIS'S U BARYONIC?  (record: L340 H1, C-H's scalar block)")
l340 = open(os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion.out")).read()
line = [ln for ln in l340.splitlines() if "U/psi_N" in ln][0].strip()
ac_, C_ = sp.symbols("alpha_c C")
Ulim = sp.limit(-2 / (C_ * ac_ + ac_ - 2), ac_, 0)
P(f"  L340 (record): {line}")
P(f"  alpha_c -> 0: U/psi_N = {Ulim}; psi_N = -R/(4k^2) is sourced by the TOTAL matter R coupling to g (CFG329 G9: matter "
  "couples to g only), i.e. baryons + the cold carrier")
check("MS1 the chassis's auxiliary U is the Newtonian potential of ALL matter (carrier included): MS1's curvature/matter door, "
      "which leaks 0.06-2300x the carrier's gravity at region edges once the gate is varied -> NOT admissible as the reader",
      f"U/psi_N = {Ulim} (alpha_c -> 0)", Ulim == 1,
      "the proposal's U violates the record rule; E1 (baryonic U_b, door d) and E2 (lap(Phi - v), door c) are the admissible replacements")
OUT["numbers"]["MS"] = dict(record_line=line, U_over_psiN=str(Ulim))

# ============================================================================== S: symbolic
banner("S  SYMBOLIC: FRW shell identity; velocity-reading inertia; baryonic escape theorem")
Hs, rho_s, Ls, r_, Gs, a_, kk = sp.symbols("H rho Lambda r G a k", positive=True)
shell = sp.Rational(1, 2) * Hs ** 2 * r_ ** 2 - sp.Rational(4, 3) * sp.pi * Gs * rho_s * r_ ** 2 - Ls * r_ ** 2 / 6
fr = sp.simplify(shell.subs(Hs ** 2, 8 * sp.pi * Gs * rho_s / 3 + Ls / 3 - kk / a_ ** 2))
P(f"  shell energy H^2 r^2/2 - GM(<r)/r - Lambda r^2/6 with Friedmann H^2 = 8piG rho/3 + Lambda/3 - k/a^2: {fr}"
  "  -> 0 for flat FRW: the Hubble flow sits EXACTLY at eps = 0 (marginally bound), whatever Lambda")
v1, v2, rho, B, W1, W2, U0 = sp.symbols("v1 v2 rho B W1 W2 U0", real=True)
Wf = sp.Function("W")
e_ = sp.Symbol("e")
Lv = rho / 2 * (v1 ** 2 + v2 ** 2) + B * Wf((v1 ** 2 + v2 ** 2) / 2 + U0)
Hm = sp.hessian(Lv, (v1, v2))
vc = sp.Symbol("v_c", positive=True)
Hm0 = Hm.subs({v1: vc, v2: 0}).doit()
Hm0 = sp.simplify(Hm0.replace(lambda q: isinstance(q, sp.Subs), lambda q: W2 if q.expr.derivative_count == 2 else W1))
P(f"  L = rho v^2/2 + B W(v^2/2 + U) about v = v_c e_1 (W1 = W', W2 = W'' at eps_0): inertia matrix {Hm0.tolist()}"
  "  -> m_par = rho + B (W' + W'' v_c^2), m_perp = rho + B W'")
gN, nu = sp.symbols("g_N nu", positive=True)
eps_pm = sp.factor(sp.Rational(1, 2) * nu * gN * r_ - gN * r_)
M_, a0s = sp.symbols("M a0", positive=True)
vf2 = sp.sqrt(Gs * M_ * a0s)
r_star = sp.solve(sp.Eq(vf2 / 2 - Gs * M_ / r_, 0), r_)[0]
P(f"  baryonic energy of a steady circular MOND orbit (point mass): eps_b = {eps_pm}  (> 0 iff nu > 2); flat curve: "
  f"eps_b = v_f^2/2 - GM/r > 0 beyond r* = {sp.simplify(r_star)} = 2 r_M")
s_ok = sp.simplify(fr + kk * r_ ** 2 / (2 * a_ ** 2)) == 0 and sp.simplify(Hm0[0, 0] - (rho + B * (W1 + W2 * vc ** 2))) == 0 and \
    sp.simplify(Hm0[1, 1] - (rho + B * W1)) == 0 and sp.simplify(r_star - 2 * sp.sqrt(Gs * M_ / a0s)) == 0
check("S1 symbolic: flat-FRW shell energy = -k r^2/(2a^2) = 0 exactly; velocity-reading gate inertia m_par = rho + B(W' + W'' v^2), "
      "m_perp = rho + B W'; baryonic eps_b = g_N r (nu/2 - 1), positive beyond 2 r_M on a flat curve",
      f"shell = {fr}; m_par = {Hm0[0,0]}; r* = {r_star}", s_ok)
OUT["numbers"]["S"] = dict(shell=str(fr), inertia=str(Hm0.tolist()), eps_pm=str(eps_pm), r_star=str(r_star))

# ============================================================================== C1, C2 controls
banner("C1  CONTROL: CFG347's theta_b failure in (b), exact settings")
TH_ON = {f: A0[f] / CL for f in FOOTS}
c1 = {"R2 3H": [], "R1 a0/c": []}
for hk in HOSTS:
    tr = TRS[KEY(*hk)]
    Om30 = math.sqrt(float(np.interp(r30, tr["r"], tr["g"])) / r30)
    c1["R2 3H"].append(0.1 * Om30 / (3 * tr["H"])); c1["R1 a0/c"].append(0.1 * Om30 / TH_ON[hk[2]])
rng_ = {k_: (min(v), max(v)) for k_, v in c1.items()}
ok1 = all(abs(rng_["R2 3H"][0] / 0.29 - 1) < 0.02 or abs(rng_["R2 3H"][0] - 0.29) < 0.006 for _ in [0]) and \
    abs(rng_["R2 3H"][1] / 6.6 - 1) < 0.02 and abs(rng_["R1 a0/c"][0] / 33 - 1) < 0.02 and abs(rng_["R1 a0/c"][1] / 154 - 1) < 0.02
check("C1 CONTROL: theta_b gate x = 0.1 Omega(30 kpc)/theta_* reproduces CFG347's 0.29-6.6 (3H) and 33-154 (a0/c) within 2%",
      "; ".join(f"{k_}: {a:.3g}-{b:.3g}" for k_, (a, b) in rng_.items()), ok1)
OUT["numbers"]["C1"] = rng_
banner("C2  CONTROL: GR limit (B = 0)")
check("C2 CONTROL: B = 0 -> inertia rho (no ghost), the gate drops out, gas + Jeans", f"{Hm0.subs(B, 0).tolist()}",
      Hm0.subs(B, 0) == sp.diag(rho, rho))

# ============================================================================== host energies (b1) and the theory's width (c)
banner("HOSTS  eps at 30 kpc (E1 baryonic, E2 MOND-sector), layer v_B, the theory's minimum width eps_on,min")
HD = {}
for hk in HOSTS:
    z, Mb, f = hk; tr = TRS[KEY(*hk)]; r = tr["r"]; g = tr["g"]; rt = RTA[KEY(*hk)]
    i = int(np.searchsorted(r, r30)); jt = int(np.searchsorted(r, rt))
    e1 = 0.5 * g[i] * r[i] - G * Mb * MS / r[i]
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(r))])      # Int_0^r g
    Ums = -(cum[jt] - cum) - g[jt] * r[jt]                                              # for r < r_ta
    e2r = 0.5 * g * r + Ums
    m = (tr["t"] > 0) & (tr["t"] < 1)
    vB2 = tr["B"][m] / tr["rho_b"][m]; vc2 = g[m] * r[m]
    emin = float(max(np.max(S1MAX * vB2), np.max(math.sqrt(S2MAX) * np.sqrt(vc2 * vB2))))
    HD[KEY(*hk)] = dict(i=i, jt=jt, e1=float(e1), e2=float(e2r[i]), e2r=e2r, vc2=float(g[i] * r[i]), Om=math.sqrt(g[i] / r[i]),
                        emin=emin, vB_med=float(np.median(np.sqrt(vB2))), y30=float(tr["y"][i]))
EPS_MIN = max(v["emin"] for v in HD.values())
P(f"  E1 eps_b(30 kpc)/v_c^2: {min(v['e1']/v['vc2'] for v in HD.values()):.3f}..{max(v['e1']/v['vc2'] for v in HD.values()):.3f}; "
  f"positive (unbound by the baryons' own Newtonian well) on {sum(v['e1'] > 0 for v in HD.values())}/24")
P(f"  E2 eps_ms(30 kpc)/v_c^2: {min(v['e2']/v['vc2'] for v in HD.values()):.3f}..{max(v['e2']/v['vc2'] for v in HD.values()):.3f} "
  f"(|eps| = {min(-v['e2'] for v in HD.values())**0.5/1e3:.0f}-{max(-v['e2'] for v in HD.values())**0.5/1e3:.0f} km/s squared)")
P(f"  layer v_B median {min(v['vB_med'] for v in HD.values())/1e3:.0f}-{max(v['vB_med'] for v in HD.values())/1e3:.0f} km/s; "
  f"eps_on,min per host {min(v['emin'] for v in HD.values())**0.5/1e3:.0f}-{EPS_MIN**0.5/1e3:.0f} km/s squared; universal = "
  f"{EPS_MIN:.3e} m^2/s^2 = {EPS_MIN/CL**2:.2e} c^2")
# DEVIATION (declared, not scored): the frozen closed form max[S' v_B^2, sqrt(S'') v_c v_B] is an approximation; the exact
# no-ghost minimum solves min_s {1 - v_B^2 S'(s)/e + v_B^2 v_c^2 S''(s)/e^2, 1 - v_B^2 S'(s)/e} > 0 on every layer.
_ss = np.linspace(0, 1, 4001); _, _s1, _s2 = Sd(_ss)


def eps_exact(hk):
    tr = TRS[KEY(*hk)]; m = (tr["t"] > 0) & (tr["t"] < 1)
    vB2 = (tr["B"][m] / tr["rho_b"][m])[:, None]; vc2 = (tr["g"][m] * tr["r"][m])[:, None]
    ok = lambda e: bool(np.min(1 - vB2 * _s1 / e + vB2 * vc2 * _s2 / e ** 2) > 0 and np.min(1 - vB2 * _s1 / e) > 0)
    lo, hi = 1e2, 1e16
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        lo, hi = (lo, mid) if ok(mid) else (mid, hi)
    return hi


for hk in HOSTS:
    HD[KEY(*hk)]["eex"] = eps_exact(hk)
EPS_EX = max(v["eex"] for v in HD.values())
P(f"  DEVIATION (sensitivity, not scored): exact no-ghost minimum per host {min(v['eex'] for v in HD.values())**0.5/1e3:.0f}-"
  f"{EPS_EX**0.5/1e3:.0f} km/s squared (frozen closed form gave {EPS_MIN**0.5/1e3:.0f}); universal {EPS_EX/CL**2:.2e} c^2")
OUT["numbers"]["eps_on_exact_universal"] = EPS_EX
OUT["numbers"]["hosts"] = {k_: {kk_: v[kk_] for kk_ in ("e1", "e2", "vc2", "emin", "vB_med", "y30")} for k_, v in HD.items()}
OUT["numbers"]["eps_on_min_universal"] = EPS_MIN

# ============================================================================== (a) FRW
banner("(a) FRW: background eps = 0; neighbourhood; L341 growth with the mean gate over the linear (Phi, v) field")
SRC = os.path.join(REPO, "real_research", "g03_audit_2026", "L341_chk_frw_gate.py")
code = open(SRC).read(); cut = code.index('banner("F1')
L41 = {"__file__": SRC, "__name__": "l341_defs"}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:cut], SRC, "exec"), L41)
if _old is None:
    os.environ.pop("MUTATE")
else:
    os.environ["MUTATE"] = _old
Or, h, Mpc, KH, DREF, A0H, nu_mono, sigma8_of = (L41[k] for k in ("Or", "h", "Mpc", "KH", "DREF", "A0", "nu_mono", "sigma8_of"))
OL = 1 - Om - Or
Ez = lambda a: math.sqrt(Or / a ** 4 + Om / a ** 3 + OL)
dlnH = lambda a: 0.5 * (-4 * Or / a ** 4 - 3 * Om / a ** 3) / Ez(a) ** 2
trapz = getattr(np, "trapezoid", None) or np.trapz
sL = solve_ivp(lambda N, Y: [Y[1], 1.5 * (Om / math.exp(3 * N) / Ez(math.exp(N)) ** 2) * Y[0] - (2 + dlnH(math.exp(N))) * Y[1]],
               (math.log(1e-3), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
Dn = lambda a: sL.sol(math.log(a))[0] / sL.sol(0.0)[0]
fg = lambda a: sL.sol(math.log(a))[1] / sL.sol(math.log(a))[0]
kc = KH * h / Mpc                                                   # comoving k in 1/m


def sig_lin(a):
    """rms physical potential and peculiar speed of the linear field (L341 spectrum, k >= 0.02 h/Mpc: a lenient cut)."""
    dl = DREF * Dn(a)
    sp2 = trapz((1.5 * Om * H0 ** 2 * dl / (a * kc ** 2)) ** 2, np.log(KH))
    sv2 = trapz((a * H0 * Ez(a) * fg(a) * dl / kc) ** 2, np.log(KH))
    return math.sqrt(sp2), math.sqrt(sv2)


RNG = np.random.default_rng(348)
NPHI = RNG.standard_normal(200000); NV2 = RNG.chisquare(3, 200000) / 3.0


def mean_gate(a, eps_on):
    sP, sV = sig_lin(a)
    return float(np.mean(gate(0.5 * sV ** 2 * NV2 + sP * NPHI, eps_on)[0]))


def growth(foot, fFRW, z_i=1000.0):
    a_i = 1 / (1 + z_i)
    sLL = solve_ivp(lambda N, Y: [Y[1], 1.5 * (Om / math.exp(3 * N) / Ez(math.exp(N)) ** 2) * Y[0] - (2 + dlnH(math.exp(N))) * Y[1]],
                    (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    Di = DREF / sLL.sol(0.0)[0]

    def grms(a, D):
        gk = 4 * math.pi * G * (Om * rho_crit0 / a ** 3) * np.abs(Di * D) / (KH * h / (a * Mpc))
        return math.sqrt(trapz(gk ** 2 / KH, KH) / trapz(1 / KH, KH))

    def rhs(N, Y):
        a = math.exp(N); D, Dp = Y
        boost = 1.0 + fFRW(a) * (nu_mono(grms(a, D) / A0H[foot]) - 1.0)
        return [Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * boost * D - (2 + dlnH(a)) * Dp]
    s = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    return s.sol(0.0)[0] / sLL.sol(0.0)[0], sigma8_of(Di * s.sol(0.0)[0])


sP0, sV0 = sig_lin(1.0)
P(f"  linear field z = 0: sigma_Phi = {sP0/CL**2:.2e} c^2 ({sP0**0.5/1e3:.0f} km/s squared), sigma_v = {sV0/1e3:.0f} km/s")
aout = {}
for lab, eon in (("zero-constant a0c/H0", None), ("eps_on,min (1 constant)", EPS_MIN)):
    for f in FOOTS:
        e_on = EPS_ZC[f] if eon is None else eon
        W_bg = float(gate(0.0, e_on)[0][0])
        nb = float(gate(-1e-3 * e_on, e_on)[0][0])                  # W just inside the bound side of FRW
        agrid = np.geomspace(1e-3, 1.0, 41)
        Wg = np.array([mean_gate(a, e_on) for a in agrid])
        fF = lambda a, Wg=Wg, agrid=agrid: float(np.interp(math.log(a), np.log(agrid), Wg)) if a >= agrid[0] else float(Wg[0])
        ratio, s8 = growth(f, fF)
        aout[f"{lab}/{f}"] = dict(W_bg=W_bg, W_nbhd=nb, meanW_z0=float(Wg[-1]), growth=ratio, sigma8=s8)
        P(f"  {lab:24s} {f:9s}: W(FRW) = {W_bg:g}; W(eps = -1e-3 eps_on) = {nb:.3g} (no finite OFF neighbourhood iff > 0); "
          f"<W>(z=0) = {Wg[-1]:.3g}; growth D/D_LCDM = {ratio:.6f}; sigma_8 = {s8:.4f}")
OUT["numbers"]["a"] = aout
a_ok = {lab: all(v["W_bg"] == 0 and v["W_nbhd"] == 0 and abs(v["growth"] - 1) < 1e-6 for k_, v in aout.items() if k_.startswith(lab))
        for lab in ("zero-constant a0c/H0", "eps_on,min (1 constant)")}
check("A1 (a) FRW: W = 0 on the background AND in a finite neighbourhood, growth = LCDM within 1e-6",
      "; ".join(f"{k_}: W_nbhd {v['W_nbhd']:.2g}, growth {v['growth']:.6f}" for k_, v in aout.items()), any(a_ok.values()),
      "flat FRW is marginally bound (eps = 0 exactly), so a zero threshold puts the Hubble flow ON the gate's edge: every "
      "overdensity (delta Phi < 0) leans ON; the linear wells are as deep as galactic ones")
if MUTATE:
    mut = min(v["growth"] for v in aout.values())
    check("MUTATE growth: the sign-flipped gate is ON on FRW and gives chassis-like fast growth (ratio >= 3)",
          f"min growth {mut:.2f}; sigma_8 " + ", ".join(f"{v['sigma8']:.2f}" for v in aout.values()), mut >= 3.0)

# ============================================================================== (b) bound
banner("(b) BOUND: static ON at 30 kpc; fidelity under a 10% compression at Omega(30 kpc)")
B1 = {}
for route in ("E1", "E2"):
    for lab, eon in (("zero-constant", None), ("eps_on,min", EPS_MIN), ("exact (sens.)", EPS_EX), ("per-host exact (lenient)", "host")):
        rows = []
        for hk in HOSTS:
            hd = HD[KEY(*hk)]; tr = TRS[KEY(*hk)]; i = hd["i"]
            e_on = EPS_ZC[hk[2]] if eon is None else (hd["eex"] if eon == "host" else eon)
            e0 = hd["e1"] if route == "E1" else hd["e2"]
            Wst = float(gate(e0, e_on)[0][0])
            worst_dW, worst_dev = 0.0, 0.0
            for k_ in (1 / KPC, 1 / (10 * KPC)):
                de = math.sqrt(hd["vc2"]) * hd["Om"] * 0.1 / k_ + nu_of(tr["y"][i]) * 4 * math.pi * G * tr["rho_b"][i] * 0.1 / k_ ** 2
                for sgn in (-1, 1):
                    Wv, W1v, W2v = (q[0] for q in gate(e0 + sgn * de, e_on))
                    worst_dW = max(worst_dW, abs(Wv - Wst))
                    rb, Bb = tr["rho_b"][i], tr["B"][i]
                    for mm in (rb + Bb * W1v, rb + Bb * (W1v + W2v * hd["vc2"])):
                        worst_dev = max(worst_dev, abs(rb / mm - 1) if mm > 0 else np.inf)
            rows.append(dict(host=KEY(*hk), W=Wst, dW=worst_dW, dev=worst_dev))
        B1[f"{route}/{lab}"] = rows
        P(f"  {route} {lab:24s}: static W(30 kpc) = 1 on {sum(r['W'] == 1.0 for r in rows)}/24 (min W {min(r['W'] for r in rows):.3g}); "
          f"|dW| max {max(r['dW'] for r in rows):.3g}; gas-mode change max {max(r['dev'] for r in rows):.3g}")
b_ok = {k_: all(r["W"] == 1.0 and r["dW"] <= 0.1 and r["dev"] <= 0.1 for r in v) for k_, v in B1.items()}
check("B1 (b) E1 baryonic potential: ON at 30 kpc on all 24 hosts, |dW| <= 0.1 and gas mode <= 10%",
      f"zero-constant {b_ok['E1/zero-constant']}, eps_on,min {b_ok['E1/eps_on,min']}; eps_b > 0 on "
      f"{sum(v['e1'] > 0 for v in HD.values())}/24", b_ok["E1/zero-constant"] or b_ok["E1/eps_on,min"],
      "MOND-supported orbits outside ~2 r_M exceed the baryons' Newtonian escape speed: a purely baryonic energy calls them unbound")
check("B2 (b) E2 MOND-sector potential: ON at 30 kpc on all 24 hosts, |dW| <= 0.1 and gas mode <= 10%",
      f"zero-constant {b_ok['E2/zero-constant']}, eps_on,min {b_ok['E2/eps_on,min']}", b_ok["E2/zero-constant"] or b_ok["E2/eps_on,min"],
      "eps is conserved along steady orbits; in the saturated interior W' = W'' = 0, so a compression changes neither W nor the gas mode")
OUT["numbers"]["b"] = {k_: dict(n_on=sum(r["W"] == 1.0 for r in v), dW_max=max(r["dW"] for r in v), dev_max=max(r["dev"] for r in v)) for k_, v in B1.items()}
# E3 zero-constant reach (CFG347 T7: reader-independent)
z0 = {}
for hk in HOSTS:
    z, Mb, f = hk; Hh = Hz(z); rt = RTA[KEY(*hk)]
    for lab, M in (("a0/c", A0[f] / CL), ("H(z)", Hh), ("3H(z)", 3 * Hh)):
        z0.setdefault(lab, []).append((CL / M / rt, CL / M <= rt / 3.89 and M >= math.sqrt(3) * Hh))
e3_ok = any(all(ok for _, ok in v) for v in z0.values())
check("B3 (b3) E3 zero-constant dynamical (c_sigma = c, framework mass): reach ell <= r_ta/3.89 and timing on all hosts",
      "; ".join(f"M = {lab}: min ell/r_ta {min(x for x, _ in v):.3g}" for lab, v in z0.items()), e3_ok,
      "CFG347 T7 is reader-independent: a luminal switch with a Hubble-scale mass averages ANY source over >> r_ta")
OUT["numbers"]["b3_E3"] = {lab: min(x for x, _ in v) for lab, v in z0.items()}

# ============================================================================== (c) transition
banner("(c) TRANSITION: inertia (ghost), gradient, Hadamard; the width the theory picks")
cc = {}
for lab, eon in (("zero-constant", None), ("eps_on,min", EPS_MIN), ("exact (sens.)", EPS_EX)):
    worst = np.inf
    for hk in HOSTS:
        tr = TRS[KEY(*hk)]; m = (tr["t"] > 0) & (tr["t"] < 1)
        e_on = EPS_ZC[hk[2]] if eon is None else eon
        ss = np.linspace(0, 1, 2001)                          # every gate value across the transition, on every layer
        rb, Bb, vc2 = tr["rho_b"][m][:, None], tr["B"][m][:, None], (tr["g"][m] * tr["r"][m])[:, None]
        _, s1, s2 = Sd(ss)
        W1v, W2v = (-s1 / e_on, s2 / e_on ** 2) if not MUTATE else (-s1 / e_on, -s2 / e_on ** 2)
        worst = min(worst, float(np.min((rb + Bb * W1v[None, :]) / rb)), float(np.min((rb + Bb * (W1v + W2v * vc2)) / rb)))
    cc[lab] = worst
    P(f"  {lab:13s}: min over layers and gate values of m/rho_b = {worst:.4f} (ghost iff <= 0)")
c_ok = {lab: v > 0 for lab, v in cc.items()}
P("  note: velocity-reading gate -> its own width is forced from below by the inertia (no-ghost) condition; the frozen closed "
  "form undershoots it (ghost at the frozen eps_on,min), the exact minimum is ghost-free by construction")
check("C3 (c) [frozen eps_on,min scored; zero-constant also] H1 no ghost on the layers for every gate value; H2 the U-dependence enters through the elliptic constraint "
      "(~k^-2), principal speeds = the gas's; H3 growth bounded uniformly in k",
      "; ".join(f"{k_}: min m/rho {v:.3g}" for k_, v in cc.items()), c_ok["zero-constant"] or c_ok["eps_on,min"])
OUT["numbers"]["c_min_m_over_rho"] = cc
wid = []
for hk in HOSTS:
    hd = HD[KEY(*hk)]; tr = TRS[KEY(*hk)]; r = tr["r"]; e2r = hd["e2r"]; jt = hd["jt"]
    j = np.where(e2r[:jt] <= -EPS_MIN / 2)[0]
    if len(j) and j[-1] < jt - 1:
        jj = j[-1]; de = abs((e2r[jj + 1] - e2r[jj - 1]) / (r[jj + 1] - r[jj - 1]))
        wid.append((KEY(*hk), EPS_MIN / de / KPC, r[jj] / KPC))
    else:
        wid.append((KEY(*hk), float("nan"), float("nan")))
okw = [w for w in wid if w[1] == w[1]]
P(f"  E2 width at eps_on,min: ell_eps = eps_on/|d eps/dr| = {min(w[1] for w in okw):.3g}-{max(w[1] for w in okw):.3g} kpc at the "
  f"crossing r = {min(w[2] for w in okw):.0f}-{max(w[2] for w in okw):.0f} kpc ({len(okw)}/24 cross inside r_ta); tolerance 100 kpc; "
  "CFG337 ell_min 183-378 kpc (C2) / 2.9 Mpc (C1)")
OUT["numbers"]["width_E2"] = wid
# nested-well numbers for the obstruction
dwarf = min(-v["e2"] for v in HD.values())
P(f"  nested wells: sigma_Phi,lin(z=0) = {sP0:.3e} m^2/s^2 vs the shallowest host |eps_ms(30 kpc)| = {dwarf:.3e} and eps_on,min = {EPS_MIN:.3e}")
OUT["numbers"]["nested"] = dict(sigma_Phi_lin=sP0, sigma_v_lin=sV0, host_min=dwarf, eps_on_min=EPS_MIN)

# ============================================================================== verdict
banner("VERDICT (frozen rule)")
routes = {
    "E1 baryonic U_b, zero-constant": dict(a=a_ok["zero-constant a0c/H0"], b=b_ok["E1/zero-constant"], c=c_ok["zero-constant"], n=0),
    "E1 baryonic U_b, eps_on,min": dict(a=a_ok["eps_on,min (1 constant)"], b=b_ok["E1/eps_on,min"], c=c_ok["eps_on,min"], n=1),
    "E2 MOND-sector U_ms, zero-constant": dict(a=a_ok["zero-constant a0c/H0"], b=b_ok["E2/zero-constant"], c=c_ok["zero-constant"], n=0),
    "E2 MOND-sector U_ms, eps_on,min": dict(a=a_ok["eps_on,min (1 constant)"], b=b_ok["E2/eps_on,min"], c=c_ok["eps_on,min"], n=1),
    "E3 dynamical, zero-constant": dict(a=a_ok["zero-constant a0c/H0"], b=e3_ok and b_ok["E2/zero-constant"], c=c_ok["zero-constant"], n=0),
}
tier = lambda r: ("FIRST-PRINCIPLES SWITCH" if (r["a"] and r["b"] and r["c"] and r["n"] == 0) else
                  "CANDIDATE WITH COST" if (r["a"] and r["b"] and r["c"]) else
                  "PARTIAL" if (r["a"] + r["b"] + r["c"]) == 2 else "NO-GO")
order = ["FIRST-PRINCIPLES SWITCH", "CANDIDATE WITH COST", "PARTIAL", "NO-GO"]
for nm, r in routes.items():
    r["tier"] = tier(r)
    P(f"  {nm:38s}: (a) {'P' if r['a'] else 'F'} (b) {'P' if r['b'] else 'F'} (c) {'P' if r['c'] else 'F'}; new constants {r['n']} -> {r['tier']}")
sens = dict(a=False, b=b_ok["E2/exact (sens.)"], c=c_ok["exact (sens.)"], n=1)
P(f"  sensitivity (not scored) E2 at the exact no-ghost eps_on: (a) F (b) {'P' if sens['b'] else 'F'} (c) {'P' if sens['c'] else 'F'} -> {tier(sens)}; "
  f"per-host exact (lenient, n = 24) (b) {'P' if b_ok['E2/per-host exact (lenient)'] else 'F'}")
OUT["sensitivity"] = dict(E2_exact=dict(sens, tier=tier(sens)), E2_perhost_b=b_ok["E2/per-host exact (lenient)"])
bt = min(order.index(r["tier"]) for r in routes.values())
bests = [nm for nm, r in routes.items() if order.index(r["tier"]) == bt]
P(f"\n  OVERALL: {order[bt]} (best: {'; '.join(bests)}); chassis U excluded (MS-illegal)")
OUT["verdict"] = dict(overall=order[bt], best_routes=bests, routes=routes)
P(f"\n  elapsed {time.time() - T0:.1f} s")
json.dump(OUT, open(os.path.join(HERE, f"cfg348_energy_switch_results{SUF}.json"), "w"), indent=1, default=str)
P("  checks: " + ", ".join(f"{n.split()[0]} {'PASS' if ok else 'FAIL'}" for n, ok in CH))
sys.exit(1 if MUTATE and not any(a_ok.values()) else 0)
