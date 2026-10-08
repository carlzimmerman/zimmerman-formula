#!/usr/bin/env python3
"""CFG450: at what radius does the CFG382 target audit read the X-COP gas mass?  (criteria: FROZEN_CRITERIA.md, 850262705)

U1 units from the FITS headers, U2 NFW / f_gas cross-check, then the definition-A deficits with gas at the JSON R500
(b = 0, 0.3; canonical 9.3603e-11 and alt 1.1312e-10, never pooled), propagated to T15, T16 and CFG431.
Read-only on CFG382, CFG431 and deepseek_push.  Run: python3 cfg450_gas_radius_audit.py  |  CFG450_MUTATE=1 plants the Mpc read.
Local data only; no network.
"""
import json, math, os, re, sys
import numpy as np
from astropy.io import fits

MUT = os.environ.get("CFG450_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG4_common as C4  # noqa: E402  (read-only: nu_mono, as the target audit uses)

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
BS = (0.0, 0.3)
COSMIC = 5.364
Gcgs, MSUN, KPC = 6.674e-8, 1.989e33, 3.0857e21
lines = []
def say(s=""):
    lines.append(s); print(s)

def defA(Mhse, Mb, b, Rk, a0_si):
    gN = Gcgs * Mb * MSUN / (Rk * KPC) ** 2
    Mph = (C4.nu_mono(np.array([gN / (a0_si * 100)]))[0] - 1) * Mb
    return (Mhse / (1 - b) - Mb - Mph) / (COSMIC * Mb)

# ------------------------------------------------------------------ U1 / U2
xdir = os.path.join(REPO, "real_research", "data", "xcop")
r5 = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
names = sorted(n for n in os.listdir(xdir) if os.path.isdir(os.path.join(xdir, n)))
units, u1_r500, u2 = {}, {}, {}
say(f"CFG450 X-COP gas-radius audit  MUTATE={MUT}")
say("")
say("U1/U2 per cluster: RADIUS unit | header R500 vs JSON | M_NFW(fgas, RADIUS=1)/M_NFW(hydro, R500_json) | f_gas(RADIUS=1)")
for nm in names:
    F = fits.open(os.path.join(xdir, nm, f"{nm}_fgas_profile.fits"))["FGAS"]
    hm = fits.open(os.path.join(xdir, nm, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data
    units[nm] = str(F.columns["RADIUS"].unit).strip()
    rh, rj = float(F.header["R500"]), r5[nm]["R500"] * 1000
    u1_r500[nm] = rh / rj - 1
    r = np.asarray(F.data["RADIUS"], float)
    m1 = math.exp(np.interp(0.0, np.log(r), np.log(np.asarray(F.data["M_NFW"], float))))
    mh = float(np.interp(rj, np.asarray(hm["RADIUS"], float), np.asarray(hm["M_NFW"], float)))
    f1 = float(np.interp(1.0, r, np.asarray(F.data["FGAS"], float)))
    u2[nm] = (m1 / mh, f1)
    say(f"  {nm:8s} {units[nm]:7s} {rh:7.1f} vs {rj:7.1f} kpc ({u1_r500[nm]:+.2%})  ratio {m1/mh:.4f}  f_gas {f1:.3f}")
if all(u == "R/R500" for u in units.values()) and all(abs(v) <= 0.02 for v in u1_r500.values()):
    U1 = "R/R500"
elif any(u.lower() in ("mpc", "kpc") for u in units.values()):
    U1 = "LENGTH"
else:
    U1 = "UNDETERMINED"
U2 = all(abs(v[0] - 1) <= 0.02 and 0.08 <= v[1] <= 0.20 for v in u2.values())
verdict_u = {"R/R500": "NOT A BUG (RADIUS = 1 is R500)", "LENGTH": "BUG (RADIUS = 1 is a fixed length)"}.get(U1, "UNDETERMINED")
if U1 == "R/R500" and not U2:
    verdict_u = "UNDETERMINED (U2 failed)"
say(f"U1 = {U1}; U2 = {'PASS' if U2 else 'FAIL'}  ->  {verdict_u}")
say("")

# ------------------------------------------------------------------ clusters + groups
CL = []
for nm in names:
    d = os.path.join(xdir, nm)
    if nm not in r5 or not os.path.exists(os.path.join(d, f"{nm}_mstar.fits")):
        continue
    hm = fits.open(os.path.join(d, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data
    F = fits.open(os.path.join(d, f"{nm}_fgas_profile.fits"))["FGAS"]
    ms = fits.open(os.path.join(d, f"{nm}_mstar.fits"))["MSTAR_SMOOTHED"].data
    Rk = r5[nm]["R500"] * 1000
    lr, lmg = np.log(np.asarray(F.data["RADIUS"], float)), np.log(np.asarray(F.data["MGAS"], float))
    x_true = Rk / float(F.header["R500"]) if U1 == "R/R500" else Rk / 1000   # gas at the JSON R500
    x_mpc = Rk / 1000                                                          # CFG431 R2 / MUTATE: RADIUS read as Mpc
    CL.append(dict(name=nm, R=Rk,
                   M=float(np.interp(Rk, np.asarray(hm["RADIUS"], float), np.asarray(hm["M_FORW"], float))),
                   Mg_audit=float(np.exp(np.interp(0.0, lr, lmg))),
                   Mg_R500=float(np.exp(np.interp(math.log(x_mpc if MUT else x_true), lr, lmg))),
                   Mg_R2=float(np.exp(np.interp(math.log(x_mpc), lr, lmg))),
                   R2_read_over_R500=(x_mpc * float(F.header["R500"]) / Rk) if U1 == "R/R500" else 1.0,   # radius R2 read, in JSON-R500 units
                   Ms=float(np.exp(np.interp(np.log(Rk), np.log(np.asarray(ms["RADIUS"], float)), np.log(np.asarray(ms["MSTAR"], float)))))))
def cl_e(b, a0, gas="Mg_R500"):
    return np.array([defA(c["M"], c[gas] + c["Ms"], b, c["R"], a0) for c in CL])

rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")) if not l.startswith("#")]
hdr, rows = rows[0], [x for x in rows[1:] if len(x) > 5]
GRP = [dict(R=float(x[hdr.index("R500_kpc")]), M=float(x[hdr.index("M500_1e13")]) * 1e13, Mg=float(x[hdr.index("Mgas500_1e12")]) * 1e12) for x in rows]
def grp_e(b, a0):
    return np.array([defA(g["M"], 1.10 * g["Mg"], b, g["R"], a0) for g in GRP])

checks = {}
c1 = (abs(np.median(cl_e(0.0, A0["canonical"], "Mg_audit")) - 0.413) < 0.002 and abs(np.median(cl_e(0.3, A0["canonical"], "Mg_audit")) - 0.905) < 0.002
      and abs(np.median(grp_e(0.0, A0["canonical"])) - 0.787) < 0.002 and abs(np.median(grp_e(0.3, A0["canonical"])) - 1.760) < 0.002 and len(CL) == 7)
checks["C1_cfg382_reproduction"] = bool(c1)
e_R2 = float(np.median(cl_e(0.0, A0["canonical"], "Mg_R2")))
checks["C2_cfg431_R2_reproduction"] = bool(abs(e_R2 - 0.225) < 0.002)

def q(a):
    return dict(med=float(np.median(a)), p16=float(np.percentile(a, 16)), p84=float(np.percentile(a, 84)))
DEF = {}
say("Definition-A deficits (median [16-84%]); gas " + ("read as Mpc (MUTATE)" if MUT else "at the JSON R500") + "; never pooled across footings:")
for fk, a0 in A0.items():
    DEF[fk] = {}
    for b in BS:
        cA, cN, g = q(cl_e(b, a0, "Mg_audit")), q(cl_e(b, a0)), q(grp_e(b, a0))
        DEF[fk][str(b)] = dict(clusters_audit=cA, clusters_R500=cN, groups=g)
        say(f"  {fk:9s} a0 {a0:.4e}  b = {b:.1f}: clusters audit-read {cA['med']:.4f} -> R500 {cN['med']:.4f} [{cN['p16']:.3f}-{cN['p84']:.3f}]"
            f"   groups {g['med']:.4f} [{g['p16']:.3f}-{g['p84']:.3f}]")
moves = max(abs(DEF["canonical"][str(b)]["clusters_R500"]["med"] - DEF["canonical"][str(b)]["clusters_audit"]["med"]) for b in BS)
decision = "MOVES" if moves > 0.02 else "UNCHANGED"
say(f"Movement (canonical, max over b): {moves:.2e}  ->  {decision}")
say("")
say("CFG431 R2 read (RADIUS taken as Mpc): effective radius in R500 units per cluster: "
    + ", ".join(f"{c['name']} {c['R2_read_over_R500']:.3f}" for c in CL) + f"; cluster e_med {e_R2:.3f}")
say("")

# ------------------------------------------------------------------ T15 / T16 (formulas copied, conventions held)
G, A0_T = 6.674e-11, 1.2e-10
GYR = 3.156e16; TAU = 10.3 * GYR; LAM = 0.028; RHO = 1.55e-24
F_R500 = 1 - math.exp(-LAM * math.sqrt(4 * math.pi * G * RHO) * TAU)
RATE = math.sqrt(4 * math.pi * G * RHO) * TAU
def S_of_R(Mb, R, a0=A0_T):
    return 1.0 / (math.exp(math.sqrt(G * Mb * 1.989e30 / a0) / 3.086e19 / R) - 1.0)
def lam_from_f(f):
    return -math.log(1 - f) / RATE if f < 0.999 else 1e9
def t15(xg0, xg3, xc0, xc3, a0=A0_T):
    Sg, Sc = S_of_R(6e12, 554.0, a0), S_of_R(2.8e13, 985.0, a0)
    rows_ = {"groups_b0": xg0 - F_R500 * Sg, "groups_b03": xg3 - F_R500 * Sg, "clusters_b0": xc0 - F_R500 * Sc, "clusters_b03": xc3 - F_R500 * Sc}
    ceil = {"groups": [xg0 / Sg, lam_from_f(xg0 / Sg)], "clusters": [xc0 / Sc, lam_from_f(xc0 / Sc)]}
    res = {"groups": [xg0 / Sg, xg3 / Sg], "clusters": [xc0 / Sc, xc3 / Sc]}
    return dict(rows=rows_, ceil=ceil, res=res, viol=0.029 / ceil["clusters"][1])
def t16(xg0, xg3, xc0, xc3, mwwin, a0=A0_T):
    Sg, Sc = S_of_R(6e12, 554.0, a0), S_of_R(2.8e13, 985.0, a0)
    lm = lambda x, S: -math.log(1 - x / S) / RATE if x < S else math.inf
    win = {"mw": list(mwwin), "groups": [lm(xg0, Sg), lm(xg3, Sg)], "clusters": [lm(xc0, Sc), lm(xc3, Sc)]}
    lo = max(w[0] for w in win.values()); hi = min(w[1] for w in win.values())
    return dict(windows=win, inter=[lo, hi], nonempty=lo <= hi, gap_floor_cl=0.028 / win["clusters"][1])

DS = os.path.join(REPO, "deepseek_push", "openai_math_cross_analysis_2026-10")
T15J = json.load(open(os.path.join(DS, "t15_cold_budget", "t15_results.json")))
T16J = json.load(open(os.path.join(DS, "t16_coupling_gradient", "t16_results.json")))
o15, o16 = t15(0.79, 1.76, 0.41, 0.91), t16(0.79, 1.76, 0.41, 0.91, T16J["windows"]["mw"])
err = [abs(o15["rows"][k] - T15J["rows"][k]) for k in o15["rows"]]
err += [abs(a - b) for k in ("groups", "clusters") for a, b in zip(o15["ceil"][k], T15J["ceil"][k])]
err += [abs(a - b) for k in ("groups", "clusters") for a, b in zip(o15["res"][k], T15J["res"][k])] + [abs(o15["viol"] - T15J["viol"])]
err += [abs(a - b) for k in ("groups", "clusters") for a, b in zip(o16["windows"][k], T16J["windows"][k])]
err += [abs(a - b) for a, b in zip(o16["inter"], T16J["inter"])] + [abs(o16["gap_floor_cl"] - T16J["gap_floor_cl"])]
checks["C3_t15_t16_reproduction"] = bool(max(err) < 1e-9)

PROP = {"original": dict(T15=o15, T16=o16)}
say("T15/T16 with the recomputed deficits (their other conventions held: a0 1.2e-10 in S, f_law 0.286, lambda floor 0.028):")
def show(lab, r15, r16):
    say(f"  {lab}")
    say("     T15 M_cold/M_b: " + "  ".join(f"{k} {v:+.3f}" for k, v in r15["rows"].items())
        + f" | f_max cl {r15['ceil']['clusters'][0]:.4f} (lam_max {r15['ceil']['clusters'][1]:.5f}) gr {r15['ceil']['groups'][0]:.4f}"
        + f" | f_res cl [{r15['res']['clusters'][0]:.4f}, {r15['res']['clusters'][1]:.4f}] | C5 violation {r15['viol']:.2f}x")
    w = r16["windows"]
    say(f"     T16 windows groups [{w['groups'][0]:.4f}, {w['groups'][1]:.4f}] clusters [{w['clusters'][0]:.4f}, {w['clusters'][1]:.4f}]"
        f" | intersection [{r16['inter'][0]:.4f}, {r16['inter'][1]:.4f}] nonempty {r16['nonempty']} | floor/cluster gap {r16['gap_floor_cl']:.2f}x")
show("original inputs 0.79/1.76, 0.41/0.91 (as committed)", o15, o16)
for fk, a0 in A0.items():
    xs = [DEF[fk]["0.0"]["groups"]["med"], DEF[fk]["0.3"]["groups"]["med"], DEF[fk]["0.0"]["clusters_R500"]["med"], DEF[fk]["0.3"]["clusters_R500"]["med"]]
    r15, r16 = t15(*xs), t16(*xs, T16J["windows"]["mw"])
    r15s, r16s = t15(*xs, a0=a0), t16(*xs, T16J["windows"]["mw"], a0=a0)
    PROP[fk] = dict(inputs=xs, T15=r15, T16=r16, T15_S_matched=r15s, T16_S_matched=r16s)
    show(f"{fk} deficits {xs[0]:.3f}/{xs[1]:.3f}, {xs[2]:.3f}/{xs[3]:.3f}; S at 1.2e-10 (as T15/T16)", r15, r16)
    show(f"{fk} deficits, S at the matching a0 {a0:.4e} (disclosed row; MW window held at T16's)", r15s, r16s)
say("")

# ------------------------------------------------------------------ CFG431 (estimator copied verbatim)
NB, SEED = 4000, 431
COSMIC431 = 0.1200 / 0.02237
tex = open(os.path.join(EXT, "alabi2017", "src", "halov3.tex")).read()
num = lambda s: re.sub(r"[^0-9.\-]", "", s.split("^")[0].split("_")[0])
t1 = {}
for line in tex.split("\\begin{table*}")[1].split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 12 and re.match(r"^\$?\s*\d{3,4}", c[0]):
        try: t1[num(c[0])] = (float(num(c[9])), float(num(c[10])))
        except ValueError: pass
t2 = {}
for line in (tex.split("\\begin{table*}")[2] + tex.split("\\begin{table*}")[3]).split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 6 and re.match(r"^\$\s*\d{3,4}\s*\$", c[0]) and re.match(r"^\$\s*0\s*\$", c[1]):
        mt, emt = [float(v) for v in c[4].strip("$").split("\\pm")]
        fd, efd = [float(v) for v in c[5].strip("$").split("\\pm")]
        t2[num(c[0])] = (mt * 1e11, fd, emt * 1e11, efd)
CENTRALS = ("4486", "4472", "1399", "1316", "4374", "4649", "5846", "1407", "4636")
GAL = [n for n in sorted(set(t1) & set(t2)) if n not in CENTRALS]
def gal_e(a0):
    out = []
    for n in GAL:
        Re, (mt, f_) = t1[n][0], t2[n][:2]
        Ms = max(1 - f_, 0.05) * mt
        y = G * Ms * 1.989e30 / (5 * Re * 3.0857e19) ** 2 / a0
        out.append((mt - math.sqrt(1 + 1 / y) * Ms) / (COSMIC431 * Ms))
    return np.array(out)
def S_of(e):
    em = float(np.median(e)); se = (np.percentile(e, 84) - np.percentile(e, 16)) / 2
    if not (0 < em < 1):
        return math.inf, em, se
    return se / (em * abs(math.log(em))), em, se
def boot_dln(e, rng):
    lnS = []
    n = len(e)
    for _ in range(NB):
        s = S_of(e[rng.integers(0, n, n)])[0]
        lnS.append(math.log(s) if (math.isfinite(s) and s > 0) else math.inf)
    lnS = np.sort(np.array(lnS))
    p16, p84 = lnS[int(0.16 * NB)], lnS[int(0.84 * NB)]
    return (p84 - p16) / 2 if math.isfinite(p84) else math.inf
def run_row(label, ebc):
    rng = np.random.default_rng(SEED)
    cls = {}
    for k in ("galaxy", "group", "cluster"):
        S, em, se = S_of(ebc[k]); cls[k] = dict(S=S, dln=boot_dln(ebc[k], rng), e_med=em, sigma_e=float(se))
    ks = [k for k in cls if math.isfinite(cls[k]["S"])]
    pairs = {f"{a}-{b}": abs(math.log(cls[a]["S"]) - math.log(cls[b]["S"])) / math.hypot(cls[a]["dln"], cls[b]["dln"])
             for i, a in enumerate(sorted(ks)) for b in sorted(ks)[i + 1:]}
    lab = "NOT UNIVERSAL" if any(z >= 2 for z in pairs.values()) else ("UNIVERSAL" if all(cls[k]["dln"] <= 0.35 for k in ks) else "CONSISTENT, NOT DIAGNOSTIC")
    say(f"  {label}: " + "  ".join(f"{k} e {v['e_med']:.3f} S {v['S']:.3f}" for k, v in cls.items())
        + " | " + "; ".join(f"{p} z {z:.2f}" for p, z in pairs.items()) + f" -> {lab}")
    return dict(classes=cls, pairs=pairs, verdict=lab)
say("CFG431 rows (definition A, b = 0):")
C431 = {}
C431["primary_as_committed"] = run_row("primary as committed (gas audit-read, canonical)", dict(galaxy=gal_e(A0["canonical"]), group=grp_e(0.0, A0["canonical"]), cluster=cl_e(0.0, A0["canonical"], "Mg_audit")))
C431["primary_gas_R500"] = run_row("primary, gas at JSON R500 (canonical)", dict(galaxy=gal_e(A0["canonical"]), group=grp_e(0.0, A0["canonical"]), cluster=cl_e(0.0, A0["canonical"])))
C431["R1_full_alt"] = run_row("R1-full alt (galaxies + groups + clusters at 1.1312e-10, gas at R500)", dict(galaxy=gal_e(A0["alt"]), group=grp_e(0.0, A0["alt"]), cluster=cl_e(0.0, A0["alt"])))
C431["R2_as_committed"] = run_row("R2 as committed (gas at RADIUS = R500 in Mpc, i.e. outside R500)", dict(galaxy=gal_e(A0["canonical"]), group=grp_e(0.0, A0["canonical"]), cluster=cl_e(0.0, A0["canonical"], "Mg_R2")))
say("")

if MUT:
    checks["MUTATE_flips"] = bool(decision == "MOVES")
say("checks: " + json.dumps(checks))
say(f"VERDICT: {verdict_u}; deficits {decision} (canonical max shift {moves:.2e}). "
    + ("CFG431 R2 read the gas outside R500 and is invalid." if U1 == "R/R500" else ""))
json.dump(dict(mutate=MUT, U1=U1, U2=U2, units=units, r500_header_vs_json=u1_r500, u2={k: list(v) for k, v in u2.items()},
               verdict_units=verdict_u, decision=decision, max_shift=moves, deficits=DEF,
               R2_read_over_R500={c["name"]: c["R2_read_over_R500"] for c in CL}, R2_e_med=e_R2,
               propagation=PROP, cfg431=C431, checks=checks),
          open(os.path.join(HERE, f"cfg450_results{TAG}.json"), "w"), indent=1, default=float)
ok = all(checks.values())
print("<LANE> COMPLETE: all checks PASS" if ok else "<LANE> COMPLETE: -- SOME CHECKS FAIL")
sys.exit(0 if ok else 1)
