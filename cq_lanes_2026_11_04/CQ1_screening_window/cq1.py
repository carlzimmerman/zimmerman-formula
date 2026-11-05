#!/usr/bin/env python3
"""CQ1_screening_window: can ONE new screening constant pass the Solar System and leave galaxies unscreened?
Criteria FROZEN_CRITERIA.md (98d0cbbefe). OMP_NUM_THREADS=1 nice -n 10 python3 -I -B cq1.py [--mutate].
Families: (i) tidal threshold T*, (ii) Vainshtein-type r_V = (r_s l^2)^(1/3), (iii) fixed screening length L*.
The Cassini solver is CW1's Solver, read from the byte copy cw1_copy.py, plus one option (rscr: F = 0 at x < rscr).
kappa = 1/2 FITTED; not theory closed."""
import csv, difflib, glob, hashlib, json, math, os, resource, sys, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf
from scipy.interpolate import CubicSpline
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; FAILS = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), msg=msg)
    if not ok: FAILS.append(name)
G, MS, AU, PC, KPC, CL = 6.6743e-11, 1.98892e30, 1.495978707e11, 3.0857e16, 3.0857e19, 2.99792458e8
KAP = 0.5; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; GCAS, GPRI, CEIL = 2.32e-10, 1.9e-10, 5.2e-27
R0 = 8.122 * KPC; RHOB = {"B2b_7.3e10 (graded)": 0.1599, "McMillan": 0.1071}; MPC3 = MS / PC ** 3
LD10 = {"canonical": 21.68, "alt": 22.85}; UPS_GC, MB_D10, M_MW, UPS_DW = 1.6, 6e10, 7.0e10, 3.0; H2PC = 90.0; FLINE = 0.1
P(f"CQ1 (criteria 98d0cbbefe){'  [MUTATE: nu = 1]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")

# ---------------- CW1's code, read from the byte copy ----------------
ORIG = os.path.join(REPO, "cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4/cw1.py"); COPY = os.path.join(HERE, "cw1_copy.py")
sha_o, sha_c = (hashlib.sha256(open(p_, "rb").read()).hexdigest() for p_ in (ORIG, COPY)); SRC = open(COPY).read()
NU_SRC = SRC[SRC.index("if MUT:\n    nu = lambda"):SRC.index("# ---------------- the solver ----------------")]
SOL_SRC = SRC[SRC.index("def legendre(L, mu):"):SRC.index("def interp2(")]
PL_SRC = SRC[SRC.index('PL = json.load(open(os.path.join(RB, "RQ3_acceptance_v2'):SRC.index("KS = list(range(")]
ANCHOR = "        Fr = (nf - 1) * gfr - (nue - 1) * eta * M; Ft = -(nf - nue) * eta * ST * np.ones_like(X)\n"
ADD = "        if getattr(s, 'rscr', 0.0) > 0: Fr = np.where(X < s.rscr, 0.0, Fr); Ft = np.where(X < s.rscr, 0.0, Ft)   # CQ1's one option\n"
PAT_SRC = SOL_SRC.replace(ANCHOR, ANCHOR + ADD)
nd = [l_ for l_ in difflib.ndiff(SOL_SRC.splitlines(), PAT_SRC.splitlines()) if l_[:2] in ("+ ", "- ")]
check("K0", sha_o == sha_c and SOL_SRC.count(ANCHOR) == 1 and nd == ["+ " + ADD.rstrip("\n")], f"copy SHA-256 {sha_c[:16]}... equals CW1's ({sha_o == sha_c}); patch adds {len(nd)} line(s)")
def build(src):
    ns = dict(np=np, math=math, brentq=brentq, erf=erf, CubicSpline=CubicSpline, MUT=MUT, json=json, os=os, RB=RB, AU=AU)
    exec(compile(NU_SRC, "cw1_copy.py:nu", "exec"), ns); exec(compile(src, "cw1_copy.py:Solver", "exec"), ns); exec(compile(PL_SRC, "cw1_copy.py:planets", "exec"), ns); return ns
NS, NS0 = build(PAT_SRC), build(SOL_SRC); eta_newton, nu, planets = NS["eta_newton"], NS["nu"], NS["planets"]
class Screened(NS["Solver"]):
    def __init__(s, eta, form="PQ", rscr=0.0, **k): s.rscr = rscr; super().__init__(eta, form, **k)
