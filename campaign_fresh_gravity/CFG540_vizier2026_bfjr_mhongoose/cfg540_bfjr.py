#!/usr/bin/env python3
"""CFG540 Part A: Tian+2026 baryonic Faber-Jackson relation (VizieR J/A+A/710/L39) under the law (FROZEN_CRITERIA.md).

Spherical self-consistent baryons (Hernquist: ellipticals, groups; Plummer: dwarfs), constant-beta Jeans, sigma_e inside Re
(groups: aperture infinity), kernel nu_mono, round rule, no EFE, census edge (CFG515 fret_census, read-only import).
kappa = 1/2 FITTED; footings 9.36e-11 / 1.13e-10 never pooled. Cold energy mass required. Not "theory closed".
CFG540_MUTATE=1 -> M1 Newtonian, M2 a0 x 4, M3 within-sub-sample sigma shuffle; outputs *_MUTATE.*
Data path: env CFG540_DATA or ../../../_external_data/vizier2026 relative to this file.
"""
import os, sys, json, math
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np
if not hasattr(np, "trapezoid"): np.trapezoid = np.trapz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG515_census_edge_resolution"))
from cfg515_lib import fret_census, ln_fac  # noqa: E402

DATA = os.environ.get("CFG540_DATA", os.path.join(HERE, "..", "..", "..", "_external_data", "vizier2026"))
MUT = os.environ.get("CFG540_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
FOOT = {"can": 9.36e-11, "alt": 1.13e-10}
BETAS = (0.0, -0.3, 0.3)
CLASS = {"MaNGA elliptical": "ELLIPTICALS", "ATLAS elliptical": "ELLIPTICALS", "Galaxy group": "GROUPS",
         "Fornax dwarf": "DWARFS", "Virgo dwarf": "DWARFS", "Local Group dwarf": "DWARFS"}
HERN_RE = 1.8153
OUT = []


def log(s=""):
    print(s); OUT.append(s)


def read_tian():
    rows = []
    for l in open(os.path.join(DATA, "J_A_A_710_L39.tsv")):
        if l.startswith("#"): continue
        r = l.rstrip("\n").split("\t")
        if len(r) < 13 or not r[0].strip().isdigit(): continue
        rows.append(dict(sample=r[1].strip(), id=r[2].strip(), ls=float(r[5]), els=float(r[6]), lM=float(r[7]),
                         elM=float(r[8]), lg=float(r[9]), Re=float(r[10]), lFP=float(r[11])))
    return rows


# ---------------- dimensionless model: G M = 1, a = 1 ----------------
X = np.logspace(-5, 5, 3000)
LX = np.log(X)


def prof(kind, x):
    if kind == "hern":
        return 1.0 / (2 * np.pi * x * (1 + x) ** 3), x ** 2 / (1 + x) ** 2
    return 3.0 / (4 * np.pi) * (1 + x ** 2) ** -2.5, x ** 3 / (1 + x ** 2) ** 1.5


def nu(y, newton=False):
    if newton: return np.ones_like(y)
    s = np.sqrt(y)
    return np.where(s > 1e-8, 1.0 / (-np.expm1(-s)), 1.0 / np.maximum(s, 1e-300))


def field(kind, a0d, xedge, newton=False):
    rho, m = prof(kind, X)
    gN = m / X ** 2
    g = nu(gN / a0d, newton) * gN
    if xedge is not None and xedge < X[-1]:
        mph = (g - gN) * X ** 2
        mph_e = np.interp(np.log(xedge), LX, mph)
        out = X > xedge
        g = np.where(out, (m + mph_e) / X ** 2, g)
    return rho, g


def sigma2(kind, a0d, beta, aperture, xedge=None, newton=False):
    """light-weighted LOS sigma^2 in units GM/a inside projected radius `aperture` (in a); None -> whole system."""
    rho, g = field(kind, a0d, xedge, newton)
    if aperture is None:
        return np.trapezoid(4 * np.pi * X ** 2 * rho * X * g * X, LX) / 3.0
    f = X ** (2 * beta) * rho * g * X                      # integrand d(ln x)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(LX))])
    P = X ** (-2 * beta) * (cum[-1] - cum)                 # rho sigma_r^2
    P = np.maximum(P, 1e-300)
    lP = np.log(P); lrho = np.log(rho)
    R = np.logspace(-4, np.log10(aperture), 160)
    tmax = np.arccosh(X[-1] / R)
    u = np.linspace(0, 1, 700)
    T = tmax[:, None] * u[None, :]
    r = R[:, None] * np.cosh(T)
    lr = np.log(r)
    Pr = np.exp(np.interp(lr, LX, lP)); rr = np.exp(np.interp(lr, LX, lrho))
    w = r * tmax[:, None]
    Ssp = 2 * np.trapezoid((1 - beta / np.cosh(T) ** 2) * Pr * w, u, axis=1)
    S = 2 * np.trapezoid(rr * w, u, axis=1)
    lR = np.log(R)
    return np.trapezoid(Ssp * R ** 2, lR) / np.trapezoid(S * R ** 2, lR)


def predict(o, a0, beta, edge=True, newton=False, dlM=0.0):
    kind = "hern" if CLASS[o["sample"]] in ("ELLIPTICALS", "GROUPS") else "plum"
    M = 10 ** (o["lM"] + dlM) * MSUN
    a = o["Re"] * KPC / (HERN_RE if kind == "hern" else 1.0)
    GM = G * M
    a0d = a0 * a * a / GM
    xedge = None
    if edge:
        f = fret_census(10 ** (o["lM"] + dlM))[0]
        xedge = (1.0 / math.sqrt(a0d)) / ln_fac(f)
    ap = None if CLASS[o["sample"]] == "GROUPS" else (o["Re"] * KPC / a)
    s2 = sigma2(kind, a0d, beta, ap, xedge, newton) * GM / a
    return 0.5 * math.log10(s2) - 3.0, (xedge * a / (o["Re"] * KPC) if xedge else None)


def class_stats(d, s, els):
    d = np.asarray(d); s = np.asarray(s); n = len(d)
    w = 1 / (els ** 2)
    m = float(d.mean()); se = float(d.std(ddof=1) / math.sqrt(n))
    sys_ = float(np.mean(s) * 0.10); tot = math.hypot(se, sys_)
    Z = m / tot
    if tot > 0.045: v = "NOT DIAGNOSTIC"
    elif abs(Z) < 2: v = "CONSISTENT"
    elif Z >= 2: v = "ABOVE LAW" + (" (strong)" if Z >= 3 else "")
    else: v = "BELOW LAW" + (" (strong)" if Z <= -3 else "")
    return dict(N=n, mean=m, se=se, sys=sys_, tot=tot, Z=Z, Z_stat=m / se, wmean=float(np.sum(w * d) / np.sum(w)),
                median=float(np.median(d)), rms=float(d.std(ddof=1)), verdict=v)


def main():
    rows = read_tian()
    log(f"CFG540 Part A {'MUTATE' if MUT else 'PRIMARY'}: Tian+2026 BFJR, N = {len(rows)}; kappa = 1/2 FITTED; footings never pooled")
    # K3
    k3 = max(abs(o["lFP"] - math.log10(5 * o["Re"] * KPC * (10 ** o["ls"] * 1e3) ** 2 / G / MSUN)) for o in rows)
    log(f"K3 logFPmass reproduces 5 Re sigma^2/G: max |diff| = {k3:.4f} dex -> {'PASS' if k3 < 0.01 else 'FAIL'}")
    # K2
    s2n = sigma2("hern", 1.0, 0.0, None, None, newton=True)
    k2 = abs(3 * s2n / (1 / 6.0) - 1)
    log(f"K2 Newtonian Hernquist 3D <v^2> = 3 sigma_los^2 vs GM/(6a): rel err {k2:.2e} -> {'PASS' if k2 < 5e-3 else 'FAIL'}"
        f" (the frozen text's 'sigma^2 = GM/(6a)' is the 3D mean square; LOS is GM/(18a))")
    res = dict(N=len(rows), K3_maxdiff=k3, K2_relerr=k2, footings={})
    a0mult = 1.0
    runs = {}
    if not MUT:
        runs = {f"beta{b:+.1f}": dict(beta=b, edge=True, newton=False) for b in BETAS}
        runs["beta+0.0_noedge"] = dict(beta=0.0, edge=False, newton=False)
    else:
        runs = {"M0_primary": dict(beta=0.0, edge=True, newton=False),
                "M1_newton": dict(beta=0.0, edge=True, newton=True),
                "M2_a0x4": dict(beta=0.0, edge=True, newton=False, a0x=4.0)}
    for fk, a00 in FOOT.items():
        log(f"\n=== footing {fk}: a0 = {a00:.3e} ===")
        # K1
        gr = [o for o in rows if o["sample"] == "Galaxy group"]
        k1 = []
        for o in gr:
            M = 10 ** o["lM"] * MSUN; a = o["Re"] * KPC / HERN_RE
            if G * M / (o["Re"] * KPC) ** 2 / a00 < 1e-3:
                lp, _ = predict(o, a00, 0.0, edge=False)
                k1.append(abs(lp - (0.25 * math.log10(4 / 81 * G * M * a00) - 3)))
        log(f"K1 deep-MOND 4/81 limit on {len(k1)} groups with y<1e-3: max |diff| = {max(k1):.4f} dex -> "
            f"{'PASS' if max(k1) < 0.01 else 'FAIL'}")
        fr = dict(K1_n=len(k1), K1_maxdiff=max(k1), runs={})
        prim = None
        for rk, rc in runs.items():
            a0 = a00 * rc.get("a0x", 1.0)
            lp = np.zeros(len(rows)); xe = np.full(len(rows), np.nan); s = np.zeros(len(rows))
            for i, o in enumerate(rows):
                lp[i], xe_i = predict(o, a0, rc["beta"], rc["edge"], rc["newton"])
                if xe_i is not None: xe[i] = xe_i
                if rk in ("beta+0.0", "M0_primary") or MUT:
                    lp2, _ = predict(o, a0, rc["beta"], rc["edge"], rc["newton"], dlM=0.01)
                    s[i] = (lp2 - lp[i]) / 0.01
            if not np.any(s):
                s = prim["s"]
            ls = np.array([o["ls"] for o in rows]); els = np.array([o["els"] for o in rows])
            elM = np.array([o["elM"] for o in rows])
            D = ls - lp
            eD = np.sqrt(els ** 2 + (s * elM) ** 2)
            cls = np.array([CLASS[o["sample"]] for o in rows]); smp = np.array([o["sample"] for o in rows])
            out = dict(classes={}, samples={})
            log(f"\n-- run {rk} (beta {rc['beta']:+.1f}, edge {rc['edge']}, newton {rc['newton']}, a0 x {rc.get('a0x', 1.0)})")
            for c in ("GROUPS", "ELLIPTICALS", "DWARFS"):
                k = cls == c
                st = class_stats(D[k], s[k], eD[k]); out["classes"][c] = st
                log(f"  {c:12s} N {st['N']:4d}  mean {st['mean']:+.3f}  SE {st['se']:.3f}  sys {st['sys']:.3f}  Z {st['Z']:+.2f}"
                    f" (Z_stat {st['Z_stat']:+.1f})  wmean {st['wmean']:+.3f}  med {st['median']:+.3f}  rms {st['rms']:.3f}  -> {st['verdict']}")
            for c in sorted(set(smp)):
                k = smp == c
                st = class_stats(D[k], s[k], eD[k]); out["samples"][c] = st
                log(f"    {c:18s} N {st['N']:4d}  mean {st['mean']:+.3f} +- {st['se']:.3f}  med {st['median']:+.3f}  rms {st['rms']:.3f}  "
                    f"s {np.mean(s[k]):.3f}")
            if rk in ("beta+0.0", "M0_primary"):
                prim = dict(D=D, s=s, lp=lp)
            if rc["edge"]:
                out["edge_over_Re_min_by_class"] = {c: float(np.nanmin(xe[cls == c])) for c in ("GROUPS", "ELLIPTICALS", "DWARFS")}
                log(f"  r_edge/Re min: " + ", ".join(f"{c} {v:.1f}" for c, v in out["edge_over_Re_min_by_class"].items()))
            out["Delta"] = [float(v) for v in D]
            fr["runs"][rk] = out
        if not MUT:
            # edge shift
            Dp = np.array(fr["runs"]["beta+0.0"]["Delta"]); Dn = np.array(fr["runs"]["beta+0.0_noedge"]["Delta"])
            cls = np.array([CLASS[o["sample"]] for o in rows])
            sh = {c: float(np.max(np.abs(Dp[cls == c] - Dn[cls == c]))) for c in ("GROUPS", "ELLIPTICALS", "DWARFS")}
            shm = {c: float(np.mean(Dp[cls == c] - Dn[cls == c])) for c in ("GROUPS", "ELLIPTICALS", "DWARFS")}
            fr["edge_shift_maxabs"] = sh; fr["edge_shift_mean"] = shm
            log("\nEdge vs no-edge (Delta_edge - Delta_noedge): " + ", ".join(
                f"{c} mean {shm[c]:+.4f} max|.| {sh[c]:.4f} -> {'irrelevant' if sh[c] < 0.005 else 'MATTERS'}" for c in sh))
            # trend with gbar
            D = prim["D"]
            x = np.array([o["lg"] for o in rows]) - math.log10(a00)
            xp = np.array([math.log10(G * 10 ** o["lM"] * MSUN / (2 * (o["Re"] * KPC) ** 2) / a00) for o in rows])
            rng = np.random.default_rng(540)
            tr = {}
            for nm, xx in (("catalogue_gbar", x), ("GM_over_2Re2", xp)):
                sl = float(np.polyfit(xx, D, 1)[0])
                bs = [np.polyfit(xx[idx], D[idx], 1)[0] for idx in (rng.integers(0, len(D), len(D)) for _ in range(2000))]
                edges = np.arange(math.floor(xx.min() * 2) / 2, xx.max() + 0.5, 0.5)
                bins = []
                for lo in edges[:-1]:
                    k = (xx >= lo) & (xx < lo + 0.5)
                    if k.sum() >= 10:
                        bins.append(dict(lo=float(lo), N=int(k.sum()), mean=float(D[k].mean()), se=float(D[k].std(ddof=1) / math.sqrt(k.sum()))))
                bad = [b for b in bins if abs(b["mean"]) > 0.10]
                tr[nm] = dict(slope=sl, slope_se=float(np.std(bs)), span_dex=float(xx.max() - xx.min()), bins=bins,
                              verdict="TRACKS" if not bad else "DOES NOT TRACK", out_of_range=[b["lo"] for b in bad])
                log(f"\nTrend vs {nm} (log g/a0 span {xx.min():.2f}..{xx.max():.2f}): slope {sl:+.4f} +- {np.std(bs):.4f} dex/dex -> "
                    f"{tr[nm]['verdict']} {('out-of-range bins ' + str(tr[nm]['out_of_range'])) if bad else ''}")
                for b in bins:
                    log(f"   [{b['lo']:+.1f},{b['lo'] + 0.5:+.1f}) N {b['N']:4d} mean {b['mean']:+.3f} +- {b['se']:.3f}")
            fr["trend"] = tr
            # replication rule
            rep = {}
            for c in ("ELLIPTICALS", "GROUPS"):
                sts = [fr["runs"][f"beta{b:+.1f}"]["classes"][c] for b in BETAS]
                yes = all(st["mean"] >= 0.035 and st["Z"] >= 2 for st in sts)
                no = all(st["mean"] + 2 * st["tot"] < 0.07 for st in sts)
                rep[c] = "REPLICATES" if yes else ("DOES NOT REPLICATE" if no else "NOT DIAGNOSTIC / beta-DEPENDENT")
                log(f"Massive-system tension, {c}: means at beta 0/-0.3/+0.3 = " + "/".join(f"{st['mean']:+.3f}" for st in sts)
                    + f" -> {rep[c]}")
            fr["replication"] = rep
            # beta-robust verdicts
            fv = {}
            for c in ("GROUPS", "ELLIPTICALS", "DWARFS"):
                vs = [fr["runs"][f"beta{b:+.1f}"]["classes"][c]["verdict"].replace(" (strong)", "") for b in BETAS]
                fv[c] = vs[0] if len(set(vs)) == 1 else "beta-DEPENDENT (" + "/".join(vs) + ")"
            fr["final_verdicts"] = fv
            log("FINAL class verdicts: " + "; ".join(f"{c}: {v}" for c, v in fv.items()))
            # massive end and mass slope inside ellipticals
            smp = np.array([o["sample"] for o in rows]); lM = np.array([o["lM"] for o in rows])
            k = (smp == "MaNGA elliptical") & (lM >= 11.3)
            ke = np.array([CLASS[o["sample"]] for o in rows]) == "ELLIPTICALS"
            msl = float(np.polyfit(lM[ke], D[ke], 1)[0])
            fr["manga_massive"] = dict(N=int(k.sum()), mean=float(D[k].mean()), se=float(D[k].std(ddof=1) / math.sqrt(k.sum())))
            fr["ellipticals_Delta_vs_logM_slope"] = msl
            log(f"MaNGA log Mb >= 11.3: N {k.sum()} mean {D[k].mean():+.3f} +- {fr['manga_massive']['se']:.3f}; "
                f"ELLIPTICALS dDelta/dlogMb = {msl:+.3f}")
            # mass bins inside ellipticals
            mb = []
            for lo in np.arange(9.0, 12.5, 0.5):
                kk = ke & (lM >= lo) & (lM < lo + 0.5)
                if kk.sum() >= 10:
                    mb.append(dict(lo=float(lo), N=int(kk.sum()), mean=float(D[kk].mean()), se=float(D[kk].std(ddof=1) / math.sqrt(kk.sum()))))
                    log(f"   ELL logMb [{lo:.1f},{lo + 0.5:.1f}) N {kk.sum():4d} mean {D[kk].mean():+.3f} +- {mb[-1]['se']:.3f}")
            fr["ellipticals_mass_bins"] = mb
            # no-EFE readout
            kc = (smp == "Fornax dwarf") | (smp == "Virgo dwarf"); kl = smp == "Local Group dwarf"
            dd = float(D[kc].mean() - D[kl].mean())
            ed = float(math.hypot(D[kc].std(ddof=1) / math.sqrt(kc.sum()), D[kl].std(ddof=1) / math.sqrt(kl.sum())))
            fr["noEFE_readout"] = dict(cluster_mean=float(D[kc].mean()), LG_mean=float(D[kl].mean()), diff=dd, diff_se=ed)
            log(f"No-EFE readout: cluster dwarfs {D[kc].mean():+.3f}, LG dwarfs {D[kl].mean():+.3f}, diff {dd:+.3f} +- {ed:.3f} "
                f"(Z {dd / ed:+.2f}); descriptive")
        else:
            # M1/M2 verdicts
            m = {}
            for rk in ("M1_newton", "M2_a0x4"):
                vv = {c: fr["runs"][rk]["classes"][c]["verdict"] for c in ("GROUPS", "DWARFS")}
                m[rk] = dict(verdicts=vv, fails_as_required=all(not v.startswith("CONSISTENT") for v in vv.values()))
                log(f"{rk}: {vv} -> {'MUTATE OK (not consistent)' if m[rk]['fails_as_required'] else 'MUTATE FAIL'}")
            # M3 shuffle
            D0 = prim["D"]; lp0 = prim["lp"]
            ls = np.array([o["ls"] for o in rows]); smp = np.array([o["sample"] for o in rows])
            cls = np.array([CLASS[o["sample"]] for o in rows])
            rng = np.random.default_rng(540)
            m3 = {}
            for c in ("ELLIPTICALS", "DWARFS"):
                k = cls == c
                true_rms = float(D0[k].std(ddof=1)); cnt = 0
                for _ in range(200):
                    lsh = ls.copy()
                    for sname in set(smp[k]):
                        idx = np.where(smp == sname)[0]
                        lsh[idx] = rng.permutation(ls[idx])
                    if (lsh - lp0)[k].std(ddof=1) > true_rms: cnt += 1
                m3[c] = dict(true_rms=true_rms, frac_shuffle_larger=cnt / 200)
                log(f"M3 shuffle {c}: true rms {true_rms:.3f}; shuffles with larger rms {cnt}/200 -> "
                    f"{'MUTATE OK' if cnt >= 190 else 'MUTATE FAIL'}")
            m["M3"] = m3
            m["pass"] = bool(m["M1_newton"]["fails_as_required"] and m["M2_a0x4"]["fails_as_required"]
                             and all(v["frac_shuffle_larger"] >= 0.95 for v in m3.values()))
            fr["mutate"] = m
            log(f"MUTATE overall ({fk}): {'PASS' if m['pass'] else 'FAIL'}")
        res["footings"][fk] = fr
    with open(os.path.join(HERE, f"cfg540_bfjr{TAG}_results.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    with open(os.path.join(HERE, f"cfg540_bfjr{TAG}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
