#!/usr/bin/env python3
"""QX29 (FROZEN_CRITERIA.md, 346612b24b): gravitationally polarizable (dipolar) cold dark energy medium.
W derived so that spherical statics give g_N = g^2/(g + a0) on the full monopole: 4 pi G Pi = a0 g/(g + a0).
Host rules for the monopole sigma: A (weak clustering, assumed), B1 / B2 (captured cold dust, R = 5.562), Bcal
(B2 at the galaxy-fixed amplitude f R), C (minimal medium, xi = |Pi|/sigma = r). QX27's grader is imported read-only
with its retention function replaced by the QX29 host rule. G6 in qx29_growth.py.
    python3 qx29.py            -> qx29.json/.out
    python3 qx29.py --mutate   -> qx29_MUTATE.json/.out  (M1 polarization off + B2 cold mass; M2 off + A; M3 B1 at 0)
kappa = 1/2 FITTED; not theory closed; footings never pooled. Units kpc, Msun, km/s. 1 thread.
a0 only from the two footings (canonical 9.3603e-11, alt 1.1312e-10 m/s^2); the law's simple mu only."""
import os, sys, json, math, io, contextlib, importlib.util, csv, re, glob
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
MUT = "--mutate" in sys.argv; TAG = "qx29_MUTATE" if MUT else "qx29"
FOOT_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}

# ---- read-only import of QX27's grader (its __main__ block does not run)
_p27 = os.path.join(REPO, "closure_2026_11_06", "QX27_tail_retention_sector", "qx27.py")
_s = importlib.util.spec_from_file_location("qx27_lib", _p27); M27 = importlib.util.module_from_spec(_s)
_argv = sys.argv; sys.argv = [_p27]
with contextlib.redirect_stdout(io.StringIO()): _s.loader.exec_module(M27)
sys.argv = _argv
GK, A0K, R, FCAP, RHO_D0, r_ta = M27.GK, M27.A0K, M27.R, M27.FCAP, M27.RHO_D0, M27.r_ta
ACC, G_SI, MS, KPC_M = M27.ACC, M27.G_SI, M27.MS, M27.KPC_M
LAW_glaw, LAW_glaw_SI, LAW_nu = M27.glaw, M27.glaw_SI, M27.Q8.nu
if MUT:   # polarization off: W = 0, mu = 1, Newtonian everywhere (grader, host solve and SPARC exact-field term)
    M27.glaw = lambda gN, a0k: np.asarray(gN, float) if np.ndim(gN) else float(gN)
    M27.glaw_SI = lambda gN, a0: float(gN)
    M27.Q8.nu = lambda y: np.ones_like(np.asarray(y, float))
glaw = lambda gN, a0k: M27.glaw(gN, a0k)


# ---- the derived W
def W_of(Pi, a0, G):  # SI or any consistent units; y = 4 pi G Pi / a0 < 1
    y = 4 * math.pi * G * Pi / a0; return a0 ** 2 / (4 * math.pi * G) * (-y - math.log1p(-y))
def g_of_Pi(Pi, a0, G):  # dW/dPi
    y = 4 * math.pi * G * Pi / a0; return a0 * y / (1 - y)
def Pi_of_g(g, a0k):  # kpc units, Msun/kpc^2 (polarization off -> 0)
    if MUT: return np.zeros_like(np.asarray(g, float))
    g = np.asarray(g, float); return a0k * g / ((g + a0k) * 4 * math.pi * GK)


# ---- candidates (host rules for sigma)
class Cand:
    def __init__(self, kind, amp=None, name=None): self.kind, self.amp = kind, amp; self._n = name
    def name(self): return self._n or f"{self.kind}" + ("" if self.amp is None else f" amp {self.amp:.4g}")
    v0 = float("nan")
    def F(self, v): return np.ones_like(np.asarray(v, float))
    def N(self): return 0.0


