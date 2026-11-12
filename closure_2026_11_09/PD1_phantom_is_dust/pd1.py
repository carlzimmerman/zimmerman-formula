#!/usr/bin/env python3
"""PD1 (FROZEN_CRITERIA.md 0dc7929421): variant N, the law's phantom IS the conserved dust. P1 population conservation and per-halo
share, P2 KiDS (pointwise, truncated phantom + leftover) and SPARC (QX8 fit), P3 groups and X-COP (phantom on baryons + Newtonian
leftover), P5 Bullet (DB1 child via WM1's wm1_local.py bchild), KA-P1..P4, MUTATE MP1 (share x 10), MP2 (truncation off), brackets
S-AM and S-src. WL1's shell solver, phantom formula and GSMF: own transcription (verified by KA-P1/P2).
    python3 pd1.py   -> pd1.json / pd1.out, pd1_MUTATE.json / pd1_MUTATE.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib, time, subprocess
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); SS1D = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"); sys.path.insert(0, SS1D)
WM1 = os.path.join(REPO, "closure_2026_11_09", "WM1_warm_component_law_baryons")
CRIT = "0dc7929421"; T0 = time.time()
_a = sys.argv; sys.argv = [_a[0]]
import ss1_core as C
sys.argv = _a
L = []
def P(s): print(s, flush=True); L.append(str(s))
G, MS, PC = 6.6743e-11, 1.98892e30, 3.0857e16; MPC = 1e6 * PC; KPC = 1e3 * PC; G_KPC = 4.3009172706e-6
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; FOOTS = ("canonical", "alt")
def glaw(g, a0): g = np.asarray(g, float); return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))
def Mph(r, Mb, a0):
    if r <= 0: return 0.0
    y = G * Mb / r ** 2 / a0; return Mb * (math.sqrt(0.25 + 1.0 / y) - 0.5)
# ---------------- background + WL1's shell solver (own transcription)
class BG:
    def __init__(s, OB, OD, h, OR_h2=4.15e-5):
        s.OB, s.OD, s.h = OB, OD, h; s.R = OD / OB; s.Om = (OB + OD) / h ** 2; s.Orr = OR_h2 / h ** 2; s.OL = 1 - s.Om - s.Orr
        s.H0s = 100 * h * 1e3 / MPC; s.RHOC = 3 * s.H0s ** 2 / (8 * math.pi * G); s.RHO_M0 = s.Om * s.RHOC; s.RHO_D0 = OD / h ** 2 * s.RHOC
    def Hs(s, a): return s.H0s * math.sqrt(s.Orr / a ** 4 + s.Om / a ** 3 + s.OL)
    def shell(s, xL, dM, a0, a_end=1.0):
        AI = 1 / 1001.0
        def rhs(t, y):
            a, r, v = y; acc = -(4 * math.pi * G / 3) * (s.RHO_M0 / a ** 3 + 2 * s.Orr * s.RHOC / a ** 4 - 2 * s.OL * s.RHOC) * r; gN = G * dM / r ** 2
            acc -= (float(glaw(gN, a0)) if a0 > 0 else gN); return [a * s.Hs(a), v, acc]
        def turn(t, y): return y[2]
        turn.terminal, turn.direction = True, -1
        def end(t, y): return y[0] - a_end
        end.terminal = True
        r0 = xL * AI; so = solve_ivp(rhs, (0, 3e18), [AI, r0, s.Hs(AI) * r0], events=(turn, end), rtol=1e-9, atol=[1e-12, r0 * 1e-12, 1e-6], method="DOP853")
        if so.t_events[0].size: return "early", so.y_events[0][0]
        return "late", so.y_events[1][0] if so.t_events[1].size else so.y[:, -1]
    def r_ta(s, dM, a0, a_end=1.0):
        lo, hi = math.log(1e-6 * MPC), math.log(1e3 * MPC)
        for _ in range(60):
            mid = 0.5 * (lo + hi); kind, st = s.shell(math.exp(mid), dM, a0, a_end)
            if kind == "early": lo = mid
            else: hi = mid
            if hi - lo < 1e-7: break
        kind, st = s.shell(math.exp(hi), dM, a0, a_end); return float(st[1]), math.exp(hi)
# ---------------- GSMF (Driver 2022, WL1's inputs)
DRV = json.load(open(os.path.join(REPO, "closure_program_2026_10_27", "population", "inputs.json")))["driver2022"]
def gsmf(h):
    h70 = h / 0.7; MST = 10 ** DRV["log10_Mstar_h70_minus2"] / h70 ** 2
    PHI = np.array([10 ** DRV[k] for k in ("log10_phi1_h70_cubed", "log10_phi2_h70_cubed")]) * 10 ** DRV["add_log10_phi_for_SDSS_and_z0"] * h70 ** 3; ALP = np.array([DRV["alpha1"], DRV["alpha2"]])
    return lambda lm: float(math.log(10) * np.sum(PHI * (10 ** lm / MST) ** (ALP + 1)) * math.exp(-10 ** lm / MST))
LG = np.arange(9.0, 12.001, 0.25); LF = np.arange(9.0, 12.0001, 0.02)
def q_pop(B, a0, z, mode):
    aE = 1 / (1 + z); per = gsmf(B.h); RHO_D_SUN = B.RHO_D0 * MPC ** 3 / MS
    tab = np.array([(B.r_ta(10 ** m * MS, a0, aE)[0] if mode == "L" else B.r_ta(10 ** m * MS * (1 + B.R), 0.0, aE)[0]) for m in LG])
    Rm = 10 ** np.interp(LF, LG, np.log10(tab)); mph = np.array([Mph(R, 10 ** m * MS, a0) / MS for R, m in zip(Rm, LF)])
    return float(np.trapz(np.array([per(m) for m in LF]) * mph, LF)) / RHO_D_SUN, tab
# ---------------- data (as TS1 / SS1)
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}; a = sys.argv; sys.argv = [path]
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns
sys.path.insert(0, os.path.join(CL6, "QX8_sparc_exact_field")); a_ = sys.argv; sys.argv = [a_[0]]
with contextlib.redirect_stdout(io.StringIO()):
    import qx8 as Q8
sys.argv = a_
GALS = Q8.load_sparc(); GB = load_prefix(os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
XC, GR = GB["XC"], GB["GR"]; LE = GB["NS"]["lensing"]()
from astropy.io import fits
R500X = {}
for name in sorted({z["name"] for z in XC}):
    with fits.open(os.path.join(GB["DATA"], "xcop", name, f"{name}_fgas_profile.fits")) as h_: R500X[name] = float(h_[1].header["R500"])
lU, lN = np.log(Q8.UPS), np.log(Q8.NODES)
PRE = {f: [np.array([np.interp(lU, lN, T[:, j]) for j in range(T.shape[1])]) for T in (np.load(os.path.join(Q8.PARTS, f, f"{i:03d}.npz"), allow_pickle=False)["T"] for i in range(len(GALS)))] for f in FOOTS}
TR1 = [0.71, 0.66, 0.58, 0.46, 0.32]
Q15 = json.load(open(os.path.join(CL6, "QX15_cmb_primary_likelihood", "qx15.json")))
def footing_bg(f): th = Q15["footings"][f]["main"]["theta"]; return BG(th["omega_b"], th["omega_d"], float(Q15["footings"][f]["main"]["h"]))
# ---------------- the share table
LM = np.arange(7.0, 15.001, 0.25)
def share_table(B, a0, z, share_mult=1.0, rule="ta"):
    aE = 1 / (1 + z); rows = []
    for m in LM:
        Mb = 10 ** m * MS; rms, xL = B.r_ta(Mb * (1 + B.R), 0.0, aE)
        sh = B.RHO_D0 * 4 * math.pi / 3 * xL ** 3 + B.R * Mb; am_ok = None
        if rule == "AM":
            try: sh = (B.OD / (B.OB + B.OD)) * C.moster_halo(10 ** m, z) * MS; am_ok = True
            except ValueError: am_ok = False                                            # outside Moster 2013's range: the ta share is kept (disclosed)
        sh *= share_mult; mp = Mph(rms, Mb, a0)
        rt = brentq(lambda r: Mph(r, Mb, a0) - sh, 1e-6 * KPC, rms) if mp > sh else rms; left = max(0.0, sh - mp)
        rows.append(dict(AM_in_range=am_ok, logMb=float(m), R_ms_Mpc=rms / MPC, x_ta_Mpc=xL / MPC, share_over_Mb=sh / Mb, Mph_Rms_over_share=mp / sh, R_trunc_kpc=rt / KPC, leftover_over_Mb=left / Mb))
    return rows
def interp(tab, key, m): return float(10 ** np.interp(m, [r["logMb"] for r in tab], np.log10(np.maximum([r[key] for r in tab], 1e-300))))
def halo_of(tab, Mb_sun, trunc=True):
    """R_trunc (m), R_ms (m), leftover (kg) at M_b by log-interpolation of the share table; leftover only where both bracketing nodes have one."""
    m = math.log10(Mb_sun); rms = interp(tab, "R_ms_Mpc", m) * MPC
    if not trunc: return math.inf, rms, 0.0
    rt = interp(tab, "R_trunc_kpc", m) * KPC; lm = np.array([r["logMb"] for r in tab]); lv = np.array([r["leftover_over_Mb"] for r in tab])
    j = int(np.clip(np.searchsorted(lm, m), 1, len(lm) - 1)); left = (interp(tab, "leftover_over_Mb", m) * Mb_sun * MS) if (lv[j - 1] > 0 and lv[j] > 0) else 0.0
    return rt, rms, left
def m_left(r, left, rms): return left * min(r, rms) / rms if left > 0 else 0.0
# ---------------- gates
def kids(a0, tab, trunc=True):
    sh = []
    for p in LE:
        Mb = p["Mb"]; R = math.sqrt(G * Mb / p["gbar"]); rt, rms, left = halo_of(tab, Mb / MS, trunc)
        M = Mb + Mph(min(R, rt), Mb, a0) + m_left(R, left, rms); sh.append(math.log10(G * M / R ** 2 / float(glaw(p["gbar"], a0))))
    sh = np.array(sh); return dict(status="PASS" if np.all(np.abs(sh) <= 0.05) else "FAIL", max_abs=float(np.max(np.abs(sh))), n_over=int(np.sum(np.abs(sh) > 0.05)), mean=float(sh.mean()), min=float(sh.min()))
def sparc(f, a0, tab, trunc=True):
    rows = []
    for q, Tf in zip(GALS, PRE[f]):
        R = q["R"]; Rm = q["Rm"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        Mbs = max(float(np.max(np.clip(VB2 * R / G_KPC, 0, None))), 1e3); rt, rms, left = halo_of(tab, Mbs, trunc); g = q["GB"]
        gt = G * Mbs * MS / rt ** 2 if math.isfinite(rt) else 0.0; ph_t = (float(glaw(gt, a0)) - gt) if math.isfinite(rt) else 0.0
        inside = (Rm < rt)[:, None]; gout = g + ph_t * (rt / Rm[:, None]) ** 2 if math.isfinite(rt) else g
        ge = np.where(inside, glaw(g, a0), gout) + (np.array([G * m_left(r_, left, rms) / r_ ** 2 for r_ in Rm])[:, None] if left > 0 else 0.0)
        lgp = np.log10(np.maximum(ge, 1e-300)) + Tf; OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k], rt / KPC, float(Rm[-1] / KPC)))
    def pooled(idx):
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
    massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]
    return dict(all=pooled(range(len(rows))), massive=pooled(massive), frac_truncated_inside_Rlast=float(np.mean([r[3] < r[4] for r in rows])), median_Rtrunc_kpc=float(np.median([r[3] for r in rows])))
def cl_points(a0, tab, pts, Msys, Mb_of, trunc=True):
    rt, rms, left = halo_of(tab, Msys, trunc); out = []
    for z in pts:
        r = z["r_kpc"] * KPC; Mb = Mb_of(z); gN = G * Mb * MS / r ** 2
        g = float(glaw(gN, a0)) if r < rt else gN + (float(glaw(G * Msys * MS / rt ** 2, a0)) - G * Msys * MS / rt ** 2) * (rt / r) ** 2
        ml = m_left(r, left, rms); g += G * ml / r ** 2; out.append((g * r ** 2 / G / MS, ml / MS, (g - gN) * r ** 2 / G / MS - ml / MS))
    return out
def xcop(a0, tab, trunc=True):
    d = []; xr = []; fl = []; fp = []
    for name in R500X:
        pts = [z for z in XC if z["name"] == name]; Msys = pts[0]["Mb_last"][0]
        for z, (Mp, ml, mph) in zip(pts, cl_points(a0, tab, pts, Msys, lambda z: z["M_b"], trunc)):
            d.append(math.log10(z["M_obs"] / Mp)); xr.append(z["r_kpc"] / R500X[name]); fl.append(ml / z["M_obs"]); fp.append((ml + mph) / z["M_obs"])
    d, xr, fl, fp = map(np.array, (d, xr, fl, fp)); EDG = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]; bins = []
    for b_, (lo, hi) in enumerate(zip(EDG[:-1], EDG[1:])):
        m = (xr >= lo) & (xr < hi)
        bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None, graded=bool(m.sum() >= 3), within=bool(abs(d[m].mean()) <= 0.10) if m.sum() >= 3 else None,
                         leftover_over_Mdyn=float(np.median(fl[m])) if m.sum() else None, dark_over_Mdyn=float(np.median(fp[m])) if m.sum() else None, TR1=TR1[b_]))
    amp = abs(d.mean()) <= 0.05 and math.sqrt((d ** 2).mean()) <= 0.10; shp = all(b["within"] for b in bins if b["graded"])
    return dict(status="PASS" if (amp and shp) else "FAIL", mean=float(d.mean()), rms=float(math.sqrt((d ** 2).mean())), bins=bins)
def groups(a0, tab, trunc=True):
    o = {}
    for fst in (0, 1):
        npass = 0; med = []
        for gp in GR:
            ok = True
            for p, (Mp, ml, mph) in zip(gp["pts"], cl_points(a0, tab, gp["pts"], gp["g5"] * (1 + fst), lambda p: p["M_gas"] * (1 + fst), trunc)):
                dl = math.log10(p["M_obs"] / Mp); med.append(dl); ok &= abs(dl) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
            npass += ok
        o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)))
    return dict(status="PASS" if all(v["n_pass"] >= 16 for v in o.values()) else "FAIL", **o)
def bullet(tabs):
    def call(arg, on):
        cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.join(WM1, "wm1_local.py"), "bchild", "W", arg, on], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
        line = [l for l in cp.stdout.splitlines() if l.startswith("WM1CHILD ")]
        if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
        return json.loads(line[0][9:])
    o0 = call("{}", "gal"); m = o0["masses"]; Mb = [m["M_gas_sub"][j] + m["M_star_sub"][j] for j in range(2)]; Ml = {}; info = {}
    for f in FOOTS:
        B = footing_bg(f); r_ = []; inf = []
        for j in range(2):
            rt, rms, left = halo_of(tabs[f]["z0.3"], Mb[j]); Hh = C.halo(Mb[j], B.R, B.h, B.Om, z=0.3); ml = m_left(Hh["R200"] * KPC, left, rms) / MS
            r_.append(ml); inf.append(dict(M_b=Mb[j], leftover_inside_R200_over_Mb=ml / Mb[j], R_ms_Mpc=rms / MPC))
        Ml[f] = r_; info[f] = inf
    oa = call(json.dumps(Ml), "gal")
    out = dict(KA_law_only_row=o0["KA"], subclusters=info)
    for f in FOOTS:
        b = oa[f]["row"]; out[f] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", row=b)
        P(f"[{f}] P5 Bullet (phantom on the baryons = DB1 law row; leftover galaxy-traced): {b['label']}; M300 Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; leftover in R200 / M_b " + ", ".join(f"{x['leftover_inside_R200_over_Mb']:.2f}" for x in info[f]) + f"; law-only KA row {o0['KA']['label']} (Z {o0['KA']['ZM'][0]:+.2f}, {o0['KA']['ZM'][1]:+.2f})")
    return out
# ---------------- run
RES = dict(criteria=CRIT, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed"); MUT = {}
# KA-P1 / KA-P2 on WL1's background
BW = BG(0.0215, 0.11958060485606123, 0.65); ka = {}
for f, ref in (("canonical", 0.936), ("alt", 1.079)):
    q, tab = q_pop(BW, A0[f], 1.0, "L"); ka[f] = dict(q_pop=q, ref=ref, pass_=bool(abs(q / ref - 1) <= 0.01))
    tc = np.array([max(BW.r_ta(10 ** m * MS * (1 + BW.R), A0[f])[0], (10 ** m * MS * (1 + BW.R) / (4 * math.pi / 3 * 5.55 * BW.RHO_M0)) ** (1 / 3)) for m in LG])
    sh_ = []
    for p in LE:
        Mb = p["Mb"]; R = math.sqrt(G * Mb / p["gbar"]); Rc = 10 ** np.interp(math.log10(Mb / MS), LG, np.log10(tc))
        def gproj(Rcut, NU=40000):
            Rc_ = min(Rcut, 1e5 * MPC); M3 = Mb + Mph(min(R, Rc_), Mb, A0[f])
            if R >= Rc_: return 4 * G * M3 / (math.pi * R ** 2)
            um = math.acosh(Rc_ / R); u = np.linspace(0.0, um, NU); r = R * np.cosh(u); yy = G * Mb / r ** 2 / A0[f]; dm = Mb / (yy * r * np.sqrt(0.25 + 1.0 / yy))
            Sig = np.trapz(dm / (2 * math.pi * r), u); Mc = M3 + np.trapz(dm * (1 - np.tanh(u)) * R * np.sinh(u), u); return 4 * G * (Mc / (math.pi * R ** 2) - Sig)
        sh_.append(math.log10(gproj(Rc) / gproj(math.inf)))
    kref = {"canonical": 0.0011, "alt": 0.0009}[f]; ka[f].update(kids_ceiling_mean=float(np.mean(sh_)), kids_ref=kref, kids_pass=bool(abs(np.mean(sh_) - kref) <= 0.0005))
    P(f"[{f}] KA-P1 q_pop z1 (WL1 background, law-on R_ms) {q:.4f} vs {ref} -> {'PASS' if ka[f]['pass_'] else 'FAIL'}; KA-P2 KiDS ceiling mean {np.mean(sh_):+.4f} vs {kref:+.4f} -> {'PASS' if ka[f]['kids_pass'] else 'FAIL'}  [{time.time()-T0:.0f}s]")
RES["KA_P1_P2"] = ka
y = 1e-6; M_ = 1e11 * MS; r_ = math.sqrt(G * M_ / (y * A0["canonical"])); RES["KA_P4"] = dict(ratio=Mph(r_, M_, A0["canonical"]) / (r_ * math.sqrt(M_ * A0["canonical"] / G)))
RES["KA_P4"]["pass_"] = bool(abs(RES["KA_P4"]["ratio"] - 1) <= 1e-3); P(f"KA-P4 deep phantom closed form ratio {RES['KA_P4']['ratio']:.6f}")
tabs = {}
for f in FOOTS:
    B = footing_bg(f); a0 = A0[f]; r = {}
    for z in (0.5, 1.0, 2.0):
        q, tb = q_pop(B, a0, z, "N"); r[f"z {z}"] = dict(q_N=q, pass_=bool(q <= 1.0)); P(f"[{f}] P1 q_N z {z}: {q:.3f} (line <= 1) -> {'PASS' if q <= 1 else 'FAIL'}")
    RES.setdefault(f, {})["P1"] = dict(rows=r, status="PASS" if all(v["pass_"] for v in r.values()) else "FAIL")
    tabs[f] = {f"z{z}": share_table(B, a0, z) for z in (0.0, 0.3, 1.0)}
    for z in ("z0.0", "z1.0"):
        P(f"[{f}] per halo {z}: " + "; ".join(f"{t['logMb']:.0f}: share {t['share_over_Mb']:.1f} M_b, M_ph(R_ms)/share {t['Mph_Rms_over_share']:.2f}, R_ms {t['R_ms_Mpc']:.2f} Mpc, R_trunc {t['R_trunc_kpc']:.0f} kpc" for t in tabs[f][z] if t["logMb"] in (8.0, 9.0, 10.0, 10.5, 11.0, 12.0, 13.0, 14.0)))
    RES[f]["share_tables"] = tabs[f]
    T = tabs[f]["z0.0"]
    base = sparc(f, a0, T, trunc=False); k = kids(a0, T); s = sparc(f, a0, T); g2 = groups(a0, T); x3 = xcop(a0, T)
    s["status"] = "PASS" if (s["all"]["rms"] <= base["all"]["rms"] + 0.010 and abs(s["all"]["mean"]) <= 0.05 and s["massive"]["rms"] <= base["massive"]["rms"] + 0.010 and abs(s["massive"]["mean"]) <= 0.05) else "FAIL"
    RES[f].update(P2_KiDS=k, P2_SPARC=dict(s, L0=base), P3_groups=g2, P3_XCOP=x3)
    P(f"[{f}] P2 KiDS {k['status']}: max {k['max_abs']:.3f} ({k['n_over']}/59 over), min {k['min']:+.3f}, mean {k['mean']:+.3f}")
    P(f"[{f}] P2 SPARC {s['status']}: rms {s['all']['rms']:.4f} (line {base['all']['rms']+0.010:.4f}) mean {s['all']['mean']:+.3f}; massive {s['massive']['rms']:.4f}; truncated inside R_last in {100*s['frac_truncated_inside_Rlast']:.0f} % of galaxies (median R_trunc {s['median_Rtrunc_kpc']:.1f} kpc)")
    P(f"[{f}] P3 groups {g2['status']} {g2['fst0']['n_pass']}/{g2['fst1']['n_pass']} med {g2['fst0']['median_res']:+.2f}/{g2['fst1']['median_res']:+.2f}; X-COP {x3['status']} {x3['mean']:+.3f}/{x3['rms']:.3f} bins " + " ".join(f"{b['mean']:+.2f} (leftover {b['leftover_over_Mdyn']:.2f}, dark {b['dark_over_Mdyn']:.2f})" for b in x3['bins'] if b['graded']))
    # KA-P3 / MP2 (truncation off, no leftover), MP1 (share x 10), S-AM bracket
    k0 = kids(a0, T, False); x0 = xcop(a0, T, False); g0 = groups(a0, T, False); ref = {"canonical": 0.4675, "alt": 0.4345}[f]
    RES[f]["KA_P3"] = dict(kids_max=k0["max_abs"], xcop=x0["mean"], groups=[g0["fst0"]["n_pass"], g0["fst1"]["n_pass"]], pass_=bool(k0["max_abs"] < 1e-9 and abs(x0["mean"] - ref) < 1e-3 and g0["fst0"]["n_pass"] == 0))
    T10 = share_table(B, a0, 0.0, share_mult=10.0); k10 = kids(a0, T10); s10 = sparc(f, a0, T10)
    TAM = share_table(B, a0, 0.0, rule="AM"); kAM = kids(a0, TAM); sAM = sparc(f, a0, TAM)
    MUT[f] = dict(MP1_share_x10=dict(kids=k10, sparc=s10), MP2_trunc_off=RES[f]["KA_P3"], S_AM=dict(kids=kAM, sparc=sAM, table=TAM))
    P(f"[{f}] KA-P3 / MP2 truncation off: KiDS {k0['max_abs']:.1e}, X-COP {x0['mean']:+.4f} (law-only {ref:+.4f}), groups {g0['fst0']['n_pass']}/{g0['fst1']['n_pass']} -> {'PASS' if RES[f]['KA_P3']['pass_'] else 'FAIL'}")
    P(f"[{f}] MP1 share x10: KiDS max {k10['max_abs']:.3f} ({k10['n_over']} over), SPARC rms {s10['all']['rms']:.4f}; S-AM bracket: KiDS max {kAM['max_abs']:.3f} ({kAM['n_over']} over), SPARC rms {sAM['all']['rms']:.4f}; S-AM M_ph(R_ms)/share at 10/11/12: "
      + ", ".join(f"{t['Mph_Rms_over_share']:.2f}" for t in TAM if t['logMb'] in (10.0, 11.0, 12.0)))
# S-src: the source's 1.35 Mpc for L*
RES["S_src"] = {f"{m:.1e}": dict(implied_share_over_Mb=Mph(1.35 * MPC, m * MS, A0["canonical"]) / (m * MS)) for m in (5e10, 8e10)}
P("S-src: the source's R_trunc 1.35 Mpc implies share / M_b " + ", ".join(f"{k}: {v['implied_share_over_Mb']:.0f}" for k, v in RES["S_src"].items()))
RES["P5_Bullet"] = bullet(tabs)
RES["seconds"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, "pd1.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "pd1.out"), "w").write("\n".join(L) + "\n")
json.dump(MUT, open(os.path.join(HERE, "pd1_MUTATE.json"), "w"), indent=1, default=float)
P(f"done {RES['seconds']:.0f} s")
