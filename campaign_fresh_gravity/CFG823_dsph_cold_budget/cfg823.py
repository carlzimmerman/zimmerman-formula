"""CFG823 -- placement-independent cold-energy budget for the 11 MW classical dSphs.  Criteria: FROZEN_CRITERIA.md (37fab0eee).
Inputs exactly CFG821/822; f_ret and r_ta read from CFG822's results.  Run: python3 cfg823.py  (CFG823_MUTATE=1: f_ret = 1).
kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG823_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
Gsi, Msun, KPC = 6.674e-11, 1.989e30, 3.0857e19; SUP = 5.364; A0 = 9.3603e-11
def fnum(x):
    try: return float(x)
    except: return None
D = []
for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv"))):
    MV, s_, es, rh = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("vlos_sigma_em")), fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    if MV is None or s_ is None or rh is None or MV > -7.7 or r["name"] in ("LMC", "SMC", "Sagittarius"): continue
    D.append(dict(name=r["name"], L=10 ** (0.4 * (4.83 - MV)), so=s_, eso=es or 0.1 * s_, rh=rh / 1000.0))
R22 = json.load(open(os.path.join(LANES, "CFG822_hex_dsph", "cfg822_results.json")))["rows"]
mreq = lambda s, r12: 3 * (s * 1e3) ** 2 * r12 * KPC / Gsi / Msun
def settled(Mb, r):
    rM = math.sqrt(Gsi * Mb * Msun / A0) / KPC; return 0.5 * Mb * (math.sqrt(1 + 4 * r * r / rM ** 2) - 1)
P(f"CFG823  cold-energy budget, 11 MW classical dSphs" + ("  [MUTATE f_ret = 1]" if MUT else ""))
RES = dict(lane="CFG823", mutate=MUT, rows={})
for ups in (2.0, 1.0, 4.0):
    qs, fails = [], []
    if ups == 2.0: P(f"\n  Upsilon = 2 (primary)\n  {'dSph':16s} {'M_b':>9s} {'M_req':>9s} {'N_in':>7s} {'ceil':>6s} {'q':>6s} {'q_lo':>6s} {'q_settled':>9s} {'r12/rta':>8s}")
    for g in D:
        Mb = ups * g["L"]; r12 = (4 / 3) * g["rh"]; row = R22[f"canonical|{g['name']}"]
        fret = 1.0 if MUT else row["fret"]; Stot = SUP * Mb / fret
        Mr = mreq(g["so"], r12); Mlo = mreq(max(g["so"] - 2 * g["eso"], 0.0), r12)
        Nin = (Mr - Mb / 2) / Mb; q = (Mr - Mb / 2) / Stot; qlo = (Mlo - Mb / 2) / Stot
        qs.append(q); fails += [g["name"]] if qlo > 1 else []
        qset = settled(Mb, r12) / Stot
        RES["rows"][f"{ups}|{g['name']}"] = dict(Mb=Mb, Mreq=Mr, N_in=Nin, ceiling=SUP / fret, q=q, q_2sig_low=qlo, q_settled=qset, r12_over_rta=r12 / row["rta_kpc"])
        if ups == 2.0:
            P(f"  {g['name']:16s} {Mb:9.2e} {Mr:9.2e} {Nin:7.1f} {SUP / fret:6.1f} {q:6.2f} {qlo:6.2f} {qset:9.3f} {r12 / row['rta_kpc']:8.4f}")
    med = float(np.median(qs))
    cls = "BUDGET FAILS" if fails else ("BUDGET TIGHT" if med > 0.3 else "BUDGET OK")
    RES[f"ups{ups:g}"] = dict(median_q=med, max_q=float(max(qs)), fails_2sig=fails, cls=cls)
    P(f"  [Upsilon {ups:g}] median q {med:.2f}  max q {max(qs):.2f}  q>1 at >2 sigma: {fails or 'none'}  -> {cls}")
g = [x for x in D if x["name"] == "Draco"][0]; r12 = (4 / 3) * g["rh"]
k1 = mreq(g["so"], r12); k1b = 3 * g["so"] ** 2 * r12 / 4.3009e-6
P(f"\n  K1 Draco M_req {k1:.6e} vs G=4.3009e-6 kpc (km/s)^2/Msun form {k1b:.6e} -> {'PASS' if abs(k1 / k1b - 1) < 1e-3 else 'CHECK'} (constant convention only)")
P(f"  median r1/2 / r_ta = {np.median([RES['rows'][f'2.0|{x}']['r12_over_rta'] for x in [d['name'] for d in D]]):.4f}")
RES["cls"] = RES["ups2"]["cls"]; P(f"\n  CLASS (Upsilon 2): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg823_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg823{sfx}.out"), "w").write("\n".join(OUT) + "\n")
