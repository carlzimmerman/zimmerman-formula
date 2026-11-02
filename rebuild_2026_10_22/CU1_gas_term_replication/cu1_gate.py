"""Step 0: k = 0 must reproduce the law. --mutate sets nu to 1, separate outputs, must exit 1."""
import sys, json, time
import cu1_core as c
mut = "--mutate" in sys.argv
c.NU_MUTATE = mut
tag = "MUTATE" if mut else "gate"
t0 = time.time(); out = {}
xc = c.XC()
out["xcop_rows"] = int(xc.r.size); out["xcop_names"] = xc.names
sh = c.Shear()
out["nI"] = int(sh.I.size); out["N"] = sh.N
for foot in ("canonical", "alt"):
    m, r = xc.stat(foot, 0.0)
    cell = {"xcop_mean": m, "xcop_rms": r}
    for hk in c.HS:
        res, nb, ncl = sh.grade(foot, hk, 0.0)
        chi, dof, p = sh.joint(foot, hk, res)
        cell[hk] = {"keys": res, "chi2": chi, "dof": dof, "p": p, "nonpos": nb,
                    "sumZ2": sum(v["Z"]**2 for v in res.values()), "chiI": sh.joint(foot, hk, res, identity=True)[0]}
    fails = [k for k in sh.KEYS if max(abs(cell[hk]["keys"][k]["Z"]) for hk in c.HS) > 2]
    cell["fails"] = fails; cell["npass"] = 15 - len(fails)
    out[foot] = cell
can = out["canonical"]
gate = {"npass": can["npass"] == 10, "M3": abs(can["h0672"]["keys"]["G-OUT-M3"]["Z"] - 4.76) <= 0.02, "X": abs(can["xcop_mean"] - 0.467) <= 0.002}
out["gate"] = gate; out["PASS"] = all(gate.values())
json.dump(out, open("cu1_%s.json" % tag, "w"), indent=1, sort_keys=True)
for foot in ("canonical", "alt"):
    ce = out[foot]
    print(foot, "npass", ce["npass"], "fails", ce["fails"], "X %.4f %.4f" % (ce["xcop_mean"], ce["xcop_rms"]))
    for hk in c.HS:
        print(" ", hk, "chi2 %.2f dof %d p %.2e nonpos %d" % (ce[hk]["chi2"], ce[hk]["dof"], ce[hk]["p"], ce[hk]["nonpos"]))
        print("   ", " ".join("%s %+.2f" % (k[2:], ce[hk]["keys"][k]["Z"]) for k in sh.KEYS))
print("gate", gate, "PASS", out["PASS"], "t", round(time.time() - t0))
sys.exit(0 if out["PASS"] else 1)