def qcurve(sv):
    """q at every node k as the screened solver gives it (F = 0 at nodes < k): CW1's C2 = 0.6 trapz(d_2/x, u) with the zeroed rows."""
    f = (sv.a[:, 2] - 2 * sv.b[:, 2]) / sv.x; seg = 0.5 * sv.du * (f[:-1] + f[1:]); tail = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    c2 = 0.6 * (tail + 0.5 * sv.du * f); c2[0] = 0.6 * tail[0]; return 2 * np.abs(c2)

# ---------------- K1, K2: known answers ----------------
P("\n== Known answers (CW1)")
k3 = json.load(open(os.path.join(REPO, "cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4/cw1.json")))["K3"]; e1 = 0.0; e2 = 0.0; PQ0 = {}
for foot, a0 in A0.items():
    rM = math.sqrt(G * MS / a0); qp = CEIL / (1.5 * a0 / rM); eta = eta_newton(GCAS, a0)
    for f in ("HALF", "LOC1"):
        xq = Screened(eta, f).q() / qp; ref = k3[f"{foot}|{f}"]["x_ceiling"]; e1 = max(e1, abs(xq / ref - 1)); P(f"  [{foot}] {f}: {xq:.10g} x ceiling vs cw1.json {ref:.10g}")
    qa, qb = Screened(eta, "PQ").q(), NS0["Solver"](eta, "PQ").q(); e2 = max(e2, abs(qa / qb - 1) if qb > 0 else (0.0 if qa == qb else 1.0)); PQ0[foot] = qa / qp
    P(f"  [{foot}] plain QUMOND (PQ) Cassini: patched copy {qa / qp:.6g} x, CW1's unpatched Solver {qb / qp:.6g} x ceiling (AX1's QUMOND range 1.69-5.18 x, comparison only)")
check("K1", e1 <= 1e-6, f"copy at rscr = 0 vs cw1.json K3 (HALF, LOC1, both footings), max rel {e1:.2e} (line 1e-6)")
check("K2", e2 <= 1e-12, f"patched copy vs CW1's unpatched Solver, PQ, max rel {e2:.2e} (line 1e-12)"); RES["PQ_plain_x_ceiling"] = PQ0

# ---------------- G1 Cassini, G2 planets ----------------
P("\n== G1 Cassini: smallest screening radius with Q2 <= ceiling (eta from 2.32e-10 inverted)")
CAS = {}; e3 = 0.0; e4 = 0.0
for foot, a0 in A0.items():
    rM = math.sqrt(G * MS / a0); qp = CEIL / (1.5 * a0 / rM); eta = eta_newton(GCAS, a0); sv = Screened(eta, "PQ"); x = sv.x; qk = qcurve(sv)
    e3 = max(e3, abs(qk[0] / sv.q() - 1) if sv.q() > 0 else 0.0)
    for xt in np.geomspace(0.02, 2.0, 8):
        k = int(np.argmin(np.abs(x - xt))); qd = Screened(eta, "PQ", rscr=x[k]).q(); e3 = max(e3, abs(qd - qk[k]) / max(qd, 1e-300) if qd > 1e-12 * max(qk[0], 1e-300) else abs(qd - qk[k]) / max(qk[0], 1e-300))
    ok = qk <= qp; bad = np.where(~ok)[0]; kmin = int(bad.max() + 1) if bad.size else 0; kfirst = int(np.argmax(ok)); xs = float(x[min(kmin, x.size - 1)])
    qd_at, qd_before = Screened(eta, "PQ", rscr=xs).q() / qp, (Screened(eta, "PQ", rscr=float(x[kmin - 1])).q() / qp if kmin > 0 else float("nan"))
    hi = Screened(eta, "PQ", per_dec=400, L=96, nmu=128); qh = qcurve(hi); bh = np.where(qh > qp)[0]; xsh = float(hi.x[int(bh.max() + 1)]) if bh.size else float(hi.x[0])
    e4 = max(e4, abs(xsh / xs - 1)); prof = {f"{v:g}": float(qk[int(np.argmin(np.abs(x - v)))] / qp) for v in (0.01, 0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0)}
    pz = planets(Screened(eta, "PQ", rscr=xs), a0); pw = max(pz.values()); scan = []
    for rau in np.geomspace(2.0, 60.0, 31):
        z = planets(Screened(eta, "PQ", rscr=rau * AU / rM), a0); scan.append((float(rau), float(max(z.values()))))
    badp = [r_ for r_, z_ in scan if z_ > 2]; cand = [r_ for r_, z_ in scan if z_ <= 2 and not any(b_ > r_ for b_ in badp)]; rpl = min(cand) if cand else float("nan")
    rs = xs * rM; CAS[foot] = dict(r_M_AU=rM / AU, q_plain_x=float(qk[0] / qp), x_s_min=xs, x_first_ok=float(x[kfirst]), contiguous=bool(kfirst == kmin), r_s_AU=rs / AU,
        direct_at=qd_at, direct_node_below=qd_before, x_s_min_hires=xsh, profile_x_ceiling=prof, planets_at_xs=pz, planets_worst=pw, planet_scan=scan, r_planets_AU=rpl,
        T_sun_at_rs=2 * G * MS / rs ** 3, T_sun_at_planets=2 * G * MS / (rpl * AU) ** 3, l_min_kpc=CL / math.sqrt(2 * G * MS / rs ** 3) / KPC)
    P(f"  [{foot}] r_M {rM / AU:.0f} AU; plain {qk[0] / qp:.4g} x ceiling; q / ceiling at x_s = " + ", ".join(f"{k_} {v:.3g}" for k_, v in prof.items()))
    P(f"  [{foot}] x_s,min {xs:.4f} r_M = {rs / AU:.0f} AU (direct {qd_at:.4f} x; node below {qd_before:.4f} x; first passing node {x[kfirst]:.4f}, contiguous {kfirst == kmin}); hi-res {xsh:.4f}")
    P(f"  [{foot}] planets at x_s,min: worst Z {pw:.3g}; smallest passing r_s {rpl:.3g} AU; Sun's tide at r_s 2GM/r_s^3 = {2 * G * MS / rs ** 3:.4g} s^-2")
