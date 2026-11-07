#!/usr/bin/env python3
"""NA1 (criteria FROZEN_CRITERIA.md): the last two untested FA1 doors, graded on both footings, never pooled.
    python3 na1.py            -> na1.json / na1.out
    python3 na1.py --mutate   -> na1_MUTATE.json / na1_MUTATE.out
I5 disformal bulk-motion selector: sympy reduction R, GW, reduced key S1 (FOSD sandwich), S2 (LP), W1 (SV5 web, F on phantom).
I7 defect network of the a0 scalar: D0-D4 analytic with numbers, sympy checks.
SV5 sv5_web imported read-only; FA3 fa3.json read-only. One thread. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, signal
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np, resource, sympy as sp
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # macOS: bytes -> GB

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07")
MUT = "--mutate" in sys.argv; TAG = "na1_MUTATE" if MUT else "na1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def dump(partial=False):
    if partial: OUT.append("PARTIAL: stopped by SIGTERM; nothing graded from this file.")
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
    if not partial: json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, sort_keys=True, default=float)
def on_term(sig, frm): dump(partial=True); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)

A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}
LSTAR = {"canonical": 21.7, "alt": 22.9}
KAPPA = 0.5
NEED = {"canonical": dict(SPARC=(None, 0.33), XCOP=(2.1, 8.4), groups=(0.6, 7.0), dSph=(0.82, 3.28), UDG=(23.6, None), CMB=(1.0, None)),
        "alt":       dict(SPARC=(None, 0.19), XCOP=(1.9, 7.6), groups=(0.45, 5.8), dSph=(0.75, 3.00), UDG=(20.2, None), CMB=(1.0, None))}
FCL_NEED = {"canonical": 4.2, "alt": 3.8}
RES = dict(tag=TAG, criteria="FROZEN_CRITERIA.md (NA1)", note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.", KA={}, I5={}, I7={})
P(f"NA1 {'MUTATE' if MUT else 'MAIN'}: FA1 doors I5 (disformal bulk motion) and I7 (defect network). kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# ================================================================== I5 R: sympy reduction (+ KA3, M3)
P("\n== I5 R: every local scalar of (g, g~, u, X, U, T) vs {gamma, X, B, rho, p} (sympy) ==")
B, X, rho, p, s, th, ph = sp.symbols("B X rho p s theta phi", real=True)
gam = sp.Symbol("gamma", positive=True)
eta = sp.diag(-1, 1, 1, 1); u_lo = sp.Matrix([-1, 0, 0, 0])      # khronon rest frame (local Lorentz frame; scalars are frame-free)
gt = eta + B * X * u_lo * u_lo.T
vv = s * sp.Matrix([sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)])   # matter 3-velocity, direction (th, ph)
G_ = 1 / sp.sqrt(1 - s ** 2)
U_up = G_ * sp.Matrix([1, vv[0], vv[1], vv[2]]); U_lo = eta * U_up
T_up = (rho + p) * U_up * U_up.T + p * eta.inv()
gti = sp.simplify(gt.inv())
scal = {
    "eig(g^-1 g~)": sp.Matrix(eta.inv() * gt).eigenvals(),
    "det g~ / det g": sp.simplify(gt.det() / eta.det()),
    "g~(U,U)": sp.simplify((U_up.T * gt * U_up)[0]),
    "g~^-1(U_lo,U_lo)": sp.simplify((U_lo.T * gti * U_lo)[0]),
    "g~_mn T^mn": sp.simplify(sum(gt[i, j] * T_up[i, j] for i in range(4) for j in range(4))),
    "T.g~.T.g~ trace": sp.simplify((T_up * gt * T_up * gt).trace()),
    "u.U (gamma)": sp.simplify((u_lo.T * U_up)[0] * -1),
}
def reduces(expr):
    """True if expr depends on the matter velocity only through s (|v|), i.e. not on the direction (th, ph):
    then, with s = sqrt(1 - 1/gamma^2), it is a function of {gamma, X, B, rho, p}."""
    if isinstance(expr, dict): return all(reduces(k) for k in expr)
    e = sp.simplify(expr); fs = e.free_symbols - {B, X, rho, p, s, th, ph}
    return (not fs) and sp.simplify(sp.diff(e, th)) == 0 and sp.simplify(sp.diff(e, ph)) == 0
Rrows = {}
for k, e in scal.items():
    ok = reduces(e)
    eg = e if isinstance(e, dict) else sp.simplify(e.subs(s, sp.sqrt(1 - 1 / gam ** 2)))
    Rrows[k] = dict(expr=str(eg), reduces=bool(ok)); P(f"   {k:20s} = {str(eg):60s} reduces: {ok}")
R_pass = all(r["reduces"] for r in Rrows.values())
# KA3: g~(U,U) = -1 + B X gamma^2; light cone c~/c = sqrt(1 - B X)
ka3a = sp.simplify(scal["g~(U,U)"].subs(s, sp.sqrt(1 - 1 / gam ** 2)) - (-1 + B * X * gam ** 2)) == 0
cl = sp.Symbol("ct", positive=True); kvec = sp.Matrix([1, cl, 0, 0])
csol = sp.solve(sp.Eq((kvec.T * gt * kvec)[0], 0), cl)
ka3b = any(sp.simplify(c_ - sp.sqrt(1 - B * X)) == 0 for c_ in csol)
ser = sp.series(scal["g~(U,U)"] + 1 - B * X, s, 0, 5).removeO()
P(f"KA3: g~(U,U) = -1 + B X gamma^2 -> {ka3a}; light cone of g~ in the khronon frame c~/c = {csol} -> sqrt(1 - B X) {ka3b}")
P(f"   gamma-dependent part of g~(U,U): {sp.simplify(ser)}  (= B X (v/c)^2 + O(v^4): DX1 D1's (v/c)^2 <= 1.1e-5 times B X)")
RES["KA"]["KA3"] = dict(gUU=bool(ka3a), light_cone=bool(ka3b), ok=bool(ka3a and ka3b))
RES["I5"]["R"] = dict(rows=Rrows, reduction_shown=bool(R_pass), gamma_part_series=str(sp.simplify(ser)),
                      maps_to={"gamma": "khronon velocity (QX5 iter_c, DEAD)", "p/rho": "p/rho (QX5 iter_b / record, DEAD)",
                               "X": "clock depth (QX5 iter_a / QX6, DEAD)", "B": "function of X", "rho": "enclosed / local density (DEAD key)"})
P(f"R: reduction shown = {R_pass}; F = F(gamma; X, p/rho) -> khronon velocity, clock depth, p/rho: all on the dead list")
if MUT:   # M3: a planted second, matter-independent vector U2 must break the reduction test
    U2 = sp.Matrix([sp.sqrt(2), 1, 0, 0]); Y = sp.simplify((U_up.T * eta * U2)[0])
    m3 = not reduces(Y); RES["MUTATE_M3"] = dict(Y=str(Y), reduction_test_fails=bool(m3), bites=bool(m3))
    P(f"MUTATE M3: planted Y = U.U2 = {Y}; reduction test fails -> {m3} (bites: {m3})")

# GW (P2): |c_T - c_light|/c = 1 - sqrt(1 - BX); GW170817 -3e-15 < dc/c < 7e-16 (PROVISIONAL)
lo_, hi_ = -3e-15, 7e-16
BX_hi = 1 - (1 - hi_) ** 2; BX_lo = 1 - (1 + abs(lo_)) ** 2       # dc/c = 1 - sqrt(1-BX) in [-3e-15, 7e-16] (either sign assignment reported)
BX_max = max(abs(BX_hi), abs(BX_lo))
GW = dict(P2_BX_window=[BX_lo, BX_hi], P2_BX_absmax=BX_max, P2_selector_spread=BX_max * 1.1e-5,
          P2="FAIL (selector argument varies by <= %.1e across all classes; an order-1 switch needs ~1)" % (BX_max * 1.1e-5),
          P1="PASS (CONDITIONAL: photons and gravitons both on g)")
RES["I5"]["GW"] = GW
P(f"GW: P2 (matter on g~): B X in [{BX_lo:.2e}, {BX_hi:.2e}] -> selector spread B X (v/c)^2 <= {BX_max*1.1e-5:.1e}: P2 FAIL; P1: PASS (CONDITIONAL)")

# ================================================================== SV5 web machinery (read-only)
SV5D = os.path.join(CL6, "SV5_growth_mechanism"); sys.path.insert(0, SV5D)
_a = sys.argv; sys.argv = [os.path.join(SV5D, "sv5_web.py")]
import sv5_web as SV
sys.argv = _a
SV1J = json.load(open(os.path.join(SV5D, "iter_1_law_on_web", "sv5_iter1.json")))
FA3J = json.load(open(os.path.join(CL7, "FA3_nonlocal_action_search", "fa3.json")))
QH = {f: FA3J["cands"]["I1"]["foot"][f]["S_host"] for f in A0}
sigA = SV.sigA; WLINE = 3 * sigA; ZG = SV.ZG; MC = SV.N3["M"]; MPC = SV.MPC; CC = SV.CC; Gn = SV.G
ob, od, h = SV.ob, SV.od, SV.h
P(f"\n[peak RSS {rss():.2f} GB] SV5: sigma_A {sigA:.4f} -> W1 line {WLINE:.4f}; ZG {ZG}; solver ob {ob} od {od:.5f} h {h} (od/ob {od/ob:.3f}); FA3 S_host q {QH}")

def Hs(z): return MC.Hubble(z) * CC / MPC
def gfield(dk, z):
    a = 1 / (1 + z); kSI = 1.0 / MPC
    phik = -1.5 * SV.H0s ** 2 * SV.Om * dk / (a * SV.K2 * kSI ** 2); phik[0, 0, 0] = 0
    return [np.real(np.fft.ifftn(-1j * Kc * kSI * phik)) / a for Kc in (SV.KX, SV.KY, SV.KZ)]
def vfield(dk, z, fgr):
    a = 1 / (1 + z); pre = a * Hs(z) * fgr * MPC; d = dk.copy(); d[0, 0, 0] = 0
    return [np.real(np.fft.ifftn(1j * Kc / SV.K2 * d)) * pre for Kc in (SV.KX, SV.KY, SV.KZ)]
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))
def Bof(g, Weff):
    divV = 0; divN = 0
    for Kc, gc, wc in zip((SV.KX, SV.KY, SV.KZ), g, Weff):
        divV = divV + Kc * np.fft.fftn(gc + wc); divN = divN + Kc * np.fft.fftn(gc)
    return SV.shell_mean(np.abs(divV) ** 2) / SV.shell_mean(np.abs(divN) ** 2)
def wquant(x, w, q):
    o = np.argsort(x); c = np.cumsum(w[o]); c /= c[-1]; return float(x[o][np.searchsorted(c, q)])
lowk = (SV.KK > 0) & (SV.KK < 4 * SV.kf)

WR, dV = SV.realise(5)
variants = {f: {} for f in A0}            # name -> list of Bz
thr = {}; web_info = {}; FLOW = None
def fdiv(arr):   # sum_c K_c fftn(arr_c), accumulated one component at a time
    acc = None
    for Kc, x in zip((SV.KX, SV.KY, SV.KZ), arr):
        t = np.fft.fftn(x); t *= Kc; acc = t if acc is None else acc + t; del t
    return acc
for j, z in enumerate(ZG):
    dk, _ = SV.delta_k(WR, dV, z); eps = 0.01; z2 = (1 + z) * (1 + eps) - 1
    dk2, _ = SV.delta_k(WR, dV, z2)
    fgr = -0.5 * math.log((np.abs(dk2[lowk]) ** 2).sum() / (np.abs(dk[lowk]) ** 2).sum()) / math.log(1 + eps); del dk2
    wt = np.maximum(1 + np.real(np.fft.ifftn(dk)), 0.0)
    vel = vfield(dk, z, fgr); sp_ = np.sqrt(vel[0] ** 2 + vel[1] ** 2 + vel[2] ** 2)
    if j == 0:
        rng = np.random.default_rng(11); idx = rng.choice(sp_.size, size=200000, p=(wt / wt.sum()).ravel())
        FLOW = np.stack([vel[k].ravel()[idx] for k in range(3)], axis=1) / 1e3        # km/s vectors
        del idx
    g = gfield(dk, z); del dk
    gn = np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2)
    cos = float((wt * (g[0] * vel[0] + g[1] * vel[1] + g[2] * vel[2]) / np.maximum(gn * sp_, 1e-300)).sum() / wt.sum())
    del vel
    cosa = abs(cos)
    web_info[str(z)] = dict(f_growth=fgr, v_median_kms=wquant(sp_.ravel(), wt.ravel(), 0.5) / 1e3, v_p95_kms=wquant(sp_.ravel(), wt.ravel(), 0.95) / 1e3,
                            v_rms_kms=float(np.sqrt((wt * sp_ ** 2).sum() / wt.sum())) / 1e3, cos_v_g=cos)
    P(f"[z {z:5g}] f {fgr:.4f}; web speed (mass-weighted) median {web_info[str(z)]['v_median_kms']:.1f} p95 {web_info[str(z)]['v_p95_kms']:.1f} rms {web_info[str(z)]['v_rms_kms']:.1f} km/s; |cos(v, g_N)| {cosa:.7f}")
    if j == 0:
        for f in A0:
            q = QH[f]; thr[f] = dict(q=q, inc_vc=wquant(sp_.ravel(), wt.ravel(), 1 - q) / 1e3, dec_vc=wquant(sp_.ravel(), wt.ravel(), q) / 1e3)
            P(f"   [{f}] host fraction q {q:.4f}: increasing step on for v >= {thr[f]['inc_vc']:.1f} km/s; decreasing step on for v <= {thr[f]['dec_vc']:.1f} km/s")
    vk = sp_ / 1e3; del sp_
    divN = fdiv(g); SN = SV.shell_mean(np.abs(divN) ** 2)
    for f, a0 in A0.items():
        n1 = nu(gn / a0) - 1.0
        Fs = {"KA1 F=1": None, "KA2 F=0": 0, "inc step": ("ge", thr[f]["inc_vc"]), "dec step": ("le", thr[f]["dec_vc"])}
        if MUT: Fs = {"M2 F=1[v<=1 km/s]": ("le", 1.0)}
        for name, spec in Fs.items():
            if spec is None: Fv = np.ones_like(vk)
            elif spec == 0: Fv = np.zeros_like(vk)
            else: Fv = (vk >= spec[1]).astype(float) if spec[0] == "ge" else (vk <= spec[1]).astype(float)
            Fn = Fv * n1
            divW = fdiv([Fn * gc for gc in g]); tot = divN + divW; del divW
            variants[f].setdefault(name, []).append(SV.shell_mean(np.abs(tot) ** 2) / SN); del tot, Fn
            variants[f].setdefault(name + " | on-mass", []).append(float((wt * Fv).sum() / wt.sum())); del Fv
        del n1
    web_info[str(z)]["cos_ok"] = bool(cosa >= 0.999999)
    del g, gn, wt, vk, divN
    P(f"   [peak RSS {rss():.2f} GB]")
RES["I5"]["web_info"] = web_info; RES["I5"]["thresholds"] = thr
ka4 = all(w["cos_ok"] for w in web_info.values()); RES["KA"]["KA4"] = dict(ok=bool(ka4), min_abs_cos=min(abs(w["cos_v_g"]) for w in web_info.values()))
P(f"KA4: linear velocity parallel to g_N at every z: {ka4} (min |cos| {RES['KA']['KA4']['min_abs_cos']:.8f})")

W1 = {}
for f in A0:
    W1[f] = {}
    for name, Bz in variants[f].items():
        if name.endswith("| on-mass"): continue
        pr = SV.project(Bz); W1[f][name] = dict(r=pr["r"], W1_pass=bool(abs(pr["r"] - 1) <= WLINE),
                                              on_mass_frac=variants[f].get(name + " | on-mass"))
        P(f"[{f}] W1 {name:20s} r {pr['r']:.6f} -> {'PASS' if abs(pr['r'] - 1) <= WLINE else 'FAIL'}" +
          (f"; web mass with F = 1 by z: {', '.join(f'{x:.3f}' for x in variants[f][name + ' | on-mass'])}" if name + " | on-mass" in variants[f] else ""))
    if not MUT:
        rj = SV1J["foot"][f]["proj"]["r"]; d1 = abs(W1[f]["KA1 F=1"]["r"] / rj - 1); d2 = abs(W1[f]["KA2 F=0"]["r"] - 1)
        RES["KA"].setdefault("KA1", {})[f] = dict(r=W1[f]["KA1 F=1"]["r"], sv5=rj, rel=d1, ok=bool(d1 <= 1e-6))
        RES["KA"].setdefault("KA2", {})[f] = dict(r=W1[f]["KA2 F=0"]["r"], absdiff=d2, ok=bool(d2 <= 1e-9))
        P(f"[{f}] KA1 F=1 r vs SV5 json {rj:.6f}: rel {d1:.1e} -> {'PASS' if d1 <= 1e-6 else 'FAIL'}; KA2 F=0 |r-1| {d2:.1e} -> {'PASS' if d2 <= 1e-9 else 'FAIL'}")
RES["I5"]["W1"] = W1
if MUT:
    m2 = all(W1[f]["M2 F=1[v<=1 km/s]"]["W1_pass"] for f in A0); RES["MUTATE_M2"] = dict(bites=bool(m2))
    P(f"MUTATE M2: planted F = 1[v <= 1 km/s] passes W1 on both footings -> bites: {m2}")
else:
    KAOK = all(RES["KA"][k][f]["ok"] for k in ("KA1", "KA2") for f in A0) and RES["KA"]["KA3"]["ok"] and ka4
    RES["KA_all_I5"] = bool(KAOK)
    if not KAOK: P("KA FAIL (I5): stop; nothing graded."); dump(); sys.exit(2)

# ================================================================== I5 S1/S2: class speed samples
P("\n== I5 S1/S2: class speeds relative to the khronon (cosmic) frame; flow = SV5 z 0.25 mass-weighted linear field ==")
DATA = os.path.join(REPO, "real_research", "data", "sparc_data")
VMAX = []
for fn in sorted(os.listdir(DATA)):
    if not fn.endswith("_rotmod.dat"): continue
    a = np.loadtxt(os.path.join(DATA, fn), comments="#"); a = a[None] if a.ndim == 1 else a
    VMAX.append(float(a[:, 1].max()))
VMAX = np.array(VMAX); P(f"SPARC: {len(VMAX)} galaxies, max V_obs median {np.median(VMAX):.1f} km/s (min {VMAX.min():.1f}, max {VMAX.max():.1f})")
rng = np.random.default_rng(11); NS_ = 200000
def iso(n): x = rng.standard_normal((n, 3)); return x / np.linalg.norm(x, axis=1)[:, None]
def flow(n): return FLOW[rng.integers(0, len(FLOW), n)]
def gauss3(n, s1): return rng.standard_normal((n, 3)) * s1
SPD = {}
SPD["SPARC"] = np.linalg.norm(flow(NS_) + iso(NS_) * VMAX[rng.integers(0, len(VMAX), NS_)][:, None], axis=1)
SPD["XCOP"] = np.linalg.norm(flow(NS_) + gauss3(NS_, 200.0), axis=1)
SPD["groups"] = np.linalg.norm(flow(NS_) + gauss3(NS_, 100.0), axis=1)
SPD["dSph"] = np.linalg.norm(flow(NS_) + gauss3(NS_, 100.0), axis=1)
if MUT:
    SPD["UDG"] = np.linalg.norm(gauss3(NS_, 1.0), axis=1); SPD["CMB"] = rng.uniform(2000.0, 2030.0, NS_)
else:
    SPD["UDG"] = np.linalg.norm(flow(NS_) + gauss3(NS_, 1000.0), axis=1); SPD["CMB"] = rng.uniform(0.0, 30.0, NS_)
for k, v in SPD.items(): P(f"   {k:7s} speed median {np.median(v):7.1f}  p5 {np.percentile(v, 5):7.1f}  p95 {np.percentile(v, 95):7.1f} km/s")
vg = np.arange(0.0, max(v.max() for v in SPD.values()) + 2.0, 1.0)
CDF = {k: np.searchsorted(np.sort(v), vg, side="right") / len(v) for k, v in SPD.items()}
def fosd(A, Bc): d = float(np.max(CDF[A] - CDF[Bc])); return d <= 0.005, d     # A FOSD B: CDF_A <= CDF_B + 0.005
inc_ok, inc_d = fosd("SPARC", "CMB"); dec_ok, dec_d = fosd("UDG", "SPARC")
S1 = {}
for f in A0:
    nd = NEED[f]
    inc_contra = inc_ok and nd["CMB"][0] > nd["SPARC"][1]
    dec_contra = dec_ok and nd["UDG"][0] > nd["SPARC"][1]
    S1[f] = dict(SPARC_fosd_CMB=inc_ok, max_excess_inc=inc_d, UDG_fosd_SPARC=dec_ok, max_excess_dec=dec_d,
                 increasing_F_contradiction=bool(inc_contra), decreasing_F_contradiction=bool(dec_contra),
                 margin_inc=f"<F>_CMB >= {nd['CMB'][0]} vs <F>_SPARC <= {nd['SPARC'][1]}", margin_dec=f"<F>_UDG >= {nd['UDG'][0]} vs <F>_SPARC <= {nd['SPARC'][1]}",
                 status="FAIL (no monotone F)" if (inc_contra and dec_contra) else "NO CONTRADICTION")
    P(f"[{f}] S1: SPARC FOSD CMB {inc_ok} (max CDF excess {inc_d:.4f}) -> increasing F contradiction {inc_contra} ({S1[f]['margin_inc']}); "
      f"UDG FOSD SPARC {dec_ok} (excess {dec_d:.4f}) -> decreasing F contradiction {dec_contra} ({S1[f]['margin_dec']}) => S1 {S1[f]['status']}")
RES["I5"]["S1"] = S1
if MUT:
    m1 = all(S1[f]["status"] == "NO CONTRADICTION" and not S1[f]["increasing_F_contradiction"] and not S1[f]["decreasing_F_contradiction"] for f in A0)
    RES["MUTATE_M1"] = dict(bites=bool(m1)); P(f"MUTATE M1: reversed planted speeds remove both S1 contradictions -> bites: {m1}")

# S2: LP, increasing F, no CMB row
from scipy.optimize import linprog
edges = np.arange(0.0, 6000.0 + 25.0, 25.0); nb = len(edges)            # F_i on [edges_i, edges_i+1), last bin open
def hist(v): i = np.minimum(np.searchsorted(edges, v, side="right") - 1, nb - 1); return np.bincount(i, minlength=nb) / len(v)
HP = {k: hist(v) for k, v in SPD.items()}
S2 = {}
for f in A0:
    Aub, bub = [], []
    for k in ("SPARC", "XCOP", "groups", "dSph", "UDG"):
        lo, hi = NEED[f][k]
        if hi is not None: Aub.append(HP[k]); bub.append(hi)
        if lo is not None: Aub.append(-HP[k]); bub.append(-lo)
    for i in range(nb - 1):
        r_ = np.zeros(nb); r_[i] = 1; r_[i + 1] = -1; Aub.append(r_); bub.append(0.0)
    lp = linprog(np.zeros(nb), A_ub=np.array(Aub), b_ub=np.array(bub), bounds=[(0, None)] * nb, method="highs")
    feas = lp.status == 0
    S2[f] = dict(feasible=bool(feas), lp_status=int(lp.status), message=str(lp.message), status="FAIL (infeasible)" if not feas else "NO VERDICT (feasible, tail-dependent)")
    if feas:
        Fv = lp.x; S2[f]["F_nonzero_from_kms"] = float(edges[np.argmax(Fv > 1e-9)]); S2[f]["F_max"] = float(Fv.max())
        S2[f]["class_means"] = {k: float(HP[k] @ Fv) for k in HP}
    P(f"[{f}] S2 LP (increasing F, no CMB row, bins 25 km/s to 6000): {S2[f]['status']}" +
      (f"; F > 0 from {S2[f]['F_nonzero_from_kms']:.0f} km/s, F_max {S2[f]['F_max']:.3g}; means {json.dumps({k: round(v, 3) for k, v in S2[f]['class_means'].items()})}" if feas else f" ({lp.message})"))
RES["I5"]["S2"] = S2
RES["I5"]["speeds"] = {k: dict(median=float(np.median(v)), p5=float(np.percentile(v, 5)), p95=float(np.percentile(v, 95))) for k, v in SPD.items()}
del SPD, CDF, HP

# I5 label per footing
if not MUT:
    for f in A0:
        rowsA = dict(S1=S1[f]["status"], W1_readingA=("PASS" if W1[f]["KA1 F=1"]["W1_pass"] else "FAIL") + f" (r {W1[f]['KA1 F=1']['r']:.3f}, plain law)", S2=S2[f]["status"])
        wB = [W1[f]["inc step"], W1[f]["dec step"]]
        rowsB = dict(W1_inc=f"{'PASS' if wB[0]['W1_pass'] else 'FAIL'} (r {wB[0]['r']:.3f})", W1_dec=f"{'PASS' if wB[1]['W1_pass'] else 'FAIL'} (r {wB[1]['r']:.3f})")
        deadA = S1[f]["status"].startswith("FAIL") and not W1[f]["KA1 F=1"]["W1_pass"]
        deadB = not wB[0]["W1_pass"] and not wB[1]["W1_pass"]
        lab = "DEAD BY REDUCTION" if (R_pass and deadA and deadB) else ("FAILS (rows)" if (deadA and deadB) else "NO VERDICT / open")
        RES["I5"].setdefault("label", {})[f] = dict(label=lab, readingA=rowsA, readingB=rowsB, GW_P2="FAIL", GW_P1="PASS (CONDITIONAL)")
        P(f"[{f}] I5 LABEL: {lab}; reading A {rowsA}; reading B {rowsB}; P2 GW FAIL")

# ================================================================== I7 defect network
P("\n== I7: defect network of the a0 scalar (eta from a0) ==")
hbar = 1.054571817e-34; kB = 1.380649e-23; T0 = 2.7255; eV = 1.602176634e-19
EPl = math.sqrt(hbar * CC ** 5 / Gn)
a_, t_, w_, wt_, C_ = sp.symbols("a t w w_tot C", positive=True)
ka6a = sp.simplify(a_ ** (-3 * (1 + sp.Rational(-1, 3))) - a_ ** -2) == 0 and sp.simplify(a_ ** (-3 * (1 + sp.Rational(-2, 3))) - a_ ** -1) == 0
# scaling: rho_def = C H^2 with H^2 ~ a^{-3(1+w_tot)} (constant w_tot over a step): w_def = -1 - (1/3) dln rho/dln a = w_tot
Hsq = a_ ** (-3 * (1 + wt_)); rdef = C_ * Hsq
wdef = sp.simplify(-1 - sp.Rational(1, 3) * sp.diff(sp.log(rdef), a_) * a_)
ka6b = sp.simplify(wdef - wt_) == 0
def wtot(z, e=1e-3):
    return -1 + (2.0 / 3.0) * (math.log(MC.Hubble(z * (1 + e) + e)) - math.log(MC.Hubble(z / (1 + e) - e / (1 + e)))) / (math.log(1 + z * (1 + e) + e) - math.log(1 + z / (1 + e) - e / (1 + e)))
OMR = 2.4728e-5 * (1 + 0.22711 * 3.046); ZEQ1 = (ob + od) / OMR     # A1-1: two-fluid known answer
def w2f(z): return (1.0 / 3.0) / (1 + ZEQ1 / (1 + z))
try:
    w1e5 = wtot(1e5); w50 = wtot(50.0)
except Exception as ex:
    w1e5 = w50 = float("nan"); P(f"KA7 solver call failed: {ex}")
w3400 = wtot(3400.0)
ka7d = {str(z): dict(solver=w_, two_fluid=w2f(z), diff=abs(w_ - w2f(z))) for z, w_ in ((1e5, w1e5), (3400.0, w3400), (50.0, w50))}
ka7 = all(v["diff"] <= 0.003 for v in ka7d.values())
P(f"KA6: frozen w -1/3, -2/3 -> a^-2, a^-1: {ka6a}; scaling rho ~ H^2 -> w_def = {wdef} = w_tot: {ka6b}")
P(f"KA7 (A1-1): 1 + z_eq {ZEQ1:.1f}; solver vs two-fluid w: " + "; ".join(f"z {k}: {v['solver']:.4f} vs {v['two_fluid']:.4f} (|d| {v['diff']:.4f})" for k, v in ka7d.items()) + f" -> {ka7} (line 0.003)")
RES["KA"]["KA6"] = dict(frozen=bool(ka6a), scaling=bool(ka6b), ok=bool(ka6a and ka6b)); RES["KA"]["KA7"] = dict(rows=ka7d, one_plus_zeq=ZEQ1, ok=bool(ka7))
H0s = SV.H0s; rhoc0 = 3 * H0s ** 2 / (8 * math.pi * Gn)
H3400 = Hs(3400.0); rho_tot3400 = 3 * H3400 ** 2 / (8 * math.pi * Gn); rho_b3400 = ob / h ** 2 * rhoc0 * 3401.0 ** 3
tot_over_b = rho_tot3400 / rho_b3400
Om0 = (ob + od) / h ** 2
P(f"solver: rho_tot / rho_b at z 3400 = {tot_over_b:.3f}; od/ob = {od/ob:.3f} (CMB need reported); Omega_m0 {Om0:.4f}")
I7 = {}
for f, a0 in A0.items():
    rhoDE = (a0 / (KAPPA * CC)) ** 2 / Gn; eta4 = rhoDE * CC ** 2 * (hbar * CC) ** 3; etaJ = eta4 ** 0.25
    a0back = KAPPA * CC * math.sqrt(Gn * (etaJ ** 4 / (CC ** 2 * (hbar * CC) ** 3))); ka5 = abs(a0back / a0 - 1) <= 1e-12
    zform = etaJ / (kB * T0) - 1
    Gmu_a0 = math.pi * (etaJ / EPl) ** 2; sigma_a0 = etaJ ** 3 / (hbar * CC) ** 2
    Omw_a0 = 8 * math.pi * Gn * sigma_a0 / (3 * CC ** 3 * H0s)
    zeta = 10.0; Gmu_cap = 1.5e-7
    str_tot = 6 * math.pi * zeta * Gmu_cap; str_b = str_tot * tot_over_b; str_b_a0 = 6 * math.pi * zeta * Gmu_a0 * tot_over_b
    Omw_cap = (4.0 / 3.0) * 1e-5
    wall_b_3400 = Omw_cap / (ob / h ** 2) * (H3400 / H0s) / 3401.0 ** 3          # rho_wall ~ sigma H / c ~ H; rho_b ~ (1+z)^3
    Om_str0 = str_tot * Om0
    fcl_str = Om_str0 / 1e3; fcl_wall = Omw_cap / 1e3
    rows = {
        "D0 existence z 3400": dict(z_form=zform, eta_eV=etaJ / eV, status="FAIL" if zform < 3400 else "PASS"),
        "D1 w at z 3400 (|w|<=0.01)": dict(strings_frozen=-1 / 3, walls_frozen=-2 / 3, scaling_strings_globalmono_textures=w3400, gauge_monopoles=0.0,
                                           status="FAIL (strings, walls, global monopoles, textures); gauge monopoles w = 0 -> D4"),
        "D2 amplitude z 3400 (need rho_def/rho_b >= 1; od/ob %.2f)" % (od / ob): dict(strings_at_CMB_cap=str_b, strings_at_a0=str_b_a0, walls_at_isotropy_cap=wall_b_3400,
                                           walls_Omega0_at_a0=Omw_a0, Gmu_at_a0=Gmu_a0, status="FAIL"),
        "D3 cluster (need %.1f)" % FCL_NEED[f]: dict(strings=fcl_str, walls=fcl_wall, status="FAIL"),
        "D4 no-particle": dict(gauge_monopoles="particle-like: DEAD by rule", status="FAIL (gauge monopoles)"),
        "D5 isotropy walls": dict(Omega_wall_cap=Omw_cap, note="delta T / T = (3/4) Omega_wall <= 1e-5"),
    }
    for k in list(rows)[:4]:
        if k.startswith("D2") and max(str_b, str_b_a0, wall_b_3400) >= 1: rows[k]["status"] = "PASS"
        if k.startswith("D3") and max(fcl_str, fcl_wall) >= FCL_NEED[f]: rows[k]["status"] = "PASS"
    dead = all(r["status"].startswith("FAIL") for k, r in rows.items() if k[:2] in ("D0", "D1", "D2", "D3", "D4"))
    I7[f] = dict(rows=rows, KA5=dict(a0_roundtrip_rel=abs(a0back / a0 - 1), ok=bool(ka5)), label="DEAD" if dead else "NOT DEAD")
    P(f"[{f}] KA5 eta round trip rel {abs(a0back/a0-1):.1e} -> {ka5}; eta {etaJ/eV:.4e} eV; rho_DE {rhoDE:.4e} kg/m^3")
    P(f"[{f}] D0: 1 + z_form = eta / kT0 -> z_form {zform:.2f} vs 3400: {rows['D0 existence z 3400']['status']}")
    P(f"[{f}] D1: frozen strings -1/3, walls -2/3; scaling (strings / global monopoles / textures) w = w_tot(3400) {w3400:.4f}; line |w| <= 0.01: FAIL; gauge monopoles w 0 -> D4")
    P(f"[{f}] D2: strings rho/rho_b at z 3400 <= {str_b:.2e} (CMB cap G mu 1.5e-7, zeta 10); at a0's eta G mu {Gmu_a0:.2e} -> {str_b_a0:.2e}; walls (isotropy cap Omega_w <= {Omw_cap:.2e}) {wall_b_3400:.2e}; Omega_wall at a0's eta {Omw_a0:.2e}; need >= 1 -> FAIL")
    P(f"[{f}] D3: cluster f strings <= {fcl_str:.2e}, walls <= {fcl_wall:.2e} vs need {FCL_NEED[f]}: FAIL; D4 gauge monopoles: particle -> DEAD by rule")
    P(f"[{f}] I7 LABEL: {I7[f]['label']}")
RES["I7"] = I7
if MUT:   # M4: planted non-relativistic network, rho_def/rho_b = od/ob, captured like dust
    m4 = {}
    for f in A0:
        amt = od / ob; d1 = abs(0.0) <= 0.01; d2 = amt >= 1.0; d3 = amt >= FCL_NEED[f]
        m4[f] = dict(D1=d1, D2=d2, D3=d3, amount=amt, label="DEAD by D4 only (particle-like)" if (d1 and d2 and d3) else "rows fail")
        P(f"MUTATE M4 [{f}]: planted w 0, rho_def/rho_b {amt:.3f}: D1 {d1} D2 {d2} D3 {d3} -> {m4[f]['label']}")
    RES["MUTATE_M4"] = dict(foot=m4, bites=bool(all(v["D1"] and v["D2"] and v["D3"] for v in m4.values())))
    RES["MUTATE_all_bite"] = bool(all(RES[k]["bites"] for k in ("MUTATE_M1", "MUTATE_M2", "MUTATE_M3", "MUTATE_M4")))
    P(f"MUTATE: M1 {RES['MUTATE_M1']['bites']} M2 {RES['MUTATE_M2']['bites']} M3 {RES['MUTATE_M3']['bites']} M4 {RES['MUTATE_M4']['bites']} -> all bite {RES['MUTATE_all_bite']}")
else:
    RES["KA_all_I7"] = bool(RES["KA"]["KA6"]["ok"] and RES["KA"]["KA7"]["ok"] and all(I7[f]["KA5"]["ok"] for f in A0))
    lab5 = {f: RES["I5"]["label"][f]["label"] for f in A0}; lab7 = {f: I7[f]["label"] for f in A0}
    RES["label_line"] = f"I5 {lab5['canonical']} / {lab5['alt']}; I7 {lab7['canonical']} / {lab7['alt']} (canonical / alt)"
    P(f"\nLABEL LINE: {RES['label_line']}; KA I5 {RES['KA_all_I5']} I7 {RES['KA_all_I7']}")
RES["peak_rss_GB"] = rss(); P(f"peak RSS {rss():.3f} GB (ru_maxrss)")
P("kappa = 1/2 FITTED; not theory closed.")
dump()
