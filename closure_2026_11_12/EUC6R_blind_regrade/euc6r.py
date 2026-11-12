#!/usr/bin/env python3
"""EUC6R: blind re-grade of EUC6 (wide-lens environment).

Written from closure_2026_11_12/EUC6_wide_lens_environment/FROZEN_CRITERIA.md, EUC1's criteria (sample S, cosmology,
b_inf) and EUC6R/PROTOCOL.md only. kappa = 1/2 FITTED; not theory closed. Does not relabel EUC6.

Subcommands:
  targets   build W, C, L, R from the ECLIPSE CSVs -> euc6r_targets.csv, euc6r_samples.json
  selftest  one completeness cone at a non-target position (row query vs server COUNT)
  fetch     one paced request stream: object rows in a cone per target, raw gz kept outside git, resumable
  grade     counts, richness, paired statistic, word, N1, N2 (EUC6R_MUTATE=shuffle for the mutation twin)
"""
import csv
import gzip
import hashlib
import io
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse")
RAW = os.path.join(REPO, "_external_data", "euclid_dr1_mer_cones_euc6r")
KEY = os.path.join(DATA, "eclipse_dr1_catalogue_key_v20261103.csv")
OBJ = os.path.join(DATA, "ECLIPSE_object_catalogue.csv")
SHA = {KEY: "65338917534c9c767c4f45732d29937d2dfb7fd68083cdfd05aec994ee4fa9ab",
       OBJ: "8247a4d5f23513b83be6db5a8244234f0cc1e1ac66e4de1a54983ae5984786b2"}

TAP = "https://eas.esac.esa.int/tap-server/tap/sync"
UA = "tap-client/1.0"
TABLE = "dr1.mer_catalogue_wide_survey"
COLS = "object_id, right_ascension, declination, flux_h_templfit, spurious_flag, det_quality_flag, point_like_prob, tile_index"
PRECUT = 5.0          # server-side loose flux pre-cut (uJy); the frozen cut is applied locally
PACE = 1.5            # seconds between requests
RETRY = [10, 30, 90, 270]

# cosmology (EUC1 section 3): flat LCDM, radiation neglected
H0 = 67.74
OM = 0.3089
C_KMS = 299792.458
DH = C_KMS / H0       # Mpc

# frozen numbers (EUC6 sections 1-4)
TH_W = 1.7
TH_C = 1.0
DZ, DM, D2MAX = 0.05, 0.1, 4.0
N_L, N_R, DEC_SHIFT = 40, 60, 0.30
R_IN = (30.0, 300.0)
R_BG = (600.0, 1000.0)
AREA_RATIO = (R_IN[1] ** 2 - R_IN[0] ** 2) / (R_BG[1] ** 2 - R_BG[0] ** 2)
FLUX_CUT, PLP_CUT, DQF_CUT = 5.75, 0.7, 4
EDGE_FRAC = 0.40
NBOOT, SEED_BOOT, SEED_MUT = 2000, 20261112, 20261113
MIN_PAIRS = 150
N1_MAX, N2_MIN, NO_RICHER_UB, P_MAX = 2.0, 3.0, 3.0, 1e-3
RADIUS_MARGIN = 1.02

W_RICHER = "WIDE LENSES SIT IN RICHER ENVIRONMENTS"
W_NO = "NO RICHER"
W_NV = "NO VERDICT"
W_NE = "NOT EVALUABLE"


# ---------------------------------------------------------------- cosmology
def _inv_e(z):
    return 1.0 / math.sqrt(OM * (1.0 + z) ** 3 + (1.0 - OM))


def comoving(z):
    from scipy.integrate import quad
    v, _ = quad(_inv_e, 0.0, z, limit=500, epsabs=0, epsrel=1e-10)
    return DH * v


def d_a(z):
    return comoving(z) / (1.0 + z)


def kpc_per_rad(z):
    return d_a(z) * 1000.0     # proper kpc per radian


# ---------------------------------------------------------------- helpers
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


def sep_rad(ra1, de1, ra2, de2):
    """exact great-circle separation (haversine), degrees in, radians out"""
    r1, d1, r2, d2 = map(np.radians, (ra1, de1, ra2, de2))
    a = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


