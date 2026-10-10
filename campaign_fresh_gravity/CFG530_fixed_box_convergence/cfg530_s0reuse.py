#!/usr/bin/env python3
"""CFG530 S0 512^3 reuse check (FROZEN_CRITERIA.md): may CFG411's S0 N512 (L200, seed 359, NSEED 512) stand in for S0_L200_N512?
(a) S0 code path identical: AST source of initial_conditions, step_grid, Mesh, P_lin0, Dgrow, fgrow, T_eh, dta_table, delta_ta compared
    exactly; measure_pk / run / forces differ only in bookkeeping (diff printed; the S0 force branch is compared line by line).
(b) cfg527_pm.py ICs at N = 512, NSEED = 512 reproduce CFG411's zi snapshot: |d sigma8|/sigma8 <= 1e-12, max|dP/P| <= 1e-10.
(c) P(k) re-measured from CFG411's saved z = 0 positions with cfg527_pm.py reproduces CFG411's z0 P: max|dP/P| <= 1e-6.
Writes cfg530_s0reuse.json / .out."""
import os, sys, ast, json, difflib, hashlib, importlib.util
os.environ.update(CFG527_THREADS="4", CFG527_NSEED="512", CFG527_L="200", CFG527_RMIN="1.56")
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
E527 = os.path.join(CFG, "CFG527_law_respecting_engine", "cfg527_pm.py"); E411 = os.path.join(CFG, "CFG411_overnight_convergence", "cfg411_pm.py")
J411 = os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"); Z411 = J411.replace(".json", "_z0.npz")
OUT, L_ = {}, []
def P(s): print(s, flush=True); L_.append(s)
def funcs(p):
    src = open(p).read(); t = ast.parse(src)
    return {n.name: ast.get_source_segment(src, n) for n in t.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
a, b = funcs(E411), funcs(E527)
same = {k: a[k] == b[k] for k in ("initial_conditions", "step_grid", "Mesh", "P_lin0", "Dgrow", "fgrow", "T_eh", "dta_table", "delta_ta")}
P(f"(a) identical functions: {same}")
def s0_branch(src):
    """forces() lines executed for switch S0 with diag = False: from the top to the end of the need_t block's header, plus the final acc line."""
    ls = src.splitlines(); keep = [l for l in ls[:6]] + [l for l in ls if l.strip().startswith("acc = [-a * mesh.inv(1j * kv * phik)")]
    return keep
s0a, s0b = s0_branch(a["forces"]), s0_branch(b["forces"])
P(f"(a) forces() S0 path (header lines + acc line) identical: {s0a == s0b}")
for k in ("measure_pk", "run"):
    d = list(difflib.unified_diff(a[k].splitlines(), b[k].splitlines(), lineterm="", n=0))
    P(f"(a) {k} diff ({len(d)} lines):"); [P("    " + x) for x in d]
OUT["a"] = dict(identical=same, s0_force_path_identical=s0a == s0b)
a_ok = all(same.values()) and s0a == s0b

spec = importlib.util.spec_from_file_location("e527", E527); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
import numpy as np
j = json.load(open(J411))
pos, mom = m.initial_conditions(512); del mom
mesh = m.Mesh(512)
kb, pb, s8 = m.measure_pk(mesh, mesh.deposit(pos), 512 ** 3); del pos
ds = abs(s8 / j["snap"]["zi"]["sigma8"] - 1); dp = float(np.max(np.abs(np.array(pb) / np.array(j["snap"]["zi"]["P"]) - 1)))
P(f"(b) zi: |d sigma8|/sigma8 = {ds:.3e}, max|dP/P| = {dp:.3e}")
OUT["b"] = dict(d_sigma8_rel=ds, max_dP_rel=dp); b_ok = ds <= 1e-12 and dp <= 1e-10
pz = np.load(Z411)["pos"].astype(np.float64)
kb, pb, s8 = m.measure_pk(mesh, mesh.deposit(pz), 512 ** 3); del pz
ds0 = abs(s8 / j["snap"]["z0"]["sigma8"] - 1); dp0 = float(np.max(np.abs(np.array(pb) / np.array(j["snap"]["z0"]["P"]) - 1)))
P(f"(c) z0 from saved float32 positions: |d sigma8|/sigma8 = {ds0:.3e}, max|dP/P| = {dp0:.3e}")
OUT["c"] = dict(d_sigma8_rel=ds0, max_dP_rel=dp0); c_ok = dp0 <= 1e-6
OUT["sha256"] = {os.path.basename(p): hashlib.sha256(open(p, "rb").read()).hexdigest() for p in (J411, Z411)}
OUT["reuse"] = bool(a_ok and b_ok and c_ok)
P(f"REUSE CFG411 S0 N512 as S0_L200_N512: {'YES' if OUT['reuse'] else 'NO -> run S0_L200_N512'} (a {a_ok}, b {b_ok}, c {c_ok})")
json.dump(OUT, open(os.path.join(HERE, "cfg530_s0reuse.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg530_s0reuse.out"), "w").write("\n".join(L_) + "\n")
