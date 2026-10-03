#!/usr/bin/env python3
"""CFG303 R3/R5 -- MUSE-DARK implied a0 in z-thirds (CFG262) with the halo-fit inputs removed from the baryon side.
CFG262's routes (ii)/(iii) are built in CFG236's R199 construction: g_bar = (1 - f_DM) g_perp rho, rho normalised by the DC14 M_fit and the
fitted Sigma_HI (LCDM-MODEL).  Here: g_bar,nat = CFG236's thin disc g_disc(M, R_e, R_e/1.678) with M = M*_SED (iii) or M*_SED (1 + mu_mol) (ii),
no HI (primary; the fitted Sigma_HI is a joint-fit nuisance), and g_obs = CFG262's g_perp (the DC14 model slit velocity at R_e; MODEL-OTHER,
halo_in_fit = yes; no measured MUSE-DARK velocity is on disk).  CFG262's own s_star / boot_s / pct / thirds, exec'd from its committed source.
Frozen criteria: FROZEN_CRITERIA.md (52976ec22) + ADDENDUM_1 + ADDENDUM_2 (section A2.2), written before any native MUSE-DARK number was computed.
kappa = 1/2 FITTED.  The cold mass is still required; no dark-matter particle is added.  No sentence here says the data favour a law.
Run:  python3 campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_musedark_LCDMFREE.py      (needs the MUSE-DARK DC14 run files beside the repo, as CFG262)
Outputs: cfg303_musedark_LCDMFREE.out, cfg303_musedark_LCDMFREE_results.json (this lane only).
"""
import os, sys, io, json, math, contextlib, time, hashlib
sys.dont_write_bytecode = True
import numpy as np

T0 = time.time()
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
for k in ("MUTATE", "SELFTEST"):
    os.environ.pop(k, None)
OUT, CHK = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


P(__doc__.split("Run:")[0].strip())
for f in ("FROZEN_CRITERIA.md", "FROZEN_CRITERIA_ADDENDUM_1.md", "FROZEN_CRITERIA_ADDENDUM_2.md"):
    P(f"  {f}: sha256 {sha(os.path.join(LANE, f))}")
