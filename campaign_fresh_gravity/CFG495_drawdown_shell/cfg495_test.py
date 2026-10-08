#!/usr/bin/env python3
"""CFG495 Step 3: frozen three-way test on the on-disk KiDS isolated-lens stack (FROZEN_CRITERIA.md, committed alone first).

Models (per footing, never pooled), all with the SAME frozen two-halo term (S0-control environment, iso05, D(z)^2; never freed in the verdict):
  LCDM    = NFW (Moster+13 / Duffy+08, (U)) to r_ta + 2h
  F_nodd  = law to r_edge + undrawn cold fluid to r_ta + 2h
  F_dd    = F_nodd + the predicted drawdown (engine rule: proportional draw, PROP)          <- the prediction under test
  F_shell = F_nodd + outer-shell-only drawdown (reported variant)
  PILEUP  = F_nodd - PROP (MUTATE: opposite sign)
Data: CFG377's primary stack (181,477 lenses, 15 g_bar bins, 50-patch jackknife, Hartlap). Controls: random-position stack (cfg495_stage_random.py)
and the cross-shear stack (cfg116_perlens WX).  Outputs: cfg495_test.out / cfg495_test_results.json (CFG495_MUTATE=1: *_MUTATE.*, which runs the
null stacks as the data vector instead of the lens stack).
"""
import os, sys, json, math
import numpy as np
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
OUTW = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg495_work"))
MUTATE = os.environ.get("CFG495_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUTATE else ""
LOG = []
def P(s=""):
    print(s, flush=True); LOG.append(str(s))
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
np.set_printoptions(linewidth=220, precision=3, suppress=True)

NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
f30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)
T = np.load(os.path.join(OUTW, "cfg495_pred_tables.npz")); gi = T["gi"]; NG = len(T["GM"])
nL = len(gi)

