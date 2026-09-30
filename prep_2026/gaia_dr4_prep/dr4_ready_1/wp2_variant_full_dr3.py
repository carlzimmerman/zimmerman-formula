#!/usr/bin/env python3
"""DR4-READY-1, WP2 at FULL SIZE: the DR3 dry run of Amendment 15(c)'s all-source VARIANT base against the PRIMARY base on ALL TWELVE sky chunks
(the owner-approved full-size Q3 in its delta form: each variant chunk = the frozen chunk plus the rows without a G magnitude, assembled by q3_delta_chunks.py and q3_pilot_delta.py).
NO NETWORK (socket guard).  NEW file: catalog_builder/build_catalog.py is imported READ-ONLY and main()'s orchestration is
COPIED (as its own --test-chunks mode does: N_SHIFT = 3, sigma18 map symlinked), so nothing frozen is edited and the
existing dr3_extract/test/ smoke build is not touched.  Each base is built from its own twelve chunk files into its own
gitignored work dir <base>/wp2_full/.  Stage G uses the builder's own cut 13 and offline correlations (the union of
the primary's two on-disk caches; uncovered ids get zero correlation and are counted, as in dry_run_driver.py).  A_V is
computed by the frozen av_sfd98 from the local SFD98 maps for each base's own stage A (cached in the work dir) -- reported.
Reports: sources per base and how many lack G; the stage counts; the final pairs common / primary-only / variant-only and,
for each difference, the first stage where the pair is missing in the other base; the size on disk.
DR3 numbers are code-path tests, never results (Amendment 7(e)).
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/wp2_variant_full_dr3.py
"""
import sys
sys.dont_write_bytecode = True
import csv, io, json, socket, time
from pathlib import Path
import numpy as np


def _blocked(*a, **k):
    raise RuntimeError("network access attempted in an offline pilot (blocked by design)")


socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _blocked
HERE = Path(__file__).resolve().parent
PREP = HERE.parent
REPO = PREP.parents[1]
sys.path.insert(0, str(PREP / "catalog_builder"))
sys.path.insert(0, str(PREP))
import build_catalog as B                                        # read-only

WB = REPO / "real_research" / "data" / "widebinaries"
BASES = {"primary": WB / "dr3_extract", "allsource_15c": WB / "dr3_extract_allsource_15c"}
N_SHIFT = 3
LOG, RES = [], {}
T0 = time.time()


def P(s=""):
    print(s, flush=True)
    LOG.append(s)


def K(name, ok, detail=""):
    RES[name] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def offline_corr(source_ids):
    zs = [np.load(WB / "dr3_extract" / f) for f in ("stage_G_corr.npz", "stage_G_corr_elbadry.npz")
          if (WB / "dr3_extract" / f).exists()]
    sid = np.concatenate([z["source_id"] for z in zs])
    u, first = np.unique(sid, return_index=True)
    ids = np.unique(np.asarray(source_ids))
    pos = np.clip(np.searchsorted(u, ids), 0, len(u) - 1)
    hit = u[pos] == ids
    out = {"source_id": ids}
    for c in ("parallax_pmra_corr", "parallax_pmdec_corr"):
        allv = np.concatenate([z[c] for z in zs])
        v = np.zeros(len(ids))
        v[hit] = allv[first[pos[hit]]]
        out[c] = v
    return out, int((~hit).sum())


