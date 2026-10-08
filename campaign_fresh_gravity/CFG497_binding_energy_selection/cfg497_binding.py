#!/usr/bin/env python3
"""CFG497: does a binding-energy selection rule, with a threshold NOT set by S, select S x M_b,orig of cold?
Criteria: FROZEN_CRITERIA.md (committed alone first, e8ec321b0).

Model: CFG118's point-core secondary infall (H-N, Planck18 LCDM) through this folder's COPY of CFG488's infall worker
(cfg497_infall.py; CFG118's shellcore.c compiled read-only). Selection: cold with specific energy E < E_thr at the dissipation
time t_d = 2 t_ta(k_b) (CFG494). Ten declared thresholds (A1-A4 a0-free, B1-B6 a0-carrying) + restatement controls R1/R2.
Scored: (M) match 5.364 +-10% in every cell with purity >= 0.9; (T) MUTATE tracking (2S -> 10.728 +-10%); (iii) G9.
Bonus: (i) clusters, (ii) KiDS window + CFG485 early-type levels.

kappa = 1/2 is FITTED. Both footings scored separately, never pooled. No dark-matter particle: the cold fluid's mass is still
required and its amount (Omega_c/Omega_b = 5.364) is an input. Offline numerics on committed record files only; no downloads.
This is not "theory closed".

Run:  nice -n 15 python3 cfg497_binding.py                    (exit 0 iff controls K1-K6 pass)
      CFG497_MUTATE=1 nice -n 15 python3 cfg497_binding.py    (Omega_c/Omega_b -> 10.728; exit 1 iff the teeth are detected)
"""
import os
import sys
import io
import math
import json
import time
import contextlib
import ctypes
from ctypes import c_double, c_int32, POINTER

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
REPO = os.path.dirname(CFGDIR)
sys.path.insert(0, CFGDIR)
import CFG4_common as C4  # noqa: E402

