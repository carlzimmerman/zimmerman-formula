#!/usr/bin/env python3
"""CFG444 -- light end (2.01-4.35e-20 eV) of the wave-field window via holes with GRAVITY-class dynamical masses.
Frozen: FROZEN_CRITERIA.md (493ba7b2f). Executes CFG367's committed cfg367_superradiance.py byte-for-byte (sha256)
with __file__ pointed at runs/<tag>/ (CFG394's wrapper method). Inputs (data/): vdb16_t2.tsv, vdb16_t3.tsv
(van den Bosch 2016, VizieR J/ApJ/831/134), gravity_masses.csv, spins_window.csv, xray_lookup.csv (fetch_xray.py),
bat105_fluxes.txt, erass1_*.tsv; plus CFG394's spins_compiled_3e8_3e9.csv (route B spins).
CFG444_MUTATE=1: all spins 0 on the hypothetical list (separate outputs, _MUTATE suffix)."""
import os, csv, json, math, hashlib, contextlib, io, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
SRC = os.path.join(HERE, "..", "CFG367_superradiance_window")
C394 = os.path.join(HERE, "..", "CFG394_bh_spins_light_end")
MUT = os.environ.get("CFG444_MUTATE", "0") == "1"
SLUG = "cfg444_light_end_gravity" + ("_MUTATE" if MUT else "")
CODE_SHA = "d78a38121a865094d8d333108533bd67e378f6c7aabc0ad6edcf74ae8bb0237e"
CSV_SHA = "6b3b1c496c4194b7bbe453baf07ab87287c6499608b65b5c6dd5c91f5d41d963"
LIGHT = (2.012653280876046e-20, 4.3452552089909754e-20)
FIELDS = ["set", "name", "mass_1e6", "err_lo", "err_hi", "approx", "spin_lo", "spin_text"]
DYN = {"star", "stars", "gas", "CO", "maser", "GRAVITY BLR", "GRAVITY BLR (2018)", "GRAVITY+ BLR", "SARM", "SARM II"}
LEDD = 1.26e38; KBOL_BAT = 8.0; F_LIM_BAT = 1.0e-11; LAM_LLAGN = 1e-3; MPC = 3.0857e24
LOG, CH, OUT = [], [], {"lane": "CFG444", "frozen": "493ba7b2f", "mutate": MUT, "light_end": LIGHT}


def P(s=""):
    print(s); LOG.append(s)


def check(n, ok, v=""):
    CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")


code = open(os.path.join(SRC, "cfg367_superradiance.py"), "rb").read()
h = hashlib.sha256(code).hexdigest()
check("C0 CFG367 code sha256 identical", h == CODE_SHA, h[:16])
if h != CODE_SHA:
    raise SystemExit("code hash mismatch: stop (frozen rule)")


def run(tag, rows, mutate=False, csv_bytes=None):
    d = os.path.join(HERE, "runs", tag); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "bh_spins_reynolds2021.csv")
    if csv_bytes is not None:
        open(p, "wb").write(csv_bytes)
    else:
        with open(p, "w", newline="") as f:
            w = csv.DictWriter(f, FIELDS); w.writeheader(); [w.writerow(r) for r in rows]
    os.environ["CFG367_MUTATE"] = "1" if mutate else "0"
    ns = {"__file__": os.path.join(d, "cfg367_superradiance.py"), "__name__": "__main__"}
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            exec(compile(code, ns["__file__"], "exec"), ns); rc = 0
        except SystemExit as e:
            rc = e.code
    os.environ["CFG367_MUTATE"] = "0"
    res = json.load(open(os.path.join(d, "cfg367_superradiance" + ("_MUTATE" if mutate else "") + "_results.json")))
    check(f"C2 [{tag}{' MUTATE' if mutate else ''}] CFG367 internal checks pass (exit {rc})", rc == 0)
    return res, ns


def overlap(ivs, lo, hi):
    return [(max(a, lo), min(b, hi)) for a, b in ivs if b >= lo and a <= hi]


def surv(ivs, lo, hi):
    out, cur = [], lo
    for a, b in sorted(overlap(ivs, lo, hi)):
        if a > cur: out.append((cur, a))
        cur = max(cur, b)
    if cur < hi: out.append((cur, hi))
    return out