check("K3", e3 <= 1e-9, f"direct screened solves at 8 radii vs the plain solve's tail, max rel {e3:.2e} (line 1e-9)")
check("K4", e4 <= 0.03, f"x_s,min at per_dec 400, L 96, n_mu 128 vs default, max rel {e4:.2e} (line 3 %)"); RES["G1_G2"] = CAS

# ---------------- G3 globulars, G4 dwarfs, G5 MW, G6 SPARC ----------------
P("\n== G3 outer globulars (D10's clusters; M = 1.6 L_V, Plummer a = r_h,l, host 6e10 Msun)")
GC = json.load(open(os.path.join(REPO, "doors_push_2026_10_22/D10_native_Lstar/d10_native_lstar_results.json")))["clusters"]; GCR = {}
for nm, g in GC.items():
    M = UPS_GC * g["LV"] * MS; a = g["rhl"] * PC; host = 2 * G * MB_D10 * MS / (g["RGC"] * KPC) ** 3; GM3 = G * M / a ** 3
    GCR[nm] = dict(M=M / MS, a_pc=g["rhl"], T_a=GM3 / 2 ** 1.5 + host, T_0=GM3 + host, V_a=2 * GM3 / 2 ** 1.5, V_0=2 * GM3, host=host, rM_pc={f: math.sqrt(G * M / a0) / PC for f, a0 in A0.items()})
    P(f"  {nm:9s} M {M / MS:.3g} Msun, a {g['rhl']:.2f} pc, r_M {GCR[nm]['rM_pc']['canonical']:.2f}/{GCR[nm]['rM_pc']['alt']:.2f} pc; T(a) {GCR[nm]['T_a']:.3g}, T(0) {GCR[nm]['T_0']:.3g}; 2GM(<a)/a^3 {GCR[nm]['V_a']:.3g}, centre {GCR[nm]['V_0']:.3g}; host {host:.2g} s^-2")
P("\n== G4 dwarfs (CZ5's selection, Plummer a = r_h, M = 3 L_V + 1.33 M_HI; Upsilon 2 reported)")
DW = []
for d in csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/mcconnachie2012_dsph.csv"))):
    if not d["e_sigma*"] or float(d["VMag"]) > -8 or d["Name"].startswith(("M32", "NGC", "Sagittarius")): continue
    L = 10 ** (-0.4 * (float(d["VMag"]) - 4.83)); MHI = float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0; a = float(d["R2"]) * PC; host = 2 * G * M_MW * MS / (float(d["D"]) * KPC) ** 3 if d["SubG"] == "MW" else 0.0
    row = dict(name=d["Name"], a_pc=float(d["R2"]), host=host)
    for u in (3.0, 2.0): M = (u * L + 1.33 * MHI) * MS; row[f"T_a_U{u:g}"] = G * M / (2 ** 1.5 * a ** 3) + host; row[f"V_a_U{u:g}"] = 2 * G * M / (2 ** 1.5 * a ** 3)
    DW.append(row)
