#!/usr/bin/env python3
"""CQ7_lstar_dwarf_window: is v3s's fixed screening length window open once the smallest dwarfs are solved, not read?
Criteria FROZEN_CRITERIA.md (a199cb1eb0). OMP_NUM_THREADS=1 nice -n 10 python3 -I -B cq7.py [--mutate]
dSphs: D10's Solver2D (grad-div stiffened C4-literal form, v3s statics) in the host field; rotation curves: D10's iso_1d ODE
on the tabulated monopole g_N(r). MUTATE: L* = 0 in every solve (no screening).
kappa = 1/2 FITTED; not theory closed."""
import csv, glob, json, math, os, resource, sys, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad, solve_bvp
from scipy.interpolate import PchipInterpolator, CubicSpline
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22/D10_native_Lstar")); import d10_solver as S
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; FAILS = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), msg=msg)
    if not ok: FAILS.append(name)
G, MS, AU, PC, KPC = 6.6743e-11, 1.98892e30, 1.495978707e11, 3.0857e16, 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; M_MW = 7.0e10
LFLOOR = {"canonical": 21.68, "alt": 22.85}; LTOP = {"canonical": 27.0, "alt": 24.6}
LGRID = {f: [LFLOOR[f], 0.5 * (LFLOOR[f] + LTOP[f]), LTOP[f]] for f in A0}; LBESIDE = [40.0, 60.0, 90.0]
UPS = np.arange(1.0, 3.0001, 0.4); GR = S.Grid2D(nper=24, Nt=16)
P(f"CQ7 (criteria a199cb1eb0){'  [MUTATE: L* = 0 in every solve]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
eff = lambda L: 0.0 if MUT else L

# ---------------- K1: CQ1's UGC 4483 (KT19 / CQ1 loader) ----------------
tab = {}
for line in open(os.path.join(REPO, "real_research/data/SPARC_Lelli2016c.mrt")):
    p = line.split()
    if len(p) >= 18 and p[1].isdigit(): tab[p[0]] = dict(L=float(p[7]) * 1e9, Rd=float(p[11]), MHI=float(p[13]) * 1e9)
SP = []
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3 or nm not in tab: continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, j] for j in range(6)); Bg = Vg * np.abs(Vg); Bs = 0.5 * Vd * np.abs(Vd) + 0.7 * Vb * np.abs(Vb)
    q = (R > 0) & (Vo > 0) & (eV > 0) & (eV / np.maximum(Vo, 1e-9) < 0.1) & (Bg + Bs > 0)
    if q.sum() < 3: continue
    SP.append(dict(name=nm, Mb=0.5 * tab[nm]["L"] + 1.33 * tab[nm]["MHI"], Rd_pc=tab[nm]["Rd"] * 1e3, R=R[q] * KPC, gobs=(Vo[q] * 1e3) ** 2 / (R[q] * KPC), gbar=(Bg + Bs)[q] * 1e6 / (R[q] * KPC)))
cq1 = json.load(open(os.path.join(REPO, "cq_lanes_2026_11_04/CQ1_screening_window/cq1.json")))["G6"]["smallest"]
smin = min(SP, key=lambda g: g["Mb"]); e1 = 0.0
for f, a0 in A0.items():
    rM = math.sqrt(G * smin["Mb"] * MS / a0) / PC; e1 = max(e1, abs(rM / cq1[f]["rM_pc"] - 1), abs(smin["Mb"] / cq1[f]["Mb"] - 1))
    P(f"  [{f}] {len(SP)} SPARC galaxies; smallest {smin['name']} M_b {smin['Mb']:.4g}, r_M {rM:.2f} pc, 0.1 r_M {0.1 * rM:.2f} pc (CQ1 {cq1[f]['rM_pc']:.2f}, {cq1[f]['L_line_pc']:.2f})")
check("K1", e1 <= 1e-3 and smin["name"] == cq1["canonical"]["name"], f"CQ1's UGC 4483 numbers, max rel {e1:.2e} (line 1e-3)")