fmt = lambda iv: "; ".join(f"[{a:.2e}, {b:.2e}]" for a, b in iv) or "none"

# ---------------- C1 control: CFG367 from its own CSV
cb = open(os.path.join(SRC, "bh_spins_reynolds2021.csv"), "rb").read()
check("C1a CFG367 CSV sha256 identical", hashlib.sha256(cb).hexdigest() == CSV_SHA)
ref = json.load(open(os.path.join(SRC, "cfg367_superradiance_results.json")))
ctl, NS = run("CONTROL_CFG367", None, csv_bytes=cb)
check("C1 control reproduces CFG367 committed intervals exactly", all(ctl[k] == ref[k] for k in ("smbh", "xrb", "primary", "primary+secondary", "per_object")))
c394 = json.load(open(os.path.join(C394, "cfg394_light_end_results.json")))
check("C1b control also equals CFG394's committed control run", ctl == json.load(open(os.path.join(C394, "runs", "CONTROL_CFG367", "cfg367_superradiance_results.json"))))

# ---------------- compilation
def vdb(fn):
    L = [l for l in open(os.path.join(D, fn)) if not l.startswith("#") and l.strip()]
    hh = L[0].rstrip("\n").split("\t")
    return [dict(zip(hh, [x.strip() for x in l.rstrip("\n").split("\t")])) for l in L[3:]]


meas = []   # one row per mass measurement
for fn, tab in (("vdb16_t2.tsv", "vdB16 table2"), ("vdb16_t3.tsv", "vdB16 table3")):
    for r in vdb(fn):
        try: m = float(r["logBHMass"])
        except ValueError: continue
        up, dn = float(r["E_logBHMass"]), float(r["e_logBHMass"])
        meas.append(dict(name=r["Name"], logM=m, dex_hi=up, dex_lo=dn, method=r["Meth"], ref=f"{tab} refs {r['Refs']}",
                         dist=float(r["Dist"]) if r["Dist"] else None, ulim=(dn >= m - 1e-9), src=tab))
for r in csv.DictReader(open(os.path.join(D, "gravity_masses.csv"))):
    meas.append(dict(name=r["name"], logM=float(r["logM"]), dex_hi=float(r["dex_hi"]), dex_lo=float(r["dex_lo"]),
                     method=r["method"].split(" model")[0].split(" (GRAVITY")[0], ref=r["paper"], dist=None, ulim=False, src="gravity_masses.csv", z=float(r["z"])))
alias = {"PG1226+023": "3C273"}   # PG 1226+023 = 3C 273
for x in meas:
    x["name"] = alias.get(x["name"], x["name"])

objs = {}
for x in meas:
    objs.setdefault(x["name"], []).append(x)


def dex(x):
    return max(x["dex_hi"], x["dex_lo"])


def assess(name, ms):
    dyn = [x for x in ms if x["method"] in DYN and not x["ulim"]]
    best = min(dyn, key=dex) if dyn else min(ms, key=dex)
    disagree = []
    for a, b in itertools.combinations(dyn, 2):
        lo, hi = (a, b) if a["logM"] < b["logM"] else (b, a)
        if hi["logM"] - lo["logM"] > math.hypot(lo["dex_hi"], hi["dex_lo"]):
            disagree.append((lo["logM"], hi["logM"]))
    precise = bool(dyn) and dex(best) <= 0.15 and not disagree
    return best, precise, disagree


comp = {}
for n, ms in objs.items():
    best, precise, dis = assess(n, ms)
    M = 10**best["logM"]
    comp[n] = dict(name=n, M=M, logM=best["logM"], dex_hi=best["dex_hi"], dex_lo=best["dex_lo"], method=best["method"], ref=best["ref"],
                   dynamical=best["method"] in DYN and not best["ulim"], precise=precise, disagree=dis, n_mass=len(ms),
                   all_masses=[(x["logM"], x["dex_hi"], x["dex_lo"], x["method"], x["ref"]) for x in ms], dist=best.get("dist"), z=best.get("z"))
win = {n: c for n, c in comp.items() if 3e8 <= c["M"] <= 3e9}
P(f"\nCOMPILATION: {len(comp)} objects with masses; {len(win)} with 3e8 <= M <= 3e9 (S2); "
  f"{sum(c['dynamical'] for c in win.values())} dynamical; {sum(c['precise'] for c in win.values())} precise (R3)")
