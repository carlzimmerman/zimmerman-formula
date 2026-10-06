#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG349 -- a causal MEMORY switch on the khronon clock: a ratchet along the baryon flow.  (criteria: FROZEN_CRITERIA.md)

Ratchet R:  u_b.dm = (u_b.dT) Gamma_b H(-theta_b) (1 - m),  Gamma_b = sqrt(4 pi G rho_b),  H(0) = 1,  MOND sector x f(m) = m.
Tests (a) FRW-off, (b) bound ON + fidelity + no flicker, (c) transition health; legality of the L-ord and L-CTP actions;
ownership classes; controls K1 (CFG242 latch), K2 (Gamma = 0), MUTATE (reversible memory, CFG349_MUTATE=1).
DE12's transition() and L341's growth harness are exec'd read-only (no file of theirs is written).
"""
import os, sys, json, math, io, contextlib, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG349_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "CFG349", "mutate": MUTATE, "checks": {}, "numbers": {}}
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
    P("\n  *** CFG349_MUTATE=1: REVERSIBLE memory -- u.dm = Gamma_b [H(-theta)(1 - m) - (1 - H(-theta)) m] ***")


def ratchet_rate(theta, m, Gam):
    """dm/dtau for the frozen ratchet (or the reversible MUTATE)."""
    on = 1.0 if theta <= 0.0 else 0.0
    if MUTATE:
        return Gam * (on * (1 - m) - (1 - on) * m)
    return Gam * on * (1 - m)


# ------------------------------------------------------------------ record machinery, read-only (as CFG347)
P_DE12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
NS = {"__name__": "de12_readonly", "__file__": P_DE12}
_src = open(P_DE12).read().split('banner("G1 G2')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
G, KPC, MS, FB, CS, transition, host = [NS[k] for k in ("G", "KPC", "MS", "FB", "CS", "transition", "host")]
H0, Om, rho_crit0, A0, Hz = NS["H0"], NS["Om"], NS["rho_crit0"], NS["A0"], NS["Hz"]
CL = 299792458.0
GYR = 3.15576e16
ZS, MBS, FOOTS = (0.25, 1.0, 2.5, 4.0), (1e10, 1e11, 1e12), ("canonical", "alt")
HOSTS = [(z, Mb, f) for z in ZS for Mb in MBS for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
with contextlib.redirect_stdout(io.StringIO()):
    TRS = {KEY(*hk): transition(hk[0], hk[1], hk[2], 0.25) for hk in HOSTS}
r30 = 30 * KPC
rhom = lambda z: Om * rho_crit0 * (1 + z) ** 3


def menc_nfw(Mb, z, r):
    hs = host(Mb, z)
    x = r / hs["rs"]
    return 4 * math.pi * hs["rho_s"] * hs["rs"] ** 3 * (math.log(1 + x) - x / (1 + x))


def r_ta(z, Mb):
    """CFG347's turnaround radius: mean enclosed density (NFW + mean) = 5.55 rho_m-bar(z)."""
    hs = host(Mb, z); rb = rhom(z)
    fn = lambda lr: (menc_nfw(Mb, z, math.exp(lr)) / (4 / 3 * math.pi * math.exp(lr) ** 3) + rb) - 5.55 * rb
    return math.exp(brentq(fn, math.log(hs["r200"]), math.log(1e3 * hs["r200"])))


def t_of_z(z):
    return quad(lambda zz: 1.0 / ((1 + zz) * Hz(zz)), z, np.inf, limit=200)[0]


P(f"\n  DE12 transition() loaded read-only (24 hosts); f_b = {FB:.4f}; c_s(1e6 K) = {CS['1e6K']/1e3:.0f} km/s")

