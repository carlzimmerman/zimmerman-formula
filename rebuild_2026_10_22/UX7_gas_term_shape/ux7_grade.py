#!/usr/bin/env python3
"""UX7 keys: UX3's path (LW1 tail, SL1 driver, NF1 grader), with the form in the source mass. Row mut 'FORM:k' or 'P:p:q:t:k'. Own cache; resumes. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "LW1_law_scorecard")); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import lw1_keys as L
from ux7_common import FORMS, RIV, controls
FI = json.load(open(os.path.join(HERE, "ux7_fit.json"))); FEET = ("canonical", "alt"); FS = 1.034
T = L.T; a = 'return RM ** 2 * _comb(gb, gb * (1 + _LAW["c"] * S / 3), _A0L[foot], _LAW["rd"]) / GE, S'; assert T.count(a) == 1
T = T.replace(a, 'return RM ** 2 * _ux7(gb, S, foot, Mb) / GE, S')
b = "def _msrc(Mb, foot):"; assert T.count(b) == 1
T = T.replace(b, r'''_UM = json.load(open(os.environ["UX7_MASS"])); _UFS = 1 + float(os.environ["X73_FSTAR"])
def _ux7(gb, S, foot, Mb):
    a0 = _A0L[foot]; Lw = _comb(gb, gb, a0, "R1"); m_ = _LAW["mut"]
    if not m_: return Lw
    p_ = m_.split(":"); F = p_[0]; k = float(p_[-1]); gg = gb / _UFS; x = gg / a0; i_, pp_ = _ST["cur"]; r5 = float(pp_["R500"]) * float(NX["MPC"]); u = np.maximum(RM / r5, .01)
    if F == "F0": return Lw * (1 + k * x)
    if F == "F1": return Lw * (1 + k * x * S)
    if F == "F2": return Lw * (1 + k * x / (1 + x))
    if F == "F3": return Lw * (1 + k * gb / a0)
    if F == "F4": return _comb(gb, gb, a0 * (1 + k * x), "R1")
    if F == "F5": return Lw + k * gg
    if F == "F6": return Lw * (1 + k * x * x)
    if F == "F7": return Lw + k * S * gg
    if F == "F8": return Lw * (1 + k * x * np.exp(-RM / r5))
    if F == "P": return Lw * (1 + k * x ** float(p_[1]) * u ** float(p_[2]) * S ** float(p_[3]))
    src = {"L": "L", "c": "cat", "S": "shuf", "G": "gas10"}[F[2]]; cl_ = NX["CL"][i_]; qd = float(pp_["R500"]) / float(cl_["R500"]); M5 = _UM[src][str(cl_["name"]).strip()] * qd ** float(os.environ.get("UX7_QDEXP", "1")) * MSUNE; s_ = Mb / float(np.interp(r5, RM, Mb)); gM = GE * M5 * s_ / RM ** 2
    if F[:2] == "R1": return Lw * (1 + k * gM / a0)
    if F[:2] == "R2": return Lw + k * gM
    raise KeyError(F)
''' + b)
c = 'pp = prep(i, foot, hk); m, S = _msrc(pp["Mb"], foot);'; assert T.count(c) == 1; T = T.replace(c, 'pp = prep(i, foot, hk); _ST["cur"] = (i, pp); m, S = _msrc(pp["Mb"], foot);')
def kf(f, form): return FI[f]["forms"][form]["k"]
def row(f, form, k, src=""): return ["R1", 0, f, f"{form}{src}:{k:.8g}"]
def fitrows(): return [row(f, x, kf(f, x)) for f in FEET for x in FORMS] + [row(f, x, kf(f, x), s) for f in FEET for x in RIV for s in ("L", "c")]
def scan(): return [row(f, x, kf(f, x) * m, "L" if x in RIV else "") for f in FEET for x in FORMS + RIV for m in (.7, .85, 1.15, 1.3)]
def checks(): return [row(f, "F0", {"canonical": 13.286788, "alt": 14.250573}[f]) for f in FEET] + [row("canonical", x, 0) for x in FORMS] + [row("canonical", "R1", 0, "L"), row("canonical", "R2", 0, "L"), row("canonical", "F3", 10.0), row("canonical", "F0", 10.34), row("canonical", "R1", 10.0, "G"), row("canonical", "F0", 10.0)]
def ctrl(): return [["R1", 0, f, f"P:{p:.5f}:{q:.5f}:{t:.5f}:{FI[f]['ctrl'][i]['k']:.8g}"] for f in FEET for i, (p, q, t) in enumerate(controls())]
def mut(): return [row(f, x, 3 * kf(f, x), "L" if x in RIV else "") for f in FEET for x in FORMS + RIV] + [row(f, x, kf(f, x), "S") for f in FEET for x in RIV]
RUNS = {"g005_f034": (.005, "0.034", lambda: fitrows() + checks() + scan() + ctrl()), "g005_f0615": (.005, "0.0615", fitrows), "g0_f034": (0.0, "0.034", fitrows), "MUTATE_g005_f034": (.005, "0.034", mut), "POST_k5": (.005, "0.034", lambda: [row("canonical", "R1", 10.0, "G"), row("canonical", "F0", 10.0)])}
if __name__ == "__main__":
    for tag in (sys.argv[1:] or RUNS):
        dex, fs, rf = RUNS[tag]; W = os.path.join(HERE, f"cache_{tag}"); os.makedirs(W, exist_ok=True); O = os.path.join(HERE, f"ux7_keys_{tag}.json")
        if os.path.exists(O) and json.load(open(O)).get("done"): print(tag, "done", flush=True); continue
        TL = os.path.join(W, "ux7_tail.py"); open(TL, "w").write(T); d = open(os.path.join(L.SL1, "sl1_harvest.py")).read()
        for a_, b_ in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(L.GAS % dex if dex else "") + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('X73_FSTAR="0.034"', f'X73_FSTAR="{fs}"')):
            assert d.count(a_) == 1, a_; d = d.replace(a_, b_)
        df = os.path.join(W, "ux7_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=L.SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", LW1_A0X="1.0", UX7_MASS=os.path.join(HERE, "ux7_mass.json"), DR1_RUN=json.dumps(dict(rows=rf(), k2=False)), **({"UX7_QDEXP": "2.5"} if tag == "POST_k5" else {}))
        p = subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(W, "run.log"), "w"), stderr=subprocess.STDOUT); print(tag, p.returncode, flush=True)
