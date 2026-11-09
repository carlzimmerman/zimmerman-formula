#!/usr/bin/env python3
"""EMV1 effective-medium validation (criteria f924165783). TEST lane, quarantined; adopts nothing; relabels nothing.
kappa = 1/2 FITTED; not theory closed. One thread.
Usage: OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 emv1.py [--mutate=mu1 | --mutate=flux]

Does SWT1's T2 statistic survive a direct nonlinear solve of one law-on bubble in a uniform external field?
The one-bubble solver is emv1_solver.py. SWT1's functions (radii, GSMF, alpha_law, compensated) are loaded read-only from
../SWT1_switch_theorems/swt1.py, the way swt1_extra.py loads them.
"""
import os, sys, json, math, time, warnings, resource
warnings.filterwarnings("ignore", message=".*encountered in matmul")   # spurious BLAS flags on this machine; the KAs check results
import numpy as np
if not hasattr(np, "trapz"): np.trapz = np.trapezoid

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from emv1_solver import Bubble, path, u_in

MUT = None
for _a in sys.argv[1:]:
    if _a.startswith("--mutate="): MUT = _a.split("=", 1)[1]
assert MUT in (None, "mu1", "flux"), MUT
TAG = "emv1" if MUT is None else "emv1_MUTATE_" + MUT
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()

# ------------------------------------------------------------------ SWT1's functions (read-only)
SWT1_DIR = os.path.join(REPO, "fable52_push", "SWT1_switch_theorems")
_src = open(os.path.join(SWT1_DIR, "swt1.py")).read(); _cut = _src.index("RES = dict(lane=")
NS = {"__file__": os.path.join(SWT1_DIR, "swt1.py"), "__name__": "swt1_lib"}
_argv = sys.argv; sys.argv = ["swt1.py"]; exec(compile(_src[:_cut], "swt1.py", "exec"), NS); sys.argv = _argv
G, MS, MPC, A0, LINE = NS["G"], NS["MS"], NS["MPC"], NS["A0"], NS["LINE"]
LG, LF, PD = NS["LG"], NS["LF"], NS["PD"]
Rms, alpha_law, compensated, radii_table = NS["Rms"], NS["alpha_law"], NS["compensated"], NS["radii_table"]
SWT1J = json.load(open(os.path.join(SWT1_DIR, "swt1.json")))
A_T2 = SWT1J["reported"]["kids_reach"]["filling_allowed_insulating"]          # 0.0230559
G_FLOOR = SWT1J["reported"]["kids_reach"]["gbar_floor_allowed"]                # 7.4625e-15
NVK = SWT1J["reported"]["kids_reach"]["KiDS_lowest_gbar"]["sum_nV"]
GK = SWT1J["reported"]["kids_reach"]["KiDS_lowest_gbar"]["gbar"]
Z = 1.0; AE = 1.0 / (1.0 + Z)
KIDS = (9.4, 10.45, 10.7, 10.9)
READ = ("L", "NC")
RAT = [10 ** (-2 + k / 4) for k in range(13)]                                 # g_ext / g_wall, 0.01 .. 10
GRID = dict(ds=0.06, Nmu=32); FINE = dict(ds=0.03, Nmu=64)

def mk(yw, grid=GRID, **kw):
    kw = dict(kw)
    if MUT == "mu1": kw["kmode"] = "mu1"
    if MUT == "flux": kw["flux_mutate"] = True
    return Bubble(yw, ds=grid["ds"], Nmu=grid["Nmu"], **kw)
def yw_of(Mb, R, a0): return G * Mb / (R * R * a0)
def alaw_dimless(yw, a0):
    R = MPC; return float(alpha_law(yw * R * R * a0 / G, R, a0)[0])
NONCONV = []
def run_path(b, es, label):
    out, x = path(b, es)
    for e, (at, ai, info) in out.items():
        if not info["converged"]: NONCONV.append(dict(where=label, e=e, info=info))
    return out, x

RES = dict(lane="EMV1", criteria="f924165783", tag=TAG, mutate=MUT, grid=GRID, fine_grid=FINE,
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, bracket={}, table={}, graded={}, reported={})
P(f"EMV1 {('MUTATE ' + MUT + ' ') if MUT else ''}run. Line {LINE}; SWT1 allowance {A_T2:.7f}; SWT1 reach floor g_bar {G_FLOOR:.4e}; "
  f"grid ds {GRID['ds']} x N_mu {GRID['Nmu']}; z {Z}")

