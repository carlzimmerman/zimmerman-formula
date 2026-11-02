#!/usr/bin/env python3
"""TM2 Part C: F2, W2 on MG1's isolated pair, with age. Table PROVISIONAL; ages PROXY unless stated. TM2_MUTATE=1: control on gas. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, csv, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); MD = os.path.join(RB, "MG1_merger_sample")
POST = os.environ.get("TM2_POST", "0") == "1"; MUT = os.environ.get("TM2_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ("_POST" if POST else "")
OUT = open(os.path.join(HERE, f"tm2_mg1{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
G = 6.674e-11; KPC = 3.0857e19; MSUN = 1.989e30; SIG_CRIT = 1.827e9; MYR = 3.15576e13; KMS = 1.02271e-3
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt"); KFIT = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_kfit.json")))
OBSJ = json.load(open(os.path.join(MD, "mg1_results.json")))["obs"]
SC = 6.61*60
def vec_err(a, ea, b, eb):
    d = np.array(a) - np.array(b); n = float(np.hypot(*d)); u = d/n; e = math.sqrt((u[0]**2)*(ea[0]**2 + eb[0]**2) + (u[1]**2)*(ea[1]**2 + eb[1]**2)); return n*SC, e*SC
J25 = dict(SE=dict(l=(-0.70, -0.43), el=(0.25, 0.06), g=(-0.79, -0.50), eg=(0.20, 0.20)), NW=dict(l=(0.46, 0.20), el=(0.13, 0.04), g=(0.39, 0.18), eg=(0.20, 0.20)))
rows = list(csv.DictReader(open(os.path.join(MD, "mg1_table.csv"))))
for r in rows:
    if r["system"] == "MACS J0025":
        p = J25[r["sub"]]; c_ = vec_err(p["g"], p["eg"], (1e-9, 1e-9), (0.08, 0.08)); r["s"] = c_[0]
    for k in ("s", "M_lens", "a_gas", "a_star"): r[k] = float(r[k])
    for k, f in (("M_gas", 0.12), ("M_star", 0.02)): r[k] = f*r["M_lens"] if r[k] == "DEFAULT" else float(r[k])
AGE = {"Bullet": 180.0, "Musket Ball": 1100.0}
def law(g, a): return 0.5*g + np.sqrt(0.25*g*g + a*g)
def fld(X, Y, Z, M, a, xc):
    dx = X - xc; f = -G*M*MSUN/((dx*dx + Y*Y + Z*Z + a*a)**1.5*KPC**3)*KPC; return f*dx, f*Y, f*Z
ZM = np.concatenate([np.linspace(0.0, 1200.0, 61), np.geomspace(1200.0, 6000.0, 41)[1:]])
def sig_pl(D, M, a): return M*a*a/(math.pi*(D*D + a*a)**2)
TAUS = ("Rdyn", "T50", "T200", "T1000", "T5000") if not POST else ("Rdyn", "T200", "T300", "T600", "T1000", "T5000")
if POST: KFIT = {f: math.pi**2 for f in FEET}  # A1, post-result
def run(gas, star, s, t, Mlens, step=20.0, h=2.0):
    w_ = max(0.5*s + 300.0, 500.0); xs = np.arange(0.5*s - w_, 0.5*s + w_ + 1e-9, step); ys = np.arange(-400.0, 400.0 + 1e-9, step); XX, YY = np.meshgrid(xs, ys, indexing="ij")
    e = np.r_[np.linspace(0, t, 5), np.geomspace(t, 10000.0, 9)[1:]]; sn = 0.5*(e[1:] + e[:-1]); g_ = np.maximum(0, 1 - sn/t); ug = 0.5*s/t
    Wpos = s*(1 - g_); Fpos = -np.minimum(ug*sn, 3500.0)  # gas centre at node; gas now at 0, stars at s
    res = {}; S = {}; keys = [f"{fm}|{ta}|{f}" for fm in ("F2", "W2") for ta in TAUS for f in FEET] + [f"LAW||{f}" for f in FEET]
    for n in keys: S[n] = np.zeros_like(XX)
    tdyn = {f: math.sqrt(300*KPC/law(G*Mlens*MSUN/(300*KPC)**2, A0F[f]))/MYR for f in FEET}
    for j0 in range(0, len(ys), 8):
        yy = ys[j0:j0 + 8]; X, Y, Z = np.meshgrid(xs, yy, ZM, indexing="ij"); div = {n: 0.0 for n in keys}
        for ax, d_ in enumerate(((h, 0, 0), (0, h, 0), (0, 0, h))):
            for sgn in (1.0, -1.0):
                Xa, Ya, Za = X + sgn*d_[0], Y + sgn*d_[1], Z + sgn*d_[2]; gv = fld(Xa, Ya, Za, gas[0], gas[1], 0.0); st = fld(Xa, Ya, Za, star[0], star[1], s); F = [fld(Xa, Ya, Za, gas[0], gas[1], p) for p in Fpos]; W = [fld(Xa, Ya, Za, gas[0], gas[1], p) for p in Wpos]
                for f in FEET:
                    a0 = A0F[f]; gb = [gv[i] + st[i] for i in range(3)]; gb[1] = gb[1] + a0/1000.0; g = np.sqrt(gb[0]**2 + gb[1]**2 + gb[2]**2); L = law(g, a0); m = L/np.maximum(g, 1e-300); base = gb[ax]*(m - 1); div[f"LAW||{f}"] = div[f"LAW||{f}"] + sgn*base
                    for ta in TAUS:
                        tau = tdyn[f] if ta == "Rdyn" else float(ta[1:]); w = np.exp(-e[:-1]/tau) - np.exp(-e[1:]/tau); w = w/w.sum()
                        for fm, A in (("F2", F), ("W2", W)):
                            v = sum(w[i]*A[i][ax] for i in range(len(w))); n = f"{fm}|{ta}|{f}"; div[n] = div[n] + sgn*(base + KFIT[f]*(L/a0)*v)
        for n in keys: S[n][:, j0:j0 + 8] = 2.0*np.trapz(-div[n]/(2*h)/(4*math.pi*G)*KPC**2/MSUN, ZM, axis=2)
    b_ = sig_pl(np.hypot(XX, YY), gas[0], gas[1]) + sig_pl(np.hypot(XX - s, YY), star[0], star[1]); dq = np.hypot(XX, YY) <= 100.0; dg = np.hypot(XX - s, YY) <= 100.0
    for n in keys:
        T = S[n] + b_; i, j = np.unravel_index(int(np.argmax(T)), T.shape); res[n] = dict(delta=float(np.hypot(xs[i], ys[j])/s), dkappa=float((T[dg].mean() - T[dq].mean())/SIG_CRIT))
    if True:
        T = S["LAW||canonical"] + b_; ctl = sig_pl(np.hypot(XX - (0.0 if MUT else s), YY), 3e14, 150.0); res["control"] = float(((T + ctl)[dg].mean() - (T + ctl)[dq].mean())/SIG_CRIT)
    return res, tdyn
say("="*90); say("TM2 Part C, pair model" + ("  [MUTATE]" if MUT else "")); say("="*90)
MODEL = {}; PR = []
for r in rows:
    tag = f"{r['system']} {r['sub']}"; ob = OBSJ.get(tag); prim = bool(ob and ob["counted"] and ob["s_over_row"] >= 2.0); lab = ob["label"] if ob else "GAL"
    if r["system"] == "Bullet": prim = False
    if not (prim or r["system"] == "Bullet" or r["system"] in ("Abell 2034",)): continue
    if MUT and r["system"] != "Bullet": continue
    ages = [AGE[r["system"]]] if r["system"] in AGE else [r["s"]/(v*KMS) for v in (1000.0, 500.0, 1500.0)]
    if r["system"] == "Musket Ball": ages += [700.0, 2400.0]
    MODEL[tag] = {}
    for it, t in enumerate(ages):
        m, td = run((r["M_gas"], r["a_gas"]), (r["M_star"], r["a_star"]), r["s"], t, r["M_lens"]); MODEL[tag][f"t{t:.0f}"] = m
        if it == 0: PR.append((tag, lab, prim, f"t{t:.0f}"))
        say(f"{tag:18s} {lab:8s} age {t:5.0f} Myr, tdyn {td['canonical']:.0f}; W2 dk " + " ".join(f"{a_}:{m[f'W2|{a_}|canonical']['dkappa']:+.3f}" for a_ in TAUS) + " | F2 dk " + " ".join(f"{a_}:{m[f'F2|{a_}|canonical']['dkappa']:+.3f}" for a_ in TAUS) + f" | law {m['LAW||canonical']['dkappa']:+.3f}; delta W2 Rdyn {m['W2|Rdyn|canonical']['delta']:.2f}, T5000 {m['W2|T5000|canonical']['delta']:.2f}")
K6 = MODEL["Bullet main"]["t180"]["control"]; ok6 = K6 > 0; say(f"  [{'PASS' if ok6 else 'FAIL'}] K6c: mass on galaxies, Bullet main, dkappa {K6:+.3f}")
if MUT:
    say("MUTATE required failure: K6c " + ("FAILED" if not ok6 else "passed (BAD)")); OUT.close(); sys.exit(1)
TALLY = {}
GALR = [p for p in PR if p[2] and p[1] == "GAL"]
for fm in ("F2", "W2"):
    for ta in TAUS:
        for f in FEET:
            n = sum(MODEL[t][a][f"{fm}|{ta}|{f}"]["dkappa"] > 0 for t, _, _, a in GALR); TALLY[f"{fm}|{ta}|{f}"] = [n, len(GALR), "HOLDS" if n >= 2/3*len(GALR) else "FAILS"]; say(f"  {fm} {ta} {f}: dkappa > 0 at {n} of {len(GALR)} GAL rows, {TALLY[f'{fm}|{ta}|{f}'][2]}")
json.dump(dict(model=MODEL, tally=TALLY, K6c=K6), open(os.path.join(HERE, f"tm2_mg1{TAG}.json"), "w"), indent=0, default=float); OUT.close()
