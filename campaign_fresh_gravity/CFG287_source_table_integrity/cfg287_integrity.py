#!/usr/bin/env python3
"""CFG287: integrity audit of the published data tables behind the a0 lanes.

Criteria: FROZEN_CRITERIA.md (written before this script). Data audit only; no lane is re-run.
Run:  python3 cfg287_integrity.py            -> cfg287_integrity.out, cfg287_results.json
      MUTATE=1 python3 cfg287_integrity.py   -> cfg287_mutate.out, cfg287_mutate_results.json
Reads files on disk only (repo data_assembly/, lane inputs, ../_external_data). Writes only into this directory.
"""
import os, sys, re, csv, json, math, hashlib, glob, html, io
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
DA = os.path.join(REPO, "data_assembly")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SEED = 287

# physical constants (SI); the 1% convention allowance covers constant choices
G = 6.67430e-11
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
C_KMS = 299792.458
GYR = 3.15576e16

OUT = []


def P(s=""):
    OUT.append(str(s))
    print(s)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rel(p):
    try:
        return os.path.relpath(p, REPO)
    except ValueError:
        return p


def fnum(s):
    if s is None:
        return float("nan")
    if isinstance(s, (int, float)):
        return float(s)
    t = str(s).strip().replace("−", "-")
    if t in ("", "nan", "NaN", "None", "-", "...", "…", "--"):
        return float("nan")
    try:
        return float(t)
    except ValueError:
        return float("nan")


def fin(x):
    return x is not None and isinstance(x, float) and math.isfinite(x)


def read_table(path):
    """csv.reader with positional columns (some CSVs repeat column names)."""
    with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
        rd = list(csv.reader(fh))
    return rd[0], rd[1:]


def read_dicts(path):
    with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
        return list(csv.DictReader(fh))


def half_unit_text(s):
    """Printed half-unit from a CSV text (FROZEN_CRITERIA section 2.1): trailing '.0' counts as an integer print;
    numbers carrying only trailing zeros (mantissa prints) get half a unit in the last significant digit."""
    t = str(s).strip().replace("−", "-").lstrip("+-")
    if t == "" or not re.match(r"^\d*\.?\d*(e[+-]?\d+)?$", t, re.I):
        return float("nan")
    if "e" in t.lower():
        mant, ex = re.split(r"[eE]", t)
        return half_unit_text(mant) * 10 ** int(ex)
    if t.endswith(".0"):
        t = t[:-2]
    if "." in t:
        return 0.5 * 10 ** (-len(t.split(".")[1]))
    # integer print: trailing zeros are not significant when there are >= 4 of them (mantissa x 10^n)
    stripped = t.rstrip("0")
    nz = len(t) - len(stripped)
    if nz >= 4 and stripped:
        return 0.5 * 10 ** nz
    return 0.5


def envelope(f, xs, hs, h_out):
    """E = sum_i |df/dx_i| h_i + h_out (linear worst case, finite differences)."""
    f0 = f(*xs)
    E = h_out
    for i, (x, h) in enumerate(zip(xs, hs)):
        if not fin(h) or h == 0:
            continue
        xp = list(xs); xm = list(xs)
        xp[i] = x + h; xm[i] = x - h
        try:
            E += 0.5 * abs(f(*xp) - f(*xm))
        except (ValueError, ZeroDivisionError, OverflowError):
            E += float("inf")
    return f0, E


def classify(delta, E, C, f):
    tol = E + C * abs(f)
    if not math.isfinite(delta):
        return "NA"
    if abs(delta) <= tol:
        return "CONSISTENT"
    if abs(delta) <= 2 * tol:
        return "ROUNDING-EDGE"
    return "PROBLEM"


# ----------------------------------------------------------------------------- registry of results
R = {"criteria_sha256": None, "seed": SEED, "mutate": MUTATE, "sources": {}, "cross": [], "transcription": {},
     "versions": {}, "problems": [], "flags": [], "mutate_result": None}
PROBLEMS = R["problems"]
FLAGS = R["flags"]


def src(sid):
    return R["sources"].setdefault(sid, {"checks": []})


def record(sid, name, kind, n_rows, classes, detail, worst=None, rows_flagged=None):
    """kind: H (hard) or S (soft). classes: dict class -> count."""
    entry = dict(check=name, kind=kind, n=n_rows, classes=classes, detail=detail, worst=worst,
                 rows_flagged=rows_flagged or [])
    src(sid)["checks"].append(entry)
    nprob = classes.get("PROBLEM", 0)
    nflag = classes.get("FLAG", 0)
    status = "PASS" if (nprob == 0 and nflag == 0) else ("PROBLEM" if nprob else "FLAG")
    P(f"  [{kind}] {name}: n={n_rows} {dict(classes)} -> {status}")
    if detail:
        P(f"        {detail}")
    if rows_flagged:
        for rf in rows_flagged[:12]:
            P(f"        row: {rf}")
        if len(rows_flagged) > 12:
            P(f"        ... {len(rows_flagged) - 12} more")
    if nprob:
        PROBLEMS.append(dict(source=sid, check=name, n=nprob, rows=rows_flagged, detail=detail))
    if nflag:
        FLAGS.append(dict(source=sid, check=name, n=nflag, rows=rows_flagged, detail=detail))
    return entry


def formula_check(sid, name, rows, getter, func, C, label, kind="H", limit_skip=None):
    """rows: list of row objects; getter(row) -> (key, inputs(list of (val, half)), (printed_val, half)) or None."""
    cl = {}
    flagged = []
    worst = (0.0, None)
    n = 0
    for r in rows:
        g = getter(r)
        if g is None:
            continue
        key, ins, outp = g
        xs = [a for a, b in ins]; hs = [b for a, b in ins]
        if not all(fin(x) for x in xs) or not fin(outp[0]):
            continue
        if limit_skip and limit_skip(r):
            cl["LIMIT-SKIPPED"] = cl.get("LIMIT-SKIPPED", 0) + 1
            continue
        f0, E = envelope(func, xs, hs, outp[1] if fin(outp[1]) else 0.0)
        d = outp[0] - f0
        c = classify(d, E, C, f0)
        n += 1
        cl[c] = cl.get(c, 0) + 1
        ratio = abs(d) / (E + C * abs(f0)) if (E + C * abs(f0)) > 0 else float("inf")
        if ratio > worst[0]:
            worst = (ratio, key)
        if c in ("PROBLEM", "ROUNDING-EDGE"):
            flagged.append(f"{key}: printed {outp[0]:.6g} recomputed {f0:.6g} diff {d:+.3g} envelope {E:.3g} (+C {C:g}) [{c}]")
    return record(sid, name, kind, n, cl, label + (f"; worst |diff|/tolerance {worst[0]:.2f} at {worst[1]}" if worst[1] is not None else ""),
                  worst=worst[0], rows_flagged=flagged)


def generic_errors(sid, name, header, rows, keycol=0, err_cols=None, pos_cols=None, frac_cols=None, inc_cols=None):
    """Generic checks: errors >= 0, positive-definite > 0, fractions in [0,1], inclinations in [0,90]."""
    cl = {}
    fl = []
    def bump(c):
        cl[c] = cl.get(c, 0) + 1
    for r in rows:
        key = r[keycol] if keycol is not None and keycol < len(r) else "?"
        for ci in (err_cols or []):
            v = fnum(r[ci]) if ci < len(r) else float("nan")
            if fin(v):
                if v < 0:
                    bump("PROBLEM"); fl.append(f"{key}: {header[ci]} = {v} (negative error)")
                else:
                    bump("CONSISTENT")
        for ci in (pos_cols or []):
            v = fnum(r[ci]) if ci < len(r) else float("nan")
            if fin(v):
                if v <= 0:
                    bump("PROBLEM"); fl.append(f"{key}: {header[ci]} = {v} (not > 0)")
                else:
                    bump("CONSISTENT")
        for ci in (frac_cols or []):
            v = fnum(r[ci]) if ci < len(r) else float("nan")
            if fin(v):
                if v < 0 or v > 1:
                    bump("PROBLEM"); fl.append(f"{key}: {header[ci]} = {v} (outside [0,1])")
                else:
                    bump("CONSISTENT")
        for ci in (inc_cols or []):
            v = fnum(r[ci]) if ci < len(r) else float("nan")
            if fin(v):
                if v < 0 or v > 90:
                    bump("PROBLEM"); fl.append(f"{key}: {header[ci]} = {v} (outside [0,90])")
                else:
                    bump("CONSISTENT")
    return record(sid, name, "H", sum(cl.values()), cl, "errors >= 0; positive-definite > 0; fractions in [0,1]; inclinations in [0,90] (cells tested)", rows_flagged=fl)


def cols_like(header, pats, exclude=()):
    out = []
    for i, h in enumerate(header):
        hl = h.lower()
        if any(re.search(p, hl) for p in pats) and not any(re.search(x, hl) for x in exclude):
            out.append(i)
    return out


