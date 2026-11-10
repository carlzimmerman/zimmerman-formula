"""DCN1 labels (FROZEN_CRITERIA.md d603f1703c; amendments A1 0a6e46fb52, A2 15f6f993e4, A3 f5e101ba9a, A4 d08610695e,
A5 00d6869022, A6 830aeed427): reads the lane's outputs and writes dcn1_labels.json / .out.  Readings in order: frozen, A1, A3 as written,
A5, A6.  Also KA1-KA5, KA3 (the rule), MUTATE M1-M4, SCS3's global sequence through the rule, and the reported global maps.
Run: python3 -I dcn1_labels.py (needs dcn1_local.py for M3's numerical half: one KA4 sphere solve at N_R 108).
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, random
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RHO = 1.5
OUT = {"lane": "DCN1", "script": "dcn1_labels.py", "criteria": "d603f1703c",
       "amendments": {"A1": "0a6e46fb52", "A2": "15f6f993e4", "A3": "f5e101ba9a", "A4": "d08610695e", "A5": "00d6869022", "A6": "830aeed427"}}
LINES = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LINES.append(s)
J = lambda f: json.load(open(os.path.join(HERE, f)))
G = 4.30091e-6; KPCKMS_TO_S = 3.0857e16; MYR = 3.15576e13


# ------------------------------------------------------------------ the rule (SCS3 A4, b34295ebcd; no flat clause)
def rule3(Q):
    Q = [float(q) for q in Q]
    def three(a, b, c):
        d1, d2 = b - a, c - b
        out = dict(d1=d1, d2=d2)
        if d1 * d2 < 0:
            out.update(kind="oscillating", Qinf=0.5 * (b + c), E=max(abs(d1), abs(d2)), p=None)
        elif d2 == 0:
            out.update(kind="flat", Qinf=c, E=abs(d1), p=None)
        elif abs(d2) < abs(d1):
            p = math.log(d1 / d2) / math.log(RHO)
            out.update(kind="monotone", p=p, Qinf=c + d2 / (RHO ** p - 1), E=1.25 * abs(d2) / (RHO ** p - 1))
        else:
            out.update(kind="growing", p=None, Qinf=None, E=None)
        return out
    fin = three(*Q[-3:]); res = dict(values=Q, finest=fin); E = fin["E"]
    if len(Q) >= 4:
        prev = three(*Q[-4:-1]); res["previous"] = prev
        if fin["Qinf"] is not None and prev["Qinf"] is not None:
            E = max(E, abs(fin["Qinf"] - prev["Qinf"]))
        res["diverging"] = bool(fin["kind"] == "growing" and prev["kind"] == "growing")
    else:
        res["diverging"] = bool(fin["kind"] == "growing")
    res["Qinf"] = fin["Qinf"]; res["E"] = E
    okp = fin["p"] is None or (0.5 <= fin["p"] <= 6)
    res["converged"] = bool(fin["Qinf"] is not None and okp and E is not None and E <= 0.20 * abs(fin["Qinf"]))
    return res


# ------------------------------------------------------------------ KA3
hs = [RHO ** -i for i in range(5)]
def ka3_on(hs_, seed):
    rnd_ = random.Random(seed); seqs = []
    for p in (1.0, 2.0, 0.75):
        for _ in range(4):
            Qi = rnd_.choice([-1, 1]) * 10 ** rnd_.uniform(-30, -27); c = rnd_.uniform(-0.8, 0.8)
            r = rule3([Qi * (1 + c * h ** p) for h in hs_])
            seqs.append(dict(p=p, c=c, converged=r["converged"], ok=bool(r["converged"] and abs(r["Qinf"] / Qi - 1) <= 1e-6), rel=abs(r["Qinf"] / Qi - 1)))
    d1_, d2_, sl_ = rule3([h ** -1 for h in hs_]), rule3([h ** -0.5 for h in hs_]), rule3([1 + h ** 0.3 for h in hs_])
    ok = bool(all(x["ok"] for x in seqs) and d1_["diverging"] and d2_["diverging"] and not sl_["converged"])
    return dict(sequences=seqs, h_minus1_diverging=d1_["diverging"], h_minus_half_diverging=d2_["diverging"], slow_p03_converged=sl_["converged"], PASS=ok)
k3a = ka3_on(hs, 20261110)                                   # first pass: h = 1.5^-i from h = 1
k3b = ka3_on([1 / n for n in (48, 72, 108, 162, 243)], 20261110)   # A6: the lane's own h = 1/N_R
KA3 = k3a["PASS"]; KA3_A6 = k3b["PASS"]
OUT["KA3"] = dict(first_grid_h0_1=k3a, A6_grid_1_over_NR=k3b, PASS=KA3, PASS_A6=KA3_A6)
for lab, k3 in (("h = 1.5^-i from 1", k3a), ("A6: h = 1/N_R", k3b)):
    P(f"KA3 the rule ({lab}): recovered max rel {max(x['rel'] for x in k3['sequences']):.1e}, converged {sum(x['converged'] for x in k3['sequences'])}/12, "
      f"h^-1 diverging {k3['h_minus1_diverging']}, h^-0.5 diverging {k3['h_minus_half_diverging']}, 1+h^0.3 converged {k3['slow_p03_converged']} -> {'PASS' if k3['PASS'] else 'FAIL'}")

# ------------------------------------------------------------------ Part A
SYM = J("dcn1_symbol.json")
PARTA = bool(SYM["PART_A_PASS"]); OUT["PART_A"] = PARTA
P("Part A (sympy):", "PASS" if PARTA else "FAIL", "| A1 identity", SYM["A1"]["PASS"], "| A2 slab", SYM["A2"]["slab_limit_over_4piGrho_b"] if "slab_limit_over_4piGrho_b" in SYM["A2"] else SYM["A2"]["slab_limit_over_4piGrho"],
  "sphere", SYM["A2"]["sphere_limit_over_4piGrho"], "| A3", SYM["A3"]["PASS"])

# ------------------------------------------------------------------ KA1, KA2 (global)
ka1 = []
for R in (4, 5, 6):
    for k, r in J(f"dcn1_global_KA1_R{R}.json")["rows"].items():
        ka1.append(dict(row=k, rel_Gamma2=r["rel_Gamma2"], rel_min_dp=r["rel_min_dp"], ok=r["KA1_pass"],
                        Gamma2=r["routeL_A1mask"]["Gamma2_max_s2"], efold_myr=r["routeL_A1mask"]["efold_myr"],
                        theta_cells_from_axis=r["routeL_A1mask"]["theta_cells_from_axis"], r_over_Rd=r["routeL_A1mask"]["r_over_Rd"],
                        u_there=r["routeL_A1mask"]["u_there"], dp_there=r["routeL_A1mask"]["dp_there"], res=R, foot=r["spec"]["foot"]))
KA1 = all(x["ok"] for x in ka1)
ka2r = J("dcn1_global_KA2.json")["rows"]
KA2 = all(r["KA2_pass"] for r in ka2r.values())
OUT["KA1"] = dict(rows=ka1, PASS=KA1); OUT["KA2"] = dict(n=len(ka2r), max_rel=max(r.get("rel_min_dp") or 0 for r in ka2r.values()), PASS=KA2)
P(f"KA1 SCS3's flagged rows at R4-R6 (6 rows): max rel {max(max(x['rel_Gamma2'], x['rel_min_dp']) for x in ka1):.1e} -> {'PASS' if KA1 else 'FAIL'}")
P(f"KA2 SCS2's isolated R1 rows ({len(ka2r)}): max rel {OUT['KA2']['max_rel']:.1e}, D.P > 0 in every masked-in cell -> {'PASS' if KA2 else 'FAIL'}")

# SCS3's global sequence through the rule (finest three R4-R6 and previous three R3-R5, SCS3's stored R3)
s3 = J("../SCS3_external_field_stability/scs3_maps_THICK_AX_A4.json")["rows"]
scs3seq = {}
for foot in ("canonical", "alt"):
    q = [s3[f"THICK_AX_{foot}_thick_9p4_0p1_z_R{R}"]["routeL"]["L"]["Gamma2_max_s2"] for R in (3, 4, 5, 6)]
    rr = rule3(q)
    loc = [x for x in ka1 if x["foot"] == foot]
    scs3seq[foot] = dict(Gamma2_R3_R6=q, finest_kind=rr["finest"]["kind"], diverging_finest_three=rr["finest"]["kind"] == "growing",
                         R4_R6_theta_cells_from_axis=[x["theta_cells_from_axis"] for x in loc], R4_R6_u_there=[x["u_there"] for x in loc],
                         R4_R6_dp_there=[x["dp_there"] for x in loc], R4_R6_efold_myr=[x["efold_myr"] for x in loc])
    P(f"SCS3 global ({foot}) Gamma_L^2 R3-R6 {['%.3g' % v for v in q]}: finest three {rr['finest']['kind']}; R4-R6 maximum "
      f"{[x['theta_cells_from_axis'] for x in loc]} theta cells from the axis, u {['%.2f' % x['u_there'] for x in loc]}, "
      f"D.P {['%.2g' % x['dp_there'] for x in loc]}")
OUT["SCS3_global_sequence"] = scs3seq

# ------------------------------------------------------------------ KA4, KA5 (local)
KAL = {}
for S in ("KA4", "KA5"):
    for k, r in J(f"dcn1_local_{S}.json")["rows"].items():
        Ns = sorted(r["res"], key=int)
        Q = [r["res"][n]["Q"] for n in Ns]; QA = [r["res"][n]["QA"] for n in Ns]
        rq, ra = rule3(Q), rule3(QA)
        sup, supA = r["exact_sup_region"], r["exact_sup_annulus"]
        tol = 0.02 if S == "KA4" else 0.05
        frozen = bool(rq["converged"] and abs(rq["Qinf"] - sup) <= max(rq["E"], 0) + tol * abs(sup) and abs(rq["Qinf"] / sup - 1) <= tol)
        a1 = bool(rq["converged"] and np.sign(rq["Qinf"]) == np.sign(sup) and 0.5 <= rq["Qinf"] / sup <= 2)
        a3 = bool(ra["converged"] and abs(ra["Qinf"] / supA - 1) <= tol)
        a6 = bool(a3 or all(abs(r["res"][n]["QA"] / supA - 1) <= tol for n in Ns[-2:]))      # A6 item 2
        shells_fin = [r["res"][n]["shells"] for n in Ns[-2:]]
        KAL[k] = dict(Q_seq=Q, Q_rule=dict(kind=rq["finest"]["kind"], p=rq["finest"]["p"], Qinf=rq["Qinf"], E=rq["E"], converged=rq["converged"]),
                      exact_sup_region=sup, frozen_pass=frozen, A1_pass=a1,
                      QA_seq=QA, QA_rule=dict(kind=ra["finest"]["kind"], p=ra["finest"]["p"], Qinf=ra["Qinf"], E=ra["E"], converged=ra["converged"]),
                      exact_sup_annulus=supA, A3_pass=a3, A6_pass=a6, shells_finest_two=shells_fin)
        P(f"{k}: Q -> {rq['Qinf']} ({rq['finest']['kind']}, p {rq['finest']['p']}, conv {rq['converged']}) vs exact {sup:.4e}: "
          f"frozen {'PASS' if frozen else 'FAIL'}, A1 {'PASS' if a1 else 'FAIL'} | Q_A -> {ra['Qinf']:.5e} (p {ra['finest']['p']}, conv {ra['converged']}) "
          f"vs {supA:.5e} ({abs(ra['Qinf'] / supA - 1):.1e}): A3 {'PASS' if a3 else 'FAIL'}; A6 {'PASS' if a6 else 'FAIL'}")
OUT["KA4_KA5"] = KAL
KA4_frozen = all(v["frozen_pass"] for k, v in KAL.items() if k.startswith("KA4")); KA5_frozen = all(v["frozen_pass"] for k, v in KAL.items() if k.startswith("KA5"))
KA4_A1 = all(v["A1_pass"] for k, v in KAL.items() if k.startswith("KA4")); KA5_A1 = all(v["A1_pass"] for k, v in KAL.items() if k.startswith("KA5"))
KA4_A3 = all(v["A3_pass"] for k, v in KAL.items() if k.startswith("KA4")); KA5_A3 = all(v["A3_pass"] for k, v in KAL.items() if k.startswith("KA5"))
KA4_A6 = all(v["A6_pass"] for k, v in KAL.items() if k.startswith("KA4")); KA5_A6 = all(v["A6_pass"] for k, v in KAL.items() if k.startswith("KA5"))


# ------------------------------------------------------------------ per-background labels
def shells_unbounded(shl):
    """A3 item 2 on one grid: innermost three positive, rising inward, log-slope <= -0.25."""
    M = [x for x in shl if x["M"] is not None]
    if len(M) < 3:
        return False, None
    inn = M[-3:]
    vals = [x["M"] for x in inn]
    if not all(v > 0 for v in vals):
        return False, None
    rising = vals[2] > vals[1] > vals[0]
    smid = [math.sqrt(x["s_lo_over_L"] * x["s_hi_over_L"]) for x in inn]
    slope = float(np.polyfit(np.log(smid), np.log(vals), 1)[0])
    return bool(rising and slope <= -0.25), slope


def label_bg(r, which="real"):
    Ns = sorted(r["res"], key=int)
    key = {"real": ("Q", "QA", "shells"), "M1": ("M1_Q", "M1_QA", "M1_shells"), "M2": (None, "M2A3_QA", "M2A3_shells")}[which]
    out = {}
    nneg2 = [r["res"][n]["n_neg"] for n in Ns[-2:]] if which == "real" else None
    # frozen (Q, and the no-negative-cell clause)
    if key[0]:
        sign = -1 if which == "M1" else 1
        Q = [r["res"][n][key[0]] for n in Ns]; rq = rule3(Q)
        nn = (nneg2 == [0, 0]) if which == "real" else False
        Qid = [r["res"][n]["Q_identity"] for n in Ns]
        qid_div = rule3(Qid)["diverging"] if which == "real" else rq["diverging"]
        if rq["diverging"] and (not PARTA or qid_div):          # frozen: Part A fails to bound it, or Q_id diverges too
            fz = "unbounded"
        elif rq["converged"] and rq["Qinf"] - rq["E"] > 0:
            fz = "bounded-unstable"
        elif (rq["converged"] and rq["Qinf"] + rq["E"] < 0) or nn:
            fz = "stable"
        else:
            fz = "open"
        out["frozen"] = fz; out["Q_rule"] = dict(Qinf=rq["Qinf"], E=rq["E"], kind=rq["finest"]["kind"], p=rq["finest"]["p"], converged=rq["converged"])
    # A3
    QA = [r["res"][n][key[1]] for n in Ns]; ra = rule3(QA)
    sh2 = [r["res"][n][key[2]] for n in Ns[-2:]]
    ub = [shells_unbounded(s) for s in sh2]
    unb = all(u[0] for u in ub)
    Min = [ [x for x in s if x["M"] is not None][-1]["M"] for s in sh2 ]
    allneg = all(all(x["M"] < 0 for x in s if x["M"] is not None) for s in sh2)
    if unb:
        a3 = "unbounded"
    elif (ra["converged"] and ra["Qinf"] - ra["E"] > 0) or (Min[1] > 0 and Min[0] > 0 and abs(Min[1] / Min[0] - 1) <= 0.2):
        a3 = "bounded-unstable"
    elif ra["converged"] and ra["Qinf"] + ra["E"] < 0 and allneg:
        a3 = "stable"
    else:
        a3 = "open"
    a5 = a3
    if which == "real" and a3 == "open" and not unb and nneg2 == [0, 0]:
        a5 = "stable"
    out.update(A3=a3, A5=a5, QA_rule=dict(Qinf=ra["Qinf"], E=ra["E"], kind=ra["finest"]["kind"], p=ra["finest"]["p"], converged=ra["converged"]),
               shells_slopes_finest_two=[u[1] for u in ub], innermost_shell_finest_two=Min, all_shells_negative_finest_two=allneg,
               n_neg_finest_two=nneg2)
    return out


def problem_label(labels, problem):
    if any(l == "unbounded" for l in labels):
        return "ILL-POSED AT THE NULL"
    if any(l == "open" for l in labels):
        return "NO VERDICT"
    if any(l == "bounded-unstable" for l in labels):
        return "BOUNDED"
    return "ARTEFACT" if problem == "P1" else "STABLE AT THE CENTRE"


PROB = {}
for S in ("P1", "P2"):
    rows = J(f"dcn1_local_{S}.json")["rows"]
    per = {}
    for k, r in rows.items():
        L_ = label_bg(r); L1 = label_bg(r, "M1"); L2 = label_bg(r, "M2")
        fin = r["res"][str(243)]
        rho0 = r["case"]["rho0"]; s4 = 4 * math.pi * G * rho0 / KPCKMS_TO_S ** 2
        null_in_box = (fin.get("slope_u_vs_s") or 0) >= 0.3
        per[k] = dict(foot=r["case"]["spec"]["foot"], logm=r["case"]["spec"]["logm"], ge=r["case"]["spec"]["ge"], L_kpc=r["case"]["L"],
                      z_null_kpc=r["case"]["z_null"], labels=L_, M1=L1, M2=L2, null_in_box=bool(null_in_box) if S == "P1" else True,
                      finest=dict(QA=fin["QA"], Q=fin["Q"], min_dp=fin["min_dp"], n_neg=fin["n_neg"], slope_dp=fin.get("slope_absdp_vs_s"),
                                  slope_u=fin.get("slope_u_vs_s"), iterations=fin["iterations"], last_update=fin["last_update"]),
                      fourpiGrho0_s2=s4, QA_over_4piGrho0=(L_["QA_rule"]["Qinf"] / s4) if L_["QA_rule"]["Qinf"] is not None else None,
                      QAfinest_over_4piGrho0=fin["QA"] / s4,
                      freefall_efold_myr=1 / math.sqrt(s4) / MYR, min_dp_over_rho0=fin["min_dp"] / rho0)
    PROB[S] = per
OUT["per_background"] = PROB

# ------------------------------------------------------------------ MUTATE
m1_bites = all(v["M1"]["A3"] != v["labels"]["A5"] for S in PROB for v in PROB[S].values() if v["labels"]["A5"] in ("stable", "bounded-unstable"))
m1_bites_frozen = all(v["M1"].get("frozen") != v["labels"].get("frozen") for S in PROB for v in PROB[S].values() if v["labels"].get("frozen") in ("stable", "bounded-unstable"))
m2_bites = all(v["M2"]["A3"] == "unbounded" for S in PROB for v in PROB[S].values())
# M3 numerical half: the mutated identity on the KA4 sphere (one solve, N_R 108)
sys.path.insert(0, HERE)
import dcn1_local as DL
Sx = DL.S
a0c = Sx.a0k("canonical"); Mx = 10 ** 9.4; Rdx = Sx.R_d_shen(Mx); _, rho0x, hzx = DL.thick_rho(Mx, Rdx)
fPhi, frho, fG2, fsup = DL.sphere_case(rho0x, a0c)
Lb = 0.4 * 0.0131
b = DL.Box(Lb, -Lb, Lb, 108, 216)
PB = {k: fPhi(*v) for k, v in DL.boundary_points(b).items()}
C0 = float(np.mean(np.concatenate([v.ravel() for v in PB.values()]))); PB = {k: v - C0 for k, v in PB.items()}
rho = DL.cell_average(b, frho)
Phi, _, _ = DL.solve(b, rho, PB, a0c, fPhi(b.RR, b.ZZ) - C0)
gR, gz = DL.grad_cells(b, Phi, PB)
A_, radd = DL.assemble(b, DL.face_coefs(b, Phi, PB, a0c, gR, gz, lambda x: 1 / (1 + x)), PB)
dp = ((A_ @ Phi.ravel() - radd).reshape(b.shape)) / (4 * np.pi * G * b.V)
gm = np.sqrt(gR ** 2 + gz ** 2); u = gm / a0c
GL = -4 * np.pi * G * dp * u * (2 + u)
HRR = np.gradient(gR, b.hR, axis=0); Hzz = np.gradient(gz, b.hz, axis=1); HRz = 0.5 * (np.gradient(gR, b.hz, axis=1) + np.gradient(gz, b.hR, axis=0))
nR = gR / gm; nz = gz / gm; Pnn = nR * nR * HRR + 2 * nR * nz * HRz + nz * nz * Hzz
s4c = 4 * np.pi * G * rho
Gid = (2 + u) * (u * Pnn / (1 + u) - s4c); Gmut = (2 + u) * (u * Pnn - s4c)
ss = np.sqrt(b.RR ** 2 + b.ZZ ** 2); ann = (ss >= Lb / 8) & (ss <= Lb / 2)
rel_true = float(np.max(np.abs(Gid[ann] / GL[ann] - 1))); rel_mut = float(np.max(np.abs(Gmut[ann] / GL[ann] - 1)))
m3_num = rel_mut > 0.05
m3_sym = SYM["M3_identity_mutated"]["bites"]
cm = open(os.path.join(HERE, "compile_MUTATE.txt")).read(); ct = open(os.path.join(HERE, "compile.txt")).read()
m4 = ("exit 1" in cm and cm.count("error") >= 6 and "exit 0" in ct)
OUT["MUTATE"] = dict(M1_A5_bites=m1_bites, M1_frozen_bites=m1_bites_frozen, M2_A3_bites=m2_bites,
                     M3=dict(sympy_bites=m3_sym, numeric_KA4_identity_rel=rel_true, numeric_KA4_mutated_rel=rel_mut, numeric_bites=bool(m3_num),
                             u_max_annulus=float(np.max(u[ann]))),
                     M4_lean_twin_fails=bool(m4))
P(f"MUTATE M1 (G -> -D.P): label changes on every stable/bounded background: A5 {m1_bites}, frozen {m1_bites_frozen}")
P(f"MUTATE M2 (planted s^-1 D.P): unbounded on every background: {m2_bites}")
P(f"MUTATE M3: sympy bites {m3_sym}; numerical half on the KA4 sphere annulus: identity vs route L max rel {rel_true:.3f}, "
  f"mutated {rel_mut:.3f} (u <= {np.max(u[ann]):.3f} there) -> {'BITES' if m3_num else 'DOES NOT BITE'}")
P(f"MUTATE M4 Lean twin: {'all false versions fail' if m4 else 'DOES NOT BITE'}")

# ------------------------------------------------------------------ readings
def lane(pl1, pl2, ka_ok):
    if not ka_ok:
        return "NO VERDICT"
    if "ILL-POSED AT THE NULL" in (pl1, pl2):
        return "ILL-POSED AT THE NULL"
    if "NO VERDICT" in (pl1, pl2):
        return "NO VERDICT"
    if "BOUNDED" in (pl1, pl2):
        return "BOUNDED"
    if pl1 == "ARTEFACT" and pl2 == "STABLE AT THE CENTRE":
        return "ARTEFACT"
    return "NO VERDICT"


base_ok = PARTA and KA1 and KA2 and KA3
READ = {}
for rd, kaok, lk in (("frozen", base_ok and KA4_frozen and KA5_frozen, "frozen"), ("A1", base_ok and KA4_A1 and KA5_A1, "frozen"),
                     ("A3", base_ok and KA4_A3 and KA5_A3, "A3"), ("A5", base_ok and KA4_A3 and KA5_A3, "A5"),
                     ("A6", PARTA and KA1 and KA2 and KA3_A6 and KA4_A6 and KA5_A6, "A5")):
    READ[rd] = {}
    for foot in ("canonical", "alt"):
        pl = {}
        for S in ("P1", "P2"):
            labs = [v["labels"][lk] for v in PROB[S].values() if v["foot"] == foot]
            pl[S] = problem_label(labs, S)
            pl[S + "_counts"] = {x: labs.count(x) for x in sorted(set(labs))}
        pl["lane"] = lane(pl["P1"], pl["P2"], kaok); pl["known_answers_ok"] = kaok
        READ[rd][foot] = pl
    P(f"reading {rd}: KA ok {kaok}; canonical lane {READ[rd]['canonical']['lane']} (P1 {READ[rd]['canonical']['P1']} "
      f"{READ[rd]['canonical']['P1_counts']}, P2 {READ[rd]['canonical']['P2']} {READ[rd]['canonical']['P2_counts']}); alt lane "
      f"{READ[rd]['alt']['lane']} (P1 {READ[rd]['alt']['P1']} {READ[rd]['alt']['P1_counts']}, P2 {READ[rd]['alt']['P2']} {READ[rd]['alt']['P2_counts']})")
OUT["readings"] = READ

# ------------------------------------------------------------------ per-background table
P("per background (finest grid N_R 243): label frozen / A3 / A5; Q_A(inf or finest)/(4 pi G rho_0); min D.P/rho_0; n_neg; null in box; slopes")
for S in ("P1", "P2"):
    for k, v in PROB[S].items():
        P(f"  {S} {k}: {v['labels'].get('frozen')} / {v['labels']['A3']} / {v['labels']['A5']}; Q_A finest/4piGrho0 {v['QAfinest_over_4piGrho0']:.3f}"
          f" (rule {v['labels']['QA_rule']['kind']}, conv {v['labels']['QA_rule']['converged']}); min D.P/rho0 {v['min_dp_over_rho0']:.2f}; "
          f"n_neg finest two {v['labels']['n_neg_finest_two']}; null in box {v['null_in_box']}; slopes dp {v['finest']['slope_dp']:.2f} u {v['finest']['slope_u']:.2f}; "
          f"innermost shell/4piGrho0 {[round(m / v['fourpiGrho0_s2'], 3) for m in v['labels']['innermost_shell_finest_two']]}")

# ------------------------------------------------------------------ reported: global unmasked maps
def gsum(f):
    rows = J(f)["rows"]; o = {}
    for k, r in rows.items():
        o[k] = dict(n_neg=r["n_negative_unmasked_offplane"], neg_r_over_Rd=r.get("negative_r_over_Rd"), neg_shells=r.get("negative_shells"),
                    r_min_over_Rd=r.get("r_min_over_Rd"), min_dp=r["min_dp_unmasked_offplane"])
    return o
OUT["reported_P2G_rmin_1e-4"] = gsum("dcn1_global_P2G.json"); OUT["reported_P2R_rmin_1e-6"] = gsum("dcn1_global_P2R.json")
thin_follow = all((v["neg_r_over_Rd"] is None) or (v["neg_r_over_Rd"][0] < 1.3 * v["r_min_over_Rd"]) for v in OUT["reported_P2R_rmin_1e-6"].values())
P(f"reported: with r_min moved 1e-4 -> 1e-6 R_d, every negative cell's inner edge follows r_min (first shells): {thin_follow}; "
  f"frozen thick deposits: {sum(v['n_neg'] for k, v in OUT['reported_P2R_rmin_1e-6'].items() if 'thick' in k and k.endswith('frozen'))} negative cells")

OUT["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
json.dump(OUT, open(os.path.join(HERE, "dcn1_labels.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, "dcn1_labels.out"), "w").write("\n".join(LINES) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