for n in ("3C273", "J0529-4351", "J0920+0657"):
    c = comp[n]; P(f"  {n}: masses {[(m[0], m[3]) for m in c['all_masses']]}; precise={c['precise']}; disagreements {c['disagree']}")
P("  GRAVITY/SARM objects outside 3e8-3e9 (dropped by S2): " + ", ".join(f"{n} logM {c['logM']:.2f}" for n, c in comp.items()
                                                                     if not (3e8 <= c["M"] <= 3e9) and any(m[4].startswith(("GRAVITY", "Abuter", "Li et")) for m in c["all_masses"])))

# ---------------- spins (S3, R1/R2)
def lower_edge(k, v, elo):
    v = float(v) if v not in ("", None) else None
    if k == "i90": return v - float(elo)
    if k == "i1s": return v - 1.645 * float(elo)
    if k == "ll": return v
    if k == "ul": return 0.0
    return None


spins = {}
for r in csv.DictReader(open(os.path.join(D, "spins_window.csv"))):
    spins.setdefault(r["name"], []).append(dict(ref=r["spin_ref"], method=r["spin_method"], kind=r["spin_kind"], used=r["used"] == "1",
                                                edge=lower_edge(r["spin_kind"], r["spin_val"], r["spin_elo"]) if r["used"] == "1" else None, note=r["note"]))
for r in csv.DictReader(open(os.path.join(C394, "spins_compiled_3e8_3e9.csv"))):
    spins.setdefault(r["name"].replace("-", "-"), []).append(dict(ref=r["spin_ref"], method=r["spin_model"], kind=r["spin_kind"], used=r["used"] == "1",
                                                                  edge=max(lower_edge(r["spin_kind"], r["spin_val"], r["spin_elo"]), 0.0) if r["used"] == "1" else None, note="CFG394 compiled row"))
for c in comp.values():
    ed = [s["edge"] for s in spins.get(c["name"], []) if s["used"] and s["edge"] is not None]
    c["spin_floor"] = min(ed) if ed else 0.0
    c["spin_records"] = [(s["ref"], s["method"], s["kind"], s["used"], s["edge"]) for s in spins.get(c["name"], [])]
    c["tier"] = ("A" if c["precise"] and c["spin_floor"] >= 0.5 else
                 "B" if c["dynamical"] and dex(c) <= 0.4 and c["spin_floor"] >= 0.5 else "none")
P("\nSPIN CROSS-MATCH (window objects with any spin record, any method, 2010-2026):")
for n, c in sorted(win.items(), key=lambda t: t[1]["M"]):
    if c["spin_records"]:
        P(f"  {n:11s} M={c['M']:.2e} ({c['method']}, precise={c['precise']}): " + "; ".join(f"{s[0]} [{s[1]}] {s[2]} edge={s[4]}" for s in c["spin_records"]) + f" -> R2 floor {c['spin_floor']:.3f}, TIER {c['tier']}")
nospin = [n for n, c in win.items() if not c["spin_records"]]
P(f"  no spin record found for {len(nospin)} window objects: {', '.join(sorted(nospin))}")
tierA = [c for c in win.values() if c["tier"] == "A"]; tierB = [c for c in win.values() if c["tier"] == "B"]
P(f"  TIER A: {[c['name'] for c in tierA] or 'none'}; TIER B: {[c['name'] for c in tierB] or 'none'}")


def row(c, a=None, err=None):
    M6 = c["M"] / 1e6
    if err is None:
        lo, hi = M6 * (1 - 10**-c["dex_lo"]), M6 * (10**c["dex_hi"] - 1)
    else:
        lo = hi = err * M6
    return dict(set="smbh", name=c["name"], mass_1e6=f"{M6:.6g}", err_lo=f"{lo:.6g}", err_hi=f"{hi:.6g}", approx="0",
                spin_lo=f"{c['spin_floor'] if a is None else a:.4f}", spin_text="CFG444")


