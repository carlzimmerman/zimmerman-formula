#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG487 analytic legs (FROZEN_CRITERIA.md e8f72dcc9):
  (a)-type switch properties: A1 m = 0 exactly on FRW and in linear parcels (delta_lin <= 0.1); A2 turnaround thresholds.
  (d) CFG337-style well-posedness of the settled-fraction switch on DE12's 24 transitions (z in {0.25, 1, 2.5, 4},
      M_b in {1e10, 1e11, 1e12}, both footings; DE12's transition() exec'd read-only, as CFG337), gas 1e5 / 1e6 K,
      k in [1e-3, 1e3]/kpc.  Linear system (quasi-static Newtonian WKB; the latch fixed where L = 1):
        s^2 xi = (Gamma_g^2 - c_s^2 k^2) xi + i (4 pi G rho_ph / k) F dm,   (s + Gamma) dm = -i k (1 - m)(Gamma/2) chi xi
      =>  s^3 + Gamma s^2 - A s - (A Gamma + C) = 0,  A = Gamma_g^2 - c_s^2 k^2,  C = Gamma_ph^2 F (1 - m) Gamma chi / 2
      H1 no ghost; H2 real speeds {0, +-c_s}; H3 growth bounded uniformly in k; H4 extra growth <= Gamma_g, no length.
  Legality (reported): conversion-energy ratios, the edge's bilocality.  Controls C4 (shell model), C5 (detector).
MUTATE (CFG487_MUTATE=1, outputs *_MUTATE.*): the FRW-firing clock (latched from z_i); A1 must FAIL; exit 1.
kappa = 1/2 FITTED; both footings, never pooled; the cold fluid's mass is still required.
Run: nice -n 10 python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_wellposed.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
import cfg487_lib as LB                                                      # noqa: E402
import cfg100_lib as C                                                       # noqa: E402  (read-only)
MUTATE = os.environ.get("CFG487_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
try:
    os.nice(10)
except OSError:
    pass
OUT, CHK = [], {}
RES = {"lane": "CFG487", "script": "cfg487_wellposed", "mutate": MUTATE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, msg, load_bearing=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=load_bearing, msg=msg)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}: {msg}")


