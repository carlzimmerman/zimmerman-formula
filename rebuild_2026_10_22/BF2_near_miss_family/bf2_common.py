#!/usr/bin/env python3
"""BF2 shared: snapshot, form evaluation, family signature, candidate generator, RQ3 loader. Criteria FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import ast, hashlib, json, math, os, sys, types
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
try: os.nice(19)
except OSError: pass
import numpy as np
np.seterr(all="ignore")
LANE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(LANE); REPO = os.path.dirname(RB); BF1 = os.path.join(RB, "BF1_exhaustive_law_search"); RQ3 = os.path.join(RB, "RQ3_acceptance_v2"); WL4 = os.path.join(BF1, "chunks", "real_L4")
MUT = os.environ.get("BF2_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""; HMUT = 1.5 if MUT else 1.0
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt"); C = 299792458.0
FN = dict(sqrt=np.sqrt, log1p=np.log1p, inv1p=lambda x: 1 / (1 + x), sq=lambda x: x * x, pi=math.pi)
def H_of(s, y, ell, f):
    e = dict(FN, y=y, ell=ell, f=f)
    return HMUT * (eval(s, {"__builtins__": {}}, e) * np.ones_like(y + f))
def law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def wrap(w, g, a, H): return law(g, a * H) if w == 1 else law(g * H, a) if w == 2 else law(g, a) * H
def snapshot():
    """done first, then hits, so every done job's hits are in. Complete lines only. Frozen once written."""
    P = os.path.join(LANE, f"snapshot{TAG}.json"); P0 = os.path.join(LANE, "snapshot.json")
    if os.path.exists(P0): return json.load(open(P0))
    done = open(os.path.join(WL4, "done.txt")).read(); done = done[:done.rfind("\n") + 1].split(); raw = open(os.path.join(WL4, "hits.jsonl"), "rb").read(); raw = raw[:raw.rfind(b"\n") + 1]; hits = [json.loads(l) for l in raw.splitlines()]
    o = dict(n_lines=len(hits), sha256=hashlib.sha256(raw).hexdigest(), n_done=len(done), done_sha256=hashlib.sha256("\n".join(done).encode()).hexdigest(), hits=hits, done=done); json.dump(o, open(P0, "w")); return o
_names = {}
def names():
    if not _names: _names["n"] = json.load(open(os.path.join(WL4, "names.json")))
    return _names["n"]
# ---------- family signature
COMM = {ast.Add, ast.Mult}
def _sig(n):
    if isinstance(n, ast.Expression): return _sig(n.body)
    if isinstance(n, ast.Constant): return "C", 1
    if isinstance(n, ast.Name):
        if n.id == "pi": return "C", 1
        if n.id == "f": return "F", 1
        return n.id, 1
    if isinstance(n, ast.Call):
        a, k = _sig(n.args[0])
        return (a if a in ("C", "F") else f"{n.func.id}({a})"), k + 1
    if isinstance(n, ast.BinOp):
        a, ka = _sig(n.left); b, kb = _sig(n.right); o = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}[type(n.op)]
        if a in ("C", "F") and b in ("C", "F"): return ("C" if a == b == "C" else "F"), ka + kb + 1
        if type(n.op) in COMM and b < a: a, b = b, a
        return f"({a}{o}{b})", ka + kb + 1
    raise ValueError(type(n))
def signature(s): return _sig(ast.parse(s, mode="eval"))
def uses(s): return {x.id for x in ast.walk(ast.parse(s, mode="eval")) if isinstance(x, ast.Name)}
def H_at_f0(s):
    """True if H = 1 at f = 0 for all probed y, ell"""
    y = np.geomspace(1e-5, 1e7, 49); o = []
    for el in (1e-12, 1e-6, 1e-2):
        o.append(H_of(s, y, y * 0 + el, y * 0))
    o = np.array(o); return o
TEMPLATE = '''"""BF2 candidate, generated. {why} Description, no action, no fitted float; chosen from about 1.7e11 tries. kappa = 1/2 FITTED."""
import math, numpy as np
NAME = {name!r}; EXPR = {expr!r}; WRAP = {wrap}; VERTICAL = ("R",); HMUT = {hmut}
_F = dict(sqrt=np.sqrt, log1p=np.log1p, inv1p=lambda x: 1 / (1 + x), sq=lambda x: x * x, pi=math.pi)
_USES_ELL = {uses_ell}
def _law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]; gg = np.asarray(Q["gg"], float); pos = gb > 0; gq = np.where(pos, gb, 1.0)
    y = gq / a; f = np.clip(np.broadcast_to(gg, gq.shape) / gq, 0.0, 1.0)
    ell = np.broadcast_to(np.asarray(Q["r"], float), gq.shape) * a / 299792458.0 ** 2 if _USES_ELL else y * 0
    with np.errstate(all="ignore"):
        H = HMUT * (eval(EXPR, {{"__builtins__": {{}}}}, dict(_F, y=y, ell=ell, f=f)) * np.ones_like(y))
        v = _law(gq, a * H) if WRAP == 1 else _law(gq * H, a) if WRAP == 2 else _law(gq, a) * H
    return np.where(pos, v, gb)
'''
def write_cand(tag, s, w, why=""):
    d = os.path.join(LANE, "candidates"); os.makedirs(d, exist_ok=True); p = os.path.join(d, f"{tag}{TAG}.py")
    open(p, "w").write(TEMPLATE.format(name=f"BF2 {tag}{TAG}", expr=s, wrap=w, hmut=HMUT, uses_ell="ell" in uses(s), why=why)); return p
# ---------- RQ3, read-only, outputs in this lane
def rq3():
    p = os.path.join(RQ3, "acceptance.py"); s = open(p).read(); W = LANE; os.makedirs(os.path.join(W, "cache_crg", "p"), exist_ok=True); os.makedirs(os.path.join(W, "cache_crg", "c"), exist_ok=True)
    SUBS = [('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {W!r}; RB = {RB!r}'), ('TOL = json.load(open(os.path.join(HERE, "tolerances.json")))', f'TOL = json.load(open(os.path.join({RQ3!r}, "tolerances.json")))'), ('MARKS = J(HERE, "row_marks.json")', f'MARKS = J({RQ3!r}, "row_marks.json")')]
    for a, b in SUBS:
        assert s.count(a) >= 1, a; s = s.replace(a, b, 1)  # first occurrence: the module's own; run_keys holds a second copy as a target string for sl1_harvest
    s = s.split('if __name__ == "__main__":')[0]; m = types.ModuleType("rq3acc"); m.__file__ = p; sys.modules["rq3acc"] = m; exec(compile(s, p, "exec"), m.__dict__); return m