# ---------------- runs
for tag, lst in (("RUN_A", tierA), ("RUN_AB", tierA + tierB)):
    res, _ = run(tag, [row(c) for c in lst])
    ex = overlap(res["primary"]["excluded_in_window"], *LIGHT); sv = surv(res["primary"]["excluded_in_window"], *LIGHT)
    v = "LIGHT END CLOSED" if not sv else ("NARROWED" if ex else "STAYS OPEN")
    OUT[tag] = dict(objects=[c["name"] for c in lst], excluded_light=ex, surviving_light=sv, verdict=v)
    P(f"\n{tag} ({len(lst)} objects): light end excluded {fmt(ex)}; surviving {fmt(sv)}; VERDICT {v}" + ("" if tag == "RUN_A" else " (indicative)"))
VERDICT = OUT["RUN_A"]["verdict"]

allwin = sorted(win.values(), key=lambda c: c["M"])
res_f, _ = run("RUN_FLOORS_ALL", [row(c) for c in allwin])
OUT["RUN_FLOORS_ALL"] = dict(n=len(allwin), excluded_light=overlap(res_f["primary"]["excluded_in_window"], *LIGHT))
P(f"RUN_FLOORS_ALL (all {len(allwin)} window objects at their R2 floors, any mass precision): light end excluded {fmt(OUT['RUN_FLOORS_ALL']['excluded_light'])}")
hyp = [row(c, a=0.98) for c in allwin if c["dynamical"]]
res_h, _ = run("RUN_HYP098", hyp, mutate=MUT)
OUT["RUN_HYP098"] = dict(n=len(hyp), excluded_light=overlap(res_h["primary"]["excluded_in_window"], *LIGHT),
                         per_object_light={n: overlap(iv, *LIGHT) for n, iv in res_h["per_object"].items() if overlap(iv, *LIGHT)})
P(f"RUN_HYP098 (HYPOTHETICAL: every dynamical window mass at its own errors with a >= 0.98){' MUTATE spins 0' if MUT else ''}: "
  f"light end excluded {fmt(OUT['RUN_HYP098']['excluded_light'])}; by: {', '.join(OUT['RUN_HYP098']['per_object_light']) or 'none'}")
if MUT:
    check("MUTATE: spins 0 on the hypothetical list -> union empty", not res_h["smbh"] and not res_h["xrb"])
else:
    mres, _ = run("RUN_FLOORS_ALL", [row(c) for c in allwin], mutate=True)
    check("MUTATE (frozen form): all window objects, CFG367_MUTATE=1 -> union empty", not mres["smbh"] and not mres["xrb"])

# ---------------- alpha table (frozen: every compiled window object)
P("\nALPHA = 7.49e9 M m at 2.01e-20 / 4.35e-20 eV (central M; [mass_range ends]); Omega_H(R2 floor)")
al = {}
for c in allwin:
    lo, hi = NS["mass_range"](row(c))
    a = c["spin_floor"]; OH = a / (2 * (1 + math.sqrt(max(1 - a * a, 0))))
    al[c["name"]] = dict(a20=NS["ALPHA_K"] * c["M"] * LIGHT[0], a435=NS["ALPHA_K"] * c["M"] * LIGHT[1], range20=[NS["ALPHA_K"] * lo * LIGHT[0], NS["ALPHA_K"] * hi * LIGHT[0]],
                         range435=[NS["ALPHA_K"] * lo * LIGHT[1], NS["ALPHA_K"] * hi * LIGHT[1]], Omega_H=OH, floor=a)
    if c["precise"] or c["spin_records"]:
        P(f"  {c['name']:11s} M={c['M']:.2e}: alpha {al[c['name']]['a20']:.3f} [{al[c['name']]['range20'][0]:.3f},{al[c['name']]['range20'][1]:.3f}] .. "
          f"{al[c['name']]['a435']:.3f} [{al[c['name']]['range435'][0]:.3f},{al[c['name']]['range435'][1]:.3f}]; Omega_H({a:.2f}) = {OH:.3f}")
P(f"  (all {len(al)} window objects in the results JSON; every R2 floor is {max(c['spin_floor'] for c in allwin):.2f} or less -> Omega_H <= "
  f"{max(v['Omega_H'] for v in al.values()):.3f})")
OUT["alpha"] = al

# ---------------- decider grid (D2)
mg = np.logspace(math.log10(LIGHT[0]), math.log10(LIGHT[1]), 200)


def dmask(r, a):
    lo, hi = NS["mass_range"](r); Ms = np.logspace(math.log10(lo), math.log10(hi), 9)
    return np.array([all(NS["excluded"](m, M, a, NS["TAU"]["smbh"]) for M in Ms) for m in mg])


