#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR4_ungc_group_census.py -- how many Local Volume groups in the UNGC on disk actually have a measurable Hubble-flow
zero-velocity radius?  Cross-thread review, 2026-09-26.  New code; reads real_research/data/ungc_karachentsev2013.tsv.

WHY.  The 09-03 hunt's "highest-value follow-up" (predictions_2026/SECOND_LAW_HUNT_2026.md, lines 570-573) assumed
"~30 Local Volume groups with Hubble-flow coverage" and derived sigma ~ 0.371/sqrt(30) = 0.068 dex.  The same commit's
hunt_2026/k_dimensional_turnaround_groups.py measured SEVEN hand-picked groups and found only the Local Group stable
(its Monte Carlo: external groups recover a known R_0 to 0.22-0.37 dex; the limit is the ~100 km/s flow scatter, not N).
This census applies k_dimensional's own selection to EVERY main disturber in the catalogue.

SELECTION (copied from k_dimensional_turnaround_groups.py lines 122 and 162-171, unchanged): accurate distances (TRGB,
Cep, RR, HB, CMD); group-centric deprojection V_gc = (Vlg_g - Vlg_c)/(rhat.u_g) with |rhat.u_g| > 0.5; galaxies bound to
a DIFFERENT main disturber excluded; linear fit V_gc = H (R - R_0).  Two inner cuts are reported: rlo = 0.15 Mpc (what
the committed code does -- measure_R0's default) and rlo = 0.7 Mpc (what its printed text says it does).
STABILITY (k_dimensional's pre-specified criterion): bootstrap 16-84% interval positive; half-width < 25% of R_0; R_0
moves by less than the half-width when the outer cut goes 3.5 -> 2.5 Mpc or the geometry cut 0.5 -> 0.7.

CHECKS
  C1 CONTROL: the seven committed groups reproduce k_dimensional's N (34, 29, 19, 18, 21, 14, 16) and the LG's R_0 = 0.906.
  N1 (reported) the number of main disturbers with >= 8 usable galaxies, and how many pass the stability criterion.
  N2 THE PREMISE: at least 20 groups are usable AND stable (what a ~0.07 dex ensemble needs at 0.3 dex per group).
Runtime < 30 s.  Writes XR4_ungc_group_census_results.json.
"""
import os, sys, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
from hunt_lib import vizier_tsv, _f   # noqa: E402

T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "XR4_ungc_group_census", "checks": {}, "numbers": {}}
CH = []
rng = np.random.default_rng(20260926)


def check(name, ok, measured):
    ok = bool(ok); CH.append((name, ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")


rows = vizier_tsv("ungc_karachentsev2013.tsv")
name = np.array([r["Name"].strip() for r in rows])
ra = np.array([_f(r["_RAJ2000"]) for r in rows]); de = np.array([_f(r["_DEJ2000"]) for r in rows])
dist = np.array([_f(r["Dist"]) for r in rows]); vlg = np.array([_f(r["Vlg"]) for r in rows])
klum = np.array([_f(r["KLum"]) for r in rows])
ti1 = np.array([_f(r["Ti1"]) for r in rows]); md = np.array([r["MD"].strip() for r in rows])
fdis = np.array([r["f_Dist"].strip() for r in rows])
ACC = np.isin(fdis, ["TRGB", "Cep", "RR", "HB", "CMD"])
a_, d_ = np.radians(ra), np.radians(de)
U = np.array([np.cos(d_) * np.cos(a_), np.cos(d_) * np.sin(a_), np.sin(d_)])
POS = dist[None, :] * U
FIN = np.isfinite(vlg) & np.isfinite(dist) & (dist > 0)


def measure(cvec, cvel, iexcl, mdname, rlo=0.15, rhi=3.5, mu_min=0.5, boot=1000):
    rvec = POS - cvec[:, None]; R = np.linalg.norm(rvec, axis=0)
    mu = np.sum(rvec / np.maximum(R, 1e-9) * U, axis=0)
    elsewhere = (ti1 > 0) & (md != (mdname if mdname else "@@none@@"))
    with np.errstate(invalid="ignore", divide="ignore"):
        Vgc = (vlg - cvel) / np.where(np.abs(mu) > 1e-9, mu, np.nan)
    sel = ACC & FIN & np.isfinite(Vgc) & (R > rlo) & (R < rhi) & (np.abs(mu) > mu_min) & ~elsewhere
    if iexcl is not None: sel[iexcl] = False
    x, y = R[sel], Vgc[sel]
    if sel.sum() < 8: return None
    A = np.vstack([x, np.ones(len(x))]).T
    h, b = np.linalg.lstsq(A, y, rcond=None)[0]
    bs = []
    for _ in range(boot):
        s2 = rng.integers(0, len(x), len(x))
        hh, bb = np.linalg.lstsq(A[s2], y[s2], rcond=None)[0]
        if abs(hh) > 1e-6: bs.append(-bb / hh)
    bs = np.array(bs)
    return dict(R0=(-b / h if h != 0 else np.nan), H=h, N=int(sel.sum()), rms=float((y - h * x - b).std()),
                lo=float(np.percentile(bs, 16)), hi=float(np.percentile(bs, 84)))


def stable(r, v25, v70):
    if r is None or v25 is None or v70 is None: return False
    hw = 0.5 * (r["hi"] - r["lo"])
    return r["lo"] > 0 and hw < 0.25 * r["R0"] and abs(v25["R0"] - r["R0"]) < hw and abs(v70["R0"] - r["R0"]) < hw


iM31 = int(np.where(name == "MESSIER031")[0][0])
LG = 0.55 * dist[iM31] * U[:, iM31]
committed = {"Local Group": 34, "MESSIER081": 29, "NGC5128": 19, "NGC5236": 18, "NGC4736": 21, "NGC0253": 14, "IC0342": 16}

# ------------------------------------------------------------------------------------------------ control
ctl = {}
r = measure(LG, 0.0, None, None); ctl["Local Group"] = r["N"]; R0_LG = r["R0"]
for g in list(committed)[1:]:
    i = int(np.where(name == g)[0][0]); ctl[g] = measure(POS[:, i], vlg[i], i, g)["N"]
check("C1 CONTROL: the seven committed groups reproduce k_dimensional's N and the Local Group's R_0 = 0.906 Mpc",
      all(ctl[g] == committed[g] for g in committed) and abs(R0_LG - 0.906) < 0.005, f"N {ctl}; R_0(LG) = {R0_LG:.3f}")
r07 = measure(LG, 0.0, None, None, rlo=0.7)
OUT["numbers"]["LG_rlo0.7"] = dict(R0=float(r07["R0"]), lo=r07["lo"], hi=r07["hi"], N=r07["N"])
P(f"  Local Group with the inner cut the committed TEXT states (0.7 Mpc; the code uses 0.15): R_0 = {r07['R0']:.3f} "
  f"[{r07['lo']:.2f}, {r07['hi']:.2f}], N = {r07['N']}")

# ------------------------------------------------------------------------------------------------ census
hosts = sorted(set(m for m in md if m and m in set(name)))
res = []
for g in hosts:
    i = int(np.where(name == g)[0][0])
    if not (np.isfinite(dist[i]) and np.isfinite(vlg[i])): continue
    nmem = int(np.sum((md == g) & (ti1 > 0)))
    for rlo in (0.15, 0.7):
        r = measure(POS[:, i], vlg[i], i, g, rlo=rlo)
        if r is None:
            res.append(dict(host=g, rlo=rlo, N=0, members=nmem, D=float(dist[i]), stable=False)); continue
        v25 = measure(POS[:, i], vlg[i], i, g, rlo=rlo, rhi=2.5, boot=200)
        v70 = measure(POS[:, i], vlg[i], i, g, rlo=rlo, mu_min=0.7, boot=200)
        res.append(dict(host=g, rlo=rlo, N=r["N"], members=nmem, D=float(dist[i]), R0=float(r["R0"]), lo=r["lo"],
                        hi=r["hi"], rms=r["rms"], stable=bool(stable(r, v25, v70))))
OUT["numbers"]["census"] = res
for rlo in (0.15, 0.7):
    sub = [x for x in res if x["rlo"] == rlo]
    use = [x for x in sub if x["N"] >= 8]; st = [x for x in use if x["stable"]]
    P(f"\n  inner cut {rlo} Mpc: {len(sub)} main disturbers in the catalogue; {len(use)} with >= 8 usable galaxies; "
      f"{len(st)} pass the stability criterion")
    for x in sorted(use, key=lambda t: -t["N"]):
        P(f"    {x['host']:<14s} D = {x['D']:5.2f} Mpc  N = {x['N']:3d}  R_0 = {x['R0']:7.3f} [{x['lo']:6.2f},{x['hi']:6.2f}]  "
          f"rms {x['rms']:5.1f} km/s  {'STABLE' if x['stable'] else 'unstable'}")
    OUT["numbers"][f"rlo_{rlo}"] = dict(n_hosts=len(sub), n_usable=len(use), n_stable=len(st),
                                        stable=[x["host"] for x in st])
n_use = min(OUT["numbers"]["rlo_0.15"]["n_usable"], OUT["numbers"]["rlo_0.7"]["n_usable"])
n_st = max(OUT["numbers"]["rlo_0.15"]["n_stable"], OUT["numbers"]["rlo_0.7"]["n_stable"])
check("N2 THE PREMISE of the 09-03 follow-up: >= 20 Local Volume groups with a usable AND stable zero-velocity radius in "
      "the UNGC on disk", n_st >= 20, f"usable (>= 8 galaxies): {n_use}-{max(OUT['numbers']['rlo_0.15']['n_usable'], OUT['numbers']['rlo_0.7']['n_usable'])}; "
      f"stable: {n_st} at most")
nf = sum(1 for _, ok in CH if not ok)
OUT["n_checks"], OUT["n_fail"] = len(CH), nf
json.dump(OUT, open(os.path.join(HERE, "XR4_ungc_group_census_results.json"), "w"), indent=1, default=float)
P(f"\n  {len(CH) - nf}/{len(CH)} checks pass  [{time.time() - T0:.0f}s]")
