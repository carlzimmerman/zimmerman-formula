"""Post-freeze diagnosis of K2, K3 failures and of the joint's R; frozen checks stay failed as reported."""
import numpy as np, json
import cu1_core as c
sh = c.Shear(); out = {}
Am = 1e15 * c.MS / c.MPC
P, Sb, _ = c.project(Am * c.RM, 0.0)
# truncated isothermal at Rmax: Sigma(R) = A/(2 pi R) arctan(sqrt(Rmax^2-R^2)/R); DeltaSigma by the same quadrature on a fine grid
Rmax = c.RG[-1] * c.MPC
def SigT(R):
    return Am / (2 * np.pi * R) * np.arctan(np.sqrt(Rmax**2 - R**2) / R)
out["K2_trunc"] = []
for Rc in c.RC:
    R = Rc * c.MPC; g = np.logspace(-8, 0, 200001) * R
    mean = (np.trapz(SigT(g) * g, g) + 0.5 * SigT(g[0]) * g[0]**2) * 2 / R**2
    out["K2_trunc"].append(float(P[list(c.RC).index(Rc)] / ((mean - SigT(R)) / c.KG_PC2) - 1))
out["K2_untrunc"] = (P / (Am / (4 * c.RC * c.MPC) / c.KG_PC2) - 1).tolist()
M = sh.msrc("canonical", 10, "h0672", 0.0)
P1, _, _ = c.project(M, 0.3); P2, _, _ = c.project(2 * M, 0.3)
out["K3_rel_off0.3"] = (P2 / P1 / 2 - 1).tolist(); out["K3_P_off0.3"] = P1.tolist()
P1, _, _ = c.project(M, 0.0); P2, _, _ = c.project(2 * M, 0.0)
out["K3_rel_off0"] = float(np.abs(P2 / P1 / 2 - 1).max())
own = sh.chain["h0672"][10]["off"]
P1, _, _ = c.project(M, own); P2, _, _ = c.project(2 * M, own)
out["own_off_mpc"] = own; out["K3_rel_own"] = float(np.abs(P2 / P1 / 2 - 1).max())
# floor use in graded prediction, canonical h0672, k fitted
g = json.load(open("cu1_grade.json")); k = g["canonical"]["k"]
nf = 0; offs = []
for i in range(sh.N):
    P, _, _ = c.project(sh.msrc("canonical", i, "h0672", k), sh.chain["h0672"][i]["off"])
    if (P < 1e-20).any():
        nf += int((P < 1e-20).sum())
out["floored_P_bins_all_clusters"] = nf
# R seed sensitivity at k = 0 and fitted k
G0 = json.load(open("cu1_gate.json"))
Z0 = np.array([G0["canonical"]["h0672"]["keys"][q]["Z"] for q in sh.KEYS])
Zk = {hk: np.array([g["canonical"][hk]["Z"][q] for q in sh.KEYS]) for hk in c.HS}
rows = []
for sd in (20261102, 1, 2, 3, 4):
    sh.meas.pop(("canonical", "h0672", "R"), None); sh.meas.pop(("canonical", "h0686", "R"), None)
    r = {}
    for hk in c.HS:
        res = {q: {"Z": Zk[hk][j]} for j, q in enumerate(sh.KEYS)}
        sh.meas[("canonical", hk, "R")] = sh.corr("canonical", hk, seed=sd)
        r[hk] = sh.joint("canonical", hk, res)
    res0 = {q: {"Z": Z0[j]} for j, q in enumerate(sh.KEYS)}
    r["law_h0672"] = sh.joint("canonical", "h0672", res0)
    rows.append(dict(seed=sd, **r))
out["R_seed_sensitivity"] = rows
json.dump(out, open("cu1_diag.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=0)[:3000])