# C3: CFG394 decider row reproduced
r394 = dict(set="smbh", mass_1e6=str(1.0 * 1e3), err_lo=str(0.1 * 1e3), err_hi=str(0.1 * 1e3), approx="0")
f394 = [d["frac_excluded"] for d in c394["decider"] if d["M"] == 1e9 and d["frac_err_1sig"] == 0.1 and d["a_lo"] == 0.98][0]
check("C3 CFG394 decider row (1.0e9, +/-10%, a>=0.98) reproduced", abs(dmask(r394, 0.98).mean() - f394) < 1e-12, f"{dmask(r394, 0.98).mean():.3f} vs {f394:.3f}")

# X-ray + accretion state
xr = {r["name"]: r for r in csv.DictReader(open(os.path.join(D, "xray_lookup.csv")))}
bf = sorted(float(x) for x in open(os.path.join(D, "bat105_fluxes.txt")).read().split() if x.replace(".", "").isdigit())
P(f"\nBAT105 non-detection limit F_lim = {F_LIM_BAT:.1e} cgs: {np.mean(np.array(bf) < F_LIM_BAT / 1e-12):.0%} of the {len(bf)} catalogue sources are fainter (sanity: limit sits near the survey's faint end)")
er = {}
for n in ("J0529", "J0920"):
    L = [l.split("\t") for l in open(os.path.join(D, f"erass1_{n}.tsv")) if l.strip() and not l.startswith("#")]
    er[n] = float(L[3][1]) if len(L) > 3 else None
gstate = {"J0529-4351": "efficient (paper: super-Eddington, L_bol >~ 1e48)", "J0920+0657": "efficient (paper: super-Eddington)", "3C273": "efficient (quasar)"}


def state(c):
    n = c["name"]
    if n in gstate: return "efficient", gstate[n], None
    x = xr.get(n)
    LE = LEDD * c["M"]
    if x and x["bat_flux_1e12cgs"]:
        if x["bat_logL"]:
            lam = KBOL_BAT * 10**float(x["bat_logL"]) / LE
        else:
            lam = KBOL_BAT * 4 * math.pi * (c["dist"] * MPC)**2 * float(x["bat_flux_1e12cgs"]) * 1e-12 / LE
        return ("efficient" if lam >= LAM_LLAGN else "LLAGN"), f"BAT105 detected ({x['bat_type']}), lambda ~ {lam:.1e}", lam
    if c["dist"]:
        lam = KBOL_BAT * 4 * math.pi * (c["dist"] * MPC)**2 * F_LIM_BAT / LE
        return ("LLAGN" if lam < LAM_LLAGN else "unknown"), f"BAT105 non-detection: lambda < {lam:.1e}", lam
    return "unknown", "no BAT, no distance", None


for c in comp.values():
    c["state"], c["state_basis"], c["lambda"] = state(c)
    x = xr.get(c["name"], {})
    c["xray"] = dict(nustar_ks=float(x["nustar_ks_3arcmin"]) if x else None, xmm_ks=float(x["xmm_ks_10arcmin"]) if x else None,
                     f2_12=float(x["f2_12_4xmm_median"]) if x and x["f2_12_4xmm_median"] else None,
                     bat=float(x["bat_flux_1e12cgs"]) * 1e-12 if x and x["bat_flux_1e12cgs"] else None)
    if c["name"] == "J0529-4351": c["xray"]["erass1_0.2_2.3"] = er["J0529"]
    if c["name"] == "J0920+0657": c["xray"]["erass1_0.2_2.3"] = er["J0920"]
    c["lacks_spectra"] = (c["xray"]["nustar_ks"] in (None, 0.0))

