#!/usr/bin/env python3
"""CFG520 part B (FROZEN_CRITERIA.md section 5; criteria commit 6d184c37d): CFG502 / CFG503 re-scored with the measured leaked-satellite
fraction f_obs = 0.2234 (CFG519) in place of their HOD value, everything else unchanged.

f' = clip(s f, 0, 1), s = 0.2234 / X (X = the value CFG519 compared against: CFG502 0.17122, CFG503 Moster 0.18056; CFG503 Behroozi: its own
stack-weighted value, CFG506's convention). E rebuilt from each lane's own pieces (check B0). CFG502: own = committed model - committed E
(check B1). CFG503: CFG506's scoring function (check B2); f' in E and in the own mixing (primary), E-only reported. Constant f' = 0.2234 reported.
Run: nice -n 10 python3 cfg520_partB.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import json, time
import numpy as np
from scipy import stats
from scipy.interpolate import RegularGridInterpolator

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, os.path.join(LANES, "CFG495_drawdown_shell"))
import cfg495_lenslib as LL                                                  # noqa: E402  (read-only)

EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
FOOTS = ("canonical", "alt")
F_OBS = 0.22342746446430256
X502, X503M = 0.17122385594807057, 0.1805564701196465
LOG, CHK = [], {}
RES = {"lane": "CFG520", "script": "cfg520_partB", "f_obs": F_OBS}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2


def esd_full_loo(WG, WW, patch, mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev


def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)


def pstack(tab, gi, WW, mask):
    NG = tab.shape[0]; out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out


ET = np.load(os.path.join(EXT, "cfg503_work", "cfg503_env_table.npz"))
E2 = np.load(os.path.join(EXT, "cfg502_work", "cfg502_env_table.npz"))
OT = np.load(os.path.join(EXT, "cfg503_work", "cfg503_own_tables.npz"))
LMS, ZG, RG = ET["LMS"], ET["ZG"], ET["RG"]; LRG = np.log(RG)
assert np.array_equal(LMS, E2["LMS"]) and np.array_equal(ZG, E2["ZG"]) and np.array_equal(RG, E2["RG"])
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
nL = len(lens["z"]); ALLM = np.ones(nL, bool)
gi, GM, GZ, GS = OT["gi"], OT["GM"], OT["GZ"], OT["GS"]; NG = len(GM)
d, Cv = esd_full_loo(WG, WW, patch, ALLM)
J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
dref = np.array(J377["primary"]["esd"]); Rm = np.array(J377["primary"]["meanR"])
check("C1 stack P data vector = CFG377 primary", np.max(np.abs(d / dref - 1)) < 1e-10, f"max rel {np.max(np.abs(d / dref - 1)):.1e}")
INN = Rm <= 0.445; OUTB = ~INN


def grid_interp(tab):
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    return f(np.c_[np.clip(GS, LMS[0], LMS[-1]), np.clip(GZ, ZG[0], ZG[-1])])


def evec(Etab):
    Eg = grid_interp(Etab); out = np.zeros((NG, 15))
    for g in range(NG):
        out[g] = LL.finish(lambda R, e=Eg[g]: np.interp(np.log(R), LRG, e), GM[g])
    return out


def f_stack(fg):
    return float(pstack(np.repeat(np.clip(grid_interp(fg), 0, 1)[:, None], 15, 1), gi, WW, ALLM)[0])


def relmax(a, b): return float(np.max(np.abs(a - b) / (np.abs(b) + 1e3)))


# ================================================================= CFG502
P("\n=============== CFG502 (E = HOLE + (1 - f) b_c T2h + f (T_host + b_h T2h); data-only chi2, Hartlap 15/9/6) ===============")
f2 = E2["W10_f"]


def E502(fg):
    f = np.clip(fg, 0, 1)[..., None]
    return E2["HOLE"] + (1 - f) * E2["W10_bc"][..., None] * E2["S2H"] + f * (E2["W10_Thost"] + E2["W10_bh"][..., None] * E2["S2H"])


b0 = relmax(E502(f2), E2["E_W10"])
check("B0 [CFG502] f' = f rebuilds the committed E_W10 table (1e-9 rel, 1e3 floor)", b0 < 1e-9, f"{b0:.1e}")
J502 = json.load(open(os.path.join(LANES, "CFG502_two_halo_first_principles", "cfg502_score_results.json")))["MAIN"]
E10_old = np.array(J502["E_W10"])
E10_re = pstack(evec(E2["E_W10"]), gi, WW, ALLM)
MODELS = ("LCDM", "LAW_RTA", "EDGE", "V1", "F_DD", "F_NODD", "LAW_X05")


def chi2(dv, C_, h, m):
    r = dv - m; return float(h * r @ np.linalg.inv(C_) @ r)


def sc502(Evec):
    out = {}
    for foot in FOOTS:
        out[foot] = {}
        for m in MODELS:
            own = np.array(J502[foot][m]["model"]) - E10_old
            mv = own + Evec
            out[foot][m] = dict(chi2=chi2(d, Cv, hart(15), mv), chi2_inner9=chi2(d[INN], Cv[np.ix_(INN, INN)], hart(9), mv[INN]),
                                chi2_outer6=chi2(d[OUTB], Cv[np.ix_(OUTB, OUTB)], hart(6), mv[OUTB]))
            out[foot][m]["p"] = float(stats.chi2.sf(out[foot][m]["chi2"], 15))
    return out


S_old = sc502(E10_re)
dv = max(abs(S_old[f][m]["chi2"] - J502[f][m]["chi2"]) for f in FOOTS for m in MODELS)
check("B1 [CFG502] with f' = f (E re-stacked here) the code reproduces CFG502's 14 stack-P chi2 within 0.01", dv <= 0.01,
      f"max |d| {dv:.4f}; re-stacked E vs committed E max |d| {np.max(np.abs(E10_re - E10_old)):.2e} Msun/pc^2")
s2 = F_OBS / X502
VAR502 = {"scaled": E502(s2 * f2), "constant": E502(np.full_like(f2, F_OBS))}
R502 = {"scale": s2, "old": S_old, "E_old": E10_re.tolist()}
for nm, Et in VAR502.items():
    Ev = pstack(evec(Et), gi, WW, ALLM)
    S_ = sc502(Ev)
    R502[nm] = dict(E=Ev.tolist(), scores=S_)
    P(f"\n  [{nm}{' (primary, s = %.4f)' % s2 if nm == 'scaled' else ' (reported)'}]")
    P("    R [Mpc]  : " + " ".join(f"{x:6.3f}" for x in Rm))
    P("    E old    : " + " ".join(f"{x:6.3f}" for x in E10_re))
    P("    E new    : " + " ".join(f"{x:6.3f}" for x in Ev))
    for foot in FOOTS:
        P(f"    [{foot}] model    | chi2/15 old -> new (dchi2) | p new    | inner9 old -> new | outer6 old -> new")
        for m in MODELS:
            o, n_ = S_old[foot][m], S_[foot][m]
            P(f"      {m:8s} | {o['chi2']:7.2f} -> {n_['chi2']:7.2f} ({n_['chi2'] - o['chi2']:+7.2f}) | {n_['p']:.2e} | "
              f"{o['chi2_inner9']:6.2f} -> {n_['chi2_inner9']:6.2f} | {o['chi2_outer6']:6.2f} -> {n_['chi2_outer6']:6.2f}")
    P(f"    CFG502 gate (LCDM p > 0.01 on 15 bins) with f': {'PASS' if S_['canonical']['LCDM']['p'] > 0.01 else 'FAIL'} "
      f"(chi2 {S_['canonical']['LCDM']['chi2']:.2f}, p {S_['canonical']['LCDM']['p']:.2e})")
RES["CFG502"] = R502

# ================================================================= CFG503
P("\n=============== CFG503 (nonlinear 2h + stripping + SHMR rank-one; CFG506's scoring function) ===============")


def own_group(foot, model, shmr, fgrid):
    f = np.clip(grid_interp(fgrid), 0, 1)[:, None]
    def one(m):
        base = f"P|{foot}|{m}|"
        return (1 - f) * OT[base + f"full_{shmr}"] + f * OT[base + f"tr_{shmr}_W10"]
    if model == "F_DD":
        return one("F_NODD") + one("PROP")
    return one(model)


def chi2c(dv_, C_, h, m, extra=None):
    Ct = C_ / h + (extra if extra is not None else 0.0)
    r = dv_ - m
    return float(r @ np.linalg.solve(Ct, r))


def score_rows(Evec_m, Evec_b, fgrid_m, fgrid_b):
    out = {}
    for foot in FOOTS:
        out[foot] = {}
        for mdl in MODELS:
            mM = pstack(own_group(foot, mdl, "moster", fgrid_m) + Evec_m, gi, WW, ALLM)
            mB = pstack(own_group(foot, mdl, "behroozi", fgrid_b) + Evec_b, gi, WW, ALLM)
            dl = mB - mM; ex = np.outer(dl, dl)
            c15 = chi2c(d, Cv, hart(15), mM, ex)
            ci = chi2c(d[INN], Cv[np.ix_(INN, INN)], hart(9), mM[INN], ex[np.ix_(INN, INN)])
            out[foot][mdl] = dict(chi2=c15, p=float(stats.chi2.sf(c15, 15)), chi2_inner9=ci, p_inner9=float(stats.chi2.sf(ci, 9)),
                                  chi2_data_only=chi2c(d, Cv, hart(15), mM))
    return out


J503 = json.load(open(os.path.join(LANES, "CFG503_two_halo_nonlinear", "cfg503_score_results.json")))["MAIN"]
XF = {}
for shmr in ("moster", "behroozi"):
    f = ET[f"{shmr}_W10_f"]; E = ET[f"E_{shmr}_nlz_W10"]; H = ET[f"{shmr}_HOLE"]; S2 = ET[f"{shmr}_S2H_nlz"]; bc = ET[f"{shmr}_W10_bc"]
    assert np.all(f > 0)
    XF[shmr] = (E - H - bc[..., None] * S2) / f[..., None]
    reb = H + bc[..., None] * S2 + f[..., None] * XF[shmr]
    check(f"B0 [CFG503 {shmr}] f' = f rebuilds the committed E_nlz_W10 table (1e-9 rel, 1e3 floor)", relmax(reb, E) < 1e-9, f"{relmax(reb, E):.1e}")


def E503(shmr, fg):
    return ET[f"{shmr}_HOLE"] + ET[f"{shmr}_W10_bc"][..., None] * ET[f"{shmr}_S2H_nlz"] + np.clip(fg, 0, 1)[..., None] * XF[shmr]


fm, fb = ET["moster_W10_f"], ET["behroozi_W10_f"]
xm, xb = f_stack(fm), f_stack(fb)
P(f"  stack-weighted f (CFG506 convention): Moster {xm:.5f} (CFG519 used {X503M:.5f}), Behroozi {xb:.5f}")
Em0, Eb0 = evec(ET["E_moster_nlz_W10"]), evec(ET["E_behroozi_nlz_W10"])
S3_old = score_rows(Em0, Eb0, fm, fb)
dv = max(abs(S3_old[f][m]["chi2"] - J503["P"][f][m]["chi2"]) for f in FOOTS for m in MODELS)
check("B2 [CFG503] with f' = f the scoring reproduces CFG503's 14 stack-P chi2 within 0.01", dv <= 0.01, f"max |d| {dv:.4f}")
di = max(abs(S3_old[f][m]["chi2_inner9"] - J503["P"][f][m]["chi2_inner9"]) for f in FOOTS for m in MODELS)
P(f"  (reported) inner-9 vs CFG503's committed inner-9: max |d| {di:.3f} (CFG503's inner-9 convention may differ)")
sM, sB = F_OBS / X503M, F_OBS / xb
fm2, fb2 = np.clip(sM * fm, 0, 1), np.clip(sB * fb, 0, 1)
fc = np.full_like(fm, F_OBS)
VAR503 = {"scaled (primary: E and own mixing)": (E503("moster", fm2), E503("behroozi", fb2), fm2, fb2),
          "scaled, E only (reported)": (E503("moster", fm2), E503("behroozi", fb2), fm, fb),
          "constant 0.2234 (reported)": (E503("moster", fc), E503("behroozi", fc), fc, fc)}
R503 = {"scale_moster": sM, "scale_behroozi": sB, "f_stack_moster": xm, "f_stack_behroozi": xb, "old": S3_old,
        "E_old": pstack(Em0, gi, WW, ALLM).tolist()}
for nm, (Emt, Ebt, fgm, fgb) in VAR503.items():
    Emv, Ebv = evec(Emt), evec(Ebt)
    S_ = score_rows(Emv, Ebv, fgm, fgb)
    R503[nm] = dict(E=pstack(Emv, gi, WW, ALLM).tolist(), scores=S_, f_stack_new=f_stack(fgm))
    P(f"\n  [{nm}] s_M = {sM:.4f}, s_B = {sB:.4f}; new stack-weighted f (Moster) {f_stack(fgm):.4f}")
    P("    E old    : " + " ".join(f"{x:6.3f}" for x in R503["E_old"]))
    P("    E new    : " + " ".join(f"{x:6.3f}" for x in R503[nm]["E"]))
    for foot in FOOTS:
        P(f"    [{foot}] model    | chi2/15 old -> new (dchi2) | p new    | inner9 old -> new (dchi2)")
        for m in MODELS:
            o, n_ = S3_old[foot][m], S_[foot][m]
            P(f"      {m:8s} | {o['chi2']:7.2f} -> {n_['chi2']:7.2f} ({n_['chi2'] - o['chi2']:+7.2f}) | {n_['p']:.2e} | "
              f"{o['chi2_inner9']:6.2f} -> {n_['chi2_inner9']:6.2f} ({n_['chi2_inner9'] - o['chi2_inner9']:+6.2f})")
    P(f"    CFG503 G1 (LCDM stack P p > 0.01, 15 bins) with f': {'PASS' if S_['canonical']['LCDM']['p'] > 0.01 else 'FAIL'} "
      f"(chi2 {S_['canonical']['LCDM']['chi2']:.2f}, p {S_['canonical']['LCDM']['p']:.2e})")
RES["CFG503"] = R503
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, "cfg520_partB_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg520_partB.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
