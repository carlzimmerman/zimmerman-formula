#!/usr/bin/env python3
"""CFG534 Test 1 (KiDS) and the KiDS part of Test 4 (FROZEN_CRITERIA.md, criteria commit aa8dc312e).
Machinery: CFG531's cfg531_kids.py exec'd read-only up to its 'EARLY = TYP == 1' line (which itself execs CFG529's scorer read-only):
data, CFG503 (M_gal, z) groups, LAW_RTA tables from the CFG531 cache, the validated f30 environment, comps / fit_eps / bands.
New: mass matching inside (group, bin) cells -- class-B lens weights x W_A,gk / W_B,gk, cells lacking either class dropped -- so the
two classes share identical stacked model vectors; the difference Delta d = d_A - d_B is fitted with the own stack (GLS, jackknife C).
Splits: 1a early vs late; 1b NUV-undetected vs detected (GALEX coverage only, CFG505 table); inside-type UV splits; per-tertile 1a.
MUTATE (CFG534_MUTATE=1 -> *_MUTATE.*): MU1 labels shuffled inside groups (type and NUV), MU2 injected Delta eps = 0.3.
Run: nice -n 10 python3 cfg534_kids.py ; CFG534_MUTATE=1 nice -n 10 python3 cfg534_kids.py
"""
import os, sys, io, math, json, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG534_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
LOG, CHK = [], {}
RES = {"lane": "CFG534", "script": "cfg534_kids", "mutate": MUT, "criteria_commit": "aa8dc312e",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass still required; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


try:
    os.nice(10)
except OSError:
    pass

# ------------------------------------------------------------------ CFG531 machinery (read-only exec up to its class split)
P531 = os.path.join(LANES, "CFG531_inner_halo_shortfall", "cfg531_kids.py")
_src = open(P531).read()
_cut = _src.index("EARLY = TYP == 1")
NS = {"__file__": P531, "__name__": "cfg531_ro"}
os.environ["CFG531_MUTATE"] = "0"
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_src[:_cut], "cfg531_kids", "exec"), NS)
P(f"CFG531 machinery exec'd read-only ({len(_buf.getvalue().splitlines())} lines suppressed); its checks: "
  f"{ {k: v['ok'] for k, v in NS['CHK'].items()} }")
F30, WW, WG, patch, gi, NGRP = NS["F30"], NS["WW"], NS["WG"], NS["patch"], NS["gi"], NS["NGRP"]
NPATCH, KG, hart, BANDS, SHMRS, FOOTS, CONS = NS["NPATCH"], NS["KG"], NS["hart"], NS["BANDS"], NS["SHMRS"], NS["FOOTS"], NS["CONS"]
TYP, LMSL, MEAS, evec, own_mix, GP, fit_eps, comps, esd_loo = (NS[k] for k in ("TYP", "LMSL", "MEAS", "evec", "own_mix", "GP", "fit_eps", "comps", "esd_loo"))
EARLY = TYP == 1
UV = np.load(os.path.join(NS["REPO"], "..", "_external_data", "cfg505_work", "cfg505_uv_table.npz"))
DET, COV = UV["det"].astype(bool), ~UV["nocov"].astype(bool)
assert len(DET) == len(TYP)
J531 = json.load(open(os.path.join(LANES, "CFG531_inner_halo_shortfall", "cfg531_kids_results.json")))

# per-group E and own tables (CFG531 comps internals, LAW_RTA, f30 stripping mix)
GT = {}
for c in CONS:
    for foot in FOOTS:
        for s in SHMRS:
            fE = MEAS["f30"]
            GT[(c, foot, s)] = (evec(GP, c, s, "W30", fE[s], f"cfg531|{id(fE)}|W30"), own_mix(c, foot, "LAW_RTA", fE, None, s))
P(f"group tables built ({time.time() - T0:.0f} s)")


def wsum(mask, M=None):
    """W[g, k] = summed WW (x multiplier) of the lenses in mask."""
    W = np.zeros((NGRP, 15))
    for k in range(15):
        w = WW[mask, k] if M is None else WW[mask, k] * M[mask, k]
        W[:, k] = np.bincount(gi[mask], weights=w, minlength=NGRP)
    return W


def match(mA, mB, mode="A"):
    """lens multipliers (N x 15) for classes A and B: A keeps cells where B exists; B scaled to A's cell weight.
    mode "overlap" (POST-FREEZE diagnostic, 2026-10-09, no verdict weight): both classes scaled to W_A W_B / (W_A + W_B)."""
    WA, WB = wsum(mA), wsum(mB)
    keep = (WA > 0) & (WB > 0)
    safeA, safeB = np.where(WA > 0, WA, 1.0), np.where(WB > 0, WB, 1.0)
    if mode == "A":
        rA, rB = keep.astype(float), np.where(keep, WA / safeB, 0.0)
    else:
        WT = np.where(keep, WA * WB / np.where(keep, WA + WB, 1.0), 0.0)
        rA, rB = WT / safeA, WT / safeB
    MA = np.zeros_like(WW); MB = np.zeros_like(WW)
    MA[mA] = rA[gi[mA]]
    MB[mB] = rB[gi[mB]]
    return MA, MB