sets = {
    "D1a precise dynamical, 0.8-1.5e9": [c for c in comp.values() if c["precise"] and 0.8e9 <= c["M"] <= 1.5e9],
    "D1b precise dynamical, 3e8-3e9 (wider band)": [c for c in comp.values() if c["precise"] and 3e8 <= c["M"] <= 3e9 and not 0.8e9 <= c["M"] <= 1.5e9],
    "D1c dynamical 0.15-0.3 dex, 0.8-1.5e9": [c for c in comp.values() if c["dynamical"] and not c["precise"] and 0.15 < dex(c) <= 0.3 and 0.8e9 <= c["M"] <= 1.5e9],
}
# route B (labelled departure): AGN with spin records but non-dynamical / method-dependent masses, 0.5-2e9 -> what a GRAVITY mass at +/-10% would buy
routeB = [c for c in comp.values() if c["spin_records"] and not c["precise"] and 5e8 <= c["M"] <= 2e9]
c394rows = {r["name"]: r for r in csv.DictReader(open(os.path.join(C394, "spins_compiled_3e8_3e9.csv")))}
for n, r in c394rows.items():
    if n not in comp and 5e8 <= float(r["mass_1e6"]) * 1e6 <= 2e9:
        e = [s["edge"] for s in spins[n] if s["used"] and s["edge"] is not None]
        comp[n] = dict(name=n, M=float(r["mass_1e6"]) * 1e6, logM=math.log10(float(r["mass_1e6"]) * 1e6), dex_hi=0.4, dex_lo=0.4, method=r["mass_method"],
                       ref=r["mass_ref"], dynamical=False, precise=False, disagree=[], dist=None, spin_floor=min(e) if e else 0.0,
                       spin_records=[(s["ref"], s["method"], s["kind"], s["used"], s["edge"]) for s in spins[n]], state="efficient", state_basis="quasar (CFG394)", lam=None)
        x = xr.get(n, {})
        comp[n]["xray"] = dict(nustar_ks=float(x["nustar_ks_3arcmin"]) if x else None, xmm_ks=float(x["xmm_ks_10arcmin"]) if x else None,
                               f2_12=float(x["f2_12_4xmm_median"]) if x and x["f2_12_4xmm_median"] else None,
                               bat=float(x["bat_flux_1e12cgs"]) * 1e-12 if x and x["bat_flux_1e12cgs"] else None)
        comp[n]["lacks_spectra"] = comp[n]["xray"]["nustar_ks"] in (None, 0.0)
        routeB.append(comp[n])
routeB = sorted({c["name"]: c for c in routeB}.values(), key=lambda c: c["M"])

ZB = {r["name"]: float(r["z"]) for r in csv.DictReader(open(os.path.join(D, "redshifts_routeB.csv")))}
KLINES = {"Bry": 2.1661, "Paa": 1.8756, "Pab": 1.2822, "Ha": 0.6563, "Hb": 0.4861}   # um, rest (vacuum, approximate)


def gravity_feasible(c):
    """Departure (route B only): a broad line falls in GRAVITY's K band (1.95-2.45 um) and dec <= +30 (VLTI)."""
    x = xr.get(c["name"], {}); z = ZB.get(c["name"], float(x["bat_z"]) if x and x.get("bat_z") else c.get("z"))
    if z is None: return None, "z unknown"
    ln = [k for k, l in KLINES.items() if 1.95 <= l * (1 + z) <= 2.45]
    dec = float(x["dec"]) if x else None
    ok = bool(ln) and (dec is not None and dec <= 30)
    return ok, f"z={z}, K-band lines {ln or 'none'}, dec {dec:+.1f}" if dec is not None else f"z={z}, K-band lines {ln or 'none'}"


