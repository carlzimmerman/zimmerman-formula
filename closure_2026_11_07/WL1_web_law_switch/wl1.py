#!/usr/bin/env python3
"""WL1 (FROZEN_CRITERIA.md, origin c371c8ce59): the law's phantom keyed on khronon multi-streaming (F = 1 inside the
shell-crossed region r <= R_ms, F = 0 outside), SV5's two-switch escape arm (i), host side graded first.
    nice -n 15 python3 wl1.py            -> wl1.json / wl1.out
    nice -n 15 python3 wl1.py --mutate   -> wl1_MUTATE.json / .out   (M-ON R_ms = inf, M-OFF R_ms = 0, M-R x100)
Read-only reuse: QX5 loaders (lensing), GB1 battery source (up to its main block), QX7 iter_4 JSON, SV5 JSONs, QX10 rule.
One thread, < 1 GB, minutes. kappa = 1/2 FITTED; not theory closed; footings never pooled."""
import os, sys, json, math, io, contextlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import signal
import numpy as np
from scipy.integrate import solve_ivp

signal.signal(signal.SIGTERM, lambda *a: sys.exit(143))      # preemptible: nothing long-lived to checkpoint
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06")
MUT = "--mutate" in sys.argv; TAG = "wl1_MUTATE" if MUT else "wl1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# ------------------------------------------------------------- GB1 battery source up to its main block (read-only)
GB = os.path.join(CL, "GB1_all_gates_battery", "gb1.py"); src = open(GB).read()
cut = src.index("# ------------------------------------------------------------------ main")
NS = {"__file__": GB, "__name__": "gb1_lib"}; argv0 = sys.argv; sys.argv = [GB]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], GB, "exec"), NS)
sys.argv = argv0
_i, _j = src.index("def short(g, r):"), src.index("for cn, mk in CANDS.items():")
exec(compile(src[_i:_j], GB, "exec"), NS)                     # GB1's own row printer, verbatim
G, MS, PC, C, A0 = NS["G"], NS["MS"], NS["PC"], NS["C"], NS["A0"]
MPC = 1e6 * PC
LE = NS["NS"]["lensing"]()                                     # QX5's 59 KiDS isolated-lens points
GB1J = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))
SV1 = json.load(open(os.path.join(CL, "SV5_growth_mechanism", "iter_1_law_on_web", "sv5_iter1.json")))
SV2 = json.load(open(os.path.join(CL, "SV5_growth_mechanism", "iter_2_charge_switched_sound_speed", "sv5_iter2.json")))
Q7 = json.load(open(os.path.join(CL, "QX7_unified_cold_switch", "iter_4_late_evaporation", "qx7_iter4.json")))
def glaw(g, a0): return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))

# ------------------------------------------------------------- background (QX3 corner as QX7 iter_4 / QX10 iter_2)
OB, OD, H0 = 0.0215, 0.11958060485606123, 65.0
R_DUST = OD / OB; OR_h2 = 4.15e-5; h = H0 / 100
Om, Orr = (OB + OD) / h ** 2, OR_h2 / h ** 2; OL = 1 - Om - Orr
H0s = H0 * 1e3 / MPC
RHOC = 3 * H0s ** 2 / (8 * math.pi * G)
RHO_M0 = Om * RHOC
def Hs(a): return H0s * math.sqrt(Orr / a ** 4 + Om / a ** 3 + OL)
ZI = 1000.0; AI = 1 / (1 + ZI)

def shell(xL, dM, a0, a_end=1.0):
    """Lagrangian comoving radius xL (m). Returns ('early', a_ta) if v < 0 before a = 1 else ('late', r(a=1))."""
    def rhs(t, s):
        a, r, v = s
        acc = -(4 * math.pi * G / 3) * (RHO_M0 / a ** 3 + 2 * Orr * RHOC / a ** 4 - 2 * OL * RHOC) * r
        gN = G * dM / r ** 2
        acc -= (glaw(gN, a0) if a0 > 0 else gN)
        return [a * Hs(a), v, acc]
    def turn(t, s): return s[2]
    turn.terminal, turn.direction = True, -1
    def end(t, s): return s[0] - a_end
    end.terminal = True
    r0 = xL * AI; s0 = [AI, r0, Hs(AI) * r0]
    so = solve_ivp(rhs, (0, 3e18), s0, events=(turn, end), rtol=1e-9, atol=[1e-12, r0 * 1e-12, 1e-6], method="DOP853")
    if so.t_events[0].size: return "early", so.y_events[0][0]
    return "late", so.y_events[1][0] if so.t_events[1].size else so.y[:, -1]