MUT = os.environ.get("CFG497_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
TESTN = int(os.environ.get("CFG497_TESTN", "0"))           # development only: small-N smoke test, writes *_TEST.*
if TESTN:
    TAG += "_TEST"
for _e in ("CFG488_MUTATE", "CFG485_MUTATE", "CFG494_MUTATE"):
    os.environ.pop(_e, None)
try:
    os.nice(15)
except OSError:
    pass

sys.path.insert(0, HERE)
import cfg497_infall as IF  # noqa: E402  (copy of CFG488's worker; MUTATE via CFG497_MUTATE)

sys.path.insert(0, os.path.join(CFGDIR, "CFG100_kids_mass_rederivation"))
import cfg100_lib as L100  # noqa: E402

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


S_TRUE = 5.364
S_RUN = IF.SHARE
assert abs(S_RUN - (2 * S_TRUE if MUT else S_TRUE)) < 1e-12
FB_TRUE = 1.0 / (1.0 + S_TRUE)
X_E = 1.0 / math.log(1.0 + 1.0 / S_TRUE)
FOOTS = C4.FOOTS
LOGMB = [9.0, 10.5, 11.5]
QS = IF.QS
NS = TESTN or IF.NS
M_SIM = IF.M_SIM
G = IF.G
H0 = IF.H0
NU1 = float(C4.nu_mono(np.array([1.0]))[0])
MATCH = (0.9 * S_RUN, 1.1 * S_RUN)
CANDS = ["A1 VIR200", "A2 VIRTH", "A3 CATCH", "A4 CORE-BOUND", "B1 Y1-FIELD", "B2 A0-FIELD", "B3 Y1-RM", "B4 LAW-TA",
         "B5 VF-SPEED", "B6 LYNDEN-BELL"]
CTRLS = ["R1 BARYON-E", "R2 TOP-S"]
CLASS_A = {"A1 VIR200", "A2 VIRTH", "A3 CATCH", "A4 CORE-BOUND"}
G9 = {"A1 VIR200": (True, "total potential at R_200 (total density)"), "A2 VIRTH": (True, "total potential at R_ta/2"),
      "A3 CATCH": (True, "total potential at R_ta"), "A4 CORE-BOUND": (False, "species split: the baryon core's own potential"),
      "B1 Y1-FIELD": (True, "total field + a0 + kernel nu(1)"), "B2 A0-FIELD": (True, "total field + a0"),
      "B3 Y1-RM": (False, "species split: r_M needs M_b"), "B4 LAW-TA": (False, "law's nu(g_N[b]) before settling: needs M_b"),
      "B5 VF-SPEED": (False, "species split: V_f needs M_b"), "B6 LYNDEN-BELL": (False, "not formulable without a quantum")}
CONSTS = {"A1 VIR200": "1 conventional (200)", "A2 VIRTH": "1 structural (1/2)", "A3 CATCH": "0", "A4 CORE-BOUND": "0",
          "B1 Y1-FIELD": "0 (kernel nu(1))", "B2 A0-FIELD": "0", "B3 Y1-RM": "0", "B4 LAW-TA": "0", "B5 VF-SPEED": "0",
          "B6 LYNDEN-BELL": "needs a quantum mass (excluded: no particle)"}
R = {"lane": "CFG497", "mutate": MUT, "kappa": "1/2 FITTED", "S_run": S_RUN, "controls": {}, "cells": {}, "crit": {}}

P("=" * 118)
P(f"CFG497 binding-energy selection   MUTATE={MUT}   S_run = Omega_c/Omega_b = {S_RUN}   match window [{MATCH[0]:.3f}, {MATCH[1]:.3f}]")
P(f"kappa = 1/2 FITTED; footings never pooled; nu_mono(1) = {NU1:.5f}")
P("=" * 118)

# ---------------------------------------------------------------- K3
mph = float(C4.nu_mono(np.array([1.0 / X_E ** 2]))[0] - 1.0)
K3 = abs(X_E - 5.8498) < 1e-3 and abs(mph / S_TRUE - 1) < 1e-6
P(f"[K3] x_e = {X_E:.6f}; point phantom at x_e = {mph:.9f} M_b -> {'PASS' if K3 else 'FAIL'}")
R["controls"]["K3"] = {"pass": bool(K3)}


# ======================================================================================================== infall
def integrate(L, Pp, r0, v0, tsnap):
    N = Pp.N
    snap = np.zeros((len(tsnap), N))
    ro, vo, j2, tta, rta, rp1 = (np.zeros(N) for _ in range(6))
    npe = np.zeros(N, np.int32)
    St = IF.Stats()
    f = lambda x: x.ctypes.data_as(POINTER(c_double))
    r0 = np.ascontiguousarray(r0, float); v0 = np.ascontiguousarray(v0, float); ts = np.ascontiguousarray(tsnap, float)
    rc = L.run_shells(ctypes.byref(Pp), f(r0), f(v0), f(ts), f(snap), f(ro), f(vo), f(j2), f(tta), f(rta), f(rp1),
                      npe.ctypes.data_as(POINTER(c_int32)), ctypes.byref(St))
    if rc != len(tsnap):
        raise RuntimeError(f"integrator returned {rc}")
    return dict(r=ro, v=vo, j2=j2, t_ta=tta, r_ta=rta, snap=snap)


LIB = IF.build_lib()


def rho_crit(t):
    a = IF.a_of_t(t)
    Hh = H0 * math.sqrt(IF.OM / a ** 3 + IF.OL)
    return 3.0 * Hh * Hh / (8.0 * math.pi * G)


EPOCHS = ("tta", "td", "z2")


def run(q, N, Mc):
    """one H-N run with the core = Mc (sim units = Msun); returns per-epoch state for the selection."""
    t0r = time.time()
    su = IF.setup(Mc, "LCDM")
    eds, Om_, OL_, fsm, ocold = IF.cosmo("LCDM")
    m = su["M_out"] / N
    Mk = m * (np.arange(N) + 0.5)
    r0 = (3.0 * Mk / (4.0 * math.pi * su["rhoci"])) ** (1.0 / 3.0)
    v0 = su["Hi"] * r0
    mkP = lambda ns: IF.Params(eds, H0, Om_, OL_, fsm, G, 1, Mc, su["soft"], 1.0, N, m, q, su["t0"], su["t1"], IF.KMAX,
                               IF.KF, IF.ETA, IF.ETAH, ns)
    o1 = integrate(LIB, mkP(1), r0, v0, np.array([su["t1"]]))
    bk = np.full(N, m / S_RUN)                                     # adiabatic: each cold shell carries m/S of baryons
    cb = np.concatenate([[0.0], np.cumsum(bk)[:-1]])
    w = np.clip((Mc - cb) / bk, 0.0, 1.0)                           # partner weight (labels; used for purity and R1 only)
    kb = int(np.max(np.where(w > 0)[0]))
    tta = o1["t_ta"]
    tb = float(tta[kb])
    td = min(2.0 * tb, su["t1"] * (1.0 - 2e-6))
    times = {"tta": tb, "td": td, "z2": IF.t_of_a(1.0 / 3.0)}
    tl = []
    for k, t in times.items():
        tl += [(k, t), (k + "+", t * (1.0 + 1e-6))]
    tl.sort(key=lambda x: x[1])
    o2 = integrate(LIB, mkP(len(tl)), r0, v0, np.array([t for _, t in tl]))
    snaps = {k: o2["snap"][i] for i, (k, _) in enumerate(tl)}
    turned = np.isfinite(tta) & (tta > 0)
    oo = np.argsort(tta[turned])
    T_ta, R_ta = tta[turned][oo], o2["r_ta"][turned][oo]
    out = {"q": q, "N": N, "Mc": Mc, "m": m, "su": su, "w": w, "kb": kb, "t_ta_kb": tb, "t_d": td, "times": times,
           "z_d": 1.0 / IF.a_of_t(td) - 1.0, "z_ta": 1.0 / IF.a_of_t(tb) - 1.0, "partner_over_SMb": float(np.sum(w) * m / (S_RUN * Mc)),
           "two_pass": float(np.max(np.abs(o2["r"] - o1["r"]) / np.maximum(o1["r"], 1e-30))), "ep": {}}
    for ek in EPOCHS:
        t = times[ek]
        rs, rs2 = snaps[ek], snaps[ek + "+"]
        dt = t * 1e-6
        v = (rs2 - rs) / dt
        a = IF.a_of_t(t)
        o = np.argsort(rs)
        rsort = rs[o]
        csum = m * np.arange(N)                                       # shell mass strictly inside each sorted shell
        outer = np.concatenate([np.cumsum((m / rsort)[::-1])[::-1][1:], [0.0]])
        eps = su["soft"]
        bg = lambda r: fsm * H0 ** 2 * r ** 2 / (4.0 * a ** 3) - OL_ * H0 ** 2 * r ** 2 / 2.0
        phi_s = -G * Mc / np.sqrt(rsort ** 2 + eps ** 2) - G * (csum / rsort + outer) - G * 0.5 * m / rsort + bg(rsort)
        phi = np.empty(N); phi[o] = phi_s
        E = 0.5 * v * v + 0.5 * o2["j2"] / np.maximum(rs, 1e-30) ** 2 + phi
        Ecore = 0.5 * v * v + 0.5 * o2["j2"] / np.maximum(rs, 1e-30) ** 2 - G * Mc / np.sqrt(rs ** 2 + eps ** 2)
        # CFG494's own energy (K2): no background, Min/r with the core inside
        Min = Mc + m * np.arange(N)
        phi494 = np.empty(N); phi494[o] = -G * (Min / rsort + outer) - G * 0.5 * m / rsort
        E494 = 0.5 * v * v + 0.5 * o2["j2"] / np.maximum(rs, 1e-30) ** 2 + phi494
        cumall = np.concatenate([[0.0], np.cumsum(np.full(N, m))])

        def Phi_at(Rr):
            n = np.searchsorted(rsort, Rr)
            outer_ = float(np.sum(m / rsort[n:]))
            return float(-G * Mc / math.sqrt(Rr ** 2 + eps ** 2) - G * (m * n / Rr + outer_) + bg(Rr))

        def Menc(Rr):
            return float(IF.Mcore(Mc, Rr, eps) + m * np.searchsorted(rsort, Rr))

        def g_tot(Rr):
            return G * Menc(Rr) / Rr ** 2 + 0.5 * fsm * H0 ** 2 / a ** 3 * Rr - OL_ * H0 ** 2 * Rr

        Rgrid = np.geomspace(1e-5 * su["r_ta0"], 3.0 * su["r_ta0"], 6001)
        Mg = IF.Mcore(Mc, Rgrid, eps) + m * np.searchsorted(rsort, Rgrid)
        gg = G * Mg / Rgrid ** 2 + 0.5 * fsm * H0 ** 2 / a ** 3 * Rgrid - OL_ * H0 ** 2 * Rgrid
        vc = np.sqrt(np.maximum(G * Mg / Rgrid, 0.0))
        # R_200 (CFG494's definition)
        Me = Mc + m * (np.arange(N) + 1)
        rho = Me / (4.0 / 3.0 * math.pi * rsort ** 3)
        ok = np.where(rho >= 200.0 * rho_crit(t))[0]
        R200 = float(rsort[ok[-1]]) if len(ok) else float("nan")
        out["ep"][ek] = dict(t=t, z=1.0 / a - 1.0, E=E, Ecore=Ecore, E494=E494, Phi_at=Phi_at, g_tot=g_tot, Rgrid=Rgrid, gg=gg,
                             vc=vc, R200=R200, Rta=float(np.interp(t, T_ta, R_ta)), rs=rs)
    out["seconds"] = time.time() - t0r
    return out


def outermost(Rgrid, f, thr):
    """outermost radius where f(R) >= thr (log-interpolated); nan if nowhere."""
    k = np.where(f >= thr)[0]
    if not len(k):
        return float("nan")
    k = k[-1]
    if k + 1 >= len(Rgrid):
        return float(Rgrid[-1])
    lf1, lf2 = math.log(f[k]), math.log(max(f[k + 1], 1e-300))
    x = (math.log(thr) - lf1) / (lf2 - lf1) if lf2 != lf1 else 0.0
    return float(math.exp(math.log(Rgrid[k]) + x * (math.log(Rgrid[k + 1]) - math.log(Rgrid[k]))))


def select(run_, ek, cand, Mb, foot):
    """(s_sel, purity, r_x/R_ta) for candidate cand at physical baryon mass Mb (Msun), footing foot, epoch ek."""
    e = run_["ep"][ek]
    Mc, m, w = run_["Mc"], run_["m"], run_["w"]
    lam = (Mb / Mc) ** (1.0 / 3.0)                                   # physical / sim length (and velocity, field) scale
    a0 = IF.A0K[foot]
    rx = float("nan")
    if cand == "A1 VIR200":
        rx = e["R200"]
    elif cand == "A2 VIRTH":
        rx = 0.5 * e["Rta"]
    elif cand == "A3 CATCH":
        rx = e["Rta"]
    elif cand == "B1 Y1-FIELD":
        rx = outermost(e["Rgrid"], e["gg"], NU1 * a0 / lam)
    elif cand == "B2 A0-FIELD":
        rx = outermost(e["Rgrid"], e["gg"], a0 / lam)
    elif cand == "B3 Y1-RM":
        rx = IF.r_M_kpc(Mb, foot) / lam
    elif cand == "B4 LAW-TA":
        rx = 1000.0 * L100.r_ta_law(Mb, L100.A0[foot], e["z"]) / lam
    elif cand == "B5 VF-SPEED":
        Vf = (G * Mb * a0) ** 0.25
        rx = outermost(e["Rgrid"], e["vc"], Vf / lam)
    elif cand == "B6 LYNDEN-BELL":
        return float("nan"), float("nan"), float("nan")
    if cand == "A4 CORE-BOUND":
        mask = e["Ecore"] < 0.0
    elif cand == "R1 BARYON-E":
        mask = e["E"] < e["E"][run_["kb"]]
    elif cand == "R2 TOP-S":
        n = int(round(S_RUN * Mc / m))
        mask = np.zeros(len(w), bool); mask[np.argsort(e["E"])[:n]] = True
    else:
        if not np.isfinite(rx):
            return 0.0, float("nan"), float("nan")
        mask = e["E"] < e["Phi_at"](rx)
    n = int(mask.sum())
    s = n * m / Mc
    pur = float(np.sum(w[mask]) / n) if n else float("nan")
    return s, pur, (rx / e["Rta"] if np.isfinite(rx) else float("nan"))


P("\n[infall] H-N q = 0.05, 0.1, 0.2 at N = 20000 (core 1e10); K6: q = 0.1 with the core at 1e9")
RUNS = {}
for q in QS:
    RUNS[q] = run(q, NS, M_SIM)
    r_ = RUNS[q]
    P(f"  q = {q:.2f}: {r_['seconds']:.0f} s; two-pass {r_['two_pass']:.1e}; M_ta/M_b {r_['su']['M_ta'] / M_SIM:.3f}; r_ta0 "
      f"{r_['su']['r_ta0']:.2f} kpc; k_b {r_['kb']}; z_ta(k_b) {r_['z_ta']:.3f}; z_d {r_['z_d']:.3f}; partner/(S M_b) {r_['partner_over_SMb']:.12f}")
RUN6 = None if MUT else run(0.1, NS, 1e9)

# ---------------------------------------------------------------- K1, K2
if not MUT:
    k1 = all(abs(RUNS[q]["su"]["M_ta"] / M_SIM / 23.632 - 1) <= 0.01 and abs(RUNS[q]["su"]["r_ta0"] / 507.94 - 1) <= 0.01
             and abs(RUNS[q]["partner_over_SMb"] - 1) < 1e-9 and abs(RUNS[q]["z_d"] - 3.51) <= 0.02 and RUNS[q]["two_pass"] < 1e-9
             for q in QS)
else:
    k1 = all(abs(RUNS[q]["partner_over_SMb"] - 1) < 1e-9 for q in QS)
P(f"[K1] set-up vs CFG494/CFG118 -> {'PASS' if k1 else 'FAIL'}" + (" (MUTATE: partner = 2S M_b only)" if MUT else ""))
R["controls"]["K1"] = {"pass": bool(k1)}
k2v = []
for q in QS:
    e = RUNS[q]["ep"]["td"]; w = RUNS[q]["w"]; m = RUNS[q]["m"]
    n = int(math.ceil(S_RUN * M_SIM / m))
    sel = np.argsort(e["E494"])[:n + 1]
    k2v.append(float(np.sum(w[sel]) / len(sel)))
ref494 = (0.9721, 0.9779, 0.9996)
K2 = MUT or all(abs(a - b) <= 0.01 for a, b in zip(k2v, ref494))
P(f"[K2] CFG494 energy-rank purity (its Phi): " + ", ".join(f"{v:.4f}" for v in k2v) + f" vs {ref494} -> {'PASS' if K2 else 'FAIL'}"
  + (" (MUTATE: not required)" if MUT else ""))
R["controls"]["K2"] = {"pass": bool(K2), "values": k2v}

# ======================================================================================================== selection table
P("\n" + "=" * 118)
P(f"SELECTION at t_d: s_sel = selected cold / M_b,orig (target {S_RUN}); purity = partner fraction; r_x / R_ta(t_d)")
P("=" * 118)
CELLS = {}
for cand in CANDS + CTRLS:
    CELLS[cand] = {}
    for f in FOOTS:
        for lm in LOGMB:
            for q in QS:
                s, pu, rr = select(RUNS[q], "td", cand, 10 ** lm, f)
                CELLS[cand][f"{f}|{lm}|{q}"] = {"s": s, "pur": pu, "rx_over_Rta": rr}
    vals = [v["s"] for v in CELLS[cand].values()]
    P(f"\n  {cand}:")
    for f in FOOTS:
        P(f"    {f:9s} " + " | ".join(
            f"lgM {lm}: " + ", ".join(f"{CELLS[cand][f'{f}|{lm}|{q}']['s']:.3f}" + (f"(pu {CELLS[cand][f'{f}|{lm}|{q}']['pur']:.2f})"
                                       if np.isfinite(CELLS[cand][f'{f}|{lm}|{q}']['pur']) else "") for q in QS) for lm in LOGMB))
    rxs = [v["rx_over_Rta"] for v in CELLS[cand].values() if np.isfinite(v["rx_over_Rta"])]
    if rxs:
        P(f"    r_x/R_ta(t_d) range {min(rxs):.4f} - {max(rxs):.4f}")

# epoch robustness at the three masses (q = 0.1, both footings): s_sel at t_ta(k_b), t_d, z = 2
P("\n  epoch robustness (q = 0.1): s_sel at t_ta(k_b) / t_d / z = 2")
EPOCH = {}
for cand in CANDS + CTRLS:
    EPOCH[cand] = {}
    for f in FOOTS:
        for lm in LOGMB:
            EPOCH[cand][f"{f}|{lm}"] = [select(RUNS[0.1], ek, cand, 10 ** lm, f)[0] for ek in EPOCHS]
    P(f"    {cand:15s} " + "; ".join(f"{k}: " + "/".join(f"{x:.2f}" for x in v) for k, v in EPOCH[cand].items()))

# ---------------------------------------------------------------- K6 self-similarity
if not MUT:
    k6 = []
    for cand in ("B2 A0-FIELD", "A1 VIR200"):
        for f in FOOTS:
            a = select(RUNS[0.1], "td", cand, 1e9, f)[0]
            b = select(RUN6, "td", cand, 1e9, f)[0]
            k6.append((cand, f, a, b))
    K6 = all(abs(b / a - 1) <= 0.02 for _, _, a, b in k6 if a > 0)
    P("\n[K6] rescaled (1e10 run) vs direct (1e9 run) at M_b = 1e9: " + "; ".join(f"{c} {f}: {a:.4f} vs {b:.4f}" for c, f, a, b in k6)
      + f" -> {'PASS' if K6 else 'FAIL'}")
    R["controls"]["K6"] = {"pass": bool(K6), "rows": k6}

# ---------------------------------------------------------------- (M) and (iii)
MROW = {}
for cand in CANDS:
    vv = list(CELLS[cand].values())
    ok = all(np.isfinite(v["s"]) and MATCH[0] <= v["s"] <= MATCH[1] and np.isfinite(v["pur"]) and v["pur"] >= 0.9 for v in vv)
    nhit = sum(1 for v in vv if np.isfinite(v["s"]) and MATCH[0] <= v["s"] <= MATCH[1])
    ss = [v["s"] for v in vv if np.isfinite(v["s"])]
    MROW[cand] = {"pass": bool(ok), "n_hit": nhit, "n_cells": len(vv), "s_min": min(ss) if ss else None, "s_max": max(ss) if ss else None}
R["cells"] = CELLS
R["epoch"] = EPOCH

# ======================================================================================================== bonus (main only)
BONUS = {}
if not MUT:
    P("\n" + "=" * 118)
    P("BONUS: (i) clusters, (ii) KiDS window and CFG485 early-type levels (q-geometric-mean s_sel; class B via a mass grid)")
    P("=" * 118)
    LG = np.arange(8.0, 14.51, 0.25)
    SGRID = {}
    for cand in CANDS:
        if cand == "B6 LYNDEN-BELL":
            continue
        SGRID[cand] = {}
        for f in FOOTS:
            arr = []
            for lg in LG:
                sv = [select(RUNS[q], "td", cand, 10 ** lg, f)[0] for q in QS]
                arr.append(float(np.exp(np.mean(np.log(np.maximum(sv, 1e-6))))))
            SGRID[cand][f] = np.array(arr)

    def s_of(cand, f, Mb):
        return float(np.exp(np.interp(math.log10(Mb), LG, np.log(np.maximum(SGRID[cand][f], 1e-6)))))

    YG = np.logspace(-14, 6, 40001)
    NUG = C4.nu_mono(YG) - 1.0

    def x_for_phantom(T):
        T = np.asarray(T, float)
        y = np.exp(np.interp(np.log(T), np.log(NUG[::-1]), np.log(YG[::-1])))
        return 1.0 / np.sqrt(y)

    # (i) clusters
    J453 = json.load(open(os.path.join(CFGDIR, "CFG453_t15_deficit_units", "cfg453_results.json")))
    for cand in SGRID:
        BONUS[cand] = {"clusters": {}, "kids": {}, "early": {}}
    CLR = {}
    for f in FOOTS:
        D = J453["D1"][f]
        xA, xT, nucl = D["xA"]["cl"], D["xT"]["cl"], D["nu"]["cl"]
        urec = [S_TRUE * a / t for a, t in zip(xA, xT)]
        CLR[f] = (min(urec), max(urec), nucl, xT)
        P(f"  clusters {f}: record range [{CLR[f][0]:.4f}, {CLR[f][1]:.4f}]; nu-1 = {nucl - 1:.3f}; x_T15 {xT[0]:.3f}/{xT[1]:.3f}")
    for cand in SGRID:
        okall = True
        for f in FOOTS:
            lo, hi, nucl, xT = CLR[f]
            us = {}
            for lgc in (13.5, 14.0, 14.5):
                sc = s_of(cand, f, 10 ** lgc)
                st = min(nucl - 1.0, sc)
                us[lgc] = [1.0 - st / xT[0], 1.0 - st / xT[1]]
            ok = all(lo <= u <= hi for u in us[14.0])
            okall = okall and ok
            BONUS[cand]["clusters"][f] = {"u_by_lgM": us, "s_at_1e14": s_of(cand, f, 1e14), "pass": ok}
        BONUS[cand]["clusters"]["pass"] = okall
        P(f"  (i) {cand:15s} " + "; ".join(f"{f}: s(1e14) {BONUS[cand]['clusters'][f]['s_at_1e14']:.2f}, u {BONUS[cand]['clusters'][f]['u_by_lgM'][14.0][0]:.3f}/"
                                         f"{BONUS[cand]['clusters'][f]['u_by_lgM'][14.0][1]:.3f}" for f in FOOTS) + f" -> {'PASS' if okall else 'FAIL'}")
    # (ii) KiDS
    DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
    lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
    zl = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float)
    WW = np.load(os.path.join(DATA, "cfg110_perlens.npz"))["WW"]
    lmg = np.log10(Mgal)
    key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(zl / 0.03).astype(np.int64)
    _, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
    gi = gi.ravel()
    GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=zl) / cnt
    GW = np.bincount(gi, weights=WW.sum(1))
    NG = len(cnt)

    def wpct(v, w, p):
        o = np.argsort(v)
        cw = np.cumsum(w[o]) / w.sum()
        return float(np.interp(p / 100.0, cw, v[o]))

    XR = {}
    for f in FOOTS:
        a0 = L100.A0[f]
        rta = np.array([L100.r_ta_law(GM[g], a0, GZ[g]) for g in range(NG)])
        XR[f] = np.sqrt(L100.G_MPC * GM / a0) / rta
    k4 = {f: wpct(X_E * XR[f], GW, 50) for f in FOOTS}
    K4 = abs(k4["canonical"] - 0.0377) <= 0.001 and abs(k4["alt"] - 0.0327) <= 0.001
    P(f"[K4] KiDS median at 5.8498 r_M: {k4['canonical']:.4f} / {k4['alt']:.4f} -> {'PASS' if K4 else 'FAIL'}")
    R["controls"]["K4"] = {"pass": bool(K4)}
    for cand in SGRID:
        for f in FOOTS:
            sg = np.array([s_of(cand, f, M) for M in GM])
            xe = x_for_phantom(np.maximum(sg, 1e-8)) * XR[f]
            BONUS[cand]["kids"][f] = {"median": wpct(xe, GW, 50), "p16": wpct(xe, GW, 16), "p84": wpct(xe, GW, 84)}
        BONUS[cand]["kids"]["pass"] = all(0.3 <= BONUS[cand]["kids"][f]["median"] <= 0.5 for f in FOOTS)
        P(f"  (ii) KiDS {cand:15s} " + "; ".join(f"{f} {BONUS[cand]['kids'][f]['median']:.4f}" for f in FOOTS)
          + f" -> {'PASS' if BONUS[cand]['kids']['pass'] else 'FAIL'}")
    # (ii) early-type levels (CFG485 machinery, executed read-only up to its C6 banner)
    p485 = os.path.join(CFGDIR, "CFG485_kids_split_settling_completeness", "cfg485_settling_split.py")
    src = open(p485).read()
    g = {"__file__": p485, "__name__": "lane485"}
    t_ = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index("# ================================================================== C6")], p485, "exec"), g)
    P(f"  CFG485 prefix executed ({time.time() - t_:.0f} s); its controls: {[c['ok'] for c in g['R'].checks]}")
    idx = g["idx"]; C30 = g["C30"]; d_early = g["d_early"]
    blk = slice(15, 30)
    Ci_e = np.linalg.inv(C30[blk, blk][np.ix_(idx, idx)])
    LMG, ZG, RG, rgrid = g["LMG"], g["ZG"], g["RG"], g["rgrid"]
    C7 = g["C"]

    def early_chi2(foot, xfun):
        tables = {}
        for b, zb in enumerate(ZG):
            arr = np.zeros((len(LMG), len(RG)))
            for a_, lm in enumerate(LMG):
                Mb = 10 ** lm * (1 + g["fcold"](lm))
                re = float(g["r_M"](Mb, foot)) * xfun(Mb)
                ML = np.asarray(C7.M_law(Mb, np.minimum(rgrid, re), C7.A0[foot], C7.nu_mono), float)
                arr[a_] = g["project"](rgrid, ML - Mb, RG)
            tables[(foot, b)] = arr
        cb = g["contrib"](1, foot, tables, g["DF"][foot][1])
        Ph, Bar, T, _ = g["parts"](cb)
        return g["chi2_free"](d_early[idx] - (Ph + Bar)[idx], Ci_e, T[idx])

    k5 = {f: early_chi2(f, lambda Mb: X_E)[0] for f in FOOTS}
    K5 = abs(k5["canonical"] - 30.5) <= 0.5 and abs(k5["alt"] - 38.1) <= 0.5
    P(f"[K5] early-type chi2 at 5.8498 r_M: {k5['canonical']:.2f} / {k5['alt']:.2f} -> {'PASS' if K5 else 'FAIL'}")
    R["controls"]["K5"] = {"pass": bool(K5)}
    for cand in SGRID:
        for f in FOOTS:
            c2_, A_ = early_chi2(f, lambda Mb, c=cand, ff=f: float(x_for_phantom(max(s_of(c, ff, Mb), 1e-8))))
            BONUS[cand]["early"][f] = {"chi2": c2_, "A_2h": A_}
        BONUS[cand]["early"]["pass"] = all(BONUS[cand]["early"][f]["chi2"] <= 12.59 for f in FOOTS)
        P(f"  (ii) early {cand:15s} " + "; ".join(f"{f} chi2 {BONUS[cand]['early'][f]['chi2']:.2f}" for f in FOOTS)
          + f" -> {'PASS' if BONUS[cand]['early']['pass'] else 'FAIL'}")
    R["bonus"] = BONUS
    R["s_grid"] = {c: {f: v.tolist() for f, v in d.items()} for c, d in SGRID.items()}
    R["s_grid_lgM"] = LG.tolist()

