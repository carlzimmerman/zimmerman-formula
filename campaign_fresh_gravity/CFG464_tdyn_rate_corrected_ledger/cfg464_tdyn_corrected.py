#!/usr/bin/env python3
"""CFG464: the zero-constant t_dyn settling rate (Gamma = lambda/t_dyn, lambda = 1) on the CORRECTED cold-budget ledger.
(criteria: FROZEN_CRITERIA.md, bbecbb93c)  Supersedes CFG429's verdict; CFG429 is not edited.

Ledger (T15): M_cold/M_b = x - f S/M_b,  f = 1 - exp(-lambda sqrt(4 pi G rho) tau),  S/M_b = 1/(exp(r_t/R) - 1),  r_t = sqrt(G M_b/a0).
Corrections vs CFG429: groups/clusters use T15's own x = (M_tot - M_b)/M_b per object (CFG453; gas at the JSON R500, CFG450);
the MW-30 row uses ONE baryon mass per row (7e10 and 1e11 both reported; the 10-08 audit a2); both a0 footings, never pooled.
Run: python3 cfg464_tdyn_corrected.py  |  CFG464_MUTATE=1 plants x := x_A (def A) with lambda = the cluster ceiling.  Local data only.
"""
import json, math, os, re, sys
import numpy as np
from astropy.io import fits