def r_ta(dM, a0, a_end=1.0):
    """physical radius (m) of the shell turning around at a = 1 (bisection on the Lagrangian radius)."""
    lo, hi = math.log(1e-6 * MPC), math.log(1e3 * MPC)
    for _ in range(60):
        mid = 0.5 * (lo + hi); kind, st = shell(math.exp(mid), dM, a0, a_end)
        if kind == "early": lo = mid
        else: hi = mid
        if hi - lo < 1e-7: break
    kind, st = shell(math.exp(hi), dM, a0, a_end)
    return float(st[1])

def r_qx10(Mb): return (Mb * (1 + R_DUST) / (4 * math.pi / 3 * 5.55 * RHO_M0)) ** (1 / 3)
def RmsC(Mb, a0): return max(r_ta(Mb * (1 + R_DUST), a0), r_qx10(Mb))
def RmsL(Mb, a0): return r_ta(Mb, a0)
# reported, not graded: self-consistent reading (outside R_ms the key turns the law off, so the collapse there is Newtonian)
def RmsNC(Mb, a0): return max(r_ta(Mb * (1 + R_DUST), 0.0), r_qx10(Mb))
def RmsNL(Mb, a0): return r_ta(Mb, 0.0)

# ------------------------------------------------------------- projected lensing g = 4 G DeltaSigma for M_b point + phantom (r <= Rcut)
def dMph(r, Mb, a0):
    y = G * Mb / r ** 2 / a0
    return Mb / (y * r * np.sqrt(0.25 + 1.0 / y))
def Mph(r, Mb, a0):
    if r <= 0: return 0.0
    y = G * Mb / r ** 2 / a0
    return Mb * (np.sqrt(0.25 + 1.0 / y) - 0.5)
def g_proj(R, Mb, a0, Rcut, NU=40000):
    Rc = min(Rcut, 1e5 * MPC)
    M3 = Mb + Mph(min(R, Rc), Mb, a0)
    if R >= Rc: return 4 * G * M3 / (math.pi * R ** 2)
    um = math.acosh(Rc / R); u = np.linspace(0.0, um, NU); r = R * np.cosh(u); dm = dMph(r, Mb, a0)
    Sig = np.trapz(dm / (2 * math.pi * r), u)
    Mc = M3 + np.trapz(dm * (1 - np.tanh(u)) * R * np.sinh(u), u)
    return 4 * G * (Mc / (math.pi * R ** 2) - Sig)
def g_point(R, Mb, a0, Rcut): return G * (Mb + Mph(min(R, Rcut), Mb, a0)) / R ** 2

def kids_shift(a0, Rfun):
    lp, lq = [], []
    for p in LE:
        Mb = p["Mb"] / MS; R = math.sqrt(G * p["Mb"] / p["gbar"]); Rc = Rfun(Mb)
        lp.append(math.log10(g_proj(R, p["Mb"], a0, Rc) / g_proj(R, p["Mb"], a0, math.inf)))
        lq.append(math.log10(g_point(R, p["Mb"], a0, Rc) / glaw(p["gbar"], a0)))
    return float(np.mean(lp)), float(np.mean(lq))

# ------------------------------------------------------------- run
RES = dict(lane="WL1", criteria="origin c371c8ce59", tag=TAG, note="kappa = 1/2 FITTED; not theory closed", foot={}, KA={})
P(f"WL1 {'MUTATE' if MUT else 'MAIN'}: law phantom on only in the multi-streamed region r <= R_ms. kappa = 1/2 FITTED; not theory closed.")
P(f"background: Om {Om:.4f} OL {OL:.4f} Or {Orr:.2e} H0 {H0}; R = omega_d/omega_b {R_DUST:.3f}; z_i {ZI:g}")

# ---- known answers
ka = {}
ka["KA_SV5"] = dict(r_can=SV1["foot"]["canonical"]["proj"]["r"], r_alt=SV1["foot"]["alt"]["proj"]["r"],
                    sig_can=SV2["foot"]["canonical"]["Sigma_star_over_rhoDE"], sig_alt=SV2["foot"]["alt"]["Sigma_star_over_rhoDE"])
