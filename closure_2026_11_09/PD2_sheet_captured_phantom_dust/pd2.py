#!/usr/bin/env python3
"""PD2 (FROZEN_CRITERIA.md 98a5315562): variant P. Galaxy share M_share = pi Sigma_sheet R_ta^2 (graded as stated; universal R_trunc),
S-claim bracket R_trunc = (3/2) Omega_d (H0/H)^2 L_web; Q1 conservation, Q2 KiDS / SPARC, Q3 groups / X-COP and Q5 Bullet through
PD1's pd1_a1.py halo rule at 0.40 of the share with prefactor 1 (orchestrator stand-in) and pd1_a2.py's DB1 child; KA-Q1..Q3;
MUTATE MQ1 (f_sheet x 5), MQ2 (cluster fraction 1.0 = PD1's pd1_a1_share5.41_fcpre1.0, read).
    python3 pd2.py   -> pd2.json / pd2.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PD1 = os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust")
CRIT = "98a5315562"; F_SHEET = 0.60; CL_FRAC = 0.40; L = []
def P(s): print(s, flush=True); L.append(str(s))
src = open(os.path.join(PD1, "pd1.py")).read(); ns = {"__file__": os.path.join(PD1, "pd1.py"), "__name__": "pd1_lib"}
exec(compile(src[:src.index("# ---------------- run")], "pd1_prefix", "exec"), ns)
np, G, MS, KPC, MPC, glaw, Mph, A0, FOOTS = ns["np"], ns["G"], ns["MS"], ns["KPC"], ns["MPC"], ns["glaw"], ns["Mph"], ns["A0"], ns["FOOTS"]
footing_bg, gsmf, LF, LE, GALS, PRE, Q8, G_KPC = ns["footing_bg"], ns["gsmf"], ns["LF"], ns["LE"], ns["GALS"], ns["PRE"], ns["Q8"], ns["G_KPC"]
from scipy.optimize import brentq
VST = {"canonical": 265.8, "alt": 288.1}
def model(B, f, f_sheet=F_SHEET):
    H0 = B.H0s; Lweb = VST[f] * 1e3 / H0; Sig = f_sheet * B.RHO_D0 * Lweb; cH2 = math.pi / 2 * H0 ** 2
    def share(Mb_kg): R2 = 2 * math.sqrt(G * Mb_kg * A0[f]) / cH2; return math.pi * Sig * R2, math.sqrt(R2)
    Rt_closed = 2 * math.pi * G * Sig / cH2; Rt_claim = lambda z: 1.5 * (B.OD / B.h ** 2) * (B.H0s / B.Hs(1 / (1 + z))) ** 2 * Lweb
    return dict(L_web_Mpc=Lweb / MPC, Sigma=Sig, share=share, Rt_closed_Mpc=Rt_closed / MPC, Rt_claim=Rt_claim)
def rtrunc(Mb_kg, a0, Msh):
    return brentq(lambda r: Mph(r, Mb_kg, a0) - Msh, 1e-6 * KPC, 1e4 * MPC)
def kids(a0, Rt_of):
    sh = []
    for p in LE:
        Mb = p["Mb"]; R = math.sqrt(G * Mb / p["gbar"]); rt = Rt_of(Mb); M = Mb + Mph(min(R, rt), Mb, a0); sh.append(math.log10(G * M / R ** 2 / float(glaw(p["gbar"], a0))))
    sh = np.array(sh); return dict(status="PASS" if np.all(np.abs(sh) <= 0.05) else "FAIL", max_abs=float(np.max(np.abs(sh))), n_over=int(np.sum(np.abs(sh) > 0.05)), min=float(sh.min()), mean=float(sh.mean()))
def sparc(f, a0, Rt_of):
    rows = []; nt = 0
    for q, Tf in zip(GALS, PRE[f]):
        R = q["R"]; Rm = q["Rm"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2; Mbs = max(float(np.max(np.clip(VB2 * R / G_KPC, 0, None))), 1e3)
        rt = Rt_of(Mbs * MS); g = q["GB"]; nt += rt < Rm[-1]
        if math.isfinite(rt): gt = G * Mbs * MS / rt ** 2; ge = np.where((Rm < rt)[:, None], glaw(g, a0), g + (float(glaw(gt, a0)) - gt) * (rt / Rm[:, None]) ** 2)
        else: ge = glaw(g, a0)
        lgp = np.log10(np.maximum(ge, 1e-300)) + Tf; OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k]))
    def pooled(idx):
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
    massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]; return dict(all=pooled(range(len(rows))), massive=pooled(massive), n_truncated_inside_Rlast=int(nt))
RES = dict(criteria=CRIT, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
# KA-Q3: the inverse map y(x) = x^2 / (1 - x) of x = y (nu(y) - 1)
ys = np.geomspace(1e-4, 1e4, 20); xs = ys * (0.5 + np.sqrt(0.25 + 1 / ys) - 1); dev = float(np.max(np.abs(xs ** 2 / (1 - xs) / ys - 1)))
src_form = {f"y {y:.0e}": dict(law_J_over_a0=float(x), source_F_prime_gives=float(y / (1 - y)) if y < 1 else float("inf")) for y, x in zip(ys[::4], xs[::4])}
RES["KA_Q3"] = dict(max_rel_dev=dev, pass_=bool(dev < 1e-10), source_dFdy_comparison=src_form)
P(f"KA-Q3 inverse map y = x^2/(1-x): max rel dev {dev:.1e} -> {'PASS' if dev < 1e-10 else 'FAIL'}; the source's dF/dy = y/(y+1) gives |J|/a0 = y/(1-y): e.g. at y 0.01 law {xs[4]:.4f} vs source-form {ys[4]/(1-ys[4]):.4f}")
for f in FOOTS:
    B = footing_bg(f); a0 = A0[f]; Mdl = model(B, f); r = dict(L_web_Mpc=Mdl["L_web_Mpc"], R_trunc_closed_Mpc=Mdl["Rt_closed_Mpc"], R_trunc_claim_z0_Mpc=Mdl["Rt_claim"](0.0) / MPC)
    # KA-Q1: universality
    kq = []
    for lm in (8, 9, 10, 11, 12):
        Mb = 10 ** lm * MS; Msh, Rta = Mdl["share"](Mb); rt = rtrunc(Mb, a0, Msh); kq.append(dict(logMb=lm, share_over_Mb=Msh / Mb, R_ta_Mpc=Rta / MPC, R_trunc_Mpc=rt / MPC, closed_Mpc=Mdl["Rt_closed_Mpc"], dev=rt / MPC / Mdl["Rt_closed_Mpc"] - 1))
    r["KA_Q1"] = dict(rows=kq, pass_=bool(all(abs(x["dev"]) <= 0.02 for x in kq if x["logMb"] <= 11)))
    P(f"[{f}] L_web {Mdl['L_web_Mpc']:.3f} Mpc; R_trunc closed form {Mdl['Rt_closed_Mpc']:.3f} Mpc (S-claim {r['R_trunc_claim_z0_Mpc']:.3f} Mpc at z 0); KA-Q1 numeric R_trunc / share / R_ta: " + "; ".join(f"{x['logMb']}: {x['R_trunc_Mpc']:.3f} Mpc, {x['share_over_Mb']:.1f} M_b, R_ta {x['R_ta_Mpc']:.2f}" for x in kq) + f" -> {'PASS' if r['KA_Q1']['pass_'] else 'FAIL'}")
    # Q1 conservation
    per = gsmf(B.h); RHO_D_SUN = B.RHO_D0 * MPC ** 3 / MS; w = np.array([per(m) for m in LF])
    qg = float(np.trapz(w * np.array([Mdl["share"](10 ** m * MS)[0] / MS for m in LF]), LF)) / RHO_D_SUN
    qc = {f"z {z}": float(np.trapz(w * np.array([Mph(Mdl["Rt_claim"](z), 10 ** m * MS, a0) / MS for m in LF]), LF)) / RHO_D_SUN for z in (0.5, 1.0, 2.0)}
    r["Q1"] = dict(q_graded_all_z=qg, q_claim=qc, status="PASS" if qg <= 1 else "FAIL")
    P(f"[{f}] Q1 q (graded share, z-independent) {qg:.3f} -> {r['Q1']['status']}; S-claim " + " ".join(f"{k} {v:.3f}" for k, v in qc.items()))
    # Q2 KiDS / SPARC
    Rt_g = lambda Mb_kg: rtrunc(Mb_kg, a0, Mdl["share"](Mb_kg)[0]); Rt_c = lambda Mb_kg: Mdl["Rt_claim"](0.0)
    k_g, k_c, k_0 = kids(a0, Rt_g), kids(a0, Rt_c), kids(a0, lambda m: math.inf)
    s_0 = sparc(f, a0, lambda m: math.inf); s_g = sparc(f, a0, Rt_g); s_c = sparc(f, a0, Rt_c)
    st = lambda s: "PASS" if (s["all"]["rms"] <= s_0["all"]["rms"] + 0.010 and abs(s["all"]["mean"]) <= 0.05 and s["massive"]["rms"] <= s_0["massive"]["rms"] + 0.010 and abs(s["massive"]["mean"]) <= 0.05) else "FAIL"
    s_g["status"], s_c["status"] = st(s_g), st(s_c)
    Mdl5 = model(B, f, F_SHEET * 5); k_5 = kids(a0, lambda Mb_kg: rtrunc(Mb_kg, a0, Mdl5["share"](Mb_kg)[0]))
    r.update(Q2_KiDS=k_g, Q2_SPARC=s_g, S_claim=dict(kids=k_c, sparc=s_c), KA_Q2=dict(kids_trunc_off=k_0["max_abs"], pass_=bool(k_0["max_abs"] < 1e-9)), MQ1_fsheet_x5=dict(kids=k_5, R_trunc_Mpc=Mdl5["Rt_closed_Mpc"]))
    P(f"[{f}] Q2 KiDS {k_g['status']} max {k_g['max_abs']:.3f} ({k_g['n_over']}/59, min {k_g['min']:+.3f}); SPARC {s_g['status']} rms {s_g['all']['rms']:.4f} (line {s_0['all']['rms']+0.010:.4f}; truncated inside R_last: {s_g['n_truncated_inside_Rlast']})")
    P(f"[{f}] S-claim ({r['R_trunc_claim_z0_Mpc']:.2f} Mpc): KiDS {k_c['status']} max {k_c['max_abs']:.3f} ({k_c['n_over']}/59); SPARC {s_c['status']} rms {s_c['all']['rms']:.4f}; MQ1 f_sheet x5 (R_trunc {Mdl5['Rt_closed_Mpc']:.2f}): KiDS max {k_5['max_abs']:.3f} ({k_5['n_over']}/59); KA-Q2 trunc off {k_0['max_abs']:.1e}")
    RES[f] = r
# Q3 / Q5 via PD1's halo rule at 0.40 of the share, prefactor 1
env = dict(os.environ, PD1_SHARE=f"{CL_FRAC * 5.41:g}", PD1_FCPRE="1.0", OMP_NUM_THREADS="1")
cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.join(PD1, "pd1_a1.py")], capture_output=True, text=True, env=env)
if cp.returncode != 0: raise RuntimeError(cp.stderr[-1500:])
A = json.load(open(os.path.join(PD1, f"pd1_a1_share{CL_FRAC * 5.41:g}_fcpre1.0.json"))); A1q = json.load(open(os.path.join(PD1, "pd1_a1_share5.41_fcpre1.0.json")))
for f in FOOTS:
    x = A[f]["P3_XCOP"]; g = A[f]["P3_groups"]; gb = [b for b in x["bins"] if b["graded"]]
    RES[f].update(Q3_groups=g, Q3_XCOP=x, Q5_gaslocked_reported=A[f]["P5_Bullet"], MQ2_fraction1=dict(xcop=A1q[f]["P3_XCOP"]["status"], groups=A1q[f]["P3_groups"]["status"]))
    P(f"[{f}] Q3 groups {g['status']} {g['fst0']['n_pass']}/{g['fst1']['n_pass']}; X-COP {x['status']} {x['mean']:+.3f}; f_miss " + " / ".join(f"{b['f_miss']:.2f}" for b in gb) + " vs TR1 0.71 / 0.66 / 0.58"
      + f"; MQ2 (fraction 1.0, PD1 bracket): X-COP {A1q[f]['P3_XCOP']['status']}, groups {A1q[f]['P3_groups']['status']}")
# Q5 graded: galaxy-traced Newtonian
src2 = open(os.path.join(PD1, "pd1_a1.py")).read(); n2 = {"__file__": os.path.join(PD1, "pd1_a1.py"), "__name__": "pd1_a1_lib"}
os.environ["PD1_SHARE"] = f"{CL_FRAC * 5.41:g}"; os.environ["PD1_FCPRE"] = "1.0"
exec(compile(src2[:src2.index("RES = dict(amendment=A1")], "pd1_a1_prefix", "exec"), n2)
def call(arg):
    cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.join(PD1, "pd1_a2.py"), "nchild", arg, "newton"], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
    line = [l for l in cp.stdout.splitlines() if l.startswith("PD1CHILD ")]
    if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
    return json.loads(line[0][9:])
o0 = call("{}"); mm = o0["masses"]; Mb = [mm["M_gas_sub"][j] + mm["M_star_sub"][j] for j in range(2)]; Md = {}; inf = {}
for f in FOOTS:
    B = n2["footing_bg"](f); T3 = n2["share_table"](B, A0[f], 0.3); v_ = []; ii = []
    for j in range(2):
        S = n2["system"](B, f, T3, Mb[j], z=0.3); R2 = S["R200_kpc"] * KPC; ph = min(S["W"] * Mph(R2, Mb[j] * MS, A0[f]) / MS, S["E"]); md = ph + S["core"](S["R200_kpc"]) + n2["rem_in"](S, R2) / MS
        v_.append(md); ii.append(dict(M_b=Mb[j], f_core=S["f_core"], dark_in_R200=md))
    Md[f] = v_; inf[f] = ii
on = call(json.dumps(Md))
for f in FOOTS:
    b = on[f]["row"]; RES[f]["Q5_Bullet"] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", row=b, subclusters=inf[f])
    P(f"[{f}] Q5 Bullet (galaxy-traced, Newtonian) {b['label']}: cls {b['cls']}; M300 Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; dark in R200 " + ", ".join(f"{x['dark_in_R200']:.2e}" for x in inf[f]) + f"; gas-locked reading {RES[f]['Q5_gaslocked_reported']['status']}")
RES["Q6"] = dict(screening_at_Saturn=(9.58 * 4.848e-6 / 22.0) ** 4, note="(r/L*)^4 at 9.58 AU, L* 22 pc; Cassini and moving Sun carried from the record's v3s (MS3 PASS scoped)")
P(f"Q6 screening factor (r/L*)^4 at Saturn {RES['Q6']['screening_at_Saturn']:.1e}; Cassini / moving Sun carried")
for f in FOOTS:
    st = {"Q1": RES[f]["Q1"]["status"], "Q2 KiDS": RES[f]["Q2_KiDS"]["status"], "Q2 SPARC": RES[f]["Q2_SPARC"]["status"], "Q3 groups": RES[f]["Q3_groups"]["status"], "Q3 X-COP": RES[f]["Q3_XCOP"]["status"], "Q4 (carried)": "PASS", "Q5 Bullet": RES[f]["Q5_Bullet"]["status"]}
    fails = [k for k, v in st.items() if v != "PASS"]; RES[f]["label"] = dict(status=st, label="PASS" if not fails else "FAIL", first_fail=fails[0] if fails else None)
    P(f"[{f}] PD2 LABEL {RES[f]['label']['label']}; first failing gate {RES[f]['label']['first_fail']}; " + ", ".join(f"{k} {v}" for k, v in st.items()))
json.dump(RES, open(os.path.join(HERE, "pd2.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "pd2.out"), "w").write("\n".join(L) + "\n")
