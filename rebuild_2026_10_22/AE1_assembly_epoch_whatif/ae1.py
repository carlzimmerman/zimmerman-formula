#!/usr/bin/env python3
"""AE1_assembly_epoch_whatif (FROZEN_CRITERIA.md): Sigma_coll at the core-assembly epoch z(f_s) against the half-mass z_f,
as ratios to 1e12, through NF1's what-if. X43's machinery (EM1 backgrounds, sigma(M), D(z)) is executed read-only with
its outputs redirected here; X43's own files are not touched. A convention check, not a measurement.
    python3 -I ae1.py [--mutate]
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, io, json, math, contextlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUTATE = "--mutate" in sys.argv; TAG = "_MUTATE" if MUTATE else ""
X43 = os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py")
src = open(X43).read(); cut = src.index("k2 = all(abs(EPS[t]"); assert src.count("k2 = all(abs(EPS[t]") == 1
# run X43 up to (not including) its K2 line, with HERE pointing at this folder so every file it opens lands here
ns = {"__file__": os.path.join(HERE, "x43_collapse_core.py"), "__name__": "x43_ro"}; argv0 = sys.argv; sys.argv = [X43]
buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(compile(src[:cut], X43, "exec"), ns)
sys.argv = argv0
open(os.path.join(HERE, f"ae1_x43_machinery{TAG}.log"), "w").write(buf.getvalue())
EPS, DC = ns["EPS"], ns["DC"]; OMEGA = ns["OMEGA"] * (2.0 if MUTATE else 1.0)
import numpy as np
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def B(x): return math.asinh(x) - x / math.sqrt(1 + x * x)
def zf(tag, M, f):
    e = EPS[tag]; s2 = lambda l: float(np.interp(l, e["lMg"], e["s2"]))
    S = math.sqrt(max(s2(math.log10(f * M)) - s2(math.log10(M)), 0.0)); Df = DC / (DC + OMEGA * S)
    if Df >= 1.0: return 0.0
    return float(np.interp(-Df, -e["Dg"], e["zg"]))
A_ = 13.34; FS = B(math.sqrt(2)) / B(A_)
P(f"AE1{TAG}: Sigma_coll at the core-assembly epoch, as a ratio to 1e12; kappa = 1/2 FITTED; not theory closed")
P(f"  f_s = B(sqrt2)/B({A_}) = {FS:.4f}; omega {OMEGA}")
k2 = abs(FS - 0.144) <= 0.002
X43Z = {1e11: 1.14, 1e12: 0.94, 1e13: 0.75, 1e14: 0.56, 1e15: 0.39}
zA = {M: zf("A_c2b_refit", M, 0.5) for M in X43Z}
k1 = all(abs(zA[M] - z) <= 0.011 for M, z in X43Z.items())
P(f"  K1 z_f(f 0.5) on A vs X43: " + ", ".join(f"{M:g} {zA[M]:.3f}/{z}" for M, z in X43Z.items()) + f": {'PASS' if k1 else 'FAIL'}")
P(f"  K2 f_s {FS:.4f} vs 0.144: {'PASS' if k2 else 'FAIL'}")
res = dict(f_s=FS, omega=OMEGA, checks=dict(K1=k1, K2=k2), footings={})
for tag in EPS:
    rows = {}
    for M in (1e10, 1e11, 1e12, 1e14):
        z5, z25, zs = zf(tag, M, 0.5), zf(tag, M, 0.25), zf(tag, M, FS)
        rows[M] = dict(z_half=z5, z_quarter=z25, z_fs=zs, R_quarter=((1 + z25) / (1 + z5)) ** 2, R_fs=((1 + zs) / (1 + z5)) ** 2)
    rel = {k: dict(r10=rows[1e10][k] / rows[1e12][k], r11=rows[1e11][k] / rows[1e12][k]) for k in ("R_quarter", "R_fs")}
    res["footings"][tag] = dict(rows={f"{M:g}": v for M, v in rows.items()}, rel=rel)
    P(f"  [{tag}] " + "; ".join(f"M {M:g}: z 0.5 {v['z_half']:.3f}, 0.25 {v['z_quarter']:.3f}, f_s {v['z_fs']:.3f}; R_0.25 {v['R_quarter']:.3f}, R_fs {v['R_fs']:.3f}" for M, v in rows.items()))
    P(f"  [{tag}] relative to 1e12: f_s rho10 {rel['R_fs']['r10']:.3f}, rho11 {rel['R_fs']['r11']:.3f}; f 0.25 rho10 {rel['R_quarter']['r10']:.3f}, rho11 {rel['R_quarter']['r11']:.3f}")
# MUTATE gate: omega doubled must move z(f_s, 1e10) by > 0.1 against the unmutated value stored on the first run
ref = os.path.join(HERE, "ae1_results.json")
if MUTATE:
    r0 = json.load(open(ref)); dz = res["footings"]["A_c2b_refit"]["rows"]["1e+10"]["z_fs"] - r0["footings"]["A_c2b_refit"]["rows"]["1e+10"]["z_fs"]
    P(f"  MUTATE omega x2: z(f_s, 1e10) moves by {dz:+.3f}: {'BITES' if abs(dz) > 0.1 else 'DOES NOT BITE, STOP'}")
    res["mutate_dz"] = dz
# NF1 what-if on background A's ratios (the graded run uses f_s; f 0.25 reported)
NF1 = os.path.join(REB, "NF1_no_floor_rule", "nf1_native_read.py"); env = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1")
if not MUTATE:
    chk = subprocess.run([sys.executable, NF1, "--check"], cwd=os.path.dirname(NF1), env=env, capture_output=True, text=True)
    P("  K3 NF1 --check: " + (chk.stdout.strip().splitlines()[-1] if chk.stdout.strip() else chk.stderr[-300:]))
    res["nf1"] = {}
    for key in ("R_fs", "R_quarter"):
        r = res["footings"]["A_c2b_refit"]["rel"][key]
        p = subprocess.run([sys.executable, NF1, "--rho", f"{r['r10']:.4f}", f"{r['r11']:.4f}"], cwd=os.path.dirname(NF1), env=env, capture_output=True, text=True)
        txt = p.stdout + p.stderr; open(os.path.join(HERE, f"ae1_nf1_{key}.log"), "w").write(txt)
        P(f"  NF1 what-if at {key} (rho10 {r['r10']:.4f}, rho11 {r['r11']:.4f}):"); [P("    " + l) for l in p.stdout.strip().splitlines()]
        res["nf1"][key] = txt
json.dump(res, open(os.path.join(HERE, f"ae1_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"ae1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
