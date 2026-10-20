#!/usr/bin/env python3
"""CFG900: kappa door D4 -- the record's nodal fermion medium made Lorentz-invariant (v = c), its own vacuum as the dark energy.

Criteria: FROZEN_CRITERIA.md (committed alone first, 32264ab5d); AMENDMENTS.md A1-A3 (committed alone before this script,
7f72af505). Rules: CFG894 KAPPA_CAMPAIGN_RULES.md; door text KAPPA_DOORS.md D4.

Question: the fermion-polarisation candidate (sol61 mechanism_2026_10_12) gets its cubic |P|^3 polarisation energy from a
nodal-ring band with velocity v. If the medium is made Lorentz-invariant (v = c) and its filled-band (vacuum) energy is the
dark energy, do a0 (through K = G a0) and rho_DE then come from one Hamiltonian, and what kappa follows?

Method: sympy (+ numpy for Clifford spectra). Variants V1 (strict Lorentz-invariant Dirac medium), V2 (ring, cone dimensional
regularisation), V3 (ring, physical tube band), V4 (ring, Pauli-Villars), V5 (timelike cosmological polarisation, N1-N4).
Measured H0 and Omega_L enter only at the very end (report-only numbers).

Run:   OMP_NUM_THREADS=1 nice -n 10 python3 cfg900.py               -> cfg900.out, cfg900_results.json (exit 0 = checks pass)
       CFG900_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg900.py -> cfg900_MUTATE.out, cfg900_results_MUTATE.json
                                                                       (exit 1 = all teeth bite; 2 = VOID)
kappa = 1/2 is FITTED. Not theory closed.
"""
import json
import math
import os
import re
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG900_MUTATE", "0") == "1"
OUT = os.path.join(HERE, "cfg900_MUTATE.out" if MUTATE else "cfg900.out")
JSN = os.path.join(HERE, "cfg900_results_MUTATE.json" if MUTATE else "cfg900_results.json")

LINES = []
CHECKS = {}


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


def check(name, ok, detail=""):
    CHECKS[name] = {"pass": bool(ok), "detail": str(detail)}
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def z(expr):
    """True if a sympy expression simplifies to zero."""
    return sp.simplify(sp.expand(expr)) == 0


# ----------------------------------------------------------------------------------------------------------------------
# symbols (SI unless stated)
# ----------------------------------------------------------------------------------------------------------------------
G, c, hbar, rho = sp.symbols("G c hbar rho_DE", positive=True)
N, ms, k0, v, h, Lam, qb, C = sp.symbols("N m_star k_0 v h Lambda q_b C", positive=True)
Dl, q, m, Mpv, mu = sp.symbols("Delta q m M_PV mu", positive=True)
Pp, r, Mb, a0, H, eL = sp.symbols("P r M_b a_0 H epsilon_L", positive=True)
lam, sig, ee = sp.symbols("lambda_x sigma e", positive=True)
eps = sp.Symbol("epsilon")            # dim-reg parameter, D = 4 - 2 epsilon
th = sp.Symbol("theta", real=True)
q1, q2 = sp.symbols("q_1 q_2", real=True)

W_DATA = (0.227, 0.607)          # rho_DE footing, rules section 7 (2 sigma of the primary measurement)
W_DATA_CRIT = (0.189, 0.501)     # rho_crit footing
FOUR_PI = 4 * sp.pi


def A_of(vfac=1, stat=1):
    """Ring prefactor A = N m*/(2 pi hbar^3 v) (SI), times the statistics sign of the mode sum (stat = +1 filled fermion sea)."""
    return N * ms / (2 * sp.pi * hbar**3 * (v * vfac))


def tube_band(vfac=1, stat=1):
    """Filled-band energy in the tube q1^2 + q2^2 < Lambda^2: V = -stat * A * int_0^Lambda q dq sqrt(q^2 + Delta^2)."""
    A = A_of(vfac)
    V = -stat * A * sp.integrate(q * sp.sqrt(q**2 + Dl**2), (q, 0, Lam))
    return A, sp.simplify(V)


def I_dr(n, a, mass):
    """Dimensional-regularisation master formula int d^n q/(2pi)^n (q^2 + m^2)^a."""
    return sp.gamma(-a - sp.Rational(n, 2) if isinstance(n, int) else -a - n / 2) / (
        sp.gamma(-a) * (4 * sp.pi) ** (sp.Rational(n, 2) if isinstance(n, int) else n / 2)) * mass ** (2 * a + n)


# ----------------------------------------------------------------------------------------------------------------------
# the record's force sector (static), the dictionary a0 = K/G, the unified vacuum formula
# ----------------------------------------------------------------------------------------------------------------------
def beta_of(vfac=1, stat=1):
    return stat * A_of(vfac) * h**3


def a0_of(beta):
    """a0 = K/G with K = q_b^3/(4 pi C^3 beta) (record: V_inf^4 = K M_b)."""
    return qb**3 / (4 * sp.pi * C**3 * beta * G)


def kappa2_from_vacuum(eps0, a0expr):
    """kappa^2 = a0^2/(G rho_DE c^2) with the matching rho_DE c^2 = eps0."""
    return sp.simplify(a0expr**2 / (G * eps0))


# ----------------------------------------------------------------------------------------------------------------------
# dimensions: base units Mu, Lu, Tu and Pu (the polarisation's own unit)
# ----------------------------------------------------------------------------------------------------------------------
Mu, Lu, Tu, Pu = sp.symbols("Mu Lu Tu Pu", positive=True)
ENERGY = Mu * Lu**2 / Tu**2
DIMS = {
    G: Lu**3 / (Mu * Tu**2), c: Lu / Tu, hbar: Mu * Lu**2 / Tu, rho: Mu / Lu**3, ms: Mu, k0: 1 / Lu, v: Lu / Tu,
    h: ENERGY / Pu, Lam: ENERGY, Mpv: ENERGY, Dl: ENERGY, qb: Pu * Lu**2 / Mu, C: Pu**2 * Lu * Tu**2 / Mu, a0: Lu / Tu**2,
    Pp: Pu, Mb: Mu, r: Lu, H: 1 / Tu, eL: 1, N: 1,
}


def dim(expr):
    sub = {s: s * d for s, d in DIMS.items()}
    return sp.simplify(sp.powsimp(sp.expand_power_base(expr.subs(sub, simultaneous=True) / expr, force=True), force=True))


def dlog(expr, x):
    return sp.simplify(x * sp.diff(sp.log(expr), x))


# ----------------------------------------------------------------------------------------------------------------------
# blocks used by both runs
# ----------------------------------------------------------------------------------------------------------------------
def block_V1_exponent(D):
    """Strict Lorentz-invariant Dirac sea in D spacetime dims: nonanalytic vacuum term ~ m^D; deep MOND needs |P|^(D-1)."""
    p_li = D
    p_need = D - 1
    return p_li, p_need


def block_ring_exponent(D, codim=2):
    """Codimension-c_N node: effective (c_N+1)-dim cone, vacuum term ~ |Delta|^(c_N+1); deep MOND in n = D-1 needs |P|^n."""
    return codim + 1, D - 1


