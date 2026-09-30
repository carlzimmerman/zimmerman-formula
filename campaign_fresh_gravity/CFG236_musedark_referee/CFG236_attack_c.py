"""CFG236 attack (c): which mass is right.  C1-C6 and the decision table (section 9 of the frozen criteria).  Seed 2362.
Run-time interpretation declared BEFORE this script ran (recorded here): a condition on tau* must hold on BOTH constructions (R198 and R199 reading (a))
for O1 and for O2; d_M and C4 are evaluated as written; C6 (sSFR) window = interquartile range of log M*_SED in S (the frozen text said 'a fixed window');
SFR in musedark_joined.csv is read as log10 SFR (Msun/yr) because its range is -1.6..+1.9 (units UNVERIFIED)."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG236_common as c

SEED = 2362
B = 2000
o = c.Out("attack_c")
c.header(o, "CFG236 attack (c): which mass is right")
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


def slopes(cfg, with_ci=False, only="ii"):
    R = c.routes(C, cfg)
    cols = {r: np.log10(R["a0_" + r]) for r in ("i", "ii", "iii")}
    out = {r: c.theil_sen(z, cols[r]) for r in cols}
    out["n_ii"] = int(np.isfinite(cols["ii"]).sum())
    both = np.isfinite(cols["i"]) & np.isfinite(cols["ii"])
    out["d"] = c.theil_sen(z, np.where(both, cols["ii"], np.nan)) - c.theil_sen(z, np.where(both, cols["i"], np.nan))
    if with_ci:
        st, _ = c.slope_table(z, {only: cols[only]}, B, SEED)
        out["ci"] = (st[only]["lo"], st[only]["hi"])
        out["sd"] = st[only]["sd"]
    return out, R


# ---------------------------------------------------------------- C1 algebra
o.P("C1: gain S(D) = dln a0/dln g_bar at fixed g_obs = 1 - 1/eta, and f_d, on route (ii) rows (R198)")
st0, R0 = slopes(cons["R198"])
ker = c.get_kernel("RAR")
ok = np.isfinite(R0["a0_ii"])
ys = c.invert(R0["D_ii"][ok], ker)
h = 1e-4
eta = -(np.log(ker(ys * math.exp(h))) - np.log(ker(ys * math.exp(-h)))) / (2 * h)
Sg = 1 - 1 / eta
Rd = C["Re"][ok] / 1.678
M_ii = 10 ** (C["logMsed"][ok]) * (1 + R0["mu"][ok])
gd = c.g_disc(M_ii, C["Re"][ok], Rd)
fd = gd / (gd + c.g_hi(C["Sig"][ok]))
o.P(f"   S(D): median {np.median(Sg):+.2f}, 16-84 [{np.percentile(Sg,16):+.2f},{np.percentile(Sg,84):+.2f}], min {Sg.min():+.2f}; f_d median {np.median(fd):.2f} [{np.percentile(fd,16):.2f},{np.percentile(fd,84):.2f}]; median |S| f_d {np.median(np.abs(Sg)*fd):.2f}")
st_d2 = c.theil_sen(z, C["logMfit"] - C["logMsed"] - np.log10(1 + R0["mu"]))
o.P(f"   prediction Delta b ~ -(S f_d) x 0.868 = {np.median(np.abs(Sg)*fd)*st_d2:+.3f} (observed {st0['d']:+.3f})")
o.res["C1"] = dict(S_med=float(np.median(Sg)), fd_med=float(np.median(fd)), Sfd_med=float(np.median(np.abs(Sg) * fd)))

# ---------------------------------------------------------------- C2 bias grids
TAUS = [-0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
TAUS_EXT = [1.4, 1.6, 1.8, 2.0, 2.4, 3.0]


def cross(xs, ys_, target):
    for a in range(len(xs) - 1):
        d0, d1 = ys_[a] - target, ys_[a + 1] - target
        if d0 == 0:
            return xs[a]
        if d0 * d1 < 0:
            return xs[a] + (target - ys_[a]) * (xs[a + 1] - xs[a]) / (ys_[a + 1] - ys_[a])
    return None


C2 = {}
for nm, base in cons.items():
    o.P(f"C2 [{nm}]: SED-M* z-dependent bias tau (true = SED - tau (z - zmed)), frozen grid then EXTENDED grid (post-frozen extension, labelled)")
    bi = slopes(base)[0]["i"]
    rows = []
    for tau in TAUS + TAUS_EXT:
        s, _ = slopes(dict(base, tau=tau), with_ci=(tau in TAUS))
        ext = tau in TAUS_EXT
        rows.append((tau, s["ii"], s["d"], s["n_ii"], s.get("ci"), ext))
        o.P(f"   tau {tau:+.1f}{' [EXT]' if ext else ''}: b_ii {s['ii']:+.3f}{'' if 'ci' not in s else ' [%+.2f,%+.2f]' % s['ci']}  Delta b {s['d']:+.3f}  n(ii) {s['n_ii']}  b_iii {s['iii']:+.3f}")
    xs = [r[0] for r in rows]
    bii = [r[1] for r in rows]
    t_i = cross(xs, bii, bi)
    t_III = cross(xs, bii, 0.298)
    t_i_frozen = cross(xs[:len(TAUS)], bii[:len(TAUS)], bi)
    t_III_frozen = cross(xs[:len(TAUS)], bii[:len(TAUS)], 0.298)
    o.P(f"   b_i = {bi:+.3f}.  tau*_i = {t_i if t_i is None else round(t_i,2)} (frozen grid alone: {t_i_frozen if t_i_frozen is None else round(t_i_frozen,2)});  tau*_III (b_ii = +0.298) = {t_III if t_III is None else round(t_III,2)} (frozen grid alone: {t_III_frozen if t_III_frozen is None else round(t_III_frozen,2)})")
    C2[nm] = dict(rows=[(r[0], r[1], r[2], r[3]) for r in rows], b_i=bi, tau_star_i=t_i, tau_star_III=t_III, tau_star_i_frozen=t_i_frozen, tau_star_III_frozen=t_III_frozen)
    # constant offsets
    for off in (-0.3, 0.0, 0.3):
        s, _ = slopes(dict(base, off=off))
        o.P(f"   constant offset {off:+.1f}: b_ii {s['ii']:+.3f}  Delta b {s['d']:+.3f}  n(ii) {s['n_ii']}")
    # H2-only tilt
    o.P("   H2-only tilt t_H:")
    for tH in (-0.6, -0.3, 0.0, 0.3, 0.6):
        s, _ = slopes(dict(base, tH=tH))
        o.P(f"      t_H {tH:+.1f}: b_ii {s['ii']:+.3f}  Delta b {s['d']:+.3f}  n(ii) {s['n_ii']}")
    # combined: tau* under H2 tilt and HI tilt
    for what in ("tH", "tg"):
        for v in (-0.3, 0.0, 0.3):
            xs2, b2 = [], []
            for tau in TAUS + TAUS_EXT:
                cfg = dict(base, tau=tau)
                if what == "tH":
                    cfg["tH"] = v
                else:
                    cfg["Sig"] = C["Sig"] * 10 ** (v * (z - zmed))
                s, _ = slopes(cfg)
                xs2.append(tau); b2.append(s["ii"])
            tt = cross(xs2, b2, bi)
            o.P(f"   combined: {what} = {v:+.1f}: tau*_i = {None if tt is None else round(tt, 2)}")
            C2[nm][f"tau_star_i|{what}={v}"] = tt
o.res["C2"] = C2

# ---------------------------------------------------------------- C3 confound
o.P("C3: mass-z confound")
lMf, lMs = C["logMfit"], C["logMsed"]
dstar = lMf - lMs
s_f, s_s, s_d = c.theil_sen(z, lMf), c.theil_sen(z, lMs), c.theil_sen(z, dstar)
o.P(f"   TS slopes on z: log M_fit {s_f:+.3f}; log M*_SED {s_s:+.3f}; Delta* {s_d:+.3f}; corr(z, log M*_SED) = {np.corrcoef(z, lMs)[0,1]:+.2f}; corr(z, log M_fit) = {np.corrcoef(z, lMf)[0,1]:+.2f}")
beta = float(np.polyfit(lMs, lMf, 1)[0])
ex = np.array([float(J[i]["logMstar_phot_err"]) if J[i]["logMstar_phot_err"] not in ("", None) else np.nan for i in ids])
lam = 1 - np.nanmean(ex ** 2) / np.var(lMs)
inv = 1.0 / float(np.polyfit(lMf, lMs, 1)[0])
o.P(f"   beta = slope of log M_fit on log M*_SED: OLS {beta:.2f}; corrected for the SED errors (lambda {lam:.3f}, median err {np.nanmedian(ex):.2f}) {beta/lam:.2f}; inverse-regression bracket {inv:.2f}; quoted M_fit 1-sigma median {np.median(T['DC14_logMdisk_err'][idx]):.2f}")
m9 = lMs - 9.24


def ols_partial(y, cols_list, B_, seed):
    X = np.column_stack([np.ones(len(y))] + cols_list)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    r = np.random.default_rng(seed)
    n = len(y)
    bb = np.empty((B_, X.shape[1]))
    for t in range(B_):
        i = r.integers(0, n, n)
        bb[t] = np.linalg.lstsq(X[i], y[i], rcond=None)[0]
    return b, bb


b, bb = ols_partial(dstar, [z, m9], B, SEED)
dM = float(b[1]); dM_ci = c.ci(bb[:, 1])
b0, bb0 = ols_partial(dstar, [z], B, SEED)
o.P(f"   Delta* OLS slope on z alone {b0[1]:+.3f} [{c.ci(bb0[:,1])[0]:+.3f},{c.ci(bb0[:,1])[1]:+.3f}];  with covariate (log M*_SED - 9.24): d_M = {dM:+.3f} [{dM_ci[0]:+.3f},{dM_ci[1]:+.3f}]; mass coefficient {b[2]:+.3f}")
terc = np.array_split(np.argsort(lMs, kind="stable"), 3)
tercile = []
for k, t in enumerate(terc):
    st, _ = c.slope_table(z[t], {"d": dstar[t]}, B, SEED)
    tercile.append(dict(n=len(t), b=st["d"]["b"], ci=(st["d"]["lo"], st["d"]["hi"]), M_range=(float(lMs[t].min()), float(lMs[t].max())), z_med=float(np.median(z[t]))))
    o.P(f"   M* tercile {k+1} (log M*_SED {lMs[t].min():.2f}-{lMs[t].max():.2f}, n={len(t)}, z range {z[t].min():.2f}-{z[t].max():.2f}): Delta* slope {st['d']['b']:+.3f} [{st['d']['lo']:+.3f},{st['d']['hi']:+.3f}]")
for nm, base in cons.items():
    R = c.routes(C, base)
    for r in ("i", "ii"):
        y = np.log10(R["a0_" + r])
        m = np.isfinite(y)
        bp, bbp = ols_partial(y[m], [z[m], m9[m]], B, SEED)
        b1, bb1 = ols_partial(y[m], [z[m]], B, SEED)
        o.P(f"   [{nm}] log a0,{r}: OLS z slope alone {b1[1]:+.3f}; with M* covariate {bp[1]:+.3f} [{c.ci(bbp[:,1])[0]:+.2f},{c.ci(bbp[:,1])[1]:+.2f}]; M* coefficient {bp[2]:+.3f}")
        o.res.setdefault("C3_a0", {})[f"{nm}|{r}"] = dict(alone=float(b1[1]), partial=float(bp[1]), ci=c.ci(bbp[:, 1]), mcoef=float(bp[2]))
o.res["C3"] = dict(s_fit=s_f, s_sed=s_s, s_dstar=s_d, beta=beta, beta_corr=beta / lam, dM=dM, dM_ci=dM_ci, terciles=tercile)

# ---------------------------------------------------------------- C4 enclosed-mass overshoot
o.P("C4: enclosed-mass overshoot (impossibility test): 0.5 M_r + pi R_e^2 Sigma_HI > M_dyn(<R_e)?  (log_Mdyn read as the total mass within R_e: UNVERIFIED)")
Mdyn = 10 ** C["logMdyn"]
valid = np.isfinite(C["logMdyn"])
MHI = math.pi * C["Re"] ** 2 * 1e6 * C["Sig"]
mu0 = c.mu_mol(z, lMs)
masses = {"fit": 10 ** lMf, "SED+H2": 10 ** lMs * (1 + mu0), "SED": 10 ** lMs}
zlo = z <= zmed
C4 = {}
for nm, M in masses.items():
    enc = 0.5 * M + MHI
    ex_all = (enc > Mdyn) & valid
    ex_mod = (enc > (1 - C["fDM"]) * Mdyn) & valid
    for lab, e in (("> M_dyn", ex_all), ("> (1-fDM) M_dyn", ex_mod)):
        kl, nl = int(e[zlo & valid].sum()), int((zlo & valid).sum())
        kh, nh = int(e[~zlo & valid].sum()), int((~zlo & valid).sum())
        pl, ph = kl / nl, kh / nh
        pp = (kl + kh) / (nl + nh)
        zst = (ph - pl) / math.sqrt(pp * (1 - pp) * (1 / nl + 1 / nh)) if 0 < pp < 1 else float("nan")
        wl, wh = c.wilson(kl, nl), c.wilson(kh, nh)
        o.P(f"   {nm:7s} enclosed {lab:16s}: low-z {kl}/{nl} = {pl:.2f} [{wl[0]:.2f},{wl[1]:.2f}]; high-z {kh}/{nh} = {ph:.2f} [{wh[0]:.2f},{wh[1]:.2f}]; diff z-stat {zst:+.2f}")
        C4[f"{nm}|{lab}"] = dict(f_low=pl, f_high=ph, zstat=zst, k=(kl, nl, kh, nh))
o.res["C4"] = C4

# sensitivity of the C4 / O4 call to the geometry (post-frozen sensitivity, labelled): enclosed fraction and M_dyn scale
o.P("C4 sensitivity (POST-FROZEN, labelled): does O4's condition (f_high >= 25% and diff >= 2 SD) hold for SED+H2 under other geometries?")
sens = {}
for fenc in (0.4, 0.5, 0.6):
    for ms in (0.8, 1.0, 1.25):
        e = ((fenc * masses["SED+H2"] + MHI) > ms * Mdyn) & valid
        kl, nl = int(e[zlo & valid].sum()), int((zlo & valid).sum())
        kh, nh = int(e[~zlo & valid].sum()), int((~zlo & valid).sum())
        pl, ph = kl / nl, kh / nh
        pp = (kl + kh) / (nl + nh)
        zs_ = (ph - pl) / math.sqrt(pp * (1 - pp) * (1 / nl + 1 / nh)) if 0 < pp < 1 else float("nan")
        e0 = ((fenc * masses["fit"] + MHI) > ms * Mdyn) & valid
        sens[f"{fenc}|{ms}"] = dict(f_low=pl, f_high=ph, z=zs_, O4=bool(ph >= 0.25 and zs_ >= 2), fit_low=float(e0[zlo & valid].mean()), fit_high=float(e0[~zlo & valid].mean()))
        o.P(f"   f_enc {fenc}, M_dyn x{ms}: SED+H2 low {pl:.2f} high {ph:.2f} z {zs_:+.2f} O4 {sens[f'{fenc}|{ms}']['O4']};  fit low {sens[f'{fenc}|{ms}']['fit_low']:.2f} high {sens[f'{fenc}|{ms}']['fit_high']:.2f}")
o.P(f"   O4 holds in {sum(v['O4'] for v in sens.values())} of 9 cells")
o.res["C4_sens"] = sens

# ---------------------------------------------------------------- C5 baryons-only bound
o.P("C5: baryons-only fit as an upper bound (no halo): M*_SED(1+mu) above M_disc,bo + M_gas,bo ?")
bod = np.array([float(J[i]["baryons_only_logMdisk"]) if J[i]["baryons_only_logMdisk"] not in ("", None) else np.nan for i in ids])
bog = np.array([float(J[i]["baryons_only_logMgas"]) if J[i]["baryons_only_logMgas"] not in ("", None) else np.nan for i in ids])
Mbo = 10 ** bod + 10 ** bog
okb = np.isfinite(Mbo)
for nm, M in (("SED+H2", masses["SED+H2"]), ("SED", masses["SED"]), ("fit", masses["fit"])):
    e = (M > Mbo) & okb
    kl, nl = int(e[zlo & okb].sum()), int((zlo & okb).sum())
    kh, nh = int(e[~zlo & okb].sum()), int((~zlo & okb).sum())
    o.P(f"   {nm:7s} > M_disc,bo + M_gas,bo: low-z {kl}/{nl}, high-z {kh}/{nh}")
    e2 = (M > 10 ** bod) & np.isfinite(bod)
    o.P(f"   {nm:7s} > M_disc,bo alone: low-z {int(e2[zlo].sum())}/{int(zlo.sum())}, high-z {int(e2[~zlo].sum())}/{int((~zlo).sum())}")
d_bo = bod - lMs
o.P(f"   M_disc,bo - M*_SED: median {np.nanmedian(d_bo):+.2f}; TS slope on z {c.theil_sen(z, d_bo):+.3f}; M_disc,bo - M_fit TS slope {c.theil_sen(z, bod - lMf):+.3f}")
o.res["C5"] = dict(bo_minus_sed_slope=c.theil_sen(z, d_bo), bo_minus_fit_slope=c.theil_sen(z, bod - lMf))

# ---------------------------------------------------------------- C6 sSFR (weak)
o.P("C6: sSFR test (WEAK; main-sequence evolution expected about +0.67 +- 0.3 dex/z is FROM MEMORY, UNVERIFIED; SFR read as log10 SFR)")
logsfr = np.array([float(J[i]["SFR"]) if J[i]["SFR"] not in ("", None) else np.nan for i in ids])
ssfr = logsfr - lMs
q1, q3 = np.percentile(lMs, [25, 75])
w = (lMs >= q1) & (lMs <= q3) & np.isfinite(ssfr)
st6, _ = c.slope_table(z[w], {"s": ssfr[w]}, B, SEED)
bp, bbp = ols_partial(ssfr[np.isfinite(ssfr)], [z[np.isfinite(ssfr)], m9[np.isfinite(ssfr)]], B, SEED)
obs6 = st6["s"]["b"]
o.P(f"   window log M*_SED in [{q1:.2f},{q3:.2f}] (n={int(w.sum())}): TS slope of log sSFR on z {obs6:+.3f} [{st6['s']['lo']:+.2f},{st6['s']['hi']:+.2f}]; OLS with M* covariate {bp[1]:+.3f} [{c.ci(bbp[:,1])[0]:+.2f},{c.ci(bbp[:,1])[1]:+.2f}]")
tau6 = 0.67 - obs6
o.P(f"   implied tau ~ expected - observed = {tau6:+.2f} dex/z (vs the tau needed, section C2); caveat: SFR and M* likely from the same SED fit; selection")
o.res["C6"] = dict(obs=obs6, ci=(st6["s"]["lo"], st6["s"]["hi"]), tau_implied=tau6, ols_cov=float(bp[1]))

# ---------------------------------------------------------------- decision table
o.P("\nDECISION TABLE (frozen section 9; conditions evaluated as written)")
B_PL = 0.25
ti = {nm: C2[nm]["tau_star_i"] for nm in C2}
o.P(f"   tau*_i per construction: {ti}; B_pl = {B_PL}")


def cond(f):
    vals = [f(v) for v in ti.values()]
    return all(vals)


tau_gt = cond(lambda v: v is not None and v > 0.4)
tau_le = cond(lambda v: v is not None and v <= B_PL)
f_key = "SED+H2|> M_dyn"
fl, fh, zst = C4[f_key]["f_low"], C4[f_key]["f_high"], C4[f_key]["zstat"]
o1_dM = dM <= -0.4 and dM_ci[1] < -0.1
o1_c4 = (abs(zst) < 2 if np.isfinite(zst) else True) and fl <= 0.10 and fh <= 0.10
O1 = tau_gt and o1_dM and o1_c4
O2 = tau_le
O3 = abs(dM) <= 0.25 and dM_ci[0] <= 0 <= dM_ci[1]
O4 = fh >= 0.25 and zst >= 2
o.P(f"   O1: tau*_i > 0.4 on all constructions {tau_gt}; d_M <= -0.4 with upper CI < -0.1: {o1_dM} (d_M {dM:+.2f}, upper {dM_ci[1]:+.2f}); C4 silent (f_low {fl:.2f}, f_high {fh:.2f}, z {zst:+.2f}): {o1_c4}  -> O1 = {O1}")
o.P(f"   O2: tau*_i <= 0.25 on all constructions: {O2}")
o.P(f"   O3: |d_M| <= 0.25 and CI contains 0: {O3}")
o.P(f"   O4: f_high >= 25% and diff >= 2 SD: {O4}")
held = [n for n, v in (("O1", O1), ("O2", O2), ("O3", O3), ("O4", O4)) if v]
outcome = held if held else ["O5"]
o.P(f"   OUTCOME: {outcome} (O5 is the default when none of O1-O4 holds)")
o.P(f"   weak counter-check C6: implied tau {tau6:+.2f} vs the O1/O2 call: differs from tau*_i by more than B_pl? { {k: (v is not None and abs(tau6 - v) > B_PL) for k, v in ti.items()} }")
o.res["decision"] = dict(outcome=outcome, tau_star_i=ti, dM=dM, dM_ci=dM_ci, f_low=fl, f_high=fh, zstat=zst, O=dict(O1=O1, O2=O2, O3=O3, O4=O4))
o.finish()
sys.exit(0)
