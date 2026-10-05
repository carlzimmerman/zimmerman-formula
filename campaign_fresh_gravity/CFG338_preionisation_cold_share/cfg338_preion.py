#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG336 -- formation-epoch density of the native cold mass vs the ultra-faint shortfall.  Criteria frozen first: FROZEN_CRITERIA.md (18a68e0ad).

  mass      M_c = M_b / f_b (CFG35 / CFG313 native; f_b = 0.157126); M_b = CFG45 sigma_read's own inventory.
  density   top-hat collapse at z_f: r_f = [3 M_c / (4 pi 18 pi^2 rho_m0 (1+z_f)^3)]^(1/3), rho_m0 = 2.7754e11 (w_b + w_c) Msun/Mpc^3 (h-free).
  profiles  P1 SIS truncated at r_f (CFG313 V2 shape, primary); P2 NFW r_s = r_f/4 (reported); PB all of M_c inside r (bound).
  readings  S = B's committed rule (CFG35, CFG45 S: f_ex switch); M = CFG4 T5 max bookkeeping written locally (CFG45 M); A = additive (diagnostic, NOT B).
  z_f       a-priori class split: M_V > -7.7 -> 8 (6..10); classical satellites and LV field dwarfs -> 3 (2..4).  Never tuned.
  machinery CFG45's satellite harness exec'd read-only (READ reduced to L), its sigma_read replaced by this lane's; LV field dwarfs via CFG313's d2 recipe.
