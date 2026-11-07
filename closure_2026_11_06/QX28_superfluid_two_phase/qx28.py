#!/usr/bin/env python3
"""QX28 (FROZEN_CRITERIA.md, c5852ac12f): two-phase superfluid cold dark energy sector (BK class). TEST lane.
Condensed phase: P = K rho^3 Thomas-Fermi condensate (cosmic share R M_b, kept inside r_ta) in the Newtonian
potential of baryons + itself; phonons give the law's force on baryons: g = glaw(g_N,b) + G M_X/r^2.
Normal phase: Newtonian, M_X = R M_b(<r). Phase: condensed iff M_b,tot <= M_c (largest calibration host).
K_min from SPARC G5 (C1) + KiDS (C2) only. Law g_N = g^2/(g + a0), footings canonical 9.3603e-11 / alt 1.1312e-10.
    python3 qx28.py            -> qx28.json/.out
    python3 qx28.py --mutate   -> qx28_MUTATE.json/.out  (M1 always condensed; M2 always normal; M3 K = 1e-8)
kappa = 1/2 FITTED; not theory closed; footings never pooled. Units kpc, Msun, km/s. 1 thread."""
import os, sys, json, math, runpy, io, contextlib, importlib.util, csv, glob, re
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
MUT = "--mutate" in sys.argv; TAG = "qx28_MUTATE" if MUT else "qx28"
FOOT_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}

# ------------------------------------------------------------------ KA0 (a): no standard-MOND a0 literal in QX28 scripts
_bad = re.compile(r"1\.2" + r"0*\s*[eE]\s*-\s*10\b|1\.2" + r"0*\s*\*\s*10\s*\*\*\s*\(?-10")
KA0a_hits = [(os.path.basename(p), i + 1) for p in sorted(glob.glob(os.path.join(HERE, "*.py")))
             for i, ln in enumerate(open(p)) if _bad.search(ln)]
if KA0a_hits:
    sys.exit(f"KA0 FAIL: standard-MOND a0 literal found in {KA0a_hits}")

Q3 = os.path.join(REPO, "closure_2026_11_06", "QX12_triangle", "iter_3_isothermal_sea", "qx12_i3.py")
argv0 = sys.argv; sys.argv = [Q3]
with contextlib.redirect_stdout(io.StringIO()):
    L = runpy.run_path(Q3, run_name="qx12_i3_lib")          # read-only reuse: QX10 lib + A1 hosts
sys.argv = argv0
GK, glaw, A0K, R, RHO_D0, r_ta = (L[k] for k in ("GK", "glaw", "A0K", "R", "RHO_D0", "r_ta"))
expdisc, G5SYS, LE, EL, GR, clusters, baselines, rd_of, profile_core = (L[k] for k in ("expdisc", "G5SYS", "LE", "EL", "GR", "clusters", "baselines", "rd_of", "profile_core"))
G_SI, MS, KPC_M, ACC, glaw_SI = L["G_SI"], L["MS"], L["KPC_M"], L["ACC"], L["glaw_SI"]

_spec = importlib.util.spec_from_file_location("qx8_lib", os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field", "qx8.py"))
Q8 = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()): _spec.loader.exec_module(Q8)

# ------------------------------------------------------------------ KA0 (b), (c): the law and the footings
def ka0():
    out = {"scan_hits": KA0a_hits}
    gN = np.geomspace(1e-14, 1e-6, 400); worst = 0.0
    for f, a0 in FOOT_SI.items():
        a0k = A0K[f]
        out[f"a0_lib_SI_{f}"] = a0k * ACC; out[f"a0_qx8_{f}"] = Q8.FOOT[f]
        for g, aa in ((glaw_SI(gN, a0), a0), (Q8.nu(gN / a0) * gN, a0), (glaw(gN / ACC, a0k) * ACC, a0k * ACC)):
            worst = max(worst, float(np.max(np.abs(g ** 2 / (g + aa) - gN) / gN)))   # each law against its own a0
    out["max_rel_law_residual"] = worst
    out["ok"] = bool(not KA0a_hits and worst <= 1e-12
                     and all(abs(out[f"a0_lib_SI_{f}"] / FOOT_SI[f] - 1) < 1e-4 and Q8.FOOT[f] == FOOT_SI[f] for f in FOOT_SI))
    return out