# ============================================================================== S / legality
banner("L  LEGALITY: the two actions (sympy on the parcel reduction V(t), m(t), lambda(t))")
t = sp.symbols("t", real=True)
V, m, lam = (sp.Function(n)(t) for n in ("V", "m", "lam"))
Mi, Gm, w = sp.symbols("M Gamma w", positive=True)
Sstep = sp.Function("S")          # smoothed version of H (width w) so the second variation exists; H is the w -> 0 limit
fm = sp.Function("f")
LM = sp.Function("L_M")
th = sp.diff(V, t) / V            # parcel expansion (1D proxy of theta_b)
L_ord = sp.Rational(1, 2) * Mi * sp.diff(V, t) ** 2 + fm(m) * LM(V) + lam * (sp.diff(m, t) - Gm * Sstep(-th / w) * (1 - m))
EL = {q: sp.simplify(sp.diff(L_ord, q) - sp.diff(sp.diff(L_ord, sp.diff(q, t)), t)) for q in (V, m, lam)}
lam_eq = sp.solve(EL[m], sp.diff(lam, t))[0]
P(f"  L-ord: delta lambda -> the ratchet: {sp.simplify(EL[lam])} = 0")
P(f"  L-ord: delta m      -> lambda' = {sp.simplify(lam_eq)}")
# Liouville partner: d/dt[lambda (1 - m)] on shell
mdot = Gm * Sstep(-th / w) * (1 - m)
partner = sp.simplify(sp.diff(lam * (1 - m), t).subs({sp.diff(lam, t): lam_eq, sp.diff(m, t): mdot}))
P(f"  L-ord: d/dt[lambda (1 - m)] = {partner}   (unsourced: lambda = const/(1 - m) -> diverges as m -> 1)")
Meff = sp.simplify(sp.diff(L_ord, sp.diff(V, t), 2))
P(f"  L-ord: parcel inertia d2L/dVdot2 = {Meff}")
qd = [sp.diff(q, t) for q in (V, m)]
E_ord = sp.simplify(sum(qq * sp.diff(L_ord, qq) for qq in qd) - L_ord)
P(f"  L-ord: energy function E = {E_ord}")
lin_in_lam = sp.simplify(sp.diff(E_ord, lam, 2)) == 0 and sp.simplify(sp.diff(E_ord, lam)) != 0
# CTP physical limit: static 1D MOND-type field with a position-dependent f(x): stress-divergence residual
x = sp.symbols("x", real=True)
Phi = sp.Function("Phi")(x); fx = sp.Function("fx")(x); F = sp.Function("F"); rho = sp.Function("rho")(x)
Lf = -fx * F(sp.diff(Phi, x) ** 2) - rho * Phi
fieldeq = sp.diff(sp.diff(Lf, sp.diff(Phi, x)), x) - sp.diff(Lf, Phi)    # = 0 on shell
Txx = sp.diff(Phi, x) * sp.diff(Lf, sp.diff(Phi, x)) - (Lf + rho * Phi)  # field stress (baryon term excluded)
resid = sp.simplify(sp.diff(Txx, x) - (-rho * sp.diff(Phi, x)) * 0 - sp.diff(Phi, x) * fieldeq)
P(f"  L-CTP (physical limit, static): dT_field/dx - Phi' (field eq) = {sp.simplify(resid)}")
P("          = (force on baryons) + (-f' F): the extra -f'(x) F term is a non-conserved momentum where m varies (Bianchi residual)")
bianchi_term = sp.simplify(resid + sp.diff(Phi, x) * rho)   # remove the baryon force -rho Phi'
P(f"          residual after the baryon force: {bianchi_term}")
leg = dict(L_ord_lambda_partner=str(partner), L_ord_inertia=str(Meff), L_ord_energy_linear_in_lambda=bool(lin_in_lam),
           L_CTP_residual=str(bianchi_term))
P("  L2 diff-safety: every term (u_b.dm, u_b.dT, theta_b = nabla.u_b, rho_b, f(m) L_M) is a spacetime scalar on the leaves -> diff-safe (CFG329's method: no leaf-dependent non-scalar enters).")

# ============================================================================== (a) FRW
banner("(a) FRW + LINEAR PERTURBATIONS")
# A1: integrate the ratchet along FRW parcels with perturbed expansion theta = 3H(1 + d), d in (-1, 1)
a1 = []
for d in (-0.99, -0.9, -0.5, 0.0, 0.5):
    mm = 0.0
    zgrid = np.concatenate([np.geomspace(1000, 0.01, 3000), [0.0]])
    for i in range(len(zgrid) - 1):
        z1, z2 = zgrid[i], zgrid[i + 1]
        dtau = (z1 - z2) / ((1 + z1) * Hz(z1))
        thv = 3 * Hz(z1) * (1 + d)
        Gb = math.sqrt(4 * math.pi * G * FB * rhom(z1))
        mm = 1 - (1 - mm) * math.exp(-Gb * dtau * (1.0 if thv <= 0 else 0.0)) if not MUTATE else mm + dtau * ratchet_rate(thv, mm, Gb)
    a1.append((d, mm))
a1_ok = all(v == 0.0 for _, v in a1)
check("A1 (a) m = 0 EXACTLY along FRW parcels with theta = 3H(1 + d), d in {-0.99..0.5} (finite OFF neighbourhood |d| < 1)",
      "; ".join(f"d={d}: m={v}" for d, v in a1), a1_ok)