CONTROLS  C1 z_f = 0 reproduces CFG313 native rows; C2 AUDIT_UFD baseline; C3 r_f scaling and profile normalisation.
MUTATE    CFG336_MUTATE=1: z_f permuted across all scored dwarfs (seed 336); outputs *_MUTATE.
Run: python3 campaign_fresh_gravity/CFG336_ufd_formation_epoch/cfg336_formation_epoch.py
"""
import os, sys, io, math, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C                                                     # noqa: E402
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
MUTATE = os.environ.get("CFG338_MUTATE") == "1"
MUT336 = False
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(s=""):
    print(s); OUT.append(s)


def check(name, ok, detail=""):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")


P(__doc__.split("Run: python3")[0].strip())
if MUT336:
    P("\n  *** MUTATE: z_f permuted across all scored dwarfs (seed 336) ***")
FOOTS = ("canonical", "alt")
WBC = 0.02237 + 0.1200
RHO_M0_KPC = 2.7754e11 * WBC / 1e9                                          # Msun / kpc^3
DELTA_C = 18 * math.pi ** 2
Z_CLASS = {"ufd": (6.0, 8.0, 10.0), "cls": (2.0, 3.0, 4.0)}


# ------------------------------------------------------------------------------------------------ CFG45 harness (read-only exec)
def quiet_exec(code, ns, name):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, name, "exec"), ns)
    os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return ns


SRC45 = open(os.path.join(LANES, "CFG45_rule_readings.py")).read()
SRC45 = SRC45[:SRC45.index('R.banner("C1  CONTROLS: (S) and (L) against the lanes\' committed results")')]
assert SRC45.count('READ = ("L", "S", "M", "E")') == 1
SRC45 = SRC45.replace('READ = ("L", "S", "M", "E")', 'READ = ("L",)')
NS = quiet_exec(SRC45, {"__file__": os.path.join(LANES, "CFG45_rule_readings.py"), "__name__": "cfg45_ro"}, "CFG45_ro")
FB = float(NS["FB"]); assert abs(FB - 0.157126) < 1e-6, FB
A0H, a_int, edge_info, UPS_V = NS["A0H"], NS["a_int"], NS["edge_info"], NS["UPS_V"]
G_S, MSUN_S = NS["G_SAT"], NS["MSUN_SAT"]
SAMPLES, UL = NS["SAMPLES"], NS["UL"]
FLD = NS["g42"]["ns"]["fld"]
UF_LAW = {f: NS["UF"][(f, "L")] for f in FOOTS}
CL_LAW = {(k, f): NS["CL"][(k, f, "L")] for k in ("cls", "col", "m31") for f in FOOTS}


def mv_of(d):
    for k in ("MV", "M_V", "mv"):
        if k in d and d[k] is not None and np.isfinite(d[k]):
            return float(d[k])
    return 4.83 - 2.5 * math.log10(d["LV"])


# per-dwarf class (declared): MW by sample membership (the ufd sample IS the M_V > -7.7 cut); M31 by M_V; LV field all classical-era
CLASS = {}
for d in SAMPLES["ufd"] + list(UL):
    CLASS[id(d)] = "ufd"
for d in SAMPLES["cls"]:
    CLASS[id(d)] = "cls"
for key in ("col", "m31"):
    for d in SAMPLES[key]:
        CLASS[id(d)] = "ufd" if mv_of(d) > -7.7 else "cls"
for d in FLD:
    CLASS[id(d)] = "cls"
ALL = [d for d in SAMPLES["ufd"] + list(UL) + SAMPLES["cls"] + SAMPLES["col"] + SAMPLES["m31"] + FLD]
ZTRIP = {id(d): Z_CLASS[CLASS[id(d)]] for d in ALL}

# ---- CFG338: population R_ind from CFG317 (fiducial yield -0.2), read from its committed JSON
_R = json.load(open(os.path.join(LANES, "CFG317_baryon_loss_cold_mass", "cfg317_baryon_loss_results.json")))["numbers"]["RIND"]["-0.2"]
RPOP = {"ufd": 10 ** _R["P1"]["med"], "cls": 10 ** _R["P2a"]["med"], "col": 10 ** _R["P2b"]["med"], "m31": 10 ** _R["P2c"]["med"], "fld": 10 ** _R["P2d"]["med"]}
KPOP = {}
def _setk(on, perm=None):
    KPOP.clear()
    if not on:
        return
    keys = ["ufd", "cls", "col", "m31", "fld"]; vals = [RPOP[k] for k in keys]
    if perm is not None:
        vals = [vals[j] for j in perm]
    m = dict(zip(keys, vals))
    for d in SAMPLES["ufd"] + list(UL): KPOP[id(d)] = m["ufd"]
    for d in SAMPLES["cls"]: KPOP[id(d)] = m["cls"]
    for d in SAMPLES["col"]: KPOP[id(d)] = m["col"]
    for d in SAMPLES["m31"]: KPOP[id(d)] = m["m31"]
    for d in FLD: KPOP[id(d)] = m["fld"]

if MUT336:
    trips = [ZTRIP[id(d)] for d in ALL]
    perm = np.random.default_rng(336).permutation(len(trips))
    ZTRIP = {id(d): trips[perm[i]] for i, d in enumerate(ALL)}
n_cls = {k: sum(1 for d in SAMPLES[k] if CLASS[id(d)] == "ufd") for k in ("col", "m31")}
P(f"\n  z_f classes: MW ufd {len(SAMPLES['ufd'])}+{len(UL)} limits (z_f 8); MW cls {len(SAMPLES['cls'])} (3); "
  f"M31 Collins {n_cls['col']}/{len(SAMPLES['col'])} ufd-class; M31 LVD {n_cls['m31']}/{len(SAMPLES['m31'])} ufd-class; LV field {len(FLD)} (3)")

CFGZ = dict(reading="L", prof="P1", zsel=1, zall=None, kmul=1.0)


def r_f_kpc(Mc, zf):
    return (3.0 * Mc / (4.0 * math.pi * DELTA_C * RHO_M0_KPC * (1.0 + zf) ** 3)) ** (1.0 / 3.0)


def _m(t):
    return math.log1p(t) - t / (1.0 + t)


def m_cold(Mc, r_kpc, zf, prof):
    if prof == "PB":
        return Mc
    rf = r_f_kpc(Mc, zf)
    if prof == "P1":
        return Mc * min(r_kpc / rf, 1.0)
    if prof == "P2":
        return Mc * _m(min(4.0 * r_kpc / rf, 4.0)) / _m(4.0)
    raise ValueError(prof)


def zf_of(d):
    return CFGZ["zall"] if CFGZ["zall"] is not None else ZTRIP[id(d)][CFGZ["zsel"]]


def sigma_read(d, foot, reading=None, ups=None, floor_mh=None, gas=False, info=False):
    """CFG45 sigma_read line for line (law part), plus this lane's cold term.  reading 'L' = law; otherwise CFGZ['reading']."""
    a0 = A0H[foot]; ups = UPS_V if ups is None else ups
    Ms = ups * d["LV"]
    Mb = Ms + (max(1.33 * d["MHI"], NS["infall_gas"](d)) if gas else 1.33 * d["MHI"])
    rh_pc = (4.0 / 3.0) * d["rh"]; rh = rh_pc * 3.0857e16
    gN = G_S * 0.5 * Mb * MSUN_S / rh ** 2
    g = a_int(gN, 0.0, a0); glaw = g
    rd = "L" if reading == "L" else CFGZ["reading"]
    Mc = CFGZ["kmul"] * KPOP.get(id(d), 1.0) * Mb / FB
    Mcold = m_cold(Mc, rh_pc / 1000.0, zf_of(d), CFGZ["prof"])
    gc = (1.0 - FB) * G_S * Mcold * MSUN_S / rh ** 2
    if rd == "S":
        ph, _ = edge_info(Mb, foot)
        g += max(0.0, 1.0 - ph / ((1.0 - FB) * Mc)) * gc
    elif rd == "M":
        g = gN + max(g - gN, gc)
    elif rd == "A":
        g += gc
    s = math.sqrt(g * rh / 3.0) / 1e3
    if info:
        return s, dict(Mb=Mb, ph_r=(glaw - gN) * rh ** 2 / (G_S * MSUN_S), cold_tot=(1.0 - FB) * Mc, cold_r=(1.0 - FB) * Mcold)
    return s


