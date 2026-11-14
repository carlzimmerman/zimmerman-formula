"""AGB3R loader: the DES-SN5YR Dovekie per-supernova metadata table, the distance file, samples, mu_fid and bins.

Run python with -I (the table is a downloaded file). Paths are relative to this folder; nothing is downloaded.
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
EXT = os.path.normpath(os.path.join(REPO, "..", "_external_data"))
META = os.path.join(EXT, "agb3_des_dovekie_metadata", "DES-Dovekie_Metadata.csv")
HD = os.path.join(EXT, "cfg684_inputs", "des5", "DES-Dovekie_HD.csv")
META_SHA256 = "45ad71f8470eaecfe2b386699ef66b26b0717c50f445d5f32941988d32c75388"
FLOATS = ("zHD", "zHEL", "MU", "MUERR_RENORM", "mB", "x1", "c", "biasCor_mu", "HOST_LOGMASS", "HOST_LOGsSFR",
          "HOST_COLOR", "PROBCC_BEAMS")
OM_FID = 0.330


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_snana(path):
    hdr, rows = None, []
    for line in open(path):
        if line.startswith("VARNAMES:"):
            hdr = line.split()[1:]
        elif line.startswith("SN:"):
            rows.append(line.split()[1:])
    if hdr is None:
        raise ValueError("no VARNAMES line")
    if any(len(r) != len(hdr) for r in rows):
        raise ValueError("ragged table")
    return hdr, rows


class Meta:
    """Columns of the metadata table (file order), as numpy arrays."""
    def __init__(s, path=META):
        hdr, rows = _read_snana(path)
        col = {h: i for i, h in enumerate(hdr)}
        s.n = len(rows)
        s.cid = np.array([r[col["CID"]] for r in rows])
        s.ids = np.array([int(r[col["IDSURVEY"]]) for r in rows])
        for k in FLOATS:
            setattr(s, k, np.array([float(r[col[k]]) for r in rows]))
        s.lm, s.ls, s.col, s.pcc = s.HOST_LOGMASS, s.HOST_LOGsSFR, s.HOST_COLOR, s.PROBCC_BEAMS
        s.L = (s.lm < 10.0).astype(float)                      # 1 for a low-mass host
        s.key = [f"{a}|{b}" for a, b in zip(s.cid, s.ids)]

    def sample(s, name):
        """Boolean selection (file order)."""
        des = s.ids == 10
        if name == "full": return np.ones(s.n, bool)
        if name == "des_only": return des
        if name == "pure": return des & (s.pcc <= 0.1)
        if name == "young": return s.ls >= -9.5
        if name == "old": return s.ls < -9.5
        if name == "young_des": return des & (s.ls >= -9.5)
        if name == "blue": return s.col <= 0.8
        if name == "ls10": return s.ls >= -10.0
        raise ValueError(name)


def read_hd(path=HD):
    """Distance file rows: CID, IDSURVEY, zHD, zHEL, MU, MUERR (file order = covariance order)."""
    hdr, rows = _read_snana(path)
    col = {h: i for i, h in enumerate(hdr)}
    out = dict(cid=np.array([r[col["CID"]] for r in rows]), ids=np.array([int(r[col["IDSURVEY"]]) for r in rows]))
    for k in ("zHD", "zHEL", "MU", "MUERR"):
        out[k] = np.array([float(r[col[k]]) for r in rows])
    out["key"] = [f"{a}|{b}" for a, b in zip(out["cid"], out["ids"])]
    return out


def hd_index(meta, hd):
    """For every distance-file row, the metadata row with the same (CID, IDSURVEY)."""
    pos = {k: i for i, k in enumerate(meta.key)}
    if len(pos) != meta.n:
        raise ValueError("duplicate (CID, IDSURVEY) in the metadata")
    return np.array([pos[k] for k in hd["key"]])


# ---------------- fiducial distance ----------------
_ZG = np.linspace(0.0, 1.3, 13001)


def mu_fid(zhd, zhel, om=OM_FID):
    e = np.sqrt(om*(1 + _ZG)**3 + 1 - om)
    dm = np.concatenate([[0.0], np.cumsum(0.5*(1/e[1:] + 1/e[:-1])*np.diff(_ZG))])
    return 5*np.log10((1 + zhel)*np.interp(zhd, _ZG, dm))


def bins(z, nb):
    """Equal-count bins by rank (stable sort): bin = floor(nb x rank / n)."""
    o = np.argsort(z, kind="stable"); b = np.empty(len(z), int)
    b[o] = (np.arange(len(z))*nb)//len(z)
    return b
