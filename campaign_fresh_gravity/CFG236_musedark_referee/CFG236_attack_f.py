"""CFG236 extras F1-F8 (duplicates, selection, censoring, error-model MC, kernel, placement, covariates, subsets).  Seed 2365."""
import os, sys, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG236_common as c

SEED = 2365
B = 2000
NMC = 2000
o = c.Out("attack_f")
c.header(o, "CFG236 extras F1-F8")
T = c.load_numeric()
J = c.load_joined()
idx, cnt = c.sample(T)
C = c.get_cols(T, idx)
z = C["z"]
zmed = float(np.median(z))
ids = T["muse_id"][idx].astype(int)
DAT = c.dat_available()
cons = {"R198": dict(mode="R198")}
if DAT:
    dat = c.load_dat(T, idx)
    cons["R199a"] = dict(mode="R199", gperp=c.gperp_reading(dat["v1"], C["Re"], C["incl"], "a"))
    cons["R199b"] = dict(mode="R199", gperp=c.gperp_reading(dat["v1"], C["Re"], C["incl"], "b"))


def cols_of(cfg, CC=None):
    R = c.routes(CC or C, cfg)
    return R, {r: np.log10(R["a0_" + r]) for r in ("i", "ii", "iii")}


def sl3(cols, zz=None, sel=None):
    zz = z if zz is None else zz
    cc = {r: (np.where(sel, v, np.nan) if sel is not None else v) for r, v in cols.items()}
    b = {r: c.theil_sen(zz, cc[r]) for r in cc}
    both = np.isfinite(cc["i"]) & np.isfinite(cc["ii"])
    b["d"] = c.theil_sen(zz, np.where(both, cc["ii"], np.nan)) - c.theil_sen(zz, np.where(both, cc["i"], np.nan))
    return b


# ---------------------------------------------------------------- F1 duplicates
o.P("F1: duplicates")
mid = T["muse_id"].astype(int)
dups = [int(m) for m in np.unique(mid) if np.sum(mid == m) > 1]
o.P(f"   duplicated muse_id in the numeric CSV: {dups}; distinct ids {len(np.unique(mid))} of {len(mid)}; ids in CSV but not in joined: {sorted(set(mid.tolist()) - set(J))}; in joined but not in CSV: {sorted(set(J) - set(mid.tolist()))}")
dj = json.load(open(os.path.join(c.CAT, "duplicated_rows.json")))["DC14"]["26"]
r26 = np.where(mid == 26)[0]
o.P(f"   id 26 rows in CSV: {len(r26)}; in S: {bool(26 in ids)}")
if len(r26):
    i26 = r26[0]
    o.P(f"   id 26 CSV: Vvir {T['Vvir'][i26]:.2f}, DC14_log_X {T['DC14_log_X'][i26]:.3f}, DC14_logMvir {T['DC14_logMvir'][i26]:.3f}; dup row A: V_vir {float(dj[0]['virial_velocity']):.2f}, log_X {float(dj[0]['log_X']):.3f}, log_Mvir {float(dj[0]['log_Mvir']):.3f}; dup row B: V_vir {float(dj[1]['virial_velocity']):.2f}, log_X {float(dj[1]['log_X']):.3f}, log_Mvir {float(dj[1]['log_Mvir']):.3f}")
    dV = [abs(T["Vvir"][i26] - float(d["virial_velocity"])) for d in dj]
    o.P(f"   |CSV V_vir - row| = {dV[0]:.2f}, {dV[1]:.2f} -> matches row {'A' if dV[0] < dV[1] else 'B'} (DC14_bestfit.txt), tolerance check {min(dV):.2f} km/s")
    o.res["F1"] = dict(dups=dups, match=("A" if dV[0] < dV[1] else "B"), min_dV=min(dV))
keep = ids != 26
for nm, base in cons.items():
    Rf, cf = cols_of(base)
    full = sl3(cf)
    red = sl3(cf, sel=keep)
    o.P(f"   [{nm}] with / without id 26: b_i {full['i']:+.3f}/{red['i']:+.3f}, b_ii {full['ii']:+.3f}/{red['ii']:+.3f}, Delta b {full['d']:+.3f}/{red['d']:+.3f}")
o.P(f"   source absences: DC14 halo file lacks id 36; in the numeric set id 36 present: {bool(36 in mid)}; id 69 (baryons-only lacks): {bool(69 in mid)}")

# ---------------------------------------------------------------- F2 selection and leave-one-out
o.P("\nF2: selection and influence")
zh_all = T["z"] <= zmed
fin = np.ones(len(mid), bool)
reasons = []
for k in ("z", "logMstar_phot", "DC14_logMdisk", "fDM_at_Re", "Re_kpc", "gas_density_Msun_pc2"):
    bad = ~np.isfinite(T[k])
    reasons.append((f"missing {k}", int(bad.sum()), int((bad & zh_all).sum())))