# ---------------- K2: C6's Sun (Route F, CQ2's copy of C6's kernel) ----------------
def chi_c6(kap, c, xe):
    m = (1 - c * c) / (1 + xe) + c * c / (1 + xe) ** 2
    return m / (1 - m + kap ** 2 * m / 2)
def routeF_radial(GM, L, xe, r, nc=48, kmul=400.0, nk=200000):
    rho = r / L; cg, cw = np.polynomial.legendre.leggauss(nc); K = kmul / rho
    lk = np.linspace(np.log(1e-6), np.log(K), nk); k = np.exp(lk)
    c0 = np.concatenate([0.5 * (chi_c6(kk[:, None], cg[None, :], xe) * cw).sum(1) for kk in np.array_split(k, 20)])
    z = k * rho; j1 = np.where(z < 1e-3, z / 3 - z ** 3 / 30, np.sin(z) / z ** 2 - np.cos(z) / z)
    head = np.trapz(k * k * j1 * c0, lk); a = K * rho
    t1 = quad(lambda zz: 1 / zz ** 3, a, np.inf, weight="sin", wvar=1.0)[0]; t2 = quad(lambda zz: 1 / zz ** 2, a, np.inf, weight="cos", wvar=1.0)[0]
    return 2 * GM / (np.pi * L ** 2) * (head + 2 * (t1 - t2))
c6 = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22/C6_literal_cassini/c6_literal_cassini_results.json")))["R3_wide_binary"]
d7b = json.load(open(os.path.join(REPO, "doors_push_2026_10_22/D7b_cassini_Q2/d7b_cassini_q2_results.json")))["grid"]
A0C6 = {"canonical": 9.36e-11, "alt": 1.13e-10}; GMS = 1.32712440018e20; s20 = 20e3 * AU; e2 = 0.0
for key, ref in c6.items():
    f, Lpc = key.split("|"); Lpc = float(Lpc)
    vals = [math.sqrt(1 + routeF_radial(1.5 * GMS, Lpc * PC, v["ge_total"] / A0C6[f], s20) / (1.5 * GMS / s20 ** 2)) - 1 for v in d7b[f]["none"].values()]
    e2 = max(e2, max(abs(a / b - 1) for a, b in zip(vals, ref["gamma_minus_1"])))
check("K2", e2 <= 1e-6, f"C6's 24 recorded Sun wide-binary gamma - 1 values (1.5 Msun, 20 kAU) reproduced, max rel {e2:.2e} (line 1e-6)")

# ---------------- K3: isolated 2D at L* = 0 vs the law ----------------
k3 = []
for y in (0.04, 3.0):
    sv = S.Solver2D(GR, y, 0.0, 0.0, isolated=True); sv.solve(); rf, gr = sv.field_monopole()
    _, va, _ = S.jeans(rf, gr, [1.0]); _, vb, _ = S.jeans(rf, S.law_v(S.plummer_gN(rf, y)), [1.0]); k3.append(abs(math.sqrt(va / vb) - 1))
check("K3", max(k3) <= 2e-3, f"isolated 2D L* = 0 global sigma vs the algebraic law, max rel {max(k3):.2e} (line 2e-3)")

# ---------------- dSphs ----------------
DW = []
for d in csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/mcconnachie2012_dsph.csv"))):
    if not d["e_sigma*"] or float(d["VMag"]) > -8 or d["Name"].startswith(("M32", "NGC", "Sagittarius")): continue
    DW.append(dict(name=d["Name"], sub=d["SubG"], D=float(d["D"]), L=10 ** (-0.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]), s=float(d["sigma*"]), e=float(d["e_sigma*"]), MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0))
