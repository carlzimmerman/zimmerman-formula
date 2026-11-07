#!/usr/bin/env python3
"""QX27 (FROZEN_CRITERIA.md, 8e1126f9e3): cold dark energy sector, cold before z_h = 10, then a power-law-tail speed
distribution p_n(v) = N v^2 (1 + v^2/(m v0^2))^-m, m = (n+2)/2. Retention dM_X = R F_n(v_esc) dM_b, v_esc from the
self-consistent a0-law potential to r_ta. v0 per (n, footing) fixed by SPARC G5 + KiDS only; then G1, G3-G5, G7, G8
graded (G6 growth in qx27_growth.py).
    python3 qx27.py            -> qx27.json/.out
    python3 qx27.py --mutate   -> qx27_MUTATE.json/.out  (M1 Maxwellian same v0; M2 R = 0; M3 v0 30 km/s)
kappa = 1/2 FITTED; not theory closed; footings never pooled. Units kpc, Msun, km/s. 1 thread."""
import os, sys, json, math, runpy, io, contextlib, importlib.util, csv
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.special import betainc, gammainc, beta as Bfn

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
MUT = "--mutate" in sys.argv; TAG = "qx27_MUTATE" if MUT else "qx27"
Q3 = os.path.join(REPO, "closure_2026_11_06", "QX12_triangle", "iter_3_isothermal_sea", "qx12_i3.py")
argv0 = sys.argv; sys.argv = [Q3]
with contextlib.redirect_stdout(io.StringIO()):
    L = runpy.run_path(Q3, run_name="qx12_i3_lib")          # read-only reuse: QX10 lib + A1 hosts
sys.argv = argv0
GK, glaw, A0K, R, FCAP, RHO_D0, r_ta = (L[k] for k in ("GK", "glaw", "A0K", "R", "FCAP", "RHO_D0", "r_ta"))
expdisc, G5SYS, LE, EL, GR, clusters, baselines, rd_of, profile_core = (L[k] for k in ("expdisc", "G5SYS", "LE", "EL", "GR", "clusters", "baselines", "rd_of", "profile_core"))
G_SI, MS, KPC_M, ACC, glaw_SI = L["G_SI"], L["MS"], L["KPC_M"], L["ACC"], L["glaw_SI"]

NGRID = [3.5, 4.0, 5.0, 6.0, 8.0, 12.0]
V0GRID = np.geomspace(100.0, 30000.0, 71)


# ------------------------------------------------------------------ the speed distributions
class Tail:
    def __init__(self, v0, n): self.v0, self.n, self.m = v0, n, (n + 2) / 2
    def F(self, v):
        u = np.asarray(v, float) ** 2 / (self.m * self.v0 ** 2); return betainc(1.5, self.m - 1.5, u / (1 + u))
    def N(self): return 2.0 / ((self.m * self.v0 ** 2) ** 1.5 * Bfn(1.5, self.m - 1.5))           # p = N v^2 (...)
    def sigma1d(self): return math.sqrt(self.m * self.v0 ** 2 * Bfn(2.5, self.m - 2.5) / Bfn(1.5, self.m - 1.5) / 3)
    def name(self): return f"tail n={self.n:g} v0={self.v0:.1f}"
class Maxw:
    def __init__(self, v0): self.v0 = v0
    def F(self, v): return gammainc(1.5, np.asarray(v, float) ** 2 / self.v0 ** 2)
    def N(self): return 4.0 / (math.sqrt(math.pi) * self.v0 ** 3)
    def sigma1d(self): return self.v0 / math.sqrt(2)
    def name(self): return f"Maxwellian v0={self.v0:.1f}"
class Zero:                                     # R = 0 (no sector)
    v0 = float("nan")
    def F(self, v): return np.zeros_like(np.asarray(v, float))
    def N(self): return 0.0
    def name(self): return "R = 0"