KA0 = ka0()
if not KA0["ok"]:
    sys.exit(f"KA0 FAIL: {KA0}")

KGRID = np.geomspace(1e-8, 1e4, 61)


# ------------------------------------------------------------------ Thomas-Fermi condensate, P = K rho^3
def solve_tf(Mb_fn, MS_tot, K, rta, n=900, rmin=1e-3, rout_fac=60.0):
    """1.5 K rho^2 = mu - Phi; Phi Newtonian (baryons + condensate). Total condensate mass MS_tot on the grid to
    rout_fac * r_ta. Returns cumulative condensate mass on the grid, its outer radius, the kept fraction inside r_ta."""
    r = np.geomspace(rmin, rout_fac * rta, n); dr = np.diff(r)
    Mb = np.array([Mb_fn(min(x, rta)) for x in r])            # baryons end at r_ta
    sh_w = 4 * math.pi * r ** 2
    def cum(rho):
        s = sh_w * rho
        return np.concatenate([[4 / 3 * math.pi * r[0] ** 3 * rho[0]], 4 / 3 * math.pi * r[0] ** 3 * rho[0] + np.cumsum(0.5 * (s[1:] + s[:-1]) * dr)])
    Mx = np.zeros(n); err = 1.0
    if MS_tot <= 0: return dict(r=r, Md=Mx, R_tf=0.0, kept=0.0, conv=True, its=0, edge=False)
    for it in range(400):
        g = GK * (Mb + Mx) / r ** 2
        Phi = -np.concatenate([np.cumsum((0.5 * (g[1:] + g[:-1]) * dr)[::-1])[::-1], [0.0]]) - GK * (Mb[-1] + Mx[-1]) / r[-1]
        def mass(mu): return cum(np.sqrt(np.maximum(mu - Phi, 0.0) / (1.5 * K)))[-1]
        lo = Phi.min(); hi = Phi.max() + 1.0
        while mass(hi) < MS_tot: hi = Phi.max() + 2 * (hi - Phi.max())
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if mass(mid) < MS_tot: lo = mid
            else: hi = mid
        rho = np.sqrt(np.maximum(0.5 * (lo + hi) - Phi, 0.0) / (1.5 * K)); new = cum(rho)
        err = float(np.max(np.abs(new - Mx)) / MS_tot)
        Mx = new if it == 0 else 0.5 * Mx + 0.5 * new
        if err < 1e-6 and it > 2: break
    nz = np.nonzero(rho > 0)[0]; Rtf = float(r[nz[-1]]) if len(nz) else 0.0
    kept = float(np.interp(math.log(rta), np.log(r), Mx) / MS_tot)
    return dict(r=r, Md=Mx, rho=rho, R_tf=Rtf, kept=kept, conv=bool(err < 1e-6), its=it, edge=bool(Rtf >= r[-2]))


def Mat(sol, x, rta):
    x = min(x, rta); a = sol["Md"]
    if x <= sol["r"][0]: return float(a[0] * (x / sol["r"][0]) ** 3)
    return float(np.interp(math.log(x), np.log(sol["r"]), a))


class Phase:
    """mode 'rule' (M_c), 'cond' (always condensed, M1), 'norm' (always normal, M2). Rfac = R (0 for KA3/KA4)."""
    def __init__(self, K, Mc, mode="rule", Rfac=None): self.K, self.Mc, self.mode, self.Rf = K, Mc, mode, (R if Rfac is None else Rfac)
    def condensed(self, Mbt):
        return True if self.mode == "cond" else False if self.mode == "norm" else bool(Mbt <= self.Mc * (1 + 1e-9))
    def host(self, Mb_fn, Mbt, rta, n=900):
        """returns (cond, Mx(x), sol)"""
        if self.condensed(Mbt):
            s = solve_tf(Mb_fn, self.Rf * Mbt, self.K, rta, n=n)
            return True, (lambda x: Mat(s, x, rta)), s
        return False, (lambda x: self.Rf * Mb_fn(min(x, rta))), None
    def Mpred(self, cond, Mb, Mx, x, a0k):
        if cond: return (glaw(GK * Mb / x ** 2, a0k) + GK * Mx / x ** 2) * x ** 2 / GK
        return Mb + Mx
    def name(self): return f"{self.mode} K={self.K:.3g} Mc={self.Mc:.3g} R={self.Rf:.3f}"