assert len(DW) == 24, len(DW)
def dsph_sig(dw, a0, Lpc):
    a = dw["a"] * PC; iso = dw["sub"] != "MW"
    xe = 0.0 if iso else float(S.law_v(G * M_MW * MS / (dw["D"] * KPC) ** 2 / a0))
    out, U, nneg = [], None, 0
    for u in UPS:
        y = G * (u * dw["L"] + 1.33 * dw["MHI"]) * MS / (a * a * a0)
        sv = S.Solver2D(GR, y, xe, eff(Lpc) * PC / a, isolated=iso); U, res, it = sv.solve(U0=U); rf, gr = sv.field_monopole()
        _, vir, _ = S.jeans(rf, gr, [1.0]); out.append(math.sqrt(vir * a0 * a) / 1e3)
        D_, _, _ = sv.divp(U[:GR.n]); nneg = max(nneg, int(np.sum((D_ < 0) & (GR.r2d.ravel() < 10.0)))) if hasattr(GR, "r2d") else nneg
        if not (res < 1e-8): out[-1] = float("nan")
    return np.array(out), xe, nneg
def dsph_gate(foot, Lpc):
    a0 = A0[foot]; rows = []; n = 0
    for dw in DW:
        sg, xe, nneg = dsph_sig(dw, a0, Lpc)
        lu = np.log(UPS); fine = np.exp(np.linspace(lu[0], lu[-1], 201)); sf = CubicSpline(lu, sg)(np.log(fine))
        dmin = float(np.min(np.abs(sf - dw["s"]))); ok = bool(np.isfinite(sg).all() and dmin <= 2 * dw["e"]); n += ok
        rows.append(dict(name=dw["name"], a_pc=dw["a"], gate=bool(dw["a"] < 10 * Lpc), x_e=xe, sig_U1=float(sg[0]), sig_U3=float(sg[-1]), obs=dw["s"], err=dw["e"], dmin=dmin, passed=ok, neg_divp_cells=nneg))
    return dict(n_pass=n, ok=bool(n >= 15), rows=rows)

# ---------------- rotation curves ----------------
def rc_pred(R, gN, a0, Lpc):
    """g_pred at R (SI) on the tabulated monopole; L* = 0 -> the algebraic law."""
    x = gN / a0
    if eff(Lpc) <= 0: return a0 * S.law_v(x)
    rp = R / PC; M = np.maximum(x * rp ** 2, 1e-12); ip = PchipInterpolator(np.log(rp), np.log(M))
    r1, rl = rp[0], rp[-1]
    def gn(r):
        r = np.asarray(r); lr = np.log(r)
        m = np.where(r < r1, np.log(M[0]) + 3 * (lr - np.log(r1)), np.where(r > rl, np.log(M[-1]), ip(np.clip(lr, np.log(r1), np.log(rl)))))
        return np.exp(m) / r ** 2
    # AMENDMENT A1: finite-difference Newton on ln r (solve_bvp hit its node limit); same ODE, same boundary conditions
    l2 = 0.5 * eff(Lpc) ** 2; rin = min(r1 / 10, eff(Lpc) / 10); rout = 30 * rl
    N = 40000; xg = np.linspace(math.log(rin), math.log(rout), N); h = xg[1] - xg[0]; r = np.exp(xg); g_ = gn(r)
    v0 = S.law_v(g_); p = v0 / (1 + v0); c = l2 / r ** 2; st = 1
    from scipy.linalg import solve_banded
    for it in range(60):
        f = p * p / (1 - p); df = (2 * p - p * p) / (1 - p) ** 2
        F = np.empty(N); lo = np.zeros(N); di = np.zeros(N); up = np.zeros(N)
        F[1:-1] = c[1:-1] * ((p[2:] - 2 * p[1:-1] + p[:-2]) / h ** 2 + (p[2:] - p[:-2]) / (2 * h) - 2 * p[1:-1]) - f[1:-1] + g_[1:-1]
        di[1:-1] = c[1:-1] * (-2 / h ** 2 - 2) - df[1:-1]; up[1:-1] = c[1:-1] * (1 / h ** 2 + 1 / (2 * h)); lo[1:-1] = c[1:-1] * (1 / h ** 2 - 1 / (2 * h))
        F[0] = (p[1] - p[0]) / h - 0.5 * (p[0] + p[1]); di[0] = -1 / h - 0.5; up[0] = 1 / h - 0.5
        F[-1] = f[-1] - g_[-1]; di[-1] = df[-1]
        ab = np.zeros((3, N)); ab[0, 1:] = up[:-1]; ab[1] = di; ab[2, :-1] = lo[1:]
        dp = solve_banded((1, 1), ab, -F); al = 1.0
        while np.any(p + al * dp >= 1) or np.any(p + al * dp <= 0): al *= 0.5
        p = p + al * dp
        if np.max(np.abs(dp)) < 1e-12 * np.max(p): st = 0; break
    return a0 * (x + np.interp(np.log(rp), xg, p)), st