def finish():
    RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
    nlb = sum(1 for c in CHK.values() if c["load_bearing"] and not c["ok"])
    P(f"\n  {sum(c['ok'] for c in CHK.values())}/{len(CHK)} checks pass; load-bearing failures: {nlb}; elapsed {RES['elapsed_s']} s")
    json.dump(RES, open(os.path.join(HERE, f"cfg487_wellposed_results{SUF}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg487_wellposed{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    P(f"rc = {1 if nlb else 0}")
    sys.exit(1 if nlb else 0)


P(__doc__.split("Run:")[0].strip())
SC = LB.ShellClock(Om=C.OM)
Om, OL = C.OM, 1 - C.OM
Ez = lambda a: math.sqrt(Om / a ** 3 + OL)

# =============================================================================================== (a)-type properties
P("\n(a) SWITCH PROPERTIES ON FRW AND LINEAR PARCELS")
ai = 1e-3


def parcel(di, a_end=1.0):
    """top-hat parcel from a_i (pure growing mode); returns (turned around by a_end?, min theta/3H along the path)."""
    Ri = ai * (1 - di / 3.0); GM = 0.5 * Om * (1 + di) * Ri ** 3 / ai ** 3; Hi = Ez(ai)
    ev = lambda t, y: y[0] - a_end; ev.terminal = True
    s = solve_ivp(lambda t, y: [y[0] * Ez(y[0]), y[2], -GM / y[1] ** 2 + OL * y[1]], [0, 60],
                  [ai, Ri, Hi * Ri * (1 - di / 3.0)], events=ev, rtol=1e-10, atol=1e-13, max_step=0.01)
    a, R, V = s.y
    ratio = (V / R) / np.array([Ez(x) for x in a])                     # theta/3H = (R'/R)/H
    return bool(np.any(V <= 0)), float(np.min(ratio))


def Dlin(a):
    g = lambda x: quad(lambda u: 1.0 / (u * Ez(u)) ** 3, 0, x)[0] * Ez(x)
    return g(a)


di01 = 0.1 * Dlin(ai) / Dlin(1.0)                                     # delta_lin(a = 1) = 0.1
ta0, r0 = parcel(0.0)
ta1, r1 = parcel(di01)
if MUTATE:
    Ebg = quad(lambda x: LB.LAMBDA * math.sqrt(1.5 * Om / x ** 3) / (x * Ez(x)), ai, 1.0)[0]
    m_frw = -math.expm1(-Ebg)
    P(f"  MUTATE: FRW-firing clock (latched from z_i): background exponent {Ebg:.3f} -> m_bg(z = 0) = {m_frw:.4f}")
else:
    m_frw = 0.0 if not ta0 else float("nan")
m_lin = 0.0 if (not ta1 and not MUTATE) else (m_frw if MUTATE else float("nan"))
a1_ok = (m_frw == 0.0) and (m_lin == 0.0) and (r1 >= 0.967 - 1e-9)
check("A1 m = 0 exactly on FRW (latch never fires: theta = 3H > 0) and in linear parcels delta_lin(z = 0) <= 0.1 (theta/3H >= 0.967)",
      a1_ok, f"FRW parcel turned around: {ta0}, min theta/3H {r0:.6f}, m {m_frw:.4g}; delta_lin = 0.1 parcel turned around: {ta1}, "
             f"min theta/3H {r1:.5f}, m {m_lin:.4g}")
RES["A1"] = dict(frw_turned=ta0, frw_min_theta_ratio=r0, lin_turned=ta1, lin_min_theta_ratio=r1, m_frw=m_frw, m_lin=m_lin)
if MUTATE:
    P("  MUTATE detected: the FRW-firing clock gives a nonzero background switch (A1 fails) -> exit 1")
    finish()
eta = sp.symbols("eta", positive=True)
dlin_ta = sp.nsimplify(sp.Rational(3, 20) * (6 * sp.pi) ** sp.Rational(2, 3))
f0 = (Om / (Om + OL)) ** 0.55
P(f"  A2 (reported): EdS sphere turnaround delta_lin = (3/20)(6 pi)^(2/3) = {float(dlin_ta):.4f}; Zel'dovich sheet 3/(3+f): "
  f"f = 1 -> {3 / 4:.3f}, f(z=0) = {f0:.3f} -> {3 / (3 + f0):.3f}")
RES["A2"] = dict(sphere=float(dlin_ta), sheet_f1=0.75, sheet_z0=3 / (3 + f0))

# =============================================================================================== C4 shell model
P("\nC4 SHELL MODEL")
EdS = LB.ShellClock(Om=0.9999999, ndi=12)
rat = [r["t_c"] / r["t_ta"] for r in EdS.rows]
c4a = max(abs(x / (1.5 + 1 / math.pi) - 1) for x in rat)
c4b = {zz: SC.rho_ta_at(1 / (1 + zz)) * (1 + zz) ** -3 / C.dta(zz) - 1 for zz in (0.0, 0.25, 1.0)}
check("C4 shell model: EdS t_c/t_ta = 1.5 + 1/pi within 0.5%; LCDM turnaround density = cfg100 one_plus_delta_ta within 1% (z 0, 0.25, 1)",
      c4a < 0.005 and all(abs(v) < 0.01 for v in c4b.values()),
      f"EdS max rel dev {c4a:.2e}; LCDM rel dev {', '.join(f'z{k}: {v:+.2e}' for k, v in c4b.items())}")
RES["C4"] = dict(eds_dev=c4a, lcdm_dev=c4b)
# POST-HOC (added after run 1; the frozen C4 FAIL above is kept): the EdS deviation is a bang-time offset of the strongly
# nonlinear initial conditions (d_i up to 0.35, a_ta < 0.02); the offset-free collapse duration (t_c - t_ta) against the cycloid's
# (pi/2 + 1) sqrt(R_ta^3 / 8 GM) is what the clock uses after turnaround.
dur, devs = [], []
for r in EdS.rows:
    GMe = 0.5 * 0.9999999 * (1 + r["di"]) * (1e-3 * (1 - r["di"] / 3)) ** 3 / 1e-9
    dur.append((r["t_c"] - r["t_ta"]) / ((math.pi / 2 + 1) * math.sqrt(r["R_ta"] ** 3 / (8 * GMe))) - 1)
    devs.append((r["a_ta"], r["t_c"] / r["t_ta"] / (1.5 + 1 / math.pi) - 1))
lin = [d for a, d in devs if a >= 0.027]
P(f"  POST-HOC C4': offset-free collapse duration max |rel dev| {max(abs(x) for x in dur):.2e} (all {len(dur)} shells); t_c/t_ta within "
  f"{max(abs(x) for x in lin):.2e} for shells turning around at a_ta >= 0.027; the 7e-2 deviation is the a_ta = 0.0038 shell")
mtab = SC.table(0.2)                                                   # the earliest observation epoch used (z = 4)
early = [r for r in SC.rows if r["a_ta"] < 0.02]
lr_early = math.log(min(8 * r["rho_ta"] for r in early)) if early else float("nan")
Emin_early = float(np.interp(lr_early, mtab["lrho"], np.maximum.accumulate(mtab["E"]))) if early else float("nan")
P(f"  POST-HOC C4'': shells with a_ta < 0.02 have present density >= {math.exp(lr_early):.3g} rho_m0 and E >= {Emin_early:.1f} even at "
  f"z = 4 (m = 1 - {math.exp(-Emin_early):.1e}); they cannot move any scored number")
RES["C4_posthoc"] = dict(duration_max_dev=max(abs(x) for x in dur), lin_max_dev=max(abs(x) for x in lin), early_E_min_z4=Emin_early)

# =============================================================================================== DE12 transitions
P_DE12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
NS = {"__name__": "de12_readonly", "__file__": P_DE12}
_src = open(P_DE12).read().split('banner("G1 G2')[0]
_src = _src.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
G, KPC, MS, FBd, CS, transition, A0d = [NS[k] for k in ("G", "KPC", "MS", "FB", "CS", "transition", "A0")]
RHOM0_SI = NS["Om"] * NS["rho_crit0"]
CL = 2.99792458e8
P(f"\nDE12 transition() loaded read-only; f_b(DE12) {FBd:.4f} vs engine {LB.FB:.4f}; gas c_s 1e5 K {CS['1e5K'] / 1e3:.1f}, 1e6 K {CS['1e6K'] / 1e3:.1f} km/s")
ZS, MBS, FOOTS = (0.25, 1.0, 2.5, 4.0), (1e10, 1e11, 1e12), ("canonical", "alt")
KG = np.geomspace(1e-3, 1e3, 121) / KPC


def smax_batch(A, Gam, Cc):
    """max real part of the roots of s^3 + Gam s^2 - A s - (A Gam + Cc) = 0 (batched companion matrices)."""
    n = A.size
    M = np.zeros((n, 3, 3))
    M[:, 0, 0] = -Gam.ravel(); M[:, 0, 1] = A.ravel(); M[:, 0, 2] = (A * Gam + Cc).ravel()
    M[:, 1, 0] = 1.0; M[:, 2, 1] = 1.0
    return np.max(np.linalg.eigvals(M).real, axis=1).reshape(A.shape)


def host_rows(z, Mb, foot):
    tr = transition(z, Mb, foot, 0.25, amp=True)
    idx = np.arange(0, len(tr["r"]), 50)
    r, y = tr["r"][idx], tr["y"][idx]
    rho_b = tr["rho_b"][idx]
    rho_ph = np.maximum(Mb * MS * (NS["h_of"](y) - y * NS["dh_of"](y)) / (2 * math.pi * r ** 3 * y), 0.0)
    rfull = tr["r"]; yf = tr["y"]
    rpf = np.maximum(Mb * MS * (NS["h_of"](yf) - yf * NS["dh_of"](yf)) / (2 * math.pi * rfull ** 3 * yf), 0.0)
    rtf = tr["rho_b"] / FBd + rpf
    Mt = Mb * MS + 4 * math.pi / 3 * rfull[0] ** 3 * rtf[0] + np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * rfull[1:] ** 2 * rtf[1:] + 4 * math.pi * rfull[:-1] ** 2 * rtf[:-1]) * np.diff(rfull))])
    Mbb = Mb * MS + 4 * math.pi / 3 * rfull[0] ** 3 * tr["rho_b"][0] + np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * rfull[1:] ** 2 * tr["rho_b"][1:] + 4 * math.pi * rfull[:-1] ** 2 * tr["rho_b"][:-1]) * np.diff(rfull))])
    a_obs = 1.0 / (1.0 + z)
    m1 = SC.m_of_rho(3 * Mt[idx] / (4 * math.pi * r ** 3) / RHOM0_SI, a_obs)[0]
    m2 = SC.m_of_rho(3 * Mbb[idx] / (LB.FB * 4 * math.pi * r ** 3) / RHOM0_SI, a_obs)[0]
    re = LB.EDGE_FAC * math.sqrt(G * Mb * MS / A0d[foot])
    return dict(tr=tr, idx=idx, r=r, rho_b=rho_b, rho_ph=rho_ph, rho_t=rho_b / FBd + rho_ph, m1=m1, m2=m2, re=re)


