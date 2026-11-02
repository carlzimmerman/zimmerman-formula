"""Step 1: fit k on X-COP positions 0,2,4,6; grade; readings R2-R4; checks K1-K4."""
import sys, json, time, os, re
import numpy as np
import cu1_core as c
out_name = sys.argv[1] if len(sys.argv) > 1 else "cu1_grade.json"
xc = c.XC(); sh = c.Shear(); out = {}
# K1
man = {}
for line in open(os.path.join(c.INP, "MANIFEST.txt")):
    p = line.rstrip("\n").split("\t")
    if len(p) >= 3:
        man[p[0]] = p[2]
chk = ["clusters/x7_measure_percluster.npz", "clusters/x2_catalogue_columns.npz", "clusters/erass1_kt.csv", "clusters/x7_outer_mgas_cal.json", "clusters/efe_table_canonical.npz", "clusters/efe_table_alt.npz", "scalars.json"]
xf = [os.path.join("xcop", n, n + s + ".fits") for n in xc.names for s in ("_hydro_mass", "_fgas_profile", "_mstar")]
bad = [f for f in chk + xf if man.get(f) != c.sha(os.path.join(c.INP, f))]
out["K1"] = dict(checked=len(chk + xf), bad=bad, N=sh.N, nI=int(sh.I.size), rows=int(xc.r.size), PASS=(not bad) and sh.N == 326 and sh.I.size == 106 and xc.r.size == 35)
# K2: isothermal sphere, M = A r: rho = A/(4 pi r^2), Sigma = A/(4 R), DeltaSigma = A/(4R) too
Am = 1e15 * c.MS / (1.0 * c.MPC)
P, Sb, _ = c.project(Am * c.RM, 0.0)
ana = Am / (4 * c.RC * c.MPC) / c.KG_PC2
out["K2"] = dict(maxrel=float(np.abs(P / ana - 1).max()), PASS=bool(np.abs(P / ana - 1).max() < 0.01))
# K3
v0, _ = sh.vector(10, "h0672", sh.msrc("canonical", 10, "h0672", 0.0))
P1, S1, _ = c.project(sh.msrc("canonical", 10, "h0672", 0.0), 0.3)
P2, S2, _ = c.project(2 * sh.msrc("canonical", 10, "h0672", 0.0), 0.3)
out["K3"] = dict(max_rel_double=float(np.abs(P2 / P1 / 2 - 1).max()), PASS=bool(np.abs(P2 / P1 / 2 - 1).max() < 1e-9))
wt = np.zeros(7); wt[[0, 2, 4, 6]] = 1
fit4 = [xc.names[i] for i in (0, 2, 4, 6)]; hold = [1, 3, 5]
out["fit_clusters"] = fit4; out["hold_clusters"] = [xc.names[i] for i in hold]
def cell(foot, k, uncapped=False):
    ce = {"k": k}
    worst = 0
    for hk in c.HS:
        res, nb, ncl = sh.grade(foot, hk, k, uncapped)
        chi, dof, p = sh.joint(foot, hk, res)
        ce[hk] = dict(Z={q: res[q]["Z"] for q in sh.KEYS}, pred={q: res[q]["pred"] for q in sh.KEYS}, chi2=chi, dof=dof, p=p, nonpos_cells=nb, nonpos_clusters=ncl)
    ce["fails"] = [q for q in sh.KEYS if max(abs(ce[hk]["Z"][q]) for hk in c.HS) > 2]
    ce["npass"] = 15 - len(ce["fails"])
    ce["joint_worse_p"] = min(ce[hk]["p"] for hk in c.HS)
    return ce
for foot in ("canonical", "alt"):
    k = xc.fit(foot, wt)
    k2 = xc.fit_mean0(foot, wt); k3 = xc.fit_linear(foot, wt)
    ce = cell(foot, k)
    ce["xcop"] = {"all7": xc.stat(foot, k), "fit4": xc.stat(foot, k, [0, 2, 4, 6]), "hold3": xc.stat(foot, k, hold)}
    ce["xcop_per_cluster"] = {xc.names[i]: xc.stat(foot, k, [i]) for i in range(7)}
    ce["R2_mean0"] = dict(k=k2, **{kk: v for kk, v in cell(foot, k2).items() if kk in ("fails", "npass", "joint_worse_p")}, xcop=xc.stat(foot, k2))
    ce["R3_linear"] = dict(k=k3, **{kk: v for kk, v in cell(foot, k3).items() if kk in ("fails", "npass", "joint_worse_p")}, xcop=xc.stat(foot, k3))
    u = cell(foot, k, uncapped=True)
    ce["R4_uncapped"] = {kk: u[kk] for kk in ("fails", "npass", "joint_worse_p")}
    ce["R4_uncapped"]["M3"] = u["h0672"]["Z"]["G-OUT-M3"]; ce["R4_uncapped"]["OUTall"] = u["h0672"]["Z"]["G-OUT-all"]
    if foot == "canonical":
        res = {q: {"Z": ce["h0672"]["Z"][q]} for q in sh.KEYS}
        chiI = sh.joint(foot, "h0672", res, identity=True)[0]
        out["K4"] = dict(d=abs(chiI - sum(v["Z"]**2 for v in res.values())), PASS=abs(chiI - sum(v["Z"]**2 for v in res.values())) < 1e-9)
    out[foot] = ce
    print(foot, "k %.3f (R2 %.3f R3 %.3f)" % (k, k2, k3), "npass", ce["npass"], "fails", ce["fails"], "worse p %.3f" % ce["joint_worse_p"])
    print("  X all7 %+.4f %.4f; fit4 %+.4f %.4f; hold3 %+.4f %.4f" % (ce["xcop"]["all7"] + ce["xcop"]["fit4"] + ce["xcop"]["hold3"]))
    for hk in c.HS:
        print(" ", hk, "chi2 %.2f dof %d p %.3f nonpos cells %d clusters %d" % (ce[hk]["chi2"], ce[hk]["dof"], ce[hk]["p"], ce[hk]["nonpos_cells"], ce[hk]["nonpos_clusters"]))
        print("   ", " ".join("%s %+.2f" % (q[2:], ce[hk]["Z"][q]) for q in sh.KEYS))
    print("  R2", ce["R2_mean0"]["npass"], ce["R2_mean0"]["fails"], "R3", ce["R3_linear"]["npass"], ce["R3_linear"]["fails"], "R4", ce["R4_uncapped"]["npass"], ce["R4_uncapped"]["fails"])
print({q: out[q]["PASS"] for q in ("K1", "K2", "K3", "K4")}, out["K1"]["bad"], out["K2"]["maxrel"], out["K3"]["max_rel_double"])
json.dump(out, open(out_name, "w"), indent=1, sort_keys=True)
