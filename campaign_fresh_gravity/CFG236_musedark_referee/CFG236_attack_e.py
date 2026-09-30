"""CFG236 attack (e): III's own law as a sanity anchor on III's route (route (i)).  Seed 2364.
III's law (quoted by CFG198 from CFG190, NOT verified by me): a0(z) = a0(0) + a1 z, a0(0)=1.0, a1=1.59 (x1e-10 m/s^2), ratio a1/a0(0) = 1.59."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG236_common as c

SEED = 2364
B = 2000
o = c.Out("attack_e")
c.header(o, "CFG236 attack (e): III's law anchor")
T = c.load_numeric()
idx, cnt = c.sample(T)
C = c.get_cols(T, idx)
z = C["z"]
DAT = c.dat_available()
cons = {"R198": dict(mode="R198")}
if DAT:
    dat = c.load_dat(T, idx)
    cons["R199a"] = dict(mode="R199", gperp=c.gperp_reading(dat["v1"], C["Re"], C["incl"], "a"))
    cons["R199b"] = dict(mode="R199", gperp=c.gperp_reading(dat["v1"], C["Re"], C["incl"], "b"))
    cons["R199a+D1"] = dict(mode="R199", gperp=c.gperp_reading(dat["v1"], C["Re"], C["incl"], "a", dat["s1"], "D1"))
    cons["R199b+D1"] = dict(mode="R199", gperp=c.gperp_reading(dat["v1"], C["Re"], C["incl"], "b", dat["s1"], "D1"))


def lin_ts(zz, a):
    """Theil-Sen of a (linear, 1e-10 m/s^2) on z: slope B, intercept A = median(a - B z)."""
    Bs = c.theil_sen(zz, a)
    A = float(np.median(a - Bs * zz))
    return Bs, A


def lin_boot(zz, a, B_, seed):
    r = np.random.default_rng(seed)
    n = len(zz)
    out = np.empty((B_, 2))
    for t in range(B_):
        i = r.integers(0, n, n)
        bs = c.theil_sen(zz[i], a[i])
        out[t] = (bs, np.median(a[i] - bs * zz[i]))
    return out


def III(zz):
    return 1.0 + 1.59 * zz


res = {}
for nm, base in cons.items():
    for sub, sel in (("all S", np.ones(len(z), bool)), ("III-like cuts (M*_SED>10^8.8, 0.33<z<1.44)", (C["logMsed"] > 8.8) & (z > 0.33) & (z < 1.44))):
        R = c.routes(C, base)
        for r in ("i", "ii"):
            a = R["a0_" + r] * c.CONV / 1e-10
            m = np.isfinite(a) & sel
            zz, aa = z[m], a[m]
            Bl, A = lin_ts(zz, aa)
            bo = lin_boot(zz, aa, B, SEED)
            ratio_b = bo[:, 0] / bo[:, 1]
            ratio_b = ratio_b[np.isfinite(ratio_b)]
            ratio = Bl / A if A != 0 else float("nan")
            sdr = float(np.std(ratio_b)) if len(ratio_b) else float("nan")
            # log slope vs III reference over these galaxies
            logs = np.log10(aa)
            bl = c.theil_sen(zz, logs)
            cols = {"x": np.where(m, np.log10(R["a0_" + r]), np.nan)}
            st, _ = c.slope_table(z, cols, B, SEED)
            ref = c.ref_slopes(zz)["III"]
            inside = st["x"]["lo"] <= ref <= st["x"]["hi"]
            # level at the lowest third
            th = c.thirds(zz)
            lev_med = float(np.median(aa[th[0]]))
            zl = float(np.median(zz[th[0]]))
            III_lev = float(III(zl))
            dex = math.log10(lev_med / III_lev)
            # E1b: level-free, intercept-free anchor: ratio of the highest to the lowest z-third medians of a0 against III's ratio
            r2 = np.random.default_rng(SEED + 1)
            a_lo, a_hi = aa[th[0]], aa[th[2]]
            z_lo_, z_hi_ = float(np.median(zz[th[0]])), float(np.median(zz[th[2]]))
            obs_lr = math.log10(np.median(a_hi) / np.median(a_lo))
            III_lr = math.log10(III(z_hi_) / III(z_lo_))
            bl_ = [math.log10(np.median(r2.choice(a_hi, len(a_hi))) / np.median(r2.choice(a_lo, len(a_lo)))) for _ in range(B)]
            sd_lr = float(np.std(bl_))
            e1b = (obs_lr - III_lr) / sd_lr
            verdict_slope = (abs(ratio - 1.59) <= 2 * sdr) and inside
            verdict = "PASS" if (verdict_slope and abs(dex) <= 0.15) else ("PARTIAL" if verdict_slope else "FAIL")
            key = f"{nm}|{r}|{sub[:5]}"
            res[key] = dict(n=int(m.sum()), B_lin=Bl, A=A, ratio=ratio, sd_ratio=sdr, log_slope=st["x"]["b"], ci=(st["x"]["lo"], st["x"]["hi"]), III_ref=ref, inside=bool(inside),
                            level=lev_med, z_low=zl, III_level=III_lev, dex=dex, verdict=verdict, obs_third_ratio_dex=obs_lr, III_third_ratio_dex=III_lr, sd_third=sd_lr, e1b_sd=e1b)
            o.P(f"[{nm}] route ({r}) {sub}: n={int(m.sum())}  linear TS: B = {Bl:+.2f}, A(z=0) = {A:+.2f} (x1e-10), B/A = {ratio:+.2f} (bootstrap SD {sdr:.2f}; III 1.59);  log slope {st['x']['b']:+.3f} [{st['x']['lo']:+.2f},{st['x']['hi']:+.2f}] vs III {ref:+.3f} ({'inside' if inside else 'OUTSIDE'});  lowest-third level {lev_med:.2f}e-10 at z={zl:.2f} vs III {III_lev:.2f}e-10: {dex:+.2f} dex  -> {verdict}")
            o.P(f"      E1b third-median ratio (z {z_lo_:.2f} -> {z_hi_:.2f}): observed {obs_lr:+.2f} dex, III {III_lr:+.2f} dex, difference {e1b:+.1f} SD (SD {sd_lr:.2f})")
o.res = res
o.P("\nE5: III's 79-galaxy multi-radius RAR fit is not this R_e-only per-galaxy construction; a failed match here is 'not reproduced at R_e on this construction', not a failure of III.")
o.finish()
sys.exit(0)