BASE = {f: baselines(a) for f, a in A0K.items()}


def calib(ph, a0k, base):
    g5 = []
    for nm, Mb, Ro in G5SYS:
        rt = r_ta(Mb); c, mx, s = ph.host(expdisc(Mb, Ro), Mb, rt); g5.append(mx(Ro) / Mb)
    d = []; cache = {}
    for p in LE:
        Mb = p["Mb"] / MS; r = math.sqrt(G_SI * p["Mb"] / p["gbar"]) / KPC_M; key = round(math.log10(Mb), 6)
        if key not in cache: cache[key] = ph.host(expdisc(Mb, 3.2 * rd_of(Mb)), Mb, r_ta(Mb))
        c, mx, s = cache[key]; gX = G_SI * mx(r) * MS / (r * KPC_M) ** 2
        gp = glaw_SI(p["gbar"], a0k * ACC) + gX if c else p["gbar"] + G_SI * mx(r) * MS / (r * KPC_M) ** 2
        d.append(math.log10(p["gobs"] / gp))
    c2 = float(np.mean(d)) - base[0]
    kept = [v[2]["kept"] for v in cache.values() if v[2] is not None]
    rtf = [v[2]["R_tf"] / r_ta(10 ** k) for k, v in cache.items() if v[2] is not None]
    return dict(C1_max=max(g5), C1=bool(max(g5) <= 0.3), C2_shift=c2, C2=bool(abs(c2) <= 0.05), ok=bool(max(g5) <= 0.3 and abs(c2) <= 0.05),
                kids_kept_frac=[min(kept), max(kept)] if kept else None, kids_Rtf_over_rta=[min(rtf), max(rtf)] if rtf else None)


def find_Kmin(Mc, a0k, base):
    last = None; rows = []
    for K in KGRID[::-1]:
        c = calib(Phase(float(K), Mc), a0k, base); rows.append(dict(K=float(K), **c))
        if not c["ok"]: break
        last = float(K)
    return last, rows