assert len(DW) == 24, len(DW)
for k_ in ("T_a_U3", "V_a_U3", "T_a_U2", "V_a_U2"):
    w = max(DW, key=lambda r_: r_[k_]); P(f"  max {k_}: {w[k_]:.4g} s^-2 ({w['name']}, a {w['a_pc']:.0f} pc)")
wa = min(DW, key=lambda r_: r_["a_pc"]); P(f"  smallest a: {wa['a_pc']:.0f} pc ({wa['name']}); n = {len(DW)}")
P("\n== G5 MW midplane at R0 = 8.122 kpc")
MW = {}
for foot, a0 in A0.items():
    gN = eta_newton(GPRI, a0) * a0
    MW[foot] = dict(T_rho={k_: 4 * math.pi * G * v * MPC3 for k_, v in RHOB.items()}, V_gN=2 * gN / R0, V_Mtot=2 * G * M_MW * MS / R0 ** 3, gN=gN)
    P(f"  [{foot}] 4 pi G rho_b: " + ", ".join(f"{k_} {v:.4g}" for k_, v in MW[foot]["T_rho"].items()) + f"; 2 g_N/R0 {2 * gN / R0:.4g} (g_N {gN:.4g}); 2GM_tot/R0^3 {MW[foot]['V_Mtot']:.4g} s^-2")
P("\n== G6 SPARC (KT19's loader and sample, M_b = 0.5 L + 1.33 M_HI)")
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
    SP.append(dict(name=nm, Mb=0.5 * tab[nm]["L"] + 1.33 * tab[nm]["MHI"]))
smin = min(SP, key=lambda g_: g_["Mb"]); SPR = {}
for foot, a0 in A0.items():
    rM = math.sqrt(G * smin["Mb"] * MS / a0); SPR[foot] = dict(name=smin["name"], Mb=smin["Mb"], rM_pc=rM / PC, T_line=2 * G * smin["Mb"] * MS / (FLINE * rM) ** 3, T_loose=2 * a0 / rM, L_line_pc=FLINE * rM / PC, L_loose_pc=rM / PC)
    P(f"  [{foot}] {len(SP)} galaxies; smallest M_b {smin['Mb']:.3g} Msun ({smin['name']}), r_M {rM / PC:.0f} pc; r_screen <= 0.1 r_M needs T >= {SPR[foot]['T_line']:.4g}, L* <= {FLINE * rM / PC:.1f} pc (loose r_M: {2 * a0 / rM:.3g}, {rM / PC:.0f} pc)")
RES.update(G3=GCR, G4=DW, G5=MW, G6=dict(n=len(SP), smallest=SPR))

# ---------------- windows ----------------
P("\n== Windows (lo = largest lower bound, hi = smallest upper bound)")
def win(lo, hi):
    L_ = max(lo, key=lambda t: t[1]); H_ = min(hi, key=lambda t: t[1]); return dict(lo=L_, hi=H_, open=bool(L_[1] < H_[1]), lows=lo, highs=hi)
