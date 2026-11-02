"""Step 2: my numbers against UX3's README, line by line. Claim values typed from the README; nothing else of UX3 read."""
import json, sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import chi2 as chi2dist
import cu1_core as c
out_name = sys.argv[1] if len(sys.argv) > 1 else "cu1_compare.json"
xc = c.XC(); sh = c.Shear(); PI2 = np.pi**2
wt = np.zeros(7); wt[[0, 2, 4, 6]] = 1
K = {f: xc.fit(f, wt) for f in ("canonical", "alt")}
TOL = {"k": (.2, .5), "Z": (.05, .2), "X": (.002, .01), "p": (.02, .05), "chi2": (.5, 2.0)}
rows = []
def cmp(line, kind, claim, mine):
    if kind == "n" or kind == "set":
        lab = "MATCH" if claim == mine else "DISAGREE"
        rows.append(dict(line=line, claim=claim, mine=mine, label=lab)); return
    d = abs(mine - claim); a, b = TOL[kind]
    # the claim is printed rounded: allow half a last digit by rounding mine the same way is not used; d is direct
    lab = "MATCH" if d <= a else "CLOSE" if d <= b else "DISAGREE"
    rows.append(dict(line=line, claim=claim, mine=round(mine, 4), label=lab))
def cell(sx, foot, k, mult=None):
    r = {}
    for hk in c.HS:
        if mult is None:
            res, _, _ = sx.grade(foot, hk, k)
        else:
            V = np.zeros((sx.N, 8))
            for i in range(sx.N):
                V[i], _ = sx.vector(i, hk, mult * sx.msrc(foot, i, hk, 0.0))
            res = sx.grade_V(foot, hk, V)
        r[hk] = dict(Z={q: res[q]["Z"] for q in sx.KEYS}, j=sx.joint(foot, hk, res))
    r["fails"] = [q for q in sx.KEYS if max(abs(r[hk]["Z"][q]) for hk in c.HS) > 2]
    r["n"] = 15 - len(r["fails"])
    return r
def jack_p(sx, foot, hk, Z):
    B = sx._measure(foot, hk); sets = sx._sets(); rep = []
    for q in range(30):
        row = []
        keep = sx.PATCH != q
        for key in sx.KEYS:
            band, st, _ = sx._key_def(key); b = B[band]
            if st == "b":
                row.append(sx._wls(b["n"][sx.I], b["d"][sx.I], keep[sx.I].astype(float))[1])
            else:
                ids = sets[st]; w = keep[ids]
                row.append(b["raw"][ids][w].sum() / b["d"][ids][w].sum())
        rep.append(row)
    R = np.corrcoef(np.array(rep).T); lam, U = np.linalg.eigh(R); kp = lam >= 1e-3 * lam.max()
    z = np.array([Z[q] for q in sx.KEYS]); pz = U[:, kp].T @ z
    chi = float((pz**2 / lam[kp]).sum())
    return chi, int(kp.sum()), float(chi2dist.sf(chi, kp.sum()))
# law row
L = cell(sh, "canonical", 0.0)
cmp("law: keys", "n", 10, L["n"]); cmp("law: M3 h0.672", "Z", 4.76, L["h0672"]["Z"]["G-OUT-M3"]); cmp("law: chi2", "chi2", 65.0, L["h0672"]["j"][0]); cmp("law: p", "p", 3e-8, L["h0672"]["j"][2])
# table
T = [("canonical", PI2, "canonical pi^2", 12, ["G-MID-T3", "G-MID-b", "G-OUT-all"], 1.65, 1.36, 22.2, .10, .02, (.040, .078), (.065, .106)),
     ("canonical", K["canonical"], "canonical k fit", 14, ["G-OUT-all"], .58, .35, 16.1, .38, .20, (-.044, .081), (-.016, .089)),
     ("alt", PI2, "alt pi^2", 12, ["G-MID-T3", "G-MID-b", "G-OUT-all"], 1.19, .89, 23.3, .08, .02, (.056, .088), (.080, None)),
     ("alt", K["alt"], "alt k fit", 10, ["G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-Mall", "G-OUT-M2"], -.06, -.27, 18.5, .24, .14, (-.042, .079), (-.015, .087))]
cells = {}
for foot, k, nm, n, fails, m1, m2, chi, pb, pj, hold, al in T:
    r = cell(sh, foot, k); cells[nm] = r
    cmp(nm + ": keys", "n", n, r["n"]); cmp(nm + ": over 2", "set", sorted(fails), sorted(r["fails"]))
    cmp(nm + ": M3 h0.672", "Z", m1, r["h0672"]["Z"]["G-OUT-M3"]); cmp(nm + ": M3 h0.686", "Z", m2, r["h0686"]["Z"]["G-OUT-M3"])
    cmp(nm + ": chi2 h0.672", "chi2", chi, r["h0672"]["j"][0]); cmp(nm + ": p boot h0.672", "p", pb, r["h0672"]["j"][2])
    cmp(nm + ": p jack h0.672", "p", pj, jack_p(sh, foot, "h0672", r["h0672"]["Z"])[2])
    a, b = xc.stat(foot, k, [1, 3, 5]); cmp(nm + ": X unseen mean", "X", hold[0], a); cmp(nm + ": X unseen rms", "X", hold[1], b)
    a, b = xc.stat(foot, k); cmp(nm + ": X all7 mean", "X", al[0], a)
    if al[1] is not None:
        cmp(nm + ": X all7 rms", "X", al[1], b)
