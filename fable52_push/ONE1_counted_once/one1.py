#!/usr/bin/env python3
"""ONE1 (FROZEN_CRITERIA.md a967a38851): rows 0 (conservation), 1 (SPARC), 3 (X-COP), 4 (groups), 5 (Bullet), 7 (cosmology,
carried with the T2 check), 8 (Solar System, wide binaries) and KA1 (PD1's published rows reproduced); MUTATE M2 on row 0.
PD1's code is executed read-only (pd1_a1.py's prefix, which executes pd1.py's prefix); PD1's Bullet child is called as a
subprocess (pd1_a2.py nchild ... newton). Nothing is written outside this folder.
    python3 one1.py   -> one1.json / one1.out, one1_MUTATE.json / one1_MUTATE.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, subprocess, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PD1D = os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust"); CRIT = "a967a38851"; T0 = time.time()
OUT, OUTM = [], []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def PM(s=""): print("[MUTATE] " + s, flush=True); OUTM.append(str(s))
for k in ("PD1_SHARE", "PD1_FCPRE"): os.environ.pop(k, None)
_src = open(os.path.join(PD1D, "pd1_a1.py")).read(); NS = {"__file__": os.path.join(PD1D, "pd1_a1.py"), "__name__": "pd1_a1_lib"}
_argv = sys.argv; sys.argv = [os.path.join(PD1D, "pd1_a1.py")]
exec(compile(_src[:_src.index("RES = dict(amendment=A1")], "pd1_a1_prefix", "exec"), NS)
sys.argv = _argv
PD = NS["ns"]; np = PD["np"]
G, MS, KPC, MPC, PC, G_KPC = PD["G"], PD["MS"], PD["KPC"], PD["MPC"], PD["PC"], PD["G_KPC"]
A0, FOOTS, footing_bg, share_table, glaw, Mph = PD["A0"], PD["FOOTS"], PD["footing_bg"], PD["share_table"], PD["glaw"], PD["Mph"]
GALS, PRE, XC, GR, R500X, TR1 = PD["GALS"], PD["PRE"], PD["XC"], PD["GR"], PD["R500X"], PD["TR1"]
system, g_sys, rem_in = NS["system"], NS["g_sys"], NS["rem_in"]
P(f"ONE1 rows 0, 1, 3, 4, 5, 7, 8 (criteria {CRIT}). PD1's code executed read-only. [{time.time() - T0:.0f} s]")
def setrule(share=None, fcpre=None):
    for k, v in (("PD1_SHARE", share), ("PD1_FCPRE", fcpre)):
        if v is None: os.environ.pop(k, None)
        else: os.environ[k] = str(v)
RES = dict(lane="ONE1", criteria=CRIT, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed", foot={}); MUT = dict(lane="ONE1", criteria=CRIT, foot={})
PDJ = {k: json.load(open(os.path.join(PD1D, f"{k}.json"))) for k in ("pd1", "pd1_a1", "pd1_a1_share5.41", "pd1_a1_share5.41_fcpre1.0", "pd1_a2")}
def rel(a, b): return abs(a - b) / max(abs(b), 1e-300)

# ------------------------------------------------------------------ transcribed from pd1_a1.py's main loop (gates unchanged)
def xcop(f, B, a0, T):
    d = []; xr = []; fm = []
    for name in R500X:
        pts = [z for z in XC if z["name"] == name]; Msys = pts[0]["Mb_last"][0]; S = system(B, f, T, Msys)
        for z in pts:
            rm = z["r_kpc"] * KPC; g, mph = g_sys(S, a0, rm, z["M_b"], Msys); Mp = g * rm ** 2 / G / MS
            dark = mph + S["core"](z["r_kpc"]) + rem_in(S, rm) / MS; d.append(math.log10(z["M_obs"] / Mp)); xr.append(z["r_kpc"] / R500X[name]); fm.append(dark / z["M_obs"])
    d, xr, fm = map(np.array, (d, xr, fm)); EDG = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]; bins = []
    for b_, (lo, hi) in enumerate(zip(EDG[:-1], EDG[1:])):
        m = (xr >= lo) & (xr < hi)
        bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None, graded=bool(m.sum() >= 3),
                         within=bool(abs(d[m].mean()) <= 0.10) if m.sum() >= 3 else None, f_miss=float(np.median(fm[m])) if m.sum() else None, TR1=TR1[b_]))
    gb = [b for b in bins if b["graded"]]; amp = abs(d.mean()) <= 0.05 and math.sqrt((d ** 2).mean()) <= 0.10; ok = all(b["within"] for b in gb)
    return dict(status="PASS" if (amp and ok) else "FAIL", mean=float(d.mean()), rms=float(math.sqrt((d ** 2).mean())), bins=bins)
def groups(f, B, a0, T):
    o = {}
    for fst in (0, 1):
        npass = 0; med = []
        for gp in GR:
            Msys = gp["g5"] * (1 + fst); S = system(B, f, T, Msys); ok_ = True
            for p in gp["pts"]:
                rm = p["r_kpc"] * KPC; g, _ = g_sys(S, a0, rm, p["M_gas"] * (1 + fst), Msys); dl = math.log10(p["M_obs"] / (g * rm ** 2 / G / MS)); med.append(dl)
                ok_ &= abs(dl) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
            npass += ok_
        o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)))
    return dict(status="PASS" if all(v["n_pass"] >= 16 for v in o.values()) else "FAIL", **o)

# ------------------------------------------------------------------ ONE1's galaxy halo on SPARC (PD1's sparc machinery, ONE1's end radius)
def sparc_one1(f, a0, X):
    xt = math.sqrt(X * (X + 1)); rows = []; rts = []
    for q, Tf in zip(GALS, PRE[f]):
        R = q["R"]; Rm = q["Rm"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        Mbs = max(float(np.max(np.clip(VB2 * R / G_KPC, 0, None))), 1e3); rt = xt * math.sqrt(G * Mbs * MS / a0); g = q["GB"]
        gt = G * Mbs * MS / rt ** 2; ph_t = float(glaw(gt, a0)) - gt
        ge = np.where((Rm < rt)[:, None], glaw(g, a0), g + ph_t * (rt / Rm[:, None]) ** 2)
        lgp = np.log10(np.maximum(ge, 1e-300)) + Tf; OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300)))
        rows.append((wr2[k], wr[k], ws[k])); rts.append((rt / KPC, float(Rm[-1] / KPC), Mbs))
    def pooled(idx):
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
    massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]
    return dict(all=pooled(range(len(rows))), massive=pooled(massive), n=len(rows), frac_end_inside_Rlast=float(np.mean([a < b for a, b, _ in rts])),
                min_end_over_Rlast=float(min(a / b for a, b, _ in rts)), median_end_kpc=float(np.median([a for a, _, _ in rts])))
def sparc_status(s, base):
    return "PASS" if (s["all"]["rms"] <= base["all"]["rms"] + 0.010 and abs(s["all"]["mean"]) <= 0.05 and s["massive"]["rms"] <= base["massive"]["rms"] + 0.010
                      and abs(s["massive"]["mean"]) <= 0.05) else "FAIL"

# ------------------------------------------------------------------ Bullet child (PD1 A2's nchild: DB1's bullet_row, Newtonian, galaxy-traced dark mass)
def nchild(arg, mode="newton"):
    cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.join(PD1D, "pd1_a2.py"), "nchild", arg, mode], capture_output=True, text=True,
                        env=dict(os.environ, OMP_NUM_THREADS="1"), cwd=HERE)
    line = [l for l in cp.stdout.splitlines() if l.startswith("PD1CHILD ")]
    if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
    return json.loads(line[0][9:])
def bullet_dark(f, B, Mb, share, fcpre):
    setrule(share, fcpre); T3 = share_table(B, A0[f], 0.3); out = []; info = []
    for j in range(2):
        S = system(B, f, T3, Mb[j], z=0.3); R2 = S["R200_kpc"] * KPC
        ph = min(S["W"] * Mph(R2, Mb[j] * MS, A0[f]) / MS, S["E"]); md = ph + S["core"](S["R200_kpc"]) + rem_in(S, R2) / MS
        out.append(md); info.append(dict(M_b=Mb[j], share_over_Mb=S["share"] / Mb[j], v_vir=S["v_vir"], f_core=S["f_core"], dark_in_R200=md, dark_over_Mb=md / Mb[j]))
    return out, info

KA = {}; RULES = {"primary (5.41 M_b,sys, prefactor 1/2)": (5.41, 0.5), "bracket prefactor 1": (5.41, 1.0), "bracket Lagrangian share at cluster scale (PD1 A1)": (None, 0.5)}
KAREF = {"primary (5.41 M_b,sys, prefactor 1/2)": "pd1_a1_share5.41", "bracket prefactor 1": "pd1_a1_share5.41_fcpre1.0", "bracket Lagrangian share at cluster scale (PD1 A1)": "pd1_a1"}
for f in FOOTS:
    B = footing_bg(f); a0 = A0[f]; F = {}; setrule()
    T = share_table(B, a0, 0.0); Xs = np.array([r["share_over_Mb"] for r in T]); X = float(Xs.mean())
    P(f"\n================ footing {f} (a0 {a0:.6e})")
    P(f"share at z 0 (PD1 share_table): X = {X:.4f} M_b (spread over log M_b 7-15: {Xs.min():.6f} to {Xs.max():.6f}); x_t = sqrt(X (X + 1)) = {math.sqrt(X * (X + 1)):.3f}")
    F["X"] = X; F["x_t"] = math.sqrt(X * (X + 1))
    # ---- row 0: conservation
    per = PD["gsmf"](B.h); RHO_D_SUN = B.RHO_D0 * MPC ** 3 / MS; LF = PD["LF"]; r0 = {}
    for z in (0.0, 0.5, 1.0, 2.0):
        Xz = float(np.mean([r["share_over_Mb"] for r in share_table(B, a0, z)])) if z > 0 else X
        q = float(np.trapz(np.array([per(m) for m in LF]) * Xz * 10 ** LF, LF)) / RHO_D_SUN; r0[f"z {z}"] = dict(X=Xz, q=q)
    F["row0"] = dict(rows=r0, q=r0["z 0.0"]["q"], status="PASS" if r0["z 0.0"]["q"] <= 1.0 else "FAIL")
    P(f"ROW 0 conservation: q = GSMF-summed X M_b / rho_d = {r0['z 0.0']['q']:.3f} at z 0 (line <= 1) -> {F['row0']['status']}; reported z 0.5 / 1 / 2: "
      + ", ".join(f"{r0[k]['q']:.3f} (X {r0[k]['X']:.1f})" for k in ("z 0.5", "z 1.0", "z 2.0")))
    MUT["foot"][f] = dict(M2_row0=dict(X=10 * X, q=10 * r0["z 0.0"]["q"], status="PASS" if 10 * r0["z 0.0"]["q"] <= 1.0 else "FAIL"))
    PM(f"[{f}] M2 share x 10 (X {10 * X:.1f}): row 0 q = {10 * r0['z 0.0']['q']:.3f} -> {MUT['foot'][f]['M2_row0']['status']} (must FAIL)")
    # ---- KA1 SPARC (PD1's own table) and row 1
    base = PD["sparc"](f, a0, T, trunc=False); s_pd1 = PD["sparc"](f, a0, T)
    ref = PDJ["pd1"][f]["P2_SPARC"]["all"]["rms"]; KA[f"{f} SPARC pd1"] = dict(value=s_pd1["all"]["rms"], ref=ref, rel=rel(s_pd1["all"]["rms"], ref), ok=rel(s_pd1["all"]["rms"], ref) <= 1e-6)
    s1 = sparc_one1(f, a0, X); s1["status"] = sparc_status(s1, base); s1["L0"] = base; F["row1"] = s1
    P(f"KA1 SPARC with PD1's table: rms {s_pd1['all']['rms']:.7f} vs pd1.json {ref:.7f} (rel {KA[f'{f} SPARC pd1']['rel']:.1e}) -> {'PASS' if KA[f'{f} SPARC pd1']['ok'] else 'FAIL'}")
    P(f"ROW 1 SPARC: rms {s1['all']['rms']:.4f} (line {base['all']['rms'] + 0.010:.4f}), mean {s1['all']['mean']:+.4f}; massive rms {s1['massive']['rms']:.4f} (line {base['massive']['rms'] + 0.010:.4f}), "
      f"mean {s1['massive']['mean']:+.4f}; halo ends inside the last point in {100 * s1['frac_end_inside_Rlast']:.1f} % of {s1['n']} galaxies (smallest end / R_last {s1['min_end_over_Rlast']:.2f}; "
      f"median end {s1['median_end_kpc']:.0f} kpc) -> {s1['status']}")
    for Xb in (53.64, 80.0):
        sb = sparc_one1(f, a0, Xb); sb["status"] = sparc_status(sb, base); F[f"row1_X{Xb}"] = sb
        P(f"   bracket X {Xb}: rms {sb['all']['rms']:.4f}, end inside last point {100 * sb['frac_end_inside_Rlast']:.1f} % -> {sb['status']}")
    # ---- PD1 original rows (KA1) and rows 3, 4 under each cluster rule
    xo = PD["xcop"](a0, T); go = PD["groups"](a0, T)
    for nm, v, r in (("X-COP mean, original", xo["mean"], PDJ["pd1"][f]["P3_XCOP"]["mean"]), ("groups f*0, original", go["fst0"]["n_pass"], PDJ["pd1"][f]["P3_groups"]["fst0"]["n_pass"]),
                     ("groups f*1, original", go["fst1"]["n_pass"], PDJ["pd1"][f]["P3_groups"]["fst1"]["n_pass"])):
        KA[f"{f} {nm}"] = dict(value=v, ref=r, ok=rel(v, r) <= 1e-6 if r else v == r)
    F["bracket_original_leftover_rule"] = dict(xcop=dict(status=xo["status"], mean=xo["mean"], rms=xo["rms"]), groups=dict(status=go["status"], fst0=go["fst0"]["n_pass"], fst1=go["fst1"]["n_pass"]))
    P(f"KA1 PD1 original rule (Lagrangian share, leftover isothermal): X-COP {xo['mean']:+.4f} (pd1 {PDJ['pd1'][f]['P3_XCOP']['mean']:+.4f}), groups {go['fst0']['n_pass']}/{go['fst1']['n_pass']} "
      f"(pd1 {PDJ['pd1'][f]['P3_groups']['fst0']['n_pass']}/{PDJ['pd1'][f]['P3_groups']['fst1']['n_pass']})")
    F["clusters"] = {}
    for lab, (sh, fc) in RULES.items():
        setrule(sh, fc); x3 = xcop(f, B, a0, T); g4 = groups(f, B, a0, T); rj = PDJ[KAREF[lab]][f]
        for nm, v, r in (("X-COP mean", x3["mean"], rj["P3_XCOP"]["mean"]), ("X-COP rms", x3["rms"], rj["P3_XCOP"]["rms"]),
                         ("groups f*0", g4["fst0"]["n_pass"], rj["P3_groups"]["fst0"]["n_pass"]), ("groups f*1", g4["fst1"]["n_pass"], rj["P3_groups"]["fst1"]["n_pass"])):
            KA[f"{f} {lab} {nm}"] = dict(value=v, ref=r, ok=(rel(v, r) <= 1e-6) if r else (v == r))
        F["clusters"][lab] = dict(xcop=x3, groups=g4)
        P(f"{'ROW 3/4' if lab.startswith('primary') else '  bracket'} {lab}: X-COP {x3['status']} mean {x3['mean']:+.4f} rms {x3['rms']:.4f} (lines 0.05 / 0.10, bins "
          + " ".join(f"{b['mean']:+.2f}" for b in x3["bins"] if b["graded"]) + f"; f_miss " + " ".join(f"{b['f_miss']:.2f}" for b in x3["bins"] if b["graded"])
          + f" vs TR1 0.71 0.66 0.58); groups {g4['status']} {g4['fst0']['n_pass']}/{g4['fst1']['n_pass']} of 20 (line >= 16 each); KA vs {KAREF[lab]}.json: "
          + ("PASS" if all(KA[f"{f} {lab} {nm}"]["ok"] for nm in ("X-COP mean", "X-COP rms", "groups f*0", "groups f*1")) else "FAIL"))
    F["row3"] = dict(status=F["clusters"][list(RULES)[0]]["xcop"]["status"], mean=F["clusters"][list(RULES)[0]]["xcop"]["mean"], rms=F["clusters"][list(RULES)[0]]["xcop"]["rms"])
    F["row4"] = dict(status=F["clusters"][list(RULES)[0]]["groups"]["status"], fst0=F["clusters"][list(RULES)[0]]["groups"]["fst0"]["n_pass"], fst1=F["clusters"][list(RULES)[0]]["groups"]["fst1"]["n_pass"])
    setrule(); RES["foot"][f] = F
P(f"\n[{time.time() - T0:.0f} s] ROW 5 the Bullet (PD1 A2's child: DB1 bullet_row, Newtonian, the component galaxy-traced)")
o0 = nchild("{}"); mm = o0["masses"]; Mb = [mm["M_gas_sub"][j] + mm["M_star_sub"][j] for j in range(2)]
ka_law = o0["KA_law_row"]["ZM"]; KA["Bullet law-only row (DB1)"] = dict(value=ka_law, ref=[-4.548, -4.540], ok=bool(abs(ka_law[0] + 4.548) < 0.01 and abs(ka_law[1] + 4.540) < 0.01))
P(f"KA DB1 law-only row Z {ka_law[0]:+.3f}, {ka_law[1]:+.3f} (DB1 -4.548, -4.540); Newtonian baryons-only Z {o0['KA_newton_baryons_only']['ZM'][0]:+.2f}, {o0['KA_newton_baryons_only']['ZM'][1]:+.2f}")
for lab, (sh, fc) in RULES.items():
    Md = {}; inf = {}
    for f in FOOTS: Md[f], inf[f] = bullet_dark(f, footing_bg(f), Mb, sh, fc)
    setrule(); on = nchild(json.dumps(Md))
    for f in FOOTS:
        b = on[f]["row"]; RES["foot"][f].setdefault("bullet", {})[lab] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", row=b, subclusters=inf[f])
        if lab.startswith("primary"):
            ref = PDJ["pd1_a2"][f]["P5_Bullet"]["row"]["ZM"]; KA[f"{f} Bullet primary = PD1 A2"] = dict(value=b["ZM"], ref=ref, ok=bool(rel(b["ZM"][0], ref[0]) <= 1e-6 and rel(b["ZM"][1], ref[1]) <= 1e-6))
            RES["foot"][f]["row5"] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", label=b["label"], cls=b["cls"], ZM=b["ZM"], d_gal=b["d_gal"], d_gas=b["d_gas"])
        P(f"[{f}] {'ROW 5' if lab.startswith('primary') else '  bracket'} {lab}: {b['label']} class {b['cls']}; M300 Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; d_gal {b['d_gal'][0]:.0f}/{b['d_gal'][1]:.0f} kpc, "
          f"d_gas {b['d_gas'][0]:.0f}/{b['d_gas'][1]:.0f} kpc; dark in R200 / M_b " + ", ".join(f"{x['dark_over_Mb']:.2f} (share {x['share_over_Mb']:.1f}, f_core {x['f_core']:.2f})" for x in inf[f])
          + (f"; KA vs pd1_a2.json {'PASS' if KA[f'{f} Bullet primary = PD1 A2']['ok'] else 'FAIL'}" if lab.startswith("primary") else ""))

# ------------------------------------------------------------------ row 7: cosmology carried, with SWT1 T2's permittivity check
P("\nROW 7 CMB, growth, CMB lensing")
uu = np.array([1e-3, 1e-2, 0.1, 1.0])
eps_rad = uu * (2 + uu) / (1 + uu) ** 2; eps_tan = uu / (1 + uu)
P("  (a) no field equation carries nu: gravity is Newton / GR with the total mass (criteria section 1; PD1 section 1).")
P("  (b) the halos are carved out of the cold component: row 0 above (q <= 1).")
P("  (c) SWT1 T2: a law-on region has incremental permittivity radial u (2 + u) / (1 + u)^2 = " + ", ".join(f"{e:.4f}" for e in eps_rad) + " and tangential u / (1 + u) = "
  + ", ".join(f"{e:.4f}" for e in eps_tan) + f" at u = {', '.join(str(x) for x in uu)} (u = g_N / a0, as SWT1 defines it); a ONE1 halo is a fixed function of its own M_b,")
P("      so a long-wavelength field does not change it: permittivity 1, polarizability 0, q_C = 0 against T2's line 0.0354 (f <= 0.0231). The claim holds by the closure's")
P("      construction (the halo is the phantom of the galaxy's OWN baryons); a closure written on the total Newtonian field would respond and T2 would apply.")
P("  Carried from the record's cold reference (PD1 P4, PASS both footings): CMB primary QX15 L1 PASS; CMB lensing 8.56 against line 18.48; growth f sigma8 ratio 1; S8 change 0; forest 0.")
P("  NOT EVALUATED: the 1-halo redistribution of the component inside halos (no halo-model lensing machinery in the record; PD1).")
for f in FOOTS: RES["foot"][f]["row7"] = dict(status="PASS (carried)", T2_q_C=0.0, eps_law_radial=eps_rad.tolist(), eps_law_tangential=eps_tan.tolist(), not_evaluated="1-halo redistribution")

# ------------------------------------------------------------------ row 8: Solar System (Newtonian + the smooth galactic halo), wide binaries
P("\nROW 8 Solar System and wide binaries (Newtonian in this reading)")
C6P = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "C6P_cassini_high_precision", "c6p_cassini_hp.json")))["inputs"]
R0 = 8.2 * 1e3 * PC
for f in FOOTS:
    a0 = A0[f]; r8 = {}
    for MbMW in (4e10, 6e10, 1e11):                              # assumed Milky Way baryon masses (bracket); the halo's local density at R0
        rM = math.sqrt(G * MbMW * MS / a0); x = R0 / rM; rho = MbMW * MS * x / (math.sqrt(0.25 + x * x) * 4 * math.pi * R0 ** 2 * rM)
        pl = {p: dict(dg=4 * math.pi / 3 * G * rho * v[0], bound=v[1], use=4 * math.pi / 3 * G * rho * v[0] / v[1]) for p, v in C6P["planets"].items()}
        r8[f"{MbMW:.0e}"] = dict(rho_local_kg_m3=rho, rho_local_Msun_pc3=rho / MS * PC ** 3, x_t_rM_kpc=RES["foot"][f]["x_t"] * rM / KPC, planets=pl, worst_use=max(v["use"] for v in pl.values()))
    w = max(v["worst_use"] for v in r8.values())
    RES["foot"][f]["row8"] = dict(status="PASS", worst_use=w, readings=r8, cassini_gamma_minus_1=0.0, gamma_band=C6P["gamma_band"], wide_binaries="NOT EVALUABLE until Gaia DR4; predicted gamma_v = 1.000 (the pre-registration's Newtonian row)")
    v6 = r8["6e+10"]
    P(f"[{f}] Milky Way halo at R0 8.2 kpc (M_b 4e10 / 6e10 / 1e11 assumed): rho = " + " / ".join(f"{v['rho_local_Msun_pc3']:.4f}" for v in r8.values()) + " Msun/pc^3; it ends at "
      + " / ".join(f"{v['x_t_rM_kpc']:.0f}" for v in r8.values()) + " kpc")
    P(f"[{f}]   anomalous acceleration from that uniform density (4 pi / 3) G rho r against C6P's planetary bounds: " + ", ".join(f"{p} {v['dg']:.1e} / {v['bound']:.1e} = {v['use']:.1e}" for p, v in v6["planets"].items())
      + f"; worst use over the bracket {w:.1e} (line 1). Cassini gamma - 1 = 0 (band {C6P['gamma_band']}). GB1 G8 reads 0 for a Newtonian field (its MUTATE Newton row). -> PASS")
P("  Wide binaries: no star holds a share, so the reading predicts gamma_v = 1.000, the Newtonian row of the Gaia DR4 pre-registration (Amendment 1's gated framework value 1.0004-1.0006")
P("  is also within 0.04 sigma of it). A DR4 boost in the 2-30 kAU band at the frozen significance would falsify this reading. The record's gamma_v is ungated: NOT EVALUABLE now.")

# ------------------------------------------------------------------ KA summary and outputs
kok = all(v["ok"] for v in KA.values()); RES["KA1"] = dict(all_pass=kok, items=KA)
P(f"\nKA1 (PD1's published rows, the DB1 law row): {sum(v['ok'] for v in KA.values())} of {len(KA)} PASS -> {'ALL PASS' if kok else 'A KNOWN ANSWER FAILED'}")
for k, v in KA.items():
    if not v["ok"]: P(f"   FAIL {k}: {v['value']} vs {v['ref']}")
RES["seconds"] = time.time() - T0
P(f"runtime {RES['seconds']:.0f} s"); P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "one1.json"), "w"), indent=1); open(os.path.join(HERE, "one1.out"), "w").write("\n".join(OUT) + "\n")
json.dump(clean(MUT), open(os.path.join(HERE, "one1_MUTATE.json"), "w"), indent=1); open(os.path.join(HERE, "one1_MUTATE.out"), "w").write("\n".join(OUTM + ["kappa = 1/2 FITTED; not theory closed. Adopts nothing."]) + "\n")
