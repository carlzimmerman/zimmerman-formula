#!/usr/bin/env python3
"""CFG494: is the supply postulate (settled cold = 5.364 x the galaxy's baryons) supplied by adiabatic initial conditions?
Criteria: FROZEN_CRITERIA.md (committed alone first, cbfc9b04b).

Readings: LP-G (the settled cold is the Lagrangian partner of the galaxy's dissipated baryons; LIVE / SET for expelled
baryons) and LP-H (the partner of every baryon in the halo's collapsed Lagrangian patch; infall catchment and law turnaround).
Scored on (a) G9, (b) pairing at the dissipation time, (c) KiDS window + CFG485 early-type levels, (d) cluster unsettled
fraction.

kappa = 1/2 is FITTED. Both footings scored separately, never pooled. No dark-matter particle is added: the cold fluid's mass
is still required and its amount (Omega_c/Omega_b = 5.364) is an input. Offline numerics on committed record files only; no
downloads. This is not "theory closed".

Run:  python3 cfg494_adiabatic.py                    (exit 0 iff controls K1-K5 pass)
      CFG494_MUTATE=1 python3 cfg494_adiabatic.py    (coherent isocurvature labels; exit 1 iff the teeth are detected)
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
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
REPO = os.path.dirname(CFGDIR)
sys.path.insert(0, CFGDIR)
import CFG4_common as C4  # noqa: E402  (nu_mono = FP1's committed kernel; constants)

MUT = os.environ.get("CFG494_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
os.environ.pop("CFG488_MUTATE", None)
os.environ.pop("CFG485_MUTATE", None)
try:
    os.nice(15)
except OSError:
    pass

sys.path.insert(0, os.path.join(CFGDIR, "CFG488_cosettling_supply"))
import cfg488_infall as IF  # noqa: E402  (CFG118's machinery as copied by CFG488; imported read-only, MUTATE off)

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


S = 5.364
FB = 1.0 / (1.0 + S)
X_E = 1.0 / math.log(1.0 + 1.0 / S)
FOOTS = C4.FOOTS
LOGMB = [9.0, 10.5, 11.5]
QS = (0.05, 0.1, 0.2)
NS, NS_RES = 20000, 5000
M_SIM = IF.M_SIM
G = IF.G
H0 = IF.H0
assert IF.SHARE == S and not IF.MUT
R = {"lane": "CFG494", "mutate": MUT, "kappa": "1/2 FITTED", "S": S, "f_b": FB, "x_e": X_E, "controls": {}, "runs": {},
     "crit": {}, "reported": {}}

P("=" * 118)
P(f"CFG494 supply from adiabatic initial conditions   MUTATE={MUT}")
P(f"S = Omega_c/Omega_b = {S} (f_b = {FB:.6f}); x_e = 1/ln(1+1/S) = {X_E:.5f} r_M; footings never pooled; kappa = 1/2 FITTED")
P("=" * 118)


def nu(y):
    return C4.nu_mono(np.maximum(np.asarray(y, float), 1e-300))


# ---------------------------------------------------------------- K5
mph_xe = float(nu(1.0 / X_E ** 2) - 1.0)
K5 = abs(X_E - 5.8498) < 1e-3 and abs(mph_xe / S - 1) < 1e-6
P(f"\n[K5] x_e = {X_E:.6f}; nu_mono point phantom at x_e = {mph_xe:.9f} M_b vs S = {S}: rel {mph_xe / S - 1:+.1e} -> "
  f"{'PASS' if K5 else 'FAIL'}")
R["controls"]["K5"] = {"pass": bool(K5), "x_e": X_E, "mph_at_xe": mph_xe}


# ======================================================================================================== infall runs
def integrate(L, Pp, r0, v0, tsnap):
    """IF.integrate, also returning j^2 (needed for the reported energy rank)."""
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


def ratio_profile(Mk, M_ta, mode):
    """the shells' cold/baryon ratio: adiabatic S; MUTATE coherent isocurvature S 2^(1/2 - m/M_ta) (S/sqrt2 beyond M_ta);
    random: S 2^(u - 1/2), u ~ U(0,1), seed 494 (mean-preserving to 2%)."""
    if mode == "adiabatic":
        return np.full(len(Mk), S)
    if mode == "coherent":
        return S * 2.0 ** (0.5 - np.minimum(Mk / M_ta, 1.0))
    rng = np.random.default_rng(494)
    return S * 2.0 ** (rng.random(len(Mk)) - 0.5)


def a_of_t(t, eds):
    return IF.a_of_t(t, eds)


def rho_crit(t, eds):
    a = a_of_t(t, eds)
    Hh = H0 * math.sqrt((1.0 / a ** 3) if eds else (IF.OM / a ** 3 + IF.OL))
    return 3.0 * Hh * Hh / (8.0 * math.pi * G)


def run(kind, q, N, label_modes):
    t0r = time.time()
    cos = "EdS" if kind == "HB" else "LCDM"
    su = IF.setup(M_SIM, cos)
    eds, Om_, OL_, fsm, ocold = IF.cosmo(cos)
    m = su["M_out"] / N
    Mk = m * (np.arange(N) + 0.5)
    r0 = (3.0 * Mk / (4.0 * math.pi * su["rhoci"])) ** (1.0 / 3.0)
    v0 = su["Hi"] * r0
    mk_P = lambda ns: IF.Params(eds, H0, Om_, OL_, fsm, G, 1, M_SIM, su["soft"], 1.0, N, m, q, su["t0"], su["t1"], IF.KMAX,
                                IF.KF, IF.ETA, IF.ETAH, ns)
    # pass 1: turnaround times only
    o1 = integrate(LIB, mk_P(1), r0, v0, np.array([su["t1"]]))
    cold_frac = 1.0 if kind == "HN" else 1.0 - FB
    mc = m * cold_frac                                   # cold mass per shell
    out = {"setup": su, "m": m, "N": N, "kind": kind, "q": q, "labels": {}}
    # labels per mode
    labs = {}
    for mode in label_modes:
        if kind == "HN":
            bk = m / ratio_profile(Mk, su["M_ta"], mode)
        else:
            bk = np.full(N, m * FB)                       # H-B: shells of total matter in the cosmic ratio (adiabatic only)
        cb = np.concatenate([[0.0], np.cumsum(bk)[:-1]])
        w = np.clip((M_SIM - cb) / bk, 0.0, 1.0)
        kb = int(np.max(np.where(w > 0)[0]))
        labs[mode] = dict(w=w, kb=kb, partner=float(np.sum(w) * mc))
    # times (from the scored label mode)
    tta = o1["t_ta"]
    turned = np.isfinite(tta) & (tta > 0)
    times = {}
    for mode, L_ in labs.items():
        tb = float(tta[L_["kb"]])
        td = min(2.0 * tb, su["t1"] * (1.0 - 2e-6))
        L_.update(t_ta_kb=tb, t_d=td, t_d_capped=bool(2.0 * tb > su["t1"] * (1.0 - 2e-6)))
        times[f"{mode}:half"] = 0.5 * tb
        times[f"{mode}:tta"] = tb
        times[f"{mode}:td"] = td
        times[f"{mode}:td+"] = td * (1.0 + 1e-6)
        for i, ts_ in enumerate(np.geomspace(tb * 1.05, su["t1"] * 0.999, 30)):    # POST-HOC epoch scan (print only)
            times[f"{mode}:scan{i:02d}"] = float(ts_)
    for zz in (2.0, 1.0):
        ae = 1.0 / (1.0 + zz)
        times[f"z{zz:.0f}"] = IF.t_of_a(ae, eds == 1)
    times["z0"] = su["t1"]
    keys = sorted(times, key=lambda k: times[k])
    tarr = np.array([times[k] for k in keys])
    o2 = integrate(LIB, mk_P(len(tarr)), r0, v0, tarr)
    same = float(np.max(np.abs(o2["r"] - o1["r"]) / np.maximum(o1["r"], 1e-30)))
    snaps = {k: o2["snap"][i] for i, k in enumerate(keys)}
    # turnaround radius as a function of time (shells' own turnaround records; monotone in k before crossing)
    o_ = np.argsort(tta[turned])
    T_ta, R_ta = tta[turned][o_], o2["r_ta"][turned][o_]

    def R_ta_at(t):
        return float(np.interp(t, T_ta, R_ta))

    def enclosed(rs, R):
        return np.sum(rs < R)

    def comp_pur(rs, R, w):
        inside = rs < R
        part = float(np.sum(w[inside]) * mc)
        allc = float(np.sum(inside) * mc)
        return part, allc

    def R200(rs, t):
        o = np.argsort(rs)
        rsort = rs[o]
        Menc = M_SIM + mc * (np.arange(N) + 1) if kind == "HN" else M_SIM + m * (np.arange(N) + 1)
        rho = Menc / (4.0 / 3.0 * math.pi * rsort ** 3)
        ok = np.where(rho >= 200.0 * rho_crit(t, eds == 1))[0]
        return float(rsort[ok[-1]]) if len(ok) else float("nan")

    def energy_rank(rs, rs2, dt, w, target):
        v = (rs2 - rs) / dt
        o = np.argsort(rs)
        rsort = rs[o]
        msh = m if kind == "HB" else mc
        Min = M_SIM + msh * np.arange(N)                                     # mass strictly inside each shell (+ core)
        outer = np.concatenate([np.cumsum((msh / rsort)[::-1])[::-1][1:], [0.0]])
        phi_s = -G * (Min / rsort + outer) - G * 0.5 * msh / rsort
        phi = np.empty(N); phi[o] = phi_s
        E = 0.5 * v * v + 0.5 * o2["j2"] / np.maximum(rs, 1e-30) ** 2 + phi
        oe = np.argsort(E)
        cum = np.cumsum(np.full(N, mc))
        n = int(np.searchsorted(cum, target))
        sel = oe[:n + 1]
        return float(np.sum(w[sel]) * mc / (cum[n]))

    for mode, L_ in labs.items():
        w = L_["w"]
        rec = {"kb": L_["kb"], "partner_cold_over_SMb": L_["partner"] / (S * M_SIM), "t_ta_kb": L_["t_ta_kb"],
               "t_d": L_["t_d"], "t_d_capped": L_["t_d_capped"], "z_ta_kb": 1.0 / a_of_t(L_["t_ta_kb"], eds == 1) - 1.0,
               "z_d": 1.0 / a_of_t(L_["t_d"], eds == 1) - 1.0, "at": {}}
        # K2: before the boundary shell turns around, the sphere of its own radius holds partners only
        rs = snaps[f"{mode}:half"]
        part, allc = comp_pur(rs, rs[L_["kb"]] * (1 + 1e-12), w)
        rec["K2_purity"] = part / allc if allc > 0 else float("nan")
        for tk in ("tta", "td", "z2", "z1", "z0"):
            key = f"{mode}:{tk}" if tk in ("tta", "td") else tk
            t = times[key] if tk != "td" else L_["t_d"]
            rs = snaps[key]
            row = {"t": t, "z": 1.0 / a_of_t(t, eds == 1) - 1.0}
            for nm, Rr in (("R_ta", R_ta_at(t)), ("R_200", R200(rs, t))):
                part, allc = comp_pur(rs, Rr, w)
                row[nm] = {"R_kpc_sim": Rr, "C": part / (S * M_SIM), "Pi": part / allc if allc > 0 else float("nan"),
                           "all_cold_over_SMb": allc / (S * M_SIM)}
            # R_S: the sphere holding exactly S M_b of cold (restatement selector)
            rsort = np.sort(rs)
            nS = int(math.ceil(S * M_SIM / mc))
            RS = float(rsort[min(nS, N) - 1]) * (1 + 1e-12)
            part, allc = comp_pur(rs, RS, w)
            row["R_S"] = {"R_kpc_sim": RS, "C": part / (S * M_SIM), "Pi": part / allc}
            # R_edge per cell (restatement selector)
            row["R_edge"] = {}
            for f in FOOTS:
                for lm in LOGMB:
                    Mb = 10 ** lm
                    Re_sim = X_E * IF.r_M_kpc(Mb, f) * (M_SIM / Mb) ** (1.0 / 3.0)
                    part, allc = comp_pur(rs, Re_sim, w)
                    row["R_edge"][f"{f}|{lm}"] = {"R_over_Rta": Re_sim / R_ta_at(t), "C": part / (S * M_SIM),
                                                  "Pi": part / allc if allc > 0 else float("nan"),
                                                  "all_cold_over_SMb": allc / (S * M_SIM)}
            rec["at"][tk] = row
        # POST-HOC (added after the first output; print only): does ANY epoch give a label-free sphere C >= 0.9 and Pi >= 0.9?
        scan = []
        for i in range(30):
            k_ = f"{mode}:scan{i:02d}"
            rs = snaps[k_]; t = times[k_]
            ent = {"t": t, "z": 1.0 / a_of_t(t, eds == 1) - 1.0}
            for nm, Rr in (("R_ta", R_ta_at(t)), ("R_200", R200(rs, t))):
                part, allc = comp_pur(rs, Rr, w)
                ent[nm] = {"C": part / (S * M_SIM), "Pi": part / allc if allc > 0 else float("nan")}
            scan.append(ent)
        rec["posthoc_scan"] = scan
        # energy rank at t_d (reported; S inserted)
        rec["energy_rank_purity_td"] = energy_rank(snaps[f"{mode}:td"], snaps[f"{mode}:td+"],
                                                   times[f"{mode}:td+"] - times[f"{mode}:td"], w, S * M_SIM)
        out["labels"][mode] = rec
    out["cold_in_Rta_z0_over_Mb"] = float(enclosed(snaps["z0"], R_ta_at(su["t1"])) * mc / M_SIM)
    out["r_ta_z0_sim"] = R_ta_at(su["t1"])
    out["two_pass_max_rel_diff"] = same
    out["seconds"] = time.time() - t0r
    return out


label_modes = ("coherent", "random") if MUT else ("adiabatic",)
SCORED = label_modes[0]
RUNS = {}
P("\n[infall] H-N (scored) q = 0.05, 0.1, 0.2 at N = 20000; reported: N = 5000 (q = 0.1), H-B (q = 0.1)")
specs = [("HN", q, NS) for q in QS] + ([("HN", 0.1, NS_RES), ("HB", 0.1, NS)] if not MUT else [])
for kind, q, N in specs:
    modes = label_modes if kind == "HN" else ("adiabatic",)
    r_ = run(kind, q, N, modes)
    RUNS[f"{kind}|{q}|{N}"] = r_
    P(f"  {kind} q={q:.2f} N={N}: {r_['seconds']:.0f} s; two-pass identity {r_['two_pass_max_rel_diff']:.1e}; "
      f"cold inside r_ta(z=0) = {r_['cold_in_Rta_z0_over_Mb']:.3f} M_b")
R["runs"] = {k: {kk: vv for kk, vv in v.items() if kk != "setup"} | {"M_ta": v["setup"]["M_ta"], "r_ta0": v["setup"]["r_ta0"]}
             for k, v in RUNS.items()}

# ---------------------------------------------------------------- K1, K2
P("\n[K1] H-N set-up vs CFG118/CFG488; partner cold from labels")
k1 = []
for q in QS:
    r_ = RUNS[f"HN|{q}|{NS}"]
    su = r_["setup"]
    ok = (abs(su["M_ta"] / M_SIM / 23.632 - 1) <= 0.01 and abs(su["r_ta0"] / 507.94 - 1) <= 0.01
          and abs(r_["cold_in_Rta_z0_over_Mb"] / 23.632 - 1) <= 0.01 and r_["two_pass_max_rel_diff"] < 1e-9)
    pc = r_["labels"][SCORED]["partner_cold_over_SMb"]
    if not MUT:
        ok = ok and abs(pc - 1) < 1e-9
    k1.append(ok)
    P(f"  q = {q:.2f}: M_ta/M_b = {su['M_ta'] / M_SIM:.3f}, r_ta0 = {su['r_ta0']:.2f} kpc, cold in r_ta(z=0) = "
      f"{r_['cold_in_Rta_z0_over_Mb']:.3f} M_b; partner cold / (S M_b) = {pc:.12f}; {'ok' if ok else 'MISS'}")
K1 = all(k1)
P(f"  -> K1 {'PASS' if K1 else 'FAIL'}" + (" (MUTATE: partner = S M_b not required)" if MUT else ""))
R["controls"]["K1"] = {"pass": bool(K1)}
k2v = [RUNS[f"HN|{q}|{NS}"]["labels"][SCORED]["K2_purity"] for q in QS]
K2 = all(v >= 0.99 for v in k2v)
P(f"[K2] purity inside the boundary shell's own radius at t_ta(k_b)/2: " + ", ".join(f"{v:.5f}" for v in k2v)
  + f" -> {'PASS' if K2 else 'FAIL'}")
R["controls"]["K2"] = {"pass": bool(K2), "values": k2v}

# ======================================================================================================== LP-G pairing / G9
P("\n" + "=" * 118)
P(f"LP-G: Lagrangian partner of the galaxy's baryons (labels: {SCORED})")
P("=" * 118)
P("  self-similar set-up: C and Pi at R_ta / R_200 / R_S are the same for every mass; R_edge differs per cell")
for q in QS:
    rec = RUNS[f"HN|{q}|{NS}"]["labels"][SCORED]
    P(f"  q = {q:.2f}: boundary shell k_b = {rec['kb']}; t_ta(k_b) = {rec['t_ta_kb'] * 0.9778:.3f} Gyr (z {rec['z_ta_kb']:.2f}); "
      f"t_d = 2 t_ta = {rec['t_d'] * 0.9778:.3f} Gyr (z {rec['z_d']:.2f}){' CAPPED at z=0' if rec['t_d_capped'] else ''}; "
      f"partner cold / (S M_b) = {rec['partner_cold_over_SMb']:.4f}")
    for tk in ("tta", "td", "z2", "z1", "z0"):
        row = rec["at"][tk]
        P(f"     {tk:4s} (z {row['z']:5.2f}): R_ta  C {row['R_ta']['C']:.4f} Pi {row['R_ta']['Pi']:.4f} (all cold {row['R_ta']['all_cold_over_SMb']:.3f} S M_b) | "
          f"R_200 C {row['R_200']['C']:.4f} Pi {row['R_200']['Pi']:.4f} (all {row['R_200']['all_cold_over_SMb']:.3f}) | "
          f"R_S C=Pi {row['R_S']['C']:.4f}")
    for tk in ("td", "z0"):
        row = rec["at"][tk]
        P(f"     R_edge at {tk}: " + "; ".join(f"{k} C {v['C']:.3f} Pi {v['Pi']:.3f} (R/R_ta {v['R_over_Rta']:.3f})"
                                             for k, v in row["R_edge"].items()))
    P(f"     energy rank (most-bound S M_b at t_d, S inserted; reported): purity {rec['energy_rank_purity_td']:.4f}")

P("\n  POST-HOC epoch scan (added after the first output; not a verdict input): epochs where R_200 or R_ta has C >= 0.9 and Pi >= 0.9")
for q in QS:
    sc = RUNS[f"HN|{q}|{NS}"]["labels"][SCORED]["posthoc_scan"]
    ok = [e for e in sc if any(e[nm]["C"] >= 0.9 and e[nm]["Pi"] >= 0.9 for nm in ("R_ta", "R_200"))]
    best = max(sc, key=lambda e: min(e["R_200"]["C"], e["R_200"]["Pi"]))
    P(f"    q = {q:.2f}: {len(ok)} of {len(sc)} epochs" + (f" (z {max(e['z'] for e in ok):.2f} to {min(e['z'] for e in ok):.2f})" if ok else "")
      + f"; best R_200 min(C, Pi) = {min(best['R_200']['C'], best['R_200']['Pi']):.3f} at z {best['z']:.2f} "
      f"(C {best['R_200']['C']:.3f}, Pi {best['R_200']['Pi']:.3f})")

# (b) LP-G
Cb = {q: RUNS[f"HN|{q}|{NS}"]["labels"][SCORED]["at"]["td"]["R_ta"]["C"] for q in QS}
B_LPG = all(0.9 <= v <= 1.1 for v in Cb.values())
# (a) LP-G: label-free selector with C >= 0.9 and Pi >= 0.9 at t_d (R_ta or R_200), every q
a_rows = {}
for q in QS:
    row = RUNS[f"HN|{q}|{NS}"]["labels"][SCORED]["at"]["td"]
    a_rows[q] = {nm: (row[nm]["C"] >= 0.9 and row[nm]["Pi"] >= 0.9) for nm in ("R_ta", "R_200")}
A_LPG = all(any(v.values()) for v in a_rows.values())
P(f"\n  (b) LP-G: C(R_ta(t_d)) = " + ", ".join(f"q {q}: {v:.4f}" for q, v in Cb.items()) + f" -> {'PASS' if B_LPG else 'FAIL'}"
  + " (the partner total is S M_b by the initial composition; C measures only whether it is inside the catchment)")
P(f"  (a) LP-G: label-free selector with C >= 0.9 and Pi >= 0.9 at t_d: "
  + ", ".join(f"q {q}: " + "/".join(f"{k} {'y' if v else 'n'}" for k, v in d.items()) for q, d in a_rows.items())
  + f" -> {'PASS' if A_LPG else 'G9-FAIL'}")

# ======================================================================================================== LP-H pairing
P("\n" + "=" * 118)
P("LP-H: partner of every baryon in the halo's collapsed Lagrangian patch (all turned-around cold)")
P("=" * 118)
B_LPH_inf = {}
for q in QS:
    r_ = RUNS[f"HN|{q}|{NS}"]
    row = r_["labels"][SCORED]["at"]["td"]["R_ta"]
    B_LPH_inf[q] = {"td": row["all_cold_over_SMb"], "z0": r_["cold_in_Rta_z0_over_Mb"] / S}
    P(f"  LP-H/inf q = {q:.2f}: settled partner / (S M_b of the galaxy) = {row['all_cold_over_SMb']:.3f} at t_d, "
      f"{r_['cold_in_Rta_z0_over_Mb'] / S:.3f} at z = 0")
MCATCH = float(np.mean([RUNS[f"HN|{q}|{NS}"]["cold_in_Rta_z0_over_Mb"] for q in QS]))
X_INF = 1.0 / math.log(1.0 + 1.0 / MCATCH)
P(f"  LP-H/inf edge (z = 0 catchment {MCATCH:.3f} M_b, point host): x = 1/ln(1 + 1/{MCATCH:.3f}) = {X_INF:.3f} r_M")

sys.path.insert(0, os.path.join(CFGDIR, "CFG100_kids_mass_rederivation"))
import cfg100_lib as L100  # noqa: E402

YG = np.logspace(-14, 6, 40001)
NUG = nu(YG) - 1.0                                      # decreasing in y


def x_for_phantom(T):
    """x (r_M units) where the point-host phantom M_b(nu(1/x^2) - 1) = T M_b."""
    T = np.asarray(T, float)
    y = np.exp(np.interp(np.log(T), np.log(NUG[::-1]), np.log(YG[::-1])))
    return 1.0 / np.sqrt(y)


B_LPH_law = {}
for f in FOOTS:
    for lm in LOGMB:
        Mb = 10 ** lm
        rta = L100.r_ta_law(Mb, L100.A0[f], 0.0)
        nta = float(L100.nu_mono(L100.G_MPC * Mb / rta ** 2 / L100.A0[f]))
        B_LPH_law[f"{f}|{lm}"] = {"nu_ta": nta, "ratio": (1 - FB) * nta / S,
                                  "x_edge_over_rta": float(x_for_phantom((1 - FB) * nta)) * math.sqrt(L100.G_MPC * Mb / L100.A0[f]) / rta}
P("  LP-H/law (z = 0): settled partner / (S M_b) = f_b nu(r_ta): " + "; ".join(
    f"{k} {v['ratio']:.2f} (nu_ta {v['nu_ta']:.1f}, edge {v['x_edge_over_rta']:.3f} r_ta)" for k, v in B_LPH_law.items()))
B_LPH = all(0.9 <= v["td"] <= 1.1 for v in B_LPH_inf.values()) and all(0.9 <= v["ratio"] <= 1.1 for v in B_LPH_law.values())
P(f"  (b) LP-H: {'PASS' if B_LPH else 'FAIL'};  (a) LP-H: G9-CLEAN by construction (own orbit history + total field)")

# ======================================================================================================== (c1) KiDS window
P("\n" + "=" * 118)
P("(c1) KiDS window: lensing-weighted median x_edge / r_ta over CFG413's lens groups (CFG488's grouping)")
P("=" * 118)
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


KIDS = {}
for f in FOOTS:
    a0 = L100.A0[f]
    rta = np.array([L100.r_ta_law(GM[g], a0, GZ[g]) for g in range(NG)])
    rM = np.sqrt(L100.G_MPC * GM / a0)
    xr = rM / rta
    nta = np.array([float(L100.nu_mono(L100.G_MPC * GM[g] / rta[g] ** 2 / a0)) for g in range(NG)])
    x_law = x_for_phantom((1 - FB) * nta) * xr
    rows = {"LP-G/LIVE": X_E * xr, "LP-H/inf": X_INF * xr, "LP-H/law": x_law}
    KIDS[f] = {nm: {"median": wpct(v, GW, 50), "p16": wpct(v, GW, 16), "p84": wpct(v, GW, 84)} for nm, v in rows.items()}
    KIDS[f]["n_groups"] = int(NG)
    KIDS[f]["f_ret_halo_law_median"] = wpct(1.0 / (FB * nta), GW, 50)
    P(f"  {f:9s}: " + "; ".join(f"{nm} {d['median']:.4f} ({d['p16']:.3f}-{d['p84']:.3f})" for nm, d in KIDS[f].items()
                                 if isinstance(d, dict)) + f"; LP-H/law implied f_ret,halo median {KIDS[f]['f_ret_halo_law_median']:.4f}")
K3 = abs(KIDS["canonical"]["LP-G/LIVE"]["median"] - 0.0377) <= 0.001 and abs(KIDS["alt"]["LP-G/LIVE"]["median"] - 0.0327) <= 0.001
P(f"[K3] LIVE medians {KIDS['canonical']['LP-G/LIVE']['median']:.4f} / {KIDS['alt']['LP-G/LIVE']['median']:.4f} vs CFG488 0.0377 / 0.0327 -> "
  f"{'PASS' if K3 else 'FAIL'}")
R["controls"]["K3"] = {"pass": bool(K3)}
C1 = {nm: all(0.3 <= KIDS[f][nm]["median"] <= 0.5 for f in FOOTS) for nm in ("LP-G/LIVE", "LP-H/inf", "LP-H/law")}

# ======================================================================================================== (c2) early-type levels
P("\n" + "=" * 118)
P("(c2) early-type absolute levels: CFG485 R8 machinery (executed read-only up to its C6 banner), fully settled, truncated")
P("=" * 118)
p485 = os.path.join(CFGDIR, "CFG485_kids_split_settling_completeness", "cfg485_settling_split.py")
src = open(p485).read()
g = {"__file__": p485, "__name__": "lane485"}
t_ = time.time()
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================== C6")], p485, "exec"), g)
P(f"  CFG485 prefix executed ({time.time() - t_:.0f} s); its controls C1-C5: {[c['ok'] for c in g['R'].checks]}")
idx = g["idx"]; C30 = g["C30"]; d_early = g["d_early"]
blk = slice(15, 30)
Ci_e = np.linalg.inv(C30[blk, blk][np.ix_(idx, idx)])
LMG, ZG, RG, rgrid = g["LMG"], g["ZG"], g["RG"], g["rgrid"]
C7 = g["C"]


def early_chi2(foot, tables):
    cb = g["contrib"](1, foot, tables, g["DF"][foot][1])
    Ph, Bar, T, _ = g["parts"](cb)
    return g["chi2_free"](d_early[idx] - (Ph + Bar)[idx], Ci_e, T[idx])


def tables_xfun(foot, xfun):
    """truncated nu_mono phantom tables with edge x(lm, z) r_M (per node and z bin)."""
    out = {}
    for b, zb in enumerate(ZG):
        arr = np.zeros((len(LMG), len(RG)))
        for a, lm in enumerate(LMG):
            Mb = 10 ** lm * (1 + g["fcold"](lm))
            re = float(g["r_M"](Mb, foot)) * xfun(Mb, zb, foot)
            ML = np.asarray(C7.M_law(Mb, np.minimum(rgrid, re), C7.A0[foot], C7.nu_mono), float)
            arr[a] = g["project"](rgrid, ML - Mb, RG)
        out[(foot, b)] = arr
    return out


def x_law_node(Mb, z, foot):
    rta = L100.r_ta_law(Mb, L100.A0[foot], z)
    nta = float(L100.nu_mono(L100.G_MPC * Mb / rta ** 2 / L100.A0[foot]))
    return float(x_for_phantom((1 - FB) * nta))


EARLY = {}
for f in FOOTS:
    EARLY[f] = {}
    for nm, xf in (("LP-G/LIVE", lambda Mb, z, ft: X_E), ("LP-H/inf", lambda Mb, z, ft: X_INF), ("LP-H/law", x_law_node),
                   ("LP-G/SET f_ret 0.10 (reported)", lambda Mb, z, ft: 1.0 / math.log(1.0 + 0.10 / S))):
        c2_, A_ = early_chi2(f, tables_xfun(f, xf))
        EARLY[f][nm] = {"chi2": c2_, "A_2h": A_}
    P(f"  {f:9s}: " + "; ".join(f"{nm} chi2 {d['chi2']:.2f} (A {d['A_2h']:.2f})" for nm, d in EARLY[f].items()))
K4 = abs(EARLY["canonical"]["LP-G/LIVE"]["chi2"] - 30.5) <= 0.5 and abs(EARLY["alt"]["LP-G/LIVE"]["chi2"] - 38.1) <= 0.5
P(f"[K4] 5.8498 r_M fully settled: {EARLY['canonical']['LP-G/LIVE']['chi2']:.2f} / {EARLY['alt']['LP-G/LIVE']['chi2']:.2f} vs "
  f"CFG485 R8 30.5 / 38.1 -> {'PASS' if K4 else 'FAIL'}")
R["controls"]["K4"] = {"pass": bool(K4)}
C2 = {nm: all(EARLY[f][nm]["chi2"] <= 12.59 for f in FOOTS) for nm in ("LP-G/LIVE", "LP-H/inf", "LP-H/law")}

# ======================================================================================================== (d) clusters
P("\n" + "=" * 118)
P("(d) clusters: unsettled fraction of the dark mass inside R500 (CFG453 medians as used by CFG488)")
P("=" * 118)
J453 = json.load(open(os.path.join(CFGDIR, "CFG453_t15_deficit_units", "cfg453_results.json")))
CL = {}
FSTAR = (0.05, 0.10, 0.20)
for f in FOOTS:
    D = J453["D1"][f]
    xA, xT, nucl = D["xA"]["cl"], D["xT"]["cl"], D["nu"]["cl"]
    urec = [S * a / t for a, t in zip(xA, xT)]
    lo, hi = min(urec), max(urec)
    lpg = {}
    for fs in FSTAR:
        settled = min(nucl - 1.0, S * fs)
        lpg[fs] = [1.0 - settled / xT[0], 1.0 - settled / xT[1]]
    f_need = (1.0 - hi) * xT[0] / S
    CL[f] = {"range": [lo, hi], "nu_minus_1": nucl - 1, "xT": xT, "LP-G": lpg, "LP-G_fstar_needed_b0": f_need,
             "LP-H_free": 0.0, "LP-H_inplace": 1.0 - min(nucl - 1.0, S) / S}
    P(f"  {f:9s}: record range [{lo:.4f}, {hi:.4f}]; nu-1 = {nucl - 1:.3f}; x_T15 = {xT[0]:.3f}/{xT[1]:.3f}")
    P("             LP-G (settled = S f_* M_b, f_* RECALLED): " + "; ".join(f"f_* {k}: u = {v[0]:.3f}/{v[1]:.3f}" for k, v in lpg.items())
      + f"; f_* needed to reach u = {hi:.3f} at b = 0: {f_need:.3f}")
    P(f"             LP-H: free placement u = 0.000; in place (reported) u = {CL[f]['LP-H_inplace']:.4f}")
D_ = {"LP-G": all(any(all(CL[f]["range"][0] <= u <= CL[f]["range"][1] for u in CL[f]["LP-G"][fs]) for fs in FSTAR) for f in FOOTS),
      "LP-H": False}
P(f"  (d): LP-G {'PASS' if D_['LP-G'] else 'FAIL'} (any recalled f_*), LP-H (free) FAIL")

# ======================================================================================================== verdict
P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
rows = {
    "LP-G/LIVE": dict(a=A_LPG, b=B_LPG, c=C1["LP-G/LIVE"] and C2["LP-G/LIVE"], d=D_["LP-G"]),
    "LP-G/SET": dict(a=A_LPG, b=B_LPG, c=False, d=D_["LP-G"]),
    "LP-H/inf": dict(a=True, b=all(0.9 <= v["td"] <= 1.1 for v in B_LPH_inf.values()), c=C1["LP-H/inf"] and C2["LP-H/inf"], d=False),
    "LP-H/law": dict(a=True, b=all(0.9 <= v["ratio"] <= 1.1 for v in B_LPH_law.values()), c=C1["LP-H/law"] and C2["LP-H/law"], d=False),
}
P(f"  {'reading':10s} {'(a) G9':>9s} {'(b) pair':>9s} {'(c1) KiDS':>10s} {'(c2) early':>11s} {'(c)':>5s} {'(d)':>5s}  DERIVES")
for nm, d in rows.items():
    c1s = "COND" if nm == "LP-G/SET" else ("PASS" if C1[nm] else "FAIL")
    c2s = "COND" if nm == "LP-G/SET" else ("PASS" if C2[nm] else "FAIL")
    d["derives"] = bool(d["a"] and d["b"] and (d["c"] or d["d"]))
    P(f"  {nm:10s} {('PASS' if d['a'] else 'FAIL'):>9s} {('PASS' if d['b'] else 'FAIL'):>9s} {c1s:>10s} {c2s:>11s} "
      f"{('PASS' if d['c'] else 'FAIL'):>5s} {('PASS' if d['d'] else 'FAIL'):>5s}  {'YES' if d['derives'] else 'no'}")
any_der = any(d["derives"] for d in rows.values())
restate = (B_LPG and not A_LPG)
LANE = "DERIVES" if any_der else ("NOT DERIVED: RESTATEMENT (initial-condition relabel)" if restate else "NOT DERIVED")
P(f"\n  LANE VERDICT: {LANE}")
R["crit"] = {"rows": rows, "lane": LANE, "C_Rta_td": Cb, "a_rows": {str(k): v for k, v in a_rows.items()},
             "LPH_inf": {str(k): v for k, v in B_LPH_inf.items()}, "LPH_law": B_LPH_law, "kids": KIDS, "early": EARLY,
             "clusters": CL, "x_inf": X_INF, "M_catch": MCATCH}

# ======================================================================================================== reported: resolution, H-B
if not MUT:
    P("\nREPORTED (not verdict inputs)")
    for k in (f"HN|0.1|{NS_RES}", f"HB|0.1|{NS}"):
        rec = RUNS[k]["labels"]["adiabatic"]
        row = rec["at"]["td"]
        P(f"  {k}: z_d {rec['z_d']:.2f}; R_ta C {row['R_ta']['C']:.4f} Pi {row['R_ta']['Pi']:.4f}; R_200 C {row['R_200']['C']:.4f} "
          f"Pi {row['R_200']['Pi']:.4f}; R_S {row['R_S']['C']:.4f}; energy-rank purity {rec['energy_rank_purity_td']:.4f}")

# ======================================================================================================== MUTATE teeth
EXIT = 0
CTRL = all(R["controls"][k]["pass"] for k in ("K1", "K2", "K3", "K4", "K5"))
if MUT:
    P("\nMUTATE: coherent isocurvature labels (cold/baryon x2 across the catchment); teeth = C(R_ta(t_d)) vs S M_b outside [0.9, 1.1]")
    teeth = all(not (0.9 <= Cb[q] <= 1.1) for q in QS)
    for q in QS:
        rr = RUNS[f"HN|{q}|{NS}"]["labels"]
        P(f"  q = {q:.2f}: coherent C = {Cb[q]:.4f} (partner {rr['coherent']['partner_cold_over_SMb']:.4f} S M_b); "
          f"random (reported) C = {rr['random']['at']['td']['R_ta']['C']:.4f} (partner {rr['random']['partner_cold_over_SMb']:.4f} S M_b)")
    P(f"  -> TEETH {'DETECTED' if teeth else 'NOT DETECTED'}")
    R["teeth"] = bool(teeth)
    EXIT = 1 if teeth else 0
else:
    P(f"\nCONTROLS K1-K5: {'ALL PASS' if CTRL else 'FAILURE'}")
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
json.dump(jsafe(R), open(os.path.join(HERE, f"cfg494_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg494{TAG}.out"), "w").write("\n".join(_LOG) + "\n")
sys.exit(EXIT)