NS["sigma_read"] = lambda d, foot, reading, **kw: (sigma_read(d, foot, reading, **kw), 0.0)
offs, km_median, boot = NS["offs"], NS["km_median"], NS["boot"]


def ufd_x(foot, rd, ups=None):
    x = np.array([math.log10(d["sig"] / sigma_read(d, foot, rd, ups=ups)) for d in SAMPLES["ufd"]])
    xu = np.array([math.log10(d["sig_ul"] / sigma_read(d, foot, rd, ups=ups)) for d in UL])
    return km_median(x, xu), x, xu


def with_z(zsel, fn):
    old = CFGZ["zsel"]; CFGZ["zsel"] = zsel
    try:
        return fn()
    finally:
        CFGZ["zsel"] = old


def ufd_row(foot, rd):
    m, x, xu = ufd_x(foot, rd)
    err = boot(x, xu)
    u = [ufd_x(foot, rd, ups=v)[0] for v in (1.0, 4.0)]
    f_ups = 0.5 * abs(u[1] - u[0])
    zz = [with_z(s, lambda: ufd_x(foot, rd)[0]) for s in (0, 2)]
    f_zf = 0.5 * abs(zz[1] - zz[0])
    tot = math.sqrt(err ** 2 + f_ups ** 2 + f_zf ** 2)
    return dict(med=m, err=err, f_ups=f_ups, f_zf=f_zf, tot=tot, z=m / tot)


def sat_row(sample, foot, rd, gas=True, d2=False):
    def med(**kw):
        return float(np.median([math.log10(d["sig"] / sigma_read(d, foot, rd, gas=gas, **kw)) for d in sample]))
    x = np.array([math.log10(d["sig"] / sigma_read(d, foot, rd, gas=gas)) for d in sample])
    u = [med(ups=v) for v in (1.0, 4.0)]
    f_ups = 0.5 * abs(u[1] - u[0])
    zz = [with_z(s, lambda: med()) for s in (0, 2)]
    f_zf = 0.5 * abs(zz[1] - zz[0])
    err = 1.2533 * float(np.std(x)) / math.sqrt(len(x))
    tot = math.sqrt(err ** 2 + f_ups ** 2 + f_zf ** 2)
    return dict(med=float(np.median(x)), err=err, f_ups=f_ups, f_zf=f_zf, tot=tot, z=float(np.median(x)) / tot, n=len(x))


POPS = ("UFD", "CLS", "M31col", "M31lvd", "LVfld")


def score(rd, prof):
    CFGZ["reading"], CFGZ["prof"] = rd, prof
    out = {}
    for f in FOOTS:
        out[f"UFD|{f}"] = ufd_row(f, rd)
        out[f"CLS|{f}"] = sat_row(SAMPLES["cls"], f, rd)
        out[f"M31col|{f}"] = sat_row(SAMPLES["col"], f, rd)
        out[f"M31lvd|{f}"] = sat_row(SAMPLES["m31"], f, rd)
        out[f"LVfld|{f}"] = sat_row(FLD, f, rd, gas=False)
    return out