ka["KA_SV5"]["ok"] = bool(round(ka["KA_SV5"]["r_can"], 1) == 74.7 and round(ka["KA_SV5"]["r_alt"], 1) == 89.4
                          and round(ka["KA_SV5"]["sig_can"], 1) == 8.0 and round(ka["KA_SV5"]["sig_alt"], 1) == 6.0)
P(f"KA-SV5 iter_1 r {ka['KA_SV5']['r_can']:.4f} / {ka['KA_SV5']['r_alt']:.4f}; iter_2 Sigma_*/rho_DE {ka['KA_SV5']['sig_can']:.4f} / {ka['KA_SV5']['sig_alt']:.4f} -> {'PASS' if ka['KA_SV5']['ok'] else 'FAIL'}")
BATT = {}
for f, a0 in A0.items():
    S, E, X = NS["build"](f, a0); GRp = {0: NS["groups_pts"](a0, 0.0), 1: NS["groups_pts"](a0, 1.0)}
    U = NS["udgs"](f, a0); D = NS["dsphs"](f, a0); K = NS["kids"](a0)
    st = NS["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=U, D=D, K=K, sigU=sigU); B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    BATT[f] = B
    cm = dict(X=np.mean([p["D"] for p in X]), E=np.mean([p["D"] for p in E]), S=np.mean([p["D"] for p in S]),
              G0=np.mean([p["D"] for g in GRp[0] for p in g["pts"]]), G1=np.mean([p["D"] for g in GRp[1] for p in g["pts"]]))
    ref = GB1J["KA"][f]["KA1"]["class_means"]; d = max(abs(cm[k] - ref[k]) for k in cm)
    base = float(np.mean([math.log10(p["gobs"] / glaw(p["gbar"], a0)) for p in LE])); dk = abs(base - Q7["baselines"][f]["L"])
    ka[f] = dict(GB1_means_maxdiff=float(d), GB1_ok=bool(d <= 1e-9), KIDS_base=base, KIDS_base_diff=dk, KIDS_ok=bool(dk <= 1e-9))
    # KA-P: deep-MOND point mass, y = 1e-4
    Mb = 1e11 * MS; R = math.sqrt(G * Mb / (1e-4 * a0)); gp = g_proj(R, Mb, a0, math.inf); gl = glaw(1e-4 * a0, a0)
    ka[f]["KA_P"] = dict(ratio=gp / gl, ok=bool(abs(gp / gl - 1) <= 0.01))
    P(f"[{f}] KA-GB1 L0 class means max|d| {d:.1e}; KA-K KiDS base {base:.6f} vs QX7 iter_4 {Q7['baselines'][f]['L']:.6f} |d| {dk:.1e}; "
      f"KA-P 4G DeltaSigma / g_law at y 1e-4 {gp/gl:.5f} -> {'PASS' if ka[f]['GB1_ok'] and ka[f]['KIDS_ok'] and ka[f]['KA_P']['ok'] else 'FAIL'}")
# KA-T: Newtonian shell code vs QX10's 5.55 rho_m0 rule at M_b 1e11
rN = r_ta(1e11 * (1 + R_DUST) * MS, 0.0); rQ = r_qx10(1e11 * MS)
ka["KA_T"] = dict(r_newton_Mpc=rN / MPC, r_qx10_Mpc=rQ / MPC, ratio=rN / rQ, within20=bool(abs(rN / rQ - 1) <= 0.2))
P(f"KA-T Newton shell r_ta(M_b 1e11 (1+R)) {rN/MPC:.4f} Mpc vs QX10 rule {rQ/MPC:.4f} Mpc: ratio {rN/rQ:.3f} -> {'within 20 %' if ka['KA_T']['within20'] else 'OUTSIDE 20 % (reported; ceiling takes the max)'}")
RES["KA"] = ka
kaok = ka["KA_SV5"]["ok"] and all(ka[f]["GB1_ok"] and ka[f]["KIDS_ok"] and ka[f]["KA_P"]["ok"] for f in A0)
RES["KA_all"] = bool(kaok)
if not kaok:
    P("KA FAIL: stop, nothing graded.")
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)