def host_solve(Mb_fn, cand, rta, a0k, Rfac=None, n=900, rmin=1e-3):
    r = np.geomspace(rmin, rta, n); dr = np.diff(r)
    Mb = np.array([Mb_fn(x) for x in r]); Mbt = Mb[-1]
    if cand.kind == "A":
        Mx = np.zeros(n); sig = np.zeros(n)
    elif cand.kind == "B1":
        Mx = cand.amp * Mb; sig = cand.amp * np.gradient(Mb, r) / (4 * math.pi * r ** 2)
    elif cand.kind == "B2":
        Mx = cand.amp * Mbt * (r / rta) ** 0.75; sig = cand.amp * Mbt * 0.75 * r ** -0.25 / rta ** 0.75 / (4 * math.pi * r ** 2)
    elif cand.kind == "C":   # dM/dr = 4 pi r^2 (Pi / r) = 4 pi r Pi(g), g from the law on M_b + M_X; RK2 outward
        Mx = np.zeros(n)
        f = lambda x, mb, mx: 4 * math.pi * x * float(Pi_of_g(glaw(GK * (mb + mx) / x ** 2, a0k), a0k))
        Mx[0] = 0.5 * r[0] * f(r[0], Mb[0], 0.0)
        for i in range(n - 1):
            h = dr[i]; k1 = f(r[i], Mb[i], Mx[i]); mbm = 0.5 * (Mb[i] + Mb[i + 1])
            k2 = f(r[i] + 0.5 * h, mbm, Mx[i] + 0.5 * h * k1); Mx[i + 1] = Mx[i] + h * k2
        sig = np.array([float(Pi_of_g(glaw(GK * (Mb[i] + Mx[i]) / r[i] ** 2, a0k), a0k)) for i in range(n)]) / r
    else: raise ValueError(cand.kind)
    g = glaw(GK * (Mb + Mx) / r ** 2, a0k)
    H = np.concatenate([np.cumsum((0.5 * (g[1:] + g[:-1]) * dr)[::-1])[::-1], [0.0]])
    return dict(r=r, Md=Mx, Mb=Mb, sig=sig, ve=np.sqrt(2 * H), F=np.ones(n), Mlv=np.full(n, 1e300), its=0, conv=True)
M27.solve_tail = host_solve          # QX27's grade / calib / g1 now use the QX29 host rule
Mat, vat = M27.Mat, M27.vat
def sig_at(s, x):
    if x >= s["r"][-1]: return 0.0
    return float(np.exp(np.interp(math.log(max(x, s["r"][0])), np.log(s["r"]), np.log(np.maximum(s["sig"], 1e-300)))))