# ------------------------------------------------------------------ the bracket (Section 3), read from the record
A0C = A0["canonical"]
P2J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "P2_spec_isolated_lensing", "p2_spec_isolated_lensing_results.json")))["ye_S3"]["canonical"]
BR = [("P2 c10 p16", P2J["c10"]["p16"] * A0C, 1.6182e-15),
      ("P2 lo10 median (no completeness)", P2J["lo10"]["median"] * A0C, 2.3975e-15),
      ("P2 c10 median (catalogue field)", P2J["c10"]["median"] * A0C, 6.1430e-15),
      ("P2 c20 median (to 20 Mpc)", P2J["c20"]["median"] * A0C, 9.9354e-15),
      ("P2 c10 p84", P2J["c10"]["p84"] * A0C, 1.9098e-14),
      ("QX7 noclu median e_N 0.0004", 0.0004 * 1.2e-10, 4.8e-14),
      ("S2 Chae noclu median", 10 ** -3.215 * 1.2e-10, 7.3145e-14),
      ("P2 bary median", P2J["bary"]["median"] * A0C, 1.2903e-13),
      ("QX7 PRIMARY maxclu median e_N 0.0033", 0.0033 * 1.2e-10, 3.96e-13),
      ("S2 Chae maxclu median", 10 ** -2.30 * 1.2e-10, 6.0142e-13),
      ("QX7 maxclu p84 e_N 0.0052", 0.0052 * 1.2e-10, 6.24e-13),
      ("P2 matter median", P2J["matter"]["median"] * A0C, 8.2116e-13),
      ("P2 matter p84", P2J["matter"]["p84"] * A0C, 2.5529e-12),
      ("QX7 ceiling x8 e_N 0.026", 0.026 * 1.2e-10, 3.12e-12)]
BR.sort(key=lambda t: t[1])
ka0b = max(abs(v / fz - 1) for _, v, fz in BR)
GB = [v for _, v, _ in BR]
RES["bracket"] = [dict(name=n, g_ext=v, frozen=fz) for n, v, fz in BR]
P("Bracket (SI, Newtonian, same on both footings): " + "; ".join(f"{n} {v:.4e}" for n, v, _ in BR))
P(f"KA0 bracket values against the frozen table: max rel {ka0b:.2e} (line 1e-4)")
EMAX_SCAN = 1.0
def scan_nodes(a0):
    etop = GB[-1] / a0
    return [etop * 10 ** (k / 8) for k in range(1, 40) if etop * 10 ** (k / 8) <= EMAX_SCAN * 1.0001]

# ------------------------------------------------------------------ KA0: SWT1's T2 reproduced, radii tables
def q_from_alpha(tab, al, z, qff):
    Vt = 4 * math.pi / 3 * (tab / MPC) ** 3 * (1 + z) ** 3
    Vf = 10 ** np.interp(LF, LG, np.log10(np.maximum(Vt, 1e-300)))
    af = np.interp(LF, LG, np.asarray(al, float))
    fV = float(np.trapz(PD * Vf, LF)); beta = float(np.trapz(PD * Vf * af, LF))
    b = beta if fV <= 0.30 else beta * 0.30 / fV
    qC = -3 * b / (1 + 2 * b)
    return dict(f_V=fV, beta=beta, alpha_vol=beta / fV, q_C=qC, q_tot=qC + abs(qff))