# A2: turnaround thresholds
eta = sp.symbols("eta", positive=True)
Rth = 1 - sp.cos(eta); tth = eta - sp.sin(eta)
theta_th = 3 * sp.diff(Rth, eta) / sp.diff(tth, eta) / Rth
eta_ta = sp.nsolve(sp.numer(sp.together(theta_th)), eta, 3.0)
dlin_sph = float(sp.Rational(3, 20) * (6 * sp.pi) ** sp.Rational(2, 3))
P(f"  sympy: top-hat theta = 0 at eta = {float(eta_ta):.6f} (pi = {math.pi:.6f}); delta_lin,ta = (3/20)(6 pi)^(2/3) = {dlin_sph:.4f}")


def growth_f(z):
    a = 1 / (1 + z); OmA = Om / a ** 3 / (Om / a ** 3 + 1 - Om)
    return OmA ** 0.55


sheet = {z: 3 / (3 + growth_f(z)) for z in (0, 1, 4, 100)}
lin_pos = min(1 - growth_f(z) * 0.1 / 3 for z in (0, 0.5, 1, 4, 100))
P(f"  Zel'dovich sheet thresholds delta_lin = 3/(3+f): " + ", ".join(f"z={z}: {v:.3f}" for z, v in sheet.items()))
P(f"  linear parcels delta_lin <= 0.1: min theta_b/3H = {lin_pos:.4f} > 0 -> never triggered")
a2_ok = lin_pos > 0 and dlin_sph >= 0.5 and min(sheet.values()) >= 0.5 and abs(float(eta_ta) - math.pi) < 1e-8
check("A2 (a) linear parcels (delta <= 0.1) have theta_b > 0; turnaround needs delta_lin = 1.062 (sphere) / 3/(3+f) (sheet) >= 0.5",
      f"min theta/3H {lin_pos:.4f}; sphere {dlin_sph:.4f}; sheet min {min(sheet.values()):.3f}", a2_ok)
OUT["numbers"]["a"] = dict(A1=a1, sphere=dlin_sph, sheet=sheet, lin_min_theta_ratio=lin_pos)
# A3: L341 growth with the switch value m = 0
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