def dsph_rows():
    out = []
    for row in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "mcconnachie2012_dsph.csv"))):
        if row["Name"] not in ("Carina", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans (I)", "Ursa Minor"): continue
        out.append((row["Name"], 2.0 * 10 ** (-0.4 * (float(row["VMag"]) - 4.83)), float(row["R2"]) / 1e3))
    return out
DSPH = dsph_rows()
GALS = Q8.load_sparc()
PARTS = {f: [dict(np.load(os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field", "parts", f, f"{i:03d}.npz"), allow_pickle=False)) for i in range(len(GALS))] for f in A0K}
def sparc_Mb(q): return (0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9
MC_PARTS = dict(sparc=max(sparc_Mb(q) for q in GALS), kids=max(p["Mb"] / MS for p in LE), dsph=max(m for _, m, _ in DSPH))
MC = max(MC_PARTS.values())


def grade(ph, a0k):
    o = {}; conv = []
    d = []; elph = []
    for e in EL:
        Mt = e["Mbar"](1e9); rt = r_ta(Mt); c, mx, s = ph.host(e["Mbar"], Mt, rt); elph.append(c)
        if s is not None: conv.append(s["conv"])
        for m in (2, 4, 8):
            x = m * e["Re"]; d.append(math.log10(e["Mtot"](x) / ph.Mpred(c, e["Mbar"](x), mx(x), x, a0k)))
    o["G3_D"] = float(np.mean(d)); o["G3"] = bool(abs(o["G3_D"]) <= 0.15); o["EL_condensed"] = int(sum(elph)); o["EL_n"] = len(elph)
    xd = []; xph = []
    for nm, pts in clusters.items():
        Ml, rl = pts[0]["Mb_last"]; host = profile_core([p_["r_kpc"] for p_ in pts], [p_["M_b"] for p_ in pts], Ml, rl)
        rt = r_ta(Ml); c, mx, s = ph.host(host, Ml, rt); xph.append(c)
        if s is not None: conv.append(s["conv"])
        for p_ in pts:
            x = p_["r_kpc"]; xd.append(math.log10(p_["M_obs"] / ph.Mpred(c, p_["M_b"], mx(x), x, a0k)))
    xd = np.array(xd); o["X_mean"] = float(xd.mean()); o["X_rms"] = float(np.sqrt((xd ** 2).mean()))
    o["G4"] = bool(abs(o["X_mean"]) <= 0.05 and o["X_rms"] <= 0.10); o["X_condensed"] = int(sum(xph))
    gm = {}; strict = {}; gph = 0
    for fst in (0.0, 1.0):
        v = []; npass = 0
        for gp in GR:
            Mbt = gp["g5"] * (1 + fst)
            host = profile_core([q_["r_kpc"] for q_ in gp["pts"]], [q_["M_gas"] * (1 + fst) for q_ in gp["pts"]], Mbt, gp["R5"])
            rt = r_ta(Mbt); c, mx, s = ph.host(host, Mbt, rt); gph += c; ok = True
            if s is not None: conv.append(s["conv"])
            for q_ in gp["pts"]:
                x = q_["r_kpc"]; Mb = q_["M_gas"] * (1 + fst)
                dl = math.log10(q_["M_obs"] / ph.Mpred(c, Mb, mx(x), x, a0k)); v.append(dl)
                ok &= abs(dl) <= 2 * q_["eM"] / (q_["M_obs"] * math.log(10))
            npass += ok
        gm[fst] = float(np.mean(v)); strict[f"fst{fst:g}"] = int(npass)
    lo, hi = sorted([gm[0.0], gm[1.0]])
    o["G_fst0"] = gm[0.0]; o["G_fst1"] = gm[1.0]; o["G5"] = bool(lo <= 0.05 and hi >= -0.05); o["G_strict"] = strict; o["G_condensed"] = int(gph)
    sh = []
    for nm, Ms, a in DSPH:
        host = (lambda M_, a_: (lambda x: M_ * x ** 3 / (x * x + a_ * a_) ** 1.5))(Ms, a)
        rt = r_ta(Ms); c, mx, s = ph.host(host, Ms, rt)
        if s is not None: conv.append(s["conv"])
        Mb = host(a); sh.append(math.log10(ph.Mpred(c, Mb, mx(a), a, a0k) / (glaw(GK * Mb / a ** 2, a0k) * a ** 2 / GK)))
    o["G7_median_shift"] = float(np.median(sh)); o["G7"] = bool(o["G7_median_shift"] <= 0.05)
    o["conv_frac"] = float(np.mean(conv)) if conv else 1.0
    return o


def g1(ph, foot):
    a0 = Q8.FOOT[foot]; lU = np.log(Q8.UPS); lN = np.log(Q8.NODES); rows = []; fr = []; nc = 0
    for q, pt in zip(GALS, PARTS[foot]):
        mt = q["meta"]; Mb = sparc_Mb(q); rd = mt["Rdisk"] if mt["Rdisk"] > 0 else rd_of(Mb); rt = r_ta(Mb)
        c, mx, s = ph.host(expdisc(Mb, 3.2 * rd), Mb, rt, n=500); nc += c
        Mx = np.array([mx(x) for x in q["R"]]); gX = GK * Mx / q["R"] ** 2 * ACC
        fr.append(float(Mx[-1] / Mb))
        GB = q["GB"]
        if c: lgl = np.log10(np.maximum(Q8.nu(GB / a0) * GB + gX[:, None], 1e-300))
        else: lgl = np.log10(np.maximum(GB + gX[:, None], 1e-300))
        Tf = np.array([np.interp(lU, lN, pt["T"][:, j]) for j in range(pt["T"].shape[1])])
        rows.append(Q8.fit_one(q, lgl + Tf))
    st = Q8.pooled(rows)
    return dict(rms=st["rms"], U_median=st["U_median"], G1=bool(Q8.line(st)), Mx_last_over_Mb_max=max(fr), Mx_last_over_Mb_median=float(np.median(fr)), SPARC_condensed=int(nc))


def full(ph, foot):
    a0k = A0K[foot]; o = grade(ph, a0k); o.update(calib(ph, a0k, BASE[foot])); o.update(g1(ph, foot))
    o["G2"] = o["C2"]; o["phase"] = ph.name()
    o["pass_static"] = bool(o["G1"] and o["G2"] and o["G3"] and o["G4"] and o["G5"] and o["G7"])
    return o


def line_of(f, o):
    P_ = lambda b: "P" if b else "F"
    return (f"[{f}] {o['phase']}: C1 {o['C1_max']:.3f} C2/G2 {o['C2_shift']:+.3f} | G1 rms {o['rms']:.4f}@{o['U_median']:.2f} {P_(o['G1'])} (cond {o['SPARC_condensed']}) | "
            f"G3 D {o['G3_D']:+.3f} {P_(o['G3'])} (cond {o['EL_condensed']}/{o['EL_n']}) | G4 X-COP {o['X_mean']:+.3f}/{o['X_rms']:.3f} {P_(o['G4'])} (cond {o['X_condensed']}) | "
            f"G5 groups [{o['G_fst1']:+.3f},{o['G_fst0']:+.3f}] {P_(o['G5'])} strict {o['G_strict']} (cond {o['G_condensed']}/40) | G7 {o['G7_median_shift']:+.4f} {P_(o['G7'])} | conv {o['conv_frac']:.2f}")


# ------------------------------------------------------------------ KA1: Lane-Emden n = 1/2
def ka1():
    def f(x, y): return [y[1], -max(y[0], 0.0) ** 0.5 - 2 * y[1] / x]
    ev = lambda x, y: y[0]; ev.terminal = True; ev.direction = -1
    x0 = 1e-6; s = solve_ivp(f, [x0, 10], [1 - x0 ** 2 / 6, -x0 / 3], events=ev, rtol=1e-11, atol=1e-13)
    xi1 = float(s.t_events[0][0]); om = float(-xi1 ** 2 * s.y_events[0][0][1])
    K = 0.03; M = 3e11
    a = (1.5 * K * M / (16 * math.pi ** 2 * GK * om)) ** 0.2; Rpred = xi1 * a; rhoc = M / (4 * math.pi * a ** 3 * om)
    sol = solve_tf(lambda x: 0.0, M, K, Rpred / 30.0, n=3000, rmin=1e-2, rout_fac=60.0)
    # central density from the solver
    rc = float(sol["rho"][0])
    return dict(xi1=xi1, omega1=om, R_pred=Rpred, R_solver=sol["R_tf"], rhoc_pred=rhoc, rhoc_solver=rc,
                ok=bool(abs(sol["R_tf"] / Rpred - 1) <= 0.01 and abs(rc / rhoc - 1) <= 0.01))


# ------------------------------------------------------------------ implied BK constants (reported only)
def bk_constants(K, Mc, a0_SI):
    hbarc = 1.97327e-7; eV = 1.602177e-19; c = 2.99792458e8; Msun_kpc3 = MS / KPC_M ** 3
    to_nat = lambda u_J: u_J / eV * hbarc ** 3                   # J/m^3 -> eV^4
    rho = 1.0; u = to_nat(rho * Msun_kpc3 * c ** 2); P = to_nat(K * rho ** 3 * Msun_kpc3 * 1e6)
    Lm3 = math.sqrt(u ** 3 / (12 * P))                           # Lambda m^3 in eV^4
    Vc = (GK * Mc * a0_SI / ACC) ** 0.25; rta = r_ta(Mc)
    rhoX = R * Mc / (4 / 3 * math.pi * rta ** 3)                 # Msun/kpc^3, mean sector density in r_ta
    m = (to_nat(rhoX * Msun_kpc3 * c ** 2) / (Vc * 1e3 / c) ** 3) ** 0.25
    Lam = Lm3 / m ** 3
    a0n = a0_SI / c * 6.582120e-16; Mpl = 2.435e27                # reduced Planck mass, eV
    alpha = (a0n * Mpl / Lam ** 2) ** (1 / 3)
    return dict(Lambda_m3_eV4=Lm3, V_c_kms=Vc, rhoX_Msun_kpc3=rhoX, m_eV=m, Lambda_eV=Lam, alpha=alpha,
                note="BK overlap m^4 = rho/v^3 (hbar = c = 1); a0 = alpha^3 Lambda^2 / M_Pl with reduced M_Pl; reported only")


if __name__ == "__main__":
    OUT = []
    def P(s=""): print(s, flush=True); OUT.append(str(s))
    P(f"QX28 ({'MUTATE' if MUT else 'main'}): two-phase superfluid cold dark energy sector (BK class). kappa = 1/2 FITTED; not theory closed. Criteria c5852ac12f.")
    P(f"KA0: scan hits {KA0['scan_hits']}; max rel residual of g_N = g^2/(g+a0) {KA0['max_rel_law_residual']:.2e}; a0 lib "
      f"{KA0['a0_lib_SI_canonical']:.5g} / {KA0['a0_lib_SI_alt']:.5g} m/s^2 -> PASS")
    P(f"R {R:.3f}; rho_sea {RHO_D0:.4g} Msun/kpc^3; plain-law bases (KiDS, EL): " + ", ".join(f"{f} {BASE[f][0]:+.4f} {BASE[f][1]:+.4f}" for f in A0K))
    P(f"M_c rule: max calibration M_b: SPARC {MC_PARTS['sparc']:.4g}, KiDS {MC_PARTS['kids']:.4g}, dSph {MC_PARTS['dsph']:.4g} -> M_c = {MC:.4g} Msun")
    P(f"  ellipticals M_b,tot {sorted(round(e['Mbar'](1e9)/1e11, 3) for e in EL)} e11; groups min {min(g['g5'] for g in GR):.3g}; X-COP min {min(p[0]['Mb_last'][0] for p in clusters.values()):.3g}")
    RES = dict(lane="QX28", criteria="c5852ac12f", mutate=MUT, note="kappa = 1/2 FITTED; not theory closed", KA0=KA0, M_c=MC, M_c_parts=MC_PARTS)
    if not MUT:
        k1 = ka1(); RES["KA1"] = k1
        P(f"KA1 Lane-Emden n=1/2: xi1 {k1['xi1']:.5f} omega1 {k1['omega1']:.5f}; R pred {k1['R_pred']:.2f} solver {k1['R_solver']:.2f} kpc; rho_c pred {k1['rhoc_pred']:.4g} solver {k1['rhoc_solver']:.4g} -> {'PASS' if k1['ok'] else 'FAIL'}")
        ok2 = abs(BASE["canonical"][1] - 0.210) <= 1e-3 and abs(BASE["alt"][1] - 0.189) <= 1e-3
        RES["KA2"] = dict(canonical=BASE["canonical"][1], alt=BASE["alt"][1], ok=bool(ok2))
        P(f"KA2 plain-law ellipticals D {BASE['canonical'][1]:+.4f} / {BASE['alt'][1]:+.4f} vs QX18 +0.210/+0.189 -> {'PASS' if ok2 else 'FAIL (reported)'}")
        RES["KA3_KA4"] = {}; RES["KA5"] = {}
        for f in A0K:
            z = full(Phase(1.0, MC, "cond", Rfac=0.0), f); RES["KA3_KA4"][f] = z
            ref3 = 0.4675 if f == "canonical" else 0.4345; ref4 = (0.0560, 0.58) if f == "canonical" else (0.0558, 0.52)
            P(f"KA3/KA4 [{f}] R=0: X-COP {z['X_mean']:+.4f} (ref {ref3:+.4f}) {'PASS' if abs(z['X_mean']-ref3) <= 2e-3 else 'FAIL'}; "
              f"SPARC exact rms {z['rms']:.4f}@{z['U_median']:.2f} (ref {ref4[0]}@{ref4[1]}) {'PASS' if abs(z['rms']-ref4[0]) <= 1e-4 and abs(z['U_median']-ref4[1]) < 0.005 else 'FAIL'}; G3 D {z['G3_D']:+.4f}")
            c = calib(Phase(1e4, MC), A0K[f], BASE[f]); RES["KA5"][f] = c
            P(f"KA5 [{f}] K 1e4: C2 {c['C2_shift']:+.4f} C1 {c['C1_max']:.4f} -> {'PASS' if abs(c['C2_shift']) <= 0.02 else 'FAIL'}")
        RES["per_foot"] = {}
        for f in A0K:
            Km, rows = find_Kmin(MC, A0K[f], BASE[f]); ent = dict(K_min=Km, scan=rows)
            if Km is None:
                P(f"[{f}] no K on the grid passes calibration"); RES["per_foot"][f] = ent; continue
            ph = Phase(Km, MC); o = full(ph, f); ent.update(o)
            # condensate geometry at the KiDS / G5 hosts
            geo = []
            for Mb in (1e9, 1e10, 1e11, MC):
                rt = r_ta(Mb); s = solve_tf(expdisc(Mb, 3.2 * rd_of(Mb)), R * Mb, Km, rt)
                geo.append(dict(Mb=Mb, r_ta=rt, R_tf=s["R_tf"], kept_in_rta=s["kept"], Mx_30kpc_over_Mb=Mat(s, 30.0, rt) / Mb, Mx_300kpc_over_Mb=Mat(s, 300.0, rt) / Mb))
            ent["geometry"] = geo; ent["bk_constants"] = bk_constants(Km, MC, FOOT_SI[f])
            # reported: ellipticals in the other phase
            ent["EL_other_phase_D"] = grade(Phase(Km, MC, "norm" if o["EL_condensed"] == len(EL) else "cond"), A0K[f])["G3_D"]
            RES["per_foot"][f] = ent
            P(f"[{f}] K_min {Km:.4g} (km/s)^2 kpc^6 Msun^-2; KiDS kept-in-r_ta {o['kids_kept_frac']}, R_tf/r_ta {o['kids_Rtf_over_rta']}")
            for gg in geo:
                P(f"   host M_b {gg['Mb']:.3g}: r_ta {gg['r_ta']:.0f} kpc, R_TF {gg['R_tf']:.0f} kpc, kept {gg['kept_in_rta']:.3f}, M_X(<30)/M_b {gg['Mx_30kpc_over_Mb']:.4f}, M_X(<300)/M_b {gg['Mx_300kpc_over_Mb']:.3f}")
            P("   " + line_of(f, o))
            P(f"   reported: ellipticals in the other phase D {ent['EL_other_phase_D']:+.3f}")
            P(f"   implied BK constants (reported only): {ent['bk_constants']}")
        # reported: M_c band with no group / X-COP phase change
        P(f"reported: any M_c in [{MC:.3g}, {min(g['g5'] for g in GR):.3g}) leaves every group (f_st 0) and X-COP host normal; the ellipticals' phase is the only galaxy-side change.")
    else:
        q = json.load(open(os.path.join(HERE, "qx28.json")))
        for lab, mode in (("M1", "cond"), ("M2", "norm")):
            RES[lab] = {}
            for f in A0K:
                Km = q["per_foot"][f]["K_min"]
                o = full(Phase(Km, MC, mode), f)
                bites = (not (o["G3"] and o["G4"] and o["G5"])) if lab == "M1" else (not (o["G1"] and o["C2"] and o["G7"]))
                o["bites"] = bool(bites); RES[lab][f] = o
                P(f"{lab} ({'always condensed' if mode == 'cond' else 'always normal'}) " + line_of(f, o) + f" -> {'BITES' if bites else 'DOES NOT BITE'}")
        RES["M3"] = {}
        for f in A0K:
            c = calib(Phase(1e-8, MC), A0K[f], BASE[f]); RES["M3"][f] = dict(c, bites=bool(not c["ok"]))
            P(f"M3 [{f}] K 1e-8: C1 {c['C1_max']:.3f} C2 {c['C2_shift']:+.3f} -> {'BITES' if not c['ok'] else 'DOES NOT BITE'}")
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
