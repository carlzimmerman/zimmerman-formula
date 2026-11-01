#!/usr/bin/env python3
"""DR3 read-across (FROZEN_CRITERIA.md): UR3's DiskMass and Milky Way with the true disc monopole in the response. UR3, RG1, GD3 read only. Doesn't enter DR3's label. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*matmul.*")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); UR = os.path.join(RB, "UR3_direct_weighing"); OUT = []; RES = {}
def P(s): print(s, flush=True); OUT.append(s)
PREF = 'HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from ur3_common import *'
def load(fn, stop, extra=()):
    s = open(os.path.join(UR, fn)).read(); assert s.count(PREF) == 1; s = s.replace(PREF, f'HERE = {UR!r}; sys.path.insert(0, HERE); from ur3_common import *'); s = s[:s.index(stop)]
    for a, b in extra: assert s.count(a) == 1, a; s = s.replace(a, b)
    ns = {"__file__": os.path.join(UR, fn), "__name__": "m"}; exec(compile(s, fn, "exec"), ns); return ns
A = load("ur3_diskmass.py", 'R = {}; P("UR3 Part A'); J = json.load(open(os.path.join(UR, "ur3_diskmass.json"))); Mo = A["Mbar"]
def mx(r, M, h): x = r / h; return M * (1 - (1 + x) * np.exp(-x))
def Mm(r, t, Y, BD): return np.maximum.accumulate(mx(r, Y * t["Ld"], t["hR"]) + mx(r, t["Ma"], 2 * t["hR"]) + mx(r, t["Mm"], t["hR"]) + Y * t["Ld"] * BD)
P("DR3 read-across on UR3; kappa = 1/2 FITTED, unused; not theory closed"); ok = True
for mo in ("blum", "gnedin"):
    A["Mbar"] = Mo; a = A["run"](mo); d = abs(a["r"] - J[f"1.5 hR|{mo}"]["r"]); ok &= d <= 1e-3; A["Mbar"] = Mm; b = A["run"](mo); c = A["run"](mo, fR=2.2); rs = np.array(b["rs"]); bs = np.median(np.random.default_rng(1).choice(rs, (4000, len(rs))), axis=1); RES[f"DiskMass|{mo}"] = dict(off=[a["r"], a["Y"], a["fc"], a["n"]], dr3=[b["r"], b["Y"], b["fc"], b["n"]], ci=[float(np.percentile(bs, 16)), float(np.percentile(bs, 84))], dr3_22=[c["r"], c["Y"]], k=d)
    P(f"DiskMass {mo}: monopole off r {a['r']:.3f} Y_K {a['Y']:.3f} share {a['fc']:.2f} n {a['n']} (|d| to UR3 {d:.1e}); on r {b['r']:.3f} [{RES[f'DiskMass|{mo}']['ci'][0]:.3f}, {RES[f'DiskMass|{mo}']['ci'][1]:.3f}] Y_K {b['Y']:.3f} share {b['fc']:.2f} n {b['n']}: {'NOT DECIDED' if b['n'] < 27 else 'REACHED' if 0.9 <= b['r'] <= 1.1 else 'NOT REACHED'}; at 2.2 hR r {c['r']:.3f} Y_K {c['Y']:.3f}")
_DR = [False]; _MC = {}
RGP = ('f"HERE = {RGD!r}")', 'f"HERE = {RGD!r}").replace("s = open(P).read();", "s = open(P).read().replace(\'return dict(Mb=Mt * Mu,\', \'return dict(rhof_=rhof, Mb=Mt * Mu,\');")')
GP = ('Mbg = np.maximum.accumulate(Mbg) * mut', 'Mbg = DR3_MONO(bar, rg) * mut if DR3_ON[0] else np.maximum.accumulate(Mbg) * mut')
def mono_table(bar):
    k = id(bar)
    if k in _MC: return _MC[k]
    Re = np.r_[0.0, np.geomspace(1e-3, 400.0, 500)]; Ze = np.r_[0.0, np.geomspace(1e-3, 100.0, 220)]; Rm = 0.5 * (Re[1:] + Re[:-1]); Zm = 0.5 * (Ze[1:] + Ze[:-1]); RR, ZZ = np.meshgrid(Rm, Zm, indexing="ij"); rho = bar["rhof_"](RR.ravel(), ZZ.ravel()).reshape(RR.shape); dm = rho * 2 * math.pi * RR * np.diff(Re)[:, None] * np.diff(Ze)[None, :] * 2; r = np.hypot(RR, ZZ).ravel(); o = np.argsort(r); c = np.cumsum(dm.ravel()[o]); _MC[k] = (r[o][::200], c[::200], float(c[-1]) / bar["Mb"]); return _MC[k]
def mono(bar, rg): r, c, q = mono_table(bar); return np.maximum.accumulate(np.interp(np.log(rg), np.log(np.maximum(r, 1e-6)), c, left=0.0) / q)
B = load("ur3_mw.py", 'g["MODE"].update(', extra=(RGP, GP)); B["DR3_ON"] = _DR; B["DR3_MONO"] = mono; g2, CELLS, classify, MCM = B["g2"], B["CELLS"], B["classify"], B["MCM"]; B["g"]["MODE"].update(m="native", t="A_c2b_refit"); Jm = json.load(open(os.path.join(UR, "ur3_mw.json")))["rows"]; t = "A_c2b_refit"
_x = np.array([8.0, 2 * 2.6, 3 * 2.6, 4 * 2.6, 20.0]); P(f"McMillan: integrated density over Mb {mono_table(MCM)[2]:.3f}; cells min, max " + f"{min(mono_table(c['bar'])[2] for c in CELLS):.3f}, {max(mono_table(c['bar'])[2] for c in CELLS):.3f}")
for mo in ("blum", "gnedin"):
    for on in (False, True):
        _DR[0] = on; m = g2(MCM, t, mo); rows = [g2(c["bar"], t, mo) for c in CELLS]; c = classify(rows); ip = [(CELLS[i], r) for i, r in enumerate(rows) if CELLS[i]["tag_Rd_IN"] and CELLS[i]["tag_Mstar_IN"] and all(r[l] for l in ("L1", "L2a", "L2b", "L3"))]; RES[f"MW|{mo}|{'on' if on else 'off'}"] = dict(cls=c["cls"], n_all=c["n_all"], n_inprior=len(ip), mcm=[m["vc_R0"], m["K_R0"], m["Qr0"]], best_D=c["best"]["D"], inprior_D=c["best_in_prior"] and c["best_in_prior"]["D"], cells=[[a["R_d"], a["Mstar"], r["vc_R0"], r["K_R0"], r["Qr0"]] for a, r in ip[:4]])
        P(f"MW {mo} monopole {'on' if on else 'off'}: {c['cls']}, all4 {c['n_all']}, in-prior {len(ip)}, best D {c['best']['D']:.2f}, in-prior best D {c['best_in_prior'] and round(c['best_in_prior']['D'], 2)}; McMillan V_c {m['vc_R0']:.1f} K_z {m['K_R0']:.1f} Q(R0) {m['Qr0']:.2f}" + ("; " + "; ".join(f"Rd {a['R_d']:.2f} M* {a['Mstar']:.2e} Vc {r['vc_R0']:.0f} K {r['K_R0']:.1f}" for a, r in ip[:3]) if ip else ""))
        if not on:
            u = Jm[f"{t}|d0|{mo}"]; d = abs(u["mcmillan"]["vc_R0"] - m["vc_R0"]) + abs(u["mcmillan"]["K_R0"] - m["K_R0"]); same = u["cls"] == c["cls"] and u["n_all"] == c["n_all"]; RES[f"MW|{mo}|k"] = [d, same]; ok &= d <= 1e-3 and same; P(f"  reproduces UR3: |d| {d:.1e}, class same {same}")
RES["K_ur3"] = bool(ok); P(f"K UR3 reproduced with the monopole off: {'PASS' if ok else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "dr3_ur3.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "dr3_ur3.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
