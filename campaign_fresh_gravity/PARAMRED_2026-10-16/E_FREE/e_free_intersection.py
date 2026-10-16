"""PARAMRED lane E (FREE): constraint intersection for the free (untethered) cold-energy component.
Criteria: FROZEN_CRITERIA.md (written before this script).  Tests T1-T5, controls K1, N2, T5-control, MUTATE.
Inputs: small JSON only (CFG317 per-object table, CFG782 results).  Pure python, one process, seconds.
Run:  OMP_NUM_THREADS=1 nice -n 19 python3 e_free_intersection.py        (E_FREE_MUTATE=1: R_ind = 1 variant, exits 1)
kappa = 1/2 FITTED; Omega_c/Omega_b = 5.364 measured; both footings, never pooled; not theory closed.
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(os.path.dirname(HERE))
MUT = os.environ.get("E_FREE_MUTATE") == "1"
OUT = []
RES = {"lane": "PARAMRED_E_FREE", "mutate": MUT}
FAILS = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        FAILS.append(name)


G, MSUN, KB, MP = 6.674e-11, 1.989e30, 1.380649e-23, 1.6726e-27
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
OMEGA = 5.364
cs = lambda T: math.sqrt(KB * T / (0.59 * MP)) / 1e3          # km/s, isothermal, mu 0.59
Vinit = lambda M, a0: (G * M * MSUN * a0) ** 0.25 / 1e3          # km/s
Vflat = Vinit

# ---------------------------------------------------------------- T1 selector window
j = json.load(open(os.path.join(LANES, "CFG317_baryon_loss_cold_mass", "cfg317_baryon_loss_results.json")))["numbers"]
EST, NAMES = j["EST"], j["NAMES"]
GROUPS = {"MW UFDs": "ufd", "MW classicals": "cls", "M31 (Collins)": "col", "M31 (LVD)": "m31", "LV field": "fld"}
objs, pts = {}, []
for lab, key in GROUPS.items():
    lst = []
    for nm, e in zip(NAMES[key], EST[f"-0.2|{key}"]):
        if e is None:
            continue
        Mb = float(e["Ms"]) + float(e.get("Mg") or 0.0)
        lR = None if e.get("lR") is None else float(e["lR"])
        lst.append(dict(name=nm, Mb=Mb, lR=lR))
        if lR is not None:
            pts.append((math.log10(Mb), lR))
    objs[lab] = lst
n = len(pts)
mx, my = sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n
slope = sum((p[0] - mx) * (p[1] - my) for p in pts) / sum((p[0] - mx) ** 2 for p in pts)
icpt = my - slope * mx
P("PARAMRED lane E (FREE): constraint intersection" + ("  [MUTATE R_ind = 1]" if MUT else ""))
P(f"T1 inputs: CFG317 per-object table, {n} objects with R_ind; OLS log R_ind = {icpt:+.3f} {slope:+.3f} log M_b,now")
RES["T1_relation"] = dict(icpt=icpt, slope=slope, n=n)


def vlist(lab, a0, mutate):
    out = []
    for o in objs[lab]:
        lR = 0.0 if mutate else (o["lR"] if o["lR"] is not None else icpt + slope * math.log10(o["Mb"]))
        lR = max(lR, 0.0)
        out.append((Vinit(o["Mb"] * 10 ** lR, a0), o["name"], lR))
    return sorted(out)


def window(a0, mutate):
    u = vlist("MW UFDs", a0, mutate)
    N = len(u)
    k = -(-9 * N // 10)                              # ceil(0.9 N), integer arithmetic
    L, Lname = u[k - 1][0], u[k - 1][1]
    ups = {}
    for lab in ("MW classicals", "M31 (Collins)", "M31 (LVD)", "LV field"):
        v = vlist(lab, a0, mutate)
        m = len(v) // 10
        ups[lab] = dict(U=v[m][0], who=v[m][1], N=len(v), n_below_L=sum(1 for x in v if x[0] < L), allowed=m)
    Umin_lab = min(ups, key=lambda t: ups[t]["U"])
    return dict(N_ufd=N, k=k, L=L, L_who=Lname, ups=ups, U=ups[Umin_lab]["U"], U_lab=Umin_lab, U_who=ups[Umin_lab]["who"],
                nonempty=bool(L < ups[Umin_lab]["U"]), ratio_L_over_U=L / ups[Umin_lab]["U"])


T1 = {}
for foot, a0 in A0.items():
    w = window(a0, MUT)
    # exploratory (not a verdict): S2 applied only to groups without UFD analogues
    Uexp = min(w["ups"]["MW classicals"]["U"], w["ups"]["LV field"]["U"])
    w["exploratory_no_M31_window"] = dict(L=w["L"], U=Uexp, nonempty=bool(w["L"] < Uexp))
    w["lambda"] = {f"T{int(T)}": dict(cs=cs(T), lam_L=w["L"] / cs(T), lam_U=w["U"] / cs(T),
                                      sqrt2_inside=bool(w["L"] < math.sqrt(2) * cs(T) <= w["U"]),
                                      sqrt2_inside_exploratory=bool(w["L"] < math.sqrt(2) * cs(T) <= Uexp))
                   for T in (1e4, 1.5e4, 2e4)}
    T1[foot] = w
    P(f"\n  T1 {foot}: S1 needs V_th > {w['L']:.2f} km/s (UFD {w['k']}-th of {w['N_ufd']}: {w['L_who']})")
    for lab, u in w["ups"].items():
        P(f"      S2 {lab:14s}: V_th <= {u['U']:.2f} km/s (allowed flagged {u['allowed']} of {u['N']}; set by {u['who']}); {u['n_below_L']} objects have V_init < L")
    P(f"      WINDOW = ({w['L']:.2f}, {w['U']:.2f}] km/s  non-empty: {w['nonempty']}  (L/U = {w['ratio_L_over_U']:.3f}; tightest group {w['U_lab']} via {w['U_who']})")
    P(f"      exploratory, S2 on classicals+field only: ({w['L']:.2f}, {Uexp:.2f}] non-empty {w['exploratory_no_M31_window']['nonempty']}")
    for t, d in w["lambda"].items():
        P(f"      {t}: c_s {d['cs']:.2f}  lambda window ({d['lam_L']:.3f}, {d['lam_U']:.3f}]  sqrt2 inside: {d['sqrt2_inside']}  (exploratory-no-M31: {d['sqrt2_inside_exploratory']})")
RES["T1"] = T1


def window_frac(a0, f1, f2):
    u = vlist("MW UFDs", a0, False)
    k = max(1, math.ceil(round(f1 * len(u), 9)))
    L = u[k - 1][0]
    U = min(vlist(lab, a0, False)[int(math.floor(round(f2 * len(objs[lab]), 9)))][0]
            for lab in ("MW classicals", "M31 (Collins)", "M31 (LVD)", "LV field"))
    return L, U


# POST-HOC DIAGNOSTIC (not one of the five frozen tests): how far would the S1/S2 gates have to be relaxed to open a window?
sens = {}
P("\n  post-hoc sensitivity (canonical): window (L, U] for S1 fraction f1 (UFDs flagged >=) and S2 fraction f2 (others flagged <=)")
for f1 in (0.9, 0.8, 0.7, 0.6, 0.5):
    row = []
    for f2 in (0.1, 0.2, 0.3, 0.4, 0.5):
        L, U = window_frac(A0["canonical"], f1, f2)
        sens[f"f1={f1},f2={f2}"] = dict(L=L, U=U, nonempty=bool(L < U))
        row.append(f"{'open' if L < U else 'EMPTY'}({L:.1f},{U:.1f})")
    P(f"    f1={f1}: " + "  ".join(row))
RES["posthoc_sensitivity"] = sens

# K1 reproduction of CFG782 at the primary setting
r782 = json.load(open(os.path.join(LANES, "CFG782_unbinding_selector", "cfg782_results.json")))["groups"]["canonical|T1.5e+04"]
if not MUT:
    vth = math.sqrt(2) * cs(1.5e4)
    ok, det = True, []
    for lab in GROUPS:
        fr = sum(1 for x in vlist(lab, A0["canonical"], False) if x[0] < vth) / len(objs[lab])
        ref = r782[lab]["frac_sudden"]
        ok &= abs(fr - ref) < 1e-9
        det.append(f"{lab} {fr:.4f}/{ref:.4f}")
    check("K1 reproduces CFG782 group fractions (canonical, 1.5e4 K)", ok, "; ".join(det))

# ---------------------------------------------------------------- T2 / T3 / T4 interval algebra
def inter(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    return (lo, hi) if lo <= hi else None


def class_intervals(swap_E_with_C=False):
    d = {}
    # U: lower bound only (data constrain inside r)
    delta, sig = 0.325, 0.325 / 3.5
    r_lo, r_mid, r_hi = (10 ** (2 * (delta + s)) - 1 for s in (-sig, 0.0, sig))
    q_lo, q_mid, q_hi = 1.75, 3.5, 7.0
    m_lo = r_lo * (1 + q_lo * OMEGA)
    m_mid = r_mid * (1 + q_mid * OMEGA)
    m_hi = r_hi * (1 + q_hi * OMEGA)
    acct = {"leaky_box_primary": OMEGA * (10 ** 2.07 - 1), "CFG336_lead_R6_30_largestS": OMEGA * (30 - 1), "CFG317_Rneed_log3.65": OMEGA * (10 ** 3.65 - 1)}
    d["U"] = dict(r_U=(r_lo, r_mid, r_hi), m_U_over_Mb=(m_lo, m_mid, m_hi),
                  S_over_Mb=acct, F_lower={k: m_lo / s for k, s in acct.items()},
                  F_mid={k: m_mid / s for k, s in acct.items()})
    # E amount
    S_E = (OMEGA * (5.6 - 1), OMEGA * (10 - 1))
    d["E"] = dict(S_over_Mb=S_E, F=(0.55 / S_E[1], 0.80 / S_E[0]))
    # E differential (frozen small-signal linear form); also the CFG811 Z
    d["E_diff"] = dict(F_needed=((0.280 - 0.083) / 0.013, 0.280 / 0.013, (0.280 + 0.083) / 0.013), Z_vs_universal=(0.280 - 0.013) / 0.083)
    # C
    S_C = (OMEGA * (1 / 0.686 - 1), OMEGA * (1 / 0.636 - 1))
    Fc = (1.9 / S_C[1], 4.5 / S_C[0])
    d["C"] = dict(S_over_Mb=S_C, F_raw=Fc, F=(Fc[0], min(Fc[1], 1.0)), alt_median_F=2.74 / (S_C[0] + S_C[1]) * 2)
    if swap_E_with_C:
        d["E"]["F"] = d["C"]["F"]
    return d


def run_T2_T3_T4(swap=False):
    d = class_intervals(swap)
    U_acc = d["U"]["F_lower"]
    U_generous = min(U_acc.values())
    U_prim = U_acc["leaky_box_primary"]
    E, C = d["E"]["F"], d["C"]["F"]
    pw = {}
    for nm, Uset in (("primary", (U_prim, 1.0)), ("generous", (U_generous, 1.0))):
        pw[nm] = dict(U_E=inter(Uset, E), U_C=inter(Uset, C), E_C=inter(E, C),
                      joint=(inter(inter(Uset, E), C) if inter(Uset, E) else None))
    gap = C[0] / E[1] if C[0] > E[1] else None
    # T3 family B
    kC = (2.88, 3.62)
    m_lo = d["U"]["m_U_over_Mb"][0]
    R_lb = 10 ** 2.07
    kU_alt_lower = m_lo / R_lb
    T3 = dict(k_C=kC, U_present_hot_gas="VIOLATED (M_hot = 0 today, needed m_U >= %.1f M_b)" % m_lo,
              k_U_alt_ever_hot_lower=kU_alt_lower, alt_overlap_with_kC=bool(kU_alt_lower <= kC[1]),
              E_status="PENDING (sealed CFG746 prediction, not a pass)")
    # T4
    logM = {}
    ufd_M = sorted(o["Mb"] for o in objs["MW UFDs"])
    logM["U"] = math.log10(ufd_M[len(ufd_M) // 2])
    logM["E"] = 10.8
    logM["C"] = (13.0, 14.0)
    p_EC = ((math.log10(C[0]) - math.log10(E[1])) / (logM["C"][1] - logM["E"]), (math.log10(C[1]) - math.log10(E[0])) / (logM["C"][0] - logM["E"]))
    p_UE_max = {k: (math.log10(E[1]) - math.log10(v)) / (logM["E"] - logM["U"]) for k, v in U_acc.items()}
    T4 = dict(logM=logM, p_EC=p_EC, p_UE_upper=p_UE_max,
              single_power_law_possible={k: bool(v >= p_EC[0]) for k, v in p_UE_max.items()})
    return d, pw, gap, T3, T4


d, pw, gap, T3, T4 = run_T2_T3_T4(False)
P("\nT2 family A: M_free = F x 5.364 x M_exp, universal F")
P(f"  U: r_U = M_free/M_law = {d['U']['r_U'][1]:.2f} [{d['U']['r_U'][0]:.2f}, {d['U']['r_U'][2]:.2f}]; m_U = {d['U']['m_U_over_Mb'][1]:.1f} M_b,now [{d['U']['m_U_over_Mb'][0]:.1f}, {d['U']['m_U_over_Mb'][2]:.1f}]")
for k, s in d["U"]["S_over_Mb"].items():
    P(f"     supply {k}: {s:.1f} M_b  ->  F_U >= {d['U']['F_lower'][k]:.4f} (mid {d['U']['F_mid'][k]:.4f})")
P(f"  E amount: F_E in [{d['E']['F'][0]:.4f}, {d['E']['F'][1]:.4f}]  (S_E = {d['E']['S_over_Mb'][0]:.1f}-{d['E']['S_over_Mb'][1]:.1f} M_b)")
P(f"  E differential (frozen linear form): F needed [{d['E_diff']['F_needed'][0]:.1f}, {d['E_diff']['F_needed'][1]:.1f}, {d['E_diff']['F_needed'][2]:.1f}] vs cap 1; universal-rule Z = {d['E_diff']['Z_vs_universal']:.2f}")
P(f"  C: F_C in [{d['C']['F'][0]:.3f}, {d['C']['F'][1]:.3f}] (raw upper {d['C']['F_raw'][1]:.2f} before the cap)")
for nm, w in pw.items():
    P(f"  pairwise ({nm} U): U-E {w['U_E']}  U-C {w['U_C']}  E-C {w['E_C']}  joint {w['joint']}")
P(f"  E-C gap factor (C lower / E upper) = {gap:.1f}" if gap else "  E-C: intervals overlap")
P("T3 family B: M_free = k M_hot")
P(f"  k_C = {T3['k_C']}; U with present hot gas: {T3['U_present_hot_gas']}; alt 'ever-hot' reading k_U >= {T3['k_U_alt_ever_hot_lower']:.3f} (overlaps k_C range if inside-fraction free: {T3['alt_overlap_with_kC']}); E: {T3['E_status']}")
P("T4 single power law F ~ M_b^p")
P(f"  log M_b: U {T4['logM']['U']:.2f}, E {T4['logM']['E']}, C {T4['logM']['C']}; p_EC in [{T4['p_EC'][0]:.2f}, {T4['p_EC'][1]:.2f}]")
for k, v in T4["p_UE_upper"].items():
    P(f"    U accounting {k}: p_UE <= {v:.3f}  -> single power law possible: {T4['single_power_law_possible'][k]}")
RES.update(T2=dict(classes=d, pairwise=pw, EC_gap_factor=gap), T3=T3, T4=T4)

# control N2: replace E by C; overlap code must now find a non-empty joint
_, pw2, gap2, _, _ = run_T2_T3_T4(True)
check("N2 control (E := C interval) gives non-empty E-C and joint", pw2["generous"]["E_C"] is not None and pw2["generous"]["joint"] is not None,
      f"E-C {pw2['generous']['E_C']}, joint {pw2['generous']['joint']}")
RES["N2_control"] = dict(E_C=pw2["generous"]["E_C"], joint=pw2["generous"]["joint"])

# ---------------------------------------------------------------- T5 dimensional analysis
DIM = {  # exponents of (L, M, T)
    "G": (3, -1, -2), "a0": (1, 0, -2), "M": (0, 1, 0), "c": (1, 0, -1), "cs": (1, 0, -1), "r": (1, 0, 0)}


def nullspace(names):
    cols = [DIM[x] for x in names]
    rows = [[Fraction(cols[j][i]) for j in range(len(names))] for i in range(3)]
    piv, r = [], 0
    for c in range(len(names)):
        pr = next((i for i in range(r, 3) if rows[i][c] != 0), None)
        if pr is None:
            continue
        rows[r], rows[pr] = rows[pr], rows[r]
        rows[r] = [x / rows[r][c] for x in rows[r]]
        for i in range(3):
            if i != r and rows[i][c] != 0:
                rows[i] = [a - rows[i][c] * b for a, b in zip(rows[i], rows[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(len(names)) if c not in piv]
    ns = []
    for f in free:
        v = [Fraction(0)] * len(names)
        v[f] = Fraction(1)
        for i, pc in enumerate(piv):
            v[pc] = -rows[i][f]
        ns.append([str(x) for x in v])
    return ns


T5 = {"G,a0,M": nullspace(["G", "a0", "M"]), "G,a0,M,c": nullspace(["G", "a0", "M", "c"]), "G,a0,M,cs": nullspace(["G", "a0", "M", "cs"])}
P("\nT5 dimensionless combinations (exponents in the listed order):")
for k, v in T5.items():
    P(f"  {k}: {len(v)} combination(s) {v}")
ctrl = nullspace(["G", "M", "r", "c"])
# POST-RUN FIX (disclosed): the first run compared the control vector exactly to (1,1,-1,-2); the nullspace routine returns it
# up to a scalar (-1/2 times it), which is the same dimensionless combination. The check now compares up to a scalar multiple.
_c = [Fraction(x) for x in ctrl[0]] if len(ctrl) == 1 else []
_ref = [Fraction(x) for x in (1, 1, -1, -2)]
_ratio = {(a / b) for a, b in zip(_c, _ref)} if _c else set()
check("T5 control (G,M,r,c): exactly one combination, proportional to (1,1,-1,-2)", len(ctrl) == 1 and len(_ratio) == 1, f"{ctrl} (scalar multiple {sorted(str(x) for x in _ratio)})")
check("T5 (G,a0,M) has no dimensionless combination", T5["G,a0,M"] == [], str(T5["G,a0,M"]))
RES["T5"] = T5
RES["Vflat_kms"] = {}
for foot, a0 in A0.items():
    RES["Vflat_kms"][foot] = {"U_median": Vflat(10 ** T4["logM"]["U"], a0), "E_logM10.8": Vflat(10 ** 10.8, a0),
                              "C_logM13.0": Vflat(1e13, a0), "C_logM14.0": Vflat(1e14, a0)}
    v = RES["Vflat_kms"][foot]
    P(f"  V_flat {foot}: U median {v['U_median']:.1f}, E {v['E_logM10.8']:.1f}, C {v['C_logM13.0']:.1f}-{v['C_logM14.0']:.1f} km/s")

# ---------------------------------------------------------------- verdict summary
q1 = bool(pw["generous"]["joint"] is not None and d["E_diff"]["F_needed"][0] <= 1.0)
q3 = bool(all(T1[f]["nonempty"] and all(T1[f]["lambda"][t]["sqrt2_inside"] for t in T1[f]["lambda"]) for f in T1))
RES["Q1_pin"] = q1
RES["Q2_one_constant"] = bool(q1 and len(T5["G,a0,M,cs"]) > 0)   # needs Q1 and a dimensionless variable from allowed quantities
RES["Q3_selector_forced"] = q3
RES["fails"] = FAILS
P(f"\nQ1 (one form for U,E,C): {q1}   Q2: {RES['Q2_one_constant']}   Q3 (selector forced): {q3}")

if MUT:
    base = window(A0["canonical"], False)
    moved = abs(base["L"] - T1["canonical"]["L"]) > 1e-6 or abs(base["U"] - T1["canonical"]["U"]) > 1e-6
    P(f"MUTATE: window with R_ind = 1 is ({T1['canonical']['L']:.2f}, {T1['canonical']['U']:.2f}] vs main ({base['L']:.2f}, {base['U']:.2f}]; moved {moved}")
    RES["mutate_moved"] = moved

json.dump(RES, open(os.path.join(HERE, f"e_free_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"e_free{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if (FAILS or MUT) else 0)
