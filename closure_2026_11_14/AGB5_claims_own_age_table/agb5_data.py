"""AGB5 loaders: the two host-age tables of Chung et al. (2025) and their match to the SDSS-II and Pantheon+ tables."""
import os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("AGB5_REPO") or os.path.normpath(os.path.join(HERE, "..", ".."))
os.environ.setdefault("AGB4_REPO", REPO)
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_14", "AGB4_measured_host_ages"))
import agb4_data as D4
CHUNG = os.path.join(D4.EXT, "agb5_chung2025_ages", "unpacked")


def table(which):
    """which = 1 (Gupta sample, 199) or 2 (Rose sample, 102). Arrays: id, age, s_age, hr, s_hr, and for table 1 hr_orig."""
    ids, age, sa, hr, ho, sh = [], [], [], [], [], []
    for l in open(os.path.join(CHUNG, f"table{which}.dat")):
        t = l.strip().rstrip("\\").strip()
        if not re.match(r"^\d", t): continue
        p = [v.strip() for v in t.split("&")]; m = re.match(r"^(-?[\d.]+)\s*(?:\(\s*(-?[\d.]+)\s*\))?$", p[3])
        ids.append(p[0]); age.append(float(p[1])); sa.append(float(p[2])); hr.append(float(m.group(1))); ho.append(float(m.group(2)) if m.group(2) else np.nan); sh.append(float(p[4]))
    S = D4.sako(); pos = {c: i for i, c in enumerate(S["cid"])}; ix = np.array([pos[i] for i in ids])
    return dict(id=np.array(ids), age=np.array(age), s_age=np.array(sa), hr=np.array(hr), hr_orig=np.array(ho), s_hr=np.array(sh),
                z=S["z"][ix], mass=S["logMass_Ravi"][ix], x1=S["x1"][ix], type=S["type"][ix])