WIN = {}
for foot, a0 in A0.items():
    c = CAS[foot]; GrL = a0 ** 2 / (KAP ** 2 * CL ** 2); Tdw = max(r_["T_a_U3"] for r_ in DW); Vdw = max(r_["V_a_U3"] for r_ in DW)
    fam = {}
    for F_, key, dk, mwv, glob_a, glob_0 in (("i_tidal", "T*", Tdw, max(MW[foot]["T_rho"].values()), "T_a", "T_0"), ("ii_vainshtein", "T_V = c^2/l^2", Vdw, MW[foot]["V_gN"], "V_a", "V_0")):
        lo = [("G4 dwarfs unscreened", dk), ("G5 MW midplane unscreened", mwv), ("G6 SPARC r_screen <= 0.1 r_M", SPR[foot]["T_line"])]
        hi = [("G1 Cassini", c["T_sun_at_rs"]), ("G2 planets", c["T_sun_at_planets"])] + [(f"G3 {n_} screened at r_h", GCR[n_][glob_a]) for n_ in ("Pal 4", "Pal 14")]
        fam[F_] = dict(unit="s^-2", var=key, full=win(lo, hi), no_G3=win(lo, hi[:2]), G3_centre=win(lo, hi[:2] + [(f"G3 {n_} screened at centre", GCR[n_][glob_0]) for n_ in ("Pal 4", "Pal 14")]),
                       SPARC_loose=win([t for t in lo if not t[0].startswith("G6")] + [("G6 SPARC r_screen <= r_M", SPR[foot]["T_loose"])], hi))
    lo3 = [("G1 Cassini", c["r_s_AU"] * AU / PC), ("G2 planets", c["r_planets_AU"] * AU / PC), ("G3 D10 floor", LD10[foot])]
    hi3 = [("G4 dwarfs a_min", wa["a_pc"]), ("G5 MW H2 layer", H2PC), ("G6 SPARC 0.1 r_M", SPR[foot]["L_line_pc"])]
    fam["iii_length"] = dict(unit="pc", var="L*", full=win(lo3, hi3), no_G3=win(lo3[:2], hi3), SPARC_loose=win(lo3, hi3[:2] + [("G6 SPARC r_M", SPR[foot]["L_loose_pc"])]))
    # vacuum combinations: every s^-2 one is N G rho_L, every length N c^2/a0 (tie a0 = kappa c sqrt(G rho_L)); natural N in [1e-3, 1e3]
    vacT, vacL = (1e-3 * GrL, 1e3 * GrL), (1e-3 * CL ** 2 / a0 / PC, 1e3 * CL ** 2 / a0 / PC)
    for F_, w_ in fam.items():
        for v_ in ("full", "no_G3", "G3_centre", "SPARC_loose"):
            if v_ not in w_: continue
            W = w_[v_]; lo_, hi_ = W["lo"][1], W["hi"][1]
            if F_ == "iii_length": W["vacuum_inside"] = bool(W["open"] and vacL[1] >= lo_ and vacL[0] <= hi_)
            else: W["vacuum_inside"] = bool(W["open"] and vacT[1] >= lo_ and vacT[0] <= hi_)
            if F_ == "ii_vainshtein" and W["open"]: W["l_kpc"] = [CL / math.sqrt(hi_) / KPC, CL / math.sqrt(lo_) / KPC]
        W = w_["full"]; lab = (f"WINDOW [{W['lo'][1]:.3g}, {W['hi'][1]:.3g}] {w_['unit']}" if W["open"] else f"NO WINDOW (binding: {W['lo'][0]} {W['lo'][1]:.3g} > {W['hi'][0]} {W['hi'][1]:.3g} {w_['unit']})")
        w_["label"] = lab; P(f"  [{foot}] {F_} ({w_['var']}): {lab}")
        for v_ in ("no_G3", "G3_centre", "SPARC_loose"):
            if v_ in w_: V = w_[v_]; P(f"      {v_}: {'open' if V['open'] else 'closed'} [{V['lo'][0]} {V['lo'][1]:.3g}, {V['hi'][0]} {V['hi'][1]:.3g}]" + (f", l {V['l_kpc'][0]:.3g}-{V['l_kpc'][1]:.3g} kpc" if "l_kpc" in V else "") + f"; vacuum inside {V['vacuum_inside']}")
        P(f"      vacuum inside the full window: {W['vacuum_inside']} (vacuum band {'%.2g-%.2g pc' % vacL if F_ == 'iii_length' else '%.2g-%.2g s^-2' % vacT})")
    # G7 wide binaries, report only
    wb = {}
    for F_ in ("i_tidal", "ii_vainshtein"):
        Ts = {"Cassini end": c["T_sun_at_rs"]}; V = fam[F_]["no_G3"]
        if V["open"]: Ts["no-G3 window low end"] = V["lo"][1]
        wb[F_] = {k_: {f"M{m}": (2 * G * m * MS / T) ** (1 / 3) / AU / 1e3 for m in (1.0, 2.0)} for k_, T in Ts.items()}
    wb["iii_length"] = {"D10 floor": {"M1.0": LD10[foot] * PC / AU / 1e3, "M2.0": LD10[foot] * PC / AU / 1e3}}
    for F_, d_ in wb.items():
        for k_, r_ in d_.items():
            m_ = min(r_.values()); r_["label"] = "SCREENS" if m_ >= 30 else "PARTLY" if max(r_.values()) >= 1 else "DOES NOT"
            P(f"  [{foot}] G7 wide binaries, {F_} at {k_}: r_screen {r_['M1.0']:.3g} / {r_['M2.0']:.3g} kAU (1 / 2 Msun) -> {r_['label']}")
    fam["G7_wide_binaries"] = wb; WIN[foot] = fam