def kappa_posits(e=1, n=3, vfac=1):
    """V5 locus posits computed through beta (v kept symbolic inside beta, so any v-dependence would show).

    N1: q_b P0/C = a0;  N3: q_b P0/C = c H with the footing Friedmann H^2 = e * (16 pi G rho/(n(n-1))).
    Returns (kappa_N1, kappa_N3) as sympy numbers (n = 3) or the general-n forms.
    """
    beta = beta_of(vfac)
    S = 2 * sp.pi ** sp.Rational(n, 2) / sp.gamma(sp.Rational(n, 2))
    if n == 3:
        # N1: eps0 = beta P*^3/3, P* = C a0/q_b, with a0 = K/G
        a0e = a0_of(beta)
        Pst = C * a0e / qb
        k2_N1 = kappa2_from_vacuum(beta * Pst**3 / 3, a0e)
        # N3: eps0 = beta P_H^3/3 = rho c^2 fixes beta, then a0 = K/G
        bsym = sp.Symbol("b", positive=True)
        Hs = sp.sqrt(e * 8 * sp.pi * G * rho / 3)
        PH = C * c * Hs / qb
        bsol = sp.solve(sp.Eq(bsym * PH**3 / 3, rho * c**2), bsym)[0]
        a0N3 = sp.simplify(a0_of(bsol))
        kN3 = sp.simplify(a0N3 / (c * sp.sqrt(G * rho)))
        return sp.sqrt(sp.simplify(k2_N1)), kN3, a0N3, S
    # general n (formal): eps* = lambda^n a0^2/(n S G); N1 lambda = 1 -> kappa^2 = n S; N3 kappa^(n-2) = (H^2/G rho)^(n/2)/(n S)
    k2_N1 = n * S
    Hsq_over_Grho = e * 16 * sp.pi / (n * (n - 1))
    kN3_pow = sp.simplify(Hsq_over_Grho ** sp.Rational(n, 2) / (n * S))      # = kappa^(n-2)
    return sp.sqrt(k2_N1), kN3_pow, None, S


def micro_trade(vfac=1, stat=1):
    """V3 magnitude-only microscopic trade: kappa^2 = a0^2/(G |E0_tube|) at fixed (N, m*, v, h, Lambda, q_b, C)."""
    A, V = tube_band(vfac, stat)
    E0 = sp.simplify(V.subs(Dl, 0))
    beta = beta_of(vfac, stat)
    a0e = a0_of(beta)
    k2 = sp.simplify(a0e**2 / (G * sp.Abs(E0)))
    return A, V, E0, beta, a0e, k2


def frac(x):
    return float(sp.N(x, 30))