TAB, YW, AL, QFF, BASE = {}, {}, {}, {}, {}
ka0 = dict(allowance=abs(LINE / (1.5 + LINE) / A_T2 - 1), rows={})
for f, a0 in A0.items():
    for X in READ:
        tab = radii_table(X, a0, Z); TAB[(f, X)] = tab
        YW[(f, X)] = [yw_of(10 ** m * MS, R, a0) for m, R in zip(LG, tab)]
        AL[(f, X)] = [float(alpha_law(10 ** m * MS, R, a0)[0]) for m, R in zip(LG, tab)]
        d = compensated(tab, a0, Z); QFF[(f, X)] = d["q_ff"]
        mine = q_from_alpha(tab, AL[(f, X)], Z, d["q_ff"])
        ref = SWT1J["T2"][f][X]["1.0"]["q_tot"]
        BASE[(f, X)] = ref
        ka0["rows"][f"{f}_{X}"] = dict(q_tot_swt1_json=ref, q_tot_recomputed=d["q_tot"], q_tot_mine=mine["q_tot"],
                                       rel_vs_json=abs(d["q_tot"] / ref - 1), rel_mine=abs(mine["q_tot"] / d["q_tot"] - 1), f_V=mine["f_V"])
ka0_ok = ka0b < 1e-4 and ka0["allowance"] < 1e-6 and all(r["rel_vs_json"] < 1e-6 and r["rel_mine"] < 1e-9 for r in ka0["rows"].values())
RES["KA"]["KA0"] = dict(bracket_rel=ka0b, **ka0, pass_=bool(ka0_ok))
for k, r in ka0["rows"].items():
    P(f"KA0 {k}: SWT1 q_tot {r['q_tot_swt1_json']:.6f}, recomputed {r['q_tot_recomputed']:.6f} (rel {r['rel_vs_json']:.1e}), "
      f"own Maxwell-Garnett with alpha_law {r['q_tot_mine']:.6f} (rel {r['rel_mine']:.1e}); filling {r['f_V']:.4f}")
P(f"KA0 allowance LINE / (3/2 + LINE) vs SWT1 {ka0['allowance']:.1e} -> {'PASS' if ka0_ok else 'FAIL'}  ({time.time() - T0:.0f} s)")

# ------------------------------------------------------------------ KA2 linear homogeneous and coated spheres
def coated_exact(m1, m2, x3):
    num = (m2 - 1) * (m1 + 2 * m2) + x3 * (m1 - m2) * (1 + 2 * m2)
    den = (m2 + 2) * (m1 + 2 * m2) + 2 * x3 * (m2 - 1) * (m1 - m2)
    return num / den
ka2 = []
for m in (0.1, 0.5, 2.0):
    b = mk(0.0, kmode="const", ref="none", Kconst=m); r = b.solve(1e-2)
    ka2.append(dict(case=f"homogeneous mu {m}", alpha_tot=r[2], alpha_inc=r[3], exact=(m - 1) / (m + 2), err=max(abs(r[2] - (m - 1) / (m + 2)), abs(r[3] - (m - 1) / (m + 2)))))
for m1, m2, xa in ((1.0, 0.05, 0.5), (3.0, 0.2, 0.3), (0.1, 2.0, 0.7)):
    b = mk(0.0, kmode="coated", ref="none", coat=(m1, m2, xa)); r = b.solve(1e-2); ex = coated_exact(m1, m2, xa ** 3)
    ka2.append(dict(case=f"coated core {m1} shell {m2} a/R {xa}", alpha_tot=r[2], alpha_inc=r[3], exact=ex, err=max(abs(r[2] - ex), abs(r[3] - ex))))
ka2_ok = all(r["err"] < 2e-3 for r in ka2)
RES["KA"]["KA2"] = dict(rows=ka2, pass_=bool(ka2_ok))
for r in ka2: P(f"KA2 {r['case']}: alpha {r['alpha_tot']:.6f} / inc {r['alpha_inc']:.6f}, exact {r['exact']:.6f}, err {r['err']:.1e}")
P(f"KA2 -> {'PASS' if ka2_ok else 'FAIL'}")

# ------------------------------------------------------------------ KA3 no galaxy, nonlinear
def x_uniform(e): return ((3 * e - 2) + math.sqrt((2 - 3 * e) ** 2 + 36 * e)) / 6
ka3 = []
for e in (1e-3, 1e-2, 0.1, 1.0):
    b = mk(0.0, ref="none"); out, x = run_path(b, [e * 1e-3, e], f"KA3 e {e}")
    at, ai, info = out[e]; xx = x_uniform(e)
    grf, Gf = b.fields(x); dev = float(np.max(np.abs(Gf / Gf.mean() - 1)))
    resid_eq = abs(Gf.mean() * (Gf.mean() / (1 + Gf.mean()) + 2) / (3 * e) - 1)
    ka3.append(dict(e=e, x=xx, field_mean=float(Gf.mean()), uniform_dev=dev, matching_rel=resid_eq, alpha_tot=at, alpha_tot_exact=-1 / (2 + 3 * xx),
                    alpha_inc=ai, alpha_inc_exact=-1 / (2 + 6 * xx + 3 * xx * xx), err=max(abs(at + 1 / (2 + 3 * xx)), abs(ai + 1 / (2 + 6 * xx + 3 * xx * xx)))))