LT = []
DD = os.path.join(os.path.dirname(REPO), "_external_data", "little_things_oh2015")
def ltload(fn):
    out = {}
    for l in open(os.path.join(DD, fn)):
        p = l.split()
        if len(p) < 7 or p[1] != "Data": continue
        R0, V0, Rs, Vs, eVs = map(float, p[2:7]); out.setdefault(p[0], []).append((Rs * R0, Vs * V0, eVs * V0))
    return {k: np.array(sorted(v)) for k, v in out.items()}
if os.path.exists(os.path.join(DD, "rotdmbar.dat")):
    TOT, DMc = ltload("rotdmbar.dat"), ltload("rotdm.dat")
    for nm, t in TOT.items():
        if nm not in DMc: continue
        R, Vt = t[:, 0], t[:, 1]; Vd = np.interp(R, DMc[nm][:, 0], DMc[nm][:, 1], left=np.nan, right=np.nan); vb2 = Vt ** 2 - Vd ** 2
        m = np.isfinite(vb2) & (vb2 > 0) & (R > 0)
        if m.sum() < 3: continue
        Rm = R[m] * KPC; LT.append(dict(name="LT " + nm, R=Rm, gobs=(Vt[m] * 1e3) ** 2 / Rm, gbar=vb2[m] * 1e6 / Rm, Mb=vb2[m][-1] * 1e6 * Rm[-1] / G / MS, Rd_pc=np.inf))
P(f"  LITTLE THINGS galaxies loaded: {len(LT)}")
def rc_gate(foot, Lpc, gals):
    a0 = A0[foot]; rows = []; ok = True
    for g in gals:
        b = np.log10(g["gobs"] / rc_pred(g["R"], g["gbar"], a0, 0.0)); r_ = rc_pred(g["R"], g["gbar"], a0, Lpc)
        gp, st = r_ if isinstance(r_, tuple) else (r_, 0); s = np.log10(g["gobs"] / gp)
        drms = float(np.sqrt(np.mean(s ** 2)) - np.sqrt(np.mean(b ** 2))); dmed = float(np.median(s) - np.median(b)); dmax = float(np.max(np.abs(s - b)))
        lab = "FAILS" if (drms > 0.02 or abs(dmed) > 0.05 or st != 0) else "HURT" if drms > 0.005 else "SURVIVES"; ok &= lab != "FAILS"
        rows.append(dict(name=g["name"], Mb=g["Mb"], rM_pc=math.sqrt(G * g["Mb"] * MS / a0) / PC, d_rms=drms, d_med=dmed, max_shift_dex=dmax, bvp_status=st, label=lab))
    return dict(ok=bool(ok), rows=rows)
def rc_gals(foot, Lpc):
    a0 = A0[foot]; sel = []
    for g in SP + LT:
        rM = math.sqrt(G * g["Mb"] * MS / a0) / PC
        if min(rM, 1.68 * g["Rd_pc"]) < 10 * Lpc or g is smin: sel.append(g)
    return sel

# K4: 1D RC solve at small L* vs the law (UGC 4483)
k4 = 0.0
for f, a0 in A0.items():
    if MUT: break
    gp, st = rc_pred(smin["R"], smin["gbar"], a0, 0.3); k4 = max(k4, float(np.max(np.abs(gp / (a0 * S.law_v(smin["gbar"] / a0)) - 1))), 0.0 if st == 0 else 1.0)
check("K4", k4 <= 1e-3, f"UGC 4483 1D screened solve at L* = 0.3 pc vs the algebraic law, max rel {k4:.2e} (line 1e-3)")