# ======================================================================================================== verdict
P("\n" + "=" * 118)
P("VERDICT TABLE")
P("=" * 118)
other = os.path.join(HERE, ("cfg497_results_MUTATE" if not MUT else "cfg497_results") + ("_TEST" if TESTN else "") + ".json")
OTH = json.load(open(other)) if os.path.exists(other) else None
TROW = {}
for cand in CANDS:
    if MUT:
        src = CELLS[cand]
    else:
        src = OTH["cells"][cand] if OTH else None
    if src is None:
        TROW[cand] = None
        continue
    vv = list(src.values())
    lo, hi = 0.9 * 2 * S_TRUE, 1.1 * 2 * S_TRUE
    ok = all(v["s"] is not None and np.isfinite(v["s"]) and lo <= v["s"] <= hi and v["pur"] is not None and v["pur"] >= 0.9 for v in vv)
    ss = [v["s"] for v in vv if v["s"] is not None and np.isfinite(v["s"])]
    TROW[cand] = {"pass": bool(ok), "s_min": min(ss) if ss else None, "s_max": max(ss) if ss else None}
MROW_TRUE = MROW if not MUT else ({c: OTH["crit"]["M"][c] for c in CANDS} if OTH else None)
P(f"  {'candidate':15s} {'(M) s_sel range (true)':>24s} {'hits':>6s} {'(T) s_sel range (2S)':>22s} {'(iii) G9':>9s}  constants")
rows = {}
for cand in CANDS:
    mr = MROW_TRUE[cand] if MROW_TRUE else None
    tr = TROW[cand]
    g9 = G9[cand][0]
    fm = lambda x: "nan" if x is None else f"{x:.2f}"
    mtxt = (f"{fm(mr['s_min'])}-{fm(mr['s_max'])} {'P' if mr['pass'] else 'F'}") if mr else "n/a"
    ttxt = (f"{fm(tr['s_min'])}-{fm(tr['s_max'])} {'P' if tr['pass'] else 'F'}") if tr else "n/a (run MUTATE)"
    P(f"  {cand:15s} {mtxt:>24s} {(str(mr['n_hit']) + '/' + str(mr['n_cells'])) if mr else '':>6s} {ttxt:>22s} "
      f"{'PASS' if g9 else 'FAIL':>9s}  {CONSTS[cand]}; G9: {G9[cand][1]}")
    der = bool(mr and tr and mr["pass"] and tr["pass"] and g9)
    label = "DERIVES" if der else ("COINCIDENCE" if (mr and mr["pass"] and tr and not tr["pass"]) else "FAIL")
    rows[cand] = {"M": mr, "T": tr, "G9": g9, "G9_why": G9[cand][1], "constants": CONSTS[cand], "label": label}