def verdict(res, base):
    others = all(abs(res[f"{p}|{f}"]["z"]) < 2 for p in POPS[1:] for f in FOOTS)
    if others and all(abs(res[f"UFD|{f}"]["z"]) < 2 for f in FOOTS):
        return "SOLVES"
    if others and all(res[f"UFD|{f}"]["med"] <= 0.5 * base[f] for f in FOOTS):
        return "PARTIAL"
    return "NOT"


RES = {"lane": "CFG336", "mutate": MUTATE, "f_b": FB, "rho_m0_Msun_kpc3": RHO_M0_KPC}
BASE = {f: UF_LAW[f]["km"] for f in FOOTS}

# ================================================================================================ controls
P("\n# C1-C3 controls")
law = score("L", "P1"); RES["law"] = law
AUD = json.load(open(os.path.join(LANES, "AUDIT_UFD_2026-10-03", "audit_ufd_results.json")))
d_aud = max(abs(law[f"UFD|{f}"]["med"] - AUD[f"base|{f}"]["km"]) for f in FOOTS)
check("C2 AUDIT_UFD baseline reproduced (law row)", d_aud < 1e-4, f"max |d km| = {d_aud:.2e}; z {law['UFD|canonical']['z']:+.2f} | {law['UFD|alt']['z']:+.2f}")
N313 = json.load(open(os.path.join(LANES, "CFG313_native_collapse_mass", "cfg313_native_rescore_results.json")))["numbers"]["mode_native_V2"]
CFGZ["zall"] = 0.0
c1 = {}
for rd in ("S", "M"):
    c1[rd] = score(rd, "P1")
dev, devrd, devwhere = 0.0, {}, {}
for rd in ("S", "M"):
    for f in FOOTS:
        dprev = dev; dev = 0.0
        dev = max(dev, abs(c1[rd][f"UFD|{f}"]["med"] - N313["UF"][f"{f}|S"]["km"]), abs(c1[rd][f"UFD|{f}"]["z"] - N313["UF"][f"{f}|S"]["z"]))
        for p, k in (("CLS", "cls"), ("M31col", "col"), ("M31lvd", "m31")):
            dev = max(dev, abs(c1[rd][f"{p}|{f}"]["med"] - N313["CL"][f"{k}|{f}|S"]["med"]))
        dev = max(dev, abs(c1[rd][f"LVfld|{f}"]["med"] - N313["D2"][f"{f}|S"]["med"]))
        devrd[rd] = max(devrd.get(rd, 0.0), dev); dev = max(dev, dprev)
for rd in ("S", "M"):
    for f in FOOTS:
        for p in POPS:
            ref = c1[rd][f"{p}|{f}"]["med"]; lw = law[f"{p}|{f}"]["med"]
            if abs(ref - lw) > 1e-9:
                devwhere[f"{rd}|{p}|{f}"] = ref - lw
P(f"  C1 detail: max dev reading S {devrd['S']:.2e}, reading M {devrd['M']:.2e}; rows moved off the law at z_f = 0: {devwhere if devwhere else 'none'}")
RES["C1_detail"] = dict(dev_by_reading=devrd, moved=devwhere)
CFGZ["zall"] = None
check("C1 z_f = 0 (S and M, P1) reproduces CFG313 native rows (inert)", dev < 1e-6, f"max dev {dev:.2e}")
RES["C1_dev"] = dev
d0 = SAMPLES["ufd"][0]; Mc0 = UPS_V * d0["LV"] / FB
sc = max(abs(r_f_kpc(Mc0 * 8, 5.0) / r_f_kpc(Mc0, 5.0) - 2.0), abs(r_f_kpc(Mc0, 3.0) / r_f_kpc(Mc0, 7.0) - 2.0))
nm = max(abs(m_cold(Mc0, r_f_kpc(Mc0, z), z, p) / Mc0 - 1) for z in (0.0, 3.0, 8.0) for p in ("P1", "P2"))
check("C3 r_f scaling M^(1/3)/(1+z) and profiles enclose M_c at r_f", sc < 1e-12 and nm < 1e-12, f"scale {sc:.1e}, norm {nm:.1e}")