def solve_tail(Mb_fn, dist, rta, a0k, Rfac=None, n=900, rmin=1e-3):
    Rf = R if Rfac is None else Rfac
    r = np.geomspace(rmin, rta, n); dr = np.diff(r)
    Mb = np.array([Mb_fn(x) for x in r]); dMb = np.diff(Mb)
    Mx = np.zeros(n); err = 1.0
    for it in range(4000):
        g = glaw(GK * (Mb + Mx) / r ** 2, a0k)
        H = np.concatenate([np.cumsum((0.5 * (g[1:] + g[:-1]) * dr)[::-1])[::-1], [0.0]])
        ve = np.sqrt(2 * H); F = dist.F(ve)
        new = Rf * np.concatenate([[F[0] * Mb[0]], F[0] * Mb[0] + np.cumsum(0.5 * (F[1:] + F[:-1]) * dMb)])
        err = float(np.max(np.abs(new - Mx)) / max(np.max(new), 1e-300)) if np.max(new) > 0 else 0.0
        Mx = 0.5 * Mx + 0.5 * new
        if err < 1e-7 and it > 3: break
    g = glaw(GK * (Mb + new) / r ** 2, a0k)
    H = np.concatenate([np.cumsum((0.5 * (g[1:] + g[:-1]) * dr)[::-1])[::-1], [0.0]]); ve = np.sqrt(2 * H)
    # G8: Liouville bound on the bound mass inside each radius, plus the sea itself
    rho_max = RHO_D0 * (dist.N() * ve ** 3 / 3.0 + 1.0)
    sh = 4 * math.pi * r ** 2 * rho_max
    Mlv = np.concatenate([[4 / 3 * math.pi * r[0] ** 3 * rho_max[0]], 4 / 3 * math.pi * r[0] ** 3 * rho_max[0] + np.cumsum(0.5 * (sh[1:] + sh[:-1]) * dr)])
    return dict(r=r, Md=new, ve=ve, F=dist.F(ve), Mlv=Mlv, its=it, conv=bool(err < 1e-7))


def Mat(sol, x, key="Md"):
    a = sol[key]
    if x <= sol["r"][0]: return float(a[0] * (x / sol["r"][0]) ** 3)
    if x >= sol["r"][-1]: return float(a[-1])
    return float(np.interp(math.log(x), np.log(sol["r"]), a))
def vat(sol, x): return float(np.interp(math.log(min(max(x, sol["r"][0]), sol["r"][-1])), np.log(sol["r"]), sol["ve"]))


BASE = {f: baselines(a) for f, a in A0K.items()}

def calib(dist, a0k, base, Rfac=None):
    """C1 (G5 list) and C2 (KiDS shift)."""
    g5 = []
    for nm, Mb, Ro in G5SYS:
        s = solve_tail(expdisc(Mb, Ro), dist, r_ta(Mb), a0k, Rfac); g5.append(Mat(s, Ro) / Mb)
    d = []; sols = {}
    for p in LE:
        Mb = p["Mb"] / MS; r = math.sqrt(G_SI * p["Mb"] / p["gbar"]) / KPC_M; key = round(math.log10(Mb), 6)
        if key not in sols: sols[key] = solve_tail(expdisc(Mb, 3.2 * rd_of(Mb)), dist, r_ta(Mb), a0k, Rfac)
        mx = Mat(sols[key], r); gN = p["gbar"] + G_SI * mx * MS / (r * KPC_M) ** 2
        d.append(math.log10(p["gobs"] / glaw_SI(max(gN, 1e-30), a0k * ACC)))
    c2 = float(np.mean(d)) - base[0]
    kv = [vat(s, 300.0) for s in sols.values()]
    return dict(C1_max=max(g5), C1=bool(max(g5) <= 0.3), C2_shift=c2, C2=bool(abs(c2) <= 0.05), ok=bool(max(g5) <= 0.3 and abs(c2) <= 0.05),
                kids_vesc_300kpc=[min(kv), max(kv)])


