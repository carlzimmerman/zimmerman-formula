#!/usr/bin/env python3
"""UX3 keys and Part C dump: LW1's exact path (imports its tail) with H = 1 + k g_gas/a0 on the law's mass. Own cache; resumes. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "LW1_law_scorecard")); sys.dont_write_bytecode = True
import lw1_keys as L
PI2 = math.pi ** 2; KF = json.load(open(os.path.join(HERE, "ux3_kfit.json")))
T = L.T; a = 'return RM ** 2 * _comb(gb, gb * (1 + _LAW["c"] * S / 3), _A0L[foot], _LAW["rd"]) / GE, S'; assert T.count(a) == 1
T = T.replace(a, 'return RM ** 2 * _comb(gb, gb * (1 + _LAW["c"] * S / 3), _A0L[foot], _LAW["rd"]) / GE * (1 + _UK() * gb / (1 + float(os.environ["X73_FSTAR"])) / _A0L[foot]) * _UA(), S')
b = "def _msrc(Mb, foot):"; assert T.count(b) == 1; T = T.replace(b, 'def _UK(): m_ = _LAW["mut"]; return float(m_[1:]) if m_ and m_.startswith("k") else 0.0\ndef _UA(): m_ = _LAW["mut"]; return float(m_[1:]) if m_ and m_.startswith("a") else 1.0\n' + b)
DUMP = r'''
CL = NX["CL"]; _LAW.update(rd="R1", c=0, mut=None, on=True); _OK = json.load(open(os.environ["UX3_OK"])); _nm = [str(CL[i]["name"]).strip() for i in range(N)]; _D = {}; _K4 = []
for f_ in ("canonical", "alt"):
    for hk in HK:
        for tag in ("raw", "eq17", "trunc", "cat"):
            V_ = np.zeros((N, 8)) * np.nan
            for nm_, o_ in _OK.items():
                i = _nm.index(nm_); pp = prep(i, f_, hk); qd = float(pp["R500"]) / float(CL[i]["R500"]); cf = o_["cf"] if tag == "eq17" else (o_["Mcat"] / o_["M500"] if tag == "cat" else 1.0); M5 = o_["M500"] * cf * qd * MSUNE; M2 = o_["M200"] * cf * qd * MSUNE; R5 = o_["R500_m"] * cf ** (1 / 3) * qd; R2 = o_["R200_m"] * cf ** (1 / 3) * qd
                f_n = lambda c_: np.log(1 + c_) - c_ / (1 + c_); from scipy.optimize import brentq as _bq; rs = _bq(lambda rr: f_n(R2 / rr) / f_n(R5 / rr) - M2 / M5, 1e-3 * R5, 1e3 * R5); m_ = M5 * f_n(RM / rs) / f_n(R5 / rs)
                if tag == "trunc": m_ = np.minimum(m_, M5 * f_n(2 * R2 / rs) / f_n(R5 / rs))
                m_ = np.maximum(m_, 1e-12 * float(m_[-1])); V_[i] = _dv0(i, f_, hk, m_)
                if tag == "raw" and hk == "h0672" and f_ == "canonical": _K4.append(float(np.interp(float(pp["R500"]) * float(NX["MPC"]), RM, pp["Mb"])) / (1 + float(os.environ["X73_FSTAR"])) / (float(CL[i]["Mgas500"]) * qd ** 2.5 * 10 ** float(os.environ["UX3_GAS"]) * (MSUNE if float(CL[i]["Mgas500"]) < 1e30 else 1.0)))
            _D[f"VOK_{tag}_{f_}_{hk}"] = V_
        V5 = np.zeros((N, 8)) * np.nan
        for nm_ in _OK:
            i = _nm.index(nm_); pp = prep(i, f_, hk); V5[i] = _dv0(i, f_, hk, _msrc(pp["Mb"], f_)[0])
        _D[f"VLAW_{f_}_{hk}"] = V5; PREP.clear()
_D["K4"] = np.array(_K4); _D["names"] = np.array(_nm); np.savez_compressed(os.environ["UX3_DUMP"], **_D)
'''
c = '_RES["done"] = True;'; assert T.count(c) == 1; T = T.replace(c, 'if os.environ.get("UX3_DUMP"): ' + 'exec(' + repr(DUMP) + ')\n' + c)
CA = json.load(open(os.path.join(HERE, "ux3_constA.json"))) if os.path.exists(os.path.join(HERE, "ux3_constA.json")) else {}
def rows(ks): return [["R1", 0, f, f"k{ (KF[f] if k == 'kfit' else k):.6f}"] for f in ("canonical", "alt") for k in ks]
M0 = 1.0
RUNS = {"g005_f034": (.005, "0.034", [0.0, PI2, "kfit", .7 * PI2, 1.3 * PI2, PI2 / 1.7, PI2 * 1.7]), "g005_f0615": (.005, "0.0615", [0.0, PI2, "kfit"]), "g0_f034": (0.0, "0.034", [PI2, "kfit"]), "MUTATE_g005_f034": (.005, "0.034", [3 * PI2, 3 * KF["canonical"]])}
if CA: RUNS["POST_const_f034"] = (.005, "0.034", [])
if __name__ == "__main__":
    for tag in (sys.argv[1:] or RUNS):
        dex, fs, ks = RUNS[tag]; W = os.path.join(HERE, f"cache_{tag}"); os.makedirs(W, exist_ok=True); O = os.path.join(HERE, f"ux3_keys_{tag}.json")
        if os.path.exists(O) and json.load(open(O)).get("done"): print(tag, "done", flush=True); continue
        TL = os.path.join(W, "ux3_tail.py"); open(TL, "w").write(T); d = open(os.path.join(L.SL1, "sl1_harvest.py")).read()
        for a_, b_ in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(L.GAS % dex if dex else "") + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('X73_FSTAR="0.034"', f'X73_FSTAR="{fs}"')):
            assert d.count(a_) == 1, a_; d = d.replace(a_, b_)
        df = os.path.join(W, "ux3_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=L.SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", LW1_A0X="1.0", UX3_OK=os.path.join(HERE, "ux3_okabe.json"), UX3_GAS=str(dex), DR1_RUN=json.dumps(dict(rows=rows(ks) if tag != "POST_const_f034" else [["R1", 0, f, f"a{CA[f]:.6f}"] for f in ("canonical", "alt")], k2=False)))
        env.pop("UX3_DUMP", None)
        if tag == "g005_f034": env["UX3_DUMP"] = os.path.join(W, "dump.npz")
        p = subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(W, "run.log"), "w"), stderr=subprocess.STDOUT); print(tag, p.returncode, flush=True)