bulge = (T["has_bulge"] == 1)
fdm_bad = np.isfinite(T["fDM_at_Re"]) & ~((T["fDM_at_Re"] > 0) & (T["fDM_at_Re"] < 1))
reasons.append(("bulge component", int(bulge.sum()), int((bulge & zh_all).sum())))
reasons.append(("fDM outside (0,1) (any)", int(fdm_bad.sum()), int((fdm_bad & zh_all).sum())))
for r_ in reasons:
    o.P(f"   exclusion {r_[0]:32s}: n={r_[1]} (low-z half {r_[2]})")
Rf, cf = cols_of(cons["R198"])
for r in ("i", "ii", "iii"):
    cen = ~np.isfinite(cf[r])
    o.P(f"   route ({r}) undefined (D<=1.05): {int(cen.sum())}  (low-z half {int((cen & (z<=zmed)).sum())}, high-z half {int((cen & (z>zmed)).sum())})")
o.P(f"   fDM<=0 or >=1 ids in the 110 disc rows: {sorted(T['muse_id'][(T['has_bulge']==0)&np.isfinite(T['logMstar_phot'])&~((T['fDM_at_Re']>0)&(T['fDM_at_Re']<1))].astype(int).tolist())}; fDM median {np.median(C['fDM']):.2f}, fDM<0.2: {int((C['fDM']<0.2).sum())}, fDM>0.9: {int((C['fDM']>0.9).sum())}")
F2 = {}
for nm, base in cons.items():
    Rf, cf = cols_of(base)
    full = sl3(cf)
    loo = {k: np.empty(len(z)) for k in ("i", "ii", "d")}
    for j in range(len(z)):
        s = np.ones(len(z), bool); s[j] = False
        t = sl3(cf, sel=s)
        for k in loo:
            loo[k][j] = t[k]
    for k in loo:
        dv = loo[k] - full[k]
        o.P(f"   [{nm}] leave-one-out {k}: full {full[k]:+.3f}; max |change| {np.max(np.abs(dv)):.3f}; top five ids by |change| {[int(ids[i]) for i in np.argsort(-np.abs(dv))[:5]]}")
    up = np.argsort(-(loo["ii"] - full["ii"]))[:10]
    dn = np.argsort(loo["ii"] - full["ii"])[:10]
    for lab, dd in (("drop the 10 whose removal raises b_ii most", up), ("drop the 10 whose removal lowers b_ii most", dn)):
        s = np.ones(len(z), bool); s[dd] = False
        t = sl3(cf, sel=s)
        o.P(f"   [{nm}] {lab}: b_i {t['i']:+.3f}  b_ii {t['ii']:+.3f}  Delta b {t['d']:+.3f}")
    F2[nm] = dict(max_dbi=float(np.max(np.abs(loo['i'] - full['i']))), max_dbii=float(np.max(np.abs(loo['ii'] - full['ii']))), max_dd=float(np.max(np.abs(loo['d'] - full['d']))))
o.res["F2"] = F2

# ---------------------------------------------------------------- F3 censoring
o.P("\nF3: censoring (D<=1.05 rows are upper limits on a0)")
F3 = {}
for nm, base in cons.items():
    R, cf = cols_of(base)
    cen = ~np.isfinite(cf["ii"]) & np.isfinite(cf["i"])
    for lab, off in (("(lo) set to the a0 bound", 0.0), ("(hi) bound - 1 dex", -1.0)):
        y = np.where(cen, np.log10(R["bound_ii"]) + off, cf["ii"])
        b = c.theil_sen(z, y)
        F3[f"{nm}|{lab}"] = b
        o.P(f"   [{nm}] {lab}: b_ii (n={int(np.isfinite(y).sum())}) = {b:+.3f}")
    y = np.where(cen, -np.inf, cf["ii"])
    rk = np.full(len(z), np.nan)
    ok = np.isfinite(cf["i"])
    yy = np.where(np.isfinite(y), y, -99.0)
    rho, p = c.stats.spearmanr(z[ok], yy[ok])
    o.P(f"   [{nm}] Spearman(z, a0_ii) with the censored rows at the bottom rank: {rho:+.2f} (p={p:.3f}); uncensored only: {c.stats.spearmanr(z[np.isfinite(cf['ii'])], cf['ii'][np.isfinite(cf['ii'])])[0]:+.2f}")
o.res["F3"] = F3