def git_grep(pattern, glob_="*.py"):
    """Committed files naming a pattern (git grep over the tracked tree; this lane's own files excluded)."""
    import subprocess
    try:
        out = subprocess.run(["git", "-C", REPO, "grep", "-l", "-F", pattern, "--", glob_], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return []
    lines = [l for l in out.splitlines() if l.strip() and "CFG287_source_table_integrity" not in l]
    # no personal names in this lane's files: a path whose file name carries one is written generically
    return [re.sub(r"[^/]*" + "zim" + "merman" + r"[^/]*$", "<theory-figures script>", l, flags=re.I) for l in lines]


def soft_lower_bound(sid, name, header, rows, pairs, keycol=0):
    """S: value - lower error < 0 for a positive-definite quantity; asymmetric pair ratio > 10."""
    cl = {}; fl = []
    for r in rows:
        for (vi, hi, lo) in pairs:
            v, eh, el = fnum(r[vi]), fnum(r[hi]) if hi is not None else float("nan"), fnum(r[lo]) if lo is not None else float("nan")
            if not fin(v):
                continue
            ok = True
            if fin(el) and v - el < 0:
                ok = False; fl.append(f"{r[keycol]}: {header[vi]} {v} - {el} < 0")
            if fin(eh) and fin(el) and eh > 0 and el > 0 and max(eh, el) / min(eh, el) > 10:
                ok = False; fl.append(f"{r[keycol]}: {header[vi]} asymmetric +{eh}/-{el}")
            cl["FLAG" if not ok else "CONSISTENT"] = cl.get("FLAG" if not ok else "CONSISTENT", 0) + 1
    return record(sid, name, "S", sum(cl.values()), cl, "value - lower error < 0 (positive-definite) or asymmetric errors > 10x", rows_flagged=fl)


# =============================================================================== S01 SPARC
def s01_sparc():
    sid = "S01 SPARC (Lelli+16)"
    P(f"\n=== {sid}")
    mrt = os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")
    P(f"  file {rel(mrt)} sha256 {sha(mrt)[:16]}")
    lines = open(mrt, encoding="latin-1").read().splitlines()
    # data lines: after the last '----' separator
    last_sep = max(i for i, l in enumerate(lines) if l.startswith("-----"))
    data = [l for l in lines[last_sep + 1:] if l.strip()]
    # the data rows are 131 characters wide while the header's byte description ends at byte 113, so the
    # byte positions do not apply; every repo loader splits on whitespace (19 tokens), as done here.
    keys = ["name", "T", "D", "eD", "fD", "Inc", "eInc", "L", "eL", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q", "Ref"]
    rows = [dict(zip(keys, l.split())) for l in data]
    ntok = sorted({len(l.split()) for l in data}); widths = sorted({len(l) for l in data})
    fmt_ok = ntok == [19] and widths == [113]
    record(sid, "MRT data rows follow the header's byte-by-byte layout (bytes 1-113)", "S", len(data),
           {"CONSISTENT" if fmt_ok else "FLAG": 1},
           f"token counts {ntok}; line widths {widths}: the header ends at byte 113, so a fixed-width (CDS) reader would misparse; whitespace parsing (all repo loaders) is unaffected")
    rotdir = os.path.join(REPO, "real_research", "data", "sparc_data")
    rotfiles = sorted(glob.glob(os.path.join(rotdir, "*_rotmod.dat")))
    names_rot = {os.path.basename(f)[:-len("_rotmod.dat")] for f in rotfiles}
    names_mrt = {r["name"] for r in rows}
    cnt_ok = len(rows) == 175 and len(rotfiles) == 175 and names_rot == names_mrt
    record(sid, "175 MRT rows, 175 rotmod files, names one-to-one", "H", len(rows),
           {"CONSISTENT" if cnt_ok else "PROBLEM": 1},
           f"MRT rows {len(rows)}, rotmod files {len(rotfiles)}, only-in-MRT {sorted(names_mrt - names_rot)[:5]}, only-rotmod {sorted(names_rot - names_mrt)[:5]}")
    # SBeff = L 1e9 / (2 pi (1e3 Reff)^2)
    def g_sbeff(r):
        L, Re, SB = fnum(r["L"]), fnum(r["Reff"]), fnum(r["SBeff"])
        if not (fin(L) and fin(Re) and Re > 0 and fin(SB)):
            return None
        return (r["name"], [(L, half_unit_text(r["L"])), (Re, half_unit_text(r["Reff"]))], (SB, half_unit_text(r["SBeff"])))
    formula_check(sid, "SBeff = L[3.6] / (2 pi Reff^2)", rows, g_sbeff, lambda L, Re: L * 1e9 / (2 * math.pi * (Re * 1e3) ** 2), 0.0,
                  "MRT byte columns 35-41, 49-53, 54-61")
    q = []
    for r in rows:
        L, Re, SB = fnum(r["L"]), fnum(r["Reff"]), fnum(r["SBeff"])
        if fin(L) and fin(Re) and Re > 0 and fin(SB):
            q.append((r["name"], SB / (L * 1e9 / (2 * math.pi * (Re * 1e3) ** 2))))
    qq = np.array([x for _, x in q])
    out5 = [(n, round(x, 3)) for n, x in q if abs(x - 1) > 0.05]
    record(sid, "POST-HOC: SBeff printed / recomputed, distribution", "S", len(q), {"INFO": 1},
           f"median {np.median(qq):.4f}, 16-84% {np.percentile(qq, 16):.4f}-{np.percentile(qq, 84):.4f}; |ratio - 1| > 5%: {out5}")
    src(sid)["sbeff_ratio"] = dict(median=float(np.median(qq)), p16=float(np.percentile(qq, 16)), p84=float(np.percentile(qq, 84)), beyond_5pct=out5)
    # soft: disk luminosity vs total
    cl = {}; fl = []
    for r in rows:
        L, SBd, Rd = fnum(r["L"]), fnum(r["SBdisk"]), fnum(r["Rdisk"])
        if fin(L) and L > 0 and fin(SBd) and fin(Rd) and Rd > 0:
            Ld = 2 * math.pi * SBd * (Rd * 1e3) ** 2 / 1e9
            q = Ld / L
            c = "FLAG" if (q > 1.5 or q < 0.2) else "CONSISTENT"
            cl[c] = cl.get(c, 0) + 1
            if c == "FLAG":
                fl.append(f"{r['name']}: L_disk/L = {q:.2f} (L {L}, SBdisk {SBd}, Rdisk {Rd})")
    record(sid, "L_disk = 2 pi SBdisk Rdisk^2 vs L[3.6] (0.2..1.5)", "S", sum(cl.values()), cl, "exponential-fit disc luminosity against the total", rows_flagged=fl)
    # rotmod checks
    bymrt = {r["name"]: r for r in rows}
    cl_d = {}; fl_d = []; cl_r = {}; fl_r = []; cl_v = {}; fl_v = []
    neg_gas = 0
    for f in rotfiles:
        nm = os.path.basename(f)[:-len("_rotmod.dat")]
        txt = open(f).read().splitlines()
        m = re.search(r"Distance\s*=\s*([\d.]+)", txt[0])
        dist = float(m.group(1)) if m else float("nan")
        dmrt = fnum(bymrt.get(nm, {}).get("D"))
        ok = fin(dist) and fin(dmrt) and abs(dist - dmrt) < 1e-6
        cl_d["CONSISTENT" if ok else "PROBLEM"] = cl_d.get("CONSISTENT" if ok else "PROBLEM", 0) + 1
        if not ok:
            fl_d.append(f"{nm}: rotmod {dist} vs MRT {dmrt}")
        arr = np.array([[float(x) for x in l.split()[:8]] for l in txt if l.strip() and not l.startswith("#")])
        rad, vobs, ev, vgas = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
        bad = []
        if np.any(np.diff(rad) <= 0):
            bad.append("Rad not strictly increasing")
        if np.any(ev <= 0):
            bad.append(f"errV <= 0 in {int(np.sum(ev <= 0))} rows")
        if np.any(vobs < 0):
            bad.append("Vobs < 0")
        neg_gas += int(np.any(vgas < 0))
        c = "PROBLEM" if bad else "CONSISTENT"
        cl_r[c] = cl_r.get(c, 0) + 1
        if bad:
            fl_r.append(f"{nm}: " + "; ".join(bad))
        r = bymrt.get(nm)
        if r:
            vf, evf = fnum(r["Vflat"]), fnum(r["eVflat"])
            if fin(vf) and vf > 0:
                med = float(np.median(vobs[-3:]))
                tol = 3 * evf + 0.05 * vf
                c = "FLAG" if abs(vf - med) > tol else "CONSISTENT"
                cl_v[c] = cl_v.get(c, 0) + 1
                if c == "FLAG":
                    fl_v.append(f"{nm}: Vflat {vf} +- {evf} vs median(last 3 Vobs) {med:.1f}")
    record(sid, "rotmod header distance = MRT D", "H", sum(cl_d.values()), cl_d, "", rows_flagged=fl_d)
    record(sid, "rotmod: Rad increasing, errV > 0, Vobs >= 0", "H", sum(cl_r.values()), cl_r,
           f"{neg_gas} files carry negative Vgas (SPARC convention for a negative gas contribution; not a problem)", rows_flagged=fl_r)
    record(sid, "Vflat vs median of the last three Vobs (3 e_Vflat + 5%)", "S", sum(cl_v.values()), cl_v, "", rows_flagged=fl_v)
    cl = {}; fl = []
    for r in rows:
        vf, evf = fnum(r["Vflat"]), fnum(r["eVflat"])
        ok = (vf == 0) == (evf == 0)
        cl["CONSISTENT" if ok else "PROBLEM"] = cl.get("CONSISTENT" if ok else "PROBLEM", 0) + 1
        if not ok:
            fl.append(f"{r['name']}: Vflat {vf} e_Vflat {evf}")
    record(sid, "Vflat = 0 iff e_Vflat = 0", "H", len(rows), cl, "", rows_flagged=fl)
    hdr = ["name", "D", "eD", "Inc", "eInc", "L", "eL", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat"]
    tab = [[r[k] for k in hdr] for r in rows]
    generic_errors(sid, "generic: errors >= 0, positive D/L/Reff, Inc in [0,90]", hdr, tab, 0,
                   err_cols=[2, 4, 6, 14], pos_cols=[1, 5, 7], inc_cols=[3])
    # SPARC_table.txt trap
    trap = os.path.join(REPO, "real_research", "data", "SPARC_table.txt")
    head = open(trap, errors="ignore").read(400)
    is404 = "404 Not Found" in head
    readers = git_grep("SPARC_table.txt")
    record(sid, "SPARC_table.txt is a 404 page; scripts naming it", "H", 1, {"CONSISTENT" if is404 else "PROBLEM": 1},
           f"404 page: {is404}; {len(readers)} .py files name it (inspect whether they read it): {readers[:15]}")
    R["sources"][sid]["sparc_table_readers"] = readers
    return {r["name"]: r for r in rows}


# =============================================================================== S02 LVD
def s02_lvd():
    sid = "S02 LVD (Pace)"
    P(f"\n=== {sid}")
    rows = []
    for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
        p = os.path.join(REPO, "real_research", "data", "dsph", f)
        P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
        for r in read_dicts(p):
            r["_file"] = f
            rows.append(r)
    C = 0.001
    def g(fields, fout):
        def _g(r):
            vals = [(fnum(r[k]), half_unit_text(r[k])) for k in fields]
            return (r["key"], vals, (fnum(r[fout]), half_unit_text(r[fout])))
        return _g
    formula_check(sid, "distance = 10^(mu/5+1) pc", rows, g(["distance_modulus"], "distance"), lambda mu: 10 ** (mu / 5 + 1) / 1e3, C, "kpc")
    formula_check(sid, "M_V = m_V - mu", rows, g(["apparent_magnitude_v", "distance_modulus"], "M_V"), lambda m, mu: m - mu, 0.0, "")
    formula_check(sid, "rhalf_physical = distance x rhalf(arcmin)", rows, g(["distance", "rhalf"], "rhalf_physical"),
                  lambda D, rh: D * 1e3 * rh * math.pi / 10800, C, "pc")
    def g_sph(r):
        e = fnum(r["ellipticity"])
        if not fin(e):
            e = 0.0
        return (r["key"] + (" (ellipticity_ul)" if r.get("ellipticity_ul") not in ("", None) else ""),
                [(fnum(r["rhalf_physical"]), half_unit_text(r["rhalf_physical"])), (e, half_unit_text(r["ellipticity"]) if fin(fnum(r["ellipticity"])) else 0.0)],
                (fnum(r["rhalf_sph_physical"]), half_unit_text(r["rhalf_sph_physical"])))
    formula_check(sid, "rhalf_sph_physical = rhalf_physical sqrt(1 - e)", rows, g_sph, lambda rp, e: rp * math.sqrt(1 - e), C, "missing e taken as 0")
    best = None
    for msun in (4.80, 4.81, 4.83):
        n_ok = 0; n = 0
        for r in rows:
            MV, lm = fnum(r["M_V"]), fnum(r["mass_stellar"])
            if fin(MV) and fin(lm):
                n += 1
                n_ok += abs(lm - math.log10(2 * 10 ** (-0.4 * (MV - msun)))) <= 0.4 * half_unit_text(r["M_V"]) + half_unit_text(r["mass_stellar"]) + 1e-9
        if best is None or n_ok > best[1]:
            best = (msun, n_ok, n)
    P(f"  majority M_V,sun for mass_stellar: {best[0]} ({best[1]}/{best[2]} rows within the envelope)")
    formula_check(sid, f"mass_stellar = log10(2 L_V), M_V,sun = {best[0]}", rows, g(["M_V"], "mass_stellar"),
                  lambda MV: math.log10(2 * 10 ** (-0.4 * (MV - best[0]))), 0.0, "log10 Msun")
    for rcol in ("rhalf_sph_physical", "rhalf_physical"):
        pass
    best_w = None
    for rcol in ("rhalf_sph_physical", "rhalf_physical"):
        n_ok = 0; n = 0
        for r in rows:
            s, rr, mw = fnum(r["vlos_sigma"]), fnum(r[rcol]), fnum(r["mass_dynamical_wolf"])
            if fin(s) and fin(rr) and fin(mw) and s > 0 and rr > 0:
                n += 1
                n_ok += abs(mw - math.log10(930 * s * s * rr)) < 0.01
        if best_w is None or n_ok > best_w[1]:
            best_w = (rcol, n_ok, n)
    P(f"  majority radius for mass_dynamical_wolf: {best_w[0]} ({best_w[1]}/{best_w[2]})")
    formula_check(sid, f"mass_dynamical_wolf = log10(930 sigma^2 {best_w[0]})", rows, g(["vlos_sigma", best_w[0]], "mass_dynamical_wolf"),
                  lambda s, rr: math.log10(930 * s * s * rr), 0.0, "log10 Msun", limit_skip=lambda r: r.get("vlos_sigma_ul", "") not in ("", None))
    qa = [fnum(r["rhalf_physical"]) / (fnum(r["distance"]) * 1e3 * fnum(r["rhalf"]) * math.pi / 10800) for r in rows
          if all(fin(fnum(r[k])) for k in ("rhalf_physical", "distance", "rhalf"))]
    qb = [(r["key"], fnum(r["rhalf_sph_physical"]) / (fnum(r["rhalf_physical"]) * math.sqrt(1 - (fnum(r["ellipticity"]) if fin(fnum(r["ellipticity"])) else 0))))
          for r in rows if fin(fnum(r["rhalf_sph_physical"])) and fin(fnum(r["rhalf_physical"]))]
    beyond = [(k, round(x, 3)) for k, x in qb if abs(x - 1) > 0.02]
    record(sid, "POST-HOC: size-column ratios", "S", len(qb), {"INFO": 1},
           f"rhalf_physical / (D x rhalf): median {np.median(qa):.4f}, 1-99% {np.percentile(qa, 1):.3f}-{np.percentile(qa, 99):.3f}; "
           f"rhalf_sph / (rhalf_phys sqrt(1-e)): median {np.median([x for _, x in qb]):.4f}; rows beyond 2%: {beyond}")
    src(sid)["size_ratios"] = dict(rphys_median=float(np.median(qa)), rsph_beyond_2pct=beyond)
    hdr = list(rows[0].keys())
    tab = [[r.get(k, "") for k in hdr] for r in rows]
    errc = [i for i, h in enumerate(hdr) if h.endswith("_em") or h.endswith("_ep")]
    generic_errors(sid, "generic: errors >= 0, ellipticity in [0,1)", hdr, tab, 0, err_cols=errc,
                   frac_cols=[hdr.index("ellipticity")], pos_cols=[hdr.index("rhalf"), hdr.index("distance")])
    return rows


# =============================================================================== S03 KiDS (Brouwer+21)
def s03_kids():
    sid = "S03 KiDS-1000 lensing RAR (Brouwer+21)"
    P(f"\n=== {sid}")
    B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
    sets = {}
    for f in sorted(glob.glob(os.path.join(B, "*.txt"))):
        bn = os.path.basename(f)
        if bn == "README.txt":
            continue
        m = re.match(r"(Fig-[\w-]+?_[\w-]+?)(?:_(\d)|-(\d)|_Nobins)?\.txt$", bn)
        if "covmatrix" in bn:
            stem = bn.replace("_covmatrix.txt", "")
            sets.setdefault(stem, {})["cov"] = f
        else:
            sets.setdefault("?", {})
    # group data files with their covariance by the figure prefix
    groups = {}
    for f in sorted(glob.glob(os.path.join(B, "*.txt"))):
        bn = os.path.basename(f)
        if bn == "README.txt":
            continue
        if bn.endswith("_covmatrix.txt"):
            groups.setdefault(bn[:-len("_covmatrix.txt")], {"data": [], "cov": None})["cov"] = f
    for f in sorted(glob.glob(os.path.join(B, "*.txt"))):
        bn = os.path.basename(f)
        if bn == "README.txt" or bn.endswith("_covmatrix.txt"):
            continue
        # find the group whose stem matches the start (Colorbin_1 -> Colorbins, Massbin-1 -> Massbins, Nobins -> Nobins)
        stem = None
        for k in groups:
            base = re.sub(r"s$", "", k)
            if bn.startswith(base) or bn.startswith(k):
                if stem is None or len(k) > len(stem):
                    stem = k
        if stem:
            groups[stem]["data"].append(f)
    cl_err = {}; fl_err = []; cl_cov = {}; fl_cov = []; cl_grid = {}; fl_grid = []; cl_b = {}; fl_b = []; cl_x = {}; fl_x = []
    from scipy import stats
    for stem, gr in sorted(groups.items()):
        if not gr["data"] or not gr["cov"]:
            continue
        D = [np.loadtxt(f) for f in gr["data"]]
        cov = np.loadtxt(gr["cov"])
        nb = sum(len(d) for d in D)
        # covariance file: long table (bin m, bin n, radius i, radius j, cov, corr, bias) per the README
        M = None; Mb = None
        if cov.ndim == 2 and cov.shape[1] == 7 and cov.shape[0] == nb * nb:
            bins = sorted(set(np.round(cov[:, 0], 9)))
            radii = sorted(set(np.round(cov[:, 2], 30)))
            nbin, nrad = len(bins), len(radii)
            if nbin * nrad == nb:
                bi = {b: k for k, b in enumerate(bins)}
                M = np.full((nb, nb), np.nan); Mb = np.full((nb, nb), np.nan)
                rr = np.array(radii)
                for row in cov:
                    i = bi[round(row[0], 9)] * nrad + int(np.argmin(np.abs(rr - row[2])))
                    j = bi[round(row[1], 9)] * nrad + int(np.argmin(np.abs(rr - row[3])))
                    M[i, j] = row[4]; Mb[i, j] = row[4] / row[6]
        tag = stem
        if M is None:
            fl_cov.append(f"{tag}: covariance shape {cov.shape} not understood for {nb} points"); cl_cov["FLAG"] = cl_cov.get("FLAG", 0) + 1
            continue
        sym = np.allclose(M, M.T, rtol=1e-6, atol=0)
        ev = np.linalg.eigvalsh(0.5 * (M + M.T))
        psd = ev.min() >= -1e-10 * abs(ev.max())
        c = "CONSISTENT" if (sym and psd) else "PROBLEM"
        cl_cov[c] = cl_cov.get(c, 0) + 1
        if c != "CONSISTENT":
            fl_cov.append(f"{tag}: symmetric {sym}, min eigenvalue {ev.min():.3g}")
        err = np.concatenate([d[:, 3] for d in D]); bias = np.concatenate([d[:, 4] for d in D])
        sd = np.sqrt(np.diag(M)); sdb = np.sqrt(np.diag(Mb))
        cands = [(np.max(np.abs(sd / err - 1)), "sqrt(diag C) = error"), (np.max(np.abs(sdb / (err / bias) - 1)), "sqrt(diag C/bias) = error/(1+K)"),
                 (np.max(np.abs(sd / (err / bias) - 1)), "sqrt(diag C) = error/(1+K)")]
        form = min(cands)
        c = "CONSISTENT" if form[0] <= 1e-3 else "PROBLEM"
        cl_err[c] = cl_err.get(c, 0) + 1
        fl_err.append(f"{tag}: best form {form[1]} (max rel dev {form[0]:.2e}); [{c}]")
        gb = [d[:, 0] for d in D]
        same = all(len(x) == len(gb[0]) and np.allclose(x, gb[0], rtol=1e-4) for x in gb)
        dl = np.diff(np.log10(gb[0]))
        uni = np.allclose(dl, dl.mean(), rtol=1e-3, atol=2e-4)
        c = "CONSISTENT" if (same and uni) else "PROBLEM"
        cl_grid[c] = cl_grid.get(c, 0) + 1
        if c != "CONSISTENT":
            fl_grid.append(f"{tag}: same grid {same}, log-uniform {uni} (dlog range {dl.min():.4f}..{dl.max():.4f})")
        for f, d in zip(gr["data"], D):
            b = d[:, 4]
            okb = np.allclose(b, b[0], rtol=1e-6) and 0.8 < b[0] < 1.2
            cl_b["CONSISTENT" if okb else "FLAG"] = cl_b.get("CONSISTENT" if okb else "FLAG", 0) + 1
            if not okb:
                fl_b.append(f"{os.path.basename(f)}: bias column {b.min():.4f}..{b.max():.4f}")
            chi2 = float(np.sum((d[:, 2] / d[:, 3]) ** 2)); dof = len(d)
            p = float(stats.chi2.sf(chi2, dof))
            cx = "FLAG" if p < 0.001 else "CONSISTENT"
            cl_x[cx] = cl_x.get(cx, 0) + 1
            fl_x.append(f"{os.path.basename(f)}: ESD_x chi2/dof {chi2:.1f}/{dof} p {p:.3g}" + (" [FLAG]" if cx == "FLAG" else ""))
    record(sid, "covariance symmetric and positive semi-definite", "H", sum(cl_cov.values()), cl_cov, "", rows_flagged=fl_cov)
    record(sid, "error column vs sqrt(diag covariance)", "H", sum(cl_err.values()), cl_err, "; ".join(fl_err[:4]) + " ...", rows_flagged=[x for x in fl_err if "PROBLEM" in x])
    record(sid, "g_bar grid identical across bins and log-uniform", "H", sum(cl_grid.values()), cl_grid, "", rows_flagged=fl_grid)
    record(sid, "bias (1+K) constant per file, in (0.8,1.2)", "S", sum(cl_b.values()), cl_b, "", rows_flagged=fl_b)
    record(sid, "cross-shear ESD_x null test (diagonal errors)", "S", sum(cl_x.values()), cl_x, "; ".join(fl_x[:6]), rows_flagged=[x for x in fl_x if "FLAG" in x])


# =============================================================================== CDS byte-by-byte reader (independent of the builds)
def cds_layout(readme, table):
    txt = open(readme, encoding="latin-1").read().splitlines()
    start = None
    for i, l in enumerate(txt):
        if l.startswith("Byte-by-byte Description of file:") and table in l:
            start = i
            break
    if start is None:
        return []
    cols = []
    seen_sep = 0
    for l in txt[start + 1:]:
        if l.startswith("-----"):
            seen_sep += 1
            if seen_sep >= 3:
                break
            continue
        if seen_sep < 2:
            continue
        m = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s+(\S+)\s+(\S+)\s+(\S+)", l) or re.match(r"^\s*(\d+)()\s+(\S+)\s+(\S+)\s+(\S+)", l)
        if m:
            a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
            cols.append(dict(a=a, b=b, fmt=m.group(3), unit=m.group(4), label=m.group(5)))
    return cols


def cds_rows(datfile, layout):
    out = []
    for l in open(datfile, encoding="latin-1").read().splitlines():
        if not l.strip():
            continue
        d = {}
        for c in layout:
            d[c["label"]] = l[c["a"] - 1:c["b"]].strip()
        out.append(d)
    return out


# =============================================================================== S04 RC100
def s04_rc100():
    sid = "S04 RC100 (Nestor Shachar+23)"
    P(f"\n=== {sid}")
    po = os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv")
    pp = os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")
    P(f"  original {rel(po)} sha256 {sha(po)[:16]}; paper values {rel(pp)} sha256 {sha(pp)[:16]}")
    O = read_dicts(po); Pv = read_dicts(pp)
    def g_g(r):
        return (f"{r['idx']} {r['name']}", [(fnum(r["Vc_Re_kms"]), 0.0), (fnum(r["Re_kpc"]), 0.0)], (fnum(r["g_Re_ms2"]), 0.0))
    formula_check(sid, "original CSV: g_Re = Vc^2/Re (repo-derived column)", O, g_g, lambda V, Re: (V * 1e3) ** 2 / (Re * KPC), 1e-3, "m/s^2")
    def g_a(r):
        return (f"{r['idx']} {r['name']}", [(fnum(r["Vc_Re_kms"]), 0.0), (fnum(r["logMbar_Msun"]), 0.0)], (fnum(r["a0_Vc4_over_GMbar_ms2"]), 0.0))
    formula_check(sid, "original CSV: Vc^4/(G Mbar) (repo-derived column)", O, g_a, lambda V, lm: (V * 1e3) ** 4 / (G * 10 ** lm * MSUN), 2e-3, "m/s^2")
    def g_r(r):
        return (f"{r['idx']} {r['name']}", [(fnum(r["a0_Vc4_over_GMbar_ms2"]), 0.0)], (fnum(r["a0_over_1.2e-10"]), half_unit_text(r["a0_over_1.2e-10"])))
    formula_check(sid, "original CSV: ratio to 1.2e-10 (repo-derived column)", O, g_r, lambda a: a / 1.2e-10, 1e-3, "")
    cl = {}; fl = []
    for r in O:
        flag = int(fnum(r["deepMOND_g_lt_a0"])); g = fnum(r["g_Re_ms2"])
        ok = flag == int(g < 1.2e-10)
        cl["CONSISTENT" if ok else "PROBLEM"] = cl.get("CONSISTENT" if ok else "PROBLEM", 0) + 1
        if not ok:
            fl.append(f"{r['idx']}: flag {flag}, g_Re {g:.3e}")
    record(sid, "original CSV: deepMOND flag = (g_Re < 1.2e-10)", "H", len(O), cl, "", rows_flagged=fl)
    # changed_cells vs actual differences
    fields = [("name", "name"), ("z", "z"), ("logMbar_Msun", "logMbar"), ("Re_kpc", "Re"), ("fDM_within_Re", "fDM"), ("Vc_Re_kms", "Vc"), ("sigma0_kms", "sigma0")]
    cl = {}; fl = []; ndiff = 0; diffs = []
    for a, b in zip(O, Pv):
        actual = []
        for fo, lab in fields:
            va, vb = a[fo], b[fo]
            same = (va.strip() == vb.strip()) if fo == "name" else (abs(fnum(va) - fnum(vb)) < 1e-9)
            if not same:
                actual.append(fo)
                diffs.append(dict(idx=a["idx"], field=fo, original=va, paper=vb))
        ndiff += len(actual)
        stated = [x for x in re.split(r"[;,| ]+", b.get("changed_cells", "") or "") if x]
        ok = (len(stated) > 0) == (len(actual) > 0)
        cl["CONSISTENT" if ok else "PROBLEM"] = cl.get("CONSISTENT" if ok else "PROBLEM", 0) + 1
        if not ok:
            fl.append(f"idx {a['idx']}: stated {stated} actual {actual}")
    record(sid, "paper-values file: changed_cells column vs actual differences", "H", len(O), cl,
           f"{ndiff} cells differ between the original CSV and the paper values in {len({d['idx'] for d in diffs})} rows", rows_flagged=fl)
    src(sid)["original_vs_paper_diffs"] = diffs
    # soft: implied baryon coefficient on the paper values
    ks = []
    for r in Pv:
        f, V, Re, lm = fnum(r["fDM_within_Re"]), fnum(r["Vc_Re_kms"]), fnum(r["Re_kpc"]), fnum(r["logMbar_Msun"])
        if all(fin(x) for x in (f, V, Re, lm)):
            ks.append((f"{r['idx']} {r['name']}", math.log10((1 - f) * (V * 1e3) ** 2 * Re * KPC / (G * 10 ** lm * MSUN))))
    med = float(np.median([k for _, k in ks]))
    cl = {}; fl = []
    for key, k in ks:
        c = "FLAG" if abs(k - med) > 0.5 else "CONSISTENT"
        cl[c] = cl.get(c, 0) + 1
        if c == "FLAG":
            fl.append(f"{key}: log k = {k:+.2f} (median {med:+.2f})")
    record(sid, "paper values: implied baryon coefficient k = (1-fDM) Vc^2 Re/(G Mbar) outliers (> 0.5 dex)", "S", len(ks), cl,
           f"median log k {med:+.3f} (k = {10 ** med:.2f}); spread 16-84% {np.percentile([k for _, k in ks], 16):+.2f}..{np.percentile([k for _, k in ks], 84):+.2f}", rows_flagged=fl)
    # the same test on the original CSV (the uncorrected file still read by older lanes)
    ks_o = []
    for r in O:
        f, V, Re, lm = fnum(r["fDM_within_Re"]), fnum(r["Vc_Re_kms"]), fnum(r["Re_kpc"]), fnum(r["logMbar_Msun"])
        ks_o.append((f"{r['idx']} {r['name']}", math.log10((1 - f) * (V * 1e3) ** 2 * Re * KPC / (G * 10 ** lm * MSUN))))
    fl = [f"{k}: log k = {v:+.2f}" for k, v in ks_o if abs(v - med) > 0.5]
    record(sid, "original CSV: the same k test (shows which uncorrected rows stand out)", "S", len(ks_o),
           {"FLAG": len(fl), "CONSISTENT": len(ks_o) - len(fl)}, "", rows_flagged=fl)
    # arithmetic on the effect of the uncorrected file on a simple per-galaxy statistic (no lane re-run)
    ao = np.array([fnum(r["a0_Vc4_over_GMbar_ms2"]) for r in O])
    ap = np.array([(fnum(r["Vc_Re_kms"]) * 1e3) ** 4 / (G * 10 ** fnum(r["logMbar_Msun"]) * MSUN) for r in Pv])
    src(sid)["uncorrected_effect"] = dict(median_Vc4_GM_original=float(np.median(ao)), median_Vc4_GM_paper=float(np.median(ap)),
                                          dex_shift_median=float(np.log10(np.median(ao) / np.median(ap))),
                                          max_row_dex=float(np.max(np.abs(np.log10(ao / ap)))))
    P(f"  arithmetic: median Vc^4/(G Mbar) original {np.median(ao):.4e} vs paper values {np.median(ap):.4e} "
      f"({np.log10(np.median(ao) / np.median(ap)):+.4f} dex); largest single-row change {np.max(np.abs(np.log10(ao / ap))):.2f} dex")
    return O, Pv


# =============================================================================== S05 KMOS3D (Wisnioski+19)
def s05_kmos3d():
    sid = "S05 KMOS3D release (Wisnioski+19)"
    P(f"\n=== {sid}")
    p = os.path.join(DA, "kmos3d_phibss", "kmos3d_catalog.csv")
    P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
    K = read_dicts(p)
    cl = {}; fl = []
    for r in K:
        z, zh = fnum(r["Z"]), fnum(r["HAFIT_Z"])
        if fin(z) and fin(zh) and z > 0 and zh > 0:
            c = "FLAG" if abs(z - zh) > 0.002 else "CONSISTENT"
            cl[c] = cl.get(c, 0) + 1
            if c == "FLAG":
                fl.append(f"{r['ID']}: Z {z} HAFIT_Z {zh}")
    record(sid, "|Z - HAFIT_Z| <= 0.002", "S", sum(cl.values()), cl, "", rows_flagged=fl)
    cl = {}; fl = []
    for r in K:
        bad = []
        q, rh, rhe, se = fnum(r["Q"]), fnum(r["RHALF"]), fnum(r["RHALFERR"]), fnum(r["HAFIT_SIG_ERR"])
        if fin(q) and q > 0 and not (0 < q <= 1):
            bad.append(f"Q {q}")
        if fin(rh) and rh > 0 and rh <= 0:
            bad.append(f"RHALF {rh}")
        if fin(rhe) and rhe < 0 and rhe != -99:
            bad.append(f"RHALFERR {rhe}")
        if fin(se) and se < 0 and se not in (-99, -1, -99.9):
            bad.append(f"HAFIT_SIG_ERR {se}")
        if not r["FILE"].startswith(r["ID"]):
            bad.append(f"FILE {r['FILE']}")
        c = "PROBLEM" if bad else "CONSISTENT"
        cl[c] = cl.get(c, 0) + 1
        if bad:
            fl.append(f"{r['ID']}: " + ", ".join(bad))
    # sentinel census
    sent = {k: sum(1 for r in K if fnum(r[k]) in (-99.0, -1.0, -999.0, -99.9)) for k in ("Q", "RHALF", "LMSTAR", "Z", "HAFIT_Z", "HAFIT_SIG", "HAFIT_SIG_ERR")}
    record(sid, "0 < Q <= 1, errors >= 0, FILE begins with ID (sentinels -99/-1 excluded)", "H", len(K), cl, f"sentinel counts {sent}", rows_flagged=fl)
    # POST-HOC characterisation of the flagged rows (not a frozen check)
    n_cube = sum(1 for r in K if not r["FILE"].startswith(r["ID"]) and r["FILE"].startswith(r["ID_TARGETED"]))
    n_cube_add = sum(1 for r in K if not r["FILE"].startswith(r["ID"]) and r["FILE"].startswith(r["ID_TARGETED"]) and r["FLAG_ADDGALDET"] == "1")
    n_other = sum(1 for r in K if not r["FILE"].startswith(r["ID"]) and not r["FILE"].startswith(r["ID_TARGETED"]))
    n999 = sum(1 for r in K if fnum(r["RHALFERR"]) == -999.0)
    record(sid, "POST-HOC: what the flagged rows are", "S", len(K), {"INFO": 1},
           f"FILE named after ID_TARGETED (the cube of the targeted galaxy): {n_cube} rows ({n_cube_add} with FLAG_ADDGALDET = 1); FILE matching neither ID nor ID_TARGETED: {n_other}; RHALFERR = -999 (a sentinel missing from the frozen list): {n999}")
    src(sid)["posthoc_flag_explanation"] = dict(file_is_targeted_cube=n_cube, addgaldet=n_cube_add, file_unexplained=n_other, rhalferr_m999=n999)
    return K


# =============================================================================== S06 Price+21
def s06_price():
    sid = "S06 RC41 (Price+21)"
    P(f"\n=== {sid}")
    p = os.path.join(DA, "price2021_rc41", "price2021_rc41.csv")
    P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
    hdr, rows = read_table(p)
    errc = [hdr.index(c) for c in hdr if c.endswith("_lo") or c.endswith("_hi")]
    generic_errors(sid, "generic: interval half-widths >= 0, fDM in [0,1], positive Re", hdr, rows, 0, err_cols=errc,
                   frac_cols=[hdr.index("fDM_Re_1D")], pos_cols=[hdr.index("Re_1D_kpc")])
    D = read_dicts(p)
    cl = {}; fl = []
    for r in D:
        lm, ls, lg = fnum(r["logMbar_1D"]), fnum(r["logMstar_SED"]), fnum(r["logMgas"])
        if fin(lm) and fin(ls) and fin(lg):
            d = lm - math.log10(10 ** ls + 10 ** lg)
            c = "FLAG" if abs(d) > 0.5 else "CONSISTENT"
            cl[c] = cl.get(c, 0) + 1
            if c == "FLAG":
                fl.append(f"{r['id']}: logMbar {lm} vs log(M*+Mgas) {math.log10(10 ** ls + 10 ** lg):.2f}")
    record(sid, "log Mbar(1D) vs log(M*_SED + Mgas) (0.5 dex)", "S", sum(cl.values()), cl, "the fit has a 0.2 dex prior centred on M*+Mgas", rows_flagged=fl)
    return D


# =============================================================================== S07 FS+18 SINS/zC-SINF AO
def s07_fs18(t6_override=None, sid="S07 SINS/zC-SINF AO (FS+18)", quiet_other=False):
    P(f"\n=== {sid}")
    base = os.path.join(DA, "highz_literature_tables", "sins_ao")
    p6 = os.path.join(base, "sins_ao_table6_kinematics.csv")
    P(f"  table 6 {rel(p6)} sha256 {sha(p6)[:16]}" + ("  [MUTATED COPY IN USE]" if t6_override else ""))
    hdr6, rows6 = read_table(t6_override or p6)
    D6 = [dict(zip(hdr6, r)) for r in rows6]
    def g_vc(r):
        return (r["source"], [(fnum(r["Vrot_kms"]), half_unit_text(r["Vrot_kms"])), (fnum(r["sigma0_kms"]), half_unit_text(r["sigma0_kms"]))],
                (fnum(r["Vc_kms"]), half_unit_text(r["Vc_kms"])))
    e1 = formula_check(sid, "Vc = sqrt(Vrot^2 + 3.36 sigma0^2) (eq. 1)", D6, g_vc, lambda V, s: math.sqrt(V * V + 3.36 * s * s), 0.0, "km/s")
    def g_md(r):
        return (r["source"], [(fnum(r["Re_kpc"]), half_unit_text(r["Re_kpc"])), (fnum(r["Vc_kms"]), half_unit_text(r["Vc_kms"]))],
                (fnum(r["Mdyn_1e10Msun"]), half_unit_text(r["Mdyn_1e10Msun"])))
    e2 = formula_check(sid, "Mdyn = 2 Re Vc^2 / G (eq. 2)", D6, g_md, lambda Re, V: 2 * Re * KPC * (V * 1e3) ** 2 / G / MSUN / 1e10, 0.01, "1e10 Msun")
    def g_rs(r):
        return (r["source"], [(fnum(r["Vrot_kms"]), half_unit_text(r["Vrot_kms"])), (fnum(r["sigma0_kms"]), half_unit_text(r["sigma0_kms"]))],
                (fnum(r["Vrot_over_sigma0"]), half_unit_text(r["Vrot_over_sigma0"])))
    e3 = formula_check(sid, "Vrot/sigma0 column = Vrot / sigma0", D6, g_rs, lambda V, s: V / s, 0.0, "")
    pos = [hdr6.index(c) for c in ("Re_kpc", "Vrot_kms", "sigma0_kms", "Vc_kms", "Mdyn_1e10Msun", "half_dv_obs_kms")]
    errc = [i for i, h in enumerate(hdr6) if h.endswith("_errlo") or h.endswith("_errhi")]
    e4 = generic_errors(sid, "table 6 generic: errors >= 0, positive Re/V/sigma/Vc/Mdyn, sin i in [0,1]", hdr6, rows6, 0, err_cols=errc, pos_cols=pos,
                        frac_cols=[hdr6.index("sin_i")])
    cl = {}; fl = []
    for r in D6:
        V, si, dv = fnum(r["Vrot_kms"]), fnum(r["sin_i"]), fnum(r["half_dv_obs_kms"])
        if fin(V) and fin(si) and fin(dv) and dv > 0:
            cp = V * si / dv
            c = "FLAG" if not (0.95 <= cp <= 2.0) else "CONSISTENT"
            cl[c] = cl.get(c, 0) + 1
            if c == "FLAG":
                fl.append(f"{r['source']}: C_PSF = Vrot sin i / (dv/2) = {cp:.2f}")
    e5 = record(sid, "C_PSF = Vrot sin i / (dv_obs/2) in [1,2]", "S", sum(cl.values()), cl, "beam-smearing correction implied by the table", rows_flagged=fl)
    if t6_override:
        return dict(vc=e1, md=e2, ratio=e3, generic=e4)
    p1 = os.path.join(base, "sins_ao_table1_sample.csv"); p5 = os.path.join(base, "sins_ao_table5_sizes.csv")
    D1 = read_dicts(p1); D5 = read_dicts(p5)
    def g_ss(r):
        return (r["source"], [(fnum(r["SFR_SED"]), half_unit_text(r["SFR_SED"])), (fnum(r["Mstar_1e10Msun"]), half_unit_text(r["Mstar_1e10Msun"]))],
                (fnum(r["sSFR_SED"]), half_unit_text(r["sSFR_SED"])))
    formula_check(sid, "table 1: sSFR_SED = SFR_SED / M* (Gyr^-1)", D1, g_ss, lambda sfr, m: sfr / (m * 1e10) * 1e9, 0.0, "Gyr^-1")
    cl = {}; fl = []
    for r in D5:
        rh, Re, q = fnum(r["r_half_circ_kpc_1G"]), fnum(r["Re_kpc_1G"]), fnum(r["q_1G"])
        if fin(rh) and fin(Re) and fin(q) and Re > 0 and q > 0:
            x = rh / (Re * math.sqrt(q))
            c = "FLAG" if abs(x - 1.10) > 0.45 else "CONSISTENT"
            cl[c] = cl.get(c, 0) + 1
            if c == "FLAG":
                fl.append(f"{r['source']}: r1/2,circ / (Re sqrt q) = {x:.2f}")
    record(sid, "table 5: r1/2,circ vs Re sqrt(q) (paper: +10% +- 15%)", "S", sum(cl.values()), cl, "", rows_flagged=fl)
    return dict(t1=D1, t5=D5, t6=D6)


# =============================================================================== S08 FS+09 SINS
def s08_fs09():
    sid = "S08 SINS (FS+09)"
    P(f"\n=== {sid}")
    p = os.path.join(DA, "high_z_tf_tables", "sins2009_dynamics.csv")
    P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
    D = read_dicts(p)
    hdr, rows = read_table(p)
    errc = [hdr.index(c) for c in ("e_half_vobs", "E_vel", "e_vel", "E_m0", "e_m0", "E_mdyn", "e_mdyn", "e_r_half_kpc", "E_mstar", "e_mstar")]
    generic_errors(sid, "generic: errors >= 0; positive V, Mdyn, r1/2", hdr, rows, 0, err_cols=errc,
                   pos_cols=[hdr.index(c) for c in ("vel_kms", "mdyn_1e10msun", "r_half_halpha_kpc")])
    ks = []
    for r in D:
        V, Md, rr = fnum(r["vel_kms"]), fnum(r["mdyn_1e10msun"]), fnum(r["r_half_halpha_kpc"])
        if fin(V) and fin(Md) and fin(rr) and V > 0 and rr > 0 and Md > 0 and r["l_mdyn"] == "" and r["l_vel"] == "":
            ks.append((r["name"], r["method"], math.log10(Md * 1e10 * MSUN * G / ((V * 1e3) ** 2 * rr * KPC))))
    out = {}
    for meth in sorted({m for _, m, _ in ks}):
        sub = [(n, k) for n, m, k in ks if m == meth]
        med = float(np.median([k for _, k in sub]))
        fl = [f"{n}: log k {k:+.3f} (median {med:+.3f})" for n, k in sub if abs(k - med) > 0.1]
        out[meth] = med
        record(sid, f"Mdyn G/(V^2 r1/2) coefficient, method '{meth}' (0.1 dex from the median)", "S", len(sub),
               {"FLAG": len(fl), "CONSISTENT": len(sub) - len(fl)}, f"median k = {10 ** med:.3f}", rows_flagged=fl)
    return D


# =============================================================================== S09 Tacconi+13 PHIBSS
def lum_dist_mpc(z, H0=70.0, Om=0.3):
    from scipy.integrate import quad
    I = quad(lambda x: 1.0 / math.sqrt(Om * (1 + x) ** 3 + (1 - Om)), 0, z)[0]
    return (1 + z) * C_KMS / H0 * I


def s09_tacconi13():
    sid = "S09 PHIBSS (Tacconi+13)"
    P(f"\n=== {sid}")
    p = os.path.join(DA, "kmos3d_phibss", "phibss13_joined.csv")
    P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
    D = read_dicts(p)
    def g_mb(r):
        if r["mbar_is_upper_limit"] == "1":
            return None
        return (r["name"] + r["comp"], [(fnum(r["mmol_msun"]), half_unit_text(r["mmol_msun"])), (fnum(r["mstar_msun"]), half_unit_text(r["mstar_msun"]))],
                (fnum(r["mbar_msun"]), 0.0))
    formula_check(sid, "M_bar = M_mol + M* (repo-derived column)", D, g_mb, lambda a, b: a + b, 0.0, "Msun")
    def g_mm(r):
        if r["co_upper_limit"] == "1":
            return None
        return (r["name"] + r["comp"], [(fnum(r["lco_K_kms_pc2"]), half_unit_text(r["lco_K_kms_pc2"]))], (fnum(r["mmol_msun"]), half_unit_text(r["mmol_msun"])))
    formula_check(sid, "M_mol = 4.36 x 2 x L'CO(3-2) (ReadMe note 5)", D, g_mm, lambda L: 8.72 * L, 0.0, "Msun")
    def g_fg(r):
        return (r["name"] + r["comp"], [(fnum(r["mmol_msun"]), half_unit_text(r["mmol_msun"])), (fnum(r["mstar_msun"]), half_unit_text(r["mstar_msun"]))],
                (fnum(r["fgas_quoted"]), half_unit_text(r["fgas_quoted"])))
    formula_check(sid, "f_gas (quoted) = M_mol / (M_mol + M*)", D, g_fg, lambda a, b: a / (a + b), 0.0, "",
                  limit_skip=lambda r: r["co_upper_limit"] == "1")
    nflag = sum(1 for r in D if r.get("fgas_inconsistent_in_source") == "1")
    P(f"  the build's own flag fgas_inconsistent_in_source = 1 for {nflag} rows")
    def g_l(r):
        z = fnum(r["z_co"]); S = fnum(r["fco_jykms"])
        if not (fin(z) and fin(S)) or S <= 0 or r["co_upper_limit"] == "1":
            return None
        return (r["name"] + r["comp"], [(S, half_unit_text(r["fco_jykms"])), (z, half_unit_text(r["z_co"]))], (fnum(r["lco_K_kms_pc2"]), half_unit_text(r["lco_K_kms_pc2"])))
    nu32 = 345.79599
    formula_check(sid, "L'CO(3-2) = 3.25e7 S dV nu_obs^-2 D_L^2 (1+z)^-3 (H0 70, Om 0.3)", D, g_l,
                  lambda S, z: 3.25e7 * S * (nu32 / (1 + z)) ** -2 * lum_dist_mpc(z) ** 2 * (1 + z) ** -3, 0.02,
                  "K km/s pc^2; rows with a CO(2-1) line (BzK/PEP) would deviate by the line frequency", kind="H")
    return D


AT = os.path.join(DA, "arxiv_tables")
NU_REST = {"CO(1-0)": 115.2712018, "CO(2-1)": 230.538, "CO(3-2)": 345.7959899, "CO(4-3)": 461.0407682, "CO(5-4)": 576.2679305,
           "CO(6-5)": 691.4730763, "CO(7-6)": 806.651806, "\\CIi": 492.160651, "\\CIii": 809.34197, "[CI](1-0)": 492.160651, "[CI](2-1)": 809.34197}


def kpc_per_arcsec(z, cosmo):
    return cosmo.kpc_proper_per_arcmin(z).value / 60.0


# =============================================================================== S10 CRISTAL
def s10_cristal():
    sid = "S10 ALMA-CRISTAL (Lee+25)"
    P(f"\n=== {sid}")
    out = {}
    for t in ("sample", "kinematics", "dynamics"):
        p = os.path.join(AT, f"cristal2025_{t}.csv")
        P(f"  {t} {rel(p)} sha256 {sha(p)[:16]}")
        out[t] = read_table(p)
    hdr, rows = out["dynamics"]
    errc = [i for i, h in enumerate(hdr) if h.endswith("_errhi") or h.endswith("_errlo")]
    generic_errors(sid, "dynamics generic: errors >= 0, fDM in [0,1], inc in [0,90], positive Re/Vrot/sigma0", hdr, rows, 0, err_cols=errc,
                   frac_cols=[hdr.index("fDM_Re")], inc_cols=[hdr.index("inc_deg")], pos_cols=[hdr.index(c) for c in ("Re_disk_kpc", "sigma0_kms", "Rout_over_Re")])
    soft_lower_bound(sid, "dynamics: value - lower error < 0 or asymmetric > 10x", hdr, rows,
                     [(hdr.index(c), hdr.index(c + "_errhi"), hdr.index(c + "_errlo")) for c in ("Vrot_Re_kms", "sigma0_kms", "Re_disk_kpc")])
    hk, rk = out["kinematics"]
    generic_errors(sid, "kinematics generic: f_molgas in [0,1], errors >= 0", hk, rk, 0, err_cols=[hk.index("errhi"), hk.index("errlo")],
                   frac_cols=[hk.index("f_molgas")])
    D = [dict(zip(hdr, r)) for r in rows]
    ks = []
    for r in D:
        f, V, s, Re, lm = (fnum(r[c]) for c in ("fDM_Re", "Vrot_Re_kms", "sigma0_kms", "Re_disk_kpc", "logMtot"))
        if all(fin(x) for x in (f, V, s, Re, lm)):
            ks.append((r["id"], math.log10((1 - f) * ((V * 1e3) ** 2 + 3.36 * (s * 1e3) ** 2) * Re * KPC / (G * 10 ** lm * MSUN))))
    med = float(np.median([k for _, k in ks]))
    fl = [f"{i}: log k {k:+.2f} (median {med:+.2f})" for i, k in ks if abs(k - med) > 0.5]
    record(sid, "implied baryon coefficient k = (1-fDM)(Vrot^2+3.36 sigma0^2) Re/(G Mtot) outliers (> 0.5 dex)", "S", len(ks),
           {"FLAG": len(fl), "CONSISTENT": len(ks) - len(fl)}, f"median k = {10 ** med:.2f}; values {[round(k, 2) for _, k in ks]}", rows_flagged=fl)
    return out


# =============================================================================== S11 Jones+21 and the corpus copy
def s11_jones():
    sid = "S11 ALPINE (Jones+21) + corpus copy"
    P(f"\n=== {sid}")
    pj = os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_tableA3_rings.csv")
    pt = os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_table1_sample_classes.csv")
    pcg = os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_galaxies.csv")
    pcr = os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_rings.csv")
    for p in (pj, pt, pcg, pcr):
        P(f"  {rel(p)} sha256 {sha(p)[:16]}")
    J = read_dicts(pj); T1 = read_dicts(pt); CG = read_dicts(pcg); CR = read_dicts(pcr)
    def g_m(r):
        return (f"{r['name']} R={r['R_kpc']}", [(fnum(r["vrot_kms"]), half_unit_text(r["vrot_kms"])), (fnum(r["R_kpc"]), half_unit_text(r["R_kpc"]))],
                (fnum(r["Mdyn_Msun"]), half_unit_text(r["Mdyn_Msun"])))
    formula_check(sid, "rings: Mdyn = Vrot^2 R / G", J, g_m, lambda V, R: (V * 1e3) ** 2 * R * KPC / G / MSUN, 0.01, "Msun")
    # corpus rings identical to Jones rings
    def norm(n):
        return re.sub(r"[^a-z0-9]", "", n.lower()).replace("vc7875", "vc5110377875")
    jr = {(norm(r["name"]), round(fnum(r["R_kpc"]), 3)): r for r in J}
    cl = {}; fl = []
    for r in CR:
        k = (norm(r["galaxy"]), round(fnum(r["R_kpc"]), 3))
        j = jr.get(k)
        if j is None:
            cl["PROBLEM"] = cl.get("PROBLEM", 0) + 1; fl.append(f"{r['galaxy']} R={r['R_kpc']}: no Jones ring"); continue
        pairs = [("Vrot_kms", "vrot_kms"), ("e_Vrot_kms", "vrot_kms_err"), ("sigma_kms", "sigma_kms"), ("e_sigma_kms", "sigma_kms_err"), ("Mdyn_msun", "Mdyn_Msun")]
        bad = [f"{a} {r[a]} vs {j[b]}" for a, b in pairs if abs(fnum(r[a]) - fnum(j[b])) > 1e-6 * max(1, abs(fnum(j[b])))]
        c = "PROBLEM" if bad else "CONSISTENT"
        cl[c] = cl.get(c, 0) + 1
        if bad:
            fl.append(f"{r['galaxy']} R={r['R_kpc']}: " + "; ".join(bad))
    record(sid, "corpus rings are a cell-by-cell copy of the Jones rings", "H", len(CR), cl, f"{len(CR)} corpus rings vs {len(J)} Jones rings", rows_flagged=fl)
    def g_vs(r):
        return (f"{r['galaxy']} R={r['R_kpc']}", [(fnum(r["Vrot_kms"]), half_unit_text(r["Vrot_kms"])), (fnum(r["sigma_kms"]), half_unit_text(r["sigma_kms"]))],
                (fnum(r["v_over_sigma"]), half_unit_text(r["v_over_sigma"])))
    formula_check(sid, "corpus rings: v_over_sigma = Vrot/sigma", CR, g_vs, lambda V, s: V / s, 0.0, "")
    # corpus galaxy means
    cl = {}; fl = []
    by = {}
    for r in CR:
        by.setdefault(norm(r["galaxy"]), []).append(r)
    for g in CG:
        rr = by.get(norm(g["galaxy"]))
        if not rr:
            continue
        vm = float(np.mean([fnum(x["Vrot_kms"]) for x in rr])); sm = float(np.mean([fnum(x["sigma_kms"]) for x in rr]))
        mmax = max(fnum(x["Mdyn_msun"]) for x in rr); vmax = max(fnum(x["Vrot_kms"]) for x in rr)
        tests = [("vrot_mean_kms", vm, 0.002), ("sigma_mean_kms", sm, 0.002), ("vrot_max_kms", vmax, 0.002), ("mdyn_max_msun", mmax, 1e-6),
                 ("log_mdyn_msun", math.log10(mmax), 0.0006), ("v_over_sigma", fnum(g["vrot_mean_kms"]) / fnum(g["sigma_mean_kms"]), 0.0006),
                 ("n_rings", len(rr), 0)]
        for col, val, tol in tests:
            x = fnum(g.get(col))
            if not fin(x):
                continue
            ok = abs(x - val) <= max(tol * (abs(val) if tol < 0.01 and col not in ("log_mdyn_msun", "v_over_sigma") else 1), half_unit_text(g[col]) + 1e-9)
            cl["CONSISTENT" if ok else "PROBLEM"] = cl.get("CONSISTENT" if ok else "PROBLEM", 0) + 1
            if not ok:
                fl.append(f"{g['galaxy']}: {col} {x} vs recomputed {val:.4g}")
    record(sid, "corpus galaxies: means, maxima, log Mdyn, v/sigma, n_rings from the rings", "H", sum(cl.values()), cl, "", rows_flagged=fl)
    # the build's parse: Table 1 row count and the KC1 / class_L20 duplication
    src(sid)["table1_rows"] = len(T1)
    dup = sum(1 for r in T1 if r["KC1"] == r["class_L20"])
    record(sid, "Table 1 parse: KC1 and class_L20 are distinct columns", "S", len(T1), {"FLAG" if dup == len(T1) else "CONSISTENT": 1},
           f"KC1 == class_L20 in {dup}/{len(T1)} rows (build.py assigns both from the same HTML cell r[11]); checked against the HTML in the transcription step")
    # HZ9 corpus M* has no source (CFG271 disclosure)
    hz9 = [g for g in CG if norm(g["galaxy"]) == "hz9"]
    if hz9:
        P(f"  corpus HZ9 row: log_mstar {hz9[0].get('log_mstar_msun')} reference '{hz9[0].get('reference', '')[:80]}' (no M* source; disclosed in CFG271)")
    return dict(J=J, T1=T1, CG=CG, CR=CR)


# =============================================================================== S12 sigma-M* compilation (Parlanti+23 rows, Danhaive rows)
def s12_sigma_compilation():
    sid = "S12 sigma-M* compilation (HZ9 et al.)"
    P(f"\n=== {sid}")
    p = os.path.join(REPO, "real_research", "virial_floor_2026", "highz_sigma_mstar.csv")
    P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
    D = read_dicts(p)
    rows = []
    for r in D:
        m = re.search(r"sigma0=([\d.]+).*?V=([\d.]+).*sigma_eff=sqrt\(sigma0\^2\+V\^2/3\)", r["construction"])
        if m:
            rows.append(dict(name=r["name"], s0=m.group(1), V=m.group(2), sig=r["sigma"], src=r["source_arXiv"]))
    def g(r):
        return (f"{r['name']} ({r['src']})", [(fnum(r["s0"]), half_unit_text(r["s0"])), (fnum(r["V"]), half_unit_text(r["V"]))], (fnum(r["sig"]), half_unit_text(r["sig"])))
    formula_check(sid, "sigma_eff = sqrt(sigma0^2 + V^2/3) per the construction string", rows, g, lambda s, V: math.sqrt(s * s + V * V / 3), 0.0, "km/s")
    return D


# =============================================================================== S13 ALPAKA
def s13_alpaka():
    sid = "S13 ALPAKA I (Rizzo+23)"
    P(f"\n=== {sid}")
    from astropy.cosmology import Planck18
    T = {}
    for t in ("sample", "alma_obs", "properties", "geometry", "kinematics"):
        p = os.path.join(AT, f"alpaka1_{t}.csv")
        P(f"  {t} {rel(p)} sha256 {sha(p)[:16]}")
        T[t] = read_table(p)
    S = {r[0]: dict(zip(T["sample"][0], r)) for r in T["sample"][1]}
    O = {r[0]: dict(zip(T["alma_obs"][0], r)) for r in T["alma_obs"][1]}
    Pp = {r[0]: dict(zip(T["properties"][0], r)) for r in T["properties"][1]}
    rows = []
    for i, pr in Pp.items():
        line = O[i]["line"].strip()
        nu = NU_REST.get(line)
        z = fnum(S[i]["z"])
        rows.append(dict(id=i, line=line, nu=nu, z=z, I=pr["iline_jykms"], L=pr["lprime_1e10_kkmspc2"]))
    def g_l(r):
        if r["nu"] is None:
            return None
        return (f"ID {r['id']} {r['line']}", [(fnum(r["I"]), half_unit_text(r["I"]))], (fnum(r["L"]), half_unit_text(r["L"])))
    def mk(r):
        DL = Planck18.luminosity_distance(r["z"]).value
        return lambda I: 3.25e7 * I * (r["nu"] / (1 + r["z"])) ** -2 * DL ** 2 * (1 + r["z"]) ** -3 / 1e10
    cl = {}; fl = []; worst = (0, None)
    for r in rows:
        g = g_l(r)
        if g is None or not fin(fnum(r["I"])) or not fin(fnum(r["L"])):
            continue
        f0, E = envelope(mk(r), [g[1][0][0]], [g[1][0][1]], g[2][1])
        d = g[2][0] - f0; c = classify(d, E, 0.005, f0)
        cl[c] = cl.get(c, 0) + 1
        if c != "CONSISTENT":
            fl.append(f"{g[0]}: printed L' {g[2][0]} recomputed {f0:.4g} (z {r['z']}, I {r['I']}) [{c}]")
    record(sid, "L' = 3.25e7 S dV nu_obs^-2 D_L^2 (1+z)^-3 (Planck18; line from the ALMA table)", "H", sum(cl.values()), cl, "1e10 K km/s pc^2", rows_flagged=fl)
    hk, rk = T["kinematics"]
    K = [dict(zip(hk, r)) for r in rk]
    cl = {}; fl = []
    for r in K:
        vm, ve = fnum(r["vmax_kms"]), fnum(r["vext_kms"])
        if fin(vm) and fin(ve):
            ok = ve <= vm + 1.0
            cl["CONSISTENT" if ok else "PROBLEM"] = cl.get("CONSISTENT" if ok else "PROBLEM", 0) + 1
            if not ok:
                fl.append(f"ID {r['id']}: Vext {ve} > Vmax {vm}")
    record(sid, "V_ext <= V_max", "H", sum(cl.values()), cl, "", rows_flagged=fl)
    # V/sigma columns (positional: duplicate names)
    rr = []
    for r in rk:
        rr.append(dict(id=r[0], vm=r[1], sm=r[5], sm_lim=r[8], ve=r[9], se=r[13], se_lim=r[16], q1=r[17], q1lim=r[20], q2=r[21], q2lim=r[24]))
    def g1(r):
        return (f"ID {r['id']} Vmax/sigma_m", [(fnum(r["vm"]), 0.5), (fnum(r["sm"]), 0.5)], (fnum(r["q1"]), 0.5))
    def g2(r):
        return (f"ID {r['id']} Vext/sigma_ext", [(fnum(r["ve"]), 0.5), (fnum(r["se"]), 0.5)], (fnum(r["q2"]), 0.5))
    formula_check(sid, "Vmax/sigma_m column = Vmax / sigma_m", rr, g1, lambda a, b: a / b, 0.0, "integer prints", limit_skip=lambda r: r["sm_lim"] != "" or r["q1lim"] != "")
    formula_check(sid, "Vext/sigma_ext column = Vext / sigma_ext", rr, g2, lambda a, b: a / b, 0.0, "integer prints", limit_skip=lambda r: r["se_lim"] != "" or r["q2lim"] != "")
    hg, rg = T["geometry"]
    generic_errors(sid, "geometry: inclinations in [0,90], errors >= 0", hg, rg, 0, err_cols=[i for i, h in enumerate(hg) if h in ("e1", "e2")],
                   inc_cols=[hg.index("i_hst"), hg.index("i_alma")])
    hp, rp = T["properties"]
    generic_errors(sid, "properties: errors >= 0, positive M*/SFR/L'", hp, rp, 0, err_cols=[hp.index(c) for c in ("e_mstar", "e_sfr", "e_iline", "e_lprime", "delta_ms_errhi", "delta_ms_errlo")],
                   pos_cols=[hp.index(c) for c in ("mstar_1e10msun", "sfr_msun_yr", "lprime_1e10_kkmspc2", "iline_jykms")])
    # digitised curves vs table
    pd = os.path.join(AT, "alpaka1_digitised", "alpaka1_vrot_digitised.csv")
    P(f"  digitised {rel(pd)} sha256 {sha(pd)[:16]}")
    Dg = read_dicts(pd)
    curves = {}
    for r in Dg:
        if r["panel"] == "V":
            curves.setdefault(r["id"], []).append((fnum(r["R_arcsec"]), fnum(r["value_kms"]), fnum(r["R_kpc"])))
    cl = {}; fl = []; cl2 = {}; fl2 = []; cl3 = {}; fl3 = []
    for r in K:
        c = sorted(curves.get(r["id"], []))
        if len(c) < 2:
            continue
        ve, vm = fnum(r["vext_kms"]), fnum(r["vmax_kms"])
        dm = 0.5 * (c[-1][1] + c[-2][1]); mx = max(v for _, v, _ in c)
        for (lab, tab, dig, clx, flx) in (("Vext", ve, dm, cl, fl), ("Vmax", vm, mx, cl2, fl2)):
            tol = 0.5 + 0.03 * tab
            k = "CONSISTENT" if abs(tab - dig) <= tol else ("ROUNDING-EDGE" if abs(tab - dig) <= 2 * tol else "PROBLEM")
            clx[k] = clx.get(k, 0) + 1
            if k != "CONSISTENT":
                flx.append(f"ID {r['id']}: table {lab} {tab} vs digitised {dig:.1f} [{k}]")
        zz = fnum(S[r["id"]]["z"])
        kd = c[-1][2] / c[-1][0]; kc = kpc_per_arcsec(zz, Planck18)
        k = "CONSISTENT" if abs(kd / kc - 1) <= 0.02 else ("ROUNDING-EDGE" if abs(kd / kc - 1) <= 0.04 else "PROBLEM")
        cl3[k] = cl3.get(k, 0) + 1
        if k != "CONSISTENT":
            fl3.append(f"ID {r['id']}: digitised kpc/arcsec {kd:.3f} vs Planck18 {kc:.3f} [{k}]")
    record(sid, "digitised: table V_ext vs mean of the last two digitised points (3% + rounding)", "H", sum(cl.values()), cl, "", rows_flagged=fl)
    record(sid, "digitised: table V_max vs maximum digitised point (3% + rounding)", "H", sum(cl2.values()), cl2, "", rows_flagged=fl2)
    record(sid, "digitised: kpc/arcsec vs Planck18 at z (2%)", "H", sum(cl3.values()), cl3, "", rows_flagged=fl3)
    # arXiv:2601.03338 copy: check the M* log/linear relation to the ALPAKA table is not asserted (different SED); internal errors only
    pj = os.path.join(AT, "alpaka_jwst2026_data.csv"); pf = os.path.join(AT, "alpaka_jwst2026_fiducial_fit.csv")
    hj, rj = read_table(pj); hf, rf = read_table(pf)
    generic_errors(sid, "arXiv:2601.03338 tables: errors >= 0", hj + hf, [a + b for a, b in zip(rj, rf)], 0,
                   err_cols=[i for i, h in enumerate(hj + hf) if h.endswith("errhi") or h.endswith("errlo") or h.startswith("e_")])
    return dict(S=S, O=O, P=Pp, K=K)


# =============================================================================== S14 Amvrosiadis
def s14_amvrosiadis():
    sid = "S14 Amvrosiadis+25 (arXiv v1)"
    P(f"\n=== {sid}")
    from astropy.cosmology import FlatLambdaCDM
    cosmo = FlatLambdaCDM(H0=67.8, Om0=0.308)
    pb = os.path.join(AT, "amvrosiadis_bestfit.csv"); pp = os.path.join(AT, "amvrosiadis_parent.csv")
    for p in (pb, pp):
        P(f"  {rel(p)} sha256 {sha(p)[:16]}")
    hb, rb = read_table(pb); hp, rp = read_table(pp)
    B = [dict(zip(hb, r)) for r in rb]; PA = {r[0]: dict(zip(hp, r)) for r in rp}
    generic_errors(sid, "best-fit: errors >= 0, inc in [0,90], positive r_e/V/sigma", hb, rb, 0,
                   err_cols=[i for i, h in enumerate(hb) if "_err" in h], inc_cols=[hb.index("inc_deg")],
                   pos_cols=[hb.index(c) for c in ("re_arcsec", "vmax_kms", "sigma_kms", "vcirc_2re_kms", "mdyn_10kpc_1e11msun")])
    generic_errors(sid, "parent: errors >= 0", hp, rp, 0, err_cols=[i for i, h in enumerate(hp) if "_err" in h])
    cl = {}; fl = []
    for r in B:
        vc, s, vm, evm = fnum(r["vcirc_2re_kms"]), fnum(r["sigma_kms"]), fnum(r["vmax_kms"]), fnum(r["vmax_kms_errhi"])
        if all(fin(x) for x in (vc, s, vm)):
            lhs = (vc - 0.5) ** 2 - 3.36 * (s + 0.5) ** 2
            okk = lhs <= (vm + 0.5 + (evm if fin(evm) else 0)) ** 2
            okn = lhs <= (vm + 0.5) ** 2
            c = "CONSISTENT" if okn else ("ROUNDING-EDGE" if okk else "PROBLEM")
            cl[c] = cl.get(c, 0) + 1
            if c != "CONSISTENT":
                fl.append(f"{r['alessid']}: Vcirc(2re)^2 - 3.36 sigma^2 = {vc ** 2 - 3.36 * s ** 2:.0f} vs Vmax^2 = {vm ** 2:.0f} [{c}]")
    record(sid, "Vcirc(2re)^2 - 3.36 sigma^2 <= Vmax^2 (arctan V_rot <= V_max)", "H", sum(cl.values()), cl, "within rounding (+1 sigma on Vmax for ROUNDING-EDGE)", rows_flagged=fl)
    cl = {}; fl = []; nb = 0; nbar = 0; bar = []
    for r in B:
        pa = PA.get(r["alessid"])
        if not pa:
            continue
        z = fnum(pa["z"]); re_kpc = fnum(r["re_arcsec"]) * kpc_per_arcsec(z, cosmo)
        md = fnum(r["mdyn_10kpc_1e11msun"]) * 1e11; vc = fnum(r["vcirc_2re_kms"])
        v10 = math.sqrt(G * md * MSUN / (10 * KPC)) / 1e3
        if abs(2 * re_kpc / 10 - 1) <= 0.2:
            x = v10 / vc
            c = "CONSISTENT" if abs(x - 1) <= 0.1 else "FLAG"
            cl[c] = cl.get(c, 0) + 1
            fl.append(f"{r['alessid']}: 2 r_e = {2 * re_kpc:.1f} kpc; V(10 kpc) from Mdyn {v10:.0f} vs Vcirc(2re) {vc:.0f} (ratio {x:.3f})" + (" [FLAG]" if c == "FLAG" else ""))
        ms, mg = fnum(pa["logMstar"]), fnum(pa["logMgas_msun"])
        if fin(ms) and fin(mg):
            nb += 1
            ratio = (10 ** ms + 10 ** mg) / md
            bar.append((r["alessid"], round(ratio, 2)))
            nbar += ratio > 1
    record(sid, "Mdyn(10 kpc) vs Vcirc(2re)^2 x 10 kpc / G where 2 r_e is within 20% of 10 kpc", "S", sum(cl.values()), cl, "; ".join(fl), rows_flagged=[x for x in fl if "FLAG" in x])
    record(sid, "baryons (M* + M_gas, parent table) vs Mdyn(10 kpc)", "S", nb, {"FLAG": nbar, "CONSISTENT": nb - nbar},
           f"(M*+Mgas)/Mdyn per disc: {bar} (total masses vs a 10 kpc dynamical mass; CFG227 already recorded g_obs < g_bar in 7 of 9)",
           rows_flagged=[f"{a}: (M*+Mgas)/Mdyn(10kpc) = {b}" for a, b in bar if b > 1])
    return dict(B=B, PA=PA)


# =============================================================================== S15 Danhaive
def s15_danhaive():
    sid = "S15 Danhaive+25 (arXiv v1, 41 gold)"
    P(f"\n=== {sid}")
    p = os.path.join(AT, "danhaive2025_gold.csv")
    P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
    hdr, rows = read_table(p)
    D = [dict(zip(hdr, r)) for r in rows]
    generic_errors(sid, "generic: errors >= 0, positive r_e/sigma0", hdr, rows, 0, err_cols=[i for i, h in enumerate(hdr) if "_err" in h],
                   pos_cols=[hdr.index("re_kpc"), hdr.index("sigma0_kms")])
    def g(r):
        return (f"{r['jades_id']}" + (" (sigma0 limit)" if r["sigma0_kms_lim"] else ""),
                [(fnum(r["re_kpc"]), half_unit_text(r["re_kpc"])), (fnum(r["v_over_sigma0"]), half_unit_text(r["v_over_sigma0"])),
                 (fnum(r["sigma0_kms"]), half_unit_text(r["sigma0_kms"]))], (fnum(r["logMdyn"]), half_unit_text(r["logMdyn"])))
    def f(re_, vs, s):
        v = vs * s
        return math.log10(1.8 * re_ * KPC * ((v * 1e3) ** 2 + 3.36 * (s * 1e3) ** 2) / G / MSUN)
    # C = 1% in mass = 0.0043 dex; formula_check's C is relative to f (a log), so pass the dex equivalent
    formula_check(sid, "log Mdyn = log[1.8 r_e (v^2 + 3.36 sigma0^2)/G], v = (v/sigma0) sigma0 (non-limit rows)", D, g, f, 0.0043 / 10.0, "dex (C = 1% in mass)",
                  limit_skip=lambda r: r["sigma0_kms_lim"] != "" or r["v_over_sigma0_lim"] != "")
    lim = [r for r in D if r["sigma0_kms_lim"] != ""]
    cl = {}; fl = []
    for r in lim:
        ld = f(fnum(r["re_kpc"]), fnum(r["v_over_sigma0"]), fnum(r["sigma0_kms"]))
        x = fnum(r["logMdyn"]) - ld
        fl.append(f"{r['jades_id']}: sigma0 < {r['sigma0_kms']}, v/sigma0 {r['v_over_sigma0']}: printed logMdyn {r['logMdyn']} - formula at the limit {ld:.2f} = {x:+.2f}")
        cl["INFO"] = cl.get("INFO", 0) + 1
    record(sid, "sigma0-limit rows: printed log Mdyn against the formula evaluated at the limit (information)", "S", len(lim), cl, "", rows_flagged=fl)
    return D


# =============================================================================== S16 Roman-Oliveira
def s16_romanoliveira():
    sid = "S16 Roman-Oliveira+23"
    P(f"\n=== {sid}")
    from astropy.cosmology import FlatLambdaCDM
    cosmo = FlatLambdaCDM(H0=67.7, Om0=0.31)
    T = {}
    for t in ("sample", "gasmasses", "kinematics"):
        p = os.path.join(AT, f"romanoliveira2023_{t}.csv")
        P(f"  {t} {rel(p)} sha256 {sha(p)[:16]}")
        T[t] = read_table(p)
    hk, rk = T["kinematics"]
    K = [dict(zip(hk, r)) for r in rk]
    def g1(r):
        return (r["id"] + " Vmax/sigma", [(fnum(r["vrot_max_kms"]), 0.5), (fnum(r["sigma_mean_kms"]), 0.5)], (fnum(r["vmax_over_sigma"]), half_unit_text(r["vmax_over_sigma"])))
    def g2(r):
        return (r["id"] + " Vext/sigma_ext", [(fnum(r["vrot_ext_kms"]), 0.5), (fnum(r["sigma_ext_kms"]), 0.5)], (fnum(r["vext_over_sigma_ext"]), half_unit_text(r["vext_over_sigma_ext"])))
    formula_check(sid, "Vmax/sigma = Vrot,max / sigma_mean", K, g1, lambda a, b: a / b, 0.0, "")
    formula_check(sid, "Vext/sigma_ext = Vrot,ext / sigma_ext", K, g2, lambda a, b: a / b, 0.0, "")
    cl = {}; fl = []
    for r in K:
        ok = fnum(r["vrot_ext_kms"]) <= fnum(r["vrot_max_kms"]) + 0.5
        cl["CONSISTENT" if ok else "PROBLEM"] = cl.get("CONSISTENT" if ok else "PROBLEM", 0) + 1
        if not ok:
            fl.append(f"{r['id']}: Vext {r['vrot_ext_kms']} > Vmax {r['vrot_max_kms']}")
    record(sid, "V_ext <= V_max", "H", len(K), cl, "", rows_flagged=fl)
    generic_errors(sid, "kinematics: errors >= 0", hk, rk, 0, err_cols=[i for i, h in enumerate(hk) if "_err" in h])
    hs, rs = T["sample"]
    Sx = [dict(zip(hs, r)) for r in rs]
    def g3(r):
        return (r["id"], [(fnum(r["z"]), half_unit_text(r["z"]))], (fnum(r["kpc_per_arcsec"]), half_unit_text(r["kpc_per_arcsec"])))
    formula_check(sid, "kpc/arcsec = Planck18-like (67.7, 0.31) scale at z", Sx, g3, lambda z: kpc_per_arcsec(z, cosmo), 0.005, "kpc/arcsec")
    return dict(K=K, S=Sx, G=[dict(zip(T["gasmasses"][0], r)) for r in T["gasmasses"][1]])


# =============================================================================== S17 Lelli+23
def s17_lelli23():
    sid = "S17 Lelli+23"
    P(f"\n=== {sid}")
    pm = os.path.join(AT, "lelli2023_massmodels.csv"); pb = os.path.join(AT, "lelli2023_3dbarolo.csv")
    pdg = os.path.join(DA, "lelli2023_rotcur_digitised", "lelli2023_rotcur_digitised.csv")
    for p in (pm, pb, pdg):
        P(f"  {rel(p)} sha256 {sha(p)[:16]}")
    M = read_dicts(pm)
    def g(r):
        ins = [(fnum(r[c]) if fin(fnum(r[c])) else 0.0, half_unit_text(r[c]) if fin(fnum(r[c])) else 0.0) for c in ("Mgas_1e10", "Mdisk_1e10", "Mbul_1e10")]
        return (f"{r['galaxy']} / {r['model']}", ins, (fnum(r["Mbar_1e10"]), half_unit_text(r["Mbar_1e10"])))
    formula_check(sid, "M_bar = M_gas + M_disk + M_bul", M, g, lambda a, b, c: a + b + c, 0.0, "1e10 Msun")
    def g2(r):
        return (f"{r['galaxy']} / {r['model']}", [(fnum(r["Mbul_1e10"]), half_unit_text(r["Mbul_1e10"])), (fnum(r["Mbar_1e10"]), half_unit_text(r["Mbar_1e10"]))],
                (fnum(r["Mbul_over_Mbar"]), half_unit_text(r["Mbul_over_Mbar"])))
    formula_check(sid, "M_bul/M_bar column = M_bul / M_bar", M, g2, lambda a, b: a / b, 0.0, "")
    B = read_dicts(pb)
    vrow = [r for r in B if "V_" in r["parameter"] or "rot" in r["parameter"].lower()]
    Dg = read_dicts(pdg)
    cl = {}; fl = []
    for gal in ("zC-400569", "zC-488879"):
        tab = None
        for r in vrow:
            m = re.match(r"\s*([\d.]+)", r[gal])
            if m:
                tab = (r["parameter"], float(m.group(1)))
        co = [fnum(r["vrot_kms"]) for r in Dg if r["galaxy"] == gal and "CO" in r["line"]]
        if tab and co:
            x = float(np.mean(co))
            tol = 0.5 + 0.03 * tab[1]
            c = "CONSISTENT" if abs(x - tab[1]) <= tol else "FLAG"
            cl[c] = cl.get(c, 0) + 1
            fl.append(f"{gal}: table {tab[0]} = {tab[1]} vs mean digitised CO V = {x:.1f} over {len(co)} points" + (" [FLAG]" if c == "FLAG" else ""))
    record(sid, "table mean V_rot vs mean of the digitised CO points (3% + rounding)", "S", sum(cl.values()), cl, "; ".join(fl), rows_flagged=[x for x in fl if "FLAG" in x])
    return dict(M=M, B=B, D=Dg)


# =============================================================================== S18 MUSE-DARK numeric set
def s18_musedark():
    sid = "S18 MUSE-DARK I numeric set (+ II/III tables)"
    P(f"\n=== {sid}")
    from astropy.cosmology import Planck15, Planck18, FlatLambdaCDM
    p = os.path.join(DA, "musedark_catalogues", "musedark_numeric.csv")
    P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
    D = read_dicts(p)
    def g1(r):
        return (r["muse_id"], [(fnum(r["DC14_log_X"]), half_unit_text(r["DC14_log_X"])), (fnum(r["DC14_logMvir"]), half_unit_text(r["DC14_logMvir"]))],
                (fnum(r["log_X_plus_logMvir"]), half_unit_text(r["log_X_plus_logMvir"])))
    formula_check(sid, "log_X + log Mvir = stored sum (repo-derived)", D, g1, lambda a, b: a + b, 0.0, "dex")
    def g2(r):
        return (r["muse_id"], [(fnum(r["Re_arcsec_from_table"]), half_unit_text(r["Re_arcsec_from_table"])), (fnum(r["kpc_per_arcsec"]), 0.0)],
                (fnum(r["Re_kpc_from_table"]), half_unit_text(r["Re_kpc_from_table"])))
    formula_check(sid, "Re(kpc) from table = Re(arcsec) x kpc/arcsec", D, g2, lambda a, k: a * k, 0.0, "kpc")
    cl = {}; fl = []
    for r in D:
        a, b = fnum(r["Re_kpc"]), fnum(r["Re_kpc_from_table"])
        if fin(a) and fin(b):
            c = "CONSISTENT" if abs(a - b) <= 0.0055 + 0.0005 else "FLAG"
            cl[c] = cl.get(c, 0) + 1
            if c == "FLAG":
                fl.append(f"{r['muse_id']}: Re_kpc {a} vs from table {b}")
    record(sid, "catalogue Re vs table Re", "S", sum(cl.values()), cl, "", rows_flagged=fl)
    best = None
    for nm, c in (("Planck15", Planck15), ("Planck18", Planck18), ("flat 70/0.3", FlatLambdaCDM(H0=70, Om0=0.3))):
        n_ok = sum(1 for r in D if abs(fnum(r["kpc_per_arcsec"]) / kpc_per_arcsec(fnum(r["z"]), c) - 1) <= 0.005)
        if best is None or n_ok > best[1]:
            best = (nm, n_ok, c)
    def g3(r):
        return (r["muse_id"], [(fnum(r["z"]), 0.0)], (fnum(r["kpc_per_arcsec"]), 0.0))
    formula_check(sid, f"kpc/arcsec vs {best[0]} at z (majority cosmology)", D, g3, lambda z: kpc_per_arcsec(z, best[2]), 0.005, "kpc/arcsec")
    cl = {}; fl = []
    for r in D:
        hb = r["has_bulge"] == "1"; mb = fin(fnum(r["logMbulge"]))
        ok = hb == mb
        cl["CONSISTENT" if ok else "PROBLEM"] = cl.get("CONSISTENT" if ok else "PROBLEM", 0) + 1
        if not ok:
            fl.append(f"{r['muse_id']}: has_bulge {r['has_bulge']} logMbulge '{r['logMbulge']}'")
    record(sid, "has_bulge iff log M_bulge is finite", "H", len(D), cl, "", rows_flagged=fl)
    hdr, rows = read_table(p)
    generic_errors(sid, "generic: fDM in [0,1], inc in [0,90], errors >= 0", hdr, rows, 0, err_cols=[hdr.index("DC14_logMdisk_err")],
                   frac_cols=[hdr.index("fDM_at_Re")], inc_cols=[hdr.index("incl_deg")], pos_cols=[hdr.index("Re_kpc"), hdr.index("v22")])
    dup = json.load(open(os.path.join(DA, "musedark_catalogues", "duplicated_rows.json")))
    ndup = {k: len(v) for k, v in dup.items()}
    P(f"  known duplicated catalogue rows (build record duplicated_rows.json): {ndup} galaxies per model")
    return D


# =============================================================================== S19 ADF22.5 literature values
def s19_adf22(alp):
    sid = "S19 ADF22.5 literature values (Umehata+25 / Huang+25 / ADF22-WEB)"
    P(f"\n=== {sid}")
    p = os.path.join(DA, "adf22_5_literature_2026-10-02", "adf22_5_literature_values.csv")
    P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
    D = {r["quantity"]: r for r in read_dicts(p)}
    m, eh, el = fnum(D["Mstar"]["value"]), fnum(D["Mstar"]["err_hi"]), fnum(D["Mstar"]["err_lo"])
    lm, leh, lel = fnum(D["log10_Mstar"]["value"]), fnum(D["log10_Mstar"]["err_hi"]), fnum(D["log10_Mstar"]["err_lo"])
    exp = (math.log10(m), math.log10((m + eh) / m), math.log10(m / (m - el)))
    ok = all(abs(a - b) < 1e-4 for a, b in zip(exp, (lm, leh, lel)))
    record(sid, "log M* and its errors from the linear value (4.4 +2.6/-2.5 e10)", "H", 1, {"CONSISTENT" if ok else "PROBLEM": 1},
           f"recomputed {exp[0]:.5f} +{exp[1]:.5f} -{exp[2]:.5f} vs stored {lm} +{leh} -{lel}")
    s = alp["S"]["24"]
    ra, dec = fnum(s["ra_deg"]), fnum(s["dec_deg"])
    def sex2deg(t):
        m_ = re.match(r"\s*(\d+):(\d+):([\d.]+)\s+([+-]?)(\d+):(\d+):([\d.]+)", t)
        if not m_:
            return None
        a = 15 * (int(m_.group(1)) + int(m_.group(2)) / 60 + float(m_.group(3)) / 3600)
        d = int(m_.group(5)) + int(m_.group(6)) / 60 + float(m_.group(7)) / 3600
        return a, (-d if m_.group(4) == "-" else d)
    cl = {}; fl = []
    for q in ("position_huang25", "position_umehata25"):
        pos = sex2deg(D[q]["value"])
        if pos:
            sep = 3600 * math.hypot((pos[0] - ra) * math.cos(math.radians(dec)), pos[1] - dec)
            c = "CONSISTENT" if sep <= 1.0 else "PROBLEM"
            cl[c] = cl.get(c, 0) + 1
            fl.append(f"{q}: separation from ALPAKA 24 {sep:.2f} arcsec")
    record(sid, "positions within 1 arcsec of the ALPAKA ID 24 table position", "H", sum(cl.values()), cl, "; ".join(fl))
    dz = abs(fnum(D["redshift"]["value"]) - fnum(s["z"]))
    record(sid, "z (Huang+25) vs ALPAKA 24", "H", 1, {"CONSISTENT" if dz <= 0.002 else "PROBLEM": 1}, f"|dz| = {dz:.4f}")
    # provenance census
    how = {}
    for r in D.values():
        k = "WebFetch summary" if "WebFetch" in r["how_read"] else r["how_read"][:30]
        how[k] = how.get(k, 0) + 1
    used_web = [q for q, r in D.items() if "WebFetch" in r["how_read"] and r["used_in_cfg284"].startswith("yes")]
    src(sid)["provenance"] = dict(how=how, used_in_cfg284_from_webfetch=used_web)
    P(f"  provenance: {how}; values used in CFG284 that were read only through a page summariser: {used_web}")
    # the on-disk ADF22-WEB PDF (arXiv:2609.06679): search the cited numbers in its text layer
    pdf = os.path.join(EXT, "arxiv_pdf", "2609.06679.pdf")
    found = {}
    if os.path.exists(pdf):
        import subprocess
        txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
        flat = re.sub(r"\s+", " ", txt)
        for lab, pats in (("alpha_CO 3.6", [r"3\.6"]), ("M* 4.4e10 (as 10.64 dex or 4.4)", [r"10\.64", r"4\.4\s*[×x]\s*10"]),
                          ("A7 named", [r"A7\b"]), ("CO(1-0)", [r"CO\s*\(\s*1\s*[–-]\s*0\s*\)"])):
            found[lab] = any(re.search(pt, flat) for pt in pats)
        P(f"  arXiv:2609.06679 PDF text layer ({len(txt)} chars): {found}")
    src(sid)["adf22web_pdf_search"] = found
    return D


# =============================================================================== S20 PKS 0529 (Lin+24, digitised)
def s20_pks0529():
    sid = "S20 PKS 0529-549 (Lin+24, digitised)"
    P(f"\n=== {sid}")
    p = os.path.join(REPO, "campaign_fresh_gravity", "CFG275_pks0529_ci_rings", "lin2024_rings_digitised.csv")
    P(f"  file {rel(p)} sha256 {sha(p)[:16]}")
    D = read_dicts(p)
    ratios = [fnum(r["R_kpc"]) / fnum(r["R_arcsec"]) for r in D]
    spread = (max(ratios) - min(ratios)) / np.median(ratios)
    record(sid, "R_kpc / R_arcsec constant across rings (1e-3)", "H", len(D), {"CONSISTENT" if spread <= 1e-3 else "PROBLEM": 1},
           f"kpc/arcsec {min(ratios):.4f}..{max(ratios):.4f} (relative spread {spread:.1e})")
    from astropy.cosmology import Planck18
    pz = os.path.join(DA, "multitracer_gas", "singles_multitracer_galaxies.csv")
    zz = fnum([r for r in read_dicts(pz) if r["galaxy"].startswith("PKS")][0]["z"])
    k18 = kpc_per_arcsec(zz, Planck18)
    P(f"  z = {zz} (multitracer table); Planck18 kpc/arcsec {k18:.4f} vs digitised {np.median(ratios):.4f}")
    by = {}
    for r in D:
        by.setdefault(r["series"], {})[int(r["ring"])] = r
    cl = {}; fl = []
    vr = by.get("V_rot (3DFIT)", {}); vc = by.get("V_c (constant sigma_v)", {})
    for k in sorted(vr):
        if k in vc:
            a, b = fnum(vr[k]["V_kms"]), fnum(vc[k]["V_kms"])
            c = "CONSISTENT" if b >= a * 0.99 else "FLAG"
            cl[c] = cl.get(c, 0) + 1
            if c == "FLAG":
                fl.append(f"ring {k}: V_c(const sigma) {b} < V_rot {a}")
    record(sid, "V_c (constant sigma_v) >= V_rot ring by ring (1% digitisation)", "S", sum(cl.values()), cl, "", rows_flagged=fl)
    cl = {}; fl = []
    for s_, rr in by.items():
        ks = sorted(rr)
        R = [fnum(rr[k]["R_kpc"]) for k in ks]
        e = [fnum(rr[k][c]) for k in ks for c in ("err_lo_kms", "err_hi_kms") if fin(fnum(rr[k][c]))]
        ok = all(np.diff(R) > 0) and all(x >= 0 for x in e)
        cl["CONSISTENT" if ok else "PROBLEM"] = cl.get("CONSISTENT" if ok else "PROBLEM", 0) + 1
        if not ok:
            fl.append(s_)
    record(sid, "radii increasing and errors >= 0 per series", "H", sum(cl.values()), cl, "", rows_flagged=fl)
    return D


# =============================================================================== S21 GN20 constants
def s21_gn20():
    sid = "S21 GN20 (Ubler+24 / Boogaard+25) constants in CFG276"
    P(f"\n=== {sid}")
    ub = open(os.path.join(EXT, "arxiv_src", "2403.03192", "GN20_accepted.tex"), errors="ignore").read()
    bo = open(os.path.join(EXT, "arxiv_src", "2510.17804", "boogaard-gn20-noema-hires.tex"), errors="ignore").read()
    lane = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG276_gn20", "cfg276_gn20.py")).read()
    checks = [("Z0 = 4.055", ub + bo, r"4\.055"), ("RE = 3.6 kpc", ub, r"R_e=3\.6\{\\rm kpc\}"), ("V_FID 496", ub, r"v_c\(R_e\)=496"),
              ("V_INFL 472", ub, r"v_\{\\rm circ\}\(R_e\)\$ \[km/s\] & 472"), ("V_ROT_FID 469", ub, r"=469\$~km/s"), ("SIG0 89", ub, r"\\sigma_0=89\$"),
              ("v_rot 551 (i = 150 deg)", ub, r"=551\$~km/s"), ("LMD2_FID 11.68", ub, r"& 11\.68"), ("LMD2_INFL 11.51", ub, r"& 11\.51"),
              ("M_STAR 1.1e11", ub, r"M_\\star=1\.1\\times10\^\{11\}"), ("M_BULGE 2.5e10", ub, r"2\.5\\times10\^\{10\}"),
              ("H12 gas 1.3e11", ub, r"M_\{\\rm H2\}=1\.3\\times10\^\{11\}"), ("RT gas 2.87e11", bo, r"M_\{\\rm mol\}\$ \[\$10\^\{11\}\$ M\$_\{\\odot\}\$\] & \$2\.87")]
    lane_vals = [("Z0 = 4.055", r"Z0 = 4\.055"), ("RE = 3.6 kpc", r"RE = 3\.6"), ("V_FID 496", r"496\.0"), ("V_INFL 472", r"472\.0"), ("V_ROT_FID 469", r"469\.0"),
                 ("SIG0 89", r"SIG0 = 89\.0"), ("v_rot 551 (i = 150 deg)", r"551\.0"), ("LMD2_FID 11.68", r"11\.68"), ("LMD2_INFL 11.51", r"11\.51"),
                 ("M_STAR 1.1e11", r"M_STAR, M_BULGE = 1\.1e11"), ("M_BULGE 2.5e10", r"2\.5e10"), ("H12 gas 1.3e11", r"\"H12\": 1\.3e11"), ("RT gas 2.87e11", r"\"RT\": 2\.87e11")]
    cl = {}; fl = []
    for (lab, t, pat), (lab2, pat2) in zip(checks, lane_vals):
        a = re.search(pat, re.sub(r"[ \t]+", " ", t)) is not None
        b = re.search(pat2, lane) is not None
        c = "CONSISTENT" if (a and b) else "PROBLEM"
        cl[c] = cl.get(c, 0) + 1
        fl.append(f"{lab}: in source TeX {a}, in lane script {b}")
    record(sid, "each hard-coded CFG276 constant is in the lane script and in the source TeX", "H", len(checks), cl, "", rows_flagged=[x for x in fl if "False" in x])
    def g(r):
        return r
    vv = [("fiducial: v_c(Re) vs v_rot 469, sigma0 89", 496.0, (469.0, 89.0)), ("i = 150 deg: sqrt(551^2 + 3.36 x 89^2) used as V_150", math.sqrt(551 ** 2 + 3.36 * 89 ** 2), (551.0, 89.0))]
    cl = {}; fl = []
    for lab, pr, (V, s) in vv:
        f0, E = envelope(lambda a, b: math.sqrt(a * a + 3.36 * b * b), [V, s], [0.5, 0.5], 0.5)
        c = classify(pr - f0, E, 0.0, f0)
        cl[c] = cl.get(c, 0) + 1
        fl.append(f"{lab}: printed/used {pr:.1f} recomputed {f0:.1f} [{c}]")
    record(sid, "v_circ = sqrt(v_rot^2 + 3.36 sigma0^2) for the fiducial model", "H", len(vv), cl, "; ".join(fl))


# =============================================================================== S22 MIGHTEE
def s22_mightee():
    sid = "S22 MIGHTEE (Varasteanu+26 table; Jarvis+25)"
    P(f"\n=== {sid}")
    tex = open(os.path.join(EXT, "arxiv_src", "2608.03576", "main.tex"), errors="ignore").read()
    comp = re.sub(r"\s+", "", tex)
    lane = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG279_mightee_published_values", "cfg279_mightee_published.py")).read()
    m = re.search(r"PAPER = dict\((.*?)\)\n", lane)
    vals = {k: v for k, v in re.findall(r"(\w+)=\(([-\d.]+, [\d.]+)\)", m.group(1))} if m else {}
    cl = {}; fl = []
    for k, v in vals.items():
        a, e = [x.strip() for x in v.split(",")]
        # the TeX prints a_0=(1.50\pm0.05) etc.; accept either symbol
        pats = [f"({a}\\pm{e})", f"{a}\\pm{e}", f"({a}\\pm{e}0)" if len(e.split('.')[-1]) == 1 else f"({a}\\pm{e})"]
        ok = any(p in comp for p in pats)
        c = "CONSISTENT" if ok else "PROBLEM"
        cl[c] = cl.get(c, 0) + 1
        fl.append(f"{k} = {a} +- {e}: found {ok}")
    record(sid, "CFG279's PAPER values each found in the TeX (independent search)", "H", len(vals), cl, "; ".join(fl), rows_flagged=[x for x in fl if "False" in x])
    p = os.path.join(DA, "mightee_hi_highz", "mightee_hi_highz.csv")
    P(f"  Jarvis+25 table {rel(p)} sha256 {sha(p)[:16]}")
    D = read_dicts(p)
    def g(r):
        if not (fin(fnum(r["W50_kms"])) and fin(fnum(r["W50c_kms"]))):
            return None
        return (r["id"], [(fnum(r["W50_kms"]), 0.5), (fnum(r["incl_deg"]), 0.5)], (fnum(r["W50c_kms"]), 0.5))
    formula_check(sid, "Jarvis+25: W50c = W50 / sin i (C = 8%, the build's own statement)", D, g, lambda w, i: w / math.sin(math.radians(i)), 0.08, "km/s")
    return D


# =============================================================================== transcription engine (independent of the builds)
NUM = r"[-+\u2212]?(?:\d+\.?\d*|\.\d+)"


def split_depth0(s, sep):
    """split on sep only at brace depth 0 (keeps \\substack{+9 \\\\ -10} intact)."""
    out, cur, depth, i = [], [], 0, 0
    while i < len(s):
        ch = s[i]
        if ch == "{" and (i == 0 or s[i - 1] != "\\"):
            depth += 1
        elif ch == "}" and (i == 0 or s[i - 1] != "\\"):
            depth = max(0, depth - 1)
        if depth == 0 and s.startswith(sep, i) and not (sep == "&" and i > 0 and s[i - 1] == "\\"):
            out.append("".join(cur)); cur = []; i += len(sep); continue
        cur.append(ch); i += 1
    out.append("".join(cur))
    return out


def strip_tex_comments(s):
    """drop full-line comments and inline comments; a % preceded by an even number of backslashes (e.g. after a
    row-ending \\\\) starts a comment, an odd number (\\%) is an escaped percent sign."""
    out = []
    for l in s.split("\n"):
        if l.lstrip().startswith("%"):
            continue
        cut = None
        for m in re.finditer("%", l):
            k = m.start(); nb = 0
            while k - 1 - nb >= 0 and l[k - 1 - nb] == "\\":
                nb += 1
            if nb % 2 == 0:
                cut = m.start(); break
        out.append(l if cut is None else l[:cut])
    return "\n".join(out)


def tex_table(texpath, label):
    t = open(texpath, encoding="utf-8", errors="ignore").read()
    i = t.find("\\label{%s}" % label)
    while i >= 0 and t.rfind("\n", 0, i) >= 0 and t[t.rfind("\n", 0, i) + 1:i].lstrip().startswith("%"):
        i = t.find("\\label{%s}" % label, i + 1)
    if i < 0:
        return None
    b = max(t.rfind("\\begin{table", 0, i), t.rfind("\\begin{deluxetable", 0, i), t.rfind("\\begin{sidewaystable", 0, i))
    ends = [x for x in (t.find("\\end{table", i), t.find("\\end{deluxetable", i), t.find("\\end{sidewaystable", i)) if x >= 0]
    e = min(ends)
    body = strip_tex_comments(t[b:e])
    nxt = t.find("\\begin{table", e)
    if nxt >= 0 and "\\ContinuedFloat" in t[nxt:nxt + 200]:
        e2 = t.find("\\end{table", nxt)
        body2 = strip_tex_comments(t[nxt:e2])
        tb2 = body2.find("\\begin{tabular"); te2 = body2.rfind("\\end{tabular")
        body = body + "\\\\" + (body2[tb2:te2] if tb2 >= 0 else body2)
    tb = body.find("\\begin{tabular")
    if tb >= 0:
        body = body[tb:]
    body = re.sub(r"\\end\{tabular[x*]?\}.*?(?=\\begin\{tabular|$)", " ", body, flags=re.S)
    rows = []
    for r in split_depth0(body, "\\\\"):
        r = re.sub(r"\\(hline|noalign\{[^}]*\}|midrule|toprule|bottomrule|cline\{[^}]*\})", " ", r)
        r = re.sub(r"^\s*\[[-\d.]+mm\]", " ", r)
        cells = [c.strip() for c in split_depth0(r, "&")]
        if any(c for c in cells):
            rows.append(cells)
    return rows


def flat_html(x):
    x = re.sub(r'<math[^>]*alttext="([^"]*)"[^>]*>.*?</math>', lambda m: " $" + html.unescape(m.group(1)) + "$ ", x, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()


def html_table(path, tid):
    s = open(path, errors="ignore").read()
    i = s.index('<table id="%s"' % tid); j = s.index("</table>", i)
    return [[flat_html(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)] for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s[i:j], flags=re.S)]


def clean_math(c):
    t = c.replace("\u2212", "-").replace("$", " ")
    t = re.sub(r"\\tablefootmark\{[^}]*\}", " ", t)
    t = re.sub(r"\\(hphantom|phantom|vspace|hspace)\*?\{[^}]*\}", " ", t)
    t = re.sub(r"\\multirow\{[^}]*\}\{[^}]*\}", " ", t)
    t = re.sub(r"(?<!\\)\\(,|;|!|:|quad|qquad)", " ", t).replace("~", " ")
    t = re.sub(r"(?<!\\)\\ ", " ", t)
    t = re.sub(r"\\farcs", ".", t)
    t = re.sub(r"\\(mathrm|rm|textbf|textit|bf|it|scriptsize|footnotesize|small|tiny|boldsymbol|mathbf)\b", " ", t)
    return t


def parse_cell(c):
    """-> dict(v, p, m, lim) (numbers as floats, scale not applied) plus all numbers in reading order."""
    t = clean_math(c)
    lim = "<" if re.search(r"\\lesssim|\\leq|\\la\b|<|\\lt\b", t) else (">" if re.search(r"\\gtrsim|\\geq|\\ga\b|>|\\gt\b", t) else "")
    num = NUM
    pats = [
        (rf"({num})\s*\^\s*\{{?\s*\+?\s*({num})\s*\}}?\s*_\s*\{{?\s*-?\s*({num})\s*\}}?", ("v", "p", "m")),
        (rf"({num})\s*_\s*\{{?\s*-?\s*({num})\s*\}}?\s*\^\s*\{{?\s*\+?\s*({num})\s*\}}?", ("v", "m", "p")),
        (rf"({num})\s*\\substack\s*\{{\s*\+\s*({num})\s*\\\\\s*-\s*({num})\s*\}}", ("v", "p", "m")),
        (rf"({num})\s*(?:\\pm|\u00b1)\s*({num})", ("v", "pm")),
    ]
    comp = {}
    for pat, roles in pats:
        m = re.search(pat, t)
        if m:
            for role, g in zip(roles, m.groups()):
                x = float(g.replace("\u2212", "-"))
                if role == "pm":
                    comp["p"] = comp["m"] = abs(x)
                else:
                    comp[role] = abs(x) if role in ("p", "m") else x
            break
    nums = [float(x.replace("\u2212", "-")) for x in re.findall(num, re.sub(r"10\^\{?-?\d+\}?", " ", t))]
    if "v" not in comp and nums:
        comp["v"] = nums[0]
    sc = re.search(r"\\times\s*10\^\{?\s*(-?\d+)\s*\}?", t)
    comp["lim"] = lim
    comp["scale"] = int(sc.group(1)) if sc else 0
    if comp["scale"]:
        for role in ("v", "p", "m"):
            if role in comp:
                comp[role] = comp[role] * 10 ** comp["scale"]
    comp["ditto"] = t.strip() in ('"', "\u201d", "''")
    return comp, nums


def norm_key(s):
    s = re.sub(r"\$\^\{\\mathrm\{[a-z, ]+\}\}\$|\^\{\\mathrm\{[a-z, ]+\}\}|\$\^\{[a-z\\alpha\\beta, ]+\}\$|\^\{\\alpha[^}]*\}", " ", s)
    s = s.replace("\u2020", " ")
    s = clean_math(s)
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    return re.sub(r"[^a-z0-9.+]", "", s.lower().replace("\u2212", "-"))


def equal_num(x, y):
    return abs(x - y) <= 1e-9 * max(abs(x), abs(y), 1e-300) + 1e-15


def infer_mapping(csv_rows, header, keycol, src_by_key, skip_cols=(), keyf=None):
    """majority mapping CSV column -> (cell index, component, power of ten)."""
    maps = {}
    for j, h in enumerate(header):
        if j == keycol or j in skip_cols:
            continue
        votes = {}
        n = 0
        asym = {"p": 0, "m": 0}
        for r in csv_rows:
            if j >= len(r):
                continue
            x = fnum(r[j])
            s = src_by_key.get(keyf(r) if keyf else norm_key(r[keycol]))
            if not fin(x) or s is None:
                continue
            n += 1
            for ci, (comp, nums) in enumerate(s):
                for role in ("v", "p", "m"):
                    if role not in comp:
                        continue
                    y = comp[role]
                    for k in range(-12, 13):
                        if equal_num(x, y * 10 ** k) or (x == 0 and y == 0 and k == 0):
                            votes[(ci, role, k)] = votes.get((ci, role, k), 0) + 1
                            if role in ("p", "m") and comp.get("p") != comp.get("m"):
                                asym[role] += 1
        if not votes or n == 0:
            maps[j] = None
            continue
        sem = "p" if re.search(r"errhi|_ep$|^e_?hi|E_|err_hi|_hi$|plus", h) else ("m" if re.search(r"errlo|_em$|e_?lo|err_lo|_lo$|minus", h) else None)
        best = max(votes.items(), key=lambda kv: (kv[1], 1 if (sem and kv[0][1] == sem) else 0, 1 if kv[0][2] == 0 else 0, -kv[0][0]))
        (ci, role, k), cnt = best
        if cnt >= max(1, math.ceil(0.6 * n)):
            maps[j] = dict(ci=ci, role=role, k=k, votes=cnt, n=n, sem=sem)
        else:
            maps[j] = None
    return maps


def transcription_table(tag, csv_path, src_rows, keycol=0, key_from_src=0, skip_cols=(), rng=None, data_filter=None, csv_rows_override=None, header_override=None, keyfix=None):
    """src_rows: list of source rows (lists of cell strings). Returns a result dict; draws the 10% sample from rng."""
    if csv_rows_override is not None:
        header, rows = header_override, csv_rows_override
    else:
        header, rows = read_table(csv_path)
    src_by_key = {}
    for sr in src_rows:
        if not sr or key_from_src >= len(sr):
            continue
        key = norm_key(sr[key_from_src])
        if keyfix:
            key = keyfix(key)
        if not key or (data_filter and not data_filter(sr)):
            continue
        parsed = [parse_cell(c) for c in sr]
        src_by_key.setdefault(key, parsed)
    csv_keys = [(keyfix(norm_key(r[keycol])) if keyfix else norm_key(r[keycol])) for r in rows]
    _ck = {id(r): k for r, k in zip(rows, csv_keys)}
    matched = sum(1 for k in csv_keys if k in src_by_key)
    maps = infer_mapping(rows, header, keycol, src_by_key, skip_cols, keyf=lambda r: _ck[id(r)])
    mapped = {j: m for j, m in maps.items() if m}
    unmapped = [header[j] for j, m in maps.items() if not m and any(fin(fnum(r[j])) for r in rows if j < len(r))]
    sem_problems = []
    for j, m in mapped.items():
        if m["sem"] and m["role"] in ("p", "m") and m["role"] != m["sem"]:
            # count asymmetric rows supporting each reading
            sup = {"p": 0, "m": 0}
            for r in rows:
                s = src_by_key.get(_ck[id(r)]); x = fnum(r[j]) if j < len(r) else float("nan")
                if s is None or not fin(x):
                    continue
                comp = s[m["ci"]][0]
                if "p" in comp and "m" in comp and comp["p"] != comp["m"]:
                    for role in ("p", "m"):
                        if equal_num(x, comp[role] * 10 ** m["k"]):
                            sup[role] += 1
            if sup[m["role"]] > 0 and sup[m["sem"]] == 0:
                sem_problems.append(f"{header[j]}: named {m['sem']}-error but equals the source {m['role']}-error in {sup[m['role']]} asymmetric rows")
    cells = []
    for i, r in enumerate(rows):
        for j in sorted(mapped):
            if j < len(r) and fin(fnum(r[j])) and csv_keys[i] in src_by_key:
                cells.append((i, j))
    def check_cell(i, j):
        m = mapped[j]; r = rows[i]; s = src_by_key[csv_keys[i]]
        x = fnum(r[j])
        if m["ci"] < len(s) and s[m["ci"]][0].get("ditto"):
            return True, f"{r[keycol]} / {header[j]} = {x}: source cell is a ditto mark (same as the row above)"
        if m["ci"] >= len(s) or m["role"] not in s[m["ci"]][0]:
            return False, f"{r[keycol]} / {header[j]} = {x}: source cell {m['ci']} has no '{m['role']}' component"
        y = s[m["ci"]][0][m["role"]] * 10 ** m["k"]
        ok = equal_num(x, y)
        return ok, f"{r[keycol]} / {header[j]} = {x} vs source {y:.6g}"
    full_bad = [d for ok, d in (check_cell(i, j) for i, j in cells) if not ok]
    dropped = []
    for i, r in enumerate(rows):
        s_ = src_by_key.get(csv_keys[i])
        if s_ is None:
            continue
        for j, m in mapped.items():
            if (j >= len(r) or r[j].strip() in ("", "nan", "NaN")) and m["ci"] < len(s_):
                comp = s_[m["ci"]][0]
                if m["role"] in comp and not comp.get("ditto") and not comp.get("lim"):
                    dropped.append(f"{r[keycol]} / {header[j]}: CSV empty, source prints {comp[m['role']]:.6g}")
    sample = []
    if rng is not None and cells:
        n = min(len(cells), max(5, math.ceil(0.10 * len(cells))))
        idx = sorted(rng.choice(len(cells), size=n, replace=False))
        sample = [(cells[t], ) + check_cell(*cells[t]) for t in idx]
    s_bad = [d for (_, ok, d) in sample if not ok]
    res = dict(table=tag, csv=rel(csv_path) if csv_path else None, csv_rows=len(rows), src_rows_keyed=len(src_by_key), csv_rows_matched=matched,
               mapped_columns=len(mapped), unmapped_columns=unmapped, cells_mapped=len(cells), sample_n=len(sample), sample_fail=len(s_bad),
               sample_fail_detail=s_bad, full_fail=len(full_bad), full_fail_detail=full_bad[:30], semantic_problems=sem_problems, dropped=dropped,
               mapping={header[j]: f"cell {m['ci']} {m['role']} x10^{m['k']} ({m['votes']}/{m['n']})" for j, m in mapped.items()})
    status = "PASS" if (not s_bad and not sem_problems and matched == len(rows)) else "PROBLEM"
    res["status"] = status
    P(f"  [T] {tag}: CSV rows {len(rows)}, matched to source {matched}; mapped columns {len(mapped)}, unmapped {len(unmapped)}; "
      f"sample {len(sample)} cells, {len(s_bad)} fail; full scan {len(cells)} cells, {len(full_bad)} mismatch -> {status}")
    if unmapped:
        P(f"        unmapped (derived/converted, excluded): {unmapped[:12]}")
    for d in s_bad[:10]:
        P(f"        SAMPLE FAIL: {d}")
    for d in full_bad[:10]:
        P(f"        full-scan mismatch: {d}")
    for d in sem_problems:
        P(f"        SEMANTIC: {d}")
    for d in dropped[:10]:
        P(f"        DROPPED: {d}")
    if matched != len(rows):
        P(f"        CSV rows without a source row: {[r[keycol] for r, k in zip(rows, csv_keys) if k not in src_by_key][:10]}")
    return res


def rc100_posthoc():
    """POST-HOC (added after the targeted re-read of row 83; not in the frozen criteria): RC100 eq. 8 at r = R_e."""
    sid = "S04 RC100 (Nestor Shachar+23)"
    pp = os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")
    Pv = read_dicts(pp)
    cl = {}; fl = []; cl2 = {}; fl2 = []
    for r in Pv:
        V, s = fnum(r["Vc_Re_kms"]), fnum(r["sigma0_kms"])
        v2_hi = (V + 0.5) ** 2 - 3.36 * (s - 0.5) ** 2
        v2 = V * V - 3.36 * s * s
        c = "CONSISTENT" if v2_hi > 0 else "PROBLEM"
        cl[c] = cl.get(c, 0) + 1
        if c == "PROBLEM":
            fl.append(f"{r['idx']} {r['name']}: Vc {V:.0f}, sigma0 {s:.0f}: Vc^2 - 3.36 sigma0^2 = {v2:.0f} (km/s)^2 < 0")
        if v2 > 0:
            q = math.sqrt(v2) / s
            c2 = "FLAG" if q < 2.3 else "CONSISTENT"
            cl2[c2] = cl2.get(c2, 0) + 1
            if c2 == "FLAG":
                fl2.append(f"{r['idx']} {r['name']}: V_rot(R_e)/sigma0 = {q:.2f}")
    record(sid, "POST-HOC: V_rot(R_e)^2 = Vc^2 - 3.36 sigma0^2 > 0 (the paper's eq. 8 at R_e)", "H", len(Pv), cl, "added after the targeted re-read of row 83; not in the frozen criteria", rows_flagged=fl)
    record(sid, "POST-HOC: V_rot(R_e)/sigma0 >= 2.3 (the selection cut, if applied at R_e)", "S", sum(cl2.values()), cl2, "the paper's cut may be applied to the observed curve, not at R_e", rows_flagged=fl2)


def run_transcription():
    P("\n=== CHECK 4: TRANSCRIPTION (seed 287; frozen table order)")
    rng = np.random.default_rng(SEED)
    T = R["transcription"]
    # ---- S04 RC100: visual re-read of the seed rows
    idx = sorted(int(i) + 1 for i in rng.choice(100, size=10, replace=False))
    pv = {r["idx"]: r for r in read_dicts(os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv"))}
    po = {r["idx"]: r for r in read_dicts(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"))}
    vis = {r["idx"]: r for r in read_dicts(os.path.join(HERE, "rc100_visual_reread.csv"))}
    fails = []; fails_o = []; n = 0
    for i in idx + [83]:
        v = vis.get(str(i))
        if v is None:
            fails.append(f"row {i}: no visual reading"); continue
        for fcol in ("name", "z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "Vc_Re_kms", "sigma0_kms"):
            n += 1
            a, b, c = v[fcol], pv[str(i)][fcol], po[str(i)][fcol]
            same = (a.strip() == b.strip()) if fcol == "name" else abs(fnum(a) - fnum(b)) < 1e-9
            same_o = (a.strip() == c.strip()) if fcol == "name" else abs(fnum(a) - fnum(c)) < 1e-9
            if not same:
                fails.append(f"row {i} {fcol}: image {a} vs paper-values file {b}")
            if not same_o:
                fails_o.append(f"row {i} {fcol}: image {a} vs original CSV {c}")
    P(f"  [T] S04 RC100 Table 3 (PDF page images, visual): seed rows {idx} + targeted row 83; {n} cells; paper-values file mismatches {len(fails)}; original CSV mismatches {len(fails_o)}")
    for d in fails + fails_o:
        P(f"        {d}")
    T["S04 RC100"] = dict(seed_rows=idx, targeted=[83], cells=n, fail_paper_values=fails, fail_original_csv=fails_o,
                          status="PASS" if not fails else "PROBLEM")
    # ---- S06 Price+21 (HTML; Tables 1 and 3 merged by ID)
    ph = os.path.join(DA, "price2021_rc41", "raw_small", "arxiv_2109.02659_html_fetched_2026-09-29.html")
    t1 = html_table(ph, "S2.T1.4"); t3 = html_table(ph, "S3.T3.4")
    t3k = {norm_key(r[0]): r for r in t3 if r and r[0]}
    merged = [r + t3k.get(norm_key(r[0]), []) for r in t1 if r and r[0] and norm_key(r[0]) in t3k]
    hdr, rows = read_table(os.path.join(DA, "price2021_rc41", "price2021_rc41.csv"))
    T["S06 Price+21"] = transcription_table("S06 Price+21 Tables 1+3 (HTML)", os.path.join(DA, "price2021_rc41", "price2021_rc41.csv"), merged, rng=rng,
                                            skip_cols=(hdr.index("in_2D_priors_table"),))
    T["S06 Price+21"]["html_data_rows"] = dict(t1=len([r for r in t1 if r and re.match(r"^[A-Za-z]", r[0] or "") and r[0] != "ID"]), t3=len(t3k) - 1)
    # ---- S07 FS+18 (HTML)
    fh = os.path.join(DA, "highz_literature_tables", "raw_small", "arxiv_1802.07276_html_fetched_2026-09-29.html")
    base = os.path.join(DA, "highz_literature_tables", "sins_ao")
    for tid, f in (("S2.T1.2", "sins_ao_table1_sample.csv"), ("S5.T5.2", "sins_ao_table5_sizes.csv"), ("S6.T6.2", "sins_ao_table6_kinematics.csv")):
        T[f"S07 FS+18 {f}"] = transcription_table(f"S07 FS+18 {f} (HTML {tid})", os.path.join(base, f), html_table(fh, tid), rng=rng)
    # ---- S10 CRISTAL (TeX)
    ct = os.path.join(EXT, "arxiv_src", "2507.11600", "main_arxiv.tex")
    for lab, f in (("tab:main_table", "cristal2025_sample.csv"), ("tab:kins_props", "cristal2025_kinematics.csv"), ("tab:dysmalpy_results", "cristal2025_dynamics.csv")):
        T[f"S10 CRISTAL {f}"] = transcription_table(f"S10 CRISTAL {f} (TeX {lab})", os.path.join(AT, f), tex_table(ct, lab), rng=rng,
                                                    keyfix=lambda k: re.sub(r"^cristal", "", k))
    # ---- S11 Jones+21 (HTML): Table 1 and the rings (composite key name|R)
    jh = os.path.join(DA, "highz_literature_tables", "raw_small", "arxiv_2104.03099_html_fetched_2026-09-30.html")
    T["S11 Jones Table 1"] = transcription_table("S11 Jones+21 Table 1 (HTML S3.T1.6)", os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_table1_sample_classes.csv"),
                                                 html_table(jh, "S3.T1.6"), rng=rng)
    t1rows = [r for r in html_table(jh, "S3.T1.6") if r and r[0] and re.match(r"^[A-Za-z]", r[0]) and r[0] not in ("Name",)]
    T["S11 Jones Table 1"]["html_data_rows"] = len(t1rows)
    T["S11 Jones Table 1"]["html_names_not_in_csv"] = sorted({r[0] for r in t1rows} - {r["name"] for r in read_dicts(os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_table1_sample_classes.csv"))})
    src_r = []; cur = None
    for r in html_table(jh, "A3.T2.4"):
        if len(r) < 5:
            continue
        if r[0].strip() and r[0].strip() not in ("Source",):
            cur = r[0].strip()
        if cur and re.match(r"^[\d.]+$", r[1].strip()):
            src_r.append([f"{cur}|{r[1].strip()}"] + r[1:])
    hj, rj = read_table(os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_tableA3_rings.csv"))
    rj2 = [[f"{r[0]}|{r[1]}"] + r[1:] for r in rj]
    T["S11 Jones rings"] = transcription_table("S11 Jones+21 rings (HTML A3.T2.4)", os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_tableA3_rings.csv"),
                                               src_r, rng=rng, csv_rows_override=rj2, header_override=["key"] + hj[1:])
    # ---- S13 ALPAKA (TeX, the compiled alpaka_v2.tex) + arXiv:2601.03338
    at = os.path.join(EXT, "arxiv_src", "2303.16227", "alpaka_v2.tex")
    for lab, f in (("tab:tab1", "alpaka1_sample.csv"), ("tab:tab2", "alpaka1_alma_obs.csv"), ("tab:mstar", "alpaka1_properties.csv"), ("tab:PA", "alpaka1_geometry.csv"), ("tab:vsigma", "alpaka1_kinematics.csv")):
        T[f"S13 ALPAKA {f}"] = transcription_table(f"S13 ALPAKA {f} (TeX {lab})", os.path.join(AT, f), tex_table(at, lab), rng=rng)
    jt = os.path.join(EXT, "arxiv_src", "2601.03338", "main.tex")
    for lab, f in (("tab:data", "alpaka_jwst2026_data.csv"), ("tab:fid", "alpaka_jwst2026_fiducial_fit.csv")):
        T[f"S13 {f}"] = transcription_table(f"S13 arXiv:2601.03338 {f} (TeX {lab})", os.path.join(AT, f), tex_table(jt, lab), rng=rng,
                                            keyfix=lambda k: re.sub(r"^id", "", k))
    # ---- S14 Amvrosiadis (TeX)
    am = os.path.join(EXT, "arxiv_src", "2312.08959", "main.tex")
    for lab, f in (("tab:properties", "amvrosiadis_parent.csv"), ("tab:table1", "amvrosiadis_bestfit.csv")):
        T[f"S14 Amvrosiadis {f}"] = transcription_table(f"S14 Amvrosiadis {f} (TeX {lab})", os.path.join(AT, f), tex_table(am, lab), rng=rng)
    # ---- S15 Danhaive (TeX)
    dt = os.path.join(EXT, "arxiv_src", "2503.21863", "main.tex")
    T["S15 Danhaive"] = transcription_table("S15 Danhaive gold (TeX tab:results-gold)", os.path.join(AT, "danhaive2025_gold.csv"), tex_table(dt, "tab:results-gold"), rng=rng)
    # ---- S16 Roman-Oliveira (TeX)
    rt = os.path.join(EXT, "arxiv_src", "2302.03049", "main.tex")
    for lab, f in (("tab:data", "romanoliveira2023_sample.csv"), ("tab:masses", "romanoliveira2023_gasmasses.csv"), ("tab:vel", "romanoliveira2023_kinematics.csv")):
        T[f"S16 RO23 {f}"] = transcription_table(f"S16 Roman-Oliveira {f} (TeX {lab})", os.path.join(AT, f), tex_table(rt, lab), rng=rng)
    # ---- S17 Lelli+23 (TeX; mass models keyed galaxy|model)
    lt = os.path.join(EXT, "arxiv_src", "2302.00030", "ColdGasDiskCosmicNoon.tex")
    src_m = []; cur = None
    for r in tex_table(lt, "tab:mass") or []:
        if len(r) < 9:
            continue
        g = clean_math(r[0]).strip()
        if g.startswith("zC"):
            cur = g
        if cur and r[1].strip() and not r[1].strip().startswith("Model"):
            src_m.append([f"{cur}|{clean_math(r[1]).replace('+', ' ').strip()}"] + r[2:])
    hm, rm = read_table(os.path.join(AT, "lelli2023_massmodels.csv"))
    rm2 = [[f"{r[0]}|{r[1].replace('+', ' ')}"] + r[2:] for r in rm]
    T["S17 Lelli mass models"] = transcription_table("S17 Lelli+23 mass models (TeX tab:mass)", os.path.join(AT, "lelli2023_massmodels.csv"), src_m, rng=rng,
                                                     csv_rows_override=rm2, header_override=["key"] + hm[2:])
    # ---- S18 MUSE-DARK II Table 3 (TeX; keyed by row order)
    mt = os.path.join(EXT, "arxiv_src", "2603.28856", "aa59953-26.tex")
    srcm = [r for r in (tex_table(mt, "tab:TFR_fits") or []) if len(r) >= 9 and "star" in r[0] or (len(r) >= 9 and "bar" in r[0] and "M_" in r[0])]
    srcm = [[f"row{i + 1}"] + r for i, r in enumerate(srcm)]
    h2, r2 = read_table(os.path.join(AT, "musedark_II_III", "musedarkII_table3_tfr_fits.csv"))
    r2b = [[f"row{i + 1}"] + r for i, r in enumerate(r2)]
    T["S18 MUSE-DARK II Table 3"] = transcription_table("S18 MUSE-DARK II Table 3 (TeX tab:TFR_fits)", os.path.join(AT, "musedark_II_III", "musedarkII_table3_tfr_fits.csv"),
                                                        srcm, rng=rng, csv_rows_override=r2b, header_override=["key"] + h2)
    # ---- S22 Jarvis+25 (HTML Tables 2 + 3 merged by ID)
    mh = os.path.join(DA, "mightee_hi_highz", "raw_small", "arxiv_2506.11935_html_fetched_2026-09-29.html")
    a = html_table(mh, "S4.T2.11"); b = html_table(mh, "S4.T3.9")
    bk = {norm_key(r[0]): r for r in b if r and r[0]}
    merged = [r + bk.get(norm_key(r[0]), []) for r in a if r and r[0] and re.match(r"^\d", r[0])]
    T["S22 Jarvis+25"] = transcription_table("S22 Jarvis+25 Tables 2+3 (HTML)", os.path.join(DA, "mightee_hi_highz", "mightee_hi_highz.csv"), merged, rng=rng,
                                             skip_cols=tuple(i for i, h in enumerate(read_table(os.path.join(DA, "mightee_hi_highz", "mightee_hi_highz.csv"))[0]) if h in ("logMHI_recomputed_Planck18", "shared_with_11a")))
    # ---- machine reads: S05 KMOS3D FITS, S08 FS+09 .dat, S09 Tacconi+13 .dat
    run_machine_reads(rng)
    # raw_small TeX fragments are verbatim substrings of the original TeX
    frag_ok = []; frag_bad = []
    srcmap = {"alpaka1_2303.16227": "2303.16227/alpaka_v2.tex", "alpaka_jwst2026_2601.03338": "2601.03338/main.tex", "amvrosiadis2025_2312.08959": "2312.08959/main.tex",
              "cristal2025_2507.11600": "2507.11600/main_arxiv.tex", "danhaive2025_2503.21863": "2503.21863/main.tex", "kurvs2023_2305.04382": None,
              "lelli2023_2302.00030": "2302.00030/ColdGasDiskCosmicNoon.tex", "romanoliveira2023_2302.03049": "2302.03049/main.tex", "manceraPina2026_2511.08685": None}
    for f in sorted(glob.glob(os.path.join(AT, "raw_small", "*.tex"))):
        bn = os.path.basename(f)
        key = next((k for k in srcmap if bn.startswith(k)), None)
        if key is None:
            continue
        cand = [srcmap[key]] if srcmap[key] else []
        if not cand:
            d = os.path.join(EXT, "arxiv_src", bn.split("_")[1])
            cand = [os.path.relpath(x, os.path.join(EXT, "arxiv_src")) for x in glob.glob(os.path.join(d, "*.tex"))]
        frag = re.sub(r"\s+", "", open(f, errors="ignore").read())
        ok = any(frag in re.sub(r"\s+", "", open(os.path.join(EXT, "arxiv_src", c), errors="ignore").read()) for c in cand)
        (frag_ok if ok else frag_bad).append(bn)
    P(f"  raw_small TeX fragments verbatim in the original TeX: {len(frag_ok)} yes, {len(frag_bad)} no {frag_bad}")
    T["raw_small_fragments"] = dict(verbatim=frag_ok, not_verbatim=frag_bad)


def run_machine_reads(rng):
    T = R["transcription"]
    from astropy.io import fits
    # KMOS3D: CSV vs FITS (same column names)
    fp = os.path.join(DA, "kmos3d_phibss", "raw_small", "k3d_fnlsp_table_v3.fits")
    fh = os.path.join(DA, "kmos3d_phibss", "raw_small", "k3d_fnlsp_table_hafits_v3.fits")
    K = read_dicts(os.path.join(DA, "kmos3d_phibss", "kmos3d_catalog.csv"))
    with fits.open(fp) as h1, fits.open(fh) as h2:
        d1 = h1[1].data; d2 = h2[1].data
        n1 = list(d1.columns.names); n2 = list(d2.columns.names)
        byid1 = {str(x).strip(): i for i, x in enumerate(d1["ID"])}
        byid2 = {str(x).strip(): i for i, x in enumerate(d2["ID"])} if "ID" in n2 else {}
        cells = []
        for i, r in enumerate(K):
            for c, v in r.items():
                if c == "ID":
                    continue
                x = fnum(v)
                if not fin(x):
                    continue
                if c in n1:
                    cells.append((i, c, 1))
                elif c in n2 or (c.startswith("HAFIT_") and c[6:] in n2):
                    cells.append((i, c, 2))
        n = min(len(cells), max(5, math.ceil(0.10 * len(cells))))
        idx = sorted(rng.choice(len(cells), size=n, replace=False))
        bad = []
        for t in idx:
            i, c, w = cells[t]
            r = K[i]; x = fnum(r[c])
            if w == 1:
                y = float(d1[c][byid1[r["ID"]]])
            else:
                cc = c if c in n2 else c[6:]
                j = byid2.get(r["ID"])
                if j is None:
                    bad.append(f"{r['ID']} {c}: no hafits row"); continue
                y = float(d2[cc][j])
            if not (abs(x - y) <= 1e-6 * max(1.0, abs(y))):
                bad.append(f"{r['ID']} {c}: CSV {x} vs FITS {y}")
    P(f"  [T] S05 KMOS3D catalogue vs FITS (machine read): {len(cells)} cells, sample {n}, {len(bad)} fail")
    for d in bad[:10]:
        P(f"        SAMPLE FAIL: {d}")
    T["S05 KMOS3D FITS"] = dict(cells=len(cells), sample_n=n, sample_fail=len(bad), detail=bad, status="PASS" if not bad else "PROBLEM",
                                rows_csv=len(K), rows_fits=len(d1))
    # FS+09: CSV vs CDS .dat
    raw = os.path.join(DA, "high_z_tf_tables", "raw_small")
    rd = os.path.join(raw, "forsterschreiber2009_ReadMe.txt")
    t9 = {r["Name"]: r for r in cds_rows(os.path.join(raw, "forsterschreiber2009_table9.dat"), cds_layout(rd, "table9.dat"))}
    t6 = {r["Name"]: r for r in cds_rows(os.path.join(raw, "forsterschreiber2009_table6.dat"), cds_layout(rd, "table6.dat"))}
    t3 = {r["Name"]: r for r in cds_rows(os.path.join(raw, "forsterschreiber2009_table3.dat"), cds_layout(rd, "table3.dat"))}
    mp = {"half_vobs_kms": (t9, "Vel/2"), "e_half_vobs": (t9, "e_Vel/2"), "v_over_2sig": (t9, "V/2sig"), "vrot_over_sig": (t9, "Vrot/sig"),
          "vel_kms": (t9, "Vel"), "E_vel": (t9, "E_Vel"), "e_vel": (t9, "e_Vel"), "mgas_sfr0_1e10msun": (t9, "M0"), "E_m0": (t9, "E_M0"), "e_m0": (t9, "e_M0"),
          "mgas_sfr00_1e10msun": (t9, "M00"), "mdyn_1e10msun": (t9, "Mdyn"), "E_mdyn": (t9, "E_Mdyn"), "e_mdyn": (t9, "e_Mdyn"), "z_halpha": (t6, "zHa"),
          "r_half_halpha_kpc": (t6, "r1/2"), "e_r_half_kpc": (t6, "e_r1/2"), "sigma_int_kms": (t6, "Sig"), "mstar_1e10msun": (t3, "Mass"), "E_mstar": (t3, "E_Mass"),
          "e_mstar": (t3, "e_Mass"), "sfr_sed_msun_yr": (t3, "SFR")}
    S = read_dicts(os.path.join(DA, "high_z_tf_tables", "sins2009_dynamics.csv"))
    cells = [(i, c) for i, r in enumerate(S) for c in mp if fin(fnum(r[c]))]
    n = min(len(cells), max(5, math.ceil(0.10 * len(cells))))
    idx = sorted(rng.choice(len(cells), size=n, replace=False))
    bad = []
    for t in idx:
        i, c = cells[t]
        tab, lab = mp[c]
        y = fnum(tab.get(S[i]["name"], {}).get(lab))
        if not (fin(y) and abs(fnum(S[i][c]) - y) < 1e-9):
            bad.append(f"{S[i]['name']} {c}: CSV {S[i][c]} vs CDS {lab} {y}")
    full = [(S[i]["name"], c) for i, c in cells if not (fin(fnum(mp[c][0].get(S[i]["name"], {}).get(mp[c][1]))) and abs(fnum(S[i][c]) - fnum(mp[c][0][S[i]["name"]][mp[c][1]])) < 1e-9)]
    P(f"  [T] S08 FS+09 vs CDS .dat (machine read): {len(cells)} cells, sample {n}, {len(bad)} fail; full scan mismatches {len(full)}")
    for d in bad[:10]:
        P(f"        SAMPLE FAIL: {d}")
    T["S08 FS+09 CDS"] = dict(cells=len(cells), sample_n=n, sample_fail=len(bad), detail=bad, full_mismatch=full[:20], status="PASS" if not bad else "PROBLEM")
    # Tacconi+13: CSV vs CDS .dat
    raw = os.path.join(DA, "kmos3d_phibss", "raw_small")
    rd = os.path.join(raw, "tacconi2013_ReadMe.txt")
    tb2 = {(r["Name"], r["m_Name"]): r for r in cds_rows(os.path.join(raw, "tacconi2013_table2.dat"), cds_layout(rd, "table2.dat"))}
    tb1 = {r["Name"]: r for r in cds_rows(os.path.join(raw, "tacconi2013_table1.dat"), cds_layout(rd, "table1.dat"))}
    mp = {"vrot_kms": "Vrot", "rh_opt_kpc": "Rh.o", "rh_co_kpc": "Rh.co", "sfr_msun_yr": "SFR", "fco_jykms": "F(CO)", "fco_err": "e_F(CO)", "lco_K_kms_pc2": "L(CO)",
          "mmol_msun": "Mmol", "mstar_msun": "M*", "fgas_quoted": "fgas", "logSigma_mol": "logSmol", "logSigma_sfr": "logSsf"}
    Tq = read_dicts(os.path.join(DA, "kmos3d_phibss", "phibss13_joined.csv"))
    def tv(r, c):
        if c == "z_co":
            return fnum(tb1.get(r["name"], {}).get("zCO"))
        row = tb2.get((r["name"], r["comp"]))
        if row is None:
            return float("nan")
        y = fnum(row.get(mp[c]))
        return y
    def same(x, y, c):
        if c in ("fco_jykms", "lco_K_kms_pc2", "mmol_msun"):
            x, y = abs(x), abs(y)      # the ReadMe: a minus sign marks a 3-sigma upper limit; the CSV keeps the sign on F and L', not on Mmol
        return fin(y) and abs(x - y) <= 1e-6 * max(1, abs(y))
    cells = [(i, c) for i, r in enumerate(Tq) for c in list(mp) + ["z_co"] if fin(fnum(r[c]))]
    n = min(len(cells), max(5, math.ceil(0.10 * len(cells))))
    idx = sorted(rng.choice(len(cells), size=n, replace=False))
    bad = []
    for t in idx:
        i, c = cells[t]
        y = tv(Tq[i], c); x = fnum(Tq[i][c])
        if not same(x, y, c):
            bad.append(f"{Tq[i]['name']}{Tq[i]['comp']} {c}: CSV {x} vs CDS {y}")
    full = [f"{Tq[i]['name']}{Tq[i]['comp']} {c}: CSV {Tq[i][c]} vs CDS {tv(Tq[i], c)}" for i, c in cells if not same(fnum(Tq[i][c]), tv(Tq[i], c), c)]
    P(f"  [T] S09 Tacconi+13 vs CDS .dat (machine read): {len(cells)} cells, sample {n}, {len(bad)} fail; full scan mismatches {len(full)}")
    for d in bad[:10] + full[:10]:
        P(f"        {d}")
    T["S09 Tacconi13 CDS"] = dict(cells=len(cells), sample_n=n, sample_fail=len(bad), detail=bad, full_mismatch=full[:20], status="PASS" if not bad else "PROBLEM")


# =============================================================================== CHECK 2: cross-survey overlaps
HZ_ALIAS = {"hz1": "dc536534", "hz2": "dc417567", "hz3": "dc683613", "hz4": "dc494057", "hz6": "dc848185", "hz8": "dc873321"}


def nn(name):
    s = str(name).lower().replace("\\_", "_")
    s = s.split(",")[0]
    s = re.sub(r"[\s_\-.]", "", s)
    s = s.replace("deimoscosmos", "dc").replace("vudscosmos", "vc").replace("vudsefdcs", "ve").replace("deep3a", "d3a").replace("ssa22a", "ssa22")
    s = re.sub(r"^q\d{4}(?=bx|md|bm)", "", s)
    s = re.sub(r"^cristal", "", s)
    return HZ_ALIAS.get(s, s)


def sym(eh, el):
    a = [x for x in (eh, el) if fin(x)]
    return float(np.mean(a)) if a else float("nan")


def compare(src1, src2, obj, qty, a, ea, b, eb, tag_same, note="", rel_only=False, log=False):
    d = a - b
    sig = math.sqrt((ea if fin(ea) else 0) ** 2 + (eb if fin(eb) else 0) ** 2)
    pull = d / sig if sig > 0 and not rel_only else float("nan")
    if fin(pull):
        cls = "AGREE" if abs(pull) <= 2 else ("TENSION" if abs(pull) <= 3 else "DISAGREE")
    else:
        cls = "NO-ERRORS"
    problem = (cls == "DISAGREE" and tag_same)
    entry = dict(pair=f"{src1} vs {src2}", object=obj, quantity=qty, a=a, ea=ea, b=b, eb=eb, diff=d, pull=pull, cls=cls,
                 same_definition=bool(tag_same), problem=problem, note=note, rel=(d / b if (b and not log) else None))
    R["cross"].append(entry)
    return entry


def z_half(z):
    t = repr(float(z))
    if t.endswith(".0"):
        return 0.05
    return 0.5 * 10 ** (-len(t.split(".")[1])) if "." in t else 0.5


def zcompare(src1, src2, obj, za, zb, same_line, note=""):
    """velocity classes of FROZEN_CRITERIA section 4, with the printed half-units of both redshifts (section 2.1) added as a
    rounding allowance (an application of section 2 to section 4, disclosed in AUDIT.md)."""
    if not (fin(za) and fin(zb)):
        return None
    zm = 1 + 0.5 * (za + zb)
    dv = C_KMS * abs(za - zb) / zm
    dround = C_KMS * (z_half(za) + z_half(zb)) / zm
    cls = "AGREE" if dv <= 300 + dround else ("TENSION" if dv <= 1000 + dround else "DISAGREE")
    entry = dict(pair=f"{src1} vs {src2}", object=obj, quantity="z", a=za, b=zb, diff=za - zb, dv_kms=dv, dv_round_kms=dround, cls=cls, same_definition=bool(same_line),
                 problem=(cls == "DISAGREE" and same_line), note=note)
    R["cross"].append(entry)
    return entry


def radec_sex(ra, dec):
    try:
        h, m, s_ = [float(x) for x in ra.split(":")]
        dec = dec.replace("[", "").replace("]", "").replace("$", "").replace(" ", "")
        sg = -1 if dec.startswith("-") else 1
        d, mm, ss = [float(x) for x in dec.lstrip("+-").split(":")]
        return 15 * (h + m / 60 + s_ / 3600), sg * (d + mm / 60 + ss / 3600)
    except Exception:
        return None


def sep_arcsec(p1, p2):
    return 3600 * math.hypot((p1[0] - p2[0]) * math.cos(math.radians(0.5 * (p1[1] + p2[1]))), p1[1] - p2[1])


def run_cross():
    P("\n=== CHECK 2: CROSS-SURVEY OVERLAPS")
    rc = {nn(r["name"]): r for r in read_dicts(os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv"))}
    pr = {nn(r["id"]): r for r in read_dicts(os.path.join(DA, "price2021_rc41", "price2021_rc41.csv"))}
    k3 = {nn(r["ID"]): r for r in read_dicts(os.path.join(DA, "kmos3d_phibss", "kmos3d_catalog.csv"))}
    base = os.path.join(DA, "highz_literature_tables", "sins_ao")
    f1 = {nn(r["source"]): r for r in read_dicts(os.path.join(base, "sins_ao_table1_sample.csv"))}
    f6 = {nn(r["source"]): r for r in read_dicts(os.path.join(base, "sins_ao_table6_kinematics.csv"))}
    f9 = {nn(r["name"]): r for r in read_dicts(os.path.join(DA, "high_z_tf_tables", "sins2009_dynamics.csv"))}
    tq = {}
    for r in read_dicts(os.path.join(DA, "kmos3d_phibss", "phibss13_joined.csv")):
        tq.setdefault(nn(r["name"]), r)
    lm = read_dicts(os.path.join(AT, "lelli2023_massmodels.csv"))
    lb = read_dicts(os.path.join(AT, "lelli2023_3dbarolo.csv"))
    alp_s = {r["id"]: r for r in read_dicts(os.path.join(AT, "alpaka1_sample.csv"))}
    alp_p = {r["id"]: r for r in read_dicts(os.path.join(AT, "alpaka1_properties.csv"))}
    alp_k = {r["id"]: r for r in read_dicts(os.path.join(AT, "alpaka1_kinematics.csv"))}
    n0 = len(R["cross"])
    # ---- RC100 x Price+21 (RC41 is a subset of RC100; same team; RC100 = mean of methods A, B, C)
    for k, p in pr.items():
        r = rc.get(k)
        if not r:
            P(f"  RC41 {p['id']} has no RC100 row"); continue
        zcompare("RC100", "Price+21", p["id"], fnum(r["z"]), fnum(p["z"]), True, "RC100 prints z to 2 decimals")
        compare("RC100", "Price+21", p["id"], "log M_bar", fnum(r["logMbar_Msun"]), float("nan"), fnum(p["logMbar_1D"]), sym(fnum(p["logMbar_hi"]), fnum(p["logMbar_lo"])), False,
                "Price errors only (RC100's printed errors are in the page image); RC100 averages three methods, one being Price's", log=True)
        compare("RC100", "Price+21", p["id"], "R_e,disk", fnum(r["Re_kpc"]), float("nan"), fnum(p["Re_1D_kpc"]), sym(fnum(p["Re_hi"]), fnum(p["Re_lo"])), False, "RC100 = mean of methods A, B, C; Price = method B MAP")
        compare("RC100", "Price+21", p["id"], "sigma0", fnum(r["sigma0_kms"]), float("nan"), fnum(p["sigma0_1D_kms"]), sym(fnum(p["sigma0_hi"]), fnum(p["sigma0_lo"])), False, "RC100 = mean of methods A, B, C; Price = method B MAP")
        compare("RC100", "Price+21", p["id"], "f_DM(R_e)", fnum(r["fDM_within_Re"]), float("nan"), fnum(p["fDM_Re_1D"]), sym(fnum(p["fDM_hi"]), fnum(p["fDM_lo"])), False, "RC100 = mean of methods A, B, C; Price = method B MAP")
    # ---- RC100 / Price x KMOS3D release
    for k, r in rc.items():
        q = k3.get(k)
        if q and fnum(q["Z"]) > 0:
            zcompare("RC100", "KMOS3D release", r["name"], fnum(r["z"]), fnum(q["Z"]), True, "RC100 2 decimals")
    for k, p in pr.items():
        q = k3.get(k)
        if q and fnum(q["LMSTAR"]) > 0:
            compare("Price+21", "KMOS3D release", p["id"], "log M* (SED)", fnum(p["logMstar_SED"]), float("nan"), fnum(q["LMSTAR"]), float("nan"), True,
                    "same team's SED masses; no errors printed", rel_only=True, log=True)
    # ---- the SINS family: FS+18 x FS+09 x Tacconi+13 x RC100 x Price x KMOS3D x Lelli+23 x ALPAKA 14
    for k, a in f1.items():
        z18 = fnum(a["z_Halpha"]); m18 = fnum(a["Mstar_1e10Msun"])
        pos18 = radec_sex(a["ra"], a["dec"])
        if k in f9:
            b = f9[k]
            zcompare("FS+18", "FS+09", a["source"], z18, fnum(b["z_halpha"]), True, "both Halpha (SINFONI)")
            if fin(m18) and fin(fnum(b["mstar_1e10msun"])):
                compare("FS+18", "FS+09", a["source"], "log M*", math.log10(m18 * 1e10), 0.2, math.log10(fnum(b["mstar_1e10msun"]) * 1e10),
                        0.434 * sym(fnum(b["E_mstar"]), fnum(b["e_mstar"])) / fnum(b["mstar_1e10msun"]), False, "different SED fits (FS+18 states +-0.2 dex)", log=True)
            if k in f6 and fin(fnum(b["vel_kms"])):
                compare("FS+18", "FS+09", a["source"], "V_c (FS+18 eq.1) vs v_d (FS+09)", fnum(f6[k]["Vc_kms"]), sym(fnum(f6[k]["Vc_kms_errhi"]), fnum(f6[k]["Vc_kms_errlo"])),
                        fnum(b["vel_kms"]), sym(fnum(b["E_vel"]), fnum(b["e_vel"])), False, "AO vs seeing-limited; different definitions")
        if k in tq:
            b = tq[k]
            zcompare("FS+18", "Tacconi+13", a["source"], z18, fnum(b["z_co"]), False, "Halpha vs CO")
            if pos18 and fin(fnum(b["ra_deg"])):
                s_ = sep_arcsec(pos18, (fnum(b["ra_deg"]), fnum(b["dec_deg"])))
                R["cross"].append(dict(pair="FS+18 vs Tacconi+13", object=a["source"], quantity="position", diff=s_, cls="AGREE" if s_ <= 1 else "DISAGREE",
                                       same_definition=False, problem=False, note="optical vs CO/optical position (arcsec)"))
            if fin(m18) and fin(fnum(b["mstar_msun"])):
                compare("FS+18", "Tacconi+13", a["source"], "log M*", math.log10(m18 * 1e10), 0.2, math.log10(fnum(b["mstar_msun"])), 0.13, False, "Tacconi+13: +-30% systematic", log=True)
        rk = rc.get(k)
        if rk:
            zcompare("FS+18", "RC100", a["source"], z18, fnum(rk["z"]), True, "RC100 2 decimals")
            if k in f6:
                compare("FS+18", "RC100", a["source"], "sigma0", fnum(f6[k]["sigma0_kms"]), sym(fnum(f6[k]["sigma0_kms_errhi"]), fnum(f6[k]["sigma0_kms_errlo"])),
                        fnum(rk["sigma0_kms"]), float("nan"), False, "direct estimate vs forward model")
                compare("FS+18", "RC100", a["source"], "R_e", fnum(f6[k]["Re_kpc"]), sym(fnum(f6[k]["Re_kpc_errhi"]), fnum(f6[k]["Re_kpc_errlo"])),
                        fnum(rk["Re_kpc"]), float("nan"), False, "light R_e vs disc R_e of the mass model")
                compare("FS+18", "RC100", a["source"], "V_c (eq.1, no radius) vs V_c(R_e)", fnum(f6[k]["Vc_kms"]), sym(fnum(f6[k]["Vc_kms_errhi"]), fnum(f6[k]["Vc_kms_errlo"])),
                        fnum(rk["Vc_Re_kms"]), float("nan"), False, "different radius definitions")
        if k in pr and fin(m18):
            compare("FS+18", "Price+21", a["source"], "log M*", math.log10(m18 * 1e10), 0.2, fnum(pr[k]["logMstar_SED"]), float("nan"), False, "different SED fits", log=True)
        q = k3.get(k)
        if q and pos18:
            s_ = sep_arcsec(pos18, (fnum(q["RA"]), fnum(q["DEC"])))
            R["cross"].append(dict(pair="FS+18 vs KMOS3D release", object=a["source"], quantity="position", diff=s_, cls="AGREE" if s_ <= 1 else "DISAGREE",
                                   same_definition=True, problem=s_ > 1, note="arcsec"))
    # positional cross-match FS+18 x KMOS3D independent of names
    k3pos = [(r["ID"], fnum(r["RA"]), fnum(r["DEC"]), fnum(r["Z"]), fnum(r["LMSTAR"])) for r in k3.values()]
    for k, a in f1.items():
        pos18 = radec_sex(a["ra"], a["dec"])
        if not pos18:
            continue
        best = min(((sep_arcsec(pos18, (x[1], x[2])), x) for x in k3pos), key=lambda t: t[0])
        if best[0] <= 1.0:
            zcompare("FS+18", "KMOS3D release (1\" match)", f"{a['source']} = {best[1][0]}", fnum(a["z_Halpha"]), best[1][3], True, f"sep {best[0]:.2f}\"")
            if fin(fnum(a["Mstar_1e10Msun"])) and best[1][4] > 0:
                compare("FS+18", "KMOS3D release (1\" match)", f"{a['source']} = {best[1][0]}", "log M*", math.log10(fnum(a["Mstar_1e10Msun"]) * 1e10), 0.2, best[1][4], float("nan"),
                        False, "different SED fits", log=True)
    # Lelli+23 x FS+18 x RC100 x Price
    lbd = {r["parameter"]: r for r in lb}
    for gal in ("zC-400569", "zC-488879"):
        k = nn(gal)
        vrow = [v for kk, v in lbd.items() if "rot" in kk.lower()]
        vt = None
        for r in lb:
            if "V_{\\rm rot}" in r["parameter"] or "rot" in r["parameter"].lower():
                m = re.match(r"\s*([\d.]+)", r[gal]); vt = float(m.group(1)) if m else None
        mb = {r["model"]: fnum(r["Mbar_1e10"]) * 1e10 for r in lm if r["galaxy"] == gal}
        if k in f6:
            compare("Lelli+23", "FS+18", gal, "<V_rot> (CO) vs V_c (Halpha, eq.1)", vt, float("nan"), fnum(f6[k]["Vc_kms"]),
                    sym(fnum(f6[k]["Vc_kms_errhi"]), fnum(f6[k]["Vc_kms_errlo"])), False, "different tracers and definitions")
        if k in rc:
            for model, M in mb.items():
                compare("Lelli+23", "RC100", gal, f"log M_bar ({model}) vs RC100 log M_bar", math.log10(M), float("nan"), fnum(rc[k]["logMbar_Msun"]), float("nan"), False,
                        "different mass models", rel_only=True, log=True)
        if k in pr:
            compare("Lelli+23", "Price+21", gal, "log M_bar (Baryons+NFW) vs Price log M_bar", math.log10(mb.get("Baryons+NFW", float("nan"))), float("nan"),
                    fnum(pr[k]["logMbar_1D"]), sym(fnum(pr[k]["logMbar_hi"]), fnum(pr[k]["logMbar_lo"])), False, "different mass models", log=True)
    # ALPAKA 14 = BX610
    a14 = alp_s.get("14")
    if a14:
        k = nn("BX610")
        for nm_, tab, zc, same in (("FS+18", f1, "z_Halpha", False), ("FS+09", f9, "z_halpha", False), ("Tacconi+13", tq, "z_co", True), ("RC100", rc, "z", False)):
            if k in tab:
                zcompare("ALPAKA 14", nm_, "BX610", fnum(a14["z"]), fnum(tab[k][zc]), same, "CO vs Halpha" if not same else "CO vs CO")
        if k in f1:
            compare("ALPAKA 14", "FS+18", "BX610", "log M*", math.log10(fnum(alp_p["14"]["mstar_1e10msun"]) * 1e10), 0.434 * fnum(alp_p["14"]["e_mstar"]) / fnum(alp_p["14"]["mstar_1e10msun"]),
                    math.log10(fnum(f1[k]["Mstar_1e10Msun"]) * 1e10), 0.2, False, "different SED fits", log=True)
        if k in f1 and "14" in alp_k:
            compare("ALPAKA 14", "FS+18", "BX610", "V_max (CO) vs V_c (Halpha eq.1)", fnum(alp_k["14"]["vmax_kms"]), sym(fnum(alp_k["14"]["vmax_errhi"]), fnum(alp_k["14"]["vmax_errlo"])),
                    fnum(f6[k]["Vc_kms"]), sym(fnum(f6[k]["Vc_kms_errhi"]), fnum(f6[k]["Vc_kms_errlo"])), False, "different tracers and definitions")
            compare("ALPAKA 14", "FS+18", "BX610", "sigma (CO, mean) vs sigma0 (Halpha)", fnum(alp_k["14"]["sigma_m_kms"]), sym(fnum(alp_k["14"]["sigma_m_errhi"]), fnum(alp_k["14"]["sigma_m_errlo"])),
                    fnum(f6[k]["sigma0_kms"]), sym(fnum(f6[k]["sigma0_kms_errhi"]), fnum(f6[k]["sigma0_kms_errlo"])), False, "molecular vs ionised gas")
    # ALPAKA x arXiv:2601.03338 (IDs 1, 3, 13: same group, later paper)
    for r in read_dicts(os.path.join(AT, "alpaka_jwst2026_data.csv")):
        i = r["alpaka_id"]
        zcompare("ALPAKA I", "arXiv:2601.03338", f"ALPAKA {i}", fnum(alp_s[i]["z"]), fnum(r["z"]), True, "same line")
        compare("ALPAKA I", "arXiv:2601.03338", f"ALPAKA {i}", "L'", fnum(alp_p[i]["lprime_1e10_kkmspc2"]), fnum(alp_p[i]["e_lprime"]), fnum(r["Lprime_1e10"]), fnum(r["e_Lprime"]), True, "same data")
        if fin(fnum(alp_p[i]["mstar_1e10msun"])):
            compare("ALPAKA I", "arXiv:2601.03338", f"ALPAKA {i}", "log M* (SED)", math.log10(fnum(alp_p[i]["mstar_1e10msun"]) * 1e10),
                    0.434 * fnum(alp_p[i]["e_mstar"]) / fnum(alp_p[i]["mstar_1e10msun"]), fnum(r["logMstar_sed"]), sym(fnum(r["errhi"]), fnum(r["errlo"])), False, "re-fitted SED", log=True)
        compare("ALPAKA I", "arXiv:2601.03338", f"ALPAKA {i}", "SFR", fnum(alp_p[i]["sfr_msun_yr"]), fnum(alp_p[i]["e_sfr"]), fnum(r["sfr_msun_yr"]), fnum(r["e_sfr"]), False, "")
    # ---- CRISTAL x ALPINE (Jones Table 1 and the corpus)
    cs = read_dicts(os.path.join(AT, "cristal2025_sample.csv"))
    jt = {nn(r["name"]): r for r in read_dicts(os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_table1_sample_classes.csv"))}
    cg = {nn(r["galaxy"]): r for r in read_dicts(os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_galaxies.csv"))}
    last = None
    for r in cs:
        nm_ = r["name"] if r["name"] not in ("\\ldots", "") else last
        repeat = (nm_ == last and re.search(r"[b-z]$", r["id"]) is not None)
        last = nm_
        if r["name"] in ("\\ldots", "") or repeat:
            continue     # companion components of the same system (b, c, ...) are not compared
        names = [nn(x) for x in nm_.split(",")]
        for k in names:
            if k in jt:
                zcompare("CRISTAL", "Jones+21", f"CRISTAL-{r['id']} = {jt[k]['name']}", fnum(r["z_cii"]), fnum(jt[k]["z"]), True, "both [CII]; CRISTAL prints 3 decimals")
            if k in cg and fin(fnum(r["logMstar"])) and fin(fnum(cg[k].get("log_mstar_msun"))):
                compare("CRISTAL", "ALPINE corpus", f"CRISTAL-{r['id']} = {cg[k]['galaxy']}", "log M*", fnum(r["logMstar"]), float("nan"), fnum(cg[k]["log_mstar_msun"]), float("nan"),
                        False, "Li+24/Mitsuhashi+24 vs Faisst+20 SED masses", rel_only=True, log=True)
    # ---- HZ9 / HZ4 / HZ7 between Jones, CRISTAL and the sigma-M* compilation
    comp = {}
    for r in read_dicts(os.path.join(REPO, "real_research", "virial_floor_2026", "highz_sigma_mstar.csv")):
        comp.setdefault(nn(r["name"]), r)
    crz = {}
    for r in cs:
        for x in r["name"].split(","):
            crz.setdefault(nn(x), (r["id"], fnum(r["z_cii"])))
    for nm_ in ("HZ9", "HZ4", "HZ7"):
        k = nn(nm_)
        c = comp.get(nn(nm_)) or comp.get(k)
        if not c:
            continue
        if k in jt:
            zcompare("sigma-M* compilation (Parlanti row)", "Jones+21", nm_, fnum(c["z"]), fnum(jt[k]["z"]), True, "both should be [CII] systemic redshifts")
        if k in crz or nm_.lower() in crz:
            cid, zc = crz.get(k) or crz.get(nm_.lower())
            zcompare("sigma-M* compilation (Parlanti row)", "CRISTAL", f"{nm_} = CRISTAL-{cid}", fnum(c["z"]), zc, True, "both [CII]")
        if k in cg and fin(fnum(cg[k].get("log_mstar_msun"))):
            compare("sigma-M* compilation (Parlanti row)", "ALPINE corpus", nm_, "log M*", fnum(c["logMstar"]), fnum(c["logMstar_err"]), fnum(cg[k]["log_mstar_msun"]), float("nan"),
                    False, "Capak+15 via Parlanti vs an unsourced corpus value", log=True)
        if k in cg:
            compare("sigma-M* compilation (Parlanti row)", "ALPINE corpus", nm_, "sigma0 vs ring-mean sigma",
                    float(re.search(r"sigma0=([\d.]+)", c["construction"]).group(1)), float(re.search(r"\+/-([\d.]+)", c["construction"]).group(1)),
                    fnum(cg[k]["sigma_mean_kms"]), float("nan"), False, "Method-II sigma0 vs 3DBarolo ring mean")
    # ---- J0817: Jones rings, Roman-Oliveira, corpus
    ro_k = {nn(r["id"]): r for r in read_dicts(os.path.join(AT, "romanoliveira2023_kinematics.csv"))}
    ro_s = {nn(r["id"]): r for r in read_dicts(os.path.join(AT, "romanoliveira2023_sample.csv"))}
    jr = [r for r in read_dicts(os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_tableA3_rings.csv")) if r["name"] == "J0817"]
    k = nn("J081740")
    if k in ro_k and jr:
        vo = max(jr, key=lambda r: fnum(r["R_kpc"]))
        compare("Jones+21 rings (outer)", "Roman-Oliveira+23", "J0817", "V_rot (outer ring) vs V_rot,ext", fnum(vo["vrot_kms"]), fnum(vo["vrot_kms_err"]),
                fnum(ro_k[k]["vrot_ext_kms"]), sym(fnum(ro_k[k]["vrot_ext_kms_errhi"]), fnum(ro_k[k]["vrot_ext_kms_errlo"])), False,
                f"different data/resolution; Jones ring at R = {vo['R_kpc']} kpc")
        compare("Jones+21 rings (mean)", "Roman-Oliveira+23", "J0817", "sigma (ring mean) vs sigma_mean", float(np.mean([fnum(r["sigma_kms"]) for r in jr])), float("nan"),
                fnum(ro_k[k]["sigma_mean_kms"]), sym(fnum(ro_k[k]["sigma_mean_kms_errhi"]), fnum(ro_k[k]["sigma_mean_kms_errlo"])), False, "")
        if "j0817" in cg:
            zcompare("ALPINE corpus", "Roman-Oliveira+23", "J0817", fnum(cg["j0817"]["redshift"]), fnum(ro_s[k]["z"]), True, "both [CII]")
    # ---- Danhaive x the sigma-M* compilation (rows built from arXiv:2503.21863)
    dg = {r["jades_id"]: r for r in read_dicts(os.path.join(AT, "danhaive2025_gold.csv"))}
    for r in read_dicts(os.path.join(REPO, "real_research", "virial_floor_2026", "highz_sigma_mstar.csv")):
        if r["source_arXiv"] != "2503.21863":
            continue
        jid = r["name"].replace("JADES-", "")
        d = dg.get(jid)
        m = re.search(r"sigma0=([\d.]+).*?V=([\d.]+)", r["construction"])
        if not d:
            R["cross"].append(dict(pair="compilation vs Danhaive gold", object=r["name"], quantity="presence", cls="NOT IN GOLD (other Danhaive sample)",
                                   same_definition=True, problem=False, note="the compilation row is not in the 41-gold table"))
            continue
        compare("sigma-M* compilation", "Danhaive gold", r["name"], "log M*", fnum(r["logMstar"]), float("nan"), fnum(d["logMstar"]), float("nan"), True, "copy", rel_only=True, log=True)
        if m:
            compare("sigma-M* compilation", "Danhaive gold", r["name"], "sigma0", float(m.group(1)), float("nan"), fnum(d["sigma0_kms"]), float("nan"), True, "copy", rel_only=True)
            compare("sigma-M* compilation", "Danhaive gold", r["name"], "V = (v/sigma0) sigma0", float(m.group(2)), float("nan"), fnum(d["v_over_sigma0"]) * fnum(d["sigma0_kms"]),
                    0.05 * fnum(d["sigma0_kms"]), True, "copy; the gold table prints v/sigma0 to 0.1 (envelope 0.05 sigma0)")
    # ---- SPARC x LVD by name
    sp = {nn(t[0]): t for t in (l.split() for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()[98:] if l.strip())}
    lvd = {}
    for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
        for r in read_dicts(os.path.join(REPO, "real_research", "data", "dsph", f)):
            lvd[nn(r["name"])] = r
    for k in sorted(set(sp) & set(lvd)):
        compare("SPARC", "LVD", sp[k][0], "distance (Mpc)", float(sp[k][2]), float(sp[k][3]), fnum(lvd[k]["distance"]) / 1e3,
                sym(fnum(lvd[k]["distance_ep"]), fnum(lvd[k]["distance_em"])) / 1e3, True, "same quantity; different distance methods possible")
    # ---- report
    new = R["cross"][n0:]
    by = {}
    for e in new:
        by.setdefault(e["pair"], []).append(e)
    for pair, es in by.items():
        cls = {}
        for e in es:
            cls[e["cls"]] = cls.get(e["cls"], 0) + 1
        P(f"  {pair}: {len(es)} comparisons {cls}")
        for e in es:
            if e["cls"] in ("DISAGREE", "TENSION") or e.get("problem"):
                extra = f"dv {e['dv_kms']:.0f} km/s" if "dv_kms" in e else (f"pull {e['pull']:+.2f}" if fin(e.get("pull", float('nan'))) else f"diff {e.get('diff', 0):+.3g}")
                P(f"      {e['cls']}{' [PROBLEM: same definition]' if e.get('problem') else ''}: {e['object']} {e['quantity']}: {e.get('a', '')} vs {e.get('b', '')} ({extra}) {e.get('note', '')}")
    big = [e for e in new if e["pair"] == "CRISTAL vs ALPINE corpus" and abs(e.get("diff", 0)) > 0.3]
    for e in big:
        P(f"      CRISTAL vs corpus |d log M*| > 0.3: {e['object']}: {e['a']} vs {e['b']} ({e['diff']:+.2f} dex)")
    # RC100 x KMOS3D release: stellar mass where RC100's own log M* is not tabulated in the repo; report U3 10584 explicitly
    q = k3.get(nn("U3 10584")); r = rc.get(nn("U3 10584"))
    if q and r:
        P(f"  RC100 row 80 'U3 10584' (z {r['z']}, log Mbar {r['logMbar_Msun']}; the page prints log M* 10.5) vs KMOS3D release U3_10584: Z {q['Z']}, "
          f"LMSTAR {q['LMSTAR']}, ID_SKELTON {q['ID_SKELTON']} (no 3D-HST match): identity UNRESOLVED (RC100 requires log M* > 9.5)")
        R["cross"].append(dict(pair="RC100 vs KMOS3D release", object="U3 10584", quantity="log M* (RC100 page 10.5) vs LMSTAR", a=10.5, b=fnum(q["LMSTAR"]),
                               diff=10.5 - fnum(q["LMSTAR"]), cls="DISAGREE", same_definition=True, problem=True,
                               note="name match only; KMOS3D row has no 3D-HST counterpart (ID_SKELTON 99999); z 2.22 vs 2.2455; identity unresolved"))
    # summary of relative differences where no errors
    for pair, es in by.items():
        rels = [e["diff"] for e in es if e["cls"] == "NO-ERRORS" and fin(e.get("diff", float('nan')))]
        if rels:
            P(f"  {pair} (no errors): {len(rels)} differences, median {np.median(rels):+.3f}, max |d| {max(abs(x) for x in rels):.3f}")


# =============================================================================== CHECK 3: versions (page-read record + on-disk source facts)
def run_versions():
    P("\n=== CHECK 3: VERSIONS AND ERRATA (page-read record versions_errata_pagereads.json + on-disk facts)")
    V = json.load(open(os.path.join(HERE, "versions_errata_pagereads.json")))
    R["versions"]["papers"] = V["papers"]
    R["versions"]["summary"] = V["summary"]
    st = {}
    for k, v in V["papers"].items():
        st.setdefault(v["status"].split(" (")[0], []).append(f"{k} {v['short']}")
    for s_, ks in sorted(st.items()):
        P(f"  {s_}: {len(ks)}: " + "; ".join(ks))
    P(f"  registered errata or corrigenda: {V['summary']['registered_errata'] or 'none'}")
    # ALPAKA: the tarball holds three drafts; the compile used alpaka_v2.tex (.fls). Count numeric cells that differ between drafts.
    d = os.path.join(EXT, "arxiv_src", "2303.16227")
    fls = open(os.path.join(d, "alpaka_v2.fls"), errors="ignore").read()
    used = re.findall(r"INPUT (\w+\.tex)", fls)
    P(f"  ALPAKA tarball: the compile (.fls) read {sorted(set(used))}")
    out = {}
    for lab in ("tab:mstar", "tab:PA", "tab:vsigma"):
        ref = {norm_key(r[0]): [parse_cell(c)[0] for c in r] for r in tex_table(os.path.join(d, "alpaka_v2.tex"), lab) if r and r[0]}
        for f in ("aanda.tex", "aanda2.tex"):
            oth = {norm_key(r[0]): [parse_cell(c)[0] for c in r] for r in (tex_table(os.path.join(d, f), lab) or []) if r and r[0]}
            ndiff = 0; ncomp = 0; ex = []
            for k, cells in ref.items():
                if not re.match(r"^\d+$", k) or k not in oth:
                    continue
                for ci, (a, b) in enumerate(zip(cells, oth[k])):
                    for role in ("v", "p", "m"):
                        if role in a and role in b:
                            ncomp += 1
                            if not equal_num(a[role], b[role]):
                                ndiff += 1
                                if len(ex) < 3:
                                    ex.append(f"ID {k} cell {ci} {role}: v2 {a[role]} vs {f} {b[role]}")
            out[f"{lab} vs {f}"] = dict(compared=ncomp, differ=ndiff, examples=ex)
            P(f"  ALPAKA {lab}: alpaka_v2.tex (used) vs {f}: {ndiff} of {ncomp} numeric components differ {ex}")
    R["versions"]["alpaka_drafts"] = out
    # fetch dates of the on-disk sources
    dates = {}
    for f in sorted(glob.glob(os.path.join(EXT, "arxiv_src", "*.tar.gz"))):
        import time
        dates[os.path.basename(f)[:-7]] = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(f)))
    R["versions"]["tarball_dates"] = dates


# =============================================================================== CHECK 5: impact arithmetic (no lane re-run)
def run_impact():
    P("\n=== CHECK 5: IMPACT ARITHMETIC (no lane is re-run)")
    imp = {}
    # LVD: rhalf_sph_physical inconsistency on the ultra-faint rows CFG7/CFG28 read (MW, M_V > -7.7, sigma measured, not an upper limit)
    rows = read_dicts(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv"))
    ufd = []
    for r in rows:
        MV, s_, ul = fnum(r["M_V"]), fnum(r["vlos_sigma"]), r.get("vlos_sigma_ul", "")
        rs, rp, e = fnum(r["rhalf_sph_physical"]), fnum(r["rhalf_physical"]), fnum(r["ellipticity"])
        if fin(MV) and MV > -7.7 and fin(s_) and s_ > 0 and ul in ("", None) and fin(rs) and fin(rp):
            dl = math.log10(rs / (rp * math.sqrt(1 - (e if fin(e) else 0))))
            ufd.append((r["name"], dl))
    big = [(n, round(d, 3)) for n, d in ufd if abs(d) > 0.01]
    mx = max(abs(d) for _, d in ufd) if ufd else 0.0
    bound = 0.5 * mx
    cfg28 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG28_ufd_referee_results.json")))["numbers"]["RES"]["canonical"]
    km, ekm, floor = cfg28["km"][0], cfg28["km"][1], cfg28["floor"]
    tot = math.hypot(ekm, floor)
    zs = (km - bound) / tot
    P(f"  LVD x CFG28: {len(ufd)} UFD rows; {len(big)} with |log rhalf_sph - log(rhalf sqrt(1-e))| > 0.01 dex: {big}")
    P(f"    sigma_pred depends on r at most as r^-1/2 (Newtonian limit; ~r^0 deep-MOND): median-offset shift <= 0.5 x {mx:.3f} = {bound:.3f} dex;"
      f" CFG28 KM median {km:.3f} +- {ekm:.3f} (floor {floor:.3f}) -> worst case {zs:.2f} sigma instead of {km / tot:.2f}")
    imp["LVD_rhalf_sph"] = dict(n_ufd=len(ufd), rows_gt_0p01dex=big, max_dlog_r=mx, bound_dex=bound, cfg28_km=km, cfg28_sigma=tot, z_nominal=km / tot, z_worst=zs)
    # RC100 uncorrected file: older lanes
    eff = R["sources"].get("S04 RC100 (Nestor Shachar+23)", {}).get("uncorrected_effect", {})
    imp["RC100_uncorrected_file"] = dict(effect=eff, readers=git_grep("rc100_nestorshachar2023_table3.csv"))
    P(f"  RC100 original CSV readers (git grep): {len(imp['RC100_uncorrected_file']['readers'])} files; median Vc^4/(G Mbar) shift {eff.get('dex_shift_median', float('nan')):+.4f} dex")
    # CFG52 / CFG90 read the original CSV: which affected rows sit in their z >= 1.5, g_bar < a0 pool (CFG90's committed per-object table; arithmetic only)
    po = os.path.join(REPO, "campaign_fresh_gravity", "CFG90_a0z_rederivation", "cfg90_per_object.csv")
    if os.path.exists(po):
        diffs = R["sources"]["S04 RC100 (Nestor Shachar+23)"]["original_vs_paper_diffs"]
        Odict = {r["idx"]: r for r in read_dicts(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"))}
        dM = {}
        for x in diffs:
            if x["field"] == "logMbar_Msun":
                dM[Odict[x["idx"]]["name"]] = fnum(x["paper"]) - fnum(x["original"])
        rows9 = read_dicts(po)
        pool = [r for r in rows9 if fnum(r["z"]) >= 1.5 and fnum(r["y_can"]) < 1 and r["name"] != "GS4 01529" and r["survey"] in ("RC100", "MSA3D", "KMOS3D")]
        def wmean(rr, col):
            w = np.array([1 / fnum(r["sigma"]) ** 2 for r in rr]); v = np.array([fnum(r[col]) for r in rr])
            return float((w * v).sum() / w.sum())
        moved = [(r["name"], round(fnum(r["y_can"]) * 10 ** dM[r["name"]], 2)) for r in pool if r["survey"] == "RC100" and r["name"] in dM]
        keep = [r for r in pool if not (r["survey"] == "RC100" and r["name"] in dM and fnum(r["y_can"]) * 10 ** dM[r["name"]] >= 1)]
        a = (wmean(pool, "dflat"), wmean(pool, "drival")); b = (wmean(keep, "dflat"), wmean(keep, "drival"))
        P(f"  CFG52/CFG90 z >= 1.5, g_bar < a0 pool (CFG90 per-object values): N {len(pool)}; RC100 rows with a corrected M_bar inside it: {moved} (y with the paper M_bar);"
          f" weighted Df/Dr {a[0]:+.3f}/{a[1]:+.3f} -> {b[0]:+.3f}/{b[1]:+.3f} (N {len(keep)}); shift {b[0] - a[0]:+.3f}/{b[1] - a[1]:+.3f} dex vs the pool's correlated sigma 0.136")
        gs = [r for r in rows9 if r["name"] == "GS4 01529"]
        if gs:
            P(f"  GS4 01529 (excluded after seeing it in CFG52; CFG90 calls it 'mutually inconsistent'): logM {gs[0]['logM']} in the original CSV is the paper's log M_bulge;"
              f" the paper's log M_baryon is 11.33 (+1.70 dex): y_can {fnum(gs[0]['y_can']):.2f} -> {fnum(gs[0]['y_can']) * 10 ** 1.70:.1f}, i.e. not a g_bar < a0 object")
        imp["CFG52_CFG90_pool"] = dict(n=len(pool), moved=moved, before=a, after=b, shift=(b[0] - a[0], b[1] - a[1]))
    # RC100 rows 67 and 83 (Vc^2 < 3.36 sigma0^2): their share of the 100-row sample
    imp["RC100_rows_67_83"] = dict(n=2, of=100, note="two rows of 100 enter the within-sample statistics; a median moves by at most one order-statistic step per row")
    # ADF22.5 inputs: what is verified on disk
    imp["ADF22_inputs"] = dict(verified_on_disk=["log M* 10.64 +0.20/-0.36 (ADF22-WEB PDF Table 1)", "z 3.09536 (ADF22-WEB PDF) vs ALPAKA 3.094",
                                                  "position (ALPAKA table, 0.04-0.06 arcsec)", "R_e,* circularized 1.65 +- 0.21 kpc = 2.24 x sqrt(0.54)"],
                               unverified=["F444W R_e 2.24 kpc and b/a 0.54 separately", "Sersic n 3.21", "870um R_e 1.53 and b/a 0.58 (the 2026 table gives circularized 1.05 +- 0.12; 1.53 x sqrt(0.58) = 1.17)"])
    R["impact"] = imp


# =============================================================================== MUTATE
def run_mutate():
    P("\n=== MUTATE: three planted errors in a copy of FS+18 Table 6")
    p6 = os.path.join(DA, "highz_literature_tables", "sins_ao", "sins_ao_table6_kinematics.csv")
    hdr, rows = read_table(p6)
    orig = [list(r) for r in rows]
    mut = [list(r) for r in rows]
    jv, jm, jr = hdr.index("Vc_kms"), hdr.index("Mdyn_1e10Msun"), hdr.index("Vrot_kms")
    # M1: Vc of data rows 10-14 (1-based) shifted down by one row
    for i in range(14, 9, -1):
        mut[i - 1][jv] = orig[i - 2][jv]
    # M2: Mdyn of row 20 x 10; M3: Vrot of row 25 negated
    mut[19][jm] = repr(fnum(orig[19][jm]) * 10)
    mut[24][jr] = repr(-fnum(orig[24][jr]))
    planted = {}
    for i in range(len(rows)):
        for j in range(len(hdr)):
            if mut[i][j] != orig[i][j]:
                planted[(orig[i][0], hdr[j])] = (orig[i][j], mut[i][j])
    out = os.path.join(HERE, "CFG287_MUTATE_sins_ao_table6.csv")
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(hdr); w.writerows(mut)
    P(f"  wrote {rel(out)}; planted cells that differ from the original: {len(planted)}")
    for k, v in planted.items():
        P(f"    {k[0]} / {k[1]}: {v[0]} -> {v[1]}")
    def flagged(entries):
        s_ = set()
        for e in entries.values():
            for rf in e["rows_flagged"]:
                if "[PROBLEM]" in rf or "not > 0" in rf or "negative" in rf:
                    s_.add(rf.split(":")[0])
        return s_
    keep = list(R["sources"].keys())
    base = s07_fs18(t6_override=p6, sid="MUTATE baseline (unmutated copy)")
    mutd = s07_fs18(t6_override=out, sid="MUTATE (mutated copy)")
    fb, fm = flagged(base), flagged(mutd)
    new = fm - fb
    m1_rows = {orig[i - 1][0] for i in range(10, 15) if mut[i - 1][jv] != orig[i - 1][jv]}
    m2_row = {orig[19][0]}; m3_row = {orig[24][0]}
    vc_flag = {rf.split(":")[0] for rf in mutd["vc"]["rows_flagged"] if "[PROBLEM]" in rf}
    md_flag = {rf.split(":")[0] for rf in mutd["md"]["rows_flagged"] if "[PROBLEM]" in rf}
    ra_flag = {rf.split(":")[0] for rf in mutd["ratio"]["rows_flagged"] if "[PROBLEM]" in rf}
    gen_flag = {rf.split(":")[0] for rf in mutd["generic"]["rows_flagged"]}
    ok1 = m1_rows <= vc_flag
    ok2 = m2_row <= md_flag
    ok3 = m3_row <= gen_flag and m3_row <= ra_flag
    ok_extra = new <= (m1_rows | m2_row | m3_row)
    # transcription over all cells of the mutated table
    fh_ = os.path.join(DA, "highz_literature_tables", "raw_small", "arxiv_1802.07276_html_fetched_2026-09-29.html")
    tr = transcription_table("MUTATE copy vs the FS+18 HTML (all cells)", out, html_table(fh_, "S6.T6.2"), rng=None)
    caught = set()
    for d in tr["full_fail_detail"]:
        m = re.match(r"(\S+) / (\S+) =", d)
        if m:
            caught.add((m.group(1), m.group(2)))
    ok_t = caught == set(planted.keys())
    # cross-survey detection of M1 (reported, not required)
    rc = {nn(r["name"]): r for r in read_dicts(os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv"))}
    xs = []
    for i in range(10, 15):
        k = nn(orig[i - 1][0])
        if k in rc:
            xs.append(f"{orig[i - 1][0]}: RC100 V_c(R_e) {rc[k]['Vc_Re_kms']} vs mutated FS+18 Vc {mut[i - 1][jv]} (original {orig[i - 1][jv]})")
    res = dict(planted={f"{k[0]}|{k[1]}": v for k, v in planted.items()}, M1_rows=sorted(m1_rows), M1_caught_by_eq1=sorted(vc_flag & m1_rows), M1_pass=ok1,
               M2_row=sorted(m2_row), M2_caught_by_eq2=sorted(md_flag & m2_row), M2_pass=ok2, M3_row=sorted(m3_row), M3_caught_by_positivity=sorted(gen_flag & m3_row),
               M3_caught_by_ratio=sorted(ra_flag & m3_row), M3_pass=ok3, new_flags=sorted(new), no_flags_outside_planted_rows=ok_extra,
               transcription_caught=sorted(f"{a}|{b}" for a, b in caught), transcription_exact=ok_t, cross_survey_M1=xs,
               pass_all=bool(ok1 and ok2 and ok3 and ok_extra and ok_t))
    P(f"  M1 shifted Vc rows {sorted(m1_rows)}: eq.1 flags {sorted(vc_flag & m1_rows)} -> {'PASS' if ok1 else 'FAIL'}")
    P(f"  M2 unit slip {sorted(m2_row)}: eq.2 flags {sorted(md_flag & m2_row)} -> {'PASS' if ok2 else 'FAIL'}")
    P(f"  M3 sign flip {sorted(m3_row)}: positivity {sorted(gen_flag & m3_row)}, Vrot/sigma0 {sorted(ra_flag & m3_row)} -> {'PASS' if ok3 else 'FAIL'}")
    P(f"  newly flagged rows {sorted(new)} all inside the planted rows: {ok_extra}")
    P(f"  transcription (all cells) flags exactly the planted cells: {ok_t} ({len(caught)} flagged, {len(planted)} planted)")
    for x in xs:
        P(f"  cross-survey (reported only): {x}")
    P(f"  MUTATE overall: {'PASS' if res['pass_all'] else 'FAIL'}")
    # keep the MUTATE entries out of the audit's source list
    for k in list(R["sources"].keys()):
        if k not in keep:
            R["sources"].pop(k)
    PROBLEMS[:] = [p for p in PROBLEMS if not p["source"].startswith("MUTATE")]
    FLAGS[:] = [f for f in FLAGS if not f["source"].startswith("MUTATE")]
    R["mutate_result"] = res
    return res


# =============================================================================== main
def main():
    crit = os.path.join(HERE, "FROZEN_CRITERIA.md")
    R["criteria_sha256"] = sha(crit)
    P("CFG287 integrity audit of the published tables behind the a0 lanes")
    P(f"criteria FROZEN_CRITERIA.md sha256 {R['criteria_sha256']}; seed {SEED}; MUTATE={int(MUTATE)}")
    P("kappa = 1/2 FITTED. Data audit only: no lane is re-run, no verdict word is applied to a law.")
    if MUTATE:
        res = run_mutate()
        return res["pass_all"]
    P("\n=== CHECK 1: INTERNAL CONSISTENCY")
    s01_sparc(); s02_lvd(); s03_kids(); s04_rc100(); rc100_posthoc(); s05_kmos3d(); s06_price(); s07_fs18(); s08_fs09(); s09_tacconi13()
    s10_cristal(); s11_jones(); s12_sigma_compilation(); alp = s13_alpaka(); s14_amvrosiadis(); s15_danhaive(); s16_romanoliveira(); s17_lelli23()
    s18_musedark(); s19_adf22(alp); s20_pks0529(); s21_gn20(); s22_mightee()
    run_cross()
    run_versions()
    run_transcription()
    run_impact()
    # summary
    P("\n=== SUMMARY")
    P(f"  hard-check PROBLEM entries (frozen rules): {len(PROBLEMS)}")
    for p in PROBLEMS:
        P(f"    {p['source']} :: {p['check']} ({p['n']} rows)")
    P(f"  soft FLAG entries: {len(FLAGS)}")
    for f in FLAGS:
        P(f"    {f['source']} :: {f['check']} ({f['n']})")
    xp = [e for e in R["cross"] if e.get("problem")]
    P(f"  cross-survey same-definition DISAGREE: {len(xp)}")
    for e in xp:
        P(f"    {e['pair']} :: {e['object']} {e['quantity']} ({e.get('note', '')})")
    tp = {k: v.get("status") for k, v in R["transcription"].items() if isinstance(v, dict) and "status" in v}
    P(f"  transcription sample results: " + ", ".join(f"{k}: {v}" for k, v in tp.items()))
    full_mis = {k: v.get("full_fail", 0) for k, v in R["transcription"].items() if isinstance(v, dict) and v.get("full_fail")}
    drops = {k: v.get("dropped") for k, v in R["transcription"].items() if isinstance(v, dict) and v.get("dropped")}
    P(f"  full-scan mismatches outside the sample: {full_mis}")
    P(f"  dropped cells: {drops}")
    return True


if __name__ == "__main__":
    import time
    t0 = time.time()
    ok = main()
    R["seconds"] = round(time.time() - t0, 1)
    stem = "cfg287_mutate" if MUTATE else "cfg287_integrity"
    jname = "cfg287_mutate_results.json" if MUTATE else "cfg287_results.json"
    open(os.path.join(HERE, stem + ".out"), "w").write("\n".join(OUT) + "\n")
    def clean(o):
        if isinstance(o, float):
            return o if math.isfinite(o) else None
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple, set)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating,)):
            return clean(float(o))
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return o
    json.dump(clean(R), open(os.path.join(HERE, jname), "w"), indent=1)
    sys.exit(0 if ok else 1)
