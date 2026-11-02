#!/usr/bin/env python3
"""BK1 gate 5 calibration (FROZEN_CRITERIA.md), before any target search. --mutate: G's dimension wrong, C2 must fail. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, subprocess, sys, resource
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from bk1_engine import *
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
RES = {}
# C1
A = os.path.join(REPO, "project_atomos"); r = subprocess.run([sys.executable, "-B", os.path.join(A, "calibration", "calibrate.py")], capture_output=True, text=True, cwd=A); line = [l for l in r.stdout.splitlines() if "CALIBRATION VERDICT" in l]; P("C1 atomos: " + (line[0] if line else "NO VERDICT")); RES["C1"] = dict(line=line[0] if line else None, ok=bool(line and "8/8" in line[0]), note="a0's Gate A pass in it is the unit mismatch in FROZEN_CRITERIA")
# CAL alphabet
LV = dict(G=6.67430e-11, c=2.99792458e8, H0=2.184e-18, Lambda=1.1e-52, rho_c=9.5e-27, l_P=1.616e-35, t_P=5.391e-44, m_P=2.176e-8)
T = Tree(LV, dims={"G": (2, -1, -2)} if MUT else None)
for d in (2, 3): T.layer(d)
a0 = 1.2e-10; sig = math.hypot(.02e-10, .24e-10); WS = [Window("a0_sigma", a0, sig), Window("a0_5pc", a0, a0 * .05 / 2), Window("a0_10pc", a0, a0 * .10 / 2)]
H, _, rows, zh, st = search(T, TARGET_DIMS["accel"], WS); cum = cumulative(H); P(f"tried {st['tried_formal']}, dim-correct {st['dimcorrect']}, distinct <=3 {st['distinct']}")
RES["tree_counts"] = st
# C2 winner
nm = T.names; v = T.vals(); ig, ic, ir = nm.index("G"), nm.index("c"), nm.index("rho_c"); t = 0
ex = np.zeros(T.k); ex[ic] = 1; ex[ig] = .5; ex[ir] = .5; lval = ex @ T.lv + math.log10(.5); dim_ok = (dkey(ex @ T.D) == dkey(TARGET_DIMS["accel"])).all()
found = False; w10 = WS[2]; R = rows["a0_10pc"]; x = prune(R, w10, 10 ** 7) if R else (np.array([]),) * 4
found = bool(dim_ok and len(x[0]) and (np.abs(x[0] - lval) < 1e-8).any())
P(f"C2: c sqrt(G rho_c)/2 = {10 ** lval:.4e}, err vs 1.2e-10 {abs(10 ** lval / a0 - 1) * 100:.2f} %, in dim-correct depth 4 list: {found}, hits within 10 % at depth 4 listed {len(x[0])}"); RES["C2"] = dict(value=10 ** lval, found=found)
# C3
cf = .5 * (3 / (8 * PI)) ** .5; dec = decompose(cf); P(f"C3: coefficient after Friedmann {cf:.6f}, decompositions {dec[:4]}"); RES["C3"] = dict(coef=cf, decs=[str(d) for d in dec[:6]], ok=any(len(d[0]) == 2 and {f[0] for f in d[0]} == {"einstein", "friedmann"} and d[1] == "1/2" for d in dec)); RES["reg_set_size"] = mech_rate()
# C4
occ = np.where((H[1] + H[2] + H[3] + H[4]) > 0)[0]; span = (LO + BIN * occ.min(), LO + BIN * occ.max()) if len(occ) else None; RES["span"] = span; P(f"occupied span, lg accel {span}")
RES["C4"] = {}
for w in WS:
    RES["C4"][w.name] = dict(local=grade(cum, w), span=grade(cum, w, span=span) if span else None, z_hist=zh[w.name].tolist())
    for nm2 in ("local", "span"):
        g = RES["C4"][w.name][nm2]
        if g: P(f"C4 {w.name} {nm2}: d* {g['dstar']} P {g.get('P')} bits(x15) {g.get('bits')} ceiling {g['ceiling_bits']:.2f}; " + "; ".join(f"d{d}: {x_['real']} vs {x_['ctrl_mean']:.2f}, P {x_['ctrl_P']:.3f}" for d, x_ in g["depth"].items()))
# C5 negatives, through this gate at tolerance 1e-3, numbers-only effective alphabet A without f_b, canonical
a00 = 9.360324825027975e-11; rho = (2 * a00 / 2.99792458e8) ** 2 / 6.6743e-11
TA = Tree(dict(c=2.99792458e8, G=6.6743e-11, rho=rho, a0=a00))
for d in (2, 3): TA.layer(d)
NEG = [("alpha_inv_4Z2p3", 137.035999), ("mmu_me_64piZ", 206.76828), ("mtau_mmu_Zp11", 16.817), ("mp_me_6pi5", 1836.15267), ("sin2W_3over13", .23122)]
WN = [Window(n, x, x * 1e-3 / 2) for n, x in NEG] + [Window("K_pi2_row", 13.2868, 3.2279), Window("PLANT_kernel", math.sqrt(8 * PI / 3) / 2, 1e-4)]
H2, _, rn, _, stn = search(TA, TARGET_DIMS["none"], WN, cap=2000); cum2 = cumulative(H2); RES["C5"] = {}; RES["alpha_A_counts"] = stn
for w in WN:
    g = grade(cum2, w); RES["C5"][w.name] = g; P(f"C5 {w.name}: d* {g['dstar']} P {g.get('P')} bits {g.get('bits')} ceiling {g['ceiling_bits']:.2f}; depth hits " + ", ".join(f"{x_['real']}/{x_['ctrl_mean']:.1f}" for x_ in g["depth"].values()))
# K checks
fm = T.tried[2]; RES["K1"] = bool(abs(10 ** lval - 1.1878e-10) / 1.1878e-10 < .05)
small = Tree(dict(c=2.99792458e8, G=6.6743e-11)); small.layer(2); RES["K2"] = dict(tried2=small.tried[2], hand=2 * 12 + 2 * 14 + 3 + 4, ok=small.tried[2] == 2 * 12 + 2 * 14 + 3 + 4)
P(f"K2 hand count depth 2, 2 leaves: {small.tried[2]}, hand 12 x 2 unary + 14 x 2 decoration + 3 mul + 4 div = {2 * 12 + 2 * 14 + 3 + 4}; a first hand count of 58 in this script forgot x/x")
hand = int(((T.d <= 3) & (T.dimk() == dkey(TARGET_DIMS['accel'])).all(1) & (T.vals() >= WS[0].lo) & (T.vals() <= WS[0].hi)).sum()); hist_c = int(counts(cum[3], [WS[0].lo], [WS[0].hi])[0]); RES["K3"] = dict(exact=hand, hist=hist_c, ok=hand == hist_c); P(f"K3 exact {hand} hist {hist_c}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; print(f"K5 RSS {rss:.2f} GB", flush=True); RES["K5_ok"] = bool(rss < 4)
# labels
bref = RES["C4"]["a0_sigma"]["local"].get("bits"); RES["B_ref"] = bref; neg = [RES["C5"][n].get("bits") or 0 for n, _ in NEG]; a_a = bool(bref is not None and bref >= 10); a_b = bool(bref is not None and all(x < bref for x in neg)) if bref and bref > 0 else False; RES["neg_max_bits"] = max(neg); hc = RES["C1"]["ok"] and found and RES["C3"]["ok"]
nb = {n: (x.get("bits"), x.get("P")) for n, x in RES["C5"].items()}; RES["a0_bits_no_lee"] = {w.name: {k: (None if RES["C4"][w.name][k].get("P") in (None, 0) else -math.log2(RES["C4"][w.name][k]["P"])) for k in ("local", "span")} for w in WS}; P(f"a0 bits without x15: {RES['a0_bits_no_lee']}"); P(f"PLANT without x15: {-math.log2(RES['C5']['PLANT_kernel']['P']):.2f}")
lab = "CERTIFIES" if (hc and a_a and max(neg) < 10) else "CERTIFIES AT B ONLY" if (hc and a_b) else "DOES NOT CERTIFY"; RES["label"] = lab; P(f"GATE 5 LABEL: {lab}; B_ref {bref}; negatives max bits {max(neg)}")
json.dump(RES, open(f"bk1_cal{TAG}.json", "w"), indent=1, sort_keys=True, default=lambda o: o.item() if hasattr(o, "item") else str(o)); open(f"bk1_cal{TAG}.out", "w").write("\n".join(OUT) + "\n")