# ---------------------------------------------------------------- F4 error model MC
o.P("\nF4: Monte Carlo through the tabulated errors (seed 2365; fDM, v, R_e NOT propagated: no errors in the CSV; g_obs held fixed)")
ex_sed = np.array([float(J[i]["logMstar_phot_err"]) if J[i]["logMstar_phot_err"] not in ("", None) else np.nan for i in ids])
ex_sed = np.where(np.isfinite(ex_sed), ex_sed, 0.15)
ex_fit = T["DC14_logMdisk_err"][idx]
o.P(f"   sigma(log M*_SED) joined: median {np.median(ex_sed):.3f} [{np.percentile(ex_sed,10):.3f},{np.percentile(ex_sed,90):.3f}]; sigma(log M_fit) median {np.median(ex_fit):.3f}")
F4 = {}
for nm, base in cons.items():
    R0, cf0 = cols_of(base)
    st0, _ = c.slope_table(z, cf0, B, SEED)
    gobs0 = R0["gobs"] if base["mode"] == "R198" else None
    for vlab, sseds in (("joined errors", ex_sed), ("floored at 0.15", np.maximum(ex_sed, 0.15))):
        rng = np.random.default_rng(SEED)
        vals = {"i": [], "ii": [], "iii": [], "d": []}
        for t in range(NMC):
            C2 = dict(C)
            C2["logMsed"] = C["logMsed"] + rng.normal(0, 1, len(z)) * sseds
            C2["logMfit"] = C["logMfit"] + rng.normal(0, 1, len(z)) * ex_fit
            cfg = dict(base, mu_fac=10 ** rng.normal(0, 0.15, len(z)), zmed=zmed)
            if gobs0 is not None:
                cfg["gobs_fixed"] = gobs0
            R, cc = cols_of(cfg, C2)
            b = sl3(cc)
            for k in vals:
                vals[k].append(b[k])
        m = {k: (float(np.nanmean(v)), float(np.nanstd(v))) for k, v in vals.items()}
        sd_b = st0["ii"]["sd"]
        tot = math.sqrt(sd_b ** 2 + m["ii"][1] ** 2)
        o.P(f"   [{nm}] {vlab}: MC mean shift b_i {m['i'][0]-st0['i']['b']:+.3f} (SD {m['i'][1]:.3f}); b_ii {m['ii'][0]-st0['ii']['b']:+.3f} (SD {m['ii'][1]:.3f}); Delta b mean {m['d'][0]:+.3f} (SD {m['d'][1]:.3f}); bootstrap SD b_ii {sd_b:.3f}; quadrature total {tot:.3f} = {tot/sd_b:.2f} x bootstrap")
        F4[f"{nm}|{vlab}"] = dict(m=m, boot_sd=sd_b, ratio=tot / sd_b)
o.res["F4"] = F4

# ---------------------------------------------------------------- F5 kernels
o.P("\nF5: kernels")
F5 = {}
for nm, base in cons.items():
    for kn in ("RAR", "P2", "mono"):
        try:
            R, cc = cols_of(dict(base, kernel=kn))
        except Exception as e:
            o.P(f"   [{nm}] {kn}: NOT RUN ({type(e).__name__})"); continue
        b = sl3(cc)
        F5[f"{nm}|{kn}"] = b
        o.P(f"   [{nm}] {kn}{' (IMPORT, shared)' if kn=='mono' else ''}: b_i {b['i']:+.3f}  b_ii {b['ii']:+.3f}  b_iii {b['iii']:+.3f}  Delta b {b['d']:+.3f}")
    for kn in ("P2", "mono"):
        if f"{nm}|{kn}" in F5:
            dd = max(abs(F5[f"{nm}|{kn}"][k] - F5[f"{nm}|RAR"][k]) for k in ("i", "ii", "d"))
            o.P(f"   [{nm}] max |{kn} - RAR| over b_i, b_ii, Delta b = {dd:.3f} (frozen prediction: within 0.03)")
o.res["F5"] = F5

# ---------------------------------------------------------------- F6 placement
o.P("\nF6: placement against flat (0), E(z), III for every route and row (95% bootstrap CI, B=2000)")
rows = [("R198 primary", dict(mode="R198")), ("R198 Sigma=0", dict(mode="R198", Sig=0.0)), ("R198 Sigma=15", dict(mode="R198", Sig=15.0)),
        ("R198 mu x0.5", dict(mode="R198", mu_scale=0.5)), ("R198 mu x2", dict(mode="R198", mu_scale=2.0))]
if DAT:
    rows += [("R199a", cons["R199a"]), ("R199b", cons["R199b"]), ("R199a Sigma=0", dict(cons["R199a"], Sig=0.0)), ("R199a mu x2", dict(cons["R199a"], mu_scale=2.0))]