ka3_ok = all(r["uniform_dev"] < 0.01 and r["err"] < 2e-3 for r in ka3)
RES["KA"]["KA3"] = dict(rows=ka3, pass_=bool(ka3_ok))
for r in ka3:
    P(f"KA3 e {r['e']}: interior field {r['field_mean']:.6f} (closed {r['x']:.6f}, uniform to {r['uniform_dev']:.1e}); alpha_tot {r['alpha_tot']:.6f} "
      f"(closed {r['alpha_tot_exact']:.6f}); alpha_inc {r['alpha_inc']:.6f} (closed {r['alpha_inc_exact']:.6f}); err {r['err']:.1e}")
P(f"KA3 -> {'PASS' if ka3_ok else 'FAIL'}")

# ------------------------------------------------------------------ KA4 no external field, Newton reference
def ka4_run():
    Mb = 10 ** 10.45 * MS; a0 = A0["canonical"]; R = Rms("L", Mb, a0, AE); yw = yw_of(Mb, R, a0)
    b = mk(yw, ref="newton"); x, dx, at, ai, info = b.solve(0.0)
    if not info["converged"]: NONCONV.append(dict(where="KA4", e=0.0, info=info))
    grf, Gf = b.fields(x); meff = (b.rf ** 2)[:, None] * grf / yw
    nu = lambda y: 0.5 + math.sqrt(0.25 + 1 / y)
    rows = []
    for rr in (0.01, 0.1, 0.5, 0.9):
        k = int(np.argmin(np.abs(b.rf - rr))); m = float(meff[k].mean()); n = nu(yw / b.rf[k] ** 2)
        rows.append(dict(r=float(b.rf[k]), Meff_over_Mb=m, nu=n, rel=abs(m / n - 1)))
    lw = b.legendre_wall(x)
    ext_mono = 1 + b.eta * lw[0] / yw
    return dict(y_w=yw, rows=rows, exterior_Meff_over_Mb=ext_mono, max_l_ge_1_over_yw=float(np.max(np.abs(lw[1:])) / yw), iters=info["iters"])
ka4 = ka4_run()
ka4_ok = all(r["rel"] < 1e-3 for r in ka4["rows"]) and abs(ka4["exterior_Meff_over_Mb"] - 1) < 1e-10 and ka4["max_l_ge_1_over_yw"] < 1e-10
RES["KA"]["KA4"] = dict(**ka4, pass_=bool(ka4_ok))
P("KA4 (Newton reference, no external field, log M_b 10.45 at its L radius): " + "; ".join(
    f"r {r['r']:.3f}: r^2 g / G M_b {r['Meff_over_Mb']:.6f} vs nu {r['nu']:.6f} (rel {r['rel']:.1e})" for r in ka4["rows"])
  + f"; exterior M_eff / M_b {ka4['exterior_Meff_over_Mb']:.12f}; max |psi_l>=1| / y_w {ka4['max_l_ge_1_over_yw']:.1e} -> {'PASS' if ka4_ok else 'FAIL'}")