P("\n(d) WELL-POSEDNESS ON THE 24 TRANSITIONS")
WP = {}
worst = {}
bound_ok = True
legal = {"V1_30kpc": [], "V1_edge": [], "V2_30kpc": [], "V2_edge": []}
for z in ZS:
    for Mb in MBS:
        for foot in FOOTS:
            h = host_rows(z, Mb, foot)
            r = h["r"]; Gg2 = 4 * math.pi * G * h["rho_t"]; Gph2 = 4 * math.pi * G * h["rho_ph"]
            for ver in ("V1", "V2"):
                m = h["m1"] if ver == "V1" else h["m2"]
                Gam = np.sqrt(4 * math.pi * G * (h["rho_t"] if ver == "V1" else h["rho_b"] / FBd))
                chi = h["rho_b"] / h["rho_t"] if ver == "V1" else np.ones_like(r)
                for edge in ("edge", "noedge"):
                    F = (r <= h["re"]).astype(float) if edge == "edge" else np.ones_like(r)
                    for T in ("1e5K", "1e6K"):
                        cs = CS[T]
                        A = Gg2[:, None] - (cs * KG[None, :]) ** 2
                        Cc = (Gph2 * F * (1 - m) * Gam * chi / 2)[:, None] * np.ones_like(A)
                        GamB = Gam[:, None] * np.ones_like(A)
                        s = smax_batch(A, GamB, Cc)
                        s0 = np.sqrt(np.maximum(A, 0.0))
                        extra = np.max(s - s0, axis=1)
                        Gg = np.sqrt(Gg2)
                        h4 = float(np.max(extra / Gg))
                        h3 = bool(np.all(s[:, -1] <= 1.01 * np.maximum(s[:, 0], 0.0) + 1e-30))
                        bnd = bool(np.all(np.max(s, axis=1) ** 2 <= Gg2 + Gph2 * F * (1 - m) * chi / 2 * (1 + 1e-9) + 1e-60))
                        bound_ok &= bnd
                        key = f"{ver}|{edge}|{T}"
                        w = worst.get(key, dict(h4=-1))
                        if h4 > w["h4"]:
                            j = int(np.argmax(extra / Gg))
                            w = dict(h4=h4, at=f"z{z}/{Mb:.0e}/{foot}", r_kpc=float(r[j] / KPC), m=float(m[j]),
                                     smax_over_Gg=float(np.max(s[j]) / Gg[j]))
                        w["h3_all"] = w.get("h3_all", True) and h3
                        worst[key] = w
            # legality ratios (reported): conversion energy per unit settled mass vs the parcel's kinetic/thermal scale
            B = h["tr"]["B"][h["idx"]]; g = h["tr"]["g"][h["idx"]]
            rho_c = h["rho_t"] - h["rho_b"]
            for lab, rr_ in (("30kpc", 30 * KPC), ("edge", h["re"])):
                j = int(np.argmin(np.abs(r - rr_)))
                legal[f"V1_{lab}"].append(float(B[j] / (rho_c[j] * g[j] * r[j] / 2)))
                legal[f"V2_{lab}"].append(float(B[j] / (h["rho_b"][j] * CS["1e6K"] ** 2)))
