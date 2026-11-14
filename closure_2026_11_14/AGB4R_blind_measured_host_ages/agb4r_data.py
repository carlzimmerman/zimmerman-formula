"""AGB4R blind re-grade: loaders and cross-match (written from FROZEN_CRITERIA.md of AGB4 only).

Data paths are relative to the repository root's parent: ../_external_data/.
Nothing here fits a magnitude against an age.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
SAKO = os.path.join(EXT, "agb4_sako2018_master", "sdsssn_master.dat2")
ROSE_DIR = os.path.join(EXT, "agb4_rose2019_ages")
PP_DAT = os.path.join(EXT, "pantheonplus_dr", "PantheonPlusSH0ES.dat")
PP_COV = os.path.join(EXT, "pantheonplus_dr", "PantheonPlusSH0ES_STAT+SYS.cov")

OM_FID = 0.334
SLOPE = -0.030  # mag per Gyr; D_i = SLOPE * age_i
C_KMS = 299792.458
H0_FID = 70.0   # absorbed by the bin offsets


def _f(tok):
    if tok == "\\N":
        return np.nan
    try:
        return float(tok)
    except ValueError:
        return np.nan


def load_sako():
    """Return dict of column arrays. Repeated header names: the FIRST occurrence of x0/x1/c/mu/muerr is the
    spectroscopic-redshift SALT2 fit (columns 16-28, 1-based); host columns are the last block (118-135)."""
    with open(SAKO) as fh:
        header = fh.readline().split()
        rows = [ln.split() for ln in fh if ln.strip()]
    ncol = len(header)
    assert ncol == 136, ncol
    for r in rows:
        assert len(r) == ncol
    idx = {}
    for j, name in enumerate(header):
        idx.setdefault(name, j)  # first occurrence
    def col(name, j=None, num=True):
        jj = idx[name] if j is None else j
        if num:
            return np.array([_f(r[jj]) for r in rows])
        return np.array([r[jj] for r in rows])
    d = {}
    d["cid"] = np.array([int(r[0]) for r in rows])
    d["type"] = col("type_dr", num=False)
    d["z_hel"] = col("z_best_with_BOSS_HELIO")
    d["z_cmb"] = col("z_best_with_BOSS_CMB")
    # first SALT2 block (spec-z fit): 1-based columns 16..28 -> 0-based 15..27
    assert header[15] == "x0" and header[17] == "x1" and header[19] == "c" and header[24] == "muerr"
    d["x0"] = col(None, 15); d["x0err"] = col(None, 16)
    d["x1"] = col(None, 17); d["c"] = col(None, 19)
    d["mu"] = col(None, 23); d["muerr"] = col(None, 24)
    # host block (last): 0-based 117..134
    host_names = ["logMass_Ravi", "logMass_lo_Ravi", "logMass_hi_Ravi", "logSSFR_Ravi", "logSSFR_lo_Ravi",
                  "logSSFR_hi_Ravi", "age_Ravi", "age_lo_Ravi", "age_hi_Ravi", "minredchi2_Ravi", "logMass_Mat",
                  "logMass_lo_Mat", "logMass_hi_Mat", "logSFR_Mat", "logSFR_lo_Mat", "logSFR_hi_Mat", "age_Mat",
                  "minchi2_Mat"]
    for k, name in enumerate(host_names):
        assert header[117 + k] == name, (header[117 + k], name)
        d[name] = col(None, 117 + k)
    return d


def load_pantheon():
    with open(PP_DAT) as fh:
        header = fh.readline().split()
        rows = [ln.split() for ln in fh if ln.strip()]
    d = {"CID": np.array([r[0] for r in rows])}
    for j, name in enumerate(header[1:], start=1):
        d[name] = np.array([float(r[j]) for r in rows])
    d["row"] = np.arange(len(rows))
    return d


def load_pantheon_cov_diag(n_expected):
    with open(PP_COV) as fh:
        n = int(fh.readline())
        vals = np.array(fh.read().split(), dtype=float)
    assert n == n_expected and vals.size == n * n
    C = vals.reshape(n, n)
    return np.diag(C).copy()


def load_rose_summary():
    out = {}
    with open(os.path.join(ROSE_DIR, "results-summary.csv")) as fh:
        hdr = fh.readline()
        assert hdr.startswith("# sn id")
        for ln in fh:
            if not ln.strip():
                continue
            t = ln.strip().split(",")
            out[int(t[0])] = dict(local=float(t[1]), local_unc=float(t[2]), glob=float(t[3]),
                                  glob_unc=float(t[4]), mass=float(t[5]), pc1=float(t[6]))
    return out


def load_tsv(name):
    with open(os.path.join(ROSE_DIR, name)) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        rows = [ln.rstrip("\n").split("\t") for ln in fh if ln.strip()]
    d = {}
    for j, h in enumerate(header):
        vals = [r[j] for r in rows]
        try:
            d[h] = np.array([float(v) for v in vals])
        except ValueError:
            d[h] = np.array(vals)
    return d


def _dc_over(z, om):
    return quad(lambda x: 1.0 / np.sqrt(om * (1 + x) ** 3 + 1 - om), 0.0, z, epsabs=1e-12, epsrel=1e-12)[0]


def mu_flat(z_hd, z_hel, om):
    """Flat LCDM distance modulus, Pantheon+ convention D_L = (1 + z_hel) * D_C(z_hd)."""
    z_hd = np.atleast_1d(z_hd); z_hel = np.atleast_1d(z_hel)
    dc = np.array([_dc_over(z, om) for z in z_hd]) * C_KMS / H0_FID
    dl = (1 + z_hel) * dc
    return 5 * np.log10(dl) + 25.0


def equal_count_bins(z, nb, tiebreak):
    """Bin index 0..nb-1 by rank in z (ties broken by tiebreak key): bin = floor(rank * nb / N)."""
    order = np.lexsort((tiebreak, z))
    rank = np.empty(len(z), dtype=int)
    rank[order] = np.arange(len(z))
    return (rank * nb) // len(z)


def build_samples():
    """Return dict of samples. Each sample: dict of arrays aligned row by row."""
    S = load_sako()
    P = load_pantheon()
    diag = load_pantheon_cov_diag(len(P["CID"]))
    sako_by_cid = {c: i for i, c in enumerate(S["cid"])}
    assert len(sako_by_cid) == len(S["cid"])

    sdss = np.where(P["IDSURVEY"] == 1)[0]
    found = []
    for r in sdss:
        cid = P["CID"][r]
        try:
            k = sako_by_cid[int(cid)]
        except (ValueError, KeyError):
            k = -1
        found.append(k)
    found = np.array(found)

    match = dict(n_sdss=len(sdss), n_found=int((found >= 0).sum()))
    ok = found >= 0
    m_rows = sdss[ok]; m_sako = found[ok]

    def pp_arrays(rows, ks):
        a = {}
        a["cid"] = S["cid"][ks]
        a["zHD"] = P["zHD"][rows]; a["zHEL"] = P["zHEL"][rows]
        a["z_tab_cmb"] = S["z_cmb"][ks]; a["z_tab_hel"] = S["z_hel"][ks]
        a["mB"] = P["mB"][rows]; a["m_b_corr"] = P["m_b_corr"][rows]
        a["x1"] = P["x1"][rows]; a["c"] = P["c"][rows]
        a["Cii"] = diag[rows]
        a["mass_pp"] = P["HOST_LOGMASS"][rows]
        a["mass_fsps"] = S["logMass_Ravi"][ks]
        a["age"] = S["age_Ravi"][ks]; a["age_lo"] = S["age_lo_Ravi"][ks]; a["age_hi"] = S["age_hi_Ravi"][ks]
        a["age_mat"] = S["age_Mat"][ks]
        a["x1_tab"] = S["x1"][ks]
        a["pp_row"] = rows
        return a

    allm = pp_arrays(m_rows, m_sako)
    has_age = np.isfinite(allm["age"]) & np.isfinite(allm["age_lo"]) & (allm["age_lo"] > 0)
    pp = {k: v[has_age] for k, v in allm.items()}
    pp["L"] = (pp["mass_pp"] < 10).astype(float)
    pp["mu_fid"] = mu_flat(pp["zHD"], pp["zHEL"], OM_FID)
    pp["w"] = 1.0 / pp["Cii"]
    pp["z"] = pp["zHD"]

    # rose: pp rows with a Rose et al. (2019) entry
    R = load_rose_summary()
    inr = np.array([c in R for c in pp["cid"]])
    rose = {k: v[inr] for k, v in pp.items()}
    rose["age_rose_global"] = np.array([R[c]["glob"] for c in rose["cid"]])
    rose["age_rose_local"] = np.array([R[c]["local"] for c in rose["cid"]])

    # big: SDSS-II SNIa / zSNIa with FSPS age, own SALT2 fit, |x1|<3, |c|<0.3, 0.03<z<0.45
    typ = S["type"]
    isIa = (typ == "SNIa") | (typ == "zSNIa")
    zc = S["z_cmb"]
    # positive lower age bound applied here too (age_lo = -99 flags a failed host fit); this reproduces the
    # criteria's design count 1,092 (387 spectroscopic); without it the count is 1,095 (389)
    sel_core = (isIa & np.isfinite(S["age_Ravi"]) & (S["age_lo_Ravi"] > 0)
                & np.isfinite(S["x0"]) & (S["x0"] > 0) & np.isfinite(S["x1"])
                & np.isfinite(S["c"]) & np.isfinite(S["muerr"]) & (np.abs(S["x1"]) < 3) & (np.abs(S["c"]) < 0.3)
                & (zc > 0.03) & (zc < 0.45))
    big = {}
    keys = dict(cid="cid", type="type", z_hel="z_hel", z_cmb="z_cmb", x0="x0", x1="x1", c="c", muerr="muerr",
                age="age_Ravi", age_lo="age_lo_Ravi", age_hi="age_hi_Ravi", mass_fsps="logMass_Ravi",
                age_mat="age_Mat")
    for k, v in keys.items():
        big[k] = S[v][sel_core]
    big["z"] = big["z_cmb"]
    big["L"] = (big["mass_fsps"] < 10).astype(float)
    big["mu_fid"] = mu_flat(big["z_cmb"], big["z_hel"], OM_FID)
    big["w"] = 1.0 / (big["muerr"] ** 2 + 0.1 ** 2)
    big["y"] = -2.5 * np.log10(big["x0"]) - big["mu_fid"]
    return dict(S=S, P=P, match=match, allm=allm, pp=pp, rose=rose, big=big, rose_summary=R)


def subset(sample, mask):
    return {k: (v[mask] if isinstance(v, np.ndarray) and v.shape[:1] == mask.shape else v)
            for k, v in sample.items()}