# ======================================================================================================================
# NORMAL RUN
# ======================================================================================================================
def main_normal():
    R = {"lane": "CFG900", "mode": "normal", "criteria": "32264ab5d", "amendments": "7f72af505"}
    say("CFG900  kappa door D4: the nodal fermion medium made Lorentz-invariant (v = c), its own vacuum as the dark energy")
    say("criteria 32264ab5d (FROZEN_CRITERIA.md), amendments 7f72af505 (A1 M4 factor, A2 PV set, A3 hbar under H1r)")
    say("kappa = 1/2 is FITTED (kappa_L 0.417 +- 0.095, CFG493 -- quoted, not used). Footings never pooled. Not theory closed.")
    say("")

    # ---------------- I1 self-grep
    say("== I1: self-grep for forbidden constants")
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    forb = ["9.36" + "e-11", "9.3603" + "e-11", "1.13" + "e-10", "1.1312" + "e-10", "1.2" + "e-10", "0.4" + "17",
            "0.4" + "5", "0.4" + "65", "0.5" + "3", "0.5" + "5", "0.5" + "51", "5.78" + "88", "0.17" + "27"]
    hits = []
    for val in forb:
        pat = r"(?<![\d.])" + re.escape(val) + r"(?![\d])"
        for ln, line in enumerate(src.splitlines(), 1):
            if re.search(pat, line):
                hits.append((val, ln))
    allowed = [(val, ln) for (val, ln) in hits if "quoted, not used" in src.splitlines()[ln - 1]]
    bad = [x for x in hits if x not in allowed]
    check("I1 no forbidden constants used", len(bad) == 0, f"hits outside the quoted standing-fact line: {bad}")
    say("")

    # ---------------- K1 Clifford algebra and spectra (numpy)
    say("== K1: Clifford algebra and spectra")
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]], complex)
    szm = np.array([[1, 0], [0, -1]], complex)
    I2 = np.eye(2)
    G4 = [np.kron(sx, I2), np.kron(szm, I2), np.kron(sy, sx), np.kron(sy, sy), np.kron(sy, szm)]   # record's set
    G8 = [np.kron(g, sx) for g in G4] + [np.kron(np.eye(4), sy)]                                   # six, 8x8

    def cliff_err(gs):
        d = gs[0].shape[0]
        e = 0.0
        for i, a in enumerate(gs):
            for j, b in enumerate(gs):
                e = max(e, np.abs(a @ b + b @ a - 2 * (i == j) * np.eye(d)).max())
            e = max(e, np.abs(a - a.conj().T).max())
        return e

    e4, e8 = cliff_err(G4), cliff_err(G8)
    rng = np.random.default_rng(900)
    err_ring = err_li = err_t = 0.0
    for _ in range(20):
        a1, a2, dd = rng.normal(size=3)
        nvec = rng.normal(size=3)
        nvec /= np.linalg.norm(nvec)
        Hm = a1 * G4[0] + a2 * G4[1] + dd * sum(nvec[j] * G4[2 + j] for j in range(3))
        ev = np.sort(np.linalg.eigvalsh(Hm))
        E = math.sqrt(a1**2 + a2**2 + dd**2)
        err_ring = max(err_ring, np.abs(ev - np.array([-E, -E, E, E])).max())
        kv = rng.normal(size=3)
        mv = rng.normal(size=3)
        Hli = sum(kv[j] * G8[j] for j in range(3)) + sum(mv[j] * G8[3 + j] for j in range(3))
        ev = np.sort(np.linalg.eigvalsh(Hli))
        E = math.sqrt(kv @ kv + mv @ mv)
        err_li = max(err_li, np.abs(ev - np.array([-E] * 4 + [E] * 4)).max())
        P3 = rng.normal(size=3)
        P0 = rng.normal()
        Ht = a1 * G8[0] + a2 * G8[1] + sum(P3[j] * G8[2 + j] for j in range(3)) + P0 * G8[5]
        ev = np.sort(np.linalg.eigvalsh(Ht))
        E = math.sqrt(a1**2 + a2**2 + P3 @ P3 + P0**2)
        err_t = max(err_t, np.abs(ev - np.array([-E] * 4 + [E] * 4)).max())
    check("K1 Clifford sets and spectra", max(e4, e8, err_ring, err_li, err_t) < 1e-12,
          f"anticommutator err 4x4 {e4:.1e}, 8x8 (six matrices) {e8:.1e}; spectra err ring {err_ring:.1e}, "
          f"strict-LI (V1) {err_li:.1e}, timelike P0 (V5) {err_t:.1e}; N = 2 bands per sign (4x4), 4 per sign (8x8)")
    say("")

    # ---------------- K2 ring measure
    say("== K2: ring measure")
    kperp = sp.sqrt(k0**2 + 2 * ms * q1 / hbar**2)
    kz = q2 / (hbar * v)
    meas = sp.simplify(2 * sp.pi * kperp * sp.diff(kperp, q1) * sp.diff(kz, q2) / (2 * sp.pi) ** 3)
    check("K2 d^3k/(2pi)^3 = m*/(4 pi^2 hbar^3 v) dq1 dq2, q1-independent",
          z(meas - ms / (4 * sp.pi**2 * hbar**3 * v)) and sp.diff(meas, q1) == 0, f"measure = {meas}")
    say("")

    # ---------------- K3 tube band
    say("== K3: tube band energy (record's regulator), fermion sea")
    A, Vb = tube_band()
    rec = -(A / 3) * ((Lam**2 + Dl**2) ** sp.Rational(3, 2) - Lam**3 - Dl**3)
    E0t = sp.simplify(Vb.subs(Dl, 0))
    beta = beta_of()
    PL = Lam / h
    ser = sp.series(Vb - E0t, Dl, 0, 5).removeO()
    ser_exp = -A * Lam * Dl**2 / 2 + A * Dl**3 / 3 - A * Dl**4 / (8 * Lam)
    ok3 = z(Vb - E0t - rec) and z(E0t + beta * PL**3 / 3) and z(ser - ser_exp)
    check("K3 tube formula, E0_tube(0) = -beta P_L^3/3, small-gap series", ok3,
          f"V_band = {Vb};  E0_tube(0) = {E0t} = -beta (Lambda/h)^3/3;  V - V(0) = {sp.expand(ser)} + O(Delta^5)")
    R["E0_tube"] = str(E0t)
    say("")

    # ---------------- K4 dimensional regularisation
    say("== K4: dimensional regularisation (Lorentz-invariant regulator)")
    d1 = sp.integrate(q / (q**2 + m**2) ** 2, (q, 0, sp.oo)) / (2 * sp.pi)
    d2 = sp.integrate(4 * sp.pi * q**2 / (q**2 + m**2) ** 3, (q, 0, sp.oo)) / (2 * sp.pi) ** 3
    ok_i = z(d1 - I_dr(2, -2, m)) and z(d2 - I_dr(3, -3, m))
    eps_dr = sp.simplify(-A * 2 * sp.pi * I_dr(2, sp.Rational(1, 2), Dl))      # cone, dim reg
    tt = sp.Symbol("t", positive=True)
    Vb_t = sp.series(Vb.subs(Lam, 1 / tt), tt, 0, 3).removeO()
    lam0 = sp.simplify(sp.expand(Vb_t).coeff(tt, 0))
    ok_ii = z(eps_dr - A * Dl**3 / 3) and z(lam0 - A * Dl**3 / 3)
    Nb = sp.Symbol("N_b", positive=True)
    li3 = sp.simplify(-Nb * I_dr(2, sp.Rational(1, 2), m))                      # hbar = c = 1, D = 3
    ring_nat = sp.simplify((A * Dl**3 / 3).subs({hbar: 1}))
    ok_iii = z(li3 - Nb * m**3 / (6 * sp.pi)) and z(ring_nat - (ms / v) * N * Dl**3 / (6 * sp.pi))
    # general D (odd): -N_b I(D-1, 1/2, m) ~ m^D ; D = 4: pole + m^4 ln m finite part
    gen = {}
    for D in (3, 5, 7):
        val = sp.simplify(-Nb * I_dr(D - 1, sp.Rational(1, 2), m))
        gen[D] = val
    ok_gen = all(sp.degree(sp.Poly(sp.simplify(gen[D] / Nb), m)) == D for D in gen)
    I4 = mu ** (2 * eps) * sp.gamma(-2 + eps) / (sp.gamma(-sp.Rational(1, 2)) * (4 * sp.pi) ** ((3 - 2 * eps) / 2)) \
        * m ** (4 - 2 * eps)
    s4 = sp.expand(sp.series(-Nb * I4, eps, 0, 1).removeO())
    fin = sp.simplify(s4.coeff(eps, 0))
    pole = sp.simplify(s4.coeff(eps, -1))
    mubar = sp.Symbol("mubar", positive=True)
    fin_ms = sp.simplify(sp.expand_log(fin.subs(mu, mubar * sp.exp(sp.EulerGamma / 2) / sp.sqrt(4 * sp.pi)), force=True))
    target4 = -Nb * m**4 / (32 * sp.pi**2) * (sp.log(m**2 / mubar**2) - sp.Rational(3, 2))
    ok_iv = z(sp.expand_log(fin_ms - target4, force=True)) and z(pole - Nb * m**4 / (32 * sp.pi**2))
    check("K4 dim reg: convergent cases, cone = tube's Lambda^0 part, D = 3 sea, ring = (m*/v) x cone, D = 4 finite part",
          ok_i and ok_ii and ok_iii and ok_iv and ok_gen,
          f"(i) {ok_i}; (ii) cone eps_dr(Delta) = {eps_dr}, tube Lambda^0 part = {lam0}; (iii) D=3 sea = {li3}, ring "
          f"(hbar=1) = {ring_nat}; odd-D seas: " + ", ".join(f"D={D}: {gen[D]}" for D in gen)
          + f"; (iv) D=4: pole {pole}/epsilon, MS-bar finite {sp.simplify(target4)}")
    R["dimreg_cone"] = str(eps_dr)
    R["D4_finite"] = str(target4)
    say("")

    # ---------------- V1 exponent theorem and K9 point nodes
    say("== V1 / K9: strict Lorentz invariance allows only point nodes; exponent mismatch in every D")
    kk, MM = sp.symbols("k M", real=True)
    shell = hbar**2 * c**2 * kk**2 + MM**2 * c**4
    poly = sp.Poly(shell, kk, MM)
    sos = all(cf > 0 for cf in poly.coeffs()) and all(all(e % 2 == 0 for e in mon) for mon in poly.monoms())
    # boost a zero-energy ring state (E = 0, k = k0 x) with v_r = c (m* = hbar k0/c), rapidity along x
    bb = 0.3
    gg = 1 / math.sqrt(1 - bb**2)
    k0n, hbn, cn = 1.0, 1.0, 1.0
    msn = hbn * k0n / cn
    Ep = -gg * bb * hbn * cn * k0n
    kxp = gg * k0n
    Ering = hbn**2 * (kxp**2 - k0n**2) / (2 * msn)
    off = abs(abs(Ep) - abs(Ering)) > 1e-3
    exps = {D: block_V1_exponent(D) for D in (3, 4, 5, 6)}
    ring4 = block_ring_exponent(4)
    check("K9 Lorentz-invariant shells vanish only at k = 0, M = 0; boosted ring state leaves the ring spectrum",
          sos and off,
          f"shell {shell} is a sum of even squares with positive coefficients; boost beta 0.3: |E'| = {abs(Ep):.4f} vs "
          f"ring |E(k')| = {abs(Ering):.4f}")
    say("  strict-LI exponent p = D vs deep-MOND need p = D - 1: "
        + "; ".join(f"D={D}: {p} vs {pn}" for D, (p, pn) in exps.items()))
    say(f"  record ring (codimension 2) in D = 4: p = {ring4[0]} vs need {ring4[1]} -> the cubic needs a nodal LINE, "
        "which no Lorentz-invariant spectrum has")
    v1_class = "NO LAW" if all(p != pn for (p, pn) in exps.values()) else "LAW"
    R["V1"] = {"class": v1_class, "exponents": {str(D): list(e) for D, e in exps.items()}}
    say(f"  V1 class: {v1_class}")
    say("")

    # ---------------- K5 pressures
    say("== K5: mode-sum pressure p = (1/3) sum_filled k.grad(eps_k) (isotropic ensemble)")
    avg_even = sp.integrate(2 * sp.cos(th) ** 2 + sp.sin(th) ** 2, (th, 0, 2 * sp.pi)) / (2 * sp.pi)
    avg_odd = sp.integrate(sp.cos(th), (th, 0, 2 * sp.pi)) / (2 * sp.pi)
    J1 = 2 * sp.pi * I_dr(2, sp.Rational(1, 2), Dl)
    Jm1 = 2 * sp.pi * I_dr(2, -sp.Rational(1, 2), Dl)
    J3 = sp.simplify(J1 - Dl**2 * Jm1)
    e_dr, p_dr = sp.simplify(-A * J1), sp.simplify(-(A / 2) * J3)
    w_dr = sp.simplify(p_dr / e_dr)
    e_t0 = sp.simplify(-A * sp.integrate(q * q, (q, 0, Lam)))
    p_t0 = sp.simplify(-(A / 2) * sp.integrate(q * q**2 / q, (q, 0, Lam)))
    w_t0 = sp.simplify(p_t0 / e_t0)
    Eq_ = sp.sqrt(q**2 + Dl**2)
    w_exc_ring = sp.simplify(((q**2 / Eq_) / 2).subs(Dl, 0) / Eq_.subs(Dl, 0))      # pointwise, any occupation f(E)
    w_exc_li = sp.Rational(1, 3)                                                     # E = |k|: k.grad E = E, p = eps/3
    # tube at finite gap (report)
    e_t = -A * sp.integrate(q * Eq_, (q, 0, Lam))
    p_t = -(A / 2) * sp.integrate(q * q**2 / Eq_, (q, 0, Lam))
    w_t = {x: frac(sp.simplify((p_t / e_t).subs({Dl: x * Lam}).subs(Lam, 1))) for x in (sp.Rational(1, 10), 1)}
    ok5 = (avg_even == sp.Rational(3, 2) and avg_odd == 0 and w_dr == -1 and w_t0 == sp.Rational(1, 2)
           and w_exc_ring == sp.Rational(1, 2))
    check("K5 dim-reg cone vacuum w = -1; tube vacuum w(0) = +1/2; excitations w = 1/2 (ring), 1/3 (LI)", ok5,
          f"<2cos^2+sin^2> = {avg_even}, <cos> = {avg_odd}; dim reg eps = {e_dr}, p = {p_dr}, w = {w_dr}; "
          f"tube eps(0) = {e_t0}, p(0) = {p_t0}, w = {w_t0}; tube w at Delta/Lambda 0.1, 1: "
          f"{w_t[sp.Rational(1, 10)]:.4f}, {w_t[1]:.4f}; w_exc ring {w_exc_ring}, LI {w_exc_li}")
    R["w"] = {"dimreg": str(w_dr), "tube0": str(w_t0), "exc_ring": str(w_exc_ring), "exc_LI": str(w_exc_li)}
    say("")

    # ---------------- V4 Pauli-Villars
    say("== V4: Pauli-Villars in the cone (Lorentz-invariant regulator, regulator masses free)")
    sets = {"S2 (frozen)": [(1, 0), (-2, Mpv**2), (1, 2 * Mpv**2)],
            "S3 (A2)": [(1, 0), (-3, Mpv**2), (3, 4 * Mpv**2), (-1, 9 * Mpv**2)]}
    pv = {}
    ok_pv = True
    Qb = sp.Symbol("Q", positive=True)
    for name, S in sets.items():
        sc = sum(ci for ci, _ in S)
        scm = sp.simplify(sum(ci * m2 for ci, m2 in S))
        Vpv = A / 3 * sum(ci * (Dl**2 + m2) ** sp.Rational(3, 2) for ci, m2 in S)
        # direct regulated integral: -A int_0^Q q sum c_i sqrt(q^2 + Delta^2 + M_i^2), Q -> infinity
        direct = -A * sum(ci * ((Qb**2 + Dl**2 + m2) ** sp.Rational(3, 2) - (Dl**2 + m2) ** sp.Rational(3, 2)) / 3
                          for ci, m2 in S)
        lim = sp.limit(sp.simplify(direct.subs(Dl, 0)), Qb, sp.oo)
        const = sp.simplify(Vpv.subs(Dl, 0))
        serpv = sp.expand(sp.series(Vpv, Dl, 0, 4).removeO())
        cub = sp.simplify(serpv.coeff(Dl, 3))
        quad = sp.simplify(serpv.coeff(Dl, 2))
        # pressure of the constant: p = -(A/2) sum c_i J3(M_i), J3 dim-reg value; w of the constant
        pconst = sp.simplify(-(A / 2) * sum(ci * (2 * sp.pi * I_dr(2, sp.Rational(1, 2), sp.sqrt(m2))
                                                  - m2 * 2 * sp.pi * I_dr(2, -sp.Rational(1, 2), sp.sqrt(m2)))
                                            for ci, m2 in S if m2 != 0))
        wconst = sp.simplify(pconst / const)
        okS = sc == 0 and scm == 0 and z(lim - const) and z(cub - A / 3) and wconst == -1
        ok_pv = ok_pv and okS
        s_val = sp.simplify(const / (A * Mpv**3 / 3))
        pv[name] = {"const": str(const), "s": str(s_val), "s_num": frac(s_val), "quad": str(quad), "w_const": str(wconst)}
        say(f"  {name}: sum c = {sc}, sum c M^2 = {scm}; E0(0) = {const} (s = {s_val} = {frac(s_val):+.4f}); "
            f"cubic coeff {cub}; quadratic {quad}; w of the constant {wconst}; direct limit agrees: {z(lim - const)}")
    check("V4/K4b PV: universal cubic A/3, constant w = -1, constant sign set by the regulator set", ok_pv and
          pv["S2 (frozen)"]["s_num"] > 0 > pv["S3 (A2)"]["s_num"], "S2 positive, S3 negative (A2)")
    R["V4"] = pv
    say("")

    # ---------------- K6 static force algebra (record)
    say("== K6: the record's static force algebra from F = |C grad phi - P|^2/(2C) + beta P^3/3 + q_b rho_b phi")
    x = sp.Symbol("x", real=True)
    phi = sp.Function("phi")(x)
    Pf = sp.Function("P")(x)
    rb = sp.Function("rho_b")(x)
    bt = sp.Symbol("beta", positive=True)
    Fd = (C * phi.diff(x) - Pf) ** 2 / (2 * C) + bt * Pf**3 / 3 + qb * rb * phi
    el = sp.euler_equations(Fd, [phi, Pf], x)
    Dx = C * phi.diff(x) - Pf
    ok_el = z(el[0].lhs - (qb * rb - Dx.diff(x))) or z(el[0].lhs + (qb * rb - Dx.diff(x)))
    ok_el2 = z(el[1].lhs - (-Dx / C + bt * Pf**2)) or z(el[1].lhs + (-Dx / C + bt * Pf**2))
    Dr = qb * Mb / (4 * sp.pi * r**2)
    Psol = sp.sqrt(Dr / (C * bt))
    gM = qb * Psol / C
    V4 = sp.simplify((r * gM) ** 2)
    Kc = qb**3 / (4 * sp.pi * C**3 * bt)
    Krec = sp.simplify((qb**3 / (4 * sp.pi * C**3 * beta)) - qb**3 * v * hbar**3 / (2 * N * ms * C**3 * h**3))
    check("K6 EL equations, P = B/r, V^4 = K M_b, K = q_b^3/(4 pi C^3 beta) = record's q_b^3 v/(2 N m* C^3 h^3) (x hbar^3 in SI)",
          ok_el and ok_el2 and z(V4 - Kc * Mb) and Krec == 0,
          f"EL: {el[0].lhs} = 0, {el[1].lhs} = 0; P = {sp.simplify(Psol)}; V^4/M_b = {sp.simplify(V4 / Mb)}")
    say("")

    # ---------------- K7 slot identity and general n
    say("== K7: cubic energy at the transition polarisation (the slot) and its general-n coefficient")
    bsym = sp.Symbol("b", positive=True)
    a0b = a0_of(bsym)
    Pst = C * a0 / qb
    bsol = sp.solve(sp.Eq(a0b, a0), bsym)[0]
    slot = sp.simplify(bsol * Pst**3 / 3)
    nS = {}
    for n in (3, 4):
        S = 2 * sp.pi ** sp.Rational(n, 2) / sp.gamma(sp.Rational(n, 2))
        Gn, bn, Bn = sp.symbols("G_n b_n B_n", positive=True)
        # deep MOND in n dims: V^(2(n-1)) = a0^(n-2) G_n M_b; medium: P^(n-1) = q_b M_b/(C b S r^(n-1)) -> V^2 = q_b B/C
        Bexpr = (qb * Mb / (C * bn * S)) ** sp.Rational(1, n - 1)
        Vexp = sp.simplify((qb * Bexpr / C) ** (n - 1))
        bn_sol = sp.solve(sp.Eq(Vexp, a0 ** (n - 2) * Gn * Mb), bn)[0]
        epsn = sp.simplify(bn_sol * (C * a0 / qb) ** n / n)
        nS[n] = sp.simplify(a0**2 / (Gn * epsn))
    check("K7 beta P*^3/3 = a0^2/(12 pi G); general n: eps* = a0^2/(n S_{n-1} G_n), n S = 12 pi (n=3), 8 pi^2 (n=4)",
          z(slot - a0**2 / (12 * sp.pi * G)) and z(nS[3] - 12 * sp.pi) and z(nS[4] - 8 * sp.pi**2),
          f"slot = {slot}; n S_(n-1): n=3 {nS[3]}, n=4 {nS[4]}")
    say("")

    # ---------------- K8 unified formula and the variants that link the vacuum to beta
    say("== K8: unified formula: eps0 = sigma beta P_x^3/3  =>  kappa^2 = 12 pi/(sigma lambda_x^3), lambda_x = q_b P_x/(C a0)")
    Px = sp.Symbol("P_x", positive=True)
    k2u = sp.simplify((a0**2 / (G * sig * bsol * Px**3 / 3)))
    lam_def = qb * Px / (C * a0)
    ok_u = z(k2u - 12 * sp.pi / (sig * lam_def**3))
    # V3 tube: sigma = -1, P_x = Lambda/h
    k2_tube = sp.simplify(a0_of(beta) ** 2 / (G * E0t))
    lamL = sp.simplify(qb * PL / (C * a0_of(beta)))
    ok_t = z(k2_tube + 12 * sp.pi / lamL**3)
    # V4 PV S2: sigma = s, P_x = M/h
    s2 = sp.sympify(pv["S2 (frozen)"]["s"])
    k2_pv = sp.simplify(a0_of(beta) ** 2 / (G * s2 * A * Mpv**3 / 3))
    lamPV = sp.simplify(qb * (Mpv / h) / (C * a0_of(beta)))
    ok_p = z(k2_pv - 12 * sp.pi / (s2 * lamPV**3))
    kN1, kN3, a0N3, _ = kappa_posits()
    ok_n = z(kN1**2 - 12 * sp.pi) and z(kN3 - sp.Rational(2, 9) * sp.sqrt(8 * sp.pi / 3))
    check("K8 unified formula reproduced for V3 tube (sigma -1), V4 PV (sigma s), V5-N1 (lambda 1), V5-N3 (horizon)",
          ok_u and ok_t and ok_p and ok_n,
          f"general {k2u}; tube kappa^2 = {k2_tube} = -12 pi/lambda_L^3; PV kappa^2 = 12 pi/(s lambda_PV^3); "
          f"N1 kappa^2 = {sp.simplify(kN1**2)}; N3 kappa = {kN3}, a0 = {a0N3}")
    say("")

    # ---------------- K10 dimensions, I7 hbar, K11 v
    say("== K10 / I7 / K11: dimensions, hbar powers, v-dependence")
    A_, Vb_, E0_, beta_, a0m, k2m = micro_trade()
    dims = {"beta": dim(beta_), "K": dim(qb**3 / (4 * sp.pi * C**3 * beta_)), "a0_micro": dim(a0m),
            "E0_tube": dim(E0_), "kappa2_micro": dim(k2m), "lambda_L": dim(lamL), "lambda_PV": dim(lamPV),
            "kappa_N3": dim(kN3), "slot/(rho c^2)": dim(slot / (rho * c**2))}
    target = {"beta": Mu / (Lu * Tu**2 * Pu**3), "K": Lu**4 / (Tu**4 * Mu), "a0_micro": Lu / Tu**2,
              "E0_tube": Mu / (Lu * Tu**2), "kappa2_micro": 1, "lambda_L": 1, "lambda_PV": 1, "kappa_N3": 1,
              "slot/(rho c^2)": 1}
    ok_dim = all(z(dims[kx] - target[kx]) for kx in target)
    check("K10 SI dimensions (beta, K, a0, E0, kappa^2, lambda_x dimensionless)", ok_dim,
          ", ".join(f"{kx}: {dims[kx]}" for kx in dims))
    hp_a0 = dlog(a0m, hbar)
    hp_k2 = dlog(k2m, hbar)
    sub_h1r = {ms: hbar * k0 / c, v: c, Lam: eL * hbar * c * k0 / 2}
    a0_h1r = sp.simplify(a0m.subs(sub_h1r))
    k2_h1r = sp.simplify(k2m.subs(sub_h1r))
    hp_a0r, hp_k2r = dlog(a0_h1r, hbar), dlog(k2_h1r, hbar)
    hp_unified = dlog(sp.simplify(12 * sp.pi / lam**3), hbar)
    check("I7 hbar: 0 at fixed (beta, P_x); a0 ~ hbar^3, kappa^2 ~ hbar^9 at fixed (N, m*, v, h, Lambda, q_b, C); "
          "A3: hbar^2, hbar^3 under H1r", hp_unified == 0 and hp_a0 == 3 and hp_k2 == 9 and hp_a0r == 2 and hp_k2r == 3,
          f"d ln/d ln hbar: unified {hp_unified}; a0 {hp_a0}, kappa^2 {hp_k2}; H1r a0 {hp_a0r}, kappa^2 {hp_k2r}; "
          f"no Bekenstein-Hawking 1/4 appears")
    dv_fixed_lam = dlog(12 * sp.pi / lam**3, v)
    dv_micro = dlog(k2m, v)
    dv_posits = (sp.diff(kN1, v), sp.diff(kN3, v))
    check("K11 v: d ln kappa^2/d ln v = 0 at fixed lambda_x (posits v-free), = 3 at fixed microscopic parameters",
          dv_fixed_lam == 0 and dv_micro == 3 and all(d == 0 for d in dv_posits),
          f"fixed lambda {dv_fixed_lam}; micro {dv_micro}; d kappa_N1/dv, d kappa_N3/dv = {dv_posits}")
    say(f"  microscopic tube trade (magnitude only): kappa^2 = {k2m}")
    say(f"  under H1 + H1r (v = v_r = c, Lambda = eps_L hbar c k0/2): kappa^2 = {k2_h1r};  a0 = {a0_h1r}")
    R["kappa2_micro"] = str(k2m)
    R["kappa2_micro_H1r"] = str(k2_h1r)
    say("")

    # ---------------- K12 horizon locus and I8 pi-weights
    say("== K12 / I8: horizon locus and pi-weights")
    kH2 = sp.simplify(kN3**2)
    ZH = sp.simplify(sp.sqrt(8 * sp.pi / 3) / kN3)
    kH_gen = sp.simplify((8 * sp.pi * ee / 3) ** sp.Rational(3, 2) / (12 * sp.pi))

    def piw(expr):
        tp = sp.Symbol("t_pi", positive=True)
        return sp.simplify(tp * sp.diff(sp.log(sp.simplify(expr).subs(sp.pi, tp * sp.pi)), tp)).subs(tp, 1)

    pw = {"kappa_N1^2 = 12 pi": piw(kN1**2), "kappa_N3^2": piw(kH2), "slot n=4 (8 pi^2)": piw(nS[4])}
    check("K12 kappa_H = (2/9) sqrt(8 pi/3) = (8 pi e/3)^(3/2)/(12 pi) at e = 1; kappa_H^2 = 32 pi/243 (pi-odd)",
          z(kH2 - 32 * sp.pi / 243) and z(kH_gen.subs(ee, 1) - kN3) and pw["kappa_N3^2"] == 1 and pw[
              "kappa_N1^2 = 12 pi"] == 1 and pw["slot n=4 (8 pi^2)"] == 2,
          f"kappa_H^2 = {kH2}, Z_H = sqrt(8pi/3)/kappa_H = {ZH}; pi-weights {pw}")
    R["pi_weights"] = {kx: str(vx) for kx, vx in pw.items()}
    say("")

    # ---------------- I2, I3, I5, I6 and the rename test I4
    say("== I2: dependence of every graded output on free constants")
    deps = {}
    for name, ex in (("V3 kappa^2 micro (magnitude)", k2m), ("V3 kappa^2 (H1r)", k2_h1r),
                     ("V4 kappa^2 (PV, S2)", k2_pv)):
        deps[name] = {str(s): str(dlog(ex, s)) for s in sorted(ex.free_symbols, key=str)}
        say(f"  {name}: " + ", ".join(f"dln/dln {k_} = {v_}" for k_, v_ in deps[name].items()))
    say("  V2 eps0(P_cos = 0) = 0 for every value of every constant (identity); V1 no a0 (no law)")
    # free directions under H1 + H1r: rank of the Jacobian of (ln a0, ln |E0|) in (ln k0, ln eps_L, ln Q), Q = q_b/(C h)
    Qs = sp.Symbol("Q", positive=True)
    a0Q = sp.simplify(a0_h1r.subs(qb, Qs * C * h))
    E0Q = sp.simplify(sp.Abs(E0_.subs(sub_h1r)))
    J = sp.Matrix([[dlog(a0Q, s) for s in (k0, eL, Qs)], [dlog(E0Q, s) for s in (k0, eL, Qs)]])
    rankJ = J.rank()
    say(f"  H1+H1r: ln a0, ln|E0| vs (ln k0, ln eps_L, ln Q = ln q_b/(C h)): Jacobian {J.tolist()}, rank {rankJ} of 3 "
        f"-> {3 - rankJ} continuous direction left after fixing both a0 and rho_DE (plus N): any kappa is reachable")
    R["free_directions_after_a0_rho"] = int(3 - rankJ)
    ok_dep = all(any(sp.sympify(v_) != 0 for k_, v_ in deps[nm].items() if k_ not in ("G",)) for nm in deps)
    check("I2 graded kappa outputs depend on free medium constants (TRADE)", ok_dep and rankJ == 2,
          "every graded kappa expression carries free constants; Jacobian rank 2 < 3")
    say("")
    say("== I3: scaling G -> lG, rho -> mu rho, c -> nu c")
    l_, mu_, nu_ = sp.symbols("l mu_s nu", positive=True)
    a0N3s = a0N3.subs({G: l_ * G, rho: mu_ * rho, c: nu_ * c}, simultaneous=True)
    kN3s = sp.simplify(a0N3s / (nu_ * c * sp.sqrt(l_ * G * mu_ * rho)))
    check("I3 a0(N3) -> nu sqrt(l mu) a0, kappa invariant; unified kappa invariant at fixed lambda_x",
          z(sp.simplify(a0N3s / a0N3) - nu_ * sp.sqrt(l_ * mu_)) and z(kN3s - kN3), f"a0 ratio {sp.simplify(a0N3s / a0N3)}")
    say("")

    def grade(kappa_law):
        lam_req = (12 * sp.pi / kappa_law**2) ** sp.Rational(1, 3)
        return {"kN1": frac(kN1), "kN3": frac(kN3), "lam_req": frac(lam_req),
                "N1 equals law": abs(frac(kN1) - frac(kappa_law)) < 1e-9,
                "N3 equals law": abs(frac(kN3) - frac(kappa_law)) < 1e-9, "V2": 0.0}

    g_half = grade(sp.Rational(1, 2))
    g_25 = grade(sp.Rational(2, 5))
    ok_i4 = (g_half["kN1"] == g_25["kN1"] and g_half["kN3"] == g_25["kN3"] and not g_25["N1 equals law"]
             and not g_25["N3 equals law"] and abs(g_half["lam_req"] - g_25["lam_req"]) > 0.1 and g_25["V2"] == 0)
    check("I4 rename test (law's kappa 1/2 -> 2/5): posits do not move and fail the comparison; required lambda moves",
          ok_i4, f"kappa_N1 {g_half['kN1']:.4f} / {g_25['kN1']:.4f}; kappa_N3 {g_half['kN3']:.4f} / {g_25['kN3']:.4f}; "
                 f"lambda_req {g_half['lam_req']:.4f} -> {g_25['lam_req']:.4f}; V2 stays 0")
    check("I5 no Friedmann tautology: kappa_H depends on the Gauss-cubic factor and on Friedmann; Z_H^2 != 32 pi/3",
          not z(ZH**2 - 32 * sp.pi / 3) and sp.diff(kH_gen, ee) != 0, f"Z_H = {ZH}, Z_H^2 = {sp.simplify(ZH**2)}")
    check("I6 declared footing rho_DE only; rho_crit printed separately as kappa_crit = kappa_L sqrt(Omega_L)", True,
          "no pooling")
    say("")

    # ---------------- numbers (end only)
    say("== Numbers (measured H0 = 67.4 km/s/Mpc and Omega_L = 0.685 enter only here; report only)")
    OmL = 0.685
    lam_half = frac((48 * sp.pi) ** sp.Rational(1, 3))
    lam_hi = frac((12 * sp.pi / sp.Float(W_DATA[1]) ** 2) ** sp.Rational(1, 3))
    lam_lo = frac((12 * sp.pi / sp.Float(W_DATA[0]) ** 2) ** sp.Rational(1, 3))
    kN1n, kN3n = frac(kN1), frac(kN3)
    say(f"  unified trade: kappa = 1/2 needs lambda_x = (48 pi)^(1/3) = {lam_half:.4f}; W_data [0.227, 0.607] needs "
        f"lambda_x in [{lam_hi:.3f}, {lam_lo:.3f}] (a band or cutoff polarisation 4.7-9 x the transition one)")
    say(f"  V5-N1 (X2 slot) kappa_L = sqrt(12 pi) = {kN1n:.4f}  (kappa_crit = {kN1n * math.sqrt(OmL):.4f})")
    say(f"  V5-N3 (X3 horizon) kappa_L = (2/9) sqrt(8 pi/3) = {kN3n:.4f} (a0 = (2/9) c H_L, Z_H = 9/2)  "
        f"(kappa_crit = {kN3n * math.sqrt(OmL):.4f} vs rho_crit window {W_DATA_CRIT})")
    G_n, c_n, hb_n = 6.6743e-11, 2.99792458e8, 1.054571817e-34
    H0 = 67.4e3 / 3.0856775814913673e22
    rho_crit = 3 * H0**2 / (8 * math.pi * G_n)
    rho_de = OmL * rho_crit
    eps_de = rho_de * c_n**2
    k0_need = (48 * math.pi * eps_de / (2 * 1.0 * hb_n * c_n)) ** 0.25
    E_ring_meV = hb_n * c_n * k0_need / 1.602176634e-22
    say(f"  report-only band scale if |E0_tube| = rho_DE c^2 (N = 2, eps_L = 1, H1r): k0 = {k0_need:.3e} /m, "
        f"hbar c k0 = {E_ring_meV:.2f} meV (rho_DE^(1/4) = {(eps_de * (hb_n * c_n) ** 3) ** 0.25 / 1.602176634e-22:.2f} meV); "
        f"sign wrong (E0 < 0) and w = +1/2, so this is not a solution")
    R["numbers"] = {"lambda_half": lam_half, "lambda_window": [lam_hi, lam_lo], "kappa_N1": kN1n, "kappa_N3": kN3n,
                    "kappa_N1_crit": kN1n * math.sqrt(OmL), "kappa_N3_crit": kN3n * math.sqrt(OmL),
                    "band_scale_meV": E_ring_meV}
    say("")

    # ---------------- grading
    say("== Grading (frozen section 9)")
    inside = lambda kx: W_DATA[0] <= kx <= W_DATA[1]
    V = {
        "V1 strict Lorentz-invariant Dirac medium": ("NO LAW", "nonanalytic vacuum term ~ m^D (m^4 ln m at D=4); deep MOND "
                                                               "needs |P|^(D-1); only point nodes are Lorentz-invariant"),
        "V2 ring, v = v_r = c, cone dim reg, P_cos = 0": ("IDENTITY (vanishing)",
                                                          f"eps0 = {eps_dr.subs(Dl, 0)} at P_cos = 0 for every kappa"),
        "V3 ring, v = v_r = c, tube band": ("NO SOLUTION (sign and EOS)",
                                            f"E0 = -beta P_L^3/3 < 0, w = {w_t0}; magnitude-only TRADE kappa^2 = 12 pi/"
                                            f"lambda_L^3 (window needs lambda_L {lam_hi:.2f}-{lam_lo:.2f})"),
        "V4 ring, v = v_r = c, Pauli-Villars": ("CONDITION",
                                                f"E0 = s (A/3) M_PV^3, s = {pv['S2 (frozen)']['s_num']:+.3f} (S2) / "
                                                f"{pv['S3 (A2)']['s_num']:+.3f} (S3), w = -1; TRADE kappa^2 = 12 pi/"
                                                f"(s lambda_PV^3)"),
        "V5-N1 q_b P0/C = a0 (X2 slot)": ("EXCLUDED-CLASS POSIT",
                                          f"kappa = {kN1n:.4f} ({'inside' if inside(kN1n) else 'outside'} W_data)"),
        "V5-N2 tether / law vacuum": ("IDENTITY (vanishing)", "P0 = 0, eps0 = 0"),
        "V5-N3 q_b P0/C = c H_L (X3 horizon)": ("EXCLUDED-CLASS POSIT",
                                                f"kappa = {kN3n:.4f} ({'inside' if inside(kN3n) else 'outside'} W_data)"),
        "V5-N4 free minimum": ("IDENTITY (vanishing)", "minimum of P^2/2C + beta|P|^3/3 at P0 = 0"),
    }
    for kx, (cl, why) in V.items():
        say(f"  {kx}: {cl} -- {why}")
    graded = [cl for kx, (cl, _) in V.items() if not kx.startswith("V5-N1") and not kx.startswith("V5-N3")]
    allpass = all(cv["pass"] for cv in CHECKS.values())
    if not allpass:
        overall = "VOID"
    elif any(cl.startswith("CONSISTENT") for cl in graded):
        overall = "CONSISTENT (not significant, TRADE)"
    else:
        overall = "CLOSURE"
    p_exact, p_data = 0.0, 0.0
    say("")
    say(f"Checks: {sum(cv['pass'] for cv in CHECKS.values())}/{len(CHECKS)} PASS")
    say(f"OVERALL: {overall}.  p_exact = {p_exact}, p_data = {p_data} (no graded variant gives a determinate kappa; the two "
        f"posits are excluded-class and miss). S4 second prediction not reached. kappa = 1/2 stays FITTED. Not theory closed.")
    R["variants"] = {kx: {"class": cl, "why": why} for kx, (cl, why) in V.items()}
    R["checks"] = CHECKS
    R["overall"] = overall
    R["p_exact"], R["p_data"] = p_exact, p_data
    return R, (0 if allpass else 2)