# ------------------------------------------------------------------ KA1 and the table: four KiDS masses at the L and NC radii
P(""); P("Table: alpha against g_ext / g_wall (z 1 radii), and KA1 at 0.01")
TABLE = {}; ka1 = []; ALL_ALPHA = []
for f, a0 in A0.items():
    TABLE[f] = {}
    for X in READ:
        for lm in KIDS:
            Mb = 10 ** lm * MS; R = Rms(X, Mb, a0, AE); yw = yw_of(Mb, R, a0)
            b = mk(yw); gw = b.gwall; es = [r * gw for r in RAT]
            out, x = run_path(b, es, f"table {f} {X} {lm}")
            al = alaw_dimless(yw, a0)
            rows = []
            for r_, e in zip(RAT, es):
                at, ai, info = out[e]; rows.append(dict(ratio=r_, g_ext=e * a0, alpha_tot=at, alpha_inc=ai, alpha_iso=(ai + 2 * at) / 3))
                ALL_ALPHA += [at, ai]
            TABLE[f][f"{X}_{lm}"] = dict(R_Mpc=R / MPC, y_w=yw, g_wall=gw * a0, alpha_law=al, rows=rows)
            rel = abs(rows[0]["alpha_inc"] / al - 1); ka1.append(dict(footing=f, reading=X, logMb=lm, alpha_law=al, alpha_inc=rows[0]["alpha_inc"], rel=rel))
            P(f"[{f}] {X} log M_b {lm}: R_w {R / MPC:.3f} Mpc, g_wall {gw * a0:.3e} m/s^2, alpha_law {al:.5f} | g_ext/g_wall: "
              + "  ".join(f"{rw['ratio']:.3g}: {rw['alpha_tot']:.4f}/{rw['alpha_inc']:.4f}" for rw in rows[::2]))
    # the allowance's bubble at y_A (KA1 there too)
    yA = G_FLOOR / a0; b = mk(yA); gw = b.gwall
    out, x = run_path(b, [0.01 * gw], f"KA1 y_A {f}")
    al = alaw_dimless(yA, a0); ai = out[0.01 * gw][1]
    ka1.append(dict(footing=f, reading="allowance wall", logMb=None, alpha_law=al, alpha_inc=ai, rel=abs(ai / al - 1)))
RES["table"] = TABLE
ka1_ok = {f: all(r["rel"] < 0.01 for r in ka1 if r["footing"] == f) for f in A0}
RES["KA"]["KA1"] = dict(rows=ka1, pass_=ka1_ok)
P("KA1 alpha_inc at g_ext/g_wall 0.01 vs alpha_law: max rel " + ", ".join(
    f"{f} {max(r['rel'] for r in ka1 if r['footing'] == f):.1e}" for f in A0) + " -> " + ", ".join(f"{f} {'PASS' if v else 'FAIL'}" for f, v in ka1_ok.items()))
P(f"   ({time.time() - T0:.0f} s)")

# ------------------------------------------------------------------ graded: allowance and q_tot of L and NC over the bracket
P(""); P("Graded: the allowance and the readings' q_tot with alpha_inc, over the bracket")
GRADED = {}
for f, a0 in A0.items():
    eb = [g / a0 for g in GB]; es = eb + ([] if MUT else scan_nodes(a0))
    # allowance
    yA = G_FLOOR / a0; b = mk(yA); outA, _ = run_path(b, es, f"allowance {f}")
    for e in es: ALL_ALPHA += [outA[e][0], outA[e][1]]
    # readings
    outX = {}
    for X in READ:
        outX[X] = []
        for k, yw in enumerate(YW[(f, X)]):
            o, _ = run_path(mk(yw), es, f"graded {f} {X} {LG[k]}"); outX[X].append(o)
            for e in es: ALL_ALPHA += [o[e][0], o[e][1]]
    nodes = []
    for e in es:
        aA_inc, aA_tot = outA[e][1], outA[e][0]
        A = LINE / (-aA_inc * (3 + 2 * LINE)); A_iso = LINE / (-((aA_inc + 2 * aA_tot) / 3) * (3 + 2 * LINE))
        row = dict(g_ext=e * a0, e=e, in_bracket=bool(any(abs(e / x - 1) < 1e-12 for x in eb)),
                   allowance=dict(alpha_inc=aA_inc, alpha_tot=aA_tot, A=A, move=A / A_T2 - 1, A_iso=A_iso, move_iso=A_iso / A_T2 - 1))
        for X in READ:
            ai = [outX[X][k][e][1] for k in range(len(LG))]; at = [outX[X][k][e][0] for k in range(len(LG))]
            q = q_from_alpha(TAB[(f, X)], ai, Z, QFF[(f, X)])
            qi = q_from_alpha(TAB[(f, X)], [(a + 2 * t) / 3 for a, t in zip(ai, at)], Z, QFF[(f, X)])
            row[X] = dict(alpha_inc_9_10p5_12=[ai[0], float(np.interp(10.5, LG, ai)), ai[-1]], alpha_vol=q["alpha_vol"], q_tot=q["q_tot"],
                          move=q["q_tot"] / BASE[(f, X)] - 1, side=("above" if q["q_tot"] > LINE else "at or below"),
                          q_tot_iso=qi["q_tot"], move_iso=qi["q_tot"] / BASE[(f, X)] - 1)
        nodes.append(row)
    GRADED[f] = nodes
    for row, (nm, g, _) in zip([r for r in nodes if r["in_bracket"]], BR):
        P(f"[{f}] {nm:<40s} g_ext {g:.3e} (e {row['e']:.2e}): allowance alpha_inc {row['allowance']['alpha_inc']:.4f} -> A {row['allowance']['A']:.5f} "
          f"(move {row['allowance']['move']:+.3f}); L q {row['L']['q_tot']:.4f} (move {row['L']['move']:+.3f}, {row['L']['side']}); "
          f"NC q {row['NC']['q_tot']:.5f} (move {row['NC']['move']:+.3f}, {row['NC']['side']})")
    P(f"   ({time.time() - T0:.0f} s)")