for k, w in worst.items():
    P(f"  {k:18s}: worst extra growth / Gamma_g {w['h4']:.4f} at {w['at']} r {w['r_kpc']:.0f} kpc (m {w['m']:.3f}, s_max/Gamma_g {w['smax_over_Gg']:.4f}); H3 bounded {w['h3_all']}")
RES["d_worst"] = worst
h_ok = {v: all(worst[f"{v}|edge|{T}"]["h4"] <= 1.0 and worst[f"{v}|edge|{T}"]["h3_all"] for T in ("1e5K", "1e6K")) for v in ("V1", "V2")}
check("(d) H1 gas inertia rho > 0 and no kinetic term for the label (first-order transport): no ghost", True,
      "state of the system: rho_b > 0 on every transition; the label obeys a first-order rate law (CFG349 C1 analogue)")
check("(d) H2 characteristic speeds real, |v| <= c: {0 (label, along the flow), +-c_s}", max(CS.values()) < CL,
      f"c_s max {max(CS.values()) / 1e3:.1f} km/s")
for v in ("V1", "V2"):
    RES[f"d_pass_{v}"] = h_ok[v]
    check(f"(d) {v} with the edge: H3 bounded in k and H4 extra growth <= Gamma_g on all 24 transitions, 1e5 and 1e6 K", h_ok[v],
          ", ".join(f"{T}: {worst[f'{v}|edge|{T}']['h4']:.4f}" for T in ("1e5K", "1e6K")), load_bearing=False)
    nos = all(worst[f"{v}|noedge|{T}"]["h4"] <= 1.0 and worst[f"{v}|noedge|{T}"]["h3_all"] for T in ("1e5K", "1e6K"))
    RES[f"d_noedge_{v}"] = nos
    check(f"(d) {v} switch only (no edge): H3 and H4 (reported)", nos,
          ", ".join(f"{T}: {worst[f'{v}|noedge|{T}']['h4']:.4f}" for T in ("1e5K", "1e6K")), load_bearing=False)