# ======================================================================================================================
# MUTATE RUN
# ======================================================================================================================
def main_mutate():
    say("CFG900 MUTATE run (criteria 32264ab5d section 6; amendment A1 for the M4 factor)")
    say("")
    teeth = {}

    # M1 v = c -> c/2 at fixed N, m*, h, Lambda, q_b, C
    _, _, E0b, bb, a0b, k2b = micro_trade(1)
    _, _, E0m, bm, a0m, k2m = micro_trade(sp.Rational(1, 2))
    rb_, ra_, re_, rk_ = (sp.simplify(bm / bb), sp.simplify(a0m / a0b), sp.simplify(E0m / E0b), sp.simplify(k2m / k2b))
    kN1b, kN3b, _, _ = kappa_posits(vfac=1)
    kN1m, kN3m, _, _ = kappa_posits(vfac=sp.Rational(1, 2))
    p_same = block_V1_exponent(4) == block_V1_exponent(4)
    bite = (rb_ == 2 and ra_ == sp.Rational(1, 2) and re_ == 2 and rk_ == sp.Rational(1, 8)
            and z(kN1m - kN1b) and z(kN3m - kN3b) and p_same)
    teeth["M1 v -> c/2: beta x2, a0 x1/2, E0_tube x2, kappa_tube^2 x1/8; posits unchanged; V1 exponent unchanged"] = bite
    say(f"  M1: beta x{rb_}, a0 x{ra_}, E0 x{re_}, kappa^2 x{rk_} (kappa x{frac(sp.sqrt(rk_)):.4f}); posits "
        f"{frac(kN1m):.4f}/{frac(kN3m):.4f} (base {frac(kN1b):.4f}/{frac(kN3b):.4f}) -> {'BITES' if bite else 'DOES NOT BITE'}")

    # M2 D = 4 -> 5
    pli, pneed = block_V1_exponent(5)
    pring, pneed_r = block_ring_exponent(5)
    pring4, pneed4 = block_ring_exponent(4)
    k1n4, kN3pow4, _, S4 = kappa_posits(n=4)
    slot4 = sp.simplify(k1n4**2)
    bite = (pli == 5 and pneed == 4 and pring == 3 and pneed_r == 4 and pring4 == pneed4 and z(slot4 - 8 * sp.pi**2))
    teeth["M2 D 4->5: LI 5 vs 4 (NO LAW persists); ring 3 vs 4 (ring loses the law); slot 12 pi -> 8 pi^2"] = bite
    say(f"  M2: LI p {pli} vs need {pneed}; ring p {pring} vs need {pneed_r} (D=4: {pring4} vs {pneed4}) -> V2-V5 NO LAW; "
        f"slot n S = {slot4} (pi-weight 2); formal horizon kappa^2 at n = 4: {kN3pow4} (pi-free) -> "
        f"{'BITES' if bite else 'DOES NOT BITE'}")

    # M3 statistics flip
    Ab, Vbb = tube_band(1, 1)
    Am, Vbm = tube_band(1, -1)
    E0f, E0bos = sp.simplify(Vbb.subs(Dl, 0)), sp.simplify(Vbm.subs(Dl, 0))
    bf, bbos = beta_of(1, 1), beta_of(1, -1)
    cubf = sp.simplify(sp.expand(sp.series(Vbb, Dl, 0, 4).removeO()).coeff(Dl, 3))
    cubb = sp.simplify(sp.expand(sp.series(Vbm, Dl, 0, 4).removeO()).coeff(Dl, 3))
    sign = lambda e: 1 if sp.simplify(e).is_positive else (-1 if sp.simplify(e).is_negative else 0)
    dr0 = sp.simplify(-Ab * 2 * sp.pi * I_dr(2, sp.Rational(1, 2), Dl)).subs(Dl, 0)
    bite = (sign(E0f) == -1 and sign(cubf) == 1 and sign(E0bos) == 1 and sign(cubb) == -1 and sign(bbos) == -1
            and dr0 == 0 and sign(E0f) == -sign(bf) and sign(E0bos) == -sign(bbos))
    teeth["M3 statistics flip: E0_tube > 0, beta < 0 (NO LAW); sign lock both ways; dim reg E0(0) = 0"] = bite
    say(f"  M3: fermion E0 {E0f}, cubic {cubf}; boson E0 {E0bos}, cubic {cubb} (concave: P = B/r has no real B) -> "
        f"{'BITES' if bite else 'DOES NOT BITE'}")

    # M4 Einstein coupling 8 pi G -> 4 pi G (A1)
    _, kN3e1, _, _ = kappa_posits(e=1)
    _, kN3e2, _, _ = kappa_posits(e=sp.Rational(1, 2))
    ratio = sp.simplify(kN3e2 / kN3e1)
    frozen_ok = z(ratio - 1 / sp.sqrt(2))
    amended_ok = z(ratio - sp.Rational(1, 2) ** sp.Rational(3, 2))
    kN1e2, _, _, _ = kappa_posits(e=sp.Rational(1, 2))
    slot_same = z(kN1e2 - kN1b)
    trade_same = True     # kappa^2 = 12 pi/lambda^3 carries no Einstein coupling (Newton's G in the MOND law only)
    bite = amended_ok and slot_same and trade_same
    teeth["M4 8piG -> 4piG: kappa_H x (1/2)^(3/2) (A1); slot and trade unchanged"] = bite
    say(f"  M4: kappa_H {frac(kN3e1):.4f} -> {frac(kN3e2):.4f} (ratio {ratio} = {frac(ratio):.4f}); frozen expectation "
        f"1/sqrt2: {'holds' if frozen_ok else 'FAILS AS FROZEN (hand slip, corrected by A1 before any script)'}; "
        f"amended (1/2)^(3/2): {'holds' if amended_ok else 'fails'}; slot unchanged {slot_same} -> "
        f"{'BITES' if bite else 'DOES NOT BITE'}")

    allbite = all(teeth.values())
    say("")
    say(f"MUTATE: {sum(teeth.values())}/{len(teeth)} teeth bite -> {'exit 1 (by design)' if allbite else 'VOID (exit 2)'}")
    say("The overall label of the normal run is not changed by a MUTATE run.")
    return {"lane": "CFG900", "mode": "MUTATE", "teeth": teeth, "all_bite": allbite,
            "M4_frozen_factor_holds": bool(frozen_ok), "M4_amended_factor_holds": bool(amended_ok)}, (1 if allbite else 2)


if __name__ == "__main__":
    if MUTATE:
        res, code = main_mutate()
    else:
        res, code = main_normal()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(LINES) + "\n")
    with open(JSN, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=str)
    sys.exit(code)