RES["graded"] = GRADED

# g_20: field at which each move first reaches 20 % (reported)
def g20(nodes, getter):
    xs = [(r["g_ext"], abs(getter(r))) for r in nodes]; xs.sort()
    for (g1, m1), (g2, m2) in zip(xs[:-1], xs[1:]):
        if m1 < 0.2 <= m2:
            t = (0.2 - m1) / (m2 - m1); return float(math.exp(math.log(g1) + t * (math.log(g2) - math.log(g1))))
    return None if xs[0][1] < 0.2 else xs[0][0]
if not MUT:
    G20 = {f: dict(allowance=g20(GRADED[f], lambda r: r["allowance"]["move"]), L=g20(GRADED[f], lambda r: r["L"]["move"]),
                   NC=g20(GRADED[f], lambda r: r["NC"]["move"]), allowance_iso=g20(GRADED[f], lambda r: r["allowance"]["move_iso"]),
                   L_iso=g20(GRADED[f], lambda r: r["L"]["move_iso"])) for f in A0}
    RES["reported"]["g_20"] = G20
    for f in A0:
        P(f"reported [{f}] field at which the move reaches 20 %: " + ", ".join(f"{k} {('%.3e' % v) if v else '> a0'}" for k, v in G20[f].items()))

# ------------------------------------------------------------------ labels
def label(f):
    ka_ok = RES["KA"]["KA0"]["pass_"] and RES["KA"]["KA2"]["pass_"] and RES["KA"]["KA3"]["pass_"] and RES["KA"]["KA4"]["pass_"] and RES["KA"]["KA1"]["pass_"][f]
    for k in ("KA5", "KA6", "KA7"):
        if k in RES["KA"]: ka_ok = ka_ok and RES["KA"][k]["pass_"][f] if isinstance(RES["KA"][k]["pass_"], dict) else ka_ok and RES["KA"][k]["pass_"]
    br = [r for r in GRADED[f] if r["in_bracket"]]
    mA = max(abs(r["allowance"]["move"]) for r in br); mL = max(abs(r["L"]["move"]) for r in br); mN = max(abs(r["NC"]["move"]) for r in br)
    sideL = all(r["L"]["q_tot"] > LINE for r in br); sideN = all(r["NC"]["q_tot"] <= LINE for r in br)
    top = br[-1]
    d = dict(max_move_allowance=mA, max_move_L=mL, max_move_NC=mN, L_stays_above=sideL, NC_stays_below=sideN,
             allowance_at_top=top["allowance"]["A"], q_L_at_top=top["L"]["q_tot"], q_NC_at_top=top["NC"]["q_tot"], known_answers_pass=bool(ka_ok))
    if not ka_ok: d["label"] = "NO VERDICT (a known answer failed)"
    elif max(mA, mL, mN) < 0.20 and sideL and sideN: d["label"] = "T2 HOLDS"
    else:
        ch = [n for n, ok in (("L", sideL), ("NC", sideN)) if not ok]
        d["label"] = f"T2 MOVES (new allowance at the top node {top['allowance']['A']:.4f}; readings changing side: {', '.join(ch) if ch else 'none'})"
    return d