# ================================================================================================ main scoring
P("\n# Main scoring (offset dex, z) -- canonical | alt")
MAIN = {}
for rd in ("S", "M", "A"):
    for prof in ("P1", "P2", "PB"):
        MAIN[f"{rd}|{prof}"] = score(rd, prof)
RES["main"] = MAIN
hdr = f"  {'row':10s} " + " ".join(f"{p:>22s}" for p in POPS)
P(hdr)
for key, res in [("law", law)] + list(MAIN.items()):
    P(f"  {key:10s} " + " ".join(f"{res[p + '|canonical']['med']:+.3f}({res[p + '|canonical']['z']:+.2f})|{res[p + '|alt']['z']:+.2f}".rjust(22) for p in POPS))
VER = {k: verdict(v, BASE) for k, v in MAIN.items()}
RES["verdicts"] = VER
P("\n  verdicts: " + "; ".join(f"{k} {v}" for k, v in VER.items()))
P(f"  DECISIVE (P1): S -> {VER['S|P1']}, M -> {VER['M|P1']}   (A is a diagnostic, not B)")

# ================================================================================================ the per-object bound
P("\n# Per-object bound: whole native cold share (1-f_b) M_c vs the law's phantom inside (4/3) r_half")
PER = {}
for f in FOOTS:
    rows = []
    for d in SAMPLES["ufd"] + list(UL):
        _, inf = sigma_read(d, f, "L", info=True)
        rows.append(dict(name=d.get("name", "?"), Mb=inf["Mb"], ph_r=inf["ph_r"], cold_tot=inf["cold_tot"], ratio=inf["ph_r"] / inf["cold_tot"]))
    PER[f] = rows
    r = np.array([x["ratio"] for x in rows])
    P(f"  {f:9s}: phantom/cold_total over {len(r)} UFDs: min {r.min():.2f}, median {np.median(r):.2f}, max {r.max():.2f}; all > 1: {bool((r > 1).all())}")
RES["per_object"] = PER
sat_ratio = {}
for key, smp, gas in (("CLS", SAMPLES["cls"], True), ("M31col", SAMPLES["col"], True), ("M31lvd", SAMPLES["m31"], True), ("LVfld", FLD, False)):
    rr = [sigma_read(d, "canonical", "L", gas=gas, info=True)[1] for d in smp]
    sat_ratio[key] = sorted(x["ph_r"] / x["cold_tot"] for x in rr)
    P(f"  {key:7s} canonical phantom/cold_total: min {min(sat_ratio[key]):.2f}, median {np.median(sat_ratio[key]):.2f} (n {len(rr)})")
RES["sat_ratio_canonical"] = sat_ratio

# ================================================================================================ screens (report only)
P("\n# Screen: multiplier k on M_c needed for the UFD KM median to reach 2 x (law error) and 0 (canonical), reading M")


def k_needed(prof, target, foot="canonical"):
    CFGZ["reading"], CFGZ["prof"] = "M", prof
    lo, hi = 1.0, 1e4
    def f(k):
        CFGZ["kmul"] = k; v = ufd_x(foot, "M")[0]; CFGZ["kmul"] = 1.0; return v
    if f(lo) <= target:
        return 1.0
    if f(hi) > target:
        return float("inf")
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        lo, hi = (mid, hi) if f(mid) > target else (lo, mid)
    return hi


tgt2 = 2.0 * UF_LAW["canonical"]["tot"]
KN = {f"{p}|{t}": k_needed(p, v) for p in ("PB", "P1") for t, v in (("2sig", tgt2), ("zero", 0.0))}
RES["k_needed"] = KN
P("  " + "; ".join(f"{k}: k = {v:.1f}" for k, v in KN.items()) + f"   (target 2 x law err = {tgt2:.3f} dex)")
P("  P1 at fixed z_f: M_cold(<r) = M_c r / r_f  proportional to  M_c^(2/3) (1+z_f) r  -> slope 2/3 in M_b at fixed r, not 0.52; z_f is one value per class,"
  " so the within-class scatter it predicts is 0 (CFG335 needs 0.6 dex).")

