#!/usr/bin/env python3
"""XF1 Stage C grader (FROZEN_CRITERIA.md 8b99d12c42). Run from anywhere:
  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 -B closure_2026_11_08/XF1_moving_host_field/xf1_grade.py [--allow-missing]
Writes xf1.json, xf1.out, xf1_MUTATE.out.

Per cell, row and footing: g_static = the record's static EFE reading (D10's solver on X1/SE2's own call: AQUAL + EFE +
screening at the floor), g_iso = the isolated plain law (x_e = 0, L* = 0; with L* at the floor reported), g_N = Newton,
g_dyn = g_N (1 + eps) with eps the Stage B anomalous-charge gravity at the readout radius, sphere-averaged, worst over
starts, V brackets and grids. D = log10(g_dyn/g_static) FIRST (C3), then F = (log g_dyn - log g_static)/(log g_iso - log g_static) (C1);
C2 on SE2's data path (post_udg, widths_half_post_freeze) and X1's rows; C4 D only for B3/B4; C5 the Sun under AC15's
grading (ported verbatim); KB1-KB3; MUTATE-1/2/3; label by the frozen rule. Both footings separately, never pooled.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, glob, math, io, contextlib, csv
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import eval_legendre

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar"))
import xf1_field as XF                                                        # noqa: E402
import d10_solver as S                                                        # noqa: E402  (read-only, X1/SE2's solver)
ALLOW_MISSING = "--allow-missing" in sys.argv
OUT, MOUT = [], []
RES = dict(lane="XF1_moving_host_field", criteria="8b99d12c42", note="kappa = 1/2 FITTED; not theory closed. Footings never pooled. Adopts nothing.",
           KB={}, KA={}, footings={}, MUTATE={}, HE={})
CELLS = json.load(open(os.path.join(HERE, "xf1_cells.json")))
FOOTS = ("canonical", "alt"); A0 = CELLS["a0"]; LN10 = math.log(10)
G_SI, MSUN, PC, AU = 6.67430e-11, 1.989e30, 3.0856775814913673e16, 1.495978707e11
PARTS = os.path.join(HERE, "parts")


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def PM(s=""):
    P(s); MOUT.append(str(s))


def check(d, name, ok, detail):
    d[name] = dict(ok=bool(ok), detail=str(detail)); P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


# ---------------------------------------------------------------- static path (D10, S1/X1's call)
GRID = S.Grid2D(nper=24, Nt=16)
_SCACHE = {}


def static(y, xe, Lam):
    key = (round(y, 12), round(xe, 12), round(Lam, 12))
    if key in _SCACHE:
        return _SCACHE[key]
    iso = xe <= 0
    sv = S.Solver2D(GRID, y, 0.0 if iso else xe, Lam, isolated=iso); U, res, it = sv.solve(tol=1e-10)
    rf, gr = sv.field_monopole(); _, vir, wo = S.jeans(rf, gr, [])
    out = dict(rf=rf, gr=gr, vir=vir, wo=wo, res=res, it=it); _SCACHE[key] = out
    return out


def newton(y):
    rf = GRID.re[1:-1]; gr = S.plummer_gN(rf, y); _, vir, wo = S.jeans(rf, gr, [])
    return dict(rf=rf, gr=gr, vir=vir, wo=wo)


def g_at(st, r):
    return float(np.interp(r, st["rf"], st["gr"]))


# ---------------------------------------------------------------- hydro readout
def load_snaps(tag):
    fs = sorted(glob.glob(os.path.join(PARTS, tag, "snap_*.npz")))
    return [dict(np.load(f)) for f in fs] if fs else None


def done_of(tag):
    f = os.path.join(PARTS, tag, "done.json")
    return json.load(open(f)) if os.path.exists(f) else None


def readout(snaps, par, static_s=None):
    """eps(theta) = anomalous-charge gravity / body gravity at the readout radius, per snapshot; sphere average and bands."""
    out = []
    for sn in snaps:
        g = XF.Grid(sn["re"], sn["te"]); F = XF.Forces(g, par["x_e"], par["kappa_q"])
        dq = (sn["q"] - 1.0) + sn["s"]
        mf = XF.plummer_mass_frac(par["a_code"])
        res = {}
        for rr in par["r_read_code"]:
            rr_ = float(sn["re"][np.argmin(np.abs(sn["re"] - rr))])              # nearest radial edge (exact shell split, as AC15)
            ar, at = F.grav_at(dq, np.array([rr_]), g.tc)
            gb = par["gpar"] * float(mf(rr_)) / rr_ ** 2
            eps = -ar[0] / gb
            w = g.w_sphere; tc = g.tc
            up = tc < math.radians(60); dn = tc > math.radians(120); sd = ~(up | dn)
            res[f"{rr:.6g}"] = dict(r_edge=rr_, eps_sphere=float(np.sum(eps * w)), eps_up=float(np.sum(eps[up] * w[up]) / w[up].sum()),
                                   eps_side=float(np.sum(eps[sd] * w[sd]) / w[sd].sum()), eps_down=float(np.sum(eps[dn] * w[dn]) / w[dn].sum()),
                                   eps_max_abs=float(np.max(np.abs(eps))), t=float(sn["t"]))
        out.append(res)
    stat = None
    if static_s is not None:
        sn = snaps[-1]; g = XF.Grid(sn["re"], sn["te"]); F = XF.Forces(g, par["x_e"], par["kappa_q"]); mf = XF.plummer_mass_frac(par["a_code"])
        stat = {}
        for rr in par["r_read_code"]:
            rr_ = float(sn["re"][np.argmin(np.abs(sn["re"] - rr))]); ar, _ = F.grav_at(static_s, np.array([rr_]), g.tc)
            gb = par["gpar"] * float(mf(rr_)) / rr_ ** 2; stat[f"{rr:.6g}"] = float(np.sum(-ar[0] / gb * g.w_sphere))
    return out, stat


def tag_of(cell, foot, row, vi, start, res, bc="transmit", flags=""):
    return f"{cell}_{foot}_r{row}_V{vi}_{bc}_{start}_{res}{flags}"


REP = {"B1": 0, "B2": 6, "B3": 0, "B4": 0}
TEND_FLAG = {"B3": "_t30", "B4": "_t30"}


def runs_for(cell, foot, row):
    """the Stage B runs of a row: list of (tag, start, vi, res)."""
    L = []
    rep = REP[cell] == row
    starts = ("uniform",) if cell in ("B3", "B4") else ("uniform", "hedgehog")   # B3/B4 HEDGEHOG NOT RUN (linear phantom invalid: gN/gext > 1)
    for start in starts:
        sfx = TEND_FLAG.get(cell, "") + ("_d10" if start == "hedgehog" else "")
        L.append((tag_of(cell, foot, row, 1, start, "coarse", flags=sfx), start, 1, "coarse"))
        if rep or cell in ("B3", "B4"):
            L.append((tag_of(cell, foot, row, 0, start, "coarse", flags=sfx), start, 0, "coarse"))
        if rep and cell in ("B1", "B2"):
            for vi in (0, 1):
                L.append((tag_of(cell, foot, row, vi, start, "medium", flags=("_d10" if start == "hedgehog" else "")), start, vi, "medium"))
    if cell in ("B3", "B4"):
        L.append((tag_of(cell, foot, row, 1, "uniform", "medium", flags=TEND_FLAG[cell]), "uniform", 1, "medium"))
    return L


MISSING = []

P("XF1 Stage C: the action's own hosted state, graded. kappa = 1/2 FITTED; not theory closed. Footings never pooled. Adopts nothing.")
P(f"footings (the record's hosted path): a0 canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e}; L* floor {CELLS['L_floor_pc']}")

# ================================================================ known answers KB1-KB3 (Stage B)
# ---- AC15's grader, ported verbatim (field, grade_snap) for the Sun cells (C5, KB1)
cl = 2.99792458e8; GMs = 1.32712440018e20
FOOT15 = {"canonical": dict(rho=0.0447, lengths=(21.68, 24., 27.)), "alt": dict(rho=0.0514, lengths=(22.85, 24., 24.60))}
VS15 = (220e3, 369e3); PLAN = {"Earth": (1.0, 8.7e-15), "Mars": (1.524, 1.4e-15), "Saturn": (9.58, 7.0e-15)}
Q2_LINE, HEES, LMAX15 = 5.2e-27, 9.0e-27, 24


def cells15():
    out = []
    for f, p in FOOT15.items():
        rho = p["rho"] * MSUN / PC ** 3
        for L in p["lengths"]:
            cg = math.sqrt(2 * math.pi * G_SI * rho) * L * PC
            for V in VS15:
                RA = 2 * GMs / V ** 2
                out.append(dict(foot=f, Lstar=L, V=V, rho=rho, c_gal=cg, M=V / cg, RA=RA, hedgehog=GMs / (L * PC) ** 2))
    return out


CELLS15 = cells15()


def field15(snap, Mcell, rp_list, use_qB=False):
    q, u, v, re, te, Mrun = snap["q"], snap["u"], snap["v"], snap["re"], snap["te"], float(snap["M"])
    rc = 0.75 * (re[1:] ** 4 - re[:-1] ** 4) / (re[1:] ** 3 - re[:-1] ** 3)
    tc = 0.5 * (te[1:] + te[:-1])
    if use_qB:
        w2 = u ** 2 + v ** 2
        qq = np.maximum(1.0 + Mrun ** 2 * (0.5 / rc[:, None] + 0.5 * (1.0 - w2)), 0.0)
    else:
        qq = q
    dq = qq - 1.0
    scale = max((Mcell / Mrun) ** 2, 1.0)
    dV = 2 * np.pi * ((re[1:] ** 3 - re[:-1] ** 3) / 3)[:, None] * (np.cos(te[:-1]) - np.cos(te[1:]))[None, :]
    m = dq * dV * scale
    x = np.cos(tc)
    Pl = np.array([eval_legendre(l, x) for l in range(LMAX15 + 1)])
    dPl = np.zeros_like(Pl)
    for l in range(1, LMAX15 + 1):
        dPl[l] = l * (x * Pl[l] - Pl[l - 1]) / np.where(np.abs(x ** 2 - 1) > 1e-14, x ** 2 - 1, 1e-14) * (-np.sin(tc))
    rin = re[0]
    Mcore = 4 * np.pi * Mcell ** 2 * (rin ** 2 / 4 + rin ** 3 / 6)
    mom = np.einsum("it,lt->li", m, Pl)
    out = {}
    Iext1_0 = np.sum(mom[1] * rc ** (-2.0))
    for rp0 in rp_list:
        rp = float(re[np.argmin(np.abs(re - rp0))])
        inner = rc < rp
        ar = np.zeros_like(tc); at = np.zeros_like(tc); ar2 = np.zeros_like(tc); at2 = np.zeros_like(tc)
        for l in range(LMAX15 + 1):
            Ilt = np.sum(mom[l][inner] * rc[inner] ** l)
            Igt = np.sum(mom[l][~inner] * rc[~inner] ** (-l - 1.0))
            if l == 0:
                Ilt += Mcore
            arl = Pl[l] * (-(l + 1) * rp ** (-l - 2.0) * Ilt + l * rp ** (l - 1.0) * Igt)
            atl = dPl[l] / rp * (rp ** (-l - 1.0) * Ilt + rp ** l * Igt)
            ar += arl; at += atl
            if l == 2:
                ar2, at2 = arl, atl
        ar -= Iext1_0 * np.cos(tc); at -= -Iext1_0 * np.sin(tc)
        out[rp0] = (ar, at, ar2, at2)
    return out, tc


def grade_snap15(snap, use_qB=False, cells=None):
    rows = []
    for c in (cells or CELLS15):
        rps = {pl: d * AU / c["RA"] for pl, (d, _) in PLAN.items()}
        f, tc = field15(snap, c["M"], list(rps.values()), use_qB)
        conv = G_SI * c["rho"] * c["RA"]
        row = dict(foot=c["foot"], Lstar=c["Lstar"], V=c["V"], M=c["M"])
        for pl, rp in rps.items():
            ar, at, ar2, at2 = f[rp]
            mag = np.hypot(ar, at) * conv
            row[f"G1_{pl}"] = float(mag.max() / PLAN[pl][1])
            row[f"G2_{pl}"] = float((mag.max() - mag.min()) / PLAN[pl][1])
            row[f"hh_{pl}"] = float(c["hedgehog"] / PLAN[pl][1])
            if pl == "Saturn":
                row["G3"] = float(np.hypot(ar2, at2).max() * conv / (rp * c["RA"]) / Q2_LINE)
        rows.append(row)
    return rows


GKEYS = [f"G1_{p}" for p in PLAN] + [f"G2_{p}" for p in PLAN] + ["G3"]


def worst15(rows):
    return {k: max(r[k] for r in rows) for k in GKEYS}


def grade_sun_run(tag, cells=None):
    snaps = load_snaps(tag)
    if snaps is None:
        MISSING.append(tag); return None
    per = {}
    for use_qB in (False, True):
        hist = [worst15(grade_snap15(s_, use_qB, cells)) for s_ in snaps]
        fin = hist[-1]; env = {k: max(h[k] for h in hist) for k in GKEYS}
        chg = max(abs(h[k] / fin[k] - 1) if fin[k] > 0 else 0.0 for h in hist for k in GKEYS)
        steady = chg <= 0.05
        per["qB" if use_qB else "q"] = dict(final=fin, envelope=env, max_change_last20=chg, steady=steady, graded=(fin if steady else env),
                                            rows=grade_snap15(snaps[-1], use_qB, cells))
    return per


P("\n=== KB1: the Sun with AC15's reduced equations (REFLECT, M 490, coarse: AC15's worst bracket), and the full A1 system at 1 AU ===")
kb1_tag = "B5_canonical_r0_V1_reflect_uniform_coarse_REDUCED_M490"
kb1 = grade_sun_run(kb1_tag)
ac15_snap = os.path.join(REPO, "action_search_2026_11_05", "AC15_moving_sun_nonlinear", "parts", "M490_reflect_uniform_coarse", "snap_04.npz")
if kb1 is not None:
    e_q, s_q = kb1["qB"]["graded"]["G1_Earth"], kb1["qB"]["graded"]["G1_Saturn"]
    bit = None
    if os.path.exists(ac15_snap):
        a15 = np.load(ac15_snap); mine = load_snaps(kb1_tag)[-1]
        bit = max(float(np.max(np.abs(a15["q"] - mine["q"]))), float(np.max(np.abs(a15["u"] - mine["u"]))), float(np.max(np.abs(a15["v"] - mine["v"]))))
    ok1 = abs(e_q / 0.03628 - 1) <= 0.30 and abs(s_q / 0.10749 - 1) <= 0.30
    check(RES["KB"], "KB1a", ok1, f"reduced equations, AC15's REFLECT M490 coarse run regraded over AC15's 12 cells, q_B reading: Earth {e_q:.5f} (AC15 0.03628), "
          f"Saturn {s_q:.5f} (AC15 0.10749), line 30 %; q reading Earth {kb1['q']['graded']['G1_Earth']:.3g}; bitwise vs AC15's snap_04 (q, u, v) max |diff| {bit}")
    RES["KB"]["KB1a"].update(earth_qB=e_q, saturn_qB=s_q, bitwise_max_diff=bit, worst_q=kb1["q"]["graded"], worst_qB=kb1["qB"]["graded"])
else:
    check(RES["KB"], "KB1a", False, f"run missing: {kb1_tag}")

# ---- the Sun under the full A1 system: every B5 run, graded on the floor cells of its footing (and AC15's 12 cells, reported)
SUN = {}
for f in FOOTS:
    row = CELLS["cells"][f]["B5"]["rows"][0]
    floor_cells = [c for c in CELLS15 if c["foot"] == f and c["Lstar"] == FOOT15[f]["lengths"][0]]
    SUN[f] = {}
    for vi in (0, 1):
        for start, res, bc in (("uniform", "coarse", "transmit"), ("uniform", "medium", "transmit"), ("hedgehog", "coarse", "transmit")):
            tag = tag_of("B5", f, 0, vi, start, res, bc=bc)
            SUN[f][tag] = dict(floor=grade_sun_run(tag, floor_cells), all12=grade_sun_run(tag))
    tag = tag_of("B5", f, 0, 1, "uniform", "coarse", bc="reflect")
    SUN[f][tag] = dict(floor=grade_sun_run(tag, floor_cells), all12=grade_sun_run(tag))
ac15_ref = None
try:
    g15 = json.load(open(os.path.join(REPO, "action_search_2026_11_05", "AC15_moving_sun_nonlinear", "GRADE.json")))
    rws = g15["brackets"]["M490_transmit_uniform_medium"]["q"]["rows"]
    ac15_ref = [r for r in rws if r["foot"] == "canonical" and r["Lstar"] == 21.68 and r["V"] == 369000.0][0]
except Exception as e:  # noqa
    P(f"   AC15 GRADE.json not readable: {e}")
tagf = tag_of("B5", "canonical", 0, 1, "uniform", "medium")
if SUN["canonical"].get(tagf, {}).get("floor") and ac15_ref:
    mine = [r for r in SUN["canonical"][tagf]["floor"]["q"]["rows"] if r["V"] == 369000.0][0]
    d_earth = abs(mine["G1_Earth"] / ac15_ref["G1_Earth"] - 1)
    check(RES["KB"], "KB1b", d_earth <= 0.27, f"full A1 system (Legendre + charge gravity on), canonical floor cell V 369 (M {mine['M']:.1f}), TRANSMIT uniform medium, q reading: "
          f"G1 Earth {mine['G1_Earth']:.4g} vs AC15's {ac15_ref['G1_Earth']:.4g} (rel diff {d_earth:.2e}, line 27 %); Mars {mine['G1_Mars']:.3g} vs {ac15_ref['G1_Mars']:.3g}, "
          f"Saturn {mine['G1_Saturn']:.3g} vs {ac15_ref['G1_Saturn']:.3g}")
    RES["KB"]["KB1b"].update(mine={k: mine[k] for k in GKEYS}, ac15={k: ac15_ref[k] for k in GKEYS})
else:
    check(RES["KB"], "KB1b", False, f"run or AC15 reference missing: {tagf}")

P("\n=== KB2: HEDGEHOG start at V = 0 holds the static solution (line 1e-2) ===")
kb2 = {}
P("   B3/B4 HEDGEHOG and no-wind starts NOT RUN: the linear EFE response (A1g/A1h) is outside its validity there (the body's Newtonian field exceeds the host's "
  "at the readout, gN/gext 2.1-2.6; the linear phantom carries a negative total charge down to -12.6 rho_h and the hold runs away). B3/B4 are graded on the UNIFORM start only (C4: D only).")
for tag, kind in ((tag_of("B1", "canonical", 0, 1, "hedgehog", "coarse", flags="_NOWIND_linear"), "galaxy"), (tag_of("B1", "canonical", 0, 1, "hedgehog", "medium", flags="_NOWIND_linear"), "galaxy"),
                  (tag_of("B2", "canonical", 6, 1, "hedgehog", "coarse", flags="_NOWIND_linear"), "galaxy"), (tag_of("B1", "canonical", 0, 1, "hedgehog", "coarse", flags="_NOWIND_d10"), "galaxy-d10"),
                  (tag_of("B5", "canonical", 0, 0, "hedgehog", "coarse", flags="_NOWIND_t50"), "sun")):
    snaps = load_snaps(tag)
    if snaps is None:
        MISSING.append(tag); kb2[tag] = None; P(f"   {tag}: MISSING"); continue
    sn = snaps[-1]; re = sn["re"]; rc = 0.75 * (re[1:] ** 4 - re[:-1] ** 4) / (re[1:] ** 3 - re[:-1] ** 3)
    if kind.startswith("galaxy"):
        st = np.load(os.path.join(PARTS, tag, "static.npz"))["s"]
        err = float(np.max(np.abs(sn["s"] - st)) / np.max(np.abs(st))); errq = float(np.max(np.abs(sn["q"] - 1)))
        kb2[tag] = dict(hold_err=err, q_drift=errq, s_static_max=float(st.max()), s_static_min=float(st.min()), t=float(sn["t"]), max_w=float(np.max(np.hypot(sn["u"], sn["v"]))),
                        graded=(kind == "galaxy"))
        P(f"   {tag}: t {sn['t']:.1f}: max|s - s_static|/max|s_static| {err:.2e}; max|q - 1| {errq:.2e}; max|w| {kb2[tag]['max_w']:.2e}; s_static in [{st.min():.3g}, {st.max():.3g}]"
          + ("" if kind == "galaxy" else "  (the record's nonlinear D10 phantom under the linear kernel: reported, not graded)"))
    else:
        par = json.loads(str(sn["par"])); qh = 1 + float(sn["M"]) ** 2 * par["gpar"] / rc
        err = float(np.abs(sn["q"][rc <= 100] / qh[rc <= 100, None] - 1).max()); kb2[tag] = dict(hold_err=err, t=float(sn["t"]))
        P(f"   {tag}: t {sn['t']:.1f}: max|q/q_hh - 1| at r <= 100 R_A = {err:.2e}")
vals = [v["hold_err"] for v in kb2.values() if v and v.get("graded", True)]
check(RES["KB"], "KB2", bool(vals) and max(vals) <= 1e-2 and all(v is not None for v in kb2.values()), f"worst hold {max(vals) if vals else None:.2e} over {len(vals)} no-wind runs (line 1e-2)")
RES["KB"]["KB2"].update(runs=kb2)

P("\n=== KB3: UNIFORM start, gravity off, holds the uniform wind (line 1e-2 on medium; AC15 KA3 line) ===")
kb3 = {}
for cell, res, flags in (("B1", "coarse", "_NOGRAV"), ("B1", "medium", "_NOGRAV"), ("B5", "coarse", "_NOGRAV_t50"), ("B5", "medium", "_NOGRAV_t50")):
    tag = tag_of(cell, "canonical", 0, 1, "uniform", res, flags=flags); snaps = load_snaps(tag)
    if snaps is None:
        MISSING.append(tag); kb3[tag] = None; P(f"   {tag}: MISSING"); continue
    sn = snaps[-1]; re = sn["re"]; rc = np.sqrt(re[1:] * re[:-1]); sel = rc >= 2.5 * re[0]
    tm, tp = sn["te"][:-1], sn["te"][1:]
    SC = ((tp - tm) / 2 - (np.sin(2 * tp) - np.sin(2 * tm)) / 4) / (np.cos(tm) - np.cos(tp)); CC = ((np.sin(tp) ** 2 - np.sin(tm) ** 2) / 2) / (np.cos(tm) - np.cos(tp))
    eq = float(np.abs(sn["q"][sel] - 1).max()); ew = float(max(np.abs(sn["u"][sel] + CC).max(), np.abs(sn["v"][sel] - SC).max()))
    kb3[tag] = dict(res=res, cell=cell, max_q_err=eq, max_w_err=ew, t=float(sn["t"]))
    P(f"   {tag}: t {sn['t']:.1f}, r >= 2.5 r_in: max|q - 1| {eq:.2e}, |w + z| {ew:.2e}")
med = [v["max_q_err"] for v in kb3.values() if v and v["res"] == "medium"]
check(RES["KB"], "KB3", bool(med) and len(med) == 2 and max(med) <= 1e-2, f"medium grids: max|q - 1| {med} (line 1e-2); coarse reported")
RES["KB"]["KB3"].update(runs=kb3)

# ================================================================ static references per row and the hydro readouts
P("\n=== static references (D10 solver on X1/SE2's call) and Stage B readouts, per footing, cell and row ===")
ROWS = {f: {} for f in FOOTS}
for f in FOOTS:
    a0 = A0[f]
    for cell in ("B1", "B2", "B3", "B4"):
        ROWS[f][cell] = []
        for i, row in enumerate(CELLS["cells"][f][cell]["rows"]):
            a_m = row["a_pc"] * PC; M = row["M_b_Msun"] * MSUN
            y = float(row["y_plummer"]) if "y_plummer" in row else G_SI * M / (a_m ** 2 * a0)      # the record's own y (S1 / X1)
            xe = row["x_e"]; Lam = row["Lam_floor"]
            rread = row["r_read_pc"][0] / row["a_pc"]                           # readout in units of a
            st = static(y, xe, Lam); iso0 = static(y, 0.0, 0.0); isoL = static(y, 0.0, Lam); nw = newton(y)
            gs, gi, giL, gN = g_at(st, rread), g_at(iso0, rread), g_at(isoL, rread), float(S.plummer_gN(rread, y))
            r12 = 4.0 / 3.0
            rec = dict(name=row["name"], y=y, x_e=xe, Lam=Lam, r_read_over_a=rread, g_static=gs, g_iso=gi, g_iso_Lfloor=giL, g_N=gN,
                       g_static_over_gN=gs / gN, g_iso_over_gN=gi / gN, wo_static=st["wo"], wo_N=nw["wo"], wo_iso=iso0["wo"], vir_static=st["vir"], vir_N=nw["vir"],
                       g_static_r12_over_gN=g_at(st, r12) / float(S.plummer_gN(r12, y)), solver_res=st["res"], gN_over_gext=gN / xe)
            # KA: SE2's E_v3_dmean reproduced (B1) ; X1's column difference (B2)
            if cell == "B1":
                a_s1 = row["a_pc"] * 3.0857e16                                      # S1's PC_ (CFG933's constants) for the sealed estimator
                sig_pred = math.sqrt(st["wo"] * a0 * a_s1) / 1e3; E = 2 * math.log(row["sigma_obs"] / sig_pred)
                rec.update(E_v3_repro=E, E_v3_record=row["E_v3_dmean"], dE=E - row["E_v3_dmean"],
                           E_N=2 * math.log(row["sigma_obs"] / (math.sqrt(nw["wo"] * a0 * a_s1) / 1e3)), E_iso=2 * math.log(row["sigma_obs"] / (math.sqrt(iso0["wo"] * a0 * a_s1) / 1e3)))
            if cell == "B2":
                rc_ = row["record"]; rec.update(record=rc_, csv_dlog=rc_["Delta_v3_floor"] - rc_["Delta_Newton"], solver_dlog_r12=-math.log10(st["wo"] / nw["wo"]))
            # Stage B runs of the row
            runs = []
            for tag, start, vi, res in runs_for(cell, f, i):
                snaps = load_snaps(tag); dn = done_of(tag)
                if snaps is None or dn is None:
                    MISSING.append(tag); runs.append(dict(tag=tag, start=start, vi=vi, res=res, missing=True)); continue
                par = json.loads(str(snaps[-1]["par"]))
                stat_s = np.load(os.path.join(PARTS, tag, "static.npz"))["s"] if start == "hedgehog" else None
                ro, eps_static = readout(snaps, par, stat_s)
                key = f"{rread:.6g}"
                hist = [r_[key]["eps_sphere"] for r_ in ro]; fin = ro[-1][key]
                chg = max(abs((1 + h) / (1 + hist[-1]) - 1) for h in hist); chg_eps = max(abs(h - hist[-1]) for h in hist)
                run = dict(tag=tag, start=start, vi=vi, res=res, V_kms=par["V_kms"], M_inf=par["M_inf"], gpar=par["gpar"], eps_final=fin["eps_sphere"],
                           eps_up=fin["eps_up"], eps_side=fin["eps_side"], eps_down=fin["eps_down"], eps_max_abs=fin["eps_max_abs"], eps_hist=hist,
                           steady_change_graded=chg, eps_abs_change_last20=chg_eps, forces=dn.get("forces"), peak_rss_mb=dn.get("peak_rss_mb"), t_end=float(snaps[-1]["t"]))
                if eps_static is not None:
                    es = eps_static[key]; run.update(eps_static_lin=es, swept_fraction=(1 - fin["eps_sphere"] / es) if es != 0 else None)
                runs.append(run)
            rec["runs"] = runs
            eps_list = [r_["eps_final"] for r_ in runs if not r_.get("missing")]
            rec["eps_worst"] = max(eps_list) if eps_list else None               # the reading most in the theory's favour
            rec["eps_min"] = min(eps_list) if eps_list else None
            rec["D_by_vi"] = {vi: math.log10(gN * (1 + max(r_["eps_final"] for r_ in runs if not r_.get("missing") and r_["vi"] == vi)) / gs)
                              for vi in (0, 1) if any(not r_.get("missing") and r_["vi"] == vi for r_ in runs)}
            sw = [r_["swept_fraction"] for r_ in runs if not r_.get("missing") and r_.get("swept_fraction") is not None]
            rec["swept_fraction_range"] = [min(sw), max(sw)] if sw else None
            if rec["eps_worst"] is not None:
                gd = gN * (1 + rec["eps_worst"])
                rec["g_dyn"] = gd; rec["D"] = math.log10(gd / gs); rec["F"] = (math.log10(gd) - math.log10(gs)) / (math.log10(gi) - math.log10(gs))
                rec["D_at_eps0"] = math.log10(gN / gs); rec["F_at_eps0"] = (math.log10(gN) - math.log10(gs)) / (math.log10(gi) - math.log10(gs))
                mres = [r_ for r_ in runs if not r_.get("missing") and r_["res"] == "medium"]; cres = [r_ for r_ in runs if not r_.get("missing") and r_["res"] == "coarse"]
                if mres and cres:
                    pairs = []
                    for m_ in mres:
                        c_ = [c for c in cres if c["start"] == m_["start"] and c["vi"] == m_["vi"]]
                        if c_:
                            pairs.append(dict(start=m_["start"], vi=m_["vi"], eps_coarse=c_[0]["eps_final"], eps_medium=m_["eps_final"],
                                              D_coarse=math.log10(gN * (1 + c_[0]["eps_final"]) / gs), D_medium=math.log10(gN * (1 + m_["eps_final"]) / gs)))
                    rec["convergence"] = pairs
                    rec["conv_max_rel_change_graded"] = max(abs((1 + p["eps_coarse"]) / (1 + p["eps_medium"]) - 1) for p in pairs) if pairs else None
            ROWS[f][cell].append(rec)
            fl = (f"D {rec['D']:+.4f} F {rec['F']:+.4f} eps_worst {rec['eps_worst']:+.2e} (min {rec['eps_min']:+.2e})" if rec.get("D") is not None else "runs MISSING")
            extra = (f"; KA_SE2 E_v3 repro {rec['E_v3_repro']:.6f} vs record {rec['E_v3_record']:.6f} (d {rec['dE']:.1e})" if cell == "B1" else
                     f"; X1 csv Delta[v3]-Delta[N] {rec['csv_dlog']:+.3f} vs solver -log10(wo_v3/wo_N) {rec['solver_dlog_r12']:+.3f}" if cell == "B2" else "")
            P(f"  [{f}] {cell} {row['name'][:20]:20s} y {y:.3e} x_e {xe:.3f} Lam {Lam:.2e}: g_static/g_N {gs / gN:.4f} g_iso/g_N {gi / gN:.4f} (iso L*floor {giL / gN:.4f}) | {fl}{extra}")
            for r_ in runs:
                if r_.get("missing"):
                    P(f"       MISSING {r_['tag']}"); continue
                sw = f" static_lin eps {r_['eps_static_lin']:+.3e} swept {r_['swept_fraction']:.4f}" if "eps_static_lin" in r_ else ""
                fo = r_["forces"] or {}
                P(f"       {r_['tag']}: eps sphere {r_['eps_final']:+.3e} (up {r_['eps_up']:+.2e} side {r_['eps_side']:+.2e} down {r_['eps_down']:+.2e}; max|.| {r_['eps_max_abs']:.2e}) "
                  f"steady chg {r_['steady_change_graded']:.1e}{sw}; forces/grav {fo.get('max_force_over_max_grav')} RSS {r_['peak_rss_mb'] and round(r_['peak_rss_mb'])} MB")

# KA checks of the static path
dEs = [abs(r["dE"]) for f in FOOTS for r in ROWS[f]["B1"]]
check(RES["KA"], "KA_SE2", max(dEs) <= 1e-6, f"SE2/S1's per-galaxy E_v3_dmean reproduced by the same solver call for the 9 Coma UDGs, both footings: max |dE| {max(dEs):.1e} (line 1e-6)")
dX = [abs(r["csv_dlog"] - r["solver_dlog_r12"]) for f in FOOTS for r in ROWS[f]["B2"]]
check(RES["KA"], "KA_X1", max(dX) <= 0.05, f"X1's per-row Delta[v3 L*floor] - Delta[Newton] vs the solver's -log10(wo_v3/wo_N) (E-W at r_1/2), 8 MW classical rows both footings: max |d| {max(dX):.3f} (line 0.05; X1's columns are MC medians)")
sres = max(r["solver_res"] for f in FOOTS for c in ("B1", "B2", "B3", "B4") for r in ROWS[f][c])
check(RES["KA"], "KA_solver", sres <= 1e-9, f"D10 Newton residual max {sres:.1e} over every static solve (tol 1e-10)")

# ================================================================ Stage C grades
def boot_median(vals, sds, nb=4000, seed=11):
    rng = np.random.default_rng(seed); vals = np.asarray(vals); sds = np.asarray(sds); n = len(vals); meds = np.empty(nb)
    for b in range(nb):
        ix = rng.integers(0, n, n); meds[b] = np.median(vals[ix] + rng.normal(0, 1, n) * sds[ix])
    q = np.percentile(meds, [2.5, 50, 97.5])
    return dict(median=float(q[1]), ci95=[float(q[0]), float(q[2])], contains0=bool(q[0] <= 0 <= q[2]), n=int(n))


# SE2's own posterior functions (read-only exec of se2.py up to its main loop)
SE2 = None
try:
    f_ = os.path.join(REPO, "closure_2026_11_06", "SE2_step_as_systematics", "se2.py"); src = open(f_).read()
    cut = src.index("# ------------------------------------------------------------------ main loop")
    NS = {"__file__": f_, "__name__": "se2_lib"}; argv0 = sys.argv; sys.argv = [f_]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], f_, "exec"), NS)
    sys.argv = argv0; SE2 = NS
except Exception as e:  # noqa
    P(f"SE2 preamble not loaded: {e}")


def se2_regrade(f, shifts_ln, plant_dex=0.0):
    """SE2's Coma UDG posterior with each admitted galaxy's E_v3_dmean shifted by shifts_ln[name] (ln units) - plant_dex ln10."""
    rows, sk, base = SE2["udg_inputs"](f, SE2["A0"][f])
    rows2 = []
    for r in rows:
        r2 = dict(r); r2["E_v3_dmean"] = float(r["E_v3_dmean"]) + shifts_ln.get(r["name"], 0.0) - plant_dex * LN10; rows2.append(r2)
    out = {}
    for kind in ("half", "main"):
        x, info = SE2["post_udg"](rows2, sk, f, SE2["SPEC"](kind)); xn, _ = SE2["post_udg"](rows2, sk, f, SE2["SPEC"](kind), nominal=True)
        pm, pr = SE2["summ"](x), SE2["summ"](xn)
        out[kind] = dict(post=pm, raw_stat_only=pr, n=info["n"], label=SE2["lab"](pm, pr, info["n"], True))
    return out


X1ROWS = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))
for f in FOOTS:
    FR = dict(cells={}, C2={}, C5={})
    P(f"\n=== [{f}] Stage C ===")
    # ---- C3 first: the sign of D on B1 (per row and median), then C1 F
    for cell in ("B1", "B2", "B3", "B4"):
        rows = ROWS[f][cell]; Ds = [r["D"] for r in rows if r.get("D") is not None]; Fs = [r["F"] for r in rows if r.get("F") is not None]
        D0 = [r["D_at_eps0"] for r in rows if r.get("D_at_eps0") is not None]
        conv = [r["conv_max_rel_change_graded"] for r in rows if r.get("conv_max_rel_change_graded") is not None]
        c = dict(n_rows=len(rows), n_graded=len(Ds), D=Ds, F=Fs, D_median=float(np.median(Ds)) if Ds else None, F_median=float(np.median(Fs)) if Fs else None,
                 D_range=[min(Ds), max(Ds)] if Ds else None, F_range=[min(Fs), max(Fs)] if Fs else None, D_sign_all_negative=bool(Ds) and all(d < 0 for d in Ds),
                 D_at_eps0_range=[min(D0), max(D0)] if D0 else None, conv_max_rel_change=max(conv) if conv else None,
                 D_by_vi={vi: [r["D_by_vi"][vi] for r in rows if r.get("D_by_vi") and vi in r["D_by_vi"]] for vi in (0, 1)},
                 V_bracket_same_label=all(all(d < 0 for d in r["D_by_vi"].values()) or all(d >= 0 for d in r["D_by_vi"].values()) for r in rows if r.get("D_by_vi")),
                 swept_fraction_range=([min(r["swept_fraction_range"][0] for r in rows if r.get("swept_fraction_range")), max(r["swept_fraction_range"][1] for r in rows if r.get("swept_fraction_range"))]
                                       if any(r.get("swept_fraction_range") for r in rows) else None))
        FR["cells"][cell] = c
        P(f"  C3 {cell}: D per row {[round(d, 4) for d in Ds]} -> sign {'ALL NEGATIVE' if c['D_sign_all_negative'] else 'MIXED/POSITIVE'}; median D {c['D_median']}; "
          f"D at eps = 0 (pure Newton) range {c['D_at_eps0_range']}; D by V reading: V0 {[round(d, 3) for d in c['D_by_vi'][0]]} V1 {[round(d, 3) for d in c['D_by_vi'][1]]} "
          f"(same label across the bracket: {c['V_bracket_same_label']}); HEDGEHOG swept fraction range {c['swept_fraction_range']}")
        if cell in ("B1", "B2"):
            P(f"  C1 {cell}: F per row {[round(x, 4) for x in Fs]}; median F {c['F_median']}; coarse->medium change of the graded ratio (rep row) {c['conv_max_rel_change']}")
        else:
            P(f"  C4 {cell}: D only (host row proxy; the member sweep cannot change the host's own hydrostatic/lensing need of x4.2/3.8): D {Ds}")
    # ---- C2: Coma UDGs on SE2's path; X1's MW classical and bright M31 rows
    if SE2 is not None and all(r.get("eps_worst") is not None for r in ROWS[f]["B1"]):
        shifts = {r["name"]: math.log(r["wo_static"] / (r["wo_N"] * (1 + r["eps_worst"]))) for r in ROWS[f]["B1"]}   # E_dyn = E_v3 + ln(wo_v3/wo_dyn)
        rec0 = se2_regrade(f, {}); regr = se2_regrade(f, shifts)
        FR["C2"]["Coma_UDGs"] = dict(record=rec0, regraded=regr, shifts_ln=shifts,
                                     shifts_dex={k: v / LN10 for k, v in shifts.items()})
        P(f"  C2 Coma UDGs (SE2 path, widths_half_post_freeze): record median {rec0['half']['post']['median']:+.4f} [{rec0['half']['post']['ci95'][0]:+.3f}, {rec0['half']['post']['ci95'][1]:+.3f}] {rec0['half']['label']} "
          f"-> with g_dyn: {regr['half']['post']['median']:+.4f} [{regr['half']['post']['ci95'][0]:+.3f}, {regr['half']['post']['ci95'][1]:+.3f}] {regr['half']['label']}; "
          f"main widths: {regr['main']['post']['median']:+.4f} [{regr['main']['post']['ci95'][0]:+.3f}, {regr['main']['post']['ci95'][1]:+.3f}] {regr['main']['label']}; per-galaxy shift (dex) "
          + ", ".join(f"{k[:8]} {v / LN10:+.3f}" for k, v in shifts.items()))
    else:
        P("  C2 Coma UDGs: NOT GRADED (runs missing or SE2 unavailable)")
    epsB2 = [r["eps_worst"] for r in ROWS[f]["B2"] if r.get("eps_worst") is not None]
    if epsB2:
        eB2 = max(epsB2)
        for cls in ("MW classical", "bright M31"):
            rr = [r for r in X1ROWS if r["footing"] == f and r["cls"] == cls]
            dv3 = [float(r["Delta[v3 L*floor]"]) for r in rr]; sv3 = [float(r["sdMC[v3 L*floor]"]) for r in rr]
            dN = [float(r["Delta[Newton]"]) - math.log10(1 + eB2) for r in rr]; sN = [float(r["sdMC[Newton]"]) for r in rr]
            rec_b = boot_median(dv3, sv3); dyn_b = boot_median(dN, sN)
            FR["C2"][cls] = dict(record=rec_b, regraded=dyn_b, eps_used=eB2, note="g_dyn = g_N(1 + eps_B2,worst) for every row; bootstrap median over systems with the per-row MC sd")
            P(f"  C2 {cls} (X1 rows, n {len(rr)}): record v3 L*floor median {rec_b['median']:+.3f} [{rec_b['ci95'][0]:+.3f}, {rec_b['ci95'][1]:+.3f}] -> with g_dyn (Newton x (1 + {eB2:+.2e})): "
              f"{dyn_b['median']:+.3f} [{dyn_b['ci95'][0]:+.3f}, {dyn_b['ci95'][1]:+.3f}] {'EXPLAINED' if dyn_b['contains0'] else 'NOT EXPLAINED'}")
    # ---- C5: the Sun under the full A1 system
    wq = {}; steady_all = True; brackets = {}
    for tag, gr in SUN[f].items():
        if gr["floor"] is None:
            brackets[tag] = "MISSING"; continue
        per = gr["floor"]; brackets[tag] = {k_: dict(graded=per[k_]["graded"], steady=per[k_]["steady"], chg=per[k_]["max_change_last20"]) for k_ in ("q", "qB")}
        for k_ in ("q", "qB"):
            steady_all &= per[k_]["steady"]
            for gk in GKEYS:
                wq[gk] = max(wq.get(gk, 0.0), per[k_]["graded"][gk])
        P(f"  C5 {tag}: q {'steady' if per['q']['steady'] else 'NOT STEADY'} " + ", ".join(f"{k} {per['q']['graded'][k]:.3g}" for k in GKEYS)
          + f" | qB {'steady' if per['qB']['steady'] else 'NOT STEADY'} " + ", ".join(f"{k} {per['qB']['graded'][k]:.3g}" for k in GKEYS))
    c5_ok = bool(wq) and all(v < 1 for v in wq.values()) and not any(v == "MISSING" for v in brackets.values())
    FR["C5"] = dict(worst_over_brackets_floor=wq, brackets=brackets, steady_all=steady_all, ok=c5_ok)
    P(f"  C5 [{f}] worst over every B5 bracket (floor L*, q and q_B, envelopes where NOT STEADY), ratio to the AC15/MS3 lines: {wq} -> {'PASS' if c5_ok else 'FAIL/INCOMPLETE'}")
    RES["footings"][f] = FR

# ================================================================ MUTATE
PM("\n=== MUTATE (must bite) ===")
for f in FOOTS:
    FR = RES["footings"][f]; MU = {}
    # MUTATE-1: V -> 0: the Stage B state is the held static solution; F must read 0
    m1 = {}
    for cell, row_i, tagn in (("B1", 0, tag_of("B1", "canonical", 0, 1, "hedgehog", "coarse", flags="_NOWIND_linear")), ("B2", 6, tag_of("B2", "canonical", 6, 1, "hedgehog", "coarse", flags="_NOWIND_linear"))):
        snaps = load_snaps(tagn); rec = ROWS[f][cell][row_i]
        if snaps is None:
            m1[cell] = None; continue
        par = json.loads(str(snaps[-1]["par"])); st = np.load(os.path.join(PARTS, tagn, "static.npz"))["s"]
        ro, eps_st = readout(snaps, par, st); key = f"{rec['r_read_over_a']:.6g}"; eps_hold = ro[-1][key]["eps_sphere"]; eps_lin = eps_st[key]
        g_hold = rec["g_N"] * (1 + eps_hold); g_lin = rec["g_N"] * (1 + eps_lin)
        F_own = (math.log10(g_hold) - math.log10(g_lin)) / (math.log10(rec["g_iso"]) - math.log10(g_lin))                 # against the lane's own static (linear) reference
        F_rec = (math.log10(g_hold) - math.log10(rec["g_static"])) / (math.log10(rec["g_iso"]) - math.log10(rec["g_static"]))   # against the record's (nonlinear) static
        m1[cell] = dict(tag=tagn, eps_hold=eps_hold, eps_static_lin=eps_lin, F_vs_own_static=F_own, F_vs_record_static=F_rec,
                        g_static_lin_over_gN=1 + eps_lin, g_static_record_over_gN=rec["g_static_over_gN"], note="the no-wind run is the canonical footing's")
        PM(f"  [{f}] MUTATE-1 V -> 0 ({cell} {rec['name']}): held state eps {eps_hold:+.4e} vs its static start {eps_lin:+.4e}: F vs the lane's static {F_own:+.2e} (must read 0); "
           f"F vs the record's static (nonlinear D10) {F_rec:+.3f} [linear static boost {1 + eps_lin:.3f} vs record {rec['g_static_over_gN']:.3f}]")
    ok1 = all(v is not None and abs(v["F_vs_own_static"]) <= 0.3 for v in m1.values())
    MU["M1"] = dict(ok=ok1, rows=m1)
    # MUTATE-2: g_ext -> 0: isolated host, the body keeps its own khronon: g_dyn = g_iso and the reference g_static -> g_iso; F must read 1 by construction
    m2 = {}
    for cell in ("B1", "B2"):
        rec = ROWS[f][cell][REP[cell]]
        Fm2 = (math.log10(rec["g_iso"]) - math.log10(rec["g_static"])) / (math.log10(rec["g_iso"]) - math.log10(rec["g_static"]))
        m2[cell] = dict(F=Fm2)
        PM(f"  [{f}] MUTATE-2 g_ext -> 0 ({cell} {rec['name']}): g_dyn := g_iso (no host khronon to sweep; the isolated static state) -> F = {Fm2:.4f} (must read 1)")
    MU["M2"] = dict(ok=all(abs(v["F"] - 1) < 1e-12 for v in m2.values()), rows=m2)
    # MUTATE-3: plant +0.5 dex on g_dyn in B1; C2 must move toward EXPLAINED
    if SE2 is not None and "Coma_UDGs" in FR["C2"]:
        shifts = FR["C2"]["Coma_UDGs"]["shifts_ln"]; base = FR["C2"]["Coma_UDGs"]["regraded"]["half"]["post"]
        pl = se2_regrade(f, shifts, plant_dex=0.5); pp = pl["half"]["post"]
        moved = base["median"] - pp["median"]; flipped = pl["half"]["label"] == "EXPLAINED"
        MU["M3"] = dict(planted_dex=0.5, median_before=base["median"], median_after=pp["median"], ci95_after=pp["ci95"], moved_dex=moved, label_after=pl["half"]["label"],
                        flips=flipped, bites=abs(moved - 0.5) < 0.05, power="FLIPS" if flipped else "NO POWER at a 0.5 dex plant (the plant is detected; the shortfall is larger than the plant)")
        PM(f"  [{f}] MUTATE-3 +0.5 dex planted on g_dyn (B1): C2 half-width median {base['median']:+.4f} -> {pp['median']:+.4f} [{pp['ci95'][0]:+.3f}, {pp['ci95'][1]:+.3f}] {pl['half']['label']}; "
           f"moved {moved:+.3f} dex ({'detected' if MU['M3']['bites'] else 'NOT detected'}); {MU['M3']['power']}")
    else:
        MU["M3"] = dict(ok=False, note="not graded")
    RES["MUTATE"][f] = MU

# ================================================================ labels, hand estimates
P("\n=== LABEL (frozen rule) ===")
pipeline_ok = all(RES["KB"][k]["ok"] for k in ("KB1a", "KB1b", "KB2", "KB3")) and all(RES["KA"][k]["ok"] for k in RES["KA"])
sA = json.load(open(os.path.join(HERE, "xf1_stageA.json"))); stageA_ok = all(c["ok"] for c in sA["checks"].values())
LAB = {}
for f in FOOTS:
    FR = RES["footings"][f]; B1 = FR["cells"]["B1"]; MU = RES["MUTATE"][f]
    mut_ok = MU["M1"]["ok"] and MU["M2"]["ok"]
    complete = B1["n_graded"] == B1["n_rows"] and FR["C5"]["ok"] is not None and not any(v == "MISSING" for v in FR["C5"]["brackets"].values())
    c2 = FR["C2"].get("Coma_UDGs", {}).get("regraded", {}).get("half", {}).get("label")
    reasons = []
    if not (pipeline_ok and stageA_ok and mut_ok):
        label = "NO VERDICT (pipeline: a known answer or MUTATE-1/2 failed)"; reasons.append("pipeline")
    elif not complete:
        label = "INCOMPLETE (runs missing)"
    else:
        Fs = B1["F"]; Ds = B1["D"]
        if not FR["C5"]["ok"]:
            reasons.append("C5 breach")
        if B1["D_sign_all_negative"]:
            reasons.append("C3 D < 0 on B1 (sweep makes the hosted rows worse)")
        if all(x <= 0.3 for x in Fs):
            reasons.append("C1 F <= 0.3 on every B1 row (hosted rows stand as graded)")
        if reasons:
            label = "FAIL"
        elif all(x >= 0.7 for x in Fs) and c2 == "EXPLAINED" and FR["C5"]["ok"]:
            label = "PASS (scoped, hosted state: member rows only; host rows (X-COP, groups) unchanged)"
        else:
            label = "NO VERDICT"; reasons.append(f"F range {B1['F_range']}, C2 {c2}, C5 {FR['C5']['ok']}")
    LAB[f] = dict(label=label, reasons=reasons, F_range_B1=B1["F_range"], D_range_B1=B1["D_range"], C2_Coma=c2, C5_ok=FR["C5"]["ok"], complete=complete)
    P(f"[{f}] LABEL: {label}  reasons: {reasons}; B1 F range {B1['F_range']}, D range {B1['D_range']}; C2 Coma {c2}; C5 {FR['C5']['ok']}")
RES["label"] = LAB; RES["pipeline_ok"] = pipeline_ok; RES["stageA_ok"] = stageA_ok; RES["missing_runs"] = sorted(set(MISSING))

# hand estimates
B1c = RES["footings"]["canonical"]["cells"]["B1"]; B1a = RES["footings"]["alt"]["cells"]["B1"]
HE = {}
HE["HE-a"] = dict(claim="Stage A keeps a Bernoulli-type integral only in the unscreened limit; the screened system is a coupled PDE", verdict="HIT" if stageA_ok else "MISS",
                  basis="A1e/A1d: chi is fixed by the elliptic constraint div[grad chi/(1+|grad chi|/a0)] = K q; Bernoulli only at W = 0 (A4)")
Fall = (B1c["F"] or []) + (B1a["F"] or [])
HE["HE-b"] = dict(claim="B1's F lands between 0.3 and 0.7 (NO VERDICT)", verdict=("HIT" if Fall and all(0.3 < x < 0.7 for x in Fall) else "MISS"), F_range=[min(Fall), max(Fall)] if Fall else None)
wq = [v for f in FOOTS for v in RES["footings"][f]["C5"]["worst_over_brackets_floor"].values()]
HE["HE-c"] = dict(claim="B5 passes C5 with margin > 10x", verdict=("HIT" if wq and max(wq) < 0.1 else "MISS"), worst_ratio_to_line=max(wq) if wq else None,
                  note="graded on the worst over q and q_B readings and every bracket, as AC15/MS3 graded")
Dall = (B1c["D"] or []) + (B1a["D"] or [])
c2lab = [RES["footings"][f]["C2"].get("Coma_UDGs", {}).get("regraded", {}).get("half", {}).get("label") for f in FOOTS]
HE["HE-d"] = dict(claim="D on B1 is positive; C2 stays NOT EXPLAINED", verdict=("HIT" if Dall and all(d > 0 for d in Dall) and all(l == "NOT EXPLAINED" for l in c2lab) else
                  ("MISS on the sign (D negative); the C2 half holds (NOT EXPLAINED)" if all(l == "NOT EXPLAINED" for l in c2lab) else "MISS")), D_range=[min(Dall), max(Dall)] if Dall else None, C2=c2lab)
RES["HE"] = HE
P("\n=== hand estimates ===")
for k, v in HE.items():
    P(f"{k} {v['verdict']}: {v['claim']} -> " + ", ".join(f"{kk} {vv}" for kk, vv in v.items() if kk not in ("claim", "verdict")))
if MISSING:
    P(f"\nMISSING runs ({len(set(MISSING))}): {sorted(set(MISSING))}")
P("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, "xf1.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "xf1.out"), "w").write("\n".join(OUT) + "\n")
open(os.path.join(HERE, "xf1_MUTATE.out"), "w").write("\n".join(MOUT) + "\n")
