#!/usr/bin/env python3
"""RG1 P2: GD3's X5-box Milky Way with the native-N rule. OS1 mode (K2) reproduces GD3."""
import contextlib, io, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); P = os.path.join(REB, "GD3_smooth_core_mw", "gd3_smooth_core_mw.py")
sys.path.insert(0, HERE); import rg1_lib as L
s = open(P).read(); head = s[:s.index("# ---- K1: smooth mass function")]; body = s[s.index("# ================================================================== stage M"):s.index("# K2: Burkert + OS1 q_f reproduces GD2")]
a = "    Sig = SIG_A0[foot] * (vlast / math.sqrt(2) / SREF) ** q\n"; assert body.count(a) == 1; body = body.replace(a, "")
a = "M200 = 10 ** lM\n"; assert body.count(a) == 1; body = body.replace(a, "M200 = 10 ** lM\n    Sig = SIGFN(lM, foot, vlast, q)\n")
a = "Sig_ratio=Sig / SIG_A0[foot]"; assert body.count(a) == 1
g = {"__file__": P, "__name__": "gd3_ro", "MODE": {}, "np": None}; sys.argv = [P]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head, P, "exec"), g)
    g["SIGFN"] = lambda lM, foot, vlast, q: g["SIG_A0"][foot] * (vlast / math.sqrt(2) / g["SREF"]) ** q if g["MODE"]["m"] == "os1" else L.S_nat(10 ** lM, g["MODE"]["t"]) * 1e6
    exec(compile(body, P, "exec"), g)
J = json.load(open(os.path.join(REB, "GD3_smooth_core_mw", "gd3_smooth_core_mw_results.json")))
grade, CELLS, classify, BGS, SM, MCM = g["grade"], g["CELLS"], g["classify"], g["BGS"], g["B_smooth"], g["MCM"]
g["MODE"].update(m="os1", t="A_c2b_refit"); qs = J["stageS"]["canonical"]["q_fS"]
c0 = classify([grade(c["bar"], "canonical", 172.98, BGS["A_c2b_refit"], qs, SM) for c in CELLS]); r0 = J["stageM"]["graded"]["canonical|PRIMARY|A_c2b_refit"]
k2 = c0["cls"] == r0["cls"] and abs(c0["best"]["D"] - r0["best"]["D"]) < 1e-9; print("K2 OS1 + q_fS reproduces GD3:", c0["cls"], c0["best"]["D"], "PASS" if k2 else "FAIL")
OUT = dict(K2=k2, rows={}); g["MODE"]["m"] = "native"
for t in BGS:
    g["MODE"]["t"] = t; rows = [grade(c["bar"], "canonical", 0, BGS[t], 0, SM) for c in CELLS]; c = classify(rows)
    c["counts"] = {l: sum(r[l] for r in rows) for l in ("L1", "L2a", "L2b", "L3")}; c["Sig_range"] = [min(r["Sig_ratio"] for r in rows) * g["SIG_A0"]["canonical"] / 1e6, max(r["Sig_ratio"] for r in rows) * g["SIG_A0"]["canonical"] / 1e6]
    c["lgM200_range"] = [min(r["lgM200"] for r in rows), max(r["lgM200"] for r in rows)]; m = grade(MCM, "canonical", 0, BGS[t], 0, SM); c["mcmillan"] = {k: m[k] for k in ("vc_R0", "K_R0", "chi2_Kz", "chi2_Ou", "lgM200", "r0", "L1", "L2a", "L2b", "L3")}
    OUT["rows"][t] = c; print(t, c["cls"], c["counts"], "all4", c["n_all"], c["passing_Rd"], "best", c["best"], "inprior", c["best_in_prior"], "S", c["Sig_range"], "McM", c["mcmillan"])
OUT["eilers"] = [g["vE"], g["eE"]]; print("Eilers", g["vE"], g["eE"])
json.dump(OUT, open(os.path.join(HERE, "rg1_p2_mw" + ("_MUTATE" if L.MUT != 1 else "") + ".json"), "w"), indent=1, default=float); sys.exit(0 if k2 else 1)