# ---- R_ms tables
LM = np.arange(0.0, 15.51, 1.0)
for f, a0 in A0.items():
    tC = np.array([RmsC(10 ** m * MS, a0) for m in LM]); tL = np.array([RmsL(10 ** m * MS, a0) for m in LM])
    RES["foot"][f] = dict(logM=LM.tolist(), RmsC_Mpc=(tC / MPC).tolist(), RmsL_Mpc=(tL / MPC).tolist())
    P(f"[{f}] R_ms ceiling / lower (Mpc) at log M_b 9.4..10.9: " + "; ".join(
        f"{lm}: {RmsC(10**lm*MS, a0)/MPC:.3f} / {RmsL(10**lm*MS, a0)/MPC:.3f}" for lm in (9.4, 10.45, 10.7, 10.9)))
    if not MUT: P(f"[{f}] REPORTED self-consistent (Newton outside R_ms) R_ms dust / no dust (Mpc): " + "; ".join(
        f"{lm}: {RmsNC(10**lm*MS, a0)/MPC:.3f} / {RmsNL(10**lm*MS, a0)/MPC:.3f}" for lm in (9.4, 10.45, 10.7, 10.9)))
def interp_R(f, which):
    lr = np.log10(np.array(RES["foot"][f][which]) * MPC)
    return lambda Mb_sun: 10 ** float(np.interp(math.log10(max(Mb_sun, 1.0)), LM, lr))

# ---- stage 1: K-G6
def stage1(f, a0, mode):
    if mode == "C": Rf = lambda M: RmsC(M * MS, a0)
    elif mode == "L": Rf = lambda M: RmsL(M * MS, a0)
    elif mode == "ON": Rf = lambda M: math.inf
    elif mode == "OFF": Rf = lambda M: 0.0
    elif mode == "C100": Rf = lambda M: 100 * RmsC(M * MS, a0)
    elif mode == "NC": Rf = lambda M: RmsNC(M * MS, a0)
    elif mode == "NL": Rf = lambda M: RmsNL(M * MS, a0)
    cache = {}
    def Rc(M):
        if M not in cache: cache[M] = Rf(M)
        return cache[M]
    sp, sq = kids_shift(a0, Rc)
    Rpts = np.array([math.sqrt(G * p["Mb"] / p["gbar"]) for p in LE]); fr = float(np.mean([Rpts[i] > Rc(p["Mb"] / MS) for i, p in enumerate(LE)]))
    return dict(shift_proj=sp, shift_point=sq, frac_points_outside=fr, R_range_Mpc=[float(Rpts.min() / MPC), float(Rpts.max() / MPC)],
                pass_=bool(abs(sp) <= 0.05), margin=float(0.05 - abs(sp)))
modes = ("ON", "OFF", "C100", "C") if MUT else ("C", "L", "NC", "NL")   # NC / NL reported only
S1 = {}
for f, a0 in A0.items():
    S1[f] = {m: stage1(f, a0, m) for m in modes}
    for m, v in S1[f].items():
        P(f"[{f}] K-G6 {m:4s}{' (REPORTED)' if m in ('NC', 'NL') else ''}: shift (4G DeltaSigma) {v['shift_proj']:+.4f} dex, pointwise {v['shift_point']:+.4f} vs base; "
          f"{100*v['frac_points_outside']:.0f} % of 59 points outside R_ms (R {v['R_range_Mpc'][0]:.3f}-{v['R_range_Mpc'][1]:.2f} Mpc); "
          f"|shift| <= 0.05 -> {'PASS' if v['pass_'] else 'FAIL'} (margin {v['margin']:+.4f})")
    RES["foot"][f]["K_G6"] = S1[f]

# ---- stage 1: GB1 rows
def cand(f, Rmode):
    a0 = A0[f]
    if Rmode == "ON": Rf = lambda M: math.inf
    elif Rmode == "OFF": Rf = lambda M: 0.0
    else: Rf = interp_R(f, "RmsC_Mpc")
    def c(ft):
        M = ft["x"] * a0 * ft["r"] ** 2 / G / MS if (ft.get("x") is not None and ft.get("r") is not None) else None
        if M is None: raise NS["Missing"]("r")
        return dict(b=1.0, F=1.0 if ft["r"] <= Rf(M) else 0.0, T=0.0)
    return c