def build(name, src):
    work = src / "wp2_full"
    work.mkdir(exist_ok=True)
    s18 = WB / "dr3_extract" / "sigma18_hpx7.fits"
    if not (work / "sigma18_hpx7.fits").exists():
        (work / "sigma18_hpx7.fits").symlink_to(s18)
    rep = {"base": name, "work_dir": str(work.relative_to(REPO))}
    S = B.cached(work / "stage_A.npz", False, lambda: B.stage_a(src, range(12)))
    rep["n_sources"] = int(len(S["ra"]))
    rep["n_no_G"] = int((~np.isfinite(np.asarray(S["phot_g_mean_mag"], float))).sum())
    Bn = B.cached(work / "stage_B.npz", False, lambda: {"n_nbr": B.stage_b(S)})
    keep = np.flatnonzero(Bn["n_nbr"] <= 30)
    rep["n_uncrowded"] = int(len(keep))
    C = B.cached(work / "stage_C.npz", False, lambda: dict(zip(("a", "b", "th"), B.orient(S, *B.pair_search(S, keep)))))
    rep["n_initial_pairs"] = int(len(C["a"]))

    def _d():
        th_of = {(x, y): t for x, y, t in zip(C["a"].tolist(), C["b"].tolist(), C["th"].tolist())}
        a, b = B.remove_triples(C["a"], C["b"])
        a, b, _ = B.remove_clusters(S, a, b)
        return {"a": a, "b": b, "th": np.array([th_of[(x, y)] for x, y in zip(a.tolist(), b.tolist())])}
    D = B.cached(work / "stage_D.npz", False, _d)
    rep["n_clean_pairs"] = int(len(D["a"]))

    def _e():
        out = {}
        rng = np.random.default_rng(B.SEED)
        for r in range(N_SHIFT):
            p1, p2, th = B.orient(S, *B.pair_search(S, keep, shift=True, seed=r + 1), dedup=False)
            m = rng.random(len(p1)) < 0.5
            out[f"a{r}"], out[f"b{r}"], out[f"th{r}"] = p1[m], p2[m], th[m]
        return out
    E = B.cached(work / "stage_E.npz", False, _e)

    def _f():
        m18 = B.sigma18_map(work)
        sep_c = 1000 / S["parallax"][D["a"]] * D["th"]
        sel = sep_c < B.S_KDE_AU
        a, b, th = D["a"][sel], D["b"][sel], D["th"][sel]
        Xc = B.features(S, a, b, th, B.sigma18_at(S["ra"][a], S["dec"][a], m18))
        Xs = [B.features(S, E[f"a{r}"], E[f"b{r}"], E[f"th{r}"], B.sigma18_at(S["ra"][E[f"a{r}"]], S["dec"][E[f"a{r}"]], m18))
              for r in range(N_SHIFT)]
        return {"a": a, "b": b, "th": th, "R": B.r_chance(Xc, Xs), "Xc": Xc}
    F = B.cached(work / "stage_F.npz", False, _f)
    rep["n_R_pairs"] = int(len(F["a"]))
    # stage G (COPIED from main(), with offline correlations)
    extra = {"third": np.zeros(len(F["a"]), bool)}
    pre, _, _ = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx = np.flatnonzero(pre)
    extra["third"][idx] = B.third_star_flags(S, F["a"][idx], F["b"][idx])
    pre2, _, tab0 = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx2 = np.flatnonzero(pre2)
    corr, nunc = offline_corr(np.concatenate([S["source_id"][F["a"][idx2]], S["source_id"][F["b"][idx2]]]))
    rep["corr_uncovered"] = nunc
    sig_vt = B.vt_error_mc(S, F["a"][idx2], F["b"][idx2], F["th"][idx2], corr)
    from wide_binary_pipeline import G as GN, MSUN, AU
    vc0 = np.sqrt(GN * (tab0["M1_msun"][idx2] + tab0["M2_msun"][idx2]) * MSUN / (tab0["sep_kAU"][idx2] * 1e3 * AU)) / 1e3
    ok = np.zeros(len(F["a"]), bool)
    ok[idx2] = sig_vt <= 0.1 * np.maximum(1.0, (tab0["v_perp_kms"][idx2] / vc0) / 2)
    extra["vt_err_ok"] = ok
    z = B.av_sfd98(S, work / "AV_sfd98.npz")
    rep["AV_applied"] = z is not None
    if z is not None:
        extra["AV_ok"] = (z["av"][F["a"]] < 0.5) & (z["av"][F["b"]] < 0.5)
    keepG, flow, table = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    rep["cut_flow"] = flow
    rep["n_final"] = int(keepG.sum())
    final = {tuple(sorted((int(S["source_id"][F["a"][i]]), int(S["source_id"][F["b"][i]])))) for i in np.flatnonzero(keepG)}
    stages = {"C": C, "D": D, "F": F}
    sets = {k: {tuple(sorted((int(S["source_id"][x]), int(S["source_id"][y])))) for x, y in zip(v["a"], v["b"])}
            for k, v in stages.items()}
    sets["G"] = final
    buf = io.StringIO(newline="")
    w = csv.writer(buf)
    cols = list(table)
    w.writerow(cols)
    for i in np.flatnonzero(keepG):
        w.writerow([table[c][i] for c in cols])
    rep["final_csv_sha256"] = __import__("hashlib").sha256(buf.getvalue().encode()).hexdigest()
    gnull = set(S["source_id"][~np.isfinite(np.asarray(S["phot_g_mean_mag"], float))].tolist())
    return rep, sets, gnull, S