# ---------------- grade ----------------
GRADE = {}
def evaluate(foot, L):
    t = time.time(); dg = dsph_gate(foot, L); rg = rc_gate(foot, L, rc_gals(foot, L))
    gd = [r for r in dg["rows"] if r["gate"]]
    P(f"  [{foot}] L* {L:.2f} pc: dSphs {dg['n_pass']}/24 ({'PASS' if dg['ok'] else 'FAIL'}; gate dwarfs r_h < 10 L*: " + ", ".join(f"{r['name']} {'p' if r['passed'] else 'F'}" for r in gd) + ")")
    P(f"      RC gate galaxies {len(rg['rows'])}: " + "; ".join(f"{r['name']} d_rms {r['d_rms']:+.4f} d_med {r['d_med']:+.4f} max {r['max_shift_dex']:.4f} {r['label']}" for r in rg["rows"]) + f"  ({time.time() - t:.0f} s)")
    return dict(L=L, dsph=dg, rc=rg, ok=bool(dg["ok"] and rg["ok"]))
for foot in A0:
    P(f"\n== [{foot}]"); base = evaluate(foot, 0.0) if True else None
    GRADE[foot] = dict(L0=base, graded=[evaluate(foot, L) for L in LGRID[foot]], beside=[])
    gr_ = GRADE[foot]["graded"]
    if all(e["ok"] for e in gr_):
        for L in LBESIDE:
            e = evaluate(foot, L); GRADE[foot]["beside"].append(e)
            if not e["ok"]: break
        hi = LTOP[foot]; lab = f"WINDOW OPEN [{LFLOOR[foot]:.2f}, {hi:.2f}] pc"
    elif not gr_[0]["ok"]: hi = None; lab = "WINDOW CLOSED"
    else:
        lo_, hi_ = max(e["L"] for e in gr_ if e["ok"]), min(e["L"] for e in gr_ if not e["ok"])
        while hi_ - lo_ > 0.1:
            m_ = 0.5 * (lo_ + hi_); e = evaluate(foot, m_)
            lo_, hi_ = (m_, hi_) if e["ok"] else (lo_, m_)
        hi = lo_; lab = f"WINDOW OPEN [{LFLOOR[foot]:.2f}, {hi:.2f}] pc"
    seq = gr_ + GRADE[foot]["beside"]; first = next((e for e in seq if not e["ok"]), None); bind = None
    if first:
        fd = [r["name"] for r in first["dsph"]["rows"] if not r["passed"] and r["name"] not in [q["name"] for q in base["dsph"]["rows"] if not q["passed"]]]
        fr = [r["name"] for r in first["rc"]["rows"] if r["label"] == "FAILS"]
        bind = dict(L=first["L"], dsph_count=first["dsph"]["n_pass"], newly_failing_dsph=fd, failing_rc=fr)
    GRADE[foot].update(label=lab, hi=hi, binding=bind)
    P(f"LABEL [{foot}] {lab}; binding {bind}")
RES["grade"] = GRADE

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
check("K5", rss < 1.0, f"peak RSS {rss:.2f} GB (line 1 GB)")
if MUT:
    z = max(abs(r["d_rms"]) for f in GRADE for e in GRADE[f]["graded"] for r in e["rc"]["rows"]) if GRADE else 0
    P(f"MUTATE: max |d_rms| {z:.2e}; dSph counts " + ", ".join(f"{f} {[e['dsph']['n_pass'] for e in GRADE[f]['graded']]} vs L*=0 {GRADE[f]['L0']['dsph']['n_pass']}" for f in GRADE))
P(f"\nfailed checks: {len(FAILS)} {FAILS}; wall {time.time() - T0:.0f} s; peak RSS {rss:.2f} GB")
RES.update(failed=FAILS, wall_s=time.time() - T0, peak_rss_gb=rss, note="kappa = 1/2 FITTED; not theory closed")
sfx = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"cq7{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"cq7{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or FAILS) else 0)
