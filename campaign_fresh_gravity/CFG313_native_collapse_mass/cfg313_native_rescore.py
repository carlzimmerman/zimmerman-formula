#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG313 -- B's cold-mass rule with a FRAMEWORK-NATIVE collapse mass, M_c = M_b / f_b, re-scored on every population the rule has met.

Criteria frozen and committed before any score: campaign_fresh_gravity/CFG313_native_collapse_mass/FROZEN_CRITERIA.md.

  native mass  M_c = M_b / f_b, f_b = Omega_b/Omega_m = 0.02237/(0.02237 + 0.1200) (CFG35's FB); M_b = the lane's own baryon mass, the same one fed to
               its edge phantom.  No feedback, no abundance matching.
  profiles     V1 = h48's Dutton-Maccio NFW (200c) as committed (its c(M) is LCDM-derived); V2 = a singular isothermal truncated at the law's own
               turnaround radius, M_cold(<r) = M_c min(r / r_ta, 1), r_ta = CFG7's r_ta_law (= r_e / 0.40), no parameter.
  machinery    CFG45 (satellites, SPARC, UGC 2487, Di Teodoro, SLUGGS h50, X-ray, Ogle), CFG58 (d2) (LV field dwarfs, CFG45's estimator),
               CFG55 (SLUGGS JAM), CFG111 (SLUGGS literature gamma), CFG39 (SPARC rms) -- each exec'd read-only with its own MUTATE off; where a
               collapse mass enters, the call site is replaced by a hook whose 'committed' mode returns the lane's own function (C1 proves it).
CONTROLS  C1 committed masses reproduce the committed numbers; C2 M_c -> 0 gives the law; C3 the native hook is M_b/f_b and V2 is the declared shape.
CHECKS    H1 [prediction] f_ex = 0 everywhere under the native mass: every native rule row equals the law row (V1 and V2); H2/H3 reported tables.
MUTATE=1: f_b x 0.5 wherever f_b enters the rule (native V1) -- the check 'every population shifts in the predicted direction' is predicted to FAIL.
Run: python3 campaign_fresh_gravity/CFG313_native_collapse_mass/cfg313_native_rescore.py   (MUTATE=1 for the control)
"""
import os, sys, io, math, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("cfg313_native_rescore", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: f_b x 0.5 in the native rule -- the shift check is predicted to FAIL (the rule stays inert) ***")
FOOTS = ("canonical", "alt")
BAR = "# ================================================================================================ "
CFG = dict(mode="committed", prof="nfw", fbx=1.0, floor="native", lmcut=10.0, foot="canonical", collect=True)
LOG = dict(ratio=[], mb=set(), mb_scored=set())
FB0 = None                                                        # set from CFG35 once loaded


def quiet_exec(code, ns, name):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, name, "exec"), ns)
    os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return ns


def patch(src, pairs, name):
    for old, new in pairs:
        n = src.count(old)
        assert n == 1, f"{name}: patch target found {n} times: {old[:70]}"
        src = src.replace(old, new)
    return src


# ------------------------------------------------------------------------------------------------ the hooks
def mc_native(Mb):
    fb = FB0 * CFG["fbx"]; Mc = Mb / fb
    LOG["ratio"].append(Mc * fb / Mb); LOG["mb"].add(float(Mb))
    if CFG["collect"]:
        LOG["mb_scored"].add(float(Mb))
    return Mc


def make_mc(committed_fn):
    """committed_fn(Ms, colour) -> the lane's own collapse mass; returns the hook (Ms, colour, Mb) -> M_c for the current mode."""
    def hook(Ms, colour, Mb):
        if CFG["mode"] == "committed":
            return float(committed_fn(Ms, colour))
        if CFG["mode"] == "zero":
            return 1e-30
        return mc_native(Mb)
    return hook


def make_floor():
    def hook(floor_mh, Mb):
        if CFG["mode"] == "committed":
            return floor_mh
        if CFG["mode"] == "zero":
            return 1e-30
        if CFG["floor"] == "verbatim":
            return floor_mh
        return (floor_mh / 1e9) * mc_native(Mb)                    # the committed 1e8..1e10 span = x0.1..x10 about the clamp
    return hook


def sis_enclosed(Mh, r_kpc, rta_kpc):
    return Mh * np.minimum(np.asarray(r_kpc, float) / rta_kpc, 1.0)


def rta_kpc(Mb, foot):
    return C.r_ta_law(Mb, C.A0[foot], C.nu_mono, 1.0) * 1000.0


# ================================================================================================ CFG45 (hooked)
SRC45 = open(os.path.join(LANES, "CFG45_rule_readings.py")).read()
SRC45 = SRC45[:SRC45.index('R.banner("C1  CONTROLS: (S) and (L) against the lanes\' committed results")')]
SRC45 = patch(SRC45, [
    ('g10, halo_mass = g36["g10"], g35["halo_mass"]', 'g10, halo_mass = g36["g10"], g35["halo_mass"]\nFB = FB * __CFG__["fbx"]'),
    ('READ = ("L", "S", "M", "E")', 'READ = ("L", "S")'),
    ('return fex * (1 - FB) * np.asarray(nfw_enclosed(Mh, r), float) * conv', 'return fex * (1 - FB) * np.asarray(__PROF__(Mh, r, r_e_kpc), float) * conv'),
    ('Mh = float(halo_mass(UPS_V * d["LV"])) * MCF', 'Mh = float(__MC__(UPS_V * d["LV"], None, Mb)) * MCF'),
    ('Mh = floor_mh * MCF', 'Mh = __FLOOR__(floor_mh, Mb) * MCF'),
    ('Mh = (float(halo_mass(Ms)) if kind == "dwarf" else collapse(Ms, "blue" if m["T"] >= 1 else "red")) * MCF',
     'Mh = __MC__(Ms, None if kind == "dwarf" else ("blue" if m["T"] >= 1 else "red"), Mb) * MCF'),
    ('Mh = collapse(Ms, "blue" if UGC["T"] >= 1 else "red") * MCF', 'Mh = __MC__(Ms, "blue" if UGC["T"] >= 1 else "red", Mb) * MCF'),
    ('Mh = collapse(Ms, colour_of(g)) * MCF', 'Mh = __MC__(Ms, colour_of(g), Mb) * MCF'),
    ('Mh = collapse(Ms, "red") * MCF', 'Mh = __MC__(Ms, "red", Ms) * MCF'),
    ('Mh = collapse(g["uk"] * g["LK"], "red") * MCF', 'Mh = __MC__(g["uk"] * g["LK"], "red", Ms) * MCF'),
    ('Mh = collapse(Ms, col) * MCF', 'Mh = __MC__(Ms, col, Mb) * MCF'),
], "CFG45")


def run45():
    ns = {"__file__": os.path.join(LANES, "CFG45_rule_readings.py"), "__name__": "cfg45_hooked", "__CFG__": CFG}
    ns["__MC__"] = make_mc(lambda Ms, colour: ns["halo_mass"](Ms) if colour is None else ns["collapse"](Ms, colour))
    ns["__FLOOR__"] = make_floor()
    ns["__PROF__"] = lambda Mh, r, r_e_kpc: (ns["nfw_enclosed"](Mh, r) if CFG["prof"] == "nfw" else sis_enclosed(Mh, r, r_e_kpc / ns["XE"]))
    quiet_exec(SRC45, ns, "CFG45_hooked")
    # LV field dwarfs: CFG58 (d2), CFG45's estimator without infall gas, CFG58's error recipe line for line
    FLD = ns["g42"]["ns"]["fld"]; sr = ns["sigma_read"]
    offs_fld = lambda foot, rd_, **kw: np.array([math.log10(d["sig"] / sr(d, foot, rd_, **kw)[0]) for d in FLD])
    D2 = {}
    for foot in FOOTS:
        for rd_ in ("L", "S"):
            x = offs_fld(foot, rd_)
            ups = [offs_fld(foot, rd_, ups=u) for u in (1.0, 4.0)]
            f_ups = 0.5 * abs(float(np.median(ups[1])) - float(np.median(ups[0])))
            flo = [float(np.median(offs_fld(foot, rd_, floor_mh=fm))) for fm in ns["FLOORS"]] if rd_ == "S" else [float(np.median(x))]
            err = 1.2533 * float(np.std(x)) / math.sqrt(len(x)); tot = math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)
            D2[(foot, rd_)] = dict(med=float(np.median(x)), tot=tot, z=float(np.median(x)) / tot, n=len(x))
    return dict(UF=ns["UF"], CL=ns["CL"], SP=ns["SP"], U2=ns["U2"], DT=ns["DT"], SL=ns["SL"], XR=ns["XR"], OG=ns["OG"], D2=D2), ns


# ================================================================================================ CFG55 / CFG111 (hooked by namespace)
SRC111 = open(os.path.join(LANES, "CFG111_sluggs_literature_gamma.py")).read()
g111 = quiet_exec(SRC111[:SRC111.index("MASS = {f: dict(")], {"__file__": os.path.join(LANES, "CFG111_sluggs_literature_gamma.py"), "__name__": "cfg111"}, "CFG111")
g55 = g111["g55"]
FB0 = float(g55["FB"])
_col55, _ep55, _nfw55 = g55["collapse"], g55["edge_phantom"], g55["nfw_enclosed"]
MC55 = make_mc(lambda Ms, colour: _col55(Ms, colour))


def debris313(Ms, foot):
    Mh = MC55(Ms, "red", Ms)
    return max(0.0, 1.0 - _ep55(Ms, foot, 0.40) / ((1 - FB0 * CFG["fbx"]) * Mh)), Mh


def prof55(Mh, r):
    if CFG["prof"] == "nfw":
        return _nfw55(Mh, r)
    Mb = Mh * FB0 * CFG["fbx"]                                     # native mode only (V2 is run only with the native mass)
    return sis_enclosed(Mh, r, rta_kpc(Mb, CFG["foot"]))


for _ns in (g55, g111):
    _ns["debris"] = debris313; _ns["nfw_enclosed"] = prof55


def run55():
    g55["FB"] = g111["FB"] = FB0 * CFG["fbx"]
    out55, out111 = {}, {}
    CFG["collect"] = False                                        # solver trial masses are not scored objects
    for f in FOOTS:
        CFG["foot"] = f
        ML = [g55["law_mass_g"](g, f) for g in g55["G16"]]; MR = [g55["rule_mass"](g, f) for g in g55["G16"]]; MS = [g["r"]["Mstar"] for g in g55["G16"]]
        s = g55["sample"]
        o = dict(law=s(f, ML, "law"), rule=s(f, MR, "rule"), law_sl=s(f, MS, "law"), rule_sl=s(f, MS, "rule"))
        out55[f] = {k: dict(mean=v[1], err=v[2], z=v[1] / v[2], n=len(v[0])) for k, v in o.items()}
        if CFG["mode"] == "native":
            LOG["mb_scored"].update(float(m) for m in ML + MR + MS if np.isfinite(m))
        sg = g111["sample_g"]; GL = g111["GLIT"]
        o = dict(law=sg(f, ML, "law", GL), rule=sg(f, MR, "rule", GL))
        out111[f] = {k: dict(mean=v[1], err=v[2], z=v[1] / v[2], n=len(v[0])) for k, v in o.items()}
    g55["FB"] = g111["FB"] = FB0
    CFG["foot"] = "canonical"; CFG["collect"] = True
    return out55, out111


# ================================================================================================ CFG39 SPARC rms (hooked)
SRC39 = open(os.path.join(LANES, "CFG39_harness_with_rule.py")).read()
i_b = SRC39.index(BAR + "C1 the budget"); i_s = SRC39.index(BAR + "SPARC"); i_g = SRC39.index("gpred = np.where(ok,"); i_k = SRC39.index(BAR + "KiDS threshold")
ns39 = {"__file__": os.path.join(LANES, "CFG39_harness_with_rule.py"), "__name__": "cfg39"}
quiet_exec(SRC39[:i_b], ns39, "CFG39_head")
quiet_exec(SRC39[i_s:i_g], ns39, "CFG39_sparc_load")
SRC39L = patch(SRC39[i_g:i_k], [
    ("if math.log10(Ms) < 10.0:", "if math.log10(Ms) < __CFG__['lmcut']:"),
    ("Mh = MCF * collapse(Ms, colour)", "Mh = MCF * __MC__(Ms, colour, Mb)"),
    ("float(nfw_enclosed(Mh, rr / KPC_S))", "float(__PROF__(Mh, rr / KPC_S, Mb))"),
], "CFG39")
_col39, _nfw39 = ns39["collapse"], ns39["nfw_enclosed"]
ns39["__CFG__"] = CFG
ns39["__MC__"] = make_mc(lambda Ms, colour: _col39(Ms, colour))
ns39["__PROF__"] = lambda Mh, r, Mb: (_nfw39(Mh, r) if CFG["prof"] == "nfw" else float(sis_enclosed(Mh, r, rta_kpc(Mb, "canonical"))))


def run39():
    ns39["FB"] = FB0 * CFG["fbx"]
    quiet_exec(SRC39L, ns39, "CFG39_sparc_loop")
    ns39["FB"] = FB0
    return dict(rms0=ns39["rms0"], rms1=ns39["rms1"], touched=list(ns39["touched"]))


# ================================================================================================ run the modes
def run_mode(mode, prof="nfw", fbx=1.0, floor="native"):
    CFG.update(mode=mode, prof=prof, fbx=fbx, floor=floor, lmcut=(10.0 if mode == "committed" else -1e9))
    b, ns = run45()
    b["C55"], b["C111"] = run55()
    b["C39"] = run39()
    CFG.update(mode="committed", prof="nfw", fbx=1.0, floor="native", lmcut=10.0)
    return b, ns


MODES = {}
if not MUTATE:
    MODES["committed"], NS45 = run_mode("committed")
    MODES["zero"], _ = run_mode("zero")
LOG["ratio"].clear(); LOG["mb"].clear(); LOG["mb_scored"].clear()
MODES["native_V1"], NS45 = run_mode("native", "nfw")
MODES["native_V2"], _ = run_mode("native", "sis")
if MUTATE:
    MODES["native_V1_fbhalf"], _ = run_mode("native", "nfw", fbx=0.5)
else:
    MODES["native_V1_floor_verbatim"], _ = run_mode("native", "nfw", floor="verbatim")

# ================================================================================================ row extraction
# each row: (id, label, getter(bundle, foot, reading) -> (offset, z)), with readings "L" / "S"
def g_uf(b, f, r): v = b["UF"][(f, r)]; return v["km"], v["z"]
def g_cl(key): return lambda b, f, r: (b["CL"][(key, f, r)]["med"], b["CL"][(key, f, r)]["z"])
def g_d2(b, f, r): v = b["D2"][(f, r)]; return v["med"], v["z"]
def g_ugc(b, f, r): v = b["U2"][(f, r)]; return v["off"], v["z"]
def g_s0(b, f, r): v = b["DT"][(f, r)]; return v["s0"]["corr"], v["s0z"]
def g_dt(b, f, r): v = b["DT"][(f, r)]["all"]; return v["corr"], v["z"]
def g_sl(b, f, r): v = b["SL"][(f, r)]; return v["mean"], v["z"]
def g_c55(kl, kr): return lambda b, f, r: (b["C55"][f][kl if r == "L" else kr]["mean"], b["C55"][f][kl if r == "L" else kr]["z"])
def g_c111(b, f, r): v = b["C111"][f]["law" if r == "L" else "rule"]; return v["mean"], v["z"]
def g_xr(b, f, r): v = b["XR"][(f, r)]; return v["mean"], v["z"]
def g_og(b, f, r): v = b["OG"][(f, r)]; return v["mean"], v["z"]


absz = lambda zc, za: abs(zc) < 2 and abs(za) < 2
above = lambda zc, za: zc > -2 and za > -2
ROWS = [
    ("P1", "MW ultra-faints (KM median)", g_uf, absz, "A1"),
    ("P2a", "MW classical dSph", g_cl("cls"), above, "A2"),
    ("P2b", "M31 Collins+13", g_cl("col"), above, "A2"),
    ("P2c", "M31 LVD", g_cl("m31"), above, "A2"),
    ("P2d", "LV field dwarfs (CFG58 d2)", g_d2, absz, "|z|<2"),
    ("P4a", "UGC 2487", g_ugc, absz, "A6"),
    ("P4b", "Di Teodoro four S0/S0a", g_s0, lambda zc, za: zc > -2, "A7 (canonical)"),
    ("P4b'", "Di Teodoro all 15", g_dt, lambda zc, za: abs(zc) < 2, "H2a (reported)"),
    ("P5", "SLUGGS h50 masses (19)", g_sl, absz, "A4"),
    ("P5J", "SLUGGS JAM, gamma 3 (CFG55)", g_c55("law", "rule"), absz, "CFG55 H2"),
    ("P5S", "SLUGGS SLUGGS masses (16)", g_c55("law_sl", "rule_sl"), absz, "CFG55 R1"),
    ("P5L", "SLUGGS JAM, literature gamma (CFG111)", g_c111, absz, "CFG111 H2"),
    ("P6", "X-ray ellipticals", g_xr, absz, "A5"),
    ("P7", "Ogle super spirals", g_og, absz, "reported"),
]

# ================================================================================================ CONTROLS
R.banner("C1  CONTROL: with the committed Moster / Mandelbaum masses and NFW the hooked harness reproduces the committed numbers")
J = lambda n: json.load(open(os.path.join(LANES, n)))["numbers"]
if not MUTATE:
    b = MODES["committed"]; c45 = J("CFG45_rule_readings_results.json"); c58 = J("CFG58_rule_more_populations_results.json")
    c55 = J("CFG55_sluggs_dynamical_masses_results.json")["RES"]; c111 = J("CFG111_sluggs_literature_gamma_results.json")["RES"]; c39 = J("CFG39_harness_with_rule_results.json")["sparc"]
    devs = []
    for f in FOOTS:
        for r in ("L", "S"):
            for k in ("km", "tot", "z"):
                devs.append((f"CFG45 UF {f}|{r} {k}", abs(b["UF"][(f, r)][k] - c45["UF"][f"{f}|{r}"][k]), 1e-6))
            for key in ("cls", "col", "m31"):
                for k in ("med", "tot", "z"):
                    devs.append((f"CFG45 CL {key}|{f}|{r} {k}", abs(b["CL"][(key, f, r)][k] - c45["CL"][f"{key}|{f}|{r}"][k]), 1e-6))
            for k in ("off", "z"):
                devs.append((f"CFG45 UGC {f}|{r} {k}", abs(b["U2"][(f, r)][k] - c45["UGC2487"][f"{f}|{r}"][k]), 1e-6))
            devs.append((f"CFG45 DT s0z {f}|{r}", abs(b["DT"][(f, r)]["s0z"] - c45["DT23"][f"{f}|{r}"]["s0z"]), 1e-6))
            devs.append((f"CFG45 DT all z {f}|{r}", abs(b["DT"][(f, r)]["all"]["z"] - c45["DT23"][f"{f}|{r}"]["all"]["z"]), 1e-6))
            for k in ("mean", "z"):
                devs.append((f"CFG45 SLUGGS {f}|{r} {k}", abs(b["SL"][(f, r)][k] - c45["SLUGGS"][f"{f}|{r}"][k]), 1e-6))
            for k in ("mean", "tot", "z"):
                devs.append((f"CFG45 XRAY {f}|{r} {k}", abs(b["XR"][(f, r)][k] - c45["XRAY"][f"{f}|{r}"][k]), 1e-6))
                devs.append((f"CFG45 OGLE {f}|{r} {k}", abs(b["OG"][(f, r)][k] - c45["OGLE"][f"{f}|{r}"][k]), 1e-6))
                devs.append((f"CFG58 field {f}|{r} {k if k != 'mean' else 'med'}", abs(b["D2"][(f, r)][k if k != "mean" else "med"] - c58["field_dwarfs"][f"{f}|{r}"][k if k != "mean" else "med"]), 1e-6))
        for k55 in ("law", "rule"):
            devs.append((f"CFG55 {f} {k55}", abs(b["C55"][f][k55]["mean"] - c55[f][k55]["mean"]), 1e-9))
            devs.append((f"CFG111 {f} {k55}", abs(b["C111"][f][k55]["mean"] - c111[f][k55]["mean"]), 1e-9))
        devs.append((f"CFG55 {f} law_sluggs", abs(b["C55"][f]["law_sl"]["mean"] - c55[f]["law_sluggs"]["mean"]), 1e-9))
        devs.append((f"CFG55 {f} rule_sluggs", abs(b["C55"][f]["rule_sl"]["mean"] - c55[f]["rule_sluggs"]["mean"]), 1e-9))
    for kind in ("dwarf", "spiral"):
        for r in ("L", "S"):
            for k in ("frac_lt003", "max"):
                devs.append((f"CFG45 SPARC {kind}|{r} {k}", abs(b["SP"][(kind, r)][k] - c45["SPARC"][f"{kind}|{r}"][k]), 1e-6))
    devs.append(("CFG39 rms0", abs(b["C39"]["rms0"] - c39["rms0"]), 1e-9)); devs.append(("CFG39 rms1", abs(b["C39"]["rms1"] - c39["rms1"]), 1e-9))
    worst = max(devs, key=lambda t: t[1] / t[2]); over = [d for d in devs if d[1] > d[2]]
    check("C1 CONTROL: committed masses reproduce CFG45 (UF/CL/UGC/DT23/SLUGGS/X-ray/Ogle/SPARC, 1e-6), CFG58 field dwarfs (1e-6), CFG55 and CFG111 means (1e-9), CFG39 rms (1e-9)",
          f"{len(devs)} comparisons; worst ratio to tolerance {worst[1] / worst[2]:.2e} ({worst[0]}: {worst[1]:.1e}); over tolerance: {[(d[0], f'{d[1]:.1e}') for d in over]}",
          not over)

    R.banner("C2  CONTROL: with M_c -> 0 every rule row equals the law row")
    b = MODES["zero"]; dz = []
    for rid, lab, gt, _, _ in ROWS:
        for f in FOOTS:
            (oL, zL), (oS, zS) = gt(b, f, "L"), gt(b, f, "S")
            dz.append((f"{rid} {f}", max(abs(oL - oS), abs(zL - zS))))
    for kind in ("dwarf", "spiral"):
        dz.append((f"SPARC {kind}", max(abs(b["SP"][(kind, "S")]["max"]), abs(b["SP"][(kind, "S")]["frac_lt003"] - b["SP"][(kind, "L")]["frac_lt003"]))))
    dz.append(("CFG39 rms", abs(b["C39"]["rms1"] - b["C39"]["rms0"])))
    wz = max(dz, key=lambda t: t[1])
    check("C2 CONTROL: M_c = 1e-30 Msun: every rule row equals the law row (offset and z) to 1e-9, both footings", f"{len(dz)} comparisons; worst {wz[0]}: {wz[1]:.1e}",
          wz[1] <= 1e-9)
else:
    check("C1 CONTROL: skipped in the MUTATE run", "-", True, load_bearing=False)
    check("C2 CONTROL: skipped in the MUTATE run", "-", True, load_bearing=False)

R.banner("C3  CONTROL: the native hook returns M_b / f_b; V2 has the declared shape")
rat = np.array(LOG["ratio"]); mb = np.array(sorted(LOG["mb"]))
rt = rta_kpc(1e8, "canonical")
v2 = max(abs(sis_enclosed(5e9, rt, rt) / 5e9 - 1), abs(sis_enclosed(5e9, rt / 2, rt) / 2.5e9 - 1), abs(sis_enclosed(5e9, 3 * rt, rt) / 5e9 - 1))
check("C3 CONTROL: over every native rule evaluation M_c f_b / M_b = 1 (1e-12); V2: M(<r_ta) = M_c, M(<r_ta/2) = M_c/2, flat beyond (1e-12)",
      f"{len(rat)} evaluations, {len(mb)} distinct M_b ({mb.min():.2e}-{mb.max():.2e} Msun); max |ratio - 1| {np.max(np.abs(rat - 1)):.1e}; V2 max deviation {v2:.1e}; f_b = {FB0:.6f}",
      len(rat) > 0 and np.max(np.abs(rat - 1)) <= 1e-12 and v2 <= 1e-12)

# the inertness margin: by what factor must the native cold share grow before the rule touches any scored object?
ei = NS45["edge_info"]
mbs = np.array(sorted(LOG["mb_scored"]))
kst = []
for f in FOOTS:
    for m in mbs:
        kst.append((ei(float(m), f)[0] / ((1 - FB0) * m / FB0), m, f))
k_min = min(kst)
check("R0 (reported) the inertness margin k* = min M_ph,edge / [(1 - f_b) M_b / f_b] over every scored object's M_b (all variants; SLUGGS solver trial masses excluded) and both footings",
      f"{len(mbs)} M_b values ({mbs.min():.2e}-{mbs.max():.2e}); k* = {k_min[0]:.2f} at M_b = {k_min[1]:.2e} ({k_min[2]}); the native leftover switches on only if the cold share were {k_min[0]:.1f}x larger", True, load_bearing=False)
R.num("inertness_margin", dict(k_min=k_min[0], Mb=k_min[1], foot=k_min[2], n_Mb=len(mbs), Mb_range=[float(mbs.min()), float(mbs.max())]))

# ================================================================================================ H1 prediction
R.banner("H1  THE PRE-FLIGHT PREDICTION: under the native mass f_ex = 0 everywhere, so every native rule row equals the law")
for vn in ("native_V1", "native_V2"):
    b = MODES[vn]; dd = []
    for rid, lab, gt, _, _ in ROWS:
        for f in FOOTS:
            (oL, zL), (oS, zS) = gt(b, f, "L"), gt(b, f, "S")
            dd.append((f"{rid} {f}", max(abs(oL - oS), abs(zL - zS))))
    for kind in ("dwarf", "spiral"):
        dd.append((f"SPARC {kind} max d log v", abs(b["SP"][(kind, "S")]["max"])))
    dd.append(("CFG39 rms change", abs(b["C39"]["rms1"] - b["C39"]["rms0"])))
    w = max(dd, key=lambda t: t[1])
    check(f"H1 [{vn}] every native rule row equals the law row to 1e-9 (f_ex = 0 for every object)" + ("  [MUTATE run: f_b unchanged here]" if MUTATE else ""),
          f"{len(dd)} comparisons; worst {w[0]}: {w[1]:.1e}; SPARC galaxies touched: {b['C39']['touched']}", w[1] <= 1e-9)

# ================================================================================================ the table
R.banner("THE TABLE: offset [dex] and z, canonical | alt -- law alone (L), committed rule (Moster/Mandelbaum + NFW), native rule V1 (NFW), V2 (isothermal)")
COMM = MODES.get("committed")
c45 = J("CFG45_rule_readings_results.json"); c58 = J("CFG58_rule_more_populations_results.json")
c55 = J("CFG55_sluggs_dynamical_masses_results.json")["RES"]; c111 = J("CFG111_sluggs_literature_gamma_results.json")["RES"]


def committed_row(rid, gt, f):
    """the committed rule's (offset, z) from the committed result files (independent of this run)."""
    if rid == "P1": v = c45["UF"][f"{f}|S"]; return v["km"], v["z"]
    if rid in ("P2a", "P2b", "P2c"):
        v = c45["CL"][f"{dict(P2a='cls', P2b='col', P2c='m31')[rid]}|{f}|S"]; return v["med"], v["z"]
    if rid == "P2d": v = c58["field_dwarfs"][f"{f}|S"]; return v["med"], v["z"]
    if rid == "P4a": v = c45["UGC2487"][f"{f}|S"]; return v["off"], v["z"]
    if rid == "P4b": v = c45["DT23"][f"{f}|S"]; return v["s0"]["corr"], v["s0z"]
    if rid == "P4b'": v = c45["DT23"][f"{f}|S"]["all"]; return v["corr"], v["z"]
    if rid == "P5": v = c45["SLUGGS"][f"{f}|S"]; return v["mean"], v["z"]
    if rid == "P5J": v = c55[f]["rule"]; return v["mean"], v["mean"] / v["err"]
    if rid == "P5S": v = c55[f]["rule_sluggs"]; return v["mean"], v["mean"] / v["err"]
    if rid == "P5L": v = c111[f]["rule"]; return v["mean"], v["mean"] / v["err"]
    if rid == "P6": v = c45["XRAY"][f"{f}|S"]; return v["mean"], v["z"]
    if rid == "P7": v = c45["OGLE"][f"{f}|S"]; return v["mean"], v["z"]


V1, V2 = MODES["native_V1"], MODES["native_V2"]
fmt = lambda oz_c, oz_a: f"{oz_c[0]:+.3f} ({oz_c[1]:+.2f}|{oz_a[1]:+.2f})"
P(f"    {'population':38s} {'law alone':>24s} {'committed rule':>24s} {'native rule V1':>24s} {'native rule V2':>24s}  gate")
TABLE = {}
MOVES = {"V1": [], "V2": []}
for rid, lab, gt, gate, gname in ROWS:
    L = {f: gt(V1, f, "L") for f in FOOTS}; Cm = {f: committed_row(rid, gt, f) for f in FOOTS}
    N1 = {f: gt(V1, f, "S") for f in FOOTS}; N2 = {f: gt(V2, f, "S") for f in FOOTS}
    pc = {k: gate(d["canonical"][1], d["alt"][1]) for k, d in (("law", L), ("committed", Cm), ("V1", N1), ("V2", N2))}
    TABLE[rid] = dict(label=lab, gate=gname, law=L, committed=Cm, native_V1=N1, native_V2=N2, passes=pc)
    P(f"    {rid + ' ' + lab:38s} {fmt(L['canonical'], L['alt']):>24s} {fmt(Cm['canonical'], Cm['alt']):>24s} {fmt(N1['canonical'], N1['alt']):>24s} "
      f"{fmt(N2['canonical'], N2['alt']):>24s}  {gname}: law {'P' if pc['law'] else 'F'} / comm {'P' if pc['committed'] else 'F'} / V1 {'P' if pc['V1'] else 'F'} / V2 {'P' if pc['V2'] else 'F'}")
    for v in ("V1", "V2"):
        if pc["committed"] != pc[v] and "reported" not in gname:
            MOVES[v].append(f"{rid} {lab}: {'FAIL -> PASS' if pc[v] else 'PASS -> FAIL'}")
for kind, lab in (("dwarf", "SPARC dwarfs, d log v < 0.03 (A3)"), ("spiral", "SPARC log M* >= 10, d log v < 0.03 (A3)")):
    cm = c45["SPARC"][f"{kind}|S"]
    P(f"    {'P3 ' + lab:38s} law {100 * V1['SP'][(kind, 'L')]['frac_lt003']:.0f}% | committed {100 * cm['frac_lt003']:.0f}% (max {cm['max']:.3f}) | V1 {100 * V1['SP'][(kind, 'S')]['frac_lt003']:.0f}% "
      f"(max {V1['SP'][(kind, 'S')]['max']:.3f}) | V2 {100 * V2['SP'][(kind, 'S')]['frac_lt003']:.0f}% (max {V2['SP'][(kind, 'S')]['max']:.3f})")
    TABLE["P3 " + kind] = dict(law=V1["SP"][(kind, "L")]["frac_lt003"], committed=cm["frac_lt003"], committed_max=cm["max"], V1=V1["SP"][(kind, "S")]["frac_lt003"],
                               V1_max=V1["SP"][(kind, "S")]["max"], V2=V2["SP"][(kind, "S")]["frac_lt003"], V2_max=V2["SP"][(kind, "S")]["max"])
c39 = J("CFG39_harness_with_rule_results.json")["sparc"]
P(f"    {'P8 SPARC rms (CFG39, canonical)':38s} law {V1['C39']['rms0']:.4f} | committed {c39['rms1']:.4f} ({c39['rms1'] - c39['rms0']:+.4f}) | V1 {V1['C39']['rms1']:.4f} "
  f"({V1['C39']['rms1'] - V1['C39']['rms0']:+.4f}) | V2 {V2['C39']['rms1']:.4f} ({V2['C39']['rms1'] - V2['C39']['rms0']:+.4f})")
TABLE["P8"] = dict(law=V1["C39"]["rms0"], committed=c39["rms1"], V1=V1["C39"]["rms1"], V2=V2["C39"]["rms1"])
if "native_V1_floor_verbatim" in MODES:
    vb = MODES["native_V1_floor_verbatim"]
    P(f"    reported: P1 with the committed floor VALUES (1e8..1e10, not native) in the error: z {vb['UF'][('canonical', 'S')]['z']:+.2f}|{vb['UF'][('alt', 'S')]['z']:+.2f} "
      f"(KM median {vb['UF'][('canonical', 'S')]['km']:+.3f} +- {vb['UF'][('canonical', 'S')]['tot']:.3f})")
    TABLE["P1_floor_verbatim"] = {f: dict(km=vb["UF"][(f, "S")]["km"], tot=vb["UF"][(f, "S")]["tot"], z=vb["UF"][(f, "S")]["z"]) for f in FOOTS}

check("H2 (reported) moves against the committed rule (gated rows)", "V1: " + ("; ".join(MOVES["V1"]) or "none") + " || V2: " + ("; ".join(MOVES["V2"]) or "none"),
      True, load_bearing=False)
gp = {v: [rid for rid, d in TABLE.items() if isinstance(d, dict) and "passes" in d and "reported" not in d["gate"] and d["passes"][v]] for v in ("law", "committed", "V1", "V2")}
ng = sum(1 for d in TABLE.values() if isinstance(d, dict) and "passes" in d and "reported" not in d["gate"])
check("H3 (reported) gated rows passed (P3 and P8 separately: all pass under every column)", "; ".join(f"{k}: {len(v)}/{ng} ({', '.join(v)})" for k, v in gp.items()), True, load_bearing=False)

# ================================================================================================ MUTATE
if MUTATE:
    R.banner("MUTATE: f_b x 0.5 -- does every population's rule statistic shift in the predicted direction (offsets fall)?")
    M = MODES["native_V1_fbhalf"]; sh = []
    for rid, lab, gt, gate, gname in ROWS:
        for f in FOOTS:
            sh.append((f"{rid} {f}", gt(M, f, "S")[0] - gt(V1, f, "S")[0]))
    sp = [(f"SPARC {k} max", M["SP"][(k, "S")]["max"] - V1["SP"][(k, "S")]["max"]) for k in ("dwarf", "spiral")]
    ok = all(d < -1e-6 for _, d in sh) and all(d > 1e-6 for _, d in sp)
    check("MUTATE CHECK (as specified; the pre-flight predicts FAIL): with f_b x 0.5 every population's rule offset falls by > 1e-6 dex and SPARC's max d log v rises",
          "largest |shift| " + f"{max(abs(d) for _, d in sh + sp):.1e} dex; " + "; ".join(f"{a}: {d:+.1e}" for a, d in sh[:6]) + " ...", ok)
    R.num("mutate_shifts", dict(sh + sp))


def jkeys(d):
    if isinstance(d, dict):
        return {("|".join(map(str, k)) if isinstance(k, tuple) else str(k)): jkeys(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)):
        return [jkeys(x) for x in d]
    return d


for k, b in MODES.items():
    R.num(f"mode_{k}", jkeys({kk: vv for kk, vv in b.items() if kk != "C39"} | {"C39": {kk: vv for kk, vv in b["C39"].items()}}))
R.num("TABLE", jkeys(TABLE)); R.num("MOVES", MOVES); R.num("f_b", FB0)
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