F262 = os.path.join(CFG, "CFG262_musedark_zthirds_by_route", "cfg262_musedark_zthirds.py")
src = open(F262).read()
STOP = "# ================================================================== STAGE A"
assert src.count(STOP) == 1
os.environ["STAGE"] = "B"
ns = {"__file__": F262, "__name__": "cfg303_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(STOP)], "cfg262[upto STAGE A]", "exec"), ns)
os.environ.pop("STAGE", None)
P(f"  CFG262 (sha {sha(F262)[:12]}) exec'd up to its stage-A block; S = {ns['NG']} galaxies")
c, C, THN, ZMED, ROUTES, CONV = ns["c"], ns["C"], ns["THN"], ns["ZMED"], ns["ROUTES"], ns["CONV"]
gperp_of, routes_of, s_star, boot_s, pct, s_of, LAWS = ns["gperp_of"], ns["routes_of"], ns["s_star"], ns["boot_s"], ns["pct"], ns["s_of"], ns["LAWS"]
J = json.load(open(os.path.join(CFG, "CFG262_musedark_zthirds_by_route", "cfg262_stageB_results.json")))["numbers"]
JR = J["rows"]


def level(D, gb, label):
    ok = np.isfinite(D) & np.isfinite(gb) & (gb > 0) & (D > 0)
    D, gb = D[ok], gb[ok]
    ls0, u0 = s_star(D, gb)
    lsb, ub = boot_s(D, gb, label)
    itv = pct(lsb); itv["unb_frac"] = float(ub.mean()); itv["sd"] = float(lsb.std())
    return dict(n=int(ok.sum()), ls=ls0, s=s_of(ls0, u0), no_root=u0, itv=itv, median_D=float(np.median(D)), n_D_lt1=int((D < 1).sum()),
                y_med=float(np.median(gb / 9.3603e-11)))


# ================================================================== C-ii / C-i
P("\nCONTROLS")
RO = {rd: routes_of(gperp_of(rd)) for rd in ("bD", "b")}
dmax, dmax_i = 0.0, 0.0
for rd in ("bD", "b"):
    for r in ROUTES:
        for k, t in THN.items():
            lab = f"{k}-route{r}-{rd}"
            D = RO[rd]["D_" + r][t]; gb = RO[rd]["gb_" + r][t] * CONV
            L = level(D, gb, lab)
            cm = JR[lab]
            dmax = max(dmax, abs(L["ls"] - cm["ls"]), abs(L["itv"]["lo95"] - cm["itv"]["lo95"]), abs(L["itv"]["hi95"] - cm["itv"]["hi95"]))
            gp = gperp_of(rd)[t]
            Li = level(gp / RO[rd]["gb_" + r][t], gb, lab)                 # the native formula D = g_perp / g_bar fed the committed g_bar
            dmax_i = max(dmax_i, abs(Li["ls"] - cm["ls"]), abs(Li["itv"]["lo95"] - cm["itv"]["lo95"]))
check("C-ii CFG262's exec'd machinery reproduces the committed stage-B s* and 95% edges of all 18 rows", f"max |diff| {dmax:.1e} (log10)", dmax <= 1e-9)
check("C-i the native formula D = g_perp / g_bar fed the committed (R199) g_bar reproduces the committed rows", f"max |diff| {dmax_i:.1e}", dmax_i <= 1e-9)

# ================================================================== native rows
P("\nNATIVE ROWS (g_bar = thin disc of M*_SED [route iii] or M*_SED (1 + mu_mol) [route ii]; g_obs = CFG262's g_perp)")
VAR = {"noHI (primary)": dict(Sig=0.0), "HI Sigma 15 (prior ceiling)": dict(Sig=15.0), "HI fitted (as committed; joint-fit nuisance)": dict()}
RES = {}
for vn, cfgv in VAR.items():
    Rn = c.routes(C, dict(mode="R198", **cfgv))
    for rd in ("bD", "b"):
        gp_all = gperp_of(rd)
        for r in ("iii", "ii"):
            for k, t in THN.items():
                lab = f"{k}-route{r}-{rd}"
                gbk = Rn["gb_" + r][t]
                L = level(gp_all[t] / gbk, gbk * CONV, "CFG303|" + vn + "|" + lab)
                L["z"] = ZMED[k]
                L["flags95"] = {Lw: bool(s_of(L["itv"]["lo95"], False) <= fn(ZMED[k]) <= s_of(L["itv"]["hi95"], False)) for Lw, fn in LAWS.items()}
                RES[f"{vn}|{lab}"] = L
DIF = {}
for vn in VAR:
    for rd in ("bD", "b"):
        for r in ("iii", "ii"):
            a, b = RES[f"{vn}|z3-route{r}-{rd}"], RES[f"{vn}|z1-route{r}-{rd}"]
            DIF[f"{vn}|{rd}|{r}"] = None if (a["no_root"] or b["no_root"]) else dict(d=a["ls"] - b["ls"], sd=math.hypot(a["itv"]["sd"], b["itv"]["sd"]),
                                                                                   rival=math.log10(LAWS["H(z)"](ZMED["z3"]) / LAWS["H(z)"](ZMED["z1"])))


def fmt(L):
    return ("NO ROOT" if L["no_root"] else f"{L['s']:.3f}") + f" [{s_of(L['itv']['lo95'], False):.2f}, {s_of(L['itv']['hi95'], False):.2f}]"


for rd in ("bD", "b"):
    P(f"  reading {rd}:")
    for r in ("i", "ii", "iii"):
        P(f"    committed route ({r:3s}): " + " / ".join(fmt(JR[f'{k}-route{r}-{rd}'] | {'no_root': JR[f'{k}-route{r}-{rd}']['no_root']}) for k in THN)
          + (f";  z3 - z1 {J['diff'][f'{rd}|{r}']['d']:+.3f} +- {J['diff'][f'{rd}|{r}']['sd']:.3f}" if J["diff"].get(f"{rd}|{r}") else ""))
    for vn in VAR:
        for r in ("ii", "iii"):
            d_ = DIF[f"{vn}|{rd}|{r}"]
            P(f"    NATIVE {vn:44s} route ({r:3s}): " + " / ".join(fmt(RES[f'{vn}|{k}-route{r}-{rd}']) for k in THN)
              + (f";  z3 - z1 {d_['d']:+.3f} +- {d_['sd']:.3f} (H(z) expects {d_['rival']:+.3f}; FLAT 0)" if d_ else ";  z3 - z1 not formed (a third has no root)")
              + ";  median D " + "/".join(f"{RES[f'{vn}|{k}-route{r}-{rd}']['median_D']:.2f}" for k in THN)
              + ";  D<1 " + "/".join(f"{RES[f'{vn}|{k}-route{r}-{rd}']['n_D_lt1']}" for k in THN))
fl = {Lw: sum(RES[f"noHI (primary)|{k}-route{r}-bD"]["flags95"][Lw] for k in THN for r in ("ii", "iii")) for Lw in LAWS}
P("  primary native (no HI, reading bD): the law's expected s* inside the 95% interval in " + ", ".join(f"{Lw} {v}/6" for Lw, v in fl.items()) + " rows (routes ii + iii x thirds)")

# ================================================================== MUTATE
P("\nC-iii MUTATE: M*_SED x 10^0.2 (route iii, no HI, reading bD)")
R0 = c.routes(C, dict(mode="R198", Sig=0.0)); R1 = c.routes(C, dict(mode="R198", Sig=0.0, off=-0.2))
gp = gperp_of("bD")
okm, lines = True, []
for k, t in THN.items():
    D0 = gp[t] / R0["gb_iii"][t]; D1 = gp[t] / R1["gb_iii"][t]
    sh = np.log10(D1) - np.log10(D0)
    okD = np.allclose(sh[np.isfinite(sh)], -0.2, atol=1e-12, rtol=0)
    L0 = level(D0, R0["gb_iii"][t] * CONV, "CFG303|mut0|" + k); L1 = level(D1, R1["gb_iii"][t] * CONV, "CFG303|mut1|" + k)
    dn = (L0["no_root"] and L1["no_root"]) or L1["no_root"] or (L1["ls"] < L0["ls"])
    okm &= okD and dn
    lines.append(f"{k}: log D -0.2 exact {okD}; s* {fmt(L0)} -> {fmt(L1)}")
P("  " + "; ".join(lines))
check("C-iii MUTATE: route (iii) log D moves by -0.2000 exactly and s* moves down or loses its root in every third", "see line above", okm)
npass = sum(CHK)
P(f"\n{npass}/{len(CHK)} checks pass   ({time.time() - T0:.0f} s)")


def jc(o):
    if isinstance(o, dict):
        return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    return o


json.dump(jc(dict(rows=RES, diff=DIF, flags_primary=fl, committed_rows={k: dict(s=v["s"], ls=v["ls"], no_root=v["no_root"], itv=v["itv"]) for k, v in JR.items()},
                  committed_diff=J["diff"], checks=dict(passed=npass, n=len(CHK)))),
          open(os.path.join(LANE, "cfg303_musedark_LCDMFREE_results.json"), "w"), indent=1)
open(os.path.join(LANE, "cfg303_musedark_LCDMFREE.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
