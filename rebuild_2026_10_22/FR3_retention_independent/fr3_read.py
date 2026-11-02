#!/usr/bin/env python3
"""FR3 read: FR1's read path (fr1_read.py text up to its labels, read only), caches. python3 -I fr3_read.py. Reinstates nothing. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, sys, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); FR1 = os.path.join(RB, "FR1_fair_share_retention"); CC = os.path.join(HERE, "cache_jobs"); OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T = open(os.path.join(FR1, "fr1_read.py")).read(); T = T[:T.index("lab = {}")]; ns = {"__file__": os.path.join(FR1, "fr1_read.py"), "__name__": "fr1r"}
with contextlib.redirect_stdout(io.StringIO()) as bb: exec(compile(T, "fr1r", "exec"), ns)
P("FR1's read path up to labels, own internal checks: " + str(ns["CK"])); ok1 = all(ns["CK"].values())
Fc = ns["CC"]; cells = ns["cells"]; rowfor = ns["rowfor"]; label = ns["label"]; FS = ns["FS"]; HH = ns["HH"]
ns["CC"] = CC; J3 = lambda n: json.load(open(os.path.join(CC, re.sub(r"\W", "_", n) + ".json")))
# K1: FR1's H row through my driver
dk = dx = 0.0
for f in FS:
    a = cells(J3(f"KH {f}")); b = json.load(open(os.path.join(Fc, re.sub(r"\W", "_", f"H {f}") + ".json"))); c = cells(b); dk = max(dk, max(abs(a[h][k]["pred"] - c[h][k]["pred"]) for h in HH for k in a[h])); xa = J3(f"KH {f}")["footings"]["canonical"]; xb = b["footings"]["canonical"]; dx = max(dx, abs(xa["mean"] - xb["mean"]), abs(xa["rms"] - xb["rms"]))
K1 = dk <= 1e-6 and dx <= 1e-6; P(f"K1 FR1's H row reproduced, per key and X-COP, both f*: preds {dk:.1e}, X-COP {dx:.1e}: {'PASS' if K1 else 'FAIL'}")
RA = json.load(open(os.path.join(HERE, "fr3_results.json"))); Pr = RA["primary"]; Rr = RA["R"]; Yc = json.load(open(os.path.join(HERE, "fr3_y_ComptonY.json")))
def show(k, name, fs=FS):
    r = rowfor(k, fs); ra = [c["reach"] for f in r for c in r[f]["cell"].values()]; xs = [r[f]["xok"] for f in r]
    P(f"{name}: " + " | ".join(f"f* {f}: {r[f]['keys']}/15 {r[f]['bad'] if r[f]['keys'] < 15 else ''} M3 {r[f]['cell']['h0672']['Z']:+.2f},{r[f]['cell']['h0686']['Z']:+.2f} Ztot {r[f]['cell']['h0672']['Ztot']:+.2f},{r[f]['cell']['h0686']['Ztot']:+.2f} chi2 {r[f]['cell']['h0672']['chi2']:.1f},{r[f]['cell']['h0686']['chi2']:.1f} X-COP {r[f]['xcop'][0]:+.3f},{r[f]['xcop'][1]:.3f} {'PASS' if r[f]['xok'] else 'FAIL'} no-fs {r[f]['no_fs']}" for f in r) + f" | reach {min(ra):.3f} to {max(ra):.3f}"); return r, ra, xs, label(ra, r, False, xs)
P("\nGas +0.005; cells f* 0.034, 0.0615; h 0.672, 0.686"); ROWS = {}
ROWS["KH"] = show("KH", "H (FR1's, reproduced)")
for k, n in (("R", "R, anchored, LABEL ROW"), ("Rfit", "R, own fit"), ("Rup", "R + 0.044"), ("Rdn", "R - 0.044"), ("Rcarry", f"R with y carry {Yc['c']:+.3f}, reported")): ROWS[k] = show(k, n)
xm = J3("MUT flip 0.034")["footings"]["canonical"]; Mm = cells(J3("MUT flip 0.034"))["h0672"]["G-OUT-M3"]["Z"]; R0 = cells(J3("R 0.034"))["h0672"]["G-OUT-M3"]["Z"]; bite = abs(xm["mean"]) > .05 or abs(Mm - R0) > .5; P(f"MUTATE (b) slope flip on R: X-COP {xm['mean']:+.3f}, {xm['rms']:.3f}, no-fs {J3('MUT flip 0.034')['zn1']['no_fs']}, M3 {Mm:+.2f} vs {R0:+.2f}: {'BITES' if bite else 'DOES NOT BITE'}"); open(os.path.join(HERE, "fr3_grade_MUTATE.out"), "w").write("\n".join(OUT[-1:]) + "\n")
# budget at frozen mock term
Sfz = math.sqrt(Pr["sY"] ** 2 + Pr["Sap"] ** 2 + Pr["Sbi"] ** 2 + .0036 ** 2 + Pr["Ssh"] ** 2); P(f"\nsigma_tot on lg Y, mock term as frozen (no mass function): {Sfz:.3f}. With the added mass-function term (+0.031): {Pr['St']:.3f}. Eligible below 14.3: {Rr['n143']}")
Lb = ROWS["R"][3]; V = "NO INDEPENDENT MEASUREMENT" if (Sfz > .04 or Rr["n143"] < 15) else Lb; tg = []
if not all(ROWS["R"][2]): tg.append("[X-COP LOST]")
if ROWS["Rup"][3] != Lb or ROWS["Rdn"][3] != Lb: tg.append("[ERROR-DEPENDENT]")
if Pr["St"] > .04: tg.append("[BUDGET-DEPENDENT: added mass-function term gives NO INDEPENDENT MEASUREMENT]")
valid = K1 and ok1 and bite; P(f"VERDICT FR1's labels{'' if valid else ' NOT VALID'}: {V} {' '.join(tg)}")
r = J3("R 0.034"); D = r["dump"]; Al = sorted([v for v in D.values() if v["i"] is not None], key=lambda v: v["Mb200"]); M3 = Al[-len(Al) // 3:]; med = lambda k: float(np.median([v[k] for v in M3])); P(f"M3 on R: lg M500 {med('lgM500'):.3f}, Y500 lg {math.log10(med('Y500_line')):+.3f}, carry lg {math.log10(med('carry')):+.3f}, Y200 lg {math.log10(med('Y200')):+.3f}; HM1's need -0.127 (Z 2) to -0.203 (Z 0); closure {math.log10(med('Y500_model') / med('Y500_line')):+.4f} dex")
qq = .7 / 0.6758; A = Rr["anchored"]; P("\nRead-across, report only: EM1 against line R (anchored), M3's carry, as FR1's table")
for lb in (12.5, 13, 13.5, 14):
    lgc = 11.18 + .9 * (lb - 10); M2 = lgc - math.log10(5.2715 / 6.2715); y = 6.2715 * 10 ** lb / 10 ** M2; lm5 = M2 - .15; l5 = A["a"] + A["b"] * (lm5 - math.log10(qq) - 14.5) + math.log10(1.034) + 1.5 * math.log10(qq); P(f"  lg M_b {lb}: EM1 Y200 lg {math.log10(y):+.3f}; R with carry {l5 + math.log10(med('carry')):+.3f}; R minus EM1 {l5 + math.log10(med('carry')) - math.log10(y):+.3f}")
s = lambda c: {k: v for k, v in c.items() if k != "x"}
json.dump({k: dict(row=v[0], label=v[3]) for k, v in ROWS.items()} | dict(verdict=V, tags=tg, K1=K1, S_frozen=Sfz, valid=valid), open(os.path.join(HERE, "fr3_grade_results.json"), "w"), indent=0, default=float); open(os.path.join(HERE, "fr3_grade.out"), "w").write("\n".join(OUT) + "\n")
