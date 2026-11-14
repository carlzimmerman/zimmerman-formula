"""AGB4 loaders (criteria: FROZEN_CRITERIA.md). Pantheon+ SDSS supernovae joined to the SDSS-II host table of
Sako et al. (2018) and to the Rose et al. (2019) ages, by SDSS supernova id."""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("AGB4_REPO") or os.path.normpath(os.path.join(HERE, "..", ".."))
EXT = os.path.normpath(os.path.join(REPO, "..", "_external_data"))
PP = os.path.join(EXT, "pantheonplus_dr")
SAKO = os.path.join(EXT, "agb4_sako2018_master", "sdsssn_master.dat2")
ROSE = os.path.join(EXT, "agb4_rose2019_ages")


def sako():
    """dict of arrays keyed by column name (host block and SALT2 block), one entry per SDSS-II candidate."""
    lines = open(SAKO).read().split("\n"); hdr = lines[0].split(); rows = [l.split() for l in lines[1:] if l.strip()]
    last = lambda name: max(i for i, n in enumerate(hdr) if n == name)       # repeated names: the host block is the last
    first = lambda name: min(i for i, n in enumerate(hdr) if n == name)      # the first x0, x1, c block is the spectroscopic-redshift SALT2 fit
    num = lambda i: np.array([np.nan if r[i] == "\\N" else float(r[i]) for r in rows])
    out = dict(cid=np.array([r[0] for r in rows]), type=np.array([r[hdr.index("type_dr")] for r in rows]), z=num(hdr.index("z_best_with_BOSS_CMB")))
    for n in ("logMass_Ravi", "logSSFR_Ravi", "age_Ravi", "age_lo_Ravi", "age_hi_Ravi", "logMass_Mat", "age_Mat"): out[n] = num(last(n))
    for n in ("x0", "x1", "c", "mu", "muerr"): out[n] = num(first(n))
    return out


def pantheon_sdss():
    """Pantheon+ rows of the SDSS survey (IDSURVEY 1) with the Sako host ages attached; diagonal of the covariance."""
    f = os.path.join(PP, "PantheonPlusSH0ES.dat"); hdr = open(f).readline().split(); raw = np.genfromtxt(f, skip_header=1, dtype=str)
    g = lambda n: raw[:, hdr.index(n)].astype(float)
    cov = np.fromfile(os.path.join(PP, "PantheonPlusSH0ES_STAT+SYS.cov"), sep=" "); n = int(cov[0]); var = np.diag(cov[1:].reshape(n, n))
    sel = g("IDSURVEY").astype(int) == 1; cid = raw[:, hdr.index("CID")][sel]
    S = sako(); pos = {c: i for i, c in enumerate(S["cid"])}; ix = np.array([pos.get(c, -1) for c in cid])
    out = dict(cid=cid, z=g("zHD")[sel], zh=g("zHEL")[sel], mcorr=g("m_b_corr")[sel], mB=g("mB")[sel], x1=g("x1")[sel], c=g("c")[sel],
               lm=g("HOST_LOGMASS")[sel], var=var[sel], matched=ix >= 0)
    for n in ("age_Ravi", "age_lo_Ravi", "age_hi_Ravi", "age_Mat", "logSSFR_Ravi", "logMass_Ravi", "z"):
        out["sako_" + n] = np.where(ix >= 0, S[n][np.maximum(ix, 0)], np.nan)
    rose = np.genfromtxt(os.path.join(ROSE, "results-summary.csv"), delimiter=",", skip_header=1)
    rp = {str(int(r[0])): r for r in rose}
    out["rose_local"] = np.array([rp[c][1] if c in rp else np.nan for c in cid]); out["rose_global"] = np.array([rp[c][3] if c in rp else np.nan for c in cid])
    return out