# ---- G7 dSphs (QX27's hosts) and G10 dipole-continuum
DSPH = []
for row in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "mcconnachie2012_dsph.csv"))):
    if row["Name"] in ("Carina", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans (I)", "Ursa Minor"):
        DSPH.append((row["Name"], 2.0 * 10 ** (-0.4 * (float(row["VMag"]) - 4.83)), float(row["R2"]) / 1e3))
def plummer(M_, a_): return lambda x: M_ * x ** 3 / (x * x + a_ * a_) ** 1.5
def g7(cand, a0k):
    sh = []
    for nm, Ms, a in DSPH:
        h = plummer(Ms, a); s = host_solve(h, cand, r_ta(Ms), a0k); Mb = h(a)
        sh.append(math.log10(glaw(GK * (Mb + Mat(s, a)) / a ** 2, a0k) / glaw(GK * Mb / a ** 2, a0k)))
    return float(np.median(sh))

def xi_over_r(s, x, Mb, a0k):
    g = glaw(GK * (Mb + Mat(s, x)) / x ** 2, a0k); Pi = float(Pi_of_g(g, a0k)); sg = sig_at(s, x) + RHO_D0
    return Pi / sg / x
def g10(cand, foot):
    a0k = A0K[foot]; out = {}
    v = []                                   # KiDS lens radii
    for p in M27.LE:
        Mb = p["Mb"] / MS; x = math.sqrt(G_SI * p["Mb"] / p["gbar"]) / KPC_M
        s = host_solve(M27.expdisc(Mb, 3.2 * M27.rd_of(Mb)), cand, r_ta(Mb), a0k, n=400); v.append(xi_over_r(s, x, M27.expdisc(Mb, 3.2 * M27.rd_of(Mb))(x), a0k))
    out["KiDS"] = v; v = []
    for q in M27.GALS:                       # last SPARC point
        mt = q["meta"]; Mb = (0.5 * mt["L36"] + 1.33 * mt["MHI"]) * 1e9; rd = mt["Rdisk"] if mt["Rdisk"] > 0 else M27.rd_of(Mb)
        h = M27.expdisc(Mb, 3.2 * rd); s = host_solve(h, cand, r_ta(Mb), a0k, n=300); x = float(q["R"][-1]); v.append(xi_over_r(s, x, h(x), a0k))
    out["SPARC_last"] = v; v = []
    for nm, pts in M27.clusters.items():
        Ml, rl = pts[0]["Mb_last"]; h = M27.profile_core([p_["r_kpc"] for p_ in pts], [p_["M_b"] for p_ in pts], Ml, rl)
        s = host_solve(h, cand, r_ta(Ml), a0k)
        for p_ in pts: v.append(xi_over_r(s, p_["r_kpc"], p_["M_b"], a0k))
    out["XCOP"] = v; v = []
    for fst in (0.0, 1.0):
        for gp in M27.GR:
            Mbt = gp["g5"] * (1 + fst); h = M27.profile_core([q_["r_kpc"] for q_ in gp["pts"]], [q_["M_gas"] * (1 + fst) for q_ in gp["pts"]], Mbt, gp["R5"])
            s = host_solve(h, cand, r_ta(Mbt), a0k)
            for q_ in gp["pts"]: v.append(xi_over_r(s, q_["r_kpc"], q_["M_gas"] * (1 + fst), a0k))
    out["groups"] = v; v = []
    for nm, Ms, a in DSPH:
        h = plummer(Ms, a); s = host_solve(h, cand, r_ta(Ms), a0k); v.append(xi_over_r(s, a, h(a), a0k))
    out["dSph"] = v
    allv = np.concatenate([np.asarray(x, float) for x in out.values()])
    res = {k: dict(max=float(np.max(x)), median=float(np.median(x))) for k, x in out.items()}
    res["max"] = float(np.max(allv)); res["median"] = float(np.median(allv)); res["G10"] = bool(np.max(allv) <= 1.0 + 1e-9)
    # Solar System report: local sigma for a MW host (M_b 6e10, R_d 2.6 kpc) at 8.2 kpc; xi in AU at Saturn
    h = M27.expdisc(6e10, 3.2 * 2.6); s = host_solve(h, cand, r_ta(6e10), a0k); sg = sig_at(s, 8.2) + RHO_D0
    Pis = a0k / (4 * math.pi * GK)            # saturated (g >> a0 at Saturn)
    res["SS_sigma_local_Msun_kpc3"] = sg; res["SS_xi_AU"] = Pis / sg * 2.0626e8 if Pis > 0 else 0.0
    return res


# ---- G8 Solar System (record: E2 R1 AQUAL Q2; Saturn monopole against AX1's bound)
E2 = json.load(open(os.path.join(REPO, "doors_push_2026_10_22", "E2_field_equation", "e2_field_equation_results.json")))
GM_SUN, AU = 1.32712440018e20, 1.495978707e11; A_SAT = 9.5826 * AU; SAT_BOUND = 7.0e-15
def g8(foot):
    a0 = FOOT_SI[foot]; gN = GM_SUN / A_SAT ** 2; dg = M27.glaw_SI(gN, a0) - gN
    q = E2["R1"][f"{foot}|none"]["over_Hees"]; qt = E2["R1"][f"{foot}|66.3803"]["over_Hees"]
    if MUT: q = [0.0] * 4
    return dict(Q2_over_Hees=q, Q2_turnoff_reported=qt, Saturn_dg=dg, Saturn_over_bound=dg / SAT_BOUND,
                G8=bool(max(q) <= 1 and dg / SAT_BOUND <= 1))


def calib_all(cand, foot):
    a0k = A0K[foot]; c = M27.calib(cand, a0k, M27.BASE[foot]); c["G7_shift"] = g7(cand, a0k); c["G7"] = bool(c["G7_shift"] <= 0.05)
    c["ok"] = bool(c["C1"] and c["C2"] and c["G7"]); return c

def full(cand, foot, do_g10=True):
    a0k = A0K[foot]; o = M27.grade(cand, a0k, M27.BASE[foot]); o.update(M27.calib(cand, a0k, M27.BASE[foot])); o.update(M27.g1(cand, foot))
    o["G1_line"] = o["G1"]; o["G1"] = bool(o["G1_line"] and o["C1"]); o["G2"] = o["C2"]
    o["KiDS_abs_resid"] = o["C2_shift"] + M27.BASE[foot][0]
    o["dist"] = cand.name()
    for k in ("G8_max_ratio_xcop", "G8_max_ratio_groups", "G8_frac_points_violating", "G8"): o.pop(k, None)   # QX27's Liouville gate: not this class
    o.update({("SS_" + k): v for k, v in g8(foot).items()}); o["G8"] = o.pop("SS_G8")
    if do_g10: t = g10(cand, foot); o["G10_detail"] = t; o["G10"] = t["G10"]; o["G10_max"] = t["max"]; o["G10_median"] = t["median"]
    o["fails"] = [g for g in ("G1", "G2", "G3", "G4", "G5", "G7", "G8", "G10") if g in o and not o[g]]
    return o


def line(f, o):
    P_ = lambda b: "P" if b else "F"
    s = (f"[{f}] {o['dist']}: G1 rms {o['rms']:.4f}@{o['U_median']:.2f} C1 {o['C1_max']:.3f} {P_(o['G1'])} | G2 KiDS shift {o['C2_shift']:+.3f} (abs {o['KiDS_abs_resid']:+.3f}) {P_(o['G2'])} | "
         f"G3 D {o['G3_D']:+.3f} {P_(o['G3'])} | G4 X-COP {o['X_mean']:+.3f}/{o['X_rms']:.3f} {P_(o['G4'])} | G5 [{o['G_fst1']:+.3f},{o['G_fst0']:+.3f}] {P_(o['G5'])} strict {o['G_strict']} | "
         f"G7 {o['G7_median_shift']:+.4f} {P_(o['G7'])} | G8 Q2/Hees max {max(o['SS_Q2_over_Hees']):.2f} Saturn {o['SS_Saturn_over_bound']:.3g}x {P_(o['G8'])}")
    if "G10" in o: s += f" | G10 xi/r max {o['G10_max']:.3g} med {o['G10_median']:.3g} {P_(o['G10'])}"
    return s + f" | FAILS {o['fails']}"


def ka0():
    pats = [re.compile(x) for x in ("1" + r"\.2e-10", "1" + r"\.20e-10", "1" + r"\.2\s*\*\s*1e-10")]
    hits = []
    for fn in glob.glob(os.path.join(HERE, "*.py")):
        for i, ln in enumerate(open(fn).read().splitlines()):
            if any(p.search(ln) for p in pats): hits.append(f"{os.path.basename(fn)}:{i+1}")
    return hits


if __name__ == "__main__":
    OUT = []
    def P(s=""): print(s, flush=True); OUT.append(str(s))
    P(f"QX29 ({'MUTATE' if MUT else 'main'}): dipolar cold dark energy medium. kappa = 1/2 FITTED; not theory closed. Criteria 346612b24b.")
    P(f"R {R:.4f}; f_cap {FCAP}; rho_sea {RHO_D0:.4g} Msun/kpc^3; plain-law bases (KiDS, EL): " + ", ".join(f"{f} {M27.BASE[f][0]:+.4f} {M27.BASE[f][1]:+.4f}" for f in A0K))
    RES = dict(lane="QX29", criteria="346612b24b", mutate=MUT, note="kappa = 1/2 FITTED; not theory closed")
    # KA0 / KA0b
    hits = ka0(); RES["KA0"] = dict(hits=hits, ok=not hits); P(f"KA0 standard-MOND a0 string in QX29 scripts: {hits or 'none'} -> {'PASS' if not hits else 'FAIL'}")
    if hits: raise SystemExit("KA0 FAIL: standard-MOND a0 found")
    ka = {}
    for f in A0K:
        rel = abs(A0K[f] * ACC / FOOT_SI[f] - 1)
        x = np.geomspace(1e-4, 1e4, 200)
        gg = x * A0K[f]; gN = gg ** 2 / (gg + A0K[f]); back = np.array([LAW_glaw(v, A0K[f]) for v in gN]); e = float(np.max(np.abs(back / gg - 1)))
        ka[f] = dict(a0_rel=rel, glaw_inverse_maxrel=e, ok=bool(rel <= 1e-4 and e <= 1e-10))
        P(f"KA0b [{f}] a0 {A0K[f]*ACC:.5e} m/s^2 vs {FOOT_SI[f]:.5e} rel {rel:.1e}; glaw inverse max rel {e:.1e} -> {'PASS' if ka[f]['ok'] else 'FAIL'}")
    RES["KA0b"] = ka
    if not MUT:
        # KA1 derived W (SI)
        k1 = {}
        for f, a0 in FOOT_SI.items():
            errs = []; fd = []
            for x in np.geomspace(1e-4, 1e4, 81):
                g = x * a0; Pi = brentq(lambda P_: g_of_Pi(P_, a0, G_SI) - g, 0.0, a0 / (4 * math.pi * G_SI) * (1 - 1e-15), xtol=1e-30, rtol=1e-15, maxiter=500)
                gN = g - 4 * math.pi * G_SI * Pi; errs.append(abs(gN / (g * g / (g + a0)) - 1))
                h = 1e-6 * Pi; fd.append(abs((W_of(Pi + h, a0, G_SI) - W_of(Pi - h, a0, G_SI)) / (2 * h) / g - 1))
            sat = 4 * math.pi * G_SI * (a0 * 1e4 * a0 / (1e4 * a0 + a0)) / (4 * math.pi * G_SI) / a0
            k1[f] = dict(law_maxrel=max(errs), fd_maxrel=max(fd), sat=sat, ok=bool(max(errs) <= 1e-10 and max(fd) <= 1e-6 and abs(sat - 1) <= 1e-3))
            P(f"KA1 [{f}] W: g_N(W) vs g^2/(g+a0) max rel {max(errs):.1e}; dW/dPi vs g max rel {max(fd):.1e}; 4piG Pi/a0 at g/a0 1e4 {sat:.5f} -> {'PASS' if k1[f]['ok'] else 'FAIL'}")
        RES["KA1"] = k1
        # POST-RESULT (reported only, after KA1 failed as frozen on its finite-difference line): step scaled to (1 - y)
        for f, a0 in FOOT_SI.items():
            fd = []
            for x in np.geomspace(1e-4, 1e4, 81):
                g = x * a0; y = g / (g + a0); Pi = y * a0 / (4 * math.pi * G_SI); h = 1e-5 * Pi * (1 - y)
                fd.append(abs((W_of(Pi + h, a0, G_SI) - W_of(Pi - h, a0, G_SI)) / (2 * h) / g - 1))
            k1[f]["POST_fd_scaled_step_maxrel"] = max(fd)
            P(f"KA1b POST-RESULT [{f}] dW/dPi vs g with step 1e-5 Pi (1 - y): max rel {max(fd):.1e} (reported only)")
        RES["cand"] = {}
        A = Cand("A", name="A weak clustering")
        for f in A0K:
            o = full(A, f); RES["cand"].setdefault("A", {})[f] = o; P(line(f, o))
            refD = 0.210 if f == "canonical" else 0.189; refX = 0.4675 if f == "canonical" else 0.4345; ref1 = (0.0560, 0.58) if f == "canonical" else (0.0558, 0.52)
            ok2 = abs(o["G3_D"] - refD) <= 1e-3; ok3 = abs(o["X_mean"] - refX) <= 2e-3; ok4 = abs(o["rms"] - ref1[0]) <= 1e-4 and abs(o["U_median"] - ref1[1]) <= 0.005
            z = M27.grade(Cand("B1", 0.0), A0K[f], M27.BASE[f]); ok5 = abs(z["X_mean"] - o["X_mean"]) <= 1e-6
            RES.setdefault("KA2_5", {})[f] = dict(KA2=ok2, KA3=ok3, KA4=ok4, KA5=ok5)
            P(f"   KA2 D {o['G3_D']:+.4f} vs {refD:+.3f} {'PASS' if ok2 else 'FAIL'}; KA3 X-COP {o['X_mean']:+.4f} vs {refX:+.4f} {'PASS' if ok3 else 'FAIL'}; "
              f"KA4 SPARC {o['rms']:.4f}@{o['U_median']:.2f} vs {ref1[0]}@{ref1[1]} {'PASS' if ok4 else 'FAIL'}; KA5 B1 amp 0 X-COP {z['X_mean']:+.6f} {'PASS' if ok5 else 'FAIL'}")
            try:
                kh = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "AX1_action_for_law", "khronon", "ax1_khronon.json")))["static"][f"{f}|law"]["Saturn_dg"]
                k6 = abs(o["SS_Saturn_dg"] / kh - 1); RES.setdefault("KA6", {})[f] = dict(rel=k6, ok=bool(k6 <= 1e-6))
                P(f"   KA6 Saturn dg {o['SS_Saturn_dg']:.6e} vs AX1 {kh:.6e} rel {k6:.1e} -> {'PASS' if k6 <= 1e-6 else 'FAIL'}")
            except (OSError, KeyError): P("   KA6 not checked (AX1 json missing)")
        for nm, cd in (("B1", Cand("B1", R, "B1 traced, R")), ("B2", Cand("B2", R, "B2 infall r^-9/4, R")), ("C", Cand("C", name="C minimal medium xi=r"))):
            for f in A0K:
                o = full(cd, f); RES["cand"].setdefault(nm, {})[f] = o; P(line(f, o))
                if nm == "C":
                    mrat = []
                    for p in M27.LE:
                        Mb = p["Mb"] / MS; s = host_solve(M27.expdisc(Mb, 3.2 * M27.rd_of(Mb)), cd, r_ta(Mb), A0K[f]); mrat.append(s["Md"][-1] / Mb)
                    o["C_Mta_over_Mb_KiDS"] = [float(min(mrat)), float(max(mrat))]
                    P(f"   C: minimal medium inside r_ta for KiDS hosts = {min(mrat):.3g}-{max(mrat):.3g} M_b (cosmic share R = {R:.2f})")
                    nos = []                     # POST-RESULT: same floor with g from the baryons alone (no runaway feedback)
                    for p in M27.LE:
                        Mb = p["Mb"] / MS; h_ = M27.expdisc(Mb, 3.2 * M27.rd_of(Mb)); rr = np.geomspace(1e-3, r_ta(Mb), 900)
                        gb = glaw(GK * np.array([h_(x) for x in rr]) / rr ** 2, A0K[f]); dm = 4 * math.pi * rr * Pi_of_g(gb, A0K[f])
                        nos.append(float(np.sum(0.5 * (dm[1:] + dm[:-1]) * np.diff(rr))) / Mb)
                    o["POST_C_noself_Mta_over_Mb_KiDS"] = [min(nos), max(nos)]
                    P(f"   C POST-RESULT: the same floor with g from baryons only = {min(nos):.3g}-{max(nos):.3g} M_b (reported only)")
        for nm, cd in (("B1_fcap", Cand("B1", FCAP * R, "B1 traced, f_cap R")), ("B2_fcap", Cand("B2", FCAP * R, "B2 infall, f_cap R"))):
            for f in A0K:
                o = full(cd, f, do_g10=False); RES["cand"].setdefault(nm, {})[f] = o; P("   reported " + line(f, o))
        # Bcal: f from C1 + C2 + G7 only, B2 profile
        FG = np.geomspace(1e-4, 1.0, 61)
        for f in A0K:
            last = None; rows = []
            for fr in FG:
                c = calib_all(Cand("B2", fr * R), f); rows.append(dict(f=float(fr), C1=c["C1_max"], C2=c["C2_shift"], G7=c["G7_shift"], ok=c["ok"]))
                if not c["ok"]: break
                last = float(fr)
            ent = dict(f_gal=last, scan=rows)
            if last is None: P(f"Bcal [{f}] no f on the grid passes C1+C2+G7"); RES["cand"].setdefault("Bcal", {})[f] = ent; continue
            o = full(Cand("B2", last * R, f"Bcal B2 at f {last:.4g} (f R {last*R:.4g})"), f); ent.update(o); RES["cand"].setdefault("Bcal", {})[f] = ent
            P(f"Bcal [{f}] f_gal {last:.4g} (first failing f {rows[-1]['f']:.4g}: C1 {rows[-1]['C1']:.3f} C2 {rows[-1]['C2']:+.3f} G7 {rows[-1]['G7']:+.4f})"); P("   " + line(f, o))
        # summary
        P("\nSummary: failing gates per candidate (G6 conditional and G9 not evaluable apply to all; see README)")
        for nm in ("A", "B1", "B2", "Bcal", "C"):
            P(f"   {nm}: " + "; ".join(f"{f} {RES['cand'][nm][f].get('fails')}" for f in A0K))
        RES["any_candidate_passes_static"] = bool(any(all(not RES["cand"][nm][f].get("fails", ["x"]) for f in A0K) for nm in ("A", "B1", "B2", "Bcal", "C")))
        P(f"any candidate passes G1-G5, G7, G8, G10 on both footings: {RES['any_candidate_passes_static']}")
    else:
        for nm, cd in (("M1", Cand("B2", R, "M1 polarization off + B2 cold mass R")), ("M2", Cand("A", name="M2 polarization off + A"))):
            RES[nm] = {}
            for f in A0K:
                o = full(cd, f, do_g10=False); core = [g for g in ("G1", "G2", "G3", "G4", "G5", "G7") if not o[g]]
                o["bites"] = bool(core) if nm == "M1" else bool(not o["G1"]); RES[nm][f] = o
                P(line(f, o) + f" -> {'BITES' if o['bites'] else 'DOES NOT BITE'}")
        P("M3 (B1 at amplitude 0 equals A) is checked in the main run as KA5.")
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
