#!/usr/bin/env python3
"""ET6_core_shape: does the low-mass rise and ET5's floor verdict depend on the chosen core?
python3 et6_shape.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
HERE6 = os.path.dirname(os.path.abspath(__file__)); REB6 = os.path.dirname(HERE6); ET5D = os.path.join(REB6, "ET5_joint_upsilon_pressure")
MUT6 = "--mutate" in sys.argv; SRC5 = open(os.path.join(ET5D, "et5_joint.py")).read()
__file__ = os.path.join(ET5D, "et5_joint.py"); sys.argv = [sys.argv[0]]; exec(compile(SRC5[:SRC5.index('W(f"ET5 joint')], "et5_head", "exec"))
L6 = []
def W(s): print(s, flush=True); L6.append(s)
from scipy.integrate import quad
def _s(x): x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
def _b(x): x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def _p(x): x = np.asarray(x, float); return 4 * (x - np.arctan(x))
def _t(x): x = np.asarray(x, float); return 2 * (np.arctan(x) - x / (1 + x * x))
SH = dict(SMOOTH=_s, BURKERT=_b, PISO=_p, STEEP=_t)
DENS = dict(SMOOTH=lambda x: (1 + x * x) ** -1.5, BURKERT=lambda x: 1 / ((1 + x) * (1 + x * x)), PISO=lambda x: 1 / (1 + x * x), STEEP=lambda x: (1 + x * x) ** -2)
SBASE = solve_r0.__globals__
def setB(n):
    global B
    B = SH[n]; SBASE["B"] = SH[n]
NORM = {n: float(f(1.0) / _s(1.0)) for n, f in SH.items()}
W(f"ET6 core shape; kappa = 1/2 FITTED; footings never pooled; not theory closed{' [MUTATE]' if MUT6 else ''}\nsample {len(SAMPLE)}; norm {NORM}")
RES = dict(mutate=MUT6, norm=NORM); code = 0
def fwd6(tr, S0, s, sig, fw, tag, fitsh="SMOOTH"):
    global iu
    S = []
    for q in SAMPLE:
        setB(tr); iu = iu_of(TAB[q["name"]]["vf"], s); g = forward(q, S0, fw, sig); setB(fitsh); S.append(fit(q, I05, g)[0])
    setB("SMOOTH"); return grade(NM5, S, tag)
if MUT6:
    r = fwd6("BURKERT", FL["canonical"], 0, 0, 0, "Burkert", "BURKERT"); ok = all(98 <= b["med"] <= 118 for b in r["bins"].values()) and r["p"] >= 0.01; code = int(not ok); RES["mut"] = r; W(f"MUTATE recovered floor, no rise: {ok}")
else:
    et2 = json.load(open(os.path.join(REB6, "ET2_free_core_low_mass", "et2_results.json")))["ups"]["0.50"]["gal"]; e5 = json.load(open(os.path.join(ET5D, "et5_results.json")))["C"]
    W("\nChecks"); setB("SMOOTH"); k1 = all(fit(q, I05)[0] == et2[q["name"]]["S"] for q in SAMPLE); W(f"K1 SMOOTH equals ET2: {'PASS' if k1 else 'FAIL'}"); code |= not k1
    k2 = 0.0
    for n in SH:
        for x in (0.1, 1, 10): k2 = max(k2, abs(float(SH[n](x)) / (4 * quad(lambda t: t * t * DENS[n](t), 0, x, epsabs=1e-12, epsrel=1e-12)[0]) - 1))
    W(f"K2 B vs integrated density, max rel {k2:.1e}: {'PASS' if k2 < 1e-6 else 'FAIL'}"); code |= k2 >= 1e-6
    bg = BGS[TAG]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); k3 = 0.0; k4 = []
    for n in SH:
        setB(n)
        for q in sel(100, 150)[:3]:
            M = m200(q); R2 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); r = r0_et1(q, 100.0); k3 = max(k3, abs(math.pi * 100.0 * PCONV * r ** 2 * float(B(R2 / r)) / (M * MSUNE) - 1))
        q = sel(100, 150)[0]; a, b, _, _ = fit(q, I05, np.log10(np.maximum(q["GB"][:, I05] + gh(q, SG[80], RG[20]), 1e-300))); k4.append(a == SG[80] and b == RG[20])
    setB("SMOOTH"); W(f"K3 M(R200) = M200 max rel {k3:.1e}: {'PASS' if k3 < 1e-8 else 'FAIL'}; SAT count {SAT['n'] if 'SAT' in globals() else SBASE['SAT']['n']}"); code |= k3 >= 1e-8
    W(f"K4 plants exact: {k4}: {'PASS' if all(k4) else 'FAIL'}"); code |= not all(k4)
    low = Vf < 150; MS = {}
    for n in SH:
        setB(n); MS[n] = np.array([surface(q, I05)[0].min() for q in SAMPLE])
    setB("SMOOTH"); ratio = {n: float(np.median(MS[n][low]) / np.median(MS["SMOOTH"][low])) for n in SH}; counted = [n for n in SH if ratio[n] <= 1.5]; W(f"\nFit guard, median mse ratio: {ratio}; counted {counted}")
    C = {"SMOOTH": {k: dict(P=v) for k, v in e5.items()}}
    for k, v in C["SMOOTH"].items(): v["N"] = v["P"]
    for n in ("BURKERT", "PISO", "STEEP"):
        setB(n); C[n] = {}; W(f"\n{n}")
        for s in (0, 0.25, 0.5):
            for sig in (0, 8, 12):
                for fw in (0, 30):
                    k = f"s{s}_p{sig}_b{fw}"; a = real(s, sig, fw, f"{s}/{sig}/{fw} P"); Sn = [None if x is None else x * NORM[n] for x in a["S"]]; b = grade(NM5, Sn, f"{s}/{sig}/{fw} N"); C[n][k] = dict(P=a, N=b)
    setB("SMOOTH")
    def verdict(key, v):
        rec, con = [], []
        for n in counted:
            for k, c in C[n].items():
                r = c[key]; cc = contains(r, v); (con.append(n + ":" + k) if cc else 0); (rec.append(n + ":" + k) if cc and r["p"] >= 0.01 else 0)
        al = lambda L: [x for x in L if "s0.5_" not in x]; a = al(rec); b = [x for x in rec if x not in a]; c = al(con)
        return ("SHAPE EXPLAINS IT" if a else ("SHAPE EXPLAINS IT ONLY BEYOND THE BAND" if b else ("FLOOR CONSISTENT, RISE REMAINS" if c else "NOT RECONCILED"))), rec, con
    V = {}
    W("\nVerdicts")
    for f, v in FL.items():
        p, pr, pc = verdict("P", v); nn, nr, nc = verdict("N", v); V[f] = dict(primary=p, normalised=nn, rec_P=pr, con_P=pc, rec_N=nr, con_N=nc); W(f"{f}: {'DEFINITION-DEPENDENT ' if p != nn else ''}PRIMARY {p}; NORMALISED {nn}\n   reconciled P {pr}\n   contained P {pc}\n   reconciled N {nr}\n   contained N {nc}")
    fl = [n for n in counted if not C[n]["s0_p0_b0"]["P"]["rise"]]; rv = "RISE IS SHAPE-FREE" if not fl else "SHAPE-DEPENDENT " + str(fl); W(f"Rise, base cell: {rv}; " + "; ".join(f"{n} rho {C[n]['s0_p0_b0']['P']['rho']:+.3f}" for n in SH))
    W("\nForward, fit SMOOTH"); F = {}
    for n in ("BURKERT", "PISO", "STEEP"):
        for f, v in FL.items():
            for cs, s, sig, fw in (("plain", 0, 0, 0), ("corner", 0.25, 12, 30)):
                r = fwd6(n, v, s, sig, fw, f"{n[:3]} {f[:3]} {cs}"); a_, c_ = r["bins"]["20-60"]["med"], r["bins"]["100-150"]["med"]; r["verdict"] = ("FAKED" if a_ <= 77.3 and c_ >= 136.6 else "PARTIAL") if r["rise"] else "NOT FAKED"; F[f"{n}_{f}_{cs}"] = r; W(f"   -> {r['verdict']}")
    for n in C:
        for c in C[n].values():
            for z in c.values(): z.pop("S", None)
    RES.update(ratio=ratio, counted=counted, C=C, V=V, rise=rv, F=F, K=dict(K1=k1, K2=k2, K3=k3, K4=k4))
t = "_MUTATE" if MUT6 else ""
json.dump(RES, open(os.path.join(HERE6, f"et6_results{t}.json"), "w"), indent=1, default=lambda o: o.item()); open(os.path.join(HERE6, f"et6{t}.out"), "w").write("\n".join(L6) + "\n"); sys.exit(int(code))