def esd_full_loo(WGx, WWx, mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WGx[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WWx[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev
def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)
def pstack(tab, mask, WWx=WW):
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WWx[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out
def chi2(d, Ci, h, m): r = d - m; return float(h * r @ Ci @ r)
def ampfit(d, Ci, h, base, mu):
    """best amplitude A of mu on top of base; sigma_A; lambda = expected Delta chi^2 of the full template."""
    r = d - base; F = float(mu @ Ci @ mu)
    A = float(mu @ Ci @ r) / F; sA = 1 / math.sqrt(h * F)
    return A, sA, float(h * F)

def models(foot, mask, two="2h_iso05_D2", dl="", WWx=WW):
    sfx = "" if dl == "" else f"_dlogM{dl}"
    g = lambda n: pstack(T[f"{foot}_{n}{sfx}"], mask, WWx)
    two_v = pstack(T[two], mask, WWx) if two is not None else np.zeros(15)
    lc, no, pr, sh = g("lcdm"), g("nodd"), g("prop"), g("shell")
    return dict(LCDM=lc + two_v, F_nodd=no + two_v, F_dd=no + pr + two_v, F_shell=no + sh + two_v, PILEUP=no - pr + two_v,
                prop=pr, shell=sh, two=two_v)

def score(d, C, h, M):
    Ci = np.linalg.inv(C)
    out = {n: chi2(d, Ci, h, M[n]) for n in ("LCDM", "F_nodd", "F_dd", "F_shell", "PILEUP")}
    out["dchi2_dd_minus_nodd"] = out["F_dd"] - out["F_nodd"]
    out["dchi2_pileup_minus_nodd"] = out["PILEUP"] - out["F_nodd"]
    A, sA, lam = ampfit(d, Ci, h, M["F_nodd"], M["prop"])
    out.update(A_prop=A, sigA_prop=sA, lam_prop=lam,
               power2=float(stats.norm.cdf(math.sqrt(lam) - 2) + stats.norm.cdf(-math.sqrt(lam) - 2)))
    return out
def verdict_one(s):
    x = s["dchi2_dd_minus_nodd"]
    return "DETECTED" if x <= -4 else ("EXCLUDED" if x >= 4 else "NOT DIAGNOSTIC")

RES = dict(mutate=MUTATE, checks=CHK)
ALL = np.ones(nL, bool)
if not MUTATE:
    d, C = esd_full_loo(WG, WW, ALL); h = hart(15)
    Rm = np.array(json.load(open(os.path.join(HERE, "cfg495_predict_results.json")))["Rm"])
    ref = json.load(open(os.path.join(HERE, "..", "CFG377_kids_reservoir_dip", "cfg377_results.json")))["primary"]["esd"]
    check("C1 data vector = CFG377 primary", np.max(np.abs(d - np.array(ref))) < 1e-9, f"max dev {np.max(np.abs(d - np.array(ref))):.1e}")
    check("C2 15 bins, 181,477 lenses", len(d) == 15 and nL == 181477, f"{len(d)} bins, {nL} lenses")
    P(f"== primary stack: R [Mpc] {np.round(Rm, 3)}")
    P(f"   ESD data  {np.round(d, 3)}")
    P(f"   jk sigma  {np.round(np.sqrt(np.diag(C)), 3)}   Hartlap {h:.4f}")
    VER = {}
    for foot in ("canonical", "alt"):
        M = models(foot, ALL); s = score(d, C, h, M); VER[foot] = verdict_one(s)
        RES[foot] = dict(primary=s, vectors={k: v.tolist() for k, v in M.items()})
        P(f"\n== [{foot}] primary (frozen 2h iso05 D^2)")
        for n in ("LCDM", "F_nodd", "F_dd", "F_shell", "PILEUP"):
            P(f"   {n:8s} {np.round(M[n], 3)}  chi2 {s[n]:8.2f} /15")
        P(f"   drawdown PROP vector {np.round(M['prop'], 3)}; 2h {np.round(M['two'], 3)}")
        P(f"   Delta chi2 (F_dd - F_nodd) = {s['dchi2_dd_minus_nodd']:+.2f}; amplitude of PROP A = {s['A_prop']:.3f} +- {s['sigA_prop']:.3f} "
          f"(prediction A = 1; lambda {s['lam_prop']:.1f}, power 2 sigma {s['power2']:.3f}); PILEUP - F_nodd = {s['dchi2_pileup_minus_nodd']:+.2f}")
        P(f"   -> {VER[foot]}")
        # declared sensitivity rows (reported; enter the label only)
        SENS = {}
        for two in ("2h_iso1_D2", "2h_all_D2", "2h_iso05_D1", "2h_iso05_D0", None):
            SENS[f"2h={two}"] = score(d, C, h, models(foot, ALL, two=two))
        for dl in ("-0.2", "+0.2"):
            SENS[f"dlogM={dl}"] = score(d, C, h, models(foot, ALL, dl=dl))
        # free R^-0.8 amplitude (CFG377/413 floor; reported only, never the verdict)
        Ci = np.linalg.inv(C); tm = pstack(T["TT"], ALL)
        def prof(m):
            r = d - m; return float(h * (r @ Ci @ r - (tm @ Ci @ r) ** 2 / (tm @ Ci @ tm))), float((tm @ Ci @ r) / (tm @ Ci @ tm))
        M0 = models(foot, ALL, two=None)
        fr = {n: prof(M0[n]) for n in ("LCDM", "F_nodd", "F_dd", "F_shell", "PILEUP")}
        SENS["free_R08_2h"] = {n: dict(chi2=fr[n][0], A=fr[n][1]) for n in fr}
        SENS["free_R08_2h"]["dchi2_dd_minus_nodd"] = fr["F_dd"][0] - fr["F_nodd"][0]
        # trusted 9 inner bins (R <= 0.445 Mpc) and f30 strict isolation
        inn = Rm <= 0.445
        di, Cii = d[inn], C[np.ix_(inn, inn)]; hi = hart(int(inn.sum()))
        Mi = {k: v[inn] for k, v in M.items()}; SENS["inner9"] = score(di, Cii, hi, Mi)
        d30, C30 = esd_full_loo(WG, WW, f30); SENS["f30"] = score(d30, C30, h, models(foot, f30))
        RES[foot]["sensitivity"] = SENS
        P(f"   sensitivity (Delta chi2 F_dd - F_nodd; A_prop +- sigma):")
        for k, v in SENS.items():
            if k == "free_R08_2h":
                P(f"     {k:22s}: {v['dchi2_dd_minus_nodd']:+8.2f}  (chi2 LCDM {v['LCDM']['chi2']:.1f} A {v['LCDM']['A']:.2f}; F_nodd {v['F_nodd']['chi2']:.1f} A {v['F_nodd']['A']:.2f}; "
                  f"F_dd {v['F_dd']['chi2']:.1f} A {v['F_dd']['A']:.2f})")
            else:
                P(f"     {k:22s}: {v['dchi2_dd_minus_nodd']:+8.2f}  A {v['A_prop']:.2f} +- {v['sigA_prop']:.2f}  (chi2 LCDM {v['LCDM']:.1f}, F_nodd {v['F_nodd']:.1f}, F_dd {v['F_dd']:.1f}, PILEUP {v['PILEUP']:.1f})")
        rob = [verdict_one(v) == VER[foot] for k, v in SENS.items() if k not in ("free_R08_2h", "inner9")]
        RES[foot]["robust_frac"] = float(np.mean(rob))
        P(f"   verdict holds in {np.sum(rob)}/{len(rob)} declared sensitivity rows (2h variants, halo mass +-0.2 dex, f30)")
    v = VER["canonical"] if VER["canonical"] == VER["alt"] else "NOT DIAGNOSTIC (footings split)"
    pile_bad = any(RES[f]["primary"]["dchi2_pileup_minus_nodd"] <= -4 for f in ("canonical", "alt"))
    label = []
    if pile_bad: label.append("PILE-UP PREFERRED: the data want more mass, not a drawdown; the test is not clean")
    if min(RES[f]["robust_frac"] for f in ("canonical", "alt")) < 1: label.append("NOT ROBUST to the declared 2h / halo-mass / isolation rows")
    pbest = {f: float(stats.chi2.sf(min(RES[f]["primary"][n] for n in ("LCDM", "F_nodd", "F_dd")), 15)) for f in ("canonical", "alt")}
    RES["p_best_frozen_model"] = pbest
    if min(pbest.values()) < 1e-3: label.append(f"MODEL-INADEQUATE (best frozen model p = {min(pbest.values()):.1e})")
    RES["verdict"] = dict(per_footing=VER, lane=v, labels=label)
    P(f"\nLANE VERDICT: {v}" + (f"  [{'; '.join(label)}]" if label else ""))
else:
    # null stacks: random positions and cross shear; the model under test is the drawdown alone (no halo there)
    RW = np.load(os.path.join(OUTW, "cfg495_random_perlens.npz"))
    WX = np.load(os.path.join(DATA, "cfg116_perlens.npz"))["WX"]
    h = hart(15)
    for name, WGx, WWx in (("random_positions", RW["WG"], RW["WW"]), ("cross_shear", WX, WW)):
        ok = WWx.sum(1) > 0
        d, C = esd_full_loo(WGx, WWx, ok); Ci = np.linalg.inv(C)
        RES[name] = {}
        P(f"== null stack [{name}]: {ok.sum()} lenses; ESD {np.round(d, 4)}")
        for foot in ("canonical", "alt"):
            M = models(foot, ok, WWx=WWx)
            A, sA, lam = ampfit(d, Ci, h, np.zeros(15), M["prop"])
            dchi = chi2(d, Ci, h, M["prop"]) - chi2(d, Ci, h, np.zeros(15))
            Ap, sAp, _ = ampfit(d, Ci, h, np.zeros(15), -M["prop"])
            RES[name][foot] = dict(A=A, sigA=sA, lam=lam, dchi2_drawdown_vs_zero=dchi, chi2_zero=chi2(d, Ci, h, np.zeros(15)))
            killed = abs(A / sA) < 2 and dchi > -4
            check(f"null {name} [{foot}] shows no drawdown", killed, f"A {A:+.3f} +- {sA:.3f} (lambda {lam:.0f}); Delta chi2(drawdown - zero) {dchi:+.1f}; chi2(zero) {RES[name][foot]['chi2_zero']:.1f}/15")
P(f"checks: {CHK}")
json.dump(RES, open(os.path.join(HERE, f"cfg495_test{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg495_test{TAG}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