def maxratio(f, B):
    a0 = A0[f]; Rf = interp_R(f, "RmsC_Mpc"); o = {}
    groups = dict(S=B["S"], E=B["E"], X=B["X"], U=B["U"], D=[p for v in B["D"].values() for p in v], K=B["K"][0] + B["K"][1])
    for k, pts in groups.items():
        rs = [p["feat"]["r"] / Rf(p["feat"]["x"] * a0 * p["feat"]["r"] ** 2 / G / MS) if isinstance(p, dict) and "feat" in p else
              p["r"] / Rf(p["x"] * a0 * p["r"] ** 2 / G / MS) for p in pts]
        o[k] = float(max(rs))
    return o
gmodes = ("ON", "OFF") if MUT else ("C",)
RES["GB1"] = {}
for gm in gmodes:
    RES["GB1"][gm] = {}
    for f, a0 in A0.items():
        c = cand(f, gm); B = BATT[f]; row = {}
        for gname, fn, fills in NS["GATES"]:
            r = NS["run_gate"](fn, c, B, a0, fills); L0s = GB1J["cands"]["L0"][f][gname]["status"]
            row[gname] = dict(status=r["status"], L0=L0s, num=r["num"], worse=bool(L0s == "PASS" and r["status"] != "PASS"))
            P(f"[{f}] GB1 {gm:3s} {gname:17s} {r['status']:10s} (L0 {L0s}) {NS['short'](gname, r)}")
        if gm == "C": row["max_r_over_Rms"] = maxratio(f, B); P(f"[{f}] GB1 max r / R_ms per class: " + ", ".join(f"{k} {v:.3g}" for k, v in row["max_r_over_Rms"].items()))
        RES["GB1"][gm][f] = row

# ---- labels
if not MUT:
    s1C = all(S1[f]["C"]["pass_"] for f in A0); s1L = all(S1[f]["L"]["pass_"] for f in A0)
    gb_ok = all(not v["worse"] for f in A0 for k, v in RES["GB1"]["C"][f].items() if k.startswith("G"))
    if not s1C: lab = "FAIL (K-G6 KiDS: law off beyond the shell-crossed region at the generous ceiling)"
    elif not gb_ok: lab = "FAIL (GB1 row worse than L0)"
    elif not s1L: lab = "NO VERDICT (K-G6 between R_ms lower and ceiling)"
    else: lab = "STAGE 1 PASS (stages 2-4 to be run)"
    RES["label"] = lab; RES["stages_2_4"] = "NOT REACHED" if lab.startswith("FAIL") else "PENDING"
    P(f"STAGE 1 READING: {lab}")
else:
    on0 = all(abs(S1[f]["ON"]["shift_proj"]) <= 1e-6 for f in A0)
    offG1 = all(RES["GB1"]["OFF"][f]["G1 SPARC"]["status"] == "FAIL" for f in A0) and all(not S1[f]["OFF"]["pass_"] for f in A0)
    mono = all(abs(S1[f]["C100"]["shift_proj"]) <= abs(S1[f]["C"]["shift_proj"]) for f in A0)
    bite_C = all(abs(S1[f]["C"]["shift_proj"] - S1[f]["ON"]["shift_proj"]) > 1e-6 for f in A0)
    RES["MUTATE"] = dict(M_ON_shift0=on0, M_ON_web_r=[ka["KA_SV5"]["r_can"], ka["KA_SV5"]["r_alt"]], M_OFF_fails=offG1, M_R_monotone=mono, graded_differs_from_ON=bite_C,
                         bites=bool(on0 and offG1 and mono and bite_C))
    P(f"MUTATE: M-ON shift 0 {on0} (web r = SV5 iter_1 {ka['KA_SV5']['r_can']:.1f} / {ka['KA_SV5']['r_alt']:.1f} by identity); M-OFF G1 + K-G6 FAIL {offG1}; "
      f"M-R x100 moves toward 0 {mono}; graded key != ON {bite_C} -> {'BITES' if RES['MUTATE']['bites'] else 'NO BITE'}")

# ---- stage 2 (AMENDMENT_A1): the host population's retained phantom as a lensing source
from scipy.special import gamma as Gam
DRV = json.load(open(os.path.join(REPO, "closure_program_2026_10_27", "population", "inputs.json")))["driver2022"]
h70 = h / 0.7
MSTAR = 10 ** DRV["log10_Mstar_h70_minus2"] / h70 ** 2
PHI = np.array([10 ** DRV[k] for k in ("log10_phi1_h70_cubed", "log10_phi2_h70_cubed")]) * 10 ** DRV["add_log10_phi_for_SDSS_and_z0"] * h70 ** 3
ALP = np.array([DRV["alpha1"], DRV["alpha2"]])
def per_dex(lm):
    x = 10 ** lm / MSTAR; return float(math.log(10) * np.sum(PHI * x ** (ALP + 1)) * math.exp(-x))
