#!/usr/bin/env python3
"""X80 AMENDMENT A1, reported line 4: the no-floor rule with eta below 1e12 from X80's measured ratios; SPARC line on both backgrounds, LS1's table by V_flat against ET1.
    python3 nf1_native_read.py           # rho10, rho11 from X80's x80_converged.json
    python3 nf1_native_read.py --check   # rho10 = rho11 = 1 must reproduce NF1's N0
    python3 nf1_native_read.py --rho r10 r11   # a stated what-if, reported as such; not a measurement
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, subprocess, sys
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE); CE1 = os.path.join(FRB, "CE1_converged_eta_grade"); SLOPE = "2.7774425603108597"; FS = "0.034"; CHECK = "--check" in sys.argv; OUTL = []
def Pn(s): print(s, flush=True); OUTL.append(s)
HYP = "--rho" in sys.argv
if CHECK: r10, r11, TAGN = 1.0, 1.0, "NF1_NATIVE_CHECK"
elif HYP: _i = sys.argv.index("--rho"); r10, r11 = float(sys.argv[_i + 1]), float(sys.argv[_i + 2]); TAGN = f"NF1_NATIVE_HYP_{r10:g}_{r11:g}"   # a what-if, never X80's measurement
else:
    J = json.load(open(os.path.join(FRB, "X80_low_mass_floor_emergence", "x80_converged.json")))
    if "r10" not in J: raise SystemExit(f"NOT YET: {J.get('reading')}")
    r10, r11, TAGN = J["r10"], J["r11"], "NF1_NATIVE"
TABV = [math.log10(r10), math.log10(r11), 0.0]; A4T = os.path.join(CE1, f"CE1_A4_med_fs{FS}_cf_table.json"); TAB = A4T if os.path.exists(A4T) else os.path.join(CE1, f"CE1_med_fs{FS}_cf_table.json"); CER = os.path.join(CE1, "ce1_a4_results.json"); CER = CER if os.path.exists(CER) else os.path.join(CE1, "ce1_results.json")
names = [f"x74_fs{float(FS):g}_nat_s{float(SLOPE):.4f}.out", f"x74_results_fs{float(FS):g}_nat_s{float(SLOPE):.4f}.json"]
env = dict(os.environ, CN1_R="1.0", CN1_MODE="off", NF1_ON="1", NF1_TAB=json.dumps(TABV), X74_CF=TAB, X73_FSTAR=FS, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
p = subprocess.run(["nice", "-n", "15", sys.executable, "nf1_x74.py"], cwd=FHERE, env=env, capture_output=True, text=True); open(os.path.join(FHERE, f"{TAGN}.log"), "w").write(p.stdout + p.stderr); o = {}
for n in names:
    f = os.path.join(FHERE, n)
    if os.path.exists(f):
        d = os.path.join(FHERE, f"{TAGN}_{n}"); os.replace(f, d)
        if d.endswith(".json"): o = json.load(open(d)); o["x74"]["cf_src"] = os.path.basename(o["x74"]["cf_src"]); json.dump(o, open(d, "w"), indent=1)
if not o: raise SystemExit(f"NOT DECIDED: the grader wrote no results (exit {p.returncode}): {p.stderr[-400:]}")
q = {t: dict(U=v["U_median"], rms=v["rms"], line=v["line"]) for t, v in o["footings"]["canonical"]["sparc"].items()}; ok = all(v["line"] for v in q.values()); lab = "NATIVE N PASSES THE SPARC LINE" if ok else "NATIVE N FAILS THE SPARC LINE"
Pn(("WHAT-IF, NOT A MEASUREMENT. " if HYP else "") + f"NF1 native read: rho10 {r10:.3f}, rho11 {r11:.3f}, table {os.path.basename(TAB)}, f* {FS}; kappa = 1/2 FITTED; not theory closed"); Pn(f"  SPARC U {q['A_c2b_refit']['U']:.2f}/{q['B_cfg886_bg']['U']:.2f} rms {q['A_c2b_refit']['rms']:.4f}/{q['B_cfg886_bg']['rms']:.4f}; groups Z {o['footings']['canonical']['groups']['Z']:+.2f}; failing {o['footings']['canonical']['failing']}"); Pn(f"LABEL (SPARC only): {lab}")
RES = dict(r10=r10, r11=r11, table=os.path.basename(TAB), sparc=q, label=lab, failing=o["footings"]["canonical"]["failing"])
if CHECK:
    N0 = json.load(open(os.path.join(FHERE, f"NF1_N0_x74_results_fs{FS}_nat_s2.7774.json")))["footings"]; dk = 0.0
    for f in ("canonical", "alt"):
        for t, v in o["footings"][f]["sparc"].items(): dk = max(dk, abs(v["U_median"] - N0[f]["sparc"][t]["U_median"]), abs(v["rms"] - N0[f]["sparc"][t]["rms"]))
        for hk, c in o["footings"][f]["clusters"]["cells"].items():
            for k, w in c.items(): dk = max(dk, abs(w["pred"] - N0[f]["clusters"]["cells"][hk][k]["pred"]))
    Pn(f"K rho 1, 1 reproduces N0: max |d| {dk:.1e}: {'PASS' if dk <= 1e-9 else 'FAIL'}"); RES["K"] = dk
ETAJ = json.load(open(CER))["eta"]; ETAV = [ETAJ[str(e)]["med"] for e in (12, 13, 14)]; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
LSD = os.path.join(FRB, "LS1_lstar_analogs"); S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(LSD, "ls1_analogs.py"); OUTK = OUTL; PK = Pn
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec")); HERE = FHERE; OUTL = OUTK; Pn = PK
def Srule(M): Mt = M / FC; return FC * float(np.interp(math.log10(Mt), [12, 13, 14], ETAV)) * 10 ** float(np.interp(math.log10(Mt), [10.0, 11.0, 12.0], TABV)) * sigma_coll(TAG, Mt)[0] * MSUNE / PC2
def gh(q_):
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = 10 ** (bg["a"] + bg["b"] * (q_["lMb"] - 10)); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); c = Srule(M); r0 = solve_r0(M * MSUNE, R200, c); return GE * math.pi * c * r0 ** 2 * B(q_["Rm"] / r0) / q_["Rm"] ** 2
ET = json.load(open(os.path.join(FRB, "ET1_core_strength_needed", "et1_results.json")))["ups"]["0.50"]["bins"]; RES["bins"] = {}
for lo, hi in ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)):
    qs = sel(lo, hi); U, D = [], []
    for q_ in qs:
        g = gh(q_); _, _, iu = fit_one(q_, np.log10(np.maximum(q_["GB"] + g[:, None], 1e-300))); U.append(UPS[iu]); d = dv(q_, g)
        if d is not None: D.append(d)
    k = f"{lo}-{hi}"; e = ET[k]; Sr = Srule(10 ** e["lgM"]) / (MSUNE / PC2); ins = e["ci"][0] <= Sr <= e["ci"][1]; RES["bins"][k] = dict(n=len(qs), U=float(np.median(U)), dV=float(np.median(D)), S_rule=Sr, ET1=e["med"], ET1_ci=e["ci"], inside=bool(ins))
    Pn(f"  {k}: n {len(qs)} U {np.median(U):.2f} dV {np.median(D):+.1f}; S_rule {Sr:.0f} vs ET1 {e['med']:.0f} [{e['ci'][0]:.0f},{e['ci'][1]:.0f}] {'inside' if ins else 'outside'}")
tg = "nf1_native_check" if CHECK else (f"nf1_native_hyp_{r10:g}_{r11:g}" if HYP else "nf1_native_read"); json.dump(RES, open(os.path.join(HERE, f"{tg}.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{tg}.out"), "w").write("\n".join(OUTL) + "\n")