P("\nDECIDER LIST (D1-D5). frac = share of [2.01e-20, 4.35e-20] excluded by CFG367's mass_range/excluded at the object's OWN mass and errors with hypothetical spin floors")
DEC = {}
for sname, lst in list(sets.items()) + [("ROUTE B (departure, labelled): spin-record AGN 0.5-2e9 IF a GRAVITY mass at +/-10% existed", routeB)]:
    rows_ = []
    for c in lst:
        rb = sname.startswith("ROUTE B")
        r = row(c, err=0.10) if rb else row(c)
        fr = {a: float(dmask(r, a).mean()) for a in (0.7, 0.9, 0.98)}
        m98 = dmask(r, 0.98); rng = (float(mg[m98][0]), float(mg[m98][-1])) if m98.any() else None
        rows_.append(dict(name=c["name"], M=c["M"], dex=dex(c), method=c["method"], ref=c["ref"], state=c["state"], state_basis=c["state_basis"],
                          gravity=gravity_feasible(c) if rb else None, frac=fr, range98=rng, spin_floor=c["spin_floor"], xray=c["xray"], lacks_spectra=c["lacks_spectra"], mask98=m98.tolist(), mask90=dmask(r, 0.9).tolist()))
    rows_.sort(key=lambda t: (t["state"] != "efficient", not (t["gravity"] or [True])[0], -t["frac"][0.98], -((t["xray"]["f2_12"] or 0))))
    DEC[sname] = rows_
    P(f"\n {sname}: {len(rows_)}")
    for i, t in enumerate(rows_, 1):
        xx = t["xray"]
        P(f"  {i:2d}. {t['name']:11s} M={t['M']:.2e} +/-{t['dex']:.2f} dex ({t['method']}); {t['state']} [{t['state_basis']}]; "
          f"frac a>=0.7/0.9/0.98 = {t['frac'][0.7]:.2f}/{t['frac'][0.9]:.2f}/{t['frac'][0.98]:.2f}"
          + (f" [{t['range98'][0]:.2e}-{t['range98'][1]:.2e}]" if t["range98"] else "")
          + f"; NuSTAR {xx['nustar_ks']} ks, XMM {xx['xmm_ks']} ks, F(2-12) " + (f"{xx['f2_12']:.1e}" if xx['f2_12'] else "none")
          + (f", BAT {xx['bat']:.1e}" if xx["bat"] else "") + (f", eRASS1(0.2-2.3) {xx.get('erass1_0.2_2.3')}" if "erass1_0.2_2.3" in xx else "")
          + ("; LACKS NuSTAR" if t["lacks_spectra"] else "") + (f"; GRAVITY-feasible={t['gravity'][0]} ({t['gravity'][1]})" if t["gravity"] else ""))
        t["set"] = sname.split(" ")[0] + (" " + sname.split(" ")[1] if sname.startswith("ROUTE") else "")
# pairs
P("\nPAIRS (union of two holes' exclusions, each at own mass/errors; route B at +/-10%)")
pool = [t for s in DEC.values() for t in s]
pool = list({t["name"] + "|" + t["set"]: t for t in pool}.values())
pairs = []
for a, b in itertools.combinations(pool, 2):
    for key, al_ in (("mask98", 0.98), ("mask90", 0.9)):
        f = float((np.array(a[key]) | np.array(b[key])).mean())
        if a["name"] == b["name"]: continue
        pairs.append(dict(a=a["name"] + " [" + a["set"] + "]", b=b["name"] + " [" + b["set"] + "]", a_lo=al_, frac=f, both_efficient=a["state"] == "efficient" and b["state"] == "efficient"))
pairs.sort(key=lambda p: -p["frac"])
closing = [p for p in pairs if p["frac"] >= 0.99]
P(f"  closing pairs (>= 99%): {len(closing)}")
for p in closing[:15]:
    P(f"    {p['a']} + {p['b']} at a>={p['a_lo']}: {p['frac']:.2f}{'' if p['both_efficient'] else '  (involves an LLAGN: reflection spin not expected)'}")
P("  best pairs overall: " + "; ".join(f"{p['a']}+{p['b']} a>={p['a_lo']} {p['frac']:.2f}" for p in pairs[:5]))
real = [p for p in pairs if "ROUTE" not in p["a"] + p["b"]]
P("  best pairs among REAL masses only (no route-B hypothetical +/-10%): " + "; ".join(f"{p['a']}+{p['b']} a>={p['a_lo']} {p['frac']:.2f}" for p in real[:5]))
best_eff = [p for p in pairs if p["both_efficient"]][:5]
P("  best pairs with both radiatively efficient: " + "; ".join(f"{p['a']}+{p['b']} a>={p['a_lo']} {p['frac']:.2f}" for p in best_eff))
for s in DEC.values():
    for t in s:
        t.pop("mask98"); t.pop("mask90")
OUT["decider"] = DEC; OUT["pairs_top"] = pairs[:40]; OUT["closing_pairs"] = closing
OUT["compiled_window"] = {n: {k: v for k, v in c.items() if k not in ("all_masses",)} | {"all_masses": c.get("all_masses")} for n, c in win.items()}
OUT["verdict"] = VERDICT
P(f"\nVERDICT (RUN_A): {VERDICT}")
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1, default=str)
raise SystemExit(0 if all(CH) else 1)