RHO_D_SUN = OD * 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G) * MPC ** 3 / MS          # comoving Msun / Mpc^3
LG = np.arange(9.0, 12.001, 0.25); LF = np.arange(9.0, 12.0001, 0.02)
def q_pop(a0, z, which="L", scale=1.0):
    aE = 1 / (1 + z)
    if which == "L": tab = np.array([r_ta(10 ** m * MS, a0, aE) for m in LG])
    else: tab = np.array([max(r_ta(10 ** m * MS * (1 + R_DUST), 0.0, aE), r_qx10(10 ** m * MS) * aE) for m in LG])   # NC, QX10 rule scaled to a (reported)
    tab = tab * scale
    Rm = 10 ** np.interp(LF, LG, np.log10(np.maximum(tab, 1e-30)))
    mph = np.array([Mph(R, 10 ** m * MS, a0) / MS if R > 0 else 0.0 for R, m in zip(Rm, LF)])
    rho = float(np.trapz(np.array([per_dex(m) for m in LF]) * mph, LF))
    return rho / RHO_D_SUN, rho, dict(zip([float(x) for x in LG], (tab / MPC).tolist()))
if not MUT and RES["label"].startswith("STAGE 1 PASS"):
    rho_star = float(np.trapz(np.array([per_dex(m) * 10 ** m for m in LF]), LF)); rho_an = float(MSTAR * np.sum(PHI * Gam(ALP + 2)))
    RES["KA"]["KA_A1"] = dict(rho_star_9_12=rho_star, rho_star_analytic_total=rho_an, frac=rho_star / rho_an)
    P(f"KA-A1 GSMF (h {h}): rho_* (9-12) {rho_star:.4e} Msun/Mpc^3 = {rho_star/rho_an:.4f} of the analytic total {rho_an:.4e}; rho_d {RHO_D_SUN:.4e}")
    S2 = {}
    for f, a0 in A0.items():
        S2[f] = {}
        for z in (0.5, 1.0, 2.0):
            q, rho, tab = q_pop(a0, z)
            S2[f][str(z)] = dict(q_pop=q, rho_ph_pop=rho, r_pop=(1 + q) ** 2, RmsL_Mpc=tab, factor_to_line=q / 0.0354,
                                 pass_=bool(q <= 0.0354), graded=(z == 1.0))
            P(f"[{f}] stage 2 z {z}: rho_ph,pop {rho:.3e} Msun/Mpc^3, q_pop {q:.3f} (line 0.0354), r_pop {(1+q)**2:.2f} (line 1.072), "
              f"phi M_ph must fall x{q/0.0354:.0f}; R_ms^L(1e10.5) {np.interp(10.5, LG, list(tab.values())):.3f} Mpc{' [GRADED]' if z == 1.0 else ''}")
        qn, rn, tn = q_pop(a0, 1.0, "NC")
        S2[f]["NC_z1"] = dict(q_pop=qn, factor_to_line=qn / 0.0354)
        P(f"[{f}] stage 2 REPORTED self-consistent R_ms (NC) z 1: q_pop {qn:.3f}, x{qn/0.0354:.0f} over the line")
    RES["stage2"] = S2
    s2ok = all(S2[f]["1.0"]["pass_"] for f in A0)
    RES["label"] = "STAGE 2 PASS (stages 3-4 to be run)" if s2ok else "FAIL (stage 2, population phantom: hosts' retained phantom over-sources CMB lensing)"
    RES["stages_2_4"] = "stage 2 graded; stages 3-4 " + ("PENDING" if s2ok else "NOT REACHED")
    P(f"LABEL WL1: {RES['label']}; {RES['stages_2_4']}")
if MUT:
    q0 = q_pop(A0["canonical"], 1.0, "L", scale=0.0)[0]; RES["MUTATE"]["M_A1_q_zero"] = bool(q0 == 0.0)
    P(f"MUTATE-A1: R_ms -> 0 gives q_pop {q0:.1e} -> {'BITES' if q0 == 0.0 else 'NO BITE'}")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
