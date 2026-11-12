#!/usr/bin/env python3
"""SS4 (FROZEN_CRITERIA.md f3effad98c): option (c) table and variant K's local gates / Bullet through SS1's machinery, read-only
(SS1's ss1v module is monkeypatched inside this process only).
    python3 ss4.py ka            KA-K1 (closed form of the cored profile's enclosed mass)
    python3 ss4.py optc          option (c): max f_gal per R_c under the record's KiDS line and SPARC F2   -> parts/optc.json
    python3 ss4.py local <V>     V in K (primary), Kp2 (power 2), Kform (R_c1 from the source's formula), MK1 (pressure off), MK2 (v_stiff x 2)
    python3 ss4.py bullet <V>    gas-traced (both halves pressured; DB1 on = "gas"), galaxy-traced reported   -> parts/vbullet_<V>.json
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, math, json, io, contextlib, subprocess, resource
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"); sys.path.insert(0, SS1)
W = sys.argv[1]; V = sys.argv[2] if len(sys.argv) > 2 else "K"
os.environ["SS1V"] = V; os.environ["SS1V_OPT"] = ""
sys.dont_write_bytecode = True
import numpy as np
CRIT = "f3effad98c"; PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
_a = sys.argv; sys.argv = [_a[0]]
import ss1_core as C
import ss1v as SV
sys.argv = _a
SV.PARTS = PARTS; SV.VAR = V
RC1 = 2600.0                                                                   # kpc, physical, as given
def m_core(x): x = np.asarray(x, float); return (2 / math.pi) * (np.arctan(x) - x / (1 + x * x))
def rc1_formula(F): return F["v_stiff"] / (4 * math.pi * 100 * F["h"]) * 1000.0     # kpc: v_stiff / (4 pi H0)
def vparK(Vx, f):
    F = SV.footing(f); vst = F["v_stiff"] * (2.0 if Vx == "MK2" else 1.0)
    return dict(z_dec=F["z_q0"], alpha=F["alpha_G"], kick=0.0, base="H", v_stiff=vst, F=F, force_x0_zero=False, hfull=False, iform=False, K=True,
                power=(2 if Vx == "Kp2" else 3), rc1=(rc1_formula(F) if Vx == "Kform" else RC1), off=(Vx == "MK1"))
def h_encK(p, H, r, tau=None):
    r = np.asarray(r, float)
    if p.get("off"): return H["Menc"](r)                                       # MK1: no pressure, compact pre-conversion halo
    v = math.sqrt(SV.G_KPC * H["M500"] / H["R500"]); rc2 = H["R500"] * (p["v_stiff"] / v) ** p["power"]
    return 0.5 * H["Mchi0"] * (m_core(r / p["rc1"]) + m_core(r / rc2))
SV.vpar = vparK; SV.h_enc = h_encK
def P(s): print(s, flush=True)

def ka():
    from scipy.integrate import quad
    worst = 0.0
    for x in (0.1, 0.5, 1.0, 3.0, 20.0):
        num = quad(lambda s: s * s / (1 + s * s) ** 2, 0, x)[0] / (math.pi / 4); worst = max(worst, abs(num - float(m_core(x))))
    out = dict(KA_K1_max_dev=worst, pass_=bool(worst < 1e-8), rc1_formula_kpc={f: rc1_formula(SV.footing(f)) for f in SV.FOOTS}, rc1_frozen_kpc=RC1)
    json.dump(out, open(os.path.join(PARTS, "ka.json"), "w"), indent=1); P(json.dumps(out))

def optc():
    import ss1 as S
    GB = S.J.load_prefix(os.path.join(S.CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
    LE = GB["NS"]["lensing"](); G, MS, KPC = S.G_SI, S.MS, S.KPC
    out = dict(criteria=CRIT, source_claim=dict(zip(["0.12", "0.3", "0.6", "1.2", "2.4", "3"], [0.18, 0.23, 0.30, 0.44, 1.00, 1.00])), footings={})
    for f in S.FOOTS:
        a0 = S.A0H[f]; glaw = S.glaw; F2 = S.F2_ALLOW[f]; rows = {}
        sp = [(float(g["vb2"][-1] * g["R"][-1] / G / MS), float(g["R"][-1] / KPC)) for g in GB["SP"]]
        for Rc in (0.12, 0.3, 0.6, 1.2, 2.4, 3.0):
            Rk = Rc * 1000.0
            def worst(fg, sub=False):
                w = 0.0
                for p_ in LE:
                    Mb = p_["Mb"] / MS; r = math.sqrt(G * p_["Mb"] / p_["gbar"]); rk = r / KPC
                    if sub and not (300.0 <= rk <= 1500.0): continue
                    mk = fg * 5.41 * Mb * float(m_core(rk / Rk)); w = max(w, abs(math.log10(glaw(p_["gbar"] + G * mk * MS / r ** 2, a0) / glaw(p_["gbar"], a0))))
                return w
            def f_max(sub):
                if worst(1.0, sub) <= 0.05: return 1.0
                lo, hi = 0.0, 1.0
                for _ in range(40):
                    mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if worst(mid, sub) <= 0.05 else (lo, mid)
                return lo
            fa, fs = f_max(False), f_max(True)
            sparc_med = float(np.median([5.41 * float(m_core(rl / Rk)) for Mb, rl in sp]))           # F2 at f_gal = 1
            rows[f"{Rc:g}"] = dict(f_max_all_points=fa, f_max_0p3_1p5Mpc=fs, sparc_F2_at_f1=sparc_med, sparc_f_max=min(1.0, F2 / max(sparc_med, 1e-30)), f_gal_max=min(fa, min(1.0, F2 / max(sparc_med, 1e-30))))
            P(f"[{f}] R_c {Rc:>4} Mpc: f_max (KiDS, all 59 points) {fa:.3f}; 0.3-1.5 Mpc subset {fs:.3f}; SPARC F2 at f 1 {sparc_med:.2e} -> f_gal_max {rows[f'{Rc:g}']['f_gal_max']:.3f}  (source {out['source_claim'][f'{Rc:g}']:.2f})")
        out["footings"][f] = rows
    json.dump(out, open(os.path.join(PARTS, "optc.json"), "w"), indent=1)

def bullet():
    def call(arg, on):
        cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.abspath(__file__), "bchild", V, arg, on], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
        line = [l for l in cp.stdout.splitlines() if l.startswith("SS4CHILD ")]
        if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
        return json.loads(line[0][9:])
    o0 = call("{}", "gal"); m = o0["masses"]; Mb = [m["M_gas_sub"][j] + m["M_star_sub"][j] for j in range(2)]; Mret = {}; info = {}
    for f in SV.FOOTS:
        p = vparK(V, f); F = p["F"]; r_ = []; inf = []
        for j in range(2):
            H = C.halo(Mb[j], F["R"], F["h"], F["Om"], z=p["z_dec"]); H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]; mk = float(h_encK(p, H, H["R200"]))
            r_.append(mk); inf.append(dict(M_b=Mb[j], inside_R200_over_Mb=mk / Mb[j], R200=H["R200"]))
        Mret[f] = r_; info[f] = inf
    og = call(json.dumps(Mret), "gas"); oa = call(json.dumps(Mret), "gal")
    out = dict(variant=V, criteria=CRIT, KA_K4=o0["KA"], subclusters=info, child_peak_rss_MB=max(o0["child_peak_rss_MB"], og["child_peak_rss_MB"]))
    for f in SV.FOOTS:
        b = og[f]["row"]; out[f] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", row=b, galaxy_traced_reported=oa[f]["row"])
        P(f"[{f}] {V} Bullet gas-traced: {b['label']} cls {b['cls']}; M300 Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; galaxy-traced {oa[f]['row']['label']} ({oa[f]['row']['cls']}); inside R200 / M_b " + ", ".join(f"{x['inside_R200_over_Mb']:.2f}" for x in info[f]))
    json.dump(out, open(os.path.join(PARTS, f"vbullet_{V}.json"), "w"), indent=1, default=float)

def bchild(arg, on):
    Rs_all = json.loads(arg); RB = os.path.join(REPO, "rebuild_2026_10_22"); DB1 = os.path.join(RB, "DB1_cluster_dark_baryons")
    src = open(os.path.join(DB1, "db1_fast.py")).read(); pre = src[:src.index("# ---------- X-COP, own replica")]
    a_ = 'OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")'; assert pre.count(a_) == 1; pre = pre.replace(a_, "OUT = io.StringIO()")
    sys.path.insert(0, DB1); os.chdir(DB1); sys.argv = [os.path.join(DB1, "db1_fast.py"), "ss4"]
    BNS = {"__file__": os.path.join(DB1, "db1_fast.py"), "__name__": "db1_fast_ss4"}; so = sys.stdout; sys.stdout = io.StringIO(); out = {}
    try:
        exec(compile(pre, "db1_fast_prefix", "exec"), BNS)
        MST, MGJ = BNS["MST"], BNS["MGJ"]; row = BNS["bullet_row"]
        out["KA"] = row("Z", "canonical", 0.0, Rs=[0.0, 0.0]); out["masses"] = dict(M_star_sub=[float(x) for x in MST], M_gas_sub=[float(x) for x in MGJ])
        for f, Mret in Rs_all.items(): out[f] = dict(row=row("Z", f, 0.0, Rs=[Mret[j] / MST[j] for j in range(len(MST))], on=on))
    finally: sys.stdout = so
    out["child_peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print("SS4CHILD " + json.dumps(out, default=float)); sys.exit(0)

if __name__ == "__main__":
    if W == "bchild": bchild(sys.argv[3], sys.argv[4])
    P(f"SS4 {W} {V}. Criteria {CRIT}. kappa = 1/2 FITTED; not theory closed; adopts nothing.")
    if W == "ka": ka()
    elif W == "optc": optc()
    elif W == "local":
        import ss1; ss1.PARTS = PARTS; ss1.MUT = "primary-only"; SV.run_local(V)
    elif W == "bullet": bullet()
