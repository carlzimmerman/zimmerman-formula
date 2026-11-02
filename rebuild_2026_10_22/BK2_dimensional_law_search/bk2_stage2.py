#!/usr/bin/env python3
"""BK2 cheap gates G4-G7, G9, G10, G12 on every train pass (LINE or ERR) and the top 25 near misses, both readings, Z per gate. python3 bk2_stage2.py FOOT MODE LEVEL. kappa = 1/2 FITTED; not theory closed."""
import json, sys
from bk2_lib import *
import bk2_read as Rd, bk2_gates as Gg
from scipy.stats import chi2
foot, mode, lev = sys.argv[1:4]; J = json.load(open(os.path.join(HERE, f"bk2_train_{lev}_{foot}_{mode}.json"))); Gt = Rd.Gates(foot, mode); a0 = Gt.a0
rows = {}; 
for r in J["train_pass"]: rows.setdefault(r["F"], r)
for r in J["byZ"][:25] + J["byLine"][:25]: rows.setdefault(r["F"], r)
neff = max(J["tally"].get("newton", 1), 1); out = []
print(f"{foot} {mode} {lev}: {len(rows)} formulas; train pass {J['n_train_pass']}; tally {J['tally']}; counts {J['counts']}", flush=True)
for n, (f, r) in enumerate(sorted(rows.items(), key=lambda t: t[1]["Z"])):
    if n >= 3000: print("capped at 3000 by Z", flush=True); break
    c = Gt.full_cheap(f); S = Gg.s_line(f, a0, 0); SA = Gg.s_line(f, a0); DM = Gg.diskmass(f, a0)
    gr = lambda g: dict(line=bool(g and g["line"]), err=bool(g and g["err"]))
    x3, s2, x5, s4, lt_, G7, dw = c["G3"], c["G2"], c["G5"], c["G4"], c["G6"], c["G7"], c["G9_10"]
    L = dict(G1b=c["solar"]["cass"], G2=bool(s2 and s2["line"]), G3=bool(x3 and x3["line"]), G4=bool(s4 and s4["line"] and S and S["line"] and S["tilt_ok"]), G5=bool(x5 and x5["line"]), G6=bool(lt_ and lt_["line"]), G7=bool(G7 and G7["PASS"]), G9=bool(dw and dw["line"]), G10=bool(dw and dw["ic_line"]), G12=bool(DM and DM["line"]))
    E = dict(G1b=c["solar"]["cass"], G2=bool(s2 and s2["err"]), G3=bool(x3 and x3["err"]), G4=bool(s4 and s4["err"] and S and S["ZU"] <= 2 and S["tilt_ok"]), G5=bool(x5 and x5["err"]), G6=bool(lt_ and lt_["err"]), G7=bool(G7 and G7["PASS"]), G9=bool(dw and dw["line"]), G10=bool(dw and dw["ic_line"]), G12=bool(DM and DM["err"]))
    Zs = dict(G1b=c["solar"]["Zc"], G2r=s2["Zr"] if s2 else None, G2u=s2["Zu"] if s2 else None, G3m=x3["Zm"] if x3 else None, G3s=x3["Zs"] if x3 else None, G4r=s4["Zr"] if s4 else None, G4u=s4["Zu"] if s4 else None, S_ZU=S["ZU"] if S else None, G5m=x5["Zm"] if x5 else None, G5s=x5["Zs"] if x5 else None, G6=lt_["Z"] if lt_ else None, G7=G7["Z"] if G7 else None, G12=DM["Z"] if DM else None, G10=dw["IC"]["Z"] if dw else None, **({f"G9_{k}_{c_.split()[0]}{c_.split()[1][:3]}": v["Z"] for k in ("plain", "E2") for c_, v in dw[k].items()} if dw else {}))
    zt = [v for k, v in Zs.items() if k in ("G3m", "G2r", "G2u") and v is not None]; ch = sum(z * z for z in zt); pl = float(chi2.sf(ch, max(len(zt), 1))); pg = float(1 - (1 - pl) ** neff) if pl > 0 else 1.0
    out.append(dict(F=f, fit=r["fit"], line=L, err=E, n_line=sum(L.values()), n_err=sum(E.values()), Z=Zs, X_train=x3, S_train={k: s2[k] for k in ("rms", "rms_law", "med", "med_U")} if s2 else None, X_hold=x5, S_hold={k: s4[k] for k in ("rms", "rms_law", "med")} if s4 else None, S_line_even=S, S_line_all=SA, LT=lt_, groups=G7, IC=dw["IC"] if dw else None, DM=DM, p_local=pl, p_sidak=pg, train_rank_Z=r["Z"]))
    if n % 100 == 0: print(n, flush=True)
ct = {g: dict(line=sum(o["line"][g] for o in out), err=sum(o["err"][g] for o in out)) for g in ("G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G9", "G10", "G12")}; allL = [o for o in out if all(o["line"].values())]; allE = [o for o in out if all(o["err"].values())]; nc = [o for o in out if all(v for k, v in o["err"].items() if k != "G1b")]
print("per gate among these:", ct); print(f"all cheap LINE {len(allL)}, all cheap ERR {len(allE)}, all but Cassini ERR {len(nc)}")
out.sort(key=lambda o: (-o["n_line"], -o["n_err"], o["train_rank_Z"]))
for o in out[:15]: print(f"LINE {o['n_line']}/10 ERR {o['n_err']}/10 fails-line {[g for g, v in o['line'].items() if not v]} fails-err {[g for g, v in o['err'].items() if not v]} p_sidak {o['p_sidak']:.2g} fit{o['fit']} {o['F'][:110]}")
json.dump(dict(counts=ct, all_line=len(allL), all_err=len(allE), all_but_cass=len(nc), rows=out[:400]), open(os.path.join(HERE, f"bk2_stage2_{lev}_{foot}_{mode}.json"), "w"), indent=0)