RES["windows"] = WIN

# ---------------- Part A ----------------
P("\n== Part A: s^-2 quantities from {c, G, rho_L, a0}")
P("  [M] fixes G and rho_L as G rho_L; the s^-2 monomials are (G rho_L)^p (a0/c)^(2-2p) x numbers. With rho_L = a0^2/(kappa^2 c^2 G) each is kappa^(2-2p) G rho_L.")
PA = {}
for foot, a0 in A0.items():
    GrL = a0 ** 2 / (KAP ** 2 * CL ** 2)
    q_ = {"G rho_L": GrL, "(a0/c)^2": (a0 / CL) ** 2, "a0 sqrt(G rho_L)/c": a0 * math.sqrt(GrL) / CL, "(4 pi/3) G rho_L": 4 * math.pi / 3 * GrL, "4 pi G rho_L": 4 * math.pi * GrL,
          "8 pi G rho_L = Lambda c^2": 8 * math.pi * GrL, "(8 pi/3) G rho_L": 8 * math.pi / 3 * GrL, "(2 pi a0/c)^2": (2 * math.pi * a0 / CL) ** 2, "32 pi^2 G rho_L": 32 * math.pi ** 2 * GrL, "1e3 G rho_L (band top)": 1e3 * GrL}
    sad = {}
    for lab_, gobs in (("2.32e-10", GCAS), ("1.9e-10", GPRI)):
        gNe = eta_newton(gobs, a0) * a0; rs_ = math.sqrt(G * MS / gNe); sad[lab_] = dict(gN_e=gNe, r_sad_AU=rs_ / AU, T_sad=2 * G * MS / rs_ ** 3)
    Tmw = max(MW[foot]["T_rho"].values()); Tout = a0 / (10 * KPC); Tsad = min(v["T_sad"] for v in sad.values()); top = max(q_.values())
    lab = "VACUUM SCALE IN GAP" if top >= Tout else "NOT IN GAP"
    PA[foot] = dict(quantities=q_, rho_L=GrL / G, saddle=sad, T_MW=Tmw, T_outskirts=Tout, label=lab, hand_estimate_verified=bool(0.5 <= GrL / 4e-37 <= 2),
                    N_needed=dict(outskirts=Tout / GrL, MW=Tmw / GrL, sun_saddle=Tsad / GrL), lengths_pc=dict(c2_over_a0=CL ** 2 / a0 / PC, c_over_sqrtGrho=CL / math.sqrt(GrL) / PC))
    P(f"  [{foot}] " + "; ".join(f"{k_} {v:.3g}" for k_, v in q_.items()) + " s^-2")
    P(f"  [{foot}] rho_L {GrL / G:.4g} kg/m^3; Sun's saddle " + "; ".join(f"g_e {k_}: r {v['r_sad_AU']:.0f} AU, 2GM/r^3 {v['T_sad']:.3g}" for k_, v in sad.items()) + f"; MW 4 pi G rho_b {Tmw:.3g}; a0/10 kpc {Tout:.3g} s^-2")
    P(f"  [{foot}] N needed to reach: outskirts {Tout / GrL:.3g}, MW midplane {Tmw / GrL:.3g}, Sun's saddle {Tsad / GrL:.3g}; G rho_L / 4e-37 = {GrL / 4e-37:.3f} -> hand estimate {'VERIFIED' if PA[foot]['hand_estimate_verified'] else 'NOT VERIFIED'}; {lab}")
    P(f"  [{foot}] vacuum lengths: c^2/a0 {CL ** 2 / a0 / PC:.3g} pc, c/sqrt(G rho_L) {CL / math.sqrt(GrL) / PC:.3g} pc (all are c^2/a0 x numbers)")
RES["partA"] = PA

# ---------------- finish ----------------
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
check("K5", rss < 1.0, f"peak RSS {rss:.2f} GB (line 1 GB)")
P(f"\nfailed checks: {len(FAILS)} {FAILS}; wall {time.time() - T0:.0f} s; peak RSS {rss:.2f} GB")
RES["failed"] = FAILS; RES["wall_s"] = time.time() - T0; RES["peak_rss_gb"] = rss; RES["copy_sha256"] = sha_c; RES["note"] = "kappa = 1/2 FITTED; not theory closed"
sfx = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"cq1{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"cq1{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or FAILS) else 0)