# ================================================================================================ MUTATE-sensitive checks
P("\n# Checks")
if False:
    MN = json.load(open(os.path.join(HERE, "cfg336_formation_epoch_results.json")))["main"]
    dA = MAIN["A|P1"]["UFD|canonical"]["med"] - MN["A|P1"]["UFD|canonical"]["med"]
    dM = MAIN["M|P1"]["UFD|canonical"]["med"] - MN["M|P1"]["UFD|canonical"]["med"]
    check("MUTATE: additive (A, P1) UFD offset degrades (rises) under permuted z_f", dA > 0, f"d = {dA:+.4f} dex")
    check("MUTATE: reading M (P1) UFD offset does not improve", dM >= -1e-12, f"d = {dM:+.4f} dex (0 = inert in both)")
    RES["mutate_delta"] = dict(A=dA, M=dM)
else:
    allin = all(x["ratio"] > 1 for f in FOOTS for x in PER[f])
    check("H1 [pre-flight] whole cold share below the phantom for every UFD, both footings", allin)
    inert = max(abs(MAIN[f"{rd}|{p}"][f"UFD|{f}"]["med"] - law[f"UFD|{f}"]["med"]) for rd in ("S", "M") for p in ("P1", "P2", "PB") for f in FOOTS)
    check("H2 [prediction] readings S and M leave the UFD row at the law value for every profile", inert < 1e-12, f"max shift {inert:.1e}")

RES["checks"] = CHECKS
with open(os.path.join(HERE, f"cfg338_base_cfg336rows.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
with open(os.path.join(HERE, f"cfg338_base_cfg336rows.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=float)
nfail = sum(not c["ok"] for c in CHECKS)
P(f"\n{len(CHECKS) - nfail}/{len(CHECKS)} checks pass")
pass  # CFG338: the inherited CFG336 rows are printed above; CFG338 scoring follows


# ================= CFG338 scoring =================
L338 = []
def Q(x=""):
    print(x); L338.append(x)
Q("\nCFG338 -- cold share from pre-reionisation baryons, M_c = R_ind M_b/f_b" + ("   *** MUTATE: R_ind permuted ***" if MUTATE else ""))
Q("R_ind by population: " + ", ".join(f"{k} {v:.1f}" for k, v in RPOP.items()))
CFGZ["kmul"] = 1.0
_setk(False); base_M = score("M", "PB")
_setk(True, perm=(np.random.default_rng(338).permutation(5) if MUTATE else None))
R338 = {}
for rd, pf in (("M", "PB"), ("M", "P1"), ("S", "PB")):
    R338[f"{rd}|{pf}"] = score(rd, pf)
    Q(f"\n  reading {rd}, profile {pf}:")
    for f in FOOTS:
        Q("    " + f + ": " + "  ".join(f"{p} {R338[f'{rd}|{pf}'][f'{p}|{f}']['med']:+.3f} ({R338[f'{rd}|{pf}'][f'{p}|{f}']['z']:+.2f})" for p in POPS))
_setk(False); c1 = score("M", "PB")
c1ok = all(abs(c1[k]["med"] - MAIN["M|PB"][k]["med"]) < 1e-9 for k in c1) if "MAIN" in globals() else None
Q(f"\n  C1 R_ind = 1 reproduces CFG336 M|PB: {c1ok}")
def dec(res, f):
    u = res[f"UFD|{f}"]; others = [res[f"{p}|{f}"] for p in POPS if p != "UFD"]
    if abs(u["z"]) < 2 and all(abs(o["z"]) < 2 for o in others): return "SOLVES"
    if abs(u["med"]) <= 0.5 * abs(base_M[f"UFD|{f}"]["med"]) and sum(abs(o["z"]) >= 2 for o in others) <= 1: return "PARTIAL"
    return "NOT"
V = {f: dec(R338["M|PB"], f) for f in FOOTS}
order = ["NOT", "PARTIAL", "SOLVES"]; verdict = min(V.values(), key=order.index)
Q(f"\n  decision row M|PB: {V} -> VERDICT {verdict}")
tag = "_MUTATE" if MUTATE else ""
open(os.path.join(HERE, f"cfg338_preion{tag}.out"), "w").write("\n".join(L338) + "\n")
json.dump({"lane": "CFG338", "RPOP": RPOP, "rows": R338, "decision": V, "verdict": verdict, "C1": c1ok}, open(os.path.join(HERE, f"cfg338_preion{tag}_results.json"), "w"), indent=1, default=float)
