#!/usr/bin/env python3
"""RET1 POST-RESULT, no verdict: the frozen P rule outruns the SN energy above V_esc 333 km/s (epsilon 1), so cap it at E1. Also the slope's closed form. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80"); TG = ("A_c2b_refit", "B_cfg886_bg"); RES = os.path.join(HERE, "ret1_post_results.json"); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); r10, r11 = J["r10"], J["r11"]
if not os.path.exists(RES):
    W = os.path.join(HERE, "cache_post"); os.makedirs(W, exist_ok=True); a = open(os.path.join(HERE, "ret1_tail_add.py")).read(); c = a.index('_K = _run("EM1", "off")')
    a = a[:c].replace('def _mubase(mode, V2): return _VSN2 / V2 if mode == "E" else _PSN / math.sqrt(V2)', 'def _mubase(mode, V2):\n    if isinstance(mode, tuple): return min(_VSN2 / V2, mode[1] * _PSN / math.sqrt(V2))\n    return _VSN2 / V2 if mode == "E" else _PSN / math.sqrt(V2)')
    a += '''
_R = dict(EPS=_EPS, runs={})
_MC = {t: ("C", 1.0) for t in _TG}; _MF = {t: ("C", _EPS["P"][t]) for t in _TG}
def _setm(M):
    SLMAP["m"] = "RET"; SLMAP["f"] = lambda lMb, bg, rc: 10 ** _solve(lMb, _TAGOF(bg), M[_TAGOF(bg)], 1.0)
for nm, M_ in (("C1", _MC), ("CF", _MF)):
    for m_ in ("off", "blum"): _setm(M_); _R["runs"][f"{nm}|{m_}"] = _run("RET", m_)
_GR = [7, 8, 9, 10, 10.25, 10.5, 10.59, 10.75, 10.8, 11, 11.5, 12, 13, 14]
_R["lines"] = {t: {n: {str(x): _solve(x, t, M_[t], 1.0) for x in _GR} for n, M_ in (("C1", _MC), ("CF", _MF))} for t in _TG}; _R["EM1"] = {t: {str(x): BGS[t]["a"] + BGS[t]["b"] * (x - 10) for x in _GR} for t in _TG}
_R["V333_lMb"] = {t: _epsreq(10.25, t, "E")[1] for t in _TG}
json.dump(_R, open(os.environ["SL1_OUT"], "w"), indent=1, default=float); print("RET1 post done", flush=True); sys.exit(0)
'''
    t = open(os.path.join(UR1, "ur1_tail.py")).read(); t = t[:t.index("import time as _tm")] + a; tl = os.path.join(W, "ret1_tail.py"); open(tl, "w").write(t)
    U1 = open(os.path.join(UR1, "ur1.py")).read(); PRE = eval(re.search(r'pre = (""".*?""")', U1, re.S).group(1)); a = "\\n    M = SLMAP['mut']"; assert PRE.count(a) == 1
    PRE = PRE.replace(a, "\\n    if SLMAP['m'] == 'RET': M = SLMAP['f'](lMb, bg, rc); return M, (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)" + a); d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(PRE) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, "NR2_MEDIAN_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "ret1_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=RES, CN1_FORCE="1", OMP_NUM_THREADS="1", UR1_DRIVER="1"); subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(HERE, "ret1_post_run.log"), "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(RES): raise SystemExit("no result, see ret1_post_run.log")
R = json.load(open(RES)); P("RET1 post-result, no verdict; kappa = 1/2 FITTED, unused; not theory closed. C1: mu = min(E, P) at epsilon 1. CF: mu = min(E at 1, epsilon_P P).")
for n, r in R["runs"].items():
    s = r["sparc"]; P(f"{n}: U {s[TG[0]]['U']:.2f}/{s[TG[1]]['U']:.2f} rms {s[TG[0]]['rms']:.4f}/{s[TG[1]]['rms']:.4f} tilt {s[TG[0]]['tilt']:+.2f}/{s[TG[1]]['tilt']:+.2f} bins {[round(v, 2) for v in s[TG[0]]['bins'].values()]}; groups {r['groups']['Z']:+.2f} {r['groups']['verdict']}; LT {r['lt'][TG[0]]:+.3f}/{r['lt'][TG[1]]:+.3f}")
for t in TG:
    for n in ("C1", "CF"):
        L = R["lines"][t][n]; E_ = R["EM1"][t]; P(f"{t} {n}: slope(9-11) {(L['11'] - L['9']) / 2:.3f}; d from EM1 " + ", ".join(f"{k} {L[k] - E_[k]:+.2f}" for k in L))
# closed form: mu >> 1, V^2 ~ M^(2/3): M^(4/3) ~ M*, so slope = (3/4) dlgM*/dlgM_b
rows = []
for l in open(os.path.join(RB, "..", "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = l.split()
    if len(p) < 18: continue
    try: rows.append((float(p[7]), float(p[13])))
    except ValueError: pass
A = np.array([r for r in rows if r[0] > 0]); rng = np.random.default_rng(1); O = {}
for Y in (0.35, 0.5, 0.7):
    x = np.log10((Y * A[:, 0] + 1.33 * A[:, 1]) * 1e9); y = np.log10(Y * A[:, 0] * 1e9); b, a = np.polyfit(x - 10, y, 1); bs = [np.polyfit(x[i] - 10, y[i], 1)[0] for i in (rng.integers(0, len(x), len(x)) for _ in range(2000))]; O[str(Y)] = dict(n=len(x), b=float(b), a=float(a), sb=float(np.std(bs)), scatter=float(np.std(y - a - b * (x - 10))), slope34=float(0.75 * b)); P(f"Upsilon {Y}: dlgM*/dlgM_b {b:.3f} +- {np.std(bs):.3f}, scatter {O[str(Y)]['scatter']:.2f} dex; (3/4) x slope {0.75 * b:.3f}")
try: E1 = json.load(open(os.path.join(RB, "EM1_emergent_dust_law", "em1_emergent_results.json")))["rows"]; P("EM1 R1: " + "; ".join(f"{t} a {E1[t]['R1']['a']} b {E1[t]['R1']['b']}" + (f" sb {E1[t]['R1'].get('sb')}" if 'sb' in E1[t]['R1'] else ' (no b error stored)') for t in TG))
except Exception as e: P(f"EM1 b error not read: {e}")
json.dump(O, open(os.path.join(HERE, "ret1_post_slope.json"), "w"), indent=1); open(os.path.join(HERE, "ret1_post.out"), "w").write("\n".join(OUT) + "\n")