P("WP2 full size: primary vs all-source variant base, all 12 chunks (N_SHIFT = 3, as the builder's smoke mode; DR3 numbers are code-path tests)")
out, SETS, GN_ = {}, {}, {}
for name, src in BASES.items():
    t = time.time()
    with __import__("contextlib").redirect_stdout(io.StringIO()):
        rep, sets, gnull, S_ = build(name, src)
    out[name], SETS[name], GN_[name] = rep, sets, gnull
    P(f"  {name:14s}: sources {rep['n_sources']:,d} (no G {rep['n_no_G']:,d}); uncrowded {rep['n_uncrowded']:,d}; initial pairs "
      f"{rep['n_initial_pairs']:,d}; clean {rep['n_clean_pairs']:,d}; with R {rep['n_R_pairs']:,d}; FINAL {rep['n_final']:,d}; "
      f"correlations uncovered {rep['corr_uncovered']}; A_V applied {rep['AV_applied']}  ({time.time() - t:.0f} s)")
K("W1 the primary base's sources are a subset of the variant's (the variant only drops the G condition)",
  out["primary"]["n_sources"] <= out["allsource_15c"]["n_sources"] and
  out["allsource_15c"]["n_sources"] - out["allsource_15c"]["n_no_G"] == out["primary"]["n_sources"],
  f"variant - no-G = {out['allsource_15c']['n_sources'] - out['allsource_15c']['n_no_G']:,d} vs primary {out['primary']['n_sources']:,d}")
Pf, Vf = SETS["primary"]["G"], SETS["allsource_15c"]["G"]
common, ponly, vonly = Pf & Vf, Pf - Vf, Vf - Pf
P(f"\n  final pairs: common {len(common):,d}; primary only {len(ponly)}; variant only {len(vonly)}")


def first_missing(pair, other):
    for st in ("C", "D", "F", "G"):
        if pair not in SETS[other][st]:
            return st
    return "present"


diff = {}
for lab, pset, other in (("primary_only", ponly, "allsource_15c"), ("variant_only", vonly, "primary")):
    where = {}
    ng = 0
    for pr in pset:
        st = first_missing(pr, other)
        where[st] = where.get(st, 0) + 1
        ng += int(pr[0] in GN_["allsource_15c"] or pr[1] in GN_["allsource_15c"])
    diff[lab] = dict(n=len(pset), first_missing_stage_in_other=where, with_a_no_G_component=ng)
    P(f"  {lab:12s}: {len(pset)} pairs; first stage where each is missing in the other base: {where}; with a no-G component: {ng}")
sizes = {k: sum((BASES[k] / f"chunk_{c:02d}.fits").stat().st_size for c in range(12)) for k in BASES}
P(f"\n  SIZING: the 12 variant chunks total {sizes['allsource_15c'] / 1e6:.0f} MB on disk vs {sizes['primary'] / 1e6:.0f} MB for the primary (the variant only adds the rows without G)")
res = dict(bases=out, final_pairs=dict(common=len(common), primary_only=len(ponly), variant_only=len(vonly)), differences=diff,
           sizing=dict(total_bytes=sizes),
           checks=RES, seconds=round(time.time() - T0, 1))
ok = all(RES.values())
P(f"\n{sum(RES.values())}/{len(RES)} checks pass -> {'ALL PASS' if ok else 'FAILURES'}  ({time.time() - T0:.0f} s)")
(HERE / "wp2_variant_full_dr3.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
(HERE / "wp2_variant_full_dr3.out").write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