def find_v0min(mk, a0k, base):
    """Scan down from the top of the grid; v0_min = grid value just above the first failure."""
    last = None; rows = []
    for v0 in V0GRID[::-1]:
        c = calib(mk(float(v0)), a0k, base); rows.append(dict(v0=float(v0), **c))
        if not c["ok"]: break
        last = float(v0)
    return last, rows


# ------------------------------------------------------------------ predictions
def grade(dist, a0k, base, Rfac=None):
    o = {}; nconv = ntot = 0
    # G3 ellipticals, absolute D (QX18 line)
    d = []; dpl = []; el_ve = []
    for e in EL:
        Mt = e["Mbar"](1e9); s = solve_tail(e["Mbar"], dist, r_ta(Mt), a0k, Rfac); ntot += 1; nconv += s["conv"]
        for m in (2, 4, 8):
            x = m * e["Re"]; Mp = glaw(GK * (e["Mbar"](x) + Mat(s, x)) / x ** 2, a0k) * x ** 2 / GK; d.append(math.log10(e["Mtot"](x) / Mp))
            el_ve.append(vat(s, x))
    o["G3_D"] = float(np.mean(d)); o["G3"] = bool(abs(o["G3_D"]) <= 0.15); o["EL_vesc"] = [min(el_ve), max(el_ve)]
    # G4 X-COP + G8
    xd = []; lv_x = []; xve = []; xF = []
    for nm, pts in clusters.items():
        Ml, rl = pts[0]["Mb_last"]; host = profile_core([p_["r_kpc"] for p_ in pts], [p_["M_b"] for p_ in pts], Ml, rl)
        s = solve_tail(host, dist, r_ta(Ml), a0k, Rfac); ntot += 1; nconv += s["conv"]
        for p_ in pts:
            x = p_["r_kpc"]; Mx = Mat(s, x); Mp = glaw(GK * (p_["M_b"] + Mx) / x ** 2, a0k) * x ** 2 / GK; xd.append(math.log10(p_["M_obs"] / Mp))
            lv_x.append(Mx / Mat(s, x, "Mlv")); xve.append(vat(s, x)); xF.append(Mx / (R * p_["M_b"]))
    xd = np.array(xd); o["X_mean"] = float(xd.mean()); o["X_rms"] = float(np.sqrt((xd ** 2).mean()))
    o["G4"] = bool(abs(o["X_mean"]) <= 0.05 and o["X_rms"] <= 0.10)
    o["X_vesc"] = [min(xve), max(xve)]; o["X_ret_frac"] = [float(min(xF)), float(np.median(xF)), float(max(xF))]
    # G5 groups + G8
    gm = {}; strict = {}; lv_g = []; gve = []; gF = []
    for fst in (0.0, 1.0):
        v = []; npass = 0
        for gp in GR:
            Mbt = gp["g5"] * (1 + fst)
            host = profile_core([q_["r_kpc"] for q_ in gp["pts"]], [q_["M_gas"] * (1 + fst) for q_ in gp["pts"]], Mbt, gp["R5"])
            s = solve_tail(host, dist, r_ta(Mbt), a0k, Rfac); ntot += 1; nconv += s["conv"]; ok = True
            for q_ in gp["pts"]:
                x = q_["r_kpc"]; Mb = q_["M_gas"] * (1 + fst); Mx = Mat(s, x); Mp = glaw(GK * (Mb + Mx) / x ** 2, a0k) * x ** 2 / GK
                dl = math.log10(q_["M_obs"] / Mp); v.append(dl); ok &= abs(dl) <= 2 * q_["eM"] / (q_["M_obs"] * math.log(10))
                lv_g.append(Mx / Mat(s, x, "Mlv")); gve.append(vat(s, x)); gF.append(Mx / (R * Mb))
            npass += ok
        gm[fst] = float(np.mean(v)); strict[f"fst{fst:g}"] = int(npass)
    lo, hi = sorted([gm[0.0], gm[1.0]])
    o["G_fst0"] = gm[0.0]; o["G_fst1"] = gm[1.0]; o["G5"] = bool(lo <= 0.05 and hi >= -0.05); o["G_strict"] = strict
    o["G_vesc"] = [min(gve), max(gve)]; o["G_ret_frac"] = [float(min(gF)), float(np.median(gF)), float(max(gF))]
    o["G8_max_ratio_xcop"] = float(max(lv_x)); o["G8_max_ratio_groups"] = float(max(lv_g))
    o["G8_frac_points_violating"] = float(np.mean(np.array(lv_x + lv_g) > 1.0))
    o["G8"] = bool(max(lv_x + lv_g) <= 1.0)
    # G7 dSphs (MW classical, McConnachie 2012), Plummer hosts, M* = 2 L_V
    sh = []
    for row in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "mcconnachie2012_dsph.csv"))):
        if row["Name"] not in ("Carina", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans (I)", "Ursa Minor"): continue
        Ms = 2.0 * 10 ** (-0.4 * (float(row["VMag"]) - 4.83)); a = float(row["R2"]) / 1e3
        host = (lambda M_, a_: (lambda x: M_ * x ** 3 / (x * x + a_ * a_) ** 1.5))(Ms, a)
        s = solve_tail(host, dist, r_ta(Ms), a0k, Rfac); ntot += 1; nconv += s["conv"]
        Mb = host(a); sh.append(math.log10(glaw(GK * (Mb + Mat(s, a)) / a ** 2, a0k) / glaw(GK * Mb / a ** 2, a0k)))
    o["G7_median_shift"] = float(np.median(sh)); o["G7_n"] = len(sh); o["G7"] = bool(o["G7_median_shift"] <= 0.05)
    o["conv_frac"] = nconv / ntot
    return o


# ------------------------------------------------------------------ G1 SPARC on QX8's exact field
_spec = importlib.util.spec_from_file_location("qx8_lib", os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field", "qx8.py"))
Q8 = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()): _spec.loader.exec_module(Q8)
GALS = Q8.load_sparc()
PARTS = {f: [dict(np.load(os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field", "parts", f, f"{i:03d}.npz"), allow_pickle=False)) for i in range(len(GALS))] for f in A0K}

def g1(dist, foot, Rfac=None):
    a0 = Q8.FOOT[foot]; a0k = A0K[foot]; lU = np.log(Q8.UPS); lN = np.log(Q8.NODES); rows = []; fr = []
    for q, pt in zip(GALS, PARTS[foot]):
        mt = q["meta"]; Mb = (0.5 * mt["L36"] + 1.33 * mt["MHI"]) * 1e9
        rd = mt["Rdisk"] if mt["Rdisk"] > 0 else rd_of(Mb)
        s = solve_tail(expdisc(Mb, 3.2 * rd), dist, r_ta(Mb), a0k, Rfac, n=500)
        Mx = np.array([Mat(s, x) for x in q["R"]]); gX = GK * Mx / q["R"] ** 2 * ACC        # m/s^2
        fr.append(float(Mx[-1] / Mb))
        GB = q["GB"] + gX[:, None]
        lgl = np.log10(np.maximum(Q8.nu(GB / a0) * GB, 1e-300))
        Tf = np.array([np.interp(lU, lN, pt["T"][:, j]) for j in range(pt["T"].shape[1])])
        rows.append(Q8.fit_one(q, lgl + Tf))
    st = Q8.pooled(rows)
    return dict(rms=st["rms"], U_median=st["U_median"], G1=bool(Q8.line(st)), Mx_last_over_Mb_max=max(fr), Mx_last_over_Mb_median=float(np.median(fr)))


def full(dist, foot, Rfac=None):
    a0k = A0K[foot]; o = grade(dist, a0k, BASE[foot], Rfac); o.update(calib(dist, a0k, BASE[foot], Rfac)); o.update(g1(dist, foot, Rfac))
    o["G2"] = o["C2"]; o["dist"] = dist.name()
    o["pass_static"] = bool(o["G1"] and o["G3"] and o["G4"] and o["G5"] and o["G7"] and o["G8"])
    return o


def line_of(f, o):
    return (f"[{f}] {o['dist']}: C1 {o['C1_max']:.3f} C2/G2 {o['C2_shift']:+.3f} | G1 rms {o['rms']:.4f}@{o['U_median']:.2f} {'P' if o['G1'] else 'F'} | "
            f"G3 D {o['G3_D']:+.3f} {'P' if o['G3'] else 'F'} | G4 X-COP {o['X_mean']:+.3f}/{o['X_rms']:.3f} {'P' if o['G4'] else 'F'} (ret {o['X_ret_frac'][1]:.2f}) | "
            f"G5 groups [{o['G_fst1']:+.3f},{o['G_fst0']:+.3f}] {'P' if o['G5'] else 'F'} strict {o['G_strict']} (ret {o['G_ret_frac'][1]:.2f}) | "
            f"G7 {o['G7_median_shift']:+.4f} {'P' if o['G7'] else 'F'} | G8 max M_X/M_Liouville X-COP {o['G8_max_ratio_xcop']:.3g} groups {o['G8_max_ratio_groups']:.3g} {'P' if o['G8'] else 'F'} | conv {o['conv_frac']:.2f}")


if __name__ == "__main__":
    OUT = []
    def P(s=""): print(s, flush=True); OUT.append(str(s))
    P(f"QX27 ({'MUTATE' if MUT else 'main'}): power-law-tail retention sector. kappa = 1/2 FITTED; not theory closed. Criteria 8e1126f9e3.")
    P(f"R {R:.3f}; rho_sea {RHO_D0:.4g} Msun/kpc^3; plain-law bases (KiDS, EL): " + ", ".join(f"{f} {BASE[f][0]:+.4f} {BASE[f][1]:+.4f}" for f in A0K))
    RES = dict(lane="QX27", criteria="8e1126f9e3", mutate=MUT, note="kappa = 1/2 FITTED; not theory closed")
    if not MUT:
        vv = np.geomspace(10, 1e6, 400)
        ka1a = float(abs(Tail(1000.0, 4.0).F(1e9) - 1)); ka1b = float(np.max(np.abs(Tail(1000.0, 400.0).F(vv) - Maxw(1000.0).F(vv))))
        RES["KA1"] = dict(F_inf_minus_1=ka1a, n400_vs_maxwell=ka1b, ok=bool(ka1a < 1e-9 and ka1b <= 2e-3))
        P(f"KA1: F(inf)-1 {ka1a:.1e}; n=400 vs Maxwellian max |dF| {ka1b:.2e} (line 2e-3) -> {'PASS' if RES['KA1']['ok'] else 'FAIL'}")
        RES["KA2"] = {f: BASE[f][1] for f in A0K}
        ok2 = abs(BASE["canonical"][1] - 0.210) <= 1e-3 and abs(BASE["alt"][1] - 0.189) <= 1e-3
        P(f"KA2 plain-law ellipticals D {BASE['canonical'][1]:+.4f} / {BASE['alt'][1]:+.4f} vs QX18 +0.210/+0.189 -> {'PASS' if ok2 else 'FAIL (reported; G3 graded as computed)'}")
        RES["KA2"]["ok"] = bool(ok2)
        RES["KA3_KA4"] = {}
        for f in A0K:
            z = full(Zero(), f); RES["KA3_KA4"][f] = z
            P(f"KA3/KA4 [{f}] R=0: X-COP {z['X_mean']:+.4f}; SPARC exact rms {z['rms']:.4f}@{z['U_median']:.2f}; G3 D {z['G3_D']:+.4f}")
            c = calib(Tail(30000.0, 4.0), A0K[f], BASE[f]); RES.setdefault("KA5", {})[f] = c
            P(f"KA5 [{f}] v0 30000 n 4: C2 {c['C2_shift']:+.4f} C1 {c['C1_max']:.4f} -> {'PASS' if abs(c['C2_shift']) <= 0.02 else 'FAIL'}")
        RES["per_n"] = {}
        for n in NGRID:
            RES["per_n"][str(n)] = {}
            for f in A0K:
                v0m, rows = find_v0min(lambda v0: Tail(v0, n), A0K[f], BASE[f])
                ent = dict(v0_min=v0m, scan=rows)
                if v0m is None:
                    P(f"[{f}] n {n:g}: no v0 on the grid passes calibration"); RES["per_n"][str(n)][f] = ent; continue
                d = Tail(v0m, n); o = full(d, f); ent.update(o); ent["sigma1d"] = d.sigma1d()
                ov = full(d, f, Rfac=FCAP * R); ent["variant_fcap"] = {k: ov[k] for k in ("X_mean", "X_rms", "G_fst0", "G_fst1", "G3_D", "G8_max_ratio_xcop")}
                RES["per_n"][str(n)][f] = ent
                P(f"n {n:g} [{f}] v0_min {v0m:.1f} km/s (sigma_1D {d.sigma1d():.1f}); KiDS v_esc(300 kpc) {o['kids_vesc_300kpc'][0]:.0f}-{o['kids_vesc_300kpc'][1]:.0f}; "
                  f"EL v_esc {o['EL_vesc'][0]:.0f}-{o['EL_vesc'][1]:.0f}; groups {o['G_vesc'][0]:.0f}-{o['G_vesc'][1]:.0f}; X-COP {o['X_vesc'][0]:.0f}-{o['X_vesc'][1]:.0f}")
                P("   " + line_of(f, o))
                P(f"   variant f_cap R: X-COP {ov['X_mean']:+.3f}/{ov['X_rms']:.3f}, groups [{ov['G_fst1']:+.3f},{ov['G_fst0']:+.3f}], G3 {ov['G3_D']:+.3f}, G8 {ov['G8_max_ratio_xcop']:.3g}")
    else:
        q = json.load(open(os.path.join(HERE, "qx27.json")))
        RES["M1"] = {}; bites_all = True
        for n in NGRID:
            RES["M1"][str(n)] = {}
            for f in A0K:
                v0m = q["per_n"][str(n)][f]["v0_min"]
                if v0m is None: continue
                o = full(Maxw(v0m), f); b = not o["pass_static"]; bites_all &= b; o["bites"] = b
                RES["M1"][str(n)][f] = o
                P(f"M1 n {n:g} [{f}] Maxwellian at v0 {v0m:.1f}: " + line_of(f, o) + f" -> {'BITES' if b else 'DOES NOT BITE'}")
        RES["M1_all_bite"] = bool(bites_all)
        RES["M1b"] = {}
        for f in A0K:
            v0m, rows = find_v0min(lambda v0: Maxw(v0), A0K[f], BASE[f])
            if v0m is None: P(f"M1b [{f}] no Maxwellian v0 passes calibration"); continue
            o = full(Maxw(v0m), f); RES["M1b"][f] = dict(v0_min=v0m, **o)
            P(f"M1b [{f}] Maxwellian own v0_min {v0m:.1f}: " + line_of(f, o))
        RES["M2"] = {}
        for f in A0K:
            o = grade(Zero(), A0K[f], BASE[f]); ref = 0.4675 if f == "canonical" else 0.4345
            RES["M2"][f] = dict(X_mean=o["X_mean"], bites=bool(abs(o["X_mean"] - ref) <= 2e-3))
            P(f"M2 [{f}] R = 0: X-COP {o['X_mean']:+.4f} (ref {ref:+.4f}) -> {'BITES' if RES['M2'][f]['bites'] else 'DOES NOT BITE'}")
            c = calib(Tail(30.0, 4.0), A0K[f], BASE[f]); RES.setdefault("M3", {})[f] = dict(c, bites=bool(not c["ok"]))
            P(f"M3 [{f}] v0 30 n 4: C1 {c['C1_max']:.3f} C2 {c['C2_shift']:+.3f} -> {'BITES' if not c['ok'] else 'DOES NOT BITE'}")
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