MUT = os.environ.get("CFG464_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
sys.path.insert(0, CFG)
import CFG4_common as C4  # noqa: E402  (read-only: nu_mono, as the CFG382 audit and CFG453 use)

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0_T15 = 1.2e-10          # T15/CFG429's value: reference only, not a footing
BS = (0.0, 0.3)
COSMIC = 5.364
G, MSUN, KPC, GYR = 6.674e-11, 1.989e30, 3.086e19, 3.156e16
TAU = 10.3 * GYR
RHO_R500 = 1.55e-24       # T15's R500 local density (held)
LAM1 = 1.0                # zero constants
LAM_T15_CEIL = 0.0073     # T15's committed cluster ceiling (as CFG429's MUTATE)
MW_MB = (7.0e10, 1.0e11)
MW_V = (188, 200, 230)
lines = []
def say(s=""):
    lines.append(s); print(s)

def S_of_R(Mb, R_kpc, a0):
    return 1.0 / (math.exp(math.sqrt(G * Mb * MSUN / a0) / KPC / R_kpc) - 1.0)
def f_of(lam, rho):
    return 1.0 - math.exp(-lam * math.sqrt(4 * math.pi * G * rho) * TAU)
def rho30(V, R=30.0):
    return (V * 1e3) ** 2 / (4 * math.pi * G * (R * KPC) ** 2)
def x_mw(V, Mb, R=30.0):
    return (V * 1e3) ** 2 * R * KPC / G / (Mb * MSUN) - 1.0

# ------------------------------------------------------------------ objects: CFG453's read verbatim (gas at the JSON R500, CFG450)
Gcgs, MSUN_CGS, KPC_CGS = 6.674e-8, 1.989e33, 3.0857e21
xdir = os.path.join(REPO, "real_research", "data", "xcop")
r5 = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
CL = []
for nm in sorted(os.listdir(xdir)):
    d = os.path.join(xdir, nm)
    if not os.path.isdir(d) or nm not in r5 or not os.path.exists(os.path.join(d, f"{nm}_mstar.fits")):
        continue
    hm = fits.open(os.path.join(d, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data
    F = fits.open(os.path.join(d, f"{nm}_fgas_profile.fits"))["FGAS"]
    ms = fits.open(os.path.join(d, f"{nm}_mstar.fits"))["MSTAR_SMOOTHED"].data
    Rk = r5[nm]["R500"] * 1000
    Mg = float(np.exp(np.interp(math.log(Rk / float(F.header["R500"])), np.log(np.asarray(F.data["RADIUS"], float)), np.log(np.asarray(F.data["MGAS"], float)))))
    Ms = float(np.exp(np.interp(np.log(Rk), np.log(np.asarray(ms["RADIUS"], float)), np.log(np.asarray(ms["MSTAR"], float)))))
    CL.append(dict(name=nm, R=Rk, M=float(np.interp(Rk, np.asarray(hm["RADIUS"], float), np.asarray(hm["M_FORW"], float))), Mb=Mg + Ms))
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")) if not l.startswith("#")]
hdr, rows = rows[0], [x for x in rows[1:] if len(x) > 5]
GRP = [dict(name=x[hdr.index("name")], R=float(x[hdr.index("R500_kpc")]), M=float(x[hdr.index("M500_1e13")]) * 1e13,
            Mb=1.10 * float(x[hdr.index("Mgas500_1e12")]) * 1e12) for x in rows]

def per_object(objs, b, a0):
    out = []
    for o in objs:
        Mt = o["M"] / (1 - b)
        gN = Gcgs * o["Mb"] * MSUN_CGS / (o["R"] * KPC_CGS) ** 2
        nu = float(C4.nu_mono(np.array([gN / (a0 * 100)]))[0])
        out.append(dict(name=o["name"], Mb=o["Mb"], R=o["R"], nu=nu, xA=(Mt - o["Mb"] - (nu - 1) * o["Mb"]) / (COSMIC * o["Mb"]), xT=(Mt - o["Mb"]) / o["Mb"]))
    return out

def objects(a0):
    return {b: dict(gr=per_object(GRP, b, a0), cl=per_object(CL, b, a0)) for b in BS}

def med(L, k):
    return float(np.median([o[k] for o in L]))

def gc_rows(lam, a0, P, key="xT"):
    """8 group/cluster rows: (i) T15 conventions, (ii) per-object S (median of x_i - f S_i)."""
    fR = f_of(lam, RHO_R500)
    Sg, Sc = S_of_R(6e12, 554.0, a0), S_of_R(2.8e13, 985.0, a0)
    ri, rii, nneg, worst = {}, {}, {}, {}
    for b in BS:
        bl = "0" if b == 0 else "03"
        for cls, kk, S in (("groups", "gr", Sg), ("clusters", "cl", Sc)):
            L = P[b][kk]
            ri[f"{cls}_b{bl}"] = med(L, key) - fR * S
            m = [o[key] - fR * S_of_R(o["Mb"], o["R"], a0) for o in L]
            rii[f"{cls}_b{bl}"] = float(np.median(m))
            nneg[f"{cls}_b{bl}"] = [int(sum(v < 0 for v in m)), len(m)]
            j = int(np.argmin(m)); worst[f"{cls}_b{bl}"] = [L[j]["name"], float(m[j])]
    return dict(f=fR, S_i=dict(groups=Sg, clusters=Sc), i=ri, ii=rii, nneg_ii=nneg, worst_ii=worst)

def mw_rows(lam, a0, Mb):
    S = S_of_R(Mb, 30.0, a0)
    r = {f"V{V}": dict(x=x_mw(V, Mb), S=S, f=f_of(lam, rho30(V)), Mcold=x_mw(V, Mb) - f_of(lam, rho30(V)) * S) for V in MW_V}
    g = lambda V: x_mw(V, Mb) - f_of(lam, rho30(V)) * S
    lo, hi = 100.0, 400.0
    for _ in range(100):
        m = 0.5 * (lo + hi)
        if g(m) < 0: lo = m
        else: hi = m
    signs = [r[f"V{V}"]["Mcold"] >= 0 for V in MW_V]
    lab = "robust-positive" if all(signs) else ("robust-negative" if not any(signs) else "speed-dependent")
    return dict(rows=r, V0=0.5 * (lo + hi), label=lab, tension_V188=bool(r["V188"]["Mcold"] < 0))

checks = {}
say(f"CFG464 zero-constant t_dyn settling rate on the corrected ledger  MUTATE={MUT}")
say(f"ledger: M_cold/M_b = x - f S/M_b;  f = 1 - exp(-lambda sqrt(4 pi G rho) tau), tau 10.3 Gyr, rho_R500 {RHO_R500:.2e} kg/m^3 (T15)")
say("x: groups/clusters T15's own (M_tot - M_b)/M_b per object (CFG453 read, gas at JSON R500); MW-30 one M_b per row")
say("")

C453 = json.load(open(os.path.join(CFG, "CFG453_t15_deficit_units", "cfg453_results.json")))
A2 = json.load(open(os.path.join(CFG, "AUDIT_data_and_assumptions_2026-10-08", "a2_cfg429_rescore.json")))
D450 = json.load(open(os.path.join(CFG, "CFG450_xcop_gas_radius_audit", "cfg450_results.json")))["deficits"]
C451 = json.load(open(os.path.join(CFG, "CFG451_t15_t16_own_footings", "cfg451_results.json")))["rows"]

KEY = "xA" if MUT else "xT"     # MUTATE plants CFG429's misread: x := x_A (definition A)
if MUT:
    say("MUTATE: planted x := x_A (CFG382 definition A) for groups/clusters -- the CFG429 misread")
    say("")
OUT, c1, c2, c3, c5 = {}, [], [], [], []
for fk, a0 in A0.items():
    P = objects(a0)
    # C1 / C2 (on the true ledger, both modes)
    for kk in ("gr", "cl"):
        c1 += [abs(med(P[b][kk], "xT") - C453["D1"][fk]["xT"][kk][i]) for i, b in enumerate(BS)]
    g028 = gc_rows(0.028, a0, P, "xT")
    c2 += [abs(g028[conv][k] - C453["D2"][fk][conv]["rows"][k]) for conv in ("i", "ii") for k in g028[conv]]
    gc = gc_rows(LAM1, a0, P, KEY)
    mw = {f"{Mb:.0e}": mw_rows(LAM1, a0, Mb) for Mb in MW_MB}
    legacy = {f"V{V}": x_mw(V, 1e11) - f_of(LAM1, rho30(V)) * S_of_R(7e10, 30.0, a0) for V in MW_V}
    c5 += [gc["f"]] + [r["f"] for m in mw.values() for r in m["rows"].values()]
    if not MUT:   # C3: the audit's a2 re-score (f = 1, rounded x)
        a2 = A2[f"{a0:.4e}"]
        c3 += [abs(gc["i"][k] - a2[k]["Mcold_T15_definition"]) for k in gc["i"]]
        c3 += [abs(mw[f"{Mb:.0e}"]["rows"][f"V{V}"]["Mcold"] - a2[f"MW30_V{V} consistent M_b {Mb:.0e}".replace("e+", "e")]["Mcold"]) for Mb in MW_MB for V in (188, 200)]
    gcv = list(gc["i"].values()) + list(gc["ii"].values())
    any_feas, all_feas = any(v >= 0 for v in gcv), all(v >= 0 for v in gcv)
    mw_rneg = all(m["label"] == "robust-negative" for m in mw.values())
    verdict = "NOT EXCLUDED" if any_feas else ("EXCLUDED" if mw_rneg else "MW-SPEED-DEPENDENT")
    rest = {}
    for kk, cls in (("cl", "clusters"), ("gr", "groups")):
        L = P[0.0][kk]
        dif = [S_of_R(o["Mb"], o["R"], a0) - (o["nu"] - 1) for o in L]
        rest[cls] = [float(np.median(dif)), float(max(abs(v) for v in dif))]
    say(f"{fk} footing (a0 {a0:.4e}), lambda = {LAM1:g}")
    say(f"  f(lambda=1): R500 {gc['f']:.6f} (at rho_R500/10: {f_of(LAM1, RHO_R500 / 10):.4f});  MW-30 {min(r['f'] for m in mw.values() for r in m['rows'].values()):.6f}")
    for conv, lab in (("i", "(i) T15 conventions"), ("ii", "(ii) per-object S")):
        Sx = (f"S/M_b groups {gc['S_i']['groups']:.3f} clusters {gc['S_i']['clusters']:.3f}" if conv == "i" else "median of x_i - f S_i")
        say(f"  {lab:22s} [{Sx}]: " + "  ".join(f"{k} {v:+.3f}" for k, v in gc[conv].items()))
    say("  per-object negatives (ii): " + "  ".join(f"{k} {v[0]}/{v[1]}" for k, v in gc["nneg_ii"].items())
        + ";  worst object: " + "  ".join(f"{k} {w[0]} {w[1]:+.2f}" for k, w in gc["worst_ii"].items()))
    bind = min(((v, f"{k} ({c})") for c in ("i", "ii") for k, v in gc[c].items()))
    say(f"  binding GC row: {bind[1]} = {bind[0]:+.3f}")
    say(f"  info: per-object S - (nu - 1) at b = 0, median / max|.|: clusters {rest['clusters'][0]:+.4f} / {rest['clusters'][1]:.4f}, groups {rest['groups'][0]:+.4f} / {rest['groups'][1]:.4f}"
        " (kernel supply vs the law's phantom: at f = 1, M_cold ~ x - (nu - 1) = 5.364 x_A, the beyond-law excess)")
    for Mb in MW_MB:
        m = mw[f"{Mb:.0e}"]
        say(f"  MW-30 M_b {Mb:.0e} throughout: " + "  ".join(f"V{V}: x {m['rows'][f'V{V}']['x']:.3f} S {m['rows'][f'V{V}']['S']:.3f} -> {m['rows'][f'V{V}']['Mcold']:+.3f}" for V in MW_V)
            + f";  V0 = {m['V0']:.1f} km/s; {m['label']}; V188 tension {m['tension_V188']}")
    say("  LEGACY (not scored) CFG429 mixed row, x at 1e11 / S at 7e10: " + "  ".join(f"{k} {v:+.3f}" for k, v in legacy.items()))
    say(f"  -> GC rows feasible {sum(v >= 0 for v in gcv)}/8;  MW robust-negative for both M_b: {mw_rneg};  VERDICT ({fk}): {verdict}")
    say("")
    OUT[fk] = dict(a0=a0, gc=gc, mw=mw, legacy_mixed_mw=legacy, S_minus_phantom_b0=rest, gc_feasible=[int(sum(v >= 0 for v in gcv)), 8],
                   any_feasible=any_feas, all_feasible=all_feas, mw_robust_negative_both=mw_rneg, verdict=verdict)

labels = {OUT[fk]["verdict"] for fk in A0}
overall = labels.pop() if len(labels) == 1 else "FOOTING-DEPENDENT"
if overall == "NOT EXCLUDED":
    overall += " (ROBUST: all 8 GC rows feasible on both footings)" if all(OUT[fk]["all_feasible"] for fk in A0) else " (PARTIAL)"

# ------------------------------------------------------------------ reference: T15's a0 = 1.2e-10 (not a footing; not scored)
Pr = objects(A0_T15)
gr = gc_rows(LAM1, A0_T15, Pr, KEY)
say(f"reference only (T15's a0 1.2e-10, not a footing): (i) " + "  ".join(f"{k} {v:+.3f}" for k, v in gr["i"].items())
    + ";  MW-30 V0 " + "  ".join(f"{Mb:.0e}: {mw_rows(LAM1, A0_T15, Mb)['V0']:.1f}" for Mb in MW_MB) + " km/s")

# ------------------------------------------------------------------ C4: CFG429's own inputs reproduce its committed rows
cfg429_out = open(os.path.join(CFG, "CFG429_tdyn_rate_zero_constant", "cfg429_tdyn.out")).read()
committed = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\s+(\S+)\s*:.*M_cold/M_b ([+-][0-9.]+)", cfg429_out, re.M)}
fR = f_of(LAM1, RHO_R500)
mine429 = {"MW30_V200": 1.80 - f_of(LAM1, rho30(200)) * S_of_R(7e10, 30.0, A0_T15),
           "groups_b0": 0.79 - fR * S_of_R(6e12, 554.0, A0_T15), "groups_b03": 1.76 - fR * S_of_R(6e12, 554.0, A0_T15),
           "clusters_b0": 0.41 - fR * S_of_R(2.8e13, 985.0, A0_T15), "clusters_b03": 0.91 - fR * S_of_R(2.8e13, 985.0, A0_T15)}
c4 = [abs(mine429[k] - committed[k]) for k in mine429] if set(committed) == set(mine429) else [1.0]

checks["C1_xT_medians_cfg453"] = bool(max(c1) < 1e-9)
checks["C2_cfg453_rows_lambda0.028"] = bool(max(c2) < 1e-9)
if not MUT:
    checks["C3_audit_a2_rows"] = bool(max(c3) < 2e-3)
checks["C4_cfg429_reproduced"] = bool(max(c4) < 0.005)
checks["C5_f_lambda1_ge_0.9999"] = bool(min(c5) >= 0.9999)
say(f"controls: C1 max |dxT| {max(c1):.1e};  C2 max |drow| {max(c2):.1e};" + (f"  C3 max |d a2| {max(c3):.1e};" if not MUT else "")
    + f"  C4 max |d CFG429| {max(c4):.4f};  C5 min f {min(c5):.6f}")

MOUT = {}
if MUT:
    # M1a: T15's committed conventions, x_A 0.41, lambda = 0.0073
    m1a = 0.41 - f_of(LAM_T15_CEIL, RHO_R500) * S_of_R(2.8e13, 985.0, A0_T15)
    # M1b: per footing, CFG450 x_A with CFG451's committed footing cluster ceiling
    m1b = {}
    for fk, a0 in A0.items():
        ref = next(v for k, v in C451.items() if k.startswith(fk))
        lam_c = ref["T15"]["ceil"]["clusters"][1]
        xa = D450[fk]["0.0"]["clusters_R500"]["med"]
        m1b[fk] = dict(lam_ceiling=lam_c, xA=xa, Mcold=xa - f_of(lam_c, RHO_R500) * S_of_R(2.8e13, 985.0, a0))
    # sensitivity: the corrected ledger at lambda = 0.0073 (expected all positive: no ceiling there)
    sens = {fk: gc_rows(LAM_T15_CEIL, a0, objects(a0), "xT") for fk, a0 in A0.items()}
    checks["M1a_T15_ceiling_binding_row_zero"] = bool(abs(m1a) <= 0.01)
    checks["M1b_footing_ceiling_binding_row_zero"] = bool(all(abs(v["Mcold"]) <= 0.01 for v in m1b.values()))
    checks["M2_xA_lambda1_all_GC_negative"] = bool(all(not OUT[fk]["any_feasible"] for fk in A0))
    say(f"M1a: x_A 0.41, a0 1.2e-10, lambda {LAM_T15_CEIL}: clusters_b0 {m1a:+.4f}  PASS={checks['M1a_T15_ceiling_binding_row_zero']}")
    say("M1b: " + "  ".join(f"{fk} lambda_c {v['lam_ceiling']:.5f} x_A {v['xA']:.4f} -> clusters_b0 {v['Mcold']:+.2e}" for fk, v in m1b.items())
        + f"  PASS={checks['M1b_footing_ceiling_binding_row_zero']}")
    say(f"M2: x := x_A at lambda = 1, GC rows feasible: " + "  ".join(f"{fk} {OUT[fk]['gc_feasible'][0]}/8" for fk in A0)
        + f"  PASS={checks['M2_xA_lambda1_all_GC_negative']}")
    say("sensitivity (not a check): corrected ledger at lambda 0.0073: " + "  ".join(
        f"{fk} (i) " + " ".join(f"{v:+.2f}" for v in s["i"].values()) for fk, s in sens.items()) + "  (no group/cluster row reaches 0)")
    MOUT = dict(M1a=m1a, M1b=m1b, sensitivity_corrected_lambda_T15ceil={fk: s["i"] for fk, s in sens.items()})

say("")
say(f"OVERALL VERDICT (lambda = 1, Gamma = 1/t_dyn): {overall}")
if not MUT:
    say("  at lambda = 1, f -> 1 everywhere, so M_cold/M_b = x - S (the fully settled ledger); on T15's own x every group and")
    say("  cluster row keeps positive cold mass, so these rows give no upper bound on lambda (as CFG453 found). The only row that")
    say("  can go negative is the MW 30-kpc point, and its sign depends on V and on the MW baryon mass (V0 lines above).")
say("checks: " + json.dumps(checks))
json.dump(dict(mutate=MUT, x_key=KEY, lam=LAM1, footings=OUT, overall=overall, cfg429_reproduction=dict(mine=mine429, committed=committed),
               mutate_checks=MOUT, checks=checks), open(os.path.join(HERE, f"cfg464_results{TAG}.json"), "w"), indent=1, default=float)
ok = all(checks.values())
say("<LANE> COMPLETE: all checks PASS" if ok else "<LANE> COMPLETE: -- SOME CHECKS FAIL")
open(os.path.join(HERE, f"cfg464_tdyn_corrected{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if ok else 1)