if not MUT:
    for c in CTRLS:
        vv = list(CELLS[c].values())
        P(f"  control {c:12s} s_sel {min(v['s'] for v in vv):.3f}-{max(v['s'] for v in vv):.3f}, purity "
          f"{min(v['pur'] for v in vv):.3f}-{max(v['pur'] for v in vv):.3f} (reads the label / inserts S: RESTATEMENT)")
complete = all(TROW[c] is not None for c in CANDS) and MROW_TRUE is not None
LANE = ("DERIVES" if any(r["label"] == "DERIVES" for r in rows.values()) else "NOT DERIVED") if complete else "INCOMPLETE (other run missing)"
P(f"\n  LANE VERDICT: {LANE}")
R["crit"] = {"M": MROW, "T": TROW, "rows": rows, "lane": LANE}

EXIT = 0
if MUT:
    tv = [CELLS[c][k]["s"] for c in CTRLS for k in CELLS[c]]
    teeth = all(abs(s / (2 * S_TRUE) - 1) <= 0.05 for s in tv)
    P(f"\nMUTATE teeth (R1/R2 move to 10.728 +-5%): s_sel {min(tv):.3f}-{max(tv):.3f} -> {'DETECTED' if teeth else 'NOT DETECTED'}")
    R["teeth"] = bool(teeth)
    EXIT = 1 if teeth else 0
