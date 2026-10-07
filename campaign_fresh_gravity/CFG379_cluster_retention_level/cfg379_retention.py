"""CFG379: does the working model's supply limit set the retention levels? r = min(M_ph(<R_ap), S_catch) / (5.364 M_b(<R_ap)).
Criteria: FROZEN_CRITERIA.md (2858fb9a3). Run: python3 cfg379_retention.py ; CFG379_MUTATE=1 multiplies the supply by 10 (separate outputs, rc 1).
kappa = 1/2 is FITTED; both a0 footings, never pooled; no dark-matter particle (the cold fluid's amount 5.364 is free, not derived).
"""
import json, math, os, sys
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(CFG, ".."))
sys.path.insert(0, os.path.join(CFG, "CFG100_kids_mass_rederivation"))
import cfg100_lib as L  # noqa: E402  (read-only: nu_mono, r_ta_law, dta, constants)

MUTATE = os.environ.get("CFG379_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
SFAC = 10.0 if MUTATE else 1.0
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

COSMIC = 5.364
FC_M = COSMIC / (COSMIC + 1.0)                                 # Omega_c / Omega_m
G, A0, OM, H, RHOC0 = L.G_MPC, L.A0, L.OM, L.H, L.RHOC0          # Mpc (km/s)^2/Msun ; (km/s)^2/Mpc ; Msun/Mpc^3
FOOTS = ("canonical", "alt")
TARGET = {"clusters": 0.576, "groups": 0.60, "MW": 0.14}
def nu(y): return float(L.nu_mono(np.array([y]))[0])
def mph(Mb, R, a0): return (nu(G * Mb / R**2 / a0) - 1.0) * Mb   # monopole phantom target inside R (Mpc)

RC = 3.0 / H                                                   # comoving Mpc
S_RC = OM * FC_M * RHOC0 * (2 * math.pi) ** 1.5 * RC**3
S_RC_TH = OM * FC_M * RHOC0 * 4 * math.pi / 3 * RC**3
def supply(Mb, a0, catch):
    if catch == "RC":
        return S_RC * SFAC
    rta = L.r_ta_law(Mb, a0, 0.0)
    return FC_M * Mb * nu(G * Mb / rta**2 / a0) * SFAC

say("CFG379 supply-limited retention" + ("  (MUTATE: supply x10)" if MUTATE else ""))
say("=" * 88)
say(f"S_RC (Gaussian, R_c = 3 Mpc/h comoving) = {S_RC:.3e} Msun (top-hat variant {S_RC_TH:.3e}); Omega_c/Omega_m = {FC_M:.4f}; Delta_ta(0) = {L.dta(0):.3f}")

# ---------------- hosts
hosts = []                                                     # dict(cls, name, Mb [Msun], R [Mpc], Mtot or None)
xdir = os.path.join(REPO, "real_research", "data", "xcop")
r500j = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
for nm in sorted(os.listdir(xdir)):
    d = os.path.join(xdir, nm)
    if not os.path.isdir(d) or nm not in r500j:
        continue
    R500 = r500j[nm]["R500"] * 1000.0                          # kpc
    fg = fits.open(os.path.join(d, f"{nm}_fgas_profile.fits"))["FGAS"].data
    hm = fits.open(os.path.join(d, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data
    x, Mg = np.asarray(fg["RADIUS"], float), np.asarray(fg["MGAS"], float)
    Mgas = float(np.exp(np.interp(0.0, np.log(x), np.log(Mg))))
    msf = os.path.join(d, f"{nm}_mstar.fits")
    if os.path.exists(msf):
        ms = fits.open(msf)["MSTAR_SMOOTHED"].data
        Ms = float(np.exp(np.interp(math.log(R500), np.log(np.asarray(ms["RADIUS"], float)), np.log(np.asarray(ms["MSTAR"], float)))))
    else:
        Ms = 0.10 * Mgas
    Mtot = float(np.interp(R500, np.asarray(hm["RADIUS"], float), np.asarray(hm["M_FORW"], float)))
    hosts.append(dict(cls="clusters", name=nm, Mb=Mgas + Ms, R=R500 / 1000.0, Mtot=Mtot, star_measured=os.path.exists(msf)))

sys.path.insert(0, CFG)
import CFG7_common as C7  # noqa: E402
HUNT = os.path.join(REPO, "hunt_2026"); sys.path.insert(0, HUNT)
g7, _ = C7.C4.exec_slices(os.path.join(HUNT, "h7_groups_hot_gas.py"), [(None, 'P("="*116); P("ITEM 7A'),
                          ('lp = os.path.join(DATA, "lovisari2015_groups.tsv")', "R7B = {}")], name="h7_slices")
for g in g7["gr"]:
    hosts.append(dict(cls="groups", name=g["name"], Mb=g["Mg500"] + g7["mstar500"](g["M500"]), R=g["R500"] / 1000.0, Mtot=g["M500"]))
hosts.append(dict(cls="MW", name="MW-like", Mb=6.5e10, R=0.030, Mtot=None))
say(f"hosts: {sum(h['cls']=='clusters' for h in hosts)} X-COP clusters, {sum(h['cls']=='groups' for h in hosts)} Lovisari groups, 1 MW-like")

# ---------------- controls
say("\nControls")
fA = {f: {} for f in FOOTS}
for f in FOOTS:
    for h in hosts:
        if h["Mtot"] is not None:
            fA[f].setdefault(h["cls"], []).append((h["Mtot"] - h["Mb"] - mph(h["Mb"], h["R"], A0[f])) / (COSMIC * h["Mb"]))
mc, mg = float(np.median(fA["canonical"]["clusters"])), float(np.median(fA["canonical"]["groups"]))
check("C1 X-COP median f_A (canonical, R500) reproduces 0.576 within 0.10", abs(mc - 0.576) <= 0.10, f"{mc:.3f}")
check("C2 Lovisari median f_A (canonical, b = 0) reproduces cm02's 0.549 within 0.02", abs(mg - 0.549) <= 0.02, f"{mg:.3f}")
c3 = []
for f in FOOTS:
    for Mb in (6.5e10, 5e12, 1e14):
        rta = L.r_ta_law(Mb, A0[f], 0.0)
        c3.append(abs(Mb * nu(G * Mb / rta**2 / A0[f]) / (4 * math.pi / 3 * rta**3 * OM * RHOC0 * L.dta(0.0)) - 1))
check("C3 turnaround identity M_b nu(y_ta) = (4pi/3) r_ta^3 Omega_m rho_c Delta_ta to 1e-6", max(c3) < 1e-6, f"max dev {max(c3):.1e}")
Mt, Rt = 1e14, 1.0
c4a = min(mph(Mt, Rt, A0["canonical"]), 1e300) / (COSMIC * Mt) == mph(Mt, Rt, A0["canonical"]) / (COSMIC * Mt)
c4b = min(mph(Mt, Rt, A0["canonical"]), 0.0) == 0.0
check("C4 min-rule limits (S -> inf gives the target; S = 0 gives 0)", c4a and c4b, "exact")

# ---------------- predictions
say("\nPer host (canonical | alt): r_ph = M_ph/(5.364 M_b); s_TA, s_RC = S/(5.364 M_b); f_A measured (beyond the law); r_tot = (M_tot - M_b)/(5.364 M_b)")
rows = []
for h in hosts:
    row = dict(cls=h["cls"], name=h["name"], Mb=h["Mb"], R_Mpc=h["R"])
    for f in FOOTS:
        a0 = A0[f]; den = COSMIC * h["Mb"]; M_ph = mph(h["Mb"], h["R"], a0)
        row[f] = dict(y=G * h["Mb"] / h["R"]**2 / a0, r_ph=M_ph / den)
        for c in ("TA", "RC"):
            S = supply(h["Mb"], a0, c)
            row[f][c] = dict(s=S / den, r=min(M_ph, S) / den, bind="TARGET" if M_ph < S else "SUPPLY")
        if h["Mtot"] is not None:
            row[f]["f_A"] = (h["Mtot"] - h["Mb"] - M_ph) / den
            row[f]["r_tot"] = (h["Mtot"] - h["Mb"]) / den
    rows.append(row)
    c, a = row["canonical"], row["alt"]
    fa = f"f_A {c['f_A']:+.3f}|{a['f_A']:+.3f}  r_tot {c['r_tot']:.3f}" if "f_A" in c else "f_A (0.14 ledger)"
    say(f"  {h['cls']:8s} {h['name']:14s} Mb {h['Mb']:.2e} R {h['R']*1000:6.0f} kpc y {c['y']:.3f}  r_ph {c['r_ph']:.3f}|{a['r_ph']:.3f}  "
        f"s_TA {c['TA']['s']:6.2f}  s_RC {c['RC']['s']:7.3f}  r_TA {c['TA']['r']:.3f}  r_RC {c['RC']['r']:.3f}|{a['RC']['r']:.3f}  {fa}")

say("\nClass medians vs measured levels (pass: |pred - level| <= 0.10, or inside the measured f_A 16-84% range)")
res = {}
for c in ("TA", "RC"):
    res[c] = {}
    for f in FOOTS:
        cls_out, npass = {}, 0
        for k in ("clusters", "groups", "MW"):
            sub = [r for r in rows if r["cls"] == k]
            pred = float(np.median([r[f][c]["r"] for r in sub]))
            nbind = sum(r[f][c]["bind"] == "SUPPLY" for r in sub)
            ok = abs(pred - TARGET[k]) <= 0.10
            rng = None
            if k != "MW":
                lo, hi = np.percentile(fA[f][k], [16, 84]); rng = [float(lo), float(hi)]
                ok = ok or (lo <= pred <= hi)
            npass += ok
            cls_out[k] = dict(pred=pred, target=TARGET[k], f_A_16_84=rng, supply_binds=f"{nbind}/{len(sub)}", passes=bool(ok))
            say(f"  {c} {f:9s} {k:8s} pred {pred:.3f} vs {TARGET[k]:.3f}" + (f" (f_A 16-84 {rng[0]:.2f}-{rng[1]:.2f})" if rng else "")
                + f"  supply binds {nbind}/{len(sub)}  -> {'PASS' if ok else 'fail'}")
        res[c][f] = dict(classes=cls_out, npass=int(npass))
    say(f"  {c}: passes canonical {res[c]['canonical']['npass']}/3, alt {res[c]['alt']['npass']}/3")

def catch_grade(c):
    a, b = res[c]["canonical"]["npass"], res[c]["alt"]["npass"]
    if a == 3 and b == 3: return 3
    if min(a, b) >= 2 or max(a, b) == 3: return 2
    return 0
grades = {c: catch_grade(c) for c in ("TA", "RC")}
best = max(grades.values())
V = {3: "PREDICTS", 2: "PARTIAL", 0: "FAILS"}[best]
lab = [c for c in grades if grades[c] == best]
say(f"\nVERDICT: {V}  (catchment grades {grades}; best under {lab})")

say("\nBookkeeping check B (reported): the cap M_tot - M_b <= min(M_ph, S) in the model's own accounting")
B = {}
for f in FOOTS:
    for k in ("clusters", "groups"):
        sub = [r for r in rows if r["cls"] == k]
        viol = sum(r[f]["f_A"] > 0 for r in sub)
        rt = float(np.median([r[f]["r_tot"] for r in sub]))
        B[f"{f}|{k}"] = dict(cap_violated=f"{viol}/{len(sub)}", median_r_tot=rt)
        say(f"  {f:9s} {k:8s}: cap violated (f_A > 0) in {viol}/{len(sub)}; measured total cold content r_tot median {rt:.3f} vs r_ph median {np.median([r[f]['r_ph'] for r in sub]):.3f}")

say("\nSensitivities (reported)")
sens = {}
for Mb in (5e10, 8e10):
    for f in FOOTS:
        sens[f"MW_Mb{Mb:.0e}_{f}"] = mph(Mb, 0.030, A0[f]) / (COSMIC * Mb)
say("  MW r_ph at M_b 5e10 / 8e10: " + ", ".join(f"{k} {v:.3f}" for k, v in sens.items()))
thr = []
for k in ("clusters", "groups"):
    sub = [r for r in rows if r["cls"] == k]
    thr.append(f"{k} RC top-hat supply binds {sum(S_RC_TH*SFAC < (r['canonical']['r_ph']*COSMIC*r['Mb']) for r in sub)}/{len(sub)}, median r "
               f"{np.median([min(r['canonical']['r_ph']*COSMIC*r['Mb'], S_RC_TH*SFAC)/(COSMIC*r['Mb']) for r in sub]):.3f}")
say("  " + "; ".join(thr) + " (canonical)")
say("  mass sweep (aperture = MOND radius sqrt(G M_b/a0), canonical): r_ph is the same at every mass there (y = 1):"
    f" {(nu(1.0)-1)/COSMIC:.3f}; s_TA / s_RC:")
sweep = {}
for lm in range(10, 16):
    Mb = 10.0**lm
    sTA = supply(Mb, A0["canonical"], "TA") / (COSMIC * Mb); sRC = supply(Mb, A0["canonical"], "RC") / (COSMIC * Mb)
    sweep[lm] = dict(r_ph=(nu(1.0) - 1) / COSMIC, s_TA=sTA, s_RC=sRC)
    say(f"    M_b 1e{lm}: s_TA {sTA:8.2f}  s_RC {sRC:10.3f}  r_TA {min((nu(1.0)-1)/COSMIC, sTA):.3f}  r_RC {min((nu(1.0)-1)/COSMIC, sRC):.3f}")

flip = None
if MUTATE and os.path.exists(os.path.join(HERE, "cfg379_results.json")):
    m0 = json.load(open(os.path.join(HERE, "cfg379_results.json")))
    cnt = any(m0["results"][c][f]["npass"] != res[c][f]["npass"] for c in ("TA", "RC") for f in FOOTS)
    bnd = any(m0["results"][c][f]["classes"]["clusters"]["supply_binds"] != res[c][f]["classes"]["clusters"]["supply_binds"] for c in ("TA", "RC") for f in FOOTS)
    flip = dict(pass_count_changed=cnt, cluster_binding_changed=bnd, headline_main=m0["verdict"], headline_mutate=V)
    say(f"\nMUTATE vs main: pass count changed {cnt}; cluster binding changed {bnd}; headline {m0['verdict']} -> {V}"
        f" -> declared flip {'MET' if (cnt or bnd) else 'NOT MET'}" + ("" if m0["verdict"] != V else " (headline unchanged, disclosed)"))
check("T-MUT main-run marker (MUTATE exits rc 1)", not MUTATE, V)
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG379", "mutate": MUTATE, "supply_factor": SFAC, "verdict": V, "grades": grades, "results": res, "bookkeeping_B": B,
           "S_RC": S_RC, "S_RC_tophat": S_RC_TH, "rows": rows, "sensitivity": sens, "sweep": sweep, "checks": checks, "mutate_flip": flip},
          open(os.path.join(HERE, f"cfg379_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg379{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