cmp("k fit canonical", "k", 13.29, K["canonical"]); cmp("k fit alt", "k", 14.25, K["alt"])
cmp("canonical k fit: OUT-all h0.672", "Z", -2.71, cells["canonical k fit"]["h0672"]["Z"]["G-OUT-all"]); cmp("canonical k fit: OUT-all h0.686", "Z", -2.77, cells["canonical k fit"]["h0686"]["Z"]["G-OUT-all"])
cmp("alt k fit: OUT-all h0.672", "Z", -3.23, cells["alt k fit"]["h0672"]["Z"]["G-OUT-all"])
cmp("canonical pi^2: MID-T3", "Z", 2.37, cells["canonical pi^2"]["h0672"]["Z"]["G-MID-T3"]); cmp("canonical pi^2: OUT-all", "Z", -2.27, cells["canonical pi^2"]["h0672"]["Z"]["G-OUT-all"])
cmp("canonical pi^2: p boot h0.686", "p", .045, cells["canonical pi^2"]["h0686"]["j"][2]); cmp("alt pi^2: p boot h0.686", "p", .033, cells["alt pi^2"]["h0686"]["j"][2])
# k scan
for fac, nc, na, m3, oa in ((.59, 12, 11, 2.93, None), (.7, 12, 11, 2.59, None), (1.3, 13, 11, .72, None), (1.7, 11, 10, None, -3.17)):
    a = cell(sh, "canonical", fac * PI2); b = cell(sh, "alt", fac * PI2)
    cmp("scan %.2f pi^2 canonical keys" % fac, "n", nc, a["n"]); cmp("scan %.2f pi^2 alt keys" % fac, "n", na, b["n"])
    if m3 is not None:
        cmp("scan %.2f pi^2 M3" % fac, "Z", m3, a["h0672"]["Z"]["G-OUT-M3"])
    if oa is not None:
        cmp("scan %.2f pi^2 OUT-all" % fac, "Z", oa, a["h0672"]["Z"]["G-OUT-all"])
# other f*, gas
sens = {}
for dex, fs in ((.005, .0615), (0.0, .034), (0.0, .0615)):
    sx = c.Shear(dex, fs)
    r = cell(sx, "canonical", K["canonical"]); ra = cell(sx, "alt", PI2)
    sens["g%s_f%s" % (dex, fs)] = dict(n=r["n"], fails=r["fails"], OUTall=[r[hk]["Z"]["G-OUT-all"] for hk in c.HS], alt_pi2_n=ra["n"], alt_pi2_fails=ra["fails"])
    cmp("canonical k fit, gas %s, f* %s: keys" % (dex, fs), "n", 14, r["n"])
    cmp("alt pi^2, gas %s, f* %s: keys" % (dex, fs), "n", 11 if fs == .0615 else 12, ra["n"])
# HSE bracket
hs = {}
for foot in K:
    d = xc.d(foot, K[foot]) - 0.12
    hs[foot] = dict(mean=float(d.mean()))
cmp("HSE -0.12 dex: X at k fit", "X", -.136, hs["canonical"]["mean"])
sav = xc.mh.copy(); xc.mh = xc.mh * 10**-0.12
kh = xc.fit("canonical", wt); xc.mh = sav
rh = cell(sh, "canonical", kh)
hs["k_refit_canonical"] = kh; hs["n"] = rh["n"]; hs["fails"] = rh["fails"]; hs["M3"] = rh["h0672"]["Z"]["G-OUT-M3"]; hs["worse_p"] = min(rh[q]["j"][2] for q in c.HS)
# multiplier
mr = cell(sh, "canonical", 0.0, mult=2.95)
cmp("multiplier H 2.95: keys", "n", 2, mr["n"]); cmp("multiplier H 2.95: M3", "Z", -12.4, mr["h0672"]["Z"]["G-OUT-M3"]); cmp("multiplier H 2.95: chi2", "chi2", 428, mr["h0672"]["j"][0])
# my frozen headline, worse h
head = {nm: dict(worse_h_p=min(cells[nm][q]["j"][2] for q in c.HS), h0686_p=cells[nm]["h0686"]["j"][2], h0686_chi2=cells[nm]["h0686"]["j"][0]) for nm in cells}
labs = [r["label"] for r in rows]
out = dict(rows=rows, counts={l: labs.count(l) for l in ("MATCH", "CLOSE", "DISAGREE")}, sens=sens, hse=hs, headline=head, multiplier=dict(n=mr["n"], M3=mr["h0672"]["Z"]["G-OUT-M3"], chi2=mr["h0672"]["j"][0]))
json.dump(out, open(out_name, "w"), indent=1, sort_keys=True)
for r in rows:
    print("%-9s %-46s claim %s mine %s" % (r["label"], r["line"], r["claim"], r["mine"]))
print(out["counts"]); print(json.dumps(sens)); print(json.dumps(hs)); print(json.dumps(head))