F6 = {}
for lab, cfg in rows:
    R, cc = cols_of(cfg)
    st, _ = c.slope_table(z, cc, B, SEED)
    for r in ("i", "ii", "iii"):
        refs = c.ref_slopes(z[np.isfinite(cc[r])])
        cl = c.classify(st[r], refs)
        F6[f"{lab}|{r}"] = dict(st=st[r], cl=cl)
        s = st[r]
        o.P(f"   {lab:15s} route ({r}): b {s['b']:+.3f} [{s['lo']:+.2f},{s['hi']:+.2f}] SD {s['sd']:.2f} | flat {cl['flat']['dist_sd']:+.1f} SD {'in ' if cl['flat']['inside'] else 'OUT'} | E(z) {cl['Ez']['dist_sd']:+.1f} {'in ' if cl['Ez']['inside'] else 'OUT'} | III {cl['III']['dist_sd']:+.1f} {'in ' if cl['III']['inside'] else 'OUT'}")
o.res["F6"] = F6

# ---------------------------------------------------------------- F7 multi-covariate
o.P("\nF7: multi-covariate OLS  log a0 ~ z + (log M*_SED - 9.24) + (log R_e - med) + (log g_bar - med)   (bootstrap B=2000)")


def ols_boot_full(y, X, B_, seed):
    Xc = np.column_stack([np.ones(len(y)), X])
    b = np.linalg.lstsq(Xc, y, rcond=None)[0]
    r = np.random.default_rng(seed)
    n = len(y)
    bb = np.empty((B_, Xc.shape[1]))
    for t in range(B_):
        i = r.integers(0, n, n)
        bb[t] = np.linalg.lstsq(Xc[i], y[i], rcond=None)[0]
    return b, bb


F7 = {}
for nm, base in cons.items():
    R, cc = cols_of(base)
    for r in ("i", "ii"):
        y = cc[r]
        m = np.isfinite(y)
        gb = np.log10(R["gb_" + r])
        X = np.column_stack([z[m], (C["logMsed"] - 9.24)[m], (np.log10(C["Re"]) - np.median(np.log10(C["Re"])))[m], (gb - np.median(gb))[m]])
        for lab, cols_ in (("z only", [0]), ("z + M*", [0, 1]), ("z + M* + R_e", [0, 1, 2]), ("z + M* + R_e + g_bar", [0, 1, 2, 3])):
            b, bb = ols_boot_full(y[m], X[:, cols_], B, SEED)
            lo, hi = c.ci(bb[:, 1])
            F7[f"{nm}|{r}|{lab}"] = dict(b=float(b[1]), ci=(lo, hi))
            o.P(f"   [{nm}] route ({r}) {lab:22s}: partial z slope {b[1]:+.3f} [{lo:+.2f},{hi:+.2f}]")
o.res["F7"] = F7

# ---------------------------------------------------------------- F8 subsets
o.P("\nF8: M*_SED terciles and z-halves")
lM = C["logMsed"]
terc = np.array_split(np.argsort(lM, kind="stable"), 3)
for nm, base in cons.items():
    R, cc = cols_of(base)
    for k, t in enumerate(terc):
        sel = np.zeros(len(z), bool); sel[t] = True
        sub = {r: np.where(sel, cc[r], np.nan) for r in cc}
        st, _ = c.slope_table(z, {"i": sub["i"], "ii": sub["ii"]}, B, SEED)
        o.P(f"   [{nm}] M* tercile {k+1} (log M* {lM[t].min():.2f}-{lM[t].max():.2f}): b_i {st['i']['b']:+.2f} [{st['i']['lo']:+.2f},{st['i']['hi']:+.2f}] (n={st['i']['n']}); b_ii {st['ii']['b']:+.2f} [{st['ii']['lo']:+.2f},{st['ii']['hi']:+.2f}] (n={st['ii']['n']})")
    for lab, sel in (("low-z half", z <= zmed), ("high-z half", z > zmed)):
        sub = {r: np.where(sel, cc[r], np.nan) for r in cc}
        Li = c.level_log(R["a0_i"])
        Lii = c.level_log(R["a0_ii"])
        o.P(f"   [{nm}] {lab}: n_i {int(np.isfinite(sub['i']).sum())}, n_ii {int(np.isfinite(sub['ii']).sum())}; median log a0 route (i) {np.nanmedian(np.where(sel, Li, np.nan)):.2f}, route (ii) {np.nanmedian(np.where(sel, Lii, np.nan)):.2f}; b_i {c.theil_sen(z, sub['i']):+.2f}, b_ii {c.theil_sen(z, sub['ii']):+.2f}")
o.finish()
sys.exit(0)