def esd_w(mask, M):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k] * M[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k] * M[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev, loo


def mstack(tab, mask, M):
    W = wsum(mask, M)
    return (W * tab).sum(0) / W.sum(0)


def cp_w(c, foot, mask, M):
    return {s: (mstack(GT[(c, foot, s)][0], mask, M), mstack(GT[(c, foot, s)][1], mask, M)) for s in SHMRS}


def gls(dd, Cd, o, idx):
    idx = np.asarray(idx)
    W = np.linalg.inv(Cd[np.ix_(idx, idx)] / hart(len(idx)))
    F = float(o[idx] @ W @ o[idx]); e = float(o[idx] @ W @ dd[idx]) / F
    return dict(eps=e, sig=F ** -0.5, Z=e * F ** 0.5)


def compare(mA, mB, label, inject=None, cells=None, mode="A"):
    """matched comparison A - B; returns per (c|foot) the per-class eps and Delta eps per band (both SHMR templates)."""
    MA, MB = match(mA, mB, mode)
    dA, CA, LA = esd_w(mA, MA); dB, CB, LB = esd_w(mB, MB)
    out = dict(nA=int(mA.sum()), nB=int(mB.sum()), nA_kept=int((MA[mA].sum(1) > 0).sum()), nB_kept=int((MB[mB].sum(1) > 0).sum()))
    k2 = 0.0
    for c in CONS:
        for foot in FOOTS:
            if cells is not None and (c, foot) not in cells:
                continue
            cA, cB = cp_w(c, foot, mA, MA), cp_w(c, foot, mB, MB)
            for s in SHMRS:
                for j in (0, 1):
                    k2 = max(k2, float(np.max(np.abs(cA[s][j] / cB[s][j] - 1))))
            dA_ = dA if inject is None else dB + inject * cA["moster"][1]
            # MU2 covariance (fixed 2026-10-09 after the first MUTATE run hit a singular C): keep the real jackknife scatter of Delta d
            LA_ = LA if inject is None else LA - dA[None, :] + dB[None, :] + inject * cA["moster"][1][None, :]
            dd = dA_ - dB; dv = LA_ - LB; dv = dv - dv.mean(0)
            Cd = (NPATCH - 1) / NPATCH * dv.T @ dv
            r = {}
            for b, ix in BANDS.items():
                gm = gls(dd, Cd, cA["moster"][1], ix); gb = gls(dd, Cd, cA["behroozi"][1], ix)
                eA = fit_eps(dA_, CA, cA, ix); eB = fit_eps(dB, CB, cB, ix)
                r[b] = dict(d_eps_moster=gm, d_eps_behroozi=gb, Zmin=min(gm["Z"], gb["Z"]) if gm["Z"] > 0 else max(gm["Z"], gb["Z"]),
                            eps_A=eA["eps"], sig_A=eA["sig"], eps_B=eB["eps"], sig_B=eB["sig"])
            out[f"{c}|{foot}"] = r
            if inject is None:
                k9 = r["K9"]
                P(f"  {label:22s} [{c} {foot:9s}] eps_A {k9['eps_A']:+.3f}+-{k9['sig_A']:.3f}  eps_B {k9['eps_B']:+.3f}+-{k9['sig_B']:.3f}  "
                  f"Delta eps K9 {k9['d_eps_moster']['eps']:+.3f}+-{k9['d_eps_moster']['sig']:.3f} (Z {k9['d_eps_moster']['Z']:+.2f}; "
                  f"behroozi Z {k9['d_eps_behroozi']['Z']:+.2f})  | K-in {r['K-in']['d_eps_moster']['eps']:+.3f}+-{r['K-in']['d_eps_moster']['sig']:.3f} "
                  f"K-mid {r['K-mid']['d_eps_moster']['eps']:+.3f}+-{r['K-mid']['d_eps_moster']['sig']:.3f} "
                  f"K-out {r['K-out']['d_eps_moster']['eps']:+.3f}+-{r['K-out']['d_eps_moster']['sig']:.3f}")
    out["K2_model_maxrel"] = k2
    return out


SPL = {"1a_type": (F30 & EARLY, F30 & ~EARLY),
       "1b_uv": (F30 & COV & ~DET, F30 & COV & DET),
       "1b_uv_in_late": (F30 & COV & ~DET & ~EARLY, F30 & COV & DET & ~EARLY),
       "1b_uv_in_early": (F30 & COV & ~DET & EARLY, F30 & COV & DET & EARLY)}

if not MUT:
    # K1: unmatched per-class eps(K9) = CFG531 (c)
    k1 = 0.0
    for cls, mk in (("early", F30 & EARLY), ("late", F30 & ~EARLY)):
        dcl, Ccl, _ = esd_loo(mk)
        for c in CONS:
            for foot in FOOTS:
                e = fit_eps(dcl, Ccl, comps(c, foot, mk), BANDS["K9"])["eps"]
                k1 = max(k1, abs(e - J531["c"][f"{cls}|{c}|{foot}"]["bands"]["K9"]["eps"]))
    check("K1 unmatched early / late eps(K9) reproduce CFG531 (c) to 1e-6 (A, B, both footings)", k1 < 1e-6, f"max |d| {k1:.1e}")
    RES["unmatched_CFG531_c"] = {k: v["bands"]["K9"]["eps"] for k, v in J531["c"].items()}

    P("\n== matched comparisons (inside (M_gal, z) group x bin cells) ==")
    CMP = {}
    for nm, (a, b) in SPL.items():
        CMP[nm] = compare(a, b, nm)
        P(f"     {nm}: n_A {CMP[nm]['nA']} (kept {CMP[nm]['nA_kept']}), n_B {CMP[nm]['nB']} (kept {CMP[nm]['nB_kept']}); model max rel diff {CMP[nm]['K2_model_maxrel']:.1e}")
    k2 = max(v["K2_model_maxrel"] for v in CMP.values())
    check("K2 matched classes share identical stacked model vectors (1e-10 rel; all splits, bands, SHMRs)", k2 < 1e-10, f"max rel {k2:.1e}")
    P("\n== 1c: matched early - late inside each f30 log M* tertile ==")
    q = np.percentile(LMSL[F30], [100 / 3, 200 / 3])
    TER = {}
    for t, (lo, hi) in enumerate([(-np.inf, q[0]), (q[0], q[1]), (q[1], np.inf)]):
        mk = F30 & (LMSL > lo) & (LMSL <= hi)
        TER[f"T{t + 1}"] = compare(mk & EARLY, mk & ~EARLY, f"1c T{t + 1} (med {np.median(LMSL[mk]):.2f})")
        TER[f"T{t + 1}"]["logMs_median"] = float(np.median(LMSL[mk]))
    RES["tertiles"] = TER
    RES["compare"] = CMP

    # rules
    RULE = {}
    for foot in FOOTS:
        za = [CMP["1a_type"][f"{c}|{foot}"]["K9"]["Zmin"] for c in CONS]
        sa = [CMP["1a_type"][f"{c}|{foot}"]["K9"]["d_eps_moster"]["sig"] for c in CONS]
        zb = [CMP["1b_uv"][f"{c}|{foot}"]["K9"]["Zmin"] for c in CONS]
        eb = [CMP["1b_uv"][f"{c}|{foot}"]["K9"]["d_eps_moster"]["eps"] for c in CONS]
        zl = [CMP["1a_type"][f"{c}|{foot}"]["K9"]["eps_B"] / CMP["1a_type"][f"{c}|{foot}"]["K9"]["sig_B"] for c in CONS]
        dea = {c: CMP["1a_type"][f"{c}|{foot}"]["K9"]["d_eps_moster"]["eps"] for c in CONS}
        dl = {c: J531["a"][f"d0|{c}|{foot}"]["K9"]["eps"] - J531["a"][f"d0.10|{c}|{foot}"]["K9"]["eps"] for c in CONS}
        tmpl = {c: {b: J531["a"][f"d0|{c}|{foot}"][b]["eps"] - J531["a"][f"d0.10|{c}|{foot}"][b]["eps"] for b in ("K-in", "K-mid", "K-out", "K9")} for c in CONS}
        RULE[foot] = dict(
            sig_1a_max=max(sa), Z_1a=za, pass_1a=all(z >= 3 for z in za), ge2_1a=all(z >= 2 for z in za), contra_1a=any(z <= -2 for z in za),
            Z_1b=zb, same_sign_1b=all(e > 0 for e in eb), sig_1b=all(z >= 3 for z in zb), contra_1b=any(z <= -2 for z in zb),
            late_Z=zl, late_on_law=all(abs(z) < 2 for z in zl),
            delta_equiv_dex={c: 0.10 * dea[c] / dl[c] for c in CONS},
            ML_template_eps_per_0p10dex=tmpl)
        P(f"\n  [{foot}] 1a K9 Zmin {['%+.2f' % z for z in za]} -> PASS {RULE[foot]['pass_1a']} (>=2: {RULE[foot]['ge2_1a']}, contra {RULE[foot]['contra_1a']}); "
          f"sigma max {max(sa):.3f}")
        P(f"  [{foot}] 1b K9 Zmin {['%+.2f' % z for z in zb]} -> same sign {RULE[foot]['same_sign_1b']}, >=3 {RULE[foot]['sig_1b']}, contra {RULE[foot]['contra_1b']}")
        P(f"  [{foot}] matched late eps(K9)/sigma {['%+.2f' % z for z in zl]} -> late on the law: {RULE[foot]['late_on_law']}")
        P(f"  [{foot}] delta_equiv (uniform M* shift giving the matched early-late Delta eps): " +
          ", ".join(f"{c} {v:+.3f} dex" for c, v in RULE[foot]["delta_equiv_dex"].items()))
        P(f"  [{foot}] M/L-shift template (eps change per +0.10 dex, CFG531 tables; KiDS radial = not discriminating, report only): " +
          "; ".join(f"{c}: " + " ".join(f"{b} {v:.3f}" for b, v in tmpl[c].items()) for c in CONS))
    RES["rules"] = RULE

    # POST-FREEZE diagnostic (added 2026-10-09 after the first run; NO verdict weight): overlap weighting W_A W_B / (W_A + W_B)
    # per cell, the minimum-variance weighting for a constant within-cell difference; it asks whether the frozen estimator's
    # power (late lenses up-weighted in high-mass cells) is what limits 1a.
    P("\n== POST-FREEZE diagnostic (no verdict weight): overlap-weighted matching ==")
    PF = {nm: compare(SPL[nm][0], SPL[nm][1], nm + " [overlap]", mode="overlap") for nm in ("1a_type", "1b_uv")}
    for v in PF.values():
        v.pop("K2_model_maxrel", None)
    RES["postfreeze_overlap"] = PF
else:
    P("\n== MUTATE ==")
    rng = np.random.default_rng(534)
    idx30 = np.nonzero(F30)[0]

    def shuffle(lab, base):
        out = lab.copy()
        for g in np.unique(gi[idx30]):
            m = idx30[(gi[idx30] == g) & base[idx30]]
            out[m] = rng.permutation(lab[m])
        return out
    ES = shuffle(EARLY, F30)
    DS = shuffle(DET, F30 & COV)
    mu1 = {}
    ok = True
    for nm, (a, b) in (("type", (F30 & ES, F30 & ~ES)), ("uv", (F30 & COV & ~DS, F30 & COV & DS))):
        r = compare(a, b, f"MU1 shuffled {nm}")
        for c in CONS:
            for foot in FOOTS:
                z = r[f"{c}|{foot}"]["K9"]["d_eps_moster"]["Z"]; zb = r[f"{c}|{foot}"]["K9"]["d_eps_behroozi"]["Z"]
                mu1[f"{nm}|{c}|{foot}"] = dict(Z=z, Z_behroozi=zb, d_eps=r[f"{c}|{foot}"]["K9"]["d_eps_moster"]["eps"])
                ok &= abs(z) < 2.5 and abs(zb) < 2.5
    check("MU1 labels shuffled inside groups: matched Delta eps(K9) |Z| < 2.5 in all cells (type and NUV)", ok,
          "; ".join(f"{k} {v['Z']:+.2f}" for k, v in mu1.items()))
    RES["MU1"] = mu1
    # POST-FREEZE (2026-10-09, no verdict weight): the same shuffles under the overlap-weighted diagnostic
    pf = {}
    for nm, (a, b) in (("type", (F30 & ES, F30 & ~ES)), ("uv", (F30 & COV & ~DS, F30 & COV & DS))):
        r = compare(a, b, f"MU1-PF shuffled {nm} [overlap]", mode="overlap")
        pf[nm] = {f"{c}|{foot}": r[f"{c}|{foot}"]["K9"]["d_eps_moster"]["Z"] for c in CONS for foot in FOOTS}
    P(f"  MU1-PF (reported): overlap-weighted shuffled Z {pf}")
    RES["MU1_postfreeze_overlap"] = pf
    r = compare(F30 & EARLY, F30 & ~EARLY, "MU2", inject=0.3)
    mu2 = max(abs(r[f"{c}|{f}"][b]["d_eps_moster"]["eps"] - 0.3) for c in CONS for f in FOOTS for b in BANDS)
    check("MU2 mock d_A = d_B,matched + 0.3 own: Delta eps = 0.300 in every band (1e-6)", mu2 < 1e-6, f"max |d| {mu2:.1e}")

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for v in CHK.values() if not v["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg534_kids_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg534_kids{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