else:
    CTRL = all(R["controls"][k]["pass"] for k in ("K1", "K2", "K3", "K4", "K5", "K6"))
    P(f"\nCONTROLS K1-K6: {'ALL PASS' if CTRL else 'FAILURE'}")
    EXIT = 0 if CTRL else 1


def jsafe(o):
    if isinstance(o, dict):
        return {str(k): jsafe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsafe(v) for v in o]
    if isinstance(o, np.ndarray):
        return jsafe(o.tolist())
    if isinstance(o, (np.floating, float)):
        return float(o) if np.isfinite(o) else None
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


P("\nkappa = 1/2 FITTED; footings never pooled; the cold fluid's mass is still required (no particle); not 'theory closed'.")
R["runs"] = {str(q): {"z_d": RUNS[q]["z_d"], "z_ta": RUNS[q]["z_ta"], "kb": RUNS[q]["kb"], "M_ta_over_Mb": RUNS[q]["su"]["M_ta"] / M_SIM,
                      "r_ta0": RUNS[q]["su"]["r_ta0"], "partner_over_SMb": RUNS[q]["partner_over_SMb"]} for q in QS}
json.dump(jsafe(R), open(os.path.join(HERE, f"cfg497_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg497{TAG}.out"), "w").write("\n".join(_LOG) + "\n")
sys.exit(EXIT)
