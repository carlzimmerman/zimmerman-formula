#!/usr/bin/env python3
"""WM1 (FROZEN_CRITERIA.md 6e40130dfa): local gates 1-5b, 10 and the Bullet through SS1's machinery, read-only (SS1's ss1v module is
monkeypatched inside this process only, as SS4 did). The component in each system = S(M200) x SS1's primary halo (KD1 P3, truncated
SIS, f_cap R M_b), S(M) = (1 + M_hm / M)^-1.16.
    python3 wm1_local.py local <V>    V in W (main, M_hm 4.97e12), W3 (x3), Wthird (x1/3), MW1 (x10), MW2 (/10), Racc (S = 1)
    python3 wm1_local.py bullet <V>   galaxy-traced (graded), gas-traced reported
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, math, json, io, subprocess, resource
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"); sys.path.insert(0, SS1)
W = sys.argv[1]; V = sys.argv[2] if len(sys.argv) > 2 else "W"
os.environ["SS1V"] = "H"; os.environ["SS1V_OPT"] = ""
sys.dont_write_bytecode = True
import numpy as np
CRIT = "6e40130dfa"; PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
_a = sys.argv; sys.argv = [_a[0]]
import ss1_core as C
import ss1v as SV
sys.argv = _a
SV.PARTS = PARTS; SV.VAR = V
MHM0 = (0.050 ** (-1 / 1.16) - 1) * 4.060e11                                   # frozen rule: S(4.060e11) = 0.050
MHM = {"W": MHM0, "W3": 3 * MHM0, "Wthird": MHM0 / 3, "MW1": 10 * MHM0, "MW2": MHM0 / 10, "Racc": 0.0}
def S_of(M, Vx=V): return (1 + MHM[Vx] / M) ** -1.16
def vparW(Vx, f):
    F = SV.footing(f)
    return dict(z_dec=0.55, alpha=F["alpha_G"], kick=0.0, base="H", v_stiff=F["v_stiff"], F=F, force_x0_zero=False, hfull=False, iform=False, W=True, Mhm=MHM[Vx])
def h_encW(p, H, r, tau=None): return S_of(H["M200"]) * H["Menc"](np.asarray(r, float))
SV.vpar = vparW; SV.h_enc = h_encW
def P(s): print(s, flush=True)

def bullet():
    def call(arg, on):
        cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.abspath(__file__), "bchild", V, arg, on], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
        line = [l for l in cp.stdout.splitlines() if l.startswith("WM1CHILD ")]
        if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
        return json.loads(line[0][9:])
    o0 = call("{}", "gal"); m = o0["masses"]; Mb = [m["M_gas_sub"][j] + m["M_star_sub"][j] for j in range(2)]; Mret = {}; info = {}
    for f in SV.FOOTS:
        p = vparW(V, f); F = p["F"]; r_ = []; inf = []
        for j in range(2):
            H = C.halo(Mb[j], F["R"], F["h"], F["Om"], z=p["z_dec"]); H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]; mk = float(h_encW(p, H, H["R200"]))
            r_.append(mk); inf.append(dict(M_b=Mb[j], M200=H["M200"], S=S_of(H["M200"]), inside_R200_over_Mb=mk / Mb[j], R200=H["R200"]))
        Mret[f] = r_; info[f] = inf
    oa = call(json.dumps(Mret), "gal"); og = call(json.dumps(Mret), "gas")
    out = dict(variant=V, criteria=CRIT, M_hm=MHM[V], KA_bullet=o0["KA"], subclusters=info, child_peak_rss_MB=max(o0["child_peak_rss_MB"], oa["child_peak_rss_MB"]))
    for f in SV.FOOTS:
        b = oa[f]["row"]; out[f] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", row=b, gas_traced_reported=og[f]["row"])
        P(f"[{f}] {V} Bullet galaxy-traced: {b['label']} cls {b['cls']}; M300 Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; gas-traced {og[f]['row']['label']} ({og[f]['row']['cls']}); S " + ", ".join(f"{x['S']:.3f}" for x in info[f]) + "; inside R200 / M_b " + ", ".join(f"{x['inside_R200_over_Mb']:.2f}" for x in info[f]))
    json.dump(out, open(os.path.join(PARTS, f"vbullet_{V}.json"), "w"), indent=1, default=float)

def bchild(arg, on):
    Rs_all = json.loads(arg); RB = os.path.join(REPO, "rebuild_2026_10_22"); DB1 = os.path.join(RB, "DB1_cluster_dark_baryons")
    src = open(os.path.join(DB1, "db1_fast.py")).read(); pre = src[:src.index("# ---------- X-COP, own replica")]
    a_ = 'OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")'; assert pre.count(a_) == 1; pre = pre.replace(a_, "OUT = io.StringIO()")
    sys.path.insert(0, DB1); os.chdir(DB1); sys.argv = [os.path.join(DB1, "db1_fast.py"), "wm1"]
    BNS = {"__file__": os.path.join(DB1, "db1_fast.py"), "__name__": "db1_fast_wm1"}; so = sys.stdout; sys.stdout = io.StringIO(); out = {}
    try:
        exec(compile(pre, "db1_fast_prefix", "exec"), BNS)
        MST, MGJ = BNS["MST"], BNS["MGJ"]; row = BNS["bullet_row"]
        out["KA"] = row("Z", "canonical", 0.0, Rs=[0.0, 0.0]); out["masses"] = dict(M_star_sub=[float(x) for x in MST], M_gas_sub=[float(x) for x in MGJ])
        for f, Mret in Rs_all.items(): out[f] = dict(row=row("Z", f, 0.0, Rs=[Mret[j] / MST[j] for j in range(len(MST))], on=on))
    finally: sys.stdout = so
    out["child_peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print("WM1CHILD " + json.dumps(out, default=float)); sys.exit(0)

if __name__ == "__main__":
    if W == "bchild": bchild(sys.argv[3], sys.argv[4])
    P(f"WM1 {W} {V}: M_hm {MHM[V]:.4g} Msun (S(4.06e11) {S_of(4.060e11):.4f}). Criteria {CRIT}. kappa = 1/2 FITTED; not theory closed; adopts nothing.")
    if W == "local":
        import ss1; ss1.PARTS = PARTS; ss1.MUT = "primary-only"; SV.run_local(V)
    elif W == "bullet": bullet()
