#!/usr/bin/env python3
"""RG1 P3-P5: patched read-only copies of HO2 and HO1, run in this lane's directory with their Step 0 intact; native-N rows added after the source grade."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
ho2 = open(os.path.join(REB, "HO2_sluggs_milkyway_heldout", "ho2_heldout.py")).read()
a = 'NS["halo_M"] = halo_M_cl2; rE = route_e'; assert ho2.count(a) == 1; ho2 = ho2.replace(a, 'NS["halo_M"] = CUR.get("halo", halo_M_cl2); rE = route_e')
a = "    def own_lgM200(M):"; assert ho2.count(a) == 1
ho2 = ho2.replace(a, '''    from scipy.optimize import brentq as _bq, minimize_scalar as _ms
    def _solve(Mtot, Rout, Sig):
        lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(RG1.B_smooth(Rout / math.exp(lr))))
        pk = _ms(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
        if lm(pk.x) < math.log(Mtot): CUR["sat"] = True; return math.exp(pk.x)
        CUR["sat"] = False; return math.exp(_bq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), pk.x, xtol=1e-14))
    def halo_M_nat(n, foot, q, Mstar, sig, gas=None):
        Mb = Mstar + (0.0 if gas is None else float(gas[-1]))
        M200 = 10 ** (bgA["a"] + bgA["b"] * (math.log10(Mb) - 10)) * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rcA)) ** (1 / 3)
        sc = RG1.S_nat(M200 / MSUNE) * MSUNE / PC2; r0 = _solve(M200, R200, sc)
        CUR["lgM200"] = math.log10(M200 / MSUNE); CUR["Sig_ratio"] = sc / SIGkg[foot]
        return math.pi * sc * r0 ** 2 * RG1.B_smooth(np.minimum(RG * KPC, R200) / r0) / MSUNE, sc
''' + a)
a = '        NS["halo_M"] = HALO_GR1\n        def pk(s):'; assert ho2.count(a) == 1
ho2 = ho2.replace(a, '''        CUR["halo"] = halo_M_nat; stn = sluggs_cl2(f); cln = cls(stn, s0); CUR.pop("halo")
        _r = lambda s: dict(per=s["per"], Z=s["Z"], mean=s["mean"], Z_class=s["Z_class"], n_cleared=s["n_cleared"], n_reversed=s["n_reversed"], closes=s["closes"], info=s.get("info"))
        RG1O[f] = dict(cls=cln, native=_r(stn), x38=_r(s0), cl2=_r(st), cl2_cls=c); json.dump(RG1O, open(os.path.join(HERE, "rg1_p3_sluggs" + ("_MUTATE" if RG1.MUT != 1 else "") + ".json"), "w"), indent=1, default=float)
''' + a)
ho2 = ho2.replace("import numpy as np\n", "import numpy as np\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport rg1_lib as RG1\nRG1O = {}\n", 1)
ho1 = open(os.path.join(REB, "HO1_xcop_hotgas_heldout", "ho1_heldout.py")).read()
a = 'open(os.path.join(HERE, f"ho1_heldout{TAG}.out"), "w")'; _i = ho1.index(a); assert ho1[_i - 1] == "\n"
ho1 = ho1[:_i] + ('''import sys as _s; _s.path.insert(0, HERE); import rg1_lib as RG1
_CL2 = {f: dict(mean=RES["footings"][f]["xcop"]["mean"], rms=RES["footings"][f]["xcop"]["rms"], D=RES["footings"][f]["hg2"]["D_pred"]) for f in FEET}
RG1M = {"cl": False}
def sig_core(foot, tag, M):
    return (RG1.S_mt(M, tag) if RG1M["cl"] else RG1.S_nat(M, tag)) * MSUNE / PCm ** 2, True
Bk = RG1.B_smooth
def solve_r0(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(Bk(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    if lm(pk.x) < math.log(Mtot): SAT["n"] += 1; return math.exp(pk.x)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), pk.x, xtol=1e-14))
_R = dict(cl2=_CL2, native={})
for f in FEET:
    RG1M["cl"] = True; xa = xcop_cl2(f); RG1M["cl"] = False; hb = hg2_cl2(f)
    _R["native"][f] = dict(xcop={k: xa[k] for k in ("mean", "rms", "n", "saturated", "per_cluster", "by_x", "verdict", "info")}, hg2={k: hb[k] for k in ("D_pred", "n_bright", "n_faint", "interval", "verdict", "reported")})
    P(f"RG1 native [{f}] X-COP {xa['mean']:+.3f} / {xa['rms']:.3f} {xa['verdict']}; HG2 D {hb['D_pred']:+.3f} {hb['verdict']}")
json.dump(_R, open(os.path.join(HERE, "rg1_p45" + ("_MUTATE" if RG1.MUT != 1 else "") + ".json"), "w"), indent=1, default=float)
''' + a) + ho1[_i + len(a):]
env = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1")
code = 0
for name, txt in ((("_rg1_ho2_copy.py", ho2), ("_rg1_ho1_copy.py", ho1))[int(os.environ.get("RG1_ONLY_HO1", "0")):]):
    p = os.path.join(HERE, name); open(p, "w").write(txt)
    r = subprocess.run(["nice", "-n", "15", sys.executable, p], cwd=HERE, env=env, capture_output=True, text=True)
    open(os.path.join(HERE, name + ".log"), "w").write(r.stdout[-20000:] + "\n--stderr--\n" + r.stderr[-6000:]); print(name, "exit", r.returncode, r.stderr[-500:]); code |= r.returncode
sys.exit(code)
