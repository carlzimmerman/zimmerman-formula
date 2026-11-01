#!/usr/bin/env python3
"""SP3 post-result, no verdict: stress on the weighing win, and UR3's c 12.95 against the definition of c. kappa = 1/2 FITTED, unused; not theory closed."""
import re, runpy, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); s = open(os.path.join(HERE, "sp3_weigh.py")).read(); s = s[:s.index('R = {}; P("SP3 weighing')].replace("os.path.abspath(__file__)", repr(os.path.join(HERE, "sp3_weigh.py"))); exec(s)
import json
U.T = NR2T; R = {}
def Mc2(rg, Mbg, M, R_, S_, r0, mode, C={}):
    if S["shape"] == "nfwc":
        c = S["c"]; mu = lambda x: np.log1p(x) - x / (1 + x); M0 = M * mu(rg / (R_ / c)) / mu(c)
        if S["mode"] == "off": return M0
        Mf = U.contract(rg, Mbg, M0, float(Mbg[-1] / M0[-1]))[0]; return M0 + (FQ if S["mode"] == "fq" else 1.0) * (Mf - M0)
    return Mc(rg, Mbg * S.get("mb", 1.0), M, R_, S_, r0, mode)
DN["Mc"] = Mc2; MN["Mc"] = Mc2
def halo2(lMb, t, d=0.0):
    if S["shape"] == "nfwc": lM = line(lMb, t); M = 10 ** lM; return M, (3 * M / (4 * math.pi * 200 * rcof(t))) ** (1 / 3), 1.0, 1.0
    return halo(lMb, t, d)
DN["halo"] = halo2; MN["halo"] = halo2
def w(**kw):
    S.pop("mb", None); S.update(dict(line="EM1", shape="hand", map="tot", mode="off", mh=1.0)); S.update(kw); a = DN["run"](S["mode"]); rows = [MN["g2"](c["bar"], TAG, S["mode"]) for c in MN["CELLS"]]; c = MN["classify"](rows); ip = [(MN["CELLS"][i], r) for i, r in enumerate(rows) if MN["CELLS"][i]["tag_Rd_IN"] and MN["CELLS"][i]["tag_Mstar_IN"] and all(r[l] for l in ("L1", "L2a", "L2b", "L3"))]; return dict(r=a["r"], Y=a["Y"], n=a["n"], cls=c["cls"], n_all=c["n_all"], inprior=len(ip), ex=[dict(Rd=a_["R_d"], Mstar=a_["Mstar"], Vc=b_["vc_R0"], Kz=b_["K_R0"]) for a_, b_ in ip[:3]])
def show(l, **kw): a = w(**kw); R[l] = a; P(f"{l:42s} r {a['r']:.3f} Y_K {a['Y']:.3f} n {a['n']} | {a['cls']} all4 {a['n_all']} in-prior {a['inprior']} {a['ex'][:1]}")
P("c: EM1 line, NFW on R200. LC1's c_nfw 12.95 is over r_vir; ZN1 reports c200 5.94, c_nfw 10.35 at 1e14, 6.47, 12.20 at 1e13; ZN2's table at 1e12 fits c200 7.8")
for c in (12.95, 7.8, 6.9):
    for mo in ("off", "fq"): show(f"NFW c200 {c} {mo}", shape="nfwc", c=c, mode=mo)
P("\nSeparate shape from f: hand core, f_Q 0.872"); show("hand EM1 fq", mode="fq")
P("\nStress: native + f_Q on EM1. LC1's f_Q 16-84 ish bracket [0.54, 1.07]; M_b in the response; maps")
for mn in ("tot", "fc1"):
    for fq_ in (0.54, 0.872, 1.07):
        FQ = fq_; show(f"native {mn} f_Q {fq_}", shape="native", map=mn, mode="fq")
    FQ = 0.872
    for mb in (0.7, 0.85, 1.15): show(f"native {mn} f_Q 0.872 M_b x {mb}", shape="native", map=mn, mode="fq", mb=mb)
json.dump(R, open(os.path.join(HERE, "sp3_post.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "sp3_post.out"), "w").write("\n".join(OUT) + "\n")
P("\nRefit rows, FITTED: EM1 + delta, f_Q 0.872")
for mn, dl in (("tot", -0.0938), ("fc1", -0.15)):
    S.pop("mb", None); S.update(dict(line="EM1", shape="native", map=mn, mode="fq", mh=10 ** dl, c=None)); a = DN["run"]("fq"); rows = [MN["g2"](c["bar"], TAG, "fq") for c in MN["CELLS"]]; c = MN["classify"](rows); R[f"refit {mn}"] = dict(r=a["r"], Y=a["Y"], n=a["n"], cls=c["cls"], n_all=c["n_all"]); P(f"native {mn} delta {dl}: r {a['r']:.3f} Y_K {a['Y']:.3f} n {a['n']} | {c['cls']} all4 {c['n_all']}")
json.dump(R, open(os.path.join(HERE, "sp3_post.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "sp3_post.out"), "w").write("\n".join(OUT) + "\n")