# ------------------------------------------------------------------ KA5-KA7 (main run only), reported extras
if not MUT:
    P(""); P("KA5 resolution (grid doubled in both directions)")
    ka5 = []
    a0 = A0["canonical"]
    for X in READ:
        Mb = 10 ** 10.45 * MS; R = Rms(X, Mb, a0, AE); yw = yw_of(Mb, R, a0)
        bc, bf = mk(yw), mk(yw, grid=FINE); gw = bc.gwall; es = [0.01 * gw, gw, 10 * gw]
        oc, _ = run_path(bc, es, f"KA5 coarse {X}"); of, _ = run_path(bf, es, f"KA5 fine {X}")
        for e in es: ka5.append(dict(footing="canonical", case=f"{X} 10.45 ratio {e / gw:.2g}", coarse=oc[e][1], fine=of[e][1], diff=abs(oc[e][1] - of[e][1])))
    for f, a0 in A0.items():
        yA = G_FLOOR / a0; e = GB[-1] / a0
        oc, _ = run_path(mk(yA), [e], f"KA5 coarse y_A {f}"); of, _ = run_path(mk(yA, grid=FINE), [e], f"KA5 fine y_A {f}")
        ka5.append(dict(footing=f, case="allowance wall, top node", coarse=oc[e][1], fine=of[e][1], diff=abs(oc[e][1] - of[e][1])))
    for r in ka5: P(f"KA5 [{r['footing']}] {r['case']}: alpha_inc {r['coarse']:.6f} vs {r['fine']:.6f}, diff {r['diff']:.1e}")
    ka5_ok = all(r["diff"] < 2e-3 for r in ka5)
    RES["KA"]["KA5"] = dict(rows=ka5, pass_=bool(ka5_ok)); P(f"KA5 -> {'PASS' if ka5_ok else 'FAIL'}")

    ka6 = []
    a0 = A0["canonical"]; Mb = 10 ** 10.45 * MS; R = Rms("L", Mb, a0, AE); yw = yw_of(Mb, R, a0)
    for rr in (0.1, 1.0, 10.0):
        b = mk(yw); e = rr * b.gwall; out, x = run_path(b, [e], f"KA6 {rr}")
        dl = 0.01
        xp = b.solve(e * (1 + dl), x)[0]; xm = b.solve(e * (1 - dl), x)[0]
        p_p = float(b.legendre_wall(xp)[1]) + e * (1 + dl); p_m = float(b.legendre_wall(xm)[1]) + e * (1 - dl)
        fd = (p_p - p_m) / (2 * e * dl)
        ka6.append(dict(ratio=rr, tangent=out[e][1], central_difference=fd, diff=abs(out[e][1] - fd)))
    for r in ka6: P(f"KA6 ratio {r['ratio']}: alpha_inc tangent {r['tangent']:.6f}, central difference of p {r['central_difference']:.6f}, diff {r['diff']:.1e}")
    ka6_ok = all(r["diff"] < 1e-3 for r in ka6); RES["KA"]["KA6"] = dict(rows=ka6, pass_=bool(ka6_ok)); P(f"KA6 -> {'PASS' if ka6_ok else 'FAIL'}")

    b1 = mk(yw); b2 = mk(yw, eps_fac=1e-5); e = 10 * b1.gwall
    o1, _ = run_path(b1, [e], "KA7 eps"); o2, _ = run_path(b2, [e], "KA7 eps x10")
    ka7 = dict(alpha_inc=o1[e][1], alpha_inc_eps10=o2[e][1], diff=abs(o1[e][1] - o2[e][1]))
    ka7_ok = ka7["diff"] < 1e-4; RES["KA"]["KA7"] = dict(**ka7, pass_=bool(ka7_ok))
    P(f"KA7 regulariser x10 at g_ext/g_wall 10: alpha_inc {ka7['alpha_inc']:.7f} vs {ka7['alpha_inc_eps10']:.7f}, diff {ka7['diff']:.1e} -> {'PASS' if ka7_ok else 'FAIL'}")

    # null point (reported): the +z axis, log M_b 10.45, L, canonical
    nulls = []
    for rr in (0.3, 1.0, 3.0, 10.0):
        b = mk(yw); e = rr * b.gwall; out, x = run_path(b, [e], f"null {rr}")
        grf, Gf = b.fields(x); j = int(np.argmax(b.mu)); col = Gf[:, j]; k = int(np.argmin(col))
        nulls.append(dict(ratio=rr, r_min_over_Rw=float(b.rf[k]), min_field_over_gwall=float(col[k] / b.gwall), at_wall=bool(k == len(col) - 1)))
    RES["reported"]["null_point_10p45_L_canonical"] = nulls
    P("reported null point on the +z axis (log M_b 10.45, L, canonical): " + "; ".join(
        f"ratio {n['ratio']}: min |g| {n['min_field_over_gwall']:.3f} g_wall at r {n['r_min_over_Rw']:.3f} R_w" for n in nulls))

    # self-consistent reach (reported)
    scr = {}
    for f, a0 in A0.items():
        scr[f] = []
        for nm, g, _ in [BR[2], BR[8], BR[-1]]:
            yA = G_FLOOR / a0; hist = []
            for it in range(5):
                b = mk(yA); out, _ = run_path(b, [g / a0], f"reach {f} {nm} {it}")
                A = LINE / (-out[g / a0][1] * (3 + 2 * LINE)); xr = (A / NVK) ** (1 / 3); gfl = GK / xr ** 2
                hist.append(dict(y_A=yA, alpha_inc=out[g / a0][1], A=A, reach_fraction=xr, g_floor=gfl)); yA = gfl / a0
            scr[f].append(dict(node=nm, g_ext=g, iterations=hist))
            h = hist[-1]
            P(f"reported [{f}] self-consistent reach at {nm} ({g:.2e}): allowance {h['A']:.5f}, reach {h['reach_fraction']:.3f} of R_K, "
              f"g_bar floor {h['g_floor']:.3e} m/s^2 (SWT1: 0.430, {G_FLOOR:.3e})")
    RES["reported"]["self_consistent_reach"] = scr