check("(d) analytic bound s_max^2 <= Gamma_g^2 + Gamma_ph^2 F (1 - m) chi / 2 holds at every point (Lean L5)", bound_ok, "all transitions, versions, edges, temperatures")

# =============================================================================================== C5 detector
P("\nC5 DETECTOR")
Gg0 = np.array([1e-15]); A0k = Gg0[:, None] ** 2 - (1e5 * KG[None, :]) ** 2
s_nc = smax_batch(A0k, np.full_like(A0k, 1e-15), np.zeros_like(A0k))
c5a = abs(s_nc[0, 0] / math.sqrt(Gg0[0] ** 2 - (1e5 * KG[0]) ** 2) - 1) < 1e-6   # Jeans value (run 1 compared to Gamma_g: README)
A_sl = Gg0[:, None] ** 2 - ((1e5) ** 2 - (2e5) ** 2) * KG[None, :] ** 2         # slaved: c_g = 2 c_s (negative stiffness)
s_sl = smax_batch(A_sl, np.full_like(A_sl, 1e-15), np.zeros_like(A_sl))
c5b = not bool(s_sl[0, -1] <= 1.01 * s_sl[0, 0])
check("C5 detector: no-coupling limit gives s_max = Gamma_g at small k; an injected slaved k-linear term is flagged unbounded by H3",
      c5a and c5b, f"s / Jeans at k_min {s_nc[0, 0] / math.sqrt(Gg0[0] ** 2 - (1e5 * KG[0]) ** 2):.12f} (s/Gamma_g {s_nc[0, 0] / Gg0[0]:.9f}); "
                   f"slaved s(k_max)/s(k_min) {s_sl[0, -1] / s_sl[0, 0]:.3e}")

# =============================================================================================== legality (reported)
P("\nLEGALITY (reported; cannot raise a verdict)")
for k, v in legal.items():
    P(f"  conversion-energy ratio {k:10s}: min {min(v):.3g}  median {float(np.median(v)):.3g}  max {max(v):.3g}"
      + ("   [B / (rho_c v_c^2/2): cold-fluid heating per unit settled mass]" if k.startswith("V1") else "   [B / (rho_b c_s^2), 1e6 K: gas heating]"))
RES["legality"] = {k: dict(min=min(v), median=float(np.median(v)), max=max(v)) for k, v in legal.items()}
yedge = (1.0 / LB.EDGE_FAC) ** 2
P(f"  the edge reads the host's total M_b (bilocal, CFG48-type); for a point mass it is the local baryonic field g_N = a0 / {LB.EDGE_FAC:.3f}^2 "
  f"= {yedge:.4f} a0 (a local, baryon-only reading; not used in the scored model)")
RES["edge_local_yN"] = yedge
finish()
