"""AGB5R loaders (blind re-grade of AGB5). Own code; reads the tables beside the repository.

Data root: ../_external_data relative to the repository root (this file sits two levels below it).
Nothing here fits anything.
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
T1 = os.path.join(EXT, "agb5_chung2025_ages", "unpacked", "table1.dat")
T2 = os.path.join(EXT, "agb5_chung2025_ages", "unpacked", "table2.dat")
SAKO = os.path.join(EXT, "agb4_sako2018_master", "sdsssn_master.dat2")
PPD = os.path.join(EXT, "pantheonplus_dr", "PantheonPlusSH0ES.dat")
PPC = os.path.join(EXT, "pantheonplus_dr", "PantheonPlusSH0ES_STAT+SYS.cov")


def _num(s):
    return float(s.strip())


def load_chung(path, two_residuals):
    """Rows 'id & age & sig_age & HR [ (HR_orig) ] & sig_HR \\\\'. Returns dict of arrays."""
    ids, age, sage, hr, hro, shr = [], [], [], [], [], []
    with open(path) as f:
        lines = f.read().splitlines()
    for ln in lines:
        s = ln.strip()
        if not s or "&" not in s:
            continue
        s = s.replace("\\\\", "").strip()
        parts = [p.strip() for p in s.split("&")]
        if len(parts) != 5:
            raise ValueError("bad row: %r" % ln)
        if not parts[0].isdigit():
            continue  # header
        ids.append(int(parts[0]))
        age.append(_num(parts[1]))
        sage.append(_num(parts[2]))
        f3 = parts[3]
        if two_residuals:
            a, b = f3.split("(")
            hr.append(_num(a))
            hro.append(_num(b.replace(")", "")))
        else:
            if "(" in f3:
                raise ValueError("unexpected bracket in table 2: %r" % ln)
            hr.append(_num(f3))
            hro.append(np.nan)
        shr.append(_num(parts[4]))
    return dict(id=np.array(ids, dtype=int), age=np.array(age), sage=np.array(sage),
                hr=np.array(hr), hr_orig=np.array(hro), shr=np.array(shr))


def load_sako(ids_wanted=None):
    """Return {cid: dict(logmass, z_cmb, z_hel, type)} from the SDSS-II master table.
    Column names repeat; index by position. First x0/x1/c block = spectroscopic-redshift SALT2 fit."""
    with open(SAKO) as f:
        hdr = f.readline().split()
        n = len(hdr)
        idx = {}
        for i, h in enumerate(hdr):
            idx.setdefault(h, []).append(i)
        i_cid = idx["cid"][0]
        i_type = idx["type_dr"][0]
        i_zh = idx["z_best_with_BOSS_HELIO"][0]
        i_zc = idx["z_best_with_BOSS_CMB"][0]
        i_m = idx["logMass_Ravi"][0]
        i_age = idx["age_Ravi"][0]
        i_x1 = idx["x1"][0]
        i_c = idx["c"][0]
        out = {}
        for line in f:
            t = line.rstrip("\n").split(" ")
            if len(t) != n:
                raise ValueError("row with %d fields, header %d" % (len(t), n))
            cid = int(t[i_cid])
            if ids_wanted is not None and cid not in ids_wanted:
                continue

            def g(i):
                v = t[i]
                return np.nan if v == "\\N" else float(v)
            zh, zc = g(i_zh), g(i_zc)
            zh = zh if zh > 0 else np.nan  # -9 = no spectroscopic redshift
            zc = zc if zc > 0 else np.nan
            out[cid] = dict(type=t[i_type], z_hel=zh, z_cmb=zc, logmass=g(i_m),
                            age_ravi=g(i_age), x1=g(i_x1), c=g(i_c))
    return out


def load_pantheon():
    """Pantheon+ rows (dict of arrays, CID as string) and the diagonal of the STAT+SYS covariance."""
    with open(PPD) as f:
        hdr = f.readline().split()
        rows = [ln.split() for ln in f if ln.strip()]
    cols = {h: [r[i] for r in rows] for i, h in enumerate(hdr)}
    with open(PPC) as f:
        n = int(f.readline())
        flat = np.fromiter((float(x) for x in f.read().split()), dtype=float, count=n * n)
    if n != len(rows):
        raise ValueError("cov size %d vs %d rows" % (n, len(rows)))
    diag = flat.reshape(n, n).diagonal().copy()
    out = dict(CID=np.array(cols["CID"]), IDSURVEY=np.array(cols["IDSURVEY"], dtype=int))
    for k in ("zHD", "zHEL", "mB", "x1", "c", "HOST_LOGMASS", "m_b_corr"):
        out[k] = np.array(cols[k], dtype=float)
    out["Cii"] = diag
    return out


def tables():
    t1 = load_chung(T1, True)
    t2 = load_chung(T2, False)
    want = set(t1["id"].tolist()) | set(t2["id"].tolist())
    sk = load_sako(want)
    for t in (t1, t2):
        t["in_sako"] = np.array([i in sk for i in t["id"]])
        t["logmass"] = np.array([sk[i]["logmass"] if i in sk else np.nan for i in t["id"]])
        t["z"] = np.array([sk[i]["z_cmb"] if i in sk else np.nan for i in t["id"]])
        t["z_hel"] = np.array([sk[i]["z_hel"] if i in sk else np.nan for i in t["id"]])
        t["type"] = np.array([sk[i]["type"] if i in sk else "" for i in t["id"]])
        t["L"] = np.where(np.isfinite(t["logmass"]), (t["logmass"] < 10.0).astype(float), np.nan)
    return t1, t2


def subset(t, mask):
    return {k: (v[mask] if isinstance(v, np.ndarray) and v.shape[:1] == mask.shape else v) for k, v in t.items()}