RES["non_converged"] = NONCONV
P(""); P(f"Newton solves not converged: {len(NONCONV)}")
LAB = {f: label(f) for f in A0}
RES["labels"] = LAB
if MUT:
    mx = float(np.nanmax(np.abs(ALL_ALPHA))) if ALL_ALPHA else float("nan")
    if MUT == "mu1":
        bites = (mx < 2e-3) and not all(RES["KA"]["KA1"]["pass_"].values())
        RES["MUTATE"] = dict(arm="M-MU1", max_abs_alpha=mx, KA1=RES["KA"]["KA1"]["pass_"], bites=bool(bites))
        P(f"MUTATE M-MU1 (mu = 1 inside): max |alpha| over every galaxy solve {mx:.2e} (must be < 2e-3); KA1 {RES['KA']['KA1']['pass_']} -> {'BITES' if bites else 'NO BITE'}")
    else:
        bites = (not all(RES["KA"]["KA1"]["pass_"].values())) and (not RES["KA"]["KA2"]["pass_"])
        RES["MUTATE"] = dict(arm="M-FLUX", KA1=RES["KA"]["KA1"]["pass_"], KA2=RES["KA"]["KA2"]["pass_"], bites=bool(bites))
        P(f"MUTATE M-FLUX (dPhi/dr continuous instead of mu dPhi/dr): KA1 {RES['KA']['KA1']['pass_']}, KA2 {RES['KA']['KA2']['pass_']} -> {'BITES' if bites else 'NO BITE'}")
for f in A0:
    d = LAB[f]
    P(f"LABEL [{f}]: {d['label']} | max move: allowance {d['max_move_allowance']:.3f}, L {d['max_move_L']:.3f}, NC {d['max_move_NC']:.3f}; "
      f"L above the line throughout {d['L_stays_above']}, NC at or below {d['NC_stays_below']}; at the top node A {d['allowance_at_top']:.5f}, "
      f"q_L {d['q_L_at_top']:.4f}, q_NC {d['q_NC_at_top']:.5f}")
RES["runtime_s"] = time.time() - T0
RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
P(f"runtime {RES['runtime_s']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