def growth(foot, fFRW, z_i=1000.0):
    a_i = 1 / (1 + z_i)
    sL = solve_ivp(lambda N, Y: [Y[1], 1.5 * (Om / math.exp(3 * N) / Ez(math.exp(N)) ** 2) * Y[0] - (2 + dlnH(math.exp(N))) * Y[1]],
                   (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    Di = DREF / sL.sol(0.0)[0]

    def grms(a, D):
        gk = 4 * math.pi * G * Om * rho_crit0 / a ** 3 * np.abs(Di * D) / (KH * h / (a * Mpc))
        return math.sqrt(trapz(gk ** 2 / KH, KH) / trapz(1 / KH, KH))

    def rhs(N, Y):
        a = math.exp(N); D, Dp = Y
        boost = 1.0 + fFRW(a) * (nu_mono(grms(a, D) / A0H[foot]) - 1.0)
        return [Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * boost * D - (2 + dlnH(a)) * Dp]
    s = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    return s.sol(0.0)[0] / sL.sol(0.0)[0], sigma8_of(Di * s.sol(0.0)[0])


m_frw = a1[3][1]
gr = {f: growth(f, lambda a: m_frw) for f in FOOTS}
a3_ok = all(abs(v[0] - 1) < 1e-6 for v in gr.values())
check("A3 (a) L341 growth with f = m_FRW: D/D_LCDM = 1 within 1e-6",
      "; ".join(f"{f}: D ratio {v[0]:.8f}, sigma_8 {v[1]:.4f}" for f, v in gr.items()), a3_ok)
a_ok = a1_ok and a2_ok and a3_ok

# ============================================================================== (b) bound
banner("(b) BOUND SYSTEMS: ON at 30 kpc (conservative exponent), fidelity, no flicker")
brow = []
for hk in HOSTS:
    z, Mb, f = hk; tr = TRS[KEY(*hk)]
    i = int(np.searchsorted(tr["r"], r30))
    rho_enc = menc_nfw(Mb, z, r30) / (4 / 3 * math.pi * r30 ** 3) + rhom(z)
    out = {}
    for lab, X, duty in (("cons", 44.4, 0.5), ("len", 5.55, 1.0)):
        zta = (rho_enc / (X * rhom(0))) ** (1 / 3) - 1
        if zta <= z:
            E = 0.0
        else:
            Gta = math.sqrt(4 * math.pi * G * FB * 5.55 * rhom(zta))
            E = duty * Gta * (t_of_z(z) - t_of_z(zta))
        out[lab] = dict(z_ta=zta, E=E, m=1 - math.exp(-E))
    mc = out["cons"]["m"]
    gN = G * Mb * MS / r30 ** 2; g = float(np.interp(r30, tr["r"], tr["g"])); gph = g - gN
    yv = tr["y"][i]
    rph = max(Mb * MS * (NS["h_of"](yv) - yv * NS["dh_of"](yv)) / (2 * math.pi * r30 ** 3 * yv), 0.0)
    rb = tr["rho_b"][i]
    devs = []
    for kk in (1 / KPC, 1 / (10 * KPC)):
        A = CS["1e6K"] ** 2 * kk ** 2 - 4 * math.pi * G * (rb / FB + rph)
        devs.append((1 - mc) * (4 * math.pi * G * rph + abs(gph) * kk) / abs(A))
    brow.append(dict(host=KEY(*hk), z_ta_cons=out["cons"]["z_ta"], E_cons=out["cons"]["E"], m_cons=mc,
                     m_len=out["len"]["m"], dev=max(devs), dev_k1=devs[0], dev_k10=devs[1]))
for r in brow:
    P(f"  {r['host']:22s} z_ta(cons) {r['z_ta_cons']:6.2f}  E {r['E_cons']:6.2f}  m_cons {r['m_cons']:.4f}  m_len {r['m_len']:.4f}  dev {r['dev']:.2e}")
b1_ok = all(r["m_cons"] >= 0.9 for r in brow)
n_on = sum(r["m_cons"] >= 0.9 for r in brow)
check("B1 (b) ON: f = m >= 0.9 at 30 kpc on all 24 hosts (conservative exponent: 44.4 rho-bar, duty 1/2, Gamma at turnaround density)",
      f"{n_on}/24 ON; m_cons {min(r['m_cons'] for r in brow):.4f}-{max(r['m_cons'] for r in brow):.6f}; lenient m {min(r['m_len'] for r in brow):.4f}-{max(r['m_len'] for r in brow):.6f}", b1_ok)
b2_ok = all(r["dev"] <= 0.1 for r in brow)
check("B2 (b) fidelity: gas compressive mode changes <= 10% (delta f <= 1 - m, worst case) at k = 1/kpc, 1/10 kpc on all 24 hosts",
      f"dev {min(r['dev'] for r in brow):.2e}-{max(r['dev'] for r in brow):.2e}; passing {sum(r['dev'] <= 0.1 for r in brow)}/24", b2_ok)

# B3: no flicker. 10 cycles of a 10% compression at Omega(30 kpc), starting from the host's m_cons
fl = []
for hk, r in zip(HOSTS, brow):
    z, Mb, f = hk; tr = TRS[KEY(*hk)]
    g = float(np.interp(r30, tr["r"], tr["g"])); Om30 = math.sqrt(g / r30)
    rb = tr["rho_b"][int(np.searchsorted(tr["r"], r30))]
    lnr = lambda tt: 0.5 * math.log(1.1) * (1 - math.cos(Om30 * tt))
    thf = lambda tt: -0.5 * math.log(1.1) * Om30 * math.sin(Om30 * tt)
    Gb = lambda tt: math.sqrt(4 * math.pi * G * rb * math.exp(lnr(tt)))
    T = 10 * 2 * math.pi / Om30
    sol = solve_ivp(lambda tt, y: [ratchet_rate(thf(tt), y[0], Gb(tt))], (0, T), [r["m_cons"]], max_step=T / 4000, rtol=1e-11, atol=1e-14)
    mt = sol.y[0]
    drop = float(np.max(np.maximum.accumulate(mt) - mt))
    late = mt[sol.t > T * 0.8]
    fl.append(dict(host=r["host"], drop=drop, m_start=r["m_cons"], m_end=float(mt[-1]), late_pp=float(np.ptp(late)), late_mean=float(np.mean(late))))
maxdrop = max(v["drop"] for v in fl)
P(f"  flicker test: max drop {maxdrop:.3e}; late peak-to-peak {min(v['late_pp'] for v in fl):.2e}-{max(v['late_pp'] for v in fl):.2e}; "
  f"late mean m {min(v['late_mean'] for v in fl):.4f}-{max(v['late_mean'] for v in fl):.4f}")


# CFG242's probe shell (GM = 1, softening 0.05; t_dyn(q=1) = 1) with the ratchet; rate = baryonic sqrt(4 pi G f_b rho_enc)
EPS, GM1 = 0.05, 1.0


def shell_rhs(tt, y, mode):
    xq, v, n = y
    q = math.sqrt(xq * xq + EPS ** 2)
    thb = 3 * (xq * v / q) / q
    a = -GM1 * xq / (xq * xq + EPS ** 2) ** 1.5
    if mode == "E3":                      # CFG242 frozen latch E3 (control K1)
        u = -thb / (3 * 0.01)
        s1 = 0.0 if u <= 0 else (1.0 if u >= 1 else 3 * u * u - 2 * u ** 3)
        tau_n = math.sqrt(4 * math.pi * q ** 3 / (3 * GM1))
        return [v, a, (s1 * (1 - n) - (1 - s1) * n) / tau_n]
    Gam = 0.0 if mode == "zero" else math.sqrt(3 * FB * GM1 / q ** 3)
    return [v, a, ratchet_rate(thb, n, Gam)]


tff = math.pi / (2 * math.sqrt(2))
tt = np.linspace(0, 120, 24001)
shell = {}
for mode in ("E3", "R", "zero"):
    s = solve_ivp(lambda t_, y: shell_rhs(t_, y, mode), (0, 120), [1.0, 0.0, 0.0], method="LSODA", rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.05)
    nb = s.sol(tt)[2]; ia = np.searchsorted(tt, tff)
    shell[mode] = dict(n_tff=float(nb[ia]), n_min_after=float(np.min(nb[ia:])), drop=float(np.max(np.maximum.accumulate(nb) - nb)),
                       t99=float(tt[np.argmax(nb >= 0.99)]) if np.any(nb >= 0.99) else float("inf"), n_end=float(nb[-1]), nmax=float(np.max(np.abs(nb))))
P(f"  probe shell, ratchet: m(t_ff) = {shell['R']['n_tff']:.4f}; first m >= 0.99 at t = {shell['R']['t99']:.2f} t_dyn "
  f"({shell['R']['t99']/tff:.2f} t_ff); max drop {shell['R']['drop']:.2e}; m(120) = {shell['R']['n_end']:.6f}")
b3_ok = maxdrop <= 1e-12 and shell["R"]["drop"] <= 1e-12
check("B3 (b) no flicker: m non-decreasing under 10 compression cycles on all 24 hosts and on CFG242's probe shell (drop <= 1e-12)",
      f"hosts max drop {maxdrop:.2e}; probe shell drop {shell['R']['drop']:.2e}", b3_ok,
      "a ratchet has no decay term, so a compression can only raise m (Lean R1)")
# B3 post-hoc (LABELLED, not scored): the frozen 1e-12 line is below LSODA's noise near m = 1. Integrate the orbit only,
# then apply the EXACT step solution m' = 1 - (1 - m) exp(-Gamma dt chi) (chi = 1 if theta <= 0) on the dense grid.
so = solve_ivp(lambda t_, y: shell_rhs(t_, [y[0], y[1], 0.0], "zero")[:2], (0, 120), [1.0, 0.0], method="LSODA", rtol=1e-10, atol=1e-13, dense_output=True, max_step=0.05)
xs, vs = so.sol(tt)
mex = np.zeros_like(tt)
for j in range(len(tt) - 1):
    q = math.sqrt(xs[j] ** 2 + EPS ** 2); thj = 3 * (xs[j] * vs[j] / q) / q
    if MUTATE:
        mex[j + 1] = mex[j] + (tt[j + 1] - tt[j]) * ratchet_rate(thj, mex[j], math.sqrt(3 * FB * GM1 / q ** 3))
    else:
        mex[j + 1] = 1 - (1 - mex[j]) * math.exp(-math.sqrt(3 * FB * GM1 / q ** 3) * (tt[j + 1] - tt[j]) * (1.0 if thj <= 0 else 0.0))
drop_ex = float(np.max(np.maximum.accumulate(mex) - mex))
P(f"  B3-posthoc (labelled, not scored): probe shell with the exact step update: max drop {drop_ex:.1e}; m(t_ff) = {mex[np.searchsorted(tt, tff)]:.4f}; "
  + (f"the frozen-line miss ({shell['R']['drop']:.1e}) is integrator noise near m = 1" if drop_ex == 0 else "the drop is real (reversible memory)"))
OUT["numbers"]["B3_posthoc_exact_drop"] = drop_ex
b_ok = b1_ok and b2_ok and b3_ok
OUT["numbers"]["b"] = dict(rows=brow, flicker=fl, shell=shell)

# sensitivity rates (reported, not scored): E with Gamma = H(z_host) and a0/c over (t_host - t_ta), duty 1/2
sens = {}
for lab in ("H", "a0/c"):
    ms_ = []
    for hk, r in zip(HOSTS, brow):
        z, Mb, f = hk
        if r["z_ta_cons"] <= z:
            ms_.append(0.0); continue
        Gm_ = Hz(z) if lab == "H" else A0[f] / CL
        ms_.append(1 - math.exp(-0.5 * Gm_ * (t_of_z(z) - t_of_z(r["z_ta_cons"]))))
    sens[lab] = (min(ms_), max(ms_), sum(v >= 0.9 for v in ms_))
    P(f"  sensitivity (not scored): Gamma = {lab:5s}: m(30 kpc) {sens[lab][0]:.3f}-{sens[lab][1]:.3f}; ON (>= 0.9) {sens[lab][2]}/24")
OUT["numbers"]["sensitivity"] = sens

# ============================================================================== (c) transition
banner("(c) TRANSITION: ghost, characteristics, strong hyperbolicity, Hadamard, edge sharpness")
rho0, cs, k, om = sp.symbols("rho0 c_s k omega", positive=True)
v0 = sp.symbols("v0", real=True)
# principal symbol (comoving frame) of (drho, dv_par, dv_perp1, dv_perp2, dm); the H(-theta) source is bounded -> not principal
Msym = sp.Matrix([[0, rho0 * k, 0, 0, 0],
                  [cs ** 2 * k / rho0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]])
ev = Msym.eigenvects()
nvec = sum(len(e[2]) for e in ev)
speeds = sorted([sp.simplify(e[0] / k) for e in ev for _ in range(e[1])], key=str)
P(f"  principal symbol eigenvalues/k: {speeds}; independent eigenvectors {nvec}/5")
Mdust = Msym.subs(cs, 0)
nd = sum(len(e[2]) for e in Mdust.eigenvects())
Mdust_noM = Mdust[:2, :2]
ndn = sum(len(e[2]) for e in Mdust_noM.eigenvects())
P(f"  dust limit (c_s = 0): eigenvectors {nd}/5 (Jordan block); dust ALONE without m: {ndn}/2 -> the same block (the ratchet adds none)")
# the CFG242-type (principal) coupling, for contrast: a slaved/smoothed trigger S(-theta/w) puts Gamma(1-m)S'/w k into the m row
aa = sp.symbols("a", positive=True)
Mslav = Msym.copy(); Mslav[4, 1] = aa * k
ns = sum(len(e[2]) for e in Mslav.eigenvects())
P(f"  contrast: a smoothed trigger (principal m-v entry a k) -> eigenvectors {ns}/5 for c_s > 0 (still diagonalizable: eigenvalue 0 of m is distinct from +-c_s k)")
# ghost: the baryon kinetic coefficient in the physical limit
vv = sp.symbols("v", real=True); mm_ = sp.symbols("m", real=True)
Lb = sp.Rational(1, 2) * rho0 * vv ** 2 + fm(mm_) * LM(rho0)
kin = sp.diff(Lb, vv, 2)
c1_ok = sp.simplify(kin - rho0) == 0
check("C1 (c) no ghost: baryon kinetic coefficient in the physical limit = rho (f(m) has no velocity dependence)", f"d2L/dv2 = {kin}", c1_ok)
c2_ok = all(sp.im(s_) == 0 for s_ in speeds) and set(speeds) == {0, cs, -cs}
check("C2 (c) characteristics: real speeds {0 (m, along u_b), 0, 0, +-c_s}", f"{speeds}", c2_ok)
c3_ok = nvec == 5
check("C3 (c) strongly hyperbolic for c_s > 0 (5 independent eigenvectors; CFG242's BIMOND failure was weak hyperbolicity)",
      f"{nvec}/5; dust {nd}/5 = dust alone {ndn}/2 + 3 (inherited, not added)", c3_ok)
# Hadamard: linear system y = (delta, delta', dm) on the ON side, worst-sign coupling, on every host at 30 kpc
had = []
for hk, r in zip(HOSTS, brow):
    z, Mb, f = hk; tr = TRS[KEY(*hk)]
    i = int(np.searchsorted(tr["r"], r30)); rb = tr["rho_b"][i]
    yv = tr["y"][i]
    rph = max(Mb * MS * (NS["h_of"](yv) - yv * NS["dh_of"](yv)) / (2 * math.pi * r30 ** 3 * yv), 0.0)
    gph = float(np.interp(r30, tr["r"], tr["g"])) - G * Mb * MS / r30 ** 2
    GJ2 = 4 * math.pi * G * (rb / FB + rph); Gb = math.sqrt(4 * math.pi * G * rb)
    worst = 0.0
    for kk in np.geomspace(1e-3, 1e3, 400) / KPC:
        A = CS["1e6K"] ** 2 * kk ** 2 - GJ2
        for sg in (1, -1):
            Mx = np.array([[0, 1, 0], [-A, 0, -sg * kk * abs(gph)], [0.5 * Gb * (1 - r["m_cons"]), 0, -Gb]])
            worst = max(worst, float(np.max(np.linalg.eigvals(Mx).real)) / (math.sqrt(GJ2) + Gb))
    had.append(worst)
c4_ok = max(had) <= 1.0 + 1e-9
check("C4 (c) Hadamard: max linear growth rate over k in [1e-3, 1e3]/kpc <= Gamma_Jeans + Gamma_b on all 24 hosts",
      f"max ratio {max(had):.4f}", c4_ok)
c_ok = c1_ok and c2_ok and c3_ok and c4_ok
# edge sharpness: top-hat infall from turnaround (R_ta = 1): dE/deta = sqrt(3 f_b/8) (2/(1 - cos eta))^(3/2) (1 - cos eta)
dE = lambda e: math.sqrt(3 * FB / 8) * (2 / (1 - math.cos(e))) ** 1.5 * (1 - math.cos(e))
etas = np.linspace(math.pi, 1.999 * math.pi, 20001)
Ecum = np.concatenate([[0], np.cumsum(0.5 * (np.array([dE(e) for e in etas[1:]]) + np.array([dE(e) for e in etas[:-1]])) * np.diff(etas))])
mcur = 1 - np.exp(-Ecum)
Rcur = (1 - np.cos(etas)) / 2
tcur = (etas - np.sin(etas) - math.pi) / math.pi        # in units of the turnaround->collapse free-fall time (pi B)
edge = {}
for mv in (0.1, 0.5, 0.9):
    j = int(np.argmax(mcur >= mv)); edge[mv] = dict(R_over_Rta=float(Rcur[j]), t_over_tff=float(tcur[j]))
mvir = float(mcur[int(np.argmax(Rcur <= 0.5))])
RTA = {KEY(*hk): r_ta(hk[0], hk[1]) for hk in HOSTS}
w_kpc = [RTA[KEY(*hk)] * (edge[0.5]["R_over_Rta"] - edge[0.9]["R_over_Rta"]) / KPC for hk in HOSTS]
P(f"  edge (top-hat, ratchet exponent with Gamma_b): m = 0.1 / 0.5 / 0.9 at R/R_ta = {edge[0.1]['R_over_Rta']:.3f} / "
  f"{edge[0.5]['R_over_Rta']:.3f} / {edge[0.9]['R_over_Rta']:.3f}; t/t_ff = {edge[0.1]['t_over_tff']:.3f} / {edge[0.5]['t_over_tff']:.3f} / {edge[0.9]['t_over_tff']:.3f}")
P(f"  m at virialisation (R = R_ta/2, first infall only) = {mvir:.4f}; radial edge width (m 0.5 -> 0.9) = {min(w_kpc):.0f}-{max(w_kpc):.0f} kpc "
  f"(r_ta {min(RTA.values())/KPC:.0f}-{max(RTA.values())/KPC:.0f} kpc): the edge sits at the turnaround shell, outside 30 kpc")
OUT["numbers"]["c"] = dict(speeds=[str(s_) for s_ in speeds], nvec=nvec, dust=nd, hadamard_max=max(had), edge=edge, m_vir=mvir,
                           edge_width_kpc=[min(w_kpc), max(w_kpc)])

# legality numbers: CTP Bianchi residual size at 30 kpc today and during switch-on; |L_M| ~ g_ph^2/(8 pi G), |grad f| ~ (1-m)/r
bz = []
for hk, r in zip(HOSTS, brow):
    z, Mb, f = hk; tr = TRS[KEY(*hk)]
    i = int(np.searchsorted(tr["r"], r30)); rb = tr["rho_b"][i]
    g = float(np.interp(r30, tr["r"], tr["g"])); gph = g - G * Mb * MS / r30 ** 2
    LMv = gph ** 2 / (8 * math.pi * G)
    bz.append(((1 - r["m_cons"]) * LMv / r30 / (rb * g), LMv / r30 / (rb * g)))
P(f"  L-CTP Bianchi residual |L_M grad f|/(rho_b g) at 30 kpc: today {min(b[0] for b in bz):.2e}-{max(b[0] for b in bz):.2e}; "
  f"during switch-on (|grad f| ~ 1/r) {min(b[1] for b in bz):.2e}-{max(b[1] for b in bz):.2e}")
leg["CTP_residual_today"] = [min(b[0] for b in bz), max(b[0] for b in bz)]
leg["CTP_residual_switch_on"] = [min(b[1] for b in bz), max(b[1] for b in bz)]
legal_ok = False
leg_reason = ("L-ord: energy linear in lambda (unbounded), lambda = const/(1-m) diverges as m -> 1, and the parcel inertia gets "
              "lambda Gamma (1-m) S''/(w^2 V^2) (indefinite sign; a delta at theta_b = 0 for the sharp H); L-CTP: causal and ghost-free "
              "but non-conservative (Bianchi residual -f' F where m varies)")
OUT["legality"] = dict(leg, pass_=legal_ok, reason=leg_reason)

# ============================================================================== ownership
banner("OWNERSHIP (reported): FG001 classes from the ratchet")
own = {}
# class A: satellite that turned around on its own (m_sat) is accreted (theta alternates); ratchet keeps m >= m_sat
own["A"] = dict(m_before=0.95, m_after=1 - (1 - 0.95) * math.exp(-1.0), on=True)
# class E: a cluster/binary formed from host gas that already has m_host; it inherits m_host (a Lagrangian label)
own["E"] = dict(m_host=min(r["m_cons"] for r in brow if r["m_cons"] > 0), inherited=True)
P(f"  class A (accreted top-level): keeps its own ON state (m non-decreasing: {own['A']['m_before']} -> {own['A']['m_after']:.3f})")
P(f"  class E (formed embedded): inherits the host gas's m (>= {own['E']['m_host']:.3f} where the host is ON) -> ON, not Newtonian;"
  " the ratchet carries one number per parcel and both classes have the same history bit -> FG001's class E is NOT reproduced"
  " (this is CFG251's (iii-a) 'inherit' reading)")
P("  field baryons that never turned around (voids, filaments at delta_lin < 0.75): m = 0 exactly; ejected gas keeps m (ratchet)")
OUT["numbers"]["ownership"] = dict(A="reproduced (keeps own ON)", E="NOT reproduced (inherits host ON; record says Newtonian)")

# ============================================================================== controls
banner("CONTROLS")
k1 = shell["E3"]
k1_ok = abs(k1["n_tff"] - 0.791) / 0.791 < 0.01 and abs(k1["n_min_after"] - 0.143) / 0.143 < 0.01
check("K1 CONTROL: CFG242's frozen latch E3 on its probe shell: n(t_ff) = 0.791, min n (t >= t_ff) = 0.143, within 1%",
      f"n(t_ff) = {k1['n_tff']:.4f}; min after = {k1['n_min_after']:.4f}; static decay time 2.05 = sqrt(4 pi/3) = {math.sqrt(4*math.pi/3):.3f}", k1_ok)
k2_ok = shell["zero"]["nmax"] == 0.0
check("K2 CONTROL: Gamma = 0 -> m = 0 for all time -> f = 0: Newtonian (exact)", f"max |m| = {shell['zero']['nmax']}", k2_ok)
if MUTATE:
    P(f"  MUTATE (reversible): host late mean m {min(v['late_mean'] for v in fl):.4f}-{max(v['late_mean'] for v in fl):.4f}, "
      f"late peak-to-peak {max(v['late_pp'] for v in fl):.3e}; probe shell min m after t_ff {shell['R']['n_min_after']:.4f}")

# ============================================================================== verdict
banner("VERDICT (frozen rule)")
ncon = 0
tier = ("MEMORY SWITCH WORKS" if (a_ok and b_ok and c_ok and ncon == 0) else "WITH COST" if (a_ok and b_ok and c_ok)
        else "PARTIAL" if (a_ok + b_ok + c_ok) == 2 else "NO-GO")
suffix = "LEGALITY PASS" if legal_ok else f"LEGALITY FAIL ({leg_reason})"
P(f"  (a) {'PASS' if a_ok else 'FAIL'}  (b) {'PASS' if b_ok else 'FAIL'}  (c) {'PASS' if c_ok else 'FAIL'}; new constants {ncon}")
P(f"  VERDICT: {tier}, {suffix}")
OUT["verdict"] = dict(a=a_ok, b=b_ok, c=c_ok, constants=ncon, tier=tier, legality=suffix)
P(f"\n  elapsed {time.time() - T0:.1f} s")
json.dump(OUT, open(os.path.join(HERE, f"cfg349_memory_switch_results{SUF}.json"), "w"), indent=1, default=str)
P("  checks: " + ", ".join(f"{n.split()[0]} {'PASS' if ok else 'FAIL'}" for n, ok in CH))
sys.exit(1 if (MUTATE and not b3_ok) else 0)
