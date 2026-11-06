#!/usr/bin/env python3
"""AC15 grader: planets (G1, G2), Cassini Q_eff (G3), known answers KA3-KA5, MUTATE, steadiness,
convergence, shock proxy. Criteria: FROZEN_CRITERIA.md (b089f97024 + AMENDMENT 1 aa2612a47c).

  python3 action_search_2026_11_05/AC15_moving_sun_nonlinear/grade.py
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, glob, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import eval_legendre

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, "parts")
OUT, RES = [], {"lane": "AC15_moving_sun_nonlinear", "criteria": ["b089f97024", "aa2612a47c"], "checks": {}}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    RES["checks"][name] = dict(ok=bool(ok), detail=str(detail)); P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


# ------------------------------------------------------------------ physical inputs
cl = 2.99792458e8; PC = 3.0856775814913673e16; AU = 1.495978707e11; G = 6.67430e-11; MSUN = 1.98847e30
GMs = 1.32712440018e20
FOOT = {"canonical": dict(rho=0.0447, lengths=(21.68, 24., 27.)), "alt": dict(rho=0.0514, lengths=(22.85, 24., 24.60))}
VS = (220e3, 369e3)
PLAN = {"Earth": (1.0, 8.7e-15), "Mars": (1.524, 1.4e-15), "Saturn": (9.58, 7.0e-15)}
Q2_LINE, HEES = 5.2e-27, 9.0e-27
LMAX = 24


def cells():
    out = []
    for f, p in FOOT.items():
        rho = p["rho"] * MSUN / PC ** 3
        for L in p["lengths"]:
            cg = math.sqrt(2 * math.pi * G * rho) * L * PC
            for V in VS:
                RA = 2 * GMs / V ** 2
                out.append(dict(foot=f, Lstar=L, V=V, rho=rho, c_gal=cg, M=V / cg, RA=RA, hedgehog=GMs / (L * PC) ** 2))
    return out


CELLS = cells()
P(f"cells: M_inf {min(c['M'] for c in CELLS):.1f}-{max(c['M'] for c in CELLS):.1f}")


def load(tag, k=None):
    fs = sorted(glob.glob(os.path.join(PARTS, tag, "snap_*.npz")))
    if not fs:
        return None
    return [dict(np.load(f)) for f in (fs if k is None else [fs[k]])]


# ------------------------------------------------------------------ field of an axisymmetric charge
def field(snap, Mcell, rp_list, use_qB=False):
    """code acceleration (relative to the Sun) at radii rp (units R_A), theta grid = cell centres.
    returns dict rp -> (a_r(theta), a_t(theta), a_r_l2, a_t_l2) with G = 1, density in rho0, length in R_A."""
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
    Pl = np.array([eval_legendre(l, x) for l in range(LMAX + 1)])          # (L, NT)
    # theta derivative dP_l/dtheta = -sin(theta) P_l'(x); use recurrence via finite formula
    dPl = np.zeros_like(Pl)
    for l in range(1, LMAX + 1):
        dPl[l] = l * (x * Pl[l] - Pl[l - 1]) / np.where(np.abs(x ** 2 - 1) > 1e-14, x ** 2 - 1, 1e-14) * (-np.sin(tc))
    rin = re[0]
    Mcore = 4 * np.pi * Mcell ** 2 * (rin ** 2 / 4 + rin ** 3 / 6)            # Bernoulli cap inside r_in (exact in M_cell)
    mom = np.einsum("it,lt->li", m, Pl)                                       # (L, NR) per-shell P_l moment
    out = {}
    # Sun's own acceleration: exterior l = 1 at r -> 0: a_z(0) = G * sum m r'^-2 P_1
    Iext1_0 = np.sum(mom[1] * rc ** (-2.0))
    for rp0 in rp_list:
        rp = float(re[np.argmin(np.abs(re - rp0))])                        # evaluate on the nearest radial edge (exact shell split)
        inner = rc < rp
        ar = np.zeros_like(tc); at = np.zeros_like(tc); ar2 = np.zeros_like(tc); at2 = np.zeros_like(tc)
        for l in range(LMAX + 1):
            Ilt = np.sum(mom[l][inner] * rc[inner] ** l)
            Igt = np.sum(mom[l][~inner] * rc[~inner] ** (-l - 1.0))
            if l == 0:
                Ilt += Mcore
            arl = Pl[l] * (-(l + 1) * rp ** (-l - 2.0) * Ilt + l * rp ** (l - 1.0) * Igt)
            atl = dPl[l] / rp * (rp ** (-l - 1.0) * Ilt + rp ** l * Igt)
            ar += arl; at += atl
            if l == 2:
                ar2, at2 = arl, atl
        # subtract the Sun's acceleration (uniform vector G Iext1_0 z): r-comp cos, theta-comp -sin
        ar -= Iext1_0 * np.cos(tc); at -= -Iext1_0 * np.sin(tc)
        out[rp0] = (ar, at, ar2, at2)
    return out, tc


def grade_snap(snap, use_qB=False):
    """per cell: G1, G2 (ratios to bound), G3 (Q_eff / line), plus hedgehog-fraction."""
    rows = []
    for c in CELLS:
        rps = {pl: d * AU / c["RA"] for pl, (d, _) in PLAN.items()}
        f, tc = field(snap, c["M"], list(rps.values()), use_qB)
        conv = G * c["rho"] * c["RA"]                                            # code accel -> m/s^2
        row = dict(foot=c["foot"], Lstar=c["Lstar"], V=c["V"], M=c["M"])
        for pl, rp in rps.items():
            ar, at, ar2, at2 = f[rp]
            mag = np.hypot(ar, at) * conv
            row[f"G1_{pl}"] = float(mag.max() / PLAN[pl][1])
            row[f"G2_{pl}"] = float((mag.max() - mag.min()) / PLAN[pl][1])
            row[f"radial_mean_{pl}"] = float(np.mean(ar) * conv)
            row[f"hh_{pl}"] = float(c["hedgehog"] / PLAN[pl][1])
            if pl == "Saturn":
                row["G3"] = float(np.hypot(ar2, at2).max() * conv / (rp * c["RA"]) / Q2_LINE)
                row["G3_hees"] = row["G3"] * Q2_LINE / HEES
        rows.append(row)
    return rows


GKEYS = [f"G1_{p}" for p in PLAN] + [f"G2_{p}" for p in PLAN] + ["G3"]


def worst(rows):
    return {k: max(r[k] for r in rows) for k in GKEYS}


# field-code test (added, not frozen): a synthetic static hedgehog must give C6P's GM/Lstar^2 (code pi M^2 r^2 shells + core cap)
_re = 2 * np.exp(0.025 * np.arange(277)); _te = np.linspace(0, np.pi, 161)
_rc = 0.75 * (_re[1:] ** 4 - _re[:-1] ** 4) / (_re[1:] ** 3 - _re[:-1] ** 3)
_q = (1 + 234.0 ** 2 * 0.5 / _rc)[:, None] * np.ones(160)
_f, _ = field(dict(q=_q, u=0 * _q, v=0 * _q, re=_re, te=_te, M=234.0), 234.0, [27.28, 261.3])
_err = max(abs(_f[rp][0].mean() / (-(math.pi * 234.0 ** 2 * (float(_re[np.argmin(abs(_re - rp))]) ** 2 - 4) + 4 * math.pi * 234.0 ** 2 * (7 / 3))
                                    / float(_re[np.argmin(abs(_re - rp))]) ** 2) - 1) for rp in _f)
_c = CELLS[0]
_conv = abs(G * _c["rho"] * _c["RA"] * math.pi * _c["M"] ** 2 / _c["hedgehog"] - 1)

# ------------------------------------------------------------------ known answers
def ka3():
    res = {}
    for rs in ("coarse", "medium"):
        s = load(f"M234_transmit_uniform_{rs}_NOGRAV_t50")
        if s is None:
            return None
        s = s[-1]; re = s["re"]; rc = np.sqrt(re[1:] * re[:-1]); tc = 0.5 * (s["te"][1:] + s["te"][:-1])
        sel = rc >= 5
        tm, tp = s["te"][:-1], s["te"][1:]
        SC = ((tp - tm) / 2 - (np.sin(2 * tp) - np.sin(2 * tm)) / 4) / (np.cos(tm) - np.cos(tp))   # cell averages
        CC = ((np.sin(tp) ** 2 - np.sin(tm) ** 2) / 2) / (np.cos(tm) - np.cos(tp))
        res[rs] = dict(q=float(np.abs(s["q"][sel] - 1).max()),
                       w=float(max(np.abs(s["u"][sel] + CC).max(), np.abs(s["v"][sel] - SC).max())))
    return res


RES["checks"]["FIELD_TEST"] = dict(ok=bool(_err <= 1e-2 and _conv <= 1e-12), detail=f"synthetic hedgehog radial field vs exact {_err:.1e} (1e-2); code->SI pi M^2 vs GM/Lstar^2 {_conv:.1e}")
P(f"FIELD_TEST {'PASS' if RES['checks']['FIELD_TEST']['ok'] else 'FAIL'} {RES['checks']['FIELD_TEST']['detail']}")
r3 = ka3()
if r3:
    check("KA3", r3["coarse"]["q"] <= 1e-2 and r3["medium"]["q"] <= r3["coarse"]["q"] / 2,
          f"gravity off, t 50, r >= 5: max|q-1| coarse {r3['coarse']['q']:.2e} (line 1e-2), medium {r3['medium']['q']:.2e} "
          f"(<= half); |w + z| coarse {r3['coarse']['w']:.2e} medium {r3['medium']['w']:.2e} (reported)")
else:
    check("KA3", False, "runs missing")

s4 = load("M234_transmit_hedgehog_coarse_NOWIND_t50")
if s4:
    s4 = s4[-1]; re = s4["re"]; rc = 0.75 * (re[1:] ** 4 - re[:-1] ** 4) / (re[1:] ** 3 - re[:-1] ** 3)
    qh = 1 + 234.0 ** 2 * 0.5 / rc
    e4 = float(np.abs(s4["q"][rc <= 100] / qh[rc <= 100, None] - 1).max())
    check("KA4", e4 <= 2e-2, f"static hedgehog, no wind, t 50: max |q/q_hh - 1| at r <= 100 = {e4:.2e} (line 2e-2)")
else:
    check("KA4", False, "run missing")
s4r = load("M234_reflect_hedgehog_coarse_NOWIND_t50")
if s4r:
    s4r = s4r[-1]; e4r = float(np.abs(s4r["q"][rc <= 100] / qh[rc <= 100, None] - 1).max())
    P(f"   KA4 with REFLECT inner wall (reported): {e4r:.2e}")


def dust_density(r, psi, rin):
    """pressureless point-mass focusing density n/n0 (GM = 1/2, V = 1), streams with valid periapsis."""
    A = (1 - math.cos(psi)) / 2; B = math.sin(psi)

    def roots(rr):
        disc = math.sqrt(B * B + 4 * A / rr)
        return (-B + disc) / (2 * A), (-B - disc) / (2 * A)

    def rper(b):
        return b * b / (0.5 + math.sqrt(0.25 + b * b))
    dr = 1e-5 * r
    xp1, xm1 = roots(r - dr); xp2, xm2 = roots(r + dr); xp, xm = roots(r)
    n = 0.0
    b1 = 1 / xp; psi_p1 = math.pi - math.atan(2 * b1)            # periapsis angle in (pi/2, pi)
    if psi < psi_p1 or rper(b1) > rin:
        n += abs((1 / xp2 - 1 / xp1) / (2 * dr)) / math.sin(psi)
    b2 = -1 / xm
    if rper(b2) > rin:
        n += abs((-1 / xm2 + 1 / xm1) / (2 * dr)) / math.sin(psi)
    return n


def ka5_err(tag):
    s = load(tag)
    if s is None:
        return None
    s = s[-1]; re = s["re"]; rc = 0.75 * (re[1:] ** 4 - re[:-1] ** 4) / (re[1:] ** 3 - re[:-1] ** 3)
    tc = 0.5 * (s["te"][1:] + s["te"][:-1])
    worst_ = 0.0
    for i in np.where((rc >= 20) & (rc <= 100))[0]:
        for j in np.where((tc >= math.radians(10)) & (tc <= math.radians(80)))[0]:
            nd = dust_density(rc[i], tc[j], re[0])
            worst_ = max(worst_, abs(s["q"][i, j] / nd - 1))
    return worst_


e5 = ka5_err("M490_absorb_uniform_medium")
check("KA5", e5 is not None and e5 <= 0.05, f"ballistic focusing density, r 20-100, psi 10-80 deg (M 490, ABSORB, medium): max rel {e5}")

# ------------------------------------------------------------------ graded runs
BRACKETS = ["M234_transmit_uniform_medium", "M490_transmit_uniform_medium", "M234_absorb_uniform_medium",
            "M490_absorb_uniform_medium", "M234_reflect_uniform_medium", "M490_reflect_uniform_coarse",
            "M234_transmit_hedgehog_coarse"]
LADDER = [("M234_transmit_uniform_coarse", "M234_transmit_uniform_medium"),
          ("M490_transmit_uniform_coarse", "M490_transmit_uniform_medium"),
          ("M234_absorb_uniform_coarse", "M234_absorb_uniform_medium"),
          ("M490_absorb_uniform_coarse", "M490_absorb_uniform_medium"),
          ("M234_reflect_uniform_coarse", "M234_reflect_uniform_medium")]
RES["brackets"] = {}
steady_all = True
missing = [b for b in BRACKETS if load(b) is None]
if missing:
    P(f"missing bracket runs: {missing}")
for b in BRACKETS:
    snaps = load(b)
    if snaps is None:
        continue
    per = {}
    for use_qB in (False, True):
        hist = [worst(grade_snap(s_, use_qB)) for s_ in snaps]
        fin = hist[-1]
        env = {k: max(h[k] for h in hist) for k in GKEYS}
        chg = max(abs(h[k] / fin[k] - 1) if fin[k] > 0 else 0.0 for h in hist for k in GKEYS)
        steady = chg <= 0.05
        steady_all &= steady
        rows = grade_snap(snaps[-1], use_qB)
        per["qB" if use_qB else "q"] = dict(final=fin, envelope=env, max_change_last20=chg, steady=steady,
                                            graded=(fin if steady else env), rows=rows)
    RES["brackets"][b] = per
    for k_ in ("q", "qB"):
        g = per[k_]["graded"]
        P(f"[{b} {k_}] {'steady' if per[k_]['steady'] else 'NOT STEADY'} (chg {per[k_]['max_change_last20']:.2e}): "
          + ", ".join(f"{k} {g[k]:.3g}" for k in GKEYS))
    r0 = per["q"]["rows"][0]
    P(f"   e.g. {r0['foot']} L {r0['Lstar']} V {r0['V'] / 1e3:.0f}: hedgehog/bound Earth {r0['hh_Earth']:.3g} Mars {r0['hh_Mars']:.3g} "
      f"Saturn {r0['hh_Saturn']:.3g}; moving G1 Earth {r0['G1_Earth']:.3g} Mars {r0['G1_Mars']:.3g} Saturn {r0['G1_Saturn']:.3g}; "
      f"radial mean Earth {r0['radial_mean_Earth']:.3g} m/s^2")

# convergence
conv_ok = True; conv_rep = {}
for c_, m_ in LADDER:
    sc, sm = load(c_), load(m_)
    if sc is None or sm is None:
        conv_ok = False; conv_rep[m_] = "missing"; continue
    wc, wm = worst(grade_snap(sc[-1])), worst(grade_snap(sm[-1]))
    ch = max(abs(wc[k] / wm[k] - 1) if wm[k] > 0 else 0 for k in GKEYS)
    flip = any((wc[k] > 1) != (wm[k] > 1) for k in GKEYS)
    conv_rep[m_] = dict(max_rel_change=ch, flip=flip, coarse=wc, medium=wm)
    conv_ok &= (ch <= 0.30) and not flip
    P(f"ladder {m_}: max rel change coarse->medium {ch:.3f}, label flip {flip}")
RES["convergence"] = conv_rep
check("CONV", conv_ok, "every graded ratio within 30 % coarse vs medium, no label flip")

# hedgehog start vs uniform start
hs, us = load("M234_transmit_hedgehog_coarse"), load("M234_transmit_uniform_coarse")
if hs and us:
    wh, wu = worst(grade_snap(hs[-1])), worst(grade_snap(us[-1]))
    RES["start_compare"] = dict(hedgehog=wh, uniform=wu)
    P("start compare (coarse transmit M234) hedgehog vs uniform: " + ", ".join(f"{k} {wh[k]:.3g}/{wu[k]:.3g}" for k in GKEYS))

# MUTATE
mu, mn = load("M234_transmit_uniform_coarse_MUTATE"), us
if mu and mn:
    rm_ = grade_snap(mu[-1]); rn_ = grade_snap(mn[-1])
    sgn_m = np.sign(rm_[0]["radial_mean_Earth"]); sgn_n = np.sign(rn_[0]["radial_mean_Earth"])
    big = max(r["G1_Earth"] for r in rm_)
    e5m = ka5_err("M234_transmit_uniform_coarse_MUTATE")
    bite = (big > 0.1 and sgn_m != sgn_n) or (e5m is not None and e5m > 0.5)
    check("MUTATE", bite, f"repulsive Sun: G1 Earth max {big:.3g} of bound, radial sign {sgn_m:+.0f} vs main {sgn_n:+.0f}; "
          f"focusing density error {e5m}")
else:
    check("MUTATE", False, "runs missing")

# S1
s1 = json.load(open(os.path.join(HERE, "s1.json")))
check("S1", all(c["ok"] for c in s1["checks"].values()), "s1.json all PASS")

# ------------------------------------------------------------------ label
over_cell = {}
for b, per in RES["brackets"].items():
    for k_ in ("q", "qB"):
        snap_rows = per[k_]["rows"]
        hist_ok = per[k_]["steady"]
        for r in snap_rows:
            key = (r["foot"], r["Lstar"], r["V"])
            vals = [r[k] for k in GKEYS]
            if not hist_ok:                                  # envelope scale: inflate by the worst-run change
                vals = [x_ * (1 + per[k_]["max_change_last20"]) for x_ in vals]
            over_cell.setdefault(key, []).append(max(vals) > 1)
all_under = all(not any(v) for v in over_cell.values())
some_all_over = any(all(v) for v in over_cell.values())
kas = all(RES["checks"][k]["ok"] for k in ("KA3", "KA4", "KA5", "MUTATE", "S1", "CONV"))
complete = not missing
if not kas or not complete:
    label = "NO VERDICT"
elif all_under:
    label = "PASS (scoped)"
elif some_all_over:
    label = "FAIL"
else:
    label = "UNDECIDED"
RES["label"] = label; RES["steady_all"] = steady_all; RES["missing"] = missing
RES["worst_over_brackets"] = {k: max(per[k_]["graded"][k] for per in RES["brackets"].values() for k_ in ("q", "qB")) for k in GKEYS} if RES["brackets"] else {}
P(f"worst over every bracket (ratio to line): {RES['worst_over_brackets']}")
P(f"LABEL: {label}{'' if steady_all else ' (some runs NOT STEADY: envelopes graded)'}  kappa = 1/2 FITTED; not theory closed")
json.dump(RES, open(os.path.join(HERE, "GRADE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "grade.out"), "w").write("\n".join(OUT) + "\n")
