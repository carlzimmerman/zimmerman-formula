"""Post-result: k = all-7 fit graded directly; one try at the joint chi^2 offset (R from n, not raw)."""
import json, numpy as np
import cu1_core as c
xc = c.XC(); sh = c.Shear(); out = {}
for foot in c.A0:
    k = xc.fit(foot, np.ones(7)); fs = {}
    for hk in c.HS:
        res, _, _ = sh.grade(foot, hk, k); fs[hk] = dict(Z={q: res[q]["Z"] for q in sh.KEYS}, j=sh.joint(foot, hk, res))
    fails = [q for q in sh.KEYS if max(abs(fs[h]["Z"][q]) for h in c.HS) > 2]
    m, r = xc.stat(foot, k)
    out[foot] = dict(k_all7=k, n=15 - len(fails), fails=fails, X=[m, r], M3=fs["h0672"]["Z"]["G-OUT-M3"], OUTall=fs["h0672"]["Z"]["G-OUT-all"], MIDT3=[fs[h]["Z"]["G-MID-T3"] for h in c.HS], worse_p=min(fs[h]["j"][2] for h in c.HS))
# R variant: replace raw by leak-subtracted n in the ratio replicates
g = json.load(open("cu1_grade.json")); G0 = json.load(open("cu1_gate.json")); hk = "h0672"
R0 = sh.corr("canonical", hk)
B = sh._measure("canonical", hk); sav = {b: B[b]["raw"] for b in B}
sh.meas.pop(("canonical", hk, "R"))
for b in B:
    B[b]["raw"] = B[b]["n"]
R1 = sh.corr("canonical", hk)
for b in B:
    B[b]["raw"] = sav[b]
def chi(R, z):
    lam, U = np.linalg.eigh(R); kp = lam >= 1e-3 * lam.max(); p = U[:, kp].T @ z
    return float((p**2 / lam[kp]).sum())
zk = np.array([g["canonical"][hk]["Z"][q] for q in sh.KEYS]); z0 = np.array([G0["canonical"][hk]["keys"][q]["Z"] for q in sh.KEYS])
out["chi_R_raw"] = dict(kfit=chi(R0, zk), law=chi(R0, z0)); out["chi_R_n"] = dict(kfit=chi(R1, zk), law=chi(R1, z0)); out["record"] = dict(kfit=16.1, law=65.0)
json.dump(out, open("cu1_post.json", "w"), indent=1, sort_keys=True); print(json.dumps(out, indent=0))