# ---------------------------------------------------------------- samples
def build_targets():
    for p, h in SHA.items():
        got = sha256(p)
        if got != h:
            sys.exit(f"sha256 mismatch for {os.path.basename(p)}: {got}")
    obj = {r["Unique_Identifier"]: r for r in csv.DictReader(open(OBJ, newline=""))}
    key = list(csv.DictReader(open(KEY, newline="")))
    key.sort(key=lambda r: r["unique_identifier"])

    def lsw(r):
        return obj[r["unique_identifier"]]["large_system_warning"] == "True"

    pos_off = []
    S = []
    removed = {"theta_E<=0": 0, "R_e<=0": 0, "n_out_of_range": 0, "phz<=0": 0, "mass<=0": 0}
    base = 0
    for r in key:
        o = obj.get(r["unique_identifier"])
        if o is None:
            sys.exit("identifier missing from object catalogue: " + r["unique_identifier"])
        pos_off.append(math.degrees(float(sep_rad(fnum(r["ra"]), fnum(r["dec"]),
                                                  fnum(o["RA_obj"]), fnum(o["DEC_obj"])))) * 3600)
        if not (r["lens_grade"] in ("A", "B") and r["lens_model_success"] == "True"
                and r["final_sample"] == "True" and not lsw(r)):
            continue
        base += 1
        th, re_, n = fnum(r["eclipse_effective_einstein_radius"]), fnum(r["eclipse_effective_radius"]), fnum(r["eclipse_sersic_index"])
        z, m = fnum(r["eclipse_median_phz"]), fnum(r["eclipse_log_survived_mass_med"])
        if not th > 0:
            removed["theta_E<=0"] += 1; continue
        if not re_ > 0:
            removed["R_e<=0"] += 1; continue
        if not (0.6 <= n <= 10):
            removed["n_out_of_range"] += 1; continue
        if not z > 0:
            removed["phz<=0"] += 1; continue
        if not m > 0:
            removed["mass<=0"] += 1; continue
        S.append(r)

    W = [r for r in S if fnum(r["eclipse_effective_einstein_radius"]) >= TH_W]
    pool = [r for r in S if fnum(r["eclipse_effective_einstein_radius"]) < TH_C]
    pz = np.array([fnum(r["eclipse_median_phz"]) for r in pool])
    pm = np.array([fnum(r["eclipse_log_survived_mass_med"]) for r in pool])
    used = np.zeros(len(pool), bool)
    pairs, dropped, ties, eq4 = [], [], 0, 0
    for w in W:                                    # W already in identifier order; pool too
        d2 = ((pz - fnum(w["eclipse_median_phz"])) / DZ) ** 2 + ((pm - fnum(w["eclipse_log_survived_mass_med"])) / DM) ** 2
        d2 = np.where(used, np.inf, d2)
        j = int(np.argmin(d2))                     # argmin returns the first = lowest identifier on a tie
        if np.sum(d2 == d2[j]) > 1:
            ties += 1
        if d2[j] > D2MAX:
            dropped.append(w["unique_identifier"]); continue
        if d2[j] == D2MAX:
            eq4 += 1
        used[j] = True
        pairs.append((w, pool[j], float(d2[j])))

    L = [r for r in key if lsw(r) and fnum(r["eclipse_median_phz"]) > 0][:N_L]
    R = W[:N_R]

    rows = []

    def add(kind, tid, r, ra, dec, pair=-1, d2=float("nan")):
        z = fnum(r["eclipse_median_phz"])
        rows.append(dict(target=tid, kind=kind, lens_id=r["unique_identifier"], ra=ra, dec=dec, z=z,
                         logm=fnum(r["eclipse_log_survived_mass_med"]),
                         theta_e=fnum(r["eclipse_effective_einstein_radius"]), grade=r["lens_grade"],
                         pair=pair, d2=d2, r_deg=math.degrees(R_BG[1] / kpc_per_rad(z)) * RADIUS_MARGIN))

    for w in W:
        add("W", "W:" + w["unique_identifier"], w, fnum(w["ra"]), fnum(w["dec"]))
    for i, (w, c, d2) in enumerate(pairs):
        add("C", "C:" + c["unique_identifier"], c, fnum(c["ra"]), fnum(c["dec"]), pair=i, d2=d2)
    for r in L:
        add("L", "L:" + r["unique_identifier"], r, fnum(r["ra"]), fnum(r["dec"]))
    for r in R:
        add("R", "R:" + r["unique_identifier"], r, fnum(r["ra"]), fnum(r["dec"]) + DEC_SHIFT)
    widx = {w["unique_identifier"]: None for w in W}
    for i, (w, c, d2) in enumerate(pairs):
        widx[w["unique_identifier"]] = i
    for row in rows:
        if row["kind"] == "W":
            p = widx[row["lens_id"]]
            row["pair"] = -1 if p is None else p
            if p is not None:
                row["d2"] = pairs[p][2]

    with open(os.path.join(HERE, "euc6r_targets.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        for row in rows:
            wr.writerow(row)
    info = dict(
        sha256_ok=True, n_base_before_validity=base, validity_removed=removed, n_S=len(S),
        n_W=len(W), n_W_gradeA=sum(r["lens_grade"] == "A" for r in W), n_W_gradeB=sum(r["lens_grade"] == "B" for r in W),
        n_pool_C=len(pool), n_pairs_matched=len(pairs), n_W_dropped_no_control=len(dropped),
        W_dropped_no_control=dropped, exact_distance_ties=ties, d2_equal_4=eq4,
        d2_max_matched=max(p[2] for p in pairs), d2_median_matched=float(np.median([p[2] for p in pairs])),
        n_L=len(L), L_z_range=[min(fnum(r["eclipse_median_phz"]) for r in L), max(fnum(r["eclipse_median_phz"]) for r in L)],
        n_R=len(R), n_targets=len(rows), area_ratio=AREA_RATIO,
        key_vs_object_position_offset_arcsec_max=max(pos_off),
        median_dz_pairs=float(np.median([fnum(w["eclipse_median_phz"]) - fnum(c["eclipse_median_phz"]) for w, c, _ in pairs])),
        median_dlogm_pairs=float(np.median([fnum(w["eclipse_log_survived_mass_med"]) - fnum(c["eclipse_log_survived_mass_med"]) for w, c, _ in pairs])),
    )
    json.dump(info, open(os.path.join(HERE, "euc6r_samples.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in info.items() if k != "W_dropped_no_control"}, indent=1))


# ---------------------------------------------------------------- TAP
def tap(query, fmt="csv", timeout=600):
    data = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": fmt,
                                   "MAXREC": "1000000", "QUERY": query}).encode()
    req = urllib.request.Request(TAP, data=data, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def cone_query(ra, dec, r):
    return (f"SELECT {COLS} FROM {TABLE} WHERE 1 = CONTAINS(POINT('ICRS', right_ascension, declination), "
            f"CIRCLE('ICRS', {ra:.8f}, {dec:.8f}, {r:.8f})) AND flux_h_templfit > {PRECUT}")


def fetch_one(query):
    last = None
    for k in range(len(RETRY) + 1):
        try:
            t0 = time.time()
            body = tap(query)
            dt = time.time() - t0
            head = body[:200].decode("utf-8", "replace")
            if not head.startswith("object_id"):
                raise RuntimeError("unexpected response: " + head[:150].replace("\n", " "))
            return body, dt
        except Exception as e:                      # retry, slower, never in parallel
            last = e
            if k < len(RETRY):
                print(f"   retry in {RETRY[k]} s: {str(e)[:120]}", flush=True)
                time.sleep(RETRY[k])
    raise RuntimeError(f"failed after retries: {last}")


def selftest():
    key = sorted(csv.DictReader(open(KEY, newline="")), key=lambda r: r["unique_identifier"])
    t = [l.split(",") for l in open(os.path.join(HERE, "euc6r_targets.csv")).read().splitlines()]
    hdr = t[0]
    first = None
    S_ids = set(r[hdr.index("lens_id")] for r in t[1:])
    # first lens of S in identifier order: rebuild S membership from the targets is not enough; use the protocol's
    # position: 0.60 deg south of the first S lens; S is recomputed here with the same rule
    obj = {r["Unique_Identifier"]: r for r in csv.DictReader(open(OBJ, newline=""))}
    for r in key:
        if (r["lens_grade"] in ("A", "B") and r["lens_model_success"] == "True" and r["final_sample"] == "True"
                and obj[r["unique_identifier"]]["large_system_warning"] == "False"
                and fnum(r["eclipse_effective_einstein_radius"]) > 0 and fnum(r["eclipse_effective_radius"]) > 0
                and 0.6 <= fnum(r["eclipse_sersic_index"]) <= 10 and fnum(r["eclipse_median_phz"]) > 0
                and fnum(r["eclipse_log_survived_mass_med"]) > 0):
            first = r
            break
    ra, dec, rad = fnum(first["ra"]), fnum(first["dec"]) - 0.60, 0.15
    q = cone_query(ra, dec, rad)
    body, dt = fetch_one(q)
    nrows = body.decode().count("\n") - 1
    time.sleep(PACE)
    qc = (f"SELECT COUNT(*) AS n FROM {TABLE} WHERE 1 = CONTAINS(POINT('ICRS', right_ascension, declination), "
          f"CIRCLE('ICRS', {ra:.8f}, {dec:.8f}, {rad:.8f})) AND flux_h_templfit > {PRECUT}")
    bc = tap(qc).decode().splitlines()
    out = dict(position=[ra, dec], radius_deg=rad, rows_returned=nrows, server_count=int(bc[1]), seconds=dt,
               note="completeness test of the sync service at a non-target position; not used in any statistic",
               first_S_lens_is_target=first["unique_identifier"] in S_ids)
    json.dump(out, open(os.path.join(HERE, "euc6r_selftest.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


def fetch():
    os.makedirs(RAW, exist_ok=True)
    rows = list(csv.DictReader(open(os.path.join(HERE, "euc6r_targets.csv"), newline="")))
    seen = {}
    for r in rows:                                  # one query per distinct target id
        seen.setdefault(r["target"], r)
    man_path = os.path.join(HERE, "euc6r_manifest.csv")
    man = {}
    if os.path.exists(man_path):
        for m in csv.DictReader(open(man_path, newline="")):
            man[m["target"]] = m
    todo = [t for t in seen if not (t in man and os.path.exists(os.path.join(RAW, man[t]["file"])))]
    print(f"{len(seen)} targets, {len(todo)} to fetch", flush=True)
    for i, tid in enumerate(todo):
        r = seen[tid]
        q = cone_query(float(r["ra"]), float(r["dec"]), float(r["r_deg"]))
        body, dt = fetch_one(q)
        fn = tid.replace(":", "_") + ".csv.gz"
        with gzip.open(os.path.join(RAW, fn), "wb") as f:
            f.write(body)
        man[tid] = dict(target=tid, file=fn, rows=body.decode().count("\n") - 1,
                        sha256_raw=hashlib.sha256(body).hexdigest(), seconds=f"{dt:.1f}",
                        utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), query=q)
        with open(man_path + ".tmp", "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=["target", "file", "rows", "sha256_raw", "seconds", "utc", "query"])
            wr.writeheader()
            for t in seen:
                if t in man:
                    wr.writerow(man[t])
        os.replace(man_path + ".tmp", man_path)
        print(f"[{i + 1}/{len(todo)}] {tid} rows={man[tid]['rows']} {dt:.1f}s", flush=True)
        time.sleep(PACE)


# ---------------------------------------------------------------- counting
def count_target(r, dedup=False, pg_nan=False):
    raw = gzip.open(os.path.join(RAW, r["file"]), "rt").read()
    rd = csv.DictReader(io.StringIO(raw))
    ra, de, fl, sp, dq, pl = [], [], [], [], [], []
    for o in rd:
        ra.append(fnum(o["right_ascension"])); de.append(fnum(o["declination"]))
        fl.append(fnum(o["flux_h_templfit"])); sp.append(fnum(o["spurious_flag"]))
        dq.append(fnum(o["det_quality_flag"])); pl.append(fnum(o["point_like_prob"]))
    ra, de, fl, sp, dq, pl = map(np.array, (ra, de, fl, sp, dq, pl))
    nulls = dict(flux=int(np.isnan(fl).sum()), spurious=int(np.isnan(sp).sum()),
                 det_quality=int(np.isnan(dq).sum()), point_like=int(np.isnan(pl).sum()))
    # Missing values (the archive writes NaN as an empty field) fail every condition: the protocol's rule.
    # pg_nan=True mimics a literal server-side PostgreSQL WHERE, where NaN sorts above every number: a NaN flux PASSES
    # "flux > 5.75" and a NaN point_like_prob FAILS "< 0.7" (variant added after the NaN finding; reported only).
    fl_ok = (fl > FLUX_CUT) | (np.isnan(fl) if pg_nan else False)
    ok = fl_ok & (sp == 0) & (dq < DQF_CUT) & (pl < PLP_CUT)
    R = sep_rad(float(r["ra"]), float(r["dec"]), ra, de) * kpc_per_rad(float(r["z"]))
    if dedup and ok.sum() > 1:
        idx = np.where(ok)[0]
        # pairs of qualifying objects closer than 0.2 arcsec: keep one
        x = np.radians(ra[idx]) * np.cos(np.radians(de[idx])); y = np.radians(de[idx])
        order = np.argsort(y)
        keep = np.ones(len(idx), bool)
        tol = math.radians(0.2 / 3600)
        for a in range(len(order)):
            ia = order[a]
            if not keep[ia]:
                continue
            b = a + 1
            while b < len(order) and y[order[b]] - y[ia] < tol:
                ib = order[b]
                if keep[ib] and math.hypot(x[ib] - x[ia], y[ib] - y[ia]) < tol:
                    keep[ib] = False
                b += 1
        ok2 = np.zeros_like(ok); ok2[idx[keep]] = True
        ok = ok2
    n_in = int(((R >= R_IN[0]) & (R < R_IN[1]) & ok).sum())
    n_bg = int(((R >= R_BG[0]) & (R < R_BG[1]) & ok).sum())
    return n_in, n_bg, nulls


# ---------------------------------------------------------------- b_inf (EUC1 sections 3-4, my own code)
G_SI = 6.67430e-11
MSUN = 1.98892e30   # kg (IAU nominal G*Msun / G gives 1.98841e30; difference is 2.6e-4, irrelevant for ranks)
KPC = 3.0856775814913673e19
C_SI = 299792458.0
FOOT = {"canonical": 9.3603e-11, "alt": 1.132e-10}


def b_ciotti(n):
    return 2 * n - 1 / 3 + 4 / (405 * n) + 46 / (25515 * n ** 2) + 131 / (1148175 * n ** 3) - 2194697 / (30690717750 * n ** 4)


def m3d_frac(r, Re, n):
    from scipy.special import gammainc
    p = 1 - 0.6097 / n + 0.05463 / n ** 2
    b = b_ciotti(n)
    return gammainc(n * (3 - p), b * (r / Re) ** (1 / n))


_GL_X, _GL_W = np.polynomial.legendre.leggauss(400)


def m2d_law(R, Mstar, Re, n, a0, rmax=1e6 * KPC, newton=False):
    """M_2D(<R) = (R^2/G) int_R^rmax g dr / sqrt(r^2 - R^2), r = R cosh u (SI)"""
    U = math.acosh(rmax / R)
    # split u in two pieces to resolve the inner region
    out = 0.0
    for lo, hi in ((0.0, min(U, 3.0)), (min(U, 3.0), U)):
        if hi <= lo:
            continue
        u = 0.5 * (hi - lo) * _GL_X + 0.5 * (hi + lo)
        r = R * np.cosh(u)
        gN = G_SI * Mstar * m3d_frac(r, Re, n) / r ** 2
        g = gN if newton else 0.5 * gN * (1 + np.sqrt(1 + 4 * a0 / np.maximum(gN, 1e-300)))
        out += 0.5 * (hi - lo) * np.sum(_GL_W * g)
    return R ** 2 / G_SI * out


CHI_INF = None


def b_inf(z, theta_e, Re_arcsec, n, logm, a0):
    global CHI_INF
    if CHI_INF is None:
        CHI_INF = comoving(1100.0)
    chi_l = comoving(z)
    Dl = chi_l / (1 + z) * 1000 * KPC
    sig_cr_inf = C_SI ** 2 / (4 * math.pi * G_SI * Dl) * CHI_INF / (CHI_INF - chi_l)
    RE = math.radians(theta_e / 3600) * Dl
    Re = math.radians(Re_arcsec / 3600) * Dl
    Mmin = math.pi * RE ** 2 * sig_cr_inf
    M = 10 ** logm * MSUN
    from scipy.optimize import brentq
    f = lambda lb: math.log(m2d_law(RE, 10 ** lb * M, Re, n, a0) / Mmin)
    return brentq(f, -4, 4, xtol=1e-6)


def k1_check():
    """point mass: M_2D returns the mass to 1e-6 at a0 -> 0 (Sersic with Re -> tiny behaves as a point)"""
    M = 1e11 * MSUN
    R = 5 * KPC
    v = m2d_law(R, M, 1e-6 * KPC, 4.0, 0.0, newton=True) / M
    # SIS check: g = v^2/r -> M2D = pi sigma^2 R / G with v^2 = 2 sigma^2
    return dict(point_mass_ratio=v)


# ---------------------------------------------------------------- statistic
def word_for(D, n_pairs, n1_ok, n2_ok):
    from scipy.stats import wilcoxon
    rng = np.random.default_rng(SEED_BOOT)
    idx = rng.integers(0, len(D), size=(NBOOT, len(D)))
    meds = np.median(D[idx], axis=1)
    lo, hi = np.percentile(meds, [2.5, 97.5])
    p = float(wilcoxon(D, alternative="greater").pvalue)
    richer = lo > 0 and p < P_MAX
    norich = hi <= NO_RICHER_UB
    if n_pairs < MIN_PAIRS or not (n1_ok and n2_ok):
        w = W_NE
    elif richer:
        w = W_RICHER
    elif norich:
        w = W_NO
    else:
        w = W_NV
    return dict(median_D=float(np.median(D)), ci95=[float(lo), float(hi)], p_wilcoxon_greater=p,
                richer_condition=bool(richer), no_richer_condition=bool(norich), both_conditions=bool(richer and norich),
                word=w)


def grade():
    mutate = os.environ.get("EUC6R_MUTATE", "")
    if mutate not in ("", "shuffle"):
        sys.exit("EUC6R_MUTATE must be empty or 'shuffle'")
    tg = list(csv.DictReader(open(os.path.join(HERE, "euc6r_targets.csv"), newline="")))
    man = {m["target"]: m for m in csv.DictReader(open(os.path.join(HERE, "euc6r_manifest.csv"), newline=""))}
    missing = [t["target"] for t in tg if t["target"] not in man]
    if missing:
        sys.exit(f"{len(missing)} targets not fetched")
    cnt = {}
    nulls_tot = dict(flux=0, spurious=0, det_quality=0, point_like=0)
    for t in tg:
        t["file"] = man[t["target"]]["file"]
        if t["target"] in cnt:
            continue
        sha = hashlib.sha256(gzip.open(os.path.join(RAW, t["file"])).read()).hexdigest()
        if sha != man[t["target"]]["sha256_raw"]:
            sys.exit("raw file hash mismatch: " + t["target"])
        n_in, n_bg, nl = count_target(t)
        n_in_d, n_bg_d, _ = count_target(t, dedup=True)
        n_in_p, n_bg_p, _ = count_target(t, pg_nan=True)
        for k in nulls_tot:
            nulls_tot[k] += nl[k]
        cnt[t["target"]] = dict(n_in=n_in, n_bg=n_bg, delta=n_in - AREA_RATIO * n_bg,
                                n_in_dedup=n_in_d, n_bg_dedup=n_bg_d, delta_dedup=n_in_d - AREA_RATIO * n_bg_d,
                                n_in_pgnan=n_in_p, n_bg_pgnan=n_bg_p, delta_pgnan=n_in_p - AREA_RATIO * n_bg_p)
    for t in tg:
        t.update(cnt[t["target"]])

    W = [t for t in tg if t["kind"] == "W"]
    C = {int(t["pair"]): t for t in tg if t["kind"] == "C"}
    L = [t for t in tg if t["kind"] == "L"]
    R = [t for t in tg if t["kind"] == "R"]
    Wp = {int(t["pair"]): t for t in W if int(t["pair"]) >= 0}

    lens_bg = [t["n_bg"] for t in W] + [C[i]["n_bg"] for i in C] + [t["n_bg"] for t in L]
    ref = float(np.median(lens_bg))
    ref_wc = float(np.median([t["n_bg"] for t in W] + [C[i]["n_bg"] for i in C]))
    thr = EDGE_FRAC * ref

    def pairs_after_edge(threshold, key_d="delta"):
        keep, drop = [], []
        for i in sorted(Wp):
            w, c = Wp[i], C[i]
            if w["n_bg"] < threshold or c["n_bg"] < threshold:
                drop.append(i)
            else:
                keep.append(i)
        return keep, drop

    keep, drop = pairs_after_edge(thr)
    dW = np.array([Wp[i]["delta"] for i in keep])
    dC = np.array([C[i]["delta"] for i in keep])
    D = dW - dC
    Rk = [t for t in R if t["n_bg"] >= thr]
    Lk = [t for t in L if t["n_bg"] >= thr]
    medR = float(np.median([t["delta"] for t in Rk]))
    medL = float(np.median([t["delta"] for t in Lk]))
    medC = float(np.median(dC))
    n1 = abs(medR) <= N1_MAX
    n2 = (medL - medC) >= N2_MIN

    suffix = ""
    mut = None
    if mutate == "shuffle":
        swap = np.random.default_rng(SEED_MUT).random(len(D)) < 0.5
        D = np.where(swap, -D, D)
        suffix = "_mutate_shuffle"
        mut = dict(n_swapped=int(swap.sum()))

    st = word_for(D, len(D), n1, n2)

    res = dict(
        lane="EUC6R", note="blind re-grade of EUC6; does not relabel EUC6. kappa = 1/2 FITTED; not theory closed.",
        mutate=mutate or None, mutation=mut,
        area_ratio=AREA_RATIO, edge_reference_median_nbg=ref, edge_reference_W_C_only=ref_wc, edge_threshold=thr,
        n_W=len(W), n_pairs_matched=len(Wp), n_pairs_edge_dropped=len(drop), n_pairs=len(keep),
        edge_dropped_pairs=[[Wp[i]["lens_id"], C[i]["lens_id"], Wp[i]["n_bg"], C[i]["n_bg"], float(Wp[i]["z"])] for i in drop],
        statistic=st,
        N1=dict(median_delta_R=medR, n_R_used=len(Rk), n_R=len(R), passes=bool(n1),
                median_delta_R_no_edge_cut=float(np.median([t["delta"] for t in R]))),
        N2=dict(median_delta_L=medL, median_delta_C=medC, difference=medL - medC, n_L_used=len(Lk), n_L=len(L),
                passes=bool(n2), median_delta_L_no_edge_cut=float(np.median([t["delta"] for t in L]))),
        missing_values_in_cut_columns_all_rows=nulls_tot,
        missing_value_note="the archive stores NaN, not NULL (IS NULL counts 0 at the test cone); the CSV writes NaN as an empty field",
    )
    if not mutate:
        res["reported"] = reported(Wp, C, keep, dW, dC, L, R, thr, ref_wc)
        res["robustness"] = robustness(Wp, C, L, R, ref, ref_wc, [t for t in W if int(t["pair"]) < 0])
    out = os.path.join(HERE, f"euc6r_result{suffix}.json")
    json.dump(res, open(out, "w"), indent=1)
    # per-target table
    with open(os.path.join(HERE, f"euc6r_counts{suffix}.csv"), "w", newline="") as f:
        fn = ["target", "kind", "lens_id", "pair", "ra", "dec", "z", "logm", "theta_e", "grade", "d2",
              "n_in", "n_bg", "delta", "n_in_dedup", "n_bg_dedup", "delta_dedup", "n_in_pgnan", "n_bg_pgnan", "delta_pgnan"]
        wr = csv.DictWriter(f, fieldnames=fn, extrasaction="ignore")
        wr.writeheader()
        for t in tg:
            wr.writerow(t)
    print(json.dumps({k: v for k, v in res.items() if k not in ("edge_dropped_pairs",)}, indent=1))
    if mutate:
        print("MUTATE twin: word =", st["word"], "| passes" if st["word"] != W_RICHER else "| FAILS (returned RICHER)")
        sys.exit(1)


def reported(Wp, C, keep, dW, dC, L, R, thr, ref_wc):
    from scipy.stats import spearmanr
    out = dict(
        median_delta_W=float(np.median(dW)), median_delta_C=float(np.median(dC)),
        median_delta_L=float(np.median([t["delta"] for t in L if t["n_bg"] >= thr])),
        median_delta_R=float(np.median([t["delta"] for t in R if t["n_bg"] >= thr])),
        frac_W_above_C_p84=float(np.mean(dW > np.percentile(dC, 84))), C_p84=float(np.percentile(dC, 84)),
        mean_D=float(np.mean(dW - dC)),
        median_n_in_W=float(np.median([Wp[i]["n_in"] for i in keep])),
        median_n_in_C=float(np.median([C[i]["n_in"] for i in keep])),
        median_n_bg_W=float(np.median([Wp[i]["n_bg"] for i in keep])),
        median_n_bg_C=float(np.median([C[i]["n_bg"] for i in keep])),
    )
    zs = np.array([float(Wp[i]["z"]) for i in keep])
    zmed = float(np.median(zs))
    lo, hi = zs <= zmed, zs > zmed
    out["z_split"] = dict(z_median_W=zmed,
                          low=dict(n=int(lo.sum()), median_delta_W=float(np.median(dW[lo])), median_D=float(np.median((dW - dC)[lo]))),
                          high=dict(n=int(hi.sum()), median_delta_W=float(np.median(dW[hi])), median_D=float(np.median((dW - dC)[hi]))))
    # b_inf by own code from EUC1 text (law S), per footing
    key = {r["unique_identifier"]: r for r in csv.DictReader(open(KEY, newline=""))}
    sp = {}
    for foot, a0 in FOOT.items():
        bw, bc = [], []
        for i in keep:
            for t, lst in ((Wp[i], bw), (C[i], bc)):
                r = key[t["lens_id"]]
                lst.append(b_inf(fnum(r["eclipse_median_phz"]), fnum(r["eclipse_effective_einstein_radius"]),
                                 fnum(r["eclipse_effective_radius"]), fnum(r["eclipse_sersic_index"]),
                                 fnum(r["eclipse_log_survived_mass_med"]), a0))
        bw, bc = np.array(bw), np.array(bc)
        rw = spearmanr(dW, bw)
        ra = spearmanr(np.concatenate([dW, dC]), np.concatenate([bw, bc]))
        sp[foot] = dict(spearman_W=dict(rho=float(rw.statistic), p=float(rw.pvalue)),
                        spearman_W_and_C=dict(rho=float(ra.statistic), p=float(ra.pvalue)),
                        median_b_inf_W=float(np.median(bw)), median_b_inf_C=float(np.median(bc)))
    out["b_inf_lawS"] = sp
    out["K1_point_mass"] = k1_check()
    return out


def robustness(Wp, C, L, R, ref, ref_wc, W_unmatched=()):
    out = {}
    # (a) edge reference from W and C only
    for name, thr in (("edge_ref_W_C_only", EDGE_FRAC * ref_wc), ("no_edge_cut", -1.0)):
        keep = [i for i in sorted(Wp) if Wp[i]["n_bg"] >= thr and C[i]["n_bg"] >= thr]
        D = np.array([Wp[i]["delta"] - C[i]["delta"] for i in keep])
        n1 = abs(np.median([t["delta"] for t in R if t["n_bg"] >= thr])) <= N1_MAX
        n2 = (np.median([t["delta"] for t in L if t["n_bg"] >= thr]) - np.median([C[i]["delta"] for i in keep])) >= N2_MIN
        out[name] = dict(n_pairs=len(keep), **word_for(D, len(keep), n1, n2))
    # (b) de-duplicated counts (qualifying objects closer than 0.2 arcsec merged)
    thr = EDGE_FRAC * ref
    keep = [i for i in sorted(Wp) if Wp[i]["n_bg"] >= thr and C[i]["n_bg"] >= thr]
    D = np.array([Wp[i]["delta_dedup"] - C[i]["delta_dedup"] for i in keep])
    n1 = abs(np.median([t["delta_dedup"] for t in R if t["n_bg"] >= thr])) <= N1_MAX
    n2 = (np.median([t["delta_dedup"] for t in L if t["n_bg"] >= thr]) - np.median([C[i]["delta_dedup"] for i in keep])) >= N2_MIN
    out["dedup_0p2arcsec"] = dict(n_pairs=len(keep), **word_for(D, len(keep), n1, n2),
                                  n_objects_merged=int(sum((t["n_in"] + t["n_bg"]) - (t["n_in_dedup"] + t["n_bg_dedup"])
                                                           for t in list(Wp.values()) + list(C.values()) + L + R)))
    # (b2) PostgreSQL NaN semantics (NaN flux passes the flux cut; its own edge reference and threshold)
    refp = float(np.median([t["n_bg_pgnan"] for t in Wp.values()] + [t["n_bg_pgnan"] for t in W_unmatched]
                           + [C[i]["n_bg_pgnan"] for i in C] + [t["n_bg_pgnan"] for t in L]))
    thp = EDGE_FRAC * refp
    keep_p = [i for i in sorted(Wp) if Wp[i]["n_bg_pgnan"] >= thp and C[i]["n_bg_pgnan"] >= thp]
    D = np.array([Wp[i]["delta_pgnan"] - C[i]["delta_pgnan"] for i in keep_p])
    mR = float(np.median([t["delta_pgnan"] for t in R if t["n_bg_pgnan"] >= thp]))
    mL = float(np.median([t["delta_pgnan"] for t in L if t["n_bg_pgnan"] >= thp]))
    mC = float(np.median([C[i]["delta_pgnan"] for i in keep_p]))
    out["postgres_nan_semantics"] = dict(n_pairs=len(keep_p), edge_reference=refp,
                                         **word_for(D, len(keep_p), abs(mR) <= N1_MAX, (mL - mC) >= N2_MIN),
                                         median_delta_W=float(np.median([Wp[i]["delta_pgnan"] for i in keep_p])),
                                         median_delta_C=mC, median_delta_L=mL, median_delta_R=mR,
                                         extra_objects_counted=int(sum((t["n_in_pgnan"] + t["n_bg_pgnan"]) - (t["n_in"] + t["n_bg"])
                                                                       for t in list(Wp.values()) + list(C.values()) + L + R)))
    # (c) grade A pairs only (W lens grade A)
    keep_a = [i for i in keep if Wp[i]["grade"] == "A"]
    D = np.array([Wp[i]["delta"] - C[i]["delta"] for i in keep_a])
    out["W_grade_A_only"] = dict(n_pairs=len(keep_a), **word_for(D, len(keep_a), True, True))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"targets": build_targets, "selftest": selftest, "fetch": fetch, "grade": grade}.get(
        cmd, lambda: sys.exit(__doc__))()
